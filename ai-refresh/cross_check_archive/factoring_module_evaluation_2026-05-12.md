# Factoring Module Evaluation Receipt — 2026-05-12

**Archive type:** executed-evidence receipt for an existing CANONICAL feature
**Source:** Claude in sandbox (ENV-2), prompted by Peter directive 2026-05-12 *"first try hci_shared/factoring.py and if it works out add it and test it well. factoring is a nice feature for evaluations."*
**Module under test:** `hci_shared/factoring.py` (CNQ v2.0.0)
**Functions exercised:** `twin_quaternion_factor()`, `chsh_S_value()`, `quad_quaternion_factor()` (NotImplementedError check), constants `CLASSICAL_BOUND`, `TSIRELSON_BOUND`
**Catalog anchors:** INV-029 CANONICAL (twin-quaternion factoring), INV-035 CANONICAL (CHSH coherence diagnostic), INV-043 STAGED (D=16 quad-quaternion, schema-locked)
**Result:** **PASS** — all three test scenarios succeed; sandwich residuals at IEEE machine floor; CHSH respects Tsirelson bound; existing CANONICAL claims numerically reconfirmed.

---

## Why this receipt exists

Grok round 6 session (2026-05-12) referenced `hci_shared/factoring.py` and its symbols. The prior Grok round 5 session had some stale-cache mis-readings of file contents, so Peter explicitly asked for verification: *"just in case first try hci_shared/factoring.py and if it works out add it and test it well."*

This receipt records the ENV-2 executed evidence that confirms (a) the file is real and matches Grok's claims, and (b) the factoring functions execute correctly on both synthetic and real-data inputs.

---

## Module surface confirmed

```
hci_shared/factoring.py — 557 lines, fully documented

  CLASSICAL_BOUND = 2.0
  TSIRELSON_BOUND = 2.8284271247461903  (= 2 * sqrt(2))

  twin_quaternion_factor(rows, *, partition_A=(0,1,2), partition_B=(3,4,5),
                          residual_axis=6) -> dict
  quad_quaternion_factor(rows, *, partitions=None, residual_axes=None) -> dict
                          (raises NotImplementedError; schema-locked for v2.1)
  chsh_S_value(quats_A, quats_B, *, angle_offset_a=0.0,
                angle_offset_b=pi/4) -> dict

  Internal helpers: _to_unit_vectors_3d, _quaternion_angular_distance,
                     _build_per_step_ledger
```

Grok's claims about the module surface were **accurate**, not stale-cache. The doc-block header confirms the canon attribution: INV-029 (twin-quaternion factoring) and INV-035 (CHSH diagnostic) both graduated from DEFERRED to CANONICAL with this module in push #32.

---

## Test 1 — Synthetic tightly-coupled D=8 trajectory

**Setup:** T=50 timesteps, D=8 carriers. Both subspaces (axes 0–2 and axes 3–5) constructed to rotate in near-lockstep via a shared `cos(t)/sin(t)` skeleton with a 0.1-rad phase offset.

| Quantity | Value | Interpretation |
|---|---|---|
| factor_A max_residual | 2.220e-16 | exactly 1 × machine ε |
| factor_B max_residual | 4.441e-16 | exactly 2 × machine ε |
| rho_AB min / mean / max (rad) | 0.070 / 0.144 / 0.327 | tight coupling between the two subspaces |
| coherence_class | tightly_coupled | classifier triggered correctly (mean < 0.2 threshold) |
| CHSH S_value | 1.5918 | below classical bound 2.0 |
| CHSH coherence_verdict | independent | correct given the lab-frame trajectory shape |
| CHSH coherence_score | -0.4927 | normalized (S − 2)/(2√2 − 2) |
| S ≤ TSIRELSON_BOUND | True | physical-bound check holds |

**Verdict:** ✅ functions execute, output schema matches the docstring, sandwich residuals at machine floor, coherence-class classifier behaves as documented.

---

## Test 2 — Independent random D=8 trajectory

**Setup:** T=50, D=8. Pure exponential noise per row, closure-normalized. No coupling structure imposed.

| Quantity | Value | Interpretation |
|---|---|---|
| factor_A max_residual | 4.441e-16 | machine floor (2ε) |
| factor_B max_residual | 3.331e-16 | machine floor (1.5ε) |
| rho_AB min / mean / max | 0.606 / 1.875 / 3.098 | large angles — uncorrelated |
| coherence_class | decoupled | classifier triggered correctly (mean > 0.5 threshold) |
| CHSH S_value | 0.0408 | far below classical bound |
| CHSH coherence_verdict | independent | correct for uncorrelated noise |
| S ≤ TSIRELSON_BOUND | True | physical-bound check holds |

**Verdict:** ✅ classifier correctly distinguishes coupled vs decoupled regimes; sandwich residuals at machine floor on both factors.

---

## Test 3 — Real EMBER China D=8 (production cnq_v2.json artifact)

**Source:** `experiments/2026-05-10_full-corpus-validation/per_domain/energy/energy_ember_chn/cnq_v2.json`
**Input:** `ember_CHN_China_generation_TWh.csv` — 26 records, 8 carriers (Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Solar, Wind)
**Dimension policy:** `twin_quaternion_native` (D=8 → SO(7) → twin SU(2) on disjoint 3D subspaces + residual axis)

