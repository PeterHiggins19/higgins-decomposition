#!/usr/bin/env python3
"""
Hs reads the WORLD COMPOSITION of the advanced-semiconductor field and locates Canada; then a deterministic
EARLY-ADOPTION MOMENTUM model. Region shares are illustrative, mixed-metric PUBLIC figures (T3 inputs); the
compositional read + the model are deterministic. Descriptive, not a forecast. Not financial/political advice.
Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import hashlib, json, math
import numpy as np

WORLD = {  # illustrative public 2025 shares, blended metric (flagged T3)
 "Asia-Pacific (mfg mass: China/TW/SK/JP)": 53.0,
 "United States (value/design lead)":       22.0,
 "Europe (incl. NL/ASML)":                  12.7,
 "Rest of world":                           12.1,
 "Canada":                                   0.2,
}

def read_comp(counts):
    items=list(counts.items()); n=np.array([c for _,c in items],float); p=n/n.sum()
    H=-(p*np.log(p)).sum(); eff=math.exp(H); hhi=float((p**2).sum())
    order=np.argsort(-p); clr=np.log(p)-np.log(p).mean()
    return {"shares_%":{items[i][0]:round(float(p[i])*100,2) for i in order},
            "arrow":items[int(np.argmax(clr))][0],"effective_dimension":round(eff,2),
            "concentration_HHI":round(hhi,3),
            "canada_share_%":round(float(p[[k for k,_ in items].index("Canada")])*100,3)}

def logistic(t,t0,k=0.9,cap=1.0): return cap/(1.0+math.exp(-k*(t-t0)))

def main():
    world=read_comp(WORLD)
    years=list(range(0,13)); vol=world["canada_share_%"]/100.0
    influence=lambda t0:[round(vol+0.30*logistic(t,t0),3) for t in years]
    early=influence(2.0); late=influence(7.0)
    out={
     "world_field_read":world,
     "canada_position":"By MASS Canada is in the deep tail (~0.2% of global semiconductor revenue; arrow = Asia-Pacific manufacturing, value concentrated in US/TW/SK/NL). By SPECIALTY Canada sits in the leading cluster: compound semiconductors (CPFC = N. America's only end-to-end pure-play), photonics, advanced packaging (Bromont/C2MI), AI/quantum. Quality-not-quantity. Note: only G7 nation without a national semiconductor strategy (a gap = an opening).",
     "momentum_model":{
       "premise":"Canada cannot win on manufacturing VOLUME (mass is in Asia). It CAN move early on an auditable, deterministic monitoring/quality STANDARD -- influence disproportionate to volume.",
       "canada_volume_share":round(vol,4),
       "early_adopter_influence_by_year":early,"late_adopter_influence_by_year":late,
       "early_vs_late_gap_at_year12":round(early[12]-late[12],3),
       "compounding_lead_area_over_12yr":round(sum(e-l for e,l in zip(early,late)),2),
       "reading":"Same tiny volume share; the early mover compounds standard-layer influence sooner and holds a persistent lead (the area between the curves). A head start on the STANDARD, not the FAB, is how a small player gains ongoing momentum."
     },
     "honest_note":"Region shares are illustrative mixed-metric public figures (T3); read + curves deterministic given inputs but the model is ILLUSTRATIVE, not a forecast. Standard-layer weight (0.30) and timing are assumptions. Descriptive; the government decides meaning. NOT financial/political advice."
    }
    out["content_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
