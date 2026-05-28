# CODAwork2026 — conference folder

**Document version:** 2.6 · **Revised:** 2026-05-27 · **Author:** Peter Higgins, Rogue Wave Audio · **Conforms to:** [HUF-STD-001 v1.1](../../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json) · [HUF-STD-002](../../huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) · [HUF-STD-003](../../huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json).

Authoritative home for the CoDaWork 2026 conference (Coimbra, Portugal · 1–5 June 2026). Current material lives at the root of this folder and in [`data_outputs/`](data_outputs/). Older material is in [`archive/`](archive/) with a folder-level explanation — kept for lineage, not for use.

---

## 🎤 For attendees — follow along with the talk

The fastest entry point is **[`CONFERENCE_ATTENDEES.md`](../CONFERENCE_ATTENDEES.md)** (one folder up). It walks through the talk slide-by-slide with every supporting document linked in the order the speaker will reference them. The interactive HTML projector runs in your browser; no install required. If you can't see the screen or are remote, the whole talk runs from that page.

## The conference package — foundation manuscript + three-piece presentation

The manuscript is the foundation document. The three-piece presentation (talk + cinema scroll + projector) sits on top of it; the talk condenses the paper, not the other way around.

| # | Piece | File |
|---|---|---|
| 0 | **Foundation manuscript** — 25-page peer-reviewable paper with cover, TOC, six figures, three appendices | [`Compositional_Monitoring_2026.pdf`](Compositional_Monitoring_2026.pdf) · [`.docx`](Compositional_Monitoring_2026.docx) |
| 1 | **Presentation** — **single grayscale deck, 19 slides** (numbered N / 19): the talk (standard CoDa → how we add time → the three case studies), then the **rest-of-world finale** (the other six countries), then the **live-projector close**. ~13 min spoken + ~1 min HTML close = ~14 min, then 5 min Q&A. White background, black text, hatched (value + pattern) size-view and Power-Share figures for low-ink printing and distance contrast. The talk is named on its subject, **deceptive drift**, defined on the slide where it first appears. Companion: [`SPEAKING_SCRIPT_19slide_QA_companion.md`](SPEAKING_SCRIPT_19slide_QA_companion.md) · [`.pdf`](SPEAKING_SCRIPT_19slide_QA_companion.pdf). | [`data_outputs/CodaWork2026_Presentation_2026-05-27.pdf`](data_outputs/CodaWork2026_Presentation_2026-05-27.pdf) · [`.pptx`](data_outputs/CodaWork2026_Presentation_2026-05-27.pptx). The 13-slide colour predecessor (and its scripts) archived at [`archive/talk_decks_pre_presentation_2026-05-27/`](archive/talk_decks_pre_presentation_2026-05-27/); earlier stages at [`archive/talk_decks_pre_13slide_2026-05-24/`](archive/talk_decks_pre_13slide_2026-05-24/) and [`archive/talk_decks_pre_10slide_2026-05-20/`](archive/talk_decks_pre_10slide_2026-05-20/). |
| 2 | **Full-corpus reference** — 66 slides / 325-page PDF: master cover + 9 country sections × 6 plates each. The six non-case-study countries already appear in the Presentation's rest-of-world finale; this is the complete output for Q&A that reaches past the trajectories. | [`data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf`](data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf) · [`.pptx`](data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pptx) |
| 3 | **Interactive HTML projector** — three projection modes (RADAR / BARY / ALIGN) + SHOCK overlay; runs offline in any browser | [`data_outputs/codawork2026_projector.html`](data_outputs/codawork2026_projector.html) |

## Folder layout

