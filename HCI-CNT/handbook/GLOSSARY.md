# Glossary — Minimal-Now Refresh (Volume IV-touched + HCI vocabulary + Helmsman family extensions)

**Scope:** terms touched by the Volume IV (Quaternion View) integration of 2026-05-07, plus the HCI instrument-family vocabulary promoted from `HCI/HCI_FOUNDATION.md` and `HCI/README.md` during the 2026-05-07 ChatGPT cross-check pass (push #23), plus six **proposed Helmsman-family extensions** surfaced during the 2026-05-08 Grok cross-check pass (push #24, §I). Approximately 53 entries.
**Companions:** [Volume I — Theory and Mathematics](VOLUME_1_THEORY_AND_MATHEMATICS.md), [Volume II — Practitioner and Operations](VOLUME_2_PRACTITIONER_AND_OPERATIONS.md), [Volume III — Verification, Reference and Release](VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md), [Volume IV — The Quaternion View](VOLUME_4_QUATERNION_VIEW.md), and [HCI/HCI_FOUNDATION.md](../../HCI/HCI_FOUNDATION.md).
**Full refresh planned for a separate cycle.** This document covers (i) terms used in the central-claim chain so the four volumes are internally cross-referenceable today, and (ii) the most-used HCI instrument-family vocabulary so the handbook and HCI specs share one authoritative naming layer. The broader CNT vocabulary (atlas modules, schema fields, audit-chain terms) will be added in a dedicated glossary push after CodaWork.

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

**Bi-quaternion.** The natural algebra for D=8 compositional dynamics, factoring as SU(2) × SU(2) under the SO(8) ⊃ SU(2) × SU(2) decomposition. Each EMBER country trajectory (D=8) potentially decomposes into two coupled quaternion paths under this factoring. → Volume IV §C; [`../../HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md`](../../HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md) §H.

**Central claim.** *CNT measures invariance. CNQ names the algebra that invariance lives in.* → Volume IV §A.

**Clifford algebra Cl(D−1).** The dimensional generalisation of quaternions to arbitrary D. For D=4, Cl(3) is the quaternions; for D=8, the natural factoring is bi-quaternions; for arbitrary D, Cl(D−1) is the algebra in which the three Volume-IV invariances are unified. → Volume IV §A.

**CNQ (Compositional Navigation Quaternion).** The quaternion-native sibling tier to CNT in the Hs system. Doctrine, three IEEE-floor demonstrations, three-tier comparison, ROI/use-case guidance, and the engineering proposal for a compiled `cnq.py` engine all live canonically at [`../../HCI-CNQ/`](../../HCI-CNQ/). The tier is live since push #23 (2026-05-07); the compiled `cnq.py` engine is pending (~14 days per the engineering proposal). When implemented, `cnq.py` produces the same JSON as CNT but via Hamilton products instead of channel arithmetic, exposing operations (SLERP, bi-quaternion factoring, spinor parity) that the channel form leaves implicit. → [`../../HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md`](../../HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md).

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

**CNQ tier.** The high-performance compositional analytics tier above CNT in the Hs three-tier stack (CoDa → CNT → CNQ). Quaternion-native operations sized for dimensionally larger systems (climate modeling, multi-decade economics, microbiome cohorts). Built on Volume IV. **Tier is live and canonical since push #23 (2026-05-07)**: doctrine, three IEEE-floor demonstrations, comparisons, and the compiled-engine proposal all sit in [`../../HCI-CNQ/`](../../HCI-CNQ/). The compiled `cnq.py` engine itself is the next milestone (~14 days). → [`../../HCI-CNQ/README.md`](../../HCI-CNQ/README.md).

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

## §H — HCI instrument-family vocabulary (cross-check refresh, push #23)

The HCI (Higgins Compositional Instrument) family has its own working
vocabulary defined in `HCI/HCI_FOUNDATION.md` and `HCI/README.md`. The
following entries promote the most-used HCI terms into the canonical
glossary so the handbook volumes and the HCI-side specifications share
one authoritative naming layer. Sourced from the HCI files plus the
2026-05-07 ChatGPT cross-check pass.

**HLR (Higgins Log-Ratio Level).** The dimensionless natural-log unit in
which all HCI plate coordinates are reported. Defined as
`h_j(t) = ln(x_j(t)) − mean_k ln(x_k(t)) = ln(x_j(t) / g(x(t)))`. Nearest
relative in the log-level family: the neper. → `HCI/README.md` Unit
Standard, `HCI/HCI_USER_GUIDE.md`.

**κᴴˢ (Higgins Steering Metric Tensor).** The full D×D Aitchison pullback
metric on the simplex, written `κᴴˢ_ij(x) = (δ_ij − 1/D) / (x_i · x_j)`.
In matrix form, `κᴴˢ(x) = diag(1/x) · P · diag(1/x)` with `P = I − (1/D)·11ᵀ`.
The diagonal `κᴴˢ_jj(x) = (1 − 1/D) / x_j²` governs single-carrier
sensitivity; the off-diagonal `κᴴˢ_ij(x) = −1 / (D · x_i · x_j)` governs
inter-carrier metric coupling. The scalar `s_j(x) = 1/x_j` is the **diagonal
steering sensitivity** — one diagnostic readout from κᴴˢ, **not** the full
tensor. CNT channel κ (curvature) reports the trajectory's response to this
metric; this glossary entry names the metric itself. → `HCI/HCI_FOUNDATION.md`
Definition 3.

**DCDI (Dominant Carrier Displacement Index).** Formal operator name for
the carrier with the largest absolute CLR displacement between consecutive
compositions: `σᴴˢ(t, t+1) = argmax_j |h_j(t+1) − h_j(t)|`. The instrument
alias is the **Helmsman Index** — the carrier "steering" the local
displacement at each step. CNT channel σ reports DCDI per timestep.
→ `HCI/HCI_FOUNDATION.md` Definition 4.

**Multiplexed Carrier Section Plate.** The Stage 1 plate convention in
which all carriers' sections are rendered under shared geometry on one
multi-panel page (XY plan view + XZ bearings + YZ CLR bars + info + legend).
One section plate is produced per time index; the time-indexed sequence
forms the Section Atlas. → `HCI/HCI_FOUNDATION.md` Stage 1, `HCI/README.md`
Stage 1 — Section Plate Generator.

**System Course Plot.** The summary terminal page of a Stage 1 plate
cine-deck — the trajectory's whole-run course rendered in one frame after
the per-timestep section plates. Provides at-a-glance trajectory shape;
the per-timestep plates provide the per-step authority. → `HCI/README.md`
Stage 1, `HCI/codawork2026/stage1_plates/`.

**HCI Barycentric Navigation Volume.** The 3D enclosing manifold inside
which a CNT trajectory navigates relative to the simplex barycentre — the
spatial scope a Spatial Morphographic Analyzer (HCI-VR) renders. Relates
to the CBS cube (Volume II §D, Volume IV §A) as the volume whose three
orthogonal faces the cube parameterises. Status: defined in HCI vocabulary;
no rendering instrument yet implemented in the canonical engine.

**HCI Spatial Morphographic Analyzer (HCI-VR, exploratory).** Proposed VR
or 3D-renderer instrument for walking through the Barycentric Navigation
Volume — manipulable section plates in 3D, CBS cube faces seen from inside.
Status: design exploration only. Lives in the experimental folder
(`Quaternion Decomposition/Hs-VR/` at workspace root, not in the canonical
repo) until a working pilot exists. Listed here so the vocabulary is
canonical when the instrument arrives.

---

## §I — Helmsman family extensions (proposed, Grok crosscheck)

Status: **proposed extensions**, not yet implemented in `cnt.py` 2.0.4. Surfaced during the 2026-05-08 Grok cross-check pass (push #24). These extend the existing CNT helmsman σ channel (defined in §B) with a coherent diagnostic vocabulary for trajectory steering. They will graduate from "proposed" to canonical only when the engine implements them and produces them in the JSON schema.

**Sign of the Helmsman (σ̂).** The dominant carrier exerting the largest weighted directional influence on the compositional state at a given step, with sign attached: σ̂(t) = sign(Δx_{i*}) where i* = argmax_i (|Δx_i(t)| · w_i(t)). The weight w_i is typically the local intensity x_i(t), but in the quark-sector extension proposed by Grok it incorporates mass-hierarchy dependence on energy scale Q². The sign component carries handedness (CP-like in the quark sector, polarisation handedness in EM, room-mode parity in acoustics). → Volume IV §B.2 for the CNT-side relationship to spinor parity. **Proposed, not implemented.**

**Helmsman Stability (S_σ).** Scalar diagnostic in [0, 1] measuring how persistently the same helmsman dominates over a window. Defined as S_σ = 1 − (number_of_flips) / (N − 1) for a trajectory of length N. Practical interpretation: S_σ near 1 means the trajectory is dominated by one carrier throughout (high modal lock); S_σ near 0 means the helmsman changes at almost every step (rapid trading of dominance, often a sign of chaos or strong oscillation). **Proposed, not implemented.**

**Helmsman Flips.** Count of indices t where σ̂(t) ≠ σ̂(t−1). Equivalently, the number of times the dominant-carrier identity changes along the trajectory. Sustained periodic flipping between two carriers is the universal signature of a sustained `LIMIT_CYCLE_P2` regime (the period-2 attractor); flip statistics that show the period-doubling cascade (P2 → P4 → P8 → … → chaos) are the dynamical-systems route to Helmsman Chaos described below. **Proposed, not implemented.**

**Helmsman Chaos.** The regime in which the Helmsman sequence becomes aperiodic and sensitive to initial conditions. Reached via the period-doubling cascade governed (universally, for one-dimensional unimodal maps) by Feigenbaum's δ ≈ 4.6692 and α ≈ −2.5029. Diagnostic signatures: positive Lyapunov exponent of the σ̂(t) sequence, fractal structure with Hausdorff dimension ≈ 0.538, and breakdown of the standard IR taxonomy (the trajectory no longer fits cleanly into a damping class). Predicted to appear in driven nonlinear acoustic, EM, or quark-sector trajectories at sufficiently strong control parameter. **Proposed, not implemented.**

**Helmsman Torque.** Rate of change of the helmsman's effective steering direction. Lightly developed — Grok proposed it as a diagnostic correlated with rapid CKM running or new physics in the quark sector, and as a potential observable in EM polarisation rotation rates. No formal definition committed. **Proposed, weakly developed.**

**Joint Helmsman.** When two or more subsystems (channels, drivers, polarisation states, phonon modes, droplets, …) share a common physical field (joint quaternion field q_joint), the helmsman extracted from log(q_joint) is the **joint helmsman** — non-separable across subsystems. The joint statistics of helmsman signs across multiple measurement settings can produce CHSH-like correlations bounded by the Tsirelson value 2√2; values around S ≈ 2.49 are typical in high-memory hydrodynamic analogs and are predicted in strongly coupled multi-channel acoustic or EM systems. → [`../../HCI-CNQ/doctrine/`](../../HCI-CNQ/doctrine/) for the CNQ-side many-body machinery. **Proposed, not implemented in cnt.py; some hand computation is possible from existing JSON outputs.**

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
