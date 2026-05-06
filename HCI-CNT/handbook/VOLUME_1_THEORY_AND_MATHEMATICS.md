# Volume I — Theory and Mathematics

**HUF-CNT System v1.1.x**
**The mathematics handbook**

This volume is the canonical reference for the mathematical content
of the HUF-CNT system. It walks the reader from the foundations of
compositional-data analysis (Aitchison, Egozcue, Pawlowsky-Glahn)
through the additions the Compositional Navigation Tensor (CNT)
brings on top of that toolkit, the schema that records the result,
the doctrine that classifies every output by its derivational order,
and the side-by-side comparison that shows how the two algebras
relate.

The companion volumes are:

* **Volume II — Practitioner and Operations** — how to run the
  system, the modules that produce the reports, the experiments
  corpus, the conference demo package, the use-case decision
  framework, and the operations checklists.
* **Volume III — Verification, Reference and Release** — the
  determinism contract, the hash-chain verification value to the
  CoDa community, the talk-prep brief, the public-trial readiness
  audit, and the release record.

Together these three volumes replace the previous ad-hoc
documentation tree. They preserve the canonical wording from every
source document; only the discovery-path scaffolding (intermediate
proposals, planning notes, transitional READMEs) has been folded
into a coherent narrative.

---

# Part A — Foundations: Why compositional data is special

The HUF-CNT System is the reference implementation of the Compositional
Navigation Tensor for analysing data that lives on a simplex —
proportions, percentages, parts-of-a-whole, allocations, and any
multi-component composition that has been closed to a unit sum.
Compositional data analysis (CoDa) has a mature mathematical foundation
(Aitchison 1986, Egozcue 2003, Pawlowsky-Glahn and Egozcue 2015), but
the practical workflow has historically been bespoke: each project
assembles its own chain of scripts, its own conventions for closure
and zero replacement, its own choices for visualisation. Reproducing
a published result from someone else's compositional study is harder
than it ought to be.

This package addresses that gap. It is built around three commitments
which reappear throughout the handbook.

The schema is the contract. There is one canonical JSON format
(version 2.0.0) into which the engine writes every analytical result.
Any conforming JSON can be read by any conforming viewer; the engine
and the viewers depend on the schema, not on each other. New tools
that respect the schema slot in without modifying anything else.

The engine is deterministic. Same input plus same configuration
yields the same `content_sha256` byte for byte. Every constant the
engine uses lives in a USER CONFIGURATION block at the top of
`cnt/cnt.py` (and its R port in `cnt/cnt.R`). Every active value is
echoed into `metadata.engine_config` of every JSON the engine writes.
A run that produces a different SHA from a published reference is
either using a different input, a different config, or a different
engine version — those three possibilities are the only ones, and the
JSON's metadata block tells you which.

The pre-parsers are fully disclosed. Every adapter that converts raw
third-party data into an ingestible CSV is open Python in `adapters/`
with a top-level docstring describing source format, transformation
rule, what is preserved, what is discarded, and why. Section 7 of
this handbook is a unified disclosure document covering every adapter
used to produce the twenty reference experiments. Together with the
schema and the determinism contract, the disclosure forms the full
trust surface.

## Who this is for

Researchers who already work with compositional data. The handbook
assumes you are comfortable with the simplex, the closure operator,
log-ratio transforms, and the basic geometry summarised in section 2.
If you are coming from outside CoDa, Aitchison's 1986 monograph and
the Pawlowsky-Glahn / Egozcue 2015 textbook are the canonical
references; this handbook does not duplicate them.

The package is also useful for practitioners in adjacent fields
where compositional structure shows up empirically — energy mix,
sector allocation in finance, geochemistry, ecology, demographic
proportions, hardware-sensor distributions, climate-zone partitions.
The twenty reference experiments include real third-party data from
EMBER electricity generation, EarthChem geochemistry, FAO irrigation,
BackBlaze hard-drive fleet, and AME2020 nuclear binding energies.
None of them are toy datasets.

## How to read this handbook

Section 2 surveys the CoDa basics the rest of the handbook depends on.
Section 3 describes the engine — the program that transforms a
compositional CSV into the canonical JSON. Section 4 documents the
schema; sections 5 and 6 cover the atlas viewer and the mission
command orchestrator. Section 7 is the pre-parser disclosure. Section
8 is the experiment walkthrough. Section 9 is the determinism
contract. Section 10 is the glossary.

If your question is "should I trust this for a published paper?",
read sections 7 and 9 first. If your question is "how do I run this on
my own data?", read sections 3 and 4 and the quickstart in
`examples/01_quickstart.py`. If your question is "what does the
output look like?", open any reference atlas in `atlas/runs/` after
running mission command, or look at the sample atlas pages in
`atlas/SAMPLE_*.pdf`.

The HTML mirror at `handbook/docs_html/index.html` is the same
content; use whichever surface fits your reading.

## What this handbook is not

It is not a CoDa textbook. The mathematics is summarised where
needed but not derived; for proofs and theorems, see the references
in section 2. It is not an API reference for an arbitrary library —
the package is small enough that the source is the most accurate API
documentation, and `pyproject.toml` already declares the public
entry points. It is not a tutorial for general data wrangling — every
adapter shipped with the package is a worked example, but the
handbook does not teach Python or R.

What it is: a complete description of what the system computes, how
to verify the result reproduces, and how to extend the system to new
data of your own.

---

*The instrument reads. The expert decides. The loop stays open.*



---

# Part B — Compositional-data foundations (Aitchison, Egozcue, Pawlowsky-Glahn)


This section summarises the parts of compositional data analysis that
the rest of the handbook assumes. Everything here is standard CoDa
material; see Aitchison (1986), Egozcue et al. (2003), and
Pawlowsky-Glahn and Egozcue (2015) for the proofs.

## The simplex

A composition of D parts is a vector x = (x_1, ..., x_D) of non-negative
real numbers carrying only relative information. The values are
defined up to a positive scale: 0.30 / 0.20 / 0.50 contains the same
compositional information as 30 / 20 / 50 or 6 / 4 / 10. To work with
a unique representative, compositions are closed to a constant total
(canonically 1) by

    C(x) = (x_1 / Σx, x_2 / Σx, ..., x_D / Σx).

The image of this closure is the standard (D-1)-simplex S^(D-1), the
set of D-tuples of non-negative reals that sum to 1. Every point on
S^(D-1) is a valid composition.

## What "compositional" means

The defining property is that **only ratios between parts carry
information**. Adding a constant to every part does not change the
composition; multiplying every part by the same positive scalar does
not change it either. A statistical method that fails to respect
this — for example, computing the arithmetic mean of compositions
component-by-component — is producing artefacts. Compositional
methods are designed to respect the simplex's geometry rather than
fight it.

## The Aitchison geometry

The simplex carries a natural inner-product geometry — the Aitchison
geometry — under which it becomes a (D-1)-dimensional Euclidean
space. The geometry is built on three operations.

**Perturbation** is the simplex's addition:

    x ⊕ y = C(x_1·y_1, x_2·y_2, ..., x_D·y_D).

**Powering** is its scalar multiplication:

    α ⊙ x = C(x_1^α, x_2^α, ..., x_D^α).

**Aitchison distance** is its metric:

    d_A(x, y) = sqrt( (1/D) · Σ_{i<j} ( ln(x_i/x_j) - ln(y_i/y_j) )² ).

These operations make S^(D-1) a (D-1)-dimensional real Hilbert space.
The CNT engine does all of its arithmetic in this geometry; it never
treats compositions as raw vectors in R^D.

## CLR and ILR transforms

Two log-ratio transforms move data between the simplex and Euclidean
space.

The **centred log-ratio (CLR)** of x is

    clr(x)_j = ln( x_j / g(x) )      where  g(x) = (∏ x_k)^(1/D).

CLR is one-to-one between S^(D-1) and the linear subspace of R^D
where coordinates sum to zero. It is the natural surface on which
log-ratio variances and Aitchison distances are computed.

The **isometric log-ratio (ILR)** transform sends compositions to
R^(D-1) using an orthonormal basis of the CLR subspace. Egozcue's
Helmert basis is the canonical choice: it produces independent
contrast coordinates in which Euclidean operations have a
compositional meaning.

The CNT engine uses the Helmert basis to compute angles, velocities,
and curvatures of the trajectory. It uses CLR coordinates for
log-ratio variance, lock detection, and the duality test
M(M(x)) = x.

## Closure and zero replacement

Real compositional data routinely contains zeros — counts that didn't
land in some bin, percentages that round below the reporting
threshold, measurements below detection limit. Log-ratio methods
require strictly positive values, so a zero must be replaced before
analysis. The most defensible replacement is the multiplicative
imputation of Martín-Fernández et al. (2003): replace each zero with
a small positive value δ such that the relative magnitudes of the
non-zero parts are preserved by a proportional rescaling.

The CNT engine applies this replacement automatically with δ =
DEFAULT_DELTA (1e-15 by default; user-configurable). Every
replacement is recorded in `input.zero_replacement` in the JSON,
including the count of replaced cells and the final-row check that
each row remains a valid simplex point.

## Subcompositional coherence

A subcomposition is what you get when you select some of the parts
and re-close the remainder. Compositional methods must produce
results that are coherent under subcomposition: the Aitchison
distance between two compositions, restricted to a subcomposition,
must be the Aitchison distance between the subcompositions
themselves. CLR and ILR satisfy this. Raw subset-then-percent
calculations do not.

This matters for the depth tower (section 3.4): the recursion
descends into subcompositions, and the arithmetic must remain
coherent for the per-level helmsman to be meaningful.

## What CoDa adds beyond ordinary statistics

Three things, briefly. First, the geometry is curved relative to
naive R^D — the simplex is a manifold, not a flat region — and
proper analysis must use the manifold's intrinsic operations.
Second, log-ratios capture multiplicative relationships that
percentage-point arithmetic destroys. Third, the closure constraint
introduces a degenerate covariance structure (every covariance
matrix has rank D−1, not D); ignoring this produces spurious
correlations.

## What the CNT engine adds on top of CoDa

The Compositional Navigation Tensor extends CoDa with a navigational
reading of compositional trajectories. For an ordered sequence of
compositions x_1, x_2, ..., x_T (a time series, or a labelled
cross-section with any meaningful ordering), it computes per-step:

* **Bearing θ** — the direction of motion in the Aitchison geometry,
* **Angular velocity ω** — the per-step bearing change,
* **Steering metric κ** — the local curvature of the trajectory,
* **Helmsman σ** — the carrier whose log-ratio is doing the steering,
* **Higgins scale H_s** — a normalised entropy on [0, 1].

The recursive depth sounder then iterates on the trajectory's energy
and curvature towers, exposing the system's period-2 attractor (when
present) and reporting an Information-Recovery (IR) class describing
how the simplex absorbs perturbations.

## References

