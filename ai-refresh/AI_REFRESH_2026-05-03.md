# AI Refresh — 2026-05-03

## Session Summary

Stage 1 CBS instrument completed as standard tool. Layout finalized to Higgins tensor data field layout v1.0 (from Visio specification). Fixed-scale display verified. Historical analysis comparison completed. Engine verified and ready for collective cross-check. Stage 1 output system is concluded and ready for deployment.

## What Changed

### 1. Fixed-Scale Instrument Display (stage1_plates_raw.py) — with improved layout

The Stage 1 section plate generator now operates like a physical oscilloscope with a fixed graticule. All axis scales are locked across all time frames so rapid scrolling through the PDF cine-deck reveals genuine compositional movement against a constant backdrop.

Scale determination algorithm:
1. Load all N records
2. Pre-scan all CLR values across all carriers and all time steps
3. Compute global min/max
4. Pad by 10% of range for visual margin
5. Lock these limits for ALL plates in the output

Fixed bounds:
- XZ face (bearings): [-180, +180] deg — mathematically exact (atan2 guarantee)
- YZ face (CLR bars): data-adaptive, pre-scanned from full dataset
- XY face (CLR scatter): same CLR range on both axes
- Hs: [0, 1] — exact by definition

Japan EMBER D=8 actual ranges:
- Bearings: [-179.40, +178.84] deg
- CLR: [-33.86, +6.79] → padded to [-37.93, +10.85]
- Hs: [0.1978, 0.3409]

Layout — Higgins tensor data field layout v1.0 (final):

```
┌──────────┬──────────┬──────────────────┐
│  Info    │  Legend  │  XZ Bearings bar │
├──────────┴──────────┼──────────────────┤
│  XY Scatter         │  YZ CLR bar      │
└─────────────────────┴──────────────────┘
```

- 2x3 grid: Info and Legend share top-left as two columns, 3 face views fill remaining area
- Width ratios from Visio spec: Info 1.82, Legend 1.76, Charts 2.91
- XY scatter spans Info+Legend width below for maximum plot area
- No wasted footer or empty quadrants — every panel is data or essential reference
- Scale range shown in each face title
- Info panel contains: dataset, metrics, and scale summary
- Legend panel contains: all D(D-1)/2 pair indices in 2 columns with carrier names
- Visio specification file: `tensor_data_field_layout_v1.0.vsdx`

### 2. EMBER Analysis Evolution Document (EMBER_Analysis_Evolution.docx)

7-page landscape document covering all 10 eras of EMBER Japan analysis across the entire project history. Contains: development timeline table, numerical comparison, CLR coordinates table, validity assessment per method, conclusion.

Key finding: All methods computing Hs on D=8 produce identical values. The data never changed — only the analytical depth evolved. Two bugs identified in historical methods: phantom D=9 carrier (Other Renewables=1e-06) and Year-as-carrier in Hs-M02 pipeline. The current Stage 1 engine addresses both flaws.

### 3. Standard Method Designation

`stage1_plates_raw.py` is now designated as the STANDARD METHOD for Stage 1 output:
- Field-deployable (laptop, no network, no AI)
- Pure Python + matplotlib only
- Reads stage1_output.json, produces multi-page PDF or individual PNGs
- Fixed scales for cine-deck scrolling
- Monochrome, raw data, no interpretation
- Scales to any D (number of carriers)

### 4. CBS Display Range Theory

Documented in README.md — the mathematical bounds of all CBS channels:

| Channel | Bound Type | Range |
|---------|-----------|-------|
| Bearings theta_ij | Exact | [-180, +180] deg |
| Hs | Exact | [0, 1] |
| Angular velocity omega | Exact | [0, 180] deg |
| CLR h_j | Data-adaptive | depends on composition floor |

For CLR: the range depends on how close any carrier approaches zero. Nuclear CLR = -33.86 in 2014 (post-Fukushima, composition effectively zero) defines the lower bound for Japan EMBER.

## Performance Verification

Engine output independently verified:
- Hs: max diff from independent calculation = 5.03e-07 (JSON 6dp truncation)
- Bearings: max diff = 4.99e-05 deg (CLR rounding propagation)
- Helmsman: 100% match on all years
- Scale bounds: all within theoretical limits
- CLR sum-to-zero: holds to 2e-08 (floating point)

## Critical Invariants for Collective Cross-Check

Other AIs running the same EMBER Japan CSV through equivalent mathematics MUST reproduce these values:

```
D = 8
N = 26
Hs(2000) = 0.234683
Hs(2012) = 0.312291
Hs(2025) = 0.197825
Helmsman(2012) = Nuclear
Helmsman(2014) = Nuclear
Ring(2000) = Hs-2
Ring(2025) = Hs-2
```

