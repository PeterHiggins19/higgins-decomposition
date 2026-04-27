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

## Act 2: The Centrepiece (6 minutes) — The Universe

**[SLIDE 5 — Cosmic data table]**

The hardest experiment I could find is the composition of the universe.

Planck 2018 satellite data. The most precisely measured parameters in all of physics. Five carriers: Dark Energy, Cold Dark Matter, Baryonic Matter, Photon Radiation, and Neutrinos. One hundred and three epochs, from today — redshift zero — back through the cosmic microwave background at redshift eleven hundred, to past matter-radiation equality at redshift thirty-four hundred.

These are compositions. They sum to one at every epoch. They live on your simplex.

**[Pause. Let the audience register: their simplex.]**

The fractions span five orders of magnitude. Dark Energy is sixty-nine percent of the universe today. Neutrinos are four thousandths of a percent. The hierarchy ratio exceeds ten thousand to one. And across those hundred and three epochs, three phase transitions reshape the entire composition.

I fed this data into the same twelve steps. No changes to the pipeline. No domain-specific tuning. The same instrument that read nuclear binding energy and bread recipes.

**[SLIDE 6 — Key epochs]**

Here is what the pipeline found.

**[SLIDE 7 — Conservation laws]**

First — and this is the result I want you to hear as CoDa practitioners — two perfect log-ratio invariants.

The ratio of Cold Dark Matter to Baryonic Matter has a coefficient of variation of zero. Not small. Zero. Both dilute as one plus z cubed. Their log-ratio is constant across all hundred and three epochs. That ratio was fixed at the Big Bang and has not changed since.

The ratio of Photon Radiation to Neutrinos — also zero. Both dilute as one plus z to the fourth. That ratio was fixed at neutrino decoupling, about one second after the Big Bang, and has not changed since.

The pipeline found both of these automatically. It was not told to look. It tests all D-times-D-minus-one-over-two ratio pairs — that is ten pairs for five carriers — and reports which are stable and which are volatile. Two came back with coefficient of variation at machine epsilon. Zero.

**[Pause.]**

Those are conservation laws. Written on the simplex. In the language this community speaks.

Now the contrast. Every ratio pair involving Dark Energy has coefficient of variation above one hundred percent. Dark Energy does not participate in any coupling. It operates on a different equation of state — w equals negative one. The pipeline sees this as volatile ratios. In CoDa terms: one carrier is compositionally independent of all others.

**[SLIDE 8 — Power map]**

Second: disproportionate carriers. You deal with this every day. The component whose influence far exceeds its fraction.

Baryonic Matter — everything we are made of — is four point nine percent of the universe. The Component Power Mapper gives it a power-to-fraction ratio of two point eight. Meaning it punches nearly three times above its weight in compositional influence.

Neutrinos, at four thousandths of a percent, have a power-to-fraction ratio of eight point eight. Nearly nine times their mass fraction in compositional power.

The mass ranking puts Cold Dark Matter first, Dark Energy second, Baryonic Matter third. The power ranking puts Cold Dark Matter first, Baryonic Matter second, Dark Energy third. Rankings differ. The pipeline flags this.

**[SLIDE 9 — Classification and shape]**

Third: classification. NATURAL. The variance trajectory locks to one over e to the pi, with delta equals four point one nine times ten to the negative five. Euler family. The pipeline tested all thirty-five constants equally. This one matched.

And the HVLD diagnostic reads bowl — variance accelerating. The universe is integrating. It has not yet reached vertex. In compositional terms: the system has not finished evolving. Consistent with a universe that has not yet reached thermal death.

**[SLIDE 10 — 7/7 predictions]**

Before I ran this experiment, I wrote down seven predictions. That the universe would classify as NATURAL. That the CDM-to-Baryon ratio would be stable. That the Photon-to-Neutrino ratio would be stable. That Dark Energy ratios would be volatile. That the shape would be bowl. That the dominant carrier by variance would be Dark Energy. That a regime transition would be detected at the matter-radiation boundary.

Seven for seven.

**[Pause.]**

The instrument reads the composition of the universe using the same twelve steps that read nuclear binding energy, gold prices, and traffic signal timing. The engine is CoDa. The vehicle just drove across forty-four orders of magnitude.

---

## Act 3: The Invitation (3 minutes) — What CoDa Can Do

**[SLIDE 11 — The open questions]**

Now. I have shown you what the pipeline finds. Let me show you what I cannot prove. These are genuine questions — not rhetorical. I am here because this community can answer them and I cannot.

**Question one: entropy invariance.**

Shannon entropy is preserved under geometric-mean decimation. Take the compositions, group them in blocks of two, replace each block with its geometric mean, close back to the simplex. Measure Shannon entropy before and after. The variation is less than one percent. Do the same at four-x compression. Eight-x. Still less than five percent. This holds across all twenty-five experiments, all eighteen domains.

