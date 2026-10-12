# Pico replacement controller (both sides, one Pico)

The stock kit is **two identical boxes**, one per end of the table. Each has 3×AA, the controller board, two single-colour LED strips and one button. This build replaces both controller boards with **one Raspberry Pi Pico** that:

- Drives all **four strips independently**, with smooth PWM fades.
- Lets **each side's button control only that side's two strips**.
- Keeps each box's own batteries powering its own strips.

## Layout

```
        SIDE 1 box (Pico lives here)                 SIDE 2 box
  ┌──────────────────────────────────┐        ┌───────────────────────────┐
  │ 3xAA ─ Pico ─ Q1a,Q1b            │ 4-wire │ 3xAA ─ Q2a,Q2b            │
  │ strip 1a, strip 1b, button 1     │════════│ strip 2a, strip 2b,       │
  └──────────────────────────────────┘ ~2.5 m │ button 2                  │
                                              └───────────────────────────┘
  Cable cores: GND, GATE_2A, GATE_2B, BUTTON_2
```

The side 2 MOSFETs sit **in the side 2 box**, so only 3.3 V logic signals cross the table and the LED current never does. The cable can be any 4-core wire: alarm cable, an old USB cable or a phone cable. It needs to be about as long as the table (8 ft ≈ 2.5 m) plus slack.

> The Pico (51 × 21 mm) is larger than the stock board (32 × 13 mm) and may not fit the stock box's board compartment. A Pico-sized project box glued or screwed to the side 1 battery box works, or use a smaller RP2040 board (Waveshare RP2040-Zero, Seeed XIAO RP2040) with the same firmware and pin numbers changed.

## Parts

| Qty | Part | Notes |
|---|---|---|
| 1 | Raspberry Pi Pico (or Pico W) | Runs on VSYS from 1.8–5.5 V, so 3×AA (3.3–4.8 V) is fine directly |
| 4 | Logic-level N-MOSFET: **AO3400** or **SI2302** (SOT-23), or a through-hole **IRLB8721** | Must be fully on at 3.3 V gate. Avoid IRF520/IRLZ44N modules. The two stock boards supply two SI2302s you can reuse. |
| 4 | 100 Ω resistor | Gate resistors, at the Pico end |
| 4 | 10 kΩ resistor | Gate pull-downs, **at each MOSFET**, so strips stay off if the cable is unplugged |
| 2 | 1 kΩ resistor | In series with each button input (protection, especially for the long cable) |
| 1 | 100 nF capacitor | Button 2 input to GND at the Pico. Filters noise picked up by the long cable. |
| 1 | 1N5817 Schottky diode | Side 1 battery+ → VSYS. Stops USB from back-feeding the AA cells while programming. |
| 2 | Small slide switch | One in each box's battery red lead. A Pico idles at ~20 mA, versus micro-amps for the stock chip, so it needs a real off switch. |
| 1 | 4-core cable + a connector at each end (JST-XH 4-pin, or a 3.5 mm TRRS jack/plug) | Lets the two sides be packed separately |
| — | Perfboard, wire, heat-shrink | |

## Wiring

### Side 1 box (with the Pico)

```
 3xAA(1) + ──[switch]──┬──[1N5817 >|]── Pico VSYS (pin 39)
                       ├── Strip 1a +
                       └── Strip 1b +
 3xAA(1) − ─────────────── Pico GND (pin 38) ── cable GND

 Strip 1a − ── drain Q1a   source ── GND
 Strip 1b − ── drain Q1b   source ── GND
 Pico GP15 (pin 20) ──[100R]──┬── gate Q1a      (10k gate → GND)
 Pico GP14 (pin 19) ──[100R]──┬── gate Q1b      (10k gate → GND)

 Pico GP13 (pin 17) ──[100R]── cable GATE_2A
 Pico GP12 (pin 16) ──[100R]── cable GATE_2B

 Button 1: GP16 (pin 21) ──[1k]── button ── GND
 Button 2: GP17 (pin 22) ──[1k]──┬── cable BUTTON_2
                                [100nF]── GND
```

### Side 2 box (no Pico; batteries power its strips only)

```
 3xAA(2) + ──[switch]──┬── Strip 2a +
                       └── Strip 2b +
 3xAA(2) − ── cable GND                (common ground with side 1)

 Strip 2a − ── drain Q2a   source ── GND
 Strip 2b − ── drain Q2b   source ── GND
 cable GATE_2A ──┬── gate Q2a      (10k gate → GND)
 cable GATE_2B ──┬── gate Q2b      (10k gate → GND)
 cable BUTTON_2 ── button ── GND
```

**Only the battery negatives are joined, through the cable GND.** Never connect the two boxes' battery positives together.

Both buttons use the Pico's internal pull-ups, so no extra pull-up resistors are needed. If button 2 ever gives phantom presses, add a 4.7 kΩ pull-up from GP17 to 3V3 (pin 36).

### Current limiting

The stock boards have a 0.3 Ω resistor in the LED return. If your strips have their own resistors (check for small SMD resistors on the strip), you don't need it. If they are bare LEDs straight across the battery, put a ~0.3–1 Ω resistor in series with each MOSFET source, or cap brightness with `MAX_BRIGHTNESS` in the firmware.

## Flashing the firmware

1. Hold BOOTSEL, plug the Pico into USB, and drop the MicroPython UF2 for your board (Pico / Pico W) onto the `RPI-RP2` drive.
2. Copy `firmware/main.py` to the Pico with Thonny or `mpremote cp firmware/main.py :main.py`.
3. Unplug USB, switch the batteries on, and it runs at power-up.

Pin assignments are all in the `SIDES` table at the top of `main.py`.

## Controls (each button affects only its own side)

| Input | Action |
|---|---|
| Single click | Next mode for that side |
| Double click | 3-second "cup made!" celebration on that side |
| Hold 0.8 s | That side on / off (soft power; use the slide switches for storage) |

Modes, in order: solid, breathe, ping-pong fade (between the side's two strips), alternate flash, strobe, heartbeat, dim.

## Upgrade ideas

- **Pico W:** host a small web page so a phone can set both sides and keep score.
- **Cup sensors:** a vibration switch or IR break-beam under each rack triggers that side's celebration automatically.
- **Addressable strips (WS2812B):** per-cup effects. Each strip needs one data wire instead of a MOSFET.
