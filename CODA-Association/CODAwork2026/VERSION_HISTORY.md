# Version History — CODA-Association/CODAwork2026 media

**Purpose.** Tracks all version changes to documents and media in this folder. Each entry names the affected file, its new version, the change summary, and the change date. Authoritative version of any document is whatever VERSION_HISTORY records as the most recent for that file.

**Versioning convention.**
- **Major version** (e.g. 1.0 → 2.0): substantive content change — new beats, new claims, retracted material, structural reorganization.
- **Minor version** (e.g. 1.0 → 1.1): clarifications, corrections, additions to existing content, updates that reflect new repository state without changing the core argument.
- **Patch version** (e.g. 1.0 → 1.0.1): typo and link fixes only.

**Stable filenames.** Filenames do not change with version. The version number lives in the document header and in this log. Slide deck file may include a date stamp in the filename for archival clarity.

---

## 2026-05-28 — Presentation switches to 16:9 widescreen (v13/v14): exact match to projector / monitor displays (post-#69 working tree, S2 doc/media only)

*Per Peter, 2026-05-28: "ok i figured out what is happening — the CodaWork2026_CN-TT_Output_2026-05-28.pdf file is actually on 16 in by 10 inch paper then scaled for view to 69% and fits the screens with 16:9 perfectly... can the same be done for the 21 slide presentation to make it utilize the full screen. this time it should work as now it make sense what is happening, the 16:10 scale fits 16:9 screens very well, perhaps design to 16:9 for the paper scaling to get an exact perfect display."*

**Root-cause analysis.** The earlier 2026-05-28 rebuilds were on **Letter landscape (11 × 8.5, aspect 1.294)**. On a modern 16:9 projector or monitor (aspect 1.778), Letter landscape gets letterboxed: the PDF viewer adds black bars on the top and bottom (or sides) because the page aspect doesn't match the display aspect. Peter noticed that the CN-TT Output PDF (which is **16 × 10 inches, aspect 1.60**) fits 16:9 screens nearly perfectly — only thin bars — because 1.60 is much closer to 1.778. The fix is to take the Presentation all the way to **exact 16:9** so a 16:9 display shows the slide edge-to-edge with no letterboxing at all.

**Canvas.** Switched from `11 × 8.5` to **`13.333 × 7.5` inches** — the PowerPoint widescreen standard, exact 16:9 (1.7777…). Rendered PDF is **959.981 × 540 pts (16:9)**. Drops 1:1 onto any 16:9 display.

**Builder.** `outputs/combined_build/build_v14_final.py` in the workspace scratchpad. PPTX is an intermediate; only the PDF is placed in the repo.

**Per-slide layout grid (16:9, 13.333 × 7.5).** Tight margins (0.18 in left/right). Title strip y=0.15, h=0.62 (font 28); subtitle y=0.80, h=0.34 (font 16); content area y=1.18 to y=6.95 (5.77 in tall); footer y=7.05, h=0.30.

| Slide | Subject | Layout |
|---|---|---|
| 1 | Title + contact | Centered text stack, large hierarchy (title 38 pt, byline 26 pt, contact 22 pt). |
| 2 | Size view hides the work | Two columns 6.25 in each (wider canvas → roomier columns), full-width emphasis bar bottom. |
| 3 | Method diagram | **Two-column** — `fig1_method.png` at width 8.40 in on the left + "FIVE READINGS" labeled list at 20 pt + descriptors on the right. The wider canvas gives the diagram and the readings their own real estate side by side. |
| 4 | Activation Coefficient | Centered formula band (26 pt Consolas) + 3 regime lines at 22 pt + worked-example block at 22 pt. |
| 5 | Three archetypes | Three columns 4.20 in each (more room than Letter-landscape gave) — country name 28 pt, descriptor 17 pt italic, body 19 pt. |
| 6 / 10 / 12 | Share-and-work (hatched) | Figure at width ~9.00 (aspect 1.857, height 4.85) centered, captions below. The intrinsic 1.857 aspect is only ~4% wider than the 1.778 canvas, so figures end up centred with a small symmetric framing (≤ 2 in each side). |
| **7 / 11 / 13** | **Nav-chart trajectories** | **Two-column** — chart at 7.12 × 5.50 on the left + side reading panel on the right with HUGE country code (44 pt: DEU / JPN / GBR), descriptor (22 pt: continuous arc / loop and reorganise / jump and return), pattern label (16 pt italic), and five key metric lines (18 pt). **No black bars** — the right panel fills exactly the space the chart's aspect ratio leaves. |
| 8 / 9 | Germany complete plate set | **Two-column** — plate image at width 9.04 in (aspect 1.6, height 5.65) on the left + side reading panel on the right with country code at 44 pt and 6 takeaway lines. The plate has the engineer-grade metric panel built in; the external side panel gives the distance-reading version. |
| **14** | **Cross-country (5 of 9)** | **Two-column** — `fig5_crosscountry.png` at width 6.39 in on the left + right panel with **52 pt "5 of 9"** + PRESENT / ABSENT country lists at 22 pt. |
| 15–20 | Rest of world (6 plates) | Two-column plate + side panel matching 8 / 9. Each side panel carries the country code + present/absent state + one-line takeaway. |
| 21 | Close | Five WHAT / WHO / WHEN / HOW MUCH / WHY rows at 26 / 20 / 19 pt spanning full width; live-close cue line names the CN-TT Output PDF (30 s) + projector (30 s). |

**The aspect-fit doctrine, written down.** A presentation PDF and its display device are coupled by *aspect ratio*. If the PDF is 1.294 (Letter landscape) and the screen is 1.778 (16:9), the viewer letterboxes. The fix is to author the PDF at the display's aspect; then the PDF fills the screen edge to edge. The CN-TT Output's accidental 16:10 (1.60) fits 16:9 well because it's close. The Presentation's exact 16:9 (1.778) fits 16:9 perfectly. Going forward, Presentation = 16:9; CN-TT Output stays 16:10 because re-rendering 325 engine plates is out of scope. The projector (HTML, browser-scaled) fits any aspect natively.

**Doc chain.** Filename unchanged (`CodaWork2026_Presentation_2026-05-28.pdf`) and the PDF-only convention is unchanged, so the README chain swept in the earlier 2026-05-28 entry remains accurate. The descriptions in the README chain that say "Letter landscape" should be revised in the next sweep to "16:9 widescreen" — flagged here for the push #70 surface check.

**Lockdown discipline.** S2 doc/media only. Engine code, schemas, INV catalog, NO-CREATE, manuscript, projector v2.2, per-country plates all untouched. Same 21-slide content arc; the *canvas aspect* is what changed. The two prior 2026-05-28 entries (the Letter-landscape layout expansion and the v12 full canvas-fill rebuild) are superseded by this 16:9 rebuild.

*Staged for push #70.*

### Companion edit — 2026-05-28: presentation-format guidance written into the standards companion

Per Peter's directive that "16:9 widescreen is the general use case for presentation formats" should live in one of the standards documents, the aspect-ratio doctrine is codified as a new section in `huf-gov/standards/TENSOR_TRAIN.md` (the HUF-STD-002 companion .md — the HUF-STD-002 JSON schema itself is locked under the pre-conference lockdown, but the companion documentation is S2 doc-only and editable). New section: **"Presentation rendering — aspect-ratio guidance"** between the existing "PPTX boundary" section and the "What was already there vs what HUF-STD-002 adds" section. It documents:

- The headline recommendation: use 16:9 widescreen (13.333 × 7.5 in, PowerPoint widescreen standard, exact 1.7777…) as the general-purpose presentation format so a PDF maps 1:1 onto any 16:9 projector or monitor with no letterboxing.
- The display-fit table showing the loss percentages for the common alternatives (16:10, Letter landscape, 4:3, A4 landscape) — Letter landscape at 1.294 loses ~37 % of display area to top/bottom bars on a 16:9 screen, which is the lesson the CoDaWork 2026 prep arc learned the hard way.
- The when-to-use-what table separating presentation decks (16:9), engine-output decks (16:10 — CN-TT Output stays at its existing aspect because re-rendering 325 plate pages is not S2 work), manuscripts/handouts (Letter / A4 portrait — print, not projection), and HTML projectors (viewport-relative — scales natively).
- The layout-consequences subsection noting that a 16:9 canvas is wider and shorter than Letter landscape: more horizontal room for two-column layouts; less vertical room for full-canvas figures with aspect ≤ 1.6, which therefore get paired with side reading panels. Distance-reading font ranges named (titles 28–38 pt, body 18–22 pt, callouts 20–28 pt, side-panel labels 28–52 pt).
- The worked example: this Presentation PDF at `CodaWork2026_Presentation_2026-05-28.pdf` (959.981 × 540 pts, exact 16:9) + the v14 build script.

Cross-reference also added to `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` as §5.10 — "Presentation-format aspect-ratio standard (Tensor-Train companion update, 2026-05-28)" — recording the conference-prep lesson learned alongside the other §4–§5 application/standards entries.

**Lockdown discipline.** Both edits are S2 doc-only on companion-markdown surfaces — the HUF-STD-001/002/003 JSON schemas remain untouched. The aspect-ratio doctrine is a presentation-rendering practice, not a schema change.

*This sub-entry also stages for push #70.*

### Companion edit — 2026-05-28: speech companion adjustments (page-fit + Terms + slide-14 tables + World observation)

Per Peter, four targeted refinements to `SPEAKING_SCRIPT_QA_companion.md` (+ rebuilt `.pdf`, 75 KB, 13 pages Letter landscape):

1. **One-slide-per-page-side rule.** New CSS in the build pipeline (`outputs/combined_build/` rebuild step): `h2 { page-break-after: avoid }` keeps the slide heading attached to its table, `h2 + table { page-break-inside: avoid }` keeps the whole slide block on one page. Adjacent slides naturally group when both fit on a single page (e.g. slides 7 + 8 now share page 5); a slide that won't fit on the current page bumps to the next page rather than splitting mid-table. Peter intends to double-side print and hold the companion while talking — zero page flips during a single slide's talk is now the discipline.
2. **Per-slide "Terms used" italic block** at the bottom of each Q&A bench column. Concise dot-separated lists of the technical terms used on each slide (e.g. slide 7 = *PCA · CLR trajectory projected by PCA · PC1 / PC2 · course directness (= net distance ÷ path length) · h_S · h_F · HLR (Higgins Log-Ratio) · V_net = h_F − h_S · dynamic range · Reading guide*; slide 8 = *Section plate · t = 13 · D = 9 carriers · N = 26 readings · pairs = 36 · Hˢ · Ring · E_metric · κ_HS · ω · d_A · Helm · Helm d · DR · DR ratio · XY plan · XZ bearings · YZ CLR · CLR plan view*). These are fill-in glossary cues for clarification IF the audience needs more depth — not part of the main speech; can be skipped if time is short. Bug caught and fixed during QA: an initial regex prefix-match assigned slide 1's terms to slides 10–14 + slide 21 (because `## Slide 1` is a prefix of `## Slide 10`, `## Slide 11`, etc.); fixed with a strict numeric-section match.
3. **Slide 14 — PRESENT / ABSENT reference tables in slide-show order.** In the speech column on slide 14 (cross-country corpus summary), two compact inner tables replace the previous prose. **PRESENT (5 of 9)** in slide-show order: JPN (10) · GBR (12) · AUS (15) · CHN (16) · IND (17), each row carrying a one-line *why drift fires* reason. **ABSENT (4 of 9)** in slide-show order: DEU (6, annual) · FRA (18) · USA (19) · WLD (20), each row carrying a *why absent* reason. Compact inner-table CSS (9.5 pt body, 2 pt padding) keeps slide 14 on one page side.
4. **Slide 20 — World uniformity observation appended.** At the end of the World line: *"Notice the Helmsman: uniform across the study window — one largest-motion carrier holds from start to finish. The world as a whole is a smoothly-operating energy system over time; countries absorb the perturbations, the global composition does not flip."* Written in italics so the speaker can read it or skip it depending on time. The observation lands on the slide where it makes immediate sense and is consistent with what the aggregate trajectory shows.

**Build provenance.** Source: `SPEAKING_SCRIPT_QA_companion.md` (644 lines). Pipeline: pandoc → HTML → weasyprint. Output: 13 pages Letter landscape, 75 KB. The masthead `**Deck:**` line was already updated for the 16:9 widescreen Presentation in the parent entry above; no further README-chain sweep needed for this edit.

