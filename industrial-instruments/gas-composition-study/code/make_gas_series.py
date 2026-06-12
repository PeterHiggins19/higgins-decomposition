#!/usr/bin/env python3
"""make_gas_series.py — TRANSPARENT SYNTHETIC generator for the Hs general
gas-composition study. NOT real patient/flight data: a clearly-labelled,
physiologically-plausible closed-loop breathing-gas scenario (O2/CO2/N2, dry
volume %) used to demonstrate the Hs (CN-TT) compositional read. The public-data
verification target (VitalDB et al.) is specified in the study README; this
generator exists so the demonstration is fully reproducible (fixed seed).

Scenario (60 one-minute steps), designed to exercise MC-4 (composition monitoring):
  t00-19  Nominal closed loop:        O2~21.0  CO2~0.5   N2 balance
  t20-39  CO2 scrubber degradation:   CO2 ramps 0.5->5.0; O2 drifts 21.0->19.6
  t40     Scrubber replaced (step):   CO2 -> ~0.6;  O2 -> ~20.8
  t41-44  Settle to nominal
  t45-51  O2 supply fault:            O2 falls 20.8->16.8; CO2 steady; N2 rises
  t52-59  Sub-threshold deceptive drift: every gas kept inside its single-channel
          'normal band' while the O2:CO2:N2 RATIO rotates (the ratio-blindness case)
"""
import numpy as np, csv, sys

rng = np.random.default_rng(20260611)
T = 60
O2 = np.empty(T); CO2 = np.empty(T)

for t in range(T):
    if t < 20:                              # nominal
        o2, co2 = 21.0, 0.5
    elif t < 40:                            # scrubber degradation
        f = (t - 20) / 19.0
        o2, co2 = 21.0 - 1.4 * f, 0.5 + 4.5 * f
    elif t < 41:                            # scrubber replaced (step)
        o2, co2 = 20.8, 0.6
    elif t < 45:                            # settle
        o2, co2 = 20.9, 0.55
    elif t < 52:                            # O2 supply fault
        f = (t - 45) / 6.0
        o2, co2 = 20.8 - 4.0 * f, 0.55
    else:                                   # sub-threshold deceptive ratio drift
        f = (t - 52) / 7.0
        o2, co2 = 19.9, 0.6 + 0.8 * f       # CO2 0.6->1.4 (kept < 1.5 'ok'), O2 ~19.9 (>19.5 'ok')
    O2[t] = o2 + rng.normal(0, 0.05)
    CO2[t] = max(0.01, co2 + rng.normal(0, 0.02))

N2 = 100.0 - O2 - CO2                        # balance gas (dry basis)

with open(sys.argv[1] if len(sys.argv) > 1 else "gas_series.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["minute", "O2", "CO2", "N2"])
    for t in range(T):
        w.writerow([t, round(float(O2[t]), 4), round(float(CO2[t]), 4), round(float(N2[t]), 4)])
print("wrote gas_series.csv", T, "rows; O2/CO2/N2 dry volume %")
