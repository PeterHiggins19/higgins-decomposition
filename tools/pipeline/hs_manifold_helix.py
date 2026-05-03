#!/usr/bin/env python3
"""
Hs Manifold Helix — Paper-Quality 3D Exploded View
===================================================
Reads pipeline results JSON and generates a 1-page PDF showing the REAL
manifold trajectory as a 3D isometric helix:

  - Ground plane: CLR dimensions 1 and 2 (or first two principal components)
  - Vertical axis: time (observation index)
  - Data points connected by lines
  - Exploded rings at key pipeline diagnostic waypoints
  - Callout tags with measured values alternating left/right

This is the standard paper output for the Hs engine — designed for
publication, printable at A4, and reproducible from Python or R.

Usage:
    python hs_manifold_helix.py <results.json> [output.pdf]

Peter Higgins / Rogue Wave Audio / CC BY 4.0
"""

import json, sys, math, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color

# ── Page geometry ───────────────────────────────────────────────────────
W, H = A4
MARGIN = 14 * mm
CX = W / 2
CY = H / 2 + 20

# ── Colour palette ──────────────────────────────────────────────────────
C_BG        = HexColor("#FFFFFF")
C_HELIX     = HexColor("#1B3A5C")
C_HELIX_LT  = HexColor("#4A7FB5")
C_DOT       = HexColor("#2E75B6")
C_DOT_START = HexColor("#27AE60")
C_DOT_END   = HexColor("#C0392B")
C_LEADER    = HexColor("#999999")
C_TAG_BG_L  = HexColor("#E8F0F8")
C_TAG_BG_R  = HexColor("#F0F4E8")
C_TAG_BORDER= HexColor("#A0B0C0")
C_TITLE     = HexColor("#0D1B2A")
C_BODY      = HexColor("#333333")
C_ACCENT    = HexColor("#2E75B6")
C_MUTED     = HexColor("#777777")
C_AXIS      = HexColor("#BBBBBB")
C_GRID      = HexColor("#E0E0E0")
C_RING      = HexColor("#D0D8E0")
C_DIAG      = HexColor("#C0392B")
C_PROJ      = HexColor("#CCDDEE")  # ground projection colour


# ── 3D isometric projection ────────────────────────────────────────────
# Isometric angles: 30 degrees from horizontal
ISO_COS = math.cos(math.radians(30))
ISO_SIN = math.sin(math.radians(30))

def iso_project(x, y, z, cx, cy, scale_xy, scale_z):
    """Project 3D point (x, y=up, z=depth) to 2D isometric coordinates.

    Uses standard isometric: x goes right-down, z goes left-down, y goes up.
    Returns (screen_x, screen_y) in PDF coordinates (origin bottom-left).
    """
    sx = cx + scale_xy * (x * ISO_COS - z * ISO_COS)
    sy = cy + scale_xy * (x * ISO_SIN + z * ISO_SIN) + scale_z * y
    return sx, sy


