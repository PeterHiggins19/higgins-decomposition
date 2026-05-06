# Stage 2 — Pseudocode Reference (Order 2, locked)

**Module:** `atlas/stage2_locked.py`
**R port:** `atlas/stage2.R` (metric computation; PDF rendering is Python-only)
**Status:** Authoritative. Conforms to `atlas/OUTPUT_DOCTRINE.md` v1.0.1.
**Last revised:** 2026-05-05

This document is the language-neutral algorithm reference for Stage 2.
The Python (`stage2_locked.py`) and R (`stage2.R`) implementations are
reference instances of the algorithms defined here. Anyone reading this
can re-implement Stage 2 in any language.

---

## 1 — Inputs

A schema-2.x conformant CNT JSON. Stage 2 reads the following fields:

```
input.n_records              T
input.n_carriers             D
input.carriers               list of D carrier names
input.labels                 list of T row labels
tensor.helmert_basis.coefficients   (D-1, D) Helmert basis matrix
tensor.timesteps[t].coda_standard.clr            (D,)  CLR coordinates
tensor.timesteps[t].coda_standard.composition    (D,)  closed values
tensor.timesteps[t].higgins_extensions.bearing_tensor.pairs
                                       list of {carrier_i, carrier_j, theta_deg}
tensor.timesteps[t].higgins_extensions.metric_tensor.trace
tensor.timesteps[t].higgins_extensions.condition_number
stages.stage1.higgins_extensions.metric_ledger[t]
                                       hs, ring, omega_deg, helmsman, energy
stages.stage2.coda_standard.variation_matrix     (D, D)
stages.stage2.higgins_extensions.carrier_pair_examination
                                       list of {i, j, pearson_r, bearing_spread_deg, ...}
diagnostics.higgins_extensions.lock_events       list
metadata.engine_version, schema_version
diagnostics.content_sha256
```

No engine recomputation. Every value displayed at Stage 2 traces back to
one of these JSON fields by deterministic transforms.

---

## 2 — Order discipline

Per OUTPUT_DOCTRINE v1.0.1, Stage 2 displays only Order-2 content:

* per-step quantities aggregated across more than one timestep (Hs
  trajectory, Aitchison-norm trajectory, ILR-axes trajectories);
* inter-timestep dynamic quantities (bearings θ, angular velocity ω,
  metric trace, condition number, helmsman σ, ring class);
* whole-trajectory aggregates (variation matrix, pair correlations,
  lock events, V_net, path_length, course_directness);
* the System Course Plot (PCA-projected CLR trajectory, math handbook
  Ch 15) and the Compositional Bearing Scope (CBS, Ch 16).

Stage 1 (single-composition first principles) and Stage 3 (recursive /
dynamical) are out of scope.

---

## 3 — Algorithms

### 3.1 — Trajectory aggregates

```
For t in 0..T-1:
    composition[t]  = json.tensor.timesteps[t].coda_standard.composition
    clr[t]          = json.tensor.timesteps[t].coda_standard.clr
    aitchison_norm[t] = sqrt( sum_j clr[t][j]^2 )
    Hs[t]           = json.stages.stage1.higgins_extensions.metric_ledger[t].hs
    ring[t]         = json.stages.stage1.higgins_extensions.metric_ledger[t].ring
    omega[t]        = json.stages.stage1.higgins_extensions.metric_ledger[t].omega_deg
    helmsman[t]     = json.stages.stage1.higgins_extensions.metric_ledger[t].helmsman

basis = json.tensor.helmert_basis.coefficients     # (D-1, D)
ilr_mat = clr[*] @ basis.T                         # (T, D-1)
```

### 3.2 — Inter-step Aitchison distances

```
For t in 1..T-1:
    d_step[t] = sqrt( sum_j (clr[t][j] - clr[t-1][j])^2 )
d_step[0] = 0.0
```

### 3.3 — Pairwise distance matrix

```
For a in 0..T-1:
    For b in 0..T-1:
        d_mat[a, b] = sqrt( sum_j (clr[a][j] - clr[b][j])^2 )
```

### 3.4 — Navigation metrics (System Course Plot)

```
h_start          = clr[0]
h_final          = clr[T-1]
V_net            = h_final - h_start
net_distance     = || V_net ||              (Euclidean norm of V_net)
path_length      = sum over t of d_step[t]
course_directness = net_distance / path_length     (∈ [0, 1])
                                              1.0 ⇒ straight S→F line
                                              0.0 ⇒ pure looping
dynamic_range_S  = max(h_start) - min(h_start)
dynamic_range_F  = max(h_final) - min(h_final)
```

