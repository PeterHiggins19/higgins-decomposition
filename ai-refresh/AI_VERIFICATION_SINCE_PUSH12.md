# AI Verification Document — Push #12 to Current State

## Purpose

This document provides everything a future AI session needs to verify the complete state of the Hˢ repository since push #12 (commit df5a904, April 29, 2026). It is designed to be read after HS_MACHINE_MANIFEST.json and HS_ADMIN.json. It supplements AI_REFRESH_2026-05-02.md with deeper verification data.

---

## 1. Repository Identity

| Field | Value |
|-------|-------|
| Name | Higgins Decomposition |
| Symbol | Hˢ (H-superscript-S) |
| Framework version | v3.0 |
| Decomposition | Hˢ = R . M . E . C . T . V . S |
| Tensor functor | ρ ∘ Tr ∘ Σ ∘ Λ ∘ S |
| Author | Peter Higgins |
| Last push | #12 — df5a904, 2026-04-29 |
| Pending push | #13 |

---

## 2. Canonical Counts (Verified)

| Item | Count | Verification method |
|------|-------|-------------------|
| Domains tested | 19 | Count unique domains in HS_SYSTEM_INVENTORY.json |
| Systems analysed | 38 | Count individual systems across all domains |
| Experiment folders | 33 | `ls -d experiments/Hs-*/ HCI/ Higgins_Coordinate_System/ Hs_Direct/` |
| Pipeline files | 26 | `find tools/pipeline -name "*.py" \| wc -l` |
| Interactive tools | 10 | `find tools/interactive -name "*.html" \| wc -l` |
| Diagnostic codes | 106 + 9 PD-* | Count in hs_codes.py |
| Structural modes | 14 | Count in hs_codes.py |
| HCI instruments | 1 (CBS) | HCI/hci_cbs.py |
| HCI calibration tests | 10 | Run hci_cal01_cnt_calibration.py → 10/10 PASS |
| HCI precision experiments | 10 | Run cnt_precision_experiment.py → P01–P10 |
| Flagship papers (.docx) | 8 | `ls papers/flagship/*.docx \| wc -l` |
| Reference standards | 15 | Count in HS_SYSTEM_INVENTORY.json |
| Transcendental constants | 35 | Count in pipeline pretest |
| Languages | 5 | en, zh, hi, pt, it |

---

## 3. New Since Push #12

### 3.1 New Top-Level Folders (3)

| Folder | Contents | File count |
|--------|----------|-----------|
| `HCI/` | Higgins Computational Instruments — CBS engine, CNT tensor, calibration suite, precision experiments | 8 files (excl. __pycache__) |
| `Higgins_Coordinate_System/` | Coordinate system spec, handbook v4.2, diagnostic experiment | 4 files |
| `Hs_Direct/` | Japan EMBER direct analysis — PPTX, PDF, SVGs, JSON, QA images | ~15 files |

### 3.2 New Experiment Folders (3)

| Folder | Type | Key result |
|--------|------|-----------|
| `Hs-LAB01_Titration_Standards/` | LAB-series | pH curves as compositional trajectories |
| `Hs-MC4_Shape_Calibration/` | MC-series | 5 geometric test objects, projector normalization validation |
| `Hs-STD_Standards_Test/` | STD-series | cylinder/sphere/cube with lock point detection, 3/3 PASS |

### 3.3 New Pipeline Tools (12 additions: 14 → 26)

| File | Description |
|------|-------------|
| `hs_run.py` | Unified pipeline runner — data in → complete standard output |
| `hs_helix_exploded.py` | Exploded helix PDF generator |
| `hs_manifold_helix.py` | 3D manifold helix PDF generator |
| `hs_manifold_projections.py` | 4-page projection suite PDF |
| `hs_polar_stack.py` | Per-interval polar stack PDF + JSON |
| `hs_manifold_paper.py` | 3D manifold-on-paper PDF |
| `hs_projector_gen.py` | Interactive 3D projector HTML generator |
| `hs_cinema_gen.py` | Compositional cinema PPTX generator |
| `hs_tensor.py` | Tensor functor implementation |
| `balun_matrix_analysis.py` | Deep matrix eigenstructure analysis |
| `impedance_bridge.py` | Tr × basis × step impedance bridge |
| `tr_basis_experiment.py` | Trace basis experiment runner |

### 3.4 Updated Pipeline Tools

