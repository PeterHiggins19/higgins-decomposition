#!/usr/bin/env python3
"""
HCI-Atlas Stage 3 — Order-3 paged module (recursive / dynamical).

Reads only j["depth"]["higgins_extensions"]; emits one paged report per
dataset covering the depth-sounder output: tower convergence, period-2
attractor, IR classification, M^2 = I duality proof.

Doctrine: Order 3 = recursive / dynamical. Anything that emerges from
the recursive depth sounder belongs here.

Reading order — basic to advanced:
  1. Cover (auto-titled "Compositional system depth and dynamics for, ...")
  2. Data disclosure (Order 3 specific)
  3. Summary table (the headline numbers)
  4. Energy tower convergence (Hs(level), ω(level))
  5. Curvature tower convergence (Hs(level), ω(level))
  6. Period-2 attractor (c_even / c_odd compositions)
  7. Attractor amplitude (A) + damping (ζ) card
  8. IR classification card with the seven-class taxonomy
  9. Energy / curvature cycle detection
 10. M^2 = I involution proof (residual histogram)
 11. Dynamical depth summary
"""
from __future__ import annotations
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Re-use the Stage 2 helpers (engine signature, friendly names, footer)
from . import stage2_locked as s2  # type: ignore  # package-relative

PAGE_SIZE = (11.0, 8.5)
PDF_DPI   = 150


def _palette(n):
    base = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd",
            "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"]
    return [base[i % len(base)] for i in range(n)]


def _title3(fig, dataset_id, plate_no, plate_name, j):
    md = j["metadata"]
    name = s2._dataset_friendly(dataset_id, j)
    yrs  = s2._year_range(j)
    full = (f"Compositional system depth and dynamics for, {name}"
            + (f" {yrs}" if yrs else ""))
    fig.text(0.5, 0.972, full, ha="center", fontsize=11,
             fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.952, f"Plate {plate_no}  |  {plate_name}",
             ha="center", fontsize=9, color="#444", fontstyle="italic")
    fig.text(0.5, 0.935,
             f"Engine {md['engine_version']}  |  Schema {md['schema_version']}  |  Order 3",
             ha="center", fontsize=8, color="#666")


def _footer3(fig, j, run_id, page_num, total, method=""):
    inp = j["input"]; di = j["diagnostics"]; md = j["metadata"]
    src_sha = (inp.get("source_file_sha256") or "?")[:12]
    csha    = (di.get("content_sha256") or "?")[:12]
    eng_sig = s2.engine_signature()["short"]
    eng_v   = md.get("engine_version", "?")
    fig.text(0.5, 0.025,
             f"engine: {eng_v}  ({eng_sig}…)  |  data: {csha}…  |  source: {src_sha}…",
             ha="center", fontsize=7, family="monospace", color="#666")
    fig.text(0.5, 0.010,
             f"{s2._today_iso()}  |  run: {run_id or 'unsaved'}  |  "
             f"page {page_num}/{total}  |  STAGE 3 (Order 3)  |  {method}",
             ha="center", fontsize=7, family="monospace", color="#888")


def _depth_block(j):
    return j["depth"]["higgins_extensions"]


