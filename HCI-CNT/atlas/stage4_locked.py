#!/usr/bin/env python3
"""
HCI-Atlas Stage 4 — Order-4+ paged module (cross-dataset / EITT / inference).

Group-level: spans MULTIPLE datasets within a project. Reads each member
JSON's depth + diagnostics blocks and produces one comparison report per
project.

Doctrine: Order 4+ = inference / cross-dataset. The plates here only
make sense when comparing two or more datasets sharing the same
analytic frame.

Reading order:
  1. Cover (auto-titled "Compositional system inference for, <project>")
  2. Data disclosure (group-level)
  3. Per-dataset summary table
  4. Cross-dataset attractor amplitude A
  5. Cross-dataset depth comparison (energy / curvature)
  6. Cross-dataset IR-class distribution
  7. EITT residuals comparison (where present)
  8. Cross-dataset Hs / norm range comparison
  9. Cross-dataset ω statistics
 10. Convergence-quality matrix
 11. Inference summary
"""
from __future__ import annotations
import math, json
import numpy as np
import matplotlib.pyplot as plt

from . import stage2_locked as s2  # type: ignore

PAGE_SIZE = (11.0, 8.5)
PDF_DPI   = 150


def _palette(n):
    base = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd",
            "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"]
    return [base[i % len(base)] for i in range(n)]


def _title4(fig, project_id, plate_no, plate_name, ctx):
    fig.text(0.5, 0.972,
        f"Compositional system inference for, {project_id}",
        ha="center", fontsize=11, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.952, f"Plate {plate_no}  |  {plate_name}",
             ha="center", fontsize=9, color="#444", fontstyle="italic")
    fig.text(0.5, 0.935,
        f"{len(ctx['members'])} datasets  |  Engine {ctx.get('engine_version','?')}  |  "
        f"Schema {ctx.get('schema_version','?')}  |  Order 4+",
        ha="center", fontsize=8, color="#666")


def _footer4(fig, ctx, run_id, page_num, total, method=""):
    eng_sig = s2.engine_signature()["short"]
    eng_v   = ctx.get("engine_version", "?")
    fig.text(0.5, 0.025,
        f"engine: {eng_v}  ({eng_sig}…)  |  members: {len(ctx['members'])}  "
        f"|  group_sha: {ctx['group_sha'][:12]}…",
        ha="center", fontsize=7, family="monospace", color="#666")
    fig.text(0.5, 0.010,
        f"{s2._today_iso()}  |  run: {run_id or 'unsaved'}  |  "
        f"page {page_num}/{total}  |  STAGE 4 (Order 4+)  |  {method}",
        ha="center", fontsize=7, family="monospace", color="#888")


# ─── Build aggregate context across multiple datasets ─────────────
def collect_group(members: list, jsons: list, project_id: str) -> dict:
    """Aggregate per-dataset metrics into a group context.

    members : list of dataset_ids (in display order)
    jsons   : list of CNT JSON dicts in the same order
    """
    import hashlib
    rows = []
    group_h = hashlib.sha256()
    for did, j in zip(members, jsons):
        di = j["diagnostics"]
        he = j["depth"]["higgins_extensions"]
        ir = he["impulse_response"]; ca = he["curvature_attractor"]
        summ = he["summary"]; inv = he["involution_proof"]
        eitt = di.get("higgins_extensions", {}).get("eitt_residuals", {}) or {}
        ts = j["tensor"]["timesteps"]
        hs_vals = [t["coda_standard"]["shannon_entropy"] for t in ts]
        norm_vals = [t["coda_standard"]["aitchison_norm"] for t in ts]
        ml = j["stages"]["stage1"]["higgins_extensions"]["metric_ledger"]
        omega_vals = [m.get("omega_deg", 0.0) for m in ml[1:]]
        sha = (di.get("content_sha256") or "?")
        group_h.update(sha.encode())
        rows.append({
            "dataset_id":      did,
            "n_records":       j["input"]["n_records"],
            "n_carriers":      j["input"]["n_carriers"],
            "ir_class":        ir.get("classification"),
            "amplitude_A":     ir.get("amplitude_A") or 0.0,
            "damping_zeta":    ir.get("damping_zeta") or 0.0,
            "depth_delta":     ir.get("depth_delta") or 0.0,
            "energy_depth":    summ.get("energy_depth"),
            "curvature_depth": summ.get("curvature_depth"),
            "dyn_depth":       summ.get("dynamical_depth"),
            "energy_term":     summ.get("energy_termination"),
            "curv_term":       summ.get("curvature_termination"),
            "period":          ca.get("period"),
            "lyapunov":        ca.get("contraction_lyapunov") or 0.0,
            "banach":          ca.get("banach_satisfied"),
            "ca_residual":     ca.get("residual") or 0.0,
            "inv_mean_res":    inv.get("mean_residual") or 0.0,
            "inv_verified":    inv.get("verified"),
            "hs_min":          float(min(hs_vals)) if hs_vals else 0.0,
            "hs_max":          float(max(hs_vals)) if hs_vals else 0.0,
            "hs_mean":         float(np.mean(hs_vals)) if hs_vals else 0.0,
            "norm_min":        float(min(norm_vals)) if norm_vals else 0.0,
            "norm_max":        float(max(norm_vals)) if norm_vals else 0.0,
            "norm_mean":       float(np.mean(norm_vals)) if norm_vals else 0.0,
            "omega_max":       float(max(omega_vals)) if omega_vals else 0.0,
            "omega_mean":      float(np.mean(omega_vals)) if omega_vals else 0.0,
            "eitt":            eitt,
            "content_sha256":  sha,
            "name":            s2._dataset_friendly(did, j),
            "year_range":      s2._year_range(j),
        })
    md0 = jsons[0]["metadata"]
    return {
        "project_id":     project_id,
        "members":        members,
        "rows":           rows,
        "engine_version": md0.get("engine_version"),
        "schema_version": md0.get("schema_version"),
        "group_sha":      group_h.hexdigest(),
    }


