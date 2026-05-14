# data_outputs — Premier CNT v3.1.0 + CNQ v2.0.0 Data Output

**Document version:** 2.0
**Document status:** authoritative — the premier scientific data output for the CoDaWork 2026 talk
**Created:** 2026-05-13
**Updated:** 2026-05-14 — master PDF regenerated after CNQ-dashboard fix (325 pages); PPTX rebuilt with corrected CNQ + NEW per-country Triplet Plate slide (66 slides, 6 plates per country)
**Author:** Peter Higgins, Rogue Wave Audio
**Conforms to:** HUF Publication Standards (HUF-STD-001) — `../../../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json`; HUF Tensor Train I/O Standard (HUF-STD-002) — `../../../huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json`

---

## Status

These are the **actual data outputs of the CNT v3.1.0 and CNQ v2.0.0 engines** applied to the full 9-country EMBER electricity-generation corpus (2000–2025). Not slides about data — the data, run, plotted, hash-chained, packaged. This is what the CoDa community is being shown.

Built from scratch on 2026-05-13 using the unchanged engines. Engine code untouched; this is engine output. Lockdown-compatible (the lockdown forbids changing engine code; it does not forbid running it to produce documented output).

---

## Files

### Master deliverables (start here)

| File | Pages / Slides | Size | Purpose |
|---|---|---|---|
| [`CodaWork2026_PremierDataOutput_2026-05-13.pdf`](CodaWork2026_PremierDataOutput_2026-05-13.pdf) | **325 pages** | 3.8 MB | Master PDF: master cover + TOC + 9 country sections (cover + Stage 1 27-plate cine-deck + Stage 2/3 7-page navigation + CNQ 1-page quaternion-view dashboard). **Full per-year detail for every country.** Regenerated 2026-05-14 after CNQ dashboard correction. |
| [`CodaWork2026_PremierDataOutput_2026-05-13.pptx`](CodaWork2026_PremierDataOutput_2026-05-13.pptx) | **66 slides** | 6.3 MB | Compact PPTX with master cover, TOC, and per-country **6-slide** summary (cover + representative Stage 1 Section plate + course plot + helmsman + **NEW: ILR-Helmert Triplet Plate** + corrected CNQ dashboard) + AI Use Declaration. Rebuilt 2026-05-14 to propagate CNQ fix and add the Triplet companion view per the dual-view doctrine. For conference-room projection. |

### Per-country canonical JSON (hash-chained engine output)

[`per_country_json/cnt_v3/`](per_country_json/cnt_v3/) — 9 files, one per country, ~290–350 KB each:

- `cnt_AUS.json`, `cnt_CHN.json`, `cnt_DEU.json`, `cnt_FRA.json`, `cnt_GBR.json`, `cnt_IND.json`, `cnt_JPN.json`, `cnt_USA.json`, `cnt_WLD.json`

Each file contains the complete CNT v3.1.0 output: metadata, input ledger (source SHA-256), tensor frames (one per year with bearing tensor, angular velocity, Higgins scale, helmsman index, κ^HS metric), stages 1/2/3, depth tower, helmsman family, attractor fit, diagnostics. Schema 3.1.0.

[`per_country_json/cnq_v2/`](per_country_json/cnq_v2/) — 9 files, ~17–35 KB each:

- `cnq_AUS.json` through `cnq_WLD.json`

Each contains CNQ v2.0.0 output: metadata, input, CNT reference link, cnq_view (bearing trajectories at D=2 / D=3 / D=4 twin-factor, CHSH joint-coherence diagnostic, twin-quaternion factoring residuals), helmsman family, attractor fit. Schema cnq/2.0.0.

### Stage-0 Foundations Plates (NEW 2026-05-14 — the bedrock made visible)

[`CodaWork2026_FoundationsPlates_2026-05-14.pdf`](CodaWork2026_FoundationsPlates_2026-05-14.pdf) — **19 pages**, ~810 KB — Master Foundations PDF: cover + 9 country sections × 2 pages each (six-panel foundations grid + numeric verification table).

