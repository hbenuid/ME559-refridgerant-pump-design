# AGENTS.md

Instructions for AI agents working in this repo. People on the team use agents here, so follow these rules whoever
you're working for.

## What this repo is

The engineering notebook for ME559 Team R3: a sealless rotary vane pump for liquid R-134a, driven through a magnetic
coupling, designed to be field-repairable, remanufacturable and recyclable. It holds the requirements, research,
calculations and design decisions. It is graded on manufacturing, materials, functional and economic choices
([README.md](README.md#how-the-project-is-graded)).

Not everything happens here:

- **CAD** is done by teammates in Onshape. STEP and PDF snapshots go in `cad/`.
- **Materials** are screened in Granta EduPack and **cost** is estimated in aPriori, both in the university's Citrix.
  People run them; the results come back as exported files (for example `data/granta/*.tsv`) and are written up in
  the docs.

## Design basis

[docs/requirements.md](docs/requirements.md) is the source of truth. If this summary and that file disagree, the
file wins.

- Liquid R-134a, treated as liquid at all times over −20 °F to 150 °F ([D9](docs/decisions.md)).
- 55 psig in, 150 psig out, 3600 RPM. Design pressure 300 psig, from a pump standing idle at 150 °F (D32).
- Rotor diameter fixed at 3.1 in (D5). Flow is ours to choose (D3, D10); the smallest practical pump must deliver at
  least 85% of its swept volume at 150 °F (D34).
- 50,000 h MTBF in continuous running, in a basement in Arizona.
- 7,000 units a year over 5 years (D18).
- A standard motor outside the housing drives the pump through a magnetic coupling (D33).

## Where things go

[README.md](README.md#repo-map) has the full repo map. When you learn or decide something, record it:

| What | Where | Rule |
|---|---|---|
| A decision | [docs/decisions.md](docs/decisions.md) | Add a row to the index (next free D number, date, status) and a `## D#: Title` section with the reasons. Never delete an entry; to reverse one, add a new entry that supersedes it. Later changes go in an `Update (YYYY-MM-DD):` paragraph. |
| An unanswered question | [docs/open-questions.md](docs/open-questions.md) | Add it with the working assumption used until it's answered. When answered, move it to Answered with the date, and add a decision if it settles a design choice. |
| A source | [docs/references.md](docs/references.md) | Add it when first used and say what it's used for. Mark anything not yet checked. |
| A number | `calcs/` | Every number in the docs traces back to a script. Don't type in a computed number by hand. |
| Topic findings | `docs/` | requirements, functional-design, materials, manufacturing, economics, serviceability. |
| Teammates' notes | `notes/` | Word files kept as received. Their content is merged into the docs and cited as team notes. |

The plan for the analysis is the [order of work](docs/functional-design.md#order-of-work), with the tool for each
step in [D6](docs/decisions.md#d6-tooling).

## Running the calculations

The environment is managed with uv (Python 3.12, `pyproject.toml`, `uv.lock`). Don't use `pip` or
`python -m venv`.

```sh
uv run calcs/<script>.py      # run a script; uv installs what's missing on first use
uv add <package>              # add a dependency (updates pyproject.toml and uv.lock)
```

- Scripts print Markdown tables that are pasted into the docs. Each script's docstring says what it computes.
- R-134a properties come from CoolProp. Reuse the helpers in `calcs/r134a_properties.py`.
- `calcs/vane_pocket_model.py` takes about a minute and rewrites the PNGs in `docs/figures/`. Use `--quick` to run
  its checks without redrawing the figures. If a full run doesn't change the results, restore the figures
  (`git checkout -- docs/figures`) instead of committing new PNG bytes.
- Check each model two ways: against a hand calculation (verification) and against published or test data
  (validation).

## Writing the docs

- Plain, short sentences. Say what a number means for the design, not just the number.
- **US units only**: in, psig, °F, lbf, hp, GPM, lb/in³. Convert SI values from sources. Some older passages still
  give SI in brackets; convert them when you edit that passage.
- Link IDs where they appear: `[D32](decisions.md)`, `[Q27](open-questions.md)`, and section anchors for detail.
- Absolute dates (YYYY-MM-DD), never "yesterday" or "last week".
- Mark estimates and anything unchecked, for example "(check)".
- Wrap prose at about 120 characters, like the existing docs. Tables stay on one line per row.

## Git

- Edit files freely, but commit, push, open pull requests or merge only when asked. Never push straight to `main`.
- One branch per topic, named after the area: `calcs/<topic>` or `docs/<topic>`. Changes reach `main` through a
  GitHub pull request.
- Commit subjects are imperative and in sentence case, with no full stop (for example "Add the Level 1 vane-pocket
  model"). The body says what changed and why, with bullets for new D and Q entries.
- No AI credit anywhere: no `Co-Authored-By` trailer naming an AI, no "Generated with" line, and no mention of AI in
  commit messages, branch names or pull requests. Commits are authored by the person's own git identity.
