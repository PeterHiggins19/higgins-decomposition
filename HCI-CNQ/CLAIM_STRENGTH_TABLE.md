# HCI-CNQ — Claim Strength Table

**Purpose:** lock the language used in Paper 1, the README, and downstream documents. Every CNQ-related claim falls into one of four bins. Wording outside this discipline is a defect to be fixed.

**Last revised:** push #26 (2026-05-08), per ChatGPT round-2 audit.

---

## Confirmed

These are claims supported by reproducible IEEE-floor numerical evidence on multiple unrelated datasets.

| # | Claim | Evidence |
|---|---|---|
| C1 | For D=4 compositional trajectories, the Helmert-projected Aitchison direction changes are reproduced exactly (to floating-point precision) by unit-quaternion sandwich rotations. | Backblaze fleet (730 pairs), Planck CMB (2498 pairs). Max residual 4.441e-16 in both, bit-identical. |
| C2 | The same residual ceiling appears on physically unrelated D=4 datasets, indicating the result is algebraic rather than domain-specific. | Backblaze (drive failures, T=731) ⟂ Planck (cosmological power spectrum, T=2499). |
| C3 | CNT remains canonical and unchanged. CNQ inherits from CNT via a portable adapter. | `cnq.py` carries `parent_cnt_content_sha256` from CNT JSON forward into every CNQ JSON. |
| C4 | The CNQ engine is deterministic across platforms. | Determinism contract in `engine/hashing.py`; two runs on the same CNT JSON produce identical `cnq_content_sha256`. |
| C5 | Three structural invariances (SO(D-1) simplex rotation, SU(2) handedness, M²=I time-reversal) co-occur at IEEE floor on the tested datasets. | All three measured channels in cnt.py converge at 4.441e-16 to 7.6e-17 across the three confirmation datasets. |

**Wording for confirmed claims:** assertive past or present tense.
*"D=4 trajectories are reproduced..."* / *"The residual ceiling is 4.441e-16 on..."*

---

## Candidate

These are claims that are mathematically coherent and partially supported, but the gate has not yet been met for full promotion.

| # | Claim | Promotion gate |
|---|---|---|
| K1 | "CNT measures invariance. CNQ names the algebra it lives in." | Round 3 full-corpus validation passes (INV-022) AND at least one new diagnostic is exposed that CNT alone cannot compute. |
| K2 | LIMIT_CYCLE_P2 is a universal compositional invariance signature for substantive flow-directional systems. | Round 3 + at least one fresh domain not in the current 25-experiment corpus. |
| K3 | The Hamilton-product cross-dataset comparison provides analytical capability beyond channel-wise CNT. | Working pilot demonstrating an inference CNT cannot make. |
| K4 | The spinor / vector branch diagnostic (per Volume IV) separates two known regimes. | Pilot on a known-regime dataset showing branch separation. |
| K5 | CNQ engine output `cnq_content_sha256` is reproducible across AI platforms. | Successful cross-platform reproduction by ChatGPT and/or Grok against the same CNT JSON in push #26 follow-up. |

**Wording for candidate claims:** explicit candidate framing.
*"CNQ is proposed to..."* / *"Across the tested demonstrations, the result is consistent with..."* / *"The candidate interpretation is..."*

---

## Experimental

These are claims and structures that exist in the documentation but have no validation pilot. They are kept in the open as roadmap items, not as findings.

| # | Item | Status |
|---|---|---|
| X1 | D=8 bi-quaternion factoring (INV-029) | Algebra documented in `CNQ_BIQUATERNION_FACTORING.md`. Pilot deferred. |
| X2 | HCI Dyadic Coupling Ladder (INV-028) | Order-2 → 4 → 8 tensor ladder proposed in `HCI_DYADIC_COUPLING_LADDER.md`. Pilot deferred. |
| X3 | D≥9 Clifford Cl(D-1) extension | Framing in tier-system docs. No implementation. |
| X4 | CNQ for climate-scale and very-high-D bundles | Reduced-projection diagnostic in cnq.py v1.0.0; full extension deferred. |

**Wording for experimental items:** future-tense or roadmap framing.
*"The proposed extension would..."* / *"If a pilot validates this..."* / *"Documented as a candidate Stage 4 / Stage 5 diagnostic."*

---

## Future / out of scope

| # | Item |
|---|---|
| F1 | Round 3 full 25-experiment corpus validation (INV-022). |
| F2 | cnq.R port to match cnt.py / cnt.R parity. |
| F3 | CNQ ↔ HCI-VR course-attitude integration. |
| F4 | Paper 3 — CNQ parallel verification methodology (gated on cnq.py production use across the full corpus). |

**Wording for future items:** explicitly future and gated.
*"Future work: Paper 3 will be drafted once cnq.py has produced cnq_content_sha256 across the full corpus."*

---

## Avoid / scope

The ChatGPT round-2 audit specifically flagged language that should NOT appear in any CNQ document.

| Avoid | Use instead |
|---|---|
| "universally across all substantively-flowing compositional data" | "across the tested demonstrations so far, with full-corpus validation pending" |
| "CNQ computes ..." (when referring to engine features not yet in cnq.py) | "the CNQ demonstrations compute ..." OR "the CNQ engine v1.0.0 computes ..." (depending on what is shipped) |
| "CNQ is canonical" (without scope) | "the CNQ tier documents are canonical; the engine v1.0.0 ships reproduction-grade quaternion sandwich computation" |
| "M²=I proves time-reversal symmetry" | "M²=I is one of three structural invariance pillars; the D=4 quaternion sandwich is the stronger independent test" |
| "D=3 neutrino confirms native quaternion structure" | "D=3 is consistency support, not native D=4 quaternion proof" |
| "the quaternion identification is not analogy" (unbounded) | "the D=4 quaternion identification is not analogy in the tested Helmert-projected case" |

---

## Application to Paper 1

Paper 1 (INV-026, *A Universal Compositional Invariance Signature*) draws claims exclusively from the **Confirmed** column for its load-bearing argument. **Candidate** claims appear with explicit gating language. **Experimental** items appear in the future-work section.

The wedge is the universality claim, scoped to flow-directional compositional dynamics carrying the structural preconditions. The title retains "Universal" because the result IS universal *for the class of systems that meet the conditions* — which is what the paper is claiming.
