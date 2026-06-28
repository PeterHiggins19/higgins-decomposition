#!/usr/bin/env python3
"""
ultrasonic_probe_hs.py -- the filter-injection ultrasonic probe (the differential engine, made physical).

THE IDEA (Peter): inject a known-property filter signal to cause a desired diagnostic probe, then LOCK ONTO
STRUCTURE by reading the RETURN as perturbed relative to the INJECTED, using Hs. Lineage: HCI-ULTRASOUND
(geometry-lock probe, inert / Paired-Measurement) + AN-001 (cancels by reciprocation; clr is the differential,
reciprocal-antisymmetric) + the P2 differential-engine seed (knock-and-read vs a known reference).

PHYSICS (synthetic but grounded, T2): a non-contact probe interrogates a sub-component (DUT) with a known
injected spectral composition s_inj over D frequency bands. The DUT's STRUCTURE is a power transfer function
|H(f)|^2 (a geometry resonance + maybe a flaw resonance). The measured return is

      return(f) = s_inj(f) * |H(f)|^2 * g   (+ noise)

where g is the NUISANCE COMMON-MODE -- overall source level x coupling efficiency -- the classic bane of
ultrasonic NDE (couplant variability), a single scalar that changes every shot and FOOLS an absolute read.

THE Hs READ (T1 exact): closure+clr is the differential.  z = clr(closure(return)) - clr(closure(s_inj)).
Because clr(g*x)=clr(x), the scalar common-mode g CANCELS EXACTLY -- what remains is clr(|H|^2): the pure
structure. That is "lock onto structure by reading return-as-perturbed-to-injected." Non-invasive: the
injected is known, the probe is read-only, it imprints nothing.

HONEST FENCE: the SCALAR common-mode (source level, coupling) cancels exactly; a frequency-SHAPED nuisance
(e.g. dispersive attenuation) is only partly removed and needs the Paired-Measurement reference channel, not
clr alone. The physics here is a model (synthetic transfer functions), not real ultrasonic hardware data --
that real-data run is the T3 to earn.

Deterministic; SHA-256 receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per
HUF-STD-001. 2026-06-25. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

D=24                                   # frequency bands
BAND_GEOM=6                            # the component's geometry resonance (the structure to lock onto)
BAND_FLAW=17                           # a flaw resonance (crack/delamination) -- present only when flawed

def closure(v):
    v=np.asarray(v,float); return v/v.sum(axis=-1,keepdims=True)
def clr(v):
    v=closure(v); g=np.exp(np.mean(np.log(v),axis=-1,keepdims=True)); return np.log(v/g)

def transfer_power(flawed=False):
    """|H(f)|^2: baseline + a geometry resonance; + a flaw resonance if flawed."""
    H=np.ones(D)
    H[BAND_GEOM]   += 3.0; H[BAND_GEOM-1]+=1.2; H[BAND_GEOM+1]+=1.2     # geometry-lock peak
    if flawed:
        H[BAND_FLAW]+= 2.0; H[BAND_FLAW-1]+=0.8; H[BAND_FLAW+1]+=0.8    # flaw signature
    return H

def shot(flawed, g, rng, noise=0.02, inj="white"):
    """One probe shot. inj='white' = flat known injection (maximally diagnostic)."""
    s_inj = np.ones(D) if inj=="white" else (1.0+0.5*np.cos(np.linspace(0,np.pi,D)))
    s_inj = closure(s_inj)
    H = transfer_power(flawed)
    ret = s_inj * H * g                                 # the scalar common-mode g multiplies all bands
    ret = ret * (1+noise*rng.standard_normal(D))        # independent measurement noise
    ret = np.abs(ret)
    return s_inj, ret

def hs_structure(s_inj, ret):
    """The differential read: z = clr(return) - clr(injected) = clr(|H|^2), common-mode g removed exactly."""
    return clr(ret) - clr(s_inj)

if __name__=="__main__":
    rng=np.random.default_rng(7)
    z_true_healthy = clr(transfer_power(False))

    # ---- (1) STRUCTURE RECOVERY under a wild nuisance common-mode ----
    recov_err=[]; hs_geom=[]
    for _ in range(200):
        g=rng.uniform(0.2,5.0)                          # coupling/source level varies 25x shot to shot
        s_inj,ret=shot(False,g,rng)
        z=hs_structure(s_inj,ret)
        recov_err.append(np.sqrt(np.mean((z-z_true_healthy)**2)))
        hs_geom.append(int(np.argmax(z)))
    recovery_rmse=float(np.mean(recov_err))
    hs_band_vals=[]; abs_band_vals=[]
    for _ in range(200):
        g=rng.uniform(0.2,5.0); s_inj,ret=shot(False,g,rng)
        hs_band_vals.append(hs_structure(s_inj,ret)[BAND_GEOM])
        abs_band_vals.append(np.log(ret)[BAND_GEOM])
    cm_rej_dB=float(10*np.log10(np.var(abs_band_vals)/(np.var(hs_band_vals)+1e-30)))

    # ---- (2) FLAW DETECTION under the same wild nuisance ----
    def flaw_stats(flawed):
        hs=[]; ab=[]
        for _ in range(300):
            g=rng.uniform(0.2,5.0); s_inj,ret=shot(flawed,g,rng)
            hs.append(hs_structure(s_inj,ret)[BAND_FLAW])      # Hs differential flaw statistic
            ab.append(np.log(ret)[BAND_FLAW])                  # absolute flaw statistic
        return np.array(hs),np.array(ab)
    hs_h,ab_h=flaw_stats(False); hs_f,ab_f=flaw_stats(True)
    def separability(a,b):
        return float(abs(a.mean()-b.mean())/np.sqrt(0.5*(a.var()+b.var())+1e-30))
    sep_hs=separability(hs_h,hs_f); sep_abs=separability(ab_h,ab_f)

    out={"_meta":{"tool":"ultrasonic_probe_hs.py",
                  "what":"filter-injection ultrasonic probe: lock onto structure by reading return-vs-injected in clr space; scalar common-mode (coupling/source) cancels exactly.",
                  "D_bands":D,"geometry_band":BAND_GEOM,"flaw_band":BAND_FLAW},
         "structure_recovery":{
             "rmse_vs_true_clr_structure":float(f"{recovery_rmse:.3e}"),
             "geometry_lock_band_modal":int(np.bincount(hs_geom).argmax()),
             "geometry_lock_correct":bool(np.bincount(hs_geom).argmax()==BAND_GEOM),
             "common_mode_rejection_dB_vs_absolute":round(cm_rej_dB,1)},
         "flaw_detection_under_varying_coupling":{
             "Hs_differential_separability":round(sep_hs,2),
             "absolute_read_separability":round(sep_abs,2),
             "verdict":("Hs locks the flaw; absolute read is swamped by coupling variation"
                        if sep_hs>5 and sep_abs<2 else "see numbers")},
         "non_invasive":"injected known + read-only; the probe imprints nothing (inert)"}
    blob=json.dumps(out,sort_keys=True,default=str).encode()
    out["_meta"]["receipt_sha256"]=hashlib.sha256(blob).hexdigest()[:16]
    print(json.dumps(out,indent=2))
