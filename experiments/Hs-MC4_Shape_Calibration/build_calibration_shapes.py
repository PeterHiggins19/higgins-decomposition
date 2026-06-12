#!/usr/bin/env python3
"""Build MC-4 calibration shape test data using pure CoDa methodology.

LAW: The projector reveals data structure. It never fabricates.
If the projected shape does not match expectation, the data failed,
not the engine. The engine is an instrument.

Method:
1. Define compositions as proportions summing to 1 (the simplex)
2. Apply standard CLR transform: clr_j = log(x_j) - mean(log(x))
3. Feed to projector pipeline unchanged
4. What you see is what the data IS

No post-hoc adjustment. No normalization tricks. Pure CoDa.
"""
import json, math, os

D = 27  # carriers for all calibration objects
T = 41  # timesteps (0..40, gives clean midpoint at t=20)
CARRIERS = ["C%02d" % i for i in range(D)]

def clr_transform(proportions):
    """Standard CoDa CLR: clr_j = log(x_j) - mean(log(x))"""
    logs = [math.log(max(p, 1e-15)) for p in proportions]
    mean_log = sum(logs) / len(logs)
    return [l - mean_log for l in logs]

def make_polar_stack(experiment, test_object, intervals):
    """Build a polar_stack JSON from interval data."""
    return {
        "experiment": experiment,
        "test_object": test_object,
        "carriers": CARRIERS,
        "intervals": intervals
    }

# ============================================================
# TEST 1: CYLINDER — constant uniform composition
# Expected: circle of constant radius at every time slice
# ============================================================
def build_cylinder():
    intervals = []
    for t in range(T):
        # Uniform composition: all carriers equal
        props = [1.0/D] * D
        clr = clr_transform(props)
        intervals.append({"index": t, "year": t, "clr": {c: clr[j] for j, c in enumerate(CARRIERS)}})
    return make_polar_stack("MC4-CYLINDER", "Cylinder (uniform)", intervals)

# ============================================================
# TEST 2: SPHERE — CLR spread follows sin envelope
# At each time t, one carrier dominates by an amount proportional
# to sin(pi*t/(T-1)). At poles (t=0, t=T-1): nearly uniform.
# At equator (t=T/2): maximum imbalance.
#
# Method: Start with uniform, then redistribute mass following
# a sinusoidal amplitude. The composition is real: proportions
# sum to 1, all positive, CLR computed from actual proportions.
# ============================================================
def build_sphere():
    intervals = []
    for t in range(T):
        # Amplitude of perturbation: 0 at poles, max at equator
        amplitude = math.sin(math.pi * t / (T - 1))
        
        # Create a composition where carrier 0 gets extra mass
        # proportional to amplitude, distributed evenly
        # Use a smooth radial pattern so all carriers contribute
        # to a round cross-section that grows/shrinks
        props = []
        for j in range(D):
            # Base: uniform
            base = 1.0 / D
            # Perturbation: sinusoidal pattern around the polygon
            # Each carrier gets a perturbation based on its angle
            angle = 2 * math.pi * j / D
            # For a circle cross-section at each t, we want ALL carriers
            # to deviate equally from uniform — meaning one group up, one down
            # Use cos to create a dipole pattern (half up, half down)
            perturbation = amplitude * 0.8 * math.cos(angle)
            # Map to positive proportions via softmax-like transform
            props.append(math.exp(perturbation))
        
        # Normalize to sum to 1 (closure operation — standard CoDa)
        total = sum(props)
        props = [p / total for p in props]
        
        clr = clr_transform(props)
        intervals.append({"index": t, "year": t, "clr": {c: clr[j] for j, c in enumerate(CARRIERS)}})
    return make_polar_stack("MC4-SPHERE", "Sphere (sin envelope)", intervals)

