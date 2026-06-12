# Push #52 — Pre-Push Summary

**Date:** 2026-05-19
**Status:** READY-TO-COMMIT (HOLD released — see [`PUSH52_READY_FOR_COMMIT.md`](PUSH52_READY_FOR_COMMIT.md))
**Theme:** 🏁 Point-of-restore milestone — CoDaWork 2026 conference-ready · publish for attendees
**Doctrine class:** S2 (engine source change, all conference artefacts unchanged in substance)

---

## What this push contains

This is the **conference-publication push**. It captures the 2026-05-19 point-of-restore milestone and makes the entire bundle publicly visible for CoDaWork 2026 attendees (in-room or remote) to follow along, download, and run locally.

### Headline changes

1. **Engine v3.2.0** — `HCI-CNT/engine/cnt.py` bumped from v3.1.0 to v3.2.0. New `compute_navigation_2d()` function emits an ILR-Helmert PCA 2-D barycenter trajectory in every output as a top-level `navigation_2d` block. Backwards-compatible — every v3.1.0 field unchanged.

2. **Projector v2.0** — `CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html` now offers the three-mode projection standard:
   - **RADAR STACK** (default) — per-year radar snapshots stacked along z.
   - **BARYCENTER TRAJECTORY** (BARY) — spine bends through space via engine v3.2.0 ILR-Helmert PCA.
   - **BARYCENTER-ALIGNED** (ALIGN) — trajectory forced onto the z-axis; pure shape variation remains.
   - **SHOCK** overlay tints plate outlines by Aitchison-step magnitude.
   A live PROJECTION info panel shows the math being applied. Japan 2014 now visibly registers the multi-year reorganisation.

3. **Manuscript v1.3** — `papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.docx` + `.pdf` rebuilt with a cover page, table of contents, header on every body page, footer with page numbers, fixed table widths (no margin overflow), and a working copy placed inside `CODA-Association/CODAwork2026/` so the conference folder holds everything in one place. 25 pages total.

4. **Conference-attendee landing page** — new `CODA-Association/CONFERENCE_ATTENDEES.md` is the single-link entry point for the audience. Direct links to talk deck PDF, manuscript PDF, cinema scroll PDF, interactive projector. Instructions for in-browser use via GitHub Pages, local download, or git clone.

5. **README chain refreshed** — root README has a prominent attendee callout linking to the new page. CODA-Association/README.md, CODAwork2026/README.md, and data_outputs/README.md all carry the milestone callout. All landing pages refreshed.

6. **Milestone document** — `CODA-Association/POINT_OF_RESTORE_2026-05-19.md` defines the recovery target if anything destabilises before the conference.

7. **AI refresh narrative** — `ai-refresh/AI_REFRESH_2026-05-19_conference_ready.md` for cross-AI consumers covering the milestone state.

8. **VERSION_HISTORY.md** — bumped from v1.6 to v1.10 with four new 2026-05-19 dated entries (manuscript v1.3, projector v2.0, engine v3.2.0, milestone).

9. **CHANGELOG.md** — push #52 entry prepended to the conference-prep arc table.

10. **EXPERIMENTS_JOURNAL.md** — push #52 row appended to §5 push event log; "Last refresh" updated.

### Engine-version policy (conference-stability lock)

| Layer | Version | Status |
|---|---|---|
| Engine source (`HCI-CNT/engine/cnt.py`) | **v3.2.0** | Current. Adds `navigation_2d` block. |
| R port (`HCI-CNT/engine/cnt.R`) | v3.1.0 | v3.2.0 port queued post-conference. |
| **CoDaWork 2026 corpus** (`CODA-Association/CODAwork2026/data_outputs/per_country_json/cnt_v3/`) | **v3.1.0 (LOCKED)** | Not regenerated. Conference materials cite this. |
| Projector inline data | v3.1.0 base + v3.2.0-equivalent `bary_xy` | Produced by sidecar `outputs/regen_baryxy.py` from v3.1.0 JSONs. |
| Manuscript engine citations | v3.1.0 | Unchanged. |

