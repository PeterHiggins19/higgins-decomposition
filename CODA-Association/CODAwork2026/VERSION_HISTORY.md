# Version History — CODA-Association/CODAwork2026 media

**Purpose.** Tracks all version changes to documents and media in this folder. Each entry names the affected file, its new version, the change summary, and the change date. Authoritative version of any document is whatever VERSION_HISTORY records as the most recent for that file.

**Versioning convention.**
- **Major version** (e.g. 1.0 → 2.0): substantive content change — new beats, new claims, retracted material, structural reorganization.
- **Minor version** (e.g. 1.0 → 1.1): clarifications, corrections, additions to existing content, updates that reflect new repository state without changing the core argument.
- **Patch version** (e.g. 1.0 → 1.0.1): typo and link fixes only.

**Stable filenames.** Filenames do not change with version. The version number lives in the document header and in this log. Slide deck file may include a date stamp in the filename for archival clarity.

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

*This file is the audit trail. Authoritative is whatever is recorded as most recent here.*
