#!/usr/bin/env python3
"""
HCI-Atlas Stage 2 v2 — comprehensive Order-2 + bridge from Stage 1.

Doctrine v1.0.1: integer orders only. Anything that aggregates across
timesteps rounds UP to Order 2. The Stage 1 closing summary's
trajectory aggregates (Hs traj, Aitchison-norm traj, ILR-axis traj)
formally live here.

Adds three named views from the CNT Engine Mathematics Handbook:
  * System Course Plot (Ch 15) — PCA 2D path with S/F markers + V_net
  * Compositional Bearing Scope (Ch 16) — three orthogonal faces
  * Helmsman displacement per year (from stage23_plates.py)
  * Pairwise divergence ranking (top-15 year-pair Aitchison distances)

Plus all current Stage 2 methods (polar rose, bearing heatmap, ω,
helmsman lineage / frequency / transitions, ring strip, lock timeline,
variation matrix, pair correlation, ω-vs-Hs, 3D, small-multiples, table).
"""
from __future__ import annotations
import hashlib, math, os
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


PAGE_SIZE = (11.0, 8.5)
PDF_DPI   = 150


def _carrier_palette(n):
    base = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    return [base[i % len(base)] for i in range(n)]


# ─── Engine signature: hash of the source files producing this report ───
def _engine_signature() -> dict:
    """Hash the engine + atlas source files producing this Stage 2 report.
    The signature is the same across runs as long as the source code is
    unchanged — gives every output PDF a traceable engine fingerprint."""
    here = Path(__file__).resolve()
    atlas_dir = here.parent
    cnt_py    = atlas_dir.parent / "cnt" / "cnt.py"
    files = {
        "stage2_locked.py": here,
        "cnt.py":           cnt_py,
    }
    h_each = {}
    h_combined = hashlib.sha256()
    for tag, p in files.items():
        if p.exists():
            d = hashlib.sha256(p.read_bytes()).hexdigest()
            h_each[tag] = d
            h_combined.update(d.encode())
        else:
            h_each[tag] = None
    return {
        "files":    h_each,
        "combined": h_combined.hexdigest(),
        "short":    h_combined.hexdigest()[:12],
    }


_ENGINE_SIG_CACHE = None
def engine_signature() -> dict:
    global _ENGINE_SIG_CACHE
    if _ENGINE_SIG_CACHE is None:
        _ENGINE_SIG_CACHE = _engine_signature()
    return _ENGINE_SIG_CACHE


# ─── Friendly dataset name + year-range banner ───
_FRIENDLY_NAMES = {
    "ember_chn":              "China — EMBER electricity generation",
    "ember_deu":              "Germany — EMBER electricity generation",
    "ember_fra":              "France — EMBER electricity generation",
    "ember_gbr":              "United Kingdom — EMBER electricity generation",
    "ember_ind":              "India — EMBER electricity generation",
    "ember_jpn":              "Japan — EMBER electricity generation",
    "ember_usa":              "United States — EMBER electricity generation",
    "ember_wld":              "World — EMBER electricity generation",
    "ember_combined_panel":   "EMBER combined panel (8 countries)",
    "backblaze_fleet":        "BackBlaze hard-drive fleet failures",
    "geochem_ball_region":    "EarthChem Ball — region binning",
    "geochem_ball_age":       "EarthChem Ball — age-epoch binning",
    "geochem_ball_tas":       "EarthChem Ball — TAS rock-type binning",
    "geochem_stracke_oib":    "EarthChem Stracke OIB",
    "geochem_stracke_morb":   "EarthChem Stracke MORB",
    "geochem_tappe_kim1":     "EarthChem Tappe — kimberlites",
    "geochem_qin_cpx":        "EarthChem Qin — clinopyroxenes",
    "fao_irrigation_methods": "FAO irrigation methods (cross-section)",
    "commodities_gold_silver":"Gold / Silver commodities",
    "nuclear_semf":           "Nuclear binding energy — SEMF",
    "markham_budget":         "Markham municipal operating budget",
    "iiasa_ngfs":             "IIASA NGFS Phase-4 NZ-2050 sectors",
    "esa_planck_cosmic":      "ESA Planck cosmic energy budget × redshift",
    "financial_sector":       "S&P 500 GICS sector portfolio",
    "chemixhub_oxide":        "ChemixHub HOIP-7 oxide samples",
}


def _dataset_friendly(dataset_id: str, j: dict) -> str:
    name = _FRIENDLY_NAMES.get(dataset_id)
    if name:
        return name
    # Fallback: title-case the id with underscores → spaces
    return dataset_id.replace("_", " ").title()


def _year_range(j: dict) -> str:
    inp = j["input"]
    labels = inp.get("labels") or []
    if not labels:
        return ""
    def to_int(s):
        try:    return int(s)
        except: return None
    ints = [to_int(l) for l in labels]
    if all(x is not None for x in ints):
        return f"{min(ints)}-{max(ints)}"
    return f"{labels[0]} → {labels[-1]}"


def _report_title(dataset_id: str, j: dict) -> str:
    name = _dataset_friendly(dataset_id, j)
    yrs  = _year_range(j)
    if yrs:
        return f"Compositional system geometry and dynamics for, {name} {yrs}"
    return f"Compositional system geometry and dynamics for, {name}"


def _today_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _footer(fig, j, run_id, page_num, total, method=""):
    inp = j["input"]; di = j["diagnostics"]; md = j["metadata"]
    src_sha = (inp.get("source_file_sha256") or "?")[:12]
    csha    = (di.get("content_sha256") or "?")[:12]
    eng_sig = engine_signature()["short"]
    eng_v   = md.get("engine_version", "?")
    fig.text(0.5, 0.025,
             f"engine: {eng_v}  ({eng_sig}…)  |  data: {csha}…  |  source: {src_sha}…",
             ha="center", fontsize=7, family="monospace", color="#666")
    fig.text(0.5, 0.010,
             f"{_today_iso()}  |  run: {run_id or 'unsaved'}  |  "
             f"page {page_num}/{total}  |  STAGE 2 (Order 2)  |  {method}",
             ha="center", fontsize=7, family="monospace", color="#888")


def _title(fig, dataset_id, plate_no, plate_name, j):
    md = j["metadata"]
    report_title = _report_title(dataset_id, j)
    fig.text(0.5, 0.972, report_title,
             ha="center", fontsize=11, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.952,
             f"Plate {plate_no}  |  {plate_name}",
             ha="center", fontsize=9, color="#444", fontstyle="italic")
    fig.text(0.5, 0.935,
             f"Engine {md['engine_version']}  |  "
             f"Schema {md['schema_version']}  |  Order 2",
             ha="center", fontsize=8, color="#666")


def collect(j):
    inp = j["input"]; T = inp["n_records"]; D = inp["n_carriers"]
    carriers = inp["carriers"]; labels = inp["labels"]

    # Bearings T × n_pairs
    n_pairs = D * (D - 1) // 2
    bearings = np.full((T, n_pairs), np.nan)
    pair_names = [None]*n_pairs; pair_idx = {}
    for k, (i, jj) in enumerate(combinations(range(D), 2)):
        pair_names[k] = f"{carriers[i]}-{carriers[jj]}"
        pair_idx[(i, jj)] = k
    for t, ts in enumerate(j["tensor"]["timesteps"]):
        for p in (ts.get("higgins_extensions", {}).get("bearing_tensor", {}) or {}).get("pairs", []):
            ci = carriers.index(p["carrier_i"]) if p.get("carrier_i") in carriers else None
            cj = carriers.index(p["carrier_j"]) if p.get("carrier_j") in carriers else None
            if ci is not None and cj is not None:
                k = pair_idx.get((min(ci, cj), max(ci, cj)))
                if k is not None:
                    bearings[t, k] = p.get("theta_deg", float("nan"))

    # CLR matrix (T x D) for course plot
    clr_mat = np.zeros((T, D))
    for t, ts in enumerate(j["tensor"]["timesteps"]):
        cs = ts.get("coda_standard", {}) or {}
        clr_mat[t] = np.asarray(cs.get("clr") or ts.get("clr") or [0.0]*D)

    # Helmert ILR
    basis = np.asarray(j["tensor"]["helmert_basis"]["coefficients"])
    ilr_mat = (basis @ clr_mat.T).T   # (T, D-1)

    # Metric ledger
    ml = j["stages"]["stage1"]["higgins_extensions"]["metric_ledger"]
    omega = np.array([m.get("omega_deg", 0.0) for m in ml])
    hs    = np.array([m.get("hs", 0.0) for m in ml])
    cond  = np.array([m.get("condition", 0.0) for m in ml])
    rings = [m.get("ring", "") for m in ml]
    helms = [m.get("helmsman", "") for m in ml]
    metric_trace = np.array([
        ts.get("higgins_extensions", {}).get("metric_tensor", {}).get("trace", 0.0)
        for ts in j["tensor"]["timesteps"]
    ])

    # Aitchison distances per consecutive step
    d_step = np.zeros(T)
    for t in range(1, T):
        d_step[t] = np.sqrt(np.sum((clr_mat[t] - clr_mat[t-1])**2))

    # Pairwise distance matrix
    d_mat = np.zeros((T, T))
    for a in range(T):
        for b in range(T):
            d_mat[a, b] = np.sqrt(np.sum((clr_mat[a] - clr_mat[b])**2))

    # Aitchison norm per timestep
    norm = np.array([np.sqrt(np.sum(clr_mat[t]**2)) for t in range(T)])

    # Variation matrix + carrier pair examination
    var_mat = np.asarray(j["stages"]["stage2"]["coda_standard"]["variation_matrix"])
    cpe = j["stages"]["stage2"]["higgins_extensions"]["carrier_pair_examination"]

    # Locks
    locks = j["diagnostics"]["higgins_extensions"].get("lock_events", [])

    return dict(
        T=T, D=D, carriers=carriers, labels=labels,
        bearings=bearings, pair_names=pair_names,
        omega=omega, hs=hs, cond=cond, rings=rings, helms=helms,
        metric_trace=metric_trace,
        clr_mat=clr_mat, ilr_mat=ilr_mat,
        d_step=d_step, d_mat=d_mat, norm=norm,
        var_mat=var_mat, cpe=cpe, locks=locks,
    )


