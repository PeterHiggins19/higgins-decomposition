# HCI-Atlas — The Compositional Plate Atlas

**Name:** HCI-Atlas (Higgins Computation Instruments — Atlas)
**Purpose:** Render any CNT JSON ever produced as a comparable, fully-logged
PDF atlas. The first analysis tool of the HCI tool family — read-only on
the JSON contract, write-only to a versioned catalog.
**Status:** PLAN. Implementation pending after CoDaWork 2026.
**Date:** 2026-05-05

---

## 1 — Position in the HCI family

| Tool | Role | Status |
|---|---|---|
| `cnt_v2` (cnt.py / cnt.R) | Composer — produces canonical CNT JSON from compositional CSV | DONE (2.0.3) |
| **HCI-Atlas** | Reader — renders any CNT JSON as PDF + HTML atlas with full provenance | **THIS PLAN** |
| Mission Command | Orchestrator — runs the engine across the corpus, manages experiments | PLANNED (`MISSION_CONTROL_PLAN.md`) |

HCI-Atlas reads the JSON the engine writes. It never recomputes; it only
displays. The JSON is the contract — every plate is one transformation
of one already-computed value, never a derived computation in the viewer.

---

## 2 — Plate taxonomy (the central distinction)

Two plate classes with **different counting rules**:

### 2a — Tour plates (user-limited)

The xy / xz / yz cross-section sweep across the trajectory. For T frames
and D carriers there are C(D,2) plate classes, with up to T frames per
class — total potentially `C(D,2) × T`. For BackBlaze (T=731, D=4) this
is `6 × 731 = 4 386` plates. For EMBER Japan (T=26, D=8) it is
`28 × 26 = 728`. Both are too many for paper; both should be sampled.

The **user controls a single budget**: `MAX_TOUR_PLATES`. The tool decides
what to skip and how, then **declares the decision visibly** on every
page. Three sampling regimes:

| Regime | Triggered when | Behaviour |
|---|---|---|
| FULL | `T × C(D,2) ≤ MAX_TOUR_PLATES` | Every frame × every plate class. No compression. |
| DECIMATED | `T × C(D,2) > MAX_TOUR_PLATES` and T > MAX_TOUR_PLATES | Pick representative frames at decimation ratio `1:N`. |
| WINDOWED | (Manual override) | User specifies frame range; plates restricted to that range. |

### 2b — Analytical plates (fixed count, never limited)

These have no `T` axis — they summarise the whole trajectory. Their count
is fixed and small; they are always rendered in full. Initial set:

| # | Plate | Source field in JSON |
|---|---|---|
| 1 | IR Classification Card  | `diagnostics.ir_classification` |
| 2 | M² = I residual heatmap | `bridges.coda_standard.M2_residual_matrix` |
| 3 | Bearing rose (all carriers) | `tensor.coda_standard.theta` |
| 4 | Lock timeline             | `diagnostics.lock_events` |
| 5 | Helmsman lineage tree     | `depth.coda_standard.helmsman_lineage` |
| 6 | Energy depth tower        | `depth.coda_standard.energy_levels` |
| 7 | Curvature depth tower     | `depth.coda_standard.curvature_levels` |
| 8 | EITT M-sweep curve        | `bridges.higgins_extensions.eitt_residuals` |
| 9 | Period-2 attractor scatter | `depth.higgins_extensions.attractor_points` |
| 10 | Banach contraction trace  | `depth.higgins_extensions.contraction_lambda` |
| 11 | Carrier triadic surface   | `stages.higgins_extensions.triadic` |
| 12 | Provenance card           | `metadata` (full block as table) |

Total fixed: **~12 analytical plates**. These are always rendered. They
are the heart of cross-dataset comparison — every atlas, regardless of
T or D, has the same analytical pages in the same order with the same
scales.

### 2c — Cardinal rule

