# CNT Engine — Single-Program Canonical JSON Generator

**Schema version:** 2.0.0
**Engine version:** 2.0.3 (Python); 2.0.2 (R port)
**Status:** Working. Verified on 20 datasets across the corpus
(Japan, Ball/Region, BackBlaze T=731, FAO 83 countries, Stracke MORB, etc.).
Determinism gate passes — same config + same input ⇒ same content_sha256;
different config ⇒ different content_sha256, recorded in
`metadata.engine_config`.

## Engine fix log within 2.0.x

| Engine | Fix |
|---|---|
| 2.0.0 | Initial schema-2 layout (coda_standard / higgins_extensions split) |
| 2.0.1 | Period-1 detection requires TWO consecutive convergences (was 1) — fixes false-positive early stop on USA EMBER and Ball/TAS |
| 2.0.1 | Curvature composition uses 1/x_j² (was 1/x_j) — matches Math Handbook Ch 19.2(b) |
| 2.0.1 | TRIADIC_T_LIMIT default lowered 1000 → 500 |
| 2.0.2 | USER CONFIGURATION block at top of source files; echoed in metadata.engine_config |
| 2.0.3 | IR taxonomy refinement (Python only): `DEGENERATE` split into `ENERGY_STABLE_FIXED_POINT`, `CURVATURE_VERTEX_FLAT`, `D2_DEGENERATE`. cnt.R remains at 2.0.2. |

This folder contains the CNT engine: one program, one canonical JSON,
one schema. Replaces the three-program path with a single, audited
entry point.

## Architecture

```
              CNT Engine (cnt.py | cnt.R)
                         |
                         ▼
               canonical CNT JSON  (the data store)
                         |
            ┌────────────┼────────────┬──────────┐
            ▼            ▼            ▼          ▼
         plates     projector    spectrum     future
                                  analyser     viewers
```

The engine produces the JSON. Every downstream tool reads only the
JSON. Future contributors can write their own diagnostic generators
against the schema document without ever touching the engine source.

## Two orthogonal classifications

Every analytic field carries two labels:

**Ownership** — `coda_standard/` (Aitchison/Egozcue/Pawlowsky-Glahn
lineage) or `higgins_extensions/` (HUF-framework readings of the same
simplex). A CoDa-community reviewer can read just `coda_standard/`
fields and audit the engine without engaging Higgins-specific
machinery. Schema §8 documents that every Higgins extension is a
function of CoDa-standard quantities.

**Function** — the role each block plays:

| `_function`  | Role                                                        |
|--------------|-------------------------------------------------------------|
| `composer`   | Creates compositional structure (closure, CLR, ILR, …)      |
| `review`     | Analyses the composed structure (variation matrix, attractor)|
| `formatter`  | Prepares specific representations for display (atlas, ledger)|
| `provenance` | Identity, hashes, environment — neither computation nor display |

A viewer building a projector reads `composer` blocks. An analytical
report reader reads `review` blocks. A plate generator reads
`formatter` blocks.

## Files

| File                          | Purpose                                                         |
|-------------------------------|------------------------------------------------------------------|
| `CNT_JSON_SCHEMA.md`          | Authoritative schema document (v2.0.0). The contract.           |
| `CNT_PSEUDOCODE.md`           | Language-neutral algorithm reference.                            |
| `cnt.py`                      | Python reference implementation (canonical).                     |
| `cnt.R`                       | R reference implementation (parity port).                        |
| `parity_test.py`              | Cross-language parity gate.                                      |
| `README.md`                   | This file.                                                       |
| `jpn_cnt.json`                | Japan EMBER reference output.                                    |
| `ball_regions_cnt.json`       | Ball/Region reference output.                                    |

## Usage

### Python

```bash
python3 cnt.py input.csv -o output.json --temporal --ordering-method by-time
```

For non-temporal data:

```bash
python3 cnt.py input.csv -o output.json --ordering-method by-label \
    --ordering-caveat "Region barycenters; not temporal"
```

### R

```bash
Rscript cnt.R input.csv output.json --temporal --ordering-method by-time
```

R requirements (one-time):

```r
install.packages(c("jsonlite", "digest"))
```

### Programmatic (Python)

```python
from cnt import cnt_run
j = cnt_run("input.csv", "output.json",
            ordering={"is_temporal": True,
                      "ordering_method": "by-time", "caveat": None})

# Read CoDa-only fields:
for ts in j["tensor"]["timesteps"]:
    print(ts["coda_standard"]["clr"])

# Read Higgins-specific fields:
print(j["depth"]["higgins_extensions"]["curvature_attractor"]["amplitude"])
```

### Programmatic (R)

```r
source("cnt.R")
j <- cnt_run("input.csv", "output.json",
             ordering = list(is_temporal = TRUE,
                              ordering_method = "by-time",
                              caveat = NULL))

# CoDa fields per timestep:
sapply(j$tensor$timesteps, function(ts) ts$coda_standard$shannon_entropy)
```

## CSV format

First column = label (year, region, sample id). Remaining columns = D
carriers (compositional parts). All values must be positive (zeros are
replaced with 1e-15 and counted).

Example (Japan EMBER, D=8):

```csv
Year,Bioenergy,Coal,Gas,Hydro,Nuclear,Other Fossil,Solar,Wind
2000,16.11,238.24,258.5,84.47,319.12,182.78,0.34,0.11
2001,16.03,253.91,256.52,81.54,320.54,153.85,0.5,0.25
...
```