# ── PLATE 1 — Cover / declaration ──────────────────────────────
def p_cover(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    inp = j["input"]; md = j["metadata"]; di = j["diagnostics"]
    sig = engine_signature()

    # Headline title (auto-formatted per dataset)
    report_title = _report_title(dataset_id, j)
    fig.text(0.5, 0.88, "Compositional system",
             ha="center", fontsize=22, fontweight="bold", color="#1f4e79")
    fig.text(0.5, 0.83, "geometry and dynamics for,",
             ha="center", fontsize=14, color="#444", fontstyle="italic")
    fig.text(0.5, 0.77, _dataset_friendly(dataset_id, j),
             ha="center", fontsize=18, fontweight="bold", color="#222")
    yrs = _year_range(j)
    if yrs:
        fig.text(0.5, 0.73, yrs, ha="center", fontsize=14, color="#222")

    # Identity + traceability block
    rows = [
        ("Report title",   report_title),
        ("Generated",      _today_iso()),
        ("Run ID",         run_id or "unsaved"),
        ("Dataset ID",     dataset_id),
        ("T (records)",    str(ctx["T"])),
        ("D (carriers)",   str(ctx["D"])),
        ("Engine version", md["engine_version"]),
        ("Schema version", md["schema_version"]),
        ("Engine signature (sha256[:32])",
                           sig["combined"][:32] + "…"),
        ("Source CSV SHA-256",
                           (inp.get("source_file_sha256") or "?")[:32] + "…"),
        ("Closed data SHA-256",
                           (inp.get("closed_data_sha256") or "?")[:32] + "…"),
        ("Content SHA-256 (canonical JSON)",
                           (di.get("content_sha256") or "?")[:32] + "…"),
    ]
    y = 0.62
    for k, v in rows:
        fig.text(0.10, y, f"{k:<34}", fontsize=9, family="monospace",
                 color="#222", fontweight="bold")
        fig.text(0.45, y, v, fontsize=9, family="monospace", color="#1f4e79")
        y -= 0.030

    # Reading order note
    fig.text(0.10, 0.20,
             "Reading order — geometry first, dynamics second.\n"
             "  §A  Data disclosure & processing notes\n"
             "  §B  Geometry  : structure on the simplex\n"
             "             evolution of proportions → ternaries → variation\n"
             "             → correlation → scree → biplot → top-N biplot\n"
             "             → balance-dendrogram → SBP table\n"
             "  §C  Dynamics : evolution through compositional space\n"
             "             trajectories (Hs, ‖clr‖, ILR axes) → System Course Plot\n"
             "             → bearing rose → bearing heatmap → ω → metric trace\n"
             "             → helmsman → ring class → locks → CBS\n"
             "             → pairwise divergence ranking → ω↔Hs\n"
             "  §D  Summary",
             fontsize=9, family="monospace", color="#222")

    _footer(fig, j, run_id, page_num, total, "cover")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 2 — Data disclosure & processing-anomaly review ──────
def p_data_disclosure(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "§A  Data Disclosure & Processing-Anomaly Review", j)

    inp = j["input"]; md  = j["metadata"]; di  = j["diagnostics"]
    he  = di.get("higgins_extensions", {}) or {}
    units = md.get("units", {}) or {}
    eng_cfg = md.get("engine_config", {}) or {}

    # Compose disclosure rows
    lines = []
    lines.append("INPUT DATA")
    lines.append(f"  source file        : {inp.get('source_file', '?')}")
    lines.append(f"  source SHA-256     : {inp.get('source_file_sha256','?')}")
    lines.append(f"  closed data SHA-256: {inp.get('closed_data_sha256','?')}")
    lines.append(f"  records (T)        : {inp['n_records']}")
    lines.append(f"  carriers (D)       : {inp['n_carriers']}")
    lines.append(f"  carriers           : {', '.join(inp['carriers'])}")
    lines.append("")

    lines.append("ORDERING")
    ord_ = inp.get("ordering", {}) or {}
    lines.append(f"  is_temporal        : {ord_.get('is_temporal','?')}")
    lines.append(f"  ordering_method    : {ord_.get('ordering_method','?')}")
    cav = ord_.get("caveat")
    if cav: lines.append(f"  caveat             : {cav}")
    lines.append("")

    lines.append("ZERO REPLACEMENT")
    zr = inp.get("zero_replacement", {}) or {}
    if isinstance(zr, dict):
        n_zero = zr.get("n_zeros_replaced", zr.get("zeros_replaced",
                       zr.get("n_replaced", 0)))
        delta  = zr.get("delta", zr.get("replacement_delta", "default"))
        method = zr.get("method", "additive δ")
        lines.append(f"  zeros replaced     : {n_zero}")
        lines.append(f"  replacement δ      : {delta}")
        lines.append(f"  method             : {method}")
    else:
        lines.append(f"  {zr}")
    lines.append("")

    lines.append("UNITS LINEAGE  (schema 2.1.0)")
    lines.append(f"  input_units                 : {units.get('input_units','—')}")
    lines.append(f"  higgins_scale_units         : {units.get('higgins_scale_units','—')}")
    lines.append(f"  units_scale_factor_to_neper : {units.get('units_scale_factor_to_neper','—')}")
    lines.append("")

    lines.append("ENGINE CONFIG ACTIVE OVERRIDES")
    overrides = eng_cfg.get("active_overrides", {}) or {}
    if overrides:
        for k, v in overrides.items():
            lines.append(f"  {k:<30}: {v}")
    else:
        lines.append("  (none — defaults from cnt.py USER CONFIGURATION block)")
    lines.append("")

    lines.append("ENGINE SOURCE FINGERPRINT")
    sig = engine_signature()
    for tag, h in sig["files"].items():
        lines.append(f"  {tag:<22}: {h or 'missing'}")
    lines.append(f"  combined sha256       : {sig['combined']}")
    lines.append("")

    lines.append("DEGENERACY FLAGS")
    flags = he.get("degeneracy_flags", []) or []
    if not flags:
        lines.append("  (none)")
    else:
        for f in flags[:15]:
            lines.append(f"  ⚠ {f}")
        if len(flags) > 15:
            lines.append(f"  … ({len(flags)-15} more)")
    lines.append("")

    lines.append("LOCK EVENTS  (period-2 detector)")
    locks = he.get("lock_events", []) or []
    lines.append(f"  total events       : {len(locks)}")
    if locks:
        # group by type
        types = {}
        for lk in locks:
            t = lk.get("type") or lk.get("kind") or "lock"
            types[t] = types.get(t, 0) + 1
        for t, n in sorted(types.items(), key=lambda kv:-kv[1]):
            lines.append(f"    {t:<22}: {n}")
    lines.append("")

    lines.append("EITT BENCH-TEST RESIDUALS")
    eitt = he.get("eitt_residuals", {}) or {}
    if eitt:
        for k, v in list(eitt.items())[:8]:
            lines.append(f"  {k:<22}: {v}")
    else:
        lines.append("  (no residuals recorded)")
    lines.append("")

    # Sanity flags computed from ctx
    lines.append("SANITY CHECKS  (computed during this report)")
    norm = np.asarray(ctx["norm"])
    omega = np.asarray(ctx["omega"])
    hs = np.asarray(ctx["hs"])
    n_nonfinite_norm = int(np.sum(~np.isfinite(norm)))
    n_nonfinite_om   = int(np.sum(~np.isfinite(omega)))
    n_nonfinite_hs   = int(np.sum(~np.isfinite(hs)))
    cs_min = ctx["clr_mat"].sum(axis=1).min() if ctx["clr_mat"].size else 0.0
    cs_max = ctx["clr_mat"].sum(axis=1).max() if ctx["clr_mat"].size else 0.0
    lines.append(f"  ‖clr‖ non-finite count : {n_nonfinite_norm}")
    lines.append(f"  ω    non-finite count : {n_nonfinite_om}")
    lines.append(f"  Hs   non-finite count : {n_nonfinite_hs}")
    lines.append(f"  Σ CLR per row range   : [{cs_min:+.2e}, {cs_max:+.2e}]"
                 f"   (should be ≈ 0)")
    lines.append("")

    # Render — two columns to fit a single page
    col1 = lines[: len(lines)//2 + 1]
    col2 = lines[len(lines)//2 + 1:]
    for i, line in enumerate(col1):
        y = 0.90 - i*0.022
        fig.text(0.04, y, line, fontsize=8, family="monospace", color="#222")
    for i, line in enumerate(col2):
        y = 0.90 - i*0.022
        fig.text(0.50, y, line, fontsize=8, family="monospace", color="#222")

    fig.text(0.5, 0.05,
             "If any flag above is non-empty, the analysis on subsequent "
             "pages still ran but the reader should weight those plates "
             "accordingly. Determinism is preserved either way.",
             ha="center", fontsize=8, color="#888", fontstyle="italic")

    _footer(fig, j, run_id, page_num, total, "data disclosure")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 2 — System Course Plot (CNT Math Handbook Ch 15) ────
def p_course_plot(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "System Course Plot — PCA 2D path with S→F net vector", j)

    # PCA on CLR matrix
    X = ctx["clr_mat"] - ctx["clr_mat"].mean(axis=0)
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    pc = U[:, :2] * S[:2]   # (T, 2)
    pc1, pc2 = pc[:, 0], pc[:, 1]

    ax = fig.add_axes([0.10, 0.18, 0.55, 0.70])
    palette = _carrier_palette(ctx["D"])
    # Course line
    ax.plot(pc1, pc2, "-", color="#888", lw=1.2, alpha=0.8, zorder=2)
    # All points coloured by helmsman
    for t in range(ctx["T"]):
        h = ctx["helms"][t]
        c = palette[ctx["carriers"].index(h)] if h in ctx["carriers"] else "#444"
        ax.scatter(pc1[t], pc2[t], s=80, color=c, edgecolor="black",
                   linewidth=0.6, zorder=4)
        ax.annotate(ctx["labels"][t], (pc1[t], pc2[t]), fontsize=7,
                    xytext=(4, 3), textcoords="offset points")
    # Start / Final markers
    ax.scatter([pc1[0]], [pc2[0]], s=300, marker="s", color="#2ca02c",
               edgecolor="black", linewidth=1.2, zorder=5, label="S (start)")
    ax.scatter([pc1[-1]], [pc2[-1]], s=300, marker="*", color="#d62728",
               edgecolor="black", linewidth=1.2, zorder=5, label="F (final)")
    # V_net arrow S → F
    ax.annotate("", xy=(pc1[-1], pc2[-1]), xytext=(pc1[0], pc2[0]),
                arrowprops=dict(arrowstyle="->", color="#1f4e79", lw=2.0,
                                alpha=0.7))
    # Centroid crosshair
    ax.axhline(0, color="#bbb", lw=0.5, ls=":")
    ax.axvline(0, color="#bbb", lw=0.5, ls=":")
    ax.set_xlabel(f"PC1 ({100*S[0]**2/np.sum(S**2):.1f}% var)", fontsize=9)
    ax.set_ylabel(f"PC2 ({100*S[1]**2/np.sum(S**2):.1f}% var)", fontsize=9)
    ax.set_title("CLR trajectory projected by PCA",
                 fontsize=10, color="#1f4e79")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, alpha=0.3)

    # Metrics block
    h_start = ctx["clr_mat"][0]; h_final = ctx["clr_mat"][-1]
    V_net = h_final - h_start
    net_dist = np.sqrt(np.sum(V_net**2))
    path_len = ctx["d_step"].sum()
    directness = net_dist / path_len if path_len > 0 else 0.0
    dr_start = h_start.max() - h_start.min()
    dr_final = h_final.max() - h_final.min()

    ax_t = fig.add_axes([0.68, 0.18, 0.30, 0.70])
    ax_t.axis("off"); ax_t.set_xlim(0, 1); ax_t.set_ylim(0, 1)
    ax_t.text(0.0, 0.97, "Navigation metrics (V_net = h_F − h_S)",
              fontsize=10, fontweight="bold", color="#1f4e79")
    rows = [
        f"h_start label    : {ctx['labels'][0]}",
        f"h_final label    : {ctx['labels'][-1]}",
        "",
        f"net_distance     : {net_dist:.4f} HLR",
        f"path_length      : {path_len:.4f} HLR",
        f"course_directness: {directness:.4f}",
        f"  (1.0 = straight line, 0 = pure looping)",
        "",
        f"dynamic range S  : {dr_start:.4f} HLR",
        f"dynamic range F  : {dr_final:.4f} HLR",
        "",
        "Reading guide:",
        "  tight cluster  → stable composition",
        "  long excursion → structural shift",
        "  sharp turn     → regime transition",
        "  loop           → cyclic behaviour",
        "  spiral         → systematic drift",
    ]
    for i, r in enumerate(rows):
        ax_t.text(0.0, 0.91 - i*0.045, r, fontsize=8,
                  family="monospace", color="#222")

    _footer(fig, j, run_id, page_num, total, "system course plot (PCA)")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 3 — Hs trajectory (bridge from Stage 1) ──────────────
def p_hs_trajectory(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "Hs (Higgins scale) trajectory — Order 2 aggregate", j)
    ax = fig.add_axes([0.10, 0.20, 0.80, 0.65])
    x = list(range(ctx["T"]))
    ax.plot(x, ctx["hs"], "o-", color="#1f4e79", lw=1.4, markersize=5)
    for hh in (0.1, 0.3, 0.5, 0.7, 0.9):
        ax.axhline(hh, color="#888", ls=":", lw=0.4)
    ax.set_xlim(-0.5, ctx["T"]-0.5); ax.set_ylim(0, 1.05)
    ax.set_xlabel("timestep"); ax.set_ylabel("Hs")
    ax.grid(True, alpha=0.3)
    ax.text(0.02, 0.97,
            f"min {ctx['hs'].min():.4f}  mean {ctx['hs'].mean():.4f}  "
            f"max {ctx['hs'].max():.4f}",
            transform=ax.transAxes, fontsize=8, family="monospace", va="top")
    if ctx["T"] <= 30:
        ax.set_xticks(x)
        if ctx["T"] <= 12:
            ax.set_xticklabels(ctx["labels"], rotation=45, ha="right",
                               fontsize=7)
    _footer(fig, j, run_id, page_num, total, "Hs trajectory")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 4 — Aitchison norm trajectory ────────────────────────
def p_norm_trajectory(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "Aitchison norm trajectory ‖clr(x)‖₂ — Order 2 aggregate", j)
    ax = fig.add_axes([0.10, 0.20, 0.80, 0.65])
    x = list(range(ctx["T"]))
    ax.plot(x, ctx["norm"], "s-", color="#d62728", lw=1.4, markersize=5)
    ax.fill_between(x, 0, ctx["norm"], color="#d62728", alpha=0.10)
    ax.set_xlim(-0.5, ctx["T"]-0.5)
    ax.set_xlabel("timestep"); ax.set_ylabel("‖clr(x)‖₂  (HLR)")
    ax.grid(True, alpha=0.3)
    ax.text(0.02, 0.97,
            f"min {ctx['norm'].min():.4f}  mean {ctx['norm'].mean():.4f}  "
            f"max {ctx['norm'].max():.4f} HLR",
            transform=ax.transAxes, fontsize=8, family="monospace", va="top")
    if ctx["T"] <= 30:
        ax.set_xticks(x)
        if ctx["T"] <= 12:
            ax.set_xticklabels(ctx["labels"], rotation=45, ha="right",
                               fontsize=7)
    _footer(fig, j, run_id, page_num, total, "Aitchison norm trajectory")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 5 — ILR axes 1-3 trajectories ────────────────────────
def p_ilr_trajectories(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "ILR axes 1–3 trajectories (Helmert basis) — Order 2 aggregate", j)
    ax = fig.add_axes([0.10, 0.20, 0.80, 0.65])
    x = list(range(ctx["T"]))
    n = min(3, ctx["ilr_mat"].shape[1])
    cs = ["#2ca02c", "#1f77b4", "#ff7f0e"]
    for k in range(n):
        ax.plot(x, ctx["ilr_mat"][:, k], "-o", color=cs[k], lw=1.0,
                markersize=3, label=f"ILR({k+1})")
    ax.axhline(0, color="#888", lw=0.5, ls="--")
    ax.set_xlim(-0.5, ctx["T"]-0.5)
    ax.set_xlabel("timestep"); ax.set_ylabel("ILR (HLR)")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)
    if ctx["T"] <= 30:
        ax.set_xticks(x)
        if ctx["T"] <= 12:
            ax.set_xticklabels(ctx["labels"], rotation=45, ha="right",
                               fontsize=7)
    _footer(fig, j, run_id, page_num, total, "ILR axes 1-3 trajectories")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 6 — Polar bearing rose at sample timesteps ─────────
def p_polar_rose(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num, "Polar bearing rose (4 sample timesteps)", j)
    T = ctx["T"]
    samples = sorted(set([0, T//3, (2*T)//3, T-1]))[:4]
    pos = [(0.05, 0.50, 0.40, 0.40), (0.50, 0.50, 0.40, 0.40),
           (0.05, 0.05, 0.40, 0.40), (0.50, 0.05, 0.40, 0.40)]
    for k, fi in enumerate(samples):
        ax = fig.add_axes(pos[k], projection="polar")
        b = ctx["bearings"][fi]
        valid = ~np.isnan(b)
        thetas = np.deg2rad(b[valid])
        ax.bar(thetas, np.ones_like(thetas), width=0.08, color="#1f77b4",
               alpha=0.75, edgecolor="white", lw=0.5)
        ax.set_theta_zero_location("E"); ax.set_theta_direction(1)
        ax.set_ylim(0, 1.2); ax.set_yticks([])
        ax.set_title(f"t={fi}  ({ctx['labels'][fi]})  ω={ctx['omega'][fi]:.2f}°",
                     fontsize=10, color="#1f4e79")
    _footer(fig, j, run_id, page_num, total, "polar bearing rose")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 7 — Bearing heatmap T × pairs ────────────────────────
def p_bearing_heatmap(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num, "Bearing heatmap T × C(D,2) pairs", j)
    ax = fig.add_axes([0.10, 0.12, 0.80, 0.74])
    im = ax.imshow(ctx["bearings"].T, aspect="auto", cmap="twilight",
                   vmin=-180, vmax=180, interpolation="nearest")
    ax.set_xlabel("timestep"); ax.set_ylabel("carrier pair index")
    fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02).set_label("θ (deg)")
    if ctx["T"] <= 30:
        ax.set_xticks(range(ctx["T"]))
        if ctx["T"] <= 12:
            ax.set_xticklabels(ctx["labels"], rotation=45, ha="right",
                               fontsize=6)
    if len(ctx["pair_names"]) <= 30:
        ax.set_yticks(range(len(ctx["pair_names"])))
        ax.set_yticklabels(ctx["pair_names"], fontsize=6)
    _footer(fig, j, run_id, page_num, total, "bearing heatmap")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 8 — ω trajectory ─────────────────────────────────────
def p_omega(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num, "ω angular velocity trajectory", j)
    ax = fig.add_axes([0.10, 0.20, 0.80, 0.66])
    x = list(range(ctx["T"]))
    ax.plot(x, ctx["omega"], "o-", color="#1f4e79", lw=1.4, markersize=5)
    ax.fill_between(x, 0, ctx["omega"], color="#1f4e79", alpha=0.15)
    ax.set_xlim(-0.5, ctx["T"]-0.5)
    ax.set_xlabel("timestep"); ax.set_ylabel("ω (deg)")
    ax.grid(True, alpha=0.3)
    if ctx["T"] <= 30:
        ax.set_xticks(x)
        if ctx["T"] <= 12:
            ax.set_xticklabels(ctx["labels"], rotation=45, ha="right",
                               fontsize=7)
    _footer(fig, j, run_id, page_num, total, "ω line plot")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 9 — Metric trace + condition ─────────────────────────
def p_metric_lines(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "Metric tensor trace + condition number", j)
    x = list(range(ctx["T"]))
    ax1 = fig.add_axes([0.10, 0.55, 0.80, 0.30])
    ax1.plot(x, ctx["metric_trace"], "s-", color="#2ca02c", lw=1.2)
    ax1.set_ylabel("trace(g)"); ax1.grid(True, alpha=0.3)
    ax1.set_title("Metric tensor trace (κ surrogate)", fontsize=9,
                  color="#1f4e79", loc="left")
    ax2 = fig.add_axes([0.10, 0.12, 0.80, 0.30])
    ax2.semilogy(x, ctx["cond"], "^-", color="#d62728", lw=1.2)
    ax2.set_xlabel("timestep"); ax2.set_ylabel("condition #")
    ax2.grid(True, alpha=0.3, which="both")
    ax2.set_title("Condition number (log)", fontsize=9, color="#1f4e79",
                  loc="left")
    _footer(fig, j, run_id, page_num, total, "metric + condition")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 10 — Helmsman lineage ────────────────────────────────
def p_helmsman_lineage(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num, "Helmsman σ lineage timeline", j)
    ax = fig.add_axes([0.10, 0.12, 0.80, 0.74])
    palette = _carrier_palette(ctx["D"])
    cmap = {c: palette[i] for i, c in enumerate(ctx["carriers"])}
    cmap[""] = "#cccccc"
    for t, h in enumerate(ctx["helms"]):
        c = cmap.get(h, "#cccccc")
        y = ctx["carriers"].index(h) if h in ctx["carriers"] else -0.5
        ax.barh([y], [1], left=[t-0.5], height=0.8, color=c, alpha=0.85,
                edgecolor="white", lw=0.4)
    ax.set_xlim(-0.5, ctx["T"]-0.5); ax.set_ylim(-1, ctx["D"])
    ax.set_yticks(range(ctx["D"])); ax.set_yticklabels(ctx["carriers"],
                                                       fontsize=8)
    ax.invert_yaxis(); ax.set_xlabel("timestep")
    if ctx["T"] <= 30:
        ax.set_xticks(range(ctx["T"]))
        if ctx["T"] <= 12:
            ax.set_xticklabels(ctx["labels"], rotation=45, ha="right",
                               fontsize=6)
    _footer(fig, j, run_id, page_num, total, "helmsman lineage")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 11 — Helmsman frequency + transitions + per-year displacement ──
def p_helmsman_full(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "Helmsman σ — frequency · transitions · per-year displacement", j)
    carriers = ctx["carriers"]; helms = ctx["helms"]
    palette = _carrier_palette(ctx["D"])

    # Frequency
    ax_h = fig.add_axes([0.05, 0.50, 0.28, 0.40])
    counts = {c: 0 for c in carriers}; counts[""] = 0
    for h in helms: counts[h] = counts.get(h, 0) + 1
    keys = [c for c in carriers if counts.get(c, 0) > 0]
    vals = [counts[k] for k in keys]
    cs = [palette[carriers.index(k)] for k in keys]
    ax_h.barh(range(len(keys)), vals, color=cs)
    ax_h.set_yticks(range(len(keys))); ax_h.set_yticklabels(keys, fontsize=7)
    ax_h.invert_yaxis(); ax_h.set_xlabel("count"); ax_h.tick_params(labelsize=7)
    ax_h.set_title("Helmsman frequency", fontsize=9, color="#1f4e79", loc="left")
    ax_h.grid(True, axis="x", alpha=0.3)

    # Transitions
    D = ctx["D"]; trans = np.zeros((D, D))
    for k in range(len(helms)-1):
        a, b = helms[k], helms[k+1]
        if a in carriers and b in carriers:
            trans[carriers.index(a), carriers.index(b)] += 1
    ax_t = fig.add_axes([0.40, 0.50, 0.28, 0.40])
    im = ax_t.imshow(trans, cmap="Blues", aspect="auto")
    ax_t.set_xticks(range(D)); ax_t.set_yticks(range(D))
    ax_t.set_xticklabels(carriers, rotation=45, ha="right", fontsize=6)
    ax_t.set_yticklabels(carriers, fontsize=6)
    ax_t.set_xlabel("to", fontsize=8); ax_t.set_ylabel("from", fontsize=8)
    ax_t.set_title("Transition matrix", fontsize=9, color="#1f4e79", loc="left")
    fig.colorbar(im, ax=ax_t, fraction=0.04, pad=0.02)

    # Per-year displacement (|delta h| per t with helmsman colour)
    ax_d = fig.add_axes([0.05, 0.08, 0.90, 0.32])
    x = list(range(ctx["T"]))
    bar_colors = [cmap.get(h, "#888") if (cmap := {c: palette[i] for i, c in enumerate(carriers)}).get(h) else "#888"
                  for h in helms]
    # Simpler colour computation
    bar_colors = []
    cmap = {c: palette[i] for i, c in enumerate(carriers)}
    for h in helms:
        bar_colors.append(cmap.get(h, "#888"))
    ax_d.bar(x, ctx["d_step"], color=bar_colors, edgecolor="white", lw=0.4)
    # Helmsman labels above tallest bars
    for t in range(ctx["T"]):
        if ctx["d_step"][t] > 0.6 * ctx["d_step"].max():
            ax_d.text(t, ctx["d_step"][t]*1.02, helms[t][:8],
                      ha="center", fontsize=6, color="#222", rotation=90)
    ax_d.set_xlabel("timestep"); ax_d.set_ylabel("|Δh| (HLR)")
    ax_d.set_title("Helmsman displacement per year (bar coloured by helmsman)",
                   fontsize=9, color="#1f4e79", loc="left")
    ax_d.grid(True, axis="y", alpha=0.3)
    if ctx["T"] <= 30:
        ax_d.set_xticks(x)
        if ctx["T"] <= 12:
            ax_d.set_xticklabels(ctx["labels"], rotation=45, ha="right",
                                 fontsize=6)
    _footer(fig, j, run_id, page_num, total, "helmsman freq + transitions + displacement")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 12 — Ring strip + Hs ─────────────────────────────────
def p_ring_strip(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num, "Ring class evolution + Hs", j)
    ax = fig.add_axes([0.10, 0.45, 0.80, 0.20])
    rc = {"Hs-1": "#1f4e79", "Hs-2": "#2ca02c", "Hs-3": "#bcbd22",
          "Hs-4": "#ff7f0e", "Hs-5": "#d62728", "Hs-6": "#9467bd", "": "#ccc"}
    for t, r in enumerate(ctx["rings"]):
        ax.barh([0], [1], left=[t-0.5], height=0.8,
                color=rc.get(r, "#ccc"), edgecolor="white", lw=0.4)
    ax.set_xlim(-0.5, ctx["T"]-0.5); ax.set_yticks([])
    ax.set_title("Ring class evolution", fontsize=9, color="#1f4e79", loc="left")
    if ctx["T"] <= 30:
        ax.set_xticks(range(ctx["T"]))
        if ctx["T"] <= 12:
            ax.set_xticklabels(ctx["labels"], rotation=45, ha="right",
                               fontsize=6)

    ax2 = fig.add_axes([0.10, 0.12, 0.80, 0.25])
    ax2.plot(range(ctx["T"]), ctx["hs"], "o-", color="#1f4e79", lw=1.2)
    for hh in (0.1, 0.3, 0.5, 0.7, 0.9):
        ax2.axhline(hh, color="#888", lw=0.4, ls=":")
    ax2.set_xlim(-0.5, ctx["T"]-0.5); ax2.set_ylim(0, 1.05)
    ax2.set_xlabel("timestep"); ax2.set_ylabel("Hs"); ax2.grid(True, alpha=0.3)
    _footer(fig, j, run_id, page_num, total, "ring strip + Hs")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 13 — Lock event timeline ─────────────────────────────
def p_locks(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "Lock event timeline (carriers × timesteps)", j)
    ax = fig.add_axes([0.10, 0.15, 0.80, 0.72])
    palette = _carrier_palette(ctx["D"])
    if not ctx["locks"]:
        ax.text(0.5, 0.5, "No lock events recorded.", ha="center",
                va="center", fontsize=12, color="#888",
                transform=ax.transAxes)
    else:
        for ev in ctx["locks"]:
            ti = ev.get("timestep_index", 0)
            c = ev.get("carrier", "?")
            etype = ev.get("event_type", "LOCK")
            y = ctx["carriers"].index(c) if c in ctx["carriers"] else -1
            color = palette[ctx["carriers"].index(c)] if c in ctx["carriers"] else "#888"
            marker = "v" if "ACQ" in etype else ("^" if "REL" in etype else "o")
            ax.scatter([ti], [y], s=120, color=color, edgecolor="black",
                       linewidth=0.7, marker=marker)
    ax.set_xlim(-1, ctx["T"]); ax.set_ylim(-1, ctx["D"])
    ax.set_yticks(range(ctx["D"])); ax.set_yticklabels(ctx["carriers"], fontsize=8)
    ax.invert_yaxis(); ax.set_xlabel("timestep"); ax.grid(True, alpha=0.3)
    _footer(fig, j, run_id, page_num, total, "lock timeline")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 14 — Variation matrix ─────────────────────────────────
def p_var_matrix(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num, "Variation matrix τ_ij heatmap", j)
    ax = fig.add_axes([0.18, 0.12, 0.65, 0.74])
    im = ax.imshow(ctx["var_mat"], cmap="viridis", aspect="equal")
    ax.set_xticks(range(ctx["D"])); ax.set_yticks(range(ctx["D"]))
    ax.set_xticklabels(ctx["carriers"], rotation=45, ha="right", fontsize=7)
    ax.set_yticklabels(ctx["carriers"], fontsize=7)
    fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02).set_label("τ_ij")
    for i in range(ctx["D"]):
        for jj in range(ctx["D"]):
            v = ctx["var_mat"][i, jj]
            if v > 0:
                ax.text(jj, i, f"{v:.2f}", ha="center", va="center",
                        fontsize=6,
                        color="white" if v > ctx["var_mat"].max()/2 else "black")
    _footer(fig, j, run_id, page_num, total, "variation matrix")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 15 — Pair correlation r heatmap + scatter ────────────
def p_pair_correlation(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "Pair Pearson r heatmap + co-movement scatter", j)
    D = ctx["D"]; R = np.eye(D)
    for p in ctx["cpe"]:
        i, jj = p["i"], p["j"]
        R[i, jj] = R[jj, i] = p.get("pearson_r", 0)
    ax_h = fig.add_axes([0.06, 0.12, 0.42, 0.74])
    im = ax_h.imshow(R, cmap="RdBu_r", vmin=-1, vmax=1, aspect="equal")
    ax_h.set_xticks(range(D)); ax_h.set_yticks(range(D))
    ax_h.set_xticklabels(ctx["carriers"], rotation=45, ha="right", fontsize=7)
    ax_h.set_yticklabels(ctx["carriers"], fontsize=7)
    fig.colorbar(im, ax=ax_h, fraction=0.04, pad=0.02)
    ax_s = fig.add_axes([0.55, 0.12, 0.40, 0.74])
    rs = [p.get("pearson_r", 0) for p in ctx["cpe"]]
    bs = [p.get("bearing_spread_deg", 0) for p in ctx["cpe"]]
    ax_s.scatter(rs, bs, s=40, color="#1f77b4", edgecolor="black", lw=0.4)
    ax_s.set_xlabel("Pearson r"); ax_s.set_ylabel("bearing spread (°)")
    ax_s.axvline(0, color="#888", lw=0.4); ax_s.grid(True, alpha=0.3)
    _footer(fig, j, run_id, page_num, total, "pair correlation")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 16 — Compositional Bearing Scope (CBS) — 3 faces ────
def p_cbs(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "Compositional Bearing Scope (CBS) — 3 orthogonal faces (Math Handbook Ch 16)", j)
    # Per-step: mean theta over pairs at t, distance d_step[t], κ surrogate
    mean_theta = np.array([np.nanmean(ctx["bearings"][t]) for t in range(ctx["T"])])
    d = ctx["d_step"]
    kappa = ctx["metric_trace"]
    palette_t = plt.cm.viridis(np.linspace(0, 1, ctx["T"]))

    # XY: θ vs d_A
    ax_xy = fig.add_axes([0.05, 0.50, 0.28, 0.40])
    ax_xy.scatter(mean_theta, d, c=range(ctx["T"]), cmap="viridis",
                  s=40, edgecolor="black", lw=0.3)
    ax_xy.set_xlabel("⟨θ⟩ (deg)", fontsize=8); ax_xy.set_ylabel("d_A (HLR)", fontsize=8)
    ax_xy.set_title("XY: bearing × distance", fontsize=9, color="#1f4e79")
    ax_xy.grid(True, alpha=0.3); ax_xy.tick_params(labelsize=7)

    # XZ: θ vs κ (log)
    ax_xz = fig.add_axes([0.36, 0.50, 0.28, 0.40])
    ax_xz.scatter(mean_theta, kappa, c=range(ctx["T"]), cmap="viridis",
                  s=40, edgecolor="black", lw=0.3)
    ax_xz.set_yscale("log")
    ax_xz.set_xlabel("⟨θ⟩ (deg)", fontsize=8)
    ax_xz.set_ylabel("κ trace (log)", fontsize=8)
    ax_xz.set_title("XZ: bearing × steering metric", fontsize=9, color="#1f4e79")
    ax_xz.grid(True, alpha=0.3, which="both"); ax_xz.tick_params(labelsize=7)

    # YZ: d_A vs κ
    ax_yz = fig.add_axes([0.05, 0.05, 0.28, 0.40])
    ax_yz.scatter(d, kappa, c=range(ctx["T"]), cmap="viridis",
                  s=40, edgecolor="black", lw=0.3)
    ax_yz.set_yscale("log")
    ax_yz.set_xlabel("d_A (HLR)", fontsize=8); ax_yz.set_ylabel("κ (log)", fontsize=8)
    ax_yz.set_title("YZ: distance × steering metric", fontsize=9, color="#1f4e79")
    ax_yz.grid(True, alpha=0.3, which="both"); ax_yz.tick_params(labelsize=7)

    # Info panel
    ax_t = fig.add_axes([0.40, 0.05, 0.55, 0.40])
    ax_t.axis("off"); ax_t.set_xlim(0, 1); ax_t.set_ylim(0, 1)
    ax_t.text(0.0, 0.97, "CBS info panel (Math Handbook Ch 16)",
              fontsize=10, fontweight="bold", color="#1f4e79")
    rows = [
        f"⟨θ⟩ range  : [{np.nanmin(mean_theta):.1f}, {np.nanmax(mean_theta):.1f}]°",
        f"d_A range  : [{d.min():.4f}, {d.max():.4f}] HLR",
        f"κ range    : [{kappa.min():.2e}, {kappa.max():.2e}]",
        f"Hs range   : [{ctx['hs'].min():.4f}, {ctx['hs'].max():.4f}]",
        f"ω max      : {ctx['omega'].max():.2f}°",
        "",
        "Each face: one observation per timestep.",
        "Colour = timestep (early=dark, late=bright).",
        "Three faces locate the system in the",
        "(bearing, distance, steering) measurement cube.",
    ]
    for i, r in enumerate(rows):
        ax_t.text(0.0, 0.90 - i*0.045, r, fontsize=9,
                  family="monospace", color="#222")
    _footer(fig, j, run_id, page_num, total, "CBS three faces")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 17 — Pairwise divergence ranking + distance matrix ──
def p_divergence_ranking(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "Pairwise divergence — distance matrix + top-15 ranking", j)
    # Distance matrix
    ax_m = fig.add_axes([0.05, 0.10, 0.45, 0.78])
    im = ax_m.imshow(ctx["d_mat"], cmap="magma", aspect="equal")
    ax_m.set_xticks([0, ctx["T"]-1]); ax_m.set_yticks([0, ctx["T"]-1])
    ax_m.set_xticklabels([ctx["labels"][0], ctx["labels"][-1]], fontsize=7)
    ax_m.set_yticklabels([ctx["labels"][0], ctx["labels"][-1]], fontsize=7)
    ax_m.set_xlabel("timestep"); ax_m.set_ylabel("timestep")
    fig.colorbar(im, ax=ax_m, fraction=0.04, pad=0.02).set_label("d_A (HLR)")
    ax_m.set_title("Aitchison distance matrix (T × T)",
                   fontsize=9, color="#1f4e79", loc="left")

    # Top-15 ranking
    pairs = []
    for a in range(ctx["T"]):
        for b in range(a+1, ctx["T"]):
            pairs.append((a, b, ctx["d_mat"][a, b]))
    pairs.sort(key=lambda p: -p[2])
    top = pairs[:15]
    ax_r = fig.add_axes([0.55, 0.10, 0.42, 0.78])
    ax_r.axis("off"); ax_r.set_xlim(0, 1); ax_r.set_ylim(0, 1)
    ax_r.text(0.0, 0.97,
              f"{'rank':>4}  {'A':>10}  {'B':>10}  {'d_A':>10}",
              fontsize=8, family="monospace", fontweight="bold", color="#1f4e79")
    for i, (a, b, d) in enumerate(top):
        ax_r.text(0.0, 0.92 - i * 0.052,
                  f"{i+1:>4}  {ctx['labels'][a][:10]:>10}  "
                  f"{ctx['labels'][b][:10]:>10}  {d:>10.4f}",
                  fontsize=8, family="monospace", color="#222")
    _footer(fig, j, run_id, page_num, total, "divergence ranking")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 18 — ω vs Hs scatter (XY test case) ─────────────────
def p_omega_hs(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num, "ω vs Hs scatter (XY test)", j)
    ax = fig.add_axes([0.15, 0.15, 0.74, 0.70])
    sc = ax.scatter(ctx["hs"], ctx["omega"], s=60, c=range(ctx["T"]),
                    cmap="viridis", edgecolor="black", lw=0.5)
    for t in range(ctx["T"]):
        ax.annotate(str(t), (ctx["hs"][t], ctx["omega"][t]),
                    fontsize=6, xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel("Hs"); ax.set_ylabel("ω (deg)"); ax.set_xlim(0, 1)
    ax.grid(True, alpha=0.3)
    fig.colorbar(sc, ax=ax, fraction=0.04, pad=0.02).set_label("timestep")
    _footer(fig, j, run_id, page_num, total, "ω-vs-Hs scatter")
    pdf.savefig(fig); plt.close(fig)


# ── PLATE 19 — Stage 2 numeric summary ─────────────────────────
def p_summary(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num, "Stage 2 numeric summary", j)
    ax = fig.add_axes([0.05, 0.05, 0.90, 0.85]); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    h_start = ctx["clr_mat"][0]; h_final = ctx["clr_mat"][-1]
    V_net = h_final - h_start
    net_dist = float(np.sqrt(np.sum(V_net**2)))
    path_len = float(ctx["d_step"].sum())
    directness = net_dist / path_len if path_len > 0 else 0.0

    rows = [
        f"T = {ctx['T']},  D = {ctx['D']}",
        f"carriers: {', '.join(ctx['carriers'])}",
        "",
        "Navigation (System Course Plot):",
        f"  net_distance     = {net_dist:.4f} HLR",
        f"  path_length      = {path_len:.4f} HLR",
        f"  course_directness= {directness:.4f}",
        "",
        f"ω (deg)        : min {ctx['omega'].min():.2f}  "
        f"mean {ctx['omega'].mean():.2f}  max {ctx['omega'].max():.2f}",
        f"Hs             : min {ctx['hs'].min():.4f}  "
        f"mean {ctx['hs'].mean():.4f}  max {ctx['hs'].max():.4f}",
        f"Aitchison norm : min {ctx['norm'].min():.4f}  "
        f"mean {ctx['norm'].mean():.4f}  max {ctx['norm'].max():.4f}",
        f"κ trace        : min {ctx['metric_trace'].min():.2f}  "
        f"max {ctx['metric_trace'].max():.2f}",
        f"condition #    : min {ctx['cond'].min():.2e}  "
        f"max {ctx['cond'].max():.2e}",
        "",
        f"Bearings: range [{np.nanmin(ctx['bearings']):.2f}, "
        f"{np.nanmax(ctx['bearings']):.2f}]°,  std {np.nanstd(ctx['bearings']):.2f}°",
        f"Lock events    : {len(ctx['locks'])}",
        f"Pairs          : {len(ctx['cpe'])}",
        f"|r| > 0.7 pairs: {sum(1 for p in ctx['cpe'] if abs(p.get('pearson_r', 0)) > 0.7)}",
        "",
        "Helmsman frequency (top 5):",
    ]
    counts = {}
    for h in ctx["helms"]: counts[h] = counts.get(h, 0) + 1
    for c, n in sorted(counts.items(), key=lambda x: -x[1])[:5]:
        rows.append(f"  {c or '(none)':<14}{n:>4}  ({100*n/ctx['T']:.1f}%)")

    rows += ["", f"Variation matrix trace : {float(np.trace(ctx['var_mat'])):.4f}"]

    for i, line in enumerate(rows):
        ax.text(0.05, 0.97 - i*0.026, line, fontsize=9,
                family="monospace", color="#222")
    _footer(fig, j, run_id, page_num, total, "summary table")
    pdf.savefig(fig); plt.close(fig)


PLATES = [p_cover, p_course_plot, p_hs_trajectory, p_norm_trajectory,
          p_ilr_trajectories, p_polar_rose, p_bearing_heatmap, p_omega,
          p_metric_lines, p_helmsman_lineage, p_helmsman_full,
          p_ring_strip, p_locks, p_var_matrix, p_pair_correlation,
          p_cbs, p_divergence_ranking, p_omega_hs, p_summary]


def render_stage2(pdf, j, dataset_id, run_id, options=None):
    """Render the locked Stage 2 plate book.

    options : optional dict honoured by configurable plates. Currently:
        ternary_triplets: list of triplets that p_ternary_panel will draw
            instead of the default top-3 / rank-2-4 / bottom-3 heuristic.
            Each entry can be either a list of 3 carrier names, or a dict
            {"name": "fossils", "carriers": ["Coal","Gas","Other Fossil"]}.
            Up to 3 triplets are drawn on the panel page.
        biplot_top_n: integer N (default 6). p_biplot_topN keeps only the
            N carriers with the largest 2D loading magnitude — solves
            clutter on high-D datasets.
    """
    ctx = collect(j)
    ctx["_options"] = options or {}
    total = len(PLATES)
    for k, fn in enumerate(PLATES, 1):
        fn(pdf, j, dataset_id, run_id, k, total, ctx)
    return total


# ════════════════════════════════════════════════════════════════
# CoDa-standard plates (reviewer addition, v1.1.x)
# ════════════════════════════════════════════════════════════════

def _coda_palette(n):
    base = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd",
            "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"]
    return [base[i % len(base)] for i in range(n)]


# ── Plate: evolution of proportions (raw + cumulative) ──────────
def p_evolution_proportions(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "Evolution of Proportions  (raw + cumulative)", j)

    inp = j["input"]; ts = j["tensor"]["timesteps"]
    T = inp["n_records"]; D = inp["n_carriers"]
    carriers = inp["carriers"]; labels = inp["labels"]
    palette = _coda_palette(D)
    composition = np.array([t["coda_standard"]["composition"] for t in ts])
    # x-axis: try ints
    def xs():
        try:    return [int(l) for l in labels]
        except: return list(range(T))
    x = xs()

    # Top panel: line plot of proportions per carrier
    ax_top = fig.add_axes([0.07, 0.56, 0.86, 0.34])
    for k in range(D):
        ax_top.plot(x, composition[:, k], "-o", lw=1.4, ms=3.0,
                    color=palette[k], label=carriers[k])
    ax_top.set_xlim(x[0]-0.5, x[-1]+0.5)
    ax_top.set_ylim(0, max(0.5, composition.max()*1.05))
    ax_top.set_ylabel("share  x_k(t)"); ax_top.grid(True, alpha=0.3)
    ax_top.set_title("(top) Per-carrier proportion x_k(t) — Order 1",
                     fontsize=10, color="#1f4e79", loc="left")
    ax_top.legend(fontsize=7, ncol=4, framealpha=0.85, loc="upper left")

    # Bottom panel: stacked area of cumulative proportions
    ax_bot = fig.add_axes([0.07, 0.10, 0.86, 0.40])
    cum = np.zeros(T)
    for k in range(D):
        ax_bot.fill_between(x, cum, cum + composition[:, k],
                            color=palette[k], edgecolor="white",
                            linewidth=0.4, label=carriers[k])
        cum = cum + composition[:, k]
    ax_bot.set_xlim(x[0]-0.5, x[-1]+0.5); ax_bot.set_ylim(0, 1.0)
    ax_bot.set_xlabel("t / year"); ax_bot.set_ylabel("cumulative share")
    ax_bot.set_title("(bot) Cumulative composition (stacked area) — Order 1",
                     fontsize=10, color="#1f4e79", loc="left")

    _footer(fig, j, run_id, page_num, total, "evolution of proportions (raw + cumulative)")
    pdf.savefig(fig); plt.close(fig)


# ── Plate: main ternary diagram (top-3 carriers by mean share) ───
def _draw_ternary(ax, points, labels_xyz, point_colors=None,
                  point_labels=None, title=""):
    """Draw a ternary diagram on ax. points = (N, 3) sub-composition rows."""
    # Triangle vertices
    V = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, math.sqrt(3)/2]])
    # Fill triangle background
    ax.fill(V[:,0], V[:,1], color="#f6f8fb", edgecolor="#1f4e79", lw=1.2)
    # Gridlines (every 0.2)
    for f in np.arange(0.2, 1.0, 0.2):
        # parallel to BC (vary a)
        p1 = V[1]*(1-f) + V[2]*0
        p2 = V[1]*(1-f) + V[2]*f
        # Easier — sample three barycentric lines
    # simple internal gridlines (rasterize-ish)
    for f in [0.2, 0.4, 0.6, 0.8]:
        # points where carrier 0 share = f
        lo = V[0]*f + V[1]*(1-f)
        hi = V[0]*f + V[2]*(1-f)
        ax.plot([lo[0],hi[0]], [lo[1],hi[1]], color="#cbd2e0", lw=0.6)
        # carrier 1 share = f
        lo = V[1]*f + V[0]*(1-f)
        hi = V[1]*f + V[2]*(1-f)
        ax.plot([lo[0],hi[0]], [lo[1],hi[1]], color="#cbd2e0", lw=0.6)
        # carrier 2 share = f
        lo = V[2]*f + V[0]*(1-f)
        hi = V[2]*f + V[1]*(1-f)
        ax.plot([lo[0],hi[0]], [lo[1],hi[1]], color="#cbd2e0", lw=0.6)

    # Vertex labels
    ax.text(V[0,0]-0.04, V[0,1]-0.04, labels_xyz[0],
            ha="right", va="top", fontsize=9, color="#1f4e79", fontweight="bold")
    ax.text(V[1,0]+0.04, V[1,1]-0.04, labels_xyz[1],
            ha="left", va="top", fontsize=9, color="#1f4e79", fontweight="bold")
    ax.text(V[2,0], V[2,1]+0.05, labels_xyz[2],
            ha="center", va="bottom", fontsize=9, color="#1f4e79", fontweight="bold")

    # Plot points
    points = np.asarray(points)
    if points.size == 0:
        return
    pts2d = points @ V    # (N, 2) cartesian
    if point_colors is None:
        point_colors = ["#5dd6ff"] * len(points)
    # trajectory line
    ax.plot(pts2d[:,0], pts2d[:,1], "-", color="#888", lw=0.8, alpha=0.5)
    # scatter coloured by index (time)
    sc = ax.scatter(pts2d[:,0], pts2d[:,1], s=40, c=range(len(pts2d)),
                    cmap="viridis", edgecolor="black", linewidth=0.5,
                    zorder=5)
    # mark first / last
    ax.scatter([pts2d[0,0]], [pts2d[0,1]], s=150, marker="^",
               color="#2ca02c", edgecolor="black", linewidth=0.8,
               zorder=6, label=f"start ({point_labels[0]})" if point_labels else "start")
    ax.scatter([pts2d[-1,0]], [pts2d[-1,1]], s=150, marker="s",
               color="#d62728", edgecolor="black", linewidth=0.8,
               zorder=6, label=f"end ({point_labels[-1]})" if point_labels else "end")

    ax.set_xlim(-0.15, 1.15); ax.set_ylim(-0.10, 1.05)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=10, color="#1f4e79")
    ax.legend(fontsize=7, loc="upper left", framealpha=0.85)


