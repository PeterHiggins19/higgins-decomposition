---
title: "Speaking Script + Q&A Bench — 21-slide grayscale talk"
subtitle: "CoDaWork 2026 · Coimbra, Portugal · 1–5 June 2026"
author: "Peter Higgins · Rogue Wave Audio / Binaural Test Lab"
date: "2026-05-27"
---

# Speaking Script + Q&A Bench — 21-slide grayscale talk

**Deck:** `CodaWork2026_Presentation_2026-05-28.pdf` — single grayscale PDF, **16:9 widescreen** (13.333 × 7.5 in, exact 1.778 aspect — maps edge-to-edge onto modern projector / monitor displays with no letterboxing), **21 slides**, every slide numbered N / 21. PDF-only as of 2026-05-28 (no PPTX); the nav-chart / plate / cross-country slides use a two-column layout (chart on left + side reading panel on right) to fully use the canvas width without black bars.

**Narrative (clinical order):** standard CoDa → how we add **time** to the simplex (the five named readings) → three highlighted countries (Germany carried in full — the complete plate set) → **the rest of the world** (the other six) → the live instrument closes the show.

**Timing:** ~14 min spoken across 21 slides (Germany carried in full; the rest-of-world finale a brisk sweep) · +~1 min live close (**30 sec CN-TT Output PDF flash-through** of the Stage 1 plates, movie-like, + **30 sec live HTML projector**) = **~15 min** · then **5 min Q&A**.

**How to read this page:** left column is what you say (read from this). Right column is the Q&A bench — likely questions with ready responses. Glance right only if a question lands.

**Voice notes:** No preamble. Periods, not commas. Numbers first, qualifier after. Slow on the three case studies (slides 6–13; Germany carries two extra complete-set plates, 8–9). The rest-of-world finale (15–20) is a sweep — one breath per country, do not dwell. End on slide 21, then **flash through the CN-TT Output PDF** (Stage 1 plates, ~1 sec/page, raw-data provenance moving like film) for 30 sec, and **open the projector** for the final 30 sec.

---

## Slide 1 · Title — standard CoDa, and we add time   ·   40 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Good morning. *Compositional monitoring of energy-mix drift on the simplex.*

The question: **which carrier did the structural work?** Not which one got bigger — which one moved the composition.

This is standard compositional data analysis. The one new move is what happens when we add time to the simplex.

Follow along on the repository — the deck, the manuscript, and the live projector are all open. Every view here is reproducible on your data.

</td>
<td>

**Q:** Who are you / what's BTL?
**A:** Audio/electronics engineer; founder of the Binaural Test Lab at Rogue Wave Audio, Markham, Ontario. Hˢ generalised retroactively from acoustic compositional work.

**Q:** How long is the talk?
**A:** ~14 minutes across 21 slides, then ~1 minute live close (30 sec CN-TT Output PDF flash-through of the Stage 1 plates + 30 sec HTML projector) — about 15 minutes total — then 5 minutes of Q&A.

**Q:** "Any compositional dataset" — what's included?
**A:** Anything CoDa-describable: closed, non-negative, finite carriers, static or time-series. Energy mixes, biogeochemistry, microbiome ratios, expenditure shares, CMB photon power per multipole. Three IEEE-floor reference datasets in the repo confirm engine behaviour across unrelated domains.

**Q:** Why is the deck grayscale?
**A:** High-contrast at a distance and low-cost to reproduce. The structure carries the meaning; colour was doing no work the labels don't already do.


**Terms used:** *CoDa · simplex · Hˢ (Higgins decomposition) · reproducible-on-your-data*
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

Solar acted at three-hundred-thirty-three times its size — four years before the share view calls solar visible. No size view shows that.

This talk is the reason that number exists. The mathematics is standard compositional data analysis. The application — monitoring the simplex for structural work — may be new.

</td>
<td>

**Q:** What dataset?
**A:** EMBER electricity, public CC BY 4.0. Country-level annual generation by carrier 2000–2025. Hash-chained to the source CSV; reproducible.

