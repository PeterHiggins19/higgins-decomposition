---
title: "Speaking Script + Q&A Bench — 13-slide expanded talk"
subtitle: "CoDaWork 2026 · Coimbra, Portugal · 1–5 June 2026"
author: "Peter Higgins · Rogue Wave Audio / Binaural Test Lab"
date: "2026-05-27"
geometry: "landscape, margin=0.5in"
fontsize: 10pt
documentclass: article
header-includes:
  - \usepackage{xcolor}
  - \usepackage{array}
  - \renewcommand{\arraystretch}{1.25}
---

# Speaking Script + Q&A Bench — 13-slide expanded talk

**Deck:** `CodaWork2026_Presentation_2026-05-27.pptx` — the single presentation file: 13 talk slides + a 15-slide data appendix (slides 14–28) covering the **six corpus countries beyond the three case studies** — a data view and a full-trajectory diagram for each. One file, no switching, no repetition (Germany / Japan / UK are already in the talk).

**Timing:** ~13 min spoken across 13 slides · +1 min live HTML projector intro = **14 min presentation** · then **5 min Q&A** (≈20-minute slot).

**How to read this page:** left column is what you say on each slide (read from this). Right column is the Q&A bench — likely questions for that slide with ready responses. Glance right only if the question lands; otherwise the left column carries the whole talk.

**Voice notes:** No preamble. Periods, not commas. Numbers first, qualifier after. Slow on the case-study pairs (slides 6–11). On the navigation slides (7, 9, 11) let the chart breathe — about 50 seconds each, unhurried. The talk is paced to fill 13 minutes comfortably; do not rush.

---

## Slide 1 · Title + question + contact + follow-along + CoDa-tools framing   ·   50 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Good morning. *Compositional monitoring of energy-mix drift on the simplex.*

The question of this talk: **which carrier did the structural work?** Not which one got bigger. Which one moved the composition.

Follow along on the repository — the slide deck, manuscript, and live projector are all open. The framework runs any compositional dataset the CoDa community can describe; what you'll see in the next thirteen minutes is reproducible on your data.

My email and the repo URL are on this slide. The one-page handout is in six UN languages. Let me begin.

</td>
<td>

**Q:** Who are you / what's BTL?
**A:** Audio/electronics engineer; founder of the Binaural Test Lab at Rogue Wave Audio in Markham, Ontario. Hˢ generalised retroactively from acoustic compositional work.

**Q:** How long is the talk?
**A:** ~13 minutes spoken across 13 slides, then ~1 minute introducing the live HTML projector — 14 minutes of presentation — then 5 minutes of Q&A. About a 20-minute slot.

**Q:** "Any compositional dataset" — what does that include?
**A:** Anything CoDa-describable: closed, non-negative, finite carriers, time-series or static. Energy mixes, biogeochemistry, geochemical assemblages, microbiome ratios, expenditure shares, electoral compositions, fleet reliability, CMB photon power per multipole. Three IEEE-floor reference datasets in the repo (Backblaze D=4, Planck CMB D=4, SM neutrino D=3) confirm engine behavior across physically unrelated domains.

**Q:** Is this peer-reviewed?
**A:** Conference submission peer-reviewed by the CoDaWork organising committee. Flagship paper in the repo (`papers/flagship/`); manuscript in `CODA-Association/CODAwork2026/`.

**Q:** Where do I find everything?
**A:** Repo URL on this slide; UN-6 handout via the QR code at the back; `CONFERENCE_ATTENDEES.md` is the slide-by-slide follow-along; `TRUST_AND_VERIFICATION.md` for the seven-step verification protocol.

</td>
</tr>
</table>

---

## Slide 2 · The size view hides the work   ·   70 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Twenty-five years of German electricity. Stacked-area chart. Coal and lignite recede. Nuclear phases out. Gas holds. Solar and wind grow steadily. Wind passes coal in the late twenty-tens.

That is the headline view. Here is what it hides.

**Germany Solar, 2005 → 2006.** Starting share, zero-point-two-one percent. Structural Power Share, seventy-one-point-one percent. Activation Coefficient, approximately three-hundred-thirty-three times.

Solar acted at three-hundred-thirty-three times its size — four years before the share view calls solar visible. No size view shows that. No size view ever could.

