# Open questions

Questions we can't answer yet, with the working assumption we use in the meantime. When one is answered, move it to
[Answered](#answered) with the date, and add an entry to [decisions.md](decisions.md) if it settles a design choice.

| ID | Question | Why it matters | Working assumption | Status |
|---|---|---|---|---|
| Q2 | What are the smallest practical eccentricity and rotor length, and what flow do they give? | Flow is now an output of the geometry ([D10](decisions.md)). It sets motor size, power and cost. | Method in [functional-design.md](functional-design.md#sizing). Needs a leakage model. | Team to work out |
| Q3 | Will oil (POE) be present in the R-134a? | Oil-free means vanes and bearings run on a fluid thinner than water. Oil changes elastomer and motor-insulation compatibility. The pump is standalone, so no compressor oil arrives unless we add it on purpose. | Kept open. Design for oil-free wear (worst case) and check materials against POE too. | Open |
| Q4 | Is 3600 RPM the actual running speed or the synchronous speed of a 2-pole motor? | An induction motor slips to about 3450–3550 RPM, which lowers flow by 1–4%. | 2-pole induction motor on 60 Hz; 3600 used as an upper bound. | Open |
| Q6 | What electrical supply is available (voltage, phase)? | It sets the motor design and terminal, and whether starting current matters. | 208–230 V, 3-phase, common in US commercial buildings. | Not specified (2026-10-22); assumption stands |
| Q7 | Which codes and standards apply: ASHRAE 15, UL 60335-2-34 (hermetic and semi-hermetic motor-compressors), pressure-vessel rules for the housing? | They set the design pressure, proof and burst test factors, and electrical safety requirements for the housing and terminal. | None adopted yet. | Research |
| Q8 | The rubric shown covers 70% (4 × 17.5%). What makes up the other 30%? | It decides where effort goes. | The final-deliverables handout gives no weights. Its criteria add one thing to the four rubric areas: how well the choices are communicated in the drawings, documentation and presentation ([requirements.md](requirements.md#how-it-is-judged)). That may be the other 30%. | Ask instructor |
| Q9 | What design and proof pressure does the housing need? | The bolted housing is a pressure boundary. It sets wall thickness, bolt size and O-ring design. | 150 psig maximum operating pressure under the liquid-at-all-times assumption, with a code factor applied once Q7 is settled. | Open |
| Q11 | Which properties of R-134a make it "easier to pump"? The course hinted at this without specifics. | It probably points at a design simplification we're expected to use. | Our reading is in [requirements.md](requirements.md#r-134a-as-a-pumped-liquid): low viscosity, clean, non-corrosive, dielectric, non-flammable. | Confirm if possible |
| Q13 | What cost data feeds the repair-vs-swap decision: technician labour rate and hours, refrigerant handling, wear-kit cost, remanufactured unit price, core credit? | Without it, D14's life-cycle cost comparison can't be run. | — | Research |
| Q14 | How does the pump connect to the piping: Rotalock service valves, brazed copper stubs, or bolted O-ring flanges? | It sets how fast a unit can be swapped in a basement and how many joints can leak. It also determines what form the built-in isolation valves ([D15](decisions.md)) take. | Rotalock valves are standard on semi-hermetic compressors and combine valve and connection, but nothing is chosen. | Open |
| Q15 | How is the pump mounted: horizontal shaft on a base, or vertical shaft? | It sets thrust bearing load, vane seating at startup, footprint and service access. | Not decided. | Open |
| Q19 | When is the final presentation? | Everything is due that day: paper drawings, the digital folder and the presentation. | — | Ask instructor |
| Q21 | Which consumables (assembly oil, thread locker, grease) can be used inside the housing? | They sit in R-134a for the life of the pump, and they go in the BOM. Assembly oil also bears on [Q3](open-questions.md). | Check each against R-134a and POE; prefer mechanical locking to thread locker inside the housing ([materials.md](materials.md#consumables)). | Research |
| Q22 | Does motor heat raise any part, or the liquid entering the pump, above 150 °F? | The motor shares the housing and is cooled by the liquid. If the liquid passes the motor before the pump, or parts near the motor run hot, the Granta screen needs a higher maximum service temperature ([materials.md](materials.md#selection-in-granta), Stage 1), and expansion changes clearances further. Polymer vanes and elastomer seals are the most sensitive. | Every part is at fluid temperature, so 150 °F is the upper limit. | Open |

## Answered

| ID | Question | Answer | Date | Decision |
|---|---|---|---|---|
| Q1 | The brief gives −20 °F to 150 °F as the refrigerant temperature, but R-134a at 55 psig is liquid only below 58 °F. What does the pump see? | Treat it as liquid at all times over the full range (course guidance). | 2026-10-22 | [D9](decisions.md) |
| Q2 (system part) | What system is the pump part of? | None. It is a standalone pump that has to meet the given specs. | 2026-10-22 | [D10](decisions.md) |
| Q5 | What does "MTBF 50,000 hours" mean for design? | Industry practice: predicted MTBF = 1/Σλᵢ ≥ 50,000 h (NSWC-11 for mechanical parts), with bearings at L10h ≥ 50,000 h, a 50,000 h vane wear allowance, and infinite-life fatigue design. (Briefly read as a literal failure rate only, D11, then reversed.) | 2026-10-22 | [D12](decisions.md) |
| Q10 | R-134a is being phased down under the AIM Act. Is that a concern? | Out of scope. The course is replacing R-134a in the assignment next year. | 2026-10-22 | — |
| Q12 | Does the 50,000 h MTBF cover the whole unit or only the pump mechanism? | Pump mechanism only. The motor and other purchased parts are judged separately. | 2026-10-22 | [D17](decisions.md) |
| Q16 | Is there a noise target? | None given. Noise is minimised as a quality, with no number. | 2026-10-22 | — |
| Q17 | The deliverables handout is headed ME500 and says to upload to the ME691 shared folder. Which folder is ours? | The ME559 shared folder. The handout was reused from another course. | 2026-10-29 | — |
| Q18 | What part-numbering scheme do we use? | Assembly-coded, with ranges by assembly group. | 2026-10-29 | [D19](decisions.md) |
| Q20 | Do fasteners go in the BOM? | Yes, by standard designation with quantity and torque, and no drawing. | 2026-10-29 | [D20](decisions.md) |
| Q23 | Which ductile iron grade is rated to −20 °F, so ductile iron can be used despite Granta's temperature data? | EN GJS 350-22-LT, which EN 1563 impact-tests at −40 °C (confirm against the standard). It comes back into the housing screen as a documented exception, added by hand on the ranking chart; the screen itself stays whole-record. | 2026-11-05 | [D25](decisions.md) |
| Q24 | Should the PEEK wear grades come back into the vane screen by hand? | Yes. Granta has no service-temperature data for them; they are added by hand on the vane chart, with the rating from the supplier datasheet. | 2026-11-05 | [D26](decisions.md) |
| Q25 | Should the 7.5 µstrain/°F expansion cap move up slightly, so AISI 4140 passes? | Yes, to 7.6, for the stack and the shaft. 4140 passes, along with 22 other steels in the stack. | 2026-11-05 | [D29](decisions.md) |
| Q26 | Should the shaft get a higher price cap than 1,500 USD/ft³? | Yes, 2,000. 17-4PH and 15-5PH pass. | 2026-11-05 | [D30](decisions.md) |
