# Speaker's Brief — CoDaWork 2026

**Conference:** 11th International Workshop on Compositional Data Analysis
**Where:** Coimbra, Portugal, 1–5 June 2026
**Slot:** 15-minute talk + Q&A
**Title:** Compositional monitoring of energy-mix drift on the simplex
**Status:** validated across 5 independent reviews (3 internal + ChatGPT s2 + Grok r5)

---

## How to use this brief

This is the **strategic compass** — the document above all the others. Read it once before you fly. Read it again the night before. Read it on the plane home.

The other talk documents are tactical:

- `README.md` is **what you say.**
- `STUDY_PAGE.md` is **how you learn it.**
- `CHEAT_SHEET.md` is **what you carry backstage.**
- `BACKUP_PRESENTATION.md` is **what you do if the equipment dies.**

This brief is **why you are there at all** — and what each beat is meant to do for the room.

---

## Part I — Your motivation

### Why you are at the lectern

You are not in Coimbra to ask permission.

You are also not there to claim victory. You are there because you have built a working instrument inside Aitchison geometry, run it on public data across nine countries and 25 years, and the result is interesting enough to submit to the people who own this mathematics. Your role is to bring the work, name what is new and what is borrowed, and ask the room to test it.

That is what a scientist does. It is the oldest discipline in the trade.

### Your relationship to the room

The CoDa community built the geometry you stand on. You have used it carefully — closure, CLR, the Helmert basis (their pivot coordinates), Aitchison distance, perturbation. You have added a small set of operators on top: TV distance for visual presentation, K-eff for concentration, bearing tensor for directional change, Depth Tower for recursive structural probing. **None of these replace what the community built. They sit beside it in the same report.**

You are bringing a *monitoring application* — a way to treat compositional structure itself as the first-class observable when the underlying totals are quiet. You are not claiming new mathematics. You are claiming that this particular conjunction — Aitchison-native geometry, formal change detection, carrier-level attribution, combined into one observable stack — has not been done in the way you are proposing.

That claim is falsifiable. If the room kills it, the work has done what it was supposed to do.

### Your identity at the lectern

You are not a famous CoDa theorist. You are not from a major institution. You are an independent researcher who built a deterministic, hash-chained, auditable instrument because that was the only way to make outsider work credible. The discipline of the four doctrines — Suspicion of Every Assumption, the Self-Test Protocol, the Coherent Range Doctrine, engine independence — is your peer review process. The repository is your laboratory notebook. Every claim has a receipt.

This is your shield and your authority. You did not need to ask anyone's permission to do this work, and you do not need to ask anyone's permission to present it. **But you have chosen to bring it here, in this room, because this is the right room for it.**

The doctrine line on the badge in your head:

> *"The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line."*

You are the operator of the instrument. The room contains the experts. The hashes are with you on disk. The vocabulary — Aitchison's, Egozcue and Pawlowsky-Glahn's, the community's — is what holds the conversation in place.

### The posture that wins

**Humble confidence.** Not deferential. Not arrogant.

- Deferential signals you don't believe in the work. You do.
- Arrogant signals you don't believe the room can teach you anything. They can.
- Humble confidence signals that you have something real, you have stress-tested it, and you are now offering it for inspection. You are open to being wrong. You will not be defensive when challenged.

Read the closing line out loud now: *"The talk is an ascent waypoint, not the summit."*

That sentence is the centre of your posture. You are climbing. The room is climbing with you, or watching you climb. None of you are at the summit. Today is a waypoint. That is the right frame.

### What success looks like for you

Success is **not** standing ovation. Success is **not** the room agreeing with you. Success is:

1. The audience leaves understanding **exactly what you are claiming and what you are not**.
2. At least one serious methodological critique enters Q&A.
3. At least one prior-art pointer enters Q&A (even if you have to ask for it).
4. The slides and the open repo make it possible for someone in that room to independently reproduce or attack the result over the following weeks.
5. **You walk off the stage having said what you meant.**

