# Reproducibility Checklist — Higgins Decomposition (Hs)

**Audience:** any reviewer, AI assistant, or collaborator who wants to verify the framework's reproducibility claims without becoming our internal historian.
**Time to complete:** 15–30 minutes for the five-step path; longer if you want to rerun the full corpus.
**Status as of push #40:** all five steps pass on the canonical platform (Linux x86_64 / Python 3.10 / numpy / R 4.0+ / jsonlite / digest).

---

## The five-step verification path

### Step 1 — Verify the engines exist at the named versions

| Engine | Path | Expected version | Schema |
|---|---|---|---|
| CNT (Python) | `HCI-CNT/engine/cnt.py` | `ENGINE_VERSION = "3.1.0"` | `SCHEMA_VERSION = "3.1.0"` |
| CNT (R) | `HCI-CNT/engine/cnt.R` | `3.0.0` (v3.1.0 parity queued EngPromo-2) | `3.0.0` |
| CNQ (Python) | `HCI-CNQ/engine/cnq.py` | `2.0.0` | `cnq/2.0.0` |
| CNQ (R) | `HCI-CNQ/engine/cnq.R` | `2.0.0` | `cnq/2.0.0` |

```bash
grep -E '(ENGINE_VERSION|SCHEMA_VERSION)' HCI-CNT/engine/cnt.py HCI-CNQ/engine/cnq.py
```

**Pass condition:** engine and schema strings match the table above.

---

### Step 2 — Verify the four doctrines are codified

The framework is governed by four binding doctrines as of push #33. Each has a canonical document.

| Doctrine | Document | Catalog entry |
|---|---|---|
| SEA-1.0 (Suspicion of Every Assumption) | `docs/SUSPICION_OF_EVERY_ASSUMPTION.md` | INV-045 |
| STP-1.0 (Self-Test Protocol / BIST) | `docs/SELF_TEST_PROTOCOL.md` | INV-046 |
| CRD-1.0 (Coherent Range Doctrine) | `docs/COHERENT_RANGE_DOCTRINE.md` | INV-047 |
| Engine independence | `ai-refresh/CNT_V3_CNQ_V2_DESIGN.md` | INV-038 |

**Pass condition:** all four documents exist; each is the binding reference for its doctrine; the policy index in `Hs/README.md` lists all four.

---

### Step 3 — Run the BIST self-test (STP-1.0)

The Self-Test Protocol produces hash-chained receipts under `HCI-CNQ/engine/self_test/RECEIPTS/`.

```bash
python HCI-CNQ/engine/run_self_test.py --repo-root .
```

**Pass condition:** receipt JSON written; `gate_pass: true`; `cnq_content_sha256` hash chain links to the previous receipt (or marks itself as initial). Standard test matrices are at `HCI-CNQ/engine/standard_test_matrices.json`.

---

### Step 4 — Run the 43-test CNQ suite

```bash
pytest HCI-CNQ/engine/tests/ -v
```

**Pass condition:** 43/43 tests pass. Breakdown:

- `test_first_principles.py` — 15 tests (geometry, quaternion algebra, atan2 rotation)
- `test_dimension_policy.py` — 19 tests (D=2,3,4,5,7,8,9,10 labels and behaviour)
- `test_determinism.py` — 9 tests (canonical-JSON, hashing, end-to-end Planck CMB)

---

### Step 5 — Reproduce the three IEEE-floor confirmations

The three load-bearing demonstrations from `HCI-CNQ/experiments/`:

| Demonstration | D | T | Expected `max_residual` | Expected `cnt_content_sha256` (head) |
|---|---|---|---|---|
| Backblaze fleet drive failures | 4 | 731 | `4.440892098500626e-16` | — |
| Planck 2018 CMB power spectrum | 4 | 2499 | `4.440892098500626e-16` | `3de7d4007866dc11...` |
| SM 3-flavour ν_μ oscillation | 3 | 1000 | `3.3306690738754696e-16` | `60d733d2219fbe3c...` |

