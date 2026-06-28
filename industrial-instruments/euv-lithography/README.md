# EUV lithography × Hˢ — reading the most advanced process on Earth as a composition (INTERNAL · PLANNING)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑24. Promoting a
**long‑standing repo seed** — EUV lithography has been a listed Tier‑2 candidate application since the Higgins
Operator H₁ paper (Feb 2026, `ARC_OF_DISCOVERY.md` §5) — into a **built, receipted experiment**. **No contact,
partnership, or endorsement with any equipment maker, foundry, or research institute is implied or sought** —
this reads the *public physics* of EUV. Honest‑broker tiered; nothing posted; Peter is the sole gate.*

---

## Why EUV, why now

EUV is where everything this project just built converges in one machine. The 13.5 nm light is made by a
**laser‑produced plasma** — a high‑power CO₂ (or 2 µm) drive laser vaporizing tin microdroplets at ~100 kHz¹ ² —
so the source itself is a *laser + droplet + plasma composition*, and its **coherence/stability** is the
yield‑limiting variable. The printing limit is **stochastic**: at 13.5 nm (~91.8 eV/photon) only a limited number
of photons land per feature, so outcomes follow **photon shot noise** (Poisson), and failures appear as a
**two‑sided cliff** — missing/broken contacts when under‑dosed, bridging/merging when over‑dosed.³ ⁴ ⁵ That is a
*composition* `{OK, missing, bridge}` whose **ratios** move with dose long before the total failure count crosses
a yield spec. Hˢ was built for exactly this.

## The built result (the planning anchor)

*Measured (`euv_stochastic_drift.py`, receipt `877516b6`):* a deterministic, analytic Poisson model of the
two‑sided stochastic cliff under a slow downward dose drift (1.000 → 0.975 over a 100‑wafer lot). Hˢ reads the
defect composition `{OK, missing, bridge}` and flags the **silent ratio drift at wafer 7** — while the total
stochastic defectivity is still ~0.006 ppm — whereas the single‑channel "total‑NOK crosses 0.1 ppm" yield alarm
only fires at **wafer 69**: a **62‑wafer lead**. And because the cliff is two‑sided, the arrow is a **directional
helmsman** — it points to *missing/broken → steer dose UP* (or *bridge/merge → steer dose DOWN*), telling the
operator not just *that* dose is drifting but *which way to correct it*. (Lead time scales with the spec and the
drift rate; the point is that the ratio is a leading indicator of the cliff.)

## The four EUV objects Hˢ reads

| on the EUV line | the composition / exact object | the value |
|---|---|---|
| **stochastic printing** | defect‑class composition `{OK, missing, bridge, merge, broken}` | silent ratio drift + a *directional* dose helmsman, before yield drops |
| **source (LPP)** | drive‑laser + droplet + plasma budget; dose per pulse | common‑mode rejection of drive‑laser drift (the coherence law); live source‑coherence health |
| **dose / CD uniformity** | CD field‑map as a composition / deformation field | intra‑field uniformity read as rotation⊕shape⊕size |
| **defect inventory (AOI/e‑beam)** | lot defect signature in motion | which stochastic mode is rising across wafers — the conductor across the lot |

## What's in this folder

