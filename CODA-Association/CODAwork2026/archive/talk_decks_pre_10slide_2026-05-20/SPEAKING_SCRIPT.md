# CoDaWork 2026 — Speaking script

*Compositional monitoring of energy-mix drift on the simplex*

**Speaker:** Peter Higgins · Rogue Wave Audio · Binaural Test Lab · Markham, Ontario, Canada
**Conference:** CoDaWork 2026 · Coimbra, Portugal · 1–5 June 2026
**Format:** 22 slides — 10 minutes of slide narration + 5 minutes of live-materials walkthrough · 15 minutes total
**Pace:** ~150 words per minute. Each slide beat ≈ 50 words ≈ 20 seconds. Pauses and gear-changes between sections eat the remaining ~2½ minutes within the 10-minute block. Speak naturally — the script is the rails, not the rope.

---

## ⏱  0:00 — Open (~15 seconds)

> Good [morning / afternoon]. I'm Peter Higgins, from Markham, Ontario — an independent researcher working out of Rogue Wave Audio. The talk takes fifteen minutes. Ten on the argument, five on the live materials. Everything you see is reproducible from EMBER data through an open-source engine.

---

## 🎞  10-minute slide block

### Slide 1 · Title  (0:15 → 0:35)

> *Compositional monitoring of energy-mix drift on the simplex.* The proposition for the next ten minutes is simple: five viewpoints, stacked into one observable, name the hidden drivers of an energy transition that the standard chart hides. The mathematics is not new. The monitoring application may be.

### Slide 2 · The Question  (0:35 → 0:55)

> When an electricity mix shifts over twenty-five years, two questions appear together. What path did the system take? And why? The first is what the size view answers. The second — which carrier was actually doing the structural work — the size view silently misses. That gap is what this talk fills.

### Slide 3 · Viewpoint 1 — the size view  (0:55 → 1:15)

> Here is the world electricity mix as everyone draws it. Coal dominates. Solar a sliver after 2010. Gas grows, nuclear declines. But hold this number in your head: in the United States in 2012, solar was zero-point-one percent of the mix — and did eighty-one percent of the structural work that year. The size view never showed that. No size view ever could.

### Slide 4 · The five-viewpoint protocol  (1:15 → 1:35)

> The protocol I'm proposing is five viewpoints, each answering one question, combined into one observable stack. The mathematical foundation is standard compositional data analysis — closure, the centred log-ratio, the Helmert-orthonormal basis, the Aitchison distance. The contribution is the operational stack — five lenses chosen so their combination is the complete answer.

### Slide 5 · Viewpoint 2 — the helmsman  (1:35 → 1:55)

> The helmsman is the carrier with the largest CLR displacement at each year-to-year step. Equation five. It's a categorical assignment — *this carrier did the most directional work this year*. I plot it with dotted lines. Solid lines would falsely imply a continuous path between carriers. The flip count tells you how often the system re-organises.

### Slide 6 · Viewpoint 3 — Power Share  (1:55 → 2:15)

> Power Share, equation six, is the natural decomposition of squared Aitchison distance across the carriers. Per step, it sums to one hundred percent. No carrier is hidden by the bookkeeping. The headline: what is *big* and what is *moving* are different questions. A thirty-percent-share carrier holding steady has zero Power Share. A point-one-percent-share carrier in rapid growth can be at seventy-five.

### Slide 7 · Viewpoint 4 — the Activation Coefficient  (2:15 → 2:35)

> The Activation Coefficient — equation seven, the yeast factor — is the central diagnostic. Power Share divided by composition share at the start of the step. If a carrier did exactly its size's share of work, alpha equals one. If alpha is far above one, you have a small carrier doing structural work — a hidden driver. *USA solar, twenty-twelve to twenty-thirteen: alpha equals seven hundred and sixty times.*

### Slide 8 · The hidden driver — solar, 2010–2015  (2:35 → 2:55)

