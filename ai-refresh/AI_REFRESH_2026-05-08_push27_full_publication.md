# Push #27 — full publication, multi-language engines, AI loader

**Date:** 2026-05-08
**Push:** #27 (after #26 "HCI-CNQ updates" landed green via Validate Repository)
**Type:** publication-grade landing — engines in all languages, single-file AI loader, public-use declaration retiring all legacy guards
**Catalog references:** INV-026 (Paper 1), INV-022 (Round 3), INV-028, INV-029

---

## Why this push

Peter's directive after push #26 landed: *"ensure the full cnq and cnt full python and r and pseudocode engines in all languages are now updated and prepared for full push to hs repo with all components and adapters and support systems all updated and included in hs repo for full use by public and ai assistance. make the entire system available, we have tested this to a level of trust few ever reach and now is the time and place to make the big splash, publish all and make it logical and useful."*

Push #27 is the big-splash publication landing.

## What this push ships

### 1. CNQ R port (parity contract with cnq.py)

`HCI-CNQ/engine/cnq.R` — full R implementation of the CNQ engine. Uses `jsonlite` + `digest` only. Same Helmert basis convention, same atan2-stable rotation, same sandwich product, same canonical-JSON serialisation, same SHA-256 contract. Two implementations, one algorithm, identical hashes on identical input.

### 2. CNQ language-agnostic pseudocode

`HCI-CNQ/engine/CNQ_PSEUDOCODE.md` — the canonical algorithm reference. 10 sections: inputs, top-level flow, geometry primitives, dimension policy, CNQ view computation, output assembly, determinism contract, CLI surface, cross-platform conformance test, recommended tests for any port. Both cnq.py and cnq.R are faithful translations of this document. Any future port (Julia, Rust, JS, C++) implements the pseudocode and must reproduce the same `cnq_content_sha256`.

### 3. CNQ test suite — 43 tests, all green

`HCI-CNQ/engine/tests/`:

| Module | Tests | Contract |
|---|---|---|
| `test_first_principles.py` | 15 | Geometry primitives (closure, CLR, Helmert basis), quaternion algebra (axis-angle, conjugate, Hamilton product, sandwich rotate), atan2-stable rotation between unit vectors, end-to-end IEEE-floor sanity |
| `test_dimension_policy.py` | 19 | classify_dimension(D) returns correct label for D ∈ {2, 3, 4, 5, 6, 7, 8, 9, 10}; run_cnq_view respects each policy |
| `test_determinism.py` | 9 | Canonical-JSON serialiser sorts keys, strips clock fields, ASCII-escapes unicode; two runs on same CNT JSON produce identical hash; parent CNT hash carried forward verbatim; Planck max residual hits 4.440892098500626e-16 to the last digit |

Total: **43 tests passing in ~1.4s on Linux x86_64 / Python 3.10**.

### 4. HS_FAST_REFRESH — single-file AI loader at repo root

`HS_FAST_REFRESH.json` + `HS_FAST_REFRESH.md` — designed for one-fetch AI session loading. Mirrors the proven `HUF_FAST_REFRESH.json` pattern from the HUF repo. Contains:

- canonical names with NOT-list to prevent acronym mutation
- canonical engines (Python + R + pseudocode + schema for both CNT and CNQ) with raw URLs
- canonical numbers (three IEEE-floor confirmations with exact residuals + parent CNT hashes)
- canonical formulas (closure, CLR, Helmert, κᴴˢ, M²=I, atan2-stable rotation, sandwich product, Hamilton product, canonical-hash contract)
- dimension policy by D
- claim-strength table with avoid-phrases
- investigation catalog pointer (29 entries)
- notation/terminology pointer
- experiments (raw URLs for inputs + expected outputs)
- cross-platform reproduction challenge wording
- paper pipeline
- file map
- common drift errors (eight catalogued)

Any AI platform (Claude, ChatGPT, Grok, Gemini, Copilot) can fetch ONE URL and have the full system loaded. No more 10-files-at-a-time uploads.

### 5. PUBLICATION_READY.md — single entry point for the world

