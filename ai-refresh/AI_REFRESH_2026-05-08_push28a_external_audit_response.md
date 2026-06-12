# Push #28a — External audit response (ChatGPT deep-research crawl)

**Date:** 2026-05-08
**Push:** #28a (after #27 "HCI-CNT/CNQ engines" landed green at commit `0640b59`)
**Type:** software-product-maturity hardening — packaging, licensing, easy-access entry points
**Catalog reference:** INV-030 (NEW, CANONICAL — actioned in this push)

---

## Why this push

After push #27 landed publication-grade, ChatGPT performed a **deep-research web crawl** of the live repo and produced a structured external audit. This is the third productive ChatGPT seam (after vocabulary cleanup in push #23 and engine + claim-control in push #26). Unlike the earlier rounds — which were prompt-driven — this one was a fresh-eyes external read of what an outsider sees on GitHub today.

The audit's framing was useful: *"the repo is strongest when read as a public research program with a reproducibility ethos, a deterministic pipeline, and a rapidly evolving theory/application stack. It is weaker when judged by the standards of a production-ready open-source software package."*

Push #28a addresses every actionable software-product-maturity item the audit raised, while preserving everything intentional about the research-character monorepo structure.

---

## What the audit found

Seven actionable items + several fair-criticism-but-design-choice items.

### Actionable (all eight items addressed in push #28a)

| # | Audit finding | Action |
|---|---|---|
| 1 | Stale paragraph in README: *"the compiled `cnq.py` engine is the next milestone (~14 days)"* contradicts the push #27 overlay declaring CNQ shipped | Rewrote the push #23 paragraph to reflect the full #23 → #27 arc |
| 2 | License badge says "CC BY 4.0" — Creative Commons themselves recommend against using CC for software | License split: Apache-2.0 for code (`LICENSE`), CC BY 4.0 for docs (`LICENSE-DOCS`), `NOTICE` explaining rationale |
| 3 | No `pyproject.toml` / `requirements.txt` / Dockerfile at root | `pyproject.toml` (PEP 621, setuptools backend, console scripts `hs-cnt` and `hs-cnq`) + `requirements.txt` |
| 4 | `pytest-cache-files-*/` accidentally committed; `.gitignore` minimal | Expanded `.gitignore` to cover `.pytest_cache/`, `pytest-cache-files-*/`, build artefacts, virtualenvs, IDE files, R artefacts, secrets |
| 5 | `tools/pipeline/` presented as primary engine surface, obscuring the canonical HCI-CNT and HCI-CNQ engines | Cross-link banner at top of `tools/pipeline/README.md` explicitly directing readers to `HCI-CNT/engine/cnt.py` and `HCI-CNQ/engine/cnq.py` as the current canonical engines |
| 6 | License badges in Hs/README.md and HCI-CNT/README.md still show CC BY 4.0 only | Updated both READMEs to display dual-licence badges and a cross-link to NOTICE |
| 7 | "HCI-CNQ tier live (cnq.py pending)" badge is stale | Updated to "HCI-CNQ engine shipped (py + R + pseudocode)" |
| (bonus) | First-time visitors lack a single-page on-ramp | Added `QUICKSTART.md` at repo root: 30-second reproduction + 2-minute Python + 2-minute R + 5-minute AI-assistant paths |

### Deferred (with explicit owner)

| Item | Owner / when |
|---|---|
| GitHub repo description shows "17 domains, 28 systems"; README At-a-Glance shows "18 domains, 36 systems" | Peter to update via GitHub UI; pure-text fix |
| Release tag `v0.27.0` for the publication-grade landing | Apply after push #28a validates green via the Validate Repository workflow |

### Deliberately kept (with justification)

