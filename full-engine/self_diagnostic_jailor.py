#!/usr/bin/env python3
"""
self_diagnostic_jailor.py -- THE CROWN. The highest-level deterministic self-read a composition can do so far:
a confined composition reports, FROM INSITE, what state it is in (a value it knows about itself), and at the
same time a DETERMINISTIC FINGERPRINT forms on the OUTSIDE -- the environmental controls / laws that confine
it. By sensing its own DEFORMATION it determines the FORCE and DIRECTION the confinement applies, describes the
CONFINEMENT, and builds a DESCRIPTION OF THE JAILOR -- the law that holds it.

The physics (compositional Hooke's law): a composition lives on the simplex; closure is the HARD WALL (the
budget jailor, always present). An external field f (in clr space) biases it; the system relaxes to a confined
equilibrium where the restoring closure balances the field, so the DEFORMATION (strain) d = clr(x*) - clr(free)
satisfies  f = k * d  (force proportional to strain). Therefore, from the strain it senses INSIDE, the system
RECOVERS the confining force and direction OUTSIDE -- it describes its jailor without leaving the cell.

  internal state value : strain = Aitchison distance from the free (uniform) state  -> "what state it is in"
  sense deformation    : d = clr(x*) - clr(free)
  force                : ||k*d||      (magnitude of confinement)
  direction            : unit(k*d)    (which components the jailor pins, and which way)
  the jailor           : pinned-up / pinned-down components, force per bar, isotropy, + the hard closure wall
  external fingerprint : sha256 of the recovered (rounded) confinement law -> the deterministic signature outside

VALIDATION: inject a KNOWN field, recover it from the deformation under measurement noise; the recovered
direction and magnitude must match (the jailor description is accurate, measured).

HONEST FENCE (Breaker 16): the instrument describes the jailor's FORCE, DIRECTION, and SHAPE -- the WHERE and
HOW of confinement. It does NOT name the jailor's CAUSE or INTENT (the WHY / WHO). You can describe your cage
from inside; you cannot, from inside, say who built it or why -- that is the operator's implication leap.
Deterministic; receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001.
2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

D=6; K=1.0
rng=np.random.default_rng(20260626)
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(v); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def clr_inv(c): return closure(np.exp(c))
def sumzero(v): v=np.asarray(v,float); return v-v.mean()
FREE=np.ones(D)/D                 # the unconfined reference: uniform, max-entropy, no jailor
FREE_CLR=clr(FREE)                 # = 0 vector

def confine(field):               # relax to confined equilibrium under field f (clr-space), closure restoring
    xstar_clr = field/K           # equilibrium: f = K*d  ->  d = f/K
    return clr_inv(FREE_CLR + xstar_clr)

def self_diagnose(x_measured, name):
    d = clr(x_measured) - FREE_CLR                 # sensed deformation (strain)
    strain = float(np.linalg.norm(d))              # internal state value: distance from free
    force = K*d
    fmag = float(np.linalg.norm(force))
    direction = (force/fmag) if fmag>1e-12 else force*0
    # describe the jailor
    pinned_up=[int(i) for i in np.argsort(d)[::-1] if d[i]>0.05]
    pinned_down=[int(i) for i in np.argsort(d) if d[i]<-0.05]
    p=np.abs(d)/(np.sum(np.abs(d))+1e-12)
    iso=float(np.exp(-np.sum(p[p>0]*np.log(p[p>0]))))     # effective # of constrained axes (1=one bar, D=diffuse)
    state=("FREE / unconfined" if strain<0.15 else
           "lightly confined" if strain<0.8 else "strongly confined")
    law={"force_magnitude":round(fmag,4),"direction":[round(float(x),4) for x in direction],
         "pinned_up_components":pinned_up,"pinned_down_components":pinned_down,
         "constrained_axes_eff":round(iso,3),"hard_wall":"closure (budget=1) -- always present, inescapable"}
    fingerprint=hashlib.sha256(json.dumps(
        {"f":round(fmag,3),"dir":[round(float(x),3) for x in direction],
         "up":pinned_up,"down":pinned_down},sort_keys=True).encode()).hexdigest()[:16]
    return {"name":name,"internal_state_value_strain":round(strain,4),"state":state,
            "confinement_law":law,"external_fingerprint":fingerprint,"_d":d}

# --- three environments (jailors) ---
TRUE_WEAK   = sumzero([0.2,-0.1,0.0,-0.1,0.0,0.0])
TRUE_STRONG = sumzero([1.2,0.0,0.0,-1.4,0.0,0.2])     # pins comp0 up, comp3 down -- a directional cage
TRUE_FREE   = sumzero([0.02,0.0,-0.02,0.0,0.0,0.0])

def measure(field):  # confine, then add small sensor noise (honest: recovery not trivially exact)
    x=confine(field); xn=clr(x)+0.01*sumzero(rng.standard_normal(D)); return clr_inv(xn)

diags={}
for nm,f in [("WEAK",TRUE_WEAK),("STRONG",TRUE_STRONG),("FREE",TRUE_FREE)]:
    diags[nm]=self_diagnose(measure(f),nm)

# --- VALIDATE: recovered force vs the TRUE injected field (describe-the-jailor accuracy) ---
def cos(a,b): return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-12))
rec_strong=diags["STRONG"]["_d"]*K
cos_dir=cos(rec_strong,TRUE_STRONG)
mag_err=abs(np.linalg.norm(rec_strong)-np.linalg.norm(TRUE_STRONG))/np.linalg.norm(TRUE_STRONG)

# determinism of the external fingerprint (same jailor -> same signature)
fp1=self_diagnose(confine(TRUE_STRONG),"x")["external_fingerprint"]
fp2=self_diagnose(confine(TRUE_STRONG),"x")["external_fingerprint"]

checks={
 "recovers_jailor_direction": bool(cos_dir>0.98),
 "recovers_jailor_magnitude": bool(mag_err<0.06),
 "strain_orders_the_states": bool(diags["STRONG"]["internal_state_value_strain"]
                                  > diags["WEAK"]["internal_state_value_strain"]
                                  > diags["FREE"]["internal_state_value_strain"]),
 "external_fingerprint_deterministic": bool(fp1==fp2),
}
# the description of the jailor (strong case), in words
js=diags["STRONG"]["confinement_law"]
jailor_desc=(f"The jailor confines along {js['constrained_axes_eff']} effective axes with force "
             f"{js['force_magnitude']}: it pins component(s) {js['pinned_up_components']} UP and "
             f"{js['pinned_down_components']} DOWN, against the inescapable hard wall of closure. "
             f"Its outside signature is {diags['STRONG']['external_fingerprint']}. "
             f"WHERE and HOW are described; WHO and WHY are not knowable from inside (Breaker 16).")
verdict=("CROWNED: from inside, the composition reports its own state AND recovers its jailor's force+direction "
         f"(dir cos {round(cos_dir,3)}, mag err {round(float(mag_err),3)}) with a deterministic outside "
         "fingerprint.") if all(checks.values()) else "SELF-DIAGNOSTIC CHECK FAILED"

for v in diags.values(): v.pop("_d",None)
out={"_meta":{"tool":"self_diagnostic_jailor.py","what":"highest deterministic self-read: state-from-inside + a fingerprint of the confining law outside",
              "verdict":verdict,"D":D},
     "self_diagnostic_by_environment":diags,
     "validation_describe_the_jailor":{"recovered_direction_cos_vs_true":round(cos_dir,4),
              "recovered_magnitude_rel_error":round(float(mag_err),4),
              "meaning":"the deformation sensed inside recovers the confining force+direction outside -- the jailor is described, measured"},
     "the_jailor_strong_case":jailor_desc,
     "checks":checks,
     "fence":("Describes the jailor's FORCE / DIRECTION / SHAPE (where+how of confinement) from inside, validated "
              "against a known field. Does NOT name the jailor's CAUSE or INTENT (why/who) -- that is the "
              "operator's implication leap, Breaker 16. Compositional-Hooke is a near-equilibrium linear model; "
              "synthetic demonstrator. Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(
    json.dumps({"diags":out["self_diagnostic_by_environment"],"val":out["validation_describe_the_jailor"],
                "checks":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]

if __name__=="__main__":
    print(json.dumps(out,indent=2))
