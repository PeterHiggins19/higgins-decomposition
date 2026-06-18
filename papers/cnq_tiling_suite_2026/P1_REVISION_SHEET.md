# P1 — collective revision sheet (awaiting Peter's approval)

*Compiled by Claude from the collective's review returns against the brief
([`P1_REVIEW_BRIEF.json`](P1_REVIEW_BRIEF.json)). Nothing here is applied to the paper yet — each item is a
proposal for Peter to accept, edit, or decline. Peter is the sole gate; no edit lands until he approves it.
Author of all claims: Peter Higgins; AI-assisted per HUF-STD-001.*

---

## Status of returns

| Member | Focus | Returned | Tier-1 flags |
|---|---|---|---|
| **Grok** | prior art + novelty | ✅ 2026-06-18 | none — **R-1, R-2 APPLIED** (Peter-approved); R-3 figure → Peter supplies |
| Gemini | math re-derivation + R-port parity | ⏳ pending | — |
| ChatGPT | claim/tier/wording audit | ⏳ pending | — |
| Copilot | independent reproduction | ⏳ pending | — |

Grok's verdict: prior-art framing **fair and narrow**; novelty **under-stated (in a good way)**; arXiv
readiness **high** once Figure 1 is replaced and the interpretability sentence is added. **No Tier-1 flags.**

## Proposed edits (each awaits Peter's yes/no)

### R-1 — Engage Greenacre (2022) in §2 *(Grok, Tier 2; also flagged by the publication-fit benchmark)*
**Why:** a CoDa reviewer who knows the 2022 reappraisal (arXiv:2201.05197, pairwise-logratio selection on
connected graphs) will expect it addressed; it shares the connected-graph setting, so the contrast is worth
one sentence. Low risk, no change to the contribution.
**Where:** end of §2 (Background and prior art).
**Proposed text (Grok's wording, lightly fitted):**
> Greenacre (2022) develops pairwise log-ratio selection on connected graphs for interpretability and
> variable reduction; the present construction is orthogonal — it retains the full set of within-chart
> log-ratios and recovers the global clr state exactly (in exact arithmetic), or to bounded floating-point
> drift (in floating-point), via the quaternion identification.
**Also needs:** a `refs.bib` entry for Greenacre 2022 (to be verified at submission).
**Decision:** ☑ **APPLIED** 2026-06-18 (Peter-approved) — §2 paragraph + `greenacre2022` bib entry added; P1 recompiles clean (6 pp). Exact venue/year still to verify at submission.

### R-2 — Add the interpretability sentence in §3.1 *(Grok + benchmark, Tier 2)*
**Why:** the field's standard knock on exact-ILR is "uninterpretable (ratios of geometric means)." The paper
already implies the answer; one explicit sentence turns the weakness into the contribution for readers
coming from classical CoDa.
**Where:** §3.1 (the quaternion reading at D=4), after the sandwich equation.
**Proposed text:**
> Where exact-ILR coordinates are often considered hard to interpret — they are ratios of geometric means —
> the quaternion identification gives them a concrete geometric meaning: an Aitchison perturbation is a
> rotation of the ILR vector on $S^3$, so the direction and magnitude of compositional change read off as a
> rotation axis and angle.
**Decision:** ☑ **APPLIED** 2026-06-18 (Peter-approved) — added to §3.1 after the sandwich equation; abstract untouched; P1 recompiles clean.

### R-3 — Replace Figure 1 placeholder *(all reviewers; Tier 2 / blocker for submission)*
**Why:** Figure 1 is still the `\fbox` placeholder (chart-graph atlas: path vs balanced tree, diameter-vs-D).
A CoDa reviewer expects the real diagram; arXiv post should not go out with a placeholder.
**Action:** generate the real figure from `experiments/cnq_tiling_highd_2026-06/` (path vs balanced-tree
diameter vs D), export as `fig1.pdf` (vector, per the LaTeX standard), drop into `latex/`.
**Decision:** ☑ **Peter supplies the figure** (his call, 2026-06-18). Claude wires it in as `fig1.pdf` when received. This is the one remaining hard blocker before an arXiv post.

## Notes
- R-1 and R-2 are body edits only; the **approved abstract is untouched**.
- The su(2) `+2` sign, the HS-EPS-1 conformance, and the clean build are already settled (Grok raised no
  issue with them).
- When Gemini / ChatGPT / Copilot return, their items get appended here and the table updated; Peter then
  approves a single consolidated edit pass.
