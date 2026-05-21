# CoDaWork 2026 — Final Presentation Package

**Document version:** 6.0 · **Updated:** 2026-05-20 · **Author:** Peter Higgins, Rogue Wave Audio · **Conforms to:** [HUF-STD-001 v1.1](../../../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json) · [HUF-STD-002](../../../huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) · [HUF-STD-003](../../../huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json).

The three-piece presentation package: the **10-slide compressed final-talk deck**, a 66-slide cinema scroll of the engine's raw output, and an interactive HTML projector for live Q&A. Audience-facing entry point: **[`../../CONFERENCE_ATTENDEES.md`](../../CONFERENCE_ATTENDEES.md)** — a slide-by-slide follow-along.

The 10-slide deck is **the** talk. Earlier-stage refinements (22-slide narrative, 12-slide intermediate compression, their builders, the 22-slide speaking script) have been archived for lineage at [`../archive/talk_decks_pre_10slide_2026-05-20/`](../archive/talk_decks_pre_10slide_2026-05-20/) — preserved for traceability, not for use.

---

## The presentation as three pieces

The CoDaWork 2026 presentation runs as **three stacked artefacts**, each doing a specific job:

**Piece 1 — the talk deck (story).**
[`CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx`](CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx) — **10 slides**, ~1.5 MB
[`CodaWork2026_FinalTalk_10Slide_2026-05-20.pdf`](CodaWork2026_FinalTalk_10Slide_2026-05-20.pdf) — read-only companion
Built 2026-05-20. Compressed from the 22-slide narrative deck via a ChatGPT-prepared plan and a final pass that drops the MC-4 falsifiability slide and the "Inspect the instrument" closer in favour of moving all contact details onto slide 1.
**Story arc (10 slides):** title + question + contact → size-view blind spot (USA Solar 760× hook) → five viewpoints in one schematic → Activation Coefficient (yeast factor + formula) → three archetypes overview → Germany (continuous arc) → Japan (shock + reorganisation) → UK (regime change) → 5-of-9 cross-country signature → synthesis ("what the stack answers") with AI Use Declaration footer.
**Timing:** ~8 min 20 sec spoken across the 10 slides + ~1.5 min cinema scroll + ~1 min projector demo = ~11.5 min apparatus time, leaving ~3.5 min Q&A in a 15-minute slot. Slides 6 / 7 / 8 (Germany / Japan / UK) weighted at 75 sec each — the cases are where the room sees the instrument do work.

**Earlier stages archived for lineage.** The 22-slide narrative, 12-slide intermediate, their builders, the original compression-plan JSON, and the 22-slide speaking script live at [`../archive/talk_decks_pre_10slide_2026-05-20/`](../archive/talk_decks_pre_10slide_2026-05-20/) with a folder-level README. Preserved for traceability; do not use against the 10-slide deck — slide numbers will not match.

**Piece 2 — the data scroll (movie).**
[`CodaWork2026_PremierDataOutput_2026-05-13.pptx`](CodaWork2026_PremierDataOutput_2026-05-13.pptx) — 66 slides, 6.3 MB
[`CodaWork2026_PremierDataOutput_2026-05-13.pdf`](CodaWork2026_PremierDataOutput_2026-05-13.pdf) — 325-page master PDF
Master cover + 9 country sections × 6 plates each (cover · Stage 1 Section · system course plot · helmsman · ILR-Helmert Triplet · CNQ dashboard). Hash-chained to the input CSVs. Designed to be **scrolled at speed** as a Q&A backdrop after slide 10 — the audience sees the engine's actual output as a movie. Pause anywhere.

**Piece 3 — the closing projector (live) — v2.0.**
[`codawork2026_projector.html`](codawork2026_projector.html) — interactive 3-D manifold projector, runs offline in a browser. **Three projection modes** (RADAR / BARY / ALIGN) plus an Aitchison-step **SHOCK** overlay. Consumes engine v3.2.0 ILR-Helmert PCA barycenter coordinates so BARY and ALIGN match the manuscript's Fig 6 navigation chart exactly. A live PROJECTION info panel (top-left, toggleable) shows the math being applied. See "The projector — engine v3.2.0 ILR-Helmert PCA" below for full detail.

## How to run the presentation

