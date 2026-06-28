# Compositional Navigation in Finance: a deterministic kinematic reading of allocation systems on the Aitchison simplex

**Author:** Peter Higgins. *AI-assisted per HUF-STD-001 (human authorship for all claims).*
**Status:** arXiv preprint draft (target: q-fin.ST / q-fin.PM; cross-list stat.AP). Key paper of the
Hˢ series; sequenced after P1 (the exact D=4 quaternion / tiling anchor) and P3 (the deterministic
tool paper). **Descriptive instrument — not investment advice, no forecast.**
**Data, code, figures, and full reproduction:** the Hˢ repository, `industrial-instruments/financial/`
(this paper carries the concept; the repository carries the data effort — see §7).

---

## Abstract

A portfolio, a desk, an index, a flow ledger — any allocation is a *composition*: parts of a whole,
tracked in order. Its realised path therefore lives on the Aitchison simplex and, read as a path, has a
**direction**. We present a deterministic, model-free, hash-receipted instrument that reads an observed
compositional financial trajectory as **kinematics**: the net *arrow of intent* (mass-weighted
momentum), the *helmsman* (loudest mover), the *character* (diffusive vs directed), the *effective
dimensionality*, and the *dated regime changes* where the system reorganises. The reading is purely
descriptive — it fits no model, estimates no probability, and predicts no price — and it is exactly
reproducible: the same data yields the same reading and the same SHA-256 receipt on any machine. We
position the instrument between two existing literatures it complements but is distinct from: *static
compositional-data finance* (which characterises and classifies snapshots) and *Stochastic Portfolio
Theory* (which models the market-weight process stochastically). A worked reading of a public S&P 500
ten-sector composition over 252 trading days illustrates the instrument, with a time-permutation null
reported honestly. The contribution is a reproducible *situational-awareness* instrument for a field of
many viewpoints: one map all parties can re-derive from the same receipt.

## 1. Introduction

Markets are argued over endlessly, but the *allocation* a system actually held over a window is not in
dispute — it is a recorded composition. What is missing is a way to read that recorded composition's
**motion** that is (i) descriptive rather than prescriptive, (ii) deterministic and reproducible rather
than model- and seed-dependent, and (iii) honest about its own limits. Practitioners reason about
"sector rotation" qualitatively; statisticians read allocations compositionally but as snapshots;
mathematical finance models the weight process as a stochastic object. None of these hands an
institution *inside the mix* a reproducible answer to the plain question: **where is my system, which
way is the whole carrying it, and where did it last reorganise?**

This paper offers that instrument. It is deliberately narrow: it reads what the data did, exactly, and
stops. Its confidence is epistemic — certainty about the reading and its reproducibility — not a claim
about the future.

## 2. Related work and positioning

**Stochastic Portfolio Theory (SPT; Fernholz, 2002).** The closest neighbour. SPT is *descriptive*
(not normative) and already places **market weights** on the simplex as a process over time, deriving
functionally generated portfolios and relative-arbitrage results. The distinction is sharp and
load-bearing: SPT is a **stochastic, model-theoretic** framework (continuous semimartingales,
probability measures, growth/drift). Our instrument is **deterministic and model-free**: it neither
posits a generating process nor derives a strategy; it reads the realised path and computes nothing
beyond it. Where SPT asks *what processes and strategies the weight dynamics admit*, we ask *what the
observed trajectory did*, reproducibly.

**Static compositional-data finance.** Compositional methods are increasingly applied to financial
ratios and allocations — e.g. compositional financial ratios (arXiv:2210.11138), and the CoDaWork 2026
contributions on allocation *proportionality* (Vega Baquero & Santolino) and compositional *bankruptcy
prediction* (Keivani & Coenders). These are snapshot or classification analyses. Our instrument is their
*kinematic* extension: same geometry, read in motion.

