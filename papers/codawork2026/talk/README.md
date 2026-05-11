# CoDaWork 2026 — Talk Oratory

**Title:** Compositional monitoring of energy-mix drift on the simplex
**Speaker:** Peter Higgins
**Where:** Coimbra, Portugal — 1–5 June 2026
**Time:** 15 minutes + Q&A

---

## How to use this folder

This folder is **the talk in three forms**:

- **This README** — the spoken script. Read top-to-bottom on a phone, tablet, or laptop. Each beat is a section. Each section links to the matching slide file.
- **`slides/`** — one Markdown file per slide. Visual described + spoken text + transition phrase to the next slide.
- **`qa_bench/`** — Q&A response cards. Tap when a reviewer asks the named question.

Three other files in this folder:

- **`STUDY_PAGE.md`** — how to *moot* the talk (law-student phrase-chain memorization).
- **`CHEAT_SHEET.md`** — one-page backstage scanner. Spine phrases only.
- **`BACKUP_PRESENTATION.md`** — if AV fails, you read directly from this README.

**Phone-friendly:** every page is short paragraphs. No tables wider than 3 columns. No requirement to load images.

**Self-contained:** works offline. No external links needed during the talk. Open the repo on your phone, mirror it locally if needed.

---

## The spine — ten beats in fifteen minutes

| Beat | Time | Anchor phrase | Slide |
|---|---|---|---|
| 1 | 1 min | *"Energy generation is a composition."* | [→ slide_01](slides/slide_01_simplex_view.md) |
| 2 | 1 min | *"No monitoring framework combines all three conjuncts."* | [→ slide_02](slides/slide_02_data_and_mc4.md) |
| 3 | 2 min | *"Perturbation, Aitchison distance, TV distance, K-eff."* | [→ slide_03](slides/slide_03_protocol.md) |
| 4 | 2 min | *"Japan, Fukushima, 2011–2012, the spike."* | [→ slide_04](slides/slide_04_japan_fukushima.md) |
| 5 | 3 min | *"Germany, the trajectory, the deceptive drift, p = 0.0016 — with the null caveat."* | [→ slide_05](slides/slide_05_germany_continuous.md) |
| 6 | 1 min | *"The UK coal exit registers as a regime change."* | [→ slide_06](slides/slide_06_uk_coal_exit.md) |
| 7 | 1 min | *"Beyond the three: five-of-nine countries reproduce the deceptive signature."* | [→ slide_07](slides/slide_07_beyond_three.md) |
| 8 | 1 min | *"Three open questions for the room."* | [→ slide_08](slides/slide_08_three_open_questions.md) |
| 9 | 2 min | *"A defeater must combine all three conjuncts."* | [→ slide_09](slides/slide_09_four_defeat_paths.md) |
| 10 | 1 min | *"Two repositories, one self-discipline note, thank you."* | [→ slide_10](slides/slide_10_closing.md) |

**Cuts applied by default:** Germany year-by-year animation is removed (Beat 5 uses static start + mid + end); live demo is removed (Beat 10 says "see me afterward"). See `CHEAT_SHEET.md` for the cut order if you need to drop more.

---

## Beat 1 (1 min) — The simplex view

> *"Energy generation is a composition. A country's electricity mix in a given year is a vector of carrier shares that sum to one. Coal, gas, oil, nuclear, hydro, wind, solar, biomass, other — nine carriers, on the eight-simplex. Standard compositional data analysis gives us the right machinery: closure to put each year on the simplex, perturbation to move from one year to the next as a relative change rather than a difference, Aitchison distance to measure how big that change is, and a concentration measure related to effective diversity to read how spread out the mix is."*

→ See [slide_01_simplex_view.md](slides/slide_01_simplex_view.md)

---

## Beat 2 (1 min) — The data and MC-4

> *"The data is EMBER electricity generation, 2001 to 2025, nine countries on a coherent range. The central claim — MC-4, sharpened to its three-conjunct form: no monitoring framework in the energy or market-share literature operates **natively in Aitchison geometry**, with **formal change detection**, at the **carrier level** — the three conjuncts combined into one observable stack. A defeater must overturn the conjunction. Falsifiable. I'll come back to that at the end."*

