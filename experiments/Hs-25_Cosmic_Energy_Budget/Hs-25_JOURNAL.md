# Hs-25: Cosmic Energy Budget — Planck 2018 ΛCDM

**Experiment journal for the Higgins Decomposition of the composition of the universe.**

*Author: Peter Higgins*
*Date: 2026-04-27*
*Domain: COSMOLOGY*
*Claim tier: Core science (pipeline results) + Exploratory (physical interpretation)*

---

## 1. Motivation

This is the hardest experiment in the Hˢ catalog. The cosmic energy budget is the most extreme compositional system known: five carriers spanning 44 orders of magnitude in scale, with hierarchy ratios exceeding 10⁴, three known phase transitions across cosmic time, and the most precisely measured parameters in all of physics (Planck 2018 satellite data).

The experiment tests every capability of the Hˢ instrument simultaneously: can it read the geometry of a system where one carrier (dark energy) dominates at 69% today but was 0% at the CMB? Where two carriers (photons and neutrinos) are below 0.01% today but dominated the entire universe in the first epoch? Where the physically most consequential carrier (baryonic matter — literally everything we can see and touch) is never more than 16% at any epoch?

This is also the first experiment designed specifically for CoDaWork 2026 presentation.

---

## 2. Data Source

**Planck 2018 cosmological parameters** (Planck Collaboration, arXiv:1807.06209, Table 2: TT,TE,EE+lowE+lensing+BAO best fit):

| Parameter | Symbol | Value | Physical Meaning |
|---|---|---|---|
| Dark energy density | Ω_Λ | 0.6847 | Cosmological constant — accelerating expansion |
| Cold dark matter density | Ω_CDM | 0.2589 | Non-baryonic gravitating matter |
| Baryonic matter density | Ω_b | 0.0486 | Ordinary matter (atoms, stars, planets, us) |
| Photon radiation density | Ω_γ | 5.38×10⁻⁵ | CMB photons (from T_CMB = 2.7255 K) |
| Neutrino density | Ω_ν | 3.63×10⁻⁵ | Cosmic neutrino background (3 species, N_eff = 3.046) |

Present-day closure check: Σ Ω = 0.9923 (the remaining ~0.8% is curvature consistent with flat).

**Evolution model:** Standard Friedmann equations in flat ΛCDM. Energy densities scale as:

- Dark energy: ρ_Λ ∝ constant (equation of state w = −1)
- Matter (CDM + baryonic): ρ_m ∝ (1+z)³ (volume dilution)
- Radiation (photons + neutrinos): ρ_r ∝ (1+z)⁴ (volume dilution + frequency redshift)

At each redshift z, the fractions are normalised to sum to 1 (simplex closure).

**Sampling:** 103 epochs from z = 0 (today) to z = 3400 (well past matter-radiation equality), using combined logarithmic and linear spacing to capture all three phase transitions. Key transition redshifts included explicitly: z ≈ 0.3 (dark energy transition), z ≈ 3400 (matter-radiation equality), z = 1100 (CMB / last scattering surface).

---

## 3. Composition at Key Epochs

### Today (z = 0)

| Carrier | Fraction |
|---|---|
| Dark Energy | 69.00% |
| Cold Dark Matter | 26.09% |
| Baryonic Matter | 4.90% |
| Photon Radiation | 0.005% |
| Neutrinos | 0.004% |

### Dark Energy Transition (z ≈ 0.3)

| Carrier | Fraction |
|---|---|
| Dark Energy | 50.33% |
| Cold Dark Matter | 41.81% |
| Baryonic Matter | 7.85% |
| Photon Radiation | 0.011% |
| Neutrinos | 0.008% |

### CMB / Last Scattering (z = 1100)

| Carrier | Fraction |
|---|---|
| Dark Energy | 0.00% |
| Cold Dark Matter | 63.66% |
| Baryonic Matter | 11.95% |
| Photon Radiation | 14.56% |
| Neutrinos | 9.83% |

### Matter-Radiation Equality (z ≈ 3400)

| Carrier | Fraction |
|---|---|
| Dark Energy | 0.00% |
| Cold Dark Matter | 42.17% |
| Baryonic Matter | 7.92% |
| Photon Radiation | 29.80% |
| Neutrinos | 20.11% |

---

## 4. Pipeline Results

### Core Diagnosis

| Metric | Value |
|---|---|
| HVLD Shape | **bowl** — variance accelerating (universe integrating toward dark energy domination) |
| HVLD R² | **0.9320** (PRECISION band) |
| σ²_A final | **54.3659** (extremely high — reflects 10⁴+ hierarchy ratio) |
| Classification | **NATURAL** |
| Nearest constant | **1/(e^π)** |
| Proximity δ | **4.19 × 10⁻⁵** (precision-level match) |
| Constant family | **EULER** |
| EITT | **PASS** |