1. Open `CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx` in presenter mode. Walk through the 10-slide story arc using [`../SPEAKING_SCRIPT_10slide.md`](../SPEAKING_SCRIPT_10slide.md) for timing (≈ 8 minutes spoken, slides 6/7/8 weighted for the case studies).
2. Immediately after slide 10, switch the projector display to `CodaWork2026_PremierDataOutput_2026-05-13.pptx`. Auto-advance at ~1 second per slide or scroll manually. The 66-slide reel is the engine's actual output — *"Pause me anywhere."*
3. Open `codawork2026_projector.html` in a browser (Chrome / Firefox / Safari all work; no network required) as the Q&A backdrop. Click **JPN**, then **BARY** for the trajectory view, **ALIGN** to flatten it onto the central axis, **SHOCK** to highlight Aitchison-step shocks. Take questions with the manifold live.

## The projector — engine v3.2.0 ILR-Helmert PCA

The HTML projector is now a true visual aid for compositional time-series. It loads with the inline CNT v3.1.0 corpus data + engine-derived `bary_xy` arrays produced by the v3.2.0 `navigation_2d` block. Three projection modes are available, switchable from the top-right control row.

### Mode 1 — RADAR STACK *(default)*
**Plate centre:** fixed at (0, 0, z(t)) for every year.
**Reads:** the per-year radar/spider snapshot stacked along time. Each carrier sits at a fixed angle around the disk; its vertex radius is its min-max-normalized CLR. Good first read on "which carriers swelled when".

### Mode 2 — BARYCENTER TRAJECTORY  *(click BARY)*
**Plate centre:** b(t) = PCA₂( Vᵀ·CLR(t) − μ ) · 0.85R   (engine v3.2.0 ILR-Helmert PCA)
**Reads:** the spine of plate-centres bends through space, tracing the composition's trajectory on the simplex's principal 2-D subspace. A bright trail connects consecutive centroids; the current year is highlighted gold. This is the CoDa-native answer to "where is the composition going".

### Mode 3 — BARYCENTER-ALIGNED  *(click ALIGN)*
**Plate centre:** (0, 0, z(t)); polygon vertices shifted by −b(t).
**Reads:** the barycenter trajectory is mathematically forced onto the central z-axis. What survives in the polygon shape is the structural variation around each year's own centroid. The standard CoDa "centred" view — every composition observed relative to its own geometric centre.

### SHOCK overlay *(combinable with any of the three modes)*
Tints each plate's outline red proportional to the Aitchison-step distance from the previous year. Quiet years stay in the country's base colour; external-shock years (Japan 2011 → 2012, the multi-year 2013–2014 reorganisation) light up obviously. Magnitude precomputed once per dataset on load.

### Variance captured by the 2-D projection (per country)

PC1 + PC2 across the nine EMBER countries:

| Country | PC1 % | PC2 % | PC1+PC2 |
|---|---|---|---|
| AUS | — | — | (not loaded into projector) |
| CHN | 93.1 | 5.9 | 99.0 % |
| DEU | 58.9 | 31.6 | 90.5 % |
| FRA | 92.7 | 4.0 | 96.7 % |
| GBR | 75.9 | 22.5 | 98.4 % |
| IND | 97.0 | 2.3 | 99.3 % |
| JPN | 89.6 | 9.6 | 99.2 % |
| USA | 98.3 | 1.6 | 99.9 % |
| WLD | 99.5 | 0.3 | 99.8 % |

The 2-D projection is essentially lossless for the World aggregate, USA, and India; reasonably tight for everyone else. Germany has the most genuinely multi-dimensional trajectory (still 90.5 %).

### Math displayed live in the PROJECTION info panel

```
PROJECTION  ·  Hˢ MANIFOLD
mode         RADAR STACK   ⟷   BARYCENTER TRAJECTORY   ⟷   BARYCENTER-ALIGNED   [+ SHOCK]
vertex j     (r·cos θ_j, r·sin θ_j) at depth z(t)
angle θ_j    (j/D)·2π − π/2                                         rad
radius r_j   R·(0.1 + 0.9·η_j),  R=140                              px
depth z(t)   (t − ⌊T/2⌋)·18                                         px
η_j          min-max scaled CLR_j(t)                                ∈[0,1]
CLR_i(t)     log ρ_i(t) − (1/D)Σ log ρ_j(t)
b(t)         PCA₂( Vᵀ·CLR(t) − μ ) · 0.85R                          ILR-Helmert  (BARY/ALIGN)
alignment    v_j(t) = (r_j·cos θ_j, r_j·sin θ_j) − b(t)              (ALIGN only)
shock tint   stroke→red as ‖Δclr(t)‖ / max → 1                      (SHOCK only)
perspective  s = FOV/(FOV+z+350), FOV=700
D, T         carriers 8–9, years 25–26
source       EMBER CSV → CNT v3.1.0  ·  bary_xy via v3.2.0
label        calendar year, rotated 90°, above plate
```

