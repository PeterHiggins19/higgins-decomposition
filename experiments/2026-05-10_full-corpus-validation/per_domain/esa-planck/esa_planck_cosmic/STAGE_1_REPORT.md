# Stage 1 Report (pure CoDa) — esa_planck_cosmic

**Domain:** esa-planck
**Description:** ESA Planck cosmological energy-density composition vs redshift. T = 18 redshift bins (z = 0.0 to z = 1100), D = 5 species carriers (Dark Energy, Cold Dark Matter, Baryons, Photons, Neutrinos).
**Citation / source:** Planck 2018 cosmological parameters (Planck Collaboration); composition computed at each redshift bin per standard LCDM evolution equations

**Engine:** HCI-CNT v3.0.0 (schema 3.0.0)
**Reading:** *standard CoDa community vocabulary only — closure, CLR, ILR, variation matrix, sub-compositional pair coherence.*
**Generated:** 2026-05-10T13:58:04Z
**cnt_content_sha256:** `d8aa00837caa13b0d5916c0f6f07d07c70e4691ec0e4b602f84d48fd2680328b`

## Input

- Source CSV: `esa_planck_cosmic_input.csv`
- Source SHA-256: `040d0e79dacf1ab6...`
- Records (T): **17**
- Carriers (D): **5**
- Carriers: Dark Energy, Cold Dark Matter, Baryons, Photons, Neutrinos
- Closed-data SHA-256: `8e24713b9a2d916e...`

## CoDa-standard per-step view

Per-timestep CoDa quantities. Columns: Shannon entropy (carrier diversity at that step); Aitchison norm (composition's distance from the simplex barycenter, ‖h‖_A); step-to-step Aitchison distance (how far the composition moved relative to the previous step).

| t | label | Shannon H | Aitchison ‖h‖ | step Δ |
|---|---|---|---|---|
| 0 | z=0.0 | 0.7552 | 9.4464 | — |
| 1 | z=0.5 | 0.9373 | 8.4641 | 1.3325 |
| 2 | z=1.0 | 0.8693 | 7.8302 | 0.9454 |
| 3 | z=2.0 | 0.6791 | 7.0562 | 1.3325 |
| 4 | z=3.0 | 0.5778 | 6.6157 | 0.9454 |
| ... | ... | ... | ... | ... |
| 14 | z=1050.0 | 1.0376 | 16.7234 | 0.1602 |
| 15 | z=1080.0 | 1.0448 | 16.8097 | 0.0925 |
| 16 | z=1100.0 | 1.0494 | 16.8659 | 0.0602 |

## Variation matrix τ_ij = var(log x_i / x_j)

Aitchison's classical CoDa subcompositional coherence indicator. Small τ_ij = carriers move together (their log-ratio is stationary); large τ_ij = carriers move independently or in opposition.

### Top 5 most-coherent carrier pairs (highest Pearson r on CLR)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Photons | Neutrinos | +1.0000 | 174.2° | no |
| Cold Dark Matter | Neutrinos | +1.0000 | 87.6° | no |
| Cold Dark Matter | Photons | +1.0000 | 88.6° | no |
| Baryons | Neutrinos | +1.0000 | 113.0° | no |
| Baryons | Photons | +1.0000 | 114.9° | no |

### Top 5 most-opposed carrier pairs (lowest Pearson r)

| i | j | Pearson r | bearing spread (deg) | locked? |
|---|---|---|---|---|
| Cold Dark Matter | Baryons | +1.0000 | 5.4° | YES |
| Dark Energy | Baryons | -1.0000 | 144.5° | no |
| Dark Energy | Cold Dark Matter | -1.0000 | 123.3° | no |
| Dark Energy | Photons | -1.0000 | 354.1° | no |
| Dark Energy | Neutrinos | -1.0000 | 353.3° | no |

## Section atlas (CLR-space pair ranges)

All C(D, 2) = 10 pairwise (i, j) coordinate ranges across the trajectory.

| i | j | i_min | i_max | j_min | j_max |
|---|---|---|---|---|---|
| Dark Energy | Cold Dark Matter | -15.027 | 4.584 | 3.611 | 5.012 |
| Dark Energy | Baryons | -15.027 | 4.584 | 1.938 | 3.339 |
| Dark Energy | Photons | -15.027 | 4.584 | -4.864 | 3.541 |
| Dark Energy | Neutrinos | -15.027 | 4.584 | -5.269 | 3.135 |
| Cold Dark Matter | Baryons | 3.611 | 5.012 | 1.938 | 3.339 |
| Cold Dark Matter | Photons | 3.611 | 5.012 | -4.864 | 3.541 |
| Cold Dark Matter | Neutrinos | 3.611 | 5.012 | -5.269 | 3.135 |
| Baryons | Photons | 1.938 | 3.339 | -4.864 | 3.541 |
| Baryons | Neutrinos | 1.938 | 3.339 | -5.269 | 3.135 |
| Photons | Neutrinos | -4.864 | 3.541 | -5.269 | 3.135 |

---

*Stage 1 = pure CoDa. For the full Hˢ extension stack and CNQ v2 quaternion view, see `ADVANCED_ANALYSIS.md`.*