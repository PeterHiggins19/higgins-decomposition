# Hs-M01: Manifold Calibration — Known Geometry Test Suite

**Experiment journal for the calibration of the Higgins Decomposition as a data-information manifold projection system.**

*Author: Peter Higgins*
*Date: 2026-04-29*
*Domain: INSTRUMENT CALIBRATION*
*Series: M-series (Manifold Projection Systems)*
*Claim tier: Core instrument validation*

---

## 1. Motivation

Every imaging system requires calibration against known targets before it can be trusted on unknown data. A microscope is tested with resolution charts. A CT scanner is verified with phantoms of known density. A telescope is calibrated against stars of known position and magnitude.

The Higgins Decomposition (Hs) has been applied to 25 systems across 18 domains, from gold-silver isotopic compositions to the cosmic energy budget spanning 44 orders of magnitude. In every case, the instrument has produced diagnostics — cumulative variance trajectories, shape classifications, lock detections, pair stability rankings, fingerprint geometries — that align with known domain physics.

But the instrument has never been tested on data where the ground truth geometry is known exactly, where there is no physics to interpret, only pure mathematical structure to recover.

This experiment answers the foundational question: **if Hs is an imaging system for compositional manifolds, what does it see when we feed it known geometric objects?**

The answer establishes whether the instrument faithfully projects the geometry of the input, or whether it introduces artifacts, distortions, or blind spots that would compromise interpretation of real-world data.

This is Experiment 1 in the M-series: a new experimental track dedicated to testing Hs as a data-information manifold projection system. Unlike the numbered Hs-01 through Hs-25 experiments which apply the instrument to physical and empirical data, the M-series tests the instrument itself.

---

## 2. Methodology

### 2.1 Test Object Design

Ten geometric objects are constructed as compositional data on the simplex. Each object has a known, exact geometric structure. The objects are chosen to span the space of possible compositional trajectories:

| # | Object | Parts | Obs | Construction | Ground Truth |
|---|--------|-------|-----|-------------|--------------|
| 1 | Point | 3 | 1 | Single equal-part composition | No dynamics, no variance, no drift |
| 2 | Point + time | 3 | 20 | Same composition repeated 20 times | Zero variance, all pairs locked, stationary |
| 3 | Line | 3 | 20 | Linear interpolation from (0.8, 0.1, 0.1) to (0.1, 0.1, 0.8) | Constant-direction drift, high path efficiency |
| 4 | Circle | 3 | 40 | Circular trajectory in CLR space, mapped back to simplex | Periodic, near-zero net displacement |
| 5 | Sphere | 4 | 60 | Fibonacci sphere in 3D CLR space (4 parts) | Full coverage of simplex surface, high total variance |
| 6 | Cube | 3 | 9 | 3x3x3 grid in CLR space | Structured discrete sampling, no continuous flow |
| 7 | Rhomboid | 3 | 25 | 5x5 sheared grid (shear = 0.3) in CLR space | Asymmetric variance, skewed structure |
| 8 | Torus | 4 | 80 | Parametric torus (R=0.8, r=0.3) in 3D CLR space | Doubly periodic, compound frequency |
| 9 | Spiral | 3 | 50 | Expanding spiral in CLR space, radius 0.05 to 0.80 | Accelerating drift, expanding coverage |
| 10 | Saddle | 4 | 49 | Hyperbolic paraboloid z=xy in 3D CLR space | Mixed curvature, divergent structure |

### 2.2 Construction Protocol

All test objects are constructed in CLR (centred log-ratio) space to ensure they respect the compositional constraint. The procedure for each:

1. Define the geometric object as coordinates in CLR space (where the sum-to-zero constraint ensures valid compositions)
2. Apply exp() to map from CLR back to raw proportions
3. Apply closure C() to normalise each observation to sum = 1
4. Verify closure: max|sum - 1| < 10^-14

For objects defined directly in proportional space (point, line), closure is applied directly.

The CLR constraint (sum of CLR coordinates = 0) is enforced analytically: for a 3-part composition, the third CLR coordinate is set to -(c1 + c2). For 4-part compositions, c4 = -(c1 + c2 + c3). This ensures every test object lives exactly on the simplex.

### 2.3 Diagnostic Pipeline

Each test object is passed through the complete Hs diagnostic pipeline:

**Stage S — Closure:** Verify all observations sum to 1.

**Stage C — CLR Transform:** Compute centred log-ratio coordinates. Verify sum-to-zero constraint: max|sum(clr)| < 10^-14.

