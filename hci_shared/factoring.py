"""
hci_shared.factoring — twin-quaternion (D=8), quad-quaternion (D=16),
and CHSH joint coherence diagnostic

INV-029 (twin-quaternion factoring) graduates from DEFERRED scaffolding
to load-bearing CANONICAL with this module (push #32). INV-035 (CHSH
coherence diagnostic) graduates the same way. INV-043 (quad-quaternion
factoring at D=16) is schema-locked here for v2.1 implementation when
the first D=16 dataset lands.

Twin-quaternion factoring at D=8:

    The 7-dim ILR space is partitioned into two 3-dim subspaces (factor A
    and factor B) plus an optional 1-dim residual (common-mode axis). Each
    factor's 3-dim trajectory carries its own per-step quaternion path via
    the standard sandwich product. The coupling angle rho_AB(t) is the
    angle between q_A(t) and q_B(t) per step — small values indicate the
    two factors rotate in lockstep (tightly coupled), large values
    indicate independent rotation (decoupled).

Default partition for D=8:
    factor_A      = ILR axes [0, 1, 2]
    factor_B      = ILR axes [3, 4, 5]
    residual axis = ILR axis 6

Quad-quaternion factoring at D=16:

    The 15-dim ILR space partitions into four 3-dim subspaces plus an
    optional 3-dim residual. Each factor produces a per-step quaternion;
    six pairwise coupling angles (rho_AB, rho_AC, rho_AD, rho_BC, rho_BD,
    rho_CD) plus a 4-way joint coherence score characterise the bundle.
    Schema-locked here; full implementation in CNQ v2.1.

CHSH joint coherence diagnostic (INV-035):

    For two trajectories of unit quaternions (q_A(t), q_B(t)), CHSH measures
    whether the joint sign correlations across Tsirelson-aligned directions
    exceed the classical-additive bound 2.0. The classical bound 2.0 is
    saturated when q_A and q_B are independent random rotations; the
    Tsirelson bound 2*sqrt(2) ≈ 2.828 is the theoretical maximum for any
    physical correlation. S-values between 2.0 and 2.828 indicate
    structural coupling beyond classical bounds.

The interpretation of these channels in any specific domain (audio
perceptual unity at the auditory cortex, financial cross-asset coherence,
geochemical source-rock unity) lives in domain wrappers, not in this
module.
"""

from __future__ import annotations

import math
from typing import Optional, Sequence

import numpy as np

from hci_shared.geometry import (
    compositions_to_ilr,
    quat_rotate,
    quaternion_sandwich_residuals,
    rotation_quaternion_between,
)
from hci_shared.validation import (
    InvalidInputError,
    validate_partition,
    validate_rows,
)


# Tsirelson bound = 2 * sqrt(2). Locked at module level for clarity.
CLASSICAL_BOUND = 2.0
TSIRELSON_BOUND = 2.0 * math.sqrt(2.0)


# ---------------------------------------------------------------------------
# Twin-quaternion factoring (D=8 native)
# ---------------------------------------------------------------------------


