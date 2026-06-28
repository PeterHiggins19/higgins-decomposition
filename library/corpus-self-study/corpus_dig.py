#!/usr/bin/env python3
"""
corpus_dig.py -- Hs turned on US. Peter's falsifiable claim: the system was BUILT BACKWARDS, so "the more one
digs (into the archive/past), the more ADVANCED the work." Test it, honestly, across as many dimensions as the
prose yields. Read every .md in the CoWorker folder (excl DATA/.git), score each on a feature vector, then:
  - read the CORPUS as a composition (clr) -> effective dimension + helmsman dimension (what the corpus is made of)
  - TEST the claim two ways and report whichever way it falls.

Per-file dimensions (all normalized per 1000 words unless noted):
  dig_depth      : archive/draft/old in path (0/1) blended with directory depth  -> "how deep the dig"
  date_min       : earliest YYYY-MM-DD in the text (chronology), if any
  advanced       : density of an advanced-concept vocabulary (quaternion, ilr, locked discriminant, ...)
  formula        : density of math markers (= sum sqrt log x >= <=, code fences)
  receipt        : density of rigor markers (sha256 / receipt / hex hash)  -> the FORWARD-maturity axis
  tier           : density of honest-broker markers (T1/T2/T3, honest-broker)
  crossref       : density of .md cross-links
  words          : length

THE TWO TESTS:
  (A) BACKWARD-CONCEPTS: is 'advanced' higher in the archive (deep dig) than in current?  + corr(advanced, dig_depth)
  (B) FORWARD-RIGOR    : does 'receipt' rise with RECENCY (newer date)?  corr(receipt, recency)
The honest hypothesis going in: the system may show BOTH -- advanced CONCEPTS seeded early (backward depth) AND
RIGOR maturing forward in time. Let the data decide; report means + correlations + coverage.

HONEST SCOPE: 'advanced' is a LEXICAL PROXY (a designed word-list), NOT a true measure of intellectual
advancement -- T2. The correlations ARE measured on the proxies (T1). Deterministic (sorted walk); receipt over
the aggregates. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26.
Peter is the sole gate; nothing posted.
"""
import os, re, json, hashlib, math

ROOT = os.environ.get("CORPUS_ROOT", "/sessions/sharp-sleepy-bell/mnt/Claude CoWorker")
OUTDIR = os.path.dirname(os.path.abspath(__file__))

ADVANCED = ["quaternion","octonion","so(4)","dual-quaternion","clr","ilr","isometric log-ratio","simplex",
 "aitchison","locked discriminant","maximal invariant","eigen","manifold","clifford","hurwitz","tensor",
 "homeostas","kardashev","common-mode","log-ratio","compositional","determinis","closure","helmsman",
 "differential","coherence","invariant","spectral","topolog"]
DATE = re.compile(r"\b(20\d{2})-(\d{2})-(\d{2})\b")
HEXHASH = re.compile(r"\b[0-9a-f]{12,64}\b")
MATH = re.compile(r"[=√∑×≥≤]|\\sum|sqrt|log10|\blog\b")
MDLINK = re.compile(r"\]\([^)]+\.md")
TIER = re.compile(r"\bT[123]\b|honest-broker|honest broker")

def ordinal(y,m,d):
    try: return __import__("datetime").date(int(y),int(m),int(d)).toordinal()
    except Exception: return None

def feats(text, path):
    low = text.lower()
    words = max(len(low.split()), 1)
    per1k = lambda n: round(1000.0*n/words, 3)
    adv = sum(low.count(t) for t in ADVANCED)
    rec = len(HEXHASH.findall(low)) + low.count("receipt") + low.count("sha256")
    math_n = len(MATH.findall(text))
    xref = len(MDLINK.findall(text))
    tier_n = len(TIER.findall(text))
    dates = [ordinal(*m) for m in DATE.findall(text)]
    dates = [d for d in dates if d]
    low_path = path.lower()
    is_archive = int(any(k in low_path for k in ("archive","draft","/old","_bak","pre-")))
    depth = low_path.count(os.sep)
    return {"words":words, "advanced":per1k(adv), "receipt":per1k(rec), "formula":per1k(math_n),
            "crossref":per1k(xref), "tier":per1k(tier_n), "is_archive":is_archive, "depth":depth,
            "date_min":(min(dates) if dates else None)}

# --- walk (deterministic) ---
rows=[]
for dp,dn,fn in sorted(os.walk(ROOT)):
    if os.sep+"DATA" in dp or os.sep+".git" in dp: continue
    for f in sorted(fn):
        if not f.endswith(".md"): continue
        p=os.path.join(dp,f)
        try:
            with open(p,encoding="utf-8",errors="ignore") as fh: text=fh.read()
        except OSError: continue
        rel=os.path.relpath(p,ROOT)
        fe=feats(text,rel); fe["path"]=rel
        rows.append(fe)

N=len(rows)
depths=[r["depth"] for r in rows]; dmin,dmax=min(depths),max(depths)
def dig_depth(r):  # blend archive flag + normalized directory depth
    nd=(r["depth"]-dmin)/max(dmax-dmin,1)
    return round(0.6*r["is_archive"]+0.4*nd,3)
for r in rows: r["dig_depth"]=dig_depth(r)

