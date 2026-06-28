#!/usr/bin/env python3
"""
tetrode_completeness_analyzer.py -- let the analysis of the current group tell the next components to build.
The tetrode standard (huf-gov/doctrine/THE_TETRODE_STANDARD_for_sensitive_studies.md) requires every sensitive
study to be FOUR independent legs. This reads the current built/registered group, sorts it into its sensitive
clusters, compares to the required four INDEPENDENT modalities, and names the missing components -- so the next
build is decided by the gap, not by guess.

Deterministic; receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001.
2026-06-27. These are PLANS/SEEDS named by the analysis, not built studies; each must be an INDEPENDENT leg on
real data, fenced and gated. Peter is the sole gate; nothing posted.
"""
import json, hashlib
def sha(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()[:16]
STUDIES=[
 {"id":"P-psi","cluster":"Peterson cognition","modality":"linguistic-cultural","status":"built","receipt":"8ec3ae8d5623c5d7"},
 {"id":"P-nu","cluster":"Peterson cognition","modality":"neural-computational","status":"built","receipt":"b7fd9a39b664dc1a"},
 {"id":"P-mu","cluster":"medical (sensitive)","modality":"clinical-epidemiology","status":"built","receipt":"0c44c4a150cad7f0"},
]
REQUIRED={  # 4 INDEPENDENT legs per sensitive cluster
 "Peterson cognition":["linguistic-cultural","neural-computational","behavioral-survey","personality-structural"],
 "medical (sensitive)":["clinical-epidemiology","hematologic","microbiome-molecular","physiologic-respiratory"],
}
NEXT={
 "behavioral-survey":"World Values Survey value-priorities as a composition (real public survey; what people rank as important)",
 "personality-structural":"Big Five higher-order metatraits (Stability/Plasticity) from public item data (Open Psychometrics) -- Peterson's own empirical domain",
 "hematologic":"Blood / CBC differential composition (the 4-channel blood tetrode)",
 "microbiome-molecular":"Microbiome relational read (real data already in hand -- Crohn/HIV, CMP work)",
 "physiologic-respiratory":"Respiratory gas-mix composition (Southmedic channel; O2/CO2/agent)",
}
report={}
for cluster,req in REQUIRED.items():
    built=[s for s in STUDIES if s["cluster"]==cluster]; have=[s["modality"] for s in built]
    missing=[m for m in req if m not in have]
    report[cluster]={"required_legs":4,"have_count":len(built),"missing_count":len(missing),
        "built":[{"id":s["id"],"modality":s["modality"],"receipt":s["receipt"]} for s in built],
        "next_components_to_build":[{"modality":m,"component":NEXT[m]} for m in missing],
        "tetrode_complete":len(built)>=4}
checks={
 "two_sensitive_clusters": bool(len(report)==2),
 "peterson_needs_2_more": bool(report["Peterson cognition"]["missing_count"]==2),
 "medical_needs_3_support_cases": bool(report["medical (sensitive)"]["missing_count"]==3),
 "neither_complete_yet": bool(not any(c["tetrode_complete"] for c in report.values())),
}
master=sha(report)
out={"_meta":{"tool":"tetrode_completeness_analyzer.py","what":"analyze the group -> next components for the two tetrodes",
              "receipt_sha256":master},
     "analysis":report,"checks":checks,
     "verdict":("THE ANALYSIS NAMES THE NEXT COMPONENTS. Peterson-cognition tetrode: 2/4 built (P-psi linguistic, "
        "P-nu neural) -> build 2 more (behavioral-survey, personality-structural). Medical-quality tetrode: 1/4 "
        "built (P-mu cancer-epidemiology) -> build 3 support cases (hematologic, microbiome-molecular, "
        "physiologic-respiratory). Four independent legs each; the gap, not a guess, sets the build order.") if all(checks.values()) else "CHECK FAILED",
     "fence":("Plans/seeds named by the analysis, NOT built studies. Each must be an INDEPENDENT leg on real data "
        "(correlated legs buy nothing -- the tetrode independence fence). Medical legs stay research/epidemiology, "
        "not clinical, until validated. Any Peterson approach off-repo + Peter-gated. Peter is the sole gate; nothing posted.")}
if __name__=="__main__": print(json.dumps(out,indent=2))
