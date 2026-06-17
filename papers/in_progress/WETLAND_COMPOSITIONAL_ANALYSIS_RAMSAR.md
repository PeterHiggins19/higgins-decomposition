# Wetland Compositional Analysis — Hˢ as field-work tool for Ramsar Convention sites

**Filed:** 2026-05-27 (pre-conference; doc-only, S2-class).
**Status:** Working note. Records Peter's pivot expanding the framework's Ramsar offering from governance-only (HUF-GOV / HUF-CLS observe-or-control fork) to *also* compositional field-work tools for wetland ecologists, hydrologists, and ornithologists.
**Trigger:** Peter's flight-prep observation, *"Ramsar is also on my agenda, now we can offer more than governance, compositional analysis tools for wetlands field work."*
**Companion documents:** `HUF/science/quantum/HUF_Topography_Conjecture_v1.0.md` (which uses Ramsar as its canonical worked example for the mixed-geometry hierarchy); `papers/in_progress/ATTRACTOR_MORPHOLOGY_AND_TRANSCENDENTAL_BASINS.md` (sibling, filed same day; ecological trajectories may become a primary application target for the attractor diagnostic module); `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` §5.9 (post-conference work entry).
**Lockdown discipline:** S2 doc-only; `papers/in_progress/`; no engine, schema, INV catalog, or NO-CREATE touches.

---

## 1. What changes — governance → governance + field-work

The HUF Topography Conjecture (`HUF/science/quantum/HUF_Topography_Conjecture_v1.0.md`) already uses Ramsar as its canonical worked example, but framed at the **governance** layer: a three-tier deployment with the site ranger seeing a 1-node fuel-gauge MDG reading, the regional director seeing a clustered 2-D grid view, and the Ramsar Secretariat seeing the full topographic manifold. The site ranger's job, in that framing, is to *report drift*; the regional director's job is to *consolidate reports*; the Secretariat's job is to *govern across the network of sites*.

That's HUF-GOV / HUF-CLS — the *observe-or-control* fork at ADAC — applied to the international-convention monitoring layer. It is correct and useful but represents only one half of what the framework can offer.

The other half — the half this note names — is **field-work compositional analysis**. The site ranger isn't just reporting an MDG drift; they're walking transects, recording vegetation composition, sampling water chemistry, counting birds, logging hydroperiod. *Every one of those activities produces a compositional time-series.* And every compositional time-series is, by construction, an Hˢ input — closed, non-negative, finite carriers, time-series structure. The framework's existing tooling (CNT engine → Helmsman trajectory → Power Share → Activation Coefficient → navigation_2D) applies *unchanged* to wetland data. No new engine. No new schema. Just a new domain entry in the Adapter layer (Order 0 of the tensor train).

What changes: the framework now offers Ramsar **two tiers of service**, not one:

| Tier | Audience | What it does |
|---|---|---|
| **Governance** (existing) | Ramsar Secretariat, regional authorities | Multi-site drift monitoring, MDG aggregation, hierarchical decision support per the HUF Topography Conjecture |
| **Field-work** (new, named here) | Site rangers, field ecologists, hydrologists, ornithologists | Per-site compositional time-series analysis — which species/carrier is the structural driver of change, what kind of transition the site is undergoing, when the steering changes |

---

## 2. The five wetland compositional time-series types

Wetland field-work produces compositional data in at least five natural categories, each of which fits CNT's input format without modification:

**(1) Vegetation composition.** Per-site, per-transect, per-season: the proportion of total biomass (or stem count, or canopy cover) by species. Closed (sums to 100 % of recorded vegetation); D varies from ~5 (boreal peatlands) to ~50+ (tropical floodplains); T can be seasonal (4/year), annual, or multi-decadal. The trajectory shows ecological succession + disturbance response. *Application: identify the helmsman species — which one is doing the structural work of community-composition change at each step?*

**(2) Water chemistry composition.** Per-site, per-sampling-event: the proportion of major ions / nutrients / pollutants by mass. Major-element CoDa territory; D typically 5–15 (Na, Mg, K, Ca, Cl, SO₄, HCO₃, NO₃, PO₄, NH₄, …); T sub-annual (weekly to monthly). Trajectory shows seasonal pulses + anthropogenic loading. *Application: detect a pollutant carrier with small starting share doing large structural work (Activation Coefficient — the yeast factor for water-quality early warning).*

