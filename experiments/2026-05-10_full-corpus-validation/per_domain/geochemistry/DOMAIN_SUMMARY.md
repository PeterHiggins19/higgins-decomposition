# Domain summary — geochemistry

**Datasets in this domain:** 7

## Headline diagnostics

| Dataset | Status | T | D | Termination | IR class | M²=I residual | A | ζ | flips | stability |
|---|---|---|---|---|---|---|---|---|---|---|
| geochem_stracke_morb | OK | 5 | 10 | `EXHAUSTED` | `CRITICALLY_DAMPED` | 1.11e-16 | 0.000 | +0.000 | 3 | 0.000 |
| geochem_ball_age | OK | 10 | 10 | `EXHAUSTED` | `LIGHTLY_DAMPED` | 1.67e-16 | 0.161 | +0.097 | 6 | 0.250 |
| geochem_ball_region | OK | 95 | 10 | `EXHAUSTED` | `MODERATELY_DAMPED` | 1.11e-16 | 0.565 | -0.000 | 58 | 0.376 |
| geochem_ball_tas | OK | 15 | 10 | `EXHAUSTED` | `OVERDAMPED_EXTREME` | 1.11e-16 | 0.725 | -0.056 | 6 | 0.538 |
| geochem_qin_cpx | OK | 30 | 9 | `EXHAUSTED` | `MODERATELY_DAMPED` | 1.11e-16 | 0.370 | -0.016 | 21 | 0.250 |
| geochem_stracke_oib | OK | 15 | 10 | `EXHAUSTED` | `MODERATELY_DAMPED` | 1.11e-16 | 0.329 | -0.008 | 8 | 0.385 |
| geochem_tappe_kim1 | OK | 8 | 10 | `EXHAUSTED` | `MODERATELY_DAMPED` | 5.55e-17 | 0.549 | +0.234 | 4 | 0.333 |

## Per-dataset detail

- **geochem_stracke_morb** — Stracke MORB (mid-ocean ridge basalt) major-oxide composition, by ocean basin. T = 5 locations, D = 10 oxide carriers (SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5).
  - [Stage 1 report](per_domain/geochemistry/geochem_stracke_morb/STAGE_1_REPORT.md)  ·  [Advanced analysis](per_domain/geochemistry/geochem_stracke_morb/ADVANCED_ANALYSIS.md)
- **geochem_ball_age** — Ball (2022) intraplate-volcanic database — major-oxide composition binned by IUGS chronostratigraphic age epoch (Holocene through Eocene_or_older). T = 10 epochs, D = 10 oxides (SiO2, TiO2, Al2O3, FeO, CaO, MgO, MnO, K2O, Na2O, P2O5).
  - [Stage 1 report](per_domain/geochemistry/geochem_ball_age/STAGE_1_REPORT.md)  ·  [Advanced analysis](per_domain/geochemistry/geochem_ball_age/ADVANCED_ANALYSIS.md)
- **geochem_ball_region** — Ball (2022) intraplate-volcanic database — major-oxide composition binned by geographic Region (95 regions retained at min n=10 per region). T = 95, D = 10 oxides.
  - [Stage 1 report](per_domain/geochemistry/geochem_ball_region/STAGE_1_REPORT.md)  ·  [Advanced analysis](per_domain/geochemistry/geochem_ball_region/ADVANCED_ANALYSIS.md)
- **geochem_ball_tas** — Ball (2022) intraplate-volcanic database — major-oxide composition binned by Total-Alkali-Silica (TAS, Le Bas 1986) rock-type classification. T = 15 rock types, D = 10 oxides.
  - [Stage 1 report](per_domain/geochemistry/geochem_ball_tas/STAGE_1_REPORT.md)  ·  [Advanced analysis](per_domain/geochemistry/geochem_ball_tas/ADVANCED_ANALYSIS.md)
- **geochem_qin_cpx** — Qin et al. (2024) clinopyroxene mineral spot analyses from intra-cratonic mantle xenoliths and ultramafic rocks. T = 30 top locations (>=10 spots each), D = 9 oxides (SiO2, TiO2, Al2O3, Cr2O3, FeO, CaO, MgO, MnO, Na2O — note Cr2O3 replaces K2O for clinopyroxene). Crucial test for whether the K2O-prefix in the helmsman lineage is specifically potassium or 'dominant alkali in general'.
  - [Stage 1 report](per_domain/geochemistry/geochem_qin_cpx/STAGE_1_REPORT.md)  ·  [Advanced analysis](per_domain/geochemistry/geochem_qin_cpx/ADVANCED_ANALYSIS.md)
- **geochem_stracke_oib** — Stracke (2022) ocean island basalt (OIB) major-oxide composition, binned by location (top 15 locations by sample count, including Galapagos, Iceland, Hawaii, Tristan da Cunha, etc.). T = 15, D = 10 oxides.
  - [Stage 1 report](per_domain/geochemistry/geochem_stracke_oib/STAGE_1_REPORT.md)  ·  [Advanced analysis](per_domain/geochemistry/geochem_stracke_oib/ADVANCED_ANALYSIS.md)
- **geochem_tappe_kim1** — Tappe et al. (2024) Kimberlite Group-1 bulk rock major-oxide composition, binned by country/region. T = 8 countries, D = 10 oxides. Kimberlites are intra-cratonic mantle-derived ultrapotassic rocks; K2O is typically very high (>3% on mass basis).
  - [Stage 1 report](per_domain/geochemistry/geochem_tappe_kim1/STAGE_1_REPORT.md)  ·  [Advanced analysis](per_domain/geochemistry/geochem_tappe_kim1/ADVANCED_ANALYSIS.md)