Visualizes the **seven linear-algebra foundations of Hs** per HUF-STD-003:

1. **§1 Symmetric matrix** — variation matrix heatmap (D × D), with `max|M − Mᵀ|` verification
2. **§2 Property of transpose** — Helmert basis H + orthonormality `max|HHᵀ − I|` at IEEE-floor
3. **§3 Matrix decomposition** — raw → CLR → ILR chain
4. **§4 Eigenvectors / eigenvalues** — eigenvalue scree + cumulative variance
5. **§5 Spectral Theorem** — numeric residual `max|Σ − QΛQᵀ|` at IEEE-floor proving the theorem holds on actual data
6. **§6 Spectral decomposition** — orthonormal eigenbasis Q heatmap + rank-k variance breakdown
7. **§7 Visualization** — the plate IS this component

Per-country PDFs at [`per_country_pdfs/`](per_country_pdfs/) — `{ISO}_stage0.pdf` × 9 (~86 KB each, 2 pages each).

Headline: **Germany's** electricity-mix evolution lives essentially in a 2-D plane within the 8-D ILR space (Rank-1 = 60.5%, Rank-2 = 90.4%, Rank-3 = 99.9%) — consistent with the dominant Coal-to-Renewable axis plus a Nuclear-shaped secondary axis.

Generator: `HCI/codawork2026/stage0_foundations/foundations_plate.py` (NEW 2026-05-14).
Doctrine: HUF-STD-003 — `../../../huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json`.

### Dual-View Stage 1 Output (NEW 2026-05-13 — the paired reading)

[`dual_view/`](dual_view/) — paired Section Plate + ILR Triplet Plate per country.

| File | Pages | Size | Purpose |
|---|---|---|---|
| [`dual_view/CodaWork2026_DualViewStage1Output_2026-05-13.pdf`](dual_view/CodaWork2026_DualViewStage1Output_2026-05-13.pdf) | 503 | 4.1 MB | **Master Dual-View PDF** — cover + 9 country sections × (View A Section Plate + View B ILR-Helmert Triplet Plate) |
| `dual_view/{ISO}_dual_view.pdf` × 9 | ~56 ea | ~450 KB ea | Per-country dual-view PDFs |
| [`dual_view/README.md`](dual_view/README.md) | — | — | Folder explanation + reading guide |

**View A — Section Plate** (CoDa-Standard): bars for pairwise bearings + bars for CLR per carrier + XY scatter plan view. Answers "what are the magnitudes at this timestep?"

**View B — ILR Triplet Plate** (Orthonormal, NEW): three orthogonal scatter panels (ilr_1×ilr_2, ilr_1×ilr_3, ilr_2×ilr_3) with full trajectory drawn ○→◾. Answers "where is the composition in ILR space and where has it moved?"

Both views are Order-1 first-principles per Output Doctrine v1.0. The new generator is `HCI/codawork2026/stage1_plates/ilr_triplet_plate.py` (2026-05-13).

### Per-country plate PDFs (individual access)

[`per_country_pdfs/`](per_country_pdfs/) — 27 files (3 per country):

- `{ISO}_stage1.pdf` (~210 KB, ~27 pages) — full Stage 1 cine-deck: one plate per year showing XY scatter (plan view of pairwise bearings) + XZ bar chart (all D(D-1)/2 pairwise bearings in degrees) + YZ bar chart (CLR coordinates per carrier) + info panel + legend. Plus a course plot summarizing the full trajectory.
- `{ISO}_stage23.pdf` (~100 KB, 7 pages) — group barycenter distance matrix, helmsman frequency chart, pairwise divergence ranking, triadic area ranking, carrier interaction matrix, navigation summary table.
- `{ISO}_cnq.pdf` (~45 KB, 2 pages) — CNQ v2.0.0 quaternion-view dashboard: Hs(t), ω(t), bearing tensor magnitude, helmsman channel σ(t), κ^HS metric energy, CHSH + twin-quaternion + attractor diagnostics. Plus bearing trajectories at D=2 / D=3 / D=4 twin-factor.

