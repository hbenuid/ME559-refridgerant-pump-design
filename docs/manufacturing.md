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
| Cam ring (single-lobe) | Bore, then hone or grind, from casting, tube or PM blank | A round bore is cheap to hold tight. |
| Cam ring (balanced) | PM blank, then profile grinding, jig grinding, or wire EDM and finish | The non-circular profile is the main cost of the balanced layout. |
| Rotor | PM steel with formed slots, then size and grind faces; or bar stock with slots ground | Slot width and squareness to the faces are critical. PM shifts cost into tooling. |
| Vanes | Carbon-graphite: mould then grind. PEEK: injection-mould then grind. Steel: precision-ground strip, cut to length | Vane thickness against the slot sets leakage and friction. |
| Side / port plates | Cast or PM blank, face-ground or lapped flat | Flatness and parallelism set the axial clearance, the main leak path. |
| Pump body | Sand-cast gray iron and CNC; or die-cast aluminium and CNC | The material choice drives the process ([materials.md](materials.md)). |
| Shaft | Turn, harden, grind journals | Standard. |
| Housing sections (semi-hermetic) | Sand-cast iron, then CNC: O-ring grooves, sealing faces, bolt holes, bearing and cartridge bores | Replaces a welded shell ([D13](decisions.md)). Sealing-face flatness and finish set static leak tightness. |
| Pumping cartridge | Ring, rotor, vanes and side plates assembled and doweled, clearances set and checked at the factory | Sold as the field repair kit ([serviceability.md](serviceability.md)). |
| Motor | Purchased stator and rotor stack, or buy a complete motor | Make vs. buy. The stator must be removable for remanufacture. |
| Isolation valves | Purchased | — |
| Bearings, O-rings, terminal | Purchased | — |

## Critical-to-function features

These are the features where tolerance drives performance, and so drives process choice:

- **Axial (side) clearance** between rotor/vanes and side plates: the largest leak path in a thin liquid.
- **Vane-to-slot clearance**: leakage and vane tilt.
- **Ring bore form and finish**: vane tip sealing and wear.
- **Bearing bore alignment** across the pump and motor: they share a shaft, and the bores sit in separate bolted
  sections, so the joints need doweled location.
- **O-ring sealing faces**: flatness and finish at each housing joint.

## Assembly and test

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
- How semi-hermetic compressor manufacturers build and remanufacture their housings and motors.
- Fixturing and in-process gauging for side clearance.
