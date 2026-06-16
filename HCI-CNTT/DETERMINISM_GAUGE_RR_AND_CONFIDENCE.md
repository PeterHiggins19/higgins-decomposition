# Determinism, Gauge R&R, and Confidence — what we can claim, and how to answer industry

*Engine doctrine (HCI-CNTT). Companion to PRECISION_AND_CONTROL.md. Written after a deliberately loaded question — "can we say ≥6σ on any viable dataset?" — because that is the exact question every industrial reviewer and every metrologist will ask, and getting the answer shaped correctly matters more than getting a big number. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker; claim tiers at the end. Every quantitative statement is Tier-1 measured or flagged otherwise.*

---

## 0. Why this note exists (the learning frame)

Industry uses statistics because their gauges are noisy and they have never owned a gauge with zero repeatability error. So when we say "deterministic," it sounds like marketing, not measurement. The honest move is not to claim a single heroic sigma — it is to translate what the engine actually guarantees into the language industry already trusts (Gauge R&R / MSA, uncertainty propagation, the GUM), and to be scrupulous about the line between what is *deterministic* and what is *inferential*. The loaded question was worth asking out loud because it forces that line into the open. The lesson, for all of us: **never let determinism and confidence collapse into one number.** State them separately, validate them separately, and you satisfy both the metrologist and the statistician.

## 1. Two layers, two kinds of certainty

The system has two layers, and they carry different kinds of truth. Conflating them is the single most common error this note exists to prevent.

**Layer 1 — the transform (deterministic).** Closure → CLR/ILR → tiling → reconstruction → hash. Given the *same input bits*, it returns the *same output bits* to the IEEE floor (~1e-15), on every machine, every run, verified by a content hash. This is not a statistical claim; it is a checksum-grade guarantee. You audit it the way you audit a file transfer — re-run and compare hashes — not with a t-test.

**Layer 2 — the inference (statistical).** "Is this regime change real? Is this drift deceptive? Does this correlation hold?" These depend on the data's noise, and here statistics correctly re-enter: a falsifiable null, a p-value, a confidence level. The deceptive-drift label-permutation null is the worked example — and the honest result was modest (Australia at p≈0.0011 ≈ 3.3σ; only 1 of 9 countries significant at annual grain). That is the data's verdict, not the engine's.

Determinism and statistics are not competitors. They live in different layers and get **different validation protocols**.

## 2. Where the engine sits in Gauge R&R (MSA)

Measurement-Systems Analysis decomposes total observed variation:

> σ²_total = σ²_part (true part-to-part) + σ²_gauge, where σ²_gauge = Repeatability (equipment, EV) + Reproducibility (appraiser/conditions, AV).

Acceptance is by %GRR (= σ_gauge / σ_total or / tolerance): <10% good, 10–30% conditional, >30% unacceptable; and ndc = 1.41·(PV/GRR) ≥ 5 distinct categories.

**The engine's contribution to gauge error is machine epsilon.**

- *Repeatability (EV) of the engine ≈ 1e-15.* Same input → same output, bit-for-bit. There is no equipment scatter in the math.
- *Reproducibility (AV) of the engine = exact.* Different operators, platforms, runs → the identical hash. There is no appraiser variation in the transform.
- Therefore the engine's %GRR contribution ≈ 0 and the ndc it permits is effectively unbounded — it never blurs two distinct inputs above ~1e-15.

This is a genuine, demonstrable selling point: **the analysis stage adds no measurement variation.** It is provable with a "determinism certificate" — re-run N times across platforms, show identical hashes — which is a *stronger* artifact than a %GRR number, because it is exact rather than estimated.

## 3. The honest limit — the engine is the back end of the chain

Here is the line a sharp metrologist will press, and the answer that builds credibility rather than losing it:

**The engine guarantees identical *output* for identical *input*. It does not, and cannot, make noisy re-measurements agree.** The physical front end — the gas analyzer, the assay, the sequencer, the sampling — still has real R&R. So:

> total system R&R = (sensor + sampling R&R)  ⊕  (engine ≈ 0)

We remove the **computation/analysis** component of measurement variation entirely; we do **not** touch the **sensing/sampling** component. The remaining R&R in a full study is essentially *your sensors'* R&R. Said plainly to industry: *"Run your standard ANOVA Gauge R&R on the whole chain — sensor through engine — and whatever %GRR you measure is your sensor, because our stage contributes epsilon. We can then help you characterize and propagate that, but we won't pretend to have removed it."* This is the distinction between **computational reproducibility** (engine: perfect) and **measurement reproducibility** (chain: sensor-limited). Stating it first is what earns trust.

## 4. Uncertainty propagation — the engine propagates, it does not add

