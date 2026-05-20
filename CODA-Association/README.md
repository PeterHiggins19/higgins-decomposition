# CODA-Association — the Hˢ home for compositional-data community work

**Document version:** 2.2 · **Revised:** 2026-05-19 · **Author:** Peter Higgins, Rogue Wave Audio · **Conforms to:** [HUF-STD-001 v1.1](../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json) (Publication) · [HUF-STD-002](../huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) (Tensor Train I/O) · [HUF-STD-003](../huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json) (Linear Algebra Foundations).

This folder is the Hˢ home for compositional-data community work — current talk material, conference packages, correspondence, and CoDaWork submissions. The active material lives at root and inside [`CODAwork2026/`](CODAwork2026/); older versions are kept in `CODAwork2026/archive/` for lineage, not for use.

---

## 🎤 For CoDaWork 2026 attendees

If you are in the audience (or following from anywhere) for *Compositional monitoring of energy-mix drift on the simplex* — open **[`CONFERENCE_ATTENDEES.md`](CONFERENCE_ATTENDEES.md)** on your phone or laptop. It is laid out **slide-by-slide alongside the talk**, with every supporting document, figure, equation, and data file linked in the order you'll hear them referenced. The interactive HTML projector at the end runs in your browser with no install. If you can't see the screen or are joining remotely, you can study the full talk from that page alone.

A one-page community handout (with QR code to this repo) is available **print-ready in all UN-6 locales** — same layout, same single A4 page, localized prose:

- **PDF (print-ready):** [EN](Higgins_Decomposition_Handout_CoDaCommunity.pdf) · [FR](Higgins_Decomposition_Handout_CoDaCommunity.fr.pdf) · [ES](Higgins_Decomposition_Handout_CoDaCommunity.es.pdf) · [RU](Higgins_Decomposition_Handout_CoDaCommunity.ru.pdf) · [ZH](Higgins_Decomposition_Handout_CoDaCommunity.zh.pdf) · [AR](Higgins_Decomposition_Handout_CoDaCommunity.ar.pdf)
- **Markdown (editable source):** [EN](Higgins_Decomposition_Handout_CoDaCommunity.md) · [FR](Higgins_Decomposition_Handout_CoDaCommunity.fr.md) · [ES](Higgins_Decomposition_Handout_CoDaCommunity.es.md) · [RU](Higgins_Decomposition_Handout_CoDaCommunity.ru.md) · [ZH](Higgins_Decomposition_Handout_CoDaCommunity.zh.md) · [AR](Higgins_Decomposition_Handout_CoDaCommunity.ar.md)

English is canonical. FR/ES/RU/ZH/AR non-English versions are drafts pending native expert review per `HCI-CNQ/wrappers/WRAPPER_SCHEMA.md §11.1`. Arabic is rendered right-to-left; Chinese uses Simplified glyphs.

## What this folder is

This is the **standard CoDa folder** for the Hˢ repository.

When in doubt about which file is current, this folder's README and the inner [`CODAwork2026/README.md`](CODAwork2026/README.md) are the source of truth.

## Folder map

```
CODA-Association/
├── README.md                                 ← you are here
└── CODAwork2026/                             ← conference (June 2026)
    ├── README.md                             ← inner folder map + how to run the presentation
    ├── VERSION_HISTORY.md                    ← changes over time
    ├── ABSTRACT.md                           ← committed abstract (the conference letter)
    ├── Codaworks2026 proposal for conference/ ← original submission (abstract + MC-4 packet + committee letter)
    ├── SPEAKING_SCRIPT_10slide.md            ← beat-by-beat speaking script (10-slide deck)
    ├── data_outputs/                         ← **the presentation package**
    │   ├── CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx  ← MAIN TALK (10 slides) — START HERE
    │   ├── CodaWork2026_FinalTalk_10Slide_2026-05-20.pdf
    │   ├── CodaWork2026_FinalTalk_12Slide_2026-05-20.pptx  ← 12-slide variant (preserved sibling)
    │   ├── CodaWork2026_FinalTalk_2026-05-17.pptx          ← 22-slide narrative (preserved sibling)
    │   ├── CodaWork2026_PremierDataOutput_2026-05-13.pptx  ← the cinema scroll (66 slides)
    │   ├── CodaWork2026_PremierDataOutput_2026-05-13.pdf
    │   ├── codawork2026_projector.html        ← live HTML manifold projector for Q&A
    │   ├── CodaWork2026_FoundationsPlates_2026-05-14.pdf  ← Stage-0 Foundations
    │   ├── per_country_json/                  ← canonical engine output per country
    │   ├── per_country_pdfs/                  ← per-country Stage 0/1/2/3/CNQ plates
    │   ├── dual_view/                         ← Stage 1 Section + ILR-Helmert Triplet
    │   └── README.md                          ← presentation flow + reproducibility
    └── archive/                              ← superseded material — preserved for lineage
        ├── README.md                          ← archive index
        ├── talk_decks_legacy/                 ← superseded Hˢ-authored decks
        ├── prep_docs_legacy_2026-05-13/       ← speaker prep written for the old 13-slide talk
        └── legacy_decks_external/             ← copies of older external decks for record
```

