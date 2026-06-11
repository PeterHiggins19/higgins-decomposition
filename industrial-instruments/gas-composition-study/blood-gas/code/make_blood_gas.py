#!/usr/bin/env python3
"""make_blood_gas.py -- TRANSPARENT SYNTHETIC generator for Study 3
(blood / alveolar gas, dissolved oxygen). NOT patient data: a clearly-labelled,
physiologically-plausible alveolar gas partial-pressure composition (mmHg)
through a breath-hold (apnea) and recovery, used to demonstrate the Hs (CN-TT)
read. D=4 (O2, CO2, N2, H2O) is CNQ-native -- the move is an EXACT quaternion
rotation. Public reference: standard alveolar gas values / the alveolar gas
equation (pH2O = 47 mmHg at body temperature; partial pressures sum ~760 mmHg).
Fixed seed.

Scenario (30 timepoints, seconds):
  t00-05  resting:   pO2~100  pCO2~40  pH2O=47  pN2 balance (~573)
  t06-18  apnea:     pO2 100->58 (dissolved O2 falls), pCO2 40->54 (rises)
  t19-29  recovery:  pO2 -> ~100, pCO2 -> ~40
"""
import numpy as np, csv, sys
rng = np.random.default_rng(20260611)
T = 30; PB = 760.0; pH2O = 47.0
rows = []
for t in range(T):
    if t < 6:      o2, co2 = 100.0, 40.0
    elif t < 19:   f = (t - 6) / 12.0; o2, co2 = 100 - 42 * f, 40 + 14 * f
    else:          f = (t - 19) / 10.0; o2, co2 = 58 + 42 * f, 54 - 14 * f
    o2  += rng.normal(0, 0.4); co2 += rng.normal(0, 0.3)
    n2 = PB - pH2O - o2 - co2            # balance gas
    rows.append([t, round(o2, 3), round(co2, 3), round(n2, 3), round(pH2O, 3)])
with open(sys.argv[1] if len(sys.argv) > 1 else "blood_gas.csv", "w", newline="") as fp:
    w = csv.writer(fp); w.writerow(["second", "pO2", "pCO2", "pN2", "pH2O"])
    for r in rows: w.writerow(r)
print("wrote blood_gas.csv", T, "rows; alveolar partial pressures mmHg; D=4 CNQ-native")
