#!/usr/bin/env python3
"""
HUF-CNT Mission Command — orchestrator for the experiment corpus.

Reads experiments/INDEX.json, locates each experiment's input CSV
inside experiments/<subdir>/<id>/, runs the cnt engine with the
correct ordering, and verifies (or updates) the published
content_sha256.

Two modes:
  --verify  (default)   Run; compare new SHA against INDEX. PASS/FAIL.
  --update              Run; rewrite INDEX with new SHAs (release flow).

Optional master_control.json overrides per-experiment ordering and
engine config. See mission_command/master_control.json for a template.

Usage:
  python mission_command.py                   # verify all 20
  python mission_command.py ember_jpn         # verify one
  python mission_command.py --subset domain   # verify by subdir
  python mission_command.py --update          # rewrite SHAs
  python mission_command.py --status          # summary only
"""
from __future__ import annotations

# ============================================================
# MISSION COMMAND USER CONFIGURATION
# ============================================================
MC_VERSION              = "1.0.0"

# Default ordering when an experiment's INDEX.json entry doesn't specify
DEFAULT_ORDERING_TEMPORAL    = ("by-time",  True)
DEFAULT_ORDERING_NONTEMPORAL = ("by-label", False)

# Per-id ordering overrides — used when neither INDEX nor master_control
# resolves a value. Reflects the canonical published runs (engine 2.0.3).
DEFAULT_ORDERING = {
    "ember_chn":             (True,  "by-time"),
    "ember_deu":             (True,  "by-time"),
    "ember_fra":             (True,  "by-time"),
    "ember_gbr":             (True,  "by-time"),
    "ember_ind":             (True,  "by-time"),
    "ember_jpn":             (True,  "by-time"),
    "ember_usa":             (True,  "by-time"),
    "ember_wld":             (True,  "by-time"),
    "ember_combined_panel":  (True,  "by-label"),
    "backblaze_fleet":       (True,  "by-time"),
    "geochem_ball_region":   (False, "by-label"),
    "geochem_ball_age":      (True,  "by-time"),
    "geochem_ball_tas":      (False, "by-label"),
    "geochem_stracke_oib":   (False, "by-label"),
    "geochem_stracke_morb":  (False, "by-label"),
    "geochem_tappe_kim1":    (False, "by-label"),
    "geochem_qin_cpx":       (False, "by-label"),
    "fao_irrigation_methods":(False, "by-d_A"),
    "commodities_gold_silver":(True, "by-time"),
    "nuclear_semf":          (False, "by-label"),
    # v1.1.x extended battery — 5 deferred adapters built
    "markham_budget":        (True,  "by-time"),
    "iiasa_ngfs":            (True,  "by-time"),
    "esa_planck_cosmic":     (False, "by-label"),
    "financial_sector":      (True,  "by-time"),
    "chemixhub_oxide":       (False, "by-label"),
}

# Verification budget — how many experiments to run before stopping
# on first failure (None = run all, report at end)
STOP_ON_FIRST_FAIL = False

# Auto-generate journal alongside JSON
WRITE_JOURNAL = True
# ============================================================

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PACKAGE_ROOT / "cnt"))
import cnt as cnt_engine

INDEX_PATH = PACKAGE_ROOT / "experiments" / "INDEX.json"
EXPERIMENTS_DIR = PACKAGE_ROOT / "experiments"


# --------------------------------------------------------------
# Resolution helpers
# --------------------------------------------------------------
def load_master_control(path: Path) -> dict:
    if not path.exists():
        return {"experiments": {}, "engine_config_overrides": {}}
    return json.loads(path.read_text())


def resolve_csv(experiment_id: str, subdir: str) -> Path:
    """Find the input CSV inside experiments/<subdir>/<id>/.
    Prefers exact <id>_input.csv, otherwise the first CSV in the folder."""
    folder = EXPERIMENTS_DIR / subdir / experiment_id
    candidates = [
        folder / f"{experiment_id}_input.csv",
        folder / f"{experiment_id}_TWh.csv",
    ] + sorted(folder.glob("*.csv"))
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"No input CSV for {experiment_id} under {folder}")


