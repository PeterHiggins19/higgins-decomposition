import hashlib, json

# DIVISION ROUTING -- assign every portfolio item to a controlled stream (MATH/INDUSTRY/GOVERNANCE),
# a disposition (OPEN/REVIEW/STEWARD), and a Canada-division flag. Deterministic; receipted.
# Streams are the containers; the export transfer-sensitivity index (tsi) is the gate.

# (item, kind, tsi-from-export-read or None for pure-math, canada_relevant)
ITEMS = [
 # MATH stream (the principle / proofs) -- OPEN, published to the world
 ("P1_D4_ILR_SU2_lossless_tiling","paper",None,False),
 ("methods_proofs_Hs_Kinematics","repo",None,False),
 ("coherence_law","science",None,False),
 ("the_blindness_suite","science",None,False),
 ("dimension_is_the_message","science",None,False),
 ("the_data_is_the_carrier","science",None,False),
 # INDUSTRY stream (applied use-cases) -- tiered by tsi
 ("gas-life-support","industry",0.22,False),
 ("blood-gas-clinical","industry",0.22,False),
 ("geoscience","industry",0.22,False),
 ("backblaze-fleet","industry",0.30,False),
 ("produced-water-oilgas","industry",0.32,False),
 ("financial-markets","industry",0.39,False),
 ("smt-dispense-placement","industry",0.42,False),
 ("energy-grid","industry",0.46,True),
 ("microbiome-bio","industry",0.46,False),
 ("fiber-photonics","industry",0.48,True),
 ("wine-trade-canada-portugal","industry",0.30,True),
 # GOVERNANCE stream (steward / sensitive applied) -- STEWARD
 ("euv-lithography","governance",0.58,True),
 ("constellation-space-SSA","governance",0.55,False),
 ("aerospace-defense-skin(future)","governance",0.58,False),
 ("fusion-nuclear-diag(future)","governance",0.59,False),
 ("space-launch-GNC(future)","governance",0.57,False),
 ("quantum-photonics-mfg(future)","governance",0.55,True),
 ("advanced-packaging-chiplet(future)","governance",0.50,True),
 ("critical-infra-control(future)","governance",0.54,False),
 # GOVERNANCE -- the division rules + Canada track themselves
 ("THE_THREE_STREAM_DIVISION","governance-doc",None,False),
 ("CANADA_DIVISION","governance-doc",None,True),
 ("EXPORT_AND_TRANSFER_GOVERNANCE","governance-doc",None,False),
]

def disp(tsi):
    if tsi is None: return "OPEN"          # pure math / principle
    if tsi>=0.55: return "STEWARD"
    if tsi>=0.42: return "REVIEW"
    return "OPEN"

def stream(kind,tsi):
    if kind in ("paper","repo","science"): return "MATH"
    if kind=="industry": return "INDUSTRY"
    return "GOVERNANCE"

rows=[]
for name,kind,tsi,can in ITEMS:
    rows.append({"item":name,"stream":stream(kind,tsi),"disposition":disp(tsi),
                 "tsi":tsi,"canada_division":can})

counts={}
for r in rows:
    counts.setdefault(r["stream"],{}).setdefault(r["disposition"],0)
    counts[r["stream"]][r["disposition"]]+=1

out={
 "schema":"hs_division_routing/1.0",
 "axis":"deployment/adoption stream division (complementary to papers/PAPER_AND_REPO_DIVISION.md intelligence/data axis)",
 "streams":{"MATH":"controlled-OPEN (principle, published)","INDUSTRY":"controlled-TIERED (OPEN/REVIEW by tsi)","GOVERNANCE":"controlled-STEWARD (sensitive applied -> national steward)"},
 "gate":"disposition set by export transfer-sensitivity index tsi (EXPORT_AND_TRANSFER_GOVERNANCE.md, 14b2f557): OPEN<0.42, REVIEW 0.42-0.55, STEWARD>=0.55; pure-math = OPEN",
 "routing":rows,
 "counts_by_stream_disposition":counts,
 "canada_division_members":[r["item"] for r in rows if r["canada_division"]],
 "moves_note":"Authoritative SEPARATION is this manifest. Physical relocation of any file into a stream folder is STAGED + REVERSIBLE, pending Peter's gate. Nothing moved or deleted on AI authority.",
 "governance":"Publish the principle; gate applied by tsi; defer sensitive release upward to national governance; no company contact; Peter sole gate; nothing posted."
}
out["content_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()
print(json.dumps(out,indent=2))
