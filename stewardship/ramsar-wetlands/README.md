# Ramsar wetlands pursuit — governance + field‑work for the Convention on Wetlands

*The basics of the Ramsar commitment. Distilled from `WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md`, the `RAMSAR_COMPLEXITY_GAP.md`, and the Human‑AI Accord. **Interest expressed, never acquired** — nothing deployed, no outreach sent. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001.*

---

## What Ramsar is

The **Convention on Wetlands** (Ramsar, Iran, 1971) is an intergovernmental treaty with **172 Contracting Parties**; the Ramsar Sites Information Service lists ~**2,500 Wetlands of International Importance**, from under a hectare to over six million. It is *a treaty, not a database* — and any instrument offered to it must respect that.

## The offer — two tiers

| Tier | Audience | What it does |
|---|---|---|
| **Governance** | Ramsar Secretariat, regional authorities | Multi‑site drift monitoring and aggregation — site rangers report drift, regional directors consolidate, the Secretariat governs across the network. |
| **Field‑work** (the expansion) | Site rangers, field ecologists, hydrologists, ornithologists | Per‑site compositional time‑series analysis — *which species/carrier is steering the change, what kind of transition the site is undergoing, when the steering changes.* |

The field‑work tier needs **no new engine and no new schema** — only a new domain adapter. Every wetland field activity already produces a closed, non‑negative, time‑ordered composition, which is exactly an Hˢ input.

## Five wetland compositions Hˢ reads unchanged

1. **Vegetation** — share of biomass / stem count / cover by species (succession + disturbance). *Which species is the helmsman of community change?*
2. **Water chemistry** — proportion of major ions / nutrients / pollutants (seasonal pulses + loading). *A small‑share pollutant doing large structural work — the Activation Coefficient as early warning.*
3. **Sediment** — organic / mineral / fraction proportions by depth or time (depositional regime shifts).
4. **Avian community** — proportion of bird count by species or guild (migration + reorganisation under habitat change). *Keystone (small‑share / large‑work) species detection.*
5. **Hydroperiod** — proportion of time wet / dry / transitional / flooded (climate + management response). *Regime classified as fixed‑point / drift / limit‑cycle / chaotic.*

All five are CoDa‑native and run through the existing pipeline (Adapter → CN‑TT → CNQ → render) unmodified.

## The honest complexity gap (named, not hidden)

Ramsar is **not a clean dataset waiting for a better algorithm.** It is a political‑scientific‑ecological system: ~2,500 sites, no standardised monitoring protocol across 172 countries, wildly variable temporal resolution, pervasive and *ecologically meaningful* zeros, reporting bias (designation carries obligations; countries have incentives to report stability), and jurisdictional variation in what "monitoring" even means. *"Saying the mathematics scales is not the same as proving the instrument works."* The full gap register exists so anyone — Peter, the CoDa community, Ramsar scientists, sceptics — can see exactly where the bridge is incomplete and decide whether to help.

This is why the **zero‑treatment** and **all‑zero carrier guard** work matters here (the E‑21 carrier guard, the multiplicative zero‑treatment): wetland compositions are zero‑heavy, and the instrument must handle structural absence honestly rather than producing a poisoned read.

## The posture — drift reported, never enforced

When Hˢ detects compositional drift in a wetland — emergent marsh quietly absorbing open water over years — it **reports, clearly, with the structural narrative that explains what the numbers mean.** It does not recommend action or trigger an alert; it does not stay silent either. *The drift is never suppressed; the interpretation is always human.* The conservation scientist decides whether it is succession, climate, or degradation requiring intervention. (This is the Open‑Loop Doctrine applied to the earth.)

## Where the pursuit goes (Tier 3, to earn)

A site scientist runs Hˢ on real Ramsar data and finds the helmsman/regime read useful; a reproduction confirms it; the Secretariat sees value in a deterministic multi‑site view. None of this is claimed today. This folder records the **basics of the commitment** so the work, if it advances, advances honestly.

**Sources (fuller record):** `../../papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md` · `../../../HUF/archive/post-coimbra-planning/RAMSAR_COMPLEXITY_GAP.md` · `../../../HUF/science/wetlands/HUF_Human_AI_Accord_Ramsar_v1.0.json`.

*The instrument reads. The expert decides. The drift is never suppressed; the interpretation is always human.*
