# Glossary — Minimal-Now Refresh (Volume IV-touched terms)

**Scope:** terms touched by the Volume IV (Quaternion View) integration of 2026-05-07. Approximately 40 entries.
**Companions:** [Volume I — Theory and Mathematics](VOLUME_1_THEORY_AND_MATHEMATICS.md), [Volume II — Practitioner and Operations](VOLUME_2_PRACTITIONER_AND_OPERATIONS.md), [Volume III — Verification, Reference and Release](VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md), [Volume IV — The Quaternion View](VOLUME_4_QUATERNION_VIEW.md).
**Full refresh planned for a separate cycle.** This document covers the terms used in the central-claim chain so the four volumes are internally cross-referenceable today; the broader CNT vocabulary (atlas modules, schema fields, audit-chain terms) will be added in a dedicated glossary push after CodaWork.

---

## §A — CoDa foundations

**Aitchison metric.** The natural distance metric on the simplex, invariant under the simplex's intrinsic operations (perturbation and powering). Distances measured in Aitchison metric correspond to Euclidean distances in ILR coordinates. → Volume I §C.

**Balance.** A single ILR coordinate, interpreted as the log-ratio between two carrier subgroups. Each balance is a single number representing one degree of freedom of the composition, chosen by an SBP. (Egozcue–Pawlowsky-Glahn vocabulary.) → Volume I §F.

**Closure.** The operation that rescales a positive vector to sum to a fixed constant (typically 1). Closure makes any positive vector into a composition on the simplex. → Volume I §B.

**CLR (Centered Log-Ratio).** Maps a composition x → log(x) − mean(log(x)). Image lies in the (D−1)-dimensional hyperplane Σ = 0 inside ℝ^D. The "ambient" or "extrinsic" representation: same dimensionality as the original carrier set, with a sum-to-zero constraint. **Teaching alias: "close to simplex"** — CLR keeps you in the simplex's neighbourhood, just log-transformed and centered. → Volume I §C.

**Composition.** A vector of strictly positive numbers (carrier abundances) treated as a point on the simplex, where only relative magnitudes matter (the absolute scale is removed by closure). → Volume I §B.

**Helmert basis / Helmert ILR.** A specific canonical orthonormal basis on the (D−1)-dim CLR hyperplane, built from Helmert contrast vectors. The default ILR basis when no domain-specific SBP is preferred. The CNT engine's Stage 1 uses the Helmert ILR. → Volume I §F.

**ILR (Isometric Log-Ratio).** The canonical orthogonal projection of a composition into ℝ^(D−1), preserving the Aitchison metric isometrically. Egozcue, Pawlowsky-Glahn, Mateu-Figueras & Barceló-Vidal (2003). The "intrinsic" or "isometric" representation: proper Cartesian coordinates of the simplex at its true dimension. **Teaching alias: "image simplex"** — ILR is the simplex's isometric image in normal Euclidean space. → Volume I §F.

**ILR-Helmert orthogonal triplet.** CNT's specific D=4 Stage 1 representation: ILR with a Helmert basis projected to ℝ³, producing the per-timestep orthogonal triplet plate. → Volume I §F, Volume II §D.

**🆕 ILR-quaternion (Volume IV addition).** The same ILR-Helmert projection re-expressed as a unit quaternion (axis+angle), valid specifically at D=4 where SO(D−1) = SO(3) is exactly covered by SU(2). Two names for the same mathematical object: ILR-Helmert names it in compositional vocabulary; ILR-quaternion names it in algebraic vocabulary. → Volume IV §C.

**SBP (Sequential Binary Partition).** A way to specify which orthonormal basis to use for an ILR, by recursively partitioning the carrier set into two groups. Each SBP defines a balance dendrogram and corresponding ILR coordinates. → Volume I §F.

**Simplex S^D.** The set of compositions with D positive components summing to 1. The natural sample space of compositional data analysis. → Volume I §B.

---

## §B — CNT core terms

**Amplitude A.** A scalar diagnostic of the period-2 attractor's strength (magnitude of curvature attractor). Reported per CNT JSON in `depth.higgins_extensions.impulse_response.amplitude_A`. → Volume I §H.

**atan2 simplification.** CNT's per-timestep bearing computation, `θ = atan2(y, x)`, replacing the alternative `arccos(x · y)`. 3× fewer operations, 10⁷ better numerical stability, AND structurally equivalent to the rank-1 case of the quaternion log map (Volume IV §C). → Volume I §F, Volume IV §C.

