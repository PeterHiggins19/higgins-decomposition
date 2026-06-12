# CNT Exploratory — The Compositional Navigation Tensor

A running Q&A building from the tensor itself outward — structure, geometry, transforms, and every viewpoint needed to see the system whole.

## Figures (line art, B&W, large text — see `codawork2026/cnt_presentation/`)

| Figure | File | Shows |
|--------|------|-------|
| Fig. 1a | `slide_01a_pipeline_input.svg` | Raw data -> Closure -> CLR transform (stage 1) |
| Fig. 1b | `slide_01b_theta_omega.svg` | Channel specs: theta (bearing) + omega (angular velocity) |
| Fig. 1c | `slide_01c_kappa_sigma.svg` | Channel specs: kappa_HS (steering) + sigma (helmsman) |
| Fig. 1d | `slide_01d_corollaries_output.svg` | Corollaries + total output (66 measurements from 16 inputs) |
| Fig. 2a | `slide_02a_cube_structure.svg` | CBS cube 3D isometric with XY/XZ/YZ face imagery |
| Fig. 2b | `slide_02b_higgins_axis.svg` | Higgins axis time projection — section cine-deck |
| Fig. 2c | `slide_02c_face_specs.svg` | Three face specifications + info panel contents |
| Fig. 3 | `slide_03_hlr_evidence.svg` | HLR unit family — 7-system k-factors + round-trip evidence |

---

## Q1. What IS the CNT? Show me the structure.

The Compositional Navigation Tensor is a 4-channel instrument reading. Given any closed composition x (a vector of D proportions summing to 1), the CNT produces four simultaneous outputs:

```
CNT(x) = (theta, omega, kappa_HS, sigma)
           |       |       |         |
           |       |       |         +-- WHO moved most (index)
           |       |       +------------ HOW SENSITIVE is each carrier (D x D matrix)
           |       +-------------------- HOW FAST is the heading changing (scalar)
           +---------------------------- WHERE is the system pointing (D(D-1)/2 angles)
```

It is NOT a single number. It is NOT a matrix. It is a **tuple of tensors of different rank** — a composite instrument reading, like a ship's bridge reading (compass + speed + sea-state + helmsman log) all computed from one measurement.

### Structural Skeleton

```
                    x = (x_1, x_2, ..., x_D)
                    |
                    | CLOSURE CHECK: sum = 1
                    v
              h = CLR(x) = ln(x) - mean(ln(x))
                    |
         +----------+----------+-----------+
         |          |          |           |
         v          v          v           v
     theta_ij    omega      kappa_HS     sigma
   [D(D-1)/2    [scalar]   [D x D       [index
    angles]                 matrix]       1..D]
```

Each channel has a different tensor rank:

| Channel | Symbol | Rank | Shape | Unit |
|---------|--------|------|-------|------|
| Bearing tensor | theta | 2 (antisymmetric) | D(D-1)/2 independent | degrees |
| Angular velocity | omega | 0 (scalar) | 1 value | degrees/step |
| Steering metric tensor | kappa_HS | 2 (symmetric) | D x D | HLR^-2 |
| Helmsman index | sigma | 0 (categorical) | 1 index | carrier label |

---

## Q2. What does "CLR" actually do to my data? Show the transform.

The Centred Log-Ratio transform takes a closed composition and maps it to an unconstrained coordinate space. This is the ONLY entry point to the CNT — everything flows from CLR.

### The Transform Chain (Scale Provenance)

```
RAW DATA        CLOSURE         CLR COORDINATE       CNT CHANNELS
                                (Higgins Space)
Y_j(t)   -->   x_j = Y_j/T   -->   h_j = ln(x_j) - (1/D) sum_k ln(x_k)   -->   (theta, omega, kappa_HS, sigma)
  |               |                       |
  |               |                       |
absolute        proportion              log-ratio displacement
counts          on simplex              from geometric barycentre
```

### What CLR does geometrically

The simplex S^D (the space where proportions live) is a D-1 dimensional surface embedded in D-space. CLR "unfolds" this curved surface into a flat coordinate system:

```
SIMPLEX (curved, constrained)          CLR SPACE (flat, unconstrained*)
                                       
     x_1 + x_2 + x_3 = 1                    h_1 + h_2 + h_3 = 0
                                       
        . (apex x_3=1)                         +h_3
       / \                                      |
      /   \                                     |
     / . P \          CLR           ------+------  h_1
    /       \        ----->                |
   /_________\                             |
 x_1=1    x_2=1                           +h_2
                                       
   * lives on sum=0 hyperplane
```

The constraint changes from "proportions sum to 1" to "coordinates sum to 0." This is crucial — it means h lives in a (D-1)-dimensional hyperplane through the origin.

### Key properties of CLR

- **Barycentre = origin**: The geometric mean composition maps to h = (0, 0, ..., 0)
- **Positive h_j**: Carrier j is ABOVE its geometric-mean share
- **Negative h_j**: Carrier j is BELOW its geometric-mean share
- **Large negative h_j**: Carrier j is near zero (approaching absence)
- **Sum constraint**: h_1 + h_2 + ... + h_D = 0 always (redundancy — only D-1 are free)

### Unit: HLR (Higgins Log-Ratio Level)

The CLR values are measured in HLR — a dimensionless natural-log ratio unit. Its nearest relative in the log-level family is the neper.

```
1 HLR = one natural-log ratio unit of displacement from the barycentre
      = a factor of e (~2.718) change in the carrier's share relative to the geometric mean
```

---

## Q3. How does the BEARING tensor work? Show me the geometry.

The bearing tensor theta answers: "from carrier i's perspective, where is carrier j?"

### Definition

```
theta_ij(x) = atan2(h_j, h_i)
```

This is the angle in the 2D plane spanned by CLR dimensions i and j. It tells you the direction FROM carrier i TOWARD carrier j in log-ratio space.

### Geometric Picture (D=3, three carriers)

```
                    h_2 (carrier 2 axis)
                     |
                     |     . P = (h_1, h_2)
                     |    /
                     |   /
                     |  /  theta_12 = angle from h_1 axis to point P
                     | / )
        -------------|/----------  h_1 (carrier 1 axis)
                     |
                     |
```

For D=3 carriers, you get D(D-1)/2 = 3 bearings: theta_12, theta_13, theta_23. Each is an angle in a different 2D slice of CLR space.

### For D=8 (Japan EMBER): 28 bearings

With 8 carriers, you get 8*7/2 = 28 pairwise bearings. Each bearing is an independent directional measurement:

```
Carrier pairs:  (1,2), (1,3), (1,4), ..., (7,8)
                 28 independent angles
                 
Think of it as: 28 compass readings, each one measuring the relative
               bearing between two specific carriers in CLR space.
```

### What bearings TELL you

| Bearing value | Meaning |
|---------------|---------|
| theta_ij = 0 deg | Carrier j is pure-positive in this plane (j dominates, i at geometric mean) |
| theta_ij = 90 deg | Both carriers displaced equally above their means |
| theta_ij = +/-180 deg | Carrier j is directly opposite to i (one up, one down maximally) |
| theta_ij near constant | Carriers i and j are LOCKED — moving together (constant ratio) |

### Bearing Reversal

When theta_ij crosses zero, it means the structural ordering between carriers i and j has FLIPPED. One has overtaken the other relative to the geometric mean. This is a genuine structural crossover event.

---

## Q4. What is angular velocity omega? The single number that captures total heading change.

### Definition

```
omega(t, t+1) = atan2( ||h(t) x h(t+1)||, <h(t), h(t+1)> )

where:
  h(t)         = full D-dimensional CLR vector at time t
  <.,.>        = dot product (inner product)
  ||h1 x h2||  = magnitude of generalised cross product
               = sqrt( ||h1||^2 * ||h2||^2 - <h1,h2>^2 )   [Lagrange identity]
```

### Geometric Picture

