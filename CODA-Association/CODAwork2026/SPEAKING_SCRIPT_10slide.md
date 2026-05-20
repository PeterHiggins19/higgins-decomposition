# Speaking script — 10-slide compressed talk

**Deck:** `CODA-Association/CODAwork2026/data_outputs/CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx`
**Total target:** ~8 min talk + 1.5 min cinema scroll + 1 min projector = ~10.5 min spoken. Leaves ~4.5 min Q&A in a 15-minute slot.

Voice: direct, information-packed, no preamble. Each sentence carries a fact or a turn. Use periods, not commas. Numbers stay precise.

The case-study slides (6 Germany, 7 Japan, 8 UK) get the most time — that's where the room sees the instrument do work on data they recognise.

---

## Slide 1 — Title + question + contact   ·   25 sec

Good morning. *Compositional monitoring of energy-mix drift on the simplex.*

The question of this talk: **which carrier did the structural work?** Not which one got bigger. Which one moved the composition.

My email and the repo URL are on this slide. The one-page handout is in six UN languages — the QR code at the back leads to all of them. Let me begin.

---

## Slide 2 — The size view hides the work   ·   50 sec

Twenty-five years of world electricity. Stacked-area chart. Coal dominant. Gas grows. Nuclear declines. Solar appears as a thin sliver after 2010.

That is the headline view. Here is what it hides.

**USA Solar, 2012 → 2013.** Starting share, 0.107 percent. Structural Power Share, 81.7 percent. Activation Coefficient, approximately 760×.

Solar acted at 760 times its size. No size view shows that. No size view ever could.

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

Worked example. USA Solar, 2012 → 2013. Starting share 0.107 percent — small. Power Share 81.7 percent — most of the work. Alpha approximately 760.

Yeast is two percent of a loaf by mass and does one hundred percent of the rising. Same mathematical shape. Solar 2010 through 2015 appears repeatedly across the corpus as small-share, large-structural-work.

---

## Slide 5 — Three archetypes   ·   20 sec

Three case studies. Three different transition regimes.

Germany — deliberate transition, continuous arc. Japan — external shock, loop and reorganise. UK — regime change, jump and return.

One instrument reads all three.

---

## Slide 6 — Germany   ·   75 sec   *(case study 1)*

The Energiewende. Twenty-five years of deliberate composition change.

The size view tells you what you already know. Coal recedes. Gas holds. Solar and wind grow steadily. That is the headline.

The Power Share view tells you something the size view doesn't.

**Solar 2005 → 2006.** Share, 0.21 percent. Structural work, 71.1 percent. Activation Coefficient, approximately 333×.

Three years before the size view calls solar visible, the instrument names solar as the structural beginning of the Energiewende. The transition started in the data before it appeared on the chart.

The helmsman trajectory shows course directness 0.41 — a continuous arc toward the renewable vertex on the simplex. Thirteen helmsman flips across twenty-five years.

This is the textbook case of a deliberate transition. The size view confirms what we know. The Power Share view tells us **when it actually started.**

---

## Slide 7 — Japan   ·   75 sec   *(case study 2)*

Fukushima 2011. The shock appears in every viewpoint simultaneously.

Composition — nuclear collapses. Helmsman — seventeen flips across twenty-five years, the loudest count in the corpus. Power Share — massive concentration of squared CLR motion at one step. Aitchison distance 2011 → 2012, approximately three times the neighbouring-year baseline.

But the years *after* the shock tell the deeper story.

Japan's post-Fukushima mix kept reorganising for more than a decade. The yeast moments distribute across multiple carriers — solar, gas, wind, renewables, each taking turns absorbing the displaced nuclear share. Wind 2004 → 2005, alpha 188. Nuclear 2015 → 2016, alpha 187. Solar 2005 → 2006, alpha 176. The list goes on for years.

Course directness 0.09. A looping reorganisation. Not a single step.

The instrument detects both the shock *and* the multi-year recovery. That is what the stack adds to the size view.

---

## Slide 8 — United Kingdom   ·   75 sec   *(case study 3)*

