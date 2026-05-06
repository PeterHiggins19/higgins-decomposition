# Atlas — the four-stage paged report system

The HCI-Atlas is the report family produced from any conformant CNT JSON.
Four stages, each tagged by derivational order (see Volume I §G doctrine).

| Module | Order | Output |
|---|---|---|
| [`stage1_v4.py`](stage1_v4.py) | Order 1 | Per-timestep ILR-Helmert orthogonal triplet plate (T plates per dataset) |
| [`atlas_stage1_complete.py`](atlas_stage1_complete.py) | Order 1 | Stage 1 driver: T plates + 1 trajectory-summary plate |
| [`stage1_summary.py`](stage1_summary.py) | Order 1.5→2 | Closing summary plate (folded into Stage 2 by doctrine v1.0.1) |
| [`stage2_locked.py`](stage2_locked.py) | Order 2 | 28-plate single report combining classical CoDa + CNT trajectory plates |
| [`stage2.R`](stage2.R) | Order 2 | R metric port (parity with the Python Stage 2) |
| [`stage3_locked.py`](stage3_locked.py) | Order 3 | 11-plate single report — depth tower / IR / period-2 attractor |
| [`stage4_locked.py`](stage4_locked.py) | Order 4+ | 11-plate group-level cross-dataset inference report |
| [`spectrum_paper.py`](spectrum_paper.py) | Order 2 (group) | Paper PDF: cross-dataset spectrum with FIXED scales |
| [`plate_time_projector.html`](plate_time_projector.html) | Order 1+2 (interactive) | 3D HTML viewer; barycenter z-spine; valid-known connections only |
| [`det_pdf.py`](det_pdf.py) | (utility) | v1.1-A deterministic PDF metadata helper |
| [`alias_map.py`](alias_map.py) | (utility) | Carrier alias-mapping for plate display |
| [`compare.py`](compare.py) | (utility) | Run-vs-run delta tool |
| [`standard_calibration.py`](standard_calibration.py) | (utility) | Stage 1 27-point HLR-grid fixture builder |
| [`standard_calibration_stage2.py`](standard_calibration_stage2.py) | (utility) | Stage 2 straight / loop calibration fixtures |
| `STANDARD_CALIBRATION_27pt_*` | (fixture) | Stage 1 ground-truth grid (drift O(1e-10)) |
| `STANDARD_CALIBRATION_stage2_*` | (fixture) | Stage 2 directness=1.0 (straight) / 0.0 (loop) at IEEE floor |

## Reading order

For a single dataset:
1. Stage 1 — per-timestep first-principles plate book (one PDF per dataset).
2. Stage 2 — single 28-plate report combining geometry plates (CoDa-standard:
   variation matrix, biplot, balance dendrogram, SBP, ternary, scree) with
   dynamics plates (course plot, polar rose, bearing heatmap, ω, helmsman,
   ring strip, locks, CBS three orthogonal faces, divergence ranking).
3. Stage 3 — depth tower / period-2 attractor / IR class single report.

For a project (multiple datasets):
4. Stage 4 — cross-dataset inference report (one per project).
5. Spectrum paper — cross-dataset spectrum with FIXED scales.
6. Projector HTML — interactive 3D viewer.

## Doctrine

Every plate is tagged with its derivational order. Mixing orders within
one plate is forbidden by design. See
[`../handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md`](../handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md)
Part G for the doctrine reference and Part H for Stage 2 pseudocode.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
