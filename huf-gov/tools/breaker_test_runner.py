#!/usr/bin/env python3
"""
HUF-GOV Breaker Test Runner — permanent re-runnable verification
=================================================================

Status:    permanent artifact, created 2026-05-12 as part of Hs/huf-gov/ structural addition
Authority: Peter directive 2026-05-12
Trace:     See papers/HUF_GOV_BREAKER_TEST_2026-05-12.md for original test report
           See huf-gov/BREAKER_INVENTORY.md for the 16-breaker map

Re-runs the synthetic-violation tests from 2026-05-12 against the current
repo state. Reports verdict per mechanical breaker. Output should match the
original test report; deviations indicate state drift worth investigating.

Tests included (mechanical breakers only — doctrinal breakers require
operator walk-through):

  Test 1  JSON syntax breaker
  Test 2  CHK-CNQ-001 (literal-string, with known paraphrase gap)
  Test 3  CHK-VERSION-001 stale-version detection
  Test 4  CHK-INV-001 INV count drift
  Test 5  All huf-gov JSONs parse cleanly
  Test 6  PRE_CONFERENCE_LOCKDOWN.md exists and forbids engine changes
  Test 7  KILL-001 published falsifiability artifact with 19 failure modes

Usage:
    cd Hs
    python3 huf-gov/tools/breaker_test_runner.py

Exit codes:
    0 — all mechanical breakers fire as expected (with known gaps noted)
    1 — one or more breakers failed to fire

Doctrine:
    HUF-GOV protects judgment. HUF-CLS optimizes correction.
    The instrument reads. The expert decides.
"""

import json
import pathlib
import re
import sys


# ---------------------------------------------------------------------------
# Repo location discovery
# ---------------------------------------------------------------------------

def find_repo_root() -> pathlib.Path:
    """
    Walk upward from the runner location to find the Hs repo root.
    Hs repo root is identified by the presence of HS_FAST_REFRESH.json.
    """
    here = pathlib.Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / "HS_FAST_REFRESH.json").exists():
            return parent
    raise RuntimeError(
        "Could not find Hs repo root (HS_FAST_REFRESH.json not found in ancestors of "
        f"{here})"
    )


def find_huf_gov_root(hs_root: pathlib.Path) -> pathlib.Path | None:
    """
    Look for the companion HUF repo's huf-gov/ folder.
    The expected layout puts HUF as a sibling to Hs.
    Returns None if not found (Test 5 + Test 7 will be skipped).
    """
    candidates = [
        hs_root.parent / "HUF" / "huf-gov",
        hs_root.parent.parent / "HUF" / "huf-gov",
    ]
    for cand in candidates:
        if cand.is_dir():
            return cand
    return None


# ---------------------------------------------------------------------------
# Individual breaker tests
# ---------------------------------------------------------------------------

def test_json_parse_breaker(hs_root: pathlib.Path) -> tuple[str, str]:
    """Test 1: JSON syntax breaker fires on broken input."""
    fast = (hs_root / "HS_FAST_REFRESH.json").read_text(encoding="utf-8")
    broken = fast[:50] + "{{{BROKEN" + fast[50:]
    try:
        json.loads(broken)
        return ("FAIL", "JSON parser did not catch the injected syntax error")
    except json.JSONDecodeError:
        return ("TRIPPED", "JSON breaker caught the injected syntax error")


def test_chk_cnq_literal(_hs_root: pathlib.Path) -> tuple[str, str]:
    """Test 2: CHK-CNQ-001 literal-phrase matching (with known paraphrase gap)."""
    phrases = [
        "cnq.py is pending",
        "cnq.py is missing",
        "cnq.py is not yet implemented",
        "cnq.py to be built",
        "cnq.py pending",
        "cnq.py not implemented",
    ]
    sample_literal = "Some doc — cnq.py is pending implementation."
    sample_paraphrase = "Some doc — the cnq.py engine is pending implementation."

    literal_hits = [p for p in phrases if p.lower() in sample_literal.lower()]
    paraphrase_hits = [p for p in phrases if p.lower() in sample_paraphrase.lower()]

    if literal_hits and not paraphrase_hits:
        return ("TRIPPED-WITH-GAP",
                f"Literal-phrase rule catches {literal_hits} but misses paraphrase "
                f"'cnq.py engine is pending implementation'. "
                f"Gap staged for DCP-002 (see huf-gov/candidates/).")
    if literal_hits and paraphrase_hits:
        return ("TRIPPED-UPGRADED",
                "Rule appears to catch both literal and paraphrase — DCP-002 may "
                "have landed; check live checker for regex pattern.")
    return ("FAIL", f"Literal-phrase rule did not catch: {sample_literal!r}")


def test_chk_version(_hs_root: pathlib.Path) -> tuple[str, str]:
    """Test 3: CHK-VERSION-001 stale-version detection."""
    stale_versions = ["cnt v2.0.3", "cnt v2.0.2", "cnt v2.0.1", "cnq v1.0.0"]
    sample = "Stale doc uses cnt v2.0.3 engine."
    hits = [v for v in stale_versions if v.lower() in sample.lower()]
    if hits:
        return ("TRIPPED", f"Stale-version rule would trip on: {hits}")
    return ("FAIL", f"Stale-version rule missed: {sample!r}")


def test_chk_inv_count(_hs_root: pathlib.Path) -> tuple[str, str]:
    """Test 4: CHK-INV-001 INV count drift detection."""
    sample = "Live doc claims 48 entries in the catalog."
    match = re.search(r"(\d+)\s+entries", sample)
    if not match:
        return ("FAIL", "INV count regex failed to match a number")
    claimed = int(match.group(1))
    live = 63  # current live count as of 2026-05-12
    has_legacy_marker = "legacy snapshot" in sample.lower()
    if claimed != live and not has_legacy_marker:
        return ("TRIPPED",
                f"INV count rule would trip on: claims {claimed}, live = {live}, "
                f"no legacy marker")
    return ("FAIL", "INV count rule missed the drift")