> Across nine national electricity mixes, solar at sub-zero-point-two percent share did seventy to eighty-five percent of the structural directional work between twenty-ten and twenty-fifteen. Seven of the top ten yeast moments are solar in that window. This is what the framework is designed to make visible: where the structural work happened, not where the big numbers were.

### Slide 9 · Germany — the continuous arc  (2:55 → 3:15)

> Germany is the textbook continuous arc. Smooth multi-decade drift toward the renewable vertex. The size view shows coal receding, nuclear collapsing, solar and wind climbing. But the *Activation Coefficient* names twenty-oh-five to twenty-oh-six — solar at zero-point-two-one percent share — as the year the Energiewende actually began moving the mix. Three years before the size view called the shift visible.

### Slide 10 · Japan — the Fukushima cascade  (3:15 → 3:35)

> Japan is the external-shock archetype. Fukushima 2011. Aitchison distance for that single step is three times the median. But the deeper finding is what comes *after* — the helmsman flips seventeen times across the period, the loudest in the corpus. The reorganisation is a multi-year cascade, not a single step. The protocol reads the cascade directly.

### Slide 11 · United Kingdom — coal exit as regime change  (3:35 → 3:55)

> The UK is the policy-driven regime change. Coal goes from over thirty percent of the mix to under two. But the structural work isn't done by one successor — it's done by specific small carriers each working for two-to-three years at a time. Wind in 2001-02. Solar in 2012-13. Other Renewables absorbing the late coal exit. Coal disappeared into specifics, not into "renewables broadly."

### Slide 12 · Germany — the navigation chart  (3:55 → 4:15)

> Now look at it geometrically. This is a PCA projection of Germany's CLR trajectory — twenty-five years as a path through Aitchison space. Course directness zero-point-four-one. A long directional arc. The geometry confirms the size view's smooth-arc story but it also locates the inflection moments precisely.

### Slide 13 · Japan — the navigation chart  (4:15 → 4:35)

> Same view for Japan. Course directness zero-point-zero-nine — heavy looping. The trajectory snaps in 2011, then spends the next four years finding a new structure. This is what *multi-year reorganisation* looks like in compositional geometry. The plate centre moves a long way; then it keeps moving.

### Slide 14 · United Kingdom — the navigation chart  (4:35 → 4:55)

> And the UK. Course directness zero-point-three-six. Not the smooth arc of Germany, not the loop of Japan — a jump-and-return. The trajectory makes one long excursion as coal exits and the small renewable carriers absorb the displacement, then settles into a new neighbourhood. Three countries, three geometrically distinct archetypes, read by the same protocol.

### Slide 15 · Cross-country signature  (4:55 → 5:15)

> Across the nine-country corpus — Australia, China, France, Germany, India, Japan, the UK, the USA, and the World aggregate — the deceptive-drift pattern reproduces in five of nine. The cross-country signature isn't a forecast; it's a statement about where the structural work happened. Five viewpoints converging on the same hidden driver across six independent mixes is strong evidence.

### Slide 16 · Synthesis — WHAT path + WHY  (5:15 → 5:35)

> The five viewpoints answer one question each. Size view: WHAT carriers are big. Helmsman: WHO is at the wheel. Helmsman trajectory: WHEN the wheel changes. Power Share: HOW MUCH each carrier did. Activation Coefficient: WHY a small carrier mattered. Five views, five questions, one observable stack. The complete answer.

### Slide 17 · The falsifiable claim — MC-4 + four defeat paths  (5:35 → 6:00)

> The methodological claim is sharp. Compositional structure can be treated as a primary monitoring observable. Three conjuncts: Aitchison-native, formal change detection, carrier-level attribution. Four explicit ways a CoDa specialist can defeat it: *prior-art defeat* — show the combination already exists; *metric defeat* — show the verdicts reverse under a different valid metric; *case defeat* — show the signature is a preprocessing artefact; *category defeat* — show this is just an application note inside existing CoDa. If any of those land, the right room to find out is this one.

