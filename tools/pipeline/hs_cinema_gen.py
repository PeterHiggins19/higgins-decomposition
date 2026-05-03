#!/usr/bin/env python3
"""hs_cinema_gen.py -- Generate PPTX compositional cinema from polar_stack JSON files."""
import argparse, json, os, sys, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Color palettes for up to 10 runs
RUN_PALETTES = [
    {"bg": "#1A1A2E", "accent": "#E63946", "colors": ["#E63946","#457B9D","#2A9D8F","#F4A261","#E76F51","#264653","#A8DADC","#8338EC","#FF006E","#06D6A0"]},
    {"bg": "#16213E", "accent": "#4ECDC4", "colors": ["#FF6B6B","#4ECDC4","#45B7D1","#FFA07A","#98D8C8","#F7DC6F","#BB8FCE","#85C1E9","#F1948A","#7DCEA0"]},
    {"bg": "#10002B", "accent": "#F72585", "colors": ["#F72585","#7209B7","#3A0CA3","#4361EE","#4CC9F0","#B5179E","#560BAD","#480CA8","#3F37C9","#4895EF"]},
    {"bg": "#1B1B2F", "accent": "#E94560", "colors": ["#E94560","#0F3460","#533483","#16C79A","#F67280","#355C7D","#6C5B7B","#C06C84","#F8B500","#FC5185"]},
    {"bg": "#0B132B", "accent": "#5BC0BE", "colors": ["#5BC0BE","#3A506B","#6FFFE9","#1C2541","#FFE66D","#F7FFF7","#4ECDC4","#FF6B6B","#C7F9CC","#80ED99"]},
    {"bg": "#1A1423", "accent": "#C77DFF", "colors": ["#C77DFF","#9D4EDD","#7B2CBF","#5A189A","#E0AAFF","#3C096C","#240046","#10002B","#FF9E00","#FF7900"]},
    {"bg": "#1B2838", "accent": "#66C0F4", "colors": ["#66C0F4","#B8D4E3","#2A475E","#C7D5E0","#1B2838","#4FC3F7","#29B6F6","#03A9F4","#0288D1","#0277BD"]},
    {"bg": "#1E1E2E", "accent": "#F38BA8", "colors": ["#F38BA8","#FAB387","#F9E2AF","#A6E3A1","#89DCEB","#74C7EC","#B4BEFE","#CBA6F7","#F5C2E7","#EBA0AC"]},
    {"bg": "#1C1C1C", "accent": "#FFD700", "colors": ["#FFD700","#FF6347","#4169E1","#32CD32","#FF69B4","#FF4500","#00CED1","#9370DB","#D4944A","#4AB8D4"]},
    {"bg": "#2D1B69", "accent": "#00F5D4", "colors": ["#00F5D4","#00BBF9","#FEE440","#9B5DE5","#F15BB5","#00F5D4","#00BBF9","#FEE440","#9B5DE5","#F15BB5"]},
]

STEP_THRESHOLDS = [(10000, 128), (5000, 64), (1000, 16), (400, 8), (200, 4), (100, 2), (50, 1)]

def get_step(N):
    """Determine subsampling step based on number of intervals."""
    for threshold, step in STEP_THRESHOLDS:
        if N >= threshold:
            return step
    return 1