def pearson(xs,ys):
    pts=[(x,y) for x,y in zip(xs,ys) if x is not None and y is not None]
    if len(pts)<3: return None
    n=len(pts); mx=sum(p[0] for p in pts)/n; my=sum(p[1] for p in pts)/n
    sx=sum((p[0]-mx)**2 for p in pts)**.5; sy=sum((p[1]-my)**2 for p in pts)**.5
    if sx==0 or sy==0: return None
    cov=sum((p[0]-mx)*(p[1]-my) for p in pts)
    return round(cov/(sx*sy),3)

arch=[r for r in rows if r["is_archive"]]; curr=[r for r in rows if not r["is_archive"]]
def mean(rs,k):
    v=[r[k] for r in rs if r[k] is not None]; return round(sum(v)/len(v),3) if v else None

# TEST A: backward-concepts
adv_arch=mean(arch,"advanced"); adv_curr=mean(curr,"advanced")
corr_adv_dig=pearson([r["advanced"] for r in rows],[r["dig_depth"] for r in rows])
# TEST B: forward-rigor (receipt vs recency); recency = date_min (larger ordinal = newer)
dated=[r for r in rows if r["date_min"]]
corr_receipt_recency=pearson([r["receipt"] for r in dated],[r["date_min"] for r in dated])
corr_adv_recency=pearson([r["advanced"] for r in dated],[r["date_min"] for r in dated])

# the corpus as a composition across the 5 lexical dimensions (aggregate density shares)
dims=["advanced","receipt","formula","crossref","tier"]
agg={d:sum(r[d] for r in rows) for d in dims}
tot=sum(agg.values()) or 1.0
share={d:round(agg[d]/tot,4) for d in dims}
def clr(comp):
    import math as _m
    g=_m.exp(sum(_m.log(max(v,1e-9)) for v in comp.values())/len(comp))
    return {k:round(_m.log(max(v,1e-9)/g),3) for k,v in comp.items()}
clr_share=clr(share)
helm=max(clr_share,key=lambda k:abs(clr_share[k]))
eff=round(math.exp(-sum(v*math.log(v) for v in share.values() if v>0)),3)

# top-advanced files + by-top-dir advancement
top_adv=sorted(rows,key=lambda r:-r["advanced"])[:12]
def topdir(rel): return rel.split(os.sep)[0] if os.sep in rel else "."
bydir={}
for r in rows: bydir.setdefault(topdir(r["path"]),[]).append(r["advanced"])
bydir_mean=sorted(((k,round(sum(v)/len(v),3),len(v)) for k,v in bydir.items()),key=lambda t:-t[1])[:12]

verdict_A=("SUPPORTED" if (adv_arch is not None and adv_curr is not None and adv_arch>=adv_curr) else "NOT SUPPORTED")
study={"_meta":{"tool":"corpus_dig.py","n_md_files":N,"what":"Hs-on-us: is 'dig deeper = more advanced' true?"},
  "corpus_as_composition":{"shares":share,"clr":clr_share,"helmsman_dimension":helm,"effective_dimension":round(eff,3),
        "reading":"the dimension the corpus is most made of (by |clr|) is the helmsman"},
  "TEST_A_backward_concepts":{"advanced_density_archive":adv_arch,"advanced_density_current":adv_curr,
        "archive_minus_current":round((adv_arch or 0)-(adv_curr or 0),3),
        "corr_advanced_vs_dig_depth":corr_adv_dig,"n_archive":len(arch),"n_current":len(curr),
        "verdict":verdict_A,
        "meaning":"if archive advanced-density >= current, the deep dig is at least as advanced -> 'built backwards' has support"},
  "TEST_B_forward_rigor":{"corr_receipt_vs_recency":corr_receipt_recency,"corr_advanced_vs_recency":corr_adv_recency,
        "n_dated":len(dated),
        "meaning":"positive corr(receipt,recency) = rigor MATURED FORWARD in time, coexisting with backward-seeded concepts"},
  "top_advanced_files":[{"path":r["path"],"advanced":r["advanced"],"archive":r["is_archive"]} for r in top_adv],
  "advancement_by_top_dir":[{"dir":k,"mean_advanced":m,"n":n} for k,m,n in bydir_mean],
  "fence":("'advanced' is a LEXICAL PROXY (designed word-list), NOT true intellectual advancement (T2); the "
        "correlations are measured on the proxies (T1). Archive-flag and dig_depth are path proxies. Dates are "
        "self-reported in text. Peter is the sole gate; nothing posted.")}
study["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(
    {k:v for k,v in study.items() if k!="_meta"},sort_keys=True,default=str).encode()).hexdigest()[:16]

# write study + the per-file dimension INDEX (improve indexing/documenting of all)
with open(os.path.join(OUTDIR,"CORPUS_DIG_STUDY.json"),"w") as f: json.dump(study,f,indent=2)
index={"_meta":{"tool":"corpus_dig.py","n":N,"dimensions":["dig_depth","is_archive","depth","date_min",
        "advanced","receipt","formula","crossref","tier","words"],"receipt":study["_meta"]["receipt_sha256"]},
       "files":sorted([{k:r[k] for k in ("path","dig_depth","is_archive","depth","date_min","advanced",
        "receipt","formula","crossref","tier","words")} for r in rows],key=lambda r:r["path"])}
with open(os.path.join(OUTDIR,"CORPUS_DIMENSION_INDEX.json"),"w") as f: json.dump(index,f,indent=1)

print(json.dumps({k:study[k] for k in ("_meta","corpus_as_composition","TEST_A_backward_concepts",
    "TEST_B_forward_rigor","advancement_by_top_dir")},indent=2))
