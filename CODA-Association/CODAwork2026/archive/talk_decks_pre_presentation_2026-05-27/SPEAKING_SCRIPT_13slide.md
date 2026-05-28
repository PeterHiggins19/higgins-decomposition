# Speaking script — 13-slide expanded talk

**Deck:** `CODA-Association/CODAwork2026/data_outputs/CodaWork2026_FinalTalk_13Slide_2026-05-24.pptx`
**Total target:** ~10 min talk + 1 min cinema scroll + 1 min projector = ~12 min spoken. Leaves ~3 min Q&A in a 15-minute slot.

Voice: direct, information-packed, no preamble. Each sentence carries a fact or a turn. Use periods, not commas. Numbers stay precise.

The country case-study **pairs** (slides 6+7 Germany, 8+9 Japan, 10+11 UK) are the heart of the talk — that is where the room sees the instrument do work on data they recognise *and* sees the trajectory chart at legible size on its own dedicated slide. The 10-slide compression worked, but the per-country navigation chart at 2.6″ wide was unreadable from the back of the room; the 13-slide expansion fixes that without changing the talk's substance.

---

## Slide 1 — Title + question + contact   ·   30 sec

Good morning. *Compositional monitoring of energy-mix drift on the simplex.*

The question of this talk: **which carrier did the structural work?** Not which one got bigger. Which one moved the composition.

Follow along on the repository — the slide deck, manuscript, and live projector are all open. The framework runs any compositional dataset the CoDa community can describe; what you'll see in the next nine minutes is reproducible on your data.

My email and the repo URL are on this slide. The one-page handout is in six UN languages. Let me begin.

---

## Slide 2 — The size view hides the work   ·   50 sec

Twenty-five years of German electricity. Stacked-area chart. Coal and lignite recede. Nuclear phases out. Gas holds. Solar and wind grow steadily. Wind passes coal in the late twenty-tens.

That is the headline view. Here is what it hides.

**Germany Solar, 2005 → 2006.** Starting share, zero-point-two-one percent. Structural Power Share, seventy-one-point-one percent. Activation Coefficient, approximately three-hundred-thirty-three times.

Solar acted at three-hundred-thirty-three times its size — four years before the share view calls solar visible. No size view shows that. No size view ever could.

This talk is the reason that number exists. The mathematics is standard compositional data analysis — Aitchison geometry, CLR, ILR. The application — monitoring the simplex for structural work — may be new.

---

## Slide 3 — Five viewpoints, one observable stack   ·   35 sec

Five viewpoints. Each answers one question. Together they form one observable stack.

**Composition** — size view. **Helmsman** — which carrier did the largest CLR move at a step. **Helmsman trajectory** — when steering changes. **Power Share** — how much squared CLR motion each carrier did. **Activation Coefficient** — Power Share divided by starting share. The yeast factor.

All five derive from CLR plus Helmert-ILR. Standard geometry, no new mathematics. The new framing is the stack.

---

## Slide 4 — The Activation Coefficient   ·   45 sec

Alpha-sub-i of t equals Power Share over starting share. That ratio is the diagnostic.

When alpha is near 1, the carrier does work proportional to its size. Ordinary. When alpha is much greater than 1 — hidden driver. The carrier acts above its size. When alpha is less than 1 — coasting.

Worked example. Germany Solar, 2005 → 2006. Starting share zero-point-two-one percent — small. Power Share seventy-one-point-one percent — most of the work. Alpha approximately three-hundred-thirty-three.

Yeast is two percent of a loaf by mass and does one hundred percent of the rising. Same mathematical shape. The Energiewende's structural beginning — named four years before solar appears in the share view.

---

## Slide 5 — Three archetypes   ·   20 sec

Three case studies. Three different transition regimes.

Germany — deliberate transition, continuous arc. Japan — external shock, loop and reorganise. UK — regime change, jump and return.

One instrument reads all three.

*Each country gets a pair of slides next: the share-and-work view, then the navigation chart on its own.*

---

## Slide 6 — Germany, share-and-work view   ·   55 sec   *(case study 1, beat 1)*

The Energiewende. Twenty-five years of deliberate composition change.

The size view tells you what you already know. Coal recedes. Gas holds. Solar and wind grow steadily. That is the headline.

The Power Share view tells you something the size view doesn't.

**Solar 2005 → 2006.** Share, 0.21 percent. Structural work, 71.1 percent. Activation Coefficient, approximately 333×.

Three years before the size view calls solar visible, the instrument names solar as the structural beginning of the Energiewende. The transition started in the data before it appeared on the chart.