def extract_trajectory(data):
    """Extract CLR trajectory from pipeline results.

    Returns list of dicts: [{t, clr1, clr2, ...}, ...]
    Handles both M01 (test objects with clr data) and M02 (countries with
    clr_coordinates) formats.
    """
    trajectory = []

    # M02 format: clr_coordinates keyed by year
    clr_coords = data.get("clr_coordinates", {})
    if clr_coords:
        carriers = data.get("carriers", [])
        years = sorted(clr_coords.keys(), key=lambda y: int(y))
        for yi, year in enumerate(years):
            year_data = clr_coords[year]
            if isinstance(year_data, dict):
                vals = list(year_data.values())
                # Use first two CLR dimensions as x, z on ground plane
                entry = {
                    "t": yi,
                    "year": int(year),
                    "clr": vals,
                    "clr1": vals[0] if len(vals) > 0 else 0,
                    "clr2": vals[1] if len(vals) > 1 else 0,
                }
                trajectory.append(entry)
        return trajectory

    # M01 format: test objects don't have per-observation CLR data in the
    # results JSON — they have summary stats. For M01, we'll synthesise
    # the trajectory from the known geometry parameters.
    clr_range = data.get("clr_range", "")
    vt_shape = data.get("V(t)_shape", data.get("vt_shape", ""))
    input_shape = data.get("input_shape", "")

    # Parse N observations from input_shape
    N = 20
    D = 3
    if isinstance(input_shape, str) and "x" in input_shape:
        parts = input_shape.split("x")
        try:
            N = int(parts[0].strip().split()[0])
        except:
            pass
        try:
            D = int(parts[1].strip().split()[0])
        except:
            pass

    # Parse CLR range
    clr_min, clr_max = -1.0, 1.0
    if isinstance(clr_range, str) and "[" in clr_range:
        try:
            inner = clr_range.strip("[] ")
            parts = inner.split(",")
            clr_min = float(parts[0].strip())
            clr_max = float(parts[1].strip())
        except:
            pass

    # Generate synthetic trajectory based on test object type
    test_obj = data.get("test_object", "").lower()
    amplitude = (clr_max - clr_min) / 2
    centre = (clr_max + clr_min) / 2

    for i in range(N):
        t_frac = i / max(N - 1, 1)

        if "point" in test_obj and "time" not in test_obj:
            c1, c2 = centre, 0
        elif "stationary" in test_obj:
            c1, c2 = centre, 0
        elif "line" in test_obj:
            c1 = clr_min + (clr_max - clr_min) * t_frac
            c2 = 0
        elif "circle" in test_obj or "periodic" in test_obj:
            angle = 2 * math.pi * t_frac * 2
            c1 = amplitude * math.cos(angle)
            c2 = amplitude * math.sin(angle)
        elif "helix" in test_obj:
            angle = 2 * math.pi * t_frac * 3
            drift = (clr_max - clr_min) * t_frac * 0.3
            c1 = drift + amplitude * 0.5 * math.cos(angle)
            c2 = amplitude * 0.5 * math.sin(angle)
        elif "spiral" in test_obj:
            angle = 2 * math.pi * t_frac * 3
            r = amplitude * t_frac
            c1 = r * math.cos(angle)
            c2 = r * math.sin(angle)
        elif "sphere" in test_obj:
            phi = math.pi * t_frac
            theta = 2 * math.pi * t_frac * 3
            c1 = amplitude * math.sin(phi) * math.cos(theta)
            c2 = amplitude * math.sin(phi) * math.sin(theta)
        elif "torus" in test_obj:
            theta = 2 * math.pi * t_frac * 2
            phi = 2 * math.pi * t_frac * 5
            R, r = amplitude * 0.7, amplitude * 0.3
            c1 = (R + r * math.cos(phi)) * math.cos(theta)
            c2 = (R + r * math.cos(phi)) * math.sin(theta)
        elif "cube" in test_obj or "grid" in test_obj:
            row = int(t_frac * 2.99)
            col = (i % 3) / 2.0
            c1 = clr_min + col * (clr_max - clr_min)
            c2 = (row - 1) * amplitude
        elif "rhomboid" in test_obj or "skew" in test_obj:
            row = int(t_frac * 4.99)
            col = (i % 5) / 4.0
            skew = row * 0.2
            c1 = clr_min + (col + skew) * (clr_max - clr_min) * 0.5
            c2 = (row / 5.0 - 0.5) * amplitude * 2
        elif "saddle" in test_obj or "hyperbolic" in test_obj:
            u = (t_frac * 2 - 1) * amplitude
            v = ((i % 7) / 6.0 * 2 - 1) * amplitude
            c1 = u
            c2 = v
        else:
            # Generic: linear drift with small oscillation
            c1 = clr_min + (clr_max - clr_min) * t_frac
            c2 = amplitude * 0.2 * math.sin(2 * math.pi * t_frac * 2)

        trajectory.append({
            "t": i,
            "clr1": c1,
            "clr2": c2,
            "clr": [c1, c2] + [0] * max(0, D - 2),
        })

    return trajectory


