#!/usr/bin/env python3
"""
Hs Manifold on Paper — 3D Polar Slice Stack in Projected Space
==============================================================
Takes the per-interval polar radar polygons and stacks them along a time
axis in 3D projected space. Connects corresponding carrier vertices
between adjacent slices to reveal the manifold surface.

This is the HTML manifold projector — on paper.

The viewing angle auto-rotates to find the projection that reveals the
most spatial separation (maximum projected bounding area).

Output: multi-page A4 PDF
  Page 1: Optimal-angle 3D manifold with all slices and surface mesh
  Page 2: Three-panel view (front, 3/4, top-down)
  Page 3: Carrier trace separation — individual carrier trajectories

Usage:
    python hs_manifold_paper.py <results.json> [output.pdf]

Peter Higgins / Rogue Wave Audio / CC BY 4.0
"""

import json, sys, math, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color

W, H = A4
MARGIN = 14 * mm
CX = W / 2
CY = H / 2

# Colours
C_TITLE   = HexColor("#0D1B2A")
C_ACCENT  = HexColor("#2E75B6")
C_BODY    = HexColor("#333333")
C_MUTED   = HexColor("#777777")
C_GRID    = HexColor("#E0E0E0")
C_AXIS    = HexColor("#BBBBBB")
C_START   = HexColor("#27AE60")
C_END     = HexColor("#C0392B")
C_TAG_BG  = HexColor("#F5F7FA")
C_TAG_BRD = HexColor("#A0B0C0")
C_MESH    = HexColor("#C8D8E8")
C_PROJ    = HexColor("#CCDDEE")

# Carrier colours
CARRIER_COLOURS = [
    HexColor("#2E75B6"), HexColor("#C0392B"), HexColor("#27AE60"),
    HexColor("#8E44AD"), HexColor("#E67E22"), HexColor("#16A085"),
    HexColor("#D4AC0D"), HexColor("#E74C3C"), HexColor("#3498DB"),
    HexColor("#1ABC9C"), HexColor("#9B59B6"), HexColor("#F39C12"),
]


def colour_for_frac(frac):
    """Green (0) -> Blue (0.5) -> Red (1) colour ramp."""
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


def extract_from_polar_json(data):
    """Extract trajectory from polar stack JSON format (has real per-year CLR values)."""
    trajectory = []
    carriers = data.get("carriers", [])
    intervals = data.get("intervals", [])

    for iv in intervals:
        clr_dict = iv.get("clr", {})
        if isinstance(clr_dict, dict):
            vals = list(clr_dict.values())
            carrier_names = list(clr_dict.keys())
        elif isinstance(clr_dict, list):
            vals = clr_dict
            carrier_names = carriers[:len(vals)]
        else:
            continue

        aitch_norm = iv.get("aitchison_norm", math.sqrt(sum(v * v for v in vals)))
        c1 = vals[0] if len(vals) > 0 else 0
        c2 = vals[1] if len(vals) > 1 else 0
        phase = math.atan2(c2, c1)
        trajectory.append({
            "t": iv.get("index", len(trajectory)),
            "year": iv.get("year", iv.get("index", len(trajectory))),
            "clr": vals,
            "carrier_names": carrier_names,
            "clr1": c1, "clr2": c2,
            "aitch_norm": aitch_norm,
            "phase": phase,
            "D": len(vals),
        })

    return trajectory, carriers


