#!/usr/bin/env python3
"""
CNQ-Tiling — Hierarchical (tree / phylogenetic) atlas vs sliding-window (path) atlas.
2026-06-10.

Tests the prediction: a balanced 4-ary tree atlas has co-occurrence-graph diameter
O(log D), so the reconstruction Laplacian stays well-conditioned and reconstruction
holds near machine precision at any D -- fixing the path-atlas error growth
(2e-13 at D=64 -> 2.6e-7 at D=1e6).

Tree atlas construction (all charts are REAL 4-part charts; representatives are real parts):
  level 0 = the D parts.
  group consecutive parts into blocks of 4 -> each block is a chart (4-clique);
  the block's first part is its representative.
  level 1 = the representatives; recurse until one node remains.
Representatives chain every chart up to the root => connected; depth = log_4(D);
any leaf->leaf distance <= 2*depth+const => O(log D).
For microbiome this tree IS the phylogeny: sibling taxa share the low-level charts.
"""
import numpy as np, time, json, itertools, platform, math
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.sparse.csgraph import connected_components, shortest_path

def clr(x): L=np.log(x); return L-L.mean()

# ---- atlases ----
def path_charts(D):
    # sliding window of 4, overlap 3
    return [tuple(range(i,i+4)) for i in range(0,D-3)] or [tuple(range(D))]

def tree_charts(D, k=4):
    charts=[]; level=list(range(D))
    while len(level)>1:
        nxt=[]; n=len(level)
        s=0
        while s<n:
            blk=level[s:s+k]
            if len(blk)<2:                       # lone trailing rep -> fold into previous chart
                if charts:
                    charts[-1]=tuple(dict.fromkeys(charts[-1]+tuple(blk)))
                nxt.append(blk[0]); s+=k; continue
            charts.append(tuple(blk)); nxt.append(blk[0]); s+=k
        level=nxt
    return charts

def edges_from_charts(charts):
    E=set()
    for c in charts:
        for a,b in itertools.combinations(c,2):
            E.add((a,b) if a<b else (b,a))
    return np.array(sorted(E),dtype=np.int64)

def reconstruct(D, edges, x):
    a=edges[:,0]; b=edges[:,1]; m=len(edges)
    bv=np.log(x[a])-np.log(x[b])
    rows=np.repeat(np.arange(m),2); cols=np.empty(2*m,np.int64); cols[0::2]=a; cols[1::2]=b
    data=np.empty(2*m); data[0::2]=1.0; data[1::2]=-1.0
    A=sparse.csr_matrix((data,(rows,cols)),shape=(m,D)); L=(A.T@A).tocsr()
    ncomp,_=connected_components(L,directed=False); Atb=A.T@bv
    rest=np.arange(1,D); c=np.zeros(D)
    c[rest]=spsolve(L[rest][:,rest].tocsc(),Atb[rest]); c-=c.mean()
    return np.max(np.abs(c-clr(x))), ncomp

def eccentricity0(D, edges):
    # unweighted distance from node 0 (proxy for diameter ~ within factor 2)
    a=edges[:,0]; b=edges[:,1]
    adj=sparse.csr_matrix((np.ones(2*len(edges)),
        (np.concatenate([a,b]),np.concatenate([b,a]))),shape=(D,D))
    d=shortest_path(adj,method='D',unweighted=True,indices=[0]).ravel()
    d=d[np.isfinite(d)]
    return int(d.max())

RESULTS={"meta":{"date":"2026-06-10","python":platform.python_version()},"rows":[]}
print(f"{'D':>8} | {'atlas':>5} | {'charts':>8} {'edges':>9} {'ecc0':>6} {'comp':>4} | {'recon_err':>10} {'solve_s':>8}")
print("-"*78)
for D in [64,256,1024,4096,16384,65536,100000]:
    rng=np.random.default_rng(99); x=rng.dirichlet(np.ones(D)*0.3); x/=x.sum()
    row={"D":D}
    for name,charts in [("path",path_charts(D)),("tree",tree_charts(D))]:
        E=edges_from_charts(charts)
        ecc=eccentricity0(D,E)
        t0=time.perf_counter(); err,nc=reconstruct(D,E,x); dt=time.perf_counter()-t0
        row[name]={"charts":len(charts),"edges":int(len(E)),"ecc0":ecc,
                   "components":int(nc),"recon_err":err,"solve_s":dt}
        print(f"{D:>8} | {name:>5} | {len(charts):>8} {len(E):>9} {ecc:>6} {nc:>4} | {err:>10.2e} {dt:>8.3f}")
    RESULTS["rows"].append(row)
    print("-"*78)
json.dump(RESULTS,open("cnq_tiling_hierarchical_results.json","w"),indent=2)
print("saved cnq_tiling_hierarchical_results.json")
