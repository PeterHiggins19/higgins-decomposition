# 03_combined — Cross-dataset views

Cross-country panel and shared-frame visualisations that span all 8 EMBER
countries + World aggregate at once. These are the showpiece pages of the
talk: one PCA frame, one barycentre, one z-spine for time.

## Contents

```
03_combined/
├── _pipeline_manifest.json                       run record
├── plate_time_projector_codawork2026_ember.html  shared-frame 3D viewer
├── spectrum_paper_codawork2026_ember.pdf         cross-dataset spectrum
└── stage1_*.pdf, stage2_*.pdf                    per-country pages bundled here
```

The `plate_time_projector_*.html` is the interactive 3D widget — open in any
browser, drag to rotate, time-slider scrubs through 2000–2025, all 9
trajectories overlay in a shared PCA frame.

## See also

- `../README.md` — full demo-package overview
- `../../../atlas/plate_time_projector.html` — generic projector source
- `../../../atlas/spectrum_paper.py` — cross-dataset spectrum generator
