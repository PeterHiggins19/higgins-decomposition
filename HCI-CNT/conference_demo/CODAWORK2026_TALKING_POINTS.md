# CodaWork 2026 — Talking Points (tone-calibration overlay)

**Companion to:** [`CODAWORK2026_TALK_PLAN.md`](CODAWORK2026_TALK_PLAN.md)
**Status:** Tone-calibration overlay (push #23, 2026-05-07).
The TALK_PLAN is the authoritative slide-by-slide script. This document
overlays delivery notes and audience-framing guidance from the 2026-05-07
ChatGPT cross-check pass. Slides and timing are unchanged.

---

## Headline framing (the answer to "what is this talk about")

> **"A deterministic, hash-chained instrument that takes a compositional
> CSV and produces an audit-grade report. Classical CoDa plates inside,
> trajectory-native operators added, every byte reproducible by anyone
> with the raw data."**

That sentence wins the talk. Lead with it on Slide 1, return to it before
the demo, close with it after the 3D projector.

What does **not** win the talk: leading with "we found that compositional
dynamics live in a quaternion algebra." That sentence is true (and
documented in Volume IV), but it is the depth statement, not the headline.
Audiences at CodaWork are CoDa practitioners; they want to know whether
this is something they can use on their data tomorrow. The depth
statement is for the journal paper.

---

## Where Volume IV (Quaternion View) belongs in the talk

**Not in the main 15 minutes.** The slide deck stays at the channel-form
CNT description (θ, ω, κ, σ + period-2 attractor + IR class). The
quaternion-view interpretation is a one-line mention, not a section.

**Where to place it:** one sentence in Slide 2 (Value to the CoDa
community), folded into the "what's new" list, and one sentence in Q&A
prep below.

**Recommended one-sentence form for Slide 2:**

> "Recently integrated as Volume IV of the canonical handbook: a
> compact algebraic interpretation of what these four channels measure —
> for the D=4 case, they are the four components of a unit quaternion
> in disguise. Three IEEE-floor confirmations across drive failures,
> CMB photons, and SM neutrino oscillation. Documented; not the talk."

If asked to expand in Q&A, the Q&A pre-emption below covers it.

**Why this placement:** the talk's strongest 15 minutes are (a) the
deterministic-engine demonstration, (b) the classical-plates-plus-
trajectory-operators framing, (c) the live demo. Volume IV is real and
the math is locked, but it is a depth claim that needs ~10 minutes of
dedicated explanation to land properly. Trying to compress it into the
main talk weakens both halves.

---

## Tone calibration for the CoDa audience

**Be additive, not displacive.** The talk's job is to extend the CoDa
community's toolkit, not to claim that CNT replaces CoDa. The existing
slide deck does this well; keep that posture.

**Lead with the deterministic engine, not the math.** The most
distinctive thing about CNT is the byte-identical reproducibility
chain. Most CoDa toolkits do not promise this. The math is good but
the determinism contract is the differentiator.

**Use the corpus as the proof.** 25 experiments, all green, all
byte-identical across re-runs, all reachable via the public repo.
Show this number; it is hard-earned and quantitative.

**Concede what the engine does not yet do.** Explicitly: it doesn't
do compositional kriging, it doesn't do Bayesian updating, it doesn't
do causal inference. Saying so up front buys credibility for the
claims that are made.

**The one-sentence value prop is not "look what we discovered" but
"here is a working tool you can use."** The discovery framings (Volume
IV, the universal LIMIT_CYCLE_P2 signature) are real, but they are
positioned as findings the tool produces — not as the tool's reason for
existing.

---

## Q&A pre-emption — Volume IV question pack

These are the questions a sharp listener will ask if Volume IV gets a
one-sentence mention. Answer briefly; defer to the handbook for depth.

**Q: "What does the quaternion interpretation actually buy you?"**
> "Three things. First, a precise algebraic statement of what each CNT
> channel IS — they're the four components of a unit quaternion in
> disguise, for D=4. Second, a second independent verification path
> for any result — the Hs-CNQ engine sketch in the handbook gives a
> parallel `cnq_content_sha256` reviewers can check against the CNT
> hash. Third, a path to dimensionally larger systems via the bi-
> quaternion factoring at D=8 and Clifford algebras at general D.
> All of that is documented; none of it is needed to use the engine
> today."