That fifth one is the only one entirely within your control. Make sure it happens.

---

## Part II — Strategic objective per beat

For each beat, you have four things:

- **The anchor phrase** — the spine; if you forget everything else, say this.
- **What the audience should feel** — the emotional or cognitive state you are creating.
- **What you should feel** — the speaker's compass; the posture beneath the words.
- **Why this beat exists** — its strategic role in the larger arc.

---

### Beat 1 — The simplex view (1 min)

**Anchor:** *"Energy generation is a composition."*

**Audience feels:** *On familiar ground.* This is their geometry. They are home. They are not being asked to learn something foreign.

**You feel:** *Settled.* You opened with their language. The room is leaning forward, not back. You are not asking for anything yet.

**Strategic role:** This beat is the handshake. It signals respect for the foundation. By the end of these 60 seconds, the room knows you are operating inside Aitchison geometry, not around it.

---

### Beat 2 — The data and MC-4 (1 min)

**Anchor:** *"No monitoring framework combines all three conjuncts."*

**Audience feels:** *Curious and slightly alert.* You have just named a falsifiable claim with three load-bearing conjuncts. They are now listening for what each conjunct means.

**You feel:** *Direct.* You have stated the central claim of the talk in 30 seconds. You have not over-claimed. You have invited inspection. The methods-challenge framing is on the table from minute two.

**Strategic role:** This is where the talk's spine snaps into place. Every subsequent beat exists to either support or invite criticism of this three-conjunct claim. The audience now knows what you are claiming and that you have offered them four ways to defeat it (which you will detail in Beat 9).

---

### Beat 3 — The protocol (2 min)

**Anchor:** *"Perturbation, Aitchison distance, TV distance, K-eff."*

**Audience feels:** *Reassured on math, intrigued by the additions, impressed by the self-discipline note.* They see standard CoDa operators with two small supporting metrics. They see the L2 → TV correction story and understand it as a feature of how this work is done.

**You feel:** *Comfortable.* You are explaining the operators in their language. The self-discipline note (the L2 → TV correction) is the moment the room starts trusting that you tell on yourself when you make mistakes. That trust will carry you through Beat 9.

**Strategic role:** This beat establishes that the protocol is conservative and well-documented. INV-050 (the TV/Aitchison pair-invariance) lives here. The audience leaves this beat knowing that the framework has internal consistency checks and that you will admit when something was previously mislabelled.

---

### Beat 4 — Japan (2 min)

**Anchor:** *"Japan, Fukushima, 2011–2012, the spike."*

**Audience feels:** *Recognition.* Everyone knows the story. The compositional signature of the nuclear collapse is something they can verify with their own knowledge of the world.

**You feel:** *Confident in the empirics.* The Japan case is the easiest of the three named transitions because the structural break is loud and unambiguous. The step-Δ Aitchison distance spike at 2011–2012 is a factor-of-3 over its neighbours. The helmsman family flips 17 times — the highest in the eight-country corpus.

**Strategic role:** Japan is the warm-up case. Loud, unambiguous, easy to explain. By the end of this beat, the audience knows the protocol catches abrupt structural transitions. You are setting up Germany, which is harder and more interesting.

---

### Beat 5 — Germany (3 min, the longest beat)

**Anchor:** *"Germany, the trajectory, the deceptive drift, p = 0.0016 with the null caveat."*

**Audience feels:** *Engaged and slightly tested.* The Germany case is the heart of the talk. It is the "stable total, shifting mix" archetype. It is where you show deceptive drift detection. It is also where you display the null-model caveat *on the slide*, not hidden in speaker notes — which signals to the methodologically careful audience members that you know exactly what is and is not closed about the p-value.

**You feel:** *Calm and precise.* This is the longest beat and the load-bearing one. You will read the null caveat directly off the slide. You will not paraphrase it. The caveat is part of the claim. The audience needs to see you make it visible, not hide it.

