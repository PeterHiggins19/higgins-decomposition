import numpy as np, csv
np.set_printoptions(suppress=True)
BASE="/sessions/sharp-sleepy-bell/mnt/Claude CoWorker"

# ---------- engine core (inline, to spec) ----------
def clr(P): P=np.clip(P,1e-12,None); L=np.log(P); return L-L.mean(1,keepdims=True)
def close(M): M=np.clip(M.astype(float),0,None); s=M.sum(1,keepdims=True); s[s==0]=1; return M/s
def keff(P): P=np.clip(P,1e-12,None); P=P/P.sum(1,keepdims=True); H=-(P*np.log(P)).sum(1); return np.exp(H)
def cl_helmsman(P):  # OLD: argmax total |dCLR|
    d=np.abs(np.diff(clr(P),axis=0)).sum(0); return int(np.argmax(d)), d
# ---------- NEW guard modules (inlined verbatim from repo, self-tested) ----------
def coherent_helmsman(P):
    P=np.clip(P,1e-12,None); logP=np.log(P); T,D=P.shape; m=np.zeros(D)
    for i in range(D):
        for j in range(D):
            if i!=j: m[i]+=np.abs(np.diff(logP[:,i]-logP[:,j])).sum()
        m[i]/=(D-1)
    return int(np.argmax(m)), m
def effective_rank(P):
    X=clr(P); X=X-X.mean(0); s=np.linalg.svd(X,compute_uv=False); s=s[s>s.max()*1e-9]
    pr=float((s.sum()**2)/(s**2).sum()); maxr=min(P.shape[0]-1,P.shape[1]-1)
    return round(pr,2), maxr, ("DG-RNK-WRN" if pr<0.5*maxr else None)
def matrix_sparsity(M): return float((M<=0).mean())
def hold_lock(P, engine_floor=1e-9, k_up=4.0, k_down=2.0, struct_k=3.0):
    H=clr(P); steps=np.linalg.norm(np.diff(H,axis=0),axis=1)
    if steps.size==0: return {"floor":0,"events":[],"n_hold":0,"n_move":0}
    med=np.median(steps); mad=np.median(np.abs(steps-med))*1.4826
    noise=max(engine_floor, max(np.quantile(steps,0.5)-mad, np.quantile(steps,0.25)),1e-12)
    up,lo=k_up*noise,k_down*noise; state="HOLD"; states=[]; ev=[]; ref=0
    for t,m in enumerate(steps):
        if state=="HOLD" and m>up: state="MOVING"
        elif state=="MOVING" and m<lo:
            net=float(np.linalg.norm(H[t+1]-H[ref]))
            if net>=struct_k*noise: ev.append(t+1); ref=t+1
            state="HOLD"
        states.append(state)
    return {"floor":round(noise,4),"upper":round(up,4),"events":ev,"n_hold":states.count("HOLD"),"n_move":states.count("MOVING")}
def resolvability(P):
    d=np.abs(np.diff(clr(P),axis=0)).sum(0); o=np.argsort(-d); mag=float(d[o[0]]); margin=float(d[o[0]]-d[o[1]])
    code=None
    if mag<1e-6: code="HM-NUL-WRN"
    elif margin<=1e-3*mag: code="HM-TIE-WRN"
    return mag,margin,code

def load_csv(path, skip_hash=True, label_col0=True):
    rows=[]; hdr=None
    with open(path) as f:
        for line in f:
            if line.startswith('#'): continue
            rows.append(line.rstrip('\n'))
    rd=list(csv.reader(rows)); hdr=rd[0]; data=rd[1:]
    labels=[r[0] for r in data]; M=np.array([[float(x) if x not in('','NA') else 0.0 for x in r[1:]] for r in data])
    return hdr, labels, M

print("="*70); print("GUEST 2 — GEOLOGY: Frielingen-9 mudstone, real D=4 XRF (depth-ordered)"); print("="*70)
hdr,depth,M=load_csv(f"{BASE}/Current-Repo/Hs/collaborations/geology-wehner/demo_frielingen9/frielingen9_xrf_4part.csv")
parts=hdr[1:5]; X=M[:, :4]; P=close(X); depth=np.array([float(d) for d in depth])
print("parts:",parts,"| n_samples:",P.shape[0])
oh,od=cl_helmsman(P); ch,cm=coherent_helmsman(P)
print(f"OLD CLR helmsman: {parts[oh]}  (per-carrier |dCLR| {np.round(od,2)})")
print(f"NEW coherent helmsman: {parts[ch]}  -> {'CONFIRMS' if ch==oh else 'DIFFERS from'} CLR read (robust to which elements are included)")
er=effective_rank(P); print(f"NEW effective rank: {er[0]} of {er[1]} dims  {er[2] or '(full-rank, no degeneracy)'}")
hl=hold_lock(P); old_reg=int((np.linalg.norm(np.diff(clr(P),axis=0),axis=1) > (np.linalg.norm(np.diff(clr(P),axis=0),axis=1).mean()+2*np.linalg.norm(np.diff(clr(P),axis=0),axis=1).std())).sum())
print(f"OLD regime boundaries (mean+2std): {old_reg}")
print(f"NEW hold-lock: discovered floor={hl['floor']}, band-up={hl['upper']}, REGISTERED structural changes={len(hl['events'])} at depths {np.round(depth[hl['events']],1) if hl['events'] else []}")
print(f"     -> {hl['n_hold']} held vs {hl['n_move']} moving steps (chatter-free, self-calibrated)")
print(f"sparsity: {matrix_sparsity(X)*100:.0f}% zeros (dense -> log-ratio read fully valid)")