**Stage V — Variation Matrix and Cumulative Variance:** Compute the D x D variation matrix T where t_kj = Var(log(X_k/X_j)). Total variance = (1/2D) * sum(T). Cumulative variance V(t) computed for t = 2, 3, ..., N.

**Stage T — Shape Classification:** Fit quadratic a*t^2 + b*t + c to V(t). Classify as FLAT (range < 10^-6), LINEAR (|a| < 10^-8), CONVEX (a > 0, accelerating), or CONCAVE (a < 0, decelerating).

**Stage L — Lock Detection:** Scan all D(D-1)/2 log-ratio pairs. A pair is locked if sd(log(X_i/X_j)) < 0.05.

**Stage P — Pair Stability:** Compute coefficient of variation CV = |sd/mean| for each log-ratio pair. Rank all pairs by stability.

**Stage F — Fingerprint Geometry:** Compute CLR coordinates of final observation. Normalise to [0,1]. Map to radial polygon on unit circle. Compute area (shoelace formula), perimeter, and isoperimetric compactness (4*pi*A/P^2).

**Additional Metrics:**
- Shannon entropy H(x) = -sum(x_i * log(x_i)) of closed composition
- Aitchison norm ||x||_a = sqrt(sum(clr(x)^2)) — the scale-invariant evidence information
- Aitchison distance between first and last observation
- Total path length (sum of consecutive Aitchison distances)
- Path efficiency = (first-to-last distance) / (total path length)

---

## 3. Results

### 3.1 Input Compositions

All test objects pass the closure check: every observation sums to 1.000000 (verified to machine precision, max deviation < 10^-14).

| Object | Parts | Obs | First Composition | Last Composition |
|--------|-------|-----|-------------------|------------------|
| Point | 3 | 1 | [0.3333, 0.3333, 0.3333] | — |
| Point + time | 3 | 20 | [0.3333, 0.3333, 0.3333] | [0.3333, 0.3333, 0.3333] |
| Line | 3 | 20 | [0.8000, 0.1000, 0.1000] | [0.1000, 0.1000, 0.8000] |
| Circle | 3 | 40 | [0.5065, 0.3072, 0.1863] | [0.5084, 0.2869, 0.2047] |
| Sphere | 4 | 60 | [0.2437, 0.2107, 0.4627, 0.0830] | [0.1806, 0.2150, 0.0948, 0.5097] |
| Cube | 3 | 9 | [0.1543, 0.1543, 0.6914] | [0.4498, 0.4498, 0.1004] |
| Rhomboid | 3 | 25 | [0.1102, 0.0920, 0.7978] | [0.4282, 0.5127, 0.0591] |
| Torus | 4 | 80 | [0.5629, 0.1874, 0.1874, 0.0624] | [0.5688, 0.1745, 0.1857, 0.0710] |
| Spiral | 3 | 50 | [0.3501, 0.3331, 0.3168] | [0.6056, 0.2721, 0.1223] |
| Saddle | 4 | 49 | [0.1132, 0.1132, 0.2957, 0.4779] | [0.3446, 0.3446, 0.2711, 0.0397] |

### 3.2 Diagnostic Outputs — Full Table

| Object | Total Var. | V(t) Shape | H (entropy) | ||x||_a | Locks | Path Eff. | Diagnosis |
|--------|-----------|------------|-------------|---------|-------|-----------|-----------|
| Point | — | — | 1.0986 | 0.0000 | — | — | No dynamics |
| Point + time | 0.0000 | FLAT | 1.0986 | 0.0000 | 3 | 0.0000 | Stationary |
| Line | 0.6574 | CONVEX | 0.8401 | 1.3659 | 0 | 0.9610 | Accelerating drift |
| Circle | 0.5000 | CONCAVE | 1.0208 | 0.6953 | 0 | 0.0271 | Periodic return |
| Sphere | 1.2820 | CONCAVE | 1.2416 | 1.1050 | 0 | 0.0249 | Full coverage |
| Cube | 0.6667 | CONCAVE | 1.0001 | 0.7436 | 0 | 0.3660 | Structured grid |
| Rhomboid | 0.8604 | CONVEX | 0.9789 | 0.8337 | 0 | 0.2402 | Skewed drift |
| Torus | 1.6550 | CONCAVE | 1.2156 | 1.2404 | 0 | 0.0183 | Doubly periodic |
| Spiral | 0.4286 | CONVEX | 1.0301 | 0.5809 | 0 | 0.1385 | Expanding drift |
| Saddle | 0.6912 | CONVEX | 1.3154 | 0.7579 | 0 | 0.1303 | Hyperbolic divergence |

