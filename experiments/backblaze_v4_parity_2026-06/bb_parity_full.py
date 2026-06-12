"""Full-output parity: the 6 newly-ported v4 components vs the real oracle output
(bb_oracle_v3.json) on the identical Backblaze series."""
import csv, json, sys
from pathlib import Path
import numpy as np
HS = Path(__file__).resolve().parents[2]; ENG = HS / "HCI-CNTT" / "engine"; sys.path.insert(0, str(ENG))
import geometry as geo, helmsman as hm, attractors as at, diagnostics as dg
O = json.load(open(Path(__file__).resolve().parent / "bb_oracle_v3.json"))
CSV = HS / "HCI-CNT" / "experiments" / "codawork2026" / "backblaze_fleet" / "backblaze_fleet_input.csv"
with open(CSV) as f: r = list(csv.reader(f)); header = r[0]; rows = [x for x in r[1:] if x]
carriers = [c.strip() for c in header[1:]]
M = np.array([[float(x) for x in row[1:]] for row in rows], float)
comp = geo.closure(M); clr = geo.clr(comp); H = geo.helmert_basis(comp.shape[1]); ilr = clr @ H.T

def mx(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    return float(np.max(np.abs(a - b))) if a.size and a.shape == b.shape else (0.0 if a.size==0 else 9e9)

PASS = True
def line(name, ok, detail=""):
    global PASS; PASS = PASS and ok; print(f"  [{'OK ' if ok else 'DIFF'}] {name:<34} {detail}")
T1 = 1e-9
print("== full-output parity: ported v4 components vs real oracle (731x4 Backblaze) ==\n")

# 1 helmsman family
v = hm.compute_helmsman_family(M); o = O["helmsman_family"]
line("helmsman.flips.total", v["flips"]["total"]==o["flips"]["total"], f"v={v['flips']['total']} o={o['flips']['total']}")
line("helmsman.sigma", v["sigma"]==o["sigma"])
line("helmsman.sign", v["sign"]==o["sign"])
line("helmsman.stability.global", abs(v["stability_S_sigma"]["global"]-o["stability_S_sigma"]["global"])<T1)
line("helmsman.torque_proxy", mx(v["torque_proxy"],o["torque_proxy"])<T1, f"maxd={mx(v['torque_proxy'],o['torque_proxy']):.1e}")
line("helmsman.flips.rolling", v["flips"]["rolling"]==o["flips"]["rolling"])
line("helmsman.chaos_indicator", v["chaos_indicator"]==o["chaos_indicator"], f"v={v['chaos_indicator']} o={o['chaos_indicator']}")

# 2 attractor
v = at.fit_attractor(comp); o = O["attractor_fit"]
line("attractor.fitted/period", v["fitted"]==o["fitted"] and v["period"]==o["period"], f"fitted={v['fitted']} period={v['period']}")
line("attractor.period_stability", abs(v["period_stability"]-o["period_stability"])<T1)
line("attractor.dominant_pair", v["dominant_pair"]==o["dominant_pair"], f"{v['dominant_pair']}")
line("attractor.amplitude_A", abs(v["amplitude_A"]-o["amplitude_A"])<T1, f"maxd={abs(v['amplitude_A']-o['amplitude_A']):.1e}")
line("attractor.damping_zeta", abs(v["damping_zeta"]-o["damping_zeta"])<T1)
line("attractor.contraction_lambda", abs(v["contraction_lambda"]-o["contraction_lambda"])<T1)

# 3 depth tower
v = dg.compute_depth_tower(comp, clr); o = O["depth_tower"]
line("depth.energy_levels.norm_mean", mx([e["norm_mean"] for e in v["energy_levels"]],[e["norm_mean"] for e in o["energy_levels"]])<T1)
line("depth.curvature_levels.norm_mean", mx([e["norm_mean"] for e in v["curvature_levels"]],[e["norm_mean"] for e in o["curvature_levels"]])<T1)
line("depth.termination.kind", v["termination"]["kind"]==o["termination"]["kind"], v["termination"]["kind"])
line("depth.ir_class", v["ir_class"]==o["ir_class"], v["ir_class"])
line("depth.involution.max_residual", abs(v["involution_M_squared"]["max_residual_overall"]-o["involution_M_squared"]["max_residual_overall"])<T1)

# 4 stage1
v = dg.compute_stage1(clr, carriers); o = O["stages"]["stage1"]
d = max(max(abs(a[k]-b[k]) for k in ("i_min","i_max","j_min","j_max")) for a,b in zip(v["sections"],o["sections"]))
line("stage1.sections (clr ranges)", d<T1, f"maxd={d:.1e}")

# 5 stage2
v = dg.compute_stage2(comp, clr, carriers); o = O["stages"]["stage2"]
dt = mx(v["variation_matrix"]["tau"], o["variation_matrix"]["tau"])
dr = max(abs(a["pearson_r"]-b["pearson_r"]) for a,b in zip(v["carrier_pair_examination"],o["carrier_pair_examination"]))
line("stage2.variation_matrix tau", dt<T1, f"maxd={dt:.1e}")
line("stage2.pairwise pearson_r", dr<T1, f"maxd={dr:.1e}")

# 6 stage3
v = dg.compute_stage3(comp, clr, carriers); o = O["stages"]["stage3"]
da = mx([t["area"] for t in v["triadic_area"]["triads"]],[t["area"] for t in o["triadic_area"]["triads"]])
dl = mx([e["mean_correlation"] for e in v["subcomposition_ladder"]["entries"]],[e["mean_correlation"] for e in o["subcomposition_ladder"]["entries"]])
line("stage3.triadic_area", da<T1, f"maxd={da:.1e}")
line("stage3.subcomposition_ladder", dl<T1, f"maxd={dl:.1e}")
line("stage3.regime_boundaries", v["regime_detection"]["boundary_indices"]==o["regime_detection"]["boundary_indices"],
     f"n={v['regime_detection']['n_boundaries']}")

# 7 eitt
v = dg.eitt_bench_test(comp, clr); o = O["diagnostics"]["eitt"]
vr = [x.get("rel_variation_pct") for x in v["results"] if "rel_variation_pct" in x]
orr = [x.get("rel_variation_pct") for x in o["results"] if "rel_variation_pct" in x]
line("eitt.rel_variation_pct", mx(vr,orr)<T1, f"maxd={mx(vr,orr):.1e}")

# 8 nav-2d
v = dg.compute_navigation_2d(ilr); o = O["navigation_2d"]
dve = mx(v["variance_explained"], o["variance_explained"])
db = mx([p for row in v["bary_xy"] for p in row],[p for row in o["bary_xy"] for p in row])
line("nav2d.variance_explained", dve<T1, f"maxd={dve:.1e}")
line("nav2d.bary_xy", db<1e-5, f"maxd={db:.1e}")

print(f"\n== VERDICT: {'FULL-OUTPUT TIER-A PARITY' if PASS else 'DIVERGENCE (see above)'} ==")
