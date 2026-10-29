# Materials

Rubric: *ability to choose appropriate materials* (17.5%).

Nothing is selected yet. Candidates below are starting points to research; material properties are typical values to
confirm against a specific grade's data sheet.

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

## Thermal expansion

Typical coefficients of thermal expansion, to confirm per grade:

| Material | CTE (×10⁻⁶ /°F) |
|---|---|
| Carbon-graphite | ~2–3 |
| Gray cast iron | ~6 |
| Carbon / alloy steel | ~6.5 |
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