This talk is the reason that number exists. The mathematics is standard compositional data analysis — Aitchison geometry, CLR, ILR. The application — monitoring the simplex for structural work — may be new.

</td>
<td>

**Q:** What dataset?
**A:** EMBER electricity, public CC BY 4.0. Country-level annual generation by carrier 2000–2025. Hash-chained to the source CSV; reproducible byte-for-byte.

**Q:** Why Germany Solar 2005–2006 specifically?
**A:** First step where Solar's Power Share crosses 70% in the German grid — first year structural work concentrates in solar. Four years before its size-view share crosses the ~1% threshold conventionally called "visible".

**Q:** How was 71.1% computed?
**A:** Squared CLR motion of Solar at the 2005→2006 step, divided by the sum of squared CLR motions across all carriers at that step. The diagnostic — definition in §4.

**Q:** Isn't 333× just sensitive to a tiny denominator?
**A:** Yes, by construction. That sensitivity *is* the diagnostic — the work-to-size ratio. The framework names when a small carrier is structurally large.

**Q:** Could this be measurement noise?
**A:** No — 0.21% is recorded share, not estimate. CLR motion is mathematically defined and reproducible byte-identically (see `TRUST_AND_VERIFICATION.md`).

**Q:** What if starting share is zero?
**A:** Standard Aitchison-1986 replacement handles it; the framework declines to compute α when share is mathematically zero, and flags the step.

</td>
</tr>
</table>

---

## Slide 3 · Five viewpoints, one observable stack   ·   55 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Five viewpoints. Each answers one question. Together they form one observable stack.

**Composition** — size view. **Helmsman** — which carrier did the largest CLR move at a step. **Helmsman trajectory** — when steering changes. **Power Share** — how much squared CLR motion each carrier did. **Activation Coefficient** — Power Share divided by starting share. The yeast factor.

All five derive from CLR plus Helmert-ILR. Standard geometry, no new mathematics. The new framing is the stack.

</td>
<td>

**Q:** Why exactly five?
**A:** Each answers a distinct question that the others don't. Drop any one and you lose a question. Drop all five and you have a stacked-area chart.

**Q:** How is this different from PCA / SVD?
**A:** Not dimensionality reduction. Each viewpoint is interpretable per-carrier per-step. The stack is diagnostic, not compressive.

**Q:** Why ILR-Helmert specifically?
**A:** Orthonormal basis with no preferred carrier; rotation-invariant. Standard CoDa basis since Egozcue et al. 2003.

**Q:** Is this in the manuscript?
**A:** Yes — Appendix A equations 1–8 + Supplementary Information §S2 has the full formula tables.

**Q:** Why these five and not seven?
**A:** Tested with extensions; each addition either duplicates an existing viewpoint or reads as derivable. Five is the minimum spanning set.

</td>
</tr>
</table>

---

## Slide 4 · The Activation Coefficient   ·   65 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Alpha-sub-i of t equals Power Share over starting share. That ratio is the diagnostic.

When alpha is near 1, the carrier does work proportional to its size. Ordinary. When alpha is much greater than 1 — hidden driver. The carrier acts above its size. When alpha is less than 1 — coasting.

Worked example. Germany Solar, 2005 → 2006. Starting share zero-point-two-one percent — small. Power Share seventy-one-point-one percent — most of the work. Alpha approximately three-hundred-thirty-three.

Yeast is two percent of a loaf by mass and does one hundred percent of the rising. Same mathematical shape. The Energiewende's structural beginning — named four years before solar appears in the share view.

</td>
<td>

**Q:** Is this just elasticity?
**A:** No — elasticity is response to price. Activation Coefficient is structural work over share — different math, different domain. Compositional, not behavioural.

**Q:** Why call it yeast factor?
**A:** Pedagogical metaphor. α = (work done) / (mass present). Yeast: 2 % of a loaf's mass, 100 % of the rising. Same shape; useful for the room.

**Q:** Doesn't this just exaggerate small carriers?
**A:** Yes, *by design*. The diagnostic IS the work-to-size ratio. A small carrier with small work has α ≈ 1, ordinary; the framework only flags when the ratio is large.

**Q:** Threshold for "much greater than 1"?
**A:** No hard threshold by default. Distribution is heavy-tailed; the framework reports α directly and lets domain expertise interpret. Diagnostic, not classifier.

