# Backup Presentation — what to do if the equipment fails

**Document version:** 1.1
**Document status:** authoritative
**Created:** 2026-05-13 v1.0; **Revised:** 2026-05-13 v1.1 (added AI Use Declaration per HUF-STD-001)
**Author:** Peter Higgins, Rogue Wave Audio
**Conforms to:** HUF Publication Standards (HUF-STD-001)

**Purpose.** This is the contingency plan. If the projector dies, the laptop won't boot, the conference Wi-Fi is gone, the room's adapter doesn't match yours, or PowerPoint refuses to open the deck on the conference machine, you can still deliver the entire 15-minute talk from this document.

**Method.** Read it once before you fly. Carry it on your phone. If the equipment fails, walk to the lectern and deliver from voice alone. The talk works on a phone, on a piece of paper, or from memory.

---

## The two-minute equipment-fail diagnostic

If something goes wrong:

1. **Do not panic.** The room will wait 60 seconds while you problem-solve.
2. **Try the simplest fix first.** Conference machine: hit the right HDMI source. Conference adapter: yours might not be the only option in the AV cabinet.
3. **If after 60 seconds the slides are not up, switch to voice-only.** Say something like: *"The slides are not cooperating today. I'll walk through this without them — the talk works without slides because the geometry is yours and I just need to name what I built on top of it. If you want to see the visuals afterward, the deck is in the open repository and I can email anyone."*
4. **Open this document on your phone or laptop screen** if either is available. The phone version of this document is a complete fallback.
5. **Deliver the talk from the anchors.** This document gives you everything you need.

The audience will be on your side. CoDa community members are technical and friendly. Equipment failure is the *least* embarrassing thing that happens at academic conferences. Calmly proceeding without slides is a minor credibility booster, not a discredit.

---

## The fallback delivery — beat by beat (15 minutes total)

### Beat 1 — The simplex view (1 min)

*"A country's electricity mix is a vector of carrier shares that sums to one. Coal, gas, oil, nuclear, hydro, wind, solar, bioenergy, other — nine carriers in the EMBER public dataset. Each year, each country produces one point on the simplex Δ^8.*

*The mix moves. It moves in ways that the totals don't capture. Total electricity output can be flat while the composition shifts dramatically. That motion — the structural change inside the unity constraint — is what the talk is about.*

*Energy generation is a composition. The geometry is yours. I built a monitoring instrument inside it."*

### Beat 2 — The data and MC-4 (1 min)

*"The data is EMBER, monthly electricity production by carrier, nine countries, 2001 through 2025. Twenty-five years. Coal, gas, oil, nuclear, hydro, wind, solar, bioenergy, other.*

*The claim of this talk is simple to state and easy to defeat. We say: no existing monitoring framework combines all three of these conjuncts — natively in Aitchison geometry, with formal change detection, at the carrier level — combined into one observable stack.*

*That is the central falsifiable claim. Four ways to defeat it come at Beat 9."*

### Beat 3 — The protocol (2 min)

*"The protocol uses standard CoDa operators. Perturbation. Closure. CLR. Helmert-ILR. Aitchison distance. These are yours and we use them carefully.*

*On top of those, we add two small supporting metrics. TV distance — total variation — measures how fast the composition is moving structurally. K-eff measures concentration — how many carriers are meaningfully participating in the structure.*

*There is one important self-discipline note. In an earlier version we labelled a metric as L2 when it was actually TV. The correction is on the record in the repo. We tell on ourselves when we mislabel. This matters because INV-050 — TV / Aitchison metric-invariance — is the result that says the protocol's verdict doesn't depend on which of these two metrics you use. INV-050 is verified across 101 datasets and is CANONICAL in the Investigation Catalog."*

### Beat 4 — Japan (2 min)

*"The first case is Japan, 2011 to 2012, post-Fukushima. The step-Δ Aitchison distance spikes by a factor of three over neighbouring years. Seventeen helmsman flips — the highest in the corpus. The carrier-level attribution names nuclear to fossil substitution.*

*The protocol catches this cleanly. It catches it as a regime change — an abrupt external shock disrupting clean classification. Not as a deceptive drift. The protocol distinguishes between shock and drift.*

