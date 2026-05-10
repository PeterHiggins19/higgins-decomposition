# Domain summary — world_bank_fao

**Datasets in this domain:** 4

## Headline diagnostics

| Dataset | Status | T | D | Termination | IR class | M²=I residual | A | ζ | flips | stability |
|---|---|---|---|---|---|---|---|---|---|---|
| fao_credit_to_agriculture | OK | 28 | 10 | `EXHAUSTED` | `LIGHTLY_DAMPED` | 5.55e-17 | 4.558 | +0.061 | 20 | 0.231 |
| fao_value_added_aff | OK | 55 | 10 | `EXHAUSTED` | `MODERATELY_DAMPED` | 2.22e-16 | 0.689 | -0.023 | 33 | 0.377 |
| fao_value_added_agriculture | OK | 15 | 10 | `EXHAUSTED` | `OVERDAMPED_EXTREME` | 1.67e-16 | 3.463 | -0.053 | 9 | 0.308 |
| fao_value_added_food_mfg | **CNQ_FAILED** | — | — | — | — | — | — | — | — | — |

## Per-dataset detail

- **fao_credit_to_agriculture** — FAO indicator FAO_IC_23068 — Credit to Agriculture, Forestry and Fishing (USD millions). Pivoted compositional view: top-10 countries by total reporting volume, normalised so each year's row is the country-share of total recorded credit. Reveals year-by-year concentration shifts in agricultural lending.
  - [Stage 1 report](per_domain/world_bank_fao/fao_credit_to_agriculture/STAGE_1_REPORT.md)  ·  [Advanced analysis](per_domain/world_bank_fao/fao_credit_to_agriculture/ADVANCED_ANALYSIS.md)
- **fao_value_added_aff** — FAO indicator FAO_MK_22016 — Value Added in Agriculture, Forestry and Fishing. Top-10 country compositional pivot, 1970-2024 (T = 55 years).
  - [Stage 1 report](per_domain/world_bank_fao/fao_value_added_aff/STAGE_1_REPORT.md)  ·  [Advanced analysis](per_domain/world_bank_fao/fao_value_added_aff/ADVANCED_ANALYSIS.md)
- **fao_value_added_agriculture** — FAO indicator FAO_MK_22010 — Value Added (Agriculture), USD millions. Top-10 country compositional pivot. T years × D = 10 countries; each year's row sums to 1.0 (country-share of agricultural value added among the top-10 reporting nations).
  - [Stage 1 report](per_domain/world_bank_fao/fao_value_added_agriculture/STAGE_1_REPORT.md)  ·  [Advanced analysis](per_domain/world_bank_fao/fao_value_added_agriculture/ADVANCED_ANALYSIS.md)
- **fao_value_added_food_mfg** — CNQ_FAILED: ValueError: Out of range float values are not JSON compliant
