# AI Refresh — 2026-05-05

## Session Summary

Single-engine CNT JSON generator established under `HCI/cnt_v2/`.
Authoritative schema (`CNT_JSON_SCHEMA.md` v2.0.0) defines a canonical
JSON layout with `coda_standard/` and `higgins_extensions/` sub-blocks
plus functional labelling (`_function ∈ {composer, review, formatter,
provenance}`). Two reference implementations: `cnt.py` (Python,
canonical) and `cnt.R` (R, parity port). 19 experiments run across the
data corpus and registered in `HCI/experiments_v2/INDEX.json`.

Two important engine fixes during the verification work
(`2.0.0 → 2.0.1`) and a user-control restructuring (`2.0.1 → 2.0.2`).
Two empirical results in `experiments_v2/` significantly extend the
robustness story of the depth-sounder period-2 attractor.

## What Changed

### 1. cnt_v2 single-engine architecture (`HCI/cnt_v2/`)

Replaces the three-program path (`cnt_tensor_engine.py` +
`cnt_analysis.py` + `cnt_depth_sounder.py`) with one program that
ingests a CSV and emits one canonical JSON. Downstream tools (plates,
projector, spectrum analyser, future viewers) read that JSON without
recomputation.

* `cnt.py` — Python canonical, 1500+ lines
* `cnt.R` — R parity port
* `CNT_JSON_SCHEMA.md` — authoritative schema (v2.0.0, 10 sections
  + migration table from v1.0.0 + CoDa↔Higgins mapping)
* `CNT_PSEUDOCODE.md` — language-neutral algorithm reference
* `parity_test.py` — cross-language parity gate
* `README.md` — usage + verification status

### 2. Schema 2.0.0 — dual classification

Every analytic block (`tensor`, `stages/{1,2,3}`, `bridges`, `depth`,
`diagnostics`) split into:

* **By ownership** — `coda_standard/` (Aitchison/Egozcue/Pawlowsky-Glahn
  /Shannon lineage) vs `higgins_extensions/` (HUF-framework readings).
  A CoDa-community reviewer reads only `coda_standard/` to audit; the
  schema's §8 documents that every Higgins extension is a function of
  CoDa-standard quantities.
* **By function** — `_function ∈ {composer, review, formatter,
  provenance}`. Plate generators read `formatter` blocks; analytical
  reports read `review` blocks; projectors read `composer` blocks.

### 3. Engine fix 2.0.0 → 2.0.1: period-1 detection

`detect_period` now requires TWO consecutive level-pair convergences
for period-1 (was 1). Mirrors the period-2 logic that always required
two same-parity convergences. Fixed false positives:

* **USA EMBER**: was curv_depth=3 / IR=DEGENERATE because L2 ≈ L1 by
  coincidence. Now curv_depth=16 / LIGHTLY_DAMPED.
* **Ball/TAS** (geochem): was curv_depth=3 / IR=DEGENERATE. Now
  curv_depth=12 / LIGHTLY_DAMPED, A=0.094, period-2 attractor confirmed.
  This *strengthens* the geochem within-domain robustness story —
  5 of 5 non-D=2 schemes now show period-2.

The "TAS is degenerate by design" claim in
`experiments/Hs-05_Geochemistry/region_binning/ROBUSTNESS_JOURNAL_v2.md`
has been retracted via inline erratum.

### 4. Engine fix 2.0.0 → 2.0.1: curvature composition formula

`derived_curvature` corrected from 1/x_j to (1−1/D)/x_j² (the actual
κ_jj diagonal of the Aitchison metric tensor). The (1−1/D) factor
cancels under closure, so the engine uses 1/x_j² directly. Matches
Math Handbook Ch 19.2(b). Effect: depth-tower trajectories now match
the legacy reference engine bit-for-bit on Japan EMBER.

### 5. Engine 2.0.1 → 2.0.2: USER CONFIGURATION block

Top of `cnt.py` and `cnt.R` is now a documented USER CONFIGURATION
block grouping all controllable constants by purpose:

* VERSION (do not edit)
* ZERO REPLACEMENT (`DEFAULT_DELTA`)
* LOCK EVENT THRESHOLDS (`DEGEN_THRESHOLD`, `LOCK_CLR_THRESHOLD`)
* DEPTH RECURSION (`DEPTH_MAX_LEVELS`, `DEPTH_PRECISION_TARGET`,
  `NOISE_FLOOR_OMEGA_VAR`)
