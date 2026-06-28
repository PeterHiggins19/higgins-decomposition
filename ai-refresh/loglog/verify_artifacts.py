#!/usr/bin/env python3
"""
verify_artifacts.py -- agenda D: codify the fix for the recurring stale-mount torn-write. The system kept
SAYING (through repeated failures) that a Write can leave a torn file in the mount. This makes the heal a single
command: scan every receipted .py artifact, compile it, and report which are INTACT vs TORN -- so the
rebuild-don't-rescue heal is targeted, not per-incident guesswork.

Usage: python3 verify_artifacts.py   -> prints intact/torn counts + the torn list to re-Write.
HONEST: checks COMPILE integrity (the torn-write symptom), not behaviour. Deterministic. Author: Peter Higgins
(human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import os, re, py_compile, json
HS=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",".."))
RX=re.compile(r'receipt_sha256|master_receipt|content_sha256')
intact=[]; torn=[]
for dp,dn,fn in os.walk(HS):
    if os.sep+"DATA" in dp or os.sep+".git" in dp or "__pycache__" in dp: continue
    for f in sorted(fn):
        if not f.endswith(".py"): continue
        p=os.path.join(dp,f); rel=os.path.relpath(p,HS)
        try: txt=open(p,encoding="utf-8",errors="ignore").read()
        except OSError: continue
        if not RX.search(txt): continue
        try: py_compile.compile(p,doraise=True); intact.append(rel)
        except Exception as e: torn.append({"file":rel,"error":str(e).splitlines()[0][:80]})
out={"_meta":{"tool":"verify_artifacts.py","what":"torn-write integrity check over receipted artifacts"},
     "intact":len(intact),"torn":len(torn),"torn_files":torn,
     "action":"re-Write (rebuild-don't-rescue) each torn file from its file-tool view; re-run until torn==0",
     "fence":"checks COMPILE integrity (the torn-write symptom), not behaviour. Peter is the sole gate; nothing posted."}
if __name__=="__main__": print(json.dumps(out,indent=2))
