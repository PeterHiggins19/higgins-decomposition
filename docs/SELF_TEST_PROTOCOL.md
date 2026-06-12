# Hs Engine Self-Test Protocol — BIST Doctrine

**Doctrine ID:** STP-1.0  *(self-test protocol, version 1.0)*
**Adopted:** push #32 (2026-05-09)
**Authority:** project doctrine — applies to all HCI engines (CNT v3, CNQ v2, future versions)
**Catalog reference:** INV-046
**Source:** Peter Higgins (push #32 directive)

---

## 1. The principle

> *"A series of test input matrices that on startup runs as a diagnostics engine self-test, providing a dated receipt with the traceability engine that hash-marks the documents."*
> — Peter, push #32

Every engine in the Hs framework carries a **frozen reference corpus** and a **runner** that compares the engine's actual output against the corpus's expected output, on demand or at startup, and produces a **dated, hash-signed receipt** that extends an audit chain back to the engine's first self-test.

This is the same pattern aerospace firmware calls **Built-In Self-Test (BIST)** or **Power-On Self-Test (POST)**: the engine reports its own health every time it runs. A passed self-test is positive evidence that the deployed engine still computes what it computed at release; a failed self-test is positive evidence that something has changed (numerical drift, dependency upgrade, file corruption, deliberate sabotage) and the operator should investigate before trusting any new analytic output.

The receipt makes the engine's health **auditable in retrospect**: a deployment six months from now can produce its receipt chain back to the day of release and demonstrate that every run between then and now passed self-test.

## 2. Scope

The doctrine applies to:

- **Every shipping HCI engine**: CNT v3, CNQ v2, future versions, future engines.
- **Every applied tier instrument** that produces analytic output of consequence (HCI-AUDIO measurement instruments, HCI-ULTRASOUND instruments, etc.).

The doctrine does NOT apply to:

- One-off exploratory scripts under `experiments/` (these run against live data and have no fixed reference corpus).
- Wrapper data files (which carry their own audit pattern via the SEA anti-specification doctrine).

When in doubt, apply the doctrine. The cost of an extra self-test is small; the cost of skipping it on an instrument that ships analytic results is downstream irreproducibility.

## 3. Components per engine

Every engine that adopts the protocol carries:

```
<engine>/self_test/
    standard_test_matrices.json    Frozen reference inputs (corpus version C/k)
    expected_results.json          Locked expected outputs per test (within tolerance)
    STANDARD_TEST_MATRICES.md      Human-readable description of the corpus
    run_self_test.py               Runner: corpus -> engine -> compare -> receipt
    RECEIPTS/                      Archive (one subdir per date)
        YYYY-MM-DD/
            HHMMSS_<verdict>.json
        LATEST_RECEIPT.json        Pointer to most recent receipt
```

Every receipt conforms to `docs/self_test_receipt_schema.json` (JSON Schema, draft 2020-12).

## 4. Corpus design conventions

### 4.1 Composition of a standard test corpus

A corpus exercises the full diagnostic surface of the engine, not just one or two happy paths. For CNQ v2 the corpus includes (but is not limited to):

| Test class | Purpose | Example IDs |
|---|---|---|
| Centroid / uniform | Degenerate case where every carrier is equal — exercises closure, CLR=0, ILR=0, kappa_HS singular | `uniform_centroid_d8`, `uniform_centroid_d16` |
| Single-carrier dominance | Carrier i at high amplitude — exercises Hs scale near 1, ring class Hs-6 | `dominant_d8`, `dominant_d16` |
| Random Dirichlet | Frozen-seed random samples with known statistical properties — exercises typical-case throughput | `random_dirichlet_d8_t64`, `random_dirichlet_d16_t128` |
| Period-2 alternation | Two-state alternation — exercises attractor fit, helmsman flips, stability | `period_2_d8`, `period_2_d16` |
| Period-4 cascade | Four-state cycle — exercises chaos_indicator (period-doubling depth) | `period_4_d8` |
| Tightly coupled stereo | D=8 twin-quaternion factoring with q_A == q_B (small rho_AB) | `stereo_coupled_d8` |
| Decoupled stereo | D=8 with independent quaternion paths in the two factors | `stereo_decoupled_d8` |
| Antipodal | Anti-correlated halves | `stereo_antipodal_d8` |
| Monotonic drift | Slow trend, no period — exercises termination=EXHAUSTED | `monotonic_drift_d8` |
| Crossover misalignment | Synthetic version of the audio-wrapper worked example | `crossover_misalign_d8` |
| Pairwise coverage | One row exists for each ordered pair of carriers exhibiting a known relationship — exercises C(D,2) pairwise diagnostics | `pairwise_coverage_d8`, `pairwise_coverage_d16` |
| Edge: T=1 | Single-row degenerate trajectory | `edge_T1_d4` |
| Edge: T=2 | Minimum-pair input | `edge_T2_d4` |
| Edge: T=large | Stress test (T=1000 or larger) | `stress_T1000_d4` |

### 4.2 Reproducibility

Every matrix that uses randomness MUST declare its `generation_seed` and `generation_method` so the matrix can be regenerated bit-for-bit from the corpus document. Determinism within a language version is mandatory.

### 4.3 Versioning

The corpus carries `corpus_version` (e.g., `cnq_corpus/1.0`). Bumping the corpus is a deliberate event that requires:

1. Updating `expected_results.json` to match the new corpus.
2. Recording the corpus version bump in the engine's audit chain.
3. The first receipt under the new corpus version explicitly references the corpus_sha256.

## 5. Expected-results lock

`expected_results.json` carries the locked expected output per test. Two flavours of expectation:

- **Point value**: for deterministic outputs (e.g., `M^2 = I` involution residual at IEEE floor), the expected value is locked exactly. Comparison uses absolute tolerance e.g. `1e-13`.
- **Range value**: for outputs that depend on stochastic generation (e.g., helmsman flips count on a random-Dirichlet trajectory), the expected value is a `{min, max}` pair, and comparison checks the actual value falls within the range.

A test result is `PASS` if all its expected fields are met within their tolerances; `FAIL` if any tolerance is exceeded; `SKIP` if the test could not run (missing dependency, unsupported feature flagged in the corpus).

## 6. Receipt structure

Each self-test run produces a receipt JSON file. Required fields per `docs/self_test_receipt_schema.json`:

```json
{
  "self_test_protocol_version": "STP-1.0",
  "engine": "HCI-CNQ",
  "engine_version": "2.0.0",
  "schema_version": "cnq/2.0.0",
  "engine_content_sha256_at_test_time": "<hex>",

  "corpus_id": "cnq_corpus/1.0",
  "corpus_sha256": "<hex>",
  "expected_results_sha256": "<hex>",

  "run_timestamp": "<ISO-8601>",
  "run_environment": {
    "git_sha": "<hex>",
    "python_version": "...",
    "numpy_version": "...",
    "platform": "...",
    "hostname_hash": "<hex>"
  },

  "test_results": [
    {
      "test_id": "uniform_centroid_d8",
      "verdict": "PASS",
      "wall_clock_ms": 12,
      "checks": [
        { "field": "ir_class", "expected": "D2_DEGENERATE", "actual": "D2_DEGENERATE", "match": true },
        { "field": "involution_M_squared.max_residual_overall", "expected_max": 1e-13, "actual": 4.8e-17, "match": true }
      ],
      "warnings": []
    }
  ],

  "summary": {
    "total_tests": 14,
    "passed": 14,
    "failed": 0,
    "skipped": 0,
    "duration_ms": 1234,
    "aggregate_verdict": "ALL_PASS"
  },

  "previous_receipt_sha256": "<hex or null>",
  "receipt_sha256": "<hex>"
}
```

The `receipt_sha256` is computed *last*, on the canonical-JSON serialisation of the receipt with the `receipt_sha256` field omitted (or zeroed). This makes the receipt self-verifying: anyone can recompute the hash from the receipt body and confirm it has not been tampered with.

The `previous_receipt_sha256` field is `null` for the very first receipt and the hex digest of the immediately preceding receipt for every subsequent one. The chain forms a Merkle-style audit log: any inserted, deleted, or modified receipt breaks the chain.

## 7. Aggregate verdicts

| Verdict | Meaning |
|---|---|
| `ALL_PASS` | Every test in the corpus passed. The engine is healthy. |
| `SOME_FAILED` | At least one test failed. Investigate before trusting analytic output. |
| `SOME_SKIPPED` | Some tests were not run; remaining tests passed. Acceptable for partial deployments (e.g., R port without quad-quaternion). |
| `INFRASTRUCTURE_FAIL` | The runner itself crashed before completing all tests. The receipt records what was attempted. |

A deployment in production should refuse to start if the most recent receipt is anything other than `ALL_PASS` or `SOME_SKIPPED` (with the operator's explicit acknowledgement of which tests were skipped and why).

## 8. When self-tests run

Three triggers:

1. **Startup**: when the engine is first invoked in a process (lazy-cache the result for the rest of that process's lifetime).
2. **On demand**: explicit CLI invocation (`cnq --self-test`) or programmatic call (`cnq.self_test()`).
3. **Scheduled**: periodic (daily / weekly) via the `schedule` skill or external cron, useful for long-running deployments where the engine itself doesn't restart often.

Every trigger produces a receipt; the archive accumulates.

## 9. Receipt archive policy

- Receipts are written to `<engine>/self_test/RECEIPTS/YYYY-MM-DD/HHMMSS_<verdict>.json`.
- A separate `<engine>/self_test/RECEIPTS/LATEST_RECEIPT.json` is updated to point at the most recent receipt (file copy, not symlink, for filesystem portability).
- Receipts are never deleted from the archive. Disk-pressure operators may compress old receipts (e.g., `gzip` per-month) but the chain must remain reconstructable.
- Each engine release (tag bump) starts a fresh chain — `previous_receipt_sha256` of the first receipt under a new release is the last receipt of the previous release, providing cross-release continuity.

## 10. Verifying a receipt

Anyone can verify a receipt without re-running the engine:

1. Read the receipt JSON.
2. Compute SHA-256 of the canonical-JSON serialisation of the receipt with `receipt_sha256` omitted.
3. Compare against the stored `receipt_sha256`. Match = receipt has not been tampered with.
4. Recompute the canonical-JSON SHA-256 of the corpus file and compare against `corpus_sha256` in the receipt. Match = corpus has not changed since the receipt was issued.
5. Walk the chain: read the receipt at `previous_receipt_sha256`, repeat the process. Termination = first receipt of the engine's deployment history.

A `verify_receipt.py` companion script automates the walk and reports any chain breaks.

## 11. Integration with existing doctrines

This doctrine is additive to and compatible with:

- **OPERATIONS_PROTOCOL.md** — the Gawande meta-checklist gets a "self-test passed" item in the engine-release transition checklist.
- **SUSPICION_OF_EVERY_ASSUMPTION.md** (SEA) — the self-test corpus is one source of failure-mode evidence (TEST type) for the engine's anti-specification.
- **The priority lock** — basic-first ordering. Self-test is part of "basics complete," not after.
- **The engine-independence policy** — each engine's receipts are independent of others'; no cross-engine receipt chains.
- **The wrapper architecture** — wrappers do not have self-tests in this doctrine version; wrapper validity is checked via the SEA anti-specification at wrapper authoring time.

## 12. The principle, recapitulated

> *"On startup runs as a diagnostics engine self-test, providing a dated receipt with the traceability engine that hash-marks the documents."*
> — Peter, push #32

Every engine that ships in the Hs framework carries its own audit trail. The trail begins on the day of release and extends one receipt per run to the present. A breakage of the chain is detectable without external auditors. A passed run six months ago, six months from now, is reproducible from the receipt — the engine's own honesty about what it computed.

---

**Status:** doctrine adopted push #32. First instances: CNQ v2 self-test corpus (delivered Phase C2), CNT v3 self-test corpus (delivered Phase C1).

**See also:**
- `docs/self_test_receipt_schema.json` — JSON Schema for receipt files
- `<engine>/self_test/STANDARD_TEST_MATRICES.md` — per-engine corpus documentation
- `docs/SUSPICION_OF_EVERY_ASSUMPTION.md` — companion doctrine for failure-mode enumeration
- `OPERATIONS_PROTOCOL.md` — release-transition integration
- `ai-refresh/INVESTIGATION_CATALOG.json` — INV-046 records this doctrine adoption
