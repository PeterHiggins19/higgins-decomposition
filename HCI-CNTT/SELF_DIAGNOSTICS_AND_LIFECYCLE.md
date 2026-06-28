# CN‑TT v4 — Self‑Diagnostics (internal vs external shock) + Stage Lifecycle Control

*2026-06-10. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Built + verified by `engine/self_test/self_diagnostics_demo.py` (all checks PASS; the modular self‑test stays green). Two capabilities a larger NASA/USGS system demands of an embedded instrument: (1) tell a central controller *why* a data anomaly occurred — internal or external; (2) run each processing stage under explicit operational state and start/halt control. Extends `CONTROL_POINTS_AND_REMOTE_ADAPTATION.md` and `CNTT_COMPLETE_SPECIFICATION.md`.*

---

## 1 · Internal vs external shock differentiation (FDIR)

**The problem.** A central controller flags an anomaly in the downlinked data and asks the instrument: *did the world change, or did you?* For remote sensing this is critical — an **external** shock (the observed composition genuinely shifted) is a science event to keep; an **internal** shock (a sensor degraded, a carrier channel glitched, a calibration drifted) is a fault to flag, isolate, and possibly roll back.

**The discriminator — cross‑channel coherence on shared carriers.** CN‑TT already carries redundancy: multi‑sensor fusion (one CNT per sensor), triple‑modular redundancy (TMR), or independent charts that overlap on shared carriers. At a flagged shock, take the **K independent observations** of the same composition (in CLR) and compute their robust **consensus** (per‑carrier median = a vote). Then:
- **EXTERNAL** — all channels agree with the consensus (low residual). The shift is shared and coherent → the world really changed. Report the **shock magnitude** = ‖Δconsensus‖.
- **INTERNAL** — one channel diverges from the consensus (high residual). The shift is *not* shared → an instrument/component fault, and **the divergent channel isolates the failed component** (FDIR).

This is the classic detection–isolation logic, expressed in the instrument's own Aitchison geometry; it is a residual/voting computation (Tier 1), not borrowed theory.

```
classify_shock(channel_clrs_now, consensus_prev, resid_threshold) -> 
   {class: EXTERNAL|INTERNAL|UNDETERMINED, faulty_channel, incoherence_max_resid,
    shock_magnitude, channel_residuals, n_channels}
```

**Verified (demo, D=8, 3 channels):**
- External shock (channels coherent): **EXTERNAL**, incoherence 0.053, shock magnitude 3.11.
- Internal fault (channel 1 glitches): **INTERNAL**, **faulty channel = 1**, incoherence 2.84.
- Single channel: **UNDETERMINED** — honest: with no redundancy an instrument cannot self‑distinguish internal from external. The capability requires **≥2 independent channels** (which the multi‑sensor / TMR remote‑sensing context provides).

**The report to a central controller** is therefore one deterministic, hash‑stamped line: *EXTERNAL (real Δ = m)* or *INTERNAL (fault isolated to channel c)* — exactly the self‑diagnostic a larger system demands, and a natural input to the Coherence Supervisor's FDIR and smart‑downlink decisions.

**Honest scope.** Needs redundancy (≥2 independent observations). A deliberate internal adaptation (a logged config/hash change at a control point) is a *known* internal change, distinguished from a *fault* by being intended and recorded — the registry/journal already carries that. Threshold tuning of `resid_threshold` against sensor noise is a calibration step.

## 2 · Stage lifecycle control (operational state + start/halt)

**Each processing stage now runs under an explicit operational state**, held by a `StageController` (stages stay pure compute; the controller holds live state):

`IDLE · READY · RUNNING · BUSY · HALTED · ERROR`

**Commands, stage‑by‑stage:** `halt(stage)` / `start(stage)` (and `halt_all`/`start_all`). The pipeline is state‑aware: before running a stage it checks the controller — a **HALTED** stage blocks itself **and everything downstream** (the run stops, `_halted_at` is recorded, no downstream work happens); a started stage returns to **READY** and the run completes. A stage that raises is marked **ERROR** and the run stops there. Every run reports a per‑stage `_stage_states` snapshot and an `_halted_at`/`_error_at` marker.

**Who controls it.** The `StageController` has an `owner` field — **CN‑TT** drives it now (the Coherence Supervisor can halt a stage on incoherence and roll back); the **same interface** is exposed for an external controller (a domain collaborator, NASA, USGS, or the operator) to drive later. No code change is needed to hand over control — only who issues the commands.

**Verified (demo):** normal run → all six stages cycle to READY; `halt("atlas")` → run halts at atlas (downstream `navigate` does not run; upstream `geometry` stays READY); `start("atlas")` → run completes, all READY. The change is backward‑compatible — with no controller the pipeline behaves exactly as before (modular self‑test stays green).

## 3 · How the two fit the architecture
- The shock classifier is the **detection/isolation** half of FDIR; the stage lifecycle is the **response** half (halt a faulted stage, roll back to last‑known‑good via the control points). Together they are the embedded self‑diagnostic + safe‑state machinery a mission‑critical deployment requires.
- Both are deterministic and hash‑stamped: the shock verdict and the stage‑state chain are receipts a ground receiver / central controller can verify.
- They advance the completeness‑map items **Coherence Supervisor / FDIR** (now partially built: detection + isolation + halt/rollback hooks) and the **control‑point config layer** (the lifecycle commands).

## 4 · Claim tiers
- **Tier 1 (verified):** the shock classifier separates external vs internal and isolates the faulty channel (demo 0.053 vs 2.84); the stage lifecycle (states + halt/start + downstream blocking) works and is backward‑compatible.
- **Tier 2 (sound):** the cross‑channel‑coherence discriminator (FDIR voting/residuals in Aitchison geometry); the controller/owner hand‑off design.
- **Tier 3 (to earn):** `resid_threshold` calibration against real sensor noise; full Coherence‑Supervisor wiring (automatic halt‑on‑incoherence + rollback) and the BUSY/concurrent‑streaming semantics; an end‑to‑end remote demo with a real multi‑sensor stream.

*Files: `engine/shock_diagnostics.py`, `engine/stage_controller.py`, `engine/pipeline.py` (state‑aware run), `engine/self_test/self_diagnostics_demo.py`. The instrument reads — and now it can also say whether the surprise was the world's or its own, and be told to stand down a stage at a time.*
