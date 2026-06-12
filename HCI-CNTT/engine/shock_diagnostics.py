"""CN-TT v4 — internal vs external shock differentiation (self-diagnostics / FDIR).
A central controller flags a data anomaly; CN-TT reports WHETHER it is EXTERNAL (the
observed world really changed) or INTERNAL (an instrument/component fault). The
discriminator is cross-channel COHERENCE on the shared carriers: independent channels
(multi-sensor / TMR / redundant charts) AGREE under an external shock, DISAGREE under
an internal fault (and the divergent channel isolates the failed component).
Requires >=2 independent channels; a single stream cannot self-distinguish (noted)."""
from __future__ import annotations
import numpy as np

def classify_shock(channel_clrs_now, consensus_prev=None, resid_threshold=0.5):
    """channel_clrs_now : (K, D) CLR of K independent observations of the same composition
    at this step. consensus_prev : (D,) previous consensus CLR (for shock magnitude).
    Returns the internal/external verdict + the faulty channel + the real shift magnitude."""
    C = np.asarray(channel_clrs_now, float)
    if C.ndim != 2 or C.shape[0] < 2:
        return {"class": "UNDETERMINED", "reason": "needs >=2 independent channels (no redundancy)",
                "n_channels": int(C.shape[0]) if C.ndim == 2 else 1}
    K, D = C.shape
    consensus = np.median(C, axis=0)                     # robust cross-channel consensus (voting)
    resid = np.linalg.norm(C - consensus, axis=1)        # each channel's disagreement
    max_resid = float(resid.max()); divergent = int(np.argmax(resid))
    shock_mag = float(np.linalg.norm(consensus - np.asarray(consensus_prev, float))) if consensus_prev is not None else None
    internal = max_resid > resid_threshold
    return {
        "class": "INTERNAL" if internal else "EXTERNAL",
        "verdict": ("instrument/component fault — one channel diverges" if internal
                    else "real environmental change — channels agree"),
        "incoherence_max_resid": max_resid,
        "resid_threshold": resid_threshold,
        "faulty_channel": divergent if internal else None,
        "channel_residuals": [float(x) for x in resid],
        "shock_magnitude": shock_mag,
        "n_channels": K,
        "consensus_clr": [float(x) for x in consensus],
    }
