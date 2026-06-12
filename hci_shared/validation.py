"""
hci_shared.validation — strict input validators

Every public engine entry point validates its inputs through these functions
before any math runs. The contract is: invalid input raises InvalidInputError
with a clear message; valid input returns silently. No silent coercion, no
NaN propagation, no surprises later in the pipeline.

This addresses one of the major weaknesses ChatGPT identified in CNQ v1.0.0:
the engine's `closure` and `clr` functions accepted negative inputs, NaN, Inf,
and zero rows — producing nonsensical output that only failed at hash
canonicalisation (where allow_nan=False finally caught the problem). Strict
validation at the entry point converts those silent failures into explicit
errors with line numbers.
"""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np


class InvalidInputError(ValueError):
    """Raised by hci_shared validators when input fails contract.

    Inherits from ValueError so existing error-handling that catches
    ValueError continues to work; downstream code that wants to distinguish
    contract-level failures from other ValueErrors can catch this subclass.
    """

    pass


def validate_rows(
    rows: np.ndarray,
    *,
    min_carriers: int = 2,
    max_carriers: Optional[int] = None,
    allow_zero: bool = False,
    context: str = "rows",
) -> np.ndarray:
    """Validate a (T, D) compositional row matrix.

    Parameters
    ----------
    rows : array-like
        Raw input rows. Will be converted to a NumPy float64 array.
    min_carriers : int, default 2
        Minimum required number of carriers (D). D < min_carriers raises.
    max_carriers : int or None
        If given, D > max_carriers raises. None means no upper limit.
    allow_zero : bool, default False
        If False, any row containing a zero or negative carrier raises.
        If True, zeros are allowed but negatives still raise (caller is
        expected to handle zeros downstream, e.g. via delta-replacement).
    context : str
        Free-form label included in error messages for traceability.

    Returns
    -------
    rows : np.ndarray
        Validated rows as a 2-D float64 array. Always a fresh array, never
        a view of the input.

    Raises
    ------
    InvalidInputError
        On any contract violation, with a message describing the specific
        failure (shape, dtype, finiteness, positivity, row sum).
    """

    arr = np.asarray(rows, dtype=np.float64)

    if arr.ndim != 2:
        raise InvalidInputError(
            f"{context}: expected a 2-D (T, D) array, got ndim={arr.ndim}"
        )

    T, D = arr.shape

    if T == 0:
        raise InvalidInputError(f"{context}: zero rows (T=0)")

    if D < min_carriers:
        raise InvalidInputError(
            f"{context}: at least {min_carriers} carriers required, got D={D}"
        )

    if max_carriers is not None and D > max_carriers:
        raise InvalidInputError(
            f"{context}: at most {max_carriers} carriers allowed, got D={D}"
        )

    if not np.isfinite(arr).all():
        # Report the first offending row for easier debugging.
        bad_rows = np.where(~np.isfinite(arr).all(axis=1))[0]
        first = int(bad_rows[0])
        raise InvalidInputError(
            f"{context}: row {first} contains NaN or Inf; "
            f"all carrier values must be finite"
        )

    if allow_zero:
        if (arr < 0).any():
            bad_rows = np.where((arr < 0).any(axis=1))[0]
            first = int(bad_rows[0])
            raise InvalidInputError(
                f"{context}: row {first} contains a negative carrier value; "
                f"all carrier values must be non-negative"
            )
    else:
        if (arr <= 0).any():
            bad_rows = np.where((arr <= 0).any(axis=1))[0]
            first = int(bad_rows[0])
            raise InvalidInputError(
                f"{context}: row {first} contains a non-positive carrier "
                f"(zero or negative); all carrier values must be strictly "
                f"positive (set allow_zero=True if zeros will be replaced "
                f"downstream)"
            )

    row_sums = arr.sum(axis=1)
    if (row_sums <= 0).any():
        bad_rows = np.where(row_sums <= 0)[0]
        first = int(bad_rows[0])
        raise InvalidInputError(
            f"{context}: row {first} has non-positive sum; all rows must "
            f"sum to a strictly positive value before closure"
        )

    # Return a fresh contiguous array; downstream code can mutate without
    # affecting caller's input.
    return np.ascontiguousarray(arr)


def validate_dimension(D: int, *, min_d: int = 2, max_d: Optional[int] = None) -> int:
    """Validate a scalar carrier-count D.

    Returns D as a plain Python int after type/range checks.
    """

    if not isinstance(D, (int, np.integer)):
        raise InvalidInputError(
            f"dimension D must be an integer, got {type(D).__name__}"
        )

    D = int(D)

    if D < min_d:
        raise InvalidInputError(
            f"dimension D={D} below minimum {min_d}; engine does not "
            f"support trajectories with fewer than {min_d} carriers"
        )

    if max_d is not None and D > max_d:
        raise InvalidInputError(
            f"dimension D={D} above maximum {max_d}; engine schema does "
            f"not extend to D > {max_d}"
        )

    return D


def validate_t_count(T: int, *, min_t: int = 1) -> int:
    """Validate a scalar trajectory-length T.

    Note that T=1 is permitted by default; the engine handles single-row
    inputs gracefully (no quaternion path, but full schema with bearing
    fields set to null where pairs are required). Engines that need at
    least two rows should pass min_t=2.
    """

    if not isinstance(T, (int, np.integer)):
        raise InvalidInputError(
            f"trajectory length T must be an integer, got {type(T).__name__}"
        )

    T = int(T)

    if T < min_t:
        raise InvalidInputError(
            f"trajectory length T={T} below minimum {min_t}"
        )

    return T


def validate_partition(
    partition: Sequence[int],
    *,
    D: int,
    name: str = "partition",
) -> tuple:
    """Validate a partition of ILR axes for twin/quad-quaternion factoring.

    A partition is a sequence of zero-based axis indices, all in [0, D-2]
    (since ILR space has D-1 dimensions). Indices must be unique and within
    range.

    Returns the partition as an immutable tuple of plain Python ints.
    """

    seq = tuple(int(x) for x in partition)

    if len(seq) == 0:
        raise InvalidInputError(f"{name}: empty partition not allowed")

    if len(set(seq)) != len(seq):
        raise InvalidInputError(f"{name}: duplicate axis indices in partition {seq}")

    ilr_max = D - 2  # ILR space has D-1 dims, max index is D-2
    for axis in seq:
        if axis < 0 or axis > ilr_max:
            raise InvalidInputError(
                f"{name}: axis index {axis} out of range [0, {ilr_max}] "
                f"for ILR dimension D-1 = {D-1}"
            )

    return seq
