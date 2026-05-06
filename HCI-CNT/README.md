# HCI-CNT — Compositional Navigation Tensor

**Engine 2.0.4 · Schema 2.1.0 · 25 reference experiments · Apache-2.0**

The HCI-CNT subsystem is the Compositional Navigation Tensor implementation
inside the Hˢ research repository. It is a deterministic, fully-disclosed
software stack for analysing compositional time series and cross-sections.
Reads any compositional CSV; emits a single canonical JSON conforming to a
fixed schema; renders that JSON as a four-stage paged report family with
full hash-chained provenance.

CNT extends the classical CoDa toolkit (Aitchison, Egozcue, Pawlowsky-Glahn)
with trajectory-native operators (bearings, angular velocity, helmsman,
period-2 attractor, IR class), end-to-end determinism, and cross-dataset
inference. Classical CoDa plates (variation matrix, biplot, balance
dendrogram, SBP, ternary, scree) ship inside the same atlas — both
languages, one report.

---

## Reading order

| Volume | What it covers |
|---|---|
| [`handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md`](handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md) | CoDa foundations, CNT additions, schema 2.1.0, doctrine v1.0.1, pseudocode, side-by-side balance, glossary |
| [`handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md`](handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md) | Engine, atlas (4 stages), Mission Command, modules, adapters, 25-experiment walkthrough, conference demo, ROI/use-case decisions, integration plans |
| [`handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md`](handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md) | Determinism contract, hash-chain CoDa-community paper, talk plan + Q&A, public-trial readiness, citations |

For a 5-minute walkthrough, see Volume II §E (Engine usage) plus the
quickstart below.

---

## Repository layout

```
HCI-CNT/
├── README.md                              ← this file
│
├── handbook/                              The 3 canonical handbook volumes
│   ├── VOLUME_1_THEORY_AND_MATHEMATICS.md
│   ├── VOLUME_2_PRACTITIONER_AND_OPERATIONS.md
│   └── VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md
│
├── engine/                                Deterministic engine
│   ├── cnt.py                             Python canonical (engine 2.0.4)
│   ├── cnt.R                              R port (parity)
│   ├── native_units.py                    v1.1-B units helper
│   └── tests/                             determinism + parity tests
│
├── atlas/                                 HCI-Atlas — paged report system
│   ├── stage1_v4.py                       Order 1 (per-timestep ortho plate)
│   ├── stage2_locked.py                   Order 2 (28-plate single report)
│   ├── stage3_locked.py                   Order 3 (depth tower / IR / attractor)
│   ├── stage4_locked.py                   Order 4+ (cross-dataset inference)
│   ├── spectrum_paper.py                  Cross-dataset spectrum (PDF)
│   ├── plate_time_projector.html          Interactive 3D viewer
│   ├── det_pdf.py                         Deterministic PDF metadata
│   ├── compare.py, alias_map.py, ...
│   └── STANDARD_CALIBRATION_*             Mathematical ground-truth fixtures
│
├── mission_command/                       Orchestrator + module pipeline
│   ├── mission_command.py
│   ├── modules.py                         stage1, stage2, stage3, stage4, spectrum, projector
│   └── master_control.json                project + experiment config
│
├── tools/                                 Driver scripts
│   ├── run_pipeline.py
│   └── verify_package.py
│
├── adapters/                              Pre-parsers (raw → canonical CSV)
│   └── *.py                               13 adapters, full disclosure in Volume II §C
│
├── experiments/                           25 reference experiments
│   ├── INDEX.json                         registry with content_sha256 per experiment
│   └── codawork2026/, domain/, reference/, extended/
│       └── <id>/
│           ├── <id>_input.csv             input (hashed)
│           ├── <id>_cnt.json              canonical output (hashed)
│           └── JOURNAL.md                 per-experiment audit record
│
├── examples/                              Quickstart + tutorials
│
├── coda_community/                        Standalone preprint papers (also folded into the volumes)
│   ├── CNT_VS_CODA_BALANCE.md             technical balance book
│   ├── CNT_ROI_AND_USE_CASES.md           ROI & use-case decisions
│   ├── CNT_VERIFICATION_VALUE_FOR_CODA.md hash-chain verification proposal
│   └── cnt_roi_ternary.{pdf,png}          time-budget ternary figure
│
└── conference_demo/                       CodaWork 2026 self-contained package
    ├── README.md
    ├── DEMO_GUIDE.md                      30-minute walkthrough script
    ├── CODAWORK2026_TALK_PLAN.md          slide outline + Q&A study list
    ├── talk_deck/                         editable PowerPoint deck (10 slides)
    │   ├── CodaWork2026_CNT_Talk.pptx
    │   ├── *.svg                          source SVGs
    │   └── build_deck.js                  regenerable build script
    └── cnt_demo/                          self-contained demo folder
        ├── 01_engine/                     engine source + sample CSV
        ├── 02_per_country/                8 EMBER + World, full Stage 1/2 PDFs + JSON
        ├── 03_combined/                   spectrum + projector
        ├── 04_calibration/                Stage 1/2 ground truth
        └── 08_extended/                   extended-battery Stage 2 PDFs
```

---

## Quickstart

```bash
# From inside HCI-CNT/
pip install -r ../requirements.txt    # numpy, matplotlib, reportlab, openpyxl, scipy

# Run one experiment
python mission_command/mission_command.py ember_jpn

# Run a project (engine + Stage 1 + Stage 2 + Stage 3 + Stage 4 + spectrum + projector)
python mission_command/mission_command.py --project codawork2026_ember

# Verify the package
python tools/verify_package.py
```

---

## Status

| | |
|---|---|
| **Engine version** | 2.0.4 (Python) / 2.0.4 (R) |
| **Schema version** | 2.1.0 (additive `metadata.units`) |
| **Reference experiments** | 25 / 25 PASS at the determinism gate |
| **License** | Apache-2.0 (license grant + patent grant) |
| **Audit** | every page footer carries: engine version + signature + content_sha256 + source_sha + date |

---

## History

This subsystem began life as the standalone `HUF-CNT-System` package under the
broader Higgins Unity Framework workspace. As the v1.1.x feature set matured,
it became clear that CNT is a natural component of the Hˢ research line —
both share the same Aitchison-geometry foundations, the same simplex
operators, and the same determinism principle (`same input, same output,
always`). The standalone package is preserved at the original location as
archived history; this `HCI-CNT/` folder is the live development home.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