# ── PLATE 1 — Cover ──────────────────────────────────────────────
def p_cover(pdf, ctx, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    sig = s2.engine_signature()
    fig.text(0.5, 0.88, "Compositional system",
        ha="center", fontsize=22, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.83, "inference for,",
        ha="center", fontsize=14, color="#444", fontstyle="italic")
    fig.text(0.5, 0.77, ctx["project_id"],
        ha="center", fontsize=18, fontweight="bold", color="#222")
    fig.text(0.5, 0.73, f"{len(ctx['members'])} member datasets",
        ha="center", fontsize=12, color="#222")

    rows = [
        ("Generated",      s2._today_iso()),
        ("Run ID",         run_id or "unsaved"),
        ("Project ID",     ctx["project_id"]),
        ("Members",        ", ".join(ctx["members"][:6])
                          + (" …" if len(ctx["members"])>6 else "")),
        ("Engine version", ctx["engine_version"]),
        ("Schema version", ctx["schema_version"]),
        ("Engine signature", sig["combined"][:32] + "…"),
        ("Group SHA-256",    ctx["group_sha"][:32] + "…"),
    ]
    y = 0.62
    for k, v in rows:
        fig.text(0.10, y, f"{k:<24}", fontsize=9, family="monospace",
                 color="#222", fontweight="bold")
        fig.text(0.36, y, v, fontsize=9, family="monospace", color="#1f4e79")
        y -= 0.028

    fig.text(0.10, 0.32,
        "Reading order — cross-dataset inference, basic to advanced.\n"
        "  §A  Group disclosure\n"
        "  §B  Per-dataset summary table\n"
        "  §C  Cross-dataset attractor amplitude A\n"
        "  §D  Cross-dataset depth comparison\n"
        "  §E  IR-class distribution\n"
        "  §F  EITT residuals comparison\n"
        "  §G  Cross-dataset Hs / Aitchison-norm ranges\n"
        "  §H  Cross-dataset ω statistics\n"
        "  §I  Convergence-quality matrix\n"
        "  §J  Inference summary",
        fontsize=9, family="monospace", color="#222")
    _footer4(fig, ctx, run_id, page_num, total, "cover")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 2 — Group disclosure ───────────────────────────────────
def p_disclosure(pdf, ctx, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title4(fig, ctx["project_id"], page_num,
            "§A  Group Disclosure", ctx)

    sig = s2.engine_signature()
    lines = []
    lines.append("PROJECT")
    lines.append(f"  project_id     : {ctx['project_id']}")
    lines.append(f"  n_members      : {len(ctx['members'])}")
    lines.append(f"  engine_version : {ctx['engine_version']}")
    lines.append(f"  schema_version : {ctx['schema_version']}")
    lines.append(f"  group sha      : {ctx['group_sha']}")
    lines.append("")
    lines.append("MEMBER DATASETS")
    for r in ctx["rows"]:
        lines.append(f"  {r['dataset_id']:<28}  T={r['n_records']:<5}  "
                     f"D={r['n_carriers']:<3}  IR={r['ir_class']:<22}  "
                     f"sha={r['content_sha256'][:12]}…")
    lines.append("")
    lines.append("ENGINE SOURCE FINGERPRINT")
    for tag, h in sig["files"].items():
        lines.append(f"  {tag:<22}: {h or 'missing'}")
    lines.append(f"  combined sha256       : {sig['combined']}")
    lines.append("")
    lines.append("SANITY")
    schemas = {r['content_sha256'][:8] for r in ctx["rows"]}
    lines.append(f"  unique content_sha256 prefixes : {len(schemas)} of {len(ctx['rows'])}")
    eng_versions = set()
    lines.append(f"  members all at engine {ctx['engine_version']} : "
                 f"(group field, individual checked at JSON load)")

    half = len(lines)//2 + 1
    for i, line in enumerate(lines[:half]):
        fig.text(0.04, 0.90 - i*0.020, line, fontsize=8, family="monospace", color="#222")
    for i, line in enumerate(lines[half:]):
        fig.text(0.50, 0.90 - i*0.020, line, fontsize=8, family="monospace", color="#222")
    _footer4(fig, ctx, run_id, page_num, total, "group disclosure")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 3 — Per-dataset summary table ──────────────────────────
def p_summary_table(pdf, ctx, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title4(fig, ctx["project_id"], page_num,
            "§B  Per-Dataset Summary Table", ctx)
    rows = ctx["rows"]
    headers = ["dataset", "T", "D", "IR class", "A",  "ζ",  "E.dep", "C.dep", "period", "Banach"]
    ax = fig.add_axes([0.04, 0.10, 0.92, 0.80]); ax.axis("off")
    # Header
    cols_x = [0.02, 0.22, 0.27, 0.33, 0.55, 0.62, 0.69, 0.76, 0.83, 0.92]
    for i, h in enumerate(headers):
        ax.text(cols_x[i], 0.96, h, fontsize=9, fontweight="bold",
                color="#1f4e79", transform=ax.transAxes)
    # Rows
    y = 0.92
    for r in rows[:18]:
        for i, v in enumerate([
            r["dataset_id"][:18], r["n_records"], r["n_carriers"],
            (r["ir_class"] or "?")[:20],
            f"{r['amplitude_A']:.4f}", f"{r['damping_zeta']:.3f}",
            r["energy_depth"], r["curvature_depth"], r["period"], str(r["banach"])
        ]):
            ax.text(cols_x[i], y, str(v), fontsize=8, family="monospace",
                    color="#222", transform=ax.transAxes)
        y -= 0.045
    if len(rows) > 18:
        ax.text(0.5, y - 0.02, f"… ({len(rows)-18} more datasets)",
                fontsize=8, color="#888", transform=ax.transAxes,
                ha="center", fontstyle="italic")
    _footer4(fig, ctx, run_id, page_num, total, "summary table")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — Cross-dataset attractor amplitude A ─────────────────
def p_amplitude_compare(pdf, ctx, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title4(fig, ctx["project_id"], page_num,
            "§C  Cross-Dataset Attractor Amplitude A", ctx)
    rows = ctx["rows"]
    names = [r["dataset_id"] for r in rows]
    A     = [r["amplitude_A"] for r in rows]
    pal   = _palette(len(rows))

    ax = fig.add_axes([0.10, 0.30, 0.84, 0.55])
    bars = ax.bar(range(len(rows)), A, color=pal, edgecolor="black", linewidth=0.4)
    for b, v in zip(bars, A):
        ax.text(b.get_x()+b.get_width()/2, v, f"{v:.4f}",
                ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("amplitude A")
    ax.grid(True, axis="y", alpha=0.3)
    ax.set_title("Period-2 attractor amplitude per dataset",
                 fontsize=10, color="#1f4e79", loc="left")

    # Reference IR bands
    bands = [
        (0.000, 0.01,  "#2ca02c",  "CRITICALLY"),
        (0.01,  0.05,  "#bcbd22",  "LIGHTLY"),
        (0.05,  0.20,  "#ff7f0e",  "MODERATELY"),
        (0.20,  1.00,  "#d62728",  "OVERDAMPED"),
    ]
    Amax = max(A) * 1.3 if A else 1.0
    for lo, hi, col, lab in bands:
        if lo > Amax: continue
        ax.axhspan(lo, min(hi, Amax), color=col, alpha=0.10)

    fig.text(0.10, 0.18,
        "Background colour bands: green=CRITICALLY (A<0.01), olive=LIGHTLY (0.01-0.05), "
        "orange=MODERATELY (0.05-0.20), red=OVERDAMPED (>0.20).",
        fontsize=8, color="#444", wrap=True)
    _footer4(fig, ctx, run_id, page_num, total, "amplitude comparison")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — Cross-dataset depth comparison ───────────────────────
def p_depth_compare(pdf, ctx, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title4(fig, ctx["project_id"], page_num,
            "§D  Cross-Dataset Depth Comparison", ctx)
    rows = ctx["rows"]
    names = [r["dataset_id"] for r in rows]
    e_dep = [r["energy_depth"] or 0 for r in rows]
    c_dep = [r["curvature_depth"] or 0 for r in rows]
    d_dep = [r["dyn_depth"] or 0 for r in rows]

    ax = fig.add_axes([0.08, 0.20, 0.86, 0.65])
    x = np.arange(len(rows))
    w = 0.27
    ax.bar(x - w, e_dep, w, color="#1f4e79", label="energy", edgecolor="black", linewidth=0.4)
    ax.bar(x,     c_dep, w, color="#d62728", label="curvature", edgecolor="black", linewidth=0.4)
    ax.bar(x + w, d_dep, w, color="#2ca02c", label="dynamical", edgecolor="black", linewidth=0.4)
    ax.set_xticks(x); ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("depth (levels)")
    ax.legend(loc="upper right")
    ax.grid(True, axis="y", alpha=0.3)
    ax.set_title("Depth-tower convergence: energy / curvature / dynamical",
                 fontsize=10, color="#1f4e79", loc="left")
    _footer4(fig, ctx, run_id, page_num, total, "depth comparison")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — IR-class distribution ────────────────────────────────
def p_ir_distribution(pdf, ctx, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title4(fig, ctx["project_id"], page_num,
            "§E  IR-Class Distribution Across Members", ctx)
    rows = ctx["rows"]
    counts = {}
    for r in rows:
        c = r["ir_class"] or "?"
        counts[c] = counts.get(c, 0) + 1
    classes = sorted(counts.keys(), key=lambda c: -counts[c])
    vals = [counts[c] for c in classes]
    pal = _palette(len(classes))

    ax = fig.add_axes([0.20, 0.28, 0.60, 0.55])
    ax.barh(range(len(classes)), vals, color=pal, edgecolor="black", linewidth=0.4)
    for i, v in enumerate(vals):
        ax.text(v + 0.05, i, str(v), va="center", fontsize=10, fontweight="bold")
    ax.set_yticks(range(len(classes))); ax.set_yticklabels(classes, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("# datasets")
    ax.grid(True, axis="x", alpha=0.3)
    ax.set_title("IR-class membership across the project",
                 fontsize=10, color="#1f4e79", loc="left")
    fig.text(0.10, 0.16,
        "If most members fall in one IR class, the project shows a "
        "consistent dynamical regime; high IR-class diversity means "
        "the comparison is bridging different attractor families.",
        fontsize=9, color="#444", wrap=True)
    _footer4(fig, ctx, run_id, page_num, total, "IR class distribution")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — EITT residuals comparison ────────────────────────────
def p_eitt_compare(pdf, ctx, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title4(fig, ctx["project_id"], page_num,
            "§F  EITT Residuals Comparison (where present)", ctx)
    rows = ctx["rows"]

    has_eitt = [r for r in rows if r.get("eitt")]
    if not has_eitt:
        fig.text(0.5, 0.5, "No EITT residuals recorded for any member.",
                 ha="center", fontsize=12, color="#444")
        _footer4(fig, ctx, run_id, page_num, total, "eitt (none)")
        pdf.savefig(fig); plt.close(fig); return

    # Try to find a common numeric key; fallback to first numeric entry
    first = has_eitt[0]["eitt"]
    keys = [k for k, v in first.items() if isinstance(v, (int, float))]
    if not keys:
        fig.text(0.5, 0.5,
                 f"EITT residuals present but no scalar fields. Keys: {list(first.keys())}",
                 ha="center", fontsize=10, color="#d62728")
        _footer4(fig, ctx, run_id, page_num, total, "eitt (non-scalar)")
        pdf.savefig(fig); plt.close(fig); return

    key = keys[0]
    names = [r["dataset_id"] for r in has_eitt]
    vals = [r["eitt"].get(key, 0.0) for r in has_eitt]
    ax = fig.add_axes([0.10, 0.28, 0.84, 0.60])
    ax.bar(range(len(names)), vals,
           color="#1f4e79", edgecolor="black", linewidth=0.4)
    ax.set_xticks(range(len(names))); ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel(key)
    ax.set_title(f"EITT residual key: {key}  (datasets without recorded value omitted)",
                 fontsize=10, color="#1f4e79", loc="left")
    ax.grid(True, axis="y", alpha=0.3)

    fig.text(0.10, 0.18,
        f"Shown: '{key}' from diagnostics.higgins_extensions.eitt_residuals. "
        f"Datasets without an EITT record: "
        f"{', '.join(r['dataset_id'] for r in rows if not r.get('eitt')) or '(none)'}.",
        fontsize=8, color="#444", wrap=True)
    _footer4(fig, ctx, run_id, page_num, total, f"eitt({key})")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — Hs / norm range comparison ───────────────────────────
def p_hs_norm_ranges(pdf, ctx, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title4(fig, ctx["project_id"], page_num,
            "§G  Hs / Aitchison-Norm Ranges", ctx)
    rows = ctx["rows"]
    names = [r["dataset_id"] for r in rows]

    ax_hs = fig.add_axes([0.08, 0.50, 0.86, 0.36])
    for i, r in enumerate(rows):
        ax_hs.plot([i, i], [r["hs_min"], r["hs_max"]],
                   color="#1f4e79", lw=4, alpha=0.7)
        ax_hs.plot([i], [r["hs_mean"]], "o", color="black", markersize=5)
    ax_hs.set_xticks(range(len(rows))); ax_hs.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    ax_hs.set_ylabel("Hs (nats)")
    ax_hs.set_title("Hs trajectory range per dataset (• = mean)",
                    fontsize=10, color="#1f4e79", loc="left")
    ax_hs.grid(True, axis="y", alpha=0.3)

    ax_n = fig.add_axes([0.08, 0.10, 0.86, 0.32])
    for i, r in enumerate(rows):
        ax_n.plot([i, i], [r["norm_min"], r["norm_max"]],
                  color="#d62728", lw=4, alpha=0.7)
        ax_n.plot([i], [r["norm_mean"]], "o", color="black", markersize=5)
    ax_n.set_xticks(range(len(rows))); ax_n.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    ax_n.set_ylabel("‖clr‖ (nepers)")
    ax_n.set_title("Aitchison-norm range per dataset",
                   fontsize=10, color="#1f4e79", loc="left")
    ax_n.grid(True, axis="y", alpha=0.3)
    _footer4(fig, ctx, run_id, page_num, total, "hs+norm ranges")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — ω statistics comparison ──────────────────────────────
def p_omega_compare(pdf, ctx, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title4(fig, ctx["project_id"], page_num,
            "§H  ω Statistics Comparison", ctx)
    rows = ctx["rows"]
    names = [r["dataset_id"] for r in rows]
    omax  = [r["omega_max"] for r in rows]
    omean = [r["omega_mean"] for r in rows]

    ax = fig.add_axes([0.08, 0.20, 0.86, 0.65])
    x = np.arange(len(rows))
    w = 0.40
    ax.bar(x - w/2, omean, w, color="#1f4e79", label="mean |ω|", edgecolor="black", linewidth=0.4)
    ax.bar(x + w/2, omax,  w, color="#d62728", label="peak |ω|", edgecolor="black", linewidth=0.4)
    ax.set_xticks(x); ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("|ω|  (deg / step)")
    ax.legend(loc="upper right")
    ax.grid(True, axis="y", alpha=0.3)
    ax.set_title("Inter-step angular velocity per dataset",
                 fontsize=10, color="#1f4e79", loc="left")
    _footer4(fig, ctx, run_id, page_num, total, "omega comparison")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — Convergence-quality matrix ───────────────────────────
def p_convergence_matrix(pdf, ctx, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title4(fig, ctx["project_id"], page_num,
            "§I  Convergence-Quality Matrix", ctx)
    rows = ctx["rows"]
    names = [r["dataset_id"] for r in rows]
    metrics = [
        ("involution res", [r["inv_mean_res"] for r in rows], "log10"),
        ("attractor res",  [r["ca_residual"] for r in rows], "log10"),
        ("Lyapunov",       [r["lyapunov"] for r in rows], "linear"),
        ("damping ζ",      [r["damping_zeta"] for r in rows], "linear"),
    ]
    ax = fig.add_axes([0.18, 0.18, 0.78, 0.68])
    M = []
    for (name, vals, scale) in metrics:
        if scale == "log10":
            row = [math.log10(max(v, 1e-30)) for v in vals]
        else:
            row = list(vals)
        M.append(row)
    M = np.asarray(M)
    im = ax.imshow(M, aspect="auto", cmap="RdYlGn_r")
    ax.set_yticks(range(len(metrics)))
    ax.set_yticklabels([f"{n} ({s})" for n, _, s in metrics], fontsize=9)
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    for i in range(len(metrics)):
        for j in range(len(rows)):
            ax.text(j, i, f"{M[i,j]:.2e}", ha="center", va="center",
                    fontsize=7, color="black")
    plt.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    ax.set_title("Per-dataset convergence diagnostics  "
                 "(log10 for residuals; linear for Lyapunov / ζ)",
                 fontsize=9, color="#1f4e79", loc="left")
    _footer4(fig, ctx, run_id, page_num, total, "convergence matrix")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE — Inference summary ────────────────────────────────────
def p_inference_summary(pdf, ctx, run_id, page_num, total):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title4(fig, ctx["project_id"], page_num,
            "§J  Inference Summary", ctx)
    rows = ctx["rows"]
    A = [r["amplitude_A"] for r in rows]
    e_dep = [r["energy_depth"] or 0 for r in rows]
    c_dep = [r["curvature_depth"] or 0 for r in rows]

    headlines = [
        f"Project           : {ctx['project_id']}",
        f"Members           : {len(rows)}",
        f"Engine            : {ctx['engine_version']}  (sig {s2.engine_signature()['short']})",
        "",
        f"Amplitude A range : {min(A):.4f}  …  {max(A):.4f}",
        f"Amplitude A mean  : {np.mean(A):.4f}",
        f"Energy depth   sum: {sum(e_dep)}    mean: {np.mean(e_dep):.1f}    max: {max(e_dep)}",
        f"Curv.  depth   sum: {sum(c_dep)}    mean: {np.mean(c_dep):.1f}    max: {max(c_dep)}",
        "",
        "IR class composition:",
    ]
    counts = {}
    for r in rows:
        counts[r["ir_class"] or "?"] = counts.get(r["ir_class"] or "?", 0) + 1
    for c in sorted(counts.keys(), key=lambda c: -counts[c]):
        headlines.append(f"  {c:<26}: {counts[c]} / {len(rows)}")
    headlines.append("")
    headlines.append("Banach-contractive members:")
    banach_yes = sum(1 for r in rows if r["banach"])
    headlines.append(f"  {banach_yes} / {len(rows)} datasets satisfy the Banach contraction.")
    headlines.append("")
    headlines.append("Cross-dataset attractor convergence:")
    if max(A) - min(A) < 0.02:
        headlines.append(f"  Tight band: range {max(A)-min(A):.4f} - members converge to a")
        headlines.append("  similar attractor amplitude. Suggests a structural family.")
    else:
        headlines.append(f"  Wide band: range {max(A)-min(A):.4f} - members differ in attractor")
        headlines.append("  amplitude. Each dataset's dynamical regime is distinct.")

    for i, line in enumerate(headlines):
        fig.text(0.10, 0.86 - i*0.030, line, fontsize=10, family="monospace", color="#222")
    _footer4(fig, ctx, run_id, page_num, total, "inference summary")
    pdf.savefig(fig); plt.close(fig)


PLATES = [p_cover, p_disclosure, p_summary_table,
          p_amplitude_compare, p_depth_compare, p_ir_distribution,
          p_eitt_compare, p_hs_norm_ranges, p_omega_compare,
          p_convergence_matrix, p_inference_summary]


def render_stage4(pdf, members: list, jsons: list, project_id: str,
                  run_id=None, options=None) -> int:
    """Render the Stage 4 paged group report.

    members : list of dataset_ids
    jsons   : matching list of CNT JSON dicts
    """
    ctx = collect_group(members, jsons, project_id)
    total = len(PLATES)
    for k, fn in enumerate(PLATES, 1):
        fn(pdf, ctx, run_id, k, total)
    return total
