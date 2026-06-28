#!/usr/bin/env python3
"""
go_blindness_study.py -- the Go Hs-vs-blind parable, turned into a STATISTICAL study: play the game many times
with randomized noise across drift-speed regimes, and measure the consequence with confidence intervals and an
ANOVA. Evidence, not anecdote -- the engaging companion to P1.

Each game (a Go-framed compositional contest, NOT Go tactics): both place stones at the same rate (with mean-zero
noise, so the absolute stone-margin random-walks near 0 -- the board looks even); White converts contested ->
control at a regime-dependent PROPORTIONAL rate. A BLIND decision-maker reads the noisy ABSOLUTE margin; an Hs
decision-maker reads the noisy RELATIONAL control share. The game is DECIDED when true control crosses WIN.
  blindsided  = the blind player did NOT alert at/before the decided move
  Hs foresight = decided_move - Hs_alert_move (how many moves early Hs saw the turn)

Design: 3 drift regimes (slow/med/fast) x N games each. Reported: blindsided rate (binomial 95% CI), Hs
foresight (mean, 95% t-CI), absolute margin at the decided move; ONE-WAY ANOVA of foresight across regimes (F, p)
-- the interpretable effect: faster drift decides sooner, so foresight shrinks.

HONEST FENCE: Hs is NOT a Go engine; this is a controlled SYNTHETIC parable. The statistics are about the
MODEL's behaviour across randomized conditions (robustness of the ratio-blindness cost), not a claim about real
Go or a universal law. Deterministic (seeded); receipt. Author: Peter Higgins (human authorship for all claims);
AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib
from scipy import stats

WIN=0.62; HS_GATE=0.55; BLIND_GATE=6.0; T=60
DRIFT={"slow":0.22,"med":0.42,"fast":0.66}
def play(seed, drift0):
    r=np.random.default_rng(seed)
    b_s=4.0; w_s=4.0; b_c=4.0; w_c=4.0; cont=73.0
    hs_alert=None; blind_alert=None; decided=None; margin_at_dec=None
    for m in range(T):
        b_s+=1.0+r.normal(0,0.3); w_s+=1.0+r.normal(0,0.3)          # even placement + mean-zero noise
        conv=max(drift0+0.02*m+r.normal(0,0.05),0.0)
        w_c+=conv; b_c+=0.30; cont=max(cont-conv-0.30,1.0)
        true_ws=w_c/(b_c+w_c)
        hs_read=true_ws+r.normal(0,0.02)                            # noisy relational read
        blind_read=abs(b_s-w_s)+abs(r.normal(0,0.4))               # noisy absolute read
        if hs_alert is None and hs_read>HS_GATE: hs_alert=m
        if blind_alert is None and blind_read>BLIND_GATE: blind_alert=m
        if decided is None and true_ws>WIN: decided=m; margin_at_dec=abs(b_s-w_s)
    blindsided = (blind_alert is None) or (decided is not None and blind_alert>decided)
    foresight = (decided-hs_alert) if (decided is not None and hs_alert is not None) else None
    return {"decided":decided,"hs_alert":hs_alert,"blindsided":bool(blindsided),"foresight":foresight,"margin_at_decided":margin_at_dec}

N=800; rows={k:[] for k in DRIFT}; sd=1000
for lvl,d0 in DRIFT.items():
    for i in range(N): rows[lvl].append(play(sd:=sd+1,d0))
allr=[g for lvl in rows for g in rows[lvl]]
def ci95_mean(x): x=np.array(x,float); m=x.mean(); se=x.std(ddof=1)/np.sqrt(len(x)); return round(float(m),2),round(float(m-1.96*se),2),round(float(m+1.96*se),2)
def ci95_rate(k,n): p=k/n; se=np.sqrt(p*(1-p)/n); return round(p,4),round(max(p-1.96*se,0),4),round(min(p+1.96*se,1),4)

decided_games=[g for g in allr if g["decided"] is not None and g["hs_alert"] is not None]
blind_k=sum(g["blindsided"] for g in allr); blind_rate=ci95_rate(blind_k,len(allr))
foresight_all=[g["foresight"] for g in decided_games]; fore_ci=ci95_mean(foresight_all)
margin_dec=ci95_mean([g["margin_at_decided"] for g in allr if g["margin_at_decided"] is not None])
per_level={lvl:{"blindsided_rate":ci95_rate(sum(g["blindsided"] for g in rows[lvl]),len(rows[lvl])),
                "foresight_mean_ci":ci95_mean([g["foresight"] for g in rows[lvl] if g["foresight"] is not None])} for lvl in DRIFT}
# ONE-WAY ANOVA of foresight across drift regimes
groups=[[g["foresight"] for g in rows[lvl] if g["foresight"] is not None] for lvl in DRIFT]
F,p=stats.f_oneway(*groups)

checks={
 "blindsided_rate_high": bool(blind_rate[1]>0.85),                 # lower CI bound > 0.85
 "Hs_foresight_significantly_positive": bool(fore_ci[1]>0),        # CI lower bound > 0
 "board_even_at_decision": bool(margin_dec[2]<BLIND_GATE),         # margin upper CI < blind threshold
 "anova_significant": bool(p<0.05),                                # drift regime affects foresight
}
verdict=(f"MAJOR STUDY (N={len(allr)}): the blind player is blindsided in {blind_rate[0]*100:.1f}% of games "
   f"(95%CI {blind_rate[1]*100:.1f}-{blind_rate[2]*100:.1f}%); the Hs player's foresight is {fore_ci[0]} moves "
   f"(95%CI {fore_ci[1]}-{fore_ci[2]}); the board sits at margin {margin_dec[0]} (even, < {BLIND_GATE}) when the "
   f"game is decided; one-way ANOVA across drift regimes F={F:.1f}, p={p:.2e} (faster drift -> less foresight). "
   "Ratio-blindness loses, robustly and significantly.") if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"go_blindness_study.py","what":"statistical study: Hs vs blind in a proportional contest","N_games":len(allr),"verdict":verdict},
     "blindsided_rate_95CI":blind_rate,"Hs_foresight_moves_95CI":fore_ci,"absolute_margin_at_decision_95CI":margin_dec,
     "per_drift_regime":per_level,"anova_foresight_by_regime":{"F":round(float(F),2),"p_value":float(f"{p:.3e}"),"groups":list(DRIFT)},
     "checks":checks,
     "fence":("Hs is NOT a Go engine; controlled SYNTHETIC parable. The statistics describe the MODEL's behaviour "
        "across randomized conditions (robustness of the ratio-blindness cost), not real Go or a universal law. "
        "Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(
    {"br":blind_rate,"fc":fore_ci,"md":margin_dec,"pl":per_level,"F":round(float(F),2),"c":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]
if __name__=="__main__": print(json.dumps(out,indent=2))