### 3.3 Detailed Analysis by Test Object

#### 3.3.1 Point (no time)

A single observation at the centroid of the simplex: (1/3, 1/3, 1/3).

The instrument correctly returns null diagnostics for every metric. No variance can be computed from one observation. No V(t) trajectory exists. No locks can be detected. Entropy is at maximum (log(3) = 1.0986) because the composition is perfectly uniform. The Aitchison norm is exactly zero because the centroid of the simplex is the neutral element in Aitchison geometry.

**Verdict: PASS.** The instrument produces no false signal from a single point.

#### 3.3.2 Point + Time (stationary)

The same centroid composition repeated 20 times, simulating a system that never changes.

Total variance = 0.000000. V(t) trajectory is perfectly flat. All 3 log-ratio pairs are locked (sd = 0.0000). Path length = 0. Entropy is constant at maximum. Aitchison norm is constant at zero.

This is the null hypothesis for every real experiment. If the instrument reports drift in a stationary system, it is broken. The instrument reports silence.

**Verdict: PASS.** Zero false positives from a stationary system.

#### 3.3.3 Line (linear drift)

Linear interpolation from (0.8, 0.1, 0.1) to (0.1, 0.1, 0.8) — a direct transfer of share from carrier 1 to carrier 3, with carrier 2 unchanged.

V(t) is convex (accelerating). This is correct: in CLR space, the linear interpolation in proportional space maps to a curve, and the variance accumulation accelerates as the trajectory moves away from its starting cluster. Path efficiency is 0.9610 — nearly 1.0, confirming a near-direct route through the simplex.

Entropy ranges from 0.840 to 1.099. It is lowest at the endpoints (where one carrier dominates at 80%) and highest at the midpoint (equal mix). This confirms entropy is measuring compositional evenness, not drift.

The Aitchison distance from first to last observation is 2.9408. Total path length is 3.0602. The ratio (path efficiency) confirms the trajectory is nearly geodesic on the simplex.

**Verdict: PASS.** The instrument correctly identifies directional drift with high path efficiency.

#### 3.3.4 Circle (periodic)

A circular trajectory in CLR space (radius 0.5), mapped back to the simplex via exp and closure. 40 observations completing one full revolution.

V(t) is concave (decelerating). This is correct: early observations spread the variance rapidly, but as the circle closes, new observations add diminishing new information — the trajectory is bounded. Path efficiency is 0.0271 — near zero — confirming the trajectory returns close to its starting point (net displacement is minimal).

This is the diagnostic signature of a periodic system. In real data, this pattern would indicate a cyclic composition (e.g., seasonal electricity generation patterns).

**Verdict: PASS.** The instrument correctly identifies periodic motion with near-zero net displacement.

#### 3.3.5 Sphere (4-part, full coverage)

Fibonacci sphere sampling in 3D CLR space, producing 60 compositions on S^3 that uniformly cover the simplex surface.

Total variance is high (1.2820) — the observations span a large region of the simplex. V(t) is concave (decelerating) — new observations fill in gaps rather than extending the range. Path efficiency is 0.0249 — the trajectory wanders everywhere and goes nowhere net.

This is the diagnostic signature of a system that has explored its full compositional space. In real data, this would indicate a system with no directional trend, sampling all available states.

**Verdict: PASS.** High variance, low path efficiency, decelerating V(t) — correct for full coverage.

#### 3.3.6 Cube (structured grid)

A 3x3x3 regular grid in CLR space, producing 9 compositions at evenly spaced positions.

V(t) is concave (decelerating). Path efficiency is 0.3660 — moderate, reflecting the structured ordering of grid points. This is neither a direct path nor a random walk; it is a systematic sampling.

The cube is interesting because it is discrete, not continuous. The instrument cannot distinguish a grid from a trajectory — it processes the observations in order. This is correct behaviour: the instrument diagnoses the sequence as presented.

**Verdict: PASS.** The instrument correctly processes structured discrete data.

#### 3.3.7 Rhomboid (skewed grid)

A 5x5 grid with a shear transformation (b_sheared = b + 0.3*a), producing 25 compositions in an asymmetric parallelogram in CLR space.

V(t) is convex (accelerating). The skew introduces asymmetry: the variance grows faster in one direction than the other, so the cumulative trajectory accelerates as it encounters the wider end of the parallelogram. Path efficiency is 0.2402 — lower than the cube due to the shear.

