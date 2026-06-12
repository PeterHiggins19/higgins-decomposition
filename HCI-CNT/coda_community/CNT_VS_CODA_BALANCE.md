# CNT vs Standard CoDa — A Performance Balance Book

**Date:** 2026-05-05
**Engine target:** cnt 2.0.4 / Schema 2.1.0
**Audience:** CoDa-literate reviewers, instrument operators, partner labs

This is a short, deliberately-bounded paper that compares the
Compositional Navigation Tensor (CNT) approach to the established
Aitchison–Pawlowsky-Egozcue compositional-data (CoDa) toolkit on the
operations they share. The aim is to be specific about where CNT
buys real performance and reproducibility, and equally specific
about where standard CoDa methods remain the right choice.

CNT is not a replacement for CoDa. It is a different operator
algebra over the same simplex. Both compute, ultimately, in
log-ratio coordinates. Where the two diverge is in **how** they
arrive at those coordinates, and in **how** they handle the
practical singularities (zeros, near-poles, complex pair behaviour)
that arise in real datasets.

The headline of this paper: CNT is preferred *when* the workload
involves trajectories, high dimensionality, near-boundary
compositions, cross-dataset comparison, or audit-grade
determinism. For exploratory single-snapshot ternary work, the
classical CoDa approach is simpler and entirely sufficient.

---

## §1  The two diagnostic traditions

| | Aitchison–Pawlowsky CoDa (1986–) | Higgins CNT (2026) |
|---|---|---|
| Foundational object | the centred log-ratio (CLR) vector | the Compositional Navigation Tensor (bearings θ, angular velocity ω, curvature κ, helmsman σ) |
| Primary operation | log-ratio transform → ILR via Helmert | tensor decomposition with metric-dual involution M² = I |
| Orthogonality | enforced through the orthonormal Helmert basis | enforced through the metric tensor and its dual |
| Native unit | neper (natural-log ratio) | neper (Higgins-scale, optionally `bit` / `dB` per `metadata.units`) |
| Statistical companion | classical biplot, variation matrix, balance dendrogram, scree | bearing rose, helmsman lineage, period-2 attractor, depth tower, IR class |
| Strength | static-snapshot geometry, ratio-based testing | trajectory dynamics, recursive depth, cross-dataset structural comparison |

Both methods pass through the same simplex barycenter; both produce
log-ratio quantities measured in the same physical unit (the neper).
Where they differ is operational.

---

## §2  The atan2 simplification

The pairwise bearing θ_{i,j} between carriers *i* and *j* is the most
fundamental Order-1 derivative quantity. Standard CoDa, when computing
this explicitly, uses an `arccos` formula:

```
                   ⟨ u_i , u_j ⟩
θ_{i,j} = arccos( ─────────────── )         (1)
                   ‖u_i‖ · ‖u_j‖
```

with three numerical characteristics worth noting:

1. **Sign loss.** `arccos` returns values in `[0, π]`. The sign of
   the angle (which side of the reference direction) is lost; a
   second cross-product test must follow to restore it.
2. **Numerical instability near 0 and π.** Small angle errors are
   amplified because `arccos` derivatives blow up at the endpoints
   (the curve is nearly vertical there). This matters when carriers
   are nearly parallel or anti-parallel — exactly the situations
   we care most about (near-locks, phase-outs).
3. **Normalisation cost.** Two ‖·‖ evaluations and a dot product
   per pair, repeated D(D-1)/2 times per timestep.

CNT replaces this with a single `atan2` call:

```
θ_{i,j} = atan2( y_{i,j} , x_{i,j} )         (2)
```

where `(x_{i,j}, y_{i,j})` are the centred coordinates of carrier *j*
relative to carrier *i* in the local simplex frame. `atan2`:

* returns `[-π, π]` in one call — no sign-restoration step;
* is numerically stable for every quadrant including the
  axes, because its branch cuts are at the outer ±π and not at
  the angles we care about;
* is implemented as a single CPU instruction in IEEE 754.

