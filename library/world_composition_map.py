#!/usr/bin/env python3
"""
world_composition_map.py -- read the world ITSELF as a composition: which systems are compositional,
which are not, who is closest to the front line (already reading ratios) and who is farthest (compositional
data but reading totals -- the blindness gap). Then derive the STAGED on-ramp: guidance depth scaled to how
far each audience sits from the front line, so communication is coherent without being conspicuous.

Two read-axes per domain (each 0..1):
  need     = how compositional the domain's data really is  = mean(closure, proportion_action, multipart)
  literacy = how much the field ALREADY reads ratios/log-ratios/shares (short on-ramp if high)

Derived (deterministic):
  front_line_proximity = need * literacy          -> high = already operating compositionally (peers)
  guidance_depth       = need * (1 - literacy)     -> high = needs it but cannot see it (max scaffolding)
  door_fit             = need                       -> below threshold = friendly redirect (composition-is-qualifier)

HONEST SCOPE: the per-domain axis scores are REASONED ESTIMATES (T2 designed judgment), not a measured
survey. The MATH on them is deterministic and receipted; the INPUTS are a rubric. Falsifier: survey real
practitioners in each field for closure/proportion-action/literacy and refit. Nothing here profiles a person
-- it sorts FIELDS by how their data behaves, to meet each where it lives. Author: Peter Higgins (human
authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import json, hashlib

# domain: (closure, proportion_action, multipart, literacy)  -- all 0..1, reasoned estimates (T2)
W = {
 # --- fields whose data is parts-of-a-whole AND who already read it that way (front line / peers) ---
 "geochemistry / mineralogy (CoDa home)":     (0.98, 0.95, 0.95, 0.92),
 "microbiome / metagenomics":                 (0.97, 0.92, 0.97, 0.80),
 "analytical chemistry / assays":             (0.95, 0.90, 0.90, 0.72),
 "portfolio / asset allocation":              (0.92, 0.95, 0.85, 0.74),
 "ecology / species abundance":               (0.90, 0.82, 0.92, 0.70),
 "psephology / vote share":                   (0.88, 0.85, 0.80, 0.66),
 # --- compositional, partly literate (near / mid) ---
 "energy mix / grid (EMBER)":                 (0.90, 0.85, 0.85, 0.52),
 "process gas / emissions monitoring":        (0.92, 0.88, 0.82, 0.46),
 "nutrition / diet composition":              (0.85, 0.78, 0.85, 0.45),
 "marketing / market share":                  (0.82, 0.80, 0.70, 0.46),
 "materials / alloys / SMT solder":           (0.85, 0.80, 0.78, 0.42),
 "demography / census shares":                (0.80, 0.70, 0.82, 0.50),
 "epidemiology / case mix":                   (0.78, 0.72, 0.78, 0.42),
 # --- compositional but reading TOTALS (far -- the blindness gap, biggest payoff) ---
 "clinical labs / blood panels":              (0.82, 0.78, 0.85, 0.26),
 "macroeconomics / national accounts":        (0.78, 0.72, 0.80, 0.30),
 "climate / atmospheric composition":         (0.80, 0.75, 0.78, 0.34),
 "supply chain / fleet & SKU mix":            (0.76, 0.74, 0.75, 0.30),
 "telecom / network traffic mix":             (0.72, 0.68, 0.72, 0.30),
 "sports analytics / play mix":               (0.66, 0.62, 0.68, 0.34),
 # --- not really compositional (off-door -- friendly redirect, NOT a target) ---
 "single-sensor process control (temp/press)":(0.22, 0.30, 0.20, 0.30),
 "timing / latency measurement":              (0.18, 0.25, 0.15, 0.35),
 "astrometry / position & distance":          (0.20, 0.22, 0.25, 0.40),
}

DOOR = 0.45      # below this 'need' the field is redirected, not targeted (composition-is-qualifier)
rows = []
for name,(cl,pa,mp,lit) in W.items():
    need = round((cl+pa+mp)/3, 3)
    prox = round(need*lit, 3)
    depth = round(need*(1-lit), 3)
    if need < DOOR:
        bucket, onramp = "off-door", "friendly redirect (no composition -> kindly out of scope; no targeting)"
    elif prox >= 0.55:
        bucket, onramp = "front-line (peer)", "Stage P: hand the instrument + receipt; a 2nd viewpoint, no scaffolding"
    elif depth >= 0.42:
        bucket, onramp = "far (blindness gap)", "Stage 0-1: full magic show (their own data first), deceptive-drift reveal, max guidance"
    else:
        bucket, onramp = "near/mid", "Stage 2-3: one new read on their own data, light bridge to the relational view"
    rows.append({"domain":name,"need":need,"literacy":lit,"front_line_proximity":prox,
                 "guidance_depth":depth,"bucket":bucket,"onramp":onramp})

rows.sort(key=lambda r:(-r["front_line_proximity"], -r["need"]))
order = [r["domain"] for r in rows]                      # near -> far ranking
buckets = {}
for r in rows: buckets.setdefault(r["bucket"], []).append(r["domain"])

# the staged guidance ladder (depth scaled to distance) -- the deliverable shape
ladder = {
 "front-line (peer)":   {"who":"already read ratios","words":"peer-to-peer; offer the determinism + receipt as a second viewpoint on data they already trust; no mountain, no props","reveal":"none needed"},
 "near/mid":            {"who":"compositional, partly literate","words":"one re-computable win on their OWN data; name the helmsman; hand the gauge","reveal":"light"},
 "far (blindness gap)": {"who":"compositional data, read as totals","words":"start with a prop they own (bread/yeast, the gas tank); the silent-drift surprise; one rabbit at a time","reveal":"full magic show"},
 "off-door":            {"who":"not compositional","words":"the friendly door: 'parts of a whole that move? then this is for you; if not, it isn't -- and that's fine'","reveal":"redirect, never pursue"},
}

out = {"_meta":{"tool":"world_composition_map.py",
                "what":"the world read as a composition -> who is near/far the front line -> staged on-ramp depth",
                "door_threshold_need":DOOR,"n_domains":len(W)},
       "ranking_near_to_far":order,
       "by_bucket":buckets,
       "rows":rows,
       "staged_guidance_ladder":ladder,
       "non_obvious_rule":("Tailor the DEPTH to the bucket; never DISPLAY the tailoring. Speak each field in "
                "its own data, not in the meta-model of the listener -- relevance reads as care, a visible "
                "profile reads as surveillance. The map stays back-stage; only the right-depth on-ramp shows."),
       "fence":("Axis scores are reasoned estimates (T2), not a measured survey; the math on them is "
                "deterministic + receipted. This sorts FIELDS by how their data behaves, not individuals. "
                "Anticipation here = meeting-where-they-are (a good teacher pitching to level), NOT deception: "
                "no false facts, reveal+invite, the human keeps the gate. Falsifier: survey real practitioners "
                "and refit. Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(
    json.dumps({"rows":rows,"door":DOOR},sort_keys=True,default=str).encode()).hexdigest()[:16]

if __name__=="__main__":
    print(json.dumps(out,indent=2,ensure_ascii=False))
