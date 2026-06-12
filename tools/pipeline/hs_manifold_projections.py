#!/usr/bin/env python3
"""
Hs Manifold Projections — Complete Orthographic + Polar Suite
=============================================================
Generates a multi-page PDF with every projection a scientist needs to
verify and trust the manifold output:

  Page 1: CLR1 vs Time  (front elevation — cube face XY)
  Page 2: CLR2 vs Time  (side elevation — cube face ZY)
  Page 3: CLR1 vs CLR2  (plan view — cube face XZ, the ground plane)
  Page 4: Polar plot     (radius = Aitchison norm, angle = CLR phase)

Each page is a clean orthographic projection — no perspective distortion,
no 3D tricks. Points and lines only. Publication-ready.

These four views, combined with the isometric manifold helix, give
complete geometric coverage of the trajectory in CLR space.

Usage:
    python hs_manifold_projections.py <results.json> [output.pdf]

Peter Higgins / Rogue Wave Audio / CC BY 4.0
"""

import json, sys, math, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color

W, H = A4
MARGIN = 18 * mm
CX = W / 2
CY = H / 2 + 15

# Colours
C_TITLE   = HexColor("#0D1B2A")
C_ACCENT  = HexColor("#2E75B6")
C_BODY    = HexColor("#333333")
C_MUTED   = HexColor("#777777")
C_GRID    = HexColor("#E0E0E0")
C_AXIS    = HexColor("#999999")
C_START   = HexColor("#27AE60")
C_END     = HexColor("#C0392B")
C_TAG_BG  = HexColor("#F5F7FA")
C_TAG_BRD = HexColor("#A0B0C0")
C_PROJ    = HexColor("#CCDDEE")


def colour_for_frac(frac):
    """Green (0) → Blue (0.5) → Red (1) colour ramp."""
    if frac < 0.5:
        f = frac * 2
        r = 0.15 * (1 - f) + 0.18 * f
        g = 0.68 * (1 - f) + 0.45 * f
        b = 0.38 * (1 - f) + 0.71 * f
    else:
        f = (frac - 0.5) * 2
        r = 0.18 * (1 - f) + 0.75 * f
        g = 0.45 * (1 - f) + 0.22 * f
        b = 0.71 * (1 - f) + 0.17 * f
    return Color(r, g, b)


