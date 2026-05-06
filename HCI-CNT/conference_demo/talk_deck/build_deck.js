/**
 * CodaWork 2026 — 10-slide CNT presentation deck.
 *
 * Honours the Higgins Display Standard:
 *   dark monochrome background, line graphics only, large readable text.
 *
 * Reuses existing SVGs from cnt_presentation/ and adds new
 * side-by-side comparison flow charts.
 *
 * Build:
 *   NODE_PATH=/usr/local/lib/node_modules_global/lib/node_modules node build_deck.js
 */
const pptxgen = require("pptxgenjs");
const sharp = require("sharp");
const fs = require("fs");
const path = require("path");

const DIR = __dirname;
const OUTPUT = path.join(DIR, "CodaWork2026_CNT_Talk.pptx");

const SLIDES = [
  // 1. Title — text-only
  { kind: "title" },

  // 2. Value to CoDa — text + bullets
  { kind: "value" },

  // 3. CNT pipeline overview (existing SVG: closure → CLR)
  { kind: "svg", file: "slide_01a_pipeline_input.svg",
    note: "Pipeline overview — raw → closed → CLR." },

  // 4. Side-by-side: Closure + CLR (new SVG)
  { kind: "svg", file: "slide_cmp_closure_clr.svg",
    note: "Same step in both pipelines. CNT adds the audit metadata." },

  // 5. Side-by-side: Helmert ILR (new SVG)
  { kind: "svg", file: "slide_cmp_helmert_ilr.svg",
    note: "Egozcue's projection in both. CNT publishes V in the JSON and uses one shared FIXED window across panels." },

  // 6. Side-by-side: Bearing tensor — atan2 vs arccos (new SVG; the headline)
  { kind: "svg", file: "slide_cmp_bearing_atan2.svg",
    note: "Same angle. atan2 keeps extra numerical headroom near the axes — useful for trajectory locks." },

  // 7. Side-by-side: Metric tensor M² = I (new SVG)
  { kind: "svg", file: "slide_cmp_metric_m2.svg",
    note: "CNT addition: M² = I provides the contraction certificate the depth tower needs." },

  // 8. CNT depth tower → period-2 attractor → IR class (new SVG)
  { kind: "svg", file: "slide_cnt_depth_attractor.svg",
    note: "CNT additions built on M²=I: recursive depth sounder converging on a period-2 attractor." },

  // 9. CBS three orthogonal projection (existing SVG — Peter's keep-this slide)
  { kind: "svg", file: "slide_02a_cube_structure.svg",
    note: "CBS — three orthogonal faces of the compositional bearing scope." },

  // 10. Closing one-picture summary (new SVG)
  { kind: "svg", file: "slide_pipeline_summary.svg",
    note: "Hash chain end-to-end. 25 experiments. Anyone with the raw CSV can verify any plate in ~2 minutes." },
];

async function svgToPng(p, w, h) {
  const buf = fs.readFileSync(p);
  const out = await sharp(buf).resize(w, h, {
    fit: "contain", background: { r: 26, g: 26, b: 26, alpha: 1 }
  }).png().toBuffer();
  return "image/png;base64," + out.toString("base64");
}

