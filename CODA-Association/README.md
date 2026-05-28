# CODA-Association — the Hˢ home for compositional-data community work

**Document version:** 2.3 · **Revised:** 2026-05-20 · **Author:** Peter Higgins, Rogue Wave Audio · **Conforms to:** [HUF-STD-001 v1.1](../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json) (Publication) · [HUF-STD-002](../huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) (Tensor Train I/O) · [HUF-STD-003](../huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json) (Linear Algebra Foundations).

This folder is the Hˢ home for compositional-data community work — current talk material, conference packages, correspondence, and CoDaWork submissions. The active material lives at root and inside [`CODAwork2026/`](CODAwork2026/); older versions are kept in `CODAwork2026/archive/` for lineage, not for use.

---

## 🎤 For CoDaWork 2026 attendees

If you are in the audience (or following from anywhere) for *Compositional monitoring of energy-mix drift on the simplex* — open **[`CONFERENCE_ATTENDEES.md`](CONFERENCE_ATTENDEES.md)** on your phone or laptop. It is laid out **slide-by-slide alongside the talk**, with every supporting document, figure, equation, and data file linked in the order you'll hear them referenced. The interactive HTML projector at the end runs in your browser with no install. If you can't see the screen or are joining remotely, you can study the full talk from that page alone.

A **two-side community handout** (single A4 sheet, both sides printed; QR code to this repo top-right of side 1) is available **print-ready in all UN-6 locales** — same layout, localized prose. **Side 1** carries the operationalization pitch (what / why / who / how to engage); **side 2** carries the full operations reference (CoDa core operations, Hˢ supplementary operations, CNQ quaternion operations, closure constraints across domains, apparatus map of *who reads what*, and the symbols legend). The complete ambassador: a real one-sheet that gives a complete picture of what is being done, by which apparatus, and why — on both pages of the only piece of paper a conference visitor needs to take home.

- **PDF (print-ready, 2-side):** [EN](Higgins_Decomposition_Handout_CoDaCommunity.pdf) · [FR](Higgins_Decomposition_Handout_CoDaCommunity.fr.pdf) · [ES](Higgins_Decomposition_Handout_CoDaCommunity.es.pdf) · [RU](Higgins_Decomposition_Handout_CoDaCommunity.ru.pdf) · [ZH](Higgins_Decomposition_Handout_CoDaCommunity.zh.pdf) · [AR](Higgins_Decomposition_Handout_CoDaCommunity.ar.pdf)
- **Markdown (editable source):** [EN](Higgins_Decomposition_Handout_CoDaCommunity.md) · [FR](Higgins_Decomposition_Handout_CoDaCommunity.fr.md) · [ES](Higgins_Decomposition_Handout_CoDaCommunity.es.md) · [RU](Higgins_Decomposition_Handout_CoDaCommunity.ru.md) · [ZH](Higgins_Decomposition_Handout_CoDaCommunity.zh.md) · [AR](Higgins_Decomposition_Handout_CoDaCommunity.ar.md)

English is canonical. FR/ES/RU/ZH/AR non-English versions are drafts pending native expert review per `HCI-CNQ/wrappers/WRAPPER_SCHEMA.md §11.1`. Arabic is rendered right-to-left (side 2 tables included); Chinese uses Simplified glyphs. Mathematical operation names on side 2 (closure, CLR, ILR, Aitchison distance, etc.) are kept in English across all locales per standard mathematical publishing convention; section headings and column labels are fully localized.

## What this folder is

This is the **standard CoDa folder** for the Hˢ repository.

