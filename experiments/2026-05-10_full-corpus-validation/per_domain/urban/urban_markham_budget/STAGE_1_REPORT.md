# Stage 1 Report (pure CoDa) — urban_markham_budget

**Domain:** urban
**Description:** City of Markham (Ontario) operating budget composition, fiscal years 2011-2025. T = 15 fiscal years, D = 8 budget category carriers (Operations & Asset Mgmt, Public Safety, Planning & Building, Recreation & Culture, Library & Heritage, Engineering & Capital, Corporate Services, Council & Administration).
**Citation / source:** City of Markham annual budget reports (compiled from public budget documents)

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:05Z
**cnt_content_sha256:** `27f20ce2d5611f695825e61666f9569de52501cc3273abdb8b55679d2e409e1e`

## Input

- Source CSV: `markham_budget_input.csv`
- Source SHA-256: `dff512242fcb4dac...`
- Records (T): **15**
- Carriers (D): **8**
- Carriers: Operations & Asset Mgmt, Public Safety, Planning & Building, Recreation & Culture, Library & Heritage, Engineering & Capital, Corporate Services, Council & Administration
- Closed-data SHA-256: `669410b20de65a65...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | 2011 | 1.9204 | 1.5391 | — |
| 1 | 2012 | 1.9192 | 1.5580 | 0.0702 |
| 2 | 2013 | 1.9175 | 1.5800 | 0.0706 |
| 3 | 2014 | 1.9152 | 1.6050 | 0.0713 |
| 4 | 2015 | 1.9123 | 1.6330 | 0.0723 |
| ... | ... | ... | ... | ... |
| 12 | 2023 | 1.8683 | 1.9810 | 0.0953 |
| 13 | 2024 | 1.8599 | 2.0448 | 0.1017 |
| 14 | 2025 | 1.8507 | 2.1155 | 0.1097 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Public Safety | Engineering & Capital | +1.0000 | 39.9° | no |
| Library & Heritage | Council & Administration | +0.9990 | 0.5° | YES |
| Planning & Building | Engineering & Capital | +0.9975 | 342.9° | no |
| Public Safety | Planning & Building | +0.9968 | 32.4° | no |
| Corporate Services | Council & Administration | +0.9901 | 40.3° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Library & Heritage | Engineering & Capital | -0.9964 | 357.3° | no |
| Public Safety | Library & Heritage | -0.9971 | 19.1° | no |
| Engineering & Capital | Council & Administration | -0.9992 | 25.0° | no |
| Public Safety | Council & Administration | -0.9995 | 16.6° | no |
| Planning & Building | Corporate Services | -0.9995 | 340.0° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 28 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Operations & Asset Mgmt | Public Safety | 1.052 | 1.112 | 0.303 | 0.802 |
| Operations & Asset Mgmt | Planning & Building | 1.052 | 1.112 | -0.141 | 0.104 |
| Operations & Asset Mgmt | Recreation & Culture | 1.052 | 1.112 | 0.225 | 0.246 |
| Operations & Asset Mgmt | Library & Heritage | 1.052 | 1.112 | -0.807 | -0.631 |
| Operations & Asset Mgmt | Engineering & Capital | 1.052 | 1.112 | -0.079 | 0.380 |
| Operations & Asset Mgmt | Corporate Services | 1.052 | 1.112 | -0.762 | 0.071 |
| Operations & Asset Mgmt | Council & Administration | 1.052 | 1.112 | -1.072 | -0.824 |
| Public Safety | Planning & Building | 0.303 | 0.802 | -0.141 | 0.104 |
| Public Safety | Recreation & Culture | 0.303 | 0.802 | 0.225 | 0.246 |
| Public Safety | Library & Heritage | 0.303 | 0.802 | -0.807 | -0.631 |
| ... (18 more) | | | | | |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*