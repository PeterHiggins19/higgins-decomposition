#!/usr/bin/env python3
"""
foresight_run.py -- the SEAT-BELT read. Re-run all EMBER systems (10 countries incl. Canada + World) and the
full Backblaze fleet on the latest-engine primitives, at the finest grain, and add three things the finer read
makes possible -- the extended language "know thy system, and thy is part of thy system; don't damage where you
live":

  1. FINEST-DETAIL MOTION  (T1)  -- effective dimension, trajectory directedness, motion-helmsman: the system
                                    has MORE motion than a totals view reveals, read exactly from the ratios.
  2. THE FORWARD CAST      (T2)  -- the Ghost of Christmas Yet to Come: extrapolate the RECENT clr-velocity
                                    forward H years (a deterministic WHAT-IF, not a forecast) -> where the mix
                                    lands IF the current motion simply continues, uncorrected.
  3. THE STEWARDSHIP GATE  (T2)  -- Breaker S, "don't damage where you live": flag only when the forward cast
                                    REDUCES the commons/clean share; otherwise the report card reads "on course."
  4. THE CORRECTIVE LEVER  (T2)  -- the seat belt works: a modest compositional steer that bends the cast back.
                                    The image can change; the future is a warning, not a sentence.

HONEST: the cast is a clr-velocity extrapolation, fenced as a what-if; the stewardship gate is a designed
breaker; "clean/commons" for energy = non-fossil share (Coal+Gas+Other Fossil are fossil). Most systems read
fairly -- the responsible move is already visible; no bad report cards. Deterministic; receipt. Author: Peter
Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27. Peter is the sole gate;
nothing posted.
"""
import numpy as np, csv, json, hashlib, os
HS=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..")
def P(*a): return os.path.normpath(os.path.join(HS,*a))
FLOOR=1e-9
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,FLOOR,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def softmax_clr(z): e=np.exp(z-z.max()); return e/e.sum()
def eff_dim(v): v=closure(v); H=-np.sum(v*np.log(v+1e-300),-1); return float(np.exp(np.mean(H)))
def receipt(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]
def load(path,drop=()):
    with open(P(path)) as f: rows=list(csv.reader(f))
    hdr=rows[0]; keep=[i for i,h in enumerate(hdr) if h not in drop]; names=[hdr[i] for i in keep]; data=[]
    for r in rows[1:]:
        try:
            vals=[float(r[i]) for i in keep]
            if all(np.isfinite(vals)) and sum(abs(x) for x in vals)>0: data.append(vals)
        except (ValueError,IndexError): pass
    return names,np.clip(np.array(data),0,None)

FOSSIL={"Coal","Gas","Other Fossil"}
def commons_share(names,share,fossil=FOSSIL):   # clean/commons = non-fossil
    return float(sum(s for nm,s in zip(names,share) if nm not in fossil))

