# Hˢ Experiment Folder Standard

*Version 1.0 — 2026-04-30*
*Author: Peter Higgins / Rogue Wave Audio*

This document defines the required structure, naming convention, and machine-readable index schema for all Hˢ calibration and validation experiment folders. Every experiment folder in this repository conforms to this standard.

## Folder Naming

```
Hs-{NN}_{Short_Name}/
```

Where `{NN}` is the experiment number (zero-padded to 2 digits for 01–25, or prefixed M for M-series manifold experiments). `{Short_Name}` uses Title_Case with underscores separating words.

Examples: `Hs-01_Gold_Silver/`, `Hs-M02_EMBER_Energy/`, `Hs-23_Radionuclides/`

## Required Contents

Every experiment folder contains at minimum:

| File | Purpose |
|------|---------|
| `Hs_INDEX.json` | Machine-readable experiment manifest (schema below) |
| `JOURNAL.md` | Science-grade experiment journal with methodology, results, and conclusions |
| `pipeline_output/` | Directory containing all pipeline run outputs |

The `pipeline_output/` directory contains the standard output set from `hs_run.py`:

| File Pattern | Description |
|--------------|-------------|
| `{PREFIX}_results.json` | Full pipeline results JSON (all 12+ steps, extended diagnostics) |
| `{PREFIX}_report_en.txt` | Diagnostic report in English |
| `{PREFIX}_helix_exploded.pdf` | Exploded helix diagram (1 page) |
| `{PREFIX}_manifold_helix.pdf` | Manifold helix projection (1 page) |
| `{PREFIX}_projections.pdf` | Six-view projection suite (1 page) |
| `{PREFIX}_polar_stack.pdf` | Per-interval polar stack with ghost composite (variable pages) |
| `{PREFIX}_polar_stack.json` | Polar stack CLR values in machine-readable JSON |
| `{PREFIX}_manifold_paper.pdf` | 3D manifold-on-paper projection (3 pages) |

Multi-run experiments (e.g., Hs-M02 with 7 countries, Hs-23 with 2 isotope chains) have one output set per run, each with a distinct `{PREFIX}`.

## Hs_INDEX.json Schema

The index file is the machine-readable identity of each experiment. It connects the raw data source, the pipeline configuration, and every output artifact into a single auditable record.

```json
{
  "$schema": "Hs_INDEX/1.0",
  "experiment_id": "Hs-01",
  "name": "Gold/Silver Price Ratio",
  "domain": "COMMODITIES",
  "series": "Core (Hs-01 through Hs-25)",
  "date_created": "2026-04-30",
  "author": "Peter Higgins",
  "affiliation": "Independent Researcher, Markham, Ontario, Canada",
  "purpose": "Validate Hˢ decomposition on a 2-part time-varying simplex from commodity price ratios.",

  "data_source": {
    "origin": "MeasuringWorth.com",
    "origin_url": "https://www.measuringworth.com/datasets/gold/",
    "raw_data_path": "D:\\HUF_Research\\Claude CoWorker\\DATA\\Commodities\\",
    "repo_copy": "data/Commodities/gold_silver_simplex.csv",
    "description": "Monthly gold/silver price ratios converted to 2-part simplex (gold_frac, silver_frac).",
    "license": "Public domain / academic use",
    "data_hash_sha256_16": "631e1793a086b598"
  },

  "system": {
    "N": 624,
    "D": 2,
    "carriers": ["Gold", "Silver"],
    "time_axis": "Monthly (1687–2024)",
    "zero_replacement": false,
    "epsilon": 1e-10
  },

  "pipeline": {
    "version": "1.0 Extended",
    "runner": "hs_run.py",
    "instrument": "Hˢ Higgins Decomposition — 12-Step Pipeline v1.0 Extended",
    "deterministic": true,
    "run_timestamp": "2026-04-30T00:00:00Z",
    "run_command": "python hs_run.py ../../data/Commodities/gold_silver_simplex.csv --exp-id Hs-01 --name \"Gold/Silver Price Ratio\" --domain COMMODITIES"
  },

  "results_summary": {
    "total_variance": 0.2958,
    "variance_shape": "bowl",
    "variance_R2": 0.9071,
    "aitchison_path_length": null,
    "aitchison_net_distance": null,
    "path_efficiency": null,
    "entropy_mean": 0.1846,
    "entropy_cv": 58.19,
    "closure_verified": true,
    "clr_sum_verified": true,
    "diagnostic_code_count": 0,
    "error_count": 0,
    "warning_count": 0,
    "discovery_count": 0,
    "structural_mode_count": 0
  },

  "classification": {
    "structural_modes": [],
    "diagnostic_codes_summary": "No anomalies detected. Clean 2-part simplex.",
    "claim_tier": "Validated — deterministic pipeline produces consistent results on repeated runs."
  },

  "outputs": {
    "results_json": "pipeline_output/Hs-01_results.json",
    "report_en": "pipeline_output/Hs-01_report_en.txt",
    "helix_exploded": "pipeline_output/Hs-01_helix_exploded.pdf",
    "manifold_helix": "pipeline_output/Hs-01_manifold_helix.pdf",
    "projections": "pipeline_output/Hs-01_projections.pdf",
    "polar_stack": "pipeline_output/Hs-01_polar_stack.pdf",
    "polar_stack_json": "pipeline_output/Hs-01_polar_stack.json",
    "manifold_paper": "pipeline_output/Hs-01_manifold_paper.pdf"
  },

  "governance": {
    "journal": "JOURNAL.md",
    "admin_ref": "ai-refresh/HS_ADMIN.json",
    "executive_summary_ref": "EXECUTIVE_SUMMARY.md",
    "pipeline_readme": "tools/pipeline/README.md"
  },

  "repeatability": {
    "deterministic": true,
    "note": "Pipeline is fully deterministic. No stochastic elements. Bit-identical output on repeated runs with identical input and pipeline version."
  }
}
```