**(3) Sediment composition.** Per-core, per-depth or per-time-slice: the proportion of organic / mineral / specific fractions. D typically 4–8; T can be depth-indexed (paleo-record) or temporal (sediment trap). Trajectory shows depositional regime shifts. *Application: classify sediment regime changes (deliberate Energiewende-like arc vs Fukushima-like shock vs UK-coal-exit-like jump) using the same morphological vocabulary.*

**(4) Avian community composition.** Per-site, per-survey: proportion of total bird count by species or guild. D = 10–100+ depending on guild aggregation; T = seasonal or annual. Trajectory shows migratory patterns + community reorganisation under habitat change. *Application: detect keystone species (small-share / large-structural-work) and identify the helmsman of community change at each survey.*

**(5) Hydroperiod composition.** Per-site, per-year: proportion of time spent in wet / dry / transitional / flooded states. D = 4 (or finer hydrologic categorisation); T = annual. Trajectory shows climate response + management impact. *Application: characterise the hydrological regime as fixed-point / drift / limit-cycle / chaotic using the Helmsman family taxonomy.*

All five are CoDa-native, all five are within CNT's existing capability, all five can run through the existing pipeline (Adapter → CNT → CNQ → Vector render) without any engine modification.

---

## 3. Worked example — vegetation transect at a hypothetical fen

Consider a Ramsar-designated fen, monitored annually for 25 years. The site ranger records vegetation composition along five permanent transects. Aggregated to the site level: D = 8 species (sphagnum mosses, sedges, rushes, ericaceous shrubs, herbaceous forbs, encroaching trees, invasive grasses, bare ground), T = 25 timesteps.

A drought episode in year 12 shifts the hydrological balance; an invasive grass arrives in year 14; site managers initiate restoration in year 18. The vegetation composition responds across all these events.

**What CNT outputs:**

- **Composition view** — the share of each species over time. Standard ecology output; the field already has this view in stacked-area or biplot form.

- **Helmsman trajectory** — the species doing the largest CLR-step at each year. Pre-drought: sphagnum stable, sedges fluctuating. Year 12 → 13 step: ericaceous shrubs jump (drought tolerance). Year 14 → 15 step: invasive grass becomes helmsman (rapid establishment). Year 18 → 22 sequence: sphagnum reasserts (restoration). *The helmsman trajectory tells the ecological story in one diagnostic.*

- **Power Share** at the year-12-→-13 step: ericaceous shrubs carry, say, 73 % of the squared CLR motion. That is the *structural fingerprint* of the drought event — even though shrub *share* changes only modestly, shrub *structural work* dominates the composition shift.

- **Activation Coefficient** for invasive grass at year 14 → 15: starting share 0.4 %, Power Share 62 %, α ≈ 155×. *That is the "yeast factor" of invasive ecology* — the invasive does structural work 155 times its size in its first establishment year. The diagnostic surfaces the invasion four years before standard share-tracking calls the invasive "established" (typically when share crosses 5 %).

- **Course directness** of the 25-year trajectory: a low value (say 0.12) indicates *looping reorganisation*, which is the Japan-Fukushima-post-2011 morphological family applied here to a drought-then-invasion-then-restoration sequence. A high value (say 0.45) would indicate *deliberate-arc* recovery dynamics.

- **Strange attractor fingerprint** (per `ATTRACTOR_MORPHOLOGY_AND_TRANSCENDENTAL_BASINS.md`): Lyapunov spectrum, correlation dimension, RQA, SRB-transcendental-proximity match. *Classifies the wetland's underlying dynamics as a specific attractor morphology* — comparable across sites and across years.

**Reproducibility:** every diagnostic above runs from the same 8-species × 25-year CSV. Hash-chained from the raw transect data through CNT JSON to the Stage-1/2/3/4 plates to the final field-report PDF. A Ramsar reviewer in 2040 can re-run the analysis on the original CSV and get the same numbers byte-identical.

---

## 4. The keystone-species hypothesis (ecological yeast factor)

