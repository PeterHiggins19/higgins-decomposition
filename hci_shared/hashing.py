"""
hci_shared.hashing — canonical JSON + SHA256 with engine-version awareness

This module provides the determinism contract for the Hs engine family:
canonical_dumps + canonical_sha256 give two runs of the same engine version
on the same input byte-identical hashes within a single language. Across
languages (Python <-> R), parity is verified per-field, not byte-identical
hash, so each language's `canonical_dumps` is its own determinism contract
independently.

Per push #32 design (engine independence):

    * CNT v3 and CNQ v2 each pin their own (engine_name, engine_version,
      schema_version) triple inside the payload metadata. The triple is part
      of the canonical-hash payload. Different engines produce different
      hashes by design.

    * No cross-engine hash chain. CNQ output may carry a `cnt_reference`
      block as informational metadata, but that block does NOT participate
      in CNT-side hash propagation. CNQ's `cnq_content_sha256` covers the
      CNQ payload; CNT's `cnt_content_sha256` covers the CNT payload;
      neither contains the other's hash as a binding chain.

    * Volatile fields (timestamps, environment captures, the hash field
      itself) are stripped recursively at every nesting level before
      hashing. The default volatile-field name list is documented below
      and can be extended per engine via the `extra_volatile` parameter.

The serialiser uses Python's stdlib json with sort_keys=True,
separators=(',', ':'), ensure_ascii=True, allow_nan=False. The allow_nan=False
flag is the explicit gate that catches NaN values which would otherwise
produce ambiguous JSON (no portable spec for NaN). v1.0.0 of CNQ left this
gate but failed to validate input upstream; v2.0.0 validates upstream
(see hci_shared.validation) and keeps this gate as a defence-in-depth.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Optional, Tuple


# Default set of volatile field names recursively stripped before hashing.
# These are field names whose values change between runs even when the
# semantic content is identical (timestamps, hostnames, wall-clock figures,
# the content_sha256 itself when computed in-place).
DEFAULT_VOLATILE_FIELDS: Tuple[str, ...] = (
    "generated",
    "timestamp",
    "wall_clock",
    "wall_clock_ms",
    "_run_clock",
    "environment",
    "content_sha256",
    "cnt_content_sha256",
    "cnq_content_sha256",
)


def strip_volatile(
    obj: Any,
    *,
    volatile_fields: Optional[Iterable[str]] = None,
) -> Any:
    """Return a deep copy of `obj` with all volatile field names removed.

    Volatile fields are stripped recursively at every depth, in dicts and
    in dict-elements within lists. Other types (numbers, strings, bools,
    None) are returned unchanged.

    Parameters
    ----------
    obj : Any
        JSON-serialisable object (dict, list, scalar, None).
    volatile_fields : Iterable[str] or None
        Field names to strip. None uses DEFAULT_VOLATILE_FIELDS.

    Returns
    -------
    Any
        New object with volatile fields removed; original is not modified.
    """

    if volatile_fields is None:
        volatile_fields = DEFAULT_VOLATILE_FIELDS
    volatile_set = frozenset(volatile_fields)

    return _strip_recursive(obj, volatile_set)


def _strip_recursive(obj: Any, volatile_set: frozenset) -> Any:
    """Internal recursive helper for strip_volatile."""

    if isinstance(obj, dict):
        return {
            k: _strip_recursive(v, volatile_set)
            for k, v in obj.items()
            if k not in volatile_set
        }
    if isinstance(obj, list):
        return [_strip_recursive(x, volatile_set) for x in obj]
    if isinstance(obj, tuple):
        return [_strip_recursive(x, volatile_set) for x in obj]
    return obj


def canonical_dumps(
    obj: Any,
    *,
    extra_volatile: Optional[Iterable[str]] = None,
    strip: bool = True,
) -> str:
    """Serialise `obj` to canonical JSON.

    Canonical form: keys sorted at every nesting level, no whitespace between
    tokens, ASCII-safe (non-ASCII characters escaped as \\uXXXX), NaN/Inf
    rejected with ValueError.

    Parameters
    ----------
    obj : Any
        JSON-serialisable object.
    extra_volatile : Iterable[str] or None
        Additional field names to strip beyond DEFAULT_VOLATILE_FIELDS.
    strip : bool, default True
        If True (default), volatile fields are stripped before serialisation.
        Set False only when callers have already stripped (e.g., in tests
        of the serialiser itself).

    Returns
    -------
    str
        Canonical JSON string. Same input always produces the same output
        within a single Python version.

    Raises
    ------
    ValueError
        If `obj` contains NaN or Inf (allow_nan=False enforced).
    """

    if strip:
        if extra_volatile is None:
            volatile = DEFAULT_VOLATILE_FIELDS
        else:
            volatile = tuple(DEFAULT_VOLATILE_FIELDS) + tuple(extra_volatile)
        cleaned = strip_volatile(obj, volatile_fields=volatile)
    else:
        cleaned = obj

    return json.dumps(
        cleaned,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def canonical_sha256(
    obj: Any,
    *,
    extra_volatile: Optional[Iterable[str]] = None,
) -> str:
    """SHA-256 hex digest of `obj` after canonical-JSON serialisation.

    Convenience wrapper: `canonical_sha256(obj)` is equivalent to
    `hashlib.sha256(canonical_dumps(obj).encode("utf-8")).hexdigest()`.

    Returns
    -------
    str
        Lowercase hexadecimal SHA-256 digest, 64 characters long.
    """

    text = canonical_dumps(obj, extra_volatile=extra_volatile)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_sha256(path: Path | str, *, chunk_size: int = 65536) -> str:
    """SHA-256 hex digest of a file's bytes, streamed in chunks.

    Used to record `source_file_sha256` in engine output metadata so the
    input dataset itself can be verified without re-reading.
    """

    p = Path(path)
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def engine_payload_with_hash(
    payload: dict,
    *,
    hash_field_name: str,
    hash_path: tuple = ("diagnostics",),
) -> dict:
    """Compute and inject the canonical hash into an engine payload.

    The payload is hashed with the target hash field absent from the
    canonicalised content (`canonical_dumps` already strips known volatile
    field names including `content_sha256`, `cnt_content_sha256`,
    `cnq_content_sha256`); after hashing, the digest is written into the
    payload at the specified path.

    Parameters
    ----------
    payload : dict
        Engine payload, mutated in place by writing the hash field.
    hash_field_name : str
        Name of the hash field to write (e.g., 'cnt_content_sha256',
        'cnq_content_sha256').
    hash_path : tuple of str, default ('diagnostics',)
        Dot-path into the payload where the hash field is placed. The
        intermediate dicts are created if missing.

    Returns
    -------
    dict
        The same payload object with the hash field set. (Returned for
        chaining convenience; the input is mutated.)
    """

    digest = canonical_sha256(payload)

    cursor = payload
    for key in hash_path:
        if key not in cursor or not isinstance(cursor[key], dict):
            cursor[key] = {}
        cursor = cursor[key]
    cursor[hash_field_name] = digest

    return payload
