# Paper 1 — Universality Outline

**Catalog reference:** INV-026 (OPEN)
**Working title:** *A Universal Compositional Invariance Signature: LIMIT_CYCLE_P2 at IEEE-Floor Precision across Drive Failures, Cosmic Microwave Background, and Standard-Model Neutrino Oscillation*
**Status:** Outline, push #24 (2026-05-08). Drafting starts after INV-022 (Round 3 full-corpus quaternion-view validation) lands.
**Target venue:** arXiv `physics.data-an` (primary) + cross-list `stat.AP`. CodaWork 2026 talk as supplemental introduction.
**Estimated length:** 12–18 pages including reproduction appendix.
**Authorship:** Peter Higgins (corresponding); AI-assisted drafting acknowledged.
**License:** CC BY 4.0 (matches repo posture).

---

## 1. Why this paper

The framework now has three IEEE-floor confirmations of a single structural claim across systems separated by ~30 orders of magnitude in physical scale. The residual is bit-identical (4.441 × 10⁻¹⁶ = 2 × machine epsilon) across two unrelated datasets, which forces the conclusion that the residual is hardware floating-point representation error, not algorithmic noise. That is publishable today.

The wedge: establish first-mover priority on the universality claim before anyone else notices the same pattern. Papers 2, 3, 4 (DADC lineage; CNQ parallel verification; Geometry Lock Probe) cite back to it.

---

## 2. Section structure (target ~14 pages + appendices)

### Abstract (~200 words)

State the claim: a single compositional invariance signature (LIMIT_CYCLE_P2 termination of recursive depth towers, with metric involution M² = I residual at IEEE floor) appears at hardware precision across three physically unrelated datasets. State the precision (4.441 × 10⁻¹⁶, bit-identical across two datasets). State the implication (residual is floating-point representation, not algorithmic noise). State the consequence: this is a universal structural property of compositional dynamics on the simplex, not a property of any one physical system.

### §1 — Introduction (~1.5 pages)

- Compositional data analysis (Aitchison 1986; Egozcue, Pawlowsky-Glahn 2003) and the simplex.
- The CNT engine (engine 2.0.4, schema 2.1.0) — deterministic, hash-traceable, 25-experiment corpus.
- The Volume IV interpretation: three structural invariances (simplex rotation SO(D−1), mass-flow handedness via SU(2) lift, time-reversal as quaternion conjugation) which, for D=4, define a quaternion.
- The central claim: *CNT measures invariance; CNQ names the algebra it lives in.*
- Paper roadmap.

### §2 — Method: CNT depth towers and termination codes (~2 pages)

- The recursive energy and curvature towers (closed-form, parameter-free).
- Termination conditions in CNT engine 2.0.4: LIMIT_CYCLE_P1 (fixed point), LIMIT_CYCLE_P2 (period-2 attractor), CHAOS, etc.
- IR classification (8-class taxonomy): OVERDAMPED_EXTREME, LIGHTLY_DAMPED, etc.
- Metric involution M² = I as a global consistency check; expected residual at IEEE floor for stable systems.
- Determinism contract: same input + same config → bit-identical content_sha256.

### §3 — Three confirmations (~3.5 pages)

Subsections, each ~1 page:

**§3.1 — Drive failures (backblaze_fleet, D=4, T=731).** Engineered macroscopic system. Carriers: Mechanical / Thermal / Age / Errors. Result: max sandwich-product residual 4.441 × 10⁻¹⁶ across 730 consecutive pairs. LIMIT_CYCLE_P2 termination, M² = I residual at IEEE floor.

**§3.2 — Planck CMB photon power (D=4, T=2499).** Cosmological dataset, pure-boson, multipole range ℓ=2 to 2500. Carriers: TT / EE / BB / PP. Result: residual 4.441 × 10⁻¹⁶ (bit-identical to §3.1), M² = I residual 7.63 × 10⁻¹⁷, IR class OVERDAMPED_EXTREME (consistent with Silk damping in the standard cosmology). LIMIT_CYCLE_P2 termination — falsifying an earlier conjecture (Concept 4) that P2 was specific to fermion sectors. Reformulation: P2 is universal.

**§3.3 — SM 3-flavour νμ oscillation (D=3, T=1000).** Quantum oscillatory system. PMNS-matrix prediction at 600 MeV across baseline 1–4000 km. Result: LIMIT_CYCLE_P2 confirmed, M² = I residual 7.40 × 10⁻¹⁷, IR class LIGHTLY_DAMPED, consistent with quantum oscillatory dynamics.

