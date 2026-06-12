# PUSH #58 — READY FOR COMMIT

**Date:** 2026-05-20
**Status:** HOLD cleared — ready for Peter to commit via GitHub Desktop.
**Suggested CI name:** `Refinement-trail archive — 10-slide is the only talk`
**Suggested commit message:**

```
Archive the talk-deck refinement trail — 10-slide is the only active talk

Trigger: ChatGPT review of CODA-Association/ flagged that the README chain
still framed the 22-slide and 12-slide decks as "preserved siblings" or
"time-budget fallbacks". With the 10-slide compressed final adopted as
the conference talk, the sibling framing was a source of confusion — the
repo still looked like three decks were on offer rather than one.

Peter's directive: "keep the 10 slide and talk, archive the other slides
and associated talks and update the readme files and md files to reflect
the change, this will clean up and make the repo less confusing, the
trail of refinements get archived the best move forward."

Files moved to CODA-Association/CODAwork2026/archive/talk_decks_pre_10slide_2026-05-20/:
  CodaWork2026_FinalTalk_2026-05-17.pptx              (22-slide original narrative)
  CodaWork2026_FinalTalk_2026-05-17.pdf
  CodaWork2026_FinalTalk_12Slide_2026-05-20.pptx      (12-slide intermediate compression)
  CodaWork2026_FinalTalk_12Slide_2026-05-20.pdf
  CodaWork2026_FinalTalk_12Slide_CompressionPlan.json (ChatGPT 22→12 plan)
  build_final_talk.py                                  (22-slide builder)
  build_final_talk_v2.py                               (22-slide builder v2)
  build_final_talk_12slide.py                          (12-slide builder)
  SPEAKING_SCRIPT.md                                   (22-slide beat script)

Files remaining active:
  CODA-Association/CODAwork2026/data_outputs/
    CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx     ← THE talk
    CodaWork2026_FinalTalk_10Slide_2026-05-20.pdf
    build_final_talk_10slide.py
  CODA-Association/CODAwork2026/SPEAKING_SCRIPT_10slide.md

Stale-reference fixes flagged by ChatGPT (now closed):
  "At slide 18, switch projector to cinema scroll"
    → "After slide 10, switch the projector display to cinema scroll"
  "At slide 19, open the manifold projector"
    → "Then open the projector as the Q&A backdrop"
  "AI Use Declaration on slide 19 of the FinalTalk; Standard Stamp on slide 20"
    → "AI Use Declaration on slide 10 (synthesis-slide footer) and on
       the manuscript cover + back-matter"

Refreshed (README chain):
  CODA-Association/README.md                                    (v2.3)
  CODA-Association/CONFERENCE_ATTENDEES.md                      (sibling link → archive link)
  CODA-Association/POINT_OF_RESTORE_2026-05-19.md               (added 2026-05-20 update note)
  CODA-Association/CODAwork2026/README.md                       (v2.3)
  CODA-Association/CODAwork2026/data_outputs/README.md          (v6.0)
  CODA-Association/CODAwork2026/VERSION_HISTORY.md              (+entry at top)
  CODA-Association/CODAwork2026/archive/README.md               (rebuilt — added new section first)

New:
  CODA-Association/CODAwork2026/archive/talk_decks_pre_10slide_2026-05-20/README.md

Admin (queued for post-commit sync):
  HS_FAST_REFRESH.json                last_push → #58 HOLD
  ai-refresh/HS_ADMIN.json            push_58_prepared
  ai-refresh/PUSHES_INDEX.md          push #58 section
  ai-refresh/PUSH58_READY_FOR_COMMIT.md
  CHANGELOG.md                        push #58 row

Untouched (Pre-Conference Lockdown discipline preserved):
  Engine code (HCI-CNT/engine/cnt.py, HCI-CNQ/engine/cnq.py)
  Schemas (CNT 3.1.0, CNQ 2.0.0)
  Investigation catalog
  papers/codawork2026/talk/ and papers/codawork2026/manuscript/
  CODAwork2026/Compositional_Monitoring_2026.{docx,pdf}  (msprint, populated TOC)
  data_outputs/per_country_json/, per_country_pdfs/, dual_view/, projector, cinema scroll
  All NO-CREATE files

Push class: S2 (doc-only). Files moved within the working tree, not deleted.
Lineage fully preserved; the archive folder ships its own README explaining
each artefact and why it was superseded.

The instrument reads. The expert decides. The hashes carry the receipts.
The vocabulary holds the line. The AI follows the same protocol.
```

