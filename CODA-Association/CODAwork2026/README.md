# CODAwork2026 — conference folder

**Document version:** 2.3 · **Revised:** 2026-05-20 · **Author:** Peter Higgins, Rogue Wave Audio · **Conforms to:** [HUF-STD-001 v1.1](../../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json) · [HUF-STD-002](../../huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) · [HUF-STD-003](../../huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json).

Authoritative home for the CoDaWork 2026 conference (Coimbra, Portugal · 1–5 June 2026). Current material lives at the root of this folder and in [`data_outputs/`](data_outputs/). Older material is in [`archive/`](archive/) with a folder-level explanation — kept for lineage, not for use.

---

## 🎤 For attendees — follow along with the talk

The fastest entry point is **[`CONFERENCE_ATTENDEES.md`](../CONFERENCE_ATTENDEES.md)** (one folder up). It walks through the talk slide-by-slide with every supporting document linked in the order the speaker will reference them. The interactive HTML projector runs in your browser; no install required. If you can't see the screen or are remote, the whole talk runs from that page.

## The presentation in three pieces

| # | Piece | File |
|---|---|---|
| 1 | **Manuscript** — 25-page peer-reviewable paper with cover, TOC, six figures, three appendices | [`Compositional_Monitoring_2026.pdf`](Compositional_Monitoring_2026.pdf) · [`.docx`](Compositional_Monitoring_2026.docx) |
| 2 | **Talk deck** — **10-slide compressed final**, ~8 min spoken + cinema scroll + projector demo during Q&A. Spoken script in [`SPEAKING_SCRIPT_10slide.md`](SPEAKING_SCRIPT_10slide.md). | [`data_outputs/CodaWork2026_FinalTalk_10Slide_2026-05-20.pdf`](data_outputs/CodaWork2026_FinalTalk_10Slide_2026-05-20.pdf) · [`.pptx`](data_outputs/CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx). Earlier 22-slide narrative and 12-slide intermediate compression archived for lineage at [`archive/talk_decks_pre_10slide_2026-05-20/`](archive/talk_decks_pre_10slide_2026-05-20/). |
| 3 | **Cinema scroll** — 66 slides / 325-page PDF: master cover + 9 country sections × 6 plates each | [`data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf`](data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf) · [`.pptx`](data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pptx) |
| 4 | **Interactive HTML projector** — three projection modes (RADAR / BARY / ALIGN) + SHOCK overlay; runs offline in any browser | [`data_outputs/codawork2026_projector.html`](data_outputs/codawork2026_projector.html) |

## Folder layout

```
CODAwork2026/
├── README.md                          ← this file
├── VERSION_HISTORY.md                 ← chronological revision log (v1.10)
├── ABSTRACT.md                        ← committed abstract (the conference letter)
├── Compositional_Monitoring_2026.docx ← MANUSCRIPT v1.3 — working copy in this folder
├── Compositional_Monitoring_2026.pdf  ← MANUSCRIPT v1.3 — PDF render
├── Codaworks2026 proposal for conference/  ← original submission package
│   ├── Compositional monitoring of energy-mix drift on the simplex.txt
│   ├── HUF_MC4_CoDaWork_Packet_v3.pdf  (11 pages — the methods-challenge framing)
│   └── CoDaWork 2026 Organising Committee.txt
├── data_outputs/                      ← the THREE-PIECE presentation package
│   ├── CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx   ← Piece 1 — THE TALK (10 slides)
│   ├── CodaWork2026_FinalTalk_10Slide_2026-05-20.pdf
│   ├── CodaWork2026_PremierDataOutput_2026-05-13.pptx ← Piece 2 — cinema scroll (66 slides)
│   ├── CodaWork2026_PremierDataOutput_2026-05-13.pdf
│   ├── codawork2026_projector.html    ← Piece 3 — projector v2.0 (RADAR/BARY/ALIGN + SHOCK)
│   ├── CodaWork2026_FoundationsPlates_2026-05-14.pdf  (Stage-0 plates × 9 countries)
│   ├── per_country_json/cnt_v3/       ← canonical CNT v3.1.0 output (9 countries)
│   ├── per_country_json/cnq_v2/       ← canonical CNQ v2.0.0 output (9 countries)
│   ├── per_country_pdfs/              ← per-country Stage 0 / 1 / 2-3 / CNQ plates
│   ├── dual_view/                     ← Section + ILR-Helmert Triplet (View A + View B)
│   ├── build_final_talk_10slide.py    ← reproducible 10-slide deck builder
│   └── README.md                      ← presentation flow + reproducibility
└── archive/                           ← superseded material — preserved for lineage
    ├── README.md                      ← archive index
    ├── talk_decks_pre_10slide_2026-05-20/  ← 22-slide narrative + 12-slide intermediate + their builders + old 22-slide script
    ├── talk_decks_legacy/             ← prior Hˢ talk decks (May-12, May-13)
    ├── prep_docs_legacy_2026-05-13/   ← speaker prep written for the old 13-slide talk
    └── legacy_decks_external/         ← copies of earlier CoDaWork decks from other repo paths
```

