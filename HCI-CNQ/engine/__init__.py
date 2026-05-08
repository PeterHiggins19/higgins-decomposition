"""HCI-CNQ engine package — Compositional Navigation Quaternion.

The compiled sibling to HCI-CNT/engine/cnt.py. Inherits from the canonical
CNT engine via cnt_adapter; produces hash-chained CNQ outputs that carry
the parent CNT content_sha256 forward into a quaternion-native view.

Pure stdlib + numpy. No hidden dependencies. No hardcoded local paths.

Public surface:
    cnq.run_cnq           — top-level CNQ run from CNT JSON or raw CSV
    geometry.helmert_basis — Helmert orthonormal contrast matrix
    geometry.quat_*        — quaternion utilities
    cnt_adapter.find_cnt_engine — locate canonical cnt.py from any clone
    hashing.canonical_sha256    — deterministic JSON content hash
"""

__version__ = "1.0.0"
__schema__ = "cnq/1.0.0"
