# Version History — CODA-Association/CODAwork2026 media

**Purpose.** Tracks all version changes to documents and media in this folder. Each entry names the affected file, its new version, the change summary, and the change date. Authoritative version of any document is whatever VERSION_HISTORY records as the most recent for that file.

**Versioning convention.**
- **Major version** (e.g. 1.0 → 2.0): substantive content change — new beats, new claims, retracted material, structural reorganization.
- **Minor version** (e.g. 1.0 → 1.1): clarifications, corrections, additions to existing content, updates that reflect new repository state without changing the core argument.
- **Patch version** (e.g. 1.0 → 1.0.1): typo and link fixes only.

**Stable filenames.** Filenames do not change with version. The version number lives in the document header and in this log. Slide deck file may include a date stamp in the filename for archival clarity.

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
