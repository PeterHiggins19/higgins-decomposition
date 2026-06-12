# AI Refresh — 2026-05-05  (v1.1.x consolidation)

**Engine:** 2.0.4   **Schema:** 2.1.0   **Experiments:** 25 / 25 PASS

## What changed since AI_REFRESH_2026-05-05.md

The earlier 2026-05-05 refresh closed v1.0.0 with 19 experiments. The
afternoon session (this refresh) drove the system from v1.0.0 into a
fully-consolidated v1.1.x state: every previously-deferred or
"reserved-for-v1.1" item is now built and locked.

## Doctrine + locks

* **Output Doctrine v1.0.1** locked at `atlas/OUTPUT_DOCTRINE.md`
  (hash-stamped). Order classification: 1 = first principles,
  2 = metric / inter-step, 3 = recursive / dynamical, 4+ = inference.
  Trajectory aggregates round UP to next integer order.
* **Stage 1 standard locked** — `atlas/stage1_v4.py` (ILR-Helmert
  orthogonal triplet, FIXED HLR scale, automatic magnitude factor).
* **Stage 2 standard locked** — `atlas/stage2_locked.py` (19-plate
  Order-2 atlas) + `STAGE2_PSEUDOCODE.md` + `stage2.R` port.
* **Calibration fixtures locked** — Stage 1 27-point HLR grid (drift
  ~1e-10), Stage 2 straight-line (directness=1.0) and closed-loop
  (directness=0.0) fixtures at IEEE floor.

## v1.1 Feature menu — all shipped

| Feature | Status | Path |
|---|---|---|
| A — Deterministic PDF backend | ✅ | `atlas/det_pdf.py` |
| B — Native units (engine adoption) | ✅ | `cnt/cnt.py` 2.0.4 + `cnt/native_units.py` |
| C — PNG / SVG export sibling | ✅ | flag in `atlas/stage1_v4.py` |
| D — Comparison atlas | ✅ | `atlas/compare.py` |
| E — Carrier alias map | ✅ | `atlas/alias_map.py` |
| F — Trajectory windowing | ✅ | `atlas/atlas.py` |
| G — Schema validator | ✅ | `tools/validate_cnt_schema.py` |
| H — Orthogonal triplet plate | ✅ | `atlas/stage1_v4.py` |
| Spectrum (paper) | ✅ | `atlas/spectrum_paper.py` |
| Plate-time projector (HTML, COMBINED) | ✅ | `atlas/plate_time_projector.html` |
| Mission Command module pipeline | ✅ | `mission_command/modules.py` |
| `engine_config_overrides` wired | ✅ | `cnt/cnt.py` `cnt_run(...)` kwarg |
| Schema 2.1.0 units block | ✅ | additive: `metadata.units.{input_units, higgins_scale_units, units_scale_factor_to_neper}` |
| Conference package | ✅ | `codawork2026_conference/cnt_demo/` |
| 5 deferred adapters built | ✅ | `experiments/extended/` |

## Engine 2.0.3 → 2.0.4 — what changed

* `cnt_run` accepts `engine_config_overrides`, `input_units`,
  `higgins_scale_units` kwargs.
* `metadata.engine_config.active_overrides` echoes the actual kwargs
  used. Different overrides → different `content_sha256` (by design).
* `metadata.units` block written for every JSON. Unit lineage is
  declarative.
* Same input + same config + same overrides + same units →
  byte-identical `content_sha256` (the determinism contract is
  preserved through the additions).

## Schema 2.0.0 → 2.1.0 — additive only

Three new optional fields:
* `metadata.units.input_units`
* `metadata.units.higgins_scale_units`
* `metadata.units.units_scale_factor_to_neper`

Plus echo `metadata.engine_config.active_overrides` (always present,
empty `{}` for default runs).

The new fields are additive; older v2.0.0 readers still parse the JSON
because they ignore unknown sibling keys.

## Reference corpus 20 → 25 experiments

Five deferred adapters built (synthetic baselines from published
recipes, swap-in points documented):

| ID | Subdir | T | D |
|---|---|---:|---:|
| markham_budget    | extended | 15  | 8  |
| iiasa_ngfs        | extended | 31  | 7  |
| esa_planck_cosmic | extended | 17  | 5  |
| financial_sector  | extended | 252 | 10 |
| chemixhub_oxide   | extended | 24  | 7  |

Full corpus run: 25 PASS / 0 FAIL / 0 ERR at engine 2.0.4.

## Mission Command module pipeline

`mission_command/modules.py` registers four post-CNT modules:
* `stage1` (per-experiment) — Order-1 plate book
* `stage2` (per-experiment) — Order-2 19-plate atlas
* `spectrum_paper` (group) — cross-dataset spectrum PDF
* `projector_html` (group) — interactive HTML projector

`mission_command/master_control.json` declares projects:
* `codawork2026_ember` — 8 EMBER + World, all 4 modules
* `codawork2026_geochem` — 7 geochem datasets, stage1 + stage2
* `reference_set` — gold/silver + nuclear SEMF, stage1 + stage2

Run via:
```
python mission_command/mission_command.py --project codawork2026_ember
python tools/run_pipeline.py codawork2026_ember
```

Every run writes a `_pipeline_manifest.json` recording paths +
sha256 + bytes for every artefact.

## Conference package

`codawork2026_conference/cnt_demo/` is self-contained:
* `01_engine/` — engine source + sample CSV
* `02_per_country/` — 8 EMBER countries + World, each with full
  Stage 1 + Stage 2 + JSON
* `03_combined/` — spectrum (paper) + projector (HTML)
* `04_calibration/` — Stage 1 27-pt grid + Stage 2 straight/loop
* `05_doctrine/` — doctrine + pseudocode + feature menu

Plus `codawork2026_conference/DEMO_GUIDE.md` — 30-minute walkthrough.

## Public-trial readiness

`PUBLIC_TRIAL_READINESS.md` at repo root maps every claim to its
evidence file. All v1.0.x limitations now resolved. The package is
audit-ready.

## Status

cnt 2.0.4 / schema 2.1.0 / 25 experiments / 4 modules / 1 conference
package / 1 readiness audit. **The instrument reads. The expert
decides. The loop stays open.**
