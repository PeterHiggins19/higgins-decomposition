"""
HUF MC-4 packet operators — TV distance + K_eff.

These are the operational metrics from the submitted HUF MC-4 packet
(Part II, page 5). They sit alongside the CoDa-canonical Aitchison distance
and Shannon entropy that the published abstract names. Per the packet's
Appendix A metric-correction note, both stacks should be computed and the
side-by-side agreement on shock hit/miss verdicts is the headline robustness
result.

Definitions:
    TV(t)   = (1/2) * sum_i |rho_i(t) - rho_i(t-1)|     # half-L1 distance, bounded [0,1]
    K_eff(t) = exp( -sum_i rho_i(t) * ln(rho_i(t)) )    # effective number of categories

This module post-processes a CNT v3 JSON output, adding per-timestep:
    - coda_packet.tv_distance_step       (bounded [0,1])
    - coda_packet.k_eff                  (1 <= K_eff <= D, where D = n_carriers)
    - coda_packet.k_eff_yoy_change       (year-over-year absolute change in K_eff)
    - coda_packet.tv_acceleration        (d(TV)/dt approximated as central differences)

The block is named coda_packet so it does not collide with coda_standard.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List


def _tv_distance(comp_t: List[float], comp_prev: List[float]) -> float:
    """Half-L1 (Total Variation) distance between two closed compositions."""
    return 0.5 * sum(abs(a - b) for a, b in zip(comp_t, comp_prev))


def _k_eff(composition: List[float]) -> float:
    """Effective number of categories: exp(Shannon entropy)."""
    H = 0.0
    for r in composition:
        if r > 0:
            H -= r * math.log(r)
    return math.exp(H)


def augment_with_packet_operators(payload: Dict[str, Any]) -> Dict[str, Any]:
    """In-place augment a CNT v3 JSON payload with the HUF MC-4 packet operators.

    Adds a `coda_packet` block per timestep alongside the existing
    `coda_standard` block. Computed values are deterministic; same input
    composition gives same output values to IEEE precision.
    """
    timesteps = payload.get("tensor", {}).get("timesteps", [])
    if not timesteps:
        return payload

    # Compute TV distance + K_eff per timestep
    prev_comp: List[float] | None = None
    k_eff_series: List[float] = []

    for ts in timesteps:
        comp = ts.get("coda_standard", {}).get("composition")
        if comp is None:
            ts["coda_packet"] = None
            continue
        if not isinstance(comp, list):
            ts["coda_packet"] = None
            continue
        try:
            comp_f = [float(x) for x in comp]
        except (ValueError, TypeError):
            ts["coda_packet"] = None
            continue

        k = _k_eff(comp_f)
        k_eff_series.append(k)

        if prev_comp is None:
            tv = None  # no previous step
        else:
            tv = _tv_distance(comp_f, prev_comp)

        ts["coda_packet"] = {
            "tv_distance_step": tv,
            "k_eff": k,
            "k_eff_yoy_change": None,  # filled in pass 2
            "tv_acceleration": None,   # filled in pass 2
        }
        prev_comp = comp_f

    # Pass 2: year-over-year K_eff change and TV acceleration (central differences where possible)
    tv_series: List[float | None] = []
    for ts in timesteps:
        cp = ts.get("coda_packet")
        if cp is None:
            tv_series.append(None)
        else:
            tv_series.append(cp.get("tv_distance_step"))

    for i, ts in enumerate(timesteps):
        cp = ts.get("coda_packet")
        if cp is None:
            continue
        # YoY change in K_eff
        if i > 0 and k_eff_series and i - 1 < len(k_eff_series):
            cp["k_eff_yoy_change"] = k_eff_series[i] - k_eff_series[i - 1]
        # TV acceleration: simple forward difference (this step's TV minus previous step's TV)
        if i > 0 and tv_series[i] is not None and tv_series[i - 1] is not None:
            cp["tv_acceleration"] = tv_series[i] - tv_series[i - 1]

    # Series-level summary for the talk's depth bench
    valid_tv = [v for v in tv_series if v is not None]
    valid_k = k_eff_series
    payload.setdefault("packet_summary", {})
    payload["packet_summary"] = {
        "operators": "TV distance (half-L1) + K_eff (= exp Shannon H)",
        "source": "HUF MC-4 Packet v3, Part II page 5",
        "tv_distance_step": {
            "min": min(valid_tv) if valid_tv else None,
            "max": max(valid_tv) if valid_tv else None,
            "mean": sum(valid_tv) / len(valid_tv) if valid_tv else None,
            "n_steps": len(valid_tv),
        },
        "k_eff": {
            "min": min(valid_k) if valid_k else None,
            "max": max(valid_k) if valid_k else None,
            "mean": sum(valid_k) / len(valid_k) if valid_k else None,
            "final": valid_k[-1] if valid_k else None,
        },
        "robustness_note": (
            "TV distance and Aitchison distance agree on all shock hit/miss "
            "verdicts at the year-grain level (Appendix A of the HUF MC-4 "
            "packet). K_eff is the packet's concentration measure; "
            "exp(Shannon entropy on closed composition)."
        ),
    }
    return payload


if __name__ == "__main__":
    # Smoke test on one country
    import json
    from pathlib import Path
    p = Path(__file__).parent / "per_country" / "ember_deu" / "cnt_v3.json"
    if p.exists():
        d = json.loads(p.read_text(encoding="utf-8"))
        augment_with_packet_operators(d)
        print("DEU packet_summary:", json.dumps(d.get("packet_summary"), indent=2))