| File | Change |
|------|--------|
| `higgins_decomposition_12step.py` | Step 5.5 EDI control gate + Step 6.5 matrix analysis |
| `hs_codes.py` | v2.0, 106 codes + 9 PD-* Poincaré codes, 14 structural modes |

### 3.5 New Interactive Tool (1)

| File | Description |
|------|-------------|
| `tools/interactive/hs_projector.html` | Universal Manifold Projector |

### 3.6 New HCI Files (8)

| File | Description |
|------|-------------|
| `HCI/HCI_FOUNDATION.md` | Pure math proofs — 4 definitions, 5 corollaries, display standard |
| `HCI/hci_cbs.py` | CBS oscilloscope engine (~180 lines core + CNT functions) |
| `HCI/README.md` | Folder purpose and usage |
| `HCI/calibration/hci_cal01_cnt_calibration.py` | 10 CNT calibration test objects |
| `HCI/calibration/cnt_precision_experiment.py` | 10 precision experiments (P01–P10) |
| `HCI/calibration/CNT_PRECISION_DIAGNOSTIC.md` | Multi-view diagnostic with state machine, tensor chain |
| `HCI/calibration/JOURNAL.md` | HCI-CAL01 experiment journal |
| `HCI/calibration/HCI-CAL01_results.json` | Machine-readable calibration results |

### 3.7 New Papers and Handbooks (3 new since push #12)

| File | Description |
|------|-------------|
| `papers/flagship/Hs_Manifold_Character_Handbook.docx` | Manifold characterisation handbook |
| `papers/flagship/Hs_Software_Handbook.docx` | Complete codebase publication |
| `papers/flagship/Manifold_Characterization_by_Decomposition.docx` | CoDa publication paper |
| `papers/flagship/CNT_Engine_Mathematics_Handbook.docx` | CNT engine math reference |
| `Higgins_Coordinate_System/Higgins_Coordinate_System_Handbook_v4.2.docx` | Coordinate system handbook |

---

## 4. Key Scientific Findings Since Push #12

### 4.1 Compositional Navigation Tensor (CNT)

From any closed composition x in the D-simplex:

```
CNT(x) = (θ, ω, κ, σ)

θ_{ij}(x)  = atan2(h_j, h_i)                  — bearing tensor
ω(t, t+1)  = atan2(||h₁×h₂||, ⟨h₁,h₂⟩)      — angular velocity
κ_{jj}(x)  = 1/x_j                             — steering sensitivity
σ(t, t+1)  = argmax_j |h_j(t+1) - h_j(t)|     — helmsman index
```

Five corollaries: bearing determinism, steering asymmetry, lock detection, bearing reversal, infinite helm. All verified by HCI-CAL01 calibration (10/10 PASS).

### 4.2 T03 Finding: Norm Variation in Naive CLR Circle

The naive CLR zero-sum construction `h[2] = -(h[0]+h[1])` produces `||h||² = r²(2+sin2θ)`, a 53.6% norm variation. This is geometric (ellipse on zero-sum plane), not numerical. Fixed by Helmert orthonormal basis `e₁=[1,-1,0]/√2`, `e₂=[1,1,-2]/√6`, giving constant `||h|| = r` and ω constant to 10⁻¹⁴ degrees.

### 4.3 Angular Velocity Refinement

Replaced arccos with atan2 via Lagrange identity:
```
||h₁×h₂||² = ||h₁||²||h₂||² - ⟨h₁,h₂⟩²
ω = atan2(√(cross²), dot)
```
Eliminates up to 8 digits of precision loss near 0° and 180°. Works in arbitrary dimension D.

### 4.4 Aitchison Isometry Verification

CLR and ILR angular velocities are identical to 10⁻¹² degrees across D=3..20 (P05). The Aitchison isometry (Egozcue 2003) is exact; residual is floating-point roundoff.

### 4.5 Condition Number Precision Predictor

κ = max(x)/min(x) predicts available precision: digits ≈ 15 - log₁₀(κ). Engine stable to x = 10⁻¹⁵ (P08). Scales to D = 100 (P09).

### 4.6 EDI Control Gate

Eigenstructure Distortion Index: EDI = √(angular² + spectral²)/√2. Quantifies CLR transform effect on covariance eigenstructure. Regimes: MINIMAL (<0.1), MODERATE (0.1–0.3), WORKING (0.3–0.7), EXTREME (>0.7).

### 4.7 Poincaré Disc Connection