**Q:** Why Germany Solar 2005–2006?
**A:** First step where Solar's Power Share crosses 70 % in the German grid — the first year structural work concentrates in solar, four years before its size-view share crosses ~1 %.

**Q:** Isn't 333× just a tiny denominator?
**A:** Yes, by construction. That sensitivity *is* the diagnostic — the work-to-size ratio. The framework names when a small carrier is structurally large.

**Q:** Could this be noise?
**A:** No — 0.21 % is recorded share, not estimate. CLR motion is mathematically defined and reproducible byte-identically.


**Terms used:** *deceptive drift · CLR (Centred Log-Ratio) · Power Share · Activation Coefficient (α) · structural work · squared compositional motion · stacked-area*
</td>
</tr>
</table>

---

## Slide 3 · Reading time on the simplex — the five named methods   ·   60 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Here is the whole method. Standard CoDa geometry — but we walk it forward, year by year. Five named readings.

**Composition** — what share each carrier has. **Helmsman** — which carrier makes the largest CLR move at a step. **Helmsman trajectory** — when the largest-motion carrier changes. **Power Share** — how much squared CLR motion each carrier did. **Activation Coefficient** — Power Share divided by starting share.

All five derive from CLR plus Helmert-ILR. Standard geometry — no new mathematics. The new move is reading it over time. That is the whole talk; the rest is showing it work.

</td>
<td>

**Q:** Why exactly five?
**A:** Each answers a distinct question the others don't. Drop one and you lose a question. Drop all five and you have a stacked-area chart.

**Q:** How is this different from PCA / SVD?
**A:** Not dimensionality reduction. Each reading is interpretable per-carrier per-step. Diagnostic, not compressive.

**Q:** Why ILR-Helmert?
**A:** Orthonormal basis with no preferred carrier; rotation-invariant. Standard CoDa basis since Egozcue et al. 2003.

**Q:** Is this in the manuscript?
**A:** Yes — Appendix A equations 1–8 + Supplementary §S2 has the full formula tables.


**Terms used:** *Closure · CLR · Helmert-orthonormal ILR · Aitchison-distance trajectory · Composition · Helmsman · Helmsman trajectory · Power Share · Activation Coefficient · observable stack · falsifiable*
</td>
</tr>
</table>

---

## Slide 4 · The Activation Coefficient   ·   60 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Alpha-sub-i of t equals Power Share over starting share. That ratio is the diagnostic.

Alpha near one — the carrier does work proportional to its size. Ordinary. Alpha much greater than one — hidden driver; the carrier acts above its size. Alpha less than one — coasting.

Worked example. Germany Solar, 2005 to 2006. Starting share zero-point-two-one percent — small. Power Share seventy-one-point-one percent — most of the work. Alpha approximately three-hundred-thirty-three.

Yeast is two percent of a loaf by mass and does one hundred percent of the rising. Same shape. That is the structural beginning of the Energiewende — named four years before solar appears in the share view.

</td>
<td>

**Q:** Is this just elasticity?
**A:** No — elasticity is response to price. Activation Coefficient is structural work over share. Compositional, not behavioural.

**Q:** Doesn't this just exaggerate small carriers?
**A:** By design. A small carrier doing small work has α ≈ 1, ordinary; the framework only flags when the work-to-size ratio is large.

**Q:** Threshold for "much greater than 1"?
**A:** No hard default. Distribution is heavy-tailed; the framework reports α directly and lets domain expertise interpret.

**Q:** Does it generalise beyond Germany Solar?
**A:** Yes — Japan (multiple high-Activation-Coefficient moments post-Fukushima) and the UK coal exit show the same shape in different regimes.


**Terms used:** *α_i(t) · Power Share_i(t) · starting share_i(t) · ordinary · hidden driver · coasting · yeast analogy*
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

Germany — deliberate transition, a continuous arc. Japan — external shock, loop and reorganise. United Kingdom — regime change, jump and return.

