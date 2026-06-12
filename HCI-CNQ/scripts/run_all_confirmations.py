#!/usr/bin/env python3
"""Run the three IEEE-floor confirmation experiments end-to-end via cnq.py.

This is the one-command reproduction entry point referenced in
Paper 1 Appendix A. From a clean clone of the higgins-decomposition repo:

    python HCI-CNQ/scripts/run_all_confirmations.py --repo-root .

What it does:
    1. Locates each experiment's CNT JSON (already shipped in the repo)
    2. Invokes HCI-CNQ/engine/cnq.py against each one
    3. Writes a CNQ JSON next to the source CNT JSON
    4. Reports headline residuals + cnq_content_sha256 per experiment
    5. Returns 0 on success, 1 on any failure

Use verify_publication_results.py for the strict expected-vs-observed
check — this script just runs the experiments and reports.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_REPO_HCI_CNQ = _HERE.parent
sys.path.insert(0, str(_REPO_HCI_CNQ / "engine"))

from cnq import run_cnq  # noqa: E402
from cnt_adapter import find_repo_root  # noqa: E402


# Experiment manifest. Each entry maps a logical name to:
#   - the CNT JSON consumed
#   - the input CSV (for raw rows when CNT JSON does not store them)
#   - the output CNQ JSON path
EXPERIMENTS = [
    {
        "name": "backblaze_fleet_quaternion",
        "input_csv": "HCI/experiments_v2/codawork2026/backblaze_fleet/backblaze_fleet_input.csv",
        "cnt_json": None,  # Will run CNT first if no JSON is in HCI-CNQ/experiments
        "out": "HCI-CNQ/experiments/backblaze_fleet_quaternion/cnq_run.json",
    },
    {
        "name": "planck_cmb_quaternion",
        "input_csv": "HCI-CNQ/experiments/planck_cmb_quaternion/planck_cmb_boson_input.csv",
        "cnt_json": "HCI-CNQ/experiments/planck_cmb_quaternion/planck_cmb_boson_cnt.json",
        "out": "HCI-CNQ/experiments/planck_cmb_quaternion/cnq_run.json",
    },
    {
        "name": "sm_neutrino_quaternion",
        "input_csv": "HCI-CNQ/experiments/sm_neutrino_quaternion/sm_numu_oscillation_input.csv",
        "cnt_json": "HCI-CNQ/experiments/sm_neutrino_quaternion/sm_numu_oscillation_cnt.json",
        "out": "HCI-CNQ/experiments/sm_neutrino_quaternion/cnq_run.json",
    },
]


def _resolve_under(repo_root: Path, rel: str) -> Path:
    """Resolve a path that may live under repo_root or repo_root/Hs."""
    p1 = (repo_root / rel).resolve()
    if p1.exists():
        return p1
    p2 = (repo_root / "Hs" / rel).resolve()
    if p2.exists():
        return p2
    # Return the first candidate — caller will see a clean FileNotFoundError.
    return p1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Run all three CNQ confirmation experiments."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Path to higgins-decomposition (or its Hs/ subdir). "
             "Auto-detected if omitted.",
    )
    parser.add_argument(
        "--cnt-engine",
        type=Path,
        default=None,
        help="Path to cnt.py override.",
    )
    args = parser.parse_args(argv)

    repo_root = find_repo_root(explicit=args.repo_root)
    print(f"[run_all_confirmations] repo_root: {repo_root}")
    print(f"[run_all_confirmations] running {len(EXPERIMENTS)} experiments")
    print("=" * 72)

    summary = []
    failures = 0

    for exp in EXPERIMENTS:
        name = exp["name"]
        print(f"\n[{name}]")
        print("-" * 72)

        cnt_json = _resolve_under(repo_root, exp["cnt_json"]) if exp["cnt_json"] else None
        input_csv = _resolve_under(repo_root, exp["input_csv"]) if exp["input_csv"] else None
        out_path = _resolve_under(repo_root, exp["out"])

        # Prefer existing CNT JSON if it's there (faster + no engine dependency).
        if cnt_json is not None and cnt_json.exists():
            print(f"  CNT JSON: {cnt_json.name} (existing)")
            try:
                payload = run_cnq(
                    cnt_json_path=cnt_json,
                    input_csv_path=input_csv if input_csv and input_csv.exists() else None,
                    out_path=out_path,
                    repo_root=repo_root,
                    cnt_engine=args.cnt_engine,
                )
            except Exception as e:
                print(f"  ERROR: {e}")
                failures += 1
                summary.append({"name": name, "ok": False, "error": str(e)})
                continue
        else:
            # Run CNT first.
            print(f"  CNT JSON: not found; will run CNT on {input_csv}")
            try:
                payload = run_cnq(
                    cnt_json_path=None,
                    input_csv_path=input_csv,
                    out_path=out_path,
                    repo_root=repo_root,
                    cnt_engine=args.cnt_engine,
                )
            except Exception as e:
                print(f"  ERROR: {e}")
                failures += 1
                summary.append({"name": name, "ok": False, "error": str(e)})
                continue

        cv = payload["cnq_view"]
        qp = cv.get("quaternion_path") or {}
        cnq_hash = payload["cnq_content_sha256"]
        parent_hash = payload["provenance"].get("parent_cnt_content_sha256")
        max_res = qp.get("max_residual")
        gate = qp.get("gate_pass")

        print(f"  D = {cv['n_carriers_D']}, T = {cv['n_records_T']}")
        print(f"  dimension label: {cv['dimension_policy']['label']}")
        if max_res is not None:
            print(f"  max residual:    {max_res}")
        print(f"  gate pass:       {gate}")
        print(f"  parent CNT hash: {parent_hash}")
        print(f"  cnq_content_sha256: {cnq_hash}")

        summary.append({
            "name": name,
            "ok": True,
            "D": cv["n_carriers_D"],
            "T": cv["n_records_T"],
            "dimension_label": cv["dimension_policy"]["label"],
            "max_residual": max_res,
            "gate_pass": gate,
            "parent_cnt_content_sha256": parent_hash,
            "cnq_content_sha256": cnq_hash,
            "out": str(out_path),
        })

    print("\n" + "=" * 72)
    print(f"  Summary: {len(summary) - failures} / {len(EXPERIMENTS)} succeeded")
    print("=" * 72)

    summary_path = repo_root / "HCI-CNQ" / "results" / "confirmation_summary.json"
    if not summary_path.parent.exists():
        summary_path = repo_root / "Hs" / "HCI-CNQ" / "results" / "confirmation_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with summary_path.open("w") as f:
        json.dump({
            "experiments": summary,
            "total": len(EXPERIMENTS),
            "failures": failures,
        }, f, indent=2, sort_keys=True)
    print(f"\nSummary written to: {summary_path}")

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