*Japan is the warm-up case. Loud, unambiguous, easy to verify against everyone's prior knowledge of the world. By the end of this beat, you know the protocol catches abrupt structural transitions. The next case is harder."*

### Beat 5 — Germany (3 min — the longest beat)

*"Germany is the headline. Germany is the trajectory case — the continuous arc toward the renewable vertex. No single spike. Multi-year slide. IR class is OVERDAMPED_EXTREME — smooth convergence to an attractor.*

*At the monthly grain, the deceptive-drift detector returns p = 0.0016. That is the packet's headline empirical claim.*

*Now the caveat — and I want to read this exactly because it matters. The p-value is computed against the series' own empirical-frequency baseline. This is a weaker null than a Dirichlet, permutation, or bootstrap null. The community knows these alternatives. The empirical-frequency baseline is the weakest defensible null. If the community has a preferred null, we will adopt it and rerun.*

*The Germany trajectory is the 'stable total, shifting mix' archetype. Total generation is comparatively flat. Internal mix shifts dramatically. This is the cleanest public demonstration of compositional monitoring revealing structure that headline totals hide.*

*Thirteen helmsman flips. High stability score — S_σ around 0.43. The flips are spread evenly, not concentrated. The carrier-level attribution names continuous nuclear phase-down and continuous renewable growth.*

*Germany is the cleanest case. The p-value is conditional. The methodology is open. The trajectory is real."*

### Beat 6 — UK coal exit (1 min)

*"The third named case is the UK coal exit. 2012 to 2016. Coal share collapses from dominant to negligible. Fifteen helmsman flips. IR class OVERDAMPED_EXTREME.*

*The protocol reads this as a regime change in the step-Δ Aitchison distance pattern. Different shape from Japan — Japan was external and abrupt. UK is policy-driven and abrupt. Germany was policy-driven and continuous. Three archetypes, three different shapes. The protocol discriminates among them."*

### Beat 7 — Beyond the three (1 min)

*"Beyond the three named cases, we tested the deceptive-drift signature across the full nine-country corpus. The result is 5 of 9 — five countries reproduce the signature: AUS, CHN, GBR, IND, JPN.*

*Four countries do not reproduce it. Germany at annual grain shows K-eff tightening but TV above median — loud drift, not deceptive. France is in a loosening regime — K-eff has been rising as renewables join the nuclear baseline. USA is mostly stable. WLD aggregate doesn't fire because aggregation smooths the individual signatures.*

*This is INV-051 CANONICAL. The protocol discriminates. It does not over-fire. Generalisation is supported but moderate — not universal."*

### Beat 8 — Three open questions (1 min)

*"At this point I want to stop explaining what we found and start asking what you think.*

*Three questions for the room.*

*Q1: the relationship between K-eff — concentration measures — and the Aitchison norm of the change vector. Are they the same observable in two different clothes, or two different facets of compositional structure?*

*Q2: the right family of valid simplex distances against which to test verdict-invariance. INV-050 establishes TV / Aitchison pair-invariance. Does it extend to weighted log-ratio? Mahalanobis on CLR? Egozcue–Pawlowsky-Glahn evidence information distance? I do not know.*

*Q3 — and this is the one that matters most methodologically — the right null model for compositional change-point detection. Dirichlet? Permutation? Bootstrap? Each has trade-offs. I do not have a preferred answer. If the community recommends one, we will adopt it and rerun.*

*These are open questions. I genuinely want the answers."*

### Beat 9 — Four defeat paths (2 min)

*"Four ways to defeat the central claim. I have catalogued them so the room can do its job.*

*Metric defeat — show the verdict flips under a different valid simplex metric. Preempted by INV-050.*

*Case defeat — show the signature fires uniformly everywhere. Preempted by INV-051. Five of nine fire; four do not. The protocol discriminates.*

*Prior-art defeat — show the three-conjunct conjunction already exists. The closest adjacent prior art I have found is Morais, Thomas-Agnan and Simioni 2017/18 — compositional plus Dirichlet for market-share regression — and Arata and Onozaki 2017 — CoDa for market-share dynamics using ILR. Both thank Egozcue and Pawlowsky-Glahn. Neither combines all three conjuncts. Three more search areas are pending. This path is open.*