This is the textbook case of a deliberate transition. The size view confirms what we know. The Power Share view tells us *when it actually started.*

*Pause — flip to the navigation chart.*

---

## Slide 7 — Germany, course on the simplex   ·   30 sec   *(case study 1, beat 2)*

This is the Germany helmsman trajectory. Course directness 0.41 — a continuous arc toward the renewable vertex.

Thirteen helmsman flips across twenty-five years. Smooth, monotone reorientation — no loops, no backtracks. The simplex shows what deliberate transition looks like: a single sustained course, year after year, in one direction.

This is the geometry of policy intent. Next: what happens when policy doesn't get to choose.

---

## Slide 8 — Japan, share-and-work view   ·   55 sec   *(case study 2, beat 1)*

Fukushima 2011. The shock appears in every viewpoint simultaneously.

Composition — nuclear collapses. Helmsman — seventeen flips across twenty-five years, the loudest count in the corpus. Power Share — massive concentration of squared CLR motion at one step. Aitchison distance 2011 → 2012, approximately three times the neighbouring-year baseline.

But the years *after* the shock tell the deeper story.

Japan's post-Fukushima mix kept reorganising for more than a decade. The yeast moments distribute across multiple carriers — solar, gas, wind, renewables, each taking turns absorbing the displaced nuclear share. Wind 2004 → 2005, alpha 188. Nuclear 2015 → 2016, alpha 187. Solar 2005 → 2006, alpha 176. The list goes on for years.

The instrument detects both the shock *and* the multi-year reorganisation that followed.

*Pause — flip to the navigation chart.*

---

## Slide 9 — Japan, course on the simplex   ·   30 sec   *(case study 2, beat 2)*

This is the Japan helmsman trajectory. Course directness 0.09 — the loop-and-reorganise archetype.

Compare it directly to Germany's smooth arc. Japan's course revisits and reroutes. The system has to *find* a new composition rather than walk a planned course; the trajectory shows the search.

That is what an unplanned reorganisation looks like on the simplex. Not a direction — a basin being explored.

---

## Slide 10 — United Kingdom, share-and-work view   ·   55 sec   *(case study 3, beat 1)*

Coal exit as regime change. Between 2012 and 2020, coal goes from more than 30 percent of UK electricity to less than 2 percent.

That is a true regime change, not a drift. The size view shows the headline cleanly.

The Power Share view tells us *how the displaced structural work was absorbed.*

Wind. Solar. Other renewables. Each took portions of the displaced load. There was no single replacement carrier.

The Activation Coefficient surfaces multiple yeast moments across the exit period — wind 2004 → 2005, biomass and other renewables in the mid-2010s, solar throughout. The instrument names them all.

The protocol separates **size decline** from **who absorbed the structural work.** A regression on raw shares would not show that separation.

*Pause — flip to the navigation chart.*

---

## Slide 11 — United Kingdom, course on the simplex   ·   30 sec   *(case study 3, beat 2)*

This is the UK helmsman trajectory. Course directness 0.36 — the jump-and-return archetype.

The course leaves the coal vertex sharply, then settles toward a new mix. Regime change reads as one decisive displacement followed by re-stabilisation. Distinct from Germany's continuous arc, distinct from Japan's looping search.

Three transitions. Three archetypes. One geometry that names them all.

---

## Slide 12 — 5 of 9 reproduce the pattern   ·   60 sec

From three case archetypes to a corpus-level result.

We applied the same protocol — same engine, same definition of deceptive drift — to all nine EMBER countries.

The signature fires in five of nine. **Australia, China, United Kingdom, India, Japan.**

The signature does *not* fire in Germany at annual grain, France, USA, or the World aggregate.

This matters. A useful detector should not fire everywhere. Discrimination is itself evidence the protocol is reading real structure, not artifact.

China and India top the helmsman-flips count — small carriers absorbing structural work over and over. USA, France, World aggregate top the peak Activation Coefficient — solar 2010 through 2015 acting at 500 to 760 times its size.

Same instrument. Nine countries. Five fire. Four stay quiet.

---

## Slide 13 — What the stack answers   ·   40 sec

One observable. Five distinct questions.

**WHAT** carriers are big — the size view.
**WHO** is at the wheel — the helmsman.
**WHEN** the steering changes — the helmsman trajectory.
**HOW MUCH** work each carrier did — Power Share.
**WHY** a small carrier mattered — Activation Coefficient.

The stack does not replace interpretation. It gives interpretation a reproducible object.

