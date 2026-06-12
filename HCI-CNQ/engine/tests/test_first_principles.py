"""First-principles tests for CNQ geometry and quaternion algebra.

Each test is a hand-constructed scenario where the expected output is
known to floating-point precision. These tests verify the math, not the
data; they guarantee the engine's primitives behave per the pseudocode.

Pseudocode reference: HCI-CNQ/engine/CNQ_PSEUDOCODE.md §3 (Geometry).
"""
from __future__ import annotations

import math

import numpy as np
import pytest

import geometry as G  # noqa: E402  — added by conftest.py


# ─────────────────────────────────────────────────────────────────────
# Closure / CLR
# ─────────────────────────────────────────────────────────────────────

def test_closure_sums_to_one():
    x = np.array([2.0, 3.0, 5.0])
    c = G.closure(x)
    assert math.isclose(c.sum(), 1.0, abs_tol=1e-15)
    np.testing.assert_allclose(c, [0.2, 0.3, 0.5], atol=1e-15)


def test_clr_sums_to_zero():
    x = G.closure(np.array([1.0, 2.0, 4.0, 8.0]))
    z = G.clr(x)
    assert abs(z.sum()) < 1e-15


def test_clr_translation_invariance():
    """clr is translation-invariant under multiplicative constant."""
    x = np.array([1.0, 2.0, 4.0, 8.0])
    np.testing.assert_allclose(G.clr(x), G.clr(x * 7.0), atol=1e-14)


# ─────────────────────────────────────────────────────────────────────
# Helmert basis
# ─────────────────────────────────────────────────────────────────────

def test_helmert_orthonormal():
    """H @ H.T == I_(D-1) for the Helmert orthonormal contrast matrix."""
    for D in (2, 3, 4, 5, 8, 10):
        H = G.helmert_basis(D)
        np.testing.assert_allclose(H @ H.T, np.eye(D - 1), atol=1e-14)


def test_helmert_rows_perpendicular_to_one():
    """Each Helmert row sums to zero (perpendicular to (1,1,...,1))."""
    for D in (2, 3, 4, 5, 8):
        H = G.helmert_basis(D)
        np.testing.assert_allclose(H.sum(axis=1), np.zeros(D - 1), atol=1e-14)


def test_helmert_signature_matches_pseudocode():
    """Spot-check the D=4 Helmert matrix matches the pseudocode convention."""
    H = G.helmert_basis(4)
    # Row 0: 1/sqrt(2)*(+1, -1, 0, 0)
    np.testing.assert_allclose(H[0], [1/math.sqrt(2), -1/math.sqrt(2), 0, 0], atol=1e-14)
    # Row 1: 1/sqrt(6)*(+1, +1, -2, 0)
    np.testing.assert_allclose(H[1], [1/math.sqrt(6), 1/math.sqrt(6), -2/math.sqrt(6), 0],
                                atol=1e-14)
    # Row 2: 1/sqrt(12)*(+1, +1, +1, -3)
    np.testing.assert_allclose(H[2], [1/math.sqrt(12), 1/math.sqrt(12),
                                       1/math.sqrt(12), -3/math.sqrt(12)], atol=1e-14)


# ─────────────────────────────────────────────────────────────────────
# Quaternion algebra
# ─────────────────────────────────────────────────────────────────────

def test_quat_identity_rotates_nothing():
    q = np.array([1.0, 0, 0, 0])
    v = np.array([1.0, 2.0, 3.0])
    np.testing.assert_allclose(G.quat_rotate(q, v), v, atol=1e-15)


def test_quat_180deg_around_z():
    """180° rotation around z flips x and y."""
    q = G.quat_from_axis_angle(np.array([0.0, 0, 1]), math.pi)
    v = np.array([1.0, 2.0, 3.0])
    rotated = G.quat_rotate(q, v)
    np.testing.assert_allclose(rotated, [-1.0, -2.0, 3.0], atol=1e-14)


def test_quat_conj_is_self_inverse_for_unit():
    q = G.quat_from_axis_angle(np.array([1.0, 1, 1]), math.pi / 3)
    qq = G.quat_mul(q, G.quat_conj(q))
    np.testing.assert_allclose(qq, [1.0, 0, 0, 0], atol=1e-14)


