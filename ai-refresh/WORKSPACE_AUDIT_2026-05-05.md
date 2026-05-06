# Workspace Audit — 2026-05-05

A walk through every top-level tree under `D:\HUF_Research\Claude CoWorker`,
with status (current / dormant / archived) and any open work.

## Active trees (last touched May 2026)

### `HUF-CNT-System/`  ← **CANONICAL**
The HUF-CNT system at v1.0.0 + v1.1.x. This is the single source of
truth for the engine, atlas, mission command, conference demo, and
public-trial readiness. **No open issues** beyond the optional next-cycle
items (Stage 3 / Stage 4 plate modules).

### `Current-Repo/Hs/`  ← **CURRENT — Hs research canon**
The Hs (Higgins) research repo. Contains:
* `experiments/Hs-01..Hs-25` — 25 research experiments at v1 engine
  (separate from the HUF-CNT 25-experiment corpus).
* `HCI/cnt_v2/` — preserved older cnt_v2 layout (now superseded by
  HUF-CNT-System; kept for diff/audit).
* `papers/codawork2026/` — drafts.
* `ai-refresh/` — the manifests this audit is being written into.

**Open items:**
- Some Hs-experiment journals predate engine 2.0.4 and reference older
  schema. They're historically accurate (snapshots) but if regenerated
  via the new pipeline they would shift SHAs. Not blocking.

### `Current-Repo/Hs-Lab/`  ← **ACTIVE component prototyping**
12 component sub-folders (`amalgamation-tester`,
`archetype-classifier`, `causal-flow-detector`, `decomposer`,
`fingerprint-comparator`, `governor`, `matrix-diagnostics`,
`reader-adapter`, `report-generator`, `sensitivity-engine`,
`tensor-bridge`, `constant-library`). Last touched 2026-04-30.

**Status:** Component scaffolding; not yet integrated into the
HUF-CNT-System pipeline. Future-work track.

### `Current-Repo/HUF/`  ← **CURRENT — HUF research canon**
Discoveries, drafts, briefings, dormant explorations, and the full
codawork2026 preparation tree. Last touched 2026-04-28.

**Open items / dormant subtrees** (`Current-Repo/HUF/dormant/`):
* `deceptive-drift/`, `early-governance/`,
  `grok-tensor-exploration-apr14/`, `hagf/`,
  `medical-commercial-exploration/`, `peterson-outreach/`,
  `planck-case/`, `pre-coda-metrics/` — all explicitly dormant by name;
  no action required.

### `DATA/`  ← **READ-ONLY raw data sources**
Source data for adapters. The 5 deferred adapter sources point here.

### `Collective Documents/`, `CoDa-Responses/`  ← **REFERENCE**
Inbound documents from collaborators / responses to the CoDa community.
Read-only.

### `External_Published_Papers/`  ← **READ-ONLY reference**

## Dormant trees (last touched April 2026)

The following trees were active during the cnt_v2 / earlier-Hs build
phase but are **superseded by HUF-CNT-System**:

| Tree | Last touched | Status |
|---|---|---|
| `HUF-Project/`         | 2026-04-13 | Superseded — HUF-CNT-System is the new canonical project layout |
| `HUF-Decomposition-Dev/` | 2026-04-12 | Superseded — `HUF_DOC_MANIFEST.json` here predates the rebuild |
| `HUF-repo/`            | 2026-04-10 | Stub — only `drafts/` subfolder; superseded |
| `HUF-repo-pre-S016-2026-04-09-bak/` | 2026-04-09 | Explicit backup (S016 cut) |
| `Githubrepo/`          | 2026-04-16 | Pre-rebuild HUF mirror; superseded |
| `repo-staging/`, `repo-update/`, `rwa-update/` | 2026-04-15..16 | Earlier release-staging shells; superseded |
| `Chatgpt/`             | 2026-04-17 | ChatGPT artefacts (read-only history) |
| `EITT/`                | 2026-04-09 | EITT lab outputs (12K files); kept as historical record |
| `code/`                | 2026-04-09 | Single legacy file |
| `Hs/` (legacy)         | varies     | Pre-Current-Repo Hs work — keep for lineage |
| `HUF/` (legacy)        | 2026-04-10 | Pre-Current-Repo HUF — keep for lineage |
| `regimes/`             | 2026-01-09 | January 2026 regime data; closed |
| `Unity/`               | 2026-03-08 | Unity-related references; closed |
| `RogueWaveAudio/`      | 2026-03-20 | RogueWaveAudio side-project; closed |

**Recommendation:** these can be retained as-is (audit lineage) or
collapsed under a `_archive/` folder if the workspace needs trimming.
None contain unfinished v1.1.x work.

## Documents that may need a refresh

Search for "v1.0", "engine 2.0.0/.1/.2/.3", "schema 2.0.0" in
out-of-tree docs revealed nothing critical: every reference is either
historically correct (snapshots, journals) or already updated by this
session. The HUF-CNT-System CHANGELOG, README, V1.1_FEATURE_MENU,
PUBLIC_TRIAL_READINESS, and all admin JSONs have been refreshed.

A small docstring inside the Hs `EXECUTIVE_SUMMARY.md` references
"19/19 experiments" and "cnt_v2" — that summary is a historical
snapshot of the pre-rebuild phase. It's been preserved; the new
state is captured in `AI_REFRESH_2026-05-05_v1.1.x.md` and
`HS_ADMIN.json`.

## Unfinished projects / future tracks

| Track | Where | Notes |
|---|---|---|
| Stage 3 plate module (Order 3 — depth tower / IR / attractor) | `HUF-CNT-System/atlas/` (open) | Next-cycle |
| Stage 4 plate module (Order 4+ — EITT / inference) | `HUF-CNT-System/atlas/` (open) | Next-cycle |
| Hs-Lab components → HUF-CNT integration | `Current-Repo/Hs-Lab/components/` | Wide track |
| Raw-data swap-in for 5 extended adapters | `HUF-CNT-System/adapters/` | Replace `build_synthetic_*()` with real data loaders |
| ChemixHub native loader integration | per `DEFERRED_ADAPTERS.md §5` | Treated as separate experiment track |
| ESA Planck FITS / HEALPix path | per `DEFERRED_ADAPTERS.md §3` | Closed-form Friedmann path is shipping; FITS path is optional |
| Schema 2.1.0 → R port adoption | `HUF-CNT-System/cnt/cnt.R` | Python now writes `metadata.units`; R should mirror |

**Hs-Lab components** are scaffolds that were never closed. If you
want them adopted into the HUF-CNT-System pipeline, the natural
landing path is:
- `archetype-classifier`  → new module under `mission_command/modules.py`
- `causal-flow-detector`  → Stage 3+ plate
- `report-generator`      → ties into the conference demo's per-country index

## Summary

- 1 active canonical tree (`HUF-CNT-System/`) at full v1.1.x.
- 1 active research repo (`Current-Repo/Hs/`).
- 1 active component-prototyping repo (`Current-Repo/Hs-Lab/`).
- 1 active broader-research repo (`Current-Repo/HUF/`).
- ~15 dormant trees (April-2026 vintage), retained for lineage.

The workspace is consolidated. No critical refresh blocked.