Because the transform is exact and differentiable, sensor uncertainty passes through it cleanly: if the sensor delivers composition x ± δx, the output is f(x) with uncertainty ≈ J·δx (Jacobian propagation), or by Monte-Carlo through the exact transform — with **no additional model error introduced by the analysis**. The output's uncertainty is traceable entirely to the input's. This is metrologically clean and GUM-compatible (ISO/IEC Guide 98-3): a perfect transform is the *ideal* object to propagate uncertainty through, because it contributes none of its own. The number industry actually wants — output uncertainty — is therefore just their characterized input uncertainty, faithfully carried.

## 5. The value-add beyond zero-R&R — a discriminating axis others are blind to

Zero analysis-R&R is the defensive claim. The offensive one: the engine reads the **composition / ratio axis (MC-4)** that magnitude-only single-channel gauges cannot see. So it can separate parts, batches, or regimes that conventional instrumentation calls identical — an ndc improvement *in a dimension the incumbent gauge does not measure at all* (the real-data example: in the USGS produced-water brines the dominant drivers were the minor ions SO₄/HCO₃, invisible to a magnitude read of the Na-Cl bulk). That is a new measurement capability, not just a cleaner version of the old one.

## 6. How to validate each layer (the protocol industry can run)

- **Transform (Layer 1):** a determinism certificate — N re-runs across platforms, identical content hashes. Exact V&V, stronger than a %GRR. Plus a conventional ANOVA Gauge R&R on the full chain to show the engine's contribution is epsilon and the measured R&R is the sensor's.
- **Inference (Layer 2):** a falsifiable null (the label-permutation / time-shuffle family, which itself passed a kill-test) reporting a calibrated p-value; a stated decision gate; and **replication across independent datasets** to compound confidence.

## 7. The confidence-gate policy (what to put on a spec sheet)

- **Determinism is not sigma — do not convert it.** Exact reconstruction is algebra, not inference. Calling it "infinite sigma" is a category error that would let a reviewer dismiss the real statistical claims alongside it.
- **6σ / 9σ are a decision gate, not a per-dataset guarantee.** Defensible wording: *"The instrument emits an actionable claim only when the evidence clears 6σ for industrial action or 9σ for research, and honestly withholds — reporting hold / no-signal / insufficient-confidence — otherwise."* This mirrors the physics 5σ discovery convention and is a statement about *when we act*, not about what every dataset yields.
- **9σ is reached by independent replication, not by one dataset.** This is the only legitimate use of the 3ⁿ confidence index: independent confirmations compound (e.g. O₂ the dominant helmsman in 13/13 independent anaesthesia cases across two hospitals). Manufacturing 6σ from a single dataset by invoking the formula over non-independent reads is the pseudo-replication fallacy — the fastest way to discredit the whole project. The index is valid only over genuinely independent channels.
- **"Six Sigma" (quality) ≠ "6σ" (significance).** Manufacturing's Six Sigma is 3.4 defects per million ≈ 4.5σ short-term — a defect-rate/process-capability metric, a different animal from a hypothesis-test confidence. Say which you mean.

Reference values (two-sided, computed): 3σ ≈ 1 in 370; 5σ ≈ 1 in 1.7M (physics discovery); 6σ ≈ 1 in 5×10⁸; 9σ ≈ 1 in 4×10¹⁸.

## 8. Analogies for a statistics-only audience

- **Checksum vs. poll.** You don't run a t-test to know a file copied correctly — you compare checksums (deterministic). You do run statistics to know a drug works (noisy biology). The engine is a checksum-grade transform feeding a statistical inference. Use the right tool per layer.
- **Ruler vs. eyeballing.** Statistics-only is averaging many eyeball guesses because the instrument is noisy. We hand you a ruler with perfect, traceable graduations for the math step; your remaining uncertainty is only how well you can see the object's edge (the sensor).
- **The CMM precedent.** Industry already accepts this structure: a coordinate-measuring machine computes geometry deterministically from probe points that have R&R. We are making the same split explicit — and adding the composition axis.

## 9. Claim tiers and the one-line standard

- Engine repeatability ~1e-15, exact cross-platform reproducibility (hash-verified), engine %GRR ≈ 0, exact uncertainty propagation — **Tier 1** (measured / demonstrable).
- The MC-4 discriminating-axis value-add — **Tier 1** on the cases run; **Tier 2** as a general guarantee.
- The 6σ/9σ decision-gate policy and the independence rule — **governance standard** (a policy we adopt, not an empirical result).
- "≥6σ on any viable dataset" — **rejected** (an overclaim; confidence is bounded by the data, and the system's honest outputs include correctly reporting *low* confidence on weak data).

**The standard, in one line:** *On any valid composition the engine is deterministically lossless and reproducible to the IEEE floor — contributing ≈ zero gauge R&R and propagating your sensor uncertainty exactly; for inferential claims it enforces a 6σ gate for industrial action and 9σ for research, withholding when the data cannot clear it, and reaching those levels by independent replication rather than from any single dataset.*

Every word of that is defensible. That is a better story than "6σ on everything" — because it is auditable.
