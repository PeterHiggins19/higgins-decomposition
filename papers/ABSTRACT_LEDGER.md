# The Hˢ publication abstract ledger — intent revealed, abstracts live

*The chain of papers the Hˢ project intends to publish, each shown by its current abstract. This reveals
intent openly and dates it publicly. **Every abstract here is a pre-submission draft and may change with
feedback** — that is by design, not a defect. The authoritative novelty timestamp for any paper is its
arXiv post (not this file's commit date); nothing here claims "first." When a paper is posted, its arXiv
ID is recorded in its row, and this abstract is reconciled to the posted version. Author: Peter Higgins
(human authorship for all claims); AI-assisted per HUF-STD-001. Honest-broker; claim-tiered.*

> **Why this is safe to post (web-checked 2026-06-16).** Posting your own abstracts on your own
> repository does not interfere with arXiv (arXiv only forbids *duplicates within arXiv*; updates are
> handled as versions v1→v2…). It does not generally block journal submission either — most journals
> accept preprints (several name GitHub explicitly) **provided you (a) check the target journal's
> preprint policy and (b) disclose the preprint at submission.** This ledger is the public, dated trail;
> the arXiv post is the authoritative record. See `industrial-instruments/financial/PUBLICATION_FIT.md`
> and the arXiv versioning policy.

## Status legend

`DRAFT` abstract written, paper drafting · `READY` paper drafted, pre-submission gate pending ·
`POSTED` on arXiv (ID recorded) · `PUBLISHED` in venue. Tiers: T1 verified/reproducible · T2 sound
framing · T3 open/to-confirm.

## The chain

### P1 — Quaternion-exact compositions and lossless dimension-four tiling  · status: READY · gate: final novelty pass + independent reproduction + Peter's post
A four-part composition's three ILR coordinates identify with a unit quaternion on S³ = SU(2); an
Aitchison perturbation is the exact sandwich `q v q*`, reproducing the SO(3) rotation to the IEEE floor
(~10⁻¹⁵). High-dimensional compositions are tiled into overlapping four-part charts and reconstructed
from the chart data; a balanced tree-atlas keeps the chart-graph diameter ~log D and carries the
reconstruction to D = 10⁶ at ~4×10⁻¹² (locally exact at the floor; globally floating-point, not a
mathematical identity at scale). Positioned as recognition + synthesis on prior art (Aitchison;
Egozcue & Pawlowsky-Glahn; Greenacre; synchronization/Laplacian methods). *T1 numerics; T3 absolute
novelty pending the final Scholar/ADS/patent pass.* **The math anchor everything else cites.**

### P2 — A deceptive-drift detector for compositional monitoring  · status: DRAFT · gate: a defensible null model
A monitoring signature that fires when concentration tightens (effective number of parts declining)
while step-to-step compositional movement stays quiet — a divergence standard magnitude/threshold
monitors miss. Framed narrowly: compositional SPC and change-point methods already exist and are cited
generously; the contribution is the specific divergence construction and its honest null. *T1 detector;
T3 the null model (the load-bearing open question).* **Movement V — vigilance.**

### P3 — A deterministic, hash-receipted instrument for compositional navigation (tool paper)  · status: DRAFT · gate: engine navigation parity certified corpus-wide
The CN-TT engine as a reproducible tool: closure → CLR → tiling → diagnostics → hash, with a
cross-platform determinism contract (same input → same output → same SHA-256 receipt) and a modular
control surface. The contribution is reproducibility and open implementation, sidestepping any
findings dispute. Target JOSS/SoftwareX-style. *T1 reproducibility; the engineering contribution, not a
novel-result claim.* **The engine-credibility paper P4/P5/P6 lean on.**

### P4 — Compositional kinematics: reading the motion of a composition on the Aitchison manifold  · status: DRAFT
Reads an observed compositional trajectory as kinematics — velocity/acceleration (the jet), the
mass-weighted arrow of intent (momentum ≠ helmsman), Frenet curvature, effective dimensionality — with
an explicit noise-bounded maximum order as an honesty ceiling. Positioned as a descriptive instrument
on the Aitchison metric, distinct from replicator dynamics (a prescribed model) and information geometry
(Fisher-Rao). *T1 instrument + values; T2 the kinematics framing; T3 terminological novelty.*
**Movement III — motion.**

### P5 — Compositional Character Space: reading systems by their own readings (Hˢ²)  · status: DRAFT
The second-order read: take each system's diagnostic profile (the engine's own outputs) as a feature
vector and read the *systems*. Across 107 real systems in 13 domains, four characters emerge —
Ballistic, Contested, Turbulent, Diffusive — that order cross-domain coherently (a market, a microbiome,
and a conversation can share a "churn" character). The character space is mildly low-dimensional
(~4 axes at n=107; an earlier ~3-axis "collapse" was a small-sample artifact, corrected). *T1 the table
+ clustering; T3 the dimensionality claim, honestly bounded.* **Movement IV — character.**

### P6 — Compositional navigation in finance: a deterministic kinematic reading of allocation systems  · status: DRAFT (new) · key paper, sequenced after P1+P3
A deterministic, model-free, hash-receipted instrument reads an observed allocation composition (sector
weights, holdings, flows, or the mix of observers who study the market) as kinematics — arrow of intent,
character, effective dimensionality, dated regime changes. Positioned between static compositional-data
finance (which characterises/predicts) and Stochastic Portfolio Theory (which models the weight process
stochastically); this reads the realised path deterministically and predicts nothing. Worked on a public
S&P 500 ten-sector composition with a time-permutation null reported honestly; expanding across multiple
exchanges. *T1 reading; T3 relevance; not investment advice.* Full draft:
`papers/financial/P6_COMPOSITIONAL_NAVIGATION_IN_FINANCE.md`.

## The publication-intent statement

The intent is to release this chain progressively, **upon review**: each paper posts to arXiv (the
authoritative timestamp) when its gate is met, then to its venue with the preprint disclosed. Abstracts
of unposted papers will change as feedback lands — readers should treat any `DRAFT`/`READY` row as
provisional. Sequence: **P1 and P3 first** (the foundation everything cites), then P4/P5, then P6 once a
genuinely sourced, citable dataset is in hand. The repository carries the data effort behind each paper;
the paper carries the intelligence (see `PAPER_AND_REPO_DIVISION.md`). Nothing is submitted or posted by
the assistant — Peter is sole gate.

*Intent revealed, dated, and honest. The abstracts are alive; the receipts are fixed; the timestamps
will be arXiv's.*
