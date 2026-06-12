# Push #18 Audit Report — Hs-CNT_2026-05 corpus snapshot

**Date:** 2026-05-06
**Last validated push:** `0efda90` (Validate Repository #17 — HCI Community)
**Next push:** #18 — dated CNT corpus snapshot under Hs/experiments/
**Status:** **READY TO PUSH**

---

## What this push adds

A new dated experiment-series folder `experiments/Hs-CNT_2026-05/` is
added to the Hs research repository. It is the **release snapshot** of
the 25-experiment HCI-CNT canonical corpus at engine 2.0.4 / schema
2.1.0, sitting alongside the historical Hs-01 to Hs-25 experiment
series.

## Why a dated snapshot

The Hs/experiments/ tree has historically been the experiment line of
the Hs research repo. The Hs-01 to Hs-25 experiments date from before
CNT and use the original Hs pipeline. The new CNT corpus was developed
under the HCI-CNT/ subsystem and lives there for engine working
purposes (Stage 1/2/3/4 atlas modules read from
HCI-CNT/experiments/).

Adding a dated snapshot under Hs/experiments/ does three things:

1. Brings the CNT corpus into the standard discoverable location for
   anyone browsing the Hs experiment line.
2. Captures the canonical state at a specific engine version — the
   "as-published" record at engine 2.0.4 / schema 2.1.0.
3. Keeps the historical Hs-01 to Hs-25 experiments unchanged; both
   series remain part of the Hs canon.

When the engine evolves and re-runs the corpus, the next dated
snapshot folder (`Hs-CNT_<later-date>/`) captures the new state.
Earlier snapshots remain for lineage.

## What's in the snapshot

```
experiments/Hs-CNT_2026-05/
├── README.md                           full corpus inventory + verification recipe
├── INDEX.json                          25-experiment registry (engine 2.0.4 / schema 2.1.0)
├── codawork2026/                       10 experiments
│   ├── ember_chn/  ember_deu/  ember_fra/  ember_gbr/
│   ├── ember_ind/  ember_jpn/  ember_usa/  ember_wld/
│   ├── ember_combined_panel/
│   └── backblaze_fleet/
├── domain/                             8 experiments
│   ├── fao_irrigation_methods/
│   ├── geochem_ball_age/  geochem_ball_region/  geochem_ball_tas/
│   ├── geochem_qin_cpx/
│   ├── geochem_stracke_morb/  geochem_stracke_oib/
│   └── geochem_tappe_kim1/
├── reference/                          2 experiments
│   ├── commodities_gold_silver/
│   └── nuclear_semf/
└── extended/                           5 experiments (v1.1.x additions)
    ├── chemixhub_oxide/
    ├── esa_planck_cosmic/
    ├── financial_sector/
    ├── iiasa_ngfs/
    └── markham_budget/
```

72 total files.

Each experiment ships with its canonical JSON output (`<id>_cnt.json`)
and JOURNAL.md. The codawork2026 / reference / extended subfolders
also ship the input CSV alongside. The domain subfolder's input data
is regenerable from the adapters in `HCI-CNT/adapters/` against the
raw datasets in `DATA/` (this matches the canonical
`HCI-CNT/experiments/` layout and is documented in the snapshot
README).

## Per-experiment integrity check (8 representative samples)

```
codawork2026/ember_jpn:        csv ✓  json ✓  journal ✓  (cnt 2.0.4 / 2.1.0)
codawork2026/ember_chn:        csv ✓  json ✓  journal ✓  (cnt 2.0.4 / 2.1.0)
codawork2026/backblaze_fleet:  csv ✓  json ✓  journal ✓  (cnt 2.0.4 / 2.1.0)
domain/fao_irrigation_methods: csv −  json ✓  journal ✓  (cnt 2.0.4 / 2.1.0)
domain/geochem_tappe_kim1:     csv −  json ✓  journal ✓  (cnt 2.0.4 / 2.1.0)
reference/nuclear_semf:        csv ✓  json ✓  journal ✓  (cnt 2.0.4 / 2.1.0)
extended/markham_budget:       csv ✓  json ✓  journal ✓  (cnt 2.0.4 / 2.1.0)
extended/financial_sector:     csv ✓  json ✓  journal ✓  (cnt 2.0.4 / 2.1.0)
```

All 25 experiments at engine 2.0.4 / schema 2.1.0.

## Files added by push #18

```
experiments/Hs-CNT_2026-05/                            (72 files, 25 experiments)
ai-refresh/PUSH18_AUDIT_REPORT_2026-05-06.md           (this file)
```

## Files modified by push #18

```
ai-refresh/HS_ADMIN.json                  (experiment_series block added)
ai-refresh/HS_SYSTEM_INVENTORY.json        (experiment_series block added)
ai-refresh/PROJECT_HISTORY.json            (phase 28 appended)
```

## Carryover (still pending from push #17)

```
HCI-CNT/conference_demo/talk_deck/lu4422tlij.tmp       (LibreOffice temp leak)
```

The new HCI-CNT/.gitignore (push #16) blocks future leaks. Single
`git rm` on this file at any future push tidies it. Not blocking,
not visible to community-standards check, doesn't appear in any
user-facing artefact.

## Recommended commit + push

From the parent `Current-Repo/Hs/` directory:

```bash
git add experiments/Hs-CNT_2026-05/
git add ai-refresh/HS_ADMIN.json ai-refresh/HS_SYSTEM_INVENTORY.json
git add ai-refresh/PROJECT_HISTORY.json
git add ai-refresh/PUSH18_AUDIT_REPORT_2026-05-06.md
git rm  HCI-CNT/conference_demo/talk_deck/lu4422tlij.tmp 2>/dev/null
git commit -m "experiments/Hs-CNT_2026-05: dated release snapshot of the 25-experiment CNT canonical corpus"
git push origin main
```

## What this push communicates

The single repository now contains both experiment series side by side:
the historical Hs pipeline (Hs-01..Hs-25) and the CNT canonical corpus
(Hs-CNT_2026-05). A reader browsing the Hs/experiments/ tree finds
both in one place. The CNT corpus is no longer "off in HCI-CNT/" from
the Hs research perspective; it's a dated experiment series in the
canonical Hs experiments line, fully discoverable.

This makes the consolidated repository the single, complete home of
the Higgins research line — Hs as the canonical research repo, CNT as
the core engine within it, and the experiment record laid out in the
expected location for both the historical and the current series.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
