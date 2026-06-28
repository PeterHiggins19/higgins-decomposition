"""Compositional Message Principle (CMP) — real-data test on coda4microbiome Crohn.

Law 1 (Relational Locus): the discriminative signal about an external label lives in the
   inter-part LOG-RATIO (ILR/Aitchison) geometry, not in scalar/marginal aggregates.
   Aggregates (effective diversity K_eff, Shannon, Gini-Simpson dominance, sequencing
   depth) are relationship-blind functionals; by the data-processing inequality each
   carries <= the relational information and can be NULL while the relational signal is large.
Law 2 (Dimensional Articulation): amalgamating parts coarsens the composition, so recoverable
   signal is non-decreasing in the number of parts D (more symbols), with finite-sample saturation.

Honest-broker: deterministic, seeded, hash-receipted. Reports nulls straight. Uses the repo
engine geometry (HCI-CNTT/engine/geometry.py). Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import sys, json, hashlib, time
from pathlib import Path
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score

ROOT = Path("/sessions/sharp-sleepy-bell/mnt/Claude CoWorker")
ENG = ROOT/"Current-Repo/Hs/HCI-CNTT/engine"; sys.path.insert(0, str(ENG))
import geometry as geo  # closure, clr, helmert_basis, ilr  (the actual engine geometry)
import pyreadr

SEED = 20260622
np.random.seed(SEED)
OUT = Path(__file__).resolve().parent

def sha(obj):
    if isinstance(obj, np.ndarray):
        return hashlib.sha256(np.ascontiguousarray(obj).tobytes()).hexdigest()[:16]
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]

def treat(M):
    """multiplicative replacement of any nonpositive (none in this dataset; guard kept)."""
    M = M.copy().astype(float)
    for j in range(M.shape[1]):
        col = M[:, j]; pos = col[col > 0]
        if pos.size and (col <= 0).any():
            M[col <= 0, j] = 0.65 * pos.min()
    return M

def ilr_of(counts):
    comp = geo.closure(treat(counts))
    return geo.ilr(comp), comp

def cv_auc(Z, y, folds=5, repeats=10, seed=SEED):
    """mean repeated stratified k-fold ROC-AUC of L2 logistic regression on Z."""
    clf = make_pipeline(StandardScaler(), LogisticRegression(penalty="l2", C=1.0, max_iter=2000))
    aucs = []
    for rp in range(repeats):
        skf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed + rp)
        aucs.append(cross_val_score(clf, Z, y, cv=skf, scoring="roc_auc").mean())
    return float(np.mean(aucs)), float(np.std(aucs))

def permanova(Z, y, perms=999, seed=SEED):
    """PERMANOVA pseudo-F on Euclidean(ILR)=Aitchison distance, label-permutation p."""
    from scipy.spatial.distance import pdist, squareform
    D = squareform(pdist(Z, metric="euclidean")); N = len(y)
    D2 = D**2
    def pseudoF(lab):
        a = 2; tot = D2.sum()/(2*N)
        within = 0.0
        for g in (True, False):
            idx = np.where(lab == g)[0]; n = len(idx)
            within += D2[np.ix_(idx, idx)].sum()/(2*n)
        between = tot - within
        return (between/(a-1)) / (within/(N-a))
    F0 = pseudoF(y)
    rng = np.random.default_rng(seed); cnt = 1
    for _ in range(perms):
        if pseudoF(rng.permutation(y)) >= F0: cnt += 1
    return float(F0), float(cnt/(perms+1))

# ----------------------------------------------------------------------------- load
r = pyreadr.read_r(str(ROOT/"DATA/MicroBiome/coda4microbiome/data/Crohn.rda"))
X = r['x_Crohn'].values.astype(float); names = list(r['x_Crohn'].columns)
y = (r['y_Crohn'].iloc[:, 0].values == 'CD')
N, Draw = X.shape
res = {"dataset": "coda4microbiome Crohn (Calle, Pujolassos & Susin 2023, BMC Bioinformatics 24:82)",
       "N": int(N), "D": int(Draw), "n_CD": int(y.sum()), "n_control": int((~y).sum()),
       "seed": SEED, "input_hash": {"X": sha(X), "y": sha(y.astype(int))}}

comp_full = geo.closure(treat(X))
Zfull = geo.ilr(X if False else comp_full)  # ILR of full composition

# ----------------------------------------------------------------------------- LAW 1
t0 = time.time()
p = comp_full
shannon = -(p*np.log(p)).sum(1)
keff = np.exp(shannon)
dominance = (p**2).sum(1)            # Gini-Simpson complement (relationship-blind)
depth = X.sum(1)                     # sequencing depth (non-compositional magnitude)
def auc1(s):
    a = stats.mannwhitneyu(s[y], s[~y], alternative="two-sided")
    from sklearn.metrics import roc_auc_score
    au = roc_auc_score(y, s); return float(max(au, 1-au)), float(a.pvalue)
agg = {}
for nm, s in [("K_eff", keff), ("Shannon", shannon), ("Gini_dominance", dominance), ("seq_depth", depth)]:
    sep, pv = auc1(s); agg[nm] = {"separation_auc": sep, "mannwhitney_p": pv}

rel_auc, rel_sd = cv_auc(Zfull, y)
F, pmanova = permanova(Zfull, y, perms=999)
# permutation null for the relational classifier (single CV per shuffle, B shuffles)
B = 200; rng = np.random.default_rng(SEED)
null = []
for _ in range(B):
    yp = rng.permutation(y)
    a, _ = cv_auc(Zfull, yp, folds=5, repeats=1, seed=SEED)
    null.append(a)
null = np.array(null); rel_p = float(((null >= rel_auc).sum()+1)/(B+1))
res["law1"] = {
    "aggregates": agg,
    "relational_ilr": {"cv_auc": rel_auc, "cv_auc_sd": rel_sd, "n_features": int(Zfull.shape[1])},
    "permanova": {"pseudoF": F, "p": pmanova},
    "relational_perm_null": {"B": B, "null_mean": float(null.mean()), "null_p95": float(np.percentile(null,95)), "p_value": rel_p},
    "determinism_recheck_auc": cv_auc(Zfull, y)[0],
    "seconds": round(time.time()-t0, 1),
}

# ----------------------------------------------------------------------------- LAW 2
t1 = time.time()
def order_by_abundance(): return np.argsort(-comp_full.mean(0))
def order_by_clrvar():
    c = geo.clr(comp_full); return np.argsort(-c.var(0))
def dscaling(order, grid, null_B=40):
    rows = []
    for Dk in grid:
        idx = order[:Dk]; rest = [j for j in range(Draw) if j not in set(idx.tolist())]
        cols = [comp_full[:, idx]]
        if rest: cols.append(comp_full[:, rest].sum(1, keepdims=True))
        sub = geo.closure(np.hstack(cols))
        Z = geo.ilr(sub)
        au, sd = cv_auc(Z, y, folds=5, repeats=8)
        rng = np.random.default_rng(SEED+Dk); nl = []
        for _ in range(null_B):
            a, _ = cv_auc(Z, rng.permutation(y), folds=5, repeats=1, seed=SEED+Dk)
            nl.append(a)
        rows.append({"D_parts": int(Dk+ (1 if rest else 0)), "n_top": int(Dk),
                     "cv_auc": au, "cv_auc_sd": sd, "null_p95": float(np.percentile(nl,95))})
    return rows
grid = [2,3,4,6,8,12,16,24,32,40,48]
res["law2"] = {
    "ordering_abundance": dscaling(order_by_abundance(), grid),
    "ordering_clr_variance": dscaling(order_by_clrvar(), grid),
    "note": "top-n taxa + remainder amalgamated into one 'other' part (coarsening of the full composition).",
    "seconds": round(time.time()-t1, 1),
}
res["result_hash"] = sha({k: res[k] for k in ("law1", "law2")})
json.dump(res, open(OUT/"cmp_result.json", "w"), indent=2)
print(json.dumps({"law1_agg": {k: round(v["separation_auc"],3) for k,v in agg.items()},
                  "law1_relational_cv_auc": round(rel_auc,3), "law1_relational_p": rel_p,
                  "permanova_p": pmanova,
                  "law2_abundance_auc": [round(r["cv_auc"],3) for r in res["law2"]["ordering_abundance"]],
                  "law2_grid_parts": [r["D_parts"] for r in res["law2"]["ordering_abundance"]],
                  "result_hash": res["result_hash"],
                  "secs": round(time.time()-t0,1)}, indent=2))