The user budget MAX_TOUR_PLATES applies **only to xy/xz/yz tour plates**.
Analytical plates are not budgeted; they always render. This must be
clearly shown in the UI: "Tour budget: 5 of 731 used (1:146 decimation).
Analytical pages: 12 of 12 rendered (always full)."

---

## 3 — User awareness layer

The user's choice of MAX_TOUR_PLATES determines the trade-off between
compression and detail. The tool must make this trade-off **visible on
every page and at the start of every report**.

### 3a — The cover banner

Every PDF starts with a single-page cover declaring:

```
DATASET:        ember_jpn
SOURCE SHA-256: e7643dca648ecadc9...  (truncated)
ENGINE:         cnt 2.0.3 (Python)
SCHEMA:         2.0.0

T (records):    26
D (carriers):   8
PLATE BUDGET:   user-set MAX_TOUR_PLATES = 5
TOUR REGIME:    DECIMATED 1:5 (5 of 26 frames shown across 28 cross-sections = 140 plates)
ANALYTICAL:     12 of 12 (always full)

WARNING: Time compression applied. 21 of 26 frames omitted from tour plates.
         For full-precision tours, increase MAX_TOUR_PLATES to >= 728.
```

### 3b — Per-page footer

Every plate carries a footer:

```
[SOURCE: ember_jpn]   [FRAME 14 of 26 = 2014]   [PLATE Coal × Gas, xy]
[CONTENT_SHA: fded914144fd…]   [RUN: #042]   [PAGE 87/152]
```

### 3c — Compression visualisation

When DECIMATED, each tour plate also shows a small thumbnail strip on
the right edge — a row of T thin bars, with the rendered frames marked
in colour and the omitted frames greyed. The user sees at a glance which
frames are present and which are skipped.

### 3d — Smart defaults

If T × C(D,2) ≤ 50, default `MAX_TOUR_PLATES` to FULL automatically and
note "Auto-set to FULL: total tour count fits below threshold."

If T × C(D,2) > 50, default to DECIMATED with `MAX_TOUR_PLATES = 50` and
emit a warning: "Auto-set to DECIMATED. For full precision, set
`MAX_TOUR_PLATES = <total>`."

---

## 4 — Run counter and traceability database

The atlas catalog is a single JSON file: `HCI/atlas/atlas_catalog.json`.
Append-only; every run gets a row.

### 4a — Catalog schema

```json
{
  "_meta": {
    "type": "HCI_ATLAS_CATALOG",
    "schema": "1.0",
    "run_counter": 142,
    "last_updated": "2026-06-15T..."
  },
  "runs": [
    {
      "run_id": "042",
      "generated": "2026-05-05T18:00:00Z",
      "dataset_id": "ember_jpn",
      "input_csv_sha":  "e7643dca…",
      "input_json_sha": "fded914144fd…",   // CNT JSON content_sha256
      "engine_version": "cnt 2.0.3",
      "schema_version": "2.0.0",
      "atlas_version":  "1.0.0",
      "plate_budget":     5,
      "plate_count_tour": 5,
      "plate_count_analytical": 12,
      "tour_regime": "DECIMATED",
      "decimation_ratio": "1:5",
      "frames_total": 26,
      "frames_rendered": 5,
      "frames_omitted": 21,
      "atlas_pdf_path": "atlas/runs/042_ember_jpn.pdf",
      "atlas_pdf_sha":  "...",
      "atlas_html_path":"atlas/runs/042_ember_jpn.html",
      "atlas_html_sha": "...",
      "delta_from_run":  null,
      "user_notes":      ""
    },
    ...
  ]
}
```

### 4b — Tagging and hashing

Every artifact is hashed. The atlas PDF SHA-256 is recorded so the user
can prove a circulated copy is the same as the catalog entry. The input
JSON SHA-256 connects every atlas to its CNT JSON; the input CSV SHA-256
connects the CNT JSON to its source data. The chain is end-to-end.

