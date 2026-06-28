#!/usr/bin/env python3
"""
Dimension is the message — relational signal AND communication symbol-capacity grow with D.

Real coda4microbiome Crohn data (Calle, Pujolassos & Susin 2023, BMC Bioinformatics 24:82).
As the number of parts D grows, three quantities are tracked:
  - relational_auc        : 5-fold CV ROC-AUC of an L2 logistic read of the ILR coordinates
                            (the compositional / relational MESSAGE about Crohn's disease);
  - scalar_shannon_auc    : separation by the scalar Shannon diversity index alone
                            (the Margalef / E.O. Wilson "community as a message" read — a SCALAR);
  - symbol_capacity_bits  : the composition read as an N-dim signal constellation; the Gaussian-
                            channel capacity over the ILR covariance eigen-directions,
                            sum_i 0.5*log2(1 + lambda_i/delta^2)  (bits) at a fixed noise floor.

Result: the relational message and the symbol capacity GROW with D; the scalar diversity read
stays at chance. More parts / higher dimension = more message and more communication symbology.

Deterministic (seeded), hash-receipted. Uses the repo engine geometry. Honest-broker; Tier 1 on the run.
Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import sys, json, hashlib, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score
sys.path.insert(0, "/sessions/sharp-sleepy-bell/mnt/Claude CoWorker/Current-Repo/Hs/HCI-CNTT/engine")
import geometry as geo
import pyreadr

SEED = 20260623; np.random.seed(SEED)
DATA = "/sessions/sharp-sleepy-bell/mnt/Claude CoWorker/DATA/MicroBiome/coda4microbiome/data/"


def treat(M):
    M = M.copy().astype(float)
    for j in range(M.shape[1]):
        col = M[:, j]; p = col[col > 0]
        if p.size and (col <= 0).any():
            M[col <= 0, j] = 0.65 * p.min()
    return M
def cv_auc(Z, y, folds=5, repeats=4, seed=SEED):
    clf = make_pipeline(StandardScaler(), LogisticRegression(penalty="l2", C=1.0, max_iter=2000))
    a = []
    for rp in range(repeats):
        skf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed + rp)
        a.append(cross_val_score(clf, Z, y, cv=skf, scoring="roc_auc").mean())
    return float(np.mean(a))
def cap_bits(Z, delta2=0.25):
    lam = np.linalg.eigvalsh(np.cov(Z.T) + 1e-12 * np.eye(Z.shape[1]))
    return float(np.sum(0.5 * np.log2(1.0 + np.maximum(lam, 0) / delta2)))


def main():
    r = pyreadr.read_r(DATA + "Crohn.rda")
    X = r["x_Crohn"].values.astype(float); y = (r["y_Crohn"].iloc[:, 0].values == "CD")
    N, Draw = X.shape; comp = geo.closure(treat(X))
    order = np.argsort(-comp.mean(0))
    rows = []
    for Dk in [2, 4, 8, 16, 24, 32, 48]:
        idx = order[:Dk]; rest = [j for j in range(Draw) if j not in set(idx.tolist())]
        cols = [comp[:, idx]]
        if rest: cols.append(comp[:, rest].sum(1, keepdims=True))
        sub = geo.closure(np.hstack(cols)); Z = geo.ilr(sub)
        sh = -(sub * np.log(sub)).sum(1); a = roc_auc_score(y, sh)
        rows.append({"D_parts": int(Z.shape[1] + 1), "ilr_dims": int(Z.shape[1]),
                     "relational_auc": round(cv_auc(Z, y), 3),
                     "scalar_shannon_auc": round(float(max(a, 1 - a)), 3),
                     "symbol_capacity_bits": round(cap_bits(Z), 2)})
    out = {"experiment": "dimension_is_the_message",
           "dataset": "coda4microbiome Crohn (Calle/Pujolassos/Susin 2023)",
           "N": int(N), "D_max": int(Draw), "seed": SEED, "grid": rows}
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
