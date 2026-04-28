# Hˢ Architecture Overview
## System Topology and Component Registry

**Author:** Peter Higgins, Markham, Ontario, Canada
**Version:** 1.0 — April 2026

---

## System Stack

```
┌─────────────────────────────────────────────────────┐
│                    Hˢ-GOV                           │
│  Governance: OPEN / SUPERVISED / LOCKED / QUARANTINE│
│  Policy engine · Controller registry · Fingerprint DB│
│  Event aggregation · State persistence              │
├─────────────────────────────────────────────────────┤
│                  HsController                       │
│  States: IDLE → RUNNING → HELD/COMPLETED/ABORTED   │
│  Event bus · Breakpoint integration · Resume logic  │
├─────────────────────────────────────────────────────┤
│              12-Step Pipeline + Extended             │
│  Closure → CLR → Variance → HVLD → Squeeze → EITT  │
│  → Ternary → Complex → Helix → Extended Panel      │
├─────────────────────────────────────────────────────┤
│                   Audit Trail                       │
│  16 breakpoints · Chain hash · SHA-256 per operation│
│  5 presets · 4 actions · Full traceability          │
├─────────────────────────────────────────────────────┤
│              Post-Pipeline Tools                    │
│  Codes (73) · Reporter (5 langs) · Fingerprint     │
│  Metrology · Test generation · Ingest · HEPData    │
└─────────────────────────────────────────────────────┘
```

---

## Component Registry

### Core Pipeline

| File | Purpose | Key Output |
|------|---------|------------|
| `higgins_decomposition_12step.py` | 12-step pipeline + extended panel | Results dict with all diagnostics |
| `higgins_transcendental_pretest.py` | 35-constant proximity test | Match list with δ values |

### Diagnostic Layer

| File | Purpose | Key Output |
|------|---------|------------|
| `hs_codes.py` | 78 diagnostic codes + 10 structural modes | Code list with parameters |
| `hs_reporter.py` | Multilingual report generation | Human-readable reports (5 languages) |

### Sensitivity Analysis

| File | Purpose | Key Output |
|------|---------|------------|
| `hs_sensitivity.py` | Component Power Mapper (CLI, PBM, CPS) | Power rankings, phase boundaries, power-to-fraction ratios |

### Knowledge Engine

| File | Purpose | Key Output |
|------|---------|------------|
| `hs_fingerprint.py` | Deterministic geometric identity | SHA-256 fingerprint + similarity scoring |
| `hs_testgen.py` | Self-generating test tools | Regression, healthcheck, crosscheck, stability scripts |
| `hs_metrology.py` | Instrument meta-evaluation | 8 quality metrics, ISO 17025-compatible |

### Integrity Layer

| File | Purpose | Key Output |
|------|---------|------------|
| `hs_audit.py` | Audit trail with 16 breakpoints | Chain-hashed operation records |
| `hs_controller.py` | Industrial state machine + Hˢ-GOV | Event-driven controller with governance |

### Ingest Layer

| File | Purpose | Key Output |
|------|---------|------------|
| `hs_ingest.py` | Universal CSV/JSON loader | Pipeline-ready data matrix |
| `hs_hepdata.py` | HEPData fetch (8 curated datasets) | Published HEP compositions |

---

## Data Flow

```
Raw CSV/JSON
    │
    ▼
hs_ingest.py ──────────────────► numpy array (N×D)
    │                                   │
    │  (or hs_hepdata.py)               │
    │                                   ▼
    │                     higgins_decomposition_12step.py
    │                            │
    │                     ┌──────┴──────┐
    │                     │  12 Core    │
    │                     │  Steps      │
    │                     │  + Extended │
    │                     │  Panel      │
    │                     └──────┬──────┘
    │                            │
    │                            ▼
    │                     results dict
    │                     ┌──────┴───────────────────┐
    │                     │              │            │
    │                     ▼              ▼            ▼
    │               hs_codes.py   hs_fingerprint.py  hs_reporter.py
    │               (78 codes)    (SHA-256 hash)     (5 languages)
    │                     │              │            │
    │                     └──────┬───────┘            │
    │                            │                    │
    │                            ▼                    │
    │                     hs_audit.py                 │
    │                     (chain hash)                │
    │                            │                    │
    │                     ┌──────┴──────┐             │
    │                     ▼             ▼             │
    │              hs_testgen.py  hs_metrology.py     │
    │              (test scripts) (quality metrics)   │
    │                                                 │
    └─────────────────────────────────────────────────┘
```

---

## Diagnostic Code System

**78 codes across 12 prefixes:**

