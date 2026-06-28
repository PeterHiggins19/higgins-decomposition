"""CMP figures from the saved result JSONs (Crohn + HIV + HIV fix). Deterministic, real data only."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
OUT = Path(__file__).resolve().parent
cr = json.load(open(OUT/"cmp_result.json")); hv = json.load(open(OUT/"cmp_result_hiv.json")); fx = json.load(open(OUT/"cmp_fix_hiv_law2.json"))

# ---- Figure 1: Law 1 — aggregates vs relational (both cohorts) ----
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
for ax, R, ttl in [(axes[0], cr, "Crohn (N=975, D=48)"), (axes[1], hv, "HIV (N=155, D=60)")]:
    agg = R["law1"]["aggregates"]
    labels = list(agg.keys()) + ["RELATIONAL\n(ILR log-ratios)"]
    vals = [agg[k]["separation_auc"] for k in agg] + [R["law1"]["relational_ilr"]["cv_auc"]]
    colors = ["#9aa0a6"]*len(agg) + ["#1a73e8"]
    ax.bar(range(len(vals)), vals, color=colors, edgecolor="black", linewidth=0.6)
    ax.axhline(0.5, color="black", lw=0.8, ls=":")
    p95 = R["law1"]["relational_perm_null"]["null_p95"]
    ax.axhline(p95, color="#d93025", lw=1.0, ls="--")
    ax.text(len(vals)-1, p95+0.006, "perm-null 95%", color="#d93025", fontsize=7, ha="right")
    ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=8)
    ax.set_ylim(0.45, 0.9); ax.set_ylabel("separation AUC"); ax.set_title(ttl, fontsize=10)
    pm = R["law1"]["permanova"]["p"]
    ax.text(0.02, 0.95, f"PERMANOVA p={pm}", transform=ax.transAxes, fontsize=8, va="top")
fig.suptitle("Law 1 — the message is in the ratios: scalar aggregates are blind, relational geometry sees it", fontsize=10.5)
fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(OUT/"fig1_law1_relational_vs_aggregate.png", dpi=150); plt.close(fig)

# ---- Figure 2: Law 2 — dimensional articulation + its finite-sample boundary ----
fig, ax = plt.subplots(figsize=(7.5, 4.6))
ab = cr["law2"]["ordering_abundance"]; cv = cr["law2"]["ordering_clr_variance"]
ax.plot([x["D_parts"] for x in ab], [x["cv_auc"] for x in ab], "-o", color="#1a73e8", label="Crohn N/D≈20 (abundance order) — RISES, saturates")
ax.plot([x["D_parts"] for x in cv], [x["cv_auc"] for x in cv], "--s", color="#669df6", ms=4, label="Crohn (CLR-variance order)")
ax.plot(fx["grid_parts"], fx["fixed_C1_auc"], "-o", color="#d93025", label="HIV N/D≈2.6 (C=1) — PEAKS mid-D, declines (overfit)")
ax.plot(fx["grid_parts"], fx["cv_tuned_auc"], "--^", color="#f29900", label="HIV (CV-tuned C) — partly rescued, still non-monotone")
nb = [x["null_p95"] for x in ab]
ax.plot([x["D_parts"] for x in ab], nb, ":", color="grey", label="permutation-null 95% (Crohn)")
ax.set_xlabel("number of parts D included (top-D taxa + amalgamated remainder)")
ax.set_ylabel("cross-validated AUC (recoverable signal)")
ax.set_title("Law 2 — more parts = more recoverable signal, up to the sample's capacity", fontsize=10.5)
ax.legend(fontsize=7.5, loc="lower right"); ax.grid(alpha=0.25)
fig.tight_layout(); fig.savefig(OUT/"fig2_law2_dimensional_articulation.png", dpi=150); plt.close(fig)
print("wrote fig1_law1_relational_vs_aggregate.png, fig2_law2_dimensional_articulation.png")
print("Crohn relational AUC", cr["law1"]["relational_ilr"]["cv_auc"], "| HIV relational AUC", hv["law1"]["relational_ilr"]["cv_auc"])