### 4c — Run counter

`_meta.run_counter` is monotone. `run_id` is zero-padded to 3 digits
(`042`). Run files use this in their names so directory listings sort
chronologically.

---

## 5 — HTML catalog and command-JSON integration

### 5a — Catalog HTML

`HCI/atlas/atlas_catalog.html` — a single static page that reads
`atlas_catalog.json` and renders a sortable / filterable table. Columns:
run_id, dataset_id, generated, engine_version, plate_budget, tour_regime,
PDF link, HTML link, source SHA, atlas SHA. No server required; pure JS
that loads the JSON.

### 5b — Per-run HTML

Each run also gets a lightweight HTML page mirroring the PDF — same
plates as inline SVG/PNG, same banner, same footers. The HTML is
clickable: hover a frame on the compression strip and the plate updates;
click a carrier name and the bearing rose highlights it. The PDF is the
shareable archival format; the HTML is the live navigation surface.

### 5c — Command-JSON integration

Mission Command (planned) emits one JSON describing the experiment run.
HCI-Atlas reads that and the per-experiment CNT JSON; emits one row in
`atlas_catalog.json`. The two catalog systems share `dataset_id` as the
key. Mission Command tracks "what was computed when"; Atlas tracks "what
was rendered when". Together they give a complete provenance graph.

---

## 6 — Multi-run management and delta comparison

### 6a — Listing prior runs

