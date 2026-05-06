# Deferred Adapters

**Date:** 2026-05-05
**Status:** These data sources have been surveyed and deferred. Each
entry documents what's required to bring the dataset into the v2.0.x
experiment battery.

---

## Why deferred

The 20 experiments currently in `experiments_v2/` cover the CoDaWork
2026 deliverable scope plus the core within-domain robustness
demonstrations. The datasets below are valid future-work targets but
require domain-specific adapter code that is not on the critical path
for the conference. Each is documented here so future work can pick up
where the survey left off.

---

## 1 — `DATA/Urban Data/Markham Project/`

**Status:** PENDING. Adapter not built.

**Source format:** Multiple Excel sheets covering Markham municipal
budgets, 2011–2018:

* `2018-Operating-Budget-by-Account.xlsx`
* `2018-Capital-Budget-by-Dept-and-Funding-Source.xlsx`
* `2018-Consolidated-Budget-by-Dept-and-Funding-Source.xlsx`
* `2011-Tax-Rates.xlsx`, `2016-Tax-Rates.xlsx`
* `Development-Charge-Rates-as-of-Nov-2018.xlsx`
* GeoJSON files for various municipal layers (Bicycle_Routes,
  Business_Parks, City_Owned_Facilities, Heritage_Conservation_Districts)

**What an adapter would need to do:**

1. Pick one of the budget Excel files (Operating Budget is most CoDa-natural).
2. Aggregate budget line items into department-level proportions —
   D = number of departments (typical municipal: 8–12).
3. Cross-section: one record per fiscal-year file. For multi-year T,
   reconstruct a budget trajectory from 2011 / 2016 / 2018 + any other
   available years.
4. Carrier convention: Department names from the workbook's
   "Department" column.

**Estimated effort:** 2–3 hours including manual checking of which
budget rows are line-items vs subtotals (Excel files often mix both).

**Cross-reference:** The original Hs-18 (`experiments/Hs-18_*`) ran
this; the existing pipeline_output JSON could be re-ingested if a
quick parity-check is needed without rebuilding the adapter.

---

## 2 — `DATA/IIASA Data/`

**Status:** PENDING. Adapter not built.

**Source format:** Three NGFS Phase-4 scenario zip files
(V4.0 / V4.1 / V4.2) plus a series of Antarctic climate-model NetCDF
files (HIRHAM5 / CESM2 / EC-Earth3 / UKESM, historical and SSP
scenarios).

**What an adapter would need to do:**

For NGFS scenarios:

1. Extract the scenario CSVs from one of the Phase-4 zips.
2. Filter to compositional indicators — most natural: emissions
   composition by sector, or final energy by carrier.
3. For each scenario × year, build a D-carrier composition.
4. Cross-section: scenarios as records, or temporal: one scenario,
   years as records.

For Antarctic NetCDF:

1. Use `xarray` or `netCDF4` to extract gridded climate data.
2. Aggregate to climate-zone composition (e.g. fraction of grid cells
   in each temperature bracket).
3. T = years 1971–2014 (historical) or 2015–2100 (SSP585).

**Estimated effort:** 4–6 hours. Both NGFS and NetCDF need
domain-specific logic. NGFS is simpler if pre-extracted CSVs exist.

**Cross-reference:** Earlier HUF work in `HUF/codawork-2026/extended/`
references NGFS — `HUF_NGFS_Phase4_Analysis.xlsx` exists at the
repository root (1.3 MB) and may already contain the relevant
extracted data.

---

## 3 — `DATA/esa-planck/`

**Status:** PENDING. Adapter not built.

**Source format:** FITS sky-map files

* `HFI_SkyMap_353_2048_R3.01_full.fits`
* `HFI_SkyMap_353_2048_R3.01_full-evenring.fits`
* `HFI_SkyMap_353_2048_R3.01_full-oddring.fits`
* `PSO_Posh_Cat_R0.14.fits` (Planck Source Catalog)
* COBE_DMR_4YR / DIRBE / esa subdirectories

**What an adapter would need to do:**

1. Use `astropy.io.fits` and `healpy` to read the HEALPix sky maps.
2. Decide an angular partition — the natural CoDa setup is to bin the
   sky into N angular zones (e.g. by galactic latitude bands) and
   measure CMB intensity composition per zone.
3. Or: use the published 5-component cosmic energy budget (CMB / Dark
   Energy / Dark Matter / Baryons / Neutrinos) — already done as Hs-25
   `cosmic_cnt_Hs25.json` in the existing repo.

**Estimated effort:** 6–8 hours. FITS / HEALPix is a specialist
toolchain. The Hs-25 cosmic-budget result already exists; a fresh
v2.0.x run on a 5-carrier cosmic composition is straightforward if the
input CSV is reconstructed from `cosmic_cnt_Hs25.json`.