def test_hamilton_product_noncommutative():
    """The Hamilton product is non-commutative — i*j = k but j*i = -k."""
    i = np.array([0.0, 1, 0, 0])
    j = np.array([0.0, 0, 1, 0])
    k_pos = G.quat_mul(i, j)
    k_neg = G.quat_mul(j, i)
    np.testing.assert_allclose(k_pos, [0.0, 0, 0, 1], atol=1e-15)
    np.testing.assert_allclose(k_neg, [0.0, 0, 0, -1], atol=1e-15)


# ─────────────────────────────────────────────────────────────────────
# Rotation between two unit vectors (atan2-stable)
# ─────────────────────────────────────────────────────────────────────

def test_rotation_aligned_returns_identity():
    u = np.array([1.0, 0, 0])
    q = G.rotation_quaternion_between(u, u)
    np.testing.assert_allclose(q, [1.0, 0, 0, 0], atol=1e-14)


def test_rotation_recovers_target():
    """rotation_quaternion_between(u1, u2) applied to u1 must give u2."""
    rng = np.random.default_rng(seed=42)
    for _ in range(20):
        u1 = rng.standard_normal(3)
        u1 /= np.linalg.norm(u1)
        u2 = rng.standard_normal(3)
        u2 /= np.linalg.norm(u2)
        q = G.rotation_quaternion_between(u1, u2)
        rec = G.quat_rotate(q, u1)
        np.testing.assert_allclose(rec, u2, atol=1e-14)


def test_rotation_antiparallel_case():
    """Antiparallel pair: rotation should still reach the target."""
    u1 = np.array([1.0, 0, 0])
    u2 = np.array([-1.0, 0, 0])
    q = G.rotation_quaternion_between(u1, u2)
    rec = G.quat_rotate(q, u1)
    np.testing.assert_allclose(rec, u2, atol=1e-14)


# ─────────────────────────────────────────────────────────────────────
# End-to-end IEEE-floor sanity check
# ─────────────────────────────────────────────────────────────────────

def test_compositions_to_unit_vectors_pipeline():
    """Hand-constructed D=4 trajectory: closure -> CLR -> Helmert -> unit."""
    rows = np.array([
        [0.4, 0.3, 0.2, 0.1],
        [0.1, 0.4, 0.3, 0.2],
        [0.2, 0.1, 0.4, 0.3],
    ])
    units, radii = G.compositions_to_helmert_unit_vectors(rows, 4)
    assert units.shape == (3, 3)
    # Each unit vector should have norm 1 (within fp precision)
    norms = np.linalg.norm(units, axis=1)
    np.testing.assert_allclose(norms, np.ones(3), atol=1e-14)
    assert all(r > 0 for r in radii)


def test_quaternion_sandwich_residuals_at_ieee_floor():
    """For a smooth D=4 trajectory, quaternion-sandwich residuals are at
    or below IEEE floor (~1e-15)."""
    # A simple D=4 trajectory: small smooth excursion.
    T = 30
    t = np.linspace(0, 1, T)
    rows = np.column_stack([
        0.25 + 0.1 * np.cos(2 * np.pi * t),
        0.25 + 0.1 * np.sin(2 * np.pi * t),
        0.25 + 0.05 * np.cos(4 * np.pi * t),
        0.25 - 0.1 * np.cos(2 * np.pi * t) - 0.1 * np.sin(2 * np.pi * t)
                - 0.05 * np.cos(4 * np.pi * t),
    ])
    # Force positivity (some entries may go negative for large amplitudes)
    rows = np.abs(rows) + 0.01
    units, _ = G.compositions_to_helmert_unit_vectors(rows, 4)
    residuals, quats, angles = G.quaternion_sandwich_residuals(units)
    assert residuals.size == T - 1
    # Residual should be near machine epsilon — ~1e-15 or lower
    assert residuals.max() < 1e-13, (
        f"max residual {residuals.max():.3e} exceeds 1e-13 IEEE-floor budget"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
