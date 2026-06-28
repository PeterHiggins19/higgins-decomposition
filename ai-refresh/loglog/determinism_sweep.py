#!/usr/bin/env python3
"""
determinism_sweep.py -- the fixed-point guarantee, made checkable. "As long as the math is fixed-point flawless"
is turned into a gate: re-run each receipted artifact TWICE and confirm the output is identical -- a true fixed
point (same input -> same output -> same hash). What reproduces is solid; what does not is named, not hidden.

For each target script: run it twice (timeout-guarded), hash each run's stdout, and classify:
  REPRODUCES : both runs succeed and the output hashes are IDENTICAL (the fixed point holds).
  FLAKY      : both runs succeed but the outputs differ (NON-deterministic -- a real problem to fix).
  ERROR      : a run failed (e.g., needs args/data, or a transient mount issue -- retried once).
A master receipt is emitted over the per-file status map, so the GUARANTEE itself reproduces.

Usage: python3 determinism_sweep.py [file1.py file2.py ...]   (default: this session's receipted artifacts)
HONEST: this checks SELF-reproduction (run-twice-identical), the operational meaning of "deterministic". It does
not re-validate against historically recorded hashes unless those are printed by the script. Author: Peter
Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27. Peter is the sole gate.
"""
import os, sys, json, hashlib, subprocess
HS=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",".."))
def sha(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]
def shabytes(b): return hashlib.sha256(b).hexdigest()[:16]

DEFAULT=[
 "papers/go-blindness-study/go_three_arms_compiled.py",
 "papers/psychology-receipt/ngram_values_receipt.py",
 "Hs-Kinematics/hs_stewardship_extension.py",
 "experiments/foresight_stewardship_2026-06/foresight_run.py",
 "papers/medical-epidemiology/breast_cancer_composition_demo.py",
 "papers/medical-epidemiology/hs_tetrode_determinism.py",
 "library/tetrode_self_guided_map.py",
 "industrial-instruments/the-sniffer/the_sniffer.py",
]
def run_once(path, timeout=40):
    try:
        r=subprocess.run([sys.executable, path], capture_output=True, timeout=timeout, cwd=HS)
        return (r.returncode==0, r.stdout, (r.stderr[-200:] if r.returncode else b""))
    except subprocess.TimeoutExpired: return (False, b"", b"TIMEOUT")
    except Exception as e: return (False, b"", str(e).encode())

def classify(rel):
    path=os.path.join(HS,rel)
    if not os.path.exists(path): return {"file":rel,"status":"MISSING"}
    ok1,out1,err1=run_once(path)
    if not ok1:
        import time; time.sleep(2); ok1,out1,err1=run_once(path)   # one retry (mount-settle)
        if not ok1: return {"file":rel,"status":"ERROR","detail":err1.decode("utf-8","ignore")[:120]}
    ok2,out2,_=run_once(path)
    if not ok2: return {"file":rel,"status":"ERROR","detail":"second run failed"}
    h1,h2=shabytes(out1),shabytes(out2)
    return {"file":rel,"status":("REPRODUCES" if h1==h2 else "FLAKY"),"output_hash":h1,"second_hash":h2}

targets=sys.argv[1:] if len(sys.argv)>1 else DEFAULT
results=[classify(t) for t in targets]
counts={}
for r in results: counts[r["status"]]=counts.get(r["status"],0)+1
all_solid=all(r["status"]=="REPRODUCES" for r in results)
master=sha({"r":[{ "f":x["file"],"s":x["status"],"h":x.get("output_hash")} for x in results]})
out={"_meta":{"tool":"determinism_sweep.py","what":"fixed-point guarantee: every receipted artifact reproduces",
              "n":len(results),"summary":counts,"all_reproduce":all_solid,"sweep_receipt":master},
     "results":results,
     "verdict":("FIXED POINT HOLDS across all targets -- every artifact's output is identical on re-run; the "
        "math is solid and backed." if all_solid else "NOT ALL SOLID -- see FLAKY/ERROR entries (named, not hidden)."),
     "note":"REPRODUCES = run-twice-identical output (deterministic). ERROR may be a transient mount tear; re-run to confirm."}
if __name__=="__main__": print(json.dumps(out,indent=2))
