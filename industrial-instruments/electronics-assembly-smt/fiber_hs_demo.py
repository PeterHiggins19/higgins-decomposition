#!/usr/bin/env python3
"""
Fiber-optic + Hs demonstration (physics-grounded model; T2 reasoned, hash-receipted). Planning anchor for the
future-projects case: a multi-channel fiber sensor readout (FBG / WDM array, D channels) carries

  - per-channel true signal  s_i(t)          (strain / temperature at D points along the fiber)
  - a SHARED multiplicative common-mode g(t)  (laser-power droop + bulk temperature + connector-loss step)
  - small per-channel additive noise          (detector / shot noise)

Classic ratiometric / referenced fiber sensing rejects common-mode with ONE reference channel. Hs rejects it
across ALL D channels at once: closure + clr -> clr(g*x) = clr(x), exact. Same principle as the RWA ground-state
noise cancellation and the Hs 313 dB common-mode anchor -- here in glass.

Honest: the shared MULTIPLICATIVE common-mode cancels to the numerical floor; independent ADDITIVE detector
noise does NOT cancel and sets the residual floor. The CMRR figure is for the common-mode (multiplicative) part
-- which is the dominant real fiber disturbance (laser power, bulk temperature, connector loss).

Author: Peter Higgins; AI-assisted per HUF-STD-001. Internal / planning. No vendor relationship implied.
"""
import hashlib, json, math
import numpy as np

rng = np.random.default_rng(24)

def clr(X):
    L = np.log(X); return L - L.mean(axis=1, keepdims=True)

def main():
    D, T = 8, 4000
    t = np.linspace(0, 1, T)
    S = np.stack([1.0 + 0.05*np.sin(2*math.pi*(k+1)*t + k) for k in range(D)], axis=1)  # T x D, all > 0
    g = (1.0 - 0.40*t + 0.15*np.sin(2*math.pi*0.5*t) - 0.10*(t > 0.6))                  # shared common-mode
    Xclean = S * g[:, None]
    add = 0.002 * rng.standard_normal((T, D))
    X = np.clip(Xclean + add, 1e-6, None)

    raw_cm_amp  = float(np.std(g))
    raw_sig_amp = float(np.mean(np.std(S, axis=0)))
    raw_cmrr_dB = 20*math.log10(raw_cm_amp / raw_sig_amp)

    C = clr(X); C_ref = clr(S)
    leak = float(np.std(clr(Xclean) - C_ref))
    resid_with_noise = float(np.std(C - C_ref))
    cmrr_mult_dB = 20*math.log10(raw_cm_amp / max(leak, 1e-18))

    true_lr  = np.log(S[:, 0]) - np.log(S[:, 1])
    raw_lr   = np.log(X[:, 0]) - np.log(X[:, 1])
    abs_read = np.log(X[:, 0])
    err_relational = float(np.std(raw_lr - true_lr))
    err_absolute   = float(np.std(abs_read - np.log(S[:, 0])))

    out = {
        "model": "D=8 FBG/WDM fiber sensor array; shared multiplicative common-mode (laser droop + thermal + connector step) + small additive noise",
        "common_mode_disturbance_amp": round(raw_cm_amp, 4),
        "true_signal_amp_per_channel": round(raw_sig_amp, 4),
        "raw_absolute_read": {
            "disturbance_above_signal_dB": round(raw_cmrr_dB, 1),
            "single_channel_abs_read_error_std": round(err_absolute, 4)
        },
        "Hs_clr_read": {
            "multiplicative_common_mode_leakage_std": leak,
            "common_mode_rejection_multiplicative_dB": round(cmrr_mult_dB, 1),
            "residual_with_additive_noise_std": round(resid_with_noise, 5),
            "relational_two_FBG_read_error_std": round(err_relational, 6)
        },
        "honest_note": "Shared MULTIPLICATIVE common-mode (laser power, bulk temperature, connector loss) cancels to the numerical floor under closure+clr (clr(g*x)=clr(x)). Independent ADDITIVE detector noise does NOT cancel and sets the residual floor. CMRR is for the common-mode (multiplicative) part -- the dominant real fiber disturbance.",
        "maps_to": "RWA ground-state / Hs common-mode rejection (313 dB numerical anchor, d8c21c70); deterministic denoise subspace (cb0c3f52); dimension-is-the-message for mode/wavelength shares (bf24c615); 6-DOF for fiber pose / active alignment (SO4 module)."
    }
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