```
CODAwork2026/
├── README.md                          ← this file
├── VERSION_HISTORY.md                 ← chronological revision log (v1.10)
├── ABSTRACT.md                        ← committed abstract (the conference letter)
├── SPEAKING_SCRIPT_19slide_QA_companion.md  ← side-by-side speech + Q&A bench reading aid (19-slide deck)
├── SPEAKING_SCRIPT_19slide_QA_companion.pdf ← PDF render of the reading aid (landscape, large speech font)
├── Compositional_Monitoring_2026.docx ← MANUSCRIPT v1.3 — working copy in this folder
├── Compositional_Monitoring_2026.pdf  ← MANUSCRIPT v1.3 — PDF render
├── Codaworks2026 proposal for conference/  ← original submission package
│   ├── Compositional monitoring of energy-mix drift on the simplex.txt
│   ├── HUF_MC4_CoDaWork_Packet_v3.pdf  (11 pages — the methods-challenge framing)
│   └── CoDaWork 2026 Organising Committee.txt
├── data_outputs/                      ← the presentation package
│   ├── CodaWork2026_Presentation_2026-05-27.pptx   ← Piece 1 — THE TALK (single grayscale deck, 19 slides)
│   ├── CodaWork2026_Presentation_2026-05-27.pdf
│   ├── CodaWork2026_PremierDataOutput_2026-05-13.pptx ← Piece 2 — full-corpus reference (66 slides)
│   ├── CodaWork2026_PremierDataOutput_2026-05-13.pdf
│   ├── codawork2026_projector.html    ← Piece 3 — projector v2.2 (RADAR/BARY/ALIGN + SHOCK); closes the show
│   ├── CodaWork2026_FoundationsPlates_2026-05-14.pdf  (Stage-0 plates × 9 countries)
│   ├── per_country_json/cnt_v3/       ← canonical CNT v3.1.0 output (9 countries)
│   ├── per_country_json/cnq_v2/       ← canonical CNQ v2.0.0 output (9 countries)
│   ├── per_country_pdfs/              ← per-country Stage 0 / 1 / 2-3 / CNQ plates
│   ├── dual_view/                     ← Section + ILR-Helmert Triplet (View A + View B)
│   └── README.md                      ← presentation flow + reproducibility
└── archive/                           ← superseded material — preserved for lineage
    ├── README.md                      ← archive index
    ├── talk_decks_pre_presentation_2026-05-27/  ← 13-slide colour deck + its scripts + builders (immediate predecessor)
    ├── talk_decks_pre_13slide_2026-05-24/  ← 10-slide compressed deck + builder + 10-slide script
    ├── talk_decks_pre_10slide_2026-05-20/  ← 22-slide narrative + 12-slide intermediate + builders + 22-slide script
    ├── talk_decks_legacy/             ← prior Hˢ talk decks (May-12, May-13)
    ├── prep_docs_legacy_2026-05-13/   ← speaker prep written for an older talk
    └── legacy_decks_external/         ← copies of earlier CoDaWork decks from other repo paths
```

## How to run the presentation

1. Open **`data_outputs/CodaWork2026_Presentation_2026-05-27.pptx`** in presenter mode. Walk through the 19-slide arc (numbered N / 19, ~13 min spoken): title (standard CoDa → adding time to the simplex) → the size view's blind spot, where **deceptive drift** is defined (Germany Solar 2005–2006, Activation Coefficient ≈ 333×) → the method diagram (the five named readings, each defined) → the Activation Coefficient → three archetypes → Germany / Japan / UK each as a pair (share-and-structural-work view, then the trajectory on the simplex) → deceptive drift across the corpus (5 of 9) → the **rest-of-world finale** (the other six: Australia / China / India present, France / United States / World absent) → the close (what the stack answers; hand to the live instrument). The bread analogy is kept on the Activation-Coefficient slide, marked as an analogy. The verbal beat-by-beat + Q&A bench is in [`SPEAKING_SCRIPT_19slide_QA_companion.md`](SPEAKING_SCRIPT_19slide_QA_companion.md) / [`.pdf`](SPEAKING_SCRIPT_19slide_QA_companion.pdf) (large speech font for low-light podium reading).
2. **Slide 19 hands to the live instrument.** Open **`data_outputs/codawork2026_projector.html`** in a browser. Click a country code, then **BARY** for the trajectory, **ALIGN** to flatten it onto the central axis, **SHOCK** to highlight Aitchison-step shocks. Take questions with the manifold live. Runs offline; no network required.
3. For any question that reaches past the trajectories, the full-corpus reference **`data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pptx`** holds all 27 plates per country + Stage 2/3 + CNQ for all nine countries.

## What is current

Authoritative material at root and in `data_outputs/`:

- The **abstract** (`ABSTRACT.md`) and the original submission package (the `Codaworks2026 proposal for conference/` subfolder) — these are unchanged from the conference submission.
- The **three-piece presentation package** in `data_outputs/` — see *How to run the presentation* above.
- The **companion engine outputs** in `data_outputs/per_country_json/`, `per_country_pdfs/`, `dual_view/`, and the Foundations Plates PDF — these are the deterministic CNT v3.1.0 / CNQ v2.0.0 engine outputs that the talk decks visualise. Hash-chained to the raw EMBER CSVs.