**Q: "How exact is the quaternion identification?"**
> "Bit-identical at the IEEE 754 floor — 4.441 × 10⁻¹⁶ across three
> independent confirmations on disparate datasets: drive failures,
> Planck CMB photons, SM neutrino oscillation. That's the same
> residual you'd get from any rounding error of the same operations
> in any order. The identification is mathematically exact; the residual
> is floating-point representation."

**Q: "Why hasn't this been mentioned in the talk so far?"**
> "Because it's a depth claim that needs ten minutes of math to land
> properly, and the talk's job today is the working instrument. Volume
> IV is the journal-paper material. Happy to walk through it after the
> session for anyone interested."

**Q: "Is the CNQ engine you mentioned implemented?"**
> "Not yet. The proposal is in the QD experimental folder — it's a
> ~14-day implementation that produces a parallel `cnq_content_sha256`
> as a second verification path. Whether to implement it depends on
> whether the CoDa community sees value in a quaternion-native sibling
> engine. That's a conversation I'm hoping this talk starts, not one
> the talk needs to finish."

---

## Q&A pre-emption — engine and determinism questions

**Q: "How do you handle missing data?"**
> "δ-replacement before closure, δ value reported in
> `metadata.engine_config.DEFAULT_DELTA` of every JSON output.
> Anyone using a different δ produces a different `content_sha256` by
> design. The choice is the analyst's; the audit chain captures it."

**Q: "What about subcompositional coherence?"**
> "Engine respects it via the standard CoDa machinery — same closure,
> same CLR, same Helmert ILR. The CNT operators (θ, ω, κ, σ) are
> defined on the ILR coordinates and inherit subcompositional
> coherence from there. The handbook Volume I §F-§G has the formal
> argument."

**Q: "How do I run this on my data?"**
> "Five commands documented in the README. Adapter for your data
> format, Mission Command runs the pipeline, JSON + PDF + Stage 1-4
> plates land in the experiment directory. CCTT_RUNBOOK.md walks
> through it phase-by-phase if you want guardrails."

**Q: "Where can I find the engine code?"**
> "Public repo on GitHub — `PeterHiggins19/higgins-decomposition`.
> Engine is `Hs/HCI-CNT/engine/cnt.py`, parallel R port at `cnt.R`.
> Determinism gate is `Hs/HCI-CNT/engine/tests/test_determinism.py`,
> 25-experiment corpus at `Hs/HCI-CNT/experiments/`."

**Q: "Will the byte-identical hash hold across Python versions / OSes?"**
> "Yes — Volume III §A documents the determinism contract: same Python
> minor version, same library set, same input bytes → same content_sha256.
> The contract has been audited across the corpus, the gate enforces it."

---

## Closing-line options

The TALK_PLAN ends with the 3D projector. The verbal closing line should
land the headline framing one more time. Three workable options, choose
on the day:

**Option A (toolkit-positioning):**
> "That's CNT. A deterministic, hash-chained extension to the CoDa
> toolkit. Public repo, 25 corpus experiments, 5 commands to run on
> your data. Volume IV in the handbook for the math story. Happy to
> talk after."

**Option B (cross-dataset framing):**
> "Same engine, twenty-five corpus experiments, hash-identical
> reproduction every time. Energy mixes, geochemistry, drive
> failures, irrigation, neutrinos, CMB photons. The instrument
> doesn't care what the carriers are; it just measures the
> trajectory. Try it on yours."

**Option C (invitation):**
> "Everything I showed today is in the public repo. The CCTT
> protocol walks any dataset through to a CNT-grade JSON in seven
> phases. If you have a compositional time series you want to try
> on it, find me at the break — I'll run it before the next session."

---

## What this overlay isn't

**Not a slide change.** Slides and timing are unchanged from
CODAWORK2026_TALK_PLAN.md.

**Not a doctrine change.** The 25-experiment determinism gate, schema
2.1.0, and engine 2.0.4 are all unchanged.

**Not a Volume IV demotion.** Volume IV is canonical — see
[`../handbook/VOLUME_4_QUATERNION_VIEW.md`](../handbook/VOLUME_4_QUATERNION_VIEW.md).
This overlay just calibrates how it's mentioned in the talk vs how it's
treated in the handbook.

**Not a hard rule.** The speaker's judgement on the day overrides the
overlay. If the audience wants the depth claim early, give it; if they
want only the working instrument, defer Volume IV to Q&A entirely.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
*Lead with the working tool. The depth claim is in the handbook.*