**Q:** What does "structural beginning" mean for Germany Solar 2005-06?
**A:** Solar's Power Share crosses 70% — first year structural work concentrates in one carrier. Four years before its share-view share crosses ~1% (≈2009). The structure precedes the visibility.

**Q:** Does this generalise beyond Germany Solar?
**A:** Yes. Slides 8-9 (Japan post-Fukushima reorganisation, multiple yeast moments across carriers) and slides 10-11 (UK coal exit absorbed across wind/solar/biomass) show the same shape in different transition regimes.

</td>
</tr>
</table>

---

## Slide 5 · Three archetypes — one instrument, three regimes   ·   35 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Three case studies. Three different transition regimes.

Germany — deliberate transition, continuous arc. Japan — external shock, loop and reorganise. UK — regime change, jump and return.

One instrument reads all three.

*Each country gets a pair of slides next: the share-and-work view, then the navigation chart on its own.*

</td>
<td>

**Q:** Why these three countries?
**A:** Three textbook cases of three distinct transition regimes. Representative, not selective — see slide 12 for the corpus-level result on 9 countries.

**Q:** Did you cherry-pick to fit a story?
**A:** No. Protocol fixed before dispositions were known; the same five-viewpoint stack applied to all nine countries (slide 12). Pre-registered.

**Q:** What about [my country]?
**A:** EMBER covers ~80 nations; the framework extends. These nine are the high-information national-grid trajectories I worked with first.

</td>
</tr>
</table>

---

## Slide 6 · Germany — share-and-work view   ·   70 sec   *(case study 1, beat 1)*

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

The Energiewende. Twenty-five years of deliberate composition change.

The size view tells you what you already know. Coal recedes. Gas holds. Solar and wind grow steadily. That is the headline.

The Power Share view tells you something the size view doesn't.

**Solar 2005 → 2006.** Share, 0.21 percent. Structural work, 71.1 percent. Activation Coefficient, approximately 333×.

Three years before the size view calls solar visible, the instrument names solar as the structural beginning of the Energiewende. The transition started in the data before it appeared on the chart.

This is the textbook case of a deliberate transition. The size view confirms what we know. The Power Share view tells us *when it actually started.*

*Pause — flip to the navigation chart.*

</td>
<td>

**Q:** Why is Solar 2005–2006 the inflection?
**A:** First step where Solar's Power Share crosses 70 % — first year structural work concentrates in one carrier. Three years before its size-view share crosses the 1 % threshold.

**Q:** "Three years before visible" — what's "visible"?
**A:** Standard size-view convention: a carrier becomes "visible" when its share exceeds ~1 %. Solar crosses 1 % around 2009 in the German grid; the structural signal precedes by ~3 years.

**Q:** Is this just renewable subsidy timing?
**A:** The diagnostic doesn't read policy — only composition. It tells you *when* the composition started changing. *Why* requires domain knowledge.

**Q:** How does this compare to the energy-transition literature?
**A:** Hˢ catches the structural-work signal earlier than the size-view signal those papers traditionally use. Complementary, not conflicting.

**Q:** Why call this deliberate?
**A:** The Helmsman trajectory (next slide) shows a smooth monotone arc — no loops, no flips. The geometry of a planned course.

</td>
</tr>
</table>

---

## Slide 7 · Germany — course on the simplex   ·   50 sec   *(case study 1, beat 2)*

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

This is the Germany helmsman trajectory. Course directness 0.41 — a continuous arc toward the renewable vertex.

Thirteen helmsman flips across twenty-five years. Smooth, monotone reorientation — no loops, no backtracks. The simplex shows what deliberate transition looks like: a single sustained course, year after year, in one direction.

This is the geometry of policy intent. Next: what happens when policy doesn't get to choose.

</td>
<td>

**Q:** Course directness — what does 0.41 mean?
**A:** End-to-end Aitchison distance divided by total path length. 1.0 = straight line; lower = more meander. 0.41 means the composition travelled about 2.4× the end-to-end distance to get there.

**Q:** Why "Helmsman"?
**A:** The carrier with the largest CLR move at a step — the carrier "steering" the composition right now. Helmsman trajectory = the sequence of steering changes.

**Q:** What's the renewable vertex?
**A:** The simplex corner where renewables dominate. Geometrically opposite the coal/nuclear corner. The trajectory's direction names the strategic intent.

