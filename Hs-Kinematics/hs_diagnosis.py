#!/usr/bin/env python3
"""
Hˢ diagnosis — a deterministic language of diagnosis that lets a composition SAY what it is doing.

The same deterministic readings the kinematics engine computes are composed, by a fixed grammar,
into a human-readable narrative — and the language **expands automatically with complexity**: a
2-part system has one or two words to say; a microbiome of hundreds of taxa has many voices. The
number of "active voices" is not chosen — it is the count of parts actually doing something
(deterministic), so the system tells you what it is doing in exactly as many words as it has
structure to fill.

Deterministic by construction: same input -> same words -> same hash. An LLM may *polish* the
phrasing, but the canonical utterance is rule-generated from the engine state, so it carries the
same trust as the numbers. Honest: if the system is at rest, it says so and stops; the fringe
note is Tier-3 (a clue, never a claim).

numpy + stdlib only. Author: Peter Higgins (human authorship for claims); AI-assisted per
HUF-STD-001. Honest-broker.
"""
import numpy as np, hashlib, json

def closure(M): M=np.clip(np.asarray(M,float),0,None); s=M.sum(1,keepdims=True); s[s==0]=1; return M/s
def clr(P): P=np.clip(P,1e-12,None); L=np.log(P); return L-L.mean(1,keepdims=True)
def keff(P): P=np.clip(closure(P),1e-12,None); return np.exp(-(P*np.log(P)).sum(1))

def _hold(P):
    H=clr(P); st=np.linalg.norm(np.diff(H,axis=0),axis=1)
    if st.size<2: return 1e-9,[],0.0
    md=np.median(st); mad=np.median(np.abs(st-md))*1.4826
    noise=max(1e-9,max(np.quantile(st,0.5)-mad,np.quantile(st,0.25)),1e-12); up,lo=4*noise,2*noise
    s="HOLD"; ev=[]; ref=0
    for t,m in enumerate(st):
        if s=="HOLD" and m>up: s="MOVING"
        elif s=="MOVING" and m<lo:
            if np.linalg.norm(H[t+1]-H[ref])>=3*noise: ev.append(t+1); ref=t+1
            s="HOLD"
    return noise,ev,float(st.max())

def _movers(P,names,frac=0.12):
    mass=(P[:-1]+P[1:])/2; v=np.diff(clr(P),axis=0); mom=(mass*v).sum(0)  # net per-carrier momentum (mass*velocity)
    mag=np.abs(mom); thr=frac*(mag.max()+1e-30)
    return [(names[j], "gaining" if mom[j]>0 else "shedding", round(float(mom[j]),4))
            for j in np.argsort(-mag) if mag[j]>=thr]

def diagnose(M, names=None):
    M=np.asarray(M,float); names=list(names) if names is not None else [f"c{j}" for j in range(M.shape[1])]
    P=closure(M); Ks,Ke=float(keff(P)[0]),float(keff(P)[-1]); noise,ev,maxstep=_hold(P)
    X=clr(P); X=X-X.mean(0); s=np.linalg.svd(X,compute_uv=False); s=s[s>s.max()*1e-9] if s.max()>0 else s
    rank=float((s.sum()**2)/(s**2).sum()) if s.size else 0.0
    # honest gate: at rest -> one sentence, then stop
    if maxstep < 4*noise and maxstep < 1e-6:
        out={"narrative":"The system is holding steady — at rest below its own noise floor. Nothing to report.",
             "active_voices":0,"utterances":[],"complexity_words":0}
        out["hash"]=hashlib.sha256(out["narrative"].encode()).hexdigest(); return out
    movers=_movers(P,names)
    gaining=[m[0] for m in movers if m[1]=="gaining"]; shedding=[m[0] for m in movers if m[1]=="shedding"]
    trend="concentrating" if Ke<Ks-0.05 else ("diversifying" if Ke>Ks+0.05 else "steady")
    # utterances (subject, verb, object) — the deterministic semantic output; count scales with complexity
    utt=[("the whole", trend, f"effective spread {Ks:.2f} -> {Ke:.2f}")]
    for nm,d,val in movers: utt.append((nm, d, f"net momentum {val:+.3f}"))
    if ev: utt.append(("the system","changed state",f"{len(ev)} time(s)"))
    if rank>1.5: utt.append(("the motion","runs in",f"{round(rank,1)} independent directions at once"))
    # human narrative — clauses scale with the number of active voices
    sent=[]
    if movers: sent.append(f"{movers[0][0]} is steering ({movers[0][1]}).")
    if len(movers)>1:
        if gaining: sent.append("Weight is moving toward " + ", ".join(gaining[:8]) + ("…" if len(gaining)>8 else "") + ".")
        if shedding: sent.append("It is moving away from " + ", ".join(shedding[:8]) + ("…" if len(shedding)>8 else "") + ".")
    sent.append(f"The mixture is {trend} (effective spread {Ks:.2f} → {Ke:.2f}).")
    if ev: sent.append(f"It changed state {len(ev)} time(s).")
    if rank>1.5: sent.append(f"The motion runs in about {round(rank)} independent directions.")
    sent.append(f"({len(movers)} of {P.shape[1]} parts have something to say; the rest are quiet.)")
    out={"narrative":" ".join(sent),"active_voices":len(movers),"complexity_words":len(utt),
         "utterances":[{"subject":a,"verb":b,"object":c} for a,b,c in utt]}
    out["hash"]=hashlib.sha256(json.dumps(out["utterances"],sort_keys=True).encode()).hexdigest()
    return out

if __name__=="__main__":
    rng=np.random.default_rng(0)
    # SIMPLE D=2 -> one or two voices
    g=np.linspace(.7,.55,40); M2=np.c_[g,1-g]
    print("SIMPLE (D=2):", diagnose(M2,["Gold","Silver"])["narrative"], "\n")
    # MODERATE D=8 energy-like
    base=np.array([.30,.22,.18,.12,.08,.04,.04,.02]); M8=np.maximum(base+np.cumsum(rng.normal(0,.012,(40,8)),0),1e-4)
    d8=diagnose(M8,["Coal","Gas","Hydro","Nuclear","Wind","Solar","Bio","Other"]); print("MODERATE (D=8):", d8["narrative"], "\n")
    # COMPLEX D=60 microbiome-like -> many voices
    taxa=[f"taxon_{i}" for i in range(60)]
    Mb=np.abs(rng.lognormal(0,1.2,(40,60))+np.cumsum(rng.normal(0,.05,(40,60)),0));
    dC=diagnose(Mb,taxa); print(f"COMPLEX (D=60): active_voices={dC['active_voices']}, words={dC['complexity_words']}\n  ", dC["narrative"][:400])
