#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cnq_multimap.py  --  CONCEPT TEST: tiling a higher-dimensional composition with
overlapping, CNQ-exact D=4 charts, and reconstructing the full-D navigation from
their shared ("duplicate boundary") data.

IDEA (Higgins): CNQ is exact only at D=4 (3 ILR balances -> quaternion). For a
composition with more than 4 parts, instead of one lossy high-D projection, take
an ATLAS of exact D=4 sub-charts that SHARE parts. The shared parts are the
duplicate boundary data; subcompositional coherence forces the charts to agree on
them, and that agreement is what lets the charts be glued back into the full-D move.

TEST DATA: the working Frielingen-9 example, extended to a D=6 bulk subcomposition
  [SiO2, Al2O3, Rb, Zr, CaCO3, TOC]   (Rb,Zr mg/kg -> /1e4; all on a wt%-like scale)
NB: for this concept test CaCO3 + TOC are folded INTO the composition (so there is
no held-out calibration target here); the proper test uses the high-resolution
multi-element core-scan (Ca,Ti,K,Mn,Fe,Sr...). Honest scope: this validates the
GLUING MATHS on real data; the scientific value of the per-chart CNQ ensemble on
genuinely high-D data still needs testing.

ATLAS: anchor = {SiO2, Al2O3} shared by every chart (the alignment "duplicates");
each chart adds one pair from {Rb, Zr, CaCO3, TOC} -> 6 overlapping D=4 charts.

