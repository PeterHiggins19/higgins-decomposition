# Hs-05 Geochemistry — Robustness Test, Extended (v2)

## Date: 2026-05-05

> **ERRATUM (added 2026-05-05 after engine 2.0.1 fix):** Finding 1
> below originally classified Ball/TAS as DEGENERATE / curv_depth=3 and
> attributed this to "TAS bins are silica-defined, so the recursion
> can't develop." That attribution is **wrong**. The same engine bug
> that produced false-positive period-1 detection on USA EMBER (see
> `experiments_v2/codawork2026/ember_usa/USA_DIAGNOSIS.md`) also
> affected Ball/TAS. With the fix in engine 2.0.1 (period-1 detection
> requires TWO consecutive level-pair convergences), Ball/TAS recovers
> to **curv_depth = 12, IR = LIGHTLY_DAMPED, A = 0.094**. This
> *strengthens* the universality finding: 5 of 5 non-Higgins-extension
> geochem schemes now show period-2 attractor (TAS no longer the lone
> degenerate exception). The "TAS is degenerate by design" reading
> below is superseded; only D=2 systems (e.g. Gold/Silver) remain
> genuinely degenerate. See `experiments_v2/INDEX.json` for the
> refreshed v2.0.2 numbers.

## Status

Six within-domain runs across four geochemical regimes plus a six-point
T-sweep on Ball/Region. **Three findings hold; two prior conjectures are
revised.** This document supersedes ROBUSTNESS_JOURNAL.md (v1).

The instrument now reads geochemistry across kimberlite, ocean-island
basalt, mantle-xenolith pyroxene, and mixed continental-intraplate volcanics.

---

## Six Runs

| Scheme              | Source        | Bin covariate     | T  | D  | Petrological regime              |
|---------------------|---------------|-------------------|----|----|----------------------------------|
| Ball / Region       | Ball 2022     | geographic Region | 95 | 10 | mixed continental + intraplate   |
| Ball / Age          | Ball 2022     | IUGS epoch        | 10 | 10 | (same population, time-binned)   |
| Ball / TAS          | Ball 2022     | TAS rock-type     | 15 | 10 | (degenerate — silica-defined)    |
| Stracke / Location  | Stracke 2022  | OIB Location      | 15 | 10 | pure ocean-island basalt         |
| Tappe / Country     | Tappe 2024    | Country/Region    |  8 | 10 | Group-1 kimberlite (intra-craton)|
| Qin / Location      | Qin 2024      | Cpx-grain Location| 30 |  9 | mantle xenolith clinopyroxene    |

Total samples summed across kept bins: ~50,500.

---

## Headline Numbers

```
Scheme                      T   D  CurvD CurvP  EnD  EnP   A      λ
====================================================================
Ball/Region (T=95)         95  10     14     2   46    1   0.118 −0.581
Ball/Age    (T=10)         10  10     13     2    6    0   0.036 −0.619
Ball/TAS    (T=15)         15  10      4     1    4    2     —      —
Stracke-OIB (T=15)         15  10     14     2   11    0   0.114 −0.569
Tappe-KIM   (T=8)           8  10     16     2    4    0   0.066 −0.596
Qin-Cpx     (T=30)         30   9     15     2   26    0   0.098 −0.691
```

M² = I verified to IEEE 754 floor in all six runs
(residuals 1.6 × 10⁻¹⁷ to 1.3 × 10⁻¹⁶).

---

## Finding 1 (CONFIRMED) — Period-2 attractor universality

**5 of 6 schemes converge to a period-2 limit cycle** in the curvature
tower. The five non-degenerate runs all show:

* curvature depth 13–16 (mean 14.4)
* curvature attractor amplitudes 0.04–0.12
* Lyapunov exponents −0.57 to −0.69 (all asymptotically stable)

