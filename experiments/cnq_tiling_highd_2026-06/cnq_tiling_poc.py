#!/usr/bin/env python3
"""
CNQ-Tiling Proof of Concept  (Hs / higgins-decomposition)  2026-06-10

Proves, on real arithmetic:
  (1) QUATERNION EXACTNESS at D=4 (sandwich rotation round-trip; atan2 vs arccos).
  (2) LOSSLESS RECONSTRUCTION of a full D-part composition from a CONNECTED atlas
      of overlapping exact 4-part charts (machine precision).
  (3) OVERLAP IS NECESSARY: a disjoint atlas is rank-deficient -> reconstruction fails.
  (4) NATIVE D=16 UNNECESSARY: a random D=16 move reconstructed from D=4 charts exactly.
  (5) SCALING to D=100,000: charts O(D), reconstruction near-linear; vs C(D,4) and dense-ILR wall.

A 4-part chart measures the 3 independent log-ratios among its parts (its local Helmert-ILR
coords are an invertible linear map of those). Stacking chart log-ratios log(x_i/x_j)=clr_i-clr_j
gives A c = b on the CLR vector c. A^T A is the graph Laplacian of the part co-occurrence graph;
the atlas reconstructs c losslessly IFF that graph is connected. Exact, deterministic, hash-stable.
"""
import numpy as np, time, json, math, itertools, platform
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.sparse.csgraph import connected_components

RESULTS={"meta":{"python":platform.python_version(),"numpy":np.__version__,"date":"2026-06-10"},"experiments":{}}

def closure(v):
    v=np.asarray(v,float); return v/v.sum()
def clr(x):
    L=np.log(x); return L-L.mean()

def quat_mul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return np.array([w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
                     w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2])
def quat_conj(q): return np.array([q[0],-q[1],-q[2],-q[3]])

def exp_quat_exactness(trials=20000,seed=1):
    rng=np.random.default_rng(seed); max_err=0.0
    for _ in range(trials):
        v=rng.normal(size=3); axis=rng.normal(size=3); axis/=np.linalg.norm(axis)
        th=rng.uniform(0,np.pi); q=np.array([np.cos(th/2),*(np.sin(th/2)*axis)])
        qv=quat_mul(quat_mul(q,np.array([0,*v])),quat_conj(q))[1:]
        ref=(np.cos(th)*v+(1-np.cos(th))*np.dot(axis,v)*axis+np.sin(th)*np.cross(axis,v))
        max_err=max(max_err,np.max(np.abs(qv-ref)))
    tab=[]
    for eps in [1e-1,1e-3,1e-5,1e-7,1e-9]:
        u0=np.array([1.0,0,0]); u1=np.array([np.cos(eps),np.sin(eps),0.0])
        dot=np.clip(np.dot(u0,u1),-1,1)
        a_ac=np.arccos(dot); a_at=math.atan2(np.linalg.norm(np.cross(u0,u1)),np.dot(u0,u1))
        tab.append((eps,abs(a_ac-eps)/eps,abs(a_at-eps)/eps))
    return max_err,tab

rot_err,angle_tab=exp_quat_exactness()
RESULTS["experiments"]["quaternion_exactness"]={"sandwich_vs_rodrigues_max_abs_err":rot_err,
  "angle_recovery_near_zero":[{"true_angle":e,"arccos_rel_err":ar,"atan2_rel_err":at} for e,ar,at in angle_tab]}
print("== (1) Quaternion exactness ==")
print(f"  sandwich vs Rodrigues max abs err (20k rotations): {rot_err:.2e}")
for e,ar,at in angle_tab: print(f"  angle {e:.0e}: arccos rel-err {ar:.2e}  atan2 rel-err {at:.2e}")

def band_edges(D,bw=3):
    rows=[];cols=[]
    for k in range(1,bw+1):
        i=np.arange(0,D-k); rows.append(i); cols.append(i+k)
    return np.stack([np.concatenate(rows),np.concatenate(cols)],axis=1)
def disjoint_block_edges(D,w=4):
    E=[]
    for s in range(0,D-(D%w),w):
        for x,y in itertools.combinations(range(s,s+w),2): E.append((x,y))
    return np.array(E)