In the CNT engine `cnt/cnt.py`, the bearing is computed once per
pair per timestep via `bearing_pairs()`; the result feeds the
metric ledger, ω(t), and the helmsman classifier without any
re-derivation.

### Numerical demonstration

For the EMBER Japan dataset (D = 8 carriers, T = 26 years, 28 pairs
× 26 timesteps = 728 bearings per run):

| Operation | arccos path (with sign correction) | atan2 path | Δ |
|---|---|---|---|
| Float ops per bearing | ≈ 12 (dot, two norms, divide, arccos, sign test) | ≈ 4 (atan2 itself) | **3× fewer** |
| Stability near θ = 0 | error ∝ √ε near zero | machine-precision | **better by ~10⁷** |
| Stability near θ = π | same √ε near pole | machine-precision | **better by ~10⁷** |
| Quadrant disambiguation | extra cross-product | implicit in atan2 | **simpler** |

That `~10⁷` factor is not theoretical — it's the regime where
trajectory locks live. A pair held near θ ≈ 0 for several timesteps
is a lock candidate; if the bearing's noise floor is √ε ≈ 10⁻⁸
instead of ε ≈ 10⁻¹⁵, the lock-detection threshold has to be set
that much higher and false-negative locks become more likely than necessary.

---

## §3  Three orthogonal views — side by side

The Stage 1 plate book offers three orthogonal projections of the
ILR space (XY = ILR(1)×ILR(2), XZ = ILR(1)×ILR(3), YZ =
ILR(2)×ILR(3)). Generating these the standard-CoDa way and the
CNT way, given the same input JSON:

### Standard CoDa procedure

```
For each timestep t in 1..T:
    1. Read closed composition x(t)
    2. Apply zero replacement (additive δ-substitution)
    3. Compute CLR(x(t))
    4. Build Helmert orthonormal basis V (D-1, D)
    5. ILR(t) = V @ CLR(t)         # (D-1)-vector

For each axis pair (a, b) in {(1,2), (1,3), (2,3)}:
    6. Extract pairs of ILR coordinates per timestep
    7. Compute axis-specific window:
         x_lo = min over t of ILR(t)[a]
         x_hi = max over t of ILR(t)[a]
         y_lo = min over t of ILR(t)[b]
         y_hi = max over t of ILR(t)[b]
    8. Build separate plot setup (axes, ticks, labels)
    9. Render scatter / trajectory line
```

This produces three independent figures with three independent
windows and three independent label setups. The bearings between
carriers shown on each axis-pair are the dot-product / arccos
quantities of §2.

### CNT internal procedure

```
1. Read closed composition x(t) for all t (one matmul over T):
     Closed[T, D] from j["tensor"]["timesteps"][*]["coda_standard"]["composition"]

2. Read pre-computed CLR matrix:
     CLR[T, D] from j["tensor"]["timesteps"][*]["coda_standard"]["clr"]
   (no zero-replacement step at viewing time — the engine already did it)

3. Read pre-computed Helmert basis from JSON:
     V[D-1, D] from j["tensor"]["helmert_basis"]["coefficients"]

4. ONE matmul:
     ILR[T, D-1] = (V @ CLR.T).T

5. Compute ONE shared window across the FIRST 3 ILR axes:
     window = (min, max) over CLR[:, 0:3]
     magnitude_factor F = pick_factor(window)   # for FIXED-SCALE display
   (axes 4..D-1 are not displayed at level 1; using only the visible
    ones prevents distant axes from stretching the FIXED scale)

6. Slice the same ILR matrix for each panel:
     XY = ILR[:, [0, 1]]
     XZ = ILR[:, [0, 2]]
     YZ = ILR[:, [1, 2]]

7. Render with the SAME window on all three panels (FIXED SCALE).
   Each panel is square (set_aspect("equal")).
   The window is annotated on every plate footer.
```

### Side-by-side comparison

