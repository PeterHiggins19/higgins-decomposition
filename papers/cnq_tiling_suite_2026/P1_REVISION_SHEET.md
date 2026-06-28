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
| **Gemini** | math re-derivation + R-port parity | ✅ 2026-06-18 | **all PASS** (math/conformance/discipline); only blocker = Figure 1 (R-4) |
| **ChatGPT** | claim/tier/wording audit | ✅ 2026-06-18 | **R-5…R-9 + tightenings APPLIED** (Peter-approved, incl. abstract); R-4 figure → Peter supplies |
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
- When Gemini / ChatGPT / Copilot return, the
---

## ChatGPT return (claim/tier/wording audit) — 2026-06-18

*Verdict: strong, near arXiv-ready; **6 blockers** (precision/wording, not concept failure) + tightenings.
Every flag was **verified against the current source** (`arXiv/P1_cnq_tiling/latex/`). Awaiting Peter's
approval per item; the safe set can be applied in one pass + recompile.*

### R-4 (BLOCKER) — Figure 1 placeholder *(= R-3; also flagged by Grok)*
The `\fbox` placeholder cannot go to arXiv. Min figure: path atlas (diameter O(D)) | balanced-tree atlas
(O(log D)); inset residual/diameter vs D. **Status:** ☑ Peter supplies the figure.

### R-5 (BLOCKER) — "Aitchison perturbation acts as q·v·q*" is imprecise *(verified §3.1 l.4)*
A standard **Aitchison perturbation** is the simplex group op = **translation/addition** in clr/ilr space,
**not** a rotation. The sandwich q·v·q* is an **isometric rotation** of ILR space (SO(3)), a different
operation. A CoDa reviewer will object. **Proposed (ChatGPT):**
> In D=4, the Helmert-ILR representation identifies the clr-zero composition with a vector in ℝ³ —
> equivalently a pure imaginary quaternion. Unit quaternions q ∈ S³ ≅ SU(2) act on this ILR vector by the
> sandwich v ↦ q v q*, giving the SO(3) isometric rotations of the ILR space. This is an
> *Aitchison-isometric rotation of the ILR representation*, not the Aitchison perturbation operation itself.

**Tier 1 (correctness).** **Decision:** ☐ apply ☐ edit ☐ decline

### R-6 (BLOCKER) — "v on S³" vs "q on S³" *(verified; lands on the R-2 sentence I added, §3.1 l.12)*
The ILR vector **v ∈ Im(ℍ) ≅ ℝ³** is a *pure imaginary* quaternion (not a unit quaternion); **q ∈ S³** is
the rotor. My own R-2 interpretability line ("a rotation of the ILR vector on S³") carries exactly this
imprecision and must be fixed with R-5. **Proposed:** "…the unit quaternion q ∈ S³ ≅ SU(2) acts on that
vector **by conjugation** (q v q*); the direction and magnitude of change read off as a rotation axis and
angle." **Tier 1.** **Decision:** ☐ apply ☐ edit ☐ decline

### R-7 (BLOCKER) — Abstract overclaims cross-platform hash parity *(verified abstract l.37–38)*
Abstract says "matching content hash across platforms"; §6/§7 + HS-EPS-1 (F-1) say byte-hash parity is the
**P3** matter and norm varies by 1 ULP — an internal **contradiction** (fails the contradiction test).
**Proposed (ChatGPT):** "The construction is deterministic and hash-receipted under a stated
canonicalization profile; the D=4 conformance receipt is reproduced across implementations, while full
cross-platform engine hash parity is treated in the companion tool paper." **Tier 1.** **Decision:** ☐ apply ☐ edit ☐ decline

### R-8 (BLOCKER) — 12-decimal engine hash vs full-precision conformance receipt *(verified §3.5 l.107)*
Engine output hashes round to 12 decimals; HS-EPS-1 residuals (~1e-16) would round to 0 — hence the
separate full-precision core receipt. Add one clarifying sentence so a reproducibility reviewer doesn't see
a contradiction: "Engine-output hashes use the 12-decimal canonical payload; HS-EPS-1 uses a separate
full-precision receipt over the exactness-residual fields because those residuals live below the 12-decimal
round." **Tier 1.** **Decision:** ☐ apply ☐ edit ☐ decline

### R-9 (BLOCKER) — Finalize the Greenacre-2022 reference note *(verified refs.bib l.38)*
`note = {…; verify exact volume/pages/year at submission}` cannot remain in the posted PDF. Replace with
final bibliographic metadata or drop the note. *(This is my own R-1 placeholder.)* **Decision:** ☐ finalize ☐ drop note

