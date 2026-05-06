# HCI User Guide — Compositional Systems Navigation Plotter

## 1. What HCI Is

HCI is a compositional systems navigation plotter. It converts raw carrier data into a geometric instrument frame where position, bearing, displacement, dominance, and dynamic range become measurable quantities.

HCI charts where the system is, where it has been, which carriers drove displacement, and which metric directions support future guidance.

HCI does not automatically predict the future. It provides the navigational geometry needed to reason about future guidance. HCI is the navigation plotter — it tells the operator what steering means.

The instrument reads. The expert decides. The loop stays open.

## 2. What Data HCI Reads

HCI reads positive carrier data from any domain: energy systems, chemical compositions, economic sectors, biological samples, audio spectra, particle physics, or any system that can be expressed as D positive parts summing to a whole.

The data are closed to a composition. Closure removes absolute magnitude from the plotted coordinate, so raw totals are preserved separately as system size. The plate coordinate shows relative structure, not raw amplitude.

## 3. HCI Units — Higgins Log-Ratio Level (HLR)

The plate coordinate unit is **Higgins Log-Ratio Level (HLR)**.

HLR is a dimensionless natural log-ratio unit. It measures carrier displacement above or below the geometric-mean share. It is analogous in spirit to audio decibel thinking, but it is not automatically a decibel. The nearest relative in the log-level family is the **neper** (natural-log amplitude ratio).

### Definition

```
HLR_j(t) = h_j(t) = ln(x_j(t)) - mean_k ln(x_k(t))
                    = ln(x_j(t) / g(x(t)))

where:
  x_j(t)   = closed share of carrier j at time t
  g(x(t))  = geometric mean of all carrier shares
```

### Interpretation

| HLR value | Ratio exp(HLR) | Meaning |
|-----------|----------------|---------|
| -2.0 | 0.135x | carrier far below geometric-mean share |
| -1.0 | 0.368x | carrier about one-third geometric-mean share |
| -0.693 | 0.500x | carrier is half geometric-mean share |
| 0.0 | 1.000x | carrier is at geometric-mean share |
| +0.693 | 2.000x | carrier is twice geometric-mean share |
| +1.0 | 2.718x | carrier is e times geometric-mean share |
| +2.0 | 7.389x | carrier far above geometric-mean share |

### Why "Higgins Log-Ratio Level"?

The name is not a claim of inventing log-ratios. It is an instrument stamp: it tells the reader that this value was produced by the HCI processing chain (raw data, closure, CLR/Higgins Coordinate, metric tensor, section ledger/plate). The stamp identifies the measurement protocol, not just the numerical unit.

Reporting values in Higgins Log-Ratio Level indicates that the data have been processed through the HCI compositional navigation instrument, not read directly as raw magnitude.

### Scale Family — Nearest Relatives

| Scale | Formula | What it means |
|-------|---------|---------------|
| HLR | ln(x_j / g(x)) | compositional log-ratio level |
| Neper | ln(amplitude ratio) | natural-log amplitude ratio |
| Log fold change | ln(A/B) or log2(A/B) | biological/statistical ratio change |
| Decibel amplitude | 20 log10(A/B) | audio/electrical amplitude level |
| Decibel power | 10 log10(P1/P2) | power ratio level |

### Conversions

| HCI readout | Formula | Meaning |
|-------------|---------|---------|
| HLR level | h_j = ln(x_j/g(x)) | carrier log-ratio level |
| Carrier multiplier | exp(h_j) | carrier relative to geometric-mean share |
| Carrier change | delta_h_j | log-ratio change between plates |
| Change multiplier | exp(delta_h_j) | readable carrier rise/fall |
| Metric distance | \|\|h(t2)-h(t1)\|\| | compositional distance between plates |
| Metric energy | \|\|h(t)\|\|^2 | displacement from barycentric balance |
| Dynamic range | max(h)-min(h) | strongest-to-weakest carrier spread |
| Dynamic range ratio | exp(max(h)-min(h)) | strongest/weakest carrier ratio |
| HLR-dB amplitude | 8.686 * h | audio-like level analogy |
| HLR-dB power | 4.343 * h | power-ratio analogy |

## 4. The HCI Scale Provenance Map

Every section plate shows data that has passed through a transformation chain. The Scale Provenance Map explains what is being related to what.

### The Chain

