# HCI/calibration — calibration data and results

Calibration measurements and results from the foundational Higgins
Coordinate System pipeline.

## Status

The current canonical calibration fixtures live in the CNT subsystem at:

* `HCI-CNT/atlas/STANDARD_CALIBRATION_27pt_*` — Stage 1 27-point HLR-grid fixture (drift O(1e-10))
* `HCI-CNT/atlas/STANDARD_CALIBRATION_stage2_A_straight_*` — Stage 2 straight-line trajectory: directness = 1.0 exactly
* `HCI-CNT/atlas/STANDARD_CALIBRATION_stage2_B_loop_*` — Stage 2 closed-loop trajectory: directness = 0.0 exactly

These are mathematically-known-answer fixtures verified at IEEE floor
precision. See
[`../../HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md`](../../HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md)
Part G for the doctrine reference.

The calibration material here is preserved for lineage.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
