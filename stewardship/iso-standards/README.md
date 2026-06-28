# ISO standards pursuit — MC‑4, the missing fourth monitoring category

*The basics of the HUF↔ISO positioning. Distilled from `MC4_ISO_Positioning_Document.docx` (Higgins, April 2026, prepared for CoDaWork 2026; target audiences ISO/TC 69, Ramsar Secretariat, CoDa community). A **proposal**, not an accepted standard — interest expressed, never acquired. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001.*

---

## The gap, in one table

Three of the four monitoring questions are already well served by international standards. The fourth has no home.

| Category | Question | ISO standard(s) | TC/SC | Status |
|---|---|---|---|---|
| **MC‑1 Magnitude** | How much? | ISO 17025, GUM (JCGM 100) | TC 69 / SC 6 | Mature |
| **MC‑2 Identity** | What is it? | ISO 22400, ISO 5725 | TC 69 / SC 6 | Mature |
| **MC‑3 Trend** | Which direction? | ISO 7870, ISO 7966, ISO 22514 | TC 69 / SC 4 | Mature |
| **MC‑4 Composition** | What is the internal balance? | — | — | **GAP** |

No ISO standard addresses the monitoring of **proportional balance among the parts of a system** — whether a portfolio is diversified, an ecosystem resilient, or a grid transitioning safely. The absence isn't an oversight; it reflects a historical assumption that compositional structure is a *derived* property, not a *primary* observable.

## The argument

A system can satisfy **MC‑1** (all quantities within tolerance), **MC‑2** (all parts correctly identified), and **MC‑3** (all trends stable) while its **internal proportional balance silently degrades.** That is the blind spot existing standards cannot detect — *ratio blindness.* MC‑4 (Composition Monitoring) names and fills it.

The mathematics is **not new**: it is four decades of Aitchison's Compositional Data Analysis (1982) — the geometry of constrained, proportional data on the simplex, where ordinary Euclidean statistics give systematically wrong answers. The CoDa community already built the geometry, the transforms (CLR, ILR), and the statistical methods. **What has been missing is the operational and institutional scaffolding** to deploy that mathematics as a formal monitoring standard — and the deterministic instrument (Hˢ / CN‑TT) that makes a composition read reproducible and auditable.

## The honest scope line

*The mathematics is standard CoDa‑compatible geometry; the new contribution is the deterministic monitoring instrument and the proposal to recognise composition as a fourth standardisable category.* MC‑4 is **recognition, not invention** — and today it is a **proposal**: there is no ISO work item, no committee engagement, no endorsement. The role of the CoDa community would be as the mathematical foundation; the role of Hˢ is to supply a deterministic, hash‑chained reference instrument so a standard could be written against something reproducible.

## Where the pursuit goes (Tier 3, to earn)

A genuine pathway would mean engaging ISO/TC 69 on the merits, with empirical evidence and a reference implementation, and letting the standards process decide. Nothing here is initiated; this folder records the **basics of the purpose** so a future engagement starts from an honest map.

**Source (full):** `../../../HUF/science/coda-monitoring/MC4_ISO_Positioning_Document.docx` · **doctrine:** `../../../HUF/huf-gov/doctrine/HUF_GOV_OPERATING_DOCTRINE_2026-06.md` §4 (MC‑4) · `../../../HUF/huf-gov/RATIO_BLINDNESS_DOCTRINE.md`.

*The instrument reads. The expert decides. A standard is written against what can be reproduced.*

---

## Update — 2026‑06‑14: the missing piece now exists

This root named the missing element as *"the deterministic instrument that makes a composition read reproducible and auditable."* That instrument is now built and demonstrated. The realistic strategy — the function/IEEE‑754 reproducibility framing, the wedge of extending MSA/GUM rather than proposing a new philosophy, the four‑leg evidence portfolio, and an honest ladder of where the project stands — is written up in **`PATH_TO_A_STANDARD.md`** (this folder). Supporting current doctrine, now integral to this pursuit: `../../HCI-CNTT/DETERMINISM_GAUGE_RR_AND_CONFIDENCE.md` (engine gauge R&R ≈ 0, conformance), `../../HCI-CNTT/DESIGN_PHILOSOPHY_THE_EXPERT_ENGINE_AND_THE_GUARDS.md`, and the `../../onramp/` PhD onramp (the consensus flywheel). Still a proposal; still Tier 3; still nothing initiated.
