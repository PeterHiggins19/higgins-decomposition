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

## P7 — Foundations (the Coda) — *SEED*

The closing paper of the series. **Working abstract (provisional):** *A practical instrument for reading conserved mixtures, pushed until it was exact, is shown to sit on a specific algebraic structure — the four-part composition as a unit quaternion on $S^3=SU(2)=\mathrm{Spin}(3)$ — and to inherit, by the same exactness, sharp limits on what it can be: the high-dimensional construction is a flat, connectivity-only atlas with no nontrivial topology, no "lossless" identity at scale, and no manufactured significance. We report the positive structure (the exact rung; the two $SU(2)$ chiralities; why four parts is forced by the Cayley–Dickson break) together with its boundary, stated as theorems by contradiction, and the epistemic practice the exactness makes possible (cross-platform machine-epsilon conformance; internal contradiction testing). The negative results are first-class.* *Tier 1/2 throughout; assembled LAST from P1/P3/P4/P5; no "lossless"/"first".* Seed: `papers/P7_FOUNDATIONS_SEED.md`.

## P8 (seed) — The Compositional Message Principle

The discriminative signal in a composition lives in the inter-part log-ratios (the ILR map is a sufficient statistic; by the data-processing inequality scalar aggregates are lossy and can be null while the relational read is strong), and recoverable information scales with the number of parts up to a finite-sample capacity D*(N). Proved + tested on real microbiome data (Crohn relational AUC 0.832 vs diversity-null 0.505 p=0.78, PERMANOVA p=0.001; HIV replicates p=0.002). *Tier 1 core; the universality claim is T2/T3 until triangulated.* Seed: `papers/COMPOSITIONAL_MESSAGE_PRINCIPLE_PAPER_SEED.md`.

## The Triangulation Trilogy (applied case-ordered axis) — W-I/W-II/W-III + Keystone

A backwards-built series that projects the spine math through **three independent real systems** to *locate* the compositional law by our own 3-to-locate method: **W-I Microbiome** (measured, T1), **W-II Mudstone / Frielingen-9** (measured, 3/3 located, T1), **W-III Backblaze drive fleet** (measured, T1 — real public telemetry, hash 058fde30806a8e6b, 159 silent-drift pre-fault events; the engineered-fleet anchor), and the **Capstone** = the HUF Constellation System proposal (the SpaceX *reach*), supported by the three measured witnesses + HUF math (T2/T3, with its decisive public-data test named): `papers/THE_HUF_CONSTELLATION_SYSTEM_PROPOSAL.md`. Each paper is self-contained (no assumed prior reading); the shared stones are restated by design, and *repetition across independent domains is the signal* — under the explicit guard that each repetition carries its own fresh receipt. Plan + build order: `papers/TRIANGULATION_TRILOGY_PLAN.md`. *Reuses the P-series stones; feeds P7; nothing re-derived or replaced.*

## P-C (seed) — Deterministic compositional coding and noise rejection

The communications substrate beneath the pinnacle: a message rides the D−1 isometric-log-ratio channels of a composition; encoder and reader are exact mutual inverses (fixed point `742f1b5a`); closure rejects common-mode multiplicative gain exactly (313 dB numerical, `d8c21c70`); additive noise off the coherent k-subspace is removed at 10·log₁₀((D−1)/k) dB and known-structure noise to the floor, while in-subspace random noise is provably not separable (`cb0c3f52`); ~3.5–10× compression within ~10% of symbol entropy (`305cc0db`); the ilr representation is ≈700× more error-robust than raw shares on a validated 16-QAM/AWGN link (`f502c15d`); the SO(n) generator (`8107b173`) supplies the data factory. *Tier 1 throughout; no Shannon limit beaten.* Seed: `papers/P_C_COMPOSITIONAL_CODING_SEED.md`.

## P-Ω (seed) — Deterministic Compositional Communication: when the data is the carrier (THE PINNACLE)

The apex paper. A communications engineer's reflex — "where is the carrier?" — is answered with proof: for compositional data the data's own geometry performs every carrier function. **Prop 1** closure supplies the reference and rejects any common gain (`clr(g·x)=clr(x)`, proven; 8.9e-16 measured). **Prop 2** the ilr map is an exact isometric frame (bijection). **Prop 3** the symbols are relational (sufficiency + DPI) and capacity grows with parts (7→79 bits, `bf24c615`). **Fixed point:** encoder/reader are exact mutual inverses — the message is a fixed point of decode∘encode (1500/1500 exact over D=3…48, `742f1b5a`) — and determinism makes the receipt a fixed point under recomputation. **Demonstration:** the Hˢ Duplex carries an instruction that is observed, executed by the engine, and returned verified, with no control channel (`4241d38a`). Positioned in **Deterministic Identification** theory and **Semantic-Channel Theory**; the honest cap stated (no Shannon limit beaten; value = determinism + integrity + control intrinsic to the data). *Tier 1 the proofs/measurements; T3 no priority/beyond-Shannon claim.* Seed: `papers/P_OMEGA_THE_DATA_IS_THE_CARRIER_SEED.md`. Architecture: `papers/THE_PINNACLE_RELEASE_ARCHITECTURE.md`.

## P-ψ (seed) — A hash receipt for psychology: a value composition read and cast on public data

