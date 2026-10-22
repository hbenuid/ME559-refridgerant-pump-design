# Decision log

One entry per decision. Never delete an entry; if a decision is reversed, add a new entry that supersedes it.

| ID | Date | Decision | Status |
|---|---|---|---|
| D1 | 2026-10-22 | The pump moves liquid R-134a; it is not a compressor | Decided |
| D2 | 2026-10-22 | The −20 °F to 150 °F range is the refrigerant temperature | Superseded by D9 |
| D3 | 2026-10-22 | Flow rate is ours to choose | Decided; method in D10 |
| D4 | 2026-10-22 | Hermetic construction, motor inside the shell | Decided; shell closure refined by D13 |
| D5 | 2026-10-22 | Rotor diameter fixed at 3.1 in | Constraint |
| D6 | 2026-10-22 | Tooling: Python + CoolProp for calcs, Onshape for CAD, Markdown in this repo for documentation | Decided |
| D7 | — | Vane layout: single-lobe eccentric vs. balanced double-lobe | **Open**: trade study in [functional-design.md](functional-design.md#vane-layout-trade-study) |
| D8 | — | Lubrication assumption: oil-free vs. oil present | **Open** ([Q3](open-questions.md)) |
| D9 | 2026-10-22 | The fluid is liquid at all times over −20 °F to 150 °F | Decided (course guidance) |
| D10 | 2026-10-22 | Size the smallest practical pump; flow follows from the geometry | Decided; values open ([Q2](open-questions.md)) |
| D11 | 2026-10-22 | MTBF is read literally, as a constant failure rate | Superseded by D12 |
| D12 | 2026-10-22 | MTBF is handled per industry practice: component failure-rate prediction, plus wear-out and fatigue parts sized to outlast 50,000 h | Decided |
| D13 | 2026-10-22 | Semi-hermetic: bolted housing with O-ring joints instead of a welded shell | Decided |
| D14 | 2026-10-22 | Field-maintainable where life-cycle cost justifies it, otherwise factory-refurbishable; recyclable at end of life. A refrigeration technician does field repair. | Decided; cost data open ([Q13](open-questions.md)) |
| D15 | 2026-10-22 | Inlet and outlet isolation valves built into the pump | Decided |
| D16 | — | Bearing type: product-lubricated sleeve vs. rolling-element | **Open**: trade study in [functional-design.md](functional-design.md#bearing-trade-study) |
| D17 | 2026-10-22 | The 50,000 h MTBF applies to the pump mechanism only | Decided |
| D18 | 2026-10-22 | Tooling is amortized over 5 years of production (35,000 units) | Decided |

## D1: Liquid pump

The team reads the brief as describing a liquid refrigerant pump, so the fluid is treated as incompressible.
Compression ratio and discharge temperature do not apply.

## D2: Temperature range is the refrigerant temperature (superseded)

Read literally, this conflicted with D1 above 58 °F, where R-134a at 55 psig is vapor. D9 resolves the conflict.

## D3: Flow rate is a design choice

The brief gives no flow. D10 sets how we choose it.

## D4: Hermetic

There is no shaft seal, which removes a leak path and a wear item, and with them a common failure mode against the
50,000 h MTBF. This matches how commercial refrigeration machinery is built. It costs us in two ways: motor
insulation must be compatible with the refrigerant (and with oil, if present), and the unit can't be repaired in the
field. Liquid R-134a is a dielectric, so the motor can run flooded in it and be cooled by it.

Update: D13 makes the shell bolted (semi-hermetic), so the unit can be opened for repair. The motor still runs in
the refrigerant and there is still no shaft seal.

## D5: Rotor diameter 3.1 in

Added to the brief on 2026-10-22. With the diameter fixed, the free sizing variables are eccentricity (or cam stroke),
rotor length, and vane count and thickness.

## D6: Tooling

Calculations are Python scripts in `calcs/`, using CoolProp for R-134a properties, so every number can be reproduced
and diffed. CAD is done in Onshape, with STEP and PDF snapshots stored in `cad/`. Documentation is Markdown in this
repo, which can be exported to PDF later.

## D9: Liquid at all times

Per course guidance, the R-134a is treated as liquid over the whole −20 °F to 150 °F range, even though real R-134a
at 55 psig would be vapor above 58 °F. This removes cavitation and NPSH analysis and makes 150 psig the highest
pressure. Design properties are saturated-liquid values at each temperature. The bounding cases are 150 °F (lowest
viscosity, most leakage) and −20 °F (highest viscosity and density, most drag). See
[requirements.md](requirements.md#liquid-at-all-times).

## D10: Smallest practical pump

The pump is standalone, so no system demands a particular flow. We choose the smallest eccentricity and rotor length
that can be made reliably and still pump with reasonable volumetric efficiency, and report the resulting flow. This
minimizes material, motor size and power, which is the strongest economic argument available. The likely binding
limit is leakage: it doesn't shrink with displacement, so a very small pump in a very thin liquid loses most of its
flow to leakage. See [functional-design.md](functional-design.md#sizing).

## D11: Literal MTBF (superseded)

"MTBF 50,000 hours" was taken only as a constant failure rate λ = 2.0 × 10⁻⁵ per hour. Reversed the same day in
favour of industry practice (D12).

## D12: MTBF per industry practice

Two parts, following how industry handles an MTBF requirement for mechanical equipment:

1. **Reliability prediction.** MTBF is the mean operating time between failures. It is shown by predicting each
   component's failure rate and summing them for the series system: MTBF = 1/Σλᵢ ≥ 50,000 h. NSWC-11 is the standard
   handbook for mechanical components (bearings, seals, springs, shafts, pumps); motor and terminal rates come from
   vendor data. This assumes a constant failure rate during useful life, so a population meeting the MTBF still sees
   about 16% failures a year.
2. **Wear-out kept beyond the life.** The constant-rate assumption only holds if nothing wears out within 50,000 h.
   So bearings are sized for L10h ≥ 50,000 h (ISO 281 rating life). That is double API 610's 25,000 h minimum for
   pump bearings and within the 40,000–60,000 h range that guideline tables give for continuous-duty pumps. Vanes
   and ring get a wear allowance for 50,000 h, and fatigue-loaded parts are designed for infinite life.

See [functional-design.md](functional-design.md#reliability).

## D13: Semi-hermetic, bolted housing

The goal in D14 rules out a welded shell, which can only be opened by cutting and in practice is scrapped rather
than rebuilt. A bolted housing with O-ring joints keeps the main benefit of D4 (no shaft seal, motor cooled by the
liquid) and can be opened both in the field and at the factory. Semi-hermetic commercial compressors are built this
way and are routinely field-repaired and remanufactured. Costs: heavier cast and machined housing sections, static
O-ring leak paths, and bolted joints that must hold preload under pressure cycles.

## D14: Serviceability goal

The pump should be field-maintainable where that is worth it. Otherwise it should be designed for refurbishment by
the manufacturer, and for recycling at end of life.

- **Who**: field work is done by a refrigeration technician, who is equipped to recover and recharge refrigerant.
- **How we decide**: "worth it" is settled per failure mode by life-cycle cost, comparing field repair against a
  swap plus factory remanufacture.

See [serviceability.md](serviceability.md).

## D15: Integral isolation valves

Valves on the pump's inlet and outlet let a technician isolate the pump and recover only its own small charge
instead of the system's. This makes field repair much cheaper, at the cost of the valves and two more potential leak
points.

## D17: MTBF scope is the pump mechanism

The 50,000 h MTBF budget (Σλᵢ ≤ 2.0 × 10⁻⁵ per hour) covers the pump mechanism: the cartridge (ring, rotor, vanes,
side plates), the shaft and the bearings. The motor, terminal and isolation valves are purchased parts, judged
separately against their suppliers' ratings. The housing O-ring joints are also outside the budget.

## D18: 5-year production horizon

Tooling is amortized over 5 years × 7,000 units/yr = 35,000 units. This is conservative: it favours processes with
low tooling cost, so any tooling-heavy process (powder metal, dies) has to justify itself over 35,000 units.