* TRIADIC ENUMERATION (`TRIADIC_T_LIMIT`, `TRIADIC_K_DEFAULT`)
* EITT BENCH-TEST (`EITT_GATE_PCT`, `EITT_M_SWEEP_BASE`)

Each variable carries inline documentation. Active values are echoed
in `metadata.engine_config` of every JSON output. The engine_config
block is part of the deterministic content_sha256 — two runs with
identical config and identical input produce identical content_sha256;
two runs with different config produce different content_sha256, and
the JSON records exactly which config was active.

The user controls the tool, not the tool. This is a CoDa-friendly
posture: the operator owns the dial.

### 6. Experiment battery — `HCI/experiments_v2/`

Registry-driven runner (`run_experiments.py`) with 19 experiments
across three subdirectories:

| Subdir | Experiments |
|---|---|
| `codawork2026/` | EMBER 8 countries (CHN/DEU/FRA/GBR/IND/JPN/USA/WLD), combined panel (T=207), BackBlaze fleet (T=731) |
| `domain/`       | Geochemistry battery (Ball/Region, Ball/Age, Ball/TAS, Stracke OIB, Tappe KIM, Qin Cpx) + FAO Aquastat irrigation methods |
| `reference/`    | Gold/Silver D=2 (T=1338), Nuclear SEMF D=5 (T=76) |

Every experiment folder contains: source CSV (or built input CSV),
canonical CNT JSON, auto-generated `JOURNAL.md`. Selected experiments
also have an `INTERPRETATION.md` (BackBlaze fleet, FAO irrigation,
USA EMBER diagnosis).

Three working adapters live in `experiments_v2/adapters/`:

* `backblaze_adapter.py` — resumable, processes 8 quarterly zips (8 GB
  source) into 731 daily SMART means (4 carriers per Hs-17 preparser).
* `fao_irrigation_adapter.py` — pivots FAO Aquastat WIDEF.csv into
  D=3 country-by-method composition (Surface / Sprinkler / Localized).
* In-script builders for combined EMBER panel, gold/silver, nuclear SEMF.

### 7. Empirical findings worth flagging

**Period-2 attractor universality strengthened**. Geochemistry now
contributes 5 confirmed period-2 systems (Ball/Region, Ball/Age,
Ball/TAS-after-fix, Stracke OIB, Tappe KIM, Qin Cpx). Mean λ_geochem
≈ -0.61. Across 19 systems in the battery, only 2 systems are
genuinely DEGENERATE — both for documented reasons (Gold/Silver D=2
has no off-diagonal metric structure; BackBlaze fleet has Errors at
60-96% driving curvature recursion to a vertex).

**BackBlaze two-tower split**. T=731 daily SMART composition over
2024-2025 reproduces the canonical Hs-17 finding ("memoryless fleet")
via period-1 fixed point in the energy tower at Hs=0.31, depth=8.
The curvature tower hits HS_FLAT due to extreme Errors-carrier
dominance — *not* an engine bug, a real signature of single-carrier
concentration > 60%. Documented in
`experiments_v2/codawork2026/backblaze_fleet/INTERPRETATION.md`.
Action item flagged: add `ENERGY_STABLE_FIXED_POINT` and
`CURVATURE_VERTEX_FLAT` IR classes in a future engine bump.

**FAO irrigation 3-paradigm clustering**. D=3 cross-section over 83
countries cleanly separates surface-dominated (Mali, Philippines,
China, India), sprinkler-dominated (Serbia, France, Germany, NZ), and
localized-dominated (UAE, Israel, Jordan, Cyprus) regimes. Pure CoDa
setup (3 carriers sum to FAO_AS_4311 "full-control irrigation total"),
ternary-plot visualizable, reproducible by any CoDa user with `compositions::aDist()`.

**Cross-domain A ≈ 0.066 match**. Tappe kimberlite (D=10, T=8) and
FAO irrigation (D=3, T=83) both converge to amplitude A=0.066 in
CRITICALLY_DAMPED class — same value across two completely different
domains and dimensions. Suggests A may be a structural property of
cross-sectional compositions bounded by the simplex.

## What Stays True

* M² = I involution verified to ~7e-17 (IEEE 754 floor) on every
  D ≥ 3 dataset run.
* Determinism gate: `diagnostics.content_sha256` reproduces under
  re-run with same config.