## How to run the presentation

1. Open **`data_outputs/CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx`** in presenter mode. Walk through the 10-slide story arc (~8 min 20 sec spoken). The arc walks the audience through: title + question + contact → size view's blind spot (USA Solar 760× hook) → five viewpoints in one schematic → Activation Coefficient (the yeast factor) → three archetypes preview → Germany (continuous arc) → Japan (shock + reorganisation) → UK (regime change) → 5-of-9 cross-country signature → synthesis (what the stack answers). Slides 6 / 7 / 8 (Germany / Japan / UK) weighted at 75 sec each — the cases are where the room sees the instrument do work. MC-4 falsifiability and the "Inspect the instrument" closer were dropped from the deck; both still live in the manuscript. The verbal beat-by-beat is in [`SPEAKING_SCRIPT_10slide.md`](SPEAKING_SCRIPT_10slide.md).
2. After slide 10, switch the projector display to **`data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pptx`**. Auto-advance at ~1 second per slide, or scroll manually (~1.5 min as a movie). The 66-slide reel is the engine's actual output — pause anywhere.
3. Then open **`data_outputs/codawork2026_projector.html`** in a browser as the Q&A backdrop. Click **JPN**, then **BARY** for the trajectory view, **ALIGN** to flatten it onto the central axis, **SHOCK** to highlight Aitchison-step shocks. Take questions with the manifold live. Runs offline; no network required.

## What is current

Authoritative material at root and in `data_outputs/`:

- The **abstract** (`ABSTRACT.md`) and the original submission package (the `Codaworks2026 proposal for conference/` subfolder) — these are unchanged from the conference submission.
- The **three-piece presentation package** in `data_outputs/` — see *How to run the presentation* above.
- The **companion engine outputs** in `data_outputs/per_country_json/`, `per_country_pdfs/`, `dual_view/`, and the Foundations Plates PDF — these are the deterministic CNT v3.1.0 / CNQ v2.0.0 engine outputs that the talk decks visualise. Hash-chained to the raw EMBER CSVs.

## What is archived

Everything in `archive/` has been **superseded** by current material. Preserved for lineage; do not use as source for the current presentation. See [`archive/README.md`](archive/README.md) for the full index. Summary:

- **Pre-10-slide refinement trail** (`talk_decks_pre_10slide_2026-05-20/`): the 22-slide narrative (2026-05-17), the 12-slide intermediate compression (2026-05-20 morning), their python-pptx builders, the original ChatGPT compression-plan JSON, and the 22-slide speaking script. Superseded by the 10-slide compressed final on 2026-05-20.
- **Prior talk decks** (`talk_decks_legacy/`): May-12 first draft, May-13 thirteen-slide deck.
- **Legacy speaker prep** (`prep_docs_legacy_2026-05-13/`): SPEAKER_BRIEF, BACKUP_PRESENTATION, CHEAT_SHEET, PEDAGOGICAL_TABLES, QA_BENCH, STUDY_PAGE. These reference the May-13 13-slide structure; using them against the 10-slide deck will mislead.
- **External legacy decks** (`legacy_decks_external/`): `HCI_Japan_CoDaWork2026` (Japan-specific iteration), `CodaWork2026_CNT_Talk` (the May-6 first complete deck from `HCI-CNT/conference_demo/talk_deck/`).
- **Manuscript render lineage** (`manuscript_2026-05-19_msprint_pre-push58/`, `manuscript_2026-05-19_libreoffice_empty_toc/`): fallback copies of the conference-distribution manuscript PDF (Microsoft Print To PDF, 26 pp, populated TOC) and the LibreOffice canonical export (25 pp, empty-TOC placeholder).

## Companion documents elsewhere in the repo

- **Manuscript** — [`papers/codawork2026/manuscript/`](../../papers/codawork2026/manuscript/). The peer-reviewable paper that the talk condenses. Nature-style structure with Appendix A (Equations), B (Terms), C (Plate Digest), and split references (External / Hˢ Repository).
- **Community study** — `Studies/Energy_HiddenDirections_2026-05-17/Energy_HiddenDirections_2026-05-17.pdf` (outside the Hs repo). 20-slide community-friendly version of the same data.

## Standards conformance

- **HUF-STD-001 v1.1** — AI Use Declaration on slide 10 of the talk (synthesis-slide footer) and on the manuscript cover + back-matter. The HUF AI Collective is named in both; the named author retains full scientific responsibility.
- **HUF-STD-002** — All engine outputs ship as deterministic vector outputs (PDF / PNG / SVG) with hash-chained provenance.
- **HUF-STD-003** — Seven Linear Algebra Foundations visualised in the Stage-0 plates.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*The mathematics is not new; the monitoring application may be.*
