# Does this methodology exist? Yes — and where Hˢ honestly fits it

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter asked
the right question: does "exact manifolds with planted, recoverable invariants" already exist as a study
methodology, and how does Hˢ fill the space? The honest answer: **the family is mature and has flagship
members** — Hˢ does **not** invent it. Hˢ is a **specialized member** that fills one under-served corner. This
positions the work against the prior art, claiming only the bounded niche. Sourced below. Peter is the sole
gate; nothing posted.*

---

## Yes, it exists — and it is a gold standard

The idea — *build an exact known-answer reference, run your method on it, check it recovers the planted truth* —
is established and respected in at least four communities:

1. **Method of Manufactured Solutions (MMS)** — the **gold standard for CFD / PDE code verification.** You
   *manufacture* an exact solution, substitute it into the governing equations to get a source term, run the
   solver, and confirm it recovers the manufactured solution at the theoretically expected convergence rate —
   "verification with a theorem-like quality" [1][2]. This is *exactly* the fluid/Reynolds case, done rigorously
   for decades.
2. **Simulation-Based Calibration (SBC)** — the **Bayesian/statistics analog**: simulate data from known
   parameters, refit, and check the ground-truth parameters rank uniformly in the recovered posteriors —
   validating an inference algorithm against self-recovery [3][4].
3. **Phantoms / Digital Reference Objects (DRO)** — in medical imaging and metrology: physical or digital
   objects with known properties to calibrate and validate instruments.
4. **Certified Reference Materials (CRM)** — in analytical chemistry/metrology: samples with certified
   composition used to calibrate measurements.

So "exact manifolds with planted, recoverable invariants" is **not a new paradigm.** It is the
manufactured-solution / known-answer-reference methodology, which is venerable. Honesty demands we say so first.

## Where Hˢ actually fills the space (the bounded niche)

Hˢ does not improve on MMS for PDEs or SBC for posteriors. It fills a **specific gap** none of them targets:

- **The compositional / parts-of-a-whole domain.** MMS lives in continuous PDE fields; SBC in probability
  models; phantoms in images; CRM in bulk chemistry. **None is built on the simplex.** Hˢ supplies the
  manufactured-reference method for quantities that are **parts of a conserved whole** — regime fractions,
  species fractions, spectra-as-composition, modal shares — under **Aitchison geometry.** It is, in one phrase,
  **"the Method of Manufactured Solutions for compositional data."**
- **Two exactness properties the others don't center, free by construction.** Where MMS recovers a solution at
  a convergence *rate* and SBC recovers parameters ~80–94 % with rank-uniformity [3], the Hˢ compositional
  reference gives, *exactly to the floor*: **conservation** (the budget closes, ~10⁻¹⁶) and **multiplicative
  gain-invariance** (the reference calibrates out a sensor's overall scale, ~10⁻¹⁵). The planted feature then
  recovers analytically (Re\* = 2300 exact; isotope peak exact). That gain-invariance is precisely the property
  a *calibration* reference wants and a PDE-verification reference does not need.
- **Content-addressed reproducibility.** Every reference and recovery carries a **SHA receipt**, so the
  verification is bit-reproducible by anyone — addressing the reproducibility concern the broader field has
  flagged. MMS/SBC are reproducible in principle but not content-addressed by default.
- **One geometry across domains.** The four-domain demo (`deterministic_manifold_factory.py`, `bd24835fa51edf7c`)
  runs fluid, chemistry, radiation, and field dynamics through **one** simplex engine — a uniform compositional
  V&V instrument, not a bespoke per-domain construction.

## The honest one-line placement

> Hˢ is **not** a new verification paradigm; it is the **compositional-data member of the manufactured-solution
> / simulation-based-calibration family** — the manufactured-reference method specialized to the simplex, with
> exact conservation and gain-invariance and a content-addressed receipt, under one geometry across domains.

That is a real, defensible contribution: a recognized methodology, extended to a domain (compositional
engineering quantities) where it was missing, with two exactness properties and a reproducibility layer that
suit *calibration* specifically. It also tells us how to publish it — *cite MMS and SBC as the parent
methodology*, and claim only the compositional specialization, never the invention of the family.

## Honest scope

- **T1 (measured):** the four-domain references conserve and gain-cancel to the floor and recover their planted
  invariants (`bd24835fa51edf7c`).
- **T2 (positioning):** that Hˢ is the compositional member of the MMS/SBC family is a reasoned placement
  against the cited prior art; the comparison to MMS's convergence-rate and SBC's rank-uniformity is qualitative
  (they answer slightly different verification questions).
- **Not claimed:** novelty of the manufactured-reference idea itself, superiority over MMS/SBC in their own
  domains, or that Hˢ replaces a CFD/Bayesian verification workflow. **Nothing posted; Peter is the sole gate.**

## Sources

1. Roy, *Verification of Euler/Navier–Stokes codes using the Method of Manufactured Solutions* (Int. J. Numer. Methods Fluids, 2004): [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1002/fld.660).
2. *Code Verification by the Method of Manufactured Solutions* (ASME J. Fluids Eng., 2002): [ASME](https://asmedigitalcollection.asme.org/fluidsengineering/article/124/1/4/462791/Code-Verification-by-the-Method-of-Manufactured).
3. Talts, Betancourt, Simpson, Vehtari, Gelman, *Validating Bayesian Inference Algorithms with Simulation-Based Calibration* (2018): [arXiv 1804.06788](https://arxiv.org/pdf/1804.06788).
4. *Posterior SBC: Simulation-Based Calibration Checking Conditional on Data* (2025): [arXiv 2502.03279](https://arxiv.org/html/2502.03279v2).

*Cross-refs: `deterministic_manifold_factory.py` + `THE_MANIFOLD_FACTORY_APPLICATION.md` (the application),
`../../experiments/son_generator_2026-06/son_exact_generator.py` (the exact generator),
`../../papers/frontier/THE_FULL_INSTRUMENT_FOR_LOW_DIM_TOPOLOGY.md` (the Piccirillo move). Peter is the sole gate;
nothing posted.*

*Proof & Honesty Standard — the parent methodology (MMS/SBC) is credited and cited first · Hˢ's niche is the
compositional specialization, stated bounded · the distinguishing properties (conservation, gain-invariance,
receipt, one geometry) are measured · no novelty of the family is claimed · the human keeps the gate.*
