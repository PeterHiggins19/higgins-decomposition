# Geology Applications of Hs — Case Folder (public · Hs repo)

Applying the **Higgins Decomposition (Hs)** to compositional geoscience — mudstone chemostratigraphy, higher-dimensional reconstruction, and **geosensing** (multi-sensor field / remote-sensing compositional analysis). Builds on and complements the established compositional-data-in-geoscience literature (wavelet + CoDa chemostratigraphy, Wehner 2017; cell-phone-Raman field identification, Dhankhar & Wehner 2023).

---

> ★ **PRIME PROJECT (2026‑06).** This is the lead collaboration of the program. The flagship deliverable — a complete read of the Frielingen‑9 section through the full Hˢ kinematics platform, in geologist's language — is **[`FRIELINGEN9_WHAT_YOUR_SYSTEM_SAYS_2026-06.md`](FRIELINGEN9_WHAT_YOUR_SYSTEM_SAYS_2026-06.md)**: lossless to 3.55e‑15, trace‑over‑bulk confirmed, **8 datable structural boundaries**, ~2 effective dimensions, Diffusive character among 107 cross‑domain systems, within‑regime. Reproducible to a content hash; the geology stays the geologist's.

## Executive summary — the key

> **The full version is [`00_EXECUTIVE_OVERVIEW.md`](00_EXECUTIVE_OVERVIEW.md) — read it first. This is the condensed key.**

**Hs is a deterministic instrument for compositional series** (parts-of-a-whole indexed by depth, time, or position). It is formalised as a hash-chained pipeline — the **Tensor Train (HUF-STD-002)**: *raw data → CNT (the pre-processor: closure → CLR → ILR → per-step navigation) → CNQ (exact quaternion at four parts) → vector output* — every link carrying the entry hash forward, so any result is reproducible and auditable. Claim tiers (confirmed / experimental / to-be-earned) travel with every number.

**What's in hand (confirmed):** a cited, one-command-reproducible CNT/CNQ run on real Lower-Cretaceous mudstone (Frielingen-9, PANGAEA 897615) with an interactive dashboard and a field-by-field guide; a tested **CNQ-tiling / faceted-read** result — an atlas of overlapping exact D=4 charts reconstructs the full higher-dimensional compositional move **losslessly**; a validated **upstream zero-treatment** that fixes the engine's 1e-15-floor artifact while leaving zero-free data untouched and confirming prior results robust.

**The flagship application — geosensing.** The same architecture runs at field scale: the **geologist is the rover, the phone is a multi-sensor platform**, one CNT runs per sensor, and a **calibration-weighted fusion** combines them, anchored by a few onsite grab-samples. A simulation on the Frielingen-9 wall shows the honest design rule directly: the high-fidelity elemental sensor (Raman/pXRF) leads, naive equal-weight fusion *dilutes* it, and calibration-weighted fusion recovers it — *calibrate and weight by reliability, don't just add sensors.* This is the front-end / edge-instrument thesis (deterministic, tiny, reconstructable, auditable reduction at the sensor) made concrete and testable today, on hardware everyone carries — and it scales toward autonomous rover sensing.

**Governance.** Hs computes; **HUF governs what is released** via the carrier filter (need-to-know / withhold-on-distribution), which fits government and pre-publication data handling. AI involvement is disclosed (HUF-STD-001 AI Use Declaration; human-only authorship). **The instrument reads. The expert decides. The hashes carry the receipts.**

> **Carrier-filter governance (HUF).** This is a *public* repo folder: **no personal or private material here.** Relationship and contact material is kept **off-repo and tracked** (HUF Governance Charter, *Carrier Filter* article).

---