One instrument reads all three. Each country gets a pair of slides next: the share-and-work view, then its trajectory on the simplex.

</td>
<td>

**Q:** Why these three countries?
**A:** Three textbook cases of three distinct regimes. Representative, not selective — slide 12 gives the corpus-level result on all nine.

**Q:** Did you cherry-pick?
**A:** No. The protocol was fixed before dispositions were known; the same five-reading stack applied to all nine countries.


**Terms used:** *archetype · deliberate transition · external shock · regime change · continuous arc · loop and reorganise · jump and return · Energiewende · Fukushima · coal exit*
</td>
</tr>
</table>

---

## Slide 6 · Germany — share and structural work   ·   60 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

The Energiewende. Twenty-five years of deliberate composition change.

The size view tells you what you already know — coal recedes, gas holds, solar and wind grow. The Power Share view tells you something it doesn't.

**Solar 2005 → 2006.** Share 0.21 percent. Structural work 71.1 percent. Alpha approximately 333.

Three years before the size view calls solar visible, the instrument names solar as the structural beginning of the Energiewende. The transition started in the data before it appeared on the chart.

*Pause — flip to the trajectory.*

</td>
<td>

**Q:** Why is Solar 2005–2006 the inflection?
**A:** First step where Solar's Power Share crosses 70 % — structural work concentrates in one carrier, three years before its share crosses 1 %.

**Q:** Is this just subsidy timing?
**A:** The diagnostic reads composition, not policy. It tells you *when* the composition started changing; *why* is domain knowledge.

**Q:** Why call it deliberate?
**A:** The trajectory (next slide) is a smooth monotone arc — no loops, no flips. The geometry of a planned trajectory.


**Terms used:** *size view · stacked-area · Power Share · % squared CLR motion per step · structural work · Energiewende · α ≈ 333 ×*
</td>
</tr>
</table>

---

## Slide 7 · Germany — the trajectory   ·   40 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

The Germany Helmsman trajectory. Trajectory directness 0.41 — a continuous arc toward the renewable vertex.

Thirteen Helmsman flips across twenty-five years. Smooth, monotone reorientation — no loops, no backtracks. The simplex shows what a deliberate transition looks like: a single sustained trajectory, year after year, in one direction.

This is the geometry of policy intent. Because Germany is our worked exemplar, two more plates follow — the complete geometric set for one country — then the other regimes.

</td>
<td>

**Q:** Trajectory directness — what is 0.41?
**A:** End-to-end Aitchison distance ÷ total path length. 1.0 = straight line; lower = more meander. 0.41 ≈ the composition travelled ~2.4× the end-to-end distance.

**Q:** Why "Helmsman"?
**A:** The carrier with the largest CLR move at a step — the one in largest motion right now.

**Q:** Can I see this live?
**A:** Yes — projector at the close. Click DEU → BARY.


**Terms used:** *PCA · CLR trajectory projected by PCA · PC1 / PC2 · course directness (= net distance ÷ path length) · h_S (start) · h_F (final) · HLR (Higgins Log-Ratio) · V_net = h_F − h_S · dynamic range · Reading guide*
</td>
</tr>
</table>

---

## Slide 8 · Germany — orthogonal projections (the complete set)   ·   30 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Germany is our worked exemplar, so Germany alone gets the complete plate set — the full geometric view one country deserves.

This is the Section view: the CLR plan, the XZ bearings between carrier pairs, and the per-carrier CLR for a representative year. Everything the engine computes for a single year, on one plate.

</td>
<td>

**Q:** Why does only Germany get this?
**A:** One country shown in full proves the instrument's depth; the other eight would multiply the slide count for no new argument. Germany is the deliberate-transition exemplar, so it carries the complete set.

**Q:** What is the "Section view"?
**A:** The Stage-1 orthogonal projections — XY (CLR plan), XZ (bearings), YZ (per-carrier CLR) — for one representative year (2013 here), plus the metadata box (Hˢ, kappa, the Helmsman, the directness ratio).

