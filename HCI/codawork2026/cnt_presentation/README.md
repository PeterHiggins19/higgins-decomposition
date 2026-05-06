# CNT Tensor Engine — CoDaWork 2026 Presentation Preparation

Slides for the Compositional Navigation Tensor engine section of the CoDaWork 2026 presentation.

**Status**: In development. Slides added incrementally as content matures.

## Current Slides (9 total: 1 title + 8 content)

| Slide | File | Content |
|-------|------|---------|
| Title | (generated) | CNT section header |
| 1 | `slide_01a_pipeline_input.svg` | Raw data to CLR transform (Y -> x -> h) |
| 2 | `slide_01b_theta_omega.svg` | Channels 1-2: Bearing tensor + Angular velocity |
| 3 | `slide_01c_kappa_sigma.svg` | Channels 3-4: Steering metric + Helmsman |
| 4 | `slide_01d_corollaries_output.svg` | Corollaries and total output summary (66 measurements) |
| 5 | `slide_02a_cube_structure.svg` | CBS cube 3D structure with face labels |
| 6 | `slide_02b_higgins_axis.svg` | Higgins axis time projection (cine-deck) |
| 7 | `slide_02c_face_specs.svg` | Three face specifications + info panel |
| 8 | `slide_03_hlr_evidence.svg` | HLR unit family conversion evidence (7 systems) |

Legacy (superseded by enlarged versions above):

| File | Status |
|------|--------|
| `slide_01_cnt_transform_pipeline.svg` | Superseded — text too small for back row |
| `slide_02_cube_face_projections.svg` | Superseded — text too small for back row |

## Build

```bash
NODE_PATH=/usr/local/lib/node_modules_global/lib/node_modules node build_cnt_pptx.js
```

Produces `CNT_Tensor_Engine.pptx` (9 slides).

## Higgins Display Standard

- MAXIMUM TEXT SIZE — fill available space, never shrink to fit
- BACK ROW READABLE — 18pt minimum body, 28pt titles, 16pt math
- MORE SLIDES OVER SMALLER TEXT — split rather than compress
- LINE GRAPHICS ONLY — no gradients, shadows, 3D effects, colour fills
- 7-BIT CLEAN — ASCII text, monochrome, no decoration
- MONOCHROME — white on dark (#1a1a1a background)
- SVG source files — vector, scalable, editable
- Rendered to PNG via sharp — embedded in PPTX at 1920px width

## Files

| File | Purpose |
|------|---------|
| `slide_01a_pipeline_input.svg` | Pipeline stage 1: Raw -> Closure -> CLR |
| `slide_01b_theta_omega.svg` | Channels theta + omega (full specs) |
| `slide_01c_kappa_sigma.svg` | Channels kappa_HS + sigma (full specs) |
| `slide_01d_corollaries_output.svg` | Corollaries + output dimensions |
| `slide_02a_cube_structure.svg` | CBS cube isometric with axes and labels |
| `slide_02b_higgins_axis.svg` | Time axis with section plate slices |
| `slide_02c_face_specs.svg` | Three face specifications + info panel |
| `slide_03_hlr_evidence.svg` | HLR unit family k-factors + round-trip |
| `build_cnt_pptx.js` | PptxGenJS generator script |
| `CNT_Tensor_Engine.pptx` | Generated output (rebuild with script above) |
| `README.md` | This file |

## Relationship to CNT Character Manual

The same SVG diagrams are referenced in `HCI/CNT_EXPLORATORY.md` (the running Q&A character manual) as canonical line-art figures. The presentation and the manual share identical source artwork.

## Adding New Slides

1. Create `slide_NNx_description.svg` in this folder (B&W line art, large text)
2. Add entry to SLIDES array in `build_cnt_pptx.js`
3. Rebuild PPTX
4. Reference in CNT_EXPLORATORY.md if the diagram belongs in the manual

## HLR Unit Family — Universal Adapter

HLR is a member of the log-ratio level family. Any data natively expressed in nepers, decibels, log fold change, or any log-ratio unit is compositional by nature and directly displayable on a CNT plate via a constant scale factor. The info panel shows the DUT native unit with conversion.

---

The instrument reads. The expert decides. The loop stays open.
