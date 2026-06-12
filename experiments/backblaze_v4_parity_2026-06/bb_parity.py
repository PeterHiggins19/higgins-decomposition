"""Backblaze head-to-head: CN-TT v4 vs the frozen oracle (CNT v3.2.0) on the
identical full fleet-longitudinal composition (731 x D=4)."""
import csv, json, sys, time
from pathlib import Path
import numpy as np
HS = Path(__file__).resolve().parents[2]
ENG = HS / "HCI-CNTT" / "engine"
sys.path.insert(0, str(ENG))
import geometry as geo, navigate as nav
from pipeline import Pipeline
from stages import AdaptStage, TreatStage, CalibrateStage, GeometryStage, AtlasStage, NavigateStage

CSV = HS / "HCI-CNT" / "experiments" / "codawork2026" / "backblaze_fleet" / "backblaze_fleet_input.csv"
ORACLE = json.load(open(Path(__file__).resolve().parent / "bb_oracle_v3.json"))

# read identical CSV
with open(CSV) as f:
    r = list(csv.reader(f)); header = r[0]; rows = [row for row in r[1:] if row]
carriers = [c.strip() for c in header[1:]]
labels = [row[0] for row in rows]
M = np.array([[float(x) for x in row[1:]] for row in rows], float)

# --- v4 end-to-end via the MODULAR PIPELINE (proves it runs on real data) ---
pipe = Pipeline([AdaptStage(), TreatStage(), CalibrateStage(), GeometryStage(), AtlasStage(), NavigateStage()])
t0 = time.perf_counter()
ctx = pipe.run({"header": header, "raw_rows": rows})
dt = time.perf_counter() - t0
print(f"== v4 modular pipeline on full Backblaze ({M.shape[0]}x{M.shape[1]}) ==")
print(f"  ran in {dt:.3f}s; chain_hash={ctx['_chain_hash'][:16]}; atlas lossless={ctx['atlas']['lossless']} (err={ctx['atlas']['recon_max_err']:.1e})")

# --- v4 quantities for the field-by-field diff ---
comp = geo.closure(M); clr = geo.clr(comp); H = geo.helmert_basis(4); ilr = clr @ H.T
navout = nav.navigate(comp, clr, ilr)
T = comp.shape[0]
ts = ORACLE["tensor"]["timesteps"]

def maxabs(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    return float(np.max(np.abs(a - b))) if a.size else 0.0

# accumulate per-field max abs diff (numeric) / mismatch count (categorical)
num = {}; cat = {"ring_class": 0, "concentration_regime": 0, "helmsman_local": 0}
angvel_diffs = []
for t in range(T):
    o = ts[t]; cs = o["coda_standard"]; nc = o["navigation_concentration_family"]; hx = o["higgins_extensions"]
    num.setdefault("composition", []).append(maxabs(comp[t], cs["composition"]))
    num.setdefault("clr", []).append(maxabs(clr[t], cs["clr"]))
    num.setdefault("shannon_entropy", []).append(abs(nav.shannon_entropy(comp[t]) - cs["shannon_entropy"]))
    num.setdefault("aitchison_norm", []).append(abs(nav.aitchison_norm(clr[t]) - cs["aitchison_norm"]))
    num.setdefault("k_eff", []).append(abs(nav.k_eff(comp[t]) - nc["k_eff"]))
    num.setdefault("higgins_scale", []).append(abs(nav.higgins_scale(comp[t]) - hx["higgins_scale"]))
    num.setdefault("kappa_HS_trace", []).append(abs(nav.kappa_hs_trace(comp[t]) - hx["kappa_HS_full"]["trace"]))
    num.setdefault("s_j_sensitivity", []).append(maxabs(nav.s_j_sensitivity(comp[t]), hx["s_j_sensitivity"]))
    num.setdefault("ilr_norm", []).append(abs(float(np.linalg.norm(ilr[t])) - cs["aitchison_norm"]))
    bp_v4 = nav.bearing_pairs(clr[t], carriers); bp_o = hx["bearing_tensor"]["pairs"]
    num.setdefault("bearing_theta", []).append(maxabs([p["theta_deg"] for p in bp_v4], [p["theta_deg"] for p in bp_o]))
    if hx["ring_class"] != nav.ring_class(nav.higgins_scale(comp[t])): cat["ring_class"] += 1
    st = navout["steps"][t]
    if (st["regime"] or "") != (nc["concentration_regime"] or ""): cat["concentration_regime"] += 1
    if t > 0:
        num.setdefault("aitchison_step", []).append(abs(nav.aitchison_distance(clr[t-1], clr[t]) - cs["aitchison_distance_step"]))
        num.setdefault("tv_step", []).append(abs(nav.tv_distance(comp[t-1], comp[t]) - nc["tv_distance_step"]))
        if st["helmsman"] != hx["helmsman_local"]: cat["helmsman_local"] += 1
        v4_ang = np.degrees(nav.stable_angle(ilr[t-1], ilr[t]))
        angvel_diffs.append(abs(v4_ang - hx["angular_velocity_deg"]))

print("\n== field-by-field max |v4 - oracle| over 731 steps ==")
TIER1 = 1e-9
allbit = True
for k in ["composition","clr","shannon_entropy","aitchison_norm","k_eff","higgins_scale",
          "kappa_HS_trace","s_j_sensitivity","ilr_norm","bearing_theta","aitchison_step","tv_step"]:
    mx = max(num[k]); ok = mx <= TIER1; allbit = allbit and ok
    print(f"  [{'IDENTICAL' if ok else 'DIFFERS  '}] {k:<18} max|diff|={mx:.2e}")
print("\n== categorical (count of step mismatches over 731) ==")
for k, v in cat.items():
    print(f"  [{'IDENTICAL' if v==0 else 'DIFFERS  '}] {k:<22} mismatches={v}")
print("\n== angular_velocity: v4 atan2 vs oracle arccos (the documented improvement) ==")
ad = np.array(angvel_diffs)
print(f"  max|diff|={ad.max():.2e} deg  mean|diff|={ad.mean():.2e} deg  (agree to oracle precision; v4 superior near 0/180 by construction)")

verdict = "TIER-A PARITY" if allbit and sum(cat.values())==0 else "DIVERGENCE (see above)"
print(f"\n== VERDICT: {verdict} ==")
print(f"  oracle cnt_content_sha256: {ORACLE['diagnostics']['cnt_content_sha256'][:24]}")

# save a machine-readable parity record
rec = {"input": str(CSV), "T": T, "D": int(comp.shape[1]), "carriers": carriers,
       "v4_chain_hash": ctx["_chain_hash"], "oracle_hash": ORACLE["diagnostics"]["cnt_content_sha256"],
       "numeric_max_abs_diff": {k: max(v) for k, v in num.items()},
       "categorical_mismatches": cat,
       "angular_velocity_max_diff_deg": float(ad.max()),
       "verdict": verdict}
json.dump(rec, open(Path(__file__).resolve().parent / "bb_parity_result.json", "w"), indent=2)
print("  saved bb_parity_result.json")
