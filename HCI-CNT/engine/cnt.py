#!/usr/bin/env python3
"""
CNT Engine — Single-Program Canonical JSON Generator
=====================================================

Schema version : 2.0.0    (see CNT_JSON_SCHEMA.md for the contract)
Engine version : 2.0.0
Algorithm ref  : CNT_PSEUDOCODE.md

v2.0.0 structural change: every analytic block (tensor, stages, bridges,
depth, diagnostics) is split into coda_standard / higgins_extensions
sub-blocks, with _function ∈ {composer, review, formatter, provenance}
and _description meta fields per schema §2-§7. Math is unchanged from
1.0.0; only the JSON layout differs.

This single program ingests a compositional CSV and emits ONE canonical
JSON conforming to the CNT JSON schema. The JSON is the authoritative
data store; downstream tools (plates, projector, future viewers) read
it without computing anything.

Mathematical lineage:
  Aitchison (1986) — CLR transform, simplex geometry
  Egozcue (2003)   — ILR, Helmert basis, orthonormal coordinates
  Shannon (1948)   — Entropy
  Higgins (2026)   — CNT tensor decomposition, recursive depth sounder

Usage:
    python cnt.py input.csv [--output OUT.json] [--ordering OPT]

The instrument reads. The expert decides. The loop stays open.
"""

from __future__ import annotations
import sys, os, json, csv, math, hashlib, time, platform, subprocess, argparse
from datetime import datetime, timezone
from itertools import combinations
from typing import Optional, Any

import numpy as np

# ════════════════════════════════════════════════════════════════
# USER CONFIGURATION
# ════════════════════════════════════════════════════════════════
#
# These values control the engine's behaviour. Edit them to suit
# your dataset and analytical needs. The active values are echoed
# in `metadata.engine_config` of every JSON the engine produces so
# the run is self-documenting.
#
# Two consecutive runs of the engine with IDENTICAL configuration
# on IDENTICAL input produce IDENTICAL `diagnostics.content_sha256`
# (verified). Two runs with DIFFERENT configuration produce
# different content_sha256 — that is correct and expected: the
# hash reflects every setting that affects output.
#
# Categories below: VERSION, ZERO REPLACEMENT, LOCK EVENTS,
# DEPTH RECURSION, TRIADIC ENUMERATION, EITT BENCH-TEST.
# ════════════════════════════════════════════════════════════════

# ── VERSION (do not edit unless modifying the engine) ─────────────
SCHEMA_VERSION = "2.1.0"        # 2.1.0: additive — metadata.input_units / higgins_scale_units / units_scale_factor_to_neper
ENGINE_VERSION = "2.0.4"        # 2.0.4: engine_config_overrides honoured; units block written
ENGINE_NAME    = "cnt"

# ── ZERO REPLACEMENT ─────────────────────────────────────────────
# When an input value is zero or below this floor, the engine
# replaces it with `DEFAULT_DELTA` so log-ratios remain finite.
# Lower values preserve more dynamic range; higher values smooth
# out boundary effects.
#
#   Default 1e-15 — at the IEEE 754 double-precision floor.
#   Practical alternatives: 1e-10 (less aggressive), 1e-6 (smoothing).
DEFAULT_DELTA = 1e-15

# ── LOCK EVENT THRESHOLDS ────────────────────────────────────────
# Boundary-marker thresholds for `diagnostics.lock_events`. Lock
# events ride through downstream display tools as DEGEN diamond /
# LOCK-ACQ green ring / LOCK-LOSS amber ring.
#
#   DEGEN_THRESHOLD: composition is "near barycenter / collapsed"
#     when max(CLR) - min(CLR) is below this. Default 1e-4.
#   LOCK_CLR_THRESHOLD: a carrier is "locked low" (approaching zero)
#     when its CLR value is below this. Default -10.0.
#     Less negative (e.g. -8) flags more carriers; more negative
#     (e.g. -15) flags only extreme zeros.
DEGEN_THRESHOLD     = 1e-4
LOCK_CLR_THRESHOLD  = -10.0

# ── DEPTH RECURSION (depth sounder) ──────────────────────────────
# Controls the curvature/energy tower iteration in `depth/`.
#
#   DEPTH_MAX_LEVELS: hard cap on tower length. The engine stops
#     at this level even if convergence hasn't been reached.
#     Larger = potentially deeper exploration; default 50 covers
#     all known compositional systems.
#   DEPTH_PRECISION_TARGET: relative precision for period detection.
#     A period-1 fixed point requires TWO consecutive level pairs
#     under this gate; a period-2 limit cycle requires both
#     same-parity sequences under this gate. Default 0.01 (1%).
#     Tighter (e.g. 0.001) → longer towers; looser → faster, less
#     reliable.
#   NOISE_FLOOR_OMEGA_VAR: angular-velocity variance below this
#     declares OMEGA_FLAT termination (signal exhausted). Default
#     1e-6. Raise to terminate earlier; lower to push deeper.
DEPTH_MAX_LEVELS         = 50
DEPTH_PRECISION_TARGET   = 0.01
NOISE_FLOOR_OMEGA_VAR    = 1e-6

# ── TRIADIC ENUMERATION (Stage 3 day-triad area) ─────────────────
# Stage 3 enumerates C(T, 3) day-triads to find the largest metric
# triangles in CLR space. This is O(T³) — at T=731 it's 65 M
# candidates and ~5 minutes of compute.
#
#   TRIADIC_T_LIMIT: above this T, the engine SKIPS the enumeration
#     and emits `selection_method: "none_T_too_large"`. The
#     underlying CLR vectors are still in `tensor.timesteps[]` so
#     a viewer can compute on demand. Default 500.
#     - Raise to 1000+ for full enumeration on T<=1000 (slower).
#     - Lower to 200 if you only ever want fast Stage 3.
#   TRIADIC_K_DEFAULT: when enumeration runs, store this many
#     top-area triads in `results[]`. Default 500.
TRIADIC_T_LIMIT     = 500
TRIADIC_K_DEFAULT   = 500

# ── EITT BENCH-TEST (diagnostics.eitt_residuals) ─────────────────
# Empirical observation of trajectory smoothness under temporal
# decimation. NOT a CoDa-geometric theorem (per Egozcue 2026
# correspondence) — recorded as such in the JSON note.
#
#   EITT_GATE_PCT: variation_pct above this is FAIL. Default 5.0
#     (the canonical Math Handbook value). Tightening to 2.0 makes
#     a stricter gate; loosening to 10.0 is more permissive.
#   EITT_M_SWEEP_BASE: which compression ratios M to bench-test.
#     The engine adds ⌈T/101⌉ on top of these for high-T datasets.
EITT_GATE_PCT       = 5.0
EITT_M_SWEEP_BASE   = [2, 4, 8, 16, 32, 64, 128]

# ── NATIVE UNITS (v1.1 — reserved, not wired in v1.0) ────────────
# When wired (v1.1), these declare the natural unit of the input
# data and the unit in which the Higgins scale is reported. The
# display layout is unchanged; only the project-card annotation
# and metadata.units_* fields are affected.
#
#   INPUT_UNITS options:
#     "ratio" (default), "neper", "nat", "bit",
#     "dB_power", "dB_amplitude", "%", "absolute"
#   HIGGINS_SCALE_UNITS:
#     "auto"  — picks "neper" for ratio/neper/nat,
#               "bit" for bit, "dB" for dB_*
#     or explicit: "neper", "bit", "ratio"
#   REPORT_UNITS_SCALE_FACTORS:
#     If True, the cover banner declares the conversion factor
#     (e.g. "1 dB_power = 0.2303 nepers; Hs reported in nepers").
#
#   See atlas/V1.1_FEATURE_MENU.md for the full design.
INPUT_UNITS                = "ratio"
HIGGINS_SCALE_UNITS        = "auto"
REPORT_UNITS_SCALE_FACTORS = True

# ════════════════════════════════════════════════════════════════
# End USER CONFIGURATION. Edit above; do not edit below.
# ════════════════════════════════════════════════════════════════

# ════════════════════════════════════════════════════════════════
# §0 — Math primitives
# ════════════════════════════════════════════════════════════════

def close(x: list[float], delta: float = DEFAULT_DELTA) -> list[float]:
    """Close a positive vector to the unit simplex."""
    x_pos = [max(float(v), delta) for v in x]
    s = sum(x_pos)
    if s <= 0:
        raise ValueError("Composition has non-positive sum")
    return [v / s for v in x_pos]


def clr(x: list[float]) -> list[float]:
    """Centred log-ratio: clr(x)_j = ln(x_j) - mean(ln x)."""
    log_x = [math.log(v) for v in x]
    mean_log = sum(log_x) / len(x)
    return [lx - mean_log for lx in log_x]


def helmert_basis(D: int) -> np.ndarray:
    """Helmert orthonormal basis, (D-1) x D. Egozcue 2003 Sec 3."""
    basis = np.zeros((D - 1, D))
    for k in range(1, D):
        scale = math.sqrt(k / (k + 1.0))
        for j in range(k):
            basis[k - 1, j] = scale / k
        basis[k - 1, k] = -scale
    return basis