→ See [slide_02_data_and_mc4.md](slides/slide_02_data_and_mc4.md)

---

## Beat 3 (2 min) — The protocol

> *"Period to period, the composition perturbs. The magnitude is the Aitchison distance. Alongside it we compute TV distance — half the L1 — bounded zero to one, useful for visual presentation. They differ in magnitude. They agree on every shock hit-or-miss verdict across the nine-country corpus — INV-050 in our catalog — robust within this pair. Whether that invariance extends to the broader simplex-distance family is the second of our three open questions."*

> *"K-eff — exp of Shannon entropy on the closed composition — is our concentration measure. Equal mix gives K-eff equal to D. Single-carrier dominance gives K-eff approaching one. K-eff and the Aitchison norm co-vary but are not the same quantity — the abstract names this relationship as the first open question."*

> *"One self-discipline note worth surfacing here rather than at the end: in the original packet the metric was labelled L2. ChatGPT corpus review in March 2026 caught that the labelling was wrong — what we had computed was TV distance, half-L1. We corrected it. Both metrics now run side-by-side, and the agreement of their verdicts is what gave us INV-050."*

→ See [slide_03_protocol.md](slides/slide_03_protocol.md)

---

## Beat 4 (2 min) — Japan: Fukushima 2011–2012

> *"Japan post-Fukushima — the abstract's first named transition. The nuclear share collapses; gas and coal absorb the shortfall. In the Aitchison-distance step column for the JPN run, you see it: a step-delta spike at 2011 to 2012 that is several times any neighbouring year. The helmsman family — our carrier-attribution layer — fires seventeen direction flips over the period, the highest in the eight-country set. The trajectory is loud; the protocol catches it; the carrier-level attribution names nuclear-to-fossil as the substitution."*

→ See [slide_04_japan_fukushima.md](slides/slide_04_japan_fukushima.md)

---

## Beat 5 (3 min) — Germany: continuous trajectory + deceptive drift

> *"Germany is the second named transition — and the case the packet built around. The trajectory is continuous: a long arc toward the renewable vertex. The IR classification is overdamped extreme: snap-to-attractor. No single spike — instead, a multi-year slide."*

> *"On top of that, the deceptive-drift signature. The packet's protocol detects months where K-eff is tightening while TV stays at or below the series median. Internal redistribution within an apparently stable whole. Germany pre-2022 fires. The p-value is 0.0016."*

> ***Null-model caveat — said on the slide, not hidden in speaker notes:*** *"that p-value is computed against the series' own empirical-frequency baseline. This is a weaker null than a Dirichlet, permutation, or bootstrap null. The right null for compositional change-point detection on the simplex is the third of our three open questions. We treat p = 0.0016 as an opening empirical claim, not a closed methodological one."*

> *"Static visual: start composition, mid-trajectory snapshot, end composition. The continuity is in the shape; you don't need the animation to see it."*

→ See [slide_05_germany_continuous.md](slides/slide_05_germany_continuous.md)

---

## Beat 6 (1 min) — UK: coal exit as regime change

> *"The UK is the third named transition. Different shape from Japan or Germany. Not a single shock; not a continuous slide. An abrupt step-change in the step-delta Aitchison-distance pattern: coal share collapses from dominant to negligible across about four years. Helmsman flips: fifteen. The protocol reads it as a regime change. The carrier-level attribution names coal as the carrier that exited."*

→ See [slide_06_uk_coal_exit.md](slides/slide_06_uk_coal_exit.md)

---

## Beat 7 (1 min) — Beyond the three

> *"Beyond DEU, JPN, GBR — the engine's concentration-regime tag fires `deceptive` at annual grain in five of nine EMBER countries. AUS, CHN, GBR, IND, JPN. Catalogued as INV-051. Germany at annual grain shows K-eff tightening but TV above median — loud drift, not deceptive — the protocol distinguishes the two cleanly. The packet's single-country headline is the conservative case. Across multiple economies of different structural types — Pacific economy, large emerging, island nation, post-Fukushima reorganisation — the signature reproduces."*

→ See [slide_07_beyond_three.md](slides/slide_07_beyond_three.md)

---