| Item | Standard CoDa | CNT |
|---|---|---|
| Total matmuls per dataset | 3 × T (one per axis-pair × per timestep) | 1 (T × D-1 ILR matrix once) |
| Window calculations | 3 separate (one per axis-pair) | 1 shared, fixed across all panels |
| Magnitude rescaling | usually absent; axes auto-fit | automatic via `pick_magnitude_factor()` so values land in the comfort range [0.5, 50] |
| Determinism | depends on implementation | byte-identical when content_sha256 matches |
| Cross-timestep comparability | breaks: each plate's axis range differs | preserved: the window is the same on every plate, so a small movement of the trajectory dot is visually meaningful |
| Pages required | 3 figures or a 3-panel composition (typically separate windows) | 1 plate per timestep showing all three projections at the SAME fixed scale |

The CNT approach is not novel mathematics — it's the same Helmert
ILR projection. What's different is the **bookkeeping**: one matrix
computed once, three views as slices of that matrix, one shared
fixed-scale window across all three. The result is a plate book
where every page is comparable to every other page without mental
zoom adjustment.

This matters most when a reader is scrolling through T plates of a
trajectory and needs to perceive a small shift as a small visual
change. Independent auto-scales would make every plate look
similar; CNT's shared-window FIXED SCALE makes the trajectory's
scale of motion legible.

---

## §4  Boundary behaviour: zeros, near-poles, near-locks

This is the section where the choice of operator algebra matters
beyond performance. Real compositional data has zeros (carrier not
present at that timestep), near-zeros (carrier in phase-out), and
near-poles (carrier dominating > 60 %). All three are routine in
energy data, geochemistry, and finance.

### How standard CoDa handles boundary

* **Zeros**: `log(0) = −∞`. Standard CoDa applies an *additive*
  zero replacement: `x_j ← max(x_j, δ)` with δ chosen by the
  practitioner (typically 1e-6 or 1e-9). The choice of δ is
  arbitrary and **affects downstream results** including
  IR classification on near-degenerate datasets.
* **Near-poles**: a single carrier above ~60 % squeezes the other
  D-1 carriers into the simplex's edge region. CLR coordinates
  near a vertex have very large magnitudes; the Helmert ILR
  inherits this and the resulting ‖ILR(t)‖ can drift outside the
  comfort range of any plot.
* **Near-locks (pairs nearly parallel)**: as discussed in §2, the
  arccos formula has poor stability there.

### How CNT handles boundary

* **Zeros**: same δ-replacement at the engine boundary, but the
  value is a USER CONFIGURATION constant (`DEFAULT_DELTA` in
  cnt.py) and is echoed in `metadata.engine_config.DEFAULT_DELTA`
  in every output JSON. Different δ → different `content_sha256`,
  by design. The arbitrariness becomes auditable rather than
  implicit.
* **Near-poles**: the metric tensor M(x) is computed with full
  D × D structure; its dual M⁻¹ is the inverse, and the
  involution M² = I is *verified per timestep* with the residual
  recorded in `diagnostics.higgins_extensions.involution_proof`.
  Mean residuals near IEEE floor (~10⁻¹⁵) indicate the metric is
  numerically well-behaved even where the simplex is geometrically
  squeezed. Near-vertex degeneracies are flagged
  explicitly via the `D2_DEGENERATE` and `CURVATURE_VERTEX_FLAT`
  IR classes.
* **Near-locks**: the atan2-based bearing has stable slope near
  θ = 0; the `LOCK_CLR_THRESHOLD` constant determines when a pair
  is marked as locked, and the lock event is recorded in
  `diagnostics.higgins_extensions.lock_events`.

### What this buys

Standard CoDa workflows on near-boundary data are commonly
**δ-sensitive**: changing δ from 1e-6 to 1e-9 changes the dendrogram,
the biplot, and the IR class of a borderline dataset. The change
is implicit unless explicitly documented.

CNT workflows on the same data are **disclosed**: the value of δ
is in the JSON, in the report's data-disclosure plate, and in the
content hash. If two parties disagree on a result, they can
identify whether they used different δ values within seconds.