## What is archived

Everything in `archive/` has been **superseded** by current material. Preserved for lineage; do not use as source for the current presentation. See [`archive/README.md`](archive/README.md) for the full index. Summary:

- **Pre-Presentation deck** (`talk_decks_pre_presentation_2026-05-27/`): the 13-slide colour talk deck (navy/gold) that was active 2026-05-24 → 2026-05-27, with its builders and its two 13-slide speaking-script files. Superseded on 2026-05-27 by the single grayscale 19-slide Presentation (talk + rest-of-world finale + live-projector close; deceptive-drift terminology; hatched grayscale figures; per-slide numbering).
- **Pre-13-slide deck** (`talk_decks_pre_13slide_2026-05-24/`): the 10-slide compressed deck that was active 2026-05-20 → 2026-05-24, with its python-pptx builder and 10-slide speaking script. Superseded by the 13-slide expansion on 2026-05-24 (per-country navigation chart on its own slide at legible size).
- **Pre-10-slide refinement trail** (`talk_decks_pre_10slide_2026-05-20/`): the 22-slide narrative (2026-05-17), the 12-slide intermediate compression (2026-05-20 morning), their python-pptx builders, the original ChatGPT compression-plan JSON, and the 22-slide speaking script. Superseded by the 10-slide compressed deck on 2026-05-20.
- **Prior talk decks** (`talk_decks_legacy/`): May-12 first draft, May-13 thirteen-slide deck (a distinct early lineage — the May-13 talk before the FinalTalk series began).
- **Legacy speaker prep** (`prep_docs_legacy_2026-05-13/`): SPEAKER_BRIEF, BACKUP_PRESENTATION, CHEAT_SHEET, PEDAGOGICAL_TABLES, QA_BENCH, STUDY_PAGE. These reference the May-13 structure; using them against the active 19-slide deck will mislead.
- **External legacy decks** (`legacy_decks_external/`): `HCI_Japan_CoDaWork2026` (Japan-specific iteration), `CodaWork2026_CNT_Talk` (the May-6 first complete deck from `HCI-CNT/conference_demo/talk_deck/`).
- **Manuscript render lineage** (`manuscript_2026-05-19_msprint_pre-push58/`, `manuscript_2026-05-19_libreoffice_empty_toc/`): fallback copies of the conference-distribution manuscript PDF (Microsoft Print To PDF, 26 pp, populated TOC) and the LibreOffice canonical export (25 pp, empty-TOC placeholder).

## Companion documents elsewhere in the repo

- ⭐ **Flagship master-standard paper** — [`../../papers/flagship/GROUND_STATE_AND_TRACTION.md`](../../papers/flagship/GROUND_STATE_AND_TRACTION.md) (v2.1, 2026-05-21). The unified-formula statement of the framework's foundation, with the full lemma chain (Banach contraction, Helmholtz reciprocity, Rayleigh-Sommerfeld, Gershgorin, group-delay-as-rotation, closure invariance under log-ratio). The CoDaWork 2026 manuscript is the *first non-acoustic application* of the unified formula derived there.
- **Manuscript** — [`papers/codawork2026/manuscript/`](../../papers/codawork2026/manuscript/). The peer-reviewable paper that the talk condenses. Nature-style structure with Appendix A (Equations), B (Terms), C (Plate Digest), and split references (External / Hˢ Repository).
- **Community study** — `Studies/Energy_HiddenDirections_2026-05-17/Energy_HiddenDirections_2026-05-17.pdf` (outside the Hs repo). 20-slide community-friendly version of the same data.

## Standards conformance

- **HUF-STD-001 v1.1** — AI Use Declaration on slide 19 of the talk (the closing synthesis-slide footer) and on the manuscript cover + back-matter. The HUF AI Collective is named in both; the named author retains full scientific responsibility.
- **HUF-STD-002** — All engine outputs ship as deterministic vector outputs (PDF / PNG / SVG) with hash-chained provenance.
- **HUF-STD-003** — Seven Linear Algebra Foundations visualised in the Stage-0 plates.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*The mathematics is not new; the monitoring application may be.*