Coal exit as regime change. Between 2012 and 2020, coal goes from more than 30 percent of UK electricity to less than 2 percent.

That is a true regime change, not a drift. The size view shows the headline cleanly.

The Power Share view tells us *how the displaced structural work was absorbed.*

Wind. Solar. Other renewables. Each took portions of the displaced load. There was no single replacement carrier.

The Activation Coefficient surfaces multiple yeast moments across the exit period — wind 2004 → 2005, biomass and other renewables in the mid-2010s, solar throughout. The instrument names them all.

Course directness 0.36. Jump-and-return archetype. Coal jumps out of the system; the system finds a new equilibrium spread across renewable carriers.

The protocol separates **size decline** from **who absorbed the structural work.** A regression on raw shares would not show that separation.

---

## Slide 9 — 5 of 9 reproduce the pattern   ·   60 sec

From three case archetypes to a corpus-level result.

We applied the same protocol — same engine, same definition of deceptive drift — to all nine EMBER countries.

The signature fires in five of nine. **Australia, China, United Kingdom, India, Japan.**

The signature does *not* fire in Germany at annual grain, France, USA, or the World aggregate.

This matters. A useful detector should not fire everywhere. Discrimination is itself evidence the protocol is reading real structure, not artifact.

China and India top the helmsman-flips count — small carriers absorbing structural work over and over. USA, France, World aggregate top the peak Activation Coefficient — solar 2010 through 2015 acting at 500 to 760 times its size.

Same instrument. Nine countries. Five fire. Four stay quiet.

---

## Slide 10 — What the stack answers   ·   40 sec

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
| 1 | Title + question + contact | 25 |
| 2 | Size view hides work (USA Solar 760×) | 50 |
| 3 | Five viewpoints | 35 |
| 4 | Activation Coefficient | 45 |
| 5 | Three archetypes overview | 20 |
| **6** | **Germany (case 1)** | **75** |
| **7** | **Japan (case 2)** | **75** |
| **8** | **UK (case 3)** | **75** |
| 9 | 5 of 9 cross-country | 60 |
| 10 | What the stack answers | 40 |
| **Spoken talk total** | | **~500 sec ≈ 8 min 20** |
| Cinema scroll | (Q&A backdrop) | 90 |
| Projector demo (Japan BARY → SHOCK → ALIGN) | (during Q&A) | 60 |
| **Total apparatus time** | | **~11.5 min** |
| Q&A reserve | | **~3.5 min** |

A 15-minute slot leaves ~3.5 min for direct Q&A on top of the cinema scroll and projector. The room can pause the scroll at any plate; that's the fallback if Q&A runs short.

---

## Voice notes

- **No preamble.** Walk on, open with "Good morning. *Title.* The question is X."
- **Periods, not commas.** Short sentences land. Long sentences scatter attention.
- **Numbers go first, qualifier after.** "0.107 percent — small" is better than "small — about 0.107 percent."
- **The case studies are the heart of the talk.** Slides 6, 7, 8 deserve full delivery. Slow there. The earlier slides set up; the cases pay off.
- **Don't summarise the cases on slide 9.** The cross-country result speaks for itself once the three cases are in.
- **Slide 10 is the close.** End on "It gives interpretation a reproducible object" — let it sit. Then transition to Q&A.

---

## Optional verbal returns if asked

- **MC-4 (falsifiability):** "The claim is in the manuscript. Three conjuncts — Aitchison-native compositional metrics, formal change-point detection, carrier-level structural-work attribution. Four defeat paths — prior-art, metric, case, category. Any one of the four narrows or kills the claim. Please find one if you can; that's how the work improves."

- **Why this isn't already standard CoDa:** "The mathematics is standard. The CoDa community has had the geometry since Aitchison 1986. What I added is the time-series operational layer — walk the geometry forward, ask which carrier did the work at each step, name the diagnostic. That layer is the contribution."

- **Why these five viewpoints:** "Each one answers a distinct question that the others don't. Drop any one and you lose a question. Drop all five and you have a stacked-area chart."

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.   The AI follows the same protocol.*
