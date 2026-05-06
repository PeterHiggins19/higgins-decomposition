# Experiments Directory

## Higgins Decomposition Validation Suite

**25 experiments across 18 domains -- spanning 44 orders of magnitude**
**Plus M-series: instrument calibration and manifold projection testing**

This directory contains the complete experimental validation of the Higgins Decomposition (Hs) pipeline. From 2-carrier commodity markets to 5-carrier cosmic energy budgets, these experiments demonstrate that compositional structure is universal: the simplex geometry that governs gold/silver ratios is the same geometry that governs the energy budget of the observable universe.

---

## Folder Structure

Each experiment follows the naming pattern:

```
Hs-NN_Name/
```

Where `NN` is a zero-padded experiment ID (01--25) and `Name` is a descriptive label using underscores. A typical experiment folder contains:

| File | Purpose |
|------|---------|
| `Hs-NN_results.json` | Full pipeline output: carriers, CLR coordinates, variance, diagnostics |
| `Hs-NN_report_en.txt` | Diagnostic report (English) |
| `Hs-NN_report_pt.txt` | Diagnostic report (Portuguese) |
| `Hs-NN_report_it.txt` | Diagnostic report (Italian) |
| `Hs-NN_report_zh.txt` | Diagnostic report (Chinese) |
| `Hs-NN_report_hi.txt` | Diagnostic report (Hindi) |
| `*.csv` | Source data (where applicable) |
| `Hs-NN_JOURNAL.md` | Experiment journal with methodology and findings |

### Reading Results

Every `_result.json` file contains:

- **carriers**: the compositional parts (D components on the simplex)
- **CLR coordinates**: centred log-ratio transformed values
- **sigma2_A**: Aitchison variance (total compositional variability)
- **HVLD codes**: diagnostic classification from the 78-code system
- **structural_mode**: one of 10 identified compositional modes

Higher D (carrier count) means higher-dimensional simplex geometry. N is the number of observations processed through the pipeline.

---

## Experiment Catalogue

### Physical Sciences

| ID | Name | Domain | D | N | Description |
|----|------|--------|---|---|-------------|
| Hs-01 | Gold/Silver | COMMODITIES | 2 | 624 | Precious metals price ratio decomposition on the 1-simplex |
| Hs-03 | Nuclear SEMF | NUCLEAR | 3 | 92 | Semi-empirical mass formula binding energies for all stable nuclei |
| Hs-04 | Bessel Acoustics | ACOUSTICS | 3 | 200 | Acoustic mode decomposition using Bessel function carrier structure |
| Hs-05 | Geochemistry | GEOCHEMISTRY | 3 | 150 | Major-element oxide compositions of igneous rock samples |
| Hs-06 | Fusion | NUCLEAR | 3 | 100 | Fusion cross-section decomposition across light nuclei |
| Hs-11 | AME2020 | NUCLEAR | 3 | 500 | Atomic Mass Evaluation 2020 nuclear binding energy surface |
| Hs-12 | Spring-Mass | FORCE | 3 | 200 | Classical spring-mass system energy partition decomposition |
| Hs-13 | Steel | MATTER | 3 | 80 | Steel alloy composition and mechanical property relationships |
| Hs-15 | hBN Dielectric | MATERIALS | 3 | 200 | Hexagonal boron nitride dielectric response decomposition |

### Particle Physics and Cosmology

| ID | Name | Domain | D | N | Description |
|----|------|--------|---|---|-------------|
| Hs-07 | QCD | QCD | 3 | 20 | Quantum chromodynamics coupling constant running with energy scale |
| Hs-08 | CKM/PMNS | PARTICLE | 3 | 11 | Quark and neutrino mixing matrix element compositions |
| Hs-10 | GW150914 | GRAVITY | 3 | 40 | LIGO gravitational wave event energy-frequency decomposition |
| Hs-16 | Planck Cosmic | COSMOLOGY | 3 | 200 | Planck satellite CMB power spectrum compositional analysis |
| Hs-23 | Radionuclides | NUCLEAR | 4 | -- | Radionuclide decay chain compositional tracking (4-carrier simplex) |
| Hs-25 | Cosmic Energy Budget | COSMOLOGY | 5 | 103 | Full LCDM cosmic energy budget: baryons, CDM, photons, neutrinos, dark energy |

### Astrophysics and Signals

| ID | Name | Domain | D | N | Description |
|----|------|--------|---|---|-------------|
| Hs-02 | US Energy | ENERGY | 3 | 25 | United States primary energy source mix over time |
| Hs-09 | Stellar | ASTROPHYSICS | 3 | 30 | Stellar nucleosynthesis abundance pattern decomposition |
| Hs-14 | Conjugate Pairs | SIGNAL THEORY | 3 | 200 | Fourier conjugate pair structure in compositional signal space |

### Engineering and Urban Systems

| ID | Name | Domain | D | N | Description |
|----|------|--------|---|---|-------------|
| Hs-17 | Backblaze | ENGINEERING | 3 | 34 | Hard drive failure mode compositional analysis from Backblaze data |
| Hs-18 | Urban Markham | URBAN | 3 | 31 | Land use composition of Markham, Ontario municipal zones |
| Hs-19 | Traffic Signals | URBAN | 3 | 831 | Traffic signal timing decomposition across urban intersections |

