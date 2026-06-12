# 04_calibration — Stage 1 / Stage 2 ground truth

The 27-point synthetic calibration set used to anchor Stage 1 and Stage 2
output. These are closed-form references with known analytical answers for
each CNT channel — the engine must reproduce them within numerical tolerance
on every release.

## Contents

```
04_calibration/
├── calibration_27pt_input.csv         the synthetic 27-point set
├── calibration_27pt_cnt.json          canonical CNT JSON
├── stage1_calibration.pdf             Stage 1 page rendered against ground truth
├── stage2_calibration.pdf             Stage 2 page rendered against ground truth
└── ground_truth_*.{csv,json}          analytical reference values
```

These files exist so a reviewer can verify the engine themselves: run
`python ../../../engine/cnt.py calibration_27pt_input.csv` and diff against
`calibration_27pt_cnt.json` — they must match exactly.

## See also

- `../README.md` — full demo-package overview
- `../../../engine/tests/` — full determinism + parity test suite
- `../../../handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md` — the determinism gate
