#!/usr/bin/env python3
"""
The skin of sensors — a sensor array is a composition; more sensors = more language.

A "skin" of N sensors on a manifold senses a conserved stimulus budget. The reading is a
composition (N parts); Hs reads it in log-ratio coordinates. As N grows (higher D), the skin
distinguishes more states (finer discrimination) and carries more symbol-capacity (bits) — the
dimension-is-the-message result in the sensing frame, and the analogue of AI scaling with compute.

Stimulus: a touch in one of `classes` regions; sensor i responds to its distance from the touch.
Deterministic (seeded), hash-receipted. Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import hashlib, json, math
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold

rng = np.random.default_rng(11)
def helmert(D):
    B = np.zeros((D-1, D))
    for i in range(1, D):
        B[i-1, :i] = 1.0/i; B[i-1, i] = -1.0; B[i-1] *= math.sqrt(i/(i+1.0))
    return B
def clr(x): L = np.log(x); return L - L.mean(1, keepdims=True)
def cap_bits(Z, d2=0.25):
    lam = np.linalg.eigvalsh(np.cov(Z.T) + 1e-12*np.eye(Z.shape[1]))
    return float(np.sum(0.5*np.log2(1 + np.maximum(lam, 0)/d2)))

def skin_read(N, M=600, sigma=0.18, noise=0.02, classes=6):
    pos = np.linspace(0, 1, N); X = []; y = []
    for _ in range(M):
        cls = rng.integers(0, classes); loc = (cls + 0.5)/classes
        resp = np.exp(-(pos-loc)**2/sigma**2) + noise*rng.standard_normal(N)
        resp = np.clip(resp, 1e-6, None); X.append(resp/resp.sum()); y.append(cls)
    return np.array(X), np.array(y)

def main():
    rows = []
    for N in [3, 5, 9, 17, 33, 65]:
        X, y = skin_read(N); Z = clr(X) @ helmert(N).T
        clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, multi_class='ovr'))
        acc = float(np.mean([cross_val_score(clf, Z, y, cv=StratifiedKFold(4, shuffle=True, random_state=7+r)).mean() for r in range(3)]))
        rows.append({"sensors_N": N, "ilr_dims": N-1, "touch_discrimination_acc": round(acc, 3),
                     "skin_symbol_capacity_bits": round(cap_bits(Z), 2)})
    out = {"experiment": "skin_of_sensors", "stimulus": "touch location, 6 regions",
           "chance_acc": round(1/6, 3), "grid": rows,
           "reading": "more sensors (higher D) -> finer discrimination + more capacity = more language; like AI scaling with compute"}
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
