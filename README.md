# ME559 Refrigerant Pump Design — Team R3

A semi-hermetic rotary vane pump for liquid R-134a, designed to be field-repairable, remanufacturable and
recyclable. This repo is the engineering notebook for the project. It gathers
requirements, research, calculations and design decisions in one place.

Status (2026-10-22): just starting. The concept (rotary vane) is set; nothing is sized or selected yet.

## Brief

| Item | Value |
|---|---|
| Substance | R-134a refrigerant |
| Temperature | −20 °F to 150 °F |
| Inlet pressure | 55 psig |
| Outlet pressure | 150 psig |
| Speed | 3600 RPM |
| MTBF | 50,000 hours continuous operation |
| Installation | Basement of a commercial building in Arizona |
| Yearly quantity | 7,000 units per year |
| Rotor diameter | 3.1 in (fixed) |

Course guidance so far: treat the fluid as liquid at all times; the pump is standalone (no larger system); 80% of
mechanical failures are due to fatigue. [docs/requirements.md](docs/requirements.md) explains how we interpret each
line and what follows from it.

## How the project is graded

| Criterion | Weight | Notes live in |
|---|---|---|
| Understanding of manufacturing processes | 17.5% | [docs/manufacturing.md](docs/manufacturing.md) |
| Ability to choose appropriate materials | 17.5% | [docs/materials.md](docs/materials.md) |
| Ability to make functionally sound design choices | 17.5% | [docs/functional-design.md](docs/functional-design.md) |
| Ability to make economically sound design choices | 17.5% | [docs/economics.md](docs/economics.md) |
| Remaining 30% | — | Not yet known (see [open questions](docs/open-questions.md)) |

## Repo map

| Path | What it holds |
|---|---|
| [docs/requirements.md](docs/requirements.md) | The brief, our interpretation of it, and derived numbers |
| [docs/open-questions.md](docs/open-questions.md) | Unanswered questions and the working assumptions we use until they're answered |
| [docs/decisions.md](docs/decisions.md) | Decision log: what was decided, when, and why |
| [docs/functional-design.md](docs/functional-design.md) | Operating principle, sizing, vane layout trade, functional risks |
| [docs/materials.md](docs/materials.md) | Material requirements and candidates per component |
| [docs/manufacturing.md](docs/manufacturing.md) | Process candidates per component at 7,000 units/yr |
| [docs/economics.md](docs/economics.md) | Cost model structure and economic levers |
| [docs/serviceability.md](docs/serviceability.md) | Field repair, remanufacture and recycling: service routes, design features, repair-vs-swap decision |
| [docs/references.md](docs/references.md) | Sources |
| [calcs/](calcs/) | Python calculations. Every number in the docs should trace back to a script here |

CAD lives in Onshape (link TBD). STEP and PDF snapshots go in `cad/` once they exist.

## Running the calculations

```sh
python3 -m venv .venv
.venv/bin/pip install -r calcs/requirements.txt
.venv/bin/python calcs/r134a_properties.py
.venv/bin/python calcs/displacement.py
.venv/bin/python calcs/reliability.py
```

Each script prints Markdown tables that are pasted into the docs.