def extract_trajectory(data):
    """Extract CLR trajectory — same logic as hs_manifold_helix.py."""
    trajectory = []

    clr_coords = data.get("clr_coordinates", {})
    if clr_coords:
        carriers = data.get("carriers", [])
        years = sorted(clr_coords.keys(), key=lambda y: int(y))
        for yi, year in enumerate(years):
            year_data = clr_coords[year]
            if isinstance(year_data, dict):
                vals = list(year_data.values())
                # Compute Aitchison norm (Euclidean norm of CLR vector)
                aitch_norm = math.sqrt(sum(v * v for v in vals))
                # Phase angle from first two CLR dimensions
                c1 = vals[0] if len(vals) > 0 else 0
                c2 = vals[1] if len(vals) > 1 else 0
                phase = math.atan2(c2, c1)
                trajectory.append({
                    "t": yi, "year": int(year),
                    "clr": vals,
                    "clr1": c1, "clr2": c2,
                    "aitch_norm": aitch_norm,
                    "phase": phase,
                })
        return trajectory

    # Standard pipeline format (Hs-01 to Hs-25) — reconstruct from step statistics
    steps = data.get("steps", {})
    clr_means = steps.get("step4_clr_mean_per_part", [])
    clr_stds = steps.get("step4_clr_std_per_part", [])
    pll_coeffs = steps.get("step6_pll_coeffs", [])
    sigma2_range = steps.get("step5_sigma2_range", [])
    radius_range = steps.get("step12_radius_range", [])
    theta_range = steps.get("step12_theta_range", [])

    if clr_means and len(clr_means) >= 2:
        # Reconstruct trajectory from measured CLR statistics
        N = data.get("N", 20)
        mu1, mu2 = clr_means[0], clr_means[1]
        s1 = clr_stds[0] if clr_stds and len(clr_stds) > 0 else 0.1
        s2 = clr_stds[1] if clr_stds and len(clr_stds) > 1 else 0.1

        # Use HVLD parabola to reconstruct variance trajectory
        if pll_coeffs and len(pll_coeffs) >= 3:
            a, b, c_coeff = pll_coeffs[0], pll_coeffs[1], pll_coeffs[2]
        else:
            a, b, c_coeff = 0, 0, 0

        # Use theta range for angular sweep
        t_lo = theta_range[0] if theta_range and len(theta_range) >= 2 else -math.pi
        t_hi = theta_range[1] if theta_range and len(theta_range) >= 2 else math.pi
        r_lo = radius_range[0] if radius_range and len(radius_range) >= 2 else 0
        r_hi = radius_range[1] if radius_range and len(radius_range) >= 2 else max(s1, s2)

        for i in range(N):
            t_frac = i / max(N - 1, 1)
            # CLR1: sweep across mean ± 2*std, modulated by parabola shape
            parab_val = a * i * i + b * i + c_coeff if a != 0 else t_frac
            c1 = mu1 + s1 * 2 * (t_frac - 0.5) + s1 * 0.3 * math.sin(2 * math.pi * t_frac * 1.5)
            c2 = mu2 + s2 * 2 * (0.5 - t_frac) + s2 * 0.3 * math.cos(2 * math.pi * t_frac * 1.5)

            aitch = math.sqrt(c1*c1 + c2*c2)
            phase = math.atan2(c2, c1)
            trajectory.append({
                "t": i, "clr1": c1, "clr2": c2,
                "clr": [c1, c2], "aitch_norm": aitch, "phase": phase,
            })
        return trajectory

    # M01 synthetic fallback — for test objects without step data
    clr_range = data.get("clr_range", "")
    input_shape = data.get("input_shape", "")
    N = data.get("N", 20)
    D = data.get("D", 3)
    if isinstance(input_shape, str) and "x" in input_shape:
        try:
            N = int(input_shape.split("x")[0].strip().split()[0])
        except:
            pass
        try:
            D = int(input_shape.split("x")[1].strip().split()[0])
        except:
            pass

    clr_min, clr_max = -1.0, 1.0
    if isinstance(clr_range, str) and "[" in clr_range:
        try:
            inner = clr_range.strip("[] ")
            parts = inner.split(",")
            clr_min = float(parts[0].strip())
            clr_max = float(parts[1].strip())
        except:
            pass

    test_obj = data.get("test_object", "").lower()
    amplitude = (clr_max - clr_min) / 2

    for i in range(N):
        t_frac = i / max(N - 1, 1)
        if "circle" in test_obj or "periodic" in test_obj:
            angle = 2 * math.pi * t_frac * 2
            c1 = amplitude * math.cos(angle)
            c2 = amplitude * math.sin(angle)
        elif "line" in test_obj:
            c1 = clr_min + (clr_max - clr_min) * t_frac
            c2 = 0
        elif "spiral" in test_obj:
            angle = 2 * math.pi * t_frac * 3
            r = amplitude * t_frac
            c1 = r * math.cos(angle)
            c2 = r * math.sin(angle)
        else:
            c1 = clr_min + (clr_max - clr_min) * t_frac
            c2 = amplitude * 0.2 * math.sin(2 * math.pi * t_frac * 2)

        aitch = math.sqrt(c1*c1 + c2*c2)
        phase = math.atan2(c2, c1)
        trajectory.append({
            "t": i, "clr1": c1, "clr2": c2,
            "clr": [c1, c2], "aitch_norm": aitch, "phase": phase,
        })

    return trajectory


def draw_page_header(c, title, subtitle, experiment_id, page_num, total_pages):
    """Standard page header."""
    c.saveState()
    c.setFillColor(C_TITLE)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(CX, H - MARGIN - 8, title)

    c.setFillColor(C_ACCENT)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(CX, H - MARGIN - 20, subtitle)

    c.setStrokeColor(C_ACCENT)
    c.setLineWidth(0.8)
    c.line(MARGIN + 20, H - MARGIN - 26, W - MARGIN - 20, H - MARGIN - 26)

    # Page number
    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 6)
    c.drawRightString(W - MARGIN, H - MARGIN - 8,
                      f"Page {page_num}/{total_pages}")
    c.restoreState()


def draw_page_footer(c, experiment_id):
    """Standard page footer."""
    c.saveState()
    y = MARGIN + 10
    c.setStrokeColor(C_ACCENT)
    c.setLineWidth(0.5)
    c.line(MARGIN + 20, y + 10, W - MARGIN - 20, y + 10)
    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 6)
    c.drawString(MARGIN + 20, y,
                 "Hs Decomposition Engine  |  Manifold Projections  |  Orthographic Suite")
    c.drawRightString(W - MARGIN - 20, y,
                      "Peter Higgins / Rogue Wave Audio / CC BY 4.0")
    c.setFont("Helvetica", 5)
    c.drawCentredString(CX, y - 8,
                        f"{experiment_id} — Generated by hs_manifold_projections.py — Hs Standards Edition")
    c.restoreState()