def resolve_ordering(experiment_id: str, master_ctrl: dict) -> dict:
    """Resolve ordering via master_control override > DEFAULT_ORDERING > inferred."""
    mc_entry = master_ctrl.get("experiments", {}).get(experiment_id, {})
    if "is_temporal" in mc_entry and "ordering_method" in mc_entry:
        is_temporal = mc_entry["is_temporal"]
        method = mc_entry["ordering_method"]
    elif experiment_id in DEFAULT_ORDERING:
        is_temporal, method = DEFAULT_ORDERING[experiment_id]
    else:
        method, is_temporal = DEFAULT_ORDERING_NONTEMPORAL
    return {
        "is_temporal":     is_temporal,
        "ordering_method": method,
        "caveat":          None if is_temporal else
            "Order is treated as arbitrary; angular_velocity and "
            "energy_depth are ordering-dependent.",
    }


# --------------------------------------------------------------
# Run one experiment
# --------------------------------------------------------------
def run_experiment(experiment_id: str, mode: str = "verify",
                   master_ctrl: dict | None = None) -> dict:
    """Run cnt engine on one experiment. Mode: verify | update."""
    master_ctrl = master_ctrl or {"experiments": {}}
    idx = json.loads(INDEX_PATH.read_text())
    if experiment_id not in idx["experiments"]:
        raise SystemExit(f"unknown experiment: {experiment_id}")
    spec = idx["experiments"][experiment_id]
    subdir = spec["subdir"]

    csv_path = resolve_csv(experiment_id, subdir)
    out_json = EXPERIMENTS_DIR / subdir / experiment_id / f"{experiment_id}_cnt.json"
    ordering = resolve_ordering(experiment_id, master_ctrl)

    # Engine-config overrides:
    # 1. global engine_config_overrides at top level
    # 2. per-experiment engine_config_overrides (wins on collision)
    overrides = dict(master_ctrl.get("engine_config_overrides", {}) or {})
    mc_entry = master_ctrl.get("experiments", {}).get(experiment_id, {}) or {}
    overrides.update(mc_entry.get("engine_config_overrides", {}) or {})
    # Drop annotation-only keys (e.g. "_comment")
    overrides = {k: v for k, v in overrides.items() if not k.startswith("_")}

    # v1.1-B native units selection
    input_units         = mc_entry.get("input_units")
    higgins_scale_units = mc_entry.get("higgins_scale_units")

    t0 = time.time()
    cnt_engine.cnt_run(str(csv_path), str(out_json), ordering,
                       engine_config_overrides=overrides or None,
                       input_units=input_units,
                       higgins_scale_units=higgins_scale_units)
    elapsed_ms = int((time.time() - t0) * 1000)

    j = json.loads(out_json.read_text())
    new_sha = j["diagnostics"]["content_sha256"]
    pub_sha = spec.get("content_sha256", "")
    matched = (new_sha == pub_sha)

    result = {
        "id":              experiment_id,
        "subdir":          subdir,
        "csv":             str(csv_path),
        "json":            str(out_json),
        "engine_version":  j["metadata"]["engine_version"],
        "schema_version":  j["metadata"]["schema_version"],
        "n_records":       j["input"]["n_records"],
        "n_carriers":      j["input"]["n_carriers"],
        "ir_class":        j["depth"]["higgins_extensions"]["impulse_response"]["classification"],
        "amplitude_A":     j["depth"]["higgins_extensions"]["impulse_response"]["amplitude_A"],
        "curvature_depth": j["depth"]["higgins_extensions"]["summary"]["curvature_depth"],
        "energy_depth":    j["depth"]["higgins_extensions"]["summary"]["energy_depth"],
        "content_sha256":  new_sha,
        "published_sha":   pub_sha,
        "matched":         matched,
        "wall_clock_ms":   elapsed_ms,
        "ordering":        ordering,
    }

    if WRITE_JOURNAL:
        write_journal(experiment_id, j, result)

    if mode == "update":
        spec["content_sha256"] = new_sha
        spec["n_records"] = j["input"]["n_records"]
        spec["n_carriers"] = j["input"]["n_carriers"]
        spec["wall_clock_ms"] = elapsed_ms
        spec["ir_class"] = result["ir_class"]
        spec["amplitude_A"] = result["amplitude_A"]
        spec["curvature_depth"] = result["curvature_depth"]
        spec["energy_depth"] = result["energy_depth"]
        idx["_meta"]["last_updated"] = datetime.now(timezone.utc).isoformat()
        INDEX_PATH.write_text(json.dumps(idx, indent=2))

    return result


