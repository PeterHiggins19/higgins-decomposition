#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cnt_cnq_analysis.py  --  reproducible CNT/CNQ pass on Frielingen-9 mudstone.

WHAT THIS IS
  A faithful, self-contained implementation of the documented Hs / CNT method
  (closure -> CLR -> Helmert-orthonormal ILR -> per-step navigation), plus the
  native D=4 CNQ (radial magnitude + bearing rotation). It is the INSTRUMENT.
  It reports compositional structure; it assigns NO geological meaning. The
  geologist reads the outputs and the displays and determines the meaning.

DATA (cited)
  Input file:  frielingen9_xrf_4part.csv  (in this folder)
  Provenance:  Thoele, H. et al. (2019). Geochemistry/CaCO3/TOC of core
               Frielingen-9, Lower Cretaceous, eastern Lower Saxony Basin.
               PANGAEA, https://doi.org/10.1594/PANGAEA.897615  (CC-BY-4.0)
               Paper: https://doi.org/10.1002/dep2.83
  Composition used (D=4, CNQ-native): SiO2, Al2O3, Rb, Zr  (siliciclastic system).
  Independent calibration targets (NOT in the composition): CaCO3, TOC.

REQUIREMENTS
  python>=3.8, numpy, matplotlib      ->  pip install numpy matplotlib

RUN
  python cnt_cnq_analysis.py
  Outputs (this folder): mud_fig1_step_caco3.png, mud_fig2_helmsman.png,
  mud_fig3_cnq.png, frielingen9_cnt_cnq_series.csv, frielingen9_results.json,
  projector_data.json  (the last feeds build_dashboard.py).

