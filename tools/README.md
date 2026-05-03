# Hˢ Tools Library

**Hˢ = R ∘ M ∘ E ∘ C ∘ T ∘ V ∘ S** — Seven operators. One composition. One deterministic reading.

This directory contains every runnable tool in the Higgins Decomposition system: the Python pipeline that performs the 12-step analysis, the interactive HTML visualizations, and the Jupyter notebooks that tie it all together. Everything here reads compositional structure — it does not create or destroy it.

---

## Quick Start

| I want to... | Use this |
|---|---|
| Run Hˢ on my data right now | [Hs_Standards_Edition.ipynb](Hs_Standards_Edition.ipynb) — open in JupyterLab, Run All, upload CSV |
| Explore results visually | [Hs_Dashboard.ipynb](Hs_Dashboard.ipynb) — 6-panel dashboard with existing pipeline output |
| See the spectrum analyzer | [Hs_Spectrum_Analyzer.html](interactive/Hs_Spectrum_Analyzer.html) — interactive frequency-domain viewer |
| Browse the cosmic energy budget | [cosmic_composition_interactive.html](interactive/cosmic_composition_interactive.html) — Planck 2018 slider |
| Run the pipeline from Python | `from higgins_decomposition_12step import HigginsDecomposition` — see [pipeline/](pipeline/) |

---

## Pipeline — 13 Python Files

The core engine. Requires only `numpy`. Every file begins with `hs_` except the two founding instruments.

| File | Lines | Purpose |
|---|---|---|
| [higgins_decomposition_12step.py](pipeline/higgins_decomposition_12step.py) | ~2,400 | **The instrument.** 12-step decomposition: closure → CLR → variance trajectory → HVLD shape → squeeze → entropy → chaos → ternary → complex → polar. Outputs a complete result dict. |
| [hs_codes.py](pipeline/hs_codes.py) | ~800 | **Diagnostic codes.** 78 codes across 10 structural modes (LOCK, DRIFT, SQUEEZE, EXPAND, CHAOS, BIFURCATION, ENTROPY, SYMMETRY, COMPLEX, POLAR). Reads a result dict and emits investigation prompts. |
| [hs_reporter.py](pipeline/hs_reporter.py) | ~600 | **Multilingual reporter.** Generates human-readable diagnostic reports in 5 languages (en, pt, it, zh, hi). Each code becomes a sentence with context. |
| [hs_controller.py](pipeline/hs_controller.py) | ~1,200 | **State machine controller.** Hˢ-GOV supervisory layer with breakpoints, tolerance gates, and audit trail. Runs multiple experiments under governance. |
| [hs_sensitivity.py](pipeline/hs_sensitivity.py) | ~700 | **Component Power Mapper.** Identifies which carrier drives the most variance through leverage, criticality, transfer entropy, and synergy scores. |
| [hs_amalgamation.py](pipeline/hs_amalgamation.py) | ~750 | **Subcompositional Recursion.** Tests whether the classification survives when carriers are merged — the T2 stability test. Black hole / white hole duality mapping. |
| [hs_fingerprint.py](pipeline/hs_fingerprint.py) | ~500 | **Compositional Fingerprint.** Generates a unique geometric identity hash for any system — comparable across domains. |
| [hs_audit.py](pipeline/hs_audit.py) | ~400 | **Audit trail.** Immutable logging of every pipeline step with timestamps, hashes, and governance state. |
| [hs_ingest.py](pipeline/hs_ingest.py) | ~350 | **Data ingest.** Reads CSV/JSON, validates compositional constraints (closure, positivity), applies zero replacement. |
| [hs_metrology.py](pipeline/hs_metrology.py) | ~300 | **Instrument metrology.** Precision bounds, resolution limits, and uncertainty propagation for the decomposition. |
| [hs_testgen.py](pipeline/hs_testgen.py) | ~250 | **Test generator.** Creates synthetic compositional datasets with known properties for validation and calibration. |
| [hs_hepdata.py](pipeline/hs_hepdata.py) | ~200 | **HEPData bridge.** Fetches and ingests particle physics data from the HEPData repository for Hˢ analysis. |
| [higgins_transcendental_pretest.py](pipeline/higgins_transcendental_pretest.py) | ~400 | **Transcendental pretest.** Pre-screens variance trajectories against the constant library before the full squeeze test. |

**Locale files** in [pipeline/locales/](pipeline/locales/): `en.json`, `pt.json`, `it.json`, `zh.json`, `hi.json` — translation dictionaries for the multilingual reporter.

---

## Interactive HTML Tools — 9 Visualizations

Open any of these directly in a browser. No server required. No dependencies.

