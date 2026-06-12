"""CN-TT v4 — provenance + the cross-platform determinism contract.
stable_hash() rounds floats to a DECLARED precision before hashing, so a receipt
is identical across platforms (rover vs ground) to that precision. CNTT hashes
are independent of CNT/CNQ hashes by design (engine-independence, INV-038)."""
from __future__ import annotations
import hashlib, json

ENGINE_NAME = "HCI-CNTT"
ENGINE_VERSION = "4.0.0"
SCHEMA_VERSION = "cntt/4.0.0"
DETERMINISM_DECIMALS = 12   # declared precision: hashes stable to 1e-12 absolute

def _default(o):
    try:
        return list(o)
    except TypeError:
        return float(o)

def _canon(o):
    if isinstance(o, bool):
        return o
    if isinstance(o, float):
        r = round(o, DETERMINISM_DECIMALS)
        return 0.0 if r == 0 else r
    if isinstance(o, dict):
        return {k: _canon(o[k]) for k in sorted(o, key=str)}
    if isinstance(o, (list, tuple)):
        return [_canon(x) for x in o]
    try:
        import numpy as np
        if isinstance(o, np.ndarray):
            return _canon(o.tolist())
        if isinstance(o, (np.floating,)):
            return _canon(float(o))
        if isinstance(o, (np.integer,)):
            return int(o)
    except Exception:
        pass
    return o

def canonical_sha256(obj):
    s = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=_default)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def stable_hash(obj):
    """Platform-stable receipt: floats normalized to DETERMINISM_DECIMALS first."""
    s = json.dumps(_canon(obj), sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=_default)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def version_triple():
    return {"engine": ENGINE_NAME, "engine_version": ENGINE_VERSION, "schema_version": SCHEMA_VERSION}
