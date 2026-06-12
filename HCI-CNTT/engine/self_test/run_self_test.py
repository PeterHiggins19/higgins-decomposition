"""CN-TT v4 BIST — proves the engine kernel reproduces the 2026-06-10 tiling proof
numbers and D=4 quaternion exactness from INSIDE the engine. Dated, hash-signed."""
import sys, time
from pathlib import Path
import numpy as np
ENG = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENG))
import geometry as geo, quaternion as quat, atlas as atl, provenance as prov
import cntt

PASS = True
def check(name, cond, detail=""):
    global PASS
    ok = bool(cond); PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")

print("== CN-TT v4 self-test ==")

# (1) D=4 quaternion exactness: sandwich == Rodrigues; atan2 beats arccos near 0
rng = np.random.default_rng(1); maxerr = 0.0
for _ in range(20000):
    v = rng.normal(size=3); ax = rng.normal(size=3); ax/=np.linalg.norm(ax); th = rng.uniform(0,np.pi)
    q = quat.unit_quaternion_from_axis_angle(ax, th)
    qv = quat.sandwich(q, v)
    ref = np.cos(th)*v + (1-np.cos(th))*np.dot(ax,v)*ax + np.sin(th)*np.cross(ax,v)
    maxerr = max(maxerr, np.max(np.abs(qv-ref)))
check("D=4 sandwich == Rodrigues (<=1e-12)", maxerr <= 1e-12, f"max_err={maxerr:.2e}")
eps=1e-9; u0=np.array([1.0,0,0]); u1=np.array([np.cos(eps),np.sin(eps),0.0])
atan2_err = abs(quat.angle_between(u0,u1)-eps)/eps
arccos_err = abs(np.arccos(np.clip(np.dot(u0,u1),-1,1))-eps)/eps
check("atan2 angle exact where arccos fails near 0", atan2_err < 1e-6 and arccos_err > 0.5,
      f"atan2_relerr={atan2_err:.0e} arccos_relerr={arccos_err:.2f}")

# (2) lossless reconstruction on connected atlas (sliding + hierarchical)
def rand_comp(D): 
    x = rng.dirichlet(np.ones(D)*0.3); return x/x.sum()
errs_sl=[]; errs_tr=[]
for D in [16,64,256]:
    for _ in range(5):
        x=rand_comp(D)
        e_sl=atl.reconstruct_clr(D, atl.edges_from_charts(atl.sliding_window_atlas(D)), x)[1]
        e_tr=atl.reconstruct_clr(D, atl.edges_from_charts(atl.hierarchical_atlas(D)), x)[1]
        errs_sl.append(e_sl); errs_tr.append(e_tr)
check("connected sliding atlas lossless (<1e-9)", max(errs_sl) < 1e-9, f"max_err={max(errs_sl):.2e}")
check("connected tree atlas lossless (<1e-9)", max(errs_tr) < 1e-9, f"max_err={max(errs_tr):.2e}")

# (3) overlap necessity: disjoint atlas fails
D=64; x=rand_comp(D)
disjoint=[tuple(range(s,s+4)) for s in range(0,D,4)]
_,e_dis,nc=atl.reconstruct_clr(D, atl.edges_from_charts(disjoint), x)
check("disjoint atlas rank-deficient (fails + >1 component)", e_dis > 0.1 and nc>1, f"err={e_dis:.2e} comps={nc}")

# (4) native D=16 unnecessary: D=16 move reconstructed from D=4 charts
D=16; x0=rng.dirichlet(np.ones(D)); x1=rng.dirichlet(np.ones(D))
ed=atl.edges_from_charts(atl.hierarchical_atlas(D))
mv_true=geo.clr(x1)-geo.clr(x0)
mv_rec=atl.reconstruct_clr(D,ed,x1)[0]-atl.reconstruct_clr(D,ed,x0)[0]
mverr=float(np.max(np.abs(mv_rec-mv_true)))
check("D=16 move reproduced from D=4 charts (<=1e-12)", mverr<=1e-12, f"move_err={mverr:.2e}")

# (5) hierarchical holds precision at high D (D=100k tree vs sliding)
D=100000; x=rand_comp(D)
t0=time.perf_counter(); e_tr=atl.reconstruct_clr(D, atl.edges_from_charts(atl.hierarchical_atlas(D)), x)[1]; dt=time.perf_counter()-t0
check("tree atlas precise at D=100k (<1e-10)", e_tr < 1e-10, f"err={e_tr:.2e} time={dt:.2f}s")

# (6) full engine run (D=4) + determinism (same input -> same content hash)
rowsD4 = np.abs(rng.normal(size=(40,4)))+0.01
p1=cntt.cntt_run(rowsD4, carriers=list("ABCD"))
p2=cntt.cntt_run(rowsD4, carriers=list("ABCD"))
check("engine D=4 run lossless", p1["atlas"]["lossless"], f"recon_err={p1['atlas']['reconstruction_max_err']:.2e}")
check("determinism: identical content hash on rerun", p1["diagnostics"]["cntt_content_sha256"]==p2["diagnostics"]["cntt_content_sha256"],
      f"sha={p1['diagnostics']['cntt_content_sha256'][:16]}...")

receipt={"engine":prov.ENGINE_VERSION,"date":time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
         "verdict":"PASS" if PASS else "FAIL"}
receipt["receipt_sha256"]=prov.canonical_sha256(receipt)
print(f"\n== VERDICT: {'PASS' if PASS else 'FAIL'} ==")
print(f"receipt: {receipt['receipt_sha256'][:24]}  ({receipt['date']})")
sys.exit(0 if PASS else 1)