**Information geometry and econophysics.** Velocity and curvature on the probability simplex are
established in information geometry (Fisher-Rao-family metrics), and econophysics studies the geometric
distributional behaviour of price series. We work in the **Aitchison** metric specifically, on the
*allocation* composition rather than the price series, as a deterministic instrument rather than a
statistical model. The general prior art for "kinematics on the simplex" (replicator dynamics,
information geometry, CoDa's perturbation operator) is mapped in the companion prior-art assessment;
the present contribution is the descriptive, mass-weighted, noise-bounded reading applied to finance.

## 3. Method (concept)

Let `M` be a `T × D` array of allocation shares (rows sum to one). The reading proceeds in the standard
compositional way, then extends into motion:

1. **Aitchison geometry.** Closure and the centred-log-ratio (CLR) place the trajectory in real space
   (Aitchison, 1986; Egozcue & Pawlowsky-Glahn, 2003).
2. **Manifold projection.** The CLR trajectory is projected onto its leading principal axes — a faithful
   low-dimensional view of the path.
3. **Kinematic reads.** From the CLR perturbations between successive compositions: the **arrow of
   intent** (net mass-weighted momentum — where weight flows, distinct from the mass-blind helmsman); the
   **helmsman** (loudest single mover); **path efficiency** and **coherence** (near 0 ⇒ diffusive /
   rebalancing, near 1 ⇒ directed); the **effective dimensionality** (independent directions, an
   over-reading guard); and the **regime changes** from a noise-floor hold-lock that fires only when the
   composition reorganises beyond its own noise, with hysteresis.
4. **Determinism + receipt.** Every quantity is computed by a fixed, open engine and stamped with a
   SHA-256 content hash. Same data → same reading → same hash. The heavy implementation — engine,
   specification, language-agnostic pseudocode, and an R port — lives in the repository (§7).

The method asserts no probability model and no forecast. It reports only what the trajectory did, with
a stated noise-bounded ceiling on how far it will read.

## 4. A worked reading

On a public S&P 500 ten-sector composition over 252 trading days, the instrument reads: the **helmsman
is Financials**, and it is **shedding**; the **arrow of intent** flows toward *Communication Services,
Information Technology, Materials* and away from *Financials, Health Care, Consumer Discretionary*;
**path efficiency 0.066** and **coherence 0.048** mark a **rebalancing, diffusive** system rather than a
directed one; the motion runs in about **five** independent directions of ten; and the system shows
**five dated regime changes** (trading days 32, 72, 182, 209, 246). The reading is reproducible to
`content_hash = 5b2a32d6…`. Full data, the four figures (the share view, the CLR biplot, the navigation
manifold, and the per-part position panels), and an interactive projector are in the repository (§7);
this paper summarises rather than reproduces them, by design.

## 5. Robustness

To test whether the regime changes exceed what time alone would produce, we hold the composition fixed
and permute the order of days, destroying temporal structure, then re-detect. Over 2000 permutations
(seed 7), the real series shows **5** regime changes versus a null mean of **2.2** (sd 1.5), placing the
observation at the null's **95th percentile** (exceedance `p ≈ 0.08`). The honest reading: the
trajectory carries **more temporal organisation than a typical time-shuffle, but not a strong anomaly** —
fully consistent with a diffusive, rebalancing system. The value of the reading therefore lies in the
**dated locations** of the reorganisations and in the **directional** motion, not in any claim of
anomalous regime density. (Script: `industrial-instruments/financial/null_robustness.py`.)

## 6. Discussion — what it is, and is not

The instrument supplies *situational awareness*, not a signal. It is **descriptive, not predictive**: it
computes no probability, fits no model, forecasts no price, and recommends no trade. It is **not
investment advice**; what the motion means, and any decision, are the reader's. Its claims are tiered:
the reading is **Tier 1** (verified, reproducible); its relevance to any decision is **Tier 3** (the
expert's judgement). When the data cannot support a read, the instrument **holds or warns** rather than
return a confident wrong answer — a restraint that, in finance, is the source of trust rather than its
opposite. Because it takes no market view, it serves a field of many viewpoints equally: each can argue
its interpretation from one shared, audit-able map.

## 7. Reproducibility — and the division of labour

This paper is the concept; the **data effort lives in the repository**, by deliberate design (the Hˢ
paper/repository division, applied across the series): the engine and its specification, pseudocode and
R port (`Hs-Kinematics/`), the financial instrument, data, runner, figures, interactive projector, the
null script, and the full study (`industrial-instruments/financial/`). Every figure regenerates with
`build_visuals.py`; every reading reproduces with `run_financial.py` to the stated hash. The reader who
wants the mathematics goes to P1; the reader who wants the engine's reproducibility contract goes to P3;
the reader who wants to re-run this case goes to the repository folder above.

## References

- Aitchison, J. (1986). *The Statistical Analysis of Compositional Data.* Chapman & Hall.
- Egozcue, J.J., Pawlowsky-Glahn, V., et al. (2003). Isometric logratio transformations for compositional data analysis. *Mathematical Geology* 35(3).
- Fernholz, E.R. (2002). *Stochastic Portfolio Theory.* Springer.
- Linares-Mustarós, S., Coenders, G., et al. New financial ratios based on the compositional data methodology. arXiv:2210.11138.
- Vega Baquero, J.D., & Santolino, M. (2026). Proportionality between allocations in asset management. *CoDaWork 2026 Book of Abstracts* (Univ. Barcelona).
- Keivani, F., & Coenders, G. (2026). Adapting Altman's bankruptcy prediction model to the compositional data methodology. *CoDaWork 2026 Book of Abstracts* (Univ. Girona).
- Hofbauer, J., & Sigmund, K. (1998). *Evolutionary Games and Population Dynamics* (replicator velocity field). Cambridge.
- Amari, S. (2016). *Information Geometry and Its Applications* (velocity/acceleration on the simplex). Springer.
- Higgins, P. (2026). Hˢ series P1 (exact D=4 quaternion / tiling) and P3 (deterministic CN-TT tool); prior-art assessment `papers/PRIOR_ART_compositional_kinematics_2026-06-14.md`.

*Honest-broker. The instrument reads; the expert decides; the receipt carries the proof.*
