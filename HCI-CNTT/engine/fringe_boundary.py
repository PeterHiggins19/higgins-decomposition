"""
fringe_boundary (CN-TT v4, additive, EXPLORATORY) — the boundary/fringe engine seed.

The deterministic instrument (foreground) reports what it can resolve with confidence, and
HOLDS at its limit. This module is the BACKGROUND, exploratory layer that looks at the EDGE
— where the instrument holds/withholds — for fringe patterns, using the old tools (EITT and
the frozen oracle's attractor/IR-class + transcendental-basin proximity). It is **Tier 3 /
exploratory**: clues on the fringe of understanding, NEVER used for claims. Quarantined by
design (the transcendental-constant cluster was set aside as likely coincidence; this layer
is where such pattern-of-patterns exploration lives, clearly labelled).

EITT-as-boundary-test (the new role for an old tool): Shannon entropy is ~invariant under
geometric-mean (CoDa-correct) temporal decimation when the composition has coherent
structure; it DRIFTS when the region is structureless/white — so a large entropy drift flags
a BOUNDARY of analysable structure (the edge where the deterministic read runs out).

Hooks (Tier 3): the frozen-oracle binary additionally offers an attractor/IR-class character
read and a transcendental-basin proximity at the boundary — call the oracle (`HCI-CNT/engine/
cnt.py`) for those; they are exploratory fringe clues, not engine outputs.

Additive, observe-only, oracle untouched. Author: Peter Higgins (human authorship for claims);
AI-assisted per HUF-STD-001. Honest-broker; this whole module is Tier-3 fringe by construction.
"""
from __future__ import annotations
import numpy as np


def _closure(P):
    P = np.clip(np.asarray(P, float), 1e-12, None); return P / P.sum(1, keepdims=True)


def _shannon_mean(P):
    P = _closure(P); return float(-(P * np.log(P)).sum(1).mean())


def _geomean_decimate(P, k):
    P = _closure(P); T = (len(P) // k) * k; G = []
    for i in range(0, T, k):
        g = np.exp(np.log(P[i:i + k]).mean(0)); G.append(g / g.sum())
    return np.array(G) if G else P[:1]


def eitt_boundary(P, levels=(1, 2, 4), drift_gate=0.01):
    """EITT entropy-invariance as a boundary test. Returns the entropy by decimation level,
    the relative drift, and a verdict: within-regime (structure holds) vs BOUNDARY (the edge
    of analysable structure — entropy not invariant under geometric-mean decimation)."""
    H = [_shannon_mean(_geomean_decimate(P, k)) for k in levels if len(P) // k >= 2]
    drift = (max(H) - min(H)) / (abs(np.mean(H)) + 1e-12) if H else 0.0
    return {"entropy_by_level": [round(h, 4) for h in H], "relative_drift": round(drift, 4),
            "code": None if drift < drift_gate else "FR-BND-INF",
            "verdict": "within-regime (EITT holds; coherent structure)" if drift < drift_gate
                       else "BOUNDARY (entropy not invariant under decimation; edge of analysable structure)",
            "tier": "Tier 3 / exploratory fringe -- a clue, never a claim"}


def _self_test():
    ok = True; rng = np.random.default_rng(0)
    # structured drift -> within-regime
    t = np.linspace(0, 1, 32); c0 = np.array([.5, .3, .15, .05]); c1 = np.array([.1, .2, .3, .4])
    P = np.exp(np.outer(1 - t, np.log(c0)) + np.outer(t, np.log(c1))); P /= P.sum(1, keepdims=True)
    ok &= eitt_boundary(P)["code"] is None
    # white composition -> BOUNDARY
    ok &= eitt_boundary(_closure(rng.random((32, 6))))["code"] == "FR-BND-INF"
    return ok


if __name__ == "__main__":
    import sys
    print("fringe_boundary self-test:", "ALL PASS" if _self_test() else "FAILED")
    sys.exit(0 if _self_test() else 1)