### 3.5 — System Course Plot projection (Math Handbook Ch 15)

```
X = clr - row_mean(clr)                     # T × D, centred
SVD: X = U S V^T                            # principal-component decomposition
PC1 = (U[:, 0] * S[0])                      # T × 1, first principal coord
PC2 = (U[:, 1] * S[1])                      # T × 1, second principal coord
var_explained_PC1 = S[0]^2 / sum(S^2)
var_explained_PC2 = S[1]^2 / sum(S^2)
```

### 3.6 — Bearing aggregates

```
For t in 0..T-1:
    bearings[t, k]  = θ_ij at timestep t for carrier-pair index k
    where the k-index iterates over combinations(D, 2) in lex order

mean_theta[t] = mean over k of bearings[t, k]   (ignoring NaN)
```

### 3.7 — Helmsman frequency + transition matrix

```
For each carrier c:
    helmsman_count[c] = # of t with helmsman[t] == c

For each (a, b) carrier pair:
    transition[a, b] = # of t such that helmsman[t] == a AND helmsman[t+1] == b
```

### 3.8 — Pair Pearson r matrix

```
R = identity D × D
For each entry p in stages.stage2.higgins_extensions.carrier_pair_examination:
    R[p.i, p.j] = R[p.j, p.i] = p.pearson_r
```

### 3.9 — Pairwise divergence ranking

```
candidates = []
For a in 0..T-1:
    For b in a+1..T-1:
        candidates.append( (a, b, d_mat[a, b]) )
candidates.sort(key=descending d)
top_15 = candidates[0:15]
```

### 3.10 — Compositional Bearing Scope (CBS) — three orthogonal faces (Math Handbook Ch 16)

```
For each timestep t:
    plot point on:
        face XY:  x = mean_theta[t],  y = d_step[t]
        face XZ:  x = mean_theta[t],  y = metric_trace[t]   (log)
        face YZ:  x = d_step[t],      y = metric_trace[t]   (log)
    colour by t (early = dark, late = bright)
```

---

## 4 — Plates emitted

The locked Stage 2 atlas emits 19 plates in this fixed order:

```
01  Cover + declaration
02  System Course Plot (PCA 2D path, S/F markers, V_net arrow)
03  Hs trajectory line plot
04  Aitchison-norm trajectory line plot
05  ILR axes 1-3 trajectories overlaid
06  Polar bearing rose at 4 sample timesteps
07  Bearing heatmap T × C(D,2) pairs
08  ω angular velocity trajectory
09  Metric tensor trace + condition number (two-panel line)
10  Helmsman σ lineage timeline (categorical strip)
11  Helmsman frequency + transition matrix + per-year displacement
12  Ring class strip + Hs trajectory
13  Lock event timeline (carrier × t)
14  Variation matrix τ_ij heatmap
15  Pair Pearson r heatmap + co-movement scatter
16  Compositional Bearing Scope (CBS) — three orthogonal faces
17  Pairwise divergence — distance matrix + top-15 ranking
18  ω vs Hs scatter
19  Stage 2 numeric summary
```

Page count = 19 regardless of T or D. Plate order is fixed; viewers
should not re-order. Footer on every page declares method tag and
order. Page 1 and 19 carry the source SHA, content SHA, and engine
version explicitly.

---

## 5 — Output format

A single PDF document, landscape Letter (11 × 8.5 inch).
Provenance footer on every page. Same FIXED-scale conventions as
Stage 1.

The matplotlib backend embeds a creation timestamp in PDF metadata,
so the PDF SHA-256 is not byte-deterministic across runs. The
underlying CNT JSON `content_sha256` is. v1.1 Feature A
(deterministic PDF backend) closes that gap.

---

## 6 — Determinism

Stage 2 is a pure function of the input JSON. Same JSON ⇒ same
plates, same numeric values to within IEEE float printing precision.
The matplotlib float-formatting uses default precision for tick
labels; the underlying data is not affected.

---

## 7 — Calibration fixture

`atlas/STANDARD_CALIBRATION_stage2_*` contains a known trajectory whose
navigation metrics can be hand-verified:

* A 6-point straight-line trajectory in CLR space:
  course_directness = 1.000 exactly.
* A 7-point closed-loop trajectory returning to origin:
  V_net = 0, course_directness = 0.

Re-running `atlas/standard_calibration_stage2.py` regenerates both
fixtures byte-identically.

---

*Stage 2 reads. The expert decides. The navigation metrics are
mathematically deterministic. The plates carry their order on every
page.*
