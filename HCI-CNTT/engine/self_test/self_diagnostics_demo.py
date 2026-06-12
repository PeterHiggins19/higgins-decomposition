"""CN-TT v4 — demonstrate (1) stage lifecycle control (READY/RUNNING/HALTED + halt/start)
and (2) internal vs external shock differentiation (FDIR)."""
import sys
from pathlib import Path
import numpy as np
ENG = Path(__file__).resolve().parent.parent; sys.path.insert(0, str(ENG))
from pipeline import Pipeline
from stage_controller import StageController
from stages import AdaptStage, TreatStage, CalibrateStage, GeometryStage, AtlasStage, NavigateStage
import shock_diagnostics as sd

PASS = True
def chk(name, cond, detail=""):
    global PASS; ok = bool(cond); PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")

print("== (1) Stage lifecycle control ==")
stages = [AdaptStage(), TreatStage(), CalibrateStage(), GeometryStage(), AtlasStage(), NavigateStage()]
names = [s.name for s in stages]
pipe = Pipeline(stages); ctrl = StageController(names, owner="CN-TT")
rng = np.random.default_rng(1); raw = np.abs(rng.normal(size=(10,4)))+0.05
ctx0 = {"header": ["t","A","B","C","D"], "raw_rows": [[str(i)]+[f"{v}" for v in raw[i]] for i in range(10)]}

r = pipe.run(ctx0, controller=ctrl)
ran = [c["stage"] for c in r["_provenance"] if c.get("ran")]
chk("normal run: all 6 stages ran + READY", len(ran)==6 and all(v=="READY" for v in r["_stage_states"].values()),
    f"states={r['_stage_states']}")

ctrl.halt("atlas")
r = pipe.run(ctx0, controller=ctrl)
chk("HALT atlas -> pipeline halts at atlas", r.get("_halted_at")=="atlas", f"halted_at={r.get('_halted_at')}")
chk("HALT atlas -> downstream (navigate) did NOT run", "navigation" not in r,
    f"atlas state={r['_stage_states']['atlas']}, upstream geometry={r['_stage_states']['geometry']}")

ctrl.start("atlas")
r = pipe.run(ctx0, controller=ctrl)
chk("START atlas -> completes, all READY", "navigation" in r and r["_stage_states"]["atlas"]=="READY")
print(f"  states after start: {r['_stage_states']}")

print("\n== (2) Internal vs external shock differentiation ==")
D = 8; rng = np.random.default_rng(7)
base = rng.normal(0,1,D); base -= base.mean()
def channels(center, noise=0.02, fault=None, fault_mag=0.0):
    C = np.array([center + rng.normal(0,noise,D) for _ in range(3)]); C = C - C.mean(axis=1,keepdims=True)
    if fault is not None:
        C[fault] += fault_mag*rng.normal(0,1,D); C[fault] -= C[fault].mean()
    return C
prev = channels(base); prev_cons = np.median(prev, axis=0)
shift = rng.normal(0,1,D); shift -= shift.mean()

r_ext = sd.classify_shock(channels(base + 1.5*shift), prev_cons)
chk("EXTERNAL shock (3 channels coherent) -> EXTERNAL", r_ext["class"]=="EXTERNAL",
    f"incoherence={r_ext['incoherence_max_resid']:.3f} shock_mag={r_ext['shock_magnitude']:.2f}")
r_int = sd.classify_shock(channels(base, fault=1, fault_mag=2.0), prev_cons)
chk("INTERNAL fault (channel 1 diverges) -> INTERNAL + isolates ch1",
    r_int["class"]=="INTERNAL" and r_int["faulty_channel"]==1,
    f"faulty_channel={r_int['faulty_channel']} incoherence={r_int['incoherence_max_resid']:.2f}")
r_one = sd.classify_shock(channels(base)[:1], prev_cons)
chk("single channel -> UNDETERMINED (no redundancy, honest)", r_one["class"]=="UNDETERMINED", r_one.get("reason",""))

print(f"\n== VERDICT: {'PASS' if PASS else 'FAIL'} ==")
sys.exit(0 if PASS else 1)