| Audit observation | Why it stays |
|---|---|
| Monorepo structure mixing code + experiments + slides + docx | Intentional: this is a research communication + experiment + code repo, not a minimal pip package. PUBLICATION_READY.md and HS_FAST_REFRESH.json are the navigation surfaces for that mixed payload. |
| HTML 75.5%, Python 20% language mix | Reflects the documentation-heavy character. Not a defect; the demos and slides ARE part of the deliverable. |
| Bus factor of one at the commit level | Mitigated structurally: 4 AI platforms (Claude × N, ChatGPT × 3, Grok × 1, deep-research-crawl × 1) and the cross-platform reproduction challenge create review-level redundancy even when commit authorship is single. |

---

## Files added/modified in push #28a

| Path | Action | Notes |
|---|---|---|
| `pyproject.toml` | new | PEP 621 + setuptools, version 0.27.0, console scripts, optional dev/plates extras |
| `requirements.txt` | new | numpy>=1.20 only; comments for optional dev/plates |
| `LICENSE` | rewrite | Was CC BY 4.0; now Apache-2.0 for code with a header explaining the split |
| `LICENSE-DOCS` | new | CC BY 4.0 for prose, slides, notebooks, HTML demos, prose-form JSON |
| `NOTICE` | new | Rationale + asset-class coverage table + attribution + companion HUF pointer |
| `.gitignore` | expand | 7 lines → 70 lines covering Python caches, build artefacts, virtualenvs, IDE, R, LibreOffice, Jupyter, secrets |
| `QUICKSTART.md` | new | Single-page absolute-fastest-path on-ramp |
| `README.md` (root) | edit | Stale push #23 paragraph rewritten; license badge → dual-licence; CNQ tier badge → "engine shipped"; At-a-Glance license row updated |
| `HCI-CNT/README.md` | edit | License line updated to "Code: Apache-2.0 · Docs: CC BY 4.0" |
| `tools/pipeline/README.md` | edit | Top banner cross-linking to canonical HCI-CNT and HCI-CNQ engines; title clarified as "legacy 12-step reference" |
| `ai-refresh/INVESTIGATION_CATALOG.json` + `.md` | edit | Added INV-030 (CANONICAL, sourced CHATGPT); summary recomputed (30 entries, 10 CANONICAL, by-source CHATGPT 7) |
| `ai-refresh/HS_ADMIN.json` | edit | + `packaging`, `license_split`, `audit_response` blocks; session log updated |
| `ai-refresh/AI_REFRESH_2026-05-08_push28a_external_audit_response.md` | new (this file) | |

---

## How the licence split works

Two licence files at the repo root, one NOTICE explaining the structure:

| File | Covers |
|---|---|
| `LICENSE` (Apache-2.0) | All `.py`, `.R`, `.js`, shell scripts, build configuration (pyproject.toml, requirements.txt), engine schemas embedded in source |
| `LICENSE-DOCS` (CC BY 4.0) | All `.md`, `.pptx`, `.docx`, HTML demonstrations, prose-form JSON, PDFs |
| `NOTICE` | Rationale + asset-class coverage + attribution + Creative Commons FAQ pointer |

The split is non-controversial — Apache-2.0 is the standard for reusable Python software (NumPy, pandas, TensorFlow all use it or compatible licences) and CC BY 4.0 is standard for prose. The CC FAQ explicitly says CC licences are not intended for software because they lack patent grants and source-vs-binary handling.

For users: code use is unrestricted with attribution and patent grant; documentation use is unrestricted with attribution. Both permit derivatives.

---

## How `pip install -e .` works now

After push #28a:

```bash
git clone https://github.com/PeterHiggins19/higgins-decomposition
cd higgins-decomposition
pip install -e .
```

This installs:
- **Console scripts**: `hs-cnt` and `hs-cnq` are exposed as command-line tools
- **Python package import paths**: `HCI_CNT` and `HCI_CNQ` (note: hyphenated folder names mapped to underscored Python identifiers via `[tool.setuptools.package-dir]`)
- **Optional dev tools**: `pip install -e .[dev]` adds pytest

For users who don't want to install, the engine scripts still run directly from source:

