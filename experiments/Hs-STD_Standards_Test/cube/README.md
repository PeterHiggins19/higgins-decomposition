# STD-CUBE — Cube Standard

**Experiment:** Hs-STD (Standards Test)  
**Test object:** Cube Standard  
**Author:** Peter Higgins  
**Date:** 2026-05-01  
**Result:** PASS

---

## Object Specification

The cube is the static non-uniform standard: a composition with alternating high and low carrier quadrants that is identical at every timestep. The cross-section through the composition space is constant. No degenerate timesteps.

| Parameter | Value |
|-----------|-------|
| Carriers (D) | 27 |
| Timesteps (T) | 41 |
| High carriers | C01–C06, C13–C18 (12 carriers, quadrants 0 and 2) |
| Low carriers | C07–C12, C19–C27 (15 carriers, quadrants 1 and 3) |
| Proportion — high | 0.063492 (= 2.0 / 31.5) |
| Proportion — low | 0.015873 (= 0.5 / 31.5) |
| High : low ratio | 4.0 exactly |
| CLR — high | +0.770164 |
| CLR — low | −0.616131 |
| CLR spread | 1.386295 (constant) |
| Degenerate timesteps | 0 of 41 |
| Lock acquisition | None (entire run resolved from t=0) |
| Lock loss | None |

## Construction

The 27 carriers are partitioned into 4 angular quadrants with 6 carriers each. The 3 remainder carriers (C25–C27) fall into quadrant 3 (low). Before closure, each quadrant is assigned a raw weight:

    Quadrant 0 (C01–C06):  raw = 2.0  →  HIGH
    Quadrant 1 (C07–C12):  raw = 0.5  →  LOW
    Quadrant 2 (C13–C18):  raw = 2.0  →  HIGH
    Quadrant 3 (C19–C27):  raw = 0.5  →  LOW

Total raw weight: 12 × 2.0 + 15 × 0.5 = 24.0 + 7.5 = 31.5

After closure:
- High carriers: p = 2.0 / 31.5 = 0.063492...
- Low carriers:  p = 0.5 / 31.5 = 0.015873...

The ratio p\_high / p\_low = 4.0 exactly. Proportions sum to 1 and CLR values sum to 0 at every timestep (verified). The same composition is repeated identically at all 41 timesteps.

## Expected Projection

A polygon with two prominent high lobes (at angular positions corresponding to C01–C06 and C13–C18) and two recessed low lobes (at C07–C12 and C19–C27 positions), forming a square-like shape. The polygon is identical at every timestep. No DEGEN frames. No LOCK markers.

The shape is not a perfect square because the carrier count per quadrant is not equal (12 high, 15 low), and the angular positions of carriers within quadrants are contiguous rather than optimally arranged for a symmetric square. The projected shape approximates a square and is constant.

## Observed Projection

Constant polygon with the correct 4:1 lobe structure at all 41 timesteps. Shape does not drift. No DEGEN frames. No LOCK markers. The 4:1 carrier weight ratio is preserved through the full closure → CLR → normalization → projection chain.

## Test Purpose

The cube tests two instrument properties:

1. **Static fidelity** — the same composition repeated 41 times must produce an identical polygon 41 times. Any drift in the rendered polygon would indicate a normalization or floating-point consistency defect.

2. **Lobe structure preservation** — the 4:1 composition ratio must be correctly represented in the relative lobe heights. A 4:1 ratio in proportion space maps to a fixed offset in CLR space (high: +0.770164, low: −0.616131) and must produce visually distinguishable high and low lobes.

The cube also establishes that the instrument handles the remainder-carrier case correctly. The 3 extra carriers in quadrant 3 shift the low lobe slightly but do not produce asymmetry in the high lobes, which is the expected geometric result.

## CLR Values (constant across all timesteps)

| Carrier group | Carriers | CLR value |
|---------------|----------|-----------|
| Quadrant 0 (high) | C01–C06 | +0.770164 |
| Quadrant 1 (low) | C07–C12 | −0.616131 |
| Quadrant 2 (high) | C13–C18 | +0.770164 |
| Quadrant 3 (low) | C19–C27 | −0.616131 |

CLR spread = 0.770164 − (−0.616131) = 1.386295 (constant at all timesteps).

## Result: PASS

Non-degenerate polygon at all 41 timesteps, constant shape across time, correct 4:1 lobe structure preserved through the full pipeline.

## Artifacts

| File | Description |
|------|-------------|
| `STD-cube_polar_stack.json` | Polar stack data — 27 carriers, 41 timesteps, constant alternating quadrant composition |
| `STD-cube_projector.html` | Single-object interactive projector |
| `STD-cube_cinema.pptx` | Frame-by-frame cinema (41 slides) |

## Reference

Aitchison, J. (1986). *The Statistical Analysis of Compositional Data*. Chapman and Hall.
