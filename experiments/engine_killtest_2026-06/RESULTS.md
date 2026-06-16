# Engine kill-test — structural blind spots and their fixes (2026-06-12)

*Break-it-and-fix-it on the engine itself. These are properties of the CN-TT definition (CLR + argmax helmsman), not of bad data. Each is demonstrated, then fixed. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker; claim tiers below. Reproduce: `python blind_spots_demo.py`. Fix: `HCI-CNTT/engine/helmsman_guard.py`.*

---

## The blind spots (demonstrated)

**1 · Near the barycentre, the helmsman is numerical noise.** At a uniform / unchanging composition the step motion sits at the determinism floor (~1e-9). `argmax |ΔCLR|` still returns a confident "leader" — but it is noise: a *different* carrier each random seed (2, 3, 4, 3…). The engine names a leader where there is none.

**2 · CLR is subcompositionally incoherent.** The helmsman of (A,B,C) is **A** computed alone, but **C** once an *irrelevant* fourth carrier D is added — because the CLR centre is the geometric mean over *all* present parts, so adding a part shifts every CLR value. Adding a carrier changed the read of the others. (This is a textbook CoDa property; here it's shown to bite the helmsman directly.)

**3 · Exact ties break by index.** Two carriers moving identically are separated arbitrarily by column order — the engine reports one as *the* leader with no signal that it was a coin-flip.

A fourth, by-design (named for completeness, not a bug): **magnitude blindness** — the engine reads ratios, so a composition constant in shape but changing in total scale is correctly invisible to it (that is MC-1's job; the paired-measurement doctrine covers it).

## The fix (verified)

`helmsman_guard.py` reports **resolvability**, not just an argmax:

| case | naive engine | guarded |
|---|---|---|
| barycentre / no motion | a noise carrier | **None** + `HM-NUL-WRN` |
| clear single mover | that carrier | that carrier (no code) |
| identical top movers | arbitrary index | **`TIE`** + `HM-TIE-WRN` (margin 0.0) |

It returns the motion **magnitude** (is there resolvable motion above the floor?) and the **margin** to the runner-up (is the leader separated, or a near-tie?), and it carries the **subcompositional note** for blind spot 2: *the CLR helmsman is relative to the declared carrier set; for cross-set comparison use ILR balances, which are coherent.* Self-test: all cases pass. Never names a leader at rest; never breaks a tie silently.

## The Tier-2 fixes — now built (`HCI-CNTT/engine/structural_guards.py`, self-tested)

**Coherent helmsman (fixes blind spot 2).** `coherent_helmsman(P)` ranks carriers by their mean **pairwise log-ratio** motion, `log(x_i/x_j)`. Pairwise log-ratios are closure-invariant — `x_i/x_j` is unchanged when other parts are added or removed — so this helmsman does **not** move when an irrelevant carrier is added. Verified: the CLR helmsman of (A,B,C) flips **A → C** once D is added; the coherent helmsman stays **A**. This is the subcompositionally-coherent read the note called for.

**SVD effective-rank guard.** `effective_rank(P)` takes the SVD of the centred CLR trajectory and reports the effective number of moving dimensions (participation ratio of the singular values), flagging **`DG-RNK-WRN`** when motion is confined to a subspace — the regime that drives the `eigh` depth/stage diagnostics toward near-zero eigenvalues (an E-21 sibling, different cause). Verified: a rank-1 line trajectory → eff-rank **1.0 / 4**, flagged; full-rank random → **3.79 / 4**, clean.

**Hold-lock with hysteresis (ties down near-zero drift; registers only valid structural change).** `hold_lock(P)` is a Schmitt-trigger dead-band on structural change. It **discovers** the trigger from two noise floors — the **system** noise floor (a robust estimate of the resting motion in the data, re-estimable as data accrues) and the **engine** noise floor (the numerical/determinism floor) — and uses `noise = max(system, engine)`. With hysteresis (enter MOVING above `k_up·noise`, return to HOLD below `k_down·noise`, `k_down < k_up`) it holds the read steady through sub-floor drift and registers a structural change only when an excursion is **sustained** and its net Aitchison displacement is **deemed structural** (`≥ struct_k·noise`). Verified: through rest → real shift → rest it registers **exactly one** change; on pure noise it registers **zero** (the near-zero drift is tied down — but the HOLD state is *announced*, never silent); on a borderline series the hysteresis cuts chattering from **13 → 7** toggles vs a single threshold. The held drift is identified, not hidden.

## Remaining (Peter's gate)

- **Wire the codes into `run_cntt`** so `HM-NUL-WRN` / `HM-TIE-WRN` / `DG-RNK-WRN` ride on the receipt — attached *conditionally* (only when a code fires), so clean / oracle data stays hash-neutral (the proven E-21 carrier-guard pattern). The `hold_lock` monitor is a run-series layer (opt-in), not a per-receipt field, so it never perturbs the oracle hash. Full always-on integration needs a CI oracle-parity re-test — Peter's commit gate.

## Claim tiers

- The three demonstrated blind spots, the helmsman-guard fix, and all three Tier-2 fixes (coherent helmsman, SVD rank guard, hold-lock hysteresis) — **Tier 1** (computed, self-tested, reproducible).
- The `run_cntt` always-on wiring — **Tier 2** (recipe known; awaits CI parity re-test at Peter's gate).

*The instrument flags; the expert decides. Now it also flags when it cannot honestly name a leader — at rest, in a tie, in a collapsed subspace — and it holds steady through noise, moving only when the change is real. A kill-test the engine passes by admitting what it cannot resolve, and by refusing to chase its own noise floor.*
