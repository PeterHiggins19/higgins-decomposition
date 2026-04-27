# Hˢ Learning Path
## From Zero to Compositional Knowledge Engine

**Author:** Peter Higgins, Markham, Ontario, Canada
**Version:** 1.0 — April 2026
**Prerequisite:** Basic familiarity with Python and data analysis. No CoDa training required to start.

---

## Who This Is For

This learning path serves three audiences: the **practitioner** who wants to analyse their own data, the **researcher** who wants to understand the mathematics, and the **integrator** who wants to embed Hˢ in a larger system. Each section marks which audience it serves.

---

## Level 1 — Run Your First Analysis (Practitioner)

**Goal:** Get a compositional diagnosis from your own data in under 5 minutes.

**Step 1: Prepare your data.** You need a CSV where each row is an observation and each column is a carrier (a part of a whole). The parts should sum to a constant — 1.0, 100%, or any fixed total. If they don't, Hˢ will close them to the simplex for you.

**Step 2: Run the pipeline.**

```bash
cd tools/pipeline
python hs_ingest.py mydata.csv --all-languages
```

This produces: a results JSON (full numeric output), diagnostic reports in 5 languages, and a console summary showing classification (NATURAL, INVESTIGATE, or FLAG), the nearest transcendental constant, and all diagnostic codes.

**Step 3: Read your report.** Open the English report file. It tells you: what shape the variance trajectory takes (bowl or hill), how close the system is to a transcendental constant, whether entropy is preserved under decimation, and what structural modes were detected.

**What you have now:** A complete compositional diagnosis of your data. If it says NATURAL, your system has the geometric fingerprint of a naturally-partitioned composition. If FLAG, the composition has unusual structure worth investigating.

---

## Level 2 — Understand What Happened (Researcher)

**Goal:** Learn what the 12 pipeline steps actually compute.

**The Pipeline:**

1. **Define System** — Name, domain, and carrier labels are registered. This is metadata, not computation.

2. **Identify Carriers** — The D columns of your CSV become the D compositional parts. D must be at least 2.

3. **Load Data** — Your N×D matrix enters the pipeline. N must be at least 5. No NaN or Inf allowed. The scale ratio (max/min of non-zero values) must be below 10¹⁵. These are the 4 input guards.

4. **Close to Simplex** — Every row is divided by its sum, so all rows now sum to 1.0. Zeros are replaced with a small multiplicative constant (10⁻⁶) to allow logarithms. This is standard CoDa practice (Aitchison, 1982).

5. **CLR Transform** — The centred log-ratio transform maps each closed composition to real-valued coordinates: CLR(x) = ln(x) - mean(ln(x)). This is the standard Aitchison geometry transform that allows Euclidean operations on compositional data.

6. **Aitchison Variance** — The cumulative Aitchison variance σ²_A(t) is computed as a running total across the observation index. This trajectory is the geometric fingerprint — its shape tells you whether the system is converging (bowl) or diverging (hill).

7. **HVLD** — The Higgins Vertex Lock Diagnostic fits a quadratic to the variance trajectory. The sign of the quadratic coefficient determines bowl (positive, concave-up) or hill (negative, concave-down). The R² of the fit measures how clean the shape is.

8. **Transcendental Super Squeeze** — The final variance value is compared to 35 transcendental constants (π, e, φ, √2, Euler-γ, Catalan, Apéry, Khinchin, etc.). The nearest constant and its proximity δ are recorded. A δ below 1% of the constant's value marks a match.

9. **EITT Entropy** — Shannon entropy H is computed on the simplex. The data is decimated by geometric-mean subsampling (every 2nd, 4th, 8th row). If entropy is preserved under decimation, the system passes the EITT (Entropy Invariance Through Thinning) test.

10. **Ternary Projection** — For D=3, barycentric coordinates are computed for visualisation on a ternary diagram.

11. **Complex Plane** — Each observation is mapped to a point in the complex plane relative to the composition centroid.