OUTPUTS (this folder): cnq_multimap_data.json, cnq_multimap.png
REQUIRES: numpy, matplotlib
"""
import os, json, itertools
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
CSVIN = os.path.join(HERE, "frielingen9_xrf_4part.csv")
PARTS = ["SiO2", "Al2O3", "Rb", "Zr", "CaCO3", "TOC"]
COL = {"SiO2": 1, "Al2O3": 2, "Rb": 3, "Zr": 4, "CaCO3": 5, "TOC": 6}
SCALE = {"Rb": 1e-4, "Zr": 1e-4}  # mg/kg -> wt%-like

# ---- read + build D=6 composition ---------------------------------------
rows = []
for line in open(CSVIN):
    line = line.strip()
    if not line or line.startswith("#") or line.lower().startswith("depth"):
        continue
    rows.append([float(x) for x in line.split(",")])
A = np.array(rows); A = A[np.argsort(A[:, 0])]
depth = A[:, 0]
V = np.column_stack([A[:, COL[p]] * SCALE.get(p, 1.0) for p in PARTS])
V = np.clip(V, 1e-6, None)               # guard zeros for log-ratio
X = V / V.sum(1, keepdims=True)          # closure (D=6 subcomposition)
N, D = X.shape

def clr(M):
    L = np.log(M); return L - L.mean(1, keepdims=True)

def helmert(d):
    H = np.zeros((d, d - 1))
    for i in range(1, d):
        H[:i, i - 1] = 1.0 / i; H[i, i - 1] = -1.0; H[:, i - 1] *= np.sqrt(i / (i + 1.0))
    return H

# ---- full D=6 reference navigation --------------------------------------
clr6 = clr(X)
radial6 = np.linalg.norm(clr6, axis=1)              # |ilr| == |clr|
dclr6 = np.diff(clr6, axis=0)
step6 = np.linalg.norm(dclr6, axis=1)
helm6 = np.argmax(np.abs(dclr6), axis=1)

# ---- the atlas: anchor {SiO2,Al2O3} + each pair of the other four --------
anchor = ["SiO2", "Al2O3"]
extras = ["Rb", "Zr", "CaCO3", "TOC"]
charts = [anchor + list(p) for p in itertools.combinations(extras, 2)]   # 6 charts, D=4 each
idx = {p: i for i, p in enumerate(PARTS)}

chart_out = []
for parts in charts:
    cols = [idx[p] for p in parts]
    sub = X[:, cols]; sub = sub / sub.sum(1, keepdims=True)   # re-closure (subcomposition)
    cl = clr(sub)
    H = helmert(4); il = cl @ H                                # 3-vector per sample (CNQ-native)
    rad = np.linalg.norm(il, axis=1)
    dcl = np.diff(cl, axis=0)
    st = np.linalg.norm(dcl, axis=1)
    hm = np.argmax(np.abs(dcl), axis=1)
    u = il / rad[:, None]
    bearing = np.degrees(np.arccos(np.clip((u[1:] * u[:-1]).sum(1), -1, 1)))
    chart_out.append({"parts": parts, "cols": cols,
                      "radial": rad, "step": st, "helm": [parts[k] for k in hm], "bearing": bearing})

# ---- ALIGNMENT: shared-anchor balance must be identical across charts -----
# ln(SiO2/Al2O3) computed inside each chart; subcompositional coherence => identical.
anchor_bal = []
for c in chart_out:
    sub_cols = c["cols"]; ci = sub_cols.index(idx["SiO2"]); cj = sub_cols.index(idx["Al2O3"])
    sub = X[:, sub_cols]; sub = sub / sub.sum(1, keepdims=True); cl = clr(sub)
    anchor_bal.append(cl[:, ci] - cl[:, cj])
anchor_bal = np.array(anchor_bal)                  # (charts, N)
align_max_dev = float(np.max(np.abs(anchor_bal - anchor_bal[0])))
true_anchor = clr6[:, idx["SiO2"]] - clr6[:, idx["Al2O3"]]
align_vs_full = float(np.max(np.abs(anchor_bal[0] - true_anchor)))

# ---- RECONSTRUCTION: glue charts -> full clr6 ----------------------------
# model per sample: clrS_k(measured) = clr6_k + offset_S   (k in chart S)
# unknowns: clr6 (D) with sum=0, plus one offset per chart. Solve per sample.
def reconstruct(atlas_cols):
    M = len(atlas_cols)
    rec = np.zeros((N, D)); errs = []
    # build design once (structure is sample-independent)
    rowsM = []; rhs_template = []
    for s, cols in enumerate(atlas_cols):
        for k in cols:
            r = np.zeros(D + M); r[k] = 1.0; r[D + s] = 1.0; rowsM.append(r)
    cons = np.zeros(D + M); cons[:D] = 1.0          # sum(clr6)=0
    G = np.vstack(rowsM + [cons * 100.0])           # weight the constraint
    rank = np.linalg.matrix_rank(G[:, :D + M])
    for n in range(N):
        b = []
        for cols in atlas_cols:
            sub = X[n, cols]; sub = sub / sub.sum(); cl = np.log(sub) - np.log(sub).mean()
            b.extend(cl.tolist())
        b.append(0.0)
        sol, *_ = np.linalg.lstsq(G, np.array(b), rcond=None)
        rec[n] = sol[:D]
        errs.append(np.max(np.abs(rec[n] - clr6[n])))
    return rec, max(errs), rank

atlas_cols = [c["cols"] for c in chart_out]
rec6, recon_err, rank_full = reconstruct(atlas_cols)
ncols_full = D + len(atlas_cols)
rad6_rec = np.linalg.norm(rec6, axis=1)
recon_corr = float(np.corrcoef(rad6_rec, radial6)[0, 1])

# ---- OVERLAP NECESSITY: two charts that share NO parts cannot be aligned --
# {SiO2,Al2O3,Rb,Zr} and {CaCO3,TOC} -> disjoint -> system rank-deficient.
disjoint = [[idx[p] for p in ["SiO2", "Al2O3", "Rb", "Zr"]], [idx[p] for p in ["CaCO3", "TOC"]]]
_, disj_err, disj_rank = reconstruct(disjoint)
disj_ncols = D + len(disjoint)

print("=== CNQ multi-map concept test (Frielingen-9, D=6 -> overlapping D=4 charts) ===")
print(f"parts D={D}: {PARTS}")
print(f"atlas: {len(charts)} charts, anchor={anchor}, each D=4:")
for c in chart_out: print("   ", c["parts"])
print(f"ALIGNMENT  anchor balance max deviation across charts = {align_max_dev:.2e}  (vs full = {align_vs_full:.2e})")
print(f"RECONSTRUCT full D=6 clr from the 6 overlapping charts: max error = {recon_err:.2e}")
print(f"           design rank = {rank_full}/{ncols_full} (full column rank => unique)  radial corr = {recon_corr:.6f}")
print(f"OVERLAP NEEDED  disjoint atlas (no shared parts): rank = {disj_rank}/{disj_ncols} (deficient), recon error = {disj_err:.2e}")

# ---- multi-map figure ----------------------------------------------------
cmap = {"SiO2": "#2a6b9a", "Al2O3": "#3a8a3a", "Rb": "#caa000", "Zr": "#6b1f2a", "CaCO3": "#111", "TOC": "#2a6b9a"}
fig, ax = plt.subplots(2, 4, figsize=(15, 8)); ax = ax.ravel()
for i, c in enumerate(chart_out):
    a = ax[i]
    a.plot(c["radial"], depth, color="#6b1f2a", lw=1.2)
    a.invert_yaxis(); a.set_title("chart %d: [%s]" % (i + 1, ", ".join(c["parts"])), fontsize=9)
    a.set_xlabel("CNQ radial |ilr|", fontsize=8); a.tick_params(labelsize=7)
    a.text(0.04, 0.02, "anchor: SiO2,Al2O3", transform=a.transAxes, fontsize=7, color="#888")
# panel 7: alignment (all anchor balances overlaid -> one line)
a = ax[6]
for r in anchor_bal: a.plot(r, depth, color="#3a8a3a", lw=0.8, alpha=0.7)
a.invert_yaxis(); a.set_title("ALIGNMENT: shared anchor ln(Si/Al)\nidentical on all 6 charts (dev %.0e)" % align_max_dev, fontsize=9)
a.set_xlabel("ln(SiO2/Al2O3)", fontsize=8); a.tick_params(labelsize=7)
# panel 8: reconstruction (glued full vs true full)
a = ax[7]
a.plot(radial6, depth, color="#111", lw=2.4, label="true D=6")
a.plot(rad6_rec, depth, color="#caa000", lw=1.0, label="glued from 6 charts")
a.invert_yaxis(); a.set_title("RECONSTRUCTION: full D=6 radial\nglued from overlapping D=4 (err %.0e)" % recon_err, fontsize=9)
a.set_xlabel("CNQ radial |ilr|", fontsize=8); a.tick_params(labelsize=7); a.legend(fontsize=7)
fig.suptitle("CNQ multi-map  ·  Frielingen-9  ·  6 overlapping D=4 charts tile a D=6 composition (concept test)", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.97]); fig.savefig(os.path.join(HERE, "cnq_multimap.png"), dpi=120); plt.close()

# ---- data json -----------------------------------------------------------
json.dump({
    "concept": "overlapping CNQ-exact D=4 charts tile a higher-D composition; shared parts align them; glue reconstructs full-D navigation",
    "data": "Frielingen-9 (PANGAEA 897615); D=6 subcomposition " + ",".join(PARTS),
    "depth": [round(float(x), 2) for x in depth],
    "anchor": anchor,
    "charts": [{"parts": c["parts"]} for c in chart_out],
    "alignment_anchor_max_dev": align_max_dev,
    "alignment_vs_full": align_vs_full,
    "reconstruction_max_error": recon_err,
    "reconstruction_radial_corr": recon_corr,
    "design_rank": [int(rank_full), int(ncols_full)],
    "overlap_necessity": {"disjoint_rank": [int(disj_rank), int(disj_ncols)], "disjoint_recon_error": float(disj_err)},
    "radial_full_true": [round(float(x), 4) for x in radial6],
    "radial_full_reconstructed": [round(float(x), 4) for x in rad6_rec],
    "note": "Gluing maths validated lossless on real data (confirmed). Scientific value of the per-chart CNQ ensemble on genuine multi-element core-scan data still to be tested."
}, open(os.path.join(HERE, "cnq_multimap_data.json"), "w"), indent=1)
print("wrote cnq_multimap.png, cnq_multimap_data.json")
