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
ENGINE_VERSION: str = "3.2.0"
SCHEMA_VERSION: str = "3.2.0"
# v3.2.0 (2026-05-19): added navigation_2d block — ILR-Helmert PCA 2-D
#   barycenter trajectory, scaled to unit disk for downstream visualisation.
#   Backwards-compatible: all v3.1.0 fields unchanged. Conference (CoDaWork
#   2026) data was generated with v3.1.0 and is NOT regenerated on this bump.
#   Reference: regen_baryxy.py for the sidecar implementation that produces
#   the same navigation_2d payload from v3.1.0 JSONs without re-running the
#   full pipeline.
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


# -----------------------------------------------------------------------------
# Navigation concentration family (schema v3.1.0, push #37)
# -----------------------------------------------------------------------------
# These quantities were promoted into the canonical engine output during
# CoDaWork 2026 preparation. The HUF MC-4 submission packet used TV distance
# (half-L1) and K_eff (= exp(Shannon H)) as the operational metric stack
# alongside Aitchison distance + Shannon entropy. The CoDa-canonical and
# packet-operational stacks both have legitimate uses, and both should travel
# with every deterministic CNT run.
#
# See: docs/SCHEMA_v3_1_0_navigation_concentration_family.md (TBD), and
# papers/codawork2026/planning/ABSTRACT_TO_CNT_V3_MAP.md for the abstract-to-
# field mapping.


def tv_distance(p_a: np.ndarray, p_b: np.ndarray) -> float:
    """Total variation distance between two closed compositions on the simplex.

    TV(p, q) = (1/2) * sum_i |p_i - q_i|    (half-L1 norm)

    Bounded [0, 1] for probability vectors. Distinct from Aitchison distance
    (which is log-ratio Euclidean); the two metrics agree on hit/miss verdicts
    but the magnitudes differ.

    The packet's Appendix A documents the L2 -> TV metric correction caught
    during external review March 22, 2026. Both metrics now travel with every
    CNT v3.1+ run for explicit metric robustness.
    """
    a = np.asarray(p_a, dtype=np.float64)
    b = np.asarray(p_b, dtype=np.float64)
    return float(0.5 * np.sum(np.abs(a - b)))


def k_eff(p: np.ndarray) -> float:
    """Effective number of categories: K_eff = exp(Shannon entropy).

    Range: [1, D]. K_eff = 1 means single-carrier dominance; K_eff = D means
    equal distribution across all carriers. This is a deterministic
    one-to-one view-transform of Shannon entropy on the closed composition.
    Some communities (notably CoDa) prefer K_eff for unit interpretability;
    others prefer raw entropy for additive composition.
    """
    return float(np.exp(shannon_entropy(p)))