* Aitchison, J. (1986). *The Statistical Analysis of Compositional Data.* Chapman and Hall.
* Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G., & Barceló-Vidal, C. (2003). "Isometric logratio transformations for compositional data analysis." *Mathematical Geology*, 35(3), 279-300.
* Pawlowsky-Glahn, V., & Egozcue, J. J. (2015). *Modeling and Analysis of Compositional Data.* Wiley.
* Martín-Fernández, J. A., Barceló-Vidal, C., & Pawlowsky-Glahn, V. (2003). "Dealing with zeros and missing values in compositional data sets using nonparametric imputation." *Mathematical Geology*, 35(3), 253-278.
* Higgins, P. (2026). "The Compositional Navigation Tensor." Forthcoming.

---

*Onwards to section 3 — the engine.*



---

# Part C — The CNT Engine: tensor decomposition over the simplex


The CNT engine is a single program that ingests a compositional CSV
and produces one canonical JSON. The Python reference implementation
is `cnt/cnt.py` (engine 2.0.3); the R port is `cnt/cnt.R` (engine
2.0.3). Both implementations write the same schema 2.0.0 JSON layout
and the same numerical results to within IEEE floor.

## Inputs

The input CSV format is minimal: the first column is a label (year,
country, location, sample id — anything string-typed that uniquely
identifies the row), and the remaining columns are numerical carriers
that sum to a meaningful total per row. The header row names the
carriers; the body has one row per record.

The engine reads the file, applies the multiplicative zero-replacement
floor (δ = DEFAULT_DELTA, default 1e-15) to any non-positive values,
and closes each row to the simplex. The closed values, the source
SHA-256, and the closed-data SHA-256 are recorded in `input.*` of the
JSON.

## USER CONFIGURATION block

Every constant the engine uses lives in a USER CONFIGURATION block at
the top of `cnt.py` and `cnt.R`. The block is grouped by category:

```python
# === VERSION ===
SCHEMA_VERSION         = "2.0.0"
ENGINE_VERSION         = "2.0.3"

# === ZERO REPLACEMENT ===
DEFAULT_DELTA          = 1e-15
DEGEN_THRESHOLD        = 1e-4

# === LOCK EVENT THRESHOLDS ===
LOCK_CLR_THRESHOLD     = -10.0

# === DEPTH RECURSION ===
DEPTH_MAX_LEVELS       = 50
DEPTH_PRECISION_TARGET = 0.01
NOISE_FLOOR_OMEGA_VAR  = 1e-6

# === TRIADIC ENUMERATION ===
TRIADIC_T_LIMIT        = 500
TRIADIC_K_DEFAULT      = 500

# === EITT BENCH-TEST ===
EITT_GATE_PCT          = 5.0
EITT_M_SWEEP_BASE      = [2, 4, 8, 16, 32, 64, 128]
```

Edit the block to change behaviour; the active values are echoed
verbatim into `metadata.engine_config` of every JSON the engine writes.
A run reproducing a published `content_sha256` requires the same
config block as the published run; a different config produces a
different SHA. Both are explicit, both are recorded.

## Stages

The engine processes the trajectory in four stages.

**Stage 0 — closure and metric.** Each row is replaced with its
closed form C(x). The Aitchison metric tensor and its dual involution
M(M(x)) = x are computed for each timestep. The CLR coordinates are
recorded; the Helmert basis is constructed once for the whole
trajectory.

**Stage 1 — tensor block.** For each timestep, the engine computes:

* the bearing pairs (θ_ij for every carrier pair),
* the angular velocity ω in degrees,
* the steering metric κ (off-diagonal entries of the inverse metric),
* the helmsman σ — the carrier whose log-ratio drives the largest
  contribution to the directional change,
* the Higgins scale H_s ∈ [0, 1] — a normalised compositional entropy.

The tensor block is the foundation; everything downstream reads from
it.

**Stage 2 — bridges.** The CoDa-standard outputs (variation matrix,
information-theoretic quantities, fisher information) live here under
the `coda_standard/` sub-block. The Higgins-extension outputs
(per-carrier Lyapunov exponents, velocity field, recurrence analysis,
state-space observability) live under `higgins_extensions/`.

**Stage 3 — depth tower.** The recursive depth sounder iterates on
both the energy and curvature towers. At each level k, the engine
computes the level-k subcompositional barycenter, derives a new
T-record trajectory from the residuals against that barycenter, and
recurses. The recursion stops when:

* the trajectory degenerates to fewer than 5 records (SIGNAL_SHORT),
* a period-1 fixed point is detected (PERIOD_1_FIXED),
* a period-2 limit cycle is detected (LIMIT_CYCLE_P2),
* a vertex is reached (HS_FLAT),
* the precision target is met (CONVERGED), or
* DEPTH_MAX_LEVELS is exhausted (MAX_DEPTH).

The summary block records the depth, the termination reason, and the
helmsman lineage at each level.

## IR classification

The Information-Recovery (IR) class summarises the system's response.
Eight classes:

| Class | Meaning |
|---|---|
| CRITICALLY_DAMPED  | Tight period-2 attractor, A < 0.1 |
| LIGHTLY_DAMPED     | Period-2 attractor, ζ small, A in [0.1, 0.5) |
| MODERATELY_DAMPED  | Period-2 attractor, A in [0.5, 0.7) |
| OVERDAMPED_EXTREME | Period-2 attractor, A ≥ 0.7 |
| UNDAMPED           | Period-2 attractor, ζ ≈ 0 (rare) |
| ENERGY_STABLE_FIXED_POINT | Period-1 stable fixed point on energy tower |
| CURVATURE_VERTEX_FLAT     | Curvature recursion driven to a vertex by single-carrier dominance > 60% |
| D2_DEGENERATE      | D = 2 — one independent compositional axis only |

The class is reported in `depth.higgins_extensions.impulse_response.classification`.

## Outputs

A single JSON file per CSV input. The default name pattern is
`<input_stem>_cnt.json`, written next to the input. The JSON is
schema 2.0.0 (see section 4) with these top-level blocks:

* `metadata` — engine version, schema version, run-time provenance
* `input` — closed data, source/closed SHAs, ordering, zero replacement
* `tensor` — Helmert basis + per-timestep tensor block
* `stages` — Stage 1, 2, 3 outputs split into coda_standard / higgins_extensions
* `bridges` — Stage 2 cross-blocks
* `depth` — energy tower, curvature tower, attractor, IR classification
* `diagnostics` — EITT bench-test, lock events, degeneracy flags, content_sha256

The `content_sha256` is the SHA-256 of the canonical-form JSON
contents (everything except the timestamp itself). It is the reference
for the determinism contract.

## Performance characteristics

On a stock laptop (2024 hardware, single thread):

| Dataset | T | D | Wall clock |
|---|---|---|---|
| EMBER Japan         |  26 | 8  |   ~100 ms |
| Ball geochem region |  95 | 10 | ~1500 ms |
| BackBlaze fleet     | 731 | 4  | ~1500 ms |
| EMBER combined panel| 207 | 9  |  ~12 sec |

The dominant cost above T ≈ 200 is the triadic enumeration in Stage 3
— C(T, 3) day-triads. The default `TRIADIC_T_LIMIT = 500` skips full
enumeration for T > 500 and uses a deterministic random subset of
`TRIADIC_K_DEFAULT = 500` triads instead.

## CLI

```bash
# basic run
python cnt/cnt.py path/to/data.csv -o path/to/data_cnt.json --temporal --ordering-method by-time

# cross-section
python cnt/cnt.py path/to/data.csv --ordering-method by-label
```

Or programmatically:

```python
import sys
sys.path.insert(0, "cnt")
import cnt as cnt_engine

ordering = {"is_temporal": True, "ordering_method": "by-time", "caveat": None}
cnt_engine.cnt_run("data.csv", "data_cnt.json", ordering)
```

## R port

`cnt.R` mirrors the Python implementation at engine 2.0.3 with a
small set of base-R-only dependencies (`jsonlite`, `digest`). Use it
when an R workflow is more natural; the JSON output is identical to
within IEEE floor on Python and R for every reference experiment.

## What the engine does NOT do

It does not visualise. The atlas (section 5) handles that.
It does not orchestrate. Mission Command (section 6) handles that.
It does not adapt raw third-party data. Adapters (section 7) handle that.
It does not interpret. Conclusions are the user's domain expertise;
the engine reports.

The engine reads. The expert decides. The loop stays open.



---

# Part D — Engine pseudocode (language-neutral reference)


**Schema version:** 2.0.0
**Engine version:** 2.0.3 (current reference; cnt.R port at 2.0.2)
**Status:** Language-neutral algorithm reference. Reproducible in any
language with basic arithmetic (no special libraries required).

This document is the algorithm. The Python (`cnt.py`) and R (`cnt.R`)
implementations are reference instances; this is the contract they
implement. Anyone reading this can re-implement the engine in any
language.

## Engine fix log (within v2.0.x)

| Engine | Fix |
|---|---|
| 2.0.0 | Initial schema-2 layout (coda_standard / higgins_extensions split) |
| 2.0.1 | Period-1 detection now requires TWO consecutive level-pair convergences (was 1) — fixed false positives on USA EMBER and Ball/TAS where coincidental L_k ≈ L_{k-1} stopped the recursion prematurely. See §6.3 below. |
| 2.0.1 | Curvature composition uses 1/x_j² (the κ_jj diagonal), not 1/x_j. See §4.5 below. |
| 2.0.1 | TRIADIC_T_LIMIT default lowered 1000 → 500. |
| 2.0.2 | USER CONFIGURATION block at top of source file with documented constants, echoed in `metadata.engine_config` of every JSON output. |
| 2.0.3 | IR taxonomy refinement (Python `cnt.py` only): the legacy `DEGENERATE` class split into three more-informative classes: `ENERGY_STABLE_FIXED_POINT` (energy depth ≥ DEPTH_MAX_LEVELS with stable amplitude), `CURVATURE_VERTEX_FLAT` (curvature recursion driven to a vertex by a single dominant carrier), `D2_DEGENERATE` (genuine D=2 limitation; a single independent compositional axis). The R port at 2.0.2 retains the single `DEGENERATE` class. |

---

## Inputs

```
csv_path     : path to CSV file with first column = label, rest = D carriers
output_path  : path to write the JSON
ordering     : { is_temporal: bool, ordering_method: str, caveat: str|null }
                — required, declared by the user

eitt_M_sweep : list of compression ratios to bench-test (default: depend on T)
include_full_distance_matrix : bool (default: T <= 200)
```

---

## High-Level Flow

```
function CNT(csv_path, output_path, ordering):
    record_input_metadata(csv_path)              # source hash, file size, etc.
    records = ingest_csv(csv_path)               # close to simplex, replace zeros
    record_data_metadata(records, ordering)

    tensor_block = compute_tensor(records)        # §1
    stages_block = compute_stages(records, tensor_block)  # §2
    bridges_block = compute_bridges(records, tensor_block) # §3
    depth_block = compute_depth(records, tensor_block)     # §4
    diagnostics_block = compute_diagnostics(records, tensor_block, depth_block) # §5

    json = {
        metadata,
        input,
        tensor: tensor_block,
        stages: stages_block,
        bridges: bridges_block,
        depth: depth_block,
        diagnostics: diagnostics_block,
    }
    json.diagnostics.content_sha256 = sha256_of_normalized(json)
    write_json(json, output_path)
```

---

## §0 — Conventions

### Closure

```
function close(x):
    s = sum(x)
    return [v / s for v in x]
```