---

## Verification

- ✓ `data_outputs/` now contains exactly the 10-slide deck (PPTX+PDF), its builder, the cinema scroll (PPTX+PDF), the projector HTML, the Foundations Plates PDF, the README, and the per-country / dual-view subfolders. No sibling decks at the active surface.
- ✓ `archive/talk_decks_pre_10slide_2026-05-20/` holds all five archived artefacts (22-slide deck PPTX+PDF, 12-slide deck PPTX+PDF, CompressionPlan.json, three builders, 22-slide SPEAKING_SCRIPT.md) plus a folder-level README.
- ✓ Three READMEs (`CODA-Association/README.md`, `CODAwork2026/README.md`, `data_outputs/README.md`) all drop the "preserved siblings" language and point at the archive folder instead.
- ✓ Stale slide-number references ("slide 18", "slide 19", "slide 20" in the run-the-presentation and standards-conformance contexts) replaced with slide-10-aware language across the README chain. ChatGPT's two flagged stale references fully closed.
- ✓ `archive/README.md` rebuilt with the new section first; the legacy-deck section still references the May-12 / May-13 decks; new section on manuscript-render lineage covers the msprint + LibreOffice archive folders.
- ✓ `VERSION_HISTORY.md` new entry at top of the chronological log documents the trigger, the files moved, the README chain refresh, and the discipline preserved.
- ✓ `POINT_OF_RESTORE_2026-05-19.md` gets a non-destructive 2026-05-20 update note pointing at the archive folder, preserving the restore-point's recoverability.
- ✓ `CONFERENCE_ATTENDEES.md` sibling-deck link replaced with archive-folder link.
- ✓ Grep verification: zero remaining references to "preserved sibling", `CodaWork2026_FinalTalk_2026-05-17` (outside archive/), `CodaWork2026_FinalTalk_12Slide` (outside archive/), or `build_final_talk*.py` (other than `build_final_talk_10slide.py`) at active surfaces.
- ✓ The manuscript working copy at `CODAwork2026/Compositional_Monitoring_2026.{docx,pdf}` is untouched and still byte-identical to the canonical (manuscript working-copy correction from earlier today preserved).

---

## Post-commit sync (after Peter pushes)

After GitHub Desktop reports the push landed and CI completes:

1. Update `HS_FAST_REFRESH.json` `last_push` field with the actual SHA + CI run number.
2. Add `push_58_completed` entry to `HS_ADMIN.json` with the SHA + CI run.
3. Update top-level `current_commit_sha` / `current_ci_run` / `current_ci_run_name` fields in `HS_FAST_REFRESH.json`; demote push #57 to `previous_*`.
4. Update `PUSHES_INDEX.md` push #58 header line with SHA + CI run.
5. Update `CHANGELOG.md` push #58 row with SHA + CI run.

---

## Why this push exists

Push #57 made the choice — 10 slides — but kept the 22-slide and 12-slide decks in the active surface as "sibling fallbacks" so a future longer slot could fall back to them. ChatGPT's review revealed that the sibling framing was reading as "this repo has three decks on offer" rather than "this repo has one deck and two earlier stages of the same one". The reviewer's read matched what Peter saw: the surface was still confusing.

Push #58 closes that gap. The 10-slide deck stands alone at the active surface. The 22-slide and 12-slide stages are still in the repo, reproducible byte-for-byte, but they live one folder down with a README that explains how each one was superseded by the next. Anyone tracing the lineage of the talk finds every stage intact; anyone trying to pick "the deck" finds exactly one option.

Same input, same output, always. One deck.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.   The AI follows the same protocol.*
