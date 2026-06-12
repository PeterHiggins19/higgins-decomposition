# HCI‑CNTT — CN‑TT v4 · the current Hˢ engine

> **This is the current, active Hˢ engine.** It supersedes the now‑archived `HCI-CNT` (CNT v3.2.0) and `HCI-CNQ` (CNQ v2.0.0), which are kept as the **frozen validation oracle** (past reference only). v4 reproduces the entire oracle output **bit‑for‑bit** on real data — see `../experiments/backblaze_v4_parity_2026-06/`.

**New here?** Read [`../HS_GUIDE.md`](../HS_GUIDE.md) (what Hˢ is and how to use it), then the full spec below.

## What it is
CN‑TT v4 is the **tile‑native** Compositional Navigation engine and the reference implementation of **HUF‑STD‑002 (Tensor Train)**. It identifies a four‑part composition with an exact unit quaternion (S³ = SU(2)) and tiles that exactness to any dimension via overlapping charts — **lossless reconstruction proven to D = 1,000,000** — deterministically, with a hash receipt at every step.

## Run it
```
python run_cntt.py  <composition.csv>  -o out.json
```
Input: CSV with a label column + D carrier columns (counts/amounts; zeros treated, closure automatic). At low D the full payload is emitted; at high D the O(D²)/combinatorial blocks auto‑gate off while the O(D) navigation family + lossless tiling carry on.

## Contents
- **`CNTT_COMPLETE_SPECIFICATION.md`** — the single authoritative spec (architecture, stages, navigation family, I/O, verification).
- `MODULAR_ARCHITECTURE.md` — the Stage framework (each section = control point + test point + hash‑cacheable).
- `CNTT_DIAGNOSTIC_CODES.md` — the `SS‑CCC‑LLL` diagnostic/error code system + the automated NULL flag.
- `CONTROL_POINTS_AND_REMOTE_ADAPTATION.md` — the bounded in‑flight control surface (GPCC).
- `SELF_DIAGNOSTICS_AND_LIFECYCLE.md` — internal‑vs‑external shock (FDIR) + stage start/halt control.
- `run_cntt.py` — the CLI. `engine/` — the kernel: `geometry · quaternion · atlas · navigate · helmsman · attractors · diagnostics · codes · provenance · stage · pipeline · stage_controller · shock_diagnostics`. `engine/self_test/` — BIST (kernel, modular, self‑diagnostics, codes).

## Status
Core instrument **functionally complete and parity‑certified on real data** (Backblaze, full output bit‑identical). Open (advanced) items: corpus‑wide parity harness, interop registry build, streaming, input‑uncertainty propagation — see `../ai-refresh/CNTT_CHAIN_COMPLETENESS_MAP.md` and `../ai-refresh/UNIFIED_AGENDA_2026-06-10.md`.

*The instrument reads. The expert decides. The hashes carry the receipts.*
