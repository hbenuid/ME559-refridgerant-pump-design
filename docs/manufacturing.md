# Manufacturing

Rubric: *understanding of manufacturing processes* (17.5%).

## Volume

At 7,000 units/yr, the line builds about 28 units per working day, or 3.5 per hour on one shift. That is medium
volume:

- High enough to justify dedicated tooling with real up-front cost: die-casting dies, PM compaction tooling,
  casting patterns and core boxes for the housing, dedicated fixtures.
- Low enough that a fully automated transfer line is hard to justify. Cells of CNC machines with dedicated fixtures
  are the likely pattern.
- Each tooling choice is a fixed cost spread over 35,000 units (5 years, [D18](decisions.md)). See
  [economics.md](economics.md).

## Process candidates by component

| Component | Candidate processes | Notes |
|---|---|---|
| Cam ring (single-lobe) | Bore, then hone or grind, from casting, tube or PM blank | A round bore is cheap to hold tight. The team proposes a honed finish of 8–16 µin Ra ([vane tip wear](functional-design.md#vane-tip-wear)). |
| Cam ring (balanced) | PM blank, then profile grinding, jig grinding, or wire EDM and finish | The non-circular profile is the main cost of the balanced layout. |
| Rotor | PM steel with formed slots, then size and grind faces; or bar stock with slots ground | Slot width and squareness to the faces are critical. PM shifts cost into tooling. |
| Vanes | Carbon-graphite: mould then grind. PEEK: injection-mould then grind. Steel: precision-ground strip, cut to length | Vane thickness against the slot sets leakage and friction. |
| Side / port plates | Cast or PM blank, face-ground or lapped flat | Flatness and parallelism set the axial clearance, the main leak path. |
| Pump body | Sand-cast gray iron and CNC; or die-cast aluminium and CNC | The material choice drives the process ([materials.md](materials.md)). |
| Shaft | Turn, harden, grind journals | Standard. |
| Housing sections | Sand-cast iron, then CNC: O-ring grooves, sealing faces, bolt holes, bearing and cartridge bores, can seat, motor adapter pilot | Replaces a welded shell ([D13](decisions.md)). Sealing-face flatness and finish set static leak tightness. |
| Pumping cartridge | Ring, rotor, vanes and side plates assembled and doweled, clearances set and checked at the factory | Sold as the field repair kit ([serviceability.md](serviceability.md)). |
| Motor | Purchased standard 2-pole flange-mounted motor | It runs in air ([D33](decisions.md)), so a catalog motor works. It bolts to an adapter that centres the outer magnet rotor around the can. |
| Magnetic coupling | Purchased inner and outer magnet rotors | The inner rotor is encapsulated against refrigerant and oil. |
| Containment can | Metal: deep-drawn or machined. Non-metallic: molded or machined | Material open ([Q28](open-questions.md)). Part of the pressure boundary, so it is leak-tested with the housing. |
| Relief valves | Purchased | Type and set points open ([Q27](open-questions.md)). |
| Isolation valves | Purchased | — |
| Bearings, O-rings | Purchased | — |

## Critical-to-function features

These are the features where tolerance drives performance, and so drives process choice:

- **Axial (side) clearance** between rotor/vanes and side plates: the largest leak path in a thin liquid.
- **Vane-to-slot clearance**: leakage and vane tilt.
- **Ring bore form and finish**: vane tip sealing and wear.
- **Bearing bore alignment** along the pump shaft: the bores sit in separate bolted sections, so the joints need
  doweled location.
- **Coupling concentricity**: the inner rotor, can and outer rotor share a small magnetic gap, so the motor adapter
  has to centre the motor on the pump shaft axis ([D33](decisions.md)).
- **Ring bore finish**: honed to 8–16 µin Ra (team proposal, [functional-design.md](functional-design.md#vane-tip-wear)).
- **O-ring sealing faces**: flatness and finish at each housing joint.

## Drawing requirements

The [final deliverables](requirements.md#final-deliverables) require each made part's drawing to show its material
and process, with GD&T for size, location, orientation and form. Any part made in a reusable mold or pattern also
shows the parting line, draft angle, and gate and ejector locations, where they apply.

### Mold and pattern callouts by process

| Process | Callouts | Notes |
|---|---|---|
| Sand casting (housing sections, iron pump body, ring or plate blanks) | Parting line, draft, gates and risers, cores, machining allowance on machined faces | The pattern is reusable; the sand mold isn't. Sand casting has no ejectors. |
| Die casting (aluminium pump body) | Parting line, draft, gates, ejector pin locations, overflows | Every callout in the handout applies. |
| Injection molding (PEEK vanes) | Parting line, draft, gate, ejector locations | The vanes are ground after molding, so the drawing should show which faces are as-molded and which are ground. |
| PM compaction (rotor, ring) | Pressing direction | The die is reusable, but there is no gate, and walls parallel to the press direction normally need no draft. Whether the handout expects these callouts on PM parts is to confirm. |
| Machined from bar, tube or strip (shaft, steel vanes) | None | Material, stock form, heat treatment and finish only. |

### GD&T for the critical features

| Feature | Likely controls |
|---|---|
| Axial clearance | Flatness and parallelism of the side-plate faces; ring width against rotor and vane length |
| Vane slots | Slot width; parallelism of the slot walls and perpendicularity to the rotor faces |
| Ring bore | Size, cylindricity (profile for a balanced cam ring), surface finish (8–16 µin Ra, honed) |
| Motor adapter pilot | Concentricity or position to the pump shaft axis, so the outer rotor clears the can |
| Bearing bores across bolted sections | Position or runout of each bore to a common datum axis set by the doweled joints |
| O-ring sealing faces and grooves | Flatness, surface finish, groove dimensions per the O-ring maker's guide |

## Assembly and test

- The assembly drawing gives a torque for every threaded fastener and lists each consumable with where it's used
  ([final deliverables](requirements.md#final-deliverables)).
- Clean, dry assembly: parts free of chips, oil residue and moisture before sealing.
- Dehydrate and evacuate the housing before charging or shipping.
- Helium leak test of the assembled housing joints.
- Run-in and performance test (flow at Δp, current draw, noise).

## Remanufacturing

Returned cores come back to the factory ([serviceability.md](serviceability.md)). The steps: recover any
refrigerant, strip, clean, inspect against reuse limits, replace all wear parts and seals, rework or replace the
motor, then run the same leak and performance tests as a new unit. This needs its own floor space, inspection gauges
and reuse criteria for each part.

## To research

- Typical achievable tolerances and costs for PM rotors and rings at this size.
- How semi-hermetic compressor manufacturers build and remanufacture their housings.
- How magnetic-drive pump makers build containment cans and size couplings.
- Fixturing and in-process gauging for side clearance.
- Whether the handout's mold callouts (draft, gates, ejectors) are expected on PM parts.
