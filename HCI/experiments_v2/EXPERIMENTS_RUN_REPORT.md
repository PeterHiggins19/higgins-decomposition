# CNT v2.0.x Experiment Suite — Master Report

**Engine:** cnt 2.0.3
**Schema:** 2.0.0
**Last updated:** 2026-05-05T17:04:56Z
**Experiments registered:** 20

## Engine fix log within 2.0.x

| Engine | Fix |
|---|---|
| 2.0.0 | Initial schema-2 layout with coda_standard / higgins_extensions split |
| 2.0.1 | Period-1 detection requires TWO consecutive convergences (was 1) — fixed false-positive DEGENERATE on USA EMBER and Ball/TAS |
| 2.0.1 | Curvature composition uses 1/x_j² (was 1/x_j) — Math Handbook Ch 19.2(b) |
| 2.0.1 | TRIADIC_T_LIMIT default lowered 1000 → 500 |
| 2.0.2 | USER CONFIGURATION block at top of source files; metadata.engine_config echo |
| 2.0.3 | IR taxonomy gains ENERGY_STABLE_FIXED_POINT, CURVATURE_VERTEX_FLAT, D2_DEGENERATE classes |

## Summary by subdirectory

### `codawork2026/` (10/10 ok)

| Experiment | T | D | curv δ | IR class | A | content_sha256 |
|---|---|---|---|---|---|---|
| `backblaze_fleet` | 731 | 4 | **4** | CURVATURE_VERTEX_FLAT | — | `2f94e05bc7b3…` |
| `ember_chn` | 26 | 8 | **12** | CRITICALLY_DAMPED | 0.0795 | `365fad70b64f…` |
| `ember_combined_panel` | 207 | 9 | **12** | MODERATELY_DAMPED | 0.6884 | `af35425f1f80…` |
| `ember_deu` | 26 | 9 | **8** | OVERDAMPED_EXTREME | 0.9167 | `2f487dfb2c25…` |
| `ember_fra` | 26 | 9 | **14** | LIGHTLY_DAMPED | 0.2679 | `e7875f1a368d…` |
| `ember_gbr` | 26 | 9 | **6** | OVERDAMPED_EXTREME | 0.8541 | `53e7b0c117c6…` |
| `ember_ind` | 26 | 8 | **11** | LIGHTLY_DAMPED | 0.2372 | `d856da1f38d2…` |
| `ember_jpn` | 26 | 8 | **13** | CRITICALLY_DAMPED | 0.0376 | `fded914144fd…` |
| `ember_usa` | 25 | 9 | **13** | LIGHTLY_DAMPED | 0.2792 | `fae4ef547caa…` |
| `ember_wld` | 26 | 9 | **14** | LIGHTLY_DAMPED | 0.2882 | `9ee6475abb1e…` |

### `domain/` (8/8 ok)

| Experiment | T | D | curv δ | IR class | A | content_sha256 |
|---|---|---|---|---|---|---|
| `fao_irrigation_methods` | 83 | 3 | **15** | CRITICALLY_DAMPED | 0.0659 | `8e684652177b…` |
| `geochem_ball_age` | 10 | 10 | **13** | CRITICALLY_DAMPED | 0.0361 | `8957cf163106…` |
| `geochem_ball_region` | 95 | 10 | **14** | MODERATELY_DAMPED | 0.1180 | `b2dbb865f614…` |
| `geochem_ball_tas` | 15 | 10 | **12** | LIGHTLY_DAMPED | 0.1356 | `7790e3b462b4…` |
| `geochem_qin_cpx` | 30 | 9 | **15** | CRITICALLY_DAMPED | 0.0982 | `ca370596e6b9…` |
| `geochem_stracke_morb` | 5 | 10 | **12** | LIGHTLY_DAMPED | 0.1133 | `32a9418135e8…` |
| `geochem_stracke_oib` | 15 | 10 | **14** | LIGHTLY_DAMPED | 0.1137 | `bd452faad10b…` |
| `geochem_tappe_kim1` | 8 | 10 | **16** | CRITICALLY_DAMPED | 0.0663 | `64c55e0259dd…` |

### `reference/` (2/2 ok)

| Experiment | T | D | curv δ | IR class | A | content_sha256 |
|---|---|---|---|---|---|---|
| `commodities_gold_silver` | 1338 | 2 | **1** | D2_DEGENERATE | — | `e990dbde0a64…` |
| `nuclear_semf` | 76 | 5 | **10** | MODERATELY_DAMPED | 0.5995 | `975ea3d17dd9…` |

## Closure notes (final pass 2026-05-05)

* **All 20 experiments at engine 2.0.3.** Reproducibility verified.
* **USA EMBER updated to EMBER 2025 release.** T=25 (2001-2025), curv_depth=13, A=0.279, LIGHTLY_DAMPED. Sits cleanly with France/India/World cohort.
* **Stracke MORB added** (5 ocean-basin barycenters) as sister to Stracke OIB.
* **IR taxonomy rationalised**: BackBlaze now reports `CURVATURE_VERTEX_FLAT` (Errors > 60% drives recursion to vertex), Gold/Silver reports `D2_DEGENERATE` (genuine D=2 limitation). Previously both were misleadingly `DEGENERATE`.
* **Engine USER CONFIG block** at top of cnt.py / cnt.R; values echoed in `metadata.engine_config` of every JSON.
* **Auto-generated Conclusions** added to all 20 JOURNAL.md files based on IR classification + locks + EITT residuals.
* **Deferred adapters documented** in `DEFERRED_ADAPTERS.md` (Markham, IIASA, Planck, financial, ChemixHub).

## Notable findings

1. **Period-2 attractor universality** confirmed in 11 systems (8 EMBER + 3 geochem schemes + 2 reference). Plus 3 schemes (Stracke OIB/MORB, Tappe KIM) supporting the cohort.
2. **BackBlaze fleet** demonstrates the new `CURVATURE_VERTEX_FLAT` reading: energy tower stable (period-1 at Hs=0.31, depth=8), curvature tower vertex-flat due to Errors carrier dominance.
3. **FAO 3-paradigm clustering** (Surface / Sprinkler / Localized) cleanly separates traditional (China, India, Mali), temperate-mechanized (France, Germany, NZ), and water-scarce (UAE, Israel, Jordan) regimes.
4. **Stracke MORB and OIB** sit close together in geochem cohort (curv δ = 12-14, IR LIGHTLY_DAMPED).
5. **Cross-domain A ≈ 0.066 match** between Tappe kimberlite (D=10, T=8) and FAO irrigation (D=3, T=83) — same critically-damped attractor amplitude across two unrelated domains and dimensions.

## Experiment count by status

* Total registered: **20**
* All ok:           **20**
* Failed/missing:   **0**

## How to add a new experiment

1. CSV-ready data: add to `REGISTRY` in `run_experiments.py`.
2. Raw data needs transformation: add a build function (in-script) or a standalone adapter (in `adapters/`).
3. Run `python3 run_experiments.py <id>` to produce JSON + JOURNAL.md.
4. Index updates automatically.

## How to change engine behaviour

Edit the USER CONFIGURATION block at the top of `cnt.py` or `cnt.R`. Each variable is documented inline. Active values echo in `metadata.engine_config`. Two runs with same config + same input produce identical content_sha256.

## Pending data — see `DEFERRED_ADAPTERS.md`

Markham budget, IIASA NGFS, ESA Planck FITS, financial sector composition, ChemixHub. Each has documented format, transformation requirements, and estimated effort.

---

*The instrument reads. The expert decides. The loop stays open.*