### CLR transform

```
function clr(x):
    D = length(x)
    log_x = [ln(v) for v in x]      # x must be all > 0
    mean_log = sum(log_x) / D
    return [lx - mean_log for lx in log_x]
```

### Helmert orthonormal basis

```
function helmert_basis(D):
    basis = []
    for k in 1 to D-1:
        row = [0] * D
        scale = sqrt(k / (k + 1))
        for j in 1 to k:
            row[j-1] = 1 / k
        row[k] = -1
        # normalize: each row scaled by sqrt(k / (k+1))
        for j in 1 to k+1:
            row[j-1] = row[j-1] * scale
        basis.append(row)
    return basis    # (D-1) x D matrix
```

### ILR projection

```
function ilr(h, basis):
    # h is the CLR vector (length D); basis is (D-1) x D
    return [dot(basis[k], h) for k in 0 to D-2]
```

### Aitchison distance

```
function aitchison_distance(x, y):
    return norm(clr(x) - clr(y))     # Euclidean norm of CLR difference
```

### Aitchison barycenter (geometric-mean of N closed compositions)

```
function aitchison_barycenter(rows):
    D = length(rows[0])
    log_means = []
    for j in 0 to D-1:
        s = sum(ln(r[j]) for r in rows)
        log_means.append(s / length(rows))
    g = [exp(lm) for lm in log_means]
    return close(g)
```

### Shannon entropy (NOT scale-invariant — empirical use only)

```
function shannon_entropy(x):
    return - sum(v * ln(v) for v in x if v > 0)
```

### Higgins scale (HUF-specific; range [0, 1])

```
function higgins_scale(x):
    H = shannon_entropy(x)
    return 1 - H / ln(D)
```

### Metric dual involution

```
function M(x):
    return close([1 / v for v in x])
```

Theorem (verified to IEEE 754 floor): `M(M(x)) = x` for all x in the
open simplex. In CLR space, `clr(M(x)) = -clr(x)`. The fixed point is
the barycenter (1/D, ..., 1/D). See Math Handbook Ch 18.

### Higgins steering metric tensor (full D x D matrix)

```
function metric_tensor(x):
    D = length(x)
    K = D x D zero matrix
    for i in 0 to D-1:
        for j in 0 to D-1:
            if i == j:
                K[i][j] = (1 - 1/D) / (x[i] * x[i])
            else:
                K[i][j] = -1 / (D * x[i] * x[j])
    return K
```

### Bearing tensor (all D(D-1)/2 pairwise CLR-plane angles)

```
function bearing_tensor(h):
    D = length(h)
    pairs = []
    for i in 0 to D-2:
        for j in i+1 to D-1:
            theta = atan2(h[j], h[i])    # signed angle in [-pi, pi]
            pairs.append((i, j, theta_in_degrees))
    return pairs
```

### Angular velocity (Lagrange identity, atan2-stable)

```
function angular_velocity(h_prev, h):
    # |a x b|^2 = |a|^2 |b|^2 - <a,b>^2
    cross_sq = norm_sq(h_prev) * norm_sq(h) - dot(h_prev, h) ** 2
    if cross_sq < 0: cross_sq = 0
    cross_mag = sqrt(cross_sq)
    omega = atan2(cross_mag, dot(h_prev, h))
    return omega_in_degrees
```

### Helmsman (DCDI)

```
function helmsman(h_prev, h, carrier_names):
    deltas = [|h[j] - h_prev[j]| for j in 0 to D-1]
    j_max = argmax(deltas)
    return (carrier_names[j_max], deltas[j_max])
```

---

## §1 — `tensor` block

```
function compute_tensor(records):
    basis = helmert_basis(records.D)
    timesteps = []
    h_prev = null
    for i, rec in enumerate(records):
        x = close(rec.values)
        h = clr(x)
        ts = {
            index:                i,
            label:                rec.label,
            raw_values:           rec.values,
            composition:          x,
            clr:                  h,
            ilr:                  ilr(h, basis),
            shannon_entropy:      shannon_entropy(x),
            higgins_scale:        1 - shannon_entropy(x) / ln(D),
            aitchison_norm:       norm(h),
            bearing_tensor:       bearing_tensor(h),
            metric_tensor:        metric_tensor(x),
            metric_tensor_diagonal: [1/v for v in x],
            condition_number:     max(x) / min(x),
        }
        if h_prev is not null:
            ts.angular_velocity_deg     = angular_velocity(h_prev, h)
            ts.aitchison_distance_step  = norm(h - h_prev)
            ts.helmsman, ts.helmsman_delta = helmsman(h_prev, h, records.carriers)
        timesteps.append(ts)
        h_prev = h
    return { helmert_basis: basis, timesteps: timesteps }
```

---

## §2 — `stages` block

### Stage 1 — section atlas + metric ledger

```
function stage1(records, tensor):
    section_atlas = []
    metric_ledger = []
    for ts in tensor.timesteps:
        # Cube faces: XY = (clr_1, clr_2), XZ = (clr_1, clr_3), YZ = (clr_2, clr_3)
        # plus higher-order projections via PCA on the full D-vector
        section_atlas.append({
            index: ts.index,
            label: ts.label,
            xy_face: ts.clr[0:2],
            xz_face: [ts.clr[0], ts.clr[2]],
            yz_face: ts.clr[1:3],
            metric_tensor_trace: trace(ts.metric_tensor.matrix),
            condition_number: ts.condition_number,
            angular_velocity_deg: ts.angular_velocity_deg or 0,
        })
        metric_ledger.append({
            index: ts.index,
            label: ts.label,
            hs: ts.higgins_scale,
            ring: ring_classify(ts.higgins_scale),
            omega_deg: ts.angular_velocity_deg or 0,
            helmsman: ts.helmsman or "",
            energy: ts.aitchison_norm ** 2,
            condition: ts.condition_number,
        })
    return { section_atlas, metric_ledger }
```

### Stage 2 — variation matrix + carrier-pair examination

```
function stage2(records, tensor):
    D = records.D
    # CoDa-standard variation matrix tau_ij = var(ln(x_i / x_j))
    variation_matrix = D x D zero matrix
    for i in 0 to D-1:
        for j in 0 to D-1:
            if i != j:
                ratios = [ln(rec.composition[i] / rec.composition[j]) for rec in records]
                variation_matrix[i][j] = variance(ratios)

    # Pairwise behaviour
    carrier_pairs = []
    for (i, j) in combinations(0..D-1, 2):
        h_i_series = [ts.clr[i] for ts in tensor.timesteps]
        h_j_series = [ts.clr[j] for ts in tensor.timesteps]
        carrier_pairs.append({
            carrier_a: records.carriers[i],
            carrier_b: records.carriers[j],
            pearson_r: pearson_correlation(h_i_series, h_j_series),
            co_movement_score: ...,
            opposition_score: ...,
            locked: variance(bearings_ij_over_time) < lock_epsilon,
        })

    return { variation_matrix, carrier_pair_examination: carrier_pairs }
```

### Stage 3 — higher-degree (subcompositions, regimes, triadic if T small)

```
function stage3(records, tensor):
    D = records.D
    T = records.T

    # Subcompositional ladder — all k-subsets for k = 2 .. D-1
    ladder = []
    for k in 2 to D-1:
        subsets = combinations(carriers, k)
        # for each, compute mean correlation among its parts
        ladder.append({ degree: k, n_subsets: len(subsets), ... })

    # Carrier triads
    carrier_triads = []
    for (i, j, k) in combinations(0..D-1, 3):
        carrier_triads.append({ carriers, mean_correlation, mean_area })

    # Triadic day-area analysis — capped to avoid C(T, 3) explosion
    triadic = { n_candidates: C(T, 3) }
    if T > 1000:
        triadic.selection_method = "none_T_too_large"
        triadic.results = []
    else:
        all_triads = combinations(0..T-1, 3)
        # compute area for each via Heron in CLR space
        results = []
        for (a, b, c) in all_triads:
            ba = tensor.timesteps[a].clr
            bb = tensor.timesteps[b].clr
            bc = tensor.timesteps[c].clr
            sides = [norm(ba-bb), norm(bb-bc), norm(bc-ba)]
            s = sum(sides) / 2
            area = sqrt(max(0, s * (s - sides[0]) * (s - sides[1]) * (s - sides[2])))
            results.append({ triad: (a,b,c), sides, area })
        results.sort(by area, descending)
        triadic.selection_method = "top_K_by_area"
        triadic.selection_K = 500
        triadic.n_returned = min(500, len(results))
        triadic.results = results[0:500]

    # Regime detection — find boundaries where Aitchison distance step exceeds threshold
    regimes = ...

    return { triadic_area: triadic, carrier_triads, subcomposition_ladder: ladder, regime_detection: regimes }
```

---

## §3 — `bridges` block

### Per-carrier Lyapunov exponents

```
function per_carrier_lyapunov(records, tensor):
    # Approximate sensitivity along each carrier axis from the CLR series
    exponents = []
    for j in 0 to D-1:
        h_j_series = [ts.clr[j] for ts in tensor.timesteps]
        # Lyapunov via mean log-divergence rate of nearby trajectories
        lyap = estimate_lyapunov_1d(h_j_series)
        exponents.append({
            carrier: records.carriers[j],
            lyapunov_exponent: lyap,
            classification: classify_lyapunov(lyap),
        })
    return exponents
```

### State-space + observability

```
function control_theory(records, tensor):
    # Fit linear model x(t+1) = A x(t) + B u(t)
    # via least squares on CLR series
    A, residual = ls_fit_AR1(tensor)
    state_space = {
        A_matrix: A,
        controllability_rank: rank(controllability_matrix(A, B)),
        observability_rank: rank(observability_matrix(A, C)),
        spectral_radius: max(|eigenvalues(A)|),
        stable: spectral_radius < 1,
        mean_residual: residual,
    }

    observability = []
    for j in 0 to D-1:
        observability.append({
            carrier: records.carriers[j],
            clr_variance: var([ts.clr[j] for ts in tensor.timesteps]),
            observability_score: ...,
        })
    return { state_space_model: state_space, observability }
```

### Information theory bridge

```
function information_theory(records, tensor):
    entropy_series = [{ label, shannon_entropy, normalised_entropy: H/ln(D), higgins_scale: 1 - H/ln(D) } for ts in tensor.timesteps]
    fisher = mean_fisher_information(records)
    kl = adjacent_pair_kl_divergence(records)
    mi = highest_mutual_information_pair(records)
    rate = entropy_rate(entropy_series)
    return { entropy_series, fisher_information: fisher, kl_divergence: kl, mutual_information: mi, entropy_rate: rate }
```

---

## §4 — `depth` block

The recursive depth sounder iterates the CNT through derived
compositions until signal exhaustion.

### Derived composition constructors

```
function energy_composition(tensor):
    # e_j(t) = (delta h_j)^2 / sum (delta h_k)^2
    energies = []
    for i in 1 to T-1:
        delta_h = tensor.timesteps[i].clr - tensor.timesteps[i-1].clr
        energies.append(close([d*d for d in delta_h]))
    return energies

function curvature_composition(tensor):
    # c_j(t) = kappa_jj(t) / sum kappa_kk(t)
    curvatures = []
    for ts in tensor.timesteps:
        diag = ts.metric_tensor.matrix[i][i] for i in 0..D-1
        curvatures.append(close(diag))
    return curvatures
```

