# Pico replacement controller

Goal: replace the stock board with a Raspberry Pi Pico that keeps the same 3×AA box, strips and button, and adds:

- **Independent control of each strip.** The stock board has one MOSFET, so both strips always do the same thing.
- **Smooth PWM fades, game modes and a "made a cup" celebration.**
- Room to grow: Pico W phone control, cup sensors, addressable LEDs.

## Parts

| Qty | Part | Notes |
|---|---|---|
| 1 | Raspberry Pi Pico (or Pico W) | Runs on VSYS from 1.8–5.5 V, so 3×AA (3.3–4.8 V) is fine directly |
| 2 | Logic-level N-MOSFET: **AO3400** or **SI2302** (SOT-23), or a through-hole **IRLB8721** | Must be fully on at 3.3 V gate. Avoid IRF520/IRLZ44N modules. You can reuse Q1 from the stock board. |
| 2 | 100 Ω resistor | Gate resistors |
| 2 | 10 kΩ resistor | Gate pull-downs, so the strips stay off while the Pico boots |
| 1 | 1N5817 Schottky diode | Battery+ → VSYS. Stops USB from back-feeding the AA cells while you're programming. |
| 1 | Small slide switch | In the battery's red lead. A Pico idles at ~1–20 mA, compared with micro-amps for the stock chip, so add a real off switch. |
| 3 | 2-pin JST pigtails (or reuse the stock board's headers) | Strips A/B and button plug straight in |
| — | Perfboard, wire, heat-shrink | |

## Wiring

```
 3xAA + ──[switch]──┬──[1N5817 >|]── Pico VSYS (pin 39)
                    ├── Strip A +
                    └── Strip B +

 Strip A − ── drain Q_A   source Q_A ── GND
 Strip B − ── drain Q_B   source Q_B ── GND

 Pico GP15 (pin 20) ──[100R]──┬── gate Q_A
                             [10k]── GND
 Pico GP14 (pin 19) ──[100R]──┬── gate Q_B
                             [10k]── GND

 Button: one side ── Pico GP16 (pin 21), other side ── GND
         (internal pull-up, no resistor needed)

 3xAA − ── Pico GND (pin 38) ── all MOSFET sources
```

Keep the LED current path (strip −, MOSFET, battery −) on short, thick-ish wire. The Pico's GND just needs to be common.

### Current limiting

The stock board has a 0.3 Ω resistor in the LED return. If your strips have their own resistors (check for small SMD resistors on the strip), you don't need it. If the strips are bare LEDs directly across the battery, put a ~0.3–1 Ω resistor back in series with each MOSFET source, or cap brightness with `MAX_BRIGHTNESS` in the firmware.

### Colour-changing LEDs caveat

If the strips use **2-pin self colour-cycling LEDs** (they change colour by themselves on plain DC), fast PWM resets their internal chip and makes them glitch. Set `SMOOTH_PWM = False` in `firmware/main.py`. The firmware then only switches the strips fully on or off, which still gives flashes, alternation and strobe, just not fades.

## Flashing the firmware

1. Hold BOOTSEL, plug the Pico into USB, and drop the MicroPython UF2 for your board (Pico / Pico W) onto the `RPI-RP2` drive.
2. Copy `firmware/main.py` to the Pico with Thonny or `mpremote cp firmware/main.py :main.py`.
3. Unplug USB, switch the battery on, and it runs at power-up.

## Controls

| Input | Action |
|---|---|
| Single click | Next mode |
| Double click | 3-second "cup made!" celebration, then back to the current mode |
| Hold 0.8 s | On / off (soft power; use the slide switch for storage) |

Modes, in order: solid, breathe, ping-pong fade, alternate flash, strobe, heartbeat, team A only, team B only. Use team A/B to show whose turn it is.

## Upgrade ideas

- **Addressable strips (WS2812B):** per-cup colour, chase effects, scoreboards. They run on 4.5 V AA (marginal but works), with data from a Pico GPIO through a 330 Ω resistor. Budget battery current: 60 mA per LED at full white, so cap brightness at ~25%.
- **Pico W:** host a small web page so a phone can pick modes and keep score.
- **Cup sensors:** a vibration switch or IR break-beam under each rack triggers the celebration automatically.