## Beat 8 (1 min) — Three open questions

> *"Three open questions for the room."*

> *"Q1 — the abstract's open question: K-eff exp(H) versus the Aitchison norm. We compute both. They co-vary. They are not the same. We do not have a clean analytical relationship. We are hoping the room knows more than we do."*

> *"Q2 — the right family of valid simplex distances against which to test verdict-invariance. INV-050 demonstrated pair-invariance for TV and Aitchison. What distance family would the room consider a fair stress test?"*

> *"Q3 — and the most methodologically consequential — the right null model for compositional change-point detection on the simplex. The packet's empirical-frequency null is the weakest defensible null. Dirichlet is parametric. Permutation disrupts temporal structure. Bootstrap is heavy. None obviously fits monitoring. If the room has a preferred null, we will adopt it and rerun."*

→ See [slide_08_three_open_questions.md](slides/slide_08_three_open_questions.md)

---

## Beat 9 (2 min) — Four defeat paths

> *"The packet states MC-4 with four falsifiability conditions. Twenty seconds each on the first two:"*

> *"Metric defeat — preempted by INV-050. TV and Aitchison agree on every shock verdict in the nine-country corpus."*

> *"Case defeat — preempted by INV-051. Five of nine countries reproduce the deceptive-drift signature; the protocol correctly classifies the other four as non-deceptive."*

> *"The two that remain open are where the room comes in."*

> *"Prior-art defeat — and here the framing is operational, not defensive: **a defeater must combine all three conjuncts.** Aitchison-native geometry, formal change detection, and carrier-level attribution. Together, in one observable stack. We have searched one of four named areas — sectoral allocation in macroeconomics. The closest adjacent work we found is Morais, Thomas-Agnan and Simioni 2017, and Arata and Onozaki 2017 — both use ILR on market shares, both explicitly thank Egozcue and Pawlowsky-Glahn, neither combines all three conjuncts. Three areas remain to search. If the room knows prior work that does combine all three, the claim is narrowed or killed. That is the correct outcome."*

> *"Category defeat — and here the framing is humble: this may be a new monitoring category. It may be at most an application note inside existing CoDa. We have no preconceived answer. We welcome the room's view, including the view that the MC-4 label is too strong."*

→ See [slide_09_four_defeat_paths.md](slides/slide_09_four_defeat_paths.md)

---

## Beat 10 (1 min) — Close

> *"Two repositories: the submission origin at PeterHiggins19/Higgins-Unity-Framework, and the production engine at PeterHiggins19/higgins-decomposition — both public, both Apache-2.0 for the code. The engines are deterministic with hash-chained outputs; the four binding doctrines — SEA, STP, CRD, engine-independence — make every claim auditable."*

> *"The talk is an ascent waypoint, not the summit. Thank you. I'll take questions."*

→ See [slide_10_closing.md](slides/slide_10_closing.md)

---

## After the talk — Q&A bench

The most likely questions, with cached answers, are in [qa_bench/](qa_bench/):

- [INV-050 metric-invariance](qa_bench/INV050_metric_invariance.md) — what we tested, what we did not
- [INV-051 5-of-9 deceptive drift](qa_bench/INV051_deceptive_drift_5of9.md) — why these 5, why not the other 4
- [Prior-art defeat](qa_bench/prior_art_defeat.md) — Morais, Arata, the three remaining search areas
- [Category defeat](qa_bench/category_defeat.md) — application note vs new monitoring category
- [Three open questions bench cards](qa_bench/three_open_questions_bench_cards.md) — Q1/Q2/Q3 with one-paragraph each

---

## How to study this on your phone

See [STUDY_PAGE.md](STUDY_PAGE.md). Short version: memorise the ten anchor phrases. The rest follows from the chain. Practice mooting it — read your phrase, speak the beat, check against this README.

## If AV fails

See [BACKUP_PRESENTATION.md](BACKUP_PRESENTATION.md). Short version: open this README on your phone. Read down. The talk is in here, end to end.

---

*This README is the talk. The slides are visualisations of the talk. The cheat sheet is the spine of the talk. The Q&A bench is the body of the talk. Everything else in the repo is the receipts behind the talk.*