| Tool | What it does |
|---|---|
| [Hs_Spectrum_Analyzer.html](interactive/Hs_Spectrum_Analyzer.html) | Load pipeline JSON output and explore the frequency-domain structure. Spectral decomposition viewer with Hˢ-GOV KNOB-001 standard controls. |
| [Hs_CoDaWork_Demo.html](interactive/Hs_CoDaWork_Demo.html) | Conference demonstration — walks through the decomposition step by step with built-in example data. |
| [EXP-19_Fourier_Conjugate_Preservation_Theorem.html](interactive/EXP-19_Fourier_Conjugate_Preservation_Theorem.html) | Interactive proof that the Fourier conjugate structure is preserved through the Hˢ pipeline. Drag sliders to test any composition. |
| [EXP-19_Interactive_Simulator.html](interactive/EXP-19_Interactive_Simulator.html) | Real-time simulator for Experiment 19 — Fourier conjugate pairs on the simplex. |
| [EXP16_Interactive_Simulator.html](interactive/EXP16_Interactive_Simulator.html) | Planck cosmic energy budget simulator — drag carrier proportions and watch the decomposition respond. |
| [cosmic_composition_interactive.html](interactive/cosmic_composition_interactive.html) | Planck 2018 ΛCDM cosmic budget as interactive sliders — dark energy, dark matter, baryonic matter, radiation, neutrinos. |
| [cosmic_cone_5min_loop.html](interactive/cosmic_cone_5min_loop.html) | Looping animation of the cosmic inflation cone — 5-minute cycle showing the universe's compositional evolution. |
| [cosmic_duality_dance.html](interactive/cosmic_duality_dance.html) | Black hole / white hole duality visualization — the compositional attractor/repeller dance with diagnostic code overlay. |
| [cosmic_future_projection.html](interactive/cosmic_future_projection.html) | Dark energy dominance projection — traces the cosmic composition forward to heat death at 10¹⁰⁰ years. |

---

## Jupyter Notebooks — 3

| Notebook | Cells | Purpose |
|---|---|---|
| [Hs_Standards_Edition.ipynb](Hs_Standards_Edition.ipynb) | 18 | **The conference handout.** Complete self-contained system. Auto-installs dependencies, auto-fetches pipeline from GitHub, includes 3 reference standards (Nuclear SEMF, Simple 3-carrier, Planck Cosmic), interactive CSV upload, full pipeline + all advanced analyses, saves results as JSON. Open in JupyterLab, Run All, done. |
| [Hs_Dashboard.ipynb](Hs_Dashboard.ipynb) | 11 | **6-panel dashboard.** Variance trajectory, entropy evolution, CLR spread, HVLD shape fit, squeeze test, and ternary diagram. Requires local pipeline directory. |
| [papers/codawork2026/Hs_Standards_Edition.ipynb](../papers/codawork2026/Hs_Standards_Edition.ipynb) | 18 | Conference copy of the Standards Edition — identical content, positioned for CoDaWork 2026 distribution. |

---

## Experiment Registry — 25 Experiments Across 18 Domains

Every experiment follows the same pattern: raw data → Hˢ pipeline → result JSON → diagnostic reports in 5 languages. Each folder in [experiments/](../experiments/) contains the full audit trail.

### Physical Sciences

| ID | Name | Domain | D | N | Closest Constant | δ |
|---|---|---|---|---|---|---|
| [Hs-01](../experiments/Hs-01_Gold_Silver/) | Gold / Silver Price Ratio | COMMODITIES | 2 | 624 | 1/π | 3.27×10⁻⁵ |
| [Hs-03](../experiments/Hs-03_Nuclear_SEMF/) | Nuclear SEMF | NUCLEAR | 3 | 92 | 1/(π^e) | 5.87×10⁻⁶ |
| [Hs-04](../experiments/Hs-04_Bessel_Acoustics/) | Bessel Acoustics | ACOUSTICS | 3 | 200 | 1/π | 2.00×10⁻⁵ |
| [Hs-05](../experiments/Hs-05_Geochemistry/) | Geochemistry | GEOCHEMISTRY | 3 | 150 | 1/(e^π) | 1.13×10⁻⁴ |
| [Hs-06](../experiments/Hs-06_Fusion/) | Fusion | NUCLEAR | 3 | 100 | 1/(π^e) | 5.74×10⁻³ |
| [Hs-11](../experiments/Hs-11_AME2020/) | AME2020 Nuclear Masses | NUCLEAR | 3 | 500 | 1/(π^e) | 9.88×10⁻³ |
| [Hs-12](../experiments/Hs-12_Spring_Mass/) | Spring-Mass System | FORCE | 3 | 200 | 1/(π^e) | 4.50×10⁻⁴ |
| [Hs-13](../experiments/Hs-13_Steel/) | Steel Composition | MATTER | 3 | 80 | ln(φ) | 1.49×10⁻⁴ |
| [Hs-15](../experiments/Hs-15_hBN_Dielectric/) | hBN Dielectric | MATERIALS | 3 | 200 | 1/(2π) | 2.86×10⁻⁵ |

### Particle Physics and Cosmology