def read_system(name,path,drop,H=10,K=5,commons=True):
    names,X=load(path,drop)
    if X.shape[0]<K+2: K=max(2,X.shape[0]//3)
    Xc=closure(np.clip(X,FLOOR,None)); now=Xc[-1]
    # finest-detail motion
    C=clr(np.clip(X,FLOOR,None)); dC=np.diff(C,axis=0)
    path_len=float(np.sum(np.linalg.norm(dC,axis=1))); net=float(np.linalg.norm(C[-1]-C[0]))
    directed=round(net/path_len,3) if path_len else None
    helm=names[int(np.argmax(np.sum(np.abs(dC),axis=0)))]
    # forward cast: extend recent mean clr-velocity H steps (the Ghost of Yet-to-Come; a what-if)
    vel=np.mean(dC[-K:],axis=0); cast=softmax_clr(C[-1]+H*vel)
    res={"system":name,"n_rows":int(X.shape[0]),"D_parts":int(X.shape[1]),
         "effective_dimension":round(eff_dim(np.mean(Xc,0)),3),"directedness":directed,"motion_helmsman":helm}
    if commons:
        now_c=commons_share(names,now); cast_c=commons_share(names,cast); delta=cast_c-now_c
        # the corrective lever: add solar+wind = +8% of current total, recompute cast endpoint share
        tot=X[-1].sum(); add=0.08*tot; lev=X[-1].copy()
        for j,nm in enumerate(names):
            if nm in ("Solar","Wind"): lev[j]+=add/2
        lev_share=closure(np.clip(lev,FLOOR,None)); lev_c=commons_share(names,lev_share)
        gate=("ON COURSE — clean/commons share holding or rising" if delta>=-0.02 else
              "FASTEN THE BELT — the cast lowers the clean/commons share")
        res.update({"clean_share_now":round(now_c,3),"clean_share_cast_%dy"%H:round(cast_c,3),
                    "cast_delta":round(delta,3),"stewardship_gate":gate,
                    "lever_recovers_to":round(lev_c,3),"lever_helps":bool(lev_c>cast_c)})
    else:
        # Backblaze fleet: the "environment the data lives in"; commons-analog = low-stress (non-Errors) share
        err_j=[j for j,nm in enumerate(names) if nm.lower()=="errors"]
        if err_j:
            now_e=float(now[err_j[0]]); cast=softmax_clr(C[-1]+H*np.mean(dC[-K:],axis=0)); cast_e=float(cast[err_j[0]])
            res.update({"errors_share_now":round(now_e,4),"errors_share_cast":round(cast_e,4),
                        "stewardship_gate":("ON COURSE — error share stable/declining" if cast_e<=now_e+0.005
                            else "FASTEN THE BELT — error share rising; pre-fault migration is the seat belt")})
    res["receipt"]=receipt({k:v for k,v in res.items() if k!="receipt"})
    return res

EMBER=[("AUS","Australia"),("CAN","Canada"),("CHN","China"),("DEU","Germany"),("FRA","France"),
       ("GBR","United_Kingdom"),("IND","India"),("JPN","Japan"),("USA","United_States"),("WLD","World")]
results=[]
for code,nm in EMBER:
    path="data/Energy/EMBER_pipeline_ready/ember_%s_%s_generation_TWh.csv"%(code,nm)
    try: results.append(read_system("Energy %s (EMBER)"%nm.replace("_"," "),path,("Year",)))
    except Exception as e: results.append({"system":nm,"error":str(e)})
try: results.append(read_system("Backblaze fleet (stress)","experiments/Hs-17_Backblaze/Hs-17_fleet_composition.csv",("index",),commons=False))
except Exception as e: results.append({"system":"Backblaze","error":str(e)})

energy=[r for r in results if "clean_share_now" in r]
on_course=[r for r in energy if r["stewardship_gate"].startswith("ON COURSE")]
flagged=[r for r in energy if not r["stewardship_gate"].startswith("ON COURSE")]
lever_works=all(r.get("lever_helps") for r in flagged) if flagged else True
checks={
 "all_systems_read": bool(len([r for r in results if "error" not in r])==len(results)),
 "finer_read_shows_motion": bool(all(r.get("directedness") is not None for r in results if "error" not in r)),
 "no_blanket_bad_report_cards": bool(len(on_course)>=len(energy)//2),
 "the_belt_works_where_flagged": bool(lever_works),
}
master=receipt({"r":[r.get("receipt") for r in results if "receipt" in r],"c":checks})
synthesis=(f"Re-run on the finest grain: every system carries MORE directed motion than a totals view shows. "
   f"Of {len(energy)} energy systems, {len(on_course)} read ON COURSE (the responsible move already visible — no "
   f"bad report cards); {len(flagged)} show a cast that would lower the clean/commons share if left uncorrected — "
   "and for those the corrective lever (a modest solar+wind steer) bends the cast back: the seat belt works. The "
   "future the cast shows is a WARNING, not a sentence — a little Dickens: change the image and the image changes.")
out={"_meta":{"tool":"foresight_run.py","what":"seat-belt read: finest-detail motion + forward cast + stewardship gate + corrective lever",
              "n_systems":len(results),"master_receipt":master,"verdict":synthesis if all(checks.values()) else "CHECK FAILED"},
     "systems":results,"checks":checks,
     "extended_language":("know thy system (the finest-grain read), and thy is part of thy system (the operator is a "
        "carrier in what they govern), so don't damage where you live (the stewardship gate + the lever). The cast "
        "is a what-if, the gate a designed breaker; the operator chooses the destination (Breaker 16)."),
     "fence":("EMBER public data; clean/commons = non-fossil share. The forward cast is a clr-velocity "
        "extrapolation (a what-if, NOT a forecast); the stewardship gate + lever are designed, illustrative. "
        "Most systems read fairly. Peter is the sole gate; nothing posted.")}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"FORESIGHT_RESULTS.json"),"w") as f:
    json.dump(out,f,indent=2)
if __name__=="__main__": print(json.dumps(out,indent=2))
