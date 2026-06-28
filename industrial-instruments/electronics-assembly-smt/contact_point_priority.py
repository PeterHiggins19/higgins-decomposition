#!/usr/bin/env python3
"""
The Contact-Point Doctrine, made quantitative (planning anchor).

Peter's field law: the machine is dirty at every point of contact with product; contamination radiates from
those points; clean the highest-CONTACT points first, not everywhere. The machine already counts its contacts.

This demo builds a small line of contact points, each with a real-shaped contact count c_i (from the machine
log) and a log-ratio drift d_i (what Hs reads). We compare four maintenance plans:

  - uniform   : clean everything equally          (the wasteful default; no aim)
  - counts    : clean by contact count c_i only   (schedule/usage-based; blind to drift)
  - drift     : clean by drift d_i only           (chases drift; blind to how far it radiates)
  - radiated  : clean by R_i = c_i * d_i          (THE DOCTRINE: contact freq x compositional drift)

The case is built to make the doctrine EARN it: there are two decoys.
  * a busy-but-clean point (highest contacts, ~no drift) -> counts-only chases it and wastes effort.
  * a drifting-but-rarely-touches point (big drift, few contacts) -> drift-only chases it; it barely radiates.
Only R_i = c_i * d_i puts the true emergency (a real fault at a high-contact node) first.
Deterministic; hash-receipted. Internal / planning. Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import hashlib, json
import numpy as np

rng = np.random.default_rng(16)

# Contact points on an SMT/dispense cell: contacts since last clean (from the machine log) + behaviour this run.
#   role: "fault" real drift at a high-contact node (the true emergency) | "busy_clean" decoy | "drift_decoy" |
#         "quiet" normal.
POINTS = {
    "squeegee_edge":  9000,   # MOST contacts, but running clean  -> counts-only decoy
    "nozzle_tip":     6000,   # high contact AND a real clog       -> the true emergency (R wins here)
    "pick_head":      4000,
    "valve_seat":     2500,
    "feeder_pocket":  1500,
    "rail_guide":      300,
    "fiducial_cam":     250,  # drifts a lot but rarely touches product -> drift-only decoy (low radiation)
}
ROLE = {"squeegee_edge": "busy_clean", "nozzle_tip": "fault", "fiducial_cam": "drift_decoy"}

def clr_drift(p_dirty, p_clean):
    L1 = np.log(p_dirty); L1 -= L1.mean()
    L0 = np.log(p_clean); L0 -= L0.mean()
    return float(np.linalg.norm(L1 - L0))

def main():
    names = list(POINTS)
    counts = np.array([POINTS[n] for n in names], float)

    # Each contact point sources a deposit composition {volume, height, footprint, voids}.
    base = np.array([0.45, 0.25, 0.25, 0.05])
    drift = np.zeros(len(names))
    for i, n in enumerate(names):
        clean = base / base.sum()
        role = ROLE.get(n, "quiet")
        if role == "fault":                   # the real clog at a high-contact node (volume down, voids up)
            mult = np.array([0.84, 0.97, 0.99, 1.7])
        elif role == "drift_decoy":           # big drift, but at a point that barely touches product
            mult = np.array([0.70, 1.0, 1.0, 3.0])
        else:                                 # busy_clean + quiet: only measurement noise, no real drift
            mult = 1.0 + 0.01 * rng.standard_normal(4)
        dirty = base * mult
        dirty = dirty / dirty.sum() + 0.002 * rng.standard_normal(4)
        dirty = np.clip(dirty, 1e-4, None); dirty /= dirty.sum()
        drift[i] = clr_drift(dirty, clean)

    R = counts * drift                        # the doctrine: radiated-risk score

    def rank(score): return [names[i] for i in np.argsort(-score)]
    plans = {
        "uniform_clean_everything": names,                 # no aim -- order as listed
        "counts_only":              rank(counts),          # clean by usage/schedule (busy-clean decoy fools it)
        "drift_only":               rank(drift),           # chase drift (low-contact decoy fools it)
        "radiated_R = c*d":         rank(R),               # THE DOCTRINE
    }

    # "effort to first real fix" = how many points you clean before you hit the true top fault (nozzle_tip)
    effort = {k: (v.index("nozzle_tip") + 1) for k, v in plans.items()}

    out = {
        "doctrine": "clean the highest-CONTACT points first; contamination radiates from points of product contact",
        "true_top_fault": "nozzle_tip",
        "per_point": {n: {"contacts": int(counts[i]), "drift": round(float(drift[i]), 4),
                          "R_radiated": round(float(R[i]), 1)} for i, n in enumerate(names)},
        "first_choice_each_plan": {k: v[0] for k, v in plans.items()},
        "points_cleaned_before_reaching_real_fault": effort,
        "verdict": ("R=c*d reaches the nozzle first (%d) vs counts-only (%d) vs uniform (%d)"
                    % (effort["radiated_R = c*d"], effort["counts_only"], effort["uniform_clean_everything"])),
    }
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True).encode()).hexdigest()
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