### Depth sounder main loop

```
function depth_sounder(records, tensor):
    # Involution proof — sample at multiple t
    involution_proof = {
        samples: [],
    }
    for t in [0, T/2, T-1]:
        x = tensor.timesteps[t].composition
        Mx = M(x)
        MMx = M(Mx)
        residual = norm(array(MMx) - array(x))
        involution_proof.samples.append({ t, x, Mx, MMx, residual_M2: residual, ... })
    involution_proof.mean_residual = mean(s.residual_M2 for s in samples)
    involution_proof.verified = (involution_proof.mean_residual < 1e-10)

    # Level 0 — base statistics
    level_0 = base_statistics(tensor)

    # Energy tower
    energy_tower = []
    current_records = records
    current_tensor = tensor
    while not exhausted and len(energy_tower) < MAX_LEVELS:
        derived = energy_composition(current_tensor)
        if len(derived) < 5:
            status = "SIGNAL_SHORT"; break
        new_tensor = compute_tensor_for(derived)
        level_summary = summarise_level(new_tensor, level=len(energy_tower)+1)
        energy_tower.append(level_summary)
        if detect_flat(new_tensor):
            level_summary.status = "OMEGA_FLAT" or "HS_FLAT"; break
        if detect_period_2(energy_tower):
            level_summary.status = "LIMIT_CYCLE_P2"; break
        if detect_period_1(energy_tower):
            level_summary.status = "LIMIT_CYCLE_P1"; break
        current_tensor = new_tensor

    # Curvature tower — same loop with curvature_composition
    curvature_tower = ... (analogous)

    # Period-2 attractor
    curvature_traj = [lvl.hs_mean for lvl in curvature_tower]
    if attractor detected with period 2:
        tail = curvature_traj[-6:] (last 6 levels for stable estimate)
        c_even = mean of even-indexed entries in tail
        c_odd = mean of odd-indexed entries in tail
        amplitude = |c_even - c_odd|
        deltas = [traj[n] - (c_even if n even else c_odd) for n]
        contraction_ratios = [|deltas[n+2]| / |deltas[n]| for n]
        contraction_lyapunov = mean(ln(r) for r in contraction_ratios if r > 0)
        mean_contraction_ratio = mean(contraction_ratios)
        banach_satisfied = (mean_contraction_ratio < 1)

        depth_curvature_attractor = {
            period: 2,
            c_even, c_odd, amplitude,
            convergence_level, residual,
            contraction_lyapunov,
            mean_contraction_ratio,
            banach_satisfied,
        }
    else:
        depth_curvature_attractor = { period: 1 (or 0), ... }

    # Impulse response
    A_initial = |curvature_traj[1] - curvature_traj[0]|
    A_final = amplitude
    depth_delta = curvature_depth
    damping_zeta = -ln(A_final / A_initial) / depth_delta
    classification = classify_IR(amplitude, damping_zeta)

    depth_impulse_response = {
        amplitude_A: amplitude,
        depth_delta,
        damping_zeta,
        classification,
    }

    return {
        involution_proof,
        level_0,
        energy_tower,
        curvature_tower,
        curvature_attractor: depth_curvature_attractor,
        impulse_response: depth_impulse_response,
        summary: { energy_depth, curvature_depth, ... },
    }
```

### IR classification

```
function classify_IR(A, zeta):
    if A < 0.1:
        return "CRITICALLY_DAMPED"
    if zeta > 0 and zeta < 0.1:
        return "LIGHTLY_DAMPED"
    if abs(zeta) < 1e-6:
        return "UNDAMPED"
    if A > 0.7:
        return "OVERDAMPED_EXTREME"
    return "MODERATELY_DAMPED"
```

---

## §5 — `diagnostics` block

### EITT residuals

```
function eitt_bench_test(records):
    H_full = mean(shannon_entropy(rec.composition) for rec in records)
    M_sweep = []
    for M in [2, 4, 8, 16, 32, 64, 128, ceil(T/101)]:
        if M >= T: continue
        decimated = []
        for b in range(0, T, M):
            block = records[b : b+M]
            if len(block) >= 2:
                decimated.append(aitchison_barycenter([r.composition for r in block]))
            elif len(block) == 1:
                decimated.append(block[0].composition)
        H_decimated = mean(shannon_entropy(c) for c in decimated)
        variation = abs(H_decimated - H_full) / H_full * 100
        M_sweep.append({ M, n_blocks: len(decimated), H_mean_decimated: H_decimated, variation_pct: variation, pass_5pct: variation < 5 })
    return {
        H_mean_full: H_full,
        M_sweep,
        gate_pct: 5.0,
        note: "Empirical observation of trajectory smoothness, not geometric theorem.",
    }
```

### Lock events

```
function detect_lock_events(records, tensor):
    events = []
    DEGEN_THRESHOLD = 1e-4   # CLR spread
    LOCK_CLR_THRESHOLD = -10
    for i, ts in enumerate(tensor.timesteps):
        clr_spread = max(ts.clr) - min(ts.clr)
        if clr_spread < DEGEN_THRESHOLD:
            events.append({
                event_type: "DEGEN",
                timestep_index: i,
                label: ts.label,
                carrier: null,
                clr_value: clr_spread,
                context: "Composition collapsed to barycenter",
            })
        for j, h in enumerate(ts.clr):
            if h < LOCK_CLR_THRESHOLD:
                # determine if this is LOCK-ACQ (transition from valid -> degen) or LOCK-LOSS (degen -> valid)
                event_type = "LOCK-ACQ" if (i > 0 and tensor.timesteps[i-1].clr[j] >= LOCK_CLR_THRESHOLD) else "LOCK-LOSS"
                events.append({
                    event_type,
                    timestep_index: i,
                    label: ts.label,
                    carrier: records.carriers[j],
                    clr_value: h,
                    context: f"{records.carriers[j]} approached zero (CLR={h:.2f})",
                })
    return events
```

### Degeneracy flags

```
function degeneracy_flags(records, tensor):
    flags = []
    if records.T < 20:
        flags.append({
            flag: "small_T",
            severity: "warning",
            message: "Trajectory too short for stable depth-tower estimation",
            condition: f"T = {records.T} < 20",
        })
    if records.D < 3:
        flags.append({
            flag: "small_D",
            severity: "warning",
            ...
        })
    # Pre-aligned: monotonic in any single carrier
    for j in 0..D-1:
        series = [rec.composition[j] for rec in records]
        if is_monotonic(series):
            flags.append({
                flag: "pre_aligned_compositionally",
                severity: "warning",
                message: f"Records appear sorted by carrier {records.carriers[j]} — depth recursion may be degenerate",
                condition: f"


---

# Part E — JSON schema 2.1.0 (the canonical contract)


**Schema version:** 2.0.0
**Engine version supported:** 2.0.3 (Python reference implementation; cnt.R port at 2.0.2)
**Status:** Authoritative
**Last revised:** 2026-05-05

**Major change from 1.0.0:** Every analytic block (tensor, stages, bridges,
depth, diagnostics) is now split into `coda_standard/` and `higgins_extensions/`
sub-blocks. Every analytic block declares its functional role (`_function`:
composer / review / formatter). Section 8 documents the CoDa↔Higgins
mathematical mapping.

**Engine fix log within 2.0.x:**

| Engine version | Fix |
|---|---|
| 2.0.0 | Initial split into coda_standard / higgins_extensions sub-blocks |
| 2.0.1 | `detect_period` requires TWO consecutive convergences for period-1 (was 1; fixed false-positive on USA EMBER and Ball/TAS) |
| 2.0.1 | `derived_curvature` corrected to use 1/x_j² (was 1/x_j) — matches Math Handbook Ch 19.2(b) |
| 2.0.1 | `TRIADIC_T_LIMIT` default lowered from 1000 to 500 |
| 2.0.2 | `metadata.engine_config` block added — REQUIRED field (see §1.2) |
| 2.0.2 | `eitt_residuals.M_sweep[i].pass_5pct` renamed to `pass_gate` (more general; reflects user-configurable EITT_GATE_PCT) |
| 2.0.3 | IR taxonomy refined: `DEGENERATE` is split into three more-informative classes — `ENERGY_STABLE_FIXED_POINT` (energy depth ≥ DEPTH_MAX_LEVELS with stable A), `CURVATURE_VERTEX_FLAT` (curvature recursion driven to vertex by single-carrier dominance), `D2_DEGENERATE` (genuine D=2 limitation; only one independent compositional axis). Python only — cnt.R remains at the 2.0.2 single-`DEGENERATE` taxonomy. |

---

## Reading This Schema

The CNT engine ingests a compositional dataset and emits exactly one JSON
conforming to this document. Downstream tools read only this JSON. The
schema is the contract; the engine and the viewers honour it.

The schema follows semantic versioning. Field additions bump the minor
version. Field removals or type changes bump the major version. Old
viewers continue to work under any minor bump.

---

## Two Orthogonal Classifications

Every analytic field carries two labels:

**Ownership** — whether the field is part of the CoDa standard (Aitchison /
Egozcue / Pawlowsky-Glahn / Shannon lineage) or a Higgins-framework
extension. A CoDa-community reviewer can read just `coda_standard/`
fields and audit the engine's compositional analysis without engaging
Higgins-specific machinery. The mapping in §8 shows that every Higgins
extension is computable from CoDa-standard quantities — it is a *reading*
of the simplex, not a deviation from it.

**Function** — the role the block plays in the engine pipeline:

| `_function`  | Role                                                              |
|--------------|-------------------------------------------------------------------|
| `composer`   | Creates compositional structure from raw data (closure, CLR, etc.)|
| `review`     | Analyses the composed structure (variation matrix, attractor)     |
| `formatter`  | Prepares specific representations for display (atlas, ledger)     |
| `provenance` | Identity, hashes, environment — neither computation nor display   |

This functional split clarifies *who reads what*: a viewer building a
projector reads `composer` blocks; a viewer building an analytical
report reads `review` blocks; a viewer building plates reads
`formatter` blocks.

---

## Top-Level Structure

```json
{
  "metadata":    { ... },     // _function: provenance
  "input":       { ... },     // _function: provenance + composer prep
  "tensor":      { ... },     // _function: composer
  "stages": {
    "stage1":    { ... },     // _function: formatter
    "stage2":    { ... },     // _function: review
    "stage3":    { ... }      // _function: review
  },
  "bridges":     { ... },     // _function: review
  "depth":       { ... },     // _function: review
  "diagnostics": { ... }      // _function: review
}
```

Every analytic block (tensor, each stage, bridges, depth, diagnostics)
carries `_function`, `_description`, `coda_standard/`, and
`higgins_extensions/`. `coda_standard/` may be `{}` when the entire
block is HUF-specific (e.g. `depth/` is wholly Higgins; the curvature
tower is not part of the CoDa canon).

---

## 1 — `metadata/`

`_function: "provenance"`. Identity, schema version, run-time provenance.

| Field                        | Type   | Notes                                                                  |
|------------------------------|--------|------------------------------------------------------------------------|
| `schema_version`             | str    | "2.0.0".                                                               |
| `engine_version`             | str    | E.g. "cnt 2.0.3".                                                      |
| `engine_implementation`      | str    | "python" \| "R".                                                       |
| `generated`                  | str    | ISO-8601 UTC timestamp.                                                |
| `wall_clock_ms`              | int    | Total run time in milliseconds.                                        |
| `mathematical_lineage`       | object | Citations: Aitchison 1986, Shannon 1948, Egozcue 2003, Higgins 2026.   |
| `engine_config/`             | object | **REQUIRED** (added 2.0.2). Active values from USER CONFIG block.      |
| `environment/`               | object | git_sha, language_version, numerical_lib, platform, hostname_hash.    |

### 1.1 — `metadata/engine_config/` — REQUIRED (added 2.0.2)

Active values from the engine's USER CONFIGURATION block at the top of
`cnt.py` / `cnt.R`. The block is part of the deterministic content and
included in `diagnostics.content_sha256`. Two runs with identical
config and identical input produce identical content_sha256; two runs
with different config produce different content_sha256.

| Field                       | Type      | Default              | Notes                                                                       |
|-----------------------------|-----------|----------------------|-----------------------------------------------------------------------------|
| `_description`              | str       | (fixed)              | Plain-language note about the deterministic contract.                       |
| `DEFAULT_DELTA`             | float     | 1e-15                | Zero-replacement floor.                                                     |
| `DEGEN_THRESHOLD`           | float     | 1e-4                 | CLR-spread threshold for DEGEN lock event.                                  |
| `LOCK_CLR_THRESHOLD`        | float     | -10.0                | CLR threshold for LOCK-ACQ / LOCK-LOSS events.                              |
| `DEPTH_MAX_LEVELS`          | int       | 50                   | Hard cap on depth-tower length.                                             |
| `DEPTH_PRECISION_TARGET`    | float     | 0.01                 | Relative precision for period detection (1%).                               |
| `NOISE_FLOOR_OMEGA_VAR`     | float     | 1e-6                 | OMEGA_FLAT termination threshold.                                           |
| `TRIADIC_T_LIMIT`           | int       | 500                  | Above this T, Stage 3 day-triad enumeration is skipped.                    |
| `TRIADIC_K_DEFAULT`         | int       | 500                  | When triadic enumeration runs, store top-K results by area.                 |
| `EITT_GATE_PCT`             | float     | 5.0                  | Variation_pct gate for EITT bench-test.                                     |
| `EITT_M_SWEEP_BASE`         | list[int] | [2,4,8,16,32,64,128] | Base M-sweep compression ratios.                                            |

The user is the operator. The engine reports its active configuration
in every JSON it produces.

---

## 2 — `input/`

`_function: "provenance"` (raw data record) + `composer` (the closed canonical form).

| Field                  | Type        | Notes                                                                 |
|------------------------|-------------|-----------------------------------------------------------------------|
| `source_file`          | str         | Filename of the source CSV (basename only).                           |
| `source_file_sha256`   | str         | SHA-256 of the raw bytes of `source_file`.                            |
| `closed_data_sha256`   | str         | SHA-256 of the closed canonical simplex form (post-ingestion).        |
| `n_records`            | int         | Number of compositional records (T).                                  |
| `n_carriers`           | int         | Number of compositional parts (D).                                    |
| `carriers`             | list[str]   | Carrier names, length D.                                              |
| `labels`               | list[str]   | Per-record labels.                                                    |
| `zero_replacement/`    | object      | { method, delta, applied, n_replacements }.                           |
| `ordering/`            | object      | REQUIRED. { is_temporal, ordering_method, caveat }.                   |

`ordering/` flags whether the input is a time series. Several derivative
fields in `tensor/`, `stages/`, and `depth/` are order-dependent
(angular velocity, energy tower depth, bearing reversals). Viewers must
check `ordering.is_temporal` before interpreting derivative quantities.

---

## 3 — `tensor/`

```
_function:    "composer"
_description: "Per-record compositional state computed by applying
               operators to the input."