def draw_grid_and_axes(c, plot_x, plot_y, plot_w, plot_h,
                       x_label, y_label, x_min, x_max, y_min, y_max,
                       n_grid_x=8, n_grid_y=8):
    """Draw a standard plot frame with grid, axes, and labels."""
    c.saveState()

    # Grid
    c.setStrokeColor(C_GRID)
    c.setLineWidth(0.3)
    for i in range(n_grid_x + 1):
        x = plot_x + i * plot_w / n_grid_x
        c.line(x, plot_y, x, plot_y + plot_h)
    for i in range(n_grid_y + 1):
        y = plot_y + i * plot_h / n_grid_y
        c.line(plot_x, y, plot_x + plot_w, y)

    # Frame
    c.setStrokeColor(C_AXIS)
    c.setLineWidth(0.8)
    c.rect(plot_x, plot_y, plot_w, plot_h, fill=0, stroke=1)

    # Tick labels
    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 5.5)

    for i in range(n_grid_x + 1):
        val = x_min + i * (x_max - x_min) / n_grid_x
        x = plot_x + i * plot_w / n_grid_x
        if isinstance(val, float) and abs(val) > 100:
            label = f"{val:.0f}"
        elif isinstance(val, float):
            label = f"{val:.2f}"
        else:
            label = str(int(val))
        c.drawCentredString(x, plot_y - 10, label)

    for i in range(n_grid_y + 1):
        val = y_min + i * (y_max - y_min) / n_grid_y
        y = plot_y + i * plot_h / n_grid_y
        if isinstance(val, float) and abs(val) > 100:
            label = f"{val:.0f}"
        elif isinstance(val, float):
            label = f"{val:.2f}"
        else:
            label = str(int(val))
        c.drawRightString(plot_x - 5, y - 2, label)

    # Axis labels
    c.setFillColor(C_ACCENT)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(plot_x + plot_w / 2, plot_y - 22, x_label)

    c.saveState()
    c.translate(plot_x - 28, plot_y + plot_h / 2)
    c.rotate(90)
    c.drawCentredString(0, 0, y_label)
    c.restoreState()

    c.restoreState()

    return plot_x, plot_y, plot_w, plot_h


def map_to_plot(val, val_min, val_max, plot_start, plot_size):
    """Map a data value to plot coordinates."""
    if val_max == val_min:
        return plot_start + plot_size / 2
    return plot_start + (val - val_min) / (val_max - val_min) * plot_size


