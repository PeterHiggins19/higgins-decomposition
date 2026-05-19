# Experiments Journal — Hs Framework Lineage and Sequential Run Record

**Status:** living document — refreshed at every push
**Last updated:** 2026-05-10 (push #34)
**Scope:** every experiment that has ever been run under the Hs / HUF / CNT / CNQ family of engines, dated, linked, and cross-referenced to the engine version that ran it
**Companion documents:** [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md) (running narrative), [`ai-refresh/INVESTIGATION_CATALOG.json`](ai-refresh/INVESTIGATION_CATALOG.json) (research-disposition record), [`HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md`](HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md) (theory)

---

## Purpose

This is the **single document that answers "what have we actually run, on what version, and what did each version change?"** It is the explanatory front-door for any new reader, reviewer, citation chase, or AI cold-start. Every experiment named below has a link to its artefacts. Every engine version named below has a link to the narrative that introduced it. Every numerical anchor named below is reproducible from the linked artefact.

The journal is **strictly historical**: it does not speculate about future work. For deferred items see `experiments/2026-05-10_full-corpus-validation/DEFERRED_ADAPTERS.md`.

---

## Reading guide

If you are short on time, read in this order:

1. The **engine-version timeline** below — answers "what versions exist and how do they relate?"
2. The **what changed and why each version was needed** table — answers "what is the improvement story?"
3. The **sequential experiment ledger** — answers "what real-world data has the engine actually been run on?"
4. The **cross-version diff highlights** — answers "what does the latest engine do that the old ones didn't?"

The four sections together are ≈ 25 minutes of reading. Each links to deeper artefacts when you want detail.

---

## 1. Engine-version timeline

```
Apr 2026         May 2026                           Jun 2026
     │                │                                  │
     ▼                ▼                                  ▼
HUF 12-step ─► CNT v1.x ─► CNT v2.0.4 ─► CNT v3.0.0  ── ► (CodaWork 2026)
                              │           │
              CNQ v0 (QD ─►   ▼           ▼
              experimental) ─► CNQ v1.0.0 ─► CNQ v2.0.0
```

| Version | First introduced | Narrative | Status today |
|---|---|---|---|
| **HUF 12-step pipeline** | Pre-2026 (lineage from DADC at the Binaural Test Lab) | [`HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md) | Frozen reference — the 12 steps, multi-language reports, the original CSVs are preserved under `experiments/Hs-NN_*/` |
| **CNT v1.x** | April 2026 | [`ai-refresh/AI_REFRESH_2026-04-27.md`](ai-refresh/AI_REFRESH_2026-04-27.md), [`ai-refresh/AI_REFRESH_2026-04-30.md`](ai-refresh/AI_REFRESH_2026-04-30.md) | Superseded — first engine that consolidated the 12 steps into a single `cnt.py` |
| **CNT v2.0.x → 2.0.4** | 2026-05-05 push #14, frozen 2026-05-08 | [`ai-refresh/AI_REFRESH_2026-05-05.md`](ai-refresh/AI_REFRESH_2026-05-05.md), [`ai-refresh/AI_REFRESH_2026-05-05_v1.1.x.md`](ai-refresh/AI_REFRESH_2026-05-05_v1.1.x.md) | Superseded by v3.0.0; archive remains for lineage comparisons |
| **CNQ v0 (QD experimental)** | April 2026, pre-#22 | [`HCI-CNQ/archive/`](HCI-CNQ/archive/) | Three experimental "rounds" (2, 2.5, 2.6) on Backblaze, Planck CMB, neutrino oscillation; promoted to canonical at push #23 |
| **CNQ v1.0.0** | 2026-05-08 push #26 | [`ai-refresh/AI_REFRESH_2026-05-08_push26_chatgpt_round2_audit.md`](ai-refresh/AI_REFRESH_2026-05-08_push26_chatgpt_round2_audit.md) | Superseded by v2.0.0; this version revealed five subtle bugs (NaN-in-hash for T<2, D=2 schema mismatch, `metadata.reference_implementation` parity-break, `extract_cnt_diagnostics` path mismatch, file-tail truncation) which became the SEA-1.0 doctrine's first targets |
| **CNT v3.0.0 + CNQ v2.0.0** | 2026-05-09 push #32 | [`ai-refresh/AI_REFRESH_2026-05-09_push32_engine_v3_v2_rebuild.md`](ai-refresh/AI_REFRESH_2026-05-09_push32_engine_v3_v2_rebuild.md) | **Current canonical**. Engine independence policy, four doctrines (SEA-1.0, STP-1.0, CRD-1.0, engine-independence), shared `hci_shared/` library, R ports, UN-6 wrappers |

The lineage is **additive, not destructive**: each successor cites the predecessor. Original HUF 12-step outputs are preserved verbatim under `experiments/Hs-NN_*/`; CNT v2.0.4 archive is at [`HCI-CNT/experiments/`](HCI-CNT/experiments/); CNT v3 + CNQ v2 outputs land in [`papers/codawork2026/conference_2026_06/`](papers/codawork2026/conference_2026_06/) and [`experiments/2026-05-10_full-corpus-validation/`](experiments/2026-05-10_full-corpus-validation/).


---

## 2. What changed at each version, and why

| Transition | What changed | Why it mattered | Lived evidence |
|---|---|---|---|
| **HUF → CNT v1** | The 12 separate pipeline scripts were consolidated into a single `cnt.py` engine that read a CSV and emitted one canonical JSON. Multi-language reports were lifted out of the engine into a separate publication layer. | The 12-step pipeline could be run in 12 different orders by 12 different operators and produce subtly different intermediates. CNT v1 made the result deterministic by making the engine atomic. The first content-hash chain landed here. | First reproducible `content_sha256` across consecutive runs on the same CSV |
| **CNT v1 → v2.0.x** | Schema 2.x stabilised: `_meta`, `input`, `stages.stage1/stage2`, `helmsman_family`, `depth_tower`, `diagnostics`, `tensor` blocks all locked. R port added. Determinism + parity tests promoted to gating. | A schema that was changing every push was a schema in name only. Locking it is what made cross-version comparison and citation possible. | [`HCI-CNT/CNT_JSON_SCHEMA.md`](HCI-CNT/CNT_JSON_SCHEMA.md), [`HCI-CNT/engine/tests/test_determinism.py`](HCI-CNT/engine/tests/test_determinism.py) |
| **CNT v2.0.x → v2.0.4** | IR-class taxonomy fixed (engine 2.0.3 corrected an off-by-one in the OVERDAMPED edge cases). USA EMBER 2025 row added. Stage 3 + Stage 4 plate modules. R port reached parity. CCTT (Cross-Check Tool Test) protocol added. CNQ tier promoted from QD experimental to canonical (push #23). Volume IV (Quaternion View) written. | The IR class is what classifies the dynamics; an off-by-one would have produced the wrong taxonomy on edge-case datasets. CNQ promotion was the moment "CNT measures invariance, CNQ names the algebra it lives in" became a defendable claim. | [`HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md`](HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md), [`ai-refresh/AI_REFRESH_2026-05-07_quaternion_integration.md`](ai-refresh/AI_REFRESH_2026-05-07_quaternion_integration.md) |
| **CNQ v0 (experimental) → CNQ v1.0.0** | Hamilton-product core, full `cnq.py` engine, `cnt_adapter.py`, `geometry.py`, `hashing.py`, `expected_results.json`, `verify_publication_results.py`. Three IEEE-floor confirmations (Backblaze fleet 4.441e-16, Planck CMB 4.441e-16 + M²=I 7.63e-17, SM neutrino LIMIT_CYCLE_P2 + M²=I 7.40e-17). | Until v1.0.0, CNQ was three Python notebooks with no determinism contract. v1.0.0 is what made independent reproduction possible. | [`HCI-CNQ/engine/expected_results.json`](HCI-CNQ/engine/expected_results.json), [`HCI-CNQ/engine/run_all_confirmations.py`](HCI-CNQ/engine/run_all_confirmations.py) |
| **CNT v2.0.4 + CNQ v1.0.0 → CNT v3.0.0 + CNQ v2.0.0 (push #32, 2026-05-09)** | Ground-up rebuild. **Engine independence policy** (no cross-engine hash chain; each engine deterministic on its own). Shared `hci_shared/` library replaces ad-hoc utility duplication. **D=8 twin-quaternion factoring** at IEEE floor (load-bearing). **D=16 quad-quaternion** schema-locked. **Anti-specification** doctrine SEA-1.0. **Self-test** doctrine STP-1.0. **UN-6 wrappers** (en, fr, es, ru, zh, ar). R ports for both engines. Cross-language per-field parity verification. | The five v1.0.0 bugs proved that an engine without an enumerated failure space is an engine with hidden trapdoors. Push #32 is the rebuild that closes them and makes "the engine cannot fail in this way" provable for each named mode. | [`docs/SUSPICION_OF_EVERY_ASSUMPTION.md`](docs/SUSPICION_OF_EVERY_ASSUMPTION.md), [`docs/SELF_TEST_PROTOCOL.md`](docs/SELF_TEST_PROTOCOL.md), [`HCI-CNT/engine/cnt.py`](HCI-CNT/engine/cnt.py), [`HCI-CNQ/engine/cnq.py`](HCI-CNQ/engine/cnq.py) |
| **Push #33 (2026-05-10 morning)** | **Coherent Range Doctrine** CRD-1.0. Multi-carrier comparisons must be computed on the intersection of all members' ranges. Manifest header on every multi-carrier output. | Surfaced by the USA-EMBER missing-year-2000 asymmetry: USA covered 2001-2025 (T=25), other countries covered 2000-2025 (T=26). Mixed-T comparison hides asymmetry; the doctrine forces the matched-window into the headline. | [`docs/COHERENT_RANGE_DOCTRINE.md`](docs/COHERENT_RANGE_DOCTRINE.md), [`papers/codawork2026/conference_2026_06/COMPARISON_v2_0_4_vs_v3_0_0.md`](papers/codawork2026/conference_2026_06/COMPARISON_v2_0_4_vs_v3_0_0.md) |
| **Push #34 (2026-05-10 afternoon)** | **Full-corpus validation reference suite**. 18 datasets across 10 domains (Phase 1) → 101 datasets across 11 domains (Phase 2). Per-dataset Stage 1 (pure CoDa) report + Advanced (full Hˢ + CNQ v2) report. Master findings document. Three new adapter classes: geochem binners (patched to walk-up DATA correctly), `owid_energy_adapter.py` (73 country-level primary-energy compositions), `fao_sdmx_adapter.py` (top-N-country SDMX pivot). | The suite is what makes the framework's claims **citable in scientific reports**. Until push #34, demonstrations were scattered; now they are one canonical folder with reproducible JSON outputs. | [`experiments/2026-05-10_full-corpus-validation/README.md`](experiments/2026-05-10_full-corpus-validation/README.md), [`experiments/2026-05-10_full-corpus-validation/MASTER_FINDINGS.md`](experiments/2026-05-10_full-corpus-validation/MASTER_FINDINGS.md) |


---

## 3. Sequential experiment ledger

Every experiment ever run, in chronological order, with a link to its artefact and the engine version that produced it.

### 3.1 HUF 12-step pipeline era — `experiments/Hs-NN_*/` (April 2026)

The original 25-experiment foundational set, plus the M-series and STD/LAB calibration runs. Each experiment folder has source CSVs, multi-language reports (en, pt, it, zh, hi), pipeline-output JSONs, and a JOURNAL.md where present.

| ID | Domain | Description | Folder |
|---|---|---|---|
| Hs-01 | commodities | Gold-silver mass-fraction composition (1688-2025, T=1338, D=2) | [`experiments/Hs-01_Gold_Silver/`](experiments/Hs-01_Gold_Silver/) |
| Hs-02 | energy | US energy primary-source consumption | [`experiments/Hs-02_US_Energy/`](experiments/Hs-02_US_Energy/) |
| Hs-03 | nuclear | SEMF term decomposition across the valley of stability | [`experiments/Hs-03_Nuclear_SEMF/`](experiments/Hs-03_Nuclear_SEMF/) |
| Hs-04 | acoustics | Bessel-mode acoustics resonance composition | [`experiments/Hs-04_Bessel_Acoustics/`](experiments/Hs-04_Bessel_Acoustics/) |
| Hs-05 | geochemistry | Major-oxide composition across volcanic regions (Ball 2022 source) | [`experiments/Hs-05_Geochemistry/`](experiments/Hs-05_Geochemistry/) |
| Hs-06 | physics | Fusion reactor plasma composition study | [`experiments/Hs-06_Fusion/`](experiments/Hs-06_Fusion/) |
| Hs-07 | physics | QCD particle yield composition | [`experiments/Hs-07_QCD/`](experiments/Hs-07_QCD/) |
| Hs-08 | physics | CKM and PMNS matrix mixing angles | [`experiments/Hs-08_CKM_PMNS/`](experiments/Hs-08_CKM_PMNS/) |
| Hs-09 | astrophysics | Stellar element-abundance composition | [`experiments/Hs-09_Stellar/`](experiments/Hs-09_Stellar/) |
| Hs-10 | astrophysics | GW150914 gravitational-wave event spectral composition | [`experiments/Hs-10_GW150914/`](experiments/Hs-10_GW150914/) |
| Hs-11 | nuclear | AME2020 atomic mass evaluation | [`experiments/Hs-11_AME2020/`](experiments/Hs-11_AME2020/) |
| Hs-12 | mechanics | Spring-mass system energy partition | [`experiments/Hs-12_Spring_Mass/`](experiments/Hs-12_Spring_Mass/) |
| Hs-13 | materials | Steel alloy compositional variants | [`experiments/Hs-13_Steel/`](experiments/Hs-13_Steel/) |
| Hs-14 | systems | Conjugate-pair coupling experiments | [`experiments/Hs-14_Conjugate_Pairs/`](experiments/Hs-14_Conjugate_Pairs/) |
| Hs-15 | materials | hBN dielectric tensor composition | [`experiments/Hs-15_hBN_Dielectric/`](experiments/Hs-15_hBN_Dielectric/) |
| Hs-16 | astrophysics | Planck cosmic microwave background composition | [`experiments/Hs-16_Planck_Cosmic/`](experiments/Hs-16_Planck_Cosmic/) |
| Hs-17 | reliability | Backblaze drive-fleet stress (D=4: Mechanical, Thermal, Age, Errors) | [`experiments/Hs-17_Backblaze/`](experiments/Hs-17_Backblaze/) |
| Hs-18 | urban | City of Markham operating-budget composition | [`experiments/Hs-18_Urban_Markham/`](experiments/Hs-18_Urban_Markham/) |
| Hs-19 | urban | Traffic signal-phase timing | [`experiments/Hs-19_Traffic_Signals/`](experiments/Hs-19_Traffic_Signals/) |
| Hs-20 | systems | Conversation-drift detection in dialogue corpora | [`experiments/Hs-20_Conversation_Drift/`](experiments/Hs-20_Conversation_Drift/) |
| Hs-21 | calibration | Reference-standard library cross-check | [`experiments/Hs-21_Reference_Standards/`](experiments/Hs-21_Reference_Standards/) |
| Hs-22 | systems | Natural-system pair study | [`experiments/Hs-22_Natural_Pairs/`](experiments/Hs-22_Natural_Pairs/) |
| Hs-23 | nuclear | Radionuclide decay chains (first new-methods experiment) | [`experiments/Hs-23_Radionuclides/`](experiments/Hs-23_Radionuclides/) |
| Hs-24 | physics | HEPData validation campaign | [`experiments/Hs-24_HEPData_Validation/`](experiments/Hs-24_HEPData_Validation/) |
| Hs-25 | astrophysics | Cosmic energy budget (Planck 2018 ΛCDM) | [`experiments/Hs-25_Cosmic_Energy_Budget/`](experiments/Hs-25_Cosmic_Energy_Budget/) |

**M-series (manifold + measurement calibration), April 29, 2026:**

| ID | Description | Folder |
|---|---|---|
| Hs-M01 | Manifold calibration (M-Series Experiment 1) | [`experiments/Hs-M01_Manifold_Calibration/`](experiments/Hs-M01_Manifold_Calibration/) |
| Hs-M02 | EMBER electricity-generation panel (M-Series Experiment 2) — first multi-country panel | [`experiments/Hs-M02_EMBER_Energy/`](experiments/Hs-M02_EMBER_Energy/) |
| Hs-MC4 | Shape calibration (cube/sphere/cylinder reference) | [`experiments/Hs-MC4_Shape_Calibration/`](experiments/Hs-MC4_Shape_Calibration/) |

**LAB / STD reference calibration:**

| ID | Description | Folder |
|---|---|---|
| Hs-LAB01 | Titration-standards 27-point calibration test set | [`experiments/Hs-LAB01_Titration_Standards/`](experiments/Hs-LAB01_Titration_Standards/) |
| Hs-STD | Standards test (cube / cylinder / sphere reference geometry) | [`experiments/Hs-STD_Standards_Test/`](experiments/Hs-STD_Standards_Test/) |

The narrative for this entire era — including the EITT analytic proof (April 28), the V-operator deep analysis (April 30), the trace formulation, the matrix integration — is in [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md) under the daily section headers from April 22 through April 30, 2026.


### 3.2 CNT v2.0.4 era full re-run — `experiments/Hs-CNT_2026-05/` (May 2026, push #14 onward)

The same compositional inputs as Hs-NN, re-run on the consolidated `cnt.py` engine at version 2.0.4 (schema 2.1.0). This is the **direct comparison set**: every input that produced a result under HUF 12-step also produced a result under CNT v2.0.4. The folder mirrors the structure used later by HCI-CNT/experiments/.

| Subfolder | Datasets covered | Note |
|---|---|---|
| `experiments/Hs-CNT_2026-05/codawork2026/` | EMBER 8 countries + combined panel + Backblaze fleet | First version of the CodaWork 2026 conference experiment set |
| `experiments/Hs-CNT_2026-05/domain/` | FAO irrigation + 6 geochem subsets (Ball-age/region/tas, Tappe-kim1, Qin-cpx, Stracke-OIB) | Domain-specific binners; used by the conference set |
| `experiments/Hs-CNT_2026-05/extended/` | Chemixhub oxide, ESA Planck cosmic, financial sector, IIASA NGFS, Markham budget | Extended demonstrations beyond the canonical CodaWork set |
| `experiments/Hs-CNT_2026-05/reference/` | Commodities gold-silver, Nuclear SEMF | Reference-standard stable benchmarks |

The same content was migrated to [`HCI-CNT/experiments/`](HCI-CNT/experiments/) at push #15 (folder rename + tier promotion); both locations now contain the v2.0.4 baseline outputs and they are the comparison-vs-v3 baseline used in the conference report.

### 3.3 CodaWork 2026 conference experiment — CNT v3.0.0 + CNQ v2.0.0 (push #32 + #33)

Production-grade, ready for June 2026 presentation.

| Component | Folder |
|---|---|
| Master comparison report | [`papers/codawork2026/conference_2026_06/COMPARISON_v2_0_4_vs_v3_0_0.md`](papers/codawork2026/conference_2026_06/COMPARISON_v2_0_4_vs_v3_0_0.md) |
| Per-country folders (8) + combined panel | [`papers/codawork2026/conference_2026_06/per_country/`](papers/codawork2026/conference_2026_06/per_country/) |
| Common-range 2001-2025 subset (CRD-1.0 demonstration) | `papers/codawork2026/conference_2026_06/common_range_2001_2025_headlines.json` |
| Runner | [`papers/codawork2026/conference_2026_06/run_ember_corpus.py`](papers/codawork2026/conference_2026_06/run_ember_corpus.py) |

Each per-country folder contains:

- `cnt_v3.json`, `cnq_v2.json` (engine outputs, deterministic, hash-chained)
- `STAGE_1_REPORT.md` (pure CoDa view — closure, CLR, ILR, variation matrix, section atlas)
- `ADVANCED_ANALYSIS.md` (full Hˢ + CNQ v2 — kappa^HS, depth tower, P2 attractor, helmsman family, IR class, bearing/radial trajectories)

### 3.4 Full-corpus validation — citation-grade reference suite (push #34, 2026-05-10)

The flagship deliverable. **101 datasets across 11 domains; 100 ran end-to-end**.

Master entry point: [`experiments/2026-05-10_full-corpus-validation/README.md`](experiments/2026-05-10_full-corpus-validation/README.md)

Sub-documents:

- [`MANIFEST.json`](experiments/2026-05-10_full-corpus-validation/MANIFEST.json) — every dataset registered with citation strings
- [`MASTER_FINDINGS.md`](experiments/2026-05-10_full-corpus-validation/MASTER_FINDINGS.md) — cross-domain digest
- [`DEFERRED_ADAPTERS.md`](experiments/2026-05-10_full-corpus-validation/DEFERRED_ADAPTERS.md) — Phase 3 priority queue
- [`all_headlines.json`](experiments/2026-05-10_full-corpus-validation/all_headlines.json) — machine-readable corpus headline

Per-domain summaries (link to `experiments/2026-05-10_full-corpus-validation/per_domain/<domain>/DOMAIN_SUMMARY.md`):

| Domain | Count | Summary | Notable |
|---|---|---|---|
| `energy` | 82 | [`per_domain/energy/DOMAIN_SUMMARY.md`](experiments/2026-05-10_full-corpus-validation/per_domain/energy/DOMAIN_SUMMARY.md) | EMBER 8 + combined panel + OWID 73 country trajectories (1965-2024 typical) |
| `geochemistry` | 7 | [`per_domain/geochemistry/DOMAIN_SUMMARY.md`](experiments/2026-05-10_full-corpus-validation/per_domain/geochemistry/DOMAIN_SUMMARY.md) | Stracke MORB/OIB, Ball age/region/tas, Tappe kim1, Qin cpx |
| `world_bank_fao` | 4 | [`per_domain/world_bank_fao/DOMAIN_SUMMARY.md`](experiments/2026-05-10_full-corpus-validation/per_domain/world_bank_fao/DOMAIN_SUMMARY.md) | FAO Credit/Value-Added pivots; one (food_mfg) surfaced an SEA-1.0 NUM finding |
| `backblaze` | 1 | [`per_domain/backblaze/DOMAIN_SUMMARY.md`](experiments/2026-05-10_full-corpus-validation/per_domain/backblaze/DOMAIN_SUMMARY.md) | Drive-fleet stress, T=731 daily |
| `chemistry` | 1 | [`per_domain/chemistry/DOMAIN_SUMMARY.md`](experiments/2026-05-10_full-corpus-validation/per_domain/chemistry/DOMAIN_SUMMARY.md) | ChemixHub oxide samples |
| `commodities` | 1 | [`per_domain/commodities/DOMAIN_SUMMARY.md`](experiments/2026-05-10_full-corpus-validation/per_domain/commodities/DOMAIN_SUMMARY.md) | Gold-silver D=2 minimum-dimension across 1338 years |
| `esa-planck` | 1 | [`per_domain/esa-planck/DOMAIN_SUMMARY.md`](experiments/2026-05-10_full-corpus-validation/per_domain/esa-planck/DOMAIN_SUMMARY.md) | LCDM cosmic vs redshift |
| `financial` | 1 | [`per_domain/financial/DOMAIN_SUMMARY.md`](experiments/2026-05-10_full-corpus-validation/per_domain/financial/DOMAIN_SUMMARY.md) | S&P 500 GICS daily sectors |
| `iiasa` | 1 | [`per_domain/iiasa/DOMAIN_SUMMARY.md`](experiments/2026-05-10_full-corpus-validation/per_domain/iiasa/DOMAIN_SUMMARY.md) | NGFS Phase-4 emission scenarios |
| `nuclear` | 1 | [`per_domain/nuclear/DOMAIN_SUMMARY.md`](experiments/2026-05-10_full-corpus-validation/per_domain/nuclear/DOMAIN_SUMMARY.md) | SEMF terms across the valley of stability |
| `urban` | 1 | [`per_domain/urban/DOMAIN_SUMMARY.md`](experiments/2026-05-10_full-corpus-validation/per_domain/urban/DOMAIN_SUMMARY.md) | Markham operating-budget composition |

Every per-dataset folder under `per_domain/<domain>/<dataset_id>/` contains four artefacts: `cnt_v3.json`, `cnq_v2.json`, `STAGE_1_REPORT.md`, `ADVANCED_ANALYSIS.md`. The two reports are designed for two audiences: Stage 1 = pure CoDa community; Advanced = the full Hˢ + CNQ v2 stack.


---

## 4. Cross-version diff highlights — what each version reveals that earlier versions did not

These are the items where a direct comparison between engine versions on the same input shows something concrete and citable.

### 4.1 Determinism and hash chains

| Version | Hash determinism | Cross-engine independence | Reproduction artefact |
|---|---|---|---|
| HUF 12-step | None — 12 scripts, ad-hoc intermediate files | N/A | Multi-language reports, no JSON contract |
| CNT v1.x | Single canonical JSON; first content-hash chain | N/A | First reproducible `content_sha256` |
| CNT v2.0.4 | Locked schema 2.x; per-version hash stable | None — single engine | [`HCI-CNT/engine/tests/test_determinism.py`](HCI-CNT/engine/tests/test_determinism.py) |
| CNQ v1.0.0 | Hash-chained but coupled to CNT (cross-engine hash) | Cross-engine hash chain produced false dependency | [`HCI-CNQ/archive/`](HCI-CNQ/archive/) |
| CNT v3.0.0 + CNQ v2.0.0 | Per-engine hash deterministic; cross-engine hash explicitly forbidden by policy | **Engine independence policy** — `cnt_content_sha256` and `cnq_content_sha256` are unrelated by design | 100 unique pairs across the full-corpus validation; non-identity is a feature, not a discrepancy |

### 4.2 IR class taxonomy

The Imaginary-Radius classifier names the damping signature of a compositional trajectory.

| Version | IR classes available | Edge cases handled | Notes |
|---|---|---|---|
| HUF 12-step | informal — labelled by inspection | none | qualitative |
| CNT v1.x | OVERDAMPED, UNDAMPED, LIMIT_CYCLE | T=2 boundary fragile | discovery phase |
| CNT v2.0.3 (mid-May 2026) | OVERDAMPED + OVERDAMPED_EXTREME, MODERATELY_DAMPED, LIGHTLY_DAMPED, CRITICALLY_DAMPED, UNDAMPED, LIMIT_CYCLE_P2 | off-by-one edge fixed in v2.0.3 | first 7-class taxonomy |
| CNT v2.0.4 | same | T=1 + D=2 explicitly handled | stable |
| CNT v3.0.0 | same + D2_DEGENERATE (explicit branch for the D=2 minimum-dimension case) | every edge enumerated under SEA-1.0 | every IR class exercised in Phase 1 + 2 corpus |

The push #34 corpus is what proved the taxonomy is exhaustive on real data: 100 datasets distributed across all IR classes (OVERDAMPED_EXTREME 26, MODERATELY_DAMPED 17, LIGHTLY_DAMPED 54, CRITICALLY_DAMPED 2, D2_DEGENERATE 1).

### 4.3 Numerical anchors over the lineage

The "IEEE floor confirmations" are the headline numerical events.

| Date | Engine | Dataset | Anchor | Significance |
|---|---|---|---|---|
| 2026-05-07 | CNT v2.0.4 + CNQ v0 (QD experimental) | Backblaze fleet | M²=I residual **4.441e-16** | First IEEE-floor confirmation; basis of the Volume IV "CNT measures invariance" claim |
| 2026-05-07 | CNT v2.0.4 + CNQ v0 | Planck CMB polarization | M²=I residual **4.441e-16 + M²=I 7.63e-17** | Falsified the original P2-vs-P1 fermion/boson reading (INV-002 FALSIFIED) and reformulated as universality — pure photons terminated at LIMIT_CYCLE_P2, not P1 |
| 2026-05-07 | CNT v2.0.4 + CNQ v0 | Standard-Model neutrino oscillation | LIMIT_CYCLE_P2 + M²=I **7.40e-17** | Third IEEE-floor confirmation across disparate physics — this is what triggered CNQ promotion from experimental to canonical (push #23) |
| 2026-05-09 | CNT v3.0.0 + CNQ v2.0.0 | EMBER 8-country corpus, conference run | All 8 countries M²=I < 3.30e-13 | First production corpus run on the rebuilt engines |
| 2026-05-10 | CNT v3.0.0 + CNQ v2.0.0 | Full-corpus validation, 100 datasets | All 100 M²=I verified at IEEE floor; worst residual **3.30e-13** | The first time the corpus has been run end-to-end on real data spanning 11 domains with documented sources |

### 4.4 Vocabulary and notation lineage

Each version refined the vocabulary.

| Term | First introduced | Where locked | Why it changed |
|---|---|---|---|
| `kappa^HS` (order-2 metric tensor) vs `s_j` (order-1 sensitivity vector) | Push #27 | [`HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md`](HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md) | Earlier docs conflated metric and sensitivity — push #27 separated them |
| "rank" → "order" sweep | Push #27 | NOTATION + GLOSSARY | Rank was overloaded with linear-algebra meaning; "order" is unambiguous for stage-1, stage-2, etc. |
| Helmsman family channels (sigma, sign, flips, stability_S_sigma, chaos_indicator, torque_proxy) | Push #24 (Grok cross-check) | [`HCI-CNT/handbook/GLOSSARY.md`](HCI-CNT/handbook/GLOSSARY.md) §I | Earlier the helmsman was a single number; Grok surfaced the channel decomposition |
| HCI instrument-family terms (HLR, kappa^HS, DCDI/Helmsman, Multiplexed Carrier Section Plate, System Course Plot, HCI Barycentric Navigation Volume, HCI Spatial Morphographic Analyzer) | Push #23 (ChatGPT cross-check) | GLOSSARY §H | Promoted from HCI-side prior work into the canonical glossary |
| "twin-quaternion factoring" (D=8 native) and "quad-quaternion factoring" (D=16 schema-locked) | Push #32 | [`docs/SUSPICION_OF_EVERY_ASSUMPTION.md`](docs/SUSPICION_OF_EVERY_ASSUMPTION.md) anti-spec, design doc | The CNQ v2 design doc made the D=8 and D=16 cases load-bearing-vs-schema-locked distinction explicit |

### 4.5 Doctrine adoption

The framework's binding doctrines are:

1. **SEA-1.0** ([`docs/SUSPICION_OF_EVERY_ASSUMPTION.md`](docs/SUSPICION_OF_EVERY_ASSUMPTION.md)) — every public function and claim enumerates its failure modes with mitigation evidence (push #32, INV-045)
2. **STP-1.0** ([`docs/SELF_TEST_PROTOCOL.md`](docs/SELF_TEST_PROTOCOL.md)) — every engine carries a frozen reference corpus and a runner that produces dated, hash-chained pass/fail receipts (push #32, INV-046)
3. **CRD-1.0** ([`docs/COHERENT_RANGE_DOCTRINE.md`](docs/COHERENT_RANGE_DOCTRINE.md)) — every multi-carrier comparison is computed on the intersection of all members' time ranges (push #33, INV-047)
4. **Engine independence** — each engine deterministic on its own; no cross-engine hash chain (push #32 design doc)

The four together are the **discipline boundary** between the v2.0.4 era (where bugs accumulated until external review found them) and the v3.0.0 era (where the engine's failure space is enumerated and dispatched during construction).


---

## 5. Push-by-push event log

A condensed event log for the CNT v2 → v3 transition window, in chronological order. Each push has its own AI refresh narrative (linked).

| Push | Date | Headline event | Narrative |
|---|---|---|---|
| #14 | 2026-05-05 | cnt_v2 single-engine canonical JSON generator (v2.0.0 → 2.0.4 incremental) | [`AI_REFRESH_2026-05-05.md`](ai-refresh/AI_REFRESH_2026-05-05.md) |
| #15 | 2026-05-06 | HCI-CNT folded into Hˢ as canonical tier | [`AI_REFRESH_2026-05-06_HCI-CNT_migration.md`](ai-refresh/AI_REFRESH_2026-05-06_HCI-CNT_migration.md) |
| #16-18 | 2026-05-06 | Push-procedure compliance audit + tier organisation | [`PUSH16_AUDIT_REPORT_2026-05-06.md`](ai-refresh/PUSH16_AUDIT_REPORT_2026-05-06.md), [`PUSH17_AUDIT_REPORT_2026-05-06.md`](ai-refresh/PUSH17_AUDIT_REPORT_2026-05-06.md), [`PUSH18_AUDIT_REPORT_2026-05-06.md`](ai-refresh/PUSH18_AUDIT_REPORT_2026-05-06.md) |
| #19 | 2026-05-06 | Dual-folder layout decided (HCI-CNT + experiments/Hs-CNT_2026-05) | [`AI_REFRESH_2026-05-06_push_19_and_dual_folder.md`](ai-refresh/AI_REFRESH_2026-05-06_push_19_and_dual_folder.md) |
| #20-21 | 2026-05-06 | OPERATIONS_PROTOCOL Gawande meta-checklist + CCTT cross-check tool test | [`PUSH21_AUDIT_REPORT_2026-05-06.md`](ai-refresh/PUSH21_AUDIT_REPORT_2026-05-06.md) |
| #22 | 2026-05-07 | Volume IV — Quaternion View — three IEEE-floor confirmations (Backblaze, Planck, neutrino) | [`AI_REFRESH_2026-05-07_quaternion_integration.md`](ai-refresh/AI_REFRESH_2026-05-07_quaternion_integration.md) |
| #23 | 2026-05-07 | ChatGPT cross-check round 1 — HCI vocabulary + tone calibration; CNQ tier promoted to canonical | [`AI_REFRESH_2026-05-07_push23_chatgpt_integration.md`](ai-refresh/AI_REFRESH_2026-05-07_push23_chatgpt_integration.md) |
| #24 | 2026-05-08 | Grok cross-check round 1 — DADC origin lineage + helmsman family extensions + HCI-AUDIO/HCI-ULTRASOUND tiers | [`AI_REFRESH_2026-05-08_push24_grok_crosscheck.md`](ai-refresh/AI_REFRESH_2026-05-08_push24_grok_crosscheck.md) |
| #26 | 2026-05-08 | CNQ v1.0.0 production engine landed (Hamilton-product core, full reproduction harness) | [`AI_REFRESH_2026-05-08_push26_chatgpt_round2_audit.md`](ai-refresh/AI_REFRESH_2026-05-08_push26_chatgpt_round2_audit.md) |
| #27 | 2026-05-08 | NOTATION_AND_TERMINOLOGY.md canonical reference + κᴴˢ vs s_j sweep | [`AI_REFRESH_2026-05-08_push26_27_chatgpt_round2_engine_terminology.md`](ai-refresh/AI_REFRESH_2026-05-08_push26_27_chatgpt_round2_engine_terminology.md) |
| #27b | 2026-05-08 | Full publication readiness: cnq.R, CNQ_PSEUDOCODE.md, 43-test suite, HS_FAST_REFRESH.json, PUBLICATION_READY.md | [`AI_REFRESH_2026-05-08_push27_full_publication.md`](ai-refresh/AI_REFRESH_2026-05-08_push27_full_publication.md) |
| #28a | 2026-05-08 | External-audit response: pyproject.toml, dual license (Apache-2.0 + CC BY 4.0), QUICKSTART.md | [`AI_REFRESH_2026-05-08_push28a_external_audit_response.md`](ai-refresh/AI_REFRESH_2026-05-08_push28a_external_audit_response.md) |
| #29 | 2026-05-08 | AI-loader visibility: llms.txt, .well-known/ai-context.json, AI_AGENTS.md, grounding-test SHA | [`AI_REFRESH_2026-05-08_push29_ai_visibility_grok_response.md`](ai-refresh/AI_REFRESH_2026-05-08_push29_ai_visibility_grok_response.md) |
| #30 | 2026-05-08 | Grok round 3 — three DEFERRED catalog entries; speculation discipline holds | [`AI_REFRESH_2026-05-08_push30_grok_round3_catalog.md`](ai-refresh/AI_REFRESH_2026-05-08_push30_grok_round3_catalog.md) |
| #31 | 2026-05-08 | License clarity: rename LICENSE-DOCS, write LICENSING.md, update NOTICE | [`AI_REFRESH_2026-05-08_push31_license_clarity.md`](ai-refresh/AI_REFRESH_2026-05-08_push31_license_clarity.md) |
| **#32** | **2026-05-09** | **Engine v3.0.0 / v2.0.0 ground-up rebuild** + four doctrines + UN-6 wrappers + R ports + cross-language parity + EMBER conference corpus | [`AI_REFRESH_2026-05-09_push32_engine_v3_v2_rebuild.md`](ai-refresh/AI_REFRESH_2026-05-09_push32_engine_v3_v2_rebuild.md) |
| **#33** | **2026-05-10 morning** | **Coherent Range Doctrine CRD-1.0** raised by Peter; codified across runner + comparison report + anti-spec + INV-047 | (catalog INV-047 + this journal §2) |
| **#34** | **2026-05-10 afternoon** | **Full-corpus validation reference suite** — 18 → 101 datasets across 11 domains + INV-048 + this journal | (catalog INV-048 + experiments folder README) |
| **#35** | **2026-05-10** | EXPERIMENTS_JOURNAL.md + admin JSON sweep (this document) | (administrative; no new INV) |
| **#36** | **2026-05-10** | CoDaWork 2026 redirect priority + planning folder + master plan | (catalog INV references; planning artefacts) |
| **#37** | **2026-05-10** | **CNT v3.1.0 — navigation_concentration_family promoted into canonical engine.** TV distance + K_eff + concentration regime tag (one of `tightening`/`loosening`/`deceptive`/`stable`) now produced natively per timestep. The HUF MC-4 packet operators are now permanent engine diagnostics. Schema bumped 3.0.0 → 3.1.0. 5 of 9 EMBER countries (AUS, CHN, GBR, IND, JPN) show non-zero `deceptive` regime counts at annual grain. | [catalog INV-049](ai-refresh/INVESTIGATION_CATALOG.json) |
| **#52** | **2026-05-19** | **🏁 Point-of-restore milestone — CoDaWork 2026 conference-ready.** **CNT v3.2.0** lands the new `navigation_2d` block — ILR-Helmert PCA barycenter trajectory, scaled to unit disk, with `pc1_direction`, `pc2_direction`, `variance_explained`, `bary_xy[t]`. Backwards-compatible: every v3.1.0 field unchanged; v3.2.0 outputs are supersets of v3.1.0 outputs. Conference corpus (`CODA-Association/CODAwork2026/data_outputs/per_country_json/cnt_v3/`) stays pinned to v3.1.0 — not regenerated under the pre-conference lockdown. The same math reaches the projector via sidecar `outputs/regen_baryxy.py`. **Projector v2.0** adopts the three-mode standard (RADAR / BARY / ALIGN) plus SHOCK overlay. Japan PC1+PC2 = 99.2 %; Germany 90.5 % (most multi-D); USA / World aggregate / India / China all > 99 %. **Manuscript v1.3** adds cover page + TOC + scientific-report layout. Five-piece bundle locked. R-port v3.2.0 + admin-JSON sync queued for post-conference. | [`AI_REFRESH_2026-05-19_conference_ready.md`](ai-refresh/AI_REFRESH_2026-05-19_conference_ready.md) · INV-064 (queued) |

---

## 6. Investigation catalog cross-reference

The investigation catalog ([`ai-refresh/INVESTIGATION_CATALOG.json`](ai-refresh/INVESTIGATION_CATALOG.json)) records every speculative branch, hypothesis, falsification, and graduation. Current state: **48 investigations registered, 26 CANONICAL, 12 DEFERRED, 1 FALSIFIED, 1 CLOSED, 8 OPEN.**

Highlights tied to specific experiments:

- **INV-001 (CANONICAL)** — Volume IV Quaternion View; promoted on three IEEE-floor confirmations (Backblaze, Planck, neutrino)
- **INV-002 (FALSIFIED)** — original P2-vs-P1 fermion/boson reading; refuted by Planck CMB → reformulated as universality
- **INV-021 (CANONICAL)** — CNQ v1.0.0 production engine
- **INV-024 (CANONICAL)** — HCI-AUDIO applied tier registered
- **INV-029 (CANONICAL)** — twin-quaternion factoring at D=8 (push #32)
- **INV-031 (CANONICAL)** — AI platform fitness audit
- **INV-045 (CANONICAL)** — SEA-1.0 doctrine
- **INV-046 (CANONICAL)** — STP-1.0 BIST doctrine
- **INV-047 (CANONICAL)** — CRD-1.0 doctrine (push #33)
- **INV-048 (CANONICAL)** — full-corpus validation reference suite (push #34)

The full catalog has the entry for every line of work that has ever been raised, with disposition and gate criteria. It is the project's research-methodology equivalent of the determinism contract: the path of every idea is traceable.

---

## 7. Citations and reproduction

**For citing a specific experiment's analysis,** cite:

1. The dataset's **source** (the `citation` field in [`experiments/2026-05-10_full-corpus-validation/MANIFEST.json`](experiments/2026-05-10_full-corpus-validation/MANIFEST.json) for v3-era runs; the `JOURNAL.md` for HUF-era runs)
2. The engine **version + content_sha256** (printed at the top of every report)
3. The **runner command** (in the experiment folder's README) for reproduction

For example, for the EMBER USA energy generation under CNT v3 + CNQ v2:
- Source: EMBER Climate, country = USA, electricity-generation-by-source TWh, 2001–2025
- Engine output: [`experiments/2026-05-10_full-corpus-validation/per_domain/energy/energy_ember_usa/cnt_v3.json`](experiments/2026-05-10_full-corpus-validation/per_domain/energy/energy_ember_usa/cnt_v3.json) (carries `cnt_content_sha256`)
- Reproduction: `python3 experiments/2026-05-10_full-corpus-validation/run_full_corpus.py`

**For citing the framework as a whole,** start with [`PUBLICATION_READY.md`](PUBLICATION_READY.md) at the repo root; that document is the single canonical entry point for external reviewers.

**For citing a specific theoretical claim,** cite the handbook volume that owns the claim:
- Volume I: [`HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md`](HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md)
- Volume II: [`HCI-CNT/handbook/VOLUME_2_INSTRUMENTATION_AND_PROTOCOLS.md`](HCI-CNT/handbook/VOLUME_2_INSTRUMENTATION_AND_PROTOCOLS.md)
- Volume III: [`HCI-CNT/handbook/VOLUME_3_APPLIED_DOMAINS.md`](HCI-CNT/handbook/VOLUME_3_APPLIED_DOMAINS.md)
- Volume IV: [`HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md`](HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md) (CNQ central claim)
- Origin lineage: [`HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md) (DADC → H₁ → HUF → Hˢ → CNT → CNQ)

---

## 8. Reading paths by audience

**For a CoDa-community reviewer** (1 hour): start with one Stage 1 report under `experiments/2026-05-10_full-corpus-validation/per_domain/<domain>/<dataset>/STAGE_1_REPORT.md`, then read [`HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md`](HCI-CNT/handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md) for the mathematical foundations.

**For a reviewer interested in dynamical systems** (1 hour): start with one Advanced report under the same path (e.g., [`per_domain/esa-planck/esa_planck_cosmic/ADVANCED_ANALYSIS.md`](experiments/2026-05-10_full-corpus-validation/per_domain/esa-planck/esa_planck_cosmic/ADVANCED_ANALYSIS.md)), then read [`HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md`](HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md).

**For a software engineer looking at the engine** (1 hour): read [`HCI-CNT/engine/cnt.py`](HCI-CNT/engine/cnt.py), [`HCI-CNQ/engine/cnq.py`](HCI-CNQ/engine/cnq.py), and the BIST runner at [`HCI-CNQ/engine/self_test/run_self_test.py`](HCI-CNQ/engine/self_test/run_self_test.py).

**For an external auditor / AI cross-check** (2 hours): read [`AI_AGENTS.md`](AI_AGENTS.md) and [`docs/SUSPICION_OF_EVERY_ASSUMPTION.md`](docs/SUSPICION_OF_EVERY_ASSUMPTION.md), then [`HCI-CNT/engine/ANTI_SPECIFICATION.md`](HCI-CNT/engine/ANTI_SPECIFICATION.md) and [`HCI-CNQ/engine/ANTI_SPECIFICATION.md`](HCI-CNQ/engine/ANTI_SPECIFICATION.md). Try to find a failure mode that's not enumerated.

**For a project historian / cold-start AI** (3 hours): read this journal end-to-end, then [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md), then the push narratives in chronological order under [`ai-refresh/`](ai-refresh/).

---

## 9. Refresh contract

This journal is refreshed at every push. Each entry to **§5 (push event log)** is added the same day the push lands. Each entry to **§3 (sequential ledger)** is added when a new experiment folder lands. Each entry to **§4 (cross-version diff)** is added when an engine-version transition occurs. The catalog cross-reference in **§6** is regenerated from the current INVESTIGATION_CATALOG.json on each push.

**Last refresh:** 2026-05-19 (push #52, point-of-restore milestone; engine v3.2.0 + projector v2.0 + manuscript v1.3; INV-064 queued)

---

*This document is itself an artefact of the SEA-1.0 doctrine: the failure mode it dispatches is "a reader cannot trace what has been done, on what version, in what order." Every link in this document is meant to be followed.*
