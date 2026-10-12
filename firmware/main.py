# Beer pong LED controller for Raspberry Pi Pico (MicroPython).
#
# Two LED strips switched by logic-level N-MOSFETs on STRIP_PINS,
# one push button to GND on BUTTON_PIN. See docs/pico-build.md for wiring.

import math
import time
from machine import Pin, PWM

STRIP_PINS = (15, 14)   # GP15 = strip A, GP14 = strip B
BUTTON_PIN = 16
PWM_FREQ = 1000
MAX_BRIGHTNESS = 1.0    # lower this to save battery / limit LED current
SMOOTH_PWM = True       # False for self colour-cycling LEDs (on/off only)
CELEBRATE_MS = 3000


class Strip:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(PWM_FREQ)
        self.set(0)

    def set(self, level):
        level = min(max(level, 0.0), 1.0)
        if not SMOOTH_PWM:
            level = 1.0 if level >= 0.5 else 0.0
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


# Patterns: t = ms since the mode started -> (strip A level, strip B level).

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


def team_a(t):
    return wave(t, 1500) * 0.7 + 0.3, 0


def team_b(t):
    return 0, wave(t, 1500) * 0.7 + 0.3


def celebrate(t):
    # Fast alternating strobe.
    phase = (t // 60) % 4
    return (1, 0) if phase == 0 else (0, 1) if phase == 2 else (0, 0)


MODES = (solid, breathe, ping_pong, alternate, strobe, heartbeat, team_a, team_b)


def main():
    strips = [Strip(p) for p in STRIP_PINS]
    button = Button(BUTTON_PIN)
    mode = 0
    on = True
    start = time.ticks_ms()
    celebrate_start = None

    while True:
        now = time.ticks_ms()
        event = button.poll(now)
        if event == "long":
            on = not on
            start = now
            celebrate_start = None
        elif on and event == "click":
            mode = (mode + 1) % len(MODES)
            start = now
        elif on and event == "double":
            celebrate_start = now

        if not on:
            levels = (0, 0)
        elif celebrate_start is not None \
                and time.ticks_diff(now, celebrate_start) < CELEBRATE_MS:
            levels = celebrate(time.ticks_diff(now, celebrate_start))
        else:
            celebrate_start = None
            levels = MODES[mode](time.ticks_diff(now, start))

        for strip, level in zip(strips, levels):
            strip.set(level)
        time.sleep_ms(10 if on else 25)


main()
