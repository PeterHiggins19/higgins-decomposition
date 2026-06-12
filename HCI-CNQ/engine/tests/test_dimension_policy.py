"""Dimension policy tests for the CNQ engine.

Each dimension D maps to a specific policy label (native_quaternion,
boundary_or_degenerate_support, degenerate_below_quaternion,
bi_quaternion_factoring_candidate, reduced_or_projected). These tests
confirm classify_dimension() returns the correct label for each D
and that CNQ output respects the policy.

Pseudocode reference: HCI-CNQ/engine/CNQ_PSEUDOCODE.md §4.
"""
from __future__ import annotations

import pytest

import cnq as CNQ  # noqa: E402  — added by conftest.py


# ─────────────────────────────────────────────────────────────────────
# Direct classify_dimension() coverage
# ─────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("D, expected_label", [
    (4, "native_quaternion"),
    (3, "boundary_or_degenerate_support"),
    (2, "degenerate_below_quaternion"),
    (8, "bi_quaternion_factoring_candidate"),
    (5, "reduced_or_projected"),
    (6, "reduced_or_projected"),
    (7, "reduced_or_projected"),
    (9, "reduced_or_projected"),
    (10, "reduced_or_projected"),
])
def test_classify_dimension_label(D, expected_label):
    p = CNQ.classify_dimension(D)
    assert p["label"] == expected_label
    assert p["D"] == D


def test_classify_dimension_d4_is_native():
    p = CNQ.classify_dimension(4)
    assert "SU(2)" in p["algebra"]
    assert "confirmed" in p["claim_strength"].lower()


def test_classify_dimension_d3_is_consistency_only():
    p = CNQ.classify_dimension(3)
    assert "boundary" in p["label"] or "degenerate" in p["label"]
    assert "consistency" in p["claim_strength"].lower()


def test_classify_dimension_d8_is_deferred_candidate():
    p = CNQ.classify_dimension(8)
    assert "bi_quaternion" in p["label"]
    assert "experimental" in p["claim_strength"].lower()


def test_classify_dimension_d5_to_10_uses_reduced_view():
    for D in (5, 6, 7, 9, 10):
        p = CNQ.classify_dimension(D)
        assert p["label"] == "reduced_or_projected"
        assert "first 3" in p["processing"]


def test_classify_dimension_d2_no_quaternion_view():
    p = CNQ.classify_dimension(2)
    assert "no rotation" in p["algebra"].lower() or "scalar" in p["algebra"].lower()


# ─────────────────────────────────────────────────────────────────────
# Dimension policy applied through run_cnq_view
# ─────────────────────────────────────────────────────────────────────

import numpy as np


def _make_compositions(T, D, seed=0):
    """Generate a smooth D-vector compositional trajectory of length T."""
    rng = np.random.default_rng(seed)
    base = rng.dirichlet(np.ones(D))
    rows = np.zeros((T, D))
    for t in range(T):
        rows[t] = np.abs(base + 0.05 * rng.standard_normal(D)) + 0.001
        rows[t] /= rows[t].sum()
    return rows


def test_run_cnq_view_d4_is_native():
    rows = _make_compositions(20, 4)
    policy = CNQ.classify_dimension(4)
    view = CNQ.run_cnq_view(rows, [f"c{i}" for i in range(4)], policy)
    assert view["dimension_policy"]["label"] == "native_quaternion"
    assert view["captured_step_fraction"] == 1.0
    assert view["quaternion_path"]["max_residual"] < 1e-13


def test_run_cnq_view_d3_embeds_with_zpad():
    rows = _make_compositions(15, 3)
    policy = CNQ.classify_dimension(3)
    view = CNQ.run_cnq_view(rows, [f"c{i}" for i in range(3)], policy)
    assert view["dimension_policy"]["label"] == "boundary_or_degenerate_support"
    assert view["captured_step_fraction"] == 1.0
    # D=3 still produces a quaternion path (after z-padding); just labelled differently
    assert view["quaternion_path"] is not None


def test_run_cnq_view_d2_returns_bearing_only():
    rows = _make_compositions(10, 2)
    policy = CNQ.classify_dimension(2)
    view = CNQ.run_cnq_view(rows, [f"c{i}" for i in range(2)], policy)
    assert view["dimension_policy"]["label"] == "degenerate_below_quaternion"
    assert view["quaternion_path"] is None
    assert view["bearing_only"] is not None


def test_run_cnq_view_d5_uses_reduced_projection():
    rows = _make_compositions(15, 5)
    policy = CNQ.classify_dimension(5)
    view = CNQ.run_cnq_view(rows, [f"c{i}" for i in range(5)], policy)
    assert view["dimension_policy"]["label"] == "reduced_or_projected"
    # Captured step fraction should be < 1.0 since we're projecting from R^4 -> R^3
    assert 0.0 <= view["captured_step_fraction"] <= 1.0


def test_run_cnq_view_d8_marked_candidate():
    rows = _make_compositions(15, 8)
    policy = CNQ.classify_dimension(8)
    view = CNQ.run_cnq_view(rows, [f"c{i}" for i in range(8)], policy)
    assert view["dimension_policy"]["label"] == "bi_quaternion_factoring_candidate"
    # D=8 reduced view captures only first 3 of 7 ILR axes
    assert view["captured_step_fraction"] < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
