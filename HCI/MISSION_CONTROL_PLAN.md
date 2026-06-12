# Mission Control — Scientific Platform Architecture (Plan)

**Date:** 2026-05-05
**Status:** Plan only. Document this design before any code is built.
**Authors:** Peter Higgins / Claude
**Audience:** Future implementers (including future Peters and future Claudes,
or anyone else who picks the tool up after both leave the room).

---

## 1 — Vision

Hˢ / HCI / CNT becomes a self-sufficient scientific instrument. The user
loads data, edits one master control JSON, runs the tool, and receives a
fully-provenanced result folder. Every choice belongs to the user. Every
output is deterministic given fixed input and fixed control JSON. Every
omission is alerted, never silent.

The tool stands on its own:

* **No expert dependence.** A user reading the inline documentation can
  run the tool without contacting the authors.
* **No hidden state.** Every parameter that affects the result is in the
  control JSON, echoed in every output, hashed for verification.
* **No silent loss.** If any input data is not represented in any output,
  the tool stops and tells the user before producing anything.
* **No randomness.** Two runs with identical input and identical control
  JSON produce identical content_sha256. Always. Verified at every step.
* **No version drift.** The output folder records which engine versions
  ran, which schemas they conformed to, and which control JSON they read.

This is the user's contract:

> "If you give me this data and this control JSON, I will give you
>  exactly this output, every time, with full provenance.
>  If I cannot do that, I will tell you why and refuse to continue.
>  You control every choice. I will tell you the consequences."

---

## 2 — The Master Control JSON (Mission Command)

A single JSON file. The user reads it, edits it, runs the tool. The
tool reads it, programs every internal JSON config, executes the
declared pipeline, writes results. Every result folder contains a copy
of the control JSON that produced it.

### 2.1 — Skeletal structure

```json
{
  "_meta": {
    "type":            "MISSION_COMMAND",
    "schema_version":  "1.0.0",
    "user":            "name or hash",
    "created":         "ISO-8601 UTC",
    "label":           "Free-form mission name",
    "comment":         "Free-form mission notes"
  },

  "input": {
    "datasets": [
      {
        "id":               "ember_jpn",
        "source_path":      "...",
        "is_temporal":      true,
        "ordering_method":  "by-time",
        "carriers":         null            // null = read from CSV header
      }
    ],
    "halt_on_missing_dataset": true,
    "halt_on_data_loss":      true          // if any input cell is dropped
  },

  "output": {
    "root":               "...",
    "subfolder_per_dataset": true,
    "include_pdf":        true,
    "include_html":       true,
    "include_csv_summary":true,
    "verbose_provenance": true,
    "compression":        "none",           // none | gzip | brotli
    "track_every_byte":   true              // emit COVERAGE_AUDIT.json
  },

  "pipeline": {
    "tools_enabled": {
      "cnt_engine":          true,
      "stage1_plates":       true,
      "manifold_projector":  true,
      "spectrum_analyzer":   false,
      "depth_pdf":           true,
      "compositional_cinema":false
    },
    "tool_order": [                          // explicit dependency order
      "cnt_engine",
      "stage1_plates",
      "manifold_projector",
      "depth_pdf"
    ],
    "halt_on_tool_failure": true
  },

  "engine_config": {
    "cnt": {                                 // -> cnt.py / cnt.R USER CONFIG
      "DEFAULT_DELTA":         1e-15,
      "DEGEN_THRESHOLD":       1e-4,
      "LOCK_CLR_THRESHOLD":    -10.0,
      "DEPTH_MAX_LEVELS":      50,
      "DEPTH_PRECISION_TARGET":0.01,
      "NOISE_FLOOR_OMEGA_VAR": 1e-6,
      "TRIADIC_T_LIMIT":       500,
      "TRIADIC_K_DEFAULT":     500,
      "EITT_GATE_PCT":         5.0,
      "EITT_M_SWEEP_BASE":     [2,4,8,16,32,64,128]
    },

    "stage1_plates": {                       // -> plate generator config
      "max_plates":         101,
      "compression_method": "eitt_block_decimation",
      "block_extrema_sidebar": true,
      "lock_event_passthrough":true,
      "scale_provenance_chain":true,
      "course_plot_full_N":  true,
      "raise_eitt_gate_pct": 5.0
    },

    "depth_pdf": {
      "include_attractor_plot":   true,
      "include_helmsman_lineage": true,
      "include_lyapunov_table":   true
    },

    "spectrum_analyzer": {
      "fft_window": "hann",
      "n_fft":      256
    }

    // ... per-tool config blocks ...
  },

  "determinism": {
    "verify_content_sha256":     true,
    "verify_two_pass":           true,       // run engine twice; assert equality
    "fail_on_nondeterminism":    true
  },

  "integrity": {
    "input_sha256_expected":     null,       // if set, must match
    "control_sha256_will_be":    "computed_on_save"
  }
}
```