---

## Layout per country (Higgins Tensor Data Field Layout v1.0)

Each Stage 1 plate follows the published Higgins display standard:

```
┌──────────┬──────────┬──────────────────┐
│  Info    │  Legend  │  Bar: XZ         │
│  (text)  │  (pairs) │  (bearings deg)  │
├──────────┴──────────┼──────────────────┤
│  Scatter: XY        │  Bar: YZ         │
│  (plan view)        │  (CLR per carr.) │
└─────────────────────┴──────────────────┘
```

- **XY scatter (plan view):** plots (h_i, h_j) for each carrier pair. The angle from origin to each point IS the bearing θ_ij.
- **XZ bar:** all D(D-1)/2 pairwise bearings in degrees, range [-180, +180].
- **YZ bar:** CLR coordinate per carrier (position in Higgins space).
- **Fixed scales** across all time frames (oscilloscope-style graticule).
- **Monochrome line graphics.** No interpretation embedded — raw data plates.

---

## Headline metrics across the corpus

| Country | N records | D carriers | Bearing pairs | Helmsman flips | IR class | CHSH S |
|---|---|---|---|---|---|---|
| AUS  Australia      | 26 | 9 | 36 | (see CNQ) | (see CNQ) | (see CNQ) |
| CHN  China          | 26 | 8 | 28 | (see CNQ) | (see CNQ) | (see CNQ) |
| DEU  Germany        | 26 | 9 | 36 | (see CNQ) | (see CNQ) | (see CNQ) |
| FRA  France         | 26 | 9 | 36 | (see CNQ) | (see CNQ) | (see CNQ) |
| GBR  United Kingdom | 26 | 9 | 36 | (see CNQ) | (see CNQ) | (see CNQ) |
| IND  India          | 26 | 8 | 28 | (see CNQ) | (see CNQ) | (see CNQ) |
| JPN  Japan          | 26 | 8 | 28 | (see CNQ) | (see CNQ) | (see CNQ) |
| USA  United States  | 25 | 9 | 36 | (see CNQ) | (see CNQ) | (see CNQ) |
| WLD  World          | 26 | 9 | 36 | (see CNQ) | (see CNQ) | (see CNQ) |

Per-country country cover pages in the master PDF have full metric tables including hash-chained content_sha256 of both CNT and CNQ outputs.

---

## Reproducing this output

Anyone with the Hs repository and Python 3.10+ can reproduce this output from raw EMBER CSV in ~5 minutes:

```bash
# From repo root
cd HCI/codawork2026/stage1_plates
for csv in ../../../data/Energy/EMBER_pipeline_ready/ember_*.csv; do
    ISO=$(basename "$csv" | sed 's/ember_\([A-Z]*\)_.*/\1/')
    python3 stage1_engine.py     "$csv"    "stage1_${ISO}.json"
    python3 stage1_plates_raw.py "stage1_${ISO}.json" "stage1_${ISO}.pdf"
    python3 stage23_plates.py    "stage1_${ISO}.json" "stage23_${ISO}.pdf"
done

# CNT v3.1.0 + CNQ v2.0.0 canonical hash-chained JSON
python3 -c "
import sys; sys.path.insert(0,'../../../HCI-CNT/engine'); sys.path.insert(0,'../../../HCI-CNQ/engine')
import cnt, cnq
for code in ['AUS','CHN','DEU','FRA','GBR','IND','JPN','USA','WLD']:
    cnt.cnt_run(f'../../../data/Energy/EMBER_pipeline_ready/ember_{code}_*.csv', out_path=f'cnt_{code}.json')
    cnq.cnq_run(input_csv=..., cnt_json_path=f'cnt_{code}.json', out_path=f'cnq_{code}.json')
"
```

Compare your `cnt_DEU.json` `content_sha256` against the one in the master PDF Germany cover page. If they match, the engine produced bit-identical results.

---

## What is in the master PDF (325 pages, regenerated 2026-05-14)

