#!/usr/bin/env python3
"""
Self-contained runner for the Hs SO(4) / dual-quaternion SE(3) self-test.

Single file (engine + battery) so it can be reproduced with no imports beyond numpy.
Emits a canonical-JSON SHA-256 receipt (the project determinism contract). Identical
math to dual_quaternion_se3.py + test_so4_dual_quaternion.py; this is the reproducible
all-in-one. Author: Peter Higgins; AI-assisted per HUF-STD-001. Deterministic (seed 4).
"""
import hashlib, json, math, sys
import numpy as np

# ── quaternion + dual-quaternion algebra ──────────────────────────────────
def qmul(a, b):
    w1, x1, y1, z1 = a; w2, x2, y2, z2 = b
    return np.array([w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
                     w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2])
def qconj(a): return np.array([a[0], -a[1], -a[2], -a[3]])
def R_from_quat(q):
    w, x, y, z = q
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                     [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
def twin_matrix(qL, qR):
    M = np.zeros((4, 4))
    for k in range(4):
        e = np.zeros(4); e[k] = 1.0
        M[:, k] = qmul(qmul(qL, e), qconj(qR))
    return M
def dq_from_pose(q_r, t):
    q_r = np.asarray(q_r, float)
    q_d = 0.5 * qmul(np.array([0.0, t[0], t[1], t[2]]), q_r)
    return np.concatenate([q_r, q_d])
def dq_mul(A, B):
    ar, ad, br, bd = A[:4], A[4:], B[:4], B[4:]
    return np.concatenate([qmul(ar, br), qmul(ar, bd) + qmul(ad, br)])
def dq_point_conj(A):                       # eta* = qr* - eps qd*  (point-transform conjugate)
    return np.concatenate([qconj(A[:4]), -qconj(A[4:])])
def dq_pose(A):                             # exact read-back of (q_r, t)
    q_r = A[:4]; t_quat = 2.0 * qmul(A[4:], qconj(q_r))
    return q_r, t_quat[1:]
def dq_transform_point(A, p):
    P = np.concatenate([np.array([1.0, 0, 0, 0]), np.array([0.0, p[0], p[1], p[2]])])
    return dq_mul(dq_mul(A, P), dq_point_conj(A))[4:][1:]
def dq_to_screw(A):
    q_r, t = dq_pose(A); w = float(np.clip(q_r[0], -1, 1))
    theta = 2.0 * math.acos(w); s = math.sqrt(max(0.0, 1.0 - w * w))
    if s < 1e-12:
        nt = np.linalg.norm(t); l = t/nt if nt > 1e-15 else np.array([0.,0.,1.])
        return l, 0.0, float(nt)
    l = q_r[1:]/s; d = float(np.dot(t, l)); return l, float(theta), d

LX=np.array([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]],float)
LY=np.array([[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]],float)
LZ=np.array([[0,0,0,-1],[0,0,-1,0],[0,1,0,0],[1,0,0,0]],float)
RX=np.array([[0,-1,0,0],[1,0,0,0],[0,0,0,1],[0,0,-1,0]],float)
RY=np.array([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]],float)
RZ=np.array([[0,0,0,-1],[0,0,1,0],[0,-1,0,0],[1,0,0,0]],float)
def comm(A, B): return A@B - B@A
def helmert(D):
    B = np.zeros((D-1, D))
    for i in range(1, D):
        B[i-1, :i] = 1.0/i; B[i-1, i] = -1.0; B[i-1] *= math.sqrt(i/(i+1.0))
    return B
def homogeneous(q_r, t):
    H = np.eye(4); H[:3, :3] = R_from_quat(q_r); H[:3, 3] = t; return H
def runit(rng): q = rng.standard_normal(4); return q/np.linalg.norm(q)

