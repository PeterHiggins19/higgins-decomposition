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

## Key specifications

| Property | Specification |
|---|---|
| **Principle** | reads compositional *dynamics* in Aitchison log‑ratio geometry; D=4 ↔ unit quaternion S³=SU(2), tiled to any D |
| **Lossless reconstruction** | exact recovery from overlapping 4‑part charts, proven to **D = 1,000,000**; demo error ~7e‑15 |
| **Determinism** | same input → same output → same content hash; cross‑platform to **1e‑12** (floats rounded before hashing). *Demonstrated: identical SHA‑256 on Windows and Linux.* |
| **Gauge R&R (analysis stage)** | ≈ **machine epsilon** — the engine adds no measurement variation; propagates the input's (GUM‑compatible) |
| **Reads** | K_eff (effective diversity) · helmsman (driver) · regime boundaries · deceptive drift · attractor/IR class · depth tower |
| **Guard layer (2026‑06)** | resolvability (`HM‑NUL/HM‑TIE`) · coherent helmsman · effective rank (`DG‑RNK`) · hold‑lock (discovered noise floor) · sparsity (`GD‑SPZ`) · E‑21 carrier guard · SafeLoop (bounded closed loop, behind breakers) |
| **Diagnostics** | `SS‑CCC‑LLL` code registry incl. the automated NULL flag; FDIR external‑vs‑internal shock |
| **Confidence policy** | a 6σ industrial / 9σ research **decision gate**; withholds below it (determinism ≠ sigma) |
| **Dependencies** | numpy only (distilled cell); base Python/R for the ports |

## Replication kit (for designers)

Everything needed to **reimplement and wield** the engine — code, pseudocode, and the judgment of how/where/when/why:

- **`CNTT_DESIGNER_SPECIFICATION.md`** — the master replication spec: the "4 W" (who/where/when/why to use it), architecture, every component, the determinism contract, and the **conformance test**.
- **`CNTT_PSEUDOCODE.md`** — the full pipeline as language‑agnostic pseudocode (the reference any port checks against).
- **`../tools/CNTT_single_cell.py`** + **`.ipynb`** — paste‑and‑run Python (verified). · **`../tools/CNTT_replication_notebook.ipynb`** — the annotated, component‑by‑component notebook. · **`../tools/cntt_single_cell.R`** — the R port (1:1 mirror).
- **`ENGINE_CAPABILITIES_DELTA_2026-06.md`** — what the engine can do now beyond the papers. · **`DETERMINISM_GAUGE_RR_AND_CONFIDENCE.md`** — the trust/metrology spec. · **`verify_hash_parity.py`** — the oracle‑parity check for hashed‑path changes.

## Development — June 2026 (the honest‑engine layer)

The engine went from a deterministic *reader* to the same reader **made honest about the limit of its own reading, and able to act behind breakers.** Added (all additive, observe‑only by default, frozen oracle untouched; each module self‑tested, kill‑tests in `../experiments/engine_killtest_2026-06/`): the **resolvability** guard (holds instead of naming a noise leader at rest), the **coherent helmsman** (carrier‑set‑robust), the **effective‑rank** guard, the self‑calibrating **hold‑lock**, **sparsity** awareness + Bayesian‑multiplicative zeros, the built **E‑21** carrier guard, **precise_ops** (compensated arithmetic), and **SafeLoop** (a bounded closed loop behind mandatory breakers + e‑stop). Plus the doctrine that frames it (`PRECISION_AND_CONTROL.md`, `DESIGN_PHILOSOPHY_THE_EXPERT_ENGINE_AND_THE_GUARDS.md`) and the standards path (`../stewardship/iso-standards/PATH_TO_A_STANDARD.md`). Engineering notes for the two hashed‑path items still at the commit gate: `E21_AND_WIRING_TODO.md`.

## Contents
- **`CNTT_COMPLETE_SPECIFICATION.md`** — the single authoritative spec (architecture, stages, navigation family, I/O, verification).
- **`CNTT_DESIGNER_SPECIFICATION.md`** + **`CNTT_PSEUDOCODE.md`** — the designer replication kit (above).
- **`ENGINE_CAPABILITIES_DELTA_2026-06.md`** · **`DETERMINISM_GAUGE_RR_AND_CONFIDENCE.md`** · **`PRECISION_AND_CONTROL.md`** · **`DESIGN_PHILOSOPHY_THE_EXPERT_ENGINE_AND_THE_GUARDS.md`** — the 2026‑06 development docs.
- **`COMPOSITIONAL_MECHANICS.md`** — the complete deterministic kinematics/dynamics of a trajectory (jet · Frenet · momentum/force/energy · integrals · spectral), to its noise‑bounded maximum. · **`TERMINOLOGY_BRIDGE.md`** — the **standing rule: name every quantity by both its navigation and physics term** (helmsman/velocity, arrow‑of‑intent/momentum, …) so every reader finds their handle.
- `MODULAR_ARCHITECTURE.md` — the Stage framework (each section = control point + test point + hash‑cacheable).
- `CNTT_DIAGNOSTIC_CODES.md` — the `SS‑CCC‑LLL` diagnostic/error code system + the automated NULL flag.
- `CONTROL_POINTS_AND_REMOTE_ADAPTATION.md` — the bounded in‑flight control surface (GPCC).
- `SELF_DIAGNOSTICS_AND_LIFECYCLE.md` — internal‑vs‑external shock (FDIR) + stage start/halt control.
- `run_cntt.py` — the CLI. `engine/` — the kernel: `geometry · quaternion · atlas · navigate · helmsman · attractors · diagnostics · codes · provenance · stage · pipeline · stage_controller · shock_diagnostics` **+ the 2026‑06 guard layer: `helmsman_guard · structural_guards · precise_ops · loop_control · zero_methods`**. `engine/self_test/` — BIST (kernel, modular, self‑diagnostics, codes).

## Status
Core instrument **functionally complete and parity‑certified on real data** (Backblaze, full output bit‑identical). Open (advanced) items: corpus‑wide parity harness, interop registry build, streaming, input‑uncertainty propagation — see `../ai-refresh/CNTT_CHAIN_COMPLETENESS_MAP.md` and `../ai-refresh/UNIFIED_AGENDA_2026-06-10.md`.

*The instrument reads. The expert decides. The hashes carry the receipts.*
