#!/usr/bin/env python3
"""
Hs Helix Exploded Diagram — Bill of Materials Output
=====================================================
Generates a 1-page PDF showing the Hs pipeline manifold output as a 3D
isometric helix with alternating left/right callout tags.

Each turn of the helix represents one pipeline analysis layer. Leader lines
connect each layer to its description tag. The diagram serves as a
printable/submittable "bill of materials" for any pipeline run.

Usage:
    python hs_helix_exploded.py <results.json> [output.pdf]

Peter Higgins / Rogue Wave Audio / CC BY 4.0
"""

import json, sys, math, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color

# ── Page setup ──────────────────────────────────────────────────────────
W, H = A4  # 595.28 x 841.89 pts
MARGIN = 18 * mm
CX = W / 2          # centre x
CY = H / 2 + 10     # centre y (nudged up for footer)

# ── Colour palette — Hs standard ────────────────────────────────────────
C_BG        = HexColor("#FFFFFF")
C_HELIX     = HexColor("#1B3A5C")   # dark navy — helix body
C_HELIX_LT  = HexColor("#4A7FB5")   # lighter blue — helix highlight
C_LEADER    = HexColor("#888888")   # leader lines
C_TAG_BG_L  = HexColor("#E8F0F8")   # left tag background
C_TAG_BG_R  = HexColor("#F0F4E8")   # right tag background
C_TAG_BORDER= HexColor("#A0B0C0")   # tag border
C_TITLE     = HexColor("#0D1B2A")   # title text
C_BODY      = HexColor("#333333")   # body text
C_ACCENT    = HexColor("#2E75B6")   # accent / section headers
C_MUTED     = HexColor("#777777")   # muted annotations
C_AXIS      = HexColor("#BBBBBB")   # axis lines
C_DIAG      = HexColor("#C0392B")   # diagnosis colour

# ── Pipeline layers (the "bill of materials") ───────────────────────────
# Each layer = one turn/section of the helix
# Format: (short_label, description, key_metric_name)
LAYERS = [
    ("INPUT",       "Raw composition on S^(D-1)",          "input_shape"),
    ("CLR",         "Centred log-ratio transform",         "clr_range"),
    ("VAR",         "Variation matrix sigma^2_A",          "total_variance"),
    ("V(t)",        "Cumulative variance trajectory",      "V(t)_shape"),
    ("ENTROPY",     "Shannon entropy H(x)",                "entropy_mean"),
    ("AITCHISON",   "Aitchison norm geometry",             "aitchison_norm_mean"),
    ("LOCKS",       "Log-ratio lock detection",            "locks_found"),
    ("FINGERPRINT", "Geometric fingerprint (A, P, C)",     "fingerprint_area"),
    ("PATH",        "Aitchison path analysis",             "path_efficiency"),
    ("DIAGNOSIS",   "Structural classification code",      "DIAGNOSIS"),
]


