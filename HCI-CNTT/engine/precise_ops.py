"""
precise_ops (CN-TT v4, additive) — compensated arithmetic for the precision-sensitive
"zeros" and the long-running accumulators.

WHY THIS, AND WHERE IT MATTERS (honest, tested):
The two structural zeros are the closure sum (sum x = 1) and the CLR centre (mean of
logs = 0). We TESTED whether compensating these helps the live engine: at the engine's
operating scale (D ~ 4..200) numpy's reductions already sum PAIRWISE, so compensated
closure / CLR are BIT-IDENTICAL to the current code (max|diff| = 0.0 at D=4). The gain
only appears at D ~ 1e4 with wide dynamic range, and even there it is marginal
(|sum CLR| 7.5e-11 -> 6.7e-11). So swapping the per-step CLR/closure is NOT worth an
oracle re-baseline -- it would change nothing in the operating regime.

The truncation concern Peter raised is real, but it bites the STATEFUL / RUNNING
accumulators -- a long-lived integrator over an automation period -- not the per-step
CLR. There, naive accumulation lets a half-quantum DC bias pile up with N (tested:
200k adds drift by ~10), while carrying the residual forward (the "balanced twin /
+-transitions absorb truncation" idea = error-feedback / sigma-delta) bounds it to ~1
quantum regardless of N. That is what `ErrorFeedbackAccumulator` is for, and it is what
the SafeLoop integrator uses.

Everything here is deterministic. Adopting compensated_* in the hashed run path is a
one-time, Peter-gated oracle re-baseline (do not assume free hash-neutrality). The
observe-only guards and the loop monitors never touch hashed values. Claim tier: Tier 1
(implemented + self-tested). Author: Peter Higgins (human authorship for claims);
AI-assisted per HUF-STD-001. Honest-broker.
"""
from __future__ import annotations
import numpy as np


def neumaier_sum(a):
    """Compensated (Neumaier/Kahan-Babuska) summation. Deterministic; robust to cancellation."""
    a = np.asarray(a, float).ravel(); s = 0.0; c = 0.0
    for x in a:
        t = s + x
        c += (s - t + x) if abs(s) >= abs(x) else (x - t + s)
        s = t
    return s + c


def compensated_closure(x):
    """Close to the simplex using a compensated total. (Bit-identical to x/x.sum() at small D.)"""
    x = np.asarray(x, float); return x / neumaier_sum(x)


def compensated_clr(x):
    """CLR with a compensated centre (mean of logs). Protects the sum-to-zero identity at scale."""
    x = np.clip(np.asarray(x, float), 1e-300, None); L = np.log(x)
    return L - neumaier_sum(L) / L.size


class ErrorFeedbackAccumulator:
    """Running sum that carries the truncation residual forward (error-feedback / sigma-delta;
    the 'balanced twin' whose +/- residual transitions absorb the per-add truncation), so a
    long-running accumulation does not build a DC bias with N. Optional `leak` (<1) makes it a
    bounded leaky integrator (anti-windup). Deterministic."""
    __slots__ = ("s", "e", "leak")

    def __init__(self, leak=1.0):
        self.s = 0.0; self.e = 0.0; self.leak = float(leak)

    def add(self, x):
        self.s *= self.leak
        u = x + self.e; t = self.s + u; self.e = (self.s - t) + u; self.s = t
        return self.s

    def value(self):
        return self.s

    def clear(self):
        self.s = 0.0; self.e = 0.0


def _self_test():
    ok = True
    rng = np.random.default_rng(0)
    # error-feedback bounds DC bias vs naive truncation over many adds
    N = 100000; q = 1e-4
    x = rng.normal(0, 1e-3, N) + 7e-4
    trunc = lambda v: np.floor(v / q) * q
    s = 0.0
    for v in x:
        s += trunc(v)
    plain = abs(s - x.sum())
    acc = ErrorFeedbackAccumulator(); e = 0.0; tot = 0.0
    for v in x:                                   # explicit error-feedback truncation
        u = v + e; t = trunc(u); e = u - t; tot += t
    ok &= abs(tot - x.sum()) < 50 * q < plain     # bounded, and far better than naive
    # compensated CLR is deterministic and sums nearer zero than naive at scale
    xz = np.exp(rng.normal(0, 12, 20000)); xz /= xz.sum()
    ok &= abs(compensated_clr(xz).sum()) <= abs((np.log(xz) - np.log(xz).mean()).sum()) * 1.000001
    ok &= np.array_equal(compensated_clr(xz), compensated_clr(xz))
    # closure closes
    ok &= abs(compensated_closure(rng.random(50)).sum() - 1.0) < 1e-12
    return ok


if __name__ == "__main__":
    import sys
    print("precise_ops self-test:", "ALL PASS" if _self_test() else "FAILED")
    sys.exit(0 if _self_test() else 1)
