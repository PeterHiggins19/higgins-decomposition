# Hs-05 Geochemistry — Region-Binned CNT/HCI Extension

## Date: 2026-05-05

## Status

CNT pipeline COMPLETE. Stage 3 day-triad analysis runs in 0.36 s on the
binned dataset (was timed out indefinitely on the raw N = 26,266).

---

## Why Region Binning

The Stage 3 `triadic_day_analysis` in `HCI/hci_stage3.py` enumerates all
C(N, 3) day-combinations. For the raw Ball intraplate-volcanic dataset
(N = 26,266 oxide-complete samples), this is 3.02 × 10¹² triads — about
2,500 hours of pure-Python compute and ~750 TB of result memory. The basic
12-step Hˢ pipeline runs fine on the same data (Hs-05 NATURAL, bowl, R² = 0.53,
1/(2π) at δ = 5.9 × 10⁻⁷); it is only the new four-program CNT pipeline
that needs aggregation.

The Ball samples are not naturally temporal at the row level — they are
independent rock samples from intraplate volcanic provinces worldwide.
Stage 3's "day" abstraction needs to map onto something with geological
meaning. Region (114 distinct values in the raw data, 95 after filtering
n ≥ 10) preserves geographic structure and lets the simplex tell a clean
story across continental and oceanic provinces.

## Method

1. Read `DATA/Geochemistry/2022-3-RY3BRK_Ball_data.csv` (Ball 2022, CC-BY 4.0,
   DOI 10.25625/RY3BRK, 27,777 data rows).
2. Keep rows with non-empty Region and all 10 oxides positive: 25,449 samples.
3. Drop regions with n < 10 samples: 95 regions kept covering 25,382
   samples (99.7 % of clean data).
4. Compute the geometric (Aitchison) barycenter per region after closing
   each sample to the simplex.
5. Run the four-program CNT pipeline on the 95 × D=10 barycenter table.

Reproducibility: `bin_by_region.py` (this folder).

## Results

### Computational

| Stage              | N=26,266 (raw)              | N=95 (region-binned) |
|--------------------|-----------------------------|----------------------|
| 12-step pipeline   | OK (HVLD bowl, R²=0.53)     | not run              |
| CNT tensor engine  | not attempted               | 0.27 s               |
| CNT analysis       | C(N,3)=3.02e12 → timeout    | 0.36 s, 138,415 triads |
| Depth sounder      | not attempted               | 0.29 s               |

### Compositional

CNT tensor engine output:
- Hs range:              0.2418 – 0.4096
- Max Aitchison distance: 6.79 HLR
- Total arc length:      113.5 HLR (across 95 regions)
- Mean ω:                12.99 deg/step
- Dominant helmsman:     **K₂O** at 43 / 94 transitions
- Locked pairs:          1
- Bearing reversals:     406

Stage 3 (the part that timed out before):
- 95 section triads computed
- 500 temporal triads ranked by metric area (max area = 7.68)
- **35 regime boundaries** detected in the metric trajectory

Bridges:
- **Dynamical**: NEUTRAL system, DIVERGENT_TRAJECTORY attractor,
  recurrence rate 0.04. The geographic walk across provinces is
  non-recurrent — each region is structurally distinct.
- **Control**: UNSTABLE (spectral bound 8.07), POOR model fit
  (mean residual 0.84). Expected — this is not a controlled time
  series.
- **Information**: NET_DISPERSING (entropy increases over the path),
  highest mutual-information pair = **SiO₂ / Al₂O₃ at MI = 0.879**
  (the standard felsic-crystallization differentiation pair —
  petrologically correct).

### Depth Sounding (M² = I, period-2 attractor)

- M² = I residual: 9.8 × 10⁻¹⁸ — verified at IEEE 754 floor.
- **Curvature tower depth δ = 14**, terminates LIMIT_CYCLE_P2.
  Period-2 attractor confirmed at residual 4.97 × 10⁻³ (below 1 % target).
- **Energy tower depth = 46**, terminates LIMIT_CYCLE_P1 (fixed point
  at Hs = 0.307, residual 0.26 %). This is anomalous: most tested systems
  (Hs-25 cosmic, Japan EMBER, etc.) show energy depth = 1. Geochemistry
  has 46 levels of productive energy-tower structure. **Worth flagging
  as a candidate finding for the math handbook.**

Period-2 attractor values:
- c_even = 0.2532 (low entropy — concentrated)
- c_odd  = 0.3712 (higher entropy — distributed)
- Amplitude **A = 0.118** → LIGHTLY_DAMPED in Ch 23.3 classification
  (alongside India, France, World).

### Lyapunov Stability

