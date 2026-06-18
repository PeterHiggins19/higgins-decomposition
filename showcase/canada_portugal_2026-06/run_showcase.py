import csv, numpy as np
np.set_printoptions(suppress=True)
BASE="/sessions/sharp-sleepy-bell/mnt/Claude CoWorker"
def clr(P): P=np.clip(P,1e-12,None); L=np.log(P); return L-L.mean(1,keepdims=True)
def close(M): M=np.clip(M.astype(float),0,None); s=M.sum(1,keepdims=True); s[s==0]=1; return M/s
def keff(P): P=np.clip(P,1e-12,None);P=P/P.sum(1,keepdims=True);H=-(P*np.log(P)).sum(1);return np.exp(H)
def cl_helm(P,names): d=np.abs(np.diff(clr(P),axis=0)).sum(0); return names[int(np.argmax(d))]
def coh_helm(P,names):
    lP=np.log(np.clip(P,1e-12,None));T,D=P.shape;m=np.zeros(D)
    for i in range(D):
        for j in range(D):
            if i!=j: m[i]+=np.abs(np.diff(lP[:,i]-lP[:,j])).sum()
        m[i]/=(D-1)
    return names[int(np.argmax(m))]
def eff_rank(P):
    X=clr(P);X=X-X.mean(0);s=np.linalg.svd(X,compute_uv=False);s=s[s>s.max()*1e-9]
    return round(float((s.sum()**2)/(s**2).sum()),2), min(P.shape[0]-1,P.shape[1]-1)
def hold_lock(P):
    H=clr(P);st=np.linalg.norm(np.diff(H,axis=0),axis=1)
    if st.size==0:return {"floor":0,"ev":[]}
    med=np.median(st);mad=np.median(np.abs(st-med))*1.4826
    noise=max(1e-9,max(np.quantile(st,0.5)-mad,np.quantile(st,0.25)));up,lo=4*noise,2*noise
    s="HOLD";ev=[];ref=0
    for t,m in enumerate(st):
        if s=="HOLD" and m>up:s="MOVING"
        elif s=="MOVING" and m<lo:
            if np.linalg.norm(H[t+1]-H[ref])>=3*noise:ev.append(t+1);ref=t+1
            s="HOLD"
    return {"floor":round(noise,3),"ev":ev,"n_move":int((st>up).sum())}
def deceptive(P):
    H=clr(P);tv=0.5*np.abs(np.diff(close(P),axis=0)).sum(1);ke=keff(P);dk=np.diff(ke)
    med=np.median(tv); return int(((dk<0)&(tv<=med)).sum())
def sparsity(M): return float((M<=0).mean())

# ---------- ENERGY: Canada + Portugal monthly EMBER ----------
rows=list(csv.DictReader(open(f"{BASE}/DATA/Energy/monthly_full_release_long_format.csv")))
def fuelmat(area):
    d={}
    for r in rows:
        if r["Area"]==area and r["Category"]=="Electricity generation" and r["Subcategory"]=="Fuel" and r["Unit"]=="TWh":
            d.setdefault(r["Date"],{})[r["Variable"]]=float(r["Value"] or 0)
    fuels=sorted({f for v in d.values() for f in v}); dates=sorted(d)
    M=np.array([[d[dt].get(f,0.0) for f in fuels] for dt in dates]); return dates,fuels,M
print("="*68);print("ENERGY SHOWCASE — Canada + Portugal, monthly EMBER, NEW engine");print("="*68)
for area in ("Canada","Portugal"):
    dates,fuels,M=fuelmat(area); P=close(M); sp=sparsity(M)
    print(f"\n[{area}] {len(dates)} months {dates[0]}..{dates[-1]} | D={len(fuels)} fuels | sparsity {sp*100:.1f}%")
    print(f"  fuels: {fuels}")
    print(f"  CLR helmsman: {cl_helm(P,fuels)}  |  coherent helmsman: {coh_helm(P,fuels)}")
    er=eff_rank(P); print(f"  effective rank: {er[0]} of {er[1]}")
    print(f"  K_eff: {keff(P)[0]:.2f} -> {keff(P)[-1]:.2f}  (diversification)")
    hl=hold_lock(P); print(f"  hold-lock: floor={hl['floor']}, GENUINE structural transitions={len(hl['ev'])} at {[dates[i] for i in hl['ev']]}")
    print(f"  deceptive-drift months: {deceptive(P)}")
    nz=[fuels[j] for j in range(len(fuels)) if (M[:,j]<=0).any()]
    print(f"  NEW zero/sparsity guard handles carriers with zero months: {nz or 'none'} (old engine floored these to artifacts)")

# ---------- WINE: public UCI wine chemistry (3 cultivars) ----------
print("\n"+"="*68);print("WINE SHOWCASE — public UCI wine chemistry (178 wines, 13 attrs, 3 cultivars)");print("="*68)
import sklearn.datasets as sk
W=sk.load_wine(); X=W.data; y=W.target; names=list(W.feature_names)
P=close(X)  # treat the 13 chemical attributes as a composition (relative chemical profile)
print(f"  D={X.shape[1]} chemical attributes, n={X.shape[0]} wines, 3 cultivars; sparsity {sparsity(X)*100:.0f}%")
# which attributes separate the cultivars (helmsman of between-class CLR variation)
H=clr(P); centroids=np.array([H[y==k].mean(0) for k in range(3)])
betw=np.abs(centroids-centroids.mean(0)).sum(0)
top=np.argsort(-betw)[:4]
print(f"  STATIC read (the standard CoDa apparatus): top discriminating chemistry between cultivars:")
for i in top: print(f"     {names[i]}  (between-cultivar CLR spread {betw[i]:.2f})")
er=eff_rank(P); print(f"  effective rank of the chemical profile: {er[0]} of {er[1]}")
print(f"  (cross-sectional -> Hs serves the static CoDa apparatus: ternary/biplot/variation matrix; no time axis, no dynamics forced)")
