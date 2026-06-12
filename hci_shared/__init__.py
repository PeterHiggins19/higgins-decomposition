"""
hci_shared — shared compositional + quaternion algebra modules for the Higgins
Decomposition (Hs) instrument family.

This package provides domain-neutral mathematical building blocks consumed by
the CNT v3 (`HCI-CNT/engine/cnt.py`) and CNQ v2 (`HCI-CNQ/engine/cnq.py`)
engines, and by any future engine in the Hs framework.

Design contract (push #32):

    1. The math here is pure CoDa-community vocabulary: closure, CLR, ILR,
       Helmert basis, quaternion algebra, Hamilton product, sandwich product,
       coupling angles, joint correlations. There is no domain-specific
       interpretation in this package; domain wrappers (see
       HCI-CNQ/wrappers/) translate engine output to domain quantities at
       the report-builder layer, downstream of this code.

    2. Engines pin their own (engine_name, engine_version, schema_version)
       triples in their canonical-hash payloads. This package provides the
       canonical_dumps / canonical_sha256 primitives but does not impose
       cross-engine hash chains. CNT v3 and CNQ v2 hashes are independent
       by design.

    3. Within a single language, two runs of the same engine version on the
       same input produce byte-identical canonical hashes. Cross-language
       parity (Python <-> R) is verified per-field, not byte-identical hash;
       see `scripts/verify_cross_language_parity.py`.

    4. Inputs are validated strictly. Negative carriers, zero rows, NaN, Inf,
       and degenerate shapes raise ValueError at the entry point rather than
       producing silent NaN outputs that later fail at hash-canonicalisation.

Modules:

    validation   - strict input validators (positivity, finiteness, shape)
    hashing      - canonical-JSON + SHA256 with engine-version awareness
    geometry     - closure, CLR, ILR, Helmert basis, quaternion algebra
    helmsman     - dominant-axis trajectory, flips, stability, chaos, torque
    attractors   - period detection + attractor parameter fitting
    factoring    - twin-quaternion (D=8), quad-quaternion (D=16),
                   CHSH joint coherence diagnostic

References:

    ai-refresh/CNT_V3_CNQ_V2_DESIGN.md   - architectural design document
    HCI-CNQ/wrappers/WRAPPER_SCHEMA.md   - wrapper schema specification
    HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md - locked vocabulary
"""

__version__ = "1.0.0"
__schema__ = "hci_shared/1.0"
__author__ = "Peter Higgins (Rogue Wave Audio / Binaural Test Lab)"
__license__ = "Apache-2.0"

# Public API re-exports for convenience. Engines may import these directly
# from `hci_shared` rather than reaching into submodules, which keeps engine
# source files cleaner.

from hci_shared.validation import (
    validate_rows,
    validate_dimension,
    validate_t_count,
    InvalidInputError,
)

from hci_shared.hashing import (
    canonical_dumps,
    canonical_sha256,
    file_sha256,
    strip_volatile,
    DEFAULT_VOLATILE_FIELDS,
)

from hci_shared.geometry import (
    closure,
    clr,
    helmert_basis,
    ilr_from_clr,
    compositions_to_helmert_unit_vectors,
    ilr_norms,
    quat_from_axis_angle,
    quat_conj,
    quat_mul,
    quat_norm,
    quat_rotate,
    rotation_quaternion_between,
    quaternion_sandwich_residuals,
)

__all__ = [
    "__version__",
    "__schema__",
    # validation
    "validate_rows",
    "validate_dimension",
    "validate_t_count",
    "InvalidInputError",
    # hashing
    "canonical_dumps",
    "canonical_sha256",
    "file_sha256",
    "strip_volatile",
    "DEFAULT_VOLATILE_FIELDS",
    # geometry
    "closure",
    "clr",
    "helmert_basis",
    "ilr_from_clr",
    "compositions_to_helmert_unit_vectors",
    "ilr_norms",
    "quat_from_axis_angle",
    "quat_conj",
    "quat_mul",
    "quat_norm",
    "quat_rotate",
    "rotation_quaternion_between",
    "quaternion_sandwich_residuals",
]
