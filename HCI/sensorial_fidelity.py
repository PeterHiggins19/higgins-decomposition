#!/usr/bin/env python3
"""
sensorial_fidelity.py -- "no perversion to the touch", made measurable. A sense-extension is only safe to
wire toward perception if what it delivers is FAITHFUL: the percept must not be silently distorted by the
hardware, and when fidelity cannot be guaranteed the system must FLAG or WITHHOLD -- never hand the cortex a
manufactured percept. This demonstrates the three guarantees the Hs trust layer (pole 3) gives a distributed
sensor field, on a toy 6-part spectral 'scene':

  1. OVERALL-GAIN INVARIANCE (the core 'no perversion'): a new sensor that is 50x more sensitive delivers the
     SAME percept -- the device's loudness/brightness does not alter the perceived STRUCTURE. (clr common-mode
     rejection; exact to machine precision.) This is what makes the read forward-compatible as hardware advances.
  2. PER-CHANNEL DRIFT IS DETECTED, NOT PASSED: per-channel mis-calibration DOES change the composition (honest
     scope -- clr cancels only the OVERALL gain). The system measures the drift and FLAGS it; corrected, the
     percept is restored exactly. Faithful-or-flagged, never silently perverted.
  3. HONEST WITHHOLD: on a degenerate/below-floor read the percept cannot be formed faithfully, so the gate
     WITHHOLDS (delivers nothing) rather than inventing one.

HONEST SCOPE: this is the TRUST LAYER demonstrated on synthetic signals -- NOT a neural interface, NOT a built
sense-extension, NOT a safety claim about any hardware. Any actual cortical/sensory coupling is far-future and
sits behind medical/safety/ethics gates far beyond this file. Deterministic; receipt. Author: Peter Higgins
(human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(v); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def aitch(a,b): return float(np.sqrt(np.sum((clr(a)-clr(b))**2)))     # Aitchison distance
def eff_dim(p): p=closure(p); H=-np.sum(p*np.log(p+1e-300)); return float(np.exp(H))

# the true scene (a 6-part spectral composition -- e.g. partials of a sound)
true = closure(np.array([8,5,3,2,1,0.6]))
def percept(meas): return clr(meas)                                   # the delivered read

# 1. overall-gain invariance: old hardware gain 1.0, new hardware 50x more sensitive
measA = 1.0*true
measB = 50.0*true
gain_invariance_residual = float(np.max(np.abs(percept(measA)-percept(measB))))

# 2. per-channel calibration drift on the new hardware (uncorrected), then corrected
cal = np.array([1.00,1.05,0.95,1.10,0.90,1.00])                       # per-channel response
measB_uncal = 50.0*true*cal
drift = aitch(measB_uncal, measA)                                     # honest: this DOES move the percept
DRIFT_FLAG_THR = 0.05
drift_flagged = bool(drift > DRIFT_FLAG_THR)                          # the system catches it
measB_corr = measB_uncal/cal                                          # apply characterized calibration
residual_after_correction = float(np.max(np.abs(percept(measB_corr)-percept(measA))))

# 3. honest withhold on a degenerate read (one part swamps; rest at structural-zero / sensor noise floor)
NOISE = 1e-6
degenerate = np.array([100.0, NOISE,NOISE,NOISE,NOISE,NOISE])
def deliver_or_withhold(meas, noise=NOISE):
    parts = closure(meas)
    # cannot faithfully form a percept if the structure collapses to ~1 part or rides the noise floor
    if eff_dim(parts) < 2.0 or np.sum(parts > 10*noise) < 2:
        return {"delivered": False, "reason": "below faithful-percept floor -> WITHHOLD (no manufactured percept)"}
    return {"delivered": True, "percept_eff_dim": round(eff_dim(parts),3)}
withhold_degenerate = deliver_or_withhold(degenerate)
deliver_normal = deliver_or_withhold(true)

results = {
 "1_overall_gain_invariance": {"new_hw_sensitivity_x": 50.0,
     "percept_residual": float(f"{gain_invariance_residual:.2e}"),
     "faithful": bool(gain_invariance_residual < 1e-12),
     "meaning": "device loudness/brightness does NOT alter perceived structure -> forward-compatible hardware"},
 "2_per_channel_drift": {"aitchison_drift": round(drift,4), "flag_threshold": DRIFT_FLAG_THR,
     "flagged_not_silently_passed": drift_flagged,
     "residual_after_calibration": float(f"{residual_after_correction:.2e}"),
     "restored_faithful": bool(residual_after_correction < 1e-12),
     "meaning": "per-channel cal DOES move the percept (honest); system detects+flags, correction restores it exactly"},
 "3_honest_withhold": {"degenerate": withhold_degenerate, "normal": deliver_normal,
     "meaning": "faithful-or-flagged-or-withheld: the cortex is never handed a manufactured percept"},
}
verdict = ("TRUST LAYER HOLDS: percept invariant to hardware gain, drift flagged not passed, degenerate read withheld"
           if (results["1_overall_gain_invariance"]["faithful"] and drift_flagged
               and results["2_per_channel_drift"]["restored_faithful"]
               and not withhold_degenerate["delivered"] and deliver_normal["delivered"])
           else "CHECK FAILED")

out = {"_meta": {"tool": "sensorial_fidelity.py",
                 "what": "'no perversion to the touch' -- the trust layer for a sense-extension, measured",
                 "verdict": verdict},
       "results": results,
       "fence": ("TRUST LAYER on synthetic signals only -- NOT a neural interface, NOT a built sense-extension, "
                 "NOT a hardware safety claim. clr cancels OVERALL gain, not per-channel cal (shown honestly). "
                 "Any cortical/sensory coupling is far-future behind medical/safety/ethics gates. The human "
                 "keeps the last breaker. Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"] = hashlib.sha256(
    json.dumps(results, sort_keys=True, default=str).encode()).hexdigest()[:16]

if __name__ == "__main__":
    print(json.dumps(out, indent=2))
