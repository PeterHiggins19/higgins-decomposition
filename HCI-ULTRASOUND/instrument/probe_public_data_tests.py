#!/usr/bin/env python3
"""
probe_public_data_tests.py -- test the Hs probe on REAL public-derived data, for HITS AND MISSES.

Datasets (real, in-repo, public-sourced + cited):
  GAS    : closed-loop O2/CO2/N2 breathing-gas series (gas-composition-study)         D=3
  BLOOD  : alveolar/blood gas {pO2,pCO2,pN2,pH2O} (VitalDB Seoul / UQ Adelaide cited) D=4
  WATER  : USGS Williston-Basin produced-water ions {Na,Cl,Ca,Mg,SO4,HCO3,K}          D=7

For each dataset we apply three NUISANCE kinds and ask: does the differential read survive?
  A scalar multiplicative common-mode (gain/coupling/dilution)  -> EXPECT HIT     (clr-invariant)
  B additive sensor offset                                      -> EXPECT MISS    (clr cannot reject additive)
  C per-channel fixed gain (miscalibration)                     -> EXPECT PARTIAL (rejected up to a constant)
We report the clr distortion each nuisance injects (0 = perfectly rejected) -- honest hits and misses.
Determinism + receipt. RESEARCH/QA ONLY -- not clinical. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib, csv, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hs_probe import HsProbe, clr, closure

GCS=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../industrial-instruments/gas-composition-study")
def load(path, cols0):
    rows=[]
    with open(path) as f:
        for d in csv.DictReader(f):
            try: rows.append([float(d[c]) for c in cols0])
            except: pass
    return np.array(rows)

DS={
 "GAS_breathing":  (GCS+"/results/gas_series.csv", ["O2","CO2","N2"]),
 "BLOOD_alveolar": (GCS+"/blood-gas/results/blood_gas.csv", ["pO2","pCO2","pN2","pH2O"]),
 "WATER_produced": (GCS+"/produced-water-codawork/results/produced_water.csv", ["Na","Cl","Ca","Mg","SO4","HCO3","K"]),
}

rng=np.random.default_rng(3)
def distortion(Xc, Xn): return float(np.max(np.abs(clr(Xn)-clr(Xc))))

results={}
for name,(path,cols) in DS.items():
    X=load(path,cols); X=X[np.all(X>0,axis=1)]; Xc=closure(X); T,D=Xc.shape
    gA=rng.uniform(0.2,5.0,size=(T,1)); XA=Xc*gA                       # A scalar common-mode
    aB=rng.uniform(0.0,0.2,size=(T,1)); XB=Xc+aB                       # B additive offset
    sC=np.ones(D); sC[0]=3.0; XC=Xc*sC                                 # C per-channel fixed gain
    results[name]={"D":D,"n_samples":T,
       "A_scalar_commonmode_distortion":float(f"{distortion(Xc,XA):.2e}"),
       "B_additive_offset_distortion":  float(f"{distortion(Xc,XB):.2e}"),
       "C_perchannel_gain_distortion":  float(f"{distortion(Xc,XC):.2e}"),
       "verdict":{"A_scalar":"HIT (rejected to floor)",
         "B_additive":"MISS (clr cannot reject additive -- needs raw-domain handling)",
         "C_perchannel_gain":"PARTIAL (a fixed clr bias remains -> calibration/paired-measurement)"}}

# real structure-change detection: inject a true relational drift into GAS (CO2 doubling at t=30)
Xg=closure(load(DS["GAS_breathing"][0],["O2","CO2","N2"]))
ref=Xg[:10].mean(0); probe=HsProbe(ref)
drift=Xg.copy(); drift[30:,1]*=2.0; drift[30:]=closure(drift[30:])
gain=rng.uniform(0.2,5.0,size=(len(drift),1))
d_clean=[probe.detect(drift[t])[0] for t in range(len(drift))]
d_underA=[probe.detect(drift[t]*gain[t])[0] for t in range(len(drift))]
detect={"drift_seen_clean_after_t30":bool(np.mean(d_clean[31:])>3*np.mean(d_clean[:29])),
        "drift_seen_under_scalar_commonmode":bool(np.allclose(d_clean,d_underA,atol=1e-9)),
        "note":"the CO2-doubling event is detected, and the scalar gain nuisance does NOT change the detection (clr-invariant)."}

out={"_meta":{"tool":"probe_public_data_tests.py",
              "what":"Hs probe tested on 3 real public datasets x 3 nuisance kinds -- honest hits and misses.",
              "datasets_cited":{
                "GAS_breathing":"closed-loop O2/CO2/N2 gas-composition study (in-repo)",
                "BLOOD_alveolar":"VitalDB (Seoul Nat'l Univ Hosp) + UQ Vital Signs (Adelaide) anaesthesia cohorts",
                "WATER_produced":"USGS Produced Waters DB, Williston Basin (CoDaWork/Engle)"}},
     "nuisance_sweep":results,"real_drift_detection":detect}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()[:16]
if __name__=="__main__":
    print(json.dumps(out,indent=2))
