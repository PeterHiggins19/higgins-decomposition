#!/usr/bin/env python3
"""Triple-channel redundancy reader — the system that exceeds the Clifford+tiling combo.

Two channels DETECT a fault (they disagree); three ISOLATE it (a 2-of-3 vote) and
emit a confidence-tiered verdict + a safe state — the framework's FDIR / Safe-Operations
doctrine (huf-gov), applied to the mathematics of the read itself.

Three INDEPENDENT reconstructions of the move endpoint (unit ilr direction v-hat):
  1. TILING   — 4-part chart reconstruction (independent DATA path; catches atlas/data faults).
  2. CLIFFORD — Spin(n) bivector rotor, closed form (rotor-algebra path).
  3. MATRIX   — explicit n-D 2-plane rotation matrix (linear-algebra path).

Verdict codes (proposed for HCI-CNTT/engine/codes.py; SS-CCC-LLL form, SS=RC "redundancy check"):
  RC-CON-INF  consensus (3/3 agree)      -> full confidence; emit read + global rotor
  RC-ISO-WRN  isolate (2-of-3 agree)     -> flag + exclude the outlier channel; emit majority read
  RC-HLT-ERR  no majority                -> HALT-AND-REPORT (Safe-Operations safe state); no read

Run:  python experiments/clifford_tiling_redundancy_2026-06/triple_channel.py
"""
import numpy as np, sys, itertools, json
from pathlib import Path
ENG = Path(__file__).resolve().parents[2] / "HCI-CNTT" / "engine"
sys.path.insert(0, str(ENG))
import geometry as geo, atlas as atl


def clifford_apply(u, v, w):
    uh = u / np.linalg.norm(u); vh = v / np.linalg.norm(v); c = float(np.clip(uh @ vh, -1, 1))
    perp = vh - c * uh; s = np.linalg.norm(perp)
    if s < 1e-300: return w.copy()
    e1 = uh; e2 = perp / s; A = e1 @ w; B = e2 @ w
    return w - A * e1 - B * e2 + (A * c - B * s) * e1 + (A * s + B * c) * e2


def matrix_rotation(u, v):
    uh = u / np.linalg.norm(u); vh = v / np.linalg.norm(v); c = float(np.clip(uh @ vh, -1, 1))
    perp = vh - c * uh; s = np.linalg.norm(perp); I = np.eye(len(u))
    if s < 1e-300: return I
    e1 = uh; e2 = perp / s; th = np.arctan2(s, c)
    return I + np.sin(th) * (np.outer(e2, e1) - np.outer(e1, e2)) \
             + (np.cos(th) - 1) * (np.outer(e1, e1) + np.outer(e2, e2))


def channels(comp_prev, comp_t, D, edges, H, fault=None):
    u = geo.clr(comp_prev) @ H.T; v = geo.clr(comp_t) @ H.T; uh = u / np.linalg.norm(u)
    rec = atl.reconstruct_clr(D, edges, comp_t)[0]; vt = rec @ H.T; vt = vt / np.linalg.norm(vt)
    ch = {"tiling": vt, "clifford": clifford_apply(u, v, uh), "matrix": matrix_rotation(u, v) @ uh}
    if fault:
        for f in (fault if isinstance(fault, list) else [fault]):
            rf = np.random.default_rng(abs(hash(f)) % 99991)
            ch[f] = ch[f] + rf.normal(scale=1e-3, size=len(uh))   # distinct independent corruption
    return ch


def vote(ch, tau=1e-9):
    names = list(ch)
    res = {tuple(sorted(p)): float(np.linalg.norm(ch[p[0]] - ch[p[1]])) for p in itertools.combinations(names, 2)}
    bad = lambda n: all(res[tuple(sorted((n, m)))] > tau for m in names if m != n)
    if all(r < tau for r in res.values()):
        return "RC-CON-INF", "CONSENSUS (3/3 agree) — full confidence", None, res
    outliers = [n for n in names if bad(n)]
    others = [n for n in names if n not in outliers]
    if len(outliers) == 1 and len(others) == 2 and res[tuple(sorted(others))] < tau:
        return "RC-ISO-WRN", f"ISOLATE: channel '{outliers[0]}' diverges; majority {others} agree", outliers[0], res
    return "RC-HLT-ERR", "HALT-AND-REPORT — no 2-of-3 majority (Safe-Operations safe state)", None, res


if __name__ == "__main__":
    rng = np.random.default_rng(7); D = 12
    comp = geo.closure(np.abs(rng.normal(size=(2, D))) + 0.05); H = geo.helmert_basis(D)
    edges = atl.edges_from_charts(atl.hierarchical_atlas(D))
    cases = [("CLEAN", None), ("FAULT in tiling", "tiling"),
             ("FAULT in clifford", "clifford"), ("FAULT in 2 channels", ["tiling", "matrix"])]
    log = []
    for label, fault in cases:
        ch = channels(comp[0], comp[1], D, edges, H, fault=fault)
        code, msg, iso, res = vote(ch)
        print(f"[{label:22}] {code}  {msg}")
        print("   pairwise: " + "  ".join(f"{a[:4]}-{b[:4]}={r:.1e}" for (a, b), r in res.items()))
        log.append({"case": label, "code": code, "verdict": msg, "isolated": iso,
                    "residuals": {f"{a}-{b}": r for (a, b), r in res.items()}})
    json.dump({"date": "2026-06-11", "tier": 1, "cases": log}, open(Path(__file__).resolve().parent / "triple_results.json", "w"), indent=1)
    print("wrote triple_results.json")
