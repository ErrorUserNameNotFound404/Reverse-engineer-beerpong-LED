# Beer pong LED: reverse engineering and Pico upgrade

A stock beer pong light kit (3×AA box, tiny controller board, two LED strips and a button), taken apart and rebuilt around a Raspberry Pi Pico.

![controller](docs/photos/controller-with-battery.jpg)

## What's inside (summary)

- **Power:** 3 × AA (4.5 V), soldered straight to the board's `VCC`/`GND`, with no power switch.
- **Brain:** an unmarked 8-pin OTP microcontroller.
- **Driver:** one SI2302 (`A2SHB`) N-MOSFET low-side switch with a 0.3 Ω series resistor, so **both strips always do the same thing**.
- **Connectors:** three 2-pin JST headers: strip A, strip B, button.

Full details, the inferred schematic and multimeter checks are in [`docs/teardown.md`](docs/teardown.md).

## The upgrade

[`docs/pico-build.md`](docs/pico-build.md) covers the parts list, wiring and controls. [`firmware/main.py`](firmware/main.py) is the MicroPython firmware:

- Independent PWM on each strip (two MOSFETs instead of one)
- 8 modes: solid, breathe, ping-pong, alternate, strobe, heartbeat, team A, team B
- Click = next mode, double-click = "cup made!" celebration, hold = on/off