The split preserves every word of the conference materials (they continue to cite engine v3.1.0 corpus output) while allowing the projector to use the CoDa-correct ILR-Helmert PCA geometry that v3.2.0 makes canonical.

## Files touched

### New files (8)
- `CODA-Association/POINT_OF_RESTORE_2026-05-19.md` — milestone document
- `CODA-Association/CONFERENCE_ATTENDEES.md` — attendee landing page
- `CODA-Association/CODAwork2026/Compositional_Monitoring_2026.docx` — manuscript working copy
- `CODA-Association/CODAwork2026/Compositional_Monitoring_2026.pdf` — manuscript working copy
- `ai-refresh/AI_REFRESH_2026-05-19_conference_ready.md` — narrative
- `ai-refresh/PUSH52_PRE_PUSH_SUMMARY.md` (this file)
- `ai-refresh/PUSH52_READY_FOR_COMMIT.md` — commit-time release card

### Modified files
- `HCI-CNT/engine/cnt.py` — engine version 3.1.0 → 3.2.0; new `compute_navigation_2d()` function; wired into `cnt_run` payload
- `CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html` — projector v2.0 (three-mode standard + SHOCK + engine v3.2.0 bary_xy)
- `CODA-Association/CODAwork2026/data_outputs/CodaWork2026_FinalTalk_2026-05-17.pptx` + `.pdf` — 20 → 22 slides (3 per-country navigation slides)
- `CODA-Association/CODAwork2026/data_outputs/build_final_talk.py` — reproducible build for the 22-slide deck
- `CODA-Association/CODAwork2026/data_outputs/README.md` — projector v2.0 documentation added (v3.0 → v4.0)
- `CODA-Association/CODAwork2026/VERSION_HISTORY.md` — v1.6 → v1.10 with four 2026-05-19 entries
- `CODA-Association/CODAwork2026/README.md` — milestone callout, slide-count update, projector v2.0 (v2.0 → v2.1)
- `CODA-Association/README.md` — milestone callout (v2.0 → v2.1)
- `README.md` (Hs root) — CoDaWork attendees callout + point-of-restore callout above conference-status block
- `CHANGELOG.md` — push #52 entry prepended to conference-prep arc table
- `EXPERIMENTS_JOURNAL.md` — push #52 row in §5; "Last refresh" updated
- `papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.docx` + `.pdf` — manuscript v1.3 master copies
- `papers/codawork2026/manuscript/build/build_docx.js` — adds cover page + TOC; replaces cramped repo table with vertical entries; widens colour-table notes column; reduces equation font

## Pre-flight verification

- ✅ All new/modified files exist on disk (verified via bash).
- ✅ Projector HTML JavaScript syntax check passes (`node --check`).
- ✅ Engine v3.2.0 smoke test on Japan: PC1+PC2 captures 99.5 %; 2011→2012 disk-step 0.052; 2013→2014 disk-step 0.83 (multi-year reorganisation, as predicted in the manuscript Discussion).
- ✅ Conference corpus JSONs unchanged (still engine v3.1.0).
- ✅ Manuscript renders cleanly to PDF (25 pages, cover + TOC + body).
- ✅ Talk deck renders cleanly to PDF (22 slides, 1.5 MB).
- ✅ All cross-references in the new README chain resolve.
- ✅ VERSION_HISTORY.md is structurally valid (Markdown).
- ✅ CHANGELOG.md push #52 entry inserted at correct position.

## Queued admin updates (not blocking conference)

