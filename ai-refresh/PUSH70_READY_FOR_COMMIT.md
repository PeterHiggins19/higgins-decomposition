# PUSH #70 — READY FOR COMMIT

**Prepared:** 2026-05-29 · **Push class:** S2 (doc/media only) · **Lockdown window:** 2026-05-12 → 2026-06-06 — compliant.
**Theme (proposed CI name):** *"16:9 Widescreen"* — the conference Presentation switches to PowerPoint widescreen 16:9 (13.333 × 7.5 in, exact 1.778 aspect) so the PDF maps 1:1 onto any 16:9 projector or monitor with no letterboxing; aspect-ratio doctrine codified into the standards companion; speech companion adjusted for one-slide-per-page-side podium use.

Four days before CoDaWork 2026. This push promotes the 16:9 widescreen Presentation as the conference deliverable, codifies the aspect-ratio guidance into the HUF-STD-002 companion doc so it persists as durable practice, and refines the speech companion for double-side print use at the podium. All changes are doc/media — the engine, schemas, INV catalog, and NO-CREATE files remain untouched.

---

## Change groups

**(A) Presentation switches to exact 16:9 widescreen.**
`CODA-Association/CODAwork2026/data_outputs/CodaWork2026_Presentation_2026-05-28.pdf` (3.3 MB, 21 slides, **959.981 × 540 pts = exact 16:9**, 1.7777…). The earlier Letter-landscape canvas (1.294) was letterboxed on 16:9 projectors/monitors; the new 13.333 × 7.5 in canvas (PowerPoint widescreen standard) drops 1:1 onto any 16:9 display with no black bars. Same 21-slide arc and content as the pushed `057177e` deck (deceptive drift defined on first appearance, Germany complete plate set on slides 8–9, two-column nav-chart slides, world finale, CN-TT + projector close); only the canvas aspect changed. The nav-chart slides (7 / 11 / 13), plate slides (8 / 9 + 15–20), and cross-country slide (14) use two-column layouts with side reading panels (country code + descriptor + key metrics at 18–44 pt) to fully use the wider canvas without black bars. Distance-reading fonts: titles 28–38 pt, body 18–22 pt, callouts 20–28 pt, side-panel labels 28–52 pt.

**(B) Aspect-ratio doctrine codified into the standards companion.**
`huf-gov/standards/TENSOR_TRAIN.md` gains a new section **"Presentation rendering — aspect-ratio guidance"** between the existing PPTX-boundary section and the what-HUF-STD-002-adds section. It documents the recommendation (use 16:9 widescreen, render at exact 13.333 × 7.5 in), a display-fit table showing aspect-loss percentages on a 16:9 screen for the common alternatives (16:9 = 0 % · 16:10 ≈ 6 % · A4 landscape ≈ 26 % · 4:3 ≈ 33 % · Letter landscape ≈ 37 %), a when-to-use-what table separating presentation decks (16:9) / engine-output decks (16:10) / manuscripts (Letter / A4 portrait) / projector HTML (viewport-relative), layout consequences (wider/shorter canvas → more horizontal room for two-column layouts, less vertical room for full-canvas figures with aspect ≤ 1.6), distance-reading font ranges, and the worked example. Lockdown-compliant: this is the HUF-STD-002 *companion .md* (S2 doc-only); the JSON schema itself remains untouched.

**(C) POST_CONFERENCE_ROADMAP §5.10 — presentation-format aspect-ratio standard.**
`papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` gains §5.10 *Presentation-format aspect-ratio standard (Tensor-Train companion update, 2026-05-28)* — records the conference-prep lesson learned, cross-references the TENSOR_TRAIN.md section + the CODAwork2026 VERSION_HISTORY entry, and frames the doctrine for post-conference work.

**(D) Speech companion adjustments — page-fit + Terms + slide-14 tables + World observation.**
`CODA-Association/CODAwork2026/SPEAKING_SCRIPT_QA_companion.md` (+ rebuilt `.pdf`, 75 KB, 13 pages Letter landscape). Four refinements:
- One-slide-per-page-side CSS (`page-break-after: avoid` on h2, `page-break-inside: avoid` on the slide table). Adjacent slides group when both fit; a slide that doesn't fit bumps to a fresh page rather than splitting mid-table. Peter intends to double-side print and hold the companion — zero page flips per slide.
- Per-slide *Terms used* italic block in the Q&A bench column — concise dot-separated lists of technical terms used on each slide (PCA / CLR / κ_HS / HLR / ILR-Helmert / etc.). Fill-in glossary for clarification; skippable when time is tight.
- Slide 14 PRESENT (5 of 9) + ABSENT (4 of 9) reference tables in slide-show order — JPN (10) / GBR (12) / AUS (15) / CHN (16) / IND (17) for present; DEU (6, annual) / FRA (18) / USA (19) / WLD (20) for absent. Each row carries a one-line classification reason.
- Slide 20 World uniformity observation appended — *"Notice the Helmsman: uniform across the study window — one largest-motion carrier holds from start to finish. The world as a whole is a smoothly-operating energy system over time; countries absorb the perturbations, the global composition does not flip."*

