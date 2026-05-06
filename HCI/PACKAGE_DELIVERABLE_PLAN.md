# HUF-CNT Software System — GitHub Deliverable Package Plan

**Date:** 2026-05-05
**Status:** AUDIT + PLAN. No build yet.
**Goal:** A self-contained, isolated, independently runnable GitHub package
of the entire HUF-CNT system, with full disclosure of every pre-parser,
adapter, and engine constant — engineered for user trust and determinism.

---

## 1 — Direct answer to "is there enough?"

**The specification is complete. The build is partial.** Of three tools
required for a credible release, one is fully built (cnt_v2 engine), two
are well-specified but not yet implemented (HCI-Atlas, Mission Command).
The disclosure principle is enforced piece-by-piece across the codebase
already; what's missing is consolidation into a single user-facing
handbook and a packaging shell.

**Closing the gap is bounded work.** No new science, no new design
surface — just implementation of two specified tools, document
consolidation, and packaging glue.

---

## 2 — Inventory: what exists vs what's needed

### 2a — Engine (the composer)

| Item | State | Action |
|---|---|---|
| `cnt.py` (Python) | DONE — engine 2.0.3, schema 2.0.0 | freeze, version-tag |
| `cnt.R` (R port) | engine 2.0.2 — IR taxonomy not refined | bring to 2.0.3 parity (~2 hrs) |
| `CNT_JSON_SCHEMA.md` | DONE | freeze |
| `CNT_PSEUDOCODE.md` | DONE | freeze |
| `cnt_v2/README.md` | DONE | freeze |
| Determinism test | parity script exists | promote to packaged test (~2 hrs) |

### 2b — Atlas (the reader)

| Item | State | Action |
|---|---|---|
| Design plan | DONE — `ATLAS_PLAN.md` | reference for build |
| `atlas.py` | NOT BUILT | implement Phase A+B (~5 d), catalog (~2 d) |
| `atlas.R` | NOT BUILT | port after Python settles (~2 d) |
| `ATLAS_PSEUDOCODE.md` | NOT WRITTEN | extract from atlas.py once stable (~0.5 d) |
| Per-plate renderers | NOT BUILT | ~12 plates × 0.5 d each, parallelisable |
| `atlas_catalog.json` schema | DESIGNED | implement with engine (~1 d) |
| Catalog HTML index | DESIGNED | static HTML+JS (~1 d) |

### 2c — Mission Command (the orchestrator)

| Item | State | Action |
|---|---|---|
| Design plan | DONE — `MISSION_CONTROL_PLAN.md` | reference for build |
| `mission_command.py` | NOT BUILT | the existing `run_experiments.py` is the seed; promote and harden (~3 d) |
| Master control JSON schema | DESIGNED | implement (~1 d) |
| HTML controller surface | DESIGNED | (~1-2 d, optional for v1.0) |

### 2d — Adapters / pre-parsers (the disclosure surface)

| Adapter | State | Documented |
|---|---|---|
| `backblaze_adapter.py` | working | docstring header |
| `fao_irrigation_adapter.py` | working | docstring header |
| `ember_usa_2025_adapter.py` | working | docstring header |
| `bin_stracke_MORB.py` | working | docstring header |
| `bin_stracke_OIB.py` (sister) | working | docstring header |
| `bin_ball_region.py` / `_age.py` / `_tas.py` | working | docstring headers |
| `bin_tappe_kim1.py` | working | docstring header |
| `bin_qin_cpx.py` | working | docstring header |
| Inline build functions | working | inline comments |
| `ADAPTERS_DISCLOSURE.md` | NOT WRITTEN | consolidate (~1 d) |
| `DEFERRED_ADAPTERS.md` | DONE | freeze |

### 2e — Experiments + data corpus

| Item | State | Action |
|---|---|---|
| 20 CNT JSON outputs | DONE | freeze, ship |
| 20 JOURNAL.md with conclusions | DONE | freeze, ship |
| `INDEX.json` | DONE | freeze, ship |
| `EXPERIMENTS_RUN_REPORT.md` | DONE | freeze, ship |
| Raw data CSVs | exist locally | decide what to ship vs link out |
| Original-source data (EMBER, FAO, EarthChem, BackBlaze) | local copy | document fetch instructions |

### 2f — Handbook / user manual

