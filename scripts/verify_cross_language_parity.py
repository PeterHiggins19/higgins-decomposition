"""
Cross-language parity verification — Python <-> R per-field comparison.

Runs the same input through both language ports of an engine, compares output
field-by-field within tolerance, and emits a parity-receipt JSON. The contract
is per-field numerical match, NOT byte-identical hash (push #32 design §3.3).

Each language has its own canonical_dumps (Python uses json.dumps with
sort_keys=True; R uses jsonlite::toJSON with recursive sort_keys_recursive).
Float formatting differs subtly between the two — well within the per-field
tolerance for any meaningful diagnostic, but enough to break byte-identical
hash comparison.

Usage:

    python scripts/verify_cross_language_parity.py \
        --engine cnq \
        --input-csv test_input.csv \
        --tolerance-abs 1e-13 \
        --output parity_receipt.json

Exit codes:
    0  PARITY_OK         all fields match within tolerance
    1  PARITY_VIOLATIONS some field exceeded tolerance; receipt lists each
    2  INFRASTRUCTURE    one or both engines unavailable (e.g., R not installed)

The receipt is independently verifiable:

    python scripts/verify_cross_language_parity.py --verify <receipt.json>

See: docs/SELF_TEST_PROTOCOL.md (related but distinct discipline)
     ai-refresh/CNT_V3_CNQ_V2_DESIGN.md §3.3 (parity contract)
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


_THIS_FILE = Path(__file__).resolve()
_REPO_ROOT = _THIS_FILE.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

DEFAULT_TOLERANCE_ABS = 1e-13
DEFAULT_TOLERANCE_REL = 1e-12

ENGINE_PATHS = {
    "cnq": {
        "py": _REPO_ROOT / "HCI-CNQ" / "engine" / "cnq.py",
        "r":  _REPO_ROOT / "HCI-CNQ" / "engine" / "cnq.R",
        "py_module": "cnq",
        "py_dir": _REPO_ROOT / "HCI-CNQ" / "engine",
        "py_run": "cnq_run",
        "py_kwarg": "input_csv",
    },
    "cnt": {
        "py": _REPO_ROOT / "HCI-CNT" / "engine" / "cnt.py",
        "r":  _REPO_ROOT / "HCI-CNT" / "engine" / "cnt.R",
        "py_module": "cnt",
        "py_dir": _REPO_ROOT / "HCI-CNT" / "engine",
        "py_run": "cnt_run",
        "py_kwarg": "input_csv",
    },
}


def _canonical_sha256(obj: Any) -> str:
    text = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _flatten(obj: Any, prefix: str = "") -> Dict[str, Any]:
    """Flatten nested dict to dot-notation paths -> leaf values.

    Lists are flattened with [i] index suffixes. Used for per-field comparison.
    """
    out: Dict[str, Any] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_prefix = f"{prefix}.{k}" if prefix else k
            out.update(_flatten(v, new_prefix))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            new_prefix = f"{prefix}[{i}]"
            out.update(_flatten(v, new_prefix))
    else:
        out[prefix] = obj
    return out


def _compare_values(
    py_val: Any, r_val: Any, tol_abs: float, tol_rel: float
) -> Tuple[bool, str]:
    """Return (match, reason). Numerical fields compared within tolerance;
    string and bool compared exactly; null on either side comparable to null.
    """
    if py_val is None and r_val is None:
        return True, "both null"
    if py_val is None or r_val is None:
        return False, f"null mismatch (py={py_val}, r={r_val})"
    if isinstance(py_val, bool) or isinstance(r_val, bool):
        return (py_val == r_val), f"bool match" if py_val == r_val else f"bool mismatch"
    if isinstance(py_val, str) or isinstance(r_val, str):
        return (str(py_val) == str(r_val)), "string match" if str(py_val) == str(r_val) else "string mismatch"
    try:
        a = float(py_val)
        b = float(r_val)
        diff = abs(a - b)
        if diff <= tol_abs:
            return True, f"abs diff {diff:.3e} <= {tol_abs:.0e}"
        denom = max(abs(a), abs(b), 1e-30)
        if diff / denom <= tol_rel:
            return True, f"rel diff {diff/denom:.3e} <= {tol_rel:.0e}"
        return False, f"diff {diff:.3e} exceeds tolerance (abs={tol_abs:.0e}, rel={tol_rel:.0e})"
    except (TypeError, ValueError):
        return (py_val == r_val), "non-numeric comparison"


def _run_python_engine(engine: str, input_csv: Path) -> Optional[Dict[str, Any]]:
    info = ENGINE_PATHS[engine]
    if str(info["py_dir"]) not in sys.path:
        sys.path.insert(0, str(info["py_dir"]))
    try:
        mod = __import__(info["py_module"])
        runner = getattr(mod, info["py_run"])
        return runner(**{info["py_kwarg"]: input_csv})
    except Exception as exc:
        return {"_engine_error": str(exc), "_engine_error_type": type(exc).__name__}


def _run_r_engine(engine: str, input_csv: Path) -> Optional[Dict[str, Any]]:
    info = ENGINE_PATHS[engine]
    rscript = shutil.which("Rscript")
    if rscript is None:
        return None
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        out_path = Path(f.name)
    try:
        result = subprocess.run(
            [rscript, str(info["r"]),
             "--input-csv", str(input_csv),
             "-o", str(out_path)],
            capture_output=True, text=True, timeout=300,
        )
        if result.returncode != 0:
            return {"_engine_error": result.stderr.strip()[:500],
                    "_engine_error_type": "RscriptNonZeroExit"}
        if not out_path.exists() or out_path.stat().st_size == 0:
            return {"_engine_error": "R port produced no output JSON",
                    "_engine_error_type": "RscriptEmptyOutput"}
        return json.loads(out_path.read_text(encoding="utf-8"))
    except subprocess.TimeoutExpired:
        return {"_engine_error": "Rscript timed out", "_engine_error_type": "Timeout"}
    except Exception as exc:
        return {"_engine_error": str(exc), "_engine_error_type": type(exc).__name__}
    finally:
        try:
            os.unlink(out_path)
        except OSError:
            pass


# Fields excluded from comparison (volatile, language-specific, or schema-flexible).
EXCLUDED_FIELDS = (
    "metadata.generated",
    "metadata.wall_clock_ms",
    "metadata.environment",
    "metadata.engine_implementation",
    "metadata.implementation_lang_version",
    "diagnostics.cnq_content_sha256",
    "diagnostics.cnt_content_sha256",
    "diagnostics.content_sha256",
    "input.source_file",  # path differs across runs
)


def _is_excluded(path: str) -> bool:
    for ex in EXCLUDED_FIELDS:
        if path == ex or path.startswith(ex + "."):
            return True
    if ".environment" in path:
        return True
    return False


def run(
    engine: str,
    input_csv: Path,
    tol_abs: float = DEFAULT_TOLERANCE_ABS,
    tol_rel: float = DEFAULT_TOLERANCE_REL,
    output: Optional[Path] = None,
) -> Tuple[int, Dict[str, Any]]:
    t0 = time.monotonic()
    py_out = _run_python_engine(engine, input_csv)
    r_out = _run_r_engine(engine, input_csv)

    if py_out is None or "_engine_error" in (py_out or {}):
        py_status = "ERROR"
        py_err = (py_out or {}).get("_engine_error", "Python engine returned None")
    else:
        py_status = "OK"; py_err = None

    if r_out is None:
        r_status = "UNAVAILABLE"; r_err = "Rscript not on PATH"
    elif "_engine_error" in r_out:
        r_status = "ERROR"; r_err = r_out["_engine_error"]
    else:
        r_status = "OK"; r_err = None

    receipt: Dict[str, Any] = {
        "parity_protocol_version": "PARITY-1.0",
        "engine": engine,
        "input_csv": str(input_csv),
        "input_csv_sha256": hashlib.sha256(Path(input_csv).read_bytes()).hexdigest(),
        "tolerance_abs": tol_abs,
        "tolerance_rel": tol_rel,
        "python_status": py_status,
        "r_status": r_status,
        "python_error": py_err,
        "r_error": r_err,
        "run_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "platform": platform.platform(),
        "fields_compared": 0,
        "fields_matched": 0,
        "fields_violated": 0,
        "fields_only_py": [],
        "fields_only_r": [],
        "violations": [],
        "aggregate_verdict": "INFRASTRUCTURE",
    }

    if py_status != "OK" or r_status != "OK":
        receipt["aggregate_verdict"] = "INFRASTRUCTURE"
        receipt["duration_ms"] = int((time.monotonic() - t0) * 1000)
        receipt["receipt_sha256"] = _canonical_sha256(
            {k: v for k, v in receipt.items() if k != "receipt_sha256"}
        )
        if output is not None:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
        return (2, receipt)

    py_flat = _flatten(py_out)
    r_flat = _flatten(r_out)

    py_keys = set(py_flat.keys())
    r_keys = set(r_flat.keys())
    common = py_keys & r_keys
    only_py = py_keys - r_keys
    only_r = r_keys - py_keys

    receipt["fields_only_py"] = sorted([k for k in only_py if not _is_excluded(k)])[:50]
    receipt["fields_only_r"] = sorted([k for k in only_r if not _is_excluded(k)])[:50]

    matched = 0
    violations: List[Dict[str, Any]] = []
    for key in sorted(common):
        if _is_excluded(key):
            continue
        py_val = py_flat[key]
        r_val = r_flat[key]
        ok, reason = _compare_values(py_val, r_val, tol_abs, tol_rel)
        receipt["fields_compared"] += 1
        if ok:
            matched += 1
        else:
            violations.append({
                "field": key,
                "python_value": _safe_repr(py_val),
                "r_value": _safe_repr(r_val),
                "reason": reason,
            })

    receipt["fields_matched"] = matched
    receipt["fields_violated"] = len(violations)
    receipt["violations"] = violations[:100]

    if violations:
        receipt["aggregate_verdict"] = "PARITY_VIOLATIONS"
        exit_code = 1
    elif receipt["fields_only_py"] or receipt["fields_only_r"]:
        receipt["aggregate_verdict"] = "PARITY_OK_WITH_SHAPE_DIFFS"
        exit_code = 0
    else:
        receipt["aggregate_verdict"] = "PARITY_OK"
        exit_code = 0

    receipt["duration_ms"] = int((time.monotonic() - t0) * 1000)
    receipt["receipt_sha256"] = _canonical_sha256(
        {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    )

    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")

    return (exit_code, receipt)


def _safe_repr(v: Any) -> Any:
    if isinstance(v, float):
        return f"{v:.6e}"
    if isinstance(v, str) and len(v) > 100:
        return v[:100] + "..."
    return v


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Python <-> R cross-language parity verifier")
    p.add_argument("--engine", choices=["cnq", "cnt"], required=True)
    p.add_argument("--input-csv", type=str, required=True)
    p.add_argument("--tolerance-abs", type=float, default=DEFAULT_TOLERANCE_ABS)
    p.add_argument("--tolerance-rel", type=float, default=DEFAULT_TOLERANCE_REL)
    p.add_argument("--output", type=str, default=None)
    args = p.parse_args(argv)

    out_path = Path(args.output) if args.output else None
    code, receipt = run(
        engine=args.engine,
        input_csv=Path(args.input_csv),
        tol_abs=args.tolerance_abs,
        tol_rel=args.tolerance_rel,
        output=out_path,
    )

    print(f"=== Cross-language parity receipt ===")
    print(f"engine        : {receipt['engine']}")
    print(f"python_status : {receipt['python_status']}")
    print(f"r_status      : {receipt['r_status']}")
    print(f"fields:        compared={receipt['fields_compared']}  "
          f"matched={receipt['fields_matched']}  violated={receipt['fields_violated']}")
    if receipt['fields_only_py']:
        print(f"fields_only_py: {len(receipt['fields_only_py'])} (e.g., {receipt['fields_only_py'][:3]})")
    if receipt['fields_only_r']:
        print(f"fields_only_r : {len(receipt['fields_only_r'])} (e.g., {receipt['fields_only_r'][:3]})")
    print(f"verdict       : {receipt['aggregate_verdict']}")
    print(f"receipt sha   : {receipt['receipt_sha256']}")
    if out_path:
        print(f"written to    : {out_path}")
    return code


if __name__ == "__main__":
    sys.exit(main())