**Q:** Where are the other countries' full plates?
**A:** The 325-page CN-TT Output (`CodaWork2026_CN-TT_Output_2026-05-28.pdf` — renamed 2026-05-28 from PremierDataOutput per HUF-STD-002; PPTX editing source kept at `CodaWork2026_PremierDataOutput_2026-05-13.pptx`) holds all 27 plates per country for all nine.


**Terms used:** *Section plate · t = 13 (Year 2013) · D = 9 carriers · N = 26 readings · pairs = 36 · Hˢ · Ring (= Hˢ − 2) · E_metric · κ_HS · ω (omega) · d_A (Aitchison) · Helm (Helmsman) · Helm d · DR (Dynamic Range) · DR ratio · XY plan · XZ bearings · YZ CLR · CLR plan view*
</td>
</tr>
</table>

---

## Slide 9 · Germany — ILR-Helmert triplet (the complete set)   ·   30 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

And the orthonormal companion: the ILR-Helmert triplet — three orthogonal scatter projections of Germany's twenty-five-year trajectory onto the first three Helmert ILR axes.

The same continuous arc you saw on the simplex, now in the orthonormal basis where the axes have no preferred carrier. That is the complete geometric set for one country.

Now the other two regimes, then the rest of the world.

</td>
<td>

**Q:** Why show the ILR triplet as well as the trajectory?
**A:** The trajectory (slide 7) is the PCA-projected path; the ILR triplet is the orthonormal-basis view with explicit carrier contrasts. Same data, two complementary geometries — completeness for the exemplar country.

**Q:** What do the ILR axes mean?
**A:** Helmert contrasts: ilr1 = Bioenergy vs Coal; ilr2 = (Bioenergy + Coal) vs Gas; ilr3 = (Bioenergy + Coal + Gas) vs Hydro. Orthonormal, rotation-invariant, no preferred carrier.


**Terms used:** *ILR-Helmert orthogonal triplet · ilr1 × ilr2 · ilr1 × ilr3 · ilr2 × ilr3 · Helmert basis loadings · orthonormal · Stage 1 Order-1 plate*
</td>
</tr>
</table>

---

## Slide 10 · Japan — share and structural work   ·   60 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Fukushima 2011. The shock appears in every reading at once.

Composition — nuclear collapses. Helmsman — seventeen flips across twenty-five years, the loudest count in the corpus. Power Share — a massive concentration of squared CLR motion at one step. Aitchison distance 2011 to 2012, about three times the neighbouring-year baseline.

But the years *after* the shock tell the deeper story. Japan's mix kept reorganising for more than a decade — solar, gas, wind, each taking turns absorbing the displaced nuclear share.

The instrument detects both the shock and the multi-year reorganisation that followed.

*Pause — flip to the trajectory.*

</td>
<td>

**Q:** Could the framework predict Fukushima?
**A:** No — it detects, it doesn't predict. What it adds is the multi-year *reorganisation* signature that traditional analyses miss.

**Q:** Why 3× baseline distance?
**A:** Aitchison distance per step; baseline = median year-to-year step. The 2011→2012 step is an outlier by ~3×.

**Q:** Why isn't nuclear the helmsman every year after 2011?
**A:** Helmsman is the carrier *moving most* at a step, not the one in crisis. Once nuclear stabilises low, the largest-motion role passes to whichever renewable absorbs the load that year.


**Terms used:** *size view · Power Share · Aitchison distance · baseline step · Fukushima 2011 · Helmsman flips (17 on the corpus)*
</td>
</tr>
</table>

---

## Slide 11 · Japan — the trajectory   ·   40 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

The Japan Helmsman trajectory. Trajectory directness 0.09 — the loop-and-reorganise pattern.

Compare it to Germany's smooth arc. Japan's trajectory revisits and reroutes. The system has to *find* a new composition rather than walk a planned one; the trajectory shows the search.