### Interpretation

The universe's compositional evolution locks to the reciprocal of Euler's number raised to the power of π, with a proximity of δ = 4.19 × 10⁻⁵. This is a precision-level match (code S8-TGT-DIS). The EULER family detection (code S8-EUL-DIS) indicates that the pipeline's log-ratio geometry resonates with the fundamental structure of the cosmic energy budget.

The bowl shape indicates the universe is compositionally integrating — dark energy is progressively dominating, pulling all other fractions toward zero. The system has not yet reached its vertex (equilibrium point on the variance trajectory), which is consistent with a universe that has not yet reached thermal death.

### Key Diagnostic Codes (51 total)

**Discoveries (17):**

- **S8-EUL-DIS** — Euler-family transcendental match (1/(e^π), δ = 4.19 × 10⁻⁵)
- **S8-TGT-DIS** — Precision match (δ < 0.001)
- **S9-STL-DIS** — 6 entropy stalls detected (mark the phase transitions)
- **S9-REV-DIS** — 1 entropy reversal (the matter-to-dark-energy crossover)
- **XU-PCD-DIS** — Dark Energy dominates CLR variance (72.6%)
- **XU-DRU-DIS** — Drift increasing (universe is evolving, not static)
- **XC-PIR-DIS** — PID redundancy (carriers share information — coupled by gravity)
- **XC-RPS-DIS** — **CDM/Baryon ratio is perfectly stable** (CV ≈ 0) — they dilute identically because both scale as (1+z)³
- **XC-RPS-DIS** — **Photon/Neutrino ratio is perfectly stable** (CV ≈ 0) — both scale as (1+z)⁴
- **XC-RPV-DIS** — All Dark Energy ratios are highly volatile (CV > 100%) — dark energy behaves completely differently from all other carriers
- **XC-ZCR-DIS** — Zero-crossing events for Dark Energy, Photons, and Neutrinos (approach simplex boundary at extreme redshifts)
- **XU-CPM-INF** — Component Power Mapper completed
- **XU-DPC-DIS** — 3 disproportionate carriers detected
- **XU-PWR-DIS** — Power ranking ≠ mass ranking

**Structural Modes (5):**

- **SM-OVC-CAL** — Overconstrained (near-perfect fit — expected: this is model-derived data from the most precisely measured parameters in physics)
- **SM-RTR-DIS** — Regime transition detected (the phase transitions between radiation/matter/dark energy domination)
- **SM-DMR-DIS** — Domain resonance (Euler-family geometry encodes deep cosmological structure)
- **SM-CPL-DIS** — Carrier coupling (CDM↔Baryon and Photon↔Neutrino pairs are physically locked)
- **SM-SCG-INF** — Smooth convergence (despite transitions, the overall evolution is smooth — expected for Friedmann dynamics)

---

## 5. Component Power Map

### Power Ranking

| Rank | Carrier | Power Score | Mass % | Power/Fraction Ratio | Phase | Flip Risk |
|---|---|---|---|---|---|---|
| 1 | Cold Dark Matter | 0.5450 | 61.4% | 0.55x | safe | no |
| 2 | **Baryonic Matter** | **0.5187** | **11.5%** | **2.76x** | safe | no |
| 3 | Dark Energy | 0.2720 | 24.4% | 0.69x | safe | no |
| 4 | Photon Radiation | 0.1657 | 1.6% | 6.28x | safe | no |
| 5 | Neutrinos | 0.1567 | 1.1% | 8.81x | safe | no |

### Disproportionate Carriers (3 found)

| Carrier | Mass Fraction | Power/Fraction Ratio | Interpretation |
|---|---|---|---|
| **Neutrinos** | 1.1% | **8.81x** | Nearly 9x more influential than mass predicts. Neutrinos set the radiation density at early times, determining when matter-radiation equality occurs. |
| **Photon Radiation** | 1.6% | **6.28x** | Over 6x more influential than mass predicts. The CMB radiation field determined the entire early universe structure. |
| **Baryonic Matter** | 11.5% | **2.76x** | Nearly 3x more influential than mass predicts. This is everything we can see and touch — all stars, galaxies, planets, and life. |

### Physical Interpretation

**Power ranking ≠ mass ranking.** The mass ranking is CDM > Dark Energy > Baryonic > Photons > Neutrinos. The power ranking swaps Dark Energy and Baryonic Matter — baryonic matter has more influence on the system's geometric identity than dark energy does, despite having less than half the mass fraction. This is because baryonic matter's coupling to CDM (the perfectly stable ratio) means perturbing baryons disrupts the matter sector's internal structure.

