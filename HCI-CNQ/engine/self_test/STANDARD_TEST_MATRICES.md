# CNQ Standard Test Matrices

**Corpus ID:** `cnq_corpus/1.0`
**Engine target:** CNQ v2.0.0 (`cnq/2.0.0`)
**Doctrine:** STP-1.0 (`docs/SELF_TEST_PROTOCOL.md`)
**Frozen at:** 2026-05-09

---

## Overview

This is the frozen reference corpus that the CNQ v2 self-test runner uses to verify engine health on every startup or on-demand invocation. Each test exercises a specific portion of the engine's diagnostic surface; together they cover the full feature set documented in the design doc.

The corpus is a single JSON file (`standard_test_matrices.json`) so it is language-portable: Python and R runners read the same corpus and compare against the same expected results, providing per-field cross-language parity verification as a side benefit.

## Test corpus content

| ID | n_carriers | n_records | Generator | Diagnostic focus |
|---|---|---|---|---|
| `uniform_centroid_d8` | 8 | 20 | uniform | Closure / CLR / ILR at the simplex centroid; degenerate-case schema |
| `dominant_d8` | 8 | 20 | single_dominant | High Higgins scale (Hs-6); helmsman attribution stability |
| `period_2_d8` | 8 | 50 | period_2_alternation | Attractor fit (period=2, stability>0.9); helmsman chaos_indicator depth 1 |
| `random_dirichlet_d8_t64` | 8 | 64 | dirichlet (seed=42) | Typical-case throughput; statistical robustness |
| `stereo_coupled_d8` | 8 | 50 | stereo_coupled (seed=7) | Twin-quaternion factoring with small rho_AB; high CHSH S-value |
| `stereo_decoupled_d8` | 8 | 50 | stereo_decoupled (seeds 11, 23) | Twin-quaternion factoring with large rho_AB; low CHSH S-value |
| `monotonic_drift_d8` | 8 | 30 | monotonic_drift | Termination=EXHAUSTED; attractor unfit; helmsman flips low |
| `pairwise_coverage_d8` | 8 | 56 | pairwise_coverage (seed=99) | All C(8,2)=28 pair diagnostics in stage2.carrier_pair_examination |
| `uniform_centroid_d16` | 16 | 20 | uniform | D=16 schema-locked path; quad-quaternion factoring scaffold |
| `random_dirichlet_d16_t128` | 16 | 128 | dirichlet (seed=314) | D=16 typical case; 15-dim ILR stress |
| `edge_T1_d4` | 4 | 1 | inline rows | T=1 graceful-degenerate path |
| `edge_T2_d4` | 4 | 2 | inline rows | Minimum-pair trajectory; one sandwich pair |
| `edge_D2_T20` | 2 | 20 | monotonic_drift | D=2 bearing-only path |

13 tests total. The corpus version bumps to `cnq_corpus/2.0` when this set changes (additions, removals, generation-method changes); within version 1.0 the test set is frozen.

## Generator methods

The corpus JSON uses these declarative generators so each matrix is reproducible from its parameters alone:

| `method` | Parameters | Output |
|---|---|---|
| `uniform` | `value_per_carrier: float` | All rows = constant vector of that value |
| `single_dominant` | `dominant_index: int, dominant_value: float, background_value: float` | All rows have one carrier at dominant_value, rest at background_value |
| `period_2_alternation` | `state_a: [float], state_b: [float]` | Alternates rows between state_a and state_b |
| `dirichlet` | `alpha: float, seed: int` | Random Dirichlet samples with given concentration and seed |
| `stereo_coupled` | `seed: int, coupling_strength: float in [0,1]` | Two halves driven by shared rotation with given coupling fraction |
| `stereo_decoupled` | `seed_A: int, seed_B: int` | Two halves with independent random rotations |
| `monotonic_drift` | `growth_carrier: int, decay_carrier: int, growth_rate: float` | Carriers drift linearly with given rate |
| `pairwise_coverage` | `seed: int` | Designed so each (i, j) pair exhibits a deterministic correlation pattern |

A test matrix may alternatively carry an inline `rows_provided` array (preferred for very small T tests where embedding the rows is more readable than declaring a generator).

## Expected-results lock

`expected_results.json` (sibling file) carries the locked expected outputs per test. Each entry is a list of checks, where each check is one of:

- `point_value`: exact match required, e.g. `attractor.fitted == true`.
- `range`: actual must fall in `[expected_min, expected_max]`, e.g. `helmsman.flips.total ∈ [10, 30]` for the random Dirichlet case.
- `tolerance_abs`: numerical match within absolute tolerance, e.g. `involution_M_squared.max_residual < 1e-13`.
- `tolerance_rel`: numerical match within relative tolerance, e.g. `attractor.amplitude_A within 5% of expected`.
- `presence`: field must exist (no value comparison), useful for schema completeness checks.

Tests that use generators with seeds are reproducibly deterministic, so their expected values can be locked exactly. Tests with no randomness are even more so.

## Runner usage

From the repository root:

```bash
python HCI-CNQ/engine/self_test/run_self_test.py
```

or programmatically:

```python
from HCI_CNQ.engine.self_test import run_self_test
verdict = run_self_test.run()  # returns 0 on ALL_PASS, non-zero otherwise
```

The runner writes a receipt to `RECEIPTS/YYYY-MM-DD/HHMMSS_<verdict>.json` and updates `RECEIPTS/LATEST_RECEIPT.json`. It never modifies the corpus or the expected results.

## Verifying a receipt without re-running

```bash
python docs/scripts/verify_receipt.py HCI-CNQ/engine/self_test/RECEIPTS/LATEST_RECEIPT.json
```

(verify_receipt.py utility ships in a follow-up push.)

## Corpus governance

- The corpus version is `cnq_corpus/1.0`.
- Bumping requires:
  1. Recomputing all expected_results entries.
  2. Recording the bump in the engine release notes.
  3. The first receipt under the new corpus version explicitly records both old and new corpus_sha256 to provide chain continuity.
- Adding a new test (e.g., a new edge case discovered in production) is a corpus-version bump.
- Modifying an existing test's generation is a corpus-version bump.
- Adding a new check to `expected_results.json` for an existing test is NOT a corpus version bump (it is an expected-results bump only).

## Cross-language parity

Both the Python runner (`run_self_test.py`) and the R runner (`run_self_test.R`, ships with cnq.R) consume the same corpus JSON and produce receipts in the same schema. A cross-language parity test passes when:

- The Python receipt and the R receipt for the same corpus + same engine version produce the same per-field actual values within tolerance.
- The two receipts may have different `engine_content_sha256` (Python vs R source files) but identical `corpus_sha256` and `expected_results_sha256`.