- λ = **−0.580** (asymptotically stable, period-2 attracting)
- Mean contraction ratio: **1.60 — Banach contraction NOT satisfied**
  (mean ratio > 1)
- **First contraction ratio = 13.24** — extreme initial overshoot

This is a clean illustration of the non-uniform contraction case
discussed in Math Handbook Ch 24.5: "individual early steps expand
before later steps contract; their overall trajectories still converge
(negative λ), meaning the contraction condition holds asymptotically
but not uniformly." Geochemistry joins phosphoric acid, citric acid,
nuclear SEMF, and conversation drift as a sixth documented example
of this regime.

Where this lands among the 18 systems in Ch 24.4:

| System         | λ      | Notes                              |
|----------------|--------|------------------------------------|
| Backblaze      | −4.54  | most stable                        |
| Germany        | −2.36  |                                    |
| Cosmic / Japan | −1.37  |                                    |
| China          | −1.03  |                                    |
| Planck         | −0.85  |                                    |
| USA            | −0.64  |                                    |
| **Geochem**    | **−0.58**  | **this run, n = 95 regions**   |
| Citric         | −0.56  |                                    |
| Conv. Drift    | −0.39  |                                    |
| Nuclear SEMF   | −0.33  | least negative (still converging)  |
| Mean (18)      | −1.12  |                                    |

### Helmsman Lineage in the Curvature Tower

The carrier steering each recursion level migrates with petrological
significance:

| Level   | Helmsman | Geological meaning                  |
|---------|----------|--------------------------------------|
| L1–L3   | K₂O      | LILE (large ion lithophile), fertility / metasomatism signal |
| L4      | MgO      | Mafic crossover                     |
| L5–L10  | Na₂O     | Alkali differentiation              |
| L11–L14 | SiO₂     | Felsic / silica differentiation     |

This is not a trivial relabelling — at each level the curvature
composition is reconstructed from the steering metric tensor, and the
dominant carrier shifts along a recognisable petrological gradient
(LILE → mafic transition → alkalis → felsic). The recursion levels
are reading distinct strata of the differentiation series.

## Findings to Promote

1. **Method**: Region-binning unblocks the four-program CNT pipeline
   for non-temporal compositional datasets. Pattern is generalisable
   to any high-N dataset where samples carry a categorical covariate.
   Recommend adding a `--bin-by COLUMN` flag to `cnt_tensor_engine.py`.

2. **Empirical**: The period-2 attractor universality survey (Math
   Handbook Ch 23.5) extends from 7 to 8 domains with this run.
   Geochemistry: A = 0.118, δ = 14, λ = −0.58, LIGHTLY_DAMPED.

3. **Empirical**: First documented system with energy tower depth ≫ 1
   (δ_energy = 46, period-1). All previously tested systems show
   energy depth = 1. The asymmetry δ_energy / δ_curvature ≈ 3.3 is
   reversed from the cosmic case (δ_energy = 1, δ_curvature = 9).
   This is a candidate finding worth probing across other high-N
   datasets.

4. **Empirical**: Helmsman lineage K₂O → MgO → Na₂O → SiO₂ across
   the 14-level curvature tower mirrors the standard intraplate
   volcanic differentiation series. Suggests the recursion is not
   merely numerical but reads physically meaningful strata.

5. **Theoretical**: Geochemistry is the sixth confirmed case of
   non-uniform contraction (Banach fails, λ < 0). The first
   contraction ratio of 13.24 is the largest initial overshoot
   recorded in the survey.

## Open Questions

1. Does Region × Alkalinity (multi-covariate cross) preserve the
   period-2 attractor with different c_even / c_odd values? Would
   be the first within-domain robustness test.
2. Energy tower depth = 46 — what makes it so deep? Is it the high
   ambient dimensionality (D=10) or the distributional shape of the
   geographic cohort?
3. Does the helmsman lineage K₂O → MgO → Na₂O → SiO₂ appear in
   alternative bin schemes (Age epochs, TAS rock type)? If yes,
   it is a property of the simplex, not the binning.

## Files Produced

In this folder:
- `bin_by_region.py` — reproducible binning script
- `ball_oxides_by_region_long.csv` — 25,382 closed samples × 12 cols
- `ball_oxides_by_region_barycenters.csv` — 95 region barycenters
- `ball_oxides_by_region_summary.json` — per-region metadata
- `ball_regions_cnt.json` — full CNT tensor output (2.0 MB)
- `ball_regions_analysis.json` — Stage 1/2/3 + bridges (607 KB)
- `ball_regions_depth.json` — depth sounder, M² proof, towers (49 KB)
- `ball_regions_lyapunov.json` — λ, contraction ratios, IR class
- `JOURNAL.md` — this file

---

*The instrument reads. The expert decides. The loop stays open.*