**Bearing (θ).** Channel 1. The angular orientation of a CLR-projected pair, computed via atan2. The first of CNT's four channels. In Volume IV terms, this is the angle component of the quaternion log. → Volume I §F, Volume IV §C.

**CBS cube.** The 3D structure used in Stage 2 with three orthogonal faces representing the (ω, κ), (κ, σ), (ω, σ) planes of the trajectory state space. The Higgins time axis runs orthogonal to all three. In Volume IV terms, the three faces correspond to the three quaternion-imaginary basis pairs (ij, jk, ki). → Volume II §D, Volume IV §A.

**Channel.** One of CNT's four named per-timestep outputs: θ (bearing), ω (angular velocity), κ (curvature/steering), σ (helmsman). The four channels together describe the trajectory's instantaneous state. In Volume IV: the four channels are the four quaternion components in disguise. → Volume I §F, Volume IV §C.

**Curvature (κ).** Channel 3. Δω/Δt — the rate of change of angular velocity. Captures trajectory turning. → Volume I §G.

**Damping ζ (zeta).** A scalar diagnostic of how quickly the trajectory settles toward its attractor. Sets the IR class via threshold rules. → Volume I §H.

**Depth tower.** CNT's recursive depth-sounder operation. Two parallel towers, `curvature_tower` and `energy_tower`, are built by recursive contraction until termination. Reported as `summary.curvature_depth` and `summary.energy_depth`. → Volume I §G.

**Helmsman (σ).** Channel 4. The signed accumulated angular change — tracks left-handed vs right-handed rotation. In Volume IV: the spinor parity tracker, identifying which SU(2) sheet the trajectory lifts to. → Volume I §G, Volume IV §B.2.

**Higgins time axis.** The trajectory's temporal direction, projected through the CBS cube. In Volume IV terms, the scalar (real) axis of the underlying quaternion. → Volume II §D, Volume IV §A.

**IR class (8-class taxonomy).** Per-trajectory classification into one of: CRITICALLY_DAMPED, OVERDAMPED_EXTREME, LIGHTLY_DAMPED, MODERATELY_DAMPED, DEGENERATE, D2_DEGENERATE, ENERGY_STABLE_FIXED_POINT, CURVATURE_VERTEX_FLAT. Set by threshold rules on amplitude A and damping ζ. The "IR" stands for impulse-response classification. → Volume I §H.

**LIMIT_CYCLE_P2.** Curvature termination code: trajectory returns to itself after exactly 2 recursion steps (period-2 attractor). Observed across virtually every substantively-flowing compositional dataset in the corpus AND on Planck CMB AND on SM neutrino oscillation. **Volume IV interpretation: the universal experimental signature of compositional dynamics carrying all three quaternion invariances at the population level** (simplex rotation, mass-flow handedness, time-reversal symmetry). Not a fermion-vs-boson distinguisher (that conjecture was tested and falsified in QD Round 2.5; reformulated here is the cleaner truth). → Volume I §H, Volume IV §B.

**M² = I.** The metric tensor's involution property — the Banach contraction certificate. Apply M twice, get identity back. Reported per JSON as `M_squared_I_residual`, typically at IEEE floor (~10⁻¹⁷). In Volume IV: equals quaternion conjugation q → q*, which physically is time-reversal symmetry. → Volume I §D, Volume IV §B.3.

**Period-2 attractor.** A trajectory that returns to itself after 2 recursion steps but not after 1. The structural signature of LIMIT_CYCLE_P2 termination. → Volume I §H.

**Angular velocity (ω).** Channel 2. The bearing's rate of change Δθ/Δt. → Volume I §G.

---

## §C — Volume IV (Quaternion View) terms

**Bi-quaternion.** The natural algebra for D=8 compositional dynamics, factoring as SU(2) × SU(2) under the SO(8) ⊃ SU(2) × SU(2) decomposition. Each EMBER country trajectory (D=8) potentially decomposes into two coupled quaternion paths under this factoring. → Volume IV §C, Hs-CNQ engine proposal §H.

**Central claim.** *CNT measures invariance. CNQ names the algebra that invariance lives in.* → Volume IV §A.

