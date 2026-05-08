# Hˢ — Higgins Decomposition on the Simplex

> **🎉 Fully Public — Publication-Grade (push #27, 2026-05-08).** Both engines (CNT and CNQ) are shipped in Python and R; CNQ has language-agnostic pseudocode and a 43-test suite. Single-file AI loader at [`HS_FAST_REFRESH.json`](HS_FAST_REFRESH.json); human entry point at [`PUBLICATION_READY.md`](PUBLICATION_READY.md). All "EXPERIMENTAL — NOT FOR REPO USE" guards retired. Free to use, help available.

**Hˢ = R ∘ M ∘ E ∘ C ∘ T ∘ V ∘ S**

A deterministic compositional inference instrument operating within Aitchison geometry on the simplex. Seven operators — Simplex closure, Variance trajectory, Transcendental squeeze, Classification, Entropy test, Mode synthesis, and Report — compose into a single decomposition function derived from a single axiom: *same input, same output, always.*

Validated across 18 physical domains, 25 experiments, 53 devices under test, and 44 orders of magnitude. The instrument reads structure without creating or destroying it.

[![Validate Repository](https://github.com/PeterHiggins19/higgins-decomposition/actions/workflows/validate.yml/badge.svg)](https://github.com/PeterHiggins19/higgins-decomposition/actions/workflows/validate.yml)
[![Code: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-d22.svg)](LICENSE) [![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-blue.svg)](LICENSE-DOCS)
[![HCI-CNT engine 2.0.4](https://img.shields.io/badge/HCI--CNT%20engine-2.0.4-1f4e79.svg)](HCI-CNT/)
[![HCI-CNT schema 2.1.0](https://img.shields.io/badge/HCI--CNT%20schema-2.1.0-1f4e79.svg)](HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md)
[![HCI-CNQ engine shipped](https://img.shields.io/badge/HCI--CNQ%20engine-shipped%20py%2BR%2Bpseudocode-7b3294.svg)](HCI-CNQ/engine/)
[![HCI-AUDIO doctrine](https://img.shields.io/badge/HCI--AUDIO-doctrine--only-c84a8e.svg)](HCI-AUDIO/)
[![HCI-ULTRASOUND doctrine](https://img.shields.io/badge/HCI--ULTRASOUND-doctrine--only-d97706.svg)](HCI-ULTRASOUND/)
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
| License | Code: Apache-2.0 (LICENSE) · Docs: CC BY 4.0 (LICENSE-DOCS) |

---

## What's New — May 2026

Two protocols shipped that make this repo dramatically more usable for
both researchers and AI assistants:

**🆕 CCTT v1.0 — CNT Compositional Tensor Train.** A 7-phase protocol that takes any compositional dataset (CSV/XLSX) and produces a CNT-grade analysis with full hash-chained provenance — even if you have never heard of Aitchison geometry. Works in two interchangeable modes:

- **User-mode** — researcher walks the [runbook](ai-refresh/CCTT_RUNBOOK.md) by hand
- **User + AI-mode** — AI assistant (Claude, ChatGPT, Gemini, in-house) executes the same 7 phases; user confirms at every gate

The protocol is identical in both modes. Pilot acceptance test: an AI given only the spec and a raw CSV reproduced the canonical `content_sha256` byte-for-byte. → [`ai-refresh/CCTT_QUICKSTART.md`](ai-refresh/CCTT_QUICKSTART.md)

**🆕 Volume IV — The Quaternion View (May 7, 2026, push #22).**  Names the algebra CNT has been computing in.  Three IEEE-floor confirmations on drive failures, Planck CMB photons, and Standard Model neutrino oscillation establish that compositional dynamics on the simplex carries three structural invariances simultaneously — simplex rotation, mass-flow handedness, time-reversal symmetry — which is exactly the definition of a quaternion.  Central claim: **CNT measures invariance.  CNQ names the algebra it lives in.**  Engine unchanged; 25-experiment determinism gate unchanged; what changes is what we can say about what the engine is doing.  → [`HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md`](HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md)

**🆕 HCI-CNQ — Compositional Navigation Quaternion (May 7-8, 2026, pushes #23–#27).** The CNQ tier is live, canonical, and the engine is shipped. Promoted from experimental status after the third IEEE-floor confirmation (push #23); the production `cnq.py` engine landed in push #26; the R port `cnq.R`, language-agnostic pseudocode, and 43-test suite landed in push #27. The Hs system now ships a three-tier compositional analytics stack (CoDa → CNT → CNQ) plus the HCI instrument family. Both engines (cnt.py + cnq.py + cnt.R + cnq.R) are deterministic and hash-chained, producing identical content_sha256 across consecutive runs. Three reproducible IEEE-floor demonstrations on Backblaze, Planck CMB, and SM neutrino. Cross-platform reproduction challenge open. **Open code, hash-chained outputs, doctrine published, build-to-spec help available, free.** → [`HCI-CNQ/README.md`](HCI-CNQ/README.md)

**🆕 HCI-AUDIO + HCI-ULTRASOUND — applied sibling tiers (May 8, 2026, push #24).** Two new canonical tiers landed alongside the third AI cross-check pass (Grok). [`HCI-AUDIO/`](HCI-AUDIO/) is the canonical home for psychoacoustic 4-way active loudspeaker alignment with ERB-band carriers, quaternion phase mapping, and listening-position diffraction — the modern descendant of the original DADC compositional work. [`HCI-ULTRASOUND/`](HCI-ULTRASOUND/) is the canonical home for non-contact medical and industrial ultrasound, with a **geometry lock probe** as the headline use case. Both are doctrine-only scaffolds; first pilots are the next milestones. → [`HCI-AUDIO/README.md`](HCI-AUDIO/README.md), [`HCI-ULTRASOUND/README.md`](HCI-ULTRASOUND/README.md)

**🆕 DADC origin lineage documented (May 8, 2026, push #24).** The Grok cross-check pass surfaced and verified the historical origin of the entire framework: DADC (Dimension-Apportioned Diffraction Correction) at the Binaural Test Lab in Markham, with a fixed 6.02 dB diffraction budget apportioned across cabinet dimensions — the first natural simplex constraint in the Higgins lineage. The lineage runs DADC → H₁ → HUF → Hˢ → CNT → CNQ. Original work: [Rogue-Wave-Audio repository](https://github.com/PeterHiggins19/Rogue-Wave-Audio). Canonical lineage doc: [`HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md).

**🆕 OPERATIONS_PROTOCOL v1.0 — Gawande meta-checklist for the whole repo.** A single map of 12 transition points (starting an analysis, pushing, cowork session start/end, push failure, corpus drift, …) each with a binary pass/fail local checklist pointing at the canonical document holding the deeper detail. → [`OPERATIONS_PROTOCOL.md`](OPERATIONS_PROTOCOL.md)

Both protocols are model-agnostic, registered in [`ai-refresh/HS_ADMIN.json`](ai-refresh/HS_ADMIN.json) for future cold-start discovery, and proven end-to-end on the live repo (see [`OPERATIONS_PROTOCOL_PILOT_REPORT.md`](OPERATIONS_PROTOCOL_PILOT_REPORT.md) and [`ai-refresh/CCTT_PILOT_REPORT.md`](ai-refresh/CCTT_PILOT_REPORT.md)).

---

## Start Here

**If you have a compositional dataset and want a CNT-grade analysis right now (NEW):** [`CCTT_QUICKSTART.md`](ai-refresh/CCTT_QUICKSTART.md) → walk the [`CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md) yourself, or paste the AI-mode prompt into Claude/ChatGPT/Gemini.

**If you are working on or with this repo (NEW):** [`OPERATIONS_PROTOCOL.md`](OPERATIONS_PROTOCOL.md) — the front-door map of every operational transition (analysis, push, cowork start/end, AI cold-start, recovery paths). One row per transition, each pointing at its canonical checklist.

**If you are a person:** [Learning Path](docs/Hs_Learning_Path.md) → [Architecture Overview](docs/Hs_Architecture_Overview.md) → [Applications Guide](docs/Hs_Applications_Guide.md) → [High Index Platform](docs/Hs_High_Index_Platform_Guide.md)

**If you are a machine:** [`ai-refresh/HS_MACHINE_MANIFEST.json`](ai-refresh/HS_MACHINE_MANIFEST.json) — identity, navigation, protocol, governance, and authority resolution in a single file. Follow the onboarding sequence defined there. Then read [`OPERATIONS_PROTOCOL.md`](OPERATIONS_PROTOCOL.md) and [`ai-refresh/CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md).

**If you want to run Hs right now:** [Standards Edition Notebook](tools/Hs_Standards_Edition.ipynb) — self-contained Jupyter notebook, auto-installs dependencies, auto-fetches pipeline from GitHub, includes 3 built-in reference standards, runs all advanced analyses. The conference handout tool.

**If you are reviewing for CoDaWork 2026:** [Abstract (PDF)](papers/codawork2026/CoDaWork2026_Abstract_Higgins.pdf) → [Executive Summary](papers/codawork2026/Hs_CoDaWork2026_Executive_Summary.md) → [`CCTT_QUICKSTART.md`](ai-refresh/CCTT_QUICKSTART.md) → [Standards Edition Notebook](papers/codawork2026/Hs_Standards_Edition.ipynb) → [Collaboration Path](papers/codawork2026/CoDaWork2026_Collaboration_Path.md)

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

## HCI-CNQ — Compositional Navigation Quaternion (live tier, push #23)

The `HCI-CNQ/` subsystem is the quaternion-native sibling tier above
CNT in the three-tier Hs stack (CoDa → CNT → CNQ). Promoted to canonical
on 2026-05-07 after three independent IEEE-floor confirmations of the
quaternion identification on real datasets. Doctrine, demonstrations,
comparisons with CoDa and CNT, and the engineering proposal for a
compiled `cnq.py` engine all live in this folder, in public.

The CNQ tier is what comes above CNT for problems CNT was not designed
for: D ≥ 8, large T, multi-trajectory bundles, cross-dataset structure
as the primary observable. Climate modeling, multi-decade economic
flows, large industrial composition, microbiome cohorts.

| Folder | Contents |
|---|---|
| [`HCI-CNQ/doctrine/`](HCI-CNQ/doctrine/) | Central claim, deeper connections, concepts-for-test, corpus comparison plan, post-CoDa benefits |
| [`HCI-CNQ/tier_system/`](HCI-CNQ/tier_system/) | CoDa → CNT → CNQ tier explanation, ROI/use cases, engine proposal, three-way comparison |
| [`HCI-CNQ/experiments/`](HCI-CNQ/experiments/) | Three IEEE-floor demonstrations: backblaze drive failures, Planck CMB photons, SM neutrino oscillation |

Three reproducible demonstrations are in the experiments folder. Each
is self-contained — script, input data, CNT JSON output, results,
report. Anyone can re-run.

The compiled `cnq.py` engine itself is the next milestone (~14 days
per [`HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md`](HCI-CNQ/tier_system/CNQ_ENGINE_PROPOSAL.md)).
Until it lands, the experiments are the working proofs and the
canonical CNT engine continues to produce the underlying compositional
data. Quickstart: see [`HCI-CNQ/README.md`](HCI-CNQ/README.md).

**How we work — demonstration first.** Every tool in the Hs family —
CoDa methods (community-standard), CNT (`HCI-CNT/`), CNQ (`HCI-CNQ/`),
HCI-AUDIO (`HCI-AUDIO/`), HCI-ULTRASOUND (`HCI-ULTRASOUND/`), and the HCI
instrument family (`HCI/`) — is built and tested in public on the same
terms: open code, hash-chained outputs, doctrine published. We show
what each tool is, what it does (by demonstration on real datasets),
when to use it, how to use it, and **we offer to help you build it to
specification on your own data, free**. Open an issue, find Peter at a
conference, or follow the contact in this README.

---

## HCI-AUDIO — applied sibling, doctrine-only (push #24)

The `HCI-AUDIO/` subsystem is the canonical home for **applied audio
work**: 4-way active loudspeaker alignment with ERB psychoacoustic
band carriers, quaternion phase mapping, and listening-position
diffraction.

This is the direct modern descendant of the original DADC
(Dimension-Apportioned Diffraction Correction) work in
[Rogue-Wave-Audio](https://github.com/PeterHiggins19/Rogue-Wave-Audio) —
the BTL loudspeaker-laboratory work that created the first natural simplex
constraint in the Higgins lineage. Where DADC apportioned a fixed 6.02
dB diffraction budget across three cabinet dimensions, HCI-AUDIO
apportions perceptual energy across 40 ERB bands × 4 drivers at the
listening position. Same closure principle, applied at the right scale.

| Folder | Contents |
|---|---|
| [`HCI-AUDIO/doctrine/`](HCI-AUDIO/doctrine/) | ERB band mapping, quaternion phase mapping, helmsman at listening position, alignment targets |
| [`HCI-AUDIO/spec/`](HCI-AUDIO/spec/) | Psychoacoustic 4-way adapter spec, pipeline spec |

Status: doctrine-only. First pilot (real measurement against Peter's
4-way system) is the next milestone. Quickstart:
[`HCI-AUDIO/README.md`](HCI-AUDIO/README.md).

---

## HCI-ULTRASOUND — applied sibling, doctrine-only (push #24)

The `HCI-ULTRASOUND/` subsystem is the canonical home for **non-contact
medical and industrial ultrasound**, with a **geometry lock probe** as
the headline use case. The lock probe uses CNT/CNQ-driven feedback
(Joint Helmsman + Helmsman Stability + M² = I) to actively maintain
measurement on a specific geometric feature of the target — an edge, a
tissue interface, a defect, a specular reflector — under relative
motion or noise.

This is the active-sensing descendant of DADC: the same closure
principle (apportioning a fixed return-signal total across carriers),
plus a control loop that steers the probe to keep the helmsman locked
on the desired feature.

| Folder | Contents |
|---|---|
| [`HCI-ULTRASOUND/doctrine/`](HCI-ULTRASOUND/doctrine/) | Geometry lock probe, object detection, autofocus and stabilisation, medical vs industrial |
| [`HCI-ULTRASOUND/spec/`](HCI-ULTRASOUND/spec/) | Ultrasound adapter spec |

Status: doctrine-only. Recommended first pilot is industrial composite
inspection on a public dataset (lower regulatory overhead). Quickstart:
[`HCI-ULTRASOUND/README.md`](HCI-ULTRASOUND/README.md).

---

## Lineage

The simplex / compositional thinking that underpins Hˢ → CNT → CNQ originated in Peter's earlier loudspeaker work at the **Binaural Test Lab (BTL)** in Markham, Ontario — a single-identity lab with canonical machine-readable identity card [`RWA-001.json`](../RWA/RWA-001.json). The BTL work is documented in the [Rogue-Wave-Audio repository](https://github.com/PeterHiggins19/Rogue-Wave-Audio) (live site) and mirrored locally at [`../RWA/`](../RWA/) for reference. Specifically, **DADC** (Dimension-Apportioned Diffraction Correction) discovered that the cabinet-edge diffraction gain was a fixed 6.02 dB budget that had to be apportioned across the three cabinet dimensions — the first natural simplex constraint in the Higgins lineage. The lineage runs **DADC → H₁ (Higgins Operator, a nonlinear unity-normalization map on Hilbert space) → HUF (Higgins Unity Framework, MC-4 + EITT) → Hˢ (Higgins Decomposition, this repo) → CNT (engine 2.0.4) → CNQ (push #23) → HCI-AUDIO + HCI-ULTRASOUND (push #24, applied tiers)**. Full canonical narrative: [`HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md). RWA-side reciprocal: [`../RWA/HUF_RELATIONSHIP.json`](../RWA/HUF_RELATIONSHIP.json).

This tool also emerged from the [Higgins Unity Framework](https://github.com/PeterHiggins19/Higgins-Unity-Framework), which remains the governance, application, and historical development sibling. The mathematical foundations build on Aitchison (1982/1986) simplex geometry, Shannon (1948) entropy, and Varley (2025) information theory for complex systems. Computational support: Claude (Anthropic), ChatGPT (OpenAI), Grok (xAI), Gemini (Google), Copilot (Microsoft).

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

Three open questions posed to the CoDa community: (1) Can the EITT entropy invariance be proved from Aitchison geometry? (2) Does classification survive ILR 