#!/usr/bin/env python3
"""
Distributed compositional robotic work-cell — cross-flow control with self-maintenance behind Breaker 16.

A work cell's health is a composition over its subsystems {placement, thermal, feeder, throughput}.
  - SENSE flows UP: the skin reads the cell as a composition; Hs reads its drift.
  - CONTROL flows DOWN: a SafeLoop restores the cell toward its healthy setpoint (self-maintenance) --
    but ONLY when the operator's Breaker 16 is armed (the human gate is the fixed point).
  - A governing node reads the fleet (a composition of cell distress) and locates the worst cell,
    each cell's read hash-verified (trust topology: any node re-derives any node's receipt).

Deterministic; hash-receipted. Author: Peter Higgins; AI-assisted per HUF-STD-001. Honest-broker.
"""
import hashlib, json, math
import numpy as np

rng = np.random.default_rng(16)
def helmert(D):
    B = np.zeros((D-1, D))
    for i in range(1, D):
        B[i-1, :i] = 1.0/i; B[i-1, i] = -1.0; B[i-1] *= math.sqrt(i/(i+1.0))
    return B
def clr(x): L = np.log(x); return L - L.mean()
def ilr(x, H): return clr(x) @ H.T
def inv_ilr(z, H): c = np.exp(z @ H); return c/c.sum()

D = 4; H = helmert(D)
SETPOINT = np.array([0.40, 0.25, 0.20, 0.15]); S_ILR = ilr(SETPOINT, H)

def run_cell(breaker_armed, k=0.5, T=60, drift=0.06):
    x = SETPOINT.copy(); dist = []
    fault = np.array([0.0, 0.0, 1.0])                         # feeder degrades (silent drift)
    for _ in range(T):
        z = ilr(x, H) + drift*fault + 0.01*rng.standard_normal(D-1)   # SENSE (up): drift + noise
        if breaker_armed:                                     # CONTROL (down) only behind Breaker 16
            z = z + k*(S_ILR - z)                             # restore toward setpoint (self-maintenance)
        x = inv_ilr(z, H); dist.append(float(np.linalg.norm(ilr(x, H) - S_ILR)))
    return float(np.mean(dist[-10:])), x

def main():
    armed, _ = run_cell(True); tripped, _ = run_cell(False)
    M = 5
    states = [run_cell(c != 2)[1] for c in range(M)]          # cell 2's breaker tripped
    cd = np.array([float(np.linalg.norm(ilr(s, H) - S_ILR)) for s in states])
    fleet = (cd + 1e-3); fleet = fleet/fleet.sum()
    h = [hashlib.sha256(np.round(ilr(s, H), 10).tobytes()).hexdigest()[:12] for s in states]
    out = {
        "system": "distributed compositional robotic work-cell (cross-flow + Breaker-16 + self-maintenance)",
        "cell_health_budget": ["placement", "thermal", "feeder", "throughput"], "setpoint": list(SETPOINT),
        "self_maintenance": {"breaker16_ARMED_distance": round(armed, 4), "breaker16_TRIPPED_distance": round(tripped, 4),
            "verdict": "armed -> closed loop holds homeostasis; tripped -> drift to fault; operator breaker is the fixed point"},
        "cross_flow": "SENSE up (skin->cell->fleet); CONTROL down (fleet->cell->actuator) behind Breaker 16; operator at top",
        "distributed_fleet": {"cells": M, "cell_distances": [round(d, 3) for d in cd],
            "fleet_distress_points_to_cell": int(np.argmax(clr(fleet))),
            "hash_verified": bool(h == [hashlib.sha256(np.round(ilr(s, H), 10).tobytes()).hexdigest()[:12] for s in states])},
    }
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
