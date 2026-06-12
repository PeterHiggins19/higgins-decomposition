# Mission Command — orchestrator + module pipeline

The corpus orchestrator. Reads `INDEX.json`, locates each experiment's
input CSV, runs the engine in the correct order, and verifies (or
updates) the published `content_sha256`. Optionally dispatches the
post-CNT module pipeline (Stage 1, Stage 2, Stage 3, Stage 4, spectrum,
projector) per project.

## 🆕 Mission Command and CCTT — how they relate

Mission Command is the orchestrator for the **canonical 25-experiment
corpus**: it knows about every registered experiment by ID and runs them
through the engine + module pipeline with locked per-experiment ordering.

**CCTT v1.0** is the orchestrator for *any* compositional dataset —
including ones that aren't yet in the corpus. CCTT phase 5 (render
pipeline) calls into the same modules registered in
[`modules.py`](modules.py); the difference is that CCTT generates a
temporary project block on the fly (or invokes single modules directly)
rather than reading from `INDEX.json`. Both use the same engine, the same
modules, and the same hash-chain provenance.

If you are running a corpus experiment, use Mission Command directly. If
you are running a new analysis from raw data, use [`CCTT_RUNBOOK.md`](../../ai-refresh/CCTT_RUNBOOK.md);
it will call Mission Command for you when the dataset is ready to render.

| File | Purpose |
|---|---|
| [`mission_command.py`](mission_command.py) | Orchestrator; `--verify` (default) and `--update` modes; per-experiment + per-project dispatch |
| [`modules.py`](modules.py) | Post-CNT module registry (six modules: stage1, stage2, stage3, stage4, spectrum_paper, projector_html) |
| [`master_control.json`](master_control.json) | User-editable: per-experiment ordering overrides + per-project module selection + Stage 2 plate options |

## Usage

```bash
# Verify the full 25-experiment corpus (default)
python mission_command.py

# Run one experiment + all of its project's modules
python mission_command.py --project codawork2026_ember

# Verify by subdir
python mission_command.py --subset domain

# Update INDEX.json with new SHAs (release flow)
python mission_command.py --update
```

## master_control.json structure

Two top-level blocks:

* `experiments` — per-experiment ordering and engine_config_overrides
  (engine-side overrides; used by `cnt_run`).
* `projects` — per-project module bundles (post-CNT modules; used by
  `tools/run_pipeline.py` and `mission_command.py --project`).

Each project declares:

```json
{
  "experiments": ["ember_chn", "ember_jpn", ...],
  "modules":     ["stage1", "stage2", "stage3", "stage4",
                  "spectrum_paper", "projector_html"],
  "options": {
    "stage2": {
      "biplot_top_n": 6,
      "per_experiment": {
        "ember_jpn": { "ternary_triplets": [...] }
      }
    }
  }
}
```

For the canonical reference, see
[`../handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md`](../handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md)
Part B.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
