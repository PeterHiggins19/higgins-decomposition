#!/usr/bin/env python3
"""
max_power_hs.py -- the smallest component a system can SUPPORT (max-power Hs).

"Know the knowable" has a hard edge: you can only resolve a component if BOTH
  (1) your DATA can tell it apart from its neighbours (statistical ceiling), and
  (2) your COMPUTE can carry the relational web at that grain (compute ceiling).
The finest supportable grain is the MIN of the two ceilings. Component-web density w
(relations per component) trades them: a denser web carries more information per part but
costs more samples AND more compute. Max-power Hs operates exactly where the two ceilings
meet -- push past either and the read is no longer supported (it is guessed, not known).

HONEST FENCE: this is a DESIGN RELATION (T2), not a measured law. The scaling forms are the
standard ones -- relational estimation needs N >~ (relations) so D_stat ~ N/(beta*w); the
relational read costs ~D*w so D_comp solves C ~ kappa*D*w -- but the CONSTANTS are illustrative.
The structural claim (resolution = min(data ceiling, compute ceiling); web density sets the grain,
data-vs-compute sets which ceiling binds) is the result; the numbers are scenario numbers.
Consistent with the CMP finite-sample boundary D*(N). Deterministic; SHA-256 receipt.
Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001.
2026-06-25. Peter is the sole gate; nothing posted.
"""
import math, json, hashlib

def ceilings(N, C, w, beta=2.0, kappa=1.0):
    """N = samples available; C = compute budget (relative ops); w = web density (relations per component).
    Returns the statistical ceiling, the compute ceiling, the binding one, and the finest supportable share."""
    # statistical ceiling: to estimate ~ w relational stats per part reliably you need N >~ beta * D * w
    #   -> D_stat = N / (beta * w)   (more relations per part -> fewer parts resolvable from the same N)
    D_stat = N / (beta * w)
    # compute ceiling: the relational read costs ~ kappa * D * w ops -> D_comp = C / (kappa * w)
    D_comp = C / (kappa * w)
    D_max = min(D_stat, D_comp)
    binding = "statistical (need more DATA)" if D_stat < D_comp else "compute (need more POWER)"
    if abs(D_stat-D_comp)/max(D_stat,D_comp) < 0.05: binding = "balanced (at the meeting point -- MAX POWER)"
    finest_share = 1.0 / D_max if D_max>0 else float('inf')   # smallest evenly-split component share
    return {"web_density_w":w,"D_stat":round(D_stat,2),"D_comp":round(D_comp,2),
            "D_max_supportable":round(D_max,2),"binding_ceiling":binding,
            "finest_component_share":float(f"{finest_share:.3e}")}

if __name__=="__main__":
    scenarios=[
        ("data-rich, compute-poor",  {"N":1_000_000, "C":5_000,    "w":4}),
        ("compute-rich, data-poor",  {"N":2_000,     "C":2_000_000,"w":4}),
        ("balanced (max-power)",     {"N":40_000,    "C":20_000,   "w":4}),
        ("dense web (w=20)",         {"N":40_000,    "C":20_000,   "w":20}),
        ("sparse web (w=1)",         {"N":40_000,    "C":20_000,   "w":1}),
    ]
    runs=[]
    for label,p in scenarios:
        r=ceilings(**p); r["scenario"]=label; r["inputs"]=p; runs.append(r)
    out={"_meta":{"tool":"max_power_hs.py",
                  "what":"the finest supportable component = min(statistical ceiling, compute ceiling); web density sets the grain; data-vs-compute sets which ceiling binds; max-power Hs sits at the meeting point.",
                  "fence":"DESIGN RELATION (T2); scaling forms standard, constants illustrative; the structural claim is the result, not the numbers."},
         "runs":runs}
    blob=json.dumps(out,sort_keys=True,default=str).encode()
    out["_meta"]["receipt_sha256"]=hashlib.sha256(blob).hexdigest()[:16]
    print(json.dumps(out,indent=2))
