# Archive — superseded CoDaWork 2026 material

**Updated:** 2026-05-28 — the prior 21-slide Presentation PPTX + PDF (2026-05-27 layout) archived after Peter's PDF-only directive; the **single grayscale 21-slide PDF, Letter landscape** (`CodaWork2026_Presentation_2026-05-28.pdf`) is now the active conference deck — same arc as before (talk + rest-of-world finale + live-projector close, deceptive-drift terminology, hatched grayscale figures, per-slide numbering) but with the layout rebuilt to fully use the expanded canvas (figures up to 10.20 in wide; fonts +20 % for distance reading).
**Purpose:** preserve the lineage of CoDaWork 2026 work without confusing the active material.

Everything in this folder has been **superseded** by current material elsewhere in `CODAwork2026/`. It is preserved here so reviewers can trace the lineage of the work, but it should **not** be used as source for the current presentation.

For current material see the parent folder's [`README.md`](../README.md) and the [`data_outputs/`](../data_outputs/) presentation package.

## Folder layout

### `talk_decks_pre_pdfonly_2026-05-28/` *(added 2026-05-28)*

The 21-slide grayscale Presentation as it stood **just before** the 2026-05-28 switch to PDF-only delivery + the layout-expansion rebuild. Holds the prior `CodaWork2026_Presentation_2026-05-27.pptx` (3.3 MB) and its rendered `.pdf` (2.9 MB) — same 21-slide content as the active 2026-05-28 PDF, but with the older v10 layout (figures under-using canvas width; some sub-7-pt fonts at distance).

| File | Date | Role at time of writing |
|---|---|---|
| `CodaWork2026_Presentation_2026-05-27.pptx` | 2026-05-27 | The last PPTX shipped as a public artifact. |
| `CodaWork2026_Presentation_2026-05-27.pdf` | 2026-05-27 | The rendered PDF from that PPTX. |

Successor: [`../data_outputs/CodaWork2026_Presentation_2026-05-28.pdf`](../data_outputs/CodaWork2026_Presentation_2026-05-28.pdf) (PDF-only). See the folder-level [`README.md`](talk_decks_pre_pdfonly_2026-05-28/README.md) for full detail.

### `talk_decks_pre_presentation_2026-05-27/` *(added 2026-05-27)*

The 13-slide colour talk deck (navy/gold) that lived as the active conference deck 2026-05-24 → 2026-05-27, with its two python-pptx builders and its two 13-slide speaking-script files (the plain script and the speech + Q&A-bench companion). Replaced by the single grayscale 21-slide Presentation.

| File | Date | Role at time of writing |
|---|---|---|
| `CodaWork2026_FinalTalk_13Slide_2026-05-24.pptx` / `.pdf` | 2026-05-24 | The 13-slide colour talk deck — three case studies, each a share-and-work + navigation-chart pair. |
| `build_final_talk_13slide.py` / `build_final_talk_13slide_v2.py` | 2026-05-24/25 | python-pptx builders for the 13-slide deck. |
| `SPEAKING_SCRIPT_13slide.md` | 2026-05-24 | Plain per-slide speaking script. |
| `SPEAKING_SCRIPT_13slide_QA_companion.md` / `.pdf` | 2026-05-25 | Two-column speech + Q&A-bench companion. |
| `README_package_snapshot_2026-05-20.pdf` | 2026-05-20 | Stale rendered snapshot of an earlier data_outputs README (10-slide era). |

Successor: [`../data_outputs/CodaWork2026_Presentation_2026-05-27.pptx`](../data_outputs/CodaWork2026_Presentation_2026-05-27.pptx) with [`../SPEAKING_SCRIPT_QA_companion.md`](../SPEAKING_SCRIPT_QA_companion.md). See the folder-level [`README.md`](talk_decks_pre_presentation_2026-05-27/README.md) for full detail.

### `talk_decks_pre_13slide_2026-05-24/` *(added 2026-05-24)*

The 10-slide compressed deck that lived as the active conference deck 2026-05-20 → 2026-05-24, with its builder and speaking script. Replaced by the 13-slide expanded deck so each country case-study could carry its navigation chart on a dedicated slide at legible size (the 2.6″-wide nav chart crammed onto the right margin of the 10-slide pairings was not readable from the back of the conference room).

| File | Date | Slides | Role at time of writing |
|---|---|---|---|
| `CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx` / `.pdf` | 2026-05-20 | 10 | The compressed final-talk deck — Germany / Japan / UK each on one slide with a small nav-chart inset. |
| `build_final_talk_10slide.py` | 2026-05-20 | — | python-pptx builder for the 10-slide deck. |
| `SPEAKING_SCRIPT_10slide.md` | 2026-05-20 | — | Beat-by-beat speaking script for the 10-slide pacing. Slide numbers do not apply to the 13-slide expansion. |

Successor: [`../data_outputs/CodaWork2026_FinalTalk_13Slide_2026-05-24.pptx`](../data_outputs/CodaWork2026_FinalTalk_13Slide_2026-05-24.pptx) with [`../SPEAKING_SCRIPT_13slide.md`](../SPEAKING_SCRIPT_13slide.md). See the folder-level [`README.md`](talk_decks_pre_13slide_2026-05-24/README.md) for full detail.

### `talk_decks_pre_10slide_2026-05-20/` *(added 2026-05-20)*

