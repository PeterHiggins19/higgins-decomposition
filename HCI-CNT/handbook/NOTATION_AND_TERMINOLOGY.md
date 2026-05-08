# NOTATION AND TERMINOLOGY — Canonical reference

**Status:** canonical, push #27 (2026-05-08).
**Purpose:** lock the vocabulary used across CNT / CNQ / HCI / Hs documents. Every other document in the repo cites this file for term definitions.
**Maintenance:** this is THE LAW. Drift is caught at review time because this reference exists. New terms enter via Investigation Catalog with explicit definitions; old terms get retired here, not silently.
**Companion:** the existing [`GLOSSARY.md`](GLOSSARY.md) gives the readable narrative; this file gives the locked definitions.

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
| **Helmsman Stability** S_σ | Variance / persistence of σ over a window | PROPOSED (INV-009) |
| **Helmsman Flips** | Count or rate of σ sign-changes | PROPOSED (INV-009) |
| **Helmsman Chaos** | Onset of irregular Helmsman dynamics (e.g. period-doubling cascade) | PROPOSED (INV-009) |
| **Helmsman Torque** | Rate-of-change-of-σ object; informal proposal | PROPOSED (INV-009) |
| **Joint Helmsman** | Multi-trajectory coupled Helmsman channel for HCI-AUDIO / HCI-ULTRASOUND multi-driver / multi-element work | PROPOSED |

PROPOSED items are documented in [`GLOSSARY.md`](GLOSSARY.md) §I and gated on either cnt.py implementation or a hand-computation pilot (INV-009 in the Investigation Catalog). They do not appear in current cnt.py output.

---

## §5 — Tier, Stage, Order, Level, Regime, Degree

All of these are hierarchy words. Each has a locked specific meaning.

| Term | Locked meaning |
|---|---|
| **Tier** | Architectural level of the analytics stack. CoDa, CNT, CNQ are tiers. |
| **Stage** | Atlas plate stage (1, 2, 3, 4). Output-plate level. Defined in HCI-CNT atlas docs. |
| **Order** | Tensor order (number of indices). Strict mathematical term per §1. |
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
| **Engine** | A compiled program: cnt.py, cnq.py, cnt.R. Strict. The "instrument family" is wider; the engine is one program. |
| **Ledger** | An output JSON file with hash-chained provenance. CNT JSON is a ledger; CNQ JSON is a ledger. The audit trail metaphor is the same. |
| **Output** | The artefact a tool produces. Can be a ledger, a plate, a report, an experiment record. |
| **Plate** | An atlas Stage 1/2/3/4 visual diagram output. Specific HCI vocabulary. |
| **Section plate** | A specific HCI plate type (Multiplexed Carrier Section Plate). |

---

## §12 — Bi-quaternion correction note

This is the wording fix that triggered most of push #27. Any document that previously said:

> "Bi-quaternion factoring of a D=8 trajectory yields two coupled quaternion paths."

Now reads:

> "Twin-quaternion factoring of a D=8 trajectory yields two coupled SU(2) elements q_A(t), q_B(t)."

Where "bi-quaternion" appears in legacy headings (e.g. `CNQ_BIQUATERNION_FACTORING.md` filename, INV-029 title), it is preserved for repo-history continuity but disambiguated in the body text. The strict mathematical "bi-quaternion" (ℍ ⊗ ℂ) is reserved for explicit Lorentz / Clifford contexts where it actually applies.

This correction was raised in push #27 and is filed as a revision-note on INV-029, not as a falsification or a new investigation. The mathematics underlying the factoring is unchanged; only the name is corrected.

---

## §13 — Citation policy for documents using this reference

Every document that uses any term defined here SHOULD cite:

```
Notation: see Hs/HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md (push #27).
```

A short reference is sufficient. The point is to give downstream readers a single place to resolve ambiguity and to make future term-drift visible (anything that doesn't cite this file or that introduces a new term without an entry here is a defect to be fixed).

---

## §14 — Maintenance

This file is updated when:

1. A new term enters the framework canon (typically promoted from an Investigation Catalog entry).
2. A retired usage is identified (typically by AI cross-check audit).
3. A standard reference (Aitchison community update, Egozcue paper) is published that affects our alignment.

Each update lands in a push and is recorded in the AI refresh narrative for that push. The push #27 narrative ([`AI_REFRESH_2026-05-08_push26_27_chatgpt_round2_engine_terminology.md`](../../ai-refresh/AI_REFRESH_2026-05-08_push26_27_chatgpt_round2_engine_terminology.md)) is the inaugural reference.

---

## Cross-references

- Glossary (narrative, with examples): [`GLOSSARY.md`](GLOSSARY.md)
- Investigation Catalog (where new terms are first proposed): [`../../ai-refresh/INVESTIGATION_CATALOG.md`](../../ai-refresh/INVESTIGATION_CATALOG.md)
- CNQ-specific scope and limits: [`../../HCI-CNQ/CNQ_SCOPE_AND_LIMITS.md`](../../HCI-CNQ/CNQ_SCOPE_AND_LIMITS.md)
- Claim-strength locked language: [`../../HCI-CNQ/CLAIM_STRENGTH_TABLE.md`](../../HCI-CNQ/CLAIM_STRENGTH_TABLE.md)
- Operations protocol (catalog maintenance): [`../../OPERATIONS_PROTOCOL.md`](../../OPERATIONS_PROTOCOL.md) §14

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
