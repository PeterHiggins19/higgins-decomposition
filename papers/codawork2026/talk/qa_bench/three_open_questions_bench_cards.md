# Q&A bench cards — Three open questions (Q1, Q2, Q3)

**Q&A priority order (per ChatGPT external review):** Q3 leads. Q2 second. Q1 third. Q3 is the most methodologically consequential.

---

## Q3 — Right null model for compositional change-point detection (LEAD)

**When to use:** if asked about the p-value, the null, hypothesis testing on the simplex, or the right way to formalise change-point detection.

### 30-second answer

> *"That's exactly Q3 in our three open questions — and we believe it's the most methodologically consequential weakness in the framework. The packet's deceptive-drift result uses the series' own empirical-frequency baseline, which we acknowledge is the weakest defensible null. We've thought about Dirichlet — parametric, mis-specified if data aren't Dirichlet-generated. Permutation — non-parametric but disrupts temporal structure that the change-point test is supposed to be sensitive to. Bootstrap — robust but computationally heavy. Compositional ARIMA — sophisticated but possibly over-specified for monitoring. We treat the p = 0.0016 as an opening empirical claim, not a closed methodological one. If the community has a preferred null for compositional change-point detection, we will adopt it and rerun."*

### If a specific null is suggested

> *"That's exactly the kind of pointer we're inviting. Can we follow up after — I'd value working through the specifics with you."*

---

## Q2 — Right family of valid simplex distances (SECOND)

**When to use:** if asked about TV vs Aitchison, broader metric families, or whether INV-050 generalises.

### 30-second answer

> *"That's Q2 in our three open questions. INV-050 demonstrates pair-invariance: TV and Aitchison agree on every shock verdict across the 9-country corpus. Whether the invariance extends to weighted log-ratio distances, Mahalanobis on the CLR covariance, or Egozcue–Pawlowsky-Glahn evidence information distance is open. The useful framing — which we adopted from external review — is to ask the room operationally: what distance family would you consider a fair stress test for verdict-invariance? We have not tested the broader family. We're inviting the community to define the testing protocol."*

### If a specific metric is suggested

> *"Worth running through the engine. The corpus is open, the engine is deterministic, and adding another metric to the side-by-side comparison is straightforward. Can we discuss after?"*

---

## Q1 — Concentration measure vs Aitchison norm (THIRD)

**When to use:** if asked about K-eff, the relationship between concentration and the Aitchison norm, or the abstract's named open question.

### 30-second answer

> *"That's Q1, the abstract's named open question. K-eff equals exp(Shannon H) on the closed composition — bounded between 1 (single-carrier dominance) and D (equal mix). The Aitchison norm is the canonical CoDa magnitude — unbounded. Both are scale-invariant; both move when composition concentrates. They are not the same quantity, and they are not independent. We've seen cases where one moves and the other is quiet. We've looked at Egozcue and Pawlowsky-Glahn 2018 evidence information distance as the closest existing work; it doesn't quite close the gap. A clean analytical relationship — bounded inequality, monotone in some regime, equality on a submanifold — would be the kind of result CoDa journals publish. We're hoping the room knows more than we do."*

### If pointed to relevant work

> *"That's a citation we should know — thank you. Can we discuss after, or could you point me to it?"*

---

## Joint framing — if asked about all three at once

> *"The three questions sit in different layers. Q1 is theoretical: the relationship between two compositional measures. Q2 is methodological: how broadly does verdict-invariance hold. Q3 is statistical: what null are we testing against. All three are honestly open. We have no preconceived answer to any of them. The talk explicitly invites the room — and we have a public catalog (INV-050 through INV-053) to record whatever the community contributes."*

---

## What to NOT do

- Do not improvise an answer to a question you don't have. Use the *"I don't know — can we discuss after"* posture instead. That's prepared, not weak.
- Do not collapse the three questions into one — they really are in different layers.
- Do not promise a paper resolving any of them within a specific timeframe. Promise engagement and re-run-on-pointer.

## Receipts

- Full content of all three questions in `papers/codawork2026/planning/THREE_OPEN_QUESTIONS.md`
- INV-050, INV-051 in `ai-refresh/INVESTIGATION_CATALOG.json`
- Q&A bench Q3-first ordering noted in `THREE_OPEN_QUESTIONS.md` after ChatGPT external review