### 2.2 — Deterministic save procedure

When the user saves the control JSON or the tool reads it:

1. The tool computes a **canonical hash** of the JSON (sorted keys, no
   whitespace, no comments) — this becomes the `mission_id`.
2. The output folder is created with the mission_id in its path or in a
   sidecar file.
3. The control JSON is copied verbatim into the output folder as
   `CONTROL.json`. Any subsequent run that produces the same mission_id
   on the same input reproduces the same output.

### 2.3 — Engine programming

Every tool reads the control JSON's `engine_config.<tool_name>` block as
its USER CONFIG. The tool's own internal USER CONFIG block defines the
defaults; the control JSON overrides per-mission.

For `cnt.py`:

```bash
python3 cnt.py input.csv -o output.json --mission CONTROL.json
```

The engine reads `CONTROL.json` → `engine_config.cnt` → applies values to
its USER CONFIG variables before running. The active values are still
echoed in `metadata.engine_config` as today, but now also flagged with
`source: "mission_control"` so the JSON is forensic-complete.

If the user invokes `cnt.py` without `--mission`, the engine falls back
to its inline USER CONFIG defaults (current behaviour). Mission control
is opt-in but encouraged.

---

## 3 — Output folder structure

When the user picks an input data folder, the tool creates a sub-folder
named after the mission. Convention:

```
<user-data-root>/
├── input_data.csv                         # what the user gave
└── results_<mission_id_short>/            # what the tool produced
    ├── CONTROL.json                       # exact mission JSON used
    ├── CONTROL_sha256.txt
    ├── EXECUTION_LOG.json                 # tool order, wall_clock, status
    ├── COVERAGE_AUDIT.json                # input bytes -> output coverage
    ├── INTEGRITY_REPORT.md                # human-readable audit
    │
    ├── 01_cnt_engine/
    │   ├── <dataset>_cnt.json             # canonical CNT JSON
    │   ├── <dataset>_cnt.json.sha256
    │   └── stderr.log
    │
    ├── 02_stage1_plates/
    │   ├── <dataset>_plates.pdf
    │   ├── <dataset>_plates_metadata.json
    │   └── stderr.log
    │
    ├── 03_manifold_projector/
    │   └── <dataset>_projector.html
    │
    ├── 04_depth_pdf/
    │   └── <dataset>_depth.pdf
    │
    └── REPORT.md                          # auto-generated summary
```

Numbering preserves execution order, making forensic re-traversal trivial.

---

## 4 — Determinism + data-coverage enforcement

Every tool must satisfy:

1. **Deterministic given fixed input + fixed config.** Verified by
   running twice and comparing content_sha256. The tool refuses to
   accept its output unless this is true.
2. **Hashes inputs.** Source SHA-256 stored in metadata.
3. **Hashes outputs.** Result SHA-256 stored in `EXECUTION_LOG.json`.
4. **Reports coverage.** For every record/cell/byte in the input, the
   tool must report whether it was used, dropped, or smoothed. This
   becomes the `COVERAGE_AUDIT.json` block:

```json
{
  "_meta": {
    "type": "COVERAGE_AUDIT",
    "tool": "cnt_engine",
    "input_file": "ember_JPN_2025.csv",
    "input_sha256": "..."
  },
  "input_records":      26,
  "processed_records":  26,
  "represented_records":26,
  "dropped":            [],
  "zero_replaced": [
    {"record_index": 14, "carrier": "Nuclear", "original": 0.0, "replaced_with": 1e-15}
  ],
  "smoothed_in_blocks": [],
  "verified": true,
  "halt_on_data_loss":  true,
  "data_loss_detected": false
}
```

If `data_loss_detected` is true and `halt_on_data_loss` is true in the
control JSON, the tool refuses to write the result and emits a
diagnostic. The user fixes the data or relaxes the policy.

This is the **enforcement** of "if any data is not represented it is
alerted to the user by design."

---

## 5 — Tool catalog (current and planned)

