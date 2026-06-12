# PUSH #57 — READY FOR COMMIT

**Date:** 2026-05-20
**Status:** HOLD cleared — ready for Peter to commit via GitHub Desktop.
**Suggested CI name:** `Talk deck compression — 10-slide final`
**Suggested commit message:**

```
Talk deck compression — 22 → 10 slides

The 10-slide compressed final-talk deck becomes the conference talk.
Built from a ChatGPT-prepared compression plan plus a final pass that
drops the MC-4 falsifiability slide and the "Inspect the instrument"
closer; all contact details move onto slide 1.

Story arc (10 slides):
  1.  Title + question + full contact
  2.  Size view hides the work (USA Solar 760× hook)
  3.  Five viewpoints, one observable stack
  4.  Activation Coefficient — the yeast factor
  5.  Three archetypes overview (DEU / JPN / GBR)
  6.  Germany — continuous arc                    (75 sec)
  7.  Japan — shock + reorganisation              (75 sec)
  8.  UK — regime change                          (75 sec)
  9.  5-of-9 cross-country signature
 10.  What the stack answers (synthesis + AI Use Declaration footer)

Timing: ~8 min spoken + 1.5 min cinema scroll + 1 min projector demo
= ~10.5 min apparatus time, ~4.5 min Q&A in a 15-min slot.

Files in this commit:
  New (primary):
    CODA-Association/CODAwork2026/data_outputs/
      CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx
      CodaWork2026_FinalTalk_10Slide_2026-05-20.pdf
      build_final_talk_10slide.py
    CODA-Association/CODAwork2026/SPEAKING_SCRIPT_10slide.md

  New (preserved siblings — time-budget fallbacks):
    CODA-Association/CODAwork2026/data_outputs/
      CodaWork2026_FinalTalk_12Slide_2026-05-20.pptx
      CodaWork2026_FinalTalk_12Slide_2026-05-20.pdf
      build_final_talk_12slide.py
      CodaWork2026_FinalTalk_12Slide_CompressionPlan.json

  Refreshed (README chain):
    CODA-Association/README.md
    CODA-Association/CONFERENCE_ATTENDEES.md
    CODA-Association/CODAwork2026/README.md
    CODA-Association/CODAwork2026/data_outputs/README.md  (v5.0)
    CODA-Association/CODAwork2026/VERSION_HISTORY.md      (+entry)

  Admin:
    HS_FAST_REFRESH.json                last_push → #57 HOLD
    ai-refresh/HS_ADMIN.json            push_57_prepared
    ai-refresh/PUSHES_INDEX.md          push #57 section
    ai-refresh/PUSH57_READY_FOR_COMMIT.md
    CHANGELOG.md                        push #57 row

Preserved untouched (the original 22-slide deck stays as a sibling):
    CODA-Association/CODAwork2026/data_outputs/
      CodaWork2026_FinalTalk_2026-05-17.pptx
      CodaWork2026_FinalTalk_2026-05-17.pdf

Lockdown-compliant S2 doc-only. Engine code, schemas, INV catalog
dispositions, NO-CREATE files, papers/codawork2026/talk/, and the
cinema scroll + projector + per-country plates all untouched.

Rationale (Peter's directive):
  "this gives me breathing room and time to talk and not manage
   slides and juggle media too much, make this all seamless,
   simplify and make sense not confusion."

The 10-slide deck collapses six slides' worth of separable teaching
beats into the case studies and the synthesis. The repo and the
manuscript carry the rest. The instrument reads. The expert decides.
The hashes carry the receipts. The vocabulary holds the line.
The AI follows the same protocol.
```

---

## Verification

- ✓ 10-slide PPTX renders to a single A4 landscape page per slide; PDF companion exported via LibreOffice.
- ✓ Slides 6/7/8 image-height constraint verified — manuscript figure footers no longer overlap the gold stat lines.
- ✓ Slide 1 contact block reads: name, email (`PeterHiggins@RogueWaveAudio.com`), repo URL, community folder, UN-6 handout availability, doctrine line.
- ✓ Slide 10 closing carries the AI Use Declaration (HUF-STD-001 v1.1 compliance — previously on the old slide 12).
- ✓ `SPEAKING_SCRIPT_10slide.md` timing budget verified: 25 + 50 + 35 + 45 + 20 + 75 + 75 + 75 + 60 + 40 = 500 sec ≈ 8 min 20 s.
- ✓ `CONFERENCE_ATTENDEES.md` slide-by-slide block rewritten; all manuscript-section links, figure references, and per-country JSON/PDF pointers preserved and redistributed across the new 10-slide structure.
- ✓ The three preserved deck siblings (22-slide, 12-slide intermediate, 10-slide primary) are explicitly called out in every README so a future reader does not delete any of them.
- ✓ `papers/codawork2026/talk/SPEAKER_BRIEF.md` (with the locomotive-metaphor closing-line option) was modified in push #55 and remains valid for the 10-slide deck — no changes needed.

---

## Post-commit sync (after Peter pushes)

After GitHub Desktop reports the push landed and CI completes:

1. Update `HS_FAST_REFRESH.json` `last_push` field with the actual SHA + CI run number.
2. Add `push_57_completed` entry to `HS_ADMIN.json` with the SHA + CI run.
3. Update top-level `current_commit_sha` / `current_ci_run` / `current_ci_run_name` fields in `HS_FAST_REFRESH.json`; demote push #56 to `previous_*`.
4. Update `PUSHES_INDEX.md` push #57 header line with SHA + CI run.
5. Update `CHANGELOG.md` push #57 row with SHA + CI run.

---

## Why this push closes the deck question

For the past two days the repo has been carrying *three* candidate decks side-by-side (22-slide, 12-slide, 10-slide), each appropriate for a different time slot. Push #57 makes the choice — the 10-slide deck is the conference talk. The other two stay in the repo as sibling files because every README in the chain explicitly preserves them, but the speaking script, the attendee follow-along, the version history, and the README pointers all converge on the 10-slide structure.

That is the seamless surface Peter asked for: one deck to walk in with, one speaking script to rehearse from, one attendee page to share, one timing budget to trust. Cinema scroll and projector are still ready for Q&A. The manuscript still carries MC-4 and the longer-form falsifiability frame. The longer-form decks are still there if a slot ever opens up.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.   The AI follows the same protocol.*
