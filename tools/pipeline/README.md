# Hs Pipeline -- Core Decomposition Engine

The Hs (Higgins Decomposition) pipeline performs the canonical decomposition
**Hs = R . M . E . C . T . V . S** on compositional data -- data that lives
on the Aitchison simplex. Twenty-four Python files (~16,500 lines) implement a
deterministic 12-step instrument with extended diagnostics, governance,
audit, multilingual reporting, and unified standard I/O.

**Dependency:** NumPy only. No other packages required.

---

## Quick Start

```python
import numpy as np
from higgins_decomposition_12step import HigginsDecomposition

# Define system and load data
hd = HigginsDecomposition(
    "MY-01", "Gold/Silver Ratio", "COMMODITIES",
    carriers=["Gold", "Silver"]
)
data = np.array([[0.6, 0.4], [0.55, 0.45], [0.7, 0.3]])
hd.load_data(data)
hd.run_full_pipeline()

# Inspect results
print(hd.results["step6_pll_shape"])        # HVLD shape classification
print(hd.results["step7_squeeze_closest"])  # Closest transcendental constant
```

Or use the **Standard I/O** runner for complete output (pipeline + all projections):

```bash
python hs_run.py mydata.csv
python hs_run.py mydata.csv --exp-id "Hs-M03" --name "My System" --domain "GEOLOGY"
python hs_run.py mydata.csv --output results/ --all-languages
```

For pipeline-only (no projections):

```bash
python hs_ingest.py mydata.csv
python hs_ingest.py mydata.csv --name "My System" --domain "GEOLOGY" --lang pt
```

---

## Files

| File | Purpose |
|------|---------|
| [higgins_decomposition_12step.py](higgins_decomposition_12step.py) | Main instrument -- 12-step pipeline runner (define, identify, load, close, CLR, Aitchison variance, HVLD, super squeeze, EITT entropy, ternary, complex plane, helix/polar) |
| [hs_codes.py](hs_codes.py) | 78 diagnostic codes across 10 structural modes. Code format: `SS-CCC-LLL` (stage-condition-level) |
| [hs_reporter.py](hs_reporter.py) | Multilingual report generator -- reads diagnostic codes and produces human-readable output in 5 languages |
| [hs_controller.py](hs_controller.py) | Hs-GOV state machine controller (IDLE / RUNNING / HELD / COMPLETED / ABORTED / ERROR) for industrial embedding |
| [hs_sensitivity.py](hs_sensitivity.py) | Component Power Mapper -- measures carrier influence on system character, not just mass fraction (CLI, PBM, CPS analyses) |
| [hs_amalgamation.py](hs_amalgamation.py) | Subcompositional Recursion Engine (T2 test) -- regroups carriers into every subcomposition, maps attractor/repeller persistence |
| [hs_fingerprint.py](hs_fingerprint.py) | Compositional fingerprint generator -- deterministic signature for cross-system comparison |
| [hs_audit.py](hs_audit.py) | Audit trail and breakpoint system -- ISO 17025-grade chain-of-custody traceability for every pipeline operation |
| [hs_run.py](hs_run.py) | **STANDARD I/O** Unified pipeline runner -- one command, data in, complete science out. Chains ingest → pipeline → all 4 mandatory projections + JSON + reports |
| [hs_ingest.py](hs_ingest.py) | Universal data ingest -- accepts CSV, TSV, JSON, or .npy, auto-detects closure and zero replacement |
| [hs_metrology.py](hs_metrology.py) | Instrument metrology -- evaluates the pipeline itself (code coverage, dynamic range, noise floor, cross-domain coherence) |
| [hs_testgen.py](hs_testgen.py) | Secondary test tools generator -- builds regression suites, health checks, stability tests, and operating-envelope probes |
| [hs_hepdata.py](hs_hepdata.py) | HEPData bridge -- fetches compositional data from hepdata.net and converts to pipeline-ready CSV |
| [higgins_transcendental_pretest.py](higgins_transcendental_pretest.py) | Transcendental constant prescreen -- rapid classifier using the 35-constant library (NATURAL / INVESTIGATE / FLAG) |
| [hs_helix_exploded.py](hs_helix_exploded.py) | Exploded helix PDF -- 1-page bill-of-materials showing 10 pipeline layers as 3D helix with callout tags |
| [hs_manifold_helix.py](hs_manifold_helix.py) | Manifold helix PDF -- 1-page isometric projection of the real CLR trajectory with ground shadow and waypoints |
| [hs_manifold_projections.py](hs_manifold_projections.py) | **MANDATORY** Projection suite PDF -- 4-page orthographic (front, side, plan) + polar plot. The standard output method for all experiments |
| [hs_polar_stack.py](hs_polar_stack.py) | **MANDATORY** Polar stack PDF -- per-interval polar radar projections. One D-dimensional fingerprint per data level, plus helix slice map and summary comparison |
| [hs_manifold_paper.py](hs_manifold_paper.py) | Manifold on Paper PDF -- 3D polar slice stack in projected space. The HTML manifold projector, on paper. 3 pages: optimal-angle manifold, three-panel (front/3-4/plan), carrier trace separation |
| [hs_projector_export.py](hs_projector_export.py) | Manifold projector JSON export -- generates data for interactive HTML manifold projectors |
| [balun_matrix_analysis.py](balun_matrix_analysis.py) | Balun V(t) matrix analysis -- eigenstructure, commutators, norms, correlations |
| [impedance_bridge.py](impedance_bridge.py) | Impedance bridge matrix -- CLR/ILR/ALR x T/C/E match exhaustion |
| [tr_basis_experiment.py](tr_basis_experiment.py) | Trace basis experiment -- Tr x basis x representation exhaustion with step/operation tags |

