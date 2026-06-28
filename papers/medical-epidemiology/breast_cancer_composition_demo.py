#!/usr/bin/env python3
"""
breast_cancer_composition_demo.py -- a deterministic, receipted compositional read for cancer-incidence
EPIDEMIOLOGY (population-level, NOT patient diagnosis), demonstrated on the breast-cancer epidemiological
transition. The mechanism that was missing when the cancer thread was quarantined now exists: closure -> clr ->
directedness -> motion-helmsman -> forward cast -> SHA-256 receipt (the same instrument as the energy and
psychology reads).

IMPORTANT -- THE DATA HERE IS ILLUSTRATIVE / SYNTHETIC, clearly labelled. It is parameterized to the DOCUMENTED
QUALITATIVE DIRECTION reported in the literature (in India, breast cancer has risen to become the leading female
cancer while the cervical-cancer share has declined -- an epidemiological transition). It is NOT real registry
counts and NO real percentages are asserted. The REAL data plug-in -- India National Cancer Registry Programme
(NCRP/ICMR) or GLOBOCAN/IARC female cancer-incidence-by-site, by year -- is NAMED and PENDING: it is the
collaborator's contribution (the "one dataset away" pattern). With that plug-in, this exact pipeline returns the
measured read with a real-data fingerprint, as the energy/psychology studies do.

GUARDRAIL (the project's own EITT safety boundary, EITT_SAFETY_BOUNDARIES.md): do NOT apply this to small-n
patient-level clinical cohorts (the canonical misuse example is a 15-patient breast-cancer microbiome study --
a power problem, not a finding). This is POPULATION epidemiology: large counts, descriptive, not a diagnosis,
not a treatment, not clinical guidance.

Deterministic; numpy + stdlib. Author: Peter Higgins (human authorship for all claims); AI-assisted per
HUF-STD-001. 2026-06-27. Peter is the sole gate; nothing posted; the medical/commercial track is private.
"""
import numpy as np, json, hashlib
FLOOR=1e-12
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,FLOOR,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def softmax_clr(z): z=np.asarray(z,float); e=np.exp(z-z.max()); return e/e.sum()
def eff_dim(v): v=closure(v); H=-np.sum(v*np.log(v+1e-300),-1); return float(np.exp(np.mean(H)))
def sha(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]

# ---- ILLUSTRATIVE composition (NOT real counts): female cancer sites, ~25 yearly points ----
# parameterized ONLY to the documented direction: breast share rising, cervix share falling, others ~stable.
SITES=["Breast","Cervix","Ovary","Oral cavity","Other"]
T=25
def illustrative_series(seed=0):
    r=np.random.default_rng(seed); rows=[]
    # starting shares (illustrative, NOT a claim): cervix-led, breast second
    base=np.array([0.18,0.26,0.10,0.12,0.34])
    for t in range(T):
        f=t/(T-1)
        shift=np.array([+0.14*f, -0.16*f, +0.01*f, -0.01*f, +0.02*f])   # breast up, cervix down (documented direction)
        row=np.clip(base+shift+r.normal(0,0.004,len(SITES)),1e-3,None)
        rows.append(row)
    return np.array(rows)

X=illustrative_series()
Xc=closure(np.clip(X,FLOOR,None)); now=Xc[-1]
C=clr(np.clip(X,FLOOR,None)); dC=np.diff(C,axis=0)
path=float(np.sum(np.linalg.norm(dC,axis=1))); net=float(np.linalg.norm(C[-1]-C[0]))
directed=round(net/path,3) if path else None
K=10; vel=np.mean(dC[-K:],axis=0); helm=SITES[int(np.argmax(np.abs(vel)))]   # fastest clr-mover
H=10; cast=softmax_clr(C[-1]+H*vel)
def slope_dir(j):   # interpretable: raw-share trend over the recent window
    return "rising" if (Xc[-1][j]-Xc[-K][j])>0 else "falling"
parts={SITES[j]:{"share_start":round(float(Xc[0][j]),3),"share_now":round(float(now[j]),3),
                 "share_cast_%dy"%H:round(float(cast[j]),3),"direction":slope_dir(j)} for j in range(len(SITES))}
receipt=sha({"sites":SITES,"X":[[round(float(x),6) for x in row] for row in X.tolist()],
             "directed":directed,"helm":helm,"parts":parts})
checks={
 "method_reads_the_transition": bool(parts["Breast"]["direction"]=="rising" and parts["Cervix"]["direction"]=="falling"),
 "helmsman_is_the_transition_pair": bool(helm in ("Breast","Cervix")),
 "directedness_measured": bool(directed is not None),
 "valid_composition": bool(abs(float(now.sum())-1.0)<1e-9),
}
verdict=(f"METHOD DEMONSTRATION (ILLUSTRATIVE data): a totals-only view of cancer burden misses the COMPOSITION "
   f"turning underneath it. The compositional read catches the transition exactly -- trajectory directedness "
   f"{directed}; the fastest-moving part (motion-helmsman) is the '{helm}' share, with breast the rising "
   f"counterpart and the cervical share falling -- cast forward as a what-if. Cancer-as-compositional-drift, read "
   "deterministically with a receipt. The REAL India NCRP/GLOBOCAN registry plug-in is named and pending (the "
   "collaborator's data); this pipeline then returns the measured read with a real-data fingerprint.") if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"breast_cancer_composition_demo.py","what":"receipted compositional read for cancer-incidence epidemiology (ILLUSTRATIVE demo)",
              "DATA_STATUS":"ILLUSTRATIVE / SYNTHETIC -- parameterized to the documented direction; NOT real counts; real registry plug-in pending",
              "receipt_sha256":receipt,"verdict":verdict},
     "sites":SITES,"effective_dimension":round(eff_dim(np.mean(Xc,0)),3),"trajectory_directedness":directed,
     "motion_helmsman":helm,"parts":parts,"checks":checks,
     "real_data_plug_in":"India National Cancer Registry Programme (NCRP/ICMR) or GLOBOCAN/IARC female cancer-incidence-by-site, by year -- the collaborator's contribution",
     "guardrail":"EITT_SAFETY_BOUNDARIES.md: population epidemiology only; NOT small-n patient cohorts; NOT diagnosis/treatment/clinical guidance.",
     "fence":("ILLUSTRATIVE data, not real registry counts; no real percentage asserted. Descriptive epidemiology, "
        "not causal, not clinical. The instrument reads/cast a COMPOSITION; it does not detect, predict, or treat "
        "cancer in any person. Real-data use gated on registry data + oncology/epidemiology experts + validation. "
        "Peter is the sole gate; nothing posted; the medical track is private.")}
if __name__=="__main__": print(json.dumps(out,indent=2))