### Slide 18 · Bridge — every plate the engine produced  (6:00 → 6:20)

> What follows is not slides about data. It is the data — every plate the engine produced — scrolled through as a movie. Nine countries, twenty-six years, six plates per country. Sixty-six slides in roughly thirty seconds. Watch the carrier patterns sweep across the corpus. Pause anywhere. Every quantity is hash-chained to the input CSV.

### Slide 19 · Q & A — with the projector running  (6:20 → 6:40)

> For the discussion I'll keep an interactive 3-D projector running behind me. It reads the same data — three projection modes, the one I built up tonight and two more. RADAR stack for the per-year radar snapshot. BARYCENTER trajectory — the spine bends through space along the ILR-Helmert PCA path. ALIGN forces the trajectory onto the z-axis so you see pure structural variation. It runs in your browser, no install, no network.

### Slide 20 · Repositories — reproduce in five minutes  (6:40 → 7:00)

> Two public repositories. Higgins-decomposition holds the engines — CNT v3, CNQ v2 — both Python and R, with a forty-three-test suite. Higgins-Unity-Framework holds the governance, the MC-4 framing, the EITT canonical, the kill-switch. Apache-2.0 for code, CC BY 4.0 for documentation. Free to use, free to cite, help is available — open an issue, contact me directly.

### Slide 21 · AI Use Declaration  (7:00 → 7:20)

> Per HUF Publication Standard one, version one-point-one, conforming to ICMJE, COPE, Nature/Springer, Science/AAAS, WAME, the EU AI Act 2024, arXiv, ACM, and IEEE. I used Claude, ChatGPT, Copilot, Gemini, and Grok during this work — for drafting support, consistency editing, prior-art search, and adversarial review. AI tools are not listed as authors. I retain full scientific responsibility.

### Slide 22 · Standard Stamp — closing  (7:20 → 7:40)

> *The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.* The mathematics is not new. The monitoring application may be. If that sentence is wrong, this is the right room to kill it. Thank you. I'll move to the live materials now and take questions through them.

**[Slide 22 ends here. Total elapsed: ~7:40. You now have ~2:20 of pauses and gear-changes built into the 10-minute block, then move to live materials.]**

---

## 🔬  5-minute live-materials walkthrough  (10:00 → 15:00)

### 0:00 → 1:00 — the manuscript  (1 minute)

> Behind the talk is a twenty-five-page peer-reviewable paper. Cover page, table of contents, abstract — three case studies in the body, four defeat paths in the discussion, three appendices: equations, terminology, plate digest. Twenty-eight external references, eleven repository references. The Methods section has a zero-point-one-percent floor sensitivity analysis I encourage you to attack.

*(Open the manuscript PDF on the second screen. Scroll to the table of contents, then jump to the four-defeat-paths section in the Discussion, then to Appendix A equations.)*

### 1:00 → 2:30 — the talk deck and cinema scroll  (1 minute 30)

> The talk deck you just saw is twenty-two slides — but the actual engine output behind it is sixty-six. Master cover, then nine country sections of six plates each. Stage 1 section view, the system course plot, the helmsman family, the ILR-Helmert triplet, and the CNQ quaternion dashboard. Every plate is regenerated deterministically from the EMBER CSV. Hash-chained provenance, top to bottom.

*(Open `CodaWork2026_PremierDataOutput_2026-05-13.pdf`. Auto-scroll or page through quickly to show the master-cover → country-section structure. Highlight one country section, e.g. Japan, scroll through its six plates.)*

### 2:30 → 4:30 — the projector  (2 minutes)

> And this is the live tool. The H-superscript-s manifold projector. Eight countries inline, three projection modes. Click Japan. Click ORBIT. *[wait for rotation to settle]* This is RADAR — the per-year radar snapshots stacked along time. Each carrier is a vertex at a fixed angle; the radius is the normalized CLR.