def _concentration_regime_tag(
    k_eff_yoy: Optional[float],
    tv_step: Optional[float],
    tv_median: Optional[float],
) -> Optional[str]:
    """Qualitative tag for the step's concentration regime.

    Returns one of:
        "tightening"  : K_eff is declining (concentration increasing)
        "loosening"   : K_eff is rising (concentration decreasing)
        "deceptive"   : K_eff is declining (tightening) AND TV is below series
                         median — the packet's "deceptive drift" signature:
                         concentration accumulating while step-to-step composition
                         movement stays quiet.
        "stable"      : K_eff change is small relative to threshold
        None          : insufficient data (first step, or no median yet)
    """
    if k_eff_yoy is None:
        return None
    THRESHOLD = 0.05  # the packet's K_eff_yoy decline threshold magnitude
    if k_eff_yoy < -THRESHOLD:
        if tv_step is not None and tv_median is not None and tv_step <= tv_median:
            return "deceptive"
        return "tightening"
    if k_eff_yoy > THRESHOLD:
        return "loosening"
    return "stable"


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
    _prev_comp_for_tv: Optional[np.ndarray] = None,
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
    # Navigation concentration family (schema v3.1.0, push #37 promotion).
    # Per-step values; YoY/acceleration/regime fields are filled in pass 2
    # by compute_tensor_block.
    navigation_concentration = {
        "k_eff": k_eff(composition),
        "k_eff_yoy_change": None,           # filled in pass 2
        "tv_distance_step": (
            tv_distance(_prev_comp_for_tv, composition)
            if _prev_comp_for_tv is not None else None
        ),
        "tv_acceleration": None,            # filled in pass 2
        "concentration_regime": None,       # filled in pass 2 (needs series median)
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
        "navigation_concentration_family": navigation_concentration,
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
    prev_comp_for_tv: Optional[np.ndarray] = None
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
            _prev_comp_for_tv=prev_comp_for_tv,
        )
        timesteps.append(entry)
        prev_clr = clr_matrix[t]
        prev_comp_for_tv = rows_closed[t]

    # PASS 2: navigation_concentration_family — fill in K_eff YoY change,
    # TV acceleration, and concentration regime (needs series TV median).
    tv_series = [ts["navigation_concentration_family"]["tv_distance_step"] for ts in timesteps]
    valid_tv = [v for v in tv_series if v is not None]
    tv_median = float(np.median(valid_tv)) if valid_tv else None

    for i, ts in enumerate(timesteps):
        ncf = ts["navigation_concentration_family"]
        # K_eff YoY change: difference from previous step's K_eff
        if i > 0:
            ncf["k_eff_yoy_change"] = (
                ts["navigation_concentration_family"]["k_eff"]
                - timesteps[i - 1]["navigation_concentration_family"]["k_eff"]
            )
        # TV acceleration: difference from previous step's TV
        if i > 0 and tv_series[i] is not None and tv_series[i - 1] is not None:
            ncf["tv_acceleration"] = tv_series[i] - tv_series[i - 1]
        # Concentration regime tag (uses K_eff YoY threshold + TV series median)
        ncf["concentration_regime"] = _concentration_regime_tag(
            ncf["k_eff_yoy_change"], ncf["tv_distance_step"], tv_median
        )
    # Series-level navigation_concentration_family summary (schema v3.1.0)
    keff_series = [ts["navigation_concentration_family"]["k_eff"] for ts in timesteps]
    nav_conc_summary: Dict[str, Any] = {
        "_description": (
            "Series-level summary of the navigation concentration family "
            "(K_eff + TV distance + regime tags). Promoted from runner-side "
            "packet_operators.py into the canonical engine at schema v3.1.0 "
            "(HUF MC-4 packet operators)."
        ),
        "k_eff": {
            "min": float(min(keff_series)),
            "max": float(max(keff_series)),
            "mean": float(sum(keff_series) / len(keff_series)),
            "final": float(keff_series[-1]),
        },
        "tv_distance_step": {
            "min": float(min(valid_tv)) if valid_tv else None,
            "max": float(max(valid_tv)) if valid_tv else None,
            "mean": float(sum(valid_tv) / len(valid_tv)) if valid_tv else None,
            "median": tv_median,
            "n_steps": len(valid_tv),
        },
        "regime_counts": {
            tag: sum(
                1 for ts in timesteps
                if ts["navigation_concentration_family"]["concentration_regime"] == tag
            ) for tag in ("tightening", "loosening", "deceptive", "stable")
        },
    }
    return {
        "_function": "composer",
        "_description": (
            "Per-step compositional tensor: closure, CLR, ILR, kappa_HS_full "
            "(order-2), s_j_sensitivity (order-1), bearing pairs, and step-to-step "
            "angular velocity / helmsman local index. Schema v3.1.0 adds "
            "navigation_concentration_family per timestep (K_eff, TV distance, "
            "K_eff YoY, TV acceleration, concentration regime tag)."
        ),
        "helmert_basis": H.tolist(),
        "n_timesteps": int(T),
        "navigation_concentration_summary": nav_conc_summary,
        "timesteps": timesteps,
    }


# ---------------------------------------------------------------------------
# Schema v3.2.0 navigation_2d  —  ILR-Helmert PCA barycenter trajectory
# ---------------------------------------------------------------------------
# 2-D projection of the centred ILR trajectory onto its top two principal
# directions. Produces a disk-scaled (bary_xy ∈ [-0.85, +0.85]) per-timestep
# coordinate consumable by downstream visualisations (the CoDaWork 2026
# manifold projector reads exactly this block). Variance captured by PC1+PC2
# is reported so the consumer can warn when the 2-D projection is lossy.
#
# Math:
#   ILR(t)  = V^T · CLR(t)                     # (T x (D-1)) trajectory
#   X       = ILR − mean_t ILR                 # centred
#   PC1,PC2 = top-2 eigenvectors of (X^T X)/(T-1)
#   pc_t    = (X[t] · PC1, X[t] · PC2)
#   bary_xy[t] = pc_t / max_t ‖pc_t‖ · 0.85    # disk-scaled
#
# Backwards-compat: this block is additive to v3.1.0; CoDaWork 2026 data was
# produced under v3.1.0 and is not regenerated for the conference.