async function build() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "P. Higgins";
  pres.title  = "CNT — CodaWork 2026 Talk";

  for (let i = 0; i < SLIDES.length; i++) {
    const s = SLIDES[i];
    const slide = pres.addSlide();
    slide.background = { color: "1A1A1A" };

    if (s.kind === "title") {
      // Slide 1 — title card
      slide.addText("Compositional Navigation Tensor", {
        x: 0.5, y: 1.0, w: 9, h: 1.0,
        fontSize: 38, fontFace: "Arial", bold: true, color: "FFFFFF",
        align: "center"
      });
      slide.addText("A hash-traceable instrument for compositional dynamics", {
        x: 0.5, y: 2.0, w: 9, h: 0.6,
        fontSize: 22, fontFace: "Georgia", italic: true, color: "AAAAAA",
        align: "center"
      });
      slide.addText("CoDaWork 2026", {
        x: 0.5, y: 3.0, w: 9, h: 0.6,
        fontSize: 28, fontFace: "Arial", bold: true, color: "F0C020",
        align: "center"
      });
      slide.addText("P. Higgins", {
        x: 0.5, y: 3.8, w: 9, h: 0.4,
        fontSize: 20, fontFace: "Arial", color: "DDDDDD",
        align: "center"
      });
      slide.addText("The instrument reads.  The expert decides.  The hashes hold the line.", {
        x: 0.5, y: 4.8, w: 9, h: 0.4,
        fontSize: 14, fontFace: "Georgia", italic: true, color: "888888",
        align: "center"
      });
      slide.addNotes("Open: 'I'm going to show you an instrument my team built. Classical CoDa toolkit, deterministic engine, trajectory-native operators, hash-chained reports. Verifiable in two minutes. That's the talk.'");
    }
    else if (s.kind === "value") {
      // Slide 2 — value to CoDa
      slide.addText("What CNT adds on top of the CoDa toolkit", {
        x: 0.5, y: 0.4, w: 9, h: 0.8,
        fontSize: 32, fontFace: "Arial", bold: true, color: "FFFFFF",
        align: "center", margin: 0
      });
      slide.addText("Three additions that complement the established CoDa methods:", {
        x: 0.5, y: 1.3, w: 9, h: 0.5,
        fontSize: 18, fontFace: "Arial", color: "CCCCCC",
        align: "center", italic: true
      });

      // 3 columns of value
      const cols = [
        { t: "Trajectory operators", b: "bearings, ω, helmsman, period-2 attractor, IR class — first-class objects in the algebra, computed alongside the standard ILR." },
        { t: "End-to-end determinism", b: "raw CSV → JSON → PDF byte-identical. content_sha256 + engine_signature on every page, supporting reproducibility for both pipelines." },
        { t: "Cross-dataset inference", b: "Stage 4 reports compare attractor amplitude, depth tower, and IR distribution across multiple datasets in one document." }
      ];
      for (let k = 0; k < cols.length; k++) {
        const x = 0.4 + k * 3.15;
        slide.addShape(pres.shapes.RECTANGLE, {
          x: x, y: 1.95, w: 3.0, h: 2.6,
          fill: { color: "2A2A3A" }, line: { color: "66AAFF", width: 1.5 }
        });
        slide.addText(cols[k].t, {
          x: x + 0.15, y: 2.05, w: 2.7, h: 0.5,
          fontSize: 18, fontFace: "Arial", bold: true, color: "FFFFFF",
          align: "center", margin: 0
        });
        slide.addText(cols[k].b, {
          x: x + 0.15, y: 2.6, w: 2.7, h: 1.9,
          fontSize: 14, fontFace: "Arial", color: "DDDDDD",
          align: "center", valign: "top"
        });
      }

      slide.addText("These ship alongside the classical plates — both languages, one report.", {
        x: 0.5, y: 4.75, w: 9, h: 0.4,
        fontSize: 18, fontFace: "Arial", italic: true, color: "F0C020",
        align: "center"
      });
      slide.addText("Variation matrix · biplot · balance dendrogram · SBP · ternary · scree — same engine.", {
        x: 0.5, y: 5.15, w: 9, h: 0.4,
        fontSize: 14, fontFace: "Arial", color: "AAAAAA",
        align: "center"
      });
      slide.addNotes("'This isn't a replacement for ILR or the classical biplot. It's an extension that ships those plates plus the trajectory-native ones in one report. Both languages, one document.'");
    }
    else if (s.kind === "svg") {
      const p = path.join(DIR, s.file);
      if (!fs.existsSync(p)) {
        console.log(`SKIP missing: ${s.file}`); continue;
      }
      const img = await svgToPng(p, 1920, 1075);
      slide.addImage({ data: img, x: 0, y: 0, w: 10, h: 5.625 });
      if (s.note) slide.addNotes(s.note);
      console.log(`Slide ${i+1}: ${s.file}`);
    }
  }

  await pres.writeFile({ fileName: OUTPUT });
  console.log(`\nWrote ${OUTPUT}  (${SLIDES.length} slides)`);
}

build().catch(e => { console.error(e); process.exit(1); });
