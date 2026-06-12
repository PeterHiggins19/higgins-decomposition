#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zero_treatment.py  --  upstream zero-treatment for compositional series.

Replaces the engine's 1e-15 floor with a principled, deterministic treatment applied
BEFORE the engine (Tensor Train Link 1 / Adapter stage). The engine is NOT modified.

Two kinds of zero are handled distinctly (this distinction is the whole point):

  * STRUCTURAL zero  -- a carrier that is zero in EVERY row is genuinely absent from the
    sub-system (e.g. Canada reports no 'Other Renewables' in any year). Flooring it to
    1e-15 injects a huge artificial CLR deviation (~ -33) and inflates the Aitchison norm.
    Correct treatment: DROP the carrier -> run at the true dimensionality.

  * ROUNDED zero -- a carrier zero in SOME rows only (real but below the reporting
    precision, e.g. early-year Solar). Correct treatment: multiplicative replacement
    (Martin-Fernandez, Barcelo-Vidal & Pawlowsky-Glahn 2003): fill the zero with a small
    delta below the detection limit and preserve the ratios among the observed parts.
    Here delta_j = frac * DL_j, with DL_j = smallest positive value observed in column j
    (the implied reporting/detection limit). frac defaults to 0.65 (the common "65% of DL"
    convention). Closure is restored downstream by the engine (it closes its input).

Deterministic: same input -> same output. No randomness. No engine change.
"""
import csv
from typing import List, Tuple, Dict, Any


def treat_matrix(M: List[List[float]], names: List[str], frac: float = 0.65
                 ) -> Tuple[List[List[float]], List[str], Dict[str, Any]]:
    """Treat a raw N x D value matrix. Returns (treated_matrix, kept_names, report)."""
    N, D = len(M), len(names)
    colmax = [max(M[i][j] for i in range(N)) for j in range(D)]
    keep = [j for j in range(D) if colmax[j] > 0.0]              # drop all-zero (structural) columns
    dropped = [names[j] for j in range(D) if colmax[j] == 0.0]
    kept_names = [names[j] for j in keep]
    out = [[M[i][j] for j in keep] for i in range(N)]
    dl: Dict[str, float] = {}
    replaced = 0
    for jj, j in enumerate(keep):
        pos = [M[i][j] for i in range(N) if M[i][j] > 0.0]
        d = frac * min(pos) if pos else 0.0
        dl[names[j]] = d
        for i in range(N):
            if out[i][jj] <= 0.0:
                out[i][jj] = d
                replaced += 1
    report = {
        "method": "structural-drop + multiplicative-replacement (frac*DL, DL=min positive per column)",
        "frac": frac,
        "D_in": D, "D_out": len(kept_names),
        "structural_dropped": dropped,
        "rounded_zeros_replaced": replaced,
        "detection_limits": {k: round(v, 8) for k, v in dl.items()},
    }
    return out, kept_names, report


def treat_csv(in_csv: str, out_csv: str, frac: float = 0.65) -> Dict[str, Any]:
    """Treat a pipeline-ready CSV (first column = time index, rest = carriers)."""
    rows = list(csv.reader(open(in_csv)))
    hdr, body = rows[0], rows[1:]
    tcol, names = hdr[0], hdr[1:]
    labels = [r[0] for r in body]
    M = [[float(x) for x in r[1:]] for r in body]
    out, kept_names, report = treat_matrix(M, names, frac)
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([tcol] + kept_names)
        for i, lab in enumerate(labels):
            w.writerow([lab] + [round(v, 6) for v in out[i]])
    report["in_csv"], report["out_csv"] = in_csv, out_csv
    return report


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 3:
        print("usage: zero_treatment.py <in_csv> <out_csv> [frac]"); sys.exit(1)
    fr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.65
    print(json.dumps(treat_csv(sys.argv[1], sys.argv[2], fr), indent=1))