| # | Tool                  | Status     | Purpose                                              | Reads             | Writes                         |
|---|-----------------------|------------|------------------------------------------------------|-------------------|--------------------------------|
| 1 | `cnt.py` / `cnt.R`    | DONE 2.0.2 | Canonical CNT JSON generator                         | CSV               | `<id>_cnt.json`                |
| 2 | `mission_runner.py`   | PLANNED    | Reads CONTROL.json, dispatches tools, writes folder  | CONTROL.json      | full results folder            |
| 3 | `stage1_plates`       | PLANNED    | CBS 2x3 plate cine-deck (HUF morphographic)         | CNT JSON          | `_plates.pdf`                  |
| 4 | `manifold_projector`  | DEFERRED   | Interactive 3D radar-tube projector                  | CNT JSON          | `_projector.html`              |
| 5 | `depth_pdf`           | DEFERRED   | Recursive depth + impulse-response PDF report        | CNT JSON          | `_depth.pdf`                   |
| 6 | `spectrum_analyzer`   | DEFERRED   | FFT/cepstrum/STFT 14-page PDF                        | CNT JSON          | `_spectrum.pdf`                |
| 7 | `compositional_cinema`| DEFERRED   | Polar-slice movie PPTX                               | CNT JSON          | `_cinema.pptx`                 |
| 8 | `coverage_auditor`    | PLANNED    | Cross-checks all tools' COVERAGE_AUDIT outputs       | all `_audit.json` | `COVERAGE_REPORT.md`           |
| 9 | `web_controller`      | DEFERRED   | HTML browser GUI for editing CONTROL.json            | (interactive)     | CONTROL.json + run             |

The numbering is the build order. Each tool can be developed
independently provided it conforms to the CNT JSON schema for input
and produces a COVERAGE_AUDIT.json for its own output.

---

## 6 — The HTML data-flow controller (deferred)

Browser-based interface. Generates the CONTROL.json behind the scenes;
the user never has to edit JSON by hand unless they want to.

**Layout (rough):**

```
┌──────────────────────────────────────────────────────────────────────┐
│  HCI Data Flow Controller                              [Run] [Save]  │
├──────────────┬─────────────────────────────────────┬─────────────────┤
│              │                                     │                 │
│  DATASETS    │      PIPELINE GRAPH                 │   PARAMETERS    │
│              │                                     │                 │
│  + Add file  │   ┌──────┐  ┌──────────┐  ┌──────┐  │   <selected     │
│  + Add folder│   │  in  │->│ cnt.py   │->│ JSON │  │    tool         │
│              │   └──────┘  └──────────┘  └──────┘  │    config       │
│  ☑ ember_jpn │                  ↓                  │    visible      │
│  ☑ ball_reg  │              ┌────────────┐         │    here>        │
│  ☐ planck    │              │ stage1_pl  │         │                 │
│  ...         │              └────────────┘         │   max_plates    │
│              │                  ↓                  │   = [101]       │
│              │              ┌────────────┐         │   compression   │
│  OUTPUT      │              │  pdf       │         │   = [eitt v]    │
│  Root: <...> │              └────────────┘         │   ...           │
│              │                                     │                 │
├──────────────┴─────────────────────────────────────┴─────────────────┤
│ ▷ Console / Coverage / Errors                                         │
└──────────────────────────────────────────────────────────────────────┘
```

When the user clicks Run, the controller:

1. Validates the pipeline graph (no cycles, all dependencies satisfied).
2. Generates CONTROL.json from the GUI state.
3. Hands CONTROL.json to `mission_runner.py`.
4. Streams progress back to the console pane.
5. On completion, opens the result folder with REPORT.md displayed.

The HTML page is an **expression** of the CONTROL.json schema; the GUI
and the JSON are interchangeable. Power users edit the JSON. Casual
users edit the GUI. Both produce the same artefacts.

---

## 7 — Self-sufficiency requirements

For the tool to stand alone:

### 7.1 — Documentation

* Every JSON schema (CONTROL, CNT, COVERAGE_AUDIT, EXECUTION_LOG) is
  documented as a Markdown file in the repository.
* Every tool has an inline USER CONFIG block with field-by-field comments.
* Every error message includes:
  - what went wrong
  - which input or config caused it
  - what the user can change to fix it
* Every output JSON is self-documenting (engine_config + content_sha256
  + mathematical_lineage in metadata).

### 7.2 — Defaults

* Every parameter has a published default.
* Defaults are conservative — produce honest, slow, complete output.
* Tightening or loosening defaults is the user's choice with documented
  consequences.

### 7.3 — Failure modes

* The tool refuses to produce output it cannot verify.
* DEGENERATE / WARNING / ERROR are distinct levels with clear meanings.
* Every refusal points the user to the documentation that explains it.

### 7.4 — No outside dependencies

* `cnt.py` / `cnt.R` are pure standard-library + numpy / jsonlite-digest.
  No internet calls, no proprietary services, no API keys.
* Future tools follow the same rule: any dependency must be FOSS,
  inline-documented, and offline-runnable.

### 7.5 — Reproducibility

* Two runs of the same CONTROL.json on the same input produce identical
  content_sha256 across all output JSONs.
* If determinism fails, the tool stops and reports.
* This is the platform's most important property and must never regress.

---

## 8 — Build order

Strict dependency chain:

1. **`cnt.py` / `cnt.R`** — DONE. Schema 2.0.0, engine 2.0.2.
2. **`mission_runner.py`** — read CONTROL.json, dispatch tools, write
   folder. Sketch pseudocode in MISSION_RUNNER_SPEC.md before implementation.