**Lockdown discipline.** S2 doc/media only on `CODAwork2026/` companion surfaces; engine, schemas, INV catalog, NO-CREATE, manuscript, projector v2.2, per-country plates untouched.

*This sub-entry also stages for push #70.*

---

## 2026-05-28 — Presentation full clean-slate rebuild (v12): PDF-only, Letter landscape, full canvas fill, no black bars (post-#69 working tree, S2 doc/media only)  *[superseded by the 16:9 rebuild above — the canvas was still Letter landscape, so 16:9 displays still letterboxed]*

*Per Peter, 2026-05-28: "i believe multiple rewrites and scaling and moving between PowerPoint and pdf have taken a toll on the aspect ratio and content of the presentation, please generate a complete new presentation set of 21 plates ... generated to utilize full 11 inch wide by 8.5 inch tall letter paper output standard landscape pdf, big job but the more i practice and test the presentation the more i see the need to have fast response and full size diagrams and text without black bars and wasted space."*

**This entry supersedes the earlier 2026-05-28 layout-expansion entry below** — that rebuild's incremental layout fixes (margins 0.5 → 0.4, figure widths bumped) were not enough; multiple iterations had left residual aspect-ratio artifacts and side black bars on the nav-chart slides (7, 11, 13) and the cross-country slide (14). A **complete clean-slate redo** replaces it. Same 21-slide arc, same content, same five named readings, same deceptive-drift terminology — but every slide redesigned from the ground up for the Letter-landscape canvas with no residual width-vs-aspect compromises.

**Builder:** `outputs/combined_build/build_v12_final.py` (workspace scratchpad). Output: `data_outputs/CodaWork2026_Presentation_2026-05-28.pdf` (3.3 MB, 21 pages, 792 × 612 pts Letter landscape).

**(A) Design philosophy.** Tight margins (0.25 in left/right, 0.20 in top/bottom). Content width 10.50 in, content height ~7.0 in (after 0.92 in title strip + 0.30 in footer). Every figure fills as much of the canvas as its intrinsic aspect ratio allows. Fonts scaled aggressively for distance reading.

**(B) Per-slide layout grid.**

| Slide | Subject | Layout |
|---|---|---|
| 1 | Title + contact | Centered text stack, large hierarchy (title 38 pt, byline 26 pt, contact 22 pt). |
| 2 | Size view hides the work | Two columns 5.0 in each — left narrative, right Germany-Solar metrics + callout — full-width emphasis bar bottom. |
| 3 | Method diagram | `fig1_method.png` at full canvas width (10.50 in, height 6.50 in via aspect 1.5625). |
| 4 | Activation Coefficient | Formula centered (Consolas 24 pt), three regime lines at 22 pt, worked-example table 22 pt Consolas. |
| 5 | Three archetypes | Three columns 3.40 in each (Germany / Japan / UK) with country name at 28 pt + descriptor + body 20 pt. |
| 6 / 10 / 12 | Share-and-work (hatched) | Figures at full canvas width 10.50 in (aspect 1.857 → height 5.66 in). |
| **7 / 11 / 13** | **Nav-chart trajectories** | **Two-column** — chart at 7.20 in wide on the left + side reading panel on the right (3.10 in wide) with **HUGE country code** (44 pt: DEU / JPN / GBR), descriptor (22 pt: continuous arc / loop and reorganise / jump and return), pattern label (17 pt italic), and five key metric lines (18 pt). **Eliminates the side black bars that the centered-with-margin v11 had.** |
| 8 / 9 | Germany complete plate set | Plate images at 10.40 in wide (aspect ~1.6, height 6.50 in). |
| **14** | **Cross-country (5 of 9)** | **Two-column** — `fig5_crosscountry.png` at 6.80 in wide on the left + right panel with **48 pt "5 of 9"**, PRESENT / ABSENT country lists at 22 pt — no side black bars. |
| 15–20 | Rest of world (6 plates) | Plate images at 10.40 in wide. |
| 21 | Close | Five WHAT/WHO/WHEN/HOW MUCH/WHY rows at 28/22/20 pt across full width; live-close cue line names CN-TT Output PDF (30 s) + projector (30 s). |

**(C) The black-bar fix in detail.** The previous version's nav-chart slides centered a 7.30 in figure on the 11 in canvas, leaving 1.85 in of empty margin on each side. The new two-column layout pairs a 7.20 in chart on the left with a 3.10 in reading panel on the right — the right panel carries the trajectory's key reading IN LARGE TEXT (44 pt country code + 22 pt descriptor + 18 pt metric lines), giving the audience the distance-friendly version of what the chart's built-in metric panel says in small engine-output font. Slide 14 (cross-country) gets the same treatment: figure on the left, a giant "5 of 9" + present/absent country lists on the right.

**(D) Layout-overflow fixes verified in QA** (all 21 slides rendered to JPGs and inspected): the α formula on slide 4 fits one line at 24 pt; the Activation-Coefficient Consolas line on slide 2 fits one line at 17 pt; all captions on case-study slides 7, 10, 11, 13 read in a single line; no caption-into-figure overlaps; all footer labels and slide-of-total markers clean.

**(E) Doc chain.** No additional sweep needed in this entry — the file path remains `CodaWork2026_Presentation_2026-05-28.pdf` (unchanged from the earlier 2026-05-28 layout-expansion rebuild that also lives at this filename). The earlier rebuild's doc-chain updates (six surfaces swept for PDF-only delivery + the 2026-05-27 → 2026-05-28 rename) already cover this redo. The archived `talk_decks_pre_pdfonly_2026-05-28/` folder still holds the prior 2026-05-27 PPTX + PDF as the pre-rebuild lineage; the intermediate v11 PDF (also at 2026-05-28) is overwritten by this v12 PDF since the filename did not change and the content is the same arc — only the layout is materially better.

**Lockdown discipline.** S2 doc/media only. Engine code, schemas, INV catalog, NO-CREATE, manuscript, projector v2.2, per-country plates all untouched. The PDF *content* (21-slide arc, deceptive-drift definition, hatched figures, named methods, CN-TT + projector close) is identical to the prior 2026-05-28 deck; only the *layout footprint* is materially different (full-canvas fill, two-column nav and cross-country slides, larger distance-reading fonts).

*Staged for push #70.*

---

## 2026-05-28 — Presentation switches to PDF-only, Letter landscape, layout expanded (post-#69 working tree, S2 doc/media only)  *[superseded by the v12 clean-slate rebuild above]*

*Per Peter, 2026-05-28: "i have worked out that the best format is pdf letter size and landscape. the PowerPoint can be archived and no more PowerPoint, only pdf, the complications with PowerPoint software make pdf just that much easier and faster to work with. regenerate to utilize the expanded width real estate and make the slide even better to see at a distance now with 25% more width space, pdf landscape matches the full frame of the display much better as well giving a full performance."*

Two coordinated change groups land together; same 21-slide arc and content (no story changes), but the delivery format and the layout footprint are both rebuilt.

**(A) PDF-only delivery.** The 21-slide grayscale Presentation is now shipped as a **single PDF, Letter landscape (11 × 8.5 in)**: `data_outputs/CodaWork2026_Presentation_2026-05-28.pdf` (3.3 MB). The previous PPTX + PDF (`CodaWork2026_Presentation_2026-05-27.{pptx,pdf}`, last public PPTX) have been moved into `archive/talk_decks_pre_pdfonly_2026-05-28/` with a folder-level README documenting the lineage. The build workflow continues to use python-pptx as an internal scaffold (the v11b builder lives in the workspace scratchpad, not in the repo) and immediately converts to PDF via headless LibreOffice; only the PDF is placed in the repo. Rationale: the PPTX surface introduces a software-compatibility dependency at the conference (PowerPoint version, font availability, ligature handling); the PDF avoids all of that — frame-perfect rendering anywhere a PDF reader runs.

**(B) Layout expanded to fully use the Letter-landscape canvas.** Same canvas as before (11 × 8.5 in — the prior PPTX was already Letter landscape), but the v10 layout under-used the available width on multiple slides (e.g., the nav-chart trajectory slides centered a 7.0 in figure with 2.0 in side margins; the cross-country bar set was 5.7 in wide with 5.3 in unused). v11 tightens margins from 0.5 in to 0.4 in (content width 10.00 → 10.20 in) and bumps figure widths to take the full available real estate: the method diagram on slide 3 goes 9.80 → 10.20 in (+4 %); the hatched share-and-work figures on slides 6 / 10 / 12 go 9.60 → 10.20 in (+6 %); the world-plate and Germany-plate trajectories on slides 8 / 9 / 15–20 go 8.50 → 9.50 in (+12 %); the nav-chart trajectories on slides 7 / 11 / 13 go 7.00 → 7.30 in (+4 %, content-bounded by aspect ratio against caption space); the cross-country bar set on slide 14 goes 5.70 → 6.00 in (+5 %, content-bounded). Fonts scaled up ~20 % throughout for distance reading — title strip 30 → 34 pt, body text 15–17 → 17–19 pt, callout text 17–18 → 19–22 pt, footer slide-of-total 15 → 17 pt. Two layout-overflow fixes verified in QA: the α formula on slide 4 (font 28 → 22 to fit one line at the new width); the Activation-Coefficient Consolas line on slide 2 (font 19 → 17 to fit one line at the new width). Two caption-overflow fixes (cleaner one-line reads): slide 7 caption "Trajectory directness 0.41 (end-to-end distance ÷ path length) — a continuous arc toward the renewable vertex." → "Trajectory directness 0.41 — a continuous arc toward the renewable vertex." (the parenthetical math definition moves into the verbal delivery); slide 10 caption "Aitchison distance (distance on the simplex) 2011 → 2012 ≈ 3 × the baseline step · 17 Helmsman flips" → "Aitchison distance 2011 → 2012 ≈ 3 × the baseline step · 17 Helmsman flips on the corpus" (defines "on the corpus" as the Helmsman-flip-count scope). Visual QA: all 21 slides rendered to JPGs and inspected — no overlaps, no truncations, no off-page text, no caption-into-figure crashes; slide 21 close still names both CN-TT Output PDF (30 s) + projector (30 s) per push #69.

**(C) Doc chain swept** for the rename (2026-05-27 → 2026-05-28) and the PDF-only convention:

- `CODAwork2026/README.md` — Piece 1 table row, folder-layout block (drops PPTX line + adds the new archive folder), how-to-run step 1.
- `CODAwork2026/data_outputs/README.md` — Piece 1 file listing (PPTX line removed; the PDF gets the size + layout-expansion description), how-to-run step 1, Lineage block (now records six stages, latest being the PDF-only + expanded-layout switch).
- `CODA-Association/README.md` — folder-layout block (drops PPTX line; adds the new archive folder), What-is-current piece 1.
- root `README.md` — CoDaWork-deliverables table: two rows (Presentation .pptx + Presentation .pdf) collapse into one row (Presentation PDF-only, Letter landscape).
- `CONFERENCE_ATTENDEES.md` — 🎞 Presentation row updated (PDF only; rename note; layout-expansion note).
- `papers/README.md` — conference-distribution callout pointer updated to the PDF.
- `archive/README.md` — header banner updated (active deck is now the 2026-05-28 PDF); new `talk_decks_pre_pdfonly_2026-05-28/` section added at the top of the folder-layout block.
- `SPEAKING_SCRIPT_QA_companion.md` — masthead `**Deck:**` line updated. Source `qa_companion_21.md` synced; `SPEAKING_SCRIPT_QA_companion.pdf` rebuilt via pandoc → HTML → weasyprint (~69 KB landscape Letter), placed in the repo.

**Lockdown discipline.** S2 doc/media only — no engine, schema, INV catalog, NO-CREATE, or locked-surface edits. The PDF content (21-slide arc, deceptive-drift terminology, hatched figures, named methods, CN-TT close + projector close) is identical to the 2026-05-27 deck; only the delivery format changed (PDF-only) and the layout footprint expanded.

**Discipline note.** Switching the deck to PDF-only mirrors the doctrine already established for the projector (single self-contained HTML file, no build step, runs anywhere a browser runs) and for the UN-6 handouts (PDF deliverables, markdown sources). The conference packet is now three artifacts, three formats, each chosen for the medium: the Presentation runs as a PDF on any laptop, the projector runs as HTML in any browser, the handouts print as PDF in any locale. No platform lock-in.

