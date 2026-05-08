#!/usr/bin/env python3
"""HCI-CNQ — Compositional Navigation Quaternion engine.

The compiled sibling to cnt.py. Reads CNT JSON output (or runs CNT
itself via the adapter), then computes the quaternion-native view of
the same compositional trajectory and emits a hash-chained CNQ JSON.

Design contract
---------------
1. CNQ inherits from CNT. CNQ does not modify the canonical CNT engine
   and does not produce its own CNT-style termination codes; those are
   carried forward verbatim from the parent CNT JSON.

2. The CNQ output carries TWO content hashes:
       parent_cnt_content_sha256  - copied from CNT JSON (provenance chain)
       cnq_content_sha256         - computed over the canonical CNQ payload
   Two independent runs on the same CNT JSON must produce identical
   cnq_content_sha256. This is the cross-platform reproduction channel.

3. Dimension policy is explicit and visible in the output:
       D == 4  -> native_quaternion           (load-bearing case)
       D == 3  -> boundary_or_degenerate_support  (consistency channel)
       D == 8  -> bi_quaternion_factoring_candidate  (DEFERRED, scaffolded)
       D == 2  -> degenerate_below_quaternion (bearing-only)
       D >= 5  (not 8): reduced_or_projected  (project to first 3 ILR axes)

4. Determinism: canonical JSON, sorted keys, stripped clock fields.

5. Portability: no hardcoded paths. Auto-detect repo root, accept
   --repo-root and --cnt-engine flags. See cnt_adapter for details.

Usage
-----
    # From a CNT JSON (no CSV required):
    python cnq.py --cnt-json path/to/cnt.json --out path/to/cnq.json

    # From a raw CSV (runs CNT first, then CNQ):
    python cnq.py --input-csv path/to/input.csv --out path/to/cnq.json

    # Explicit overrides:
    python cnq.py --input-csv data.csv --out cnq.json \\
        --repo-root /path/to/higgins-decomposition \\
        --cnt-engine /path/to/cnt.py

Cross-platform reproduction challenge
-------------------------------------
This engine is shipped to invite ChatGPT, Grok, and any other AI
platform to run it against the same CNT JSON and produce their own
cnq_content_sha256. If hashes match across platforms, that is a fourth
independent confirmation channel beyond Backblaze, Planck, and the SM
neutrino result.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import sys
from pathlib import Path
from typing import Optional

import numpy as np

# Make sibling modules importable when run as a script.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from cnt_adapter import (  # noqa: E402
    add_repo_root_arg,
    extract_cnt_diagnostics,
    find_cnt_engine,
    find_repo_root,
    load_cnt_json,
    run_cnt,
)
from geometry import (  # noqa: E402
    closure,
    clr,
    compositions_to_helmert_unit_vectors,
    helmert_basis,
    quat_conj,
    quat_mul,
    quat_rotate,
    quaternion_sandwich_residuals,
    rotation_quaternion_between,
)
from hashing import canonical_sha256, file_sha256  # noqa: E402

CNQ_ENGINE_VERSION = "1.0.0"
CNQ_SCHEMA_VERSION = "cnq/1.0.0"
GATE_THRESHOLD = 1e-12  # IEEE-floor gate for D=4 quaternion sandwich


# ── Dimension policy ──────────────────────────────────────────────────

def classify_dimension(D: int) -> dict:
    """Return the dimension scope label and processing policy."""
    if D == 4:
        return {
            "D": 4,
            "label": "native_quaternion",
            "algebra": "SU(2) double cover of SO(3); Aitchison rotation in R^3",
            "processing": "Helmert -> R^3 -> unit-quaternion sandwich",
            "claim_strength": "confirmed (load-bearing case for the framework)",
        }
    if D == 3:
        return {
            "D": 3,
            "label": "boundary_or_degenerate_support",
            "algebra": "SO(2)-equivalent in R^2; promoted to R^3 by zero-padding",
            "processing": "Helmert -> R^2 -> embed in R^3 with z=0 -> sandwich",
            "claim_strength": "consistency support, not native D=4 quaternion proof",
        }
    if D == 2:
        return {
            "D": 2,
            "label": "degenerate_below_quaternion",
            "algebra": "scalar log-ratio only; no rotation degree of freedom",
            "processing": "bearing computation only",
            "claim_strength": "boundary diagnostic; quaternion view does not apply",
        }
    if D == 8:
        return {
            "D": 8,
            "label": "bi_quaternion_factoring_candidate",
            "algebra": "SO(8) ⊃ SU(2) × SU(2); two coupled quaternion paths",
            "processing": "Helmert -> R^7; reduced view = first 3 axes; "
                          "bi-quaternion factoring scaffolded but DEFERRED (INV-029)",
            "claim_strength": "experimental; full algebra extension pending pilot",
        }
    if D >= 5:
        return {
            "D": D,
            "label": "reduced_or_projected",
            "algebra": f"SO({D-1}); projection to first 3 ILR axes for the CNQ view",
            "processing": f"Helmert -> R^{D-1} -> first 3 axes -> sandwich (lossy)",
            "claim_strength": "projection diagnostic only; full extension via Clifford "
                              "Cl(D-1) is DEFERRED",
        }
    return {
        "D": D,
        "label": "unsupported",
        "algebra": "n/a",
        "processing": "n/a",
        "claim_strength": "out of scope",
    }


# ── Input handling ────────────────────────────────────────────────────

def read_csv_compositions(input_csv: Path):
    """Read a CCTT-style CSV: first column is a label/index, remaining
    columns are the carriers. Returns (label_col, carrier_names, rows).
    """
    p = Path(input_csv).resolve()
    with p.open() as f:
        reader = csv.reader(f)
        header = next(reader)
        carrier_names = header[1:]
        rows = []
        labels = []
        for row in reader:
            if not row:
                continue
            labels.append(row[0])
            rows.append([float(v) for v in row[1:]])
    return header[0], carrier_names, labels, rows


def reconstruct_compositions_from_cnt(cnt_json: dict):
    """If a CNT JSON includes the input rows (newer schema does), pull
    them back. Otherwise return None and the caller must supply a CSV.

    CNT 2.1.x stores input rows under input.rows or input.compositions
    depending on schema version. We probe the common locations.
    """
    inp = cnt_json.get("input", {}) or {}
    rows = inp.get("rows") or inp.get("compositions")
    carriers = inp.get("carrier_names") or inp.get("carriers")
    if rows and carriers:
        return list(carriers), rows
    return None, None


# ── Core CNQ computation ──────────────────────────────────────────────

def run_cnq_view(rows, carrier_names, dimension_policy: dict) -> dict:
    """The quaternion-native view: closure -> CLR -> Helmert -> unit
    vectors -> per-step sandwich quaternions and residuals.

    Returns a structured dict with all per-step quantities and the
    residual summary. The schema is documented in CNQ_SCHEMA.md.
    """
    rows = np.asarray(rows, dtype=float)
    T, D = rows.shape
    if D != dimension_policy["D"]:
        raise ValueError(
            f"Row dimension {D} != declared policy D={dimension_policy['D']}"
        )

    # 1. Closure + CLR + Helmert
    closed = np.array([closure(r) for r in rows])
    clr_vecs = np.array([clr(c) for c in closed])
    H = helmert_basis(D)
    ilr = clr_vecs @ H.T  # (T, D-1)
    radii_full = np.linalg.norm(ilr, axis=1)

    # 2. Project to R^3 according to dimension policy.
    if D == 4:
        ilr3 = ilr  # already in R^3
        capture_note = "exact (D=4 native; no projection loss)"
    elif D == 3:
        # ilr is (T, 2); embed in R^3 with z = 0
        ilr3 = np.column_stack([ilr, np.zeros(T)])
        capture_note = "D=3 boundary; embedded in R^3 with z=0"
    elif D == 2:
        # ilr is (T, 1); cannot form a R^3 unit vector — bearing only.
        return {
            "dimension_policy": dimension_policy,
            "quaternion_path": None,
            "bearing_only": {
                "ilr": ilr.flatten().tolist(),
                "note": "D=2 has no rotation degree of freedom; bearing only.",
            },
        }
    else:
        # D >= 5 (or D = 8): reduced view = first 3 ILR axes
        ilr3 = ilr[:, :3]
        capture_note = (
            f"D={D}; first 3 ILR axes used as reduced view. "
            f"Full ILR has {D-1} axes."
        )

    # 3. Captured energy fraction (per ChatGPT round-2 audit)
    captured_step_fraction = None
    if D == 4 or D == 3 or D == 2:
        captured_step_fraction = 1.0
    else:
        # ratio of squared first-3-axis displacements to full displacements
        full_steps = np.diff(ilr, axis=0)
        red_steps = np.diff(ilr3, axis=0)
        full_norm2 = np.sum(full_steps ** 2, axis=1)
        red_norm2 = np.sum(red_steps ** 2, axis=1)
        # Avoid divide-by-zero on stationary steps.
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(full_norm2 > 1e-30, red_norm2 / full_norm2, 1.0)
        captured_step_fraction = float(np.mean(ratio))

    # 4. Normalize to S^2 and run the sandwich-product reconstruction.
    radii3 = np.linalg.norm(ilr3, axis=1)
    safe_radii = np.where(radii3 > 1e-15, radii3, 1.0)
    units = ilr3 / safe_radii[:, None]
    units[radii3 <= 1e-15] = 0.0

    residuals, quats, angles = quaternion_sandwich_residuals(units)

    # 5. Summary
    n_pairs = len(residuals)
    if n_pairs > 0:
        max_residual = float(residuals.max())
        mean_residual = float(residuals.mean())
        gate_pass = bool(max_residual <= GATE_THRESHOLD)
    else:
        max_residual = float("nan")
        mean_residual = float("nan")
        gate_pass = False

    # 6. Per-step ledger (rounded to a float64-stable representation)
    # We keep raw floats; canonical_dumps will format them consistently.
    per_step = []
    for t in range(n_pairs):
        per_step.append({
            "t": t,
            "u_start": units[t].tolist(),
            "u_end": units[t + 1].tolist(),
            "q_w": float(quats[t][0]),
            "q_x": float(quats[t][1]),
            "q_y": float(quats[t][2]),
            "q_z": float(quats[t][3]),
            "angle_rad": float(angles[t]),
            "residual_linf": float(residuals[t]),
        })

    return {
        "dimension_policy": dimension_policy,
        "n_records_T": T,
        "n_carriers_D": D,
        "carrier_names": list(carrier_names),
        "frame_type": "Helmert orthonormal contrast (legacy QD convention)",
        "frame_signature": "row k: 1/sqrt(k(k+1)) [k blocks of +1, then -k]",
        "projection_to_R3": {
            "method": (
                "exact" if D == 4
                else ("zero-padded R^2 -> R^3" if D == 3
                else ("first 3 ILR axes" if D >= 5 else "n/a"))
            ),
            "note": capture_note,
        },
        "captured_step_fraction": captured_step_fraction,
        "quaternion_path": {
            "n_pairs_tested": n_pairs,
            "max_residual": max_residual,
            "mean_residual": mean_residual,
            "gate_threshold": GATE_THRESHOLD,
            "gate_pass": gate_pass,
            "per_step": per_step,
        },
        "radii": {
            "min": float(radii3.min()) if T > 0 else 0.0,
            "max": float(radii3.max()) if T > 0 else 0.0,
            "mean": float(radii3.mean()) if T > 0 else 0.0,
        },
    }


# ── Output assembly ───────────────────────────────────────────────────

def assemble_cnq_output(
    cnt_json: dict,
    cnt_diag: dict,
    cnq_view: dict,
    *,
    cnt_json_path: Optional[Path] = None,
    input_csv_path: Optional[Path] = None,
) -> dict:
    """Build the final CNQ JSON payload with the determinism contract.

    The 'metadata.generated' timestamp is recorded but stripped from
    the canonical hash. Two runs produce identical cnq_content_sha256.
    """
    # Provenance chain
    parent_hash = cnt_diag.get("content_sha256")
    source_hash = cnt_diag.get("source_file_sha256")
    if input_csv_path and not source_hash:
        source_hash = file_sha256(input_csv_path)

    # Build the full payload first (without cnq_content_sha256), then
    # compute the hash and patch it back in.
    payload = {
        "metadata": {
            "schema": CNQ_SCHEMA_VERSION,
            "engine": "HCI-CNQ",
            "engine_version": CNQ_ENGINE_VERSION,
            "generated": dt.datetime.utcnow().isoformat() + "Z",
            "principle": "CNT measures invariance. CNQ names the algebra it lives in.",
        },
        "provenance": {
            "parent_engine": "HCI-CNT",
            "parent_engine_version": cnt_diag.get("cnt_engine_version"),
            "parent_schema": cnt_diag.get("cnt_schema_version"),
            "parent_cnt_content_sha256": parent_hash,
            "source_file_sha256": source_hash,
            "cnt_json_path": str(cnt_json_path) if cnt_json_path else None,
            "input_csv_path": str(input_csv_path) if input_csv_path else None,
        },
        "cnt_diagnostics_carried_forward": {
            "cnt_termination": cnt_diag.get("cnt_termination"),
            "ir_class": cnt_diag.get("ir_class"),
            "amplitude_A": cnt_diag.get("amplitude_A"),
            "damping_zeta": cnt_diag.get("damping_zeta"),
            "helmsman_sigma": cnt_diag.get("helmsman_sigma"),
        },
        "cnq_view": cnq_view,
    }

    # Compute the cnq content hash over the canonical payload.
    cnq_hash = canonical_sha256(payload)
    payload["cnq_content_sha256"] = cnq_hash
    return payload


# ── Top-level entry point ─────────────────────────────────────────────

def run_cnq(
    *,
    cnt_json_path: Optional[Path] = None,
    input_csv_path: Optional[Path] = None,
    out_path: Path,
    repo_root: Optional[Path] = None,
    cnt_engine: Optional[Path] = None,
    cnt_extra_args: Optional[list] = None,
) -> dict:
    """Full CNQ run.

    Either cnt_json_path or input_csv_path must be provided.
    If both are None, raises ValueError. If only input_csv is given,
    CNT is invoked first (via cnt_adapter) and the resulting JSON is
    written next to out_path.
    """
    if cnt_json_path is None and input_csv_path is None:
        raise ValueError("Provide either --cnt-json or --input-csv.")

    repo_root_resolved = find_repo_root(explicit=repo_root) if (
        cnt_json_path is None or input_csv_path is not None
    ) else None

    # Step A: get a CNT JSON in hand.
    if cnt_json_path is None:
        # Run CNT first.
        engine_path = find_cnt_engine(repo_root_resolved, explicit=cnt_engine)
        cnt_json_path = out_path.with_suffix(".cnt.json")
        run_cnt(
            input_csv_path,
            cnt_json_path,
            engine_path,
            extra_args=cnt_extra_args,
        )

    cnt_json = load_cnt_json(cnt_json_path)
    cnt_diag = extract_cnt_diagnostics(cnt_json)

    # Step B: get the row-level data.
    # Prefer the CNT JSON's recorded input. Fall back to the CSV.
    carriers, rows = reconstruct_compositions_from_cnt(cnt_json)
    if rows is None:
        if input_csv_path is None:
            raise RuntimeError(
                "CNT JSON does not contain input rows and no --input-csv was "
                "provided. Pass --input-csv to enable CNQ on this CNT JSON."
            )
        _, carriers, _labels, rows = read_csv_compositions(input_csv_path)

    rows = np.asarray(rows, dtype=float)
    D = rows.shape[1]
    policy = classify_dimension(D)

    # Step C: compute the CNQ view.
    cnq_view = run_cnq_view(rows, carriers, policy)

    # Step D: assemble + write.
    payload = assemble_cnq_output(
        cnt_json,
        cnt_diag,
        cnq_view,
        cnt_json_path=cnt_json_path,
        input_csv_path=input_csv_path,
    )

    out_path = Path(out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True, ensure_ascii=True)

    return payload


# ── CLI ───────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cnq",
        description=(
            "HCI-CNQ engine — produce a quaternion-native view of a "
            "compositional trajectory, hash-chained to its parent CNT JSON."
        ),
    )
    p.add_argument(
        "--cnt-json",
        type=Path,
        default=None,
        help="Path to an existing CNT JSON (preferred — skips CNT invocation).",
    )
    p.add_argument(
        "--input-csv",
        type=Path,
        default=None,
        help="Path to a CCTT-style CSV. Required if --cnt-json is omitted "
             "(CNT will be invoked first), or as a fallback for input rows "
             "if the CNT JSON does not record them.",
    )
    p.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output CNQ JSON path.",
    )
    p.add_argument(
        "--cnt-extra-arg",
        action="append",
        default=[],
        help="Extra args to forward to cnt.py (repeatable).",
    )
    add_repo_root_arg(p)
    return p


def main(argv=None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        payload = run_cnq(
            cnt_json_path=args.cnt_json,
            input_csv_path=args.input_csv,
            out_path=args.out,
            repo_root=args.repo_root,
            cnt_engine=args.cnt_engine,
            cnt_extra_args=args.cnt_extra_arg,
        )
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"cnq: ERROR: {e}", file=sys.stderr)
        return 2

    # Print headline summary on stdout for one-line CI reading.
    cv = payload["cnq_view"]
    qp = cv.get("quaternion_path") or {}
    print(f"CNQ: D={cv['n_carriers_D']} T={cv['n_records_T']} "
          f"label={cv['dimension_policy']['label']} "
          f"max_residual={qp.get('max_residual', 'n/a')} "
          f"gate_pass={qp.get('gate_pass', 'n/a')} "
          f"cnq_content_sha256={payload['cnq_content_sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
/a')} "
          f"cnq_content_sha256={payload['cnq_content_sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
