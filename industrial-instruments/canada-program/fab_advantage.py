#!/usr/bin/env python3
"""
Does a Canadian fab "powered by Hs" have a durable advantage, or does publishing the science erase it?
Read a fab's COMPETITIVE ADVANTAGE as a composition over its sources, split into disclosure-proof (copy-resistant:
physical/tacit, NOT made public by publishing the method) vs disclosable (the published method itself). Then
locate Hs honestly: a small published slice + an accelerant of the PRIVATE operational-learning slice.
Shares are honest judgment inputs (T3); the read is deterministic + receipted. Not financial/strategic advice.
Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import hashlib, json
import numpy as np

SRC = [  # (source, weight 0-10, copy_resistant?, hs_role)
 ("capital & physical capacity (the fab, capex)",        8, True,  None),
 ("tacit process know-how / accumulated yield-learning", 9, True,  None),
 ("talent & local ecosystem",                            8, True,  None),
 ("location / sovereignty / policy access",              6, True,  None),
 ("supply-chain relationships",                          6, True,  None),
 ("early operational-learning lead (Hs-accelerated, tacit)", 7, True, "accelerant"),
 ("the published method (Hs principle)",                 2, False, "published"),
]

def main():
    names=[s[0] for s in SRC]; w=np.array([s[1] for s in SRC],float); p=w/w.sum()
    resist=np.array([s[2] for s in SRC])
    disclosable=float(p[~resist].sum()); disclosure_proof=float(p[resist].sum())
    hs_pub=float(p[[i for i,s in enumerate(SRC) if s[3]=="published"]].sum())
    hs_learn=float(p[[i for i,s in enumerate(SRC) if s[3]=="accelerant"]].sum())
    out={
     "question":"Canadian-built fab, outside-supported, 'powered by Hs' -- durable advantage, or published-away?",
     "advantage_shares_%":{names[i]:round(float(p[i])*100,1) for i in np.argsort(-p)},
     "disclosable_share_% (removed by publishing the method)": round(disclosable*100,1),
     "disclosure_proof_share_% (survives publication; copy-resistant)": round(disclosure_proof*100,1),
     "Hs_role":{"as_published_method_%":round(hs_pub*100,1),
                "as_accelerant_of_PRIVATE_operational_learning_%":round(hs_learn*100,1),
                "reading":"Hs helps the fab mostly by ACCELERATING private, tacit operational learning -- NOT by keeping a method secret. The method is a small (~%.0f%%), non-exclusive slice; publishing it removes only that slice." % (hs_pub*100)},
     "answer":"The fab's moat is ~%.0f%% copy-RESISTANT (capital, tacit yield-learning, talent, ecosystem, location) -- none of which publishing the method makes public. Publishing erodes only ~%.0f%%. So it does NOT 'become public so fast there is no advantage': the advantage that survives disclosure is exactly the part you cannot write down." % (disclosure_proof*100, disclosable*100),
     "scope_note":"Realistic Canadian fab = SPECIALTY (compound-semi / photonics III-V / advanced packaging), already underway (CPFC spin-off, $350M, May 2026) -- NOT a $20-40B leading-edge EUV logic megafab. Hs = a thin quality/yield-learning accelerant, not the fab's core moat (honest weighting).",
     "honest_note":"Shares are judgment inputs (T3); the compositional split is deterministic. Not financial/strategic advice; descriptive."}
    out["content_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
