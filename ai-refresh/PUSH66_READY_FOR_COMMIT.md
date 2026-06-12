# PUSH #66 — READY FOR COMMIT

**Prepared:** 2026-05-27 · **Push class:** S2 (doc/media only) · **Lockdown window:** 2026-05-12 → 2026-06-06 — compliant.
**Theme (proposed CI name):** *"Deceptive Drift"* — the single grayscale 19-slide Presentation, named on its subject.

Five days before CoDaWork 2026. This push promotes the single grayscale **19-slide Presentation** as the conference deliverable, archives the 13-slide colour predecessor, streamlines the `CODAwork2026/` folder for direct access to the critical files, and brings every README and support file into agreement — plus the post-#65 working-tree research filings ride along.

---

## Change groups

**(A) New active deliverable — the Presentation.**
`CODA-Association/CODAwork2026/data_outputs/CodaWork2026_Presentation_2026-05-27.pptx` (+ `.pdf`). A single grayscale deck of 19 slides (numbered N / 19): talk (1–12) → rest-of-world finale (13–18) → live-projector close (19). White background, black text, hatched (value + pattern) size-view and Power-Share figures re-plotted from the EMBER CSVs via standard CLR; bigger fonts; rebuilt method diagram. Pure-science terminology — named on **deceptive drift**, defined on first appearance; metaphors removed; bread analogy kept and marked as an analogy. Power-share computation validated against the canonical Germany Solar 2005→2006 = 71.1 %.

**(B) Companion script.**
`CODA-Association/CODAwork2026/SPEAKING_SCRIPT_19slide_QA_companion.md` (+ `.pdf`) — two-column speech + Q&A bench, rewritten to the 19-slide arc + deceptive-drift terminology; ~13 min spoken + ~1 min live close = ~14 min, then 5 min Q&A.

**(C) Archived (lineage, not for use).**
New `archive/talk_decks_pre_presentation_2026-05-27/` with a folder-level README, holding: `CodaWork2026_FinalTalk_13Slide_2026-05-24.pptx`/`.pdf`, `build_final_talk_13slide.py`, `build_final_talk_13slide_v2.py`, `SPEAKING_SCRIPT_13slide.md`, `SPEAKING_SCRIPT_13slide_QA_companion.md`/`.pdf`, `README_package_snapshot_2026-05-20.pdf`.

**(D) Streamlined.**
Deleted junk from `data_outputs/` (`.~lock.CodaWork2026_FinalTalk_13Slide_2026-05-24.pdf#`, `lu3977890.tmp`). `data_outputs/` now presents the critical files directly: the Presentation (pptx + pdf), `codawork2026_projector.html`, the full-corpus reference (`CodaWork2026_PremierDataOutput_2026-05-13.*`), the Foundations plates, and the per-country engine outputs.

**(E) Docs in agreement.**
Promoted the 19-slide Presentation across: `CODAwork2026/README.md` (v2.5 → v2.6), `data_outputs/README.md` (v7.0 → v7.1), `CODA-Association/README.md`, root `README.md`, `papers/README.md`, `CONFERENCE_ATTENDEES.md` (slide-by-slide section rewritten to the 19-slide arc), and `archive/README.md` (index header + new-folder entry). AI-Use-Declaration references moved slide 13 → slide 19; projector SHOCK descriptions updated to the v2.2 year-label chromatic-opposite behaviour. Two `VERSION_HISTORY.md` entries added (the Presentation overhaul + the earlier attractor/Ramsar journal entry).

**(F) Carry-along research filings (post-#65 working tree).**
`papers/in_progress/ATTRACTOR_MORPHOLOGY_AND_TRANSCENDENTAL_BASINS.md` (new), `papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md` (new), `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` §4.12 (attractor morphology) + §5.9 (Ramsar wetlands). Post-conference candidate work; doc-only.

---

## File manifest

**New:**
- `CODA-Association/CODAwork2026/data_outputs/CodaWork2026_Presentation_2026-05-27.pptx` · `.pdf`
- `CODA-Association/CODAwork2026/SPEAKING_SCRIPT_19slide_QA_companion.md` · `.pdf`
- `CODA-Association/CODAwork2026/archive/talk_decks_pre_presentation_2026-05-27/` (README.md + moved files below)
- `papers/in_progress/ATTRACTOR_MORPHOLOGY_AND_TRANSCENDENTAL_BASINS.md`
- `papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md`
- `ai-refresh/PUSH66_READY_FOR_COMMIT.md` (this file)

**Moved → archive/talk_decks_pre_presentation_2026-05-27/:**
- `CodaWork2026_FinalTalk_13Slide_2026-05-24.pptx` · `.pdf` (from data_outputs/)
- `build_final_talk_13slide.py` · `build_final_talk_13slide_v2.py` (from data_outputs/)
- `SPEAKING_SCRIPT_13slide.md` · `SPEAKING_SCRIPT_13slide_QA_companion.md` · `.pdf` (from CODAwork2026/ root)
- `README_package_snapshot_2026-05-20.pdf` (was data_outputs/`README package.pdf`)

**Deleted (junk):**
- `data_outputs/.~lock.CodaWork2026_FinalTalk_13Slide_2026-05-24.pdf#`
- `data_outputs/lu3977890.tmp`

**Modified (docs):**
- `CODA-Association/CODAwork2026/README.md`
- `CODA-Association/CODAwork2026/data_outputs/README.md`
- `CODA-Association/README.md`
- `CODA-Association/CONFERENCE_ATTENDEES.md`
- `README.md` (root)
- `papers/README.md`
- `CODA-Association/CODAwork2026/archive/README.md`
- `CODA-Association/CODAwork2026/VERSION_HISTORY.md`
- `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md`
- `CHANGELOG.md` (#66 row, pending SHA)

---

## Lockdown compliance (S2 doc/media)

Untouched: engine code (`cnt.py` 2026-05-19, `cnt.R`, `cnq.py`, `cnq.R`), schemas (HUF-STD-001/002/003), INV catalog dispositions (63: 33C/8S/12D/8O/1F/1C), the six NO-CREATE files (all remain absent), the manuscript, the full-corpus reference deck, the projector HTML, and the per-country engine plates. Every change is within the authorized conference-prep + `papers/in_progress/` surfaces.

**Known residual (out of scope, post-lockdown):** the trajectory plate images on slides 7/9/11 and the finale carry the engine's internal `course_directness` / `System Course Plot` labels baked into the rendered PNGs; the slide captions around them already use the science terms ("trajectory directness"). Relabeling the plates is post-conference engine work.

---

## Post-commit sync (after the SHA + CI land) — PUSH_PROTOCOL §6

1. `HS_FAST_REFRESH.json` — `last_push` + `push_66_completed` + `previous_last_push` + `last_updated`, and `_meta.current_commit_sha`.
2. `ai-refresh/HS_ADMIN.json` — `push_66_completed` entry.
3. `ai-refresh/PUSHES_INDEX.md` — Push #66 deep-detail section + parity-table row + file manifest.
4. `CHANGELOG.md` — fill the `(pending)` SHA + CI run + duration in the #66 row.
5. `VERSION_HISTORY.md` — already carries the 2026-05-27 Presentation entry (working-state); annotate with the landed SHA on sync.

---

*Prepared for Peter's review and push. S2 doc/media, lockdown-compliant. Five days to Coimbra.*
