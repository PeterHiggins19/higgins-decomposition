import numpy as np, glob, csv, os
np.set_printoptions(suppress=True)
B="/sessions/sharp-sleepy-bell/mnt/Claude CoWorker"
def closure(M):M=np.clip(M.astype(float),0,None);s=M.sum(1,keepdims=True);s[s==0]=1;return M/s
def clr(P):P=np.clip(P,1e-12,None);L=np.log(P);return L-L.mean(1,keepdims=True)

def compositional_momentum(M, names, window=None, coh_floor=0.15, mag_floor=1e-6):
    """Each carrier: mass=share, velocity=Δclr, momentum=mass·velocity. Returns the system
    'arrow of intent' = net momentum vector (where mass flows from/to), its magnitude, and a
    COHERENCE (directed arrow vs churn). NOT a prediction — the present vector of motion."""
    P=closure(M); C=clr(P); v=np.diff(C,axis=0)             # Aitchison velocity Δclr  (T-1,D)
    m=(P[:-1]+P[1:])/2                                       # mass = mean share over the step
    p=m*v                                                    # per-carrier momentum         (T-1,D)
    seg=p if window is None else p[-window:]
    Pnet=seg.sum(0)                                          # net system momentum vector   (D,)
    mag=float(np.linalg.norm(Pnet))
    permag=np.linalg.norm(seg,axis=1)                        # per-step system momentum magnitude
    coherence=float(np.linalg.norm(seg.sum(0))/(permag.sum()+1e-30))   # directed[~1] vs churn[~0]
    ke=0.5*(m*v*v).sum(1)                                    # kinetic energy of compositional motion
    order=np.argsort(-Pnet)
    gaining=[(names[j],round(float(Pnet[j]),4)) for j in order if Pnet[j]>0][:3]
    losing =[(names[j],round(float(Pnet[j]),4)) for j in order[::-1] if Pnet[j]<0][:3]
    # honesty guard (mirrors resolvability): no directed arrow if churning or motionless
    code=None
    if mag<mag_floor: code="MO-NUL-WRN"          # no resolvable momentum (at rest)
    elif coherence<coh_floor: code="MO-DIF-WRN"  # diffuse: motion present but no directed arrow (churn)
    helm=names[int(np.argmax(np.abs(v).sum(0)))] # mass-blind helmsman, for contrast
    return {"arrow_gaining":gaining,"arrow_losing":losing,"magnitude":round(mag,4),
            "coherence":round(coherence,3),"ke_mean":round(float(ke.mean()),5),
            "helmsman_massblind":helm,"code":code}

def loadwide(p):
    rows=[r for r in open(p) if not r.startswith('#') and r.strip()]; rd=list(csv.reader(rows))
    hdr=rd[0]; M=np.array([[float(x) for x in r[1:]] for r in rd[1:]]); return hdr[1:],M

print("COMPOSITIONAL MOMENTUM — the arrow of intent (real EMBER energy transitions)\n")
for area in ["deu","gbr","jpn","ind","wld"]:
    f=glob.glob(f"{B}/Current-Repo/Hs/HCI-CNT/experiments/codawork2026/ember_{area}/*generation_TWh.csv")
    if not f: continue
    nm,M=loadwide(f[0]); r=compositional_momentum(M,nm)
    print(f"[{area.upper()}] arrow: mass flowing TO {[g[0] for g in r['arrow_gaining']]}  FROM {[l[0] for l in r['arrow_losing']]}")
    print(f"       magnitude={r['magnitude']}  coherence={r['coherence']} {'(directed arrow)' if r['coherence']>=0.15 else '(diffuse/churn)'}  code={r['code']}")
    print(f"       vs mass-blind helmsman (fastest mover) = {r['helmsman_massblind']}\n")
# recent-window arrow (last 8 years) vs whole-series, for one country
nm,M=loadwide(glob.glob(f"{B}/Current-Repo/Hs/HCI-CNT/experiments/codawork2026/ember_gbr/*TWh.csv")[0])
rw=compositional_momentum(M,nm,window=8)
print(f"[GBR last-8-yr window] arrow TO {[g[0] for g in rw['arrow_gaining']]} FROM {[l[0] for l in rw['arrow_losing']]} | coherence={rw['coherence']}")
