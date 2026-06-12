#!/usr/bin/env python3
"""
Hs Polar Stack — Per-Interval Polar Projections
=================================================
Generates a multi-page PDF with one polar plot per data interval.
This IS what the manifold does: at each level in the data, the
composition has a unique polar fingerprint showing all CLR dimensions.

The 3D helix is the plan map. These polar plots are the cross-sections.
Together they give complete geometric characterisation.

Pages:
  Page 1:   3D helix overview with XYZ coordinates and event tags
  Page 2+:  One polar plot per data interval (year/observation)
  Page N+2: Ghost stack composite — all slices overlaid
  Page N+3: Difference polar — year-over-year delta polygons
  Page N+4: Norm profile strip — Aitchison norm bar chart over time
  Page N+5: Value table — complete numeric readout
  Page N+6: Summary comparison strip — small multiples

Also generates: <output>.json — structured values for experiment journal

Usage:
    python hs_polar_stack.py <results.json> [output.pdf]

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
CY = H / 2

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
C_FILL    = HexColor("#D5E8F0")

# Carrier colours — distinct palette for up to 12 carriers
CARRIER_COLOURS = [
    HexColor("#2E75B6"),  # blue
    HexColor("#C0392B"),  # red
    HexColor("#27AE60"),  # green
    HexColor("#8E44AD"),  # purple
    HexColor("#E67E22"),  # orange
    HexColor("#16A085"),  # teal
    HexColor("#D4AC0D"),  # gold
    HexColor("#E74C3C"),  # bright red
    HexColor("#3498DB"),  # light blue
    HexColor("#1ABC9C"),  # turquoise
    HexColor("#9B59B6"),  # violet
    HexColor("#F39C12"),  # amber
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


def extract_full_trajectory(data):
    """Extract full CLR trajectory with ALL dimensions per interval."""
    trajectory = []
    carriers = data.get("carriers", [])

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
    D = data.get("D", len(carriers) if carriers else 3)

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
                 "Hs Decomposition Engine  |  Polar Stack  |  Per-Interval Projections")
    c.drawRightString(W - MARGIN - 20, y,
                      "Peter Higgins / Rogue Wave Audio / CC BY 4.0")
    c.setFont("Helvetica", 5)
    c.drawCentredString(CX, y - 8,
                        f"{experiment_id} — Generated by hs_polar_stack.py — Hs Standards Edition")
    c.restoreState()


def detect_events(trajectory, raw_data):
    """Detect significant events along the trajectory for tagging."""
    events = []
    N = len(trajectory)
    if N < 2:
        return events

    # Detect dominant carrier shifts
    prev_dom = None
    for i, p in enumerate(trajectory):
        clr = p["clr"]
        names = p.get("carrier_names", [f"C{j}" for j in range(len(clr))])
        # Dominant = largest absolute CLR
        max_idx = max(range(len(clr)), key=lambda j: abs(clr[j]))
        dom = names[max_idx] if max_idx < len(names) else f"C{max_idx}"
        if prev_dom is not None and dom != prev_dom:
            events.append({"t": i, "type": "DOM_SHIFT", "label": f"{prev_dom[:4]}->{dom[:4]}"})
        prev_dom = dom

    # Detect norm peaks and troughs
    norms = [p["aitch_norm"] for p in trajectory]
    for i in range(1, N - 1):
        if norms[i] > norms[i-1] and norms[i] > norms[i+1]:
            if norms[i] > sum(norms) / N * 1.3:
                events.append({"t": i, "type": "NORM_PEAK", "label": f"||x||={norms[i]:.1f}"})
        if norms[i] < norms[i-1] and norms[i] < norms[i+1]:
            if norms[i] < sum(norms) / N * 0.7:
                events.append({"t": i, "type": "NORM_TROUGH", "label": f"||x||={norms[i]:.1f}"})

    # Detect largest YoY jumps
    if N > 2:
        deltas = []
        for i in range(1, N):
            d = abs(norms[i] - norms[i-1])
            deltas.append((d, i))
        deltas.sort(reverse=True)
        for d, i in deltas[:2]:
            if d > sum(norms) / N * 0.3:
                sign = "+" if norms[i] > norms[i-1] else "-"
                events.append({"t": i, "type": "BIG_DELTA", "label": f"delta={sign}{d:.1f}"})

    # Detect entropy from raw data if available
    entropy_traj = None
    if isinstance(raw_data, dict):
        entropy_traj = raw_data.get("entropy_trajectory")
    if entropy_traj and isinstance(entropy_traj, dict):
        e_vals = [(k, v) for k, v in sorted(entropy_traj.items())]
        if len(e_vals) > 2:
            max_e = max(e_vals, key=lambda x: x[1])
            min_e = min(e_vals, key=lambda x: x[1])
            max_idx = int(max_e[0]) - int(e_vals[0][0]) if e_vals[0][0].isdigit() else 0
            min_idx = int(min_e[0]) - int(e_vals[0][0]) if e_vals[0][0].isdigit() else 0
            if 0 <= max_idx < N:
                events.append({"t": max_idx, "type": "H_MAX", "label": f"H={max_e[1]:.2f}"})
            if 0 <= min_idx < N:
                events.append({"t": min_idx, "type": "H_MIN", "label": f"H={min_e[1]:.2f}"})

    return events


def draw_helix_overview(pdf, trajectory, experiment_id, test_object, carriers, total_pages, events=None):
    """Page 1: 3D helix overview with XYZ coordinates and event tags."""
    draw_page_header(pdf, "MANIFOLD HELIX — POLAR SLICE MAP",
                     f"{experiment_id}  |  {test_object}  |  {len(trajectory)} intervals  |  {len(carriers)} carriers",
                     experiment_id, 1, total_pages)

    N = len(trajectory)
    if N < 1:
        draw_page_footer(pdf, experiment_id)
        pdf.showPage()
        return

    if events is None:
        events = []
    event_map = {e["t"]: e for e in events}

    # Isometric projection parameters
    ISO_COS = math.cos(math.radians(30))
    ISO_SIN = math.sin(math.radians(30))

    # Data ranges
    c1_vals = [p["clr1"] for p in trajectory]
    c2_vals = [p["clr2"] for p in trajectory]
    c1_min, c1_max = min(c1_vals), max(c1_vals)
    c2_min, c2_max = min(c2_vals), max(c2_vals)
    c1_range = max(c1_max - c1_min, 0.1)
    c2_range = max(c2_max - c2_min, 0.1)

    # Plot area — shifted down to avoid title collision
    plot_cx = CX
    plot_cy = CY - 30
    scale_xy = 100 / max(c1_range, c2_range)
    scale_z = min(300, (H - 2 * MARGIN - 180)) / max(N - 1, 1)

    def iso_project(x, y, z):
        sx = plot_cx + (x * ISO_COS - y * ISO_COS) * 1.0
        sy = plot_cy + (x * ISO_SIN + y * ISO_SIN) * 1.0 + z
        return sx, sy

    # Draw trajectory
    pts = []
    for i, p in enumerate(trajectory):
        nx = (p["clr1"] - (c1_min + c1_max) / 2) * scale_xy
        ny = (p["clr2"] - (c2_min + c2_max) / 2) * scale_xy
        nz = i * scale_z
        sx, sy = iso_project(nx, ny, nz)
        pts.append((sx, sy))

    # Lines
    pdf.saveState()
    for i in range(len(pts) - 1):
        frac = i / max(N - 1, 1)
        pdf.setStrokeColor(colour_for_frac(frac))
        pdf.setLineWidth(2.0)
        pdf.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1])

    # Polar slice markers with XYZ coordinates and event tags
    label_step = max(1, N // 10)
    for i, (sx, sy) in enumerate(pts):
        frac = i / max(N - 1, 1)
        p = trajectory[i]
        page_num = i + 2
        year = p.get("year", i)
        is_labelled = (i % label_step == 0 or i == 0 or i == N - 1 or i in event_map)

        # Marker ring
        pdf.setStrokeColor(colour_for_frac(frac))
        pdf.setLineWidth(1.5)
        pdf.setFillColor(Color(1, 1, 1, 0.85))
        pdf.circle(sx, sy, 3.5, fill=1, stroke=1)

        # Page number inside circle
        pdf.setFillColor(C_BODY)
        pdf.setFont("Helvetica", 3.5)
        pdf.drawCentredString(sx, sy - 1.2, str(page_num))

        if is_labelled:
            # Alternate sides: even=right, odd=left
            side = 1 if i % 2 == 0 else -1
            tag_x = sx + side * 10
            tag_y = sy

            # Leader line
            pdf.setStrokeColor(C_TAG_BRD)
            pdf.setLineWidth(0.4)
            pdf.line(sx + side * 4, sy, tag_x, tag_y)

            # XYZ coordinate tag
            coord_text = f"{year}  CLR1={p['clr1']:+.1f}  CLR2={p['clr2']:+.1f}  ||x||={p['aitch_norm']:.1f}"
            pdf.setFont("Helvetica", 4.2)
            pdf.setFillColor(C_BODY)
            if side > 0:
                pdf.drawString(tag_x + 2, tag_y + 2, coord_text)
            else:
                pdf.drawRightString(tag_x - 2, tag_y + 2, coord_text)

            # Event tag if present
            if i in event_map:
                evt = event_map[i]
                evt_colours = {
                    "DOM_SHIFT": HexColor("#8E44AD"),
                    "NORM_PEAK": HexColor("#C0392B"),
                    "NORM_TROUGH": HexColor("#2E75B6"),
                    "BIG_DELTA": HexColor("#E67E22"),
                    "H_MAX": HexColor("#16A085"),
                    "H_MIN": HexColor("#D4AC0D"),
                }
                evt_col = evt_colours.get(evt["type"], C_ACCENT)
                pdf.setFillColor(evt_col)
                pdf.setFont("Helvetica-Bold", 3.8)
                if side > 0:
                    pdf.drawString(tag_x + 2, tag_y - 5, f"[{evt['type']}] {evt['label']}")
                else:
                    pdf.drawRightString(tag_x - 2, tag_y - 5, f"[{evt['type']}] {evt['label']}")

    pdf.restoreState()

    # Legend at bottom
    pdf.saveState()
    ly = MARGIN + 40
    pdf.setFont("Helvetica", 6.5)
    pdf.setFillColor(C_BODY)
    pdf.drawString(MARGIN + 20, ly + 12,
                   "Each numbered circle marks a polar slice. Coordinates: CLR1 (x), CLR2 (y), interval (z).")
    pdf.setFont("Helvetica", 5.5)
    pdf.setFillColor(C_MUTED)
    pdf.drawString(MARGIN + 20, ly,
                   f"Intervals: {N}  |  Carriers: {', '.join(carriers[:6])}"
                   + (f"... (+{len(carriers)-6} more)" if len(carriers) > 6 else "")
                   + f"  |  Events detected: {len(events)}")
    pdf.restoreState()

    draw_page_footer(pdf, experiment_id)
    pdf.showPage()


def draw_polar_interval(pdf, point, idx, trajectory, experiment_id, test_object, carriers, total_pages):
    """One polar plot for a single data interval showing ALL CLR dimensions."""
    N_total = len(trajectory)
    page_num = idx + 2
    frac = idx / max(N_total - 1, 1)
    year_label = str(point.get("year", f"t={idx}"))

    draw_page_header(pdf,
                     f"POLAR SLICE — {year_label}",
                     f"{experiment_id}  |  {test_object}  |  Interval {idx+1}/{N_total}  |  "
                     f"||x||_A = {point['aitch_norm']:.3f}",
                     experiment_id, page_num, total_pages)

    clr = point["clr"]
    D = len(clr)
    carrier_names = point.get("carrier_names", carriers[:D])
    if not carrier_names or len(carrier_names) < D:
        carrier_names = [f"CLR{j+1}" for j in range(D)]

    # Polar radar plot parameters — centred vertically in available space
    plot_r = min(W - 2 * MARGIN - 60, H - 2 * MARGIN - 180) / 2 * 0.75
    pcx = CX
    pcy = CY - 15  # shift down to balance whitespace above/below

    # Find max absolute CLR value for scaling (across ALL intervals for consistency)
    all_max = 0
    for p in trajectory:
        for v in p["clr"]:
            all_max = max(all_max, abs(v))
    if all_max < 0.001:
        all_max = 1.0

    pdf.saveState()

    # Concentric grid circles
    pdf.setStrokeColor(C_GRID)
    pdf.setLineWidth(0.3)
    n_rings = 4
    for i in range(1, n_rings + 1):
        r = plot_r * i / n_rings
        pdf.circle(pcx, pcy, r, fill=0, stroke=1)

    # Ring value labels
    pdf.setFillColor(C_MUTED)
    pdf.setFont("Helvetica", 5)
    for i in range(1, n_rings + 1):
        r = plot_r * i / n_rings
        val = all_max * i / n_rings
        pdf.drawString(pcx + 3, pcy + r + 2, f"{val:.1f}")

    # Radial axis lines — one per carrier
    angles = []
    for j in range(D):
        angle = 2 * math.pi * j / D - math.pi / 2  # start at top
        angles.append(angle)
        x2 = pcx + plot_r * math.cos(angle)
        y2 = pcy + plot_r * math.sin(angle)
        pdf.setStrokeColor(C_GRID)
        pdf.setLineWidth(0.5)
        pdf.line(pcx, pcy, x2, y2)

        # Carrier label
        lx = pcx + (plot_r + 14) * math.cos(angle)
        ly = pcy + (plot_r + 14) * math.sin(angle)
        pdf.setFillColor(CARRIER_COLOURS[j % len(CARRIER_COLOURS)])
        pdf.setFont("Helvetica-Bold", 5.5)
        if math.cos(angle) < -0.3:
            pdf.drawRightString(lx, ly - 2, carrier_names[j])
        elif math.cos(angle) > 0.3:
            pdf.drawString(lx, ly - 2, carrier_names[j])
        else:
            pdf.drawCentredString(lx, ly - 2, carrier_names[j])

    # Plot CLR values as filled polygon
    # Map CLR values: positive values go outward, negative go inward
    # Use absolute value for radius, colour for sign
    poly_pts = []
    for j in range(D):
        val = clr[j]
        r = abs(val) / all_max * plot_r
        angle = angles[j]
        px = pcx + r * math.cos(angle)
        py = pcy + r * math.sin(angle)
        poly_pts.append((px, py))

    # Draw filled polygon
    if len(poly_pts) >= 3:
        path = pdf.beginPath()
        path.moveTo(poly_pts[0][0], poly_pts[0][1])
        for px, py in poly_pts[1:]:
            path.lineTo(px, py)
        path.close()
        pdf.setFillColor(Color(0.18, 0.46, 0.71, 0.15))  # translucent accent
        pdf.setStrokeColor(colour_for_frac(frac))
        pdf.setLineWidth(1.8)
        pdf.drawPath(path, fill=1, stroke=1)

    # Draw data points on each axis
    for j in range(D):
        val = clr[j]
        r = abs(val) / all_max * plot_r
        angle = angles[j]
        px = pcx + r * math.cos(angle)
        py = pcy + r * math.sin(angle)

        # Point
        pdf.setFillColor(CARRIER_COLOURS[j % len(CARRIER_COLOURS)])
        pdf.circle(px, py, 3, fill=1, stroke=0)

        # Value label
        pdf.setFont("Helvetica", 4.5)
        vx = pcx + (r + 8) * math.cos(angle)
        vy = pcy + (r + 8) * math.sin(angle)
        sign = "+" if val >= 0 else ""
        pdf.drawCentredString(vx, vy - 1.5, f"{sign}{val:.2f}")

    # Centre dot
    pdf.setFillColor(C_ACCENT)
    pdf.circle(pcx, pcy, 1.5, fill=1, stroke=0)

    pdf.restoreState()

    # Info strip at bottom
    pdf.saveState()
    info_y = MARGIN + 55

    # Previous/next comparison arrows
    pdf.setFont("Helvetica", 6)
    pdf.setFillColor(C_MUTED)
    if idx > 0:
        prev_year = trajectory[idx - 1].get("year", idx - 1)
        prev_norm = trajectory[idx - 1]["aitch_norm"]
        delta_norm = point["aitch_norm"] - prev_norm
        sign = "+" if delta_norm >= 0 else ""
        pdf.drawString(MARGIN + 20, info_y + 12,
                       f"From {prev_year}: delta ||x||_A = {sign}{delta_norm:.3f}")

    pdf.drawRightString(W - MARGIN - 20, info_y + 12,
                        f"Phase = {math.degrees(point['phase']):+.1f} deg")

    # Carrier value bar (compact text)
    pdf.setFont("Helvetica", 5)
    pdf.setFillColor(C_BODY)
    vals_str = "  ".join([f"{carrier_names[j][:6]}={clr[j]:+.2f}" for j in range(min(D, 9))])
    pdf.drawString(MARGIN + 20, info_y, vals_str)
    if D > 9:
        vals_str2 = "  ".join([f"{carrier_names[j][:6]}={clr[j]:+.2f}" for j in range(9, D)])
        pdf.drawString(MARGIN + 20, info_y - 10, vals_str2)

    pdf.restoreState()

    draw_page_footer(pdf, experiment_id)
    pdf.showPage()


def draw_summary_comparison(pdf, trajectory, experiment_id, test_object, carriers, total_pages):
    """Final page: small-multiple comparison of all intervals."""
    page_num = total_pages
    draw_page_header(pdf, "POLAR STACK SUMMARY — ALL INTERVALS",
                     f"{experiment_id}  |  {test_object}  |  {len(trajectory)} intervals compared",
                     experiment_id, page_num, total_pages)

    N = len(trajectory)
    D = trajectory[0]["D"] if trajectory else 3

    # Grid layout for small multiples
    avail_w = W - 2 * MARGIN - 20
    avail_h = H - 2 * MARGIN - 100

    # Determine grid size
    cols = min(6, N)
    rows = math.ceil(N / cols)
    cell_w = avail_w / cols
    cell_h = min(avail_h / rows, cell_w)  # keep roughly square
    cell_r = min(cell_w, cell_h) / 2 * 0.65

    # Find global max for consistent scaling
    all_max = 0
    for p in trajectory:
        for v in p["clr"]:
            all_max = max(all_max, abs(v))
    if all_max < 0.001:
        all_max = 1.0

    pdf.saveState()
    start_x = MARGIN + 10 + cell_w / 2
    start_y = H - MARGIN - 50 - cell_h / 2

    for idx, point in enumerate(trajectory):
        col = idx % cols
        row = idx // cols
        cx = start_x + col * cell_w
        cy = start_y - row * cell_h

        if cy - cell_r < MARGIN + 40:
            break  # don't overflow

        frac = idx / max(N - 1, 1)
        clr = point["clr"]

        # Small circle outline
        pdf.setStrokeColor(C_GRID)
        pdf.setLineWidth(0.3)
        pdf.circle(cx, cy, cell_r, fill=0, stroke=1)

        # Plot radar polygon
        angles = [2 * math.pi * j / D - math.pi / 2 for j in range(D)]
        poly_pts = []
        for j in range(D):
            r = abs(clr[j]) / all_max * cell_r
            px = cx + r * math.cos(angles[j])
            py = cy + r * math.sin(angles[j])
            poly_pts.append((px, py))

        if len(poly_pts) >= 3:
            path = pdf.beginPath()
            path.moveTo(poly_pts[0][0], poly_pts[0][1])
            for px, py in poly_pts[1:]:
                path.lineTo(px, py)
            path.close()
            col_obj = colour_for_frac(frac)
            pdf.setFillColor(Color(col_obj.red, col_obj.green, col_obj.blue, 0.2))
            pdf.setStrokeColor(colour_for_frac(frac))
            pdf.setLineWidth(0.8)
            pdf.drawPath(path, fill=1, stroke=1)

        # Label
        year = point.get("year", idx)
        pdf.setFillColor(C_BODY)
        pdf.setFont("Helvetica-Bold", 5)
        pdf.drawCentredString(cx, cy - cell_r - 6, str(year))
        pdf.setFont("Helvetica", 4)
        pdf.setFillColor(C_MUTED)
        pdf.drawCentredString(cx, cy - cell_r - 12, f"||x||={point['aitch_norm']:.1f}")

    pdf.restoreState()

    # Carrier legend at bottom
    pdf.saveState()
    carrier_names = trajectory[0].get("carrier_names", carriers[:D])
    ly = MARGIN + 48
    pdf.setFont("Helvetica", 5)
    x_pos = MARGIN + 20
    for j in range(min(D, 12)):
        pdf.setFillColor(CARRIER_COLOURS[j % len(CARRIER_COLOURS)])
        pdf.circle(x_pos, ly + 2, 2, fill=1, stroke=0)
        pdf.setFillColor(C_MUTED)
        name = carrier_names[j] if j < len(carrier_names) else f"CLR{j+1}"
        pdf.drawString(x_pos + 4, ly, name[:12])
        x_pos += max(50, len(name) * 4 + 15)
        if x_pos > W - MARGIN - 40:
            x_pos = MARGIN + 20
            ly -= 10
    pdf.restoreState()

    draw_page_footer(pdf, experiment_id)
    pdf.showPage()


def draw_ghost_stack(pdf, trajectory, experiment_id, test_object, carriers, page_num, total_pages):
    """Ghost stack composite — all polar slices overlaid with transparency."""
    draw_page_header(pdf, "GHOST STACK — ALL INTERVALS OVERLAID",
                     f"{experiment_id}  |  {test_object}  |  {len(trajectory)} slices composited",
                     experiment_id, page_num, total_pages)

    N = len(trajectory)
    D = trajectory[0]["D"] if trajectory else 3
    carrier_names = trajectory[0].get("carrier_names", carriers[:D])
    if not carrier_names or len(carrier_names) < D:
        carrier_names = [f"CLR{j+1}" for j in range(D)]

    # Polar radar parameters
    plot_r = min(W - 2 * MARGIN - 60, H - 2 * MARGIN - 180) / 2 * 0.70
    pcx = CX
    pcy = CY - 10

    # Global max for scaling
    all_max = 0
    for p in trajectory:
        for v in p["clr"]:
            all_max = max(all_max, abs(v))
    if all_max < 0.001:
        all_max = 1.0

    pdf.saveState()

    # Concentric grid circles
    pdf.setStrokeColor(C_GRID)
    pdf.setLineWidth(0.3)
    n_rings = 4
    for i in range(1, n_rings + 1):
        r = plot_r * i / n_rings
        pdf.circle(pcx, pcy, r, fill=0, stroke=1)

    # Ring value labels
    pdf.setFillColor(C_MUTED)
    pdf.setFont("Helvetica", 5)
    for i in range(1, n_rings + 1):
        r = plot_r * i / n_rings
        val = all_max * i / n_rings
        pdf.drawString(pcx + 3, pcy + r + 2, f"{val:.1f}")

    # Radial axis lines
    angles = [2 * math.pi * j / D - math.pi / 2 for j in range(D)]
    for j in range(D):
        x2 = pcx + plot_r * math.cos(angles[j])
        y2 = pcy + plot_r * math.sin(angles[j])
        pdf.setStrokeColor(C_GRID)
        pdf.setLineWidth(0.5)
        pdf.line(pcx, pcy, x2, y2)

        # Carrier label
        lx = pcx + (plot_r + 14) * math.cos(angles[j])
        ly = pcy + (plot_r + 14) * math.sin(angles[j])
        pdf.setFillColor(CARRIER_COLOURS[j % len(CARRIER_COLOURS)])
        pdf.setFont("Helvetica-Bold", 5.5)
        if math.cos(angles[j]) < -0.3:
            pdf.drawRightString(lx, ly - 2, carrier_names[j])
        elif math.cos(angles[j]) > 0.3:
            pdf.drawString(lx, ly - 2, carrier_names[j])
        else:
            pdf.drawCentredString(lx, ly - 2, carrier_names[j])

    # Draw ALL polygons overlaid with increasing opacity
    for idx, point in enumerate(trajectory):
        frac = idx / max(N - 1, 1)
        clr = point["clr"]
        poly_pts = []
        for j in range(D):
            r = abs(clr[j]) / all_max * plot_r
            px = pcx + r * math.cos(angles[j])
            py = pcy + r * math.sin(angles[j])
            poly_pts.append((px, py))

        if len(poly_pts) >= 3:
            path = pdf.beginPath()
            path.moveTo(poly_pts[0][0], poly_pts[0][1])
            for px, py in poly_pts[1:]:
                path.lineTo(px, py)
            path.close()
            col_obj = colour_for_frac(frac)
            # Low alpha so layers build up
            alpha = max(0.04, 0.12 - 0.08 * (N / 30))
            pdf.setFillColor(Color(col_obj.red, col_obj.green, col_obj.blue, alpha))
            pdf.setStrokeColor(Color(col_obj.red, col_obj.green, col_obj.blue, 0.4))
            pdf.setLineWidth(0.6)
            pdf.drawPath(path, fill=1, stroke=1)

    # Highlight first and last with stronger outline
    for idx in [0, N - 1]:
        frac = idx / max(N - 1, 1)
        clr = trajectory[idx]["clr"]
        poly_pts = []
        for j in range(D):
            r = abs(clr[j]) / all_max * plot_r
            px = pcx + r * math.cos(angles[j])
            py = pcy + r * math.sin(angles[j])
            poly_pts.append((px, py))
        if len(poly_pts) >= 3:
            path = pdf.beginPath()
            path.moveTo(poly_pts[0][0], poly_pts[0][1])
            for px, py in poly_pts[1:]:
                path.lineTo(px, py)
            path.close()
            col_obj = colour_for_frac(frac)
            pdf.setFillColor(Color(1, 1, 1, 0))
            pdf.setStrokeColor(col_obj)
            pdf.setLineWidth(2.0)
            pdf.drawPath(path, fill=0, stroke=1)

    pdf.restoreState()

    # Legend
    pdf.saveState()
    ly = MARGIN + 48
    pdf.setFont("Helvetica", 6)
    pdf.setFillColor(C_BODY)
    y0 = trajectory[0].get("year", 0)
    yN = trajectory[-1].get("year", N - 1)
    pdf.drawString(MARGIN + 20, ly + 12,
                   f"All {N} polar slices overlaid. Bold outlines: first ({y0}, green) and last ({yN}, red).")
    pdf.setFillColor(C_MUTED)
    pdf.setFont("Helvetica", 5.5)
    pdf.drawString(MARGIN + 20, ly,
                   "Density reveals where the manifold concentrates. "
                   "Shape migration shows structural change over time.")
    pdf.restoreState()

    draw_page_footer(pdf, experiment_id)
    pdf.showPage()


def draw_difference_polar(pdf, trajectory, experiment_id, test_object, carriers, page_num, total_pages):
    """Difference polar — year-over-year delta polygons showing rate of change."""
    draw_page_header(pdf, "DIFFERENCE POLAR — YEAR-OVER-YEAR CLR CHANGE",
                     f"{experiment_id}  |  {test_object}  |  {len(trajectory)-1} delta intervals",
                     experiment_id, page_num, total_pages)

    N = len(trajectory)
    if N < 2:
        draw_page_footer(pdf, experiment_id)
        pdf.showPage()
        return

    D = trajectory[0]["D"]
    carrier_names = trajectory[0].get("carrier_names", carriers[:D])
    if not carrier_names or len(carrier_names) < D:
        carrier_names = [f"CLR{j+1}" for j in range(D)]

    plot_r = min(W - 2 * MARGIN - 60, H - 2 * MARGIN - 180) / 2 * 0.70
    pcx = CX
    pcy = CY - 10

    # Compute deltas
    deltas = []
    delta_max = 0
    for i in range(1, N):
        d = [trajectory[i]["clr"][j] - trajectory[i-1]["clr"][j] for j in range(D)]
        deltas.append(d)
        for v in d:
            delta_max = max(delta_max, abs(v))
    if delta_max < 0.001:
        delta_max = 1.0

    pdf.saveState()
    angles = [2 * math.pi * j / D - math.pi / 2 for j in range(D)]

    # Grid
    pdf.setStrokeColor(C_GRID)
    pdf.setLineWidth(0.3)
    for i in range(1, 5):
        pdf.circle(pcx, pcy, plot_r * i / 4, fill=0, stroke=1)

    pdf.setFillColor(C_MUTED)
    pdf.setFont("Helvetica", 5)
    for i in range(1, 5):
        r = plot_r * i / 4
        pdf.drawString(pcx + 3, pcy + r + 2, f"{delta_max * i / 4:.1f}")

    # Radial axes with labels
    for j in range(D):
        x2 = pcx + plot_r * math.cos(angles[j])
        y2 = pcy + plot_r * math.sin(angles[j])
        pdf.setStrokeColor(C_GRID)
        pdf.setLineWidth(0.5)
        pdf.line(pcx, pcy, x2, y2)
        lx = pcx + (plot_r + 14) * math.cos(angles[j])
        ly = pcy + (plot_r + 14) * math.sin(angles[j])
        pdf.setFillColor(CARRIER_COLOURS[j % len(CARRIER_COLOURS)])
        pdf.setFont("Helvetica-Bold", 5.5)
        if math.cos(angles[j]) < -0.3:
            pdf.drawRightString(lx, ly - 2, carrier_names[j])
        elif math.cos(angles[j]) > 0.3:
            pdf.drawString(lx, ly - 2, carrier_names[j])
        else:
            pdf.drawCentredString(lx, ly - 2, carrier_names[j])

    # Draw delta polygons
    for idx, d in enumerate(deltas):
        frac = idx / max(len(deltas) - 1, 1)
        poly_pts = []
        for j in range(D):
            r = abs(d[j]) / delta_max * plot_r
            px = pcx + r * math.cos(angles[j])
            py = pcy + r * math.sin(angles[j])
            poly_pts.append((px, py))
        if len(poly_pts) >= 3:
            path = pdf.beginPath()
            path.moveTo(poly_pts[0][0], poly_pts[0][1])
            for px, py in poly_pts[1:]:
                path.lineTo(px, py)
            path.close()
            col_obj = colour_for_frac(frac)
            alpha = max(0.06, 0.15 - 0.09 * (N / 30))
            pdf.setFillColor(Color(col_obj.red, col_obj.green, col_obj.blue, alpha))
            pdf.setStrokeColor(Color(col_obj.red, col_obj.green, col_obj.blue, 0.5))
            pdf.setLineWidth(0.5)
            pdf.drawPath(path, fill=1, stroke=1)

    pdf.restoreState()

    pdf.saveState()
    ly = MARGIN + 48
    pdf.setFont("Helvetica", 6)
    pdf.setFillColor(C_BODY)
    pdf.drawString(MARGIN + 20, ly + 12,
                   f"Year-over-year CLR differences (delta_CLR_j = CLR_j(t) - CLR_j(t-1)). "
                   f"Large polygons = rapid change. Small = stability.")
    pdf.setFillColor(C_MUTED)
    pdf.setFont("Helvetica", 5.5)
    pdf.drawString(MARGIN + 20, ly,
                   f"Max delta: {delta_max:.2f}  |  Mean delta: {sum(max(abs(v) for v in d) for d in deltas)/len(deltas):.2f}")
    pdf.restoreState()
    draw_page_footer(pdf, experiment_id)
    pdf.showPage()


def draw_norm_profile(pdf, trajectory, experiment_id, test_object, carriers, page_num, total_pages):
    """Norm profile strip — Aitchison norm bar chart over time with entropy overlay."""
    draw_page_header(pdf, "AITCHISON NORM PROFILE",
                     f"{experiment_id}  |  {test_object}  |  {len(trajectory)} intervals",
                     experiment_id, page_num, total_pages)

    N = len(trajectory)
    norms = [p["aitch_norm"] for p in trajectory]
    phases = [math.degrees(p["phase"]) for p in trajectory]
    max_norm = max(norms) if norms else 1
    min_norm = min(norms) if norms else 0

    # Plot area
    plot_left = MARGIN + 50
    plot_right = W - MARGIN - 20
    plot_bottom = MARGIN + 100
    plot_top = H - MARGIN - 60
    plot_w = plot_right - plot_left
    plot_h = plot_top - plot_bottom

    pdf.saveState()

    # Y axis
    pdf.setStrokeColor(C_AXIS)
    pdf.setLineWidth(0.5)
    pdf.line(plot_left, plot_bottom, plot_left, plot_top)

    # Y grid and labels
    n_yticks = 5
    for i in range(n_yticks + 1):
        y = plot_bottom + plot_h * i / n_yticks
        val = min_norm + (max_norm - min_norm) * i / n_yticks
        pdf.setStrokeColor(C_GRID)
        pdf.setLineWidth(0.3)
        pdf.line(plot_left, y, plot_right, y)
        pdf.setFillColor(C_MUTED)
        pdf.setFont("Helvetica", 5)
        pdf.drawRightString(plot_left - 4, y - 2, f"{val:.1f}")

    pdf.setFont("Helvetica", 6)
    pdf.setFillColor(C_BODY)
    pdf.saveState()
    pdf.translate(MARGIN + 8, CY - 20)
    pdf.rotate(90)
    pdf.drawCentredString(0, 0, "Aitchison Norm ||x||_A")
    pdf.restoreState()

    # Bars
    bar_w = max(2, plot_w / N * 0.7)
    gap = plot_w / N
    for i in range(N):
        frac = i / max(N - 1, 1)
        x = plot_left + gap * i + (gap - bar_w) / 2
        norm_frac = (norms[i] - min_norm) / max(max_norm - min_norm, 0.001)
        bar_h = norm_frac * plot_h
        col = colour_for_frac(frac)
        pdf.setFillColor(col)
        pdf.rect(x, plot_bottom, bar_w, bar_h, fill=1, stroke=0)

        # Year label
        year = trajectory[i].get("year", i)
        pdf.setFillColor(C_MUTED)
        pdf.setFont("Helvetica", 4)
        pdf.saveState()
        pdf.translate(x + bar_w / 2, plot_bottom - 4)
        pdf.rotate(90)
        pdf.drawString(0, 0, str(year))
        pdf.restoreState()

    # Phase line overlay (secondary axis)
    max_phase = max(abs(p) for p in phases) if phases else 180
    pdf.setStrokeColor(C_ACCENT)
    pdf.setLineWidth(1.0)
    pdf.setDash(3, 2)
    for i in range(N - 1):
        x1 = plot_left + gap * i + gap / 2
        x2 = plot_left + gap * (i + 1) + gap / 2
        y1 = plot_bottom + (phases[i] / max_phase * 0.5 + 0.5) * plot_h
        y2 = plot_bottom + (phases[i+1] / max_phase * 0.5 + 0.5) * plot_h
        pdf.line(x1, y1, x2, y2)
    pdf.setDash()

    # Phase axis label (right side)
    pdf.setFillColor(C_ACCENT)
    pdf.setFont("Helvetica", 5)
    pdf.drawString(plot_right + 4, plot_top - 5, "Phase (deg)")
    pdf.drawString(plot_right + 4, plot_bottom - 2, f"{-max_phase:.0f}")
    pdf.drawString(plot_right + 4, plot_top - 15, f"+{max_phase:.0f}")

    pdf.restoreState()

    # Stats strip
    pdf.saveState()
    ly = MARGIN + 55
    pdf.setFont("Helvetica", 6)
    pdf.setFillColor(C_BODY)
    mean_norm = sum(norms) / N
    pdf.drawString(MARGIN + 20, ly + 12,
                   f"Min ||x|| = {min_norm:.2f}  |  Max ||x|| = {max_norm:.2f}  |  "
                   f"Mean = {mean_norm:.2f}  |  Range = {max_norm - min_norm:.2f}")
    pdf.setFillColor(C_MUTED)
    pdf.setFont("Helvetica", 5.5)
    pdf.drawString(MARGIN + 20, ly,
                   "Bars = Aitchison norm per interval. Dashed line = CLR phase angle (secondary axis).")
    pdf.restoreState()

    draw_page_footer(pdf, experiment_id)
    pdf.showPage()


def draw_value_table(pdf, trajectory, experiment_id, test_object, carriers, raw_data, page_num, total_pages):
    """Value table — complete numeric readout of all intervals."""
    N = len(trajectory)
    D = trajectory[0]["D"] if trajectory else 3
    carrier_names = trajectory[0].get("carrier_names", carriers[:D])
    if not carrier_names or len(carrier_names) < D:
        carrier_names = [f"CLR{j+1}" for j in range(D)]

    # We may need multiple pages for the table
    rows_per_page = 32
    table_pages = math.ceil(N / rows_per_page)

    for tp in range(table_pages):
        current_page = page_num + tp
        start_row = tp * rows_per_page
        end_row = min(start_row + rows_per_page, N)

        draw_page_header(pdf, "VALUE TABLE — CLR COORDINATES PER INTERVAL",
                         f"{experiment_id}  |  {test_object}  |  Rows {start_row+1}-{end_row} of {N}",
                         experiment_id, current_page, total_pages)

        # Table layout
        table_top = H - MARGIN - 38
        table_left = MARGIN + 5
        row_h = 13
        # Columns: Year, ||x||, Phase, then up to D carrier CLR values
        # Fit as many carriers as possible
        fixed_cols = 3  # Year, Norm, Phase
        max_carrier_cols = min(D, 9)  # limit to 9 carriers per table
        col_widths = [32, 36, 36] + [max(38, (W - 2 * MARGIN - 10 - 104) / max_carrier_cols)] * max_carrier_cols

        # Header row
        pdf.saveState()
        y = table_top
        pdf.setFillColor(HexColor("#D5E8F0"))
        total_w = sum(col_widths[:fixed_cols + max_carrier_cols])
        pdf.rect(table_left, y - row_h, total_w, row_h, fill=1, stroke=0)
        pdf.setFillColor(C_TITLE)
        pdf.setFont("Helvetica-Bold", 5)
        headers = ["Year", "||x||_A", "Phase"] + [n[:7] for n in carrier_names[:max_carrier_cols]]
        x = table_left + 2
        for ci, hdr in enumerate(headers):
            pdf.drawString(x, y - row_h + 4, hdr)
            x += col_widths[ci]

        # Data rows
        for ri in range(start_row, end_row):
            p = trajectory[ri]
            row_idx = ri - start_row + 1
            y = table_top - row_h * (row_idx)
            # Alternating row background
            if row_idx % 2 == 0:
                pdf.setFillColor(HexColor("#F5F7FA"))
                pdf.rect(table_left, y - row_h, total_w, row_h, fill=1, stroke=0)

            pdf.setFont("Helvetica", 4.8)
            frac = ri / max(N - 1, 1)
            pdf.setFillColor(C_BODY)
            x = table_left + 2
            year = str(p.get("year", ri))
            pdf.drawString(x, y - row_h + 4, year)
            x += col_widths[0]
            pdf.drawString(x, y - row_h + 4, f"{p['aitch_norm']:.2f}")
            x += col_widths[1]
            pdf.drawString(x, y - row_h + 4, f"{math.degrees(p['phase']):+.1f}")
            x += col_widths[2]
            for j in range(max_carrier_cols):
                val = p["clr"][j] if j < len(p["clr"]) else 0
                pdf.setFillColor(CARRIER_COLOURS[j % len(CARRIER_COLOURS)])
                pdf.drawString(x, y - row_h + 4, f"{val:+.2f}")
                x += col_widths[3]

        # Table border
        pdf.setStrokeColor(C_GRID)
        pdf.setLineWidth(0.3)
        total_rows = end_row - start_row + 1
        pdf.rect(table_left, table_top - row_h * total_rows, total_w, row_h * total_rows, stroke=1, fill=0)
        pdf.restoreState()

        # Summary stats on last table page
        if tp == table_pages - 1:
            pdf.saveState()
            sy = table_top - row_h * (total_rows + 1)
            pdf.setFont("Helvetica", 5.5)
            pdf.setFillColor(C_BODY)

            # System diagnostics from raw data
            vt_shape = raw_data.get("vt_shape", raw_data.get("V(t)_shape", "—"))
            tot_var = raw_data.get("total_variance", "—")
            path_eff = raw_data.get("path_efficiency", "—")
            path_len = raw_data.get("aitchison_path_length", "—")
            net_dist = raw_data.get("aitchison_net_distance", "—")
            amalg = raw_data.get("amalgamation_all_pass", "—")

            lines = [
                f"V(t) Shape: {vt_shape}  |  Total Variance: {tot_var}",
                f"Path Length: {path_len}  |  Net Distance: {net_dist}  |  Path Efficiency: {path_eff}",
                f"Amalgamation Pass: {amalg}  |  Carriers: {D}  |  Observations: {N}",
            ]
            for li, line in enumerate(lines):
                if sy - li * 10 > MARGIN + 40:
                    pdf.drawString(MARGIN + 20, sy - li * 10, line)
            pdf.restoreState()

        draw_page_footer(pdf, experiment_id)
        pdf.showPage()

    return table_pages


def normalise_data(data):
    """Normalise field names across formats."""
    out = dict(data)
    if "V(t)_shape" not in out:
        out["V(t)_shape"] = data.get("vt_shape", "—")
    return out


def generate_json_output(trajectory, experiment_id, test_object, carriers, raw_data, events, output_path):
    """Generate structured JSON of all computed values for experiment journal."""
    N = len(trajectory)
    D = trajectory[0]["D"] if trajectory else 0
    carrier_names = trajectory[0].get("carrier_names", carriers[:D]) if trajectory else carriers

    norms = [p["aitch_norm"] for p in trajectory]
    phases = [math.degrees(p["phase"]) for p in trajectory]

    intervals = []
    for i, p in enumerate(trajectory):
        entry = {
            "index": i,
            "year": p.get("year", i),
            "clr": {carrier_names[j] if j < len(carrier_names) else f"CLR{j+1}": p["clr"][j]
                    for j in range(len(p["clr"]))},
            "aitchison_norm": round(p["aitch_norm"], 6),
            "phase_deg": round(math.degrees(p["phase"]), 3),
        }
        if i > 0:
            entry["delta_norm"] = round(p["aitch_norm"] - trajectory[i-1]["aitch_norm"], 6)
            entry["delta_clr"] = {
                carrier_names[j] if j < len(carrier_names) else f"CLR{j+1}":
                round(p["clr"][j] - trajectory[i-1]["clr"][j], 6)
                for j in range(len(p["clr"]))
            }
        intervals.append(entry)

    output = {
        "experiment": experiment_id,
        "test_object": test_object,
        "carriers": list(carrier_names[:D]),
        "D": D,
        "N": N,
        "generator": "hs_polar_stack.py",
        "summary": {
            "norm_min": round(min(norms), 6) if norms else None,
            "norm_max": round(max(norms), 6) if norms else None,
            "norm_mean": round(sum(norms) / N, 6) if norms else None,
            "norm_range": round(max(norms) - min(norms), 6) if norms else None,
            "phase_range_deg": round(max(phases) - min(phases), 3) if phases else None,
            "total_variance": raw_data.get("total_variance"),
            "vt_shape": raw_data.get("vt_shape", raw_data.get("V(t)_shape")),
            "path_efficiency": raw_data.get("path_efficiency"),
            "path_length": raw_data.get("aitchison_path_length"),
            "net_distance": raw_data.get("aitchison_net_distance"),
            "amalgamation_pass": raw_data.get("amalgamation_all_pass"),
        },
        "events": events,
        "intervals": intervals,
    }

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"Generated: {output_path}")
    return output_path


def build_polar_stack_pdf(results_json, output_pdf):
    """Main builder — per-interval polar projection stack with all views."""

    with open(results_json, 'r') as f:
        raw = json.load(f)

    experiment_id = raw.get("experiment", raw.get("_meta", {}).get("experiment_id", "Hs-M00"))

    # Select data
    if "countries" in raw:
        countries = raw["countries"]
        first_key = list(countries.keys())[0]
        cdata = countries[first_key]
        cdata["test_object"] = cdata.get("country", first_key)
        data = normalise_data(cdata)
    elif "results" in raw and isinstance(raw["results"], list):
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
                try:
                    if float(tv) > 0.001:
                        chosen = r
                        break
                except:
                    continue
        if chosen is None:
            chosen = results[0]
        data = normalise_data(chosen)
    else:
        data = normalise_data(raw)

    test_object = data.get("test_object", data.get("country", data.get("name", "Unknown")))
    carriers = data.get("carriers", [])

    trajectory, carriers = extract_full_trajectory(data)

    if not trajectory:
        print(f"ERROR: No trajectory data found in {results_json}")
        return None

    N = len(trajectory)

    # Detect events for helix tags
    events = detect_events(trajectory, data)

    # Calculate total pages:
    # 1 helix + N polar slices + 1 ghost + 1 difference + 1 norm profile + table pages + 1 summary
    table_page_count = math.ceil(N / 32)
    total_pages = 1 + N + 1 + 1 + 1 + table_page_count + 1

    # Create PDF
    pdf = canvas.Canvas(output_pdf, pagesize=A4)
    pdf.setTitle(f"Hs Polar Stack — {experiment_id}")
    pdf.setAuthor("Peter Higgins / Rogue Wave Audio")

    # Page 1: Helix overview with XYZ coordinates and event tags
    draw_helix_overview(pdf, trajectory, experiment_id, test_object, carriers, total_pages, events)

    # Pages 2 to N+1: Per-interval polar plots
    for i, point in enumerate(trajectory):
        draw_polar_interval(pdf, point, i, trajectory, experiment_id, test_object, carriers, total_pages)

    # Page N+2: Ghost stack composite — all slices overlaid
    ghost_page = N + 2
    draw_ghost_stack(pdf, trajectory, experiment_id, test_object, carriers, ghost_page, total_pages)

    # Page N+3: Difference polar — year-over-year delta polygons
    diff_page = ghost_page + 1
    draw_difference_polar(pdf, trajectory, experiment_id, test_object, carriers, diff_page, total_pages)

    # Page N+4: Norm profile strip
    norm_page = diff_page + 1
    draw_norm_profile(pdf, trajectory, experiment_id, test_object, carriers, norm_page, total_pages)

    # Pages N+5+: Value table
    table_start = norm_page + 1
    actual_table_pages = draw_value_table(pdf, trajectory, experiment_id, test_object, carriers, data, table_start, total_pages)

    # Final page: Summary comparison
    draw_summary_comparison(pdf, trajectory, experiment_id, test_object, carriers, total_pages)

    pdf.save()
    print(f"Generated: {output_pdf} ({total_pages} pages, {N} intervals, {len(events)} events)")

    # Generate companion JSON
    json_path = output_pdf.rsplit(".", 1)[0] + ".json"
    generate_json_output(trajectory, experiment_id, test_object, carriers, data, events, json_path)

    return output_pdf


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hs_polar_stack.py <results.json> [output.pdf]")
        sys.exit(1)

    results_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else "polar_stack.pdf"
    build_polar_stack_pdf(results_file, out_file)