The 6th (Ball/TAS) is the **degenerate case** by design: TAS classes are
defined by SiO₂ content, so ordering bins by ascending median SiO₂
produces a trajectory pre-aligned to one carrier. The dual involution
M(x) inverts the composition; in a trajectory already aligned to the
silica axis, the inversion has nothing new to reveal. Curvature
terminates at depth 4 with a period-1 fixed point at Hs = 0.669.

**Universality holds even at D = 9 with K₂O absent from the carrier set
(Qin clinopyroxene).** This is a stronger test than originally proposed:
the period-2 attractor does not depend on the specific carrier identity,
only on the existence of a non-trivial compositional simplex.

→ Math Handbook Ch 23.5: extend universality from 7 to 8 domains.
  Add geochemistry rows for Ball, Stracke, Tappe, Qin.

## Finding 2 (REVISED) — Helmsman lineage prefix is "most-diagnostic carrier", not specifically K₂O

Original conjecture (v1): the curvature tower starts with K₂O at L1–L3
across all bin schemes. **This held in 4/4 Ball + Stracke runs but
breaks at Tappe and Qin.**

```
Lvl  Ball/Region    Ball/Age      Ball/TAS    Stracke-OIB   Tappe-KIM   Qin-Cpx
L1   K2O            K2O           K2O         K2O           TiO2        Cr2O3
L2   K2O            K2O           K2O         K2O           TiO2        Cr2O3
L3   K2O            K2O           K2O         K2O           K2O         Cr2O3
L4   MgO            CaO           K2O         MgO           TiO2        Al2O3
```

Tappe (kimberlite) leads with **TiO₂** and alternates with K₂O across
deeper levels. Kimberlites are extraordinarily TiO₂-rich (phlogopite +
perovskite + Mg-Cr-titaniferous spinel mineralogy), so TiO₂ rivals K₂O
as the diagnostic carrier.

Qin (mantle xenolith clinopyroxene) leads with **Cr₂O₃** and locks
there for L1–L3, then transitions to Al₂O₃. K₂O is not a carrier in
this dataset; the recursion picks the next most-concentrated carrier.

The refined hypothesis:

> The L1–L3 helmsman is the carrier with the largest CLR variance in
> the dataset, i.e. the carrier whose log-ratio deviation from
> uniformity is most pronounced. For intraplate volcanic rocks this
> happens to be K₂O (LILE fertility tracer). For kimberlites it is
> TiO₂ (HFSE plume marker). For mantle pyroxene it is Cr₂O₃
> (compatible-element partitioning into the host phase).

The simplex is not "reading K₂O" — it is **reading the geological
diagnostic of the host system**, and that diagnostic varies by regime.

The L4 mafic-cation transition (MgO/CaO) holds in 3 of 6 schemes
(Ball/Region, Ball/Age, Stracke). It does not appear in Tappe or Qin.
**Less robust than originally claimed.**

→ Math Handbook Ch 22: add §22.8 "The Most-Diagnostic Carrier Helmsman
  Reading" — emphasise that the simplex picks the highest-variance
  carrier, not any specific element.

## Finding 3 (REVISED — important methodological caveat) — Energy tower depth is trajectory-order dependent, not an intrinsic property

Original conjecture (v1): energy depth scales as ≈ 0.5 × T for D ≈ 10
oxide compositions, in contrast to most previously-tested systems where
E_depth = 1.

**This conjecture fails on its own data.** A T-sweep on Ball/Region
with the regions sorted by sample count instead of alphabetically
yields a completely different energy depth at the same T:

```
Same 95 regions, same barycenters, different traversal order:

  Ordering                    curv_depth  curv_P  energy_depth  energy_P
  ------------------------------------------------------------------------
  alphabetical (Afar→Yemen)        14       2          46           1
  sample-count descending          14       2          17           1
```

The curvature tower is identical. The energy tower differs by a factor
of nearly 3.

This makes physical sense once stated: the energy composition

