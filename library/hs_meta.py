#!/usr/bin/env python3
"""Compositional Character Space (CCS) — Hs applied recursively to Hs (the second-order read, Hs^2).
Run the kinematics engine across many systems, take each system's diagnostic PROFILE (the engine's
own outputs) as a feature vector, and let Hs read the systems by character: the Character Table.
The finding is character collapse -- the space is ~3-dimensional. Boundary (EITT) + integral
(path efficiency, action) signatures track which realms are mapped and how they behave."""
import numpy as np, csv, glob, sys, json
sys.path.insert(0,"/sessions/sharp-sleepy-bell/mnt/Claude CoWorker/Current-Repo/Hs/Hs-Kinematics")
import hs_kinematics_engine as eng, hs_diagnosis as dx
B="/sessions/sharp-sleepy-bell/mnt/Claude CoWorker"
def loadwide(p):
    rows=[r for r in open(p) if not r.startswith('#') and r.strip()];rd=list(csv.reader(rows))
    return rd[0][1:],np.array([[float(x) for x in r[1:]] for r in rd[1:]])
def profile(name, realm, M, names):
    o=eng.run(M,names); k=o['kinematics_and_dynamics']
    spread=o['navigation_reads']['effective_spread_NAV__entropy_diversity_PHYS']
    return {"system":name,"realm":realm,
            "effective_rank":o['spectral_modes']['degrees_of_freedom_NAV__effective_dimensionality_PHYS'],
            "coherence":k['arrow_of_intent_NAV__momentum_PHYS']['coherence'],
            "path_efficiency":k['course_directness_NAV__path_efficiency_PHYS'],
            "regimes":len(o['navigation_reads']['waypoints_NAV__phase_transitions_PHYS']),
            "trend":round((spread['end']-spread['start']),2),
            "boundary":o['fringe_boundary_TIER3']['verdict'][:12]}
P=[]
# energy realm (real EMBER)
for c in ['deu','wld','jpn','gbr','ind','usa','fra','chn']:
    f=glob.glob(f"{B}/Current-Repo/Hs/HCI-CNT/experiments/codawork2026/ember_{c}/*TWh.csv")
    if f: nm,M=loadwide(f[0]); P.append(profile(f"energy_{c}","energy",M,nm))
# finance realm
f=glob.glob(f"{B}/Current-Repo/Hs/HCI-CNT/experiments/extended/financial_sector/*input.csv")
if f: nm,M=loadwide(f[0]); P.append(profile("finance_sectors","finance",M,nm))
# geology realm (Frielingen D=4)
f=glob.glob(f"{B}/Current-Repo/Hs/collaborations/geology-wehner/demo_frielingen9/frielingen9_xrf_4part.csv")
if f:
    nm,M=loadwide(f[0]); P.append(profile("geology_frielingen","geology",M[:,:4],nm[:4]))
# microbiome realm
f=f"{B}/Current-Repo/Hs/experiments/microbiome_real_2026-06/crohn.csv"
import os
if os.path.exists(f):
    nm,M=loadwide(f); P.append(profile("microbiome_crohn","microbiome",M,nm))
# print profile table
print(f"{'system':22}{'realm':12}{'rank':>5}{'coher':>7}{'pathEff':>8}{'reg':>4}{'trend':>7}")
for p in P: print(f"{p['system']:22}{p['realm']:12}{p['effective_rank']:>5}{p['coherence']:>7}{p['path_efficiency']:>8}{p['regimes']:>4}{p['trend']:>7}")
# ---- Hs ON Hs: classify by directedness x complexity ----
def cls(p):
    directed=(p['coherence']+p['path_efficiency'])/2
    if directed>=0.4 and p['effective_rank']<2.0: return "Ballistic (directed, simple)"
    if directed<0.2 and p['effective_rank']>=4: return "Turbulent (churning, complex)"
    if directed<0.3: return "Diffusive (low-direction)"
    return "Contested (mid)"
classes={}
for p in P: classes.setdefault(cls(p),[]).append(p['system'])
print("\n=== COMPOSITIONAL CHARACTER SPACE -- the Character Table (Hs-squared) ===")
for c,sys_ in classes.items(): print(f"  {c}: {sys_}")
# system-space dimensionality: effective rank of the standardized profile matrix
F=np.array([[p['effective_rank'],p['coherence'],p['path_efficiency'],p['regimes'],p['trend']] for p in P],float)
Fz=(F-F.mean(0))/(F.std(0)+1e-9); s=np.linalg.svd(Fz,compute_uv=False); s=s[s>1e-9]
print(f"\nCCS effective rank (character collapse -- axes distinguishing systems): {(s.sum()**2)/(s**2).sum():.2f} of {F.shape[1]}")
json.dump({"profiles":P,"classes":{k:v for k,v in classes.items()}},open("SYSTEMS_PROFILES.json","w"),indent=1)
