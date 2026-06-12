#!/usr/bin/env python3
"""
HUF-CNT Mission Command — Post-CNT Module Pipeline.

Registry of optional analytical modules that run AFTER the engine produces
the canonical JSON. Users select which modules to run for each experiment
in `master_control.json`.

Every module conforms to the same contract:

    def run(json_path: Path, output_dir: Path, dataset_id: str,
            options: dict) -> dict

Returns a manifest describing the artefacts created (paths, sha256, kind).
The pipeline aggregates per-experiment manifests into one project-folder
manifest written at `<project_root>/_pipeline_manifest.json`.

Currently registered modules:
  stage1            — locked Order-1 ortho plate (atlas/stage1_v4.py)
  stage2            — locked Order-2 19-plate atlas (atlas/stage2_locked.py)
  spectrum_paper    — paper-only spectrum analyzer (atlas/spectrum_paper.py)
  projector_html    — interactive HTML plate-time projector
  delta             — run-vs-run delta tool (catalog only — needs prior run)

New modules can be added without touching mission_command.py:
just append to MODULES below.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
from typing import Callable
from datetime import datetime, timezone

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PACKAGE_ROOT))


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


# ─── stage1 ──────────────────────────────────────────────────────
def _run_stage1(json_path: Path, output_dir: Path, dataset_id: str,
                options: dict) -> dict:
    from atlas import atlas_stage1_complete
    out = output_dir / f"stage1_{dataset_id}.pdf"
    atlas_stage1_complete.render(str(json_path), str(out),
        max_plates=options.get("max_plates"),
        run_id=options.get("run_id"))
    return {"kind": "stage1", "path": str(out),
            "sha256": sha256_of(out), "bytes": out.stat().st_size}


# ─── stage2 ──────────────────────────────────────────────────────
def _run_stage2(json_path: Path, output_dir: Path, dataset_id: str,
                options: dict) -> dict:
    import json as _json
    from matplotlib.backends.backend_pdf import PdfPages
    from atlas import stage2_locked
    out = output_dir / f"stage2_{dataset_id}.pdf"
    j = _json.loads(Path(json_path).read_text())
    # Resolve per-experiment overrides nested under
    # options.per_experiment[<dataset_id>] (preferred) — falls back to
    # the top-level options block so a project-wide setting works too.
    per_exp = (options.get("per_experiment", {}) or {}).get(dataset_id, {}) or {}
    plate_options = {
        "ternary_triplets": per_exp.get("ternary_triplets",
                                        options.get("ternary_triplets")),
        "biplot_top_n":     per_exp.get("biplot_top_n",
                                        options.get("biplot_top_n", 6)),
    }
    plate_options = {k: v for k, v in plate_options.items() if v is not None}
    with PdfPages(str(out)) as pdf:
        stage2_locked.render_stage2(pdf, j, dataset_id,
                                    options.get("run_id"),
                                    options=plate_options)
    return {"kind": "stage2", "path": str(out),
            "sha256": sha256_of(out), "bytes": out.stat().st_size}


# ─── stage3 (Order-3 paged module) ─────────────────────────────
def _run_stage3(json_path: Path, output_dir: Path, dataset_id: str,
                options: dict) -> dict:
    import json as _json
    from matplotlib.backends.backend_pdf import PdfPages
    from atlas import stage3_locked
    out = output_dir / f"stage3_{dataset_id}.pdf"
    j = _json.loads(Path(json_path).read_text())
    with PdfPages(str(out)) as pdf:
        stage3_locked.render_stage3(pdf, j, dataset_id, options.get("run_id"))
    return {"kind": "stage3", "path": str(out),
            "sha256": sha256_of(out), "bytes": out.stat().st_size}


# ─── stage4 (Order-4+ group-level paged module) ────────────────
def _run_stage4_group(json_paths: list, output_dir: Path,
                       group_id: str, options: dict) -> dict:
    import json as _json
    from matplotlib.backends.backend_pdf import PdfPages
    from atlas import stage4_locked
    out = output_dir / f"stage4_{group_id}.pdf"
    members = [Path(jp).stem.replace("_cnt", "") for jp in json_paths]
    jsons = [_json.loads(Path(jp).read_text()) for jp in json_paths]
    with PdfPages(str(out)) as pdf:
        stage4_locked.render_stage4(pdf, members, jsons, group_id,
                                     run_id=options.get("run_id"))
    return {"kind": "stage4", "path": str(out),
            "sha256": sha256_of(out), "bytes": out.stat().st_size,
            "members": members}


# ─── spectrum_paper ──────────────────────────────────────────────
# This module is GROUP-LEVEL: it spans a list of experiments. The pipeline
# calls it once after all per-experiment runs, with the JSONs of the group.
def _run_spectrum_group(json_paths: list, output_dir: Path,
                         group_id: str, options: dict) -> dict:
    from atlas import spectrum_paper
    datasets = []
    for jp in json_paths:
        with open(jp) as f:
            j = json.load(f)
        # Use the JSON's source filename minus .csv as a label
        did = Path(jp).stem.replace("_cnt", "")
        datasets.append((did, j))
    out = output_dir / f"spectrum_paper_{group_id}.pdf"
    spectrum_paper.render_spectrum_paper(str(out), datasets,
        title=options.get("title",
                          f"{group_id} — Spectrum (Paper)"))
    return {"kind": "spectrum_paper", "path": str(out),
            "sha256": sha256_of(out), "bytes": out.stat().st_size,
            "members": [Path(jp).stem for jp in json_paths]}


# ─── projector_html ──────────────────────────────────────────────
# Group-level too: builds one HTML file with all member datasets embedded.
def _run_projector_group(json_paths: list, output_dir: Path,
                          group_id: str, options: dict) -> dict:
    """Embed member datasets in a self-contained HTML projector with a
    shared PCA frame for the COMBINED view."""
    import numpy as np
    out = output_dir / f"plate_time_projector_{group_id}.html"
    template_path = PACKAGE_ROOT / "atlas" / "plate_time_projector.html"
    if not template_path.exists():
        raise FileNotFoundError(f"projector template not found: {template_path}")
    # Build the per-dataset payload + combined block on the fly
    canon = options.get("canonical_carriers")
    datasets = {}
    js_items = []
    for jp in json_paths:
        with open(jp) as f:
            j = json.load(f)
        did = Path(jp).stem.replace("_cnt", "").replace("ember_", "")
        datasets[did] = _slim_dataset(j)
        js_items.append((did, j))
    # COMBINED block (only meaningful if all members share canon carriers)
    if canon:
        try:
            datasets["__combined__"] = _build_combined(js_items, canon)
        except Exception as e:
            print(f"  [projector] combined view skipped: {e}")
    payload = json.dumps(datasets, separators=(",", ":"))
    # Read the prebuilt template's HTML scaffold but replace the embedded
    # payload. Easiest: clone template, swap the JSON literal between
    # `window.PAYLOAD = ` and `;` on the matching line.
    html = template_path.read_text()
    import re
    html = re.sub(
        r"window\.PAYLOAD\s*=\s*\{.*?\};",
        f"window.PAYLOAD = {payload};",
        html, count=1, flags=re.S,
    )
    out.write_text(html)
    return {"kind": "projector_html", "path": str(out),
            "sha256": sha256_of(out), "bytes": out.stat().st_size,
            "members": [Path(jp).stem for jp in json_paths]}


def _slim_dataset(j: dict) -> dict:
    import numpy as np
    inp = j["input"]; ts = j["tensor"]["timesteps"]
    D = inp["n_carriers"]; T = inp["n_records"]
    carriers = list(inp["carriers"]); labels = list(inp["labels"])
    basis = np.asarray(j["tensor"]["helmert_basis"]["coefficients"])
    clr = np.array([t["coda_standard"]["clr"] for t in ts])
    composition = np.array([t["coda_standard"]["composition"] for t in ts])
    norm = np.array([t["coda_standard"]["aitchison_norm"] for t in ts])
    hs   = np.array([t["coda_standard"]["shannon_entropy"] for t in ts])
    centred = clr - clr.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(centred, full_matrices=False)
    frame = Vt[:2]
    traj_pca   = (frame @ clr.T).T - (frame @ clr.T).T.mean(axis=0, keepdims=True)
    eye = np.eye(D) - (1.0/D)
    carrier_pca = (frame @ eye.T).T
    pair_idx = []; pair_names = []
    for i in range(D):
        for jj in range(i+1, D):
            pair_idx.append((i, jj))
            pair_names.append(f"{carriers[i]} | {carriers[jj]}")
    ml = j["stages"]["stage1"]["higgins_extensions"]["metric_ledger"]
    omega_deg = [m.get("omega_deg",0.0) for m in ml]
    rings     = [m.get("ring","") for m in ml]
    helms     = [m.get("helmsman","") for m in ml]
    cpe = j["stages"]["stage2"]["higgins_extensions"]["carrier_pair_examination"]
    pair_r = {}
    for entry in cpe:
        ai, bi = entry["i"], entry["j"]
        key = (min(ai,bi), max(ai,bi))
        pair_r[f"{key[0]},{key[1]}"] = float(entry.get("pearson_r", 0.0))
    locks = j["diagnostics"]["higgins_extensions"].get("lock_events", [])
    var_explained = float(((S[:2]**2).sum()) / ((S**2).sum() + 1e-30))
    return {
        "carriers": carriers, "labels": labels, "T": T, "D": D,
        "ilr": ((basis @ clr.T).T).tolist(),
        "composition": composition.tolist(), "clr": clr.tolist(),
        "norm": norm.tolist(), "hs": hs.tolist(),
        "omega_deg": omega_deg, "rings": rings, "helms": helms,
        "pair_idx": [list(p) for p in pair_idx],
        "pair_names": pair_names, "pair_r": pair_r, "locks": locks,
        "traj_pca": traj_pca.tolist(),
        "carrier_pca": carrier_pca.tolist(),
        "var_explained_2d": var_explained,
        "content_sha256": j["diagnostics"].get("content_sha256",""),
    }


def _build_combined(js_items, canon: list) -> dict:
    import numpy as np
    all_clr = []
    keep = []
    for did, j in js_items:
        carriers = j["input"]["carriers"]
        if not all(c in carriers for c in canon):
            continue
        ts = j["tensor"]["timesteps"]
        composition = np.array([t["coda_standard"]["composition"] for t in ts])
        idx = [carriers.index(c) for c in canon]
        sub = composition[:, idx]
        sub = sub / np.maximum(sub.sum(axis=1, keepdims=True), 1e-30)
        sub_safe = np.maximum(sub, 1e-9)
        clr = np.log(sub_safe) - np.log(sub_safe).mean(axis=1, keepdims=True)
        all_clr.append((did, j, sub, clr))
        keep.append((did, j))
    if not all_clr:
        raise RuntimeError("no members matched canonical carriers")
    big = np.vstack([t[3] for t in all_clr])
    common_mean = big.mean(axis=0, keepdims=True)
    centred = big - common_mean
    U, S, Vt = np.linalg.svd(centred, full_matrices=False)
    frame = Vt[:2]
    var_exp = float(((S[:2]**2).sum()) / ((S**2).sum() + 1e-30))
    eye = np.eye(len(canon)) - (1.0/len(canon))
    carrier_pca = (frame @ eye.T).T
    datasets = {}
    for (did, j, sub, clr) in all_clr:
        ts = j["tensor"]["timesteps"]
        norm = [t["coda_standard"]["aitchison_norm"] for t in ts]
        hs   = [t["coda_standard"]["shannon_entropy"] for t in ts]
        proj = (clr - common_mean) @ frame.T
        datasets[did.replace("ember_","")] = {
            "labels": j["input"]["labels"], "T": j["input"]["n_records"],
            "carriers_used": canon, "traj_pca": proj.tolist(),
            "composition_8": sub.tolist(),
            "norm": list(norm), "hs": list(hs),
        }
    return {
        "carriers": canon, "var_explained_2d": var_exp,
        "carrier_pca": carrier_pca.tolist(),
        "datasets": datasets,
        "common_mean": common_mean[0].tolist(),
    }


# ─── module registry ─────────────────────────────────────────────
MODULES = {
    "stage1":         {"scope": "experiment", "fn": _run_stage1,
                       "desc": "Order-1 ortho ILR-Helmert plate per timestep (locked)"},
    "stage2":         {"scope": "experiment", "fn": _run_stage2,
                       "desc": "Order-2 single-report (geometry+dynamics, 28 plates)"},
    "stage3":         {"scope": "experiment", "fn": _run_stage3,
                       "desc": "Order-3 single-report (depth tower / IR / attractor, 11 plates)"},
    "stage4":         {"scope": "group",      "fn": _run_stage4_group,
                       "desc": "Order-4+ cross-dataset inference report (group-level, 11 plates)"},
    "spectrum_paper": {"scope": "group",      "fn": _run_spectrum_group,
                       "desc": "Cross-dataset paper spectrum (group-level)"},
    "projector_html": {"scope": "group",      "fn": _run_projector_group,
                       "desc": "Interactive HTML plate-time projector (group-level)"},
}


# ─── pipeline runner ─────────────────────────────────────────────
def run_pipeline(spec: dict) -> dict:
    """Run a multi-experiment + multi-module pipeline.

    `spec` is a dict like:
       {
         "project_id":   "codawork2026_ember",
         "output_dir":   "<absolute path>",
         "experiments":  ["ember_chn", ...],          # in order
         "json_paths":   ["<abs path to *_cnt.json>", ...],
         "modules":      ["stage1","stage2","spectrum_paper","projector_html"],
         "options":      {"projector_html": {"canonical_carriers": [...]}}
       }
    """
    project_id = spec["project_id"]
    out_dir = Path(spec["output_dir"]); out_dir.mkdir(parents=True, exist_ok=True)
    exp_ids = spec["experiments"]
    json_paths = [Path(p) for p in spec["json_paths"]]
    modules = spec["modules"]
    options = spec.get("options", {})

    manifest = {
        "_meta": {
            "project_id":  project_id,
            "generated":   datetime.now(timezone.utc).isoformat(),
            "experiments": exp_ids,
            "modules":     modules,
        },
        "per_experiment": {},
        "group":          {},
    }

    # Per-experiment modules
    for eid, jp in zip(exp_ids, json_paths):
        manifest["per_experiment"][eid] = []
        for mod in modules:
            m = MODULES.get(mod)
            if not m or m["scope"] != "experiment":
                continue
            try:
                rec = m["fn"](jp, out_dir, eid, options.get(mod, {}))
                manifest["per_experiment"][eid].append(rec)
                print(f"  [{mod}] {eid} → {Path(rec['path']).name}  ({rec['bytes']} B)")
            except Exception as e:
                print(f"  [{mod}] {eid} FAILED: {e}")
                manifest["per_experiment"][eid].append({"kind": mod, "error": str(e)})

    # Group-level modules
    for mod in modules:
        m = MODULES.get(mod)
        if not m or m["scope"] != "group":
            continue
        try:
            rec = m["fn"](json_paths, out_dir, project_id, options.get(mod, {}))
            manifest["group"][mod] = rec
            print(f"  [{mod}] group → {Path(rec['path']).name}  ({rec['bytes']} B)")
        except Exception as e:
            print(f"  [{mod}] group FAILED: {e}")
            manifest["group"][mod] = {"kind": mod, "error": str(e)}

    manifest_path = out_dir / "_pipeline_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"  manifest: {manifest_path}")
    return manifest


def list_modules() -> None:
    print("Registered post-CNT modules:")
    for k, v in MODULES.items():
        print(f"  {k:20s} [{v['scope']:11s}]  {v['desc']}")


if __name__ == "__main__":
    list_modules()