`PUBLICATION_READY.md` at repo root. Human-facing entry point: what the system is, what's available, how to use it (Python, R, AI assistant, CCTT), expected outputs, citation format, lineage, contact, cross-platform challenge invitation. Designed for first-time visitors of any technical level.

### 6. Public-use overlays on high-traffic READMEs

Top-of-file overlays on `Hs/README.md`, `HCI-CNT/README.md`, `HCI-CNQ/README.md` declaring full publication-grade status, pointing at HS_FAST_REFRESH for AI sessions and PUBLICATION_READY for human readers. The "EXPERIMENTAL — NOT FOR REPO USE" / "do_not_push" guards are explicitly retired everywhere they appeared (already done in push #26's status reconciliation; reinforced here).

### 7. Public-use declarations in all admin JSONs

- `ai-refresh/HS_ADMIN.json` — top-level `public_use_declaration` block (added earlier in this session, preserved here)
- `HCI-CNQ/HCI-CNQ_ADMIN.json` — `status.public_use: "fully_public"` field with subcomponent enumeration
- `HCI-CNQ/ARCHIVE_README.json` — header `_public_use_declaration` retiring all legacy guards

---

## Files added/modified in push #27

| Path | Action | Bytes | Notes |
|---|---|---|---|
| `HS_FAST_REFRESH.json` | new | ~14k | single-file AI loader |
| `HS_FAST_REFRESH.md` | new | ~6k | companion narrative |
| `PUBLICATION_READY.md` | new | ~10k | human-facing entry point |
| `HCI-CNQ/engine/cnq.R` | new | ~16k | R port with parity contract |
| `HCI-CNQ/engine/CNQ_PSEUDOCODE.md` | new | ~13k | language-agnostic algorithm |
| `HCI-CNQ/engine/tests/test_first_principles.py` | new | ~6k | 15 tests |
| `HCI-CNQ/engine/tests/test_dimension_policy.py` | new | ~6k | 19 tests |
| `HCI-CNQ/engine/tests/test_determinism.py` | new | ~5k | 9 tests |
| `HCI-CNQ/engine/tests/conftest.py` | new | small | pytest config |
| `HCI-CNQ/engine/tests/__init__.py` | new | small | package marker |
| `HCI-CNQ/engine/tests/README.md` | new | small | test suite docs |
| `Hs/README.md`, `HCI-CNT/README.md`, `HCI-CNQ/README.md` | edit (top-of-file overlay) | — | publication-grade banners |

Combined with the still-uncommitted #26+#27 work from the prior session: NOTATION_AND_TERMINOLOGY.md, CLAIM_STRENGTH_TABLE.md, STATUS_AND_MATURITY.md, CNQ_SCOPE_AND_LIMITS.md, ROUND3_VALIDATION_PLAN.md, HCI_DYADIC_COUPLING_LADDER.md, CNQ_BIQUATERNION_FACTORING.md, run_all_confirmations.py, verify_publication_results.py, expected_results.json, cnq.py + support modules, INV-028 / INV-029, four-field status reconciliation, terminology unification, public-use declaration.

---

## Cross-platform reproduction status

**Local platform (Linux x86_64 / Python 3.10):**

- 43 / 43 CNQ engine tests pass in ~1.4s
- Planck D=4 reproduction: `max_residual = 4.440892098500626e-16` (matches published)
- SM Neutrino D=3 reproduction: `max_residual = 3.3306690738754696e-16`, dimension label `boundary_or_degenerate_support`
- Two consecutive Planck runs produce identical `cnq_content_sha256 = 927af6a3...` (within local platform; cross-platform challenge open)
- Parent CNT hashes carried forward exactly: Planck `3de7d400...400c4`, Neutrino `60d733d2...6952`

**Cross-platform challenge:** open invitation to ChatGPT, Grok, Gemini, Copilot, and any third-party reviewer to clone the repo, run `python HCI-CNQ/scripts/run_all_confirmations.py --repo-root .`, and compare their `cnq_content_sha256` against the reference observations recorded in `HCI-CNQ/results/expected_results.json`. Bit-identical hashes across platforms = a fourth independent confirmation channel beyond the three load-bearing datasets.

---

## What this push does NOT do

- Does not run Round 3 — INV-022 stays OPEN, separate push #28
- Does not implement twin-quaternion factoring — INV-029 stays DEFERRED, scaffolded only
- Does not implement the dyadic coupling ladder — INV-028 stays DEFERRED
- Does not assign release tag `v3.0.0-paper1` — that happens after #27 validates green AND Round 3 lands
- Does not modify cnt.py or cnt.R beyond what was already in push #26

---

## Engine inventory after push #27

| Engine | Path | Lang | Status |
|---|---|---|---|
| CNT Python | `HCI-CNT/engine/cnt.py` | Python 3.9+ | canonical, v2.0.4 |
| CNT R | `HCI-CNT/engine/cnt.R` | R 4.0+ | parity-tested |
| CNT pseudocode | (legacy reference in cnt_v2/) | — | preserved |
| CNT schema | `HCI-CNT/cnt_v2/CNT_JSON_SCHEMA.md` | — | locked at 2.1.0 |
| CNT tests | `HCI-CNT/engine/tests/` | Python | determinism + first-principles + corpus + stage1 synthetic |
| CNQ Python | `HCI-CNQ/engine/cnq.py` | Python 3.9+ | canonical, v1.0.0 (push #26) |
| CNQ R | `HCI-CNQ/engine/cnq.R` | R 4.0+ | **NEW push #27**, parity contract |
| CNQ pseudocode | `HCI-CNQ/engine/CNQ_PSEUDOCODE.md` | — | **NEW push #27**, language-agnostic |
| CNQ schema | `HCI-CNQ/engine/CNQ_SCHEMA.md` | — | locked at cnq/1.0.0 |
| CNQ tests | `HCI-CNQ/engine/tests/` | Python | **NEW push #27**, 43 tests |

Two engines × two languages = four implementations. One pseudocode reference. Five doc layers (handbook volumes 1-4 for CNT, claim-strength + scope + status + Round 3 plan + dyadic + twin-quaternion for CNQ). One vocabulary reference. One single-file AI loader. One human entry point.

---

## The arc

| Push | Date | Theme |
|---|---|---|
| #22 | 2026-05-07 | Volume IV — Quaternion View integrated |
| #23 | 2026-05-07 | ChatGPT round-1 vocabulary cross-check + HCI-CNQ promotion |
| #24 | 2026-05-08 | Grok lineage cross-check + applied tiers + Investigation Catalog |
| #25 | 2026-05-08 | Sensitivity refinements (HUMAN→USER cleanup) |
| #26 | 2026-05-08 | ChatGPT round-2 audit + cnq.py production engine + claim control + terminology |
| **#27 (this push)** | **2026-05-08** | **Full publication: cnq.R + CNQ_PSEUDOCODE + 43 tests + HS_FAST_REFRESH + PUBLICATION_READY + public-use declaration** |
| #28 (next) | tbd | Round 3 full-corpus quaternion validation (INV-022) |
| #29 (next) | tbd | Release tag `v3.0.0-paper1` + arXiv submission |

---

## Final notes

After push #27 lands green via Validate Repository, the system is in publication-grade state:

- ✅ Both engines public, in two languages each, all deterministic
- ✅ Language-agnostic pseudocode for any future port
- ✅ 43-test CNQ test suite green
- ✅ One-command reproduction of the three IEEE-floor confirmations
- ✅ Strict observed-vs-expected verifier
- ✅ Single-file AI loader for any platform
- ✅ Human entry point with citation format
- ✅ Four-field status model and claim-strength discipline
- ✅ Master vocabulary doc with avoid-list
- ✅ All legacy "EXPERIMENTAL — NOT FOR REPO USE" guards retired
- ✅ Cross-platform reproduction channel open
- ✅ Investigation catalog: 29 entries, 4 dispositions, 4 source platforms

The repo is ready for the world. The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.

**Ready for `git add . && git commit && git push`.**