```

### 3.1 — `tensor/helmert_basis/`

Always present. Used by both `coda_standard.ilr` and downstream Higgins
machinery.

| Field          | Type        | Notes                                                  |
|----------------|-------------|--------------------------------------------------------|
| `D`            | int         | Carrier count.                                         |
| `dim`          | int         | D − 1 (rank).                                          |
| `coefficients` | list[list]  | (D−1) × D matrix.                                      |

### 3.2 — `tensor/timesteps[i]/`

For each record i ∈ [0, T):

```json
{
  "index": <int>,
  "label": <str>,
  "raw_values": [<float>...],
  "coda_standard": {
    "composition":             [...],   // closure to simplex, sums to 1
    "clr":                     [...],   // CLR transform
    "ilr":                     [...],   // ILR projection (Helmert)
    "shannon_entropy":         <float>, // -sum x_j ln x_j
    "aitchison_norm":          <float>, // ||clr(x)||
    "aitchison_distance_step": <float>  // present iff i >= 1
  },
  "higgins_extensions": {
    "higgins_scale":           <float>, // Hs = 1 - H/ln(D), in [0,1]
    "bearing_tensor": {
      "pairs": [
        { "carrier_i": <str>, "carrier_j": <str>, "theta_deg": <float> },
        ...                                  // D(D-1)/2 entries
      ]
    },
    "metric_tensor": {
      "matrix":      [...],              // full D x D Aitchison metric
      "eigenvalues": [...],              // length D, ascending
      "trace":       <float>
    },
    "metric_tensor_diagonal":  [...],    // (1 - 1/D) / x_j^2 per j
    "condition_number":        <float>,  // max(x)/min(x)
    "angular_velocity_deg":    <float>,  // present iff i >= 1
    "helmsman":                <str>,    // present iff i >= 1
    "helmsman_delta":          <float>   // present iff i >= 1
  }
}
```

`coda_standard/` is the CoDa-community-recognised core. `higgins_extensions/`
are Higgins-framework readings of the same simplex. The mapping in §8
shows each extension as a function of `coda_standard/` quantities.

---

## 4 — `stages/`

Stage 1 / 2 / 3 cross-examinations. Each stage has its own `_function`.

### 4.1 — `stages/stage1/` — formatter

```
_function:    "formatter"
_description: "Cube-face projections and per-record metric ledger
               formatted for plate display."
```

| `coda_standard/`    | `higgins_extensions/`            |
|---------------------|----------------------------------|
| (empty — Stage 1 outputs are display formatters specific to HUF/CBS) | `section_atlas[]`, `metric_ledger[]` |

`section_atlas[i]` per record: { index, label, xy_face, xz_face, yz_face,
metric_tensor_trace, condition_number, angular_velocity_deg }.

`metric_ledger[i]` per record: { index, label, hs, ring, omega_deg,
helmsman, energy, condition }.

### 4.2 — `stages/stage2/` — review

```
_function:    "review"
_description: "Pairwise cross-examination of compositional behaviour."
```

| `coda_standard/`            | `higgins_extensions/`              |
|-----------------------------|------------------------------------|
| `variation_matrix` (Aitchison τ_ij = var(ln(x_i/x_j)), D × D) | `carrier_pair_examination[]` (per-pair pearson_r, co_movement, opposition, bearing_spread, locked-flag) |

### 4.3 — `stages/stage3/` — review

```
_function:    "review"
_description: "Higher-degree subcompositional and triadic analysis."
```

| `coda_standard/`              | `higgins_extensions/`                                |
|-------------------------------|-------------------------------------------------------|
| `subcomposition_ladder[]` (degree k ∈ [2, D−1]) | `triadic_area/`, `carrier_triads[]`, `regime_detection/` |

`triadic_area/` declares `n_candidates`, `n_returned`, `selection_method`
(`top_K_by_area` / `none_T_too_small` / `none_T_too_large`),
`selection_K`, and `results[]`.

---

## 5 — `bridges/`

```
_function:    "review"
_description: "Connections to dynamical / control / information theory."
```

| `coda_standard/`                                 | `higgins_extensions/`                               |
|--------------------------------------------------|-----------------------------------------------------|
| `information_theory/` (entropy_series, fisher_information, kl_divergence, mutual_information, entropy_rate) | `dynamical_systems/` (per_carrier_lyapunov, velocity_field, recurrence_analysis), `control_theory/` (state_space_model, observability) |

The information-theory bridge is in `coda_standard/` because Shannon
entropy and its derivatives are not exclusively CoDa, but the CoDa
community uses them on log-ratio coordinates. The dynamical and control
bridges are Higgins extensions.

---

## 6 — `depth/`

```
_function:    "review"
_description: "Recursive depth sounder, period-2 attractor, impulse response.
               Wholly Higgins-framework — no CoDa-standard analogue."
```

| `coda_standard/`     | `higgins_extensions/`                                                                   |
|----------------------|-----------------------------------------------------------------------------------------|
| `{}` — empty by design. The depth sounder, energy/curvature towers, period-2 attractor, and impulse response are Higgins extensions; they have no CoDa-canon equivalent. | `involution_proof/`, `level_0/`, `energy_tower[]`, `curvature_tower[]`, `curvature_attractor/`, `impulse_response/`, `energy_cycle/`, `curvature_cycle/`, `summary/` |

### 6.1 — `depth/higgins_extensions/curvature_attractor/`

| Field                   | Type   | Notes                                                          |
|-------------------------|--------|----------------------------------------------------------------|
| `period`                | int    | 1 (fixed point) or 2 (limit cycle). 0 if no attractor detected.|
| `c_even`                | float  | Mean Hs at even-parity tail levels.                            |
| `c_odd`                 | float  | Mean Hs at odd-parity tail levels.                             |
| `amplitude`             | float  | \|c_even − c_odd\|.                                            |
| `convergence_level`     | int    | Recursion level at which detected.                             |
| `residual`              | float  | Final residual at convergence.                                 |
| `contraction_lyapunov`  | float  | Same-parity contraction Lyapunov exponent.                     |
| `mean_contraction_ratio`| float  | Mean of \|Δ(n+2)\|/\|Δ(n)\|.                                   |
| `banach_satisfied`      | bool   | mean_contraction_ratio < 1.                                    |

### 6.2 — `depth/higgins_extensions/impulse_response/`

| Field            | Type   | Notes                                                          |
|------------------|--------|----------------------------------------------------------------|
| `amplitude_A`    | float  | Same as `curvature_attractor.amplitude`.                       |
| `depth_delta`    | int    | Curvature tower convergence level.                             |
| `damping_zeta`   | float  | −ln(A_final/A_initial) / depth_delta.                          |
| `classification` | str    | CRITICALLY_DAMPED / LIGHTLY_DAMPED / UNDAMPED / OVERDAMPED_EXTREME / MODERATELY_DAMPED. |

---

## 7 — `diagnostics/`

```
_function:    "review"
_description: "Engine self-checks: EITT residuals, lock events,
               degeneracy flags, content hash."
