import numpy as np, glob, csv, json
np.set_printoptions(suppress=True, precision=4)
B="/sessions/sharp-sleepy-bell/mnt/Claude CoWorker"
def closure(M):M=np.clip(M.astype(float),0,None);s=M.sum(1,keepdims=True);s[s==0]=1;return M/s
def clr(P):P=np.clip(P,1e-12,None);L=np.log(P);return L-L.mean(1,keepdims=True)

def derivative_tower(R,dt=1.0):
    # max MEANINGFUL order = last derivative whose magnitude still SHRINKS/holds vs the previous;
    # white-noise finite-differencing amplifies RMS by ~sqrt(2),sqrt(3),... -> growth ~>1.5 = noise-dominated.
    derivs=[R]; lab=["position","velocity","acceleration","jerk","snap","crackle"]
    for k in range(1,6):
        if len(derivs[-1])<3: break
        derivs.append(np.diff(derivs[-1],axis=0)/dt)
    mag=[np.linalg.norm(d,axis=1).mean() for d in derivs]
    order=1; ratios={}
    for k in range(2,len(derivs)):
        r=mag[k]/(mag[k-1]+1e-30); ratios[lab[k]]=round(float(r),2)
        if r<1.5: order=k
        else: break
    return derivs, {lab[k]:round(float(mag[k]),3) for k in range(1,len(derivs))}, ratios, order, lab

def mechanics(M,names,dt=1.0):
    P=closure(M); R=clr(P); o={"D":P.shape[1],"T":P.shape[0]}
    derivs,magd,ratios,order,lab=derivative_tower(R,dt)
    o["derivative_magnitudes"]=magd
    o["amplification_ratios(>~1.5 = noise)"]=ratios
    o["MAX_MEANINGFUL_ORDER"]=f"{order} ({lab[order]})"
    v=derivs[1]; a=derivs[2]; mass=(P[:-1]+P[1:])/2
    vv=a*0+v[:-1]; That=vv/(np.linalg.norm(vv,axis=1,keepdims=True)+1e-30)
    kappa=np.linalg.norm(a-(np.sum(a*That,1,keepdims=True))*That,axis=1)/(np.linalg.norm(vv,axis=1)**2+1e-30)
    p=mass*v; F=np.diff(p,axis=0)/dt; Tk=0.5*(mass*v*v).sum(1)
    L=np.array([np.linalg.norm(np.outer(R[t],p[t])-np.outer(p[t],R[t]))/np.sqrt(2) for t in range(len(p))])
    o["KINEMATIC"]={"speed_mean":round(float(np.linalg.norm(v,axis=1).mean()),3),"curvature_median":round(float(np.median(kappa)),3)}
    o["DYNAMIC"]={"kinetic_energy_mean":round(float(Tk.mean()),4),"force_mean_mag":round(float(np.linalg.norm(F,axis=1).mean()),4),
                  "power_mean":round(float(np.diff(Tk).mean()),5),"angular_momentum_mean":round(float(L.mean()),3)}
    o["INTEGRAL"]={"path_length":round(float(np.linalg.norm(v,axis=1).sum()),2),"displacement":round(float(np.linalg.norm(R[-1]-R[0])),2),
                   "path_efficiency":round(float(np.linalg.norm(R[-1]-R[0])/(np.linalg.norm(v,axis=1).sum()+1e-30)),3),
                   "action_intТ":round(float(Tk.sum()),2),"impulse_net":round(float(np.linalg.norm(p.sum(0))),3)}
    X=R-R.mean(0); s=np.linalg.svd(X,compute_uv=False); s=s[s>s.max()*1e-9]
    U,SS,Vt=np.linalg.svd(X,full_matrices=False)
    o["SPECTRAL"]={"motion_mode_singulars":[round(float(x),2) for x in s[:5]],"effective_rank":round(float((s.sum()**2)/(s**2).sum()),2),
                   "dominant_mode_carriers":[names[j] for j in np.argsort(-np.abs(Vt[0]))[:3]]}
    return o

def loadwide(p):
    rows=[r for r in open(p) if not r.startswith('#') and r.strip()];rd=list(csv.reader(rows))
    return rd[0][1:], np.array([[float(x) for x in r[1:]] for r in rd[1:]])
for c in ["deu","wld"]:
    nm,M=loadwide(glob.glob(f"{B}/Current-Repo/Hs/HCI-CNT/experiments/codawork2026/ember_{c}/*TWh.csv")[0])
    print(f"=== {c.upper()} ===\n"+json.dumps(mechanics(M,nm),indent=1)+"\n")
