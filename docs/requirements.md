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
| 2026-10-29 | Final documentation and presentation handout: what is due and how it is judged | See [Final deliverables](#final-deliverables) |

## Interpretation

How we read the brief, as of 2026-11-05. The reasoning for each line is in [decisions.md](decisions.md).

| Item | Interpretation |
|---|---|
| Substance | The pump moves **liquid** R-134a. It is a true pump, not a compressor ([D1](decisions.md)). |
| Temperature | The refrigerant temperature, and the fluid is **liquid at all times** across it ([D9](decisions.md)). |
| Design pressure | **300 psig**, set by a pump standing idle at 150 °F (263 psig, rounded up). The running maximum is the 150 psig outlet ([D32](decisions.md), [real-fluid check](#real-fluid-check)). |
| System | Standalone pump. There is no refrigeration loop to size against. |
| Flow rate | Not given. We design the **smallest practical pump**, and the flow follows from that geometry ([D10](decisions.md)). |
| Construction | **Sealless, magnetic drive**: the pump sits in a bolted housing with O-ring joints, and a standard motor outside drives it through a magnetic coupling across a containment can. There is no shaft seal, and the housing can be opened for service ([D13](decisions.md), [D33](decisions.md)). Until D33 the motor ran inside the housing ([D4](decisions.md)). |
| Serviceability | Field-repairable by a refrigeration technician where life-cycle cost favours it; otherwise refurbished by the manufacturer; recyclable at end of life ([D14](decisions.md), [serviceability.md](serviceability.md)). |
| Lubrication | Open ([Q3](open-questions.md)). The team expects to add a lubricant; type, amount and ratio aren't chosen. |
| MTBF | Industry practice: predicted MTBF ≥ 50,000 h, with wear-out and fatigue parts sized to outlast it ([D12](decisions.md)). It applies to the pump mechanism only ([D17](decisions.md)). |
| Duty cycle | Continuous, 8,760 h/yr, from the brief's "continuous operation". The failure figures in [functional-design.md](functional-design.md#reliability) already assume it. |
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

- **Cavitation**: no NPSH or cavitation analysis. The inlet is always fully liquid. Real R-134a can boil at the
  inlet; see the [real-fluid check](#real-fluid-check).
- **Properties**: saturated-liquid values at each temperature are the design properties (table below).
- **Bounding cases**: two temperatures bound the design.
  - **150 °F** has the lowest viscosity, which gives the most internal leakage.
  - **−20 °F** has the highest viscosity and density, which gives the most drag and power. It is also the furthest
    from room-temperature assembly (90 °F colder) for clearance changes.
- **Pressure**: the highest running pressure is the 150 psig outlet. The highest pressure overall comes when the
  pump is idle, which sets the 300 psig design pressure ([D32](decisions.md), [below](#real-fluid-check)).

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

### Real-fluid check

From the teammates' *Pump Temp Analysis* (2026-11-05, [references.md](references.md#team-notes)), with numbers from
[calcs/pressure_cases.py](../calcs/pressure_cases.py). The course basis above stays for performance ([D9](decisions.md)).
This check sets the design pressure ([D32](decisions.md)), and its cavitation and vapor lock cases are logged as
real-world risks outside the course basis ([functional-design.md](functional-design.md#functional-risks)).

The team's proposed ranges: the liquid runs from −20 °F to 50 °F at the 55 psig inlet and up to about 52 °F at the
outlet. The −20 °F to 150 °F envelope stays for materials, seals and the pressure rating, covering ambient, storage
and shutdown.

**Upper inlet limit, 50 °F.** The inlet is the lowest pressure in the pump, so the liquid is closest to boiling there,
and the local pressure dips a little further as liquid enters the vane cells. If it reaches the vapor pressure,
bubbles form and collapse (cavitation), damaging surfaces and cutting flow. A 10 psi margin between the inlet
pressure and the vapor pressure caps the inlet at about 50 °F:

| Inlet temp (°F) | Psat (psig) | Margin below the 55 psig inlet (psi) |
|---|---|---|
| -20 | -1.8 | 56.8 |
| 40 | 35.0 | 20.0 |
| 45 | 40.1 | 14.9 |
| 50 | 45.4 | 9.6 |
| 55 | 51.2 | 3.8 |
| 58 | 54.9 | 0.1 |

**Lower limit, −20 °F.** Set by the parts, not the fluid: colder liquid is further from boiling, and R-134a doesn't
freeze until −154 °F. The limits are elastomer seal flexibility, clearance changes from contraction, and the toughness
of cast iron.

**Outlet temperature.** Raising a liquid's pressure barely heats it, unlike compressing a gas. The only rise comes
from internal losses (friction, churning, leakage). Treating all shaft work as heat gives an upper bound,
ΔT ≤ Δp / (ρ·η·c_p):

| Inlet temp (°F) | ρ (kg/m³) | c_p (J/kg·K) | ΔT bound at η = 40% (°F) | Outlet temp (°F) | Margin below Tsat at 150 psig (°F) |
|---|---|---|---|---|---|
| -20 | 1385 | 1275 | 1.7 | -18.3 | 130 |
| 50 | 1261 | 1370 | 1.7 | 51.7 | 60 |

The outlet stays about 60 °F below the 111.5 °F boiling point at 150 psig, so the fluid stays liquid through the pump.

**Idle pressure.** While the pump runs, the liquid is cold and the highest pressure is the 150 psig outlet. When it
stops, it is a sealed container of refrigerant. If the room warms (the envelope goes to 150 °F), some liquid boils
and the pressure climbs to the saturation pressure at that temperature:

| Idle pump temperature (°F) | Pressure in the pump (psig) |
|---|---|
| 80 | 87 |
| 100 | 124 |
| 120 | 171 |
| 130 | 199 |
| 140 | 229 |
| 150 | 263 |

So the pump sees its highest pressure while doing nothing. The team rounds 263 psig up to **300 psig** for hot spots,
pressure spikes and the relief setting, and designs the body, bolts and seals for it ([D32](decisions.md)). 300 psig is
the saturation pressure at 160 °F.

## Derived values

- **Differential pressure**: 95 psi. The absolute pressure ratio (2.36) would matter only for a compressor.
- **Absolute pressures**: 69.7 psia at the inlet and 164.7 psia at the outlet (psig + 14.7).
- **Angular speed**: ω = 2πn/60 = 377 rad/s ([calcs/vane_kinematics.py](../calcs/vane_kinematics.py)).
- **Vane tip speed** at the 3.1 in rotor OD and 3600 RPM: π × 3.1 in × 60 rev/s = 584 in/s = **48.7 ft/s
  (14.8 m/s)**. At an illustrative 3.22 in cam bore (e = 0.06 in), the average tip speed is 50.6 ft/s (15.4 m/s). With
  the rotor diameter and speed both fixed, it can't be lowered.
- **Centripetal acceleration** at the rotor rim: ω²r ≈ 570 g. This is what holds the vanes against the ring
  ([functional-design.md](functional-design.md#vane-tip-wear)).
- **Sliding distance**: the vane tips slide about 2.8 × 10⁹ m (2.8 million km) over 50,000 h.
- **Outlet temperature rise**: at most about 1.7 °F ([real-fluid check](#real-fluid-check)).
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
| Dielectric | Mattered while the motor ran in the liquid ([D4](decisions.md)). With the magnetic drive the motor is outside ([D33](decisions.md)). |
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
- **Flooding and humidity**: a basement can flood. The housing joints and the external motor (its enclosure rating)
  need to tolerate a wet environment.
- **Codes**: refrigerant equipment inside occupied buildings falls under safety standards such as ASHRAE 15. Which
  ones apply to this pump is [Q7](open-questions.md).

## Final deliverables

From the course handout *Final Report and Presentation* ([references.md](references.md)). Everything is due on the
day of the final presentation. The handout doesn't give that date ([Q19](open-questions.md)).

### Drawings and CAD

| Item | Requirement |
|---|---|
| Scope | 3D CAD models, assemblies and drawings for every part, including off-the-shelf (OTS) parts. Fasteners are the only exception. |
| Part numbers | Every part, OTS included, has a unique part number assigned by us. The scheme is assembly-coded ([D19](decisions.md)). |
| OTS part drawings | Overall dimensions, vendor name and vendor part number. Our part number goes in the title block; the vendor's goes in a note. |
| Made-part drawings | Communicate design intent and show an understanding of the material and process chosen. Dimensions of size, location, orientation and form (SLOF), using GD&T where it applies. |
| Cast or molded parts | Any part made in a reusable mold or pattern also shows the parting line, draft angle, and proposed gate and ejector locations, where they apply. |
| Revision table | On every drawing, at "Initial Release". |
| Assembly drawings | Exploded and unexploded views, as needed to show how the pump is assembled. |
| BOM | A table in the upper-left corner of the assembly drawing. It lists every part (made and OTS) with its balloon number on the exploded view, our part number and the quantity. Consumables (grease, thread locker, etc.) are listed too, with where each is used. Fasteners are listed by standard designation, with torque, and get no drawing ([D20](decisions.md)). |
| Torque specs | For every threaded fastener. They needn't be rigorous, but fastener size must suit the load. |
| Paper copies | All part and assembly drawings printed on B-size sheets (11 × 17 in) and handed in at the presentation. |

### Digital folder

Uploaded to a team folder in the ME559 shared folder. The handout's ME691 is left over from another course
([Q17](open-questions.md#answered)). Four subfolders:

1. Drawings (PDF)
2. CAD Models (STEP)
3. Supporting Documentation: material comparisons and cost comparisons (PDF)
4. Final Presentation (PDF)

Other supporting information can be added as PDF.

### Presentation

- Up to 10 minutes **including Q&A**, timed.
- Start with the project specifics: fluid, yearly production, operating pressure and temperature, duty cycle.
- Then the final product; the material, design and manufacturing decisions; and the **predicted production cost per
  pump**. Be ready to defend them in Q&A.
- CAD models, animations, calculations, material choices and cost comparisons can all be shown. Pick what shows the
  problems solved and why the solutions were right.

### How it is judged

The handout's criteria: "Did you make reasonable engineering choices; and excellent design, and manufacturing
choices? Did you properly communicate those choices in your drawings, documentation, and presentation?" It gives no
weights ([Q8](open-questions.md)).

### What it means for the design

| Requirement | Effect |
|---|---|
| OTS drawings carry a vendor part number | The motor, magnetic coupling, bearings, isolation valves, relief valves and O-rings each have to end in a specific catalog part. The bearing trade ([D16](decisions.md)) and the piping connection ([Q14](open-questions.md)) end in vendor selections. |
| Casting and molding callouts | Each process choice adds drawing content. See [manufacturing.md](manufacturing.md#drawing-requirements). |
| GD&T | The [critical-to-function features](manufacturing.md#critical-to-function-features) are the main callouts. |
| Torque specs | Housing bolts are sized against the 300 psig design pressure ([D32](decisions.md)). |
| Consumables in the BOM | Anything used inside the housing sits in refrigerant. See [materials.md](materials.md#consumables). |
| Material and cost comparisons | [materials.md](materials.md) and [economics.md](economics.md) are the sources for these two supporting documents. |
| Cost per pump | The cost model in [economics.md](economics.md) has to produce a number. |
| Duty cycle | Continuous ([Interpretation](#interpretation)). |