def draw_polar_slice(ax, clr_norm, D, carriers, colors, radius=1.0):
    """Draw a single polar polygon slice."""
    angles = [2 * math.pi * j / D for j in range(D)]
    pts_x, pts_y = [], []
    for j in range(D):
        r = radius * (0.1 + 0.9 * clr_norm[j])
        pts_x.append(r * math.cos(angles[j] - math.pi/2))
        pts_y.append(r * math.sin(angles[j] - math.pi/2))
    pts_x.append(pts_x[0])
    pts_y.append(pts_y[0])
    ax.fill(pts_x, pts_y, alpha=0.35, color=colors[0], linewidth=0)
    ax.plot(pts_x, pts_y, color='white', linewidth=2, alpha=0.9)
    for j in range(D):
        r = radius * (0.1 + 0.9 * clr_norm[j])
        x = r * math.cos(angles[j] - math.pi/2)
        y = r * math.sin(angles[j] - math.pi/2)
        ax.scatter(x, y, s=max(120 - D*8, 40), color=colors[j % len(colors)],
                   zorder=5, edgecolors='white', linewidth=1.5)
        lr = radius * 1.25
        lx = lr * math.cos(angles[j] - math.pi/2)
        ly = lr * math.sin(angles[j] - math.pi/2)
        name = carriers[j][:12]
        label = f"{name}\n{clr_norm[j]:.3f}"
        fs = max(7 - D//3, 5)
        ax.text(lx, ly, label, ha='center', va='center', fontsize=fs,
                color=colors[j % len(colors)], fontweight='bold', fontfamily='monospace')
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(radius*np.cos(theta), radius*np.sin(theta), color='white', alpha=0.15, linewidth=1, linestyle='--')

def draw_bars(ax, clr_norm, D, carriers, colors):
    """Draw horizontal species fraction bars."""
    for j in range(D):
        name = carriers[j][:14]
        y = D - 1 - j
        ax.barh(y, 1.0, height=0.6, color='white', alpha=0.08)
        ax.barh(y, clr_norm[j], height=0.6, color=colors[j % len(colors)], alpha=0.85)
        ax.text(-0.02, y, name, ha='right', va='center', fontsize=max(7 - D//4, 4),
                color=colors[j % len(colors)], fontweight='bold')
        ax.text(clr_norm[j] + 0.02, y, f"{clr_norm[j]:.3f}", ha='left', va='center',
                fontsize=max(7 - D//4, 4), color='white', alpha=0.8)
    ax.set_xlim(-0.35, 1.15)
    ax.set_ylim(-0.5, D - 0.5)
    ax.axis('off')

def generate_cinema(runs, output_path, title="Hs Compositional Cinema"):
    """Generate PPTX cinema from loaded runs."""
    import tempfile

    frames_dir = tempfile.mkdtemp(prefix="hs_cinema_")

    all_frame_info = []  # (run_name, frame_path, bg_color)

    for ri, run in enumerate(runs):
        pal = RUN_PALETTES[ri % len(RUN_PALETTES)]
        name = run["name"]
        carriers = run["carriers"]
        D = len(carriers)
        intervals = run["intervals"]
        N = len(intervals)
        step = get_step(N)
        indices = list(range(0, N, step))
        total = len(indices)
        colors = pal["colors"][:D] if D <= len(pal["colors"]) else (pal["colors"] * ((D // len(pal["colors"])) + 1))[:D]

        # Normalize CLR per carrier
        clr_vals = [[iv["clr"][c] for c in carriers] for iv in intervals]
        mins = [min(row[j] for row in clr_vals if row[j] > -10) if any(row[j] > -10 for row in clr_vals) else 0 for j in range(D)]
        maxs = [max(row[j] for row in clr_vals if row[j] > -10) if any(row[j] > -10 for row in clr_vals) else 1 for j in range(D)]

        print(f"  {name}: {total} frames (from {N}, step={step})")

        for fi, idx in enumerate(indices):
            iv = intervals[idx]
            year = iv.get("year", iv["index"])
            raw = [iv["clr"][c] for c in carriers]
            norm = []
            for j in range(D):
                rng = maxs[j] - mins[j]
                if rng < 1e-12:
                    norm.append(0.5)
                elif raw[j] < -10:
                    norm.append(0.0)
                else:
                    norm.append((raw[j] - mins[j]) / rng)

            fig = plt.figure(figsize=(10, 5.625), dpi=144, facecolor=pal["bg"])
            ax_polar = fig.add_axes([0.05, 0.08, 0.55, 0.78])
            ax_polar.set_facecolor(pal["bg"])
            ax_polar.set_xlim(-1.6, 1.6)
            ax_polar.set_ylim(-1.6, 1.6)
            ax_polar.set_aspect('equal')
            ax_polar.axis('off')
            draw_polar_slice(ax_polar, norm, D, carriers, colors)

            if D <= 12:
                ax_bars = fig.add_axes([0.68, 0.15, 0.28, 0.55])
                ax_bars.set_facecolor(pal["bg"])
                draw_bars(ax_bars, norm, D, carriers, colors)

            fig.text(0.5, 0.95, f"Hs Compositional Cinema  |  {name}",
                     ha='center', va='center', fontsize=14, color='white',
                     fontweight='bold', fontfamily='monospace')

            fig.text(0.33, 0.04, f"t={year}", ha='center', va='center', fontsize=20,
                     color=pal["accent"], fontweight='bold', fontfamily='monospace')

            dom_idx = int(np.argmax(norm))
            fig.text(0.82, 0.95, f"Max: {carriers[dom_idx][:12]}", ha='center', va='center',
                     fontsize=9, color=colors[dom_idx], fontweight='bold', fontfamily='monospace')

            fig.text(0.95, 0.01, f"Frame {fi+1}/{total}", ha='right', va='center',
                     fontsize=7, color='white', alpha=0.3, fontfamily='monospace')

            progress = fi / max(total - 1, 1)
            ax_prog = fig.add_axes([0.05, 0.06, 0.9, 0.01])
            ax_prog.set_xlim(0, 1)
            ax_prog.set_ylim(0, 1)
            ax_prog.barh(0.5, progress, height=1.0, color=pal["accent"], alpha=0.6)
            ax_prog.barh(0.5, 1.0, height=1.0, color='white', alpha=0.05)
            ax_prog.axis('off')

            fpath = os.path.join(frames_dir, f"{ri:02d}_{fi:04d}.png")
            fig.savefig(fpath, facecolor=pal["bg"], bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)
            all_frame_info.append((name, fpath, pal["bg"]))

    # Build PPTX
    print(f"\nAssembling PPTX with {len(all_frame_info)} frame slides...")

    # Use pptxgenjs via Node
    build_script = os.path.join(frames_dir, "build.js")

    # Group frames by run
    run_groups = {}
    for name, fpath, bg in all_frame_info:
        if name not in run_groups:
            run_groups[name] = []
        run_groups[name].append((fpath, bg))

    js_lines = []
    js_lines.append('var pptxgen = require("pptxgenjs");')
    js_lines.append('var fs = require("fs");')
    js_lines.append('var pres = new pptxgen();')
    js_lines.append('pres.layout = "LAYOUT_16x9";')
    js_lines.append(f'pres.author = "Hs Framework";')
    js_lines.append(f'pres.title = {json.dumps(title)};')

    # Title slide
    js_lines.append('var ts = pres.addSlide();')
    js_lines.append('ts.background = { color: "0D1117" };')
    run_names_str = "  |  ".join(run_groups.keys())
    js_lines.append(f'ts.addText([')
    js_lines.append(f'  {{ text: {json.dumps(title)}, options: {{ fontSize: 36, bold: true, color: "FFFFFF", breakLine: true, fontFace: "Arial" }} }},')
    js_lines.append(f'  {{ text: " ", options: {{ fontSize: 12, breakLine: true }} }},')
    js_lines.append(f'  {{ text: "Polar Stack Slices", options: {{ fontSize: 16, color: "8B949E", breakLine: true, fontFace: "Arial" }} }},')
    js_lines.append(f'  {{ text: {json.dumps(run_names_str)}, options: {{ fontSize: 14, color: "7EE787", fontFace: "Arial" }} }}')
    js_lines.append(f'], {{ x: 0.5, y: 1.0, w: 9.0, h: 3.5, align: "center", valign: "middle" }});')
    js_lines.append(f'ts.addText("Set slideshow to auto-advance (0.5s) for movie playback", {{ x: 0.5, y: 4.8, w: 9.0, h: 0.5, fontSize: 11, color: "484F58", align: "center", fontFace: "Arial" }});')

    bg_map = {"#1A1A2E": "1A1A2E", "#16213E": "16213E", "#10002B": "10002B",
              "#1B1B2F": "1B1B2F", "#0B132B": "0B132B", "#1A1423": "1A1423",
              "#1B2838": "1B2838", "#1E1E2E": "1E1E2E", "#1C1C1C": "1C1C1C",
              "#2D1B69": "2D1B69"}

    for run_name, frames in run_groups.items():
        bg_hex = frames[0][1].lstrip('#')
        # Section divider
        js_lines.append(f'var ds = pres.addSlide();')
        js_lines.append(f'ds.background = {{ color: "{bg_hex}" }};')
        js_lines.append(f'ds.addText({json.dumps(run_name)}, {{ x: 0.5, y: 1.5, w: 9.0, h: 2.0, fontSize: 40, bold: true, color: "FFFFFF", align: "center", valign: "middle", fontFace: "Arial" }});')
        js_lines.append(f'ds.addText("{len(frames)} frames", {{ x: 0.5, y: 3.5, w: 9.0, h: 1.0, fontSize: 16, color: "8B949E", align: "center", fontFace: "Arial" }});')

        for fpath, bg in frames:
            js_lines.append(f'var s = pres.addSlide();')
            js_lines.append(f's.background = {{ color: "{bg_hex}" }};')
            js_lines.append(f'var imgData = "image/png;base64," + fs.readFileSync({json.dumps(fpath)}).toString("base64");')
            js_lines.append(f's.addImage({{ data: imgData, x: 0.15, y: 0.0, w: 9.7, h: 5.625, sizing: {{ type: "contain", w: 9.7, h: 5.625 }} }});')

    # Closing slide
    js_lines.append('var cs = pres.addSlide();')
    js_lines.append('cs.background = { color: "0D1117" };')
    js_lines.append('cs.addText([')
    js_lines.append('  { text: "Hs = R . M . E . C . T . V . S", options: { fontSize: 24, bold: true, color: "58A6FF", breakLine: true, fontFace: "Arial" } },')
    js_lines.append('  { text: " ", options: { fontSize: 12, breakLine: true } },')
    js_lines.append('  { text: "Higgins Decomposition on the Aitchison Simplex", options: { fontSize: 14, color: "8B949E", fontFace: "Arial" } }')
    js_lines.append('], { x: 0.5, y: 1.5, w: 9.0, h: 3.0, align: "center", valign: "middle" });')

    js_lines.append(f'pres.writeFile({{ fileName: {json.dumps(output_path)} }}).then(function() {{')
    js_lines.append(f'  var stats = fs.statSync({json.dumps(output_path)});')
    js_lines.append(f'  console.log("PPTX written: " + {json.dumps(output_path)});')
    js_lines.append(f'  console.log("Size: " + (stats.size / 1024 / 1024).toFixed(1) + " MB");')
    js_lines.append(f'}}).catch(function(e) {{ console.error("Error:", e); }});')

    with open(build_script, 'w') as f:
        f.write('\n'.join(js_lines))

    ret = os.system(f'NODE_PATH=/usr/local/lib/node_modules_global/lib/node_modules node {build_script}')
    if ret != 0:
        print("ERROR: PPTX build failed")
        sys.exit(1)

    # Cleanup frames
    import shutil
    shutil.rmtree(frames_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Generate Hs Compositional Cinema PPTX")
    parser.add_argument("inputs", nargs="+", help="Polar stack JSON files")
    parser.add_argument("--output", "-o", required=True, help="Output PPTX path")
    parser.add_argument("--title", "-t", default="Hs Compositional Cinema", help="Presentation title")
    args = parser.parse_args()

    runs = []
    for path in args.inputs:
        ps = json.load(open(path))
        name = ps.get("test_object", ps.get("experiment", os.path.basename(path)))
        runs.append({"name": name, "carriers": ps["carriers"], "D": ps["D"],
                      "N": ps["N"], "intervals": ps["intervals"]})
        print(f"Loaded: {name} (D={ps['D']}, N={ps['N']})")

    generate_cinema(runs, args.output, args.title)

if __name__ == "__main__":
    main()