```
Raw carrier value:     Y_j(t)
Raw total:             T(t) = sum_k Y_k(t)
Closed composition:    x_j(t) = Y_j(t) / T(t)
Higgins coordinate:    h_j(t) = ln(x_j(t)) - mean_k ln(x_k(t))
Relative multiplier:   exp(h_j(t)) = x_j(t) / geometric_mean_share
Section coordinate:    projection onto XY / XZ / YZ face
```

The plate does not plot raw values directly. It plots closed compositions as Higgins-coordinate displacement from the barycentre under a fixed run scale. Raw total T(t) is reported separately because closure removes absolute magnitude.

### Key Caution

HCI measures relative compositional power. It measures physical power only when the input carriers themselves are physical power measurements.

## 5. Stage 1 — Section Engine

Stage 1 generates the metric section atlas: one section plate per time index showing three orthogonal face projections plus a metric ledger.

### Plate Layout — Higgins Tensor Data Field Layout v1.0

```
+----------+----------+------------------+
|  Info    |  Legend  |  XZ Bearings bar |
+----------+----------+------------------+
|  XY Scatter         |  YZ CLR bar      |
+---------------------+------------------+
```

| Panel | Content |
|-------|---------|
| Info | Hs, ring, E_metric, kappa, omega, d_A, helmsman, scale ranges, HLR unit |
| Legend | All D(D-1)/2 pair indices with carrier names |
| XZ Face | Bar graph of all pairwise bearings in degrees [-180, +180] |
| XY Face | CLR scatter plan view — angle from origin = bearing |
| YZ Face | Bar graph of CLR/HLR coordinate per carrier |

### Fixed-Scale Instrument Display

All axes are fixed across all time frames (like a physical oscilloscope graticule). Rapid scrolling through the cine-deck shows genuine movement of compositional state against a constant backdrop.

One grid distance on Plate 1 equals the same Higgins-coordinate displacement on Plate 2, Plate 3, and so on. If each plate autoscaled itself, a tiny displacement could look large on one plate and a large displacement could look small on another.

### Scale Determination

1. Load all N records
2. Pre-scan all CLR values across all carriers and all time steps
3. Find global min/max
4. Pad by 10% of range for visual margin
5. Lock these limits for all plates

### Fixed Bounds

| Channel | Range | Guarantee |
|---------|-------|-----------|
| Bearings theta_ij | [-180, +180] deg | atan2 range — exact for any composition |
| Hs | [0, 1] | By definition: Hs = 1 - H/ln(D) |
| CLR / HLR | data-adaptive | Pre-scanned from full dataset, padded 10% |
| Angular velocity omega | [0, 180] deg | Absolute angular change per step |

## 6. Stage 1 Extension — System Course Plot

The System Course Plot is a whole-run barycentric plan view showing the complete compositional path from first observation to final observation. It is the navigation chart of the system.

### Required Elements

- Barycentre marker (origin crosshairs)
- Start marker (S) at h(t=0)
- Final marker (F) at h(t=N-1)
- All observation points connected by course line
- Start-to-final net vector (arrow S to F)
- DCDI/Helmsman turn markers at major displacement events
- Fixed global Higgins-coordinate scale

### Required Metrics

```
h_start           = Higgins coordinate at first observation
h_final           = Higgins coordinate at final observation
V_net             = h_final - h_start
net_distance      = ||V_net||
path_length       = sum_t ||h(t+1) - h(t)||
course_directness = net_distance / path_length
dynamic_range     = max(h) - min(h) at each time point
```

### Interpretation

The System Course Plot shows compositional course, not raw magnitude. It answers: how direct or indirect was the path? Which carriers created the major turns? How far is the final system from the initial system?

## 7. CNT and the Higgins Metric Tensor

The Compositional Navigation Tensor (CNT) is the tensor engine powering all HCI instruments.

```
CNT(x) = (theta, omega, kappa_HS, sigma)

theta    : bearing tensor      — all pairwise CLR angles
omega    : angular velocity    — heading change in full D-space (atan2, stable)
kappa_HS : Higgins Steering Metric Tensor — full (D x D) metric
sigma    : Dominant Carrier Displacement Index (Helmsman Index)
```

### Higgins Steering Metric Tensor

```
kappa_HS_ij(x) = (delta_ij - 1/D) / (x_i * x_j)
```

This is the full Aitchison metric tensor pulled back to the simplex. It describes local steering sensitivity, coupling between carriers, and boundary pressure.

### Diagonal Carrier Steering Sensitivity

```
s_j(x) = 1 / x_j
```

This is the diagonal of kappa_HS when i=j. It is a diagnostic channel, not the full tensor. Small carriers have high steering sensitivity; large carriers have low steering sensitivity.

