# Hˢ — Higgins Decomposition on the Simplex

**Hˢ = R ∘ M ∘ E ∘ C ∘ T ∘ V ∘ S**

A deterministic compositional inference instrument operating within Aitchison geometry on the simplex. Seven operators — Simplex closure, Variance trajectory, Transcendental squeeze, Classification, Entropy test, Mode synthesis, and Report — compose into a single decomposition function derived from a single axiom: *same input, same output, always.*

Validated across 18 physical domains, 25 experiments, 53 devices under test, and 44 orders of magnitude. The instrument reads structure without creating or destroying it.

[![Validate Repository](https://github.com/PeterHiggins19/higgins-decomposition/actions/workflows/validate.yml/badge.svg)](https://github.com/PeterHiggins19/higgins-decomposition/actions/workflows/validate.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/license-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![HCI-CNT engine 2.0.4](https://img.shields.io/badge/HCI--CNT%20engine-2.0.4-1f4e79.svg)](HCI-CNT/)
[![HCI-CNT schema 2.1.0](https://img.shields.io/badge/HCI--CNT%20schema-2.1.0-1f4e79.svg)](HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md)
[![25 reference experiments](https://img.shields.io/badge/reference%20experiments-25-2ca02c.svg)](HCI-CNT/experiments/INDEX.json)
[![CodaWork 2026](https://img.shields.io/badge/CodaWork-2026-f0c020.svg)](HCI-CNT/conference_demo/)

*Peter Higgins — Independent Researcher, Markham, Ontario, Canada*
*Rogue Wave Audio — PeterHiggins@RogueWaveAudio.com*

---

## At a Glance

| Measure | Value |
|---|---|
| Physical domains | 18 |
| Experiments | 25 |
| Distinct systems | 36 |
| Devices under test (DUTs) | 53 |
| Pipeline files | 13 |
| Interactive tools | 9 |
| Diagnostic codes | 78 |
| Structural modes | 10 |
| Transcendental constants | 35 |
| Conjugate pairs validated | 13 |
| Reference standards | 15 |
| Languages | 5 (en, zh, hi, pt, it) |
| Scale range | 10⁻¹⁸ m to 10²⁶ m (44 orders of magnitude) |
| Framework version | 3.0 |
| Deterministic | Yes (Gauge R&R bit-identical, SHA-256 verified) |
| Instrument metrology | QUALIFIED (6/6 metrics pass) |
| License | CC BY 4.0 |

---

## Start Here

**If you are a person:** [Learning Path](docs/Hs_Learning_Path.md) → [Architecture Overview](docs/Hs_Architecture_Overview.md) → [Applications Guide](docs/Hs_Applications_Guide.md) → [High Index Platform](docs/Hs_High_Index_Platform_Guide.md)

**If you are a machine:** [`ai-refresh/HS_MACHINE_MANIFEST.json`](ai-refresh/HS_MACHINE_MANIFEST.json) — identity, navigation, protocol, governance, and authority resolution in a single file. Follow the onboarding sequence defined there.

**If you want to run Hs right now:** [Standards Edition Notebook](tools/Hs_Standards_Edition.ipynb) — self-contained Jupyter notebook, auto-installs dependencies, auto-fetches pipeline from GitHub, includes 3 built-in reference standards, runs all advanced analyses. The conference handout tool.

**If you are reviewing for CoDaWork 2026:** [Abstract (PDF)](papers/codawork2026/CoDaWork2026_Abstract_Higgins.pdf) → [Executive Summary](papers/codawork2026/Hs_CoDaWork2026_Executive_Summary.md) → [Standards Edition Notebook](papers/codawork2026/Hs_Standards_Edition.ipynb) → [Collaboration Path](papers/codawork2026/CoDaWork2026_Collaboration_Path.md)

---

## HCI-CNT — Compositional Navigation Tensor (active development line)

The `HCI-CNT/` subsystem extends Hˢ with the Compositional Navigation
Tensor (CNT) — a deterministic, hash-traceable instrument for
compositional time series and cross-sections. Engine 2.0.4 / Schema
2.1.0 / 25 reference experiments, all passing the determinism gate.

CNT shares Hˢ's foundations (Aitchison geometry, simplex closure,
*same input → same output → always*) and adds trajectory-native
operators (bearings, angular velocity, helmsman, period-2 attractor,
IR class), a four-stage paged report family, end-to-end hash
provenance, and cross-dataset inference reports.

Three handbook volumes in [`HCI-CNT/handbook/`](HCI-CNT/handbook/)
cover the system in full:

| Volume | Audience |
|---|---|
| [`VOLUME_1_THEORY_AND_MATHEMATICS.md`](HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md) | math, schema, doctrine, balance vs classical CoDa |
| [`VOLUME_2_PRACTITIONER_AND_OPERATIONS.md`](HCI-CNT/handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md) | engine, atlas, mission command, demo, ROI, integrations |
| [`VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md`](HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md) | determinism, hash chain, talk plan, public-trial readiness |

Quickstart: see [`HCI-CNT/README.md`](HCI-CNT/README.md).

Three CoDa-community preprint papers live at [`HCI-CNT/coda_community/`](HCI-CNT/coda_community/),
and the CodaWork 2026 demo package at [`HCI-CNT/conference_demo/`](HCI-CNT/conference_demo/)
is self-contained.

The previous standalone `HUF-CNT-System` package outside the Hˢ repo
is preserved as archived history. Active CNT development from this
point forward happens inside `HCI-CNT/`.

---

## Prime Documents

These are the governing documents of the Hˢ system — the ones that define what it is, what it does, and what it claims.

| Document | Purpose |
|---|---|
| [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) | Running log of all development, decisions, results, and principles |
| [Decomposition Function (v3.0)](docs/Hs_Decomposition_Function.md) | Formal derivation: axiom → decimation → seven operators → Hˢ |
| [Logic Map and State Machine](docs/Hs_Logic_Map_and_State_Machine.md) | Complete symbolic logic of the pipeline |
| [Symbolic Logic Definition](papers/codawork2026/Hs_Symbolic_Logic_Definition.md) | Pure mathematical definition — no prose |
| [Reference v3.0 (docx)](docs/reference/Higgins_Decomposition_Reference_v3.0.docx) | Formal reference document with full operator specifications |
| [Character Analysis (docx)](papers/flagship/Higgins_Decomposition_Character_Analysis.docx) | Atomic-level disassembly — the pipeline as DUT |
| [Instrument Metrology](docs/reference/Hs_Instrument_Metrology.json) | Quantified instrument qualification (6 metrics) |
| [Naming Convention](docs/Hs_Naming_Convention.md) | File naming rules, branding, and terminology migration |
| [CITATION.cff](CITATION.cff) | How to cite this work |

---

## The Pipeline (13 Files)

All code lives in `tools/pipeline/`. No external dependencies beyond numpy.

### Core Engine

| File | Role |
|---|---|
| `higgins_decomposition_12step.py` | The 12-step pipeline — simplex closure through helix projection |
| `higgins_transcendental_pretest.py` | Transcendental constant proximity against 35-constant library |
| `hs_amalgamation.py` | Subcompositional recursion engine — amalgamation stability testing |

### Diagnostics

| File | Role |
|---|---|
| `hs_codes.py` | 78 diagnostic codes + 10 structural modes |
| `hs_fingerprint.py` | Seven-dimensional compositional fingerprint generator + matcher |
| `hs_sensitivity.py` | Component Power Mapper — leverage, phase, power scores per carrier |
| `hs_metrology.py` | Instrument meta-evaluation — Gauge R&R, self-consistency |

### Ingestion

| File | Role |
|---|---|
| `hs_ingest.py` | Universal CSV/JSON loader — any composition, automatic closure |
| `hs_hepdata.py` | HEPData fetch — 8 curated HEP datasets with validated pipeline runs |

### Infrastructure

| File | Role |
|---|---|
| `hs_reporter.py` | Multilingual diagnostic reporter (5 languages) |
| `hs_testgen.py` | Secondary test tools — adversarial, boundary, and regression tests |
| `hs_audit.py` | Audit trail + 16 configurable breakpoints |
| `hs_controller.py` | Industrial state machine controller with Hˢ-GOV supervisor |

---

## Interactive Tools (9 HTML Demos)

Download any HTML file and open in a browser. No installation, no server, no dependencies.

| Tool | What It Does |
|------|-------------|
| [CoDaWork Demo](tools/interactive/Hs_CoDaWork_Demo.html) | Dual-dataset live demo — SEMF + Radionuclides, full pipeline strip, structural modes |
| [Cosmic Composition Slider](tools/interactive/cosmic_composition_interactive.html) | Planck 2018 cosmic energy budget — slide from z=0 to z=3400, watch dark energy vanish |
| [Cosmic Cone Loop](tools/interactive/cosmic_cone_5min_loop.html) | 5-minute inflation cone animation — cosmic composition evolution from Big Bang |
| [Cosmic Duality Dance](tools/interactive/cosmic_duality_dance.html) | Black hole / white hole compositional duality across amalgamation levels |
| [Cosmic Future Projection](tools/interactive/cosmic_future_projection.html) | ΛCDM Friedmann model — dark energy dominance trajectory from 1 Myr to heat death |
| [Simplex Scope](tools/interactive/EXP-19_Interactive_Simulator.html) | Real-time Fourier conjugate pair decomposition — all 12 pipeline steps visualised |
| [Spring-Mass Simulator](tools/interactive/EXP16_Interactive_Simulator.html) | Damped oscillator decomposed into KE/PE/Damping with chaos detection |
| [Conjugate Preservation Theorem](tools/interactive/EXP-19_Fourier_Conjugate_Preservation_Theorem.html) | Mathematical proof — 3 theorems + 1 corollary, interactive walkthrough |
| [Hˢ Spectrum Analyzer](tools/interactive/Hs_Spectrum_Analyzer.html) | Universal JSON reader — 5 readings from any pipeline output file |

---

## Quick Start

**Have a CSV?** One command:

```bash
python tools/pipeline/hs_ingest.py mydata.csv --all-languages
```

**Have HEPData?** Published high-energy physics measurements:

```bash
python tools/pipeline/hs_hepdata.py --list                    # see 8 curated HEP datasets
python tools/pipeline/hs_hepdata.py --fetch higgs_br --run    # Higgs branching ratios → pipeline
python tools/pipeline/hs_hepdata.py --fetch-all --run         # all 8 → full pipeline runs
```

**Python API:**

```python
from tools.pipeline.higgins_decomposition_12step import HigginsDecomposition

hd = HigginsDecomposition("MY-01", "My System", "MY_DOMAIN",
    carriers=["A", "B", "C"])
hd.load_data(my_matrix)  # numpy array, shape (N, D)
result = hd.run_full_extended()

from tools.pipeline.hs_codes import generate_codes
from tools.pipeline.hs_reporter import report
codes = generate_codes(result)
print(report(codes, lang="pt"))  # en, zh, hi, pt, it
```

**Amalgamation stability test:**

```python
from tools.pipeline.hs_amalgamation import AmalgamationEngine
engine = AmalgamationEngine(hd)
results = engine.run_all_schemes()  # tests all valid carrier merges
```

---

## The 25 Experiments

| ID | Domain | System | Highlight |
|----|--------|--------|-----------|
| Hs-01 | Precious metals | Gold/Silver ratio | Transfer entropy: Au→Ag directed flow |
| Hs-02 | Energy | US primary energy mix | Renewable carrier drift detection |
| Hs-03 | Nuclear physics | SEMF binding energy | **Flagship:** δ = 5.87 × 10⁻⁶ at 1/(π^e), Z=38 strontium |
| Hs-04 | Acoustics | Bessel function decomposition | Spectral mode analysis on simplex |
| Hs-05 | Geochemistry | Major oxide compositions | CaO+MgO dominant (61%) — depletion carries variance |
| Hs-06 | Nuclear fusion | Plasma confinement | Lawson criterion approached compositionally |
| Hs-07 | QCD | Quark/gluon decomposition | Perturbative ↔ non-perturbative boundary |
| Hs-08 | Particle physics | CKM/PMNS mixing matrices | Flavour mixing as composition |
| Hs-09 | Stellar physics | Main-sequence composition | CNO cycle carrier detection |
| Hs-10 | Gravitational waves | GW150914 merger | Chirp mass ratio decomposition |
| Hs-11 | Nuclear mass | AME2020 atomic masses | Binding energy systematics across chart of nuclides |
| Hs-12 | Classical mechanics | Spring-mass oscillator | KE/PE exchange — reversal under heavy damping |
| Hs-13 | Metallurgy | Steel alloy compositions | Phase-boundary detection via variance trajectory |
| Hs-14 | Mathematics | Fourier conjugate pairs | 12/12 preservation — 3 theorems + 1 corollary |
| Hs-15 | Materials science | hBN dielectric response | Crystal field decomposition |
| Hs-16 | Cosmology | Planck 2018 cosmic budget | Dark energy dominance, CDM/Baryon lock (CV=0) |
| Hs-17 | Data engineering | Backblaze HDD reliability | Fleet composition drift, 4 sub-experiments |
| Hs-18 | Urban planning | Markham municipal budget | Capital vs operating drift |
| Hs-19 | Infrastructure | Traffic signal timing | Phase allocation as composition |
| Hs-20 | AI/NLP | Conversation drift | Text-to-composition mapping (exploratory) |
| Hs-21 | Calibration | Reference standard library | 15 standards: mathematical, diffraction, transcendental |
| Hs-22 | Cross-domain | Natural pairs baseline | 12 systems, 7 domain pairs, cross-pair constant sharing |
| Hs-23 | Nuclear decay | Radionuclide chains (U-235, U-238, Th-232) | Decay chain as compositional trajectory |
| Hs-24 | Particle physics | HEPData validation campaign | 9 runs across 8 HEP systems, independent data source |
| Hs-25 | Cosmology | Planck 2018 cosmic energy budget | CoDaWork centrepiece — amalgamation reveals conservation laws |

---

## Key Results

| Finding | Value | Source |
|---------|-------|--------|
| Tightest transcendental match | δ = 5.87 × 10⁻⁶ (Nuclear SEMF → 1/(π^e) at Z=38) | Hs-03 |
| Classification rate | 15/15 NATURAL across all physical systems | All experiments |
| Fourier conjugate preservation | 12/12 pairs bit-identical (3 theorems + 1 corollary) | Hs-14 |
| Amalgamation stability | 58/58 schemes preserve classification (100%) | Hs-25, cross-domain |
| EITT entropy invariance | < 5% variation under geometric-mean decimation | All natural systems |
| Adversarial robustness | 21 attacks, 0 plausible-but-wrong outputs | Character Analysis |
| Transfer entropy | Detects directed causal flow between carriers | All experiments |
| Ratio locks | CDM/Baryon and Photon/Neutrino at CV=0 survive all amalgamation | Hs-25 |

---

## CoDaWork 2026 — Coimbra, Portugal (June 1–5)

Hˢ has been submitted to the 11th International Workshop on Compositional Data Analysis.

| Deliverable | File |
|---|---|
| Abstract (PDF) | [CoDaWork2026_Abstract_Higgins.pdf](papers/codawork2026/CoDaWork2026_Abstract_Higgins.pdf) |
| Submission letter + abstract (source) | [CoDaWork2026_Letter_and_Revised_Abstract.md](papers/codawork2026/CoDaWork2026_Letter_and_Revised_Abstract.md) |
| Executive summary (tiered claims) | [Hs_CoDaWork2026_Executive_Summary.md](papers/codawork2026/Hs_CoDaWork2026_Executive_Summary.md) |
| Strategic agenda | [CoDaWork2026_Strategic_Agenda.md](papers/codawork2026/CoDaWork2026_Strategic_Agenda.md) |
| Collaboration path | [CoDaWork2026_Collaboration_Path.md](papers/codawork2026/CoDaWork2026_Collaboration_Path.md) |
| Speech — gift ramp format | [CoDaWork2026_Speech_GiftRamp.md](papers/codawork2026/CoDaWork2026_Speech_GiftRamp.md) |
| Slide deck (.pptx) | [CoDaWork2026_Presentation.pptx](papers/codawork2026/CoDaWork2026_Presentation.pptx) |
| Standards Edition notebook | [Hs_Standards_Edition.ipynb](papers/codawork2026/Hs_Standards_Edition.ipynb) — self-contained conference handout, 18 cells, 3 reference standards |
| Action plan | [CoDaWork2026_Action_Plan.md](papers/codawork2026/CoDaWork2026_Action_Plan.md) |

Three open questions posed to the CoDa community: (1) Can the EITT entropy invariance be proved from Aitchison geometry? (2) Does classification survive ILR substitution for CLR? (3) Independent validation on CoDa community datasets.

---

## Flagship Documents

| Document | Description |
|---|---|
| [Character Analysis (docx)](papers/flagship/Higgins_Decomposition_Character_Analysis.docx) | Atomic-level pipeline disassembly — every operation, variable, attribution |
| [EXP-03 Precision Inference (docx)](papers/flagship/Hs_EXP03_Precision_Inference.docx) | Standalone paper on the δ = 5.87 × 10⁻⁶ nuclear binding result |
| [Applications Guide (docx)](papers/flagship/Hs_Applications_Guide.docx) | How to apply Hˢ to any domain — worked examples |
| [High Index Platform Guide (docx)](papers/flagship/Hs_High_Index_Platform_Guide.docx) | Advanced specification — multi-DUT, fingerprint matching, governance |

---

## Theory and Reference

| Document | Description |
|---|---|
| [Decomposition Function (v3.0)](docs/Hs_Decomposition_Function.md) | Formal derivation from determinism axiom through decimation to Hˢ = R ∘ M ∘ E ∘ C ∘ T ∘ V ∘ S |
| [Logic Map](docs/Hs_Logic_Map_and_State_Machine.md) | State machine specification with diagnostic commentary |
| [Reference v3.0 (docx)](docs/reference/Higgins_Decomposition_Reference_v3.0.docx) | Complete operator specification document |
| [Reference v1.0 (docx)](docs/reference/Higgins_Decomposition_Reference_v1.0.docx) | Original reference — retained for lineage |
| [HVLD Systems Primer (docx)](docs/reference/Hs_HVLD_Systems_Primer.docx) | Higgins Vertex Lock Diagnostic — engineering context |
| [Reference Standard Library](docs/reference/Hs_Reference_Standard_Library.md) | 15 calibration standards with full metrology |
| [Natural Pairs Baseline](docs/reference/Hs_Natural_Pairs_Baseline.md) | 12 systems, 7 domain pairs, cross-pair constant sharing |
| [Diffraction Composition Principle](docs/theory/Higgins_Diffraction_Composition_Principle.md) | Information mechanics declaration |
| [Grok Mathematical Notes](docs/theory/Grok_Mathematical_Foundation_Notes.md) | Independent mathematical review (xAI Grok) |

---

## Validation Reports

| Document | Description |
|---|---|
| [Canonical Validation Report (docx)](papers/validation/Canonical_Validation_Report.docx) | Full validation across all domains |
| [Calibration Proof (docx)](papers/validation/The_Calibration_Proof.docx) | Instrument calibration evidence |
| [EXP-19b Journal (docx)](papers/validation/EXP-19b_Journal.docx) | Fourier conjugate preservation experiment journal |
| [EXP15 X-ray Crystallography Journal (docx)](papers/validation/EXP15_Xray_Crystallography_Journal.docx) | hBN dielectric response validation |

---

## Claim Tiers

Every finding in this repository carries an explicit tier:

| Tier | Meaning | Example |
|------|---------|---------|
| Core science | Proven or strongly evidenced | Gauge R&R determinism, EXP-03 δ = 5.87 × 10⁻⁶ |
| Validated companion | Strong secondary result | Per-carrier decomposition, transfer entropy, amalgamation stability |
| Engineering control | Integrity and trust layer | Input guards, adversarial robustness, reference standards |
| Point of interest | Noteworthy, not yet canonical | Euler-family resonance, conversation drift |
| Exploratory | Interesting, requires more evidence | Transcendental Naturalness Hypothesis |

If a finding does not state its tier, treat it as exploratory until verified.

---

## Repository Structure

```
higgins-decomposition/
├── README.md                         # This file
├── EXECUTIVE_SUMMARY.md              # Running log — development, decisions, principles
├── CITATION.cff                      # Citation metadata
├── LICENSE                           # CC BY 4.0
│
├── ai-refresh/                       # Machine-readable system state
│   ├── HS_MACHINE_MANIFEST.json      # ★ START HERE for automated systems
│   ├── HS_ADMIN.json                 # Identity + RWA-001 authority
│   ├── HS_SYSTEM_INVENTORY.json      # Complete domain/system inventory
│   ├── HS_GITHUB_CONFIG.json         # Repository metadata
│   ├── PREPARE_FOR_REPO.json         # Pre-push readiness manifest
│   └── AI_REFRESH_2026-04-27.md      # Changelog — April sprint
│
├── docs/                             # Documentation
│   ├── Hs_Learning_Path.md           # Where to start
│   ├── Hs_Architecture_Overview.md   # System architecture
│   ├── Hs_Applications_Guide.md      # How to use Hˢ in any domain
│   ├── Hs_High_Index_Platform_Guide.md  # Advanced multi-DUT platform
│   ├── Hs_Decomposition_Function.md  # v3.0 formal derivation
│   ├── Hs_Logic_Map_and_State_Machine.md  # Symbolic logic + state machine
│   ├── reference/                    # Specification books + metrology
│   └── theory/                       # Mathematical foundations
│
├── experiments/                      # 25 experiments (Hs-01 through Hs-25)
│   ├── Hs-01_Gold_Silver/            # → Hs-20_Conversation_Drift/
│   ├── Hs-21_Reference_Standards/    # Calibration library
│   ├── Hs-22_Natural_Pairs/          # Cross-domain pair validation
│   ├── Hs-23_Radionuclides/          # Multi-chain nuclear decay
│   ├── Hs-24_HEPData_Validation/     # HEPData campaign
│   └── Hs-25_Cosmic_Energy_Budget/   # Planck 2018 — CoDaWork centrepiece
│
├── papers/
│   ├── flagship/                     # Character Analysis, EXP-03, guides
│   ├── codawork2026/                 # Full CoDaWork 2026 package
│   └── validation/                   # Validation reports + experiment journals
│
└── tools/
    ├── pipeline/                     # 13 Python files — the engine
    │   ├── higgins_decomposition_12step.py
    │   ├── hs_amalgamation.py        # Subcompositional recursion
    │   ├── hs_codes.py               # 78 diagnostic codes + 10 modes
    │   ├── hs_sensitivity.py         # Component Power Mapper
    │   ├── hs_fingerprint.py         # Compositional fingerprint
    │   ├── ...                       # + 8 more (see Pipeline section above)
    │   └── locales/                  # 5 language files
    ├── interactive/                   # 9 HTML tools (open in browser)
    ├── Hs_Dashboard.ipynb            # JupyterLab notebook
    └── Hs_Standards_Edition.ipynb    # ★ Standards Edition — self-contained conference handout
```

---

## Languages

| Code | Language | Native |
|------|----------|--------|
| en | English | English |
| zh | Mandarin Chinese | 中文 |
| hi | Hindi | हिन्दी |
| pt | Portuguese | Português |
| it | Italian | Italiano |

Adding a language requires one JSON file in `tools/pipeline/locales/`. Zero code changes.

---

## Lineage

This tool emerged from the [Higgins Unity Framework](https://github.com/PeterHiggins19/Higgins-Unity-Framework), which remains the governance, application, and historical development sibling. The mathematical foundations build on Aitchison (1982/1986) simplex geometry, Shannon (1948) entropy, and Varley (2025) information theory for complex systems. Computational support: Claude (Anthropic), ChatGPT (OpenAI), Grok (xAI), Gemini (Google), Copilot (Microsoft).

---

## Contributing

The repository is open. The tool is free. The data is included. The results are reproducible.

If you can prove why geometric-mean decimation preserves Shannon entropy on the simplex, that's a theorem waiting to be written. If you can find a natural compositional system that fails the transcendental pretest after all alternate decompositions, that's a discovery. If you can run Hˢ on a dataset from your own domain and share the results, that's a validation.

Start with `tools/pipeline/higgins_decomposition_12step.py`. Run a reference standard. Compare your results. Report what you find.

---

## Directory Index

Each major directory has its own README with a complete guide to contents, usage, and structure.

| Directory | README | Description |
|---|---|---|
| `tools/` | [tools/README.md](tools/README.md) | Complete tools library — pipeline, interactive tools, notebooks |
| `tools/pipeline/` | [tools/pipeline/README.md](tools/pipeline/README.md) | 13-file Python pipeline — core engine, diagnostics, ingestion, infrastructure |
| `tools/interactive/` | [tools/interactive/README.md](tools/interactive/README.md) | 9 standalone HTML demos — open in any browser, no dependencies |
| `experiments/` | [experiments/README.md](experiments/README.md) | 25 experiments (Hs-01 through Hs-25) across 18 domains |
| `docs/` | [docs/README.md](docs/README.md) | Documentation — learning path, architecture, theory, reference standards |
| `papers/` | [papers/README.md](papers/README.md) | Publications — flagship papers, CoDaWork 2026, validation reports |
| `ai-refresh/` | [ai-refresh/README.md](ai-refresh/README.md) | Machine-readable system state — manifests, inventory, maintenance |

---

*Hˢ — The instrument reads. The expert decides. The loop stays open.*
*Peter Higgins, 2026*
