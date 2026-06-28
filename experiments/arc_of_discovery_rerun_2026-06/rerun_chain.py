import csv, glob, os, numpy as np
np.set_printoptions(suppress=True)
B="/sessions/sharp-sleepy-bell/mnt/Claude CoWorker"
def clr(P):P=np.clip(P,1e-12,None);L=np.log(P);return L-L.mean(1,keepdims=True)
def close(M):M=np.clip(M.astype(float),0,None);s=M.sum(1,keepdims=True);s[s==0]=1;return M/s
def keff(P):P=np.clip(P,1e-12,None);P=P/P.sum(1,keepdims=True);H=-(P*np.log(P)).sum(1);return np.exp(H)
def helm(P,nm):d=np.abs(np.diff(clr(P),axis=0)).sum(0);return nm[int(np.argmax(d))]
def coh(P,nm):
    lP=np.log(np.clip(P,1e-12,None));T,D=P.shape;m=np.zeros(D)
    for i in range(D):
        for j in range(D):
            if i!=j:m[i]+=np.abs(np.diff(lP[:,i]-lP[:,j])).sum()
    return nm[int(np.argmax(m))]
def erank(P):
    X=clr(P);X=X-X.mean(0);s=np.linalg.svd(X,compute_uv=False);s=s[s>s.max()*1e-9]
    return round(float((s.sum()**2)/(s**2).sum()),2),min(P.shape[0]-1,P.shape[1]-1)
def holds(P):
    H=clr(P);st=np.linalg.norm(np.diff(H,axis=0),axis=1)
    if st.size<2:return 0
    med=np.median(st);mad=np.median(np.abs(st-med))*1.4826
    nz=max(1e-9,max(np.quantile(st,0.5)-mad,np.quantile(st,0.25)));up,lo=4*nz,2*nz
    s="HOLD";ev=0;ref=0
    for t,m in enumerate(st):
        if s=="HOLD" and m>up:s="MOVING"
        elif s=="MOVING" and m<lo:
            if np.linalg.norm(H[t+1]-H[ref])>=3*nz:ev+=1;ref=t+1
            s="HOLD"
    return ev
def sp(M):return float((M<=0).mean())
def loadwide(path):
    rows=[r for r in open(path) if not r.startswith('#') and r.strip()]
    rd=list(csv.reader(rows));hdr=rd[0]
    data=[]
    for r in rd[1:]:
        try: data.append([float(x) for x in r[1:]])
        except: 
            try: data.append([float(x) for x in r])  # no label col
            except: pass
    M=np.array(data); nm=hdr[1:] if M.shape[1]==len(hdr)-1 else hdr
    return nm,M

# discover chain CSVs in order
groups=[
 ("CNT/EMBER", sorted(glob.glob(f"{B}/Current-Repo/Hs/HCI-CNT/experiments/codawork2026/ember_*/*generation_TWh.csv"))),
 ("CNT/geochem+ref+domain", sorted(glob.glob(f"{B}/Current-Repo/Hs/HCI-CNT/experiments/domain/*/*input.csv")+glob.glob(f"{B}/Current-Repo/Hs/HCI-CNT/experiments/reference/*/*input.csv"))),
 ("CNT/extended", sorted(glob.glob(f"{B}/Current-Repo/Hs/HCI-CNT/experiments/extended/*/*input.csv"))),
 ("Hs-NN(real)", [f"{B}/Current-Repo/Hs/experiments/Hs-25_Cosmic_Energy_Budget/Hs-25_cosmic_energy_budget.csv"]),
]
print(f"{'experiment':42} {'D':>3} {'N':>5} {'spars%':>6} {'CLRhelm':>16} {'coh==':>5} {'effRank':>9} {'Keff_end':>8} {'holds':>5}")
print("-"*108)
n=0
for gname,paths in groups:
    for p in paths:
        try:
            nm,M=loadwide(p)
            if M.ndim!=2 or M.shape[0]<3 or M.shape[1]<2: continue
            P=close(M); er=erank(P); h=helm(P,nm); c=coh(P,nm)
            name=os.path.basename(os.path.dirname(p)) or os.path.basename(p)
            print(f"{name[:42]:42} {M.shape[1]:>3} {M.shape[0]:>5} {sp(M)*100:>6.1f} {str(h)[:16]:>16} {str(c==h):>5} {er[0]:>5}/{er[1]:<3} {keff(P)[-1]:>8.2f} {holds(P):>5}")
            n+=1
        except Exception as e:
            print(f"  [skip] {os.path.basename(p)}: {e}")
print(f"\n{n} chain experiments re-run on the CURRENT guard-aware engine.")
