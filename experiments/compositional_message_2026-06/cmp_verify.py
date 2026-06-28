"""Independent verification of the CMP headline (Crohn). Different model families + independent
PERMANOVA + ILR round-trip (sufficiency premise) + determinism re-check. Honest-broker."""
import sys, json, hashlib
from pathlib import Path
import numpy as np
from scipy import stats
from scipy.spatial.distance import pdist, squareform
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
ROOT = Path("/sessions/sharp-sleepy-bell/mnt/Claude CoWorker")
sys.path.insert(0, str(ROOT/"Current-Repo/Hs/HCI-CNTT/engine")); import geometry as geo
import pyreadr
SEED = 20260622; np.random.seed(SEED)
r = pyreadr.read_r(str(ROOT/"DATA/MicroBiome/coda4microbiome/data/Crohn.rda"))
X = r['x_Crohn'].values.astype(float); y = (r['y_Crohn'].iloc[:,0].values == 'CD')
comp = geo.closure(X); clr = geo.clr(comp); H = geo.helmert_basis(comp.shape[1]); Z = clr @ H.T

# (1) ILR round-trip: clr = ilr @ H ; recover composition -> confirms bijection/sufficiency premise
clr_back = Z @ H; comp_back = np.exp(clr_back); comp_back /= comp_back.sum(1, keepdims=True)
roundtrip = float(np.max(np.abs(comp_back - comp)))

def cvauc(Z, y, est, folds=5, repeats=5, seed=SEED):
    a=[]
    for rp in range(repeats):
        skf = StratifiedKFold(folds, shuffle=True, random_state=seed+rp)
        a.append(cross_val_score(est, Z, y, cv=skf, scoring="roc_auc").mean())
    return float(np.mean(a))

logit = make_pipeline(StandardScaler(), LogisticRegression(penalty="l2", C=1.0, max_iter=2000))
rf = RandomForestClassifier(n_estimators=400, random_state=SEED, n_jobs=1)
knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=15))
auc_logit = cvauc(Z, y, logit, repeats=10)
auc_rf = cvauc(Z, y, rf)
auc_knn = cvauc(Z, y, knn)

# aggregate sanity
p = comp; keff = np.exp(-(p*np.log(p)).sum(1))
from sklearn.metrics import roc_auc_score
auc_keff = float(max(roc_auc_score(y, keff), 1-roc_auc_score(y, keff)))

# independent PERMANOVA (fresh implementation, different perm seed)
D2 = squareform(pdist(Z))**2; N = len(y)
def F(lab):
    tot = D2.sum()/(2*N); w = 0.0
    for g in (True, False):
        idx = np.where(lab==g)[0]; n=len(idx); w += D2[np.ix_(idx,idx)].sum()/(2*n)
    return ((tot-w)/1)/(w/(N-2))
F0 = F(y); rng = np.random.default_rng(777); c=1
for _ in range(999):
    if F(rng.permutation(y)) >= F0: c+=1
pmanova = c/1000

# determinism: recompute logit AUC again, compare
auc_logit_2 = cvauc(Z, y, make_pipeline(StandardScaler(), LogisticRegression(penalty="l2", C=1.0, max_iter=2000)), repeats=10)

verdict = {
  "ilr_roundtrip_max_err": roundtrip,
  "sufficiency_premise_ok": roundtrip < 1e-10,
  "relational_auc": {"logistic": round(auc_logit,3), "random_forest": round(auc_rf,3), "knn_aitchison": round(auc_knn,3)},
  "aggregate_auc_keff": round(auc_keff,3),
  "relational_beats_aggregate_all_models": bool(min(auc_logit,auc_rf,auc_knn) > auc_keff + 0.2),
  "independent_permanova_F": round(F0,1), "independent_permanova_p": pmanova,
  "determinism_logit_identical": bool(abs(auc_logit-auc_logit_2) < 1e-12),
  "matches_saved_headline_0.832": bool(abs(auc_logit-0.8316031648035043) < 1e-9),
}
print(json.dumps(verdict, indent=2))
