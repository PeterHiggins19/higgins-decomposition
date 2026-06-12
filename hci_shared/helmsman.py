"""
hci_shared.helmsman — Helmsman family of dominant-axis trajectory diagnostics

The Helmsman family was scaffolded as INV-009 in earlier pushes and ships
to load-bearing CANONICAL status in CNT v3 / CNQ v2 (push #32). All six
channels are emitted from this single shared module so they cannot drift
between engines.

Vocabulary (locked in HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md and
HCI-CNT/handbook/GLOSSARY.md §I; reproduced here for self-containment):

    sigma_t            =  argmax_j |Delta h_j(t)|
                          The carrier index whose CLR coordinate changed
                          most between step t-1 and step t. The "leading"
                          or "dominant" carrier at step t.

    sign_t             =  sign( Delta h_{sigma_t}(t) )
                          The sign of the dominant change. +1 means the
                          dominant carrier rose; -1 means it fell.

    flips              =  count of indices t where sigma_t != sigma_{t-1}
                          Number of times the dominant-carrier identity
                          changed across the trajectory.

    stability_S_sigma  =  1 - flips / max(T - 2, 1)
                          Fraction of consecutive sigma pairs that were
                          unchanged. 1.0 = sigma constant; 0.0 = sigma
                          changes at every step.

    chaos_indicator    =  Feigenbaum-style period-doubling depth, when
                          detectable on the sigma sequence. Returns the
                          smallest power-of-2 period found, or null when
                          no clear period structure is present. The
                          implementation here is a low-bar period detector;
                          a full Feigenbaum-cascade analysis is INV-future.

    torque_proxy_t     =  |sigma_{t+1} - 2*sigma_t + sigma_{t-1}|
                          Second difference of sigma indices. Spikes mark
                          moments where the dominant-axis attribution is
                          accelerating its rotation through the carriers.

These are domain-neutral mathematical operators. Audio interpretation
(sigma <-> leading driver, flips <-> group-delay-discontinuity events,
torque <-> rate of leading-driver change) lives in the audio wrapper at
HCI-AUDIO/CNQ_AUDIO_WRAPPER.md and HCI-CNQ/wrappers/wrapper_audio.json.
Other domains (geochem, finance, government budget, etc.) interpret
through their own wrappers.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from hci_shared.geometry import clr, closure
from hci_shared.validation import validate_rows


def compute_helmsman_family(
    rows: np.ndarray,
    *,
    window: int = 8,
) -> dict:
    """Compute the six Helmsman channels for a compositional trajectory.

    Parameters
    ----------
    rows : array-like
        Compositional rows, shape (T, D), strictly positive. Validated
        before any computation; bad input raises InvalidInputError.
    window : int, default 8
        Rolling window length for stability_S_sigma.rolling and
        flips.rolling. Must be at least 2; values larger than T-1 are
        clamped down to max(T-1, 2).

    Returns
    -------
    dict
        {
            "sigma":             list[int]           length T,
            "sign":              list[int]           length T,
            "flips": {
                "total":         int,
                "rolling":       list[int]           length max(T-window, 0),
                "rolling_window": int,
            },
            "stability_S_sigma": {
                "global":        float,
                "rolling":       list[float]         length max(T-window, 0),
                "rolling_window": int,
            },
            "chaos_indicator":   int | None,
            "torque_proxy":      list[float]         length T,
        }

    Notes
    -----
    sigma_0 and sign_0 are conventionally defined as 0 and 0 respectively
    (no previous step to diff against). torque_proxy at t=0 and t=T-1
    is 0 (boundary).
    """

    rows_validated = validate_rows(rows, min_carriers=2)
    T, D = rows_validated.shape

    if T < 2:
        # Degenerate: no consecutive pairs. Return schema-consistent zeros.
        return {
            "sigma": [0] * T,
            "sign": [0] * T,
            "flips": {"total": 0, "rolling": [], "rolling_window": int(window)},
            "stability_S_sigma": {
                "global": 1.0,
                "rolling": [],
                "rolling_window": int(window),
            },
            "chaos_indicator": None,
            "torque_proxy": [0.0] * T,
        }

    # CLR-space trajectory.
    closed = closure(rows_validated)
    h = clr(closed)  # shape (T, D)

    # Per-step deltas (T-1, D)
    delta = h[1:] - h[:-1]
    abs_delta = np.abs(delta)

    # sigma_t for t=1..T-1 = argmax over j of |Δh_j(t)|. sigma_0 = 0.
    sigma_internal = np.argmax(abs_delta, axis=1).astype(int)
    sigma = np.zeros(T, dtype=int)
    sigma[1:] = sigma_internal

    # sign_t for t=1..T-1. sign_0 = 0.
    sign_arr = np.zeros(T, dtype=int)
    for t in range(1, T):
        s = sigma[t]
        d = delta[t - 1, s]
        if d > 0:
            sign_arr[t] = 1
        elif d < 0:
            sign_arr[t] = -1
        else:
            sign_arr[t] = 0

    # Flips: positions t in [2..T-1] where sigma[t] != sigma[t-1].
    # (t=1 has no previous "internal" sigma; the convention skips t=1 too,
    # so we count flips on the internal sigma sequence of length T-1.)
    flips_per_t = np.zeros(T, dtype=int)
    for t in range(2, T):
        if sigma[t] != sigma[t - 1]:
            flips_per_t[t] = 1
    flips_total = int(flips_per_t.sum())

    # Effective rolling window: clamp to [2, T-1].
    eff_window = max(2, min(int(window), max(T - 1, 2)))

    # Rolling flip-count over windows [t .. t+eff_window-1] for t=0..T-eff_window
    n_windows = max(T - eff_window, 0)
    rolling_flips = np.zeros(n_windows, dtype=int)
    for i in range(n_windows):
        rolling_flips[i] = int(flips_per_t[i : i + eff_window].sum())

    # Stability_S_sigma:
    # Global = 1 - flips / max(T - 2, 1)
    n_pairs = max(T - 2, 1)
    stability_global = 1.0 - flips_total / n_pairs

    # Rolling = 1 - rolling_flips / max(eff_window - 1, 1)
    rolling_n_pairs = max(eff_window - 1, 1)
    rolling_stability = 1.0 - rolling_flips.astype(np.float64) / rolling_n_pairs

    # torque_proxy_t = |sigma_{t+1} - 2*sigma_t + sigma_{t-1}| for t in [1, T-2]
    # boundaries (t=0, t=T-1) = 0.
    torque = np.zeros(T, dtype=np.float64)
    for t in range(1, T - 1):
        torque[t] = float(abs(sigma[t + 1] - 2 * sigma[t] + sigma[t - 1]))

    # chaos_indicator: try to detect period-2, period-4 structure on sigma.
    # Returns 1 (period 2), 2 (period 4), 3 (period 8), ..., or None.
    chaos = _detect_period_doubling(sigma_internal)

    return {
        "sigma": [int(x) for x in sigma],
        "sign": [int(x) for x in sign_arr],
        "flips": {
            "total": flips_total,
            "rolling": [int(x) for x in rolling_flips],
            "rolling_window": eff_window,
        },
        "stability_S_sigma": {
            "global": float(stability_global),
            "rolling": [float(x) for x in rolling_stability],
            "rolling_window": eff_window,
        },
        "chaos_indicator": chaos,
        "torque_proxy": [float(x) for x in torque],
    }


def _detect_period_doubling(sigma_seq: np.ndarray) -> Optional[int]:
    """Detect a power-of-2 period in a discrete sigma sequence.

    Returns the smallest doubling depth k such that sigma has period 2^k:
        depth 0 = period 1  (constant)
        depth 1 = period 2  (alternating two values)
        depth 2 = period 4
        depth 3 = period 8

    Returns None if no clean power-of-2 period is detected. The depth is
    capped at 3 (period 8) for robustness; deeper cascades require longer
    trajectories than this detector reliably handles.

    A period 2^k is "clean" if sigma[t] == sigma[t + 2^k] for all valid t,
    measured as a fraction >= 0.9 of t-positions.
    """

    n = len(sigma_seq)
    if n < 4:
        return None

    for depth in range(0, 4):  # period 1, 2, 4, 8
        period = 2 ** depth
        if period >= n:
            break
        # Check sigma[t] == sigma[t + period]
        matches = (sigma_seq[:-period] == sigma_seq[period:])
        if matches.size == 0:
            continue
        match_fraction = float(matches.mean())
        if match_fraction >= 0.9:
            return depth

    return None
