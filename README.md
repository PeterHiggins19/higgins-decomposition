# Hˢ — Higgins Decomposition

**A compositional inference instrument operating on the simplex.**

*Author: Peter Higgins, Markham, Ontario, Canada*

Higgins Decomposition reads the geometric fingerprint of any compositional system — from nuclear binding energy to cosmic energy budgets — without creating or destroying structure. It is a deterministic 12-step pipeline that transforms raw measurements into compositional diagnostics on the Aitchison simplex.

**Validated:** 17 domains, 28 systems, 44 orders of magnitude. 15 reference standards. 59 diagnostic codes. 5 languages.

**Conference:** [CoDaWork 2026 package](papers/codawork2026/Hs_CoDaWork2026_Executive_Summary.md) — Coimbra, Portugal (June 2026)

| Canonical Count | Value |
|---|---|
| Physical domains | 17 |
| Distinct systems | 28 |
| Reference standards | 15 |
| Total DUTs | 43 |
| Transcendental constants | 35 |
| Conjugate pairs | 13 |
| Diagnostic codes | 59 |
| Languages | 5 (en, zh, hi, pt, it) |
| Scale range | 10⁻¹⁸ m to 10²⁶ m (44 orders of magnitude) |
| Pipeline version | 1.0 Extended |
| Deterministic | Yes (Gauge R&R bit-identical) |

**Start here:** [README](README.md) → [CoDaWork strategy](papers/codawork2026/Hs_CoDaWork2026_Executive_Summary.md) → [Character Analysis](papers/flagship/Higgins_Decomposition_Character_Analysis.docx) → [Reference Standards](docs/reference/Hs_Reference_Standard_Library.md) → [Interactive theorem demo](tools/interactive/EXP-19_Fourier_Conjugate_Preservation_Theorem.html)

---

## What This Tool Does

Given an N × D matrix of measurements across D compositional carriers, Hˢ:

1. Closes to the simplex (all rows sum to 1)
2. Transforms via centred log-ratio (CLR)
3. Tracks cumulative Aitchison variance σ²_A(t)
4. Fits a vertex lock diagnostic (HVLD — bowl or hill classification)
5. Tests proximity to 35 transcendental constants
6. Validates entropy invariance under geometric-mean decimation (EITT)
7. Detects compositional turbulence (stalls, spikes, reversals)
8. Projects into geometric embeddings (ternary, complex, helix)
9. Decomposes per-carrier contributions, transfer entropy, and ratio stability

The pipeline is deterministic: identical inputs produce identical outputs. Zero stochastic elements. SHA-256 hash verification. Gauge R&R confirmed bit-identical.

---

## Interactive Tools

**Download any HTML file and open in a browser. No installation required.**

| Tool | What It Does |
|------|-------------|
| [Simplex Scope](tools/interactive/EXP-19_Interactive_Simulator.html) | Real-time Fourier conjugate pair decomposition — all 12 pipeline steps visualised |
| [Spring-Mass](tools/interactive/EXP16_Interactive_Simulator.html) | Damped oscillator decomposed into KE/PE/Damping with chaos detection |
| [Conjugate Preservation Theorem](tools/interactive/EXP-19_Fourier_Conjugate_Preservation_Theorem.html) | Mathematical proof — 3 theorems + 1 corollary, interactive |
| [Spectrum Analyzer](tools/interactive/HUF_Spectrum_Analyzer_Universal.html) | Universal JSON reader — 5 readings from any pipeline output |

---

## Quick Start

```python
from higgins_decomposition_12step import HigginsDecomposition

hd = HigginsDecomposition("MY-01", "My System", "MY_DOMAIN",
    carriers=["Carrier_A", "Carrier_B", "Carrier_C"])
hd.load_data(my_data_matrix)  # numpy array, shape (N, D)

result = hd.run_full_extended()  # full 12-step + extended panel

from hs_codes import generate_codes
from hs_reporter import report

codes = generate_codes(result)
print(report(codes, lang="en"))  # also: "zh", "hi", "pt", "it"
```

---

## Languages

Reports are available in 5 languages:

| Code | Language | Native |
|------|----------|--------|
| en | English | English |
| zh | Mandarin Chinese | 中文 |
| hi | Hindi | हिन्दी |
| pt | Portuguese | Português |
| it | Italian | Italiano |

Adding a language requires one JSON file in `tools/pipeline/locales/`. Zero code changes.

---

## Reference Standards

