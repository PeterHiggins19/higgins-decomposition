"""Portable adapter to the canonical CNT engine.

HCI-CNQ inherits from HCI-CNT. Rather than vendor a copy of cnt.py,
this adapter locates the canonical engine on disk (by walking up from
the current file, or honouring an explicit --repo-root / --cnt-engine
flag) and exposes a small surface for invoking CNT or reading CNT JSON.

Markers used to find the repo root (in order of preference):
  1. Path passed to --repo-root or REPO_ROOT env var
  2. .git directory
  3. HCI-CNQ folder (the one containing this file)
  4. HCI-CNT folder
  5. ai-refresh folder

If none is found, raises a clear error pointing at the --repo-root flag.

Usage:
    repo_root = find_repo_root()                # auto-detect
    cnt_path  = find_cnt_engine(repo_root)      # locate cnt.py
    cnt_json  = run_cnt(input_csv, ...)         # invoke as subprocess
    cnt_data  = load_cnt_json(json_path)        # read existing run
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


_REPO_MARKERS = (".git", "HCI-CNQ", "HCI-CNT", "ai-refresh")


def find_repo_root(start: Optional[Path] = None,
                   explicit: Optional[Path] = None) -> Path:
    """Locate the Hs repository root.

    Order of resolution:
        1. explicit argument (from --repo-root flag) if provided
        2. REPO_ROOT environment variable
        3. walk upward from `start` (default: this file) looking for
           any of: .git, HCI-CNQ, HCI-CNT, ai-refresh

    Raises FileNotFoundError if no marker is found.
    """
    if explicit is not None:
        explicit = Path(explicit).resolve()
        if not explicit.exists():
            raise FileNotFoundError(f"--repo-root not found: {explicit}")
        return explicit

    env_root = os.environ.get("REPO_ROOT")
    if env_root:
        p = Path(env_root).resolve()
        if p.exists():
            return p

    if start is None:
        start = Path(__file__).resolve()
    here = start if start.is_dir() else start.parent

    # Walk upward, looking for any marker. The repo root is the
    # FIRST ancestor that contains either Hs/HCI-CNT, Hs/HCI-CNQ,
    # or .git directly. We accept either layout: Hs/ as the root,
    # or the parent of Hs/.
    for ancestor in [here, *here.parents]:
        for marker in _REPO_MARKERS:
            if (ancestor / marker).exists():
                return ancestor
        # Also accept Hs/ subdir layout
        if (ancestor / "Hs" / "HCI-CNT").exists():
            return ancestor / "Hs"

    raise FileNotFoundError(
        "Could not locate Hs repository root. "
        "Pass --repo-root /path/to/higgins-decomposition (or .../higgins-decomposition/Hs) "
        "or set the REPO_ROOT environment variable."
    )


def find_cnt_engine(repo_root: Path,
                    explicit: Optional[Path] = None) -> Path:
    """Locate cnt.py within the repo, honouring --cnt-engine override.

    Search order:
        1. explicit override
        2. <repo_root>/HCI-CNT/engine/cnt.py
        3. <repo_root>/Hs/HCI-CNT/engine/cnt.py
    """
    if explicit is not None:
        p = Path(explicit).resolve()
        if not p.exists():
            raise FileNotFoundError(f"--cnt-engine not found: {p}")
        return p

    candidates = [
        repo_root / "HCI-CNT" / "engine" / "cnt.py",
        repo_root / "Hs" / "HCI-CNT" / "engine" / "cnt.py",
    ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(
        f"cnt.py not found under {repo_root}. "
        f"Tried: {[str(c) for c in candidates]}. "
        "Pass --cnt-engine /path/to/cnt.py to override."
    )


def run_cnt(input_csv: Path,
            output_json: Path,
            cnt_engine: Path,
            extra_args: Optional[list] = None) -> Path:
    """Invoke the canonical CNT engine as a subprocess.

    The engine signature is determined by cnt.py at the time of writing:
    a CLI that accepts an input CSV and writes a CNT JSON. Extra args
    are forwarded as-is to allow --carrier-aliases, --skip-eitt, etc.

    Returns the output_json path on success.
    """
    input_csv = Path(input_csv).resolve()
    output_json = Path(output_json).resolve()
    cnt_engine = Path(cnt_engine).resolve()

    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")
    if not cnt_engine.exists():
        raise FileNotFoundError(f"CNT engine not found: {cnt_engine}")

    output_json.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        str(cnt_engine),
        "--input", str(input_csv),
        "--output", str(output_json),
    ]
    if extra_args:
        cmd.extend(extra_args)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"CNT engine failed (exit {result.returncode}).\n"
            f"stderr:\n{result.stderr}\n"
            f"stdout:\n{result.stdout}"
        )
    if not output_json.exists():
        raise RuntimeError(
            f"CNT engine returned 0 but did not write {output_json}"
        )
    return output_json


def load_cnt_json(path: Path) -> dict:
    """Read a CNT JSON output file and return the parsed object."""
    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"CNT JSON not found: {p}")
    with p.open() as f:
        return json.load(f)


def extract_cnt_diagnostics(cnt_json: dict) -> dict:
    """Pull the headline CNT diagnostics that CNQ needs.

    Tolerant to schema 2.0.x and 2.1.x variants. Returns a flat dict
    with the fields CNQ keys off of:
        D, T, content_sha256, source_file_sha256, cnt_engine_version,
        cnt_schema_version, cnt_termination, ir_class, helmsman_sigma,
        amplitude_A, damping_zeta.
    """
    out: dict = {}

    # CNT JSON structure varies a bit; probe in priority order.
    diag = cnt_json.get("diagnostics", {}) or {}
    metadata = cnt_json.get("metadata", {}) or {}
    inp = cnt_json.get("input", {}) or {}

    out["D"] = (
        inp.get("n_carriers")
        or inp.get("D")
        or cnt_json.get("D")
    )
    out["T"] = (
        inp.get("n_records")
        or inp.get("T")
        or cnt_json.get("T")
    )
    out["content_sha256"] = (
        diag.get("content_sha256")
        or cnt_json.get("content_sha256")
    )
    out["source_file_sha256"] = (
        inp.get("source_file_sha256")
        or cnt_json.get("source_file_sha256")
    )
    out["cnt_engine_version"] = (
        metadata.get("engine_version")
        or metadata.get("version")
        or cnt_json.get("engine_version")
    )
    out["cnt_schema_version"] = (
        metadata.get("schema")
        or metadata.get("schema_version")
        or cnt_json.get("schema")
    )

    # Termination / IR class / Helmsman channel — best-effort extraction.
    out["cnt_termination"] = (
        diag.get("curvature_termination")
        or diag.get("termination")
        or cnt_json.get("curvature_termination")
    )
    out["ir_class"] = (
        diag.get("ir_class")
        or cnt_json.get("ir_class")
    )
    # Helmsman / sigma channel may live under several names.
    helmsman = diag.get("helmsman") or {}
    if isinstance(helmsman, dict):
        out["helmsman_sigma"] = helmsman.get("sigma") or helmsman.get("sigma_HS")
    out["amplitude_A"] = diag.get("amplitude_A") or diag.get("A")
    out["damping_zeta"] = diag.get("damping_zeta") or diag.get("zeta")

    return out


def add_repo_root_arg(parser):
    """Helper for argparse: add the standard --repo-root and --cnt-engine
    flags to any CLI that needs them. Centralised so every CNQ script
    presents the same interface.
    """
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Path to the higgins-decomposition repo (or its Hs/ subdir). "
             "Auto-detected by walking up from the script if omitted.",
    )
    parser.add_argument(
        "--cnt-engine",
        type=Path,
        default=None,
        help="Path to cnt.py. Defaults to <repo-root>/HCI-CNT/engine/cnt.py.",
    )
    return parser
