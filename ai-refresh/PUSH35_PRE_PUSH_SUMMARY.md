# Push #35 — pre-push summary

**Date:** 2026-05-10
**Type:** doctrine + experiment-suite + admin sweep
**Catalog entries:** INV-047 (CRD-1.0, push #33), INV-048 (full-corpus validation, push #34); push #35 itself is administrative
**Catalog totals:** 48 investigations · 26 CANONICAL · 12 DEFERRED · 1 FALSIFIED · 1 CLOSED · 8 OPEN

---

## What's in this push (everything since push #32)

### Push #33 (morning) — Coherent Range Doctrine (CRD-1.0)

Multi-carrier comparisons must compute on the intersection of all members' time ranges. Triggered by the USA-EMBER missing-year-2000 asymmetry investigation: USA covers 2001–2025 (T=25), other 7 countries cover 2000–2025 (T=26). The doctrine forces the matched-window into the headline, names start-limiting and end-limiting carriers in the manifest, and provides a drop-and-recover rule for re-running with a limiting carrier excluded.

**Lands:**
- `docs/COHERENT_RANGE_DOCTRINE.md` (192 lines, 12 sections)
- `papers/codawork2026/conference_2026_06/run_ember_corpus.py` — `--range-policy {coherent|native|explicit}`, default `coherent`
- `papers/codawork2026/conference_2026_06/COMPARISON_v2_0_4_vs_v3_0_0.md` — headline restructured around 2001–2025 coherent window with manifest at top
- `papers/codawork2026/conference_2026_06/all_countries_headlines.json` — `coherent_range_manifest` as first key
- `HCI-CNT/engine/ANTI_SPECIFICATION.md` — `INTP_004` (CRD violation as headline)
- `HCI-CNQ/engine/ANTI_SPECIFICATION.md` — `INTP_005` + `WRP_007` (CRD violation + wrapper manifest loss)
- `Hs/README.md` — policy index updated; CRD-1.0 listed alongside SEA-1.0, STP-1.0, engine-independence
- `ai-refresh/INVESTIGATION_CATALOG.json` — INV-047 CANONICAL added

### Push #34 (afternoon) — Full-corpus validation reference suite

Citation-grade reference suite at `experiments/2026-05-10_full-corpus-validation/`. **101 datasets across 11 domains; 100 ran end-to-end through CNT v3 + CNQ v2.** The single failure (`fao_value_added_food_mfg`) is a SEA-1.0 NUM finding — CNQ correctly refused to emit non-finite floats from a discontinuous-reporting trajectory.

**Phase 1** (18 datasets, 10 domains): EMBER 8 + combined panel, BackBlaze fleet, Stracke MORB, ChemixHub oxide, ESA Planck cosmic, S&P 500 sectors, IIASA NGFS, Markham budget, Gold-silver D=2, Nuclear SEMF.

**Phase 2** (+83 datasets, +1 domain): 6 geochem datasets via patched binners (Ball age/region/tas, Tappe kim1, Qin cpx, Stracke OIB), 73 OWID per-country primary-energy compositions (1965–2024 typical), 4 FAO indicator pivots.

**Three new adapter classes shipped:**
- `HCI-CNT/adapters/bin_*.py` — patched DATA-walk-up resolution; 6 geochem datasets regenerated
- `experiments/2026-05-10_full-corpus-validation/adapters/owid_energy_adapter.py` — 73 country trajectories
- `experiments/2026-05-10_full-corpus-validation/adapters/fao_sdmx_adapter.py` — SDMX wide-format → top-N-country pivot

**Per-dataset artefacts:** `cnt_v3.json`, `cnq_v2.json`, `STAGE_1_REPORT.md` (pure CoDa), `ADVANCED_ANALYSIS.md` (full Hˢ + CNQ v2).

**Master deliverables:**
- `experiments/2026-05-10_full-corpus-validation/README.md` — citation entry point
- `experiments/2026-05-10_full-corpus-validation/MASTER_FINDINGS.md` — cross-domain digest
- `experiments/2026-05-10_full-corpus-validation/MANIFEST.json` — 101 datasets registered with citations
- `experiments/2026-05-10_full-corpus-validation/DEFERRED_ADAPTERS.md` — Phase 3 priority queue
- `experiments/2026-05-10_full-corpus-validation/all_headlines.json` — machine-readable headline
- `ai-refresh/INVESTIGATION_CATALOG.json` — INV-048 CANONICAL added

### Push #35 (this push) — EXPERIMENTS_JOURNAL.md + admin sweep

Master historical synthesis document at the repo root. Single citation-grade markdown documenting every experiment ever run under HUF / CNT v1 / CNT v2.0.4 / CNT v3.0.0 + CNQ v2.0.0, with engine-version transitions, what each version added, what each version revealed that predecessors did not, and direct links to every artefact.

**Lands:**
- `EXPERIMENTS_JOURNAL.md` (350 lines, 9 sections)
- `Hs/README.md` — two new placements (news banner + first "Start Here" entry)
- `ai-refresh/HS_ADMIN.json` — session_log entries for pushes #33, #34, #35
- `ai-refresh/HS_MACHINE_MANIFEST.json` — `doctrine_locks` includes CRD-1.0; experiment-suite + journal pointers
- `HS_FAST_REFRESH.json` — engine version pointers bumped from CNT 2.0.4 / CNQ 1.0.0 (stale) to CNT 3.0.0 / CNQ 2.0.0; `doctrine_pointers` block added
- `ai-refresh/PUSH35_PRE_PUSH_SUMMARY.md` (this document)

---

## Numerical anchors

| Anchor | Value | Source |
|---|---|---|
| Datasets in MANIFEST | 101 | `experiments/2026-05-10_full-corpus-validation/MANIFEST.json` |
| Datasets that ran end-to-end | 100 | `all_headlines.json` |
| Datasets with M²=I verified at IEEE floor | 100 / 100 | runner output |
| Worst M²=I residual across the corpus | **3.300e-13** | `energy_ember_usa` (long-T trajectory) |
| Unique `cnt_content_sha256` | 100 / 100 | engine independence holds |
| Unique `cnq_content_sha256` | 100 / 100 | engine independence holds |
| Investigation catalog total | 48 | up from 46 since push #32 |
| Investigation catalog CANONICAL | 26 | up from 24 |
| BIST (STP-1.0) latest receipt | `ALL_PASS` | `HCI-CNQ/engine/self_test/RECEIPTS/2026-05-10/155512_ALL_PASS.json` |

---

## Pre-push verification (all green)

- [x] All admin JSONs parse cleanly (`HS_ADMIN.json`, `HS_MACHINE_MANIFEST.json`, `HS_FAST_REFRESH.json`, `INVESTIGATION_CATALOG.json`, two `MANIFEST.json` files, two `all_headlines.json` files)
- [x] Investigation catalog math: total 48, dispositions sum to 48, sources sum to 48
- [x] Engine self-test (BIST) produces `ALL_PASS` receipt with chain link to previous receipt
- [x] Every artefact referenced from admin JSONs verified to exist (17/17)
- [x] Corpus integrity: 100/101 ran, all 100 M²=I at IEEE floor, all 100 hashes unique
- [x] `EXPERIMENTS_JOURNAL.md` linked from `Hs/README.md` in 2 places (banner + Start Here)
- [x] Doctrine docs reachable: SEA-1.0, STP-1.0, CRD-1.0, engine-independence
- [x] CRD-1.0 manifest header present in `papers/codawork2026/conference_2026_06/COMPARISON_v2_0_4_vs_v3_0_0.md`

---

## What this push does NOT change

- Engine source code (`cnt.py`, `cnt.R`, `cnq.py`, `cnq.R`) — unchanged since push #32
- BIST corpus (`HCI-CNQ/engine/self_test/standard_test_matrices.json`) — unchanged
- Schema (`CNT_JSON_SCHEMA.md`, `CNQ_SCHEMA.md`) — unchanged; CNT v3 / CNQ v2 schemas frozen at push #32
- Wrapper system (`HCI-CNQ/wrappers/`, audio/government-budget locales) — unchanged
- Handbook volumes I–IV — unchanged
- License (Apache-2.0 code + CC BY 4.0 docs) — unchanged

---

## Suggested commit message

```
Push #35 — EXPERIMENTS_JOURNAL.md + CRD-1.0 + corpus validation

PUSH #33 (CRD-1.0):
- docs/COHERENT_RANGE_DOCTRINE.md (12 sections, 192 lines)
- run_ember_corpus.py --range-policy flag (coherent default)
- Conference COMPARISON.md headline restructured for coherent window
- Anti-spec FM entries: INTP_004, INTP_005, WRP_007
- INV-047 CANONICAL

PUSH #34 (Full-corpus validation):
- experiments/2026-05-10_full-corpus-validation/ — 101 datasets, 11 domains
- 100 ran end-to-end on CNT v3.0.0 + CNQ v2.0.0
- Per-dataset Stage 1 + Advanced reports; master findings + manifest + deferred-adapters
- Three new adapter classes: geochem binners patched, owid_energy_adapter, fao_sdmx_adapter
- INV-048 CANONICAL

PUSH #35 (Journal + admin sweep):
- EXPERIMENTS_JOURNAL.md at repo root (350 lines, 9 sections)
- Linked from README.md (news banner + Start Here)
- HS_ADMIN.json + HS_MACHINE_MANIFEST.json + HS_FAST_REFRESH.json all updated
- HS_FAST_REFRESH engine pointers fixed: CNT 2.0.4 -> 3.0.0; CNQ 1.0.0 -> 2.0.0

All admin JSONs parse cleanly. BIST receipt: ALL_PASS.
Catalog: 48 investigations, 26 CANONICAL, 12 DEFERRED, 1 FALSIFIED, 1 CLOSED, 8 OPEN.
M²=I across the corpus: 100/100 verified at IEEE floor; worst 3.30e-13.
Engine independence: 100 unique cnt + 100 unique cnq fingerprints.
```

---

## Next-push queue (deferred items)

- Phase 2 corpus expansion completed; **Phase 3** items in `experiments/2026-05-10_full-corpus-validation/DEFERRED_ADAPTERS.md`
- INV-021 Round 3 full-corpus quaternion validation (long-standing priority)
- INV-026 arXiv submission of Paper 1
- INV-043 D=16 quad-quaternion implementation (gates on first D=16 dataset)
- HCI-AUDIO applied pilot full ship (months away per priority lock)
- D1 documentation refresh — README pointers and notation docs that still mention v2.0.4 in handbook prose

These remain in the OPEN / DEFERRED queue with explicit gates. Not blocking push #35.

---

*Generated 2026-05-10 as the standard pre-push hand-off card. Companion to `EXPERIMENTS_JOURNAL.md` and the per-domain summaries in `experiments/2026-05-10_full-corpus-validation/per_domain/`.*
