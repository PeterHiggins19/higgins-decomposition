# CNQ Engine Tests

Three tests covering the determinism contract, first-principles geometry, and the dimension policy.

| Test | Contract |
|---|---|
| `test_determinism.py` | Two consecutive cnq.py runs on the same CNT JSON produce identical `cnq_content_sha256`. The strip-volatile-fields layer must remove `metadata.generated` from the hashed payload. |
| `test_first_principles.py` | A hand-constructed D=4 trajectory with known rotation reproduces the expected residuals at IEEE floor; quaternion sandwich, atan2-stable rotation, Hamilton product, conjugate, and Helmert basis primitives all behave per the pseudocode. |
| `test_dimension_policy.py` | `classify_dimension(D)` returns the correct label for D ∈ {2, 3, 4, 5, 7, 8, 9, 10}. CNQ output for each D is gated by the corresponding policy. |

Run all tests:

```
pytest HCI-CNQ/engine/tests/
```

Run a single test:

```
pytest HCI-CNQ/engine/tests/test_first_principles.py -v
```

The full test suite runs in under 5 seconds and requires no network access.