METHOD = canonical Hs algorithm, reimplemented here for transparency. It is NOT
the hash-stamped engine binary; numbers are research-grade and reproducible from
the cited data with the code below.
"""
import os, json, csv
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
CSVIN = os.path.join(HERE, "frielingen9_xrf_4part.csv")
names = ["SiO2", "Al2O3", "Rb", "Zr"]
ROUND = 4

# ---- read cited input (skip comment lines) -------------------------------
rows = []
with open(CSVIN) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or line.lower().startswith("depth"):
            continue
        rows.append([float(x) for x in line.split(",")])
A = np.array(rows)
depth, SiO2, Al2O3 = A[:, 0], A[:, 1], A[:, 2]
Rb, Zr = A[:, 3] / 1e4, A[:, 4] / 1e4          # mg/kg -> same scale as wt% for closure
CaCO3, TOC = A[:, 5], A[:, 6]
order = np.argsort(depth)
depth, CaCO3, TOC = depth[order], CaCO3[order], TOC[order]
comp = np.vstack([SiO2, Al2O3, Rb, Zr]).T[order]
N, D = comp.shape

# ---- CNT core ------------------------------------------------------------
comp = comp / comp.sum(1, keepdims=True)                 # closure (subcomposition)
clr = np.log(comp); clr = clr - clr.mean(1, keepdims=True)   # centred log-ratio
H = np.zeros((D, D - 1))                                  # Helmert orthonormal ILR basis
for i in range(1, D):
    H[:i, i - 1] = 1.0 / i; H[i, i - 1] = -1.0; H[:, i - 1] *= np.sqrt(i / (i + 1.0))
ilr = clr @ H                                            # isometry: 3-vector / sample (D=4)
dclr = np.diff(clr, axis=0)
step = np.linalg.norm(dclr, axis=1)                      # Aitchison step (size of move)
helm = np.argmax(np.abs(dclr), axis=1)                   # helmsman (which part steers)
pw = dclr ** 2; pw = pw / pw.sum(1, keepdims=True)       # power share / step
rho = comp[:-1]                                          # starting share
alpha = np.where(rho > 0, pw / rho, 0.0)                 # activation = power-share / mass-share (all parts)
dd = (alpha >= 3.0) & (rho >= 1e-3)                      # deceptive-drift FLAG stays guarded (share >= 0.1%)
Keff = np.exp(-(comp * np.log(comp)).sum(1))            # effective # of active parts
flips = int((helm[1:] != helm[:-1]).sum())
directness = 1 - flips / max(1, len(helm) - 1)
thr = np.median(step) + 2 * 1.4826 * np.median(np.abs(step - np.median(step)))
regime = step > thr                                     # robust regime tripwire

# ---- CNQ (native, D=4) ---------------------------------------------------
radial = np.linalg.norm(ilr, axis=1)                    # |ilr| per sample
u = ilr / radial[:, None]
ang = np.degrees(np.arccos(np.clip((u[1:] * u[:-1]).sum(1), -1, 1)))  # bearing rotation/step

# ---- barycenter trajectory (ILR-PCA, 2D), deterministic sign convention --
Ic = ilr - ilr.mean(0)
U, S, Vt = np.linalg.svd(Ic, full_matrices=False)
scores = Ic @ Vt[:2].T                                   # first two PCs
for j in range(2):                                       # fix sign: sample 0 negative
    if scores[0, j] > 0: scores[:, j] = -scores[:, j]
bary = scores

# ---- independent calibration (CaCO3, TOC are NOT in the composition) ------
dCaCO3, dTOC = np.abs(np.diff(CaCO3)), np.abs(np.diff(TOC))
c1 = float(np.corrcoef(step, dCaCO3)[0, 1])
c2 = float(np.corrcoef(step, dTOC)[0, 1])
trace_dd = sorted([(round(float(depth[i + 1]), 2), names[j], round(float(alpha[i, j]), 1))
                   for i in range(N - 1) for j in (2, 3) if dd[i, j]], key=lambda t: -t[2])[:8]
siAl = np.log(comp[:, 0] / comp[:, 1]); zrRb = np.log(comp[:, 3] / comp[:, 2])

# ---- console report ------------------------------------------------------
print("=== CNT/CNQ on Frielingen-9 mudstone (PANGAEA 897615) ===")
print(f"N={N}, depth {depth.min():.1f}-{depth.max():.1f} m, D={D} [{','.join(names)}], CNQ native (D=4)")
print("helmsman: " + ", ".join(f"{names[k]}:{int((helm==k).sum())}" for k in range(D)))
print(f"flips={flips}, directness={directness:.2f}, regime steps={int(regime.sum())}/{N-1}")
print(f"corr(step,|dCaCO3|)={c1:.2f}   corr(step,|dTOC|)={c2:.2f}")
for i in np.argsort(step)[::-1][:6]:
    print(f"  big step @ {depth[i+1]:.2f} m  step={step[i]:.3f}  helm={names[helm[i]]}  CaCO3={CaCO3[i+1]:.1f}%")
print("deceptive-drift (trace>=3x share):", trace_dd or "none above guard")

# ---- figures -------------------------------------------------------------
plt.figure(figsize=(9, 4)); ax = plt.gca()
ax.plot(depth[1:], step, lw=1.1, color="#3a372f", label="CNT Aitchison step")
ax.scatter(depth[1:][regime], step[regime], s=22, color="#6b1f2a", zorder=3, label="regime shift")
ax.set_xlabel("depth (m)"); ax.set_ylabel("Aitchison step", color="#3a372f")
ax2 = ax.twinx(); ax2.plot(depth, CaCO3, lw=0.9, color="#2a6b9a", alpha=.7); ax2.set_ylabel("CaCO3 % (independent)", color="#2a6b9a")
ax.set_title("Frielingen-9: CNT compositional step vs CaCO3"); ax.legend(loc="upper right", fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(HERE, "mud_fig1_step_caco3.png"), dpi=110); plt.close()

plt.figure(figsize=(9, 3.2)); cols = ["#2a6b9a", "#3a8a3a", "#caa000", "#6b1f2a"]
for k in range(D):
    m = helm == k; plt.scatter(depth[1:][m], np.full(m.sum(), k), s=14, color=cols[k], label=names[k])
ddm = dd[:, 2] | dd[:, 3]
plt.scatter(depth[1:][ddm], np.full(ddm.sum(), 3.4), marker="v", s=26, color="black", label="deceptive drift")
plt.yticks(range(D), names); plt.xlabel("depth (m)")
plt.title("Helmsman (driver of each step) + deceptive-drift flags"); plt.legend(ncol=5, fontsize=7, loc="upper center")
plt.tight_layout(); plt.savefig(os.path.join(HERE, "mud_fig2_helmsman.png"), dpi=110); plt.close()

plt.figure(figsize=(9, 3.6)); ax = plt.gca()
ax.plot(depth, radial, lw=1.1, color="#3a372f", label="CNQ radial |ilr|"); ax.set_xlabel("depth (m)"); ax.set_ylabel("CNQ radial", color="#3a372f")
ax3 = ax.twinx(); ax3.plot(depth[1:], ang, lw=0.8, color="#6b1f2a", alpha=.6); ax3.set_ylabel("bearing rotation (deg)", color="#6b1f2a")
ax.set_title("CNQ (native D=4): radial magnitude + step bearing rotation")
plt.tight_layout(); plt.savefig(os.path.join(HERE, "mud_fig3_cnq.png"), dpi=110); plt.close()

# ---- per-sample series table (full transparency) -------------------------
with open(os.path.join(HERE, "frielingen9_cnt_cnq_series.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["depth_m"] + [f"x_{n}" for n in names] + [f"clr_{n}" for n in names] +
               ["aitchison_step", "helmsman", "regime", "Keff", "cnq_radial", "bary_x", "bary_y",
                "logSiAl", "logZrRb", "CaCO3_pct", "TOC_pct"] + [f"alpha_{n}" for n in names])
    for i in range(N):
        st = 0.0 if i == 0 else float(step[i - 1])
        hm = "" if i == 0 else names[int(helm[i - 1])]
        rg = 0 if i == 0 else int(regime[i - 1])
        al = ["", "", "", ""] if i == 0 else [round(float(alpha[i - 1, k]), 2) for k in range(D)]
        w.writerow([round(float(depth[i]), 2)] + [round(float(comp[i, k]), 6) for k in range(D)] +
                   [round(float(clr[i, k]), 4) for k in range(D)] +
                   [round(st, 4), hm, rg, round(float(Keff[i]), 4), round(float(radial[i]), 4),
                    round(float(bary[i, 0]), 4), round(float(bary[i, 1]), 4),
                    round(float(siAl[i]), 4), round(float(zrRb[i]), 4),
                    round(float(CaCO3[i]), 2), round(float(TOC[i]), 2)] + al)

# ---- summary json --------------------------------------------------------
json.dump({"data_source": "PANGAEA 897615 (Thoele et al. 2019), CC-BY-4.0",
           "N": N, "D": D, "composition": names, "calibration_targets": ["CaCO3", "TOC"],
           "depth_min": float(depth.min()), "depth_max": float(depth.max()),
           "helmsman_counts": {names[k]: int((helm == k).sum()) for k in range(D)},
           "flips": flips, "directness": round(directness, 3), "regime_steps": int(regime.sum()),
           "corr_step_dCaCO3": round(c1, 3), "corr_step_dTOC": round(c2, 3),
           "trace_deceptive_drift_top": trace_dd,
           "note": "Instrument outputs only; geological interpretation is the domain expert's."},
          open(os.path.join(HERE, "frielingen9_results.json"), "w"), indent=1)

# ---- projector data (feeds build_dashboard.py) ---------------------------
def r(a, n=ROUND): return [round(float(x), n) for x in a]
Araw = A[order]  # original-unit values, depth-sorted (oxides %, Rb/Zr mg/kg) for display
DATA = {"names": names, "units": ["%", "%", "mg/kg", "mg/kg"],
        "raw": [[round(float(Araw[i, 1]), 2), round(float(Araw[i, 2]), 2),
                 int(round(Araw[i, 3])), int(round(Araw[i, 4]))] for i in range(N)],
        "depth": r(depth, 2),
        "comp": [[round(float(comp[i, k]), 8) for k in range(D)] for i in range(N)],  # 8 dp: keep trace precision for CLR/alpha
        "caco3": r(CaCO3, 2), "toc": r(TOC, 2),
        "step": [0.0] + r(step), "helm": [-1] + [int(x) for x in helm],
        "regime": [0] + [int(x) for x in regime], "radial": r(radial),
        "bary": [[round(float(bary[i, 0]), ROUND), round(float(bary[i, 1]), ROUND)] for i in range(N)],
        "stepmax": float(step.max())}
json.dump(DATA, open(os.path.join(HERE, "projector_data.json"), "w"))
print("wrote: 3 figures, frielingen9_cnt_cnq_series.csv, frielingen9_results.json, projector_data.json")