| Item | State | Action |
|---|---|---|
| `CNT_HANDBOOK.md` (consolidated) | NOT WRITTEN | ~3 d to write |
| Schema doc | DONE | embed in handbook |
| Pseudocode | DONE | embed in handbook |
| Atlas user guide | NOT WRITTEN (tool not built) | write with build |
| Mission Command user guide | NOT WRITTEN (tool not built) | write with build |
| Adapter disclosure | partial | ~1 d to consolidate |
| Determinism contract | scattered | ~1 d to consolidate |
| Glossary | NOT WRITTEN | ~0.5 d |
| HTML user manual catalog | NOT BUILT | ~2 d static-site generator |

### 2g — Packaging glue

| Item | State | Action |
|---|---|---|
| Top-level `README.md` | NOT WRITTEN | ~0.5 d |
| `LICENSE` | NOT CHOSEN | decide (recommend MIT or Apache-2.0) |
| `CITATION.cff` | NOT WRITTEN | ~0.25 d |
| `CHANGELOG.md` | NOT WRITTEN | ~0.5 d derive from change_history |
| `requirements.txt` / `pyproject.toml` | NOT WRITTEN | ~0.25 d |
| `DESCRIPTION` (R package) | NOT WRITTEN | ~0.25 d |
| GitHub Actions CI | NOT WRITTEN | ~1 d |
| Examples / quickstart | NOT WRITTEN | ~0.5 d |

### 2h — Aggregate

| Category | Items DONE | Items REMAINING |
|---|---|---|
| Engine | 5/6 | R port → 2.0.3, packaged test |
| Atlas | 1/8 | implement everything else |
| Mission Command | 1/4 | implement everything else |
| Adapters | 9/10 | consolidate disclosure |
| Experiments | 4/4 | freeze, decide data shipping |
| Handbook | 2/9 | write 7 sections + HTML |
| Packaging | 0/8 | write all glue |

**Estimated build to deliverable: ~15-20 working days.**

---

## 3 — Proposed package layout

```
HUF-CNT-System/                          # GitHub repo root
│
├── README.md                            # Top-level entry — what this is, install, quickstart
├── LICENSE                              # MIT or Apache-2.0
├── CITATION.cff                         # Academic citation block
├── CHANGELOG.md                         # Version history
├── pyproject.toml                       # Python package metadata
├── DESCRIPTION                          # R package metadata
├── requirements.txt                     # Python deps (minimal — stdlib + matplotlib + reportlab)
├── .github/
│   └── workflows/
│       ├── test-python.yml              # CI: determinism + parity
│       └── test-r.yml                   # CI: R port parity
│
├── handbook/                            # The CNT Software System Handbook
│   ├── CNT_HANDBOOK.md                  # Master document
│   ├── 01_introduction.md
│   ├── 02_compositional_data_basics.md
│   ├── 03_engine_cnt.md                 # cnt.py / cnt.R
│   ├── 04_schema.md                     # JSON contract
│   ├── 05_atlas.md                      # plate viewer
│   ├── 06_mission_command.md            # orchestrator
│   ├── 07_pre_parsers_disclosure.md     # FULL DISCLOSURE — every adapter explained
│   ├── 08_experiments_walkthrough.md    # all 20 experiments, data prep, result
│   ├── 09_determinism_contract.md       # the reproducibility guarantee
│   ├── 10_glossary.md
│   └── docs_html/                       # static HTML build of the handbook
│       ├── index.html
│       └── ...
│
├── cnt/                                 # The engine
│   ├── cnt.py                           # Python reference (2.0.3)
│   ├── cnt.R                            # R port (2.0.3 — bring to parity)
│   ├── CNT_JSON_SCHEMA.md
│   ├── CNT_PSEUDOCODE.md
│   ├── README.md
│   └── tests/
│       ├── test_determinism.py
│       ├── test_parity_python_r.py
│       └── golden/                      # reference JSONs for regression
│
├── atlas/                               # The plate atlas (HCI-Atlas)
│   ├── atlas.py
│   ├── atlas.R
│   ├── ATLAS_PSEUDOCODE.md
│   ├── README.md
│   ├── plate_renderers/
│   │   ├── ir_card.py
│   │   ├── m2_heatmap.py
│   │   ├── bearing_rose.py
│   │   ├── lock_timeline.py
│   │   ├── helmsman_tree.py
│   │   ├── tour_xy.py
│   │   ├── tour_xz.py
│   │   ├── tour_yz.py
│   │   └── ...
│   └── catalog/
│       ├── atlas_catalog.json
│       └── atlas_catalog.html
│
├── mission_command/                     # The orchestrator
│   ├── mission_command.py
│   ├── README.md
│   └── master_control.json              # the central control JSON
│
├── adapters/                            # FULL DISCLOSURE — every pre-parser
│   ├── ADAPTERS_DISCLOSURE.md           # Top-level disclosure doc
│   ├── ember_usa_2025_adapter.py
│   ├── backblaze_adapter.py
│   ├── fao_irrigation_adapter.py
│   ├── bin_ball_region.py
│   ├── bin_ball_age.py
│   ├── bin_ball_tas.py
│   ├── bin_stracke_oib.py
│   ├── bin_stracke_morb.py
│   ├── bin_tappe_kim1.py
│   └── bin_qin_cpx.py
│
├── experiments/                         # The reference corpus
│   ├── INDEX.json
│   ├── EXPERIMENTS_RUN_REPORT.md
│   ├── DEFERRED_ADAPTERS.md
│   ├── codawork2026/                    # 10 experiments
│   ├── domain/                          # 8 experiments
│   └── reference/                       # 2 experiments
│
├── examples/
│   ├── 01_quickstart.py                 # CSV → JSON → atlas in 20 lines
│   ├── 02_custom_dataset.py             # how to add your own CSV
│   ├── 03_custom_adapter.py             # how to write a new adapter
│   └── 04_compare_runs.py               # delta between two runs
│
└── data_pointers/                       # Where to fetch original data
    ├── DATA_FETCH.md                    # URLs and citation for every source
    └── checksums.txt                    # SHA-256 of expected raw files
```

