#!/usr/bin/env python3
"""
Reference implementation of the CHK-CNQ-001 regex upgrade
==========================================================

Status:    CANDIDATE — reference implementation for DCP-002 (proposed status only)
Filed:     2026-05-12 (pre-conference lockdown S2 doc-only addition)
Authority: Peter directive 2026-05-12 + HUF Governance Charter Article V (visibility at correction)
Trace:     See DCP-002_CANDIDATE_CHK_CNQ_REGEX_UPGRADE.md in this folder

This file is a STANDALONE candidate implementation. It is NOT imported by the live
consistency checker at scripts/check_ai_refresh_consistency.py during the
pre-conference lockdown (2026-05-12 → 2026-06-06). When the lockdown clears,
DCP-002 will copy the regex pattern and check logic from this file into the
live checker via the standard DCP lifecycle (proposed → in_progress →
implemented → verified → released).

Run directly to execute the unit-test suite:
    python3 Hs/huf-gov/candidates/upgraded_chk_cnq_001.py

Expected output: all unit tests pass, no false positives, all paraphrase
catches succeed, both positive statements pass through unflagged.

Doctrine:
    HUF-GOV protects judgment. HUF-CLS optimizes correction.
    The instrument reads. The expert decides.
"""

import re
import sys


# ---------------------------------------------------------------------------
# The upgraded CHK-CNQ-001 rule
# ---------------------------------------------------------------------------

# Regex semantic-class pattern. Matches "cnq.py" within 40 characters of any
# drift-class word. Word-boundary anchors prevent false matches inside longer
# words. Case-insensitive for robustness against typo / casing variation.
CNQ_DRIFT_PATTERN = re.compile(
    r"\bcnq\.py\b"
    r"[^.\n]{0,40}"
    r"\b("
    r"pending|"
    r"missing|"
    r"not\s+(?:yet\s+)?(?:implemented|built|shipped|done|finished|coded)|"
    r"to\s+be\s+(?:built|implemented|shipped|coded)|"
    r"incomplete|"
    r"stub|"
    r"placeholder|"
    r"future\s+work"
    r")\b",
    re.IGNORECASE,
)


# File-level legacy markers that bypass the rule.
# Matches the pattern used by the existing checker.
FILE_LEVEL_LEGACY_MARKERS = (
    "**legacy snapshot**",
    "legacy snapshot:",
    "[legacy snapshot]",
    "*legacy april 2026*",
    "legacy april 2026:",
)


def file_marked_legacy(content: str) -> bool:
    """
    Return True if the file content contains a file-level legacy marker
    near the top of the file (within the first 1000 characters).
    """
    head = content[:1000].lower()
    return any(marker.lower() in head for marker in FILE_LEVEL_LEGACY_MARKERS)


def check_cnq_status_v2(file_path: str, content: str) -> dict:
    """
    Upgraded CHK-CNQ-001 rule.

    Returns a dict:
        {
            "rule_id": "CHK-CNQ-001",
            "file": <path>,
            "verdict": "PASS" | "TRIP",
            "message": <human-readable>,
            "match": <matched substring if TRIP, else None>,
        }
    """
    if file_marked_legacy(content):
        return {
            "rule_id": "CHK-CNQ-001",
            "file": file_path,
            "verdict": "PASS",
            "message": "file-level legacy marker present; stale phrases allowed",
            "match": None,
        }

    match = CNQ_DRIFT_PATTERN.search(content)
    if match:
        return {
            "rule_id": "CHK-CNQ-001",
            "file": file_path,
            "verdict": "TRIP",
            "message": f"CNQ-pending drift detected: '{match.group(0)}'",
            "match": match.group(0),
        }

    return {
        "rule_id": "CHK-CNQ-001",
        "file": file_path,
        "verdict": "PASS",
        "message": "no CNQ-pending drift detected",
        "match": None,
    }


# ---------------------------------------------------------------------------
# Unit test suite for DCP-002 verification
# ---------------------------------------------------------------------------