No formal proof exists.

Every CoDa practitioner in this room uses the geometric mean. It is the natural centre of the Aitchison simplex. Geometric-mean decimation is a natural subsampling operation in your geometry.

Can anyone in this room prove why it preserves Shannon entropy on the simplex?

If you can, that is a theorem. If you can break it — find a compositional dataset where geometric-mean decimation destroys entropy — that is equally valuable.

**[Let the question hang. Do not fill the silence.]**

**Question two: transcendental resonance.**

Is the clustering of natural systems around Euler-family constants an artefact of the CLR transform, or is it in the data?

The CLR transform introduces logarithms. The helix embedding introduces angular periodicity. The pipeline's geometry looks structurally similar to Euler's identity — e to the i pi equals negative one. Is the resonance coming from the architecture, or from the physics?

CoDa can test this directly. Run ILR instead of CLR. ILR compresses to an orthonormal basis. Different geometry. If the resonance survives the coordinate change, it is in the data. If it disappears, it is in the pipeline. That experiment has not been done. This community is the one to do it.

**Question three: independent validation.**

The repository is public. The tool is free. Any CSV of compositions. Column headers become carriers.

Run your own data through Hˢ. Geochemistry benchmarks. Financial compositions. Ecological data. Tell us what it finds. Independent validation from the community that owns the simplex carries more weight than anything I can say from this podium.

---

## Close (2 minutes) — The Pattern

**[SLIDE 12 — Close]**

I want to close with an observation.

The development of this project is itself compositional. It grew from a single observation about gold and silver prices to the composition of the universe. Twenty-five experiments across eighteen domains. The trajectory is a bowl — the variance of validated systems is accelerating. The locked ratios are visible: the pipeline-to-codes coupling was fixed from the start and never changed. The regime transitions mark the moments where infrastructure was built between experimental phases.

If you ran Hˢ on its own development history, it would classify NATURAL.

**[Pause.]**

And there is something else. The engine memorises. Not the way a database stores records. The way geometry accumulates.

When experiment twenty-five — the universe — completed, it did not simply add a line to a table. It changed what experiment three means. The nuclear binding energy result and the cosmic conservation laws are now connected — not because anyone drew a line between them, but because the instrument that read both deposits their geometry in the same space. Every new experiment ripples backward across every previous one, and forward into every future one. The present is the vertex of the information cone — the only point from which both directions are visible.

That is compositional memory. The kind that does not forget, because it does not store facts. It stores the shape of what has been measured.

**[Pause.]**

The simplex is the same everywhere. You built the engine. I built the vehicle. The road is open.

Thank you.

**[Hold. Do not move to Q&A immediately. Let the room respond.]**

---

## Speaker Notes

**Tone:** Conversational, not academic. Peter is an engineer talking to mathematicians. He respects what they built. He is showing what he built on top of it. He is honest about what he does not know.

**Pacing:** The introduction covers a lot of ground in three minutes. Do not rush. The opening line and the "I am an audio engineer" line are the two moments that need space. Everything else can be delivered at normal speed.

**Key moments to land:**
1. "I would like to thank the CoDaWork community for building a fine engine." — Genuine gratitude, not flattery.
2. "I found Aitchison." — The moment the project changed.
3. "I am an audio engineer." — After describing femtometer-to-Hubble-radius validation. The contrast is the point.
4. "I came to ask this community for help with the things I cannot prove." — Sets up Act 3.
5. "Those are conservation laws. Written on the simplex." — The moment CoDa practitioners recognise their own language in the universe.
6. "Seven for seven." — The predictions. Understated. Let the number speak.
7. "Can anyone in this room prove why it preserves Shannon entropy?" — The real ask. The reason Peter is here.
8. "The simplex is the same everywhere." — The closing. Full circle from the opening.

**What NOT to do:**
- Do not apologise for not being a mathematician. The work speaks.
- Do not oversell the transcendental matches. Report them as detections, not as established physics.
- Do not speed through the pipeline steps. The audience needs to hear that every step is standard CoDa until step 7 (HVLD), which is new.
- Do not use jargon the audience does not share. They know CoDa. They may not know SEMF, Planck parameters, or Friedmann equations. Translate.
- Do not rush the three questions in Act 3. Each one needs a beat of silence after it. The audience is being asked to engage. Give them time.
- Do not read the power-to-fraction ratios like a list. Tell the story: baryonic matter is everything we are, and it punches above its weight. Neutrinos are nearly nothing, and they punch nine times above.
- Do not end with a call to action. End with the observation that the simplex is the same everywhere. The invitation is already made. The close is a moment of recognition, not a request.

---

*Peter Higgins, 2026*