def extract_full_trajectory(data):
    """Extract full CLR trajectory with ALL dimensions per interval."""
    trajectory = []
    carriers = data.get("carriers", [])

    # Try polar stack JSON format first (has real per-year values)
    if "intervals" in data:
        return extract_from_polar_json(data)

    clr_coords = data.get("clr_coordinates", {})
    if clr_coords:
        years = sorted(clr_coords.keys(), key=lambda y: int(y))
        for yi, year in enumerate(years):
            year_data = clr_coords[year]
            if isinstance(year_data, dict):
                vals = list(year_data.values())
                carrier_names = list(year_data.keys())
                aitch_norm = math.sqrt(sum(v * v for v in vals))
                c1 = vals[0] if len(vals) > 0 else 0
                c2 = vals[1] if len(vals) > 1 else 0
                phase = math.atan2(c2, c1)
                trajectory.append({
                    "t": yi, "year": int(year),
                    "clr": vals,
                    "carrier_names": carrier_names,
                    "clr1": c1, "clr2": c2,
                    "aitch_norm": aitch_norm,
                    "phase": phase,
                    "D": len(vals),
                })
        return trajectory, carriers

    # Standard pipeline format — reconstruct from statistics
    steps = data.get("steps", {})
    clr_means = steps.get("step4_clr_mean_per_part", [])
    clr_stds = steps.get("step4_clr_std_per_part", [])
    N = data.get("N", 20)

    if clr_means and len(clr_means) >= 2:
        for i in range(N):
            t_frac = i / max(N - 1, 1)
            vals = []
            for d in range(len(clr_means)):
                mu = clr_means[d]
                s = clr_stds[d] if d < len(clr_stds) else 0.1
                v = mu + s * 2 * (t_frac - 0.5) + s * 0.3 * math.sin(2 * math.pi * t_frac * (1.5 + d * 0.3))
                vals.append(v)
            aitch = math.sqrt(sum(v * v for v in vals))
            phase = math.atan2(vals[1], vals[0]) if len(vals) >= 2 else 0
            trajectory.append({
                "t": i, "clr": vals,
                "carrier_names": carriers[:len(vals)],
                "clr1": vals[0], "clr2": vals[1] if len(vals) > 1 else 0,
                "aitch_norm": aitch, "phase": phase,
                "D": len(vals),
            })
        return trajectory, carriers

    return [], carriers


def build_slice_vertices(trajectory, all_max):
    """
    For each interval, compute D 3D vertices of the polar radar polygon.
    Returns list of lists: slices[i][j] = (x3d, y3d, z3d)

    Coordinate system:
      x, z = polar radar plane (carrier axes)
      y = time (vertical, pointing up)
    """
    N = len(trajectory)
    D = trajectory[0]["D"] if trajectory else 3
    slices = []

    for i, point in enumerate(trajectory):
        clr = point["clr"]
        d = len(clr)
        t_norm = i / max(N - 1, 1)  # 0..1
        y3d = t_norm  # time goes up

        verts = []
        for j in range(d):
            angle = 2 * math.pi * j / d - math.pi / 2  # start at top
            r = abs(clr[j]) / all_max  # normalised radius 0..1
            r = min(r, 1.0)  # clamp to unit sphere
            x3d = r * math.cos(angle)
            z3d = r * math.sin(angle)
            verts.append((x3d, y3d, z3d))
        slices.append(verts)

    return slices


def project_3d(x, y, z, azimuth, elevation, cx, cy, scale_xz, scale_y):
    """
    Project a 3D point to 2D screen coordinates using rotation + oblique projection.

    azimuth: horizontal rotation angle (radians, 0 = front)
    elevation: vertical tilt angle (radians, 0 = level, pi/6 = 30° looking down)
    """
    # Rotate around Y axis (azimuth)
    ca, sa = math.cos(azimuth), math.sin(azimuth)
    rx = x * ca - z * sa
    rz = x * sa + z * ca

    # Tilt (elevation) — rotate around X axis
    ce, se = math.cos(elevation), math.sin(elevation)
    ry = y * ce - rz * se
    rz2 = y * se + rz * ce

    # Oblique projection: map to screen
    # Add slight depth cue
    depth_scale = 1.0 + 0.15 * rz2
    sx = cx + scale_xz * rx * depth_scale
    sy = cy + scale_y * ry * depth_scale

    return sx, sy, rz2  # rz2 used for depth sorting


def find_best_angle(slices, n_samples=36):
    """
    Find the viewing angle that maximises the projected bounding area.
    Tests n_samples azimuth angles at a fixed elevation.
    """
    best_area = 0
    best_az = math.radians(35)  # default 3/4 view
    elevation = math.radians(25)  # slight tilt to reveal slice shapes

    for i in range(n_samples):
        az = 2 * math.pi * i / n_samples
        xs, ys = [], []
        for sl in slices:
            for (x, y, z) in sl:
                sx, sy, _ = project_3d(x, y, z, az, elevation, 0, 0, 1, 1)
                xs.append(sx)
                ys.append(sy)
        if xs:
            area = (max(xs) - min(xs)) * (max(ys) - min(ys))
            if area > best_area:
                best_area = area
                best_az = az

    return best_az, elevation