---

## Mandatory Outputs (as of 2026-04-30)

Every pipeline run **must** generate the following paper-quality PDF outputs:

1. **Exploded Helix** (`hs_helix_exploded.py`) -- bill of materials, what the pipeline measured
2. **Manifold Helix** (`hs_manifold_helix.py`) -- isometric 3D trajectory, the map
3. **Projection Suite** (`hs_manifold_projections.py`) -- 4-page orthographic + polar, the rulers
4. **Polar Stack** (`hs_polar_stack.py`) -- per-interval polar cross-sections, the slices
5. **Manifold on Paper** (`hs_manifold_paper.py`) -- 3D manifold in projected space, the HTML projector on paper

The 3D helix is the plan map. The projection suite gives the rulers. The polar stack gives the cross-sections at each data level. The manifold paper stacks those cross-sections in 3D projected space to reveal the manifold shape without needing a browser. Together they provide complete geometric characterisation. Reference handbook: `docs/Hs_Projection_Atlas.docx`

---

## Locales

The [locales/](locales/) directory contains translation files for the multilingual reporter:

| File | Language |
|------|----------|
| [en.json](locales/en.json) | English |
| [pt.json](locales/pt.json) | Portuguese |
| [it.json](locales/it.json) | Italian |
| [zh.json](locales/zh.json) | Mandarin Chinese |
| [hi.json](locales/hi.json) | Hindi |

Adding a new language requires only a new JSON file -- zero code changes.

---

## Pipeline Steps

1. Define system (name, domain, carriers)
2. Identify carriers (D parts, labels)
3. Load/simulate data -- raw matrix (N x D)
4. Close to simplex (row sums = 1, zero replacement)
5. CLR transform (centered log-ratio)
6. Aitchison variance trajectory
7. HVLD vertex lock (Higgins Vertex Lock Diagnostic)
8. Super squeeze (transcendental constant proximity)
9. EITT entropy (Shannon H on simplex, invariance test)
10. Ternary projection (D=3 barycentric coordinates)
11. Complex plane (centroid-relative mapping)
12. 3D Helix / Polar (radius-angle-time embedding)

Repeated runs on identical data produce bit-identical results. The pipeline contains no stochastic elements.

---

## Diagnostic Codes

Codes follow the format `SS-CCC-LLL`:

- **SS** -- Stage (GD, S4--SC, XU, XC, RP)
- **CCC** -- Condition detected
- **LLL** -- Severity level (INF, WRN, ERR, DIS, CAL)

The 10 structural modes summarise system character from the full code set.

---

## Architecture

```
Hs-GOV  (governance / supervisory)
   |
   v
Controller  (state machine -- start, hold, resume, abort)
   |
   v
Pipeline  (12-step + extended -- deterministic analysis)
   |
   v
Audit Trail  (chain of custody -- every operation traced)
```

---

Peter Higgins / Rogue Wave Audio -- CC BY 4.0