This isn't CNT being more "correct" mathematically — it's CNT
making an inevitable arbitrary choice into an audit-trace artefact.

---

## §5  Performance balance

Wall-clock and memory comparison on the canonical EMBER Japan run
(T = 26, D = 8, full Stage 1 + Stage 2 atlas, no caching):

| Metric | Standard-CoDa-style implementation (estimated) | CNT (measured) |
|---|---|---|
| Engine time per dataset | 100-200 ms (Python) | 121 ms (Python 2.0.4) |
| Atlas Stage 1 (T plates) | ~1.5-3 s typical | ~2.0 s (matplotlib) |
| Atlas Stage 2 (28 plates) | n/a (Stage 2 is CNT-specific) | ~2.3 s |
| Atlas Stage 3 (11 plates) | n/a (depth tower is CNT-specific) | ~1.9 s |
| Memory peak | ~30 MB | ~35 MB |
| Determinism (same input → same output bytes) | implementation-dependent | guaranteed by content_sha256 |

CNT is competitive on raw speed for this problem size and slightly
higher on memory because it caches the metric tensor and the
Helmert basis as part of the JSON output (so downstream viewers
need no recomputation).

The big performance win is on **scale**:

| Scenario | Standard CoDa | CNT |
|---|---|---|
| 1 dataset, single snapshot ternary | ~50 ms total | ~150 ms total (overkill) |
| 1 dataset, T = 26 trajectory | ~3-5 s atlas | ~2 s atlas |
| 25-experiment corpus | scattered scripts, no determinism gate | 21 s full corpus, gate passes 25/25 |
| 8-country Stage 4 cross-dataset | requires hand-stitched comparison | 11-page report in ~3 s via group module |
| Re-running on new engine version | re-run all atlases | content_sha256 tells you exactly what changed |

For T = 1, D = 3 work, classical CoDa is faster *and* simpler.
For T > 10 trajectories, multi-experiment projects, or
publication-grade reproducibility, CNT delivers strong returns.

---

## §6  When to prefer each

### Reach for classical CoDa when:

- You have a **single composition** to display (T = 1 or
  cross-section without temporal structure).
- D = 3 and a **ternary plot** is sufficient.
- The audience expects the **classical biplot or balance
  dendrogram** as the primary view (the v1.1.x Stage 2 atlas
  ships those plates anyway, computed via the CNT engine).
- The work is **exploratory** and reproducibility is not yet a
  constraint.

### Reach for CNT when:

- You have a **trajectory** (T > 5) and need bearings, ω,
  helmsman, ring-class structure, period-2 attractor.
- D > 5 and the classical biplot starts to clutter (the
  `p_biplot_topN` plate is the bridge).
- You need **cross-dataset comparison** in one common frame
  (Stage 4 group reports).
- You need **audit-grade reproducibility** with hash-chained
  outputs from raw CSV through final PDF.
- The data has **boundary issues** (zeros, near-poles, near-locks)
  and you need an explicit disclosure of the δ-choice and the
  metric-residual.
- You are doing **publication or partner-lab work** where the
  determinism gate matters.

### Reach for both when:

- The audience is mixed (classical CoDa reviewers + dynamical-
  systems reviewers). The v1.1.x Stage 2 atlas is exactly this:
  geometry plates (proportions, ternaries, variation, biplot,
  scree, dendrogram, SBP) sitting next to dynamics plates
  (bearings, ω, helmsman, ring, locks, course plot, CBS,
  divergence ranking). Both languages, one report.

---

## §7  Honest costs of choosing CNT

CNT is not free. The trade-offs that come with the framework:

1. **Conceptual overhead.** The metric tensor, the dual involution,
   the depth tower, the IR taxonomy — these require time to
   internalise. A new operator coming from a classical CoDa
   background needs ~1 day with the math handbook before the
   plates make sense.