That is what an unplanned reorganisation looks like on the simplex. Not a direction — a basin being explored.

</td>
<td>

**Q:** 0.09 — what does that mean physically?
**A:** The trajectory loops back ~11× the end-to-end displacement. The system explores many states before settling.

**Q:** Is this dynamical-systems language?
**A:** Yes — basin-search dynamics rather than limit-cycle or fixed-point. The regime taxonomy is topological-invariant per the Helmsman family.

**Q:** Could noise produce this?
**A:** No — see the supplementary null-model. A loop this strong needs correlated perturbation across carriers over years.


**Terms used:** *PCA · Helmsman trajectory · looping reorganisation · course directness 0.0875 · PC1 / PC2*
</td>
</tr>
</table>

---

## Slide 12 · United Kingdom — share and structural work   ·   60 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

Coal exit as regime change. Between 2012 and 2020, coal goes from more than 30 percent of UK electricity to less than 2 percent.

A true regime change, not a drift. The size view shows the headline cleanly. The Power Share view tells us *how the displaced structural work was absorbed.*

Wind. Solar. Other renewables. Each took portions of the displaced load. There was no single replacement carrier.

The protocol separates size decline from who absorbed the structural work. A regression on raw shares would not show that separation.

*Pause — flip to the trajectory.*

</td>
<td>

**Q:** "Regime change" vs drift?
**A:** Aitchison-step magnitude plus the topological signature in the Helmsman trajectory. Coal exits the helmsman role abruptly. Visible on slide 11.

**Q:** Evenly distributed?
**A:** No — wind led, but biomass and solar took meaningful shares. The instrument names *who* absorbed work each year.

**Q:** Policy-driven?
**A:** UK Climate Change Act + carbon pricing + market dynamics. The instrument reads composition; policy is downstream of what it shows.


**Terms used:** *size view · Power Share · coal exit · regime change · displaced work*
</td>
</tr>
</table>

---

## Slide 13 · United Kingdom — the trajectory   ·   40 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

The UK Helmsman trajectory. Trajectory directness 0.36 — the jump-and-return pattern.

The trajectory leaves the coal vertex sharply, then settles toward a new mix. Regime change reads as one decisive displacement followed by re-stabilisation. Distinct from Germany's continuous arc, distinct from Japan's looping search.

Three transitions. Three archetypes. One geometry that names them all.

</td>
<td>

**Q:** 0.36 vs Germany 0.41 vs Japan 0.09 — is the UK "in between"?
**A:** Quantitatively yes; geometrically distinct. A sharp displacement *then* re-stabilisation — a different topological signature from both.

**Q:** Only three archetypes?
**A:** Three illustrative. The framework also recognises drift, oscillation, fixed-point, periodic, and chaotic regimes. Three is what fits a short talk.


**Terms used:** *PCA · Helmsman trajectory · jump-and-return · course directness 0.3613 · coal vertex*
</td>
</tr>
</table>

---

## Slide 14 · Across the corpus — deceptive drift in 5 of 9   ·   55 sec

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

From three case archetypes to a corpus-level result.

We applied the same protocol — same engine, same definition of deceptive drift — to all nine EMBER countries. Deceptive drift is present in five of nine; absent in four. Below: the two tables in slide-show order, top to bottom.

**PRESENT (5 of 9) — slide-show order**

<table class="inner">
<tr><th>#</th><th>Country</th><th>Why drift fires</th></tr>
<tr><td>10</td><td>JPN — Japan</td><td>Fukushima 2011 displaces nuclear; 17 Helmsman flips on the corpus; multi-year reorganisation</td></tr>
<tr><td>12</td><td>GBR — United Kingdom</td><td>Coal exit 2012–2020 (>30 % → <2 %); wind / solar / others absorb displaced work — many small carriers carrying large Power Share each</td></tr>
<tr><td>15</td><td>AUS — Australia</td><td>Solar growth from near-zero; deceptive-drift signature at small-share carriers across 2000–2025</td></tr>
<tr><td>16</td><td>CHN — China</td><td>Coal-era growth then a turn; small carriers tagged by yeast moments at multiple steps</td></tr>
<tr><td>17</td><td>IND — India</td><td>Solar 2010–2015 activation above proportionality — the third small-share case</td></tr>
</table>