**Q:** 13 flips across 25 years — is that high or low?
**A:** Compare to Japan's 17 flips (next pair). Germany's flips are arc-smoothing; Japan's are loop-driven. Same count regime, distinct geometric signature.

**Q:** Can I see this live?
**A:** Yes — projector during Q&A. Click DEU then BARY.

</td>
</tr>
</table>

---

## Slide 8 · Japan — share-and-work view   ·   70 sec   *(case study 2, beat 1)*

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Fukushima 2011. The shock appears in every viewpoint simultaneously.

Composition — nuclear collapses. Helmsman — seventeen flips across twenty-five years, the loudest count in the corpus. Power Share — massive concentration of squared CLR motion at one step. Aitchison distance 2011 → 2012, approximately three times the neighbouring-year baseline.

But the years *after* the shock tell the deeper story.

Japan's post-Fukushima mix kept reorganising for more than a decade. The yeast moments distribute across multiple carriers — solar, gas, wind, renewables, each taking turns absorbing the displaced nuclear share. Wind 2004 → 2005, alpha 188. Nuclear 2015 → 2016, alpha 187. Solar 2005 → 2006, alpha 176. The list goes on for years.

The instrument detects both the shock *and* the multi-year reorganisation that followed.

*Pause — flip to the navigation chart.*

</td>
<td>

**Q:** Could the framework predict Fukushima?
**A:** No — the instrument detects, it doesn't predict. What it adds is the multi-year *reorganisation* signature that traditional analyses miss.

**Q:** Why 3× baseline distance?
**A:** Aitchison distance per step; baseline = median year-to-year step across Japan's 25-year trajectory. The 2011→2012 step is an outlier by a factor of three.

**Q:** "Loudest count in the corpus" — meaning?
**A:** 17 helmsman flips in 25 years is more than any other country in the 9-nation corpus. The diagnostic for "unplanned reorganisation".

**Q:** How long is "post-Fukushima"?
**A:** Yeast-moment density stays high through ~2018-2020 in the data, then a slow steady state. About 7–9 years of reorganisation.

**Q:** Why list multiple yeast moments?
**A:** To show the displaced share didn't go to one substitute — it spread across solar, gas, wind, renewables, each in turn. The structure of multi-carrier absorption.

**Q:** Why isn't nuclear the helmsman every year post-2011?
**A:** Helmsman is the carrier *moving most* at that step, not the carrier in crisis. Once nuclear stabilises low, the steering passes to whichever renewable is absorbing the displaced load that year.

</td>
</tr>
</table>

---

## Slide 9 · Japan — course on the simplex   ·   50 sec   *(case study 2, beat 2)*

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

This is the Japan helmsman trajectory. Course directness 0.09 — the loop-and-reorganise archetype.

Compare it directly to Germany's smooth arc. Japan's course revisits and reroutes. The system has to *find* a new composition rather than walk a planned course; the trajectory shows the search.

That is what an unplanned reorganisation looks like on the simplex. Not a direction — a basin being explored.

</td>
<td>

**Q:** 0.09 — very low. What does that mean physically?
**A:** Trajectory loops back on itself ~11× the end-to-end displacement. The system explores many compositional states before settling.

**Q:** Is this dynamical-systems language?
**A:** Yes — corresponds to basin-search dynamics rather than limit-cycle or fixed-point. Same family of mathematics; the framework's regime taxonomy is topological-invariant per the Helmsman family.

**Q:** Could random noise produce this signature?
**A:** No — see the supplementary null-model analysis. A loop signature this strong requires correlated structural perturbation across multiple carriers over multiple years.

**Q:** What's the "basin"?
**A:** Region of the simplex Japan's composition can occupy given grid constraints (no-coal-spike, capacity limits). The basin is wide; the search through it took a decade.

**Q:** Will Japan ever stabilise?
**A:** Tail behaviour in 2019–2025 suggests a quieter trajectory — the basin search may be converging. Insufficient data to confirm.

</td>
</tr>
</table>

---

## Slide 10 · United Kingdom — share-and-work view   ·   70 sec   *(case study 3, beat 1)*

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Coal exit as regime change. Between 2012 and 2020, coal goes from more than 30 percent of UK electricity to less than 2 percent.

