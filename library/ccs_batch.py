#!/usr/bin/env python3
"""Expand Compositional Character Space across the whole home data hold. Runs the kinematics
engine on every engine-ready real composition, extracts the CCS profile, checkpoints each to
ccs_results.jsonl (resumable against the sandbox wall-limit). Finalize step computes CCS rank
+ characters at scale. Author: Peter Higgins; AI-assisted per HUF-STD-001. Honest-broker."""
import numpy as np, csv, glob, sys, json, os, time, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0,"/sessions/sharp-sleepy-bell/mnt/Claude CoWorker/Current-Repo/Hs/Hs-Kinematics")
import hs_kinematics_engine as eng
B="/sessions/sharp-sleepy-bell/mnt/Claude CoWorker/Current-Repo/Hs"
V="/sessions/sharp-sleepy-bell/mnt/Claude CoWorker/Current-Repo/Hs/experiments/2026-05-10_full-corpus-validation/raw_inputs"
CK="ccs_results.jsonl"

def loadwide(p):
    rows=[r for r in open(p,encoding='utf-8',errors='replace') if r.strip() and not r.lstrip().startswith('#')]
    rd=list(csv.reader(rows)); hdr=rd[0][1:]
    M=[]; 
    for r in rd[1:]:
        try: M.append([float(x) for x in r[1:1+len(hdr)]])
        except: pass
    return hdr, np.array(M,float)

def profile(name, realm, p):
    nm,M=loadwide(p)
    M=np.clip(M,0,None)
    keep=M.sum(1)>0; M=M[keep]
    if M.shape[0]<6 or M.shape[1]<4: return None
    o=eng.run(M,nm)
    k=o['kinematics_and_dynamics']; spread=o['navigation_reads']['effective_spread_NAV__entropy_diversity_PHYS']
    return {"system":name,"realm":realm,"shape":[M.shape[0],M.shape[1]],
        "effective_rank":round(o['spectral_modes']['degrees_of_freedom_NAV__effective_dimensionality_PHYS'],3),
        "coherence":round(k['arrow_of_intent_NAV__momentum_PHYS']['coherence'],3),
        "path_efficiency":round(k['course_directness_NAV__path_efficiency_PHYS'],3),
        "regimes":len(o['navigation_reads']['waypoints_NAV__phase_transitions_PHYS']),
        "trend":round(spread['end']-spread['start'],2)}

# ---- build the catalogue (curated, deduplicated, multi-dimensional) ----
C=[]
for p in sorted(glob.glob(f"{V}/owid_energy_*.csv")):
    iso=p.split("_")[-1][:3]; C.append((f"energy_owid_{iso}","energy",p))
for p in sorted(glob.glob(f"{B}/HCI-CNT/experiments/codawork2026/ember_*/*generation_TWh.csv")):
    iso=os.path.basename(p).split("_")[1]; C.append((f"energygen_ember_{iso}","energy-gen",p))
C.append(("energygen_ember_CAN","energy-gen",f"{B}/experiments/canada_energy_2026-06/ember_CAN_Canada_generation_TWh.csv"))
for tag in ["by_age","by_tas","by_region","top10","top20","top40","top60","top80","top95"]:
    g=glob.glob(f"{B}/experiments/Hs-05_Geochemistry/region_binning/ball_{tag}*barycenters.csv")
    if g: C.append((f"geo_ball_{tag}","geology",g[0]))
for nm,fn in [("geo_qin_cpx","qin_cpx_by_location_barycenters.csv"),("geo_stracke_oib","stracke_oib_by_location_barycenters.csv"),("geo_tappe_kim","tappe_kim1_by_country_barycenters.csv")]:
    C.append((nm,"geology",f"{V}/{fn}"))
C.append(("geo_frielingen","geology",f"{B}/collaborations/geology-wehner/demo_frielingen9/frielingen9_xrf_4part.csv"))
for nm,fn in [("econ_fao_credit","fao_credit_to_agriculture.csv"),("econ_fao_va_aff","fao_value_added_aff.csv"),("econ_fao_va_agri","fao_value_added_agriculture.csv"),("econ_fao_va_food","fao_value_added_food_mfg.csv")]:
    C.append((nm,"economy",f"{V}/{fn}"))
E=f"{B}/HCI-CNT/experiments"
C+=[("finance_sp_sectors","finance",f"{E}/extended/financial_sector/financial_sector_input.csv"),
    ("nuclear_semf","nuclear",f"{E}/reference/nuclear_semf/nuclear_semf_input.csv"),
    ("cosmo_planck","cosmology",f"{E}/extended/esa_planck_cosmic/esa_planck_cosmic_input.csv"),
    ("cosmo_energy_budget","cosmology",f"{B}/experiments/Hs-25_Cosmic_Energy_Budget/Hs-25_cosmic_energy_budget.csv"),
    ("climate_iiasa_ngfs","climate-scenario",f"{E}/extended/iiasa_ngfs/iiasa_ngfs_input.csv"),
    ("urban_markham_budget","urban",f"{E}/extended/markham_budget/markham_budget_input.csv"),
    ("chem_oxide","chemistry",f"{E}/extended/chemixhub_oxide/chemixhub_oxide_input.csv"),
    ("tech_backblaze_fleet","tech",f"{B}/experiments/Hs-17_Backblaze/Hs-17_fleet_composition.csv"),
    ("lang_conversation_drift","language",f"{B}/experiments/Hs-20_Conversation_Drift/Hs-20_milestone_compositions.csv"),
    ("micro_crohn","microbiome",f"{B}/experiments/microbiome_real_2026-06/crohn.csv"),
    ("micro_ecam","microbiome",f"{B}/experiments/microbiome_real_2026-06/ecam_child.csv")]

done=set()
if os.path.exists(CK):
    for ln in open(CK):
        try: done.add(json.loads(ln)["system"])
        except: pass
t0=time.time(); n=0
with open(CK,"a") as f:
    for name,realm,p in C:
        if name in done: continue
        if time.time()-t0>36: print(f"[budget] stopping; {len(done)+n}/{len(C)} done, rerun to continue"); break
        if not os.path.exists(p): continue
        try:
            pr=profile(name,realm,p)
            if pr: f.write(json.dumps(pr)+"\n"); f.flush(); n+=1
        except Exception as e:
            pass
print(f"ran {n} this pass; total catalogue={len(C)}; checkpointed={len(done)+n}")