**ABSENT (4 of 9) — slide-show order**

<table class="inner">
<tr><th>#</th><th>Country</th><th>Why drift is absent</th></tr>
<tr><td>6</td><td>DEU — Germany (annual)</td><td>Step view fires (Solar 2005–06: α ≈ 333 ×); annual aggregate dilutes the signal — sub-annual grain might still detect it</td></tr>
<tr><td>18</td><td>FRA — France</td><td>Nuclear-stable composition; no peak Activation Coefficient passes threshold</td></tr>
<tr><td>19</td><td>USA — United States</td><td>Large grid; many carriers averaging; no single carrier crosses α threshold at annual grain</td></tr>
<tr><td>20</td><td>WLD — World</td><td>Aggregate-of-aggregates trajectory; large-N smoothing dissolves what's present in constituents</td></tr>
</table>

A useful detector should not flag every system. Discrimination is itself evidence the protocol reads real structure, not artifact.

You have seen three. Here is the rest of the corpus.

</td>
<td>

**Q:** Why these nine?
**A:** Pre-selected for grid-level diversity. EMBER public data, hash-chained provenance. Selection fixed before disposition results.

**Q:** Could you have picked to fit?
**A:** No — protocol pre-registered, dispositions discovered. 9-of-9 would be undiscriminating; 0-of-9 inert. Five is the result.

**Q:** Why isn't deceptive drift detected in Germany at annual grain?
**A:** Its trajectory is mostly monotone (slide 7); annual grain misses moments-within-years. Sub-annual grain might detect it — open question.


**Terms used:** *yeast moments (count) · AC ≥ 3 × · Peak Activation Coefficient · leverage · Helmsman flips (total, 25 transitions) · top-10 activation moments · annual grain · step grain*
</td>
</tr>
</table>

---

## Slides 15–20 · The rest of the world — the other six   ·   ~2 min 15 sec total (one breath each)

*This is the finale: a brisk sweep across the six countries you did not walk through — three with deceptive drift present, three with it absent. Do not dwell. The one-line prompt on each slide is your cue; say it and move.*

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench (covers all six)</th></tr>
<tr>
<td>

**15 · Australia (deceptive drift present).** Same protocol, the rest of the world. Australia — the full trajectory; the deceptive-drift signature, structural work concentrated in the renewable turn.

**16 · China (deceptive drift present).** China — coal-era growth, then a turn. The flips pile up; small carriers absorb structural work over and over.

**17 · India (deceptive drift present).** India — the third case where it is present. The same concentration signature, a different grid.

**18 · France (absent).** Now the three with no deceptive drift. France — nuclear-stable across the whole window. The trajectory barely moves; the detector correctly stays silent.

**19 · United States (absent).** The United States — a large grid; no deceptive drift at annual grain. Real moments exist within years; the annual view averages them out.

**20 · World (absent).** And the world aggregate. Large-N smoothing hides the deceptive drift in its constituents — the corpus average is calmer than any country in it. *Notice the Helmsman: uniform across the study window — one largest-motion carrier holds from start to finish. The world as a whole is a smoothly-operating energy system over time; countries absorb the perturbations, the global composition does not flip.*

Nine countries. Five show deceptive drift, four do not. One instrument read them all. *Move to the close.*

</td>
<td>

**Q:** Why only the trajectory for these six, not the full plate set?
**A:** This is the breadth sweep — the trajectory is the one view that reads at a glance. The full engine plates (all 27 per country, plus Stage 2/3 and CNQ) are in the 325-page master output in the repo.