That is a true regime change, not a drift. The size view shows the headline cleanly.

The Power Share view tells us *how the displaced structural work was absorbed.*

Wind. Solar. Other renewables. Each took portions of the displaced load. There was no single replacement carrier.

The Activation Coefficient surfaces multiple yeast moments across the exit period — wind 2004 → 2005, biomass and other renewables in the mid-2010s, solar throughout. The instrument names them all.

The protocol separates **size decline** from **who absorbed the structural work.** A regression on raw shares would not show that separation.

*Pause — flip to the navigation chart.*

</td>
<td>

**Q:** "Regime change" — what makes it distinct from drift?
**A:** Aitchison-distance step magnitude plus topological signature in the Helmsman trajectory. Coal exits the helmsman role abruptly, not gradually. Quantitatively visible on slide 11.

**Q:** Was the displacement evenly distributed?
**A:** No — wind led, but biomass and solar also took meaningful shares. The instrument names *who* absorbed work at each year. Not a single substitution.

**Q:** Was this policy-driven?
**A:** Mix of UK Climate Change Act + carbon pricing + market dynamics. The instrument reads composition; the policy interpretation is downstream of what it shows.

**Q:** 30 % to less than 2 % in 8 years — typical for transitions?
**A:** Very fast. Comparable to nuclear retirement programs. The UK coal exit is one of the most rapid grid-carrier transitions in the post-WW2 era.

**Q:** Why no single replacement carrier?
**A:** UK grid mix and renewables availability — the displaced load fit into multiple carriers depending on time-of-day and seasonal patterns. The instrument captures this naturally; raw shares would not.

</td>
</tr>
</table>

---

## Slide 11 · United Kingdom — course on the simplex   ·   50 sec   *(case study 3, beat 2)*

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

This is the UK helmsman trajectory. Course directness 0.36 — the jump-and-return archetype.

The course leaves the coal vertex sharply, then settles toward a new mix. Regime change reads as one decisive displacement followed by re-stabilisation. Distinct from Germany's continuous arc, distinct from Japan's looping search.

Three transitions. Three archetypes. One geometry that names them all.

</td>
<td>

**Q:** 0.36 vs Germany 0.41 vs Japan 0.09 — is the UK "in between"?
**A:** Quantitatively yes; geometrically distinct. UK has a sharp displacement *then* re-stabilises — the topological signature is different from both Germany's smooth arc and Japan's exploratory loops.

**Q:** Only three archetypes?
**A:** No — three illustrative. The framework also recognises drift, oscillation, fixed-point, periodic, and chaotic regimes (Helmsman family taxonomy). Three is what fits a 13-slide talk.

**Q:** Quantitative threshold for "jump-and-return"?
**A:** Sharp Aitchison-step spike followed by return-to-within-2×-baseline of pre-jump position. Operationalised in the Helmsman family classifier.

**Q:** Does the new mix represent a stable attractor?
**A:** Trajectory tail through 2024–2025 suggests yes. Whether it persists requires more years of data.

</td>
</tr>
</table>

---

## Slide 12 · Cross-country signature — 5 of 9 reproduce the pattern   ·   80 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

From three case archetypes to a corpus-level result.

We applied the same protocol — same engine, same definition of deceptive drift — to all nine EMBER countries.

The signature fires in five of nine. **Australia, China, United Kingdom, India, Japan.**

The signature does *not* fire in Germany at annual grain, France, USA, or the World aggregate.

This matters. A useful detector should not fire everywhere. Discrimination is itself evidence the protocol is reading real structure, not artifact.

China and India top the helmsman-flips count — small carriers absorbing structural work over and over. USA, France, World aggregate top the peak Activation Coefficient — solar 2010 through 2015 acting at 500 to 760 times its size.

Same instrument. Nine countries. Five fire. Four stay quiet.

</td>
<td>

**Q:** Why these nine countries?
**A:** Pre-selected for grid-level diversity (size, carrier mix, geography). EMBER public data, hash-chained provenance. Selection fixed before disposition results.

**Q:** Could you have picked countries to fit?
**A:** No — protocol pre-registered, dispositions discovered. Five-of-nine is the result; if 9-of-9 fired the framework would be undiscriminating, if 0-of-9 fired it would be inert.

