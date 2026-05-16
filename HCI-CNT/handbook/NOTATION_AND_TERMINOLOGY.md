# NOTATION AND TERMINOLOGY — Canonical reference

**Version:** v2.0
**Status:** canonical. Initial release push #27 (2026-05-08). Full refresh 2026-05-14 (this document).
**Purpose:** lock the vocabulary used across CNT / CNQ / HCI / Hs documents. Every other document in the repo cites this file for term definitions.
**Maintenance:** this is THE LAW. Drift is caught at review time because this reference exists. New terms enter via Investigation Catalog with explicit definitions; old terms get retired here, not silently.
**Companion:** the existing [`GLOSSARY.md`](GLOSSARY.md) gives the readable narrative; this file gives the locked definitions.

**v2.0 changes (2026-05-14):** Added §13 HUF Standards / §14 Seven Foundations / §15 Output Doctrine v1.0 + Stage 0 / §16 Power Share & Activation Coefficient / §17 Canonical Findings / §18 Other Doctrines / §19 Output Conventions / §20 Change Control. Promoted Helmsman Stability + Flips from PROPOSED → CANONICAL (§4) per schema 3.1.0. Added Stage 0 to Stage taxonomy (§5). Added Triplet Plate + Foundations Plate to plate vocabulary (§11). Renumbered prior §13 → §21 (Citation policy) and prior §14 → §22 (Maintenance).

---

## Why this exists