def twin_quaternion_factor(
    rows: np.ndarray,
    *,
    partition_A: Sequence[int] = (0, 1, 2),
    partition_B: Sequence[int] = (3, 4, 5),
    residual_axis: Optional[int] = 6,
) -> dict:
    """Twin-quaternion factoring of a D=8 compositional trajectory.

    Splits the 7-dim ILR trajectory into two 3-dim subspaces (factor A on
    axes partition_A, factor B on axes partition_B), computes per-step
    rotation quaternions on each subspace's unit-vector trajectory, and
    reports the coupling angle rho_AB(t) between the two quaternion paths.

    Parameters
    ----------
    rows : array-like
        Compositional rows, shape (T, 8), strictly positive.
    partition_A : sequence of 3 ints, default (0, 1, 2)
        ILR axis indices for factor A. Must be 3 indices in [0, 6].
    partition_B : sequence of 3 ints, default (3, 4, 5)
        ILR axis indices for factor B. Must be 3 indices in [0, 6].
    residual_axis : int or None, default 6
        ILR axis index for the residual / common-mode trajectory. Set to
        None to skip residual reporting. Must be different from any axis
        in partition_A or partition_B.

    Returns
    -------
    dict
        See twin_quaternion_factoring schema in
        ai-refresh/CNT_V3_CNQ_V2_DESIGN.md §5.4.

    Raises
    ------
    InvalidInputError
        If the trajectory is not D=8, if partitions overlap, if any axis
        index is out of range, or if rows fail validation.
    """

    rows_validated = validate_rows(rows, min_carriers=8, max_carriers=8)
    T = rows_validated.shape[0]

    # Validate partitions.
    pa = validate_partition(partition_A, D=8, name="partition_A")
    pb = validate_partition(partition_B, D=8, name="partition_B")

    if len(pa) != 3 or len(pb) != 3:
        raise InvalidInputError(
            f"twin_quaternion_factor: partition_A and partition_B must each "
            f"contain exactly 3 ILR axes; got len(partition_A)={len(pa)}, "
            f"len(partition_B)={len(pb)}"
        )

    overlap = set(pa) & set(pb)
    if overlap:
        raise InvalidInputError(
            f"twin_quaternion_factor: partition_A and partition_B overlap "
            f"on axes {sorted(overlap)}"
        )

    if residual_axis is not None:
        if residual_axis < 0 or residual_axis > 6:
            raise InvalidInputError(
                f"twin_quaternion_factor: residual_axis {residual_axis} out "
                f"of range [0, 6]"
            )
        if residual_axis in pa or residual_axis in pb:
            raise InvalidInputError(
                f"twin_quaternion_factor: residual_axis {residual_axis} "
                f"conflicts with partition_A or partition_B"
            )

    # Compute full ILR trajectory; D=8 -> ILR is (T, 7).
    ilr, radii = compositions_to_ilr(rows_validated, D=8)

    # Extract factor A and factor B subspaces as (T, 3) arrays.
    sub_A = ilr[:, list(pa)]  # (T, 3)
    sub_B = ilr[:, list(pb)]  # (T, 3)

    # Normalise to unit vectors (with zero-radius guard).
    units_A, radii_A = _to_unit_vectors_3d(sub_A)
    units_B, radii_B = _to_unit_vectors_3d(sub_B)

    # Per-step quaternion sandwich residuals on each factor.
    res_A, quats_A, angles_A = quaternion_sandwich_residuals(units_A)
    res_B, quats_B, angles_B = quaternion_sandwich_residuals(units_B)

    # Coupling angle rho_AB(t) = angular distance between q_A(t) and q_B(t).
    # For unit quaternions, the angular distance is 2 * arccos(|q_A . q_B|).
    rho_AB = _quaternion_angular_distance(quats_A, quats_B)

    # Coupling summary.
    if rho_AB.size > 0:
        rho_summary = {
            "min": float(rho_AB.min()),
            "max": float(rho_AB.max()),
            "mean": float(rho_AB.mean()),
            "median": float(np.median(rho_AB)),
            "std": float(rho_AB.std(ddof=0)),
        }
    else:
        rho_summary = {
            "min": None,
            "max": None,
            "mean": None,
            "median": None,
            "std": None,
        }

    # Coherence class from mean rho_AB.
    if rho_AB.size == 0:
        coherence_class = "indeterminate"
    elif rho_summary["mean"] < 0.2:
        coherence_class = "tightly_coupled"
    elif rho_summary["mean"] < 0.5:
        coherence_class = "loosely_coupled"
    else:
        coherence_class = "decoupled"

    # Per-step ledger.
    per_step_A = _build_per_step_ledger(res_A, quats_A, angles_A)
    per_step_B = _build_per_step_ledger(res_B, quats_B, angles_B)

    factor_A_block = {
        "partition_axes": list(pa),
        "per_step": per_step_A,
        "max_residual": float(res_A.max()) if res_A.size > 0 else None,
        "mean_residual": float(res_A.mean()) if res_A.size > 0 else None,
        "mean_angle": float(angles_A.mean()) if angles_A.size > 0 else None,
        "radii": {
            "min": float(radii_A.min()) if T > 0 else None,
            "max": float(radii_A.max()) if T > 0 else None,
            "mean": float(radii_A.mean()) if T > 0 else None,
        },
    }

    factor_B_block = {
        "partition_axes": list(pb),
        "per_step": per_step_B,
        "max_residual": float(res_B.max()) if res_B.size > 0 else None,
        "mean_residual": float(res_B.mean()) if res_B.size > 0 else None,
        "mean_angle": float(angles_B.mean()) if angles_B.size > 0 else None,
        "radii": {
            "min": float(radii_B.min()) if T > 0 else None,
            "max": float(radii_B.max()) if T > 0 else None,
            "mean": float(radii_B.mean()) if T > 0 else None,
        },
    }

    out = {
        "enabled": True,
        "partition": {
            "factor_A": list(pa),
            "factor_B": list(pb),
            "residual_axis": residual_axis,
        },
        "factor_A": factor_A_block,
        "factor_B": factor_B_block,
        "coupling": {
            "rho_AB_per_step": [float(x) for x in rho_AB],
            "rho_AB_summary": rho_summary,
            "coherence_class": coherence_class,
        },
    }

    if residual_axis is not None:
        residual_series = ilr[:, residual_axis]
        out["residual"] = {
            "axis": residual_axis,
            "per_step": [float(x) for x in residual_series],
            "summary": {
                "min": float(residual_series.min()),
                "max": float(residual_series.max()),
                "mean": float(residual_series.mean()),
                "std": float(residual_series.std(ddof=0)),
            },
        }
    else:
        out["residual"] = None

    return out