def draw_3d_helix(c, cx, cy, layers, n_turns=None):
    """Draw a 3D isometric helix in the centre of the page.

    The helix is drawn as an elliptical spiral viewed from a 30-degree
    isometric angle. Each full turn corresponds to one pipeline layer.
    """
    n = len(layers)
    if n_turns is None:
        n_turns = n

    # Helix geometry
    rx = 52          # horizontal radius (x)
    ry = 22          # vertical radius (y) — foreshortened for iso view
    total_height = min(560, H - 2 * MARGIN - 120)  # total vertical span
    step = total_height / n  # vertical distance per layer

    # Start from top, spiral downward
    top_y = cy + total_height / 2

    pts_per_turn = 60
    total_pts = pts_per_turn * n_turns

    # Collect all helix points
    helix_pts = []
    for i in range(total_pts + 1):
        frac = i / total_pts
        angle = 2 * math.pi * n_turns * frac
        x = cx + rx * math.cos(angle)
        y_iso = ry * math.sin(angle)
        y_vert = top_y - frac * total_height
        y = y_vert + y_iso
        helix_pts.append((x, y, angle, frac))

    # Draw back half of helix first (sin > 0 means behind)
    c.saveState()
    for i in range(len(helix_pts) - 1):
        x1, y1, a1, f1 = helix_pts[i]
        x2, y2, a2, f2 = helix_pts[i + 1]
        # Back half: sin(angle) > 0
        if math.sin(a1) >= 0:
            depth = 0.25 + 0.15 * math.sin(a1)
            c.setStrokeColor(Color(0.29, 0.50, 0.71, depth))
            c.setLineWidth(2.0)
            c.line(x1, y1, x2, y2)
    c.restoreState()

    # Draw central axis (dashed)
    c.saveState()
    c.setStrokeColor(C_AXIS)
    c.setLineWidth(0.5)
    c.setDash(3, 3)
    c.line(cx, top_y + 15, cx, top_y - total_height - 15)
    c.restoreState()

    # Draw front half of helix (sin < 0 means in front)
    c.saveState()
    for i in range(len(helix_pts) - 1):
        x1, y1, a1, f1 = helix_pts[i]
        x2, y2, a2, f2 = helix_pts[i + 1]
        # Front half: sin(angle) < 0
        if math.sin(a1) < 0:
            depth = 0.75 + 0.25 * abs(math.sin(a1))
            c.setStrokeColor(Color(0.106, 0.227, 0.361, depth))
            c.setLineWidth(3.0)
            c.line(x1, y1, x2, y2)
    c.restoreState()

    # Draw layer marker dots on helix (at the front-most point of each turn)
    layer_positions = []
    for li in range(n):
        # Position each layer at the front of its turn
        frac = (li + 0.5) / n
        angle = 2 * math.pi * n_turns * frac + math.pi  # front = pi
        best_idx = int(frac * total_pts)
        # Find closest front-facing point
        best_dist = 999
        best_pt = None
        search_range = pts_per_turn // 2
        for si in range(max(0, best_idx - search_range), min(total_pts, best_idx + search_range)):
            sx, sy, sa, sf = helix_pts[si]
            # Want sin(angle) close to -1 (front-most)
            d = abs(sf - frac)
            if d < best_dist:
                best_dist = d
                best_pt = (sx, sy, sf)

        if best_pt is None:
            # Fallback
            sx = cx + rx * math.cos(angle)
            sy_vert = top_y - frac * total_height
            sy = sy_vert + ry * math.sin(angle)
            best_pt = (sx, sy, frac)

        layer_positions.append(best_pt)

    # Draw marker dots
    c.saveState()
    for i, (lx, ly, _) in enumerate(layer_positions):
        c.setFillColor(C_ACCENT)
        c.circle(lx, ly, 3, fill=1, stroke=0)
    c.restoreState()

    return layer_positions, top_y, total_height


def draw_callout_tags(c, layer_positions, layers, data, top_y, total_height):
    """Draw alternating left/right callout tags with leader lines."""
    n = len(layers)

    # Tag dimensions
    tag_w = 165
    tag_h_base = 36
    tag_margin = 16  # gap from helix edge

    helix_right_edge = CX + 52 + tag_margin
    helix_left_edge = CX - 52 - tag_margin

    for i, (lx, ly, _) in enumerate(layer_positions):
        label, desc, metric_key = layers[i]

        # Get metric value from data
        metric_val = data.get(metric_key, "—")
        if isinstance(metric_val, float):
            metric_val = f"{metric_val:.6f}"
        elif isinstance(metric_val, int):
            metric_val = str(metric_val)
        metric_val = str(metric_val)

        # Truncate long values
        if len(metric_val) > 35:
            metric_val = metric_val[:32] + "..."

        # Alternate sides: even=right, odd=left
        is_right = (i % 2 == 0)

        if is_right:
            tag_x = helix_right_edge + 25
            tag_bg = C_TAG_BG_R
            leader_end_x = tag_x
            text_x = tag_x + 6
        else:
            tag_x = helix_left_edge - tag_w - 25
            tag_bg = C_TAG_BG_L
            leader_end_x = tag_x + tag_w
            text_x = tag_x + 6

        # Compute tag height based on content
        tag_h = tag_h_base

        tag_y = ly - tag_h / 2

        # Draw leader line
        c.saveState()
        c.setStrokeColor(C_LEADER)
        c.setLineWidth(0.6)
        # Horizontal from helix dot to tag
        mid_x = (lx + leader_end_x) / 2
        c.line(lx, ly, leader_end_x, ly)
        # Small dot at connection
        c.setFillColor(C_LEADER)
        c.circle(leader_end_x, ly, 1.5, fill=1, stroke=0)
        c.restoreState()

        # Draw tag background
        c.saveState()
        c.setFillColor(tag_bg)
        c.setStrokeColor(C_TAG_BORDER)
        c.setLineWidth(0.5)
        c.roundRect(tag_x, tag_y, tag_w, tag_h, 3, fill=1, stroke=1)

        # Tag label (bold header)
        c.setFillColor(C_ACCENT)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(text_x, tag_y + tag_h - 10, label)

        # Layer number badge
        badge_x = tag_x + tag_w - 16
        c.setFillColor(C_ACCENT)
        c.circle(badge_x, tag_y + tag_h - 7, 6, fill=1, stroke=0)
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 6)
        num_str = str(i + 1)
        c.drawCentredString(badge_x, tag_y + tag_h - 9, num_str)

        # Description line
        c.setFillColor(C_BODY)
        c.setFont("Helvetica", 6)
        c.drawString(text_x, tag_y + tag_h - 19, desc)

        # Metric value line
        if metric_key == "DIAGNOSIS":
            c.setFillColor(C_DIAG)
            c.setFont("Helvetica-Bold", 6)
        else:
            c.setFillColor(C_MUTED)
            c.setFont("Helvetica", 5.5)

        c.drawString(text_x, tag_y + tag_h - 28, metric_val)

        c.restoreState()