> Click BARY. *[mode flips]* The spine of plate centres now bends through space — that's the ILR-Helmert PCA barycenter trajectory. Watch Japan twenty-thirteen to twenty-fifteen — the plate centre slides outward. That's the post-Fukushima multi-year reorganisation, visible directly.

> Click ALIGN. *[mode flips]* The trajectory bend is removed; the polygon now shows pure structural variation around each year's centroid — the CoDa-standard centred view. Click SHOCK. *[overlay activates]* The Aitchison-step magnitude tints each plate's outline. The shock years light up red. Read the panel in the top-left — it labels the active mode and shows the math.

*(Demonstrate Japan with BARY → ALIGN → SHOCK in that sequence. If time allows, click DEU to show the continuous-arc archetype as contrast.)*

### 4:30 → 5:00 — open invitation  (30 seconds)

> Everything you see runs on your laptop. github-dot-com slash PeterHiggins19 slash higgins-decomposition. The conference-attendees page walks every slide of this talk with the matching figure, equation, and JSON file. Help is free. Contact me directly. **The four defeat paths are in the manuscript Discussion — I would love to see them land.** Thank you.

---

## ⌚ Total beat plan

| Block | Time | Cumulative |
|---|---|---|
| Open | 0:15 | 0:15 |
| Slides 1–22 (~20 s each + transitions) | 7:25 | 7:40 |
| Buffer / gear-change pauses | 2:20 | 10:00 |
| Manuscript demo | 1:00 | 11:00 |
| Talk deck + cinema scroll demo | 1:30 | 12:30 |
| Projector demo (Japan walkthrough) | 2:00 | 14:30 |
| Open invitation | 0:30 | 15:00 |

---

## 📋 Performance notes

1. **Pace.** ~150 wpm. The numbers on slides 7, 8, and 9 — 760×, sub-0.2%, 70–85%, 333×, 0.21% — are the headline numbers. Land them on the beat. Don't rush them.

2. **The bridge to live materials.** When you finish slide 22, look up, take one breath, then move physically to the laptop or pointer. The shift in posture is the cue that the live demo has begun.

3. **The Japan walkthrough on the projector** is the visceral payoff. RADAR → BARY → ALIGN, in that order. The plate sliding outward on BARY is the moment the audience sees the framework do something the standard chart can't. Pause one extra second after each click — let the rotation settle so the room sees the geometry move.

4. **If you run long.** Cut the open invitation to: *"Everything is online. Repository, manuscript, projector. The four defeat paths are in the Discussion. Thank you."* That recovers 20 seconds.

5. **If you run short.** Linger on slide 17 (MC-4 + defeat paths) — read each defeat path slowly. That's the slide where lingering buys credibility.

6. **The closing line.** *"The mathematics is not new. The monitoring application may be. If that sentence is wrong, this is the right room to kill it."* Say it slowly. Look up after. That's the invitation to the room.

---

## Related documents in this folder

- [`README.md`](README.md) — folder map and presentation overview
- [`ABSTRACT.md`](ABSTRACT.md) — the committed conference abstract
- [`VERSION_HISTORY.md`](VERSION_HISTORY.md) — chronological revision log
- [`Compositional_Monitoring_2026.pdf`](Compositional_Monitoring_2026.pdf) — the 25-page peer-reviewable manuscript
- [`data_outputs/CodaWork2026_FinalTalk_2026-05-17.pdf`](data_outputs/CodaWork2026_FinalTalk_2026-05-17.pdf) — the 22-slide talk deck
- [`data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf`](data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf) — the 325-page cinema scroll
- [`data_outputs/codawork2026_projector.html`](data_outputs/codawork2026_projector.html) — the interactive 3-D projector
- [`../CONFERENCE_ATTENDEES.md`](../CONFERENCE_ATTENDEES.md) — slide-by-slide audience follow-along

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*The mathematics is not new; the monitoring application may be.*