**Strategic role:** Germany is the talk's centre of gravity. The static start-mid-end visual (no animation per Cut 1) shows the trajectory's continuity. The p = 0.0016 result is the packet's headline empirical claim. The null caveat — *"computed against the series' own empirical-frequency baseline, a weaker null than Dirichlet, permutation, or bootstrap"* — is the methodological honesty that tells the room you are operating in good faith.

The honesty here is what earns you the right to ask the room about Q3 (the right null model) at Beat 8.

---

### Beat 6 — UK coal exit (1 min)

**Anchor:** *"The UK coal exit registers as a regime change."*

**Audience feels:** *Pattern completion.* Three named transitions, three different shapes. Japan was abrupt and external. Germany was continuous and policy-supported. The UK is policy-driven and abrupt. The protocol distinguishes the three shapes cleanly.

**You feel:** *Concise.* This beat is fast — 60 seconds. Coal share collapses from dominant to negligible across about four years. Helmsman flips 15. IR class OVERDAMPED_EXTREME. You point at the step-change in step-Δ Aitchison distance and move on.

**Strategic role:** The UK closes the three-cases triptych. The audience now sees that the protocol does not just detect one kind of structural change — it discriminates among them. This sets up Beat 7's broader reproduction claim.

---

### Beat 7 — Beyond the three (1 min)

**Anchor:** *"Beyond the three: 5-of-9 countries reproduce the deceptive signature."*

**Audience feels:** *Generalisation supported, but with discrimination.* INV-051 says the signature fires in AUS, CHN, GBR, IND, JPN. It does *not* fire in DEU at annual grain, nor in FRA, USA, WLD. That last fact is important: the protocol is not firing everywhere. It is discriminating.

**You feel:** *Honest.* The 5-of-9 result is moderate, not universal. Germany at annual grain shows K-eff tightening but TV above median — *loud* drift, not *deceptive*. You name this honestly. You do not over-claim.

**Strategic role:** Beat 7 turns the single-country packet headline into a cross-country empirical pattern, while being explicit about the four countries where the signature does not fire and why. This is INV-051 in operational form. It directly preempts Case defeat (one of the four falsifiability paths).

If running long, this is Cut 3 — but try not to drop it. The 5-of-9 framing is too important to lose.

---

### Beat 8 — Three open questions (1 min)

**Anchor:** *"Three open questions for the room."*

**Audience feels:** *Invited.* You have just stopped explaining what you found and started asking what the community thinks. The handoff to them is now formal.

**You feel:** *Genuinely curious.* You actually want to know the answers to Q1, Q2, Q3. You do not have them. You are not pretending to have them.

