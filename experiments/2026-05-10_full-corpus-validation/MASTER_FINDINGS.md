# Full-corpus validation — Master findings (2026-05-10)

**Engines:** CNT vv3.0.0 + CNQ vv2.0.0
**Doctrines:** SEA-1.0, STP-1.0, CRD-1.0, engine-independence (push #32)
**Run date:** 2026-05-10
**Datasets attempted:** 101
**Datasets that ran end-to-end:** 100
**Datasets that failed or had missing inputs:** 1

This is the citation-grade reference suite for the latest CNT v3 + CNQ v2 engines applied across the entire DATA folder. **No simulated data** — every input CSV was a real-world dataset with a documented source. These runs are the canonical worked examples of compositional analysis using the Hs framework as of push #33.

## Cross-domain headline grid

| Domain | Dataset | T | D | IR class | flips | stability | A | ζ | M²=I |
|---|---|---|---|---|---|---|---|---|---|
| backblaze | backblaze_fleet | 731 | 4 | `MODERATELY_DAMPED` | 220 | 0.698 | 0.216 | -0.000 | 1.1e-16 |
| chemistry | chemistry_chemixhub_oxide | 24 | 7 | `MODERATELY_DAMPED` | 9 | 0.591 | 0.175 | -0.009 | 5.6e-17 |
| commodities | commodities_gold_silver | 1338 | 2 | `D2_DEGENERATE` | 161 | 0.879 | 0.397 | +0.000 | 0.0e+00 |
| energy | energy_ember_chn | 26 | 8 | `LIGHTLY_DAMPED` | 12 | 0.500 | 0.942 | +0.032 | 1.1e-16 |
| energy | energy_ember_combined_panel | 207 | 9 | `LIGHTLY_DAMPED` | 107 | 0.478 | 8.392 | +0.001 | 1.5e-13 |
| energy | energy_ember_deu | 26 | 9 | `OVERDAMPED_EXTREME` | 13 | 0.458 | 6.824 | -0.012 | 8.9e-14 |
| energy | energy_ember_fra | 26 | 9 | `MODERATELY_DAMPED` | 12 | 0.500 | 0.177 | -0.043 | 1.1e-16 |
| energy | energy_ember_gbr | 26 | 9 | `OVERDAMPED_EXTREME` | 15 | 0.375 | 7.505 | -0.008 | 2.5e-14 |
| energy | energy_ember_ind | 26 | 8 | `LIGHTLY_DAMPED` | 15 | 0.375 | 0.616 | +0.019 | 1.1e-16 |
| energy | energy_ember_jpn | 26 | 8 | `LIGHTLY_DAMPED` | 17 | 0.292 | 7.012 | +0.019 | 1.7e-16 |
| energy | energy_ember_usa | 25 | 9 | `OVERDAMPED_EXTREME` | 8 | 0.652 | 9.688 | -0.084 | 3.3e-13 |
| energy | energy_ember_wld | 26 | 9 | `LIGHTLY_DAMPED` | 4 | 0.833 | 0.135 | +0.004 | 5.6e-17 |
| energy | energy_owid_are | 16 | 8 | `OVERDAMPED_EXTREME` | 7 | 0.500 | 1.404 | -0.111 | 1.1e-16 |
| energy | energy_owid_arg | 60 | 8 | `LIGHTLY_DAMPED` | 40 | 0.310 | 3.149 | +0.021 | 1.1e-16 |
| energy | energy_owid_aus | 60 | 8 | `OVERDAMPED_EXTREME` | 26 | 0.552 | 1.440 | -0.005 | 1.1e-16 |
| energy | energy_owid_aut | 60 | 8 | `LIGHTLY_DAMPED` | 32 | 0.448 | 0.155 | +0.018 | 1.1e-16 |
| energy | energy_owid_aze | 37 | 8 | `LIGHTLY_DAMPED` | 22 | 0.371 | 1.057 | +0.017 | 1.1e-16 |
| energy | energy_owid_bel | 60 | 8 | `LIGHTLY_DAMPED` | 30 | 0.483 | 0.815 | +0.019 | 1.1e-16 |
| energy | energy_owid_bgd | 54 | 8 | `LIGHTLY_DAMPED` | 30 | 0.423 | 0.729 | +0.015 | 1.1e-16 |
| energy | energy_owid_bgr | 60 | 8 | `LIGHTLY_DAMPED` | 32 | 0.448 | 1.365 | +0.027 | 1.1e-16 |
| energy | energy_owid_blr | 40 | 8 | `OVERDAMPED_EXTREME` | 17 | 0.553 | 4.215 | -0.044 | 2.2e-16 |
| energy | energy_owid_bra | 60 | 8 | `OVERDAMPED_EXTREME` | 20 | 0.655 | 3.553 | -0.009 | 1.1e-16 |
| energy | energy_owid_can | 60 | 8 | `LIGHTLY_DAMPED` | 30 | 0.483 | 1.321 | +0.007 | 5.6e-17 |
| energy | energy_owid_che | 56 | 8 | `LIGHTLY_DAMPED` | 30 | 0.444 | 0.645 | +0.015 | 5.6e-17 |
| energy | energy_owid_chl | 60 | 8 | `MODERATELY_DAMPED` | 33 | 0.431 | 0.501 | -0.001 | 2.8e-17 |
| energy | energy_owid_chn | 60 | 8 | `OVERDAMPED_EXTREME` | 26 | 0.552 | 1.742 | -0.020 | 2.8e-17 |
| energy | energy_owid_col | 60 | 8 | `LIGHTLY_DAMPED` | 43 | 0.259 | 0.183 | +0.008 | 5.6e-17 |
| energy | energy_owid_cyp | 21 | 8 | `LIGHTLY_DAMPED` | 12 | 0.368 | 0.574 | +0.011 | 1.4e-17 |
| energy | energy_owid_cze | 60 | 8 | `LIGHTLY_DAMPED` | 27 | 0.534 | 1.536 | +0.012 | 1.1e-16 |
| energy | energy_owid_deu | 60 | 8 | `LIGHTLY_DAMPED` | 37 | 0.362 | 1.760 | +0.009 | 1.1e-16 |
| energy | energy_owid_dnk | 47 | 8 | `LIGHTLY_DAMPED` | 29 | 0.356 | 1.908 | +0.053 | 1.1e-16 |
| energy | energy_owid_dza | 60 | 8 | `OVERDAMPED_EXTREME` | 26 | 0.552 | 0.787 | -0.002 | 1.1e-16 |
| energy | energy_owid_ecu | 35 | 8 | `LIGHTLY_DAMPED` | 19 | 0.424 | 1.140 | +0.020 | 2.2e-16 |
| energy | energy_owid_egy | 60 | 8 | `LIGHTLY_DAMPED` | 24 | 0.586 | 0.707 | +0.008 | 6.9e-18 |
| energy | energy_owid_esp | 57 | 8 | `OVERDAMPED_EXTREME` | 34 | 0.382 | 1.768 | -0.002 | 5.6e-17 |
| energy | energy_owid_est | 26 | 8 | `LIGHTLY_DAMPED` | 11 | 0.542 | 0.548 | +0.021 | 1.1e-16 |
| energy | energy_owid_fin | 51 | 8 | `LIGHTLY_DAMPED` | 31 | 0.367 | 2.561 | +0.005 | 1.1e-16 |
| energy | energy_owid_fra | 60 | 8 | `LIGHTLY_DAMPED` | 25 | 0.569 | 0.418 | +0.014 | 1.1e-16 |
| energy | energy_owid_gbr | 60 | 8 | `MODERATELY_DAMPED` | 37 | 0.362 | 0.522 | -0.004 | 1.1e-16 |
| energy | energy_owid_grc | 43 | 8 | `OVERDAMPED_EXTREME` | 24 | 0.415 | 2.909 | -0.011 | 1.1e-16 |
| energy | energy_owid_hkg | 19 | 8 | `MODERATELY_DAMPED` | 7 | 0.588 | 0.454 | -0.013 | 2.2e-16 |
| energy | energy_owid_hrv | 35 | 8 | `LIGHTLY_DAMPED` | 16 | 0.515 | 2.594 | +0.010 | 1.1e-16 |
| energy | energy_owid_hun | 60 | 8 | `OVERDAMPED_EXTREME` | 27 | 0.534 | 0.743 | -0.002 | 5.6e-17 |
| energy | energy_owid_idn | 60 | 8 | `OVERDAMPED_EXTREME` | 41 | 0.293 | 1.608 | -0.016 | 1.1e-16 |
| energy | energy_owid_ind | 60 | 8 | `LIGHTLY_DAMPED` | 30 | 0.483 | 2.008 | +0.005 | 1.1e-16 |
| energy | energy_owid_irl | 46 | 8 | `LIGHTLY_DAMPED` | 19 | 0.568 | 0.296 | +0.015 | 1.1e-16 |
| energy | energy_owid_irn | 60 | 8 | `OVERDAMPED_EXTREME` | 32 | 0.448 | 1.476 | -0.017 | 1.1e-16 |
| energy | energy_owid_isr | 44 | 8 | `LIGHTLY_DAMPED` | 25 | 0.405 | 1.154 | +0.000 | 5.6e-17 |
| energy | energy_owid_ita | 60 | 8 | `LIGHTLY_DAMPED` | 28 | 0.517 | 0.946 | +0.006 | 1.1e-16 |
| energy | energy_owid_jpn | 60 | 8 | `LIGHTLY_DAMPED` | 30 | 0.483 | 1.968 | +0.007 | 1.1e-16 |
| energy | energy_owid_kaz | 40 | 8 | `LIGHTLY_DAMPED` | 20 | 0.474 | 2.471 | +0.020 | 1.1e-16 |
| energy | energy_owid_kor | 48 | 8 | `LIGHTLY_DAMPED` | 29 | 0.370 | 1.807 | +0.005 | 2.8e-17 |
| energy | energy_owid_lka | 25 | 8 | `LIGHTLY_DAMPED` | 15 | 0.348 | 0.895 | +0.002 | 1.1e-16 |
| energy | energy_owid_ltu | 40 | 8 | `LIGHTLY_DAMPED` | 20 | 0.474 | 0.379 | +0.021 | 2.2e-16 |
| energy | energy_owid_lux | 56 | 8 | `LIGHTLY_DAMPED` | 37 | 0.315 | 0.510 | +0.008 | 1.1e-16 |
| energy | energy_owid_lva | 40 | 8 | `OVERDAMPED_EXTREME` | 26 | 0.316 | 2.749 | -0.012 | 1.1e-16 |
| energy | energy_owid_mar | 60 | 8 | `OVERDAMPED_EXTREME` | 36 | 0.379 | 3.226 | -0.012 | 2.8e-17 |
| energy | energy_owid_mex | 60 | 8 | `OVERDAMPED_EXTREME` | 34 | 0.414 | 1.963 | -0.017 | 1.1e-16 |
| energy | energy_owid_mkd | 27 | 8 | `LIGHTLY_DAMPED` | 16 | 0.360 | 0.316 | +0.029 | 5.6e-17 |
| energy | energy_owid_mys | 55 | 8 | `LIGHTLY_DAMPED` | 30 | 0.434 | 1.044 | +0.011 | 2.2e-16 |
| energy | energy_owid_nld | 57 | 8 | `LIGHTLY_DAMPED` | 34 | 0.382 | 0.730 | +0.033 | 1.1e-16 |
| energy | energy_owid_nor | 48 | 8 | `LIGHTLY_DAMPED` | 27 | 0.413 | 0.117 | +0.024 | 1.1e-16 |
| energy | energy_owid_nzl | 55 | 8 | `LIGHTLY_DAMPED` | 30 | 0.434 | 0.283 | +0.010 | 5.6e-17 |
| energy | energy_owid_pak | 60 | 8 | `OVERDAMPED_EXTREME` | 18 | 0.690 | 2.555 | -0.000 | 1.1e-16 |
| energy | energy_owid_per | 60 | 8 | `OVERDAMPED_EXTREME` | 40 | 0.310 | 3.996 | -0.015 | 1.1e-16 |
| energy | energy_owid_phl | 31 | 8 | `LIGHTLY_DAMPED` | 15 | 0.483 | 1.620 | +0.045 | 5.6e-17 |
| energy | energy_owid_pol | 60 | 8 | `MODERATELY_DAMPED` | 21 | 0.638 | 0.518 | -0.001 | 1.1e-16 |
| energy | energy_owid_prt | 36 | 8 | `LIGHTLY_DAMPED` | 17 | 0.500 | 4.211 | +0.014 | 2.8e-17 |
| energy | energy_owid_rou | 60 | 8 | `MODERATELY_DAMPED` | 36 | 0.379 | 0.275 | -0.011 | 5.6e-17 |
| energy | energy_owid_rus | 40 | 8 | `OVERDAMPED_EXTREME` | 24 | 0.368 | 1.553 | -0.035 | 1.1e-16 |
| energy | energy_owid_sau | 17 | 8 | `MODERATELY_DAMPED` | 7 | 0.533 | 0.230 | -0.003 | 5.6e-17 |
| energy | energy_owid_sgp | 17 | 8 | `LIGHTLY_DAMPED` | 8 | 0.467 | 1.838 | +0.005 | 1.1e-16 |
| energy | energy_owid_svk | 60 | 8 | `LIGHTLY_DAMPED` | 29 | 0.500 | 1.155 | +0.021 | 1.1e-16 |
| energy | energy_owid_svn | 35 | 8 | `MODERATELY_DAMPED` | 20 | 0.394 | 0.197 | -0.026 | 5.6e-17 |
| energy | energy_owid_swe | 60 | 8 | `LIGHTLY_DAMPED` | 23 | 0.603 | 2.747 | +0.003 | 1.1e-16 |
| energy | energy_owid_tha | 44 | 8 | `LIGHTLY_DAMPED` | 25 | 0.405 | 0.296 | +0.007 | 5.6e-17 |
| energy | energy_owid_tkm | 26 | 8 | `LIGHTLY_DAMPED` | 9 | 0.625 | 0.736 | +0.027 | 1.1e-16 |
| energy | energy_owid_tur | 43 | 8 | `LIGHTLY_DAMPED` | 24 | 0.415 | 0.561 | +0.006 | 5.6e-17 |
| energy | energy_owid_twn | 60 | 8 | `OVERDAMPED_EXTREME` | 38 | 0.345 | 1.805 | -0.019 | 1.1e-16 |
| energy | energy_owid_ukr | 40 | 8 | `LIGHTLY_DAMPED` | 20 | 0.474 | 0.397 | +0.004 | 5.6e-17 |
| energy | energy_owid_usa | 60 | 8 | `LIGHTLY_DAMPED` | 30 | 0.483 | 0.381 | +0.006 | 1.1e-16 |
| energy | energy_owid_uzb | 40 | 8 | `OVERDAMPED_EXTREME` | 19 | 0.500 | 1.081 | -0.030 | 1.1e-16 |
| energy | energy_owid_ven | 58 | 8 | `LIGHTLY_DAMPED` | 20 | 0.643 | 0.896 | +0.017 | 5.6e-17 |
| energy | energy_owid_vnm | 44 | 8 | `OVERDAMPED_EXTREME` | 26 | 0.381 | 3.198 | -0.011 | 1.1e-16 |
| energy | energy_owid_zaf | 54 | 8 | `OVERDAMPED_EXTREME` | 27 | 0.481 | 2.305 | -0.002 | 1.1e-16 |
| esa-planck | esa_planck_cosmic | 17 | 5 | `LIGHTLY_DAMPED` | 0 | 1.000 | 6.455 | +0.002 | 1.1e-16 |
| financial | financial_sp500_sectors | 252 | 10 | `CRITICALLY_DAMPED` | 226 | 0.096 | 0.030 | +0.003 | 1.1e-16 |
| geochemistry | geochem_ball_age | 10 | 10 | `LIGHTLY_DAMPED` | 6 | 0.250 | 0.161 | +0.097 | 1.7e-16 |
| geochemistry | geochem_ball_region | 95 | 10 | `MODERATELY_DAMPED` | 58 | 0.376 | 0.565 | -0.000 | 1.1e-16 |
| geochemistry | geochem_ball_tas | 15 | 10 | `OVERDAMPED_EXTREME` | 6 | 0.538 | 0.725 | -0.056 | 1.1e-16 |
| geochemistry | geochem_qin_cpx | 30 | 9 | `MODERATELY_DAMPED` | 21 | 0.250 | 0.370 | -0.016 | 1.1e-16 |
| geochemistry | geochem_stracke_morb | 5 | 10 | `CRITICALLY_DAMPED` | 3 | 0.000 | 0.000 | +0.000 | 1.1e-16 |
| geochemistry | geochem_stracke_oib | 15 | 10 | `MODERATELY_DAMPED` | 8 | 0.385 | 0.329 | -0.008 | 1.1e-16 |
| geochemistry | geochem_tappe_kim1 | 8 | 10 | `MODERATELY_DAMPED` | 4 | 0.333 | 0.549 | +0.234 | 5.6e-17 |
| iiasa | iiasa_ngfs | 31 | 7 | `MODERATELY_DAMPED` | 1 | 0.966 | 0.580 | -0.000 | 5.6e-17 |
| nuclear | nuclear_semf | 76 | 5 | `LIGHTLY_DAMPED` | 5 | 0.932 | 0.858 | +0.001 | 1.1e-16 |
| urban | urban_markham_budget | 15 | 8 | `MODERATELY_DAMPED` | 0 | 1.000 | 0.285 | -0.001 | 2.8e-17 |
| world_bank_fao | fao_credit_to_agriculture | 28 | 10 | `LIGHTLY_DAMPED` | 20 | 0.231 | 4.558 | +0.061 | 5.6e-17 |
| world_bank_fao | fao_value_added_aff | 55 | 10 | `MODERATELY_DAMPED` | 33 | 0.377 | 0.689 | -0.023 | 2.2e-16 |
| world_bank_fao | fao_value_added_agriculture | 15 | 10 | `OVERDAMPED_EXTREME` | 9 | 0.308 | 3.463 | -0.053 | 1.7e-16 |
| world_bank_fao | fao_value_added_food_mfg | (status: CNQ_FAILED) | | | | | | | |

## Determinism + numerical anchors

- **M² = I metric involution verified at IEEE floor (< 10⁻¹⁰) on 100 of 100 successful runs.** Worst residual across the corpus: **3.300e-13**.
- **Engine independence (push #32):** Each dataset produces two unrelated SHA-256 fingerprints — `cnt_content_sha256` and `cnq_content_sha256`. The fingerprints are independent by design; their non-identity is a feature, not a discrepancy.
- **CRD-1.0:** This master report compares heterogeneous datasets across domains (different T, different D, different units). CRD-1.0 governs *intra-domain* multi-carrier comparisons (e.g., the 8-country EMBER corpus is run under CRD-1.0 coherent policy in `papers/codawork2026/conference_2026_06/`). Cross-domain comparisons are inherently heterogeneous and shown as-is.

## IR class distribution across the corpus

| IR class | count | datasets |
|---|---|---|
| `CRITICALLY_DAMPED` | 2 | geochem_stracke_morb, financial_sp500_sectors |
| `D2_DEGENERATE` | 1 | commodities_gold_silver |
| `LIGHTLY_DAMPED` | 54 | energy_ember_chn, energy_ember_ind, energy_ember_jpn, energy_ember_wld, energy_ember_combined_panel + 49 more |
| `MODERATELY_DAMPED` | 17 | energy_ember_fra, backblaze_fleet, chemistry_chemixhub_oxide, iiasa_ngfs, urban_markham_budget + 12 more |
| `OVERDAMPED_EXTREME` | 26 | energy_ember_usa, energy_ember_deu, energy_ember_gbr, energy_owid_are, energy_owid_aus + 21 more |

The IR class taxonomy describes the damping signature of each compositional trajectory — from `OVERDAMPED_EXTREME` (snap-to-attractor) through `LIGHTLY_DAMPED` to `LIMIT_CYCLE_P2` (the universal compositional invariance signature). Domain-domain comparisons in this column are scientifically meaningful: they reveal which compositional systems are dynamically locked, which are cycling, and which are diffusive.

## Per-domain reports

- **`backblaze`** (1 datasets) — see [`per_domain/backblaze/DOMAIN_SUMMARY.md`](per_domain/backblaze/DOMAIN_SUMMARY.md)
- **`chemistry`** (1 datasets) — see [`per_domain/chemistry/DOMAIN_SUMMARY.md`](per_domain/chemistry/DOMAIN_SUMMARY.md)
- **`commodities`** (1 datasets) — see [`per_domain/commodities/DOMAIN_SUMMARY.md`](per_domain/commodities/DOMAIN_SUMMARY.md)
- **`energy`** (82 datasets) — see [`per_domain/energy/DOMAIN_SUMMARY.md`](per_domain/energy/DOMAIN_SUMMARY.md)
- **`esa-planck`** (1 datasets) — see [`per_domain/esa-planck/DOMAIN_SUMMARY.md`](per_domain/esa-planck/DOMAIN_SUMMARY.md)
- **`financial`** (1 datasets) — see [`per_domain/financial/DOMAIN_SUMMARY.md`](per_domain/financial/DOMAIN_SUMMARY.md)
- **`geochemistry`** (7 datasets) — see [`per_domain/geochemistry/DOMAIN_SUMMARY.md`](per_domain/geochemistry/DOMAIN_SUMMARY.md)
- **`iiasa`** (1 datasets) — see [`per_domain/iiasa/DOMAIN_SUMMARY.md`](per_domain/iiasa/DOMAIN_SUMMARY.md)
- **`nuclear`** (1 datasets) — see [`per_domain/nuclear/DOMAIN_SUMMARY.md`](per_domain/nuclear/DOMAIN_SUMMARY.md)
- **`urban`** (1 datasets) — see [`per_domain/urban/DOMAIN_SUMMARY.md`](per_domain/urban/DOMAIN_SUMMARY.md)
- **`world_bank_fao`** (4 datasets) — see [`per_domain/world_bank_fao/DOMAIN_SUMMARY.md`](per_domain/world_bank_fao/DOMAIN_SUMMARY.md)

## Anomalies and findings of interest

- **esa_planck_cosmic** has near-perfect helmsman stability (1.000) — monotone or near-monotone compositional trajectory.
- **financial_sp500_sectors** has unusually high flip density (226 flips in T=252) — chaotic or noisy dominant-axis structure.
- **iiasa_ngfs** has near-perfect helmsman stability (0.966) — monotone or near-monotone compositional trajectory.
- **urban_markham_budget** has near-perfect helmsman stability (1.000) — monotone or near-monotone compositional trajectory.
- **energy_owid_col** has unusually high flip density (43 flips in T=60) — chaotic or noisy dominant-axis structure.
- **fao_credit_to_agriculture** has unusually high flip density (20 flips in T=28) — chaotic or noisy dominant-axis structure.
- **fao_value_added_food_mfg** failed: `CNQ_FAILED` — ValueError: Out of range float values are not JSON compliant

---

*Generated by `experiments/2026-05-10_full-corpus-validation/run_full_corpus.py`.*