def _topk_subcomposition(composition, k=3):
    """Return indices of the top-k carriers by mean share."""
    means = composition.mean(axis=0)
    return list(np.argsort(-means)[:k])


def _close_subcomposition(composition, idx):
    """Close composition rows over the chosen carrier indices."""
    sub = composition[:, idx]
    sub = sub / np.maximum(sub.sum(axis=1, keepdims=True), 1e-30)
    return sub


def p_ternary_main(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num, "Ternary Diagram (top-3 carriers)", j)

    inp = j["input"]; ts = j["tensor"]["timesteps"]
    T = inp["n_records"]; carriers = inp["carriers"]; labels = inp["labels"]
    composition = np.array([t["coda_standard"]["composition"] for t in ts])

    if inp["n_carriers"] >= 3:
        idx = _topk_subcomposition(composition, 3)
        sub = _close_subcomposition(composition, idx)
        ax = fig.add_axes([0.10, 0.10, 0.82, 0.78])
        _draw_ternary(ax, sub,
                      [carriers[idx[0]], carriers[idx[1]], carriers[idx[2]]],
                      point_labels=labels,
                      title=(f"3-part subcomposition closed over "
                             f"{carriers[idx[0]]}, {carriers[idx[1]]}, "
                             f"{carriers[idx[2]]}\n"
                             f"(remaining {inp['n_carriers']-3} carriers "
                             f"absorbed into closure)"))
        # Add side text with mean shares
        means = composition.mean(axis=0)
        info = ["Top-3 by mean share:",
                f"  {carriers[idx[0]]:<14} {means[idx[0]]*100:5.1f}%",
                f"  {carriers[idx[1]]:<14} {means[idx[1]]*100:5.1f}%",
                f"  {carriers[idx[2]]:<14} {means[idx[2]]*100:5.1f}%",
                "",
                f"T = {T} timesteps",
                f"colour map = time index",
                f"▲ start  ■ end"]
        fig.text(0.04, 0.45, "\n".join(info),
                 fontsize=8, family="monospace", color="#222")
    else:
        fig.text(0.5, 0.5, f"D={inp['n_carriers']} — ternary requires D ≥ 3",
                 ha="center", fontsize=12, color="#d62728")

    _footer(fig, j, run_id, page_num, total, "ternary (top-3)")
    pdf.savefig(fig); plt.close(fig)


