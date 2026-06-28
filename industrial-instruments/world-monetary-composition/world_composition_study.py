#!/usr/bin/env python3
"""
Hs reads the COMPOSITION of the world's economic weight over time -- the backing of the monetary systems.
REAL public data: World Bank GDP (current US$), NY.GDP.MKTP.CD, fetched 2026; 10 largest economies, 2009-2023.
Deterministic; hash-receipted. Descriptive (what the composition IS doing), not a forecast or advice.
Author: Peter Higgins; AI-assisted per HUF-STD-001. Source: https://api.worldbank.org/v2/ (World Bank Open Data).
"""
import hashlib, json, math
import numpy as np

YEARS=list(range(2009,2024))
G={  # GDP current US$ (trillions), real World Bank values
"United States":[14.478064934,15.048964444,15.599728123,16.25397223,16.843190993,17.550680174,18.206020741,18.695110842,19.477336549,20.533057312,21.380976119,21.060473613,23.31508056,25.604848908,27.292170793],
"China":[5.189577095,6.192564874,7.671757208,8.673664713,9.743124247,10.674533168,11.280814787,11.456024085,12.537559062,14.147765773,14.560167101,14.996414167,18.20169872,18.316765022,18.270356655],
"Japan":[5.289493118,5.759071769,6.233147172,6.272362996,5.212328181,4.896994405,4.444930652,5.003677628,4.930837369,5.040880939,5.117993853,5.054068005,5.039148169,4.262463318,4.213167238],
"Germany":[3.478545517,3.46709377,3.823575804,3.596483233,3.807023797,3.964870736,3.425099579,3.536787895,3.765351626,4.055433215,3.959894794,3.941398957,4.355251953,4.201021706,4.562207532],
"India":[1.341888017,1.675615519,1.82305183,1.82763759,1.856721508,2.039126479,2.10358836,2.294796886,2.651474263,2.702929642,2.835606257,2.674851579,3.167270623,3.346107288,3.638489096],
"United Kingdom":[2.429358155,2.496740681,2.675590034,2.719715962,2.796908333,3.085362169,2.94557989,2.706807607,2.699118388,2.89702801,2.87571008,2.724001478,3.194559189,3.18124435,3.420796654],
"France":[2.700075883,2.646230028,2.870408554,2.683007096,2.816077608,2.861236113,2.442483453,2.47040762,2.588868323,2.781576321,2.722793515,2.647926055,2.966433692,2.794788137,3.056250648],
"Italy":[2.209484319,2.144936255,2.30697402,2.097929495,2.153225582,2.173255508,1.845428049,1.887111188,1.970720905,2.099435266,2.019606797,1.907481094,2.179207774,2.10406763,2.316727999],
"Brazil":[1.666996294,2.208838108,2.616156607,2.465228294,2.472819362,2.456043766,1.802211999,1.795693266,2.063514689,1.916933708,1.873288159,1.476107292,1.670647464,1.951923832,2.19113187],
"Canada":[1.374625142,1.617343367,1.79332663,1.828366482,1.846597422,1.80574988,1.556508816,1.527994742,1.649265644,1.725329193,1.743725184,1.65568473,2.022378748,2.19041108,2.17333967],
}
BLOC={"North America":["United States","Canada"],"Europe":["Germany","United Kingdom","France","Italy"],
      "Asia":["China","Japan","India"],"Latin America":["Brazil"]}

def clr(p): L=np.log(p); return L-L.mean(axis=-1,keepdims=True)

def main():
    names=list(G); M=np.array([G[n] for n in names]).T
    P=M/M.sum(axis=1,keepdims=True); C=clr(P); V=np.diff(C,axis=0)
    eff=[float(math.exp(-(P[t]*np.log(P[t])).sum())) for t in range(len(YEARS))]
    helm=[names[int(np.argmax(np.abs(V[t])))] for t in range(len(V))]
    mom=[names[int(np.argmax(np.abs(V[t])*P[t+1]))] for t in range(len(V))]
    def tort(a,b):
        seg=C[a:b+1]; steps=np.linalg.norm(np.diff(seg,axis=0),axis=1).sum()
        return float(steps/max(np.linalg.norm(seg[-1]-seg[0]),1e-9))
    turb={f"{YEARS[a]}-{YEARS[a+3]}":round(tort(a,a+3),2) for a in range(0,len(YEARS)-3,1)}
    shares={n:[round(float(P[0][i])*100,1),round(float(P[-1][i])*100,1)] for i,n in enumerate(names)}
    Bn=list(BLOC); BM=np.array([[sum(G[c][t] for c in BLOC[b]) for b in Bn] for t in range(len(YEARS))])
    BP=BM/BM.sum(axis=1,keepdims=True)
    bloc_shares={b:[round(float(BP[0][j])*100,1),round(float(BP[-1][j])*100,1)] for j,b in enumerate(Bn)}
    bloc_eff=[round(float(math.exp(-(BP[t]*np.log(BP[t])).sum())),2) for t in range(len(YEARS))]
    out={"study":"Hs reads the composition of the world's economic weight over time",
         "data":"World Bank GDP current US$ (NY.GDP.MKTP.CD), 10 largest economies, 2009-2023 (real, cited)",
         "level1_country_shares_%_2009_vs_2023":shares,
         "arrow_helmsman_by_step":dict(zip([f"{YEARS[t]}->{YEARS[t+1]}" for t in range(len(helm))],helm)),
         "momentum_dominant_by_step":dict(zip([f"{YEARS[t]}->{YEARS[t+1]}" for t in range(len(mom))],mom)),
         "effective_dimension_per_year":dict(zip(YEARS,[round(e,2) for e in eff])),
         "flow_regime_tortuosity_3yr (1=laminar,>1 turbulent)":turb,
         "level2_bloc_shares_%_2009_vs_2023":bloc_shares,
         "level2_bloc_effective_dimension_per_year":dict(zip(YEARS,bloc_eff)),
         "honest_note":"Real public data; reads are deterministic. GDP in current US$ mixes real growth + price + EXCHANGE-RATE moves (e.g. Japan's fall is partly yen depreciation). Descriptive, not a forecast or advice."}
    out["content_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
