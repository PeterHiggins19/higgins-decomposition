#!/usr/bin/env python3
"""run_vitaldb_cohort.py -- build expired {O2,CO2,Agent,N2} compositions from
Peter-supplied VitalDB anaesthesia CSVs and run CN-TT on each. Derived compositions
are written OFF-repo (DATA/_derived); only engine outputs + summary land in the repo
(instrument, not data). An identically-zero carrier (e.g. a case with no volatile
agent) is dropped -- an all-zero column is not compositional (log(0)). Engine errors
are recorded, not fatal. Usage: python run_vitaldb_cohort.py 1 2 3 ..."""
import sys, os, json, csv, subprocess
from collections import Counter
import pandas as pd, numpy as np

DATA = "/sessions/stoic-nifty-davinci/mnt/Claude CoWorker/DATA/Industrial Compositions"
DERIV = DATA + "/_derived"; os.makedirs(DERIV, exist_ok=True)
REPO = "/sessions/stoic-nifty-davinci/mnt/Claude CoWorker/Current-Repo/Hs"
ENG = REPO + "/HCI-CNTT/run_cntt.py"
COH = REPO + "/industrial-instruments/gas-composition-study/blood-gas/results_real_vitaldb/cohort"
os.makedirs(COH, exist_ok=True)
WANT = ["time", "Primus/FEO2", "Primus/ETCO2", "Primus/EXP_SEVO", "Primus/EXP_DES"]
summary = COH + "/cohort_summary.csv"
out_rows = []

for n in sys.argv[1:]:
    f = "%s/%s.csv" % (DATA, n)
    hdr = pd.read_csv(f, nrows=0).columns.tolist()
    use = [c for c in WANT if c in hdr]
    df = pd.read_csv(f, usecols=use).sort_values("time")
    for c in use:
        if c in ("Primus/ETCO2", "Primus/EXP_SEVO", "Primus/EXP_DES"):
            df[c] = df[c].ffill()
    d = df[df["Primus/FEO2"].notna()].copy()
    O2 = d["Primus/FEO2"].astype(float)
    CO2 = d["Primus/ETCO2"].astype(float) / 7.60
    ag = np.zeros(len(d))
    for c in ("Primus/EXP_SEVO", "Primus/EXP_DES"):
        if c in d.columns:
            ag = ag + d[c].fillna(0).astype(float).values
    AG = pd.Series(ag, index=d.index)
    N2 = 100.0 - O2 - CO2 - AG
    m = (O2.between(25, 75)) & (CO2.between(1, 8)) & (AG.between(0, 9)) & (N2 > 5)
    parts = {"O2": O2[m].values, "CO2": CO2[m].values, "Agent": AG[m].values, "N2": N2[m].values}
    keep = {k: v for k, v in parts.items() if np.nanmax(v) > 0.05}   # drop all-zero carriers
    dropped = [k for k in parts if k not in keep]
    out = pd.DataFrame({"t": d["time"][m].values})
    for k, v in keep.items():
        out[k] = np.round(v, 3)
    if len(out) > 900:
        out = out.iloc[::max(1, len(out) // 500)]
    out = out.reset_index(drop=True)
    if len(out) < 20:
        print("case %s: too few rows (%d) -- skipped" % (n, len(out)))
        continue
    dcsv = "%s/vitaldb_case%s_expired.csv" % (DERIV, n)
    out.to_csv(dcsv, index=False)
    oj = "%s/case%s.json" % (COH, n)
    r = subprocess.run(["python3", ENG, dcsv, "-o", oj], capture_output=True, text=True)
    carstr = "+".join(keep.keys())
    if r.returncode != 0:
        last = (r.stderr.strip().splitlines() or ["?"])[-1][:90]
        print("case %s: ENGINE ERROR -> %s ; recorded + skipped" % (n, last))
        out_rows.append([n, len(out), len(keep), carstr, "ERR", False, "-", 0, "ENGINE_ERR"])
        continue
    p = json.load(open(oj)); nav = p["navigation"]; car = p["input"]["carriers"]
    steps = next((v for v in nav.values() if isinstance(v, list) and v and isinstance(v[0], dict) and "helmsman" in v[0]), [])
    nm = lambda h: car[h] if isinstance(h, int) and 0 <= h < len(car) else None
    hs = Counter([nm(s.get("helmsman")) for s in steps if nm(s.get("helmsman"))])
    dom = hs.most_common(1)[0][0] if hs else "-"
    rb = (nav.get("summary", {}).get("regime_boundaries") or nav.get("regime_boundaries") or {})
    nrb = len(rb.get("indices", []))
    out_rows.append([n, len(out), p["input"]["n_carriers"], carstr,
                     "%.2e" % p["atlas"]["reconstruction_max_err"], p["atlas"]["lossless"],
                     dom, nrb, p["diagnostics"]["cntt_content_sha256"][:12]])
    print("case %s: T=%d D=%d kept=%s dropped=%s lossless=%s err=%.1e dominant=%s regimes=%d share=%s" % (
        n, len(out), p["input"]["n_carriers"], carstr, dropped, p["atlas"]["lossless"],
        p["atlas"]["reconstruction_max_err"], dom, nrb, dict(hs)))

new = not os.path.exists(summary)
with open(summary, "a", newline="") as fp:
    w = csv.writer(fp)
    if new:
        w.writerow(["case", "T", "D", "carriers", "recon_err", "lossless", "dominant_helmsman", "n_regimes", "hash12"])
    for row in out_rows:
        w.writerow(row)
print("appended %d rows to cohort_summary.csv" % len(out_rows))