# ── Plate: 3 ternary panel of distinct sub-compositions ─────────
def p_ternary_panel(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "Three-Part Subcompositions  (3 ternaries)", j)

    inp = j["input"]; ts = j["tensor"]["timesteps"]
    T = inp["n_records"]; D = inp["n_carriers"]
    carriers = inp["carriers"]; labels = inp["labels"]
    composition = np.array([t["coda_standard"]["composition"] for t in ts])

    if D < 3:
        fig.text(0.5, 0.5, f"D={D} — need D ≥ 3", ha="center",
                 fontsize=12, color="#d62728")
        _footer(fig, j, run_id, page_num, total, "ternary panel"); pdf.savefig(fig); plt.close(fig)
        return

    # ── Resolve triplets ─────────────────────────────────────
    # Priority order:
    #   1. options.ternary_triplets if provided (user-driven from
    #      master_control.json projects[*].options.stage2)
    #   2. fall back to top-3 / rank-2-4 / bottom-3 heuristic
    opts = (ctx.get("_options", {}) or {})
    user_triplets = opts.get("ternary_triplets")
    triplets = []
    source_tag = "default heuristic"
    if user_triplets:
        # Accept either ["A","B","C"] or {"name":..., "carriers":[..]}
        for entry in user_triplets[:3]:
            if isinstance(entry, dict):
                names = entry.get("carriers") or entry.get("triplet")
                tag   = entry.get("name") or "user"
            else:
                names, tag = entry, "user"
            if not names or len(names) < 3:
                continue
            try:
                idx = [carriers.index(n) for n in names[:3]]
                triplets.append((idx, tag))
            except ValueError as ve:
                # Unknown carrier name — fall back to ranked indices and
                # warn in the page banner
                triplets.append(([0, 1, min(2, D-1)],
                                 f"!{tag} (bad name: {ve.args[0]})"))
        source_tag = "user-configured (master_control.json)"

    if not triplets:
        means = composition.mean(axis=0)
        rank = list(np.argsort(-means))
        triplets.append((rank[:3], "top-3"))
        if D >= 4:
            triplets.append((rank[1:4], "rank 2-4"))
        else:
            triplets.append((rank[:3], "top-3 (repeat)"))
        if D >= 5:
            triplets.append((rank[-3:], "bottom-3"))
        else:
            triplets.append(([rank[0], rank[-2], rank[-1]], "top + bottom-2"))
        source_tag = "default heuristic"

    for i, (idx, tag) in enumerate(triplets):
        ax = fig.add_axes([0.04 + i*0.32, 0.18, 0.30, 0.66])
        sub = _close_subcomposition(composition, list(idx))
        _draw_ternary(ax, sub,
                      [carriers[idx[0]][:6], carriers[idx[1]][:6], carriers[idx[2]][:6]],
                      point_labels=labels,
                      title=f"{tag}: {carriers[idx[0]]}, {carriers[idx[1]]}, {carriers[idx[2]]}")

    fig.text(0.5, 0.12,
        "Each ternary closes the chosen 3 carriers; remaining carriers absorbed into closure. "
        "▲ start  ■ end  |  colour map = time index",
        ha="center", fontsize=8, color="#444")
    fig.text(0.5, 0.085,
        f"Triplet source: {source_tag}",
        ha="center", fontsize=8, color="#1f4e79", fontstyle="italic")
    _footer(fig, j, run_id, page_num, total, "ternary panel (three 3-part)")
    pdf.savefig(fig); plt.close(fig)


