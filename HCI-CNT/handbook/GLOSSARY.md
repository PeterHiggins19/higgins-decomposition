# Hˢ — Canonical Glossary and Notation (v3.0)

**Version:** v3.0 — comprehensive merged reference (2026-05-19). Replaces v2.0 GLOSSARY + NOTATION_AND_TERMINOLOGY.
**Status:** AUTHORITATIVE. This is the single source of truth for every term used across the Hˢ / HUF / CoDaWork repositories.
**Companion (legacy redirect):** [`NOTATION_AND_TERMINOLOGY.md`](NOTATION_AND_TERMINOLOGY.md) now forwards to this document.
**Author:** Peter Higgins · Rogue Wave Audio · Binaural Test Lab · Markham, Ontario, Canada
**Conforms to:** HUF-STD-001 v1.1 (Publication Standards) · HUF-STD-002 (Tensor Train I/O) · HUF-STD-003 (Linear Algebra Foundations).

---

## How to use this document

This is both a **narrative glossary** (read entries in sequence to learn the vocabulary) and a **locked notation reference** (cite specific entries to resolve ambiguity in any other document). The merger of GLOSSARY v2.0 and NOTATION_AND_TERMINOLOGY v2.0 was directed by Peter on 2026-05-19, with explicit instruction to include simple terms (e.g. PCA, eigenvalue) alongside obscure ones (e.g. EITT, LIMIT_CYCLE_P2) and to cover every HUF and CoDa term used in the repo.

**Citation form in other documents:**

> Notation: see Hs/HCI-CNT/handbook/GLOSSARY.md v3.0 (2026-05-19).

**Coverage scope.** Approximately 220 entries across thirty sections. Every term used in the conference manuscript, the speaking script, the talk deck, the cinema scroll, the projector, the Investigation Catalog, the HUF governance charter, and the three HUF standards JSONs is defined here.

---

## Contents

