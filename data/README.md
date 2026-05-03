# Hs Data — Math Validation Datasets

These are **copies** of raw data used for mathematical validation of the Hˢ
pipeline. They exist here for reproducibility — so anyone cloning the
repository can run the pipeline from raw data without needing the original
data library.

**These are not general-purpose datasets.** They are the specific subsets
used in Hˢ experiments and CoDaWork 2026 demonstrations.

## Source of Truth

The original raw data resides in:

```
D:\HUF_Research\Claude CoWorker\DATA\
```

That library contains the complete, unmodified datasets from their original
sources (EMBER, World Bank, EarthChem, AME2020, Backblaze, ESA Planck, etc.).
The files here are pipeline-ready extracts — cleaned, formatted, and ready
for `hs_run.py` or `hs_ingest.py`.

## Contents

| Directory | Source | Experiments | Description |
|-----------|--------|-------------|-------------|
| Energy/EMBER_pipeline_ready/ | EMBER Climate 2025 | Hs-M02 | 7 countries, electricity generation by source (TWh), 2000-2025 |
| Commodities/ | MeasuringWorth.com | Hs-01 | Gold/silver price ratios, monthly |
| Nuclear/ | AME2020 + SEMF | Hs-03, Hs-11 | Nuclear binding energies, SEMF decomposition ratios |
| Geochemistry/ | EarthChem (Ball 2022) | Hs-05 | Major-element oxide compositions |

## Usage

```bash
# Run any CSV through the full pipeline
cd tools/pipeline
python hs_run.py ../../data/Energy/EMBER_pipeline_ready/ember_DEU_Germany_generation_TWh.csv \
  --exp-id "Hs-M02-DEU" --name "EMBER Germany" --domain "ENERGY"
```

## Data Provenance

All datasets are from publicly available scientific sources. Individual
experiment journals in `experiments/` document the full provenance chain
for each dataset.

---

Peter Higgins / Rogue Wave Audio — CC BY 4.0