def n_charts_sliding(D,width=4,overlap=3):
    return max(1,(D-width)//(width-overlap)+1)

def reconstruct(D,edges,x_true):
    a=edges[:,0]; b=edges[:,1]; m=len(edges)
    bvals=np.log(x_true[a])-np.log(x_true[b])
    rows=np.repeat(np.arange(m),2); cols=np.empty(2*m,int); cols[0::2]=a; cols[1::2]=b
    data=np.empty(2*m); data[0::2]=1.0; data[1::2]=-1.0
    A=sparse.csr_matrix((data,(rows,cols)),shape=(m,D)); L=(A.T@A).tocsr()
    ncomp,labels=connected_components(L,directed=False); Atb=A.T@bvals; c=np.zeros(D)
    for comp in range(ncomp):
        idx=np.where(labels==comp)[0]
        if len(idx)==1: continue
        rest=idx[1:]; Lsub=L[rest][:,rest].tocsc(); c[rest]=spsolve(Lsub,Atb[rest])
    c-=c.mean(); ctrue=clr(x_true); return np.max(np.abs(c-ctrue)),ncomp,len(labels)

print("\n== (2)/(3) Lossless reconstruction & overlap necessity ==")
los=[];dis=[]
for D in [16,64,256]:
    rng=np.random.default_rng(7)
    for t in range(5):
        x=rng.dirichlet(np.ones(D)*0.3); x=x/x.sum()
        e_con,nc_con,_=reconstruct(D,band_edges(D),x)
        e_dis,nc_dis,_=reconstruct(D,disjoint_block_edges(D),x)
        los.append((D,e_con,nc_con)); dis.append((D,e_dis,nc_dis))
con_max=max(e for _,e,_ in los); dis_min=min(e for _,e,_ in dis)
dis_comp=sorted(set((D,nc) for D,_,nc in dis))
RESULTS["experiments"]["lossless_connected"]={"max_recon_err":con_max,"components":sorted(set(nc for _,_,nc in los))}
RESULTS["experiments"]["disjoint_rank_deficient"]={"min_recon_err":dis_min,"components_by_D":dis_comp}
print(f"  CONNECTED sliding atlas: max recon err over 15 runs = {con_max:.2e} (always 1 component)")
print(f"  DISJOINT atlas:          min recon err over 15 runs = {dis_min:.2e}")
print(f"    disjoint (D,#components): {dis_comp}")

print("\n== (4) Native D=16 unnecessary ==")
rng=np.random.default_rng(16); D=16
x0=rng.dirichlet(np.ones(D)); x1=rng.dirichlet(np.ones(D)); move_true=clr(x1)-clr(x0)
def recon_clr(D,edges,x):
    a=edges[:,0]; b=edges[:,1]; m=len(edges); bvals=np.log(x[a])-np.log(x[b])
    rows=np.repeat(np.arange(m),2); cols=np.empty(2*m,int); cols[0::2]=a; cols[1::2]=b
    data=np.empty(2*m); data[0::2]=1; data[1::2]=-1
    A=sparse.csr_matrix((data,(rows,cols)),shape=(m,D)); L=(A.T@A).tocsr(); Atb=A.T@bvals
    c=np.zeros(D); rest=np.arange(1,D); c[rest]=spsolve(L[rest][:,rest].tocsc(),Atb[rest]); c-=c.mean(); return c
move_rec=recon_clr(D,band_edges(D),x1)-recon_clr(D,band_edges(D),x0)
move_err=np.max(np.abs(move_rec-move_true))
RESULTS["experiments"]["native_d16_unnecessary"]={"D":16,"move_reconstruction_max_abs_err":move_err}
print(f"  random D=16 move reconstructed from D=4 charts: max abs err = {move_err:.2e}")

print("\n== (5) Scaling to D=100,000 ==")
Ds=[4,16,64,256,1024,4096,16384,65536,100000]; scaling=[]; rng=np.random.default_rng(99)
for D in Ds:
    x=rng.dirichlet(np.ones(D)*0.3); x=x/x.sum()
    t0=time.perf_counter(); edges=band_edges(D); t1=time.perf_counter()
    err,ncomp,_=reconstruct(D,edges,x); t2=time.perf_counter()
    bf=math.comb(D,4) if D<=4096 else None; dense=((D-1)*D*8)/1e9
    scaling.append({"D":D,"charts_sliding":n_charts_sliding(D),"edges":int(len(edges)),
                    "build_s":t1-t0,"solve_s":t2-t1,"total_s":t2-t0,"recon_err":err,
                    "components":int(ncomp),"bruteforce_C_D_4":bf,"dense_global_ILR_GB":dense})
    bfs=f"{bf:.3e}" if bf else ">1e13"
    print(f"  D={D:>7}: charts={n_charts_sliding(D):>7} edges={len(edges):>8} solve={t2-t1:7.3f}s err={err:.1e} | C(D,4)={bfs} denseILR={dense:8.2f}GB")
RESULTS["experiments"]["scaling"]=scaling
with open("cnq_tiling_poc_results.json","w") as f: json.dump(RESULTS,f,indent=2)
print("\nSaved cnq_tiling_poc_results.json")