def draw_header(c, experiment_id, test_object, simplex):
    """Draw page header with experiment identification."""
    c.saveState()

    # Title block
    c.setFillColor(C_TITLE)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(CX, H - MARGIN - 8, "Hs MANIFOLD OUTPUT — EXPLODED HELIX DIAGRAM")

    # Subtitle
    c.setFillColor(C_ACCENT)
    c.setFont("Helvetica", 9)
    subtitle = f"{experiment_id}  |  {test_object}  |  {simplex}"
    c.drawCentredString(CX, H - MARGIN - 22, subtitle)

    # Thin rule
    c.setStrokeColor(C_ACCENT)
    c.setLineWidth(0.8)
    c.line(MARGIN + 20, H - MARGIN - 28, W - MARGIN - 20, H - MARGIN - 28)

    # Column headers
    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 6)
    c.drawString(MARGIN, H - MARGIN - 40, "PIPELINE LAYER")
    c.drawRightString(W - MARGIN, H - MARGIN - 40, "PIPELINE LAYER")

    c.restoreState()


def draw_footer(c, experiment_id):
    """Draw page footer with identification and standards."""
    c.saveState()

    y = MARGIN + 20

    # Rule
    c.setStrokeColor(C_ACCENT)
    c.setLineWidth(0.5)
    c.line(MARGIN + 20, y + 12, W - MARGIN - 20, y + 12)

    # Footer text
    c.setFillColor(C_MUTED)
    c.setFont("Helvetica", 6)
    c.drawString(MARGIN + 20, y, "Hs Decomposition Engine  |  Manifold Output  |  Bill of Materials")
    c.drawRightString(W - MARGIN - 20, y, "Peter Higgins / Rogue Wave Audio / CC BY 4.0")

    # Version tag
    c.setFont("Helvetica", 5)
    c.drawCentredString(CX, y - 10, f"{experiment_id} — Generated by hs_helix_exploded.py — Hs Standards Edition")

    c.restoreState()