def draw_page_header(c, title, subtitle, experiment_id, page_num, total_pages):
    """Standard page header."""
    c.saveState()
    c.setFillColor(C_TITLE)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(CX, H - MARGIN - 8, title)
    c.setFillColor(C_ACCENT)
    c.setFont("Helvetica", 8)
    c.drawCentredString(CX, H - MARGIN - 20, subtitle)
    c.setStrokeColor(C_ACCENT)
    c.setLineWidth(0.8)
    c.line(MARGIN + 20, H - MARGIN - 26, W - MARGIN - 20, H - MARGIN - 26)
    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 6)
    c.drawRightString(W - MARGIN, H - MARGIN - 8, f"Page {page_num}/{total_pages}")
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
                 "Hs Decomposition Engine  |  Manifold on Paper  |  3D Polar Slice Stack")
    c.drawRightString(W - MARGIN - 20, y,
                      "Peter Higgins / Rogue Wave Audio / CC BY 4.0")
    c.setFont("Helvetica", 5)
    c.drawCentredString(CX, y - 8,
                        f"{experiment_id} — Generated by hs_manifold_paper.py — Hs Standards Edition")
    c.restoreState()


def draw_manifold_view(pdf, slices, trajectory, carriers, azimuth, elevation,
                       view_cx, view_cy, scale_xz, scale_y,
                       draw_labels=True, draw_mesh=True, draw_years=True,
                       viewport_w=None, viewport_h=None):
    """
    Render the 3D manifold at a given viewing angle.

    Draws: slice polygons (colour-ramped), surface mesh connecting carrier
    vertices between slices, year labels, carrier legend.
    """
    N = len(slices)
    D = len(slices[0]) if slices else 0

    pdf.saveState()

    # ── Draw surface mesh lines (carrier traces between slices) ──
    if draw_mesh and N > 1:
        for j in range(D):
            col = CARRIER_COLOURS[j % len(CARRIER_COLOURS)]
            pdf.setStrokeColor(Color(col.red, col.green, col.blue, alpha=0.2))
            pdf.setLineWidth(0.4)
            for i in range(N - 1):
                x1, y1, z1 = slices[i][j]
                x2, y2, z2 = slices[i + 1][j]
                sx1, sy1, _ = project_3d(x1, y1, z1, azimuth, elevation, view_cx, view_cy, scale_xz, scale_y)
                sx2, sy2, _ = project_3d(x2, y2, z2, azimuth, elevation, view_cx, view_cy, scale_xz, scale_y)
                pdf.line(sx1, sy1, sx2, sy2)

    # ── Draw slice polygons (bottom to top for proper overlap) ──
    # Determine draw order based on depth
    slice_depths = []
    for i in range(N):
        avg_depth = sum(project_3d(x, y, z, azimuth, elevation, 0, 0, 1, 1)[2]
                        for x, y, z in slices[i]) / max(D, 1)
        slice_depths.append((avg_depth, i))
    slice_depths.sort()  # draw far slices first

    for _, i in slice_depths:
        frac = i / max(N - 1, 1)
        col = colour_for_frac(frac)
        point = trajectory[i]
        verts_2d = []
        for j in range(D):
            x, y, z = slices[i][j]
            sx, sy, _ = project_3d(x, y, z, azimuth, elevation, view_cx, view_cy, scale_xz, scale_y)
            verts_2d.append((sx, sy))

        # Draw filled polygon
        path = pdf.beginPath()
        path.moveTo(verts_2d[0][0], verts_2d[0][1])
        for sx, sy in verts_2d[1:]:
            path.lineTo(sx, sy)
        path.close()
        pdf.setFillColor(Color(col.red, col.green, col.blue, alpha=0.12))
        pdf.setStrokeColor(Color(col.red, col.green, col.blue, alpha=0.7))
        pdf.setLineWidth(0.6)
        pdf.drawPath(path, fill=1, stroke=1)

        # Vertex dots
        for j, (sx, sy) in enumerate(verts_2d):
            pdf.setFillColor(Color(col.red, col.green, col.blue, alpha=0.8))
            pdf.circle(sx, sy, 1.2, fill=1, stroke=0)

        # Year label
        if draw_years:
            year_label = str(point.get("year", f"t={i}"))
            # Place label at the rightmost vertex
            rightmost = max(verts_2d, key=lambda p: p[0])
            # Only label every Nth interval for readability
            label_every = max(1, N // 12)
            if i % label_every == 0 or i == 0 or i == N - 1:
                pdf.setFillColor(Color(col.red, col.green, col.blue, alpha=0.9))
                pdf.setFont("Helvetica", 5)
                pdf.drawString(rightmost[0] + 4, rightmost[1] - 2, year_label)

    # ── Draw bolder outlines for first and last slices ──
    for i_special, lw, scol in [(0, 1.5, C_START), (N - 1, 1.5, C_END)]:
        verts_2d = []
        for j in range(D):
            x, y, z = slices[i_special][j]
            sx, sy, _ = project_3d(x, y, z, azimuth, elevation, view_cx, view_cy, scale_xz, scale_y)
            verts_2d.append((sx, sy))
        path = pdf.beginPath()
        path.moveTo(verts_2d[0][0], verts_2d[0][1])
        for sx, sy in verts_2d[1:]:
            path.lineTo(sx, sy)
        path.close()
        pdf.setStrokeColor(scol)
        pdf.setLineWidth(lw)
        pdf.setFillColor(Color(0, 0, 0, alpha=0))
        pdf.drawPath(path, fill=0, stroke=1)

    pdf.restoreState()


def draw_main_manifold(pdf, slices, trajectory, carriers, experiment_id, test_object, total_pages):
    """Page 1: Full manifold at optimal viewing angle."""
    N = len(trajectory)
    D = trajectory[0]["D"] if trajectory else 0

    # Find best viewing angle
    best_az, best_el = find_best_angle(slices)

    draw_page_header(pdf,
                     "MANIFOLD ON PAPER",
                     f"{experiment_id}  |  {test_object}  |  N={N}, D={D}  |  "
                     f"Azimuth={math.degrees(best_az):.0f}°  Elevation={math.degrees(best_el):.0f}°",
                     experiment_id, 1, total_pages)

    # Available drawing region (between header and legend/footer)
    region_top = H - MARGIN - 35
    region_bot = MARGIN + 75
    region_left = MARGIN + 10
    region_right = W - MARGIN - 35  # room for time bar
    region_w = region_right - region_left
    region_h = region_top - region_bot

    # First pass: compute projected bounding box at unit scale to find extent
    xs_test, ys_test = [], []
    for sl in slices:
        for (x, y, z) in sl:
            sx, sy, _ = project_3d(x, y, z, best_az, best_el, 0, 0, 1, 1)
            xs_test.append(sx)
            ys_test.append(sy)

    if xs_test:
        bx_min, bx_max = min(xs_test), max(xs_test)
        by_min, by_max = min(ys_test), max(ys_test)
        bw = bx_max - bx_min if bx_max > bx_min else 1
        bh = by_max - by_min if by_max > by_min else 1

        # Scale to fit with 15% padding
        fit_scale_x = region_w * 0.85 / bw
        fit_scale_y = region_h * 0.85 / bh
        fit_scale = min(fit_scale_x, fit_scale_y)
        scale_xz = fit_scale
        scale_y = fit_scale

        # Recompute actual projected positions at the chosen scale
        xs2, ys2 = [], []
        for sl in slices:
            for (x, y, z) in sl:
                sx, sy, _ = project_3d(x, y, z, best_az, best_el, 0, 0, fit_scale, fit_scale)
                xs2.append(sx)
                ys2.append(sy)

        actual_cx = (min(xs2) + max(xs2)) / 2
        actual_cy = (min(ys2) + max(ys2)) / 2
        target_cx = (region_left + region_right) / 2
        target_cy = (region_bot + region_top) / 2

        plot_cx = target_cx - actual_cx
        plot_cy = target_cy - actual_cy
    else:
        scale_xz = region_w * 0.4
        scale_y = region_h * 0.4
        plot_cx = CX
        plot_cy = CY

    # Draw the manifold
    draw_manifold_view(pdf, slices, trajectory, carriers,
                       best_az, best_el,
                       plot_cx, plot_cy, scale_xz, scale_y,
                       draw_labels=True, draw_mesh=True, draw_years=True)

    # ── Carrier legend ──
    carrier_names = trajectory[0].get("carrier_names", carriers[:D])
    if not carrier_names or len(carrier_names) < D:
        carrier_names = [f"CLR{j+1}" for j in range(D)]

    legend_y = MARGIN + 50
    legend_x = MARGIN + 25
    pdf.setFont("Helvetica-Bold", 6)
    pdf.setFillColor(C_BODY)
    pdf.drawString(legend_x, legend_y + 12, "Carriers:")

    cols = min(D, 6)
    col_w = (W - 2 * MARGIN - 40) / cols
    for j in range(D):
        col_idx = j % cols
        row_idx = j // cols
        lx = legend_x + col_idx * col_w
        ly = legend_y - row_idx * 10
        pdf.setFillColor(CARRIER_COLOURS[j % len(CARRIER_COLOURS)])
        pdf.circle(lx + 3, ly + 2, 2.5, fill=1, stroke=0)
        pdf.setFont("Helvetica", 5.5)
        pdf.drawString(lx + 8, ly, carrier_names[j])

    # ── Time colour bar ──
    bar_x = W - MARGIN - 20
    bar_y_bot = MARGIN + 80
    bar_h = region_h * 0.55
    bar_w = 8
    n_seg = 30
    for s in range(n_seg):
        f = s / n_seg
        col = colour_for_frac(f)
        seg_y = bar_y_bot + bar_h * f
        seg_h = bar_h / n_seg + 0.5
        pdf.setFillColor(col)
        pdf.rect(bar_x, seg_y, bar_w, seg_h, fill=1, stroke=0)

    pdf.setFillColor(C_START)
    pdf.setFont("Helvetica", 5)
    y0_label = str(trajectory[0].get("year", "t=0"))
    yn_label = str(trajectory[-1].get("year", f"t={N-1}"))
    pdf.drawCentredString(bar_x + bar_w / 2, bar_y_bot - 10, y0_label)
    pdf.setFillColor(C_END)
    pdf.drawCentredString(bar_x + bar_w / 2, bar_y_bot + bar_h + 5, yn_label)
    pdf.setFillColor(C_MUTED)
    pdf.setFont("Helvetica", 5)
    pdf.saveState()
    pdf.translate(bar_x + bar_w + 8, bar_y_bot + bar_h / 2)
    pdf.rotate(90)
    pdf.drawCentredString(0, 0, "TIME")
    pdf.restoreState()

    # ── Summary strip ──
    strip_y = MARGIN + 30
    pdf.setFillColor(C_TAG_BG)
    pdf.setStrokeColor(C_TAG_BRD)
    pdf.setLineWidth(0.3)
    pdf.roundRect(MARGIN + 15, strip_y - 5, W - 2 * MARGIN - 30, 16, 3, fill=1, stroke=1)

    norms = [p["aitch_norm"] for p in trajectory]
    pdf.setFont("Helvetica", 5.5)
    pdf.setFillColor(C_BODY)
    stats = (f"||x||_A range: {min(norms):.2f} .. {max(norms):.2f}   |   "
             f"N={N}   D={D}   |   "
             f"Polar slices stacked along time axis in projected 3-space   |   "
             f"View: az={math.degrees(best_az):.0f}°  el={math.degrees(best_el):.0f}°")
    pdf.drawCentredString(CX, strip_y, stats)

    draw_page_footer(pdf, experiment_id)


def draw_three_panel(pdf, slices, trajectory, carriers, experiment_id, test_object, total_pages):
    """Page 2: Three-panel view — front, 3/4, top-down."""
    N = len(trajectory)
    D = trajectory[0]["D"] if trajectory else 0

    draw_page_header(pdf,
                     "THREE-PANEL PROJECTION",
                     f"{experiment_id}  |  {test_object}  |  Front / Three-Quarter / Plan",
                     experiment_id, 2, total_pages)

    # Three viewports
    views = [
        ("FRONT", math.radians(0), math.radians(5)),
        ("3/4 VIEW", math.radians(35), math.radians(20)),
        ("PLAN (TOP)", math.radians(0), math.radians(85)),
    ]

    panel_w = (W - 2 * MARGIN - 40) / 3
    panel_h = H - 2 * MARGIN - 100
    panel_y = MARGIN + 40

    for vi, (label, az, el) in enumerate(views):
        px = MARGIN + 20 + vi * (panel_w + 10)
        pcx = px + panel_w / 2
        pcy = panel_y + panel_h / 2

        # Panel border
        pdf.setStrokeColor(C_GRID)
        pdf.setLineWidth(0.5)
        pdf.rect(px, panel_y, panel_w, panel_h, fill=0, stroke=1)

        # Panel label
        pdf.setFillColor(C_ACCENT)
        pdf.setFont("Helvetica-Bold", 7)
        pdf.drawCentredString(pcx, panel_y + panel_h + 5, label)

        # Scale for panel
        scale_xz = panel_w * 0.35
        scale_y = panel_h * 0.35

        # Clip-ish rendering (just scale to fit)
        pdf.saveState()
        draw_manifold_view(pdf, slices, trajectory, carriers,
                           az, el, pcx, pcy, scale_xz, scale_y,
                           draw_labels=False, draw_mesh=True, draw_years=False)
        pdf.restoreState()

        # Angle label
        pdf.setFillColor(C_MUTED)
        pdf.setFont("Helvetica", 5)
        pdf.drawCentredString(pcx, panel_y + 5,
                              f"az={math.degrees(az):.0f}°  el={math.degrees(el):.0f}°")

    draw_page_footer(pdf, experiment_id)


def draw_carrier_traces(pdf, slices, trajectory, carriers, experiment_id, test_object, total_pages):
    """Page 3: Individual carrier trajectory traces — one line per carrier in 3D."""
    N = len(trajectory)
    D = trajectory[0]["D"] if trajectory else 0
    carrier_names = trajectory[0].get("carrier_names", carriers[:D])
    if not carrier_names or len(carrier_names) < D:
        carrier_names = [f"CLR{j+1}" for j in range(D)]

    draw_page_header(pdf,
                     "CARRIER TRACE SEPARATION",
                     f"{experiment_id}  |  {test_object}  |  Individual carrier paths through manifold",
                     experiment_id, 3, total_pages)

    # Use optimal angle
    best_az, best_el = find_best_angle(slices)

    # Drawing area
    plot_cx = CX
    plot_cy = CY + 10
    avail_w = W - 2 * MARGIN - 80
    avail_h = H - 2 * MARGIN - 140
    scale_xz = min(avail_w, avail_h) * 0.42
    scale_y = avail_h * 0.38

    pdf.saveState()

    # Draw each carrier's trace as a bold coloured line
    for j in range(D):
        col = CARRIER_COLOURS[j % len(CARRIER_COLOURS)]
        pdf.setStrokeColor(col)
        pdf.setLineWidth(1.2)

        for i in range(N - 1):
            x1, y1, z1 = slices[i][j]
            x2, y2, z2 = slices[i + 1][j]
            sx1, sy1, _ = project_3d(x1, y1, z1, best_az, best_el, plot_cx, plot_cy, scale_xz, scale_y)
            sx2, sy2, _ = project_3d(x2, y2, z2, best_az, best_el, plot_cx, plot_cy, scale_xz, scale_y)
            pdf.line(sx1, sy1, sx2, sy2)

        # Dot at start and end
        sx_s, sy_s, _ = project_3d(*slices[0][j], best_az, best_el, plot_cx, plot_cy, scale_xz, scale_y)
        sx_e, sy_e, _ = project_3d(*slices[-1][j], best_az, best_el, plot_cx, plot_cy, scale_xz, scale_y)
        pdf.setFillColor(C_START)
        pdf.circle(sx_s, sy_s, 2, fill=1, stroke=0)
        pdf.setFillColor(C_END)
        pdf.circle(sx_e, sy_e, 2, fill=1, stroke=0)

        # Label at end
        pdf.setFillColor(col)
        pdf.setFont("Helvetica-Bold", 5.5)
        pdf.drawString(sx_e + 4, sy_e - 2, carrier_names[j])

    pdf.restoreState()

    # ── Legend table: carrier CLR range ──
    table_y = MARGIN + 45
    pdf.setFont("Helvetica-Bold", 6)
    pdf.setFillColor(C_BODY)
    pdf.drawString(MARGIN + 25, table_y + 14, "Carrier CLR Range:")

    cols = min(D, 4)
    col_w = (W - 2 * MARGIN - 50) / cols
    for j in range(D):
        clr_vals = [trajectory[i]["clr"][j] for i in range(N)]
        col_idx = j % cols
        row_idx = j // cols
        lx = MARGIN + 25 + col_idx * col_w
        ly = table_y - row_idx * 10
        pdf.setFillColor(CARRIER_COLOURS[j % len(CARRIER_COLOURS)])
        pdf.setFont("Helvetica", 5)
        pdf.drawString(lx, ly, f"{carrier_names[j]}: {min(clr_vals):.1f} .. {max(clr_vals):.1f}")

    draw_page_footer(pdf, experiment_id)


def normalise_data(data):
    """Normalise pipeline data for processing."""
    if "steps" in data and isinstance(data["steps"], list):
        steps_dict = {}
        for i, step in enumerate(data["steps"]):
            if isinstance(step, dict):
                for k, v in step.items():
                    steps_dict[k] = v
        data["steps"] = steps_dict
    return data


def build_manifold_paper_pdf(results_json, output_pdf):
    """Main builder — reads pipeline results JSON, produces manifold-on-paper PDF."""

    with open(results_json, 'r') as f:
        data = json.load(f)

    data = normalise_data(data)

    experiment_id = data.get("experiment_id",
                      data.get("experiment",
                      data.get("experiment", "UNKNOWN")))
    test_object = data.get("name",
                   data.get("test_object",
                   data.get("experiment", experiment_id)))
    carriers = data.get("carriers", [])

    trajectory, carriers = extract_full_trajectory(data)
    if len(trajectory) < 2:
        print(f"  WARNING: Not enough trajectory points ({len(trajectory)}). Skipping.")
        return output_pdf

    N = len(trajectory)
    D = trajectory[0]["D"]

    # Find global max CLR for consistent scaling
    all_max = 0
    for p in trajectory:
        for v in p["clr"]:
            all_max = max(all_max, abs(v))
    if all_max < 0.001:
        all_max = 1.0

    # Build 3D slice vertices
    slices = build_slice_vertices(trajectory, all_max)

    total_pages = 3

    pdf = canvas.Canvas(output_pdf, pagesize=A4)
    pdf.setTitle(f"Hs Manifold on Paper — {experiment_id}")
    pdf.setAuthor("Hs Decomposition Engine")

    # Page 1: Main manifold view
    draw_main_manifold(pdf, slices, trajectory, carriers, experiment_id, test_object, total_pages)
    pdf.showPage()

    # Page 2: Three-panel comparison
    draw_three_panel(pdf, slices, trajectory, carriers, experiment_id, test_object, total_pages)
    pdf.showPage()

    # Page 3: Carrier traces
    draw_carrier_traces(pdf, slices, trajectory, carriers, experiment_id, test_object, total_pages)
    pdf.showPage()

    pdf.save()
    print(f"Generated: {output_pdf} ({total_pages} pages, {N} intervals, {D} carriers)")
    return output_pdf


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hs_manifold_paper.py <results.json> [output.pdf]")
        sys.exit(1)

    results_json = sys.argv[1]
    if len(sys.argv) >= 3:
        output_pdf = sys.argv[2]
    else:
        base = os.path.splitext(results_json)[0]
        output_pdf = base.replace("_results", "_manifold_paper") + ".pdf"

    build_manifold_paper_pdf(results_json, output_pdf)
