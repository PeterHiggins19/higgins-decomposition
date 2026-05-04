# HCI Stage 1 Plates — Section Cine-Deck

Automated engine chain: **EMBER CSV** --> **Stage 1 CBS/CNT** --> **JSON** --> **PDF / PPTX**

Format: **1 section plate per year** — each plate shows 3 orthogonal face projections + metric ledger + pair index.

**Standard method**: `stage1_plates_raw.py` using **Higgins tensor data field layout v1.0**. Fixed-scale display. Field-deployable. No AI dependency.

## Reproducibility

The tensor engine is fixed. Scientists can reproduce all results:

```bash
# Step 1: Run the engine (CSV → JSON + ASCII section plates to stdout)
python stage1_engine.py path/to/ember_data.csv stage1_output.json

# Step 2a: Generate raw section plates as PDF (STANDARD METHOD — field use)
python stage1_plates_raw.py stage1_output.json stage1_plates_raw.pdf

# Step 2b: Generate Section Cine-Deck as PPTX (presentation use, requires pptxgenjs)
NODE_PATH=/usr/local/lib/node_modules_global/lib/node_modules node build_plates_pptx.js stage1_output.json HCI_Stage1_Plates.pptx
```

## Files

| File | Purpose |
|------|---------|
| `stage1_engine.py` | Python engine: reads EMBER CSV, computes all CBS/CNT Stage 1 data, outputs JSON + ASCII section plates |
| `stage1_plates_raw.py` | **STANDARD** — matplotlib plate generator: layout v1.0, fixed-scale PDF/PNG output, field-deployable |
| `tensor data field layout v1.0.vsdx` | Visio specification — canonical plate layout (Info + Legend + 3 faces) |
| `build_plates_pptx.js` | PPTX generator: reads JSON, produces 29-slide section cine-deck (1 plate per year) |
| `stage1_output.json` | Complete Stage 1 output — all years, all carriers, all tensor channels |
| `stage1_plates_fixed.pdf` | Generated PDF — 26 plates, fixed scales, legend in info panel, rapid-scroll comparable |
| `HCI_Stage1_Plates.pptx` | Generated PowerPoint — section cine-deck |
| `EMBER_Analysis_Evolution.docx` | Historical comparison — 10 eras of EMBER Japan analysis with validity assessment |

## Section Plate Structure — Layout v1.0

Higgins tensor data field layout v1.0 — maximum information density, no wasted area.

```
┌──────────┬──────────┬──────────────────┐
│  Info    │  Legend  │  XZ Bearings bar │
│  (metrics)│ (pairs) │  (all D(D-1)/2)  │
├──────────┴──────────┼──────────────────┤
│  XY Scatter         │  YZ CLR bar      │
│  (plan view)        │  (per carrier)   │
└─────────────────────┴──────────────────┘
```

| Panel | Position | Content |
|-------|----------|---------|
| **Info** | Top-left | Hs, ring, E_metric, kappa, omega, d_A, helmsman, scale ranges |
| **Legend** | Top-centre | All D(D-1)/2 pair indices with carrier names |
| **XZ Face** | Top-right | Bar graph of all pairwise bearings in degrees |
| **XY Face** | Bottom-left (wide) | CLR scatter plan view — angle from origin = bearing |
| **YZ Face** | Bottom-right | Bar graph of CLR coordinate per carrier |

## PPTX Contents (29 slides)

1. Title slide — dataset, carriers, engine identification
2-27. Section plates — 1 per year (2000-2025), each with YZ + XZ + XY faces + metric ledger
28. Informational Lock Detection — locked carrier pairs with bearing trajectory
29. Closing slide

## JSON Schema

The `stage1_output.json` contains:

- `instrument`, `engine`, `stage`: identification
- `carriers`: D carrier names
- `years`: T year values
- `records[]`: one per year, each containing:
  - `composition`, `clr`: closed composition and CLR coordinates
  - `hs`, `ring`: Higgins Scale value and ring classification
  - `bearings_deg`: all D(D-1)/2 pairwise bearings in degrees
  - `angular_velocity_deg`: omega between consecutive years
  - `helmsman`, `helmsman_delta`: DCDI (dominant carrier displacement index)
  - `steering_sensitivity`: diagonal 1/x_j for each carrier
  - `metric_diagonal`: G_jj from the Aitchison metric tensor
  - `metric_energy`, `condition_number`: displacement and conditioning
  - `d_aitchison`: Aitchison distance from previous year
- `locks[]`: informationally locked carrier pairs (bearing spread < 10 deg)

## CBS Display Range Theory — Fixed-Scale Instrument

The CBS operates like a physical oscilloscope: scales are fixed across all time frames so rapid scrolling reveals genuine compositional movement against a constant backdrop.

### Mathematically Exact Bounds (no dataset can exceed these)

| Channel | Range | Guarantee |
|---------|-------|-----------|
| Bearings θ_{ij} | [-180°, +180°] | atan2 range — exact for any composition |
| Hs | [0, 1] | By definition: Hs = 1 - H/ln(D) |
| Angular velocity ω | [0°, 180°] | Absolute angular change per step |

### Data-Adaptive Bounds (pre-scanned at load time)

| Channel | Depends On | Japan EMBER D=8 (actual) |
|---------|-----------|--------------------------|
| CLR h_j | min(x_j) in dataset | [-33.86, +6.79] |
| XY scatter | CLR range on both axes | same |

The CLR has no finite mathematical ceiling — it depends on how close any carrier approaches zero. For the Japan EMBER dataset, Nuclear's CLR reaches -33.86 in 2014 (post-Fukushima shutdown = composition effectively zero). This is genuine signal, not noise.

### Scale Determination Algorithm

1. Load all N records
2. Scan all CLR values across all carriers and all time steps
3. Find global min/max
4. Pad by 10% of range for visual margin
5. Lock these limits for all plates

### Universal Instrument Ranges

For any real-world compositional system where all carriers remain above a practical floor:

| Composition floor | CLR range (D=8) | CLR range (D=4) |
|-------------------|-----------------|-----------------|
| 1% (0.01) | approx [-3.5, +3.5] | approx [-2.5, +2.5] |
| 0.1% (0.001) | approx [-5.5, +5.5] | approx [-4.0, +4.0] |
| 0.01% (0.0001) | approx [-7.5, +7.5] | approx [-5.5, +5.5] |
| epsilon floor | depends on float precision | — |

A carrier at true zero (x_j = 0) is mathematically undefined in CLR (ln(0) = -∞). The engine uses a composition floor (typically 1e-15) to handle this, producing very large negative CLR values that indicate "carrier absent from system."

## The instrument reads. The expert decides. The loop stays open.