## What is current

The **three-piece presentation package** lives in `CODAwork2026/data_outputs/`:

1. **`CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx`** — **10-slide compressed final talk** (what Peter will present, ~8 min spoken). Beat-by-beat speaking script: [`CODAwork2026/SPEAKING_SCRIPT_10slide.md`](CODAwork2026/SPEAKING_SCRIPT_10slide.md). Longer-form variants preserved as siblings (`...12Slide_2026-05-20.pptx`, `...2026-05-17.pptx` for 22 slides) in the same folder as time-budget fallbacks.
2. **`CodaWork2026_PremierDataOutput_2026-05-13.pptx`** — 66-slide cinema scroll (the engine's actual output, played as a movie during Q&A after slide 10).
3. **`codawork2026_projector.html`** — interactive HTML manifold projector (runs offline; Q&A backdrop).

The companion **manuscript** lives in [`../papers/codawork2026/manuscript/`](../../papers/codawork2026/manuscript/) — the talk is a condensation of the paper, not the other way around. The paper is the foundation document.

The companion **community study deck** lives in [`../../../Studies/Energy_HiddenDirections_2026-05-17/`](../../../../Studies/Energy_HiddenDirections_2026-05-17/) (outside the Hs repo). It is the 20-slide community-friendly walk-through of the same data.

## What is archived

Inside `CODAwork2026/archive/`:

- **`talk_decks_legacy/`** — previous Hˢ-authored decks (2026-05-12, 2026-05-13) that have been superseded by the FinalTalk.
- **`prep_docs_legacy_2026-05-13/`** — SPEAKER_BRIEF, BACKUP_PRESENTATION, CHEAT_SHEET, PEDAGOGICAL_TABLES, QA_BENCH, STUDY_PAGE. These were written for the 13-slide May-13 talk; their slide numbers and beat references are no longer accurate against the FinalTalk. Preserved for lineage; do not use as source for current speaker prep without rebuilding.
- **`legacy_decks_external/`** — copies of earlier CoDaWork 2026 decks from other repository locations (`HCI/codawork2026/HCI_Japan_CoDaWork2026.*`, `HCI-CNT/conference_demo/talk_deck/CodaWork2026_CNT_Talk.*`). Originals remain at their source paths so existing references continue to resolve; these archive copies make the consolidation discoverable from inside CODA-Association.

For the full archive index see [`CODAwork2026/archive/README.md`](CODAwork2026/archive/README.md).

## Standards conformance

- **HUF-STD-001 v1.1** (Publication Standards): AI Use Declaration on slide 19 of the FinalTalk; Standard Stamp colophon on slide 20. The HUF AI Collective is named in both. Author retains full scientific responsibility.
- **HUF-STD-002** (Tensor Train I/O): All engine outputs (per-country CNT JSON, CNQ JSON, Foundations Plates, Stage 1/2/3, CNQ dashboards) ship as deterministic vector outputs with hash-chained provenance to the raw EMBER CSVs.
- **HUF-STD-003** (Linear Algebra Foundations): The seven foundations are visualised in `CodaWork2026_FoundationsPlates_2026-05-14.pdf` (Stage 0).

## Cross-references

- **Manuscript** — `papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.docx` (and `.pdf`). Nature-structure with back-matter Appendices A (Equations), B (Terms), C (Plate Digest), and split references (External / Hˢ Repository).
- **Community study** — `Studies/Energy_HiddenDirections_2026-05-17/Energy_HiddenDirections_2026-05-17.pdf`. 20-slide community-friendly version.
- **Original submission** — `CODAwork2026/Codaworks2026 proposal for conference/`. The abstract, the MC-4 packet (v3, 11 pages), and the committee-letter request to present.
- **HUF MC-4 packet** — `CODAwork2026/Codaworks2026 proposal for conference/HUF_MC4_CoDaWork_Packet_v3.pdf`. Cited from the manuscript as `[Repo: MC-4 Packet]`.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*The mathematics is not new; the monitoring application may be.*
