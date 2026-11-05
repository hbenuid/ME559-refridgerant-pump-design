# Economics

Rubric: *ability to make economically sound design choices* (17.5%).

## Cost model structure

Per-unit cost at 7,000 units/yr:

```
unit cost = material
          + processing (machine rate × cycle time, per operation)
          + tooling / 35,000 units   (5-year horizon, D18)
          + purchased parts (motor, magnetic coupling, bearings, seals, valves)
          + assembly and test labour
          + overhead and scrap allowance
```

No numbers yet. Collect sources for material prices, machine rates and tooling costs and cite them in
[references.md](references.md). Build the model as a script in `calcs/` once we have them.

The final presentation has to state the predicted production cost per pump, and a cost comparison document (PDF) is
one of the supporting deliverables ([requirements.md](requirements.md#final-deliverables)). Each purchased part needs
a vendor part number for its drawing anyway, so catalog prices or quotes for those parts can feed the purchased-parts
line directly.

## Economic levers

| Lever | Trade |
|---|---|
| Process choice per part | Tooling-heavy processes (PM, die casting) give low per-part cost but high fixed cost. At 7,000/yr the break-even must be checked per part, not assumed. |
| Vane layout ([D7](decisions.md)) | The balanced layout's non-circular ring costs more to make, but may let us use cheaper bearings and last longer. |
| Part count | Combining the pump body with a housing section or side plate, and integrating bearing seats, cuts machining and assembly. |
| Make vs. buy | Buying a standard motor, the magnetic coupling and the bearings is likely. PM rotors and rings may be bought from a PM supplier. |
| Material matching | Matched-expansion materials may cost more per kg but allow looser machining tolerances for the same leakage. |
| Reliability | At a 50,000 h MTBF ([D12](decisions.md)), about 175 of every 1,000 units in service fail each year. Each failure is a site visit to a basement. Warranty cost is a real line item, which justifies spending on wear life and infinite-life fatigue design. |
| Serviceability ([D13](decisions.md)–[D15](decisions.md)) | A bolted housing, isolation valves and a cartridge cost more up front. In return, a failure can be fixed with a wear kit instead of a new unit, and returned cores can be remanufactured and resold. Field repair vs. swap is settled per failure mode by life-cycle cost ([serviceability.md](serviceability.md#deciding-whats-worth-repairing-d14)). |
| Drive ([D33](decisions.md)) | A catalog motor in air replaces a refrigerant-rated motor and its terminal, and motor failures are fixed on site without refrigerant handling. The magnets and containment can add cost, and a metal can wastes some power as eddy-current heat. |
| Smallest practical pump ([D10](decisions.md)) | Less material, a smaller motor, lower power. The limit is the point where leakage makes a smaller pump inefficient. |

## Market and regulatory risk

Out of scope: the course is replacing R-134a in the assignment next year ([Q10](open-questions.md#answered)). A real
product would face the US AIM Act phase-down of R-134a (GWP ≈ 1,430), which shortens product life and changes
tooling amortization. That may be worth one sentence in the economics argument.