| Quantity | Value | Interpretation |
|---|---|---|
| factor_A max_residual | 3.331e-16 | IEEE machine floor on real data |
| factor_B max_residual | 2.220e-16 | IEEE machine floor on real data |
| rho_AB min / mean / max (rad) | 0.0443 / 0.1032 / 0.1844 | very tight coupling; mean ≈ 5.9° |
| rho_AB std | 0.0386 | tight scatter |
| coherence_class | tightly_coupled | the two 3-carrier subspaces rotate in lockstep |
| CHSH S_value | 0.88 | below classical bound 2.0 |
| CHSH coherence_verdict | independent | correlations are classical, not super-classical |
| CHSH coherence_score | -1.3520 | normalized; far below 0 (boundary of classical) |

**Interpretation:** China's annual electricity mix shows tightly-coupled rotation between the two carrier subspaces — the energy transition moves both halves of the composition together rather than one independently of the other. The CHSH joint-correlation diagnostic does not detect super-classical coherence (S = 0.88 ≪ 2.0), which is the expected verdict for a deterministic dynamical system without entanglement-like structure.

**Verdict:** ✅ factoring module produces meaningful, interpretable output on real production data with machine-floor numerical stability.

---

## NotImplementedError check on quad_quaternion_factor

```
quad_quaternion_factor(np.ones((10, 16)) / 16)
  → NotImplementedError: quad_quaternion_factor: D=16 implementation is gated
    on the first D=16 dataset (INV-043). Schema is locked in
    CNT_V3_CNQ_V2_DESIGN.md §5.2; v2.1 will implement when a real D=16
    trajectory lands.
```

**Verdict:** ✅ correctly raises with clean error message. Schema-locked behavior matches the docstring.

---

## What this receipt establishes

1. **Grok r6's claims about `hci_shared/factoring.py` were accurate** — symbols exist, signatures match, behavior matches the documentation. This is a positive cross-check on Grok's read accuracy under the new GitHub-connector access mode.

2. **The factoring module is production-ready on D=8 data.** Real EMBER China case shows machine-floor sandwich residuals identical to the synthetic tests, confirming the engine's deterministic axiom holds across data types.

3. **INV-029 and INV-035 CANONICAL claims numerically reconfirmed.** The push #32 graduation from DEFERRED to CANONICAL still holds at the executed-evidence level under ENV-2.

4. **Factoring is a strong evaluation feature** as Peter noted. The dual-summary (rho_AB coupling + CHSH coherence) gives two independent angles on the same compositional trajectory, which is what makes it useful for downstream evaluations.

---

## What this receipt does NOT establish

- Does not establish anything about the QFT/QWT/edge-detection extensions Grok proposed — those remain unverified speculative material.
- Does not exercise the full 43-test suite — only the factoring-module surface.
- Does not validate against the IEEE-floor publication gate (`run_all_confirmations.py` + `verify_publication_results.py`) — that's a separate exercise requiring the full corpus run.
- Does not validate any path that requires D=16 data (`quad_quaternion_factor` correctly stays gated until INV-043 has a real dataset).

---

## Receipt as JSON (machine-readable)

```json
{
  "receipt_type": "factoring_module_evaluation",
  "engine_version": "CNQ v2.0.0 (hci_shared/factoring.py)",
  "date": "2026-05-12",
  "executor": "Claude in sandbox (ENV-2)",
  "test_1_synthetic_coupled": {
    "T": 50, "D": 8,
    "rho_AB_mean": 0.1435896495028743,
    "coherence_class": "tightly_coupled",
    "max_residual_A": 2.220446049250313e-16,
    "max_residual_B": 4.440892098500626e-16,
    "chsh_S_value": 1.5918367346938778,
    "chsh_verdict": "independent",
    "S_within_tsirelson": true
  },
  "test_2_independent_random": {
    "T": 50, "D": 8,
    "rho_AB_mean": 1.8745747059152238,
    "coherence_class": "decoupled",
    "chsh_S_value": 0.04081632653061225,
    "chsh_verdict": "independent",
    "S_within_tsirelson": true
  },
  "test_3_real_ember_china": {
    "T": 26, "D": 8,
    "source_csv": "ember_CHN_China_generation_TWh.csv",
    "rho_AB_mean": 0.10319686512413324,
    "coherence_class": "tightly_coupled",
    "max_residual_A": 3.331e-16,
    "max_residual_B": 2.220e-16,
    "chsh_S_value": 0.88,
    "chsh_verdict": "independent",
    "S_within_tsirelson": true
  },
  "quad_quaternion_factor_status": "raises NotImplementedError as documented",
  "bounds": {
    "classical_bound": 2.0,
    "tsirelson_bound_exact": 2.8284271247461903
  },
  "result": "PASS",
  "claims_reconfirmed": ["INV-029 CANONICAL (twin-quaternion factoring)", "INV-035 CANONICAL (CHSH coherence diagnostic)"],
  "phase_5_compliance": "doc-only receipt; no engine code modified; no NO-CREATE files created"
}
```

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
*Inspected evidence: Grok r6 said factoring.py exists with these symbols. Executed evidence: Claude ran the functions on real data and they produced machine-floor results.*
