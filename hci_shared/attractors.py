"""
hci_shared.attractors — period detection and attractor parameter fitting

INV-034 graduates from DEFERRED scaffolding to load-bearing CANONICAL with
this module (push #32). The attractor fit reports the parameters of any
detected period-2 limit cycle in the ILR trajectory:

    period             :  detected period (currently 1 = fixed point or
                          2 = period-2 limit cycle; higher periods are
                          INV-future scope)
    period_stability   :  in [0, 1]; 1 = perfect period-2 alternation,
                          0 = no detectable period-2 structure
    dominant_pair      :  {axis_a, axis_b} = the two ILR axes carrying
                          most of the period-2 energy
    contraction_lambda :  Lyapunov-style envelope contraction rate;
                          negative = decaying oscillation (stable),
                          positive = growing oscillation (unstable),
                          near zero = neutral
    amplitude_A        :  RMS amplitude of the period-2 oscillation in
                          the dominant pair
    damping_zeta       :  effective damping ratio derived from envelope
                          decay
    confidence         :  per-axis oscillation_ratio and period-stability
                          score; "fitted" boolean composite

The fit operates on the ILR trajectory in R^(D-1) (no projection to 3-D
required), so it is dimension-agnostic and works for D=2 .. D=16+.

The audio-engineering interpretation of these channels (period <-> crossover
structure depth, contraction <-> group-delay coherence) lives in the audio
wrapper, not in this module.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from hci_shared.geometry import compositions_to_ilr
from hci_shared.validation import validate_rows


def fit_attractor(
    rows: np.ndarray,
    *,
    T_min: int = 8,
    period_threshold: float = 0.6,
    amplitude_threshold: float = 1e-10,
) -> dict:
    """Fit the period-2 attractor parameters to a compositional trajectory.

    Parameters
    ----------
    rows : array-like
        Compositional rows, shape (T, D), strictly positive.
    T_min : int, default 8
        Minimum trajectory length for fitting. Below this the fit is
        marked unfit and warnings are populated.
    period_threshold : float, default 0.6
        Minimum period_stability score for `fitted=True`.
    amplitude_threshold : float, default 1e-10
        Minimum amplitude_A for `fitted=True`.

    Returns
    -------
    dict
        {
            "fitted":             bool,
            "period":             int (1 or 2),
            "period_stability":   float in [0, 1],
            "dominant_pair":      {"axis_a": int, "axis_b": int},
            "contraction_lambda": float,
            "amplitude_A":        float,
            "damping_zeta":       float,
            "confidence": {
                "oscillation_ratio":      float,
                "period_stability_score": float,
            },
            "warnings":           list[str],
        }
    """

    rows_validated = validate_rows(rows, min_carriers=2)
    T = rows_validated.shape[0]

    warnings: list[str] = []

    # Default unfit return shape.
    def _unfit(reason: str) -> dict:
        warnings.append(reason)
        return {
            "fitted": False,
            "period": 1,
            "period_stability": 0.0,
            "dominant_pair": {"axis_a": 0, "axis_b": 0},
            "contraction_lambda": 0.0,
            "amplitude_A": 0.0,
            "damping_zeta": 0.0,
            "confidence": {
                "oscillation_ratio": 0.0,
                "period_stability_score": 0.0,
            },
            "warnings": warnings,
        }

    if T < T_min:
        return _unfit(f"trajectory too short for attractor fit (T={T} < T_min={T_min})")

    # ILR trajectory in R^(D-1). Use radii inside ILR space (no extra projection).
    ilr, _radii = compositions_to_ilr(rows_validated)
    # ilr has shape (T, D-1)

    # Mean-subtract for period analysis.
    centered = ilr - ilr.mean(axis=0, keepdims=True)
    var_per_axis = (centered ** 2).sum(axis=0)  # (D-1,)
    total_var = float(var_per_axis.sum())

    if total_var < amplitude_threshold:
        return _unfit("ILR variance below amplitude threshold; trajectory near fixed point")

    # Period-2 score per axis: -lag-1-autocorr / variance.
    # If trajectory alternates, lag-1 autocorr is strongly negative.
    # If trajectory is random, autocorr is near zero.
    # If trajectory is monotonic / period-1, autocorr is near positive.
    autocorr_lag1 = (centered[:-1] * centered[1:]).sum(axis=0)  # (D-1,)
    safe_var = np.where(var_per_axis > 1e-30, var_per_axis, 1.0)
    period_2_score = -autocorr_lag1 / safe_var
    # period_2_score in [-1, 1] approximately.

    # Pick the best period-2 axis (axis_a). If a second axis has substantive
    # (not noise-driven) variance, use it as axis_b; otherwise fall back to
    # a degenerate 1-D limit cycle by setting axis_b = axis_a.
    #
    # The validity threshold is RELATIVE: an axis with variance < 1e-12 of
    # the largest axis's variance is treated as numerical noise and excluded.
    # This catches the failure mode where a constant-mean axis still has
    # tiny rounding-noise variance (~5e-30 for T=50) that fools an absolute
    # threshold.
    max_var = float(var_per_axis.max())
    if max_var < amplitude_threshold:
        return _unfit("no axis has substantive variance; trajectory near fixed point")
    relative_floor = max(1e-12 * max_var, 1e-30)
    valid_mask = var_per_axis > relative_floor
    if valid_mask.sum() < 1:
        return _unfit("no axes pass relative variance threshold")

    sorted_axes = np.argsort(period_2_score)[::-1]
    sorted_valid = [int(idx) for idx in sorted_axes if bool(valid_mask[idx])]
    if len(sorted_valid) == 0:
        return _unfit("no valid axes after filter")
    axis_a = sorted_valid[0]

    if len(sorted_valid) >= 2:
        axis_b = sorted_valid[1]
        period_stability = float(
            max(0.0, (period_2_score[axis_a] + period_2_score[axis_b]) / 2.0)
        )
        pair_variance = float(var_per_axis[axis_a] + var_per_axis[axis_b])
        envelope = np.abs(centered[:, [axis_a, axis_b]]).sum(axis=1)
    else:
        # Degenerate 1-D limit cycle.
        axis_b = axis_a
        period_stability = float(max(0.0, period_2_score[axis_a]))
        pair_variance = float(var_per_axis[axis_a])
        envelope = np.abs(centered[:, axis_a])
        warnings.append(
            "1-D limit cycle: only one ILR axis carries variance; "
            "axis_b = axis_a in dominant_pair"
        )

    # Oscillation ratio: fraction of total variance carried by dominant pair.
    oscillation_ratio = pair_variance / max(total_var, 1e-30)

    # Amplitude_A: RMS in the dominant pair.
    amplitude_A = float(np.sqrt(pair_variance / T))

    # Envelope decay: linear regression of log(|x|) vs t in the dominant
    # axis (or pair, when 2-D). `envelope` already aggregated above.
    # Floor the envelope to avoid log(0).
    log_env = np.log(np.maximum(envelope, 1e-15))
    t_vec = np.arange(T, dtype=np.float64)
    # np.polyfit returns [slope, intercept]
    slope, _intercept = np.polyfit(t_vec, log_env, 1)
    contraction_lambda = float(slope)
    # damping_zeta convention: positive damping = decay, so damping_zeta = -slope
    damping_zeta = float(-slope)

    # Decide period.
    if period_stability >= period_threshold and amplitude_A >= amplitude_threshold:
        fitted = True
        period_value = 2
    else:
        fitted = False
        period_value = 1
        if period_stability < period_threshold:
            warnings.append(
                f"period_stability {period_stability:.3f} below threshold "
                f"{period_threshold}; no clean period-2 structure"
            )
        if amplitude_A < amplitude_threshold:
            warnings.append(
                f"amplitude_A {amplitude_A:.3e} below threshold {amplitude_threshold:.3e}"
            )

    return {
        "fitted": fitted,
        "period": period_value,
        "period_stability": period_stability,
        "dominant_pair": {"axis_a": axis_a, "axis_b": axis_b},
        "contraction_lambda": contraction_lambda,
        "amplitude_A": amplitude_A,
        "damping_zeta": damping_zeta,
        "confidence": {
            "oscillation_ratio": float(oscillation_ratio),
            "period_stability_score": period_stability,
        },
        "warnings": warnings,
    }

