# Beer pong LED controller for Raspberry Pi Pico (MicroPython).
#
# One Pico drives both sides of the table. Each side has two single-colour
# LED strips (switched by logic-level N-MOSFETs) and one push button to GND.
# A side's button only controls that side's strips. See docs/pico-build.md.

import math
import time
from machine import Pin, PWM

# (name, (strip 1 pin, strip 2 pin), button pin)
SIDES = (
    ("side 1", (15, 14), 16),   # local box (Pico lives here)
    ("side 2", (13, 12), 17),   # remote box, via the cable across the table
)
PWM_FREQ = 1000
MAX_BRIGHTNESS = 1.0    # lower this to save battery / limit LED current
CELEBRATE_MS = 3000


class Strip:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(PWM_FREQ)
        self.set(0)

    def set(self, level):
        level = min(max(level, 0.0), 1.0)
        # Square for a rough perceptual (gamma) curve.
        self.pwm.duty_u16(int(level * level * MAX_BRIGHTNESS * 65535))


class Button:
    DEBOUNCE_MS = 30
    LONG_MS = 800
    DOUBLE_MS = 300

    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.raw = self.stable = self.pin.value()
        self.last_change = time.ticks_ms()
        self.press_start = 0
        self.last_release = 0
        self.clicks = 0
        self.long_fired = False

    def poll(self, now):
        """Return 'click', 'double', 'long' or None."""
        raw = self.pin.value()
        if raw != self.raw:
            self.raw = raw
            self.last_change = now
        if raw != self.stable and time.ticks_diff(now, self.last_change) >= self.DEBOUNCE_MS:
            self.stable = raw
            if raw == 0:
                self.press_start = now
                self.long_fired = False
            elif not self.long_fired:
                self.clicks += 1
                self.last_release = now

        if self.stable == 0 and not self.long_fired \
                and time.ticks_diff(now, self.press_start) >= self.LONG_MS:
            self.long_fired = True
            self.clicks = 0
            return "long"
        if self.clicks and self.stable == 1 \
                and time.ticks_diff(now, self.last_release) >= self.DOUBLE_MS:
            clicks, self.clicks = self.clicks, 0
            return "double" if clicks >= 2 else "click"
        return None


# Patterns: t = ms since the mode started -> (strip 1 level, strip 2 level).

def wave(t, period):
    return (1 - math.cos(2 * math.pi * (t % period) / period)) / 2


def solid(t):
    return 1, 1


def breathe(t):
    v = wave(t, 3000)
    return v, v


def ping_pong(t):
    v = wave(t, 2000)
    return v, 1 - v


def alternate(t):
    return (1, 0) if (t // 400) % 2 == 0 else (0, 1)


def strobe(t):
    v = 1 if t % 120 < 40 else 0
    return v, v


def heartbeat(t):
    p = t % 1200
    v = 1 if p < 100 or 250 <= p < 350 else 0.1
    return v, v


def dim(t):
    return 0.35, 0.35


def celebrate(t):
    # Fast alternating strobe.
    phase = (t // 60) % 4
    return (1, 0) if phase == 0 else (0, 1) if phase == 2 else (0, 0)


MODES = (solid, breathe, ping_pong, alternate, strobe, heartbeat, dim)


class Side:
    def __init__(self, name, strip_pins, button_pin):
        self.name = name
        self.strips = [Strip(p) for p in strip_pins]
        self.button = Button(button_pin)
        self.mode = 0
        self.on = True
        self.start = time.ticks_ms()
        self.celebrate_start = None

    def update(self, now):
        event = self.button.poll(now)
        if event == "long":
            self.on = not self.on
            self.start = now
            self.celebrate_start = None
        elif self.on and event == "click":
            self.mode = (self.mode + 1) % len(MODES)
            self.start = now
        elif self.on and event == "double":
            self.celebrate_start = now

        if not self.on:
            levels = (0, 0)
        elif self.celebrate_start is not None \
                and time.ticks_diff(now, self.celebrate_start) < CELEBRATE_MS:
            levels = celebrate(time.ticks_diff(now, self.celebrate_start))
        else:
            self.celebrate_start = None
            levels = MODES[self.mode](time.ticks_diff(now, self.start))

        for strip, level in zip(self.strips, levels):
            strip.set(level)


def main():
    sides = [Side(*cfg) for cfg in SIDES]
    while True:
        now = time.ticks_ms()
        for side in sides:
            side.update(now)
        time.sleep_ms(10)


main()
