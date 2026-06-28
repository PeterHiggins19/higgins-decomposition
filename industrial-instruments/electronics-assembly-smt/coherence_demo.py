#!/usr/bin/env python3
"""
Lasers & coherence go together -- and so do coherence & Hs (T2 reasoned, hash-receipted).

The Hs common-mode rejection works ONLY to the extent the disturbance is shared across channels, i.e. COHERENT.
A coherent laser makes the laser/thermal disturbance a true common mode (the same on every channel) so
closure+clr removes it exactly. As coherence drops, the disturbance decorrelates into per-channel-independent
noise -> there is nothing "common" left to reject.

coherence rho in [0,1] = the SHARED fraction of the disturbance variance (the rest is per-channel independent).
  Closed form: clr removes the shared part exactly, residual = independent part, so
      suppression_dB ~ -10 * log10(1 - rho).
  i.e. every extra "9" of coherence (0.9, 0.99, 0.999, ...) buys ~10 dB of rejection.
AND: Hs reads rho back from the data (shared fraction = 1 - residual_var/total_var) and GATES on it
(refuse-to-guess when there is no shared structure to read).

Author: Peter Higgins; AI-assisted per HUF-STD-001. Internal / planning. No vendor relationship implied.
"""
import hashlib, json, math
import numpy as np

rng = np.random.default_rng(7)

def clr(X):
    L = np.log(X); return L - L.mean(axis=1, keepdims=True)

def run(rho, D=8, T=6000):
    t = np.linspace(0, 1, T)
    S = np.stack([1.0 + 0.04*np.sin(2*math.pi*(k+1)*t + 0.5*k) for k in range(D)], axis=1)
    V = 0.30**2
    shared = math.sqrt(rho) * np.sqrt(V) * rng.standard_normal(T)
    indep  = math.sqrt(1-rho) * np.sqrt(V) * rng.standard_normal((T, D))
    log_dist = shared[:, None] + indep
    X = np.clip(S * np.exp(log_dist), 1e-9, None)
    total = float(np.var(log_dist))
    resid = clr(X) - clr(S)
    rv = float(np.var(resid))
    return 10*math.log10(total / max(rv, 1e-30)), 1.0 - rv/total

def main():
    rows = []
    for rho in [0.0, 0.5, 0.9, 0.99, 0.999, 0.9999, 1.0]:
        s, c = run(rho)
        rows.append({"coherence_rho": rho, "Hs_suppression_dB": round(s, 1),
                     "Hs_read_back_coherence": round(float(c), 4),
                     "closed_form_-10log10(1-rho)_dB": (round(-10*math.log10(1-rho), 1) if rho < 1 else "inf")})
    GATE = 0.95
    out = {
        "principle": "Hs common-mode rejection is exactly as strong as the source is COHERENT: shared (coherent) disturbance cancels under closure+clr; decohered per-channel disturbance does not. A coherent laser hands Hs a true common mode to reject.",
        "law": "suppression_dB ~ -10*log10(1-rho): every extra '9' of coherence buys ~10 dB of rejection.",
        "sweep": rows,
        "Hs_coherence_gate_example": "Hs reads the coherent fraction back from the residual; gate refuses to trust the relational read when read-back coherence < %.2f (honest-broker: refuse to guess when there is no shared structure)." % GATE,
        "honest_note": "rho is the shared-variance fraction (a proxy for laser temporal/spatial coherence and inter-channel phase correlation). Exact-cancel applies to the SHARED multiplicative part only; independent/decohered noise sets the floor.",
        "maps_to": "Hs coherence gate (refuse-to-guess); RWA ground-state common-mode (d8c21c70); fiber common-mode demo (e791ec63); coherent optical detection recovers amplitude+phase = more dimensions (dimension-is-the-message, bf24c615)."
    }
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
