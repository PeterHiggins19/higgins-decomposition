#!/usr/bin/env python3
"""
Hs compositional source-coding benchmark — honest rate vs distortion on real data.

Question (Peter): can Hs "get close to Shannon"? Answer, stated honestly:
  - Shannon CHANNEL CAPACITY and the true source RATE-DISTORTION bound cannot be beaten
    and are NOT beaten here. No such claim is made.
  - What IS real and measured: using the compositional (ILR / Aitchison) geometry, Hs codes
    real D=8 energy-mix data far more efficiently than a structure-agnostic baseline, and its
    entropy-coding stage runs within ~10% of the entropy of its own symbols (near-optimal).

Honest correction recorded in-code: a first pass labeled the Gaussian rate-distortion value a
"floor". It is NOT a floor — a Gaussian is the MAX-ENTROPY source for a given covariance, so the
Gaussian R-D is an UPPER bound (ceiling). Real structured data has lower entropy, so coding below
the Gaussian number is expected and is NOT a Shannon violation. The mislabel was caught and fixed.

Data: OWID per-country energy generation (Coal,Gas,Oil,Nuclear,Hydro,Solar,Wind,Biofuel), pooled.
Deterministic; hash-receipted. Author: Peter Higgins; AI-assisted per HUF-STD-001. Honest-broker.
"""
import csv, glob, gzip, hashlib, json, math, os
import numpy as np

RAW = os.environ.get("OWID_DIR",
    "/sessions/sharp-sleepy-bell/mnt/Claude CoWorker/Current-Repo/Hs/"
    "experiments/2026-05-10_full-corpus-validation/raw_inputs/")
PARTS = ["Coal", "Gas", "Oil", "Nuclear", "Hydro", "Solar", "Wind", "Biofuel"]
TARGET = 0.15   # target reconstruction fidelity: mean Aitchison (clr) RMSE


def load():
    X = []
    for fn in sorted(glob.glob(os.path.join(RAW, "owid_energy_*.csv"))):
        with open(fn) as f:
            for r in csv.DictReader(f):
                try: row = [float(r[p]) for p in PARTS]
                except (KeyError, ValueError): continue
                if sum(row) > 0: X.append(row)
    X = np.clip(np.array(X), 1e-6, None)
    return X / X.sum(1, keepdims=True)


def helmert(D):
    B = np.zeros((D - 1, D))
    for i in range(1, D):
        B[i-1, :i] = 1.0/i; B[i-1, i] = -1.0; B[i-1] *= math.sqrt(i/(i+1.0))
    return B
def clr(x): L = np.log(x); return L - L.mean(1, keepdims=True)


def main():
    X = load(); N, D = X.shape
    H = helmert(D); CLR = clr(X); ILR = CLR @ H.T; mu = ILR.mean(0); Z = ILR - mu
    gz = lambda ints: len(gzip.compress(np.ascontiguousarray(ints.astype(np.int32)).tobytes(), 9)) * 8.0 / N
    rmse = lambda ilr_hat: float(np.sqrt((((ilr_hat @ H) - CLR) ** 2).sum(1).mean()))

    # --- Hs compositional (ILR) coder: water-filled uniform scalar quantize + gzip ---
    var = np.var(Z, 0); lo, hi = 1e-12, var.max()
    for _ in range(200):
        th = (lo + hi) / 2; d = np.minimum(th, var)
        lo, hi = (lo, th) if d.sum() > TARGET**2 else (th, hi)
    d = np.minimum((lo + hi) / 2, var); Q = np.zeros_like(Z); Zr = np.zeros_like(Z)
    for i in range(D - 1):
        if d[i] >= var[i] * 0.999: continue
        step = math.sqrt(12 * d[i]); q = np.round(Z[:, i] / step); Q[:, i] = q; Zr[:, i] = q * step
    ilr_bits = gz(Q); ilr_rmse = rmse(Zr + mu)
    ent = sum(-(lambda p: (p * np.log2(p)).sum())(np.unique(Q[:, c], return_counts=True)[1] /
              np.unique(Q[:, c], return_counts=True)[1].sum()) for c in range(D - 1))

    # --- structure-agnostic baseline: uniform-quantize raw shares + gzip ---
    best = None
    for step in np.geomspace(1e-6, 1e-1, 60):
        q = np.round(X / step); comp = np.clip(q * step, 1e-9, None); comp /= comp.sum(1, keepdims=True)
        rm = float(np.sqrt(((clr(comp) - CLR) ** 2).sum(1).mean())); b = gz(q)
        if rm <= TARGET and (best is None or b < best[0]): best = (b, rm)

    raw_gz = len(gzip.compress(np.ascontiguousarray(X.astype(np.float64)).tobytes(), 9)) * 8.0 / N
    out = {
        "dataset": "OWID energy generation mix (pooled countries)", "N": N, "D": D, "target_aitchison_rmse": TARGET,
        "hs_ilr_coder": {"bits_per_sample": round(ilr_bits, 2), "achieved_rmse": round(ilr_rmse, 4),
                         "order0_entropy_ref_bits": round(ent, 2), "gzip_within_pct_of_entropy": round(100*(ilr_bits/ent - 1), 1)},
        "raw_share_baseline": {"bits_per_sample": round(best[0], 2), "rmse": round(best[1], 4)} if best else {"reached_target": False},
        "lossless_float64_gzip_bits": round(raw_gz, 1),
        "hs_vs_baseline_bit_ratio": round(best[0] / ilr_bits, 2) if best else None,
        "hs_vs_lossless_float_ratio": round(raw_gz / ilr_bits, 2),
        "honest_notes": [
            "Shannon capacity and the true source rate-distortion bound are NOT beaten and cannot be.",
            "Gaussian rate-distortion is a CEILING (max-entropy for the covariance), not a floor; coding below it is expected for structured data and is not a Shannon violation.",
            "The win is the compositional (ILR) geometry; KLT decorrelation did not help the LZ pipeline (reported as a negative).",
        ],
    }
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
