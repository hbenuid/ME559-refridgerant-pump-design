# Materials

Rubric: *ability to choose appropriate materials* (17.5%).

Nothing is selected yet. Selection is under way in Granta EduPack ([below](#selection-in-granta)). Candidates below
are starting points to research; material properties are typical values to confirm against a specific grade's data
sheet.

A material comparison document (PDF) is one of the [final deliverables](requirements.md#final-deliverables). The
candidate tables here are its starting point.

## What every material must satisfy

- **Compatibility with R-134a**, and with POE oil if oil is present ([Q3](open-questions.md)). This covers swelling,
  extraction and chemical attack. With the motor inside the housing, this applies to the motor insulation as well.
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
| F. Purchased parts | O-rings, bearings, motor, terminal, valves | The supplier sets the material | Cite the source and check R-134a/POE compatibility |

### Spec for each group

| Group | Function | Constraints | Objective | Ranking |
|---|---|---|---|---|
| A. Stack | Hold the running clearances; carry vane contact on the ring | −20 °F to 150 °F; expansion matched across the stack; grindable to a fine finish; dimensionally stable; endurance limit (rotor); hard ring track; R-134a/POE compatible | Minimum cost | Expansion vs. price per unit volume; hardness vs. price |
| B. Vanes | Slide in the slot and seal at the tip | Wear in a thin fluid; fatigue at about 10¹⁰ cycles; stable at 150 °F | Low density: centrifugal tip force scales with it, and tip force drives wear | Fatigue strength vs. density |
| C. Housing | Contain 150 psig plus the code factor ([Q9](open-questions.md)) | Toughness at −20 °F; castable; machinable | Minimum cost (mass doesn't matter in a basement) | Minimize C_m·ρ/σ_y (wall t = pR/σ); leak-before-break K_IC²/σ_y |
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
| Shaft | Alloy steel (e.g. 4140); martensitic or precipitation-hardening stainless | Carries the motor rotor; bearing journals may need hardening or a sleeve. |
| Housing (pump body) | Gray cast iron; cast aluminium | Aluminium is lighter but expands about twice as much as iron or steel (see below). |
| Housing sections (semi-hermetic) | Gray cast iron; ductile iron; cast aluminium | Bolted sections with O-ring joints ([D13](decisions.md)). It is a pressure boundary: design pressure per [Q9](open-questions.md). Ductile iron gives more toughness at −20 °F. |
| Isolation valves | Purchased refrigeration service valves (brass or steel bodies) | Must be compatible with R-134a and rated for the design pressure. |
| Electrical feed-through | Glass-to-metal sealed hermetic terminal | Usually a purchased part. |
| Motor insulation | Magnet wire and slot insulation rated for refrigerant/oil service | Must be compatible with R-134a (and POE). Hermetic-motor grades exist; verify specific products. |
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

### Stages

| Stage | Type | Settings | For | Pass |
|---|---|---|---|---|
| 1 | Limit | Thermal properties. Maximum service temperature: minimum 150 °F. Minimum service temperature: maximum −20 °F. Logic AND. | All groups | 3,757 of 4,392 |
| 2 | Chart | Y: Thermal expansion coefficient (µstrain/°F), logarithmic, autoscale. X: Price per unit volume (USD/ft³), logarithmic, autoscale. No selection box yet. | A. Stack | 3,735 of 4,392 |
| 3 | Tree | Metals and alloys \ Ferrous (730 records); Non-ferrous \ Aluminum (311) and \ Titanium (52); Ceramics and glasses \ Technical ceramics \ Carbon and graphite (27), \ Carbides (19), \ Nitrides (16) and \ Oxides (57) | A. Stack | 1,145 of 4,392 |
| 4 | Limit | Price per unit volume: maximum 1,500 USD/ft³. Thermal expansion coefficient: maximum 7.5 µstrain/°F. Logic AND. | A. Stack | 548 of 4,392 |

Notes:

- **Stage 1** uses the brief's range with no margin for motor heat ([Q17](open-questions.md)).
- **Stage 2's x-axis is price per unit volume**, not per pound. The 3.1 in rotor fixes the stack's size, so material
  cost is volume × price per volume.
- **A chart stage only passes records it can plot.** One record has no data for an axis. With the y-axis logarithmic,
  21 more drop out, because zero or negative expansion can't be plotted on a log axis. The stack needs expansion near
  2 or 6 µstrain/°F, so none of them could be stack candidates.
- **What the chart shows**: most polymers plot well above 10 µstrain/°F. The stack candidates are in the clusters
  between about 1 and 10.

### Stage 2 labels

Labelled with Search → right-click the record → Label. Expansion is read off the log axis, so it's approximate; the
datasheet values replace these in the next step. The labels were removed from the chart after Stage 4 (click a label,
press Delete) to leave a clean view; they don't follow the filters, so a filtered-out record keeps its label.

| Granta record | Possible use | Expansion (µstrain/°F, from chart) |
|---|---|---|
| Cast iron, gray, flake graphite, EN GJL 250 | Ring, rotor, side plates, housing | ~6 |
| Cast iron, nodular graphite, EN GJS 400 18 LT | Ring, rotor, housing | ~6 |
| Carbon steel, AISI 1040, normalized | Rotor, shaft | ~6 |
| Stainless steel, martensitic, AISI 410, annealed | Shaft (labelled by mistake, kept as a shaft candidate) | ~6 |
| Graphite (isotropic, HTR grade IG-110) | Stand-in for pump-grade carbon-graphite | ~2.3 |
| Aluminum, A356.0, sand cast, T6 | Housing | ~12 |

What the labels show:

- **Three separate tiers.** The irons and steels plot on top of each other at about 6, graphite sits at about 2.3, and
  cast aluminium at about 12. Mixing tiers in the stack costs about 4 µstrain/°F (ferrous with graphite), or 0.002 in
  on the 3.1 in diameter over 170 °F, and about 6 (ferrous with aluminium), or 0.003 in. Both are far outside the
  placeholder budget of 1 µstrain/°F. So the stack is all ferrous or all carbon.
- **Gray and ductile iron match each other and steel**, so a steel rotor in an iron ring stays within the budget.
- **No pump-grade carbon-graphite in Level 3.** Searching "graphite" finds bulk graphites only. The resin- or
  metal-impregnated grades used in pumps need supplier data (selection step 4).
- **No PM steel record.** Searching "sinter" and "powder" turned up sintered ceramics, magnet alloys and metal-matrix
  composites but no PM steel. Powder metallurgy is listed as a process (ProcessUniverse), not a material. PM ferrous
  parts should expand like wrought steel; confirm with supplier data.
- **Housing toughness, to check later**: EN 1563 impact-tests GJS 400-18-LT at −20 °C (−4 °F) and GJS 350-22-LT at
  −40 °C, so only the 350 grade is tested below our −20 °F (−29 °C) (verify against the standard).

### Stage 3: keep only the stack families

The Tree stage keeps the two families the expansion chart and the [comparable pumps](#viable-material-families)
point to (ferrous, carbon and graphite), plus three that are close enough to rule out with data rather than by
argument: aluminium (the obvious alternative), titanium (matches iron's expansion) and technical ceramics (carbides,
nitrides, oxides: very hard, and SiC matches carbon). Later stages on fatigue, hardness, toughness and price should
show why each loses or wins. Turn this stage off (untick it in Selection Stages) when screening vanes or the housing,
which need other families.

With only ferrous and carbon in the stage (693 passing), the Stage 2 chart showed:

- **Ferrous** plots in a tight cluster between about 6 and 10 µstrain/°F. Cast irons and plain steels sit at the low
  end near 6.
- **Carbon and graphite** spreads from about 0.2 to 5 µstrain/°F at roughly 500–1,000 USD/ft³. Expansion depends
  on grade and on direction in anisotropic grades, so "carbon" isn't one number. Pump-grade carbon needs supplier
  data.
- Of the 757 records those two families hold, 64 drop out on the temperature range or missing chart data. With all
  seven families, 1,212 records are allowed and 1,145 pass all stages.

### Stack thresholds (chosen 2026-10-29)

All pass/fail filters go in before any datasheet lookups; datasheets are only for the finalists.

| Filter | Value | Why | Status |
|---|---|---|---|
| Thermal expansion coefficient | ≤ 7.5 µstrain/°F | The steel shaft (about 6.5) runs through the rotor, so the stack can't expand much more than steel. Removes aluminium (about 12) and austenitic stainless (about 9.6). | Applied (Stage 4) |
| Price per unit volume | ≤ 1,500 USD/ft³ | About 18× cast iron, generous at 7,000/yr. Should remove titanium and most technical ceramics; keeps most carbon. | Applied (Stage 4) |
| Fatigue strength at 10⁷ cycles | — | Needs the vane and rotor stress estimate first. Until then aluminium is ruled out on fatigue in words (no endurance limit), backed by the expansion cap. | Deferred |
| Hardness | — | Depends on the vane: steel vanes need a hard ring, carbon or polymer vanes don't. | Deferred to the vane choice |
| Fracture toughness | — | Would also remove carbon, which runs in real pumps at low loads. | Deferred |

### Stage 4 result

548 of 4,392 pass, read from the results list:

| Family | Result |
|---|---|
| Cast irons, carbon and low-alloy steels, tool steels | Pass |
| Stainless steels | Ferritic, martensitic and duplex grades pass. Wrought austenitic grades (AISI 3xx) are removed. Four cast austenitic records (ASTM C… grades) still pass; check their datasheets, because austenitic stainless normally expands about 9–10 µstrain/°F. |
| Carbon and graphite | Pass |
| Silicon carbide | Pass (HIP, hot pressed, nitride bonded, reaction bonded, sintered) |
| Alumina | Some grades pass (85–99%) |
| Aluminium | Removed (expansion) |
| Titanium | Removed (price) |
| Silicon nitride, zirconia | Removed |

So expansion and price removed aluminium and titanium as expected, but not the ceramics: silicon carbide and some
aluminas are under 1,500 USD/ft³. They'll be judged on toughness and machining cost instead.

**How Granta treats ranges.** Granta stores most properties as a range, and each stage has a "Pass when" setting
(stage Settings → Pass when) with two options ([Ansys help](references.md)):

- **Any part of record within selection** (the default, used so far): a record passes if any part of its range is
  inside the limit.
- **Whole record within selection**: the whole range must be inside the limit.

That explains both surprises. GJS 400-18-LT's minimum service temperature is −193 to 14 °F; part of it is below
−20 °F, so it passes Stage 1 under "any part" but would fail under "whole record". The four cast austenitic records
presumably have expansion ranges that dip below 7.5 µstrain/°F (not checked). Under the default, Stages 1 and 4 are
looser than they read: they keep materials that only might meet the limit.

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
- GJS 400-18-LT's minimum service temperature runs up to 14 °F, above our −20 °F. It passes Stage 1 only because the
  stage uses Granta's default "any part of record" rule ([above](#stage-4-result)).

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
