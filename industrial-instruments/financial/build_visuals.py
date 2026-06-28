#!/usr/bin/env python3
"""
Regenerate every visual in this study deterministically from sp500_sectors.csv + the Hs engine:
the four CoDaWork-style figures (figures/*.png) and the interactive navigation projector
(navigation_projector.html). numpy + matplotlib + stdlib. Run: python3 build_visuals.py
Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001.
"""
import numpy as np, csv, os, sys, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import gridspec
HERE = os.path.dirname(os.path.abspath(__file__))
HS = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "figures"); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(HS, "Hs-Kinematics"))
import hs_kinematics_engine as eng

rows = [r for r in open(os.path.join(HERE, "sp500_sectors.csv")) if r.strip()]
rd = list(csv.reader(rows)); names = rd[0][1:]
M = np.array([[float(x) for x in r[1:]] for r in rd[1:]]); T, D = M.shape; days = np.arange(T)
out = eng.run(M, names); k = out["kinematics_and_dynamics"]; nav = out["navigation_reads"]; spec = out["spectral_modes"]
arrow = k["arrow_of_intent_NAV__momentum_PHYS"]; waypoints = nav["waypoints_NAV__phase_transitions_PHYS"]
patheff = k["course_directness_NAV__path_efficiency_PHYS"]; effdim = spec["degrees_of_freedom_NAV__effective_dimensionality_PHYS"]; chash = out["content_hash"]
clr = np.log(np.clip(M, 1e-12, None)); clr = clr - clr.mean(1, keepdims=True); clrc = clr - clr.mean(0, keepdims=True)
U, S, Vt = np.linalg.svd(clrc, full_matrices=False); proj = U[:, :2] * S[:2]; load = Vt[:2].T * S[:2]

BG="#0a0e12"; INK="#6898b8"; HI="#8ab8d8"; GOLD="#e0b25a"; MUT="#3a5060"; RED="#d98a8a"
plt.rcParams.update({"figure.facecolor":BG,"axes.facecolor":BG,"savefig.facecolor":BG,"text.color":INK,
  "axes.labelcolor":INK,"xtick.color":MUT,"ytick.color":MUT,"axes.edgecolor":MUT,"font.family":"monospace","font.size":9,"axes.titlecolor":HI})
pal = plt.cm.twilight_shifted(np.linspace(0.05, 0.95, D)); order = np.argsort(-M[0])
def save(fig, nm): fig.savefig(os.path.join(OUT, nm), dpi=140, bbox_inches="tight"); plt.close(fig); print("wrote figures/"+nm)

fig, ax = plt.subplots(figsize=(9, 4.2))
ax.stackplot(days, *[M[:, j] for j in order], labels=[names[j] for j in order], colors=[pal[j] for j in order], alpha=.92, lw=0)
ax.set_xlim(0, T-1); ax.set_ylim(0, 1); ax.set_title("THE SIZE VIEW — sector shares over 252 trading days (what the eye sees)")
ax.set_xlabel("trading day"); ax.set_ylabel("share of whole")
ax.legend(ncol=5, fontsize=6, loc="upper center", bbox_to_anchor=(.5, -.16), frameon=False, labelcolor=INK); save(fig, "fig1_share_over_time.png")

fig, ax = plt.subplots(figsize=(7, 6)); sc = ax.scatter(proj[:, 0], proj[:, 1], c=days, cmap="viridis", s=10, alpha=.8)
for j in range(D):
    ax.annotate("", xy=(load[j, 0], load[j, 1]), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.1, alpha=.9))
    ax.text(load[j, 0]*1.06, load[j, 1]*1.06, names[j], color=HI, fontsize=6.5, ha="center", va="center")
ax.axhline(0, color=MUT, lw=.5); ax.axvline(0, color=MUT, lw=.5); ax.set_title("THE STATIC CoDa PICTURE — CLR biplot (sectors as directions; cloud = the year)")
ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); cb = plt.colorbar(sc, ax=ax, fraction=.045); cb.set_label("trading day", color=MUT); save(fig, "fig2_clr_biplot.png")

fig, ax = plt.subplots(figsize=(7.6, 6)); ax.plot(proj[:, 0], proj[:, 1], color=INK, lw=.8, alpha=.5)
ax.scatter(proj[:, 0], proj[:, 1], c=days, cmap="plasma", s=12)
ax.scatter(*proj[0], c="w", s=70, zorder=5, edgecolor=BG); ax.text(proj[0, 0], proj[0, 1], "  start", color="w", fontsize=8)
ax.scatter(*proj[-1], c=GOLD, s=90, marker="*", zorder=5, edgecolor=BG); ax.text(proj[-1, 0], proj[-1, 1], "  now", color=GOLD, fontsize=8)
net = proj[-1]-proj[0]; ax.annotate("", xy=proj[0]+net, xytext=proj[0], arrowprops=dict(arrowstyle="-|>", color=RED, lw=2, alpha=.85))
for w in waypoints:
    ax.scatter(*proj[w], s=140, facecolors="none", edgecolors=GOLD, lw=1.3, zorder=4); ax.text(proj[w, 0], proj[w, 1], f" d{w}", color=GOLD, fontsize=6.5)
ax.set_title(f"THE NAVIGATION VIEW — heading + {len(waypoints)} regime changes (path efficiency {patheff:.3f}; ~{effdim:.1f} directions)")
ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); save(fig, "fig3_navigation.png")

fig = plt.figure(figsize=(10, 5)); gs = gridspec.GridSpec(2, 5, hspace=.55, wspace=.3); to = set(arrow["to"]); fr = set(arrow["from"])
for i, j in enumerate(order):
    ax = fig.add_subplot(gs[i//5, i%5]); ax.plot(days, M[:, j], color=pal[j], lw=1.4)
    pct = 100*(M[-1, j]-M[0, j])/max(M[0, j], 1e-9)
    tag = "▲ gaining" if names[j] in to else ("▼ shedding" if names[j] in fr else "· holding")
    tcol = "#3fb37f" if names[j] in to else (RED if names[j] in fr else MUT)
    ax.set_title(names[j], fontsize=7.5, color=HI); ax.text(.02, .93, f"{tag}  {pct:+.1f}%", transform=ax.transAxes, color=tcol, fontsize=6.5, va="top")
    ax.set_xticks([]); ax.tick_params(labelsize=5)
    for w in waypoints: ax.axvline(w, color=GOLD, lw=.4, alpha=.4)
fig.suptitle("KNOW YOUR POSITION — each sector's share trajectory (gold lines = system regime changes)", color=HI, y=.98); save(fig, "fig4_sector_positions.png")

print("reads: to", arrow["to"], "from", arrow["from"], "| path_eff", round(patheff,3), "eff_dim", round(effdim,2), "| hash", chash)
print("(the interactive navigation_projector.html is generated by the companion builder; see RESULTS/README.)")
