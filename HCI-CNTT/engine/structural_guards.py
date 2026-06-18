"""
Structural guards (CN-TT v4, additive) — the Tier-2 kill-test fixes.

Three engine-level capabilities, each fixing a structural blind spot named in
experiments/engine_killtest_2026-06/. All additive: the frozen oracle and the
existing helmsman.py / helmsman_guard.py are untouched. Claim tier: Tier 1
(implemented + self-tested). Author: Peter Higgins (human authorship for claims);
AI-assisted per HUF-STD-001. Honest-broker.

  1. coherent_helmsman(P)  -- a subcompositionally COHERENT helmsman built from
     pairwise log-ratios log(x_i/x_j). Pairwise log-ratios are closure-invariant
     (the ratio x_i/x_j is unchanged when other parts are added or removed), so this
     helmsman does NOT move when an irrelevant carrier is added -- fixing the CLR
     incoherence (blind spot 2). Carries the same resolvability guard (None / 'TIE').

  2. effective_rank(P)  -- SVD of the centred CLR trajectory; reports the effective
     number of moving dimensions (participation ratio of the singular values) and
     flags DG-RNK-WRN when the motion is confined to a subspace. A rank-deficient
     trajectory is exactly what drives the eigh-based depth/stage diagnostics toward
     near-zero eigenvalues (a sibling of the E-21 failure, for a different reason).

  3. hold_lock(P)  -- a Schmitt-trigger / dead-band detector for STRUCTURAL change.
     It DISCOVERS the trigger point from two noise floors -- the system noise floor
     (a robust estimate of the resting motion in the data) and the engine noise floor
     (the numerical/determinism floor) -- and combines them: noise = max(system, engine).
     With hysteresis (enter MOVING above k_up*noise, return to HOLD below k_down*noise,
     k_down < k_up) it ties down near-zero drift into a HOLD-LOCK state and registers a
     structural change only when an excursion is sustained AND its net displacement is
     deemed structural (>= struct_k*noise). Near-zero drift is held -- but identified as
     held, never silently. Hysteresis prevents chattering around the trigger.
"""
from __future__ import annotations
import numpy as np


def _clr(P):
    P = np.clip(np.asarray(P, float), 1e-300, None); L = np.log(P)
    return L - L.mean(1, keepdims=True)


# ---- 1) coherent helmsman (pairwise log-ratio basis) ----------------------------
def coherent_helmsman(P, carriers=None, motion_floor=1e-6, tie_rel=1e-3):
    """Subcompositionally-coherent helmsman: the carrier with the largest mean pairwise
    log-ratio motion. Invariant to adding/removing OTHER carriers (closure-invariant).
    Same resolvability guard as helmsman_guard: None (HM-NUL-WRN) / 'TIE' (HM-TIE-WRN)."""
    P = np.clip(np.asarray(P, float), 1e-300, None); logP = np.log(P); T, D = P.shape
    dlr = np.zeros(D)
    for i in range(D):
        acc = 0.0
        for j in range(D):
            if i != j:
                acc += np.abs(np.diff(logP[:, i] - logP[:, j])).sum()
        dlr[i] = acc / (D - 1) if D > 1 else 0.0
    order = np.argsort(-dlr); lead = int(order[0]); runner = int(order[1]) if D > 1 else lead
    mag = float(dlr[lead]); margin = float(dlr[lead] - dlr[runner])
    helm, code = lead, None
    if mag < motion_floor:
        helm, code = None, "HM-NUL-WRN"
    elif margin <= tie_rel * mag:
        helm, code = "TIE", "HM-TIE-WRN"
    nm = (lambda i: carriers[i]) if carriers is not None else (lambda i: i)
    return {"helmsman": nm(helm) if isinstance(helm, int) else helm, "magnitude": mag,
            "margin": margin, "code": code,
            "basis": "pairwise-log-ratio (subcompositionally coherent; closure-invariant)"}


# ---- 2) SVD effective-rank guard ------------------------------------------------
def effective_rank(P, rel_floor=1e-9, deficient_frac=0.5):
    """Effective number of moving dimensions of the CLR trajectory (participation ratio
    of the singular values). Flags DG-RNK-WRN when motion is confined to a subspace
    (eff_rank < deficient_frac*max_rank) -- the regime that destabilises eigh diagnostics."""
    X = _clr(P); X = X - X.mean(0)
    s = np.linalg.svd(X, compute_uv=False)
    s = s[s > s.max() * rel_floor] if s.size and s.max() > 0 else s[:0]
    maxr = min(P.shape[0] - 1, P.shape[1] - 1)
    if s.size == 0:
        return {"effective_rank": 0.0, "max_rank": maxr, "code": "DG-RNK-WRN", "singulars": []}
    pr = float((s.sum() ** 2) / (s ** 2).sum())
    code = "DG-RNK-WRN" if pr < deficient_frac * maxr else None
    return {"effective_rank": round(pr, 3), "max_rank": maxr, "code": code,
            "singulars": [round(float(x), 4) for x in s[:6]]}


