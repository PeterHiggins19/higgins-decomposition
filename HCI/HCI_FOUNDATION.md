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

**Definition 3 (Steering Sensitivity Tensor).** The diagonal metric tensor
on the simplex is:

```
kappa_{jj}(x) = g_{jj} = 1 / x_j
```

This is the Aitchison metric tensor. Carrier j with fraction x_j has
sensitivity 1/x_j. As x_j --> 0, sensitivity diverges: infinite steering
authority at the simplex boundary.

**Definition 4 (Helmsman Index).** Between consecutive compositions x(t)
and x(t+1), the helmsman is the carrier with maximum CLR displacement:

```
sigma(t, t+1) = argmax_j |h_j(t+1) - h_j(t)|
```

The helmsman is the carrier that turned the wheel most in CLR space.


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


## File Inventory

| File | Description |
|------|-------------|
| HCI_FOUNDATION.md | This file. Pure math proofs and instrument specification |
| hci_cbs.py | Compositional Bearing Scope engine (CBS) |
| README.md | Folder purpose and usage |


---

The instrument reads. The expert decides. The loop stays open.
