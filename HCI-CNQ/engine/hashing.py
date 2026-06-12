"""Deterministic canonical-JSON SHA-256 hashing for HCI-CNQ.

Mirrors the determinism contract used by HCI-CNT/engine/cnt.py: the
content_sha256 must be byte-for-byte reproducible across:

  - operating systems (Linux, macOS, Windows)
  - Python 3.9 through 3.13
  - numpy versions
  - clock time (timestamps are excluded from the hashed payload)

The contract:
  1. JSON serialization uses sorted keys, no whitespace, ensure_ascii=True.
  2. Floats are formatted via repr() to preserve full float64 precision.
  3. The 'metadata' / 'generated' / 'timestamp' fields, if present, are
     stripped from the canonical payload before hashing.
  4. The content_sha256 is computed over the canonical bytes.

Public surface
--------------
canonical_dumps(obj)        -> str   (canonical JSON for hashing)
canonical_sha256(obj)       -> str   (lowercase hex SHA-256)
file_sha256(path)           -> str   (file content hash for source provenance)
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

# Fields excluded from the hashed canonical payload.
# These vary by clock or environment but must not change content_sha256.
_EXCLUDED_TOP_LEVEL_FIELDS = ("generated", "timestamp", "wall_clock", "_run_clock")


def _strip_volatile(obj: Any) -> Any:
    """Recursively strip clock-dependent fields. Pure function; copies."""
    if isinstance(obj, dict):
        return {
            k: _strip_volatile(v)
            for k, v in obj.items()
            if k not in _EXCLUDED_TOP_LEVEL_FIELDS
        }
    if isinstance(obj, list):
        return [_strip_volatile(v) for v in obj]
    return obj


def canonical_dumps(obj: Any) -> str:
    """Canonical JSON string used for hashing.

    Sorted keys, no whitespace, ASCII-safe. Volatile clock fields stripped.
    """
    stripped = _strip_volatile(obj)
    return json.dumps(
        stripped,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def canonical_sha256(obj: Any) -> str:
    """Lowercase-hex SHA-256 of the canonical-JSON encoding of obj."""
    payload = canonical_dumps(obj).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path) -> str:
    """SHA-256 of a file's bytes. Used for source_file_sha256 provenance."""
    p = Path(path)
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
