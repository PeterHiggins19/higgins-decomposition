#!/usr/bin/env python3
"""
EXPORT-SENSITIVITY READ -- Hs applied to its own application portfolio (deterministic; hash-receipted).

Each industrial use-case is read as a composition over four export/transfer-sensitivity axes; the engine then
ranks which applications must transfer to a governance steward and which publish openly. This operationalizes the
EXPORT_AND_TRANSFER_GOVERNANCE doctrine: the PRINCIPLE of every app is publishable; only the APPLIED how-to of
the high-sensitivity apps transfers upward.

  A1 open_science    : share that is publishable principle (basic science)
  A2 applied_knowhow  : share that is transferable applied how-to
  A3 controlled_adj   : proximity to export-controlled / dual-use technology
  A4 strategic_weight : impingement on global economics / national security
  transfer_sensitivity_index (tsi) = closed share of (controlled_adj + strategic_weight)

Axis scores are HONEST JUDGMENT INPUTS (Tier 3); the compositional read + ranking are deterministic.
Author: Peter Higgins; AI-assisted per HUF-STD-001. Internal governance tool.
"""
import hashlib, json
import numpy as np

AXES = ["open_science", "applied_knowhow", "controlled_adj", "strategic_weight"]

# (name, already_done?, [A1,A2,A3,A4] on 0-10)
APPS = [
 ("gas-life-support",          1, [8,5,1,2]),
 ("produced-water-oilgas",     1, [7,5,2,3]),
 ("blood-gas-clinical",        1, [8,5,1,2]),
 ("financial-markets",         1, [7,6,2,6]),
 ("constellation-space-SSA",   1, [6,6,7,8]),
 ("smt-dispense-placement",    1, [6,7,4,5]),
 ("fiber-photonics",           1, [6,7,6,6]),
 ("euv-lithography",           1, [6,7,9,9]),
 ("backblaze-fleet",           1, [7,6,2,3]),
 ("geoscience",                1, [9,4,1,2]),
 ("energy-grid",               1, [7,5,4,6]),
 ("microbiome-bio",            1, [7,5,5,5]),
 ("quantum-photonics-mfg",     0, [6,7,8,8]),
 ("advanced-packaging-chiplet",0, [6,7,6,7]),
 ("aerospace-defense-skin",    0, [5,7,8,9]),
 ("fusion-nuclear-diag",       0, [6,6,9,9]),
 ("critical-infra-control",    0, [6,6,6,8]),
 ("telecom-6g-comms",          0, [6,7,6,6]),
 ("autonomous-robotics",       0, [6,7,5,6]),
 ("space-launch-GNC",          0, [5,7,8,8]),
]

def clr(p):
    L = np.log(p); return L - L.mean()

def disposition(t):
    if t >= 0.55: return "STEWARD (offer applied how-to to national governance; gov decides distribution)"
    if t >= 0.42: return "REVIEW (principle public; applied how-to to steward)"
    return "OPEN (publish; low transfer sensitivity)"

def main():
    names = [a[0] for a in APPS]
    X = np.array([a[2] for a in APPS], float) + 0.5
    P = X / X.sum(axis=1, keepdims=True)
    tsi = P[:, 2] + P[:, 3]
    rows = []
    for i, n in enumerate(names):
        rows.append({"app": n, "done": bool(APPS[i][1]),
                     "shares": {AXES[j]: round(float(P[i][j]), 3) for j in range(4)},
                     "transfer_sensitivity": round(float(tsi[i]), 3),
                     "dominant_axis": AXES[int(np.argmax(clr(P[i])))],
                     "disposition": disposition(tsi[i])})
    rows.sort(key=lambda r: -r["transfer_sensitivity"])
    meanP = P.mean(0); meanP /= meanP.sum()
    C = np.array([clr(P[i]) for i in range(len(names))])
    s = np.linalg.svd(C - C.mean(0), compute_uv=False)
    ev = (s**2) / (s**2).sum(); eff_dim = float(np.exp(-(ev*np.log(ev+1e-12)).sum()))
    out = {
      "method": "Each application = a composition over 4 export/transfer-sensitivity axes; deterministic clr read + tsi = share(controlled_adj + strategic_weight).",
      "axes": AXES,
      "ranked": rows,
      "portfolio_mean_shares": {AXES[j]: round(float(meanP[j]), 3) for j in range(4)},
      "portfolio_effective_dimension_over_sensitivity": round(eff_dim, 2),
      "must_transfer_to_governance_tsi_ge_0.55": [r["app"] for r in rows if r["transfer_sensitivity"] >= 0.55],
      "publish_open_tsi_lt_0.42": [r["app"] for r in rows if r["transfer_sensitivity"] < 0.42],
      "honest_note": "Axis scores are judgment inputs (T3); the compositional read + ranking are deterministic. The PRINCIPLE of every app is publishable; only the APPLIED how-to of the high-tsi apps transfers to a governance steward."
    }
    out["content_sha256"] = hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest()
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