# --------------------------------------------------------------
# Journal writer — small, drives off the JSON
# --------------------------------------------------------------
def write_journal(experiment_id: str, j: dict, result: dict):
    folder = EXPERIMENTS_DIR / result["subdir"] / experiment_id
    journal = folder / "JOURNAL.md"
    md = j["metadata"]
    inp = j["input"]
    di = j["diagnostics"]
    ir = j["depth"]["higgins_extensions"]["impulse_response"]
    ca = j["depth"]["higgins_extensions"]["curvature_attractor"]
    summ = j["depth"]["higgins_extensions"]["summary"]
    invl = j["depth"]["higgins_extensions"]["involution_proof"]

    cls = ir.get("classification", "?")
    A = ir.get("amplitude_A", 0)
    zeta = ir.get("damping_zeta", 0)

    # Conclusion block
    conclusion = _conclusion_for_class(cls, ir, ca, summ, j)

    lines = [
        f"# Experiment Journal — `{experiment_id}`",
        "",
        f"**Engine:** {md['engine_version']}, schema {md['schema_version']}  ",
        f"**Generated:** {md['generated']}  ",
        f"**Run time:** {md['wall_clock_ms']} ms  ",
        f"**content_sha256:** `{di['content_sha256']}`  ",
        "",
        "## Input",
        f"- Source CSV: `{Path(inp['source_file']).name}`",
        f"- Source SHA-256: `{inp.get('source_file_sha256', '?')}`",
        f"- Records (T): **{inp['n_records']}**",
        f"- Carriers (D): **{inp['n_carriers']}**",
        f"- Carriers: {', '.join(inp.get('carriers', []))}",
        f"- Ordering: temporal={inp['ordering']['is_temporal']}, "
        f"method={inp['ordering']['ordering_method']}",
        "",
        "## Headline Results",
        "",
        "| Quantity | Value |",
        "|---|---|",
        f"| Curvature tower depth | **{summ['curvature_depth']}** |",
        f"| Curvature termination | {summ['curvature_termination']} |",
        f"| Energy tower depth    | {summ['energy_depth']} |",
        f"| Energy termination    | {summ['energy_termination']} |",
        f"| M² = I residual       | {invl['mean_residual']:.2e}  "
        f"(verified: {invl['verified']}) |",
        f"| IR classification     | **{cls}** |",
        f"| Amplitude A           | {A if A is None else f'{A:.4f}'} |",
        f"| Damping ζ             | {zeta:.4f} |",
        f"| Period                | {ca.get('period', '—')} |",
        "",
        "## Conclusion (auto-generated by Mission Command)",
        "",
        conclusion,
        "",
        "---",
        f"*Generated by mission_command.py at engine {md['engine_version']}.*",
    ]
    journal.write_text("\n".join(lines))


