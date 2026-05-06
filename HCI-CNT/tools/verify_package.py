#!/usr/bin/env python3
"""
HUF-CNT — verify_package.py

Quick package-readiness check. Confirms that every promised artefact is
present and that key Python modules import cleanly.

Run:  python tools/verify_package.py
"""
from __future__ import annotations
import importlib, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OK, FAIL = "[OK]", "[FAIL]"
errors = []

def check_path(rel: str):
    p = ROOT / rel
    if p.exists():
        print(f"{OK}    {rel}")
    else:
        print(f"{FAIL}  {rel}  (missing)")
        errors.append(rel)

def check_import(modpath: str):
    try:
        importlib.import_module(modpath)
        print(f"{OK}    import {modpath}")
    except Exception as e:
        print(f"{FAIL}  import {modpath} → {e}")
        errors.append(modpath)

print("=" * 60)
print("HUF-CNT  package verification")
print("=" * 60)

# Core engine
check_path("engine/cnt.py")
check_path("engine/cnt.R")
check_path("engine/native_units.py")
check_import("engine.native_units")

# Atlas modules
for f in ("atlas/stage1_v4.py", "atlas/stage2_locked.py",
          "atlas/stage3_locked.py", "atlas/stage4_locked.py",
          "atlas/spectrum_paper.py", "atlas/plate_time_projector.html",
          "atlas/det_pdf.py"):
    check_path(f)
# check_import("atlas.det_pdf")  # path differs in HCI-CNT layout
# check_import("atlas.spectrum_paper")

# Mission Command
for f in ("mission_command/mission_command.py", "mission_command/modules.py",
          "mission_command/master_control.json", "tools/run_pipeline.py"):
    check_path(f)

# Calibration fixtures
for f in ("atlas/STANDARD_CALIBRATION_27pt.csv",
          "atlas/STANDARD_CALIBRATION_27pt_cnt.json",
          "atlas/STANDARD_CALIBRATION_27pt_stage1v4.pdf",
          "atlas/STANDARD_CALIBRATION_stage2_A_straight.pdf",
          "atlas/STANDARD_CALIBRATION_stage2_B_loop.pdf"):
    check_path(f)

# Conference demo (output artefacts only — doctrine refs now folded into Volumes I/II/III)
for f in ("conference_demo/README.md",
          "conference_demo/cnt_demo/03_combined/spectrum_paper_codawork2026_ember.pdf",
          "conference_demo/cnt_demo/03_combined/plate_time_projector_codawork2026_ember.html"):
    check_path(f)

# Per-country
for code in ("chn","deu","fra","gbr","ind","jpn","usa","wld"):
    base = f"conference_demo/cnt_demo/02_per_country/ember_{code}"
    check_path(f"{base}/ember_{code}_cnt.json")
    check_path(f"{base}/stage1_ember_{code}.pdf")
    check_path(f"{base}/stage2_ember_{code}.pdf")

# Three consolidated handbook volumes + release record
check_path("handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md")
check_path("handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md")
check_path("handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md")
# CHANGELOG.md lives at the parent Hs repo root, not inside HCI-CNT
check_path("README.md")


# v1.1.x extended adapters
for f in ("adapters/markham_budget.py", "adapters/iiasa_ngfs.py",
          "adapters/esa_planck_cosmic.py", "adapters/financial_sector.py",
          "adapters/chemixhub_oxide.py"):
    check_path(f)
for code in ("markham_budget","iiasa_ngfs","esa_planck_cosmic",
             "financial_sector","chemixhub_oxide"):
    check_path(f"experiments/extended/{code}/{code}_input.csv")
    check_path(f"experiments/extended/{code}/{code}_cnt.json")

# INDEX integrity
idx_path = ROOT / "experiments" / "INDEX.json"
if idx_path.exists():
    idx = json.loads(idx_path.read_text())
    n = len(idx.get("experiments", {}))
    if n == 25:
        print(f"{OK}    experiments/INDEX.json declares 25 experiments")
    else:
        print(f"{FAIL}  experiments/INDEX.json declares {n} experiments (expected 25)")
        errors.append("INDEX.json experiment count")

print()
print("=" * 60)
if errors:
    print(f"  {len(errors)} issue(s) — package not ready")
    for e in errors: print(f"    - {e}")
    sys.exit(1)
else:
    print("  PACKAGE READY")
