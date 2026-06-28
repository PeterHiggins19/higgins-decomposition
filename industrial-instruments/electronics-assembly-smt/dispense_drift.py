#!/usr/bin/env python3
"""
Nordson-class dispense case (planning anchor) — a solder-paste deposit is a composition over its
quality budget {volume, height, footprint, voids}. A slow nozzle clog drifts the RATIOS while every
single channel stays in spec (the ratio-blind silent drift). Hs flags it early.

Deterministic; hash-receipted. Internal / planning. Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import hashlib, json, math
import numpy as np

rng = np.random.default_rng(8)
def helmert(D):
    B = np.zeros((D-1, D))
    for i in range(1, D):
        B[i-1, :i] = 1.0/i; B[i-1, i] = -1.0; B[i-1] *= math.sqrt(i/(i+1.0))
    return B
def clr(x): L = np.log(x); return L - L.mean()


def main():
    D = 4; H = helmert(D); T = 120
    base = np.array([0.45, 0.25, 0.25, 0.05])              # volume, height, footprint, voids
    dep = []
    for t in range(T):
        clog = max(0, (t-40))/200.0                        # slow clog from ~deposit 40
        w = base * np.array([1-1.0*clog, 1-0.2*clog, 1-0.1*clog, 1+6.0*clog])
        w = w/w.sum() + 0.004*rng.standard_normal(D); w = np.clip(w, 1e-4, None); w /= w.sum()
        dep.append(w)
    dep = np.array(dep)
    vol_spec = 0.40
    first_single = next((t for t in range(T) if dep[t, 0] < vol_spec), None)
    ref = clr(dep[:30].mean(0)); drift = np.array([np.linalg.norm(clr(dep[t]) - ref) for t in range(T)])
    band = drift[:30].mean() + 5*drift[:30].std()
    first_hs = next((t for t in range(40, T) if drift[t] > band), None)
    arrow = ["volume", "height", "footprint", "voids"][int(np.argmax(clr(dep[-1]) - clr(dep[30])))]
    lead = (first_single - first_hs) if (first_single and first_hs) else None
    out = {"case": "Nordson-class dispense — deposit as a composition; clog = ratio-blind silent drift",
           "deposit_budget": ["volume", "height", "footprint", "voids"],
           "Hs_silent_drift_flag_deposit": first_hs, "single_channel_volume_alarm_deposit": first_single,
           "Hs_lead_time_deposits_before_threshold": lead, "arrow_points_to": arrow}
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