If any AI produces different values from the same input data, the discrepancy indicates either: (a) a different composition floor handling for zero-proportion carriers, (b) a different rounding convention, or (c) a genuine mathematical error that needs investigation.

The diversity of AI mathematical implementations is the best test available: if all produce identical results from identical data, the engine is confirmed correct by independent verification.

## Reproducibility Instructions

```bash
# Step 1: Run engine (EMBER CSV -> JSON)
python stage1_engine.py path/to/ember_japan_d8.csv stage1_output.json

# Step 2: Generate fixed-scale plates (JSON -> PDF)
python stage1_plates_raw.py stage1_output.json stage1_plates_raw.pdf

# Step 3: Verify (check invariants)
python -c "import json; d=json.load(open('stage1_output.json')); print(d['records'][0]['hs'], d['records'][12]['hs'], d['records'][25]['hs'])"
# Expected: 0.234683 0.312291 0.197825
```

## Files Modified This Session

| File | Change |
|------|--------|
| `HCI/codawork2026/stage1_plates/stage1_plates_raw.py` | Full layout redesign to v1.0 (2x3 grid), fixed-scale pre-scan, locked axes |
| `HCI/codawork2026/stage1_plates/stage1_plates_fixed.pdf` | Final output — 26 plates, layout v1.0, fixed scales |
| `HCI/codawork2026/stage1_plates/tensor_data_field_layout_v1.0.vsdx` | New — Visio layout specification |
| `HCI/codawork2026/stage1_plates/README.md` | Layout v1.0 diagram, display range theory, standard method, file table |
| `HCI/codawork2026/stage1_plates/EMBER_Analysis_Evolution.docx` | New — 10-era historical comparison |
| `ai-refresh/PREPARE_FOR_REPO.json` | Updated for push #14, layout v1.0, display ranges |
| `ai-refresh/HS_MACHINE_MANIFEST.json` | Added hci_stage1_standard_tool, layout v1.0 |
| `ai-refresh/AI_REFRESH_2026-05-03.md` | This file |

## Full Output Table (for collective verification)

```
Year           Hs   Ring      omega     Helmsman        d_A
------------------------------------------------------------
2000       0.234683   Hs-2     0.0000          ---   0.000000
2001       0.239561   Hs-2     2.8189         Wind   0.847846
2002       0.234830   Hs-2     1.5248         Wind   0.496689
2003       0.222849   Hs-2     3.7738         Wind   0.757601
2004       0.225250   Hs-2     3.3324         Wind   0.582491
2005       0.227556   Hs-2     2.4787        Hydro   0.391966
2006       0.227477   Hs-2     2.6642 Other Fossil   0.316211
2007       0.227024   Hs-2     3.2122        Hydro   0.371740
2008       0.232256   Hs-2     2.0079      Nuclear   0.213233
2009       0.247095   Hs-2     5.2774 Other Fossil   0.545961
2010       0.237884   Hs-2     2.4037        Solar   0.282318
2011       0.230931   Hs-2     9.4013      Nuclear   0.837843
2012       0.312291   Hs-3    27.4642      Nuclear   2.200635
2013       0.312583   Hs-3     7.5396        Solar   0.639857
2014       0.340926   Hs-3    66.1070      Nuclear  34.870573
2015       0.309676   Hs-3    49.6746      Nuclear  33.667556
2016       0.303033   Hs-3    16.2591      Nuclear   1.320048
2017       0.308283   Hs-3    10.9468 Other Fossil   0.767882
2018       0.279970   Hs-2     7.1966      Nuclear   0.507945
2019       0.268630   Hs-2     7.6236 Other Fossil   0.467986
2020       0.280146   Hs-2     9.7926      Nuclear   0.591660
2021       0.246834   Hs-2     4.7105      Nuclear   0.339626
2022       0.236919   Hs-2     7.4261 Other Fossil   0.424692
2023       0.213214   Hs-2    10.0007      Nuclear   0.555145
2024       0.209872   Hs-2     6.0418 Other Fossil   0.327601
2025       0.197825   Hs-2     3.7598    Bioenergy   0.221651
```

## Status

- Engine: VERIFIED
- Fixed scales: CONFIRMED (axis limits identical on all 26 plates)
- Layout: v1.0 FINAL (Higgins tensor data field layout, from Visio spec)
- Standard method: DESIGNATED (stage1_plates_raw.py)
- Stage 1 output system: CONCLUDED — tool display makes sense, ready for deployment
- Ready for: collective cross-check by other AIs
- Push #14: READY

## The instrument reads. The expert decides. The loop stays open.
