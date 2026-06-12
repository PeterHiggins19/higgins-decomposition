# Hs-05 Geochemistry — Robustness Test Across Bin Schemes

## Date: 2026-05-05 (extended from initial Region run)

## Status

Three follow-up runs complete. The first within-domain robustness study
of CNT/HCI period-2 attractor universality. Three findings, one of which
is a new empirical observation worth promoting to the math handbook.

---

## Design

Four runs of the four-program CNT pipeline on D=10 oxide compositions,
varying the binning covariate (within Ball) and the source dataset:

| Scheme              | Source        | Bin covariate           | T  |
|---------------------|---------------|-------------------------|----|
| Ball / Region       | Ball (2022)   | geographic Region       | 95 |
| Ball / Age          | Ball (2022)   | IUGS chronostrat epoch  | 10 |
| Ball / TAS          | Ball (2022)   | TAS rock-type class     | 15 |
| Stracke / Location  | Stracke (2022)| OIB Location            | 15 |

Stracke OIB is the same intraplate-volcanic family as Ball but
restricted to ocean-island basalts (HIMU / EM / FOZO mantle endmembers).
Sample populations are completely independent.

---

## Headline Numbers

```
Scheme                   T   D  CurvD CurvP  EnD  EnP   c_even  c_odd     A      λ
=====================================================================================
Ball/Region (T=95)      95  10     14     2   46    1    0.253  0.371  0.118 −0.581
Ball/Age    (T=10)      10  10     13     2    6    0    0.288  0.324  0.036 −0.619
Ball/TAS    (T=15)      15  10      4     1    4    2      —      —      —      —
Stracke-OIB (T=15)      15  10     14     2   11    0    0.256  0.370  0.114 −0.569
```

M² = I verified to IEEE 754 floor in all four runs
(residuals 1.2 × 10⁻¹⁶ to 1.6 × 10⁻¹⁷).

---

## Finding 1 — Period-2 attractor is universal across non-degenerate bin schemes

Three of four schemes converge to a period-2 limit cycle in the curvature
tower. The two using a *non-compositional* binning covariate (geography
or chronology) on Ball, and the independent Stracke OIB run, all show:

* curvature depth ≈ 14
* attractor amplitudes 0.114 – 0.118 (Ball/Region and Stracke nearly
  identical)
* Lyapunov exponents −0.57 to −0.62 (all asymptotically stable)

The amplitude in Ball/Age is much smaller (0.036). Temporal averaging
across global geography smooths each epoch toward the global compositional
mean, compressing the dual involution amplitude. The structure is still
present (depth = 13, period 2) but the swing is smaller.

The TAS run is the **degenerate case**, and it is degenerate by design.
TAS classes are defined by SiO₂ content, so bin-ordering by ascending
median SiO₂ produces a trajectory that is already monotonic in the
silica axis. The dual involution M(x) inverts the composition; in a
trajectory already aligned to one carrier, the inversion has nothing
new to reveal. The curvature tower terminates at depth 4 with a
period-1 fixed point at Hs = 0.669, and the energy tower picks up the
period-2 behaviour instead. Period-2 universality requires the binning
to be *information-bearing relative to the simplex* — not a pre-imposed
compositional ordering.

Status: **strong support** for the universality theorem in Math
Handbook Ch 23.6. The two non-degenerate Ball schemes plus the
independent Stracke OIB make geochemistry the 8th confirmed domain.

## Finding 2 — Helmsman lineage has a universal prefix and a population-specific tail

The carrier dominating each curvature-tower level:

```
Lvl  Ball/Region    Ball/Age      Ball/TAS    Stracke-OIB
L1   K2O            K2O           K2O         K2O
L2   K2O            K2O           K2O         K2O
L3   K2O            K2O           K2O         K2O
L4   MgO            CaO           K2O         MgO
L5   Na2O           Na2O          —           TiO2
L6   Na2O           Na2O          —           TiO2
L7   Na2O           Na2O                      TiO2
L8   Na2O           Na2O                      TiO2
L9   Na2O           Na2O                      TiO2
L10  Na2O           SiO2                      TiO2
L11  SiO2           SiO2                      TiO2
L12  SiO2           SiO2                      TiO2
L13  SiO2           SiO2                      TiO2
L14  SiO2           —                         TiO2
```