Between February 2026 and May 2026 the framework moved from a 1st-order linear measurement on a single composition vector to a multi-carrier metric tensor, then to a multi-dimensional depth tower, then to quaternion algebra at D=4, then to a proposed tensor-order ladder for higher-degree analysis. Each layer introduced new vocabulary that wasn't always reconciled with the layer below. ChatGPT's two cross-check audits (push #23 vocabulary cleanup, push #26 tensor terminology + status reconciliation) flagged the drift.

This file is the catch-up. Every term below is locked, with the precise meaning, the alternative usages we are RETIRING, and the alignment to established mathematical and CoDa-community standards.

---

## §1 — Tensor order vs rank

This is the most important entry. Several documents use "rank" loosely; the locked vocabulary is:

| Locked term | Definition | Use for |
|---|---|---|
| **Order** (or **valence**) | Number of indices on a tensor | Saying "κᴴˢ is an order-2 tensor", "the proposed coupling tensor C_ijkl is order-4", "the recursive dyadic step gives order-8" |
| **Rank** (matrix sense) | Linear-independence count of rows/columns of a matrix | "The Helmert matrix has rank D−1" |
| **Rank** (tensor decomposition sense) | Minimum number of rank-1 tensors that sum to a given tensor (CP rank, Tucker rank, etc.) | "Best low-rank approximation of κᴴˢ" — only when explicitly doing decomposition |

**Retired usages:**
- "rank-2 metric tensor κᴴˢ" → say **order-2 metric tensor κᴴˢ**.
- "rank-4 coupling tensor" → say **order-4 coupling tensor**.
- "rank-8 dyadic step" → say **order-8 tensor in the dyadic ladder**.

**Why this matters.** Tensor-decomposition rank (CP rank) and tensor order (number of indices) are mathematically distinct. A rank-1 order-4 tensor is a single outer product u⊗v⊗w⊗x; a rank-4 order-2 tensor is a 4×4 matrix with four linearly independent columns. Conflating them breaks downstream readers who know the standard definitions (Hackbusch; Kolda & Bader; Lim).

**Standard alignment.** Use of "order" for index count follows Kolda & Bader (2009), Hackbusch (2012), and standard differential-geometry usage for tensor valence. Use of "rank" for matrix linear independence and CP-decomposition rank follows the same standards.

---

## §2 — κᴴˢ tensor vs s_j sensitivity vector

The framework has two distinct objects that both involve the inverse-carrier 1/x_j. They are not the same.

| Object | Symbol | Order | Definition |
|---|---|---|---|
| **Higgins Steering Metric Tensor** | κᴴˢ_ij(x) | order-2 | (δ_ij − 1/D) / (x_i x_j) — the Aitchison pullback metric on the simplex |
| **Diagonal carrier steering sensitivity** | s_j(x) | order-1 | 1/x_j — a vector of per-carrier sensitivities |

**Retired usages:**
- "κᴴˢ = 1/x_j" — wrong. That's s_j, not κᴴˢ.
- "the metric tensor diagonal" used as a synonym for κᴴˢ — wrong. The tensor has off-diagonal elements; saying "diagonal" loses them.
- "kappa with no superscript" in formal contexts — always write **κᴴˢ** in formal contexts to disambiguate from any unrelated κ that may appear in citations.

**Standard alignment.** The Aitchison pullback metric is standard CoDa; see Pawlowsky-Glahn, Egozcue & Tolosana-Delgado (2015) §4. Our addition is the engineering name "Higgins Steering Metric Tensor" and the explicit identification of s_j as a separate observable.

**Legacy-usage note.** Several older files in `HCI/calibration/`, `HCI/HCI_FOUNDATION.md`, the early AI-refresh archive (`AI_REFRESH_2026-05-02.md`), and the older calibration JOURNAL use the symbol `κ_{jj} = 1/x_j` to label the diagonal sensitivity quantity. Mathematically, the diagonal of the Aitchison pullback metric κᴴˢ is *not* `1/x_j` — it is `κᴴˢ_jj = (1 − 1/D) / x_j^2` (and the off-diagonal is `κᴴˢ_ij = −(1/D)/(x_i x_j)` for i ≠ j). The legacy `κ_{jj} = 1/x_j` formulae in those files are therefore using "κ" loosely for the per-carrier sensitivity vector `s_j`, not for the κᴴˢ tensor proper. The legacy code computations produce correct numerical results within their stated scope (they were always the sensitivity vector, just imprecisely named); the formal correction is to read `κ_{jj}` in those legacy files as `s_j` (the order-1 sensitivity vector), and to use κᴴˢ in formal contexts only when the full order-2 tensor is meant.

---

## §3 — Frame, dimension, coordinate, axis, basis

These four words are distinct. Lock:

| Term | Locked meaning |
|---|---|
| **Carrier dimension D** | Number of carriers in a composition. A row of a CNT input CSV has D values. |
| **Simplex dimension D−1** | Dimension of the (D−1)-simplex S^(D−1) on which a closed composition lives. |
| **ILR space dimension D−1** | Dimension of the isometric log-ratio space; equal to D−1. |
| **Frame** | A choice of orthonormal basis on the ILR space. Examples: Helmert frame, principal-ILR frame, named scientific balance frame. The frame is always declared in CNQ output. |
| **Basis** | Synonym of frame in this context. Use "frame" in narrative; "basis" when discussing matrix algebra. |
| **Axis** | One direction of a frame. The Helmert frame for D=4 has 3 axes. |
| **Coordinate** | A single component of a vector in a declared frame. "The first coordinate of the ILR-projected composition is …" |
| **Projection dimension** | The dimension of the space CNQ projects into for the quaternion view. For D=4 this is exactly D−1 = 3 (no projection loss). For D > 4, the engine projects to R^3 and reports `captured_step_fraction`. |

**Retired usages:**
- "D=4 quaternion" alone — under-specified. Say **"D=4 trajectory in the Helmert frame, quaternion view in R^3"**.
- "the first 3 dimensions" when meaning the first 3 ILR axes — say **"the first 3 ILR axes"** to avoid confusion with carrier-dimension D.

**Standard alignment.** The ILR construction is Egozcue & Pawlowsky-Glahn (2003). Our Helmert convention is one of multiple valid ILR bases; the framework declares its choice and any future engine adding a different basis must declare that one too.

---

## §4 — Helmsman family taxonomy

The Helmsman started as a metaphor for the σ channel direction in CNT. It's now a vocabulary cluster. The locked taxonomy:

| Term | Locked meaning | Status |
|---|---|---|
| **Helmsman σ** (or just **the Helmsman**) | The directional channel computed by CNT; the σ channel of the four CNT channels (θ, ω, κ, σ) | CANONICAL — engine output |
| **Sign of the Helmsman** | The sign of σ at any timestep; bookkeeping for handedness | CANONICAL |
| **Helmsman Stability** S_σ | 1 − (number_of_flips)/(N−1) over a window; emitted by cnt.py as `helmsman_family.stability_S_sigma.{global, rolling}` | CANONICAL (engine schema 3.1.0, push #37) |
| **Helmsman Flips** | Count of timesteps where σ̂(t) ≠ σ̂(t−1); emitted as `helmsman_family.flips.{total, rolling}` | CANONICAL (engine schema 3.1.0, push #37) |
| **Helmsman Sigma Sequence** | Per-timestep carrier-index sequence; emitted as `helmsman_family.sigma[]` | CANONICAL (engine schema 3.1.0, push #37) |
| **Helmsman Torque Proxy** | Per-timestep proxy for rate-of-change-of-σ; emitted as `helmsman_family.torque_proxy[]` | CANONICAL (engine schema 3.1.0, push #37) |
| **Helmsman Chaos** | Onset of irregular Helmsman dynamics (e.g. period-doubling cascade); reserved for INV-058 Power Spectrum work | PROPOSED (INV-009, INV-058) |
| **Joint Helmsman** | Multi-trajectory coupled Helmsman channel for HCI-AUDIO / HCI-ULTRASOUND multi-driver / multi-element work | PROPOSED |

**Promotion note (push #37, 2026-05-10):** The `navigation_concentration_family` block in CNT schema 3.1.0 promoted Helmsman Stability, Flips, Sigma Sequence, and Torque Proxy from PROPOSED to CANONICAL. They now appear in every CNT JSON output. [`GLOSSARY.md`](GLOSSARY.md) §I reflects this update.

---

## §5 — Tier, Stage, Order, Level, Regime, Degree

All of these are hierarchy words. Each has a locked specific meaning.

| Term | Locked meaning |
|---|---|
| **Tier** | Architectural level of the analytics stack. CoDa, CNT, CNQ are tiers. |
| **Stage** | Atlas plate stage (0, 1, 2, 3, 4). Output-plate level. **Stage 0** added in v2.0 per HUF-STD-003 (Foundations Plate — visualizes the seven linear-algebra components of the framework; reads once per dataset). **Stage 1-4** per Output Doctrine v1.0; see §15 for the Order classification. |
| **Order** | Tensor order (number of indices). Strict mathematical term per §1. ALSO: Output Doctrine derivational order (Order 0 raw / 1 first-principles / 2 inter-timestep / 3 recursive / 4+ inferential) — disambiguated by context; see §15. |
| **Level** | HLR (Higgins Log-Ratio) magnitude scale. The "level" channel of HLR is distinct from any other use of the word. |
| **Regime** | Multi-scale dynamical regime in the HUF sense. Imported from HUF; used for cross-regime analysis. |
| **Degree** | RESERVED — avoid using it informally. If a doc previously said "higher-degree analysis" it should now say "higher-order analysis" (per §1) or be made explicit ("higher Stage", "higher Tier"). |

**Retired usage:**
- "rank-3 plate" or "Stage-3 rank" — say **"Stage 3 plate"** or **"Order 3 in the dyadic ladder"** depending on which is meant.

---

## §6 — Channel, factor, component, field

These four describe substructures of CNT/CNQ outputs. Each is distinct.

| Term | Locked meaning |
|---|---|
| **Channel** | A scalar stream over time produced by the engine. CNT has four channels: θ (angle), ω (angular velocity), κ (curvature; from κᴴˢ), σ (helmsman). |
| **Factor** | A sub-system in a multi-system decomposition. CNQ bi-quaternion factoring (INV-029) produces two factors q_A(t), q_B(t). |
| **Component** | One number — one entry of a vector or one channel value at one timestep. Avoid using "component" to mean "channel" or "factor". |
| **Field** | A function over space or time. Reserve for explicit field-theoretic contexts (e.g. "the metric tensor field κᴴˢ_ij(x) varies over the simplex"). |

---

## §7 — Quaternion subterms

| Term | Locked meaning |
|---|---|
| **Quaternion** | Element of the Hamilton algebra ℍ; w + xi + yj + zk. Order-1 in our usage (it's a 4-vector). |
| **Unit quaternion** | Quaternion with norm 1; element of S^3. Used to encode SO(3) rotations via the SU(2) double cover. |
| **Rotation quaternion** | A unit quaternion specifically used to parameterise an SO(3) rotation. |
| **Sandwich product** | The operation q v q* (or q v q^(-1) for unit q). Rotates a 3-vector v. This is the operation cnq.py verifies at IEEE floor. |
| **Hamilton product** | Quaternion multiplication q_1 q_2. Distinct from the sandwich product. |
| **SLERP** | Spherical linear interpolation between two unit quaternions. Proposed CNQ engine feature (CANDIDATE). |
| **Twin-quaternion factoring** | Decomposition of a D=8 trajectory into two coupled SU(2) elements q_A, q_B via the SO(8) ⊃ SU(2) × SU(2) factoring. **This is what INV-029 is about.** |
| **Bi-quaternion** (strict mathematical) | Element of ℍ ⊗ ℂ; the standard Lorentz-physics / Clifford-algebra meaning. Distinct from twin-quaternion factoring. |

**Important — INV-029 wording correction.** Until push #27, the framework's INV-029 documents used "bi-quaternion factoring" informally to mean SU(2) × SU(2) decomposition. Strict mathematical "bi-quaternion" means something else (ℍ ⊗ ℂ). Push #27 introduces the term **twin-quaternion factoring** as the locked name for the SU(2) × SU(2) decomposition. The legacy phrase "bi-quaternion factoring" remains in section headers for backward-compatibility but every body-text mention now disambiguates.

---

## §8 — Aitchison / CoDa community alignment

Where our terms map onto established CoDa vocabulary. Citations are to authoritative references; the terms themselves are unchanged from those sources.

| Our usage | CoDa standard | Source |
|---|---|---|
| **Closure** C(x) = x / Σx | Same; Aitchison's closure operator | Aitchison (1986) The Statistical Analysis of Compositional Data |
| **CLR** centred log-ratio | Same; clr(x)_i = log(x_i / g(x)) where g is geometric mean | Aitchison (1986) |
| **ALR** additive log-ratio | Same; not used canonically in our framework but defined where mentioned | Aitchison (1986) |
| **ILR** isometric log-ratio | Same; orthonormal-basis projection of CLR | Egozcue, Pawlowsky-Glahn, Mateu-Figueras & Barceló-Vidal (2003) |
| **Aitchison distance** | Same; ‖clr(x) − clr(y)‖_2 | Aitchison (1986) |
| **Simplex** S^(D−1) | Same; (D−1)-simplex of D-component compositions | Standard |
| **Aitchison pullback metric** | Same as κᴴˢ | Pawlowsky-Glahn et al. (2015) §4 |
| **Helmert basis / Helmert contrast** | Same construction; one of many valid ILR bases. Our convention is documented in [`HCI-CNQ/CNQ_SCOPE_AND_LIMITS.md`](../../HCI-CNQ/CNQ_SCOPE_AND_LIMITS.md) §3 | Helmert (1875); standard in compositional statistics |
| **Aitchison geometry** | Same; the metric-space geometry on the simplex induced by Aitchison's inner product | Pawlowsky-Glahn et al. (2015) |

**Our additions** (beyond standard CoDa):

| Our term | What it adds |
|---|---|
| **HLR** (Higgins Log-Ratio Level) | Magnitude scale layer separating shape from size in compositional dynamics |
| **CNT** (Compositional Navigation Tensor) | Engine producing the four channels (θ, ω, κ, σ) over compositional time-series |
| **CNQ** (Compositional Navigation Quaternion) | Quaternion-native view of D=4 (and projected D≠4) trajectories |
| **κᴴˢ** | Engineering name for the Aitchison pullback metric in our system |
| **DCDI / Helmsman σ** | The directional / handedness channel |
| **LIMIT_CYCLE_P2** | Period-2 attractor termination of the CNT depth tower; the "universal compositional invariance signature" of Paper 1 |
| **Depth tower** | CNT-specific recursive structure tracking energy and curvature termination |
| **IR class** | 8-class taxonomy of trajectory information-recovery termination |

---

## §9 — Trajectory, path, walk, sequence

These four describe different views of the same time-ordered composition data.

| Term | Locked meaning |
|---|---|
| **Compositional time-series** | The raw data: an ordered list of D-vectors over time. |
| **Trajectory** | The geometric path through CLR / ILR space defined by the time-series. |
| **Path** | Synonym of trajectory in geometric contexts. Use "trajectory" in narrative. |
| **Walk** | Discrete-step view of the trajectory, useful for return-map and depth-tower analysis. |
| **Sequence** | Index-ordered view; emphasises ordering rather than geometry. |

---

## §10 — Closure, invariance, signature, period

| Term | Locked meaning |
|---|---|
| **Closure** (operator C) | Aitchison's rescale-to-sum-1 operator. |
| **Closure** (control-system sense) | Closing a feedback loop. Used only in DADC / ADAC contexts; always disambiguated by surrounding text. |
| **Structural invariance** | A specific algebraic invariance the trajectory carries: SO(D−1) simplex rotation, SU(2) handedness, M^2 = I metric involution (time-reversal). The framework relies on three. |
| **Invariance signature** | A pattern in the data that exhibits a structural invariance. LIMIT_CYCLE_P2 is the framework's named invariance signature. |
| **Universal Compositional Invariance Signature (UCIS)** | Paper 1's term for LIMIT_CYCLE_P2 viewed as universal across flow-directional compositional dynamics that meet the structural preconditions. |
| **Period** (in LIMIT_CYCLE_Pn) | The period of the depth-tower return map — specifically, P2 means the return map has a period-2 attractor. Distinct from any other use of "period" in physics. |

---

## §11 — Engine, ledger, output, plate

| Term | Locked meaning |
|---|---|
| **Engine** | A compiled program: cnt.py, cnq.py, cnt.R, cnq.R. Strict. The "instrument family" is wider; the engine is one program. |
| **Ledger** | An output JSON file with hash-chained provenance. CNT JSON is a ledger; CNQ JSON is a ledger. The audit trail metaphor is the same. |
| **Output** | The artefact a tool produces. Can be a ledger, a plate, a report, an experiment record. |
| **Plate** | An atlas Stage 0/1/2/3/4 visual diagram output. Specific HCI vocabulary. Standard plate types as of v2.0: Foundations Plate (Stage 0), Section Plate + ILR-Helmert Triplet Plate (Stage 1 — Dual-View doctrine), Helmsman + Course + CoDa-PCA biplot (Stage 2), Depth tower + Attractor + κ^HS (Stage 3). |
| **Foundations Plate** | The Stage-0 plate per HUF-STD-003 — visualizes the seven linear-algebra foundations (§14): variation matrix heatmap, Helmert basis + orthonormality check, decomposition tree, eigenvalue scree, orthonormal eigenbasis Q, Spectral Theorem verification residual. Generator: `HCI/codawork2026/stage0_foundations/foundations_plate.py`. |
| **Section Plate** | A Stage-1 plate (Multiplexed Carrier Section Plate) — XY plan view + XZ bearings + YZ CLR per timestep. CoDa-Standard reading. Generator: `HCI/codawork2026/stage1_plates/stage1_plates_raw.py`. |
| **ILR-Helmert Triplet Plate** | The orthonormal companion to Section Plate at Stage 1 — three orthogonal scatter projections (ilr_1×ilr_2, ilr_1×ilr_3, ilr_2×ilr_3) of the CLR trajectory under the Helmert basis. Reads trajectory shape in compositional geometry. Generator: `HCI/codawork2026/stage1_plates/ilr_triplet_plate.py` (added push #50, 2026-05-13). |
| **Dual-View Stage 1 Output** | The paired Section + Triplet reading per dataset. Section reads magnitudes per timestep; Triplet reads trajectory shape in ILR space. Together they form the complete Stage-1 doctrine. |
| **Power Share Plate** | The forthcoming Stage-1 sibling that visualizes per-carrier Power Share + Activation Coefficient per transition step (§16). Demonstrated externally on religion data 2026-05-14; engine-native implementation queued as Order-1 post-conference target per HUF-STD-002. |
| **CNQ Dashboard** | A single-page summary of CNQ output per dataset — Higgins scale Hs(t), angular velocity ω(t), K_eff + TV distance, helmsman σ(t), step-Δ Aitchison spike detector, CNQ diagnostics box (CHSH joint-coherence, twin-quaternion factor, attractor fit). |
| **Standard Stamp** | The colophon page appended to every Hs-produced document (§19). Reusable helper at `Studies/_shared/hs_standard_stamp.py`. |

---

## §12 — Bi-quaternion correction note

This is the wording fix that triggered most of push #27. Any document that previously said:

> "Bi-quaternion factoring of a D=8 trajectory yields two coupled quaternion paths."

Now reads:

> "Twin-quaternion factoring of a D=8 trajectory yields two coupled SU(2) elements q_A(t), q_B(t)."

Where "bi-quaternion" appears in legacy headings (e.g. `CNQ_BIQUATERNION_FACTORING.md` filename, INV-029 title), it is preserved for repo-history continuity but disambiguated in the body text. The strict mathematical "bi-quaternion" (ℍ ⊗ ℂ) is reserved for explicit Lorentz / Clifford contexts where it actually applies.

This correction was raised in push #27 and is filed as a revision-note on INV-029, not as a falsification or a new investigation. The mathematics underlying the factoring is unchanged; only the name is corrected.

---

## §13 — HUF Standards reference

Three numbered standards govern HUF and Hs media, output pipeline, and mathematical foundations. Every framework document intended for external audiences must conform.

| Standard | Title | Scope | File |
|---|---|---|---|
| **HUF-STD-001** | HUF Publication Standards | AI Use Declaration template, authorship rules, person-noun convention, hash chain, versioning, licensing — anything intended for external audiences | [`huf-gov/standards/HUF_PUBLICATION_STANDARDS.json`](../../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json) v1.1 (2026-05-14) |
| **HUF-STD-002** | HUF Tensor Train I/O Standard | The data → CNT → CNQ → vector-output chain (PDF/PNG/SVG); PPTX excluded as conference-only | [`huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json`](../../huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) v1.0 |
| **HUF-STD-003** | Hs Linear Algebra Foundations | The seven linear-algebra components (§14 below) every Hs engine and plate generator employs | [`huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json`](../../huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json) v1.0 |

**Standard citation in conforming docs:** *"Conforms to HUF-STD-001 + HUF-STD-002 + HUF-STD-003."*

**Authority chain:** Sibling standards; each cites the others. All three are children of the HUF Governance Charter and the parent doctrines (Output Doctrine v1.0, SAFE-001, LOOP-001).

---

## §14 — The seven linear-algebra foundations (HUF-STD-003)

The framework rests on seven classical linear-algebra components. Names locked. Established push #50 (2026-05-14).

| # | Component | Hs locations |
|---|---|---|
| 1 | **Symmetric Matrix** | Variation matrix var(log x_i/x_j); CLR covariance Cov(clr(X)); Gram matrix H·Hᵀ = I |
| 2 | **Property of Transpose** | ILR ↔ CLR via H and Hᵀ; covariance propagation Cov(M·X) = M·Cov(X)·Mᵀ; orthonormality H·Hᵀ = I |
| 3 | **Matrix Decomposition** | closure → CLR → ILR chain; pairwise bearing tensor decomposition; depth tower; CoDa-PCA |
| 4 | **Eigenvectors / Eigenvalues** | Attractor fit (cnq.py); κ^HS sensitivity vector; CoDa-PCA principal axes |
| 5 | **Strong Property of Symmetric Matrices (Spectral Theorem)** | Silent justification of ILR orthonormality, CoDa-PCA producing real eigenvalues, and all PCA-like steps. Verified at IEEE-floor in Stage-0 plates. |
| 6 | **Spectral Decomposition** | Σ = Q Λ Qᵀ explicit; rank-k truncation (Eckart-Young); Stage-2 biplot top-k visualization |
| 7 | **Visualization** | Stage-0 Foundations Plate is the dedicated tier; Stages 1-4 visualize consequences |

**Companion documents:** [`huf-gov/standards/FOUNDATIONS.md`](../../huf-gov/standards/FOUNDATIONS.md) (narrative); [`huf-gov/standards/FOUNDATIONS_TRACEABILITY.md`](../../huf-gov/standards/FOUNDATIONS_TRACEABILITY.md) (per-foundation file/plate/schema audit).

**Conformance:** Every new computational module shall declare which foundations it employs in its docstring (HUF-STD-003 §conformance_requirements). Future consistency-checker rule CHK-FOUNDATIONS-001 will audit declarations against actual content (post-conference target).

---

## §15 — Output Doctrine v1.0 — Order classification

The framework's data outputs are classified by derivational order. Locked May 5 2026 at [`HCI-CNT/conference_demo/cnt_demo/05_doctrine/OUTPUT_DOCTRINE.md`](../../HCI-CNT/conference_demo/cnt_demo/05_doctrine/OUTPUT_DOCTRINE.md). Extended at push #50 (2026-05-14) to include Order 0+ for the Foundations layer.

| Order | Meaning | Stage tier | Plate examples |
|---|---|---|---|
| **0** | Pre-engine raw data, before closure | (adapter) | (adapter disclosure, not a plate) |
| **0+** | Foundational — geometric structure of the data itself | **Stage 0** | Foundations Plate (variation matrix, Helmert basis, eigenvalue spectrum) |
| **1** | First-principles — per-timestep CNT tensor reading | **Stage 1** | Section Plate (CoDa-Standard) + ILR-Helmert Triplet Plate (orthonormal) |
| **2** | Inter-timestep — helmsman, course, variation analysis | **Stage 2** | Helmsman frequency, course plot, CoDa-PCA biplot, navigation summary |
| **3** | Recursive — depth tower, attractor, IR class | **Stage 3** | Depth tower visualization, attractor fit dashboard, κ^HS energy |
| **4+** | Inferential — EITT bench, cross-dataset comparison, schema validation | **Stage 4+** | Cross-corpus comparison, EITT decimation verification, validator surface |

Stage 0 is read **once per dataset** (foundations don't change frame-to-frame; they characterize the data's geometry). Stage 1 is read **once per timestep**. Together they form the complete per-dataset reading. Stage-2/3/4 aggregate across timesteps.

---

## §16 — Power Share / Activation Coefficient

Per-carrier directional-work decomposition. Locked 2026-05-14.

| Term | Locked definition |
|---|---|
| **Power Share** | `power_share_j(t)  =  (ΔCLR_j)²  /  Σ_k (ΔCLR_k)²` — per-carrier fraction of squared CLR motion at one transition step. Sums to 100% across carriers per step. Identical to the per-carrier component of squared Aitchison distance: `d²(t-1,t) = Σ_k (ΔCLR_k)²`. |
| **Activation Coefficient** | `activation_coefficient_j(t)  =  power_share_j(t)  /  composition_share_j(t-1)` — leverage ratio of directional work to size. AC > 1 means the carrier is structurally activating the system beyond its share; AC ≫ 1 (e.g. > 10) names "yeast factor" cases where small-share carriers do disproportionate directional work. |
| **Activation Threshold** | AC = 1 (neutral). AC > 1 is "activated." Convention: a carrier is considered structurally activating when AC > 1.5 AND power share > 5% (filters numerical noise). |
| **Yeast Factor** | Legacy / informal naming. The formal term is Activation Coefficient. "Yeast" is retained in explanatory prose because the biological metaphor (small quantity, large transformative effect) is the right intuition; the formal mathematics is the squared-CLR-change decomposition above. |

**Engine status:** As of v2.0, computed externally from CLR coordinates already emitted in CNT JSON `tensor.timesteps[t].coda_standard.clr[]`. Native engine block planned post-conference as schema bump 3.1.0 → 3.2.0 with new fields `tensor.timesteps[t].power_share[]` and `activation_coefficient[]`. New plate generator `HCI/codawork2026/stage1_plates/power_share_plate.py` will be Stage-1 sibling to Section + Triplet (HUF-STD-002 post_conference_implementation_targets Order 1; INV-060 promotion path STAGED → CANONICAL).

**Reference demonstration:** [`CODA-Association/Studies/Religion_2026-05-14/Religion_HiddenDirections_2026-05-14.pdf`](../../CODA-Association/Studies/Religion_2026-05-14/Religion_HiddenDirections_2026-05-14.pdf) slide 8/12. Religion data surfaced activation coefficients up to 148× (USA Hindus 2030→2040 step).

**Standard inclusion:** Per Peter directive 2026-05-14, Power Share + Activation Coefficient become a **standard inclusion in every Hˢ-produced data deliverable** going forward, sibling to Section Plate and Triplet Plate at Stage 1.

---

## §17 — Canonical findings (named investigations registered CANONICAL)

Selected CANONICAL Investigation Catalog entries that have entered the framework vocabulary as locked findings. (Full list: [`INVESTIGATION_CATALOG.md`](../../ai-refresh/INVESTIGATION_CATALOG.md).)

| Finding | Locked statement |
|---|---|
| **MC-4 three-conjunct claim** (push #39) | *"No monitoring framework in the energy / market-share literature operates natively in Aitchison geometry with formal change detection at the carrier level — three conjuncts combined into one observable stack."* Sharpened from earlier 4-conjunct formulation. The MC-4 packet sits at [`papers/codawork2026/planning/`](../../papers/codawork2026/planning/) — claim, evidence, falsifiability boundaries. |
| **INV-050 metric pair-invariance** | Total Variation distance and Aitchison distance agree on every shock hit/miss verdict across the 9-country EMBER 2001-2025 corpus. Demonstrated pair-invariance only; broader-family invariance is INV-050.Q2 (open). |
| **INV-051 deceptive drift 5-of-9** | The deceptive-drift signature (Aitchison distance moves while individual carrier percentages stay near-stationary) fires in 5 of 9 EMBER countries at annual grain. Headline: Germany p ≈ 0.0016. Carriers: AUS, CHN, GBR, IND, JPN. |
| **EITT** Entropy-Invariant Time Transformer | The geometric-mean decimation step within the Hs pipeline that preserves Shannon entropy at 0.18% variation across 341:1 compression. Documented at [`papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md`](../../papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md). |
| **LIMIT_CYCLE_P2** | Period-2 attractor termination of the CNT depth tower; the "universal compositional invariance signature" of Paper 1. Three IEEE-floor confirmations (Backblaze drives, Planck CMB, SM neutrino). |
| **Three IEEE-floor confirmations** | The three load-bearing datasets reproducing LIMIT_CYCLE_P2 + IEEE-floor max_residual: backblaze_fleet (D=4 N=731), planck_cmb_boson (D=4 N=2499), sm_neutrino_oscillation (D=3 N=1000). Bit-identical residual 4.44e-16 across systems. |
| **INV-059 humble-invitation framing** | Cross-model validation: two independent external models (ChatGPT session 2, Grok round 5) reading the MC-4 packet cold produced convergent humble-invitation framing recommendations. The conference talk's posture is independently stress-tested. |

---

## §18 — Other locked doctrines

| Doctrine | What it says | Citation |
|---|---|---|
| **CRD-1.0** (Coherent Range Doctrine) | Every multi-carrier comparison is computed on the intersection of all members' time ranges; the shortest-coverage member sets the binding window; every output declares its coherent-range manifest in its header. | [`docs/COHERENT_RANGE_DOCTRINE.md`](../../docs/COHERENT_RANGE_DOCTRINE.md) (push #33, INV-047) |
| **SEA-1.0** (Suspicion of Every Assumption) | Every public function and claim enumerates its failure modes with mitigation evidence; the engine is guilty until proven innocent. | [`docs/SUSPICION_OF_EVERY_ASSUMPTION.md`](../../docs/SUSPICION_OF_EVERY_ASSUMPTION.md) (push #32, INV-045) |
| **STP-1.0** (Self-Test Protocol / BIST) | Every engine carries a frozen reference corpus and a runner that produces dated, hash-chained receipts of pass/fail status. | [`docs/SELF_TEST_PROTOCOL.md`](../../docs/SELF_TEST_PROTOCOL.md) (push #32, INV-046) |
| **Engine independence policy** | `cnt_content_sha256` and `cnq_content_sha256` are unrelated by design. Cross-engine hash chains are forbidden. Each engine is deterministic on its own. | [`ai-refresh/CNT_V3_CNQ_V2_DESIGN.md`](../../ai-refresh/CNT_V3_CNQ_V2_DESIGN.md) (push #32) |
| **Tensor Train v1.0** | The named data → CNT → CNQ → vector-output chain. Four links: adapter (Order 0) → CNT (Orders 1-3) → CNQ (Order 2-3 algebraic) → vector output (PDF/PNG/SVG). PPTX excluded as conference-only. | [`huf-gov/standards/TENSOR_TRAIN.md`](../../huf-gov/standards/TENSOR_TRAIN.md) (HUF-STD-002, push #50) |
| **Output Doctrine v1.0** | Order/Stage classification of plate outputs (§15 above). | [`HCI-CNT/conference_demo/cnt_demo/05_doctrine/OUTPUT_DOCTRINE.md`](../../HCI-CNT/conference_demo/cnt_demo/05_doctrine/OUTPUT_DOCTRINE.md) (locked 2026-05-05) |
| **HUF Governance Charter** | Nine-article governance document for HUF + Hs + derivative repos. Articles include Integrity of Purpose, Accountable Data, Accountable Resolution. | [`huf-gov/HUF_GOVERNANCE_CHARTER.md`](../../huf-gov/HUF_GOVERNANCE_CHARTER.md) |
| **SAFE-001** | Cognitive-agent safety doctrine. Governs AI-tool use in framework operations. | [`huf-gov/governance/SAFE-001.json`](../../huf-gov/governance/SAFE-001.json) |
| **LOOP-001** | Open-loop doctrine. Skydiver Principle — the operator holds the last breaker. | [`huf-gov/governance/LOOP-001.json`](../../huf-gov/governance/LOOP-001.json) |
| **KILL-001** | Named-failure-modes catalog (19 modes). | [`huf-gov/governance/KILL-001.json`](../../huf-gov/governance/KILL-001.json) |

---

## §19 — Output conventions (HUF-STD-001)

| Convention | Locked meaning |
|---|---|
| **HUF AI Collective** | Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI) — cross-check participants in Hs work. Operated under HUF Governance Charter Articles II-IV + SAFE-001. Disclosed in AI Use Declaration sections, NOT in author bylines. |
| **AI Use Declaration** | Mandatory section in every external-audience document, placed at the END (before signature lines / repository pointers), per HUF-STD-001. Lists AI tools used, tasks performed, author responsibility, governance, dates of use. Standards reference: ICMJE / COPE / Nature/Springer / Science/AAAS / WAME / EU AI Act 2024 / arXiv / ACM / IEEE. |
| **Authorship convention** | Authorship is human-only; AI tools are tools, not authors. Standard byline: `[Author Name], [Affiliation]` (e.g. "P. Higgins, Rogue Wave Audio"). The HUF AI Collective is cited in the AI Use Declaration, not in the byline. |
| **Standard Stamp** | The colophon page appended to every Hs-produced document (slide deck, report, study output, presentation). Three columns: Framework / Engines + Methods / Find us + Contact. Reusable helper at [`Studies/_shared/hs_standard_stamp.py`](../../../Studies/_shared/hs_standard_stamp.py). Convention documented at [`Studies/_shared/STAMP_STANDARD.md`](../../../Studies/_shared/STAMP_STANDARD.md). Established 2026-05-14. |
| **Person-noun convention** | In general public-facing output, the word "human" as a person noun is replaced with "researcher", "user", or "reader" as context calls for. "human-readable" → "user-readable". Established at push #25 (2026-05-08) as drift-error correction; promoted to HUF-STD-001 standards-level rule at v1.1 (2026-05-14). Exceptions retained for ICMJE authorship rules ("authorship is human-only"), AI-safety vocabulary ("human-in-the-loop"), anthropology / demographic-context studies, and regulatory disclosure (EU AI Act, FDA §524B). |
| **Document versioning** | Conference and study materials carry an explicit version in the header (e.g. v1.2). Major version (1.0 → 2.0) for substantive content change; minor (1.0 → 1.1) for clarifications and revisions; patch (1.0 → 1.0.1) for typo and link fixes. Established in CODA-Association folder pattern. |
| **File naming for media** | Slide decks and PDFs carry an ISO date stamp in the filename (e.g. `CodaWork2026_Talk_2026-05-13.pptx`). Major slide revisions create a new dated file; prior file moves to `archive/`. |

---

## §20 — Change Control (HCC, DCP, CHK, Lockdown)

| Term | Locked meaning |
|---|---|
| **Hs Change Control v1.0 (HCC)** | NASA-style configuration-management discipline for the framework. Eight rules HCC-R001..R008 govern what can change and how. Established push #46 (2026-05-12). Lives at [`HCC_CHARTER.md`](../../HCC_CHARTER.md). |
| **DCP** (Discovery Change Packet) | Formal change-packet template. New computational changes file as a DCP at `proposed` status, then `in_progress`, `implemented`, `verified`. First example: DCP-001 (AI current-state alignment, push #47). Template at [`ai-refresh/CHANGE_PACKET_TEMPLATE.json`](../../ai-refresh/CHANGE_PACKET_TEMPLATE.json). |
| **CHK rule** | A consistency-checker rule in [`scripts/check_ai_refresh_consistency.py`](../../scripts/check_ai_refresh_consistency.py). Existing rules (as of v2.0): CHK-JSON-001 (JSON parse), CHK-VERSION-001 (no stale engine versions), CHK-INV-001 (catalog consistency), CHK-CCTT-001 (legacy markers), CHK-CNQ-001 (no stale CNQ-pending phrases), CHK-README-001 (no internal contradictions). Post-conference proposed: CHK-FOUNDATIONS-001 (HUF-STD-003 docstring conformance), CHK-PERSON-NOUN-001 (person-noun convention). |
| **Configuration Items (CIs)** | The 15 baseline CIs that define the framework's controlled surface — engine binaries, schemas, INV catalog, NO-CREATE files, key admin JSONs. Listed in [`ai-refresh/CONFIGURATION_ITEMS.json`](../../ai-refresh/CONFIGURATION_ITEMS.json). |
| **Interface Controls (IFs)** | The 5 interface contracts between subsystems (engine ↔ JSON, JSON ↔ plate, plate ↔ PDF, etc.). Listed in [`ai-refresh/INTERFACE_CONTROL.json`](../../ai-refresh/INTERFACE_CONTROL.json). |
| **Traceability Matrix** | Maps each computational module to the doctrine, INV entry, and standards that govern it. [`ai-refresh/TRACEABILITY_MATRIX.json`](../../ai-refresh/TRACEABILITY_MATRIX.json). |
| **PRE_CONFERENCE_LOCKDOWN** | Repository-wide protective lockdown for the 2026-05-12 → 2026-06-06 conference window. Allowed: S1-S2 doc fixes, archive entries, DCP filing without execution. Forbidden: engine code changes, claim promotions, NO-CREATE file creation, `hs_cnq_pdf_exporter.py` implementation, schema bumps. S0-defect protocol governs the only allowed engine touches. Documented at [`PRE_CONFERENCE_LOCKDOWN.md`](../../PRE_CONFERENCE_LOCKDOWN.md). |
| **NO-CREATE files** | Six files marked "do not create during lockdown" — placeholder paths the framework expects to remain empty until post-conference DCPs execute. |
| **Severity levels** | S0 = breaks engine determinism (requires patch); S1 = breaks user-facing claim or doc (allowed under lockdown); S2 = doc / wording / cross-reference fixes (always allowed). |
| **Push protocol** | Standard sequence per push: pre-flight survey → admin JSON updates → PUSHnn_PRE_PUSH_SUMMARY.md (HOLD) → verification → clear HOLD → PUSHnn_READY_FOR_COMMIT.md → commit → post-commit sync. Documented in [`ai-refresh/PUSHES_INDEX.md`](../../ai-refresh/PUSHES_INDEX.md). |

---

## §21 — Citation policy for documents using this reference

Every document that uses any term defined here SHOULD cite:

```
Notation: see Hs/HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md v2.0 (2026-05-14).
```

A short reference is sufficient. The point is to give downstream readers a single place to resolve ambiguity and to make future term-drift visible (anything that doesn't cite this file or that introduces a new term without an entry here is a defect to be fixed).

---

## §22 — Maintenance

This file is updated when:

1. A new term enters the framework canon (typically promoted from an Investigation Catalog entry or a standards JSON).
2. A retired usage is identified (typically by AI cross-check audit).
3. A standard reference (Aitchison community update, Egozcue paper) is published that affects our alignment.
4. A new HUF standards JSON (HUF-STD-NNN) is established.
5. A new doctrine is locked at HUF-Governance level.

Each update lands in a push and is recorded in the AI refresh narrative for that push.

**Version log:**

| Version | Date | Push | Summary |
|---|---|---|---|
| v1.0 | 2026-05-08 | push #27 | Initial release. Sections §1-§14 covering tensor order vs rank, κᴴˢ vs s_j, frames/dimensions, helmsman family, tier/stage/order, channels/factors/components, quaternion subterms, CoDa alignment, trajectory vocabulary, closure/invariance, engine/ledger/output/plate, bi-quaternion correction, citation policy, maintenance. |
| v2.0 | 2026-05-14 | push (TBD) | Full refresh. Added §13 HUF Standards reference (HUF-STD-001/002/003). Added §14 Seven Linear-Algebra Foundations. Added §15 Output Doctrine v1.0 Order classification (extended to Order 0+ for Foundations). Added §16 Power Share / Activation Coefficient (formerly informal "yeast factor"). Added §17 Canonical Findings (MC-4, INV-050, INV-051, EITT, LIMIT_CYCLE_P2, IEEE-floor confirmations, INV-059). Added §18 Other Locked Doctrines (CRD, SEA, STP, Engine Independence, Tensor Train, Output Doctrine, HUF Governance Charter, SAFE-001, LOOP-001, KILL-001). Added §19 Output Conventions (HUF AI Collective, AI Use Declaration placement, authorship, Standard Stamp, person-noun convention, document versioning). Added §20 Change Control (HCC, DCP, CHK rules, CIs, IFs, traceability, PRE_CONFERENCE_LOCKDOWN, NO-CREATE, severity levels, push protocol). Updated §4 to promote Helmsman Stability + Flips + Sigma Sequence + Torque Proxy from PROPOSED to CANONICAL per CNT schema 3.1.0 (push #37). Updated §5 to add Stage 0. Updated §11 to add Foundations Plate, ILR-Helmert Triplet Plate, Dual-View Stage 1 Output, Power Share Plate, CNQ Dashboard, Standard Stamp. Renumbered prior §13 → §21 (Citation policy) and §14 → §22 (this section). |

**v2.0 trigger:** Peter directive 2026-05-14 — *"an updated terms will now need to be revised, i believe one exists, i may be very outdated and in need of a big refresh."* Survey identified ~25 new terms added since push #27 across pushes #28-#50 that had not been codified in this file. Full refresh executed under PRE_CONFERENCE_LOCKDOWN as S2 doc-only work.

---

## Cross-references

- Glossary (narrative, with examples): [`GLOSSARY.md`](GLOSSARY.md)
- Investigation Catalog (where new terms are first proposed): [`../../ai-refresh/INVESTIGATION_CATALOG.md`](../../ai-refresh/INVESTIGATION_CATALOG.md)
- CNQ-specific scope and limits: [`../../HCI-CNQ/CNQ_SCOPE_AND_LIMITS.md`](../../HCI-CNQ/CNQ_SCOPE_AND_LIMITS.md)
- Claim-strength locked language: [`../../HCI-CNQ/CLAIM_STRENGTH_TABLE.md`](../../HCI-CNQ/CLAIM_STRENGTH_TABLE.md)
- Operations protocol (catalog maintenance): [`../../OPERATIONS_PROTOCOL.md`](../../OPERATIONS_PROTOCOL.md) §14

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
