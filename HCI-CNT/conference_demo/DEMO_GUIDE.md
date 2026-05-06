# CodaWork 2026 — 30-minute Demo Guide

A turnkey script for presenting the HUF-CNT system at the conference.
Each step references a file in `cnt_demo/` so an audience can reproduce
or audit on the spot.

## Slide 0 — Cover (1 min)
Open `cnt_demo/00_OVERVIEW.md`. Read the 5-line abstract.

## Slide 1 — The contract (3 min)
Open `cnt_demo/05_doctrine/OUTPUT_DOCTRINE.md`. Show:
- order classification (1 = first principles, 2 = metric/inter-step,
  3 = recursive/dynamical, 4+ = inference)
- mixing-orders rule (forbidden in one plate)
- determinism guarantee tied to `content_sha256`

## Slide 2 — The engine (3 min)
Open `cnt_demo/01_engine/cnt.py` and `cnt.R`. Point at the
`USER CONFIGURATION` block. 14 documented constants. Same input + same
config → byte-identical JSON.

## Slide 3 — Stage 1, one country (4 min)
Open `cnt_demo/02_per_country/ember_jpn/stage1_ember_jpn.pdf`. Scroll the
27 plates (26 timesteps + summary) — show the trajectory in HLR space
with FIXED scale, the closure check, the carrier table, the Helmert
loadings.

## Slide 4 — Stage 2, one country (4 min)
Open `cnt_demo/02_per_country/ember_jpn/stage2_ember_jpn.pdf`. Walk
through:
- p2 System Course Plot (V_net, course directness)
- p5 Polar bearing rose
- p15 CBS three orthogonal faces
- p17 Pairwise divergence ranking
- p19 Summary

## Slide 5 — Cross-dataset spectrum (3 min)
Open `cnt_demo/03_combined/spectrum_paper_codawork2026_ember.pdf`. Show
how 8 countries + World compare on FIXED scales:
- complexity (Aitchison norm)
- velocity (mean |ω|)
- peak structural change
- Hs drift
- mean composition heatmap

## Slide 6 — Interactive plate-time projector (5 min)
Open `cnt_demo/03_combined/plate_time_projector_codawork2026_ember.html`
in a browser. Demonstrate:
- per-country mode (PCA frame for that country)
- COMBINED mode (one shared frame across all 8 countries)
- valid connection lines only — every edge hover-attributable to JSON
- threshold slider for pair edges
- year scrubber

## Slide 7 — Calibration (3 min)
Open `cnt_demo/04_calibration/STANDARD_CALIBRATION_27pt_stage1v4.pdf`
(Stage 1 ground truth — 27-point grid). Show drift = O(1e-10).
Then `STANDARD_CALIBRATION_stage2_A_straight.pdf` and
`STANDARD_CALIBRATION_stage2_B_loop.pdf` (Stage 2 ground truth —
directness = 1.0 / 0.0 exactly at IEEE floor).

## Slide 8 — Doctrine + extension menu (2 min)
Open `cnt_demo/05_doctrine/V1.1_FEATURE_MENU.md`. Show A–G features and
status. The package is extension-ready.

## Slide 9 — Q&A (2 min)
Point at `experiments/INDEX.json` for the full 20-experiment SHA list,
including the 8 EMBER + 12 domain experiments.

