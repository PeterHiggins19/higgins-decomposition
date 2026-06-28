"""
Helmsman resolvability guard (CN-TT v4, additive) — engine blind-spot kill-test fix.

The helmsman = argmax_i |Delta CLR_i| has two structural blind spots that are
properties of the ENGINE, not the data:

  * BLIND SPOT 1 — near the barycentre (a uniform / unchanging composition), the
    step motion is at the numerical floor (~1e-9), so argmax returns a "leader" that
    is pure numerical noise (it changes with the random seed). The engine names a
    confident helmsman where there is no resolvable motion.
  * BLIND SPOT 3 — when two carriers move identically (a tie), argmax breaks the tie
    by column index, silently and arbitrarily.

This guard fixes both by reporting RESOLVABILITY: it returns the helmsman, OR None
(no resolvable motion -> HM-NUL-WRN), OR 'TIE' (leader not separated from the runner-
up -> HM-TIE-WRN), with the motion magnitude and the margin to the runner-up. It never
names a leader at rest, and never breaks a tie silently.

It also carries the honest note for BLIND SPOT 2 — CLR subcompositional INCOHERENCE:
the CLR helmsman is relative to the DECLARED carrier set (adding/removing a carrier
shifts the CLR centre and can change the read), so cross-carrier-set comparison must
use ILR balances, not CLR. (Demonstrated: helmsman of (A,B,C) = A alone, but C once an
irrelevant carrier D is added. See experiments/engine_killtest_2026-06/.)

Additive: the frozen oracle and the existing helmsman.py are untouched. Claim tier:
Tier 1 — implemented + self-tested. Author: Peter Higgins (human authorship for
claims); AI-assisted per HUF-STD-001. Honest-broker.
"""
from __future__ import annotations
import numpy as np


def _clr(P):
    P = np.clip(np.asarray(P, float), 1e-300, None); L = np.log(P)
    return L - L.mean(1, keepdims=True)


def helmsman_guard(P, carriers=None, motion_floor=1e-6, tie_rel=1e-3):
    """
    Resolvable helmsman read for a composition trajectory P (rows=time, cols=carriers).
    Returns a dict: helmsman (carrier | None | 'TIE'), magnitude, margin, code, and the
    subcompositional-coherence note.
      - motion below `motion_floor` (total |dCLR| of the leader) -> None, HM-NUL-WRN.
      - leader margin to runner-up <= tie_rel*magnitude -> 'TIE', HM-TIE-WRN.
    """
    dH = np.diff(_clr(P), axis=0); total = np.abs(dH).sum(0)
    order = np.argsort(-total); lead = int(order[0]); runner = int(order[1]) if len(order) > 1 else lead
    mag = float(total[lead]); margin = float(total[lead] - total[runner])
    helm, code = lead, None
    if mag < motion_floor:
        helm, code = None, "HM-NUL-WRN"           # at/near barycentre: no resolvable helmsman
    elif margin <= tie_rel * mag:
        helm, code = "TIE", "HM-TIE-WRN"          # leader not separated from runner-up
    name = (lambda i: carriers[i]) if carriers is not None else (lambda i: i)
    return {"helmsman": name(helm) if isinstance(helm, int) else helm,
            "magnitude": mag, "margin": margin, "code": code,
            "subcompositional_note": "CLR helmsman is relative to the DECLARED carrier set "
            "(not coherent under add/remove of carriers); for cross-set comparison use ILR balances."}


def _self_test():
    ok = True; T, D = 24, 5
    for s in (1, 2, 3):                            # barycentre -> None
        P = np.ones((T, D)) / D + np.random.default_rng(s).normal(0, 1e-11, (T, D))
        P = np.clip(P, 1e-12, None); P /= P.sum(1, keepdims=True)
        r = helmsman_guard(P); ok &= (r["helmsman"] is None and r["code"] == "HM-NUL-WRN")
    P = np.full((T, 5), 0.2); P[:, 0] = np.linspace(0.2, 0.45, T); P[:, 1] = np.linspace(0.2, 0.10, T)
    P = np.clip(P, 1e-6, None); P /= P.sum(1, keepdims=True)
    r = helmsman_guard(P); ok &= (r["helmsman"] == 0 and r["code"] is None)          # clear winner
    P = np.zeros((T, 6)); P[:, 0] = np.linspace(0.30, 0.02, T); P[:, 1] = P[:, 0].copy()
    for j in range(2, 6):
        P[:, j] = np.linspace(0.10, 0.24, T)
    P = np.clip(P, 1e-6, None); P /= P.sum(1, keepdims=True)
    r = helmsman_guard(P); ok &= (r["helmsman"] == "TIE" and r["code"] == "HM-TIE-WRN")  # tie
    return ok


if __name__ == "__main__":
    import sys
    print("helmsman_guard self-test:", "ALL PASS" if _self_test() else "FAILED")
    sys.exit(0 if _self_test() else 1)
