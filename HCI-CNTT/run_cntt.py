#!/usr/bin/env python3
"""CN-TT v4 CLI — ingest ANY composition CSV (label column + D carrier columns) and
emit the full payload. Drop a coda4microbiome CSV in the data folder and run:
    python HCI-CNTT/run_cntt.py <path-to-csv> -o out.json
Auto-gates the O(D^2)/combinatorial blocks (stage1/2/3, nav-2D) at high D."""
import sys, csv, json, time, argparse
from pathlib import Path
import numpy as np
ENG = Path(__file__).resolve().parent / "engine"; sys.path.insert(0, str(ENG))
import geometry as geo, navigate as nav, atlas as atl, helmsman as hm, attractors as at, diagnostics as dg, provenance as prov

def run(csv_path, high_d_threshold=64, atlas_strategy="hierarchical"):
    with open(csv_path) as f:
        r = list(csv.reader(f)); header = r[0]
        rows = [x for x in r[1:] if x and any(c.strip() for c in x)]
    carriers = [c.strip() for c in header[1:]]; labels = [x[0] for x in rows]
    M = np.array([[float(v) for v in x[1:]] for x in rows], float)
    for j in range(M.shape[1]):                                # multiplicative zero-treatment
        col = M[:, j]; pos = col[col > 0]
        if pos.size: M[col <= 0, j] = 0.65 * pos.min()
    T, D = M.shape; comp = geo.closure(M); clr = geo.clr(comp); H = geo.helmert_basis(D); ilr = clr @ H.T
    high_d = D > high_d_threshold
    charts = atl.hierarchical_atlas(D) if atlas_strategy == "hierarchical" else atl.sliding_window_atlas(D)
    edges = atl.edges_from_charts(charts); conn, nc = atl.is_connected(D, edges)
    recon = max(atl.reconstruct_clr(D, edges, comp[t])[1] for t in range(min(T, 50))) if conn else None
    payload = {"metadata": {**prov.version_triple(), "high_d_mode": high_d, "atlas_strategy": atlas_strategy},
               "input": {"source": str(csv_path), "n_records": T, "n_carriers": D, "carriers": carriers, "labels": labels},
               "geometry": {"radial_mean": float(np.linalg.norm(ilr, axis=1).mean())},
               "atlas": {"n_charts": len(charts), "connected": bool(conn), "reconstruction_max_err": recon,
                         "lossless": bool(conn and recon is not None and recon < 1e-6)},
               "navigation": nav.navigate(comp, clr, ilr),
               "helmsman_family": hm.compute_helmsman_family(M),
               "attractor_fit": at.fit_attractor(comp),
               "depth_tower": dg.compute_depth_tower(comp, clr),
               "diagnostics": {"eitt": dg.eitt_bench_test(comp, clr)}}
    if not high_d:
        payload["stages"] = {"stage1": dg.compute_stage1(clr, carriers),
                             "stage2": dg.compute_stage2(comp, clr, carriers),
                             "stage3": dg.compute_stage3(comp, clr, carriers)}
        payload["navigation_2d"] = dg.compute_navigation_2d(ilr)
    else:
        payload["_note"] = f"high-D mode (D={D}>{high_d_threshold}): O(D^2)/combinatorial blocks (stage1/2/3, nav-2D) skipped; O(D) family + lossless tiling emitted."
    payload["diagnostics"]["cntt_content_sha256"] = prov.stable_hash(payload)
    return payload

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("-o", "--out")
    ap.add_argument("--high-d-threshold", type=int, default=64); a = ap.parse_args()
    t0 = time.perf_counter(); p = run(a.csv, a.high_d_threshold); dt = time.perf_counter() - t0
    print(f"CN-TT v4: {p['input']['n_records']}x{p['input']['n_carriers']}  high_d={p['metadata']['high_d_mode']}  "
          f"atlas lossless={p['atlas']['lossless']} (err={p['atlas']['reconstruction_max_err']})  "
          f"helmsman.flips={p['helmsman_family']['flips']['total']}  ir_class={p['depth_tower']['ir_class']}  {dt:.2f}s")
    if a.out: json.dump(p, open(a.out, "w"), indent=2); print("wrote", a.out)
