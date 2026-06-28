"""
P1 Figure 1 — chart-graph atlas (path vs balanced tree) and diameter/residual vs D.
Data: Table 1 of the paper (real measured residuals). Vector PDF per LATEX_ARXIV_STANDARDS.
Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({
    "font.family": "serif", "mathtext.fontset": "cm",
    "font.size": 11, "axes.labelsize": 11, "axes.titlesize": 11,
    "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9,
    "axes.linewidth": 0.8, "lines.linewidth": 1.6,
})
fig = plt.figure(figsize=(6.6, 5.2))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.25], hspace=0.42, wspace=0.30,
                      left=0.10, right=0.97, top=0.93, bottom=0.10)

# ---------- (a) path atlas ----------
axa = fig.add_subplot(gs[0, 0]); axa.set_title(r"(a) path atlas: diameter $O(D)$", pad=6)
n = 8; xs = np.arange(n)
axa.plot(xs, np.zeros(n), "-", color="0.55", lw=1.2, zorder=1)
axa.scatter(xs, np.zeros(n), s=60, color="#2b6cb0", zorder=3, edgecolor="white", lw=0.7)
# overlapping 4-part charts as shaded windows
for s,(c) in zip(range(0, n-3), ["#cbe3f7","#d6eadb"]*3):
    axa.add_patch(FancyBboxPatch((s-0.32, -0.30), 3.64, 0.60, boxstyle="round,pad=0.02,rounding_size=0.12",
                  fc=c, ec="0.7", lw=0.6, alpha=0.55, zorder=0))
axa.add_patch(FancyArrowPatch((0,-0.62),(n-1,-0.62), arrowstyle="<->", mutation_scale=10, color="#b03030", lw=1.2))
axa.text((n-1)/2, -0.82, r"diameter $\sim D$", ha="center", va="top", color="#b03030", fontsize=9)
axa.text(1.6, 0.42, r"overlapping 4-part charts", ha="center", fontsize=8.5, color="0.35")
axa.set_xlim(-0.8, n-0.2); axa.set_ylim(-1.05, 0.62); axa.axis("off")

# ---------- (b) balanced tree atlas ----------
axb = fig.add_subplot(gs[0, 1]); axb.set_title(r"(b) balanced-tree atlas: diameter $O(\log D)$", pad=6)
# ternary tree, 2 levels
pos = {0:(0.0,2.0)}
lvl1 = [(-2,1.0),(0,1.0),(2,1.0)]
for i,p in enumerate(lvl1,1): pos[i]=p
leaves=[]; k=4
for j,(px,py) in enumerate(lvl1):
    for dx in (-0.8,0,0.8):
        pos[k]=(px+dx,0.0); leaves.append(k); k+=1
edges=[(0,1),(0,2),(0,3)]
ci=4
for parent in (1,2,3):
    for _ in range(3): edges.append((parent,ci)); ci+=1
for a,b in edges:
    axb.plot([pos[a][0],pos[b][0]],[pos[a][1],pos[b][1]], "-", color="0.6", lw=1.0, zorder=1)
P=np.array([pos[i] for i in pos])
axb.scatter(P[:,0],P[:,1], s=55, color="#2f855a", zorder=3, edgecolor="white", lw=0.7)
# diameter = leaf -> root -> leaf
path=[leaves[0],1,0,3,leaves[-1]]
axb.plot([pos[i][0] for i in path],[pos[i][1] for i in path], color="#b03030", lw=2.0, zorder=2, alpha=0.9)
axb.text(0,-0.55, r"diameter $\sim 2\log_3 D$", ha="center", va="top", color="#b03030", fontsize=9)
axb.set_xlim(-3.0,3.0); axb.set_ylim(-0.85,2.35); axb.axis("off")

# ---------- (c) diameter vs D ----------
axc = fig.add_subplot(gs[1, 0]); axc.set_title("(c) chart-graph diameter", pad=6)
D = np.logspace(1, 6, 200)
axc.loglog(D, D-3, color="#b03030", label=r"path $\sim D$")
axc.loglog(D, 2*np.log(D)/np.log(3), color="#2f855a", label=r"tree $\sim 2\log_3 D$")
axc.axvline(1e6, color="0.8", lw=0.8, ls=":")
axc.annotate(r"$D{=}10^6$: tree depth $\approx 13$", xy=(1e6, 2*np.log(1e6)/np.log(3)),
             xytext=(2.2e3, 60), fontsize=8.5, color="#2f855a",
             arrowprops=dict(arrowstyle="->", color="#2f855a", lw=0.8))
axc.set_xlabel(r"dimension $D$ (parts)"); axc.set_ylabel("graph diameter")
axc.legend(frameon=False, loc="upper left"); axc.grid(True, which="both", ls=":", lw=0.4, color="0.85")

# ---------- (d) measured residual vs D (Table 1) ----------
axd = fig.add_subplot(gs[1, 1]); axd.set_title("(d) reconstruction residual (measured)", pad=6)
Dp = np.array([16,64,256,1024]); rp = np.array([1.3e-15,6.7e-14,3.0e-13,5.9e-12])
Dt = np.array([1e6]);            rt = np.array([4.1e-12])
axd.loglog(Dp, rp, "o-", color="#2b6cb0", ms=6, label="path atlas")
axd.loglog(Dt, rt, "*", color="#b03030", ms=15, label="balanced tree", zorder=4)
axd.axhline(4.1e-12, color="0.8", lw=0.8, ls=":")
axd.annotate(r"tree holds $\approx 4.1\times10^{-12}$ at $D{=}10^6$",
             xy=(1e6,4.1e-12), xytext=(1.5e1, 6e-13), fontsize=8.5, color="#b03030",
             arrowprops=dict(arrowstyle="->", color="#b03030", lw=0.8))
axd.set_xlabel(r"dimension $D$ (parts)"); axd.set_ylabel("max reconstruction residual")
axd.legend(frameon=False, loc="lower right"); axd.grid(True, which="both", ls=":", lw=0.4, color="0.85")

fig.savefig("fig1.pdf", bbox_inches="tight")
fig.savefig("fig1.png", dpi=200, bbox_inches="tight")
print("wrote fig1.pdf + fig1.png")
