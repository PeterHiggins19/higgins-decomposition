"""Determinism contract tests for the CNQ engine.

These tests verify that the canonical-JSON serializer + SHA-256 produce
identical hashes for identical inputs, and that the strip-volatile-fields
layer correctly removes clock-dependent fields from the hashed payload.

Pseudocode reference: HCI-CNQ/engine/CNQ_PSEUDOCODE.md §7.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import hashing as H  # noqa: E402  — added by conftest.py
import cnq as CNQ    # noqa: E402


# ─────────────────────────────────────────────────────────────────────
# Canonical-JSON layer
# ─────────────────────────────────────────────────────────────────────

def test_canonical_dumps_sorts_keys():
    a = {"b": 1, "a": 2, "c": 3}
    b = {"c": 3, "a": 2, "b": 1}
    assert H.canonical_dumps(a) == H.canonical_dumps(b)


def test_canonical_dumps_strips_clock_fields():
    a = {"engine": "X", "generated": "2026-05-08T12:00:00Z", "value": 1}
    b = {"engine": "X", "generated": "2099-01-01T00:00:00Z", "value": 1}
    # Different timestamps but same content → same canonical string.
    assert H.canonical_dumps(a) == H.canonical_dumps(b)
    assert H.canonical_sha256(a) == H.canonical_sha256(b)


def test_canonical_dumps_strips_nested_clock_fields():
    a = {"metadata": {"engine": "X", "generated": "T1", "v": 1}}
    b = {"metadata": {"engine": "X", "generated": "T2", "v": 1}}
    assert H.canonical_sha256(a) == H.canonical_sha256(b)


def test_canonical_dumps_no_whitespace():
    s = H.canonical_dumps({"a": 1, "b": [1, 2, 3]})
    assert " " not in s
    assert "\n" not in s


def test_canonical_dumps_ascii_safe():
    """Unicode keys/values get \\u-escaped to keep the byte stream ASCII."""
    s = H.canonical_dumps({"sigma": "σ"})
    assert "\\u03c3" in s


def test_sha256_is_lowercase_hex():
    h = H.canonical_sha256({"a": 1})
    assert len(h) == 64
    assert h == h.lower()
    assert all(c in "0123456789abcdef" for c in h)


# ─────────────────────────────────────────────────────────────────────
# End-to-end determinism on a real CNT JSON
# ─────────────────────────────────────────────────────────────────────

@pytest.fixture
def repo_root():
    """Locate the repo root; skip if not running from a checkout."""
    here = Path(__file__).resolve()
    for ancestor in [here, *here.parents]:
        if (ancestor / "HCI-CNT").exists() and (ancestor / "HCI-CNQ").exists():
            return ancestor
    pytest.skip("Not running from a repo checkout; skipping integration test")


@pytest.fixture
def planck_cnt_json(repo_root):
    p = repo_root / "HCI-CNQ" / "experiments" / "planck_cmb_quaternion" / "planck_cmb_boson_cnt.json"
    if not p.exists():
        pytest.skip(f"Planck CNT JSON not found at {p}")
    return p


@pytest.fixture
def planck_csv(repo_root):
    p = repo_root / "HCI-CNQ" / "experiments" / "planck_cmb_quaternion" / "planck_cmb_boson_input.csv"
    if not p.exists():
        pytest.skip(f"Planck input CSV not found at {p}")
    return p


def test_two_runs_identical_hash(tmp_path, planck_cnt_json, planck_csv):
    """Two runs of cnq.run_cnq on the same CNT JSON produce identical
    cnq_content_sha256."""
    out1 = tmp_path / "cnq_run1.json"
    out2 = tmp_path / "cnq_run2.json"

    p1 = CNQ.run_cnq(cnt_json_path=planck_cnt_json,
                     input_csv_path=planck_csv, out_path=out1)
    p2 = CNQ.run_cnq(cnt_json_path=planck_cnt_json,
                     input_csv_path=planck_csv, out_path=out2)

    assert p1["cnq_content_sha256"] == p2["cnq_content_sha256"]
    # The on-disk JSON file metadata.generated will differ but the hashes
    # should not — that is the determinism contract.


def test_parent_cnt_hash_carried_forward(tmp_path, planck_cnt_json, planck_csv):
    """The parent CNT JSON's diagnostics.content_sha256 must appear verbatim
    as provenance.parent_cnt_content_sha256 in the CNQ output."""
    out = tmp_path / "cnq_run.json"
    payload = CNQ.run_cnq(cnt_json_path=planck_cnt_json,
                          input_csv_path=planck_csv, out_path=out)

    cnt_json = json.loads(planck_cnt_json.read_text())
    expected = cnt_json["diagnostics"]["content_sha256"]
    actual = payload["provenance"]["parent_cnt_content_sha256"]
    assert actual == expected


def test_planck_max_residual_at_ieee_floor(tmp_path, planck_cnt_json, planck_csv):
    """The Planck CMB D=4 max residual must equal the published value
    4.440892098500626e-16 to the last digit."""
    out = tmp_path / "cnq_run.json"
    payload = CNQ.run_cnq(cnt_json_path=planck_cnt_json,
                          input_csv_path=planck_csv, out_path=out)
    qp = payload["cnq_view"]["quaternion_path"]
    assert qp["max_residual"] == 4.440892098500626e-16
    assert qp["gate_pass"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
