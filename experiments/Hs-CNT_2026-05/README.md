# Hs-CNT_2026-05 — Compositional Navigation Tensor canonical corpus

**Date:** 2026-05-06   **Engine:** cnt 2.0.4   **Schema:** 2.1.0
**Determinism gate:** 25 PASS / 0 FAIL / 0 ERR

This folder is the dated release snapshot of the 25-experiment canonical
corpus produced by the HCI-CNT subsystem (`HCI-CNT/`). Each experiment
ships as a self-contained record:

* `<id>_input.csv` — the raw input (file-hashed)
* `<id>_cnt.json` — the canonical engine output (content-hashed; conforms
  to schema 2.1.0; carries the full audit trail in
  `metadata.engine_config.engine_signature` + `inp.source_file_sha256` +
  `diagnostics.content_sha256`)
* `JOURNAL.md` — the auto-generated narrative summary with IR
  classification, amplitude A, depth tower depths, and the per-experiment
  conclusion

This snapshot sits alongside the historical Hs-01 to Hs-25 experiment
series. Both series remain part of the Hs canon. The Hs- series predates
CNT and uses the original Hs pipeline; the Hs-CNT_2026-05 series uses the
CNT engine and produces the audit-traceable JSON-and-PDF chain documented
in [`HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md`](../../HCI-CNT/handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md).

## Corpus inventory (25 experiments)

### codawork2026/ — energy + reliability domain (10)
| ID | T | D | IR class |
|---|---:|---:|---|
| ember_chn | 26 | 8 | (see JSON) |
| ember_deu | 26 | 9 | (see JSON) |
| ember_fra | 26 | 9 | (see JSON) |
| ember_gbr | 26 | 9 | (see JSON) |
| ember_ind | 26 | 8 | (see JSON) |
| ember_jpn | 26 | 8 | (see JSON) |
| ember_usa | 25 | 9 | (see JSON) |
| ember_wld | 26 | 9 | (see JSON) |
| ember_combined_panel | 209 | 8 | (see JSON) |
| backblaze_fleet | varies | varies | (see JSON) |

### domain/ — geochemistry + irrigation (8)
| ID | T | D | IR class |
|---|---:|---:|---|
| fao_irrigation_methods | 83 | 3 | (see JSON) |
| geochem_ball_age | varies | varies | (see JSON) |
| geochem_ball_region | varies | varies | (see JSON) |
| geochem_ball_tas | varies | varies | (see JSON) |
| geochem_qin_cpx | varies | varies | (see JSON) |
| geochem_stracke_morb | varies | varies | (see JSON) |
| geochem_stracke_oib | varies | varies | (see JSON) |
| geochem_tappe_kim1 | 8 | 10 | (see JSON) |

### reference/ — transcendental-constant references (2)
| ID | T | D | IR class |
|---|---:|---:|---|
| commodities_gold_silver | varies | 2 | (see JSON) |
| nuclear_semf | varies | varies | (see JSON) |

### extended/ — v1.1.x additions (5)
| ID | T | D | Notes |
|---|---:|---:|---|
| markham_budget    | 15  | 8  | Synthetic baseline; raw-data swap-in path documented in Volume II §C |
| iiasa_ngfs        | 31  | 7  | Synthetic baseline (NZ-2050 sectors); raw IAMC swap-in documented |
| esa_planck_cosmic | 17  | 5  | Closed-form Friedmann scaling (Planck 2018 ΛCDM); mathematically exact |
| financial_sector  | 252 | 10 | Synthetic baseline from S&P 500 GICS weights; raw-CSV swap-in documented |
| chemixhub_oxide   | 24  | 7  | Synthetic baseline (HOIP-7 oxide profile); ChemixHub native loader documented |

The extended battery is fully disclosed at the top of each adapter
(`HCI-CNT/adapters/<adapter>.py`) and in
[`HCI-CNT/handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md`](../../HCI-CNT/handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md)
Part C.

## Verification

Each experiment is independently verifiable:

```bash
cd <repo-root>
sha256sum experiments/Hs-CNT_2026-05/codawork2026/ember_jpn/ember_JPN_*.csv
# → must match inp.source_file_sha256 in ember_jpn_cnt.json
python HCI-CNT/mission_command/mission_command.py ember_jpn
# → must produce identical content_sha256 to the published one in this snapshot
```

The full corpus runs in ~21 seconds; the determinism gate passes
25/25 byte-identically on each invocation.

## Relationship to HCI-CNT/experiments/

`HCI-CNT/experiments/` is the live working folder used by the engine
and the Stage 1/2/3/4 atlas modules. `Hs/experiments/Hs-CNT_2026-05/`
is the **dated release snapshot** of the same content at the time of
push #18. The two will drift over time as the engine evolves; this
snapshot remains the "as-published" record at engine 2.0.4 / schema
2.1.0.

When future engine versions re-run the corpus, the next dated
snapshot folder (`Hs/experiments/Hs-CNT_<later-date>/`) is the right
place to capture the new state. The historical snapshots are kept
for lineage.


## A note on input CSVs

For the **codawork2026/**, **reference/**, and **extended/** subfolders,
each experiment ships with its `<id>_input.csv` alongside the canonical
`<id>_cnt.json`. These can be hash-verified directly against
`inp.source_file_sha256` in the JSON.

For the **domain/** subfolder (geochemistry binnings + FAO irrigation),
the input CSVs are produced by the adapter scripts in
`HCI-CNT/adapters/` reading from raw third-party datasets in `DATA/`.
The `inp.source_file_sha256` and `inp.closed_data_sha256` fields in
each domain JSON identify the exact input bytes; to reproduce, run the
adapter from `HCI-CNT/adapters/<adapter>.py` against the raw data and
verify the SHAs match.

This split mirrors the canonical `HCI-CNT/experiments/` layout. The
codawork2026 / reference / extended inputs are bundled because they're
small and self-contained; the domain inputs are produced on demand
from the larger raw datasets in `DATA/` (which are not in the
repository because of file size and licensing).

---

## Citation

Cite the corpus as part of the HUF-CNT system reference:

```
Higgins, P. (2026). HUF-CNT System: Compositional Navigation Tensor
reference implementation, 25-experiment canonical corpus. Engine
2.0.4 / Schema 2.1.0, snapshot Hs-CNT_2026-05.
DOI: 10.5281/zenodo.XXXXXXX
```

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