Two specification books provide calibration baselines for any Device Under Test:

- [**Reference Standard Library**](docs/reference/Hs_Reference_Standard_Library.md) — 15 calibration references (mathematical functions, diffraction, transcendental, noise floor) with full metrology
- [**Natural Pairs Baseline**](docs/reference/Hs_Natural_Pairs_Baseline.md) — 12 systems across 7 physical domain pairs with cross-pair constant sharing

---

## Key Results

| Finding | Value | Source |
|---------|-------|--------|
| Tightest transcendental match | δ = 5.87 × 10⁻⁶ (Nuclear SEMF → 1/(π^e)) | Hs-03 |
| Domains tested | 17 (Acoustics → Cosmology) | Release validation |
| Classification rate | 15/15 NATURAL | All physical experiments |
| Fourier preservation | 12/12 pairs (11 symmetry + 1 asymmetry correctly detected) | Hs-14 |
| Adversarial robustness | 21 attacks, 0 plausible-but-wrong outputs | Character Analysis |
| Transfer entropy | Detects directed information flow between carriers | Hs-01 through Hs-22 |

---

## Repository Structure

```
higgins-decomposition/
├── EXECUTIVE_SUMMARY.md          # Running log of development and decisions
├── CITATION.cff                  # Citation metadata
├── LICENSE                       # CC BY 4.0
├── ai-refresh/                   # Machine-readable configuration
│   ├── HS_MACHINE_MANIFEST.json  # ★ START HERE for automated systems
│   ├── HS_ADMIN.json             # Identity, terminology, communication standards
│   └── HS_SYSTEM_INVENTORY.json  # Complete domain/system inventory
├── docs/reference/               # Specification books (Markdown)
├── experiments/                  # 22 experiments with results JSON
│   ├── Hs-01_Gold_Silver/        
│   ├── ...                       
│   └── Hs-22_Natural_Pairs/      
├── papers/                       # Flagship documents and conference materials
│   ├── flagship/                 
│   └── codawork2026/             
└── tools/                        
    ├── pipeline/                 # Core Python code (4 files)
    │   ├── higgins_decomposition_12step.py
    │   ├── hs_codes.py           # 59 diagnostic codes
    │   ├── hs_reporter.py        # Multilingual reporter
    │   └── locales/              # 5 language files
    └── interactive/              # 4 HTML tools (open in browser)
```

---

## Claim Tiers

Every finding in this repository carries an explicit status:

| Tier | Meaning | Example |
|------|---------|---------|
| **Core science** | Proven or strongly evidenced | Gauge R&R determinism, EXP-03 δ = 5.87 × 10⁻⁶ |
| **Validated companion** | Strong secondary result | Per-carrier decomposition, transfer entropy |
| **Engineering control** | Integrity and trust layer | Input guards, adversarial robustness, reference standards |
| **Point of interest** | Noteworthy, not yet canonical | Euler-family resonance, conversation drift |
| **Exploratory** | Interesting, requires more evidence | Transcendental Naturalness Hypothesis |

If a finding does not state its tier, treat it as exploratory until verified.

---

## For Automated Systems

Read [`ai-refresh/HS_MACHINE_MANIFEST.json`](ai-refresh/HS_MACHINE_MANIFEST.json) first. It provides identity, navigation, protocol, governance, and authority resolution in a single machine-readable file. Follow the onboarding sequence defined there.

---

## Lineage

This tool emerged from the [Higgins Unity Framework](https://github.com/PeterHiggins19/Higgins-Unity-Framework), which remains the governance, application, and historical development sibling. The mathematical foundations build on Aitchison (1982/1986) simplex geometry, Shannon (1948) entropy, and Varley (2025) information theory for complex systems. Computational support: Claude (Anthropic), ChatGPT (OpenAI), Grok (xAI), Gemini (Google), Copilot (Microsoft).

---

## Contributing

The repository is open. The tool is free. The data is included. The results are reproducible.

If you can prove why geometric-mean decimation preserves Shannon entropy on the simplex, that's a theorem waiting to be written. If you can find a natural compositional system that fails the transcendental pretest after all alternate decompositions, that's a discovery. If you can run Hˢ on a dataset from your own domain and share the results, that's a validation.

Start with `tools/pipeline/higgins_decomposition_12step.py`. Run a reference standard. Compare your results. Report what you find.

---

*Hˢ — The instrument reads. The expert decides. The loop stays open.*
*Peter Higgins, 2026*
