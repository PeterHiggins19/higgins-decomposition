"""CN-TT v4 modular BIST — proves the section architecture:
 (1) every section is a TEST POINT (test_all);
 (2) the chain is DETERMINISTIC (rerun -> identical chain hash);
 (3) identical work is CACHED (rerun -> all sections cached: 'history not repeated');
 (4) ADAPTABILITY+DELTA: changing ONE section's config recomputes only it + downstream."""
import sys
from pathlib import Path
import numpy as np
ENG = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENG))
import provenance as prov
from pipeline import Pipeline
from stages import AdaptStage, TreatStage, CalibrateStage, GeometryStage, AtlasStage, NavigateStage

PASS = True
def check(name, cond, detail=""):
    global PASS; ok = bool(cond); PASS = PASS and ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")

print("== CN-TT v4 modular self-test ==")
stages = [AdaptStage(), TreatStage(), CalibrateStage(), GeometryStage(), AtlasStage(), NavigateStage()]
pipe = Pipeline(stages)

# tiny dataset: 12 rows x 4 carriers (with a zero to exercise treat)
rng = np.random.default_rng(7)
raw = (np.abs(rng.normal(size=(12,4))) + 0.05)
raw[3,2] = 0.0
header = ["t","A","B","C","D"]
raw_rows = [[str(i)] + [f"{v}" for v in raw[i]] for i in range(12)]
ctx0 = {"header": header, "raw_rows": raw_rows}

# (1) every section is a test point
print("\n-- (1) per-section test points --")
all_ok = True
for nm, ok, detail in pipe.test_all():
    print(f"  [{'PASS' if ok else 'FAIL'}] section:{nm:<10} {detail}"); all_ok = all_ok and ok
check("all sections self-test green", all_ok)

# (2) determinism + (3) cache
print("\n-- (2)/(3) determinism + don't-repeat-history --")
r1 = pipe.run(ctx0)
r2 = pipe.run(ctx0)
check("deterministic: identical chain hash on rerun", r1["_chain_hash"] == r2["_chain_hash"],
      f"hash={r1['_chain_hash'][:16]}")
check("rerun reuses cache (no section recomputed)", all(c["cached"] for c in r2["_provenance"]),
      "all 6 sections cached")
print("  first-run cached flags: ", [c["cached"] for c in r1["_provenance"]])
print("  rerun     cached flags: ", [c["cached"] for c in r2["_provenance"]])

# (4) adaptability + delta isolation: change ONLY the atlas section's config
print("\n-- (4) adaptability + delta isolation (change atlas: hierarchical -> sliding) --")
r3 = pipe.run(ctx0, configs={"atlas": {"strategy": "sliding"}})
prov_by = {c["stage"]: c for c in r3["_provenance"]}
upstream = ["adapt","treat","calibrate","geometry"]
downstream_changed = ["atlas","navigate"]
check("upstream sections stayed cached (history not repeated)",
      all(prov_by[s]["cached"] for s in upstream),
      "cached: " + ",".join(s for s in upstream if prov_by[s]["cached"]))
check("only changed section + downstream recomputed",
      all(not prov_by[s]["cached"] for s in downstream_changed),
      "recomputed: " + ",".join(downstream_changed))
check("delta is real: chain hash changed", r3["_chain_hash"] != r1["_chain_hash"])
print("  r3 cached flags by section:", {c["stage"]: c["cached"] for c in r3["_provenance"]})

# show the navigation output is populated (P2 family running end-to-end)
navg = r1["navigation"]
check("navigation family produced end-to-end", navg["n_steps"] == 12 and "regime_counts" in navg,
      f"k_eff {navg['k_eff']['min']:.2f}..{navg['k_eff']['max']:.2f}; regimes {navg['regime_counts']}")
check("atlas lossless in-chain", r1["atlas"]["lossless"], f"err={r1['atlas']['recon_max_err']:.1e}")

print(f"\n== VERDICT: {'PASS' if PASS else 'FAIL'} ==")
sys.exit(0 if PASS else 1)