def compute_navigation_2d(ilr_matrix: np.ndarray) -> Dict[str, Any]:
    """Project the ILR trajectory onto its top-2 PCA directions and return a
    disk-scaled 2-D barycenter trajectory plus diagnostic metadata."""
    X = np.asarray(ilr_matrix, dtype=np.float64)
    T, K = X.shape
    mu = X.mean(axis=0)
    Xc = X - mu
    if T < 2 or K < 2:
        # Degenerate trajectory — return zero barycenter, no PCA.
        return {
            "_function": "review",
            "_description": (
                "Schema v3.2.0 ILR-Helmert PCA barycenter trajectory; degenerate "
                "(T<2 or K<2), returning zeros."
            ),
            "pc1_direction": [0.0] * K,
            "pc2_direction": [0.0] * K,
            "variance_explained": [0.0, 0.0],
            "max_radius_pre_scale": 0.0,
            "disk_scale_factor": 0.85,
            "bary_xy": [[0.0, 0.0] for _ in range(T)],
        }
    cov = (Xc.T @ Xc) / max(T - 1, 1)
    eigvals, eigvecs = np.linalg.eigh(cov)  # ascending
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]
    pc1 = eigvecs[:, 0]
    pc2 = eigvecs[:, 1] if K >= 2 else np.zeros(K)
    total = float(np.clip(eigvals, 0.0, None).sum())
    ve = [
        float(eigvals[0] / total) if total > 0 else 0.0,
        float(eigvals[1] / total) if (total > 0 and K >= 2) else 0.0,
    ]
    p1_scores = Xc @ pc1
    p2_scores = Xc @ pc2
    raw = np.stack([p1_scores, p2_scores], axis=1)
    max_r = float(np.linalg.norm(raw, axis=1).max())
    if max_r > 0:
        scaled = (raw / max_r * 0.85).tolist()
    else:
        scaled = [[0.0, 0.0] for _ in range(T)]
    return {
        "_function": "review",
        "_description": (
            "Schema v3.2.0 ILR-Helmert PCA barycenter trajectory, scaled to "
            "the unit disk for visualisation. pc1_direction / pc2_direction "
            "are unit vectors in (D-1)-dim ILR space; bary_xy[t] is the "
            "(pc1, pc2) projection of the centred ILR coordinate at time t, "
            "scaled so the most extreme step sits at radius 0.85 of the disk."
        ),
        "pc1_direction": pc1.tolist(),
        "pc2_direction": pc2.tolist(),
        "variance_explained": ve,
        "max_radius_pre_scale": max_r,
        "disk_scale_factor": 0.85,
        "bary_xy": [[round(float(p[0]), 6), round(float(p[1]), 6)] for p in scaled],
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
                timeout=10,
            )
            if res.returncode == 0:
                git_sha = res.stdout.strip()
        except Exception:
            git_sha = None
    hostname_hash = hashlib.sha256(socket.gethostname().encode("utf-8")).hexdigest()[:16]
    return {
        "git_sha": git_sha,
        "python_version": sys.version.split()[0],
        "numpy_version": np.__version__,
        "platform": platform.platform(),
        "hostname_hash": hostname_hash,
    }


# ---------------------------------------------------------------------------
# Top-level run + CLI
# ---------------------------------------------------------------------------


