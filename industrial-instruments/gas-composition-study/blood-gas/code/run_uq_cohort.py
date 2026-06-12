#!/usr/bin/env python3
"""run_uq_cohort.py -- build expired {O2,CO2,N2O,Agent,N2} compositions from the
University of Queensland Vital Signs Dataset per-case zips and run CN-TT on each.
End-tidal channels: etO2, etCO2 (mmHg -> %), etN2O, etSEV/etDES/etISO (agents).
All-zero carriers dropped (D=3..5). Cases lacking etO2/etCO2 or with too few
ventilated rows are skipped (reported). Derived comps OFF-repo; engine outputs +
summary in the repo (instrument, not data).
Usage: python run_uq_cohort.py /path/to/'Queensland Vital Signs Dataset'"""
import sys, os, zipfile, io, json, csv, subprocess
from collections import Counter
import pandas as pd, numpy as np

ZD = sys.argv[1]
REPO = "/sessions/stoic-nifty-davinci/mnt/Claude CoWorker/Current-Repo/Hs"
ENG = REPO + "/HCI-CNTT/run_cntt.py"
COH = REPO + "/industrial-instruments/gas-composition-study/blood-gas/results_real_uq/cohort"; os.makedirs(COH, exist_ok=True)
DERIV = "/sessions/stoic-nifty-davinci/mnt/Claude CoWorker/DATA/Industrial Compositions/_derived/uq"; os.makedirs(DERIV, exist_ok=True)
ET = ["etO2", "etCO2", "etN2O", "etSEV", "etDES", "etISO"]; rows = []

for i in range(1, 33):
    n = "%02d" % i; zp = "%s/uqvitalsignsdata_case%s.zip" % (ZD, n)
    if not os.path.exists(zp): continue
    with zipfile.ZipFile(zp) as z:
        nm = [x for x in z.namelist() if x.endswith("case%s_trenddata.csv" % n)]
        if not nm: rows.append([n, 0, "-", "-", "NO_TREND", False, "-", 0, "-"]); continue
        df = pd.read_csv(io.BytesIO(z.read(nm[0])), usecols=lambda c: c in ET, low_memory=False)
    present = [c for c in ET if c in df.columns]
    for c in present: df[c] = pd.to_numeric(df[c], errors="coerce")
    if "etO2" not in present or "etCO2" not in present:
        rows.append([n, 0, "-", "-", "NO_GAS", False, "-", 0, "-"]); continue
    O2 = df["etO2"]; CO2 = df["etCO2"] / 7.60
    N2O = (df["etN2O"] if "etN2O" in present else pd.Series(0.0, index=df.index)).fillna(0)
    ag = pd.Series(0.0, index=df.index)
    for c in ("etSEV", "etDES", "etISO"):
        if c in present: ag = ag.add(df[c].fillna(0), fill_value=0)
    N2 = 100.0 - O2 - CO2 - N2O - ag
    m = (O2.between(15, 99)) & (df["etCO2"].between(5, 60)) & (N2 > 2) & (ag.between(0, 12))
    L = int(m.sum())
    if L < 40: rows.append([n, L, "-", "-", "FEWROWS", False, "-", 0, "-"]); continue
    P = {"O2": O2, "CO2": CO2, "N2O": N2O, "Agent": ag, "N2": N2}
    P = {k: v[m].values for k, v in P.items()}
    keep = {k: v for k, v in P.items() if len(v) and np.nanmax(v) > 0.05}
    out = pd.DataFrame({"t": np.arange(L)})
    for k, v in keep.items(): out[k] = np.round(v, 3)
    if len(out) > 900: out = out.iloc[::max(1, len(out) // 500)]
    out = out.reset_index(drop=True)
    dcsv = "%s/uq_case%s_expired.csv" % (DERIV, n); out.to_csv(dcsv, index=False)
    oj = "%s/case%s.json" % (COH, n); car = "+".join(keep.keys())
    r = subprocess.run(["python3", ENG, dcsv, "-o", oj], capture_output=True, text=True)
    if r.returncode != 0:
        rows.append([n, len(out), len(keep), car, "ERR", False, "-", 0, "ERR"]); continue
    p = json.load(open(oj)); nav = p["navigation"]; cc = p["input"]["carriers"]
    steps = next((v for v in nav.values() if isinstance(v, list) and v and isinstance(v[0], dict) and "helmsman" in v[0]), [])
    nm2 = lambda h: cc[h] if isinstance(h, int) and 0 <= h < len(cc) else None
    hs = Counter([nm2(s.get("helmsman")) for s in steps if nm2(s.get("helmsman"))]); dom = hs.most_common(1)[0][0] if hs else "-"
    rb = (nav.get("summary", {}).get("regime_boundaries") or nav.get("regime_boundaries") or {})
    rows.append([n, len(out), p["input"]["n_carriers"], car, "%.1e" % p["atlas"]["reconstruction_max_err"], p["atlas"]["lossless"], dom, len(rb.get("indices", [])), p["diagnostics"]["cntt_content_sha256"][:10]])
    print("case %s: D=%d kept=%s lossless=%s dom=%s" % (n, p["input"]["n_carriers"], car, p["atlas"]["lossless"], dom))

with open(COH + "/cohort_summary.csv", "w", newline="") as fp:
    w = csv.writer(fp); w.writerow(["case", "T", "D", "carriers", "recon_err", "lossless", "dominant_helmsman", "n_regimes", "hash10"])
    for r in rows: w.writerow(r)
ok = [r for r in rows if r[5] is True]
print("RAN %d; dominant tally %s" % (len(ok), Counter([r[6] for r in ok]).most_common()))