**Clifford algebra Cl(D−1).** The dimensional generalisation of quaternions to arbitrary D. For D=4, Cl(3) is the quaternions; for D=8, the natural factoring is bi-quaternions; for arbitrary D, Cl(D−1) is the algebra in which the three Volume-IV invariances are unified. → Volume IV §A.

**CNQ (Compositional Navigation Quaternion).** The proposed quaternion-native engine sibling to `cnt.py`. Computes the same JSON as CNT but via Hamilton products instead of channel arithmetic, exposing operations (SLERP, bi-quaternion factoring, spinor parity) that the channel form leaves implicit. Status: proposed, not yet implemented; ~14 days of focused work per the engineering proposal. → Hs-CNQ engine proposal (in QD experimental folder).

**Conjugation q\*.** Quaternion involution mapping (a, b, c, d) → (a, −b, −c, −d). Negates the imaginary part. Up to sign convention, the unique antiautomorphism of the quaternion algebra fixing the scalar part. Physically: time reversal. CNT's M² = I is structurally q → q*. → Volume IV §B.3.

**Hamilton product.** Quaternion multiplication: non-commutative, closed under unit quaternions. Expresses cross-dataset comparison as `R(t) = Q₁(t) · Q₂(t)⁻¹`. Replaces CNT's channel-by-channel Stage 4 logic with a single algebraic operation. → Volume IV §C.

**IEEE floor.** ≈ 2 × machine epsilon ≈ 4.441 × 10⁻¹⁶ for double-precision IEEE 754 floats. The smallest difference numerically representable on standard hardware. Volume IV's three confirmations (backblaze_fleet, Planck CMB, SM neutrino) all hit this floor exactly, demonstrating the quaternion identification is mathematically exact rather than approximate. → Volume IV §B, §D.

**Quaternion (unit).** Element of the 3-sphere S³, written q = a + b·i + c·j + d·k with a² + b² + c² + d² = 1. The four-component algebra discovered by Hamilton (1843). For D=4 compositions, the algebra in which all three CNT invariances are unified. → Volume IV §A.

**Quaternion log map.** Maps a unit quaternion to its axis-angle representation: log(q) = (atan2(|v|, a)/|v|) · v, where v = (b, c, d). The rank-1 case is exactly CNT's atan2 bearing step. → Volume IV §C.

**Sandwich product.** The operation q · v · q* applied to a 3-vector v, where q is a unit quaternion. Rotates v by the rotation that q represents in SO(3). For D=4 compositions, this is the same operation as Aitchison rotation between consecutive Helmert-projected unit vectors (verified at IEEE floor in QD Round 2). → Volume IV §B.1, §C.

**SLERP (Spherical Linear Interpolation).** Geodesic interpolation between two unit quaternions on S³. Replaces linear interpolation in CLR space with the geodesic that respects the underlying simplex geometry exactly. → Volume IV §C.

**Spinor branch / vector branch.** The two sheets of the SU(2) → SO(3) double cover. A trajectory's lift to SU(2) is in either the spinor branch (signed −1 in SU(2), needs 720° rotation to return to identity) or the vector branch (signed +1, needs 360°). Stage 2 calibration directness=1.0 tests the spinor branch (cumulative angle = π); directness=0.0 tests the vector branch (cumulative angle = 2π). → Volume IV §B.2.

**SU(2) cover of SO(3).** The double cover of the rotation group SO(3) by the unit quaternions SU(2) ≃ S³. Every SO(3) rotation has two preimages in SU(2): q and −q. This doubling is the spinor structure. For D=4 Aitchison rotations, SO(3) is the rotation group AND SU(2) is its universal cover, so unit quaternions are exact coordinates. → Volume IV §B.1.

---

## §D — Tier system and access protocols

**CCTT (CNT Compositional Tensor Train).** The 7-phase user/AI access protocol. Lets any researcher (by hand) or AI assistant (Claude, ChatGPT, Gemini, in-house) take a raw compositional CSV and produce a CNT-grade analysis end-to-end with hash-chained provenance. → `ai-refresh/CCTT_RUNBOOK.md`.

**CNQ tier.** The proposed high-performance compositional analytics tier above CNT. Quaternion-native operations sized for dimensionally larger systems (climate modeling, multi-decade economics, microbiome cohorts). Builds on Volume IV. → Hs-CNQ engine proposal (in QD experimental folder).

**CNT tier.** The current canonical engine: trajectory-navigation tensor for medium-scale compositional analysis. Engine 2.0.4, schema 2.1.0, 25-experiment determinism gate. → Volumes I-III.