## What the engine computes

The JSON has seven top-level blocks. Every analytic block declares
`_function` and contains `coda_standard/` and `higgins_extensions/`
sub-blocks (one of which may be `{}` when a block is single-ownership).

### Per-record state — `tensor/` (composer)

Every record gets:

* `coda_standard.{composition, clr, ilr, shannon_entropy, aitchison_norm}`
* `coda_standard.aitchison_distance_step` (i ≥ 1)
* `higgins_extensions.{higgins_scale, bearing_tensor, metric_tensor,
  metric_tensor_diagonal, condition_number}`
* `higgins_extensions.{angular_velocity_deg, helmsman, helmsman_delta}` (i ≥ 1)

### Stage 1 — `stages/stage1/` (formatter)

CBS plate display preparation. Wholly Higgins
(`section_atlas`, `metric_ledger`).

### Stage 2 — `stages/stage2/` (review)

* `coda_standard.variation_matrix` — Aitchison τ_ij = var(ln(x_i/x_j))
* `higgins_extensions.carrier_pair_examination` — bearing locks, pearson r,
  co/opposition scores

### Stage 3 — `stages/stage3/` (review)

* `coda_standard.subcomposition_ladder` — degree-k subcompositional analysis
* `higgins_extensions.{triadic_area, carrier_triads, regime_detection}`

### Bridges — `bridges/` (review)

* `coda_standard.information_theory` — entropy series, Fisher,
  KL divergence, mutual info, entropy rate
* `higgins_extensions.{dynamical_systems, control_theory}` — per-carrier
  Lyapunov, AR(1) state-space, recurrence

### Depth — `depth/` (review, all Higgins)

* `higgins_extensions.{involution_proof, level_0, energy_tower,
  curvature_tower, curvature_attractor, impulse_response, summary,
  energy_cycle, curvature_cycle}`

### Diagnostics — `diagnostics/` (review, all Higgins)

* `higgins_extensions.{eitt_residuals, lock_events, degeneracy_flags}`
* `content_sha256` — at the diagnostics top level (outside both sub-blocks)

## Verification

Tests during initial implementation:

* **Math correctness** — Japan curvature trajectory matches the
  reference engine exactly to 12+ decimal places across 14 levels.
* **Determinism** — Two consecutive runs produce identical
  `diagnostics.content_sha256`. Helmsman ties broken alphabetically.
* **Cross-engine consistency** — `hs_mean` agrees to machine precision
  across tensor, depth, and stages blocks.
* **Lock events** — Japan 2014 nuclear shutdown automatically detected
  as a `LOCK-ACQ` event for carrier `Nuclear`.
* **EITT M-sweep** — Ball/Region at M=261 measured at 0.501 % (well
  under 5 % gate), reproducing the standalone bench-test result.

R↔Python parity testing requires R installation (`parity_test.py`).

## Schema version policy

| Bump  | Trigger                                                             |
|-------|---------------------------------------------------------------------|
| patch | Documentation/typo fix, no semantic change                         |
| minor | Add a new optional field; loosen allowed values                    |
| major | Add REQUIRED field; remove field; change type; tighten values; move a field between coda_standard / higgins_extensions; move between functional blocks |

A viewer declaring `min_schema_version: 2.0.0` works with all 2.x.x.

## Migration from v1.0.0

See `CNT_JSON_SCHEMA.md` §10 for the complete migration table. Every
v1.0.0 path moves to a v2.0.0 path under the new dual classification.
Old viewers must be updated to read fields from
`coda_standard/` or `higgins_extensions/` sub-blocks and to honour
`_function`.

## Status of outstanding concerns (from 2026-05-05 review)

| Concern | Status |
|---------|--------|
| A1 single-program merge   | DONE — one engine, one JSON                   |
| A2 schema documentation   | DONE — `CNT_JSON_SCHEMA.md` v2.0.0            |
| A3 input data hash        | DONE — `input.source_file_sha256` and `closed_data_sha256` |
| A4 ordering convention    | DONE — `input.ordering` REQUIRED              |
| B1 attractor metrics      | DONE — `depth.higgins_extensions.curvature_attractor`, `impulse_response` |
| B2 dual Lyapunov          | DONE — `bridges.higgins_extensions.dynamical_systems.per_carrier_lyapunov` vs `depth.higgins_extensions.curvature_attractor.contraction_lyapunov` |
| B3 EITT residuals         | DONE — `diagnostics.higgins_extensions.eitt_residuals` |
| B4 full κ_ij              | DONE — `tensor.timesteps[i].higgins_extensions.metric_tensor.matrix` |
| B5 lock events enumerated | DONE — `diagnostics.higgins_extensions.lock_events[]` |
| B6 environment provenance | DONE — `metadata.environment`                 |
| **CoDa/Higgins split**    | DONE — every analytic block has both sub-blocks |
| **Functional labeling**   | DONE — `_function` ∈ {composer, review, formatter, provenance} |
| **CoDa↔Higgins mapping**  | DONE — schema §8 documents the equations      |

The engine is the canonical JSON generator for the two-engine
architecture. It is ready for downstream viewer development.

---

*The instrument reads. The expert decides. The loop stays open.*