Circularity ratio ρ mapped to hyperbolic Poincaré disc via Cayley transform. 9 PD-* diagnostic codes.

### 4.8 Higgins Coordinate System

New coordinate system on the simplex with Euclidean, polar, hyperbolic, and projective representations.

---

## 5. Engine State (Verified by Running)

### 5.1 CNT Calibration

```bash
cd Hs/HCI/calibration
python3 hci_cal01_cnt_calibration.py
# Expected: CALIBRATION RESULT: 10/10 PASS
```

All 10 tests: T01 identity, T02 drift, T03 rotation, T04 divergence, T05 lock, T06 reversal, T07 symmetry, T08 contraction, T09 decomposition, T10 navigation.

### 5.2 Precision Experiments

```bash
python3 cnt_precision_experiment.py
# Expected: 10 experiments P01–P10, all complete
```

Key verification points:
- P01: max |Σh| = 1.78e-15 (≤ 8ε)
- P02: Orthonormal variation = 0.000%
- P04: max |arccos - atan2| = 0.00 on T03 data
- P05: max |ω_CLR - ω_ILR| < 10⁻¹² deg
- P06: Helmert orthonormal to 2.22e-16
- P08: Stable to x = 10⁻¹⁵
- P09: ω std invariant at 8.81e-14 to D=100
- P10: All channels at machine ε

### 5.3 CNT Engine Functions (hci_cbs.py)

| Function | Purpose | Verified |
|----------|---------|----------|
| `cnt_bearing(h, i, j)` | Pairwise bearing | T01, T03, T05, T06 |
| `cnt_bearing_tensor(h)` | All D(D-1)/2 bearings | T07 |
| `cnt_angular_velocity(h1, h2)` | atan2 angular velocity | P03, P04, T03 |
| `cnt_steering_sensitivity(h)` | κ = 1/x_j via softmax | T04, T08 |
| `cnt_helmsman(h1, h2, carriers)` | argmax |Δh| | T02, T10 |
| `cnt_condition_number(x)` | max(x)/min(x) | P07, P08 |
| `cnt_helmert_basis(D)` | Helmert submatrix | P06, P09 |
| `cnt_ilr_project(h, basis)` | CLR → ILR projection | P05 |

---

## 6. File Inventory Verification Commands

```bash
# Pipeline files
find tools/pipeline -name "*.py" | wc -l
# Expected: 26

# Interactive tools
find tools/interactive -name "*.html" | wc -l
# Expected: 10

# Experiment folders
ls -d experiments/Hs-*/ | wc -l
# Expected: 30 (Hs-01 through Hs-25 + LAB01 + M01 + M02 + MC4 + STD)

# Flagship papers
ls papers/flagship/*.docx | wc -l
# Expected: 8

# HCI files (excluding __pycache__)
find HCI/ -type f -not -path "*__pycache__*" | wc -l
# Expected: 8 (+ build_cnt_handbook.js = 9)

# Domains in inventory
grep -c '"systems"' ai-refresh/HS_SYSTEM_INVENTORY.json
# Expected: 19

# Calibration status
python3 HCI/calibration/hci_cal01_cnt_calibration.py 2>&1 | grep "CALIBRATION RESULT"
# Expected: CALIBRATION RESULT: 10/10 PASS
```

---

## 7. Governance Files Cross-Reference

| File | Key fields to verify |
|------|---------------------|
| `ai-refresh/HS_MACHINE_MANIFEST.json` | systems: 38, pipeline: 26, codes: 106+9, hci_calibration: 10/ALL PASS, hci_precision: IEEE 754 FLOOR |
| `ai-refresh/HS_SYSTEM_INVENTORY.json` | 19 domains, 38 systems, pipeline_tools.total: 26 |
| `ai-refresh/HS_ADMIN.json` | canonical names include CNT, CBS, EDI, Helmert |
| `ai-refresh/PREPARE_FOR_REPO.json` | systems: 38, push #13 pending |
| `ai-refresh/AI_REFRESH_2026-05-02.md` | systems: 38, all new files listed |
| `HCI/HCI_FOUNDATION.md` | Definition 2 uses atan2 (not arccos) |
| `HCI/calibration/JOURNAL.md` | 10/10 PASS, precision audit section present |

---

## 8. Complete Experiment List (33 entries)

