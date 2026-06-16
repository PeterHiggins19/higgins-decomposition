#!/usr/bin/env python3
"""
Engine kill-test — structural blind spots of the helmsman read (break it), and the fix.

These are properties of the ENGINE (the CLR + argmax helmsman definition), not the
data. Each is demonstrated, then fixed by HCI-CNTT/engine/helmsman_guard.py.

  1. Near the barycentre, the helmsman is numerical NOISE (a different "leader" per seed).
  2. CLR is subcompositionally INCOHERENT: adding an irrelevant carrier changes the read.
  3. Exact ties are broken arbitrarily by column index.

Run: python blind_spots_demo.py   (deterministic). Author: Peter Higgins (human
authorship for claims); AI-assisted per HUF-STD-001. Honest-broker; claim tiers in RESULTS.md.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "HCI-CNTT", "engine")))
from helmsman_guard import helmsman_guard
from structural_guards import coherent_helmsman, effective_rank, hold_lock


def clr(P):
    P = np.clip(P, 1e-300, None); L = np.log(P); return L - L.mean(1, keepdims=True)


def naive_helmsman(P, cols=None):
    m = np.abs(np.diff(clr(P), axis=0))
    if cols is not None:
        m = m[:, cols]
    return int(np.argmax(m.sum(0)))


def main():
    T = 24
    print("BLIND SPOT 1 — near barycentre, naive helmsman is noise; guard says None:")
    for s in (1, 2, 3, 4):
        P = np.ones((T, 5)) / 5 + np.random.default_rng(s).normal(0, 1e-11, (T, 5))
        P = np.clip(P, 1e-12, None); P /= P.sum(1, keepdims=True)
        print(f"  seed {s}: naive -> carrier {naive_helmsman(P)} | guard -> {helmsman_guard(P)['helmsman']} ({helmsman_guard(P)['code']})")

    print("\nBLIND SPOT 2 — CLR subcompositional incoherence (adding a carrier changes the read):")
    A = np.linspace(.30, .36, T); B = np.linspace(.35, .33, T); C = np.linspace(.35, .31, T)
    ABC = np.c_[A, B, C]; ABC /= ABC.sum(1, keepdims=True)
    Dd = 0.2 + 0.18 * np.sin(np.linspace(0, 6 * np.pi, T))
    ABCD = np.c_[A, B, C, Dd]; ABCD /= ABCD.sum(1, keepdims=True)
    print(f"  helmsman of (A,B,C) alone            : {'ABC'[naive_helmsman(ABC)]}")
    print(f"  helmsman of (A,B,C) inside (A,B,C,D)  : {'ABC'[naive_helmsman(ABCD, cols=[0,1,2])]}  (D is irrelevant)")
    print(f"  guard note: {helmsman_guard(ABCD)['subcompositional_note']}")

    print("\nBLIND SPOT 3 — identical movers (tie); guard says TIE instead of an arbitrary index:")
    P = np.zeros((T, 6)); P[:, 0] = np.linspace(.30, .02, T); P[:, 1] = P[:, 0].copy()
    for j in range(2, 6):
        P[:, j] = np.linspace(.10, .24, T)
    P = np.clip(P, 1e-6, None); P /= P.sum(1, keepdims=True)
    r = helmsman_guard(P)
    print(f"  naive -> carrier {naive_helmsman(P)} | guard -> {r['helmsman']} ({r['code']}, margin {r['margin']:.1e})")


def fixes():
    T = 24
    print("\n--- TIER-2 FIX 1: coherent helmsman is invariant to an added carrier ---")
    A = np.linspace(.30, .36, T); B = np.linspace(.35, .33, T); C = np.linspace(.35, .31, T)
    ABC = np.c_[A, B, C]; ABC /= ABC.sum(1, keepdims=True)
    Dd = 0.2 + 0.18 * np.sin(np.linspace(0, 6 * np.pi, T)); ABCD = np.c_[A, B, C, Dd]; ABCD /= ABCD.sum(1, keepdims=True)
    print(f"  coherent helmsman of ABC alone={coherent_helmsman(ABC)['helmsman']}  "
          f"| ABC inside ABCD={coherent_helmsman(ABCD[:, :3])['helmsman']}  (was CLR: {naive_helmsman(ABC)} -> {naive_helmsman(ABCD, [0,1,2])})")

    print("--- TIER-2 FIX 2: SVD effective-rank guard ---")
    t = np.linspace(0, 1, T); c0 = np.array([.5, .3, .1, .07, .03]); c1 = np.array([.1, .1, .3, .3, .2])
    P1 = np.exp(np.outer(1 - t, np.log(c0)) + np.outer(t, np.log(c1))); P1 /= P1.sum(1, keepdims=True)
    Pf = np.random.default_rng(0).dirichlet(np.ones(5), size=T)
    print(f"  rank-1 line  -> {effective_rank(P1)}")
    print(f"  full random  -> {effective_rank(Pf)}")

    print("--- TIER-2 FIX 3: hold-lock hysteresis (rest -> shift -> rest) ---")
    rng = np.random.default_rng(7); D = 6
    def comp(base, n): x = base + rng.normal(0, n, D); x = np.clip(x, 1e-4, None); return x / x.sum()
    b1 = np.array([.30, .25, .15, .12, .10, .08]); b2 = np.array([.10, .15, .30, .20, .15, .10])
    seg = [comp(b1, 0.004) for _ in range(12)]
    seg += [comp(b1 * (1 - a) + b2 * a, 0.004) for a in np.linspace(0, 1, 6)]
    seg += [comp(b2, 0.004) for _ in range(12)]
    r = hold_lock(np.array(seg))
    print(f"  discovered noise_floor={r['noise_floor']} band=({r['lower']},{r['upper']})  "
          f"HOLD={r['n_hold']} MOVING={r['n_moving']}  registered={r['registered_changes']}")
    print(f"  pure noise -> registered changes = {len(hold_lock(np.array([comp(b1,0.004) for _ in range(30)]))['registered_changes'])} (tied down)")


if __name__ == "__main__":
    main()
    fixes()
