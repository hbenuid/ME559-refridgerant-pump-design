# Functional design

Rubric: *ability to make functionally sound design choices* (17.5%).

## Operating principle

A slotted rotor turns inside a cam ring. Vanes slide in the rotor slots and are held against the ring by centrifugal
force, plus under-vane pressure or springs. The ring is shaped (offset, or non-circular) so the space between two
adjacent vanes grows over the inlet port and shrinks over the outlet port. Each pocket fills with liquid and then
pushes it out. In our semi-hermetic layout, the motor rotor sits on the same shaft inside the bolted housing, and the pumped
refrigerant (or a bleed of it) cools the motor.

## Sizing

The rotor diameter is fixed at 3.1 in. The free variables are eccentricity e (or cam stroke s), rotor length L, vane
count z and vane thickness t.

### Displacement

Treat the liquid between vanes as rotating rigidly with the rotor. Where the ring sits at radius ρ from the rotor
centre, the flow crossing a radial line is q = ωL(ρ² − R_r²)/2. Net delivery is the difference in q between the
widest and narrowest points.

- **Single-lobe** (round ring of diameter D_c, offset e): ρ runs from R_c − e to R_c + e, so per revolution
  V = πL(ρ_max² − ρ_min²) = 2πeLD_c. The vanes stroke 2e once per revolution and take up z·t·2e·L, giving
  **V = 2eL(πD_c − zt)**, with D_c = D_r + 2e when the rotor is tangent to the ring at the seal arc.
- **Balanced double-lobe** (cam ring with major radius R_a, minor radius R_b ≈ R_r, stroke s = R_a − R_b): there are
  two suction and two discharge zones per revolution, giving **V = 2L[π(R_a² − R_b²) − zts]**.

Check before relying on this: Esposito, *Fluid Power with Applications*, gives V = (π/2)(D_c + D_r)eL for the
single-lobe pump. That is about half the value above. The derivation here counts each pocket's full swing from
minimum to maximum volume, and the 2eL(πD − zt) form also appears in hydraulics literature (source to add to
[references.md](references.md)). Confirm against a second source.

Theoretical flow from [calcs/displacement.py](../calcs/displacement.py) at 3600 RPM, 100% volumetric efficiency, with
placeholder z = 8 and t = 0.10 in:

**Single-lobe**, flow in GPM:

| Eccentricity e (in) | L = 0.75 in | L = 1.0 in | L = 1.5 in | L = 2.0 in |
|---|---|---|---|---|
| 0.050 | 10.8 | 14.4 | 21.6 | 28.8 |
| 0.075 | 16.5 | 22.0 | 33.0 | 44.0 |
| 0.100 | 22.4 | 29.8 | 44.7 | 59.6 |
| 0.125 | 28.4 | 37.9 | 56.8 | 75.8 |
| 0.150 | 34.6 | 46.2 | 69.3 | 92.4 |

**Balanced double-lobe**, flow in GPM:

| Cam stroke s (in) | L = 0.75 in | L = 1.0 in | L = 1.5 in | L = 2.0 in |
|---|---|---|---|---|
| 0.050 | 10.6 | 14.2 | 21.3 | 28.4 |
| 0.075 | 16.1 | 21.4 | 32.2 | 42.9 |
| 0.100 | 21.6 | 28.8 | 43.3 | 57.7 |
| 0.125 | 27.3 | 36.4 | 54.5 | 72.7 |
| 0.150 | 33.0 | 44.0 | 66.0 | 88.0 |

Hydraulic power at Δp = 95 psi is 0.055 hp per GPM (10 GPM is 0.55 hp before losses).

What the tables show:

- A 3.1 in rotor at 3600 RPM is a high-flow pump even at small eccentricity: about 14 GPM at e = 0.05 in, L = 1 in.
  The smallest corner of the table (e = 0.05 in, L = 0.75 in) still gives about 11 GPM theoretical.
- For the same total vane travel per revolution, the two layouts give nearly the same flow. In the balanced pump
  each vane travels half as far per stroke but strokes twice per revolution.