> **🛡️ For skeptical users — verify before you trust.** The Hˢ framework publishes every algorithm in four forms (Python + R + language-agnostic pseudocode + HUF-STD-002 specification) so you can re-implement in your language of choice and verify byte-identically against the published code via `content_sha256` on the three canonical reference inputs. See [`../TRUST_AND_VERIFICATION.md`](../TRUST_AND_VERIFICATION.md) for the 7-step verification protocol. The conference manuscript is the first non-acoustic application of the same engine that has held a 6.02 dB closure invariant at BTL continuously, and the verification path lets you confirm that the manuscript's claims are reproducible from first principles.

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
    ├── SPEAKING_SCRIPT_QA_companion.md  ← side-by-side speech + Q&A bench reading aid (md + pdf)
    ├── SPEAKING_SCRIPT_QA_companion.pdf
    ├── data_outputs/                         ← **the presentation package**
    │   ├── CodaWork2026_Presentation_2026-05-27.pptx  ← THE TALK (single grayscale deck, 21 slides) — START HERE
    │   ├── CodaWork2026_Presentation_2026-05-27.pdf
    │   ├── CodaWork2026_CN-TT_Output_2026-05-28.pdf       ← CN-TT Output — full-corpus raw-data provenance (325 pp); 30s flash-through at the close
    │   ├── CodaWork2026_PremierDataOutput_2026-05-13.pptx ← CN-TT Output editing source (66-slide PPTX)
    │   ├── CodaWork2026_PremierDataOutput_2026-05-13.pdf  ← prior-name PDF, byte-identical content, superseded by CN-TT_Output_2026-05-28.pdf
    │   ├── codawork2026_projector.html        ← live HTML manifold projector; 30s at the close after the CN-TT flash + drives Q&A
    │   ├── CodaWork2026_FoundationsPlates_2026-05-14.pdf  ← Stage-0 Foundations
    │   ├── per_country_json/                  ← canonical engine output per country
    │   ├── per_country_pdfs/                  ← per-country Stage 0/1/2/3/CNQ plates
    │   ├── dual_view/                         ← Stage 1 Section + ILR-Helmert Triplet
    │   └── README.md                          ← presentation flow + reproducibility
    └── archive/                              ← superseded material — preserved for lineage
        ├── README.md                          ← archive index
        ├── talk_decks_pre_presentation_2026-05-27/ ← 13-slide colour deck + its scripts + builders (immediate predecessor)
        ├── talk_decks_pre_13slide_2026-05-24/ ← 10-slide compressed deck + builder + 10-slide script
        ├── talk_decks_pre_10slide_2026-05-20/ ← 22-slide narrative + 12-slide intermediate + builders + 22-slide script
        ├── talk_decks_legacy/                 ← earlier Hˢ-authored decks (May-12, May-13)
        ├── prep_docs_legacy_2026-05-13/       ← speaker prep written for an older talk
        ├── legacy_decks_external/             ← copies of older external decks for record
        ├── manuscript_2026-05-19_msprint_pre-push58/         ← fallback msprint manuscript copy
        └── manuscript_2026-05-19_libreoffice_empty_toc/      ← parked LibreOffice empty-TOC copy