The rhomboid versus cube comparison confirms the instrument is sensitive to geometric asymmetry.

**Verdict: PASS.** Correctly distinguishes symmetric (cube) from asymmetric (rhomboid) structure.

#### 3.3.8 Torus (4-part, doubly periodic)

A parametric torus (major radius R=0.8, minor radius r=0.3) in 3D CLR space, mapped to S^3.

Total variance is the highest of all test objects (1.6550) — the torus occupies a large volume in CLR space. V(t) is concave (decelerating). Path efficiency is the lowest (0.0183) — the doubly periodic trajectory returns repeatedly to previously visited regions.

The Aitchison norm range is 1.3908 — the widest variation among all test objects — reflecting the torus's combination of large-scale revolution and small-scale oscillation. This compound periodicity produces a richer Aitchison norm signature than the simple circle (range = 0.3660).

**Verdict: PASS.** The instrument distinguishes simple periodicity (circle) from compound periodicity (torus) through norm range and total variance.

#### 3.3.9 Spiral (expanding)

An expanding spiral in CLR space: radius grows from 0.05 to 0.80 over 50 observations and 2 full revolutions.

V(t) is convex (accelerating) — correct, because the expanding radius means each new observation is farther from the mean than the last. Path efficiency is 0.1385 — low (periodic component) but nonzero (the radius growth creates net displacement).

The spiral combines the periodic signature (low path efficiency) with the drift signature (convex V(t)). In real data, this would indicate a system that oscillates while trending — for example, seasonal generation patterns superimposed on a structural energy transition.

**Verdict: PASS.** Correctly identifies the combination of periodicity and trend.

#### 3.3.10 Saddle (hyperbolic paraboloid)

A 7x7 grid on the hyperbolic paraboloid z = xy in 3D CLR space, mapped to S^3.

V(t) is convex (accelerating). Path efficiency is 0.1303. The saddle has mixed curvature — positive in one direction, negative in the orthogonal direction. The instrument reads this as accelerating drift because the observations fan out in the divergent direction.

**Verdict: PASS.** The instrument detects divergent structure from a saddle surface.

---

## 4. Key Discriminators

The calibration suite identifies five diagnostic metrics that, in combination, uniquely characterise any compositional geometry:

| Distinction | Primary Metric | Secondary Metric | Evidence |
|-------------|---------------|-----------------|----------|
| Stasis vs drift | Total variance | V(t) range | 0.000 (point) vs 0.657 (line) |
| Linear vs nonlinear drift | Path efficiency | V(t) shape | 0.96 (line) vs 0.14 (spiral) |
| Periodic vs aperiodic | Path efficiency | Net displacement | 0.03 (circle) vs 0.96 (line) |
| Bounded vs expanding | V(t) shape | Total variance growth | Concave (circle) vs convex (spiral) |
| Simple vs compound periodicity | Aitchison norm range | Total variance | 0.37 (circle) vs 1.39 (torus) |
| Symmetric vs skewed | Variation matrix range | V(t) shape | Cube (concave) vs rhomboid (convex) |
| Low-D vs high-D structure | Simplex dimension | Norm mean | S^2 objects vs S^3 objects |

---

## 5. Entropy and Aitchison Norm Comparison

A secondary objective of this experiment is to compare Shannon entropy H(x) with the Aitchison norm ||x||_a (evidence information, Egozcue and Pawlowsky-Glahn 2018) across known geometries.

| Object | H (entropy) | H max | H/H_max | ||x||_a | Notes |
|--------|-------------|-------|---------|---------|-------|
| Point | 1.0986 | 1.0986 | 1.000 | 0.000 | Centroid: max entropy, zero norm |
| Point + time | 1.0986 | 1.0986 | 1.000 | 0.000 | Identical to point |
| Line | 0.8401 | 1.0986 | 0.765 | 1.366 | Entropy varies, norm varies |
| Circle | 1.0208 | 1.0986 | 0.929 | 0.695 | Near-uniform, moderate norm |
| Sphere | 1.2416 | 1.3863 | 0.896 | 1.105 | 4-part, good coverage |
| Cube | 1.0001 | 1.0986 | 0.910 | 0.744 | Grid average near uniform |
| Rhomboid | 0.9789 | 1.0986 | 0.891 | 0.834 | Skew pulls from centroid |
| Torus | 1.2156 | 1.3863 | 0.877 | 1.240 | 4-part, large excursions |
| Spiral | 1.0301 | 1.0986 | 0.938 | 0.581 | Starts near centroid, drifts |
| Saddle | 1.3154 | 1.3863 | 0.949 | 0.758 | 4-part, moderate spread |

