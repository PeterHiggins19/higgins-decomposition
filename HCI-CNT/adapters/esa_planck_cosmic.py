#!/usr/bin/env python3
"""
HUF-CNT adapter — esa_planck_cosmic

Builds a 5-component cosmic energy-budget compositional trajectory
across cosmic redshift epochs.
Carriers: Dark Energy, Cold Dark Matter, Baryons, Photons, Neutrinos.

DATA NOTE
=========
Today's composition (z=0) comes from Planck 2018 published parameters
(Ω_Λ, Ω_c, Ω_b, Ω_γ, Ω_ν). The trajectory back through redshift uses
the standard Friedmann scaling laws — radiation ∝ a⁻⁴, matter ∝ a⁻³,
dark energy ≈ const — so it is mathematical, not synthetic. To swap in
HEALPix sky-map readouts, see DEFERRED_ADAPTERS.md §3 (FITS files in
DATA/esa-planck/).
"""
from __future__ import annotations
import csv
import math
from pathlib import Path

# Planck 2018 z=0 densities, normalised
PLANCK_2018 = {
    "Dark Energy":      0.6847,
    "Cold Dark Matter": 0.2589,
    "Baryons":          0.0486,
    "Photons":          5.4e-5,
    "Neutrinos":        3.6e-5,
}
# Equation-of-state scaling exponents in (1+z): density ∝ (1+z)^n
SCALING = {
    "Dark Energy":      0.0,   # cosmological constant
    "Cold Dark Matter": 3.0,
    "Baryons":          3.0,
    "Photons":          4.0,
    "Neutrinos":        4.0,
}

CARRIERS = ["Dark Energy", "Cold Dark Matter", "Baryons", "Photons", "Neutrinos"]

# Redshift epochs (T = 17 epochs from z=0 today to z=1100 surface of last scattering)
Z_LIST = [0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0,
          200.0, 500.0, 800.0, 1000.0, 1050.0, 1080.0, 1100.0]


def build_planck_cosmic(out_csv: str) -> str:
    p = Path(out_csv); p.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for z in Z_LIST:
        s = 1.0 + z
        # un-normalised densities at this z
        rho = []
        for c in CARRIERS:
            rho.append(PLANCK_2018[c] * (s ** SCALING[c]))
        tot = sum(rho)
        shares = [r / tot for r in rho]
        rows.append((f"z={z:.1f}", shares))
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["redshift"] + CARRIERS)
        for lab, v in rows:
            w.writerow([lab] + [f"{x:.6e}" for x in v])
    return str(p)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "esa_planck_cosmic_input.csv"
    print(f"wrote {build_planck_cosmic(out)}")
