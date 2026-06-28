#!/usr/bin/env python3
"""
The ground-state noise-cancellation principle — measured.

The RWA ground state (THE_GROUND_STATE.md): the barycentre (isotropic 4-pi radiation) is the
zero-information reference; the coherent departure from it carries the signal; coherence is the
engineered quantity. Read in ratios, this is COMMON-MODE REJECTION: any gain common to all parts
cancels in the log-ratio, exactly. That is the BTL "automatic noise cancellation by reciprocation"
designed into the audio years ago, and it is the same geometry that made the QAM telemetry robust.

This script proves and quantifies it:
  - clr(g * S) = clr(S) EXACTLY: common-mode multiplicative gain (level/distance/illumination/
    common interference) is rejected to machine precision.
  - reciprocation log(a/b) = -log(b/a): bidirectional, exact.
  - recursion (geometric-mean decimation): the signal survives coarse-graining (EITT face).
  - HONEST LIMIT: independent ADDITIVE noise is NOT cancelled -- only common-mode multiplicative.

Deterministic; hash-receipted. Author: Peter Higgins; AI-assisted per HUF-STD-001. Honest-broker.
"""
import hashlib, json, math
import numpy as np

rng = np.random.default_rng(11)
def clr(x): L = np.log(x); return L - L.mean(1, keepdims=True)


def main():
    T, D = 4000, 4
    t = np.arange(T) / T
    logits = np.stack([np.sin(2*np.pi*1.5*t), 0.7*np.sin(2*np.pi*0.8*t+1),
                       0.4*np.sin(2*np.pi*2.3*t+2), np.zeros(T)], 1)
    S = np.exp(logits); S = S / S.sum(1, keepdims=True)     # the coherent signal composition
    S_clr = clr(S)

    # common-mode multiplicative gain drift (the dominant real-world corruption)
    gain_dB = 20 * np.cumsum(rng.standard_normal(T)) / math.sqrt(T)
    g = 10 ** (gain_dB / 20)
    X_cm = g[:, None] * S

    clr_cm = clr(X_cm)
    cm_res_max = float(np.max(np.abs(clr_cm - S_clr)))
    cm_noise_var = float(np.var(gain_dB / 20 * math.log(10)))
    cm_res_var = float(np.var(clr_cm - S_clr))
    cm_rej_dB = 10 * math.log10(cm_noise_var / max(cm_res_var, 1e-300))

    # honest control: independent additive noise (NOT cancelled)
    X_add = np.clip(S + 0.02 * rng.standard_normal((T, D)), 1e-9, None)
    add_rms = float(np.sqrt(((clr(X_add) - S_clr) ** 2).mean()))

    # bidirectional reciprocation
    a, b = S[:, 0], S[:, 1]
    recip = float(np.max(np.abs(np.log(a/b) + np.log(b/a))))

    # recursion: geometric-mean decimation (EITT face)
    def gm(C):
        n = (len(C) // 2) * 2; P = C[:n].reshape(-1, 2, C.shape[1])
        m = np.exp(np.log(P).mean(1)); return m / m.sum(1, keepdims=True)
    Cd = S.copy(); steps = 0
    while len(Cd) > 8: Cd = gm(Cd); steps += 1
    ent = lambda C: float(-((C.mean(0)) * np.log(C.mean(0))).sum())
    ent_drift = abs(ent(S) - ent(Cd)) / ent(S)

    out = {
        "experiment": "ground_state_common_mode_rejection",
        "common_mode_multiplicative": {
            "injected_gain_swing_dB": round(float(gain_dB.max() - gain_dB.min()), 1),
            "clr_vs_true_signal_max_residual": cm_res_max,
            "common_mode_rejection_dB": round(cm_rej_dB, 1),
            "verdict": "common-mode multiplicative noise cancelled to machine precision (EXACT)"},
        "honest_limit_additive": {"after_closure_rms_clr": round(add_rms, 4),
            "note": "closure cancels common-mode MULTIPLICATIVE noise only; independent additive noise survives"},
        "bidirectional_reciprocation_residual": recip,
        "recursion_geomean_decimation": {"steps": steps, "entropy_drift_fraction": round(ent_drift, 5)},
    }
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