* CoDa↔Higgins mapping (schema §8): every Higgins extension is
  expressible as a function of `coda_standard/` quantities. The
  CoDaWork audience can audit by reading just the CoDa-standard
  fields.
* Egozcue 2026 framing on EITT preserved: `eitt_residuals.note`
  states it is an empirical observation about trajectory smoothness,
  not a CoDa-geometric theorem about Aitchison invariance.

## Files Modified This Session

### New

* `HCI/cnt_v2/cnt.py`, `cnt.R`, `CNT_JSON_SCHEMA.md`,
  `CNT_PSEUDOCODE.md`, `parity_test.py`, `README.md`,
  `STAGE1_PLATE_CAP_SPEC.md`
* `HCI/CNT_JSON_OUTSTANDING_CONCERNS.md`
* `HCI/experiments_v2/run_experiments.py`,
  `INDEX.json`, `EXPERIMENTS_RUN_REPORT.md`
* `HCI/experiments_v2/adapters/backblaze_adapter.py`,
  `fao_irrigation_adapter.py`
* `HCI/experiments_v2/codawork2026/{ember_*}/JOURNAL.md` ×9 +
  `backblaze_fleet/{INTERPRETATION.md, ...}` +
  `ember_usa/USA_DIAGNOSIS.md`
* `HCI/experiments_v2/domain/{geochem_*, fao_irrigation_methods}/JOURNAL.md`
* `HCI/experiments_v2/reference/{commodities_gold_silver, nuclear_semf}/JOURNAL.md`

### Modified

* `experiments/Hs-05_Geochemistry/region_binning/ROBUSTNESS_JOURNAL_v2.md`
  — added erratum about TAS DEGENERATE being engine bug.
* `ai-refresh/HS_MACHINE_MANIFEST.json` — added cnt_v2 navigation
  references and 2026-05-05 change entry.
* `ai-refresh/HS_ADMIN.json` — added 2026-05-05 change entry.
* `ai-refresh/AI_REFRESH_2026-05-05.md` — this file.

## Critical Invariants for Cross-Check

A re-implementation of cnt.py in any language must reproduce these on
Japan EMBER 26-year D=8 (`ember_jpn_cnt.json`):

```
T = 26
D = 8
curvature_depth        = 13   (LIMIT_CYCLE_P2)
energy_depth           = 22
amplitude_A            = 0.0376
contraction_lyapunov   = -0.6545
classification         = CRITICALLY_DAMPED
M² residual            < 1e-15 (verified at IEEE floor)
content_sha256         = d74d1a876dccf3b488b537ace9501c89... (with default config)
```

If a different implementation produces different values, either (a)
the config differs (check `metadata.engine_config`), or (b) the
implementation has a math difference that needs investigation.

## Status

* cnt_v2 engine: **VERIFIED**, schema 2.0.0, engine 2.0.3 (Python) / 2.0.2 (R port).
* Experiments: 20/20 ok, all journals auto-generated with conclusions.
* Documents: schema, pseudocode, README, outstanding-concerns,
  experiments report, robustness journal — all refreshed.
* Admin manifests: HS_MACHINE_MANIFEST and HS_ADMIN updated.
* Master EXECUTIVE_SUMMARY.md: appended (cnt_v2 waypoint 2026-05-05).
* Deferred adapters documented (`experiments_v2/DEFERRED_ADAPTERS.md`):
  Markham, IIASA, ESA Planck, financial sector, ChemixHub.

## Closure pass 2026-05-05 (final)

* Engine 2.0.3 IR taxonomy refinement: `DEGENERATE` split into
  `ENERGY_STABLE_FIXED_POINT`, `CURVATURE_VERTEX_FLAT`, `D2_DEGENERATE`.
  BackBlaze now classifies as `CURVATURE_VERTEX_FLAT`; Gold/Silver as
  `D2_DEGENERATE`. Both were misleadingly `DEGENERATE` before.
* USA EMBER updated to EMBER 2025 release: T=25 (2001-2025),
  curv δ=13, A=0.279, LIGHTLY_DAMPED.
* Stracke MORB added (5 ocean basins) as sister to Stracke OIB.
* All 20 JOURNAL.md files have IR-class-driven Conclusions.
* Master report and INDEX.json header reflect engine 2.0.3.
* R port divergence (2.0.2 — single DEGENERATE class) noted in schema,
  README, and pseudocode.

## The instrument reads. The expert decides. The loop stays open.