## Field Definitions

**Top level:**

`$schema` — always `"Hs_INDEX/1.0"`. Enables machine validation.

`experiment_id` — canonical ID matching folder name prefix (e.g., `"Hs-01"`, `"Hs-M02"`).

`name` — descriptive experiment name.

`domain` — uppercase domain tag: `COMMODITIES`, `NUCLEAR`, `GEOCHEMISTRY`, `ENERGY`, `ASTROPHYSICS`, `STORAGE`, `COMMUNICATION`, `COSMOLOGY`, `CALIBRATION`.

`series` — experiment series classification: `"Core (Hs-01 through Hs-25)"` or `"M-series (Manifold Projection Systems)"`.

`purpose` — one sentence describing what this experiment validates.

**data_source block:**

`origin` — name of the original data provider or publication.

`origin_url` — URL where the original data can be obtained.

`raw_data_path` — path to the raw data in the primary data library (D:\HUF_Research\Claude CoWorker\DATA\).

`repo_copy` — relative path from the Hs root to the pipeline-ready CSV in the repo data/ folder.

`data_hash_sha256_16` — first 16 hex characters of the SHA-256 hash of the input CSV, as computed by the pipeline. This is the data integrity seal.

**system block:**

`N` — number of observations (rows).

`D` — number of compositional parts (carriers).

`carriers` — ordered list of carrier names.

`time_axis` — description of the time or index dimension.

`zero_replacement` — whether structural zeros were replaced with epsilon.

**pipeline block:**

`version` — pipeline version string.

`runner` — the script used to execute the run.

`deterministic` — always `true` for Hˢ pipeline.

`run_timestamp` — ISO 8601 timestamp of the run.

`run_command` — exact command line to reproduce the run.

**results_summary block:**

Captures the key numerical diagnostics without duplicating the full results JSON. All values are drawn from the pipeline results JSON.

**classification block:**

`structural_modes` — list of structural mode codes detected (e.g., `["SM-RTR-DIS", "SM-DMR-DIS"]`).

`diagnostic_codes_summary` — one-sentence summary of the diagnostic outcome.

`claim_tier` — scientific claim classification per the Hˢ claim framework.

**outputs block:**

Relative paths from the experiment folder to every output artifact. All paths are verifiable — if a file is listed, it exists.

**governance block:**

Relative paths from the Hs root to governing documents that reference this experiment.

**repeatability block:**

Statement of determinism. The pipeline has no stochastic elements.

## Multi-Run Experiments

For experiments with multiple independent runs (e.g., Hs-M02 with 7 EMBER countries), the `Hs_INDEX.json` contains a `runs` array instead of a single `results_summary` and `outputs`:

```json
{
  "runs": [
    {
      "run_id": "CHN",
      "name": "China",
      "N": 26,
      "D": 8,
      "carriers": ["Bioenergy", "Coal", "Gas", "Hydro", "Nuclear", "Other Fossil", "Solar", "Wind"],
      "data_source_csv": "data/Energy/EMBER_pipeline_ready/ember_CHN_China_generation_TWh.csv",
      "data_hash_sha256_16": "abc123...",
      "results_summary": { ... },
      "outputs": {
        "results_json": "pipeline_output/CHN_results.json",
        ...
      }
    },
    ...
  ]
}
```

## JOURNAL.md Template

Every experiment journal follows this structure:

```markdown
# Hs-{NN}: {Full Name}

*Author: Peter Higgins*
*Date: {YYYY-MM-DD}*
*Domain: {DOMAIN}*
*Series: {Series description}*

## 1. Purpose

{One paragraph: what is being tested and why.}

## 2. Data Source

{Dataset name, origin, URL, license. Description of the compositional system:
what the carriers represent, what the observations are, time range if applicable.}

## 3. System Parameters

| Parameter | Value |
|-----------|-------|
| N (observations) | {N} |
| D (carriers) | {D} |
| Carriers | {list} |
| Zero replacement | {yes/no} |
| Data hash (SHA-256/16) | {hash} |

## 4. Method

The full Hˢ pipeline (v1.0 Extended) was applied via `hs_run.py`. The pipeline
is deterministic — repeated runs on identical input produce bit-identical output.

{Any experiment-specific methodology notes.}

## 5. Results

### 5.1 Variance Structure

{Total variance, shape classification, R², interpretation.}

### 5.2 Diagnostic Summary

{Code counts: errors, warnings, discoveries, structural modes.
Key findings from the diagnostic report.}

### 5.3 Projection Analysis

{What the five mandatory projections reveal about this system.}

## 6. Conclusions

{What this experiment demonstrates about the Hˢ decomposition.
How results compare to domain knowledge.
Any limitations or caveats.}

## 7. Reproducibility

Run command:
\```bash
cd tools/pipeline
python hs_run.py {path_to_csv} --exp-id "{exp_id}" --name "{name}" --domain {DOMAIN}
\```

All outputs in `pipeline_output/`. Results JSON contains full numerical record.
```

## Validation

An experiment folder is complete when:

1. `Hs_INDEX.json` exists and validates against this schema
2. `JOURNAL.md` exists with all 7 sections populated
3. `pipeline_output/` contains the full standard output set (8 files per run)
4. All file paths in `Hs_INDEX.json` resolve to existing files
5. `data_hash_sha256_16` in the index matches the hash in the results JSON
6. `N`, `D`, and `carriers` in the index match the results JSON

---

Peter Higgins / Rogue Wave Audio — CC BY 4.0