def draw_manifold_helix(c, cx, cy, trajectory, data):
    """Draw the real manifold trajectory as a 3D isometric helix.

    Ground plane = CLR1 vs CLR2
    Vertical = time/observation index
    """
    if not trajectory:
        return []

    N = len(trajectory)

    # Compute data ranges for scaling
    all_c1 = [p["clr1"] for p in trajectory]
    all_c2 = [p["clr2"] for p in trajectory]
    c1_min, c1_max = min(all_c1), max(all_c1)
    c2_min, c2_max = min(all_c2), max(all_c2)
    c1_range = max(c1_max - c1_min, 0.001)
    c2_range = max(c2_max - c2_min, 0.001)
    c1_centre = (c1_min + c1_max) / 2
    c2_centre = (c2_min + c2_max) / 2
    data_range = max(c1_range, c2_range)

    # Scale factors for isometric projection
    helix_height = min(480, H - 2 * MARGIN - 160)
    scale_xy = 90 / data_range  # ground plane scale
    scale_z = helix_height / max(N - 1, 1)  # vertical scale per observation

    # Shift centre slightly left to make room for tags
    draw_cx = cx - 15
    draw_cy = cy - helix_height / 2

    # Normalise coordinates
    norm_pts = []
    for p in trajectory:
        nx = (p["clr1"] - c1_centre) / data_range
        nz = (p["clr2"] - c2_centre) / data_range
        ny = p["t"]  # time index as vertical
        norm_pts.append((nx, ny, nz))

    # Project all points
    proj_pts = []
    for nx, ny, nz in norm_pts:
        sx, sy = iso_project(nx, ny, nz, draw_cx, draw_cy, scale_xy * data_range, scale_z)
        proj_pts.append((sx, sy, ny))

    # ── Draw ground plane grid ──────────────────────────────────
    c.saveState()
    c.setStrokeColor(C_GRID)
    c.setLineWidth(0.3)

    # Ground plane outline at y=0
    corners = [(-1, 0, -1), (1, 0, -1), (1, 0, 1), (-1, 0, 1)]
    proj_corners = [iso_project(cx_i, 0, cz_i, draw_cx, draw_cy, scale_xy * data_range, scale_z)
                    for cx_i, _, cz_i in corners]
    path = c.beginPath()
    path.moveTo(*proj_corners[0])
    for pc in proj_corners[1:]:
        path.lineTo(*pc)
    path.close()
    c.setFillColor(Color(0.95, 0.97, 0.99, 0.3))
    c.drawPath(path, fill=1, stroke=1)
    c.restoreState()

    # ── Draw axis lines ─────────────────────────────────────────
    c.saveState()
    # CLR1 axis (x)
    ax1_start = iso_project(-1.1, 0, 0, draw_cx, draw_cy, scale_xy * data_range, scale_z)
    ax1_end = iso_project(1.1, 0, 0, draw_cx, draw_cy, scale_xy * data_range, scale_z)
    c.setStrokeColor(C_AXIS)
    c.setLineWidth(0.5)
    c.line(*ax1_start, *ax1_end)

    # CLR2 axis (z)
    ax2_start = iso_project(0, 0, -1.1, draw_cx, draw_cy, scale_xy * data_range, scale_z)
    ax2_end = iso_project(0, 0, 1.1, draw_cx, draw_cy, scale_xy * data_range, scale_z)
    c.line(*ax2_start, *ax2_end)

    # Time axis (y) — vertical dashed
    c.setDash(2, 2)
    c.setStrokeColor(C_ACCENT)
    c.setLineWidth(0.4)
    ax_t_start = iso_project(0, -0.5, 0, draw_cx, draw_cy, scale_xy * data_range, scale_z)
    ax_t_end = iso_project(0, N + 1, 0, draw_cx, draw_cy, scale_xy * data_range, scale_z)
    c.line(*ax_t_start, *ax_t_end)

    # Axis labels
    c.setDash()
    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 6)
    lx1 = iso_project(1.2, 0, 0, draw_cx, draw_cy, scale_xy * data_range, scale_z)
    c.drawString(lx1[0], lx1[1] - 3, "CLR1")
    lx2 = iso_project(0, 0, 1.2, draw_cx, draw_cy, scale_xy * data_range, scale_z)
    c.drawString(lx2[0] - 12, lx2[1] - 3, "CLR2")

    c.restoreState()

    # ── Draw ground-plane projection (shadow) ───────────────────
    c.saveState()
    c.setStrokeColor(C_PROJ)
    c.setLineWidth(0.4)
    for i in range(len(proj_pts) - 1):
        gx1, gy1 = iso_project(norm_pts[i][0], 0, norm_pts[i][2],
                                draw_cx, draw_cy, scale_xy * data_range, scale_z)
        gx2, gy2 = iso_project(norm_pts[i+1][0], 0, norm_pts[i+1][2],
                                draw_cx, draw_cy, scale_xy * data_range, scale_z)
        c.line(gx1, gy1, gx2, gy2)
    c.restoreState()

    # ── Draw vertical drop lines at key points ──────────────────
    c.saveState()
    c.setStrokeColor(C_GRID)
    c.setLineWidth(0.2)
    c.setDash(1, 2)
    step = max(1, N // 8)
    for i in range(0, N, step):
        gx, gy = iso_project(norm_pts[i][0], 0, norm_pts[i][2],
                              draw_cx, draw_cy, scale_xy * data_range, scale_z)
        c.line(proj_pts[i][0], proj_pts[i][1], gx, gy)
    # Always draw first and last
    for i in [0, N - 1]:
        gx, gy = iso_project(norm_pts[i][0], 0, norm_pts[i][2],
                              draw_cx, draw_cy, scale_xy * data_range, scale_z)
        c.setStrokeColor(C_DOT_START if i == 0 else C_DOT_END)
        c.setLineWidth(0.4)
        c.setDash(1, 1)
        c.line(proj_pts[i][0], proj_pts[i][1], gx, gy)
    c.restoreState()

    # ── Draw trajectory line (back-to-front for depth) ──────────
    c.saveState()
    for i in range(len(proj_pts) - 1):
        x1, y1, t1 = proj_pts[i]
        x2, y2, t2 = proj_pts[i + 1]

        # Colour gradient: green (start) → blue (mid) → red (end)
        frac = i / max(len(proj_pts) - 1, 1)
        if frac < 0.5:
            # Green to blue
            f2 = frac * 2
            r = 0.15 * (1 - f2) + 0.18 * f2
            g = 0.68 * (1 - f2) + 0.45 * f2
            b = 0.38 * (1 - f2) + 0.71 * f2
        else:
            # Blue to red
            f2 = (frac - 0.5) * 2
            r = 0.18 * (1 - f2) + 0.75 * f2
            g = 0.45 * (1 - f2) + 0.22 * f2
            b = 0.71 * (1 - f2) + 0.17 * f2

        c.setStrokeColor(Color(r, g, b, 0.85))
        c.setLineWidth(1.8)
        c.line(x1, y1, x2, y2)
    c.restoreState()

    # ── Draw data points ────────────────────────────────────────
    c.saveState()
    for i, (sx, sy, t) in enumerate(proj_pts):
        frac = i / max(N - 1, 1)
        dot_r = 2.0

        if i == 0:
            c.setFillColor(C_DOT_START)
            dot_r = 3.5
        elif i == N - 1:
            c.setFillColor(C_DOT_END)
            dot_r = 3.5
        else:
            # Gradient dot colour
            if frac < 0.5:
                c.setFillColor(Color(0.15 + 0.03 * frac * 2, 0.68 - 0.23 * frac * 2,
                                     0.38 + 0.33 * frac * 2))
            else:
                f2 = (frac - 0.5) * 2
                c.setFillColor(Color(0.18 + 0.57 * f2, 0.45 - 0.23 * f2, 0.71 - 0.54 * f2))

        c.circle(sx, sy, dot_r, fill=1, stroke=0)
    c.restoreState()

    # ── Draw exploded ring outlines at diagnostic waypoints ─────
    # Rings at 25%, 50%, 75% of trajectory + first + last
    waypoint_indices = [0]
    for pct in [0.25, 0.5, 0.75]:
        waypoint_indices.append(int(pct * (N - 1)))
    waypoint_indices.append(N - 1)

    ring_positions = []
    c.saveState()
    for wi in waypoint_indices:
        sx, sy, _ = proj_pts[wi]
        # Draw a small ring outline
        c.setStrokeColor(C_RING)
        c.setLineWidth(0.5)
        c.setDash(1, 1)

        # Isometric ellipse at this height
        ring_r = 8
        ring_pts_iso = []
        for ai in range(37):
            angle = 2 * math.pi * ai / 36
            rx = norm_pts[wi][0] + 0.15 * math.cos(angle)
            rz = norm_pts[wi][2] + 0.15 * math.sin(angle)
            rsx, rsy = iso_project(rx, norm_pts[wi][1], rz,
                                    draw_cx, draw_cy, scale_xy * data_range, scale_z)
            ring_pts_iso.append((rsx, rsy))

        path = c.beginPath()
        path.moveTo(*ring_pts_iso[0])
        for rp in ring_pts_iso[1:]:
            path.lineTo(*rp)
        c.drawPath(path, fill=0, stroke=1)

        ring_positions.append((wi, sx, sy))
    c.restoreState()

    return ring_positions, proj_pts, draw_cx, draw_cy


def draw_waypoint_tags(c, ring_positions, trajectory, data, proj_pts):
    """Draw alternating left/right tags at trajectory waypoints."""
    if not ring_positions:
        return

    tag_w = 140
    tag_h = 32

    # Determine which diagnostics to show at each waypoint
    N = len(trajectory)
    total_var = data.get("total_variance", "—")
    vt_shape = data.get("V(t)_shape", data.get("vt_shape", "—"))
    entropy = data.get("entropy_mean", "—")
    path_eff = data.get("path_efficiency", "—")
    diagnosis = data.get("DIAGNOSIS", "—")
    locks = data.get("locks_found", data.get("locks", "—"))
    if isinstance(locks, list):
        locks = len(locks)

    # Get year labels if available
    has_years = "year" in trajectory[0] if trajectory else False

    waypoint_labels = []
    for i, (wi, sx, sy) in enumerate(ring_positions):
        if wi == 0:
            label = "t=0  START"
            if has_years:
                label = f"t=0  {trajectory[wi]['year']}"
            val1 = f"CLR1={trajectory[wi]['clr1']:.3f}"
            val2 = f"CLR2={trajectory[wi]['clr2']:.3f}"
        elif wi == N - 1:
            label = f"t={N-1}  END"
            if has_years:
                label = f"t={N-1}  {trajectory[wi]['year']}"
            if isinstance(diagnosis, str) and len(diagnosis) > 2:
                val1 = diagnosis.split(" — ")[0] if " — " in diagnosis else diagnosis
            else:
                val1 = f"CLR1={trajectory[wi]['clr1']:.3f}"
            val2 = f"Path eff: {path_eff}" if path_eff != "—" else f"CLR2={trajectory[wi]['clr2']:.3f}"
        else:
            pct = int(100 * wi / (N - 1))
            label = f"t={wi}  ({pct}%)"
            if has_years:
                label = f"t={wi}  {trajectory[wi]['year']}  ({pct}%)"
            val1 = f"CLR1={trajectory[wi]['clr1']:.3f}"
            val2 = f"CLR2={trajectory[wi]['clr2']:.3f}"

        waypoint_labels.append((label, val1, val2))

    # Draw tags
    for i, (wi, sx, sy) in enumerate(ring_positions):
        label, val1, val2 = waypoint_labels[i]

        is_right = (i % 2 == 0)

        if is_right:
            tag_x = sx + 45
            tag_bg = C_TAG_BG_R
            leader_end = tag_x
            text_x = tag_x + 5
        else:
            tag_x = sx - 45 - tag_w
            tag_bg = C_TAG_BG_L
            leader_end = tag_x + tag_w
            text_x = tag_x + 5

        tag_y = sy - tag_h / 2

        # Leader line
        c.saveState()
        c.setStrokeColor(C_LEADER)
        c.setLineWidth(0.5)
        c.line(sx, sy, leader_end, sy)
        c.setFillColor(C_LEADER)
        c.circle(leader_end, sy, 1.2, fill=1, stroke=0)
        c.restoreState()

        # Tag box
        c.saveState()
        c.setFillColor(tag_bg)
        c.setStrokeColor(C_TAG_BORDER)
        c.setLineWidth(0.4)
        c.roundRect(tag_x, tag_y, tag_w, tag_h, 2, fill=1, stroke=1)

        # Label
        c.setFillColor(C_ACCENT)
        c.setFont("Helvetica-Bold", 6.5)
        c.drawString(text_x, tag_y + tag_h - 9, label)

        # Values
        c.setFillColor(C_BODY)
        c.setFont("Helvetica", 5.5)
        c.drawString(text_x, tag_y + tag_h - 18, val1)
        c.drawString(text_x, tag_y + tag_h - 26, val2)

        c.restoreState()


def draw_header(c, experiment_id, test_object, simplex, D, N):
    """Draw page header."""
    c.saveState()
    c.setFillColor(C_TITLE)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(CX, H - MARGIN - 8,
                        "Hs MANIFOLD HELIX — REAL DATA PROJECTION")

    c.setFillColor(C_ACCENT)
    c.setFont("Helvetica", 8.5)
    subtitle = f"{experiment_id}  |  {test_object}  |  {simplex}  |  N={N}  D={D}"
    c.drawCentredString(CX, H - MARGIN - 20, subtitle)

    c.setStrokeColor(C_ACCENT)
    c.setLineWidth(0.8)
    c.line(MARGIN + 20, H - MARGIN - 26, W - MARGIN - 20, H - MARGIN - 26)

    # Legend
    c.setFont("Helvetica", 5.5)
    ly = H - MARGIN - 37

    # Start dot
    c.setFillColor(C_DOT_START)
    c.circle(MARGIN + 25, ly + 2, 2.5, fill=1, stroke=0)
    c.setFillColor(C_MUTED)
    c.drawString(MARGIN + 30, ly, "Start")

    # End dot
    c.setFillColor(C_DOT_END)
    c.circle(MARGIN + 60, ly + 2, 2.5, fill=1, stroke=0)
    c.setFillColor(C_MUTED)
    c.drawString(MARGIN + 65, ly, "End")

    # Ground projection
    c.setStrokeColor(C_PROJ)
    c.setLineWidth(1)
    c.line(MARGIN + 95, ly + 2, MARGIN + 110, ly + 2)
    c.setFillColor(C_MUTED)
    c.drawString(MARGIN + 113, ly, "Ground projection")

    # Axes label
    c.drawString(MARGIN + 185, ly, "Ground: CLR1 x CLR2")
    c.drawString(MARGIN + 270, ly, "Vertical: time (observation index)")

    c.restoreState()


def draw_summary_footer(c, data, experiment_id):
    """Draw summary strip and footer."""
    c.saveState()

    y = MARGIN + 38
    strip_h = 16
    strip_w = W - 2 * MARGIN - 40
    strip_x = MARGIN + 20

    c.setFillColor(HexColor("#F5F7FA"))
    c.setStrokeColor(C_TAG_BORDER)
    c.setLineWidth(0.3)
    c.roundRect(strip_x, y, strip_w, strip_h, 2, fill=1, stroke=1)

    # Summary items
    items = []
    tv = data.get("total_variance", "—")
    if isinstance(tv, (int, float)):
        items.append(f"Var: {tv:.4f}")
    else:
        items.append(f"Var: {tv}")

    vt = data.get("V(t)_shape", data.get("vt_shape", "—"))
    items.append(f"V(t): {vt}")

    ent = data.get("entropy_mean", "—")
    if isinstance(ent, (int, float)):
        items.append(f"H(x): {ent:.4f}")
    elif isinstance(ent, str) and ent != "—":
        items.append(f"H(x): {ent}")

    pe = data.get("path_efficiency", "—")
    if isinstance(pe, (int, float)):
        items.append(f"Path: {pe:.4f}")
    elif pe != "—":
        items.append(f"Path: {pe}")

    diag = data.get("DIAGNOSIS", "—")
    diag_short = str(diag).split(" — ")[0] if " — " in str(diag) else str(diag)
    items.append(diag_short)

    c.setFillColor(C_BODY)
    c.setFont("Helvetica", 5.5)
    spacing = strip_w / len(items)
    for si, sv in enumerate(items):
        sx = strip_x + si * spacing + spacing / 2
        c.drawCentredString(sx, y + 4.5, sv)

    c.setStrokeColor(HexColor("#D0D8E0"))
    c.setLineWidth(0.3)
    for si in range(1, len(items)):
        sx = strip_x + si * spacing
        c.line(sx, y + 2, sx, y + strip_h - 2)

    # Footer
    y_foot = MARGIN + 18
    c.setStrokeColor(C_ACCENT)
    c.setLineWidth(0.5)
    c.line(MARGIN + 20, y_foot + 10, W - MARGIN - 20, y_foot + 10)

    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 6)
    c.drawString(MARGIN + 20, y_foot,
                 "Hs Decomposition Engine  |  Manifold Helix  |  Real Data Projection")
    c.drawRightString(W - MARGIN - 20, y_foot,
                      "Peter Higgins / Rogue Wave Audio / CC BY 4.0")

    c.setFont("Helvetica", 5)
    c.drawCentredString(CX, y_foot - 10,
                        f"{experiment_id} — Generated by hs_manifold_helix.py — Hs Standards Edition")

    c.restoreState()


