# Glossary — Full Refresh v2.0

**Version:** v2.0 (2026-05-14). Initial release v1.0 push #27 (2026-05-08).
**Canonical reference for locked vocabulary:** [`NOTATION_AND_TERMINOLOGY.md`](NOTATION_AND_TERMINOLOGY.md) v2.0 (2026-05-14). For any term that appears in both files, NOTATION_AND_TERMINOLOGY.md is authoritative; this glossary is the readable narrative companion.

**Scope (v2.0):** the previously-glossed Volume IV / HCI / Helmsman vocabulary (~53 entries), PLUS comprehensive coverage of vocabulary added across pushes #28-#50: HUF Standards (HUF-STD-001/002/003), the seven linear-algebra foundations, Stage 0 / Foundations Plate, ILR-Helmert Triplet Plate, Dual-View Stage 1 Output, Power Share / Activation Coefficient, MC-4 three-conjunct, INV-050 metric pair-invariance, INV-051 deceptive drift, EITT, CRD-1.0, HUF AI Collective, AI Use Declaration, Standard Stamp, person-noun convention, document versioning, Hs Change Control (DCP, HCC, CHK rules), PRE_CONFERENCE_LOCKDOWN, Tensor Train v1.0, Output Doctrine v1.0 Order classification, and the canonical findings catalog. Approximately 100+ entries.

**Companions:** [`NOTATION_AND_TERMINOLOGY.md`](NOTATION_AND_TERMINOLOGY.md) v2.0, [Volume I — Theory and Mathematics](VOLUME_1_THEORY_AND_MATHEMATICS.md), [Volume II — Practitioner and Operations](VOLUME_2_PRACTITIONER_AND_OPERATIONS.md), [Volume III — Verification, Reference and Release](VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md), [Volume IV — The Quaternion View](VOLUME_4_QUATERNION_VIEW.md), [HCI/HCI_FOUNDATION.md](../../HCI/HCI_FOUNDATION.md), and the three HUF Standards JSONs at [`huf-gov/standards/`](../../huf-gov/standards/).

