#!/usr/bin/env python3
"""
kardashev_projection.py -- STAGE ONE of the game: use Hs to "play Civilization" up the Compositional
Governance Scale (CGS), the treasure found in the HUF vaults (science/methodology/COMPOSITIONAL_GOVERNANCE_SCALE.md,
formerly CMSI). The regimes:

   CGS = log10(GDoF),   GDoF_domain = (carriers-1) * sites * diagnostics * temporal_scales,   GDoF = sum over domains

   CGS-1  GDoF>=1e1   Instrument Proof            (one system)
   CGS-2  GDoF>=1e2   Cross-Domain Validation
   CGS-3  GDoF>=1e4   Operational Deployment
   CGS-4  GDoF>=1e6   Network Governance          ( ~ Kardashev I: govern the full complexity of the home domain )
   CGS-5  GDoF>=1e8   Universal Compositional Std  ( ~ Kardashev V: governance of COMPLEXITY ITSELF -- the couplings )

THE GAME'S ONE RESULT (and it is on-thesis): a Civilization that governs each domain separately can climb to
CGS-4 (it governs SYSTEMS) but CANNOT reach CGS-5, because CGS-5 is governance of the COUPLINGS between domains
-- and a coupling is a relation, read only by the compositional (Hs) view. So Hs is the bridge from governing
systems to governing complexity. We test that by running the climb WITH and WITHOUT the Hs coupling layer.

HONEST SCOPE (loud, because this is a fantasy/game): the CGS scale is the source's OWN n=1 OPINION -- "the
levels are designed, not derived" (thresholds chosen for structural meaning). The "Kardashev V" mapping is an
ANALOGY borrowed from the archived unity-vcore work, NOT a physics claim about harnessing stars. This is an
illustrative simulation of a designed governance scale, deterministic so it is inspectable; receipt over the
ladder. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26.
Peter is the sole gate; nothing posted.
"""
import json, hashlib, math

def gdof_domain(carriers, sites, diagnostics, temporal):
    return (carriers - 1) * sites * diagnostics * temporal

REGIMES = [  # (label, GDoF threshold, kardashev analogy)
 ("CGS-1 Instrument Proof",        1e1, "-"),
 ("CGS-2 Cross-Domain Validation", 1e2, "-"),
 ("CGS-3 Operational Deployment",  1e4, "-"),
 ("CGS-4 Network Governance",      1e6, "~ Kardashev I (govern the home domain)"),
 ("CGS-5 Universal Compositional", 1e8, "~ Kardashev V (govern complexity itself)"),
]
def regime_of(gdof):
    lab = "CGS-0 (sub-instrument)"
    for label, thr, _ in REGIMES:
        if gdof >= thr: lab = label
    return lab

# the Civilization's climb: each epoch grows the four multiplicative dimensions across more domains.
# (domains, carriers, sites, diagnostics, temporal)  -- a designed growth schedule
EPOCHS = [
 ("E1 one meter, one country",   1,  9,     3, 2, 1),   # = HUF today: (9-1)*3*2*1 = 48
 ("E2 two domains coupled",      2, 10,     8, 3, 2),
 ("E3 operational, three domains",3, 12,    40, 4, 4),
 ("E4 planetary network",        5, 15,   500, 5, 6),
 ("E5 planet at fine resolution",5, 20,  8000, 6, 8),
]

def couplings(n_domains): return n_domains*(n_domains-1)//2   # interfaces between domains (the relations)

def run(with_hs):
    ladder=[]
    for name, D, carr, sites, diag, temporal in EPOCHS:
        per = gdof_domain(carr, sites, diag, temporal)
        domain_gdof = per * D
        # Hs adds governance of the COUPLINGS: each domain-pair interface, read relationally, governed as richly
        coupling_gdof = couplings(D) * per if with_hs else 0
        gdof = domain_gdof + coupling_gdof
        cgs = round(math.log10(gdof), 3)
        ladder.append({"epoch":name, "domains":D, "couplings_governed":couplings(D) if with_hs else 0,
                       "GDoF":gdof, "CGS":cgs, "regime":regime_of(gdof)})
    return ladder

with_hs    = run(True)
without_hs = run(False)
top_with    = with_hs[-1]
top_without = without_hs[-1]

checks = {
 "cgs_equals_log10_gdof": all(c["CGS"]==round(math.log10(c["GDoF"]),3) for c in with_hs),
 "E1_matches_HUF_48": with_hs[0]["GDoF"]==48 and with_hs[0]["CGS"]==round(math.log10(48),3),
 "climb_is_monotonic": all(with_hs[i]["GDoF"]<with_hs[i+1]["GDoF"] for i in range(len(with_hs)-1)),
 "WITHOUT_Hs_caps_below_CGS5": top_without["GDoF"] < 1e8,           # governs systems, not complexity
 "WITH_Hs_reaches_CGS5": top_with["GDoF"] >= 1e8,                   # the bridge to Kardashev V
}
verdict = ("HS IS THE BRIDGE: without the coupling layer the Civilization caps at "
           f"{top_without['regime']} (CGS {top_without['CGS']}); with Hs it reaches {top_with['regime']} "
           f"(CGS {top_with['CGS']})") if all(checks.values()) else "SIM CHECK FAILED"

out = {"_meta":{"tool":"kardashev_projection.py",
                "what":"Stage-one game: climb the CGS regimes to Kardashev V; Hs governs the couplings",
                "verdict":verdict},
       "regimes": [{"label":l,"GDoF_threshold":t,"kardashev":k} for l,t,k in REGIMES],
       "climb_with_Hs": with_hs,
       "climb_without_Hs": without_hs,
       "the_gap": {"top_without_Hs":{"regime":top_without["regime"],"CGS":top_without["CGS"],"GDoF":top_without["GDoF"]},
                   "top_with_Hs":{"regime":top_with["regime"],"CGS":top_with["CGS"],"GDoF":top_with["GDoF"]},
                   "meaning":"the coupling GDoF Hs adds is exactly what crosses the CGS-5 / Kardashev-V gate"},
       "checks": checks,
       "fence":("CGS is the source's OWN n=1 OPINION (levels designed, not derived); 'Kardashev V' is an "
                "ANALOGY, not a physics/energy claim. Illustrative deterministic simulation of a designed scale. "
                "Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(
    json.dumps({"with":with_hs,"without":without_hs,"checks":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]

if __name__=="__main__":
    print(json.dumps(out,indent=2))