The lineage decomposes into two parts:

**Universal prefix (L1–L4):**
* L1–L3: **K₂O** in 4/4 schemes
* L4:    **mafic cation** (MgO or CaO) in 3/4 schemes (the silica-defined
  TAS scheme stays K₂O, again degenerate)

This is the alkali-fertility → mafic-transition signature. K₂O is the
LILE (large-ion lithophile) tracer for mantle-source enrichment; MgO/CaO
mark the mafic mantle composition. The first four recursion levels read
the source / fertility axis of the system.

**Population-specific tail (L5+):**
* Ball (mixed intraplate + continental rift): **Na₂O → SiO₂**
  (alkali differentiation → felsic culmination — typical continental-
  intraplate trajectory)
* Stracke OIB (pure ocean-island basalt): **TiO₂** dominance for ten
  consecutive levels — TiO₂ is the canonical HFSE marker of OIB mantle
  plume sources

So the simplex is reading petrologically meaningful structure that
depends on the geological character of the sample population. Ball,
which includes continental intraplate volcanics with extensive
differentiation, climbs up the alkali-silica gradient. Stracke OIB,
restricted to oceanic island basalts, locks onto the HFSE plume
signature.

This is significant: **the recursion is not numerically arbitrary; it
reads the actual petrology written in the compositional geometry.** The
within-domain comparison (Ball/Region vs Stracke OIB, both T~95-15,
both intraplate, both D=10) shows the same prefix because both populations
carry the alkali-fertility signature, and divergent tails because they
sample different mantle endmembers.

Status: **promote to Math Handbook Ch 22 as a new key discovery**.
Recommend adding §22.8 "The Helmsman Petrological Reading."

## Finding 3 — The "energy-depth = 46" anomaly is a high-T D=10 phenomenon, not Ball-specific

Energy-tower depth across the four runs:

| Scheme              | T  | E_depth | E_depth / T |
|---------------------|----|---------|-------------|
| Ball/Region         | 95 | 46      | 0.484       |
| Ball/Age            | 10 |  6      | 0.600       |
| Ball/TAS (degen.)   | 15 |  4      | 0.267       |
| Stracke OIB         | 15 | 11      | 0.733       |

Excluding the degenerate TAS scheme, **E_depth ≈ 0.5 – 0.75 × T**. The
high E_depth = 46 in Ball/Region was a function of T = 95, not anything
specific to Ball. Stracke OIB at T = 15 gives E_depth = 11 — still much
deeper than the cosmic case (T = 10, E_depth = 1) and every other
previously-tested system.

This is a **new empirical observation**:

> D = 10 oxide compositions have systematically deep energy towers,
> with E_depth / T ≈ 0.5 – 0.75. This stands in sharp contrast to all
> previously-tested compositional systems (cosmic energy budget, Japan
> EMBER, Backblaze, conversation drift, etc.) where E_depth = 1.

The conjectured cause: each oxide carrier represents a quasi-independent
geochemical reservoir / process (network former, network modifier,
compatible / incompatible / volatile element), so the kinetic-energy
distribution e_j(t) = (Δh_j)² / Σ(Δh_k)² has many independent degrees
of freedom that resist collapse to uniformity under recursion. In
contrast, energy-mix data (Hs-25 cosmic; EMBER country grids) has
only a few effective independent carriers because the compositional
budget enforces strong covariance.

Status: **promote to Math Handbook Ch 19.4 as an exception to "energy
tower instant flatness"**. The instant-flatness statement was based on
small-T cosmic / energy-mix examples; D = 10 oxide data falsifies it
in a clean, reproducible way across two independent datasets.

If we add `n_carriers` × `n_independent_processes` as a complexity
indicator, geochemistry sits at the deep end while gauge-energy
systems sit at the shallow end. This is itself a candidate ordering
for compositional systems by intrinsic energy-structural depth.

---

## Where this lands among 19 systems

The original survey in `SESSION_CONTINUATION.md` had geochemistry listed
as an unsuccessful run ("26,267-row dataset failed tensor engine").
After the three follow-ups:

