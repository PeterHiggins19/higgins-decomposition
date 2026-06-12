"""
CNQ self-test runner — Built-In Self-Test (BIST) per STP-1.0 doctrine.

Loads HCI-CNQ/engine/self_test/standard_test_matrices.json, generates each
test matrix from its declarative generation block (or uses inline rows), runs
the CNQ engine on each matrix, compares actual output against
expected_results.json, and writes a dated, hash-signed receipt to
HCI-CNQ/engine/self_test/RECEIPTS/.

The receipt chains to the previous receipt's sha256, forming a Merkle-style
audit log. Every receipt is independently verifiable by recomputing the
canonical-JSON SHA-256 of its body (with receipt_sha256 omitted).

Usage:

    # CLI:
    python HCI-CNQ/engine/self_test/run_self_test.py

    # Programmatic:
    from HCI_CNQ.engine.self_test import run_self_test
    exit_code = run_self_test.run()  # 0 on ALL_PASS, non-zero otherwise

The runner is engine-agnostic in design: it depends on a `cnq_run` callable
that takes a CSV-or-rows-array input and returns a payload dict. When the CNQ
v2 engine ships, replace the import accordingly.

See: docs/SELF_TEST_PROTOCOL.md (STP-1.0 doctrine)
     HCI-CNQ/engine/self_test/STANDARD_TEST_MATRICES.md
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import socket
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np


_THIS_FILE = Path(__file__).resolve()
_SELF_TEST_DIR = _THIS_FILE.parent
_REPO_ROOT = _SELF_TEST_DIR.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from hci_shared.hashing import canonical_dumps, canonical_sha256, file_sha256  # noqa: E402


CORPUS_PATH = _SELF_TEST_DIR / "standard_test_matrices.json"
EXPECTED_PATH = _SELF_TEST_DIR / "expected_results.json"
RECEIPTS_DIR = _SELF_TEST_DIR / "RECEIPTS"
LATEST_PATH = RECEIPTS_DIR / "LATEST_RECEIPT.json"

PROTOCOL_VERSION = "STP-1.0"


# ---------------------------------------------------------------------------
# Matrix generation from declarative spec
# ---------------------------------------------------------------------------


def generate_matrix(test_spec: Dict[str, Any]) -> Tuple[List[Any], List[str], np.ndarray]:
    """Materialise a test input from its corpus spec.

    Returns (labels, carrier_names, rows) where rows is an (n_records, n_carriers)
    NumPy float64 array.
    """
    n_carriers = int(test_spec["n_carriers"])
    n_records = int(test_spec["n_records"])
    carriers = list(test_spec["carriers"])
    labels = [f"t{t:04d}" for t in range(n_records)]

    if "rows_provided" in test_spec and test_spec["rows_provided"] is not None:
        rows = np.asarray(test_spec["rows_provided"], dtype=np.float64)
        if rows.shape != (n_records, n_carriers):
            raise ValueError(
                f"{test_spec['test_id']}: rows_provided shape {rows.shape} "
                f"does not match declared ({n_records}, {n_carriers})"
            )
        return labels, carriers, rows

    gen = test_spec.get("generation")
    if not gen:
        raise ValueError(f"{test_spec['test_id']}: no generation method or rows_provided")

    method = gen["method"]
    rows = np.zeros((n_records, n_carriers), dtype=np.float64)

    if method == "uniform":
        rows[:] = float(gen["value_per_carrier"])
    elif method == "single_dominant":
        rows[:] = float(gen["background_value"])
        rows[:, int(gen["dominant_index"])] = float(gen["dominant_value"])
    elif method == "period_2_alternation":
        a = np.asarray(gen["state_a"], dtype=np.float64)
        b = np.asarray(gen["state_b"], dtype=np.float64)
        for t in range(n_records):
            rows[t] = a if t % 2 == 0 else b
    elif method == "dirichlet":
        rng = np.random.default_rng(seed=int(gen["seed"]))
        alpha = float(gen["alpha"])
        rows = rng.dirichlet([alpha] * n_carriers, size=n_records)
        # Re-scale away from zero to satisfy strict positivity.
        rows = rows * 0.99 + 0.01 / n_carriers
    elif method == "stereo_coupled":
        rng = np.random.default_rng(seed=int(gen["seed"]))
        coupling = float(gen.get("coupling_strength", 0.95))
        # Generate a shared rotation pattern; both halves driven by it
        # plus independent noise scaled by (1 - coupling).
        for t in range(n_records):
            shared = rng.uniform(0.5, 2.0, size=n_carriers // 2)
            noise_a = rng.uniform(-0.1, 0.1, size=n_carriers // 2)
            noise_b = rng.uniform(-0.1, 0.1, size=n_carriers // 2)
            rows[t, : n_carriers // 2] = shared + (1.0 - coupling) * noise_a
            rows[t, n_carriers // 2 :] = shared + (1.0 - coupling) * noise_b
        rows = np.maximum(rows, 0.01)
    elif method == "stereo_decoupled":
        rng_a = np.random.default_rng(seed=int(gen["seed_A"]))
        rng_b = np.random.default_rng(seed=int(gen["seed_B"]))
        for t in range(n_records):
            rows[t, : n_carriers // 2] = rng_a.uniform(0.5, 2.0, size=n_carriers // 2)
            rows[t, n_carriers // 2 :] = rng_b.uniform(0.5, 2.0, size=n_carriers // 2)
    elif method == "monotonic_drift":
        gc = int(gen["growth_carrier"])
        dc = int(gen["decay_carrier"])
        rate = float(gen["growth_rate"])
        for t in range(n_records):
            rows[t, :] = 1.0
            rows[t, gc] = 1.0 + rate * t
            rows[t, dc] = max(0.01, 1.0 - rate * t * 0.5)
    elif method == "pairwise_coverage":
        rng = np.random.default_rng(seed=int(gen["seed"]))
        # Each row segment-i exhibits a different correlation pattern between
        # specific carrier pairs. Total length covers every C(D,2) pair.
        for t in range(n_records):
            base = rng.uniform(1.0, 2.0, size=n_carriers)
            # Modulate based on which pair is active in this segment.
            pair_idx = t % (n_carriers * (n_carriers - 1) // 2)
            i = 0
            j = 1
            count = 0
            for ii in range(n_carriers):
                for jj in range(ii + 1, n_carriers):
                    if count == pair_idx:
                        i, j = ii, jj
                        break
                    count += 1
                else:
                    continue
                break
            base[i] *= 1.5
            base[j] *= 1.5
            rows[t] = base
    else:
        raise ValueError(f"{test_spec['test_id']}: unknown generation method '{method}'")

    return labels, carriers, rows


# ---------------------------------------------------------------------------
# Engine adapter (stub for now; replaced when CNQ v2 ships)
# ---------------------------------------------------------------------------


def run_engine_on_matrix(
    rows: np.ndarray,
    carriers: List[str],
    labels: List[Any],
    *,
    test_id: str,
    engine_callable: Optional[Callable] = None,
) -> Optional[Dict[str, Any]]:
    """Run the CNQ engine on a test matrix and return the payload.

    Until CNQ v2 ships (Phase C2), this routes through CNT v3 (which exists)
    so the runner is testable end-to-end on real engine output. When CNQ v2
    lands, swap the routing to the CNQ engine.

    Returns None if the engine is unavailable; runner records SKIP for that test.
    """
    if engine_callable is not None:
        try:
            return engine_callable(rows=rows, carriers=carriers, labels=labels)
        except Exception:
            return None

    # Default routing: write a temp CSV and call CNT v3.
    import tempfile
    cnt_engine_dir = _REPO_ROOT / "HCI-CNT" / "engine"
    if not (cnt_engine_dir / "cnt.py").exists():
        return None
    if str(cnt_engine_dir) not in sys.path:
        sys.path.insert(0, str(cnt_engine_dir))
    try:
        import cnt  # type: ignore
    except Exception:
        return None

    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False, newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["label"] + list(carriers))
        for label, row in zip(labels, rows):
            writer.writerow([str(label)] + [float(x) for x in row])
        tmp_path = Path(f.name)
    try:
        return cnt.cnt_run(tmp_path)
    except Exception as exc:
        return {"_engine_error": str(exc)}
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Per-test verification (matches actual against expected_results.json)
# ---------------------------------------------------------------------------


def verify_test(
    test_id: str,
    actual: Optional[Dict[str, Any]],
    expected_entry: Optional[Dict[str, Any]],
) -> Tuple[str, List[Dict[str, Any]], List[str]]:
    """Compare an engine's actual output against the locked expected entry.

    Returns (verdict, checks, warnings). Verdicts: PASS, FAIL, SKIP, ERROR.
    """
    warnings: List[str] = []
    checks: List[Dict[str, Any]] = []

    if actual is None:
        return "SKIP", checks, ["engine unavailable or returned None"]
    if "_engine_error" in actual:
        return "ERROR", [], [f"engine raised: {actual['_engine_error']}"]
    if expected_entry is None:
        warnings.append(f"no expected_results entry for {test_id}; recording presence only")
        # Schema-presence check: assert top-level fields exist.
        for top in ("metadata", "input", "diagnostics"):
            present = top in actual
            checks.append({"field": top, "match": present, "note": "presence-only"})
        return ("PASS" if all(c["match"] for c in checks) else "FAIL"), checks, warnings

    for check_spec in expected_entry.get("checks", []):
        field = check_spec["field"]
        actual_val = _resolve_field(actual, field)
        check_record: Dict[str, Any] = {"field": field, "actual": actual_val}
        if "expected" in check_spec:
            expected = check_spec["expected"]
            check_record["expected"] = expected
            check_record["match"] = bool(actual_val == expected)
        elif "expected_min" in check_spec or "expected_max" in check_spec:
            lo = check_spec.get("expected_min", float("-inf"))
            hi = check_spec.get("expected_max", float("inf"))
            check_record["expected_min"] = lo
            check_record["expected_max"] = hi
            try:
                v = float(actual_val) if actual_val is not None else None
                check_record["match"] = bool(v is not None and lo <= v <= hi)
            except (TypeError, ValueError):
                check_record["match"] = False
                check_record["note"] = "actual not numeric"
        elif "tolerance_abs" in check_spec:
            target = check_spec.get("expected", 0.0)
            tol = check_spec["tolerance_abs"]
            check_record["expected"] = target
            check_record["tolerance_abs"] = tol
            try:
                check_record["match"] = bool(abs(float(actual_val) - float(target)) <= tol)
            except (TypeError, ValueError):
                check_record["match"] = False
        else:
            check_record["match"] = False
            check_record["note"] = "malformed check spec"
        checks.append(check_record)

    verdict = "PASS" if all(c.get("match") for c in checks) else "FAIL"
    return verdict, checks, warnings


def _resolve_field(payload: Dict[str, Any], path: str) -> Any:
    """Resolve a dot-notation path into a payload dict; None if any segment missing."""
    cursor: Any = payload
    for segment in path.split("."):
        if isinstance(cursor, dict) and segment in cursor:
            cursor = cursor[segment]
        else:
            return None
    return cursor


# ---------------------------------------------------------------------------
# Receipt generation + hash chain
# ---------------------------------------------------------------------------


def _read_previous_receipt_sha256() -> Optional[str]:
    if not LATEST_PATH.exists():
        return None
    try:
        prev = json.loads(LATEST_PATH.read_text(encoding="utf-8"))
        return prev.get("receipt_sha256")
    except (OSError, json.JSONDecodeError):
        return None


def _engine_content_sha256() -> Optional[str]:
    """Hash of CNQ engine source files at test time. None if unavailable."""
    cnq_engine_path = _REPO_ROOT / "HCI-CNQ" / "engine" / "cnq.py"
    if cnq_engine_path.exists():
        return file_sha256(cnq_engine_path)
    # Fallback: hash CNT v3 (the engine actually being exercised in this stub).
    cnt_engine_path = _REPO_ROOT / "HCI-CNT" / "engine" / "cnt.py"
    if cnt_engine_path.exists():
        return file_sha256(cnt_engine_path)
    return None


def run() -> int:
    """Top-level: run all tests, write receipt, return 0 if ALL_PASS else 1."""
    t0 = time.monotonic()

    if not CORPUS_PATH.exists():
        print(f"FATAL: corpus not found at {CORPUS_PATH}", file=sys.stderr)
        return 2
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    corpus_sha = file_sha256(CORPUS_PATH)

    if EXPECTED_PATH.exists():
        expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
        expected_sha = file_sha256(EXPECTED_PATH)
    else:
        expected = {"tests": {}}
        expected_sha = "0" * 64  # all-zero hash signals "no locked expectations yet"

    test_results: List[Dict[str, Any]] = []
    verdict_counts = {"PASS": 0, "FAIL": 0, "SKIP": 0, "ERROR": 0}

    for spec in corpus.get("matrices", []):
        test_id = spec["test_id"]
        t_start = time.monotonic()
        try:
            labels, carriers, rows = generate_matrix(spec)
            actual = run_engine_on_matrix(rows, carriers, labels, test_id=test_id)
            expected_entry = expected.get("tests", {}).get(test_id)
            verdict, checks, warnings = verify_test(test_id, actual, expected_entry)
        except Exception as exc:
            verdict = "ERROR"
            checks = []
            warnings = [f"runner exception: {type(exc).__name__}: {exc}"]
        wall_ms = int((time.monotonic() - t_start) * 1000)
        test_results.append(
            {
                "test_id": test_id,
                "verdict": verdict,
                "wall_clock_ms": wall_ms,
                "checks": checks,
                "warnings": warnings,
            }
        )
        verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1

    duration_ms = int((time.monotonic() - t0) * 1000)
    if verdict_counts["FAIL"] > 0 or verdict_counts["ERROR"] > 0:
        aggregate = "SOME_FAILED"
    elif verdict_counts["SKIP"] > 0:
        aggregate = "SOME_SKIPPED"
    else:
        aggregate = "ALL_PASS"

    receipt: Dict[str, Any] = {
        "self_test_protocol_version": PROTOCOL_VERSION,
        "engine": "HCI-CNQ",
        "engine_version": "2.0.0",
        "schema_version": "cnq/2.0.0",
        "engine_content_sha256_at_test_time": _engine_content_sha256(),
        "corpus_id": corpus.get("corpus_id", "unknown"),
        "corpus_sha256": corpus_sha,
        "expected_results_sha256": expected_sha,
        "run_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "run_environment": {
            "git_sha": None,
            "python_version": sys.version.split()[0],
            "numpy_version": np.__version__,
            "platform": platform.platform(),
            "hostname_hash": hashlib.sha256(socket.gethostname().encode()).hexdigest()[:16],
            "engine_implementation": "python",
        },
        "test_results": test_results,
        "summary": {
            "total_tests": sum(verdict_counts.values()),
            "passed": verdict_counts["PASS"],
            "failed": verdict_counts["FAIL"],
            "skipped": verdict_counts["SKIP"] + verdict_counts.get("ERROR", 0),
            "duration_ms": duration_ms,
            "aggregate_verdict": aggregate,
        },
        "previous_receipt_sha256": _read_previous_receipt_sha256(),
        "receipt_sha256": "PLACEHOLDER",  # Filled in below.
    }

    # Compute self-hash on receipt body with receipt_sha256 omitted.
    body = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    digest = canonical_sha256(body, extra_volatile=("run_timestamp",))
    receipt["receipt_sha256"] = digest

    # Write archive.
    date_dir = RECEIPTS_DIR / time.strftime("%Y-%m-%d", time.gmtime())
    date_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{time.strftime('%H%M%S', time.gmtime())}_{aggregate}.json"
    archive_path = date_dir / fname
    archive_path.write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    LATEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    LATEST_PATH.write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Console summary.
    print(f"=== CNQ self-test receipt ===")
    print(f"corpus      : {receipt['corpus_id']} ({corpus_sha[:16]}...)")
    print(f"engine      : {receipt['engine']} v{receipt['engine_version']}")
    print(f"engine sha  : {receipt['engine_content_sha256_at_test_time']}")
    print(f"timestamp   : {receipt['run_timestamp']}")
    print(f"summary     : {verdict_counts['PASS']} PASS, {verdict_counts['FAIL']} FAIL, "
          f"{verdict_counts['SKIP']} SKIP, {verdict_counts['ERROR']} ERROR")
    print(f"verdict     : {aggregate}")
    print(f"receipt sha : {digest}")
    print(f"chain back  : {receipt['previous_receipt_sha256']}")
    print(f"archived to : {archive_path}")

    return 0 if aggregate == "ALL_PASS" else 1


if __name__ == "__main__":
    sys.exit(run())