The repo carries the engine, the manuscript, the handout in six languages, and a structured adoption test for the community.

Thank you. Questions next — the cinema scroll will run behind us. Every plate the engine produced for the nine-country corpus, sixty-six slides, three hundred and twenty-five pages. Pause me anywhere.

---

## Timing summary

| Slide | Topic | Seconds |
|---|---|---|
| 1 | Title + question + contact + follow-along + CoDa-tools framing | 30 |
| 2 | Size view hides work (USA Solar 760×) | 50 |
| 3 | Five viewpoints | 35 |
| 4 | Activation Coefficient | 45 |
| 5 | Three archetypes overview | 20 |
| **6** | **Germany — share-and-work view** | **55** |
| **7** | **Germany — course on the simplex** | **30** |
| **8** | **Japan — share-and-work view** | **55** |
| **9** | **Japan — course on the simplex** | **30** |
| **10** | **UK — share-and-work view** | **55** |
| **11** | **UK — course on the simplex** | **30** |
| 12 | 5 of 9 cross-country | 60 |
| 13 | What the stack answers | 40 |
| **Spoken talk total** | | **~530 sec ≈ 8 min 50** |
| Cinema scroll | (Q&A backdrop) | 60 |
| Projector demo (Japan BARY → SHOCK → ALIGN) | (during Q&A) | 60 |
| **Total apparatus time** | | **~10 min 50** |
| Q&A reserve | | **~4 min** |

A 15-minute slot leaves ~4 min for direct Q&A on top of the cinema scroll and projector. The room can pause the scroll at any plate; that's the fallback if Q&A runs short.

**Per-country pacing note.** Each country pair is 85 seconds total (55 share-and-work + 30 navigation) — the same total time as the 10-slide version's 75-second single slide, plus 10 seconds for the flip. The trade is: 10 extra seconds, in exchange for the navigation chart being legible to the room.

---

## Voice notes

- **No preamble.** Walk on, open with "Good morning. *Title.* The question is X."
- **Periods, not commas.** Short sentences land. Long sentences scatter attention.
- **Numbers go first, qualifier after.** "0.107 percent — small" is better than "small — about 0.107 percent."
- **The case-study pairs are the heart of the talk.** Slides 6–11 deserve full delivery. Slow there. The earlier slides set up; the cases pay off.
- **On the navigation slides (7, 9, 11), let the chart breathe.** You've earned the bigger image; don't fill the time with words. State the course directness, name the archetype, draw the comparison to the previous country's trajectory, move on. Thirty seconds is enough.
- **Don't summarise the cases on slide 12.** The cross-country result speaks for itself once the three cases are in.
- **Slide 13 is the close.** End on *"It gives interpretation a reproducible object"* — let it sit. Then transition to Q&A.

---

## Optional verbal returns if asked

- **MC-4 (falsifiability):** "The claim is in the manuscript. Three conjuncts — Aitchison-native compositional metrics, formal change-point detection, carrier-level structural-work attribution. Four defeat paths — prior-art, metric, case, category. Any one of the four narrows or kills the claim. Please find one if you can; that's how the work improves."

- **Why this isn't already standard CoDa:** "The mathematics is standard. The CoDa community has had the geometry since Aitchison 1986. What I added is the time-series operational layer — walk the geometry forward, ask which carrier did the work at each step, name the diagnostic. That layer is the contribution."

- **Why these five viewpoints:** "Each one answers a distinct question that the others don't. Drop any one and you lose a question. Drop all five and you have a stacked-area chart."

- **Why split each country across two slides:** "The navigation chart is the geometry the talk earns. At 2.6 inches wide on a shared slide, the back of the room can't read it. At 6.5 inches wide on its own slide, every seat sees the trajectory at the same time. The expansion is room physics, not new content."

---

## Pairing the share-and-work + navigation slides — practical staging

Each country segment runs as a paired sequence:

| Beat | What's on screen | What you say |
|---|---|---|
| 1 | Share-and-work chart (big, dominant) | Numbers, dates, the yeast-factor signature, what the share view shows and what it hides |
| Transition | *(advance slide)* | "Now the navigation chart — what the course looked like on the simplex." |
| 2 | Navigation chart (centered, legible) | Course directness, the archetype name (continuous arc / loop / jump-and-return), the comparison to the previous country |

This pairing rhythm — content slide, then geometry slide — repeats three times. By the third country (UK on slides 10/11) the room knows the rhythm and the comparison to the previous two trajectories becomes part of the punch. The cross-country slide 12 then lands as the natural generalisation.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.   The AI follows the same protocol.*
