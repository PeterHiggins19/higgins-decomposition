"""
HCI-CNT v3.0.0 — Compositional Navigation Tensor engine

Domain-neutral compositional inference engine. Reads compositional time series
(rows-by-carriers CSV), produces a deterministic JSON record of the trajectory's
geometric, dynamic, and depth-tower structure.

Pipeline (push #32 architecture):

    rows  ->  closure   ->  CLR    ->  Helmert ILR
                                      |
                                      +->  per-step tensor block (kappa_HS,
                                      |    s_j sensitivity, bearing, helmsman)
                                      |
                                      +->  stages 1/2/3 (atlas, variation,
                                      |    triadic area, carrier-pair / triad
                                      |    examinations, regime detection)
                                      |
                                      +->  depth_tower (energy + curvature
                                      |    levels, P2 attractor fit, M^2=I
                                      |    involution sample)
                                      |
                                      +->  helmsman family channels
                                      |
                                      +->  diagnostics (EITT, lock events,
                                           degeneracy flags, content_sha256)

Output is a CoDa-community-vocabulary JSON record. Domain interpretation lives
in wrappers (HCI-CNQ/wrappers/), not in this engine. Engine version, schema
version, and content hash are embedded; CNT v3 hashes are independent of any
other engine's hashes by design.

License:   Apache-2.0
Lineage:   v0.29.0 freezes v2.0.4 for legacy reproducibility; v3.0.0 generalises
Catalog:   INV-036 (CNT v3 build), INV-038 (engine-independence policy),
           INV-045 (Suspicion of Every Assumption methodology applied)

See:       ai-refresh/CNT_V3_CNQ_V2_DESIGN.md  for architectural rationale
           HCI-CNT/engine/CNT_V3_PSEUDOCODE.md for language-agnostic algorithm
           HCI-CNT/engine/CNT_V3_SCHEMA.md     for output schema
           HCI-CNT/engine/ANTI_SPECIFICATION.md for failure-mode enumeration
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import socket
import subprocess
import sys
import time
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

# Ensure hci_shared is importable when running cnt.py directly.
_THIS_FILE = Path(__file__).resolve()
for _candidate in (_THIS_FILE.parent.parent.parent, _THIS_FILE.parent.parent.parent.parent):
    if (_candidate / "hci_shared" / "__init__.py").exists():
        sys.path.insert(0, str(_candidate))
        break

from hci_shared import (  # noqa: E402
    canonical_sha256,
    closure as _shared_closure,
    clr as _shared_clr,
    file_sha256,
    helmert_basis,
    InvalidInputError,
    validate_rows,
)
from hci_shared.geometry import compositions_to_ilr  # noqa: E402
from hci_shared.attractors import fit_attractor  # noqa: E402
from hci_shared.helmsman import compute_helmsman_family  # noqa: E402


# ---------------------------------------------------------------------------
# USER CONFIG (engine-level constants and defaults)
# ---------------------------------------------------------------------------

ENGINE_NAME: str = "HCI-CNT"
ENGINE_VERSION: str = "3.0.0"
SCHEMA_VERSION: str = "3.0.0"
ENGINE_PRINCIPLE: str = (
    "Closure -> CLR -> Helmert ILR -> trajectory tensor -> depth tower; "
    "deterministic compositional inference with embedded version triple."
)

# Numerical / structural defaults.
DEFAULT_DELTA: float = 1e-15
DEGEN_THRESHOLD: float = 1e-4
LOCK_CLR_THRESHOLD: float = -10.0
DEPTH_MAX_LEVELS: int = 50
DEPTH_PRECISION_TARGET: float = 1e-2
TRIADIC_T_LIMIT: int = 500
TRIADIC_K_DEFAULT: int = 50
LADDER_K_LIMIT: int = 200
EITT_GATE_PCT: float = 5.0
EITT_M_SWEEP_BASE: Tuple[int, ...] = (2, 4, 8, 16, 32, 64, 128)
HELMSMAN_ROLLING_WINDOW: int = 8


# ---------------------------------------------------------------------------
# Core math helpers (CoDa primitives that cnt.py uses but hci_shared doesn't)
# ---------------------------------------------------------------------------


def shannon_entropy(p: np.ndarray) -> float:
    p = np.asarray(p, dtype=np.float64)
    p_safe = np.where(p > 0, p, 1.0)
    return float(-np.sum(np.where(p > 0, p * np.log(p_safe), 0.0)))


def higgins_scale(p: np.ndarray) -> float:
    p = np.asarray(p, dtype=np.float64)
    D = p.shape[-1]
    if D < 2:
        return 0.0
    h = shannon_entropy(p)
    return float(1.0 - h / np.log(D))


def aitchison_norm(clr_vec: np.ndarray) -> float:
    return float(np.linalg.norm(clr_vec))


def aitchison_distance(clr_a: np.ndarray, clr_b: np.ndarray) -> float:
    return float(np.linalg.norm(clr_a - clr_b))


def kappa_HS_full(p: np.ndarray) -> Dict[str, Any]:
    p = np.asarray(p, dtype=np.float64)
    D = p.shape[-1]
    one_over_D = 1.0 / D
    p_outer = np.outer(p, p)
    delta = np.eye(D)
    K = (delta - one_over_D) / p_outer
    eigvals = np.linalg.eigvalsh(K)
    eigvals_sorted = np.sort(eigvals)
    trace = float(np.trace(K))
    nonzero = np.abs(eigvals_sorted) > 1e-12
    if nonzero.any():
        nz = np.abs(eigvals_sorted[nonzero])
        cond = float(nz.max() / nz.min())
    else:
        cond = float("inf")
    return {
        "matrix": K.tolist(),
        "eigenvalues": [float(x) for x in eigvals_sorted],
        "trace": trace,
        "condition_number": cond if np.isfinite(cond) else None,
    }


def s_j_sensitivity(p: np.ndarray) -> List[float]:
    p = np.asarray(p, dtype=np.float64)
    inv = 1.0 / p
    inv_closed = inv / inv.sum()
    return [float(x) for x in inv_closed]


def bearing_pairs(h_clr: np.ndarray, carriers: Sequence[str]) -> List[Dict[str, Any]]:
    h = np.asarray(h_clr, dtype=np.float64)
    D = h.shape[-1]
    out = []
    for i in range(D):
        for j in range(i + 1, D):
            theta_deg = float(np.degrees(np.arctan2(h[j], h[i])))
            out.append({"i": carriers[i], "j": carriers[j], "theta_deg": theta_deg})
    return out


def angular_velocity_deg(h_prev: np.ndarray, h_curr: np.ndarray) -> float:
    a = np.asarray(h_prev, dtype=np.float64)
    b = np.asarray(h_curr, dtype=np.float64)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na < 1e-15 or nb < 1e-15:
        return 0.0
    cos_theta = float(np.clip(np.dot(a, b) / (na * nb), -1.0, 1.0))
    return float(np.degrees(np.arccos(cos_theta)))


def helmsman_dcdi(h_prev: np.ndarray, h_curr: np.ndarray) -> int:
    delta = np.asarray(h_curr, dtype=np.float64) - np.asarray(h_prev, dtype=np.float64)
    return int(np.argmax(np.abs(delta)))


def variation_matrix(rows_closed: np.ndarray) -> np.ndarray:
    rows = np.asarray(rows_closed, dtype=np.float64)
    T, D = rows.shape
    log_rows = np.log(rows)
    tau = np.zeros((D, D), dtype=np.float64)
    for i in range(D):
        for j in range(D):
            if i == j:
                continue
            ratio = log_rows[:, i] - log_rows[:, j]
            tau[i, j] = float(np.var(ratio, ddof=0))
    return tau


def ring_classify(hs: float) -> str:
    if hs < 0.1:
        return "Hs-1"
    if hs < 0.3:
        return "Hs-2"
    if hs < 0.5:
        return "Hs-3"
    if hs < 0.7:
        return "Hs-4"
    if hs < 0.9:
        return "Hs-5"
    return "Hs-6"


# ---------------------------------------------------------------------------
# Per-timestep tensor block
# ---------------------------------------------------------------------------


def compute_timestep_block(
    t_index: int,
    label: Any,
    raw_values: np.ndarray,
    composition: np.ndarray,
    clr_vec: np.ndarray,
    ilr_vec: np.ndarray,
    carriers: Sequence[str],
    prev_clr: Optional[np.ndarray],
) -> Dict[str, Any]:
    coda_standard = {
        "composition": [float(x) for x in composition],
        "clr": [float(x) for x in clr_vec],
        "ilr": [float(x) for x in ilr_vec],
        "shannon_entropy": shannon_entropy(composition),
        "aitchison_norm": aitchison_norm(clr_vec),
        "aitchison_distance_step": (
            aitchison_distance(prev_clr, clr_vec) if prev_clr is not None else None
        ),
    }
    hs_scale = higgins_scale(composition)
    kappa = kappa_HS_full(composition)
    higgins = {
        "higgins_scale": hs_scale,
        "ring_class": ring_classify(hs_scale),
        "kappa_HS_full": kappa,
        "s_j_sensitivity": s_j_sensitivity(composition),
        "bearing_tensor": {"pairs": bearing_pairs(clr_vec, carriers)},
    }
    if prev_clr is not None:
        higgins["angular_velocity_deg"] = angular_velocity_deg(prev_clr, clr_vec)
        higgins["helmsman_local"] = helmsman_dcdi(prev_clr, clr_vec)
    else:
        higgins["angular_velocity_deg"] = None
        higgins["helmsman_local"] = None
    return {
        "index": int(t_index),
        "label": str(label) if label is not None else str(t_index),
        "raw_values": [float(x) for x in raw_values],
        "coda_standard": coda_standard,
        "higgins_extensions": higgins,
    }


def compute_tensor_block(
    rows: np.ndarray,
    rows_closed: np.ndarray,
    clr_matrix: np.ndarray,
    ilr_matrix: np.ndarray,
    carriers: Sequence[str],
    labels: Sequence[Any],
) -> Dict[str, Any]:
    T, D = rows.shape
    H = helmert_basis(D)
    timesteps = []
    prev_clr = None
    for t in range(T):
        entry = compute_timestep_block(
            t_index=t,
            label=labels[t],
            raw_values=rows[t],
            composition=rows_closed[t],
            clr_vec=clr_matrix[t],
            ilr_vec=ilr_matrix[t],
            carriers=carriers,
            prev_clr=prev_clr,
        )
        timesteps.append(entry)
        prev_clr = clr_matrix[t]
    return {
        "_function": "composer",
        "_description": (
            "Per-step compositional tensor: closure, CLR, ILR, kappa_HS_full "
            "(order-2), s_j_sensitivity (order-1), bearing pairs, and step-to-step "
            "angular velocity / helmsman local index."
        ),
        "helmert_basis": H.tolist(),
        "n_timesteps": int(T),
        "timesteps": timesteps,
    }


# ---------------------------------------------------------------------------
# Stage 1 / 2 / 3
# ---------------------------------------------------------------------------


def compute_stage1(clr_matrix: np.ndarray, carriers: Sequence[str]) -> Dict[str, Any]:
    h = np.asarray(clr_matrix, dtype=np.float64)
    T, D = h.shape
    sections = []
    for i, j in combinations(range(D), 2):
        sec = {
            "i": carriers[i],
            "j": carriers[j],
            "i_min": float(h[:, i].min()),
            "i_max": float(h[:, i].max()),
            "j_min": float(h[:, j].min()),
            "j_max": float(h[:, j].max()),
        }
        sections.append(sec)
    return {
        "_function": "review",
        "_description": "CLR-space pairwise (i, j) coordinate ranges across the trajectory.",
        "n_sections": len(sections),
        "sections": sections,
    }


def compute_stage2(
    rows_closed: np.ndarray,
    clr_matrix: np.ndarray,
    carriers: Sequence[str],
) -> Dict[str, Any]:
    rows = np.asarray(rows_closed, dtype=np.float64)
    h = np.asarray(clr_matrix, dtype=np.float64)
    T, D = rows.shape
    tau = variation_matrix(rows)
    pair_examinations = []
    for i, j in combinations(range(D), 2):
        ci = h[:, i]
        cj = h[:, j]
        std_i = float(np.std(ci, ddof=0))
        std_j = float(np.std(cj, ddof=0))
        if std_i < 1e-15 or std_j < 1e-15:
            r = 0.0
        else:
            r = float(np.corrcoef(ci, cj)[0, 1])
        bearings = np.degrees(np.arctan2(cj, ci))
        spread = float(bearings.max() - bearings.min())
        pair_examinations.append(
            {
                "i": carriers[i],
                "j": carriers[j],
                "pearson_r": r,
                "co_movement_score": max(0.0, r),
                "opposition_score": max(0.0, -r),
                "bearing_spread_deg": spread,
                "locked_pair": bool(spread < 10.0),
            }
        )
    return {
        "_function": "review",
        "_description": "Pairwise structure: variation matrix tau and per-pair correlations / bearing spread.",
        "variation_matrix": {"carriers": list(carriers), "tau": tau.tolist()},
        "carrier_pair_examination": pair_examinations,
    }


def compute_stage3(
    rows_closed: np.ndarray,
    clr_matrix: np.ndarray,
    carriers: Sequence[str],
    *,
    triadic_t_limit: int = TRIADIC_T_LIMIT,
    triadic_k: int = TRIADIC_K_DEFAULT,
    ladder_k_limit: int = LADDER_K_LIMIT,
) -> Dict[str, Any]:
    h = np.asarray(clr_matrix, dtype=np.float64)
    T, D = h.shape
    if T - 2 > triadic_t_limit:
        rng = np.random.default_rng(seed=42)
        sampled = sorted(rng.choice(T - 2, size=triadic_t_limit, replace=False).tolist())
        triadic_sampling = {
            "applied": True,
            "seed": 42,
            "sample_size": triadic_t_limit,
            "total_triads_available": T - 2,
        }
    else:
        sampled = list(range(max(T - 2, 0)))
        triadic_sampling = {"applied": False}
    triads = []
    for t in sampled:
        a = h[t]
        b = h[t + 1]
        c = h[t + 2]
        area = 0.5 * abs(
            (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
        )
        triads.append(
            {
                "t": int(t),
                "area": float(area),
                "sides": [
                    float(np.linalg.norm(b - a)),
                    float(np.linalg.norm(c - b)),
                    float(np.linalg.norm(c - a)),
                ],
            }
        )
    triads_sorted = sorted(triads, key=lambda x: x["area"], reverse=True)
    top_triads = triads_sorted[:triadic_k]
    ladder = []
    for k in range(2, D):
        all_subsets = list(combinations(range(D), k))
        n_total = len(all_subsets)
        scored = all_subsets[:ladder_k_limit] if n_total > ladder_k_limit else all_subsets
        correlations = []
        for subset in scored:
            sub_clr = h[:, list(subset)]
            sub_centred = sub_clr - sub_clr.mean(axis=0, keepdims=True)
            stds = sub_centred.std(axis=0, ddof=0)
            valid = stds > 1e-15
            if valid.sum() < 2:
                correlations.append(0.0)
                continue
            valid_sub = sub_centred[:, valid]
            corr_matrix = np.corrcoef(valid_sub, rowvar=False)
            n = corr_matrix.shape[0]
            mask = ~np.eye(n, dtype=bool)
            mean_corr = float(corr_matrix[mask].mean()) if mask.any() else 0.0
            correlations.append(mean_corr)
        ladder.append(
            {
                "degree": int(k),
                "n_subsets_total": n_total,
                "n_subsets_scored": len(scored),
                "mean_correlation": float(np.mean(correlations)) if correlations else 0.0,
            }
        )
    if T > 1:
        step_distances = np.linalg.norm(h[1:] - h[:-1], axis=1)
        if step_distances.size > 1:
            mean_d = float(step_distances.mean())
            std_d = float(step_distances.std(ddof=0))
            threshold = mean_d + 2.0 * std_d
            boundaries = np.where(step_distances > threshold)[0].tolist()
        else:
            threshold = 0.0
            boundaries = []
    else:
        threshold = 0.0
        boundaries = []
    return {
        "_function": "review",
        "_description": "Triadic areas, subcomposition ladder, regime-boundary detection.",
        "triadic_area": {
            "sampling": triadic_sampling,
            "n_kept": len(top_triads),
            "triads": top_triads,
        },
        "subcomposition_ladder": {
            "ladder_k_limit": ladder_k_limit,
            "entries": ladder,
        },
        "regime_detection": {
            "threshold": threshold,
            "n_boundaries": len(boundaries),
            "boundary_indices": [int(b) for b in boundaries],
        },
    }


# ---------------------------------------------------------------------------
# Depth tower
# ---------------------------------------------------------------------------


def compute_depth_tower(
    rows_closed: np.ndarray,
    clr_matrix: np.ndarray,
    *,
    max_levels: int = DEPTH_MAX_LEVELS,
    precision: float = DEPTH_PRECISION_TARGET,
) -> Dict[str, Any]:
    h = np.asarray(clr_matrix, dtype=np.float64)
    rows = np.asarray(rows_closed, dtype=np.float64)
    T, D = h.shape

    energy_levels: List[Dict[str, Any]] = []
    energy_traj = h.copy()
    for ell in range(max_levels):
        if energy_traj.shape[0] < 2:
            break
        deltas_sq = (energy_traj[1:] - energy_traj[:-1]) ** 2 + 1e-15
        row_sums = deltas_sq.sum(axis=1, keepdims=True)
        closed = deltas_sq / row_sums
        log_closed = np.log(closed)
        clr_next = log_closed - log_closed.mean(axis=1, keepdims=True)
        energy_levels.append(
            {
                "level": ell,
                "n_rows": int(closed.shape[0]),
                "norm_mean": float(np.linalg.norm(clr_next, axis=1).mean()),
            }
        )
        energy_traj = clr_next

    curvature_levels: List[Dict[str, Any]] = []
    curvature_traj = rows.copy()
    for ell in range(max_levels):
        if curvature_traj.shape[0] < 2:
            break
        inv_sq = 1.0 / (curvature_traj ** 2 + 1e-15)
        row_sums = inv_sq.sum(axis=1, keepdims=True)
        closed_curv = inv_sq / row_sums
        log_closed = np.log(closed_curv + 1e-30)
        clr_curv = log_closed - log_closed.mean(axis=1, keepdims=True)
        curvature_levels.append(
            {
                "level": ell,
                "n_rows": int(closed_curv.shape[0]),
                "norm_mean": float(np.linalg.norm(clr_curv, axis=1).mean()),
            }
        )
        curvature_traj = np.exp(clr_curv)
        curvature_traj = curvature_traj / curvature_traj.sum(axis=1, keepdims=True)
        if ell > 0 and abs(curvature_levels[-1]["norm_mean"] - curvature_levels[-2]["norm_mean"]) < precision:
            break

    attractor = fit_attractor(rows)

    if attractor.get("fitted") and attractor.get("period") == 2:
        termination_kind = "LIMIT_CYCLE_P2"
    elif energy_levels and energy_levels[-1]["norm_mean"] < precision:
        termination_kind = "FIXED_POINT"
    else:
        termination_kind = "EXHAUSTED"

    M_indices = sorted(set([0, T // 2, T - 1])) if T >= 1 else []
    involution_samples = []
    for t in M_indices:
        p = rows[t]
        m1 = 1.0 / (p + 1e-30)
        m1 = m1 / m1.sum()
        m2 = 1.0 / (m1 + 1e-30)
        m2 = m2 / m2.sum()
        involution_samples.append(
            {"t": int(t), "max_residual_linf": float(np.max(np.abs(m2 - p)))}
        )
    involution_max = max((s["max_residual_linf"] for s in involution_samples), default=0.0)

    A = float(attractor.get("amplitude_A") or 0.0)
    zeta = float(attractor.get("damping_zeta") or 0.0)
    if D == 2:
        ir_class = "D2_DEGENERATE"
    elif A < 0.1:
        ir_class = "CRITICALLY_DAMPED"
    elif abs(zeta) < 1e-6:
        ir_class = "UNDAMPED"
    elif 0 < zeta < 0.1:
        ir_class = "LIGHTLY_DAMPED"
    elif A > 0.7:
        ir_class = "OVERDAMPED_EXTREME"
    else:
        ir_class = "MODERATELY_DAMPED"

    return {
        "_function": "review",
        "_description": (
            "Depth-tower diagnostics: energy and curvature level trajectories, "
            "P2 attractor parameter fit, M^2=I metric involution sample, IR classification."
        ),
        "energy_levels": energy_levels,
        "curvature_levels": curvature_levels,
        "termination": {
            "kind": termination_kind,
            "level_index": len(energy_levels) - 1 if energy_levels else None,
            "period": attractor.get("period") if attractor.get("fitted") else None,
        },
        "attractor": attractor,
        "involution_M_squared": {
            "samples": involution_samples,
            "max_residual_overall": involution_max,
            "verified_at_ieee_floor": involution_max < 1e-10,
        },
        "ir_class": ir_class,
    }


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------


def detect_lock_events(clr_matrix: np.ndarray, threshold: float = LOCK_CLR_THRESHOLD) -> Dict[str, Any]:
    h = np.asarray(clr_matrix, dtype=np.float64)
    T = h.shape[0]
    locked = h.min(axis=1) < threshold
    n_degen = int(locked.sum())
    transitions = []
    in_lock = False
    for t in range(T):
        if locked[t] and not in_lock:
            transitions.append({"t": int(t), "kind": "LOCK-ACQ"})
            in_lock = True
        elif not locked[t] and in_lock:
            transitions.append({"t": int(t), "kind": "LOCK-LOSS"})
            in_lock = False
    return {
        "threshold_clr": threshold,
        "n_degen_timesteps": n_degen,
        "n_transitions": len(transitions),
        "transitions": transitions,
    }


def degeneracy_flags(rows_closed: np.ndarray) -> Dict[str, Any]:
    rows = np.asarray(rows_closed, dtype=np.float64)
    T, D = rows.shape
    flags = {
        "small_T": bool(T < 20),
        "small_D": bool(D < 3),
        "row_variance_below_threshold": bool(rows.std(axis=0).max() < 1e-6),
    }
    flags["any_flag_set"] = any(flags.values())
    return flags


def eitt_bench_test(
    rows_closed: np.ndarray,
    clr_matrix: np.ndarray,
    *,
    gate_pct: float = EITT_GATE_PCT,
    m_sweep: Sequence[int] = EITT_M_SWEEP_BASE,
) -> Dict[str, Any]:
    h = np.asarray(clr_matrix, dtype=np.float64)
    T = h.shape[0]
    results = []
    for M in m_sweep:
        if M >= T:
            results.append({"M": int(M), "skipped_reason": "M >= T"})
            continue
        seg_size = T // M
        seg_norms = []
        for s in range(M):
            seg = h[s * seg_size : (s + 1) * seg_size]
            if seg.shape[0] == 0:
                continue
            seg_norms.append(float(np.linalg.norm(seg, axis=1).mean()))
        if len(seg_norms) < 2:
            results.append({"M": int(M), "skipped_reason": "fewer than 2 segments"})
            continue
        arr = np.array(seg_norms)
        rel = float(arr.std(ddof=0) / (abs(arr.mean()) + 1e-15) * 100.0)
        results.append(
            {
                "M": int(M),
                "n_segments": len(seg_norms),
                "rel_variation_pct": rel,
                "pass_gate": bool(rel < gate_pct),
            }
        )
    return {"gate_pct": gate_pct, "m_sweep": list(m_sweep), "results": results}


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------


def ingest_csv(input_csv: Path) -> Tuple[List[Any], List[str], np.ndarray, int]:
    p = Path(input_csv)
    if not p.exists():
        raise FileNotFoundError(f"input CSV not found: {p}")
    with p.open("r", encoding="utf-8", errors="strict", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        if len(header) < 2:
            raise InvalidInputError(
                f"input CSV header must have at least 2 columns; got {len(header)}"
            )
        carrier_names = [str(c).strip() for c in header[1:]]
        labels: List[Any] = []
        rows_list: List[List[float]] = []
        zero_replacement_count = 0
        for line_no, row in enumerate(reader, start=2):
            if not row or all(not c.strip() for c in row):
                continue
            if len(row) != len(header):
                raise InvalidInputError(
                    f"input CSV line {line_no}: expected {len(header)} columns, got {len(row)}"
                )
            labels.append(row[0])
            try:
                vals = [float(x) for x in row[1:]]
            except ValueError as e:
                raise InvalidInputError(
                    f"input CSV line {line_no}: non-numeric carrier value: {e}"
                )
            for k, v in enumerate(vals):
                if v == 0.0:
                    vals[k] = DEFAULT_DELTA
                    zero_replacement_count += 1
            rows_list.append(vals)
    rows = np.asarray(rows_list, dtype=np.float64)
    if rows.size == 0:
        raise InvalidInputError(f"input CSV {p} contained no data rows")
    return labels, carrier_names, rows, zero_replacement_count


def get_environment_metadata(repo_root: Optional[Path] = None) -> Dict[str, Any]:
    git_sha = None
    if repo_root is not None:
        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0:
                git_sha = res.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            git_sha = None
    hostname_hash = hashlib.sha256(socket.gethostname().encode("utf-8")).hexdigest()[:16]
    return {
        "git_sha": git_sha,
        "python_version": sys.version.split()[0],
        "numpy_version": np.__version__,
        "platform": platform.platform(),
        "hostname_hash": hostname_hash,
    }


def closed_data_sha256(rows_closed: np.ndarray) -> str:
    arr = np.ascontiguousarray(rows_closed, dtype=np.float64)
    return hashlib.sha256(arr.tobytes()).hexdigest()


# ---------------------------------------------------------------------------
# Top-level orchestration
# ---------------------------------------------------------------------------


def cnt_run(
    input_csv: Path,
    *,
    out_path: Optional[Path] = None,
    repo_root: Optional[Path] = None,
    engine_config_overrides: Optional[Dict[str, Any]] = None,
    ordering: str = "as_provided",
) -> Dict[str, Any]:
    t0 = time.monotonic()
    overrides = dict(engine_config_overrides or {})

    labels, carrier_names, rows, zero_replacement_count = ingest_csv(Path(input_csv))
    rows = validate_rows(rows, min_carriers=2)
    T, D = rows.shape

    rows_closed = _shared_closure(rows)
    clr_matrix = _shared_clr(rows_closed)
    ilr_matrix, _radii = compositions_to_ilr(rows, D=D)

    tensor_block = compute_tensor_block(
        rows=rows, rows_closed=rows_closed, clr_matrix=clr_matrix,
        ilr_matrix=ilr_matrix, carriers=carrier_names, labels=labels,
    )
    stage1 = compute_stage1(clr_matrix, carrier_names)
    stage2 = compute_stage2(rows_closed, clr_matrix, carrier_names)
    stage3 = compute_stage3(rows_closed, clr_matrix, carrier_names)
    depth_tower = compute_depth_tower(rows_closed, clr_matrix)
    helmsman = compute_helmsman_family(rows, window=HELMSMAN_ROLLING_WINDOW)

    eitt = eitt_bench_test(rows_closed, clr_matrix)
    locks = detect_lock_events(clr_matrix)
    degens = degeneracy_flags(rows_closed)

    source_file_hash = file_sha256(Path(input_csv))
    closed_hash = closed_data_sha256(rows_closed)

    wall_clock_ms = int((time.monotonic() - t0) * 1000.0)
    env = get_environment_metadata(repo_root=repo_root)

    payload: Dict[str, Any] = {
        "metadata": {
            "engine": ENGINE_NAME,
            "engine_version": ENGINE_VERSION,
            "schema_version": SCHEMA_VERSION,
            "engine_implementation": "python",
            "implementation_lang_version": f"Python {sys.version.split()[0]}",
            "principle": ENGINE_PRINCIPLE,
            "engine_config": {
                "active_overrides": overrides,
                "defaults_in_use": {
                    "DEFAULT_DELTA": DEFAULT_DELTA,
                    "TRIADIC_T_LIMIT": TRIADIC_T_LIMIT,
                    "TRIADIC_K_DEFAULT": TRIADIC_K_DEFAULT,
                    "LADDER_K_LIMIT": LADDER_K_LIMIT,
                    "DEPTH_MAX_LEVELS": DEPTH_MAX_LEVELS,
                    "DEPTH_PRECISION_TARGET": DEPTH_PRECISION_TARGET,
                    "EITT_GATE_PCT": EITT_GATE_PCT,
                    "EITT_M_SWEEP_BASE": list(EITT_M_SWEEP_BASE),
                    "HELMSMAN_ROLLING_WINDOW": HELMSMAN_ROLLING_WINDOW,
                },
            },
            "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "wall_clock_ms": wall_clock_ms,
            "environment": env,
        },
        "input": {
            "source_file": str(input_csv),
            "source_file_sha256": source_file_hash,
            "closed_data_sha256": closed_hash,
            "n_records": int(T),
            "n_carriers": int(D),
            "carriers": list(carrier_names),
            "labels": [str(label) for label in labels],
            "rows_closed": rows_closed.tolist(),
            "zero_replacement_count": int(zero_replacement_count),
            "ordering": ordering,
        },
        "tensor": tensor_block,
        "stages": {"stage1": stage1, "stage2": stage2, "stage3": stage3},
        "depth_tower": depth_tower,
        "helmsman_family": helmsman,
        "diagnostics": {
            "eitt": eitt,
            "lock_events": locks,
            "degeneracy_flags": degens,
        },
    }

    digest = canonical_sha256(payload)
    payload["diagnostics"]["cnt_content_sha256"] = digest

    if out_path is not None:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with Path(out_path).open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    return payload


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="hs-cnt",
        description=f"{ENGINE_NAME} v{ENGINE_VERSION} compositional navigation tensor engine",
    )
    p.add_argument("input", type=str, help="Path to input CSV")
    p.add_argument("-o", "--output", type=str, default=None, help="Output JSON path")
    p.add_argument("--repo-root", type=str, default=None)
    p.add_argument("--ordering", type=str, default="as_provided")
    p.add_argument("--version", action="version", version=f"{ENGINE_NAME} v{ENGINE_VERSION} (schema {SCHEMA_VERSION})")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    repo_root = Path(args.repo_root) if args.repo_root else None
    out_path = Path(args.output) if args.output else None
    payload = cnt_run(Path(args.input), out_path=out_path, repo_root=repo_root, ordering=args.ordering)
    md = payload["metadata"]
    inp = payload["input"]
    dt = payload["depth_tower"]
    diag = payload["diagnostics"]
    print(f"engine             = {md['engine']} v{md['engine_version']} (schema {md['schema_version']})")
    print(f"input              = {inp['source_file']}")
    print(f"T x D              = {inp['n_records']} x {inp['n_carriers']}")
    print(f"depth_termination  = {dt['termination']['kind']}")
    print(f"ir_class           = {dt['ir_class']}")
    print(f"M^2=I residual_max = {dt['involution_M_squared']['max_residual_overall']:.3e}")
    if dt["attractor"].get("fitted"):
        print(f"attractor.period   = {dt['attractor']['period']}")
        print(f"attractor.stability= {dt['attractor']['period_stability']:.3f}")
    print(f"helmsman.flips     = {payload['helmsman_family']['flips']['total']}")
    print(f"cnt_content_sha256 = {diag['cnt_content_sha256']}")
    if out_path:
        print(f"written            = {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
me__ == "__main__":
    sys.exit(main())