```bash
python HCI-CNT/engine/cnt.py input.csv -o output.json
python HCI-CNQ/engine/cnq.py --cnt-json output.json --out cnq.json
```

---

## Cross-platform reproduction challenge — status

The four-channel reproduction matrix is unchanged:

| Platform | Channel | Status |
|---|---|---|
| Linux x86_64 / Python 3.10 / numpy | reference | locked in `expected_results.json` |
| Cross-platform Python (Windows, macOS, other Linux) | open invitation | pending volunteers |
| Cross-language R (cnq.R) | parity-tested | conformance test in pseudocode §9 |
| Future ports (Julia, Rust, JS, C++) | open invitation | pseudocode is the conformance reference |

Any `cnq_content_sha256` hash drift across platforms is a **finding** to file as a GitHub issue, not a failure. The `max_residual` to ≤ 1 ULP is the load-bearing equivalence; hash-byte-equality is the strict additional contract.

---

## What this push does NOT do

- Does not run Round 3 (INV-022) — separate push #28
- Does not modify any engine source — cnt.py / cnt.R / cnq.py / cnq.R / pseudocode unchanged
- Does not modify the 43-test CNQ test suite
- Does not assign release tag `v0.27.0` until Validate Repository runs green on this commit

---

## The arc

| Push | Date | Theme |
|---|---|---|
| #22 | 2026-05-07 | Volume IV — Quaternion View |
| #23 | 2026-05-07 | ChatGPT round-1 vocabulary + HCI-CNQ promotion |
| #24 | 2026-05-08 | Grok lineage + applied tiers + Investigation Catalog |
| #25 | 2026-05-08 | Sensitivity refinements (HUMAN→USER cleanup) |
| #26 | 2026-05-08 | ChatGPT round-2 audit + cnq.py engine + claim control |
| #27 | 2026-05-08 | Full publication: cnq.R + pseudocode + 43 tests + HS_FAST_REFRESH + PUBLICATION_READY |
| **#28a (this push)** | **2026-05-08** | **External audit response: packaging + license split + QUICKSTART + cross-links** |
| #28 (next) | tbd | Round 3 full-corpus quaternion validation (INV-022) |
| #29 (next) | tbd | Release tag `v3.0.0-paper1` + arXiv submission |

Six pushes in a single day, four of them green-validated through CI. The cross-AI cross-check pattern is now five layers deep:

1. Claude (internal building, integration)
2. ChatGPT round 1 — vocabulary cleanup (push #23)
3. Grok — lineage and speculative extension (push #24)
4. ChatGPT round 2 — engine + claim control + terminology (push #26+#27)
5. ChatGPT deep-research crawl — software-product-maturity audit (push #28a, this push)

Each cycle has produced a measurable improvement to the system. The pattern is doing real work.

---

## Final notes

After push #28a lands green via Validate Repository, the system is in **publication-grade-with-modern-packaging** state:

- ✅ Both engines public, in two languages each
- ✅ Language-agnostic pseudocode for any future port
- ✅ 43-test CNQ test suite green
- ✅ One-command reproduction of three IEEE-floor confirmations
- ✅ Strict observed-vs-expected verifier
- ✅ Single-file AI loader for any platform
- ✅ Human entry point with two-command reproduction
- ✅ **`pip install -e .` works from a clean clone** ← NEW
- ✅ **Dual-licence: Apache-2.0 for code, CC BY 4.0 for docs** ← NEW
- ✅ **`QUICKSTART.md` for first-time visitors** ← NEW
- ✅ **`.gitignore` covers all standard cache and build artefacts** ← NEW
- ✅ **`tools/pipeline/` clearly labelled as legacy reference** ← NEW
- ✅ Investigation catalog: 30 entries across 5 source platforms
- ✅ Cross-platform reproduction channel open

The repo is now navigable for software reviewers as well as research reviewers. The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line. The licences are correctly typed. The packaging metadata exists.

**Ready for `git add . && git commit -m "Push #28a — External audit response: packaging + license split + QUICKSTART" && git push`.**