| file | what it holds |
|---|---|
| [`CONCEPT_AND_MATH.md`](CONCEPT_AND_MATH.md) | the physics → composition mapping: shot noise, the two‑sided cliff, source‑as‑composition, the coherence/dose link |
| `euv_stochastic_drift.py` | the receipted demo (the 62‑wafer silent‑drift lead, directional arrow) — needs `numpy`, `scipy` |
| [`RESULTS_euv_stochastic.md`](RESULTS_euv_stochastic.md) | the run, the numbers, the honest fences |
| [`INDUSTRY_IMPACT_AND_OFFERING.md`](INDUSTRY_IMPACT_AND_OFFERING.md) | impact, how it's offered, injection method, refinement roadmap, metrics, **Canada's part** (packaging/test/photonics — Bromont/C2MI) |
| [`POLITICAL_COMPOSITION_AND_EXPORT.md`](POLITICAL_COMPOSITION_AND_EXPORT.md) | **INTERNAL · GOVERNANCE · NOT FOR PUBLICATION** — the political composition of the field, the export question, principle‑vs‑how‑to, defer‑sensitive‑release‑upward |
| [`OFFER_TO_CANADA_AND_PUBLIC_SCIENCE.md`](OFFER_TO_CANADA_AND_PUBLIC_SCIENCE.md) | **DRAFT · INTERNAL** — the resolved disposition: publish the science to the world; offer the applied head‑start to the Government of Canada to steward for Canadian + partner companies (nothing transmitted; Peter's gate) |
| `COVER_LETTER_TO_CANADA_DRAFT.docx` | **DRAFT** — one‑page formal cover letter to ISED (not transmitted; Peter's gate) |
| [`RECEPTION_AND_VALUE.md`](RECEPTION_AND_VALUE.md) | honest read of how the offer would be received + a Tier‑3 value envelope (~$2.5–19M/yr near‑term, crux unmeasured; not financial advice) |
| `AI_ASSIST.json` | the standard onramp node |

## Honest scope

- **T1 (engine facts + the receipted demo):** determinism + hashes; the silent‑drift composition read (`877516b6`);
  the coherence→rejection law it leans on (`a5ceab9e`); the ground‑state common‑mode anchor (`d8c21c70`).
- **T2 (reasoned, planning):** the physics‑grounded Poisson model and every mapping above — sound, unbuilt on
  real tools.
- **T3 (to earn — the proof a litho engineer will respect):** run the composition read on **public imec/fab
  stochastic‑defect data** and report whether the ratio drift truly *leads* the yield excursion, and by how
  much. **No vendor relationship; none implied or sought.** Read‑only; the process owner decides; Hˢ is a
  complement, never the dose controller of record; the operator holds Breaker 16.

*Cross‑refs: `../electronics-assembly-smt/COHERENCE_AND_LASERS.md` (the coherence law), `../electronics-assembly-smt/CONTACT_POINT_DOCTRINE.md`,
`../../papers/flagship/PURE_SIGNAL_EXTRACTION_FROM_THE_GROUND_STATE.md`, `../../ARC_OF_DISCOVERY.md` §5 (the seed),
`../../library/THE_BLINDNESS_SUITE.md`. Peter is the sole gate; nothing posted.*

### References (public, for verification & citation)

1. *Production of 13.5 nm light with 5 % conversion efficiency from 2 µm laser‑driven tin microdroplet plasma*,
   Applied Physics Letters 123, 234101 (2023). https://pubs.aip.org/aip/apl/article/123/23/234101/2925750/
2. *Microdroplet‑tin plasma sources of EUV radiation driven by solid‑state lasers* (Topical Review),
   J. Opt. 24 (2022). https://iopscience.iop.org/article/10.1088/2040-8986/ac5a7e
3. *Stochastic printing failures in EUV lithography* (microbridges, broken lines, missing/merging contacts).
   https://www.researchgate.net/publication/331762907_Stochastic_printing_failures_in_EUV_lithography
4. *EUV Lithography: Sailing Along the Stochastic Cliffs*, Semiconductor Digest. https://www.semiconductor-digest.com/euv-lithography-sailing-along-the-stochastic-cliffs/
5. *Impact of chemical stochastics in EUV photoresists on pattern quality*, AIP Advances 15, 035236 (2025).
   https://pubs.aip.org/aip/adv/article/15/3/035236/3340203/
6. *High‑NA EUV lithography: the next step after EUVL*, imec. https://www.imec-int.com/en/articles/high-na-euvl-next-major-step-lithography

*Proof & Honesty Standard — numbers cited‑or‑fenced · math proven + receipted · value shown · experts decide.*
