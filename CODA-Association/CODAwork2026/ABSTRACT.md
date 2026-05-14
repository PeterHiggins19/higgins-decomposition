# Abstract — CoDaWork 2026

**Document version:** 1.2
**Document status:** authoritative
**Created:** 2026-05-12 (v1.0); **Revised:** 2026-05-13 (v1.1 — added version header; tightened technical detail). **Revised:** 2026-05-13 (v1.2 — AI assistance moved from byline to AI Use Declaration section per HUF-STD-001).
**Conforms to:** HUF Publication Standards (HUF-STD-001) — `../../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json`

**Title.** Compositional monitoring of energy-mix drift on the simplex.

**Speaker.** P. Higgins, Rogue Wave Audio.

**Talk slot.** 15 minutes + Q&A.

---

A country's electricity mix is a vector of carrier shares that sums to one. It sits on a simplex; it obeys the Aitchison geometry the CoDa community has built over four decades. We present a compositional change-detection protocol that reads this geometry natively and discriminates among three archetypes of structural change — abrupt external (Japan, 2011), policy-driven abrupt (UK coal exit), and policy-driven continuous (Germany, the headline case).

The central falsifiable claim is **MC-4**: that no existing monitoring framework combines all three of *natively in Aitchison geometry*, *with formal change detection*, *at the carrier level* — into one observable stack. The protocol uses standard CoDa operators (closure, CLR, Helmert-ILR, Aitchison distance, perturbation) together with two small supporting metrics — TV distance (structural velocity) and K-eff (concentration). Trajectory operators (helmsman family, pairwise bearing, depth tower, IR class) are first-class objects in the algebra, computed alongside the classical plates.

**Validation across the 9-country EMBER 2001–2025 corpus:** INV-050 establishes TV/Aitchison metric-invariance across 101 datasets (CANONICAL). INV-051 reports that the deceptive-drift signature fires in 5 of 9 countries — AUS, CHN, GBR, IND, JPN — and does *not* fire in DEU at annual grain, FRA, USA, or WLD (CANONICAL). The protocol discriminates; it does not over-fire. The Germany headline at monthly grain reports p = 0.0016 computed against the series' own empirical-frequency baseline, **with the null-model caveat displayed on the slide:** this is a weaker null than a Dirichlet, permutation, or bootstrap null.

The deeper algebraic structure is captured by **twin-quaternion factoring at D=8 (INV-029 CANONICAL)**, verified at IEEE machine floor (3.33e-16 + 2.22e-16 residuals) on real EMBER China data, and the **CHSH joint-coherence diagnostic (INV-035 CANONICAL)** at 0.88, well within the Tsirelson bound. Three independent IEEE-floor confirmations on unrelated datasets (Backblaze D=4, Planck CMB D=4, SM neutrino D=3) suggest a hardware-precision floor rather than algorithmic noise.

**The discipline.** Engines are deterministic and hash-chained: raw CSV → CNT v3.1.0 / CNQ v2.0.0 engine → canonical JSON → 4-stage atlas (PDF + HTML), with content_sha256 and engine_signature embedded in every page. Cross-language parity (Python + R) is verified. **Anyone with the raw CSV can verify any plate in ~2 minutes.** Twenty-five reference experiments form the determinism gate (all pass). The KILL-001 falsifiability artifact names 19 ways the framework breaks; the work is offered to the room as inspectable, falsifiable, and citable.

**What we ask the room.** Three open questions — Q1: concentration vs Aitchison norm; Q2: the right family of simplex distances for verdict-invariance testing; Q3: the right null model for compositional change-point. We will adopt the community's recommendation and rerun. **A defeater must combine all three conjuncts.** Two preempted defeat paths (Metric → INV-050; Case → INV-051) and two open paths (Prior-art — Morais, Thomas-Agnan & Simioni 2017/18 and Arata & Onozaki 2017 are the closest adjacent prior art found; three more areas pending; Category — application-note vs new monitoring category, no preconceived answer).

The talk is an ascent waypoint, not the summit.

---

## At a glance

| Item | Value |
|---|---|
| Corpus | EMBER, 9 countries, 2001–2025, 9 carriers (coal, gas, oil, nuclear, hydro, wind, solar, bioenergy, other) |
| Engines | CNT v3.1.0 (schema 3.1.0), CNQ v2.0.0 (schema cnq/2.0.0) |
| Languages | Python + R parity-verified |
| Headline result | Germany p = 0.0016 (monthly grain, empirical-frequency null) |
| Cross-country reproduction | 5 of 9 (AUS, CHN, GBR, IND, JPN) — INV-051 CANONICAL |
| Metric invariance | TV / Aitchison pair across 101 datasets — INV-050 CANONICAL |
| Algebraic structure | Twin-quaternion D=8 IEEE-floor verified — INV-029 CANONICAL |
| Joint coherence | CHSH 0.88 (Tsirelson 2√2 bound) — INV-035 CANONICAL |
| Falsifiability | KILL-001 — 19 named failure modes (HUF, published 2026-03-23) |
| Determinism gate | 25 reference experiments, all pass |
| Repositories | github.com/PeterHiggins19/higgins-decomposition + Higgins-Unity-Framework |
| License | Apache-2.0 (engines) + CC BY 4.0 (documents) |

---

## Citation

Higgins, P. (2026). *Compositional monitoring of energy-mix drift on the simplex.* CoDaWork 2026 — 11th International Workshop on Compositional Data Analysis. Coimbra, Portugal, 1–5 June 2026.

---

## AI Use Declaration

In accordance with established scientific community standards for transparency in AI-assisted research — ICMJE, COPE, Nature/Springer, Science/AAAS, WAME, EU AI Act (2024), arXiv, ACM, and IEEE — this work discloses the following AI assistance.

**AI tools used:** Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI). Collectively referred to in HUF documentation as the HUF AI Collective.

**Tasks performed by AI:** drafting of supporting documents and abstract text; editing and consistency-checking; cross-checking of claims across documents; literature-search assistance for prior-art areas; falsifiability-condition enumeration (KILL-001); slide-deck generation and design QA; adversarial review for overclaim detection and drift catching across the conference-preparation arc.

**Author responsibility:** The author retains full responsibility for all scientific claims, data interpretation, methodological choices, and conclusions presented in this work. All AI-generated content has been reviewed, verified, and where necessary corrected by the author. AI tools are not listed as authors and do not meet authorship criteria under ICMJE, COPE, Nature/Springer, Science/AAAS, WAME, ACM, or IEEE standards.

**AI use governance:** AI assistance is operated under the HUF AI Collective cross-check protocol — a multi-AI methodology in which any single AI's finding is subjected to adversarial review by the other AIs in the Collective before being adopted by the author. Final binding decisions route through the human author. Protocol documented in the HUF Governance Charter (Articles II–IV) and the SAFE-001 cognitive-agent safety doctrine. Falsifiability constraints documented in KILL-001 (19 named failure modes).

**Dates of use:** March 2026 – May 2026 (conference-preparation arc).

**Standards reference:** HUF Publication Standards v1.0 (HUF-STD-001) — `../../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json`

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
