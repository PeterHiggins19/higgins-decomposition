#!/usr/bin/env node
/**
 * HCI Stage 1 — Section Cine-Deck PPTX Generator
 * ================================================
 *
 * Reads stage1_output.json and generates a section cine-deck:
 * ONE SLIDE PER YEAR showing the section triad (XY + XZ + YZ faces)
 * plus the metric ledger for that observation.
 *
 * Per HCI_FOUNDATION.md:
 *   Section triad = XY + XZ + YZ metric sections at one time index
 *   Metric ledger = numerical output table (the measurement authority)
 *   Section cine-deck = PowerPoint scroll deck of section triads
 *
 * This generator is STABLE — the tensor engine is fixed.
 * Only the JSON format matters; this script reads JSON only.
 *
 * Usage:
 *   node build_plates_pptx.js [input.json] [output.pptx]
 *
 * The instrument reads. The expert decides. The loop stays open.
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");

// ── Configuration ────────────────────────────────────────────────
const INPUT_JSON = process.argv[2] || "stage1_output.json";
const OUTPUT_PPTX = process.argv[3] || "HCI_Stage1_Plates.pptx";

// Monochrome palette — instrument grade, no colour
const PAL = {
  bg_dark:  "1A1A1A",
  bg_plate: "F7F7F7",
  bg_card:  "FFFFFF",
  text:     "1A1A1A",
  text_dim: "6B6B6B",
  accent:   "333333",
  grid:     "D0D0D0",
  border:   "BBBBBB",
  current:  "000000",    // current year highlight
  trace:    "999999",    // background trajectory
};

// Carrier abbreviations
const CARRIER_SHORT = {
  "Bioenergy": "Bio", "Coal": "Coal", "Gas": "Gas", "Hydro": "Hyd",
  "Nuclear": "Nuc", "Other Fossil": "OFos", "Solar": "Sol", "Wind": "Wind"
};

// ── Load Data ────────────────────────────────────────────────────
const data = JSON.parse(fs.readFileSync(INPUT_JSON, "utf-8"));
const { carriers, D, N, years, records, locks } = data;

// ── Build Presentation ───────────────────────────────────────────
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "HCI Stage 1 Engine";
pres.title = `HCI Stage 1 Section Cine-Deck — ${data.dataset}`;

// ══════════════════════════════════════════════════════════════════
// SLIDE 1: Title
// ══════════════════════════════════════════════════════════════════
function addTitleSlide() {
  const slide = pres.addSlide();
  slide.background = { color: PAL.bg_dark };

  slide.addText("HCI STAGE 1 — SECTION CINE-DECK", {
    x: 0.8, y: 1.0, w: 8.4, h: 0.8,
    fontSize: 30, fontFace: "Consolas", bold: true, color: "FFFFFF", margin: 0,
  });

  slide.addText([
    { text: `Dataset: ${data.dataset}`, options: { breakLine: true } },
    { text: `Carriers: D = ${D}  (${carriers.join(", ")})`, options: { breakLine: true } },
    { text: `Observations: T = ${N}  (${years[0]}-${years[N-1]})`, options: { breakLine: true } },
    { text: `Bearing pairs: ${D * (D - 1) / 2}`, options: { breakLine: true } },
    { text: `Plates: ${N} section triads (1 per year)`, options: { breakLine: true } },
    { text: `Engine: Compositional Navigation Tensor (CNT)`, options: {} },
  ], {
    x: 0.8, y: 2.1, w: 8.4, h: 2.5,
    fontSize: 14, fontFace: "Consolas", color: "AAAAAA", lineSpacingMultiple: 1.4, margin: 0,
  });

  slide.addText("The instrument reads. The expert decides. The loop stays open.", {
    x: 0.8, y: 4.8, w: 8.4, h: 0.4,
    fontSize: 11, fontFace: "Consolas", italic: true, color: "666666", margin: 0,
  });
}

// ══════════════════════════════════════════════════════════════════
// SECTION PLATE — ONE SLIDE PER YEAR
// ══════════════════════════════════════════════════════════════════
function addSectionPlate(t) {
  const slide = pres.addSlide();
  slide.background = { color: PAL.bg_plate };
  const rec = records[t];

  // ── Header: Year and time index ──
  slide.addText(`SECTION PLATE  t=${t}  |  Year ${rec.year}`, {
    x: 0.3, y: 0.1, w: 5.5, h: 0.35,
    fontSize: 14, fontFace: "Consolas", bold: true, color: PAL.text, margin: 0,
  });

  slide.addText(`Hs = ${rec.hs.toFixed(4)}  |  ${rec.ring}  |  omega = ${rec.angular_velocity_deg.toFixed(2)} deg`, {
    x: 5.8, y: 0.1, w: 4.0, h: 0.35,
    fontSize: 11, fontFace: "Consolas", color: PAL.text_dim, align: "right", margin: 0,
  });

  // ── YZ FACE: Hs vs Time (line chart, current year highlighted) ──
  slide.addText("YZ: Hs vs Time", {
    x: 0.3, y: 0.45, w: 3.0, h: 0.25,
    fontSize: 9, fontFace: "Consolas", bold: true, color: PAL.text, margin: 0,
  });

  const hsValues = records.map(r => r.hs);
  // Create highlight series: only current year has value, rest null
  const hsHighlight = records.map((r, i) => i === t ? r.hs : null);
  const yearLabels = years.map(String);

  slide.addChart(pres.charts.LINE, [
    { name: "Hs", labels: yearLabels, values: hsValues },
  ], {
    x: 0.2, y: 0.7, w: 4.6, h: 2.2,
    lineSize: 1.5,
    chartColors: [PAL.current],
    showValue: false,
    valAxisMinVal: 0, valAxisMaxVal: 0.5,
    catAxisLabelColor: PAL.text_dim,
    catAxisLabelFontSize: 6,
    valAxisLabelColor: PAL.text_dim,
    valAxisLabelFontSize: 7,
    valGridLine: { color: PAL.grid, size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: false,
    chartArea: { fill: { color: PAL.bg_card } },
    showMarker: true, markerSize: 3,
  });

  // Current year indicator (text overlay on chart area)
  const chartXStart = 0.2;
  const chartW = 4.6;
  const yearFrac = t / Math.max(N - 1, 1);
  const markerX = chartXStart + 0.35 + yearFrac * (chartW - 0.7);

  slide.addText(`${rec.year}`, {
    x: Math.max(0.3, markerX - 0.2), y: 2.85, w: 0.5, h: 0.2,
    fontSize: 7, fontFace: "Consolas", bold: true, color: PAL.current, align: "center", margin: 0,
  });

  // ── XZ FACE: Bearing vs Time (pick dominant bearing pair) ──
  // Find highest-magnitude bearing pair for this year
  let bestPair = null;
  let bestAngle = 0;
  for (let i = 0; i < D; i++) {
    for (let j = i + 1; j < D; j++) {
      const key = `${carriers[i]}-${carriers[j]}`;
      const angle = Math.abs(rec.bearings_deg[key] || 0);
      if (angle > bestAngle) {
        bestAngle = angle;
        bestPair = key;
      }
    }
  }

  const shortPair = bestPair ?
    bestPair.replace("Other Fossil", "OFos").split("-").map(s => s.substring(0, 4)).join("-") :
    "---";

  slide.addText(`XZ: Bearing(${shortPair}) vs Time`, {
    x: 5.0, y: 0.45, w: 4.8, h: 0.25,
    fontSize: 9, fontFace: "Consolas", bold: true, color: PAL.text, margin: 0,
  });

  if (bestPair) {
    const bearingValues = records.map(r => r.bearings_deg[bestPair] || 0);

    slide.addChart(pres.charts.LINE, [
      { name: shortPair, labels: yearLabels, values: bearingValues },
    ], {
      x: 4.9, y: 0.7, w: 4.9, h: 2.2,
      lineSize: 1.5,
      chartColors: [PAL.current],
      showValue: false,
      catAxisLabelColor: PAL.text_dim,
      catAxisLabelFontSize: 6,
      valAxisLabelColor: PAL.text_dim,
      valAxisLabelFontSize: 7,
      valGridLine: { color: PAL.grid, size: 0.5 },
      catGridLine: { style: "none" },
      showLegend: false,
      chartArea: { fill: { color: PAL.bg_card } },
      showMarker: true, markerSize: 3,
    });
  }

  // ── XY FACE (PLAN VIEW): Bearing polar at this time index ──
  // Rendered as a data table of all 28 bearings — polar plots don't
  // render well in PptxGenJS, so we use the metric ledger format
  slide.addText("XY PLAN VIEW: All Bearings (deg)", {
    x: 0.3, y: 3.05, w: 4.5, h: 0.25,
    fontSize: 9, fontFace: "Consolas", bold: true, color: PAL.text, margin: 0,
  });

  // Sort bearings by absolute magnitude
  const bearingEntries = Object.entries(rec.bearings_deg)
    .map(([pair, angle]) => [pair.replace("Other Fossil", "OFos"), angle])
    .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]));

  // Split into 2 columns of 14 rows
  const half = Math.ceil(bearingEntries.length / 2);
  const col1Text = bearingEntries.slice(0, half)
    .map(([p, a]) => `${p.padEnd(12)} ${a >= 0 ? "+" : ""}${a.toFixed(1)}`)
    .join("\n");
  const col2Text = bearingEntries.slice(half)
    .map(([p, a]) => `${p.padEnd(12)} ${a >= 0 ? "+" : ""}${a.toFixed(1)}`)
    .join("\n");

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.3, y: 3.3, w: 4.5, h: 2.2,
    fill: { color: PAL.bg_card },
    line: { color: PAL.border, width: 0.5 },
  });

  slide.addText(col1Text, {
    x: 0.4, y: 3.35, w: 2.2, h: 2.1,
    fontSize: 7, fontFace: "Consolas", color: PAL.text, valign: "top", margin: 0,
  });

  slide.addText(col2Text, {
    x: 2.6, y: 3.35, w: 2.2, h: 2.1,
    fontSize: 7, fontFace: "Consolas", color: PAL.text, valign: "top", margin: 0,
  });

  // ── METRIC LEDGER ──
  slide.addText("METRIC LEDGER", {
    x: 5.0, y: 3.05, w: 4.8, h: 0.25,
    fontSize: 9, fontFace: "Consolas", bold: true, color: PAL.text, margin: 0,
  });

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 5.0, y: 3.3, w: 4.8, h: 2.2,
    fill: { color: PAL.bg_card },
    line: { color: PAL.border, width: 0.5 },
  });

  // Ledger content
  const helm = rec.helmsman ? (CARRIER_SHORT[rec.helmsman] || rec.helmsman.substring(0, 4)) : "---";
  const kappaStr = rec.condition_number > 1e6 ? rec.condition_number.toExponential(1) : rec.condition_number.toFixed(2);

  const ledgerLines = [
    `Hs       = ${rec.hs.toFixed(6)}     Ring  = ${rec.ring}`,
    `E_metric = ${rec.metric_energy.toFixed(6)}     kappa = ${kappaStr}`,
    `omega    = ${rec.angular_velocity_deg.toFixed(4)} deg`,
    `d_A      = ${rec.d_aitchison.toFixed(6)}`,
    `Helm     = ${helm}  delta = ${rec.helmsman_delta >= 0 ? "+" : ""}${rec.helmsman_delta.toFixed(6)}`,
    ``,
    `CLR:`,
  ];

  // CLR values in 2 rows of 4
  const clrRow1 = carriers.slice(0, 4).map((c, j) =>
    `${(CARRIER_SHORT[c] || c.substring(0, 3)).padEnd(4)}${rec.clr[j] >= 0 ? "+" : ""}${rec.clr[j].toFixed(3)}`
  ).join("  ");
  const clrRow2 = carriers.slice(4).map((c, j) =>
    `${(CARRIER_SHORT[c] || c.substring(0, 3)).padEnd(4)}${rec.clr[j + 4] >= 0 ? "+" : ""}${rec.clr[j + 4].toFixed(3)}`
  ).join("  ");

  ledgerLines.push(` ${clrRow1}`);
  ledgerLines.push(` ${clrRow2}`);

  // Steering sensitivity
  ledgerLines.push(``);
  ledgerLines.push(`Steering (1/x_j):`);
  const sensRow1 = carriers.slice(0, 4).map(c => {
    const val = rec.steering_sensitivity[c] || 0;
    const txt = val > 999 ? val.toExponential(0) : val.toFixed(1);
    return `${(CARRIER_SHORT[c] || c.substring(0, 3)).padEnd(4)}${txt.padStart(7)}`;
  }).join(" ");
  const sensRow2 = carriers.slice(4).map(c => {
    const val = rec.steering_sensitivity[c] || 0;
    const txt = val > 999 ? val.toExponential(0) : val.toFixed(1);
    return `${(CARRIER_SHORT[c] || c.substring(0, 3)).padEnd(4)}${txt.padStart(7)}`;
  }).join(" ");
  ledgerLines.push(` ${sensRow1}`);
  ledgerLines.push(` ${sensRow2}`);

  slide.addText(ledgerLines.join("\n"), {
    x: 5.1, y: 3.35, w: 4.6, h: 2.1,
    fontSize: 7, fontFace: "Consolas", color: PAL.text, valign: "top", margin: 0,
  });
}

// ══════════════════════════════════════════════════════════════════
// LOCK DETECTION SLIDE
// ══════════════════════════════════════════════════════════════════
function addLocksSlide() {
  const slide = pres.addSlide();
  slide.background = { color: PAL.bg_plate };

  slide.addText("INFORMATIONAL LOCK DETECTION", {
    x: 0.5, y: 0.3, w: 9, h: 0.4,
    fontSize: 16, fontFace: "Consolas", bold: true, color: PAL.text, margin: 0,
  });

  slide.addText("Carrier pairs with bearing spread < 10 deg across all years", {
    x: 0.5, y: 0.7, w: 9, h: 0.3,
    fontSize: 10, fontFace: "Consolas", color: PAL.text_dim, margin: 0,
  });

  if (locks && locks.length > 0) {
    const lockText = locks.map(lk =>
      `LOCKED: ${lk.carrier_i} - ${lk.carrier_j}    spread = ${lk.bearing_spread_deg.toFixed(1)} deg`
    ).join("\n");

    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: 1.2, w: 9, h: 0.5 + locks.length * 0.35,
      fill: { color: "EEEEEE" },
      line: { color: PAL.accent, width: 1.5 },
    });

    slide.addText(lockText, {
      x: 0.7, y: 1.3, w: 8.6, h: 0.3 + locks.length * 0.35,
      fontSize: 12, fontFace: "Consolas", bold: true, color: PAL.text, margin: 0,
    });

    // Show locked pair bearing trace
    const lk = locks[0];
    const ci = carriers.indexOf(lk.carrier_i);
    const cj = carriers.indexOf(lk.carrier_j);
    const pairKey = `${carriers[ci]}-${carriers[cj]}`;
    const bearingValues = records.map(r => r.bearings_deg[pairKey] || 0);

    slide.addChart(pres.charts.LINE, [{
      name: pairKey, labels: years.map(String), values: bearingValues,
    }], {
      x: 0.5, y: 2.3, w: 9, h: 3.0,
      lineSize: 2,
      chartColors: [PAL.current],
      showValue: false,
      catAxisLabelColor: PAL.text_dim,
      catAxisLabelFontSize: 8,
      valAxisLabelColor: PAL.text_dim,
      valGridLine: { color: PAL.grid, size: 0.5 },
      catGridLine: { style: "none" },
      showLegend: false,
      showTitle: true, title: `Bearing: ${pairKey} (LOCKED)`, titleColor: PAL.text, titleFontSize: 10,
      chartArea: { fill: { color: PAL.bg_card } },
      showMarker: true, markerSize: 4,
    });
  } else {
    slide.addText("No locked pairs detected (threshold = 10 deg)", {
      x: 0.5, y: 1.2, w: 9, h: 0.5,
      fontSize: 12, fontFace: "Consolas", color: PAL.text, margin: 0,
    });
  }
}

// ══════════════════════════════════════════════════════════════════
// CLOSING SLIDE
// ══════════════════════════════════════════════════════════════════
function addClosingSlide() {
  const slide = pres.addSlide();
  slide.background = { color: PAL.bg_dark };

  slide.addText("Section Cine-Deck Complete", {
    x: 0.8, y: 1.5, w: 8.4, h: 0.7,
    fontSize: 26, fontFace: "Consolas", bold: true, color: "FFFFFF", margin: 0,
  });

  slide.addText([
    { text: `${N} section plates (1 per year)`, options: { breakLine: true } },
    { text: `${D * (D - 1) / 2} bearing pairs per plate`, options: { breakLine: true } },
    { text: `Locks detected: ${locks ? locks.length : 0}`, options: { breakLine: true } },
    { text: `Source: ${INPUT_JSON}`, options: {} },
  ], {
    x: 0.8, y: 2.5, w: 8.4, h: 1.8,
    fontSize: 13, fontFace: "Consolas", color: "AAAAAA", lineSpacingMultiple: 1.4, margin: 0,
  });

  slide.addText("The instrument reads. The expert decides. The loop stays open.", {
    x: 0.8, y: 4.5, w: 8.4, h: 0.4,
    fontSize: 11, fontFace: "Consolas", italic: true, color: "666666", margin: 0,
  });
}

// ══════════════════════════════════════════════════════════════════
// BUILD
// ══════════════════════════════════════════════════════════════════

addTitleSlide();                          // Slide 1

for (let t = 0; t < N; t++) {            // Slides 2-27 (one per year)
  addSectionPlate(t);
}

addLocksSlide();                          // Slide 28
addClosingSlide();                        // Slide 29

const totalSlides = 2 + N + 1;

pres.writeFile({ fileName: OUTPUT_PPTX })
  .then(() => {
    console.log(`PPTX written: ${OUTPUT_PPTX}`);
    console.log(`Slides: ${totalSlides} (1 title + ${N} section plates + 1 locks + 1 closing)`);
    console.log(`Source: ${INPUT_JSON}`);
  })
  .catch(err => {
    console.error("Error writing PPTX:", err);
    process.exit(1);
  });