**Terminology unification (push #27, retained).** Tensor index count is named **order** (not rank). κᴴˢ_ij is an **order-2** tensor; the diagonal sensitivity 1/x_j is the **order-1 carrier steering sensitivity vector** s_j (a distinct object). The "bi-quaternion factoring" of INV-029 is now formally called **twin-quaternion factoring** (SU(2) × SU(2)) to avoid confusion with the strict mathematical bi-quaternion (ℍ ⊗ ℂ). See [`NOTATION_AND_TERMINOLOGY.md`](NOTATION_AND_TERMINOLOGY.md) §1, §2, §7.

**v2.0 additions (this refresh).** Helmsman Stability, Helmsman Flips, Helmsman Sigma Sequence, and Helmsman Torque Proxy are promoted PROPOSED → CANONICAL per CNT schema 3.1.0 (push #37). Stage 0 added to plate tier. "Yeast factor" formally renamed to **Activation Coefficient** (legacy term retained in prose for intuition; formal name used in tables and outputs). Person-noun convention codified at standards level (HUF-STD-001 v1.1).

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

**atan2 simplification.** CNT's per-timestep bearing computation, `θ = atan2(y, x)`, replacing the alternative `arccos(x · y)`. 3× fewer operations, 10⁷ better numerical stability, AND structurally equivalent to the 1D / single-axis case of the quaternion log map (Volume IV §C). → Volume I §F, Volume IV §C.

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

**Quaternion log map.** Maps a unit quaternion to its axis-angle representation: log(q) = (atan2(|v|, a)/|v|) · v, where v = (b, c, d). The 1D / single-axis case is exactly CNT's atan2 bearing step. → Volume IV §C. (Vocabulary note: previously called the "rank-1 case"; "rank" is now reserved for matrix / decomposition contexts per [`NOTATION_AND_TERMINOLOGY.md`](NOTATION_AND_TERMINOLOGY.md) §1.)

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

---

## §J — HUF Standards (added v2.0)

**HUF-STD-001 (Publication Standards).** Adopts ICMJE / COPE / Nature/Springer / Science/AAAS / WAME / EU AI Act 2024 / arXiv / ACM / IEEE as primary references. Establishes the AI Use Declaration template (mandatory section at the end of every externally-published document), authorship rules (human-only — AI tools are NOT authors), the person-noun convention (HUF-STD-001 v1.1, 2026-05-14), provenance/hash-chain expectations, versioning conventions, locale support, lockdown discipline, and licensing. File: [`huf-gov/standards/HUF_PUBLICATION_STANDARDS.json`](../../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json) v1.1.

**HUF-STD-002 (Tensor Train I/O Standard).** Codifies the data → CNT → CNQ → vector-output pipeline as the named **Tensor Train v1.0**. Four links: adapter (Order 0) → CNT (Orders 1-3 metric tensor) → CNQ (D=2/3/4 quaternion view) → vector diagrammatic output (PDF / PNG / SVG). **PPTX is explicitly excluded** from the standard tensor-train package — it's a conference-delivery format, not engine output. File: [`huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json`](../../huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) v1.0; narrative at [`TENSOR_TRAIN.md`](../../huf-gov/standards/TENSOR_TRAIN.md). Post-conference targets list (Order 1: Power Share / Activation Coefficient diagnostic; Order 2: CNQ Vector PDF exporter per INV-062; Orders 3-5: alternate-format exports + Stage-3 + Stage-4 plates).

**HUF-STD-003 (Hs Linear Algebra Foundations).** Names the seven classical linear-algebra components that every Hs engine and plate generator employs. Establishes Stage 0 (Foundations Plate) as the dedicated visualization tier for the foundations themselves. File: [`huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json`](../../huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json) v1.0; narrative at [`FOUNDATIONS.md`](../../huf-gov/standards/FOUNDATIONS.md); per-foundation file/plate/schema audit at [`FOUNDATIONS_TRACEABILITY.md`](../../huf-gov/standards/FOUNDATIONS_TRACEABILITY.md). Established push #50.

---

## §K — The Seven Linear-Algebra Foundations (HUF-STD-003)

The framework rests on seven classical components. Each is locked-named in NOTATION §14; the narrative reading for each is below.

**Symmetric Matrix (Foundation §1).** M = Mᵀ. The canonical objects of multivariate statistics — covariance, variation, Gram matrices are all symmetric by construction. In Hs: the **variation matrix** var(log x_i/x_j) is symmetric; the **CLR covariance** Cov(clr(X)) is symmetric and positive-semidefinite; the **Helmert Gram matrix** H·Hᵀ = I is the orthonormality certificate. The bearing tensor θ_ij is the antisymmetric (skew-symmetric) sibling: θ_ji = −θ_ij.

**Property of Transpose (Foundation §2).** For orthonormal Q, Qᵀ = Q⁻¹. The property that makes ILR-Helmert coordinate changes exact and lossless. In Hs: `ilr = clr @ Hᵀ` and `clr = ilr @ H` — both directions exact because H·Hᵀ = I. The covariance propagation rule Cov(M·X) = M · Cov(X) · Mᵀ is the engine of change-of-basis statistics.

**Matrix Decomposition (Foundation §3).** Factor a matrix into structurally-simpler pieces. In Hs: the **closure → CLR → ILR** chain decomposes a raw composition into a vector in Euclidean space; the **bearing tensor** decomposes a trajectory step into D(D−1)/2 pairwise angular channels; the **depth tower** (Stage 3) is a recursive orthogonal subspace decomposition; **CoDa-PCA** (Stage 2) is the spectral decomposition of CLR covariance.

**Eigenvectors and Eigenvalues (Foundation §4).** M·v = λ·v. Eigenvectors are the privileged directions of M; eigenvalues are how strongly M acts there. In Hs: the **attractor fit** in `cnq.py` is an eigendecomposition of the local linearization; the **κ^HS sensitivity vector** is an eigenvector-style direction on the simplex; the **CoDa-PCA biplot** plots the top eigenvectors of the CLR covariance.

**Strong Property of Symmetric Matrices / Spectral Theorem (Foundation §5).** Real symmetric Σ has real eigenvalues and an orthonormal eigenbasis: Σ = Q·Λ·Qᵀ. The strongest single result in elementary linear algebra and the **silent justification** for almost everything in Hs: ILR forms an orthonormal basis because of this theorem; CoDa-PCA produces real principal components because of this theorem; the attractor fit's eigenvalues are real because of this theorem. The Stage-0 Foundations Plate verifies the theorem numerically at IEEE-floor on actual data (typical residual ~1e-13).

**Spectral Decomposition (Foundation §6).** The explicit factorization Σ = Q·Λ·Qᵀ. Rank-k truncation gives the optimal rank-k approximation (Eckart–Young theorem). In Hs: Stage-2 CoDa-PCA biplot performs this partially (top 2 axes); Stage-0 Foundations Plate visualizes the full Q heatmap + rank-k cumulative variance.

**Visualization (Foundation §7).** The plate suite is the visible surface of all six foundations above. Stage 0 visualizes the foundations directly; Stages 1-4 visualize their consequences. Standard output formats are PDF / PNG / SVG per HUF-STD-002.

---

## §L — Stage 0 / Foundations Plate (added v2.0)

**Stage 0 (Foundations Plate).** The visualization tier reserved for the seven HUF-STD-003 foundations. One plate per dataset (read **once per dataset** — foundations characterize the data's geometry, they don't change frame-to-frame). Two pages per country: page 1 is a six-panel grid (variation matrix heatmap, Helmert basis + orthonormality check, decomposition tree, eigenvalue scree, orthonormal eigenbasis Q heatmap, Spectral Theorem residual); page 2 is a 16-row numeric verification table reporting `max|M − Mᵀ|`, `max|H·Hᵀ − I|`, `max|Σ − Q·Λ·Qᵀ|`, rank-k cumulative variance, and other foundations residuals at IEEE-floor. Generator: [`HCI/codawork2026/stage0_foundations/foundations_plate.py`](../../HCI/codawork2026/stage0_foundations/foundations_plate.py). Reference output: master PDF [`CodaWork2026_FoundationsPlates_2026-05-14.pdf`](../../CODA-Association/CODAwork2026/data_outputs/CodaWork2026_FoundationsPlates_2026-05-14.pdf) (19 pages, 9 EMBER countries × 2-page plate). Established push #50.

**Stage 1 dual view.** Two complementary readings of the same Stage-1 step:
- **Section Plate** (CoDa-Standard): XY plan view + XZ pairwise bearings (bars) + YZ CLR per carrier (bars) + info + legend. Answers *"what are the magnitudes at this timestep?"* Generator: [`HCI/codawork2026/stage1_plates/stage1_plates_raw.py`](../../HCI/codawork2026/stage1_plates/stage1_plates_raw.py).
- **ILR-Helmert Triplet Plate** (Orthonormal): three orthogonal scatter projections (ilr_1×ilr_2, ilr_1×ilr_3, ilr_2×ilr_3) of the full trajectory in ILR space. Answers *"where is the composition in ILR space and where has it moved?"* Generator: [`HCI/codawork2026/stage1_plates/ilr_triplet_plate.py`](../../HCI/codawork2026/stage1_plates/ilr_triplet_plate.py). Established push #50.

Together they form the **Dual-View Stage 1 Output** — the complete Stage-1 reading. The Section Plate gives the timestep-by-timestep magnitude index; the Triplet Plate gives the trajectory shape across the full time window. Reference output: master PDF [`CodaWork2026_DualViewStage1Output_2026-05-13.pdf`](../../CODA-Association/CODAwork2026/data_outputs/dual_view/CodaWork2026_DualViewStage1Output_2026-05-13.pdf) (503 pages).

---

## §M — Power Share / Activation Coefficient (added v2.0)

**Power Share.** Per-carrier fraction of squared CLR motion at one transition step:

```
power_share_j(t)  =  (ΔCLR_j(t))²  /  Σ_k (ΔCLR_k(t))²
```

Sums to 100% across carriers per step. Identical to the per-carrier component of squared Aitchison distance: `d²(t-1, t) = Σ_k (ΔCLR_k)²`. Gives a clean answer to "which carrier is doing what fraction of the directional work at this step?"

**Activation Coefficient.** The leverage ratio of directional work to size:

```
activation_coefficient_j(t)  =  power_share_j(t)  /  composition_share_j(t-1)
```

A carrier with AC > 1 is **structurally activating** the system beyond its share — doing more directional work than its size would suggest. AC ≫ 1 (e.g. > 10) names the *yeast factor* cases — small-share carriers doing disproportionate structural work. Activation threshold: AC = 1 is neutral; AC > 1 is activated.

**Yeast Factor.** Legacy / informal name for Activation Coefficient. The biological metaphor (a small percentage that, when active, transforms the loaf) carries the right intuition; the formal name is Activation Coefficient. Both terms appear in narrative prose; outputs and tables use the formal name.

**Reference demonstration.** [`CODA-Association/Studies/Religion_2026-05-14/Religion_HiddenDirections_2026-05-14.pdf`](../../CODA-Association/Studies/Religion_2026-05-14/Religion_HiddenDirections_2026-05-14.pdf) slide 8 — Pew religion data surfaced activation coefficients up to 148× (USA Hindus 2030→2040 step, driving 74% of directional work from 0.5% composition share).

**Engine status.** Computed externally from CLR coordinates already in CNT JSON `tensor.timesteps[t].coda_standard.clr[]`. Native engine block queued as schema bump 3.1.0 → 3.2.0 + new plate generator `power_share_plate.py` (Stage-1 sibling). This is the top-of-queue post-conference target per HUF-STD-002 (Order 1) and INV-060 promotion path. Standard inclusion in every Hs-produced data deliverable going forward per Peter directive 2026-05-14.

---

## §N — Canonical Findings (added v2.0)

**MC-4 three-conjunct claim.** *"No monitoring framework in the energy / market-share literature operates natively in Aitchison geometry with formal change detection at the carrier level — three conjuncts combined into one observable stack."* Sharpened from an earlier 4-conjunct formulation at push #39. The three conjuncts are: (1) Aitchison-native operation, (2) formal change detection, (3) carrier-level attribution. Each is non-novel individually; the conjunction is the unmet structural gap MC-4 names. Reference: [`papers/codawork2026/planning/`](../../papers/codawork2026/planning/) MC-4 packet.

**INV-050 metric pair-invariance.** Total Variation distance and Aitchison distance agree on every shock hit/miss verdict across the 9-country EMBER 2001-2025 corpus. Demonstrated pair-invariance only (TV ↔ Aitchison); broader-family invariance across all simplex distances is INV-050.Q2 (open). The finding preempts the "your verdict depends on which metric you chose" critique for this specific pair.

**INV-051 deceptive drift 5-of-9.** The deceptive-drift signature (Aitchison distance moves while individual carrier percentages stay near-stationary) fires in 5 of 9 EMBER countries at annual grain. Headline case: Germany p ≈ 0.0016. Carriers: AUS, CHN, GBR, IND, JPN. The pattern is the structural justification for compositional vs single-carrier monitoring — the geometry sees what each carrier individually does not.

**EITT — Entropy-Invariant Time Transformer.** The geometric-mean decimation step within the Hs pipeline that preserves Shannon entropy across compression. Empirical result: 0.18% variation in Shannon entropy across 341:1 compression. Documented at [`papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md`](../../papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md). One step inside the broader pipeline; the entropy-invariance under geometric-mean decimation is the canonical claim.

**LIMIT_CYCLE_P2 (Paper 1 universal invariance signature).** Period-2 attractor termination of the CNT depth tower; observed across virtually every substantively-flowing compositional dataset in the corpus AND on Planck CMB AND on SM neutrino oscillation. Three IEEE-floor confirmations at residual ~4.44e-16 (machine epsilon × 2). The "universal compositional invariance signature" reading. See Volume IV §B for the quaternion-algebraic interpretation.

**Three IEEE-floor confirmations.** Backblaze drives (D=4, T=731), Planck CMB photons (D=4, T=2499), SM neutrino oscillation (D=3, T=1000). All three reproduce LIMIT_CYCLE_P2 with `max_residual` bit-identical at 4.44e-16 across systems. Cross-system bit-identity demonstrates the residual is hardware float64 representation, not algorithmic noise.

**INV-059 humble-invitation framing.** Cross-model validation: two independent external models (ChatGPT session 2, Grok round 5) reading the MC-4 packet cold produced convergent recommendations on the conference talk's framing (humble + methods-challenge + invitation). The talk's posture is independently stress-tested across the HUF AI Collective.

---

## §O — Other Locked Doctrines (added v2.0)

**CRD-1.0 (Coherent Range Doctrine).** Every multi-carrier comparison is computed on the intersection of all members' time ranges; the shortest-coverage member sets the binding window; every output declares its coherent-range manifest in its header. Established push #33 (INV-047). Triggered by the USA-EMBER missing-year-2000 asymmetry. [`docs/COHERENT_RANGE_DOCTRINE.md`](../../docs/COHERENT_RANGE_DOCTRINE.md).

**SEA-1.0 (Suspicion of Every Assumption).** Every public function and claim enumerates its failure modes with mitigation evidence; the engine is guilty until proven innocent. Established push #32 (INV-045). [`docs/SUSPICION_OF_EVERY_ASSUMPTION.md`](../../docs/SUSPICION_OF_EVERY_ASSUMPTION.md).

**STP-1.0 (Self-Test Protocol / BIST).** Every engine carries a frozen reference corpus and a runner that produces dated, hash-chained receipts of pass/fail status. Built-In Self-Test discipline. Established push #32 (INV-046). [`docs/SELF_TEST_PROTOCOL.md`](../../docs/SELF_TEST_PROTOCOL.md).

**Engine independence policy.** `cnt_content_sha256` and `cnq_content_sha256` are unrelated by design. Cross-engine hash chains are forbidden. Each engine is deterministic on its own. Established push #32. Documented in [`ai-refresh/CNT_V3_CNQ_V2_DESIGN.md`](../../ai-refresh/CNT_V3_CNQ_V2_DESIGN.md).

**Tensor Train v1.0.** The named data → CNT → CNQ → vector-output chain. Four links with locked I/O contracts at each. PDF / PNG / SVG are standard outputs; PPTX is conference-delivery only. Established at HUF-STD-002, push #50. [`huf-gov/standards/TENSOR_TRAIN.md`](../../huf-gov/standards/TENSOR_TRAIN.md).

**Output Doctrine v1.0.** Order/Stage classification of plate outputs (Order 0 raw → 1 first-principles → 2 inter-timestep → 3 recursive → 4+ inferential, mapped to Stages 1-4). Locked May 5 2026. Extended at push #50 to include Order 0+ / Stage 0 (Foundations Plate). [`HCI-CNT/conference_demo/cnt_demo/05_doctrine/OUTPUT_DOCTRINE.md`](../../HCI-CNT/conference_demo/cnt_demo/05_doctrine/OUTPUT_DOCTRINE.md).

**HUF Governance Charter.** Nine-article governance document for HUF + Hs + derivative repos. Establishes principles (Integrity of Purpose, Accountable Data, Accountable Resolution) and authority structures. Parent doctrine for HUF-STD-001/002/003 and SAFE-001/LOOP-001/KILL-001. [`huf-gov/HUF_GOVERNANCE_CHARTER.md`](../../huf-gov/HUF_GOVERNANCE_CHARTER.md).

**SAFE-001 (Cognitive-agent safety doctrine).** Governs AI-tool use in framework operations. Cross-check protocol, human-in-the-loop discipline, fail-safe defaults.

**LOOP-001 (Open-loop / Skydiver Principle).** The operator holds the last breaker. The framework's circuit-breaker discipline routes through 16 breakers; Breaker 16 is held by the human operator and cannot be overridden by automation.

**KILL-001 (Named-failure-modes catalog).** Nineteen named failure modes with mitigations. The Hs system's HAZOP/FMEA equivalent at framework level.

---

## §P — Output Conventions (added v2.0)

**HUF AI Collective.** Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI) — the five AI participants in Hs cross-check work. Operated under the HUF Governance Charter Articles II-IV + SAFE-001 cross-check protocol. Disclosed in AI Use Declaration sections at the END of every external-audience document; **NOT** in author bylines. Established as convention 2026-05-08+; codified at HUF-STD-001.

**AI Use Declaration.** Mandatory section in every externally-published HUF or Hs document, placed at the end (before signature / repository pointers). Per HUF-STD-001, must include: AI tools used (specific name + vendor), tasks performed by AI, author responsibility statement (explicit acceptance), governance description (cross-check protocol), dates of use. Standards reference: ICMJE 2023+ / COPE 2023+ / Nature/Springer / Science/AAAS / WAME / EU AI Act 2024 / arXiv / ACM / IEEE — these conventions align with established scientific-community practice.

**Authorship convention.** Authorship is human-only; AI tools are tools, not authors. Standard byline: *"[Author Name], [Affiliation]"* (e.g. *"P. Higgins, Rogue Wave Audio"*). The HUF AI Collective is cited in the AI Use Declaration, not in the byline. This conforms to ICMJE / COPE / Nature / Science / WAME conventions on AI authorship.

**Standard Stamp.** The single-page colophon appended to every Hs-produced document — slide deck, report, study output, presentation. Three columns: **The Framework** (Hˢ one-liner, principle, license, validation footprint), **Engines · Methods** (CNT + CNQ versions, plate suite, output formats), **Find us · Contact** (repository URL, quick-start, author + lab, contact). Established 2026-05-14 per Peter directive. Reusable Python helper at [`Studies/_shared/hs_standard_stamp.py`](../../../Studies/_shared/hs_standard_stamp.py); convention doc at [`Studies/_shared/STAMP_STANDARD.md`](../../../Studies/_shared/STAMP_STANDARD.md). Like a publisher's colophon — present, factual, easy to find, never selling.

**Person-noun convention.** In general public-facing output, the word "human" as a person noun is replaced with "researcher" / "user" / "reader" as context calls for; "human-readable" becomes "user-readable". Established at push #25 (2026-05-08) as drift-error correction; promoted to standards-level rule at HUF-STD-001 v1.1 (2026-05-14). Exception contexts (retain "human"): ICMJE authorship rules ("authorship is human-only"), AI-safety vocabulary ("human-in-the-loop"), anthropology / demographic-context studies, regulatory disclosure (EU AI Act, FDA §524B).

**Document versioning.** Conference and study materials carry an explicit version in the header. Major (1.0 → 2.0): substantive content change. Minor (1.0 → 1.1): clarifications, corrections, additions. Patch (1.0 → 1.0.1): typo and link fixes only. Established in CODA-Association folder pattern; documented in [`CODA-Association/CODAwork2026/VERSION_HISTORY.md`](../../CODA-Association/CODAwork2026/VERSION_HISTORY.md).

**Date-stamped media filenames.** Slide decks and PDFs carry an ISO date in the filename (e.g. `CodaWork2026_Talk_2026-05-13.pptx`). Major slide revisions create a new dated file; the prior file moves to `archive/`.

---

## §Q — Change Control (added v2.0)

**Hs Change Control v1.0 (HCC).** NASA-style configuration-management discipline. Eight rules HCC-R001..R008 govern what can change and how. Established push #46 (2026-05-12) following ChatGPT cross-check audit that identified drift between live AI-facing files and the authoritative `HS_FAST_REFRESH.json`. [`HCC_CHARTER.md`](../../HCC_CHARTER.md).

**DCP (Discovery Change Packet).** Formal change-packet template. Every new computational change files a DCP at `proposed` status, then `in_progress`, `implemented`, `verified`. First example: DCP-001 (AI current-state alignment, push #47 — 6 live AI-facing files patched to align with `HS_FAST_REFRESH.json`). DCPs queued during PRE_CONFERENCE_LOCKDOWN at `proposed` and execute post-conference. Template at [`ai-refresh/CHANGE_PACKET_TEMPLATE.json`](../../ai-refresh/CHANGE_PACKET_TEMPLATE.json).

**CHK rule.** A consistency-checker rule in [`scripts/check_ai_refresh_consistency.py`](../../scripts/check_ai_refresh_consistency.py). The checker validates that documented state matches actual state. Live rules: **CHK-JSON-001** (all admin JSONs parse), **CHK-VERSION-001** (no stale engine versions in live files), **CHK-INV-001** (catalog count consistency), **CHK-CCTT-001** (legacy markers on CCTT v0.1 files), **CHK-CNQ-001** (no stale CNQ-pending phrases), **CHK-README-001** (no internal contradictions). Baseline: 23 passes / 0 warnings / 0 errors. Post-conference queued: **CHK-FOUNDATIONS-001** (HUF-STD-003 docstring conformance audit), **CHK-PERSON-NOUN-001** (person-noun convention audit).

**Configuration Items (CIs).** The 15 baseline CIs that define the framework's controlled surface — engine binaries (cnt.py, cnq.py, cnt.R, cnq.R), schemas, INV catalog, NO-CREATE file list, key admin JSONs. Each CI has a current revision, an interface contract, and a change-control gate. Listed in [`ai-refresh/CONFIGURATION_ITEMS.json`](../../ai-refresh/CONFIGURATION_ITEMS.json).

**Interface Controls (IFs).** The 5 interface contracts between subsystems — engine → JSON, JSON → plate, plate → PDF, CNT JSON → CNQ adapter, CNQ output → hash chain. Listed in [`ai-refresh/INTERFACE_CONTROL.json`](../../ai-refresh/INTERFACE_CONTROL.json).

**Traceability Matrix.** Maps each computational module to the doctrine, INV entry, and standards that govern it. [`ai-refresh/TRACEABILITY_MATRIX.json`](../../ai-refresh/TRACEABILITY_MATRIX.json).

**PRE_CONFERENCE_LOCKDOWN.** Repository-wide protective lockdown for the 2026-05-12 → 2026-06-06 conference window (CoDaWork 2026 in Coimbra, 1-5 June). **Allowed:** S1-S2 doc fixes, archive entries, DCP filing without execution, ai-refresh narrative updates, terminology corrections for real reader-confusion bugs. **Forbidden:** engine code changes, schema bumps, claim promotions (STAGED → CANONICAL on disposition entries), `hs_cnq_pdf_exporter.py` implementation, QFT/QWT speculation, CCTT v1.1, NO-CREATE file creation. **S0-defect protocol:** if a defect breaks engine determinism, a focused patch lands with HCC-R001..R008 discipline; everything else queues for post-conference. Documented at [`PRE_CONFERENCE_LOCKDOWN.md`](../../PRE_CONFERENCE_LOCKDOWN.md). Established push #49.

**NO-CREATE files.** Six files explicitly marked "do not create during lockdown." Placeholder paths the framework expects to remain empty until post-conference DCPs execute. The list is captured in PRE_CONFERENCE_LOCKDOWN.md.

**Severity levels.** **S0** = breaks engine determinism (requires patch). **S1** = breaks user-facing claim or doc (allowed under lockdown for fixes). **S2** = doc / wording / cross-reference fixes (always allowed).

**Push protocol.** Standard sequence: pre-flight survey → admin JSON updates → `PUSHnn_PRE_PUSH_SUMMARY.md` (HOLD status) → verification → clear HOLD → `PUSHnn_READY_FOR_COMMIT.md` → commit → push → post-commit sync (record SHA + CI). Documented in [`ai-refresh/PUSHES_INDEX.md`](../../ai-refresh/PUSHES_INDEX.md).

---

## §R — Notation cleanup (v2.0 audit)

Carried over from the v1.0 "Out of scope" section, now mostly closed:

- ✅ Engine schema fields beyond Volume IV's needs — **closed at v2.0** via NOTATION §11 update + this file's §G-§Q additions
- ✅ Atlas module names (Stage 0/1/2/3/4 modules, spectrum_paper, projector_html) — **closed at v2.0** via §L Stage 0 + Stage 1 dual-view + Volume II references
- Termination codes beyond LIMIT_CYCLE_P2 (HS_FLAT, OMEGA_FLAT, SIGNAL_SHORT, ENERGY_STABLE) — still glossed primarily in Volume I §H; no v2.0 changes needed
- Adapter, Mission Command, and CCTT phase-by-phase terminology — still glossed primarily in Volume II §C-§E and `CCTT_RUNBOOK.md`
- ✅ Output Doctrine v1.0 specifics — **closed at v2.0** via §L (Stage taxonomy) and NOTATION §15
- Audit-chain terms (corpus, INDEX, JOURNAL, PUSH-N audit reports) — still glossed primarily in Volume III; PUSHES_INDEX added in §Q

The full-refresh-target threshold (6-8k words) is met by v2.0. Future glossary refreshes will be smaller, term-specific additions tracked in the maintenance log.

---

## Maintenance log

| Version | Date | Push | Summary |
|---|---|---|---|
| v1.0 | 2026-05-08 | #27 | Initial release — minimal-now refresh covering Volume IV terms + HCI vocabulary + Helmsman family proposed extensions. ~53 entries. |
| v2.0 | 2026-05-14 | (TBD) | Full refresh. Added §J HUF Standards / §K Seven Foundations / §L Stage 0 + Dual-View / §M Power Share + Activation Coefficient / §N Canonical Findings / §O Other Doctrines / §P Output Conventions / §Q Change Control / §R Notation cleanup. Updated header to declare v2.0 scope. Promoted Helmsman Stability + Flips + Sigma + Torque Proxy to CANONICAL per schema 3.1.0. Closed several of the v1.0 "out of scope" deferrals via the new sections. Trigger: Peter directive 2026-05-14 — *"an updated terms will now need to be revised, i believe one exists, i may be very outdated and in need of a big refresh."* |

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
*CNT measures invariance. CNQ names the algebra it lives in.*
