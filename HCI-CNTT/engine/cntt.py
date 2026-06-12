"""CN-TT v4 — orchestrator (P1 kernel slice).
L1 ingest+treat (minimal) -> L2 geometry -> L3 atlas/reconstruct -> L4 emit+hash.
Full navigation-parity layer (helmsman, alpha, regime, k_eff, attractor) = P2."""
from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))
import numpy as np
import geometry as geo
import quaternion as quat
import atlas as atl
import provenance as prov

def cntt_run(rows, carriers=None, labels=None, atlas="hierarchical"):
    rows = np.asarray(rows, float)
    names = list(carriers) if carriers else None
    health = geo.carrier_health(rows)                          # E-21 carrier guard (admissibility triage)
    carrier_guard = None
    if health["structural_zero"] or health["constant"]:
        carrier_guard = {"excluded_structural_zero": [names[j] for j in health["structural_zero"]] if names else list(health["structural_zero"]),
                         "flagged_constant": [names[j] for j in health["constant"]] if names else list(health["constant"]),
                         "n_carriers_in": int(rows.shape[1]), "n_carriers_active": len(health["active"]),
                         "policy": "structural-zero carriers excluded (undefined under the log-ratio map); constant carriers retained, flagged."}
        if health["structural_zero"]:
            keep = health["active"]; rows = rows[:, keep]
            if names: names = [names[j] for j in keep]
    rows = geo.closure(rows)
    T, D = rows.shape
    H = geo.helmert_basis(D)
    clr_m = geo.clr(rows)
    if not np.isfinite(clr_m).all():                           # defense-in-depth: never propagate non-finite CLR
        raise ValueError("CN-TT E-21 guard: non-finite CLR after carrier guard — report as engine bug")
    ilr_m = clr_m @ H.T
    rad = geo.radial(ilr_m)

    charts = atl.hierarchical_atlas(D) if atlas == "hierarchical" else atl.sliding_window_atlas(D)
    edges = atl.edges_from_charts(charts)
    conn, ncomp = atl.is_connected(D, edges)
    recon_err = None
    if conn:
        recon_err = max(atl.reconstruct_clr(D, edges, rows[t])[1] for t in range(T))

    bearing = None
    if D == 4:
        units = ilr_m / np.maximum(np.linalg.norm(ilr_m, axis=1, keepdims=True), 1e-300)
        angs = [quat.angle_between(units[t-1], units[t]) for t in range(1, T)]
        bearing = {"native": True, "mean_step_angle_rad": float(np.mean(angs)) if angs else None}

    payload = {
        "metadata": {**prov.version_triple(),
                     "principle": "closure->CLR->Helmert ILR->D=4 quaternion charts->atlas reconstruction; deterministic, hash-chained.",
                     "atlas_strategy": atlas},
        "input": {"n_records": int(T), "n_carriers": int(D),
                  "carriers": list(names) if names else None},
        "geometry": {"radial_mean": float(rad.mean()), "radial_max": float(rad.max())},
        "atlas": {"strategy": atlas, "n_charts": len(charts), "n_edges": int(len(edges)),
                  "connected": bool(conn), "n_components": ncomp,
                  "reconstruction_max_err": recon_err,
                  "lossless": bool(conn and recon_err is not None and recon_err < 1e-6)},
        "bearing_d4": bearing,
        "diagnostics": {"claim_tier": "kernel(P1): geometry+atlas+quaternion exact; navigation-parity=P2"},
    }
    if carrier_guard is not None:                              # E-21: present only when carriers excluded/flagged (clean data -> identical payload+hash)
        payload["input"]["carrier_guard"] = carrier_guard
    payload["diagnostics"]["cntt_content_sha256"] = prov.canonical_sha256(payload)
    return payload