| ID | Name | Domain | D | N | Closest Constant | δ |
|---|---|---|---|---|---|---|
| [Hs-07](../experiments/Hs-07_QCD/) | QCD Coupling | QCD | 3 | 20 | ln(φ) | 3.92×10⁻³ |
| [Hs-08](../experiments/Hs-08_CKM_PMNS/) | CKM / PMNS Matrices | PARTICLE | 3 | 11 | 1/(2π) | 7.74×10⁻³ |
| [Hs-10](../experiments/Hs-10_GW150914/) | Gravitational Wave GW150914 | GRAVITY | 3 | 40 | 1/φ | 9.08×10⁻⁴ |
| [Hs-16](../experiments/Hs-16_Planck_Cosmic/) | Planck Cosmic Budget | COSMOLOGY | 3 | 200 | 1/(e^π) | 3.77×10⁻⁵ |
| [Hs-23](../experiments/Hs-23_Radionuclides/) | Radionuclide Decay Chains | NUCLEAR | 4 | — | 1/(e^π) | 7.78×10⁻³ |
| [Hs-25](../experiments/Hs-25_Cosmic_Energy_Budget/) | Cosmic Energy Budget (5-carrier) | COSMOLOGY | 5 | 103 | 1/(e^π) | 4.19×10⁻⁵ |

### Astrophysics and Signals

| ID | Name | Domain | D | N | Closest Constant | δ |
|---|---|---|---|---|---|---|
| [Hs-02](../experiments/Hs-02_US_Energy/) | US Energy Mix | ENERGY | 3 | 25 | 1/(e^π) | 4.35×10⁻⁴ |
| [Hs-09](../experiments/Hs-09_Stellar/) | Stellar Nucleosynthesis | ASTROPHYSICS | 3 | 30 | Dottie | 3.08×10⁻⁴ |
| [Hs-14](../experiments/Hs-14_Conjugate_Pairs/) | Conjugate Pairs | SIGNAL THEORY | 3 | 200 | 1/√3 | 5.79×10⁻⁴ |

### Engineering and Urban Systems

| ID | Name | Domain | D | N | Closest Constant | δ |
|---|---|---|---|---|---|---|
| [Hs-17](../experiments/Hs-17_Backblaze/) | Backblaze Hard Drive Fleet | ENGINEERING | 3 | 34 | — | — |
| [Hs-18](../experiments/Hs-18_Urban_Markham/) | Urban Land Use (Markham) | URBAN | 3 | 31 | ln(φ) | 5.01×10⁻⁵ |
| [Hs-19](../experiments/Hs-19_Traffic_Signals/) | Traffic Signal Timing | URBAN | 3 | 831 | γ (Euler) | 2.61×10⁻³ |

### Meta-Experiments and AI

| ID | Name | Domain | D | N | Closest Constant | δ |
|---|---|---|---|---|---|---|
| [Hs-20](../experiments/Hs-20_Conversation_Drift/) | AI Conversation Drift | AI SAFETY | 4 | 18 | 1/(2π) | 1.97×10⁻⁴ |

### Methodology Experiments

| ID | Name | Purpose |
|---|---|---|
| [Hs-21](../experiments/Hs-21_Reference_Standards/) | Reference Standards Library | Establishes the canonical reference standard set for calibration |
| [Hs-22](../experiments/Hs-22_Natural_Pairs/) | Natural Pairs Baseline | Maps the natural pair structure across 7 pair families (14 sub-experiments) |
| [Hs-24](../experiments/Hs-24_HEPData_Validation/) | HEPData Validation | Cross-validates pipeline against HEPData particle physics repository |

---

## How It All Connects

```
Your CSV data
     │
     ▼
┌──────────────────────┐
│  hs_ingest.py        │ ← validates, closes to simplex
│  hs_metrology.py     │ ← checks precision bounds
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  higgins_             │
│  decomposition_       │ ← THE 12 STEPS
│  12step.py            │    R ∘ M ∘ E ∘ C ∘ T ∘ V ∘ S
└──────────┬───────────┘
           ▼
    ┌──────┼──────┐
    ▼      ▼      ▼
 hs_codes  hs_    hs_
 .py       reporter fingerprint
    │      .py     .py
    ▼      ▼      ▼
 78 codes  5-lang  geometric
 10 modes  reports identity
    │
    ├──► hs_sensitivity.py  → Component Power Map
    ├──► hs_amalgamation.py → Subcompositional Stability
    └──► hs_controller.py   → Hˢ-GOV supervised batch runs
              │
              ▼
         hs_audit.py → immutable audit trail
```

---

## Site Boundary

This repository is the **mathematical fixture** — the proven, validated, stable instrument. It contains the decomposition, the experiments that validate it, and the theory that grounds it.

Applications of Hˢ to new domains, industry integrations, and production tooling belong in a separate applications repository. This site grows slowly and deliberately; the applications site can move fast.

What stays here: the 12-step pipeline, the diagnostic codes, the constant library, the experiment archive, the theory documents, and the governance framework.

What goes elsewhere: domain-specific adapters, API wrappers, GUI applications, cloud deployments, and anything that uses Hˢ without extending the mathematics.

---

*Peter Higgins — Rogue Wave Audio*
*github.com/PeterHiggins19/higgins-decomposition*
*License: CC BY 4.0*
