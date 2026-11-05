# Materials

Rubric: *ability to choose appropriate materials* (17.5%).

Nothing is final yet. The Granta screens ([below](#selection-in-granta)) point to a leading choice for most parts,
summarized under [Current choices](#current-choices). Candidates further down are starting points to research;
material properties are typical values to confirm against a specific grade's data sheet.

A material comparison document (PDF) is one of the [final deliverables](requirements.md#final-deliverables). The
candidate tables here are its starting point.

## Current choices

As of 2026-11-05. Each part follows the same method: requirements become numeric limits in Granta, only materials sure
to pass are kept (whole-record rule, [D22](decisions.md)), the survivors are ranked on cost charts, and the result is
checked against what real refrigerant pumps and compressors use.

| Part | Leading choice | Why | Still open |
|---|---|---|---|
| Cam ring | Gray cast iron | Cheapest material passing every stack requirement, by 2–4× ([Stage 6](#ranking-fatigue-strength-vs-price-stage-6)). Graphite helps under boundary lubrication. Expands like the steel shaft (about 6–7 µstrain/°F), so clearances hold over −20 °F to 150 °F. Rotary refrigerant compressors use cast iron cylinders ([check](#check-against-refrigerant-pumps)). | Grade. If the vanes are steel, the ring track has to be much harder. |
| Side plates | Gray cast iron | Same reasons as the ring. Loads are mostly compressive with low alternating stress, so cost and wear decide. | Grade. |
| Rotor | Gray iron or steel (e.g. AISI 4140) | Both pass the stack screen and match its expansion. Gray iron is cheaper; steel has far more fatigue strength for about 10¹⁰ cycles. | The rotor stress estimate sets a fatigue line on the Stage 6 chart. |
| Vanes | Not chosen: carbon-graphite, filled polymers (PEEK, PAI, PPS) or tool steel | All three are used in real vane pumps, and all pass the [vane screen](#vane-screen-in-granta). Running oil-free favours carbon or filled polymer over steel. PEEK wear grades come back by hand ([D26](decisions.md)). The team's wear estimate argues for nitrided or PVD-coated steel on a hardened ring ([vane tip wear](functional-design.md#vane-tip-wear)), and the team expects to add a lubricant ([Q3](open-questions.md)). | Read the fatigue vs. density ranking; settle oil ([Q3](open-questions.md)); supplier data for carbon grades ([D23](decisions.md)). |
| Housing | Low-temperature ductile iron EN GJS 350-22-LT | Same price as gray iron (about 74–86 USD/ft³) with about 1.7× the yield strength and twice the toughness. Impact-tested at −40 °C under EN 1563, and the usual refrigerant pump casing material. Granta fails it only on its temperature data, so it is added back by hand ([D25](decisions.md)). | Draw the wall-cost and leak-before-break rankings against gray iron, cast aluminium and cast steel ([housing screen](#housing-screen-in-granta)). |
| Shaft | A standard steel: AISI 4140, 4340, 416 or 420 stainless, or 17-4PH | All pass the [shaft screen](#shaft-screen-in-granta) after [D29](decisions.md) and [D30](decisions.md). Steels have a true endurance limit, which a part loaded about 10¹⁰ times needs. | Fatigue check, then pick one. |
| Containment can | Not chosen: 316 stainless or Hastelloy; carbon-fibre PEEK or ceramic | Holds the 300 psig design pressure ([D32](decisions.md)) inside the coupling's magnetic gap ([D33](decisions.md)). Metal is strong and simple but heats the liquid with eddy currents. Austenitic stainless is ruled out only in the stack. | [Q28](open-questions.md). |
| O-rings, bearings, motor, magnetic coupling | Set by the supplier | Purchased parts; compatibility with R-134a (and POE) is checked for the parts in the liquid. The motor runs in air ([D33](decisions.md)). O-rings in HNBR or neoprene, not FKM ([candidates](#candidates-by-component)). | Confirm against compatibility charts. |

**Ruled out:**

| Material | Where | Why |
|---|---|---|
| Aluminium | Ring, rotor, side plates | Expands about twice as much as the steel shaft (about 12 against 6.5 µstrain/°F), opening clearances by about 0.003 in over the range ([thermal expansion](#thermal-expansion)). No true endurance limit. |
| Austenitic stainless | Ring, rotor, side plates | Expands about 9–10 µstrain/°F, also too far from the steel shaft. |
| Ceramics and glasses | All structural parts | Too brittle: fracture toughness below about 5 ksi·in^0.5 ([D23](decisions.md)). |
| Ni-Resist | Stack | Costs more than most steels and has less fatigue strength ([Stage 6](#ranking-fatigue-strength-vs-price-stage-6)). |
| Cast lead and magnesium | Housing | Lead is weak and toxic; magnesium corrodes and is kept away from halogenated refrigerants ([D31](decisions.md)). |

## What every material must satisfy

- **Compatibility with R-134a**, and with POE oil if oil is present ([Q3](open-questions.md)). This covers swelling,
  extraction and chemical attack. The motor is outside ([D33](decisions.md)), so this applies to the coupling's
  encapsulated inner rotor and the containment can rather than to motor insulation.
- **The −20 °F to 150 °F range**, including toughness at −20 °F and expansion over 170 °F.
- **Wear in a fluid thinner than water**, under boundary lubrication. This affects vanes, ring, side plates and
  bearings most.
- **Matched expansion** between the rotor, ring and side plates, so clearances hold across the range.
- **Cleanliness and dryness**: no porous materials that hold moisture or contaminants unless they are sealed.
  Moisture plus POE oil makes acid in refrigerant systems.
- **Fatigue**: rotating parts see about 10¹⁰ load cycles ([functional-design.md](functional-design.md#fatigue)), so
  cyclically loaded parts need materials designed for infinite life (see [below](#fatigue)).
- **Volume and cost**: 7,000 units/yr (see [economics.md](economics.md)).
- **Separable for recycling**: avoid bonding or potting dissimilar materials, and mark major parts by material
  ([serviceability.md](serviceability.md)).

What helps: dry R-134a is clean, not corrosive to common metals, and not an electrolyte
([requirements.md](requirements.md#r-134a-as-a-pumped-liquid)). Corrosion resistance doesn't force stainless steel,
and dissimilar metals can be paired without galvanic corrosion. Cost and fatigue can drive the choice instead.

## Selection method

Ashby's method, which Granta EduPack is built around ([D21](decisions.md)). For each group of parts:

1. **Translate** the requirements into a function, constraints (pass/fail), an objective (what to minimize or
   maximize) and free variables.
2. **Screen**: remove every material that fails a constraint (Granta's Limit and Tree stages).
3. **Rank** the survivors on property charts or a performance index (Chart/Index stage). Keep the top 3–5.
4. **Gather what Granta doesn't hold**: compatibility with R-134a and POE, wear under boundary lubrication in a fluid
   thinner than water, what comparable products use, and supplier availability.
5. **Check in the models** ([functional-design.md](functional-design.md#modeling-plan)): expansion → clearance change
   → leakage; density → vane tip force → wear; fatigue strength → corrected endurance limit → safety factor. If a
   check fails, tighten that constraint and screen again.
6. **Pair with a process and cost it.** Material and process go together (PM steel with powder metallurgy, gray iron
   with sand casting). Granta's Part Cost Estimator at 7,000/yr over 35,000 units ([D18](decisions.md)) feeds
   [economics.md](economics.md).
7. **Record** each group's choice in [decisions.md](decisions.md): constraints, chart, finalists, choice and reason.

### Part groups

Parts that constrain each other are chosen together, and effort scales with how much the part matters.

| Group | Parts | Why together | Treatment |
|---|---|---|---|
| A. Pumping stack | Ring, rotor, side plates | Matched expansion holds the running clearances, which set leakage | Full method, done first |
| B. Vanes | Vanes | Wear pair with the ring | Full method |
| C. Housing | Bolted housing sections | Pressure boundary and the largest casting | Full method |
| D. Shaft | Shaft, journals | Rotating fatigue | A standard steel plus a fatigue check |
| E. Standard parts | Bolts, dowels, keys | Standard answers | One line each |
| F. Purchased parts | O-rings, bearings, motor, magnetic coupling, valves | The supplier sets the material | Cite the source and check R-134a/POE compatibility |

### Spec for each group

| Group | Function | Constraints | Objective | Ranking |
|---|---|---|---|---|
| A. Stack | Hold the running clearances; carry vane contact on the ring | −20 °F to 150 °F; expansion matched across the stack; grindable to a fine finish; dimensionally stable; endurance limit (rotor); hard ring track; R-134a/POE compatible | Minimum cost | Expansion vs. price per unit volume; hardness vs. price |
| B. Vanes | Slide in the slot and seal at the tip | Wear in a thin fluid; fatigue at about 10¹⁰ cycles; stable at 150 °F | Low density: centrifugal tip force scales with it, and tip force drives wear | Fatigue strength vs. density |
| C. Housing | Contain the 300 psig design pressure ([D32](decisions.md)), plus any code factor ([Q7](open-questions.md)) | Toughness at −20 °F; castable; machinable | Minimum cost (mass doesn't matter in a basement) | Minimize C_m·ρ/σ_y (wall t = pR/σ); leak-before-break K_IC²/σ_y |
| D. Shaft | Carry torque and bending | Endurance limit; hardenable journals | Minimum cost | Screen only |

A sand-cast housing wall is often set by the minimum castable thickness rather than by pressure. In that case price
per unit volume matters more than the index.

**How closely the stack has to match.** Axial clearance is the ring width minus the rotor length, and the rotor runs
inside the ring, so the ring and rotor matter most. The side plates matter at their clamped faces and bores. Each
1 µstrain/°F of mismatch shifts the 3.1 in diameter by 1 × 10⁻⁶ × 3.1 × 170 ≈ 0.0005 in over the range, and a 1 in
rotor length by about 0.0002 in. The allowed mismatch comes from the clearance budget, which the leakage model will
set ([Q2](open-questions.md)). Until then, the placeholder is within about 1 µstrain/°F of each other. That leaves two
consistent families: ferrous (irons and steels, about 6–7 µstrain/°F) or all carbon-graphite (about 2–3). Bronze side
plates (about 10) sit outside the ferrous band; check what that does at the clamped faces before ruling bronze out.

## Candidates by component

| Component | Candidates | Notes |
|---|---|---|
| Cam ring | Gray cast iron; hardened alloy steel; powder-metal (PM) steel; carbon-graphite insert | Gray iron's graphite helps under boundary lubrication and it damps vibration. Hardness and finish matter more than bulk strength. |
| Rotor | PM steel; gray cast iron; carbon-graphite | Expansion should match the ring and side plates. PM can form the slots near net shape. |
| Vanes | Carbon-graphite; filled PEEK (carbon/PTFE/graphite); tool steel | Rotary vane pumps for water and other thin fluids commonly pair carbon-graphite vanes and rotors with brass or stainless housings, which makes them a useful analog to research. Steel vanes are the norm in oil hydraulics but rely on an oil film. |
| Side / port plates | Gray cast iron; bronze; carbon-graphite faced | These form the axial clearance, the largest leak path. |
| Bearings | Carbon-graphite sleeve; silicon carbide sleeve; rolling-element (steel or hybrid ceramic) | Product-lubricated in liquid R-134a. Load depends on the vane layout trade ([functional-design.md](functional-design.md#vane-layout-trade-study)). |
| Shaft | Alloy steel (e.g. 4140); martensitic or precipitation-hardening stainless | Carries the coupling's inner magnet rotor; bearing journals may need hardening or a sleeve. |
| Housing (pump body) | Gray cast iron; cast aluminium | Aluminium is lighter but expands about twice as much as iron or steel (see below). |
| Housing sections | Gray cast iron; ductile iron; cast aluminium | Bolted sections with O-ring joints ([D13](decisions.md)). It is a pressure boundary, designed for 300 psig ([D32](decisions.md)). Ductile iron gives more toughness at −20 °F. |
| Isolation valves | Purchased refrigeration service valves (brass or steel bodies) | Must be compatible with R-134a and rated for the design pressure. |
| Containment can | 316 stainless; Hastelloy C; carbon-fibre PEEK; ceramic (zirconia) | Holds 300 psig in the magnetic gap. Metal cans heat the liquid with eddy currents; non-metallic cans don't ([Q28](open-questions.md)). |
| Magnetic coupling | Purchased: neodymium or samarium-cobalt magnets, the inner rotor encapsulated (stainless sleeve or polymer) | Only the encapsulated inner rotor sits in R-134a ([D33](decisions.md)). The motor runs in air, so no hermetic terminal or refrigerant-rated insulation is needed. |
| O-rings / static seals | HNBR, neoprene (CR) | Housing joints and cartridge seals; replaced at every service. FKM (Viton) is commonly listed as not recommended for R-134a. Check the compatibility chart for both R-134a and the oil. |

## Viable material families

| Family | Viable? | Where | Comparable pumps |
|---|---|---|---|
| Cast irons (gray, ductile) | Yes | Ring, rotor, side plates, housing | LPG sliding-vane pumps: gray iron liner and side discs, ductile iron rotor and casing. Rotary refrigerant compressors: gray iron cylinder. |
| Steels (carbon, alloy, tool, martensitic stainless) | Yes | Rotor, shaft, steel vanes | Rotary refrigerant compressors: high-speed tool steel vanes, often nitrided or coated, running on cast iron |
| Carbon-graphite | Yes | Vanes, bearings, or an all-carbon stack | Water vane pumps (e.g. Procon): carbon-graphite vanes, liner and bearings |
| Engineering polymers (filled PEEK and similar) | Vanes only | Vanes | LPG sliding-vane pumps use proprietary non-metallic vanes |
| Aluminium, bronze | Not in the stack: they don't match a ferrous stack, shaft or steel vanes, and an all-aluminium stack fails on fatigue (no endurance limit at 10¹⁰ cycles) and on wear (soft ring track) unless coated | Housing (aluminium); bushings or side-plate faces (bronze) | Water vane pumps: brass housings |
| Elastomers | Seals only | O-rings (purchased) | — |
| Technical ceramics (SiC) | Bearings only | Sleeve bearings (purchased) | — |
| Foams, natural materials, glasses, fibre composites | No | — | — |

For the pumping stack this leaves cast irons, steels and carbon-graphite, which matches the two expansion families
([above](#spec-for-each-group)). The closest analog, the LPG sliding-vane pump, moves a thin volatile liquid like ours
with an all-iron stack and non-metallic vanes. Sources are in [references.md](references.md).

## Selection in Granta

Granta EduPack 2026 R1, run through the university's Citrix virtual apps. The settings below are enough to repeat the
screen.

| Setting | Value |
|---|---|
| Database | Level 3, for grade-level data (fatigue strength, fracture toughness, expansion) |
| Select from | MaterialUniverse: All materials (4,392 records) |
| Units | US: °F, µstrain/°F, USD/ft³ |
| Project files | `pump-stack.ces`, `pump-vanes.ces`, `pump-housing.ces` and `pump-shaft.ces` in `X:\ME559`, on the personal X: network drive (not in this repo). The Citrix desktop doesn't keep Documents between sessions: the first save there was gone on 2026-11-05. |
| Exported results | [data/granta/](../data/granta/), one tab-separated file per project, copied from Granta's Pass/Fail table on 2026-11-05 with the current settings. Each row is one of the 4,392 records: its name, how many stages it passed, and Pass or Fail for each stage. A chart stage fails a record only when it lacks data for an axis. |

### Approach

Every requirement that can be written as a number goes in as a Limit stage, set to pass only on the **whole record**
([D22](decisions.md)). No material families are picked by hand. Whatever unsuitable material still passes points to a
requirement that hasn't been entered yet, which then becomes the next stage. Requirements Granta can't filter
(compatibility with R-134a and POE, wear in a thin fluid) are judged by hand on the shortlist.

**How Granta treats ranges.** Granta stores most properties as a range, and each stage has a "Pass when" setting
(stage Settings → Pass when) with two options ([Ansys help](references.md)):

- **Any part of record within selection** (Granta's default): a record passes if any part of its range is inside the
  limit.
- **Whole record within selection** (used here): the whole range must be inside the limit, so a material passes only
  if it is sure to meet the requirement.

### Stages

Project `pump-stack`, built 2026-11-03 and rebuilt on 2026-11-05 with the same pass counts. Later on 2026-11-05 the
expansion cap went from 7.5 to 7.6 µstrain/°F ([D29](decisions.md)); the table shows the current settings.

| Stage | Type | Settings | Pass when | Pass |
|---|---|---|---|---|
| 1 | Limit | Thermal properties. Maximum service temperature: minimum 150 °F. Minimum service temperature: maximum −20 °F. Logic AND. | Whole record | 2,866 of 4,392 |
| 2 | Limit | Price per unit volume: maximum 1,500 USD/ft³. Thermal expansion coefficient: maximum 7.6 µstrain/°F. Logic AND. | Whole record | 458 of 4,392 (434 at 7.5) |
| 3 | Chart | Y: Fracture toughness (ksi·in^0.5), logarithmic, autoscale. X: Price per unit volume (USD/ft³), logarithmic, autoscale. No selection box. | — | 458 of 4,392 |
| 4 | Limit | Impact & fracture properties. Fracture toughness: minimum 10 ksi·in^0.5. | Whole record | 316 of 4,392 (293 at 7.5) |
| 5 | Limit | Mechanical properties. Hardness - Vickers: minimum 100 HV. | Whole record | 305 of 4,392 (282 at 7.5) |
| 6 | Chart | Y: Fatigue strength at 10⁷ cycles (ksi), logarithmic, autoscale. X: Price per unit volume (USD/ft³), logarithmic, autoscale. No selection line yet. | — | 305 of 4,392 |

Notes:

- **Stage 1** uses the brief's range with no margin for heat inside the housing ([Q22](open-questions.md)). With "whole record" it
  passes 2,866 materials; Granta's default would pass 3,757. Ductile iron EN GJS 400-18-LT drops out here: its minimum
  service temperature is −193 to 14 °F, so it isn't sure to work at −20 °F.
- **Price is per unit volume**, not per pound. The 3.1 in rotor fixes the stack's size, so material cost is volume ×
  price per volume.
- **The expansion cap** is set by the steel shaft, about 6.5 µstrain/°F, running through the rotor
  ([thresholds](#stack-thresholds)). At 7.5 it removed AISI 4140, whose listed range is 6.39–7.5, so it was raised to
  7.6 ([D29](decisions.md)).
- **What 7.6 adds**: 23 records pass all stages that failed at 7.5, all steels. AISI 4140 (annealed, normalized,
  tempered at 425, 540 and 650 °C), 41L40, 5140, 5150, 81B45, the free-machining carbon steels 1137 and 1141, and the
  duplex stainless LDX2101. Nothing that passed at 7.5 drops out. The family breakdowns below were taken at 7.5; the
  23 steels are the only difference.

### What survives Stages 1 and 2

The 434 records, copied out of Granta's results list and sorted by family:

| Family | Records | Notes |
|---|---|---|
| Low-alloy and alloy steels | 104 | AISI 41xx, 43xx, 86xx and similar, in several heat treatments |
| Tool steels | 49 | |
| Martensitic stainless | 35 | Includes AISI 410, 416, 420, 440C and cast CA-15, CA-40, CA-6NM |
| Carbon steels | 34 | AISI 10xx and 11xx, and cast SA216 WCC |
| Sheet and wire steels | 26 | HSLA, dual phase, TRIP and similar; sheet forms, not stock for a rotor |
| Ferritic stainless | 17 | |
| Structural steels | 8 | |
| Gray cast iron | 6 | EN GJL 100 to 350 |
| Austenitic ductile iron (Ni-Resist) | 4 | EN GJSA XNi35 and similar |
| Pure and wrought iron | 3 | |
| Superferritic stainless (listed as duplex) | 3 | |
| Lanthanum | 1 | A reactive rare-earth metal |
| Carbon and graphite | 28 | Includes "Resin impregnated carbon" and "Carbon/resin", the type used for pump vanes and liners |
| Glasses | 45 | |
| Concrete, brick and stone | 20 | |
| Foams | 14 | |
| Technical ceramics | 13 | Alumina 85–90%, mullite, steatite, cordierite, porcelain |
| Glass ceramics | 9 | |
| Polymer composites | 9 | Carbon- or glass-fibre filled; low expansion along the fibres |
| Fibres | 6 | Asbestos, E-glass, silica |

Notes:

- **What "whole record" removed** compared with the first pass: every ordinary ductile iron (EN GJS) grade
  (GJS 400-18-LT on temperature; the others not checked, but most likely the same); the cast austenitic stainless records; and dense silicon
  carbide.
- **Unsuitable materials still pass**: about 100 records of glass, concrete, stone, foam, fibre and brittle ceramic.
  They are cheap, expand little and survive the temperature range, but they crack or crumble. Nothing entered so far
  says the part must not crack.

The Stage 3 chart shows the missing requirement. Colours are material families, matching the icons in the results
list; grey has been filtered out:

| Family (colour) | Fracture toughness (ksi·in^0.5, read from chart) |
|---|---|
| Irons and steels (teal) | About 10 to 150 |
| Ceramics, including carbon and graphite (yellow); glasses (magenta); concrete and stone (olive); fibres such as asbestos (black) | About 0.3 to 5 |
| Foams (green) | About 0.01 to 0.1 |
| A few polymers (blue) and non-ferrous metals (red) | Scattered, about 3 to 30 |

Between about 5 and 10 ksi·in^0.5 there is almost nothing. A minimum fracture toughness in that gap separates the
metals from the brittle materials. It would also remove carbon-graphite, which runs in real vane pumps at low loads, so
carbon needs its own route rather than being lost to a filter meant for metals.

### What survives Stage 4

Stage 4 sets the minimum at 10 ksi·in^0.5, in the gap. Before and after, from the copied results lists:

| Family | After Stage 2 | After Stage 4 |
|---|---|---|
| Low-alloy and alloy steels | 104 | 103 |
| Tool steels | 49 | 49 |
| Martensitic stainless | 35 | 35 |
| Carbon steels | 34 | 34 |
| Sheet and wire steels | 26 | 26 |
| Ferritic and superferritic stainless | 20 | 20 |
| Structural steels | 8 | 8 |
| Gray cast iron | 6 | 6 |
| Austenitic ductile iron (Ni-Resist) | 4 | 4 |
| Pure and wrought iron | 3 | 3 |
| Lanthanum | 1 | 1 |
| Polymer composites | 9 | 4 |
| Carbon and graphite | 28 | 0 |
| Glasses, glass ceramics, technical ceramics | 67 | 0 |
| Concrete, brick, stone, foams, fibres | 40 | 0 |
| **Total** | **434** | **293** |

- **Every brittle material is gone**, and so is carbon-graphite, as expected. The all-carbon stack is judged from
  supplier data instead ([D23](decisions.md)).
- **The only metal removed** is AISI 52100 in the annealed condition, whose toughness range presumably dips below 10.
- **Five unsuitable records remain**: lanthanum (a reactive rare-earth metal) and four fibre-filled polymers (PA66 with
  30% carbon fibre, PPA with 60% glass fibre, an FR-5 epoxy/glass laminate and a unidirectional epoxy/carbon
  laminate). They point to one more missing requirement: the ring track and rotor faces have to resist sliding wear,
  which these soft materials can't.

### What survives Stage 5

Stage 5 sets a hardness floor of 100 HV. Every sliding surface needs at least this, whatever the vane material; a ring
running against steel vanes would need far more, which waits for the vane choice. It removed 11 records:

- The four fibre-filled polymers and lanthanum, as intended.
- The softest metals, none of which would be used for a wear surface: gray iron EN GJL 100, AISI 1010 annealed, cast
  SA216 WCC annealed, a drawing-quality sheet steel and two commercially pure irons.

The 282 that pass are all irons and steels:

| Family | Records |
|---|---|
| Low-alloy and alloy steels | 103 |
| Tool steels | 49 |
| Martensitic stainless | 35 |
| Carbon steels | 32 |
| Sheet and wire steels | 25 |
| Ferritic and superferritic stainless | 20 |
| Structural steels | 8 |
| Gray cast iron (EN GJL 150, 200, 250, 300, 350) | 5 |
| Austenitic ductile iron (Ni-Resist) | 4 |
| Wrought iron | 1 |

No unsuitable family is left, so the screen now does what the Tree stage of the first pass did by hand. From here the
choice is between grades, on cost, wear pairing with the vanes, machinability and fatigue.

### Ranking: fatigue strength vs. price (Stage 6)

All 282 have fatigue data, so the chart drops none. Points identified by hovering; values read off the log axes, so
roughly ±20%:

| Record | Price per volume (USD/ft³) | Fatigue strength at 10⁷ cycles (ksi) |
|---|---|---|
| Gray cast iron (EN GJL 150–350; GJL 300 hovered) | About 75–100 | About 6–20 |
| Bake hardening sheet steel YS260 | About 250 | About 23 |
| Carbon steel AISI 1015, normalized | About 210 | About 35 |
| Martensitic stainless AISI 440B, tempered (top of the cluster) | About 350 | About 105 |
| Martensitic stainless AISI 414, intermediate temper | About 500 | About 60 |
| Tool steel AISI S5, tempered at 205 °C | About 850 | About 90 |
| Ni-Resist EN GJSA XNi35 | About 1,200 | About 27 |
| Patented steel wire (black point, clicked) | 227–348 | 377–392 |

What the ranking shows:

- **The highest point is a wire product.** Patented steel wire passes every stage and sits far above the cluster,
  and AISI 431 wire also passes. Nothing in the screen tests product form, and a ring, rotor or plate can't be made
  from wire, so these records are ignored here.
- **Gray iron is the cheapest material by a factor of 2–4** and has the lowest fatigue strength. Its datasheet value
  for GJL 250 is 10.4–19.6 ksi at 75–87 USD/ft³ ([below](#datasheet-values)).
- **Steels buy fatigue strength roughly in proportion to price.** Fatigue strength per dollar (a line of slope 1 on
  this chart) is about 0.15–0.2 ksi per USD/ft³ for gray iron and carbon steel, and about 0.3 for the best martensitic
  stainless. Material price isn't the whole cost: machining and heat treatment add to the steels.
- **Ni-Resist is dominated**: it costs more than almost every steel and has less fatigue strength than the carbon
  steels. Its low expansion isn't needed in a ferrous stack, so it drops out on this ranking.
- **Per part**: the ring and side plates carry mostly compressive contact and low alternating stress, so cost and wear
  decide, and gray iron fits. The rotor carries vane-slot bending and torque for about 10¹⁰ cycles, so its choice
  waits for a stress estimate, which sets a horizontal line on this chart. A steel rotor in a gray iron ring matches
  in expansion (about 6.5 against 6.1–7.2 µstrain/°F).

### Check against refrigerant pumps

How the screen's answer compares with what refrigerant machinery is made of
([references](references.md)):

| Part | Liquid refrigerant pumps (ammonia, HFC) | Rotary vane refrigerant compressors | Screen result |
|---|---|---|---|
| Ring / cylinder | — (mostly centrifugal) | Cast iron cylinder; sintered iron liner in aluminium automotive bodies | Gray iron passes ✓ |
| Side plates | — | Cast iron, matched to the rotor | Gray iron passes ✓ |
| Rotor / impeller | Cast iron impeller | Cast iron or steel rotor | Steel and gray iron pass ✓ |
| Vanes | — | Tool steel (often nitrided or coated), nodular iron, sintered iron | Tool steels pass; sintered iron has no record |
| Casing / housing | Ductile iron (low-temperature grades) or cast steel; canned-motor pumps rated to −60 °F | Cast iron or aluminium | **Ductile iron removed** (Stage 1) |
| Shaft | 304 stainless | Hardened steel | Shaft isn't screened here (group D) |

So the stack result matches practice: gray iron ring and side plates, iron or steel rotor. Two gaps:

- **Ductile iron** is a standard refrigerant pump material at low temperature, yet every ordinary grade fails Granta's
  −20 °F rating on the whole-record rule. Low-temperature grades (e.g. EN GJS 350-22-LT) are what industry uses, so
  ductile iron should come back for the rotor and housing on that evidence. For the housing it does, as a documented
  exception ([D25](decisions.md)).
- **Sintered (PM) iron and steel**, used for vanes and liners, have no material record in Level 3.

Most of the 282 are not standard for these parts: sheet and structural steels, ferritic stainless, Ni-Resist, and tool
steels anywhere but the vanes.

### Stack thresholds

All pass/fail filters go in before any datasheet lookups; datasheets are only for the finalists.

| Filter | Value | Why | Status |
|---|---|---|---|
| Service temperature | −20 °F to 150 °F | The brief | Applied (Stage 1) |
| Thermal expansion coefficient | ≤ 7.6 µstrain/°F (7.5 until [D29](decisions.md)) | The steel shaft (about 6.5) runs through the rotor, so the stack can't expand much more than steel. Removes aluminium (about 12) and austenitic stainless (about 9–10). 7.6 rather than 7.5 so AISI 4140 (6.39–7.5) passes. | Applied (Stage 2) |
| Price per unit volume | ≤ 1,500 USD/ft³ | About 18× cast iron, generous at 7,000/yr | Applied (Stage 2) |
| Fracture toughness | ≥ 10 ksi·in^0.5 | The chart shows a gap between about 5 and 10 ksi·in^0.5. A minimum there removes glasses, ceramics, concrete and foams, and also carbon-graphite. | Applied (Stage 4) |
| Fatigue strength at 10⁷ cycles | — | Needs the vane and rotor stress estimate first | Deferred |
| Hardness | ≥ 100 HV | A floor for any sliding surface. Steel vanes would need a much harder ring; that waits for the vane choice. | Applied (Stage 5) |

### First pass (2026-10-29, superseded)

The first screen wasn't saved in Granta, and it differed from the one above in two ways: it used Granta's default
"any part of record" rule, and a Tree stage that picked seven families by hand (ferrous, aluminium, titanium, and
carbon, carbide, nitride and oxide ceramics). That left 548 materials, including four cast austenitic stainless
records whose expansion ranges presumably dip under 7.5 µstrain/°F. Its findings that still hold:

- **Three expansion tiers.** On an expansion vs. price chart, irons and steels sit at about 6 µstrain/°F, graphite at
  about 2.3 and cast aluminium at about 12. Mixing tiers costs 0.002–0.003 in on the 3.1 in diameter over 170 °F, far
  outside the placeholder budget of 1 µstrain/°F. So the stack is all ferrous or all carbon. Gray iron, ductile iron
  and steel match each other.
- **Pump-grade carbon is only generic in Level 3.** Searching "graphite" found bulk graphites; the 2026-11-03 results
  list also shows generic "Resin impregnated carbon" and "Carbon/resin" records. Specific resin- or metal-impregnated
  grades still need supplier data (selection step 4).
- **No PM steel record.** Searching "sinter" and "powder" turned up sintered ceramics, magnet alloys and metal-matrix
  composites but no PM steel. Powder metallurgy is listed as a process (ProcessUniverse), not a material. PM ferrous
  parts should expand like wrought steel; confirm with supplier data.
- **Price removed titanium but not the ceramics:** silicon carbide and some aluminas cost under 1,500 USD/ft³.
- **Housing toughness**: EN 1563 impact-tests GJS 400-18-LT at −20 °C (−4 °F) and GJS 350-22-LT at −40 °C, so only
  the 350 grade is tested below our −20 °F (−29 °C) (verify against the standard). Settled in [D25](decisions.md).

### Datasheet values

From the Granta datasheets. A `*` in Granta marks an estimated value.

| Granta record | Expansion (µstrain/°F) | Price (USD/lb) | Price per volume (USD/ft³) | Hardness (HV) | Fatigue strength at 10⁷ cycles (ksi) | Fracture toughness (ksi·in^0.5) | Min. service temp. (°F) |
|---|---|---|---|---|---|---|---|
| Cast iron, gray, flake graphite, EN GJL 250 | 6.11–7.22 (4.99 at 73.4 °F) | 0.168–0.192 * | 75–86.9 * | 152–285 | 10.4–19.6 | 14.6–18.2 * | −238 to −58 |
| Cast iron, nodular graphite, EN GJS 400 18 LT | 5.56–6.94 | 0.168–0.192 * | 74.2–85.8 * | 135–150 | 28.3–29.2 | 30–49.1 | −193 to 14 |

- Gray and ductile iron cost the same per volume. Ductile iron has about twice the fatigue strength and toughness;
  gray iron is harder and its graphite flakes help under boundary lubrication.
- Gray iron's datasheet also gives expansion against temperature: 4.99 µstrain/°F at 73.4 °F. The headline range
  covers a wider temperature span, so compare materials on the headline values and use the temperature curve for
  the clearance calculation.
- GJS 400-18-LT fails Stage 1 under "whole record", and no other ordinary ductile iron grade in Level 3 passes
  Stages 1 and 2 either. GJS 350-22-LT fails Stage 1 too: Granta gives it the same minimum service temperature,
  −238 to 14 °F ([housing screen](#housing-screen-in-granta)). EN 1563 impact-tests it at −40 °C, so it comes back
  into the housing screen by hand ([D25](decisions.md)).

## Vane screen in Granta

Project `X:\ME559\pump-vanes.ces`, built 2026-11-05: Level 3, MaterialUniverse: All materials (4,392 records), every
Limit passing on the whole record. The thresholds are in [D24](decisions.md): no toughness or expansion limit, and a
price cap of 10,000 USD/ft³ instead of the stack's 1,500.

| Stage | Type | Settings | Pass when | Pass |
|---|---|---|---|---|
| 1 | Limit | Thermal properties. Maximum service temperature: minimum 150 °F. Minimum service temperature: maximum −20 °F. Logic AND. | Whole record | 2,866 of 4,392 |
| 2 | Limit | Price per unit volume: maximum 10,000 USD/ft³. | Whole record | 2,446 of 4,392 |
| 3 | Chart | Y: Fatigue strength at 10⁷ cycles (ksi), logarithmic, autoscale. X: Density (lb/in³), logarithmic, autoscale. No selection line yet. | — | 2,258 of 4,392 |

A chart stage drops records that lack data for either axis. Stage 3 drops 188 this way: honeycombs (aluminium, aramid,
glass/phenolic, glass/polyimide, polycarbonate), foams, cork and natural fibres. No vane candidate is among them.

**Candidates still in after Stage 3:**

- **Carbon and graphite**: "Resin impregnated carbon", "Metal impregnated carbon", "Carbon/resin", and the bulk carbons
  and graphites. Still generic records; specific grades come from supplier data ([D23](decisions.md)).
- **Polymers**: PEEK unfilled, 30% carbon fibre and 30% glass fibre; PAI unfilled and filled, including "PAI (graphite
  and PTFE)"; PPS grades, several with carbon fibre and PTFE; PTFE.
- **Tool steels**: all 82 records.

**PEEK wear grades fail Stage 1 for missing data.** Stage 1 removes "PEEK-modified (25-35% carbon filled, wear
grade)", "PEEK-modified (45-55% carbon filled, wear grade, high load)", "PEEK (30% carbon fiber, lubricated)",
"PEEK (40% carbon fiber)" and the other PEEK-modified records. The 25–35% wear grade (tradename AvaSpire) has no
minimum or maximum service temperature in its datasheet at all, so any temperature Limit removes it. It isn't
rated too warm or too cold: Granta has no rating. Its other values (from the datasheet; `*` marks estimates):

| Property | Value |
|---|---|
| Composition | PEEK blend (possibly with PPSU), 15–25% carbon fibre, 0–10% graphite, 0–10% PTFE * |
| Glass temperature | 303–334 °F * |
| Thermal expansion coefficient | 5.49–5.61 µstrain/°F |
| Density | 0.0524–0.0535 lb/in³ |
| Fatigue strength at 10⁷ cycles | 7.69–8.5 ksi * |
| Fracture toughness | 6.03–6.48 ksi·in^0.5 * |
| Hardness | 33–35 HV * |
| Price per unit volume | 3,060–3,260 USD/ft³ * |

Its expansion sits within about 1 µstrain/°F of the iron and steel stack, unlike unfilled PEEK (about 26). Its price
is why the stack's 1,500 cap would have been wrong for vanes. They come back by hand on the vane chart
([D26](decisions.md)). The other failing PEEK records weren't opened, so their reason isn't checked.

The ranking on the Stage 3 chart hasn't been read yet.

## Housing screen in Granta

Project `X:\ME559\pump-housing.ces`, built 2026-11-05: Level 3, MaterialUniverse: All materials, every Limit passing
on the whole record. Thresholds are in [D27](decisions.md): the stack's temperature, price and toughness, a casting
limit, and no expansion limit.

| Stage | Type | Settings | Pass when | Pass |
|---|---|---|---|---|
| 1 | Limit | Thermal properties. Maximum service temperature: minimum 150 °F. Minimum service temperature: maximum −20 °F. Logic AND. | Whole record | 2,866 of 4,392 |
| 2 | Limit | Price per unit volume: maximum 1,500 USD/ft³. | Whole record | 1,724 of 4,392 |
| 3 | Limit | Impact & fracture properties. Fracture toughness: minimum 10 ksi·in^0.5. | Whole record | 793 of 4,392 |
| 4 | Limit | Processing properties. Metal casting: Acceptable or Excellent. | Whole record | 129 of 4,392 |
| 5 | Chart | Y: Yield strength (elastic limit) (ksi). X: Price per unit volume (USD/ft³). Both logarithmic, autoscale. | — | 129 of 4,392 |
| 6 | Chart | Y: Fracture toughness (ksi·in^0.5). X: Yield strength (elastic limit) (ksi). Both logarithmic, autoscale. | — | 129 of 4,392 |

**What passes Stage 4, by family:**

| Family | Records | Examples |
|---|---|---|
| Cast aluminium | 45 | 356.0 and A356.0 sand and permanent mold T6; die-cast 380.0, A380.0, 383.0 |
| Cast magnesium | 27 | AZ91, AM60, WE43 |
| Cast austenitic stainless | 16 | CF-8, CF-8M, CF-3 |
| Ni-Resist (austenitic cast iron) | 11 | EN GJSA XNi22, XNi35 |
| Cast martensitic stainless | 9 | CA-15, CA-40, CA-6NM |
| Gray cast iron | 6 | EN GJL 100–350 |
| Cast lead alloys | 6 | Lead-calcium, lead-antimony |
| Cast carbon steel | 4 | SA216 WCC (a pressure-vessel valve-body grade) |
| Cast ferritic stainless | 3 | CB-30, CC-50 |
| Cast low alloy steel | 2 | SAE 4130, 4335M |

Lead and magnesium alloys are casting-capable but have no business in a refrigerant pressure housing, so the 33 of
them (6 lead, 27 magnesium) are removed by hand, leaving 96 ([D31](decisions.md)). What rules them out isn't in
Granta: lead is weak (about 5 ksi yield) and toxic, and magnesium corrodes and is generally kept out of contact with
halogenated refrigerants. They still show in the project file and in
[data/granta/pump-housing.tsv](../data/granta/pump-housing.tsv).

**Stage 5 readings** (clicked; ±20% off the log axes):

| Record | Price per volume (USD/ft³) | Yield strength (ksi) |
|---|---|---|
| Gray cast iron EN GJL 200 | 75.9–88.3 | 18.9–20.7 |
| Ductile iron EN GJS 350-22-LT (added by hand, D25; fails the screen) | 74.2–85.8 | 31.2–37.6 |
| Aluminium A390.0, permanent mold cast, F | 229–253 | 28.9–29 |
| Martensitic stainless CA-15, tempered at 315 °C (top of the cluster) | About 400 | About 150 |
| Lead-calcium alloy, cast, 0.3% Sn | 762–833 | 4.93–5.66 |

**GJS 350-22-LT datasheet** (Level 3; `*` marks estimates): fracture toughness 30–49.1 ksi·in^0.5, fatigue strength
26.1–28.3 ksi, elongation 22–29%, hardness 115–140 HV, expansion 5.56–6.94 µstrain/°F, price 74.2–85.8 USD/ft³ *,
minimum service temperature −238 to 14 °F. That last range is why it fails Stage 1. It is labelled on both charts
and costs the same as gray iron with about 1.7× the yield strength and twice the toughness. So it sits up and to the
left of everything else in the cheap corner of the yield vs. price chart.

Wall thickness t = pR/σ, so material cost per housing scales with price × ρ / σ_y. That ranking (an index line on
Stage 5) and leak-before-break (K_IC²/σ_y on Stage 6) haven't been drawn yet.

## Shaft screen in Granta

Project `X:\ME559\pump-shaft.ces`, built 2026-11-05 ([D28](decisions.md)). It repeats the stack's Stages 1, 2 and 4,
then charts fatigue strength against price. Stage 2 was first built with the stack's 1,500 USD/ft³ and 7.5 µstrain/°F
(434 and 293 passing); later on 2026-11-05 it was changed to 2,000 USD/ft³ ([D30](decisions.md)) and 7.6 µstrain/°F
([D29](decisions.md)). Current settings:

| Stage | Type | Settings | Pass when | Pass |
|---|---|---|---|---|
| 1 | Limit | Maximum service temperature ≥ 150 °F; minimum service temperature ≤ −20 °F | Whole record | 2,866 of 4,392 |
| 2 | Limit | Price per unit volume ≤ 2,000 USD/ft³; thermal expansion ≤ 7.6 µstrain/°F | Whole record | 538 of 4,392 |
| 3 | Limit | Fracture toughness ≥ 10 ksi·in^0.5 | Whole record | 370 of 4,392 |
| 4 | Chart | Y: Fatigue strength at 10⁷ cycles (ksi). X: Price per unit volume (USD/ft³). Both logarithmic, autoscale. | — | 370 of 4,392 |

The shaft has no hardness stage, and its price cap is higher than the stack's, so it passes more (370 against the
stack's 305).

**The two shaft steels named in [Candidates by component](#candidates-by-component) failed Stage 2 at first:**

- **AISI 4140**: normalized 4140 has expansion 6.39–7.5 µstrain/°F (6.51 at 73.4 °F), so its top value landed on the
  7.5 cap and the whole-record rule removed it. Its price, 241–368 USD/ft³, passes. The same happened in the stack's
  rotor screen. With the cap at 7.6 it passes, except the tempers at 205 °C and 315 °C, which fail Stage 1.
- **17-4PH stainless**: price 1,460–1,660 USD/ft³ (H1150) ran over 1,500. 15-5PH failed the same way. At 2,000 every
  17-4PH and 15-5PH record passes.

The two changes add 77 records, mostly stainless (50) and low alloy steels (18). AISI 4340, 416 and 420 passed
before and still do.

## Thermal expansion

Typical coefficients of thermal expansion, to confirm per grade (10⁻⁶/°F is the same as Granta's µstrain/°F):

| Material | CTE (×10⁻⁶ /°F) |
|---|---|
| Carbon-graphite | ~2–3 |
| Gray cast iron | ~6 |
| Carbon / alloy steel | ~6.5 |
| Bronze | ~10 |
| Aluminium casting alloys | ~12 |
| Unfilled PEEK | ~26 (filled grades are lower) |

Worked example: an aluminium ring around a steel rotor, 3.1 in diameter, over the 170 °F range. The diameters drift
apart by (12 − 6.5) × 10⁻⁶ × 3.1 × 170 ≈ **0.003 in**. That is larger than the clearances a thin-fluid pump needs to
hold leakage ([functional-design.md](functional-design.md#functional-risks)). This argues for matched materials in
the rotor, ring and side-plate stack.

## Fatigue

With about 10¹⁰ cycles, the question for each cyclically loaded part is whether its material has an endurance limit
at all. These are general rules; confirm values per grade (Shigley's is the standard reference):

| Material | Fatigue behaviour | Use here |
|---|---|---|
| Steels | Show an endurance limit. For wrought steel it is roughly 0.5 × ultimate strength (up to about 200 ksi ultimate) before correction factors. | Shaft, rotor, vanes if steel. The best fit for infinite-life parts. |
| Gray cast iron | Lower fatigue strength than steel, but its graphite flakes already act as notches, so it is less notch-sensitive. | Ring, housing, side plates: mostly compressive or low alternating stress. |
| Ductile iron, PM steel | Better fatigue strength than gray iron. PM fatigue strength falls with porosity, so density matters. | Rotor, ring. |
| Aluminium alloys | **No true endurance limit.** Fatigue strength is usually quoted at 5 × 10⁸ cycles and keeps falling beyond that. | Keep out of cyclically stressed parts. Acceptable for low-stress housings. |
| Polymers (PEEK) | Fatigue strength and modulus drop with temperature, and the material creeps. | Check vanes at 150 °F, not at room temperature. |
| Carbon-graphite | Brittle; fatigue cracks grow from flaws. | Keep vane bending low with short extension from the slot. |

## Consumables

The assembly BOM lists every consumable and where it's used
([final deliverables](requirements.md#final-deliverables)). Inside the housing, a consumable sits in liquid R-134a
for the life of the pump, so it needs the same compatibility check as a structural material
([Q21](open-questions.md)).

| Consumable | Likely use | Concern |
|---|---|---|
| Assembly lubricant | Wetting O-rings, vanes and bearings at assembly | Refrigeration oil (POE) is the obvious choice, but it puts oil into a pump we may design oil-free ([Q3](open-questions.md)). |
| Thread locker | Fasteners inside the housing | Check compatibility with R-134a and POE, or use mechanical locking instead. |
| Grease | Outside the housing | Inside, it could wash out into the refrigerant. |