**Cross-reference:** Existing `HCI/cosmic_cnt_Hs25.json` and
`cosmic_depth_Hs25.json` were the canonical Hs-25 outputs (older
engine). For CoDaWork, an equivalent v2.0.3 run is feasible without
re-reading FITS — just rebuild the 5-carrier cosmic composition CSV
manually from the published Planck 2018 values:

```
Dark Energy  : 0.6847
Cold DM      : 0.2589
Baryons      : 0.0486
Photons      : 5.4e-5
Neutrinos    : 3.6e-5
```

This is a single record (T = 1) — too small for the depth tower. To
make it interesting we'd need a temporal sweep (cosmic composition
through cosmic history), which requires a model not raw data.

---

## 4 — `DATA/financial data/`

**Status:** PENDING. Adapter not built.

**Source format:**

* `Portfolio.csv` — 27 stocks with Ticker, Quantity, Sector, Close,
  Weight (single snapshot, T = 1)
* `SP500.csv`, `NASDAQ.csv`, `Dow_Jones.csv` — daily closing prices,
  multi-year trajectories
* `all_stocks_5yr.csv` — multi-stock daily price history
* `Portfolio_prices.csv`, `stock_prices_daily.csv` — aux data

**What an adapter would need to do:**

For a sector-allocation trajectory:

1. Use `Portfolio.csv` to map each ticker to a sector.
2. Use `all_stocks_5yr.csv` for daily closes per ticker.
3. For each day, compute portfolio value per sector (price × quantity)
   and close to simplex.
4. Output: T = number of trading days, D = number of distinct sectors
   in the portfolio (~10–15).

**Estimated effort:** 3–4 hours including checking ticker availability
in the daily-close file.

**Alternative simpler version:** Just use `Portfolio.csv` as a
single-snapshot D-sector composition (T = 1). Too small for the depth
tower but exercises the engine on a small composition.

---

## 5 — `DATA/chemistry/chemixhub/`

**Status:** PENDING. Adapter not built.

**Source format:** Full ChemixHub repository — config / datasets /
media / scripts / src / setup.py / README.md.

**What an adapter would need to do:**

Substantial. ChemixHub is a research codebase with its own data-loading
infrastructure. The adapter would need to either (a) call ChemixHub's
own loaders to extract compositional samples, or (b) re-implement the
relevant subset.

The earlier project document `CHEM_EITT_RESEARCH_PLAN.md` outlines the
intended approach. The work was originally planned to validate EITT on
500 K data points across 7 chemistry datasets — see
`HUF_FAST_REFRESH.json eitt_proofs.proof_4_chemistry`.

**Estimated effort:** 1–2 days. Treating this as a separate
experiment track rather than a single adapter.

**Cross-reference:** `chem_eitt_pipeline.py` at the repo root (4 KB)
is an early pipeline-builder. The `EITT_Chemistry_Findings.docx` at
top level is the published narrative. A fresh v2.0.x run would extract
the canonical chemistry compositions from one of the ChemixHub
datasets and treat each as a separate experiment id.

---

## 6 — `DATA/ATOMIC/` — NOT APPLICABLE

Contains Duflo-Zuker programs (Fortran/Python source code), not
compositional data per se. The AME2020 nuclear data referenced by
this folder is already covered by the `nuclear_semf` experiment in
`reference/`. No adapter work needed.

---

## 7 — `DATA/Acoustics/` — NOT APPLICABLE

Contains only `EXP04_acoustics_bessel_results.json` — a result file
from a previous Hs-04 Bessel-acoustics experiment. No raw
compositional data to ingest. The result is preserved as historical
record.

---

## How to add an adapter when the time comes

The pattern is documented in `experiments_v2/run_experiments.py`. Two
options:

### Inline build function

For small datasets that can be reconstructed deterministically from a
single source file:

```python
def build_<dataset_id>(out_path: Path):
    """Build pipeline-ready CSV for <dataset_id>."""
    # ... read source, compute carriers, write CSV ...

BUILDERS = {
    ...
    "build_<dataset_id>": build_<dataset_id>,
}
```

Then register in REGISTRY:

```python
{
    "id":          "<dataset_id>",
    "subdir":      "domain",   # or codawork2026 or reference
    "source_csv":  None,
    "is_temporal": True_or_False,
    "ordering":    "by-time" or "by-label",
    "description": "...",
    "build_fn":    "build_<dataset_id>",
}
```

### Standalone adapter script

For larger / multi-step adapters (e.g. BackBlaze, FAO):

1. Create `adapters/<source>_adapter.py` modelled on
   `backblaze_adapter.py` or `fao_irrigation_adapter.py`.
2. Register the produced CSV as a static `source_csv` in REGISTRY:

```python
{
    "id":          "<dataset_id>",
    "subdir":      "...",
    "source_csv":  str(HERE / "subdir/<dataset_id>/<dataset_id>_input.csv"),
    "is_temporal": True_or_False,
    "ordering":    "...",
    "description": "...",
}
```

3. Document the adapter in this file with: source, transformation,
   estimated effort, cross-reference to any prior work.

---

*The instrument reads. The expert decides. The loop stays open.*