def _conclusion_for_class(cls, ir, ca, summ, j):
    A = ir.get("amplitude_A") or 0.0
    zeta = ir.get("damping_zeta", 0)
    locks = j["diagnostics"]["higgins_extensions"].get("lock_events", [])
    n_locks = len(locks)
    text = []
    if cls == "CRITICALLY_DAMPED":
        text.append(f"Tight period-2 attractor at small amplitude (A = {A:.4f}, "
                    f"ζ = {zeta:.4f}). The recursion compresses to a narrow "
                    f"attractor band.")
    elif cls == "LIGHTLY_DAMPED":
        text.append(f"Period-2 attractor at moderate amplitude (A = {A:.4f}). "
                    f"The system is well-bounded but exhibits visible amplitude "
                    f"in the limit cycle.")
    elif cls == "MODERATELY_DAMPED":
        text.append(f"Period-2 attractor with substantial amplitude (A = {A:.4f}). "
                    f"Significant compositional structure across records.")
    elif cls == "OVERDAMPED_EXTREME":
        text.append(f"Period-2 attractor at very high amplitude (A = {A:.4f}). "
                    f"The trajectory exhibits large directional swings — "
                    f"frequently a signature of carrier phase-out.")
    elif cls == "ENERGY_STABLE_FIXED_POINT":
        text.append("Energy tower converges to a stable period-1 fixed point. "
                    "The system has a clean resting amplitude.")
    elif cls == "CURVATURE_VERTEX_FLAT":
        text.append("Curvature recursion flattened against a vertex of the "
                    "simplex due to single-carrier dominance > 60%. The "
                    "energy tower may still be productive; consider a "
                    "carrier-renormalisation step before re-examining.")
    elif cls == "D2_DEGENERATE":
        text.append("D = 2: the simplex has a single independent compositional "
                    "axis. The depth tower cannot exercise off-diagonal metric "
                    "structure — this is a fundamental limit, not a bug.")
    else:
        text.append(f"Classification: {cls}.")
    text.append("")
    text.append(f"**Boundary events:** {n_locks} lock event(s) recorded.")
    return " ".join(text)


# --------------------------------------------------------------
# Run all
# --------------------------------------------------------------
def run_all(experiment_ids=None, mode="verify", master_ctrl=None,
            subset=None) -> list:
    idx = json.loads(INDEX_PATH.read_text())
    all_ids = list(idx["experiments"].keys())
    if experiment_ids:
        all_ids = [e for e in all_ids if e in experiment_ids]
    if subset:
        all_ids = [e for e in all_ids if idx["experiments"][e]["subdir"] == subset]

    results = []
    for eid in sorted(all_ids):
        try:
            r = run_experiment(eid, mode=mode, master_ctrl=master_ctrl)
        except Exception as e:
            r = {"id": eid, "matched": False, "error": str(e)}
        results.append(r)
        tag = "PASS" if r.get("matched") else ("FAIL" if "error" not in r else "ERR ")
        sha = (r.get("content_sha256", "") or "")[:16]
        ms  = r.get("wall_clock_ms", 0)
        print(f"  {tag}  {eid:30}  {sha}  ({ms:>5} ms)")
        if STOP_ON_FIRST_FAIL and not r.get("matched"):
            break
    return results


# --------------------------------------------------------------
# Status report
# --------------------------------------------------------------
def cmd_status():
    idx = json.loads(INDEX_PATH.read_text())
    print(f"HUF-CNT Mission Command v{MC_VERSION}")
    print(f"Index: {INDEX_PATH}")
    print(f"Experiments: {idx['_meta']['n_experiments']}")
    print(f"Engine: {idx['_meta']['engine']}")
    print(f"Last updated: {idx['_meta']['last_updated']}")
    print()
    by_subdir = {}
    for eid, spec in idx["experiments"].items():
        by_subdir.setdefault(spec["subdir"], []).append(eid)
    for sub in sorted(by_subdir):
        print(f"  {sub}:  {len(by_subdir[sub])} experiments")
        for e in sorted(by_subdir[sub]):
            print(f"     - {e}")


