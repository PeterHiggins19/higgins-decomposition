# Higgins Computational Instruments (HCI)

## Purpose

Pure mathematical discovery instruments derived from the Higgins Decomposition.
This folder contains proofs, corollaries, instrument specifications, and method
definitions only. No data. No domain interpretation. No colour.

## Instrument Naming

### The Compositional Bearing Scope (CBS)

The cube face projection instrument is named the **Compositional Bearing Scope**.
It is an oscilloscope-class instrument that displays compositional trajectory
on calibrated sweep axes.

| Property | Value |
|----------|-------|
| Full name | Higgins Compositional Bearing Scope |
| Abbreviation | CBS |
| Class | Oscilloscope-style sweep display |
| Vertical axis | Full range [0, 1] (Higgins Scale) or CLR magnitude |
| Horizontal axis | Full sweep [0, 360] degrees (polar bearing) |
| Display mode | Cartesian trace with symbol markers |
| Colour | None. 8-bit monochrome. 32-level grayscale only |

### Tensor Engine: Compositional Navigation Tensor (CNT)

The pure mathematical core is the **Compositional Navigation Tensor**.

The CNT computes, from any closed composition x in the D-simplex:

```
CNT(x) = (theta, omega, kappa, sigma)
```

where:

```
theta  : S^{D-1} --> [0, 2*pi)^{D choose 2}    Bearing tensor
omega  : S^{D-1} x S^{D-1} --> R^+              Angular velocity scalar
kappa  : S^{D-1} --> R^{D x D}                  Steering sensitivity tensor
sigma  : S^{D-1} --> {1, ..., D}                 Helmsman index
```

### Derivation from First Principles

**Definition 1 (Bearing).** Let x in S^D be a closed composition with CLR
transform h = clr(x). For any pair of carriers (i, j), the pairwise bearing is:

```
theta_{ij}(x) = atan2(h_j, h_i)
```

This is the angle from carrier i toward carrier j in the CLR plane spanned
by dimensions i and j. The full bearing tensor collects all D(D-1)/2 pairwise
bearings.

**Definition 2 (Angular Velocity).** Let x(t) and x(t+1) be consecutive
compositions with CLR transforms h(t) and h(t+1). The angular velocity in
full D-dimensional CLR space is:

```
omega(t, t+1) = atan2( ||h(t) x h(t+1)||, <h(t), h(t+1)> )
```

where ||h₁ x h₂||² = ||h₁||²·||h₂||² - ⟨h₁,h₂⟩² (Lagrange identity,
valid in all D). This is the angle between the two CLR direction vectors.
It measures total heading change across ALL carriers simultaneously.

Note: The atan2 form replaces the original arccos formulation. Both are
mathematically equivalent, but atan2 eliminates up to 8 digits of precision
loss near 0° and 180° (see CNT_PRECISION_DIAGNOSTIC.md, experiment P03).

**Definition 3 (Higgins Steering Metric Tensor).** The full Aitchison
pullback metric tensor on the simplex is:

```
kappa^Hs_ij(x) = (delta_ij - 1/D) / (x_i * x_j)
```

In matrix form:

```
kappa^Hs(x) = diag(1/x) * P * diag(1/x)
P = I - (1/D) * 1 * 1^T
```

The diagonal elements kappa^Hs_jj(x) = (1 - 1/D) / x_j^2 govern
single-carrier sensitivity. The off-diagonal elements kappa^Hs_ij(x) =
-1 / (D * x_i * x_j) govern inter-carrier metric coupling.

The repo's existing quantity 1/x_j is the **diagonal steering sensitivity**
— a readout from the metric tensor, not the tensor itself.

Mathematical lineage: Aitchison (1986) simplex geometry, Egozcue et al.
(2003) ILR metric structure, Higgins (2026) steering metric tensor in
CNT/HCI instrument.

**Definition 4 (Dominant Carrier Displacement Index / Helmsman Index).**
Between consecutive compositions x(t) and x(t+1), the Dominant Carrier
Displacement Index identifies the carrier with maximum CLR displacement:

```
sigma^Hs(t, t+1) = argmax_j |h_j(t+1) - h_j(t)|
```

Formal name: **Dominant Carrier Displacement Index (DCDI)**
HCI instrument alias: **Helmsman Index**

The selected carrier sigma^Hs is the Helmsman: the carrier channel
responsible for the largest local displacement in Higgins Coordinate space.


## Corollaries

**Corollary 1 (Bearing Determinism).** The bearing theta_{ij} is a
deterministic, closed-form function of the composition. Same composition,
same bearing. No parameters, no fitting, no model selection.

**Corollary 2 (Steering Asymmetry).** For any composition x with
max(x) / min(x) = R, the ratio of minimum to maximum steering sensitivity
is R. The rarest carrier has R times the steering authority of the most
abundant carrier.

**Corollary 3 (Lock Detection).** Two carriers (i, j) are informationally
locked when their pairwise bearing theta_{ij} varies less than epsilon
across T observations:

```
max_t(theta_{ij}(t)) - min_t(theta_{ij}(t)) < epsilon
```

Locked carriers move as a single compositional mode. Their ratio is
approximately constant regardless of absolute magnitude changes.

**Corollary 4 (Bearing Reversal).** A sign change in theta_{ij} from
positive to negative (or vice versa) indicates a structural crossover:
carrier j transitions from above to below its geometric-mean share
relative to carrier i, or vice versa.

**Corollary 5 (Infinite Helm).** When carrier j approaches zero fraction,
g_{jj} --> infinity. Any nonzero change in carrier j dominates the angular
velocity. A vanishing carrier has infinite steering authority — its
disappearance forces the largest compositional rotation.