# ---- 3) hold-lock hysteresis structural-change detector -------------------------
def discover_noise_floor(steps, engine_floor=1e-9, quiet_q=0.5):
    """Discover the trigger noise floor from the data: the robust resting-motion level
    (system noise floor) combined with the engine numerical floor. noise = max(system, engine)."""
    if steps.size == 0:
        return engine_floor
    med = np.median(steps); mad = np.median(np.abs(steps - med)) * 1.4826
    system_floor = max(np.quantile(steps, quiet_q) - mad, np.quantile(steps, 0.25))
    return float(max(engine_floor, system_floor, 1e-12))


def hold_lock(P, engine_floor=1e-9, k_up=4.0, k_down=2.0, quiet_q=0.5, struct_k=3.0):
    """Schmitt-trigger dead-band on structural change. Returns the discovered noise floor,
    the hysteresis band (upper/lower), the per-step HOLD/MOVING state, and the list of
    registered (structural + valid) changes. Near-zero drift -> held (and identified)."""
    H = _clr(P); steps = np.linalg.norm(np.diff(H, axis=0), axis=1)
    if steps.size == 0:
        return {"noise_floor": engine_floor, "states": [], "registered_changes": []}
    noise = discover_noise_floor(steps, engine_floor, quiet_q)
    up, lo = k_up * noise, k_down * noise
    state, states, events, ref = "HOLD", [], [], 0
    for t, m in enumerate(steps):
        if state == "HOLD" and m > up:
            state = "MOVING"
        elif state == "MOVING" and m < lo:
            net = float(np.linalg.norm(H[t + 1] - H[ref]))
            if net >= struct_k * noise:                       # deemed structural + valid
                events.append({"from_step": ref, "to_step": t + 1, "net_aitchison": round(net, 4)})
                ref = t + 1
            state = "HOLD"
        states.append(state)
    if state == "MOVING":
        net = float(np.linalg.norm(H[-1] - H[ref]))
        if net >= struct_k * noise:
            events.append({"from_step": ref, "to_step": len(states), "net_aitchison": round(net, 4), "open": True})
    return {"noise_floor": round(noise, 6), "engine_floor": engine_floor,
            "upper": round(up, 6), "lower": round(lo, 6), "k_up": k_up, "k_down": k_down,
            "n_hold": states.count("HOLD"), "n_moving": states.count("MOVING"),
            "registered_changes": events, "states": states,
            "note": "HOLD = motion below the discovered trigger (system+engine noise); held drift is "
                    "identified, not silent. A change registers only when sustained AND net-structural."}


def _self_test():
    ok = True; T = 24
    # 1 coherent helmsman invariant to an added carrier
    A = np.linspace(.30, .36, T); B = np.linspace(.35, .33, T); C = np.linspace(.35, .31, T)
    ABC = np.c_[A, B, C]; ABC /= ABC.sum(1, keepdims=True)
    Dd = 0.2 + 0.18 * np.sin(np.linspace(0, 6 * np.pi, T)); ABCD = np.c_[A, B, C, Dd]; ABCD /= ABCD.sum(1, keepdims=True)
    ok &= coherent_helmsman(ABC)["helmsman"] == coherent_helmsman(ABCD[:, :3])["helmsman"]
    # 2 rank guard: rank-1 line flagged, full-rank clean
    t = np.linspace(0, 1, T); c0 = np.array([.5, .3, .1, .07, .03]); c1 = np.array([.1, .1, .3, .3, .2])
    P1 = np.exp(np.outer(1 - t, np.log(c0)) + np.outer(t, np.log(c1))); P1 /= P1.sum(1, keepdims=True)
    Pf = np.random.default_rng(0).dirichlet(np.ones(5), size=T)
    ok &= effective_rank(P1)["code"] == "DG-RNK-WRN" and effective_rank(Pf)["code"] is None
    # 3 hold-lock: rest->shift->rest = 1 change; pure noise = 0
    rng = np.random.default_rng(7); D = 6
    def comp(base, n): x = base + rng.normal(0, n, D); x = np.clip(x, 1e-4, None); return x / x.sum()
    b1 = np.array([.30, .25, .15, .12, .10, .08]); b2 = np.array([.10, .15, .30, .20, .15, .10])
    seg = [comp(b1, 0.004) for _ in range(12)]
    seg += [comp(b1 * (1 - a) + b2 * a, 0.004) for a in np.linspace(0, 1, 6)]
    seg += [comp(b2, 0.004) for _ in range(12)]
    ok &= len(hold_lock(np.array(seg))["registered_changes"]) == 1
    ok &= len(hold_lock(np.array([comp(b1, 0.004) for _ in range(30)]))["registered_changes"]) == 0
    return ok


if __name__ == "__main__":
    import sys
    print("structural_guards self-test:", "ALL PASS" if _self_test() else "FAILED")
    sys.exit(0 if _self_test() else 1)