*Staged for push #70.*

---

## 2026-05-28 — CN-TT Output promoted to public face + new 30s+30s close (post-#68 working tree, S2 doc/media only) — pushed `76d2eb2`, CI #65 "CodaWork2026_CN-TT_Output" green 49s

*Per Peter: "the below document has been renamed and added back to the codawork2026 repo public face as it is the raw data needed to show what data originates all analysis downstream including manual verification plate by plate, a must in the huf system. my intention is to flash through at the end to show the movie like movement of the data points on the stage 1 plates, 30 second of this and 30sec of the html."*

**The full-corpus 325-page PDF (formerly `CodaWork2026_PremierDataOutput_2026-05-13.pdf`) is now promoted to the public face under a new framework-aligned name: `CodaWork2026_CN-TT_Output_2026-05-28.pdf` (CN-TT = CNT / Tensor Train, per HUF-STD-002 Tensor Train I/O Standard).** It is the raw-data provenance artifact for every claim in the talk — master cover + 9 country sections × 6 plates each (Stage 0 Foundations · Stage 1 Section · Stage 1 ILR-Helmert Triplet · Stage 2/3 · CNQ). Manual plate-by-plate verification is a HUF-system requirement; this is where a reviewer does it. The PPTX editing source is kept at its original `CodaWork2026_PremierDataOutput_2026-05-13.pptx` name; the prior-name PDF stays in `data_outputs/` for now (byte-identical content, just superseded as the public-face artifact).

**The talk's close is now a 30 sec + 30 sec two-step.** The previous "~1 min live HTML close" becomes: (1) **30 sec CN-TT Output PDF flash-through** of the Stage 1 plates at ~1 sec/page — the data points move on the simplex frame-by-frame, like film, showing the raw provenance; (2) **30 sec live HTML projector** — DEU → BARY, JPN → BARY, audience-driven last click. Total talk time unchanged at ~15 min + 5 min Q&A.

**Doc chain swept** for the rename and the new close timing:

- `CODAwork2026/README.md` — Presentation timing line + Piece 2 table row + folder-layout block + how-to-run-the-presentation steps 2–3.
- `CODAwork2026/data_outputs/README.md` — Timing line, Piece 2 description, Piece 3 close-handoff, how-to-run-the-presentation steps 2–3.
- `CODA-Association/README.md` — folder-layout block + "What is current" piece-2/piece-3 entries.
- root `README.md` — push-#50 monster-push inventory item 8 + CoDaWork-deliverables table row.
- `CONFERENCE_ATTENDEES.md` — 🎬 CN-TT Output row (was "Full-corpus reference (PDF)").
- `SPEAKING_SCRIPT_QA_companion.md` — masthead timing, voice notes, Slide-21 header timing + narrative (the new two-step close written into the speech), Q&A timing answer, "where are other countries' full plates" Q&A answer, voice-and-posture Close (21) line, Apparatus block (CN-TT Output PDF and Projector as two separate bullets with timing). Source `qa_companion_21.md` synced; `SPEAKING_SCRIPT_QA_companion.pdf` rebuilt via pandoc → HTML → weasyprint (~68 KB landscape Letter), placed in the repo.

**Lockdown discipline.** S2 doc/media only — no engine, schema, INV catalog, NO-CREATE, or locked-surface edits. The CN-TT Output file content is byte-identical to the prior PremierDataOutput PDF; only the public-face name changed and the documentation chain updated.

**Naming rationale.** "CN-TT" expands as "CNT / Tensor Train" — the canonical name for the engine's full output package per HUF-STD-002 (the Tensor Train I/O Standard, shipped push #50). The rename aligns the public-face artifact's name with the standard that defines the pipeline structure (`raw → [Adapter] → CSV → [CNT v3.1.0] → cnt_*.json → [CNQ v2.0.0] → cnq_*.json → [Render] → PDF · PNG · SVG`). The framework now documents its own pipeline using its own standard on its own world-facing artifact — the same meta-pattern that drove the UN-6 handout v11 Tensor Train block in push #65.

*Landed in push #69 — commit `76d2eb2`, CI #65 "CodaWork2026_CN-TT_Output" green 49s, 2026-05-28.*

---

## 2026-05-27 — Consistency-fix pass (ChatGPT review, post-#67 working tree, S2 doc-only) — pushed `dc0b4dc`, CI #64 "coda updates" green 50s

*Three stale-reference remnants flagged in an external review of the pushed `057177e` state, all corrected. Doc/media only — no engine, schema, INV, or NO-CREATE surfaces touched.*

1. **AI-Use-Declaration slide number.** `CODAwork2026/README.md` and `data_outputs/README.md` standards-conformance lines, plus the in-block VERSION_HISTORY look-summary, said the declaration sits on **slide 19**. The active deck is 21 slides and the script closes the declaration on **slide 21** — all three updated to slide 21. (Dated historical journal entries and the Premier-deck plate references — Premier slide 19 = Stage-1 Section view — are records of past/other state and left unchanged.)
2. **SHOCK math-panel wording.** `data_outputs/README.md` math panel still read `stroke→red as ‖Δclr(t)‖/max → 1`, a remnant of the superseded line-recolour design. Updated to the live v2.2 behaviour — `year label → chromatic opposite of plate when ‖Δclr(t)‖/max > 0.5`. The projector HTML itself already carried the correct chromatic-opposite text; only the README panel was stale.
3. **ALIGN mode description.** The speaking script described `ALIGN` as "the helmsman" in two places (talk close + Q&A bench). ALIGN is the barycenter-aligned / centred shape view, distinct from the Helmsman (largest-motion carrier). Both lines changed to "ALIGN, the centred view" / "ALIGN (the centred / barycenter-aligned shape view)"; source `qa_companion_21.md` synced and `SPEAKING_SCRIPT_QA_companion.pdf` rebuilt.

*Landed in push #68 — commit `dc0b4dc`, CI #64 "coda updates" green 50s, 2026-05-28.*

---

## 2026-05-27 — Germany complete plate set added → 21-slide deck; companion renamed count-free (pushed `057177e`, CI #63 "Presentation refinements" green 50s)

*Conference-prep arc, S2 doc/media. Per Peter: "add slide 19 and 22 to Germany only to provide 1 country with a complete set and highlight this in the updated speech."*

**Deck → 21 slides.** Two Premier-deck plates for Germany (Premier slide 19 = the Stage-1 Section view / XY-XZ-YZ orthogonal projections; Premier slide 22 = the ILR-Helmert orthogonal triplet) grayscaled and inserted into the Germany section as **slides 8 and 9** of `CodaWork2026_Presentation_2026-05-27.pptx`. Germany is now the one country shown with the **complete plate set** (share-and-structural-work → trajectory → orthogonal projections → ILR-Helmert triplet); the other countries keep the headline views. Both plates are clean engine output (no placeholder fields). Downstream slides renumbered: Japan 10–11, United Kingdom 12–13, cross-country 14, rest-of-world finale 15–20, close 21; every footer now N / 21.

**Speech updated to highlight it.** The companion gains two Germany sections (slides 8–9) that name Germany as the worked exemplar carried in full, with the complete-set framing; the masthead, timing (~14 min spoken + ~1 min live close, then 5 min Q&A), narrative line, voice notes, and apparatus references all renumbered to 21.

**Companion renamed count-free.** `SPEAKING_SCRIPT_19slide_QA_companion.md`/`.pdf` → `SPEAKING_SCRIPT_QA_companion.md`/`.pdf` (matching the deck's count-free naming so future slide-count changes don't force a rename). All references updated across the README chain (CODAwork2026 README, data_outputs README, CODA-Association README, root README, papers README), `CONFERENCE_ATTENDEES.md` (slide-by-slide rewritten to 21 with the two Germany slides), and the archive index. "19 slides / N / 19 / slide 19 close" → "21 / N / 21 / slide 21" throughout the active docs.

