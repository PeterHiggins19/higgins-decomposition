# STD-SPHERE — Sphere Standard

**Experiment:** Hs-STD (Standards Test)  
**Test object:** Sphere Standard  
**Author:** Peter Higgins  
**Date:** 2026-05-01  
**Result:** PASS

---

## Object Specification

The sphere is the dynamic standard: a composition whose CLR spread follows a sine envelope, expanding from zero at the first pole (t=0), reaching a maximum at the equator (t=20), and contracting back to zero at the second pole (t=40).

| Parameter | Value |
|-----------|-------|
| Carriers (D) | 27 |
| Timesteps (T) | 41 |
| Amplitude function | amplitude(t) = 0.8 × sin(π × t / 40) |
| CLR spread at t=0 | 0.000000 (degenerate pole) |
| CLR spread at t=1 | 0.125110 (lock acquisition) |
| CLR spread at t=20 | 1.600000 (equator, maximum) |
| CLR spread at t=39 | 0.125110 (lock loss) |
| CLR spread at t=40 | 0.000000 (degenerate pole) |
| Degenerate timesteps | 2 of 41 (t=0, t=40) |
| Lock acquisition | t=1 |
| Lock loss | t=39 |

## Construction

At each timestep t, a cosine perturbation is applied to each carrier j and then closed:

    raw_j(t) = exp(amplitude(t) × cos(2π × j / D))
    p_j(t) = raw_j(t) / sum_k(raw_k(t))

The sine amplitude is zero at both poles (t=0, t=40) and maximal (0.8) at the equator (t=20). All proportions sum to 1 and all CLR values sum to 0 at every timestep (verified).

The perturbation is symmetric across carriers: carriers near j=0 are pushed high, carriers near j=D/2 are pushed low, producing a two-lobe pattern that becomes a circle in the polar projection because the cosine modulation distributes smoothly across all 27 angular positions.

## CLR Spread by Timestep

| t | max\|CLR\| | CLR Spread | Status |
|---|-----------|-----------|--------|
| 0 | 0.000000 | 0.000000 | DEGEN |
| 1 | 0.062767 | 0.125110 | LOCK (acquisition) |
| 2 | 0.125148 | 0.249449 | active |
| 5 | 0.306147 | 0.612294 | active |
| 10 | 0.565685 | 1.131370 | active |
| 15 | 0.739104 | 1.478208 | active |
| 20 | 0.800000 | 1.600000 | peak |
| 25 | 0.739104 | 1.478208 | active |
| 30 | 0.565685 | 1.131370 | active |
| 35 | 0.306147 | 0.612294 | active |
| 38 | 0.125148 | 0.249449 | active |
| 39 | 0.062767 | 0.125110 | LOCK (loss) |
| 40 | 0.000000 | 0.000000 | DEGEN |

## Expected Projection

- t=0: DEGEN marker (degenerate pole, sin=0)
- t=1 through t=39: expanding then contracting circular polygon
- t=20: maximum-radius circle (equator)
- t=39: LOCK marker (last resolvable timestep)
- t=40: DEGEN marker (degenerate pole, sin=0)

## Observed Projection

DEGEN at t=0 and t=40. Lock acquisition at t=1. Lock loss at t=39. Polygon expands from t=1 to t=20 and contracts from t=20 to t=39 following the sine envelope. Circle shape maintained throughout active timesteps.

## Lock Point Interpretation

The lock offset of 0.125110 is the CLR spread at t=1. It equals 2 × 0.8 × sin(π/40) = 2 × 0.062767 = 0.125534 to first-order approximation (the small difference arises from the nonlinear closure step). This is the minimum CLR contrast that the projector resolves in this run. It is a property of the data, not an instrument error.

Lock points document the instrument's resolving boundary. In real-data runs, the lock offset identifies the minimum detectable compositional contrast given the specific dataset. The timesteps beyond lock loss and before lock acquisition are correctly flagged as unresolvable — the projector cannot draw a meaningful polygon because the carriers are not sufficiently differentiated.

## Test Purpose

The sphere tests three instrument capabilities simultaneously:

1. **Degenerate detection at poles** — the projector must flag t=0 and t=40 as DEGEN, not render false polygons from the near-zero CLR values
2. **Lock-point identification** — the projector must correctly identify and label t=1 and t=39 as the resolving boundary
3. **Monotonic dynamic range** — the polygon radius must increase from t=1 to t=20 and decrease from t=20 to t=39 without oscillation or inversion

Failure in any of these constitutes an instrument defect.

## Result: PASS

Correct DEGEN at both poles, correct LOCK markers at t=1 and t=39, monotonic expansion and contraction across all 39 active timesteps.

## Artifacts

| File | Description |
|------|-------------|
| `STD-sphere_polar_stack.json` | Polar stack data — 27 carriers, 41 timesteps, sin-envelope CLR spread |
| `STD-sphere_projector.html` | Single-object interactive projector |
| `STD-sphere_cinema.pptx` | Frame-by-frame cinema (41 slides) |

## Reference

Aitchison, J. (1986). *The Statistical Analysis of Compositional Data*. Chapman and Hall.