# ── PLATE 1 — Cover ──────────────────────────────────────────────
def p_cover(pdf, j, dataset_id, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    inp = j["input"]; md = j["metadata"]; di = j["diagnostics"]
    sig = s2.engine_signature()
    he  = _depth_block(j); summ = he["summary"]; ir = he["impulse_response"]

    name = s2._dataset_friendly(dataset_id, j)
    yrs  = s2._year_range(j)

    fig.text(0.5, 0.88, "Compositional system",
             ha="center", fontsize=22, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.83, "depth and dynamics for,",
             ha="center", fontsize=14, color="#444", fontstyle="italic")
    fig.text(0.5, 0.77, name, ha="center", fontsize=18,
             fontweight="bold", color="#222")
    if yrs:
        fig.text(0.5, 0.73, yrs, ha="center", fontsize=14, color="#222")

    rows = [
        ("Report title",  f"Compositional system depth and dynamics for, {name}"
                          + (f" {yrs}" if yrs else "")),
        ("Generated",     s2._today_iso()),
        ("Run ID",        run_id or "unsaved"),
        ("Dataset ID",    dataset_id),
        ("T (records)",   str(inp["n_records"])),
        ("D (carriers)",  str(inp["n_carriers"])),
        ("Engine version",md["engine_version"]),
        ("Schema version",md["schema_version"]),
        ("Engine signature",        sig["combined"][:32] + "…"),
        ("Source CSV SHA-256",     (inp.get("source_file_sha256") or "?")[:32] + "…"),
        ("Content SHA-256",        (di.get("content_sha256") or "?")[:32] + "…"),
        ("Curvature depth",         str(summ.get("curvature_depth"))),
        ("Energy depth",            str(summ.get("energy_depth"))),
        ("Dynamical depth",         str(summ.get("dynamical_depth"))),
        ("IR classification",       str(ir.get("classification"))),
        ("Amplitude A",  f"{(ir.get('amplitude_A') or 0):.4f}"),
        ("Damping ζ",    f"{(ir.get('damping_zeta') or 0):.4f}"),
    ]
    y = 0.62
    for k, v in rows:
        fig.text(0.10, y, f"{k:<26}", fontsize=9, family="monospace",
                 color="#222", fontweight="bold")
        fig.text(0.40, y, v, fontsize=9, family="monospace", color="#1f4e79")
        y -= 0.026

    fig.text(0.10, 0.16,
             "Reading order — depth-tower diagnostics, basic to advanced.\n"
             "  §A  Data disclosure (Order-3 specific)\n"
             "  §B  Summary headline\n"
             "  §C  Energy tower convergence\n"
             "  §D  Curvature tower convergence\n"
             "  §E  Period-2 attractor (c_even / c_odd)\n"
             "  §F  Attractor amplitude + damping card\n"
             "  §G  IR classification card\n"
             "  §H  Energy / curvature cycle detection\n"
             "  §I  M² = I involution proof\n"
             "  §J  Dynamical-depth summary",
             fontsize=9, family="monospace", color="#222")

    _footer3(fig, j, run_id, page_num, total, "cover")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 2 — Data disclosure (Order-3 specific) ────────────────
def p_disclosure(pdf, j, dataset_id, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title3(fig, dataset_id, page_num,
            "§A  Data Disclosure (Order-3 depth-sounder run)", j)
    he = _depth_block(j); summ = he["summary"]; ir = he["impulse_response"]
    inv = he["involution_proof"]; cycle_e = he["energy_cycle"]; cycle_c = he["curvature_cycle"]
    md  = j["metadata"]; eng_cfg = md.get("engine_config", {}) or {}

    lines = []
    lines.append("DEPTH-SOUNDER CONFIGURATION")
    lines.append(f"  noise_floor_omega_var  : {summ.get('noise_floor_omega_var')}")
    lines.append(f"  convergence_precision  : {summ.get('convergence_precision')}")
    lines.append(f"  max_levels             : {summ.get('max_levels')}")
    lines.append("")

    lines.append("TOWER TERMINATION")
    lines.append(f"  energy_termination     : {summ.get('energy_termination')}")
    lines.append(f"  curvature_termination  : {summ.get('curvature_termination')}")
    lines.append("")

    lines.append("ATTRACTOR DETECTION")
    ca = he.get("curvature_attractor", {})
    lines.append(f"  period                 : {ca.get('period')}")
    lines.append(f"  amplitude              : {(ca.get('amplitude') or 0):.6f}")
    lines.append(f"  convergence_level      : {ca.get('convergence_level')}")
    lines.append(f"  contraction_lyapunov   : {(ca.get('contraction_lyapunov') or 0):.6f}")
    lines.append(f"  mean_contraction_ratio : {(ca.get('mean_contraction_ratio') or 0):.6f}")
    lines.append(f"  banach_satisfied       : {ca.get('banach_satisfied')}")
    lines.append(f"  residual               : {(ca.get('residual') or 0):.2e}")
    lines.append("")

    lines.append("CYCLE DETECTION")
    lines.append(f"  energy.detected={cycle_e.get('detected')}  period={cycle_e.get('period')}  "
                 f"residual={(cycle_e.get('residual') or 0):.2e}  conv_level={cycle_e.get('convergence_level')}")
    lines.append(f"  curv.detected ={cycle_c.get('detected')}  period={cycle_c.get('period')}  "
                 f"residual={(cycle_c.get('residual') or 0):.2e}  conv_level={cycle_c.get('convergence_level')}")
    lines.append("")

    lines.append("INVOLUTION PROOF (M^2 = I)")
    lines.append(f"  mean_residual          : {(inv.get('mean_residual') or 0):.2e}")
    lines.append(f"  verified               : {inv.get('verified')}")
    lines.append(f"  n_samples              : {inv.get('n_samples')}")
    lines.append("")

    lines.append("ENGINE CONFIG ACTIVE OVERRIDES")
    overrides = eng_cfg.get("active_overrides", {}) or {}
    if overrides:
        for k, v in overrides.items(): lines.append(f"  {k:<22}: {v}")
    else:
        lines.append("  (none — defaults from cnt.py USER CONFIGURATION)")
    lines.append("")

    lines.append("ENGINE SOURCE FINGERPRINT")
    sig = s2.engine_signature()
    for tag, h in sig["files"].items():
        lines.append(f"  {tag:<22}: {h or 'missing'}")
    lines.append(f"  combined sha256        : {sig['combined']}")

    # Render two columns
    half = len(lines)//2 + 1
    for i, line in enumerate(lines[:half]):
        fig.text(0.04, 0.90 - i*0.022, line, fontsize=8, family="monospace", color="#222")
    for i, line in enumerate(lines[half:]):
        fig.text(0.50, 0.90 - i*0.022, line, fontsize=8, family="monospace", color="#222")

    _footer3(fig, j, run_id, page_num, total, "data disclosure")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 3 — Summary headline ──────────────────────────────────
def p_summary_head(pdf, j, dataset_id, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title3(fig, dataset_id, page_num, "§B  Summary Headline", j)
    he = _depth_block(j); summ = he["summary"]; ir = he["impulse_response"]
    ca = he["curvature_attractor"]

    rows = [
        ("Curvature depth",        summ.get("curvature_depth")),
        ("Curvature termination",  summ.get("curvature_termination")),
        ("Energy depth",           summ.get("energy_depth")),
        ("Energy termination",     summ.get("energy_termination")),
        ("Dynamical depth",        summ.get("dynamical_depth")),
        ("Convergence precision",  summ.get("convergence_precision")),
        ("Noise-floor ω var",      summ.get("noise_floor_omega_var")),
        ("Max levels",             summ.get("max_levels")),
        ("",                       ""),
        ("IR classification",      ir.get("classification")),
        ("Amplitude A",            f"{(ir.get('amplitude_A') or 0):.4f}"),
        ("Depth Δ",                f"{(ir.get('depth_delta') or 0):.4f}"),
        ("Damping ζ",              f"{(ir.get('damping_zeta') or 0):.4f}"),
        ("",                       ""),
        ("Period",                 ca.get("period")),
        ("Amplitude",              f"{(ca.get('amplitude') or 0):.6f}"),
        ("Banach contraction",     ca.get("banach_satisfied")),
        ("Lyapunov",               f"{(ca.get('contraction_lyapunov') or 0):.6f}"),
        ("Residual",               f"{(ca.get('residual') or 0):.2e}"),
    ]
    ax = fig.add_axes([0.10, 0.10, 0.80, 0.78]); ax.axis("off")
    y = 0.95
    for k, v in rows:
        if k:
            ax.text(0.05, y, f"{k:<28}", fontsize=11, family="monospace",
                    color="#222", fontweight="bold", transform=ax.transAxes)
            ax.text(0.55, y, str(v), fontsize=11, family="monospace",
                    color="#1f4e79", transform=ax.transAxes)
        y -= 0.045
    _footer3(fig, j, run_id, page_num, total, "summary headline")
    pdf.savefig(fig); plt.close(fig)


# ── Plate helper: tower convergence panel ───────────────────────
def _draw_tower(ax_hs, ax_om, tower, label, color):
    if not tower: return
    levels = [t["level"] for t in tower]
    hs     = [t.get("hs_mean") for t in tower]
    om     = [t.get("omega_mean") for t in tower]
    ax_hs.plot(levels, hs, "-o", color=color, lw=1.6, ms=4, label=label)
    ax_hs.set_xlabel("level"); ax_hs.set_ylabel("Hs(level)  (mean)")
    ax_hs.grid(True, alpha=0.3)
    ax_om.plot(levels, om, "-s", color=color, lw=1.4, ms=3.5, label=label)
    ax_om.set_xlabel("level"); ax_om.set_ylabel("ω(level)  (mean, deg/step)")
    ax_om.grid(True, alpha=0.3)


def p_energy_tower(pdf, j, dataset_id, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title3(fig, dataset_id, page_num,
            "§C  Energy Tower Convergence", j)
    he = _depth_block(j)
    ax_hs = fig.add_axes([0.08, 0.50, 0.40, 0.36])
    ax_om = fig.add_axes([0.55, 0.50, 0.40, 0.36])
    _draw_tower(ax_hs, ax_om, he.get("energy_tower", []),
                "energy tower", "#1f4e79")
    ax_hs.set_title("Hs per level", fontsize=10, color="#1f4e79")
    ax_om.set_title("ω per level", fontsize=10, color="#1f4e79")

    ax_status = fig.add_axes([0.08, 0.12, 0.84, 0.30]); ax_status.axis("off")
    et = he.get("energy_tower", [])
    summ = he["summary"]
    rows = ["Energy tower (levels): " + str(len(et)),
            f"  termination       : {summ.get('energy_termination')}",
            f"  energy depth      : {summ.get('energy_depth')}",
            f"  energy_hs_traj    : {summ.get('energy_hs_trajectory')}"]
    y = 0.92
    for r in rows:
        ax_status.text(0.02, y, r, fontsize=9, family="monospace", color="#222",
                       transform=ax_status.transAxes); y -= 0.08
    if et:
        ax_status.text(0.02, 0.45, "Per-level status (status / D / T / helmsman):",
                       fontsize=9, family="monospace", color="#444",
                       transform=ax_status.transAxes)
        y = 0.38
        for k, lv in enumerate(et[:8]):
            ax_status.text(0.02, y,
                f"  L{lv['level']:>2}  status={lv['status']:<14}  "
                f"T={lv['T']:<5}  D={lv['D']:<3}  helm={(lv.get('helmsman') or '-')}",
                fontsize=8, family="monospace", color="#222",
                transform=ax_status.transAxes); y -= 0.08
        if len(et) > 8:
            ax_status.text(0.02, y, f"  …  ({len(et)-8} more levels)",
                fontsize=8, family="monospace", color="#888",
                transform=ax_status.transAxes)
    _footer3(fig, j, run_id, page_num, total, "energy tower")
    pdf.savefig(fig); plt.close(fig)


def p_curvature_tower(pdf, j, dataset_id, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title3(fig, dataset_id, page_num,
            "§D  Curvature Tower Convergence", j)
    he = _depth_block(j)
    ax_hs = fig.add_axes([0.08, 0.50, 0.40, 0.36])
    ax_om = fig.add_axes([0.55, 0.50, 0.40, 0.36])
    _draw_tower(ax_hs, ax_om, he.get("curvature_tower", []),
                "curvature tower", "#d62728")
    ax_hs.set_title("Hs per level", fontsize=10, color="#1f4e79")
    ax_om.set_title("ω per level", fontsize=10, color="#1f4e79")

    ax_status = fig.add_axes([0.08, 0.12, 0.84, 0.30]); ax_status.axis("off")
    ct = he.get("curvature_tower", [])
    summ = he["summary"]
    rows = ["Curvature tower (levels): " + str(len(ct)),
            f"  termination       : {summ.get('curvature_termination')}",
            f"  curvature depth   : {summ.get('curvature_depth')}",
            f"  curvature_hs_traj : {summ.get('curvature_hs_trajectory')}"]
    y = 0.92
    for r in rows:
        ax_status.text(0.02, y, r, fontsize=9, family="monospace", color="#222",
                       transform=ax_status.transAxes); y -= 0.08
    if ct:
        ax_status.text(0.02, 0.45, "Per-level status (status / D / T / helmsman):",
                       fontsize=9, family="monospace", color="#444",
                       transform=ax_status.transAxes)
        y = 0.38
        for k, lv in enumerate(ct[:8]):
            ax_status.text(0.02, y,
                f"  L{lv['level']:>2}  status={lv['status']:<14}  "
                f"T={lv['T']:<5}  D={lv['D']:<3}  helm={(lv.get('helmsman') or '-')}",
                fontsize=8, family="monospace", color="#222",
                transform=ax_status.transAxes); y -= 0.08
        if len(ct) > 8:
            ax_status.text(0.02, y, f"  …  ({len(ct)-8} more levels)",
                fontsize=8, family="monospace", color="#888",
                transform=ax_status.transAxes)
    _footer3(fig, j, run_id, page_num, total, "curvature tower")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — Period-2 attractor (c_even / c_odd) ──────────────────
def p_attractor(pdf, j, dataset_id, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title3(fig, dataset_id, page_num,
            "§E  Period-2 Attractor (c_even / c_odd)", j)
    he = _depth_block(j); ca = he["curvature_attractor"]
    inp = j["input"]; carriers = inp["carriers"]; D = inp["n_carriers"]

    c_even = ca.get("c_even")
    c_odd  = ca.get("c_odd")
    period = ca.get("period")
    amp    = ca.get("amplitude") or 0.0

    # c_even / c_odd are scalar Hs values at the alternating attractor
    # samples, not full compositions. Display as a two-bar Hs comparison
    # with the amplitude band overlay.
    if (isinstance(c_even, (int, float)) and isinstance(c_odd, (int, float))
        and period == 2):
        ax = fig.add_axes([0.10, 0.20, 0.55, 0.65])
        labels = ["c_even (Hs)", "c_odd (Hs)"]
        vals   = [c_even, c_odd]
        cols   = ["#1f4e79", "#d62728"]
        bars = ax.bar(labels, vals, color=cols, edgecolor="black",
                      linewidth=0.6, width=0.55)
        for b, v in zip(bars, vals):
            ax.text(b.get_x()+b.get_width()/2, v, f"{v:.4f}",
                    ha="center", va="bottom", fontsize=10, fontweight="bold")
        lo, hi = min(c_even, c_odd), max(c_even, c_odd)
        ax.fill_between([-0.5, 1.5], lo, hi, color="#ffb74d", alpha=0.25,
                        label=f"amplitude |Delta| = {amp:.4f}")
        ax.set_ylabel("Hs at attractor sample (nats)")
        ax.set_title("Period-2 attractor — even / odd Hs samples",
                     fontsize=10, color="#1f4e79", loc="left")
        ax.legend(loc="upper right"); ax.grid(True, axis="y", alpha=0.3)
        info = [
            f"period       = {period}",
            f"c_even (Hs)  = {c_even:.6f}",
            f"c_odd  (Hs)  = {c_odd:.6f}",
            f"|Delta| = amplitude A = {amp:.6f}",
            "",
            f"convergence_level     = {ca.get('convergence_level')}",
            f"contraction_lyapunov  = {(ca.get('contraction_lyapunov') or 0):.6f}",
            f"mean_contraction_ratio= {(ca.get('mean_contraction_ratio') or 0):.6f}",
            f"banach_satisfied      = {ca.get('banach_satisfied')}",
            f"residual              = {(ca.get('residual') or 0):.2e}",
            "",
            "c_even / c_odd are the alternating Hs samples once",
            "the depth tower has converged on a period-2 attractor.",
            "Their gap is the attractor amplitude A.",
        ]
        fig.text(0.70, 0.84, "\n".join(info), fontsize=8, family="monospace",
                 color="#222", verticalalignment="top")
    else:
        fig.text(0.5, 0.5,
                 "No period-2 attractor recorded.\n"
                 f"period = {ca.get('period')}, "
                 f"amplitude = {amp:.4f}",
                 ha="center", fontsize=12, color="#444")
    _footer3(fig, j, run_id, page_num, total, "attractor c_even/c_odd")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — Amplitude + damping card ──────────────────────────────
def p_amplitude_damping(pdf, j, dataset_id, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title3(fig, dataset_id, page_num,
            "§F  Attractor Amplitude + Damping (impulse-response card)", j)
    he = _depth_block(j); ir = he["impulse_response"]
    A = ir.get("amplitude_A") or 0.0
    delta = ir.get("depth_delta") or 0.0
    zeta  = ir.get("damping_zeta") or 0.0
    cls   = ir.get("classification") or "?"

    # Big-number display
    fig.text(0.06, 0.78, "A (amplitude)",   fontsize=11, color="#444")
    fig.text(0.06, 0.70, f"{A:.4f}",        fontsize=36, color="#1f4e79", fontweight="bold")
    fig.text(0.36, 0.78, "ζ (damping)",     fontsize=11, color="#444")
    fig.text(0.36, 0.70, f"{zeta:.4f}",     fontsize=36, color="#d62728", fontweight="bold")
    fig.text(0.66, 0.78, "Δ (depth)",       fontsize=11, color="#444")
    fig.text(0.66, 0.70, f"{delta:.4f}",    fontsize=36, color="#2ca02c", fontweight="bold")

    fig.text(0.06, 0.58, f"Classification:  {cls}",
             fontsize=14, fontweight="bold", color="#1f4e79")

    # Reference scale strip on amplitude
    ax = fig.add_axes([0.08, 0.32, 0.84, 0.16])
    bands = [
        (0.000, 0.01,  "#2ca02c",  "CRITICALLY_DAMPED"),
        (0.01,  0.05,  "#bcbd22",  "LIGHTLY_DAMPED"),
        (0.05,  0.20,  "#ff7f0e",  "MODERATELY_DAMPED"),
        (0.20,  1.00,  "#d62728",  "OVERDAMPED_EXTREME"),
    ]
    Amax = max(0.30, A * 1.3)
    for lo, hi, col, lab in bands:
        if lo > Amax: continue
        ax.axvspan(lo, min(hi, Amax), color=col, alpha=0.25)
        ax.text((lo + min(hi, Amax))/2, 0.5, lab, ha="center", va="center",
                fontsize=8, color="#222", fontweight="bold", rotation=0)
    ax.axvline(A, color="black", lw=2.0, label=f"this run A = {A:.4f}")
    ax.set_xlim(0, Amax); ax.set_ylim(0, 1)
    ax.set_yticks([]); ax.set_xlabel("amplitude A")
    ax.legend(loc="upper right")
    ax.set_title("Reference amplitude band (for IR taxonomy)",
                 fontsize=10, color="#1f4e79", loc="left")

    _footer3(fig, j, run_id, page_num, total, "amplitude + damping card")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — IR classification card ───────────────────────────────
_IR_DESC = {
    "CRITICALLY_DAMPED": "Tight period-2 attractor at small amplitude. The recursion compresses to a narrow attractor band. System is well-bounded.",
    "LIGHTLY_DAMPED":    "Period-2 attractor at moderate amplitude. Visible amplitude in the limit cycle but well-controlled.",
    "MODERATELY_DAMPED": "Period-2 attractor with substantial amplitude. Significant compositional structure across records.",
    "OVERDAMPED_EXTREME":"Period-2 attractor at very high amplitude. Large directional swings — frequently a signature of carrier phase-out.",
    "UNDAMPED":          "No clear damping detected. Persistent oscillation amplitude.",
    "ENERGY_STABLE_FIXED_POINT":"Energy tower converges to a stable period-1 fixed point.",
    "CURVATURE_VERTEX_FLAT":    "Curvature recursion flattened against a vertex of the simplex due to single-carrier dominance > 60%.",
    "D2_DEGENERATE":            "D = 2: simplex has a single independent compositional axis. Depth tower cannot exercise off-diagonal metric structure.",
}

def p_ir_classification(pdf, j, dataset_id, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title3(fig, dataset_id, page_num,
            "§G  IR Classification — seven-class taxonomy", j)
    he = _depth_block(j); ir = he["impulse_response"]
    cls = ir.get("classification") or "?"

    fig.text(0.5, 0.86, f"This run: {cls}",
             ha="center", fontsize=18, fontweight="bold", color="#1f4e79")

    # All seven classes with descriptions
    y = 0.78
    for k, v in _IR_DESC.items():
        is_self = (k == cls)
        col = "#1f4e79" if is_self else "#444"
        bg  = "#e6f1ff" if is_self else "white"
        # Background highlight
        fig.add_artist(plt.Rectangle((0.06, y - 0.045), 0.88, 0.055,
                                     facecolor=bg, edgecolor="#cccccc",
                                     linewidth=0.5,
                                     transform=fig.transFigure))
        fig.text(0.08, y - 0.005, k, fontsize=10,
                 fontweight=("bold" if is_self else "normal"), color=col)
        fig.text(0.32, y - 0.005, v, fontsize=8.5, color="#222",
                 wrap=True)
        y -= 0.075

    fig.text(0.06, 0.06,
             "All eight IR classes are encoded in the engine's classify_impulse_response() function. "
             "The current run's class is highlighted above; each class has different downstream "
             "implications for trajectory interpretation and dynamics.",
             fontsize=8, family="monospace", color="#666", wrap=True)

    _footer3(fig, j, run_id, page_num, total, "IR classification card")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — Energy / curvature cycle detection ─────────────────
def p_cycle_detection(pdf, j, dataset_id, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title3(fig, dataset_id, page_num,
            "§H  Energy / Curvature Cycle Detection", j)
    he = _depth_block(j)
    ec = he["energy_cycle"]; cc = he["curvature_cycle"]
    summ = he["summary"]

    rows = [
        ("",                       "Energy",              "Curvature"),
        ("detected",               ec.get("detected"),    cc.get("detected")),
        ("period",                 ec.get("period"),      cc.get("period")),
        ("residual",               f"{(ec.get('residual') or 0):.2e}",
                                   f"{(cc.get('residual') or 0):.2e}"),
        ("convergence_level",      ec.get("convergence_level"),
                                   cc.get("convergence_level")),
        ("",                       "",                    ""),
        ("tower depth",            summ.get("energy_depth"),
                                   summ.get("curvature_depth")),
        ("termination reason",     summ.get("energy_termination"),
                                   summ.get("curvature_termination")),
    ]
    ax = fig.add_axes([0.08, 0.20, 0.84, 0.65]); ax.axis("off")
    y = 0.95
    for k, a, b in rows:
        if k:
            ax.text(0.05, y, k, fontsize=11, family="monospace",
                    color="#222", fontweight="bold" if k=="" else "normal",
                    transform=ax.transAxes)
            ax.text(0.45, y, str(a), fontsize=11, family="monospace",
                    color="#1f4e79", transform=ax.transAxes)
            ax.text(0.75, y, str(b), fontsize=11, family="monospace",
                    color="#d62728", transform=ax.transAxes)
        y -= 0.090
    fig.text(0.5, 0.10,
             "Cycle detection compares trajectories at successive depth-tower levels. "
             "A 'detected' cycle of period 2 with low residual ⇒ converged period-2 attractor.",
             ha="center", fontsize=8, color="#666", wrap=True)
    _footer3(fig, j, run_id, page_num, total, "cycle detection")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — M^2 = I involution proof ────────────────────────────
def p_involution(pdf, j, dataset_id, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title3(fig, dataset_id, page_num,
            "§I  Involution Proof  M² = I  (metric duality)", j)
    he = _depth_block(j); inv = he["involution_proof"]
    samples = inv.get("samples") or []
    mean_r  = inv.get("mean_residual") or 0.0
    verified = inv.get("verified")
    n = inv.get("n_samples") or len(samples)

    ax = fig.add_axes([0.10, 0.30, 0.55, 0.55])
    if samples:
        residuals = [s.get("residual", 0.0) if isinstance(s, dict) else s
                     for s in samples]
        ax.hist(residuals, bins=30, color="#1f4e79", edgecolor="white")
        ax.set_xlabel("|M²(x) − x|  residual"); ax.set_ylabel("count")
    ax.set_title(f"Residual distribution over {n} samples", fontsize=10, color="#1f4e79", loc="left")
    ax.grid(True, axis="y", alpha=0.3)

    fig.text(0.70, 0.70, "Headline:", fontsize=11, fontweight="bold", color="#1f4e79")
    fig.text(0.70, 0.65, f"mean residual = {mean_r:.2e}",
             fontsize=12, family="monospace", color="#222")
    fig.text(0.70, 0.60, f"verified = {verified}",
             fontsize=12, family="monospace",
             color=("#2ca02c" if verified else "#d62728"), fontweight="bold")
    fig.text(0.70, 0.55, f"n_samples = {n}",
             fontsize=12, family="monospace", color="#222")
    fig.text(0.70, 0.45,
             "M² = I is the metric-dual involution required for the\n"
             "depth sounder to be Banach-contractive. Mean residual\n"
             "near IEEE floor (~1e-15 typical) is the strong proof.",
             fontsize=8, family="monospace", color="#444")

    _footer3(fig, j, run_id, page_num, total, "involution proof")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — Dynamical-depth summary ────────────────────────────
def p_dyn_depth_summary(pdf, j, dataset_id, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title3(fig, dataset_id, page_num, "§J  Dynamical-Depth Summary", j)
    he = _depth_block(j); summ = he["summary"]

    # Two-bar chart: energy vs curvature depth
    ax = fig.add_axes([0.10, 0.30, 0.40, 0.55])
    energies = ["energy_depth", "curvature_depth", "dynamical_depth"]
    vals = [summ.get(k) or 0 for k in energies]
    cols = ["#1f4e79", "#d62728", "#2ca02c"]
    ax.bar(range(3), vals, color=cols, edgecolor="black", linewidth=0.5)
    ax.set_xticks(range(3)); ax.set_xticklabels(energies, rotation=15, ha="right", fontsize=9)
    ax.set_ylabel("depth (levels)")
    ax.set_title("Tower depth comparison", fontsize=10, color="#1f4e79", loc="left")
    for i, v in enumerate(vals):
        ax.text(i, v, str(v), ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.grid(True, axis="y", alpha=0.3)

    # Convergence trajectories
    ax2 = fig.add_axes([0.55, 0.30, 0.40, 0.55])
    eh = summ.get("energy_hs_trajectory") or []
    ch = summ.get("curvature_hs_trajectory") or []
    if eh:
        ax2.plot(range(len(eh)), eh, "-o", color="#1f4e79", lw=1.4, ms=3.5, label="energy")
    if ch:
        ax2.plot(range(len(ch)), ch, "-s", color="#d62728", lw=1.4, ms=3.5, label="curvature")
    ax2.set_xlabel("level"); ax2.set_ylabel("Hs(level)")
    ax2.set_title("Hs convergence per tower", fontsize=10, color="#1f4e79", loc="left")
    ax2.legend(); ax2.grid(True, alpha=0.3)

    fig.text(0.10, 0.20,
        f"mean_duality_distance  : {summ.get('mean_duality_distance')}",
        fontsize=9, family="monospace", color="#222")
    fig.text(0.10, 0.16,
        f"convergence_precision  : {summ.get('convergence_precision')}",
        fontsize=9, family="monospace", color="#222")
    fig.text(0.10, 0.12,
        f"noise_floor_omega_var  : {summ.get('noise_floor_omega_var')}",
        fontsize=9, family="monospace", color="#222")
    _footer3(fig, j, run_id, page_num, total, "dynamical depth summary")
    pdf.savefig(fig); plt.close(fig)


PLATES = [p_cover, p_disclosure, p_summary_head,
          p_energy_tower, p_curvature_tower, p_attractor,
          p_amplitude_damping, p_ir_classification, p_cycle_detection,
          p_involution, p_dyn_depth_summary]


def render_stage3(pdf, j, dataset_id, run_id, options=None):
    """Render the Stage 3 paged report.

    options : currently unused (reserved for future Order-3 knobs)."""
    total = len(PLATES)
    for k, fn in enumerate(PLATES, 1):
        fn(pdf, j, dataset_id, run_id, k, total)
    return total
