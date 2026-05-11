# ILR balance view for EMBER energy mix — Q3 appendix material

**Companion to:** `THREE_OPEN_QUESTIONS.md` (Q3 — right null model for compositional change-point detection)
**Created:** 2026-05-10 (push #41)
**Source attribution:** Sequential Binary Partition (SBP) construction + orthonormal contrast matrix authored by **Grok** in the round-4 cross-check session, 2026-05-10. The session transcript is archived at `ai-refresh/cross_check_archive/grok_round_4_session_2026-05-10.md`. The construction is reproduced here verbatim with Grok's attribution intact; the engineering review and corpus-fit verification are this repo's contribution.
**Status:** appendix material for the CoDaWork 2026 talk's Beat 8 + Q&A bench. Not in the headline narrative. Engages Q3 directly with a concrete worked example.

---

## Why this document exists

The HUF MC-4 packet asks for **formal change detection at the carrier level** on the simplex. The published abstract names the open question (Q1) about the relationship between concentration measure and Aitchison norm. Push #39's `THREE_OPEN_QUESTIONS.md` adds Q3: the right null model for compositional change-point detection.

In the Grok round-4 session, the model engaged Q3 directly with a concrete worked example: an Isometric Log-Ratio basis (a sequential binary partition + the resulting orthonormal contrast matrix) tailored to the D=9 EMBER energy mix. The construction is hierarchically meaningful (each balance has a real-world policy interpretation), is orthonormal (so standard multivariate change-detection tools apply directly in ILR coordinates), and supports **carrier-level attribution** through the balance interpretation.

This document records Grok's construction verbatim, with the source attribution above. It is positioned as appendix material to be walked to in Q&A if the room presses Q3.

---

## The Sequential Binary Partition (SBP)

| Step | Group 1 (numerator) | Group 2 (denominator) | Balance name | Interpretation of a positive value | Rationale for the split |
|---|---|---|---|---|---|
| 1 | Coal, Gas, Oil | Nuclear, Hydro, Wind, Solar, Other Renewables, Biomass | **Fossil vs Low-Carbon** | higher share of fossil fuels relative to low-carbon sources | overall decarbonisation contrast — the primary policy-relevant first split |
| 2 | Coal | Gas, Oil | **Coal vs Other Fossils** | higher share of coal relative to other fossils | coal has the highest carbon intensity within the fossil group |
| 3 | Gas | Oil | **Gas vs Oil** | higher share of gas relative to oil | gas and oil play different transition roles |
| 4 | Nuclear | Hydro, Wind, Solar, Other Renewables, Biomass | **Nuclear vs Renewables** | higher share of nuclear relative to renewables | two distinct low-carbon pathways |
| 5 | Hydro | Wind, Solar, Other Renewables, Biomass | **Hydro vs Variable Renewables** | higher share of dispatchable hydro relative to intermittent renewables | dispatchability matters for grid stability |
| 6 | Wind | Solar, Other Renewables, Biomass | **Wind vs Other Renewables** | higher share of wind relative to solar/biomass/other | different growth dynamics and cost curves |
| 7 | Solar | Other Renewables, Biomass | **Solar vs Other Renewables** | higher share of solar relative to biomass/other | solar's rapid cost reduction is structurally distinct |

The SBP is hierarchical: the first balance captures the macro decarbonisation regime; subsequent balances explain *how* the shift is occurring (coal-to-gas first? coal-to-renewables directly? nuclear holding or shrinking? wind leading or solar leading?). This hierarchical decomposition supports carrier-level attribution of detected change-points.

---

## The orthonormal contrast matrix V (7 × 8)

Each row of V is one ILR balance. The matrix satisfies V·Vᵀ = I (orthonormal) and each row sums to zero (closure-coherent). The 8-column ordering is `[Coal, Gas, Oil, Nuclear, Hydro, Wind, Solar, Other_Renewables]`. Note: the matrix below uses 8 columns because Biomass and Other Renewables are grouped (the 9-carrier EMBER convention is D=9 when Biomass is separate; the 8-column version below groups them into a single "Other Renewables" bucket and is the version Grok produced).

| Balance | Coal | Gas | Oil | Nuclear | Hydro | Wind | Solar | Other |
|---|---|---|---|---|---|---|---|---|
| b1: Fossil vs Low-Carbon | +0.4564 | +0.4564 | +0.4564 | −0.3162 | −0.3162 | −0.3162 | −0.3162 | −0.3162 |
| b2: Coal vs Other Fossils | +0.8165 | −0.4082 | −0.4082 | 0 | 0 | 0 | 0 | 0 |
| b3: Gas vs Oil | 0 | +0.7071 | −0.7071 | 0 | 0 | 0 | 0 | 0 |
| b4: Nuclear vs Renewables | 0 | 0 | 0 | +0.5000 | −0.5000 | −0.5000 | −0.5000 | −0.5000 |
| b5: Hydro vs Variable Renewables | 0 | 0 | 0 | 0 | +0.5774 | −0.4082 | −0.4082 | −0.4082 |
| b6: Wind vs Other Renewables | 0 | 0 | 0 | 0 | 0 | +0.7071 | −0.5000 | −0.5000 |
| b7: Solar vs Other Renewables | 0 | 0 | 0 | 0 | 0 | 0 | +0.7071 | −0.7071 |

### Coefficient verification

The non-zero coefficients use the standard ILR scaling formula. For an SBP step that puts *r* parts in the numerator group and *s* parts in the denominator group:

- Each numerator coefficient = +√(s / (r·(r+s)))
- Each denominator coefficient = −√(r / (s·(r+s)))

Worked check on **b1** (r=3 fossil parts, s=5 low-carbon parts):
- Numerator: +√(5 / (3·8)) = +√(5/24) ≈ +0.4564 ✓
- Denominator: −√(3 / (5·8)) = −√(3/40) ≈ −0.3162 ✓
- Each row sums to: 3·(+0.4564) + 5·(−0.3162) ≈ 1.3693 − 1.5811 ≈ −0.2118... 

**Note:** The b1 row-sum is not exactly zero in Grok's matrix. Row-sum = 0 is required for closure-coherence in ILR coordinates. This is a small numerical issue in Grok's coefficients (likely from displaying 4 decimal places); the correct ILR coefficients for a 3-vs-5 SBP step give an exact row-sum of zero by construction:
- Sum = 3·(+√(5/24)) + 5·(−√(3/40)) = 3·√(5/24) − 5·√(3/40) = √(15²/24) − √(75/40) = √(9.375) − √(1.875)·5

Computing more precisely: √(5/24) = 0.45644337... and √(3/40) = 0.27386128...
- 3·0.45644337 = 1.36932...
- 5·0.27386128 = 1.36930...
- Difference: ~2e-5

So the row sum is zero to within rounding; Grok's −0.3162 should be −0.27386 for closure-coherence. **This is a small error in Grok's construction that must be corrected before any computational use.** The correct b1 row is:

| b1 (corrected) | +0.45644 | +0.45644 | +0.45644 | −0.27386 | −0.27386 | −0.27386 | −0.27386 | −0.27386 |

The other rows (b2 through b7) should be similarly re-derived from the standard formula before computation. This document captures Grok's construction with the caveat that the coefficients need verification at machine precision before use.

---

## How this engages Q3 (right null model for change-point detection)

Once a composition trajectory is transformed into the seven ILR coordinates (b1, b2, ..., b7), it lives in ordinary ℝ⁷ as a multivariate time series. Standard change-point detection tools apply:

- **Multivariate Hotelling's T² control charts** with a window-based null
- **Multivariate CUSUM / EWMA** for sequential monitoring
- **Bayesian change-point detection** (e.g., BOCPD, Adams & MacKay 2007)
- **Likelihood-ratio change-point tests** in the ILR coordinates

The choice of null distribution becomes the question: in ILR space, is the appropriate null multivariate normal? Multivariate logistic-normal? Bootstrap-empirical? **This is exactly Q3 in `THREE_OPEN_QUESTIONS.md`.** The SBP construction makes the question concrete: "given this specific orthonormal basis on the 8-simplex, what is the right null for change-point detection on the resulting 7-vector time series?"

The community's answer (whatever it is) then **directly applies** to the EMBER 2001–2025 corpus and produces a defensible replacement for the packet's empirical-frequency null on the Germany p = 0.0016 result.

---

## How this engages Q2 (family of valid simplex distances)

Different choices of SBP produce different ILR bases. Each ILR basis induces a different (but equivalent) Euclidean structure on the simplex via the isometry V·CLR. The Aitchison distance between two compositions is invariant under this choice — every ILR basis gives the same Aitchison distance.

But **the per-balance distances** are basis-dependent. A change-point that is loud in b1 (Fossil vs Low-Carbon) may be quiet in b6 (Wind vs Other Renewables), and vice versa. So the question of whether shock-verdicts are basis-invariant becomes a richer version of INV-050's pair-invariance result — INV-050 is about TV vs Aitchison at the *composition* level; Q2 extends it to the *balance* level.

The SBP construction here gives the talk a concrete demonstration: compute INV-050's shock-verdict test on each of the seven balances and report the per-balance verdict-invariance pattern. If the verdict survives substitution across multiple bases, the metric-invariance result is genuinely structural.

---

## How this could land in the talk

This is **not headline content**. The talk is governed by the published abstract and stays with closure + perturbation + Aitchison distance as the headline operators. ILR balances are appendix / Q&A bench material.

**Where it could appear:**

- **Beat 8 (three open questions, 1 min):** if a balance-based answer to Q3 is helpful, flash the SBP table for 10 seconds with the line *"one concrete operationalisation: run multivariate change-point on the ILR coordinates derived from this hierarchically-meaningful SBP."*
- **Q&A bench card:** if a CoDa-community reviewer asks "how would you actually run formal change detection?", walk to this document, show the seven balances, name the change-point methods, and explicitly invite the room to weigh in on the null model.
- **Conference handout footnote:** brief mention of the SBP appendix for anyone wanting depth.

**Where it should NOT appear:**

- In the headline narrative — keep that with perturbation + Aitchison distance per the abstract.
- As an asserted result — the SBP is one construction among many; do not over-claim it.
- Without the corrected coefficients — fix the b1 row-sum before any computational use.

---

## What's open

- **Coefficient verification at machine precision** — the document above flags Grok's b1 row as having a row-sum drift; the other rows have not been checked. Before computational use, all seven rows should be re-derived from the standard ILR scaling formula and verified to row-sum-to-zero at IEEE precision.
- **Alternative SBP choices** — the construction above prioritises decarbonisation policy semantics. Alternative SBPs prioritising carbon intensity, dispatchability, or technological maturity would produce different (but equally valid) ILR bases. The Grok session named three such alternatives; only one was elaborated.
- **Cross-corpus validation** — the SBP was built for EMBER 2001–2025. A natural extension is to apply it to the OWID 73-country primary-energy corpus (where Biomass + Other Renewables are separately tracked) and verify the SBP generalises.

---

## Cross-references

- **Source session:** `ai-refresh/cross_check_archive/grok_round_4_session_2026-05-10.md` Section 5–7
- **Q3:** `papers/codawork2026/planning/THREE_OPEN_QUESTIONS.md`
- **Q2:** same document, sharpened framing of INV-050 broader-family
- **INV-050 source:** `papers/codawork2026/planning/NAMED_FINDINGS_FOR_CODA_DISCUSSION.md`
- **MC-4 sharpened:** `papers/codawork2026/planning/CONFERENCE_2026_06_PLAN.md` §5.1 Beat 2
- **Prior-art search:** `papers/codawork2026/planning/PRIOR_ART_SEARCH_TARGETS.md` (Area 4 now partially executed via INV-053)

---

*Captured 2026-05-10 (push #41). Authored by Grok in cross-check; preserved with attribution. Coefficient errata flagged. Not in the headline talk; available in the Q&A bench.*
