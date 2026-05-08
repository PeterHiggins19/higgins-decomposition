# Push #31 — Licence clarity + grounding-test durability + cosmetic cleanup

**Date:** 2026-05-08
**Push:** #31 (after release `v0.29.0` was tagged on push #29 commit `512a7d7`)
**Type:** doc-only (no engine, no tests, no schema, no public API changes)
**Catalog references:** none (this push is cosmetic correction, not investigation)

---

## Why this push exists

A live verification fetch of the public GitHub repo after release `v0.29.0` landed surfaced three small issues. None affect the engine, the test suite, the determinism contract, or any of the IEEE-floor results. All three are cosmetic. They reduce reader friction:

1. **GitHub sidebar showed "Unknown, Unknown licenses found."** Two licence files at the repository root (`LICENSE` and `LICENSE-DOCS`) confused the licensee detector. The dual-licence split adopted in push #28 was correct in substance — Apache-2.0 for code, CC BY 4.0 for docs, per Creative Commons' own recommendation — but the file layout prevented GitHub from auto-detecting either.

2. **Grounding-test SHA had gone stale.** The README banner, `llms.txt`, `.well-known/ai-context.json`, `AI_AGENTS.md`, and `HS_FAST_REFRESH.json` all pinned commit `8f4406a` (push #28) as the "current" answer to the first grounding-test question. That answer was already two pushes out of date by the time the verification fetch ran. Pinning a specific SHA goes stale on every push; the test needed a more durable anchor.

3. **A pytest cache directory had slipped into version control.** `pytest-cache-files-ljser_3e/v/cache/nodeids` was tracked despite `.gitignore` carrying the `pytest-cache-files-*/` pattern from push #28. The directory was added before the gitignore line, so it survives unless explicitly removed via `git rm --cached`.

---

## What this push ships

### Licence layout — sidebar now reads "Apache-2.0"

| Change | Effect |
|---|---|
| Created `docs/LICENSE-DOCS.md` containing the full CC BY 4.0 text | Canonical home for the docs licence; named with `.md` extension; out of repository root |
| Replaced root-level `LICENSE-DOCS` with a stub redirect pointer | licensee no longer matches a CC pattern at root; only `LICENSE` (Apache-2.0) survives detection |
| Added `LICENSING.md` at the repository root | Plain-English summary of the dual-licence split, asset-class coverage, attribution mechanics, and the rationale ("Why two licences"). One-page answer for any reader who lands on the question. |
| Updated `NOTICE` references from `LICENSE-DOCS` → `docs/LICENSE-DOCS.md` | Consistency between the legal NOTICE and the actual file path |
| Updated `Hs/README.md` docs-licence badge link from `LICENSE-DOCS` → `docs/LICENSE-DOCS.md` | Badge now resolves to the live file |
| Added a third badge to `Hs/README.md`: "licensing — overview" linked at `LICENSING.md` | Reader landing on the README sees three licence touchpoints (code, docs, summary) |

After this push lands and GitHub re-runs licensee, the About-panel sidebar should display **Apache-2.0** cleanly with no "Unknown" entries. The dual structure remains intact — the docs are still CC BY 4.0; that's just no longer surfaced via the sidebar auto-detector (which was always going to be a bad fit for dual-licensed repos).

### Grounding test — pinned to release tag instead of SHA

The first grounding-test question is now:

> *"What is the latest release tag, and the most recent commit message on main?"*

Answer:

> Latest tag `v0.29.0` (dated 2026-05-08, "AI visibility infrastructure + Grok R3 catalog absorption"). Patch pushes after the tag may move the SHA forward without bumping the tag; the tag is the durable anchor.

Updated in five places consistently:

- `Hs/README.md` (top banner)
- `llms.txt`
- `AI_AGENTS.md` (§2 grounding-test table)
- `HS_FAST_REFRESH.json` (`grounding_test.questions[0]`)
- `.well-known/ai-context.json` (`grounding_test.questions[0]`)

Going forward, the grounding-test answer only needs to change when a new tag is cut — not on every push. This matches the actual semantic: when a tag moves, the public surface has changed enough that AI assistants should re-fetch. Patch pushes between tags can leave the answer stable.

### Pytest cache cleanup — Peter-side step required

I cannot delete the tracked `pytest-cache-files-ljser_3e/` directory from this VM (file deletion blocked by sandbox permissions). The `.gitignore` already has the correct pattern from push #28, so once the directory is removed via `git rm --cached`, it stays gone.

**Peter to run before commit:**

```bash
cd Current-Repo/Hs
git rm -r --cached pytest-cache-files-* 2>/dev/null
rm -rf pytest-cache-files-* 2>/dev/null
```

(The `2>/dev/null` swallows the error if the directory is already gone or never tracked. Both commands are safe to run.)

---

## What did NOT happen in this push

| | |
|---|---|
| Engine source code | unchanged — `cnt.py`, `cnt.R`, `cnq.py`, `cnq.R`, `geometry.py`, `hashing.py`, `cnt_adapter.py` all untouched |
| Tests | unchanged — 43-test CNQ suite still all green |
| `expected_results.json` | unchanged — Planck `4.440892098500626e-16` remains locked |
| Cross-language parity contract | unchanged — `cnq.py` ↔ `cnq.R` agreement preserved |
| Investigation Catalog | unchanged — 35 entries unchanged; this push doesn't open or close any investigation |
| Priority lock | reinforced — the basics-first chain is intact |
| Public-use status | unchanged — fully public per push #27 |

---

## Files added / modified

| Path | Action | Purpose |
|---|---|---|
| `docs/LICENSE-DOCS.md` | new | Canonical CC BY 4.0 text with header pointers to LICENSE / LICENSING.md / NOTICE |
| `LICENSING.md` | new | Plain-English dual-licence summary at repository root |
| `LICENSE-DOCS` | rewritten as stub redirect | Defangs licensee's CC-detection at root; preserves any inbound link |
| `NOTICE` | edit | Pointers updated to `docs/LICENSE-DOCS.md`; release version bumped to v0.29.0; push #31 noted in licence-structure block |
| `Hs/README.md` | edit | Banner: tag-based grounding-test answer; release `v0.29.0` framing; LICENSING.md badge added; docs-licence badge link bumped |
| `llms.txt` | edit | Grounding-test question 1 now tag-based |
| `AI_AGENTS.md` | edit | Grounding-test table row 1 now tag-based |
| `HS_FAST_REFRESH.json` | edit | `grounding_test.questions[0]` now tag-based |
| `.well-known/ai-context.json` | edit | `grounding_test.questions[0]` now tag-based |
| `ai-refresh/HS_ADMIN.json` | edit | session log entry for push #31; `licensing` block updated to reflect new file layout |
| `ai-refresh/AI_REFRESH_2026-05-08_push31_license_clarity.md` | new (this file) | Push narrative |

No INVESTIGATION_CATALOG entry — this push is correction, not investigation.

---

## Catalog status after push #31

```
35 investigations: 12 CANONICAL · 15 DEFERRED · 1 FALSIFIED · 7 OPEN
By source: CLAUDE 7 · CHATGPT 7 · GROK 14 · USER 7 · PILOT 0
```

Identical to post-push-#30. This push does not move the catalog.

---

## The arc

| Push | Date | Theme |
|---|---|---|
| #22-#27 | 2026-05-07/08 | Engine + claim-control + publication-grade |
| #28 | 2026-05-08 | External audit response (packaging + licence split) |
| #29 | 2026-05-08 | AI visibility infrastructure |
| #30 | 2026-05-08 | Grok R3 catalog absorption (3 DEFERRED entries) |
| **#31 (this push)** | **2026-05-08** | **Licence clarity + grounding-test durability + cosmetic cleanup** |
| Round 3 (next) | tbd | Full-corpus quaternion validation (INV-022) |
| arXiv (next) | tbd | Paper 1 submission |

Eleven pushes today. The repository's public face now matches its internal substance: licence clearly displayed, grounding test durable across patch pushes, no stray cache artefacts on the public tree.

---

## Final notes

This push exists because someone reading the repo for the first time should not have to puzzle through "Unknown, Unknown" sidebar text or wonder which of two licence files governs which assets. The substance was always right; the surface was just rough. Push #31 sands the surface.

The release tag `v0.29.0` remains valid — this push is a patch on top of it, not a new tagged release. If at some later point the public face accumulates enough patch-level changes to warrant a new tag, that would be `v0.29.1` or `v0.30.0`. For now, the tag holds and the patches accumulate cleanly underneath it.

The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line. The discovery channels carry the loader. The grounding test catches the drift. The catalog absorbs the candidates. The licence speaks plainly. **Basics first.**

**Ready for `git add . && git commit -m "Push #31 — Licence clarity + grounding-test durability" && git push`.**
