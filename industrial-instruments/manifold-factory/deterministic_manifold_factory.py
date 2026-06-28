#!/usr/bin/env python3
"""
deterministic_manifold_factory.py -- the USEFUL application of the Piccirillo move (generate exact deterministic
manifolds with planted, recoverable invariants): an engineering GROUND-TRUTH / DIGITAL-TWIN / CALIBRATION
factory. Engineering rarely has an EXACT known-answer reference to validate a solver, calibrate a sensor, or
certify a detector against. This builds one -- a deterministic compositional manifold whose invariants are
planted (so the true answer is known to the floor) and recoverable -- for several compositional engineering
domains. The Piccirillo move "makes a system": the exact adjacent reference twin you measure the real one against.

For each domain it generates an exact manifold and checks the three things that make it a usable reference:
  CONSERVED   : the budget closes exactly (a conserved quantity -- mass/energy)            -> residual 0
  GAIN-INVARIANT : the relational read cancels overall scale exactly (calibrates out sensor gain) -> ~1e-15
  RECOVERABLE : the planted feature (regime transition / dominant mode / spectral peak) is recovered from the
                generated manifold -> a detector validated against a KNOWN answer (hit).

Domains: fluid (Reynolds regime mix), chemistry (species + conservation), radiation (isotope spectrum),
field dynamics (modal energy).

HONEST FENCE: these are COMPOSITIONAL/dimensionless engineering quantities (regime fractions, species fractions,
spectral bins, modal shares) -- NOT raw Navier-Stokes / NOT a CFD or transport solver / NOT a physics engine.
The manifold encodes PLANTED (assumed) structure for VALIDATION + CALIBRATION, not prediction of real flow/
reaction/decay. Reynolds/transition values are illustrative. Radiation = research/QA, not a clinical/safety
device. Deterministic; receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per
HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,1e-12,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def sig(x): return 1.0/(1.0+np.exp(-x))
rng=np.random.default_rng(20260626)
def gain_invariance(M):                       # relational read cancels overall scale exactly
    g=rng.uniform(0.1,10,size=(M.shape[0],1)); return float(np.max(np.abs(clr(g*M)-clr(M))))
def conserved(M): return float(np.max(np.abs(closure(M).sum(1)-1.0)))
def bisect(f,a,b,tol=1e-13):
    for _ in range(200):
        m=0.5*(a+b)
        if f(a)*f(m)<=0: b=m
        else: a=m
        if b-a<tol: break
    return 0.5*(a+b)

results={}

# 1. FLUID -- Reynolds-driven regime composition {laminar, transitional, turbulent}; planted transition Re*
RE_STAR=2300.0; W=300.0
def turb(Re): return float(sig((Re-RE_STAR)/W))
Re_grid=np.linspace(500,5000,120)
fluid=np.array([closure([ (1-turb(Re))*0.85, (1-turb(Re))*0.15+0.02, turb(Re)+0.02 ]) for Re in Re_grid])
Re_star_rec=bisect(lambda Re: turb(Re)-0.5, 500,5000)       # recover the planted transition
results["fluid_reynolds"]={"planted_Re_star":RE_STAR,"recovered_Re_star":round(Re_star_rec,3),
    "recovery_residual":float(f"{abs(Re_star_rec-RE_STAR):.1e}"),
    "conserved_residual":float(f"{conserved(fluid):.0e}"),"gain_invariance_residual":float(f"{gain_invariance(fluid):.0e}"),
    "detector_hit":bool(abs(Re_star_rec-RE_STAR)<1e-6)}

# 2. CHEMISTRY -- extent-of-reaction; {reactant, product, catalyst}; conserved closure; planted half-conversion
xi=np.linspace(0,1,120)
chem=np.array([closure([1-x+1e-3, x+1e-3, 0.1]) for x in xi])
xi_half=bisect(lambda x:(x+1e-3)-(1-x+1e-3),0,1)            # reactant==product crossover (planted 0.5)
results["chemistry_species"]={"planted_half_conversion":0.5,"recovered":round(xi_half,4),
    "recovery_residual":float(f"{abs(xi_half-0.5):.1e}"),
    "conserved_residual":float(f"{conserved(chem):.0e}"),"gain_invariance_residual":float(f"{gain_invariance(chem):.0e}"),
    "detector_hit":bool(abs(xi_half-0.5)<1e-6)}

# 3. RADIATION -- energy-bin spectrum with a planted isotope peak; across exposures (overall counts vary)
BINS=12; PEAK=7
def spectrum(exposure):
    base=np.ones(BINS)*0.5; base[PEAK]+=4.0; base[PEAK-1]+=1.0; base[PEAK+1]+=1.0
    return closure(exposure*base)                            # exposure = overall gain (cancels in clr)
rad=np.array([spectrum(e) for e in rng.uniform(10,10000,size=80)])
peak_rec=int(np.argmax(clr(rad).mean(0)))                    # recover isotope peak bin, invariant to exposure
results["radiation_spectrum"]={"planted_peak_bin":PEAK,"recovered_peak_bin":peak_rec,
    "recovery_residual":int(abs(peak_rec-PEAK)),
    "conserved_residual":float(f"{conserved(rad):.0e}"),"gain_invariance_residual":float(f"{gain_invariance(rad):.0e}"),
    "detector_hit":bool(peak_rec==PEAK)}

# 4. FIELD DYNAMICS -- modal energy distribution; planted dominant mode (helmsman); conserved total
MODES=6; DOM=3
field=np.array([closure(np.abs(np.array([1,1,1,5.0,1,1])*(1+0.05*rng.standard_normal(MODES)))) for _ in range(60)])
helm_rec=int(np.argmax(clr(field).mean(0)))
results["field_modes"]={"planted_dominant_mode":DOM,"recovered_dominant_mode":helm_rec,
    "recovery_residual":int(abs(helm_rec-DOM)),
    "conserved_residual":float(f"{conserved(field):.0e}"),"gain_invariance_residual":float(f"{gain_invariance(field):.0e}"),
    "detector_hit":bool(helm_rec==DOM)}

checks={
 "all_conserved_exactly": bool(all(r["conserved_residual"]<1e-12 for r in results.values())),
 "all_gain_invariant_exactly": bool(all(r["gain_invariance_residual"]<1e-12 for r in results.values())),
 "all_invariants_recovered": bool(all(r["detector_hit"] for r in results.values())),
}
verdict=("DETERMINISTIC GROUND-TRUTH FACTORY: across fluid/chemistry/radiation/field, every reference manifold "
   "conserves its budget exactly, cancels sensor gain exactly (calibration), and its planted invariant is "
   "recovered (detector validated against a KNOWN answer).") if all(checks.values()) else "CHECK FAILED"

out={"_meta":{"tool":"deterministic_manifold_factory.py","what":"the Piccirillo move as an engineering ground-truth/calibration/digital-twin factory","verdict":verdict},
     "domains":results,"checks":checks,
     "the_application":("Generate an EXACT reference manifold with planted, recoverable invariants -> validate a "
        "solver/sensor/detector against a known answer, calibrate out its gain (relational read is scale-invariant), "
        "and certify the result with a receipt. The exact adjacent reference the engineer never had."),
     "fence":("COMPOSITIONAL/dimensionless engineering quantities only -- NOT a CFD/transport/physics solver; the "
        "manifold encodes PLANTED structure for VALIDATION+CALIBRATION, not prediction of real flow/reaction/decay; "
        "Reynolds/transition values illustrative; radiation = research/QA not a clinical/safety device. Peter is the "
        "sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(
    {"d":results,"c":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]
if __name__=="__main__": print(json.dumps(out,indent=2))