| Prefix | Stage | Count | Examples |
|--------|-------|-------|---------|
| GD | Input Guards | 6 | GD-D2M-ERR, GD-NAN-ERR |
| S4 | Closure | 3 | S4-CLO-INF, S4-ZRP-INF |
| S5 | CLR Transform | 1 | S5-CLR-INF |
| S6 | Variance | 3 | S6-VAR-INF, S6-RNG-INF |
| S7 | HVLD | 5 | S7-BWL-INF, S7-HIL-INF |
| S8 | Squeeze | 6 | S8-NAT-INF, S8-FLG-WRN |
| S9 | EITT | 9 | S9-ENT-INF, S9-CHS-INF |
| SA-SC | Geometry | 3 | SA-TRN-INF, SB-CPX-INF |
| XU | Extended Universal | 18 | XU-PCC-INF, XU-FPR-INF, XU-CPM-INF |
| XC | Extended Conditional | 12 | XC-PID-INF, XC-TEE-INF |
| RP | Report | 3 | RP-CMP-INF, RP-VER-INF |

**Severity levels:** INF (informational), WRN (warning), ERR (error), DIS (discovery), CAL (calibration)

**10 Structural Modes:** SM-OVC-CAL, SM-MCA-WRN, SM-BPO-DIS, SM-TNT-DIS, SM-RTR-DIS, SM-DGN-WRN, SM-DMR-DIS, SM-CPL-DIS, SM-IND-DIS, SM-SCG-INF

---

## Breakpoint System

**16 breakpoints with 4 possible actions each:**

| Phase | Breakpoints | Default (permissive) |
|-------|-------------|---------------------|
| Pre-run | BP-PRE-RUN | CONTINUE |
| Core pipeline | BP-POST-GUARD, BP-POST-CLOSURE, BP-POST-CLR, BP-POST-VARIANCE, BP-POST-HVLD, BP-POST-SQUEEZE, BP-POST-EITT, BP-POST-GEOMETRY | CONTINUE |
| Post-processing | BP-POST-EXTENDED, BP-POST-CODES, BP-POST-FINGER | CONTINUE |
| Conditional | BP-ON-ERROR, BP-ON-FLAG, BP-ON-GUARD-FAIL | CONTINUE |
| Loop control | BP-LOOP-ITER, BP-LOOP-END | CONTINUE |

**Actions:** CONTINUE, HOLD, ABORT, LOG_ONLY

**Presets:** permissive, cautious, strict, audit, development

---

## Experiment Registry (25 Experiments)

| ID | Name | Domain | Carriers |
|----|------|--------|----------|
| Hs-01 | Gold/Silver | COMMODITIES | 2 |
| Hs-02 | US Energy | ENERGY | 4 |
| Hs-03 | Nuclear SEMF | NUCLEAR | 5 |
| Hs-04 | Bessel Acoustics | ACOUSTICS | 3 |
| Hs-05 | Geochemistry | GEOCHEMISTRY | 8 |
| Hs-06 | Fusion | ENERGY | 3 |
| Hs-07 | QCD | QCD | 6 |
| Hs-08 | CKM/PMNS | PARTICLE | 3 |
| Hs-09 | Stellar | ASTROPHYSICS | 3 |
| Hs-10 | GW150914 | GRAVITY | 3 |
| Hs-11 | AME2020 | NUCLEAR | 5 |
| Hs-12 | Spring Mass | FORCE | 3 |
| Hs-13 | Steel | MATTER | 3 |
| Hs-14 | Conjugate Pairs | SIGNAL_THEORY | varied |
| Hs-15 | hBN Dielectric | MATERIALS | 3 |
| Hs-16 | Planck Cosmic | COSMOLOGY | 4 |
| Hs-17 | Backblaze | ENGINEERING | varied |
| Hs-18 | Urban Markham | URBAN | varied |
| Hs-19 | Traffic Signals | URBAN | varied |
| Hs-20 | Conversation Drift | AI_SAFETY | 3 |
| Hs-21 | Reference Standards | CALIBRATION | varied |
| Hs-22 | Natural Pairs | CROSS_DOMAIN | varied |
| Hs-23 | Radionuclides | NUCLEAR | varied |
| Hs-24 | HEPData Validation | HEP_COLLIDER | varied |
| Hs-25 | Cosmic Energy Budget | COSMOLOGY | 5 |

---

## Governance Modes

| Mode | Preset | Max Concurrent | Behaviour |
|------|--------|---------------|-----------|
| OPEN | Any | Unlimited | Controllers run freely, events logged |
| SUPERVISED | Cautious | 5 | Policy checks on transitions |
| LOCKED | Strict | 1 | All FLAG results require approval |
| QUARANTINE | N/A | 0 | No new runs, all controllers frozen |

---

## Authority Stack

1. `HS_MACHINE_MANIFEST.json` — Structure and navigation (highest)
2. `HS_ADMIN.json` — Identity, terminology, communication standards
3. Reference standard library — Calibration values and thresholds
4. Accumulated experiment results — Validated chain of evidence
5. Individual experiment results — Newest, lowest authority until regression-tested
6. Archive — Historical context, not active authority (lowest)

---

*The instrument reads. The expert decides. The loop stays open.*
*Peter Higgins, 2026*