`atlas list ember_jpn` → shows every atlas run for ember_jpn with
content_sha and date. User can spot regressions ("the SHA changed across
two runs of the same input — was the engine config different?").

### 6b — Delta tool

`atlas delta 040 042` →

* Side-by-side cover banners highlighting changed fields
* IR card delta: was `CRITICALLY_DAMPED A=0.0376`, now `LIGHTLY_DAMPED A=0.279` (highlighted)
* Helmsman lineage diff: nodes added/removed/changed
* M² residual heatmap delta: cells with > 1% change highlighted
* Tour plate strip with delta-coloured frames
* List of unchanged sections at the end (so user knows nothing was hidden)

### 6c — Cross-dataset comparison

`atlas compare ember_jpn ember_fra ember_deu` → produces a comparison
atlas where the analytical plates from each dataset are interleaved on
common axes. This is the visual proof that "any data ever input can be
directly compared with any other" — the entire point.

---

## 7 — Display metrics and scaling

To make plates from different datasets visually comparable, all axes use
common scales pulled from the JSON's stat blocks.

| Quantity | Common scale |
|---|---|
| Bearing θ | 0–360° (always) |
| Amplitude A | 0–1 (always — Higgins scale) |
| ζ (damping) | 0–2 (always) |
| Curvature κ (per-carrier) | log-scaled; range from `tensor.coda_standard.summary_stats.kappa_quantiles` |
| CLR magnitude | clipped to [-15, 5] (with markers for excursions) |
| EITT residual % | 0–100% (gate line at user-config EITT_GATE_PCT) |
| Recursion level | 0–DEPTH_MAX_LEVELS |

The atlas reads the user-config block from `metadata.engine_config` in
the JSON and stamps the gate line accordingly. If the user changed
`EITT_GATE_PCT` from 5% to 1%, the EITT plate shows the gate at 1%.

### 7a — Automated formatting

* Auto-pick portrait or landscape per plate based on aspect ratio
* Auto-fit titles by truncating dataset_id at first non-alphanumeric if too long
* Auto-colour-code carriers consistently across all plates (deterministic mapping from carrier name → palette index)
* Auto-suppress legend on plates where the carrier name is in the title

### 7b — Advanced analysis hooks

The tool reads `diagnostics.advanced_metrics` (when present) and adds:

* IR classification card colour-coded by class family (CRIT/LIGHT/MOD/OVER/EXTREME)
* Period detector confidence band overlaid on attractor scatter
* Lock event severity ranking on the lock timeline
* Banach contraction confidence interval on the λ trace

---

## 8 — Output formats

### 8a — Primary: PDF

* ReportLab + matplotlib backend
* PDF/A-2 compliant for archival
* Full bookmarks: Cover / Tour Stage 1 / Tour Stage 2 / Tour Stage 3 / Analytical / Provenance / Appendix
* Searchable text layer (every label embedded)
* No raster-only pages — every plate is vector

### 8b — Secondary: HTML mirror

* Same plates as inline SVG
* Plate budget summary at top
* Compression strip is interactive (clickable frame selection)
* No external dependencies (pure HTML/JS, embedded data)

### 8c — Tertiary: per-plate exports

`--export-plates` flag dumps each plate as a standalone SVG/PNG in
`atlas/runs/042/plates/` — useful for slide decks and the CoDaWork paper.

---

## 9 — File layout

```
HCI/atlas/
├── atlas.py                  # main entry point
├── atlas_catalog.json        # append-only run database
├── atlas_catalog.html        # sortable index page
├── ATLAS_PLAN.md             # (this file)
├── README.md                 # usage
├── plate_renderers/
│   ├── ir_card.py
│   ├── m2_heatmap.py
│   ├── bearing_rose.py
│   ├── lock_timeline.py
│   ├── helmsman_tree.py
│   ├── tour_xy.py
│   ├── tour_xz.py
│   ├── tour_yz.py
│   └── ...
└── runs/
    ├── 001_first_run.pdf
    ├── 001_first_run.html
    ├── 001_first_run.meta.json
    ├── 042_ember_jpn.pdf
    ├── 042_ember_jpn.html
    ├── 042_ember_jpn.meta.json
    └── ...
```

`runs/<run_id>_<dataset_id>.meta.json` — per-run metadata mirroring
the catalog row, kept alongside the artifact for offline portability.

---

## 10 — User configuration block

The atlas tool follows the same pattern as `cnt.py`: a USER CONFIGURATION
block at the top of `atlas.py`, every constant documented inline, every
active value echoed in `atlas_catalog.json` per row.

```python
# ============================================================
# ATLAS USER CONFIGURATION
# ============================================================
ATLAS_VERSION         = "1.0.0"

# Plate budget
MAX_TOUR_PLATES       = 50          # User-controlled. None = render every plate.
AUTO_FULL_THRESHOLD   = 50          # If T × C(D,2) ≤ this, default to FULL regardless.
TOUR_REGIME_DEFAULT   = "AUTO"      # "AUTO" | "FULL" | "DECIMATED" | "WINDOWED"

# Display
COMMON_BEARING_SCALE  = (0, 360)
COMMON_AMPLITUDE_RANGE = (0, 1)
CARRIER_PALETTE_SEED  = 42          # Deterministic colour assignment

# Output
PDF_BACKEND           = "reportlab"
EMBED_HTML_DATA       = True        # Self-contained HTML
EXPORT_PLATES         = False       # Per-plate SVG/PNG dump
PDF_PROFILE           = "PDF/A-2"

# Catalog
CATALOG_PATH          = "HCI/atlas/atlas_catalog.json"
RUN_ID_WIDTH          = 3           # Zero-padded width for run_id

# Compression banners
SHOW_COMPRESSION_STRIP = True
WARN_BELOW_PLATES_PCT  = 5.0        # Warn if rendered/total < this percentage
# ============================================================
```

Two atlas runs with the same input + same config produce byte-identical
PDFs (modulo embedded timestamp, which the catalog records separately).

---

## 11 — Implementation phases

| Phase | Scope | Effort | Deliverable |
|---|---|---|---|
| A | Reader + 6 analytical plates + cover banner | 2-3 d | Single-dataset atlas PDF |
| B | Tour plates with budget + compression strip + warnings | 2 d | Full single-dataset atlas |
| C | Catalog DB + run counter + per-run HTML | 1-2 d | Multi-run management |
| D | Catalog HTML index + filtering | 1 d | Browseable catalog |
| E | Delta tool | 2 d | Run-to-run comparison |
| F | Cross-dataset comparison atlas | 2 d | The grand atlas page |
| G | Per-plate export + advanced analysis hooks | 1 d | Slide-ready outputs |

Total: **~10-13 working days** for full feature set. Phase A+B is the
minimum viable atlas — sufficient for the CoDaWork 2026 paper figures.

---

## 12 — Failure modes and warnings

| Condition | Response |
|---|---|
| T = 1 | "Single-record dataset. Tour plates skipped. Analytical plates only." |
| D = 2 | "Compositional dimension D=2. xz/yz plates degenerate; only xy rendered." `D2_DEGENERATE` IR class shown. |
| T very large + low budget | Warning at top of cover: "Significant compression: 99.3% of frames omitted." |
| Engine version mismatch | "JSON produced by cnt 2.0.0; atlas expects ≥ 2.0.3. IR taxonomy may differ." |
| Schema version mismatch | Hard error: "Schema 1.0.0 not supported. Re-run engine." |
| Missing analytical plate field | Render placeholder with field name and "NOT EMITTED BY THIS ENGINE VERSION." |

---

## 13 — Cross-comparability — the unifying principle

The defining promise of HCI-Atlas: any CNT JSON ever produced, by any
version of the engine, on any compositional dataset, can be opened in
HCI-Atlas and **compared on common axes** to any other.

This requires three guarantees:

1. **The schema is the contract.** The atlas reads only schema 2.x
   fields; engine version tells the atlas what optional fields to expect.
2. **The plate scales are universal.** Bearing 0-360, amplitude 0-1,
   damping 0-2, EITT 0-100 — fixed across every plate of every atlas.
3. **The provenance is end-to-end.** CSV SHA → JSON SHA → atlas SHA →
   catalog row. The graph is acyclic and complete.

When the user opens atlas run #042 (ember_jpn) and atlas run #017
(geochem_ball_age), the analytical plates can be **stacked side by
side** with the same axes. The IR card from #042 (CRITICALLY_DAMPED,
A=0.0376) sits next to #017 (CRITICALLY_DAMPED, A=0.0361) on the same
amplitude bar — the visual proof that the cross-domain finding is a
quantitative match, not a qualitative analogy.