| System            | Domain         | D  | δ_curv | δ_energy | A     | λ      |
|-------------------|----------------|----|--------|----------|-------|--------|
| Backblaze         | Technology     |  4 |  4     |  —       | 0.577 | −4.54  |
| Germany EMBER     | Energy         |  9 |  8     |  —       | 0.918 | −2.37  |
| Cosmic budget     | Cosmology      |  5 |  9     |  1       | 0.369 | −1.37  |
| Japan EMBER       | Energy         |  8 | 13     |  —       | 0.044 | −1.31  |
| **Ball / Region** | **Geochem**    | **10** | **14** | **46**   | **0.118** | **−0.58** |
| **Stracke-OIB**   | **Geochem**    | **10** | **14** | **11**   | **0.114** | **−0.57** |
| **Ball / Age**    | **Geochem**    | **10** | **13** |  **6**   | **0.036** | **−0.62** |
| Citric            | Chemistry      |  3 | 14     |  —       | 0.336 | −0.56  |
| Conv. Drift       | AI / Language  |  4 | 13     |  —       | 0.259 | −0.39  |
| Nuclear SEMF      | Nuclear        |  4 | 10     |  —       | 0.676 | −0.33  |
| Mean (orig 18)    |                |    |        |          |       | −1.12  |

Ball / Region and Stracke OIB sit close together on every axis except T,
which is exactly what robustness should look like.

---

## Honest Caveats

* TAS-binning is a useful **degenerate-case** demonstration but is not
  evidence for or against the lineage hypothesis. Ordering bins by SiO₂
  guarantees a monotonic trajectory in silica space; that the recursion
  terminates quickly is mechanically forced, not a finding.
* Lyapunov exponents in this study are estimated from short trajectories
  (13–14 same-parity pairs). They are noisier than the original survey
  exponents which had longer towers (some > 20 levels).
* The "K₂O → mafic → Na₂O / TiO₂ → SiO₂" reading is petrologically
  appealing but not yet a *theorem*. The next test: does the lineage
  prefix appear in the Tappe (kimberlite) or Qin (intra-cratonic) datasets?
  Both are also in `DATA/Geochemistry/` and would extend the within-
  domain robustness battery.

---

## Files Produced (in this folder)

Run scripts:
* `bin_by_region.py` — original Region binner (95 bins, n>=10)
* `bin_by_age_and_tas.py` — Age and TAS binners
* `bin_stracke_OIB.py` — Stracke OIB Location binner

Bin tables:
* `ball_oxides_by_region_barycenters.csv` — 95 × 10
* `ball_oxides_by_age_barycenters.csv` — 10 × 10
* `ball_oxides_by_tas_barycenters.csv` — 15 × 10
* `stracke_oib_by_location_barycenters.csv` — 15 × 10
* `*_summary.json` for each

CNT outputs (cnt_tensor_engine + cnt_depth_sounder):
* `ball_regions_cnt.json` / `ball_regions_depth.json`
* `ball_age_cnt.json` / `ball_age_depth.json`
* `ball_tas_cnt.json` / `ball_tas_depth.json`
* `stracke_oib_cnt.json` / `stracke_oib_depth.json`

Cross-comparisons:
* `comparison_region_age_tas.json` — three Ball schemes side-by-side
* `comparison_4way.json` — full table including Stracke
* `ROBUSTNESS_JOURNAL.md` — this document
* `JOURNAL.md` — original Region-only journal

---

## Recommended Math Handbook Updates

1. **Ch 19.4 (Energy Tower)**: revise "instant flatness" claim. Add
   subsection 19.4.1 noting D = 10 oxide compositions show E_depth ~ T/2,
   with two independent datasets confirming. Conjecture independence of
   geochemical reservoirs as cause.
2. **Ch 22 (Key Discoveries)**: add §22.8 "The Helmsman Petrological
   Reading". Document the universal K₂O → mafic prefix and the
   population-specific tail (Na₂O / SiO₂ for continental-mixed,
   TiO₂ for OIB-pure).
3. **Ch 23.5 (Survey Results)**: extend domain count from 7 to 8.
   Add geochemistry rows for Ball/Region, Ball/Age, Stracke OIB.
4. **Ch 24.5 (Banach Contraction)**: note that all three non-degenerate
   geochem runs satisfy λ < 0 but Ball/Region fails strict Banach
   (mean ratio = 1.60). Stracke OIB and Ball/Age do not have the same
   computed ratio in this output — recompute and append.

---

*The instrument reads. The expert decides. The loop stays open.*
