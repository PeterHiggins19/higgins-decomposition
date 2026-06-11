"""CN-TT v4 on REAL coda4microbiome data (Calle, Pujolassos & Susin 2023).
(A) Crohn cross-sectional: lossless reconstruction at D=48 + deterministic diversity
    read, checked vs the KNOWN pattern (reduced diversity in Crohn's disease).
(B) ECAM one child longitudinal: navigation read vs the KNOWN pattern (infant-gut
    diversity rises with age). Checks against established biology = honest validation,
    not novel claims. Interpretation deferred to domain experts."""
import sys, csv, json
from pathlib import Path
import numpy as np
import pyreadr
from scipy import stats
DATA = Path("/sessions/stoic-nifty-davinci/mnt/Claude CoWorker/DATA/MicroBiome/coda4microbiome/data")
ENG = Path("/sessions/stoic-nifty-davinci/mnt/Claude CoWorker/Current-Repo/Hs/HCI-CNTT/engine"); sys.path.insert(0, str(ENG))
import geometry as geo, navigate as nav, atlas as atl, provenance as prov

def treat(M):
    M = M.copy().astype(float)
    for j in range(M.shape[1]):
        col = M[:, j]; pos = col[col > 0]
        if pos.size: M[col <= 0, j] = 0.65 * pos.min()
    return M

rec = {}
print("== (A) Crohn cross-sectional (real; 975 x 48) ==")
r = pyreadr.read_r(str(DATA/"Crohn.rda")); X = r['x_Crohn'].values.astype(float); y = (r['y_Crohn'].iloc[:,0].values == 'CD')
comp = geo.closure(treat(X)); D = comp.shape[1]
charts = atl.hierarchical_atlas(D); edges = atl.edges_from_charts(charts)
recon = max(atl.reconstruct_clr(D, edges, comp[i])[1] for i in range(len(comp)))
keff = np.array([nav.k_eff(comp[i]) for i in range(len(comp))])
cd, ctrl = keff[y], keff[~y]
U, p = stats.mannwhitneyu(cd, ctrl, alternative='two-sided')
print(f"  lossless reconstruction (all 975 samples, D=48): max err = {recon:.1e}")
print(f"  effective diversity K_eff: CD mean={cd.mean():.2f} (n={y.sum()})  control mean={ctrl.mean():.2f} (n={(~y).sum()})")
print(f"  Mann-Whitney p={p:.2e}; direction CD<control: {cd.mean()<ctrl.mean()} (matches known reduced diversity in CD)")
rec["crohn"] = {"D":D,"n":len(comp),"recon_max_err":recon,"keff_CD_mean":float(cd.mean()),"keff_control_mean":float(ctrl.mean()),
                "mannwhitney_p":float(p),"CD_lower_diversity":bool(cd.mean()<ctrl.mean())}

print("\n== (B) ECAM one child longitudinal (real infant gut) ==")
r = pyreadr.read_r(str(DATA/"ecam_filtered.rda")); xe = r['x_ecam'].reset_index(drop=True); md = r['metadata'].reset_index(drop=True)
n_children = md['studyid'].nunique()
top = md['studyid'].value_counts().index[0]; sel = (md['studyid']==top).values
sx = xe[sel].values.astype(float); smd = md[sel].reset_index(drop=True)
dol = smd['day_of_life'].astype(int).values; order = np.argsort(dol, kind='stable')
sx = sx[order]; dol = dol[order]; ab = smd['antiexposedall'].values[order]; deliv = smd['delivery'].iloc[0]
comp = geo.closure(treat(sx)); clr = geo.clr(comp); H = geo.helmert_basis(comp.shape[1]); ilr = clr @ H.T
navout = nav.navigate(comp, clr, ilr)
keff = np.array([s["k_eff"] for s in navout["steps"]])
rho, prho = stats.spearmanr(dol, keff)
bnds = navout["regime_boundaries"]["indices"]; ab_days = sorted(set(int(dol[i]) for i in range(len(ab)) if ab[i]=='y'))
print(f"  dataset: {n_children} children total; analyzed child '{top}' = {len(sx)} timepoints, days {dol.min()}-{dol.max()}, delivery={deliv}")
print(f"  K_eff (effective diversity) vs day_of_life: Spearman rho={rho:.3f} (p={prho:.1e})")
print(f"    -> diversity {'RISES' if rho>0 else 'falls'} with age (known infant-gut maturation: rises)")
print(f"  K_eff: start {keff[:5].mean():.1f} -> end {keff[-5:].mean():.1f}")
print(f"  regime boundaries (compositional shifts): {len(bnds)} flagged; antibiotic-exposed days: {ab_days[:15]}{'...' if len(ab_days)>15 else ''}")
print(f"  deceptive-drift steps: {navout['regime_counts']['deceptive']}; tightening: {navout['regime_counts']['tightening']}; loosening: {navout['regime_counts']['loosening']}")
# determinism
h1 = prov.stable_hash(navout); h2 = prov.stable_hash(nav.navigate(comp, clr, ilr))
print(f"  determinism: identical navigation hash on rerun = {h1==h2}")
rec["ecam"] = {"n_children":int(n_children),"child":str(top),"n_timepoints":int(len(sx)),"day_range":[int(dol.min()),int(dol.max())],
               "delivery":str(deliv),"keff_vs_age_spearman_rho":float(rho),"keff_vs_age_p":float(prho),
               "keff_start":float(keff[:5].mean()),"keff_end":float(keff[-5:].mean()),"n_regime_boundaries":int(len(bnds)),
               "deceptive_steps":int(navout['regime_counts']['deceptive']),"determinism":bool(h1==h2)}
rec["reference"] = "coda4microbiome v0.2.4: Calle, Pujolassos & Susin 2023, BMC Bioinformatics 24:82 (data: Crohn, ecam_filtered)"
json.dump(rec, open(Path(__file__).resolve().parent/"real_microbiome_result.json","w"), indent=2)
print("\nsaved real_microbiome_result.json")