def draw_summary_strip(c, data):
    """Draw a compact summary strip at the bottom showing key metrics."""
    c.saveState()

    y = MARGIN + 42
    strip_h = 18
    strip_w = W - 2 * MARGIN - 40
    strip_x = MARGIN + 20

    # Background
    c.setFillColor(HexColor("#F5F7FA"))
    c.setStrokeColor(C_TAG_BORDER)
    c.setLineWidth(0.3)
    c.roundRect(strip_x, y, strip_w, strip_h, 2, fill=1, stroke=1)

    # Key summary values
    summaries = []

    shape = data.get("input_shape", "—")
    summaries.append(f"Input: {shape}")

    tv = data.get("total_variance", "—")
    if isinstance(tv, (int, float)):
        summaries.append(f"Var: {tv:.4f}")
    else:
        summaries.append(f"Var: {tv}")

    vt = data.get("V(t)_shape", "—")
    summaries.append(f"V(t): {vt}")

    ent = data.get("entropy_mean", "—")
    if isinstance(ent, (int, float)):
        summaries.append(f"H(x): {ent:.4f}")
    else:
        summaries.append(f"H(x): {ent}")

    pe = data.get("path_efficiency", "—")
    if isinstance(pe, (int, float)):
        summaries.append(f"Path: {pe:.4f}")
    elif pe != "—":
        summaries.append(f"Path: {pe}")

    diag = data.get("DIAGNOSIS", "—")
    # Shorten diagnosis for strip
    diag_short = diag.split(" — ")[0] if " — " in str(diag) else str(diag)
    summaries.append(diag_short)

    # Draw summary items
    c.setFillColor(C_BODY)
    c.setFont("Helvetica", 5.5)

    spacing = strip_w / len(summaries)
    for si, sv in enumerate(summaries):
        sx = strip_x + si * spacing + spacing / 2
        c.drawCentredString(sx, y + 5.5, sv)

    # Separator lines
    c.setStrokeColor(HexColor("#D0D8E0"))
    c.setLineWidth(0.3)
    for si in range(1, len(summaries)):
        sx = strip_x + si * spacing
        c.line(sx, y + 2, sx, y + strip_h - 2)

    c.restoreState()


def normalise_data(data, raw=None):
    """Normalise field names across M01 and M02 result formats.

    M01 uses: V(t)_shape, locks_found, input_shape, entropy_mean, etc.
    M02 uses: vt_shape, locks (array), D, carriers, entropy_trajectory, etc.

    Returns a dict with the canonical field names used by LAYERS.
    """
    out = dict(data)

    # input_shape
    if "input_shape" not in out:
        D = data.get("D", "?")
        n_years = len(data.get("years", []))
        carriers = data.get("carriers", [])
        if n_years and D:
            out["input_shape"] = f"{n_years} observations x {D} carriers"
        elif carriers:
            out["input_shape"] = f"{len(carriers)} carriers, D={len(carriers)}"

    # clr_range
    if "clr_range" not in out:
        clr = data.get("clr_summary", {})
        if clr:
            mn = clr.get("min", "?")
            mx = clr.get("max", "?")
            if isinstance(mn, (int, float)):
                out["clr_range"] = f"[{mn:.4f}, {mx:.4f}]"
        else:
            # Try computing from clr_coordinates (M02 format)
            coords = data.get("clr_coordinates", {})
            if coords:
                all_vals = []
                for year_data in coords.values():
                    if isinstance(year_data, dict):
                        all_vals.extend(v for v in year_data.values() if isinstance(v, (int, float)))
                if all_vals:
                    out["clr_range"] = f"[{min(all_vals):.4f}, {max(all_vals):.4f}]"

    # V(t)_shape
    if "V(t)_shape" not in out:
        out["V(t)_shape"] = data.get("vt_shape", "—")

    # entropy_mean
    if "entropy_mean" not in out:
        ent = data.get("entropy_trajectory", {})
        if ent:
            vals = [v for v in ent.values() if isinstance(v, (int, float))]
            if vals:
                out["entropy_mean"] = f"{sum(vals)/len(vals):.6f}"

    # aitchison_norm_mean
    if "aitchison_norm_mean" not in out:
        ant = data.get("aitchison_norm_trajectory", {})
        if ant:
            vals = [v for v in ant.values() if isinstance(v, (int, float))]
            if vals:
                out["aitchison_norm_mean"] = f"{sum(vals)/len(vals):.6f}"

    # locks_found
    if "locks_found" not in out:
        locks = data.get("locks", [])
        if isinstance(locks, list):
            out["locks_found"] = len(locks)
        else:
            out["locks_found"] = locks

    # fingerprint_area
    if "fingerprint_area" not in out:
        fp = data.get("fingerprint", {})
        if fp:
            out["fingerprint_area"] = fp.get("area", "—")
            out["fingerprint_perimeter"] = fp.get("perimeter", "—")
            out["fingerprint_compactness"] = fp.get("compactness", "—")

    # simplex
    if "simplex" not in out:
        D = data.get("D")
        if D:
            out["simplex"] = f"S^{D-1} ({D-1}-simplex)"

    # DIAGNOSIS
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