def cnt_run(input_csv, out_path: Optional[Path] = None) -> Dict[str, Any]:
    """Run the full CNT v3 pipeline on a single CSV; return the canonical
    payload dict and (optionally) write it to disk as JSON.

    Schema v3.1.0 (push #37) adds the navigation_concentration_family per
    timestep (K_eff, TV distance, K_eff YoY, TV acceleration, concentration
    regime tag) plus a series-level summary at tensor.navigation_concentration_summary.
    """
    t0 = time.monotonic()
    input_csv = Path(input_csv)
    labels, carriers, rows, zero_replacement_count = ingest_csv(input_csv)
    validate_rows(rows)
    rows_closed = _shared_closure(rows)
    clr_matrix = _shared_clr(rows_closed)
    H = helmert_basis(rows.shape[1])
    ilr_matrix = clr_matrix @ H.T

    tensor_block = compute_tensor_block(
        rows, rows_closed, clr_matrix, ilr_matrix, carriers, labels
    )
    stage1 = compute_stage1(clr_matrix, carriers)
    stage2 = compute_stage2(rows_closed, clr_matrix, carriers)
    stage3 = compute_stage3(rows_closed, clr_matrix, carriers)
    navigation_2d = compute_navigation_2d(ilr_matrix)  # v3.2.0 addition
    depth_tower = compute_depth_tower(rows_closed, clr_matrix)
    helmsman = compute_helmsman_family(rows, window=HELMSMAN_ROLLING_WINDOW)
    attractor = fit_attractor(rows_closed)
    eitt = eitt_bench_test(rows_closed, clr_matrix)
    locks = detect_lock_events(clr_matrix)
    degens = degeneracy_flags(rows_closed)

    source_hash = file_sha256(input_csv)
    closed_hash = canonical_sha256({"rows_closed": rows_closed.tolist()})
    wall_clock_ms = int(round((time.monotonic() - t0) * 1000))

    payload: Dict[str, Any] = {
        "metadata": {
            "engine": ENGINE_NAME,
            "engine_version": ENGINE_VERSION,
            "schema_version": SCHEMA_VERSION,
            "engine_implementation": "python",
            "implementation_lang_version": f"Python {sys.version.split()[0]}",
            "principle": ENGINE_PRINCIPLE,
            "engine_config": {
                "default_delta": DEFAULT_DELTA,
                "degen_threshold": DEGEN_THRESHOLD,
                "lock_clr_threshold": LOCK_CLR_THRESHOLD,
                "depth_max_levels": DEPTH_MAX_LEVELS,
                "depth_precision_target": DEPTH_PRECISION_TARGET,
                "triadic_t_limit": TRIADIC_T_LIMIT,
                "triadic_k_default": TRIADIC_K_DEFAULT,
                "ladder_k_limit": LADDER_K_LIMIT,
                "eitt_gate_pct": EITT_GATE_PCT,
                "eitt_m_sweep_base": list(EITT_M_SWEEP_BASE),
                "helmsman_rolling_window": HELMSMAN_ROLLING_WINDOW,
            },
            "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "wall_clock_ms": wall_clock_ms,
            "environment": get_environment_metadata(repo_root=_THIS_FILE.parent.parent.parent),
        },
        "input": {
            "source_file": str(input_csv),
            "source_file_sha256": source_hash,
            "closed_data_sha256": closed_hash,
            "n_records": int(rows.shape[0]),
            "n_carriers": int(rows.shape[1]),
            "carriers": list(carriers),
            "labels": list(labels),
            "rows_closed": rows_closed.tolist(),
            "zero_replacement_count": int(zero_replacement_count),
            "ordering": "as_provided",
        },
        "tensor": tensor_block,
        "stages": {"stage1": stage1, "stage2": stage2, "stage3": stage3},
        "navigation_2d": navigation_2d,
        "depth_tower": depth_tower,
        "helmsman_family": helmsman,
        "attractor_fit": attractor,
        "diagnostics": {
            "eitt": eitt,
            "lock_events": locks,
            "degeneracy_flags": degens,
        },
    }
    # Content hash: canonical SHA-256 over the payload sans the hash field itself.
    content_sha = canonical_sha256(payload)
    payload["diagnostics"]["cnt_content_sha256"] = content_sha

    if out_path is not None:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return payload


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description=f"{ENGINE_NAME} v{ENGINE_VERSION} compositional navigation tensor engine",
    )
    p.add_argument("input_csv", type=Path, help="Path to input CSV (rows x carriers).")
    p.add_argument("-o", "--out", type=Path, default=None, help="Optional output JSON path.")
    p.add_argument("--version", action="version", version=f"{ENGINE_NAME} v{ENGINE_VERSION} (schema {SCHEMA_VERSION})")
    args = p.parse_args(argv)
    payload = cnt_run(args.input_csv, out_path=args.out)
    md = payload["metadata"]
    print(f"engine             = {md['engine']} v{md['engine_version']} (schema {md['schema_version']})")
    print(f"input              = {payload['input']['source_file']}")
    print(f"T x D              = {payload['input']['n_records']} x {payload['input']['n_carriers']}")
    print(f"termination        = {payload['depth_tower']['termination']['kind']}")
    print(f"ir_class           = {payload['depth_tower']['ir_class']}")
    print(f"helmsman.flips     = {payload['helmsman_family']['flips']['total']}")
    print(f"cnt_content_sha256 = {payload['diagnostics']['cnt_content_sha256']}")
    if args.out is not None:
        print(f"output             = {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
