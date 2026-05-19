# CODA-Association — the Hˢ home for compositional-data community work

**Document version:** 2.1 — point-of-restore milestone (2026-05-19)
**Document status:** authoritative folder index — the standard CoDa folder for the Hˢ repository
**Revised:** 2026-05-19 — milestone checkpoint: projector v2.0 with three-mode standard (RADAR / BARY / ALIGN), engine v3.2.0 ILR-Helmert PCA barycenters, manuscript v1.3 with cover page + TOC. See [`POINT_OF_RESTORE_2026-05-19.md`](POINT_OF_RESTORE_2026-05-19.md).
**Author:** Peter Higgins, Rogue Wave Audio
**Conforms to:** HUF Publication Standards (HUF-STD-001 v1.1); HUF Tensor Train I/O Standard (HUF-STD-002); HUF Linear Algebra Foundations (HUF-STD-003)

---

## 🏁 Point of restore — CoDaWork 2026 conference-ready

This folder is in conference-ready state for CoDaWork 2026 (Coimbra, Portugal · 1–5 June 2026). The five-piece bundle — manuscript, talk deck, cinema scroll, interactive HTML projector, deterministic engine — is locked and reproducible. The projector is now a true visual aid for compositional time-series, with three projection modes (RADAR / BARY / ALIGN) reading engine v3.2.0 ILR-Helmert PCA barycenter coordinates. Japan 2014 visibly registers the multi-year reorganisation.

📌 **Read first:** [`POINT_OF_RESTORE_2026-05-19.md`](POINT_OF_RESTORE_2026-05-19.md) — the milestone document; the recovery target if anything later destabilises.

---

## What this folder is

This is the **standard CoDa folder** for the Hˢ repository. Anything tied to the compositional-data community — current talk material, conference packages, community correspondence, CoDaWork submissions — lives here. Older versions of the same material are archived inside the folder structure (not deleted) so the lineage stays traceable while the current state remains unambiguous.

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
    ├── data_outputs/                         ← **the presentation package**
    │   ├── CodaWork2026_FinalTalk_2026-05-17.pptx  ← main talk (20 slides) — START HERE
    │   ├── CodaWork2026_FinalTalk_2026-05-17.pdf
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

1. **`CodaWork2026_FinalTalk_2026-05-17.pptx`** — 20-slide talk (the story).
2. **`CodaWork2026_PremierDataOutput_2026-05-13.pptx`** — 66-slide cinema scroll (the engine's actual output, played as a movie).
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