```

| `coda_standard/`     | `higgins_extensions/`                                                       |
|----------------------|-----------------------------------------------------------------------------|
| `{}` — diagnostics are HUF-engine-specific health checks; they do not correspond to CoDa-canon procedures. | `eitt_residuals/`, `lock_events[]`, `degeneracy_flags[]` |

`content_sha256` (top-level under `diagnostics/`, outside both sub-blocks)
is the reproducibility hash. SHA-256 of the canonicalised JSON with
`metadata.generated`, `metadata.wall_clock_ms`, `metadata.environment`,
and `diagnostics.content_sha256` removed. Two runs of the engine on
identical input produce identical `content_sha256`.

`eitt_residuals/` carries the explicit framing note (Egozcue 2026):
*"Empirical observation of trajectory smoothness under temporal
decimation, not a geometric theorem. Shannon entropy is not
scale-invariant; the apparent preservation reflects compositional
smoothness of the trajectory, not Aitchison invariance."*

---

## 8 — CoDa ↔ Higgins Mapping

Every Higgins extension is a function of `coda_standard/` quantities.
A CoDa reviewer can verify by inspection that the extension reduces to
or builds upon recognised CoDa primitives.

### 8.1 — Higgins extensions defined per record

| Higgins field                    | Equation                                                            | CoDa primitives used        |
|----------------------------------|---------------------------------------------------------------------|----------------------------|
| `higgins_scale`                  | `Hs = 1 - shannon_entropy / ln(D)`                                  | composition, D             |
| `bearing_tensor.pairs[k].theta_deg` | `θ_ij = atan2(clr_j, clr_i)` × (180/π)                            | clr                        |
| `metric_tensor.matrix[i][j]`     | `κ_ij = (δ_ij − 1/D) / (x_i × x_j)` — Aitchison pullback metric     | composition (x), D         |
| `metric_tensor.eigenvalues`      | `eigvals(κ)`                                                        | metric_tensor.matrix       |
| `metric_tensor.trace`            | `tr(κ) = Σ_j (1 − 1/D) / x_j²`                                      | composition, D             |
| `metric_tensor_diagonal[j]`      | `κ_jj = (1 − 1/D) / x_j²`                                            | composition, D             |
| `condition_number`               | `max(x) / min(x)`                                                   | composition                |
| `angular_velocity_deg`           | `ω = atan2(‖clr_t × clr_{t-1}‖, ⟨clr_t, clr_{t-1}⟩)` × (180/π)      | clr at t and t−1           |
| `helmsman`                       | `argmax_j |clr_j(t) − clr_j(t-1)|`                                  | clr at t and t−1           |
| `helmsman_delta`                 | `max_j |clr_j(t) − clr_j(t-1)|`                                     | clr at t and t−1           |

The Aitchison metric κ_ij is part of CoDa (Egozcue & Pawlowsky-Glahn
discussions of the simplex inner product), but the explicit coordinate
form, the bearing tensor reading via atan2, and the helmsman /
condition number diagnostics are Higgins-specific framings.

### 8.2 — Stage 2 / Stage 3 mappings

| Higgins field                                | Equation / Definition                                                  |
|----------------------------------------------|------------------------------------------------------------------------|
| `carrier_pair_examination[k].pearson_r`      | Pearson r on the CLR-projected series for carrier pair (i, j)          |
| `carrier_pair_examination[k].bearing_spread_deg` | `max_t θ_ij(t) − min_t θ_ij(t)` over the trajectory                |
| `carrier_pair_examination[k].locked`         | `bearing_spread_deg < 10°`                                              |
| `triadic_area.results[k].area`               | Heron's formula in CLR space on three time-indexed CLR vectors         |
| `regime_detection.boundaries[k]`             | step indices where `aitchison_distance_step > mean + 2·std`            |

### 8.3 — Bridge mappings

`per_carrier_lyapunov[j].lyapunov_exponent` — heuristic estimate of the
log-divergence rate of the CLR series for carrier j. Not a formal
Lyapunov exponent of a dynamical system; an approximation derived from
the CLR difference series.

`recurrence_analysis.recurrence_rate` — fraction of pairs (a, b) with
`aitchison_distance(x_a, x_b) < 0.1 × max_aitchison_distance` over the
trajectory.

`state_space_model.A_matrix` — least-squares AR(1) fit on the CLR series.

### 8.4 — Depth sounder mappings

The depth sounder is wholly Higgins. Each derived composition is
defined by an explicit equation:

| Field                      | Equation                                                         |
|----------------------------|------------------------------------------------------------------|
| `metric_dual M(x)_j`       | `(1/x_j) / Σ_k (1/x_k)` — involution: M² = identity, clr(M(x)) = −clr(x) |
| `derived_curvature c_j(t)` | `(1/x_j²) / Σ_k (1/x_k²)` — normalised diagonal of the Aitchison metric κ |
| `derived_energy e_j(t)`    | `(Δclr_j)² / Σ_k (Δclr_k)²` — kinetic energy in CLR space, normalised   |
| `level_k composition`      | Output of the previous level passed through the chosen derived constructor |
| `period-2 attractor`       | Empirical: the curvature recursion's Hs trajectory converges to a 2-cycle in 14/19 tested systems. NOT a theorem. |
| `contraction_lyapunov λ`   | `mean_n ln(|Δ(n+2)| / |Δ(n)|)` where Δ(n) = traj[n] − attractor |
| `impulse_response.A`       | `|c_even − c_odd|` — peak-to-peak attractor displacement         |
| `impulse_response.ζ`       | `−ln(A_final / A_initial) / depth_delta`                         |

### 8.5 — Diagnostics mappings

`eitt_residuals.M_sweep[k].variation_pct` —
`100 × |mean_t H(decimated_t at compression M) − mean_t H(x_t)| / mean_t H(x_t)`

This is an *observation* about compositional trajectory smoothness, not
a CoDa-geometric theorem. The schema records it as such.

`lock_events[k]` — events triggered by simple thresholds on CLR values:

| Event type   | Trigger condition                                         |
|--------------|------------------------------------------------------------|
| DEGEN        | max(clr) − min(clr) < 1e-4 (composition near barycenter)  |
| LOCK-ACQ     | clr_j < −10 with previous clr_j ≥ −10                      |
| LOCK-LOSS    | clr_j < −10 with subsequent clr_j ≥ −10                    |

These are display markers; they do not modify any analysis.

---

## 9 — Schema Validation

An engine is **schema-conformant** if and only if:

1. The output JSON has exactly the seven top-level keys above.
2. Every analytic block (tensor, each stage, bridges, depth, diagnostics)
   carries `_function` (one of: composer, review, formatter, provenance),
   `_description`, `coda_standard`, `higgins_extensions`.
3. All fields marked **REQUIRED** in this document are present.
4. All fields have the declared type.
5. `metadata/schema_version` matches the schema version in this document.
6. Numerical sanity holds (closure to 1 ± 1e-15, CLR sums to 0 ± 1e-14,
   M² residual < 1e-10).
7. `diagnostics/content_sha256` reproduces under re-run.

Conformant viewers can rely on the schema as a contract. Non-conformant
JSON is rejected at the viewer's input gate.

---

## 10 — Schema Versioning Policy

| Action                                       | Version bump |
|----------------------------------------------|--------------|
| Add a new optional field                     | minor (2.0 → 2.1)  |
| Add a new REQUIRED field                     | major (2.x → 3.0)  |
| Remove a field                               | major              |
| Change a field's type                        | major              |
| Move a field between coda_standard/higgins_extensions | major     |
| Move a field between functional blocks       | major              |
| Tighten a field's allowed values             | major              |
| Loosen a field's allowed values              | minor              |
| Fix typo in field description                | patch (2.0.0 → 2.0.1) |

A viewer that declares `min_schema_version: 2.0.0` works with all 2.x.x.

---

## Migration from 1.0.0

| 1.0.0 path                                       | 2.0.0 path                                                       |
|--------------------------------------------------|-------------------------------------------------------------------|
| `tensor.timesteps[i].composition`                | `tensor.timesteps[i].coda_standard.composition`                  |
| `tensor.timesteps[i].clr`                        | `tensor.timesteps[i].coda_standard.clr`                          |
| `tensor.timesteps[i].ilr`                        | `tensor.timesteps[i].coda_standard.ilr`                          |
| `tensor.timesteps[i].shannon_entropy`            | `tensor.timesteps[i].coda_standard.shannon_entropy`              |
| `tensor.timesteps[i].aitchison_norm`             | `tensor.tim


---

# Part F — Schema reference (reader's view)


The schema is the contract between the engine and every viewer. This
section is a reference for what fields appear in a conforming JSON
and what they mean. The full normative definition is
`cnt/CNT_JSON_SCHEMA.md`; this section is the user-facing summary.

## Top-level structure

A conforming JSON has exactly seven top-level blocks:

```
{
  "metadata":    {...},   // identity and run-time provenance
  "input":       {...},   // closed data, hashes, ordering, zero replacement
  "tensor":      {...},   // Helmert basis + per-timestep tensor
  "stages":      {...},   // Stage 1/2/3 outputs (coda_standard + higgins_extensions)
  "bridges":     {...},   // cross-block bridges
  "depth":       {...},   // energy and curvature towers, attractor, IR
  "diagnostics": {...}    // EITT, locks, degeneracy, content_sha256
}
```

Every analytic block carries a `_function` tag — `provenance`,
`composer`, `review`, or `formatter` — so a viewer can route blocks
to the right rendering surface.

Every analytic block (except `metadata`) is split into a
`coda_standard/` subblock — values that any CoDa text would compute
the same way — and a `higgins_extensions/` subblock containing the
HUF-specific quantities (CNT, depth, IR). The split is part of the
contract: a viewer that only renders CoDa-standard fields can ignore
the higgins_extensions block entirely; a HUF-aware viewer renders
both.

## metadata

Identity and provenance. Every conforming JSON declares:

| Field | Purpose |
|---|---|
| `schema_version`        | E.g. "2.0.0" |
| `engine_version`        | E.g. "cnt 2.0.3" |
| `engine_implementation` | "python" or "R" |
| `generated`             | ISO 8601 timestamp |
| `wall_clock_ms`         | Run time in milliseconds |
| `mathematical_lineage`  | Citations to the underlying mathematical work |
| `engine_config`         | The active USER CONFIGURATION values |
| `environment`           | Python/R version, numerical library, hostname hash |

The `engine_config` block is the determinism receipt. Two runs with
the same input and the same `engine_config` produce the same
`content_sha256`. A run that omits `engine_config` is non-conforming.

## input

Records the data the engine consumed:

| Field | Purpose |
|---|---|
| `source_file`        | Filename of the input CSV |
| `source_file_sha256` | SHA-256 of the file as read |
| `closed_data_sha256` | SHA-256 of the closed-to-simplex matrix (after zero replacement) |
| `n_records`          | T |
| `n_carriers`         | D |
| `carriers`           | List of carrier names from the header |
| `labels`             | List of row labels from the first column |
| `zero_replacement`   | δ, count of replaced cells, "applied" flag |
| `ordering`           | is_temporal flag, method, caveat |

Two files with the same closed_data_sha256 produce the same engine
output. A user reproducing a published run should compare both the
source SHA (to confirm the input file is the same) and the closed
SHA (to confirm the engine read it the same way).

## tensor

The Stage 0 + Stage 1 numerical core.