### Smallest practical pump

Flow is an output ([D10](decisions.md)): we shrink e and L as far as they can go and report the flow that results.
What stops further shrinking:

- **Volumetric efficiency.** Leakage through the side, tip and slot clearances depends on clearance size, Δp and
  viscosity, not on e. As displacement shrinks, leakage becomes a larger share of it. In a liquid this thin
  (0.114 cP at 150 °F), this is probably the binding limit. A leakage model is the next calculation.
- **Manufacturing tolerance on e.** At e = 0.05 in, a ±0.001 in error in ring or rotor position is ±2% of
  displacement.
- **Vane proportions.** The vane has to stay well supported in its slot while extended by 2e, and very short vanes
  (small L) tilt more under the pressure difference across them.
- **Shaft, bearing span and motor packaging** in the housing.

## Vane layout trade study

Decision [D7](decisions.md) is open.

| Factor | Single-lobe (eccentric round ring) | Balanced double-lobe (elliptical cam ring) |
|---|---|---|
| Radial bearing load | Net hydraulic load of roughly Δp × D_c × L: about 300 lbf per inch of rotor length at 95 psi. The bearings carry it in a thin fluid. | The two opposed pressure zones cancel, leaving almost no net radial load. |
| Bearing life vs. 50,000 h | Harder. A thin-fluid sleeve bearing carries a steady load. | Easier. Bearings carry only weight, imbalance and motor magnetic pull. |
| Ring manufacture | Round bore: turn or bore, then hone or grind. Cheap. | Non-circular profile: profile grinding, jig grinding, or wire EDM followed by finishing. Costs more. |
| Port plates | One inlet and one outlet port. | Two of each, cross-connected inside the housing. More complex passages. |
| Variable displacement | Possible by moving the ring. Probably not needed at fixed speed. | Not possible. Displacement is fixed by the cam. |
| Vane motion | Stroke 2e once per revolution. | Stroke s twice per revolution. Higher vane acceleration for the same flow, depending on the cam profile. |
| Pressure pulsation and noise | One pumping event per vane per revolution. | Two per vane per revolution, at a higher frequency. Both depend on z. |
| Fatigue ([below](#fatigue)) | The fixed-direction hydraulic load puts the rotating shaft in fully reversed bending every revolution, 1.08 × 10¹⁰ cycles. | Little shaft bending, but each vane sees 2.16 × 10¹⁰ load cycles, twice the single-lobe count. |
| Typical use | Low-pressure transfer pumps and variable pumps. | Industrial hydraulic vane pumps, chosen mainly for bearing life. |

To settle before deciding: bearing type and load capacity in liquid R-134a ([below](#bearing-trade-study)), and
the cost difference of the non-circular ring at 7,000/yr (see [manufacturing.md](manufacturing.md)).

## Bearing trade study

Decision [D16](decisions.md) is open. Liquid R-134a (0.11–0.29 cSt) gives almost no lubricating film, so the bearing
choice largely sets wear life.

| Factor | Product-lubricated sleeve (carbon-graphite or SiC) | Rolling-element (hybrid ceramic) |
|---|---|---|
| Lubrication in R-134a | Runs in boundary or mixed lubrication. Carbon-graphite is self-lubricating. SiC is very hard and wear-resistant but needs liquid present. | Rolling contacts need only a very thin film, and ceramic balls tolerate marginal lubrication better than steel. Still marginal at R-134a viscosity. |
| Load capacity | Limited by the PV (pressure × velocity) rating. Suits low radial loads, so it pairs with the balanced layout. | Higher. Copes better with the single-lobe side load. |
| How life is rated | PV limit and wear rate, giving a wear allowance over 50,000 h. No standard rating life. | ISO 281 L10h ≥ 50,000 h ([D12](decisions.md)). The standard's modified life uses a viscosity ratio κ that heavily penalizes thin lubricants, and R-134a falls far below its normal range (check). |
| Running dry or on vapor | Carbon-graphite tolerates brief dry running. | Tolerates brief poor lubrication. |
| Radial precision | The running clearance lets the shaft move, which eats into vane and side clearances. | Tighter radial location of the rotor. |
| Thermal expansion | Carbon-graphite (CTE about 2–3 × 10⁻⁶/°F) against a steel shaft (about 6.5) changes the running clearance over 170 °F. | Steel races match a steel shaft. |
| Size | Compact radially. | Larger outside diameter. |
| Cost | Low: pressed bushings. | Higher: hybrid ceramic bearings are premium parts. |
| Serviceability | Can be built into the replaceable cartridge, or pressed in and out. | Standard catalogue parts, easy to stock and swap. |

To research: refrigerant-lubricated bearings in oil-free refrigeration compressors, and carbon-graphite bushing PV
data from suppliers.

## Functional risks

| Risk | Why it matters here | Lever |
|---|---|---|
| **Fatigue** | Rotating parts see about 10¹⁰ load cycles, and fatigue causes most mechanical failures ([below](#fatigue)). | Infinite-life design: alternating stress below the corrected endurance limit, with stress concentrations kept low. |
| **Internal leakage** | Liquid R-134a is 0.11–0.39 cP. ISO VG 32 hydraulic oil is about 28 cP at 40 °C, so the refrigerant is roughly 100× thinner. Leakage through a gap scales as c³Δp/μ, so matching an oil pump's volumetric efficiency needs clearances about 100^(1/3) ≈ 4.6× tighter. The worst case is 150 °F (0.114 cP). | Side (axial) clearance, tip sealing, vane slot clearance, materials with matched expansion. |
| **Vane tip wear** | The tip slides at about 49 ft/s against the ring in a fluid with almost no film strength. Wear of vane tips is the likely life-limiting failure for 50,000 h. | Vane material pairing, contact force control (under-vane pressure balance), surface finish and hardness of the ring. |
| **Vane contact force** | Centrifugal force at 3600 RPM plus under-vane pressure. Too low and the vanes lift off and leak; too high and they wear. | Vane mass, under-vane porting, intra-vane or dual-vane designs. |
| **Bearings in a thin fluid** | Product-lubricated bearings get little hydrodynamic film from R-134a. | Balanced layout (to cut load), carbon-graphite or SiC sleeve bearings, or rolling bearings. |
| **Thermal expansion over 170 °F** | Dissimilar materials change clearances. For example, an aluminium ring against a steel rotor opens about 0.003 in over the range on a 3.1 in diameter ([materials.md](materials.md)). | Matched expansion coefficients, or clearances set at the critical temperature. |
| **Motor cooling** | The hermetic motor is cooled by the liquid it runs in. The hardest case is the winding temperature with 150 °F fluid. | A cooling flow path through the motor gap; winding insulation class. |

## Fatigue

Course guidance: 80% of mechanical failures are due to fatigue. At 3600 RPM for 50,000 h, from
[calcs/reliability.py](../calcs/reliability.py):

| Load | Cycles per rev | Cycles in 50,000 h at 3600 RPM |
|---|---|---|
| Shaft, rotating bending under a fixed-direction load | 1 | 1.08e+10 |
| Vane load and stroke, single-lobe | 1 | 1.08e+10 |
| Vane load and stroke, balanced double-lobe | 2 | 2.16e+10 |
| Pressure pulses on ring and housing (z = 8) | z | 8.64e+10 |

Every cyclically loaded part runs far past the 10⁶–10⁷ cycle knee of the S-N curve. Finite-life design doesn't
apply: each part must be designed for infinite life, with its alternating stress below an endurance limit corrected
for surface, size, reliability and temperature. Materials without a true endurance limit are a poor fit for these
parts ([materials.md](materials.md#fatigue)).

| Part | Cyclic load | Likely crack site |
|---|---|---|
| Shaft | Rotating bending from the hydraulic side load (single-lobe) and motor magnetic pull. Torque ripple at z per rev. | Shoulders, keyway, motor-rotor fit |
| Vanes | Bending from Δp across the vane as it crosses the sealing arcs, tip contact load, centrifugal load. 1 or 2 cycles per rev. | Where the vane leaves the slot |
| Rotor | Vanes load the slot walls each rev. | Slot root corners |
| Cam ring | Vane tips pass 8.6 × 10¹⁰ times: contact (surface) fatigue | Ring bore surface (pitting, spalling) |
| Rolling bearings (if used) | Rolling contact fatigue. L10 life is itself a fatigue rating. | Races |
| Housing and side plates | Pressure pulsation at z per rev | Port edges, bolt holes |
| Housing bolts and O-ring joints | Pressure cycles at each start and stop (few), pulsation, vibration | Bolt threads if preload is too low to keep the joint closed |
| Under-vane springs (if used) | One cycle per rev each | Better to avoid them, or design them for infinite life |

## Reliability

The 50,000 h MTBF is handled the way industry handles it for mechanical equipment ([D12](decisions.md)), in two
parts.

**1. Reliability prediction.** The unit fails if any part fails, so its failure rate is the sum of its parts':
MTBF = 1/Σλᵢ ≥ 50,000 h, i.e. Σλᵢ ≤ 2.0 × 10⁻⁵ per hour (0.175 per unit-year).

- The budget covers the pump mechanism only ([D17](decisions.md)): bearings, vanes, ring, rotor, side plates and
  shaft. The motor, terminal and isolation valves are judged separately against their suppliers' ratings.
- NSWC-11 (*Handbook of Reliability Prediction Procedures for Mechanical Equipment*) is the standard source for
  mechanical parts. It builds each failure rate from the design itself (loads, materials, lubricant viscosity,
  contamination) rather than from a fixed table value. Motor and terminal rates come from vendor data.
- The prediction assumes a constant failure rate during useful life. A population that just meets the MTBF looks
  like this, from [calcs/reliability.py](../calcs/reliability.py):

| Running time | Hours | Fraction of units surviving |
|---|---|---|
| 1 year | 8,760 | 83.9% |
| Median life (MTBF × ln 2) | 34,657 | 50.0% |
| MTBF | 50,000 | 36.8% |

**2. Keep wear-out beyond the life.** A constant failure rate only holds if nothing wears out inside the 50,000 h.
The usual way to ensure that:

| Part | Industry-standard check | Target |
|---|---|---|
| Rolling bearings (if used) | ISO 281 basic rating life L10h: the life 90% of bearings reach before fatigue | **L10h ≥ 50,000 h** at rated conditions. API 610 requires only 25,000 h for process pumps; guideline tables give 40,000–60,000 h for continuous-duty pumps. |
| Sleeve bearings (if used) | PV limit and wear rate of the bearing material | Wear allowance not used up in 50,000 h |
| Vanes and ring | Wear rate at the tip-to-ring contact | Wear allowance not used up in 50,000 h, without vane lift-off |
| Shaft, rotor, vanes, housing | Fatigue | Infinite life ([above](#fatigue)) |

L10 and MTBF measure different things: L10 is a 90%-survival life for one part, while MTBF is a mean for the whole
unit. Sizing bearings to L10h ≥ 50,000 h keeps their wear-out beyond the life. Their contribution to Σλᵢ during
useful life still comes from the prediction in part 1.

### What it means for maintenance

MTBF counts unscheduled failures; it says nothing about scheduled maintenance. This pump needs none: there's no
shaft seal, no oil to change and no bearings to regrease. The maintenance events are failures, each handled by field
repair or by swapping the unit and remanufacturing it at the factory ([serviceability.md](serviceability.md)).

At a 50,000 h MTBF (5.7 years of continuous running), with each failure repaired or swapped, from
[calcs/reliability.py](../calcs/reliability.py):

| Years installed | Original pumps failed | Expected failures per installed position |
|---|---|---|
| 1 | 16% | 0.18 |
| 2 | 30% | 0.35 |
| 3 | 41% | 0.53 |
| 5 | 58% | 0.88 |
| 10 | 83% | 1.75 |

For a fleet, every 1,000 pumps in service need about 175 repairs or swaps a year.