```

## What is current

The **presentation package** lives in `CODAwork2026/data_outputs/`:

1. **`CodaWork2026_Presentation_2026-05-27.pptx`** — **the single grayscale deck, 21 slides** (numbered N / 21, ~14 min spoken): the talk → the rest-of-world finale → the live-projector close, one file. White background, black text, hatched (value + pattern) size-view and Power-Share figures. Pure-science terminology: named on its subject, **deceptive drift**, defined on the slide where it first appears. Side-by-side speech + Q&A bench: [`CODAwork2026/SPEAKING_SCRIPT_QA_companion.md`](CODAwork2026/SPEAKING_SCRIPT_QA_companion.md) / [`.pdf`](CODAwork2026/SPEAKING_SCRIPT_QA_companion.pdf). The 13-slide colour predecessor + scripts are archived at [`CODAwork2026/archive/talk_decks_pre_presentation_2026-05-27/`](CODAwork2026/archive/talk_decks_pre_presentation_2026-05-27/); earlier stages at [`.../talk_decks_pre_13slide_2026-05-24/`](CODAwork2026/archive/talk_decks_pre_13slide_2026-05-24/) and [`.../talk_decks_pre_10slide_2026-05-20/`](CODAwork2026/archive/talk_decks_pre_10slide_2026-05-20/). All preserved for lineage, not for use.
2. **`CodaWork2026_CN-TT_Output_2026-05-28.pdf`** — **CN-TT Output**, 325-page master PDF: the full-corpus raw-data provenance for every claim in the talk. Renamed 2026-05-28 from PremierDataOutput per HUF-STD-002 Tensor Train I/O Standard (CN-TT = CNT / Tensor Train). The talk's close flashes through this PDF for 30 sec (Stage 1 plates, movie-like animation of the simplex points) before handing to the live projector. The six non-case-study countries already appear in the Presentation's rest-of-world finale; the CN-TT Output is the complete output for any Q&A that reaches past the trajectories. Manual plate-by-plate verification — a HUF-system requirement — is done from this artifact. Editing source: `CodaWork2026_PremierDataOutput_2026-05-13.pptx`.
3. **`codawork2026_projector.html`** — interactive HTML manifold projector (runs offline; slide 21 hands first to the CN-TT Output PDF (30 sec flash) and then to this projector (30 sec live) to close the show and drive Q&A).

The companion **manuscript** lives in [`../papers/codawork2026/manuscript/`](../../papers/codawork2026/manuscript/) — the talk is a condensation of the paper, not the other way around. The paper is the foundation document.

The companion **community study deck** lives in [`../../../Studies/Energy_HiddenDirections_2026-05-17/`](../../../../Studies/Energy_HiddenDirections_2026-05-17/) (outside the Hs repo). It is the 20-slide community-friendly walk-through of the same data.

## What is archived

Inside `CODAwork2026/archive/`:

- **`talk_decks_pre_presentation_2026-05-27/`** *(added 2026-05-27)* — the 13-slide colour talk deck (navy/gold) that was active 2026-05-24 → 2026-05-27, with its builders and its two 13-slide speaking-script files. Archived when the single grayscale 21-slide Presentation landed (talk + rest-of-world finale + live-projector close; deceptive-drift terminology; hatched grayscale figures; per-slide numbering). See the folder's own README for full detail.
- **`talk_decks_pre_13slide_2026-05-24/`** *(added 2026-05-24)* — the 10-slide compressed deck that was active 2026-05-20 → 2026-05-24, with its python-pptx builder and 10-slide speaking script. Archived when the 13-slide expansion landed so each country case-study could carry its navigation chart on a dedicated slide at legible size. See the folder's own README for full detail.
- **`talk_decks_pre_10slide_2026-05-20/`** — the refinement trail that led to the 10-slide compressed deck: the 22-slide narrative (2026-05-17), the 12-slide intermediate compression (2026-05-20 morning), their python-pptx builders, the ChatGPT compression-plan JSON, and the 22-slide speaking script. The 21-slide grayscale Presentation is now the only active talk artefact.
- **`talk_decks_legacy/`** — earlier Hˢ-authored decks (2026-05-12, 2026-05-13) that pre-date the 22-slide final-talk family.
- **`prep_docs_legacy_2026-05-13/`** — SPEAKER_BRIEF, BACKUP_PRESENTATION, CHEAT_SHEET, PEDAGOGICAL_TABLES, QA_BENCH, STUDY_PAGE. These were written for the 13-slide May-13 talk; their slide numbers and beat references are no longer accurate. Preserved for lineage; do not use as source for current speaker prep without rebuilding.
- **`legacy_decks_external/`** — copies of earlier CoDaWork 2026 decks from other repository locations (`HCI/codawork2026/HCI_Japan_CoDaWork2026.*`, `HCI-CNT/conference_demo/talk_deck/CodaWork2026_CNT_Talk.*`). Originals remain at their source paths so existing references continue to resolve; these archive copies make the consolidation discoverable from inside CODA-Association.
- **`manuscript_2026-05-19_msprint_pre-push58/`** and **`manuscript_2026-05-19_libreoffice_empty_toc/`** — manuscript render lineage. The msprint version (26 pp, populated TOC) is the conference-distribution authoritative; the LibreOffice export (25 pp, empty-TOC placeholder) is parked here for build-pipeline reproducibility records.

For the full archive index see [`CODAwork2026/archive/README.md`](CODAwork2026/archive/README.md).

## Standards conformance

- **HUF-STD-001 v1.1** (Publication Standards): AI Use Declaration on slide 19 of the talk (the closing synthesis-slide footer) and on the manuscript cover + back-matter. The HUF AI Collective is named in both. Author retains full scientific responsibility.
- **HUF-STD-002** (Tensor Train I/O): All engine outputs (per-country CNT JSON, CNQ JSON, Foundations Plates, Stage 1/2/3, CNQ dashboards) ship as deterministic vector outputs with hash-chained provenance to the raw EMBER CSVs.
- **HUF-STD-003** (Linear Algebra Foundations): The seven foundations are visualised in `CodaWork2026_FoundationsPlates_2026-05-14.pdf` (Stage 0).

## Cross-references

- ⭐ **Flagship master-standard paper** — [`../papers/flagship/GROUND_STATE_AND_TRACTION.md`](../papers/flagship/GROUND_STATE_AND_TRACTION.md) (v2.1, 2026-05-21). The unified-formula statement of the framework's foundation. The CoDaWork 2026 manuscript is the *first non-acoustic application* of the unified formula derived there; the flagship paper carries the mathematical apparatus (Banach contraction, Helmholtz reciprocity, Rayleigh-Sommerfeld, Gershgorin, group-delay-as-rotation, closure invariance) and the lineage from BTL acoustic work to the present Hˢ framework. Read it for *why the conference manuscript works on energy-mix data*.
- **Manuscript** — `papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.docx` (and `.pdf`). Nature-structure with back-matter Appendices A (Equations), B (Terms), C (Plate Digest), and split references (External / Hˢ Repository).
- **Community study** — `Studies/Energy_HiddenDirections_2026-05-17/Energy_HiddenDirections_2026-05-17.pdf`. 20-slide community-friendly version.
- **Original submission** — `CODAwork2026/Codaworks2026 proposal for conference/`. The abstract, the MC-4 packet (v3, 11 pages), and the committee-letter request to present.
- **HUF MC-4 packet** — `CODAwork2026/Codaworks2026 proposal for conference/HUF_MC4_CoDaWork_Packet_v3.pdf`. Cited from the manuscript as `[Repo: MC-4 Packet]`.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*The mathematics is not new; the monitoring application may be.*
