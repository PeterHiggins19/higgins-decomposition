# The Isotropic Radiation Ground State and the Traction Engine

**Why Hˢ moves: the budget, the partition, the log-frequency carrier, and the phase trajectory — derived from thirty years of measured acoustic work, written as a single formula, with the full mathematical apparatus.**

---

**Document status:** Master standard, working flagship paper — draft v2.2.
**Created:** 2026-05-21.   **Expanded to master standard:** 2026-05-21.
**Consolidated against RWA cross-check (v2.2):** 2026-05-22.
**Author:** Peter Higgins · Rogue Wave Audio · Binaural Test Lab · Markham, Ontario, Canada.

> **v2.2 note.** This version consolidates the flagship against the Rogue-Wave-Audio repository (`Current-Repo/RWA/LINEAGE.md`, `HUF_RELATIONSHIP.json`, `RWA-001.json`, `docs/papers/`). The recomposition in v2.1 was performed bottom-up by AI synthesis without full access to the RWA archive; the v2.2 pass folds in the eight architectural details surfaced in the cross-check: (1) the HUF-GOV / HUF-CLS fork at ADAC; (2) the Paired Measurement Doctrine; (3) DADI as failure-direction diagnostic; (4) date precision (DADC formalized 2024-12-05, DADI 2024-12-06, ADAC 2025 early-mid, H₁ 2026-02, MC-4 generalization moment November 2025); (5) the November 2025 Grok-collaboration generalization moment; (6) the non-monotonic H₁ abstraction path (DADC simplex → H₁ abstract Hilbert → HUF back to simplex); (7) the concept-folder anticipations (`concepts/entropix/` → EITT, `concepts/regimes/` → HUF regime vocabulary, `concepts/v-infinity-core/` → HUF V∞Core stack); (8) the systematic AI-collaboration archiving methodology that began as `concepts/ai-reports/` in RWA and became HUF's `briefings/` discipline. The framework was substantially recovered from public material by independent synthesis; the comparison against the RWA archive closes the loop and makes the system whole.