# ---------------------------------------------------------------------------
# Quad-quaternion factoring (D=16, schema-locked, scaffold)
# ---------------------------------------------------------------------------


def quad_quaternion_factor(
    rows: np.ndarray,
    *,
    partitions: Optional[Sequence[Sequence[int]]] = None,
    residual_axes: Optional[Sequence[int]] = None,
) -> dict:
    """Quad-quaternion factoring of a D=16 compositional trajectory.

    Schema-locked scaffold for INV-043. Currently raises NotImplementedError
    when called; full implementation is queued for CNQ v2.1 once the first
    D=16 dataset lands and exercises the algorithm. The schema returned by
    a future implementation is documented in
    ai-refresh/CNT_V3_CNQ_V2_DESIGN.md §5.2.

    Default partition for D=16 (15-dim ILR):
        factor_A     = ILR axes [0, 1, 2]
        factor_B     = ILR axes [3, 4, 5]
        factor_C     = ILR axes [6, 7, 8]
        factor_D     = ILR axes [9, 10, 11]
        residuals    = ILR axes [12, 13, 14]

    Returns
    -------
    dict
        Currently raises NotImplementedError. When implemented, returns a
        block matching the quad_quaternion_factoring schema.

    Raises
    ------
    NotImplementedError
        Always (v2.0.0). Implementation is gated on first D=16 dataset.
    """

    raise NotImplementedError(
        "quad_quaternion_factor: D=16 implementation is gated on the first "
        "D=16 dataset (INV-043). Schema is locked in CNT_V3_CNQ_V2_DESIGN.md "
        "§5.2; v2.1 will implement when a real D=16 trajectory lands."
    )


# ---------------------------------------------------------------------------
# CHSH joint coherence diagnostic (INV-035)
# ---------------------------------------------------------------------------