### AI Safety

| ID | Name | Domain | D | N | Description |
|----|------|--------|---|---|-------------|
| Hs-20 | Conversation Drift | AI SAFETY | 4 | 18 | LLM conversation topic drift measured as compositional trajectory |

### Methodology and Calibration

| ID | Name | Domain | D | N | Description |
|----|------|--------|---|---|-------------|
| Hs-21 | Reference Standards | Calibration | -- | -- | Reference standard library: 15 calibration constants, 35 reference values |
| Hs-22 | Natural Pairs | Cross-domain | -- | -- | 7 pair families, 14 sub-experiments testing natural compositional relationships |
| Hs-24 | HEPData Validation | Particle physics | -- | -- | Cross-validation against published high-energy physics datasets |

### M-Series: Manifold Projection System Testing

A new experimental track dedicated to testing Hs as a data-information manifold projection system. Unlike the numbered experiments which apply the instrument to physical data, the M-series tests the instrument itself against known geometric ground truth.

| ID | Name | Domain | D | N | Description |
|----|------|--------|---|---|-------------|
| Hs-M01 | Manifold Calibration | INSTRUMENT | 3-4 | 1-80 | Gold standard calibration: 10 known geometric objects (point, line, circle, sphere, cube, rhomboid, torus, spiral, saddle) fed through full pipeline. All 10 pass -- instrument faithfully projects compositional geometry with zero false positives and zero false negatives. |
| Hs-M02 | EMBER Energy | ENERGY | 8-9 | 26 | CoDaWork 2026 reference experiment: EMBER 2025 electricity generation for 7 systems (Germany, UK, Japan, France, China, India, World). Full pipeline + amalgamation stability testing (5/7 systems show shape classification changes under coarser groupings) + decimation invariance. The par excellence applied CoDa experiment. |

---

## Summary Files

Two summary files live at the experiments root:

| File | Purpose |
|------|---------|
| [Hs_Extended_Executive_Summary.json](Hs_Extended_Executive_Summary.json) | Full executive summary across all experiments with aggregate statistics |
| [Hs_New_Domains_Summary.json](Hs_New_Domains_Summary.json) | Summary of domain expansion from core nuclear physics to all 18 domains |

---

## Scale Coverage

The experiment suite spans approximately 44 orders of magnitude in the physical quantities analysed:

- **Smallest scale**: Quark mixing matrix elements and QCD coupling (Hs-07, Hs-08) -- subatomic particle physics
- **Largest scale**: Cosmic energy budget of the observable universe (Hs-25) -- cosmological composition
- **Carrier range**: From D=2 (commodity price ratios) through D=3 (majority of experiments) to D=5 (full LCDM cosmology)

The consistent diagnostic behaviour across this range is the primary evidence that compositional geometry is scale-invariant: the simplex does not care whether it describes gold prices or dark energy.

The M-series extends this validation by testing against mathematically exact geometric objects, establishing that the instrument itself introduces no artifacts, distortions, or blind spots.

---

## Visualization Standard

Each M-series experiment (and all future experiments) produces a standard suite of 4 interactive HTML tools:

| Tool | Purpose |
|------|---------|
| Pipeline Slideshow | Step-by-step walkthrough of the decomposition pipeline |
| Manifold View | 2D CLR trajectory projection |
| Helix | Helical decomposition — drift vs oscillation separation |
| **Manifold Projector** | **Mandatory terminal output** — 3D rotating radar-polygon tube showing the compositional data manifold in space and time. This IS the diagram of the system. The slideshow is the journey; the projector is the destination. |

The Manifold Projector renders per-carrier CLR values normalized to 0-1 as radar chart fingerprints stacked along the Z-axis with perspective projection (FOV=700). Perturbation mapping shows inter-step changes as outward spikes (green to yellow to red).

---

*Peter Higgins / Rogue Wave Audio*
*Licensed under CC BY 4.0*

---

## CNT canonical corpus (added 2026-05-06)

A dated release snapshot of the **25-experiment Compositional Navigation
Tensor (CNT) canonical corpus** lives in this directory at:

* [`Hs-CNT_2026-05/`](Hs-CNT_2026-05/) — engine 2.0.4 / schema 2.1.0 release snapshot

The CNT corpus sits alongside the historical Hs-01 to Hs-25 experiment
series. Both series remain part of the Hs canon. The Hs-NN series
predates CNT and uses the original Hs pipeline; the Hs-CNT_2026-05
series uses the CNT engine (`HCI-CNT/`) and produces the audit-traceable
JSON-and-PDF chain documented in
[`../HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md`](../HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md).

The live working folder for the CNT corpus (used by the engine and
atlas modules) is at [`../HCI-CNT/experiments/`](../HCI-CNT/experiments/).
The `Hs-CNT_2026-05/` folder is the as-published snapshot.

When the CNT engine evolves and re-runs the corpus, the next dated
snapshot (`Hs-CNT_<later-date>/`) captures the new state. Earlier
snapshots are kept for lineage.

---
