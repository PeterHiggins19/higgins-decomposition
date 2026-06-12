"""CN-TT v4 diagnostic codes — demo. Operational codes on real Backblaze; the AUTOMATED
NULL flag on the real Crohn null; a separated case; an internal-fault case."""
import sys
from pathlib import Path
import numpy as np
HS = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(HS/"HCI-CNTT")); sys.path.insert(0, str(HS/"HCI-CNTT"/"engine"))
import codes, geometry as geo, shock_diagnostics as sd
import run_cntt

def show(title, res):
    print(f"\n== {title} ==  levels={res['level_counts']}")
    for c in res["codes"]: print(f"  {c['code']:<12} [{c['level']}] {c['msg']}")
    for m in res["structural_modes"]: print(f"  >> {m['mode']:<12} {m['msg']}")

# (1) operational codes on real Backblaze
csv = HS/"HCI-CNT"/"experiments"/"codawork2026"/"backblaze_fleet"/"backblaze_fleet_input.csv"
payload = run_cntt.run(str(csv))
show("(1) Backblaze operational codes", codes.generate_codes(payload))

# (2) the AUTOMATED NULL flag on the real Crohn null
import pyreadr
DAT = Path("/sessions/stoic-nifty-davinci/mnt/Claude CoWorker/DATA/MicroBiome/coda4microbiome/data")
r = pyreadr.read_r(str(DAT/"Crohn.rda")); X = r['x_Crohn'].values.astype(float); y = r['y_Crohn'].iloc[:,0].values
def treat(M):
    M = M.copy()
    for j in range(M.shape[1]):
        col = M[:,j]; pos = col[col>0]
        if pos.size: M[col<=0,j] = 0.65*pos.min()
    return M
comp = geo.closure(treat(X))
cmp = codes.group_separation(comp, y, metric="k_eff")
print(f"\n[Crohn CD vs control K_eff]: separated={cmp['separated']} p={cmp['p']:.2g} means={cmp['groups']}")
show("(2) Crohn comparison -> AUTOMATED NULL flag", codes.generate_codes(payload, comparison=cmp))

# (3) a clearly-separated synthetic case
rng = np.random.default_rng(0); D = 12
gA = rng.dirichlet(np.ones(D)*0.15, size=40)   # concentrated (low diversity)
gB = rng.dirichlet(np.ones(D)*5.0,  size=40)   # even (high diversity)
comp2 = geo.closure(np.vstack([gA, gB])); lab = np.array(["A"]*40 + ["B"]*40)
cmp2 = codes.group_separation(comp2, lab, metric="k_eff")
print(f"\n[synthetic A vs B K_eff]: separated={cmp2['separated']} p={cmp2['p']:.2g}")
show("(3) separated case -> DX-SEP-DIS", codes.generate_codes(payload, comparison=cmp2))

# (4) internal fault -> SK-INT-ERR + SM-IFT-ERR
rng = np.random.default_rng(3); base = rng.normal(0,1,8); base -= base.mean()
C = np.array([base+rng.normal(0,0.02,8) for _ in range(3)]); C = C - C.mean(1,keepdims=True)
C[2] += 2.0*rng.normal(0,1,8); C[2] -= C[2].mean()
sk = sd.classify_shock(C, np.median(C,axis=0))
show("(4) internal fault -> SK + structural mode", codes.generate_codes(payload, shock=sk))
print("\ndone.")
