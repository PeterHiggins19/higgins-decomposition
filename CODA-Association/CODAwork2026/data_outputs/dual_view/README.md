# Dual-View Stage 1 Output

**Created:** 2026-05-13
**Author:** Peter Higgins, Rogue Wave Audio
**Conforms to:** HUF-STD-001 (publication standards) + HUF-STD-002 (tensor-train I/O)

---

## What this folder is

A **paired Stage-1 reading** per country, presenting two complementary views of the same compositional time series:

- **View A — Section Plate** (CoDa-Standard reading): bars for pairwise bearings, bars for CLR per carrier, scatter for the plan view. Answers *"what are the magnitudes at this timestep?"* Generator: `HCI/codawork2026/stage1_plates/stage1_plates_raw.py`.

- **View B — ILR-Helmert Orthogonal Triplet Plate** (Orthonormal reading): three orthogonal scatter panels showing the first three Helmert ILR axes pairwise. Answers *"where is the composition in ILR space and where has it moved over time?"* Generator: `HCI/codawork2026/stage1_plates/ilr_triplet_plate.py` (NEW 2026-05-13).

Both views are Order-1 first-principles plates per Output Doctrine v1.0. Both read from the same `stage1_output.json`. Together they form a complete Stage-1 reading: the Section Plate gives the timestep-by-timestep magnitude index; the Triplet Plate gives the trajectory shape across the full time window.

---

## Files

| File | Pages | Size | Purpose |
|---|---|---|---|
| `CodaWork2026_DualViewStage1Output_2026-05-13.pdf` | 503 | 4.1 MB | **Master PDF** — cover + TOC + 9 country sections × (View A divider + 27 Section plates + View B divider + 27 Triplet plates) |
| `{ISO}_dual_view.pdf` × 9 | ~56 each | ~450 KB each | Per-country dual-view PDFs for individual access |

---

## Reading guide per country

Each per-country dual-view PDF is structured:

```
  page 1     "View A — Section Plate" divider
  page 2     country cover info
  pages 3-28 Section Plate cine-deck — one plate per year + course plot
  page 29    "View B — ILR-Helmert Orthogonal Triplet Plate" divider
  page 30    Triplet summary page (full trajectory with start ○ → end ◾)
  pages 31-56  Triplet cine pages — one per year with current year highlighted (red ×)
```

USA is 54 pages (25 years of data instead of 26 — the EMBER USA series starts 2001 not 2000).

---

## Why two views

The two views answer different questions and the bar+XY view alone hides information that the orthonormal triplet reveals:

- The **Section Plate** is good for indexed magnitude readings — "what is the bearing of pair Coal-Gas in 2012?" — and for displaying the bar-chart aesthetic that the CoDa community uses for variation matrices and per-carrier CLR readings.

- The **Triplet Plate** is good for trajectory inspection — "did the composition move continuously or with a regime change?" — and for revealing the shape of the time series in the proper compositional geometry (Aitchison-isometric ILR space). Germany's continuous arc toward the renewable vertex is visible in the Triplet that the Section misses. Japan's diagonal post-Fukushima shift is visible in the Triplet that the Section presents only as one year's magnitudes.

The pair answers both questions on one page-flip. Neither view alone is complete.

---

## Generators (HUF Tensor Train v1.0, link 4)

Both generators are now in `HCI/codawork2026/stage1_plates/`:

| Generator | Reads | Produces |
|---|---|---|
| `stage1_plates_raw.py` (existing) | `stage1_output.json` | Multi-page PDF — Section Plate cine-deck |
| `ilr_triplet_plate.py` (NEW 2026-05-13) | `stage1_output.json` | Multi-page PDF — ILR Triplet plate summary + cine |

Both are now standard outputs under HUF-STD-002 (the Tensor Train I/O Standard). PNG and SVG export are planned for the first post-conference push (per HUF-STD-002 §post_conference_implementation_targets, ordered target #2).

---

## Reproducibility recipe

```bash
# from repo root
cd HCI/codawork2026/stage1_plates

# Generate stage1 JSON + both plate views for one country (DEU example)
python3 stage1_engine.py     ../../../data/Energy/EMBER_pipeline_ready/ember_DEU_Germany_generation_TWh.csv  stage1_DEU.json
python3 stage1_plates_raw.py stage1_DEU.json  DEU_section.pdf
python3 ilr_triplet_plate.py stage1_DEU.json  DEU_triplet.pdf
```

The two PDFs together = one country's Dual-View Stage 1 Output.

---

## AI Use Declaration

Per HUF Publication Standards (HUF-STD-001).

**AI tools used:** Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI) — the HUF AI Collective.

**Tasks performed by AI:** drafting the `ilr_triplet_plate.py` generator + master cover and view dividers; consistency editing across the dual-view package. The data was produced by the unchanged CNT v3.1.0 engine + Helmert basis computation (standard linear algebra).

**Author responsibility:** The author retains full responsibility for the methodology and the published artifact. All plates have been reviewed; the Helmert basis math is the textbook orthonormal construction. AI tools are not authors.

**AI use governance:** HUF AI Collective cross-check protocol per HUF Governance Charter Articles II–IV and SAFE-001.

**Dates of use:** March 2026 – May 2026.

**Standards reference:** HUF-STD-001 + HUF-STD-002.

---

*Both views are first-principles. The Section Plate reads magnitudes. The Triplet Plate reads trajectories. Together they are the complete Stage 1.*
*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
