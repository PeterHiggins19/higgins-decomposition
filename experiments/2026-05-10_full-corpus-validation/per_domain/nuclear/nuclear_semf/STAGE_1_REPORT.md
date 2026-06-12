# Stage 1 Report (pure CoDa) — nuclear_semf

**Domain:** nuclear
**Description:** Semi-empirical mass formula (SEMF) component decomposition across the valley of stability. T = 76 nuclides (light to heavy), D = 5 SEMF term carriers (Volume, Surface, Coulomb, Asymmetry, Pairing). The 'time' axis is nuclide ordering by Z+A; each row is one (Z, A) pair.
**Citation / source:** AME2020 nuclear masses (Wang et al. 2021); SEMF terms per Weizsäcker formula

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:06Z
**cnt_content_sha256:** `61cd5824a643a0df92c590ff65d0e36ba52beb92ed3f35cb9a83921f5d169a8c`

## Input

- Source CSV: `nuclear_semf_input.csv`
- Source SHA-256: `eaeb4d01449a782e...`
- Records (T): **76**
- Carriers (D): **5**
- Carriers: Volume, Surface, Coulomb, Asymmetry, Pairing
- Closed-data SHA-256: `e35927c38c561f13...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | Z3_A7 | 0.8889 | 3.6471 | — |
| 1 | Z4_A9 | 0.8540 | 3.7827 | 0.6758 |
| 2 | Z5_A11 | 0.8341 | 3.9798 | 0.5099 |
| 3 | Z7_A15 | 0.8149 | 4.3882 | 0.7561 |
| 4 | Z9_A19 | 0.8080 | 4.7569 | 0.5590 |
| ... | ... | ... | ... | ... |
| 73 | Z80_A196 | 0.9501 | 6.4052 | 0.1456 |
| 74 | Z81_A203 | 0.9619 | 6.4415 | 0.1931 |
| 75 | Z82_A204 | 0.9589 | 6.4513 | 0.0582 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Surface | Pairing | +0.9389 | 46.8° | no |
| Volume | Coulomb | +0.7885 | 64.0° | no |
| Coulomb | Asymmetry | +0.6387 | 144.8° | no |
| Volume | Asymmetry | +0.0452 | 48.8° | no |
| Volume | Surface | -0.1843 | 14.7° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Volume | Pairing | -0.5113 | 38.0° | no |
| Surface | Coulomb | -0.7444 | 95.0° | no |
| Asymmetry | Pairing | -0.8802 | 54.8° | no |
| Coulomb | Pairing | -0.9270 | 75.1° | no |
| Surface | Asymmetry | -0.9885 | 61.0° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 10 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Volume | Surface | 2.234 | 3.061 | 1.183 | 2.039 |
| Volume | Coulomb | 2.234 | 3.061 | -1.666 | 1.468 |
| Volume | Asymmetry | 2.234 | 3.061 | -3.398 | 0.041 |
| Volume | Pairing | 2.234 | 3.061 | -5.481 | -1.027 |
| Surface | Coulomb | 1.183 | 2.039 | -1.666 | 1.468 |
| Surface | Asymmetry | 1.183 | 2.039 | -3.398 | 0.041 |
| Surface | Pairing | 1.183 | 2.039 | -5.481 | -1.027 |
| Coulomb | Asymmetry | -1.666 | 1.468 | -3.398 | 0.041 |
| Coulomb | Pairing | -1.666 | 1.468 | -5.481 | -1.027 |
| Asymmetry | Pairing | -3.398 | 0.041 | -5.481 | -1.027 |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*