# ============================================================
# TEST 3: CUBE — square cross-section, constant through time
# A cube in 27 carriers: groups of carriers form 4 "faces"
# with sharp transitions between high and low values.
# 
# Method: 4 groups of ~7 carriers each get alternating
# high/low proportions, creating a square-like polygon.
# ============================================================
def build_cube():
    intervals = []
    for t in range(T):
        props = []
        for j in range(D):
            # Divide carriers into 4 quadrants
            angle = 2 * math.pi * j / D
            # Square wave: high in quadrants 0,2; low in quadrants 1,3
            # This creates 4 flat faces
            quadrant = int((angle / (math.pi / 2)) % 4)
            if quadrant in (0, 2):
                props.append(math.exp(1.5))  # high
            else:
                props.append(math.exp(-1.5))  # low
        
        total = sum(props)
        props = [p / total for p in props]
        clr = clr_transform(props)
        intervals.append({"index": t, "year": t, "clr": {c: clr[j] for j, c in enumerate(CARRIERS)}})
    return make_polar_stack("MC4-CUBE", "Cube (square cross-section)", intervals)

# ============================================================
# TEST 4: CONE — circle that linearly shrinks from base to apex
# At t=0: maximum spread. At t=T-1: uniform (point).
# ============================================================
def build_cone():
    intervals = []
    for t in range(T):
        # Linear taper from 1.0 to 0.0
        amplitude = 1.0 - t / (T - 1)
        
        props = []
        for j in range(D):
            angle = 2 * math.pi * j / D
            perturbation = amplitude * 0.8 * math.cos(angle)
            props.append(math.exp(perturbation))
        
        total = sum(props)
        props = [p / total for p in props]
        clr = clr_transform(props)
        intervals.append({"index": t, "year": t, "clr": {c: clr[j] for j, c in enumerate(CARRIERS)}})
    return make_polar_stack("MC4-CONE", "Cone (linear taper)", intervals)

# ============================================================
# TEST 5: HELIX — circle that rotates as it moves through time
# The dominant carrier shifts around the polygon over time.
# ============================================================
def build_helix():
    intervals = []
    for t in range(T):
        props = []
        # Phase rotation: the peak rotates around the polygon
        phase = 2 * math.pi * t / (T - 1)  # full rotation over time
        for j in range(D):
            angle = 2 * math.pi * j / D
            perturbation = 0.8 * math.cos(angle - phase)
            props.append(math.exp(perturbation))
        
        total = sum(props)
        props = [p / total for p in props]
        clr = clr_transform(props)
        intervals.append({"index": t, "year": t, "clr": {c: clr[j] for j, c in enumerate(CARRIERS)}})
    return make_polar_stack("MC4-HELIX", "Helix (rotating peak)", intervals)

# ============================================================
# BUILD ALL
# ============================================================
out_dir = "/sessions/wonderful-elegant-pascal"
shapes = {
    "mc4_cylinder": build_cylinder(),
    "mc4_sphere": build_sphere(),
    "mc4_cube": build_cube(),
    "mc4_cone": build_cone(),
    "mc4_helix": build_helix(),
}

for name, data in shapes.items():
    path = os.path.join(out_dir, f"{name}_polar_stack.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    
    # Verify CoDa integrity
    ivs = data["intervals"]
    carriers = data["carriers"]
    clr_sums = [sum(iv["clr"][c] for c in carriers) for iv in ivs]
    max_sum = max(abs(s) for s in clr_sums)
    
    # Check CLR spread variation
    spreads = []
    for iv in ivs:
        vals = [iv["clr"][c] for c in carriers]
        spreads.append(max(vals) - min(vals))
    
    print(f"{name}:")
    print(f"  {len(carriers)} carriers, {len(ivs)} timesteps")
    print(f"  CLR sum check: max |sum| = {max_sum:.2e} (should be ~0)")
    print(f"  CLR spread: min={min(spreads):.4f}, max={max(spreads):.4f}")
    print(f"  Saved to {path}")
    print()

print("All calibration shapes built with pure CoDa CLR transform.")
print("No fabrication. No post-hoc adjustment. Data is sacred.")