### Tightenings (recommended, not blockers)
- **Appendix B:** replace "(verified numerically)" with the **explicit 4×4 generator matrices** (a few lines)
  or a pointer to the replication kit — strengthens an exactness paper.
- **Table 1 caption:** add "rows D=16–1024 use the path atlas; the D=10⁶ row uses the balanced-tree atlas."
- **Appendix A first sentence:** soften "must return identical numbers" → "must return the same **core**
  conformance receipt; norm preservation may differ by one ULP (norm-reduction order is library-dependent)."
- **Strict forbidden-word:** "No claim of ``lossless'' or ``identity''…" → "No claim of bit-exact
  high-dimensional identity." (optional; current is a negation, already compliant.)

### Audit passes (ChatGPT confirmed good)
High-D caveat present in abstract/results/Table-caption/claim-tiers; "lossless" only negated; HS-EPS-1 split
honest (core matches, norm excluded). **Net status: near-ready; not submit until R-4…R-9 are applied + the
figure lands; then Peter's final gate.**


---

## APPLIED — ChatGPT's blockers (Peter-approved, 2026-06-18)
**R-5/R-6** (perturbation→isometric rotation; v∈Im(ℍ) acts-on, q∈S³ the rotor; my R-2 line corrected),
**R-7** (abstract hash line → P3-aligned, Peter re-approved the abstract change), **R-8** (12-decimal engine
hash vs full-precision HS-EPS-1 receipt clarified), **R-9** (Greenacre placeholder note dropped), plus the
tightenings (Table-1 path/tree caption; App-A "core receipt" softening; App-B explicit-generators pointer;
forbidden-word → "bit-exact high-dimensional identity"). The abstract's first sentence was also corrected for
the same perturbation/rotation precision. Only **one** "Aitchison perturbation" mention remains — the honest
negation. **Edited source recompiles clean (6 pp, 0 errors, 0 undefined; Greenacre cited).**

**Caveat:** the sandbox could not overwrite the arXiv-folder build artifacts (`main.pdf`/aux are read-only to
it), so the in-place `arXiv/P1_cnq_tiling/latex/main.pdf` is **stale** — `main.tex`/`refs.bib` are updated and
verified-compiling; **regenerate `main.pdf` on your machine** (`pdflatex+bibtex+pdflatex×2`).

**Remaining before arXiv:** R-4 (Figure 1, you supply) + Gemini & Copilot returns + your final gate.


---

## Gemini return (independent math re-derivation + R-port parity) — 2026-06-18
**Verdict: math core PASSED, fully cleared except Figure 1.**
- **[M-1 MATHEMATICS] PASSED** — re-derived the D=4 ILR↔quaternion identification (q v q* via the adjoint
  action; residual ≈ 4.4e-16 = 2·ε_mach, the arithmetic floor, **Tier 1**); the Laplacian reconstruction +
  O(log D) diameter bound (path O(D)·ε drift → tree depth ~13 at D=10⁶ → ≈4.1e-12, **Tier 2 sound**); and
  Appendix B su(2) structure constants **[Gᵢ,Gⱼ]=+2εᵢⱼₖGₖ** (confirmed the +2 sign, avoiding the −2 trap).
- **[CONFORMANCE] PASSED** — re-ran HS-EPS-1: machine_eps + residA + residB exact; norm_preservation = **ε
  (1 ULP)**; **core receipt `06ccdb25` MATCH**. Replicates the ChatGPT/Copilot branch → validates finding F-1.
- **[DISCIPLINE] PASSED** — no "lossless"/"identity"/"first" misuse; abstract↔body numeric anchors consistent;
  names clean.
- **[SUBMISSION GATE] BLOCKED BY FLAG 1** = Figure 1 placeholder (= R-4; Peter supplies). Advisory A-1:
  finalize Greenacre vol/pages if published (already addressed by R-9 — note dropped).

**Note on review ordering (honest-broker):** Gemini reviewed the **pre-R5/R6** text and *passed* the §3.1
interpretability line that ChatGPT flagged for wording precision. No conflict — Gemini verified the **math**
(sound in either phrasing); ChatGPT corrected the **wording** (perturbation = translation, not rotation).
Both stand. **R-port:** Gemini's environment matched the ε-branch; a literal Python↔R run remains a nice-to-have.

## Review tally (3 of 4 returned)
Grok ✅ · ChatGPT ✅ (applied) · Gemini ✅ · **Copilot ⏳** (independent reproduction). **The only blocker
remaining across all returned reviews is Figure 1 (R-4).** Once it lands + Copilot returns → Peter's final gate.