def ilr_project(h: list[float], basis: np.ndarray) -> list[float]:
    """ILR projection from CLR vector."""
    return (basis @ np.array(h)).tolist()


def aitchison_distance(x: list[float], y: list[float]) -> float:
    """d_A(x,y) = ||clr(x) - clr(y)||."""
    h = np.array(clr(x)) - np.array(clr(y))
    return float(np.linalg.norm(h))


def aitchison_barycenter(rows: list[list[float]]) -> list[float]:
    """Geometric mean of N positive D-vectors, re-closed."""
    if not rows:
        return None
    D = len(rows[0])
    log_means = [
        sum(math.log(r[j]) for r in rows) / len(rows) for j in range(D)
    ]
    g = [math.exp(lm) for lm in log_means]
    return close(g)


def shannon_entropy(x: list[float]) -> float:
    """H(x) = -sum x_j ln x_j. NOT scale-invariant — empirical use only."""
    return -sum(v * math.log(v) for v in x if v > 0)


def higgins_scale(x: list[float]) -> float:
    """Hs = 1 - H/ln(D). HUF-specific empirical scalar in [0, 1]."""
    H = shannon_entropy(x)
    return 1.0 - H / math.log(len(x))


def metric_dual(x: list[float]) -> list[float]:
    """M(x)_j = (1/x_j) / sum(1/x_k). M^2 = identity (involution)."""
    return close([1.0 / v for v in x])


def metric_tensor_full(x: list[float]) -> np.ndarray:
    """Higgins steering metric tensor, full D x D matrix.

    kappa_ij(x) = (delta_ij - 1/D) / (x_i * x_j)
    """
    D = len(x)
    K = np.zeros((D, D))
    for i in range(D):
        for j in range(D):
            num = (1.0 - 1.0 / D) if i == j else (-1.0 / D)
            K[i, j] = num / (x[i] * x[j])
    return K


def bearing_pairs(h: list[float], carriers: list[str]) -> list[dict]:
    """All D(D-1)/2 pairwise bearings theta_ij = atan2(h_j, h_i) in degrees."""
    D = len(h)
    out = []
    for i in range(D):
        for j in range(i + 1, D):
            theta_rad = math.atan2(h[j], h[i])
            out.append({
                "carrier_i":     carriers[i],
                "carrier_j":     carriers[j],
                "theta_deg":     math.degrees(theta_rad),
            })
    return out


def angular_velocity_deg(h_prev: list[float], h: list[float]) -> float:
    """omega = atan2(||h_prev x h||, <h_prev, h>) in degrees, via Lagrange identity."""
    a = np.array(h_prev); b = np.array(h)
    a_sq = float(a @ a); b_sq = float(b @ b); ab = float(a @ b)
    cross_sq = max(0.0, a_sq * b_sq - ab * ab)
    return math.degrees(math.atan2(math.sqrt(cross_sq), ab))


def helmsman_dcdi(h_prev: list[float], h: list[float],
                   carriers: list[str]) -> tuple[str, float]:
    """argmax_j |h_j - h_prev_j| — DCDI / Helmsman index."""
    deltas = [abs(h[j] - h_prev[j]) for j in range(len(h))]
    j_max = max(range(len(h)), key=lambda j: deltas[j])
    return carriers[j_max], deltas[j_max]


# ════════════════════════════════════════════════════════════════
# §1 — Tensor block
# ════════════════════════════════════════════════════════════════

def compute_tensor_block(records: list[dict],
                          carriers: list[str]) -> dict:
    """Per-record tensor channels (flat internal representation).

    Returns a flat dict; the v2.0.0 schema split into coda_standard /
    higgins_extensions is applied at output assembly time by
    `_format_tensor_block_v2`. This keeps the compute pipeline simple
    and lets every downstream compute_* function read flat fields.
    """
    D = len(carriers)
    basis = helmert_basis(D)
    timesteps = []
    h_prev = None

    for i, rec in enumerate(records):
        x_raw = rec["raw_values"]
        x = close(x_raw)
        h = clr(x)
        ilr_v = ilr_project(h, basis)
        H = shannon_entropy(x)
        Hs = 1.0 - H / math.log(D)
        K_full = metric_tensor_full(x)

        ts = {
            "index":                  i,
            "label":                  rec["label"],
            "raw_values":             list(x_raw),
            "composition":            x,
            "clr":                    h,
            "ilr":                    ilr_v,
            "shannon_entropy":        H,
            "higgins_scale":          Hs,
            "aitchison_norm":         float(np.linalg.norm(h)),
            "bearing_tensor":         {"pairs": bearing_pairs(h, carriers)},
            "metric_tensor":          {
                "matrix":      K_full.tolist(),
                "eigenvalues": sorted(np.linalg.eigvalsh(K_full).tolist()),
                "trace":       float(np.trace(K_full)),
            },
            "metric_tensor_diagonal": [(1.0 - 1.0 / D) / (v * v) for v in x],
            "condition_number":       max(x) / min(x),
        }
        if h_prev is not None:
            ts["angular_velocity_deg"]    = angular_velocity_deg(h_prev, h)
            ts["aitchison_distance_step"] = float(np.linalg.norm(np.array(h) - np.array(h_prev)))
            hm_carrier, hm_delta = helmsman_dcdi(h_prev, h, carriers)
            ts["helmsman"]                = hm_carrier
            ts["helmsman_delta"]          = hm_delta

        timesteps.append(ts)
        h_prev = h

    return {
        "helmert_basis": {
            "D":            D,
            "dim":          D - 1,
            "coefficients": basis.tolist(),
        },
        "timesteps": timesteps,
    }


# ════════════════════════════════════════════════════════════════
# §2 — Stages block
# ════════════════════════════════════════════════════════════════

def ring_classify(hs: float) -> str:
    """Hs ring zones for the metric ledger."""
    if hs < 0.1:   return "Hs-1"
    if hs < 0.3:   return "Hs-2"
    if hs < 0.5:   return "Hs-3"
    if hs < 0.7:   return "Hs-4"
    if hs < 0.9:   return "Hs-5"
    return "Hs-6"


def compute_stage1(tensor_block: dict, carriers: list[str]) -> dict:
    """Section atlas + metric ledger."""
    section_atlas, metric_ledger = [], []
    D = len(carriers)
    for ts in tensor_block["timesteps"]:
        h = ts["clr"]
        # Cube faces: first three CLR components (or all if D < 3)
        xy = h[:2] if D >= 2 else [h[0], 0.0]
        xz = [h[0], h[2]] if D >= 3 else [h[0], 0.0]
        yz = h[1:3] if D >= 3 else [h[1] if D >= 2 else 0, 0.0]
        section_atlas.append({
            "index":               ts["index"],
            "label":               ts["label"],
            "xy_face":             xy,
            "xz_face":             xz,
            "yz_face":             yz,
            "metric_tensor_trace": ts["metric_tensor"]["trace"],
            "condition_number":    ts["condition_number"],
            "angular_velocity_deg":ts.get("angular_velocity_deg", 0.0),
        })
        metric_ledger.append({
            "index":     ts["index"],
            "label":     ts["label"],
            "hs":        ts["higgins_scale"],
            "ring":      ring_classify(ts["higgins_scale"]),
            "omega_deg": ts.get("angular_velocity_deg", 0.0),
            "helmsman":  ts.get("helmsman", ""),
            "energy":    ts["aitchison_norm"] ** 2,
            "condition": ts["condition_number"],
        })
    return {"section_atlas": section_atlas, "metric_ledger": metric_ledger}


def variation_matrix(records_closed: list[list[float]]) -> list[list[float]]:
    """CoDa standard tau_ij = var(ln(x_i / x_j)). Symmetric, diagonal zero."""
    D = len(records_closed[0])
    tau = np.zeros((D, D))
    for i in range(D):
        for j in range(D):
            if i == j:
                continue
            ratios = [math.log(r[i] / r[j]) for r in records_closed]
            mean_r = sum(ratios) / len(ratios)
            tau[i, j] = sum((r - mean_r) ** 2 for r in ratios) / len(ratios)
    return tau.tolist()


