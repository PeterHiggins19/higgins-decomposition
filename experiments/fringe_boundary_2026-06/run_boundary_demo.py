import numpy as np, glob, csv
B="/sessions/sharp-sleepy-bell/mnt/Claude CoWorker"
def closure(M):M=np.clip(M.astype(float),1e-12,None);return M/M.sum(1,keepdims=True)
def shannon(P):P=closure(P);return -(P*np.log(P)).sum(1).mean()
def geomean_decimate(P,k):
    # aggregate consecutive groups of k by closed geometric mean (the CoDa-correct temporal mean)
    P=closure(P);T=len(P)//k*k;G=[]
    for i in range(0,T,k):
        g=np.exp(np.log(P[i:i+k]).mean(0)); G.append(g/g.sum())
    return np.array(G)
def eitt_boundary(P, levels=(1,2,4)):
    """EITT-as-boundary-test: Shannon entropy should be INVARIANT under geometric-mean decimation
    IF the series is temporally autocorrelated (stationary regime). Large entropy drift across
    decimation => the autocorrelation/stationarity boundary is crossed (a fringe/boundary flag)."""
    H=[shannon(geomean_decimate(P,k)) for k in levels if len(P)//k>=2]
    drift=(max(H)-min(H))/(abs(np.mean(H))+1e-12)
    return {"entropy_by_level":[round(h,4) for h in H],"relative_drift_pct":round(drift*100,2),
            "verdict":"WITHIN-REGIME (entropy ~invariant; EITT holds)" if drift<0.01 else
                      "BOUNDARY (entropy NOT invariant under decimation; autocorrelation/stationarity edge)"}
def loadwide(p):
    rows=[r for r in open(p) if not r.startswith('#') and r.strip()];rd=list(csv.reader(rows))
    return rd[0][1:],np.array([[float(x) for x in r[1:]] for r in rd[1:]])

nm,M=loadwide(glob.glob(f"{B}/Current-Repo/Hs/HCI-CNT/experiments/codawork2026/ember_deu/*TWh.csv")[0])
P=closure(M)
print("EITT-as-boundary-test (old tool, new role) on real Germany energy series:")
print("  ordered (autocorrelated):", eitt_boundary(P))
rng=np.random.default_rng(0); Psh=P[rng.permutation(len(P))]
print("  shuffled (autocorrelation destroyed):", eitt_boundary(Psh))
# pure white composition (no structure) -> boundary
Pw=closure(rng.random((26,9)))
print("  white-noise composition:", eitt_boundary(Pw))