```
                  h(t+1)
                 /
                /
               / ) omega = angle between
              /  )        the two direction vectors
             /   )
            ----------- h(t)
            
            origin (barycentre)
```

Omega is the angle between consecutive CLR vectors measured in the FULL D-dimensional space. It doesn't care which carriers moved — it captures the TOTAL heading change of the entire composition simultaneously.

### Why atan2, not arccos?

Both formulas give the same answer mathematically, but:
- **arccos** loses 8 digits of precision near 0 deg and 180 deg (derivative goes to infinity)
- **atan2** maintains full precision everywhere (stable at all angles)

This was verified in CNT precision diagnostics (experiment P03).

### What omega TELLS you

| omega value | System behaviour |
|-------------|-----------------|
| 0 deg | No heading change — system drifting in same direction |
| 1-5 deg | Normal drift — gradual compositional evolution |
| 10-30 deg | Significant course change — structural shift |
| 50+ deg | Massive reorientation (Japan 2014: omega = 66 deg post-Fukushima) |
| 180 deg | Perfect reversal — heading exactly opposite to previous step |

### Bounds

omega is in [0, 180] degrees — always positive (it's an angle between vectors, not a signed quantity). This is a mathematically exact bound (atan2 guarantee).

---

## Q5. The Higgins Steering Metric Tensor — kappa_HS. This is the deep one.

### Definition

```
kappa_HS_ij(x) = (delta_ij - 1/D) / (x_i * x_j)
```

In matrix form:

```
kappa_HS(x) = diag(1/x) * P * diag(1/x)

where P = I - (1/D) * 1 * 1^T   (the centring matrix)
```

### What it IS

kappa_HS is the **Aitchison metric tensor pulled back to the simplex**. It tells you the local geometry of composition space — how "far" a small change in one carrier actually moves the system in Aitchison distance.

Think of it as the **curvature map of the simplex**. Near the edges (where carriers are small), the space is "stretched" — tiny changes in proportion correspond to large metric distances. Near the centre (all carriers equal), the space is "flat" — proportional changes map linearly to metric displacement.

### 3D Spatial Visualisation

```
METRIC WARPING NEAR SIMPLEX BOUNDARY
(showing how kappa_HS stretches space near rare carriers)

         SIMPLEX INTERIOR               SIMPLEX EDGE (x_j -> 0)
         (all carriers ~equal)           (one carrier vanishing)
         
          . . . . . . .                     .  .  .  .  .
          . . . . . . .                      .   .   .   .
          . . . . . . .                       .    .    .    .
          . . . . . . .                        .     .     .
          . . . . . . .                         .      .      .
          
         even grid spacing              stretched grid spacing
         kappa_HS ~ I (identity)        kappa_HS_jj ~ 1/x_j^2 (huge)
```

### Diagonal elements (carrier sensitivity)

```
kappa_HS_jj(x) = (1 - 1/D) / x_j^2
```

This is the **self-sensitivity** of carrier j. When x_j is small (rare carrier), kappa_jj is HUGE — meaning any small change in that carrier produces enormous metric displacement.

Example (Japan EMBER, D=8):

```
Coal (x ~ 0.30):  kappa_jj ~ (7/8) / 0.09  =  9.7
Nuclear (x ~ 0.01): kappa_jj ~ (7/8) / 0.0001 = 8750

Nuclear is ~900x more metrically sensitive than Coal
```

### Off-diagonal elements (inter-carrier coupling)

```
kappa_HS_ij(x) = -1 / (D * x_i * x_j)     (i != j)
```

The negative sign means carriers are **anti-correlated** in the metric — when one moves up, the closure constraint forces others down. The coupling is strongest between two rare carriers (both x_i and x_j small).

### The key insight: STEERING ASYMMETRY (Corollary 2)

```
max(kappa_jj) / min(kappa_jj) = R^2

where R = max(x) / min(x) = compositional range
```

For Japan EMBER: R ~ 30 (Coal ~30% vs Nuclear post-Fukushima ~1%), so steering asymmetry = ~900. The rarest carrier has 900x the steering authority. This is why Nuclear dominates the helmsman readings around 2011-2015.

### Physical Analogy: The Rubber Sheet

Imagine the simplex as a rubber sheet:

```
                    FLAT REGION
                   (centre, all ~equal)
                   
       ___________/____________\___________
      /                                    \
     /           gentle slopes              \
    /                                        \
   |     gradually steepening                 |
   |                                          |
   |         STEEP WALLS                      |
   |         (edges, rare carriers)           |
    \                                        /
     \_______________________________________/
     
     The metric tensor MEASURES this curvature:
     - Centre: kappa ~ I (flat, isotropic)
     - Edge:   kappa_jj -> infinity (infinitely steep wall)
```

Rolling a marble on this surface: near the centre it rolls lazily (low sensitivity). Near an edge, the slightest push sends it rocketing down the steep wall (high sensitivity). kappa_HS tells you the slope at every point.

---

## Q6. Helmsman sigma — who's steering the ship?

### Definition

```
sigma(t, t+1) = argmax_j |h_j(t+1) - h_j(t)|
```

The carrier with the largest absolute CLR displacement between time steps.

### What it IS

The simplest channel — a categorical output. At each time step, ONE carrier is responsible for the largest share of the system's movement. That carrier is the **Helmsman**.

```
TIME SERIES OF HELMSMAN:

2000  2001  2002  2003  ...  2011  2012  2013  2014  2015  ...  2025
 ---  Wind  Wind  Wind       Nuc   Nuc   Sol   NUC   NUC        Bio
                                                ^^^   ^^^
                              STRUCTURAL CRISIS: Nuclear dominates
                              because its CLR displacement is massive
                              (composition going from 30% to ~0%)
```

### Connection to kappa_HS

The helmsman is determined by kappa_HS! A carrier with large kappa_jj (high metric sensitivity) needs only a tiny proportional change to produce a large CLR displacement. So:

```
Rare carrier + small change = LARGE |delta h_j| = likely helmsman
Common carrier + large change = moderate |delta h_j| = possibly helmsman

The metric tensor PREDICTS who will steer. The helmsman CONFIRMS who did.
```

### Infinite Helm (Corollary 5)

When x_j approaches 0, kappa_jj approaches infinity. Any nonzero change in carrier j produces infinite metric displacement. A vanishing carrier has **infinite steering authority** — its disappearance forces the largest compositional rotation.

This is not a pathology. It is genuine physics: when Nuclear shuts down in Japan (2011-2014), the entire energy system rotates massively because one structural pillar disappeared.

---

## Q7. How do the four channels FLOW together? The complete transform pipeline.

### Full Data Flow (D=8, Japan EMBER)

```
RAW ELECTRICITY DATA (TWh by source, 26 years)
    |
    | Y = [Coal, Gas, Oil, Nuclear, Hydro, Wind, Solar, Bioenergy] x 26 years
    |
    v
CLOSURE: x_j(t) = Y_j(t) / sum_k Y_k(t)
    |
    | x lives on the 7-simplex S^7 (8 proportions summing to 1)
    |
    v
CLR TRANSFORM: h_j(t) = ln(x_j(t)) - (1/8) sum_k ln(x_k(t))
    |
    | h lives on the sum=0 hyperplane in R^8
    | h_1 + h_2 + ... + h_8 = 0
    |
    +----------+-----------+-----------+
    |          |           |           |
    v          v           v           v
  THETA      OMEGA      KAPPA_HS    SIGMA
    |          |           |           |
    |          |           |           |
  28 angles  1 scalar   8x8 matrix  1 index
  (bearings) (heading   (local       (who
   between    change     curvature)   steered)
   all pairs  rate)
```

### Temporal Dependencies

```
REQUIRES 1 TIME POINT:          REQUIRES 2 CONSECUTIVE POINTS:
   theta(t)                        omega(t, t+1)
   kappa_HS(t)                     sigma(t, t+1)
   
   These are INSTANTANEOUS         These are INCREMENTAL
   (snapshot of state)              (change between states)
```

### Output Dimensions (D=8)

```
Per time step, the CNT produces:
  - 28 bearing values        (upper triangle of 8x8 antisymmetric)
  - 1 angular velocity       (scalar)
  - 64 metric tensor entries (8x8 symmetric, but only 36 independent due to symmetry)
  - 1 helmsman index         (categorical)
  
  Total independent numbers: 28 + 1 + 36 + 1 = 66 per time step
  From D=8 composition at 2 time points (16 numbers input)
```

The CNT is a **dimensionality EXPANDER** — it takes 8 proportions and reveals 66 independent measurements about the system's navigational state.

---

## Q8. Multiple viewpoints — seeing the same tensor from different disciplines.

### Viewpoint 1: Physicist (Differential Geometry)

"The CNT is a connection on the statistical manifold S^D. The metric tensor kappa_HS is the Fisher-Rao metric restricted to multinomial distributions on the simplex. The bearings are parallel transport angles. Angular velocity is geodesic curvature. The helmsman is the direction of maximum sectional curvature."

Key insight: The simplex is a curved Riemannian manifold. kappa_HS IS the metric — it defines distance, angles, volumes, and curvature everywhere.

### Viewpoint 2: Navigator

"CNT is a ship's instrument panel. theta is the compass (28 compass readings for all pairwise headings). omega is the rate-of-turn indicator. kappa_HS is the sea chart (how 'close' you are to dangerous shoals — rare carriers = rocks). sigma is the wheel — who's actually turning the ship."

Key insight: Navigation is the natural metaphor because the tensor literally computes bearing, velocity, local geometry (chart), and steering (helm).

### Viewpoint 3: Audio Engineer

"Each carrier is a frequency band. CLR is the spectrum analyser reading in dB (log-power relative to mean). theta is phase relationship between bands. omega is spectral flux (how fast the spectrum is changing). kappa_HS is the sensitivity curve (how loud each band sounds per unit of power change — like Fletcher-Munson curves). sigma is which band is currently dominating the spectral motion."

Key insight: HLR units are essentially decibels (both are log-ratios). The entire CNT framework maps onto spectral analysis.

### Viewpoint 4: Data Scientist

"CNT is a feature extraction pipeline for compositional time series. It takes D proportions and extracts: (a) all pairwise angular features, (b) a global rate-of-change scalar, (c) a full local covariance structure (the metric), and (d) a categorical label for the dominant mover. It's a complete sufficient statistic for navigational state."

Key insight: The 66 numbers per time step are an over-complete representation — they contain MORE geometric information than the original 8 proportions, because they explicitly expose relationships that are only implicit in the raw data.

### Viewpoint 5: Chemist (Compositional Analysis)

"CLR is my log-ratio of chemical activities. theta tells me which species are co-varying (reaction stoichiometry). omega tells me how fast the reaction mixture is evolving. kappa_HS tells me which species are near their detection limit (infinite sensitivity = approaching zero concentration). sigma tells me which species is driving the current reaction step."

---

## Q9. The 3D Structure — visualising CLR space for D=3.

For D=3 carriers, CLR space is a 2D plane (sum=0 constraint reduces 3D to 2D). This is the simplest case to visualise completely:

```
3D AMBIENT SPACE (h_1, h_2, h_3)
         h_3
          |
          |   sum=0 plane
          |  /
          | /  . CLR point lives HERE
          |/   |
    ------+---------- h_1
         /|    |
        / |    v
       /  |  (projected down to 2D for display)
     h_2  |

The sum=0 plane passes through the origin at 45 degrees to all axes.
ALL CLR points live on this 2D plane.
```

### Bearing in D=3

With 3 carriers, there are 3 bearings: theta_12, theta_13, theta_23. Each is the angle in a different coordinate plane:

```
      h_2
       |     P = (h_1, h_2)
       |    *
       |   /
       |  /  theta_12
       | /)
  -----+---------  h_1
       |
```

### The path through time

A time series of compositions traces a PATH through CLR space. For D=3, this path lives on the sum=0 plane — you can draw it as a 2D curve:

```
    h_2
     |        2003
     |       /
     |  2002/     2004
     |    | /    /
     |    |/    /
     | 2001   2005
     |  /    /
     | / 2000     path of composition through CLR space
     |/           over time
  ---+---------- h_1
     |
```

The System Course Plot in the Stage 1 PDF is exactly this — projected from D-dimensional CLR space to 2D using PCA.

---

## Q10. For D=8 (real case) — how to visualise the high-dimensional structure?

The full CLR space for D=8 carriers is 7-dimensional (sum=0 hyperplane in R^8). We cannot draw this directly. Three strategies:

### Strategy 1: Section Plates (HCI Stage 1)

Project the full 7D structure onto three orthogonal 2D faces:

```
FULL 7D CLR SPACE
       |
       +--- XY face: scatter of h_i vs h_j for chosen pair (plan view)
       |
       +--- XZ face: bar chart of all 28 bearings (bearing view)
       |
       +--- YZ face: bar chart of all 8 CLR values (profile view)
```

Each face shows a different 2D "shadow" of the full structure. Like X-ray, CT, MRI — different projections of the same 3D object.

### Strategy 2: PCA Course Plot (System Course Plot)

Find the 2D plane that captures the MOST variance in the CLR path:

```
7D CLR path (26 time points)
       |
       | PCA: find top-2 eigenvectors of covariance
       v
2D projection that preserves maximum structure

     PC2
      |        F (2025)
      |       /
      |      /
      |     /   <-- net displacement vector
      |    /
      | S (2000)
      |
  ----+---------- PC1
      |
```

### Strategy 3: Channel-by-Channel Time Series

Plot each CNT channel against time independently:

```
theta_ij(t) vs t   -- 28 traces, shows bearing evolution
omega(t) vs t      -- 1 trace, shows heading-change rate  
kappa_jj(t) vs t   -- 8 traces, shows sensitivity evolution
sigma(t) vs t      -- categorical, shows helmsman sequence
```

This loses the spatial geometry but reveals temporal patterns clearly.

---

## Q11. How does information flow FROM kappa_HS TO sigma?

The metric tensor doesn't just describe geometry — it PREDICTS the helmsman:

```
HIGH kappa_jj (rare carrier, high sensitivity)
       |
       | Any small proportional change delta_x_j
       |
       v
LARGE metric displacement: |delta h_j| ~ (1/x_j) * |delta x_j|
       |
       | Compare across all carriers
       |
       v
HELMSMAN = argmax_j |delta h_j|
       |
       v
The carrier with the highest PRODUCT of (sensitivity * raw change) wins
```

### The Steering Equation

```
delta h_j = (1/x_j) * delta x_j - (1/D) * sum_k (1/x_k) * delta x_k

Simplification for dominant carrier:
|delta h_j| ~ |delta x_j| / x_j = RELATIVE change in carrier j

So the helmsman is approximately: argmax_j |delta x_j / x_j|
= the carrier with the largest RELATIVE (not absolute) change
```

This is why Nuclear dominates 2011-2014: its relative change is enormous (going from 30% to nearly 0%).

---

## Q12. Locks — when bearings reveal structural rigidity.

### Definition (Corollary 3)

Two carriers (i,j) are **informationally locked** when:

```
max_t(theta_ij(t)) - min_t(theta_ij(t)) < epsilon   (typically 10 deg)
```

Their bearing barely changes across the entire observation window.

### What a lock MEANS

```
LOCKED CARRIERS: theta_ij ~ constant

This means: h_j / h_i ~ constant ratio at all times
         => x_j / x_i ~ constant ratio at all times (exponentiate)
         => Carriers move in proportion — they are a SINGLE MODE

Physical interpretation: these two carriers are driven by the same
underlying force and cannot be distinguished navigationally.
```

### Lock Detection in Japan EMBER

If Wind and Solar are locked (hypothetical), it means renewable growth is a single structural mode — you can't navigate them independently. They move together regardless of what else happens.

---

## Summary — The Complete Picture

```
COMPOSITION x (D proportions, sum=1)
        |
        | CLR transform (ln-ratio from geometric mean)
        v
HIGGINS COORDINATE h (D values, sum=0, measured in HLR)
        |
        +---> THETA: 28 pairwise angles (WHERE each carrier points)
        |
        +---> OMEGA: scalar heading change (HOW FAST the system turns)
        |
        +---> KAPPA_HS: D x D metric (HOW SENSITIVE the space is locally)
        |              |
        |              +---> diagonal: per-carrier steering sensitivity
        |              +---> off-diagonal: inter-carrier coupling
        |              +---> Corollary 2: rare carriers dominate steering
        |              +---> Corollary 5: vanishing carrier -> infinite helm
        |
        +---> SIGMA: argmax displacement (WHO steered this step)

TEMPORAL CHAIN:
  x(t) -> h(t) -> theta(t), kappa_HS(t)       [instantaneous]
  h(t), h(t+1) -> omega(t,t+1), sigma(t,t+1)  [incremental]

INVARIANTS:
  - Deterministic (no parameters, no randomness)
  - Closed-form (no iteration)
  - Scale-invariant (absolute values don't matter, only proportions)
  - Domain-agnostic (works for energy, chemistry, finance, ecology...)
```

---

## Q13. The CBS Cube — Three Orthogonal Face Projections in 3-Space

The CBS (Compositional Bearing Scope) IS a cube. Each section plate shows three faces of that cube simultaneously — three orthogonal projections of the full CLR state, frozen at one instant.

### The Cube in 3-Space

```
                         θ (bearing axis, vertical)
                         |
                         |        ┌────────────────┐
                         |       /│   XZ FACE      /│
                         |      / │  (bearings)   / │
                         |     /  │  28 bars     /  │
                         |    ┌────────────────┐   │
                         |    │   │            │   │
                         |    │   │   INTERIOR │   │   ← The full D-dimensional
                         |    │   │   (CLR     │   │     state lives INSIDE
                         |    │   │    space)  │   │     this cube
                         |    │   │            │   │
                         |    │   └────────────│───┘
                         |    │  /  XY FACE    │  /
                         |    │ /  (scatter)   │ /
                         |    │/   plan view   │/
                         |    └────────────────┘
                         |         
              ───────────+──────────────────────── h_i (CLR carrier i)
                        /
                       /
                      /
                     h_j (CLR carrier j)
                     
              THREE VISIBLE FACES:
              ┌──────────┐
              │ XY (bot) │ = CLR scatter, plan view from above
              │ XZ (top) │ = Bearing bars, seen from front
              │ YZ (rgt) │ = CLR profile bars, seen from side
              └──────────┘
```

### What Each Face Shows

| Face | Axes | Content | Fixed Scale |
|------|------|---------|-------------|
| **XY** (plan view) | h_i vs h_j | Scatter of all carriers in CLR space | [CLR_min, CLR_max] both axes |
| **XZ** (bearing view) | pair index vs θ | Bar chart of all D(D-1)/2 bearings | [-180°, +180°] exact |
| **YZ** (profile view) | carrier vs h_j | Bar chart of D CLR values | [CLR_min, CLR_max] |

### The Key Insight: Fixed Graticule

All three faces have LOCKED scales — the same axis limits on every plate. This is what makes the cube an instrument rather than a chart:

```
OSCILLOSCOPE ANALOGY:
- The graticule (grid) NEVER moves
- Only the trace (data) moves
- Your eye detects motion against the fixed backdrop

CBS CUBE:
- The cube frame NEVER changes between plates
- Only the bar heights and scatter positions change
- Scrolling the cine-deck reveals genuine compositional motion
```

---

## Q14. Projection in Time Along the Higgins Axis — The Cine-Deck

The cube exists at ONE time point. To see the system evolve, you project the cube ALONG the time axis — the Higgins Axis.

### The Time Projection

```
     t=0        t=1        t=2        t=3              t=N
      │          │          │          │                │
      ▼          ▼          ▼          ▼                ▼
   ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐          ┌─────┐
   │ XY  │   │ XY  │   │ XY  │   │ XY  │   · · ·  │ XY  │
   │ XZ  │   │ XZ  │   │ XZ  │   │ XZ  │          │ XZ  │
   │ YZ  │   │ YZ  │   │ YZ  │   │ YZ  │          │ YZ  │
   └─────┘   └─────┘   └─────┘   └─────┘          └─────┘
      │          │          │          │                │
      └──────────┴──────────┴──────────┴────────────────┘
                              │
                    HIGGINS AXIS (time sweep)
                    
   Each plate = one time-slice of the cube
   The full stack = the cine-deck
   Scrolling = sweeping along the Higgins axis
```

### How Faces Emanate From the Cube Along Time

Each cube face generates a CONTINUOUS SURFACE when swept along time:

```
                    ┌─────────────────────────────────────────┐
                   /│                                         /│
    XZ SURFACE    / │   Bearing evolution surface            / │
   (top face    /  │   θ_ij(t) for all pairs              /  │
    swept)     /   │                                     /   │
              ┌─────────────────────────────────────────┐    │
              │    │                                    │    │
              │    │    THE VOLUME                      │    │
              │    │    (full CLR state × time)         │    │
              │    │                                    │    │
    YZ SURFACE│    └───────────────────────────────────│────┘
   (right face│   /                                    │   /
    swept)    │  /     XY SURFACE                      │  /
              │ /      (plan view swept)               │ /
              │/       h_i(t) vs h_j(t)               │/
              └─────────────────────────────────────────┘
                         ──────────────────────────────→
                              t (Higgins Axis)
```

The XY face swept in time traces a **trajectory surface** — the path of all carriers through CLR space as time advances. This is what the System Course Plot captures in 2D projection.

The XZ face swept in time traces a **bearing evolution surface** — 28 bearing traces evolving over all years. Constant bearings (horizontal traces) = locked pairs. Sudden jumps = structural transitions.

The YZ face swept in time traces a **profile evolution surface** — each carrier's CLR level changing year by year. Large negative excursions = carrier approaching zero.

### The Section Plate = Cross-Section of the Volume

```
FULL VOLUME (all data × all time)
         │
         │  Slice at t = t_k
         ▼
┌──────────┬──────────┬──────────────────┐
│  Info    │  Legend  │  XZ Bearings bar │
├──────────┴──────────┼──────────────────┤
│  XY Scatter         │  YZ CLR bar      │
└─────────────────────┴──────────────────┘
         │
         │  This IS the Higgins tensor data field layout v1.0
         │  One section plate = one cross-section of the volume at time t_k
```

### Reading the Cine-Deck

When you scroll rapidly through the section plates (PDF cine-deck):

| What you see | What it means |
|--------------|---------------|
| XY scatter dots shifting smoothly | Gradual compositional drift |
| XY scatter dots jumping suddenly | Structural transition (high omega) |
| XZ bars all near zero | System near maximum entropy (Hs low) |
| XZ bars at extremes (+/-180°) | Strong compositional dominance |
| One XZ bar suddenly swinging | Bearing reversal (structural crossover) |
| YZ bar going strongly negative | Carrier approaching zero (infinite helm) |
| YZ bars becoming more equal | System concentrating toward barycentre |

---

## Q15. Complete CNT Symbology Reference

### Primary Symbols

| Symbol | Name | Definition | Type | Unit |
|--------|------|-----------|------|------|
| x | Composition | x_j = Y_j / Σ Y_k | Vector in S^D | dimensionless |
| h | Higgins Coordinate | h_j = ln(x_j) - (1/D)Σ ln(x_k) | Vector in R^D, Σh=0 | HLR |
| g(x) | Geometric mean | (∏ x_k)^(1/D) | Scalar | dimensionless |
| S^D | Open simplex | {x : x_j > 0, Σx_j = 1} | Manifold | — |
| D | Number of carriers | Positive integer ≥ 2 | Scalar | count |
| N | Number of time points | Positive integer ≥ 1 | Scalar | count |

### CNT Output Channels

| Symbol | Full Name | Formula | Rank | Shape | Bounds |
|--------|-----------|---------|------|-------|--------|
| θ_ij | Bearing | atan2(h_j, h_i) | 2 (antisym) | D(D-1)/2 | [-180°, +180°] |
| ω | Angular velocity | atan2(‖h₁×h₂‖, ⟨h₁,h₂⟩) | 0 (scalar) | 1 | [0°, 180°] |
| κ_HS | Higgins Steering Metric Tensor | (δ_ij - 1/D)/(x_i·x_j) | 2 (sym) | D×D | [0, ∞) |
| σ | Helmsman (DCDI) | argmax_j \|h_j(t+1) - h_j(t)\| | 0 (categorical) | 1 | {1..D} |

### Derived Quantities (per plate)

| Symbol | Name | Formula | Unit |
|--------|------|---------|------|
| Hs | Higgins Scale | 1 - H/ln(D) where H = -Σ x_j ln(x_j) | dimensionless [0,1] |
| Ring | Hs classification | Band of Hs (Hs-0 through Hs-6) | categorical |
| d_A | Aitchison distance | √(Σ (h_j(t+1) - h_j(t))²) | HLR |
| E_metric | Metric energy | Σ d_A² over all steps | HLR² |
| DR | Dynamic range | max(h) - min(h) over all carriers and times | HLR |
| κ (condition) | Condition number | max(κ_jj)/min(κ_jj) = R² | dimensionless |
| s_j | Steering sensitivity | 1/x_j (diagonal readout from κ_HS) | HLR^-1 |

### Matrix Operators

| Symbol | Name | Formula | Size |
|--------|------|---------|------|
| P | Centring matrix | I - (1/D)·11^T | D×D |
| diag(1/x) | Inverse composition diagonal | diagonal matrix with 1/x_j | D×D |
| κ_HS | Full metric (matrix form) | diag(1/x)·P·diag(1/x) | D×D |
| CLR | Transform matrix | H_D = I - (1/D)·11^T | D×D |

### CBS Display Faces

| Face | Horizontal | Vertical | Content |
|------|-----------|----------|---------|
| XY | h_i (CLR carrier i) | h_j (CLR carrier j) | Scatter plan view |
| XZ | Pair index (1..D(D-1)/2) | θ_ij (degrees) | Bearing bar chart |
| YZ | Carrier index (1..D) | h_j (HLR) | CLR profile bars |

### Scale Provenance Chain

```
Y_j(t)  →  x_j = Y_j/T  →  h_j = CLR(x)  →  section coordinate
  │            │                  │                    │
  │            │                  │                    │
absolute    proportion         log-ratio           display
counts      (closure)         (CLR transform)      (plate face)
  │            │                  │                    │
raw data    simplex S^D      sum=0 hyperplane     fixed-scale
                                                   graticule
```

### Temporal Classification

| Channel | Requires | Classification |
|---------|----------|---------------|
| θ(t) | 1 time point | Instantaneous (state snapshot) |
| κ_HS(t) | 1 time point | Instantaneous (local geometry) |
| ω(t,t+1) | 2 consecutive points | Incremental (heading change) |
| σ(t,t+1) | 2 consecutive points | Incremental (displacement label) |
| d_A(t,t+1) | 2 consecutive points | Incremental (metric distance) |
| Hs(t) | 1 time point | Instantaneous (entropy state) |

### Corollary Quick Reference

| # | Name | Statement |
|---|------|-----------|
| C1 | Bearing Determinism | Same x → same θ. No parameters. |
| C2 | Steering Asymmetry | max(κ_jj)/min(κ_jj) = R² where R = max(x)/min(x) |
| C3 | Lock Detection | spread(θ_ij) < ε ⇒ carriers locked (constant ratio) |
| C4 | Bearing Reversal | sign(θ_ij) flips ⇒ structural crossover |
| C5 | Infinite Helm | x_j → 0 ⇒ κ_jj → ∞ ⇒ infinite steering authority |

### Mathematical Properties (all channels)

```
DETERMINISTIC     — same input, same output, always
CLOSED-FORM       — no iteration, no convergence, no optimisation
PARAMETER-FREE    — no tuning, no fitting, no model selection
SCALE-INVARIANT   — absolute magnitude irrelevant (only proportions matter)
DOMAIN-AGNOSTIC   — energy, chemistry, ecology, finance, nuclear, cosmic
```

### CNT as Dimensionality Expander (D=8)

```
INPUT:   8 proportions at 2 time points = 16 numbers
OUTPUT:  28 + 1 + 36 + 1 = 66 independent measurements

The tensor REVEALS structure that is implicit in the raw proportions.
It does not add information — it EXPOSES geometric relationships
that exist but are invisible in the original representation.
```

---

## Q16. The HLR Unit Family — CNT as Universal Instrument for ALL Log-Ratio Systems

### The Family

All members of the log-ratio level family are related by a single constant multiplier:

| Scale | Formula | k (to HLR) | k (from HLR) |
|-------|---------|------------|--------------|
| **HLR** | ln(x_j / g(x)) | 1.0000 | 1.0000 |
| **Neper (Np)** | ln(amplitude ratio) | 1.0000 | 1.0000 |
| **ln fold change** | ln(A/B) | 1.0000 | 1.0000 |
| **log2 fold change** | log2(A/B) | 0.6931 | 1.4427 |
| **dB amplitude** | 20 log10(A/B) | 0.1151 | 8.6859 |
| **dB power** | 10 log10(P1/P2) | 0.2303 | 4.3429 |
| **Cents (music)** | 1200 log2(f2/f1) | 0.000578 | 1731.2 |
| **Astronomical mag** | -2.5 log10(flux ratio) | -0.9210 | -1.0857 |
| **pH** | -log10([H+]/1M) | -2.3026 | -0.4343 |
| **f-stop** | log2(exposure ratio) | 0.6931 | 1.4427 |

The universal conversion:

```
HLR_value = native_value × k_to_HLR

Equivalently:
native_value = HLR_value × k_from_HLR
```

### The Key Insight

Any system whose data is naturally expressed in ANY of these units is **compositional by nature**. The log-ratio implies an underlying ratio. Ratios that partition a total are compositions. Therefore:

```
IF your data is expressed in dB, nepers, fold-change, pH, cents, magnitudes, or f-stops
THEN your data is a log-ratio
THEN your data implies underlying ratios
THEN those ratios can be closed (normalised to sum=1)
THEN they live on a simplex
THEN CLR applies
THEN the full CNT applies
THEN the CBS instrument can display them
```

The CNT is not restricted to "compositional data" in the narrow CoDa sense. It applies to ANY system that uses log-ratios — which turns out to be an enormous family of disciplines.

### CNT Display Standard for Non-Compositional DUT (Device Under Test)

The plate always displays in HLR (native instrument unit). But the info panel adapts to show the DUT's native scale:

```
┌─────────────────────────────────────────────────────┐
│  HCI Stage 1  |  FIXED SCALE                        │
│  Unit: HLR (Higgins Log-Ratio)                      │
│  DUT: Audio spectrum (native: dB SPL)               │
│  Scale: 1 HLR = 8.686 dB                           │
│  Y→x=Y/T→h=CLR→section                             │
│  ...                                                │
└─────────────────────────────────────────────────────┘
```

The instrument reads in HLR. The expert reads in their native unit via the posted conversion. Both are looking at the same data — one in universal compositional coordinates, the other in domain-specific language.

### Complete Domain List — Systems Computable via CNT

Every system below uses log-ratios natively and can be directly expressed on a CNT plate:

| Domain | Native Unit | What Constitutes the "Composition" | D (typical) |
|--------|-------------|-----------------------------------|-------------|
| **Audio engineering** | dB SPL, dBFS | Frequency band power distribution | 10-32 (octave bands) |
| **RF/Telecom** | dBm, dBc, SNR | Signal power allocation across channels | 4-64 |
| **Genomics** | log2 fold change | Gene expression across conditions | 1000s (reduced) |
| **Proteomics** | log2 ratio | Protein abundance across samples | 100s |
| **Spectroscopy** | absorbance (log10) | Absorption across wavelengths | 10-100 |
| **Chemistry (pH)** | pH units | Ion activity distribution | 3-10 species |
| **Acoustics** | dB(A), Leq | Sound source contributions | 5-20 sources |
| **Seismology** | magnitude (log10) | Energy release across frequency | 5-15 bands |
| **Photography** | f-stops (log2) | Exposure distribution (aperture/time/ISO) | 3 |
| **Astronomy** | magnitudes | Flux distribution across bands | 5-8 (UBVRI+) |
| **Finance** | log returns | Portfolio weight allocation | 5-50 assets |
| **Nuclear physics** | cross-section ratios | Reaction channel branching | 3-20 channels |
| **Music theory** | cents (1200 log2) | Interval ratios in tuning systems | 12 (chromatic) |
| **Ecology** | Shannon diversity (ln) | Species abundance distribution | 10-1000 |
| **Neuroscience** | dB (EEG power) | Spectral power across brain bands | 5-7 (delta-gamma) |
| **Meteorology** | dBZ (radar) | Precipitation type distribution | 4-8 types |
| **Materials science** | dB (attenuation) | Frequency-dependent loss channels | 5-20 |
| **Pharmacology** | pIC50 (-log10) | Drug potency distribution across targets | 3-10 |

### What This Means for CoDaWork 2026

The HCI/CNT is not just an energy analysis instrument. It is a **universal compositional navigation plotter** for ANY system that uses log-ratio measurement. The mathematical framework is identical — only the scale factor in the info panel changes.

A physicist reading Nuclear branching ratios sees the same CBS cube face structure as an audio engineer reading frequency band power. The math is the same. The tensor is the same. Only the native unit label differs.

### Evidence: Conversion is Exact and Lossless

```
Given: data in dB power: v_j = 10 log10(P_j / P_ref)

Step 1: Convert to HLR
  h_j = v_j × (ln(10)/10) = v_j × 0.2303

Step 2: Verify sum-to-zero
  If P_j are proportions (P_j/sum = x_j), then:
  h_j = ln(x_j/g(x)) = 0.2303 × 10 log10(x_j/g(x))
  Sum h_j = 0  (by CLR construction)

Step 3: Apply full CNT
  theta, omega, kappa_HS, sigma all computed from h_j
  All in HLR units (or degrees for angles)

Step 4: Info panel reports
  "DUT: Audio power spectrum | 1 HLR = 4.343 dB"
  Expert reads CNT plate + mentally converts via posted factor
```

No information is lost. No approximation is made. The conversion is a multiplicative constant.

---

## Q17. Show the evidence: convert through every system and see the data reproduce itself.

Here is the evidence. It may be proof. The arithmetic alone makes it easy — take a value in any log-ratio system, convert through every other system, return to the start, and watch the original number come back exactly.

### The Exchange Matrix (7 systems, all paths)

The k-factors between any two systems are constant multipliers derived from the ratio of their base logarithms:

```
System          Definition              k-factor to HLR (= Np)
─────────────── ─────────────────────── ───────────────────────
HLR (Np)        ln(ratio)               1.000000
dB (amplitude)  20 log10(ratio)         k = ln(10)/20 = 0.115129
dB (power)      10 log10(ratio)         k = ln(10)/10 = 0.230259
log2 FC         log2(ratio)             k = ln(2)     = 0.693147
Cents           1200 log2(ratio)        k = ln(2)/1200 = 0.000577622
Magnitudes      -2.5 log10(ratio)       k = -ln(10)/2.5 = -0.921034
pH              -log10([H+]/ref)        k = -ln(10)   = -2.302585
```

### Round-Trip Evidence: Every Path Returns Exact

Start with 1.000000 HLR. Convert to each system. Convert from that system to every other. Return to HLR.

```
START: 1.000000 HLR
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Path                                           │ Intermediate    │ Return (HLR)  │
├────────────────────────────────────────────────┼─────────────────┼───────────────┤
│ HLR → dB_amp → HLR                            │ 8.685890 dB     │ 1.000000000   │
│ HLR → dB_pow → HLR                            │ 4.342945 dB     │ 1.000000000   │
│ HLR → log2FC → HLR                            │ 1.442695 FC     │ 1.000000000   │
│ HLR → Cents → HLR                             │ 1731.234 cents  │ 1.000000000   │
│ HLR → Magnitudes → HLR                        │ -1.085736 mag   │ 1.000000000   │
│ HLR → pH → HLR                                │ -0.434294 pH    │ 1.000000000   │
├────────────────────────────────────────────────┼─────────────────┼───────────────┤
│ HLR → dB_amp → log2FC → HLR                   │ 8.686 → 1.443  │ 1.000000000   │
│ HLR → dB_amp → Cents → HLR                    │ 8.686 → 1731.2 │ 1.000000000   │
│ HLR → dB_pow → log2FC → dB_amp → HLR          │ 4.343 → 1.443  │ 1.000000000   │
│ HLR → Cents → dB_pow → Magnitudes → HLR       │ 1731 → 4.343   │ 1.000000000   │
│ HLR → pH → dB_amp → log2FC → Cents → HLR      │ -0.434 → ...   │ 1.000000000   │
│ HLR → Mag → pH → dB_pow → log2FC → dB_amp → HLR │ chain of 5   │ 1.000000000   │
└────────────────────────────────────────────────┴─────────────────┴───────────────┘
```

### Why It Works: One Line of Arithmetic

Every system measures `ln(ratio)` scaled by a constant. Converting between any two is division of their k-factors:

```
value_B = value_A × (k_A / k_B)
```

This is multiplication by a rational constant. Chaining any number of such multiplications and dividing by the total product returns identity:

```
k_A/k_B × k_B/k_C × k_C/k_D × ... × k_N/k_A = 1   (exact, by cancellation)
```

No rounding error. No approximation. No model. No parameter. The chain closes because it is scalar multiplication around a cycle — the factors cancel algebraically.

### The Evidence Statement

1. All seven systems measure the same thing: the natural logarithm of a ratio, scaled by a constant.
2. Converting between any two systems is multiplication by the ratio of their constants.
3. Any cyclic chain of conversions returns the starting value exactly.
4. Therefore, data expressed in ANY of these systems is directly expressible in HLR (and thus on a CNT plate) without loss of information.

The math reproduces the data in each exchange. That is the evidence. The CNT does not need to be trusted on faith — it needs only to be tested by computing the conversions and observing exact round-trip closure.

### Practical Consequence for the Instrument

When the CBS plate displays a reading in HLR, the info panel posts the DUT's native k-factor. The expert can verify any reading by:

```
native_value = HLR_reading / k_native
```

If the expert's own measurement (in their native unit) matches this back-conversion exactly, the instrument has demonstrated its own correctness for that domain. No external validation authority is required. The arithmetic IS the evidence.

---

## Q18. Comprehensive system inventory: where does CNT apply and what are the two categories?

Two categories exist. The distinction is where the logarithm lives.

### Category 1: LOG-RATIO NATIVE (Direct HLR systems)

These systems already measure in logarithmic units. The data arrives pre-logged. CNT applies via a single multiplicative k-factor — no closure step required because the log-ratio IS the native measurement. The instrument reads directly.

```
Path: native_log_value --[x k_factor]--> HLR --> CNT plate
```

#### Critical-interest systems (Category 1)

| # | Domain | Native Unit | What it measures | Composition (carriers) | D typical | Critical interest reason |
|---|--------|-------------|------------------|----------------------|-----------|------------------------|
| 1 | RF/Telecom | dBm, dBc, dBi | Signal power allocation across channels | Channel power budget | 4-256 | Spectrum management, 5G/6G allocation |
| 2 | Audio engineering | dB SPL, dBFS | Frequency band power distribution | Octave/third-octave bands | 10-32 | Room acoustics, noise control, mixing |
| 3 | Radar systems | dBZ, dBsm | Reflectivity across range/Doppler bins | Target energy distribution | 8-128 | Weather, air traffic, defence |
| 4 | Sonar/Underwater acoustics | dB re 1uPa | Source level across frequency | Spectral energy budget | 10-64 | Submarine detection, marine biology |
| 5 | Seismology | magnitude (log10 A/T) | Energy release across frequency bands | Spectral energy partition | 5-20 | Earthquake characterisation, early warning |
| 6 | Genomics | log2 fold change | Gene expression ratios across conditions | Transcriptome partition | 100-20000 | Cancer markers, drug response |
| 7 | Proteomics | log2 ratio (iTRAQ, TMT) | Protein abundance across samples | Proteome partition | 100-5000 | Biomarker discovery, drug targets |
| 8 | Metabolomics | log2/log10 ratio | Metabolite concentration ratios | Metabolome partition | 50-2000 | Disease diagnosis, nutrition |
| 9 | Spectroscopy (UV-Vis) | absorbance (log10 I0/I) | Absorption across wavelengths | Spectral absorption budget | 10-100 | Chemical analysis, quality control |
| 10 | Spectroscopy (IR/Raman) | absorbance/log intensity | Vibrational mode distribution | Mode energy budget | 20-200 | Material ID, polymer analysis |
| 11 | Spectroscopy (NMR) | log intensity ratios | Chemical shift peak distribution | Peak area budget | 5-50 | Structure determination, purity |
| 12 | Spectroscopy (Mass spec) | log intensity | Ion abundance across m/z | Fragmentation budget | 10-1000 | Forensics, environmental |
| 13 | Astronomy (photometry) | magnitudes (-2.5 log10) | Flux distribution across bands | SED (spectral energy distribution) | 5-20 | Stellar classification, redshift |
| 14 | Astronomy (radio) | Jy (log flux density) | Source flux across frequency | Radio SED | 5-30 | Pulsar, AGN characterisation |
| 15 | Nuclear physics | cross-section ratios (barns) | Reaction channel branching | Decay channel partition | 3-20 | Reactor design, medical isotopes |
| 16 | Particle physics | log(sigma) | Production cross-sections across channels | Decay mode branching | 3-15 | Collider physics, BSM searches |
| 17 | pH chemistry | pH = -log10[H+] | Ion activity distribution | Acid-base equilibrium | 3-12 species | Titration, water treatment |
| 18 | Pharmacology | pIC50, pKa, pKd (-log10) | Drug potency across targets | Target affinity distribution | 3-20 | Drug design, selectivity |
| 19 | Toxicology | log(dose-response) | Dose-response across endpoints | Toxicity profile | 5-15 | Safety assessment, regulation |
| 20 | Music/Acoustics | cents (1200 log2) | Interval ratios in tuning | Interval distribution | 12 (chromatic) | Tuning theory, instrument design |
| 21 | Photography/Imaging | EV, f-stops (log2) | Exposure distribution | Exposure triangle partition | 3 | Camera design, HDR |
| 22 | Electronics (amplifiers) | dB gain/attenuation | Gain distribution across stages | Stage gain budget | 3-20 | Amplifier design, feedback systems |
| 23 | Power systems | dB loss | Transmission loss across segments | Loss budget allocation | 5-50 | Grid design, efficiency |
| 24 | Fibre optics | dB/km, dBm | Power budget across spans | Link budget partition | 5-100 | Network design, maintenance |
| 25 | Antenna arrays | dBi, dBd | Radiation pattern across elements | Array factor partition | 4-256 | Beamforming, MIMO |
| 26 | EMC/EMI | dBuV/m | Emission distribution across frequency | Emission spectrum budget | 10-100 | Compliance, shielding |
| 27 | Vibration analysis | dB re 1g, dB re 1m/s2 | Vibration energy across frequency | Modal energy distribution | 10-50 | Machine health, structural |
| 28 | Psychoacoustics | phon, sone (log-based) | Loudness across critical bands | Perceived loudness budget | 24 (Bark bands) | Hearing aid, audio codec |
| 29 | Medical imaging (MRI) | dB (signal contrast) | Tissue contrast across sequences | Contrast budget | 3-8 tissues | Diagnosis, sequence design |
| 30 | Medical imaging (CT) | Hounsfield (log-linear) | Attenuation across tissue types | Tissue attenuation budget | 4-10 | Dose optimisation, diagnosis |
| 31 | Ultrasonics (NDT) | dB attenuation | Defect signal distribution | Flaw response budget | 5-20 | Weld inspection, materials |
| 32 | Lidar/Remote sensing | dB backscatter | Return signal across range | Atmospheric scattering budget | 10-100 | Aerosol, terrain mapping |
| 33 | Geophysics (well logging) | log resistivity | Formation property distribution | Layer property budget | 5-20 | Oil exploration, aquifer |
| 34 | Noise control | dB(A), Leq | Source contribution levels | Source budget (ISO 3744) | 5-30 | Industrial, environmental |
| 35 | Telecommunications (BER) | log10(BER) | Error rates across channels | Error budget partition | 4-64 | Network quality, 5G |
| 36 | Financial returns | log returns (ln P(t)/P(t-1)) | Return distribution across assets | Portfolio weight evolution | 5-500 | Risk management, allocation |
| 37 | Information theory | bits, nats (log2, ln) | Information across source symbols | Entropy distribution | 2-256 | Compression, coding |
| 38 | Neuroscience (EEG) | dB (power spectral) | Brain rhythm power distribution | Frequency band budget | 5-7 (delta-gamma) | BCI, sleep staging, diagnosis |
| 39 | Neuroscience (fMRI) | log BOLD ratio | Activation across brain regions | Regional activation budget | 10-100 ROIs | Cognitive mapping |
| 40 | Ecology (diversity) | Shannon H = -Sum pi ln pi | Species abundance distribution | Community structure | 10-1000 | Conservation, health assessment |
| 41 | Meteorology (radar) | dBZ | Precipitation type distribution | Hydrometeor budget | 4-8 | Severe weather, flooding |
| 42 | Materials science | dB attenuation vs frequency | Frequency-dependent loss channels | Loss mechanism budget | 5-20 | Material characterisation |
| 43 | Cosmology | log(density ratio) | Energy density across components | Cosmic energy budget | 3-7 | Dark energy, structure formation |
| 44 | Semiconductor | dB (noise figure) | Noise contribution across stages | Noise budget chain | 5-20 | IC design, sensitivity |
| 45 | Laser physics | dB gain/loss per pass | Gain distribution across cavity modes | Mode competition budget | 3-100 | Laser design, stability |
| 46 | Plasma physics | log(density), log(temperature) | Plasma parameter distribution | Plasma state partition | 3-10 | Fusion, space weather |

#### Why these are critical

Every system above ALREADY WORKS in log-ratios. The practitioners already think in dB, magnitudes, fold-change, pH. The CNT adds:

1. Multi-carrier bearing (theta) — "which way is the system pointing in compositional space?"
2. Rate of change (omega) — "how fast is the heading turning?"
3. Steering sensitivity (kappa_HS) — "which carrier dominates system motion?"
4. Dominant driver (sigma) — "who moved most this step?"

These are questions that NO existing instrument in any of these fields currently answers. The CNT is not replacing existing measurements — it is reading structure that exists in the data but has never been extracted.

---

### Category 2: COMPOSITIONAL BUT NOT LOG-RATIO NATIVE

These systems have data that sums to a constant (or can be closed to a constant) but the native measurement is in LINEAR units — percentages, mass fractions, counts, proportions. The CLR transform converts them to log-ratio form, THEN the CNT applies.

```
Path: linear_proportions --[closure]--> x --[CLR]--> h (now in HLR) --> CNT plate
```

#### Comprehensive list (Category 2)

| # | Domain | Native Unit | What it measures | Composition (carriers) | D typical |
|---|--------|-------------|------------------|----------------------|-----------|
| 1 | Geochemistry | wt%, ppm | Oxide/element concentration | Rock/mineral composition | 5-15 |
| 2 | Sedimentology | vol%, mass% | Grain size fractions | Particle size distribution | 5-12 |
| 3 | Food science | g/100g, % | Nutrient composition | Macronutrient budget | 4-10 |
| 4 | Metallurgy | wt% | Alloy element content | Alloy composition | 3-12 |
| 5 | Cement chemistry | wt% | Oxide composition | Clinker formula | 4-8 |
| 6 | Soil science | %, mg/kg | Particle and nutrient content | Soil texture/fertility | 5-15 |
| 7 | Water chemistry | mg/L, meq/L | Ion concentration | Major ion budget | 6-10 |
| 8 | Air quality | ug/m3, ppm | Pollutant concentrations | Emission source profile | 5-20 |
| 9 | Election data | % vote share | Party share of total vote | Political composition | 3-10 |
| 10 | Market share | % | Company share of total market | Market structure | 3-20 |
| 11 | Energy mix | TWh, % | Generation by source type | Electricity composition | 5-12 |
| 12 | Time use | hours/day | Activity time allocation | Daily time budget | 5-15 |
| 13 | Budget allocation | %, currency | Spending across categories | Financial composition | 5-30 |
| 14 | Household expenditure | % of income | Spending shares (Engel curves) | Consumption budget | 8-15 |
| 15 | Demographics | % population | Age/ethnic/income distribution | Population structure | 5-20 |
| 16 | Land use | km2, % | Land cover type distribution | Landscape composition | 5-12 |
| 17 | Textile | % fibre | Fibre content blend | Fabric composition | 2-6 |
| 18 | Paint/Pigment | % by volume | Pigment distribution | Colour formulation | 3-8 |
| 19 | Pharmaceutical tablet | mg, % | Excipient composition | Formulation budget | 4-10 |
| 20 | Particle physics (branching) | dimensionless ratio | Decay branching fractions | Decay budget | 3-20 |
| 21 | Sports analytics | % possession | Game statistic shares | Performance composition | 5-15 |
| 22 | Traffic flow | vehicles/hr by type | Vehicle type distribution | Traffic composition | 4-8 |
| 23 | Paleontology/Palynology | counts, % | Fossil/pollen type abundance | Community composition | 10-100 |
| 24 | Genetics (allele freq) | frequency (0-1) | Allele distribution in population | Population genetics | 2-20 per locus |
| 25 | Microbiome | relative abundance | Taxon abundance distribution | Community structure | 50-5000 |
| 26 | Atmospheric composition | ppm, % | Gas concentration distribution | Atmospheric budget | 5-10 |
| 27 | Waste management | %, tonnes | Waste stream composition | Waste characterisation | 5-12 |
| 28 | Crop yields | % of total harvest | Crop type distribution per region | Agricultural composition | 5-15 |
| 29 | Fisheries | catch weight % | Species catch distribution | Fishery composition | 5-30 |
| 30 | Ceramic/Glass | mol%, wt% | Oxide formulation | Glass/glaze composition | 4-10 |

---

### The Difference: What separates Category 1 from Category 2?

```
Category 1:  measurement --> [k-factor] --> HLR --> CNT
             (1 step: scale)

Category 2:  measurement --> [closure] --> x --> [CLR] --> HLR --> CNT
             (3 steps: close, log, centre)
```

#### Structural difference

| Property | Category 1 (log-native) | Category 2 (linear-native) |
|----------|------------------------|---------------------------|
| Native measurement | Already logarithmic | Linear (%, mass, count) |
| Closure step needed? | NO — implied by log-ratio structure | YES — must normalise to constant sum |
| CLR transform needed? | NO — k-factor scales directly to HLR | YES — full CLR is the conversion |
| Information loss at entry? | None — direct scaling | None — closure preserves relative info |
| Practitioner familiarity with log space | HIGH — they already think in dB/pH/mag | LOW — they think in % and absolute units |
| CNT adoption barrier | MINIMAL — just add bearings to existing display | MODERATE — must accept log-ratio as valid |

#### The discovery

Both categories end up on the SAME CNT plate. The theta, omega, kappa_HS, and sigma readings are identical regardless of whether the data arrived as dB values or as mass percentages — because the CLR coordinate h_j is the same in both cases once the arithmetic is done.

This means:

1. A geochemist looking at oxide percentages on a CNT plate sees the SAME mathematical object as an RF engineer looking at channel power in dBm — if their compositions have the same structure.

2. Cross-domain pattern recognition becomes possible. A bearing lock (C3 corollary) in a telecom channel budget looks identical to a bearing lock in a rock oxide composition. The physics differs. The geometry is the same.

3. Category 1 systems have an EASIER adoption path because practitioners already accept log-ratio measurement as natural. They just need the CNT channels added to their existing displays.

4. Category 2 systems require an educational step — convincing practitioners that log-ratio coordinates reveal structure invisible in linear percentages. This is the CoDa community's existing challenge, and CNT provides a new instrument to make the case.

#### The curiosity

Category 1 systems have been using log-ratios for decades (sometimes centuries — stellar magnitudes since Hipparchus) without knowing they were doing compositional data analysis. They have the TOOL (log-ratio measurement) but not the FRAMEWORK (CoDa theory).

Category 2 systems have the FRAMEWORK (many geochemists know Aitchison's work) but often lack the TOOL (practical instruments that display compositional motion in real time).

CNT bridges both: it gives Category 1 the framework they were missing, and gives Category 2 the instrument they were missing.

---

## Conclusions — CNT Character Manual Close-Out

### What the CNT IS

A 4-channel deterministic instrument reading computed from any closed composition. No parameters. No model selection. No fitting. Pure arithmetic from the CLR coordinate to a tuple of tensors of mixed rank.

### What it DOES

1. Measures WHERE the system points (theta — D(D-1)/2 bearings)
2. Measures HOW FAST the heading changes (omega — 1 scalar)
3. Measures HOW SENSITIVE each carrier is to perturbation (kappa_HS — D x D matrix)
4. Identifies WHO moved most (sigma — 1 categorical index)

### What it REQUIRES

- A closed composition (or data that can be closed)
- At least 2 time points for omega and sigma (1 for theta and kappa_HS)

### What it PRODUCES

For D=8: 66 independent measurements from 16 input numbers (dimensionality expander).

### Where it APPLIES

- 46 log-ratio-native systems (Category 1) — direct k-factor scaling
- 30+ compositional-but-linear systems (Category 2) — via CLR transform
- Total: 76+ distinct application domains across all sciences

### Key mathematical properties

- Deterministic (same input = same output, always)
- Closed-form (no iteration, no convergence criterion)
- Parameter-free (no tuning, no selection)
- Scale-invariant (multiply all carriers by a constant, tensor unchanged)
- Domain-agnostic (the math works the same regardless of what the carriers represent)

### Display standard

CBS (Compositional Bearing Scope) — three orthogonal cube face projections with fixed-scale graticule, projected along the Higgins axis as a cine-deck of section plates. Unit: HLR. Info panel shows DUT native unit with k-factor conversion.

### Evidence standard

Round-trip conversion through all 7 log-ratio systems returns exact starting value. The chain closes algebraically because scalar multiplication around a cycle cancels. This arithmetic closure IS the evidence.

### Status

CLOSED — exploratory complete at Q18. The character of the CNT is fully documented. Further work extends into Stage 2 (metric cross-examination) and Stage 3 (higher-degree structural analysis) which use the CNT as their foundational coordinate frame.

---

The instrument reads. The expert decides. The loop stays open.
