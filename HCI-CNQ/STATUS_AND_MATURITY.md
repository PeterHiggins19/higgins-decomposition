# HCI-CNQ — Status and Maturity

**Last updated:** push #26 (2026-05-08)
**Status model:** four-field (see [`HCI-CNQ_ADMIN.json -> status`](HCI-CNQ_ADMIN.json) for the machine-readable form).

---

## Four-field status

| Field | Value |
|---|---|
| `current_repo_status` | **canonical_public_tier** (since push #23) |
| `engine_status` | **cnq.py shipped** (push #26) — full Hamilton-product engine; cross-platform reproduction challenge open |
| `validation_status` | **three IEEE-floor confirmations** (Backblaze D=4, Planck CMB D=4, SM neutrino D=3 boundary support); Round 3 full-corpus validation pending (INV-022) |
| `archive_status` | historical candidate state preserved verbatim in [`ARCHIVE_README.json`](ARCHIVE_README.json) |

---

## Maturity ladder

Per the ChatGPT round-2 audit (push #26), each component of the CNQ tier is tagged with one of four maturity labels.

### CONFIRMED

| Item | Evidence |
|---|---|
| **D=4 Aitchison ↔ unit-quaternion sandwich product** | Backblaze fleet: 730 pairs, max residual 4.441e-16 at IEEE floor. |
| **D=4 quaternion reconstruction reproduces across unrelated datasets** | Planck CMB: 2498 pairs, max residual 4.441e-16. Bit-identical to Backblaze. |
| **CNT measures invariance** | Three structural invariances (SO(D-1), SU(2) handedness, M²=I) all confirmed at IEEE floor. |
| **CNT remains canonical** | cnt.py is unchanged. CNQ inherits, does not replace. |
| **cnq.py engine determinism** | Two runs on the same CNT JSON produce identical cnq_content_sha256 (push #26). |

### CANDIDATE

| Item | Promotion gate |
|---|---|
| **CNT measures invariance; CNQ names the algebra** (central tagline) | Round 3 full-corpus validation (INV-022). |
| **LIMIT_CYCLE_P2 as universal compositional invariance signature** | Round 3 corpus, plus at least one new domain. |
| **Spinor / vector branch diagnostic** | Working pilot showing the diagnostic separates two known regimes. |
| **Hamilton-product cross-dataset comparison** | Pilot demonstrating an analysis CNT alone cannot perform. |
| **SLERP interpolation layer** | Pilot demonstrating value-add over linear interpolation in CLR space. |

### EXPERIMENTAL

| Item | Status |
|---|---|
| **D=8 bi-quaternion factoring (INV-029)** | Algebra documented; pilot pending (EMBER country trajectory candidate). |
| **D≥9 Clifford extension** | Not implemented; Cl(D-1) framing in tier_system docs. |
| **HCI Dyadic Coupling Ladder (INV-028)** | Order-2 → 4 → 8 ladder proposed; pilot pending. |
| **CNQ for climate-scale and high-D bundles** | Reduced-projection view in cnq.py v1.0.0; full extension deferred. |

### FUTURE

| Item | Notes |
|---|---|
| **Round 3 full 25-experiment corpus validation** | INV-022. ~1 day of compute. Promotion gate for several CANDIDATE items. |
| **cnq.R parity** | R port to match cnt.py / cnt.R parity discipline. Not in push #26. |
| **CNQ ↔ HCI-VR course-attitude integration** | Cross-tier integration pending HCI-VR pilot. |
| **Paper 3 — CNQ parallel verification methodology** | Gated on cnq.py production use across the corpus. |

---

## Dimension policy

CNQ does not pretend to be the natural algebra at every dimension. The dimension label is part of every CNQ JSON output.

| D | Label | Claim strength |
|---|---|---|
| 4 | `native_quaternion` | **confirmed** (load-bearing case) |
| 3 | `boundary_or_degenerate_support` | consistency support, not native proof |
| 2 | `degenerate_below_quaternion` | bearing only; quaternion view does not apply |
| 8 | `bi_quaternion_factoring_candidate` | experimental (INV-029) |
| ≥5 (not 8) | `reduced_or_projected` | projection diagnostic only |

The Standard-Model neutrino result (D=3) is a CONSISTENCY CHANNEL, not native quaternion proof. Backblaze and Planck (both D=4) are the load-bearing cases.

---

## What CNQ is NOT claiming

Per ChatGPT round-2 audit, the following claims are explicitly out of scope:

- CNQ is not "universal across all compositional data."
- CNQ is not a replacement for CNT.
- M²=I is not "proof of physical time-reversal symmetry" — it is one of three structural invariance pillars; the D=4 quaternion sandwich is the stronger independent test.
- The D=3 neutrino result is not native D=4 quaternion proof — it is consistency support.
- D=8 bi-quaternion factoring is not yet validated; it is a documented candidate extension.

---

## How items move through the ladder

Promotion always follows the framework's demonstration-first discipline (per [`OPERATIONS_PROTOCOL.md`](../OPERATIONS_PROTOCOL.md) and the [`Investigation Catalog`](../ai-refresh/INVESTIGATION_CATALOG.md)):

```
EXPERIMENTAL  -- pilot succeeds -->  CANDIDATE
CANDIDATE     -- gate criteria met --> CONFIRMED
CANDIDATE     -- gate criteria fail --> FALSIFIED (kept on record)
```

Falsifications stay on record. The QD R2.5 Concept 4 falsification (P2 ≠ fermion-vs-boson distinguisher) is the canonical example — the audit trail makes the cleaner reformulation credible.
