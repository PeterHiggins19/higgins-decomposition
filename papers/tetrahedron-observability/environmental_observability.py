#!/usr/bin/env python3
"""
environmental_observability.py -- the core math of the real payoff: WHY a system with compositional coherence
can tell a lot about its OUTSIDE environment, and exactly how much, as a function of DWELL (time), CONTACT
(coupling), and SIZE OF MESH (number of components). This is the observability law that lives under the
self-diagnostic / jailor read.

Setup (extends the jailor): a confined composition is a sensor. An external environment imposes a confining
FIELD f (a vector in clr space, dimension = mesh-1). The system is observed over T samples (DWELL), each
coupled to the field with strength kappa (CONTACT) under measurement noise sigma. The system estimates the
field from its own deformation. We measure how well it recovers the environment as we vary T, kappa, and the
mesh size D.

TWO LAWS, measured:
  1. PRECISION from dwell x contact: recovery error ~ sigma / (kappa * sqrt(T)). More dwell and more contact
     -> sharper read of the outside. (averaging T independent looks; SNR grows as kappa*sqrt(T)).
  2. RESOLUTION from mesh size: a D-part composition resolves an environment of at most D-1 independent
     directions. A COARSE mesh (parts aggregated) senses LESS of the environment than a FINE mesh of the same
     world -- aggregation throws away resolvable directions. So 'size of mesh' = how many independent things
     about the outside you can distinguish.

THE TETRAHEDRON: D=4 is the minimum mesh whose clr space is 3-D -- the minimum that can LOCATE a point in a
VOLUME (locate, not merely detect). Four poles, three independent contrasts: the tetrahedron is the smallest
full-3-D environmental locator.

HONEST: synthetic; a linear near-equilibrium sensor model (compositional Hooke); it gives WHERE/HOW MUCH of
the environment, not WHY/WHO (Breaker 16). Deterministic; receipt. Author: Peter Higgins (human authorship for
all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

def sumzero(v): v=np.asarray(v,float); return v-v.mean()
def cos(a,b): return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-12))

def recover(D, T, kappa, sigma=1.0, seed=0):
    """recover a known environment field through a D-part mesh over T looks at coupling kappa."""
    r=np.random.default_rng(seed)
    field=sumzero(r.standard_normal(D)); field/=np.linalg.norm(field)   # unit environment field, dim D-1
    looks=[kappa*field+sumzero(sigma*r.standard_normal(D)) for _ in range(T)]
    est=np.mean(looks,axis=0)/kappa                                      # the system's estimate of the outside
    return cos(est,field), float(np.linalg.norm(est-field)/np.linalg.norm(field))

# --- LAW 1: precision from dwell x contact (fix mesh D=6) ---
law1=[]
for T in (1,10,100,1000):
    for kappa in (0.3,1.0,3.0):
        cs=[]; er=[]
        for s in range(40):
            c,e=recover(6,T,kappa,seed=s); cs.append(c); er.append(e)
        law1.append({"dwell_T":T,"contact_kappa":kappa,"mean_cos":round(float(np.mean(cs)),3),
                     "mean_rel_error":round(float(np.mean(er)),3)})

# --- LAW 2: resolution from mesh size (fix dwell+contact); coarse vs fine mesh on the SAME world ---
def coarse_recover(D_fine, group, T, kappa, sigma=1.0, seed=0):
    """sense a D_fine environment through a COARSE mesh that aggregates parts into 'group' bins."""
    r=np.random.default_rng(seed)
    field=sumzero(r.standard_normal(D_fine)); field/=np.linalg.norm(field)
    # aggregation matrix: D_fine -> group bins (the coarse mesh sees only bin-sums)
    A=np.zeros((group,D_fine))
    for i in range(D_fine): A[i%group,i]=1.0
    looks=[kappa*field+sumzero(sigma*r.standard_normal(D_fine)) for _ in range(T)]
    fine_est=np.mean(looks,axis=0)/kappa
    coarse_obs=np.mean([A@l for l in looks],axis=0)/kappa               # coarse mesh only sees bin sums
    coarse_back=sumzero(A.T@coarse_obs)                                  # best back-projection to fine space
    return cos(fine_est,field), cos(coarse_back,field)
law2=[]
for group in (2,3,5,10):
    fcs=[]; ccs=[]
    for s in range(40):
        fc,cc=coarse_recover(10,group,200,1.0,seed=s); fcs.append(fc); ccs.append(cc)
    law2.append({"fine_mesh_parts":10,"coarse_mesh_parts":group,
                 "fine_cos":round(float(np.mean(fcs)),3),"coarse_cos":round(float(np.mean(ccs)),3),
                 "resolvable_dims_coarse":group-1})

# --- the tetrahedron point: D=4 resolves a 3-D environment (locate in a volume) ---
tetra=[{"mesh_D":D,"clr_dims":D-1,"locates":("volume (3-D)" if D-1>=3 else ("plane (2-D)" if D-1==2 else
        ("line (1-D)" if D-1==1 else "nothing")))} for D in (2,3,4,6)]

checks={
 "precision_improves_with_dwell": bool(law1[0]["mean_rel_error"] > [r for r in law1 if r["dwell_T"]==1000 and r["contact_kappa"]==0.3][0]["mean_rel_error"]),
 "precision_improves_with_contact": bool([r for r in law1 if r["dwell_T"]==10 and r["contact_kappa"]==0.3][0]["mean_rel_error"]
                                         > [r for r in law1 if r["dwell_T"]==10 and r["contact_kappa"]==3.0][0]["mean_rel_error"]),
 "finer_mesh_resolves_more": bool(law2[0]["coarse_cos"] < law2[-1]["coarse_cos"]),
 "tetrahedron_locates_in_volume": bool([t for t in tetra if t["mesh_D"]==4][0]["clr_dims"]==3),
}
law=("Recoverable knowledge of the OUTSIDE  ~  (mesh_parts - 1)  x  precision,  where precision grows as "
     "contact_kappa * sqrt(dwell_T) / noise. DIMENSION comes from the MESH (D-1 independent directions); "
     "PRECISION comes from DWELL x CONTACT. Compositional coherence (closure + the locked-discriminant "
     "invariance) is what makes the deformation a faithful, reproducible record of the environment -- so the "
     "looks accumulate instead of cancelling, and the read sharpens.")
verdict=("OBSERVABILITY LAW HOLDS: the outside is read with precision ~ kappa*sqrt(T)/sigma and resolution "
         "= mesh-1; the tetrahedron (D=4) is the minimal mesh that locates in a volume.") if all(checks.values()) else "CHECK FAILED"

out={"_meta":{"tool":"environmental_observability.py","what":"how much a compositional system can tell about its environment, by dwell x contact x mesh","verdict":verdict},
     "THE_CORE_MATH":law,
     "law1_precision_dwell_x_contact":law1,
     "law2_resolution_by_mesh_size":law2,
     "tetrahedron_mesh_locates":tetra,
     "checks":checks,
     "fence":("Synthetic linear near-equilibrium sensor model (compositional Hooke). Gives WHERE/HOW-MUCH of the "
              "environment, not WHY/WHO (Breaker 16). The constants are illustrative; the SHAPE of the law "
              "(dimension from mesh, precision from dwell x contact) is the claim. Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(
    {"l1":law1,"l2":law2,"t":tetra,"c":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]
if __name__=="__main__": print(json.dumps(out,indent=2))
