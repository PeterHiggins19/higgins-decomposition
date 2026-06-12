import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=json.load(open("cnq_tiling_poc_results.json"))
S=R["experiments"]["scaling"]
D=np.array([s["D"] for s in S]); charts=np.array([s["charts_sliding"] for s in S])
solve=np.array([s["solve_s"] for s in S]); dense=np.array([s["dense_global_ILR_GB"] for s in S])
err=np.array([s["recon_err"] for s in S])
bf=np.array([s["bruteforce_C_D_4"] if s["bruteforce_C_D_4"] else np.nan for s in S])

fig,ax=plt.subplots(1,3,figsize=(15,4.6))
# (a) chart count: tiling O(D) vs brute force C(D,4)
ax[0].loglog(D,charts,'o-',color="#1f77b4",label="CNQ-tiling charts  (≈ D, linear)")
Dx=np.array([4,16,64,256,1024,4096]); ax[0].loglog(Dx,[__import__("math").comb(int(d),4) for d in Dx],'s--',color="#d62728",label="brute-force C(D,4)")
ax[0].set_title("Charts needed vs dimension"); ax[0].set_xlabel("D (parts)"); ax[0].set_ylabel("count")
ax[0].grid(True,which="both",alpha=.3); ax[0].legend(fontsize=8)
# (b) wall time
ax[1].loglog(D,np.maximum(solve,1e-4),'o-',color="#2ca02c")
ax[1].loglog(D,np.maximum(solve,1e-4)[1]*(D/D[1]),':',color="gray",label="linear reference")
ax[1].set_title("Reconstruction wall-time (2-core CPU)"); ax[1].set_xlabel("D (parts)"); ax[1].set_ylabel("seconds")
ax[1].annotate(f"D=100k\n{solve[-1]:.2f}s",(D[-1],solve[-1]),fontsize=8,ha="right")
ax[1].grid(True,which="both",alpha=.3); ax[1].legend(fontsize=8)
# (c) memory: dense global ILR wall vs tiling footprint (edges*16 bytes)
edges=np.array([s["edges"] for s in S]); tiling_gb=edges*16/1e9
ax[2].loglog(D,np.maximum(dense,1e-4),'s--',color="#d62728",label="dense global ILR basis")
ax[2].loglog(D,np.maximum(tiling_gb,1e-6),'o-',color="#1f77b4",label="CNQ-tiling (sparse)")
ax[2].axhline(3.8,color="k",ls=":",lw=1); ax[2].annotate("this box (3.8 GB)",(6,4.3),fontsize=8)
ax[2].set_title("Memory footprint vs dimension"); ax[2].set_xlabel("D (parts)"); ax[2].set_ylabel("GB")
ax[2].grid(True,which="both",alpha=.3); ax[2].legend(fontsize=8)
fig.suptitle("CNQ-Tiling proof of concept — deterministic, near-linear scaling to D=100,000 (recon error ≤ 1.6e-9)",fontsize=11)
fig.tight_layout(rect=[0,0,1,0.95])
fig.savefig("cnq_tiling_scaling.png",dpi=140)
print("saved cnq_tiling_scaling.png")
print("err range:",err.min(),err.max())
