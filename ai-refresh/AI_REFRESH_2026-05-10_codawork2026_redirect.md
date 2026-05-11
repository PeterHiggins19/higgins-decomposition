# AI Refresh — 2026-05-10 — CodaWork 2026 priority redirect

**Date:** 2026-05-10
**Push:** #36 (sweep + planning)
**Audience:** any AI session resuming Hs / CoDaWork 2026 work between now and 1 June 2026
**Status:** **active priority** — supersedes prior CoDaWork strategic agendas

---

## Summary in one paragraph

The CoDaWork 2026 conference programme is set. The accepted abstract on **page 25 of the official book of abstracts** is "Compositional monitoring of energy-mix drift on the simplex" — Germany, Japan, UK, EMBER 2000–2025, perturbation + Aitchison distance + concentration measure. We previously offered a broader instrument paper to Prof. Egozcue (`CoDaWork2026_Letter_and_Revised_Abstract.md`); he declined and steered us back to the original. The conference talk **must honor the original abstract**. The matured CNT v3 / CNQ v2 engines, CRD-1.0 doctrine, and 101-dataset reference suite are **depth/Q&A material, not headline material**. The master plan lives at `papers/codawork2026/planning/CONFERENCE_2026_06_PLAN.md`. Read that first.

---

## Why this matters for any AI session resuming the work

Prior planning documents in `papers/codawork2026/` describe a broader instrument-paper version of the talk that the conference declined. An AI session that walks in cold and reads the strategic-agenda or speech files **without reading the planning folder will pivot in the wrong direction**.

Specifically, do **not** plan around:

- "The Higgins Decomposition: a deterministic compositional diagnostic on the Aitchison simplex" (the broader title — superseded; deferred to journal track)
- 25 systems × 18 domains as the headline (depth/appendix only)
- Full Hˢ extension stack (κ^HS, IR taxonomy, helmsman family, depth tower, twin-quaternion factoring) as the lead (none of these are in the accepted abstract)
- The four binding doctrines (SEA-1.0, STP-1.0, CRD-1.0, engine-independence) as headline content (Q&A material)
- CNQ as a tier presented to the audience (CNQ is not mentioned in the abstract)

Do plan around:

- **Energy-mix drift detection** as the explicit topic
- **DEU, JPN, GBR as the headline narrative** (the abstract's three; the named transitions live there)
- **All countries on stage** as the wider scope (Peter's directive 2026-05-10): all EMBER 8 (USA, CHN, DEU, FRA, GBR, IND, JPN, WLD) + all 73 OWID country trajectories. Australia (AUS) still needs adding to EMBER pipeline — task 5.3.K in the master plan
- **2000–2025** as the period (EMBER 2025 release is the headline data update)
- **MC-4** as the formal claim name: "no prior monitoring framework tracks compositional market share at the carrier level with formal change detection" — falsifiable
- **Headline operators**: perturbation + Aitchison distance (CoDa-canonical from the published abstract); **packet operators**: TV distance (½ Σ|ρᵢ(t)−ρᵢ(t−1)|, half-L1 bounded [0,1]) + K_eff = exp(Shannon H) for effective number of categories. Both stacks must appear in the slides; they agree on shock hit/miss verdicts
- **Deceptive drift** as the signature concept: internal redistribution within an apparently stable whole; Germany pre-2022 gas crisis with **p = 0.0016** (with the explicit null-model caveat the packet itself flags)
- **Three named transitions**: Japan post-Fukushima 2011–2012 spike; Germany continuous trajectory toward renewable vertex; UK coal exit as abrupt regime change
- **One open question for the community**: relationship between concentration measure (K_eff = exp(H)) and Aitchison norm
- **Four defeat paths** (the falsifiability conditions named in the abstract): prior-art / metric / case / category. From Part II of the HUF MC-4 packet
- **Two repository links**: the submission origin `github.com/PeterHiggins19/Higgins-Unity-Framework` (HUF) and the production engine home `github.com/PeterHiggins19/higgins-decomposition` (Hs). Both public; both audience-facing
- **The Appendix A self-discipline note**: L2 → TV metric correction caught during ChatGPT corpus review March 22, 2026 — this is a feature aligned with SEA-1.0 anti-spec doctrine, not an embarrassment

---

## What you should do first

1. **Open `papers/codawork2026/planning/CONFERENCE_2026_06_PLAN.md`** — the master plan. Read sections 1, 2, 4, 5 before any other action.
2. **Open `External_Published_Papers/book-of-abstracts-codawork-2026-draft.pdf` page 25** — the verbatim abstract. This is the binding document.
3. **Open `papers/codawork2026/CoDaWork2026_Reply_to_Egozcue_Final.txt`** — the published correspondence record showing the redirect.
4. **Skim `papers/codawork2026/CoDaWork2026_Energy_Briefing.md`** — the 2025–2026 energy headlines that justify the live-data angle.
5. **Reference `papers/codawork2026/conference_2026_06/COMPARISON_v2_0_4_vs_v3_0_0.md`** — the per-country numbers on the new engines.

---

## Mapping older documents → current relevance

| Older artefact | Current relevance |
|---|---|
| `CoDaWork2026_Letter_and_Revised_Abstract.md` | Superseded. Save for the post-conference journal submission. |
| `CoDaWork2026_Strategic_Agenda.md` (April 27) | Pre-redirect. Some structural ideas still useful (gift ramp, 7-beat narrative) but the headline thesis was the broader paper, which is no longer the talk. **Read with caution.** |
| `CoDaWork2026_Speech_GiftRamp.md` | The "gift ramp" *form* is still good (16 slides; system speaks 80%, presenter 20%). The *content* needs to be recast around the energy-mix drift abstract, not the broader instrument paper. |
| `CoDaWork2026_Refined_Abstract.md` | The 282-word internal-presentation version of the published abstract. Wording polish, not a published change. Use it for the talk's framing language. |
| `CoDaWork2026_Energy_Briefing.md` | **Still highly relevant.** The 2025–2026 energy headlines are exactly what makes the live-data angle compelling. |
| `CoDaWork2026_Future_Path.md` | Post-conference roadmap — read after the conference, not before. |
| `Hs_CoDaWork2026_Executive_Summary.md` | Mixes scopes; needs editing to match the published abstract (task 5.3.G). |
| `papers/codawork2026/CoDaWork2026_Presentation.pptx` (v1, 12 slides) | Needs rebuild to ~16 slides matching the master plan §5.1. |
| `HCI-CNT/conference_demo/talk_deck/CodaWork2026_CNT_Talk.pdf/.pptx` | Push #19 era; CNT-tier-specific. Useful as a depth reference, not the headline deck. |
| `papers/codawork2026/conference_2026_06/` (the corpus run) | **Production source for the headline figures.** Pull from `per_country/ember_deu`, `ember_jpn`, `ember_gbr` STAGE_1_REPORT.md and cnt_v3.json. |
| `experiments/2026-05-10_full-corpus-validation/` (101 datasets) | **Q&A depth.** Don't put on stage. Walk to it if asked "does this generalise beyond energy?" |
| `EXPERIMENTS_JOURNAL.md` | **Q&A depth.** Walk to it if asked about the system's lineage. |

---

## Concrete priorities for the next 3 weeks

In order of urgency (full table in master plan §5.3):

1. **Verify the Japan 2011–2012 perturbation spike is visible** in `conference_2026_06/per_country/ember_jpn/STAGE_1_REPORT.md` step-Δ Aitchison distance column. If not, refine the report to highlight it.
2. **Generate per-country drift figures** for DEU, JPN, GBR — step-Δ over time + simplex trajectory rendering.
3. **Rebuild the slide deck** to the 9-beat headline structure (master plan §5.1). 16 slides target.
4. **Wire `Hs_Standards_Edition.ipynb` to CNT v3** (currently uses 12-step pipeline) — for the optional live demo.
5. **Confirm AV setup** with the conference organisers (HDMI at lectern, own laptop allowed, poster dimensions). Asked in the original submission letter; response unclear.
6. **Recover and document the four falsifiability conditions** mentioned in the published abstract.
7. **Prepare R-language reproducibility** answer for Q&A — Egozcue noted the CoDa community works primarily in R; CNT v3 has a cnt.R port (push #32) and the per-field parity contract holds.

---

## Files I created today (for cross-reference)

- `papers/codawork2026/planning/CONFERENCE_2026_06_PLAN.md` — the master plan
- This file (`ai-refresh/AI_REFRESH_2026-05-10_codawork2026_redirect.md`) — the AI-refresh redirect

Following deliverables (planned, not yet written):

- `papers/codawork2026/planning/INVENTORY.md` — full per-file CodaWork-asset inventory
- `papers/codawork2026/planning/ABSTRACT_TO_CNT_V3_MAP.md` — line-by-line abstract-to-engine-output mapping
- `papers/codawork2026/planning/FALSIFIABILITY_CONDITIONS.md` — the four conditions named in the abstract
- `papers/codawork2026/planning/DELIVERABLE_BUNDLE.md` — the must-exist-by-2026-05-26 list

---

## What this redirect implies for engine-side work

Push #34 + #35 corpus expansion (101 datasets across 11 domains) and EXPERIMENTS_JOURNAL.md are **stockpile depth** — the matured framework that stands behind the energy-mix drift presentation. They are the receipts the audience can fetch if they want more. They are not the talk.

The four binding doctrines (SEA-1.0, STP-1.0, CRD-1.0, engine-independence) similarly **support** the talk — every diagnostic in the talk is hash-chained, every multi-carrier comparison is coherent-range-policy compliant, every claim has an enumerated failure mode behind it. But the audience asked for energy drift, and energy drift is what they get.

**Discipline test:** if any presentation slide names a doctrine ID, an engine version, or a non-energy domain in its headline (not in a supporting line at the bottom), it is off-message and should be rewritten.

---

*Active until: 2026-06-05 (end of the conference). After the conference, this redirect retires; planning shifts to the journal-track manuscript carrying the broader instrument paper to its venue.*