**Q:** Why does the World aggregate show none when its constituents do?
**A:** Large-N smooths fluctuations; sub-population structure averages out. The aggregate composition is more stable than any constituent — itself a finding.

**Q:** Australia/China/India — what makes deceptive drift present?
**A:** The deceptive-drift composite signature: a structural-work concentration the size view doesn't show, confirmed across the five readings. Per-country detail in the repo.

**Q:** Can you pull up any of these live?
**A:** Yes — the projector runs every country in the corpus. Click the country code → BARY at the close or in Q&A.

**Q:** Is the present/absent split robust to grain?
**A:** At annual grain, this is the split. Sub-annual grain is an open question flagged in the roadmap — France and the USA are the obvious re-tests.


**Terms used:** *System Course Plot · ember CSV · PC1 / PC2 loadings · top displacement events · COURSE METRICS panel · scale provenance · large-N smoothing · annual grain · sub-annual (open question)*
</td>
</tr>
</table>

---

## Slide 21 · What the stack answers — the live instrument closes   ·   45 sec spoken + 30 sec CN-TT PDF flash + 30 sec HTML projector

<table>
<tr><th width="60%">Speech (read this)</th><th width="40%">Q&A bench</th></tr>
<tr>
<td>

One observable. Five distinct questions.

**WHAT** carriers are big — the size view. **WHO** is in largest motion — the Helmsman. **WHEN** the largest-motion carrier changes — the Helmsman trajectory. **HOW MUCH** work each carrier did — Power Share. **WHY** a small carrier mattered — the Activation Coefficient.

The stack does not replace interpretation. It gives interpretation a reproducible object.

And everything you have seen has a record. *Open `CodaWork2026_CN-TT_Output_2026-05-28.pdf` and flash through the Stage 1 plates — one page per second.* The data points move on the simplex like frames of a film — the raw provenance of every claim in the talk, played at speed. This is the artifact a reviewer opens to verify any plate by hand. **(30 sec.)**

*Now open `codawork2026_projector.html`.* Same engine output, in the browser — one file, no server. Three modes: RADAR, the composition; BARY, the trajectory; ALIGN, the centred view. *Click DEU → BARY* — Germany's arc. *Click JPN → BARY* — Japan's loop. Same instrument, two regimes, side by side. It runs on any country here, and on your data when you point it at a CoDa series. **(30 sec.)**

Thank you. Questions.

</td>
<td>

**Q:** Is the projector online / can I get it?
**A:** Single self-contained HTML file in the repo (`CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html`). No server, no build step. Apache-2.0.

**Q:** What are the three modes?
**A:** RADAR (per-carrier star plot), BARY (trajectory on the simplex), ALIGN (the centred / barycenter-aligned shape view). SHOCK is an overlay that recolours year markers on shock years.

**Q:** Code availability?
**A:** Apache-2.0 code + CC BY 4.0 docs. Every algorithm in four forms: Python + R + pseudocode + HUF-STD-002 spec. Three IEEE-floor confirmation datasets verified.

**Q:** How do I run it on my data?
**A:** `ai-refresh/CCTT_RUNBOOK.md` — 7-phase reproducible runbook. Pseudocode at `HCI-CNT/engine/CNT_PSEUDOCODE.md`.

**Q:** Can I collaborate / cite?
**A:** Yes. CITATION.cff in the repo. Non-contact discipline: expect either no reply or a substantive one; no follow-up.


**Terms used:** *observable stack · falsifiable · live close · CN-TT Output (HUF-STD-002, CNT / Tensor Train) · codawork2026_projector · RADAR · BARY · ALIGN · SHOCK · HUF-STD-001 v1.1 · AI Use Declaration · Apache-2.0 · CC BY 4.0*
</td>
</tr>
</table>

---

## General Q&A bench — non-slide-specific questions

