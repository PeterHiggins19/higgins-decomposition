#!/usr/bin/env python3
"""
onramp_paper_coherence.py -- MEASURE the thing Peter named: do the on-ramps and the arXiv papers cohere?
Coherence here is concrete and checkable: every step of the climb must carry THREE legs that all resolve --
  (1) a PAPER (the arXiv depth),
  (2) an ON-RAMP anchor (the in-their-words entry for the audience band),
  (3) MEASURED EVIDENCE (a receipted result the step actually rests on).
A step "coheres" iff all three files exist AND a band is assigned. If a leg is missing, the step is NOT
coherent -- reported honestly, not papered over. The medical/blood-gas thread (the far-band, deepest-need
case from world_composition_map) is included as its own row so the highest-stakes claim is held to the same
test.

This makes "the on-ramps and the papers cohere" a MEASURED property of the repo, re-runnable by anyone.
HONEST SCOPE: T1 = file-resolution + structural completeness (what this checks). It does NOT judge whether
the prose of a paper and its on-ramp say the same thing in spirit -- that is the collective's integrity pass.
Deterministic; receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001.
2026-06-26. Medical rows are RESEARCH/QA framing only -- never clinical/diagnostic. Peter is the sole gate;
nothing posted.
"""
import os, json, hashlib

HS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
def ex(rel): return bool(os.path.exists(os.path.normpath(os.path.join(HS, rel))))

# step: (paper, onramp_anchor, measured_evidence, audience_band, in_their_words_hook)
STEPS = [
 ("1 Exactness (P1)",
  "papers/cnq_tiling_suite_2026/P1_ABSTRACT_LOCKED.md",
  "library/THE_MAGIC_SHOW_make_visible.md",
  "industrial-instruments/gas-composition-study/blood-gas/README.md",
  "far/medical",
  "your four-part blood/alveolar gas is read EXACTLY -- a quaternion rotation, lossless to machine precision"),
 ("2 Trust (P3)",
  "papers/cnq_tiling_suite_2026/P3_ABSTRACT.md",
  "TRUST_AND_VERIFICATION.md",
  "papers/datasheets/COMPOSITIONAL_SYSTEM_SPECIFICATIONS.md",
  "near/mid",
  "same data, same answer, same fingerprint on any machine -- a measurement, not a guess"),
 ("3 Motion (P4)",
  "papers/PRIOR_ART_compositional_kinematics_2026-06-14.md",
  "library/world_composition_map.py",
  "industrial-instruments/gas-composition-study/blood-gas/results_real_vitaldb/REAL_DATA_RESULTS.md",
  "far/medical",
  "the mix has an arrow: O2 is the helmsman of desaturation -- O2-dominant in 13/13 real anaesthesia cases"),
 ("4 Character (P5)",
  "papers/cnq_tiling_suite_2026/P5_ABSTRACT.md",
  "papers/flagship/Higgins_Decomposition_Character_Analysis.md",
  "library/feedback_chain.py",
  "near/mid",
  "your system shares a CHARACTER with others you'd never compare -- read on its own terms"),
 ("5 Vigilance (P2)",
  "papers/cnq_tiling_suite_2026/P2_ABSTRACT.md",
  "library/THE_MAGIC_SHOW_make_visible.md",
  "industrial-instruments/gas-composition-study/README.md",
  "far/blindness-gap",
  "every alarm stayed green while the mixture turned -- the guard that catches the silent drift"),
 ("6 Foundations (P7+Locked+Duality)",
  "papers/P7_FOUNDATIONS_SEED.md",
  "INDUCTION_MAP.md",
  "papers/locked-discriminant/THE_LOCKED_DISCRIMINANT_PRINCIPLE.md",
  "front-line/peer",
  "why it locks: a reading is reproducible iff it factors through the invariant -- and the flaw is the proof"),
 ("7 CoDa Q-node",
  "papers/coda-q-node/HS_AS_A_Q_NODE_FOR_CODA.md",
  "IS_Hs_RIGHT_FOR_YOU.md",
  "CODA-Association/BUILT_ON_AND_FOR_THE_CODA_COMMUNITY.md",
  "front-line/peer",
  "built on and for your field -- the same geometry, instrumented, handed back"),
 # the highest-stakes far-band case held to the same three-leg test (research/QA only):
 ("* Medical avenue (blood gas/panel)",
  "papers/cnq_tiling_suite_2026/P1_ABSTRACT_LOCKED.md",
  "industrial-instruments/gas-composition-study/blood-gas/results_real_uq/README.md",
  "industrial-instruments/gas-composition-study/blood-gas/results_real_vitaldb/cohort/COHORT_RESULTS.md",
  "far/medical",
  "the deepest-need, farthest-out group: measured exact + O2-helmsman; offer-routing OFF public repo (Southmedic), fenced"),
]

rows = []
for name, paper, onramp, evid, band, hook in STEPS:
    legs = {"paper": ex(paper), "onramp": ex(onramp), "evidence": ex(evid)}
    coheres = all(legs.values()) and bool(band)
    rows.append({"step": name, "band": band, "coheres": coheres, "legs": legs,
                 "paper": paper, "onramp": onramp, "evidence": evid, "in_their_words": hook})

n = len(rows); n_ok = sum(r["coheres"] for r in rows)
missing = [{"step": r["step"], "missing": [k for k, v in r["legs"].items() if not v]}
           for r in rows if not r["coheres"]]
verdict = "COHERES (all steps carry paper + on-ramp + measured evidence)" if n_ok == n \
          else f"GAPS: {n-n_ok}/{n} steps incomplete"

out = {"_meta": {"tool": "onramp_paper_coherence.py",
                 "what": "measured coherence of the climb: each step has paper + on-ramp + evidence",
                 "verdict": verdict, "steps_coherent": f"{n_ok}/{n}"},
       "rows": rows,
       "gaps": missing,
       "fence": ("T1 = file-resolution + structural completeness only; this does NOT judge whether a paper "
                 "and its on-ramp say the same thing in spirit (the collective's integrity pass does). "
                 "Medical rows are RESEARCH/QA framing only -- never clinical/diagnostic; the Southmedic "
                 "offer-routing stays OFF the public repo. Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"] = hashlib.sha256(
    json.dumps([{k: r[k] for k in ("step", "band", "coheres", "legs")} for r in rows],
               sort_keys=True, default=str).encode()).hexdigest()[:16]

if __name__ == "__main__":
    print(json.dumps(out, indent=2, ensure_ascii=False))