### Engine version policy (conference-stability lock)

- **Engine source (`HCI-CNT/engine/cnt.py`):** v3.2.0 — current; adds `navigation_2d` block.
- **Conference corpus (`per_country_json/cnt_v3/`):** v3.1.0 — locked, not regenerated.
- **Projector inline data:** v3.1.0 base CLR/norm + v3.2.0-equivalent `bary_xy` injected by sidecar `regen_baryxy.py`.
- **R port (cnt.R):** v3.1.0 — v3.2.0 port queued for post-conference parity work.
- **Manuscript citations:** continue to cite engine v3.1.0 for the corpus; v3.2.0 referenced only in this section and the projector info panel.

## Supporting Hˢ data outputs (the rest of the folder)

| File | Pages / slides | Size | Purpose |
|---|---|---|---|
| `CodaWork2026_FoundationsPlates_2026-05-14.pdf` | 19 pages | 0.8 MB | Stage-0 Foundations Plates — the seven linear-algebra foundations of Hˢ visualised per country |
| `per_country_json/cnt_v3/cnt_<ISO>.json` × 9 | — | ~300 KB each | Canonical CNT v3.1.0 engine output per country |
| `per_country_json/cnq_v2/cnq_<ISO>.json` × 9 | — | ~25 KB each | Canonical CNQ v2.0.0 engine output per country |
| `per_country_pdfs/<ISO>_stage0.pdf` × 9 | 2 pages each | ~86 KB each | Per-country Foundations Plates |
| `per_country_pdfs/<ISO>_stage1.pdf` × 9 | varies | — | Per-country Stage 1 Section plates |
| `per_country_pdfs/<ISO>_stage23.pdf` × 9 | varies | — | Per-country Stage 2/3 navigation plates (plate 16 of these is the navigation chart used as Fig 6 in the manuscript) |
| `per_country_pdfs/<ISO>_cnq.pdf` × 9 | 1 page each | — | Per-country CNQ dashboards |
| `dual_view/CodaWork2026_DualViewStage1Output_2026-05-13.pdf` | 503 pages | 4.1 MB | Master Dual-View PDF — Section + ILR-Helmert Triplet per country |
| `build_final_talk_10slide.py` | — | 17 KB | Source of the 10-slide compressed final talk deck (reproducible build) |

## Lineage

- The **10-slide compressed final talk** (`CodaWork2026_FinalTalk_10Slide_2026-05-20`) is the active conference deck. It was reached through three stages, archived for lineage at [`../archive/talk_decks_pre_10slide_2026-05-20/`](../archive/talk_decks_pre_10slide_2026-05-20/): the 22-slide narrative (2026-05-17) → 12-slide intermediate compression (2026-05-20 morning) → 10-slide final (2026-05-20 afternoon).
- Earlier May 2026 decks (`CodaWork2026_Talk_2026-05-12`, `..._2026-05-13`, and the external `HCI/CNT` legacy decks) are archived under [`../archive/talk_decks_legacy/`](../archive/talk_decks_legacy/) and [`../archive/legacy_decks_external/`](../archive/legacy_decks_external/).
- The story arc derives from the **manuscript** at `papers/codawork2026/manuscript/`. The talk is a condensation of the paper, not the other way around.
- The five-viewpoint protocol, the Activation Coefficient diagnostic, the three transition archetypes, and the navigation chart (Fig 6) are all consistent across:
  - the manuscript (`Compositional_Monitoring_2026.docx`)
  - the community study deck (`Studies/Energy_HiddenDirections_2026-05-17.pdf`)
  - the 10-slide final talk deck

## Conformance

- **HUF-STD-001 v1.1** — AI Use Declaration is on slide 10 of the talk (synthesis slide footer), and on the cover and back of the manuscript. The HUF AI Collective is named in both; the named author retains full scientific responsibility.
- **HUF-STD-002** — All engine outputs (CNT JSON, CNQ JSON, Foundations Plates, Stage 1/2/3, CNQ dashboards) ship as deterministic vector outputs (PDF / PNG / SVG) with hash-chained provenance to the raw EMBER CSVs.
- **HUF-STD-003** — The seven Linear Algebra Foundations (Symmetric Matrix · Property of Transpose · Matrix Decomposition · Eigenvectors/Eigenvalues · Spectral Theorem · Spectral Decomposition · Visualization) are visualised in `CodaWork2026_FoundationsPlates_2026-05-14.pdf`.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*The mathematics is not new; the monitoring application may be.*