### DCDI / Helmsman Index

```
sigma_HS(t, t+1) = argmax_j |h_j(t+1) - h_j(t)|
```

The carrier with the largest absolute HLR displacement between consecutive observations. The Helmsman is the carrier that steered the system most at that step.

## 8. CLR and ILR — Dual Coordinate Standard

HCI uses two coordinate frames:

**CLR (Centred Log-Ratio)** — the visible carrier-channel display frame. One coordinate per carrier. Carrier-readable. Used for section plates, DCDI/Helmsman identification, and operator language.

**ILR (Isometric Log-Ratio)** — the hidden orthonormal computation frame. D-1 dimensional, full-rank, isometric. Used for eigenanalysis, PCA, regression, clustering, condition-number control, and Stage 2/3 computation.

### Bridge

```
h_CLR = B * z_ILR
z_ILR = B^T * h_CLR
```

where B is the Helmert or selected orthonormal basis in the CLR plane.

### Policy

Use CLR for plates, DCDI, and carrier language. Use ILR for orthogonal decomposition, Stage 2/3 computation, and numerical stability.

## 9. Stage 2 — Metric Cross-Examination

Stage 2 performs pairwise and group-level metric cross-examinations. It consumes Stage 1 metric ledgers and produces comparative analysis.

Stage 2 includes: group barycenter analysis, pairwise group cross-examination, carrier-pair cross-examination, section-view cross-examination, ranked findings, CSV ledgers, and TXT summary reports.

Stage 2 uses the shared Higgins coordinate frame and shared Higgins Steering Metric Tensor. It does not create a new geometry.

## 10. Stage 3 — Higher-Degree Structural Analysis

Stage 3 extends beyond pairwise work into triadic, subcomposition, and regime-level structural signatures.

The degree ladder: point state, temporal increment, pairwise contrast, triadic structure, and k-degree subcomposition structure.

Stage 3 includes: triadic day analysis, carrier triad analysis, subcomposition degree ladder, and metric regime detection.

### Subcomposition Modes

Two distinct modes exist and must be labeled:

- **Global restriction mode**: use global CLR components under the original full composition
- **Subcomposition reclosure mode**: extract carrier subset, reclose, then recompute local CLR

These have different geometric meanings and must not be confused.

## 11. Reading Japan and EMBER Outputs

### Japan Data (Stage 1 demonstration)

Japan EMBER D=8 energy data (2000-2025) demonstrates the complete Stage 1 plate and scale-provenance system. Key features visible in the section atlas:

- Hs rises from 0.235 to 0.341 during the nuclear departure event (2011-2014), then returns toward 0.198
- Nuclear CLR drops to -33.86 in 2014 (composition effectively zero), creating two-population structure on XY scatter
- The Helmsman is Nuclear at t=11-16, then shifts to Other Fossil and Bioenergy
- Fixed scales make the nuclear departure visible as dramatic bearing swings on XZ face

### EMBER Data (target demonstration)

EMBER data across multiple countries is the target for demonstrating the full HCI navigation plotter: multi-country comparison, cross-system dynamic range, and Stage 2/3 analysis.

## HCI Metric Energy and Dynamic Range

### Metric Energy

```
E_HCI(t) = ||h(t)||^2
```

When E_HCI = 0, all carriers are at equal geometric-mean balance. Larger values mean the composition is farther from barycentric balance. Changes between plates show whether the system became more concentrated or more balanced.

### Compositional Dynamic Range

```
DR_HLR(t) = max_j h_j(t) - min_j h_j(t)
DR_ratio(t) = exp(DR_HLR(t))
DR_dB(t) = 8.686 * DR_HLR(t)
```

The HCI dynamic range is the log-ratio between the strongest and weakest carrier. It measures how spread the system is at each time point.

## Summary

Compositional log-ratio geometry converts relative carrier shares into dimensionless log-ratio levels. In HCI these levels are reported as Higgins Log-Ratio Levels. HLR values can be converted to carrier multipliers, dynamic range ratios, dB-like equivalents, metric distances, and metric energy.

The result is not raw magnitude analysis. It is relative systems-navigation: a way to measure position, displacement, dominance, spread, and course through compositional space.

The arc came full circle. HCI started from audio/log thinking, moved into compositional geometry, built a navigation instrument, and can now return to audio — or any other domain — with stronger mathematics. The system can compute its own path.

The instrument reads. The expert decides. The loop stays open.
