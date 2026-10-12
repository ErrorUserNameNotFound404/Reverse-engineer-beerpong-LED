# Parts list and cost estimate

Everything below except the cross-table cable comes from **one distributor (DigiKey)**, so you pay one shipping charge. Mouser carries the same manufacturer part numbers (and Adafruit boards) if you prefer it.

> Prices are estimates from distributor listings checked in October 2026 (single-unit pricing, USD) and change often. Check the live cart before ordering. Search DigiKey by the **manufacturer part number (MPN)**. Sales tax is not included.

## Order from DigiKey

| Qty | Part | MPN | Est. each | Est. total | Used for |
|---|---|---|---|---|---|
| 1 | Raspberry Pi Pico H (headers pre-soldered) | `SC0917` | $5.00 | $5.00 | Controller (use Pico WH `SC0919`, ~$7, if you want phone control later) |
| 4 | N-MOSFET, logic level, TO-220 | `IRLB8721PBF` | $1.60 | $6.40 | One switch per strip (2 per box) |
| 10 | 100 Ω ¼ W resistor | `CF14JT100R` | $0.10 | $1.00 | Gate resistors (4 used) |
| 10 | 10 kΩ ¼ W resistor | `CF14JT10K0` | $0.10 | $1.00 | Gate pull-downs (4 used) |
| 10 | 1 kΩ ¼ W resistor | `CF14JT1K00` | $0.10 | $1.00 | Button input protection (2 used) |
| 2 | 100 nF ceramic capacitor | `C320C104K5R5TA` | $0.35 | $0.70 | Button 2 noise filter (1 used, 1 spare) |
| 2 | 1N5817 Schottky diode | `1N5817RLG` | $0.45 | $0.90 | Battery → Pico VSYS (1 used, 1 spare) |
| 2 | SPDT slide switch, through-hole | `EG1218` | $0.85 | $1.70 | Real off switch in each box's battery lead (rated 200 mA; see the note below) |
| 2 | 4-position 5.08 mm PCB screw terminal | `1729144` (Phoenix Contact) | $2.00 | $4.00 | Cable connection at each box |
| 2 | Adafruit Perma-Proto quarter- or half-size board | search "Perma-Proto" | $3.00–4.50 | $6.00–9.00 | One small board per box |
| | | | | **≈ $28–31** | **Parts subtotal** |
| | DigiKey standard US ground shipping | | | **≈ $7** | Check the cart; small orders don't qualify for free shipping |
| | | | | **≈ $35–38** | **DigiKey order total, before tax** |

## Buy locally (hardware store, no shipping)

| Qty | Part | Est. cost | Notes |
|---|---|---|---|
| ~10–15 ft | 4-conductor wire: 18/4 or 20/4 thermostat wire, or alarm/security cable | $5–12 | Runs GND, GATE_2A, GATE_2B and BUTTON_2 across the table. Measure your table plus slack; an 8 ft table needs about 10 ft. |

## Already have (or add to the order if not)

- Solder, soldering iron, flush cutters, small hookup wire (22 AWG), heat-shrink tubing.
- The two stock kits supply the battery boxes, 4 LED strips, 2 buttons and the strip/button JST pigtails. You can also salvage the stock boards' two SI2302 MOSFETs as spares.
- A micro-USB cable to flash the Pico.

## Estimated total

| | Low | High |
|---|---|---|
| DigiKey parts | $28 | $31 |
| DigiKey shipping | $7 | $9 |
| Local 4-core cable | $5 | $12 |
| **Total (before tax)** | **≈ $40** | **≈ $52** |

## Notes on part choices

- **Through-hole TO-220 MOSFETs** (IRLB8721) are much easier to solder on perfboard than the stock SOT-23 parts, and they switch fully on from the Pico's 3.3 V. They're overkill for current, which is fine.
- **Slide switch rating:** EG1218 is rated 200 mA. Measure one box's current with both strips fully on (meter in series with the battery's red wire). If it's over ~150 mA, pick a slide or rocker switch rated ≥ 1 A from DigiKey's switch filters instead (about $1–3).
- **Screw terminals** let you unscrew the cable so the two sides pack separately. For a plug-in connection instead, a 4-pin JST-XH header and housing pair works but needs a crimp tool.
- **Resistors in 10s:** they cost little more than single pieces and leave spares.