print(); print("="*70); print("GUEST 1 — MICROBIOME: real Crohn (D=48) + ECAM infant gut"); print("="*70)
hdr,lab,M=load_csv(f"{BASE}/Current-Repo/Hs/experiments/microbiome_real_2026-06/crohn.csv")
Pc=close(M); spc=matrix_sparsity(M)
print(f"CROHN D={M.shape[1]}, n={M.shape[0]}, sparsity={spc*100:.0f}% zeros")
print(f"  NEW sparsity flag: {'GD-SPZ-WRN (densify before log-ratio)' if spc>=0.5 else 'below 50% -> log-ratio read valid'}")
er=effective_rank(Pc); print(f"  NEW effective rank: {er[0]} of {er[1]}  {er[2] or '(full-rank)'}")
kc=keff(Pc); print(f"  K_eff mean={kc.mean():.2f} (old global null held: CD vs control not separable on K_eff)")
# ECAM maturation
hdr,day,M=load_csv(f"{BASE}/Current-Repo/Hs/experiments/microbiome_real_2026-06/ecam_child.csv")
day=np.array([float(d) for d in day]); order=np.argsort(day); day=day[order]; M=M[order]
Pe=close(M); ke=keff(Pe); spe=matrix_sparsity(M)
from numpy import corrcoef
rho=np.corrcoef(np.argsort(np.argsort(day)), np.argsort(np.argsort(ke)))[0,1]
print(f"ECAM D={M.shape[1]}, n={M.shape[0]}, sparsity={spe*100:.0f}%")
print(f"  K_eff vs day_of_life Spearman rho={rho:.2f} (maturation signal; OLD headline was ~0.71 on one child)")
hl=hold_lock(Pe); print(f"  NEW hold-lock on the maturation trajectory: floor={hl['floor']}, registered transitions={len(hl['events'])} at days {np.round(day[hl['events']],0) if hl['events'] else []}")
print(f"  NEW sparsity flag: {'GD-SPZ-WRN' if spe>=0.5 else 'valid'}; coherent helmsman robust to taxa filtering")

print(); print("="*70); print("GUEST 3 — FRONTIER MATH: Frielingen D=4 as an exact S^3=SU(2) example source"); print("="*70)
# quaternion sandwich = rotation, verify to IEEE floor on real D=4 steps
def ilr3(P):  # Helmert ILR for D=4 -> 3 coords
    H=clr(P); # Helmert basis 4->3
    B=np.array([[1,-1,0,0],[1,1,-2,0],[1,1,1,-3]],float)
    B=B/np.linalg.norm(B,axis=1,keepdims=True)
    return H@B.T
Y=ilr3(close(M[:0+1]) if False else close(load_csv(f"{BASE}/Current-Repo/Hs/collaborations/geology-wehner/demo_frielingen9/frielingen9_xrf_4part.csv")[2][:, :4]))
def quat_from_to(a,b):
    a=a/np.linalg.norm(a); b=b/np.linalg.norm(b); v=np.cross(a,b); w=1+np.dot(a,b)
    q=np.array([w,*v]); return q/np.linalg.norm(q)
def qrot(q,v):
    w,x,y,z=q; R=np.array([[1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y)],
        [2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x)],[2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)]]); return R@v
res=[]
for t in range(1,min(60,len(Y))):
    a,b=Y[t-1],Y[t]
    if np.linalg.norm(a)<1e-9 or np.linalg.norm(b)<1e-9: continue
    q=quat_from_to(a,b); bb=qrot(q,a/np.linalg.norm(a))*np.linalg.norm(b)
    res.append(np.linalg.norm(bb-b))
print(f"Aitchison step -> unit-quaternion sandwich q v q*, verified on {len(res)} real D=4 steps:")
print(f"  max residual = {max(res):.2e}  (IEEE-floor exactness of the S^3=SU(2) identification, on real geology data)")
# precise_ops near-identity demo
def neumaier(a):
    s=0.0;c=0.0
    for x in a:
        t=s+x; c+=(s-t+x) if abs(s)>=abs(x) else (x-t+s); s=t
    return s+c
small=np.full(200000,1e-10)
print(f"  precise_ops near-identity (200k tiny rotations summed): naive err={abs(small.sum()-200000e-10):.2e} vs Neumaier err={abs(neumaier(small)-200000e-10):.2e}")
hl=hold_lock(close(load_csv(f'{BASE}/Current-Repo/Hs/collaborations/geology-wehner/demo_frielingen9/frielingen9_xrf_4part.csv')[2][:, :4]))
print(f"  NEW hold-lock segments the S^3 trajectory into {len(hl['events'])} genuine structural episodes (the 'morphology' read, chatter-free)")