§1 [Foundational mathematics](#1) · §2 [Statistical concepts](#2) · §3 [CoDa foundations](#3) · §4 [CNT core terms](#4) · §5 [CNQ / Volume IV (quaternion view)](#5) · §6 [HCI instrument family](#6) · §7 [Helmsman family](#7)
§8 [Tensor order vs rank](#8) · §9 [κᴴˢ vs s_j sensitivity](#9) · §10 [Frame, dimension, coordinate](#10) · §11 [Tier, Stage, Order, Level, Regime, Degree](#11) · §12 [Channel, factor, component, field](#12) · §13 [Trajectory, path, walk, sequence](#13) · §14 [Closure, invariance, signature, period](#14) · §15 [Engine, ledger, output, plate](#15)
§16 [HUF Standards](#16) · §17 [Seven Linear-Algebra Foundations](#17) · §18 [Stage 0 / Foundations Plate / Dual-View](#18) · §19 [Power Share / Activation Coefficient](#19) · §20 [Canonical findings](#20) · §21 [MC-1 through MC-4 hierarchy](#21) · §22 [Other locked doctrines](#22) · §23 [Output conventions](#23) · §24 [Change control](#24)
§25 [Instrument-family and lineage names](#25) · §26 [Standard symbols](#26) · §27 [Standard formulas](#27) · §28 [Abbreviations A–Z](#28) · §29 [Citation policy](#29) · §30 [Maintenance log](#30)

---

<a id="1"></a>
## §1 — Foundational mathematics

The terms below are standard mathematical concepts used throughout the framework. They are not Hˢ-specific; they are listed here so any reader can resolve a term in one place.

**Centroid.** The average of a set of points, weighted equally; in CoDa, the geometric centroid of the trajectory in CLR or ILR space (see §3).

**Covariance matrix.** A symmetric matrix `Σ` whose entry `Σ_ij = Cov(X_i, X_j)` measures the joint variability of variables `X_i` and `X_j`. In CoDa, `Cov(clr(X))` is the central object of CoDa-PCA.

**Determinant.** The scalar `det(A)` measuring the signed volume change a linear transformation `A` applies to its input space. `det(A) = 0` ⟺ `A` is singular (non-invertible).

**Eigenvalue (λ).** A scalar such that `A·v = λ·v` for some non-zero `v`. The eigenvalue says *how much* the matrix `A` scales along direction `v`.

**Eigenvector (v).** A non-zero vector unchanged in direction (up to scaling) by `A`. For a symmetric matrix the eigenvectors form an orthonormal basis (Spectral Theorem, §17).

**Eckart–Young theorem.** The optimal rank-k approximation of a matrix `M` is obtained by truncating its singular value decomposition (SVD) to the top-k singular values. The justification for low-rank approximations used in Stage 2 CoDa-PCA and Stage 3 attractor fits.

**Euclidean space (ℝⁿ).** The familiar n-dimensional space with the usual dot product and distance. ILR coordinates of a composition live in `ℝ^(D−1)` and behave as Euclidean.

**Frobenius norm.** `‖A‖_F = √(Σ_ij a_ij²)`. The Euclidean norm of a matrix viewed as a vector. Used in foundations residual checks.

**Gram matrix.** `G = AᵀA`; symmetric positive-semidefinite. The Helmert basis satisfies `H·Hᵀ = I` — its Gram matrix is the identity (orthonormality certificate).

**Hyperplane.** An (n-1)-dimensional flat subspace of ℝⁿ. The CLR image of the simplex is the hyperplane `Σ_i clr_i = 0` in ℝ^D.

**Identity matrix (I).** Square matrix with 1s on the diagonal, 0 elsewhere. `I·v = v` for every vector `v`.

**Involution.** A function `f` such that `f(f(x)) = x`. The framework uses two: matrix involution `M² = I` (foundations, §4) and quaternion conjugation `(q*)* = q` (Volume IV, §5).

**Linear map / linear transformation.** A function `T: V → W` with `T(αx + βy) = α T(x) + β T(y)`. Every Hˢ pipeline step is a linear map until the CLR transform applies a per-component logarithm.

**Logarithm (natural, ln).** The inverse of the exponential. The CLR transform sits at the heart of CoDa precisely because `ln` converts ratios to differences and turns the simplex's multiplicative geometry into Euclidean.

**Norm.** The length of a vector. Euclidean: `‖v‖_2 = √(Σ v_i²)`. The Aitchison distance is the Euclidean norm of the CLR difference.

**Orthogonal.** Two vectors with inner product zero. Geometric meaning: at right angles.

**Orthonormal basis.** A set of mutually orthogonal unit vectors that span a space. The Helmert basis is the canonical orthonormal basis on the CLR hyperplane.

**PCA (Principal Component Analysis).** An eigendecomposition of a centred covariance matrix that produces the orthogonal directions of maximum variance (PC1, PC2, …) in the data. **In Hˢ, PCA is used four times:** (1) Stage 2 CoDa-PCA biplot of CLR-transformed compositions; (2) the navigation chart (Fig 6 in the manuscript, page 16 of stage23 plates) — PCA of the CLR trajectory; (3) the projector's BARY and ALIGN modes — engine v3.2.0 ILR-Helmert PCA barycenter trajectory; (4) Stage 3 attractor fit local linearisation. PC1 + PC2 captured variance: 90.5% (Germany, most multi-D) → 99.9% (USA, World, most rank-deficient) across the EMBER corpus.

**Positive definite / Positive semidefinite.** A symmetric matrix `M` such that `xᵀ M x > 0` (definite) or `≥ 0` (semidefinite) for every non-zero `x`. Covariance matrices are positive semidefinite.

**Projection (orthogonal).** Mapping a vector onto a subspace by dropping the perpendicular component. The ILR transform is an orthogonal projection from the CLR hyperplane onto `ℝ^(D−1)`.

**Quadratic form.** `xᵀ A x`. The quadratic form of the Aitchison metric tensor is the squared Aitchison distance.

**Rank (matrix).** The dimension of a matrix's column space (or equivalently, row space). The Helmert basis matrix has rank `D−1` for a `D`-dimensional composition.

**Rank-1 / Rank-k approximation.** The best approximation of a matrix by one (or k) outer product term(s) of its SVD. Used for low-dimensional summaries.

**Singular value.** The non-negative square roots of the eigenvalues of `AᵀA`. The SVD `A = UΣVᵀ` lists them in descending order.

**SVD (Singular Value Decomposition).** Factor any real `m×n` matrix `A` as `A = UΣVᵀ` with `U`, `V` orthogonal and `Σ` diagonal. The most general matrix decomposition; the Spectral Theorem is the special case for symmetric matrices.

**Spectral Theorem.** Every real symmetric matrix has real eigenvalues and an orthonormal basis of eigenvectors. The single most important theorem underpinning Hˢ — verified at IEEE floor in Stage-0 Foundations Plates.

**Symmetric matrix.** `M = Mᵀ`. The objects of multivariate statistics (covariance, variation, Gram). See foundation §1 of HUF-STD-003.

**Trace.** `tr(A) = Σ A_ii`. The sum of eigenvalues for diagonalisable matrices; used as a scalar invariant.

**Transpose (Mᵀ).** Reflect a matrix across its main diagonal. For orthonormal `Q`: `Qᵀ = Q⁻¹` (foundation §2 of HUF-STD-003).

**Variation matrix.** In CoDa: `var_ij = Var(log(x_i / x_j))`. Symmetric by construction. The Hˢ Stage-0 plate visualises this directly.

---

<a id="2"></a>
## §2 — Statistical concepts

**Bonferroni correction.** A multiple-testing correction: divide the per-test α threshold by the number of tests. Used in MC-4 case-defeat sensitivity analyses where multiple country-year transitions are tested simultaneously.

**Confidence interval.** The range of values consistent with the data at a chosen confidence level (typically 95%). Hˢ outputs report bootstrap 95% CIs for the headline Activation Coefficient values.

**Effective sample size (`N_eff`).** A correction to the nominal sample size accounting for autocorrelation in time series. For the EMBER 26-year window, `N_eff` is typically lower than 26 because successive years are correlated.

**Feigenbaum constants.** `δ ≈ 4.6692` (period-doubling ratio) and `α ≈ −2.5029` (scaling parameter). Universal constants for the route to chaos via period doubling in one-dimensional unimodal maps. The Helmsman Chaos extension (§7) predicts these to appear at sufficiently strong control parameter.

**Lyapunov exponent.** The exponential rate of separation of nearby trajectories in a dynamical system. Positive Lyapunov exponent ⟺ chaotic behaviour. Used as a diagnostic for proposed Helmsman Chaos regime.

**p-value.** The probability of observing data at least as extreme as the actual data under a stated null hypothesis. The deceptive-drift signature for Germany has `p ≈ 0.0016` (manuscript Result §5).

**Pearson correlation.** Linear correlation coefficient between two variables. Used in legacy non-compositional analyses; in Hˢ replaced by Aitchison-distance comparisons for compositional data.

**Permutation test.** A non-parametric test in which the null distribution is constructed by shuffling labels and recomputing the test statistic. Used in MC-4 case-defeat for the deceptive-drift signature.

**Shannon entropy (H).** `H = −Σ p_i ln p_i` (in nats). The information-theoretic measure of dispersion of a probability vector. For a composition, Shannon entropy quantifies how evenly carriers share the whole.

**`K_eff` (effective number of carriers).** `K_eff = exp(H)`. The exponential of Shannon entropy. Equals D when all carriers are equal; collapses toward 1 as one carrier dominates. Reported in CNT JSON per timestep as `tensor.navigation_concentration_summary.k_eff`.

**Tsirelson bound.** `S ≤ 2√2 ≈ 2.828`. The maximum value the CHSH expression can take under quantum mechanics. Values between the classical bound `S = 2` and Tsirelson are quantum-allowed; values exceeding Tsirelson would violate quantum theory itself. Hˢ-CNQ corpus produces `S ≈ 0.88` for China at D=8 — above the classical bound, below Tsirelson, consistent with quantum-like joint coherence in a strictly classical compositional dataset.

**TV distance (Total Variation).** `TV(p, q) = ½ Σ_i |p_i − q_i|`. The half-L1 norm of proportion differences, bounded in [0, 1]. The true TV distance; distinct from the `L2_drift` metric that earlier engine versions mislabelled as TV (corrected push #41).

**z-score.** Standardised deviation from the mean: `z = (x − μ) / σ`. Used in shock-event detection on the Aitchison distance time series.

---

<a id="3"></a>
## §3 — CoDa foundations

**Aitchison distance.** `d_Ait(x, y) = ‖clr(x) − clr(y)‖_2`. The Euclidean norm of the CLR difference. The natural distance between two compositions on the simplex; invariant under closure and perturbation.

**Aitchison geometry.** The metric-space geometry on the simplex induced by Aitchison's inner product. The single most important framework for compositional data. Aitchison (1986); Pawlowsky-Glahn, Egozcue & Tolosana-Delgado (2015).

**Aitchison inner product.** `⟨x, y⟩_A = clr(x) · clr(y)`. The Aitchison-geometric inner product on the simplex.

**Aitchison metric.** Same as Aitchison distance. Invariant under perturbation and powering (the simplex's intrinsic group operations).

**Aitchison pullback metric.** Same as κᴴˢ (§9): the Riemannian metric on the simplex induced by pulling back the Euclidean metric through the CLR map.

**ALR (Additive Log-Ratio).** `alr_i(x) = log(x_i / x_D)` for one chosen reference carrier `x_D`. Defined for completeness; the framework canonically uses CLR and ILR-Helmert, not ALR.

**Balance.** A single ILR coordinate, interpreted as a log-ratio between two carrier subgroups defined by an SBP.

**Balance dendrogram.** Tree representation of an SBP showing the binary partition at each level.

**Biplot (CoDa-PCA).** A scatter plot of compositional principal components with carrier loadings overlaid as arrows. Stage 2 plate.

**Carrier.** A single fuel / category / part / component within a composition. EMBER uses nine carriers: bioenergy, coal, gas, hydro, nuclear, other fossil, other renewables, solar, wind.

**Closure (C).** `C(x) = x / Σ_i x_i`. The operation that rescales a positive vector to sum to a fixed constant (typically 1). Maps any positive vector to the simplex.

**CLR (Centered Log-Ratio).** `clr_i(x) = log(x_i) − (1/D) Σ_j log(x_j) = log(x_i / g(x))` where `g(x)` is the geometric mean. Image lies in the (D−1)-dimensional hyperplane `Σ clr_i = 0` in ℝ^D. **Teaching alias:** *"close to simplex"* — keeps you in the simplex's neighbourhood, just log-transformed and centred.

**Composition.** A vector of strictly positive numbers, treated as a point on the simplex, where only relative magnitudes matter (the absolute scale is removed by closure).

**Compositional time series.** An ordered sequence of compositions indexed by time.

**Compositional whole.** The meaningful unity that the composition partitions — total electricity generation, sectoral GDP, household-expenditure budget, etc.

**Course directness.** Ratio of net distance (start → end Aitchison distance) to total path length (sum of step Aitchison distances). 1.0 = perfectly straight; → 0 = pure looping. Reported per country in the CNT JSON `tensor.navigation_chart.course_directness`. EMBER values: Germany 0.41 (directional arc), Japan 0.09 (heavy loop), UK 0.36 (jump-and-return).

**Deceptive drift.** Structural concentration or redistribution accumulating behind apparently stable aggregate indicators. Detected when K_eff is declining while structural velocity remains below the series median. The 5-of-9 cross-country signature reproduces in AUS, CHN, GBR, IND, and JPN at annual grain (INV-051).

**Geometric mean (`g(x)`).** `g(x) = (∏_i x_i)^(1/D)`. The natural mean for compositional data; the CLR is defined relative to this.

**Helmert basis / Helmert ILR.** A canonical orthonormal basis on the (D−1)-dim CLR hyperplane, built from Helmert contrast vectors. The default ILR basis used in Hˢ when no domain-specific SBP is preferred.

**Hidden driver.** A small-share carrier whose Activation Coefficient (§19) is large — doing structural work far beyond its compositional weight. The protocol's central diagnostic surfaces these.

**ILR (Isometric Log-Ratio).** `η = Vᵀ · clr(x)` for an orthonormal basis matrix `V`. The canonical orthogonal projection of a composition into `ℝ^(D−1)`, preserving the Aitchison metric isometrically. Egozcue, Pawlowsky-Glahn, Mateu-Figueras & Barceló-Vidal (2003). **Teaching alias:** *"image simplex"* — the simplex's isometric image in normal Euclidean space.

**ILR-Helmert orthogonal triplet.** Hˢ's specific D=4 Stage 1 representation: ILR with a Helmert basis projected to ℝ³, producing the per-timestep orthogonal triplet plate.

**ILR-quaternion.** The ILR-Helmert projection re-expressed as a unit quaternion (axis + angle), valid specifically at D=4. Two names for the same object.

**Navigation chart.** Fig 6 of the manuscript and slides 12–14 of the talk deck — a PCA 2-D projection of the CLR trajectory, identical to page 16 of each per-country stage23.pdf. Course directness is annotated on each chart.

**Perturbation (⊕).** The simplex's group operation: `(x ⊕ y)_i = x_i · y_i / Σ_j (x_j · y_j)`. The compositional analogue of addition; maps the simplex to itself.

**Powering (⊙).** The simplex's scalar action: `(α ⊙ x)_i = x_i^α / Σ_j x_j^α`. The compositional analogue of scalar multiplication.

**SBP (Sequential Binary Partition).** A way to specify which orthonormal basis to use for an ILR by recursively partitioning the carrier set into two groups. Egozcue–Pawlowsky-Glahn vocabulary.

**Simplex (S^(D−1)).** The set of compositions with D positive components summing to 1. The natural sample space of compositional data analysis. Dimension: D−1.

**Size view.** The standard stacked-area chart of composition shares over time. Answers *what carriers are big*; silently hides *which carriers are doing the structural work*. The view the protocol is designed to complement.

**Sub-composition.** A subset of carriers re-closed to sum to 1. Aitchison's "sub-compositional coherence" requires sub-compositional results to be consistent with full-compositional ones; ILR satisfies this.

**Yeast moment.** A specific transition (country, year, carrier) where the Activation Coefficient ≥ 3× and the carrier's starting composition share ≥ 0.1%. The 9-country EMBER corpus contains 406 yeast moments over 2000–2025.

---

<a id="4"></a>
## §4 — CNT core terms

**Amplitude (A).** A scalar diagnostic of the period-2 attractor's strength (magnitude of curvature attractor). Reported per CNT JSON in `depth.higgins_extensions.impulse_response.amplitude_A`.

**Angular velocity (ω).** Channel 2. The bearing's rate of change Δθ/Δt.

**atan2 simplification.** Hˢ's per-timestep bearing computation, `θ = atan2(y, x)`, replacing the alternative `arccos(x · y)`. 3× fewer operations, 10⁷× better numerical stability, AND structurally equivalent to the 1D / single-axis case of the quaternion log map (§5).

**Bearing (θ).** Channel 1. The angular orientation of a CLR-projected pair, computed via atan2. The first of CNT's four channels. In Volume IV terms: the angle component of the quaternion log.

**CBS cube.** The 3D structure used in Stage 2 with three orthogonal faces representing the (ω, κ), (κ, σ), (ω, σ) planes of the trajectory state space. The Higgins time axis runs orthogonal to all three. The three faces correspond to the three quaternion-imaginary basis pairs (ij, jk, ki).

**Channel.** One of CNT's four named per-timestep outputs: θ (bearing), ω (angular velocity), κ (curvature/steering), σ (helmsman). The four channels together describe the trajectory's instantaneous state. In Volume IV: the four channels are the four quaternion components in disguise.

**Curvature (κ).** Channel 3. `Δω/Δt` — the rate of change of angular velocity. Captures trajectory turning.

**Damping (ζ).** A scalar diagnostic of how quickly the trajectory settles toward its attractor. Sets the IR class via threshold rules.

**Depth tower.** Hˢ's recursive depth-sounder operation. Two parallel towers, `curvature_tower` and `energy_tower`, are built by recursive contraction until termination. Reported as `summary.curvature_depth` and `summary.energy_depth`.

**Helmsman (σ).** Channel 4. The signed accumulated angular change — tracks left-handed vs right-handed rotation. In Volume IV: the spinor parity tracker. See §7 for the full Helmsman family taxonomy.

**Higgins scale (H_s).** A scalar trajectory observable — the cumulative Aitchison-distance scale measure used in CNQ dashboard summaries. Hs(t) traces the trajectory's scale evolution; reported as `cnq_view.higgins_scale_trajectory` in CNQ JSON.

**Higgins time axis.** The trajectory's temporal direction, projected through the CBS cube. In Volume IV terms: the scalar (real) axis of the underlying quaternion.

**Information Retention (IR) class — 8-class taxonomy.** Per-trajectory classification into one of: CRITICALLY_DAMPED, OVERDAMPED_EXTREME, LIGHTLY_DAMPED, MODERATELY_DAMPED, DEGENERATE, D2_DEGENERATE, ENERGY_STABLE_FIXED_POINT, CURVATURE_VERTEX_FLAT. Set by threshold rules on amplitude A and damping ζ.

**`LIMIT_CYCLE_P2`.** Curvature termination code: trajectory returns to itself after exactly 2 recursion steps (period-2 attractor). Observed across nearly every substantively-flowing compositional dataset AND on Planck CMB AND on SM neutrino oscillation. **The universal experimental signature of compositional dynamics carrying all three quaternion invariances** (simplex rotation, mass-flow handedness, time-reversal symmetry). Paper 1 — Universal Compositional Invariance Signature.

**`M² = I`.** The metric tensor's involution property — the Banach contraction certificate. Apply M twice, get identity back. Reported per JSON as `M_squared_I_residual`, typically at IEEE floor (~10⁻¹⁷). Equals quaternion conjugation `q → q*`, physically time-reversal symmetry.

**Period-2 attractor.** A trajectory returning to itself after 2 recursion steps but not after 1. The structural signature of LIMIT_CYCLE_P2 termination.

**Termination codes (depth tower).** `LIMIT_CYCLE_P2` (period-2 attractor; the canonical case), `HS_FLAT` (Higgins scale flatline), `OMEGA_FLAT` (angular velocity flatline), `SIGNAL_SHORT` (insufficient length), `ENERGY_STABLE` (energy attractor without curvature). Each is a one-word verdict on the depth-tower fate.

---

<a id="5"></a>
## §5 — CNQ / Volume IV (quaternion view)

**Bi-quaternion (strict).** Element of `ℍ ⊗ ℂ`. The Lorentz-physics / Clifford-algebra meaning. **Distinct from twin-quaternion factoring.** Reserved for explicit Lorentz contexts where it actually applies.

**Central claim (Volume IV).** *CNT measures invariance. CNQ names the algebra that invariance lives in.*

**CHSH joint-coherence.** The Bell-test CHSH quantity `S = E(a,b) + E(a,b′) + E(a′,b) − E(a′,b′)`. Classical bound `|S| ≤ 2`; quantum (Tsirelson) bound `|S| ≤ 2√2 ≈ 2.828`. CNQ computes a compositional analogue from twin-quaternion-factored Joint Helmsmen at D=8. China EMBER 2001–2025 produces `S ≈ 0.88` — above classical bound, well below Tsirelson — consistent with quantum-like joint coherence in a strictly classical dataset.

**Clifford algebra `Cl(D−1)`.** The dimensional generalisation of quaternions. For D=4: `Cl(3)` = quaternions. For D=8: the natural factoring is bi-quaternions (in the SU(2) × SU(2) sense). For arbitrary D: `Cl(D−1)` is the algebra in which the three Volume-IV invariances unify.

**CNQ (Compositional Navigation Quaternion).** The quaternion-native sibling tier to CNT. Engine version 2.0.0, schema cnq/2.0.0. Hamilton-product core with twin-quaternion factoring, SLERP, sandwich product, and CHSH joint coherence diagnostics. Produces the same JSON as CNT but via quaternion algebra rather than channel arithmetic.

**Conjugation (q\*).** Quaternion involution mapping `(a, b, c, d) → (a, −b, −c, −d)`. Negates the imaginary part. Physically: time reversal. Hˢ's `M² = I` is structurally `q → q*`.

**Hamilton product.** Quaternion multiplication: non-commutative, closed under unit quaternions. Expresses cross-dataset comparison as `R(t) = Q₁(t) · Q₂(t)⁻¹`.

**Hamilton's discovery.** William Rowan Hamilton, Dublin, 16 October 1843 — the moment quaternions entered mathematics, carved into Broom Bridge.

**IEEE floor.** `≈ 2 × machine epsilon ≈ 4.441 × 10⁻¹⁶` for double-precision IEEE 754 floats. The smallest difference numerically representable on standard hardware. Volume IV's three confirmations all hit this floor exactly.

**Pure quaternion.** Quaternion with scalar part zero: `q = (0, b, c, d)`. The pure-quaternion subspace is isomorphic to ℝ³.

**Quaternion (unit).** Element of the 3-sphere S³, written `q = a + b·i + c·j + d·k` with `a² + b² + c² + d² = 1`. The four-component algebra discovered by Hamilton (1843).

**Quaternion log map.** Maps a unit quaternion to its axis-angle representation: `log(q) = (atan2(|v|, a) / |v|) · v`, where `v = (b, c, d)`. The 1D case is exactly Hˢ's atan2 bearing step.

**Sandwich product.** `q · v · q*` applied to a 3-vector `v`. Rotates `v` by the rotation that `q` represents in SO(3). For D=4 compositions, the same operation as Aitchison rotation between consecutive Helmert-projected unit vectors.

**SLERP (Spherical Linear Interpolation).** Geodesic interpolation between two unit quaternions on S³. `slerp(q₁, q₂, α) = sin((1−α)Ω)/sinΩ · q₁ + sin(αΩ)/sinΩ · q₂` where `cosΩ = q₁ · q₂`. Replaces linear interpolation in CLR space with the geodesic that respects the simplex geometry.

**Spinor branch / vector branch.** The two sheets of the SU(2) → SO(3) double cover. A trajectory's lift to SU(2) is in either the spinor branch (signed −1, needs 720° to return) or the vector branch (signed +1, needs 360°).

**SU(2) cover of SO(3).** The double cover of the rotation group SO(3) by the unit quaternions SU(2) ≃ S³. Every SO(3) rotation has two preimages in SU(2): `q` and `−q`. For D=4 Aitchison rotations, SO(3) is the rotation group AND SU(2) is its universal cover, so unit quaternions are exact coordinates.

**Twin-quaternion factoring.** Decomposition of a D=8 trajectory into two coupled SU(2) elements `q_A(t), q_B(t)` via the SO(8) ⊃ SU(2) × SU(2) factoring. **This is what INV-029 is about.** Formal name introduced push #27 to disambiguate from strict mathematical bi-quaternions.

---

<a id="6"></a>
## §6 — HCI instrument family

The HCI family (Higgins Compositional Instrument) is the parent name for the canonical engine tier above CoDa and below CNQ.

**ABACUS (proposed).** Acronym placeholder for a future instrument concept. Not currently a defined Hˢ term.

**ADAC.** Application Domain Adaptive Controller — a control-theory concept inherited from the audio-systems lineage (Rogue Wave Audio). Used in DADC documentation as the parent feedback-control discipline. See [`ai-refresh/ORIGIN_DADC_LINEAGE.md`](../../ai-refresh/ORIGIN_DADC_LINEAGE.md).

**Atlas.** The complete plate-suite catalog. Stage 0/1/2/3/4 plates are atlas modules.

**DADC (Direct Active Dual-Coil).** The audio-engineering lineage from which the Hˢ control-theoretic vocabulary derives. Originated at Rogue Wave Audio; documented in [`ai-refresh/ORIGIN_DADC_LINEAGE.md`](../../ai-refresh/ORIGIN_DADC_LINEAGE.md). Provides "closure" and feedback-loop intuitions that inform CNT terminology.

**DCDI (Dominant Carrier Displacement Index).** Formal operator name for the carrier with the largest absolute CLR displacement between consecutive compositions: `σᴴˢ(t, t+1) = argmax_j |h_j(t+1) − h_j(t)|`. The instrument alias is the **Helmsman Index**.

**HCI-AUDIO.** The audio-domain wrapper of HCI. Maps the CNT/CNQ generic vocabulary onto audio measurement (signal level, harmonic distortion, room modes, etc.). Lives at [`HCI-AUDIO/`](../../HCI-AUDIO/) in the repo. Status: doctrine-only (no engine yet); wrappers are JSON-driven.

**HCI-ULTRASOUND.** The ultrasound-domain wrapper of HCI. Same architecture as HCI-AUDIO; different domain vocabulary. Lives at [`HCI-ULTRASOUND/`](../../HCI-ULTRASOUND/). Status: doctrine-only.

**HCI Barycentric Navigation Volume.** The 3D enclosing manifold inside which a CNT trajectory navigates relative to the simplex barycentre. Relates to the CBS cube as the volume whose three orthogonal faces the cube parameterises.

**HCI Spatial Morphographic Analyzer (HCI-VR).** Proposed VR / 3D-renderer instrument for walking through the Barycentric Navigation Volume. Status: design exploration only. The HTML projector (`codawork2026_projector.html`) is the first interactive pilot.

**HLR (Higgins Log-Ratio Level).** The dimensionless natural-log unit in which all HCI plate coordinates are reported. `h_j(t) = ln(x_j(t)) − mean_k ln(x_k(t)) = ln(x_j(t) / g(x(t)))`. Nearest relative: the neper.

**Multiplexed Carrier Section Plate.** The Stage 1 plate convention in which all carriers' sections are rendered under shared geometry on one multi-panel page (XY plan view + XZ bearings + YZ CLR bars + info + legend). Per timestep; the sequence forms the Section Atlas.

**System Course Plot.** The summary terminal page of a Stage 1 plate cine-deck — the trajectory's whole-run course rendered in one frame after the per-timestep section plates.

**Wrapper.** A JSON schema mapping the engine's generic CoDa vocabulary onto a specific application domain (audio, ultrasound, government budget, etc.). Allows the same engine to serve multiple domains by switching wrapper files. Lives at [`HCI-CNQ/wrappers/`](../../HCI-CNQ/wrappers/) in UN-6 locales (en, fr, es, ru, zh, ar).

---

<a id="7"></a>
## §7 — Helmsman family

Locked taxonomy (codified push #37 schema 3.1.0).

| Term | Locked definition | Status |
|---|---|---|
| **Helmsman σ** | The directional channel computed by CNT; the σ channel of the four (θ, ω, κ, σ) | CANONICAL |
| **Sign of the Helmsman** | The sign of σ at any timestep; handedness bookkeeping | CANONICAL |
| **Helmsman Stability `S_σ`** | `1 − (number_of_flips)/(N−1)`; emitted as `helmsman_family.stability_S_sigma.{global, rolling}` | CANONICAL (schema 3.1.0) |
| **Helmsman Flip** | A change in the helmsman index from one transition to the next. | CANONICAL |
| **Helmsman Flips (count)** | Total flips across a window; emitted as `helmsman_family.flips.{total, rolling}` | CANONICAL |
| **Helmsman Sigma Sequence** | Per-timestep carrier-index sequence; emitted as `helmsman_family.sigma[]` | CANONICAL |
| **Helmsman Torque Proxy** | Per-timestep proxy for rate-of-change-of-σ; emitted as `helmsman_family.torque_proxy[]` | CANONICAL |
| **Helmsman Trajectory** | Time series of helmsman indices, σ(1), σ(2), …; plotted with dotted line segments | CANONICAL |
| **Helmsman Chaos** | Onset of irregular Helmsman dynamics via period-doubling cascade (Feigenbaum δ ≈ 4.6692). Diagnostics: positive Lyapunov exponent of σ̂(t), fractal Hausdorff dimension ≈ 0.538 | PROPOSED (INV-009, INV-058) |
| **Joint Helmsman** | Multi-trajectory coupled Helmsman channel from a joint quaternion field; supports CHSH-like correlations | PROPOSED |

**Flip count range across the EMBER 9-country corpus:** 4 (World aggregate, stable) → 17 (Japan, post-Fukushima cascade).

---

<a id="8"></a>
## §8 — Tensor order vs rank (locked terminology)

| Locked term | Definition | Use for |
|---|---|---|
| **Order** (or **valence**) | Number of indices on a tensor | "κᴴˢ is an order-2 tensor", "C_ijkl is order-4" |
| **Rank (matrix)** | Linear-independence count of rows/columns | "Helmert matrix has rank D−1" |
| **Rank (tensor decomposition)** | Minimum number of rank-1 tensors summing to a given tensor (CP rank, Tucker rank) | Only when explicitly doing decomposition |

**Retired usages:** "rank-2 metric tensor" → say **order-2**. "rank-4 coupling tensor" → say **order-4**.

**Standard alignment.** Use of "order" follows Kolda & Bader (2009), Hackbusch (2012), and standard differential-geometry usage for tensor valence.

---

<a id="9"></a>
## §9 — κᴴˢ vs s_j sensitivity

| Object | Symbol | Order | Definition |
|---|---|---|---|
| **Higgins Steering Metric Tensor** | `κᴴˢ_ij(x)` | order-2 | `(δ_ij − 1/D) / (x_i x_j)` — the Aitchison pullback metric on the simplex |
| **Diagonal carrier steering sensitivity** | `s_j(x)` | order-1 | `1/x_j` — a vector of per-carrier sensitivities |

The diagonal of the full tensor is `κᴴˢ_jj = (1 − 1/D) / x_j²`, NOT `1/x_j`. The legacy `κ_{jj} = 1/x_j` formulae in older HCI files are loosely labelling the sensitivity vector `s_j`, not the metric tensor proper.

---

<a id="10"></a>
## §10 — Frame, dimension, coordinate, axis, basis

| Term | Locked meaning |
|---|---|
| **Carrier dimension D** | Number of carriers in a composition |
| **Simplex dimension D−1** | Dimension of S^(D−1) |
| **ILR space dimension D−1** | Dimension of the ILR coordinate space |
| **Frame** | Choice of orthonormal basis on the ILR space. Examples: Helmert frame, principal-ILR frame, named scientific balance frame. Always declared in CNQ output |
| **Basis** | Synonym of frame; use "frame" in narrative, "basis" in matrix algebra |
| **Axis** | One direction of a frame |
| **Coordinate** | A single component of a vector in a declared frame |
| **Projection dimension** | Dimension of the space CNQ projects into for the quaternion view; D−1 for D=4 (no loss), ℝ³ with `captured_step_fraction` for D > 4 |

---

<a id="11"></a>
## §11 — Tier, Stage, Order, Level, Regime, Degree

| Term | Locked meaning |
|---|---|
| **Tier** | Architectural level of the analytics stack: CoDa, CNT, CNQ are tiers |
| **Stage** | Atlas plate stage (0, 1, 2, 3, 4). Output-plate level. Stage 0 added v2.0 per HUF-STD-003 |
| **Order** | Tensor order (number of indices). ALSO: Output Doctrine derivational order (Order 0 raw / 0+ foundations / 1 first-principles / 2 inter-timestep / 3 recursive / 4+ inferential) — context disambiguates |
| **Level** | HLR magnitude scale. The "level" channel of HLR |
| **Regime** | Multi-scale dynamical regime in the HUF sense |
| **Degree** | RESERVED — avoid. If "higher-degree analysis" appears, replace with "higher-order analysis" or be explicit |

---

<a id="12"></a>
## §12 — Channel, factor, component, field

| Term | Locked meaning |
|---|---|
| **Channel** | A scalar stream over time produced by the engine. CNT has four: θ, ω, κ, σ |
| **Factor** | A sub-system in a multi-system decomposition. CNQ twin-quaternion factoring produces two factors `q_A(t), q_B(t)` |
| **Component** | One number — one entry of a vector or one channel value at one timestep |
| **Field** | A function over space or time. Reserve for field-theoretic contexts |

---

<a id="13"></a>
## §13 — Trajectory, path, walk, sequence

| Term | Locked meaning |
|---|---|
| **Compositional time-series** | The raw data: an ordered list of D-vectors over time |
| **Trajectory** | The geometric path through CLR / ILR space defined by the time-series |
| **Path** | Synonym of trajectory in geometric contexts; use "trajectory" in narrative |
| **Walk** | Discrete-step view of the trajectory, for return-map and depth-tower analysis |
| **Sequence** | Index-ordered view; emphasises ordering rather than geometry |

---

<a id="14"></a>
## §14 — Closure, invariance, signature, period

| Term | Locked meaning |
|---|---|
| **Closure (operator C)** | Aitchison's rescale-to-sum-1 operator |
| **Closure (control-system)** | Closing a feedback loop. DADC / ADAC context |
| **Structural invariance** | An algebraic invariance the trajectory carries: SO(D−1) simplex rotation, SU(2) handedness, M² = I metric involution |
| **Invariance signature** | A pattern exhibiting structural invariance. LIMIT_CYCLE_P2 is the framework's named signature |
| **UCIS (Universal Compositional Invariance Signature)** | Paper 1's term for LIMIT_CYCLE_P2 viewed as universal across compositional dynamics |
| **Period (in LIMIT_CYCLE_Pn)** | The period of the depth-tower return map |

---

<a id="15"></a>
## §15 — Engine, ledger, output, plate

| Term | Locked meaning |
|---|---|
| **Engine** | A compiled program: `cnt.py`, `cnq.py`, `cnt.R`, `cnq.R` |
| **Ledger** | An output JSON file with hash-chained provenance |
| **Output** | Artefact a tool produces — ledger, plate, report, experiment record |
| **Plate** | An atlas Stage 0/1/2/3/4 visual diagram output |
| **Foundations Plate** | Stage-0 plate per HUF-STD-003 (variation matrix, Helmert basis check, decomposition tree, eigenvalue scree, orthonormal basis Q, Spectral Theorem residual) |
| **Section Plate** | Stage-1 Multiplexed Carrier Section Plate |
| **ILR-Helmert Triplet Plate** | Stage-1 orthonormal companion to Section Plate |
| **Dual-View Stage 1 Output** | The paired Section + Triplet reading |
| **Power Share Plate** | Forthcoming Stage-1 sibling visualising Power Share + Activation Coefficient |
| **CNQ Dashboard** | Single-page summary of CNQ output per dataset |
| **Standard Stamp** | The colophon page appended to every Hˢ-produced document |

---

<a id="16"></a>
## §16 — HUF Standards (HUF-STD-001/002/003)

| Standard | Title | Scope |
|---|---|---|
| **HUF-STD-001 v1.1** | HUF Publication Standards | AI Use Declaration template, authorship rules (human-only), person-noun convention, hash-chain expectations, versioning, locale support, lockdown discipline, licensing. Conforms to ICMJE / COPE / Nature/Springer / Science/AAAS / WAME / EU AI Act 2024 / arXiv / ACM / IEEE |
| **HUF-STD-002 v1.0** | HUF Tensor Train I/O Standard | The data → CNT → CNQ → vector-output chain. PDF / PNG / SVG standard; PPTX excluded |
| **HUF-STD-003 v1.0** | Hs Linear Algebra Foundations | The seven linear-algebra components every Hs engine and plate generator employs (§17) |

**Standard citation:** *"Conforms to HUF-STD-001 + HUF-STD-002 + HUF-STD-003."*

---

<a id="17"></a>
## §17 — The Seven Linear-Algebra Foundations (HUF-STD-003)

1. **Symmetric Matrix.** `M = Mᵀ`. Covariance, variation, Gram matrices.
2. **Property of Transpose.** Orthonormal `Q`: `Qᵀ = Q⁻¹`. ILR ↔ CLR exact via H, Hᵀ.
3. **Matrix Decomposition.** closure → CLR → ILR; bearing tensor; depth tower; CoDa-PCA.
4. **Eigenvectors / Eigenvalues.** Attractor fit; κᴴˢ sensitivity; CoDa-PCA principal axes.
5. **Spectral Theorem.** Real symmetric → real eigenvalues, orthonormal eigenbasis. Silent justification of most of Hˢ.
6. **Spectral Decomposition.** `Σ = Q Λ Qᵀ`; rank-k truncation (Eckart–Young).
7. **Visualization.** Stage-0 Foundations Plate is the dedicated tier; Stages 1–4 visualise consequences.

Conformance: every new module declares which foundations it employs in its docstring.

---

<a id="18"></a>
## §18 — Stage 0 / Foundations Plate / Dual-View

**Stage 0 (Foundations Plate).** Visualization tier for the seven HUF-STD-003 foundations. One plate per dataset (read **once** — foundations characterize the data's geometry). Two pages per country: six-panel grid + 16-row numeric verification table. Generator: `HCI/codawork2026/stage0_foundations/foundations_plate.py`. Reference output: master PDF `CodaWork2026_FoundationsPlates_2026-05-14.pdf` (19 pages, 9 EMBER countries × 2-page plate).

**Stage 1 Dual View.**
- **Section Plate (CoDa-Standard):** XY plan + XZ bearings + YZ CLR. Answers *"what are the magnitudes at this timestep?"*
- **ILR-Helmert Triplet Plate (Orthonormal):** three orthogonal scatter projections. Answers *"where is the composition in ILR space?"*

Together = **Dual-View Stage 1 Output**. Reference: 503-page master PDF.

---

<a id="19"></a>
## §19 — Power Share / Activation Coefficient

**Power Share.** `power_share_j(t) = (Δclr_j(t))² / Σ_k (Δclr_k(t))²`. Sums to 100% per step. The per-carrier component of squared Aitchison distance.

**Activation Coefficient (α).** `α_j(t) = power_share_j(t) / composition_share_j(t−1)`. Leverage ratio of directional work to size. α > 1: structurally activating; α ≫ 1 (≥ 3×): yeast factor; α ≪ 1: structural ballast. Reported only when composition share ≥ 0.1%.

**Activation Threshold.** α = 1 neutral; α > 1.5 AND power share > 5% is "structurally activating".

**Yeast Factor.** Legacy / informal name for Activation Coefficient.

**Reference numbers (EMBER 9-country corpus, 2000–2025):**
- USA Solar 2012→2013: α = 760× at 0.107% share (Power Share 81.7%)
- France Solar 2010→2011: α = 659× at 0.110% share
- World aggregate Solar 2010→2011: α = 513× at 0.151%
- China Solar 2013→2014: α = 549× at 0.154%
- Germany Solar 2005→2006: α = 333× at 0.214%
- 406 yeast moments total at α ≥ 3× and share ≥ 0.1%

---

<a id="20"></a>
## §20 — Canonical findings

**MC-4 three-conjunct claim** (push #39). *"No monitoring framework in the energy / market-share literature operates natively in Aitchison geometry with formal change detection at the carrier level — three conjuncts combined into one observable stack."* The three conjuncts: Aitchison-native + formal change detection + carrier-level attribution.

**INV-050 metric pair-invariance.** TV distance and Aitchison distance agree on every shock hit/miss verdict across the 9-country EMBER 2001–2025 corpus. Pair-invariance only; broader-family invariance is INV-050.Q2 (open).

**INV-051 deceptive drift 5-of-9.** The deceptive-drift signature fires in 5 of 9 EMBER countries (AUS, CHN, GBR, IND, JPN). Headline: Germany p ≈ 0.0016.

**EITT (Entropy-Invariant Time Transformer).** The geometric-mean decimation step within the Hˢ pipeline that preserves Shannon entropy. Empirical: 0.18% variation in Shannon entropy across 341:1 compression. Canonical reference: [`papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md`](../../papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md). The step is **one operation inside the broader Hˢ pipeline**; the entropy-invariance is the named claim.

**LIMIT_CYCLE_P2 (Paper 1 UCIS).** Period-2 attractor termination across virtually every substantively-flowing compositional dataset AND Planck CMB AND SM neutrino. Three IEEE-floor confirmations:

| Dataset | D | T | Residual |
|---|---|---|---|
| Backblaze drives | 4 | 731 | 4.44e-16 |
| Planck CMB photons | 4 | 2499 | 4.44e-16 |
| SM neutrino oscillation | 3 | 1000 | 4.44e-16 |

Cross-system bit-identity demonstrates the residual is float64 representation, not algorithmic noise.

**INV-059 humble-invitation framing.** Cross-model validation across the HUF AI Collective (ChatGPT session 2 + Grok round 5) converged on the conference talk's humble + methods-challenge + invitation posture.

---

<a id="21"></a>
## §21 — MC-1 through MC-4 (methods-claim hierarchy)

The MC hierarchy frames Hˢ claims by scope:

- **MC-1 — domain claim.** A specific empirical finding within one domain (e.g., "solar peaks at 760× AC in the USA 2012-13 transition"). Falsifiable by reproducing the corpus and showing the number is wrong.
- **MC-2 — cross-domain claim.** The same compositional protocol works in a second independent domain (e.g., the religion study reproduces Activation Coefficient leverage with 148× peaks at 0.5% share). Falsifiable by showing the protocol fails to transfer.
- **MC-3 — universality claim.** The Universal Compositional Invariance Signature (LIMIT_CYCLE_P2) holds across all compositional dynamics that meet the structural preconditions. Falsifiable by exhibiting a substantively-flowing compositional dataset that does NOT exhibit LIMIT_CYCLE_P2.
- **MC-4 — methodological claim.** Compositional structure can be treated as a primary monitoring observable (the three-conjunct claim, §20). Falsifiable via the four defeat paths: prior-art / metric / case / category.

The CoDaWork 2026 talk targets **MC-4**. The manuscript's Discussion lists the four defeat paths explicitly.

---

<a id="22"></a>
## §22 — Other locked doctrines

| Doctrine | What it says |
|---|---|
| **CRD-1.0 (Coherent Range Doctrine)** | Multi-carrier comparisons computed on the intersection of all members' time ranges; shortest-coverage member sets the binding window |
| **SEA-1.0 (Suspicion of Every Assumption)** | Every public function and claim enumerates its failure modes with mitigation evidence; engine guilty until proven innocent |
| **STP-1.0 (Self-Test Protocol / BIST)** | Every engine carries a frozen reference corpus and a runner producing dated, hash-chained pass/fail receipts |
| **Engine independence policy** | `cnt_content_sha256` and `cnq_content_sha256` unrelated by design. Cross-engine hash chains forbidden |
| **Tensor Train v1.0** | The named data → CNT → CNQ → vector-output chain. Four links with locked I/O contracts |
| **Output Doctrine v1.0** | Order/Stage classification of plate outputs |
| **HUF Governance Charter** | Nine-article governance document for HUF + Hs + derivative repos |
| **SAFE-001** | Cognitive-agent safety doctrine governing AI-tool use |
| **LOOP-001 (Skydiver Principle)** | The operator holds the last breaker. Circuit-breaker discipline routes through 16 breakers; Breaker 16 is held by the human and cannot be overridden by automation |
| **KILL-001** | Named-failure-modes catalog (19 modes). Hˢ HAZOP/FMEA equivalent |
| **Hungry Organism frame** | HUF partnership doctrine v4 — Hˢ as the organism that consumes data and produces standards-conformant outputs |

---

<a id="23"></a>
## §23 — Output conventions (HUF-STD-001)

**HUF AI Collective.** Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI). Disclosed in AI Use Declaration sections; NOT in author bylines.

**AI Use Declaration.** Mandatory section at the end of every external-audience document. Lists AI tools, tasks performed, author responsibility, governance.

**Authorship.** Human-only. Standard byline: *"P. Higgins, Rogue Wave Audio"*. AI tools are tools, not authors.

**Person-noun convention.** "human" as person noun → "researcher / user / reader" in general public output. Exceptions: ICMJE authorship rules, AI-safety vocabulary ("human-in-the-loop"), anthropology / demographic studies, regulatory disclosure.

**Document versioning.** Major (1.0 → 2.0): substantive content change. Minor (1.0 → 1.1): clarifications, corrections. Patch (1.0 → 1.0.1): typo and link fixes.

**Date-stamped filenames.** Slide decks and PDFs carry ISO date in filename (e.g., `CodaWork2026_FinalTalk_2026-05-17.pptx`).

**Standard Stamp.** The single-page colophon appended to every Hˢ-produced document — three columns: The Framework / Engines · Methods / Find us · Contact. Reusable helper at `Studies/_shared/hs_standard_stamp.py`.

---

<a id="24"></a>
## §24 — Change control

**HCC (Hs Change Control v1.0).** NASA-style configuration-management discipline. Eight rules HCC-R001..R008 govern what can change and how.

**DCP (Discovery Change Packet).** Formal change-packet template. Status flow: `proposed → in_progress → implemented → verified`.

**CHK rule.** A consistency-checker rule in `scripts/check_ai_refresh_consistency.py`. Live: CHK-JSON-001, CHK-VERSION-001, CHK-INV-001, CHK-CCTT-001, CHK-CNQ-001, CHK-README-001. Post-conference: CHK-FOUNDATIONS-001, CHK-PERSON-NOUN-001.

**Configuration Items (CIs).** 15 baseline CIs defining the framework's controlled surface.

**Interface Controls (IFs).** 5 interface contracts between subsystems.

**Traceability Matrix.** Maps each computational module to its governing doctrine, INV, and standard.

**PRE_CONFERENCE_LOCKDOWN.** Repository-wide protective lockdown 2026-05-12 → 2026-06-06. Allowed: S1-S2 doc fixes, archive entries, DCP filing without execution. Forbidden: engine code changes, claim promotions, NO-CREATE file creation.

**NO-CREATE files.** Six files explicitly marked "do not create during lockdown".

**Severity levels.** S0 = breaks engine determinism. S1 = breaks user-facing claim or doc. S2 = doc / wording / cross-reference.

**Push protocol.** pre-flight survey → admin JSON updates → `PUSHnn_PRE_PUSH_SUMMARY.md` (HOLD) → verification → clear HOLD → `PUSHnn_READY_FOR_COMMIT.md` → commit → post-commit sync.

**CCTT (CNT Compositional Tensor Train) v0.1.** Legacy 7-phase user/AI access protocol. Lets a researcher or AI assistant take a raw compositional CSV and produce a CNT-grade analysis end-to-end with hash-chained provenance. Superseded by the Tensor Train v1.0 doctrine but the runbook is retained for reference at `ai-refresh/CCTT_RUNBOOK.md`.

**Mission Command.** The audit-pipeline module that consolidates per-experiment journals into a master report. Used during the 2026-05-10 full-corpus validation push.

**OPERATIONS_PROTOCOL.** The Gawande-style meta-checklist for the whole repo. 13 transition sections.

---

<a id="25"></a>
## §25 — Instrument-family and lineage names

**BTL (Binaural Test Lab).** Peter Higgins' instrument-development laboratory. The "Lab" affiliation alongside Rogue Wave Audio.

**RWA (Rogue Wave Audio).** Peter Higgins' company. Located in Markham, Ontario, Canada. The "Audio" affiliation. Hosts the parent DADC research lineage.

**HUF (Higgins-Unity-Framework).** The parent governance / philosophy framework. Houses the MC framing, EITT canonical, KILL-001, the governance charter, and the partnership/hungry-organism frame.

**Hˢ (Higgins-Decomposition).** This repository — the deterministic compositional inference engine on the simplex. Child of HUF; the implementation-side family of tools.

**Hs (informal).** Plain-text rendering of Hˢ. Used in filenames and where the superscript can't render.

**V_Core.** A legacy code/concept lineage from earlier Higgins work. Referenced in some AI-refresh narratives as historical context; not part of the current canonical chain.

**Hs-Direct.** A legacy direct-style measurement pipeline. Folder retained for lineage.

**Higgins-Unity-Framework repo.** Sibling repository to higgins-decomposition. Holds HUF governance, MC-1..MC-4 framing, KILL-001 catalog, the partnership matrix.

---

<a id="26"></a>
## §26 — Standard symbols

| Symbol | Meaning |
|---|---|
| **D** | number of carriers (composition dimension) |
| **T** | number of records (timesteps) |
| **N** | number of trajectories in a bundle |
| **x_i, ρ_i** | the i-th carrier's value or share |
| **clr_i(t)** | the i-th CLR coordinate at time t |
| **η(t)** | ILR coordinate vector at time t |
| **θ, ω, κ, σ** | the four CNT channels (bearing, angular velocity, curvature, helmsman) |
| **A, ζ** | period-2 attractor amplitude and damping |
| **q** | unit quaternion |
| **q\*** | quaternion conjugate |
| **v** | 3-vector (typically a Helmert-projected CLR triple) |
| **Q(t)** | trajectory as a quaternion-valued function of time |
| **R(t)** | relative quaternion: Q₁(t) · Q₂(t)⁻¹ |
| **M** | metric tensor (`M² = I`) |
| **H, V** | Helmert orthogonal contrast matrix |
| **κᴴˢ_ij** | Higgins Steering Metric Tensor (order-2) |
| **s_j** | diagonal carrier sensitivity vector `= 1/x_j` (order-1) |
| **S^(D−1)** | the (D−1)-simplex |
| **S³** | the 3-sphere = unit quaternions = SU(2) |
| **α_j(t)** | Activation Coefficient for carrier j at time t |
| **π_j(t)** | Power Share for carrier j at time t |
| **σ̂(t)** | Sign of the Helmsman at time t |
| **K_eff** | effective number of carriers (`exp(H)`) |
| **g(x)** | geometric mean of composition x |

---

<a id="27"></a>
## §27 — Standard formulas

```
Closure:                  C(x)        = x / Σ x_i
Geometric mean:           g(x)        = ( ∏ x_i ) ^ (1/D)
CLR:                      clr_i(x)    = log(x_i) − (1/D) Σ_j log(x_j)
ILR (Helmert):            η(x)        = Vᵀ · clr(x)            with V·Vᵀ = I
Aitchison distance:       d_Ait(x, y) = ‖clr(x) − clr(y)‖₂

Helmsman index:           σ(t)        = argmax_i | clr_i(t+1) − clr_i(t) |
Power Share:              π_j(t)      = (Δclr_j)² / Σ_k (Δclr_k)²,    Σ π_j = 1
Activation Coefficient:   α_j(t)      = π_j(t) / ρ_j(t)              (when ρ_j ≥ 10⁻³)
Shannon entropy:          H(t)        = − Σ ρ_j(t) ln ρ_j(t)
K_eff:                    K_eff(t)    = exp( H(t) )
TV distance:              TV(p, q)    = (1/2) Σ |p_i − q_i|
L2 drift:                 L2(p, q)    = √( Σ (p_i − q_i)² )

CNT bearing (atan2):      θ           = atan2(y, x)
Quaternion log:           log(q)      = (atan2(|v|, a) / |v|) · v
Quaternion sandwich:      v'          = q · v · q*
Hamilton product:         (p · q)_k   = Hamilton 1843 multiplication
Quaternion conjugation:   q*          = (a, −b, −c, −d)
Metric involution:        M² = I      ⟺    (q*)* = q
SLERP:                    slerp(q₁, q₂, α) = sin((1−α)Ω)/sinΩ · q₁ + sin(αΩ)/sinΩ · q₂
                                       where cosΩ = q₁ · q₂

Course directness:        d_directness = ‖clr(T) − clr(0)‖ / Σ_t ‖clr(t+1) − clr(t)‖
PCA on ILR trajectory:    [PC1, PC2]  = top-2 eigenvectors of (Xᵀ X)/(T−1)
                                       where X is centred ILR coordinate matrix
Disk-scaled barycenter:   bary_xy[t]  = (PC1·η(t), PC2·η(t)) · 0.85 / max_t ‖·‖
CHSH joint coherence:     S           = E(a,b) + E(a,b′) + E(a′,b) − E(a′,b′)
```

---

<a id="28"></a>
## §28 — Abbreviations A–Z

| Abbrev | Full term |
|---|---|
| **ADAC** | Application Domain Adaptive Controller |
| **AC** | Activation Coefficient |
| **AKB** | (not currently a defined Hˢ term) |
| **ALR** | Additive Log-Ratio |
| **BIST** | Built-In Self-Test (= STP-1.0) |
| **BTL** | Binaural Test Lab |
| **CBS** | (Curvature-Bearing-Sigma) cube — the 3D Stage-2 visual structure |
| **CC** | Coherent Range (in CRD-1.0) |
| **CCTT** | CNT Compositional Tensor Train (legacy v0.1) |
| **CHK** | Consistency-checker rule prefix |
| **CHSH** | Clauser–Horne–Shimony–Holt inequality |
| **CI** | Configuration Item |
| **CLR** | Centred Log-Ratio |
| **CNQ** | Compositional Navigation Quaternion |
| **CNT** | Compositional Navigation Tensor |
| **CoDa** | Compositional Data Analysis |
| **COPE** | Committee on Publication Ethics |
| **CRD** | Coherent Range Doctrine |
| **DADC** | Direct Active Dual-Coil (RWA audio lineage) |
| **DCDI** | Dominant Carrier Displacement Index (= Helmsman) |
| **DCP** | Discovery Change Packet |
| **EITT** | Entropy-Invariant Time Transformer |
| **EMBER** | The energy think tank (ember-energy.org) — the conference data source |
| **FAO** | Food and Agriculture Organization |
| **FMEA** | Failure Mode and Effects Analysis (related to KILL-001) |
| **HCC** | Hˢ Change Control |
| **HCI** | Higgins Compositional Instrument |
| **HLR** | Higgins Log-Ratio Level |
| **Hˢ / Hs** | Higgins-Decomposition (this repo) |
| **HUF** | Higgins-Unity-Framework (parent governance) |
| **ICMJE** | International Committee of Medical Journal Editors |
| **IEEE** | Institute of Electrical and Electronics Engineers |
| **IF** | Interface Control |
| **ILR** | Isometric Log-Ratio |
| **IR** | Information Retention (CNT class taxonomy) |
| **IRENA** | International Renewable Energy Agency |
| **INV-NNN** | Investigation Catalog entry number NNN |
| **JSON** | JavaScript Object Notation |
| **KILL** | Named-failure-modes catalog (KILL-001) |
| **L2** | L2 drift (Euclidean norm of proportion differences) |
| **LOOP** | Open-loop doctrine (LOOP-001) |
| **MC** | Methods Claim (hierarchy MC-1..MC-4) |
| **NEDA** | National Eating Disorders Association (NOT used by Hˢ; deprecated as a referral) |
| **NO-CREATE** | Files explicitly marked do-not-create during lockdown |
| **PCA** | Principal Component Analysis |
| **PDF** | Portable Document Format |
| **PNG** | Portable Network Graphics |
| **PPTX** | PowerPoint OOXML format |
| **RWA** | Rogue Wave Audio |
| **S0/S1/S2** | Severity classes for changes under lockdown |
| **SAFE** | Cognitive-agent safety doctrine (SAFE-001) |
| **SBP** | Sequential Binary Partition |
| **SEA** | Suspicion of Every Assumption (SEA-1.0) |
| **SHA-256** | Secure Hash Algorithm, 256-bit |
| **SLERP** | Spherical Linear Interpolation |
| **SO(3)** | Special Orthogonal group, 3 dimensions (rotations of ℝ³) |
| **STP** | Self-Test Protocol (STP-1.0) |
| **SU(2)** | Special Unitary group, 2 dimensions (unit quaternions) |
| **SVD** | Singular Value Decomposition |
| **SVG** | Scalable Vector Graphics |
| **TV** | Total Variation (distance) |
| **UCIS** | Universal Compositional Invariance Signature |
| **WAME** | World Association of Medical Editors |

---

<a id="29"></a>
## §29 — Citation policy

Every document using any term defined here SHOULD cite:

> Notation: see Hs/HCI-CNT/handbook/GLOSSARY.md v3.0 (2026-05-19).

A short reference is sufficient. The point is to give downstream readers a single place to resolve ambiguity and to make future term-drift visible.

---

<a id="30"></a>
## §30 — Maintenance log

| Version | Date | Push | Summary |
|---|---|---|---|
| v1.0 | 2026-05-08 | #27 | Initial GLOSSARY — ~53 entries covering Volume IV + HCI + Helmsman family |
| v1.0 (notation) | 2026-05-08 | #27 | Initial NOTATION_AND_TERMINOLOGY — §1–§14 locking tensor order, κᴴˢ vs s_j, frames, channels |
| v2.0 (glossary) | 2026-05-14 | (TBD) | Full refresh — §J HUF Standards / §K Foundations / §L Stage 0 / §M Power Share / §N Findings / §O Doctrines / §P Conventions / §Q Change Control |
| v2.0 (notation) | 2026-05-14 | (TBD) | Full refresh — §13 Standards / §14 Foundations / §15 Order classification / §16 Power Share / §17 Findings / §18 Doctrines / §19 Conventions / §20 Change Control |
| **v3.0** | **2026-05-19** | **(this push)** | **Merged comprehensive reference. Combined GLOSSARY v2.0 + NOTATION_AND_TERMINOLOGY v2.0 into a single authoritative document. Added §1 Foundational mathematics (PCA, SVD, eigenvalue, eigenvector, Spectral Theorem as standalone entries), §2 Statistical concepts (Lyapunov, Feigenbaum, CHSH, Tsirelson, Shannon entropy, p-value, TV distance, K_eff), §3 enriched CoDa foundations (course directness, deceptive drift, hidden driver, navigation chart, yeast moment, size view, perturbation, powering, sub-composition), §4 enriched CNT terms (Higgins scale, termination codes), §5 enriched CNQ (CHSH, sandwich, SLERP, spinor branch, pure quaternion), §6 HCI instrument family (HCI-AUDIO, HCI-ULTRASOUND, DADC, ADAC, wrapper), §21 MC-1 through MC-4 hierarchy (new — only MC-4 was previously documented), §25 Instrument-family and lineage names (RWA, BTL, HUF, Hs, V_Core, Hs-Direct as standalone entries), §28 comprehensive A–Z abbreviations index. Approximately 220 entries. Triggered by Peter directive 2026-05-19: *"check the glossary, seems it needs updating, combine the glossary with the terms and make the glossary and terms complete, include simple and obscure references such as PCA and EITT, all huf and coda terms, make it comprehensive."* |

---

## Related documents

- **Manuscript** — [`papers/codawork2026/manuscript/MANUSCRIPT.md`](../../papers/codawork2026/manuscript/MANUSCRIPT.md)
- **Investigation Catalog** — [`ai-refresh/INVESTIGATION_CATALOG.md`](../../ai-refresh/INVESTIGATION_CATALOG.md)
- **HUF standards JSONs** — [`huf-gov/standards/`](../../huf-gov/standards/)
- **CNQ scope and limits** — [`HCI-CNQ/CNQ_SCOPE_AND_LIMITS.md`](../../HCI-CNQ/CNQ_SCOPE_AND_LIMITS.md)
- **Volumes I–IV** — [Volume I — Theory and Mathematics](VOLUME_1_THEORY_AND_MATHEMATICS.md), [Volume II — Practitioner and Operations](VOLUME_2_PRACTITIONER_AND_OPERATIONS.md), [Volume III — Verification, Reference and Release](VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md), [Volume IV — The Quaternion View](VOLUME_4_QUATERNION_VIEW.md)
- **HCI foundation** — [`HCI/HCI_FOUNDATION.md`](../../HCI/HCI_FOUNDATION.md)

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*CNT measures invariance.   CNQ names the algebra it lives in.*
*The mathematics is not new; the monitoring application may be.*
