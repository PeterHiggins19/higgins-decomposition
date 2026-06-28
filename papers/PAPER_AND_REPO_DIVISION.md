# The paper / repository division of labour — a standing method for the Hˢ series

*How every Hˢ paper is built: the **repository carries the vast effort of data analysis**; the **paper
carries the higher intelligence** — the concept, the positioning, the synthesis. They point at each
other. This is the standing method for the whole P-series, not a one-off. Author: Peter Higgins (human
authorship for claims); AI-assisted per HUF-STD-001. Honest-broker.*

---

## The principle

A scientific result has two very different kinds of weight, and they belong in two different places.

- **The data effort → the repository.** Engines, runners, real datasets, figures, hashes, null
  scripts, reproduction recipes — the heavy, exact, voluminous machinery that *proves* the result.
  This is large, mechanical, and best read by running it. It lives in the Hˢ repository, versioned and
  hash-receipted.
- **The higher intelligence → the paper.** The concept, the framing, the positioning against prior art,
  the honest envelope, the one idea worth a reader's scarce attention. This is small, dense, and best
  read once. It lives in the arXiv paper.

The paper does **not** reproduce the data effort; it *summarises and points to it*. The repository does
**not** restate the concept; it *implements and points back to it*. Each is lighter, clearer, and more
honest for the division: the paper cannot hide a weak result behind volume, and the repository cannot
hide a thin idea behind a hash.

## The contract (every paper, every repo folder)

1. **The paper states the idea and the claim tiers, then delegates.** It carries: the thesis, the
   related-work positioning, the method *at concept level*, a *summary* of the worked evidence, the
   honest envelope, and a Reproducibility section that names the exact repository home.
2. **The repository folder carries the proof.** It holds: the data, the runner, the figures and their
   builder, the null/robustness scripts, and a `content_hash` such that *same data → same reading →
   same hash*. Anyone can re-derive every number the paper summarises.
3. **They cross-reference explicitly.** The paper's §Reproducibility points to the folder; the folder's
   README points to the paper. A reader who wants the mathematics, the engine, or the case can route in
   one hop.
4. **No claim without a receipt.** A number appears in a paper only if it is reproducible to a hash in
   the repository. The paper's confidence is borrowed entirely from the repository's reproducibility.

## Applied across the series

| Paper | Higher intelligence (paper) | Data effort (repository home) |
|---|---|---|
| **P1** | exact D=4 ILR↔SU(2) / lossless tiling — the math anchor | `Hs-Kinematics/`, `experiments/cnq_tiling_highd_2026-06/`, `experiments/exact_dim4_generator_2026-06/` |
| **P2** | deceptive-drift / honest-null monitoring | `experiments/` null runs |
| **P3** | the deterministic CN-TT instrument (tool/reproducibility) | `HCI-CNTT/`, parity experiments |
| **P4** | compositional kinematics (arrow of intent, the tower) | `Hs-Kinematics/`, the guest runs |
| **P5** | Compositional Character Space (cross-domain) | `library/` CCS battery |
| **P6** | compositional navigation in finance (this addition) | `industrial-instruments/financial/` |

Each row is the same contract: concept up top, proof below, a receipt joining them.

## Why this is the honest method

It enforces the framework's discipline structurally. The paper cannot overclaim, because every figure
it cites must reproduce to a hash someone else can run. The repository cannot drift into hand-waving,
because its job is to *be the evidence*, not to argue. And the reader is served the way each kind of
reader wants to be: the thinker reads the paper; the verifier runs the repository; the receipt assures
both they are looking at the same result.

*The intelligence argues; the data proves; the receipt binds them. One idea per paper, fully
reproducible below it.*

---

## A second, orthogonal axis — the deployment division

This page divides by **intelligence vs data** (concept up top, proof below). There is a second, independent
division by **deployment stream** — **MATH · INDUSTRY · GOVERNANCE**, each controlled, ordered backwards from the
dollar to the math — in [`../huf-gov/doctrine/THE_THREE_STREAM_DIVISION.md`](../huf-gov/doctrine/THE_THREE_STREAM_DIVISION.md)
(routing: `../huf-gov/doctrine/DIVISION_ROUTING.json`; Canada track: `../huf-gov/doctrine/CANADA_DIVISION.md`).
The two axes compose: a paper's *intelligence/data* split is independent of *which stream* it belongs to.
