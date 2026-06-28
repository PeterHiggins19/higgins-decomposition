#!/usr/bin/env python3
"""
brain_kinetics_dwell_mesh.py -- how an animal brain gets "the sense" that Hˢ reveals, from DWELL and MESH. The
math has ONE answer (the exact relational read, clr of the true composition); the brain reaches it by a similar
but different path -- statistical, parallel, noisy -- and this model shows that path CONVERGING to the same
answer as dwell and mesh grow.

The correspondence (structural; real canonical neural computations):
  DIVISIVE NORMALIZATION (a neuron's response / the pooled activity of its neighbours; Carandini & Heeger 2012)
        = CLOSURE -- it cancels a common multiplicative gain (luminance/contrast/context) EXACTLY, the same way
          clr rejects common-mode (~1e-15 here).
  WEBER-FECHNER logarithmic encoding = the LOG. Divisive normalization + log together ~ centered-log-ratio (clr).
  MESH  = the receptor population sampling the scene (population coding).
  DWELL = neural integration time (temporal signal averaging; fixation dwell).
Recoverable structure ~ averages over MESH x DWELL -> the relational read emerges from the noise as ~1/sqrt(N),
exactly the observability law (recoverable ~ (mesh-1) x precision, precision ~ sqrt(dwell)/noise).

HONEST: a STRUCTURAL/computational analogy (T2/T3), not a claim that the brain implements Hˢ or that perception
is literally clr. The brain's path is approximate, learned, parallel; Hˢ computes the exact answer the brain
approaches. Deterministic; receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per
HUF-STD-001. 2026-06-27. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,1e-12,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def sha(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]
D=6
x_true=closure(np.array([3.,1.,2.,1.5,1.,0.8]))     # the relational structure = the math's ONE answer
target=clr(x_true)
def neural_read(MESH, DWELL, sigma=0.4, seed=0):
    rng=np.random.default_rng(seed); acc=np.zeros(D); cm=0.0
    for i in range(MESH):
        gain=np.exp(rng.normal(0,1.0))                  # per-receptor context/luminance gain (a nuisance)
        for t in range(DWELL):
            r=gain*x_true*np.exp(rng.normal(0,sigma,D))  # noisy receptor response
            acc+=np.log(r/r.sum())                       # divisive normalization (=closure) then log; accumulate
        cm=max(cm,float(np.max(np.abs(clr(gain*x_true)-clr(x_true)))))   # gain cancels exactly
    mean_log=acc/(MESH*DWELL); return (mean_log-mean_log.mean()), cm     # center = clr
def rms_err(MESH,DWELL,M=40):
    return float(np.sqrt(np.mean([np.linalg.norm(neural_read(MESH,DWELL,seed=s)[0]-target)**2 for s in range(M)])))
grid=[(1,1),(4,1),(1,16),(4,16),(16,64),(64,256)]
rows=[{"mesh":m,"dwell":d,"product_N":m*d,"aitchison_error_to_exact":round(rms_err(m,d),4)} for m,d in grid]
_,cm=neural_read(8,8)
slope=float(np.polyfit(np.log([r["product_N"] for r in rows]),np.log([r["aitchison_error_to_exact"] for r in rows]),1)[0])
checks={
 "divisive_normalization_cancels_gain_exact": bool(cm<1e-12),
 "error_falls_with_dwell_x_mesh": bool(rows[-1]["aitchison_error_to_exact"]<rows[0]["aitchison_error_to_exact"]),
 "converges_to_the_one_exact_answer": bool(rows[-1]["aitchison_error_to_exact"]<0.05),
 "scale_law_inverse_sqrtN": bool(-0.7<slope<-0.3),
}
master=sha({"rows":rows,"cm":round(cm,18),"checks":checks})
verdict=(f"The brain's path reaches the SAME answer. Divisive normalization cancels the common gain exactly "
   f"(~{cm:.0e}, the same common-mode rejection clr performs), and the relational read converges to the exact "
   f"clr answer as MESH x DWELL grows (error {rows[0]['aitchison_error_to_exact']} at N=1 -> "
   f"{rows[-1]['aitchison_error_to_exact']} at N={rows[-1]['product_N']}), at the ~1/sqrt(N) law (slope {round(slope,3)}). "
   "The math has one answer; the brain approaches it statistically through dwell and mesh; Hˢ computes it "
   "exactly. Same destination, different path.") if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"brain_kinetics_dwell_mesh.py","what":"the brain's dwell x mesh path converges to the exact Hˢ relational read",
              "receipt_sha256":master,"verdict":verdict},
     "true_composition":x_true.tolist(),"convergence":rows,"divisive_norm_gain_residual":float(f"{cm:.1e}"),
     "scale_law_slope":round(slope,3),"checks":checks,
     "fence":("Structural/computational analogy (T2/T3): divisive normalization (Carandini & Heeger 2012) = "
        "closure; Weber-Fechner = log; population = mesh; integration time = dwell. NOT a claim the brain "
        "implements Hˢ or that perception is literally clr -- the brain's path is approximate, learned, parallel; "
        "Hˢ computes the exact answer the brain approaches. Peter is the sole gate; nothing posted.")}
if __name__=="__main__": print(json.dumps(out,indent=2))
