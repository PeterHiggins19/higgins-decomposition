# Tools

Top-level driver scripts for the CNT subsystem.

| Script | Purpose |
|---|---|
| [`run_pipeline.py`](run_pipeline.py) | Module-only driver — dispatch the post-CNT module pipeline for a named project from `master_control.json` (without re-running the engine) |
| [`verify_package.py`](verify_package.py) | Package-readiness verifier — scans the repo for every expected artefact and reports `PACKAGE READY` or lists missing items |

## Usage

```bash
# List registered modules and projects
python tools/run_pipeline.py --list-modules
python tools/run_pipeline.py --list-projects

# Run the module pipeline for one project
python tools/run_pipeline.py codawork2026_ember

# Run all projects
python tools/run_pipeline.py --all

# Verify package readiness
python tools/verify_package.py
```

`verify_package.py` is part of the standard push pre-flight check; see
[`../../ai-refresh/PREPARE_FOR_REPO.json`](../../ai-refresh/PREPARE_FOR_REPO.json).

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