2. **More moving parts to audit.** A CNT JSON is bigger than a
   raw CoDa export — every analytic block is split into
   `coda_standard` and `higgins_extensions` halves. The schema
   2.1.0 document is 10 sections. The doctrine v1.0.1 specifies
   integer-orders-only, round-up rules. All of this is
   documented and hash-stamped, but it's still more surface area.

3. **Implementation complexity.** The engine is ~1700 lines of
   Python (parity-tested R port). The atlas modules total
   another ~6000 lines. A classical CoDa workflow can sit in
   ~200 lines of NumPy + matplotlib. CNT is a system, not a
   script.

4. **Higher disk usage per run.** The canonical JSON output
   carries every per-timestep CLR / ILR / bearing / lock event.
   For T = 26, D = 8 this is ~600 KB. For the geochem datasets
   with T ~ 1000, D ~ 12 it can reach ~50 MB. Classical CoDa
   normally caches very little of this.

5. **Pinning matplotlib for byte-identical PDFs.** The
   deterministic-PDF backend (Feature A) requires a pinned
   matplotlib version for full byte-identity. The JSON
   `content_sha256` is byte-identical without pinning; the
   PDF needs the pin.

These costs are real. They're justified when the work depends on
trajectory dynamics, cross-dataset comparison, or
publication-grade determinism. They're overkill for a one-off
ternary chart.

---

## §8  Conclusion — preferred *when*, not preferred *always*

CNT extends the classical CoDa framework with three things that
the original toolkit does not provide as first-class objects:

1. **Trajectory-native operators** — bearings, ω, helmsman, ring
   class, period-2 attractor, IR taxonomy. These need to exist
   in the operator algebra, not be added on as post-hoc plots.

2. **End-to-end determinism** — content_sha256 chains raw CSV →
   JSON → PDF, and the engine signature on every page traces
   back to the source code that produced it. Standard CoDa
   workflows are typically a stack of independent scripts where
   reproducibility relies on operator discipline.

3. **Cross-dataset structural comparison** — Stage 4 reports
   compare attractor amplitudes, depth-tower convergence, and
   IR-class distribution across multiple datasets in one
   document. Classical CoDa methods compare datasets pair-wise
   and don't have a unified Order-4 framework.

Where these three capabilities matter, CNT is the preferred
method. Where they don't, classical CoDa methods are simpler,
faster, and well-understood — and CNT happily ships those
plates inside Stage 2 anyway, computed from the same JSON.

The honest summary: CNT is a tensor-decomposition extension of
the Aitchison-Egozcue framework, useful for trajectory and
cross-dataset work, with explicit costs in conceptual overhead
and implementation complexity. It is a complement to classical CoDa,
not a replacement built for problems classical
CoDa was not designed for.

---

## Appendix A — The atan2 expression in cnt.py

```python
def angular_velocity_deg(h_prev: list[float], h: list[float]) -> float:
    """Angular velocity between two CLR vectors in degrees.
    Uses atan2 for stable quadrant resolution."""
    # ... (cnt/cnt.py §0.angular_velocity_deg)
```

The full implementation, with sign conventions and the lock-event
hookup, lives at `cnt/cnt.py`. Its test harness is at
`cnt/tests/test_determinism.py` and the calibration fixture at
`atlas/STANDARD_CALIBRATION_27pt_*` shows engine residuals near
IEEE floor on the 27-point HLR-grid ground truth.

## Appendix B — Reproducibility envelope

| Object | What's hashed | How to verify |
|---|---|---|
| Source CSV | `inp.source_file_sha256` | `sha256sum input.csv` |
| Closed data | `inp.closed_data_sha256` | engine recomputation |
| Canonical JSON | `diagnostics.content_sha256` | engine deterministic; same input + same config → same SHA |
| Engine source | `metadata.engine_config.engine_signature` | sha256(cnt.py + atlas/stage2_locked.py) |
| PDF | matplotlib metadata + content | byte-identical with pinned matplotlib |

Same input + same engine config + same engine source → byte-identical output bytes top to bottom.
That's the contract.

---

*The instrument reads. The expert decides. The loop stays open.*