# ── Plate: scree plot of CLR PCA ────────────────────────────────
def p_scree(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num, "Scree Plot - CLR PCA", j)

    clr_mat = np.asarray(ctx["clr_mat"])
    centred = clr_mat - clr_mat.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(centred, full_matrices=False)
    var = (S**2)
    var = var / max(var.sum(), 1e-30)
    cum = np.cumsum(var)

    ax_l = fig.add_axes([0.10, 0.30, 0.45, 0.55])
    ax_l.bar(np.arange(1, len(var)+1), var, color="#1f4e79", alpha=0.85)
    ax_l.set_xlabel("Principal component"); ax_l.set_ylabel("Variance fraction")
    ax_l.set_title("Per-PC variance (scree)", fontsize=10, color="#1f4e79", loc="left")
    ax_l.grid(True, axis="y", alpha=0.3)

    ax_r = fig.add_axes([0.60, 0.30, 0.34, 0.55])
    ax_r.plot(np.arange(1, len(cum)+1), cum, "-o", color="#d62728")
    ax_r.set_xlabel("PC number"); ax_r.set_ylabel("Cumulative variance")
    ax_r.set_ylim(0, 1.05); ax_r.grid(True, alpha=0.3)
    ax_r.axhline(0.9, color="#999", lw=0.6, ls="--")
    ax_r.axhline(0.95, color="#999", lw=0.6, ls="--")
    ax_r.set_title("Cumulative variance", fontsize=10, color="#1f4e79", loc="left")

    info_lines = ["Per-PC variance contribution:"]
    for i, v in enumerate(var):
        info_lines.append(f"  PC{i+1}: {v*100:5.2f}%   cum {cum[i]*100:5.2f}%")
        if i >= 5: break
    if len(var) > 6:
        info_lines.append(f"  ... {len(var)-6} more PCs")
    fig.text(0.10, 0.05, "\n".join(info_lines),
             fontsize=8, family="monospace", color="#222")
    _footer(fig, j, run_id, page_num, total, "scree (CLR PCA)")
    pdf.savefig(fig); plt.close(fig)


