# HUF-CNT Output Doctrine

**Status:** Locked.   **Effective:** v1.1 onwards.   **Date:** 2026-05-05.

This document is the formal declaration of how the HUF-CNT system
classifies, displays, and discloses analytical content. Every
schema-conformant output, every plate, and every published reference
experiment is governed by this doctrine. It is the instrument
declaration; treat it as authoritative for plate generation, schema
extension, and downstream tooling.

---

## 1. The order doctrine

The system classifies every analytic quantity by its derivational
**order** relative to the input compositional data.

| Order | Definition | Examples |
|---|---|---|
| **Order 1 — first principles** | Quantities derived from a single composition at one timestep, by closure and log-ratio operations alone. No reference to other timesteps, no derivative content. | Closed composition (xj), CLR coordinates, ILR-Helmert projection, geometric mean, Aitchison norm, Helmert basis loadings. |
| **Order 2 — metric / inter-timestep** | Quantities derived by combining two or more timesteps, or by referencing the metric tensor's off-diagonal structure. | Bearings θ, angular velocity ω, steering metric κ, helmsman σ, Higgins scale Hs, ring class, lock events, variation matrix τij, pair-index analysis. |
| **Order 3 — recursive / dynamical** | Quantities produced by recursing on Order-2 outputs: the depth tower, IR classification, cycle/attractor analysis, dynamical systems readouts. | Energy / curvature towers, period-2 attractor, IR class, contraction λ, Banach contraction, per-carrier Lyapunov, recurrence, observability. |
| **Order 4+ (reserved)** | EITT bench-test, cross-dataset comparison, statistical inference, mission-command synthesis. Future-extensible. | EITT M-sweep, cross-dataset comparison, schema-validator surface. |

The order is **a schema property**, not a runtime flag. Every analytic
block in the canonical CNT JSON declares its order. Viewers that
understand the doctrine route blocks of order N to the appropriate
display surface and only emit blocks of orders ≤ user_max_order.

---

## 2. Why this matters

Compositional analysis is layered. The lower the order, the more the
display reflects raw input content; the higher the order, the more it
reflects the engine's interpretation. Mixing orders in a single plate
without disclosure conceals which content is data and which is
inference. The doctrine forbids that.

Three consequences for the system:

1. **Disclosure as standard.** Every plate carries its order tag.
   `level 1 (first-principles)` on a Stage 1 v4 plate is normative,
   not decorative. A reader can refuse to consider higher-order
   conclusions and rely only on lower-order content; the plate has
   already told them which is which.

2. **Display routing.** Stage 1 plates render only Order-1 content.
   Stage 2 plates add Order-2. Stage 3 plates add Order-3. Stage 4+
   are cross-dataset / multi-run / inferential.

3. **Trust composition.** Users can read the system at the depth
   their question requires. A geochemist questioning the engine's IR
   classification does not need to trust the depth tower; they can
   stop at Order 2 (bearings) and still get a defensible plate. A
   user trusting the full chain reads up to Order 3 and beyond.

---

## 3. Locked standard for Stage 1: ILR-Helmert orthogonal triplet

The reference Stage 1 plate is **`atlas/stage1_v4.py`**:

* Three orthogonal panels showing pairs of the first three Helmert
  ILR axes (1×2, 1×3, 2×3) — the canonical orthonormal projection of
  the simplex.
* Stacked strip showing the closed composition with proportional
  segments and inline carrier labels.
* Carrier table listing each carrier with its closed value and CLR
  coordinate.
* Helmert axis loadings showing which carriers each ILR axis
  contrasts.
* Closure check Σ = 1.0 verified explicitly.
* FIXED HLR scale across the trajectory; auto magnitude factor
  (power of 10) declared on title and per-axis when scaling is
  needed.
* Provenance footer with source SHA, content SHA, run id, page n/N.

This is the locked Order-1 output for v1.1 and forward. Other Stage 1
modules (`ortho_plate_v3`, `ortho_plate_v2`, `ortho_plate.py`,
section_atlas tour plates) are deprecated. The legacy three-plate
layout in `atlas.py` ships as `--legacy-tours` for backward
compatibility but is no longer the default Stage 1 surface.

### Calibration fixture

The Stage 1 v4 module has a permanent calibration fixture in
`atlas/STANDARD_CALIBRATION_27pt_*` — a 3×3×3 grid in HLR space whose
plates show a clean nine-spot dot pattern in every orthogonal panel.
Re-running `python atlas/standard_calibration.py` regenerates the
fixture byte-identically. The fixture is the visual ground truth: any
plate that does not show the nine-spot pattern is misrendering the
projection, not the data.


### Doctrine refinement v1.0.1 (rounding rule)

Integer orders only. There is no Order 1.5. Any quantity that aggregates
across more than one timestep — Hs trajectory, Aitchison-norm trajectory,
ILR-axis trajectory, system course plot, V_net = h_final − h_start,
path_length, course_directness — rounds **up** to Order 2, even when each
constituent data point is itself Order 1.

