# CodaWork 2026 — Conference Package

This directory packages the HUF-CNT system for the CodaWork 2026 conference
demo. It is **self-contained**: every artefact you need to present, run, or
audit lives here.

```
codawork2026_conference/
├── README.md                  ← this file
├── DEMO_GUIDE.md              ← walk-through script for a 30-minute demo
└── cnt_demo/
    ├── 00_OVERVIEW.md
    ├── 01_engine/             ← engine sources (cnt.py / cnt.R) + a sample CSV
    ├── 02_per_country/        ← per-country output (JSON + Stage 1 PDF + Stage 2 PDF)
    │   ├── ember_chn/   ember_deu/   ember_fra/   ember_gbr/
    │   ├── ember_ind/   ember_jpn/   ember_usa/   ember_wld/
    ├── 03_combined/           ← cross-dataset views
    │   ├── spectrum_paper_codawork2026_ember.pdf
    │   └── plate_time_projector_codawork2026_ember.html
    ├── 04_calibration/        ← deterministic ground-truth fixtures
    │   └── 27-point Stage 1 grid + Stage 2 straight/loop trajectories
    └── 05_doctrine/           ← Output Doctrine v1.0.1 + Stage 2 pseudocode
```

## Audit chain — every link is hashed

raw CSV  →  `source_file_sha256`
              ↓ engine 2.0.3 (deterministic)
canonical JSON  →  `content_sha256`
              ↓ atlas modules (Stage 1, Stage 2, Spectrum, Projector)
plates / interactive views

For the EMBER 8-country + World corpus, every JSON's content_sha256 is
published in `experiments/INDEX.json` at the repo root.

## How to run

1. Install: `pip install -e .` from the repository root.
2. Verify: `python mission_command/mission_command.py --status`
3. Reproduce: `python mission_command/mission_command.py ember_jpn`

To run the post-CNT module pipeline (Stage 1 + Stage 2 + Spectrum + Projector
for any conformant CNT JSON):

```bash
python -m mission_command.modules        # list registered modules
python tools/run_pipeline.py codawork2026_ember
```

The pipeline writes outputs to one project folder; the manifest at
`<output_dir>/_pipeline_manifest.json` records every artefact's path,
sha256 and byte count.


## Artefact inventory

### Per-country (8 countries + World)
Each `cnt_demo/02_per_country/<id>/` contains:
- `<id>_cnt.json`                — engine 2.0.3, schema 2.0.0, deterministic
- `stage1_<id>.pdf`              — full Order-1 plate book (T+1 pages)
- `stage2_<id>.pdf`              — Order-2 19-plate atlas
- `_pipeline_manifest.json`      — paths + sha256 + bytes for every artefact

### Cross-dataset (combined views)
`cnt_demo/03_combined/`:
- `spectrum_paper_codawork2026_ember.pdf`        — 7-page spectrum (Order 2)
- `plate_time_projector_codawork2026_ember.html` — interactive 3D viewer
- `_pipeline_manifest.json`                      — group manifest

### Calibration (mathematical ground truth)
`cnt_demo/04_calibration/`:
- `STANDARD_CALIBRATION_27pt_*`            — Stage 1, 3×3×3 HLR grid (drift O(1e-10))
- `STANDARD_CALIBRATION_stage2_A_straight_*` — directness = 1.0 exactly
- `STANDARD_CALIBRATION_stage2_B_loop_*`     — directness = 0.0 exactly

### Doctrine (the contract)
`cnt_demo/05_doctrine/`:
- `OUTPUT_DOCTRINE.md`                — order classification (1/2/3/4+)
- `OUTPUT_DOCTRINE.md.sha256`         — hash stamp
- `STAGE2_PSEUDOCODE.md`              — language-neutral Stage 2 reference
- `V1.1_FEATURE_MENU.md`              — A–G feature list
- `ATLAS_PLAN.md`                     — atlas roadmap

## Public-trial readiness checklist (v1.0.x → conference-ready)

- ✅ Engine 2.0.3 deterministic across runs (Python and R parity)
- ✅ 20-experiment full-corpus determinism gate passes
- ✅ Output Doctrine v1.0.1 locked (hash-stamped)
- ✅ Stage 1 standard locked (`atlas/stage1_v4.py`)
- ✅ Stage 2 standard locked (`atlas/stage2_locked.py` + pseudocode + R port)
- ✅ Stage 1 + Stage 2 calibration fixtures with mathematically known answers
- ✅ Cross-dataset spectrum analyzer (paper PDF, FIXED scales)
- ✅ Interactive HTML plate-time projector with barycenter z-spine,
     COMBINED view across all 8 countries, only valid/known connection lines
- ✅ Mission Command module pipeline (`mission_command/modules.py`,
     `tools/run_pipeline.py`) — users select modules per project in
     `master_control.json`
- ✅ Deterministic PDF backend (`atlas/det_pdf.py`) — byte-identical PDFs
     across runs (matplotlib metadata epoch fixed; pinned matplotlib for
     full byte-identity)
- ✅ Native units helper (`cnt/native_units.py`) — INPUT_UNITS conversion
     factors + project-card formatter; metadata.units_* fields ready for
     schema 2.1.0
- ✅ Self-contained conference package (`codawork2026_conference/cnt_demo/`)

## Citation

```
Higgins, P. (2026). HUF-CNT System: Compositional Navigation Tensor
reference implementation. Version 1.0.0 (CodaWork 2026 demo build).
```

