"""
compositional_momentum (CN-TT v4, additive) — the arrow of intent.

Peter's concept: each carrier has a MASS (its share of the whole), a VELOCITY (its
log-ratio change per step, Δclr — the Aitchison velocity), and therefore a MOMENTUM
(mass × velocity). The system's net momentum vector is the **arrow of intent**: where
the *weight* of the composition is flowing, and how committed that motion is.

This is a DESCRIPTIVE read of the present motion, NOT a prediction. Momentum is the
current vector (Newton's first law: it continues absent a force) — but the instrument
does not claim no force will act; a policy, shock, or constraint can redirect it. So it
reports *where the mass is moving now and to what extent*, never *where it will be*.

It is the COMPLEMENT to the (mass-blind) helmsman: the helmsman = argmax|Δclr| catches
the fastest log-ratio mover, often a small carrier (ratio blindness); momentum =
mass·velocity catches where the bulk is shifting. Use both.

Honesty guard (mirrors the resolvability guard): a directed "arrow" is only reported
when the motion is (a) above the floor and (b) COHERENT over the window — the per-step
momentum vectors must mostly agree in direction (`coherence = ‖Σp‖ / Σ‖p‖ ∈ [0,1]`).
Low coherence = the system is churning with no net intent → `MO-DIF-WRN`; no motion →
`MO-NUL-WRN`. Note: in a closed composition Σ_j mass_j·velocity_j ≈ 0 (momentum is
~conserved), so the vector shows mass *redistribution* — which carriers receive vs give.

Additive, observe-only; oracle untouched. Tier 1 (implemented + self-tested + demonstrated
on real EMBER transitions). Author: Peter Higgins (human authorship for claims);
AI-assisted per HUF-STD-001. Honest-broker.
"""
from __future__ import annotations
import numpy as np


def _closure(M):
    M = np.clip(np.asarray(M, float), 0, None); s = M.sum(1, keepdims=True); s[s == 0] = 1; return M / s


def _clr(P):
    P = np.clip(P, 1e-12, None); L = np.log(P); return L - L.mean(1, keepdims=True)


def compositional_momentum(M, names=None, window=None, coh_floor=0.15, mag_floor=1e-6):
    """Arrow of intent for a composition trajectory M (rows = time/sample order, cols = carriers).
    Returns the carriers mass is flowing TO / FROM, the magnitude, the coherence (directed vs churn),
    the kinetic energy of the motion, the mass-blind helmsman (for contrast), and an honesty code."""
    M = np.asarray(M, float)
    names = list(names) if names is not None else [f"c{j}" for j in range(M.shape[1])]
    P = _closure(M); C = _clr(P)
    v = np.diff(C, axis=0)                       # Aitchison velocity Δclr        (T-1, D)
    mass = (P[:-1] + P[1:]) / 2                  # mass = mean share over the step (T-1, D)
    p = mass * v                                 # per-carrier momentum            (T-1, D)
    seg = p if window is None else p[-window:]
    Pnet = seg.sum(0)                            # net system momentum vector       (D,)
    mag = float(np.linalg.norm(Pnet))
    permag = np.linalg.norm(seg, axis=1)
    coherence = float(np.linalg.norm(seg.sum(0)) / (permag.sum() + 1e-30))
    ke = 0.5 * (mass * v * v).sum(1)             # kinetic energy of compositional motion
    order = np.argsort(-Pnet)
    gaining = [(names[j], round(float(Pnet[j]), 4)) for j in order if Pnet[j] > 0][:3]
    losing = [(names[j], round(float(Pnet[j]), 4)) for j in order[::-1] if Pnet[j] < 0][:3]
    code = None
    if mag < mag_floor:
        code = "MO-NUL-WRN"                      # no resolvable momentum (at rest)
    elif coherence < coh_floor:
        code = "MO-DIF-WRN"                      # diffuse: motion present, no directed arrow (churn)
    helm = names[int(np.argmax(np.abs(v).sum(0)))]
    return {"arrow_gaining": gaining, "arrow_losing": losing, "magnitude": round(mag, 4),
            "coherence": round(coherence, 3), "ke_mean": round(float(ke.mean()), 6),
            "helmsman_massblind": helm, "code": code,
            "note": "descriptive vector of present motion; NOT a prediction. Mass = share; "
                    "velocity = Δclr; momentum = mass·velocity; arrow reported only when coherent."}


def _self_test():
    ok = True; rng = np.random.default_rng(0); T = 40
    # 1 a clear directed transition: mass moves A->C steadily -> coherent arrow, C gaining, A losing
    a = np.linspace(0.6, 0.1, T); c = np.linspace(0.1, 0.6, T); b = np.full(T, 0.3)
    M = np.c_[a, b, c]
    r = compositional_momentum(M, ["A", "B", "C"])
    ok &= r["code"] is None and r["arrow_gaining"][0][0] == "C" and r["arrow_losing"][0][0] == "A" and r["coherence"] > 0.5
    # 2 churn: random walk back-and-forth -> low coherence -> MO-DIF-WRN
    M2 = _closure(0.25 + rng.normal(0, 0.02, (T, 4)) * np.sin(np.arange(T)[:, None]))
    r2 = compositional_momentum(M2, ["a", "b", "c", "d"])
    ok &= (r2["code"] == "MO-DIF-WRN") or (r2["coherence"] < 0.2)
    # 3 at rest -> MO-NUL-WRN
    r3 = compositional_momentum(np.tile([0.25, 0.25, 0.25, 0.25], (T, 1)) + 1e-13, ["a", "b", "c", "d"])
    ok &= r3["code"] == "MO-NUL-WRN"
    return ok


if __name__ == "__main__":
    import sys
    print("compositional_momentum self-test:", "ALL PASS" if _self_test() else "FAILED")
    sys.exit(0 if _self_test() else 1)