**CoDa tier.** The compositional-data-analysis foundation: Aitchison closure, log-ratios, balance, ternary, biplot. Two centuries of mathematical machinery. → Volume I §B-§F.

**OPERATIONS_PROTOCOL.** The Gawande-style meta-checklist for the whole repo. 13 transition sections (as of 2026-05-07; Section 13 is the Volume IV verification path). → `OPERATIONS_PROTOCOL.md` at repo root.

---

## §E — Standard symbols (most commonly used)

| Symbol | Meaning |
|---|---|
| **D** | number of carriers (composition dimension) |
| **T** | number of records (timesteps) |
| **N** | number of trajectories in a bundle |
| **θ, ω, κ, σ** | the four CNT channels (bearing, angular velocity, curvature, helmsman) |
| **A, ζ** | period-2 attractor amplitude and damping |
| **q** | unit quaternion |
| **q\*** | quaternion conjugate |
| **v** | 3-vector (typically a Helmert-projected CLR triple) |
| **Q(t)** | trajectory as a quaternion-valued function of time |
| **R(t)** | relative quaternion between two trajectories: Q₁(t) · Q₂(t)⁻¹ |
| **M** | metric tensor (M² = I) |
| **H** | Helmert orthogonal contrast matrix |
| **S^D** | the (D−1)-simplex |
| **S³** | the 3-sphere = unit quaternions = SU(2) |

---

## §F — Standard formulas (Volume IV-touched)

```
Closure:                  C(x) = x / Σ x_i
CLR:                      clr(x) = log(x) - mean(log(x))
ILR (Helmert):            ilr(x) = H @ clr(x)        where H is (D-1) × D Helmert basis
Aitchison distance:       d_A(x, y) = || ilr(x) - ilr(y) ||  (Euclidean in ILR coords)

CNT bearing (atan2):      θ = atan2(y, x)
Quaternion log:           log(q) = (atan2(|v|, a) / |v|) · v        with v = (b, c, d)
Quaternion sandwich:      v' = q · v · q*                            v as pure quaternion (0, b, c, d)
Hamilton product:         (p · q)_components per Hamilton 1843 multiplication table
Quaternion conjugation:   q* = (a, -b, -c, -d)
Metric involution:        M² = I    ↔    (q*)* = q
SLERP:                    slerp(Q_t, Q_{t+1}, α) = sin((1-α)Ω)/sinΩ · Q_t + sin(αΩ)/sinΩ · Q_{t+1}
                                                where cosΩ = Q_t · Q_{t+1}
```

---

## §G — Pointers to Volume IV-only content

The central claim, the three IEEE-floor confirmations, the operation map (CNT step → quaternion-native equivalent), and the Hs-CNQ engineering proposal are all in [Volume IV — The Quaternion View](VOLUME_4_QUATERNION_VIEW.md). This glossary defines the vocabulary; Volume IV gives the math chains, the evidence summary, and the integration plan.

---

## Out of scope for this minimal-now refresh

The following CNT vocabulary is canonically used but is NOT covered by this minimal refresh, because it predates Volume IV and is documented adequately in Volumes I–III. They will be folded into the next-cycle full glossary refresh after CodaWork:

- Engine schema fields beyond Volume IV's needs (`source_file_sha256`, `closed_data_sha256`, `engine_signature`, `INPUT_UNITS`, `engine_config_overrides`, the 7 top-level JSON keys)
- Atlas module names (Stage 1/2/3/4 modules, spectrum_paper, projector_html) — already glossed in Volume II
- Termination codes beyond LIMIT_CYCLE_P2 (HS_FLAT, OMEGA_FLAT, SIGNAL_SHORT, ENERGY_STABLE, etc.) — already glossed in Volume I §H
- Adapter, Mission Command, and CCTT phase-by-phase terminology — already in Volume II §C-§E and CCTT_RUNBOOK
- Output Doctrine v1.0.1 specifics — already in Volume I §G
- Audit-chain terms (corpus, INDEX, JOURNAL, PUSH-N audit reports) — already in Volume III

Full-refresh target: ~6-8k words covering all of the above plus this minimal-now content. Estimated 4–5 hours of focused work, scheduled as a separate push cycle after CodaWork 2026.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
*CNT measures invariance. CNQ names the algebra it lives in.*