def build_helix_pdf(results_json, output_pdf):
    """Main builder — reads pipeline results JSON, produces exploded helix PDF."""

    with open(results_json, 'r') as f:
        raw = json.load(f)

    # Handle both single-object and multi-object result formats
    experiment_id = raw.get("experiment", "Hs-M00")
    title = raw.get("title", "Manifold Output")

    if "results" in raw and isinstance(raw["results"], list):
        # Multi-object format (M01 style) — use first non-trivial object
        results = raw["results"]
        chosen = None
        for r in results:
            obj_name = r.get("test_object", "").lower()
            if "helix" in obj_name:
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
                except (ValueError, TypeError):
                    continue
        if chosen is None:
            chosen = results[0]
        data = normalise_data(chosen, raw)
    elif "results" in raw and isinstance(raw["results"], dict):
        data = normalise_data(raw["results"], raw)
    elif "countries" in raw:
        # M02-style: pick first country
        countries = raw["countries"]
        first_key = list(countries.keys())[0]
        cdata = countries[first_key]
        cdata["test_object"] = cdata.get("country", first_key)
        data = normalise_data(cdata, raw)
    else:
        data = normalise_data(raw)

    test_object = data.get("test_object", data.get("country", title))
    simplex = data.get("simplex", "S^?")

    # Create PDF
    c_pdf = canvas.Canvas(output_pdf, pagesize=A4)
    c_pdf.setTitle(f"Hs Helix Exploded — {experiment_id}")
    c_pdf.setAuthor("Peter Higgins / Rogue Wave Audio")
    c_pdf.setSubject("Manifold Output — Exploded Helix Diagram")

    # Draw components
    draw_header(c_pdf, experiment_id, test_object, simplex)

    # Draw the 3D helix
    layer_positions, top_y, total_height = draw_3d_helix(
        c_pdf, CX, CY, LAYERS, n_turns=len(LAYERS)
    )

    # Draw callout tags
    draw_callout_tags(c_pdf, layer_positions, LAYERS, data, top_y, total_height)

    # Draw summary strip
    draw_summary_strip(c_pdf, data)

    # Draw footer
    draw_footer(c_pdf, experiment_id)

    c_pdf.save()
    print(f"Generated: {output_pdf}")
    return output_pdf


def build_all_objects_pdf(results_json, output_dir):
    """Build one exploded helix PDF per test object in a multi-object results file."""

    with open(results_json, 'r') as f:
        raw = json.load(f)

    experiment_id = raw.get("experiment", "Hs-M00")

    if "results" not in raw or not isinstance(raw["results"], list):
        # Single object — just build one
        out = os.path.join(output_dir, f"{experiment_id}_helix_exploded.pdf")
        return [build_helix_pdf(results_json, out)]

    outputs = []
    for i, obj_data in enumerate(raw["results"]):
        test_obj = obj_data.get("test_object", f"Object_{i}")
        safe_name = test_obj.replace(" ", "_").replace("(", "").replace(")", "")
        safe_name = safe_name.replace(",", "").replace("/", "_")

        # Build a temporary single-object JSON
        single = {
            "experiment": experiment_id,
            "title": raw.get("title", ""),
            "results": obj_data
        }

        tmp_json = os.path.join(output_dir, f"_tmp_{safe_name}.json")
        out_pdf = os.path.join(output_dir, f"{experiment_id}_{safe_name}_helix.pdf")

        with open(tmp_json, 'w') as f:
            json.dump(single, f)

        build_helix_pdf(tmp_json, out_pdf)
        os.remove(tmp_json)
        outputs.append(out_pdf)

    return outputs


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hs_helix_exploded.py <results.json> [output.pdf]")
        print("       python hs_helix_exploded.py <results.json> --all <output_dir>")
        sys.exit(1)

    results_file = sys.argv[1]

    if len(sys.argv) >= 3 and sys.argv[2] == "--all":
        out_dir = sys.argv[3] if len(sys.argv) > 3 else "."
        outputs = build_all_objects_pdf(results_file, out_dir)
        print(f"Generated {len(outputs)} PDFs")
    else:
        out_file = sys.argv[2] if len(sys.argv) > 2 else "helix_exploded.pdf"
        build_helix_pdf(results_file, out_file)