12. **Helix Embedding** — A 3D helix embedding (radius, angle, time) shows the trajectory of the composition over the observation index.

**Extended Panel (post-pipeline):** After the 12 core steps, an extended analysis computes per-carrier contributions, transfer entropy between carriers, ratio pair stability, drift direction, PID decomposition, and structural mode detection.

**Key Documents:**
- `docs/reference/Higgins_Decomposition_Reference_v1.0.docx` — Full mathematical specification
- `docs/theory/Grok_Mathematical_Foundation_Notes.md` — Mathematical foundations
- `papers/flagship/Higgins_Decomposition_Character_Analysis.docx` — Character analysis with adversarial testing

---

## Level 3 — Compare Against Reference Standards (Researcher / Practitioner)

**Goal:** Understand how your data compares to known baselines.

Hˢ maintains two specification books:

**Reference Standard Library** (15 standards) — `docs/reference/Hs_Reference_Standard_Library.md`
These define the performance envelope: mathematical functions (Gaussian, Sinc, Sech), diffraction patterns (circular piston, rectangular aperture, Babinet), transcendental anchors (sin/cos, Fibonacci, e-family), and noise floor (uniform random, Gaussian noise, near-constant). Your DUT result can be positioned relative to the ceiling (perfect mathematical partition), the physical standard (diffraction boundary), and the floor (random noise).

**Natural Pairs Baseline** (7 pairs across 12 systems) — `docs/reference/Hs_Natural_Pairs_Baseline.md`
These are pairs of physical systems from different domains that share structural properties: Nuclear SEMF paired with DT Fusion (same energy partition physics), Planck Cosmic paired with QCD (fundamental composition at opposite scales). Cross-pair constant sharing reveals geometric connections across domains.

---

## Level 4 — Use the Knowledge Engine Tools (Practitioner / Integrator)

**Goal:** Generate fingerprints, run audited pipelines, and use the self-generating test tools.

**Fingerprinting** — Every pipeline run produces a deterministic SHA-256 fingerprint from the geometric identity vector (shape, R² band, classification, constant family, EITT result, structural modes, chaos level, drift). Two systems with similar fingerprints share compositional geometry regardless of domain.

```bash
python hs_fingerprint.py results.json -o fingerprint.json
python hs_fingerprint.py --catalog experiments/Hs-24_HEPData_Validation/
python hs_fingerprint.py --match fingerprint.json --database experiments/
```

**Audited Pipeline** — The audit system wraps every pipeline operation in a tamper-evident record: input hash, output hash, timestamp, duration, status, breakpoint decision. The chain hash (SHA-256 of the sequential record) detects any modification.

```bash
python hs_audit.py --preset cautious --run mydata.csv -v
python hs_audit.py --view audit_trail.json
python hs_audit.py --list-breakpoints
```

Breakpoint presets: permissive (no stops), cautious (hold on FLAG/errors), strict (abort on errors), audit (log everything), development (hold at every step).

**Test Generation** — The tool makes tools. From any catalog of results, Hˢ generates self-contained test scripts:

```bash
python hs_testgen.py --regression experiments/         # regression suite
python hs_testgen.py --healthcheck results.json        # perturbation stability
python hs_testgen.py --crosscheck db1/ db2/            # cross-database fingerprint comparison
python hs_testgen.py --stability results.json          # bootstrap subsampling
```

---

## Level 5 — Industrial Integration (Integrator)

**Goal:** Use Hˢ as a compositional analysis component inside a larger system.

**HsController** — A state machine that wraps the full pipeline:

```python
from hs_controller import HsController

ctrl = HsController("RUN-001", "My System", "MY_DOMAIN",
                     carriers=["A", "B", "C"])
ctrl.start(data, preset="cautious")

# If the controller reaches HELD state (breakpoint hit):
status = ctrl.inspect()
ctrl.resume(decision="continue", notes="Expert reviewed — proceed")

result = ctrl.get_result()
audit = ctrl.get_audit()
events = ctrl.get_events()
```

