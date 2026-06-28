#!/usr/bin/env python3
"""
probe_survey_lock.py -- the ultrasonic probe as INTENDED: an operator-directed SURVEY. A person moves the probe
all around another person in random scanning motions; the operator knows to give many views; the VIEW-SET (not
any single frame) is the deep signal. Hs fuses the views to LOCATE, LOCK, and TRACK the object of interest --
and crucially it locks the DETERMINIZED object, not the loud one.

THE CORE MOVE (Peter): a big bright BLOB to the foreground grabs naive focus, but it is incoherent across the
survey (clutter / reflection / it changes with angle). The real object is a small DARK SPOT that is COHERENT
across every view -- the same compositional signature from every angle once motion is cancelled. Hs picks the
object that is INVARIANT across the view-set (the locked discriminant), NOT the one with the largest amplitude.
'Adjust the beam for THIS' -> steer to the determinized spot.

Then two layers, by design:
  1. Hs SENSOR LAYER  : fuse views -> determinized target -> course of action (beam adjustment, lock, track).
  2. GOVERNANCE/SAFETY : a margin/safety gate decides AUTONOMOUS track vs REPORT-TO-OPERATOR; everything inside
                         an envelope built to comply with certification/standards (the company -- Southmedic --
                         carries the actual certification; Hs supplies the deterministic, certification-READY core).
The lock+track loop is a PID on the Hs read -- P (current error), I (accumulated over dwell/views), D (motion).
That is the recursive shape of the whole instrument: a PID on Hs, Hs scrutinising Hs.

MEDICAL FENCE: RESEARCH / QA demonstrator on SYNTHETIC data -- NOT a clinical or diagnostic device, NOT a
medical claim. Certification (IEC 62304 / ISO 13485 / regulatory) is the deploying company's responsibility;
the Southmedic offer stays OFF the public repo. Deterministic; receipt. Author: Peter Higgins (human authorship
for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,1e-9,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def aitch(a,b): return float(np.linalg.norm(clr(a)-clr(b)))

rng=np.random.default_rng(20260626)
N_VIEWS=14

# --- the survey: operator gives N random views of a scene with two features ---
# SPOT: the real object -- DARK (low amplitude) but COHERENT (fixed compositional signature across all views)
SPOT_SIG=closure([5.0,3.0,2.0]); SPOT_AMP=2.0
# BLOB: foreground clutter -- BRIGHT (high amplitude) but INCOHERENT (signature varies view to view)
BLOB_AMP=10.0
spot_views=[closure(SPOT_SIG*(1+0.03*rng.standard_normal(3))) for _ in range(N_VIEWS)]   # coherent
blob_views=[closure(np.abs(rng.standard_normal(3))+0.2) for _ in range(N_VIEWS)]          # incoherent

def coherence(views):                                   # 1 / (1 + mean pairwise Aitchison distance)
    d=[aitch(views[i],views[j]) for i in range(len(views)) for j in range(i+1,len(views))]
    return 1.0/(1.0+float(np.mean(d)))
coh_spot=coherence(spot_views); coh_blob=coherence(blob_views)

# naive vs Hs target selection
naive_target="BLOB (foreground)" if BLOB_AMP>SPOT_AMP else "SPOT"
hs_target="SPOT (determinized)" if coh_spot>coh_blob else "BLOB"
margin=round(coh_spot-coh_blob,3)

# --- PID lock + track: the determinized SPOT drifts (patient breathing); beam follows it ---
def spot_position(t): return 30.0+5.0*np.sin(0.25*t)+1.5*np.sin(0.07*t)   # object-space drift
Kp,Ki,Kd=0.6,0.05,0.15
beam=0.0; integ=0.0; prev=0.0; track_err=[]
for t in range(80):
    target=spot_position(t)
    err=target-beam; integ+=err; deriv=err-prev
    beam+=Kp*err+Ki*integ+Kd*deriv; prev=err
    if t>=20: track_err.append(abs(target-beam))           # measure after lock-in
rms_track=float(np.sqrt(np.mean(np.square(track_err))))

# --- governance / safety gate: autonomous vs report-to-operator ---
MARGIN_GATE=0.10; SAFE_RANGE=(0.0,100.0)
within_safe=bool(SAFE_RANGE[0]<=spot_position(79)<=SAFE_RANGE[1] and rms_track<3.0)
if margin>=MARGIN_GATE and within_safe:
    action="AUTONOMOUS LOCK+TRACK on the determinized SPOT (margin and safety envelope satisfied)"
    handoff="front-end autonomous within the certified envelope; operator may override (Breaker 16)"
else:
    action="REPORT TO OPERATOR: candidate located, confidence below gate -- operator confirms/corrects"
    handoff="human-in-the-loop"

checks={
 "naive_picks_the_loud_blob": bool("BLOB" in naive_target),
 "Hs_picks_the_determinized_spot": bool("SPOT" in hs_target),
 "coherence_separates_spot_from_blob": bool(coh_spot>coh_blob+0.05),
 "PID_locks_and_tracks": bool(rms_track<2.0),
}
verdict=("PROBE LOCKS THE RIGHT OBJECT: naive focus goes to the bright blob; Hs locks the determinized SPOT by "
         f"cross-view coherence (margin {margin}) and the PID tracks it (RMS {round(rms_track,3)}); the "
         "governance/safety gate sets autonomous-vs-operator.") if all(checks.values()) else "PROBE CHECK FAILED"

out={"_meta":{"tool":"probe_survey_lock.py","what":"operator-survey view-fusion -> determinized-object lock -> PID track -> governance gate",
              "verdict":verdict,"n_views":N_VIEWS},
     "target_selection":{"blob_amplitude":BLOB_AMP,"spot_amplitude":SPOT_AMP,
        "blob_cross_view_coherence":round(coh_blob,3),"spot_cross_view_coherence":round(coh_spot,3),
        "naive_amplitude_pick":naive_target,"Hs_coherence_pick":hs_target,"lock_margin":margin,
        "reading":"the loud blob is incoherent across the survey (clutter); the dark spot is invariant across views (the object) -> lock the spot, adjust the beam there"},
     "pid_lock_and_track":{"controller":"PID on the Hs read (P=error, I=dwell/views, D=motion)","rms_track_error":round(rms_track,3),
        "reading":"the determinized object drifts; the beam follows it deterministically"},
     "two_layer_architecture":{"Hs_sensor_layer":"fuse views -> determinized target -> course of action (lock/adjust/track)",
        "governance_safety_layer":action,"handoff":handoff,
        "certification":"the deploying company (Southmedic) carries IEC 62304 / ISO 13485 / regulatory; Hs supplies the deterministic, certification-READY core"},
     "checks":checks,
     "fence":("RESEARCH/QA demonstrator on SYNTHETIC data -- NOT clinical/diagnostic, NOT a medical claim. "
              "Certification is the deploying company's responsibility; the Southmedic offer stays OFF the public "
              "repo. Course of action is a RECOMMENDATION; the operator corrects/confirms and keeps the override "
              "(Breaker 16). Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(
    {"sel":out["target_selection"],"pid":out["pid_lock_and_track"],"checks":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]
if __name__=="__main__": print(json.dumps(out,indent=2))
