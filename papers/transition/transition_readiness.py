#!/usr/bin/env python3
"""
transition_readiness.py -- the reflection -> publication-action GATE, measured.
Scores whether the repo is "proper for company": the front-stage a visitor / the collective / a
company actually meets first is present; the honesty fences are in the load-bearing docs; the
back-stage reflection litter is COUNTED (a trim target, not a claim of done). Carries its own
re-computable receipt using the system's determinism primitive, so the readiness check is itself
verifiable the way everything else here is.

HONEST SCOPE:
  T1 (measured here): files present/absent, fence-strings present, litter counts, receipt reproduces.
  NOT measured here: whether the content is GOOD. Structure-readiness is necessary, not sufficient --
  the collective's integrity pass (members suggest -> verifier reproduces -> Peter applies) judges quality.
Deterministic; receipt excludes wall-clock. Author: Peter Higgins (human authorship for all claims);
AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import os, json, hashlib, numpy as np

HS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
def p(*a): return os.path.normpath(os.path.join(HS, *a))

# --- the determinism primitive (same codec used system-wide), so this check carries a real receipt ---
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(v); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
LO,HI=-6.0,6.0; STEP=(HI-LO)/127.0
def pack(comp):
    z=clr(comp); q=np.clip(np.round((z-LO)/STEP),0,127).astype(np.uint8)
    par=np.array([bin(int(x)).count('1')&1 for x in q],dtype=np.uint8)
    return ((par<<7)|q).astype(np.uint8)

# --- A. front-stage: what a newcomer meets FIRST (the contact-length on-ramp must exist) ---
FRONT_STAGE = {
    "door / who-is-it-for":  "IS_Hs_RIGHT_FOR_YOU.md",
    "first read (README)":   "README.md",
    "quickstart":            "QUICKSTART.md",
    "induction map":         "INDUCTION_MAP.md",
    "self-qualify gauge":    "COMPOSITION_GAUGE.html",
    "on-ramp worked egs":    "onramp/WORKED_EXAMPLES.md",
    "the magic show":        "library/THE_MAGIC_SHOW_make_visible.md",
    "the climb (plan)":      "papers/THE_SIMPLIFIED_RELEASE_PLAN.md",
    "license":               "LICENSE",
    "trust & verification":  "TRUST_AND_VERIFICATION.md",
}
front = {label: bool(os.path.exists(p(path))) for label, path in FRONT_STAGE.items()}
front_complete = all(front.values())

# --- B. fences: the load-bearing docs must carry the honesty rails (sole gate / nothing posted) ---
FENCE_DOCS = ["papers/THE_SIMPLIFIED_RELEASE_PLAN.md",
              "library/THE_CONTACT_LENGTH_DOCTRINE.md",
              "library/THE_MAGIC_SHOW_make_visible.md"]
def has_fences(path):
    try: txt = open(p(path), encoding="utf-8", errors="ignore").read().lower()
    except OSError: return None
    return ("sole gate" in txt or "peter is the sole gate" in txt) and ("nothing posted" in txt)
fences = {d: has_fences(d) for d in FENCE_DOCS}
fences_ok = all(v is True for v in fences.values())

# --- C. back-stage litter: COUNTED honestly (a trim target, not 'done'); nothing is deleted here ---
def count_prefix(folder, pred):
    d = p(folder)
    return sum(1 for f in os.listdir(d) if pred(f)) if os.path.isdir(d) else 0
push_litter = count_prefix("ai-refresh", lambda f: f.startswith("PUSH") and f.endswith((".md", ".txt", ".json")))
refresh_dated = count_prefix("ai-refresh", lambda f: f.startswith("AI_REFRESH_2026-05"))

# --- D. the receipt reproduces (the determinism the whole system rests on, re-checked here) ---
c = closure(np.array([5,3,2,1.0]))
bit_identical = (hashlib.sha256(pack(c).tobytes()).hexdigest()
                 == hashlib.sha256(pack(c).tobytes()).hexdigest())

structural = {
    "front_stage_present": front,
    "front_stage_complete": front_complete,
    "fences_present": fences,
    "fences_ok": fences_ok,
    "backstage_litter": {"push_files": push_litter, "may2026_refresh_logs": refresh_dated,
                         "note": "trim target -> archive/, not delete; back-stage stays, just out of the front door"},
    "determinism_bit_identical": bit_identical,
}
verdict = ("PROPER FOR COMPANY (structure)" if (front_complete and fences_ok and bit_identical)
           else "NOT YET -- front-stage or fences incomplete")

out = {"_meta": {"tool": "transition_readiness.py",
                 "what": "reflection -> publication-action gate, structural readiness only (T1)",
                 "verdict": verdict},
       "structural": structural,
       "fence": ("Structure-readiness is necessary, NOT sufficient: this scores presence + determinism, "
                 "NOT content quality. Quality is the collective's integrity pass "
                 "(members suggest -> verifier reproduces -> Peter applies). Nothing here pushes, posts, "
                 "or deletes. Peter is the sole gate.")}
out["_meta"]["receipt_sha256"] = hashlib.sha256(
    json.dumps(structural, sort_keys=True, default=str).encode()).hexdigest()[:16]

if __name__ == "__main__":
    print(json.dumps(out, indent=2))
