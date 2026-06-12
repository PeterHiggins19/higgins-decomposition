# Push #16 Audit Report — Live-Repo Verification of Push #15 + Cleanup

**Date:** 2026-05-06
**Last validated push:** `f38a7c9` (Validate Repository #15 — HCI-CNT)
**Next push:** #16 — version-coherence cleanup
**Status:** **READY TO PUSH** (after the cleanup below is committed)

---

## Live-repo verification

A fresh clone of `https://github.com/PeterHiggins19/higgins-decomposition`
at commit `f38a7c9` was inspected against the local pre-push state.

### Confirmed (10 checks PASS)

1. **HCI-CNT/ subfolder present** with 17 expected directories.
2. **236 files** in HCI-CNT/ (within 2 of the local 238 — see delta below).
3. **All 8 EMBER countries × (Stage 1 PDF + Stage 2 PDF + canonical JSON)** present.
4. **All 3 handbook volumes** present (122 KB + 172 KB + 53 KB).
5. **All 3 CoDa-community papers** present + ROI ternary figure (PDF + PNG).
6. **CodaWork 2026 conference demo** present: spectrum PDF (99 KB), projector HTML (235 KB), 10-slide PowerPoint (1.65 MB).
7. **Engine reports** `cnt 2.0.4 / schema 2.1.0` when imported.
8. **Canonical experiments folder JSONs** are all at `cnt 2.0.4 / schema 2.1.0` (verified on ember_jpn, markham_budget, nuclear_semf).
9. **`tools/verify_package.py`** runs from the live clone and reports **PACKAGE READY**.
10. **GitHub Actions Validate Repository #15** completed PASS in 34 seconds.

### Three issues found in the live state (all minor, all fixable)

**Issue 1 — Per-country snapshot JSONs in `conference_demo/cnt_demo/02_per_country/` are stale at engine 2.0.3 / schema 2.0.0.**
The canonical `experiments/codawork2026/<id>/<id>_cnt.json` files were
correctly re-generated when the engine bumped to 2.0.4 (the
determinism gate passes 25/25 on those). The conference-demo *snapshot
copies* of those JSONs were not refreshed at the same time, so they
display the older engine version in the report cover and footer.
Internally they are still self-consistent (their PDFs match their
JSONs), but they don't reflect the current engine.

**Issue 2 — `experiments/INDEX.json` `_meta.engine` field reads `cnt 2.0.3`.**
This is a stale meta string. The actual per-experiment SHAs published
in INDEX are the 2.0.4 SHAs (the determinism gate passes against
them); only the human-readable `_meta.engine` label on the registry
header was not bumped.

**Issue 3 — Stray temp file `lu4422tlij.tmp` in `conference_demo/talk_deck/`.**
A LibreOffice/`soffice` temp file leaked from the PowerPoint→PDF
conversion step at deck-build time and was committed accidentally.
Harmless, but noise.

### Minor housekeeping

- The live repo carries one `.pyc` file under `engine/__pycache__/` that should be `.gitignore`d.
- The local working copy has a different `.pyc` under `engine/tests/__pycache__/`, accounting for the 2-file delta against the live count.

## Fixes applied locally for push #16

1. **All 8 per-country JSONs refreshed** from canonical `experiments/codawork2026/`. Now all read `cnt 2.0.4 / schema 2.1.0` with `metadata.units` present.
2. **All 16 per-country PDFs (Stage 1 + Stage 2) regenerated** from the refreshed JSONs.
3. **Combined spectrum + projector regenerated** from the current engine (preserves the COMBINED projector view's shared PCA frame computation).
4. **`experiments/INDEX.json` `_meta`** bumped: `engine: cnt 2.0.4`, `schema: 2.1.0`, `last_updated: 2026-05-06T18:45:00Z`.
5. **`HCI-CNT/.gitignore`** added covering `__pycache__/`, `*.pyc`, `*.tmp`, soffice lockfiles.
6. **Note**: `lu4422tlij.tmp` could not be removed via the sandboxed bash (mount permissions). It needs `git rm` at push time, or simply staying in tree — the new `.gitignore` will prevent future leaks.

After fixes, `tools/verify_package.py` again reports **PACKAGE READY**.

## Files for push #16

### Modified (26)
```
HCI-CNT/experiments/INDEX.json
HCI-CNT/conference_demo/cnt_demo/02_per_country/ember_<8 codes>/ember_<code>_cnt.json   (8)
HCI-CNT/conference_demo/cnt_demo/02_per_country/ember_<8 codes>/stage1_ember_<code>.pdf (8)
HCI-CNT/conference_demo/cnt_demo/02_per_country/ember_<8 codes>/stage2_ember_<code>.pdf (8)
HCI-CNT/conference_demo/cnt_demo/03_combined/spectrum_paper_codawork2026_ember.pdf
HCI-CNT/conference_demo/cnt_demo/03_combined/plate_time_projector_codawork2026_ember.html
HCI-CNT/conference_demo/cnt_demo/03_combined/_pipeline_manifest.json
```

### Added (1)
```
HCI-CNT/.gitignore
```

### To remove (1)
```
HCI-CNT/conference_demo/talk_deck/lu4422tlij.tmp
```

## Recommended commit + push

From the parent `Current-Repo/Hs/` directory:

```bash
git add HCI-CNT/.gitignore
git rm HCI-CNT/conference_demo/talk_deck/lu4422tlij.tmp
git rm --cached HCI-CNT/engine/__pycache__/cnt.cpython-310.pyc 2>/dev/null
git add HCI-CNT/experiments/INDEX.json
git add HCI-CNT/conference_demo/cnt_demo/
git commit -m "HCI-CNT: refresh demo snapshots to engine 2.0.4 / schema 2.1.0; add .gitignore; clean temp file"
git push origin main
```

## What the live-repo verification proves

* The push #15 publication of HCI-CNT into the public Hs repository is
  **structurally complete and reviewer-usable today**: a third-party
  reviewer can clone, navigate to `HCI-CNT/`, run
  `python tools/verify_package.py`, and see PACKAGE READY in under a
  minute.
* The 25-experiment determinism gate is reproducible from the live
  repository at the canonical `experiments/` location.
* The conference demo, slide deck, three handbook volumes, and three
  CoDa-community papers are all in their announced locations at their
  expected sizes.
* The hash-chain provenance claim in Volume III §B is now verifiable
  against a public artefact: a reader can compute
  `sha256sum HCI-CNT/experiments/codawork2026/ember_jpn/ember_jpn_input.csv`
  and compare against the `inp.source_file_sha256` field in the
  corresponding `_cnt.json`. The chain holds.

The three issues identified are version-coherence in the *snapshots*,
not correctness in the canonical engine outputs. The cleanup commit
brings the snapshots into alignment.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
