# CNQ Twin-Quaternion Factoring (legacy filename: CNQ_BIQUATERNION_FACTORING.md)

**Investigation:** INV-029
**Disposition:** DEFERRED (push #26; terminology corrected in push #27)
**Status:** experimental D=8 algebraic extension; scaffolded in cnq.py via the `bi_quaternion_factoring_candidate` dimension label, not yet implemented as a working pilot.

---

## Terminology note (push #27)

This document was originally titled "CNQ Bi-Quaternion Factoring." Per the [Notation and Terminology canonical reference](../HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md) §7 / §12 (push #27), the formal name for the SU(2) × SU(2) factoring described here is **twin-quaternion factoring**. The term **bi-quaternion** in strict mathematical usage refers to elements of ℍ ⊗ ℂ (the standard Lorentz-physics / Clifford-algebra meaning), which is a different object.

The legacy filename and the dimension-policy label `bi_quaternion_factoring_candidate` in cnq.py v1.0.0 are preserved for repo-history continuity. Future engine versions and downstream documents should use **twin-quaternion** in body text, with `bi_quaternion_factoring_candidate` retained as a backwards-compatible identifier.

---

## Concept

For a D=8 compositional trajectory, the natural algebraic extension of the D=4 quaternion view is to factor the trajectory into **two coupled quaternion paths**. The mathematical home is the SO(8) ⊃ SU(2) × SU(2) decomposition; the algebraic object is **two coupled unit quaternions q_A and q_B with a documented coupling channel R_AB** — a twin-quaternion factoring, NOT a bi-quaternion (ℍ ⊗ ℂ) in the strict mathematical sense.

```
D = 8 composition
  -> ILR / orthonormal frame in R^7
  -> factor into two 3D quaternion navigation frames
  -> q_A(t), q_B(t)
  -> within-factor dynamics: angle_A, angle_B, parity_A, parity_B
  -> cross-factor dynamics: R_AB(t) = q_A(t) * q_B(t)^{-1}
  -> factor correlation: rho_AB
```

---

## Why D=8 is the natural site

| D | Algebra | CNQ status |
|---|---|---|
| 4 | SU(2) cover of SO(3) | native quaternion (load-bearing, confirmed) |
| 8 | SO(8) ⊃ SU(2) × SU(2) | **bi-quaternion factoring candidate** |
| ≥9 | Cl(D-1) Clifford extension or dominant-mode reduction | deferred (no current implementation) |

D=8 is the smallest dimension where the trajectory naturally admits the *two coupled quaternion paths* reading. This is qualitatively different from D=5, 6, 7 (which currently fall back to the projected R^3 view in cnq.py v1.0.0) because at D=8 the algebra has its own structure to exploit — not a projection, but a factoring.

---

## EMBER as the first-pilot candidate

The EMBER electricity-mix corpus contains country trajectories at D=8 (eight power-source carriers): coal, oil, gas, nuclear, hydro, wind, solar, other-renewables. In a bi-quaternion factoring, a natural domain partition is:

- **Factor A (q_A):** fossil sub-mix (coal, oil, gas, "other fossil" if present)
- **Factor B (q_B):** non-fossil sub-mix (nuclear, hydro, wind, solar, biomass)

Then the cross-factor product R_AB(t) measures *how the fossil-mix attitude rotates relative to the non-fossil-mix attitude* over the trajectory, and rho_AB measures their correlation.

If a country undergoing a clean-energy transition shows q_A and q_B with anti-correlated rotation (fossil mix rotating one way, non-fossil rotating the other, R_AB tracking the transition timeline), that is a *domain-meaningful signal* CNT alone does not directly expose.

---

## Promotion gate

For DEFERRED → CANDIDATE:

> Working pilot on EMBER D=8 country trajectory (recommended: countries with clear transition signal, e.g. Germany, UK, Denmark) showing factor-correlation rho_AB carries domain-meaningful signal. Compare against parent CNT termination/IR class for cross-validation.

For CANDIDATE → CONFIRMED:

> Demonstrated on at least two unrelated D=8 corpora (EMBER + one other), with the algebraic factoring producing diagnostic value beyond the per-channel CNT analysis. Implementation lands in cnq.py via a `--bi-quaternion` flag with deterministic output.

---

## Schema sketch (if implemented)

```json
{
  "bi_quaternion_factoring": {
    "dimension": 8,
    "algebra": "SO(8) ⊃ SU(2) × SU(2)",
    "factor_A": {
      "carriers": ["coal", "oil", "gas"],
      "q_path": [[w0,x0,y0,z0], ...],
      "interpretation": "fossil sub-mix attitude"
    },
    "factor_B": {
      "carriers": ["nuclear", "hydro", "wind", "solar", "biomass"],
      "q_path": [[w0,x0,y0,z0], ...],
      "interpretation": "non-fossil sub-mix attitude"
    },
    "cross_factor_product_R_AB": [...],
    "factor_correlation_rho_AB": 0.0,
    "interpretation_hint": "anti-correlated rotation indicates ongoing transition",
    "status": "candidate_pending_round3_or_ember_validation"
  }
}
```

---

## Connection to dyadic coupling

When bi-quaternion factoring lands, the natural companion analysis is the [HCI Dyadic Coupling Ladder](HCI_DYADIC_COUPLING_LADDER.md):

- **Bi-quaternion factoring** answers: *what is the algebraic structure of the two coupled paths?*
- **Dyadic coupling ladder** answers: *what is the order-4 tensor structure of the per-pair metric couplings between the two factor groups?*

Both views on the same data. Both DEFERRED until a pilot lands.

---

## What this is NOT (yet)

- Not part of cnq.py v1.0.0's runtime — only the dimension label `bi_quaternion_factoring_candidate` is wired in. The actual factoring code is intentionally not implemented until a pilot has the green light.
- Not a Paper 1 claim. Paper 1 is the D=4 universality wedge.
- Not a substitute for the D=4 native quaternion result — it is an algebraic extension to D=8, with its own gate.
- Not equivalent to the order-8 dyadic tensor — see [`HCI_DYADIC_COUPLING_LADDER.md`](HCI_DYADIC_COUPLING_LADDER.md) for the distinction.

---

## Cross-references

- Dyadic coupling ladder: [`HCI_DYADIC_COUPLING_LADDER.md`](HCI_DYADIC_COUPLING_LADDER.md)
- Tier system context: [`tier_system/CNQ_TIERED_SYSTEM.md`](tier_system/CNQ_TIERED_SYSTEM.md), [`tier_system/CNQ_VS_CODA_VS_CNT_COMPARE.md`](tier_system/CNQ_VS_CODA_VS_CNT_COMPARE.md)
- Engine proposal (parent doc): [`tier_system/CNQ_ENGINE_PROPOSAL.md`](tier_system/CNQ_ENGINE_PROPOSAL.md)
- Investigation Catalog: [`../ai-refresh/INVESTIGATION_CATALOG.md`](../ai-refresh/INVESTIGATION_CATALOG.md) → INV-029
- Origin of formal proposal: ChatGPT round-2 audit conversation (push #26 narrative).
