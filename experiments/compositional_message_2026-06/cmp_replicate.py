"""CMP replication on an INDEPENDENT cohort (coda4microbiome HIV, 155 x 60, Pos/Neg).
'Do it again' — same falsifiable pipeline as cmp_analysis.py, new dataset, new label, with zeros.
Honest caveats: minority class n=27 (Neg); MSM is a known confounder of gut enterotype (we test
WHERE the signal lives, not biological causation). Deterministic, seeded, hash-receipted."""
import sys, json, hashlib, time
from pathlib import Path
import numpy as np
from scipy import stats
from scipy.spatial.distance import pdist, squareform
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score

ROOT = Path("/sessions/sharp-sleepy-bell/mnt/Claude CoWorker")
ENG = ROOT/"Current-Repo/Hs/HCI-CNTT/engine"; sys.path.insert(0, str(ENG))
import geometry as geo
import pyreadr
SEED = 20260622; np.random.seed(SEED); OUT = Path(__file__).resolve().parent

def sha(o):
    if isinstance(o, np.ndarray): return hashlib.sha256(np.ascontiguousarray(o).tobytes()).hexdigest()[:16]
    return hashlib.sha256(json.dumps(o, sort_keys=True, default=str).encode()).hexdigest()[:16]
def treat(M):
    M = M.copy().astype(float)
    for j in range(M.shape[1]):
        col = M[:, j]; pos = col[col > 0]
        if pos.size and (col <= 0).any(): M[col <= 0, j] = 0.65 * pos.min()
    return M
def cv_auc(Z, y, folds=5, repeats=10, seed=SEED):
    clf = make_pipeline(StandardScaler(), LogisticRegression(penalty="l2", C=1.0, max_iter=3000))
    a = []
    for rp in range(repeats):
        skf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed+rp)
        a.append(cross_val_score(clf, Z, y, cv=skf, scoring="roc_auc").mean())
    return float(np.mean(a)), float(np.std(a))
def permanova(Z, y, perms=999, seed=SEED):
    D2 = squareform(pdist(Z))**2; N = len(y)
    def F(lab):
        tot = D2.sum()/(2*N); within = 0.0
        for g in (True, False):
            idx = np.where(lab == g)[0]; n = len(idx); within += D2[np.ix_(idx, idx)].sum()/(2*n)
        return ((tot-within)/1)/(within/(N-2))
    F0 = F(y); rng = np.random.default_rng(seed); c = 1
    for _ in range(perms):
        if F(rng.permutation(y)) >= F0: c += 1
    return float(F0), float(c/(perms+1))

r = pyreadr.read_r(str(ROOT/"DATA/MicroBiome/coda4microbiome/data/HIV.rda"))
X = r['x_HIV'].values.astype(float); y = (r['y_HIV'].iloc[:,0].values == 'Pos')
N, Draw = X.shape
comp = geo.closure(treat(X)); Z = geo.ilr(comp)
p = comp; shannon = -(p*np.log(p)).sum(1); keff = np.exp(shannon)
dom = (p**2).sum(1); depth = X.sum(1)
def a1(s): au = roc_auc_score(y, s); return float(max(au,1-au)), float(stats.mannwhitneyu(s[y], s[~y]).pvalue)
agg = {nm:{"separation_auc":a1(s)[0],"mannwhitney_p":a1(s)[1]} for nm,s in
       [("K_eff",keff),("Shannon",shannon),("Gini_dominance",dom),("seq_depth",depth)]}
rel, rsd = cv_auc(Z, y); F, pm = permanova(Z, y)
B=200; rng=np.random.default_rng(SEED); null=np.array([cv_auc(Z, rng.permutation(y),5,1)[0] for _ in range(B)])
relp = float(((null>=rel).sum()+1)/(B+1))
# Law 2 (abundance ordering)
order = np.argsort(-comp.mean(0)); grid=[2,3,4,6,8,12,16,24,32,44,60]
def dscale(grid):
    rows=[]
    for Dk in grid:
        idx=order[:Dk]; rest=[j for j in range(Draw) if j not in set(idx.tolist())]
        cols=[comp[:,idx]];
        if rest: cols.append(comp[:,rest].sum(1,keepdims=True))
        sub=geo.closure(np.hstack(cols)); Zk=geo.ilr(sub)
        au,sd=cv_auc(Zk,y,5,8); rng2=np.random.default_rng(SEED+Dk)
        nl=[cv_auc(Zk,rng2.permutation(y),5,1)[0] for _ in range(40)]
        rows.append({"D_parts":int(Dk+(1 if rest else 0)),"n_top":int(Dk),"cv_auc":au,"cv_auc_sd":sd,"null_p95":float(np.percentile(nl,95))})
    return rows
res={"dataset":"coda4microbiome HIV (155x60, Pos/Neg)","N":int(N),"D":int(Draw),
     "n_pos":int(y.sum()),"n_neg":int((~y).sum()),"zeros_frac":float((X==0).mean()),"seed":SEED,
     "input_hash":{"X":sha(X),"y":sha(y.astype(int))},
     "law1":{"aggregates":agg,"relational_ilr":{"cv_auc":rel,"cv_auc_sd":rsd,"n_features":int(Z.shape[1])},
             "permanova":{"pseudoF":F,"p":pm},
             "relational_perm_null":{"B":B,"null_p95":float(np.percentile(null,95)),"p_value":relp}},
     "law2":{"ordering_abundance":dscale(grid)},
     "caveats":"minority class n_neg=27 (imbalance); MSM is a known gut-enterotype confounder; claim is about WHERE discriminative info lives, not biological causation."}
res["result_hash"]=sha({k:res[k] for k in ("law1","law2")})
json.dump(res, open(OUT/"cmp_result_hiv.json","w"), indent=2)
print(json.dumps({"agg":{k:round(v["separation_auc"],3) for k,v in agg.items()},
                  "relational_cv_auc":round(rel,3),"perm_p":round(relp,4),"permanova_p":pm,
                  "law2_auc":[round(x["cv_auc"],3) for x in res["law2"]["ordering_abundance"]],
                  "law2_parts":[x["D_parts"] for x in res["law2"]["ordering_abundance"]],
                  "hash":res["result_hash"]}, indent=2))