<table>
<tr><th width="50%">Question</th><th width="50%">Ready response</th></tr>
<tr>
<td>**MC-4 (falsifiability) — what's the claim, what defeats it?**</td>
<td>Three conjuncts: Aitchison-native compositional metrics + formal change-point detection + carrier-level structural-work attribution. Four defeat paths: prior-art, metric, case, category. Any one narrows or kills the claim. Please find one — that's how the work improves.</td>
</tr>
<tr>
<td>**Why isn't this already standard CoDa?**</td>
<td>The mathematics is standard since Aitchison 1986. What I added is the time-series operational layer — walk the geometry forward, ask which carrier did the work at each step, name the diagnostic. That layer is the contribution.</td>
</tr>
<tr>
<td>**Why grayscale?**</td>
<td>High contrast at a distance and cheap to reproduce. Structure carries the meaning here; the carrier labels do the work colour would. A scientific-paper aesthetic on purpose.</td>
</tr>
<tr>
<td>**Where does Hˢ come from? What's BTL?**</td>
<td>Binaural Test Lab — acoustics laboratory I founded in Markham, Ontario. The framework generalised retroactively from BTL acoustic work — DADC (2024) → DADI → ADAC (2025) → H₁ operator (2026) → HUF → Hˢ. The 6.02 dB cabinet-edge diffraction budget was the first natural simplex constraint.</td>
</tr>
<tr>
<td>**How is reproducibility verified?**</td>
<td>Trust by independent reproduction. Every algorithm in four forms: Python + R + pseudocode + HUF-STD-002 spec. Re-implement from the pseudocode, verify per-field at IEEE-floor tolerance on the three confirmation datasets. See `TRUST_AND_VERIFICATION.md`.</td>
</tr>
<tr>
<td>**AI use — what did you use AI for?**</td>
<td>HUF AI Collective protocol per HUF-STD-001 v1.1. Claude, ChatGPT, Grok for drafting, review, cross-check, code sweeps. Author byline is human-only; I retain full scientific responsibility. Declaration on slide 21.</td>
</tr>
<tr>
<td>**Is there a manifold underneath this?**</td>
<td>Yes — layered. Smooth underlying object (open simplex with Aitchison structure; CNQ phase space S³ ≅ SU(2)); discrete sampling and HTML rendering are piecewise-linear; regime taxonomy is topological-invariant. Working note `MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md`.</td>
</tr>
<tr>
<td>**Is this gauge theory?**</td>
<td>Substantial gauge-theoretic structure is present in pieces. Closure (Σpᵢ = 1) is a Ward identity; CLR is gauge fixing of the ℝ₊ rescaling symmetry; CNQ's S³ ≅ SU(2) is the simplest non-abelian gauge group. Consolidated in `papers/in_progress/GAUGE_THEORY_AND_Hs.md`.</td>
</tr>
<tr>
<td>**If the question is hostile or sweeping…**</td>
<td>Don't defend the framework. Defend the measurement. "The instrument reads. The expert decides. The hashes carry the receipts. If you have a specific case where the diagnostic mis-classifies, I'd like to see it." Then move on.</td>
</tr>
<tr>
<td>**Time-running-out handoff.**</td>
<td>"The projector is open — every country in the corpus, live. The handout has the contact and repo. Thank you."</td>
</tr>
</table>

---

## Voice and posture reminders

| Setting | Action |
|---|---|
| **Opening** | No preamble. Walk on, open with "Good morning. *Title.* The question is X." |
| **Sentence length** | Periods, not commas. Short sentences land. |
| **Numbers** | Numbers first, qualifier after. "0.21 percent — small" beats "small — about 0.21 percent". |
| **Case studies (6–13)** | Slow there. The cases pay off. On the trajectory slides (7, 11, 13) let the chart breathe — ~40 seconds. Germany's two complete-set plates (8–9) are quick — ~30 seconds each. |
| **Rest-of-world finale (15–20)** | A sweep, not six talks. One breath per country. Say the prompt and move. ~20 seconds each. |
| **Close (21)** | End on *"It gives interpretation a reproducible object,"* then **flash the CN-TT Output PDF** through the Stage 1 plates at ~