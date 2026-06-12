#!/usr/bin/env python3
"""make_cabin_atmosphere.py -- TRANSPARENT SYNTHETIC generator for Study 4
(spacecraft cabin atmosphere gas composition). NOT telemetry: a clearly-labelled,
ISS-like cabin atmosphere composition (dry volume %, + humidity + trace) over
time, used to demonstrate the Hs (CN-TT) read. Public reference: ISS cabin
atmosphere management (total ~14.7 psia sea-level-equivalent; ppO2 ~21%; CO2
held low by the Carbon Dioxide Removal Assembly, CDRA, on a duty cycle; cabin
humidity controlled). Models a CDRA duty cycle, an O2 top-up, and a trace-VOC
contaminant event. Fixed seed.

Carriers: N2 O2 CO2 H2O trace  (D=5), 48 hourly steps.
  CDRA sawtooth: CO2 rises when the scrubber bed is loading, drops when it cycles.
  t20  O2 top-up after consumption dip.
  t34  trace VOC contaminant spike (a real cabin event -> a composition shift).
"""
import numpy as np, csv, sys
rng = np.random.default_rng(20260611)
T = 48
rows = []
for t in range(T):
    co2 = 0.30 + 0.40 * ((t % 12) / 12.0)              # CDRA sawtooth 0.30->0.70
    o2 = 20.9 - (0.6 * max(0.0, 1 - abs(t - 18) / 4.0))  # consumption dip ~t18, topped up by t20
    if t >= 20 and t < 24: o2 = 20.9
    trace = 0.02 + (0.13 if 34 <= t <= 38 else 0.0) * (1 - abs(t - 36) / 3.0 if 34 <= t <= 38 else 0)
    h2o = 0.80 + rng.normal(0, 0.02)
    o2 += rng.normal(0, 0.03); co2 += rng.normal(0, 0.01); trace = max(0.001, trace)
    n2 = 100.0 - o2 - co2 - h2o - trace               # balance
    rows.append([t, round(n2, 4), round(o2, 4), round(co2, 4), round(h2o, 4), round(trace, 4)])
with open(sys.argv[1] if len(sys.argv) > 1 else "cabin_atmosphere.csv", "w", newline="") as fp:
    w = csv.writer(fp); w.writerow(["hour", "N2", "O2", "CO2", "H2O", "trace"])
    for r in rows: w.writerow(r)
print("wrote cabin_atmosphere.csv", T, "rows; cabin atmosphere dry vol % + humidity + trace; D=5")