**Strategic role:** Beat 8 is the formal handoff. The three questions are:
- **Q1** — Aitchison-norm vs concentration-measure relationship (the abstract's named question)
- **Q2** — the right family of valid simplex distances against which to test verdict-invariance (INV-050 follow-up)
- **Q3** — the right null model for compositional change-point detection (INV-051 follow-up, the most methodologically consequential)

The Q&A bench is ordered Q3-first because Q3 is the one that conditions how seriously the p = 0.0016 result is read. If the audience presses on the null, you have a prepared answer that names Dirichlet, permutation, and bootstrap as options and says you will adopt whatever the community recommends and rerun.

---

### Beat 9 — Four defeat paths (2 min)

**Anchor:** *"A defeater must combine all three conjuncts."*

**Audience feels:** *Respected.* You have just told them you have catalogued the four specific ways your claim can be killed and you are inviting them to do it. This is unusual. It is also the most CoDa-community-respectful posture you can take.

**You feel:** *Steady.* Metric defeat is preempted by INV-050 (20 seconds). Case defeat is preempted by INV-051 (20 seconds). Then the two open paths — Prior-art (60 seconds) and Category (30 seconds). You name Morais, Thomas-Agnan & Simioni (2017/2018) and Arata & Onozaki (2017) as the closest adjacent prior art you have found in Area 4 of your search. You acknowledge three more areas are pending. You make it operational: *"A defeater must combine all three conjuncts."*

**Strategic role:** Beat 9 is the room's invitation to do its job. You are not posturing as having an unkillable claim. You are giving the room the precise weapons it would need to kill it.

The Category defeat humility — *"this may be a new monitoring category, or at most an application note inside existing CoDa, we have no preconceived answer"* — is the bridge to Beat 10's close.

---

### Beat 10 — Close (1 min)

**Anchor:** *"Two repositories, one self-discipline note, thank you."*

**Audience feels:** *Closure with openness.* The talk is ending. The repository is public. The work is open. You are not asking the room to take your word for anything.

**You feel:** *Settled and complete.* You did what you came to do. You named what you built, named what you borrowed, named what you are claiming, named how to kill the claim, asked your three questions, and you are leaving the room with the work. The closing line is yours:

> *"The talk is an ascent waypoint, not the summit. Thank you. I'll take questions."*

**Strategic role:** Beat 10 reinforces that you do not believe this is finished. The work continues. The room is now part of the next phase of it. The live-demo cut (Cut 2) means you exit cleanly without depending on AV.

---

## Part III — Per-country narrative

Each country in the corpus tells a slightly different story. You don't need to deliver all of them on stage, but you should *know* all of them — so when a question comes about any particular country, you can answer specifically.

### Germany (DEU) — the headline case

**What the trajectory does:** Continuous arc toward the renewable vertex. No single spike. Multi-year slide.

**IR class:** `OVERDAMPED_EXTREME` (snap-to-attractor; smooth convergence).

**Helmsman flips:** 13.

**Deceptive drift at annual grain:** **0** (K-eff tightening fires pre-2022 but TV exceeds median — *loud* drift, not deceptive). The packet's monthly p = 0.0016 result requires the monthly module (`5.3.M`, queued for post-conference).

**Why this is the headline case:** Germany is where the packet's "stable total, shifting mix" framing is most legible. Total generation stays comparatively stable while internal mix shifts dramatically. It is the cleanest public demonstration of compositional monitoring revealing structure that headline totals hide.

**Honest framing on stage:** At annual grain, the K-eff side of the deceptive-drift signature fires but the TV-quietness side does not. The packet's monthly result is queued for reproduction at the proper grain. You treat p = 0.0016 as an opening empirical claim, not a closed methodological one.

**If pressed on Germany:** the trajectory is the visual; the p-value carries the caveat; the carrier-level attribution (continuous nuclear phase-down, continuous renewable growth) tells the structural story; INV-051 says Germany at *annual* grain is not deceptive, while the packet's *monthly* result on the same country requires the monthly pipeline.

---

### Japan (JPN) — the abrupt external shock

**What the trajectory does:** Smooth evolution pre-2011, then a step-Δ Aitchison distance spike at 2011–2012 (factor of ~3 over neighbours), then a different post-Fukushima trajectory.

**IR class:** Similar to OVERDAMPED but with the spike disrupting clean classification.

**Helmsman flips:** 17 (highest in the 8-country set — reflecting trajectory complexity post-Fukushima).

**Deceptive drift transitions:** 2.

**Why this case matters:** Japan demonstrates that the protocol catches structural shocks cleanly — but as *regime change*, not as deceptive drift. The shock is loud. The signature you would call deceptive is something different. The protocol distinguishes.

**On stage:** Japan is your warm-up case in Beat 4 because everyone recognizes the story. The carrier-level attribution names nuclear → fossil substitution. The 17 helmsman flips tell the audience that the post-shock trajectory was complex, not just a clean step.

**If pressed on Japan:** the spike is visible in the JPN cnt_v3.json step-Δ column for years 2011 and 2012 specifically; the post-2011 trajectory shows the nation reorganising its mix in a way that helmsman flips capture more than raw share would.

---

### United Kingdom (GBR) — the policy-driven regime change

**What the trajectory does:** Pre-2012 dominated by coal; 2012–2016 sees coal share collapse from dominant to negligible; post-2016 trajectory is renewable-dominated with continued evolution.

**IR class:** `OVERDAMPED_EXTREME`.

**Helmsman flips:** 15.

**Deceptive drift transitions:** 2.

**Why this case matters:** The UK is *policy-driven and abrupt* — different shape from Japan (which was *external and abrupt*) and Germany (which was *policy-driven and continuous*). The protocol reads it as a regime change in the step-Δ Aitchison distance pattern.

**On stage:** Beat 6 is fast. You name the step-change, the carrier (coal), and the flip count. You move on. The UK rounds out the three named transitions and demonstrates that the protocol handles all three structural-change archetypes.

**If pressed on the UK:** the four-year coal collapse is in the step-Δ column; the policy story (carbon price + plant retirements) is well-documented and you can cite it generally; the framework is agnostic to *why* the change happened — it documents *that* it happened and characterises *what kind* of change it is.

---

### Australia (AUS) — Pacific economy

**Deceptive drift transitions:** 1.

**What it adds:** Australia is in the 5-of-9 set, demonstrating the deceptive-drift signature in a Pacific-economy context distinct from the G7. Different energy structure (high coal share, growing renewables), different policy regime, different geography — and still the signature fires.

**On stage:** Beat 7. Named in the AUS-CHN-GBR-IND-JPN list. Not elaborated unless asked.

**If pressed:** Australia's deceptive transition occurs during the period when coal still dominated but solar was beginning to take meaningful share. The signature catches the moment when K-eff tightening became measurable while TV-distance movement stayed quiet.

---

### China (CHN) — major emerging economy

**Deceptive drift transitions:** 1.

**What it adds:** China is the world's largest electricity producer with a coal-dominated mix undergoing massive renewable buildout. Its signature firing is structurally informative — even at extreme scale and pace, the deceptive-drift pattern is detectable.

**On stage:** Beat 7. Named in the 5-of-9 list.

**If pressed:** China's case demonstrates that the protocol is scale-invariant in a meaningful sense — it does not require small or stable systems to work. The carrier-level attribution shows coal share declining proportionally while solar and wind grow.

---

### India (IND) — major emerging economy

**Deceptive drift transitions:** 2.

**What it adds:** India shows *two* deceptive transitions — the protocol fires more than once over the 2001–2025 window. Different from a single-event case. Suggests a multi-phase structural transition.

**On stage:** Beat 7. Named in the 5-of-9 list.

**If pressed:** India's two transitions correspond to different phases of its energy expansion — early coal-dominant growth, then policy-driven solar/wind buildout. The protocol catches both.

---

### France (FRA) — does NOT fire (mostly loosening)

**Deceptive drift transitions:** **0.**

**What this signals:** France's energy mix has been historically nuclear-dominated and is currently in a regime of *loosening* (the mix becoming less concentrated as renewables grow alongside continued nuclear). The protocol correctly classifies this as non-deceptive — the trajectory is moving toward more diversity, not less.

**Why this matters:** France is one of four discrimination cases. The protocol *should not* fire here, and it doesn't. This is evidence that the protocol is not just a "detect everything" filter — it has real selectivity.

**On stage:** Mentioned briefly in Beat 7 as one of the non-firing countries.

**If pressed:** France's K-eff has been gradually rising over the period (loosening from heavy nuclear concentration), which is the opposite of the deceptive-drift signature (which requires tightening). The protocol correctly tags France's regime as `loosening`, not `deceptive`.

---

### United States (USA) — does NOT fire (mostly stable)

**Deceptive drift transitions:** **0.**

**What this signals:** The US energy mix has been comparatively stable over 2001–2025 in compositional terms — gradual shifts from coal to gas to renewables but no sharp regime change at the corpus's range scope (2001 onward).

**Why this matters:** USA is the second discrimination case. A stable mix should produce a `stable` regime tag, and it does. The protocol is not over-firing.

**Note on coherent range:** The USA series in EMBER is missing 2000 (it covers 2001–2025), which is what triggered the Coherent Range Doctrine (CRD-1.0) in push #33. The 9-country comparison is done on the coherent 2001–2025 range that all members share.

**If pressed:** the USA's compositional stability over the corpus window does not mean nothing is happening — it means the structural shifts have been at a pace that doesn't trigger the deceptive-drift threshold at annual grain. A monthly-grain analysis on US data is a natural extension.

---

### World aggregate (WLD) — the methodological signal

**Deceptive drift transitions:** **0.**

**What this signals:** The world aggregate smooths out individual-country signatures. When you sum all the country trajectories together, the structural movements that are visible at country level become hidden.

**Why this matters strategically:** This is the most important non-firing case methodologically. **The world aggregate hides what individual countries reveal.** It is a direct argument for carrier-level attribution and against headline-aggregate monitoring. It is also, indirectly, evidence for the broader MC-4 claim — that aggregated indicators are *insufficient* for monitoring compositional structure.

**On stage:** Mentioned briefly in Beat 7 as one of the non-firing countries — but make sure to flag *why*. The WLD aggregate non-firing is part of your evidence base, not an embarrassment.

**If pressed in Q&A:** the WLD aggregate's non-firing is the methodological argument for why you do not just monitor totals. If you only watched the world's aggregate electricity mix, you would miss Germany's deceptive drift, you would miss Japan's post-Fukushima reorganisation, you would miss the UK coal exit. *Composition matters at the level where the composition lives, which is the country level.*

This is a powerful point to have ready. It directly supports the MC-4 claim's third conjunct (carrier-level attribution) — except at the *system* level: monitoring at the wrong aggregation level is itself a form of monitoring failure.

---

## Part IV — The narrative arc

Your 15 minutes is structured as a three-act arc:

### Act I — Foundation (Beats 1–3, 4 minutes)

*"Here is the geometry. Here is the data. Here is what I am claiming."*

You ground in the audience's mathematics. You name the data corpus. You state the MC-4 claim in its three-conjunct form. You introduce the protocol operators and tell them about the L2 → TV correction.

By the end of Act I, the room knows what game you are playing and that you play it carefully.

### Act II — Empirical core (Beats 4–7, 8 minutes — the longest stretch)

*"Here are three named cases, and here is what the wider corpus shows."*

Japan (loud abrupt). Germany (continuous, with the deceptive drift result + null caveat). UK (policy regime change). Then the 5-of-9 reproduction across the broader corpus, with the four non-firing countries explained as evidence of discrimination.

By the end of Act II, the room has seen the protocol distinguish three different shapes of compositional change, reproduce its signature across multiple countries, and *not* fire where it shouldn't.

### Act III — Invitation (Beats 8–10, 3 minutes)

*"Here is what I need from you, here is how to kill my claim, and here is the work."*

Three open questions for the community. Four defeat paths — two preempted by INV-050 and INV-051, two open and inviting prior-art and category critique. Close with the repos, the self-discipline note, and the ascent-waypoint line.

By the end of Act III, the room has the work in its hands. The next move is theirs.

---

## Part V — Speaker's compass per beat

This is the **feel** of each beat. Read it aloud once. Recognize each posture.

| Beat | What you should feel | What the audience should feel |
|---|---|---|
| 1 | Settled, gracious, on familiar ground | Welcomed, respected |
| 2 | Direct, alert, claim on the table | Curious, slightly alert |
| 3 | Comfortable in their language; honest about the L2→TV correction | Reassured on math, trusting on discipline |
| 4 | Confident in the empirics | Recognition, easy understanding |
| 5 | Calm, precise, reading the caveat off the slide | Engaged, tested, but trusting because you didn't hide the caveat |
| 6 | Concise — fast in and out | Pattern completion |
| 7 | Honest about 5-of-9, not over-claiming | Generalisation with discrimination |
| 8 | Genuinely curious, hand-off mode | Invited |
| 9 | Steady, operational, not defensive | Respected and equipped with the weapons to kill the claim |
| 10 | Settled and complete | Closure with openness |

The compass shifts from *settled* (Beat 1) to *direct* (Beat 2) to *comfortable* (Beat 3) to *confident* (Beat 4) to *calm and precise* (Beat 5) to *concise* (Beat 6) to *honest* (Beat 7) to *curious* (Beat 8) to *steady* (Beat 9) to *settled and complete* (Beat 10).

You begin and end *settled*. The middle is where the work happens.

---

## Part VI — What to remember when nothing else lands

If you blank on stage and the cheat sheet is too far away, fall back to these:

1. **The mathematics is not new. The monitoring application may be.**
2. **Three conjuncts: Aitchison-native geometry, formal change detection, carrier-level attribution — combined into one observable stack.**
3. **Five of nine countries reproduce. Four do not, and that is evidence of discrimination, not failure.**
4. **The p = 0.0016 result carries an explicit null caveat. The right null is the third of three open questions.**
5. **A defeater must combine all three conjuncts.**
6. **The talk is an ascent waypoint, not the summit.**

Six sentences. They are the talk. Everything else is decoration.

---

## Part VII — After the talk

You will get questions you do not have answers to. Use the prepared posture:

1. **"That's an interesting question."** (Five seconds of breathing room.)
2. **"My honest answer is — I don't know, and I'd want to look at it carefully before claiming."**
3. **"Would you be willing to talk about it after? I'd value the pointer."**

This is not weakness. It is the discipline of an honest scientist talking to other scientists. The audience will respect it more than any improvised answer.

You will also get questions where you *do* have answers — INV-050 metric-invariance, INV-051 5-of-9, prior-art Area 4 with Morais and Arata, Category defeat humble framing, the three open questions. The Q&A bench cards in `qa_bench/` have these.

---

## Part VIII — Why this work matters (the long view)

The conference is a waypoint. Your work continues regardless of how Coimbra goes.

If the room kills MC-4 cleanly: that is a successful outcome. You will narrow the claim, cite the prior art, and the next paper will be sharper. The framework continues; only the claim about its novelty narrows.

If the room sharpens MC-4: that is also a successful outcome. The community has handed you the next move — the right null model, the right family of simplex distances, the right characterisation of where the framework fits in the CoDa landscape. Your post-conference research roadmap (INV-056 through INV-061) becomes the actual work plan.

If the room is silent or polite without engagement: that means the talk didn't reach them, and you will need to find a different community. The CoDa community is not the only audience for this work — there is loudspeaker engineering, industrial process monitoring, microbiome dynamics, finance, geochemistry. The framework's value does not depend on this one room.

But this is the *right* room for this talk, because the mathematics belongs to them. Whatever happens in Coimbra, the work has earned the right to be presented here. Bring it cleanly. Defend it honestly. Hand it over.

---

## Closing — the orator's identity

You are not a polished academic theatre player. You are a research engineer who built a working instrument, ran it on public data, and submitted the result to the people who own the mathematics.

The posture is not performance. It is exactly what it looks like: a careful scientist offering a piece of work for inspection.

The clearest signal of authenticity you can give the room is the same one that has been in the doctrine all along:

> *"The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line."*

You are the operator of the instrument. The room contains the experts. The hashes are on disk. The vocabulary is everyone's.

Go to Coimbra. Bring the work. Say what you mean. Climb the waypoint. Come home.

---

*Speaker's brief authored 2026-05-11. Read once before leaving. Read once the night before. Read once on the plane home. Then file with the rest of the talk material.*