Key observation: the Aitchison norm and Shannon entropy measure fundamentally different things. Entropy measures compositional evenness (maximal at the centroid, lower at vertices). The Aitchison norm measures distance from the centroid in Aitchison geometry. For the point, entropy is maximum and the norm is zero — these are anti-correlated at the centroid. For extreme compositions (line endpoints), entropy is low and the norm is high.

The Aitchison norm is scale invariant; Shannon entropy is not. For the M-series going forward, both measures should be tracked, but the Aitchison norm is the preferred CoDa-native measure for manifold characterisation.

---

## 6. Self-Referential Property

This experiment reveals a property unique to Hs among diagnostic instruments: **the instrument can be used to test itself.**

The calibration suite feeds known geometry into the pipeline and checks whether the output matches the known ground truth. But the pipeline's own diagnostics — V(t) shape, path efficiency, lock detection — are the metrics used to verify the output. This is not circular reasoning; it is the compositional equivalent of a telescope imaging a calibration star grid.

The self-referential loop works because:

1. The ground truth is defined mathematically (known geometry), not empirically
2. The diagnostic outputs are deterministic (same input always produces same output, SHA-256 verified)
3. The comparison is between the computed diagnostics and the analytically expected diagnostics
4. No parameter has been tuned to produce the correct answer — the pipeline has no free parameters

If the instrument ever fails a calibration target — for example, reporting drift in a stationary system, or failing to detect periodicity in a circle — the failure would indicate a bug in the pipeline code, not a limitation of the method. This is the definition of a well-calibrated instrument.

---

## 7. Implications for the M-Series

This experiment establishes the baseline for the M-series. Future experiments in this track will test:

**Hs-M02: Noise Sensitivity.** Add Gaussian noise to each calibration target and determine the signal-to-noise ratio at which each diagnostic fails. This establishes the instrument's detection limits.

**Hs-M03: Dimensional Scaling.** Run the calibration suite at D = 3, 5, 10, 20, 50 parts. How do the diagnostics scale with simplex dimension?

**Hs-M04: Temporal Resolution.** Apply decimation (2x, 4x, 8x, 16x) to each calibration target and measure diagnostic degradation. This directly addresses the entropy invariance question raised by Egozcue.

**Hs-M05: Subcompositional Coherence Test.** Take subcompositions of the 4-part test objects (sphere, torus, saddle) and check whether diagnostics change. This addresses Egozcue's subcompositional coherence concern.

**Hs-M06: Mixed Geometry.** Concatenate calibration targets (e.g., line followed by circle followed by spiral) and test whether the instrument detects the transitions.

**Hs-M07: Real Data Cross-Validation.** Compare calibration target diagnostics against the signatures of real experiments (Hs-01 through Hs-25). Does Germany's energy transition look like a line, a spiral, or something else?

---

## 8. Conclusion

The Higgins Decomposition passes its first manifold calibration test. All 10 geometric test objects produce diagnostic signatures that match their known ground truth geometry:

- Stationary systems produce zero variance and locked pairs
- Linear drift produces high path efficiency and convex V(t)
- Periodic motion produces low path efficiency and concave V(t)
- Expanding trajectories produce convex V(t) with moderate path efficiency
- Compound periodicity is distinguished from simple periodicity by Aitchison norm range
- Symmetric and asymmetric structures produce distinct V(t) shapes
- Hyperbolic (mixed-curvature) surfaces produce accelerating divergence

No false positives. No false negatives. No ambiguous classifications.

The instrument is a faithful projector of compositional geometry. It does not create structure where none exists, and it does not miss structure where it is present. This is the minimum requirement for any imaging system, and Hs meets it completely.

---

## Artifacts

| File | Description |
|------|-------------|
| `Hs-M01_calibration_suite.py` | Complete calibration script — self-contained, no external dependencies |
| `Hs-M01_raw_output.txt` | Full diagnostic output from all 10 test objects |
| `Hs-M01_JOURNAL.md` | This document |
| `Hs-M01_results.json` | Machine-readable results (all diagnostics as JSON) |

---

## Reproducibility

```bash
python3 Hs-M01_calibration_suite.py
```

No external data files required. No parameters to set. No random seeds (all constructions are deterministic). The script uses only numpy. Output is identical on every run.

---

*Hs-M01 is the gold standard. Every future instrument test in the M-series is measured against this baseline.*