**Q:** What about [country X]?
**A:** EMBER covers ~80 nations; the framework extends. Selection here is illustrative of grid diversity, not exhaustive of global energy transitions.

**Q:** Why doesn't it fire in Germany at annual grain?
**A:** Germany's trajectory is mostly monotone (slide 7's continuous arc); annual grain misses the moments-within-years. Sub-annual grain might fire — open question.

**Q:** USA quiet — but you opened with USA Solar 760×?
**A:** USA fires the *Activation Coefficient* viewpoint (peak α among the four "quiet" countries) but doesn't fire the *deceptive-drift composite signature*. Both are correct — the stack is multi-viewpoint.

**Q:** Why does the World aggregate stay quiet?
**A:** Large-N smooths fluctuations; sub-population structure averages out. Aggregate composition is more stable than any constituent.

</td>
</tr>
</table>

---

## Slide 13 · What the stack answers — closing synthesis   ·   65 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

One observable. Five distinct questions.

**WHAT** carriers are big — the size view.
**WHO** is at the wheel — the helmsman.
**WHEN** the steering changes — the helmsman trajectory.
**HOW MUCH** work each carrier did — Power Share.
**WHY** a small carrier mattered — Activation Coefficient.

The stack does not replace interpretation. It gives interpretation a reproducible object.

The repo carries the engine, the manuscript, the handout in six languages, and a structured adoption test for the community.

Before questions — one minute on the live instrument.

</td>
<td>

**Q:** What's next?
**A:** Post-conference roadmap (in repo): H₁ generalization ladder to stochastic and chaotic budgets; entanglement structures; attractor diagnostics; frontier-audience outreach. Eight investigations queued for promotion post 2026-06-06.

**Q:** Code availability?
**A:** Apache-2.0 code + CC BY 4.0 docs. Every algorithm in four forms: Python + R + pseudocode + HUF-STD-002 spec. Three IEEE-floor confirmation datasets (Backblaze, Planck CMB, SM neutrino) verified byte-identically.

**Q:** How do I run it on my data?
**A:** `ai-refresh/CCTT_RUNBOOK.md` — 7-phase reproducible runbook, human or AI-assisted mode. Pseudocode at `HCI-CNT/engine/CNT_PSEUDOCODE.md`. Anti-spec at `HCI-CNT/engine/ANTI_SPECIFICATION.md`.

**Q:** Can I collaborate / cite?
**A:** Yes. CITATION.cff in the repo. Open issues welcome. Non-contact discipline = expect either no reply or a substantive one; no follow-up.

**Q:** Is this only for energy?
**A:** No — energy is the first non-acoustic application. Framework operates on any compositional time-series. Backblaze fleet reliability + Planck CMB + Standard Model neutrino mixing are validated in dimensions 4, 4, 3.

</td>
</tr>
</table>

---

## HTML projector — live introduction   ·   60 sec   *(after slide 13, before Q&A)*

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

*Bring up `codawork2026_projector.html` full-screen.*

Everything you just saw on static slides is live here. This is the same engine output, running in the browser — no server, no dependencies, one HTML file.

Three modes. **RADAR** — the composition as a star plot, one spoke per carrier. **BARY** — the trajectory on the simplex, the course we walked through for Germany, Japan, and the UK. **ALIGN** — the helmsman view, which carrier is steering.

*Click DEU → BARY.* Germany's continuous arc — the deliberate transition. *Click JPN → BARY.* Japan's loop — the post-Fukushima search. Same instrument, two regimes, side by side.

And the **SHOCK** overlay: the year markers flip to their chromatic-opposite colour on the shock years — Fukushima lights up without touching the trajectory's own colours.

It runs on any country in the corpus, on your data when you point it at a CoDa series. The slide deck behind me also carries the engine plates for the *other* six countries as an appendix — the ones we didn't walk through — so we can look at the whole corpus, not just the three case studies.

Now — questions. Pause me anywhere.

</td>
<td>

**Q:** Is the projector online / can I get it?
**A:** Single self-contained HTML file in the repo (`CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html`). No server, no build step — open it in any browser. Apache-2.0.

**Q:** Does it run on my data?
**A:** Yes — it reads the same canonical JSON the engine emits. Point CNT/CNQ at your CoDa series, load the output, the three modes work unchanged.