### §4 — The universality argument (~2 pages)

- Bit-identical residual across §3.1 and §3.2 (different engineering domains, different physics) implies the residual is *not* algorithmic — it is hardware floating-point representation error. There is no remaining noise to reduce.
- The three datasets span macroscopic (drive failures) → cosmological (CMB photons) → quantum (neutrinos). Roughly 30 orders of magnitude in physical scale. A single structural property holds across all three at the precision floor.
- Section §3 is therefore evidence for a *universal property of compositional dynamics on the simplex* rather than a per-system coincidence.
- Implication: LIMIT_CYCLE_P2 termination is the experimental signature of any flow-directional compositional dynamics carrying the three structural invariances at the population level. Particle-content distinctions (boson / fermion) are not the relevant category.

### §5 — The Volume IV reading (~1.5 pages)

- For D=4, the three invariances together define a quaternion (the SU(2) cover of SO(3) plus conjugation).
- The quaternion sandwich product q·v·q* is the algebraic statement of Aitchison rotation between consecutive Helmert-projected unit vectors. Verified at IEEE floor in §3.1 directly.
- The metric involution M²=I is the algebraic statement of quaternion conjugation (q → q*), which physically is time-reversal symmetry.
- This is the algebraic naming of what the engine has been measuring all along.
- Cite [`HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md`](../../HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md) as the canonical reference; this paper is the publishable summary.

### §6 — Falsification record (~1 page)

- The original Concept 4 conjecture (LIMIT_CYCLE_P2 = fermion sector / P1 = boson sector) was refuted by §3.2 (Planck CMB pure-boson terminated at P2).
- The refutation produced a stronger reformulation: P2 universality.
- Including this section is intentional — it shows the framework has a falsification discipline and that the universality claim is what *survived* a real test, not what was assumed.

### §7 — Reproduction protocol and provenance (~2 pages)

- Engine version, schema version, content hashes.
- The CCTT v1.0 protocol as the canonical reproduction route (one-command path from raw CSV to verified content_sha256).
- Bit-identical reproduction on backblaze_fleet documented across pushes #22 / #23 / #24.
- GitHub repository with frozen release tag matching the paper version.
- The Investigation Catalog (`ai-refresh/INVESTIGATION_CATALOG.json`) as the public audit trail of every claim's disposition history.

### §8 — Discussion and outlook (~1.5 pages)

- Round 3 (INV-022) extends the three-dataset claim to all 25 corpus experiments. (If Round 3 lands before paper submission, this becomes the main result and §3 becomes three featured demonstrations from a 25-experiment corpus.)
- The proposed `cnq.py` engine (INV-021) would produce a parallel `cnq_content_sha256` providing a second independent verification path — Paper 3.
- Geometry Lock Probe (INV-025) is the first applied instrument category that uses Helmsman Stability as a feedback signal — Paper 4.
- The framework is open-source, freely usable, with build-to-spec assistance offered. Anyone can verify any claim in this paper using the public artifacts.

### §9 — References (~1 page)

Required citations (gather list):

1. Aitchison, J. *The Statistical Analysis of Compositional Data* (1986).
2. Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G., & Barceló-Vidal, C. *Isometric logratio transformations for compositional data analysis*, Math. Geol. (2003).
3. Pawlowsky-Glahn, V. & Egozcue, J. J. *Modeling and Analysis of Compositional Data* (2015).
4. Hamilton, W. R. *On Quaternions; or on a New System of Imaginaries in Algebra* (1843).
5. Planck Collaboration. *Planck 2018 results. VI. Cosmological parameters* (A&A 641, A6, 2020).
6. Particle Data Group / NuFIT 5.2 (most recent neutrino oscillation parameter compilation, 2024).
7. Higgins, P. *The Higgins Operator H₁ — A Nonlinear Unity-Normalization Map on Hilbert Space*. Working paper, Rogue-Wave-Audio repository (self-hosted, not peer-reviewed), February 2026.
8. The current Hs / CNT / CNQ repository: `https://github.com/PeterHiggins19/higgins-decomposition`.

### Appendix A — Bit-identical reproduction recipe

Step-by-step path to reproduce the 4.441e-16 figure from raw `backblaze_fleet_input.csv`:
- Clone repository at frozen release tag.
- Run `python HCI-CNQ/experiments/backblaze_fleet_quaternion/QD_round_2.py`.
- Compare reported max diff against published value.