**(E) Doc-chain sweep — "Letter landscape" → "16:9 widescreen" across the active surfaces.**
Eight surfaces updated: root `README.md` · `CODA-Association/README.md` · `CODA-Association/CODAwork2026/README.md` · `CODA-Association/CODAwork2026/data_outputs/README.md` · `CODA-Association/CONFERENCE_ATTENDEES.md` · `papers/README.md` · `CODA-Association/CODAwork2026/SPEAKING_SCRIPT_QA_companion.md` (masthead) · `PUSH_PROTOCOL.md` (worked-example stat command). All active-surface "Letter landscape" mentions now read "16:9 widescreen." Historical references in archives and dated journal entries left as records.

**(F) Archive entry — `talk_decks_pre_pdfonly_2026-05-28/`.**
New `CODA-Association/CODAwork2026/archive/talk_decks_pre_pdfonly_2026-05-28/` folder with a folder-level README, holding the prior `CodaWork2026_Presentation_2026-05-27.pptx` (3.3 MB) + `.pdf` (2.9 MB) — the last PPTX shipped as a public artifact, archived after Peter's PDF-only directive. The earlier-stage archive folders are untouched.

**(G) VERSION_HISTORY journal entries.**
`CODA-Association/CODAwork2026/VERSION_HISTORY.md` gains the 2026-05-28 entry "Presentation switches to 16:9 widescreen" + a companion-edit sub-entry for the standards-doc addition + a second companion-edit sub-entry for the speech-companion adjustments (this entry). The two earlier 2026-05-28 entries (Letter-landscape layout expansion and v12 full clean-slate rebuild) are flagged as superseded by the 16:9 rebuild.

---

## File manifest

**New:**
- `CODA-Association/CODAwork2026/archive/talk_decks_pre_pdfonly_2026-05-28/` (README.md + moved files below)
- `ai-refresh/PUSH70_READY_FOR_COMMIT.md` (this file)

**Moved → archive/talk_decks_pre_pdfonly_2026-05-28/:**
- `CodaWork2026_Presentation_2026-05-27.pptx` · `.pdf` (from data_outputs/)

**Modified (active deck — replaced in place at same filename):**
- `CODA-Association/CODAwork2026/data_outputs/CodaWork2026_Presentation_2026-05-28.pdf` (rebuilt from Letter-landscape → 16:9 widescreen; same filename, same 21-slide arc, different canvas aspect)