## Contents
| Path | What it is |
|---|---|
| [`00_EXECUTIVE_OVERVIEW.md`](00_EXECUTIVE_OVERVIEW.md) | **Start here.** Full executive overview — Hs, the Tensor Train, claim tiers, deep value points, the HUF-Gov carrier filter, the disclosed AI role + HUF AI Collective acknowledgment, and a **§9 "receipts"** layer linking the engine, standards, trust protocol, and precision tests. |
| `00_COLLABORATION_OVERVIEW.md` | Public overview — what Hs/CNT is, the candidate studies, the open collaboration posture. |
| `HS_PRIMER.md` | One-page primer on the instrument itself — method only, **no geological claims**. |
| `MUDSTONE_HS_FIT.md` | How Hs/CNT assists **mudstone chemostratigraphy** (the strongest near-term fit). |
| `demo_frielingen9/` | **Worked, cited, reproducible demo** on real PANGAEA mudstone — `REPRODUCE.md` regenerates figures + data + the single-screen 16:9 dashboard from one CSV + two scripts; `frielingen9_dashboard_guide.html` explains every field and its formula. |
| `demo_frielingen9/CNQ_TILING_CONCEPT.html` | **Tested concept:** higher-dimensional CNQ from an atlas of overlapping exact D=4 charts glued on shared parts — lossless on the Frielingen-9 data (`cnq_multimap.py`/`.png`); includes the corrected sphere reasoning. |
| `demo_frielingen9/FACETED_READ_CONCEPT.html` | The finite atlas as a *faceted read* of the curved high-D compositional manifold — more facets → truer curvature. |
| `demo_frielingen9/HS_FRONTEND_POSITION.html` | The sensor front end as the highest-leverage seat; why Hs's design is the entry ticket; hardware tiers; honestly tiered. |
| **`FIELD_MULTISENSOR_TOOL_CONCEPT.md`** | **Geosensing — the flagship application.** Rover = geologist, phone = multi-sensor platform, one CNT per sensor, calibration-weighted fusion; real-vs-simulated; NASA/USGS value; honest tiering. |
| **`field_tool_sim/field_multisensor_sim.html`** | **Working simulation** on the Frielingen-9 wall — per-sensor CNT, the elemental-sensor-leads / calibration-weighted-fusion result, live readout. Concept demonstrator (synthetic proxies, clearly labelled). |
| **`GEOSENSING_CONCEPT_PROPOSAL.md`** | **Public concept proposal** — develop the device with Matthew, lock Hs's vector-space (quaternion) computation in hardware, a staged NASA/USGS remote-sensing approach, and the **established-results proof-list** qualifying Hs. Written for discovery; honest-broker tiered. |
| **`CNTT_FLIGHT_CONTROL_SPEC.md`** | **Space spec** — the expert-steerable, deterministic CN-TT flight engine: the **Geologist Protocol Control Code** (bounded, hash-stamped, in-flight reconfiguration + delta-correction) and the **Coherence Supervisor** (engine-monitoring-engines, redundancy voting, FDIR), mapped to NASA cFS / TMR / NPR 7150.2. |
| **`GEOSENSING_FLIGHT_ROADMAP.md`** | **Vision + backward-designed path** — eight flight-architecture improvements (deterministic-replay upset detection, ground digital twin, power/bandwidth-aware resolution, sense→sample autonomy…) and the staged path from first flight back to the immediate Matthew field step. Dream big; build small; skip nothing. |
| **`flight_spec_suite/`** | **NASA-style specification suite (Pre-Phase-A drafts).** `HGS-000` spec tree + index, then ConOps, System Requirements, Software Requirements, Interface Control, Fault Management/FDIR, V&V + verification matrix, Software Assurance & CM, and the **Development Plan & staged test route** (`HGS-008`, incl. the proposal to Matthew). Build-to-flight-spec from day one → a directed instrument, testable in stages. |
| `IGNEOUS_DIFFERENTIATION_SEED.md` | Igneous differentiation / fractional crystallization as compositional dynamics. |
| `FIELD_DIRECTIONAL_SNIFFER.md` | The earlier seed of the cell-phone field "sniffer" idea (now built out in the geosensing concept above). |
| `REPO_MAP.md` | Links across the whole `PeterHiggins19` structure (Hs · HUF · RWA). |
| `copies/`, `large-linked/` | Copies of past geology/geochem docs by source; pointers to oversized outputs + raw datasets. |

## Related Hs work this collaboration generated (elsewhere in the repo)
| Path | What it is |
|---|---|
| [`../../HCI-CNT/adapters/zero_treatment.py`](../../HCI-CNT/adapters/zero_treatment.py) | **Upstream zero-treatment** (structural-drop + multiplicative replacement) — replaces the engine's 1e-15 floor; no engine change. |
| [`../../experiments/zero_treatment_2026-06/RESULTS_zero_treatment_comparison.md`](../../experiments/zero_treatment_2026-06/RESULTS_zero_treatment_comparison.md) | All-EMBER **baseline-vs-treated** validation: safe on clean data, removes the floor artifact, **prior results confirmed robust**. |
| [`../../experiments/canada_energy_2026-06/RESULTS_Canada_national_CNT.md`](../../experiments/canada_energy_2026-06/RESULTS_Canada_national_CNT.md) | **National-Canada CNT anchor** through the canonical engine (D=8 after structural-zero treatment) — the original post-conference agenda. |

## Discipline
Research-grade throughout; claim tiers preserved; calibration-gated; **Hs assists the geologist, it does not decide interpretations** or replace established methods. Published-work citations are public; the working *relationship* is private and off-repo.

*The instrument reads. The expert decides. The hashes carry the receipts.*