*Category defeat — show this is an application note within existing CoDa, not a new monitoring category. We have no preconceived answer. This path is open.*

*A defeater must combine all three conjuncts. Inspection is invited."*

### Beat 10 — Close (1 min)

*"Two repositories. higgins-decomposition for the deterministic compositional engine — CNT v3.1.0 and CNQ v2.0.0. Higgins-Unity-Framework for the broader scientific context and the published falsifiability artifact — KILL-001, nineteen named failure modes.*

*One self-discipline note — the L2 to TV correction is on the record.*

*Hashes carry the receipts. Anyone with the raw CSV can verify any plate in approximately two minutes. The reproducibility checklist is at the repository root.*

*The talk is an ascent waypoint, not the summit.*

*Thank you. I'll take questions."*

---

## What to do if Q&A also has equipment trouble

The pedagogical tables (Table 1 SU(2) double cover, Table 2 helmsman, Table 3 EITT, Table 4 bread) are in [`PEDAGOGICAL_TABLES.md`](PEDAGOGICAL_TABLES.md) on your phone. The Q&A bench cards are in [`QA_BENCH.md`](QA_BENCH.md). Both work without slides.

If a really deep question comes and you can't get to the document, the verbal fallback for each:

- **SU(2) question.** *"The compositional change between two points on the simplex is a rotation in ILR space. CNT computes it geometrically. CNQ shows the rotation lives in SU(2) — the double cover of SO(3). The double cover is why the helmsman flip exists — q and minus-q give the same rotation but different sign."*
- **Helmsman question.** *"Each year, the protocol identifies the dominant carrier driving the structural change. That carrier gets a sign — plus or minus — based on the orientation in ILR space. When the sign changes year to year, that's a flip. Japan's 17 flips post-Fukushima reflect rapid switching between nuclear collapse and fossil surge."*
- **EITT question.** *"Entropy-Invariant Time Transformer. Shannon entropy is conserved under geometric-mean temporal compression for compositional carriers. We measured 0.18 percent variation across a 341 to 1 compression ratio. It's the temporal-invariance sibling of MC-4's spatial-invariance. Published in the HUF companion repository."*
- **Bread question.** *"The simplest version. Bread is four carriers — flour, water, salt, yeast — summing to one composition. K-eff is how alive the dough reads. TV is how fast it's moving. The yeast is the active carrier — the component of power. The baker holds the breakpoint — decides when the bread is done. The same instrument that reads electricity grids reads bread."*

---

## The one-page emergency brief

If you have only 60 seconds to scan before walking on, this is what to hold in mind:

- **MC-4 three conjuncts:** Aitchison-native + formal change detection + carrier-level attribution → one observable stack.
- **Germany p = 0.0016 with the null caveat:** computed against the series' own empirical-frequency baseline — weaker than Dirichlet / permutation / bootstrap.
- **AUS CHN GBR IND JPN** — 5 of 9 reproduce.
- **Defeat:** Metric ✓ INV-050. Case ✓ INV-051. Prior-art open (Morais; Arata). Category open.
- **Closing:** *The talk is an ascent waypoint, not the summit.*

---

## File metadata

- **Document version.** 1.0 — baseline authoritative version
- **Supersedes.** May-12 BACKUP_PRESENTATION.md in `papers/codawork2026/talk/`
- **Lockdown compatibility.** S2 doc-only addition

---

## AI Use Declaration

In accordance with established scientific community standards (ICMJE, COPE, Nature, Science, WAME, EU AI Act 2024, arXiv, ACM, IEEE) this work discloses AI assistance. **AI tools used:** Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI) — the HUF AI Collective. **Tasks:** drafting fallback beat-by-beat scripts; consistency editing against the live deck content. **Author responsibility:** the author retains full responsibility; AI tools are not authors. **Governance:** HUF AI Collective cross-check protocol. **Dates:** March 2026 – May 2026. **Standards:** HUF-STD-001.

---

*If the slides die, the talk does not.*
*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