| # | ID | Domain | Systems | Status |
|---|------|--------|---------|--------|
| 1 | Hs-01 | Commodities | Gold/Silver 338yr | Complete |
| 2 | Hs-02 | Energy | US electricity 25yr | Complete |
| 3 | Hs-03 | Nuclear | SEMF Z=1-92 | Complete |
| 4 | Hs-04 | Acoustics | Bessel J₁ directivity | Complete |
| 5 | Hs-05 | Geochemistry | Basalt-rhyolite series | Complete |
| 6 | Hs-06 | Energy/Nuclear | DT fusion partition | Complete |
| 7 | Hs-07 | QCD | Quark flavour fractions | Complete |
| 8 | Hs-08 | Particle | CKM + PMNS matrices | Complete |
| 9 | Hs-09 | Astrophysics | Stellar nucleosynthesis | Complete |
| 10 | Hs-10 | Gravity | GW150914 merger | Complete |
| 11 | Hs-11 | Nuclear | AME2020 mass table | Complete |
| 12 | Hs-12 | Force | Spring-mass oscillator | Complete |
| 13 | Hs-13 | Matter | AISI 1020 steel | Complete |
| 14 | Hs-14 | Signal Theory | 12 Fourier conjugate pairs | Complete |
| 15 | Hs-15 | Materials | hBN dielectric | Complete |
| 16 | Hs-16 | Cosmology | Planck 2018 Ω evolution | Complete |
| 17 | Hs-17 | Engineering | Backblaze fleet 108 weeks | Complete |
| 18 | Hs-18 | Urban | Markham budget | Complete |
| 19 | Hs-19 | Urban | Toronto traffic 831 signals | Complete |
| 20 | Hs-20 | AI Safety | Conversation drift | Complete |
| 21 | Hs-21 | Standards | Reference standards | Complete |
| 22 | Hs-22 | Signal Theory | Natural pairs | Complete |
| 23 | Hs-23 | Nuclear | Radionuclide decay chains | Complete |
| 24 | Hs-24 | HEP Collider | HEPData validation (7 systems) | Complete |
| 25 | Hs-25 | Cosmology | Cosmic energy budget | Complete |
| 26 | Hs-LAB01 | Chemistry | Titration standards | Complete |
| 27 | Hs-M01 | Calibration | Manifold calibration (10 objects) | Complete |
| 28 | Hs-M02 | Energy | EMBER 7 countries | Complete |
| 29 | Hs-MC4 | Calibration | Shape calibration (5 objects) | Complete |
| 30 | Hs-STD | Calibration | Standards test (cyl/sphere/cube) | Complete |
| 31 | HCI | Instruments | CBS/CNT calibration + precision | Complete |
| 32 | Higgins_Coord | Mathematics | Coordinate system on simplex | Complete |
| 33 | Hs_Direct | Energy | Japan EMBER direct analysis | Complete |

---

## 9. Precision Budget Summary

| CNT Channel | Operation | Precision | Limiting Factor |
|-------------|-----------|-----------|----------------|
| CLR transform | log, mean | ≤ 8ε | Floating-point log/subtraction |
| Bearing θ | atan2(h_j, h_i) | machine ε | None |
| Angular velocity ω | atan2 + Lagrange | machine ε | None after atan2 fix |
| Sensitivity κ | 1/x_j via softmax | ~1.78e-16 | exp/sum roundtrip |
| Helmsman σ | argmax |Δh| | exact | Discrete operation |
| Overall | — | ~2.22e-16 | IEEE 754 double for κ < 100 |

Condition number rule: Available digits ≈ 15 - log₁₀(max(x)/min(x)).

---

## 10. What to Verify First

If you are a new AI session reading this file:

1. **Read** `HS_MACHINE_MANIFEST.json` — identity, navigation, protocol
2. **Read** `HS_ADMIN.json` — canonical names, banned terms, reporting rules
3. **Read** `HS_SYSTEM_INVENTORY.json` — all domains, systems, tool counts
4. **Run** `python3 HCI/calibration/hci_cal01_cnt_calibration.py` — confirm 10/10 PASS
5. **Run** `python3 HCI/calibration/cnt_precision_experiment.py` — confirm P01–P10 complete
6. **Check** counts match Section 2 above
7. **Read** `HCI/HCI_FOUNDATION.md` — confirm Definition 2 uses atan2
8. **Read** `AI_REFRESH_2026-05-02.md` — session changelog

If any count disagrees with this document, investigate. The discrepancy is the finding.

---

The instrument reads. The expert decides. The loop stays open.