---

## 4 — The handbook (Section 7 is the disclosure piece)

Each section is one markdown file under `handbook/`. The HTML version is
generated from the same markdown by a small static-site script.

### 4a — Sections

1. **Introduction** — what HUF, Hˢ, and CNT are; who this is for; how to read the handbook.
2. **Compositional Data Basics** — the simplex, closure, CLR/ILR, the Aitchison geometry. Cites Aitchison 1986, Egozcue 2003, Pawlowsky-Glahn 2015.
3. **Engine cnt** — flow of cnt.py / cnt.R. Every USER CONFIGURATION constant explained. Ties each output field back to the math.
4. **Schema** — the JSON contract. Every field, every type, every functional role.
5. **Atlas** — how the plate viewer reads the JSON, plate taxonomy, budget rules, compression banner semantics, catalog and run counter.
6. **Mission Command** — the orchestrator, master control JSON, multi-run management, delta-run mechanics.
7. **Pre-parsers and adapters — full disclosure.** Every adapter ever used in any experiment. For each: source format, transformation rule, why it was chosen, what it preserves, what it discards, deterministic SHA-256 of the produced CSV. **This is the trust foundation.**
8. **Experiments walkthrough.** Each of the 20 experiments. Source data, adapter (or build function), CSV, JSON, IR class, conclusion. End-to-end traceable.
9. **Determinism contract.** The reproducibility guarantee: same config + same input ⇒ same content_sha256. How the contract is enforced (config echo, hash gate, parity test). What can break it (numpy version drift in OS-level libm, etc.) and how the package mitigates.
10. **Glossary.** Every acronym, every constant, every mathematical symbol.

### 4b — HTML user manual catalog

A small Python script (no Jekyll, no Sphinx, no external dependency) walks
`handbook/*.md` and produces:

* `handbook/docs_html/index.html` — landing
* `handbook/docs_html/<n>_<title>.html` — one per section
* `handbook/docs_html/search.html` — client-side search via lunr.js (single embedded JS file)
* `handbook/docs_html/api.html` — auto-extracted from `cnt.py` and `atlas.py` docstrings

No external server. No build daemon. Pure static HTML the user can open
locally or host anywhere.

---

## 5 — Pre-parser disclosure document (the trust fulcrum)

`handbook/07_pre_parsers_disclosure.md` and its sibling
`adapters/ADAPTERS_DISCLOSURE.md` carry the same information at different
audiences. The handbook version is prose; the adapters version is
reference table.