**The locked ratios encode conservation laws.** CDM/Baryon: CV ≈ 0 (both dilute as (1+z)³). Photon/Neutrino: CV ≈ 0 (both dilute as (1+z)⁴). These are not approximate correlations — they are *exact* to machine precision. Hˢ detects these as carrier coupling (SM-CPL-DIS) with zero-CV stable ratios. In physical terms, these are conservation laws: the baryon-to-CDM ratio is fixed at the Big Bang and never changes. The photon-to-neutrino ratio is fixed at neutrino decoupling and never changes.

**Dark energy is compositionally independent.** Every Dark Energy ratio pair has CV > 100%. Dark energy does not participate in any coupling. It operates on a fundamentally different equation of state (w = −1 vs w = 0 for matter and w = 1/3 for radiation). Hˢ detects this as volatile ratios — dark energy is the carrier that is compositionally decoupled from all others.

---

## 6. Fingerprint

| Field | Value |
|---|---|
| Hash | `62bf32beb2f06873` |
| Shape | bowl |
| R² band | PRECISION |
| Classification | NATURAL |
| Constant family | EULER |
| EITT | PASS |
| Chaos level | LOW |
| Drift | increasing |

---

## 7. CoDaWork 2026 Significance

This experiment is designed as the centrepiece demonstration for a 15-minute CoDaWork 2026 presentation. It demonstrates:

1. **Universal applicability.** Hˢ reads the composition of the universe itself — the most extreme compositional system imaginable. If it works here, it works everywhere.

2. **Physical conservation laws as stable ratios.** The CoDa community understands log-ratio analysis. The CDM/Baryon ratio with CV = 0 is a *perfect* log-ratio invariant — it encodes a cosmological conservation law. The Photon/Neutrino ratio is another. Hˢ detects both automatically.

3. **The yeast problem at cosmic scale.** Baryonic matter is 4.9% of the universe today. It is everything we are made of. The power mapper correctly identifies it as disproportionately influential (2.76x). Neutrinos at 0.004% have an 8.81x power-to-fraction ratio. These are the yeast — the components whose influence far exceeds their mass fraction.

4. **Phase transitions as regime transitions.** The structural mode SM-RTR-DIS fires on the cosmic data. The entropy stalls mark the exact redshifts where the universe crossed from one compositional regime to another. A CoDa audience will recognise these as the compositional equivalent of thermodynamic phase transitions.

5. **Precision-level Euler family match.** The universe's compositional evolution locks to 1/(e^π) with δ = 4.19 × 10⁻⁵. Whether this is a deep geometric truth or a coincidence, it is a *detection* — the pipeline found it automatically.

---

## 8. Files

| File | Content |
|---|---|
| `Hs-25_cosmic_energy_budget.csv` | Raw data: 103 epochs × 5 carriers |
| `Hs-25_results.json` | Full pipeline output |
| `Hs-25_codes.json` | Diagnostic codes (pipeline only) |
| `Hs-25_codes_full.json` | Diagnostic codes (pipeline + power map) |
| `Hs-25_power_map.json` | Component Power Mapper output |
| `Hs-25_fingerprint.json` | Compositional fingerprint |
| `Hs-25_report_en.txt` | English diagnostic report |
| `Hs-25_report_zh.txt` | Chinese diagnostic report |
| `Hs-25_report_hi.txt` | Hindi diagnostic report |
| `Hs-25_report_pt.txt` | Portuguese diagnostic report |
| `Hs-25_report_it.txt` | Italian diagnostic report |
| `Hs-25_JOURNAL.md` | This journal |

---

## 9. Predictions (Pre-Analysis)

*Documented before pipeline run for honest reporting:*

1. **Classification: NATURAL** — The universe's energy budget is governed by fundamental physics. ✅ CONFIRMED (δ = 4.19 × 10⁻⁵)
2. **HVLD: bowl** — The universe is evolving toward dark energy domination (integrating). ✅ CONFIRMED (R² = 0.932)
3. **Baryonic matter should show disproportionate power** — it forms all structure despite small fraction. ✅ CONFIRMED (2.76x power-to-fraction)
4. **CDM/Baryon ratio should be perfectly stable** — both scale as (1+z)³. ✅ CONFIRMED (CV ≈ 0)
5. **Photon/Neutrino ratio should be perfectly stable** — both scale as (1+z)⁴. ✅ CONFIRMED (CV ≈ 0)
6. **Regime transitions should be detected** — radiation→matter→dark energy. ✅ CONFIRMED (SM-RTR-DIS + 6 stalls + 1 reversal)
7. **Dark energy should be compositionally decoupled** — different equation of state. ✅ CONFIRMED (all DE ratio pairs CV > 100%)

**7/7 predictions confirmed.** The pipeline reads the universe exactly as physics predicts.

---

*The instrument reads the composition of the universe.*
*The fingerprint captures cosmic geometry in 8 dimensions.*
*The power map reveals what mass fraction hides — at every scale.*
*The simplex is the same everywhere. Even here.*