def chsh_S_value(
    quats_A: np.ndarray,
    quats_B: np.ndarray,
    *,
    angle_offset_a: float = 0.0,
    angle_offset_b: float = math.pi / 4.0,
) -> dict:
    """CHSH joint coherence diagnostic on a pair of quaternion trajectories.

    For each pair (q_A(t), q_B(t)) of unit quaternions over t, project each
    quaternion's vector part onto two analyzer axes per side (a, a' for
    q_A; b, b' for q_B). The CHSH S-value is

        S = | E(a, b) + E(a, b') + E(a', b) - E(a', b') |

    where E(x, y) = mean over t of [sign(q_A(t).vec . x) * sign(q_B(t).vec . y)].

    The classical bound is 2.0 (saturated by independent random rotations).
    The Tsirelson bound is 2*sqrt(2) ≈ 2.828 (theoretical maximum). S
    values exceeding 2.828 indicate either an engine bug or a measurement
    error violating the CHSH inequality framework.

    Default analyzer axes use the canonical Tsirelson alignment:
        a   = (cos(angle_offset_a),         sin(angle_offset_a),         0)
        a'  = (cos(angle_offset_a + pi/2),  sin(angle_offset_a + pi/2),  0)
        b   = (cos(angle_offset_b),         sin(angle_offset_b),         0)
        b'  = (cos(angle_offset_b + pi/2),  sin(angle_offset_b + pi/2),  0)

    With angle_offset_a = 0 and angle_offset_b = pi/4, the analyzers are
    Tsirelson-optimal in the sense that maximally entangled correlations
    saturate 2*sqrt(2).

    Parameters
    ----------
    quats_A, quats_B : array-like
        Unit quaternion trajectories, shape (T, 4) each. Must have the
        same length. Caller ensures unit normalisation.
    angle_offset_a, angle_offset_b : float
        Analyzer-direction offsets in the xy-plane, in radians. Defaults
        give the Tsirelson-optimal alignment.

    Returns
    -------
    dict
        {
            "enabled":           bool,
            "S_value":           float,
            "classical_bound":   float (2.0),
            "tsirelson_bound":   float (2*sqrt(2)),
            "coherence_score":   float in [-something, 1+] = (S - 2) / (2*sqrt(2) - 2),
            "coherence_verdict": "coupled" | "borderline" | "independent" | "anomalous",
            "n_steps":           int (T),
            "correlations": {
                "E_ab":          float,
                "E_ab_prime":    float,
                "E_a_prime_b":   float,
                "E_a_prime_b_prime": float,
            },
            "warnings":          list[str],
        }

    Raises
    ------
    InvalidInputError
        If quaternion arrays don't match shape (T, 4) or have mismatched T.
    """

    qA = np.asarray(quats_A, dtype=np.float64)
    qB = np.asarray(quats_B, dtype=np.float64)

    if qA.ndim != 2 or qA.shape[1] != 4:
        raise InvalidInputError(
            f"chsh_S_value: quats_A must be (T, 4), got {qA.shape}"
        )
    if qB.ndim != 2 or qB.shape[1] != 4:
        raise InvalidInputError(
            f"chsh_S_value: quats_B must be (T, 4), got {qB.shape}"
        )
    if qA.shape[0] != qB.shape[0]:
        raise InvalidInputError(
            f"chsh_S_value: quats_A length {qA.shape[0]} != "
            f"quats_B length {qB.shape[0]}"
        )

    T = qA.shape[0]
    warnings: list[str] = []

    if T < 2:
        warnings.append(f"T={T} too small for meaningful CHSH estimate")
        return {
            "enabled": False,
            "S_value": 0.0,
            "classical_bound": CLASSICAL_BOUND,
            "tsirelson_bound": TSIRELSON_BOUND,
            "coherence_score": 0.0,
            "coherence_verdict": "indeterminate",
            "n_steps": int(T),
            "correlations": {
                "E_ab": 0.0,
                "E_ab_prime": 0.0,
                "E_a_prime_b": 0.0,
                "E_a_prime_b_prime": 0.0,
            },
            "warnings": warnings,
        }

    # Vector parts of the quaternions.
    vec_A = qA[:, 1:]  # (T, 3)
    vec_B = qB[:, 1:]  # (T, 3)

    # Analyzer axes in the xy-plane.
    def axis(angle: float) -> np.ndarray:
        return np.array([math.cos(angle), math.sin(angle), 0.0], dtype=np.float64)

    a = axis(angle_offset_a)
    a_prime = axis(angle_offset_a + math.pi / 2.0)
    b = axis(angle_offset_b)
    b_prime = axis(angle_offset_b + math.pi / 2.0)

    # Sign of each projection per step.
    def sgn(vec_traj: np.ndarray, ax: np.ndarray) -> np.ndarray:
        proj = vec_traj @ ax
        # Strict sign: zeros are mapped to +1 to avoid sign-undefined tie.
        out = np.where(proj >= 0.0, 1.0, -1.0)
        return out

    s_a = sgn(vec_A, a)
    s_a_prime = sgn(vec_A, a_prime)
    s_b = sgn(vec_B, b)
    s_b_prime = sgn(vec_B, b_prime)

    # Correlations.
    E_ab = float((s_a * s_b).mean())
    E_ab_prime = float((s_a * s_b_prime).mean())
    E_a_prime_b = float((s_a_prime * s_b).mean())
    E_a_prime_b_prime = float((s_a_prime * s_b_prime).mean())

    S = abs(E_ab + E_ab_prime + E_a_prime_b - E_a_prime_b_prime)

    coherence_score = (S - CLASSICAL_BOUND) / (TSIRELSON_BOUND - CLASSICAL_BOUND)

    if S > TSIRELSON_BOUND + 1e-9:
        verdict = "anomalous"
        warnings.append(
            f"S = {S:.4f} exceeds Tsirelson bound {TSIRELSON_BOUND:.4f} "
            f"(should not occur physically; check engine numerics or input data)"
        )
    elif S < CLASSICAL_BOUND - 1e-9:
        verdict = "independent"
    elif S < CLASSICAL_BOUND + 0.4:
        verdict = "borderline"
    else:
        verdict = "coupled"

    return {
        "enabled": True,
        "S_value": float(S),
        "classical_bound": CLASSICAL_BOUND,
        "tsirelson_bound": TSIRELSON_BOUND,
        "coherence_score": float(coherence_score),
        "coherence_verdict": verdict,
        "n_steps": int(T),
        "correlations": {
            "E_ab": E_ab,
            "E_ab_prime": E_ab_prime,
            "E_a_prime_b": E_a_prime_b,
            "E_a_prime_b_prime": E_a_prime_b_prime,
        },
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _to_unit_vectors_3d(
    sub: np.ndarray, *, eps: float = 1e-15
) -> tuple:
    """Normalise a (T, 3) trajectory to unit vectors with zero-radius guard.

    Returns (units, radii) where units has shape (T, 3) and radii has
    shape (T,). Rows with radius below eps map to zero unit vectors.
    """

    radii = np.linalg.norm(sub, axis=1)
    safe = radii > eps
    units = np.zeros_like(sub)
    units[safe] = sub[safe] / radii[safe, None]
    return units, radii


def _quaternion_angular_distance(
    qA: np.ndarray, qB: np.ndarray
) -> np.ndarray:
    """Per-step angular distance between two quaternion paths.

    For unit quaternions, the angular distance is 2 * arccos(|q_A . q_B|).
    The absolute value handles the antipodal identification (q and -q
    represent the same rotation in SO(3)).

    Returns
    -------
    np.ndarray
        Per-step angular distances in radians, shape (T,).
    """

    if qA.size == 0 or qB.size == 0:
        return np.zeros((0,), dtype=np.float64)

    if qA.shape != qB.shape:
        raise InvalidInputError(
            f"_quaternion_angular_distance: shape mismatch "
            f"{qA.shape} vs {qB.shape}"
        )

    dot = np.einsum("ij,ij->i", qA, qB)
    abs_dot = np.clip(np.abs(dot), 0.0, 1.0)
    return 2.0 * np.arccos(abs_dot)


def _build_per_step_ledger(
    residuals: np.ndarray,
    quats: np.ndarray,
    angles: np.ndarray,
) -> list:
    """Assemble per-step ledger entries from sandwich-residuals output."""

    out = []
    for t in range(residuals.shape[0]):
        out.append(
            {
                "t": int(t),
                "q_w": float(quats[t, 0]),
                "q_x": float(quats[t, 1]),
                "q_y": float(quats[t, 2]),
                "q_z": float(quats[t, 3]),
                "angle_rad": float(angles[t]),
                "residual_linf": float(residuals[t]),
            }
        )
    return out
