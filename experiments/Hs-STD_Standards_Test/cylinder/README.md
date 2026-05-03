# STD-CYLINDER — Cylinder Standard

**Experiment:** Hs-STD (Standards Test)  
**Test object:** Cylinder Standard  
**Author:** Peter Higgins  
**Date:** 2026-05-01  
**Result:** PASS

---

## Object Specification

The cylinder is the degenerate standard: a composition that is uniform at every timestep.

| Parameter | Value |
|-----------|-------|
| Carriers (D) | 27 |
| Timesteps (T) | 41 |
| Composition | p\_j = 1/D = 0.037037 for all j, all t |
| CLR at any timestep | 0.000000 (to machine precision; |CLR\_j| < 2×10⁻¹⁵) |
| CLR spread | 0.000000 at every timestep |
| Degenerate timesteps | 41 of 41 |
| Lock acquisition | None |
| Lock loss | None |

## Construction

All 27 carriers hold equal weight at all 41 timesteps. The composition is the centroid of the 27-simplex: the maximally uninformative point.

    p_j(t) = 1/27  for all j ∈ [1,27], t ∈ [0,40]

After CLR transform: clr\_j = log(1/27) − mean(log(x)) = 0, for all j. The CLR vector is the zero vector at every timestep. Proportions sum to 1 and CLR values sum to 0 at every timestep (verified).

## Expected Projection

No polygon at any timestep. The polar projector has no relative structure to render. All 41 timesteps are degenerate. A DEGEN diamond marker should appear at each frame. No polygon vertices should be placed.

## Observed Projection

DEGEN marker at all 41 timesteps. No polygon rendered at any timestep. Zero false structure introduced.

## Test Purpose

The cylinder tests the most critical instrument failure mode: generating pattern from a uniform composition. Any false polygon at any timestep would constitute a fabrication failure. The instrument passes if and only if it produces zero polygons across all 41 timesteps.

A real dataset that resembles the cylinder (CLR spread near zero across many timesteps) is a dataset with near-uniform carrier distribution. The instrument correctly reports that state. The expert then decides whether that uniformity is informative for the domain under study.

## Result: PASS

Zero false polygon renderings across all 41 timesteps.

## Artifacts

| File | Description |
|------|-------------|
| `STD-cylinder_polar_stack.json` | Polar stack data — 27 carriers, 41 timesteps, uniform composition |
| `STD-cylinder_projector.html` | Single-object interactive projector |
| `STD-cylinder_cinema.pptx` | Frame-by-frame cinema (41 slides) |

## Reference

Aitchison, J. (1986). *The Statistical Analysis of Compositional Data*. Chapman and Hall.
