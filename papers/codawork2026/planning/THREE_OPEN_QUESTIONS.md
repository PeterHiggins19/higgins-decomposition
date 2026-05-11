# The three open questions for the CoDa community

**Companion to:** `CONFERENCE_2026_06_PLAN.md` (§5.1 Beat 8) and `EXTERNAL_REVIEW_INVITE.md`
**Created:** 2026-05-10 (push #39, claim-sharpening pass)
**Status:** locked for the conference talk — these three questions go on the Beat 8 slide and into the Q&A bench

---

## Purpose

The published abstract names one open question explicitly (concentration measure vs Aitchison norm). The review pass on 2026-05-10 (push #39) sharpened this to three named questions for the CoDa community. The talk's Beat 8 should list all three by name; the conference handout footnote should cite them; the Q&A bench should carry a per-question one-paragraph answer-or-direction so the speaker can engage substantively when asked.

All three questions are explicitly invited as **community business**. None has a preconceived answer.

---

## Q1 — Concentration measure vs Aitchison norm

**This is the abstract's named open question.**

> What is the precise relationship between a concentration measure (such as **K_eff = exp(H)** for Shannon entropy H on the closed composition) and the **Aitchison norm of the composition**?

**Why this matters.** The abstract names "a concentration measure related to effective diversity" alongside the Aitchison distance. K_eff = exp(H) is a natural choice — equal distribution → K_eff = D (full diversity), single-carrier dominance → K_eff → 1. The Aitchison norm `‖clr(ρ)‖_2` is the canonical CoDa magnitude. Both are scale-invariant; both move when composition concentrates. They are not the same quantity, but they are not independent either.

**What pointing at it does for the talk.** A clean theoretical relationship (if there is one) gives the talk a methodological contribution beyond the empirical drift detection. If the relationship is non-trivial (e.g., bounded inequality, monotone in some regime, equality on a submanifold), that is the kind of result CoDa journals publish.

**Existing pointers we know about.**

- Egozcue & Pawlowsky-Glahn (2018) on evidence information distance — adjacent but not the same question.
- Aitchison (1986) §4 on the geometric mean of a composition — related to entropy via Jensen.
- Standard information-theoretic inequalities relating Shannon entropy to L₂-norms in probability simplexes.

**What we are inviting.** A pointer to existing work that closes the gap; a sharpening of the question; or a community-driven derivation we can cite.

---

## Q2 — The right family of "valid simplex distances" against which to test verdict-invariance

**This is the question raised by INV-050 (metric-invariance of the qualitative compositional verdict).**

> INV-050 demonstrates that TV distance (half-L1) and Aitchison distance (log-ratio Euclidean) agree on every shock hit/miss verdict across the 9-country EMBER 2001–2025 corpus. **Is the demonstrated pair-invariance representative of a broader family-invariance, and if so, what is the right family?**

**Why this matters.** The empirical result is verdict-invariance under metric substitution within a pair. Whether the invariance extends to the family of all "valid simplex distances" — weighted log-ratio distances, evidence information distance (Egozcue & Pawlowsky-Glahn 2018), Mahalanobis distance on the CLR covariance, or other CoDa-coherent metrics — has not been tested. A reviewer can press this hard: *"you tested two metrics; how many should you have tested before claiming family-invariance?"*

**What pointing at it does for the talk.** It explicitly frames INV-050 as a starting point, not a finished result. It invites the room to extend the family of tested metrics, which is the kind of follow-up CoDa journals welcome. It also pre-empts the reviewer who would have asked anyway.

**Candidate metrics to test (not exhaustive).**

- Weighted log-ratio distances (different weight choices on the log-ratio coordinates)
- Mahalanobis distance on the CLR covariance matrix (data-driven metric)
- Egozcue–Pawlowsky-Glahn evidence information distance
- Hellinger distance (not strictly Aitchison-coherent but commonly cited)
- Jensen–Shannon divergence (symmetrised KL — well-known but not invariant under perturbation)

**What we are inviting.** Suggestions for the right family definition; pointers to existing work where this question has been addressed; or collaborators willing to extend the testing.

---

## Q3 — The right null model for compositional change-point detection

**This is the question raised by INV-051 (deceptive-drift signature reproduced across 5 of 9 countries) and by the packet's deceptive-drift p = 0.0016 result.**

> The packet's deceptive-drift detection uses an empirical-frequency null computed under the series' own distributional baseline. **What is the right null model for a formal change-point test on the simplex?**

**Why this matters.** A serious CoDa reviewer will press here. The packet itself flags this caveat (Appendix A). Candidates for a stronger null include:

- **Dirichlet null** on the simplex — analytically tractable but parametric; mis-specified if the data are not Dirichlet-generated
- **Permutation null** on the time series — non-parametric but disrupts the temporal structure that the change-point test is supposed to be sensitive to
- **Bootstrap null** with the empirical residual structure preserved — robust but computationally heavier
- **Compositional ARIMA** null (Pawlowsky-Glahn et al.) — sophisticated but possibly over-specified for the monitoring use case
- **A new null specifically for the simplex** — open

**Why this is genuinely open.** Each null model has known strengths and weaknesses; the right choice depends on the use case. For monitoring (the framing of the talk), we want a null that is computationally cheap, non-parametric where possible, and respectful of the simplex geometry. The combination of "compositional + change-point + non-parametric + simplex-coherent" is, to our knowledge, an open question.

**What pointing at it does for the talk.** It explicitly invites the room to bring the right tooling. It pre-empts the methodological challenge by acknowledging it ahead. It frames the p = 0.0016 result as an opening empirical claim, not a closed methodological one.

**What we are inviting.** A null model the community considers appropriate; pointers to existing work on change-point detection on the simplex; collaborators willing to formalise this.

---

## How these three questions land on Beat 8 of the talk

Beat 8 (1 minute, master plan §5.1) names all three. Suggested slide content:

> **Three open questions for the CoDa community**
>
> 1. The Aitchison-norm vs concentration-measure relationship (the abstract's named question)
> 2. The right family of "valid simplex distances" against which to test verdict-invariance (INV-050 follow-up)
> 3. The right null model for formal change-point detection on the simplex (INV-051 follow-up)
>
> *None of these has a preconceived answer. The talk invites the room.*

The talk's first three minutes set up MC-4. The middle six minutes show the three named transitions. The last six minutes (Beats 8 + 9 + 10) hand the work back to the community: three open questions, four defeat paths, two repositories. The structural symmetry — *three named transitions, three open questions, four defeat paths* — is also rhetorically clean.

---

## Q&A bench cards (one paragraph each)

**If asked Q1:** "We compute both. K_eff = exp(H) is bounded [1, D]; the Aitchison norm is unbounded. They co-vary but are not identical — we've seen cases where one moves and the other is quiet. We do not have a clean analytical relationship. We've looked at Egozcue–Pawlowsky-Glahn 2018 evidence information distance as the closest existing work; it doesn't quite close the gap. We're hoping the room knows more than we do."

**If asked Q2:** "INV-050 is the demonstration of pair-invariance — TV and Aitchison agree on every shock verdict across 225 shock-candidate timesteps in 9 countries. Whether this extends to the broader family of valid simplex distances is the question we've named. We've thought about weighted log-ratio distances, Mahalanobis on CLR covariance, and evidence information distance as natural candidates. We have not tested them. We invite the room to suggest the right testing protocol."

**If asked Q3:** "The packet's deceptive-drift result uses the series' own empirical-frequency null, which we acknowledge is the weakest defensible null. Dirichlet is parametric; permutation disrupts temporal structure; bootstrap is heavy. None of these obviously fits monitoring. We treat the p = 0.0016 number as an opening empirical claim, not a closed methodological one. If the community has a preferred null for compositional change-point detection, we will adopt it and rerun."

---

*The three questions are CANONICAL for the conference talk and the discussion that follows. They are part of the talk's commitment to falsifiability + community participation, alongside the four defeat paths in §5.1 Beat 9. Refresh after the conference if community feedback narrows or replaces any of them.*