## Display Standard

### Symbology (8-bit ASCII only)

| Symbol | Meaning |
|--------|---------|
| . | Data point (normal) |
| o | Data point (highlighted) |
| * | Helmsman carrier at this timestep |
| + | Barycenter / origin marker |
| x | Lock point (carrier fraction = 0) |
| - | Horizontal axis |
| \| | Vertical axis |
| # | Grid intersection |
| = | Bearing lock band (epsilon corridor) |
| ~ | Angular velocity threshold exceeded |
| ^ | Bearing reversal event |
| > | Trajectory direction arrow |

### Grayscale Palette (32 levels)

```
Level 0:  ████  (0/31)   = black   = maximum signal
Level 8:  ░░░░  (8/31)   = dark    = strong signal
Level 16: ▒▒▒▒  (16/31)  = mid     = moderate signal
Level 24: ▓▓▓▓  (24/31)  = light   = weak signal
Level 31:       (31/31)  = white   = background / no signal
```

In practice for ASCII output:
```
@ = level 0-3   (black)
# = level 4-7   (very dark)
8 = level 8-11  (dark)
o = level 12-15 (medium dark)
: = level 16-19 (medium)
. = level 20-23 (light)
- = level 24-27 (very light)
  = level 28-31 (white / empty)
```

### Oscilloscope Display Format

The CBS displays two Cartesian traces:

**Trace 1 — XZ Face (Bearing vs Time)**
```
Horizontal: Time index [0, T-1]
Vertical:   Bearing theta [0, 360] degrees (or [-180, +180])
Symbols:    . for each year, * for helmsman transitions
Grid:       # at 90-degree intervals
```

**Trace 2 — YZ Face (Hs vs Time)**
```
Horizontal: Time index [0, T-1]
Vertical:   Higgins Scale [0.0, 1.0] full sweep
Grid:       # at ring boundaries (0.05, 0.15, 0.30, 0.50, 0.75, 0.95)
Ring labels: Hs-0 through Hs-6 on right margin
```

Both traces share the horizontal time axis. No scale factor — always
display full 0-1 and 0-360 range. The instrument shows the complete
measurement space, not a zoomed view.


## Mathematical Lineage

```
Aitchison (1986)    Closure, CLR transform, Aitchison distance
Shannon (1948)      Entropy H = -sum(x_j * ln(x_j))
Higgins (2025)      Hs = 1 - H/ln(D), ring classification
Higgins (2026)      CNT bearing/velocity/sensitivity/helmsman decomposition
```

All operations are:
- Deterministic (same input, same output)
- Closed-form (no iteration, no optimisation)
- Parameter-free (no tuning, no fitting)
- Scale-invariant (works on any closed composition)
- Domain-agnostic (energy, nuclear, geochemistry, finance, acoustics)


## HCI Staged Analysis Architecture

### Stage 1 — HCI Section Engine

Composition stream → closure S → Higgins Coordinate Λ = CLR →
local metric tensor κ^Hs → section triads → metric ledgers →
morphographic section plates → section cine-deck.

### Stage 2 — HCI Metric Cross-Examination Engine

Stage 1 outputs → grouping → pairwise comparison → carrier pair
cross-examination → section view cross-examination → ranked contrasts.

Methods:
- Group barycenter analysis
- Pairwise group cross-examination
- Carrier pair cross-examination
- Section view cross-examination

### Stage 3 — HCI Higher-Degree Analysis Engine

Pairs → triads → subcompositions → regimes → structural signatures.

Methods:
- Triadic day analysis (metric triangles in CLR space)
- Carrier triad analysis (three-carrier interaction structures)
- Subcomposition degree ladder (k-degree carrier subsets)
- Metric regime detection (time windows with similar metric structure)

Degree ladder:
- D0: Point state
- D1: Temporal increment
- D2: Pairwise contrast (Stage 2)
- D3: Triadic structure (Stage 3)
- Dk: Subcomposition / k-face structure (Stage 3)
- DD: Full simplex structure


## HCI Tensor Terminology Standard

### Core names

| Term | Meaning |
|------|---------|
| HCI | Higgins Compositional Instrument |
| κ^Hs(x) | Higgins Steering Metric Tensor |
| DCDI | Dominant Carrier Displacement Index (formal operator) |
| Helmsman Index | DCDI instrument alias |
| Carrier channel | Processing lane for one compositional component |
| Parallel carrier channels | Multiple carrier channels under shared geometry |
| Metric ledger | Numerical output table (the measurement authority) |
| Morphographic plate | Symbolic visual rendering |
| Section triad | XY + XZ + YZ metric sections at one time index |
| Section atlas | Time-indexed collection of section triads |
| Section cine-deck | PowerPoint/HTML scroll deck of section triads |

### Naming rules

- Use **Dominant Carrier Displacement Index** at first mention
- Use **Helmsman Index** as instrument alias at second mention
- Use **parallel carrier channels** for the processing architecture
- Use **metric ledger** as the numerical authority, never the plates
- Use **section**, not "slice," for scientific terminology


## File Inventory

| File | Description |
|------|-------------|
| HCI_FOUNDATION.md | This file. Pure math proofs, instrument specification, stage architecture |
| hci_cbs.py | Compositional Bearing Scope engine (CBS) with full metric tensor |
| hci_stage2.py | Stage 2 — Metric Cross-Examination Engine |
| hci_stage3.py | Stage 3 — Higher-Degree Analysis Engine |
| hci_test_stage23.py | Stage 2/3 acceptance test suite (10 tests, synthetic data) |
| README.md | Folder purpose and usage |


---

The instrument reads. The expert decides. The loop stays open.