**Modified (docs):**
- `README.md` (root)
- `CODA-Association/README.md`
- `CODA-Association/CONFERENCE_ATTENDEES.md`
- `CODA-Association/CODAwork2026/README.md`
- `CODA-Association/CODAwork2026/data_outputs/README.md`
- `CODA-Association/CODAwork2026/SPEAKING_SCRIPT_QA_companion.md`
- `CODA-Association/CODAwork2026/SPEAKING_SCRIPT_QA_companion.pdf` (rebuilt)
- `CODA-Association/CODAwork2026/VERSION_HISTORY.md`
- `CODA-Association/CODAwork2026/archive/README.md` (archive-index header + new-folder entry)
- `papers/README.md`
- `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` (§5.10 added)
- `huf-gov/standards/TENSOR_TRAIN.md` (new aspect-ratio guidance section)
- `PUSH_PROTOCOL.md` (worked-example stat command updated)
- `CHANGELOG.md` (push #70 row added with pending SHA)

**Deleted (junk):**
- (none — this is a pure doc/media + content-only push)

---

## What this push does NOT touch — lockdown surface

- Engine code: `HCI-CNT/engine/cnt.py` (mtime 2026-05-19, pre-lockdown) · `HCI-CNT/engine/cnt.R` · `HCI-CNQ/engine/cnq.py` · `HCI-CNQ/engine/cnq.R` — all untouched.
- Schemas: `huf-gov/standards/HUF_PUBLICATION_STANDARDS.json` (HUF-STD-001) · `huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json` (HUF-STD-002) · `huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json` (HUF-STD-003) — all untouched. The aspect-ratio guidance lives in the *companion .md* (`TENSOR_TRAIN.md`), not in the schema JSON.
- INV catalog: `ai-refresh/INVESTIGATION_CATALOG.json` — 63 entries (33 CANONICAL / 8 STAGED / 12 DEFERRED / 8 OPEN / 1 FALSIFIED / 1 CLOSED) — unchanged.
- NO-CREATE files: all six remain absent — `huf-gov/standards/HUF_TENSOR_TRAIN_VECTOR_PDF_GENERATOR.py` · `HCI-CNQ/engine/hs_cnq_pdf_exporter.py` · `HCI-CNT/engine/cctt_v1_1.py` · `ai-refresh/CCTT_PILOT_REPORT_v1_1.md` · `CCTT_BUILD_INSTRUCTION_v1_1.json` · `papers/codawork2026/HUF_QFT_PRIMER.md`.
- Manuscript: `CODA-Association/CODAwork2026/Compositional_Monitoring_2026.{docx,pdf}` (v1.3, 2026-05-19) — unchanged.
- Full-corpus reference: `CodaWork2026_CN-TT_Output_2026-05-28.pdf` + `CodaWork2026_PremierDataOutput_2026-05-13.pptx` (editing source) — unchanged.
- Projector v2.2: `data_outputs/codawork2026_projector.html` — unchanged.
- Per-country plates: `data_outputs/per_country_pdfs/` · `per_country_json/cnt_v3/` · `per_country_json/cnq_v2/` — unchanged.

---

## Commit message (proposed)

```
16:9 widescreen

Presentation rebuilt at exact 16:9 (13.333 × 7.5 in, PowerPoint widescreen
standard) so the PDF maps 1:1 onto any 16:9 projector or monitor with no
letterboxing. Same 21-slide arc and content as the pushed 057177e deck;
the canvas aspect is what changed. Two-column layouts on nav-chart slides
(7/11/13), Germany plate slides (8/9), cross-country (14), and world plates
(15-20) — chart on left + side reading panel with country code, descriptor,
and key metrics in distance-reading text on the right. No black bars.

Aspect-ratio doctrine codified into huf-gov/standards/TENSOR_TRAIN.md (the
HUF-STD-002 companion .md): 16:9 widescreen is the general-purpose
presentation format; engine-output decks stay at 16:10; manuscripts and
handouts stay at Letter/A4 portrait; the projector HTML scales natively.
Cross-referenced as POST_CONFERENCE_ROADMAP §5.10.

Speech companion adjusted for podium use: one-slide-per-page-side CSS so
Peter can double-side print and hold without flipping mid-talk; per-slide
"Terms used" italic blocks in the Q&A bench column as fill-in glossary
cues; slide 14 PRESENT (5 of 9) + ABSENT (4 of 9) reference tables in
slide-show order; slide 20 closes with a note that the World shows a
uniform Helmsman — the global system absorbs country-level perturbations.

Doc chain swept across 8 active surfaces ("Letter landscape" -> "16:9
widescreen"). Prior 2026-05-27 PPTX + PDF archived in
talk_decks_pre_pdfonly_2026-05-28/.

S2 doc/media only. Engine code, HUF-STD-001/002/003 JSON schemas, INV
catalog, NO-CREATE files, manuscript, projector v2.2, per-country plates
all untouched. Pre-conference lockdown discipline holds.
```

---

## Post-push §6 sync sequence (after CI lands green)

When Peter reports the commit SHA + CI run number + name + duration:

1. `CHANGELOG.md` row #70 — fill SHA + CI run + name + duration.
2. `HS_FAST_REFRESH.json` — `last_updated` · `current_commit_sha` / `_full` / `_ci_run` / `_ci_run_name` / `_ci_duration_seconds` advance · `previous_*` carry the prior #69 values · `last_push` rewritten with the #70 narrative + chained "Previous: #69 ..." · prior `last_push` value demoted to `previous_pushed_69_was_last_push` · new `push_70_completed` key inserted before `push_69_completed`.
3. `ai-refresh/HS_ADMIN.json` — `last_updated` · new `push_70_completed` entry with full multi-paragraph narrative.
4. `ai-refresh/PUSHES_INDEX.md` — new "Push #70 — *16:9 Widescreen*" deep-detail section above the #69 section.
5. `CODA-Association/CODAwork2026/VERSION_HISTORY.md` — the 2026-05-28 entry "Presentation switches to 16:9 widescreen" header gains "pushed `<SHA>`, CI #<run> "<name>" green <duration>s" + the closing "*Staged for push #70.*" line becomes "*Landed in push #70 — commit <SHA>, CI #<run> "<name>" green <duration>s, <date>.*"

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*Four days before CoDaWork 2026. The Presentation fits the screen; the standards companion remembers why; the speech fits the page.*