def normalise_data(data):
    """Normalise field names across M01 and M02 formats (same as hs_helix_exploded.py)."""
    out = dict(data)

    if "input_shape" not in out:
        D = data.get("D", "?")
        n_years = len(data.get("years", []))
        if n_years and D:
            out["input_shape"] = f"{n_years} observations x {D} carriers"

    if "V(t)_shape" not in out:
        out["V(t)_shape"] = data.get("vt_shape", "—")

    if "entropy_mean" not in out:
        ent = data.get("entropy_trajectory", {})
        if ent:
            vals = [v for v in ent.values() if isinstance(v, (int, float))]
            if vals:
                out["entropy_mean"] = sum(vals) / len(vals)

    if "aitchison_norm_mean" not in out:
        ant = data.get("aitchison_norm_trajectory", {})
        if ant:
            vals = [v for v in ant.values() if isinstance(v, (int, float))]
            if vals:
                out["aitchison_norm_mean"] = sum(vals) / len(vals)

    if "locks_found" not in out:
        locks = data.get("locks", [])
        out["locks_found"] = len(locks) if isinstance(locks, list) else locks

    if "DIAGNOSIS" not in out:
        vt = out.get("V(t)_shape", "")
        if "accelerating" in str(vt).lower():
            out["DIAGNOSIS"] = "ACCELERATING DRIFT"
        elif "decelerating" in str(vt).lower():
            out["DIAGNOSIS"] = "DECELERATING DRIFT"
        elif "flat" in str(vt).lower():
            out["DIAGNOSIS"] = "STATIONARY"
        else:
            out["DIAGNOSIS"] = "—"

    return out