**Q:** What are the three modes again?
**A:** RADAR (per-carrier star plot of the composition), BARY (trajectory on the simplex — the course), ALIGN (helmsman / steering view). SHOCK is an overlay, not a mode — it recolours year markers on shock years.

**Q:** Why chromatic-opposite for SHOCK instead of red?
**A:** Channel discipline — the trajectory line already owns carrier-identity colour and base line-width. Lighting the band red fought those. The year-label colour was a free channel; flipping it to the RGB complement gives high contrast on any palette without disturbing the line. (Same single-channel-per-job principle as the BTL constant-power crossover.)

**Q:** Can you show [my country]?
**A:** If it's in the 9-country corpus, yes — click the country code then BARY. Otherwise it runs the moment you feed it that country's engine JSON.

**Q:** Slides vs projector — which is canonical?
**A:** Same engine output. The slides are the still frames; the projector is the live one. The appended data plates (deck slides 14–28) are the full-resolution stills for the six corpus countries beyond the three case studies.

</td>
</tr>
</table>

---

## General Q&A bench — non-slide-specific questions

These come up across the talk; pull from this set when the question doesn't tie to a specific slide.

<table>
<tr><th width="50%">Question</th><th width="50%">Ready response</th></tr>
<tr>
<td>**MC-4 (falsifiability) — *what's the claim, what defeats it?***</td>
<td>The claim is in the manuscript. Three conjuncts: Aitchison-native compositional metrics + formal change-point detection + carrier-level structural-work attribution. Four defeat paths: prior-art, metric, case, category. Any one of the four narrows or kills the claim. Please find one if you can; that's how the work improves.</td>
</tr>
<tr>
<td>**Why isn't this already standard CoDa?**</td>
<td>The mathematics is standard. The CoDa community has had the geometry since Aitchison 1986. What I added is the time-series operational layer — walk the geometry forward, ask which carrier did the work at each step, name the diagnostic. That layer is the contribution.</td>
</tr>
<tr>
<td>**Why these five viewpoints specifically?**</td>
<td>Each one answers a distinct question that the others don't. Drop any one and you lose a question. Drop all five and you have a stacked-area chart.</td>
</tr>
<tr>
<td>**Why split each country across two slides?**</td>
<td>The navigation chart is the geometry the talk earns. At 2.6 inches wide on a shared slide, the back of the room can't read it. At 6.5 inches wide on its own slide, every seat sees the trajectory at the same time. The expansion is room physics, not new content.</td>
</tr>
<tr>
<td>**Where does Hˢ come from? What's BTL?**</td>
<td>Binaural Test Lab — sound-controlled acoustics laboratory I founded in Markham, Ontario; institutional deployments in Ottawa and Monaco. The framework generalised retroactively from BTL acoustic work — DADC (2024) → DADI → ADAC (2025) → H₁ operator (2026) → HUF → Hˢ. The 6.02 dB cabinet-edge diffraction budget was the first natural simplex constraint in the lineage. Full chain at `HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`.</td>
</tr>
<tr>
<td>**How is reproducibility verified?**</td>
<td>Trust by independent reproduction. Every algorithm in four forms: Python + R + pseudocode + formal HUF-STD-002 specification. A skeptical user re-implements from the pseudocode in any language and verifies per-field at IEEE-floor tolerance on the three confirmation datasets. Byte-identical hash match if the canonicalization profile is adopted. See `TRUST_AND_VERIFICATION.md` §1.5 for the four-layer parity contract.</td>
</tr>
<tr>
<td>**AI use — what did you use AI for?**</td>
<td>HUF AI Collective protocol per HUF-STD-001 v1.1. Claude, ChatGPT, Grok used for drafting, mathematical content review, cross-check, code sweeps. I retain full scientific responsibility — author byline is human-only. AI Use Declaration on the synthesis slide (slide 13 footer) and on the manuscript cover.</td>
</tr>
<tr>
<td>**Is there a manifold underneath all this?**</td>
<td>Yes — a layered one. Underlying object is smooth (open simplex with Aitchison Riemannian structure; CNQ phase space S³ ≅ SU(2)). Discrete sampling and HTML rendering are piecewise-linear. Regime taxonomy is topological-invariant. Operator-level statements are synthetic-compatible. The working note `papers/in_progress/MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md` lays out the four-category layering.</td>
</tr>
<tr>
<td>**Is this gauge theory?**</td>
<td>Substantial gauge-theoretic structure is already present, named in pieces. Closure (Σpᵢ = 1) is a Ward identity; CLR is the gauge fixing of the ℝ₊ rescaling symmetry; CNQ's S³ ≅ SU(2) is the simplest non-abelian gauge group; closure-failure flag is an anomaly indicator. Consolidated reading in `papers/in_progress/GAUGE_THEORY_AND_Hs.md`.</td>
</tr>
<tr>
<td>**Why "compositional monitoring" rather than "energy analytics"?**</td>
<td>The framework is domain-neutral — it monitors compositional structure wherever it appears. Energy is the first non-acoustic application; the talk's title reflects what the framework *is*, not which dataset shows it off.</td>
</tr>
<tr>
<td>**Skepticism about reproducibility on GitHub generally?**</td>
<td>Trust must be earned, not expected. The framework's response: open code (Apache-2.0), open docs (CC BY 4.0), four forms of every algorithm, three IEEE-floor reference inputs with published hashes, language-agnostic pseudocode for independent re-implementation, anti-specification catalogues for failure modes. `TRUST_AND_VERIFICATION.md` is the 7-step verification protocol. The discipline expects audit, not belief.</td>
</tr>
<tr>
<td>**If the question is hostile or sweeping…**</td>
<td>Don't defend the framework. Defend the measurement. "The instrument reads. The expert decides. The hashes carry the receipts. If you have a specific case where you think the diagnostic mis-fires, I'd like to see it — that's how the work improves." Then move on.</td>
</tr>
<tr>
<td>**Time-running-out handoff.**</td>
<td>"The deck behind me carries data and trajectory plates for the rest of the corpus — the six countries we didn't walk through. Flip through them any time. The handout has the contact and repo on it. Thank you."</td>
</tr>
</table>