The boundary is single-composition vs multi-composition. Single = Order 1.
Multi = Order ≥ 2.

Consequence: the Stage 1 closing summary's Hs / norm / ILR trajectories
formally belong on Stage 2, not Stage 1. They are kept on the Stage 1
closing plate as a courtesy bridge, but the canonical home is Stage 2.

---

## 4. Stage tower

| Stage | Standard plate module | Pseudocode | R port | Calibration | Highest order |
|---|---|---|---|---|---|
| Stage 1 (locked) | `atlas/stage1_v4.py`           | `cnt/CNT_PSEUDOCODE.md` | `cnt/cnt.R`     | `STANDARD_CALIBRATION_27pt_*` | Order 1 |
| Stage 2 (locked) | `atlas/stage2_locked.py`       | `atlas/STAGE2_PSEUDOCODE.md` | `atlas/stage2.R` | `STANDARD_CALIBRATION_stage2_*` | Order 2 |
| Stage 3          | `atlas/stage3.py` (planned)    | tbd | tbd | tbd | Order 3 (depth tower, IR, attractor) |
| Stage 4          | `atlas/stage4.py` (planned)    | tbd | tbd | tbd | Order 4+ (EITT, comparison, inference) |

**Stage 2 (locked) — content (19 plates):** cover/declaration; System
Course Plot (Math Handbook Ch 15) with PCA 2D path, S/F markers, V_net
arrow, and `course_directness ∈ [0, 1]`; trajectory aggregates rounded
up from Stage 1 (Hs, Aitchison norm, ILR axes 1-3); polar bearing rose
at 4 sample timesteps; bearing heatmap T × C(D,2); ω trajectory; metric
trace + condition; helmsman lineage timeline; helmsman frequency +
transitions + per-year displacement; ring class strip + Hs; lock event
timeline; variation matrix τ_ij heatmap; pair Pearson r heatmap +
co-movement scatter; Compositional Bearing Scope CBS three orthogonal
faces (Math Handbook Ch 16); pairwise divergence (distance matrix +
top-15 ranking); ω vs Hs scatter; numeric summary.

Each stage module reads the same JSON. Each stage adds disclosed
content of its highest order; lower-order content is preserved as a
small inset or footer rather than removed (so the geochemist who
trusts only Order 1 still sees the closed composition on a Stage 3
plate, even when the headline number is the IR class).

---

## 5. JSON-controller opt-in

`mission_command/master_control.json` per experiment:

```json
"experiments": {
  "<id>": {
    "plate_level": 1,
    "is_temporal": true,
    "ordering_method": "by-time",
    "carrier_aliases": { ... }
  }
}
```

`plate_level` ∈ {1, 2, 3, 4}. The atlas reads this and refuses to
render content above the declared level. Mixing levels in one atlas
is forbidden by design. To inspect higher orders, run a separate
atlas at the higher level — the catalog records both runs side by
side, and the delta tool shows what each level adds.

---

## 6. Schema implications

The schema (currently 2.0.0) annotates every analytic block with a
`_function` tag and a `coda_standard` / `higgins_extensions` split.
v1.1 introduces a parallel `_order` tag for every block:

```
"depth": {
  "_function": "review",
  "_order": 3,
  "coda_standard":     {...},
  "higgins_extensions":{...}
}
```

Order tags are *additive only* — old viewers ignore them; new viewers
route blocks. The schema bumps to 2.1.0 (already planned for native
units, Feature B) and the order tags ride that bump.

---

## 7. Adapters and pre-parsers

Adapter outputs are **Order-0** — raw composition before closure,
before any log-ratio. The adapter is responsible for delivering
clean, deterministic compositions to the engine. Once closure is
applied (in `cnt.py`), the data enters Order 1.

The disclosure document (`adapters/ADAPTERS_DISCLOSURE.md`) carries
the Order-0 narrative: source, transformation, what is preserved,
what is discarded, output SHA. Together with the Order-1 closure step
in the engine, this completes the trust chain CSV → JSON → plate.

---

## 8. Recommendation for downstream tools

Any tool reading a CNT JSON should:

1. Declare which order(s) it consumes.
2. Refuse to render content at an order higher than the user's
   declared `plate_level`.
3. Carry the order tag on every visual surface (plate, table, HTML
   page, slide deck).
4. Cite the Helmert basis explicitly when displaying ILR (the basis
   is in `tensor.helmert_basis.coefficients`).

Tools that emit content not derivable from the JSON via the doctrine
are not conforming, regardless of how visually compelling the
output. The doctrine is what makes "scientific instrument" different
from "research script."

---

## 9. Versioning

This doctrine v1.0 effective with HUF-CNT v1.1.0. Changes to the
order classification of any field in the schema bump the schema
minor version. Removing or re-classifying fields requires a schema
major bump and a doctrine version bump.

The doctrine document itself is hashed in
`atlas/OUTPUT_DOCTRINE.md.sha256` for tamper-detection on long-term
archives.

---

*The instrument reads at first order.*
*The expert combines orders deliberately.*
*The output declares which orders are present.*
*The loop stays open at every level.*