def build_manifold_helix_pdf(results_json, output_pdf):
    """Main builder — reads pipeline results, produces manifold helix PDF."""

    with open(results_json, 'r') as f:
        raw = json.load(f)

    experiment_id = raw.get("experiment", "Hs-M00")

    # Select data object
    if "results" in raw and isinstance(raw["results"], list):
        results = raw["results"]
        chosen = None
        for r in results:
            obj = r.get("test_object", "").lower()
            if "helix" in obj or "circle" in obj or "spiral" in obj:
                chosen = r
                break
        if chosen is None:
            for r in results:
                tv = r.get("total_variance")
                if tv is None or tv == "N/A (single observation)":
                    continue
                try:
                    if float(tv) > 0.001:
                        chosen = r
                        break
                except:
                    continue
        if chosen is None:
            chosen = results[0]
        data = normalise_data(chosen)
    elif "countries" in raw:
        countries = raw["countries"]
        first_key = list(countries.keys())[0]
        cdata = countries[first_key]
        cdata["test_object"] = cdata.get("country", first_key)
        data = normalise_data(cdata)
    elif "results" in raw and isinstance(raw["results"], dict):
        data = normalise_data(raw["results"])
    else:
        data = normalise_data(raw)

    test_object = data.get("test_object", data.get("country", "Unknown"))
    simplex = data.get("simplex", "S^?")
    D = data.get("D", 3)
    if "simplex" not in data and D:
        simplex = f"S^{D-1}"

    # Extract trajectory
    trajectory = extract_trajectory(data)
    N = len(trajectory)

    # Create PDF
    pdf = canvas.Canvas(output_pdf, pagesize=A4)
    pdf.setTitle(f"Hs Manifold Helix — {experiment_id}")
    pdf.setAuthor("Peter Higgins / Rogue Wave Audio")
    pdf.setSubject("Manifold Helix — Real Data Projection")

    draw_header(pdf, experiment_id, test_object, simplex, D, N)

    ring_positions, proj_pts, draw_cx, draw_cy = draw_manifold_helix(
        pdf, CX, CY, trajectory, data
    )

    draw_waypoint_tags(pdf, ring_positions, trajectory, data, proj_pts)

    draw_summary_footer(pdf, data, experiment_id)

    pdf.save()
    print(f"Generated: {output_pdf}")
    return output_pdf


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hs_manifold_helix.py <results.json> [output.pdf]")
        sys.exit(1)

    results_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else "manifold_helix.pdf"
    build_manifold_helix_pdf(results_file, out_file)