3. **`stage1_plates`** — uses CNT JSON only. First downstream tool.
4. **`coverage_auditor`** — cross-checks all tools' audits. Built once
   we have ≥ 2 tools.
5. **`manifold_projector`** / **`depth_pdf`** / **`spectrum_analyzer`**
   — independent downstream tools, any order.
6. **`web_controller`** — built last, when the JSON-driven CLI is solid.

Each tool's spec document precedes its implementation by at least one
session. No tool ships without:
- A spec (Markdown)
- An inline USER CONFIG block
- A COVERAGE_AUDIT contract
- A determinism test
- A migration entry in the relevant manifest

---

## 9 — Removing Peter and Claude

Operational test for self-sufficiency: a user (any user, anywhere) can
download the repo, read the documentation, edit a CONTROL.json, run the
tool, and produce a result folder that:

1. Reproduces the published canonical results on the same input.
2. Carries full provenance for every output byte.
3. Tells the user honestly what was computed and what was skipped.
4. Refuses to produce output it cannot verify.
5. Includes the user's edited CONTROL.json verbatim, hashed, in the
   result folder.

If the user has questions, the answer is in:

* The repository's `README.md`.
* `CONTROL_SCHEMA.md` (planned) — the master control JSON spec.
* `CNT_JSON_SCHEMA.md` — the canonical engine output spec.
* `MISSION_CONTROL_PLAN.md` — this document, the architectural overview.
* The inline USER CONFIG documentation in each tool.
* The auto-generated REPORT.md in the result folder.

The user does **not** need to email Peter, ping Claude, or contact any
expert. The tool is the documentation.

---

## 10 — What this plan does NOT promise

To be honest about the boundaries:

1. **It does not eliminate engineering judgement.** A user studying a
   D=2 dataset will still see DEGENERATE classifications because D=2
   genuinely lacks compositional structure for the curvature recursion.
   The tool reports this faithfully; the user must understand why.
2. **It does not solve domain interpretation.** The tool reads the
   simplex; the expert reads the domain. Hˢ produces structural
   diagnostics, not policy or causal claims.
3. **It does not guarantee fast.** Some configurations (full triadic
   enumeration at T = 5000, or every tool enabled at maximum verbosity)
   will produce terabytes and take hours. The tool tells the user the
   estimated wall clock before it commits to running. The user decides.
4. **It does not solve adapter-writing.** New data formats need new
   adapters. The platform provides the adapter pattern; the user (or
   contributor) writes the format-specific reader.
5. **It does not replace the schema-version contract.** Major schema
   bumps (e.g. 2.x → 3.x) still require viewer updates. Mission Command
   schema versioning (currently 1.0.0) is independent of CNT JSON
   schema versioning (currently 2.0.0).

These are the honest limits. The tool is open, deterministic, and
user-controlled within these limits.

---

## 11 — Action items (post-CoDaWork)

This plan is a target, not a build sheet. Concrete steps when work
resumes:

1. Write `CONTROL_SCHEMA.md` — the formal Mission Command JSON schema
   (mirrors §2 above with full type tables, like CNT_JSON_SCHEMA.md).
2. Modify `cnt.py` to accept `--mission CONTROL.json` and read its
   engine_config.cnt block. Backward-compatible.
3. Write `mission_runner.py` minimal version: reads CONTROL, runs
   cnt.py only, writes results folder + EXECUTION_LOG.json +
   COVERAGE_AUDIT.json.
4. Add a `STAGE1_PLATES_SPEC.md` (the existing `STAGE1_PLATE_CAP_SPEC.md`
   is a precursor) and build `stage1_plates.py` to read CNT JSON +
   CONTROL.engine_config.stage1_plates.
5. After 2 tools exist, build `coverage_auditor`.
6. Iterate on remaining tools as needed.
7. Browser GUI when CLI flow is stable across ≥ 4 tools.

---

## 12 — Why this matters

The current state of the project — Peter, Claude, and a corpus of work
spread across many sessions — is fragile. Knowledge lives in
conversation context that vanishes. Decisions get re-litigated.
Tools accumulate idiosyncratic behaviour that nobody outside the
collaboration can reproduce.

The Mission Command architecture is the antidote: every choice the user
makes is captured in a JSON file, every output ties back to a specific
CONTROL.json, every parameter is documented inline, and every result
folder is forensic-complete. The tool no longer needs Peter to remember
why something was done. It records why, in writing, on the same
filesystem as the data.

That is what makes it a scientific platform rather than a research
collaboration. The instrument reads. The expert decides. The loop stays
open. *And the next user has no need to ask anyone what any of that
means.*

---

*This document is the plan. The build follows.*

*The instrument reads. The expert decides. The loop stays open.*