Per adapter, the disclosure declares:

```
# <adapter_id>

**Purpose:** one sentence — what this adapter does
**Source:** path / URL / citation of the raw data
**Source format:** xlsx / NetCDF / zip / CSV / JSON / FITS / ...
**Source SHA-256 (canonical version):** ...
**Pre-parser logic (in plain English):** numbered steps the adapter follows
**What is preserved:** explicit list of fields and semantics that survive the transformation
**What is discarded:** explicit list of fields that are dropped, and why
**What is computed:** any derived quantities (barycenters, sums, etc.) with formula
**Output CSV format:** column names and types
**Output CSV SHA-256:** for the canonical run
**Determinism notes:** any sources of non-determinism (sorting, threading, RNG seeds — and how they're controlled)
**Critical-to-show because:** why this adapter must be disclosed for the experiment to be defensible
**Cross-reference:** path to the adapter source code
```

This is generated by a small `gen_disclosure.py` script that walks
`adapters/` and emits the disclosure markdown. The disclosure is itself
deterministic — the SHAs in it are reproducible from the source files.

---

## 6 — Why the disclosure matters (and is already mostly enforceable)

The disclosure principle Peter calls out — full visibility for user
confidence — is already enforced at the code level:

* Every engine constant is in the USER CONFIGURATION block at the top of `cnt.py`/`cnt.R`. The block is explicit, documented, and echoed in `metadata.engine_config` of every JSON. Two runs with different configs produce different content_sha256 — the change is visible.
* Every adapter is open-source Python with an explanatory docstring. The transformation is auditable line by line.
* Every CNT JSON carries `metadata.input_csv_sha256`, `metadata.engine_version`, `metadata.engine_config`, and `diagnostics.content_sha256`. The provenance chain is: raw data → CSV (SHA) → CNT JSON (SHA) → atlas (SHA, planned). Every link hashed.
* Every experiment has a JOURNAL.md with conclusions linked to the IR classification and the provenance metadata.
* The 20 reference experiments demonstrate the system on real, third-party data (EMBER, EarthChem, FAO, BackBlaze) — not toy datasets.

The work for the deliverable is **consolidation**, not invention.

---

## 7 — Build order (concrete sequence)

This is the order I recommend if we go ahead. Each phase produces something
runnable; nothing is hostage to a later phase.

| Phase | Days | Deliverable |
|---|---|---|
| **0** Repository scaffold | 0.5 | Empty repo, layout, LICENSE, CITATION, top README |
| **1** Bring R port to 2.0.3 | 0.5 | cnt.R parity with cnt.py |
| **2** Promote determinism test | 0.5 | tests/ passes; CI runs |
| **3** Atlas Phase A: 6 analytical plates | 3 | Single-page atlas PDF |
| **4** Atlas Phase B: tour plates + budget | 2 | Full-feature atlas |
| **5** Atlas catalog + run counter | 2 | Multi-run management |
| **6** Atlas HTML catalog index | 1 | Browseable run history |
| **7** Mission Command from run_experiments.py | 3 | Orchestrator with master control JSON |
| **8** Handbook sections 1-6 + 9-10 | 3 | Core handbook |
| **9** Adapter disclosure consolidation | 1 | `ADAPTERS_DISCLOSURE.md` + handbook §7 |
| **10** Experiments walkthrough handbook §8 | 1 | One narrative per experiment |
| **11** HTML user manual generator | 2 | Static-site catalog |
| **12** Examples + quickstart | 0.5 | Five-minute first-run experience |
| **13** Final verification + release tag | 0.5 | v1.0.0 |

**Total: ~20 days end-to-end.** Phases 3-6 (atlas) are the heavy lift;
everything else is documentation and packaging.

---

## 8 — What's blocked vs unblocked

**Unblocked (can start any time):**

* Phase 0 (scaffold)
* Phase 1 (R port to 2.0.3)
* Phase 2 (test promotion)
* Phase 7 (Mission Command — `run_experiments.py` is the seed)
* Phase 8 (handbook core sections)
* Phase 9 (adapter disclosure — material exists)
* Phase 10 (experiments walkthrough — material exists)

**Soft-blocked on atlas existence:**

* Atlas user manual section
* Atlas examples
* HTML catalog wiring (atlas catalog format) — though the schema is designed and could be drafted independently