---

## 14 — Relationship to existing work

* **Replaces:** Earlier ad-hoc per-experiment plate code in
  `experiments/Hs-XX_*/figures/` directories.
* **Reads:** CNT JSON v2.0.x (schema 2.0.0, engine 2.0.3+).
* **Coordinates with:** Mission Command (per `MISSION_CONTROL_PLAN.md`)
  via shared `dataset_id` and `content_sha256` keys.
* **Supersedes:** Stage 1 plate generator (`stage1_plates`) referenced
  in earlier design notes — that becomes a renderer plug-in inside
  HCI-Atlas/plate_renderers/tour_xy.py etc.

---

## 15 — Open questions to resolve before implementation

1. **PDF backend.** ReportLab (heavy, vector-perfect) vs matplotlib's
   `PdfPages` (lighter, pythonic). Recommend ReportLab for plate layout
   + matplotlib for plate body.
2. **Catalog locking.** Multi-process atlas runs writing to the same
   `atlas_catalog.json` need a lock. Use a sidecar `.lock` file with
   PID + timestamp.
3. **Run garbage collection.** Old runs stay forever by default. Add an
   `atlas archive --before <date>` command? Defer to post-launch.
4. **HTML interactivity scope.** Pure static (current plan) vs. minimal
   JS-driven filtering? Pure static is more portable and reproducible;
   prefer that for v1.0.

---

*The instrument reads. The expert decides. The loop stays open.*
*The atlas remembers what the instrument saw.*
