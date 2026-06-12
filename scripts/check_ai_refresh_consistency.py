#!/usr/bin/env python3
"""
Hs Change Control v1.0 — AI Refresh Consistency Checker

Static analyzer for AI-facing current-state drift.
Stdlib-only. Runs from repo root.

Usage:
    python scripts/check_ai_refresh_consistency.py
    python scripts/check_ai_refresh_consistency.py --profile ai-current
    python scripts/check_ai_refresh_consistency.py --strict

Exit codes:
    0  no errors
    1  errors found
    2  invalid invocation / setup problem

See ai-refresh/CHANGE_CONTROL_README.md for the full doctrine.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT_MARKERS = ("HS_FAST_REFRESH.json", "ai-refresh", "HCI-CNT")

LIVE_CURRENT_FILES = [
    "README.md",
    "PUBLICATION_READY.md",
    "QUICKSTART.md",
    "HS_FAST_REFRESH.json",
    "HS_FAST_REFRESH.md",
    "llms.txt",
    ".well-known/ai-context.json",
    "AI_AGENTS.md",
    "ai-refresh/CCTT_QUICKSTART.md",
    "ai-refresh/CCTT_RUNBOOK.md",
    "ai-refresh/CCTT_BUILD_INSTRUCTION_v1.0.json",
]

REQUIRED_JSON_FILES = [
    "HS_FAST_REFRESH.json",
    ".well-known/ai-context.json",
    "ai-refresh/INVESTIGATION_CATALOG.json",
    "ai-refresh/CONFIGURATION_ITEMS.json",
    "ai-refresh/INTERFACE_CONTROL.json",
    "ai-refresh/TRACEABILITY_MATRIX.json",
    "ai-refresh/CHANGE_PACKET_TEMPLATE.json",
]

CNQ_PENDING_PHRASES = [
    "cnq.py pending",
    "cnq.py is pending",
    "cnq.py does not exist",
    "cnq.py is the next milestone",
    "compiled cnq.py engine itself is the next milestone",
    "until it lands",
    "when the engine ships",
    "once the compiled cnq.py engine lands",
]

CONTEXT_ALLOWS_STALE = [
    "legacy",
    "historical",
    "archive",
    "old claim",
    "avoid claiming",
    "stale",
    "falsified",
    "snapshot",
    "this used to say",
    "[deprecated]",
    "do not say",
]

FILE_LEVEL_LEGACY_MARKERS = [
    "LEGACY v1.0 PROTOCOL",
    "LEGACY v1.0 — written for",
    "HISTORICAL SNAPSHOT",
    "snapshot only, see legacy header",
    "_status\": \"legacy",
    "legacy snapshot for traceability",
    "preserved as a legacy snapshot",
    "preserved as a snapshot for traceability",
]

CCTT_FILES = [
    "ai-refresh/CCTT_RUNBOOK.md",
    "ai-refresh/CCTT_BUILD_INSTRUCTION_v1.0.json",
    "ai-refresh/CCTT_QUICKSTART.md",
]

CCTT_LEGACY_MARKERS = [
    "legacy",
    "v1.0 (legacy)",
    "see CCTT v1.1",
    "see CCTT_BUILD_INSTRUCTION_v1.1",
    "this is the legacy",
    "superseded",
]


def find_repo_root(start: Path):
    cur = start.resolve()
    for _ in range(8):
        if all((cur / m).exists() for m in REPO_ROOT_MARKERS):
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def read_file(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def load_json(path: Path):
    text = read_file(path)
    if text is None:
        return None, f"cannot read {path}"
    try:
        return json.loads(text), None
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {e}"


def get_nested(obj, dotted_path, default=None):
    cur = obj
    for part in dotted_path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def find_phrase_with_context(text: str, phrase: str, window: int = 200):
    out = []
    lower = text.lower()
    needle = phrase.lower()
    start = 0
    while True:
        idx = lower.find(needle, start)
        if idx == -1:
            break
        line_no = text.count("\n", 0, idx) + 1
        snippet_start = max(0, idx - window)
        snippet_end = min(len(text), idx + len(phrase) + window)
        snippet = text[snippet_start:snippet_end]
        out.append((line_no, snippet))
        start = idx + len(phrase)
    return out


def context_allows_stale(snippet: str) -> bool:
    s = snippet.lower()
    return any(marker in s for marker in CONTEXT_ALLOWS_STALE)


def file_marked_legacy(text: str) -> bool:
    head = text[:3000]
    return any(marker.lower() in head.lower() for marker in FILE_LEVEL_LEGACY_MARKERS)


class Results:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passes = []

    def err(self, check_id, msg):
        self.errors.append(f"[{check_id}] {msg}")

    def warn(self, check_id, msg):
        self.warnings.append(f"[{check_id}] {msg}")

    def ok(self, check_id, msg):
        self.passes.append(f"[{check_id}] {msg}")


def chk_json_001(root, r):
    for rel in REQUIRED_JSON_FILES:
        path = root / rel
        if not path.exists():
            r.err("CHK-JSON-001", f"required JSON missing: {rel}")
            continue
        obj, err = load_json(path)
        if err:
            r.err("CHK-JSON-001", f"{rel}: {err}")
        else:
            r.ok("CHK-JSON-001", f"{rel} parses cleanly")


def chk_cnq_001(root, r, files):
    cnq_py = root / "HCI-CNQ" / "engine" / "cnq.py"
    if not cnq_py.exists():
        r.err("CHK-CNQ-001", "HCI-CNQ/engine/cnq.py does not exist")
        return
    for rel in files:
        path = root / rel
        text = read_file(path)
        if text is None:
            continue
        if file_marked_legacy(text):
            r.ok("CHK-CNQ-001", f"{rel} — file-level legacy marker present; stale phrases allowed")
            continue
        for phrase in CNQ_PENDING_PHRASES:
            for line_no, snippet in find_phrase_with_context(text, phrase):
                if context_allows_stale(snippet):
                    continue
                r.err("CHK-CNQ-001",
                      f"{rel}:{line_no} — live file contains stale phrase '{phrase}' (cnq.py shipped in push #26)")
    if not any(e.startswith("[CHK-CNQ-001]") for e in r.errors):
        r.ok("CHK-CNQ-001", "no live file claims cnq.py is pending or missing")


def chk_version_001(root, r, files):
    fr, err = load_json(root / "HS_FAST_REFRESH.json")
    if err:
        r.err("CHK-VERSION-001", f"cannot read HS_FAST_REFRESH.json: {err}")
        return
    cnt_v = get_nested(fr, "canonical_engines.cnt_python.version") or get_nested(fr, "canonical_engines.cnt_python")
    cnq_v = get_nested(fr, "canonical_engines.cnq_python.version") or get_nested(fr, "canonical_engines.cnq_python")
    if isinstance(cnt_v, dict): cnt_v = cnt_v.get("version")
    if isinstance(cnq_v, dict): cnq_v = cnq_v.get("version")
    if not cnt_v or not cnq_v:
        r.warn("CHK-VERSION-001", f"could not extract engine versions (cnt={cnt_v}, cnq={cnq_v})")
        return
    stale_markers = [
        ("CNT 2.0.4", cnt_v != "2.0.4"),
        ("CNQ 1.0.0", cnq_v != "1.0.0"),
        ("Schema 2.1.0", cnt_v != "2.0.4"),
    ]
    for rel in files:
        if "CONFIGURATION_ITEMS" in rel or "INTERFACE_CONTROL" in rel or "TRACEABILITY_MATRIX" in rel or "DCP-" in rel:
            continue
        path = root / rel
        text = read_file(path)
        if text is None:
            continue
        if file_marked_legacy(text):
            r.ok("CHK-VERSION-001", f"{rel} — file-level legacy marker present; stale versions allowed")
            continue
        for pattern, should_flag in stale_markers:
            if not should_flag: continue
            try:
                for m in re.finditer(pattern, text, re.IGNORECASE):
                    idx = m.start()
                    line_no = text.count("\n", 0, idx) + 1
                    snippet = text[max(0, idx - 200): idx + 200]
                    if context_allows_stale(snippet):
                        continue
                    r.err("CHK-VERSION-001",
                          f"{rel}:{line_no} — stale version reference '{m.group(0)}' (HS_FAST_REFRESH.json says cnt={cnt_v}, cnq={cnq_v})")
            except re.error:
                continue
    if not any(e.startswith("[CHK-VERSION-001]") for e in r.errors):
        r.ok("CHK-VERSION-001", f"no stale engine versions in live files (current: cnt={cnt_v}, cnq={cnq_v})")


def chk_inv_001(root, r):
    cat, err = load_json(root / "ai-refresh" / "INVESTIGATION_CATALOG.json")
    if err:
        r.err("CHK-INV-001", f"cannot read INVESTIGATION_CATALOG.json: {err}")
        return
    entries = cat.get("investigations") or []
    total = len(entries)
    if total == 0:
        r.warn("CHK-INV-001", "investigation catalog has 0 entries (unexpected)")
        return
    md_text = read_file(root / "ai-refresh" / "INVESTIGATION_CATALOG.md") or ""
    snapshot_markers = ["snapshot", "historical", "live record is INVESTIGATION_CATALOG.json", "live record"]
    if any(m.lower() in md_text.lower() for m in snapshot_markers):
        r.ok("CHK-INV-001", f"INVESTIGATION_CATALOG.md is snapshot-marked (live count in JSON: {total})")
    else:
        r.warn("CHK-INV-001", f"INVESTIGATION_CATALOG.md has no snapshot marker but JSON shows {total} entries")
    fr_md = read_file(root / "HS_FAST_REFRESH.md") or ""
    m = re.search(r"\((\d+)\s+entries[^)]*\)", fr_md, re.IGNORECASE)
    if m:
        claimed = int(m.group(1))
        if claimed != total and not any(s in fr_md.lower() for s in snapshot_markers):
            r.err("CHK-INV-001",
                  f"HS_FAST_REFRESH.md claims {claimed} entries; live JSON has {total}; no snapshot marker")
        elif claimed != total:
            r.ok("CHK-INV-001", f"HS_FAST_REFRESH.md claims {claimed} entries (live={total}) but is snapshot-marked")


def chk_cctt_001(root, r):
    fr, _ = load_json(root / "HS_FAST_REFRESH.json")
    cnt_v = None
    if fr:
        cnt_v = get_nested(fr, "canonical_engines.cnt_python.version")
        if isinstance(cnt_v, dict): cnt_v = cnt_v.get("version")
    for rel in CCTT_FILES:
        path = root / rel
        text = read_file(path)
        if text is None:
            continue
        is_current = bool(cnt_v and cnt_v in text)
        is_legacy = any(marker.lower() in text.lower() for marker in CCTT_LEGACY_MARKERS)
        if re.search(r"Engine target:\s*CNT\s*2\.0\.4", text, re.IGNORECASE):
            if file_marked_legacy(text):
                r.ok("CHK-CCTT-001", f"{rel} — 'Engine target: CNT 2.0.4' present but file legacy-marked")
                continue
            r.err("CHK-CCTT-001",
                  f"{rel} — 'Engine target: CNT 2.0.4' is stale and not marked legacy (current cnt={cnt_v})")
            continue
        if is_current or is_legacy:
            tag = []
            if is_current: tag.append("current")
            if is_legacy: tag.append("legacy-marked")
            r.ok("CHK-CCTT-001", f"{rel} — {' + '.join(tag)}")
        else:
            r.warn("CHK-CCTT-001", f"{rel} — neither current nor legacy status is explicit")


def chk_readme_001(root, r):
    readme = read_file(root / "README.md")
    if readme is None:
        r.warn("CHK-README-001", "README.md not readable")
        return
    forbidden = [
        "The compiled `cnq.py` engine itself is the next milestone",
        "Until it lands",
        "cnq.py is the next milestone",
    ]
    found_any = False
    for phrase in forbidden:
        for line_no, snippet in find_phrase_with_context(readme, phrase):
            if context_allows_stale(snippet):
                continue
            r.err("CHK-README-001",
                  f"README.md:{line_no} — forbidden phrase '{phrase}' (CNQ shipped; contradicts top of README)")
            found_any = True
    if not found_any:
        r.ok("CHK-README-001", "README.md has no internal CNQ pending/shipped contradiction")


def run(profile, strict):
    cwd = Path.cwd()
    root = find_repo_root(cwd)
    if root is None:
        print("ERROR: could not locate repo root", file=sys.stderr)
        return 2
    r = Results()
    print("=" * 70)
    print("Hs AI-Refresh Consistency Checker")
    print(f"Repo root: {root}")
    print(f"Profile:   {profile}")
    print(f"Strict:    {strict}")
    print("=" * 70)
    chk_json_001(root, r)
    chk_cnq_001(root, r, LIVE_CURRENT_FILES)
    chk_version_001(root, r, LIVE_CURRENT_FILES)
    chk_inv_001(root, r)
    chk_cctt_001(root, r)
    chk_readme_001(root, r)
    print()
    print(f"PASSES   ({len(r.passes)}):")
    for p in r.passes:
        print(f"  OK  {p}")
    print()
    print(f"WARNINGS ({len(r.warnings)}):")
    for w in r.warnings:
        print(f"  WARN {w}")
    print()
    print(f"ERRORS   ({len(r.errors)}):")
    for e in r.errors:
        print(f"  FAIL {e}")
    print()
    n_err = len(r.errors)
    n_warn = len(r.warnings)
    if n_err > 0:
        print(f"RESULT: {n_err} error(s), {n_warn} warning(s) — exit 1")
        return 1
    if strict and n_warn > 0:
        print(f"RESULT: 0 errors but {n_warn} warning(s) and --strict; exit 1")
        return 1
    print(f"RESULT: 0 errors, {n_warn} warning(s) — exit 0")
    return 0


def main():
    p = argparse.ArgumentParser(description="Hs AI-Refresh Consistency Checker")
    p.add_argument("--profile", choices=["default", "ai-current"], default="default")
    p.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = p.parse_args()
    sys.exit(run(args.profile, args.strict))


if __name__ == "__main__":
    main()
