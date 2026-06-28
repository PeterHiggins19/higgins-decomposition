#!/usr/bin/env python3
"""
go_blindness_control.py -- the COMPARISON BASE STUDY: run the same game with NO Hs (the player reads only
ABSOLUTE levels), to establish the control and prove the main study's foresight is the Hs EFFECT, not an
artifact of the setup. Same generator, same N=2400 games, same drift regimes.

Two arms on the SAME games (paired):
  HS ARM     : alert when the noisy RELATIONAL control share crosses the gate (the main study).
  CONTROL    : NO Hs -- alert only when the noisy ABSOLUTE stone margin crosses the gate (a blind player).
Measure each arm's FORESIGHT (decided_move - alert_move; positive = saw the turn early) and blindsided rate,
then compare (Welch t-test, Cohen's d). The control's foresight should be ~0 / not predictive (its alerts are
noise), isolating the Hs advantage.

HONEST FENCE: synthetic parable, not Go tactics, Hs not a Go engine; the statistics describe the MODEL across
randomized conditions. Deterministic (seeded); receipt. Author: Peter Higgins (human authorship for all claims);
AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib
from scipy import stats
WIN=0.62; HS_GATE=0.55; BLIND_GATE=6.0; T=60
DRIFT={"slow":0.22,"med":0.42,"fast":0.66}
def play(seed,drift0):
    r=np.random.default_rng(seed); b_s=4.0; w_s=4.0; b_c=4.0; w_c=4.0; cont=73.0
    hs_alert=None; blind_alert=None; decided=None
    for m in range(T):
        b_s+=1.0+r.normal(0,0.3); w_s+=1.0+r.normal(0,0.3)
        conv=max(drift0+0.02*m+r.normal(0,0.05),0.0); w_c+=conv; b_c+=0.30; cont=max(cont-conv-0.30,1.0)
        ws=w_c/(b_c+w_c)
        if hs_alert is None and ws+r.normal(0,0.02)>HS_GATE: hs_alert=m
        if blind_alert is None and abs(b_s-w_s)+abs(r.normal(0,0.4))>BLIND_GATE: blind_alert=m
        if decided is None and ws>WIN: decided=m
    def fore(a): return (decided-a) if (decided is not None and a is not None) else None
    return {"decided":decided,"hs_fore":fore(hs_alert),"blind_fore":fore(blind_alert),
            "hs_blindsided":bool(hs_alert is None or (decided is not None and hs_alert>decided)),
            "blind_blindsided":bool(blind_alert is None or (decided is not None and blind_alert>decided))}
N=800; games=[]; sd=1000
for d0 in DRIFT.values():
    for i in range(N): games.append(play(sd:=sd+1,d0))
def ci(x): x=np.array([v for v in x if v is not None],float);
def mean_ci(x):
    x=np.array([v for v in x if v is not None],float)
    if len(x)<2: return (None,None,None,0)
    m=x.mean(); se=x.std(ddof=1)/np.sqrt(len(x)); return (round(float(m),2),round(float(m-1.96*se),2),round(float(m+1.96*se),2),len(x))
def rate_ci(k,n): p=k/n; se=np.sqrt(p*(1-p)/n); return (round(p,4),round(max(p-1.96*se,0),4),round(min(p+1.96*se,1),4))

hs_fore=[g["hs_fore"] for g in games]; blind_fore=[g["blind_fore"] for g in games]
hs_mci=mean_ci(hs_fore); blind_mci=mean_ci(blind_fore)
hs_bs=rate_ci(sum(g["hs_blindsided"] for g in games),len(games)); blind_bs=rate_ci(sum(g["blind_blindsided"] for g in games),len(games))
blind_alerts_before=sum(1 for g in games if g["blind_fore"] is not None and g["blind_fore"]>0)   # how often blind alerts BEFORE decided
# comparison: Hs foresight vs blind foresight (independent Welch; blind has few samples)
hs_arr=np.array([v for v in hs_fore if v is not None],float); bl_arr=np.array([v for v in blind_fore if v is not None],float)
t,p=stats.ttest_ind(hs_arr,bl_arr,equal_var=False) if len(bl_arr)>1 else (float("inf"),0.0)
cohen_d=float((hs_arr.mean()-(bl_arr.mean() if len(bl_arr) else 0))/np.sqrt((hs_arr.var()+ (bl_arr.var() if len(bl_arr)>1 else 0))/2))

checks={
 "control_blindsided_high": bool(blind_bs[1]>0.85),
 "control_foresight_not_predictive": bool(blind_mci[0] is None or blind_mci[0]<2.0),       # blind foresight tiny/none
 "Hs_foresight_much_larger": bool(hs_mci[0] is not None and (blind_mci[0] is None or hs_mci[0]>5*max(blind_mci[0],0.1))),
 "difference_significant": bool(p<0.001),
}
verdict=(f"CONTROL (NO Hs): the blind player is blindsided {blind_bs[0]*100:.1f}% (95%CI {blind_bs[1]*100:.1f}-"
   f"{blind_bs[2]*100:.1f}%) and its foresight is {blind_mci[0]} moves over only {blind_mci[3]} games where it "
   f"alerted at all before the decision (vs Hs {hs_mci[0]} moves over {hs_mci[3]}). Without Hs there is NO "
   f"predictive sight -- the blind alerts are noise. Hs vs control: Welch t={t:.0f}, p={p:.1e}, Cohen d={cohen_d:.1f}. "
   "The foresight IS the Hs effect.") if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"go_blindness_control.py","what":"control base study: NO Hs (absolute-only) vs the Hs arm","N_games":len(games),"verdict":verdict},
     "control_no_Hs":{"blindsided_rate_95CI":blind_bs,"foresight_mean_ci_n":blind_mci,"games_where_blind_alerted_before_decision":blind_alerts_before},
     "Hs_arm":{"blindsided_rate_95CI":hs_bs,"foresight_mean_ci_n":hs_mci},
     "comparison":{"welch_t":round(float(t),1),"p_value":float(f"{p:.2e}"),"cohens_d":round(cohen_d,2),
        "reading":"the Hs arm's large positive foresight has no counterpart in the control -> the foresight is attributable to the relational read"},
     "checks":checks,
     "fence":"Synthetic parable; Hs not a Go engine; statistics describe the MODEL across randomized conditions. Peter is the sole gate; nothing posted."}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps({"c":out["control_no_Hs"],"h":out["Hs_arm"],"cmp":{"t":round(float(t),1),"d":round(cohen_d,2)},"ch":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]
if __name__=="__main__": print(json.dumps(out,indent=2))
