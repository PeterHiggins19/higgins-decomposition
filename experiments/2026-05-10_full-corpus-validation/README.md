# Full-corpus validation — 2026-05-10

**Experiment ID:** full-corpus-validation/2026-05-10
**Engines:** CNT v3.0.0 + CNQ v2.0.0 (push #32)
**Doctrines applied:** SEA-1.0, STP-1.0, CRD-1.0, engine-independence
**Run date:** 2026-05-10 (Phase 1 morning, Phase 2 afternoon)
**Status:** Phase 2 complete — **101 datasets registered, 100 ran end-to-end across 11 domains**

---

## Purpose

This experiment folder is the **citation-grade reference suite** for the latest CNT v3 + CNQ v2 engines applied across the entire DATA folder. Every dataset is a real-world compositional time-series with a documented source — **no simulated data**. The runs serve as the canonical worked examples for the Hs framework as of push #33 and are designed to be cited in future scientific reports.

## How to read this folder

1. **`MASTER_FINDINGS.md`** — single-page cross-domain digest. The cross-domain headline grid plus IR class distribution plus anomalies. Start here.

2. **`per_domain/<domain>/DOMAIN_SUMMARY.md`** — domain-level digest. One per domain; aggregates that domain's datasets in a compact table.

3. **`per_domain/<domain>/<dataset_id>/STAGE_1_REPORT.md`** — pure-CoDa view of one dataset. CoDa-community vocabulary only: closure, CLR, ILR, variation matrix τ_ij, carrier-pair Pearson r, section atlas. This is the entry point for a CoDa reviewer.

4. **`per_domain/<domain>/<dataset_id>/ADVANCED_ANALYSIS.md`** — full Hˢ + CNQ v2 view of one dataset. κ^HS metric, s_j sensitivity, depth tower with M²=I involution, P2 attractor fit, helmsman family, IR classification, plus the CNQ v2 quaternion view (bearing trajectory, radial trajectory, dimension policy).

5. **`per_domain/<domain>/<dataset_id>/cnt_v3.json` and `cnq_v2.json`** — the raw engine outputs, hash-chained and deterministic. Both files carry their own `content_sha256` for citation.

The split between Stage 1 and Advanced is deliberate: **Stage 1 = pure CoDa** (entry point in the community's own vocabulary); **Full CNQ = the more advanced option** (the Hˢ extension stack that justifies the framework's existence beyond standard CoDa).

## What's included (Phase 1 + Phase 2 — 101 datasets across 11 domains)

| Domain | Datasets | Note |
|---|---|---|
| `energy` | **82** | EMBER 8-country (USA, CHN, DEU, FRA, GBR, IND, JPN, WLD) + combined panel + **OWID primary-energy 73 countries** (1965-2024 typical) |
| `geochemistry` | **7** | Stracke MORB (5 ocean basins) + Stracke OIB (15 islands) + Ball age (10 epochs) + Ball region (95 regions) + Ball TAS (15 rock types) + Tappe kim1 (8 countries) + Qin Cpx (30 locations) |
| `world_bank_fao` | **4** | FAO Credit to Agriculture (top-10 countries) + FAO Value Added Agriculture / AFF / Food Mfg (top-10 each) |
| `backblaze` | 1 | Backblaze drive-fleet stress telemetry, daily 2024-01 through 2025-12 |
| `chemistry` | 1 | ChemixHub oxide compositional samples |
| `esa-planck` | 1 | LCDM cosmological energy-density vs redshift |
| `financial` | 1 | S&P 500 GICS sector composition, daily 1y |
| `iiasa` | 1 | NGFS Phase-4 emissions allocation by sector |
| `urban` | 1 | City of Markham operating-budget composition, fiscal years 2011-2025 |
| `commodities` | 1 | Annual gold-silver mass fraction, 1688-2025 (T = 1338) |
| `nuclear` | 1 | SEMF term decomposition across the valley of stability |

See `MANIFEST.json` for the full registered dataset list with citation strings and input-CSV paths. New Phase-2 adapter scripts live in `adapters/` (`owid_energy_adapter.py`, `fao_sdmx_adapter.py`); the geochem datasets came from the patched binners in `HCI-CNT/adapters/bin_*.py`.

**One dataset failed end-to-end** (`fao_value_added_food_mfg`): CNQ correctly refused to emit non-finite floats because the FAO indicator's reporting is discontinuous (different countries reporting in different years, producing near-degenerate trajectory geometry). This is a SEA-1.0 NUM-class failure mode catching real data quality issues — recorded explicitly in MASTER_FINDINGS.md anomalies, not silently dropped.

## Highlights — IR class diversity exercised

This corpus exercises essentially the entire IR taxonomy in a single run:

- **`OVERDAMPED_EXTREME`** (3 datasets) — USA, DEU, GBR EMBER; snap-to-attractor energy-mix dynamics in well-regulated grids.
- **`MODERATELY_DAMPED`** (5) — FRA EMBER, BackBlaze fleet, ChemixHub oxide, IIASA NGFS, Markham budget.
- **`LIGHTLY_DAMPED`** (7) — CHN/IND/JPN/WLD EMBER + combined panel, ESA Planck cosmic, Nuclear SEMF.
- **`CRITICALLY_DAMPED`** (2) — Stracke MORB, S&P 500 sectors.
- **`D2_DEGENERATE`** (1) — Gold-silver (D = 2 minimum dimension; engine handles via degenerate-pair branch).

That single corpus run covers the range from the most-damped to the most-cycling regimes the engine will classify, on real-world data. The classifications are not arbitrary: they emerge from the structure of the trajectory under the M²=I involution, and they match domain intuition (regulated grids damp hard, daily market sectors flip often, cosmological evolution is monotone).

## Highlights — domain-specific findings

**ESA Planck cosmic** — Pearson r = ±1.0000 across all carrier pairs. This is a deterministic correlation, not an artifact: LCDM evolution makes each species fraction a closed-form function of redshift, so Photons and Neutrinos (both ~ a⁻⁴) are in lockstep, Dark Energy and Cold Dark Matter are anti-correlated as they swap dominance over cosmic time, and Helmsman stability hits 1.0000 (zero flips, perfect monotone).

**Markham budget** — Helmsman stability 1.0000 across 15 fiscal years. Municipal operating budgets reallocate slowly; the dominant axis never flips. Anti-correlation pattern of Recreation & Culture vs. Operations & Asset Mgmt is the dominant pair.

**S&P 500 sectors** — 226 helmsman flips in T=252 trading days. Daily sector rotation is essentially noise at the dominant-axis level; this is exactly what one would expect from a market that is information-efficient on the day scale.

**USA EMBER** — T=25 (2001-2025) vs other countries' T=26 (2000-2025). The asymmetry is documented under CRD-1.0; the conference run uses the coherent 2001-2025 window across all 8 countries. See `papers/codawork2026/conference_2026_06/COMPARISON_v2_0_4_vs_v3_0_0.md` for the matched-window headline.

**Gold-silver D=2** — Engine handles the minimum-dimension case via the D2_DEGENERATE branch. T=1338 years of paired mass-fraction trajectory; cycle stability 0.879, amplitude 0.397.

## Determinism contract

Every dataset's output JSON carries a `content_sha256` that is reproducible across runs on the same input. Both engines (CNT and CNQ) compute disjoint hashes by design — engine independence (push #32 policy) — and both pass the M²=I involution check at IEEE floor (worst residual across the corpus: **3.300e-13**).

## How to reproduce

```bash
# From the repo root
PYTHONPYCACHEPREFIX=/tmp/hci_pyc_$RANDOM \
    python3 experiments/2026-05-10_full-corpus-validation/run_full_corpus.py
```

Reads `MANIFEST.json`, processes every registered dataset, regenerates every report. The runner produces identical SHA-256s on consecutive runs (modulo timestamp metadata).

## Citation

When citing a specific dataset's analysis from this corpus, cite the dataset's `cnt_content_sha256` (or `cnq_content_sha256`) for the engine output, plus the dataset's documented source (the `citation` field in `MANIFEST.json`). For the corpus as a whole, cite this README and the `MASTER_FINDINGS.md` SHA-256.

## Phase 2 — what's deferred and why

A meaningful slice of the DATA folder is not yet in the manifest because the input requires adapter work (raw → pipeline-ready CSV) that is best done with care, not rushed. See `DEFERRED_ADAPTERS.md` for the explicit list of deferred datasets, the reason each is deferred, and the work each one would require to land.

## Doctrine compliance

- **SEA-1.0** (Suspicion of Every Assumption) — every output is reviewable against the engine's anti-specification documents (`HCI-CNT/engine/ANTI_SPECIFICATION.md`, `HCI-CNQ/engine/ANTI_SPECIFICATION.md`).
- **STP-1.0** (Self-Test Protocol) — both engines pass their BIST corpus before any conclusions are drawn (see `HCI-CNQ/engine/self_test/RECEIPTS/`).
- **CRD-1.0** (Coherent Range Doctrine) — multi-carrier intra-domain comparisons (e.g., the EMBER 8-country panel) are run under coherent-range policy in `papers/codawork2026/conference_2026_06/`. The cross-domain master view shown here is heterogeneous by construction (different T, different D, different units across domains) and is not subject to CRD-1.0.
- **Engine independence (push #32)** — every dataset produces two independent SHA-256 fingerprints for CNT and CNQ outputs.

## Files in this folder

```
2026-05-10_full-corpus-validation/
├── README.md                        (this file)
├── MANIFEST.json                    (dataset registry)
├── MASTER_FINDINGS.md               (cross-domain digest)
├── DEFERRED_ADAPTERS.md             (Phase 2 work queue)
├── all_headlines.json               (machine-readable corpus headline)
├── run_full_corpus.py               (the runner)
├── report_lib.py                    (Stage 1 + Advanced report generators)
└── per_domain/
    ├── backblaze/
    │   ├── DOMAIN_SUMMARY.md
    │   └── backblaze_fleet/
    │       ├── cnt_v3.json
    │       ├── cnq_v2.json
    │       ├── STAGE_1_REPORT.md
    │       └── ADVANCED_ANALYSIS.md
    ├── chemistry/...
    ├── commodities/...
    ├── energy/...                   (9 EMBER datasets + combined panel)
    ├── esa-planck/...
    ├── financial/...
    ├── geochemistry/...
    ├── iiasa/...
    ├── nuclear/...
    └── urban/...
```

---

*Generated 2026-05-10. Engines: CNT v3.0.0 + CNQ v2.0.0. Catalog reference: INV-048.*