**Lockdown posture.** S2 doc/media. No engine, schema, INV, or NO-CREATE touches. Carries forward in the next push (post-#66 working tree). The trajectory plate residual (engine-internal `course_directness` label) is unchanged — still post-lockdown engine work.

---

## 2026-05-27 — Single grayscale 19-slide Presentation promoted; 13-slide deck archived; folder streamlined (pushed `ee20706`, CI #62 "course directness" green 49s)

*Conference-prep arc, S2 doc/media class. Peter's directive sequence over this session, ending with: "archive the old, promote the new and updated, simplify and streamline the repo for easy and direct access to the critical files in the presentation, make all updated files and readme and other support files in agreement … and ready for push."*

**New active deliverable — `data_outputs/CodaWork2026_Presentation_2026-05-27.pptx` (+ `.pdf`).** A single grayscale deck of **19 slides**, numbered N / 19, replacing the 13-slide colour FinalTalk. It carries the whole talk in one file:
- **Talk (1–12):** title (standard CoDa → adding time to the simplex) → the size view's blind spot, where **deceptive drift** is defined → the rebuilt method diagram (five named readings, each defined) → the Activation Coefficient → three archetypes → Germany / Japan / UK each as a pair (share-and-structural-work view → trajectory) → deceptive drift across the corpus (5 of 9).
- **Rest-of-world finale (13–18):** the other six countries as full-trajectory diagrams — Australia / China / India (deceptive drift present), France / United States / World (absent).
- **Close (19):** what the stack answers; hands to the live projector.
- **Look:** white background, black text, **hatched (value + pattern) size-view and Power-Share figures** (re-plotted from the EMBER CSVs via standard CLR) for low-ink printing and distance contrast; bigger fonts throughout; the AI Use Declaration is on slide 21.
- **Terminology:** pure-science. The talk is named on its subject, **deceptive drift**, defined on first appearance; the metaphors ("fires/quiet", "course", "at the wheel", "yeast factor") are replaced with the correct terms. The bread analogy is kept, marked as an analogy.

**Companion — `SPEAKING_SCRIPT_19slide_QA_companion.md` (+ `.pdf`).** Rewritten to the 19-slide arc and the deceptive-drift terminology; two-column speech + Q&A bench; ~13 min spoken + ~1 min live projector close = ~14 min, then 5 min Q&A.

**Archived (lineage, not for use).** New folder `archive/talk_decks_pre_presentation_2026-05-27/` holds the 13-slide colour deck (`CodaWork2026_FinalTalk_13Slide_2026-05-24.pptx` + `.pdf`), its two builders (`build_final_talk_13slide.py`, `_v2.py`), its two 13-slide script files (`SPEAKING_SCRIPT_13slide.md`, `SPEAKING_SCRIPT_13slide_QA_companion.md` + `.pdf`), and a stale rendered README snapshot — with a folder-level README documenting the supersession.

**Streamlined.** Removed junk from `data_outputs/` (a stale LibreOffice lock file and a 2 MB `.tmp`); moved a mislabeled stale README PDF to the archive. `data_outputs/` now presents the critical files directly: the Presentation (pptx + pdf), the projector HTML, the full-corpus reference (Premier 66-slide), the Foundations plates, and the per-country engine outputs.

**Docs brought into agreement.** Promoted the 19-slide Presentation across the README chain (`CODAwork2026/README.md` v2.6, `data_outputs/README.md` v7.1, `CODA-Association/README.md`, root `README.md`, `papers/README.md`), the audience follow-along (`CONFERENCE_ATTENDEES.md` — slide-by-slide section rewritten to the 19-slide arc + deceptive-drift terms), and the archive index (`archive/README.md`). AI-Use-Declaration references moved from "slide 13" to "slide 19"; the projector SHOCK descriptions updated to the v2.2 year-label chromatic-opposite behaviour. Historical push records (CHANGELOG rows, PUSHES_INDEX, PUSH63/64/65 docs) left unchanged as the record.

**Lockdown posture.** S2 doc/media only. No engine, no schema, no INV catalog, no NO-CREATE creations. All edits are within the authorized conference-prep surface. The trajectory **plate images** (slides 7/9/11 and the finale) still carry the engine's internal "course_directness / System Course Plot" labels baked into the rendered PNGs; relabeling those is post-lockdown engine work — the slide captions around them already use the science terms.

---

## 2026-05-27 — Strange-attractor flash + four-thread synthesis + Ramsar field-work pivot (working tree, post-#65)

*Working-state journal entry — these items live on the working tree after push #65 (`1b48894` CI #61 "Tensor Train Handout") landed. They are doc-only, file-only filings outside the `CODAwork2026/` lockdown surface, captured here in the CODAwork2026 VERSION_HISTORY because they touch the post-conference roadmap that the conference run-up has been building toward. No CODAwork2026/ surface edits in this round.*

**Trigger.** Peter, ~10 days from the Coimbra flight, while reviewing the talk materials: *"Claude i had a flash of a thought that i have to have analyzed, strange attractor analysis, it just flashed, what does it mean? what could cnt do with it?"* Followed by *"the transcendentals and the complex conjugates and the old html demos and the morphological analysis is in my thinking i believe."* And then: *"yes, this is my mind unloading i hope so i can keep preparing for my flight on Saturday. update all future projects and notes and histories and journals and file all as suggested, Ramsar is also on my agenda, now we can offer more than governance, compositional analysis tools for wetlands field work."*

**Two new working notes filed in `papers/in_progress/` (post-conference work; not for the talk):**

- **`papers/in_progress/ATTRACTOR_MORPHOLOGY_AND_TRANSCENDENTAL_BASINS.md`** (new) — 12-section consolidation synthesizing four threads that had been moving independently in the roadmap: §4.1 transcendental library, complex conjugates as the natural CNQ carrier algebra (D=2 quaternion factoring), the old HTML strange-attractor visualization demos, and morphological analysis of the attractor itself. The synthesis organizes them under a single principle — the **attractor fingerprint** as a 7-component diagnostic suite (Lyapunov spectrum, correlation dimension D₂, embedding dimension dₑ via Takens, RQA recurrence quantification, topological entropy h_top, UPO skeleton, SRB measure). The fingerprint is what CNT would compute on a strange-attractor budget; the transcendentals become *basins of attraction* in budget space rather than candidate constants. The note reviews what substrate already exists (the transcendental library, the CNQ complex-conjugate algebra carrier, projector Mode 4 ATTRACTOR visualization heritage from BTL acoustic 2024) and what concrete post-conference work follows (five items: Lyapunov-exponent block in CNT engine; correlation-dimension estimator; multifractal-spectrum module; transcendental-proximity matcher; gauge-theoretic adjacency surface tying to Donaldson/Seiberg-Witten 4-manifold invariants). The note also performs an empirical re-read of the Germany/Japan/UK case studies for attractor signatures and records the recursion-test observation that the BTL acoustic 2024 → projector 2026 → handout 2026 channel-discipline pattern recurs here as the *one organizing principle absorbs many separate diagnostics* pattern.

- **`papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md`** (new) — 8-section working note capturing Peter's pivot from *Ramsar = governance worked example only* to *Ramsar = governance + compositional field-work toolkit*. The HUF Topography Conjecture §6–7 already names Ramsar's three-tier governance reading (site listing / Montreux Record / removal); this note extends the offering to the practitioner level — site rangers, field ecologists, hydrologists, ornithologists. Five wetland compositional time-series the framework can read natively are named (vegetation cover, water chemistry, sediment grain-size + organic, avian community, hydroperiod); the keystone-species hypothesis is given a falsifiable form as the **ecological yeast factor** via the activation coefficient α; a worked example (fen subject to drought + invasive grass + restoration intervention) is carried through; three-tier deployment is mapped to three practitioner audience classes (site ranger / regional coordinator / Secretariat); a four-item post-conference work plan is recorded (wetland-data adapter module + field handbook + three pilot studies + Secretariat outreach under the non-contact doctrine).

**Roadmap updates in `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md`:**

- **§4.12 Attractor morphology + transcendental basins (new)** — placed after §4.11's channel-discipline doctrine, before the §5 application-targets header. The section names the attractor fingerprint as a 7-component diagnostic, reviews what substrate is already in place, lists five concrete post-conference engineering items, performs the empirical re-read of the three case studies, sets sequencing for weeks 5–20 post-conference, and cross-references §4.11 (the two sections are complementary, not redundant — §4.11 is visual-channel discipline, §4.12 is mathematical-content discipline).
- **§5.9 Ecology and wetlands — Ramsar field-work (new)** — placed after §5.8 theoretical-frontier audience, before the §6 consolidated scheduled work header. The section names the practitioner audience class (parallel to §§5.1–5.7), explains why the pivot now (field practitioners already collect compositional time-series; governance-only framing under-uses what the framework delivers), lists the five wetland compositional types + the α-based keystone-species hypothesis + the three-tier deployment + the four-item post-conference work plan + the worked-example carry-through, sets sequencing (weeks 5–10 adapter; 10–20 field handbook; 2027 field-season pilots; Secretariat outreach after pilot data lands), and records the lockdown discipline (S2 doc-only through 2026-06-06; the adapter and handbook are post-lockdown light engineering).

**Insight captured.** The two filings share a structural pattern that itself is worth recording: *the framework's substrate already contains what a new application class needs; the work is to recognize the fit and name the connection.* The attractor flash did not require new mathematics — the transcendentals, the complex conjugates, the visualization demos, the morphological-analysis thread were all already in the system. What was missing was the organizing principle (the attractor fingerprint) that consolidates them. Similarly, the Ramsar pivot did not require a new framework — the five wetland compositional time-series already fit the existing CNT/CNQ machinery; the activation coefficient α already provides the falsifiable diagnostic the ecological literature has been groping toward. What was missing was the practitioner-language presentation (field handbook + adapter module + pilot studies) that makes the existing substrate reachable by the audience class. **Both flashes are recognition flashes, not invention flashes.** The pre-flight mind-unload pattern (Peter naming what was already coalescing) is the same pattern that produced the post-#63 channel-discipline doctrine and the pre-#62 ground-state-and-traction consolidation. The framework's discipline of *file it as a working note, schedule the work in the roadmap, do not disturb the lockdown* keeps the mind-unload productive without breaking the conference run-up.

**Working-tree manifest from this round (5 files, all S2 doc-only, all outside the CODAwork2026 lockdown surface, all `papers/in_progress/` working-note class):**

- `papers/in_progress/ATTRACTOR_MORPHOLOGY_AND_TRANSCENDENTAL_BASINS.md` (new)
- `papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md` (new)
- `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` (modified, §4.12 + §5.9 added)
- `CODA-Association/CODAwork2026/VERSION_HISTORY.md` (modified, this 2026-05-27 entry — the only CODAwork2026 surface touch this round, journal-only, no media changes)
- Admin chain entries to follow per `PUSH_PROTOCOL.md §6` if this round bundles into a push #66; otherwise held as working-tree filings until the post-conference window.

**Lockdown posture.** S2 doc-only. No engine, no schema, no INV catalog disposition, no NO-CREATE creations, no CODAwork2026 media-surface edits. The two new working notes and the two roadmap section additions are post-conference candidate work, scheduled for after 2026-06-06 per the framework's discipline that the lockdown window is for *land-the-talk*, not for opening new engineering surfaces.

**Cross-references.** The two new working notes cite each other only in passing (different application domains); both cite `papers/flagship/GROUND_STATE_AND_TRACTION.md` v2.2 as the mathematical substrate; both feed into `papers/POST_CODA_PARTNERSHIP_TARGETS.md` v4's 14-system metabolism matrix at distinct rows (attractor work → cosmology + turbulent dynamics + neural attractors + climate; wetland work → ecology row, currently §5.9 in the roadmap). The Ramsar note also cites `HUF_TOPOGRAPHY_CONJECTURE.md` §6–7 as the existing governance worked example that the field-work layer extends.

---

## 2026-05-25 — Post-#63 maintenance round (working tree, held for push #64)

*Working state entry — these items live on the working tree after push #63 (`5d0119f` CI #59 "13 slide codawork2026") landed. They are held for inclusion in push #64 when Peter's pending slide-talk edits are ready to bundle in.*

**New artifacts on the working tree (not yet committed):**

- **`CODA-Association/CODAwork2026/SPEAKING_SCRIPT_13slide_QA_companion.md`** + **`.pdf`** (15 pages, letter landscape) — two-column reading aid for the talk: left column carries the speech per slide, right column carries 3–6 anticipated Q&A bench cards with ready responses per slide, plus a general Q&A bench (MC-4, why-not-already-CoDa, BTL lineage, reproducibility, manifold-category, gauge theory, hostile-question handling, time-running-out handoff) and a voice-and-posture reminders table. Rendered via pandoc-to-HTML-to-weasyprint (HTML preserves the two-column tables that LaTeX collapses). Per Peter's directive *"i will read from this, and have ready possible responses on a per slide basis."*
- **`CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html`** updated to **v2.2 SHOCK design** — the SHOCK overlay moved off the plate perimeter (which kept fighting carrier-identity color and base line-width encoding) onto the previously-unused year-label text color: when SHOCK is on and `smag > 0.5`, the year label flips to the chromatic opposite of the plate's base color (`lblR = 255 − cr`, etc.) with a small alpha bump. Carrier identity stays clean in the line; SHOCK gets a clean channel of its own. Five-line implementation, no interference with carrier encoding, high contrast against any palette by RGB-complement math. Replaces the brief v2.1 dual-encoding stroke-width attempt per Peter's *"instead of lighting the band red, simplify, make the year/plate markers the chromatic opposite color as a marker by text change."*
- **`papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` §4.11** updated with: v2.2 supersession note for item 2 (dual-encoding stroke-width superseded by year-label chromatic-opposite); new **channel-discipline doctrine** subsection recording the principle that emerged — *each visual channel owns one job; adding a diagnostic = find a clean channel, not stack onto a busy one* — explicitly tied to the BTL constant-power Butterworth crossover precedent (flagship §4.2). Acoustic engineering taught the discipline in 2024; the projector inherited it in 2026. The framework's recursion-test pattern in action.

**Insight captured.** Peter's call to revert the v2.1 dual-encoding and move SHOCK to the year label is more than a UX tweak — it is the worked-example of a doctrine that should travel. *Visual channels are driver bands.* Every encoding axis stacked onto a busy channel costs more in interference than it gains in salience. The same physics that gave the BTL crossover its constant-power objective gives the projector its single-channel-per-job objective. The §4.11 channel-discipline subsection captures the principle for future Stage 4 plate work, HUD overlays, HCI-AUDIO listening-position indicators, HCI-ULTRASOUND non-contact-measurement markers, and the post-conference temporal-profile classifier (item 3 of §4.11) whose visual surface has not yet been designed.

**Admin chain state.** Post-#63 5-step sync per `PUSH_PROTOCOL.md §6` is complete on the working tree: `HS_FAST_REFRESH.json` (last_push, push_63_completed, previous_last_push, last_updated → 2026-05-25), `ai-refresh/HS_ADMIN.json` (push_63_completed entry), `ai-refresh/PUSHES_INDEX.md` (Push #63 deep-detail section + new layered-parity table + file manifest), `CHANGELOG.md` (#63 row with actual SHA `5d0119f` + CI #59 + 50s + theme). All four admin surfaces ready to ride along in push #64. (Bash-side cache lag has reported false-positive JSON parse errors on HS_FAST_REFRESH.json; Windows-side Read confirms the file is well-formed and extends through line 621 with proper closing braces; live GitHub HEAD SHA cross-check confirms `5d0119f` matches.)

**Push #64 working-tree manifest (~10 files, all S2 doc-only, all lockdown-compliant):**

- `CODA-Association/CODAwork2026/SPEAKING_SCRIPT_13slide_QA_companion.md` (new)
- `CODA-Association/CODAwork2026/SPEAKING_SCRIPT_13slide_QA_companion.pdf` (new, rendered)
- `CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html` (modified, v2.0 → v2.2 SHOCK redesign)
- `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` (modified, §4.11 supersession + channel-discipline doctrine)
- `HS_FAST_REFRESH.json` (modified, post-#63 admin sync)
- `ai-refresh/HS_ADMIN.json` (modified, push_63_completed)
- `ai-refresh/PUSHES_INDEX.md` (modified, Push #63 section added)
- `CHANGELOG.md` (modified, #63 row filled)
- `CODA-Association/CODAwork2026/VERSION_HISTORY.md` (modified, this 2026-05-25 entry)
- Plus Peter's slide-talk edits in progress (TBD)

Push class S2 doc-only. Lockdown-compliant. No engine, no schema, no INV catalog, no NO-CREATE.

---

## 2026-05-24 — 13-slide deck promoted (the navigation chart finally readable from the back)

**Trigger.** Peter's directive 2026-05-24: *"for CodaWork2026_FinalTalk_10Slide_2026-05-20 slide 6.7.8 should have the navigation chart follow dividing from 3 to 6 slides, this was originally done and then it was condensed but now it needs to go back which is fine and the slide talk can stay as is just divide the navigation part to that slide, this will make 13 slides, this is under the recommended 15 slides suggestions, problem is the image is just too small to see and now all slides can be shown large and easier to see."*

The 10-slide compressed deck paired each country case-study with a per-country navigation chart at 2.6″ wide on the right margin. From the back of a conference room that navigation chart was not legible. The 13-slide expansion splits each country into a pair: **share-and-work view** (the 4-panel figure at 9″ wide, dominant) and **course on the simplex** (the per-country navigation chart at 6.5″ × 5.0″ centered, finally readable). Total stays under the 15-slide conference recommendation. Speaking-script substance unchanged; allocated across the new pair (~55 sec share-and-work + ~30 sec navigation per country = 85 sec total, vs the 10-slide version's 75 sec single slide — net 10 extra seconds per country for legibility).

**New active files at root and in `data_outputs/`:**
- `data_outputs/CodaWork2026_FinalTalk_13Slide_2026-05-24.{pptx,pdf}` — the talk (13 slides, ~8 min 50 sec spoken).
- `data_outputs/build_final_talk_13slide.py` — reproducible builder.
- `SPEAKING_SCRIPT_13slide.md` (new) — beat-by-beat script with explicit pairing rhythm (content slide then geometry slide, three times); per-country pacing notes; voice notes on letting the navigation chart breathe.

**Files archived to `archive/talk_decks_pre_13slide_2026-05-24/`** (with folder-level README):
- `CodaWork2026_FinalTalk_10Slide_2026-05-20.{pptx,pdf}` — the 10-slide compressed deck.
- `build_final_talk_10slide.py` — its python-pptx builder.
- `SPEAKING_SCRIPT_10slide.md` — its 10-slide beat-by-beat script.

**Documents updated for the deck switch:**
- `data_outputs/README.md` → version 7.0 — three-piece package now describes the 13-slide deck as Piece 1; expansion rationale and pairing rhythm called out.
- `CODAwork2026/README.md` → version 2.5 — table row 1 (Talk deck) now points at the 13-slide deck and the new speaking script; folder layout shows the new archive folder and the new builder; *"How to run the presentation"* section rewritten to describe the per-country pairing rhythm.
- `CODA-Association/README.md` (front door) — START HERE pointer now reads `CodaWork2026_FinalTalk_13Slide_2026-05-24.pptx`; three-piece summary updated; archive section gains the new folder; AI Use Declaration reference moved from slide 10 to slide 13.
- `CONFERENCE_ATTENDEES.md` (audience follow-along page) — slide-by-slide block rewritten from 10 slides to 13 slides; new dedicated navigation-chart sections for Germany (slide 7), Japan (slide 9), and UK (slide 11); the *"compare Germany's smooth arc to Japan's looping search to UK's jump-and-return"* comparison threaded explicitly through the navigation slides.
- `archive/README.md` — new section for `talk_decks_pre_13slide_2026-05-24/` added at top; archive index now lists 10-slide as the most recently archived predecessor.

**Visual QA discipline.** First render of the 13-slide deck had bottom-third crowding on all six new slides (gold callout + italic explainer sitting at or below the y=8.10″ footer baseline) and two-line italic wraps on slides 9 and 11 spilling below the footer. Fixes applied: case-study figures shrunk from 5.2″ to 4.85″ tall; nav charts pinned to explicit 6.5″ × 5.0″ box; callouts moved up to y=6.55/6.65; italics moved up to y=7.00/7.15; slide 9 and 11 italics shortened to fit one line. Re-rendered and re-QAed; all six previously flagged slides resolved, no new issues introduced.

**Push class:** S2 doc-only, lockdown-compliant — engine code, schemas, INV catalog dispositions, NO-CREATE files, manuscript, cinema scroll, projector, per-country plates all untouched. The 13-slide expansion is a presentation-layer change; the underlying engine outputs are unchanged.

---

## 2026-05-21 — Heading polish (manuscript / presentation hierarchy)

**README.md → version 2.4.** ChatGPT post-push #58 review of `CODA-Association/CODAwork2026/` flagged a wording inconsistency: the section heading "The presentation in three pieces" sat above a four-row table (manuscript + talk + cinema scroll + projector). ChatGPT's suggested polish — *"foundation manuscript + three-piece presentation"* — adopted. Heading rewritten to "The conference package — foundation manuscript + three-piece presentation", with an introductory sentence clarifying that the manuscript is the foundation and the talk/cinema/projector triplet condenses it. Table row indices renumbered 0–3 (0 = foundation manuscript; 1–3 = the presentation pieces) to make the hierarchy explicit. No content moved or rebuilt; pure heading-and-numbering polish. Push class: S2 doc-only, no admin-chain churn, lockdown-compliant.

---

## 2026-05-20 — Refinement trail archived, 10-slide deck is now the only active talk

**Trigger.** ChatGPT review of `CODA-Association/CODAwork2026/` flagged that the README chain still framed the 22-slide and 12-slide decks as "preserved siblings" or "time-budget fallbacks". With the 10-slide compressed final adopted as the conference talk, the sibling framing was a source of confusion — the repo still looked like three decks were on offer rather than one. Peter's directive: *"keep the 10 slide and talk, archive the the other slides and associated talks and update the readme files... the trail of refinements get archived the best move forward."*

**Files archived to `archive/talk_decks_pre_10slide_2026-05-20/`** (with folder-level README):
- `CodaWork2026_FinalTalk_2026-05-17.{pptx,pdf}` — 22-slide original narrative.
- `CodaWork2026_FinalTalk_12Slide_2026-05-20.{pptx,pdf}` — 12-slide intermediate compression.
- `CodaWork2026_FinalTalk_12Slide_CompressionPlan.json` — ChatGPT-prepared 22→12 plan.
- `build_final_talk.py`, `build_final_talk_v2.py`, `build_final_talk_12slide.py` — python-pptx builders for those two stages.
- `SPEAKING_SCRIPT.md` — 22-slide beat-by-beat script (slide numbers no longer apply to the 10-slide deck).

**Files remaining at active locations:**
- `data_outputs/CodaWork2026_FinalTalk_10Slide_2026-05-20.{pptx,pdf}` — the talk.
- `data_outputs/build_final_talk_10slide.py` — its reproducible builder.
- `SPEAKING_SCRIPT_10slide.md` — its beat-by-beat verbal script.

**README chain refresh.**
- `data_outputs/README.md` → version 6.0. Drops "preserved siblings", points at the archive folder. "How to run the presentation" simplified.
- `CODAwork2026/README.md` → version 2.3. **Critical stale-reference fixes flagged by ChatGPT:** "At slide 18... At slide 19..." replaced with "After slide 10, switch to the cinema scroll. Then open the projector." Standards-conformance line updated from "slide 19 / slide 20" to "slide 10 footer + manuscript cover/back". Folder-layout block reflects the new archive subfolder.
- `CODA-Association/README.md` → version 2.3. Folder map and "what is archived" reflect the new archive subfolder. AI-Use-Declaration line corrected to "slide 10 + manuscript".
- `archive/README.md` rebuilt with the new section first, plus manuscript-render lineage section.

**Discipline preserved.** Engine code untouched. Manuscript untouched. Per-country JSON/PDF outputs untouched. Cinema scroll and projector untouched. Push class: S2 (doc-only), Pre-Conference Lockdown-compliant.

**Outcome.** Repo presents one deck as the conference talk, one speaking script as its verbal companion, one archive folder explaining how that deck was reached. ChatGPT's flagged stale references closed. The trail is preserved; the surface is clean.

---

## 2026-05-20 — Manuscript working-copy correction (TOC integrity)

**Initial action (later reversed in the same session).** Moved the `CODA-Association/CODAwork2026/Compositional_Monitoring_2026.{docx,pdf}` working copies to `archive/manuscript_2026-05-19_msprint_pre-push58/` on the assumption they were stale Microsoft Print To PDF renders that should be replaced by the canonical LibreOffice build at `papers/codawork2026/manuscript/output/`.

**Reversal.** Peter flagged that the archived version actually had a fully populated Table of Contents (with every section + page numbers) while the LibreOffice canonical export shipped with the un-populated TOC placeholder text *("If your reader does not auto-populate this section, right-click and choose Update Field")*. Microsoft Word populates TOC fields on open before printing; LibreOffice headless export does not. The msprint render was therefore **superior for conference distribution** despite the irregular toolchain.

**Final state:**
- `CODA-Association/CODAwork2026/Compositional_Monitoring_2026.pdf` ← MS Print To PDF render with populated TOC (26 pp, 2.6 MB) — conference distribution version.
- `CODA-Association/CODAwork2026/Compositional_Monitoring_2026.docx` ← byte-identical to `papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.docx`.
- `papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.pdf` ← LibreOffice canonical build artefact, retains the un-populated TOC. Preserved as the build-pipeline reproducibility record but not used for distribution.
- `archive/manuscript_2026-05-19_libreoffice_empty_toc/` ← parked copy of the LibreOffice export, for traceability of this correction.
- `archive/manuscript_2026-05-19_msprint_pre-push58/` ← fallback copy of the msprint render, with corrected README explaining the full history.

**Policy reinforced.** Conference working copies at `CODA-Association/CODAwork2026/` must produce a populated TOC. Until the build pipeline (`papers/codawork2026/manuscript/build/build_docx.js`) can produce a populated-TOC PDF headlessly, the msprint render is the authoritative distribution artefact.

**Post-conference to-do.** Fix the headless PDF export pipeline so the LibreOffice canonical produces a populated TOC, closing the policy gap that currently lets the canonical and the distribution artefact differ. Track as a post-conference task; not blocking for CoDaWork 2026.

---

## 2026-05-20 — 10-slide compressed deck promoted to primary

**FinalTalk deck — version 2.0 (10-slide compressed).** The 10-slide deck (`CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx`) becomes the conference talk. Built from a ChatGPT-prepared compression plan plus a final pass that drops the MC-4 falsifiability slide and the "Inspect the instrument" closer; all contact details (email, repo, UN-6 handout) move onto slide 1. ~8 minutes spoken, leaves time for the cinema scroll and projector during Q&A. Slides 6/7/8 (Germany / Japan / UK case studies) deliberately weighted at 75 seconds each. Beat-by-beat verbal script committed at [`SPEAKING_SCRIPT_10slide.md`](SPEAKING_SCRIPT_10slide.md).

**Preserved siblings** (not deleted; may be used if a longer time slot is offered):
- `CodaWork2026_FinalTalk_12Slide_2026-05-20.pptx` — ChatGPT-plan intermediate compression (retains the MC-4 slide).
- `CodaWork2026_FinalTalk_2026-05-17.pptx` — original 22-slide narrative deck (full per-country navigation slides).

**Documents updated for the deck switch:**
- `data_outputs/README.md` → version 5.0 — three-piece package now describes the 10-slide deck as Piece 1; preserved siblings called out.
- `CODAwork2026/README.md` — table row 2 (Talk deck) now points at the 10-slide deck and the speaking script; folder layout shows all three deck variants.
- `CODA-Association/README.md` (front door) — START HERE pointer now reads `CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx`; three-piece summary updated.
- `CONFERENCE_ATTENDEES.md` (audience follow-along page) — slide-by-slide block rewritten from 22 slides to 10 slides; manuscript-section and figure links preserved, redistributed across the new slide structure; a "Things not in the deck but available" section added explaining MC-4 and the closer still live in the manuscript and speaker brief.
- `SPEAKING_SCRIPT_10slide.md` (new) — direct, information-packed beat-by-beat script. Slides 6/7/8 weighted for case studies. Optional verbal returns documented for likely Q&A (MC-4, why-not-already-standard-CoDa, why-these-five-viewpoints).

**Rationale.** Peter's directive: *"this gives me breathing room and time to talk and not manage slides and juggle media too much, make this all seamless, simplify and make sense not confusion."* The 10-slide deck collapses six slides' worth of separable teaching beats (helmsman + Power Share + Activation Coefficient definitions; per-country navigation chart slides; MC-4 framing; closing apparatus slides) into the case studies and the synthesis. The repo and the manuscript carry the rest.

---

## 2026-05-13 — Folder declared authoritative

Per Peter directive 2026-05-13: *"i have one folder that is the authority from now on and all other folders are the source for the information that is current and present in this folder, ensure document versions are now implemented for coda-association media."*

| File | Version | Status | Notes |
|---|---|---|---|
| `README.md` | 1.1 | Updated | Revised to declare folder authority + version policy |
| `SPEAKER_BRIEF.md` | 1.0 | New (baseline) | Consolidated from May-12 source; adds repository walking-around state + lockdown context |
| `STUDY_PAGE.md` | 1.0 | New (baseline) | Consolidated from May-12 source; minor wording tightening |
| `CHEAT_SHEET.md` | 1.0 | New (baseline) | Consolidated from May-12 source; adds EITT + KILL-001 Q&A backstops |
| `PEDAGOGICAL_TABLES.md` | 1.0 | New (baseline) | Consolidated from May-12 source; adds Table 3 (EITT) and Table 4 (bread analogy) |
| `BACKUP_PRESENTATION.md` | 1.0 | New (baseline) | Consolidated from May-12 source; updated lockdown context |
| `QA_BENCH.md` | 1.0 | New (baseline) | Consolidates 5 separate bench cards from May-12 source into single doc; adds Q&A 8 (EITT), Q&A 9 (KILL-001), Q&A 10 (governance), Q&A 11 (bread), Q&A 12 (Collective) |
| `ABSTRACT.md` | 1.1 | Revised | Adds version header; sharpens technical detail around twin-quaternion factoring + EITT |
| `CodaWork2026_Talk_2026-05-12.pptx` | 1.0 | Released | 12 slides matching the May-12 10-beat narrative; built 2026-05-13 |
| `CodaWork2026_Talk_2026-05-12.pdf` | 1.0 | Released | PDF render of the deck |
| `VERSION_HISTORY.md` | 1.0 | New | This file |

**Sources superseded.** All May-12 source documents in `../../papers/codawork2026/talk/` remain in place as the lockdown-protected source snapshot. They are not modified during the pre-conference lockdown window (2026-05-12 → 2026-06-06). The authoritative versions for future editing are in this folder.

**Lockdown compatibility.** This folder is S2 doc-only (linked doc addition). No engine, schema, INV catalog, or NO-CREATE changes. Consistency checker exit 0 confirmed.

---

## Versioning policy going forward

**From 2026-05-13 onward:**

1. **Edit happens here.** All future edits to conference materials happen in this folder. The `papers/codawork2026/talk/` folder is the historical source snapshot and is not edited (it stays in its lockdown-protected state until 2026-06-06 or beyond).

2. **Every edit bumps a version.** Even small clarifications increment the patch number. The header in each file states the current version. This file records the change.

3. **Patch / minor / major.** See conventions above. When in doubt, go higher — a minor bump is cheap; under-bumping causes silent drift.

4. **One change, one entry.** Each version-bump gets its own table row below with file, new version, summary, date.

5. **The deck file.** The PowerPoint and PDF carry a date stamp in the filename (e.g., `CodaWork2026_Talk_2026-05-12.pptx`). When a major slide revision occurs, a new dated file is created (e.g., `CodaWork2026_Talk_2026-06-15.pptx`) and the prior file is moved to an `archive/` subfolder. The current deck is always the most recent dated file.

6. **Cross-references stay stable.** Internal links within the folder use stable filenames (`SPEAKER_BRIEF.md` not `SPEAKER_BRIEF_v1.0.md`) so version bumps don't break links.

7. **External pointers (back to canonical sources).** Pointers from this folder to `../../papers/` and elsewhere remain — they point at the historical/canonical sources, while this folder remains the editable authority going forward.

---

### 2026-05-13 (later still) — Premier data output added

Per Peter directive: *"these need the new cnt and cnq engine update full run to produce the time series orthogonal projections as shown in stage 1 plates for all countries in the study... these are the proper outputs not just a talk about data, the actual data."*

A new `data_outputs/` subfolder added to host the actual engine outputs. CNT v3.1.0 + CNQ v2.0.0 + Stage-1 plate generator + Stage-2/3 plate generator run end-to-end on the 9-country EMBER corpus.

| File | Version | Pages / Slides | Size | Notes |
|---|---|---|---|---|
| `data_outputs/README.md` (NEW) | 1.0 | — | — | Folder orientation + reproducibility recipe |
| `data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf` (NEW) | 1.0 | 334 pages | 3.8 MB | Master PDF: cover + TOC + 9 country sections × (cover + 27 Stage-1 plates + 7 Stage-2/3 pages + 2 CNQ plates) |
| `data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pptx` (NEW) | 1.0 | 57 slides | 2.9 MB | Compact PPTX: cover + TOC + 9 country sections × 5 key plates + AI Use Declaration |
| `data_outputs/per_country_json/cnt_v3/cnt_*.json` (NEW × 9) | — | — | 290–350 KB ea | Hash-chained CNT v3.1.0 canonical outputs (schema 3.1.0) |
| `data_outputs/per_country_json/cnq_v2/cnq_*.json` (NEW × 9) | — | — | 17–35 KB ea | Hash-chained CNQ v2.0.0 canonical outputs (schema cnq/2.0.0) |
| `data_outputs/per_country_pdfs/{ISO}_stage1.pdf` (NEW × 9) | — | ~27 pages ea | ~210 KB ea | Per-country Stage 1 cine-deck for individual access |
| `data_outputs/per_country_pdfs/{ISO}_stage23.pdf` (NEW × 9) | — | 7 pages ea | ~100 KB ea | Per-country Stage 2/3 navigation pages |
| `data_outputs/per_country_pdfs/{ISO}_cnq.pdf` (NEW × 9) | — | 2 pages ea | ~45 KB ea | Per-country CNQ quaternion-view dashboard |
| `VERSION_HISTORY.md` (this file) | 1.2 | — | — | This entry |

**Supersedes (without modifying):** the older Japan-only `papers/codawork2026/planning/stage1_plates/stage1_plates_fixed.pdf`, `stage23_plates.pdf`, `navigation.pdf`, and `HCI_Japan_CoDaWork2026.pdf` reference outputs. Those remain in their original locations as historical artifacts.

**Lockdown compatibility:** Engine code, schema, INV catalog dispositions, NO-CREATE files, and `papers/codawork2026/talk/` are all untouched. This work runs the unchanged engines to produce documented output — not a modification of engine code. The lockdown forbids changing engine code; it does not forbid running it.

**Reproducibility:** The recipe in `data_outputs/README.md` reproduces these outputs bit-identically from raw EMBER CSV in ~5 minutes. content_sha256 + engine_signature on every JSON.

---

## Future version bumps will be logged below this line

### 2026-05-13 (later same day) — HUF Publication Standards conformance pass

Per Peter directive: *"place ai assistance at a proper scientific community location at the end of the media as part of the ai use declarations that meet general world standards for such declarations... ensure JSONs are referenced as the authority when any of the tasks must meet an established standard."*

| File | New version | Change |
|---|---|---|
| `huf-gov/standards/HUF_PUBLICATION_STANDARDS.json` (NEW) | 1.0 | New authoritative standards JSON (HUF-STD-001). Adopts ICMJE / COPE / Nature/Springer / Science/AAAS / WAME / EU AI Act (2024) / arXiv / ACM / IEEE as primary references. Establishes AI Use Declaration template, authorship attribution rules (human-only), falsifiability disclosure, provenance hash-chain, versioning, locale support, lockdown discipline, licensing. |
| `huf-gov/standards/README.md` (NEW) | — | Folder description for standards. |
| `README.md` (this folder) | 1.2 | Standards conformance + revised file index with new version numbers + speaker line corrected. |
| `../README.md` (CODA-Association parent) | 1.2 | Standards conformance. |
| `SPEAKER_BRIEF.md` | 1.1 | "with the HUF AI Collective..." removed from byline; new AI Use Declaration section appended; standards reference added. |
| `STUDY_PAGE.md` | 1.1 | AI Use Declaration appended. |
| `CHEAT_SHEET.md` | 1.1 | AI Use Declaration appended. |
| `PEDAGOGICAL_TABLES.md` | 1.1 | AI Use Declaration appended (attributes Grok r6 for Tables 1-2; Claude for Tables 3-4). |
| `BACKUP_PRESENTATION.md` | 1.1 | AI Use Declaration appended. |
| `QA_BENCH.md` | 1.1 | AI Use Declaration appended. |
| `ABSTRACT.md` | 1.2 | Speaker line corrected; AI Use Declaration section appended (full long form). |
| `CodaWork2026_Talk_2026-05-13.pptx` (NEW dated file) | 1.1 | Title slide rebuilt — speaker is now "P. Higgins, Rogue Wave Audio" (no AI Collective in byline). New Slide 13 — full AI Use Declaration following established convention with 4 information cards (tools, tasks, responsibility, governance), 9 primary-reference citations on slide. Deck is now 13 slides. |
| `CodaWork2026_Talk_2026-05-13.pdf` (NEW dated file) | 1.1 | PDF render of v1.1 deck. |
| `archive/CodaWork2026_Talk_2026-05-12.pptx` (MOVED) | v1.0 (archived) | Prior version moved to archive per versioning policy. |
| `archive/CodaWork2026_Talk_2026-05-12.pdf` (MOVED) | v1.0 (archived) | Prior version moved to archive. |
| `VERSION_HISTORY.md` (this file) | 1.1 | This entry. |

**Admin JSON updates (post-folder):**
- HS_ADMIN.json `_meta` — to reference HUF-STD-001 at next admin sync.
- HS_FAST_REFRESH.json `_meta` — to reference HUF-STD-001 at next admin sync.

**Lockdown compatibility:** S2 doc-only — "terminology corrections for real reader-confusion bugs" (the previous byline could be read as joint authorship). Engine, schema, INV catalog dispositions, NO-CREATE files, `papers/codawork2026/talk/` content all untouched.

---

### 2026-05-14 — Dual-View Stage 1 + CNQ dashboard fix + PPTX rebuild

Per Peter directive: *"peter, claude, seems we need both views, build the output code to generate the ILR-Helmert orthogonal triplet for standard output and as an additional view version..."* followed by *"CNQ dashboard scale may not be visible as nothing appears, check the output"* and *"this should make an impression on those that have been doing this by hand, also please update now the pptx to match."*

Three coupled changes consolidate into a v2.0 data-output release.

| File | New version | Change |
|---|---|---|
| `../../HCI/codawork2026/stage1_plates/ilr_triplet_plate.py` (NEW) | 1.0 | New ILR-Helmert Orthogonal Triplet Plate generator. Reads `stage1_output.json`; emits 1 summary page + N cine pages of three orthogonal scatter projections (ilr_1×ilr_2, ilr_1×ilr_3, ilr_2×ilr_3) with Helmert basis loadings + trajectory info block. Companion to `stage1_plates_raw.py`. Both are now standard Stage-1 outputs per Output Doctrine v1.0 + HUF-STD-002 link 4. |
| `data_outputs/dual_view/CodaWork2026_DualViewStage1Output_2026-05-13.pdf` (NEW) | 1.0 | 503-page Master Dual-View PDF — 9 countries × (View A divider + 27 Section plates + View B divider + 27 Triplet plates). Reads the timestep magnitudes (Section) and the trajectory shape in compositional geometry (Triplet) on one page-flip. |
| `data_outputs/dual_view/{ISO}_dual_view.pdf` (NEW × 9) | 1.0 | Per-country dual-view PDFs (~56 pages, ~450 KB each; USA 54 pages). |
| `data_outputs/dual_view/README.md` (NEW) | 1.0 | Folder explanation + reading guide. |
| `data_outputs/per_country_pdfs/{ISO}_cnq.pdf` (REGENERATED × 9) | 2.0 | CNQ dashboard fixed — root cause was JSON-key-path mismatches (tried `cnq_view.bearing_trajectory_d2/d3/d4`, real key is `cnq_view.bearing_trajectory`; tried `cnq_view.chsh_diagnostic.S_value`, real is top-level `chsh_diagnostic.S_value`; tried `helmsman_family.sigma_t`, real is `.sign`; tried `tensor.frames[t].angular_velocity_deg`, real is `tensor.timesteps[t].higgins_extensions.angular_velocity_deg`). Real data now populates all panels. China shows CHSH S = 0.88 (the talk's headline); Germany shows Hs 0.43→0.13, ω 2024 spike to ~70°/yr, K_eff arc 3.5→6.7; D=9 countries correctly report "not computed at D=9 (twin requires D=8 = 4+4 partition)." |
| `data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf` (REGENERATED) | 2.0 | Master PDF rebuilt with corrected CNQ pages. Now 325 pages (was 334 — CNQ consolidated from 2 pages to 1 single-page dashboard). |
| `data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pptx` (REGENERATED) | 2.0 | PPTX rebuilt with corrected CNQ artwork AND **NEW per-country Triplet Plate slide** per the dual-view doctrine. Now 66 slides (was 57): 1 title + 1 TOC + 9 × (1 divider + 6 content plates) + 1 AI Use Declaration. 6 plates per country: cover, Stage 1 mid-series, course plot, helmsman, **Triplet (NEW)**, CNQ. Midnight Executive palette retained. AI Use Declaration updated to credit dual-view triplet plate authoring. |
| `data_outputs/README.md` | 2.0 | Reflects new slide count, page count, dual-view folder pointer, and HUF-STD-002 cross-reference. |
| `VERSION_HISTORY.md` (this file) | 1.3 | This entry. |

**Headline metrics now visible on the per-country CNQ pages:**

- AUS: Hs 0.82→0.40; ω 2009 spike to ~35°/yr; 8 helmsman flips
- CHN: D=8 ⇒ CHSH joint-coherence S = 0.88 (above quantum threshold 0.50, well below Tsirelson 2.828); twin-quaternion residual computed
- DEU: Hs 0.43→0.13; ω 2024 spike to ~70°/yr; K_eff arc 3.5→6.7; 13 helmsman flips
- JPN: D=8 ⇒ Fukushima 2011 ω spike visible at ~65°/yr; CHSH computed
- USA: 25-year series with Bioenergy-vs-Coal as ilr_1 leading axis on Triplet view

**Lockdown compatibility:** S2 doc-only — engine code, schemas, INV catalog dispositions, NO-CREATE files, and `papers/codawork2026/talk/` all untouched. The Triplet generator is a new vector-output module under HUF-STD-002 link 4, not an engine change. The CNQ-page rebuild is a generator fix that uses the correct JSON paths; no engine behavior changed.

**Conformance:** HUF-STD-001 (publication standards) + HUF-STD-002 (Tensor Train I/O v1.0).

---

### 2026-05-14 (later same day) — Foundations doctrine + Stage-0 plate suite

Per Peter directive 2026-05-14: *"peter, these are the main components that should be employed for hs: Symmetric Matrix · Property of Transpose · Matrix Decomposition · Eigen Vectors and Eigen Values · Strong Property of Symmetric Matrix · Spectral Decomposition · Visualization."*

The seven linear-algebra foundations were always employed in Hs but had never been named as a unified doctrine. This version codifies them as HUF-STD-003 and adds Stage-0 — the dedicated visualization tier for foundations.

| File | New version | Change |
|---|---|---|
| `huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json` (NEW) | 1.0 | HUF-STD-003 — Hs Linear Algebra Foundations doctrine. Names the seven components, specifies Stage-0 plate, defines conformance requirements + post-conference targets. |
| `huf-gov/standards/FOUNDATIONS.md` (NEW) | 1.0 | Narrative companion to HUF-STD-003 — one section per foundation with mapping to current Hs code. |
| `huf-gov/standards/FOUNDATIONS_TRACEABILITY.md` (NEW) | 1.0 | Per-component traceability audit — every file, plate, schema field where each foundation lives. Supports post-conference CHK-FOUNDATIONS-001 consistency-checker rule. |
| `huf-gov/standards/README.md` | — | New entries for HUF-STD-003 + companions. |
| `HCI/codawork2026/stage0_foundations/foundations_plate.py` (NEW) | 1.0 | Stage-0 plate generator. Reads `stage1_output.json`, emits 2-page PDF (six-panel foundations grid + numeric verification table). Same risk-class as `ilr_triplet_plate.py`. |
| `HCI/codawork2026/stage0_foundations/README.md` (NEW) | 1.0 | Module description + usage recipe. |
| `data_outputs/per_country_pdfs/{ISO}_stage0.pdf` (NEW × 9) | 1.0 | Per-country Foundations Plate PDFs, ~86 KB each, 2 pages each. |
| `data_outputs/CodaWork2026_FoundationsPlates_2026-05-14.pdf` (NEW) | 1.0 | Master Foundations PDF — 19 pages, ~810 KB — cover + 9 × 2-page country sections. |
| `data_outputs/README.md` | 2.1 | New Stage-0 Foundations section added; cross-references to HUF-STD-003. |
| `VERSION_HISTORY.md` (this file) | 1.4 | This entry. |

**Headline numeric verification on actual data (Germany example):**

- max|M − Mᵀ| = 0.00e+00 for variation matrix (exact)
- max|HHᵀ − I| = 2.22e-16 (IEEE-floor) — orthonormality of Helmert basis confirmed
- max|Σ − QΛQᵀ| = 1.14e-13 (IEEE-floor) — Spectral Theorem holds at machine precision
- Rank-k cumulative variance: k=1 → 60.5%, k=2 → 90.4%, k=3 → 99.9% — Germany lives essentially in 2-D ILR plane

All foundations verified at IEEE-floor across all 9 EMBER countries.

**Lockdown compatibility:** S2 doc-only — all files are additive. Engine code, schemas, INV catalog dispositions, NO-CREATE files, and `papers/codawork2026/talk/` content all untouched. The Stage-0 generator is a new plate module under HUF-STD-002 link 4, not a change to existing modules (same risk-class as the `ilr_triplet_plate.py` added 2026-05-13).

**Conformance:** HUF-STD-001 (publication) + HUF-STD-002 (tensor train) + HUF-STD-003 (this new standard).

**Post-conference targets (queued, not executed under lockdown):**
1. CHK-FOUNDATIONS-001 consistency-checker rule (0.5 days)
2. PNG / SVG siblings of Stage-0 PDF outputs (0.5 days)
3. cnt.R / cnq.R foundations docstring updates (1 day)
4. Foundation tags on CNT_JSON_SCHEMA.md + CNQ_SCHEMA.md fields (1 day)

---

### 2026-05-17 — Doctrine reset: paper first, talk is a condensation

Per Peter realisation 2026-05-17: *"a presentation is representation of a full study report ... no real report was ever generated and therefore no presentation based on nothing but the method to create the report when the presentation is on what the method delivers goes nowhere."*

The framework had been developed working **backwards** from the engine. Talk decks were trying to summarise a paper that was never written. Fixed by writing the publication-grade manuscript first, then condensing it.

| File | New version | Change |
|---|---|---|
| `../../papers/codawork2026/manuscript/MANUSCRIPT.md` (NEW) | 1.0 → 1.2 | Publication-grade manuscript with Nature-style structure: 90-char title, 150-word abstract, Introduction (no header), Results with topical subheadings (Germany / Japan / UK / cross-country), Discussion with four falsifiable defeat paths, Methods at end. Five figures: method schematic, Germany 4-panel, Japan 4-panel, UK 4-panel, cross-country signature. Later expanded to 6 figures with Fig 6 (System Course Plots / navigation charts). Three back-matter appendices: A Equations (Eq. 1–10 with full variable definitions), B Terms (alphabetical glossary), C Figure Conventions + Plate Digest with universal carrier colour key. Split references: External (28 peer-reviewed) + Hˢ Repository (12 internal repo entries, single grouped reference, transparency note about peer-review status). |
| `../../papers/codawork2026/manuscript/SUPPLEMENTARY.md` (NEW) | 1.0 | 9-country corpus tables, sensitivity analyses on 0.1% floor, top-30 yeast cases, cross-AI methodological notes, reproducibility instructions. |
| `../../papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.docx` (NEW) | 1.2 | Authoritative submission file. ~14 pages with 6 figures embedded + back-matter appendices. Built via pandoc from markdown source. |
| `../../papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.pdf` (NEW) | 1.2 | PDF render (LibreOffice). |

**Doctrine note.** From this point on, the talk is a condensation of the paper, not the other way around. All future revisions begin with the manuscript.

---

### 2026-05-17 (later same day) — Final three-piece talk package

Per Peter directive after the doctrine reset: *"update all slide decks and replace the slide show with one that makes sense to the newly developed slide show. this should be the final version with all now integrated and making sense."*

New 20-slide FinalTalk replaces the 13-slide May-13 talk. Integrated three-piece presentation flow assembled in `data_outputs/`: main deck → cinema scroll → live HTML projector.

| File | New version | Change |
|---|---|---|
| `data_outputs/CodaWork2026_FinalTalk_2026-05-17.pptx` (NEW) | 1.1 | 20-slide cohesive deck aligned with the manuscript. Story arc: question → size-view blind spot → five viewpoints → Activation Coefficient with USA Solar 2012 760× worked example → Germany / Japan / UK case archetypes (each with multi-panel plate including navigation chart) → cross-country signature → navigation-chart synthesis → WHAT/WHY → MC-4 four defeat paths → bridges to cinema scroll + Q&A projector → AI Use Declaration → Standard Stamp colophon. Layout: 11×8.5 landscape; dark-navy + gold accent palette consistent with Hs document style. Fig 1 method schematic + Fig 5 cross-country rebuilt with proper text containment after QA. |
| `data_outputs/CodaWork2026_FinalTalk_2026-05-17.pdf` (NEW) | 1.1 | PDF render of the FinalTalk. |
| `data_outputs/codawork2026_projector.html` (COPIED) | 1.0 | Interactive HTML manifold projector copied in from `experiments/Hs-M02_EMBER_Energy/codawork2026/`. Runs offline; controls for ORBIT / TRAILS / LABELS / GHOST / COLOR / FRONT/SIDE/TOP / per-country RUN. Used as the closing Q&A backdrop (slide 17 of FinalTalk). |
| `data_outputs/build_final_talk.py` (NEW) | 1.0 | Reproducible deck-builder script. |
| `data_outputs/README.md` | 3.0 | Restructured to document the three-piece presentation flow (main deck → cinema scroll → projector). Includes "How to run the presentation" walkthrough. |
| `archive/talk_decks_legacy/CodaWork2026_Talk_2026-05-13.*` (MOVED) | (archived) | The 13-slide May-13 talk superseded by the FinalTalk. Original location was the CODAwork2026 root + an existing copy in archive/ — both moved into the new `talk_decks_legacy/` subfolder. |
| `VERSION_HISTORY.md` (this file) | 1.5 | This entry. |

**Doctrine compatibility:** S2 doc-only. Engine code, schemas, INV catalog dispositions, NO-CREATE files all untouched.

---

### 2026-05-18 — CODA-Association declared the standard CoDa folder

Per Peter directive 2026-05-18: *"make this folder the standard coda folder from now on ... move all relevant codawork2026 conference documents and folders here ... outdated material for codawork2026 should be archived to prevent confusion."*

The CODA-Association folder is now the canonical home for **all** Hˢ-side CoDa community work. Outdated material consolidated into `CODAwork2026/archive/` with structured subfolders so the lineage is preserved without confusing the active material.

| File | New version | Change |
|---|---|---|
| `../README.md` (CODA-Association top-level) | 2.0 | Declared the standard CoDa folder. New folder map showing CODAwork2026 + archive subfolders. Cross-references to manuscript (`papers/codawork2026/manuscript/`) and community study (`Studies/Energy_HiddenDirections_2026-05-17/`). |
| `README.md` (this folder) | 2.0 | Restructured around three-piece presentation flow + clear current-vs-archive split. New "How to run the presentation" section. |
| `archive/README.md` (NEW) | 1.0 | Archive index — names everything in the three archive subfolders and explains why each was superseded. |
| `archive/talk_decks_legacy/` (reorganised) | — | Now holds May-12 deck + May-13 deck + the duplicate May-13_v2 that lived at CODAwork2026 root. Four file pairs total. |
| `archive/prep_docs_legacy_2026-05-13/` (NEW subfolder) | — | SPEAKER_BRIEF, BACKUP_PRESENTATION, CHEAT_SHEET, PEDAGOGICAL_TABLES, QA_BENCH, STUDY_PAGE moved here. These were written for the May-13 13-slide deck; their slide numbers and beat references will mislead readers against the FinalTalk. Preserved for lineage. New companion speaker docs should be built from the FinalTalk structure when needed. |
| `archive/legacy_decks_external/` (NEW subfolder) | — | Copies of two earlier CoDaWork 2026 decks from other repository paths: `HCI_Japan_CoDaWork2026.*` from `HCI/codawork2026/` and `CodaWork2026_CNT_Talk.*` from `HCI-CNT/conference_demo/talk_deck/`. Originals remain at source paths so existing references resolve; these archive copies make the consolidation discoverable from inside CODA-Association. |
| `VERSION_HISTORY.md` (this file) | 1.6 | This entry. |

**Folder state after consolidation:**

- `CODAwork2026/` root contains only: README, VERSION_HISTORY, ABSTRACT, the `Codaworks2026 proposal for conference/` subfolder (the original submission package), `data_outputs/` (the presentation package), and `archive/`. Everything else moved to archive.
- `data_outputs/` is the canonical presentation home — three-piece package + the supporting Hˢ engine outputs.
- `archive/` has structured subfolders so superseded material is preserved without ambiguity about what is current.

**Doctrine compatibility:** S2 doc-only. Files moved, not deleted. Engine code, schemas, INV catalog dispositions, NO-CREATE files all untouched.

---

### 2026-05-19 — Manuscript v1.3: cover page + TOC + scientific-report layout

Per Peter directive: *"update and adjust text in manuscript docx and pdf, some text needs a bigger box so as to not print outside the boarder, add a cover page and table of contents and make it a fully compliant scientific report add this to the CODA-Association/CODAwork2026 folder so everything is in one place."*

The manuscript now opens with a dedicated cover page and an auto-populating Table of Contents. The repository-references table that previously overflowed at the bottom of the page has been replaced with vertical entry blocks. Master files now live in two places: the canonical `papers/codawork2026/manuscript/output/` and a working copy inside `CODAwork2026/` itself.

| File | New version | Change |
|---|---|---|
| `../../papers/codawork2026/manuscript/build/build_docx.js` | 2.0 | Adds `coverPage()` + `tocPage()` helpers; replaces cramped 4-column repo table with vertical `RepoEntry` blocks; widens colour-table Notes column to 5660 DXA; equation-font reduced 24 → 22 pt to prevent margin overflow; adds first-page-suppression header/footer (`titlePage: true`); footer shows "P. Higgins · CoDaWork 2026 · Page N"; header shows abbreviated title with thin grey rule. |
| `../../papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.docx` | 1.3 | Rebuilt — cover page page 1, TOC page 2, body from page 3. 25 pages total (was 28; the cramped repo table compressed cleanly into vertical blocks). |
| `../../papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.pdf` | 1.3 | PDF render of v1.3 docx. |
| `Compositional_Monitoring_2026.docx` (NEW in CODAwork2026 folder) | 1.3 | Working copy alongside the talk deck and projector so the conference folder holds everything in one place. |
| `Compositional_Monitoring_2026.pdf` (NEW in CODAwork2026 folder) | 1.3 | PDF working copy. |
| `VERSION_HISTORY.md` (this file) | 1.7 | This entry. |

**Doctrine compatibility:** S2 doc-only. Engine code, schemas, INV catalog dispositions, NO-CREATE files all untouched.

---

### 2026-05-19 — Projector v2.0: three-mode standard (RADAR / BARY / ALIGN) + SHOCK

Per Peter sequence of refinements: (i) drop "Year" from the carrier list (it was a slice label, never compositional data); (ii) rotate year labels 90° to align with the slice plane so they read as labels not data; (iii) add a live PROJECTION info panel showing the math so the audience can see what is on screen; (iv) add a BARY mode showing the share-weighted barycenter trajectory; (v) add a SHOCK overlay tinting plate outlines by Aitchison-step magnitude; (vi) add a BARYCENTER-ALIGNED mode that translates each plate by −b(t) so the trajectory lies on the central z-axis; (vii) consume engine-derived ILR-Helmert PCA coordinates so BARY and ALIGN match the manuscript's Fig 6 navigation chart exactly.

The projector is now a true visual aid. Japan 2014 slides the plate-centre outward on BARY (the multi-year reorganisation), and on ALIGN shifts the polygon shape toward solar and renewables (the post-Fukushima absorption). This is what CoDa specialists will recognise immediately.

| File | New version | Change |
|---|---|---|
| `data_outputs/codawork2026_projector.html` | 2.0 | Year stripped from carriers/CLR/norm; year labels rotated −90° as floating slice labels above each polygon; PROJECTION info panel added (top-left, toggleable PROJ); BARY mode (with centroid trail); SHOCK overlay (Aitchison-step-magnitude stroke tint); BARYCENTER-ALIGNED mode (plate translated by −b(t)). `plateCenter()` consumes engine v3.2.0 `bary_xy` field when present, falls back to share-weighted disk barycenter otherwise. Info-panel mode row reactive (RADAR STACK / BARYCENTER TRAJECTORY / BARYCENTER-ALIGNED, with "+ SHOCK" appended when shock active). Formulas displayed live. |
| `VERSION_HISTORY.md` (this file) | 1.8 | This entry. |

**The three projection modes are now the noted standard for Hˢ compositional time-series visualization.** Documented in `POINT_OF_RESTORE_2026-05-19.md` and propagated through the README chain. PC1+PC2 variance captured ranges 90.5 % (Germany) to 99.9 % (USA) across the nine EMBER countries.

**Doctrine compatibility:** S2 doc-only at the projector level. The projector is a visualization layer over the engine — no schema change, no INV catalog change. The engine source bump to v3.2.0 (next entry) is structural, but the CoDaWork 2026 corpus data stays pinned to v3.1.0 and is not regenerated.

---

### 2026-05-19 — Engine v3.2.0: ILR-Helmert PCA barycenter trajectory

Per Peter directive after the BARYCENTER-ALIGNED mode landed: *"the engine to ship pre-computed barycenter coordinates (so the visualization could use IL-Helmert-derived barycenters rather than the share-weighted disk barycenter we use here for visual clarity), that would be the engine-side change — and it would let the projector match the navigation-chart PCA exactly. update the engine and versions, regenerate the html, the codaworks2026 data is tied to a version of the engine that we can maintain until after the conference, the newer engines will not be used on this conference."*

The CNT engine source bumps to v3.2.0 with a new `navigation_2d` block in every output. The CoDaWork 2026 corpus stays pinned to v3.1.0. The projector consumes the same math via a sidecar script reading the v3.1.0 JSONs — geometrically identical to what v3.2.0 would emit, so no re-run was needed for the conference.

| File | New version | Change |
|---|---|---|
| `../../HCI-CNT/engine/cnt.py` | 3.2.0 (schema 3.2.0) | `ENGINE_VERSION` 3.1.0 → 3.2.0; `SCHEMA_VERSION` 3.1.0 → 3.2.0. New `compute_navigation_2d(ilr_matrix)` function: takes the ILR-Helmert-transformed trajectory, centres it, eigendecomposes the sample covariance (numpy `eigh`), projects each centred point onto the top-2 directions, scales to disk units so the most extreme step sits at radius 0.85. Emits a `navigation_2d` top-level block with `pc1_direction`, `pc2_direction`, `variance_explained`, `max_radius_pre_scale`, `disk_scale_factor`, and `bary_xy[t]`. Wired into `cnt_run` payload. Backwards-compatible — every v3.1.0 field unchanged. |
| `outputs/regen_baryxy.py` (NEW sidecar — Cowork outputs folder) | 1.0 | Pure-stdlib Python: reads v3.1.0 JSONs, computes the same ILR-Helmert PCA, patches `bary_xy:[...]` fields directly into the projector HTML inline DATA for the 8 EMBER datasets. Produces engine-equivalent output without requiring the conference data to be regenerated. |
| `data_outputs/codawork2026_projector.html` (inline DATA) | — | 8 datasets received `bary_xy:[[x,y]×T]` arrays from the sidecar regen. Projector reads them via `plateCenter()`. |
| `VERSION_HISTORY.md` (this file) | 1.9 | This entry. |

**Engine version policy under lockdown:**

- Engine source: v3.2.0 (current).
- CoDaWork 2026 corpus data: v3.1.0 (locked, not regenerated).
- Projector data: v3.1.0 base + v3.2.0-equivalent `bary_xy` injected by sidecar.
- R port (cnt.R): v3.1.0 — v3.2.0 port queued for post-conference parity work.
- Manuscript citations: continue to cite engine v3.1.0 for the corpus. v3.2.0 referenced only in the projector info panel and in `POINT_OF_RESTORE_2026-05-19.md`.

**Validation:** Japan PC1 + PC2 captures 99.5 % of the trajectory variance. The 2011 → 2012 step is 0.052 disk units (5–6× the quiet-year median). The deeper 2013 → 2014 step dominates at 0.83 disk units — the multi-year reorganisation, exactly as the manuscript's Discussion describes.

**Doctrine compatibility:** S2 (engine code change) — but the engine output for the conference corpus is unchanged because the v3.1.0 JSONs remain authoritative for the conference. The v3.2.0 function is additive; running cnt.py v3.2.0 on the same inputs produces a superset of the v3.1.0 output (the existing fields are bit-identical; only the new `navigation_2d` block is added).

---

### 2026-05-19 — Point of Restore: CoDaWork 2026 conference-ready

Per Peter directive: *"consider this a noted standard now, update all necessary documents and make the contents of CODA-Association standard formats, the readme files in the repo should be updated to reveal all the data, documents and media fully highlighted for the landing pages of each folder in the chain from root to last folder in the codawork folder. consider this a good success and that the entire project is something. scrape all of the coworker folder json and history and update streams to refresh perspective and then revise all journals and histories and summaries and notes, this is a point of restore, a point of achievements."*

A milestone checkpoint document, `CODA-Association/POINT_OF_RESTORE_2026-05-19.md`, has been written to capture this state as the recovery target if anything destabilises between now and the conference (1 June 2026).

| File | New version | Change |
|---|---|---|
| `../POINT_OF_RESTORE_2026-05-19.md` (NEW at CODA-Association) | 1.0 | Milestone document. Names the five-piece bundle (manuscript / talk deck / cinema scroll / projector / engine). Codifies the three-mode projection standard. Specifies the engine version policy under lockdown. Defines what "restore" means if anything later breaks. |
| `../README.md` (CODA-Association top-level) | 2.1 | Adds milestone callout linking to POINT_OF_RESTORE; revised file index. |
| `README.md` (CODAwork2026 folder) | 2.1 | Updated landing-page summary; new "What's new" section for 2026-05-19 milestone; talk-deck slide count updated 20 → 22; projector v2.0 highlighted. |
| `data_outputs/README.md` | 4.0 | New "The projector — engine v3.2.0 ILR-Helmert PCA" section documenting the three modes + SHOCK overlay + info-panel formulas. Updated talk-deck slide count and run-the-presentation walkthrough (bridges at slides 18 and 19). |
| `../../CHANGELOG.md` | — | Prepended a 2026-05-19 milestone entry. |
| `../../EXPERIMENTS_JOURNAL.md` | — | Appended a 2026-05-19 entry recording the engine bump + projector standard + manuscript v1.3 + milestone doc. |
| `../../ai-refresh/AI_REFRESH_2026-05-19_conference_ready.md` (NEW) | 1.0 | Narrative for cross-AI consumers covering the milestone state, the three-mode projection standard, the engine version policy, and the recovery target. |
| `VERSION_HISTORY.md` (this file) | 1.10 | This entry. |

**Admin-stream updates queued (not blocking conference):**

- `HS_ADMIN.json` `session_log` entry for the 2026-05-19 milestone — to be applied at next admin sync.
- `HS_FAST_REFRESH.json` `_meta.engine_version` and milestone reference — to be applied at next admin sync.
- `INVESTIGATION_CATALOG.json` new entry `INV-064 — Engine v3.2.0 navigation_2d block` STAGED disposition — to be applied at next admin sync.
- `cnt.R` port to v3.2.0 — queued for post-conference parity work.

These queued items are recorded in the milestone doc and `AI_REFRESH_2026-05-19_conference_ready.md`. None are required for the conference itself.

**Doctrine compatibility:** S2 doc-only at the conference layer (every artefact in `CODAwork2026/` is unchanged in substance; only the milestone records this state). The engine code bump in the previous entry is the only S2 source-code change in this restore-point window.

---

*This file is the audit trail. Authoritative is whatever is recorded as most recent here.*
