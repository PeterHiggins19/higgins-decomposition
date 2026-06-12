#!/usr/bin/env python3
"""build_standards.py — Generate the three Hs instrument standards test objects.

Each test object is a known geometric shape built from pure CoDa compositions.
The projector must render these correctly. This is the instrument's type test.

Cylinder: uniform composition at all timesteps → constant circle
Sphere:   CLR spread follows sin envelope → expanding then contracting circle
Cube:     alternating high/low carrier quadrants → square-like cross-section

All compositions sum to 1. All CLR values sum to 0 (to machine precision).
No data fabrication. The data IS the test.
"""
import json, math, os

D = 27  # carriers
T = 41  # timesteps
CARRIERS = [f"C{i+1:02d}" for i in range(D)]

def clr_transform(proportions):
    """Standard CoDa CLR transform: clr_j = log(x_j) - mean(log(x))"""
    log_vals = [math.log(p) for p in proportions]
    mean_log = sum(log_vals) / len(log_vals)
    return [lv - mean_log for lv in log_vals]

def make_polar_stack(experiment, test_object, intervals):
    """Build standard polar_stack JSON structure."""
    return {
        "experiment": experiment,
        "test_object": test_object,
        "carriers": CARRIERS,
        "D": D,
        "N": len(intervals),
        "T": len(intervals),
        "intervals": intervals,
        "methodology": {
            "closure": "proportions sum to 1 (simplex)",
            "transform": "CLR (Aitchison 1986)",
            "normalization": "per-run min-max",
            "purpose": "Hs instrument standards test — known geometric object"
        }
    }

def build_cylinder():
    """Uniform composition at all timesteps. CLR = 0 everywhere.
    Expected projection: constant circle through time. No degenerate timesteps
    because all timesteps are degenerate (uniform) — the entire run is uniform."""
    intervals = []
    for t in range(T):
        props = [1.0 / D] * D  # perfectly uniform
        clr = clr_transform(props)
        intervals.append({
            "index": t,
            "year": t,
            "proportions": {c: props[j] for j, c in enumerate(CARRIERS)},
            "clr": {c: clr[j] for j, c in enumerate(CARRIERS)}
        })
    return make_polar_stack("STD-CYLINDER", "Cylinder Standard", intervals)

def build_sphere():
    """CLR spread follows sin envelope. Poles at t=0 and t=T-1 are degenerate
    (all carriers equal). Maximum spread at t=T/2 (equator).
    Expected projection: circle expanding from pole to equator, contracting back."""
    intervals = []
    for t in range(T):
        amplitude = math.sin(math.pi * t / (T - 1))
        props = []
        for j in range(D):
            angle = 2 * math.pi * j / D
            perturbation = amplitude * 0.8 * math.cos(angle)
            props.append(math.exp(perturbation))
        total = sum(props)
        props = [p / total for p in props]
        clr = clr_transform(props)
        intervals.append({
            "index": t,
            "year": t,
            "proportions": {c: props[j] for j, c in enumerate(CARRIERS)},
            "clr": {c: clr[j] for j, c in enumerate(CARRIERS)}
        })
    return make_polar_stack("STD-SPHERE", "Sphere Standard", intervals)

def build_cube():
    """Alternating high/low carrier quadrants. Constant cross-section over time.
    Carriers split into 4 groups with distinct proportions to create square-like shape.
    Expected projection: square-like polygon, constant through time."""
    intervals = []
    # Split carriers into 4 quadrants
    q_size = D // 4
    for t in range(T):
        props = []
        for j in range(D):
            quadrant = j // q_size
            if quadrant == 0:
                props.append(2.0)   # high
            elif quadrant == 1:
                props.append(0.5)   # low
            elif quadrant == 2:
                props.append(2.0)   # high
            else:
                props.append(0.5)   # low (includes remainder carriers)
        total = sum(props)
        props = [p / total for p in props]
        clr = clr_transform(props)
        intervals.append({
            "index": t,
            "year": t,
            "proportions": {c: props[j] for j, c in enumerate(CARRIERS)},
            "clr": {c: clr[j] for j, c in enumerate(CARRIERS)}
        })
    return make_polar_stack("STD-CUBE", "Cube Standard", intervals)

def verify_clr(ps, name):
    """Verify CLR sums to 0 and proportions sum to 1."""
    for i, iv in enumerate(ps["intervals"]):
        clr_vals = [iv["clr"][c] for c in ps["carriers"]]
        clr_sum = sum(clr_vals)
        prop_vals = [iv["proportions"][c] for c in ps["carriers"]]
        prop_sum = sum(prop_vals)
        if abs(clr_sum) > 1e-10:
            print(f"  WARNING {name} t={i}: CLR sum = {clr_sum}")
        if abs(prop_sum - 1.0) > 1e-10:
            print(f"  WARNING {name} t={i}: prop sum = {prop_sum}")
    vals = [iv["clr"][c] for iv in ps["intervals"] for c in ps["carriers"]]
    spread = max(vals) - min(vals)
    degen_count = sum(1 for iv in ps["intervals"]
                      if max(iv["clr"][c] for c in ps["carriers"]) - min(iv["clr"][c] for c in ps["carriers"]) < 1e-4)
    print(f"  {name}: {len(ps['intervals'])} timesteps, CLR range [{min(vals):.6f}, {max(vals):.6f}], "
          f"spread={spread:.6f}, degenerate={degen_count}")

if __name__ == "__main__":
    import sys
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."

    for name, builder in [("cylinder", build_cylinder), ("sphere", build_sphere), ("cube", build_cube)]:
        ps = builder()
        path = os.path.join(outdir, name, f"STD-{name}_polar_stack.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(ps, f, indent=2)
        print(f"Wrote {path}")
        verify_clr(ps, name)