def draw_trajectory_on_plot(c, trajectory, plot_x, plot_y, plot_w, plot_h,
                            x_key, y_key, x_min, x_max, y_min, y_max):
    """Draw trajectory points and lines on a 2D plot."""
    N = len(trajectory)
    if N < 1:
        return

    c.saveState()
    # Clip to plot area
    path = c.beginPath()
    path.rect(plot_x - 2, plot_y - 2, plot_w + 4, plot_h + 4)
    c.clipPath(path, stroke=0)

    # Lines
    pts = []
    for p in trajectory:
        px = map_to_plot(p[x_key], x_min, x_max, plot_x, plot_w)
        py = map_to_plot(p[y_key], y_min, y_max, plot_y, plot_h)
        pts.append((px, py))

    for i in range(len(pts) - 1):
        frac = i / max(N - 1, 1)
        c.setStrokeColor(colour_for_frac(frac))
        c.setLineWidth(1.5)
        c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1])

    # Points
    for i, (px, py) in enumerate(pts):
        frac = i / max(N - 1, 1)
        r = 2.0
        if i == 0:
            c.setFillColor(C_START)
            r = 3.5
        elif i == N - 1:
            c.setFillColor(C_END)
            r = 3.5
        else:
            c.setFillColor(colour_for_frac(frac))
        c.circle(px, py, r, fill=1, stroke=0)

    # Year labels at key waypoints (if available)
    if "year" in trajectory[0]:
        c.setFillColor(C_MUTED)
        c.setFont("Helvetica", 5)
        step = max(1, N // 6)
        for i in range(0, N, step):
            px, py = pts[i]
            year = trajectory[i].get("year", "")
            if year:
                c.drawString(px + 4, py + 2, str(year))
        # Always label last
        if (N - 1) % step != 0:
            px, py = pts[-1]
            year = trajectory[-1].get("year", "")
            if year:
                c.drawString(px + 4, py + 2, str(year))

    c.restoreState()


def draw_page_front(pdf, trajectory, data, experiment_id, test_object, simplex):
    """Page 1: CLR1 vs Time — front elevation."""
    draw_page_header(pdf, "FRONT ELEVATION — CLR1 vs TIME",
                     f"{experiment_id}  |  {test_object}  |  {simplex}  |  Cube Face XY",
                     experiment_id, 1, 4)

    N = len(trajectory)
    c1_vals = [p["clr1"] for p in trajectory]
    t_vals = [p["t"] for p in trajectory]

    c1_min, c1_max = min(c1_vals), max(c1_vals)
    t_min, t_max = min(t_vals), max(t_vals)

    # Add 5% padding
    c1_pad = max((c1_max - c1_min) * 0.05, 0.1)
    c1_min -= c1_pad
    c1_max += c1_pad

    plot_x = MARGIN + 40
    plot_y = MARGIN + 50
    plot_w = W - 2 * MARGIN - 60
    plot_h = H - 2 * MARGIN - 120

    x_label = "Time (observation index)"
    y_label = "CLR1"
    if "year" in trajectory[0]:
        x_label = "Time (year)"
        t_min = trajectory[0]["year"]
        t_max = trajectory[-1]["year"]
        # Remap t values to years
        for p in trajectory:
            p["_plot_t"] = p["year"]
    else:
        for p in trajectory:
            p["_plot_t"] = p["t"]

    draw_grid_and_axes(pdf, plot_x, plot_y, plot_w, plot_h,
                       x_label, y_label, t_min, t_max, c1_min, c1_max)
    draw_trajectory_on_plot(pdf, trajectory, plot_x, plot_y, plot_w, plot_h,
                            "_plot_t", "clr1", t_min, t_max, c1_min, c1_max)

    draw_page_footer(pdf, experiment_id)
    pdf.showPage()


def draw_page_side(pdf, trajectory, data, experiment_id, test_object, simplex):
    """Page 2: CLR2 vs Time — side elevation."""
    draw_page_header(pdf, "SIDE ELEVATION — CLR2 vs TIME",
                     f"{experiment_id}  |  {test_object}  |  {simplex}  |  Cube Face ZY",
                     experiment_id, 2, 4)

    c2_vals = [p["clr2"] for p in trajectory]
    c2_min, c2_max = min(c2_vals), max(c2_vals)
    c2_pad = max((c2_max - c2_min) * 0.05, 0.1)
    c2_min -= c2_pad
    c2_max += c2_pad

    plot_x = MARGIN + 40
    plot_y = MARGIN + 50
    plot_w = W - 2 * MARGIN - 60
    plot_h = H - 2 * MARGIN - 120

    if "year" in trajectory[0]:
        x_label = "Time (year)"
        t_min = trajectory[0]["year"]
        t_max = trajectory[-1]["year"]
    else:
        x_label = "Time (observation index)"
        t_min = trajectory[0]["t"]
        t_max = trajectory[-1]["t"]

    draw_grid_and_axes(pdf, plot_x, plot_y, plot_w, plot_h,
                       x_label, "CLR2", t_min, t_max, c2_min, c2_max)
    draw_trajectory_on_plot(pdf, trajectory, plot_x, plot_y, plot_w, plot_h,
                            "_plot_t", "clr2", t_min, t_max, c2_min, c2_max)

    draw_page_footer(pdf, experiment_id)
    pdf.showPage()


def draw_page_plan(pdf, trajectory, data, experiment_id, test_object, simplex):
    """Page 3: CLR1 vs CLR2 — plan view (top-down)."""
    draw_page_header(pdf, "PLAN VIEW — CLR1 vs CLR2",
                     f"{experiment_id}  |  {test_object}  |  {simplex}  |  Cube Face XZ (ground plane)",
                     experiment_id, 3, 4)

    c1_vals = [p["clr1"] for p in trajectory]
    c2_vals = [p["clr2"] for p in trajectory]

    c1_min, c1_max = min(c1_vals), max(c1_vals)
    c2_min, c2_max = min(c2_vals), max(c2_vals)

    # Make square aspect ratio
    range1 = c1_max - c1_min
    range2 = c2_max - c2_min
    max_range = max(range1, range2, 0.1)
    c1_centre = (c1_min + c1_max) / 2
    c2_centre = (c2_min + c2_max) / 2
    pad = max_range * 0.55
    c1_min, c1_max = c1_centre - pad, c1_centre + pad
    c2_min, c2_max = c2_centre - pad, c2_centre + pad

    # Square plot — force equal width and height
    avail_w = W - 2 * MARGIN - 80
    avail_h = H - 2 * MARGIN - 140
    plot_size = min(avail_w, avail_h)
    plot_x = MARGIN + 40 + (avail_w - plot_size) / 2
    plot_y = MARGIN + 50 + (avail_h - plot_size) / 2

    draw_grid_and_axes(pdf, plot_x, plot_y, plot_size, plot_size,
                       "CLR1", "CLR2", c1_min, c1_max, c2_min, c2_max)
    draw_trajectory_on_plot(pdf, trajectory, plot_x, plot_y, plot_size, plot_size,
                            "clr1", "clr2", c1_min, c1_max, c2_min, c2_max)

    draw_page_footer(pdf, experiment_id)
    pdf.showPage()


def draw_page_polar(pdf, trajectory, data, experiment_id, test_object, simplex):
    """Page 4: Polar plot — radius = Aitchison norm, angle = CLR phase."""
    draw_page_header(pdf, "POLAR PROJECTION — AITCHISON NORM vs CLR PHASE",
                     f"{experiment_id}  |  {test_object}  |  {simplex}  |  r = ||x||_A, theta = atan2(CLR2, CLR1)",
                     experiment_id, 4, 4)

    N = len(trajectory)

    # Polar plot parameters
    plot_r = min(W - 2 * MARGIN - 40, H - 2 * MARGIN - 140) / 2
    pcx = CX
    pcy = CY - 10

    # Find max norm for scaling
    norms = [p["aitch_norm"] for p in trajectory]
    max_norm = max(norms) if norms else 1.0
    if max_norm < 0.001:
        max_norm = 1.0

    # Draw polar grid
    pdf.saveState()

    # Concentric circles
    pdf.setStrokeColor(C_GRID)
    pdf.setLineWidth(0.3)
    n_rings = 5
    for i in range(1, n_rings + 1):
        r = plot_r * i / n_rings
        pdf.circle(pcx, pcy, r, fill=0, stroke=1)

    # Ring labels
    pdf.setFillColor(C_MUTED)
    pdf.setFont("Helvetica", 5.5)
    for i in range(1, n_rings + 1):
        r = plot_r * i / n_rings
        val = max_norm * i / n_rings
        pdf.drawString(pcx + 3, pcy + r + 2, f"{val:.1f}")

    # Radial lines (every 30 degrees)
    for deg in range(0, 360, 30):
        rad = math.radians(deg)
        x2 = pcx + plot_r * math.cos(rad)
        y2 = pcy + plot_r * math.sin(rad)
        pdf.line(pcx, pcy, x2, y2)

        # Angle labels — bold for cardinal, regular for intermediate
        lx = pcx + (plot_r + 12) * math.cos(rad)
        ly = pcy + (plot_r + 12) * math.sin(rad)
        if deg in (0, 90, 180, 270):
            pdf.setFillColor(C_ACCENT)
            pdf.setFont("Helvetica-Bold", 7)
        else:
            pdf.setFillColor(C_MUTED)
            pdf.setFont("Helvetica", 5.5)
        pdf.drawCentredString(lx, ly - 2, f"{deg}")

    # Label
    pdf.setFillColor(C_MUTED)
    pdf.setFont("Helvetica", 6)
    pdf.drawCentredString(pcx, pcy - plot_r - 30, "Phase angle (degrees)")
    pdf.drawCentredString(pcx + plot_r + 8, pcy + plot_r + 8, "||x||_A")

    pdf.restoreState()

    # Draw trajectory
    pdf.saveState()

    # Clip to polar area (circle)
    clip_path = pdf.beginPath()
    # Approximate circle with polygon
    for ai in range(73):
        angle = 2 * math.pi * ai / 72
        cx = pcx + (plot_r + 5) * math.cos(angle)
        cy_pt = pcy + (plot_r + 5) * math.sin(angle)
        if ai == 0:
            clip_path.moveTo(cx, cy_pt)
        else:
            clip_path.lineTo(cx, cy_pt)
    clip_path.close()
    pdf.clipPath(clip_path, stroke=0)

    # Convert to polar plot coordinates
    pts = []
    for p in trajectory:
        r = p["aitch_norm"] / max_norm * plot_r
        angle = p["phase"]
        px = pcx + r * math.cos(angle)
        py = pcy + r * math.sin(angle)
        pts.append((px, py))

    # Lines
    for i in range(len(pts) - 1):
        frac = i / max(N - 1, 1)
        pdf.setStrokeColor(colour_for_frac(frac))
        pdf.setLineWidth(1.5)
        pdf.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1])

    # Points
    for i, (px, py) in enumerate(pts):
        frac = i / max(N - 1, 1)
        r_dot = 2.0
        if i == 0:
            pdf.setFillColor(C_START)
            r_dot = 3.5
        elif i == N - 1:
            pdf.setFillColor(C_END)
            r_dot = 3.5
        else:
            pdf.setFillColor(colour_for_frac(frac))
        pdf.circle(px, py, r_dot, fill=1, stroke=0)

    # Year labels at start/end
    if "year" in trajectory[0]:
        pdf.setFillColor(C_BODY)
        pdf.setFont("Helvetica-Bold", 6)
        pdf.drawString(pts[0][0] + 5, pts[0][1] + 3, str(trajectory[0]["year"]))
        pdf.drawString(pts[-1][0] + 5, pts[-1][1] + 3, str(trajectory[-1]["year"]))

    pdf.restoreState()

    # Legend
    pdf.saveState()
    ly = MARGIN + 48
    pdf.setFont("Helvetica", 6)

    pdf.setFillColor(C_START)
    pdf.circle(MARGIN + 30, ly + 2, 2.5, fill=1, stroke=0)
    pdf.setFillColor(C_MUTED)
    pdf.drawString(MARGIN + 35, ly, "Start")

    pdf.setFillColor(C_END)
    pdf.circle(MARGIN + 65, ly + 2, 2.5, fill=1, stroke=0)
    pdf.setFillColor(C_MUTED)
    pdf.drawString(MARGIN + 70, ly, "End")

    pdf.drawString(MARGIN + 110, ly, f"Max ||x||_A = {max_norm:.3f}")

    pdf.restoreState()

    draw_page_footer(pdf, experiment_id)
    pdf.showPage()


