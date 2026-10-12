# Beer pong LED: reverse engineering and Pico upgrade

A stock beer pong light kit, taken apart and rebuilt around a Raspberry Pi Pico. The kit is two identical boxes, one per end of the table. Each box has 3×AA, a tiny controller board, two single-colour LED strips and a button.

![controller](docs/photos/controller-with-battery.jpg)

## What's inside (summary)

- **Power:** 3 × AA (4.5 V), soldered straight to the board's `VCC`/`GND`, with no power switch.
- **Brain:** an unmarked 8-pin OTP microcontroller.
- **Driver:** one SI2302 (`A2SHB`) N-MOSFET low-side switch with a 0.3 Ω series resistor, so **both strips always do the same thing**.
- **Connectors:** three 2-pin JST headers: strip A, strip B, button.

Full details, the inferred schematic and multimeter checks are in [`docs/teardown.md`](docs/teardown.md).

## The upgrade

[`docs/pico-build.md`](docs/pico-build.md) covers the wiring and controls, and [`docs/parts-list.md`](docs/parts-list.md) has a single-vendor parts list with cost estimates (≈ $40–52 total). [`firmware/main.py`](firmware/main.py) is the MicroPython firmware:

- One Pico drives all four strips independently with PWM (one MOSFET per strip)
- Each side's button controls only that side's two strips
- 7 modes: solid, breathe, ping-pong, alternate, strobe, heartbeat, dim
- Click = next mode, double-click = "cup made!" celebration, hold = on/off
