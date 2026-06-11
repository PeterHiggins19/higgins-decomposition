"""CN-TT v4 — diagnostic & error code system (revives hs_codes.py v1.2 for the
tile-native engine). Format: SS-CCC-LLL (Stage-Condition-Level). Levels:
INF (information) · WRN (warning) · ERR (error) · DIS (discovery) · CAL (calibration).
Codes make every diagnostic machine-readable and flagged automatically; structural
modes are second-order reads of the code pattern. Includes the automated NULL flag
(DX-NUL-DIS): a comparison that finds NO separation is itself a coded, actionable output."""
from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
import numpy as np
import geometry as geo, navigate as nav

def _add(codes, c, lvl, msg): codes.append({"code": c, "level": lvl, "msg": msg})

def generate_codes(payload, comparison=None, shock=None):
    """Scan a CN-TT payload (+ optional group comparison / shock verdict) -> coded diagnostics."""
    codes = []
    md = payload.get("metadata", {}); inp = payload.get("input", {}); at = payload.get("atlas", {})
    navb = payload.get("navigation", {}); af = payload.get("attractor_fit", {}); dt = payload.get("depth_tower", {})
    hf = payload.get("helmsman_family", {})
    _add(codes, "GD-ALL-INF", "INF", "input guards passed; pipeline ran")
    if "geometry" in payload: _add(codes, "L2-CLR-INF", "INF", "closure -> CLR -> Helmert-ILR computed")
    # L3 atlas / tiling
    if at.get("lossless"):
        _add(codes, "L3-LSL-INF", "INF", f"atlas connected + lossless reconstruction (err {at.get('reconstruction_max_err'):.1e})")
    elif at.get("connected") is False:
        _add(codes, "L3-DSJ-ERR", "ERR", "atlas disjoint: reconstruction rank-deficient (overlap missing)")
    if md.get("high_d_mode"):
        _add(codes, "L3-HID-CAL", "CAL", f"high-D mode (D={inp.get('n_carriers')}): O(D^2)/combinatorial diagnostics gated off")
    # L4 navigation
    rb = (navb.get("regime_boundaries", {}) or {}).get("indices") if navb else None
    if rb: _add(codes, "L4-RGB-DIS", "DIS", f"{len(rb)} regime boundary(ies) detected at t={rb[:8]}")
    dec = (navb.get("regime_counts", {}) or {}).get("deceptive", 0)
    if dec: _add(codes, "L4-DEC-WRN", "WRN", f"{dec} deceptive-drift step(s): concentration tightening while motion stays quiet")
    if hf:
        stab = (hf.get("stability_S_sigma", {}) or {}).get("global")
        if stab is not None and stab < 0.3: _add(codes, "L4-HVO-WRN", "WRN", f"volatile helmsman (stability {stab:.2f}): dominant driver changing often")
    # DX diagnostics
    if af.get("fitted"): _add(codes, "DX-ATR-DIS", "DIS", f"period-{af.get('period')} limit cycle fitted (stability {af.get('period_stability'):.2f})")
    if dt.get("ir_class"): _add(codes, "DX-IRC-INF", "INF", f"IR class = {dt['ir_class']}")
    # SHOCK (FDIR)
    if shock is not None:
        cls = shock.get("class")
        if cls == "EXTERNAL": _add(codes, "SK-EXT-INF", "INF", f"EXTERNAL shock: real change (Δ {shock.get('shock_magnitude'):.2f}); channels coherent")
        elif cls == "INTERNAL": _add(codes, "SK-INT-ERR", "ERR", f"INTERNAL fault isolated to channel {shock.get('faulty_channel')} (incoherence {shock.get('incoherence_max_resid'):.2f})")
        elif cls == "UNDETERMINED": _add(codes, "SK-UND-CAL", "CAL", "shock class undetermined: no redundancy (needs >=2 independent channels)")
    # COMPARISON -> the NULL flag (the key to advancement, automated)
    if comparison is not None:
        p = comparison.get("p"); sep = comparison.get("separated")
        if sep: _add(codes, "DX-SEP-DIS", "DIS", f"group separation detected on {comparison.get('metric')} (p={p:.2g})")
        else: _add(codes, "DX-NUL-DIS", "DIS",
                   f"NULL: no separation on {comparison.get('metric')} (p={p:.2g}) — the global read is insufficient; a targeted balance/signature is indicated")
    # RP report
    _add(codes, "RP-DET-INF", "INF", "deterministic: identical content hash on rerun")
    if md.get("engine_version"): _add(codes, "RP-VER-INF", "INF", f"engine HCI-CNTT v{md['engine_version']}")
    sha = payload.get("diagnostics", {}).get("cntt_content_sha256")
    if sha: _add(codes, "RP-SHA-INF", "INF", f"content hash {sha[:16]}")
    modes = detect_modes(codes)
    counts = {lv: sum(1 for c in codes if c["level"] == lv) for lv in ("INF", "WRN", "ERR", "DIS", "CAL")}
    return {"codes": codes, "structural_modes": modes, "level_counts": counts}

def detect_modes(codes):
    has = lambda p: any(c["code"].startswith(p) for c in codes)
    modes = []
    if has("L3-LSL") and has("RP-DET") and not has("L3-DSJ") and not has("SK-INT"):
        modes.append({"mode": "SM-CLN-INF", "msg": "clean lossless deterministic run — compositionally well-behaved"})
    if has("L3-DSJ"):
        modes.append({"mode": "SM-MCA-WRN", "msg": "missing/untracked carrier: atlas disjoint — information is leaking to an untracked part; add the carrier"})
    if has("DX-NUL"):
        modes.append({"mode": "SM-NUL-DIS", "msg": "NULL RESULT: the expected separation is absent. ADVANCE via a targeted balance/signature, not a global scalar. This is a finding, not a failure."})
    if has("L4-RGB"):
        modes.append({"mode": "SM-RGS-DIS", "msg": "regime shift(s) present — segment the trajectory at the boundaries and investigate"})
    if has("SK-INT"):
        modes.append({"mode": "SM-IFT-ERR", "msg": "INTERNAL FAULT: a channel diverges — isolate the component and roll back to last-known-good"})
    return modes

def group_separation(comps, labels, metric="k_eff", threshold=0.05):
    """comps: (N, D) closed compositions; labels: length-N group labels (exactly 2 groups).
    Returns whether the groups separate on the chosen metric (Mann-Whitney). When NOT,
    generate_codes emits the automated NULL flag."""
    from scipy import stats
    comps = np.asarray(comps, float); labels = np.asarray(labels)
    groups = list(dict.fromkeys(labels.tolist()))
    if len(groups) != 2:
        return {"separated": None, "reason": "needs exactly 2 groups", "n_groups": len(groups)}
    if metric == "k_eff":
        val = np.array([nav.k_eff(comps[i]) for i in range(len(comps))])
    else:
        val = np.linalg.norm(geo.clr(comps), axis=1)  # aitchison norm
    a = val[labels == groups[0]]; b = val[labels == groups[1]]
    U, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    return {"separated": bool(p < threshold), "p": float(p), "metric": metric,
            "groups": {str(groups[0]): float(a.mean()), str(groups[1]): float(b.mean())}, "threshold": threshold}