def compute_stage2(records_closed: list[list[float]],
                   tensor_block: dict,
                   carriers: list[str]) -> dict:
    """Variation matrix + carrier-pair examination."""
    D = len(carriers)
    T = len(tensor_block["timesteps"])

    var_mat = variation_matrix(records_closed)

    pair_results = []
    for i, j in combinations(range(D), 2):
        h_i = [ts["clr"][i] for ts in tensor_block["timesteps"]]
        h_j = [ts["clr"][j] for ts in tensor_block["timesteps"]]
        if T >= 2:
            mean_i = sum(h_i) / T; mean_j = sum(h_j) / T
            num = sum((h_i[t] - mean_i) * (h_j[t] - mean_j) for t in range(T))
            den_i = math.sqrt(sum((v - mean_i) ** 2 for v in h_i))
            den_j = math.sqrt(sum((v - mean_j) ** 2 for v in h_j))
            r = num / (den_i * den_j) if den_i > 0 and den_j > 0 else 0.0
        else:
            r = 0.0
        # Bearing variation across timesteps
        bearings = [
            math.degrees(math.atan2(h_j[t], h_i[t])) for t in range(T)
        ]
        bearing_spread = max(bearings) - min(bearings) if bearings else 0.0
        pair_results.append({
            "carrier_a":         carriers[i],
            "carrier_b":         carriers[j],
            "i":                 i,
            "j":                 j,
            "pearson_r":         r,
            "co_movement_score": max(0, r),
            "opposition_score":  max(0, -r),
            "bearing_spread_deg":bearing_spread,
            "locked":            bearing_spread < 10.0,
        })

    return {
        "variation_matrix":          var_mat,
        "carrier_pair_examination":  pair_results,
    }


def compute_stage3(records_closed: list[list[float]],
                   tensor_block: dict,
                   carriers: list[str]) -> dict:
    """Subcompositional ladder + carrier triads + capped triadic-area + regimes."""
    D = len(carriers)
    T = len(tensor_block["timesteps"])

    # Subcompositional ladder: degree-k subsets
    ladder = []
    for k in range(2, D):
        subsets = list(combinations(range(D), k))
        # mean correlation among the parts in each subset
        mean_corrs = []
        for s in subsets[:200]:  # cap for combinatorial blowup
            if len(s) < 2:
                continue
            local_corrs = []
            for ii, jj in combinations(s, 2):
                hi = [ts["clr"][ii] for ts in tensor_block["timesteps"]]
                hj = [ts["clr"][jj] for ts in tensor_block["timesteps"]]
                if T < 2:
                    continue
                mi = sum(hi) / T; mj = sum(hj) / T
                num = sum((hi[t] - mi) * (hj[t] - mj) for t in range(T))
                di = math.sqrt(sum((v - mi) ** 2 for v in hi))
                dj = math.sqrt(sum((v - mj) ** 2 for v in hj))
                if di > 0 and dj > 0:
                    local_corrs.append(num / (di * dj))
            if local_corrs:
                mean_corrs.append(sum(local_corrs) / len(local_corrs))
        ladder.append({
            "degree":           k,
            "n_subsets":        len(subsets),
            "n_subsets_scored": len(mean_corrs),
            "mean_correlation": sum(mean_corrs) / len(mean_corrs) if mean_corrs else 0.0,
        })

    # Carrier triads
    carrier_triads = []
    for i, j, k in combinations(range(D), 3):
        carrier_triads.append({
            "carriers": [carriers[i], carriers[j], carriers[k]],
            "indices":  [i, j, k],
        })

    # Triadic area — capped
    triadic = {"n_candidates": int(T * (T - 1) * (T - 2) / 6) if T >= 3 else 0}
    if T < 3:
        triadic.update({
            "selection_method": "none_T_too_small",
            "n_returned":       0,
            "results":          [],
        })
    elif T > TRIADIC_T_LIMIT:
        triadic.update({
            "selection_method": "none_T_too_large",
            "selection_K":      0,
            "n_returned":       0,
            "results":          [],
        })
    else:
        results = []
        clrs = [ts["clr"] for ts in tensor_block["timesteps"]]
        for a, b, c in combinations(range(T), 3):
            ba = np.array(clrs[a]); bb = np.array(clrs[b]); bc = np.array(clrs[c])
            sab = float(np.linalg.norm(ba - bb))
            sbc = float(np.linalg.norm(bb - bc))
            sca = float(np.linalg.norm(bc - ba))
            sp = (sab + sbc + sca) / 2
            area_sq = sp * (sp - sab) * (sp - sbc) * (sp - sca)
            area = math.sqrt(max(0.0, area_sq))
            results.append({
                "triad":   [a, b, c],
                "area":    area,
                "sides":   [sab, sbc, sca],
            })
        results.sort(key=lambda r: -r["area"])
        triadic.update({
            "selection_method": "top_K_by_area",
            "selection_K":      TRIADIC_K_DEFAULT,
            "n_returned":       min(TRIADIC_K_DEFAULT, len(results)),
            "results":          results[:TRIADIC_K_DEFAULT],
        })

    # Regime detection: boundaries where step Aitchison distance exceeds mean + 2 std
    boundaries = []
    if T >= 5:
        steps = [ts.get("aitchison_distance_step", 0.0)
                 for ts in tensor_block["timesteps"][1:]]
        mean_s = sum(steps) / len(steps)
        var_s = sum((s - mean_s) ** 2 for s in steps) / len(steps)
        std_s = math.sqrt(var_s)
        threshold = mean_s + 2 * std_s
        for idx, s in enumerate(steps, start=1):
            if s > threshold:
                boundaries.append({
                    "timestep_index": idx,
                    "label":          tensor_block["timesteps"][idx]["label"],
                    "step_distance":  s,
                    "z_score":        (s - mean_s) / std_s if std_s > 0 else 0.0,
                })

    regimes = {
        "n_regimes":   len(boundaries) + 1,
        "boundaries":  boundaries,
        "method":      "step_distance > mean + 2*std",
    }

    return {
        "triadic_area":            triadic,
        "carrier_triads":          carrier_triads,
        "subcomposition_ladder":   ladder,
        "regime_detection":        regimes,
    }


# ════════════════════════════════════════════════════════════════
# §3 — Bridges block
# ════════════════════════════════════════════════════════════════

def per_carrier_lyapunov(tensor_block: dict, carriers: list[str]) -> list[dict]:
    """Per-carrier Lyapunov exponent — sensitivity along each carrier axis.

    Distinct from the contraction Lyapunov in depth/curvature_attractor.
    Uses 1D divergence rate of the CLR series for each carrier.
    """
    D = len(carriers)
    T = len(tensor_block["timesteps"])
    out = []
    for j in range(D):
        h_series = [ts["clr"][j] for ts in tensor_block["timesteps"]]
        # Mean log-divergence rate of consecutive differences (heuristic)
        if T >= 3:
            diffs = [abs(h_series[t + 1] - h_series[t]) for t in range(T - 1)]
            valid = [d for d in diffs if d > 1e-15]
            if len(valid) >= 2:
                ratios = [valid[t + 1] / valid[t] for t in range(len(valid) - 1)
                          if valid[t] > 0]
                if ratios:
                    log_ratios = [math.log(r) for r in ratios if r > 0]
                    lyap = sum(log_ratios) / len(log_ratios) if log_ratios else 0.0
                else:
                    lyap = 0.0
            else:
                lyap = 0.0
        else:
            lyap = 0.0
        if lyap > 0.05:    classification = "DIVERGENT"
        elif lyap < -0.05: classification = "CONVERGENT"
        else:               classification = "NEUTRAL"
        out.append({
            "carrier":            carriers[j],
            "index":              j,
            "lyapunov_exponent":  lyap,
            "classification":     classification,
        })
    return out


