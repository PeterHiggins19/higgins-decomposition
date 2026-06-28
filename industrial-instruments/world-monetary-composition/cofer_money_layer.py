#!/usr/bin/env python3
"""
Hs reads the MONEY layer: IMF COFER -- currency composition of official FX reserves (the world's reserve money).
REAL, cited figures (IMF COFER, via Federal Reserve 'International Role of the US Dollar, 2025 ed.'; data 1995-2024):
  2024 allocated-reserve shares (%): USD 58, EUR 20, JPY 6, GBP 5, CNY 2, nontraditional(AUD+CAD+CHF+other) 9.
  USD share trajectory (%): 1995 ~58, 2001 72 (peak), 2014 ~65, 2022 58, 2024 58. CNY = 0 until 2015-Q2.
Deterministic; hash-receipted. Descriptive, not a forecast or advice. Source: IMF COFER (data.imf.org).
Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import hashlib, json, math
import numpy as np

COFER_2024={"USD":58,"EUR":20,"JPY":6,"GBP":5,"CNY":2,"Nontraditional (AUD/CAD/CHF/other)":9}
USD_TRAJ={1995:58,2001:72,2014:65,2022:58,2024:58}

def clr(p): L=np.log(p); return L-L.mean()

def main():
    names=list(COFER_2024); p=np.array([COFER_2024[n] for n in names],float); p=p/p.sum()
    H=-(p*np.log(p)).sum()
    out={
     "study":"IMF COFER -- currency composition of the world's official FX reserves (the money layer)",
     "data":"IMF COFER allocated-reserve shares; cited via Federal Reserve 2025 ed. (data 1995-2024). Real, cited.",
     "composition_2024_%":{n:round(float(p[i])*100,1) for i,n in enumerate(names)},
     "dominant_currency_arrow":names[int(np.argmax(clr(p)))],
     "effective_dimension_2024":round(math.exp(H),2),
     "concentration_HHI_2024":round(float((p**2).sum()),3),
     "USD_top_share_trajectory_% (cited anchors)":USD_TRAJ,
     "diversification_reading":"USD top share fell 72% (2001 peak) -> 58% (2024), lowest since ~1995: a falling top share = the reserve composition DIVERSIFYING (central banks added AUD, CAD, and others). Exact cited concentration metric; no estimate of the non-USD split needed.",
     "flow_regime":"LAMINAR -- reserves re-mix slowly over decades (USD basically unchanged 2022->2024; no shock reallocation even post-2022 sanctions).",
     "cross_study_contrast":"GDP layer (d03048c3): economy CONCENTRATING (eff-dim 7.3->6.2). COFER money layer: reserves DIVERSIFYING (USD 72->58). The world's economic WEIGHT concentrates while its reserve MONEY spreads out.",
     "honest_note":"Real cited IMF COFER anchors. Full quarterly all-currency series (2000Q1-) at data.imf.org/COFER for a deeper run. CNY only since 2015-Q2; shares are 'allocated reserves'. Descriptive, not advice."}
    out["content_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