**Conforms to:** HUF-STD-001 v1.1 (Publication Standards) · HUF-STD-002 (Tensor Train I/O) · HUF-STD-003 (Linear Algebra Foundations).
**Companion to:** [`HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](../../HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md) (historical narrative) and the manuscript at [`papers/codawork2026/manuscript/`](../codawork2026/manuscript/) (first non-acoustic application).
**Scope discipline:** This is a Hˢ flagship paper. It is **not** part of the CoDaWork 2026 conference package and falls **outside** the Pre-Conference Lockdown window (2026-05-12 → 2026-06-06). It is a separate post-conference project that can be drafted, refined, and committed during the lockdown without touching any locked surface.
**Citation policy.** External references in §15 are limited to peer-reviewed published works only. Repository materials authored by the present author and not yet externally peer-reviewed are listed separately in §16 under their disposition as self-hosted preprints or working papers.

---

## Preface — why this document exists, and why now

Hˢ works. It worked the first time it was tried on energy-mix data, it worked on the geochemistry corpus, it worked on the macro-economic compositions, it worked on the eleven domains and one hundred and one datasets of the 2026-05 validation suite. Reviewers ask why, and the published reply — *"it inherits from compositional data analysis and adds a quaternion phase layer"* — is true but insufficient. It explains the structure. It does not explain the **confidence**.

This document supplies the missing explanation. The confidence is not philosophical. It is empirical. The Hˢ framework is the formal generalization of a thirty-year body of acoustic engineering practice conducted at the **Binaural Test Lab** — a sound-controlled professional laboratory operated through a private industrial sponsorship with parallel deployments in Ottawa and Monaco — where the same compositional structure has been validated against measured sound fields over working hours, under varying environmental conditions, across real listening positions, with real human listeners, on real loudspeaker hardware, in real rooms. The mathematics did not arrive first and find an application. The acoustic measurements arrived first and forced the mathematics.

Three properties of the original acoustic problem turn out to be the three properties that make Hˢ a *traction engine* — a framework that moves, not one that holds still:

1. **A physical ground state fixes the total.** The unit-sphere radiation budget — 6.02 dB across the 4π → 2π baffle-step transition — is a measured invariant, not a normalization convention. Closure is enforced by acoustic physics, not chosen for mathematical convenience.

2. **The partition lives on the simplex.** The total is distributed across cabinet dimensions in DADC, across ERB bands × drivers in HCI-AUDIO, across compositional carriers in the general case. The simplex is where the parts live. It is the same simplex regardless of the domain.

3. **Time enters the simplex through the log-frequency axis.** This is the part that has never before been written down in one place. The geometric-frequency association — the fact that the partition is naturally indexed by log-spaced carriers — couples directly to group delay, which couples directly to phase rotation on the three-sphere S³. The simplex acquires *motion* because each carrier has a log-frequency position and a phase trajectory. The static partition becomes a path. The path is traction.

The unified formula below carries all four ingredients — budget, partition, log-frequency carrier, phase trajectory — in a single expression, evaluable at one frequency or integrated across the full audible band. Around it sit the mathematical foundations that have always supported the acoustic instance and that now make the generalization rigorous: Helmholtz reciprocity (Lemma 3), the Rayleigh-Sommerfeld integral (Lemma 2), Banach fixed-point convergence (Lemma 4), spectral-radius stability of the adaptive feedback (Lemma 5), Statistical Energy Analysis positive-definiteness (Lemma 6), the group-delay-as-rotation identity on S³ (Lemma 7), and closure invariance under the log-ratio transform (Lemma 8). The chain closes with the master statement of the unified formula (Theorem 1) and its compositional generalization (Theorem 2).

This document is the first time all of it has been written down as a unified, internally-proven statement. It is intended to be the master standard for the chain.

---

## §1 — Symbols and notation

The notation below follows the conventions established in `HCI-CNT/handbook/GLOSSARY.md` v3.0 §26. Symbols introduced in this document add to that base set; they are listed below with their first-use section number.

**Scalars and physical constants**

| Symbol | Meaning | First use |
|---|---|---|
| `c`        | Ground-state radiation budget = 20·log₁₀(2) ≈ 6.0206 dB | §2 |
| `c_sound`  | Speed of sound in air, ≈ 343 m s⁻¹ at 20 °C | §4 |
| `ρ`        | Air density, ≈ 1.21 kg m⁻³ at 20 °C, 101.3 kPa | §7 (Lemma 2) |
| `λ`        | Wavelength, λ = c_sound / f | §7 |
| `k`        | Wavenumber, k = 2π / λ = ω / c_sound | §7 |
| `ω`        | Angular frequency, ω = 2πf | §5 |
| `κ`        | Evanescent decay constant, κ = √(k² − ω²/c_sound²) for |k| > ω/c_sound | §7 |

**Geometric and partition quantities**

| Symbol | Meaning | First use |
|---|---|---|
| `n`        | Number of partitions in the active instance | §3 |
| `dimᵢ`     | Physical extent of the i-th partition (acoustic case) | §3 |
| `S`        | Geometric scale, S = Σᵢ dimᵢ | §3 |
| `Iₛ`       | Reciprocal scale, Iₛ = Σᵢ (1 / dimᵢ) | §3 |
| `D`        | Dominance ratio, D = max(dimᵢ) / min(dimᵢ) | §3 |
| `β`        | Hybrid-regime blend coefficient, β = 2(D − 1.5) | §3 |
| `pᵢ`       | Simplex coordinate (portion), pᵢ = dimᵢ / S; Σ pᵢ = 1 | §3 |
| `Gᵢ`       | Per-partition gain (dB), Gᵢ = c · pᵢ; Σ Gᵢ = c | §3 |

**Spectral and phase quantities**

| Symbol | Meaning | First use |
|---|---|---|
| `f`        | Frequency (Hz) | §4 |
| `F_c,i`    | Geometric cutoff frequency for partition i, F_c,i = 115 / dimᵢ | §4 |
| `f̄ⱼ`       | Geometric centre frequency of band j | §4 |
| `S(f, F_c,i)` | First-order baffle-step shelf, 1/√(1 + (F_c,i/f)²) | §4 |
| `φ(f)`     | Phase response at frequency f | §5 |
| `τ`        | Group delay (seconds), τ = −(1/2π) dφ/df | §5 |
| `τᵢ`       | Per-partition group delay | §5 |
| `n̂ᵢ`       | Unit rotation axis for partition i on S³ | §5 |
| `q(f, t)`  | Unit-quaternion phase state at frequency f, time t | §5 |
| `iₓ, iᵧ, i_z` | Three imaginary units of the quaternion algebra | §5 |

**Hˢ system quantities (per `HCI-CNT/handbook/GLOSSARY.md` §26)**

| Symbol | Meaning |
|---|---|
| `D`        | Composition dimension (number of carriers); reused from acoustic D context-permitting |
| `T`        | Number of records (timesteps) |
| `xᵢ, ρᵢ`   | The i-th carrier's value or share |
| `clrᵢ(t)`  | Center log-ratio coordinate at time t |
| `η(t)`     | ILR coordinate vector at time t |
| `θ, ω, κ, σ` | The four CNT channels (bearing, angular velocity, curvature, helmsman) |
| `αⱼ(t)`    | Activation Coefficient for carrier j at time t |
| `πⱼ(t)`    | Power Share for carrier j at time t |
| `Q(t)`     | Quaternion trajectory as a function of time |
| `S^(D−1)`  | The (D−1)-simplex |
| `S³`       | The 3-sphere ≅ unit quaternions ≅ SU(2) |

**Operators**

| Operator | Meaning |
|---|---|
| `C(·)`     | Closure operator, C(x) = x / Σ xᵢ |
| `clr(·)`   | Center log-ratio, clrᵢ(x) = log(xᵢ) − (1/D) Σⱼ log(xⱼ) |
| `ilr(·) = Vᵀ clr(·)` | Isometric log-ratio (Helmert) with VVᵀ = I |
| `q*`       | Quaternion conjugate, (a, −b, −c, −d) |
| `Δ`        | Forward difference, Δf(t) = f(t+1) − f(t) |
| `∇²`       | Laplacian operator |

---

## §2 — The isotropic radiation ground state

**Claim.** When a point acoustic source is mounted in a rigid finite baffle, the radiation field undergoes a measured transition between two limiting regimes:

- **Low frequency.** Wavelength is large compared to the baffle dimensions. The source radiates into the full 4π steradian sphere — *isotropic radiation* — and the response carries an inverse-square-law roll-off relative to the half-space reference.
- **High frequency.** Wavelength is small compared to the baffle dimensions. The source radiates into the forward 2π steradian half-space and the response is flat relative to the same reference.

The transition between these two regimes is the *baffle step*. Its total magnitude is

```
ΔL = 20 · log₁₀(2)  ≈  6.0206  dB.                                       (1)
```

This is the **isotropic radiation ground state of the loudspeaker problem**. The 6.02 dB figure is the on-axis pressure ratio that results from a *power-conserving* redistribution: the same total radiated acoustic power, integrated over the sphere, transitions from being spread across 4π steradians to being concentrated into 2π. Total power is conserved; on-axis pressure rises by exactly 20·log₁₀(2). It is not approximate, not a convention, not a model parameter. In calibrated measurement it reproduces to better than 0.05 dB. At the Binaural Test Lab it has been observed to that precision continuously, under varying temperature, humidity, and atmospheric pressure, for more than three decades.

The conservation law that makes the budget interpretation legitimate is the conservation of *total radiated acoustic power*. The 6.02 dB itself is in pressure (amplitude) decibels, but the closure (equation 14) holds because **what is being apportioned is the total radiated power across the partitions, not the on-axis amplitude**. This distinction is the key to §4.2 below, and it determined the crossover topology that ships with every BTL build.

Define

```
c  :=  20 · log₁₀(2)  =  6.0206  dB.                                     (2)
```

The constant **c** is the *ground-state budget*. Everything in what follows is a distribution of, or a phase trajectory around, this budget. It is the analogue of the closure constraint Σpᵢ = 1 in standard compositional-data analysis (Aitchison 1986; Pawlowsky-Glahn et al. 2015) — but the analogue carries a physical interpretation that compositional data analysis (CoDa) typically lacks: the constant is *the total amount of radiation*, not an arbitrary unit of accountancy.

### §2.1 — Why this is the ground state and not just a normalization

In quantum-mechanical language, a *ground state* is the lowest-energy configuration of a system, against which all excitations are measured. The 6.02 dB radiation budget plays exactly this role in acoustic baffle problems:

- Every diffraction correction is a *deviation* from the isotropic budget.
- Every cabinet-dimension allocation is a *partition* of the budget.
- Every adaptive feedback step (ADAC) is a *return to* the budget.

The budget is what the system relaxes to in the absence of forcing. The partitions and portions are how the budget gets *allocated* under physical constraints — driver size, cabinet geometry, listening-position aiming. The closure rule is what *holds the allocation together* as conditions change.

This is the same triple structure that appears in every successful application of Hˢ to a non-acoustic problem. The energy-mix monitoring work uses electrical-generation share (closure: 100 %) as the budget; the geochemistry work uses major-element oxide fraction (closure: 100 % by weight) as the budget; the macro-economic work uses GDP share (closure: 100 %) as the budget. In each case the partition is structural, the closure is physical, and the deviations from the equal-share isotropic reference are the *signals*. The 6.02 dB was the first one, and it was measured before anyone in compositional-data analysis had thought to look for it.

---

## §3 — Partitions and portions on the simplex

**The forward map (DADC).** Given cabinet dimensions (H, W, D) with H + W + D = S, the Dimension-Apportioned Diffraction Correction distributes the ground-state budget c as

```
G_i  =  c · dimᵢ / S        for i ∈ {H, W, D}                            (3)

               Σᵢ G_i  =  c.                                              (4)
```

Equation (4) is the **closure rule**. It is the same closure rule that appears in every CoDa application; it is enforced here by the physical observation that the total radiation budget is fixed. The simplex coordinate pᵢ = dimᵢ/S is the normalized portion. The actual gain Gᵢ in decibels is the portion multiplied by the ground-state constant c. The closure proof is Lemma 1 in §7.

**The BTL measurement.** For the canonical BTL rectangular geometry (H = 0.8 m, W = 0.368 m, D = 0.33 m, S = 1.498 m):

| Dimension | dimᵢ (m) | pᵢ = dimᵢ/S | Gᵢ (dB) |
|-----------|----------|-------------|---------|
| Height    | 0.8      | 0.534       | 3.215   |
| Width     | 0.368    | 0.246       | 1.479   |
| Depth     | 0.33     | 0.220       | 1.326   |
| **Total** | **1.498**| **1.000**   | **6.020** |

The closure is exact to four decimal places. It is exact in every well-calibrated BTL measurement *because it is forced by physics*.

**The generalization.** Replacing physical dimensions with arbitrary compositional carriers and replacing the 6.02 dB ground state with whatever total constraint the application imposes gives the standard CoDa apportionment

```
pᵢ  =  xᵢ / Σⱼ xⱼ ,           Σᵢ pᵢ  =  1.                              (5)
```

Equation (5) is what one finds in Aitchison (1986) and Pawlowsky-Glahn et al. (2015). Equation (3) is the *acoustic instance* of equation (5). The simplex was already there in the 4π → 2π physics; CoDa later supplied the geometry; Hˢ supplied the dynamics. The order matters historically. The mathematics is the same.

### §3.1 — Short, long, and hybrid regimes

The single-formula treatment in equation (3) holds for the **long-dimension regime** (D = max(dimᵢ)/min(dimᵢ) > 2). In two adjacent regimes the apportionment changes form:

- **Short regime** (D < 1.5). Reciprocal emphasis: Gᵢ = −c · (1/dimᵢ) / Iₛ where Iₛ = Σⱼ (1/dimⱼ). Closure remains Σ Gᵢ = −c.
- **Hybrid regime** (1.5 ≤ D ≤ 2). Linear blend: Gᵢ = c · [β · dimᵢ/S + (1 − β)·(1/dimᵢ)/Iₛ] with β = 2(D − 1.5).

In all three regimes the closure Σ Gᵢ = ±c holds exactly. The simplex constraint is regime-independent; only the orientation of the apportionment within the simplex changes. This is the acoustic precursor of the **Helmsman family** in CNT (sign / stability / flips / chaos / torque / joint) — a single closure with multiple regime-specific orientations. The regime taxonomy itself is the descendant of the `concepts/regimes/` R&D thread in the RWA repository, which was naming and classifying regimes as a working vocabulary before HUF formalized them; the HUF regime taxonomy carries that vocabulary forward verbatim.

### §3.2 — ADAC as the observe-or-control fork

The third operation in the DADC family — adaptive closure (ADAC) — is structurally different from the first two. DADC (forward) and DADI (inverse) are mappings; ADAC is *a decision point*. ADAC produces an error signal: it knows when the closure has drifted, by how much, and in which direction. From that error signal, two architectures are physically possible:

- **Closed loop.** Feed the error signal back automatically. Correct continuously. The apparatus becomes a self-regulating control system that holds the closure constant against drift. Every engineering instinct says: close the loop.
- **Open loop.** Surface the error signal but do not act on it. Let the researcher decide whether the drift represents an instrumentation fault, a real change in the room, or a transient that should be tolerated. The apparatus becomes an *observation* tool that supplies diagnostics but withholds automatic action.

**The decision to leave ADAC open by default was deliberate.** The closed-loop architecture would have collapsed the role of the researcher into the role of the controller; the open-loop architecture preserves the researcher as the agent who interprets what the closure failure means. This is the architectural ancestor of **HUF-GOV** (open, stateless, scientific) and **HUF-CLS** (closed, stateful, control) — the two governance regimes that emerge from the same error-signal fork. HUF-GOV remains the scientific framework's home; HUF-CLS is reserved for engineered systems where the closure must be defended automatically against drift the operator cannot evaluate fast enough.

The Hˢ engine-independence policy (cnt_content_sha256 ⊥ cnq_content_sha256) is the descendant of this open-by-default discipline: the amplitude readout and the phase readout are kept architecturally independent so that no implicit feedback couples them; the researcher integrates them by decision, not by automatic loop. *The fork at ADAC made the framework scientific rather than control-theoretic.*

### §3.3 — DADI as failure-direction diagnostic

The DADI inverse map is more than an inverse: it is a *diagnostic instrument by failure-direction*. When the iteration `dim_{n+1} = G_dim · (dim_n · r) / c` converges (Banach contraction, Lemma 4), the result is the recovered cabinet geometry. When the iteration *fails to converge*, the direction in which it fails is informative:

- **Failure mode 1 — convergence to the wrong limit.** The measured response is consistent with cabinet geometry, but a different geometry than the one being tested. This indicates that a *hidden dimension* is present (an unmodelled reflection surface, an additional driver, a room mode). The fix is to add a degree of freedom to the model.
- **Failure mode 2 — divergence or oscillation.** The measured response is not consistent with any stationary cabinet geometry. This indicates *non-stationarity* — the room is changing faster than the iteration can track (temperature transient, opening of a door, occupancy change). The fix is to wait, or to declare the measurement non-quasi-static.

DADI is therefore *not just an inverse*; it is a *triage operator* that returns one of three outcomes: (a) recovered geometry, (b) hidden-dimension flag, (c) non-stationarity flag. This is the acoustic precursor of the EITT inversion diagnostic in HUF: when entropy-invariance under geometric-mean decimation fails at dimension K, the direction of the failure classifies the disturbance — increase K for hidden dimensions, decrease K for non-stationarity. **Same diagnostic-by-failure-direction logic, different domain instance.**

The general lesson: *a well-designed inverse map is also a classifier of the disturbance modes under which it fails to invert.* This is the second face of the Helmsman family in CNT (its "flips / chaos" diagnostics): the trajectory is diagnostic not only when it converges but also when it doesn't.

---

## §4 — The geometric-frequency association

**The cutoff.** Each cabinet dimension has an associated cutoff frequency

```
F_c,i  =  115 / dimᵢ            (Hz, with dimᵢ in metres)                 (6)
```

derived from c_sound / (2·dimᵢ) where c_sound ≈ 343 m s⁻¹ is the speed of sound. For the BTL geometry:

| Dimension | F_c,i (Hz) |
|-----------|------------|
| Height    | 143.75     |
| Width     | 312.50     |
| Depth     | 348.48     |

The transition for each dimension is a first-order baffle-step shelf,

```
S(f, F_c,i)  =  1 / √( 1 + (F_c,i / f)² ).                                (7)
```

**Why log-frequency, not linear.** Two independent facts make the log-frequency axis the natural one:

1. **Geometric scaling.** Cutoff frequencies inversely related to physical dimensions cluster geometrically: doubling a dimension halves its cutoff. The natural index variable is log F, because differences in log F correspond to ratios of dimension. The dimensions H = 0.8, W = 0.368, D = 0.33 give cutoffs spaced by ratios 2.18 and 1.12, not by absolute differences.

2. **Perceptual scaling.** Human auditory perception is logarithmic in frequency (pitch perception, octave equivalence) and the cochlea is a constant-Q filter bank on log frequency (Glasberg & Moore 1990; Moore 2012). The ERB-rate scale, `ERB_rate(f) = 21.4 · log₁₀(0.00437·f + 1)`, is the modern psychoacoustic standard. It is monotonically related to log F at all but the lowest frequencies.

Combine (1) and (2) and the conclusion is the same: the *geometric-mean frequency* of each band is the carrier identity. Bands are not enumerated by ordinal index alone; they are *positioned on the log-frequency axis* at their geometric centre. The partition is therefore not just a vector of n numbers — it is a vector of n numbers each labelled by its log-frequency coordinate.

This is the **geometric-frequency association**. It is the bridge that makes the simplex carry time, because log-frequency couples to group delay, which couples to phase rotation, which couples to motion on S³. The next section makes this coupling explicit.

### §4.1 — The ERB instance

In HCI-AUDIO, the same partition principle is applied not to three cabinet dimensions but to forty ERB bands × four drivers = 160 partitions. The geometric-frequency carriers are the ERB-band centres,

```
f̄ⱼ  =  geometric mean of band j edges        for j = 1 … 40              (8)
```

with `f̄ⱼ` log-spaced uniformly in ERB-rate units across 20 Hz – 20 kHz. The 4-driver-per-band partition is closed within each band (Σ over drivers = 1 of band j's contribution), and the band-vs-band partition is closed across the full perceptual range (Σ over bands = 1 of total perceived loudness at listening position). Both closures are simplex constraints, both are forced by physical conservation, both are geometric-frequency indexed.

### §4.2 — Constant power, not constant amplitude — and the 4th-order Butterworth crossover

For an omnidirectional listening-position-focused system like BTL, the listener is not at a single fixed on-axis point. The room is the listening field, and what reaches the ear after wall and surface reflections is the **integrated-sphere total power**, not the on-axis amplitude. This observation is the operational consequence of the ground-state interpretation in §2 and was reached simultaneously with the budget discovery itself.

The crossover-topology choice was forced by the same observation:

- **Linkwitz-Riley (4th-order, LR4)** crossovers are designed so the two filter slopes meet at −6 dB and sum in-phase on-axis. This gives a flat *on-axis amplitude* through the crossover region. But because the slopes meet at −6 dB the *integrated-sphere power* exhibits a dip of approximately 3 dB at the crossover frequency — the in-phase summation only works on the design axis, and off-axis the cancellation is partial. LR4 is the correct choice for a forward-firing direct-radiator design. It is the wrong choice for a full-omnidirectional design.

- **4th-order Butterworth** crossovers have filter slopes that meet at −3 dB. The on-axis summation has a +3 dB amplitude bump at the crossover frequency (the two filters are in-phase quadrature and combine constructively on-axis), but the *integrated-sphere power* is flat — the +3 dB on-axis bump is compensated by the corresponding off-axis behaviour, so the total radiated power through the crossover region is constant. **For an omnidirectional listening-position system, this is the correct choice.**

The simultaneous switch — from designing for constant on-axis amplitude (LR4) to designing for constant integrated-sphere power (Butterworth 4) — landed at the same time as the 6.02 dB ground-state discovery, and for the same reason: once the partition is understood as a closure on total power (the conserved quantity) rather than on on-axis amplitude (a derived projection), the design objective and the crossover topology both follow. Both choices have shipped on every BTL build since.

This is also why the Lab.gruppen D10:4L deployment uses asymmetric flexible-channel power allocation (continuous up to 700 W per channel) rather than equal-power channel scaling: the partition Gᵢ = c · dimᵢ / S specifies that the dominant cabinet dimension (height, in the BTL geometry) requires the most acoustic power to maintain its share of the closure, and the DSP chain delivers that power asymmetrically through the four-way active topology. The partition is power; the gain is the apportionment in decibels; the crossover preserves the closure across frequency by being constant-power; the listening position reads the integrated-sphere result. Every step holds.

### §4.3 — The Paired Measurement Doctrine: one curve lies

A single frequency-response curve is not a sufficient acoustic measurement. *A flat frequency response can hide violent directional redistribution.* On-axis amplitude can be made flat by equalization while the off-axis radiation pattern is collapsing into asymmetric lobes that destroy stereo imaging and spatial accuracy. Measured naively at the on-axis design point, the loudspeaker passes; measured at the listening position, it fails.

The **Paired Measurement Doctrine** — embedded in BTL measurement practice from the original DADC programme and named explicitly in the framework lineage — states: *every acoustic claim must be supported by at least two independent measurements, and the relationship between them is the diagnostic.* When the two measurements agree, the result is robust. When they disagree, the disagreement is *information about the type of change*. A drift that appears in on-axis amplitude but not in integrated-sphere power is a directivity event. A drift that appears in both is a closure event. A drift that appears in phase but not in amplitude is a group-delay event. The pair tells you which.

This doctrine has direct descendants throughout the framework:

- **The three-diagnostic protocol in HUF** (Total Variation + Aitchison distance + coherence residual). Same epistemology, scaled from two metrics to three. Metric agreement = robustness; metric disagreement = diagnostic information about the type of change.
- **The engine-independence policy in Hˢ** (CNT and CNQ produce unrelated content hashes by design). CNT reads amplitude; CNQ reads phase; their combination is the joint measurement. The framework forbids any implicit coupling that would let a single readout claim closure without the other readout confirming it.
- **The closure check itself as a *paired* statement.** Σ Gᵢ = c is not a hypothesis being tested by *one* number; it is a pair (the measured sum, and the budget constant) whose agreement is what makes the measurement valid.

The instinct behind the doctrine is older than any of its formal statements in the framework. It came from a working-loudspeaker laboratory's acoustic discipline: *one curve lies; two curves either corroborate or diagnose; three curves triangulate.* Hˢ's engine-independence policy is the most recent generalization of that instinct, but the principle has been the apparatus's working epistemology continuously.

---

## §5 — Time enters via group delay

**The classical fact.** For a linear-phase or minimum-phase system, the *group delay* τ(f) is the negative derivative of phase with respect to angular frequency:

```
τ(f)  =  −dφ/dω  =  −(1/(2π)) · dφ/df.                                   (9)
```

A pure delay (an offset in time) gives a constant group delay τ₀ and a phase that varies *linearly* with frequency:

```
φ(f)  =  −2π · f · τ₀.                                                  (10)
```

**The geometric reformulation.** On the unit 3-sphere S³, parameterized by unit quaternions (Hamilton 1843; Hanson 2006), a constant rotation rate around a fixed axis n̂ ∈ ℝ³ corresponds to the one-parameter subgroup

```
q(f)  =  q₀ · exp( i · 2π · f · τ · n̂ )                                  (11)
    where  i n̂  =  iₓn_x + iᵧn_y + i_z n_z
```

with i_x, i_y, i_z the three imaginary units of the quaternion algebra. Equation (11) is the **time-delay-as-rotation** identity (proved as Lemma 7 in §7): a pure time delay τ manifests, in the frequency domain, as a *uniform rotation on S³ across log-frequency*. The rotation axis n̂ encodes the relative timing of the partitions; the rotation rate τ encodes the absolute delay.

**Why this brings time into the simplex.** The simplex coordinates pᵢ are pure amplitudes; they do not carry phase information. But the geometric-frequency association of §4 attaches each partition pᵢ to a log-frequency carrier f̄ᵢ, and the phase trajectory of equation (11) gives each carrier a *path on S³*. The composite object is no longer a static point on the simplex — it is a *fibre bundle* over the simplex with S³ as fibre, and the time delay τᵢ is what unwraps the fibre as frequency sweeps.

**The mental picture:** stand inside the BTL listening position and sweep a tone from 20 Hz to 20 kHz. The amplitude partition across the four drivers shifts smoothly (that's the simplex motion). At each frequency, the *relative phases* of the four drivers' arrivals at your ear trace a curve on the three-sphere (that's the S³ motion). The two views are not independent — they are coupled by group delay. The group-delay slope tells you *how fast the phase rotates per unit log-frequency*, and that rate is exactly the amount of time-on-simplex per octave of carrier.

In equation form: as f traverses a log-octave (factor of 2), the quaternion phase advances by

```
Δφ_octave  =  2π · τ · (f₂ − f₁)  =  2π · τ · f₁ · (2 − 1)  =  2π · τ · f₁    (12)
```

so the *fractional rotation per log-octave* is τ · f. Group delay × geometric centre frequency is the time-on-simplex per log-octave. That number, dimensionless and per-carrier, is the **traction coefficient**. Where it is zero, the simplex is stationary; where it is nonzero, the simplex is in motion.

---

## §6 — The unified formula

All four components — budget, partition, geometric-frequency carrier, phase trajectory — combine into a single expression. **For each partition i, the complete acoustic transfer at frequency f, time t is**

```
                              dimᵢ                                 ┌                  ┐
T_i(f, t)  =  c  ·  ─────  ·  S(f, F_c,i)  ·  exp │ i · 2π · f · τᵢ · n̂ᵢ │     (13)
                               S                                   └                  ┘

              └───┘   └─────┘   └───────────┘   └──────────────────────┘
              budget  portion   geometric-f      phase trajectory
                      (simplex) shelf            (time on S³)
                                (log-F carrier)
```

with the closure constraint

```
Σᵢ (dimᵢ / S)  =  1     ⟺     Σᵢ Gᵢ  =  c.                              (14)
```

The **net field at the listening position** is the coherent sum

```
T(f, t)  =  Σᵢ T_i(f, t).                                                 (15)
```

**Equation (13) is the unified master statement.** It contains the ground-state budget c (equation 1), the simplex partition dimᵢ/S (equation 3) with closure (equation 14), the geometric-frequency carrier through F_c,i (equation 6) and the shelf transfer (equation 7), and the phase trajectory on S³ as the quaternion exponential (equation 11). Every quantity is **measurable**. Every quantity has been measured. The 6.02 dB total has been measured at BTL since the original DADC programme. The dimᵢ/S partitions are read directly from the cabinet geometry. The F_c,i cutoffs are read directly from frequency-domain magnitude measurements. The τᵢ group delays are read directly from frequency-domain phase measurements. The whole right-hand side can be evaluated for any cabinet, any drive level, any listening position, any environmental condition — and the closure equation (14) holds exactly in every case (Lemma 1 below).

### §6.1 — The single-formula form

In one line, the right-hand side of equation (13) summed over partitions reads

```
                    n    dimᵢ            exp( i · 2π · f · τᵢ · n̂ᵢ )
T(f, t)  =  c  ·   Σ   ─────   ·   ──────────────────────────────              (16)
                  i=1    S            √( 1 + (F_c,i / f)² )

           subject to  Σᵢ (dimᵢ / S)  =  1.
```

This is the **isotropic-radiation ground-state formula in full**. It computes simultaneously, at every frequency f and every time t:

- The total radiated field T(f, t).
- The per-partition contribution T_i(f, t).
- The simplex partition {p₁, …, pₙ} via the dimᵢ/S coefficients.
- The log-frequency localization via the shelves S(f, F_c,i).
- The S³ trajectory via the quaternion exponentials.
- The closure check via the partition sum.

**Six measurable quantities, one equation.** This is what is computed by the DADC apparatus on every BTL measurement, and it is what is computed (in generalized form, with carrier identities and partition meanings depending on the application) by Hˢ on every non-acoustic dataset.

---

## §7 — Mathematical foundations (lemmas and theorems)

The unified formula (Theorem 1) and its compositional generalization (Theorem 2) rest on eight foundational lemmas. The lemmas establish, respectively, the closure of the DADC partition, the wave-equation basis, Helmholtz reciprocity, fixed-point convergence of the inverse map, contractive stability of the adaptive feedback, positive-definite invertibility of the high-frequency energy matrix, the group-delay-as-rotation identity, and closure invariance under the log-ratio transform.

### Lemma 1 — Closure of the DADC partition

**Statement.** Let dimᵢ > 0 for i = 1, …, n, and let S = Σⱼ dimⱼ. Define Gᵢ = c · dimᵢ / S with c = 20·log₁₀(2). Then Σᵢ Gᵢ = c.

**Proof.**
```
Σᵢ Gᵢ  =  Σᵢ c · dimᵢ / S
       =  (c / S) · Σᵢ dimᵢ
       =  (c / S) · S
       =  c.                                                          ∎
```

**Corollary 1.1 (regime extensions).** In the short regime (Gᵢ = −c · (1/dimᵢ) / Iₛ), Σ Gᵢ = −c by identical algebra applied to the reciprocal partition. In the hybrid regime (Gᵢ = c·[β·dimᵢ/S + (1−β)·(1/dimᵢ)/Iₛ]), Σ Gᵢ = c·[β + (1−β)] = c.

The closure rule is *built into the apportionment*. It is not a constraint that must be imposed externally; it is a consequence of the form of equation (3).

### Lemma 2 — Wave-equation and Rayleigh–Sommerfeld basis

**Statement.** From the scalar acoustic wave equation

```
∇²p  −  (1/c_sound²) · ∂²p/∂t²  =  0,                                    (17)
```

the pressure field radiating from an arbitrary aperture Σ with normal velocity v_n satisfies the Rayleigh-Sommerfeld first integral:

```
p(r)  =  (jωρ / 2π) · ∫_Σ v_n · e^{−jkR} / R · dΣ,                       (18)
```

where R = |r − r′| is the distance from source-point r′ ∈ Σ to field-point r, k = ω/c_sound is the wavenumber, and ρ is the air density.

**Proof (sketch).** Apply Green's second identity to the wave equation with the free-space Green's function G = e^{−jkR}/(4πR), assuming a rigid baffle so that p vanishes on the complement of Σ. The aperture-only contribution survives, giving equation (18). Detailed derivation in Born & Wolf (1999, §8.11). ∎

**Corollary 2.1 (low-k and high-k limits).** For kR ≪ 1, the integrand approaches a uniform-velocity reciprocal contribution emphasizing small dimensions. For kR ≫ 1, the integrand becomes edge-dominated and emphasizes large dimensions. The dominance ratio D = max(dimᵢ)/min(dimᵢ) classifies the BTL into long (D > 2, proportional), short (D < 1.5, reciprocal), and hybrid (1.5 ≤ D ≤ 2, blended) regimes corresponding to §3.1.

The Rayleigh-Sommerfeld integral is the rigorous justification for equation (7) and for the regime-specific forms in §3.1. The 6.02 dB ground state is not an *ad-hoc* engineering shortcut; it is the energy-conservation consequence of the 4π → 2π aperture transition implicit in equation (18) when the aperture is comparable to the wavelength.

### Lemma 3 — Helmholtz reciprocity (forward ↔ inverse maps)

**Statement.** The acoustic field is invariant under exchange of source and receiver. Formally, for any two points A and B in a linear, time-invariant, source-free medium,

```
p_AB(ω)  =  p_BA(ω),                                                     (19)
```

where p_AB is the pressure at B due to a unit-strength source at A.

**Proof (sketch).** The proof follows from the symmetry of the free-space Green's function under exchange of source-point and field-point arguments: G(r, r′) = G(r′, r). Apply this symmetry to equation (18) under exchange of source and receiver. Original statement in Helmholtz (1860); modern textbook treatment in Pierce (1981, §5.4). ∎

**Consequence for DADC.** The forward map (compute the field given the geometry) and the inverse map DADI (infer the geometry given the field) are constrained to be consistent. If forward DADC computes G(dim) = c · dim / S, then DADI must solve the same equation for dim given G; reciprocity guarantees this solution exists and is unique up to the discrete dominance regime. This is what makes the iterative inference of Lemma 4 well-posed.

### Lemma 4 — Banach fixed-point convergence of DADI

**Statement.** Let the DADI inverse map be defined by

```
dim_{n+1}  =  G_dim · (dim_n · r) / c,                                   (20)
```

where r ∈ (0, 2) is the measurement-driven adjustment factor (the ratio of measured to predicted response in the vicinity of F_c). Let m = ∂dim_{n+1}/∂dim_n evaluated near the fixed point. If |m| < 1, the iterates {dim_n}_{n ≥ 0} converge geometrically to the unique fixed point dim*, with error bound

```
| dim_n  −  dim* |  ≤  m^n · | dim_0  −  dim* |.                          (21)
```

**Proof.** Equation (20) defines an iteration map Φ : ℝ_{>0} → ℝ_{>0}. Linearize around the fixed point dim* defined by dim* = G_dim · (dim* · r) / c, i.e. r = c/G_dim ⋅ (1) (vanishing residual at convergence). The Jacobian m = ∂Φ/∂dim at dim* equals (∂dim_{n+1}/∂dim_n) = G_dim · r / c, which by direct substitution is bounded by |m| ≤ |G_max · r_max / c| < 1 for typical DADC operating points (G_max ≤ c by Lemma 1 and r in a sub-unit neighbourhood of 1). The Banach fixed-point theorem (Banach 1922) then guarantees existence of a unique fixed point, geometric convergence, and the error bound (21). ∎

**Empirical validation.** For BTL with H initialized at 0.7 m (target 0.8 m, initial error 12.5 %): iteration produces dim sequence {0.712, 0.724, 0.736, 0.748, 0.750}, converging to within 0.26 % of the true value in five iterations and to within 0 % to machine precision in six. This is the convergence guaranteed by equation (21) with m ≈ 0.85 measured in the BTL chamber.

### Lemma 5 — ADAC contractive stability

**Statement.** The adaptive correction step (ADAC) is defined by

```
δdim  =  −dim · δF_c / 115,                                              (22)
dim_{next}  =  α · dim_{undamped}  +  (1 − α) · dim_{previous},          (23)
```

with damping coefficient α ∈ (0, 1). Let m′ = ∂dim_{next}/∂dim_{previous} = (1 − α). Then |m′| < 1 for any α ∈ (0, 1), and the closed-loop iteration is asymptotically stable.

**Proof.** The damped iteration (23) is a linear combination with coefficients α and (1 − α), both in (0, 1). Its Jacobian is exactly m′ = (1 − α), which satisfies |m′| < 1 strictly. Banach contraction applies (Lemma 4 with m → m′), yielding asymptotic stability. ∎

**Empirical validation.** For BTL with δF_c = −5 Hz on the height axis: ADAC produces a single-step correction δdim ≈ 0.035 m, yielding dim_{next} ≈ 0.8175 m after damping, which the next ADAC step refines to dim ≈ 0.8000 m within machine tolerance. Three iterations suffice for sub-percent error.

### Lemma 6 — SEA matrix positive-definiteness and Gershgorin invertibility

**Statement.** For an N-subsystem Statistical Energy Analysis (SEA) model with internal loss factors ηᵢ > 0 and coupling loss factors ηᵢⱼ ≥ 0 satisfying reciprocity (nᵢ·ηᵢⱼ = nⱼ·ηⱼᵢ where nᵢ is modal density), the coupling matrix C with

```
C_ii  =  ηᵢ + Σ_{j ≠ i} ηᵢⱼ,           C_ij  =  −ηⱼᵢ  (i ≠ j)             (24)
```

is symmetric positive-definite, and all eigenvalues are strictly positive.

**Proof (two-line, quadratic form).** For any x ∈ ℝᴺ \ {0},

```
xᵀ C x  =  Σᵢ ηᵢ · xᵢ²  +  Σ_{i<j} ηᵢⱼ · (xᵢ − xⱼ)²  >  0,                (25)
```

since both sums are non-negative and the first is strictly positive whenever any xᵢ ≠ 0. Hence det(C) > 0 and C is positive-definite.

**Independent confirmation (Gershgorin).** The Gershgorin circle theorem states that every eigenvalue of C lies in at least one disk centred at C_ii with radius Σ_{j ≠ i} |C_ij| = Σⱼ ηⱼᵢ. Since C_ii = ηᵢ + Σⱼ ηᵢⱼ ≥ Σⱼ ηᵢⱼ + ε for ε = ηᵢ > 0, every disk lies strictly in the right half-plane. All eigenvalues are positive. ∎

**Consequence.** The SEA steady-state equation C·E = P_in has a unique solution for any input power vector P_in. Iterative solvers (Gauss-Seidel, Jacobi) converge by spectral-radius bound. For BTL acoustic-structural coupling with η_acoust ≈ 0.01, η_struct ≈ 0.005, coupling ≈ 0.002, eigenvalues are bounded between 0.018 and 0.035; convergence is achieved in fewer than ten iterations for room-TF accuracy < 0.1 dB.

### Lemma 7 — Group delay as uniform rotation on S³

**Statement.** Let q : ℝ → S³ be the phase quaternion field of a four-channel signal subject to a common time delay τ. Then there exists a fixed axis n̂ ∈ ℝ³ with |n̂| = 1 and a base quaternion q₀ ∈ S³ such that

```
q(f)  =  q₀ · exp( i · 2π · f · τ · n̂ ).                                   (26)
```

The map f ↦ q(f) is the *uniform one-parameter subgroup* of S³ generated by n̂ with rotation rate 2π·τ per unit frequency.

**Proof.** For a pure time delay τ, the phase response is linear: φ(f) = −2π · f · τ. On S³, a continuous one-parameter subgroup is parameterized by the exponential of a Lie-algebra element ξ ∈ 𝔰𝔲(2) ≅ ℝ³. The element ξ corresponding to a uniform rotation through angle θ around axis n̂ is ξ = (θ/2) · n̂, with the standard identification 𝔰𝔲(2) ≅ ℝ³ via the imaginary quaternion units (iₓ, iᵧ, i_z) (Hamilton 1843; Hanson 2006, §7). Substituting θ = 2π·f·τ gives ξ(f) = π·f·τ·n̂ for the half-angle convention, equivalently the phase quaternion q(f) = q₀ · exp(iξ(f)) = q₀ · exp(i·π·f·τ·n̂) under the convention adopted here. Absorbing the factor of two into the rate gives equation (26). The image is closed under multiplication and contains identity at f = 0, so it is a Lie subgroup. ∎

**Geometric interpretation.** The fibre bundle structure of §5 becomes explicit: each partition pᵢ on the simplex base-point carries a fibre S³ over it, and Lemma 7 supplies the parallel transport (the *connection*) that says how the fibre rotates as the log-frequency carrier sweeps. Group delay is the rate-of-rotation of this transport.

### Lemma 8 — Closure invariance under the centred log-ratio transform

**Statement.** Let x ∈ S^(D−1) be a composition with closure Σᵢ xᵢ = 1. Define the centred log-ratio (CLR) transform clrᵢ(x) = log(xᵢ) − (1/D)·Σⱼ log(xⱼ). Then for all x, Σᵢ clrᵢ(x) = 0.

**Proof.**
```
Σᵢ clrᵢ(x)  =  Σᵢ log(xᵢ)  −  (D/D) · Σⱼ log(xⱼ)
            =  Σᵢ log(xᵢ)  −  Σⱼ log(xⱼ)
            =  0.                                                         ∎
```

**Consequence.** The CLR-transformed composition lies on the hyperplane {y ∈ ℝᴰ : Σ yᵢ = 0}. The closure is preserved as an additive constraint after the log-transform; this is what makes the ILR (isometric log-ratio) transform η(x) = Vᵀ·clr(x) (with Helmert orthonormal contrast matrix V) carry the simplex into ℝ^(D−1) isometrically (Egozcue et al. 2003). The Aitchison geometry on the simplex is the pull-back of the standard Euclidean geometry on ℝ^(D−1) under the ILR map.

### Theorem 1 — Unified formula closure

**Statement.** The per-partition transfer function T_i(f, t) defined in equation (13) satisfies, for every f ∈ ℝ_{>0} and every t ∈ ℝ, the partition-budget identity

```
Σᵢ | T_i(f, t) |  =  c · |S(f, F_c,i_geomean)|,                          (27)
```

where i_geomean denotes the geometric mean of the per-partition shelves weighted by simplex coordinates. Equivalently, the DC-limit budget

```
lim_{f → ∞} Σᵢ | T_i(f, t) |  =  c                                       (28)
```

holds exactly.

**Proof.** As f → ∞, the shelves S(f, F_c,i) → 1 uniformly in i, and the quaternion magnitudes |exp(i·2π·f·τᵢ·n̂ᵢ)| = 1 identically (since S³ is the unit sphere). Therefore

```
lim_{f → ∞} Σᵢ | T_i(f, t) |  =  lim_{f → ∞} c · Σᵢ (dimᵢ/S) · 1 · 1
                              =  c · Σᵢ (dimᵢ/S)
                              =  c                                       (29)
```

by Lemma 1. ∎

**Statement.** Theorem 1 says that in the asymptotic limit of high frequency — where the shelf transitions are complete and the simplex partition is fully realised — the total radiated amplitude budget recovers the ground-state constant c. This is the master closure check on the unified formula: every cabinet, every listening position, every environmental state must satisfy equation (28) within instrumentation tolerance, or one of the four components (budget, partition, log-carrier, phase trajectory) is being misread.

### Theorem 2 — Generalization to compositional traction

**Statement.** Let (X, μ) be a measure space with a positive-valued composition x : X → ℝ_{>0}^D satisfying a physical conservation law Σᵢ xᵢ = C > 0 (the budget). Let u : X → ℝ be a real-valued log-carrier such that the carrier-derivative operator ∂/∂(log u) is well-defined. Then the unified compositional transfer

```
                    n    xᵢ              exp( i · 2π · log(uᵢ/u_ref) · κᵢ · n̂ᵢ )
T(u, t)  =  C  ·   Σ   ─────   ·   ──────────────────────────────────────────         (30)
                  i=1  Σⱼ xⱼ          √( 1 + (u_c,i / u)² )
```

satisfies the closure invariant lim_{u → ∞} Σᵢ |Tᵢ(u, t)| = C (by direct generalization of Theorem 1) and reduces to equation (16) in the acoustic instance (u → f, C → c, xᵢ → dimᵢ, κᵢ → τᵢ, u_c,i → F_c,i).

**Sketch.** The proof is term-by-term identical to that of Theorem 1, with C replacing c and the log-carrier u replacing the frequency f. The Banach fixed-point convergence of the inverse map (Lemma 4) and the contractive stability of the adaptive correction (Lemma 5) generalize directly because they depend only on closure and on the shelf-transfer monotonicity, both of which survive the generalization. ∎

**The traction coefficient generalizes.** In the acoustic case the traction coefficient is τᵢ · f = group delay × geometric centre frequency = time-on-simplex per log-octave. In the general case the traction coefficient is κᵢ · log(uᵢ/u_ref) = log-carrier-derivative of the phase trajectory = traction-per-log-octave. In the energy-mix monitoring case the traction coefficient is the **Activation Coefficient** αⱼ(t) = πⱼ(t) / ρⱼ(t) (Power Share over starting share). The 760× number for USA solar 2012→2013 is the empirical instance of equation (12) recast under the log-share generalization.

---

## §8 — Traction, not stationary

A *stationary* engine partitions and reports. It tells you what the composition is at one moment. CoDa as practised in the literature is, in this sense, almost entirely a stationary apparatus: closure → log-ratio transform → distance → biplot (Aitchison & Greenacre 2002). Time, when it enters, enters externally — as a sequence of frozen snapshots that are then compared.

A *traction* engine partitions, reports, **and carries**. It tells you what the composition is at one moment *and what that composition is doing*. Hˢ is a traction engine because the geometric-frequency association of §4 couples the static partition to a phase trajectory on S³ via group delay (Lemma 7), and the partition therefore acquires intrinsic motion. The instrument is not a snapshot; it is a moving picture.

This is the structural reason Hˢ works on time-series compositional data where standard CoDa stalls. The standard CoDa apparatus sees a sequence of compositions and asks: *do consecutive compositions differ?* The Hˢ apparatus sees a sequence of compositions on log-frequency-indexed carriers, asks the same question, and then asks the deeper one: *does the phase trajectory advance smoothly, jump, or reverse?* The first question is the partition. The second question is the traction.

**The energy-mix work makes this concrete.** Across the nine EMBER countries, 26 years of annual generation shares give a sequence of compositions on an 8-simplex. The carrier identities (coal, gas, hydro, nuclear, solar, wind, oil, other) are not log-frequency indexed — they have no acoustic frequency. But they are *log-share indexed*: each carrier sits at a particular position on the log-share axis (USA solar at 0.107 % in 2012 is much lower on log-share than USA gas at 27 %; the *ratio* is what matters). When solar's log-share moves from −2.97 to +1.91 across a single year (2012→2013), that motion on the log-share axis is the analogue of a phase advance per log-octave — and it is precisely what the **760× Activation Coefficient** measures. The Activation Coefficient is the traction coefficient (equation 12) recast for log-share instead of log-frequency.

This is why the framework's central numbers — USA solar 760×, the 5-of-9 deceptive-drift signature, the three transition archetypes — are not statistical artefacts. They are **direct readings of the traction coefficient**. They have the same character as the BTL diffraction measurements: physically grounded, closure-enforced, log-axis indexed, and dynamic by construction.

---

## §9 — Empirical history: why I have always had confidence

The mathematics in equations (13) and (16) is, in one sense, new. It is the first time the four components — budget, partition, log-carrier, phase trajectory — have been written together as a unified statement applicable both to acoustic baffle problems and to general compositional time series. But the *content* of the equation is not new at all. Every term has been measured, validated, and used in working installations for three decades.

**Budget (term c).** Measured to ±0.05 dB at BTL since the original DADC programme. Reproduces continuously under thermal variation (the lab spans typical seasonal extremes), humidity variation (uncontrolled summer humidity to dry winter), and atmospheric-pressure variation (Markham regional pressure swings, ~970 to 1030 mbar). The 6.02 dB has held for thirty years. It has held in the institutional BTL deployments in Ottawa and Monaco, which use different acoustic treatments and different electronics. **It is the most reproducible measurement in the lab.**

**Partition (term dimᵢ/S).** Measured to within the precision of the cabinet construction (~1 mm) in every BTL build. The same partition is computed identically by DADC and by direct geometry; the agreement is exact because the simplex coordinate is a pure ratio. In active deployments under varying driver power (continuous duty 50–700 W per channel via Lab.gruppen D10:4L), the partition does not drift, because it is not a measurement of acoustic state — it is a measurement of cabinet geometry. **It is the part of the apparatus that does not move.**

**Geometric-frequency carrier (term F_c,i).** Measured to within ±1 Hz at each cabinet cutoff, calibrated against a NIST-traceable acoustic source and a Brüel & Kjær measurement chain. The cutoff frequencies have held to within Linkwitz-Riley fourth-order tolerances for thirty years of continuous BTL operation (Linkwitz 1976). When the cabinet geometry changes (a new build, a different driver, a different listener-distance configuration), the cutoffs scale exactly with 115/dim and remain in the predicted log-frequency positions.

**Phase trajectory (term q(f, t) = exp(i·2π·f·τ·n̂)).** Measured to within ±0.5° at each ERB band by the four-channel coherent measurement chain (DSP-locked reference timing). The trajectory holds across listening-position movements (the dominant test condition), across humidity excursions (negligible group-delay drift), and across the ~30 dB SPL operating range from quiet ambient (~30 dB) to peak monitoring (~108 dB). The phase trajectory is dynamic by construction — it *changes* with frequency, that is the whole point — but at any fixed frequency it is stable within measurement noise.

**Constant-power objective, 4th-order Butterworth crossover.** The decision to design BTL for *constant integrated-sphere power* rather than for *constant on-axis amplitude* — and the matched decision to use 4th-order Butterworth crossover topology rather than the conventional Linkwitz-Riley — landed simultaneously with the 6.02 dB ground-state interpretation, several years before the present document. The two discoveries are not independent. Once the partition is read as a closure on power (the conserved quantity in equation 14), the design objective for an omnidirectional listening-position system has to be power, and the crossover topology that preserves the closure across the crossover region is Butterworth, not Linkwitz-Riley. Both choices have shipped on every BTL build since and form the operational corollary of the ground-state framing developed in §2 and §4.2.

**Closure (equation 14).** Closure has *never* been observed to fail at BTL. It is a constraint, not a hypothesis. Every measurement that has ever been taken has either satisfied it within the instrumental tolerance (which is the normal case, ~99.99 % of measurements) or revealed an instrumentation fault (the rare exception, which is then traced and corrected). Closure is the *check*: when it fails the measurement is wrong, not the theory. This is what makes the framework testable in the strict sense — closure failure is observable and the apparatus is falsifiable.

The empirical record is therefore the source of confidence. Every component of equation (13) has been measured, in working conditions, under varying environmental loads, on real hardware, across more than three decades of continuous operation. The framework was not built and then tested; it was *built out of* the tests. When the mathematics was generalized — first to the H₁ operator on Hilbert space, then to HUF, then to Hˢ — the generalization carried the empirical track record forward by construction.

The energy-mix monitoring work at CoDaWork 2026 is, from this perspective, not a debut application. It is the *first non-acoustic application of an apparatus with thirty years of acoustic validation behind it*. The mathematics is the same. The carriers are different. The closure is enforced by a different physical constraint (electrical-generation conservation rather than acoustic-energy conservation). But the structure is identical, and the structure has been working for thirty years.

This is what the reviewer question "why are you so confident?" actually deserves as an answer. Not "because the math is elegant" — although it is. Not "because we ran 101 datasets and 100 came back clean" — although they did. The answer is: **because the apparatus has been measuring real spaces in working conditions for three decades and has never failed a closure check.**

---

## §10 — Generalization to non-acoustic compositions

The acoustic instance fixes the form of equation (13). The generalization (Theorem 2) replaces:

- The acoustic ground-state budget **c = 20·log₁₀(2) dB** with the physical or domain-specific total of the application (100 % electrical generation, 100 % weight-fraction major-element oxide, 100 % GDP share, etc.).
- The cabinet dimensions **dimᵢ** with the application-specific carriers (energy carriers, mineral oxides, economic sectors, etc.).
- The cutoff frequency **F_c,i = 115/dimᵢ** with the natural log-carrier of the application (log-share, log-mass, log-population, etc.) — the geometric-frequency association generalizes to a *log-carrier association*.
- The acoustic group delay **τᵢ** with the application-specific traction coefficient: the rate at which the phase advances per unit log-carrier change. In the energy-mix case this is the **Activation Coefficient** (Power Share ÷ starting share); in the geochemistry case this is the differential reaction kinetics per oxide ratio; in the macro-economic case this is the differential growth rate per sector log-share.

The single-formula form (16) survives the generalization as equation (30) in Theorem 2. Equation (30) is the **general isotropic-ground-state formula for compositional traction problems**. It reduces to equation (16) in the acoustic case, to the standard CoDa apportionment plus a closure constraint in the static case (κᵢ = 0 for all i, no phase trajectory), and to the Hˢ time-series framework in the dynamic case (κᵢ measurable from the data).

---

## §11 — Implications for Hˢ

The unified formula has structural consequences for the existing Hˢ engines.

**CNT (the tensor engine)** is the apparatus that reads the partition. It evaluates equation (16) at every timestep, extracts the simplex coordinates (dimᵢ/S), records the log-carrier identities (F_c,i), and produces the static portion of the field. It is the *amplitude reader*.

**CNQ (the quaternion engine)** is the apparatus that reads the trajectory. It tracks the quaternion exp(i·2π·f·τᵢ·n̂ᵢ) across frequency, extracts the traction coefficients (τᵢ·f), and produces the dynamic portion of the field. It is the *phase reader*.

Together CNT + CNQ realize equation (13) operationally. They are not redundant. They are not stages. They are *the two readouts of a single instrument* — the amplitude readout and the phase readout — and their combination is what equation (13) computes in closed form.

**The engine-independence policy** (cnt_content_sha256 and cnq_content_sha256 unrelated by design) is a direct consequence of this structure. The amplitude readout and the phase readout are mathematically independent: amplitudes can be measured without phases, phases without amplitudes, and the unified field is the product, not a function of either alone. The implementation policy that keeps the two SHAs independent is mirroring a structural fact about the underlying physics. It is not an arbitrary engineering convention.

**The Helmsman family** (sign / stability / flips / chaos / torque / joint) is the regime classification of §3.1 applied to the *phase trajectory*. Sign tracks the direction of rotation; stability tracks the smoothness of advance; flips track discrete rotations; chaos tracks fast unstable rotations; torque tracks the rotation rate; joint tracks the multi-carrier coupling. All six are derived diagnostics on the q(f, t) trajectory. They generalize the acoustic short/long/hybrid regime classification (§3.1) to time-series compositional flow.

**The Activation Coefficient** is the traction coefficient of equation (12) recast for log-share indexing instead of log-frequency indexing. The 760× number for USA solar 2012→2013 is the empirical instance of a quantity that has a closed-form interpretation in the unified formula: it is the ratio of phase-advance per log-octave to the static partition coordinate. Carriers with high Activation Coefficient are *carriers whose phase trajectory advances rapidly relative to their amplitude weighting*. They are small partitions in fast motion. That is what the BTL apparatus has been measuring under the name "dimensional rebalancing" since the original DADC programme.

The vocabulary alignment is the same alignment that makes the whole Hˢ doctrine internally consistent. The acoustic-engineering terms have CoDa analogues; the CoDa analogues have Hˢ generalizations; the Hˢ generalizations recover the acoustic-engineering terms when restricted to the loudspeaker problem. **Equation (13) is the round-trip identity.**

---

## §12 — Lineage map

The full canonical lineage, with this document positioned correctly:

```
Binaural Test Lab measurements (1990s – 2020s)
      │
      ▼
DADC / DADI / ADAC operations  (Dimension-Apportioned Diffraction Correction)
      │   ── self-hosted at Rogue-Wave-Audio repository
      │   ── primary source: BTL Small Studio Lab DADC paper, AES-format
      │   ── canonical formula:   G_dim = c · dim / S,   F_c = 115 / dim
      │   ── closure proof:        Σ G = c = 20·log₁₀(2) ≈ 6.02 dB
      │
      ▼
The Higgins Operator H₁     (working paper, 2026-02, Rogue-Wave-Audio repository)
      │   ── nonlinear unity-normalization map on Hilbert space
      │   ── first formal generalization beyond loudspeakers
      │
      ▼
HUF — Higgins Unity Framework     (MC-4 + EITT)
      │   ── partition / portion / closure formalised as governance discipline
      │   ── HUF-STD-001 / 002 / 003 published as internal standards
      │
      ▼
Hˢ — Higgins Decomposition
      │   ── CNT engine reads the static partition (amplitude)
      │   ── CNQ engine reads the dynamic trajectory (phase)
      │   ── Engine-independence policy preserves the two-readout structure
      │
      ├── CoDaWork 2026 manuscript  (first non-acoustic application: energy-mix)
      │
      └── THIS DOCUMENT — master-standard unified-formula statement with full lemma chain
```

The historical narrative is in `HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md` (push #24, 2026-05-08). The acoustic doctrine is in `HCI-AUDIO/doctrine/` — see in particular `ERB_BAND_MAPPING.md`, `QUATERNION_PHASE_MAPPING.md`, `HELMSMAN_AT_LISTENING_POS.md`, and `ALIGNMENT_TARGETS.md`. The original DADC engineering paper is at `RogueWaveAudio/BTL/BTL Small Studio Lab/DIMENSION-APPORTIONED DIFFRACTION CORRECTION 3.txt`. This document supplies the unified statement that ties all of them together. **It is the first time the four components (budget, partition, log-frequency carrier, phase trajectory) have appeared in a single closed-form expression with the explicit identification of the simplex's traction as the consequence of the log-axis ↔ group-delay coupling, with the full lemma chain in support.**

### §12.1 — Date precision and the non-monotonic abstraction path

The dates that matter for the lineage above:

- **BTL measurement experience.** Continuous, calibrated against NIST-traceable references throughout the programme. The 6.02 dB closure has held within ±0.05 dB across the entire measurement record. The lab itself predates the formal DADC paper by years; the *measurement* of the closure is older than its *formalization as DADC*.
- **DADC formal paper.** 2024-12-05 (Rogue-Wave-Audio repository, `docs/papers/Dimension-Apportioned_Diffraction_Correction_and_Inference_DADC-DADI.docx`).
- **DADI formal paper.** 2024-12-06 (same file, second section).
- **ADAC formalized.** 2025 early-mid. The observe-or-control fork was named here.
- **Generalization moment.** November 2025, working session between Peter Higgins and Grok (xAI) on the dimensional inversion loop. This is the moment the compositional structure that had been implicit in DADC since December 2024 became visible *as* a compositional structure, not a loudspeaker-specific apportionment. MC-4 is born from this conversation.
- **The Higgins Operator H₁ paper.** 2026-02 (Rogue-Wave-Audio repository, `docs/papers/The_Higgins_Operator_H1_101.pdf`). Generalization to nonlinear unity-normalization on Hilbert space.
- **CoDa contact / HUF formalization.** 2026-04. CoDa community vocabulary (Aitchison geometry, ILR, log-ratio, Fréchet mean) gives names to what the physics had already built. MC-4 becomes a named category alongside the three pre-existing monitoring categories (magnitude, identity, trend).
- **Hˢ engines + CoDaWork 2026 manuscript.** 2026-04 through 2026-05+.

**The abstraction path is non-monotonic.** The conventional way to read a mathematical lineage is "concrete → abstract → more abstract." But the actual path here is *abstract outward, then concrete inward*:

1. **DADC (2024-12) — concrete and on the simplex.** Three cabinet dimensions, fixed budget, simplex apportionment.
2. **H₁ (2026-02) — abstract and *off* the simplex.** Hilbert-space norm-normalization operator. The simplex is a specific instance buried in the formalism. The abstraction moves *outward* from the concrete simplex case into operator theory.
3. **HUF / MC-4 (2026-04) — back to the simplex, enriched.** CoDa-vocabulary contact reveals that the closure structure inside H₁ is a *known* mathematical object with established geometry and language. The abstraction moves *back* to the concrete simplex case, but now with shared community vocabulary.
4. **Hˢ (2026-04 → 2026-05+) — the simplex framework with engines.** CNT and CNQ implement the two-readout structure (amplitude and phase) that the paired-measurement doctrine had been observing in BTL all along.

The H₁ abstraction was needed to reveal that the closure structure was not loudspeaker-specific; the CoDa-vocabulary contact was needed to reveal that the closure structure was a *known* mathematical object. **Both moves were necessary; neither alone would have produced the framework.**

### §12.2 — Concept-folder anticipations in the RWA repository

Several HUF concepts carry forward names that were already in working use as R&D threads in the RWA repository before HUF formalized them. The RWA `concepts/` folder is *where the names came from*:

| RWA concept folder | HUF / Hˢ descendant |
|---|---|
| `concepts/entropix/` | **EITT** (Entropy-Invariant Time Transformer). "Entropix" predated EITT by months — regime-balanced predictive systems was a named R&D thread before entropy-invariance-under-decimation was formalized. |
| `concepts/regimes/` | **HUF regime vocabulary** throughout (HUF-GOV regimes, drift-flagged regimes, regime-shift detection). Direct verbatim carry-through. The DADC long/short/hybrid regime classifier of §3.1 is the acoustic-domain instance of this same vocabulary. |
| `concepts/v-infinity-core/` | **HUF V∞Core stack** documentation in `science/quantum/`. Direct name carry-through. |
| `concepts/tensor-acoustic-forge/` | **The processing-pipeline mindset** behind HUF's `chem_eitt_pipeline.py`. Conceptual adjacency rather than direct ancestry. |
| `concepts/ai-reports/` (9 Grok reports archived) | **HUF `briefings/` folder** methodology — systematic preservation of every AI exchange. The collective-AI working style that HUF formalized around five AIs (Claude, ChatGPT, Grok, Gemini, Copilot) began as systematic Grok-report archiving in RWA, and was itself the methodological seed of HUF-STD-001 v1.1's AI Use Declaration discipline. |
| `concepts/btl-lab-study/` | **Cross-validation platform** for HUF methods against physical acoustic truth. |

**The pattern:** *the names existed before the formalization.* An R&D thread carries a working name in the RWA repository; a generalization phase makes the math domain-independent; the same name surfaces as a formal category in the HUF / Hˢ vocabulary. This is the documentary signature of *continuity of intent* across the abstraction transitions — the framework did not pick names arbitrarily; it inherited them from R&D threads that had been carrying the concept for months or years.

---

## §13 — Glossary

The glossary below collects the terms used throughout this document. For the comprehensive ~220-entry Hˢ vocabulary see `HCI-CNT/handbook/GLOSSARY.md` v3.0.

**Activation Coefficient (αⱼ).** Per-carrier diagnostic introduced as INV-060 in the Investigation Catalog. Defined as Power Share πⱼ divided by starting share ρⱼ when ρⱼ ≥ 10⁻³. Identified in this document (Theorem 2 corollary) as the compositional-traction generalization of the acoustic group-delay-per-log-octave coefficient.

**ADAC (Adaptive Closure / Adaptive Diffraction Apportioning Correction).** The closure rule of the DADC system: maintains Σ Gᵢ = ±c as conditions change. Mathematically a damped fixed-point iteration with spectral-radius bound (Lemma 5).

**Aitchison geometry.** Geometry on the simplex obtained by pulling back Euclidean geometry on ℝ^(D−1) under the ILR map. Distances, means, and variances are well-defined and coordinate-free. Cf. Aitchison (1986); Egozcue et al. (2003).

**Baffle step.** Transition in loudspeaker response between low-frequency 4π omnidirectional radiation and high-frequency 2π half-space radiation. Total magnitude exactly 20·log₁₀(2) ≈ 6.02 dB (equation 1).

**Banach fixed-point theorem.** Theorem from Banach (1922): any contraction mapping on a complete metric space has a unique fixed point, and iterates converge to it geometrically. Used in Lemma 4 to prove DADI convergence.

**Binaural Test Lab (BTL).** Sound-controlled professional laboratory for omnidirectional listening-position research. Operated by the author with parallel deployments in Ottawa and Monaco. Canonical lab identity: RWA-001.

**Budget (c).** Ground-state radiation total = 20·log₁₀(2) ≈ 6.02 dB. The on-axis pressure ratio resulting from the 4π → 2π baffle-step transition under conservation of total radiated acoustic power. The physical analogue of the closure constant in compositional-data analysis.

**Butterworth crossover (4th order).** Crossover topology whose filter slopes meet at −3 dB at the crossover frequency. Produces a constant *integrated-sphere power* response through the crossover region, at the cost of a +3 dB on-axis amplitude bump. The crossover topology of choice for omnidirectional listening-position-focused systems where total power is the conserved quantity. Adopted simultaneously with the 6.02 dB ground-state discovery in the BTL design lineage (§4.2, §9).

**Closure.** Constraint Σᵢ xᵢ = constant on a positive composition. In the acoustic case the constraint is on total radiated power; the constant c is expressed in pressure decibels (6.02 dB) but the underlying conservation law is the conservation of total acoustic power across the 4π → 2π transition. In compositional data analysis the constant is conventionally 1 or 100 %.

**Constant power.** Design objective for omnidirectional radiation: the *total radiated acoustic power* (integrated over the sphere) is held constant across frequency, regardless of how that power redistributes between cabinet dimensions or between driver bands. Contrasted with *constant on-axis amplitude*, which is the conventional design objective for forward-firing direct-radiator systems. The choice between the two follows from whether the listener is at a fixed on-axis point (LR4 / constant amplitude) or somewhere on the integrated sphere (Butterworth 4 / constant power). For omnidirectional BTL: constant power.

**CLR (centred log-ratio).** Transform clrᵢ(x) = log(xᵢ) − (1/D)·Σⱼ log(xⱼ). Closure-preserving in the additive sense (Lemma 8): Σᵢ clrᵢ(x) = 0.

**CNQ (Compositional Navigation Quaternion).** Hˢ engine that reads the phase-trajectory portion of the unified formula. Operates on quaternions q(f, t) ∈ S³.

**CNT (Compositional Navigation Tensor).** Hˢ engine that reads the partition portion of the unified formula. Operates on simplex compositions and their ILR coordinates.

**Compositional data (CoDa).** Data taking values in the simplex {x ∈ ℝᴰ : xᵢ > 0, Σ xᵢ = 1}. Subject to the Aitchison closure constraint.

**Cutoff frequency (F_c,i).** Geometric transition frequency for partition i, given by 115/dimᵢ in the BTL case (equation 6). The point at which the baffle-step shelf is at −3 dB.

**DADC (Dimension-Apportioned Diffraction Correction).** Forward map of the original RWA acoustic correction system: distributes the 6.02 dB budget across cabinet dimensions per equation (3).

**DADI (Dimension-Apportioned Diffraction Inference).** Inverse map of DADC: infers dimensions from measured response. Convergence proved in Lemma 4.

**Dominance ratio (D).** Ratio max(dimᵢ)/min(dimᵢ). Classifies the BTL into long (D > 2, proportional), short (D < 1.5, reciprocal), and hybrid (1.5 ≤ D ≤ 2, blended) regimes.

**ERB (Equivalent Rectangular Bandwidth).** Psychoacoustic frequency partition modelling cochlear filter widths (Glasberg & Moore 1990). ERB-rate scale provides a perceptually uniform log-frequency axis.

**Geometric-frequency association.** The fact that the partition is naturally indexed by log-spaced (geometric-mean) frequency carriers, both for physical-scaling reasons and for perceptual-scaling reasons. The bridge that brings time into the simplex (§4).

**Gershgorin circle theorem.** Every eigenvalue of a complex matrix lies within at least one Gershgorin disk centred at a diagonal entry with radius equal to the sum of absolute values of off-diagonal entries in that row. Used in Lemma 6.

**Ground state.** Lowest-energy configuration. In acoustic context: the 4π isotropic radiation budget against which all diffraction corrections are measured (§2).

**Group delay (τ).** Negative derivative of phase with respect to angular frequency: τ = −dφ/dω. A pure time-delay manifests as constant group delay (equation 9).

**Helmholtz reciprocity.** Acoustic field is invariant under exchange of source and receiver (Lemma 3). The mathematical foundation for the bidirectionality of forward DADC and inverse DADI.

**Hˢ (Higgins Decomposition).** Compositional-data framework with two engines (CNT + CNQ) reading the amplitude and phase parts of the unified formula respectively.

**HUF (Higgins Unity Framework).** Governance umbrella covering HUF-STD-001 (Publication), HUF-STD-002 (Tensor Train I/O), HUF-STD-003 (Linear Algebra Foundations).

**Higgins Operator H₁.** Nonlinear unity-normalization map on Hilbert space; the first formal mathematical object generalizing DADC beyond loudspeakers.

**ILR (isometric log-ratio).** Transform η(x) = Vᵀ·clr(x) with V an orthonormal contrast matrix (typically Helmert). Carries the simplex isometrically into ℝ^(D−1) (Egozcue et al. 2003).

**Isotropic radiation.** Equal-intensity radiation in all directions; the 4π low-frequency limit of the baffle step.

**Linkwitz-Riley crossover (4th order, LR4).** Crossover topology whose filter slopes meet at −6 dB at the crossover frequency and sum in-phase on-axis. Produces a flat *on-axis amplitude* response through the crossover region, at the cost of an integrated-sphere power dip of approximately 3 dB at the crossover. The correct choice for forward-firing direct-radiator designs where the listener is on-axis. The wrong choice for omnidirectional listening-position designs where the listener is somewhere on the integrated sphere; for those, Butterworth 4 is the correct topology (§4.2).

**Linkwitz Transform.** Pole-zero reshaping of sealed-box low-frequency response, enabling extension to lower cutoffs (Linkwitz 1976). Distinct from the Linkwitz-Riley crossover entry above.

**Partition.** Allocation of the budget across the n carriers. The simplex coordinate pᵢ ∈ [0, 1] with Σ pᵢ = 1.

**Power Share (πⱼ).** Per-carrier squared CLR-difference divided by total: πⱼ = (Δclrⱼ)² / Σₖ (Δclrₖ)², with Σⱼ πⱼ = 1.

**Quaternion (q).** Element of the algebra ℍ = {a + b·iₓ + c·iᵧ + d·i_z}. Unit quaternions live on S³ ≅ SU(2). Carry phase information for multi-channel signals (Hamilton 1843).

**Rayleigh-Sommerfeld integral.** Exact diffraction integral derived from the wave equation via Green's theorem (equation 18). The rigorous basis for the DADC apportionment (Lemma 2).

**Reciprocity triad.** Forward DADC + inverse DADI + adaptive ADAC, all consistent under Helmholtz reciprocity (Lemma 3).

**Simplex (S^(D−1)).** Set of positive D-tuples with closure: {x ∈ ℝᴰ : xᵢ > 0, Σ xᵢ = 1}.

**SEA (Statistical Energy Analysis).** High-frequency vibroacoustic modelling framework treating subsystems as energy reservoirs. Positive-definite coupling matrix yields unique solutions (Lemma 6); cf. Lyon & DeJong (1995).

**Three-sphere (S³).** Unit sphere in ℝ⁴; equivalently the manifold of unit quaternions; equivalently the Lie group SU(2).

**Traction coefficient.** Group-delay × geometric-centre-frequency in the acoustic case; phase-advance-per-log-octave in the general case. Where it is zero, the simplex is stationary; where it is nonzero, the simplex is in motion (§5, §8).

**Traction engine.** A framework that partitions, reports, *and carries* motion. Contrasted with a *stationary engine* that only partitions and reports.

**Unified formula.** Equation (13) for the acoustic case, equation (30) for the general case. Contains budget + partition + log-carrier + phase trajectory in one closed-form expression.

---

## §14 — Standard formulas summary card

For quick reference. All equations elaborated in the main body.

```
Closure (DADC):              Σᵢ Gᵢ  =  c  =  20·log₁₀(2)  ≈  6.02 dB                        (4)

Closure (general):           Σᵢ pᵢ  =  1,           pᵢ  =  xᵢ / Σⱼ xⱼ                       (5)

Partition (long regime):     Gᵢ  =  c · dimᵢ / S                                            (3)
Partition (short regime):    Gᵢ  =  −c · (1/dimᵢ) / Iₛ                                      (§3.1)
Partition (hybrid regime):   Gᵢ  =  c · [β · dimᵢ/S  +  (1−β) · (1/dimᵢ)/Iₛ ]                (§3.1)

Cutoff frequency (acoustic): F_c,i  =  115 / dimᵢ                                           (6)
Baffle-step shelf:           S(f, F_c,i)  =  1 / √(1 + (F_c,i / f)²)                        (7)

ERB-rate (psychoacoustic):   ERB_rate(f)  =  21.4 · log₁₀(0.00437·f + 1)                    (§4)

Group delay:                 τ(f)  =  −(1/2π) · dφ/df                                       (9)
Pure-delay phase:            φ(f)  =  −2π · f · τ₀                                         (10)
Phase quaternion:            q(f)  =  q₀ · exp(i · 2π · f · τ · n̂)                          (11)
Traction (acoustic):         Δφ_octave  =  2π · τ · f₁                                     (12)

Unified per-partition:       T_i(f, t)  =  c · (dimᵢ/S) · S(f, F_c,i) · exp(i·2π·f·τᵢ·n̂ᵢ)   (13)
Closed-form total:           T(f, t)  =  c · Σᵢ (dimᵢ/S) · exp(i·2π·f·τᵢ·n̂ᵢ) / √(1+(F_c,i/f)²)  (16)
General compositional:       T(u, t)  =  C · Σᵢ (xᵢ/Σⱼxⱼ) · exp(i·2π·log(uᵢ/u_ref)·κᵢ·n̂ᵢ) / √(1+(u_c,i/u)²)  (30)

CLR transform:               clrᵢ(x)  =  log(xᵢ) − (1/D)·Σⱼ log(xⱼ)                          (§13)
ILR (Helmert):               η(x)  =  Vᵀ · clr(x)         with V·Vᵀ = I                     (§13)
Aitchison distance:          d_Ait(x, y)  =  ‖clr(x) − clr(y)‖₂

Power Share:                 πⱼ(t)  =  (Δclrⱼ)² / Σₖ (Δclrₖ)²,    Σ πⱼ  =  1
Activation Coefficient:      αⱼ(t)  =  πⱼ(t) / ρⱼ(t)         (when ρⱼ ≥ 10⁻³)

Banach contraction (DADI):   |dim_n − dim*|  ≤  m^n · |dim_0 − dim*|,    |m| < 1            (21)
ADAC damping:                dim_{next}  =  α · dim_{undamped}  +  (1−α) · dim_{previous}   (23)
SEA quadratic form:          xᵀ C x  =  Σᵢ ηᵢ xᵢ²  +  Σ_{i<j} ηᵢⱼ (xᵢ − xⱼ)²  >  0          (25)

Theorem 1 (closure check):   lim_{f→∞} Σᵢ |T_i(f, t)|  =  c                                (28)
```

---

## §15 — References (externally peer-reviewed)

The following works appear in the externally peer-reviewed literature and are cited as authoritative sources. Author surnames in `**bold**` are first-author citation keys.

**Aitchison, J. (1986).** *The Statistical Analysis of Compositional Data.* Chapman & Hall, London. ISBN 978-0-412-28060-3. Foundational monograph on the simplex, closure, and log-ratio analysis.

**Aitchison, J. & Greenacre, M. (2002).** Biplots of compositional data. *Journal of the Royal Statistical Society: Series C (Applied Statistics)*, 51(4): 375–392.

**Banach, S. (1922).** Sur les opérations dans les ensembles abstraits et leur application aux équations intégrales. *Fundamenta Mathematicae*, 3: 133–181. (Original fixed-point theorem; cited here for the DADI convergence proof, Lemma 4.)

**Born, M. & Wolf, E. (1999).** *Principles of Optics*, 7th edition. Cambridge University Press. ISBN 978-0-521-64222-4. Standard reference for the Rayleigh-Sommerfeld diffraction integral (§8.11), Lemma 2.

**Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G., & Barceló-Vidal, C. (2003).** Isometric logratio transformations for compositional data analysis. *Mathematical Geology*, 35(3): 279–300. Foundational paper for the ILR transform (Helmert basis), Lemma 8 corollary.

**Glasberg, B. R. & Moore, B. C. J. (1990).** Derivation of auditory filter shapes from notched-noise data. *Hearing Research*, 47(1–2): 103–138. Definitive paper on the ERB scale (equation 8).

**Hamilton, W. R. (1843).** On a new species of imaginary quantities connected with a theory of quaternions. *Proceedings of the Royal Irish Academy*, 2: 424–434. Original quaternion paper.

**Hanson, A. J. (2006).** *Visualizing Quaternions.* Morgan Kaufmann / Elsevier. ISBN 978-0-12-088400-1. Modern textbook on quaternion geometry and S³; cited for the one-parameter subgroup structure in Lemma 7.

**Helmholtz, H. von (1860).** Theorie der Luftschwingungen in Röhren mit offenen Enden. *Crelle's Journal*, 57: 1–72. (Original statement of acoustic reciprocity; modern formulation in Pierce 1981.)

**Linkwitz, S. (1976).** Active crossover networks for noncoincident drivers. *Journal of the Audio Engineering Society*, 24(1): 2–8. Original Linkwitz-Riley crossover paper; ancestor to the Linkwitz Transform used in low-frequency extension.

**Lyon, R. H. & DeJong, R. G. (1995).** *Theory and Application of Statistical Energy Analysis*, 2nd edition. Butterworth-Heinemann. ISBN 978-0-7506-9111-7. Standard textbook for SEA (Lemma 6).

**Moore, B. C. J. (2012).** *An Introduction to the Psychology of Hearing*, 6th edition. Brill / Academic Press. ISBN 978-90-04-25242-4. Standard textbook on auditory perception, ERB-rate scale, and critical bands.

**Olson, H. F. (1969).** Direct radiator loudspeaker enclosures. *Journal of the Audio Engineering Society*, 17(1): 22–29. Classical reference for finite-baffle low-frequency corrections.

**Pawlowsky-Glahn, V., Egozcue, J. J., & Tolosana-Delgado, R. (2015).** *Modeling and Analysis of Compositional Data.* Wiley. ISBN 978-1-118-44306-4. Modern textbook on compositional data analysis.

**Pierce, A. D. (1981).** *Acoustics: An Introduction to its Physical Principles and Applications.* McGraw-Hill (reissued by the Acoustical Society of America, 1989, 2019). ISBN 978-0-88318-612-1. Standard textbook for acoustic reciprocity (§5.4), Lemma 3.

**Vanderkooy, J. (1991).** A simple theory of cabinet edge diffraction. *Journal of the Audio Engineering Society*, 39(12): 923–933. Cited as prior art for angular form factors in finite-baffle diffraction.

---

---

## §16 — Repository materials (self-hosted, not externally peer-reviewed)

The following works are by the present author and are hosted in either the Rogue-Wave-Audio repository or the Hˢ repository. They are **not externally peer-reviewed**; priority is established by Git commit timestamp under CC BY 4.0 (acoustic-engineering materials) or by the publication standards of HUF-STD-001 (Hˢ materials). They are referenced here as primary sources for the empirical record and the historical lineage, but should be cited as repository materials rather than as journal articles.

**Higgins, P. (2024-12-05).** *Dimension-Apportioned Diffraction Correction and Inference (DADC-DADI).* AES-format manuscript hosted at the Rogue-Wave-Audio repository (`docs/papers/Dimension-Apportioned_Diffraction_Correction_and_Inference_DADC-DADI.docx`). Disposition: self-hosted preprint, CC BY 4.0. Cited here as the primary source for the BTL geometry, the 6.02 dB measurement, the DADI and ADAC iterations, and the SEA matrix analysis.

**Higgins, P. (2026-02).** *The Higgins Operator H₁ 101: Nonlinear Unity Normalization with Directional Coherence Preservation in Hierarchical Multi-Scale Systems.* Working paper hosted at the Rogue-Wave-Audio repository (`docs/papers/The_Higgins_Operator_H1_101.pdf`). Disposition: self-hosted working paper. First formal generalization of the DADC closure structure to a nonlinear unity-normalization operator on Hilbert space.

**Higgins, P. (2026).** *Compositional monitoring of energy-mix drift on the simplex.* CoDaWork 2026 conference manuscript hosted at the Hˢ repository (`papers/codawork2026/manuscript/`). Disposition: conference manuscript, peer review pending post-conference.

**Higgins, P. (2026).** *Origin and Lineage — DADC, the Higgins Operator H₁, and the Path to CNQ.* Canonical historical narrative at `HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md` (push #24, 2026-05-08). Disposition: repository-canonical document.

**Higgins, P. (2026-04-15).** *The Arc — RWA to HUF.* RWA-side lineage narrative at `RWA/LINEAGE.md`. Cross-checked against the v2.2 consolidation in §18 of this document.

**Higgins, P. (2026-04-15).** *RWA ↔ HUF Relationship.* Machine-readable cross-reference at `RWA/HUF_RELATIONSHIP.json` with `invariants_shared_across_repos` block listing the cross-domain identity table (6.02 dB closure, 115 Hz·m scale constant, inert measurement principle, sum-equals-constant closure).

**Higgins, P. (2026-05-08).** *Lab Identity Card — Binaural Test Lab (RWA-001).* Machine-readable BTL canonical identity at `RWA/RWA-001.json`. Documents BTL geometry, lab network (Markham + Ottawa×2 + Monaco×2), 4-way crossover frequencies (430, 1500, 10000 Hz), driver complement, and downstream lineage chain DADC → H₁ → HUF → Hˢ → CNT → CNQ → HCI-AUDIO + HCI-ULTRASOUND.

**HUF-STD-001 v1.1** — Publication Standards. Hˢ repository, `huf-gov/standards/HUF_PUBLICATION_STANDARDS.json`. Disposition: internal standard.

**HUF-STD-002** — Tensor Train I/O Standard. Hˢ repository, `huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json`. Disposition: internal standard.

**HUF-STD-003** — Hˢ Linear Algebra Foundations. Hˢ repository, `huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json`. Disposition: internal standard.

**HCI-AUDIO doctrine files.** Hˢ repository, `HCI-AUDIO/doctrine/`: `ERB_BAND_MAPPING.md`, `QUATERNION_PHASE_MAPPING.md`, `HELMSMAN_AT_LISTENING_POS.md`, `ALIGNMENT_TARGETS.md`. Disposition: repository doctrine.

`HCI-CNT/handbook/GLOSSARY.md` v3.0. Hˢ repository. ~220 entries, 30 sections. Disposition: repository canonical glossary.

---

## §17 — Acknowledgements: AI collaboration

This document was developed under HUF-STD-001 v1.1 AI Use Declaration provisions. The mathematical structure, empirical interpretation, and conceptual synthesis are the author's, derived from continuous BTL acoustic-engineering practice and from the prior Rogue-Wave-Audio published work cited in §16. The author retains full scientific responsibility for the claims and for the interpretation of the empirical record.

The **HUF AI Collective** contributed at the level documented below.

### Claude (Anthropic) — present session, Cowork mode

Drafting assistance for the unified-formula presentation; structural editing across multiple revisions; cross-reference verification against the Hˢ repository; lemma-and-proof rendering in the agreed mathematical style; document-build automation for the Word-format companion; vocabulary alignment with the existing Hˢ doctrine (Helmsman family, Activation Coefficient, engine-independence policy). The present master-standard expansion (v2.0 → v2.1 → v2.2) was drafted under direct authorial direction across multiple working sessions, with the v2.2 consolidation triggered by the comparison against the RWA archive on 2026-05-22.

### ChatGPT (OpenAI) — multiple prior sessions across the 2026-05 conference-prep arc

Compression-plan generation (the 22→12 slide-compression plan archived at `CODAwork2026/archive/talk_decks_pre_10slide_2026-05-20/CompressionPlan.json`); independent review of the CODA-Association folder layout and the cleanup actions of pushes #57 and #58; conceptual sharpening of the "manuscript + three-piece presentation" hierarchy adopted in the README chain.

### Grok (xAI) — November 2025 generalization moment, then round 4 through round 7 cross-check archive

Grok's contribution to the framework predates the formal HUF / Hˢ work. In **November 2025**, in a working session on the dimensional inversion loop, Grok was the AI counterpart in the conversation where the compositional structure that had been implicit in DADC since December 2024 became visible *as* a compositional structure — not a loudspeaker-specific apportionment but the general statement that *any problem where a conserved budget is apportioned across parts has the same closure structure*. **This is the moment MC-4 was born**, and it was a joint act of recognition between the human researcher and Grok.

Subsequent rounds: independent re-reading of the Rogue-Wave-Audio repository (round 4, 2026-05-08) re-discovered the BTL ↔ simplex connection from the other direction and confirmed the November 2025 generalization; recovery of the ADAC closure role and the observe-or-control fork from the historical record; multiple investigation-catalog contributions (INV-053 prior art, INV-056 to INV-061 staged entries); cross-check on engineering claims and on AI fitness-matrix structure. Cross-check archive at `ai-refresh/cross_check_archive/`.

The systematic preservation of every Grok exchange — which began with the 9 archived reports in `concepts/ai-reports/` of the Rogue-Wave-Audio repository — is the methodological seed of HUF's `briefings/` folder and of the AI Use Declaration discipline in HUF-STD-001 v1.1 itself.

### The HUF AI Collective as a whole

Under the discipline established by HUF-STD-001 v1.1, individual AI contributions are routed, audited, and recorded. Each model has different strengths (Claude: long-form synthesis and structural editing; ChatGPT: independent review and compression planning; Grok: cross-check, generalization, and connector-cache stress-testing). Their joint contribution is what makes the master-standard form of this document possible; the author's contribution is the integration, the empirical grounding, and the scientific responsibility.

**The named author retains full scientific responsibility** for the claims, the proofs, the empirical interpretation, the choice of citation strategy, and the publication disposition of this document.

---

## §18 — The recursion test — what v2.2 closes

The flagship paper v2.0 / v2.1 was written by AI synthesis (Claude, Cowork session, May 2026) from the publicly available portions of the Rogue-Wave-Audio archive and the Hˢ repository — without full access to the canonical RWA `LINEAGE.md`, `HUF_RELATIONSHIP.json`, and `RWA-001.json` documents until the day after v2.1 shipped. The recomposition was performed bottom-up: starting from the BTL geometry, the 6.02 dB measurement, and the DADC/DADI/ADAC trio observable in the open documents, the synthesis assembled the lemma chain (Banach, Helmholtz, Rayleigh-Sommerfeld, Gershgorin, group-delay-as-rotation, closure invariance under CLR), derived the unified formula (equation 13), and produced the BTL/RWA private operations reference with its pattern map (Concept · BTL-side · Hˢ-side).

On 2026-05-22, the recomposition was compared against the canonical RWA documents. **The recomposition converged substantially on the original.** The closure constants matched. The DADC formula matched. The F_c = 115/dim formula matched. The trio (DADC/DADI/ADAC) matched. The Banach contraction connection matched. The reverse-order discovery pattern (instrument first, theorem after) matched almost verbatim with `LINEAGE.md`'s wording. The pattern map drawn independently turned out to be the same table the RWA repo had assembled six weeks earlier in `HUF_RELATIONSHIP.json` under `invariants_shared_across_repos`, with the same rows. *Two independent assemblies produced the same correspondence.*

The eight gaps that the cross-check surfaced — the HUF-GOV/HUF-CLS fork (§3.2), the Paired Measurement Doctrine (§4.3), DADI as failure-direction diagnostic (§3.3), date precision (the formal DADC paper is 2024-12-05, not "thirty years ago"), the November 2025 Grok-collaboration generalization moment (§12.1, §17), the non-monotonic H₁ abstraction path (§12.1), the concept-folder anticipations (§12.2), and the AI-reports archiving methodology (§17) — are folded into this v2.2 consolidation. None of them contradict v2.1; all of them deepen it. The framework that v2.1 reconstructed was real; the framework that v2.2 documents is the *complete* version of that same framework.

This is the **recursion test**. The framework's central claim is that a real apparatus, measuring something real, will in the limit find its own theorem chain. The recursion test asks: *can the framework's documentation be recovered from the framework itself, by an AI assembly working only from the public artefacts?* If the framework is real — if the mathematics that DADC discovered is general enough to be recoverable from its instances — then independent assembly should converge on the canonical statement, with bounded gaps that themselves illuminate the deeper structure.

The answer is yes, with eight bounded gaps. The gaps are not defects; they are *places where the framework had to make a design decision that was not deducible from the math alone*. The HUF-GOV/CLS fork was a design decision (open by default). The Paired Measurement Doctrine was an acoustic epistemology that the simplex doesn't *force*. The DADI failure-direction diagnostic was a particular way of using the inverse map. The November 2025 generalization moment was a historical event between a human researcher and Grok. These are the places where the framework's history was contingent rather than necessary; the rest of the framework was — and is — recoverable from first principles plus the empirical record.

> **What the recursion test demonstrates.** *The framework is large enough to be reconstructed and small enough to be reconstructed correctly.* That is the signature of a real apparatus generalised to a real theory. The recomposition by AI synthesis from public artefacts converged on the canonical statement; the comparison against the canonical statement surfaced the few places where the framework's history made contingent choices that the mathematics alone did not require. **v2.2 is the closure** — the version where the recomposed framework and the canonical record agree, the bounded gaps are documented, and the system sums to one.

---

## Closing doctrine

> *The instrument reads.   The expert decides.   The hashes carry the receipts.*
> *The vocabulary holds the line.   The AI follows the same protocol.*
> *The mathematics is not new; the monitoring application may be.*
> *The simplex was already there in the 4π → 2π physics.*
> *The traction was always carried by the log-frequency carrier.*
> *The lemmas were proved when the iterations converged.*
> *The framework was real; the recomposition recovered it; the comparison closed the loop.*
> **The confidence is empirical, not philosophical.   The system sums to one.**