def run(seed=4, trials=4000):
    rng = np.random.default_rng(seed); out = {}
    # T1 so(4)=so(3)+so(3)
    L=[LX,LY,LZ]; R=[RX,RY,RZ]
    eps=np.array([[[0,0,0],[0,0,1],[0,-1,0]],[[0,0,-1],[0,0,0],[1,0,0]],[[0,1,0],[-1,0,0],[0,0,0]]],float)
    eLL=eRR=eLR=0.0
    for i in range(3):
        for j in range(3):
            tL=2.0*sum(eps[i,j,k]*L[k] for k in range(3)); tR=-2.0*sum(eps[i,j,k]*R[k] for k in range(3))
            eLL=max(eLL,np.max(np.abs(comm(L[i],L[j])-tL))); eRR=max(eRR,np.max(np.abs(comm(R[i],R[j])-tR)))
            eLR=max(eLR,np.max(np.abs(comm(L[i],R[j]))))
    out["T1_so4_split"]={"LL_err":float(eLL),"RR_err":float(eRR),"LR_err":float(eLR),"pass":bool(max(eLL,eRR,eLR)<1e-12)}
    # T2 SO(4)
    orth=det=0.0
    for _ in range(trials):
        M=twin_matrix(runit(rng),runit(rng)); orth=max(orth,np.max(np.abs(M.T@M-np.eye(4)))); det=max(det,abs(np.linalg.det(M)-1.0))
    out["T2_SO4_two_sided"]={"orth_resid":float(orth),"det_dev":float(det),"trials":trials,"pass":bool(max(orth,det)<1e-12)}
    # T3 double cover
    cov=0.0
    for _ in range(trials):
        qL,qR=runit(rng),runit(rng); cov=max(cov,np.max(np.abs(twin_matrix(qL,qR)-twin_matrix(-qL,-qR))))
    out["T3_double_cover"]={"max_diff":float(cov),"trials":trials,"pass":bool(cov<1e-12)}
    # T4 pose round-trip
    rq=rt=0.0
    for _ in range(trials):
        q=runit(rng); t=rng.standard_normal(3)*10; q2,t2=dq_pose(dq_from_pose(q,t))
        if np.dot(q,q2)<0: q2=-q2
        rq=max(rq,np.max(np.abs(q-q2))); rt=max(rt,np.max(np.abs(t-t2)))
    out["T4_pose_roundtrip"]={"rot_resid":float(rq),"trans_resid":float(rt),"trials":trials,"pass":bool(max(rq,rt)<1e-12)}
    # T5 motion composition == matrix
    ce=0.0
    for _ in range(trials):
        q1,t1=runit(rng),rng.standard_normal(3)*5; q2,t2=runit(rng),rng.standard_normal(3)*5
        qr,tr=dq_pose(dq_mul(dq_from_pose(q1,t1),dq_from_pose(q2,t2)))
        ce=max(ce,np.max(np.abs(homogeneous(qr,tr)-homogeneous(q1,t1)@homogeneous(q2,t2))))
    out["T5_motion_composition"]={"dq_vs_homog_resid":float(ce),"trials":trials,"pass":bool(ce<1e-12)}
    # T6 four-form conformance on a 4-part composition's ILR point
    H4=helmert(4); ff=0.0
    for _ in range(trials):
        comp=rng.dirichlet(np.ones(4)); clr=np.log(comp)-np.log(comp).mean(); p=H4@clr
        q=runit(rng); t=rng.standard_normal(3)*7; eta=dq_from_pose(q,t)
        a=dq_transform_point(eta,p)                       # A dual-quaternion sandwich
        qr,tr=dq_pose(eta); b=R_from_quat(qr)@p+tr        # B extract + Rp+t
        c=(homogeneous(q,t)@np.array([*p,1.0]))[:3]       # C homogeneous 4x4
        ff=max(ff,max(np.max(np.abs(a-b)),np.max(np.abs(a-c)),np.max(np.abs(b-c))))
    out["T6_four_form_conformance"]={"max_disagreement_A_B_C":float(ff),"trials":trials,"pass":bool(ff<1e-12)}
    # T6b screw rotation recovery
    se=0.0
    for _ in range(trials):
        q=runit(rng); q=-q if q[0]<0 else q; t=rng.standard_normal(3)*7
        l,theta,d=dq_to_screw(dq_from_pose(q,t)); q2=np.array([math.cos(theta/2),*(math.sin(theta/2)*l)])
        se=max(se,np.max(np.abs(q-q2)))
    out["T6b_screw_rotation_recovery"]={"max_resid":float(se),"trials":trials,"pass":bool(se<1e-10)}
    return out

def receipt(out):
    def rnd(o):
        if isinstance(o,bool): return o
        if isinstance(o,float): return round(o,15)
        if isinstance(o,dict): return {k:rnd(v) for k,v in o.items()}
        if isinstance(o,list): return [rnd(v) for v in o]
        return o
    return hashlib.sha256(json.dumps(rnd(out),sort_keys=True,separators=(",",":")).encode()).hexdigest()

def main():
    out=run(); h1=receipt(out); h2=receipt(run())
    out["experiment"]="so4_dual_quaternion_se3_6dof"; out["seed"]=4
    out["T7_determinism"]={"rerun_hash_matches":bool(h1==h2),"pass":bool(h1==h2)}
    out["content_sha256"]=h1
    checks=[v for v in out.values() if isinstance(v,dict) and "pass" in v]
    ap=all(c["pass"] for c in checks); out["ALL_PASS"]=bool(ap)
    print(json.dumps(out,indent=2)); print("\n"+"="*60)
    for k,v in out.items():
        if isinstance(v,dict) and "pass" in v: print(f"  [{'PASS' if v['pass'] else 'FAIL'}]  {k}")
    print(f"\n  RECEIPT content_sha256 = {h1}\n  ALL_PASS = {ap}"); print("="*60)
    sys.exit(0 if ap else 1)

if __name__=="__main__": main()
