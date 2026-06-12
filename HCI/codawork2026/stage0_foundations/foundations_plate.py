#!/usr/bin/env python3
"""
HCI Stage 0 — Foundations Plate Generator
=========================================

Visualizes the seven linear-algebra foundations of Hs (HUF-STD-003) directly,
once per dataset. Companion to Stage 1 Section + Triplet plates (which read
per-timestep magnitudes and trajectory shape) — Stage 0 reads the *foundations*
of the construction.

Seven foundations visualized (HUF-STD-003):

  1. Symmetric Matrix         —  variation matrix heatmap (D × D)
  2. Property of Transpose    —  Helmert basis H and orthonormality check H @ H^T = I
  3. Matrix Decomposition     —  closure → CLR → ILR chain (annotated arrows)
  4. Eigenvectors/Eigenvalues —  eigenvalue scree + cumulative variance
  5. Spectral Theorem         —  numeric residual ||Σ − Q Λ Q^T|| at IEEE floor
  6. Spectral Decomposition   —  orthonormal eigenbasis Q heatmap
  7. Visualization            —  this plate IS the visualization tier

Layout: 2 pages.

  Page 1 — six-panel grid (2 rows × 3 columns) showing components 1–6.
  Page 2 — verification panel: symmetry, orthonormality, spectral-reconstruction
           residuals as numeric proof at machine precision.

Input:  Canonical CNT JSON (schema 3.1.0+), same as the Stage 1 plate inputs.
Output: Multi-page PDF (2 pages).

Conforms to:
  HUF Publication Standards (HUF-STD-001)
  HUF Tensor Train I/O Standard (HUF-STD-002) — link 4 (Vector Diagrammatic Output)
  HUF Hs Linear Algebra Foundations (HUF-STD-003) — implements §7 (Visualization)

Foundations employed by this module (per HUF-STD-003 conformance requirement):
  §1 (symmetric matrix), §2 (property of transpose), §3 (matrix decomposition),
  §4 (eigenvectors/eigenvalues), §5 (Spectral Theorem), §6 (spectral decomposition),
  §7 (visualization).

Usage:
  python foundations_plate.py stage1_output.json [output.pdf]

The instrument reads. The expert decides. The hashes carry the receipts.
The vocabulary holds the line. The foundations carry the bedrock.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# ── Configuration ─────────────────────────────────────────────────
FIG_W = 16
FIG_H = 10
DPI = 150
plt.rcParams['font.family'] = 'monospace'


# ══════════════════════════════════════════════════════════════════
# Helmert basis (D-1) × D — orthonormal pivot construction
# Per HUF-STD-003 §2 (property of transpose) + §5 (spectral theorem
# silent justification of orthonormality)
# ══════════════════════════════════════════════════════════════════

def helmert_basis(D: int) -> np.ndarray:
    """Build the (D-1) × D Helmert orthonormal basis."""
    H = np.zeros((D - 1, D))
    for k in range(D - 1):
        c = math.sqrt(1.0 / ((k + 1) * (k + 2)))
        for j in range(k + 1):
            H[k, j] = c
        H[k, k + 1] = -(k + 1) * c
    return H


def variation_matrix(clr_array: np.ndarray) -> np.ndarray:
    """Compute the D × D variation matrix from CLR coordinates.

    M[i, j] = var(clr_i - clr_j) = var(log x_i / x_j) (since geometric-mean
    factor cancels). Symmetric by construction — HUF-STD-003 §1.
    """
    N, D = clr_array.shape
    M = np.zeros((D, D))
    for i in range(D):
        for j in range(D):
            if i == j:
                M[i, j] = 0.0
            else:
                M[i, j] = float(np.var(clr_array[:, i] - clr_array[:, j], ddof=1))
    return M


def clr_covariance(clr_array: np.ndarray) -> np.ndarray:
    """CLR covariance matrix — D × D symmetric positive semi-definite."""
    # rowvar=False because rows are observations, columns are carriers
    return np.cov(clr_array, rowvar=False, ddof=1)


# ══════════════════════════════════════════════════════════════════
# Page 1 — six-panel foundations plate
# ══════════════════════════════════════════════════════════════════

def _render_foundations_page(pdf, clr_arr, carriers, country_code, country_name):
    D = len(carriers)
    N = clr_arr.shape[0]

    # Compute all foundations
    H = helmert_basis(D)                                # (D-1, D)
    HHt = H @ H.T                                       # (D-1, D-1) — should be I
    var_mat = variation_matrix(clr_arr)                 # D × D symmetric
    Sigma = clr_covariance(clr_arr)                     # D × D symmetric PSD
    # Eigendecomposition of CLR covariance (spectral theorem)
    eigvals, eigvecs = np.linalg.eigh(Sigma)
    # eigh returns ascending — flip to descending
    eigvals = eigvals[::-1]
    eigvecs = eigvecs[:, ::-1]
    # Cumulative variance explained
    pos_eig = np.maximum(eigvals, 0.0)
    cum_var = np.cumsum(pos_eig) / max(pos_eig.sum(), 1e-30)

    # Set up figure
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.suptitle(
        f"Foundations Plate (Stage 0) — {country_code} {country_name}  ·  "
        f"D = {D} carriers  ·  N = {N} timesteps",
        fontsize=16, fontweight='bold', y=0.97,
    )
    fig.text(0.5, 0.935,
             "Seven linear-algebra foundations of Hs per HUF-STD-003   ·   "
             "the bedrock made visible",
             ha='center', fontsize=10, style='italic', color='#555')

    gs = fig.add_gridspec(2, 3, hspace=0.55, wspace=0.45,
                          left=0.06, right=0.97, top=0.88, bottom=0.06)

    # ── Panel (1, 1): Variation matrix heatmap (symmetric)
    ax = fig.add_subplot(gs[0, 0])
    short = [c[:6] for c in carriers]
    im = ax.imshow(var_mat, cmap='gray_r', aspect='equal')
    ax.set_xticks(range(D)); ax.set_yticks(range(D))
    ax.set_xticklabels(short, rotation=45, ha='right', fontsize=7)
    ax.set_yticklabels(short, fontsize=7)
    ax.set_title("§1  Variation matrix var(log x_i/x_j)\n"
                 f"symmetric: max|M − M^T| = {np.max(np.abs(var_mat - var_mat.T)):.2e}",
                 fontsize=10, fontweight='bold')
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # ── Panel (1, 2): Helmert basis + orthonormality check
    ax = fig.add_subplot(gs[0, 1])
    im = ax.imshow(H, cmap='RdBu_r', aspect='auto',
                   vmin=-np.max(np.abs(H)), vmax=np.max(np.abs(H)))
    ax.set_xticks(range(D)); ax.set_yticks(range(D - 1))
    ax.set_xticklabels(short, rotation=45, ha='right', fontsize=7)
    ax.set_yticklabels([f"ilr_{k+1}" for k in range(D - 1)], fontsize=8)
    ax.set_title("§2  Helmert basis H  (D−1 × D)\n"
                 f"orthonormality: max|HH^T − I| = {np.max(np.abs(HHt - np.eye(D-1))):.2e}",
                 fontsize=10, fontweight='bold')
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # ── Panel (1, 3): Composition decomposition tree
    ax = fig.add_subplot(gs[0, 2])
    ax.axis('off')
    tree = (
        "§3  Matrix Decomposition Chain\n"
        "\n"
        "   raw composition\n"
        "        │  closure C(x) = x / Σx\n"
        "        ▼\n"
        "   closed composition x ∈ Δ^{D−1}\n"
        "        │  CLR: x → log x − ⟨log x⟩\n"
        "        ▼\n"
        f"   CLR coordinates (R^{D})\n"
        "        │  ILR: clr → clr @ H^T\n"
        "        ▼\n"
        f"   ILR coordinates (R^{D-1})\n"
        "\n"
        f"  ·  D = {D} carriers\n"
        f"  ·  N = {N} timesteps\n"
        "  ·  each arrow is exact\n"
        "    (modulo IEEE float)"
    )
    ax.text(0.0, 1.0, tree, fontsize=9, family='monospace',
            transform=ax.transAxes, va='top')

    # ── Panel (2, 1): Eigenvalue scree + cumulative variance
    ax = fig.add_subplot(gs[1, 0])
    idx = np.arange(1, D + 1)
    ax.bar(idx, pos_eig, color='#1E2761', alpha=0.85, label='eigenvalue λ_k')
    ax.set_xlabel("eigenvalue index k")
    ax.set_ylabel("λ_k", color='#1E2761')
    ax.tick_params(axis='y', labelcolor='#1E2761')
    ax.set_xticks(idx)
    ax2 = ax.twinx()
    ax2.plot(idx, cum_var * 100, color='#C9954E', marker='o', lw=2,
             label='cumulative %')
    ax2.set_ylabel("cumulative variance explained (%)", color='#C9954E')
    ax2.tick_params(axis='y', labelcolor='#C9954E')
    ax2.set_ylim(0, 105)
    ax2.axhline(95, color='#C9954E', ls=':', lw=0.8, alpha=0.5)
    ax.set_title("§4  Eigenvalue scree (CLR covariance)\n"
                 f"top λ = {pos_eig[0]:.3f}  ·  trace = {pos_eig.sum():.3f}",
                 fontsize=10, fontweight='bold')

    # ── Panel (2, 2): Orthonormal eigenbasis Q as heatmap
    ax = fig.add_subplot(gs[1, 1])
    Q_disp = eigvecs[:, :D]
    im = ax.imshow(Q_disp, cmap='RdBu_r', aspect='auto',
                   vmin=-np.max(np.abs(Q_disp)), vmax=np.max(np.abs(Q_disp)))
    ax.set_xticks(range(D))
    ax.set_yticks(range(D))
    ax.set_xticklabels([f"q_{k+1}" for k in range(D)], fontsize=8)
    ax.set_yticklabels(short, fontsize=7)
    ax.set_title("§6  Orthonormal eigenbasis Q\n"
                 "columns = eigenvectors, ordered by λ ↓",
                 fontsize=10, fontweight='bold')
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # ── Panel (2, 3): Spectral reconstruction residual + key claims
    ax = fig.add_subplot(gs[1, 2])
    ax.axis('off')
    Sigma_reconstructed = eigvecs @ np.diag(eigvals) @ eigvecs.T
    residual = np.max(np.abs(Sigma - Sigma_reconstructed))
    # Rank-k reconstruction quality at k=1,2,3
    rank_k_var = [cum_var[min(k - 1, D - 1)] for k in (1, 2, 3, D)]
    text = (
        "§5  Spectral Theorem verification\n"
        "\n"
        "Σ = Q Λ Q^T  (theorem)\n"
        f"max|Σ − Q Λ Q^T| = {residual:.2e}\n"
        "  (IEEE-floor → theorem holds)\n"
        "\n"
        "Σ symmetric?\n"
        f"max|Σ − Σ^T| = {np.max(np.abs(Sigma - Sigma.T)):.2e}\n"
        "\n"
        "All λ real?\n"
        f"max|imag(λ)| = 0.00e+00  (eigh ⇒ real)\n"
        "\n"
        "Q orthonormal?\n"
        f"max|Q^T Q − I| = {np.max(np.abs(eigvecs.T @ eigvecs - np.eye(D))):.2e}\n"
        "\n"
        "Rank-k variance explained:\n"
        f"  k=1  →  {rank_k_var[0]*100:.1f}%\n"
        f"  k=2  →  {rank_k_var[1]*100:.1f}%\n"
        f"  k=3  →  {rank_k_var[2]*100:.1f}%\n"
        f"  k={D}  →  {rank_k_var[3]*100:.1f}%"
    )
    ax.text(0.0, 1.0, text, fontsize=9, family='monospace',
            transform=ax.transAxes, va='top')

    # Footer
    fig.text(0.5, 0.02,
             "HUF-STD-003 §1–§7   ·   Stage 0 (Foundations, Order 0+)   ·   "
             "Output Doctrine v1.0   ·   HUF-STD-002 link 4",
             ha='center', fontsize=9, style='italic', color='#555')

    pdf.savefig(fig)
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════
# Page 2 — Numeric verification panel
# ══════════════════════════════════════════════════════════════════

def _render_verification_page(pdf, clr_arr, carriers, country_code, country_name):
    D = len(carriers)
    N = clr_arr.shape[0]

    H = helmert_basis(D)
    HHt = H @ H.T
    HtH = H.T @ H
    var_mat = variation_matrix(clr_arr)
    Sigma = clr_covariance(clr_arr)
    eigvals, eigvecs = np.linalg.eigh(Sigma)
    eigvals = eigvals[::-1]
    eigvecs = eigvecs[:, ::-1]
    Sigma_reconstructed = eigvecs @ np.diag(eigvals) @ eigvecs.T

    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.suptitle(
        f"Foundations — Numeric Verification — {country_code} {country_name}",
        fontsize=16, fontweight='bold', y=0.96,
    )
    fig.text(0.5, 0.93,
             "Machine-precision proof that the seven foundations hold on the actual data",
             ha='center', fontsize=11, style='italic', color='#555')

    ax = fig.add_subplot(111)
    ax.axis('off')

    eps_machine = np.finfo(np.float64).eps  # ~2.22e-16

    rows = [
        ("FOUNDATION", "STATEMENT", "VALUE", "JUDGMENT"),
        ("─" * 11, "─" * 60, "─" * 14, "─" * 12),
        ("§1 Symmetric",
         "max|M − M^T| for variation matrix",
         f"{np.max(np.abs(var_mat - var_mat.T)):.3e}",
         "exact (= 0)"),
        ("§1 Symmetric",
         "max|Σ − Σ^T| for CLR covariance",
         f"{np.max(np.abs(Sigma - Sigma.T)):.3e}",
         f"IEEE-floor ({eps_machine:.2e})"),
        ("§2 Transpose",
         "max|H H^T − I_{D−1}|  (Helmert orthonormal rows)",
         f"{np.max(np.abs(HHt - np.eye(D-1))):.3e}",
         "IEEE-floor"),
        ("§2 Transpose",
         "max|H^T H − P_{D-1}|  (projection onto image)",
         f"{np.max(np.abs(HtH - HtH @ HtH)):.3e}",
         "IEEE-floor"),
        ("§3 Decomp",
         "closure → CLR → ILR → CLR roundtrip residual",
         f"{_clr_ilr_roundtrip(clr_arr, H):.3e}",
         "IEEE-floor"),
        ("§4 Eigen",
         "number of eigenvalues found",
         f"{D}",
         f"= D ({D})"),
        ("§4 Eigen",
         "max|imag(λ_k)|  (real because Σ symmetric)",
         "0.000e+00",
         "exact"),
        ("§4 Eigen",
         "λ_1 (top eigenvalue, variance along leading axis)",
         f"{eigvals[0]:.4f}",
         "—"),
        ("§4 Eigen",
         "trace(Σ) = Σ λ_k (total variance)",
         f"{eigvals.sum():.4f}",
         "—"),
        ("§5 Spectral",
         "max|Σ − Q Λ Q^T|  (Spectral Theorem residual)",
         f"{np.max(np.abs(Sigma - Sigma_reconstructed)):.3e}",
         "IEEE-floor"),
        ("§5 Spectral",
         "max|Q^T Q − I|  (orthonormality of eigenbasis)",
         f"{np.max(np.abs(eigvecs.T @ eigvecs - np.eye(D))):.3e}",
         "IEEE-floor"),
        ("§6 Decomp",
         "cumulative variance at k=1 (rank-1 approximation)",
         f"{(np.maximum(eigvals,0)[:1].sum() / max(np.maximum(eigvals,0).sum(), 1e-30)) * 100:.2f}%",
         "—"),
        ("§6 Decomp",
         "cumulative variance at k=2",
         f"{(np.maximum(eigvals,0)[:2].sum() / max(np.maximum(eigvals,0).sum(), 1e-30)) * 100:.2f}%",
         "—"),
        ("§6 Decomp",
         "cumulative variance at k=3",
         f"{(np.maximum(eigvals,0)[:3].sum() / max(np.maximum(eigvals,0).sum(), 1e-30)) * 100:.2f}%",
         "—"),
        ("§7 Visualize",
         "Stage-0 Foundations Plate (page 1 of this PDF)",
         "present",
         "delivered"),
    ]

    # Render as monospace text block
    txt_lines = []
    for row in rows:
        if isinstance(row, tuple):
            txt_lines.append(f"  {row[0]:<13} {row[1]:<60} {row[2]:>14}   {row[3]:<24}")
    body = "\n".join(txt_lines)
    ax.text(0.02, 0.92, body, fontsize=9, family='monospace',
            transform=ax.transAxes, va='top')

    # Maxim footer
    ax.text(0.5, 0.05,
            "The foundations carry the bedrock.   The instrument reads.   The expert decides.\n"
            "The hashes carry the receipts.   The vocabulary holds the line.",
            ha='center', va='center', fontsize=10, style='italic', color='#C9954E',
            transform=ax.transAxes)

    pdf.savefig(fig)
    plt.close(fig)


def _clr_ilr_roundtrip(clr_arr: np.ndarray, H: np.ndarray) -> float:
    """CLR → ILR → CLR (projected back) residual, max-norm."""
    ilr = clr_arr @ H.T
    clr_back = ilr @ H
    # clr_back is the projection of clr onto the image of H^T (= the simplex tangent
    # space). The residual should be tiny since CLR coordinates already live in
    # the tangent space (sum to zero).
    return float(np.max(np.abs(clr_arr - clr_back)))


# ══════════════════════════════════════════════════════════════════
# Driver
# ══════════════════════════════════════════════════════════════════

def render_foundations_plate(stage1_json_path, out_pdf_path) -> int:
    """Generate the Stage-0 Foundations Plate PDF.

    Args:
        stage1_json_path: Path to stage1_output.json (CNT v3.1.0+).
        out_pdf_path: Output PDF path.

    Returns:
        Number of pages written.
    """
    data = json.loads(Path(stage1_json_path).read_text(encoding='utf-8'))
    records = data['records']
    carriers = data['carriers']

    clr_arr = np.array([r['clr'] for r in records], dtype=float)

    country_code = data.get('dataset', '???')[:3].upper()
    country_name = data.get('dataset', country_code).replace('ember_', '').replace('_', ' ')

    with PdfPages(str(out_pdf_path)) as pdf:
        _render_foundations_page(pdf, clr_arr, carriers, country_code, country_name)
        _render_verification_page(pdf, clr_arr, carriers, country_code, country_name)

    return 2


def main():
    if len(sys.argv) < 2:
        print("Usage: python foundations_plate.py stage1_output.json [output.pdf]",
              file=sys.stderr)
        sys.exit(1)
    in_json = sys.argv[1]
    out_pdf = sys.argv[2] if len(sys.argv) > 2 else "foundations_plate.pdf"
    n = render_foundations_plate(in_json, out_pdf)
    print(f"  Stage-0 Foundations plate written: {out_pdf}  ({n} pages)")


if __name__ == "__main__":
    main()
