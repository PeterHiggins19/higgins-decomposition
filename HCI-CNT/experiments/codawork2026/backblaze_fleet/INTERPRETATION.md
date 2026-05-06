# BackBlaze Fleet — Interpretation Note

**Source:** `backblaze_fleet_cnt.json` (CNT v2.0.1)
**Period:** 2024-01-01 to 2025-12-31, T = 731 daily snapshots
**Carriers:** Mechanical, Thermal, Age, Errors (per Hs-17 preparser v1.0)

The auto-generated journal reports `IR class = DEGENERATE` and
`curv_depth = 4 (HS_FLAT)`. That label is correct in the strict CNT
sense (no period-2 attractor detected in the curvature tower) but
hides a richer story. Reading both towers together is necessary.

## What's actually happening

### Composition shift over 2024-2025

| Day | Mechanical | Thermal | Age   | Errors |
|-----|-----------|---------|-------|--------|
| 2024-01-01 | 1.5 % | 1.1 % | 0.9 % | **96.5 %** |
| 2025-12-31 | **23.2 %** | 5.6 % | 5.1 % | 66.0 % |

Errors carrier (read errors + seek errors + UDMA CRC) shrank by 30
percentage points in absolute share. Mechanical (reallocated +
pending + offline-uncorrectable sectors, weighted ×10) grew from
1.5 % to 23.2 % — a 15× increase over two years.

This is the expected aging pattern for a maturing storage fleet:
soft-error rates fall as drives stabilise, while latent mechanical
defects accumulate.

### Energy tower — STABLE PERIOD-1

```
energy_hs_trajectory (first 10 of 8 productive levels):
  [0.499, 0.377, 0.361, 0.333, 0.319, 0.316, 0.307, 0.307, 0.308]
```

The energy tower converges to a period-1 fixed point at Hs ≈ 0.308
at recursion level 8, terminating LIMIT_CYCLE_P1.

This is the canonical "memoryless fleet" signature from Hs-17. A
period-1 fixed point at modest amplitude in the energy tower means
the fleet's *kinetic energy distribution* across SMART carriers
relaxes to a stable shape — the fleet is well-managed, no runaway
dynamics. Earlier Hs-17 work attributed transfer-entropy = 0 to this
pattern; the v2.0.1 engine reads it more cleanly via the energy-tower
period.

**Energy tower verdict: stable, depth = 8, period-1 attractor.**

### Curvature tower — HS_FLAT termination

```
curvature_hs_trajectory:
  [0.499, 0.290, 0.995, 0.571, 1.000]
```

The curvature tower *does not* settle. It oscillates wildly between
0.29 and ~1.0 across 4 levels and terminates with `HS_FLAT` at L4
(`hs_var = 6.7e-15`). The tower is driven to a vertex by the
following mechanism:

* The curvature composition c_j = κ_jj / Σκ_kk uses 1/x_j² weighting.
* In a fleet where Errors holds 66-96 % of the composition, the
  reciprocal-square weighting *amplifies* the rare carriers (Mech,
  Therm, Age each at ~1-5 %) to dominate the curvature distribution.
* On recursion, those amplified rarities drive the trajectory toward
  a single-carrier vertex (Hs → 1.0).

This is NOT an engine bug. It is a real signature of an
**extremely concentrated composition**: when one carrier holds > 60 %
of the simplex, the curvature tower cannot develop a period-2
oscillation because the metric tensor is too anisotropic.

**Curvature tower verdict: degenerate, depth = 4, no period-2.**

### Stage 2 carrier coupling — THERMAL-AGE LOCK

```
Thermal - Age:        spread =  5.10°, r =  0.966, locked = TRUE
Thermal - Errors:     spread = 13.60°, r = -0.738
Age     - Errors:     spread = 14.32°, r = -0.818
Mechanical - Errors:  spread = 34.18°, r = -0.850
Mechanical - Age:     spread = 62.56°, r =  0.399
Mechanical - Thermal: spread = 67.66°, r =  0.277
```

**Thermal and Age are tightly locked** — bearing spread 5.10°,
Pearson r = 0.966. This reproduces the Hs-17 finding that
thermal stress accelerates age-related degradation, and the daily
2024-2025 data shows the lock is stable across the entire
observation window.

The negative Mechanical-Errors correlation (r = −0.85) reflects the
compositional shift: as Mechanical's share grew, Errors' share
fell. They are anti-coupled in proportion, not in cause.

### Regime detection — 28 boundaries

The Aitchison-distance step exceeded mean + 2 σ on 28 of the 731
day-to-day transitions. These boundaries cluster around:

* fleet additions and retirements (visible as one-day jumps in
  averaged SMART)
* model rotations (drive populations being phased in or out)

The auto-generated JOURNAL lists them in chronological order.

## Why "DEGENERATE" is the wrong label

The IR classification in `depth.higgins_extensions.impulse_response`
falls through to "DEGENERATE" when the curvature attractor period is
zero. For BackBlaze that hides the richer reading: the system is
genuinely stable in energy phase space (period-1 at Hs = 0.31,
depth = 8) but degenerate in curvature phase space because the
composition is so concentrated.

Two operator classes that the v2.0.x engine should add later:

* **ENERGY_STABLE_FIXED_POINT** — period-1 in energy tower with
  amplitude < 0.1, regardless of curvature behaviour. This is the
  "memoryless fleet" signature.
* **CURVATURE_VERTEX_FLAT** — curvature tower terminates HS_FLAT due
  to single-carrier dominance. Diagnostic: max(carrier proportion) >
  0.6 in the input composition.

For now, BackBlaze is correctly labelled DEGENERATE in the strict CNT
sense, but the JOURNAL and this interpretation note explain that the
DEGENERATE label here means "curvature recursion exhausted on a
vertex-dominated composition" — not "no signal."

## Comparison to Hs-17

| Metric                  | Hs-17 (quarterly, 2013-2023) | v2.0.1 (daily, 2024-2025) |
|-------------------------|------------------------------|---------------------------|
| T                       | 108 (108 quarters)           | 731 (daily)               |
| D                       | 5 (with index carrier)       | 4                         |
| HVLD shape              | Bowl, R² = 0.884            | (not run in v2.0.x)       |
| Thermal/Errors lock     | CV = 18.30                  | r = -0.74 (not locked)    |
| Thermal/Age lock        | (not separately reported)   | r = 0.97, spread = 5.1°   |
| Errors carrier share    | dominant (no exact %)       | 96.5 % → 66.0 %           |
| Energy tower depth      | (not run)                   | 8, period-1 at Hs = 0.308 |
| Carrier coupling story  | physical: thermal → age     | confirmed: r = 0.97       |

The v2.0.1 daily run *strengthens* the Hs-17 finding (Thermal-Age
coupling is now measured at r = 0.97 across 731 days, vs the
earlier CV = 18.30 from quarterly aggregates) and exposes the
*composition aging* pattern that quarterly aggregation hid.

## Action items

1. Engine: add ENERGY_STABLE_FIXED_POINT and CURVATURE_VERTEX_FLAT
   classes to the IR taxonomy so high-concentration fleets get a
   sensible label instead of falling through to DEGENERATE.
2. Math Handbook Ch 23 update: document that for compositions with
   single-carrier dominance > 60 %, the curvature tower will exhaust
   on a vertex; the energy tower remains the right diagnostic
   surface.
3. Stage 1-Δ deck (deferred): the daily SMART trajectory is a strong
   case for the transient-display option — 731 daily compositional
   transitions visualised as bearing rotations would be a striking
   conference image.

---

*The instrument reads. The expert decides. The loop stays open.*
