# Adapters — fully-disclosed pre-parsers

Each adapter converts raw third-party data into the canonical CNT input CSV
(label column + D carrier columns). Every adapter is fully disclosed: the
data source, the transformations applied, what is preserved, what is
dropped, and the SHA-256 of the output CSV are all in the source.

## Built-in adapters (13)

### Original 8 (codawork2026 + domain)
| Adapter | Source |
|---|---|
| `backblaze_adapter.py`        | BackBlaze hard-drive failure stats |
| `bin_ball_age_and_tas.py`     | EarthChem Ball — age epoch + TAS rock-type binning |
| `bin_ball_region.py`          | EarthChem Ball — geographic region binning |
| `bin_stracke_morb.py`         | EarthChem Stracke — MORB |
| `bin_stracke_oib.py`          | EarthChem Stracke — OIB |
| `bin_tappe_and_qin.py`        | EarthChem Tappe (kimberlites) + Qin (clinopyroxenes) |
| `ember_usa_2025_adapter.py`   | EMBER monthly long-format → USA 2025 yearly |
| `fao_irrigation_adapter.py`   | FAO/World Bank irrigation methods |

### v1.1.x extended battery (5 deferred-now-built)
| Adapter | Source recipe |
|---|---|
| `markham_budget.py`     | City of Markham 2018 operating-budget department shares + drift |
| `iiasa_ngfs.py`         | IIASA NGFS Phase-4 NZ-2050 sector emissions composition |
| `esa_planck_cosmic.py`  | Planck 2018 cosmic energy budget × redshift (Friedmann scaling, exact) |
| `financial_sector.py`   | S&P 500 GICS sector portfolio weights + daily drift |
| `chemixhub_oxide.py`    | ChemixHub HOIP-7 oxide composition profile |

The five extended adapters ship with synthetic baselines (clearly disclosed
at the top of each file). Raw-data swap-in paths are documented in
[`../handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md`](../handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md)
Part C.

## Disclosure registry

The full per-adapter disclosure (source, transformations, preserved fields,
discarded fields, SHA-256, cross-references) lives in the consolidated
handbook at
[`../handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md`](../handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md)
Part C.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