# --------------------------------------------------------------
# CLI
# --------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="HUF-CNT Mission Command")
    ap.add_argument("experiment_ids", nargs="*",
                    help="explicit experiment ids (default: all)")
    ap.add_argument("--subset", choices=["codawork2026","domain","reference","extended"],
                    help="run only one subdirectory")
    ap.add_argument("--update", action="store_true",
                    help="rewrite INDEX.json with new SHAs (release flow)")
    ap.add_argument("--status", action="store_true",
                    help="print status report and exit")
    ap.add_argument("--master-control",
                    default=str(Path(__file__).resolve().parent / "master_control.json"),
                    help="optional master_control.json path")
    ap.add_argument("--with-modules", action="store_true",
                    help="after engine runs, dispatch post-CNT module pipeline "
                         "for any project in master_control.json that includes "
                         "all completed experiments")
    ap.add_argument("--project", default=None,
                    help="run engine + module pipeline for one named project "
                         "from master_control.json projects[] block")
    args = ap.parse_args()

    if args.status:
        cmd_status()
        return

    master_ctrl = load_master_control(Path(args.master_control))
    mode = "update" if args.update else "verify"

    print(f"HUF-CNT Mission Command v{MC_VERSION}  mode={mode}")
    print(f"Master control: {args.master_control} "
          f"(experiments overridden: {len(master_ctrl.get('experiments',{}))}, "
          f"projects: {len(master_ctrl.get('projects',{}))})")
    print()

    # If --project was specified, override the experiment_id list
    project_spec = None
    if args.project:
        project_spec = master_ctrl.get("projects", {}).get(args.project)
        if not project_spec:
            print(f"unknown project: {args.project}")
            sys.exit(2)
        args.experiment_ids = project_spec["experiments"]

    results = run_all(experiment_ids=args.experiment_ids or None,
                      mode=mode, master_ctrl=master_ctrl,
                      subset=args.subset)
    n_pass = sum(1 for r in results if r.get("matched"))
    n_fail = sum(1 for r in results if not r.get("matched") and "error" not in r)
    n_err  = sum(1 for r in results if "error" in r)
    print()
    print("=" * 60)
    print(f"Results: {n_pass} PASS, {n_fail} FAIL, {n_err} ERR  "
          f"(total {len(results)})")

    # ── Post-CNT module pipeline ──────────────────────────────
    if args.with_modules or args.project:
        print()
        print("=" * 60)
        print("Post-CNT module pipeline")
        print("=" * 60)
        import importlib.util
        mp = Path(__file__).resolve().parent / "modules.py"
        _spec = importlib.util.spec_from_file_location("mc_modules", str(mp))
        mc_modules = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(mc_modules)

        projects_to_run = ([args.project] if args.project
                           else list(master_ctrl.get("projects", {}).keys()))
        completed_ids = {r["id"] for r in results if r.get("matched")}
        for proj_id in projects_to_run:
            proj = master_ctrl["projects"][proj_id]
            members = proj["experiments"]
            # If invoked without --project, only fire when ALL members are done
            if not args.project and not all(m in completed_ids for m in members):
                print(f"  skip {proj_id} — not all experiments completed in this run")
                continue
            json_paths = []
            for eid in members:
                # locate JSON via the same logic as run_experiment
                idx = json.loads(INDEX_PATH.read_text())
                sub = idx["experiments"][eid]["subdir"]
                json_paths.append(str(EXPERIMENTS_DIR / sub / eid /
                                      f"{eid}_cnt.json"))
            out_dir = proj.get("output_dir") or \
                      f"codawork2026_conference/cnt_demo/03_combined/{proj_id}"
            if not Path(out_dir).is_absolute():
                out_dir = str(PACKAGE_ROOT / out_dir)
            spec = {
                "project_id":  proj_id,
                "output_dir":  out_dir,
                "experiments": members,
                "json_paths":  json_paths,
                "modules":     proj.get("modules", ["stage1", "stage2"]),
                "options":     proj.get("options", {}),
            }
            print(f"=== project {proj_id} ===  output: {out_dir}")
            mc_modules.run_pipeline(spec)

    if n_fail or n_err:
        sys.exit(1)


if __name__ == "__main__":
    main()
