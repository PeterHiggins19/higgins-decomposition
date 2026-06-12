import numpy as np, time, math
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.sparse.csgraph import connected_components
def clr(x): L=np.log(x); return L-L.mean()
def band_edges(D,bw=3):
    r=[];c=[]
    for k in range(1,bw+1):
        i=np.arange(0,D-k); r.append(i); c.append(i+k)
    return np.stack([np.concatenate(r),np.concatenate(c)],1)
def reconstruct(D,edges,x):
    a=edges[:,0]; b=edges[:,1]; m=len(edges); bv=np.log(x[a])-np.log(x[b])
    rows=np.repeat(np.arange(m),2); cols=np.empty(2*m,int); cols[0::2]=a; cols[1::2]=b
    data=np.empty(2*m); data[0::2]=1; data[1::2]=-1
    A=sparse.csr_matrix((data,(rows,cols)),shape=(m,D)); L=(A.T@A).tocsr(); Atb=A.T@bv
    rest=np.arange(1,D); c=np.zeros(D); c[rest]=spsolve(L[rest][:,rest].tocsc(),Atb[rest]); c-=c.mean()
    return np.max(np.abs(c-clr(x)))
for D in [500000,1000000]:
    rng=np.random.default_rng(3); x=rng.dirichlet(np.ones(D)*0.3); x/=x.sum()
    t0=time.perf_counter(); e=band_edges(D); err=reconstruct(D,e,x); dt=time.perf_counter()-t0
    print(f"D={D}: charts={D-3} edges={len(e)} time={dt:.3f}s err={err:.1e} tiling_mem~{len(e)*16/1e6:.1f}MB denseILR={ (D-1)*D*8/1e9:.0f}GB")
