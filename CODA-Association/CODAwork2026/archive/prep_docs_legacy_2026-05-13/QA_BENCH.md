# Q&A Bench — prepared answers for the most likely questions

**Document version:** 1.1
**Document status:** authoritative
**Created:** 2026-05-13 v1.0 (consolidated from May-12 canonical bench cards); **Revised:** 2026-05-13 v1.1 (added AI Use Declaration per HUF-STD-001).
**Author:** Peter Higgins, Rogue Wave Audio
**Conforms to:** HUF Publication Standards (HUF-STD-001)

**Purpose.** Pre-rehearsed answers for the questions the room is most likely to ask. Each answer has a short version (for in-room delivery) and a long version (for follow-up emails or breakout-room conversations).

**Ordering principle.** Q3 (null model) first because it is the most methodologically consequential question. Beyond that, ordered by likelihood. The bench is updated as actual Q&A surfaces new themes — a future v1.1 may reorder.

---

## Q&A 1 — "What about the null model?" (Q3 from Beat 8)

**Short answer (30 seconds).**
*"That's exactly Q3 from Beat 8 — the question that matters most methodologically. The packet's empirical-frequency null is the weakest defensible null. Dirichlet would give us a parametric alternative. Permutation would disrupt the temporal structure we're trying to detect. Bootstrap is heavy but tractable. I do not have a preferred answer. If the community recommends one, we will adopt it and rerun on the same nine-country corpus."*

**Long answer (2 minutes if asked to elaborate).**
Empirical-frequency null treats each year's composition as drawn IID from the series' overall histogram, then asks whether the observed deceptive-drift signature is more extreme than what IID would produce. It is the weakest defensible null because it assumes no temporal structure at all. Stronger nulls preserve some temporal structure and test against that. Dirichlet imposes a parametric form, which is informative but adds assumption load. Permutation preserves the marginals exactly but destroys order, which means it cannot test against autoregressive nulls. Bootstrap with block resampling preserves local order but requires choosing a block length. Each of these is more careful than empirical-frequency, and each is more committal. We chose empirical-frequency for the packet to keep the assumption load minimal — but the result lives in the gap between "the protocol detected something" and "this is the right test." The right null is Q3.

**Repo pointer.** INV-051 entry in `ai-refresh/INVESTIGATION_CATALOG.json` documents the empirical-frequency null choice and notes the open follow-up.

---

## Q&A 2 — "INV-050: why TV and Aitchison together? What's the broader family?" (Q2 from Beat 8)

**Short answer (30 seconds).**
*"TV distance and Aitchison distance agree on the verdict — the protocol's same/different reading — across 101 datasets. INV-050 CANONICAL. Whether the agreement extends to weighted log-ratio, Mahalanobis on CLR, or Egozcue–Pawlowsky-Glahn evidence information distance is the open question. Suggestions on what to test next are welcome."*

**Long answer (90 seconds).**
Pair-invariance is the empirical observation that for each of 101 reference datasets, the protocol's classification — drift / no drift, deceptive / loud — is the same whether you compute TV distance or Aitchison distance as the structural-velocity proxy. That doesn't prove the verdict is metric-invariant in general; it only proves it for the pair we tested. The broader claim — that the verdict is invariant across the entire valid family of simplex distances — is what Q2 asks the community to help us bound. Candidates beyond TV and Aitchison include weighted log-ratio distances, the Mahalanobis distance on CLR coordinates, and the evidence information distance from Egozcue and Pawlowsky-Glahn. We have not tested those. If the community has experience with which family is the natural choice, we will run the protocol against it and report.

**Repo pointer.** INV-050 entry; `huf-gov/HUF_GOV_INTEGRATION.md` shows how this fits the broader governance.

---

## Q&A 3 — "Why those 5 countries and not the other 4?"

**Short answer (30 seconds).**
*"AUS, CHN, GBR, IND, JPN reproduce the signature. The four non-firing countries are interesting because they show the protocol discriminates. Germany at annual grain fires K-eff tightening but TV is above median — loud drift, not deceptive. The packet's monthly result is at a different grain. France is in a loosening regime — K-eff is rising as renewables join nuclear. USA is mostly stable. WLD aggregate smooths individual signatures."*