> e_j(t) = (Δh_j)² / Σ(Δh_k)²

is computed from differences between *consecutive* compositions.
Reorder the trajectory and the differences change. The energy tower
is intrinsically a property of the (composition set, traversal order)
pair, not of the composition set alone.

The full T-sweep on Ball/Region (sample-count ordering):

```
T   curv_depth curv_P energy_depth energy_P E/T
10        4      1          6        0    0.600 (degenerate — top-10
20       14      2          4        1    0.200      regions are too
40       13      2          4        1    0.100      similar to develop
60       14      2         13        1    0.217      compositional spread)
80       14      2         11        1    0.138
95       14      2         17        1    0.179
```

Across all 10 data points (6 T-sweep + 4 cross-dataset), a linear fit
E_depth = α·T + β gives **α = 0.097, β = 6.6, R² = 0.18**. The 0.5×T
ratio claimed in v1 was an artifact of the alphabetical ordering on
the original Ball/Region run alone.

What IS robust: **curvature tower depth = 14 (±1) for D = 10 oxide
compositions at T ≥ 20**. Five of six runs at D = 10 give curv_depth
∈ {13, 14, 16}. This is a candidate for an intrinsic-property claim,
but only with sufficient T to escape small-T degeneracy (Ball/top-10
collapses to depth 4).

→ Math Handbook Ch 19.4: do NOT add the "energy depth = 0.5×T" claim.
  Instead, add a methodological note: energy tower depth depends on
  trajectory ordering and is not a parameter-free measurement of the
  data alone. **An additional convention is needed for non-temporal
  datasets** specifying the canonical ordering (e.g. by Aitchison
  distance from barycenter, or by some diagnostic carrier value).

→ Math Handbook Ch 19.5: confirm that **curvature tower depth ≈ 14
  for D = 10 oxide systems** is a candidate intrinsic-property
  observation, requires more data points across D values to test.

---

## What Stays True From v1

* Period-2 attractor universality (now 5/6 → 8th domain)
* Lyapunov stability: λ < 0 in all 5 non-degenerate runs
* M² = I verified to IEEE floor in all 6 runs
* Ball / Region and Stracke OIB give nearly identical curvature
  attractor amplitudes (0.118 vs 0.114) and λ (−0.58 vs −0.57) —
  this is the strongest within-domain robustness signal in the study
* The TAS run is correctly identified as degenerate by the engine

## What Was Wrong In v1

* "K₂O → mafic → Na₂O → SiO₂" was reported as a universal lineage
  prefix. **It is universal within Ball + Stracke (intraplate
  volcanics) but specific to that regime.** The actual universal
  property is "the highest-CLR-variance carrier dominates L1–L3."
* "Energy tower depth = 0.5 × T" was reported as a candidate intrinsic
  observation. **The energy tower is trajectory-order dependent and
  the 0.5×T ratio was an alphabetical-ordering artifact.** The
  original Ball/Region E_depth = 46 still corresponds to one
  legitimate ordering, but is not a parameter-free measurement.

---

## Where This Lands Among 19+ Systems

Updated comparison table (geochem rows replace the prior single
"failed" entry):

