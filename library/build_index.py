#!/usr/bin/env python3
"""Hs library indexer — scan the workspace, classify every knowledge file, emit a
context-searchable JSON index + a human-readable library. Skips huge binaries/node_modules."""
import os, json, hashlib, re
from pathlib import Path
ROOT=Path("/sessions/sharp-sleepy-bell/mnt/Claude CoWorker")
SKIP={'node_modules','.git','__pycache__','.venv'}
DOMAINS={'energy':['ember','energy','electric'],'microbiome':['microbiome','crohn','ecam','taxa','glds','spaceflight'],
 'geology':['geolog','frielingen','mudstone','geochem','kimberlite','oxide','igneous'],'finance':['financ','sector','market','commodit','gold'],
 'wine':['wine','vine','oiv','grape'],'gas/medical':['gas','vitaldb','blood','co-oxim','ultrasound'],'audio/acoustic':['audio','acoustic','rwa','smaart','erb'],
 'physics/math':['quaternion','cnq','planck','cosmic','neutrino','nuclear','semf','gauge','manifold','kinematic'],'governance':['huf-gov','governance','doctrine','standard','iso'],
 'engine':['hci-cntt','hci-cnt','engine','cnt','run_cntt','tiling','guard','mechanics','momentum'],'onboarding':['onramp','ai_assist','welcome','start_here','guide','graduate'],
 'data':['.csv','.zip','.xlsx','.tab','data']}
TYPES={'.py':'code','.r':'code','.ipynb':'notebook','.md':'doc','.json':'data/node','.csv':'data','.zip':'data','.xlsx':'data',
 '.pdf':'doc/pdf','.docx':'doc','.html':'interactive','.svg':'figure','.png':'figure','.tab':'data','.txt':'doc'}
def domain(p):
    s=p.lower()
    for d,ks in DOMAINS.items():
        if any(k in s for k in ks): return d
    return 'general'
recs=[]; bydom={}; bytype={}; byrepo={}
for base in ['Current-Repo/Hs','Current-Repo/HUF','Current-Repo/RWA','DATA','docs','Studies','EITT']:
    bp=ROOT/base
    if not bp.exists(): continue
    for dp,dirs,files in os.walk(bp):
        dirs[:]=[d for d in dirs if d not in SKIP]
        for fn in files:
            fp=Path(dp)/fn; rel=str(fp.relative_to(ROOT)); ext=fp.suffix.lower()
            try: sz=fp.stat().st_size
            except: sz=0
            typ=TYPES.get(ext,'other'); dom=domain(rel)
            repo=base.split('/')[-1]
            rec={"path":rel,"name":fn,"ext":ext,"type":typ,"domain":dom,"repo":repo,"size":sz}
            recs.append(rec)
            bydom.setdefault(dom,0); bydom[dom]+=1
            bytype.setdefault(typ,0); bytype[typ]+=1
            byrepo.setdefault(repo,0); byrepo[repo]+=1
# context-search structure: index by domain and by type
index_by_domain={}; index_by_type={}
for r in recs:
    index_by_domain.setdefault(r['domain'],[]).append(r['path'])
    index_by_type.setdefault(r['type'],[]).append(r['path'])
out={"schema":"hs_library_index/1.0","generated":"2026-06-15","root":"Claude CoWorker/",
 "total_files":len(recs),"counts":{"by_domain":bydom,"by_type":bytype,"by_repo":byrepo},
 "context_search":{"by_domain":index_by_domain,"by_type":index_by_type},
 "files":sorted(recs,key=lambda r:(r['domain'],r['repo'],r['path']))}
json.dump(out,open(ROOT/"Current-Repo/Hs/library/LIBRARY_INDEX.json","w"),indent=1)
print(f"indexed {len(recs)} files")
print("by domain:",dict(sorted(bydom.items(),key=lambda x:-x[1])))
print("by type:",dict(sorted(bytype.items(),key=lambda x:-x[1])))
print("by repo:",byrepo)