A standing claim in community ecology: **keystone species** — species whose effect on the ecosystem is disproportionate to their abundance. Robert Paine's 1969 starfish-and-mussel work named the concept; subsequent literature established hundreds of examples but lacked a *quantitative diagnostic* that operates on routine monitoring data.

The framework's Activation Coefficient α = (Power Share) / (starting share) **is that diagnostic, applied to ecological data.** When α ≫ 1 for species *i* at year *t*, the framework names species *i* as doing structural work disproportionate to its abundance — *exactly the keystone definition*, but quantified, time-resolved, and reproducible on per-site transect data.

The hypothesis to test: for known keystone species (Paine's starfish, sea otters, beavers, wolves, ironwoods, mountain pine beetles, etc.), the framework's Activation Coefficient should fire at α ≫ 1 in the years of their structural action, on actual time-series data, in the published ecological record. This is a falsifiable empirical claim — and a clean post-conference research thread.

If the hypothesis holds, the framework gives ecology *a routine instrument for keystone-species detection* — not from expert intuition but from monitoring data. That instrument runs on existing CNT engine code; the only addition is a domain-specific Adapter (Order 0 of the tensor train) that converts ecological survey CSVs to CNT input.

---

## 5. Three-tier deployment — site ranger / regional / Secretariat

Mapping to the HUF Topography Conjecture's existing three-tier framing, *the field-work tier slots in below the existing governance tiers*:

| Tier | Geometry | What it reads | What it outputs |
|---|---|---|---|
| **Site ranger (field-work)** — NEW | 1-node fuel gauge + per-site CNT trajectory | Annual transect / chemistry / avian / hydroperiod compositional data per site | Site-level CNT JSON + Stage-1/2/3 plates: helmsman, Power Share, Activation Coefficient, navigation chart |
| **Regional authority (governance)** — existing | 2-D grid (per-region cluster) | Multiple sites' CNT outputs aggregated | Regional drift signature; cross-site morphology comparison; resource allocation diagnostics |
| **Secretariat (governance)** — existing | Full topographic manifold | All sites + temporal pattern | Convention-level reporting; multi-decadal trend; treaty-compliance diagnostics |

The site ranger sees a per-site Helmsman / Power Share / Activation Coefficient dashboard — same instrument the talk's energy-mix case studies use. The framework's existing engine outputs become the field-work tier's data product directly. *No new compute layer; only a new Adapter and a new viewing context.*

The regional + Secretariat tiers consume the per-site CNT JSONs as input — the framework's existing pipeline (`HUF_TENSOR_TRAIN_IO_STANDARD.json the_tensor_train_v1_0.links[]`) handles the aggregation natively. Site ranger's Stage-1 plate is the same artifact the regional director's clustering algorithm consumes is the same artifact the Secretariat's manifold visualisation reads. *One pipeline, three audiences, three views.*

---

## 6. Post-conference work entry (filed in `POST_CONFERENCE_ROADMAP_2026-06.md` §5.9)

**Four items:**

1. **Adapter module** — `adapters/ramsar_wetland.py` converts standard wetland-monitoring CSV formats (likely Ramsar Information Sheet attachment formats; species lists from World Flora Online / IUCN Red List; water-chemistry from standard limnological tables) to CNT input compositional CSV. **Effort:** moderate (~400 lines + domain-specific normalisation + per-source-format handling). **Push class:** S2 doc + adapter code (adapters live outside the locked engine).

2. **Field handbook** — `papers/in_progress/RAMSAR_FIELD_HANDBOOK.md` (or `papers/applications/ECOLOGY_FIELD_HANDBOOK.md`): a worked-example walkthrough for field ecologists, modeled on `CCTT_RUNBOOK.md`. Step-by-step from raw transect data to per-site CNT diagnostic dashboard. Audience: practicing wetland ecologists with R / Python literacy but no prior Hˢ exposure. **Effort:** moderate. **Push class:** S2 doc.

3. **Three pilot studies** — pick three Ramsar-designated sites with published long-term monitoring data (e.g., one boreal peatland in Finland, one tropical floodplain in Botswana, one temperate fen in the UK), run the full CNT diagnostic on their published time-series, publish the resulting Helmsman / Power Share / Activation Coefficient / Stage-1 plates as a companion data paper. Provides empirical anchor for the field-work claim. **Effort:** substantial (~3 weeks per site). **Push class:** S2 doc + data publication.

4. **Outreach to Ramsar Secretariat** — a standing offer following the *non-contact / ghost-tool* outreach doctrine, addressed to a practitioner audience (Secretariat or Scientific and Technical Review Panel). Frame: *"the framework that already supports the governance tier now offers a field-work tier; here are three pilot studies; happy to demo the runbook to any interested member-state ecologist."* **Effort:** low (one offer + supporting links). **Push class:** S2 (any draft kept private outside the public repo, mirroring the frontier-audience ghost-tool pattern; any sending is Peter's gate).

**Sequencing:** items 1, 2 cluster in the first post-conference sprint (weeks 1–4). Item 3 (three pilots) runs in parallel across the second and third sprints (weeks 5–20). Item 4 outreach lands after at least one pilot is complete — provides concrete demonstration content alongside the abstract framework claim.

**Effort cap:** ~6–10 weeks of focused work for the full four-item package, parallelisable across sprints.

---

## 7. Why this pivot now, six days before the conference

Two reasons.

**The first is opportunistic.** Peter is at CoDaWork 2026 next week, where the audience includes the CoDa community — many of whom work on environmental, ecological, or geochemical compositional data. Mentioning the Ramsar field-work tier verbally during Q&A is essentially free outreach to an audience already in the room. *"The framework runs any compositional dataset the CoDa community can describe — including wetland vegetation transects, water-chemistry profiles, avian community surveys, hydroperiod logs."* That sentence is now true and now in the talk's repertoire via the new Slide 1 line *"Hˢ runs any compositional dataset the CoDa community can describe."*

**The second is structural.** The framework has been Ramsar-adjacent since the HUF Topography Conjecture filed Ramsar as its canonical worked example for the governance tier. Field-work was always implicit — every governance system depends on field data — but it was never named as a tier the framework explicitly supports. Naming it now closes a gap that the framework's discipline cares about: *the framework should be explicit about what it offers*. The Topography Conjecture had Ramsar in the system; this note completes the offering.

There is also a personal-arc reason. Peter's note today framed this as *"my mind unloading i hope so i can keep preparing for my flight on Saturday"* — mid-conference-prep clarity. The two filings today (this note + the attractor-morphology consolidation) capture two threads that were live in the mind's foreground but at risk of being lost in the conference flood. Filing now preserves them for the post-conference work without disrupting the conference prep itself.

---

## 8. Cross-references and acknowledgement

**Cross-references:**

- `HUF/science/quantum/HUF_Topography_Conjecture_v1.0.md` §6 (the induced manifold) and §7 (the Ramsar three-tier example) — the existing governance-tier framing this note extends.
- `papers/in_progress/ATTRACTOR_MORPHOLOGY_AND_TRANSCENDENTAL_BASINS.md` — sibling note filed same day; ecological trajectories may become a primary application target for the attractor-fingerprint diagnostic.
- `papers/in_progress/POST_CONFERENCE_ROADMAP_2026-06.md` §5.9 — the post-conference work entry filed in parallel with this note.
- `huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json` `the_tensor_train_v1_0.links[]` Link 1 (Adapter) — where the `ramsar_wetland.py` module slots in.
- `HCI-CNT/engine/cnt.py` v3.1.0 and `HCI-CNQ/engine/cnq.py` v2.0.0 — the existing engines that run unchanged on wetland compositional inputs.
- `Studies/Energy_HiddenDirections_2026-05-17.pdf` — the community-friendly walk-through deck format; a wetland-domain equivalent would be the natural pilot-study output format.

**Acknowledgement:**

Pivot raised by Peter Higgins during pre-conference / pre-flight preparation, 2026-05-27 (six days before CoDaWork 2026 in Coimbra; flight on Saturday). The expansion from governance-only to governance + field-work was implicit in the framework since the HUF Topography Conjecture's Ramsar worked example but had not been named as a deliberate tier. This note names it. Concrete-substrate mapping (five compositional time-series types, three-tier deployment, four-item work plan) developed in conversation with Claude (Anthropic). The wetland pivot is a *practitioner-audience* offering — a field-work tier for the framework's post-conference expansion.

*Filed during the pre-conference lockdown, six days before CoDaWork 2026.*
