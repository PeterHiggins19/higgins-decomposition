#!/usr/bin/env python3
"""
HUF-CNT — run_pipeline.py

Top-level driver for the post-CNT module pipeline. Reads master_control.json
to discover which projects exist and what modules each project should run,
locates JSON inputs from experiments/INDEX.json, and dispatches into
mission_command/modules.py.

Usage:
  python tools/run_pipeline.py codawork2026_ember
  python tools/run_pipeline.py --list-modules
  python tools/run_pipeline.py --list-projects
  python tools/run_pipeline.py --all
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mission_command"))

import importlib.util
_spec = importlib.util.spec_from_file_location(
    "mc_modules", str(ROOT / "mission_command" / "modules.py"))
mc_modules = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mc_modules)


def load_master_control() -> dict:
    p = ROOT / "mission_command" / "master_control.json"
    if not p.exists():
        return {"projects": {}}
    return json.loads(p.read_text())


def load_index() -> dict:
    return json.loads((ROOT / "experiments" / "INDEX.json").read_text())


def resolve_json(eid: str, idx: dict) -> Path:
    spec = idx["experiments"][eid]
    sub = spec["subdir"]
    return ROOT / "experiments" / sub / eid / f"{eid}_cnt.json"


def run_project(project_id: str) -> dict:
    mc = load_master_control()
    if project_id not in mc.get("projects", {}):
        raise SystemExit(f"unknown project '{project_id}'.  "
                         f"Known: {list(mc.get('projects', {}).keys())}")
    proj = mc["projects"][project_id]
    idx = load_index()

    exp_ids = proj["experiments"]
    json_paths = [str(resolve_json(eid, idx)) for eid in exp_ids]

    out_dir = proj.get("output_dir") or \
              str(ROOT / "codawork2026_conference" / "cnt_demo" /
                  "03_combined" / project_id)
    if not Path(out_dir).is_absolute():
        out_dir = str(ROOT / out_dir)

    spec = {
        "project_id":  project_id,
        "output_dir":  out_dir,
        "experiments": exp_ids,
        "json_paths":  json_paths,
        "modules":     proj.get("modules", ["stage1", "stage2"]),
        "options":     proj.get("options", {}),
    }
    print(f"=== Project: {project_id} ===")
    print(f"    output: {out_dir}")
    print(f"    experiments: {len(exp_ids)}")
    print(f"    modules: {spec['modules']}")
    return mc_modules.run_pipeline(spec)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", nargs="?")
    ap.add_argument("--all", action="store_true",
                    help="run every project in master_control.json")
    ap.add_argument("--list-modules", action="store_true")
    ap.add_argument("--list-projects", action="store_true")
    args = ap.parse_args()

    if args.list_modules:
        mc_modules.list_modules(); return
    if args.list_projects:
        mc = load_master_control()
        print("Projects in master_control.json:")
        for k, v in mc.get("projects", {}).items():
            print(f"  {k}  ({len(v.get('experiments',[]))} experiments,  "
                  f"modules={v.get('modules',[])})")
        return
    if args.all:
        mc = load_master_control()
        for k in mc.get("projects", {}):
            run_project(k)
        return
    if not args.project:
        ap.print_help(); return
    run_project(args.project)


if __name__ == "__main__":
    main()
