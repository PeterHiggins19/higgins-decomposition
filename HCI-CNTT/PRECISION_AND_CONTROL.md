# Precision in the carrier, control in the channel — and the determinism that makes both safe

*Engine doctrine (HCI-CNTT). Companion to DATA_PATH_AND_CHANNELS.md. Every claim below is demonstrated in `experiments/engine_killtest_2026-06/` or the module self-tests. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker; claim tiers at the end.*

---

## The principle

The carrier/channel split (DATA_PATH_AND_CHANNELS.md) extends cleanly into numerics and control:

- **Precision lives in the carrier — the data path.** It is linear, compensated, and exact-to-zero. Nothing nonlinear, lagged, or stateful is allowed to touch the computed composition. The two structural zeros — the closure sum (`Σx = 1`) and the CLR centre (`mean(log x) = 0`) — are defended here, and only here.
- **Control lives in the channel — the decision path.** Hysteresis, dead-bands, hold-locks, and closed-loop action all live here. They annotate and they may act, but by construction they never feed back into the carrier's arithmetic. That is *why* they are safe.

Put the two in their right homes and the determinism of the whole instrument is preserved: the hash is a function of the carrier alone, and the carrier is linear + compensated.

## What the tests showed

**The balanced-twin idea is real, and it is error-feedback noise shaping.** Peter's "balanced twin quaternion, the +/- transitions absorbing the truncation" is the sigma-delta / compensated-summation principle. Accumulating 200,000 truncated adds drifts the result by ~10 as a half-quantum DC bias piles up; carrying the residual forward (the ± transitions) bounds the error to ~1 quantum regardless of N; Kahan/Neumaier drives it to 0. It is deterministic, so it never threatens the hash. (`precise_ops.py`, `ErrorFeedbackAccumulator`.)

**But the per-step CLR does not need it.** Tested honestly: at the engine's operating scale (D ≈ 4..200) numpy already sums pairwise, so compensated closure/CLR are **bit-identical** to the current code (max|diff| = 0.0 at D=4). The benefit appears only at D ≈ 1e4 with wide dynamic range, and even there is marginal (|sum CLR| 7.5e-11 → 6.7e-11). **Conclusion: do not re-base the oracle for it — it changes nothing in the operating regime.** The place truncation actually accumulates is the *stateful* path: a long-running integrator over an automation period. That is where the error-feedback carry earns its keep, and that is where it is used (the SafeLoop integrator).

**Hysteresis must be observe-only — and that is the whole reason it is safe.** A dead-band placed *inside* the loop injects lag and stiction bias straight into the data. The same dead-band kept *observe-only* — it labels the step HOLD/MOVING and never alters the value — leaves the data path **bit-identical to the raw input**. So the hold-lock (`structural_guards.hold_lock`) is feed-forward by design: it cannot accumulate error no matter how slow or noisy the stream. Its trigger is *discovered* from two noise floors — the **system** floor (a robust estimate of the resting motion in the data, re-estimable online) and the **engine** floor (the numerical/determinism floor) — `noise = max(system, engine)`. The leaky integral and the derivative gauge that watch it are read-only: the leaky-I (anti-windup) is the slow-drift alarm; the derivative is the fast-transient early-warning that compensates hysteresis's one weakness, its latency.

## Closed loops are allowed — but only behind breakers

The instrument phase will sometimes need real automation: the instrument acting on its plant over a period. This is permitted, because a valuable concept ends up in instruments we do not foresee — and for exactly that reason the safety envelope is **mandatory**, not optional. `loop_control.SafeLoop` is the only sanctioned way to close the loop:

- **Three states:** OBSERVE (open loop, safe default) → ACTIVE (closed loop, bounded authority, inside a time-boxed automation window) → TRIPPED (latched to a safe output until a human `reset()`).
- **Breakers, checked before any action and first-to-fire-latches:** `LC-TRIP-NAN` (non-finite), `LC-TRIP-RATE` (fast excursion / instability), `LC-TRIP-WIND` (integral windup / runaway), `LC-TRIP-SAT` (saturated too long — fighting the plant), `LC-TRIP-DOG` (watchdog/deadman not serviced). Plus a manual **`LC-ESTOP`** emergency stop anyone can pull at any time.
- **Bounded and gentle:** authority saturation + rate limit + dead-band (won't chase noise) + **TPDF dither** (breaks quantized-actuator limit cycles — tested, lag-2 autocorr 1.00 → 0.06) + **bumpless soft-start** (a large initial offset never trips) + **anti-windup** leaky integrator carried with error-feedback so the integrator itself stays precise over a long run.
- **Graceful exit:** the automation window is time-boxed — when it is exhausted the loop reverts to OBSERVE (`LC-WIN-END`), a normal end, not a fault. Automation is always a leased authority, never a standing one.
- **Deterministic:** seeded dither; same inputs → same outputs. The safety envelope does not break reproducibility.

All seven safety paths self-test PASS (`loop_control._self_test`): converge, runaway→trip, e-stop, time-boxed revert, watchdog, reset, determinism.

## The one-line version

The carrier is exact and linear so the answer is trustworthy and reproducible; the channel may hesitate (hysteresis), hold (hold-lock), or act (SafeLoop) — but always feed-forward, always bounded, always with a breaker and an e-stop, because a dead engine serves nobody and a runaway engine serves nobody either.

## Claim tiers

- `precise_ops` (Neumaier + error-feedback accumulator), the observe-only hold-lock, and `SafeLoop` with all breakers — **Tier 1** (implemented + self-tested + demonstrated).
- The finding that compensated CLR/closure is not worth an oracle re-baseline at operating scale — **Tier 1** (measured: bit-identical at D=4).
- Adopting any compensated reduction inside the *hashed* run path — **Tier 2 / Peter's CI gate** (a one-time oracle re-baseline; not assumed free).
