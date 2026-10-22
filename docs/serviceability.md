# Serviceability and end of life

Goal (2026-10-22): **field-maintainable where it's worth it; otherwise refurbishable by the manufacturer; recyclable
at end of life.** This cuts across all four rubric areas.

| Decision | Summary |
|---|---|
| [D13](decisions.md) | Semi-hermetic: a bolted housing with O-ring joints. The motor still runs in the refrigerant and there's still no shaft seal, but the unit can be opened. |
| [D14](decisions.md) | A refrigeration technician does field repair. Life-cycle cost decides which failures are repaired on site and which units go back to the factory. |
| [D15](decisions.md) | Inlet and outlet isolation valves are built into the pump. |

## Service routes

| Route | Who and where | What happens | When it's used |
|---|---|---|---|
| Field repair | Refrigeration technician, on site | Close the isolation valves and recover only the pump's own charge. Open the housing, replace a wear kit (pumping cartridge, bearings, O-rings), close it, evacuate, recharge, restart. | Failures where life-cycle cost favours it, likely wear failures with the housing and motor intact |
| Swap and return | Technician swaps the unit; the failed one goes back as a core | The site gets a new or remanufactured unit | Motor failure, housing damage, or when repair costs more than a swap |
| Factory remanufacture | Manufacturer | Strip, clean, inspect; replace all wear parts and seals; rework or replace the motor; run the same tests as a new unit; sell as remanufactured | Returned cores worth rebuilding |
| Recycling | Manufacturer or scrap processor | Separate by material: iron and steel, copper windings, aluminium, carbon and polymers | Cores not worth rebuilding |

Refrigerant is recovered at every route; in the US it may not be vented (EPA Clean Air Act Section 608).

## Design features for service

| Feature | Why | What it costs |
|---|---|---|
| Bolted housing with O-ring joints ([D13](decisions.md)) | Can be opened in the field and at the factory | Heavier castings, machined sealing faces, static leak paths, and bolt preload to hold under pressure cycles |
| Integral isolation valves ([D15](decisions.md)) | The technician recovers only the pump's small internal charge, not the system's | Valve cost and two more potential leak points |
| Replaceable pumping cartridge: ring, rotor, vanes and side plates pre-assembled on dowels | Field repair becomes one part swap with clearances set at the factory, so the technician never sets vane or side clearances. Industrial vane pumps (e.g. Eaton Vickers, Denison) sell repair "cartridge kits" this way (verify). | The cartridge must locate accurately in the housing, which adds an interface to tolerance |
| Bearings as retained, replaceable parts | Bearings wear | Retention features instead of permanent bonding |
| Motor stator removable from the housing | Allows rewind or replacement at the factory | Bolted or keyed in place, not bonded |
| Electrical terminal replaceable from outside | Terminals fail independently of the pump | — |
| Standard fasteners, few tool sizes, no special tools | Field technicians carry standard kits | — |
| Material marking on major parts | Sorting for recycling and remanufacture | — |

## Deciding what's worth repairing (D14)

For each failure mode i, compare:

```
C_field,i = wear kit + technician labour (travel + hours) + refrigerant handling + downtime
C_swap,i  = new or reman unit price − core credit + technician labour + downtime
```

Repair in the field when C_field,i < C_swap,i. The expected service cost per pump-year is
Σ λᵢ × 8,760 × min(C_field,i, C_swap,i), where λᵢ comes from the reliability prediction
([functional-design.md](functional-design.md#reliability)). The full life-cycle cost adds purchase, energy and
end-of-life value. The Hydraulic Institute and Europump guide *Pump Life Cycle Costs* is the standard framework.
Cost data is [Q13](open-questions.md).

## Effects on the other areas

- **Functional**: O-ring joints are new static leak paths. Housing bolts join the fatigue list.
- **Materials**: O-rings become replaceable service parts and must be compatible with R-134a ([materials.md](materials.md)). Separable materials help recycling: avoid bonding or potting dissimilar materials.
- **Manufacturing**: cast and machined housing sections replace the deep-drawn, welded shell. A remanufacturing line becomes part of production ([manufacturing.md](manufacturing.md)).
- **Economics**: core returns, remanufactured-unit revenue, and the repair-vs-swap split all enter the cost model ([economics.md](economics.md)).