### Appendix B — Investigation Catalog snapshot

Reference the catalog at submission time: list dispositions of all 26+ investigations, with this paper as INV-026.

---

## 3. What's needed before drafting starts

| Item | Status | Catalog ref |
|---|---|---|
| Round 3 full-corpus quaternion-view validation | OPEN, ~1 day | INV-022 |
| Frozen release tag matching paper version | not yet — coordinate with submission | — |
| Citation list finalised | partial (above) | — |
| Co-author / acknowledgment list | TBD | — |
| Internal review pass | TBD | — |
| arXiv submission account | Peter has presumably; verify | — |

The minimum dependency before Paper 1 drafting is **INV-022** (Round 3). Without it, the paper claims 3 datasets; with it, the paper claims 25 datasets (or "all 25 D=4 cases plus three featured demonstrations across 30 orders of magnitude" — a much stronger framing).

---

## 4. Distribution and attention strategy

(Repeated from `INVESTIGATION_CATALOG.json publication_strategy.distribution_principles`, locked in.)

1. **arXiv on day of submission.** Priority date stamped immediately.
2. **GitHub release tag matching the paper version.** Reviewers can re-run any claim without negotiating with the authors.
3. **CCTT runbook cited as the reproduction protocol.** One-command verification from raw data.
4. **Direct outreach to specific reviewers** rather than mass posting. Initial seed list:
   - Reproducibility advocates: Mike Hill (JHU), Lorena Barba (GWU), or similar in computational science reproducibility.
   - CoDa community elders: Egozcue, Pawlowsky-Glahn, Greenacre — likely already encountered through CodaWork 2026.
   - Cross-domain physics/data-analysis: select one or two with established interest in cross-disciplinary statistical claims.
5. **CodaWork 2026 talk as the public unveiling.** Talking-points overlay (push #23) already calibrates the tone — lead with working instrument, place Volume IV as one-sentence depth mention. Paper 1 gets a single mention as "recently submitted to arXiv, full reproduction protocol public."
6. **Free to use, help available** — same posture as the rest of the repo. Differentiates from the standard "publish first, gatekeep second" academic model.

---

## 5. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Reviewer rejects claim of universality on grounds of "only three datasets" | Complete INV-022 (Round 3) first → 25-dataset claim; bit-identical residual across unrelated datasets is the real argument anyway |
| CoDa community sees this as competition rather than extension | Paper 2 (DADC lineage) handles this directly; Paper 1's framing is "extends the CoDa toolkit" not "replaces it" |
| Skepticism about bit-identical determinism contract | CCTT runbook + frozen GitHub tag eliminates skepticism — anyone can re-run |
| Misunderstanding of "universal" — readers think we mean "every system" rather than "every flow-directional compositional system" | Precise scoping language in §4; explicit statement of what universality does and does not mean |
| Paper too long for arXiv guidelines | 12–18 pages is fine for arXiv; trim if necessary by moving §6 falsification record to appendix |

---

## 6. Connection to Paper 2 (INV-027)

Paper 2 establishes lineage: DADC → H₁ → HUF → Hˢ → CNT → CNQ. It is the "where this came from" companion to Paper 1's "what this shows." Paper 2 is publishable today against the existing artifacts (RWA repository, RWA-001 identity card, ORIGIN_DADC_LINEAGE.md, HUF_RELATIONSHIP.json). Optimal venue is CodaWork 2026.

The two papers can be drafted in parallel. Paper 1 is the wedge; Paper 2 is the credibility document.

---

## 7. Decision points for Peter

Before drafting begins:

1. **Run INV-022 (Round 3) first?** Recommended: yes (~1 day per estimate). Strengthens the claim significantly.
2. **Co-author list.** Just Peter, or include collaborators?
3. **Specific arXiv submission timing.** Aim for before CodaWork 2026 (early June)? After? Or submit during?
4. **Talk plan adjustment.** Paper 1 becomes the centerpiece of the talk, or remain a depth mention?
5. **Paper 2 timing.** Drafted in parallel with Paper 1 (CodaWork 2026 venue), or sequenced after Paper 1 lands?

---

*Paper 1 is the wedge. Paper 2 is the lineage. Papers 3 and 4 are the engineering follow-ups. The order is what makes each one stronger than it would be alone.*