The applied/convergence paper that projects the spine through a real, public, 120-year cultural-psychology record. **Working abstract (provisional):** *Psychology is the field most defined by its reproducibility problem; we show — as proof of concept — that a value-and-virtue compositional claim can ship with a deterministic hash receipt anchored to a fingerprint of public data anyone can re-pull. Two pre-stated compositions of Google Books Ngram frequencies (en-2019, 1900–2019) — a six-term virtue vocabulary and Jordan Peterson's order↔chaos polarity — are read relationally (effective dimension, trajectory directedness, recent motion-helmsman) and cast forward ("test the past, see the future"), with per-composition data fingerprints (`56546d3ab316f732`, `2935d3b5f31ac2f6`) and a master receipt (`8ec3ae8d5623c5d7`). The virtue lexicon is rebalancing from responsibility/discipline toward courage/gratitude/humility; the order share is falling, chaos rising.* Framed as the receipted continuation of the **Peterson Convergence** (CONV-001) — an independent 35-year clinical-psychology research program arriving at the same structural read HUF/Hˢ measures. **The contribution is methodological — determinism + a receipt for a field that needs both — NOT a claim that Hˢ explains human cognition** (book word-frequency is a cultural-attention proxy; "chaos" is inflated post-1975 by chaos theory; the cast is a what-if). *Tier 1 the reads/fingerprints; T2 the convergence framing; T3 no claim on individual cognition or causation.* Lineage: the dormant Peterson outreach (`HUF/dormant/peterson-outreach/` — letters v4–v7, never sent; `Peterson_Convergence_Analysis_v1.0.json`). Data + experiment in repo: `papers/psychology-receipt/`. Full draft (arXiv-bound): `papers/psychology-receipt/A_HASH_RECEIPT_FOR_PSYCHOLOGY.md`.

## P-μ (seed) — A receipted compositional read for cancer-incidence epidemiology

The applied medical-epidemiology companion to P-ψ. **Working abstract (provisional):** *A population's total cancer burden is one number; the composition of sites that make it up turns underneath the total, and a totals-only view misses the turn. We give a deterministic, hash-receipted compositional read — closure → clr → trajectory directedness → motion-helmsman → forward cast — for cancer-incidence epidemiology, demonstrated on the breast-cancer epidemiological transition (in India, the rising breast-cancer share and declining cervical share). The method (receipt `0c44c4a150cad7f0`) is shown on **illustrative data parameterized only to the documented qualitative direction — no real registry count is asserted** — with the real plug-in (India NCRP/ICMR or GLOBOCAN/IARC incidence-by-site) named and pending as the collaborator's contribution. This is "cancer = drift" (P2) made measurable for population epidemiology.* **Population epidemiology only — NOT clinical, NOT diagnostic, NOT a treatment; the project's own EITT safety boundary (no small-n patient cohorts) is honoured by design.** *Tier 1 the method/receipt; T2 the cancer-as-drift framing; T3 no clinical/medical claim until real data + experts + validation.* Companion to and citing *Kanjiradan Veetil & Dilip, "Integrating compositional data analysis in cancer epidemiology"* (CoDaWork 2026, p. 28). Data + experiment in repo: `papers/medical-epidemiology/`. Full draft (arXiv-bound): `papers/medical-epidemiology/A_RECEIPTED_READ_FOR_CANCER_EPIDEMIOLOGY.md`. *The medical/commercial engagement is private and off-repo (Peter-gated).*

## P-ν (seed) — A deterministic model of compositional perception (the neurological leg of the Peterson study)

The neurological companion to P-ψ, and the mechanistic half of the **Peterson convergence** (CONV-001: an independent clinical-psychology account of perception narrowing a high-dimensional world through a channel). **Working abstract (provisional):** *The canonical neural computations are the compositional operators: divisive normalization (Carandini & Heeger 2012) is closure — it cancels a common multiplicative gain exactly (measured residual 4×10⁻¹⁶) — and Weber–Fechner logarithmic encoding is the log, so divisive-normalization-then-log is structurally the centered-log-ratio. With the receptor population as the **mesh** and neural integration time as the **dwell**, a neural-style reader converges to the exact relational read (clr) of a composition as mesh×dwell grows, error 0.95→0.0075 at the 1/√N observability law (`b7fd9a39b664dc1a`). The math has one answer; the brain approaches it statistically through dwell and mesh; Hˢ computes it exactly — same destination, different path.* **Structural / computational analogy (T2/T3) — NOT a claim that the brain implements Hˢ or that perception is literally clr.** Together with **P-ψ** (the psychological use case — values read with a hash receipt) this gives the Peterson study **two receipted legs, psychological and neurological** — the connectivity reward HUF set out to deliver. Data + experiment in repo: `library/brain_kinetics_dwell_mesh.py`; write-up: `library/THE_BRAIN_DOES_KINETICS.md`. Refs: Carandini & Heeger (2012); Weber–Fechner; CONV-001 (`HUF/dormant/peterson-outreach/`).

## Quality discipline

Every paper in this ledger conforms to the **Proof & Honesty Standard** (`PROOF_AND_HONESTY_STANDARD.md`): numbers cited-or-fenced, math proven + receipted, value shown, experts decide — the discipline the whole series holds to.

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
