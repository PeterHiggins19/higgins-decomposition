# Cheat Sheet — one page, backstage scannable

**Document version:** 1.1
**Document status:** authoritative
**Created:** 2026-05-13 v1.0; **Revised:** 2026-05-13 v1.1 (added AI Use Declaration per HUF-STD-001)
**Author:** Peter Higgins, Rogue Wave Audio
**Conforms to:** HUF Publication Standards (HUF-STD-001)

**Title:** Compositional monitoring of energy-mix drift on the simplex
**Time:** 15 min talk + Q&A
**Strategic compass:** [SPEAKER_BRIEF.md](SPEAKER_BRIEF.md) — read once before going on
**Q&A depth backup:** [PEDAGOGICAL_TABLES.md](PEDAGOGICAL_TABLES.md)
**Q&A prepared answers:** [QA_BENCH.md](QA_BENCH.md)

---

## The ten anchors (the spine)

```
1. "Energy generation is a composition."
2. "No monitoring framework combines all three conjuncts."
3. "Perturbation, Aitchison distance, TV distance, K-eff."
4. "Japan, Fukushima, 2011-2012, the spike."
5. "Germany, the trajectory, deceptive drift, p=0.0016 with null caveat."
6. "The UK coal exit is a regime change."
7. "Beyond the three: 5-of-9 reproduce."
8. "Three open questions for the room."
9. "A defeater must combine all three conjuncts."
10. "Two repos, one self-discipline note, thank you."
```

---

## Six lines word-for-word

1. **MC-4 (Beats 2 + 9):** *"natively in Aitchison geometry, with formal change detection, at the carrier level — combined into one observable stack"*
2. **Germany null caveat (Beat 5):** *"computed against the series' own empirical-frequency baseline — a weaker null than Dirichlet, permutation, or bootstrap"*
3. **Defeat-path framing (Beat 9):** *"A defeater must combine all three conjuncts."*
4. **Five countries (Beat 7):** **AUS, CHN, GBR, IND, JPN.** Five of nine.
5. **Three open questions (Beat 8):** Q1 = K-eff vs Aitchison norm. Q2 = right family of simplex distances. Q3 = right null model.
6. **Closing (Beat 10):** *"The talk is an ascent waypoint, not the summit."*

---

## Two papers cited in Beat 9

- **Morais, Thomas-Agnan & Simioni (2017/2018)** — compositional + Dirichlet for market-share regression
- **Arata & Onozaki (2017)** — CoDa for market-share dynamics, uses ILR

Both thank Egozcue & Pawlowsky-Glahn. Neither combines all three conjuncts.

---

## Three named transitions

- **Japan post-Fukushima 2011–2012** — perturbation spike; nuclear → fossil substitution; 17 helmsman flips
- **Germany continuous trajectory** — overdamped-extreme IR class; toward renewable vertex; 13 flips
- **UK coal exit** — regime change in step-Δ Aitchison; 15 flips

---

## Time budget (with Cuts 1+2 applied by default)

```
Beat 1: 1 min    simplex view
Beat 2: 1 min    data + MC-4 three-conjunct
Beat 3: 2 min    protocol (perturbation, Aitchison, TV, K-eff, L2→TV note)
Beat 4: 2 min    Japan Fukushima spike
Beat 5: 3 min    Germany trajectory + deceptive drift + null caveat ON SLIDE
Beat 6: 1 min    UK coal exit
Beat 7: 1 min    5-of-9 deceptive
Beat 8: 1 min    three open questions
Beat 9: 2 min    four defeat paths
Beat 10: 1 min   close (NO LIVE DEMO — say "see me afterward")
----
Total: 15 min
```

If running over by Beat 6 → **Cut 3:** drop OWID 73-country slide in Beat 7.

---

## Q&A — first answer for the most likely questions

**"What about the null model?"**
→ Q3 is exactly this question. The packet's empirical-frequency null is the weakest defensible null. Dirichlet is parametric, permutation disrupts temporal structure, bootstrap is heavy. If the room has a preferred null, we will adopt and rerun.

**"What about other simplex distances?"**
→ Q2 — pair-invariance is shown for TV and Aitchison; whether it extends to weighted log-ratio, Mahalanobis on CLR, or Egozcue–Pawlowsky-Glahn evidence information distance is open. Suggestions welcome.

**"Why those 5 countries and not the other 4?"**
→ Germany at annual grain shows K-eff tightening but TV above median — loud drift, not deceptive. USA and WLD are mostly stable. FRA is mostly loosening. The protocol distinguishes regimes; it does not just fire everywhere.

**"Is this prior art?"**
→ One of four search areas executed. Morais et al. and Arata & Onozaki are the closest. Neither combines all three conjuncts. Three search areas pending. Pointers welcome.

**"Is this really a new monitoring category?"**
→ We don't know. Could be application-note status inside existing CoDa. Welcoming the room's view.

**"Reproducibility?"**
→ Public repos, Apache-2.0 code, deterministic engines, hash-chained outputs, 25-experiment reference corpus. See `REPRODUCIBILITY_CHECKLIST.md` at repo root.

**"R-language version?"**
→ Yes — cnt.R at v3.0.0; cnq.R at v2.0.0. Per-field parity at 1e-13 tolerance. v3.1.0 R port queued.

**"What is EITT?"** *(Q&A backstop — verbal answer)*
→ Entropy-Invariant Time Transformer. Shannon entropy is conserved under geometric-mean temporal compression for compositional carriers. 0.18% variation across 341:1 ratio. It's the temporal-invariance sibling of MC-4's spatial-invariance. Full explanation in `papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md` if anyone wants to follow up.

**"What about KILL-001?"** *(Q&A backstop)*
→ Published falsifiability artifact in the HUF companion repo. 19 named failure modes in 5 categories. Worst failure mode is KILL-3.3 — artificial carrier — which the framework cannot mechanically detect; only the domain expert can. We named it explicitly because a framework with no kill conditions is not science.

---

## What to do if you blank

1. Look at this page. Find the anchor.
2. Say it. The rest comes back.
3. If it doesn't — skip to the next anchor. The audience won't notice.

## What to say if you don't know

1. "That's an interesting question."
2. "My honest answer is, I don't know."
3. "Would you be willing to talk after? I'd value the pointer."

---

## Last 30 seconds before you go on

- Phone in pocket on silent.
- One slow breath in (4 counts), out (6 counts). Twice.
- Anchor 1: *"Energy generation is a composition."* Say it in your head.
- Walk to the lectern.
- Anchor 1, out loud. Begin.

---

## File metadata

- **Document version.** 1.0 — baseline authoritative version
- **Supersedes.** May-12 CHEAT_SHEET.md in `papers/codawork2026/talk/`
- **Lockdown compatibility.** S2 doc-only addition

---

## AI Use Declaration

In accordance with established scientific community standards (ICMJE, COPE, Nature, Science, WAME, EU AI Act 2024, arXiv, ACM, IEEE) this work discloses AI assistance. **AI tools used:** Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI) — the HUF AI Collective. **Tasks:** drafting cheat-sheet structure; first-answer Q&A formulation. **Author responsibility:** the author retains full responsibility; AI tools are not authors. **Governance:** HUF AI Collective cross-check protocol. **Dates:** March 2026 – May 2026. **Standards:** HUF-STD-001.

---

*One page. Designed to be scanned in 30 seconds. The whole talk is in here.*
