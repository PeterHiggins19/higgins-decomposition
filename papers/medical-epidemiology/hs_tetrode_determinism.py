#!/usr/bin/env python3
"""
hs_tetrode_determinism.py -- make the DUT data PAY for its lack of determinism. The instrument (Hˢ) is exact;
the noise lives in the data under test (DUT), never in Hˢ. We distribute the DUT error across N redundant
elements (the TETRODE = 4, the sensitive-case extension) and let basic statistics + the math of scale cancel it:

  * COMMON-MODE error (a per-element multiplicative gain / scale) -> cancelled EXACTLY by clr (closure removes
    any shared scalar; residual at the IEEE floor ~1e-15). This is the "never Hs": the instrument adds nothing.
  * INDEPENDENT error (per-element, per-part noise) -> averaged down by the LAW OF LARGE NUMBERS, ~ sigma/sqrt(N).
    More elements = more ways to find the determinism hidden in the noise.

So a NON-deterministic measurement is made to yield a deterministic, receipted read: clr each element (kills the
common mode), average across the N elements (kills the independent part), exp+closure back. The TETRODE (N=4) is
the recommended redundancy for sensitive cases; N=8,16 show the scale law continuing.

THE 3-WITNESS TEST (3-to-locate): the same recovery is run on THREE INDEPENDENT real DUT datasets -- energy
(EMBER India), geochemistry (Ball oxides), commodities (gold/silver). Independent domains, one law: the
repetition is the signal, each with its own receipt.

Deterministic (seeded); numpy + stdlib. Author: Peter Higgins (human authorship for all claims); AI-assisted per
HUF-STD-001. 2026-06-27. Peter is the sole gate; nothing posted.
"""
import numpy as np, csv, os, json, hashlib
HS=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..")
def P(*a): return os.path.normpath(os.path.join(HS,*a))
FLOOR=1e-9
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,FLOOR,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def inv_clr(z): return closure(np.exp(z))
def aitch(a,b): return float(np.linalg.norm(clr(a)-clr(b)))   # Aitchison distance via clr
def sha(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]
def load_mean_composition(path,drop=()):
    with open(P(path)) as f: rows=list(csv.reader(f))
    hdr=rows[0]; keep=[i for i,h in enumerate(hdr) if h not in drop]; data=[]
    for r in rows[1:]:
        try:
            vals=[float(r[i]) for i in keep]
            if all(np.isfinite(vals)) and min(vals)>0: data.append(vals)
        except (ValueError,IndexError): pass
    X=np.array(data); return [hdr[i] for i in keep], closure(np.clip(X.mean(0),FLOOR,None))

def tetrode_recover(x_true, N, sigma_ind=0.15, seed=0):
    """Build N noisy DUT elements (common-mode gain + independent per-part noise); recover via clr-average."""
    r=np.random.default_rng(seed); D=len(x_true)
    gains=np.exp(r.normal(0,0.8,N))                       # per-element common-mode multiplicative scale
    clrs=[]; cm_resid=0.0
    for i in range(N):
        eps=r.normal(0,sigma_ind,D)                       # independent per-part log-noise
        y=gains[i]*x_true*np.exp(eps)                     # the DUT element (scaled + noisy)
        cz=clr(y); clrs.append(cz)
        cm_resid=max(cm_resid, float(np.max(np.abs(clr(gains[i]*x_true)-clr(x_true)))))  # gain cancels exactly
    x_hat=inv_clr(np.mean(clrs,0))                        # average the N elements -> recovered composition
    return x_hat, cm_resid

DATASETS=[
 ("Energy (EMBER India)","data/Energy/EMBER_pipeline_ready/ember_IND_India_generation_TWh.csv",("Year",)),
 ("Geochemistry (Ball oxides)","data/Geochemistry/ball_oxides_composition.csv",()),
 ("Commodities (gold/silver)","data/Commodities/gold_silver_simplex.csv",()),
]
Ns=[1,2,4,8,16]; M=200   # M trials per N -> RMS error (the scale law is about EXPECTED error, not one draw)
witnesses=[]
for name,path,drop in DATASETS:
    parts,x_true=load_mean_composition(path,drop)
    errs={}; cmr=0.0
    for N in Ns:
        sq=0.0
        for t in range(M):
            x_hat,cm=tetrode_recover(x_true,N,seed=1000+t); sq+=aitch(x_hat,x_true)**2; cmr=max(cmr,cm)
        errs[N]=round(float(np.sqrt(sq/M)),6)   # RMS Aitchison error over M trials
    # math of scale: slope of log(err) vs log(N)
    logN=np.log(Ns); logE=np.log([errs[N] for N in Ns]); slope=float(np.polyfit(logN,logE,1)[0])
    # Hs own numerical floor: clr -> inv_clr round trip
    floor=float(np.max(np.abs(inv_clr(clr(x_true))-x_true)))
    w={"witness":name,"D_parts":len(parts),"common_mode_residual":float(f"{cmr:.1e}"),
       "tetrode_N4_error":errs[4],"single_N1_error":errs[1],"err_by_N":errs,
       "scale_law_slope_logE_vs_logN":round(slope,3),"Hs_numeric_floor":float(f"{floor:.1e}")}
    w["receipt"]=sha({k:w[k] for k in ("witness","D_parts","common_mode_residual","tetrode_N4_error","single_N1_error","scale_law_slope_logE_vs_logN")})
    witnesses.append(w)

checks={
 "common_mode_cancelled_exact_all3": bool(all(w["common_mode_residual"]<1e-12 for w in witnesses)),
 "tetrode_beats_single_all3": bool(all(w["tetrode_N4_error"]<w["single_N1_error"] for w in witnesses)),
 "scale_law_near_inverse_sqrtN_all3": bool(all(-0.75<w["scale_law_slope_logE_vs_logN"]<-0.25 for w in witnesses)),
 "Hs_at_the_floor_all3": bool(all(w["Hs_numeric_floor"]<1e-12 for w in witnesses)),
}
master=sha({"w":[w["receipt"] for w in witnesses],"c":checks})
verdict=(f"3-WITNESS TEST COMPLETE. Across three INDEPENDENT real DUTs, the common-mode (scale) error is cancelled "
   f"EXACTLY by clr (residual ~{witnesses[0]['common_mode_residual']}, the 'never Hs'), and the independent error "
   f"falls as ~1/sqrt(N) (slopes {[w['scale_law_slope_logE_vs_logN'] for w in witnesses]}) -- the TETRODE (N=4) "
   f"beats a single read on all three. The non-deterministic data is made to pay: statistics + the math of scale "
   "find the determinism in the noise, while Hˢ stays at the IEEE floor. The repetition across independent domains "
   "is the signal.") if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"hs_tetrode_determinism.py","what":"tetrode (N-element) determinism-from-noise; 3 independent real DUTs",
              "master_receipt":master,"verdict":verdict},
     "witnesses":witnesses,"N_elements_tested":Ns,
     "the_method":("clr each DUT element (common-mode/scale cancels exactly) -> average across N elements "
        "(independent noise ~1/sqrt(N)) -> exp+closure. TETRODE=4 for sensitive cases. Error lives in the DUT, "
        "never in Hˢ."),
     "fence":("The common-mode cancellation is exact for strictly-positive compositions (the locked-discriminant "
        "precondition; structural zeros excluded, E-21). The 1/sqrt(N) law assumes independent per-element noise; "
        "in-subspace correlated noise is provably not separable. Real datasets supply realistic compositions; the "
        "DUT noise model is the controlled, declared part. Peter is the sole gate; nothing posted.")}
if __name__=="__main__": print(json.dumps(out,indent=2))
