# `tools/` — current toolchain (CN‑TT v4 era)

*Reset 2026‑06‑11. The previous contents of this folder — a **piecemeal pipeline built to develop ideas** (the `hs_*` 12‑step pipeline, manifold/projector generators, old interactive demos, notebooks, the quarantined transcendental pre‑test) — predated the current engine and **do not represent the system going forward.** They are archived, intact and reversible, at `_archive_2026-06-11/Hs-tools-primitive-pipeline/` (mirror root, off‑repo). This folder now holds only **proper tools of the current system.** Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001.*

---

## The current system has one engine and one run path

Everything routes through **CN‑TT v4** (`HCI-CNTT/`), the tile‑native reference implementation of HUF‑STD‑002. There is no separate "pipeline" to maintain — the engine *is* the pipeline (Adapter → closure/CLR/Helmert‑ILR → D=4 quaternion charts → lossless atlas reconstruction → navigation/diagnostics → hash). Determinism is binding: same input → same output → same `cntt_content_sha256`.

## What's here

| Tool | What it does |
|---|---|
| [`cntt_report.py`](cntt_report.py) | **The current general‑purpose tool.** Runs any composition CSV through CN‑TT v4 and prints a human‑readable diagnostics + `SS‑CCC‑LLL` code report (or full JSON). Carrier‑guard (E‑21) aware. Composes the canonical runner + the code system; adds no new science. The modern single‑entry replacement for the archived `hs_run`/`hs_reporter`/`hs_codes`/`hs_audit` piecemeal scripts. |
| `AI_ASSIST.json` | Bring‑your‑own‑AI onboarding node for this folder. |

```
python tools/cntt_report.py  <composition.csv>                 # human report
python tools/cntt_report.py  <composition.csv> --json -o out.json
```

## The canonical tools that live elsewhere (by design)

The current reusable tools live next to what they serve, not in a catch‑all folder:

- **Run the engine:** `HCI-CNTT/run_cntt.py <csv> -o out.json` — the canonical runner.
- **Self‑test (BIST):** `HCI-CNTT/engine/self_test/run_self_test.py` — proves quaternion exactness, lossless tiling, and determinism from inside the engine (`VERDICT: PASS`).
- **Code system:** `HCI-CNTT/engine/codes.py` — the `SS‑CCC‑LLL` diagnostic/calibration codes (incl. the automated NULL flag and the E‑21 carrier‑guard codes).
- **Repo consistency / pre‑push:** `scripts/check_ai_refresh_consistency.py` — the admin‑chain closure check.

## Recent domain tools (the last‑24h work) live in their domains

The current study tooling developed recently is kept with its data and write‑ups, not duplicated here:

- `experiments/backblaze_v4_parity_2026-06/` — frozen‑oracle parity harness.
- `experiments/cnq_tiling_highd_2026-06/` — high‑D tiling / tree‑atlas scaling (to D=10⁶).
- `experiments/microbiome_real_2026-06/`, `collaborations/microbiome/code/` — real microbiome runs.
- `industrial-instruments/gas-composition-study/**/code/` — gas / blood‑gas / produced‑water / cabin generators and cohort runners.

*The instrument reads. The expert decides. The hashes carry the receipts. One engine, one run path, deterministic.*
