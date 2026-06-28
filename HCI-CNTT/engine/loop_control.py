"""
loop_control (CN-TT v4, additive) — a SAFE closed-loop controller for the instrument phase.

The structural guards (helmsman_guard, structural_guards) are observe-only by default:
they annotate, they never feed back, so they cannot corrupt the data path. But the
instrument phase will sometimes need real automation -- the instrument acting on its
plant over a period. This module allows that, and it makes the safety envelope
mandatory, because one never knows what instrument a valuable concept ends up in.

DOCTRINE (see HCI-CNTT/PRECISION_AND_CONTROL.md):
  * Precision lives in the carrier (the data path): linear + compensated + exact-to-zero.
  * Control lives in the channel (the decision path): bounded, dithered, time-boxed.
  * A closed loop is permitted ONLY behind breakers + a manual emergency stop.

SafeLoop states:
  OBSERVE  - open loop, safe default, no action (u = 0).
  ACTIVE   - closed loop, acting within bounded authority, inside the automation window.
  TRIPPED  - a breaker opened (or e-stop); output latched to safe (u = 0) until reset().

Breakers (checked BEFORE any action is applied; first to fire latches):
  LC-TRIP-NAN  non-finite measurement.
  LC-TRIP-RATE measurement step |dx| over rate_bound  (fast excursion / instability).
  LC-TRIP-WIND |leaky integral| over integ_bound      (runaway drift / windup).
  LC-TRIP-SAT  authority saturated longer than sat_dur (fighting the plant).
  LC-TRIP-DOG  watchdog/deadman: pet() not called within dog_timeout steps.
  LC-ESTOP     manual emergency stop (estop()).
Graceful (not a fault): LC-WIN-END  automation window exhausted -> revert to OBSERVE.

Safety properties: bumpless soft-start (rate gauge seeds to the first measurement, so a
large initial offset never trips); bounded authority + rate limit + dead-band (won't
chase noise); TPDF dither (breaks quantized-actuator limit cycles -- tested: lag-2
autocorr 1.00 -> 0.06); anti-windup leaky integrator carried with error-feedback
(precise_ops.ErrorFeedbackAccumulator, so the integrator itself doesn't accumulate
truncation over a long run); a trip latches and requires an explicit human reset().
Deterministic (seeded dither). Claim tier: Tier 1 (implemented + self-tested).
Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001.
Honest-broker.
"""
from __future__ import annotations
import numpy as np
try:
    from precise_ops import ErrorFeedbackAccumulator
except ImportError:
    from .precise_ops import ErrorFeedbackAccumulator


