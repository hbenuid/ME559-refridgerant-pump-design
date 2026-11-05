# Decision log

One entry per decision. Never delete an entry; if a decision is reversed, add a new entry that supersedes it.

| ID | Date | Decision | Status |
|---|---|---|---|
| D1 | 2026-10-22 | The pump moves liquid R-134a; it is not a compressor | Decided |
| D2 | 2026-10-22 | The −20 °F to 150 °F range is the refrigerant temperature | Superseded by D9 |
| D3 | 2026-10-22 | Flow rate is ours to choose | Decided; method in D10 |
| D4 | 2026-10-22 | Hermetic construction, motor inside the shell | Shell closure refined by D13; motor moved outside by D33 |
| D5 | 2026-10-22 | Rotor diameter fixed at 3.1 in | Constraint |
| D6 | 2026-10-22 | Tooling: Python + CoolProp for calcs, Onshape for CAD, Markdown in this repo for documentation | Decided |
| D7 | — | Vane layout: single-lobe eccentric vs. balanced double-lobe | **Open**: trade study in [functional-design.md](functional-design.md#vane-layout-trade-study) |
| D8 | — | Lubrication assumption: oil-free vs. oil present | **Open** ([Q3](open-questions.md)) |
| D9 | 2026-10-22 | The fluid is liquid at all times over −20 °F to 150 °F | Decided (course guidance) |
| D10 | 2026-10-22 | Size the smallest practical pump; flow follows from the geometry | Decided; values open ([Q2](open-questions.md)) |
| D11 | 2026-10-22 | MTBF is read literally, as a constant failure rate | Superseded by D12 |
| D12 | 2026-10-22 | MTBF is handled per industry practice: component failure-rate prediction, plus wear-out and fatigue parts sized to outlast 50,000 h | Decided |
| D13 | 2026-10-22 | Semi-hermetic: bolted housing with O-ring joints instead of a welded shell | Bolted housing decided; motor moved outside by D33 |
| D14 | 2026-10-22 | Field-maintainable where life-cycle cost justifies it, otherwise factory-refurbishable; recyclable at end of life. A refrigeration technician does field repair. | Decided; cost data open ([Q13](open-questions.md)) |
| D15 | 2026-10-22 | Inlet and outlet isolation valves built into the pump | Decided |
| D16 | — | Bearing type: product-lubricated sleeve vs. rolling-element | **Open**: trade study in [functional-design.md](functional-design.md#bearing-trade-study) |
| D17 | 2026-10-22 | The 50,000 h MTBF applies to the pump mechanism only | Decided |
| D18 | 2026-10-22 | Tooling is amortized over 5 years of production (35,000 units) | Decided |
| D19 | 2026-10-29 | Part numbers are assembly-coded | Decided; ranges to finalize with the part list |
| D20 | 2026-10-29 | Fasteners appear in the BOM with torque specs, but get no drawing | Decided |
| D21 | 2026-10-29 | Materials are chosen with Ashby's method in Granta EduPack 2026 R1, Level 3 database | Decided |
| D22 | 2026-11-03 | Granta screens use only numeric requirements as Limit stages, passing on the whole record; no hand-picked families | Decided |
| D23 | 2026-11-03 | The metal stack is screened with a fracture toughness minimum of 10 ksi·in^0.5; the all-carbon stack is judged from supplier data | Decided |
| D24 | 2026-11-05 | The vane screen has no toughness or expansion limit and a price cap of 10,000 USD/ft³ | Decided |
| D25 | 2026-11-05 | Low-temperature ductile iron (EN GJS 350-22-LT) is re-admitted to the housing screen as a documented exception | Decided |
| D26 | 2026-11-05 | PEEK wear grades are re-admitted to the vane screen by hand | Decided |
| D27 | 2026-11-05 | The housing screen keeps the stack's temperature, price and toughness limits, adds a casting limit, and has no expansion limit | Decided |
| D28 | 2026-11-05 | The shaft gets a light Granta screen with the stack's limits and a fatigue strength vs. price chart | Decided |
| D29 | 2026-11-05 | The stack and shaft expansion cap is 7.6 µstrain/°F, not 7.5 | Decided |
| D30 | 2026-11-05 | The shaft's price cap is 2,000 USD/ft³ | Decided |
| D31 | 2026-11-05 | Cast lead and magnesium alloys are removed from the housing shortlist by hand | Decided |
| D32 | 2026-11-05 | The design pressure is 300 psig, set by a pump standing idle at 150 °F | Decided |
| D33 | 2026-11-05 | Magnetic drive: a standard motor outside the housing drives the pump through a magnetic coupling | Decided; containment can open ([Q28](open-questions.md)) |

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

Update (2026-11-05): D33 moves the motor out of the refrigerant. It drives the pump through a magnetic coupling, so
the pump stays sealless.

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

Update (2026-11-05): D9 still sets the performance cases. A pump standing idle at 150 °F sets the design pressure
instead ([D32](#d32-design-pressure-300-psig-from-the-idle-case)), and real-fluid cavitation and vapor lock are
logged as risks outside the course basis ([requirements.md](requirements.md#real-fluid-check)).

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

Update (2026-11-05): with the magnetic drive ([D33](#d33-magnetic-drive)) the bolted housing and O-ring joints stay,
but the motor is no longer inside the housing.

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

Update (2026-11-05): with the magnetic drive ([D33](#d33-magnetic-drive)) there is no terminal, and the magnetic
coupling joins the purchased parts judged on their suppliers' ratings. The containment can is a pressure part, outside
the budget like the O-ring joints.

## D18: 5-year production horizon

Tooling is amortized over 5 years × 7,000 units/yr = 35,000 units. This is conservative: it favours processes with
low tooling cost, so any tooling-heavy process (powder metal, dies) has to justify itself over 35,000 units.

## D19: Assembly-coded part numbers

The [final deliverables](requirements.md#final-deliverables) need a unique part number of ours on every part,
off-the-shelf parts included. Each number shows which assembly group the part belongs to, which matches the split
between the housing and the pumping cartridge sold as the field repair kit ([serviceability.md](serviceability.md)).
Starting layout, to finalize once the part list exists:

| Range | Group |
|---|---|
| R3-100 | Housing |
| R3-200 | Pumping cartridge |
| R3-300 | Motor |
| R3-900 | Off-the-shelf parts |

## D20: Fasteners in the BOM

The handout exempts fasteners from drawings but says the BOM lists each part and asks for fastener torque specs. Each
fastener is listed in the BOM by its standard designation (size, length, type, grade), with quantity and torque. It
gets no drawing.

## D21: Materials selection method

Granta EduPack is available through the university, and its Limit, Tree and Chart stages carry out Ashby's
screen-and-rank method directly. The Level 3 database is used because telling grades apart needs grade-level data
such as fatigue strength, fracture toughness and expansion. Granta doesn't cover compatibility with R-134a and POE, or
wear in a fluid this thin; those come from literature and supplier data. The method, the part groups and the running
record of the screen are in [materials.md](materials.md#selection-method).

## D22: Requirement-only screen, whole record

Each requirement that can be written as a number is a Limit stage, and every stage passes a material only if its whole
range meets the limit. This replaces the first screen (2026-10-29), which used Granta's default "any part of record"
rule and a Tree stage of hand-picked families.

- **Whole record**: Granta stores properties as ranges. The default passes a material that only might meet a limit;
  for example, ductile iron GJS 400-18-LT passed −20 °F although its rating runs up to 14 °F.
- **No hand-picked families**: a Tree stage is a judgment, not a requirement, so it's harder to defend. With numbers
  only, an unsuitable survivor shows a missing requirement, which is then added as a stage.

See [materials.md](materials.md#selection-in-granta).

## D23: Toughness minimum, carbon judged separately

On the fracture toughness vs. price chart, metals sit above about 10 ksi·in^0.5 and glasses, ceramics, concrete, foams
and carbon below about 5, with almost nothing between. A minimum of 10 ksi·in^0.5 (whole record) removes every
brittle material and keeps gray iron (14.6–18.2) and the steels.

The same minimum removes carbon-graphite, which real vane pumps use at low loads. Level 3 holds only generic carbon
records ("Resin impregnated carbon", "Carbon/resin", bulk graphites), so the all-carbon stack is judged from supplier
data on specific grades rather than in this screen. See [materials.md](materials.md#what-survives-stage-4).

## D24: Vane screen thresholds

The stack's limits would remove two of the three vane candidates, so the vane screen sets its own:

- **No toughness limit.** The stack's 10 ksi·in^0.5 removes carbon-graphite and filled PEEK. Vanes are ranked
  instead, and brittleness is judged by hand: short vane extension keeps bending low. Carbon is still judged from
  supplier data ([D23](#d23-toughness-minimum-carbon-judged-separately)).
- **No expansion limit.** Each 1 µstrain/°F of mismatch with the stack changes a 1 in vane by about 0.0002 in over
  170 °F. Carbon (about 2–3), steel (about 6.5) and filled PEEK (above 10) all stay in, and each one's axial
  clearance is sized by hand once the leakage model sets the budget ([Q2](open-questions.md)).
- **Price at most 10,000 USD/ft³.** Eight vanes 0.10 in thick come to under 1 in³ even at 1 × 1 in each, so
  material costs under about $5 per pump at this cap. The stack's 1,500 would likely remove filled PEEK.

Temperature stays at −20 °F to 150 °F on the whole record ([D22](#d22-requirement-only-screen-whole-record)), and the
ranking is fatigue strength against density ([materials.md](materials.md#spec-for-each-group)).

## D25: Low-temperature ductile iron in the housing

Every ordinary ductile iron fails Granta's −20 °F rating on the whole-record rule, yet low-temperature ductile iron is
the usual casing material in refrigerant pumps ([materials.md](materials.md#check-against-refrigerant-pumps)).
EN 1563 impact-tests GJS 350-22-LT at −40 °C (−40 °F), below our −20 °F. The housing screen runs whole-record as
before, and GJS 350-22-LT is then added by hand on its ranking chart, citing EN 1563. The rating is to be confirmed
against the standard. This answers [Q23](open-questions.md#answered).

## D26: PEEK wear grades in the vane screen

Granta has no service-temperature data for the PEEK wear grades, so the whole-record temperature stage removes them
([materials.md](materials.md#vane-screen-in-granta)). They are the filled PEEK grades made for sliding wear, and the
25–35% carbon grade expands like the stack (5.5 µstrain/°F). As with ductile iron in the housing
([D25](#d25-low-temperature-ductile-iron-in-the-housing)), the screen stays whole-record and the wear grades are added
by hand on the vane chart, with the temperature rating taken from the supplier datasheet. This answers
[Q24](open-questions.md#answered).

## D27: Housing screen thresholds

- **Kept from the stack**: −20 °F to 150 °F, price at most 1,500 USD/ft³, fracture toughness at least 10 ksi·in^0.5,
  all on the whole record.
- **No expansion limit.** Cast aluminium (about 12 µstrain/°F) stays in the ranking. Around an iron cartridge it would
  loosen a 3.1 in bore fit by about 0.003 in over 170 °F, so if aluminium wins on cost the fit is designed for that
  by hand.
- **Castable**: a Limit on Granta's casting rating, so the requirement is a stage and not a hand pick.

Ranking follows the spec ([materials.md](materials.md#spec-for-each-group)): yield strength against price per unit
volume for wall cost, and fracture toughness against yield strength for leak-before-break.

## D28: Shaft screen

The shaft is a standard steel plus a fatigue check, so it gets a light screen: the stack's Stages 1, 2 and 4
(temperature, price with the expansion cap, toughness) and a fatigue strength vs. price chart. No new thresholds.

## D29: Expansion cap 7.6 µstrain/°F

The 7.5 cap was set from steel's typical 6.5 µstrain/°F, but AISI 4140, the usual shaft steel, is listed at
6.39–7.5. Its top value landed on the cap, so the whole-record rule removed it from both the stack and the shaft.
At 7.6 it passes. The stack gains 23 records (2,866 → 458 → 316 → 305), all steels, and loses none
([materials.md](materials.md#stages)). The vane and housing screens have no expansion cap, so they don't change.
This answers [Q25](open-questions.md#answered).

## D30: Shaft price cap 2,000 USD/ft³

17-4PH (1,460–1,660 USD/ft³) and 15-5PH ran just over the stack's 1,500. A shaft is a small volume, so a higher
price per volume adds only a few dollars per pump. At 2,000 both pass. The stack keeps 1,500. The shaft screen now
passes 370 ([materials.md](materials.md#shaft-screen-in-granta)). This answers [Q26](open-questions.md#answered).

## D31: Lead and magnesium out of the housing by hand

The housing screen passes 6 cast lead and 27 cast magnesium alloys. Neither belongs in a refrigerant pressure
housing, but what rules them out isn't held in Granta: lead is weak (about 5 ksi yield) and toxic, and magnesium
corrodes and is generally kept out of contact with halogenated refrigerants (to confirm against the code once
[Q7](open-questions.md) is settled). They are struck from the shortlist by hand, leaving 96. This is an exception to
[D22](#d22-requirement-only-screen-whole-record): the requirement that removes them is compatibility, which Granta
can't filter. See [materials.md](materials.md#housing-screen-in-granta).

## D32: Design pressure 300 psig, from the idle case

The teammates' temperature analysis ([references.md](references.md#team-notes)) points out that the housing sees its
highest pressure when the pump is idle, not while it runs. While it runs, the liquid is cold and the highest pressure
is the 150 psig outlet. A pump standing full of R-134a in a 150 °F space warms with it: some liquid boils, and the
pressure rises to the saturation pressure at 150 °F, 263 psig ([calcs/pressure_cases.py](../calcs/pressure_cases.py)).
Rounded up to 300 psig for hot spots, pressure spikes and the relief setting, this is the design pressure for the
housing, the containment can, the bolts and the O-ring joints.

D9 still sets the performance cases: 150 °F liquid properties for leakage and −20 °F for drag. The design takes the
worst case of each. Proof and burst test factors still depend on the codes ([Q7](open-questions.md)). This answers
[Q9](open-questions.md#answered).

The 263 psig assumes some vapor space in the pump or the connected piping. A pump that is completely full of liquid,
with both isolation valves closed, goes far higher as it warms; that case belongs to the relief question
([Q27](open-questions.md)).

## D33: Magnetic drive

The motor moves outside the housing. An outer magnet rotor on the motor shaft turns an inner magnet rotor on the pump
shaft, across a containment can that closes the pressure boundary. The team notes propose it as suitable for
low-viscosity liquids ([references.md](references.md#team-notes)). The pump stays sealless, as in
[D4](#d4-hermetic): no shaft seal and no dynamic leak path.

What changes:

- **Motor**: a standard catalog motor running in air. It no longer needs refrigerant-rated insulation, and no
  electrical terminal passes through the pressure boundary.
- **Service**: a technician can change the motor without opening the refrigerant circuit
  ([D14](#d14-serviceability-goal)).
- **New parts**: the coupling's two magnet rotors and the containment can. The can holds the 300 psig design pressure
  ([D32](#d32-design-pressure-300-psig-from-the-idle-case)); its material is [Q28](open-questions.md).
- **Overload**: the coupling slips if the torque passes its rating, for example against a blocked outlet. It doesn't
  re-engage until the motor stops, and slipping heats the magnets. It limits torque but doesn't relieve pressure
  ([Q27](open-questions.md)).
- **Heat**: a metal can turns part of the shaft power into eddy-current heat in the liquid
  ([Q22](open-questions.md)).

This supersedes the motor location in D4 and D13. The bolted housing with O-ring joints (D13), the isolation valves
([D15](#d15-integral-isolation-valves)) and the replaceable cartridge stay. See
[functional-design.md](functional-design.md#magnetic-drive).