---

## Voice and posture reminders

| Setting | Action |
|---|---|
| **Opening** | No preamble. Walk on, open with "Good morning. *Title.* The question is X." |
| **Sentence length** | Periods, not commas. Short sentences land; long sentences scatter attention. |
| **Numbers** | Numbers first, qualifier after. "0.107 percent — small" beats "small — about 0.107 percent". |
| **Country pairs (slides 6–11)** | Slow there. The cases pay off. On the navigation slides (7, 9, 11), let the chart breathe — about 50 seconds each, unhurried. |
| **Cross-country slide (12)** | Don't summarise the cases. The result speaks for itself. |
| **Close (slide 13)** | End on *"It gives interpretation a reproducible object"* — let it sit. Then the one-line handoff to the live projector beat. |
| **Hostile question** | Defend the measurement, not the framework. Invite the specific case. Move on. |
| **Question that lands on a deep technical track** | Offer a specific repo file by name; offer a one-on-one after the session. Don't try to answer the full depth in 30 seconds. |

---

## Apparatus during Q&A

- **In-deck data appendix** (slides 14–28 of the single presentation file) — the engine plates for the **six countries beyond the three case studies**, already loaded in the same PowerPoint, so the appendix adds corpus breadth instead of repeating the talk. No file switching. Navigation: appendix divider (14) → **Signature fires** divider 15 → **Australia** 16–17, **China** 18–19, **India** 20–21 → **Signature quiet** divider 22 → **France** 23–24, **United States** 25–26, **World** 27–28. Two views per country: the data plate (input + headline metrics + hashes) then the full-trajectory course plot on the simplex. This is the direct visual backing for slide 12 ("5 of 9 fire"). Jump straight to the country the question lands on.
- **Projector** (`codawork2026_projector.html`) — three modes RADAR / BARY / ALIGN + SHOCK overlay. For "show me a specific country" questions, click JPN → BARY → SHOCK is the canonical sequence (Japan post-Fukushima loop; shock years flip the year-label colour to its chromatic opposite).
- **Full corpus** — the 66-slide, 325-page master PremierDataOutput (all nine countries) remains in `data_outputs/` if a question reaches beyond the three case studies; not needed in the room, but available.
- **Handout** in 6 UN languages — the QR code on the back leads to all of them. If a non-English-speaking attendee approaches, offer the language-appropriate handout.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*Five days to Coimbra. Walk to the lectern.*