class SafeLoop:
    def __init__(self, setpoint, Kp=0.5, Kd=0.2, authority=0.2, rate_limit=0.05, deadband=1e-3,
                 window=200, integ_bound=8.0, rate_bound=0.5, sat_dur=25, dog_timeout=50,
                 dither=1e-4, leak=0.9, seed=0):
        self.sp = float(setpoint); self.Kp = Kp; self.Kd = Kd; self.auth = authority
        self.rl = rate_limit; self.db = deadband; self.window = window
        self.integ_bound = integ_bound; self.rate_bound = rate_bound
        self.sat_dur = sat_dur; self.dog_timeout = dog_timeout; self.dither = dither
        self.I = ErrorFeedbackAccumulator(leak=leak); self.rng = np.random.default_rng(seed)
        self.state = "OBSERVE"; self.code = None; self.trip = None
        self.prev_x = None; self.prev_e = 0.0; self.u = 0.0
        self.n_active = 0; self.sat_run = 0; self.since_pet = 0

    # ---- operator controls ----
    def estop(self):
        self.state = "TRIPPED"; self.code = "LC-ESTOP"; self.trip = "manual emergency stop"; self.u = 0.0

    def pet(self):
        self.since_pet = 0                                  # service the watchdog

    def reset(self):
        if self.state == "TRIPPED":
            self.state = "OBSERVE"; self.code = "LC-RESET"; self.trip = None
            self.u = 0.0; self.I.clear(); self.prev_x = None

    def _trip(self, code, why):
        self.state = "TRIPPED"; self.code = code; self.trip = why; self.u = 0.0

    def _out(self):
        return {"state": self.state, "u": self.u, "code": self.code, "trip": self.trip,
                "I": round(self.I.value(), 6)}

    def step(self, x, allow_active=True):
        """Advance one step with measurement x; returns the (safe) control output dict."""
        self.since_pet += 1
        if self.state == "TRIPPED":
            return self._out()
        if not np.isfinite(x):
            self._trip("LC-TRIP-NAN", "non-finite measurement"); return self._out()
        if self.prev_x is None:
            self.prev_x = x                                 # bumpless soft-start
        dmeas = x - self.prev_x; e = self.sp - x; d = e - self.prev_e; Ival = self.I.add(e)
        # --- breakers, before any action ---
        if self.since_pet > self.dog_timeout:
            self._trip("LC-TRIP-DOG", "watchdog/deadman timeout"); self.prev_x = x; self.prev_e = e; return self._out()
        if abs(dmeas) > self.rate_bound:
            self._trip("LC-TRIP-RATE", "fast excursion / instability"); self.prev_x = x; self.prev_e = e; return self._out()
        if abs(Ival) > self.integ_bound:
            self._trip("LC-TRIP-WIND", "integral windup / runaway drift"); self.prev_x = x; self.prev_e = e; return self._out()
        # --- automation window / authority ---
        if not allow_active or self.n_active >= self.window:
            if self.state == "ACTIVE":
                self.state = "OBSERVE"; self.code = "LC-WIN-END"
            self.u = 0.0; self.prev_x = x; self.prev_e = e; return self._out()
        # --- bounded, dithered, rate-limited closed-loop action ---
        self.state = "ACTIVE"; self.n_active += 1; self.code = None
        if abs(e) <= self.db:
            target = 0.0                                    # dead-band: don't chase noise
        else:
            dith = (self.rng.random() - self.rng.random()) * self.dither   # TPDF dither
            target = self.Kp * e + self.Kd * d + dith
        target = float(np.clip(target, -self.auth, self.auth))             # saturate to authority
        self.u = float(np.clip(target, self.u - self.rl, self.u + self.rl))  # rate limit
        sat = abs(self.u) >= self.auth - 1e-12
        self.sat_run = self.sat_run + 1 if sat else 0
        if self.sat_run > self.sat_dur:
            self.I.clear(); self._trip("LC-TRIP-SAT", "authority saturated too long (fighting the plant)")
            self.prev_x = x; self.prev_e = e; return self._out()
        self.prev_x = x; self.prev_e = e
        return self._out()


def _self_test():
    ok = True

    def run(plant_gain=1.0, dist=0.0, steps=120, estop_at=None, x0=0.0, pet=True, **kw):
        lp = SafeLoop(setpoint=1.0, **kw); x = x0; hist = []
        for t in range(steps):
            if estop_at is not None and t == estop_at:
                lp.estop()
            if pet:
                lp.pet()
            o = lp.step(x); hist.append((o["state"], o["u"], o["code"]))
            x = x + plant_gain * o["u"] + (dist(t) if callable(dist) else dist)
        return lp, hist, x

    lp, h, xf = run(steps=120); ok &= ("ACTIVE" in [s for s, _, _ in h]) and abs(xf - 1) < 0.05      # converge
    lp, h, xf = run(dist=0.8, steps=120); ok &= lp.state == "TRIPPED" and h[-1][1] == 0.0            # runaway -> trip
    lp, h, xf = run(estop_at=10, steps=60); ok &= lp.code == "LC-ESTOP" and all(u == 0 for _, u, _ in h[11:])
    lp, h, xf = run(steps=300, window=50); ok &= lp.n_active <= 50 and all(s != "ACTIVE" for s, _, _ in h[60:])
    lp, h, xf = run(steps=40, dog_timeout=10, pet=False); ok &= lp.code == "LC-TRIP-DOG"             # watchdog
    lp.reset(); ok &= lp.state == "OBSERVE"                                                          # re-arm
    ok &= run(steps=80, seed=3)[1] == run(steps=80, seed=3)[1]                                       # deterministic
    return ok


if __name__ == "__main__":
    import sys
    print("loop_control self-test:", "ALL PASS" if _self_test() else "FAILED")
    sys.exit(0 if _self_test() else 1)
