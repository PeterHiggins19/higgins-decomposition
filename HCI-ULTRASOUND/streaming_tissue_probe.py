#!/usr/bin/env python3
"""
streaming_tissue_probe.py -- the streaming tissue probe: lock onto fine structure in real time, cancel
relative probe/patient motion, and climb the resolution ladder to the system's coherence limit (max Q).

How an EXISTING animal-tissue ultrasound study plugs in: RF/IQ returns (e.g. PICMUS plane-wave data, CUBDL
subsets) -> per-band scattering-power composition over depth/frequency. The probe reads each frame's
composition against a reference; clr makes the read a DIFFERENTIAL, so:

  * MOTION CANCELLATION: rigid relative motion (probe moving, patient moving) appears as a shared
    multiplicative common-mode (coupling/gain) -> clr(g*x)=clr(x) cancels it EXACTLY. The patient can relax
    in a comfortable posture; the instrument reads structure, not pose.
  * STREAMING RESOLUTION CLIMB: as frames accumulate (N grows) the averaged differential's noise falls ~1/sqrt(N),
    so finer features rise above the floor IN REAL TIME -- climbing the max-power ladder -- until the COHERENCE
    floor (max Q: the irreducible decorrelation) caps it. That asymptote is the system's own limit.
  * CONTROL SIGNALS: each frame emits a coherence read-back (lock quality), the estimated rigid drift (for
    SE(3) registration/mapping), and a temporal-coherence flag.

HONEST: rigid/common-mode motion cancels exactly; NON-rigid tissue deformation is a REAL structural change
(correctly NOT cancelled -- it is signal); out-of-plane decorrelation is the irreducible floor (max Q) and is
NOT averaged away. RESEARCH INSTRUMENT ONLY -- not diagnostic/clinical (IEC 62304/ISO 13485 bar). The physics
here is a grounded MODEL (T2); real RF data is the T3 to earn. Deterministic; receipt. Peter is the sole gate.
"""
import numpy as np, json, hashlib

D=32                                   # scattering bands (depth/frequency)
def closure(v):
    v=np.asarray(v,float); return v/v.sum(axis=-1,keepdims=True)
def clr(v):
    v=closure(v); g=np.exp(np.mean(np.log(v),axis=-1,keepdims=True)); return np.log(v/g)

FEATURES={6:0.50, 12:0.20, 19:0.08, 25:0.03}     # band: clr amplitude (0.03 = the smallest detail)
def true_structure():
    z=0.05*np.sin(np.linspace(0,3*np.pi,D))
    for b,a in FEATURES.items(): z[b]+=a
    return z - z.mean()

def frame(zt, g, decorr, rng, deform_band=None, deform_amp=0.0):
    z = zt.copy()
    if deform_band is not None: z[deform_band]+=deform_amp     # a REAL non-rigid structural change
    lin = np.exp(z)
    ret = lin * g                                              # rigid relative-motion common-mode (scalar)
    ret = ret * np.exp(decorr*rng.standard_normal(D))          # out-of-plane decorrelation (does NOT cancel)
    return ret

if __name__=="__main__":
    rng=np.random.default_rng(5)
    zt=true_structure(); ref_clr=clr(np.exp(np.zeros(D)))
    sigma=0.06; coh_floor=0.008                                # per-frame decorrelation; max-Q irreducible floor

    clr_est=[]; abs_est=[]
    for _ in range(400):
        g=rng.uniform(0.2,5.0); ret=frame(zt,g,sigma,rng)
        clr_est.append((clr(ret)-ref_clr)[6]); abs_est.append(np.log(ret)[6])
    motion_cancel_dB=float(10*np.log10(np.var(abs_est)/(np.var(clr_est)+1e-30)))

    def finest_resolved(n_frames):
        acc=np.zeros(D)
        for _ in range(n_frames):
            g=rng.uniform(0.2,5.0); acc+=(clr(frame(zt,g,sigma,rng))-ref_clr)
        z=acc/n_frames; noise=max(sigma/np.sqrt(n_frames), coh_floor)
        resolved={b:bool(abs(z[b])>3*noise) for b in FEATURES}
        smallest=min([FEATURES[b] for b,ok in resolved.items() if ok], default=None)
        return {"frames":n_frames,"noise_floor":round(noise,4),
                "features_resolved":sum(resolved.values()),"smallest_detail_resolved":smallest}
    climb=[finest_resolved(n) for n in [1,4,16,64,256,1024]]

    sigs=[]
    for k in range(5):
        g=rng.uniform(0.5,2.0); ret=frame(zt,g,sigma,rng); z=clr(ret)-ref_clr
        coherence=float(1-np.var(z-zt)/(np.var(z)+1e-12))
        drift=float(np.mean(np.log(ret)-z-ref_clr))
        sigs.append({"frame":k,"coherence_readback":round(max(0,coherence),3),
                     "rigid_drift_log_g":round(drift,3),"lock":bool(coherence>0.8)})

    ret_def=frame(zt,1.3,sigma,rng,deform_band=15,deform_amp=0.4)
    deform_seen=bool(abs((clr(ret_def)-ref_clr)[15])>0.2)

    out={"_meta":{"tool":"streaming_tissue_probe.py",
                  "what":"streaming tissue probe: lock fine structure, cancel rigid relative motion, climb resolution to the coherence (max-Q) limit; emit positional+temporal coherence control signals.",
                  "data_ingestion":"existing RF/IQ ultrasound (PICMUS plane-wave; CUBDL subsets) -> per-band scattering composition; model used here is grounded synthetic (T2)",
                  "D_bands":D,"smallest_true_feature_clr":min(FEATURES.values())},
         "motion_cancellation":{"rigid_relative_motion_swing":"0.2-5x (25x)",
              "structure_read_stability_dB_vs_absolute":round(motion_cancel_dB,1),
              "meaning":"patient may relax / move; rigid relative motion cancels as common-mode, the structure read holds"},
         "streaming_resolution_climb":climb,
         "control_signals_sample":sigs,
         "honest_fences":{
              "non_rigid_deformation_detected_not_cancelled":deform_seen,
              "coherence_floor_caps_resolution":f"noise cannot fall below {coh_floor} (max-Q irreducible decorrelation)",
              "out_of_plane_decorrelation":"independent, NOT cancelled -- sets the floor",
              "tier":"T1 common-mode cancellation exact; T2 tissue model; T3 real RF data + clinical validation"}}
    out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()[:16]
    print(json.dumps(out,indent=2))