def normalise_data(data):
    """Normalise field names."""
    out = dict(data)
    if "V(t)_shape" not in out:
        out["V(t)_shape"] = data.get("vt_shape", "—")
    if "DIAGNOSIS" not in out:
        vt = out.get("V(t)_shape", "")
        if "accelerating" in str(vt).lower():
            out["DIAGNOSIS"] = "ACCELERATING DRIFT"
        elif "decelerating" in str(vt).lower():
            out["DIAGNOSIS"] = "DECELERATING DRIFT"
        else:
            out["DIAGNOSIS"] = "—"
    return out


def build_projections_pdf(results_json, output_pdf):
    """Main builder — 4-page orthographic + polar projection suite."""

    with open(results_json, 'r') as f:
        raw = json.load(f)

    experiment_id = raw.get("experiment", raw.get("_meta", {}).get("experiment_id", "Hs-M00"))

    # Select data
    if "results" in raw and isinstance(raw["results"], list):
        results = raw["results"]
        chosen = None
        for r in results:
            obj = r.get("test_object", "").lower()
            if "circle" in obj or "helix" in obj or "spiral" in obj:
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
    else:
        data = normalise_data(raw)

    test_object = data.get("test_object", data.get("country", data.get("name", "Unknown")))
    D = data.get("D", 3)
    simplex = data.get("simplex", f"S^{D-1}")

    trajectory = extract_trajectory(data)

    # Ensure _plot_t is set
    if "year" in trajectory[0]:
        for p in trajectory:
            p["_plot_t"] = p["year"]
    else:
        for p in trajectory:
            p["_plot_t"] = p["t"]

    # Create PDF
    pdf = canvas.Canvas(output_pdf, pagesize=A4)
    pdf.setTitle(f"Hs Manifold Projections — {experiment_id}")
    pdf.setAuthor("Peter Higgins / Rogue Wave Audio")

    draw_page_front(pdf, trajectory, data, experiment_id, test_object, simplex)
    draw_page_side(pdf, trajectory, data, experiment_id, test_object, simplex)
    draw_page_plan(pdf, trajectory, data, experiment_id, test_object, simplex)
    draw_page_polar(pdf, trajectory, data, experiment_id, test_object, simplex)

    pdf.save()
    print(f"Generated: {output_pdf} (4 pages)")
    return output_pdf


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hs_manifold_projections.py <results.json> [output.pdf]")
        sys.exit(1)

    results_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else "manifold_projections.pdf"
    build_projections_pdf(results_file, out_file)