One-command reproduction:

```bash
python HCI-CNQ/scripts/run_all_confirmations.py --repo-root .
python HCI-CNQ/scripts/verify_publication_results.py --repo-root .
```

**Pass condition:** all three `gate_pass: true`; max residuals at IEEE floor (≤ 1e-12 gate threshold); deterministic hash chain holds (`cnt_content_sha256` matches the locked values for Planck and neutrino).

Reference values are locked at `HCI-CNQ/results/expected_results.json`.

---

## Beyond the five-step path — corpus-scale reproduction

If you want to go further:

- **Full corpus (101 datasets / 11 domains)** — `experiments/2026-05-10_full-corpus-validation/` carries the citation-grade reference suite (push #34). The runner is `run_full_corpus.py`; the manifest is `MANIFEST.json`; the cross-domain digest is `MASTER_FINDINGS.md`.
- **CoDaWork 2026 conference corpus (9 EMBER countries, 2001–2025)** — `papers/codawork2026/conference_2026_06/per_country/ember_*/cnt_v3.json`. Each per-country JSON carries the navigation_concentration_family + helmsman + attractor fit + IR classification.
- **Cross-language parity** — `HCI-CNT/engine/cnt.R` and `HCI-CNQ/engine/cnq.R` are per-field parity ports of the Python engines, tolerant to 1e-13 absolute / 1e-12 relative per the engine-independence policy.

---

## What "passing" means at each step

| Step | If it passes | If it fails |
|---|---|---|
| 1 | Engines exist at canonical versions | The repo state on disk does not match the documentation — file a GitHub issue with the observed versions |
| 2 | All four binding doctrines are present and indexed | Doctrine drift — likely a stale checkout; pull main |
| 3 | BIST receipt written + hash-chained | Environment issue (Python version, numpy version, locale); compare against `HS_FAST_REFRESH.json` reference platform |
| 4 | 43/43 tests green | Test regression — file an issue with the failing test name and platform |
| 5 | Three IEEE-floor confirmations reproduce | Numerical reproduction failure — open a cross-platform reproduction issue (this is one of the project's named goals, not a bug-in-disguise) |

The framework's commitment is **same input, same output, always.** Any failure of that contract at any step is worth reporting; the project will treat it as data, not as an embarrassment.

---

## What this checklist does NOT cover

- **CoDaWork 2026 talk material** — that lives in `papers/codawork2026/planning/` and is reviewed separately per `EXTERNAL_REVIEW_INVITE.md`. The two named findings (INV-050 metric-invariance + INV-051 5-of-9-country deceptive drift), the sharpened MC-4 claim, the three open questions for the community, and the 10-beat slide structure are conference-talk concerns; this checklist is engine-reproducibility concerns.
- **Cross-language byte-level hash equality** — Python and R parity is per-field at 1e-13 tolerance (engine-independence policy). Byte-identical hashes across Python and R are not required.
- **Cross-platform byte-level hash equality** — different Linux distributions, macOS, and Windows may produce different floating-point ordering and therefore different content hashes. The cross-platform reproduction challenge in `HS_FAST_REFRESH.json` invites the community to report this.

---

## Pointers for further depth

- `HS_FAST_REFRESH.json` — canonical names, numbers, formulas, engine pointers (load first if you are an AI assistant)
- `PUBLICATION_READY.md` — single entry point for the world
- `OPERATIONS_PROTOCOL.md` — Gawande-style checklists at every transition point
- `EXPERIMENTS_JOURNAL.md` — citation-grade record of every experiment ever run
- `ai-refresh/INVESTIGATION_CATALOG.json` — every speculative branch / hypothesis classified by disposition
- `ai-refresh/CCTT_RUNBOOK.md` — protocol for any AI assistant to build a CNT-grade analysis pipeline on a new dataset

---

*This checklist retires the day a reviewer can verify the framework's reproducibility in five steps with no surprises. It is intentionally short; depth lives elsewhere.*