* `helmert_basis` — D-dimensional Helmert basis used for ILR
  projections.
* `timesteps[]` — one entry per record: label, index, raw values,
  CLR coordinates, ILR coordinates, bearing pairs (θ_ij), angular
  velocity ω, helmsman σ, Higgins scale H_s, metric tensor diagonal
  and off-diagonal, condition number.

This block is the largest in a typical JSON. Atlas tour plates,
section_atlas (xy/xz/yz projections), and lock detection all read
from here.

## stages

Stage 1, 2, 3 outputs in nested subblocks. Each stage carries:

```
"stage<N>": {
  "coda_standard":     {...},
  "higgins_extensions": {...}
}
```

Stage 1 includes section_atlas (3-axis CLR projections per timestep
for the atlas tour plates) and metric_ledger (per-timestep H_s, ring
classification, helmsman). Stage 2 includes the variation matrix
(`coda_standard`) and per-carrier-pair examination
(`higgins_extensions`). Stage 3 includes the subcomposition ladder
(`coda_standard`) and triadic enumeration (`higgins_extensions`).

## bridges

Cross-domain bridges. Includes:

* `coda_standard/information_theory` — entropy series, fisher
  information, KL divergence, mutual information, entropy rate.
* `higgins_extensions/dynamical_systems` — per-carrier Lyapunov
  exponents, velocity field, recurrence analysis.
* `higgins_extensions/control_theory` — state-space observability
  per carrier.

The information-theory block is what most CoDa-standard viewers will
read. The dynamical-systems and control-theory blocks are the
HUF-specific extensions.

## depth

The recursive depth sounder's output:

* `coda_standard/` — the standard CoDa quantities at each level
  (subcompositional barycenters, log-ratio variances).
* `higgins_extensions/`:
  * `involution_proof` — samples of M(M(x)) = x verification, mean
    residual, verified flag.
  * `level_0` — initial level statistics (T, D, hs_mean, hs_var,
    omega_mean, omega_var, helmsman, status).
  * `energy_tower[]` — per-level statistics on the energy tower.
  * `curvature_tower[]` — per-level statistics on the curvature tower.
  * `curvature_attractor` — period, c_even, c_odd, amplitude,
    convergence_level, contraction_lyapunov, banach_satisfied.
  * `impulse_response` — amplitude_A, depth_delta, damping_zeta,
    classification.
  * `energy_cycle`, `curvature_cycle` — period detection per tower.
  * `summary` — flat headline values: energy_depth, curvature_depth,
    dynamical_depth, terminations, hs_trajectories,
    mean_duality_distance, convergence_precision, noise_floor_omega_var,
    max_levels.

The atlas IR card and helmsman-lineage plates read from this block.

## diagnostics

The audit surface:

* `coda_standard/` — empty in the current schema; reserved for
  future CoDa-standard diagnostic outputs.
* `higgins_extensions/`:
  * `eitt_residuals` — H_mean_full, M_sweep[], gate_pct, note.
    The atlas EITT plate reads from this.
  * `lock_events[]` — list of LOCK-ACQ / LOCK-REL events with
    timestep_index, label, carrier, clr_value, context.
  * `degeneracy_flags[]` — engine-detected degeneracy markers (rarely
    populated for well-formed inputs).
* `content_sha256` — the SHA-256 of the canonical JSON content. The
  determinism gate compares this to the published reference value.

## Validation

A JSON is **schema-conformant** if and only if all top-level blocks
exist, every analytic block carries `_function`, every block is
split into `coda_standard/` and `higgins_extensions/`,
`metadata.engine_config` is present, `metadata.schema_version`
matches the schema in this document, and `diagnostics.content_sha256`
is a 64-character hexadecimal string.

The atlas tool refuses to render non-conforming JSON. Mission
Command's `--update` mode rewrites INDEX.json only if the produced
JSON is conformant.

## Versioning

Schema additions of new optional fields bump the minor version
(2.0.x → 2.1.0). Field removals or type changes bump the major
version (2.x.x → 3.0.0). Old viewers that declare
`min_schema_version: 2.0.0` work with all 2.x.x outputs.

A version mismatch between engine and atlas — for example, an atlas
expecting 2.0.0 reading a 2.1.0 JSON — is non-fatal: the atlas
renders the fields it understands and ignores the rest. A 2.x atlas
reading a 1.x JSON is a hard error; old engines must be rerun.

---

For the full normative schema, including required-vs-optional flags
and exact type signatures for every field, see
`cnt/CNT_JSON_SCHEMA.md`.



---

# Part G — Output Doctrine v1.0.1 (integer orders, round-up rule)


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



---

# Part H — Stage 2 pseudocode (Order-2 algorithms)


**Module:** `atlas/stage2_locked.py`
**R port:** `atlas/stage2.R` (metric computation; PDF rendering is Python-only)
**Status:** Authoritative. Conforms to `atlas/OUTPUT_DOCTRINE.md` v1.0.1.
**Last revised:** 2026-05-05

This document is the language-neutral algorithm reference for Stage 2.
The Python (`stage2_locked.py`) and R (`stage2.R`) implementations are
reference instances of the algorithms defined here. Anyone reading this
can re-implement Stage 2 in any language.

---

## 1 — Inputs

A schema-2.x conformant CNT JSON. Stage 2 reads the following fields:

```
input.n_records              T
input.n_carriers             D
input.carriers               list of D carrier names
input.labels                 list of T row labels
tensor.helmert_basis.coefficients   (D-1, D) Helmert basis matrix
tensor.timesteps[t].coda_standard.clr            (D,)  CLR coordinates
tensor.timesteps[t].coda_standard.composition    (D,)  closed values
tensor.timesteps[t].higgins_extensions.bearing_tensor.pairs
                                       list of {carrier_i, carrier_j, theta_deg}
tensor.timesteps[t].higgins_extensions.metric_tensor.trace
tensor.timesteps[t].higgins_extensions.condition_number
stages.stage1.higgins_extensions.metric_ledger[t]
                                       hs, ring, omega_deg, helmsman, energy
stages.stage2.coda_standard.variation_matrix     (D, D)
stages.stage2.higgins_extensions.carrier_pair_examination
                                       list of {i, j, pearson_r, bearing_spread_deg, ...}
diagnostics.higgins_extensions.lock_events       list
metadata.engine_version, schema_version
diagnostics.content_sha256
```

No engine recomputation. Every value displayed at Stage 2 traces back to
one of these JSON fields by deterministic transforms.

---

## 2 — Order discipline

Per OUTPUT_DOCTRINE v1.0.1, Stage 2 displays only Order-2 content:

* per-step quantities aggregated across more than one timestep (Hs
  trajectory, Aitchison-norm trajectory, ILR-axes trajectories);
* inter-timestep dynamic quantities (bearings θ, angular velocity ω,
  metric trace, condition number, helmsman σ, ring class);
* whole-trajectory aggregates (variation matrix, pair correlations,
  lock events, V_net, path_length, course_directness);
* the System Course Plot (PCA-projected CLR trajectory, math handbook
  Ch 15) and the Compositional Bearing Scope (CBS, Ch 16).

Stage 1 (single-composition first principles) and Stage 3 (recursive /
dynamical) are out of scope.

---

## 3 — Algorithms

### 3.1 — Trajectory aggregates

```
For t in 0..T-1:
    composition[t]  = json.tensor.timesteps[t].coda_standard.composition
    clr[t]          = json.tensor.timesteps[t].coda_standard.clr
    aitchison_norm[t] = sqrt( sum_j clr[t][j]^2 )
    Hs[t]           = json.stages.stage1.higgins_extensions.metric_ledger[t].hs
    ring[t]         = json.stages.stage1.higgins_extensions.metric_ledger[t].ring
    omega[t]        = json.stages.stage1.higgins_extensions.metric_ledger[t].omega_deg
    helmsman[t]     = json.stages.stage1.higgins_extensions.metric_ledger[t].helmsman

basis = json.tensor.helmert_basis.coefficients     # (D-1, D)
ilr_mat = clr[*] @ basis.T                         # (T, D-1)
```

### 3.2 — Inter-step Aitchison distances

```
For t in 1..T-1:
    d_step[t] = sqrt( sum_j (clr[t][j] - clr[t-1][j])^2 )
d_step[0] = 0.0
```

### 3.3 — Pairwise distance matrix

```
For a in 0..T-1:
    For b in 0..T-1:
        d_mat[a, b] = sqrt( sum_j (clr[a][j] - clr[b][j])^2 )
```

### 3.4 — Navigation metrics (System Course Plot)

```
h_start          = clr[0]
h_final          = clr[T-1]
V_net            = h_final - h_start
net_distance     = || V_net ||              (Euclidean norm of V_net)
path_length      = sum over t of d_step[t]
course_directness = net_distance / path_length     (∈ [0, 1])
                                              1.0 ⇒ straight S→F line
                                              0.0 ⇒ pure looping
dynamic_range_S  = max(h_start) - min(h_start)
dynamic_range_F  = max(h_final) - min(h_final)
```

### 3.5 — System Course Plot projection (Math Handbook Ch 15)

```
X = clr - row_mean(clr)                     # T × D, centred
SVD: X = U S V^T                            # principal-component decomposition
PC1 = (U[:, 0] * S[0])                      # T × 1, first principal coord
PC2 = (U[:, 1] * S[1])                      # T × 1, second principal coord
var_explained_PC1 = S[0]^2 / sum(S^2)
var_explained_PC2 = S[1]^2 / sum(S^2)
```

### 3.6 — Bearing aggregates

```
For t in 0..T-1:
    bearings[t, k]  = θ_ij at timestep t for carrier-pair index k
    where the k-index iterates over combinations(D, 2) in lex order

mean_theta[t] = mean over k of bearings[t, k]   (ignoring NaN)
```

### 3.7 — Helmsman frequency + transition matrix

```
For each carrier c:
    helmsman_count[c] = # of t with helmsman[t] == c

For each (a, b) carrier pair:
    transition[a, b] = # of t such that helmsman[t] == a AND helmsman[t+1] == b
```

### 3.8 — Pair Pearson r matrix

```
R = identity D × D
For each entry p in stages.stage2.higgins_extensions.carrier_pair_examination:
    R[p.i, p.j] = R[p.j, p.i] = p.pearson_r
```

### 3.9 — Pairwise divergence ranking

```
candidates = []
For a in 0..T-1:
    For b in a+1..T-1:
        candidates.append( (a, b, d_mat[a, b]) )
candidates.sort(key=descending d)
top_15 = candidates[0:15]
```

### 3.10 — Compositional Bearing Scope (CBS) — three orthogonal faces (Math Handbook Ch 16)

```
For each timestep t:
    plot point on:
        face XY:  x = mean_theta[t],  y = d_step[t]
        face XZ:  x = mean_theta[t],  y = metric_trace[t]   (log)
        face YZ:  x = d_step[t],      y = metric_trace[t]   (log)
    colour by t (early = dark, late = bright)
```

---

## 4 — Plates emitted

The locked Stage 2 atlas emits 19 plates in this fixed order:

```
01  Cover + declaration
02  System Course Plot (PCA 2D path, S/F markers, V_net arrow)
03  Hs trajectory line plot
04  Aitchison-norm trajectory line plot
05  ILR axes 1-3 trajectories overlaid
06  Polar bearing rose at 4 sample timesteps
07  Bearing heatmap T × C(D,2) pairs
08  ω angular velocity trajectory
09  Metric tensor trace + condition number (two-panel line)
10  Helmsman σ lineage timeline (categorical strip)
11  Helmsman frequency + transition matrix + per-year displacement
12  Ring class strip + Hs trajectory
13  Lock event timeline (carrier × t)
14  Variation matrix τ_ij heatmap
15  Pair Pearson r heatmap + co-movement scatter
16  Compositional Bearing Scope (CBS) — three orthogonal faces
17  Pairwise divergence — distance matrix + top-15 ranking
18  ω vs Hs scatter
19  Stage 2 numeric summary
```

Page count = 19 regardless of T or D. Plate order is fixed; viewers
should not re-order. Footer on every page declares method tag and
order. Page 1 and 19 carry the source SHA, content SHA, and engine
version explicitly.

---

## 5 — Output format

A single PDF document, landscape Letter (11 × 8.5 inch).
Provenance footer on every page. Same FIXED-scale conventions as
Stage 1.

The matplotlib backend embeds a creation timestamp in PDF metadata,
so the PDF SHA-256 is not byte-deterministic across runs. The
underlying CNT JSON `content_sha256` is. v1.1 Feature A
(deterministic PDF backend) closes that gap.

---

## 6 — Determinism

Stage 2 is a pure function of the input JSON. Same JSON ⇒ same
plates, same numeric values to within IEEE float printing precision.
The matplotlib float-formatting uses default precision for tick
labels; the underlying data is not affected.

---

## 7 — Calibration fixture

`atlas/STANDARD_CALIBRATION_stage2_*` contains a known trajectory whose
navigation metrics can be hand-verified:

* A 6-point straight-line trajectory in CLR space:
  course_directness = 1.000 exactly.
* A 7-point closed-loop trajectory returning to origin:
  V_net = 0, course_directness = 0.

Re-running `atlas/standard_calibration_stage2.py` regenerates both
fixtures byte-identically.

---

*Stage 2 reads. The expert decides. The navigation metrics are
mathematically deterministic. The plates carry their order on every
page.*



---

# Part I — CNT vs classical CoDa (a side-by-side balance)


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



---

# Part J — Glossary


## Native units (v1.1 feature, reserved in v1.0)

The package uses a canonical neper basis for all log-ratio quantities,
but the user can declare the input data's native unit for reporting
and scale-factor disclosure on the project card.

**neper (Np)** — Natural-log ratio unit. 1 neper is the log of e/1.
The canonical basis for all Aitchison-geometric quantities. The
Higgins scale H_s defaults to nepers when reported in absolute (not
normalised) form.

**nat** — Synonym for neper in information-theory contexts.
1 nat = 1 neper. Shannon entropy expressed in nats uses ln (rather
than log_2).

**bit** — Base-2 log ratio unit. 1 bit = ln(2) nepers ≈ 0.6931 nepers.
Shannon entropy expressed in bits uses log_2.

**decibel (dB)** — Base-10 log ratio unit, scaled.
* 1 dB_power     = ln(10)/10 nepers  ≈ 0.2303 nepers
* 1 dB_amplitude = ln(10)/20 nepers  ≈ 0.1151 nepers

Used in audio, acoustics, signal-processing.

**ratio** — Pure dimensionless ratio. Default INPUT_UNITS for the
CNT engine: input data is treated as proportional mass / count /
energy and closed to the simplex without unit declaration.

**percent (%)** — A ratio scaled by 100. Closure handles this
correctly; the engine sees it as ratio after closure.

**absolute** — Mass / energy / count without proportional meaning.
Useful when the engine should report scale invariants explicitly.

The user declares INPUT_UNITS in the cnt.py USER CONFIG block. The
HIGGINS_SCALE_UNITS option chooses whether the H_s axis reports in
nepers, bits, or dB. The conversion factor is recorded on the
project card. **The display layout never changes**; only the unit
labels and the metadata declaration adjust. See
`atlas/V1.1_FEATURE_MENU.md` Feature B for the full design.

---

## Acronyms

**AME2020** — Atomic Mass Evaluation 2020. IAEA-AMDC reference for
nuclear binding energies. Used for the `nuclear_semf` reference
experiment.

**CLR** — Centred Log-Ratio transform. Maps a composition to the
linear subspace of R^D where coordinates sum to zero. clr(x)_j =
ln(x_j / g(x)) where g(x) is the geometric mean.

**CNT** — Compositional Navigation Tensor. The collection of
per-timestep tensor quantities (bearings θ, angular velocity ω,
steering metric κ, helmsman σ, Higgins scale H_s) computed by the
engine.

**CoDa** — Compositional Data Analysis. The mathematical framework
for analysing data on the simplex.

**EITT** — Entropy-Invariant Trajectory Test. An empirical signal
of trajectory smoothness — decimate by factor M, measure mean
Shannon entropy of decimated blocks, expect variation under the
gate. Egozcue's empirical observation, NOT an Aitchison-geometric
theorem.

**EMBER** — EMBER Climate, the energy think-tank publishing
electricity-generation data. Used for the eight country
experiments and the world aggregate.

**FAO** — UN Food and Agriculture Organisation. Source of the
Aquastat irrigation database used for `fao_irrigation_methods`.

**HCI** — Higgins Computation Instruments. The family of tools
this package implements: cnt (engine), atlas (viewer), mission
command (orchestrator).

**HUF** — Higgins Unity Framework. The umbrella mathematical
framework of which CNT is the navigational sub-component.

**IEEE floor** — IEEE 754 double-precision floating-point's
representation limit, approximately 1e-15 to 1e-16 for unit-order
quantities.

**ILR** — Isometric Log-Ratio transform. Maps the simplex to
R^(D-1) using an orthonormal basis (typically Helmert) of the CLR
subspace.

**IR** — Information Recovery (classification). The single class
the engine reports for the simplex's response to perturbation.

**JSON** — JavaScript Object Notation. The package's canonical
output format.

**MORB** — Mid-Ocean Ridge Basalt. Stracke 2022 sister dataset to
the Ball compilation.

**OIB** — Ocean Island Basalt. Companion to MORB in the Stracke
template.

**SEMF** — Semi-Empirical Mass Formula. The volume / surface /
Coulomb / asymmetry / pairing decomposition of nuclear binding
energy.

**SMART** — Self-Monitoring, Analysis, and Reporting Technology.
Hard-drive sensor data; the BackBlaze fleet uses SMART logs as the
raw input.

**TAS** — Total-Alkali-Silica. Le Bas 1986 rock-type
classification used for one of the Ball binnings.

## Constants

**A (amplitude)** — The bearing-amplitude of the period-2
attractor: |c_even − c_odd| in normalised units. Bounded in
practice to [0, 1] (the Higgins scale).

**c_even, c_odd** — The two convergence values of the period-2
attractor on the curvature tower.

**δ (DEFAULT_DELTA)** — Multiplicative zero-replacement floor.
Default 1e-15. Configurable.

**EITT_GATE_PCT** — Pass / fail gate for the EITT M-sweep. Default
5.0%. Configurable.

**ζ (zeta)** — Damping coefficient. ζ = -ln(A_final / A_initial) /
depth_delta. Bounded in practice to [0, 2].

**g(x)** — Geometric mean of a composition: (∏ x_k)^(1/D).

**H_s (Higgins scale)** — Normalised Shannon entropy on [0, 1].
H_s = H(x) / ln(D).

**κ (kappa)** — Steering metric. The off-diagonal entries of the
inverse Aitchison metric tensor at a composition.

**LOCK_CLR_THRESHOLD** — When a carrier's CLR drops below this
value, a LOCK-ACQ event is recorded. Default −10.0.

**M (in EITT)** — Decimation factor for the M-sweep test.

**M (in M²=I)** — The metric dual involution: M(x)_j = (1/x_j) /
Σ(1/x_k).

**ω (omega)** — Angular velocity in degrees, computed in ILR
coordinates.

**σ (helmsman)** — The carrier whose log-ratio drives the largest
contribution to the directional change at a level.

**θ (bearing)** — The pairwise log-ratio direction in the
Aitchison geometry.

## Concepts

**Aitchison distance** — The intrinsic distance on the simplex.

**Banach contraction** — Property satisfied if the mean contraction
ratio across the curvature recursion levels is < 1. A contracting
map's iterates converge.

**bridges** — The middle layer in the schema: cross-block
quantities like information theory, dynamical systems, and control
theory derived from the tensor block.

**carrier** — A column of the input CSV after the label column. A
component of the composition.

**closure** — The operation C(x) that scales a vector to sum to a
constant total (canonically 1).

**composition** — A vector carrying only relative (proportional)
information.

**content_sha256** — The SHA-256 of the canonical JSON content. The
authoritative determinism receipt.

**curvature tower** — The recursive depth sounder iterating on
log-ratio variances.

**decimation** — The atlas tour-plate compression strategy when
the user budget is below the full-detail count.

**determinism gate** — A test that runs the engine against the
reference experiments and verifies SHAs match published values.

**energy tower** — The recursive depth sounder iterating on
Higgins-scale entropy.

**helmsman lineage** — The sequence of helmsmen across recursion
levels. When a single carrier persists across many levels, the
system is dominantly steered by that axis.

**Helmert basis** — A specific orthonormal basis of the CLR
subspace, due to Egozcue. The ILR coordinates are the Helmert
projection.

**Higgins decomposition (Hˢ)** — The recursive depth-tower analysis
of a compositional trajectory.

**Higgins scale** — Normalised Shannon entropy on [0, 1].

**impulse response** — How the simplex absorbs perturbations,
summarised by amplitude A, damping ζ, and the IR classification.

**involution proof** — Numerical verification that M(M(x)) = x.

**lock event** — A LOCK-ACQ recorded when a carrier's CLR drops
below `LOCK_CLR_THRESHOLD` (the carrier has effectively reached
the boundary).

**period-2 attractor** — A limit cycle of length 2 on the curvature
tower. The defining feature exposed by the depth sounder.

**pre-parser / adapter** — Code that converts raw third-party data
into an ingestible CSV.

**simplex** — The set of D-tuples of non-negative reals summing to
a constant. The natural domain of compositional data.

**subcomposition** — What you get when you select some carriers
and re-close the remainder.

**tensor block** — The Stage-1 per-timestep numerical core: every
(θ, ω, κ, σ, H_s) computed for every record.

**timestep** — A single record in the trajectory. May be a
literal time index (year, day) or any meaningful ordering label.

**tour plate** — A 2D projection of the trajectory at a single
timestep. The atlas emits xy / xz / yz views per rendered frame.

**triadic enumeration** — The Stage-3 enumeration of C(T, 3)
day-triads for the cross-temporal correlation analysis.

## Versions

| Component | Version |
|---|---|
| Schema      | 2.0.0 |
| Engine      | cnt 2.0.3 (Python and R) |
| Atlas       | 1.0.0 (Phase B) |
| Mission Command | 1.0.0 |
| C


---

*The instrument reads. The expert decides. The hashes carry the receipts.*
