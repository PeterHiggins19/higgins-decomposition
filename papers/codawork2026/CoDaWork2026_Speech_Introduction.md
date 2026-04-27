# CoDaWork 2026 — Speech
## Hˢ: A Compositional Inference Engine on the Simplex

**Peter Higgins — Markham, Ontario, Canada**
**CoDaWork 2026, Coimbra, Portugal**

*Speaker notes in [brackets]. Slide cues in **bold**.*

---

## Introduction (3 minutes)

**[SLIDE 1 — Title]**

Good morning. My name is Peter Higgins. I am an independent researcher from Markham, Ontario.

I would like to thank the CoDaWork community for building a fine engine. Let me introduce the autonomous vehicle it fits.

**[SLIDE 2 — Pipeline overview]**

Four years ago I was working on loudspeaker diffraction correction — a signal processing problem where you decompose a waveform into the parts that arrive at the listener's ear from the cabinet edge, the driver cone, and the baffle surface. These are compositional parts. They sum to the total field. I needed a way to read what the composition was doing without disturbing it.

I found Aitchison.

The simplex geometry that this community has developed over the past forty years turned out to be exactly the instrument I needed. Not approximately — exactly. The centred log-ratio transform. The Aitchison distance. The geometric mean as the natural centre. The closure constraint. I did not invent any of this. You did.

What I built on top of it is a twelve-step deterministic pipeline called Hˢ — Higgins Decomposition on the Simplex. It takes any compositional data — any N-by-D matrix where the rows sum to a constant — and produces a geometric diagnosis. Not a model. Not a fit. A reading of what is already there.

Here is what the twelve steps do. Close to the simplex. Replace zeros. Transform via CLR. Track cumulative Aitchison variance. Fit a vertex lock diagnostic — we call it the HVLD — which tells you whether the composition is integrating or segregating over the observation index. Test proximity to thirty-five transcendental constants. Validate entropy invariance under geometric-mean decimation. Decompose per-carrier contributions. Measure transfer entropy between carriers. Analyse ratio-pair stability. Generate a compositional fingerprint.

Every step is deterministic. No stochastic elements. Run it twice on the same data, you get bit-identical output. SHA-256 hash verification. Four input guards reject bad data before the pipeline starts. Seventy-eight diagnostic codes report what the pipeline found. Ten structural modes combine codes into investigation prompts. Reports in five languages. Full audit trail with chain of custody.

**[SLIDE 3 — Scale and scope]**

We have run this pipeline on twenty-five experiments across eighteen physical domains — from nuclear binding energy at the femtometer scale to the composition of the universe at the Hubble radius. Forty-four orders of magnitude. Gold prices over three hundred and thirty-eight years. Quark flavour fractions. Gravitational wave energy budgets. Drive fleet reliability data. Municipal budget allocations. Traffic signal timing across eight hundred and thirty-one intersections. Radionuclide decay chains. Published high-energy physics measurements from HEPData — W boson decay, Higgs branching ratios, top quark helicity, Z boson widths.

The same twelve steps. The same codes. The same simplex.

Fifteen of fifteen physical experiments classify as NATURAL — meaning the variance trajectory locks to a transcendental constant within one percent of that constant's value. The tightest match is delta equals five point eight seven times ten to the negative six, in nuclear binding energy. That is the semi-empirical mass formula — Bethe-Weizsäcker — decomposed into five carriers, with no free parameters, locking to one over pi to the power of e at the strontium shell-closure boundary.

I did not go looking for that. The pipeline found it. I am an audio engineer.

**[Pause. Let that land.]**

But that is not what I came here to show you today. I came to show you the hardest experiment I could find. And I came to ask this community for help with the things I cannot prove.

**[SLIDE 4 — Cosmic energy budget title]**

---

*[Speech continues with Act 2: The Centrepiece — the cosmic energy budget demonstration. To be written in next session.]*

---

## Speaker Notes

**Tone:** Conversational, not academic. Peter is an engineer talking to mathematicians. He respects what they built. He is showing what he built on top of it. He is honest about what he does not know.

**Pacing:** The introduction covers a lot of ground in three minutes. Do not rush. The opening line and the "I am an audio engineer" line are the two moments that need space. Everything else can be delivered at normal speed.

**Key moments to land:**
1. "I would like to thank the CoDaWork community for building a fine engine." — Genuine gratitude, not flattery.
2. "I found Aitchison." — The moment the project changed.
3. "I am an audio engineer." — After describing femtometer-to-Hubble-radius validation. The contrast is the point.
4. "I came to ask this community for help with the things I cannot prove." — Sets up Act 3.

**What NOT to do:**
- Do not apologise for not being a mathematician. The work speaks.
- Do not oversell the transcendental matches. Report them as detections, not as established physics.
- Do not speed through the pipeline steps. The audience needs to hear that every step is standard CoDa until step 7 (HVLD), which is new.
- Do not use jargon the audience does not share. They know CoDa. They may not know SEMF, Planck parameters, or Friedmann equations. Translate.

---

*Peter Higgins, 2026*