def compute_bridges(records_closed: list[list[float]],
                    tensor_block: dict,
                    carriers: list[str]) -> dict:
    """Dynamical / control / information-theoretic bridges."""
    D = len(carriers)
    T = len(tensor_block["timesteps"])

    # Dynamical systems
    per_carrier_lyap = per_carrier_lyapunov(tensor_block, carriers)
    velocity_field = {
        "mean_omega_deg":  sum(ts.get("angular_velocity_deg", 0.0)
                              for ts in tensor_block["timesteps"]) / max(1, T),
        "max_omega_deg":   max((ts.get("angular_velocity_deg", 0.0)
                                for ts in tensor_block["timesteps"]), default=0.0),
    }
    # Recurrence rate: fraction of pairs (a, b) with d_A < threshold
    if T >= 2:
        clrs = [ts["clr"] for ts in tensor_block["timesteps"]]
        d_A_max = 0.0
        for a in range(T):
            for b in range(a + 1, T):
                d = float(np.linalg.norm(np.array(clrs[a]) - np.array(clrs[b])))
                if d > d_A_max: d_A_max = d
        threshold = 0.1 * d_A_max
        recurrent = 0; total_pairs = 0
        for a in range(T):
            for b in range(a + 1, T):
                d = float(np.linalg.norm(np.array(clrs[a]) - np.array(clrs[b])))
                if d < threshold:
                    recurrent += 1
                total_pairs += 1
        recurrence_rate = recurrent / total_pairs if total_pairs > 0 else 0.0
    else:
        recurrence_rate = 0.0

    dynamical = {
        "per_carrier_lyapunov":  per_carrier_lyap,
        "velocity_field":        velocity_field,
        "recurrence_analysis":   {
            "recurrence_rate":   recurrence_rate,
            "threshold_pct":     0.1,
        },
    }

    # Control theory: simple AR(1) state-space fit on CLR series
    if T >= 2:
        clr_mat = np.array([ts["clr"] for ts in tensor_block["timesteps"]])
        X = clr_mat[:-1]; Y = clr_mat[1:]
        try:
            A_mat, residuals, rank, _ = np.linalg.lstsq(X, Y, rcond=None)
            A_mat = A_mat.T
            preds = X @ A_mat.T
            resid = Y - preds
            mean_resid = float(np.mean(np.abs(resid)))
            spec_radius = float(max(abs(np.linalg.eigvals(A_mat))))
        except np.linalg.LinAlgError:
            A_mat = np.eye(D); mean_resid = 0.0; spec_radius = 1.0
    else:
        A_mat = np.eye(D); mean_resid = 0.0; spec_radius = 1.0

    observability_list = [
        {
            "carrier":            carriers[j],
            "index":              j,
            "clr_variance":       float(np.var([ts["clr"][j]
                                                  for ts in tensor_block["timesteps"]])),
        }
        for j in range(D)
    ]

    control = {
        "state_space_model": {
            "A_matrix":         A_mat.tolist(),
            "spectral_radius":  spec_radius,
            "stable":           spec_radius < 1.0,
            "mean_residual":    mean_resid,
            "model":            "AR(1) on CLR series",
        },
        "observability":     observability_list,
    }

    # Information theory
    entropy_series = [
        {
            "label":              ts["label"],
            "shannon_entropy":    ts["shannon_entropy"],
            "max_entropy":        math.log(D),
            "normalised_entropy": ts["shannon_entropy"] / math.log(D),
            "higgins_scale":      ts["higgins_scale"],
        }
        for ts in tensor_block["timesteps"]
    ]

    # Mutual information — via bin counts on CLR pairs (coarse)
    mi_pairs = []
    if T >= 4:
        clrs = [ts["clr"] for ts in tensor_block["timesteps"]]
        for i, j in combinations(range(D), 2):
            xi = [c[i] for c in clrs]; xj = [c[j] for c in clrs]
            mi = mutual_information_1d(xi, xj)
            mi_pairs.append({
                "carrier_a": carriers[i],
                "carrier_b": carriers[j],
                "mi":        mi,
            })
    mi_pairs.sort(key=lambda r: -r["mi"])

    info = {
        "entropy_series":    entropy_series,
        "fisher_information": {
            "method": "1/var(clr)",
            "values": [
                {"carrier": carriers[j],
                 "fisher": (1.0 / max(1e-15, float(np.var([ts["clr"][j]
                                                            for ts in tensor_block["timesteps"]]))))}
                for j in range(D)
            ],
        },
        "kl_divergence":     {
            "adjacent_pairs": adjacent_kl(records_closed),
        },
        "mutual_information":{
            "top_pairs":      mi_pairs[:10],
        },
        "entropy_rate":      {
            "value":          entropy_rate(records_closed),
            "method":         "mean of d/dt H along trajectory",
        },
    }

    return {
        "dynamical_systems":   dynamical,
        "control_theory":      control,
        "information_theory":  info,
    }


def mutual_information_1d(x: list[float], y: list[float], bins: int = 8) -> float:
    """Coarse MI between two real-valued series via histogram binning."""
    if len(x) < 4: return 0.0
    x = np.array(x); y = np.array(y)
    H, _, _ = np.histogram2d(x, y, bins=bins)
    H = H / H.sum()
    px = H.sum(axis=1)
    py = H.sum(axis=0)
    mi = 0.0
    for i in range(H.shape[0]):
        for j in range(H.shape[1]):
            if H[i, j] > 0 and px[i] > 0 and py[j] > 0:
                mi += H[i, j] * math.log(H[i, j] / (px[i] * py[j]))
    return float(mi)


def adjacent_kl(records_closed: list[list[float]]) -> dict:
    """Mean and max KL divergence between adjacent records."""
    if len(records_closed) < 2:
        return {"mean": 0.0, "max": 0.0, "max_index": -1}
    kls = []
    for t in range(1, len(records_closed)):
        x = records_closed[t]; y = records_closed[t - 1]
        kl = sum(x[j] * math.log(x[j] / y[j]) for j in range(len(x)) if x[j] > 0 and y[j] > 0)
        kls.append(kl)
    max_idx = max(range(len(kls)), key=lambda i: kls[i])
    return {
        "mean": sum(kls) / len(kls),
        "max":  kls[max_idx],
        "max_index": max_idx + 1,
    }


def entropy_rate(records_closed: list[list[float]]) -> float:
    """Mean step-rate of Shannon entropy change."""
    if len(records_closed) < 2: return 0.0
    Hs = [shannon_entropy(r) for r in records_closed]
    return sum(abs(Hs[t] - Hs[t - 1]) for t in range(1, len(Hs))) / (len(Hs) - 1)


# ════════════════════════════════════════════════════════════════
# §4 — Depth block
# ════════════════════════════════════════════════════════════════

def derived_curvature(tensor_block: dict) -> list[list[float]]:
    """c_j(t) = kappa_jj(t) / sum kappa_kk(t)."""
    out = []
    for ts in tensor_block["timesteps"]:
        x = ts["composition"]
        # kappa_jj = (1 - 1/D) / x_j^2; (1-1/D) cancels under closure.
        diag = [1.0 / (v * v) for v in x]
        out.append(close(diag))
    return out


def derived_energy(tensor_block: dict) -> list[list[float]]:
    """e_j(t) = (delta h_j)^2 / sum (delta h_k)^2."""
    timesteps = tensor_block["timesteps"]
    out = []
    for i in range(1, len(timesteps)):
        dh = np.array(timesteps[i]["clr"]) - np.array(timesteps[i - 1]["clr"])
        sqs = (dh ** 2).tolist()
        # Replace zeros with epsilon for closure
        out.append(close(sqs))
    return out


def summarise_level(tensor_block: dict, level: int, status: str = "PRODUCTIVE") -> dict:
    """Summary statistics for one level of a depth tower."""
    ts = tensor_block["timesteps"]
    T = len(ts)
    if T == 0:
        return {"level": level, "T": 0, "status": "SIGNAL_SHORT"}
    hs_vals = [t["higgins_scale"] for t in ts]
    omegas = [t.get("angular_velocity_deg", 0.0) for t in ts if "angular_velocity_deg" in t]
    helms = [t.get("helmsman", "") for t in ts if "helmsman" in t]
    # Deterministic tie-break: highest count, then alphabetical (set iteration is
    # not deterministic; sorting first guarantees stable ordering across runs).
    if helms:
        unique_sorted = sorted(set(helms))
        helm_dom = max(unique_sorted, key=helms.count)
    else:
        helm_dom = ""
    return {
        "level":         level,
        "T":             T,
        "D":             len(ts[0]["composition"]),
        "hs_mean":       sum(hs_vals) / T,
        "hs_var":        float(np.var(hs_vals)),
        "omega_mean":    (sum(omegas) / len(omegas)) if omegas else 0.0,
        "omega_var":     float(np.var(omegas)) if omegas else 0.0,
        "omega_max":     max(omegas) if omegas else 0.0,
        "helmsman":      helm_dom,
        "status":        status,
    }


def detect_period(traj: list[float], precision: float) -> tuple[bool, int, float, int]:
    """Detect period-1 or period-2 limit cycle in a Hs trajectory.

    Uses RELATIVE precision (matches existing engine convention).

    Period-1 requires TWO consecutive level pairs to satisfy the precision
    condition. This guards against false positives where a single coincidental
    L_k ≈ L_{k-1} would otherwise stop the recursion prematurely (observed
    on USA EMBER, where L1=0.79, L2=0.80 happens to satisfy 1% but L3 then
    jumps to 0.99 — not a real fixed point).

    Period-2 requires BOTH even-parity AND odd-parity sequences to converge
    simultaneously (same logic, applied to alternating levels).

    Returns (detected, period, residual, convergence_level).
    """
    n = len(traj)
    if n < 4:
        return (False, 0, math.inf, -1)

    # Period 1: TWO consecutive level pairs must satisfy precision
    for k in range(3, n):
        denom_a = max(abs(traj[k - 1]), 1e-15)
        rel_a   = abs(traj[k]     - traj[k - 1]) / denom_a
        denom_b = max(abs(traj[k - 2]), 1e-15)
        rel_b   = abs(traj[k - 1] - traj[k - 2]) / denom_b
        if rel_a < precision and rel_b < precision:
            return (True, 1, max(rel_a, rel_b), k)

    # Period 2: both even-parity AND odd-parity must converge at the same level k
    for k in range(4, n):
        if k - 3 < 0:
            continue
        denom_even = max(abs(traj[k - 2]), 1e-15)
        rel_even   = abs(traj[k]     - traj[k - 2]) / denom_even
        denom_odd  = max(abs(traj[k - 3]), 1e-15)
        rel_odd    = abs(traj[k - 1] - traj[k - 3]) / denom_odd
        if rel_even < precision and rel_odd < precision:
            return (True, 2, max(rel_even, rel_odd), k)

    # Not converged within trajectory
    return (False, 0,
            abs(traj[-1] - traj[-3]) / max(abs(traj[-3]), 1e-15) if n >= 3 else math.inf,
            -1)


