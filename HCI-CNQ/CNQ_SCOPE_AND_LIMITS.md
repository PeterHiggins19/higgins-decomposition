# CNQ — Scope and Limits

**One-paragraph statement:** The Compositional Navigation Quaternion (CNQ) is a quaternion-native view of the same compositional dynamics CNT measures. For D=4 the view is exact and load-bearing. For other dimensions it is a projection, a boundary case, or a candidate algebraic extension. CNQ does not replace CNT; it inherits from it, declares its frame, and reports how much of the full compositional displacement it captures.

---

## What CNQ IS

- A **course-attitude capsule** for compositional trajectories: scalar (cos θ/2) + 3-vector (sin θ/2 × axis), the standard unit-quaternion structure.
- An **algebraic naming layer** for the invariances CNT already measures: SO(D-1) simplex rotation, SU(2) double-cover (handedness), M²=I metric involution (time-reversal).
- An **engine** (`cnq.py`, push #26) that reads CNT JSON, computes the quaternion-native view of the same trajectory, and emits hash-chained CNQ JSON with a deterministic `cnq_content_sha256`.
- A **reproducibility surface**. Other AI platforms, third-party reviewers, and independent labs can run the same engine against the same CNT JSON and match the cnq_content_sha256 byte-for-byte. That is a fourth independent confirmation channel beyond the three already in the corpus.

## What CNQ IS NOT

- **Not** a replacement for CNT. CNT is canonical and unchanged.
- **Not** a universal physical law. The signature is universal *for the class of systems meeting the preconditions* (positive-carrier compositional time-series with three structural invariances at the floor); it is not universal across arbitrary physical systems.
- **Not** a finished general theory. The D=4 case is load-bearing; everything else is bounded by explicit dimension labels.
- **Not** a black box. Every CNQ JSON declares its frame, its projection method, its captured energy fraction, and its dimension-policy label.

---

## Frame declaration (per ChatGPT round-2 audit requirement)

Every CNQ output records the frame in which the quaternion view is computed. CNQ v1.0.0 uses ONE frame:

| Field | Value (v1.0.0) |
|---|---|
| `frame_type` | `"Helmert orthonormal contrast (legacy QD convention)"` |
| `frame_signature` | `"row k: 1/sqrt(k(k+1)) [k blocks of +1, then -k]"` |

This matches the QD_round_2.py convention exactly so the IEEE-floor residuals reproduce bit-for-bit. Future engine versions may add ILR-Helmert principal-axis frames or named scientific balance frames; whichever frame is used will always be declared in the output.

---

## Captured energy fraction

For D > 4, the CNQ view projects the (D-1)-dimensional ILR trajectory into R^3 (first 3 axes) before computing the quaternion sandwich. The projection is lossy.

The output reports:

```
captured_step_fraction = mean_t( ||Δz_3(t)||² / ||Δz_full(t)||² )
```

For D=4 this is 1.0 by construction. For D>=5 it can be substantially less. **A CNQ user must check this field before interpreting the residual.** If `captured_step_fraction` is well below 1.0, the quaternion view is partial — CNT remains the load-bearing instrument and the CNQ reading is a projection diagnostic.

---

## Dimension policy (full table)

| D | Label | Algebra | Processing | Claim strength |
|---|---|---|---|---|
| 4 | `native_quaternion` | SU(2) cover of SO(3); Aitchison rotation in R^3 | Helmert → R^3 → unit-quaternion sandwich | **confirmed (load-bearing)** |
| 3 | `boundary_or_degenerate_support` | SO(2) in R^2; promoted to R^3 with z=0 | Helmert → R^2 → embed → sandwich | consistency support, not native proof |
| 2 | `degenerate_below_quaternion` | scalar log-ratio only | bearing computation only | quaternion view does not apply |
| 8 | `bi_quaternion_factoring_candidate` | SO(8) ⊃ SU(2) × SU(2) | Helmert → R^7; reduced view = first 3; bi-quaternion factoring scaffolded | experimental (INV-029) |
| ≥5 (not 8) | `reduced_or_projected` | SO(D-1) | Helmert → R^(D-1) → first 3 axes → sandwich (lossy) | projection diagnostic only |

---

## What CNQ adds over CNT

Per the central claim — *CNT measures invariance, CNQ names the algebra* — CNQ does not produce new termination codes or new IR classes. It exposes operations that CNT computes implicitly:

- **Sandwich product** as the explicit form of the rotation operation CNT measures via channel arithmetic. Independent verification path.
- **Hamilton products** for cross-dataset comparison. (Candidate — gate: working pilot.)
- **SLERP** for trajectory interpolation in the algebraic frame. (Candidate.)
- **Spinor / vector branch diagnostic** based on the period-2 attractor. (Candidate.)

CNT JSON outputs are already complete for the canonical analysis. CNQ adds a parallel verification channel and exposes the algebraic structure for downstream work.

---

## What CNQ explicitly does not do (in v1.0.0)

- Does not produce SLERP outputs (candidate, deferred).
- Does not implement bi-quaternion factoring (INV-029, deferred).
- Does not implement Cl(D-1) Clifford extensions (deferred).
- Does not modify CNT JSON. CNT is read-only from the CNQ side.
- Does not replace cnt.R; the R port is deferred to push #27 or later.

---

## Provenance chain

Three hashes carried forward in every CNQ run:

```
raw CSV bytes
  -> source_file_sha256
  -> CNT engine
  -> CNT JSON (with content_sha256)
  -> parent_cnt_content_sha256 (recorded in CNQ output)
  -> CNQ engine
  -> CNQ JSON (with cnq_content_sha256)
```

Any change at any stage is visible in the chain. Cross-platform reproduction is verified by hash equality on `cnq_content_sha256`.

---

## Cross-references

- Engine schema: [`engine/CNQ_SCHEMA.md`](engine/CNQ_SCHEMA.md)
- Status & maturity: [`STATUS_AND_MATURITY.md`](STATUS_AND_MATURITY.md)
- Claim strength: [`CLAIM_STRENGTH_TABLE.md`](CLAIM_STRENGTH_TABLE.md)
- Round 3 plan: [`ROUND3_VALIDATION_PLAN.md`](ROUND3_VALIDATION_PLAN.md)
- Bi-quaternion factoring (deferred): [`HCI-CNQ/CNQ_BIQUATERNION_FACTORING.md`](CNQ_BIQUATERNION_FACTORING.md)
- Dyadic coupling ladder (deferred): [`HCI-CNQ/HCI_DYADIC_COUPLING_LADDER.md`](HCI_DYADIC_COUPLING_LADDER.md)
- Investigation Catalog: [`../ai-refresh/INVESTIGATION_CATALOG.md`](../ai-refresh/INVESTIGATION_CATALOG.md)
