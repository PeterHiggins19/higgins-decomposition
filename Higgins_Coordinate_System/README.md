# Higgins Coordinate System — foundational specification

This folder holds the foundational specification of the Higgins
Coordinate System as it stood at the close of its first development
cycle (April–May 2026). It is preserved here as the original
end-to-end specification the system was built on.

## Current canonical engine

The operational implementation has since matured into the
**Compositional Navigation Tensor (CNT)** engine 2.0.4 / schema 2.1.0,
which is the current canonical engine and report system.

* Engine source: [`HCI-CNT/engine/cnt.py`](../HCI-CNT/engine/cnt.py)
  (Python) and [`HCI-CNT/engine/cnt.R`](../HCI-CNT/engine/cnt.R) (R).
* Documentation: [three consolidated handbook volumes](../HCI-CNT/handbook/).
* Canonical experiment corpus: [`experiments/Hs-CNT_2026-05/`](../experiments/Hs-CNT_2026-05/) (release snapshot) or [`HCI-CNT/experiments/`](../HCI-CNT/experiments/) (live working folder).

CNT preserves every axiom and every operator named in the foundational
specification — closure, CLR, variance trajectory, matrix analysis,
transcendental squeeze, EITT, report — and additionally provides
trajectory-native operators (bearings, helmsman, period-2 attractor,
IR class), end-to-end hash-chained provenance, a four-stage paged
report family, and a 25-experiment determinism gate that passes 25/25
byte-identically.

The 12-step pipeline named in §8 of `HIGGINS_COORDINATES.md` remains
mathematically valid; users running new analyses should reach for CNT
(`HCI-CNT/`) rather than re-implementing the steps directly. The
12-step recipe is documented in this folder for historical lineage
and to make the inheritance from this foundational spec to the
current engine explicit.

## Contents

| File | Status |
|---|---|
| `HIGGINS_COORDINATES.md` | Foundational specification (650 lines, May 2026). Status banner + §8.1 successor pointer + cross-reference appendix added 2026-05-06 to point at the CNT canon. |
| `Higgins_Coordinate_System_Handbook_v4.1.docx` | Foundational handbook v4.1 (.docx). Content current as of 2026-05-02; the canonical engine since v4.1 is CNT 2.0.4 — see `HCI-CNT/handbook/` for current narrative. |
| `Higgins_Coordinate_System_Handbook_v4.2.docx` | Foundational handbook v4.2 (.docx). Latest .docx in the foundational series; CNT successor canon at `HCI-CNT/handbook/`. |
| `experiment_01_diagnostic.html` | Original interactive diagnostic page. Status banner added 2026-05-06; the current canonical interactive viewer is [`HCI-CNT/atlas/plate_time_projector.html`](../HCI-CNT/atlas/plate_time_projector.html). |

## Mapping from foundational spec to current canon

| Section in `HIGGINS_COORDINATES.md` | Current home in CNT |
|---|---|
| §2 The Generating Axiom | [Volume I Part A](../HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md) |
| §3 The Barycentre | Volume I Part B |
| §4 The Higgins Coordinate (CLR) | Volume I Part B + Part C |
| §5 The Projection Cube | Stage 1 plate at [`HCI-CNT/atlas/stage1_v4.py`](../HCI-CNT/atlas/stage1_v4.py) |
| §6 The Polar Slice | Stage 2 polar bearing rose in [`HCI-CNT/atlas/stage2_locked.py`](../HCI-CNT/atlas/stage2_locked.py) |
| §7 The Tensor Functor | Volume I Part C |
| §8 The 12-Step Pipeline | [`HCI-CNT/engine/cnt.py`](../HCI-CNT/engine/cnt.py) (single deterministic engine) |
| §8.5 EITT | Stage 4 cross-dataset EITT in [`HCI-CNT/atlas/stage4_locked.py`](../HCI-CNT/atlas/stage4_locked.py) |
| §9 Diagnostic Code System | Schema 2.1.0 in Volume I Part E + IR taxonomy in `j["depth"]["higgins_extensions"]` |

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