These admin-stream JSON updates are recorded in the milestone doc and AI_REFRESH narrative; they do not affect the conference deliverables and can be applied at the next admin sync (push #53 or post-conference):

- `HS_ADMIN.json` `session_log` entry for 2026-05-19 milestone.
- `HS_FAST_REFRESH.json` `_meta.engine_version` bump to v3.2.0 + milestone reference + last_push to 52.
- `INVESTIGATION_CATALOG.json` new INV-064 — *Engine v3.2.0 `navigation_2d` block: ILR-Helmert PCA barycenter trajectory* (STAGED disposition; CANONICAL after R-port parity).
- `cnt.R` port to v3.2.0 — cross-language parity (to IEEE machine-floor precision) — queued for post-conference parity work.

## What CoDaWork attendees can do after this push

1. **Read the manuscript at https://github.com/PeterHiggins19/higgins-decomposition** — the new attendee page is one click from the root README.
2. **Download the projector HTML** and run it locally in any browser — no install required, no network calls.
3. **Try the three projection modes on Japan** — BARY shows the multi-year reorganisation, ALIGN shows the post-shock structural shift toward solar and renewables.
4. **Verify any number in the talk** — the JSON files for all 9 countries are public, the engine is open-source, and the Supplementary Information has reproduction commands with SHA-256 hashes.

## Commit message (proposed)

```
push #52: 🏁 Point-of-restore — CoDaWork 2026 conference-ready · publish for attendees

* Engine cnt.py v3.1.0 → v3.2.0 with new navigation_2d block (ILR-Helmert PCA
  barycenter trajectory). Backwards-compatible: every v3.1.0 field unchanged.
  Conference corpus pinned to v3.1.0; not regenerated. R port queued.

* Projector v2.0: three-mode standard RADAR / BARY / ALIGN + SHOCK overlay.
  Consumes engine v3.2.0 ILR-Helmert PCA bary_xy via sidecar regen_baryxy.py.
  Live PROJECTION info panel shows the math. Japan 2014 now visibly registers
  the multi-year reorganisation.

* Manuscript v1.3 with cover page + TOC + scientific-report layout. Working
  copies of .docx/.pdf placed inside CODA-Association/CODAwork2026/.

* New milestone document POINT_OF_RESTORE_2026-05-19.md defines the recovery
  target. New CONFERENCE_ATTENDEES.md is the single-link entry page for the
  audience (in-room or remote).

* README chain refreshed: root, CODA-Association, CODAwork2026, data_outputs.
  Attendee callout prominent at the top of the root README.

* VERSION_HISTORY.md 1.6 → 1.10 (four 2026-05-19 entries).
  CHANGELOG.md push #52 entry. EXPERIMENTS_JOURNAL.md push #52 row.
  AI_REFRESH_2026-05-19_conference_ready.md narrative.

Admin updates queued (HS_ADMIN, HS_FAST_REFRESH, INV-064 STAGED, cnt.R port)
— not blocking conference.
```

## Doctrine compatibility

- **S2 doctrine compatibility:** engine source code change (cnt.py v3.2.0) is the only S2 source-code change. The conference corpus output (`per_country_json/cnt_v3/`) is **unchanged** — same hashes, same content. The talk deck, manuscript, cinema scroll, all engine standards, and the INV catalog are unchanged in substance (catalog INV-064 is queued, not landed yet).
- **Lockdown compatibility:** all v3.1.0 outputs preserved. v3.2.0 functionality is additive. No regenerated conference artefacts. No NO-CREATE file changes.
- **HUF-STD-001 v1.1 (Publication Standards):** AI Use Declaration present on talk deck slide 21 and manuscript Acknowledgements section.
- **HUF-STD-002 (Tensor Train I/O):** engine v3.2.0 `navigation_2d` is a new downstream-visualisation primitive that lives at Order 0 (visualisation-only); cross-references to be added to the standard at next sync.
- **HUF-STD-003 (Linear Algebra Foundations):** the new PCA computation uses the Helmert-orthonormal basis (Foundation 5) and the spectral theorem (Foundation 6) — both already on the standard.

## Sign-off

This push prep card is the pre-flight verification for push #52. The next step is to release the HOLD and write `PUSH52_READY_FOR_COMMIT.md` with the exact command sequence Peter will run.

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