States: IDLE → RUNNING → HELD/COMPLETED/ABORTED/ERROR. The event bus publishes typed events (state_change, classification, fingerprint, hold, error) for external subscribers.

**HUF-GOV** — Top-level governance for multi-controller deployments:

```python
from hs_controller import HufGov

gov = HufGov(mode="SUPERVISED")
cid = gov.register_controller(ctrl)
gov.run_controller(cid, data)

# Cross-run fingerprint comparison
gov.fingerprint_db  # all fingerprints from all controllers

# Emergency lockdown
gov.quarantine(reason="Anomaly detected in batch run")

# Persist full state
gov.save_state("gov_state.json")
```

Governance modes: OPEN (unrestricted), SUPERVISED (cautious default, max 5 concurrent), LOCKED (strict only, max 1), QUARANTINE (emergency lockdown).

---

## Level 6 — Extend the System (Researcher)

**Goal:** Add new experiments, languages, or capabilities.

**Add an experiment:** Create a folder `experiments/Hs-NN_Name/`, run the pipeline, save results JSON and reports. Update `ai-refresh/HS_SYSTEM_INVENTORY.json` with the new domain/system entry.

**Add a language:** Create a JSON file in `tools/pipeline/locales/` with translations for all 78 diagnostic codes and 10 structural modes. Zero code changes required.

**Add a diagnostic code:** Define the code in `CODE_DICTIONARY` in `hs_codes.py` with short and verbose descriptions, add the detection logic in `generate_codes()`, add translations to all 5 locale files.

**Add a reference standard:** Generate a mathematical partition, run the pipeline, add the results to the reference library with full metrology.

---

## Reading Order

For any audience, this is the recommended reading order:

1. This document (orientation)
2. `README.md` (overview and quick start)
3. `ai-refresh/HS_MACHINE_MANIFEST.json` (machine-readable system specification)
4. `ai-refresh/HS_ADMIN.json` (terminology and communication standards)
5. `EXECUTIVE_SUMMARY.md` (full development history)
6. `docs/reference/Hs_Reference_Standard_Library.md` (calibration baselines)
7. `docs/Hs_Applications_Guide.md` (domain applications — space, finance, nuclear, 10+ more)
8. `docs/Hs_High_Index_Platform_Guide.md` (streaming platform architecture)
9. `papers/codawork2026/Hs_CoDaWork2026_Executive_Summary.md` (conference strategy)
10. `papers/flagship/Higgins_Decomposition_Character_Analysis.docx` (character analysis)

For code exploration:

1. `tools/pipeline/higgins_decomposition_12step.py` (core pipeline)
2. `tools/pipeline/hs_codes.py` (diagnostic code dictionary)
3. `tools/pipeline/hs_reporter.py` (multilingual reporting)
4. `tools/pipeline/hs_fingerprint.py` (fingerprint generation)
5. `tools/pipeline/hs_audit.py` (audit trail and breakpoints)
6. `tools/pipeline/hs_controller.py` (industrial controller and HUF-GOV)
7. `tools/pipeline/hs_sensitivity.py` (Component Power Mapper)

---

## Canonical Counts (April 2026)

| Item | Count |
|------|-------|
| Physical domains | 18 |
| Distinct systems | 36 |
| Total DUTs | 53 |
| Experiments | 25 (Hs-01 through Hs-25) |
| Reference standards | 15 |
| Transcendental constants | 35 |
| Conjugate pairs | 13 |
| Diagnostic codes | 78 |
| Structural modes | 10 |
| Pipeline files | 12 |
| Interactive tools | 5 |
| Languages | 5 |
| Breakpoints | 16 |
| Controller states | 6 |
| Governance modes | 4 |
| Scale range | 44 orders of magnitude |

---

*The instrument reads. The expert decides. The loop stays open.*
*Peter Higgins, 2026*
