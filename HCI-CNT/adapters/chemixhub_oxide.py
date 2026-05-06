#!/usr/bin/env python3
"""
HUF-CNT adapter — chemixhub_oxide

Builds a 7-oxide compositional trajectory representative of the
ChemixHub HOIP (Hybrid Organic Inorganic Perovskites) dataset.

Carriers: SiO2, TiO2, Al2O3, Fe2O3, MgO, CaO, Na2O.

DATA NOTE
=========
The ChemixHub repository ships 7 chemistry datasets and its own
data-loading infrastructure (see DEFERRED_ADAPTERS.md §5). This
adapter provides a 24-step illustrative composition trajectory
modelled on the published HOIP-7 oxide-shift profile rather than
calling ChemixHub's own loaders. To swap in raw data, replace
`build_synthetic_oxide()` with code that imports ChemixHub's loaders.
"""
from __future__ import annotations
import csv, math
from pathlib import Path

OXIDES = ["SiO2", "TiO2", "Al2O3", "Fe2O3", "MgO", "CaO", "Na2O"]

# Profile parameters (smooth oxide-shift curve)
PROFILE = [
    # (mean_share, period (steps), phase, amplitude)
    (0.45,  None,  None,  None),  # SiO2 base
    (0.04,  12.0,  0.0,   0.01),
    (0.16,  24.0,  0.0,   0.02),
    (0.10,  24.0,  3.0,   0.02),
    (0.08,  16.0,  1.5,   0.015),
    (0.13,  24.0,  6.0,   0.025),
    (0.04,  24.0,  4.0,   0.01),
]


def build_synthetic_oxide(out_csv: str, n_steps: int = 24) -> str:
    p = Path(out_csv); p.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for i in range(n_steps):
        v = []
        for k, (m, period, phase, amp) in enumerate(PROFILE):
            if period is None:
                v.append(m)
            else:
                v.append(m + amp * math.sin(2*math.pi*i/period + phase))
        # SiO2 absorbs the residual to keep closure
        s_others = sum(v[1:])
        v[0] = max(1.0 - s_others, 0.05)
        # close
        s = sum(v); v = [x/s for x in v]
        rows.append((f"sample_{i:02d}", v))
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sample"] + OXIDES)
        for lab, v in rows:
            w.writerow([lab] + [f"{x:.6f}" for x in v])
    return str(p)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "chemixhub_oxide_input.csv"
    print(f"wrote {build_synthetic_oxide(out)}")