**Hard-blocked on nothing.** No external decisions are pending.

---

## 9 — Recommended decisions to make before build

| Decision | Options | Recommendation |
|---|---|---|
| LICENSE | MIT / Apache-2.0 / BSD-3 / GPL-3 | Apache-2.0 — permissive + patent grant + attribution |
| Repo name | `HUF-CNT`, `Higgins-CNT`, `cnt-system`, `compositional-navigation-tensor` | `HUF-CNT-System` — matches handbook title |
| Package name (Python) | `huf_cnt`, `cnt`, `compositional_nav_tensor` | `huf_cnt` — short, namespace-safe |
| Package name (R) | `HufCnt`, `cnt`, `compositionalNavTensor` | `HufCnt` — CRAN naming convention |
| PDF backend | reportlab / matplotlib PdfPages | reportlab + matplotlib hybrid (per ATLAS_PLAN §15) |
| Data shipping | ship CSVs / link to sources / both | both — ship reduced/derived, link to raw with checksums |
| Versioning | semver / calver | semver. v1.0.0 = first ship. |
| Citation target | paper preprint / Zenodo DOI / GitHub release | Zenodo DOI on first tag |

---

## 10 — Risks and mitigations

| Risk | Probability | Mitigation |
|---|---|---|
| numpy/matplotlib version drift breaks determinism | medium | pin versions in `requirements.txt`; CI verifies `content_sha256` against golden file |
| Reportlab PDF rendering varies by font availability | medium | embed fonts; document required system fonts |
| R port lags Python | low | parity test in CI — CI fails if engines diverge on golden inputs |
| Large data files exceed GitHub size limits | medium | ship pipeline-ready CSVs only (small); raw data via external links + checksums |
| User config drift from "factory defaults" → support burden | low | factory `engine_config` in handbook; CI verifies factory run reproduces published SHAs |
| Adapter requires proprietary library (xlsx) | low | use openpyxl (BSD); avoid xlrd/xlwings |

---

## 11 — Minimum viable release (if 20 days is too much)

If full delivery is too long, a **v0.9 minimum viable release** is
~7 days:

* Phase 0 (scaffold) + Phase 1 (R parity) + Phase 2 (tests)
* Phase 8 condensed (single-document handbook, no per-section split)
* Phase 9 (adapter disclosure)
* Phase 10 condensed (one-pager per experiment, not full narrative)
* `run_experiments.py` ships as-is, renamed to `mission_command.py` light edition
* Atlas deferred to v1.0
* No HTML manual (markdown only)

This v0.9 already supports: install, ingest CSV, run engine, get
deterministic JSON, browse 20 reference experiments. No plate viewer,
but everything underneath the plate viewer is shippable.

---

## 12 — The trust property — restated

The package is **deterministic**: same input + same config produces same
SHA-256. Every tool's config is human-readable and echoes into the
output. Every adapter is auditable Python. Every experiment is a worked
example with full provenance. The user can:

1. Read the handbook.
2. Read any adapter and understand the transformation.
3. Re-run any experiment and verify the SHA matches.
4. Drop in their own CSV and get a CNT JSON whose SHA proves engine state.
5. Pin engine version + config and ship a reproducibility certificate alongside their paper.

Nothing in the package is opaque, and nothing in the package depends on
opaque outside services. The only third-party dependencies are
mathematical libraries (numpy, matplotlib, reportlab; base R + ggplot2)
all open-source and version-pinned.

---

## 13 — Recommendation

**Yes — build.** The plan is concrete, the gap is bounded, and the
disclosure principle is already enforced everywhere it needs to be.

Suggested next-action sequence:

1. Make the four small decisions in §9 (license, names, backend, data shipping).
2. Run **Phase 0** (scaffold) — half a day to a clean repo.
3. Run **Phases 1, 2, 8, 9, 10 in parallel-ish** — these are doc/parity work, no shared blockers.
4. Run **Phases 3-6 (atlas)** as the heavy build.
5. Run **Phase 7 (Mission Command)** — straightforward promotion from the existing runner.
6. Run **Phases 11-13** — wrap and ship.

If you say go, we can scaffold the repo today and have a v0.9 deliverable
inside a week, full v1.0 inside three.

---

*The instrument reads. The expert decides. The loop stays open.*
*The package is the loop, packaged.*