**Long answer (90 seconds).**
Deceptive drift requires two things — K-eff tightening (concentration increasing) and TV staying below median (structural velocity quiet). When both fire, the signature is deceptive — the composition is concentrating behind a calm surface. Germany at annual grain fires only the first half — K-eff tightens but TV is high — so the protocol classifies it as loud drift, not deceptive. The same Germany at monthly grain (the packet's headline) fires both, producing p = 0.0016. France's K-eff has been gradually rising — loosening, not tightening — so neither half fires. USA's composition is comparatively stable over the corpus window — neither tightening nor obviously moving — so neither half fires. WLD aggregates over the nine countries and the individual signatures wash out at the aggregate level — methodologically expected.

The fact that four countries don't fire is empirically important. A protocol that always fired would be useless. INV-051 says the protocol distinguishes.

---

## Q&A 4 — "Is this prior art?"

**Short answer (30 seconds).**
*"One of four search areas executed. The closest adjacent prior art is Morais, Thomas-Agnan and Simioni 2017/18 — compositional plus Dirichlet for market-share regression — and Arata and Onozaki 2017 — CoDa for market-share dynamics using ILR. Both thank Egozcue and Pawlowsky-Glahn. Neither combines all three conjuncts of MC-4. Three search areas remain pending. Pointers welcome."*

**Long answer (90 seconds).**
The prior-art search has four areas: (1) compositional change detection in industrial monitoring; (2) compositional time-series with carrier-level attribution; (3) compositional control charts; (4) compositional regime-change methodology. Area 1 was searched and produced the two papers cited. Areas 2, 3, 4 are pending. The community is more likely than I am to know what to read in those areas — if anyone has pointers, especially to non-English work, I am open.

The discipline I have applied: if the room produces a paper that combines all three conjuncts — Aitchison-native + formal change detection + carrier-level attribution — into one observable stack, MC-4 dies. We did not invent the geometry. We are claiming that this particular conjunction is new. Two papers come close but neither closes the gap. Three areas remain to search.

**Repo pointer.** `papers/codawork2026/talk/qa_bench/prior_art_defeat.md` has more depth on the search methodology. PRIOR_ART_SEARCH_TARGETS.md tracks the four areas.

---

## Q&A 5 — "Is this really a new monitoring category?"

**Short answer (30 seconds).**
*"We do not know. The work could be an application note within existing CoDa. The naming as a 'new monitoring category' is offered as one possibility, not asserted. The room's view matters here more than ours. Whichever shape the community chooses, we adapt."*

**Long answer (60 seconds).**
The phrase "Monitoring Category 4" inherits a naming convention from the HUF parent framework, which proposes a four-category schema MC-1 through MC-4. Inside Hs, we operationalize MC-4 through CNT v3.1.0 and CNQ v2.0.0. Whether the community sees this as a new category or as an application of existing CoDa methodology is genuinely open. We have no preconceived answer. The work stands either way — what matters is whether the protocol detects something useful, not whether it gets shelved under a new heading.

---

## Q&A 6 — "Reproducibility?"

**Short answer (30 seconds).**
*"Yes — fully. Apache-2.0 licensed engines, deterministic computation, hash-chained outputs, 25-experiment reference corpus with expected_results.json. content_sha256 and engine_signature on every page of every artifact. Anyone with the raw CSV can verify any plate in about two minutes. See REPRODUCIBILITY_CHECKLIST.md at the repo root."*

**Long answer (90 seconds).**
Both engines run deterministically — same input plus same engine version produces bit-identical output. Schema 3.1.0 (CNT) and schema cnq/2.0.0 (CNQ) are versioned. Cross-language parity is verified between Python and R ports at 1e-13 tolerance. Every output artifact carries content_sha256 (the hash of the canonical JSON) and engine_signature (the version-binding string). A reproducer downloads the repo, runs `python3 verify_publication_results.py`, and the determinism gate either passes (all 25 reference experiments match expected_results.json bit-for-bit) or it fails with named diff. Apache-2.0 licensing on the engines, CC BY 4.0 on the documents. Public on GitHub: github.com/PeterHiggins19/higgins-decomposition.

---

## Q&A 7 — "R-language version?"

**Short answer (15 seconds).**
*"Yes. cnt.R is at v3.0.0; cnq.R is at v2.0.0. Cross-language parity verified at 1e-13 tolerance. v3.1.0 R port matching the latest Python engine is queued for the first post-conference push window."*

---

## Q&A 8 — "What is EITT?" *(Q&A backstop — not on slides)*

**Short answer (45 seconds).**
*"Entropy-Invariant Time Transformer. A separate scientific contribution from the HUF companion repository. Claim: Shannon entropy is conserved under geometric-mean temporal compression for compositional carriers. Measured at 0.18 percent variation across a 341 to 1 compression ratio. Verified against six published case studies. It is the temporal-invariance sibling of MC-4's spatial-invariance — the geometric mean is to time what the Aitchison metric is to space."*

**Long answer (2 minutes if pressed).**
EITT operates on the same simplex but at a different layer. MC-4 says: compositional change detection is invariant under scale-equivalent metrics. EITT says: compositional entropy is invariant under temporal compression by the geometric mean. Together, they make the structural reading transferable across both spatial-metric choice and temporal granularity. Take an EMBER monthly series of 300 readings. Compute Shannon entropy. Take the geometric mean of every 25 readings — you now have 12 readings. Recompute Shannon entropy. The difference is below 0.5 percent. We tested this on Backblaze, GDP, OWID-Energy, Ramsar wetlands, Planck CMB, Toronto TTC, Energy mixes. Same result.

The geometric mean is the natural temporal operator for the simplex because it preserves the simplex constraint. It is also already known in the CoDa community as the simplex barycenter. EITT shows it has an entropy-conservation property that the literature had not previously published.

**Repo pointer.** `papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md` has the canonical Peter-confirmed explanation.

---

## Q&A 9 — "What about KILL-001?" *(Q&A backstop — not on slides)*

**Short answer (30 seconds).**
*"Published falsifiability artifact in the HUF companion repository. Nineteen named failure modes in five categories — wrong data, wrong question, wrong domain, wrong use, fundamental mathematical limits. Seven confirmed kills, four boundary conditions, five mathematical limits, two doctrinal violations, three degraded modes. Worst failure mode is KILL-3.3 — artificial carrier — which the framework cannot mechanically detect; only the domain expert can. We named it explicitly because a framework with no kill conditions is not science."*

**Repo pointer.** Higgins-Unity-Framework companion repo, `huf-gov/governance/KILL-001-kill-test.json`.

---

## Q&A 10 — "What's the governance angle?" *(Q&A backstop — not on slides)*

**Short answer (45 seconds).**
*"HUF Governance Charter — 9 articles published April 2026 in the companion repository — is the parent doctrine. Hs Change Control v1.0 is the working specialization for this fast-research codebase. Key principles: Open-Loop Priority (the instrument reads, the expert decides), Right to Interrupt (the human can always halt the system), Governed Breakpoint (every self-correction preserves an inspection point). We follow this discipline because the open-loop posture is what keeps the instrument honest. HUF-GOV protects judgment. HUF-CLS optimizes correction. The two are separated by design."*

**Long answer (2 minutes).**
The governance work is parallel to the scientific work — neither is on the slides because the talk is about the science. But for anyone who cares about *how* a small independent team produces this much output coherently, the apparatus is real and documented. The HUF Governance Charter is the doctrinal foundation. Hs Change Control v1.0 specializes it for fast-moving codebase work: an 8-rule doctrine (HCC-R001..R008), 6 severity classes (S0..S5), a Discovery Change Packet lifecycle (proposed → in_progress → implemented → verified → released), a Configuration Items registry, an Interface Control matrix, a Traceability Matrix, a Cross-AI Coordination apparatus, and an executable consistency checker. We ran the first end-to-end DCP cycle on 2026-05-12 (DCP-001). The breaker inventory (16 breakers) tested 2026-05-12 with 12 verified TRIPPED and 3 SOFT.

**Repo pointer.** `huf-gov/README.md` at the Hs repo root; full Charter in the HUF companion repository.

---

## Q&A 11 — "Can you walk me through a simple example?"

**Short answer (use the bread analogy — 60 seconds).**
*"Sure — bread. A loaf is a four-carrier composition: flour, water, salt, yeast. Each carrier has a job. The simplex constraint says they sum to one. K-eff reads how alive the dough is. TV reads how fast it's moving. The yeast is the active carrier — the component of power, the one that does work on the others. The baker holds the breakpoint — decides when the bread is done. The same instrument that reads electricity grids reads bread. We have a verbal narrative in the repository that walks the framework through a baking process end to end — useful for non-specialist audiences."*

**Repo pointer.** `papers/BREAD_THE_HS_WAY_2026-05-12.md` — full 1900-word memorisable verbal narrative.

---

## Q&A 12 — "Why a multi-AI collaboration?"

**Short answer (45 seconds).**
*"The HUF AI Collective — Claude, ChatGPT, Copilot, Gemini, Grok — is a cross-check mechanism. Five different architectures with five different failure modes triangulate on the same artifact. If one AI hallucinates a result, the other four catch it. Peter is the human routing layer that holds the doctrine and ratifies every binding decision. The Collective was the original cross-check protocol; Hs Change Control v1.0 specializes it for codebase work. Five reviews across the conference-prep arc validated the talk material."*

---

## File metadata

- **Document version.** 1.0 — baseline authoritative version, consolidated from five separate bench cards
- **Supersedes.** `papers/codawork2026/talk/qa_bench/` (multi-file source preserved as lockdown snapshot)
- **Lockdown compatibility.** S2 doc-only addition

---

## AI Use Declaration

In accordance with established scientific community standards (ICMJE, COPE, Nature, Science, WAME, EU AI Act 2024, arXiv, ACM, IEEE) this work discloses AI assistance. **AI tools used:** Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI) — the HUF AI Collective. **Tasks:** drafting Q&A short and long answers; cross-checking technical claims against the catalog; consolidating five separate May-12 bench cards into a single document. **Author responsibility:** the author retains full responsibility; all answers have been reviewed and verified. AI tools are not authors. **Governance:** HUF AI Collective cross-check protocol. **Dates:** March 2026 – May 2026. **Standards reference:** HUF-STD-001.

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
*Q&A is part of the talk, not an appendix to it.*
