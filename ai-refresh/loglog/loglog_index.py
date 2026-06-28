#!/usr/bin/env python3
"""
loglog_index.py -- THE LOG/LOG: a recursive tracking mechanism, a log of the logs, that manages all of this.

The system already has many trackers (logs): the journal (HS_TRACKING_LOG), the memory index (MEMORY.md), the
induction/abstract indexes, and the receipts embedded in every artifact. As the work grows, the trackers
themselves need tracking. The log/log is the index ONE LEVEL UP: it indexes the logs (not the artifacts), checks
that the logs cover the artifacts, and -- recursively -- INDEXES ITSELF, so the management layer is a closed
fixed point (every tier is tracked by the tier above; the top tracks itself).

Three tiers:
  TIER 0  artifacts   : every .py carrying a deterministic receipt (the receipted body of work).
  TIER 1  logs        : the trackers that index Tier 0 -- the journal, the memory, the indexes/ledgers.
  TIER 2  the LOG/LOG : the index of the Tier-1 logs + its OWN self-entry (recursive). This file.

On each run it SCANS, builds the index-of-indexes, reports COVERAGE (are artifacts logged? are logs present?)
and GAPS, and emits a deterministic receipt. Re-run: same receipt if nothing changed; a diff localizes what did
(the determinism-anchor cycle, applied to the management layer). HONEST: this tracks PRESENCE/coverage of the
logs, not the quality of what they record. Deterministic; receipt. Author: Peter Higgins (human authorship for
all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import os, re, json, hashlib

HS=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",".."))
RX=re.compile(r'receipt_sha256|master_receipt')

def scan_receipted():
    found=[]
    for dp,dn,fn in os.walk(HS):
        if os.sep+"DATA" in dp or os.sep+".git" in dp or "__pycache__" in dp: continue
        for f in sorted(fn):
            if not f.endswith(".py"): continue
            p=os.path.join(dp,f)
            try: txt=open(p,encoding="utf-8",errors="ignore").read()
            except OSError: continue
            if RX.search(txt):
                found.append(os.path.relpath(p,HS))
    return sorted(found)

# TIER 0 -- receipted artifacts
artifacts=scan_receipted()

# TIER 1 -- the logs (trackers) that index Tier 0
def exists(rel): return os.path.exists(os.path.join(HS,rel))
TIER1=[
 {"log":"journal","path":"ai-refresh/HS_TRACKING_LOG.json","indexes":"every G-entry: objective + docs + receipt"},
 {"log":"memory_index","path":"(spaces)/memory/MEMORY.md","indexes":"durable cross-session facts (external to repo)","external":True},
 {"log":"induction_map","path":"INDUCTION_MAP.md","indexes":"human traversal of the repo"},
 {"log":"abstract_ledger","path":"papers/ABSTRACT_LEDGER.md","indexes":"the publication abstracts"},
 {"log":"session_capstone","path":"ai-refresh/SESSION_CAPSTONE_2026-06-26.md","indexes":"this session's artifacts by four-pole spine"},
]
# journal coverage
jpath=os.path.join(HS,"ai-refresh","HS_TRACKING_LOG.json")
gentries=0; jdocs=set()
try:
    J=json.load(open(jpath))
    for e in J.get("tracks",{}).get("engine_build_v4",[]):
        if isinstance(e,dict) and str(e.get("id","")).startswith("G-"):
            gentries+=1
            for dpath in e.get("docs",[]): jdocs.add(os.path.normpath(dpath))
except Exception: pass
artifacts_in_journal=sum(1 for a in artifacts if any(os.path.normpath(a)==d or os.path.basename(a)==os.path.basename(d) for d in jdocs))

# TIER 2 -- the log/log: index the Tier-1 logs + SELF (recursion)
SELF="ai-refresh/loglog/loglog_index.py"
loglog_entries=[{"tracker":t["log"],"path":t["path"],"present":bool(t.get("external") or exists(t["path"])),
                 "indexes":t["indexes"]} for t in TIER1]
loglog_entries.append({"tracker":"loglog_index (SELF)","path":SELF,"present":exists(SELF),
                       "indexes":"the Tier-1 logs AND itself -- the recursive fixed point"})

coverage={
 "tier0_receipted_artifacts":len(artifacts),
 "tier1_logs_present":sum(1 for t in TIER1 if t.get("external") or exists(t["path"])),
 "tier1_logs_total":len(TIER1),
 "journal_G_entries":gentries,
 "artifacts_referenced_in_journal_docs":artifacts_in_journal,
 "loglog_indexes_itself":bool(exists(SELF)),
}
gaps=[]
if coverage["tier1_logs_present"]<coverage["tier1_logs_total"]:
    gaps+= [f"missing log: {t['path']}" for t in TIER1 if not (t.get('external') or exists(t['path']))]
if artifacts_in_journal < len(artifacts):
    gaps.append(f"{len(artifacts)-artifacts_in_journal} receipted artifacts not (yet) name-matched in journal docs (cross-link debt)")

out={"_meta":{"tool":"loglog_index.py","what":"recursive log-of-logs: tracks the trackers, indexes itself",
              "tiers":["artifacts","logs","log/log"]},
     "tier2_loglog_the_index_of_logs":loglog_entries,
     "coverage":coverage,"gaps":gaps,
     "tier0_artifacts_sample":artifacts[:12]+(["...(%d total)"%len(artifacts)] if len(artifacts)>12 else []),
     "recursion_note":"the log/log lists itself as a tracked tracker -> the management layer closes: each tier is tracked by the tier above, the top tracks itself (a fixed point).",
     "fence":("Tracks PRESENCE/coverage of the logs (a deterministic structural read), not the QUALITY of what "
              "they record. The artifact<->journal match is by path/basename; 'gaps' are cross-link debt to "
              "close, not errors. Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(
    {"art":artifacts,"loglog":loglog_entries,"cov":coverage},sort_keys=True,default=str).encode()).hexdigest()[:16]
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"LOGLOG_INDEX.json"),"w") as f:
    json.dump(out,f,indent=2)
if __name__=="__main__": print(json.dumps({k:out[k] for k in ("_meta","coverage","gaps","recursion_note")},indent=2))
