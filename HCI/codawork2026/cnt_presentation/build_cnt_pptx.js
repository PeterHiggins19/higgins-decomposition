/**
 * CNT Tensor Engine Presentation — CoDaWork 2026
 *
 * Builds PowerPoint from SVG diagram slides.
 * Section: CNT Tensor Engine
 *
 * DISPLAY STANDARD: Maximum text size. Back row readable. More slides over smaller text.
 * Line graphics only. No decoration. Every pixel transfers information.
 *
 * Usage:
 *   NODE_PATH=/usr/local/lib/node_modules_global/lib/node_modules node build_cnt_pptx.js
 */

const pptxgen = require("pptxgenjs");
const sharp = require("sharp");
const fs = require("fs");
const path = require("path");

const DIR = __dirname;
const OUTPUT = path.join(DIR, "CNT_Tensor_Engine.pptx");

// All slides in order — large text, split across multiple slides for readability
const SLIDES = [
  { file: "slide_01a_pipeline_input.svg",    title: "CNT Pipeline -- Raw Data to CLR" },
  { file: "slide_01b_theta_omega.svg",       title: "CNT Channels 1-2: Bearing + Angular Velocity" },
  { file: "slide_01c_kappa_sigma.svg",       title: "CNT Channels 3-4: Steering + Helmsman" },
  { file: "slide_01d_corollaries_output.svg", title: "CNT Corollaries and Output Summary" },
  { file: "slide_02a_cube_structure.svg",    title: "CBS Cube -- 3D Structure" },
  { file: "slide_02b_higgins_axis.svg",      title: "Higgins Axis -- Time Projection" },
  { file: "slide_02c_face_specs.svg",        title: "CBS Face Specifications" },
  { file: "slide_03_hlr_evidence.svg",       title: "HLR Unit Family -- Conversion Evidence" },
];

async function svgToBase64Png(svgPath, width, height) {
  const svgBuffer = fs.readFileSync(svgPath);
  const pngBuffer = await sharp(svgBuffer)
    .resize(width, height, { fit: "contain", background: { r: 26, g: 26, b: 26, alpha: 1 } })
    .png()
    .toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

async function build() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = "P. Higgins";
  pres.title = "CNT — Compositional Navigation Tensor Engine";

  // ── Title Slide ──────────────────────────────────────────
  const titleSlide = pres.addSlide();
  titleSlide.background = { color: "1A1A1A" };
  titleSlide.addText("CNT — Compositional Navigation Tensor", {
    x: 0.5, y: 1.5, w: 9, h: 1.2,
    fontSize: 36, fontFace: "Arial", bold: true, color: "FFFFFF",
    align: "center"
  });
  titleSlide.addText("CoDaWork 2026 — Tensor Engine Section", {
    x: 0.5, y: 2.8, w: 9, h: 0.6,
    fontSize: 22, fontFace: "Arial", color: "AAAAAA",
    align: "center"
  });
  titleSlide.addText("P. Higgins", {
    x: 0.5, y: 3.8, w: 9, h: 0.5,
    fontSize: 18, fontFace: "Arial", color: "CCCCCC",
    align: "center"
  });
  titleSlide.addText("The instrument reads. The expert decides. The loop stays open.", {
    x: 0.5, y: 4.6, w: 9, h: 0.4,
    fontSize: 14, fontFace: "Georgia", italic: true, color: "888888",
    align: "center"
  });

  // ── Content Slides ──────────────────────────────────────
  for (const s of SLIDES) {
    const svgPath = path.join(DIR, s.file);
    if (!fs.existsSync(svgPath)) {
      console.log(`SKIP (not found): ${s.file}`);
      continue;
    }
    console.log(`Rendering ${s.file} ...`);
    // 1000:560 aspect ratio -> full 16:9 slide
    const img = await svgToBase64Png(svgPath, 1920, 1075);

    const slide = pres.addSlide();
    slide.background = { color: "1A1A1A" };
    // Full-bleed image — fill the entire slide
    slide.addImage({ data: img, x: 0, y: 0, w: 10, h: 5.625 });
  }

  // ── Write ────────────────────────────────────────────────
  await pres.writeFile({ fileName: OUTPUT });
  console.log(`\nDone: ${OUTPUT}`);
  console.log(`${SLIDES.length + 1} slides: Title + ${SLIDES.length} diagram slides`);
}

build().catch(err => { console.error(err); process.exit(1); });
