# Round 3 — Full-Corpus Quaternion-View Validation Plan

**Investigation:** INV-022 (Round 3 — full-corpus quaternion-view validation)
**Status:** OPEN, ~1 day of compute
**Owner:** Peter (final approval); Claude (execution)
**Promotion gate for:** several CANDIDATE-tier claims in [`CLAIM_STRENGTH_TABLE.md`](CLAIM_STRENGTH_TABLE.md), and for the strongest version of Paper 1's universality claim.

---

## Goal

Run the CNQ engine v1.0.0 against every experiment in the existing 25-experiment CNT corpus (the `Hs/HCI-CNT/experiments/` tree). Record per-experiment:

- `cnq_content_sha256`
- max residual + gate pass/fail
- dimension label (one of: `native_quaternion`, `boundary_or_degenerate_support`, `degenerate_below_quaternion`, `bi_quaternion_factoring_candidate`, `reduced_or_projected`)
- captured step fraction (for D > 4)
- parent CNT termination + IR class (carried forward)

Produce a side-by-side report so any reader can see at a glance which experiments pass at IEEE floor, which sit in boundary territory, and which require the projection caveat.

---

## Why this matters

Three confirmed datasets (Backblaze, Planck, SM neutrino) give the framework strong priority on the quaternion identification. Round 3 strengthens the publication wedge from 3 datasets to up to 25 — and, equally importantly, surfaces the failure modes (if any) so the dimension policy is calibrated against the full corpus rather than the three load-bearing cases.

Per the framework's demonstration-first discipline (per [`OPERATIONS_PROTOCOL.md`](../OPERATIONS_PROTOCOL.md)): a corpus run is the strongest available promotion path for the central claim.

---

## Method

For every experiment in `HCI-CNT/experiments/INDEX.json`:

1. Locate the experiment's CNT JSON (already produced and hash-stamped).
2. Run `cnq.py --cnt-json <path> --out <path>` against it.
3. Record the CNQ output values into a row of the Round 3 results table.
4. If the experiment requires the raw CSV (older CNT JSONs may not include input rows), supply it via `--input-csv`.
5. If the experiment fails any expected condition (gate fail when D=4 was expected, dimension policy mismatch, or hash drift on re-run), flag for investigation.

The orchestration is a single script:

```
HCI-CNQ/scripts/run_round3_corpus.py --repo-root .
```

(To be added in the Round 3 push, separate from #26.)

---

## Outputs

Three artefacts written to `HCI-CNQ/results/`:

| File | Contents |
|---|---|
| `round3_corpus_results.json` | Machine-readable per-experiment CNQ summary. |
| `round3_corpus_summary.md` | Plain-text reader-friendly table. |
| `round3_failures_to_investigate.csv` | Subset of experiments that did not pass their expected dimension policy or gate. |

---

## Promotion rule

Per [`CLAIM_STRENGTH_TABLE.md`](CLAIM_STRENGTH_TABLE.md):

- A CANDIDATE claim graduates to **CONFIRMED** when its corresponding gate is met. Round 3 is the gate for the central tagline (K1) and the universal-signature interpretation (K2).
- A claim that fails at Round 3 graduates to **FALSIFIED** with full audit record. The QD R2.5 falsification (P2 ≠ fermion-vs-boson distinguisher) is the canonical example of how a falsification is preserved and how the cleaner reformulation survives.
- Failures inside the dimension policy (e.g. a D=4 experiment that does not pass gate) must be diagnosed before any CONFIRMED-tier conclusion is published.

---

## Execution order

1. Land push #26 (this push) with cnq.py shipped.
2. Verify cnq.py produces matching residuals on the three confirmation experiments via `verify_publication_results.py`.
3. **(separate push #27)** Add `run_round3_corpus.py` and execute against the full 25-experiment corpus.
4. Write `round3_corpus_summary.md` and update [`STATUS_AND_MATURITY.md`](STATUS_AND_MATURITY.md) per actual results.
5. Update [`CLAIM_STRENGTH_TABLE.md`](CLAIM_STRENGTH_TABLE.md) — promote, demote, or falsify per outcome.
6. Update [Paper 1 draft](../papers/in_progress/PAPER_1_UNIVERSAL_INVARIANCE_DRAFT.md) with Round 3 results before arXiv submission.

---

## Effort estimate

- Compute: ~1 day to walk the corpus on a local machine.
- Reporting: ~half a day to write `round3_corpus_summary.md` and update CLAIM_STRENGTH_TABLE.
- Total: ~1.5 days to push #27 hand-off.

---

## Cross-references

- Investigation Catalog entry: [`../ai-refresh/INVESTIGATION_CATALOG.md`](../ai-refresh/INVESTIGATION_CATALOG.md) → INV-022.
- Engine: [`engine/cnq.py`](engine/cnq.py)
- Expected results lock-file: [`results/expected_results.json`](results/expected_results.json)
- Verifier: [`scripts/verify_publication_results.py`](scripts/verify_publication_results.py)