# Cases that MUST trip the rule (semantic drift)
SHOULD_TRIP = [
    # Original 6 literal phrases (backward compatibility)
    "The cnq.py is pending.",
    "Note: cnq.py is missing from the repo.",
    "cnq.py is not yet implemented.",
    "cnq.py to be built next sprint.",
    "Status: cnq.py pending.",
    "cnq.py not implemented at this time.",
    # Paraphrases (the new coverage)
    "The cnq.py engine is pending implementation.",
    "cnq.py is not yet built.",
    "cnq.py to be implemented in a future release.",
    "The cnq.py module is incomplete.",
    "cnq.py is currently a placeholder.",
    "cnq.py — future work.",
    "cnq.py is not yet shipped.",
    "Currently cnq.py is a stub.",
    "cnq.py: not yet coded.",
    "cnq.py needs to be implemented eventually.",  # caught via "to be implemented"
    "The cnq.py file is a stub for now.",
    "cnq.py is to be coded post-conference.",
]

# Cases that MUST NOT trip the rule (operational / positive statements)
SHOULD_PASS = [
    "cnq.py was shipped at v2.0.0.",
    "cnq.py adapter ran on Backblaze.",
    "The cnq.py engine is at v2.0.0.",
    "cnq.py produced expected hash 4.441e-16.",
    "We use cnq.py to factor at D=8.",
    "cnq.py CHSH 0.88 within Tsirelson bound.",
    "cnq.py is released.",
    "cnq.py exits 0 on EMBER corpus.",
    "cnq.py verification: 23/0/0 green.",
    "The cnq.py module supports UN-6 locales.",
]

# Cases with the legacy marker (must pass regardless of content)
SHOULD_PASS_LEGACY_MARKED = [
    "**LEGACY SNAPSHOT** — historical document.\n\ncnq.py is pending.",
    "*Legacy April 2026* notes.\n\ncnq.py is not yet implemented.",
    "[LEGACY SNAPSHOT]\nThe cnq.py engine is pending implementation.",
]


def run_tests() -> int:
    """
    Run the full unit-test suite. Return 0 on all-pass, 1 on any failure.
    """
    failures = []
    passes = 0

    print("=" * 70)
    print("DCP-002 candidate test suite — upgraded CHK-CNQ-001")
    print("=" * 70)

    # Tests that should trip
    print("\n--- Should TRIP (drift detection) ---")
    for i, sample in enumerate(SHOULD_TRIP, start=1):
        result = check_cnq_status_v2(f"test_trip_{i}.md", sample)
        if result["verdict"] == "TRIP":
            print(f"  PASS [{i:2d}] tripped on: {sample[:60]!r}")
            passes += 1
        else:
            print(f"  FAIL [{i:2d}] DID NOT TRIP: {sample!r}")
            failures.append(("SHOULD_TRIP", i, sample, result))

    # Tests that should pass (operational / positive)
    print("\n--- Should PASS (operational statements) ---")
    for i, sample in enumerate(SHOULD_PASS, start=1):
        result = check_cnq_status_v2(f"test_pass_{i}.md", sample)
        if result["verdict"] == "PASS":
            print(f"  PASS [{i:2d}] correctly passed: {sample[:60]!r}")
            passes += 1
        else:
            print(f"  FAIL [{i:2d}] FALSE TRIP on: {sample!r} (matched {result['match']!r})")
            failures.append(("SHOULD_PASS", i, sample, result))

    # Tests with legacy marker (must pass)
    print("\n--- Should PASS (legacy-marker bypass) ---")
    for i, sample in enumerate(SHOULD_PASS_LEGACY_MARKED, start=1):
        result = check_cnq_status_v2(f"test_legacy_{i}.md", sample)
        if result["verdict"] == "PASS" and "legacy marker" in result["message"]:
            print(f"  PASS [{i:2d}] legacy-marker bypass worked")
            passes += 1
        else:
            print(f"  FAIL [{i:2d}] LEGACY BYPASS BROKEN: {result}")
            failures.append(("SHOULD_PASS_LEGACY_MARKED", i, sample, result))

    # Summary
    print("\n" + "=" * 70)
    total = passes + len(failures)
    if failures:
        print(f"RESULT: {len(failures)} FAILURES out of {total} tests")
        print("\nFailure details:")
        for category, idx, sample, result in failures:
            print(f"  [{category} #{idx}] {sample!r}")
            print(f"    Result: {result}")
        print("=" * 70)
        return 1
    else:
        print(f"RESULT: {passes}/{total} tests PASS — DCP-002 verification criteria met")
        print("=" * 70)
        return 0


if __name__ == "__main__":
    sys.exit(run_tests())
