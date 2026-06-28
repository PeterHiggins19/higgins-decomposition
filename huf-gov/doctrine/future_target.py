#!/usr/bin/env python3
"""
"Help what can be helped" -- triage the repo's support for the forward goal by BOUNDARY ZONE, and find where it
can still be made to support the goal more fully. The boundary (three-stream division + export governance +
Peter's gate) defines what is ours to build (INSIDE) vs ready (AT) vs not ours (OUTSIDE).
Deterministic; receipted. Descriptive, not advice. Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import hashlib, json
import numpy as np

A = [  # (asset, stream, zone, support_completeness 0..1)
 ("principle / P-series (open science)",        "MATH",       "INSIDE", 0.90),
 ("conformance HS-EPS-1 / HS-GOLD-1",           "MATH",       "INSIDE", 0.90),
 ("method + language-agnostic spec",            "MATH",       "INSIDE", 0.95),
 ("EUV demo (receipted)",                       "INDUSTRY",   "INSIDE", 1.00),
 ("open-data composition demo (receipted)",     "INDUSTRY",   "INSIDE", 1.00),
 ("SMT / fiber / coherence demos (receipted)",  "INDUSTRY",   "INSIDE", 1.00),
 ("value / impact / world / fab analyses",      "GOVERNANCE", "INSIDE", 1.00),
 ("export + division governance",               "GOVERNANCE", "INSIDE", 1.00),
 ("the prepared offer + email + package",       "GOVERNANCE", "AT",     0.95),
 ("arXiv publication of the principle",         "MATH",       "AT",     0.60),
 ("a real-line / real-fab pilot (KIT)",         "INDUSTRY",   "AT",     0.50),
 ("government uptake / fab decision",           "GOVERNANCE", "OUTSIDE",0.00),
 ("measured deployment value (yield fraction)", "INDUSTRY",   "OUTSIDE",0.00),
 ("the world's adoption of the principle",      "MATH",       "OUTSIDE",0.00),
]

def main():
    names=[a[0] for a in A]; zone=np.array([a[2] for a in A]); comp=np.array([a[3] for a in A],float)
    zshare=lambda z:{"count":int((zone==z).sum()),
                     "mean_support_completeness":round(float(comp[zone==z].mean()),2) if (zone==z).any() else 0.0}
    helpable=[{"asset":names[i],"zone":zone[i],"completeness":comp[i],
               "action":"finish/polish" if zone[i]=="INSIDE" else "stage + hold at gate"}
              for i in range(len(A)) if zone[i] in ("INSIDE","AT") and comp[i] < 1.0]
    within=zone!="OUTSIDE"
    out={
     "goal":"the forward deployment future (Canada program / EUV / the standard-layer head start)",
     "boundary":"three-stream division + export governance + Peter's gate: build INSIDE fully, STAGE at-boundary, do NOT cross into OUTSIDE.",
     "by_zone":{"INSIDE (ours to build)":zshare("INSIDE"),"AT (stage + hold at gate)":zshare("AT"),
                "OUTSIDE (not ours; be ready)":zshare("OUTSIDE")},
     "support_within_boundary_completeness":round(float(comp[within].mean()),2),
     "help_what_can_be_helped":helpable,
     "not_ours_support_only_by_readiness":[names[i] for i in range(len(A)) if zone[i]=="OUTSIDE"],
     "reading":"The repo already supports the goal within the boundary. The only helpable items are a few INSIDE polish tasks and the AT-boundary readiness (arXiv-ready, a pilot-ready KIT). Everything OUTSIDE is NOT ours to force -- we help it only by being completely ready. Finish the inside, perfect the readiness, stop exactly at the gate.",
     "honest_note":"Completeness scores are judgment inputs (T3); the zoning + read are deterministic. Descriptive, not advice; Peter is the sole gate."
    }
    out["content_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
