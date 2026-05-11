# Prior-art search targets — Prior-art defeat path for MC-4

**Companion to:** `EXTERNAL_REVIEW_INVITE.md` and `NAMED_FINDINGS_FOR_CODA_DISCUSSION.md`
**Created:** 2026-05-10 (push #39, claim-sharpening pass)
**Status:** open work item — search to be conducted before 2026-06-01 (conference start)
**Purpose:** specific literature areas to chase for the **Prior-art defeat** path. If anything in these areas already combines all three MC-4 conjuncts (Aitchison-coherent + formal change detection + carrier-level), the MC-4 claim should be narrowed or restated.

---

## The MC-4 claim (sharpened push #39)

> *No monitoring framework in the energy / market-share literature operates **natively in Aitchison geometry** with **formal change detection** at the **carrier level** — the three conjuncts combined into one observable stack. A defeater must overturn the conjunction, not just one disjunct.*

A successful prior-art defeat needs all three conjuncts in one piece of prior work. Partial matches (e.g., Aitchison-coherent + carrier-level but without formal change detection) narrow the claim but do not kill it.

---

## Areas already canvassed (in EXTERNAL_REVIEW_INVITE.md)

| Candidate | Match status | Reason |
|---|---|---|
| Aitchison 1982/1986 | partial — first conjunct only | Foundational simplex geometry, but compositionality framed as a *statistical condition to handle*, not as a *monitoring observable to read directly* |
| Egozcue & Pawlowsky-Glahn 2018 | partial — first conjunct only | Evidence information distance; scale-invariance theory; not framed as monitoring |
| Standard market-share monitoring in econometrics | partial — second and third conjuncts only | Magnitude-based change detection at the carrier level, but not Aitchison-coherent |
| Diversity indices (Shannon, Herfindahl-Hirschman) | partial — first and third conjuncts | Single-point concentration measurement; not framed as drift detection over time |

None of these is a full three-conjunct match. The search below targets areas where a full match is most likely to be lurking.

---

## Four targeted search areas

### Area 1 — CoDa time series specifically

This is the area where a hidden full match is most likely. The CoDa community has worked on time series of compositions for a decade-plus; if any group framed it as "monitoring with formal change detection," we need to find them and cite.

**Specific work to chase:**

- **Egozcue & Jarauta-Bragulat (2014)** — "Hilbert-space methods for time series of compositions." *Compositional Data Analysis VI*, Geological Society of London. Likely the most adjacent published reference — frames CoDa time series formally but may or may not include change-point detection.
- **Pawlowsky-Glahn, Egozcue & Tolosana-Delgado** — compositional ARIMA (CoDA-ARIMA) work; should appear in *Modeling and Analysis of Compositional Data* (Wiley, 2015) and follow-up papers.
- **Geir-Atle Fonnum and colleagues** — Norwegian school on compositional time series in fisheries / ecology contexts.
- **Coda4Microbiome, CoDaCoRe** and related software ecosystems — if any of these tools include a "change point" or "shift detection" routine, that's a direct hit.

**Search strategy:** Google Scholar query `("compositional time series" OR "CoDa time series") AND ("change point" OR "change detection" OR "regime change" OR "structural break")` filtered 2010-2026. Cross-reference against Egozcue's publication list.

### Area 2 — Industrial ecology and material flow analysis (MFA)

Material flow analysis tracks compositional shares of materials through industrial systems and uses formal accounting balances. Some MFA work uses change-point detection.

**Specific work to chase:**

- **Eurostat MFA accounts** — official EU methodology for tracking material composition over time. Does the formal methodology include compositional change detection?
- **UNEP International Resource Panel** — annual material flow reports. Change methodology?
- **Brunner & Rechberger** — *Handbook of Material Flow Analysis* (CRC Press). The canonical MFA textbook; check chapters on temporal analysis.
- **Industrial Ecology journal** — recent decade for "compositional" + "drift" + "monitoring."

**Why this might match:** MFA is *explicitly* about compositional shares. The framing is different (mass-balance accountancy rather than statistical monitoring) but the underlying objects are compositions on the simplex. If any MFA paper computes Aitchison-coherent distances over time *and* applies formal change detection, that's a full match.

**Search strategy:** Google Scholar query `"material flow analysis" AND (Aitchison OR "log-ratio" OR "simplex") AND ("change" OR "drift" OR "monitoring")`. Cross-reference against the Journal of Industrial Ecology and Resources, Conservation & Recycling.

### Area 3 — Diet composition and nutrition surveillance

Compositional surveillance of dietary patterns over time is a well-developed area in public health. NHANES, EPIC, and similar cohort studies track macronutrient share compositions formally.

**Specific work to chase:**

- **NHANES (National Health and Nutrition Examination Survey)** methodology — does the surveillance protocol include compositional change detection in the Aitchison sense?
- **EPIC (European Prospective Investigation into Cancer and Nutrition)** — diet pattern monitoring over decades.
- **Compositional Dietary Patterns literature** — search for groups using ILR or CLR coordinates on dietary data with change detection.
- **Walter Willett group (Harvard) + Frank Hu** — recent papers on temporal trends in dietary composition.

**Why this might match:** Dietary surveillance is *explicitly compositional* (macronutrient shares sum to 100% of energy intake), *explicitly per-carrier* (carbs/fats/protein/alcohol/other), and frequently uses formal statistical methods for temporal change. If any nutrition-surveillance group uses Aitchison-coherent metrics with change-point testing, that's a full match.

**Search strategy:** Google Scholar query `("dietary composition" OR "diet composition") AND (Aitchison OR "log-ratio") AND ("temporal" OR "change" OR "trend")`. Cross-reference against the Journal of Nutrition, American Journal of Clinical Nutrition.

### Area 4 — Sectoral allocation in macroeconomics — **PARTIALLY EXECUTED (push #41)**

**Status update 2026-05-10:** Grok round-4 cross-check executed this search and returned **two real, citable papers** as the closest adjacent CoDa work on market-share dynamics. Catalogued as **INV-053** (CANONICAL, push #41). Full Grok session transcript at `ai-refresh/cross_check_archive/grok_round_4_session_2026-05-10.md`.

**The two hits:**

1. **Morais, Thomas-Agnan & Simioni (2017/2018)** — *"Using compositional and Dirichlet models for market share regression."* Economic Modelling. Explicitly thanks Egozcue and Pawlowsky-Glahn for CoDa techniques. Compares CoDa approaches (including ILR) against traditional market-share regression models.
2. **Arata & Onozaki (2017)** — *"A Compositional Data Analysis of Market Share Dynamics."* Evolutionary and Institutional Economics Review. Uses the ILR transformation (Egozcue et al. 2003) to analyse how market shares evolve over time.

**Conjunction test:** Neither paper combines all three MC-4 conjuncts (Aitchison geometry + formal change-point detection + carrier-level attribution into one observable monitoring stack). Both are partial matches — first conjunct fully present, third conjunct partially present (regression/dynamics framing rather than monitoring); second conjunct (formal change detection) **absent in both**.

**Outcome:** **MC-4 survives Area 4 search with narrowing recommendation.** The talk's Beat 9 (defeat paths) should now name Morais et al. and Arata & Onozaki as the closest adjacent work the framework has been pressure-tested against. Generous citation in the talk is appropriate; the framework's distinct contribution is the *conjunction* of all three conjuncts in one observable stack, which these adjacent works do not provide.

**Original (pre-execution) area description preserved for the record:**

Share of GDP by sector tracked compositionally is a classical macroeconomics topic. Kuznets-era and modern work on sectoral transitions (agriculture → manufacturing → services) is voluminous.

**Specific work to chase:**

- **Kuznets (1971)** — *Economic Growth of Nations*. Foundational compositional treatment of sectoral GDP shares.
- **Acemoglu & Guerrieri** — capital deepening and sectoral reallocation work; potentially relevant for the methodology.
- **Herrendorf, Rogerson & Valentinyi (2014)** — Handbook of Economic Growth chapter on structural transformation. Reviews compositional methods.
- **WIOD / OECD-STAN sectoral databases** — methodology documents for tracking compositional change in GDP shares; do they use Aitchison-coherent methods?

**Why this might match:** Sectoral allocation is *explicitly compositional* (sector shares of GDP), tracked over multi-decade horizons, with extensive formal methodology. If any macroeconomic paper uses Aitchison-coherent monitoring with formal change detection, that's a full match.

**Search strategy:** Google Scholar query `("sectoral composition" OR "GDP composition" OR "structural transformation") AND (Aitchison OR "log-ratio" OR "simplex") AND ("change" OR "transition")`. Cross-reference against the Quarterly Journal of Economics, Review of Economics and Statistics.

---

## Process for any hits found

If a hit is found in any of these areas:

1. **Verify the three conjuncts are all present** in the cited work — read the methods section, not just the abstract.
2. **Catalogue the citation** as a new INV entry (CANONICAL if it survives MC-4; FALSIFIED if MC-4 was the wrong claim).
3. **Decide on narrowing or retraction**: if the prior work covers MC-4 explicitly, the MC-4 claim is killed and we restate ("MC-4 in the energy domain specifically..." or similar).
4. **Update the Beat 2 slide and the Beat 9 defeat paths** to reflect the prior-art finding before the conference.
5. **Acknowledge the prior work generously** in the talk — discovering you've been scooped is a normal scientific outcome and naming the prior work clearly is the right response.

---

## What "no full match" looks like

If a search across all four areas + any community pointers received at the conference returns **no full three-conjunct match**, the MC-4 claim survives a serious pre-conference stress test. The talk's Beat 2 + Beat 9 then stand as written.

In that case, the most honest framing is: *"We have searched these specific areas; we have not found a full match; the room is now invited to find one. If the room finds one, the claim is killed, and that is the right outcome."*

---

## Timeline

| Date | Step | Status |
|---|---|---|
| 2026-05-10 | Area 4 partially executed via Grok round 4; INV-053 catalogued; two real citations found | **DONE** |
| 2026-05-11 → 2026-05-25 | Active search across the remaining three areas (CoDa time series; industrial ecology / MFA; diet-composition surveillance) | pending |
| 2026-05-26 | Decision point: any further hits to narrate? | pending |
| 2026-05-30 | Beat 2 and Beat 9 slide content frozen | pending |
| 2026-06-01 → 2026-06-05 | Conference; community pointers integrated into Q&A | pending |
| 2026-06-06 onward | Catalogue community pointers; update post-conference manuscript | pending |

---

*This document is the open-work-item ledger for the Prior-art defeat path. It retires the day MC-4 is either confirmed defeated or confirmed surviving against the community's pressure.*