| System              | Domain       | T   | D  | curv δ | A     | λ      | curv P |
|---------------------|--------------|-----|----|--------|-------|--------|--------|
| Backblaze           | Technology   |  4  |  4 |  4     | 0.577 | −4.54  | 2      |
| Germany EMBER       | Energy       |  ≈26|  9 |  8     | 0.918 | −2.37  | 2      |
| Cosmic budget       | Cosmology    |  10 |  5 |  9     | 0.369 | −1.37  | 2      |
| Japan EMBER         | Energy       |  26 |  8 | 13     | 0.044 | −1.31  | 2      |
| **Tappe-KIM**       | **Geochem**  |   8 | 10 | **16** | 0.066 | −0.60  | 2      |
| **Stracke-OIB**     | **Geochem**  |  15 | 10 | **14** | 0.114 | −0.57  | 2      |
| **Qin-Cpx**         | **Geochem**  |  30 |  9 | **15** | 0.099 | −0.69  | 2      |
| **Ball/Region**     | **Geochem**  |  95 | 10 | **14** | 0.118 | −0.58  | 2      |
| **Ball/Age**        | **Geochem**  |  10 | 10 | **13** | 0.036 | −0.62  | 2      |
| Citric              | Chemistry    | ≈14 |  3 | 14     | 0.336 | −0.56  | 2      |
| Conv. Drift         | AI / Lang    | ≈13 |  4 | 13     | 0.259 | −0.39  | 2      |
| Nuclear SEMF        | Nuclear      | ≈10 |  4 | 10     | 0.676 | −0.33  | 2      |
| **Geochem mean**    |              |     |    | **14.4** |     | **−0.61** |   |

The five non-degenerate geochem runs cluster tightly:
**curvature depth 13–16, λ between −0.57 and −0.69**. The mean
λ = −0.61 places geochemistry in the moderate-stability band of
the survey, between Conv. Drift and Citric.

---

## Honest Caveats

* All Lyapunov exponents in this battery are estimated from short
  trajectories (13–16 same-parity pairs). Cross-system comparisons
  with the original survey (some > 20 levels) should account for
  the smaller-sample bias.
* The Tappe sample is small (T = 8). The depth = 16 result is the
  highest in the geochem cohort but rests on the fewest bins.
* Qin clinopyroxene is mineral-grain-spot data, not bulk-rock
  composition. The compositional simplex is the same mathematical
  object, but the petrological semantics differ. **The fact that
  the period-2 attractor still appears at this very different
  scale (mineral grains vs whole rocks) is itself a robustness
  result.**
* Energy depth is now established as not a parameter-free observable.
  Future work needs to fix a canonical ordering convention before
  E_depth becomes a comparable diagnostic across runs.

---

## Files Produced (in this folder)

Run scripts:
* `bin_by_region.py` — original Region binner (95 bins, n≥10)
* `bin_by_age_and_tas.py` — Ball Age and TAS binners
* `bin_stracke_OIB.py` — Stracke OIB Location binner
* `bin_tappe_and_qin.py` — Tappe KIM1 and Qin Cpx binners
* `t_sweep.py` — Ball/Region T-sweep (T = 10, 20, 40, 60, 80, 95)

Bin tables (CSV barycenters):
* `ball_oxides_by_region_barycenters.csv` — 95 × 10
* `ball_oxides_by_age_barycenters.csv` — 10 × 10
* `ball_oxides_by_tas_barycenters.csv` — 15 × 10
* `stracke_oib_by_location_barycenters.csv` — 15 × 10
* `tappe_kim1_by_country_barycenters.csv` — 8 × 10
* `qin_cpx_by_location_barycenters.csv` — 30 × 9
* `ball_top{10,20,40,60,80,95}_barycenters.csv` — T-sweep variants

CNT outputs (cnt_tensor_engine + cnt_depth_sounder):
* `ball_regions_*.json` (full 4-program suite for original Ball/Region)
* `ball_age_*.json`, `ball_tas_*.json`
* `stracke_oib_*.json`, `tappe_*.json`, `qin_*.json`
* `ball_top{T}_*.json` for the T-sweep

Cross-comparisons:
* `comparison_region_age_tas.json` — three Ball schemes (v1)
* `comparison_4way.json` — four-way (v1)
* `comparison_6way.json` — six-way (this version)
* `t_sweep_results.json` — T-sweep + linear fit
* `JOURNAL.md` — original Region-only journal
* `ROBUSTNESS_JOURNAL.md` — v1, three-finding journal (superseded)
* `ROBUSTNESS_JOURNAL_v2.md` — this document

---

*The instrument reads. The expert decides. The loop stays open.*