# ── Plate: CLR biplot (CoDa biplot, full) ────────────────────────
def p_biplot(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num, "CLR Biplot  (CoDa biplot)", j)

    inp = j["input"]
    carriers = inp["carriers"]; D = inp["n_carriers"]
    labels = inp["labels"]; T = inp["n_records"]
    clr_mat = np.asarray(ctx["clr_mat"])
    centred = clr_mat - clr_mat.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(centred, full_matrices=False)
    F = U[:, :2] * S[:2]
    G = Vt[:2].T
    var_explained = (S[:2]**2).sum() / max((S**2).sum(), 1e-30)
    fmax = max(np.abs(F).max(), 1e-9); F_n = F / fmax
    gmax = max(np.abs(G).max(), 1e-9); G_n = G / gmax

    ax = fig.add_axes([0.10, 0.10, 0.62, 0.78])
    ax.axhline(0, color="#888", lw=0.5); ax.axvline(0, color="#888", lw=0.5)
    ax.plot(F_n[:,0], F_n[:,1], "-", color="#aaa", lw=0.7, alpha=0.7)
    ax.scatter(F_n[:,0], F_n[:,1], c=range(T), cmap="viridis",
               s=60, edgecolor="black", linewidth=0.4)
    ax.scatter([F_n[0,0]], [F_n[0,1]], s=160, marker="^",
               color="#2ca02c", edgecolor="black", linewidth=0.8, zorder=5,
               label=f"start ({labels[0]})")
    ax.scatter([F_n[-1,0]], [F_n[-1,1]], s=160, marker="s",
               color="#d62728", edgecolor="black", linewidth=0.8, zorder=5,
               label=f"end ({labels[-1]})")
    pal = _coda_palette(D)
    for k in range(D):
        x, y = G_n[k]
        ax.annotate("", xy=(x, y), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=pal[k], lw=1.6))
        ax.text(x*1.10, y*1.10, carriers[k], ha="center",
                fontsize=8, color=pal[k], fontweight="bold")
    ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal")
    ax.set_xlabel(f"PC1  ({S[0]**2/(S**2).sum()*100:.1f}%)")
    ax.set_ylabel(f"PC2  ({S[1]**2/(S**2).sum()*100:.1f}%)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc="upper right", framealpha=0.85)
    ax.set_title(f"CoDa biplot - covariance form, 2D variance explained {var_explained*100:.1f}%",
                 fontsize=10, color="#1f4e79", loc="left")

    info = [
        "CoDa biplot (Aitchison-Greenacre):",
        "  - Points: timestep scores in PC(1,2) of centred CLR.",
        "  - Rays:   carrier loadings (columns of V).",
        "  - Ray length = carrier importance on the 2D plane.",
        "  - Angle between rays ~ negative log-ratio correlation.",
        "  - Distance between point projections = approximation",
        "    of the Aitchison distance restricted to PC(1,2).",
        "",
        f"PC1 captures {S[0]**2/(S**2).sum()*100:.1f}% of variance.",
        f"PC2 captures {S[1]**2/(S**2).sum()*100:.1f}% of variance.",
        f"Total 2D plane:  {var_explained*100:.1f}%",
    ]
    fig.text(0.74, 0.86, "\n".join(info), fontsize=8, family="monospace",
             color="#222", verticalalignment="top")

    _footer(fig, j, run_id, page_num, total, "CLR biplot (full)")
    pdf.savefig(fig); plt.close(fig)


# ── Plate: top-N biplot (clutter-free CoDa biplot for high-D) ────
def p_biplot_topN(pdf, j, dataset_id, run_id, page_num, total, ctx):
    """Same PCA as p_biplot but draws only the top-N carriers ranked
    by 2D loading magnitude. Score points are unchanged. Useful for
    D ≥ 8 where the full biplot's rays compete for the same plane."""
    inp = j["input"]
    carriers = inp["carriers"]; D = inp["n_carriers"]
    labels = inp["labels"]; T = inp["n_records"]
    opts = (ctx.get("_options", {}) or {})
    N = int(opts.get("biplot_top_n", 6))

    # Compute the same PCA as p_biplot
    clr_mat = np.asarray(ctx["clr_mat"])
    centred = clr_mat - clr_mat.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(centred, full_matrices=False)
    F = U[:, :2] * S[:2]
    G = Vt[:2].T
    var_explained = (S[:2]**2).sum() / max((S**2).sum(), 1e-30)
    fmax = max(np.abs(F).max(), 1e-9); F_n = F / fmax
    gmax = max(np.abs(G).max(), 1e-9); G_n = G / gmax

    # Loading magnitude (2D plane only)
    mag = np.sqrt(G[:, 0]**2 + G[:, 1]**2)
    rank = list(np.argsort(-mag))      # descending
    keep = rank[:max(3, min(N, D))]
    drop = rank[len(keep):]

    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           f"CLR Biplot — top-{len(keep)} carriers by loading magnitude", j)

    if D <= N:
        fig.text(0.5, 0.5,
                 f"D = {D} ≤ N = {N} — full biplot already shows every carrier "
                 "(see preceding plate). This page is informational.",
                 ha="center", fontsize=11, color="#1f4e79", wrap=True)
        _footer(fig, j, run_id, page_num, total, "top-N biplot (skipped)")
        pdf.savefig(fig); plt.close(fig)
        return

    ax = fig.add_axes([0.10, 0.10, 0.62, 0.78])
    ax.axhline(0, color="#888", lw=0.5); ax.axvline(0, color="#888", lw=0.5)
    ax.plot(F_n[:,0], F_n[:,1], "-", color="#aaa", lw=0.7, alpha=0.7)
    ax.scatter(F_n[:,0], F_n[:,1], c=range(T), cmap="viridis",
               s=60, edgecolor="black", linewidth=0.4)
    ax.scatter([F_n[0,0]], [F_n[0,1]], s=160, marker="^",
               color="#2ca02c", edgecolor="black", linewidth=0.8, zorder=5,
               label=f"start ({labels[0]})")
    ax.scatter([F_n[-1,0]], [F_n[-1,1]], s=160, marker="s",
               color="#d62728", edgecolor="black", linewidth=0.8, zorder=5,
               label=f"end ({labels[-1]})")

    pal = _coda_palette(D)
    for k in keep:
        x, y = G_n[k]
        ax.annotate("", xy=(x, y), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=pal[k], lw=1.8))
        ax.text(x*1.10, y*1.10, carriers[k], ha="center",
                fontsize=8, color=pal[k], fontweight="bold")

    # Faint stubs for dropped carriers
    for k in drop:
        x, y = G_n[k]
        ax.annotate("", xy=(x*0.55, y*0.55), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-", color=pal[k],
                                    lw=0.6, alpha=0.35))

    ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal")
    ax.set_xlabel(f"PC1  ({S[0]**2/(S**2).sum()*100:.1f}%)")
    ax.set_ylabel(f"PC2  ({S[1]**2/(S**2).sum()*100:.1f}%)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc="upper right", framealpha=0.85)
    ax.set_title(f"Top-{len(keep)} biplot — 2D variance {var_explained*100:.1f}%  "
                 f"(D = {D}, dropped {len(drop)} short rays)",
                 fontsize=10, color="#1f4e79", loc="left")

    # Side: ranking table
    info = ["Loading magnitudes √(G₁² + G₂²):", ""]
    for k in keep:
        info.append(f"  ✚ {carriers[k]:<14} {mag[k]:.4f}")
    if drop:
        info.append("")
        info.append(f"Dropped (faint stubs only):")
        for k in drop:
            info.append(f"    {carriers[k]:<14} {mag[k]:.4f}")
    fig.text(0.74, 0.86, "\n".join(info), fontsize=8, family="monospace",
             color="#222", verticalalignment="top")

    _footer(fig, j, run_id, page_num, total,
            f"top-{len(keep)} biplot (configurable via biplot_top_n)")
    pdf.savefig(fig); plt.close(fig)


# ── Plate: balance-dendrogram ───────────────────────────────────
def _hierarchical_sbp(var_mat, carriers):
    """Build an SBP via Ward hierarchical clustering on the variation matrix.

    Returns:
      Z          : scipy linkage matrix (n-1, 4)
      sbp        : (D, D-1) integer matrix; column k is partition k
                   (+1 numerator, -1 denominator, 0 not in this balance)
    """
    from scipy.cluster.hierarchy import linkage
    from scipy.spatial.distance import squareform
    D = len(carriers)
    # Symmetrise the variation matrix (ensure non-negative diagonal-zero)
    M = (var_mat + var_mat.T) / 2.0
    np.fill_diagonal(M, 0.0)
    M = np.maximum(M, 0.0)
    cond = squareform(M, checks=False)
    Z = linkage(cond, method="ward")

    # Build SBP from the merge tree
    # leaves: 0..D-1, internal nodes: D..2D-2
    members = {i: [i] for i in range(D)}
    sbp = np.zeros((D, D-1), dtype=int)
    for k, (a, b, *_rest) in enumerate(Z):
        a, b = int(a), int(b)
        left  = members[a]
        right = members[b]
        for c in left:  sbp[c, k] = +1
        for c in right: sbp[c, k] = -1
        members[D + k] = left + right
    return Z, sbp


def p_balance_dendrogram(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "Balance-Dendrogram  (Ward on variation matrix)", j)

    inp = j["input"]
    carriers = inp["carriers"]; D = inp["n_carriers"]
    var_mat = np.asarray(ctx["var_mat"])
    try:
        from scipy.cluster.hierarchy import dendrogram
    except ImportError:
        fig.text(0.5, 0.5, "scipy not available — cannot draw dendrogram",
                 ha="center", fontsize=12, color="#d62728")
        _footer(fig, j, run_id, page_num, total, "balance dendrogram"); pdf.savefig(fig); plt.close(fig)
        return

    Z, sbp = _hierarchical_sbp(var_mat, carriers)
    ctx["sbp"] = sbp     # stash for SBP-table plate
    ctx["sbp_Z"] = Z

    ax_d = fig.add_axes([0.10, 0.20, 0.65, 0.68])
    dendrogram(Z, labels=carriers, leaf_rotation=30, leaf_font_size=8,
               color_threshold=0, above_threshold_color="#1f4e79",
               ax=ax_d)
    ax_d.set_ylabel("Ward distance (variation matrix)")
    ax_d.set_title(
        "Hierarchical balance tree — each merge defines one balance partition",
        fontsize=10, color="#1f4e79", loc="left")
    ax_d.grid(True, axis="y", alpha=0.3)

    # Side: explanation
    info = [
        "Balance-dendrogram (Pawlowsky-Glahn-Egozcue):",
        "  – Ward clustering on the (symmetrised) variation matrix.",
        "  – Each internal node merges two carrier sets, A | B.",
        "  – That merge defines a balance:",
        "       b = sqrt(|A||B|/(|A|+|B|)) · ln( g(A) / g(B) )",
        "    where g() is the geometric mean.",
        "  – The balances form an orthonormal ILR basis (one per merge).",
        "",
        f"D = {D} carriers → D-1 = {D-1} balances.",
        "Tightly-clustered carriers (low variation) merge first.",
        "See companion plate for the full SBP matrix.",
    ]
    fig.text(0.78, 0.86, "\n".join(info), fontsize=8, family="monospace",
             color="#222", verticalalignment="top")

    _footer(fig, j, run_id, page_num, total, "balance dendrogram (Ward / variation)")
    pdf.savefig(fig); plt.close(fig)


# ── Plate: SBP matrix table ─────────────────────────────────────
def p_sbp_table(pdf, j, dataset_id, run_id, page_num, total, ctx):
    fig = plt.figure(figsize=PAGE_SIZE, dpi=PDF_DPI)
    _title(fig, dataset_id, page_num,
           "Sequential Binary Partition (SBP) Matrix", j)

    inp = j["input"]
    carriers = inp["carriers"]; D = inp["n_carriers"]
    if "sbp" in ctx:
        sbp = ctx["sbp"]
    else:
        var_mat = np.asarray(ctx["var_mat"])
        _, sbp = _hierarchical_sbp(var_mat, carriers)
        ctx["sbp"] = sbp

    ax = fig.add_axes([0.06, 0.10, 0.82, 0.80])
    ax.set_xlim(-0.5, sbp.shape[1]+0.5); ax.set_ylim(-0.5, D+0.5)
    ax.invert_yaxis()
    for k in range(sbp.shape[1]):
        ax.text(k, -0.1, f"b{k+1}", ha="center", va="bottom",
                fontsize=9, fontweight="bold", color="#1f4e79")
    for i in range(D):
        ax.text(-0.7, i+0.4, carriers[i], ha="right", va="center",
                fontsize=9, family="monospace", color="#222")
    for i in range(D):
        for k in range(sbp.shape[1]):
            v = int(sbp[i, k])
            if v > 0:   col = "#2ca02c"; sym = "+"
            elif v < 0: col = "#d62728"; sym = "-"
            else:       col = "#dddddd"; sym = "."
            ax.add_patch(plt.Rectangle((k-0.42, i+0.05), 0.84, 0.85,
                         facecolor=col, alpha=0.25, edgecolor=col, linewidth=0.5))
            ax.text(k, i+0.48, sym, ha="center", va="center",
                    fontsize=14, color=col, fontweight="bold")
    ax.axis("off")
    ax.set_title("SBP cells: + = numerator, - = denominator, . = not in this balance",
                 fontsize=10, color="#1f4e79", loc="left")
    fig.text(0.06, 0.06,
             "Balance b_k = sqrt(|A_k||B_k|/(|A_k|+|B_k|)) * ln( g(A_k) / g(B_k) ) "
             f"  |  D = {D}; D-1 = {sbp.shape[1]} balances.",
             fontsize=8, family="monospace", color="#444")

    _footer(fig, j, run_id, page_num, total, "SBP matrix")
    pdf.savefig(fig); plt.close(fig)


# ════════════════════════════════════════════════════════════════
# Canonical PLATES order (overrides any earlier PLATES = ... above).
# Reading order: cover -> data disclosure -> geometry (basic to
# advanced) -> dynamics (basic to advanced) -> summary.
# ════════════════════════════════════════════════════════════════
PLATES = [
    # §1  Cover + data disclosure
    p_cover,
    p_data_disclosure,

    # §B  GEOMETRY  (structure on the simplex; basic to advanced)
    p_evolution_proportions,    # raw + cumulative shares
    p_ternary_main,             # canonical top-3 ternary
    p_ternary_panel,            # 3 sub-compositions
    p_var_matrix,               # pairwise log-ratio variances
    p_pair_correlation,         # Pearson r per pair
    p_scree,                    # PCA variance per PC
    p_biplot,                   # full CoDa biplot
    p_biplot_topN,              # clutter-free top-N (high-D)
    p_balance_dendrogram,       # Ward hierarchy
    p_sbp_table,                # SBP matrix

    # §C  DYNAMICS (evolution through compositional space; basic to advanced)
    p_hs_trajectory,            # Hs(t) — basic
    p_norm_trajectory,          # ||clr||(t)
    p_ilr_trajectories,         # first 3 ILR axes vs t
    p_course_plot,              # System Course Plot (PCA path with V_net)
    p_polar_rose,               # bearing distribution
    p_bearing_heatmap,          # pair x time
    p_omega,                    # angular velocity per inter-step
    p_metric_lines,             # metric trace + condition number
    p_helmsman_lineage,         # per-step helmsman
    p_helmsman_full,            # frequency + transitions + displacement
    p_ring_strip,               # IR-class banding + Hs
    p_locks,                    # period-2 lock events timeline
    p_cbs,                      # CBS three orthogonal faces
    p_divergence_ranking,       # top-15 pairwise divergences
    p_omega_hs,                 # phase plot

    # §D  Summary
    p_summary,
]