The immediate refinement trail that led to the 10-slide compressed final talk. Each stage is preserved with its own builder so the lineage is reproducible.

| File | Date | Slides | Role at time of writing |
|---|---|---|---|
| `CodaWork2026_FinalTalk_2026-05-17.pptx` / `.pdf` | 2026-05-17 | 22 | Original full narrative final-talk deck — story arc with per-country navigation slides, MC-4 falsifiability slide, "Inspect the instrument" closer. |
| `CodaWork2026_FinalTalk_12Slide_2026-05-20.pptx` / `.pdf` | 2026-05-20 (am) | 12 | Intermediate compression — built from the ChatGPT-prepared `CompressionPlan.json`. Kept the MC-4 falsifiability slide and the closer. |
| `CodaWork2026_FinalTalk_12Slide_CompressionPlan.json` | 2026-05-20 | — | The 22→12 compression plan (slide-by-slide rationale). |
| `build_final_talk.py`, `build_final_talk_v2.py` | 2026-05-17 | — | python-pptx builders for the 22-slide narrative. |
| `build_final_talk_12slide.py` | 2026-05-20 | — | python-pptx builder for the 12-slide intermediate. |
| `SPEAKING_SCRIPT.md` | 2026-05-19 | — | Beat-by-beat speaking script for the **22-slide** deck. Slide numbers do not apply to the 10-slide or 13-slide finals. |

Successor at the time of archival: the 10-slide deck (since itself archived 2026-05-24; see `talk_decks_pre_13slide_2026-05-24/` above for the current active 13-slide deck).

### `talk_decks_legacy/`

Earlier Hˢ-authored talk decks, pre-dating the 22-slide narrative family.

| File | Date | Purpose |
|---|---|---|
| `CodaWork2026_Talk_2026-05-12.pptx` / `.pdf` | 2026-05-12 | First draft of the conference talk; ~12 slides; superseded by the 13-slide deck the next day. |
| `CodaWork2026_Talk_2026-05-13.pptx` / `.pdf` | 2026-05-13 | The 13-slide CoDaWork talk that lived as the conference deck until 2026-05-17. Polished through 2026-05-16 commitment audit. Replaced by the 22-slide FinalTalk after the doctrine reset described in the manuscript-first approach. |
| `CodaWork2026_Talk_2026-05-13_v2.*` | 2026-05-13 | Duplicate kept in the active root until 2026-05-18 consolidation; moved here on the same day. |

### `prep_docs_legacy_2026-05-13/`

Speaker-prep documents written for the 13-slide May-13 talk. The slide numbers and beat references in these docs apply to the **old** talk and will mislead anyone reading them against the current 10-slide deck. Preserved here as the historical record of how that talk was developed.

| File | Purpose at time of writing |
|---|---|
| `BACKUP_PRESENTATION.md` | Fallback narration if A/V failed during the talk. |
| `CHEAT_SHEET.md` | One-page speaker reminder for the May-13 talk. |
| `PEDAGOGICAL_TABLES.md` | Aitchison-to-SU(2) 10-step + Helmsman 6-step tables for Q&A depth. |
| `QA_BENCH.md` | Q&A bench cards — extended material if room asked specific questions. |
| `SPEAKER_BRIEF.md` | Executive summary + per-country + per-beat strategic compass. |
| `STUDY_PAGE.md` | "Moot method" study sheet for rehearsal. |

If the 10-slide deck needs companion speaker docs, build new ones aligned with the 10-slide structure. Reusing these without rebuilding will mislead.

### `legacy_decks_external/`

Earlier Hˢ-authored CoDaWork 2026 decks from other repository locations, copied here for completeness. Originals remain at their source paths so existing references continue to work.

| File | Source path | Date | Purpose |
|---|---|---|---|
| `CodaWork2026_CNT_Talk.pptx` / `.pdf` | `HCI-CNT/conference_demo/talk_deck/` | 2026-05-06 | The first complete CoDaWork 2026 talk deck — 10 slides built before the CODA-Association folder existed. Pre-dates the MC-4 packet sharpening. |
| `HCI_Japan_CoDaWork2026.pptx` / `.pdf` | `HCI/codawork2026/` | (earlier) | Japan-specific CNT deck. Subject matter has since been absorbed into the manuscript's Japan deep-dive (Fig 3) and into Slide 7 of the current 10-slide talk. |

### `manuscript_2026-05-19_msprint_pre-push58/`

Fallback copy of the conference-distribution manuscript (`Compositional_Monitoring_2026.docx` + Microsoft Print To PDF render, 26 pp, populated TOC). Byte-identical to the working copy currently at `../Compositional_Monitoring_2026.{docx,pdf}`. See the folder-level [`README.md`](manuscript_2026-05-19_msprint_pre-push58/README.md) for the working-copy correction history.

### `manuscript_2026-05-19_libreoffice_empty_toc/`

The LibreOffice headless export of the manuscript (25 pp, empty-TOC placeholder). Parked here because the headless build pipeline does not auto-populate Word's TOC field. The canonical artefact at `papers/codawork2026/manuscript/output/` is the same render; this archive copy exists so the round-trip is discoverable from inside CODA-Association.

---

*The instrument reads.  The expert decides.  The hashes carry the receipts.  The vocabulary holds the line.*
*Old versions held here so the new ones can be trusted as current.*
