# HCI Dyadic Coupling Ladder

**Investigation:** INV-028
**Disposition:** DEFERRED (push #26)
**Status:** experimental Stage 4 / Stage 5 diagnostic; no working pilot.

---

## Concept

A tensor-analysis ladder for compositional structure that lives in *relationships between relationships*, not just in carriers or carrier-pairs.

| Order | Object | Index structure | Detects |
|---|---|---|---|
| 2 | κᴴˢ_ij(t) | two indices | carrier-pair metric coupling (current core) |
| 4 | C_ijkl | four indices | pair-of-pairs coupling, hidden multi-attractor structure |
| 8 | B_ijklmnop | eight indices | block-of-blocks coupling — only when order-4 structures themselves become objects of comparison |

This is a recursive **dyadic** ladder: each step bundles the previous step's relational structure into a new relational object. It is NOT a general tensor-rank rule — orders need not jump 2 → 4 → 8 in arbitrary tensor analysis. It's the natural ladder when the analytic question keeps recursively asking "how do the relations relate?"

---

## Order-4 (the immediate next step)

The order-4 object is the natural candidate for:

- multi-attractor detection
- pair-of-pairs coupling
- parallel processing of carrier pairs
- higher-degree carrier interaction fields
- structure that does not live in any single κᴴˢ_ij channel

Definition:

&nbsp;&nbsp;&nbsp;&nbsp;**C_ijkl = Cov_t( κᴴˢ_ij(t), κᴴˢ_kl(t) )**

Meaning: how does the metric coupling of carrier pair (i,j) co-vary with the metric coupling of carrier pair (k,l) across time?

This is exactly the type of object you want when CNT's per-pair κ channels are individually well-behaved but the SYSTEM exhibits structure invisible to per-pair analysis.

## Order-8 (the recursive dyadic step)

If order-4 structures are themselves the object of comparison, the natural extension is an order-8 tensor:

&nbsp;&nbsp;&nbsp;&nbsp;**B_ijklmnop = Cov( C_ijkl, C_mnop )**

This is only motivated when:
- Multiple order-4 attractors are detected, AND
- They themselves exhibit relational structure across time or domain.

Order-8 should NOT be invoked speculatively. The order-4 step has to land first, and an order-4 attractor structure has to exist for an order-8 object to be analytically meaningful.

---

## Distinction from D=8 carriers

Important terminology hygiene (per ChatGPT round-2 audit):

- **Order-8 tensor**: an object with 8 indices.
- **D=8 composition**: a composition with 8 carriers, which CNQ may factor into two coupled quaternion paths via [bi-quaternion factoring](CNQ_BIQUATERNION_FACTORING.md).

These are *related but not identical*. A D=8 trajectory does not require an order-8 tensor; bi-quaternion factoring lives in the algebra of two SU(2) factors. An order-8 tensor would only enter if the order-4 covariance objects of a D=8 system themselves needed comparison.

The dyadic coupling ladder lives at the **tensor-analysis** layer; bi-quaternion factoring lives at the **algebra** layer. They support each other but are different structures.

---

## Connection to bi-quaternion factoring

When a D=8 trajectory is factored into two coupled quaternion paths q_A(t), q_B(t):

- **Bi-quaternion factoring** asks: how do the two factors interact? (R_AB(t), ρ_AB)
- **Dyadic coupling ladder** asks: how does the per-pair metric coupling of q_A's carriers co-vary with that of q_B's carriers? (C_ijkl with i,j ∈ A's carriers and k,l ∈ B's)

The two views answer different questions on the same underlying data. A push that promotes either should consider the other in parallel.

---

## Promotion gate

For this concept to graduate from DEFERRED to CANDIDATE in the Investigation Catalog:

> Working pilot showing C_ijkl detects an attractor or coupling structure that order-2 κᴴˢ_ij misses, on a real corpus experiment (or a synthetically constructed test case where the multi-attractor structure is known a priori).

For graduation from CANDIDATE to CONFIRMED:

> Demonstrated value-add on at least two unrelated corpus experiments, with documented per-experiment results published to `HCI-CNQ/results/`.

---

## Schema sketch

If this concept is implemented in a future engine version, the suggested schema is:

```json
{
  "dyadic_coupling_ladder": {
    "order_2_metric": "kappa_HS_ij(t)",
    "order_4_pair_coupling": "C_ijkl = Cov_t(kappa_HS_ij(t), kappa_HS_kl(t))",
    "order_8_block_coupling": "B_ijklmnop = Cov(C_ijkl, C_mnop)",
    "order_4_per_pair_summary": [
      {
        "pair_a": ["carrier_i", "carrier_j"],
        "pair_b": ["carrier_k", "carrier_l"],
        "C_value": 0.0,
        "interpretation": "candidate label, e.g. 'orthogonal regimes', 'coupled attractor'"
      }
    ],
    "status": "experimental_stage4",
    "use_case": [
      "multi-attractor detection",
      "pair-of-pairs coupling",
      "higher-degree carrier interaction",
      "parallel processing of carrier pairs"
    ]
  }
}
```

---

## What this is NOT (yet)

- Not a Paper 1 requirement. Paper 1 stays on order-2 κᴴˢ and the D=4 quaternion sandwich.
- Not part of cnq.py v1.0.0.
- Not promotable until a working pilot exists.
- Not a substitute for κᴴˢ_ij — the order-2 metric remains the core CNT diagnostic.

---

## Cross-references

- Bi-quaternion factoring: [`CNQ_BIQUATERNION_FACTORING.md`](CNQ_BIQUATERNION_FACTORING.md)
- Investigation Catalog: [`../ai-refresh/INVESTIGATION_CATALOG.md`](../ai-refresh/INVESTIGATION_CATALOG.md) → INV-028
- Status & maturity: [`STATUS_AND_MATURITY.md`](STATUS_AND_MATURITY.md)
- Origin of the concept: ChatGPT round-2 audit conversation (push #26 narrative).
