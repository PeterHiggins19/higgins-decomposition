"""
HCI-CNQ v2.0.0 — Compositional Navigation Quaternion engine

Native dataset producer. Reads compositional time series (rows-by-carriers
CSV), produces a deterministic JSON record covering the trajectory's
quaternion-algebraic structure: bearing trajectory, radial trajectory,
helmsman family channels, attractor fit, twin-quaternion factoring (D=8
native), and CHSH joint-coherence diagnostic.

CNQ v2 stands on its own. It does not require CNT input. If a CNT JSON
is provided, its hash is recorded in `cnt_reference` as informational
metadata only -- the CNQ canonical hash is independent (push #32
engine-independence policy).

Pipeline (push #32 architecture):

    rows  ->  closure   ->  CLR    ->  Helmert ILR
                                      |
                                      +->  bearing_trajectory (per D-policy:
                                      |    D=4 native, D=8 twin-quaternion,
                                      |    D=16 quad-quaternion future,
                                      |    others reduced or boundary)
                                      |
                                      +->  radial_trajectory (per-step ILR
                                      |    norm, preserved as first-class)
                                      |
                                      +->  helmsman_family channels
                                      |
                                      +->  attractor_fit (period, stability,
                                      |    contraction, amplitude, damping)
                                      |
                                      +->  twin_quaternion_factoring  (D=8)
                                      |
                                      +->  chsh_diagnostic (when bundle or D=8)
                                      |
                                      +->  diagnostics (warnings, content_sha256)

Output is CoDa-community vocabulary throughout. Domain interpretation lives
in wrappers (HCI-CNQ/wrappers/), not in this engine.

License:   Apache-2.0
Lineage:   v0.29.0 freezes v1.0.0 for legacy reproducibility; v2.0.0 generalises
Catalog:   INV-037 (CNQ v2 build), INV-038 (engine-independence policy),
           INV-029 (twin-quaternion factoring graduates),
           INV-035 (CHSH coherence graduates),
           INV-039 (radial-vs-bearing scope clarified),
           INV-045 (Suspicion of Every Assumption methodology applied)

See:       ai-refresh/CNT_V3_CNQ_V2_DESIGN.md  for architectural rationale
           HCI-CNQ/engine/CNQ_V2_PSEUDOCODE.md for language-agnostic algorithm
           HCI-CNQ/engine/CNQ_V2_SCHEMA.md     for output schema
           HCI-CNQ/engine/ANTI_SPECIFICATION.md for failure-mode enumeration
           HCI-CNQ/wrappers/wrapper_audio.json  for first domain wrapper
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

_THIS_FILE = Path(__file__).resolve()
for _candidate in (_THIS_FILE.parent.parent.parent, _THIS_FILE.parent.parent.parent.parent):
    if (_candidate / "hci_shared" / "__init__.py").exists():
        sys.path.insert(0, str(_candidate))
        break

from hci_shared import (  # noqa: E402
    canonical_sha256,
    file_sha256,
    helmert_basis,
    InvalidInputError,
    quaternion_sandwich_residuals,
    validate_rows,
)
from hci_shared.geometry import (  # noqa: E402
    closure as _shared_closure,
    clr as _shared_clr,
    compositions_to_helmert_unit_vectors,
    compositions_to_ilr,
)
from hci_shared.attractors import fit_attractor  # noqa: E402
from hci_shared.helmsman import compute_helmsman_family  # noqa: E402
from hci_shared.factoring import (  # noqa: E402
    chsh_S_value,
    CLASSICAL_BOUND,
    TSIRELSON_BOUND,
    twin_quaternion_factor,
)


# ---------------------------------------------------------------------------
# USER CONFIG
# ---------------------------------------------------------------------------

ENGINE_NAME: str = "HCI-CNQ"
ENGINE_VERSION: str = "2.0.0"
SCHEMA_VERSION: str = "cnq/2.0.0"
ENGINE_PRINCIPLE: str = "CNT measures invariance. CNQ names the algebra it lives in."

DEFAULT_DELTA: float = 1e-15
GATE_THRESHOLD: float = 1e-12
HELMSMAN_ROLLING_WINDOW: int = 8


# ---------------------------------------------------------------------------
# Dimension policy classifier
# ---------------------------------------------------------------------------


def classify_dimension(D: int) -> Dict[str, Any]:
    """Return the (label, algebra, processing, claim_strength) tuple for D.

    See ai-refresh/CNT_V3_CNQ_V2_DESIGN.md §5.3 for the locked policy table.
    Labels are mathematically neutral; domain interpretation lives in wrappers.
    """
    if D == 8:
        return {
            "D": 8,
            "label": "twin_quaternion_native",
            "algebra": (
                "D=8 admits twin-quaternion factoring: two coupled SU(2) "
                "elements (q_A, q_B) acting on disjoint 3-dim ILR subspaces; "
                "coupling angle rho_AB(t) is the load-bearing joint diagnostic"
            ),
            "processing": (
                "Helmert -> R^7 -> twin-quaternion sandwich on (axes [0,1,2], "
                "axes [3,4,5]) plus residual axis 6 -> rho_AB coupling -> "
                "CHSH S-value"
            ),
            "claim_strength": (
                "load-bearing -- smallest case where full algebraic structure "
                "(factoring + joint coherence) becomes simultaneously "
                "non-trivial and necessary"
            ),
        }
    if D == 16:
        return {
            "D": 16,
            "label": "quad_quaternion_native_future",
            "algebra": (
                "D=16 admits quad-quaternion factoring: four coupled SU(2) "
                "elements (q_A, q_B, q_C, q_D); 6 pairwise coupling angles + "
                "4-way joint correlation"
            ),
            "processing": (
                "Helmert -> R^15 -> four 3-dim subspaces -> per-channel "
                "sandwich + 6 coupling angles + CHSH-4"
            ),
            "claim_strength": (
                "schema locked; full implementation in v2.1 when first "
                "dataset of this dimension lands"
            ),
        }
    if D == 4:
        return {
            "D": 4,
            "label": "single_quaternion_native",
            "algebra": (
                "SU(2) double cover of SO(3); single-quaternion sandwich on "
                "R^3 ILR space; no factoring required"
            ),
            "processing": "Helmert -> R^3 -> unit-quaternion sandwich",
            "claim_strength": (
                "simplest closed-form case; widely useful for cross-domain "
                "validation (Backblaze drives, Planck CMB photons, SM "
                "neutrinos all sit here)"
            ),
        }
    if D == 3:
        return {
            "D": 3,
            "label": "boundary_3part_planar_embed",
            "algebra": "SO(2) in R^2; embedded in SO(3) by zero-padding the third axis",
            "processing": "Helmert -> R^2 -> embed (z=0) -> sandwich",
            "claim_strength": "degenerate boundary; planar consistency support",
        }
    if D == 2:
        return {
            "D": 2,
            "label": "degenerate_2part_bearing_only",
            "algebra": "scalar log-ratio only; no rotation degree of freedom",
            "processing": "bearing_only path; quaternion_path null",
            "claim_strength": "degenerate boundary; bearing diagnostic only",
        }
    if 5 <= D <= 15:
        return {
            "D": int(D),
            "label": "reduced_or_projected",
            "algebra": "SO(D-1); CNQ view projects onto first 3 ILR axes (lossy)",
            "processing": (
                "Helmert -> R^(D-1) -> first 3 axes -> sandwich; "
                "captured_step_fraction reported global+mean"
            ),
            "claim_strength": (
                "projection diagnostic -- useful when neither twin nor quad "
                "factoring applies natively"
            ),
        }
    if D >= 17:
        return {
            "D": int(D),
            "label": "reduced_or_projected_high_D",
            "algebra": "SO(D-1); first 3 ILR axes (lossy); future Cl(D-1) extension",
            "processing": "same as D=5..15 path",
            "claim_strength": (
                "projection diagnostic; native algebra extension is INV-044 (open)"
            ),
        }
    return {
        "D": int(D),
        "label": "unsupported",
        "algebra": "n/a",
        "processing": "n/a",
        "claim_strength": "out of scope",
    }


# ---------------------------------------------------------------------------
# Bearing + radial trajectory builders (per dimension policy)
# ---------------------------------------------------------------------------


def _build_per_step_ledger(
    residuals: np.ndarray,
    quats: np.ndarray,
    angles: np.ndarray,
    labels: List[Any],
) -> List[Dict[str, Any]]:
    """Assemble per-step ledger entries with labels preserved (ChatGPT recommendation)."""
    out: List[Dict[str, Any]] = []
    for t in range(residuals.shape[0]):
        out.append(
            {
                "t": int(t),
                "label_start": str(labels[t]) if t < len(labels) else None,
                "label_end": str(labels[t + 1]) if t + 1 < len(labels) else None,
                "q_w": float(quats[t, 0]),
                "q_x": float(quats[t, 1]),
                "q_y": float(quats[t, 2]),
                "q_z": float(quats[t, 3]),
                "angle_rad": float(angles[t]),
                "residual_linf": float(residuals[t]),
            }
        )
    return out


def build_bearing_trajectory_d4(
    rows: np.ndarray, labels: List[Any]
) -> Dict[str, Any]:
    """D=4 native: full ILR -> unit vectors in R^3 -> sandwich residuals."""
    units, _radii = compositions_to_helmert_unit_vectors(rows, D=4)
    residuals, quats, angles = quaternion_sandwich_residuals(units)
    return _bearing_trajectory_block(residuals, quats, angles, labels)


def build_bearing_trajectory_d3(
    rows: np.ndarray, labels: List[Any]
) -> Dict[str, Any]:
    """D=3: ILR in R^2, zero-padded into R^3, then sandwich."""
    ilr, radii = compositions_to_ilr(rows, D=3)
    T = ilr.shape[0]
    pad = np.zeros((T, 3), dtype=np.float64)
    pad[:, :2] = ilr
    norms = np.linalg.norm(pad, axis=1)
    safe = norms > 1e-15
    units = np.zeros_like(pad)
    units[safe] = pad[safe] / norms[safe, None]
    residuals, quats, angles = quaternion_sandwich_residuals(units)
    block = _bearing_trajectory_block(residuals, quats, angles, labels)
    block["projection_method"] = "zero_pad_z"
    return block


def build_bearing_trajectory_reduced(
    rows: np.ndarray, D: int, labels: List[Any]
) -> Dict[str, Any]:
    """D>=5 (excluding 8 and 16 native cases): first 3 ILR axes + sandwich residuals.

    Reports both per-step-mean and global captured-step-fraction (ChatGPT
    recommendation: per-step-then-mean overweights small-motion steps; global
    sum-of-squares ratio is more stable as a corpus-level diagnostic).
    """
    ilr, _radii = compositions_to_ilr(rows, D=D)
    full_step = ilr[1:] - ilr[:-1]
    red_step = full_step[:, :3]
    full_norm2 = (full_step ** 2).sum(axis=1)
    red_norm2 = (red_step ** 2).sum(axis=1)
    safe = full_norm2 > 1e-30
    if safe.sum() > 0:
        per_step_ratio = np.where(safe, red_norm2 / np.where(safe, full_norm2, 1.0), 1.0)
        captured_mean = float(per_step_ratio.mean())
        captured_global = float(red_norm2.sum() / max(full_norm2.sum(), 1e-30))
    else:
        captured_mean = 1.0
        captured_global = 1.0
    sub = ilr[:, :3]
    norms = np.linalg.norm(sub, axis=1)
    safe = norms > 1e-15
    units = np.zeros_like(sub)
    units[safe] = sub[safe] / norms[safe, None]
    residuals, quats, angles = quaternion_sandwich_residuals(units)
    block = _bearing_trajectory_block(residuals, quats, angles, labels)
    block["projection_method"] = "first_three_helmert_axes"
    block["captured_step_fraction_mean"] = captured_mean
    block["captured_step_fraction_global"] = captured_global
    return block


def _bearing_trajectory_block(
    residuals: np.ndarray,
    quats: np.ndarray,
    angles: np.ndarray,
    labels: List[Any],
) -> Dict[str, Any]:
    n_pairs = int(residuals.shape[0])
    if n_pairs > 0:
        max_r = float(residuals.max())
        mean_r = float(residuals.mean())
    else:
        max_r = None
        mean_r = None
    return {
        "n_pairs_tested": n_pairs,
        "max_residual": max_r,
        "mean_residual": mean_r,
        "gate_threshold": GATE_THRESHOLD,
        "gate_pass": (max_r is not None and max_r < GATE_THRESHOLD),
        "per_step": _build_per_step_ledger(residuals, quats, angles, labels),
    }


def build_bearing_trajectory_d2(rows: np.ndarray, labels: List[Any]) -> Dict[str, Any]:
    """D=2: scalar log-ratio only; bearing-only path, quaternion_path is null."""
    ilr, _radii = compositions_to_ilr(rows, D=2)
    return {
        "n_pairs_tested": 0,
        "max_residual": None,
        "mean_residual": None,
        "gate_threshold": GATE_THRESHOLD,
        "gate_pass": False,
        "per_step": [],
        "_note": "D=2: bearing-only path; quaternion sandwich does not apply.",
    }


def build_radial_trajectory(rows: np.ndarray, D: int) -> Dict[str, Any]:
    """Per-step ILR norm series (radial trajectory) plus distribution summary.

    First-class output in v2 (was thrown away in v1 by unit-vector normalisation).
    """
    ilr, radii = compositions_to_ilr(rows, D=D)
    if radii.size == 0:
        return {
            "ilr_norms": [],
            "min": None, "max": None, "mean": None, "median": None, "std": None,
        }
    return {
        "ilr_norms": [float(x) for x in radii],
        "min": float(radii.min()),
        "max": float(radii.max()),
        "mean": float(radii.mean()),
        "median": float(np.median(radii)),
        "std": float(radii.std(ddof=0)),
    }


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------


def ingest_csv(input_csv: Path) -> Tuple[List[Any], List[str], np.ndarray, int]:
    """Read a compositional CSV: first column = label, remaining = carriers.

    Strict ingest (errors='strict'); zero-replacement counted; rejects bad shape.
    """
    p = Path(input_csv)
    if not p.exists():
        raise FileNotFoundError(f"input CSV not found: {p}")
    with p.open("r", encoding="utf-8", errors="strict", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        if len(header) < 2:
            raise InvalidInputError(
                f"input CSV header must have at least 2 columns; got {len(header)}"
            )
        carrier_names = [str(c).strip() for c in header[1:]]
        labels: List[Any] = []
        rows_list: List[List[float]] = []
        zero_count = 0
        for line_no, row in enumerate(reader, start=2):
            if not row or all(not c.strip() for c in row):
                continue
            if len(row) != len(header):
                raise InvalidInputError(
                    f"input CSV line {line_no}: expected {len(header)} columns, got {len(row)}"
                )
            labels.append(row[0])
            try:
                vals = [float(x) for x in row[1:]]
            except ValueError as e:
                raise InvalidInputError(
                    f"input CSV line {line_no}: non-numeric carrier value: {e}"
                )
            for k, v in enumerate(vals):
                if v == 0.0:
                    vals[k] = DEFAULT_DELTA
                    zero_count += 1
            rows_list.append(vals)
    rows = np.asarray(rows_list, dtype=np.float64)
    if rows.size == 0:
        raise InvalidInputError(f"input CSV {p} contained no data rows")
    return labels, carrier_names, rows, zero_count


def load_cnt_reference(cnt_json_path: Optional[Path]) -> Optional[Dict[str, Any]]:
    """Optionally read a CNT JSON for informational reference (NOT hash-chained).

    Per push #32 engine-independence policy: cnt_reference is metadata only.
    The CNQ canonical hash does not depend on CNT output existence or contents.
    """
    if cnt_json_path is None:
        return None
    p = Path(cnt_json_path)
    if not p.exists():
        return {
            "cnt_engine_version": None,
            "cnt_schema_version": None,
            "cnt_content_sha256": None,
            "cnt_json_path": str(p),
            "_note": "CNT JSON path provided but file not found; reference field set to nulls.",
        }
    try:
        cnt = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return {
            "cnt_engine_version": None,
            "cnt_schema_version": None,
            "cnt_content_sha256": None,
            "cnt_json_path": str(p),
            "_note": f"CNT JSON could not be parsed: {e}",
        }
    md = cnt.get("metadata", {})
    diag = cnt.get("diagnostics", {})
    return {
        "cnt_engine_version": md.get("engine_version"),
        "cnt_schema_version": md.get("schema_version"),
        "cnt_content_sha256": diag.get("cnt_content_sha256") or diag.get("content_sha256"),
        "cnt_json_path": str(p),
    }


def get_environment_metadata(repo_root: Optional[Path] = None) -> Dict[str, Any]:
    git_sha = None
    if repo_root is not None:
        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0:
                git_sha = res.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            git_sha = None
    hostname_hash = hashlib.sha256(socket.gethostname().encode("utf-8")).hexdigest()[:16]
    return {
        "git_sha": git_sha,
        "python_version": sys.version.split()[0],
        "numpy_version": np.__version__,
        "platform": platform.platform(),
        "hostname_hash": hostname_hash,
    }


# ---------------------------------------------------------------------------
# Top-level orchestration
# ---------------------------------------------------------------------------


def cnq_run(
    *,
    input_csv: Optional[Path] = None,
    cnt_json_path: Optional[Path] = None,
    out_path: Optional[Path] = None,
    repo_root: Optional[Path] = None,
    engine_config_overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """End-to-end CNQ v2.0.0 run.

    Reads a CSV (preferred) and optionally a CNT JSON (informational reference,
    not hash-chained), validates, builds the analytic pipeline, assembles the
    output payload, computes the canonical content hash, and (optionally)
    writes JSON to disk.
    """
    t0 = time.monotonic()
    overrides = dict(engine_config_overrides or {})

    if input_csv is None:
        raise InvalidInputError(
            "cnq_run: input_csv is required (CNQ v2 is a native dataset producer; "
            "CNT JSON ingestion is optional reference only)"
        )

    labels, carrier_names, rows, zero_count = ingest_csv(Path(input_csv))
    rows = validate_rows(rows, min_carriers=2)
    T, D = rows.shape

    dim_policy = classify_dimension(D)

    # Helmert basis is shared between CNT and CNQ via hci_shared.geometry.
    H = helmert_basis(D)

    # --- Bearing trajectory dispatch by dimension policy ---
    bearing_only_block: Optional[Dict[str, Any]] = None
    twin_factor_block: Optional[Dict[str, Any]] = None
    quad_factor_block: Optional[Dict[str, Any]] = None
    chsh_block: Optional[Dict[str, Any]] = None

    if D == 4:
        bearing_block = build_bearing_trajectory_d4(rows, labels)
        bearing_block["projection_method"] = "exact"
    elif D == 3:
        bearing_block = build_bearing_trajectory_d3(rows, labels)
    elif D == 2:
        bearing_block = build_bearing_trajectory_d2(rows, labels)
        ilr, _ = compositions_to_ilr(rows, D=2)
        bearing_only_block = {
            "ilr": [float(x) for x in ilr.flatten()],
            "note": "D=2 has no rotation degree of freedom; bearing-only path.",
        }
    elif D == 8:
        bearing_block = build_bearing_trajectory_reduced(rows, D, labels)
        bearing_block["projection_method"] = "reduced_for_overall_view"
        twin_factor_block = twin_quaternion_factor(rows)
        # CHSH on the twin factor's per-step quaternions.
        per_a = twin_factor_block["factor_A"]["per_step"]
        per_b = twin_factor_block["factor_B"]["per_step"]
        if per_a and per_b and len(per_a) == len(per_b):
            qA = np.array([[s["q_w"], s["q_x"], s["q_y"], s["q_z"]] for s in per_a])
            qB = np.array([[s["q_w"], s["q_x"], s["q_y"], s["q_z"]] for s in per_b])
            chsh_block = chsh_S_value(qA, qB)
    elif D == 16:
        bearing_block = build_bearing_trajectory_reduced(rows, D, labels)
        bearing_block["projection_method"] = "reduced_for_overall_view"
        quad_factor_block = {
            "enabled": False,
            "_note": (
                "D=16 quad-quaternion factoring is schema-locked but not yet "
                "implemented (INV-043; v2.1 ships the implementation when the "
                "first D=16 dataset lands)."
            ),
        }
    else:
        bearing_block = build_bearing_trajectory_reduced(rows, D, labels)

    # --- Radial trajectory (always emitted) ---
    radial_block = build_radial_trajectory(rows, D)

    # --- Helmsman + attractor (always) ---
    helmsman = compute_helmsman_family(rows, window=HELMSMAN_ROLLING_WINDOW)
    attractor = fit_attractor(rows)

    # --- Source hash + environment ---
    source_hash = file_sha256(Path(input_csv))
    env = get_environment_metadata(repo_root=repo_root)

    cnt_ref = load_cnt_reference(cnt_json_path)

    wall_clock_ms = int((time.monotonic() - t0) * 1000.0)

    payload: Dict[str, Any] = {
        "metadata": {
            "engine": ENGINE_NAME,
            "engine_version": ENGINE_VERSION,
            "schema_version": SCHEMA_VERSION,
            "engine_implementation": "python",
            "implementation_lang_version": f"Python {sys.version.split()[0]}",
            "principle": ENGINE_PRINCIPLE,
            "engine_config": {
                "active_overrides": overrides,
                "defaults_in_use": {
                    "DEFAULT_DELTA": DEFAULT_DELTA,
                    "GATE_THRESHOLD": GATE_THRESHOLD,
                    "HELMSMAN_ROLLING_WINDOW": HELMSMAN_ROLLING_WINDOW,
                    "CLASSICAL_BOUND": CLASSICAL_BOUND,
                    "TSIRELSON_BOUND": TSIRELSON_BOUND,
                },
            },
            "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "wall_clock_ms": wall_clock_ms,
            "environment": env,
        },
        "input": {
            "source_file": str(input_csv),
            "source_file_sha256": source_hash,
            "n_records": int(T),
            "n_carriers": int(D),
            "carriers": list(carrier_names),
            "labels": [str(label) for label in labels],
            "zero_replacement_count": int(zero_count),
        },
        "cnt_reference": cnt_ref,
        "cnq_view": {
            "dimension_policy": dim_policy,
            "frame": {
                "type": "Helmert orthonormal contrast",
                "signature": "row k has (k+1) entries +1/sqrt(n*(n+1)) followed by -n/sqrt(n*(n+1))",
                "basis_matrix": H.tolist(),
            },
            "bearing_trajectory": bearing_block,
            "radial_trajectory": radial_block,
            "bearing_only": bearing_only_block,
        },
        "helmsman_family": helmsman,
        "attractor_fit": attractor,
        "twin_quaternion_factoring": twin_factor_block,
        "quad_quaternion_factoring": quad_factor_block,
        "chsh_diagnostic": chsh_block,
        "bundle_view": None,
        "diagnostics": {
            "warnings": [],
        },
    }

    # Compute content hash last (not hash-chained to CNT).
    digest = canonical_sha256(payload)
    payload["diagnostics"]["cnq_content_sha256"] = digest

    if out_path is not None:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with Path(out_path).open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    return payload


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="hs-cnq",
        description=f"{ENGINE_NAME} v{ENGINE_VERSION} compositional navigation quaternion engine",
    )
    p.add_argument("--input-csv", type=str, required=False, default=None,
                   help="Path to compositional input CSV (label column + D carriers)")
    p.add_argument("--cnt-json", type=str, default=None,
                   help="Optional CNT JSON path for informational cross-reference (NOT hash-chained)")
    p.add_argument("-o", "--output", type=str, default=None, help="Output JSON path")
    p.add_argument("--repo-root", type=str, default=None)
    p.add_argument("--self-test", action="store_true",
                   help="Run BIST self-test instead of normal engine invocation")
    p.add_argument("--version", action="version",
                   version=f"{ENGINE_NAME} v{ENGINE_VERSION} (schema {SCHEMA_VERSION})")
    return p


def self_test() -> int:
    """Run the standard self-test corpus and emit a dated, hash-signed receipt."""
    self_test_dir = _THIS_FILE.parent / "self_test"
    runner = self_test_dir / "run_self_test.py"
    if not runner.exists():
        print(f"FATAL: self-test runner not found at {runner}", file=sys.stderr)
        return 2
    if str(self_test_dir) not in sys.path:
        sys.path.insert(0, str(self_test_dir))
    import importlib.util
    spec = importlib.util.spec_from_file_location("cnq_self_test_runner", runner)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return int(mod.run())


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.self_test:
        return self_test()
    if args.input_csv is None:
        print("error: --input-csv is required (or use --self-test for BIST)", file=sys.stderr)
        return 2
    repo_root = Path(args.repo_root) if args.repo_root else None
    out_path = Path(args.output) if args.output else None
    cnt_json = Path(args.cnt_json) if args.cnt_json else None
    payload = cnq_run(
        input_csv=Path(args.input_csv),
        cnt_json_path=cnt_json,
        out_path=out_path,
        repo_root=repo_root,
    )
    md = payload["metadata"]
    inp = payload["input"]
    cv = payload["cnq_view"]
    diag = payload["diagnostics"]
    print(f"engine             = {md['engine']} v{md['engine_version']} (schema {md['schema_version']})")
    print(f"input              = {inp['source_file']}")
    print(f"T x D              = {inp['n_records']} x {inp['n_carriers']}")
    print(f"dimension_policy   = {cv['dimension_policy']['label']}")
    bt = cv['bearing_trajectory']
    if bt.get("max_residual") is not None:
        print(f"bearing.max_residual = {bt['max_residual']:.3e} (gate: {'PASS' if bt['gate_pass'] else 'FAIL'})")
    print(f"radial.mean        = {cv['radial_trajectory'].get('mean')}")
    af = payload['attractor_fit']
    print(f"attractor.fitted   = {af.get('fitted')}, period={af.get('period')}, stability={af.get('period_stability', 0):.4f}")
    if payload['twin_quaternion_factoring'] is not None and payload['twin_quaternion_factoring'].get('enabled'):
        twin = payload['twin_quaternion_factoring']
        print(f"twin.rho_AB.mean   = {twin['coupling']['rho_AB_summary']['mean']:.4f}, class={twin['coupling']['coherence_class']}")
    if payload['chsh_diagnostic'] is not None and payload['chsh_diagnostic'].get('enabled'):
        ch = payload['chsh_diagnostic']
        print(f"CHSH.S_value       = {ch['S_value']:.4f}, verdict={ch['coherence_verdict']}")
    print(f"helmsman.flips     = {payload['helmsman_family']['flips']['total']}")
    print(f"cnq_content_sha256 = {diag['cnq_content_sha256']}")
    if out_path:
        print(f"written            = {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

