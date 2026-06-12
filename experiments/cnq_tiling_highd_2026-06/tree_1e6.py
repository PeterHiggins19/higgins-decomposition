import numpy as np, time, itertools
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.sparse.csgraph import connected_components, shortest_path
def clr(x): L=np.log(x); return L-L.mean()
def tree_charts(D,k=4):
    charts=[]; level=list(range(D))
    while len(level)>1:
        nxt=[]; n=len(level); s=0
        while s<n:
            blk=level[s:s+k]
            if len(blk)<2:
                if charts: charts[-1]=tuple(dict.fromkeys(charts[-1]+tuple(blk)))
                nxt.append(blk[0]); s+=k; continue
            charts.append(tuple(blk)); nxt.append(blk[0]); s+=k
        level=nxt
    return charts
def path_charts(D): return [tuple(range(i,i+4)) for i in range(0,D-3)]
def edges_from_charts(charts):
    E=set()
    for c in charts:
        for a,b in itertools.combinations(c,2): E.add((a,b) if a<b else (b,a))
    return np.array(sorted(E),dtype=np.int64)
def reconstruct(D,edges,x):
    a=edges[:,0]; b=edges[:,1]; m=len(edges); bv=np.log(x[a])-np.log(x[b])
    rows=np.repeat(np.arange(m),2); cols=np.empty(2*m,np.int64); cols[0::2]=a; cols[1::2]=b
    data=np.empty(2*m); data[0::2]=1.0; data[1::2]=-1.0
    A=sparse.csr_matrix((data,(rows,cols)),shape=(m,D)); L=(A.T@A).tocsr()
    nc,_=connected_components(L,directed=False); Atb=A.T@bv
    rest=np.arange(1,D); c=np.zeros(D); c[rest]=spsolve(L[rest][:,rest].tocsc(),Atb[rest]); c-=c.mean()
    return np.max(np.abs(c-clr(x))),nc
def ecc0(D,edges):
    a=edges[:,0]; b=edges[:,1]
    adj=sparse.csr_matrix((np.ones(2*len(edges)),(np.concatenate([a,b]),np.concatenate([b,a]))),shape=(D,D))
    d=shortest_path(adj,method='D',unweighted=True,indices=[0]).ravel(); d=d[np.isfinite(d)]; return int(d.max())
D=1000000
rng=np.random.default_rng(3); x=rng.dirichlet(np.ones(D)*0.3); x/=x.sum()
for name,ch in [("tree",tree_charts(D)),("path",path_charts(D))]:
    t0=time.perf_counter(); E=edges_from_charts(ch); te=time.perf_counter()
    e=ecc0(D,E); err,nc=reconstruct(D,E,x); dt=time.perf_counter()-t0
    print(f"D=1,000,000 {name}: charts={len(ch)} edges={len(E)} ecc0={e} comp={nc} recon_err={err:.2e} time={dt:.2f}s")
