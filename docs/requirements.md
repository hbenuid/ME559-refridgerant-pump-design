# Requirements

## Given (course brief)

| Item | Value |
|---|---|
| Substance | R-134a refrigerant |
| Temperature | −20 °F to 150 °F |
| Inlet pressure | 55 psig |
| Outlet pressure | 150 psig |
| Speed | 3600 RPM |
| MTBF | 50,000 hours continuous operation |
| Installation | Basement of a commercial building in Arizona |
| Yearly quantity | 7,000 units per year |

Added 2026-10-22: **rotor diameter must be 3.1 in.**

## Course guidance

Clarifications received after the brief.

| Date | Guidance | Effect |
|---|---|---|
| 2026-10-22 | Treat the R-134a as liquid at all times, over the full −20 °F to 150 °F range | [D9](decisions.md). See [below](#liquid-at-all-times). |
| 2026-10-22 | The pump is standalone: it has to pump at the given specs, not serve a larger system | Flow is ours to set ([D10](decisions.md)) |
| 2026-10-22 | R-134a has properties that make it easier to pump than other liquids (no specifics given) | Our reading is [below](#r-134a-as-a-pumped-liquid) |
| 2026-10-22 | 80% of mechanical failures are due to fatigue | [Fatigue section](functional-design.md#fatigue) |
| 2026-10-22 | R-134a will be replaced in the assignment next year | Regulatory phase-down is out of scope ([Q10](open-questions.md#answered)) |

## Interpretation

How we read the brief, as of 2026-10-22. The reasoning for each line is in [decisions.md](decisions.md).

| Item | Interpretation |
|---|---|
| Substance | The pump moves **liquid** R-134a. It is a true pump, not a compressor ([D1](decisions.md)). |
| Temperature | The refrigerant temperature, and the fluid is **liquid at all times** across it ([D9](decisions.md)). |
| System | Standalone pump. There is no refrigeration loop to size against. |
| Flow rate | Not given. We design the **smallest practical pump**, and the flow follows from that geometry ([D10](decisions.md)). |
| Construction | **Semi-hermetic**: the motor runs inside a bolted housing with the refrigerant. There is no shaft seal, and the housing can be opened for service ([D4](decisions.md), [D13](decisions.md)). |
| Serviceability | Field-repairable by a refrigeration technician where life-cycle cost favours it; otherwise refurbished by the manufacturer; recyclable at end of life ([D14](decisions.md), [serviceability.md](serviceability.md)). |
| Lubrication | Open. Unknown whether oil is present ([Q3](open-questions.md)). |
| MTBF | Industry practice: predicted MTBF ≥ 50,000 h, with wear-out and fatigue parts sized to outlast it ([D12](decisions.md)). It applies to the pump mechanism only ([D17](decisions.md)). |
| Production horizon | 5 years, 35,000 units, for amortizing tooling ([D18](decisions.md)). |
| Electrical supply | Not specified. Assumed 208–230 V, 3-phase ([Q6](open-questions.md)). |
| Noise | No target given. Minimise it as a quality, with no number. |

## Liquid at all times

Real R-134a at the 55 psig inlet is liquid only below 58 °F. At 150 °F its saturation pressure is 263 psig, above even
the 150 psig outlet. The course says to treat it as liquid anyway, and we'll note this in our work as a stated
simplification.

| Point | Pressure (psig) | Pressure (psia) | Saturation temp (°F) |
|---|---|---|---|
| Inlet | 55 | 69.7 | 58.1 |
| Outlet | 150 | 164.7 | 111.5 |

What this means for the design:

- **Cavitation**: no NPSH or cavitation analysis. The inlet is always fully liquid.
- **Properties**: saturated-liquid values at each temperature are the design properties (table below).
- **Bounding cases**: two temperatures bound the design.
  - **150 °F** has the lowest viscosity, which gives the most internal leakage.
  - **−20 °F** has the highest viscosity and density, which gives the most drag and power. It is also the furthest
    from room-temperature assembly (90 °F colder) for clearance changes.
- **Pressure**: the highest pressure in the brief is the 150 psig outlet. There are no saturation-pressure cases to
  design for ([Q9](open-questions.md)).

Design properties from [calcs/r134a_properties.py](../calcs/r134a_properties.py) (CoolProp 8.0):

| Fluid temp (°F) | ρ (lb/ft³) | μ (cP) | ν (cSt) | Psat (psig) | Actual state at 55 psig |
|---|---|---|---|---|---|
| -20 | 86.5 | 0.394 | 0.285 | -1.8 | liquid |
| 0 | 84.4 | 0.337 | 0.249 | 6.5 | liquid |
| 20 | 82.2 | 0.291 | 0.221 | 18.4 | liquid |
| 40 | 79.9 | 0.252 | 0.197 | 35.0 | liquid |
| 58 | 77.7 | 0.222 | 0.178 | 54.9 | liquid |
| 80 | 74.9 | 0.191 | 0.159 | 86.7 | vapor |
| 100 | 72.2 | 0.166 | 0.144 | 124.2 | vapor |
| 112 | 70.4 | 0.152 | 0.135 | 151.1 | vapor |
| 120 | 69.1 | 0.144 | 0.130 | 171.2 | vapor |
| 150 | 63.8 | 0.114 | 0.112 | 262.9 | vapor |

For comparison, water at 68 °F has μ = 1.00 cP and ν = 1.00 cSt. Liquid R-134a is 2.5 to 9 times thinner than water.

## Derived values

- **Differential pressure**: 95 psi. The absolute pressure ratio (2.36) would matter only for a compressor.
- **Vane tip speed** at the 3.1 in rotor OD and 3600 RPM: π × 3.1 in × 60 rev/s = 584 in/s = **48.7 ft/s
  (14.8 m/s)**.
- **Speed**: 3600 RPM is the synchronous speed of a 2-pole motor on 60 Hz. An induction motor runs with slip at
  roughly 3450–3550 RPM under load. Flow tables use 3600 as an upper bound ([Q4](open-questions.md)).
- **Production rate**: 7,000 units/yr is about 28 units per working day (250 days), or 3.5 per hour on one 8-hour
  shift.
- **MTBF**: the predicted failure rate must be at most 1/50,000 h = 2.0 × 10⁻⁵ per hour, with bearings at
  L10h ≥ 50,000 h. A population meeting this MTBF still sees about 16% failures a year from random causes. See
  [functional-design.md](functional-design.md#reliability).
- **Fatigue cycles**: 1.08 × 10¹⁰ shaft revolutions in 50,000 h ([functional-design.md](functional-design.md#fatigue)).

## R-134a as a pumped liquid

The course hinted that R-134a has properties that make it easier to pump than other liquids, without naming them
([Q11](open-questions.md)). Our reading:

| Helps | Why |
|---|---|
| Low viscosity (0.11–0.39 cP) | Little viscous drag on the rotor faces and vanes, so friction power is low. Pockets fill easily at 3600 RPM, and pressure drop through the ports is small. |
| Clean and non-abrasive | No particles to erode vanes and ring, unlike slurries or dirty water. |
| Not corrosive to common metals when dry; not an electrolyte | Cast iron, carbon steel and aluminium are usable without stainless. Dissimilar metals don't form galvanic couples the way they would in water. (Verify against a compatibility source.) |
| Dielectric | The hermetic motor can run flooded in the liquid and be cooled by it. |
| Chemically stable, non-flammable, low toxicity (ASHRAE 34 class A1) | No explosion-proof motor is needed, and the unit is safe inside an occupied building. |

| Hurts | Why |
|---|---|
| Low viscosity | Leakage through a clearance scales as c³/μ. There's almost no hydrodynamic film for vanes and bearings. |
| No lubricity of its own | Vanes and bearings run in boundary lubrication unless oil is present ([Q3](open-questions.md)). |
| Attacks some elastomers | For example, FKM (Viton) is commonly listed as not recommended ([materials.md](materials.md)). |
| Escapes readily | Any external leak loses fluid, which is a good reason for a sealless design with only static seals. |

## Installation: basement of a commercial building in Arizona

What this implies for the design. These are notes to research, not settled requirements.

- **Noise and vibration**: the unit sits inside an occupied building, and a basement transmits structure-borne noise.
  This favors balanced rotating parts and vibration isolation, and it bears on vane count (pressure pulsation).
- **Access and service**: at about 16% of units failing per year at the 50,000 h MTBF, service in a basement is a
  large cost. That's why the pump is built to be repaired on site or swapped and remanufactured
  ([serviceability.md](serviceability.md)). Parts and tools have to be carried down to the plant room.
- **Ambient**: a basement moderates temperature compared with a roof. Arizona's long cooling season means high
  annual run hours.
- **Flooding and humidity**: a basement can flood. The housing joints and electrical terminal need to tolerate a wet
  environment.
- **Codes**: refrigerant equipment inside occupied buildings falls under safety standards such as ASHRAE 15. Which
  ones apply to a semi-hermetic pump is [Q7](open-questions.md).