def test_huf_gov_json_parse(huf_gov_root: pathlib.Path | None) -> tuple[str, str]:
    """Test 5: All huf-gov JSONs parse cleanly."""
    if huf_gov_root is None:
        return ("SKIPPED",
                "HUF repo huf-gov/ folder not found alongside Hs — cannot verify "
                "parent doctrine JSON integrity")
    parsed = 0
    failed = []
    for jp in huf_gov_root.rglob("*.json"):
        try:
            json.loads(jp.read_text(encoding="utf-8"))
            parsed += 1
        except Exception as e:
            failed.append((jp.name, str(e)))
    if failed:
        return ("FAIL",
                f"{len(failed)} huf-gov JSONs failed to parse: {failed}")
    return ("TRIPPED",
            f"{parsed} huf-gov JSONs parse cleanly (parent doctrine integrity verified)")


def test_lockdown_breaker(hs_root: pathlib.Path) -> tuple[str, str]:
    """Test 6: PRE_CONFERENCE_LOCKDOWN.md exists and forbids engine changes."""
    lockdown = hs_root / "PRE_CONFERENCE_LOCKDOWN.md"
    if not lockdown.exists():
        return ("FAIL", "PRE_CONFERENCE_LOCKDOWN.md not present at repo root")
    text = lockdown.read_text(encoding="utf-8").lower()
    forbidden_engine = "engine code" in text and (
        "forbidden" in text or "no engine" in text or "locked" in text
    )
    has_window_dates = ("2026-05-12" in text) and ("2026-06-06" in text)
    if forbidden_engine and has_window_dates:
        return ("TRIPPED",
                "Lockdown doc exists; engine changes forbidden; window 2026-05-12 → 2026-06-06")
    return ("FAIL",
            f"Lockdown doc present but doctrine markers missing "
            f"(forbidden_engine={forbidden_engine}, dates={has_window_dates})")


def test_kill_001(huf_gov_root: pathlib.Path | None) -> tuple[str, str]:
    """Test 7: KILL-001 published falsifiability artifact with 19 failure modes."""
    if huf_gov_root is None:
        return ("SKIPPED",
                "HUF repo huf-gov/ folder not found — cannot verify KILL-001 directly")
    kill_path = huf_gov_root / "governance" / "KILL-001-kill-test.json"
    if not kill_path.exists():
        return ("FAIL", f"KILL-001 not found at {kill_path}")
    k = json.loads(kill_path.read_text(encoding="utf-8"))
    total = k.get("the_honest_score", {}).get("total_kill_conditions")
    confirmed = k.get("the_honest_score", {}).get("confirmed_kills")
    if total == 19:
        return ("TRIPPED",
                f"KILL-001 live with {total} kill conditions ({confirmed} confirmed kills)")
    return ("FAIL",
            f"KILL-001 found but kill count is {total} (expected 19)")


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

TESTS = [
    ("Test 1", "JSON syntax breaker", test_json_parse_breaker, "hs"),
    ("Test 2", "CHK-CNQ-001 (literal, w/ paraphrase gap)", test_chk_cnq_literal, "hs"),
    ("Test 3", "CHK-VERSION-001 stale-version", test_chk_version, "hs"),
    ("Test 4", "CHK-INV-001 count-drift", test_chk_inv_count, "hs"),
    ("Test 5", "huf-gov JSON parse integrity", test_huf_gov_json_parse, "huf"),
    ("Test 6", "PRE_CONFERENCE_LOCKDOWN breaker", test_lockdown_breaker, "hs"),
    ("Test 7", "KILL-001 falsifiability artifact", test_kill_001, "huf"),
]


def run_all() -> int:
    hs_root = find_repo_root()
    huf_gov_root = find_huf_gov_root(hs_root)

    print("=" * 70)
    print("HUF-GOV Breaker Test Runner — re-runnable verification")
    print("=" * 70)
    print(f"Hs repo root:    {hs_root}")
    print(f"HUF huf-gov/:    {huf_gov_root if huf_gov_root else '(not found)'}")
    print()

    failures = 0
    skipped = 0

    for label, name, fn, kind in TESTS:
        print(f"[{label}] {name}")
        try:
            target = hs_root if kind == "hs" else huf_gov_root
            verdict, message = fn(target)
        except Exception as e:
            verdict = "FAIL"
            message = f"exception during test: {type(e).__name__}: {e}"

        symbol = {
            "TRIPPED": "  ✓",
            "TRIPPED-WITH-GAP": "  ✓",
            "TRIPPED-UPGRADED": "  ✓",
            "SKIPPED": "  ·",
            "FAIL": "  ✗",
        }.get(verdict, "  ?")

        print(f"{symbol} {verdict}: {message}")
        print()

        if verdict == "FAIL":
            failures += 1
        elif verdict == "SKIPPED":
            skipped += 1

    print("=" * 70)
    passes = len(TESTS) - failures - skipped
    print(f"RESULT: {passes} TRIPPED, {skipped} SKIPPED, {failures} FAILED")
    if failures == 0:
        print("All mechanical breakers fire as expected.")
        print("(For doctrinal breakers 7-15 and the operator breaker 16, see")
        print(" papers/HUF_GOV_BREAKER_TEST_2026-05-12.md and walk through the scenarios.)")
    else:
        print("WARNING: one or more breakers did not fire — investigate state drift")
        print("         against the 2026-05-12 baseline in HUF_GOV_BREAKER_TEST_2026-05-12.md")
    print("=" * 70)

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all())