def classify_impulse_response(A: float, zeta: float) -> str:
    if A < 0.1:                      return "CRITICALLY_DAMPED"
    if 0 < zeta < 0.1:               return "LIGHTLY_DAMPED"
    if abs(zeta) < 1e-6:             return "UNDAMPED"
    if A > 0.7:                      return "OVERDAMPED_EXTREME"
    return "MODERATELY_DAMPED"


def compute_depth(records_closed: list[list[float]],
                  tensor_block: dict,
                  carriers: list[str]) -> dict:
    """Recursive depth sounder — energy + curvature towers, attractor, IR."""
    T = len(tensor_block["timesteps"])
    D = len(carriers)

    # Involution proof — sample at multiple t
    samples = []
    sample_indices = sorted(set([0, T // 2, T - 1])) if T >= 1 else []
    for t in sample_indices:
        x = tensor_block["timesteps"][t]["composition"]
        Mx = metric_dual(x)
        MMx = metric_dual(Mx)
        residual = float(np.linalg.norm(np.array(MMx) - np.array(x)))
        h = clr(x); minus_h = clr(Mx)
        clr_neg_residual = float(np.linalg.norm(np.array(h) + np.array(minus_h)))
        d_dual = aitchison_distance(x, Mx)
        samples.append({
            "t":                       t,
            "x":                       x,
            "Mx":                      Mx,
            "MMx":                     MMx,
            "residual_M2":             residual,
            "clr_negation_residual":   clr_neg_residual,
            "duality_distance":        d_dual,
        })
    mean_resid = sum(s["residual_M2"] for s in samples) / len(samples) if samples else 0.0
    involution_proof = {
        "samples":         samples,
        "mean_residual":   mean_resid,
        "verified":        mean_resid < 1e-10,
        "n_samples":       len(samples),
    }

    level_0 = summarise_level(tensor_block, 0)

    # Build towers via iteration
    def build_tower(initial_records: list[list[float]],
                    tower_kind: str) -> tuple[list[dict], list[float]]:
        levels = []
        traj = []
        if tower_kind == "energy":
            current_records = initial_records
        else:
            current_records = initial_records

        for level_idx in range(1, DEPTH_MAX_LEVELS + 1):
            # Compute tensor for current level
            if len(current_records) < 5:
                lvl_summary = {"level": level_idx, "T": len(current_records), "status": "SIGNAL_SHORT"}
                levels.append(lvl_summary)
                break

            level_records = [{"label": f"L{level_idx}_{i}", "raw_values": list(r)}
                             for i, r in enumerate(current_records)]
            level_tensor = compute_tensor_block(level_records, carriers)
            lvl_summary = summarise_level(level_tensor, level_idx)
            levels.append(lvl_summary)
            traj.append(lvl_summary["hs_mean"])

            # Termination checks
            omega_var = lvl_summary["omega_var"]
            if omega_var < NOISE_FLOOR_OMEGA_VAR:
                lvl_summary["status"] = "OMEGA_FLAT"
                break
            if lvl_summary["hs_var"] < 1e-9:
                lvl_summary["status"] = "HS_FLAT"
                break

            # Period detection at level >= 2
            full_traj = [level_0["hs_mean"]] + traj
            detected, period, res, conv_lvl = detect_period(full_traj, DEPTH_PRECISION_TARGET)
            if detected:
                if period == 1:
                    lvl_summary["status"] = "LIMIT_CYCLE_P1"
                    break
                elif period == 2 and level_idx >= 4:
                    lvl_summary["status"] = "LIMIT_CYCLE_P2"
                    break

            # Iterate: derive next-level records
            if tower_kind == "energy":
                current_records = derived_energy(level_tensor)
            else:  # curvature
                current_records = derived_curvature(level_tensor)

        return levels, [level_0["hs_mean"]] + traj

    # Energy tower
    initial_energy_records = derived_energy(tensor_block)
    energy_tower, energy_traj = build_tower(initial_energy_records, "energy")

    # Curvature tower
    initial_curvature_records = derived_curvature(tensor_block)
    curvature_tower, curvature_traj = build_tower(initial_curvature_records, "curvature")

    # Termination summaries
    def cycle_summary(traj, levels):
        if not levels:
            return {"detected": False, "period": 0, "residual": math.inf, "convergence_level": -1}
        last_status = levels[-1].get("status", "PRODUCTIVE")
        det, per, res, conv = detect_period(traj, DEPTH_PRECISION_TARGET)
        return {
            "detected":          det,
            "period":            per if det else 0,
            "residual":          res,
            "convergence_level": conv,
        }

    energy_cycle = cycle_summary(energy_traj, energy_tower)
    curvature_cycle = cycle_summary(curvature_traj, curvature_tower)

    energy_depth = len(energy_tower)
    curvature_depth = len(curvature_tower)

    # Curvature attractor — period-2 metrics
    curv_attractor = {"period": curvature_cycle["period"]}
    if curvature_cycle["period"] == 2 and len(curvature_traj) >= 4:
        tail_size = min(6, len(curvature_traj))
        tail_start = len(curvature_traj) - tail_size
        ev = [v for n, v in enumerate(curvature_traj)
              if n >= tail_start and n % 2 == 0]
        od = [v for n, v in enumerate(curvature_traj)
              if n >= tail_start and n % 2 == 1]
        if ev and od:
            c_even = sum(ev) / len(ev); c_odd = sum(od) / len(od)
            amplitude = abs(c_even - c_odd)
            deltas = [curvature_traj[n] - (c_even if n % 2 == 0 else c_odd)
                      for n in range(len(curvature_traj))]
            ratios = []
            for n in range(len(deltas) - 2):
                a = abs(deltas[n]); b = abs(deltas[n + 2])
                if a > 1e-12 and b > 1e-12:
                    ratios.append(b / a)
            if ratios:
                contraction_lyap = sum(math.log(r) for r in ratios if r > 0) / len(ratios)
                mean_cr = sum(ratios) / len(ratios)
            else:
                contraction_lyap = float("nan"); mean_cr = float("nan")
            curv_attractor.update({
                "c_even":                  c_even,
                "c_odd":                   c_odd,
                "amplitude":               amplitude,
                "convergence_level":       curvature_cycle["convergence_level"],
                "residual":                curvature_cycle["residual"],
                "contraction_lyapunov":    contraction_lyap,
                "mean_contraction_ratio":  mean_cr,
                "banach_satisfied":        (mean_cr < 1.0) if not math.isnan(mean_cr) else False,
            })
    elif curvature_cycle["period"] == 1 and curvature_traj:
        curv_attractor.update({
            "c_fixed":             curvature_traj[-1],
            "amplitude":           0.0,
            "convergence_level":   curvature_cycle["convergence_level"],
            "residual":            curvature_cycle["residual"],
        })

    # Impulse response classification
    # Engine 2.0.3: distinguish three "non-period-2" cases that previously
    # all collapsed to DEGENERATE:
    #   ENERGY_STABLE_FIXED_POINT — energy tower converges to period-1 with
    #     low amplitude. The system is genuinely stable in energy phase
    #     space; curvature tower may have hit a vertex due to compositional
    #     concentration. Canonical example: BackBlaze fleet.
    #   CURVATURE_VERTEX_FLAT — curvature tower terminated HS_FLAT due to
    #     a single carrier dominating > 60% of the composition. The
    #     curvature recursion's 1/x_j² weighting drives to a vertex.
    #   D2_DEGENERATE — D = 2 (no off-diagonal metric structure for the
    #     recursion to develop). Canonical example: Gold/Silver.
    # Genuine "no idea what's happening" cases keep DEGENERATE.

    def _max_carrier_share(records_closed):
        if not records_closed: return 0.0
        return max(max(r) for r in records_closed)

    if curv_attractor.get("amplitude", 0) > 0 and len(curvature_traj) >= 2:
        A_init = abs(curvature_traj[1] - curvature_traj[0])
        A_final = curv_attractor["amplitude"]
        depth_delta = curvature_depth
        if A_init > 0 and A_final > 0:
            zeta = -math.log(A_final / A_init) / depth_delta
        else:
            zeta = 0.0
        ir = {
            "amplitude_A":    A_final,
            "depth_delta":    depth_delta,
            "damping_zeta":   zeta,
            "classification": classify_impulse_response(A_final, zeta),
        }
    else:
        # No period-2 attractor — disambiguate the non-period-2 case
        D_input = len(records_closed[0]) if records_closed else 0
        max_share = _max_carrier_share(records_closed)
        curv_term = curvature_tower[-1].get("status", "") if curvature_tower else ""
        e_period = energy_cycle.get("period", 0) if energy_cycle.get("detected") else 0
        e_traj = energy_traj if isinstance(energy_traj, list) else []

        # Decide the class
        if D_input <= 2:
            cls = "D2_DEGENERATE"
        elif curv_term == "HS_FLAT" and max_share > 0.60:
            cls = "CURVATURE_VERTEX_FLAT"
        elif e_period == 1 and len(e_traj) >= 2:
            # Energy tower converged period-1 — measure energy amplitude
            e_amp = abs(e_traj[-1] - e_traj[0]) if e_traj else 0.0
            if e_amp < 0.5:
                cls = "ENERGY_STABLE_FIXED_POINT"
            else:
                cls = "DEGENERATE"
        else:
            cls = "DEGENERATE"

        ir = {
            "amplitude_A":          curv_attractor.get("amplitude", 0.0),
            "depth_delta":          curvature_depth,
            "damping_zeta":         0.0,
            "classification":       cls,
            "max_carrier_share":    max_share,
            "curv_termination":     curv_term,
            "energy_period":        e_period,
            "D":                    D_input,
        }

    # Mean duality distance
    if T >= 1:
        d_duals = [aitchison_distance(ts["composition"], metric_dual(ts["composition"]))
                   for ts in tensor_block["timesteps"]]
        mean_dual = sum(d_duals) / len(d_duals)
    else:
        mean_dual = 0.0

    summary = {
        "energy_depth":            energy_depth,
        "curvature_depth":         curvature_depth,
        "dynamical_depth":         max(energy_depth, curvature_depth),
        "energy_termination":      energy_tower[-1].get("status", "UNKNOWN") if energy_tower else "NONE",
        "curvature_termination":   curvature_tower[-1].get("status", "UNKNOWN") if curvature_tower else "NONE",
        "energy_hs_trajectory":    energy_traj,
        "curvature_hs_trajectory": curvature_traj,
        "mean_duality_distance":   mean_dual,
        "convergence_precision":   DEPTH_PRECISION_TARGET,
        "noise_floor_omega_var":   NOISE_FLOOR_OMEGA_VAR,
        "max_levels":              DEPTH_MAX_LEVELS,
    }

    return {
        "involution_proof":     involution_proof,
        "level_0":              level_0,
        "energy_tower":         energy_tower,
        "curvature_tower":      curvature_tower,
        "curvature_attractor":  curv_attractor,
        "impulse_response":     ir,
        "energy_cycle":         energy_cycle,
        "curvature_cycle":      curvature_cycle,
        "summary":              summary,
    }


# ════════════════════════════════════════════════════════════════
# §5 — Diagnostics block
# ════════════════════════════════════════════════════════════════

def eitt_bench_test(records_closed: list[list[float]], T: int) -> dict:
    """EITT M-sweep at canonical compression ratios.

    Gate threshold and M-sweep set from USER CONFIG (EITT_GATE_PCT,
    EITT_M_SWEEP_BASE).
    """
    if T < 4:
        return {
            "H_mean_full":    0.0,
            "M_sweep":        [],
            "gate_pct":       EITT_GATE_PCT,
            "note":           "T < 4: EITT bench-test not applicable.",
        }
    H_full = sum(shannon_entropy(r) for r in records_closed) / T
    base_Ms = list(EITT_M_SWEEP_BASE)
    if T >= 101:
        base_Ms.append(int(math.ceil(T / 101)))
    M_sweep = []
    seen_Ms = set()
    for M in sorted(base_Ms):
        if M >= T or M in seen_Ms: continue
        seen_Ms.add(M)
        decimated = []
        for b in range(0, T, M):
            block = records_closed[b:b + M]
            if len(block) >= 2:
                decimated.append(aitchison_barycenter(block))
            elif len(block) == 1:
                decimated.append(block[0])
        if not decimated:
            continue
        H_dec = sum(shannon_entropy(c) for c in decimated) / len(decimated)
        var_pct = abs(H_dec - H_full) / H_full * 100 if H_full > 0 else 0.0
        M_sweep.append({
            "M":                 M,
            "n_blocks":          len(decimated),
            "H_mean_decimated":  H_dec,
            "variation_pct":     var_pct,
            "pass_gate":         var_pct < EITT_GATE_PCT,
        })
    return {
        "H_mean_full": H_full,
        "M_sweep":     M_sweep,
        "gate_pct":    EITT_GATE_PCT,
        "note":        ("Empirical observation of trajectory smoothness "
                        "under temporal decimation, not a geometric theorem. "
                        "Shannon entropy is not scale-invariant; the apparent "
                        "preservation reflects the compositional smoothness "
                        "of the trajectory, not Aitchison invariance."),
    }


def detect_lock_events(tensor_block: dict, carriers: list[str]) -> list[dict]:
    events = []
    timesteps = tensor_block["timesteps"]
    D = len(carriers)
    for i, ts in enumerate(timesteps):
        h = ts["clr"]
        clr_spread = max(h) - min(h)
        if clr_spread < DEGEN_THRESHOLD:
            events.append({
                "event_type":     "DEGEN",
                "timestep_index": i,
                "label":          ts["label"],
                "carrier":        None,
                "clr_value":      clr_spread,
                "context":        "Composition collapsed near barycenter",
            })
        for j in range(D):
            if h[j] < LOCK_CLR_THRESHOLD:
                # determine acquisition vs loss
                prev_low = (i > 0 and timesteps[i - 1]["clr"][j] < LOCK_CLR_THRESHOLD)
                if not prev_low:
                    event_type = "LOCK-ACQ"
                else:
                    # is this also exiting? check next
                    if i < len(timesteps) - 1 and timesteps[i + 1]["clr"][j] >= LOCK_CLR_THRESHOLD:
                        event_type = "LOCK-LOSS"
                    else:
                        event_type = "LOCK-ACQ"  # ongoing low state
                events.append({
                    "event_type":     event_type,
                    "timestep_index": i,
                    "label":          ts["label"],
                    "carrier":        carriers[j],
                    "clr_value":      h[j],
                    "context":        f"{carriers[j]} CLR = {h[j]:.2f} (below threshold {LOCK_CLR_THRESHOLD})",
                })
    return events


def degeneracy_flags(records_closed: list[list[float]],
                      carriers: list[str]) -> list[dict]:
    flags = []
    T = len(records_closed); D = len(carriers)
    if T < 20:
        flags.append({
            "flag":      "small_T",
            "severity":  "warning",
            "message":   "Trajectory too short for stable depth-tower estimation.",
            "condition": f"T = {T} < 20",
        })
    if D < 3:
        flags.append({
            "flag":      "small_D",
            "severity":  "warning",
            "message":   "Compositional dimension too small for full CNT structure.",
            "condition": f"D = {D} < 3",
        })
    # Pre-aligned: any single carrier monotonic
    for j in range(D):
        series = [r[j] for r in records_closed]
        is_inc = all(series[t] <= series[t + 1] for t in range(len(series) - 1))
        is_dec = all(series[t] >= series[t + 1] for t in range(len(series) - 1))
        if is_inc or is_dec:
            flags.append({
                "flag":      "pre_aligned_compositionally",
                "severity":  "warning",
                "message":   (f"Records appear sorted by carrier {carriers[j]}; "
                              "depth recursion may be degenerate."),
                "condition": f"composition[{j}] is monotonic across all records",
            })
            break
    return flags


def compute_diagnostics(records_closed: list[list[float]],
                         tensor_block: dict,
                         carriers: list[str]) -> dict:
    return {
        "eitt_residuals":     eitt_bench_test(records_closed, len(records_closed)),
        "lock_events":        detect_lock_events(tensor_block, carriers),
        "degeneracy_flags":   degeneracy_flags(records_closed, carriers),
        # content_sha256 added at end after full json built
    }


# ════════════════════════════════════════════════════════════════
# §6 — Orchestration & I/O
# ════════════════════════════════════════════════════════════════

def ingest_csv(path: str) -> tuple[list[str], list[dict], list[list[float]], dict, dict]:
    """Read CSV. First column = label, remaining columns = D carriers.

    Returns: (carriers, records, records_closed, ingest_meta, zero_meta)
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for r in reader:
            if not r or all(not c.strip() for c in r): continue
            rows.append(r)
    carriers = [c.strip() for c in header[1:]]
    records = []
    records_closed = []
    n_zeros = 0
    for r in rows:
        if len(r) < len(header): continue
        try:
            vals = [float(v) for v in r[1:1 + len(carriers)]]
        except ValueError:
            continue
        if any(v < 0 for v in vals): continue
        if any(v == 0 for v in vals):
            n_zeros += 1
        records.append({"label": r[0].strip(), "raw_values": vals})
        records_closed.append(close(vals))
    ingest_meta = {
        "header":       header,
        "n_carriers":   len(carriers),
        "n_records":    len(records),
    }
    zero_meta = {
        "method":         "multiplicative",
        "delta":          DEFAULT_DELTA,
        "applied":        n_zeros > 0,
        "n_replacements": n_zeros,
    }
    return carriers, records, records_closed, ingest_meta, zero_meta


def get_environment_metadata() -> dict:
    """Capture provenance: git SHA, language version, libs, platform."""
    try:
        git_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL, cwd=os.path.dirname(os.path.abspath(__file__))
        ).decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        git_sha = "unknown"
    return {
        "git_sha":         git_sha,
        "language_version":f"python {sys.version.split()[0]}",
        "numerical_lib":   f"numpy {np.__version__}",
        "platform":        platform.platform(),
        "hostname_hash":   hashlib.sha256(platform.node().encode()).hexdigest(),
    }


def file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def closed_data_sha256(records_closed: list[list[float]], carriers: list[str]) -> str:
    """SHA-256 of canonical closed-data form (carriers + closed values)."""
    canonical = json.dumps({
        "carriers": carriers,
        "values":   records_closed,
    }, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def content_sha256(json_obj: dict) -> str:
    """SHA-256 of canonicalised JSON with run-time fields removed."""
    j = json.loads(json.dumps(json_obj))
    j.get("metadata", {}).pop("generated", None)
    j.get("metadata", {}).pop("wall_clock_ms", None)
    j.get("metadata", {}).pop("environment", None)
    j.get("diagnostics", {}).pop("content_sha256", None)
    canonical = json.dumps(j, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ════════════════════════════════════════════════════════════════
# §6b — v2.0.0 output formatting
#
# Computations above produce flat internal dicts. These formatters
# split each block into coda_standard / higgins_extensions sub-blocks
# and add _function / _description fields per schema 2.0.0.
# ════════════════════════════════════════════════════════════════

# Field-ownership tables. Mapping from flat-key → "coda" or "higgins".
_TIMESTEP_CODA_FIELDS = {
    "composition", "clr", "ilr", "shannon_entropy",
    "aitchison_norm", "aitchison_distance_step",
}
_TIMESTEP_HIGGINS_FIELDS = {
    "higgins_scale", "bearing_tensor", "metric_tensor", "metric_tensor_diagonal",
    "condition_number", "angular_velocity_deg", "helmsman", "helmsman_delta",
}
_TIMESTEP_TOPLEVEL_FIELDS = {"index", "label", "raw_values"}


def _format_tensor_block_v2(tensor_block: dict) -> dict:
    """Restructure flat tensor_block into v2.0.0 schema layout."""
    out = {
        "_function":    "composer",
        "_description": ("Per-record compositional state. coda_standard fields "
                         "follow Aitchison/Egozcue/Shannon. higgins_extensions "
                         "are HUF-framework readings of the same simplex; see "
                         "schema §8 for the mapping."),
        "helmert_basis": tensor_block["helmert_basis"],
        "timesteps":    [],
    }
    for ts in tensor_block["timesteps"]:
        coda = {k: ts[k] for k in _TIMESTEP_CODA_FIELDS if k in ts}
        higg = {k: ts[k] for k in _TIMESTEP_HIGGINS_FIELDS if k in ts}
        new_ts = {k: ts[k] for k in _TIMESTEP_TOPLEVEL_FIELDS}
        new_ts["coda_standard"]      = coda
        new_ts["higgins_extensions"] = higg
        out["timesteps"].append(new_ts)
    return out


def _format_stage1_v2(stage1: dict) -> dict:
    """Stage 1 is a formatter; outputs are HUF/CBS-specific."""
    return {
        "_function":    "formatter",
        "_description": ("Cube-face projections and per-record metric ledger "
                         "formatted for plate display. HUF/CBS-specific."),
        "coda_standard":      {},
        "higgins_extensions": {
            "section_atlas":  stage1["section_atlas"],
            "metric_ledger":  stage1["metric_ledger"],
        },
    }


def _format_stage2_v2(stage2: dict) -> dict:
    """Stage 2 is a review; variation_matrix is CoDa, carrier_pair is Higgins."""
    return {
        "_function":    "review",
        "_description": "Pairwise cross-examination of compositional behaviour.",
        "coda_standard":      {
            "variation_matrix": stage2["variation_matrix"],
        },
        "higgins_extensions": {
            "carrier_pair_examination": stage2["carrier_pair_examination"],
        },
    }


def _format_stage3_v2(stage3: dict) -> dict:
    """Stage 3 is a review; subcomp ladder is CoDa, triadic+regimes are Higgins."""
    return {
        "_function":    "review",
        "_description": "Higher-degree subcompositional and triadic analysis.",
        "coda_standard":      {
            "subcomposition_ladder": stage3["subcomposition_ladder"],
        },
        "higgins_extensions": {
            "triadic_area":     stage3["triadic_area"],
            "carrier_triads":   stage3["carrier_triads"],
            "regime_detection": stage3["regime_detection"],
        },
    }


def _format_bridges_v2(bridges: dict) -> dict:
    """Bridges block; information_theory is CoDa-aligned, others are Higgins."""
    return {
        "_function":    "review",
        "_description": "Connections to dynamical / control / information theory.",
        "coda_standard":      {
            "information_theory": bridges["information_theory"],
        },
        "higgins_extensions": {
            "dynamical_systems": bridges["dynamical_systems"],
            "control_theory":    bridges["control_theory"],
        },
    }


def _format_depth_v2(depth: dict) -> dict:
    """Depth block is wholly Higgins extension."""
    return {
        "_function":    "review",
        "_description": ("Recursive depth sounder, period-2 attractor, "
                         "impulse response. Wholly Higgins-framework — no "
                         "CoDa-canon analogue."),
        "coda_standard":      {},
        "higgins_extensions": depth,
    }


def _format_diagnostics_v2(diag: dict) -> dict:
    """Diagnostics block; content_sha256 stays at top of the block."""
    out = {
        "_function":    "review",
        "_description": ("Engine self-checks: EITT residuals, lock events, "
                         "degeneracy flags, content hash."),
        "coda_standard":      {},
        "higgins_extensions": {
            "eitt_residuals":   diag["eitt_residuals"],
            "lock_events":      diag["lock_events"],
            "degeneracy_flags": diag["degeneracy_flags"],
        },
    }
    if "content_sha256" in diag:
        out["content_sha256"] = diag["content_sha256"]
    return out


# ─── v1.1-B native units bridge ────────────────────────────────────
def _build_units_block(input_units_arg: Optional[str],
                       higgins_scale_units_arg: Optional[str]) -> dict:
    """Resolve INPUT_UNITS / HIGGINS_SCALE_UNITS, return additive 2.1.0
    metadata.units block. Imports the helper lazily to avoid a hard
    coupling between the engine and the helper module."""
    import importlib, math
    iu = input_units_arg if input_units_arg else INPUT_UNITS
    hu_req = higgins_scale_units_arg if higgins_scale_units_arg else HIGGINS_SCALE_UNITS
    try:
        nu = importlib.import_module("native_units")
    except ImportError:
        try:
            from cnt import native_units as nu  # type: ignore
        except Exception:
            nu = None
    if nu is None:
        # Fallback — known factors inline (small duplicate of native_units.py)
        factors = {"ratio": 1.0, "neper": 1.0, "nat": 1.0, "%": 1.0,
                   "absolute": 1.0, "bit": math.log(2.0),
                   "dB_power": math.log(10.0)/10.0,
                   "dB_amplitude": math.log(10.0)/20.0}
        f = factors.get(iu, 1.0)
        if hu_req == "auto":
            hu = "bit" if iu == "bit" else "neper"
        else:
            hu = hu_req
        return {"_description":              "v1.1-B native units (additive 2.1.0).",
                "input_units":                iu,
                "higgins_scale_units":        hu,
                "units_scale_factor_to_neper":f,
                "report_units_scale_factors": REPORT_UNITS_SCALE_FACTORS}
    decl = nu.declare(iu, hu_req)
    decl["_description"]               = "v1.1-B native units (additive 2.1.0)."
    decl["report_units_scale_factors"] = REPORT_UNITS_SCALE_FACTORS
    return decl


def cnt_run(csv_path: str,
            output_path: Optional[str] = None,
            ordering: Optional[dict] = None,
            engine_config_overrides: Optional[dict] = None,
            input_units: Optional[str] = None,
            higgins_scale_units: Optional[str] = None) -> dict:
    """Top-level CNT run, schema 2.1.0.

    Args:
        csv_path:    input CSV (first col = label, rest = D carriers).
        output_path: where to write the JSON. If None, return dict only.
        ordering:    user-declared ordering convention (REQUIRED, see schema §2).
        engine_config_overrides:
                     dict of {USER_CONFIG_NAME: value} pairs that override the
                     module-level constants for this single call. Honoured
                     keys: DEFAULT_DELTA, DEGEN_THRESHOLD, LOCK_CLR_THRESHOLD,
                     DEPTH_MAX_LEVELS, DEPTH_PRECISION_TARGET,
                     NOISE_FLOOR_OMEGA_VAR, TRIADIC_T_LIMIT, TRIADIC_K_DEFAULT,
                     EITT_GATE_PCT, EITT_M_SWEEP_BASE.
                     Different overrides → different content_sha256 (by design).
        input_units, higgins_scale_units:
                     v1.1-B native units. If None, falls back to module
                     defaults (INPUT_UNITS / HIGGINS_SCALE_UNITS).

    Returns:
        The full canonical JSON as a dict, conforming to schema 2.1.0
        (every analytic block split into coda_standard / higgins_extensions
        sub-blocks with _function / _description meta; metadata.units_*
        block declares the unit lineage).
    """
    # ─── apply engine_config_overrides on module globals (with restore) ──
    _override_keys = ("DEFAULT_DELTA", "DEGEN_THRESHOLD", "LOCK_CLR_THRESHOLD",
                      "DEPTH_MAX_LEVELS", "DEPTH_PRECISION_TARGET",
                      "NOISE_FLOOR_OMEGA_VAR", "TRIADIC_T_LIMIT",
                      "TRIADIC_K_DEFAULT", "EITT_GATE_PCT", "EITT_M_SWEEP_BASE")
    _saved_globals = {}
    if engine_config_overrides:
        for k, v in engine_config_overrides.items():
            if k not in _override_keys:
                raise ValueError(
                    f"engine_config_overrides: '{k}' is not a recognized "
                    f"USER CONFIG constant.  Allowed: {_override_keys}")
            _saved_globals[k] = globals()[k]
            globals()[k] = v
    try:
        return _cnt_run_impl(csv_path, output_path, ordering,
                             engine_config_overrides or {},
                             input_units, higgins_scale_units)
    finally:
        for k, v in _saved_globals.items():
            globals()[k] = v


def _cnt_run_impl(csv_path: str,
                  output_path: Optional[str],
                  ordering: Optional[dict],
                  active_overrides: dict,
                  input_units: Optional[str],
                  higgins_scale_units: Optional[str]) -> dict:
    """Inner CNT run — globals already mutated by cnt_run for any overrides."""
    t0 = time.time()
    if ordering is None:
        ordering = {
            "is_temporal":     False,
            "ordering_method": "as-given",
            "caveat":          "User did not declare ordering. Treat derivative "
                               "fields (angular_velocity, energy_depth) with caution.",
        }

    carriers, records, records_closed, ingest_meta, zero_meta = ingest_csv(csv_path)

    # Compute (flat internals)
    tensor_block = compute_tensor_block(records, carriers)
    stage1       = compute_stage1(tensor_block, carriers)
    stage2       = compute_stage2(records_closed, tensor_block, carriers)
    stage3       = compute_stage3(records_closed, tensor_block, carriers)
    bridges      = compute_bridges(records_closed, tensor_block, carriers)
    depth_block  = compute_depth(records_closed, tensor_block, carriers)
    diagnostics  = compute_diagnostics(records_closed, tensor_block, carriers)

    wall_ms = int((time.time() - t0) * 1000)
    json_out = {
        "metadata": {
            "_function":              "provenance",
            "_description":           "Identity, schema version, run-time provenance.",
            "schema_version":         SCHEMA_VERSION,
            "engine_version":         f"{ENGINE_NAME} {ENGINE_VERSION}",
            "engine_implementation":  "python",
            "generated":              datetime.now(timezone.utc).isoformat(),
            "wall_clock_ms":          wall_ms,
            "mathematical_lineage": {
                "Aitchison_1986": "CLR transform, simplex geometry, Aitchison distance",
                "Shannon_1948":   "Entropy H = -sum x_j ln x_j",
                "Egozcue_2003":   "ILR, Helmert basis, orthonormal coordinates",
                "Higgins_2026":   "CNT tensor decomposition, recursive depth sounder, metric dual involution",
            },
            "engine_config": {
                "_description":           ("Active values from the USER CONFIGURATION block at top of cnt.py. "
                                            "Two runs with identical config and input produce identical content_sha256. "
                                            "Two runs with different config produce different content_sha256 - that is correct."),
                "DEFAULT_DELTA":          DEFAULT_DELTA,
                "DEGEN_THRESHOLD":        DEGEN_THRESHOLD,
                "LOCK_CLR_THRESHOLD":     LOCK_CLR_THRESHOLD,
                "DEPTH_MAX_LEVELS":       DEPTH_MAX_LEVELS,
                "DEPTH_PRECISION_TARGET": DEPTH_PRECISION_TARGET,
                "NOISE_FLOOR_OMEGA_VAR":  NOISE_FLOOR_OMEGA_VAR,
                "TRIADIC_T_LIMIT":        TRIADIC_T_LIMIT,
                "TRIADIC_K_DEFAULT":      TRIADIC_K_DEFAULT,
                "EITT_GATE_PCT":          EITT_GATE_PCT,
                "EITT_M_SWEEP_BASE":      list(EITT_M_SWEEP_BASE),
                "active_overrides":       (active_overrides or {}),
            },
            "units": _build_units_block(input_units, higgins_scale_units),
            "environment":            get_environment_metadata(),
        },
        "input": {
            "_function":           "provenance",
            "_description":        ("Source data identity, hashes, and ordering declaration."),
            "source_file":         os.path.basename(csv_path),
            "source_file_sha256":  file_sha256(csv_path),
            "closed_data_sha256":  closed_data_sha256(records_closed, carriers),
            "n_records":           len(records),
            "n_carriers":          len(carriers),
            "carriers":            carriers,
            "labels":              [r["label"] for r in records],
            "zero_replacement":    zero_meta,
            "ordering":            ordering,
        },
        "tensor":      _format_tensor_block_v2(tensor_block),
        "stages": {
            "stage1": _format_stage1_v2(stage1),
            "stage2": _format_stage2_v2(stage2),
            "stage3": _format_stage3_v2(stage3),
        },
        "bridges":     _format_bridges_v2(bridges),
        "depth":       _format_depth_v2(depth_block),
        "diagnostics": _format_diagnostics_v2(diagnostics),
    }

    json_out["diagnostics"]["content_sha256"] = content_sha256(json_out)

    if output_path:
        with open(output_path, "w") as f:
            json.dump(json_out, f, indent=2)

    return json_out


def main():
    ap = argparse.ArgumentParser(description="CNT engine v2.0.x - canonical JSON generator.")
    ap.add_argument("input", help="Input CSV (first col = label, rest = carriers).")
    ap.add_argument("-o", "--output", default=None, help="Output JSON path. Default: <input>_cnt.json")
    ap.add_argument("--temporal", action="store_true", help="Mark input as a time series.")
    ap.add_argument("--ordering-method", default="as-given")
    ap.add_argument("--ordering-caveat", default=None)
    args = ap.parse_args()

    out = args.output or os.path.splitext(args.input)[0] + "_cnt.json"
    ordering = {
        "is_temporal":     bool(args.temporal),
        "ordering_method": args.ordering_method,
        "caveat":          args.ordering_caveat or (
            None if args.temporal else
            "Order is treated as arbitrary; angular_velocity and energy_depth are ordering-dependent."
        ),
    }

    print(f"CNT Engine v{ENGINE_VERSION}  (schema {SCHEMA_VERSION})")
    print(f"Input:    {args.input}")
    print(f"Output:   {out}")
    print(f"Ordering: temporal={ordering['is_temporal']} method={ordering['ordering_method']}")

    j = cnt_run(args.input, out, ordering)

    md   = j["metadata"]
    inp  = j["input"]
    dpt  = j["depth"]["higgins_extensions"]["summary"]
    cur  = j["depth"]["higgins_extensions"]["curvature_attractor"]
    ir   = j["depth"]["higgins_extensions"]["impulse_response"]
    eitt = j["diagnostics"]["higgins_extensions"]["eitt_residuals"]
    print()
    print(f"=== Summary ===")
    print(f"  T = {inp['n_records']}, D = {inp['n_carriers']}")
    print(f"  Curvature depth = {dpt['curvature_depth']}")
    print(f"  Energy depth    = {dpt['energy_depth']}")
    if cur.get("amplitude") is not None:
        lyap = cur.get("contraction_lyapunov", float("nan"))
        period_str = str(cur.get('period', '?'))
        amp_val = cur.get('amplitude', 0.0) or 0.0
        ir_cls = ir.get('classification', '?')
        print(f"  Period-{period_str} attractor: A={amp_val:.4f}, "
              f"contraction lambda={lyap:.4f}, IR class = {ir_cls}")
    if eitt["M_sweep"]:
        biggest_M = eitt["M_sweep"][-1]
        gate_label = 'PASS' if biggest_M.get('pass_gate', biggest_M.get('pass_5pct', False)) else 'FAIL'
        print(f"  EITT residual at M={biggest_M['M']}: {biggest_M['variation_pct']:.3f}%  ({gate_label})")
    print(f"  Lock events:     {len(j['diagnostics']['higgins_extensions']['lock_events'])}")
    print(f"  Degeneracy flags:{len(j['diagnostics']['higgins_extensions']['degeneracy_flags'])}")
    print(f"  M^2 = I residual:{j['depth']['higgins_extensions']['involution_proof']['mean_residual']:.2e}")
    print(f"  content_sha256:  {j['diagnostics']['content_sha256'][:16]}...")
    print(f"  wall_clock:      {md['wall_clock_ms']} ms")


if __name__ == "__main__":
    main()