CNQ dashboard correction reduced each country's CNQ section from 2 pages to 1 (consolidated single-page dashboard with Hs(t), ω(t), K_eff+TV(t), helmsman σ(t), step-Δ Aitchison spike detector, and CNQ diagnostics box).

| Pages | Section |
|---|---|
| 1–2 | Master cover + Table of Contents |
| 3–38 | § AUS Australia — cover + 27 Stage 1 plates + 7 Stage 2/3 pages + 1 CNQ dashboard |
| 39–74 | § CHN China (CHSH S = 0.88 headline at D = 8 twin-factor) |
| 75–110 | § DEU Germany (headline case — Hs 0.43 → 0.13, ω 2024 spike, K_eff arc 3.5 → 6.7) |
| 111–146 | § FRA France |
| 147–182 | § GBR United Kingdom |
| 183–218 | § IND India |
| 219–254 | § JPN Japan (Fukushima 2011 ω spike visible) |
| 255–289 | § USA United States (25 years, 35 pages) |
| 290–325 | § WLD World aggregate |

## What is in the rebuilt PPTX (66 slides, rebuilt 2026-05-14)

| Slides | Content |
|---|---|
| 1 | Title — CoDaWork 2026 / Premier Data Output |
| 2 | TOC — 6 plates per country listed |
| 3–9 | § AUS Australia — divider + cover + Stage 1 mid + course + helmsman + **Triplet** + CNQ |
| 10–16 | § CHN China |
| 17–23 | § DEU Germany |
| 24–30 | § FRA France |
| 31–37 | § GBR United Kingdom |
| 38–44 | § IND India |
| 45–51 | § JPN Japan |
| 52–58 | § USA United States |
| 59–65 | § WLD World |
| 66 | AI Use Declaration |

Each country's 7 slides = 1 section divider + 6 content plates. The NEW Triplet Plate slide is the orthonormal companion to the Section Plate per the Dual-View Stage 1 doctrine (HUF-STD-002 link 4).

---

## AI Use Declaration

In accordance with established scientific community standards (ICMJE, COPE, Nature/Springer, Science/AAAS, WAME, EU AI Act 2024, arXiv, ACM, IEEE) this work discloses AI assistance.

**AI tools used:** Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI) — the HUF AI Collective.

**Tasks performed by AI:** plate-generator scripting orchestration; master cover + per-country cover page design; consistency editing; master-PDF assembly; PPTX layout. All data was produced by the deterministic engines (CNT v3.1.0 + CNQ v2.0.0), not by AI.

**Author responsibility:** The author (P. Higgins, Rogue Wave Audio) retains full responsibility for all data interpretation, methodological choices, and conclusions. All output has been produced by deterministic, hash-chained engines. AI tools are NOT listed as authors.

**AI use governance:** HUF AI Collective cross-check protocol per HUF Governance Charter Articles II–IV and SAFE-001.

**Dates of use:** March 2026 – May 2026 (conference-preparation arc).

**Standards reference:** HUF-STD-001.

---

## File status

- **Created:** 2026-05-13 at Peter directive to update conference data outputs with current CNT/CNQ engine.
- **Updated 2026-05-14:** CNQ dashboard generator fixed (blank panels diagnosed → real data); master PDF regenerated (334 → 325 pp); Dual-View Stage 1 Output added (503-page paired Section + Triplet master); PPTX rebuilt with 6 plates per country and corrected CNQ artwork (57 → 66 slides).
- **Severity:** S2 (linked doc addition) + engine-RUN (not engine-CHANGE).
- **Lockdown compatibility:** fully compliant — engine code untouched, schemas untouched, INV catalog dispositions untouched, NO-CREATE files untouched, `papers/codawork2026/talk/` untouched.
- **Supersedes:** the older Japan-only `HCI_Japan_CoDaWork2026.pdf`, `stage1_plates_fixed.pdf`, `stage23_plates.pdf`, `navigation.pdf` (preserved in source folders as historical references).

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
*Not slides about data. The data, run, plotted, hash-chained, packaged.*
