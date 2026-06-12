// HCI Japan CoDaWork2026 PowerPoint Builder
// Higgins Computational Instruments — Japan EMBER Electricity Generation (2000-2025)

const pptxgen = require("/usr/local/lib/node_modules_global/lib/node_modules/pptxgenjs");
const path = require("path");
const data = require("./hci_japan_results.json");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Peter Higgins";
pres.title = "HCI Analysis — Japan Electricity Generation (2000-2025)";

// ── Constants ──
const W = 10, H = 5.625;
const PRIMARY = "36454F";
const SECONDARY = "F2F2F2";
const ACCENT = "212121";
const WHITE = "FFFFFF";
const LIGHT_GRAY = "E0E0E0";
const BORDER_GRAY = "CCCCCC";
const FONT = "Calibri";

const CARRIER_COLORS = ["4CAF50","424242","FF9800","2196F3","9C27B0","795548","FFC107","00BCD4"];
const CARRIERS = data.carriers;
const YEARS = data.years;
const CBS = data.cbs_records;

// ── Helpers ──
function fmt(v, dp) { if (v == null) return "-"; return typeof v === "number" ? v.toFixed(dp) : String(v); }
function fmtSci(v, dp) {
  if (v == null) return "-";
  if (Math.abs(v) >= 1e6) return v.toExponential(dp || 1);
  return v.toFixed(dp || 2);
}

function darkSlide() {
  const s = pres.addSlide();
  s.background = { color: PRIMARY };
  return s;
}
function lightSlide() {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  return s;
}

function addSectionHeader(slide, text) {
  slide.addText(text, {
    x: 0.5, y: 0.2, w: 9, h: 0.4,
    fontSize: 10, fontFace: FONT, color: "999999", bold: false
  });
}

function addSlideTitle(slide, text, opts) {
  const dark = opts && opts.dark;
  slide.addText(text, {
    x: 0.5, y: dark ? undefined : 0.3, w: 9, h: 0.55,
    fontSize: 22, fontFace: FONT, color: dark ? WHITE : ACCENT, bold: true,
    ...(dark ? { y: 0.3 } : { y: 0.55 })
  });
}

function tableOpts(x, y, w, colW, fontSize) {
  return {
    x: x, y: y, w: w,
    colW: colW,
    fontSize: fontSize || 8,
    fontFace: FONT,
    border: { pt: 0.5, color: BORDER_GRAY },
    autoPage: false,
    autoPageRepeatHeader: true,
    margin: [1, 2, 1, 2]
  };
}

function headerCell(text) {
  return { text: text, options: { bold: true, fill: { color: LIGHT_GRAY }, color: ACCENT, fontSize: 7, align: "center", valign: "middle" } };
}

function dataCell(text, opts) {
  return { text: text, options: { color: "333333", fontSize: 7, align: "right", valign: "middle", ...(opts || {}) } };
}

// ── SLIDE 1: Title ──
(function() {
  const s = darkSlide();
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.08, fill: { color: "9C27B0" } });
  s.addText("HCI Analysis", {
    x: 0.8, y: 1.2, w: 8.4, h: 1.0,
    fontSize: 40, fontFace: FONT, color: WHITE, bold: true
  });
  s.addText("Japan Electricity Generation (2000–2025)", {
    x: 0.8, y: 2.1, w: 8.4, h: 0.6,
    fontSize: 22, fontFace: FONT, color: LIGHT_GRAY
  });
  s.addShape(pres.shapes.LINE, { x: 0.8, y: 2.85, w: 3.5, h: 0, line: { color: "9C27B0", width: 2 } });
  s.addText("Higgins Computational Instruments — CoDaWork 2026", {
    x: 0.8, y: 3.1, w: 8.4, h: 0.4,
    fontSize: 14, fontFace: FONT, color: "AAAAAA"
  });
  s.addText("EMBER Dataset  |  8 Carriers  |  26 Years  |  3-Stage Analysis", {
    x: 0.8, y: 3.6, w: 8.4, h: 0.35,
    fontSize: 11, fontFace: FONT, color: "888888"
  });
  s.addText("Peter Higgins", {
    x: 0.8, y: 4.6, w: 4, h: 0.3,
    fontSize: 11, fontFace: FONT, color: "777777"
  });
})();

// ── SLIDE 2: Stacked Bar — Raw Composition (TWh proxy) ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 1 — RAW DATA");
  addSlideTitle(s, "Raw Composition — Stacked Shares by Year");

  // Build chart data: each carrier is a series
  const chartData = CARRIERS.map((c, ci) => ({
    name: c,
    labels: YEARS.map(String),
    values: CBS.map(r => r.composition[ci])
  }));

  s.addChart(pres.charts.BAR, chartData, {
    x: 0.5, y: 1.1, w: 9, h: 4.2,
    barDir: "col", barGrouping: "stacked",
    chartColors: CARRIER_COLORS,
    showLegend: true, legendPos: "b", legendFontSize: 7,
    catAxisLabelColor: "666666", catAxisLabelFontSize: 7,
    valAxisLabelColor: "666666", valAxisLabelFontSize: 7,
    catAxisOrientation: "minMax",
    valGridLine: { color: "E8E8E8", size: 0.5 },
    catGridLine: { style: "none" },
    showTitle: false
  });
})();

// ── SLIDE 3: Line Chart — Compositional Fractions ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 1 — RAW DATA");
  addSlideTitle(s, "Compositional Fractions Over Time (Percentage Shares)");

  const chartData = CARRIERS.map((c, ci) => ({
    name: c,
    labels: YEARS.map(String),
    values: CBS.map(r => +(r.composition[ci] * 100).toFixed(2))
  }));

  s.addChart(pres.charts.LINE, chartData, {
    x: 0.5, y: 1.1, w: 9, h: 4.2,
    chartColors: CARRIER_COLORS,
    lineSize: 2,
    showLegend: true, legendPos: "r", legendFontSize: 7,
    catAxisLabelColor: "666666", catAxisLabelFontSize: 7,
    valAxisLabelColor: "666666", valAxisLabelFontSize: 7,
    valGridLine: { color: "E8E8E8", size: 0.5 },
    catGridLine: { style: "none" },
    showTitle: false
  });
})();

// ── SLIDE 4: CLR Coordinates Line Chart ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 1 — RAW DATA");
  addSlideTitle(s, "CLR Coordinates (Higgins Coordinates) Over Time");

  const chartData = CARRIERS.map((c, ci) => ({
    name: c,
    labels: YEARS.map(String),
    values: CBS.map(r => +r.clr[ci].toFixed(3))
  }));

  s.addChart(pres.charts.LINE, chartData, {
    x: 0.5, y: 1.1, w: 9, h: 4.2,
    chartColors: CARRIER_COLORS,
    lineSize: 2,
    showLegend: true, legendPos: "r", legendFontSize: 7,
    catAxisLabelColor: "666666", catAxisLabelFontSize: 7,
    valAxisLabelColor: "666666", valAxisLabelFontSize: 7,
    valGridLine: { color: "E8E8E8", size: 0.5 },
    catGridLine: { style: "none" },
    showTitle: false
  });
})();

// ── SLIDE 5: Higgins Scale (Hs) Over Time ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 1 — RAW DATA");
  addSlideTitle(s, "Higgins Scale (Hs) Over Time");

  s.addChart(pres.charts.LINE, [{
    name: "Hs",
    labels: YEARS.map(String),
    values: CBS.map(r => +r.hs.toFixed(4))
  }], {
    x: 0.5, y: 1.1, w: 9, h: 4.0,
    chartColors: ["9C27B0"],
    lineSize: 3,
    showLegend: false,
    catAxisLabelColor: "666666", catAxisLabelFontSize: 7,
    valAxisLabelColor: "666666", valAxisLabelFontSize: 7,
    valGridLine: { color: "E8E8E8", size: 0.5 },
    catGridLine: { style: "none" },
    showTitle: false,
    showValue: false
  });

  // Annotation
  s.addText("Hs range: " + fmt(Math.min(...CBS.map(r=>r.hs)),4) + " – " + fmt(Math.max(...CBS.map(r=>r.hs)),4), {
    x: 0.5, y: 5.1, w: 5, h: 0.3, fontSize: 9, fontFace: FONT, color: "888888"
  });
})();

// ── SLIDE 6: Angular Velocity Over Time ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 1 — RAW DATA");
  addSlideTitle(s, "Angular Velocity (ω) Over Time — Fukushima Signal");

  s.addChart(pres.charts.LINE, [{
    name: "ω (deg)",
    labels: YEARS.map(String),
    values: CBS.map(r => +r.angular_velocity_deg.toFixed(2))
  }], {
    x: 0.5, y: 1.1, w: 9, h: 4.0,
    chartColors: ["FF5722"],
    lineSize: 3,
    showLegend: false,
    catAxisLabelColor: "666666", catAxisLabelFontSize: 7,
    valAxisLabelColor: "666666", valAxisLabelFontSize: 7,
    valGridLine: { color: "E8E8E8", size: 0.5 },
    catGridLine: { style: "none" },
    showTitle: false
  });

  // Fukushima annotation
  s.addShape(pres.shapes.RECTANGLE, {
    x: 4.3, y: 1.1, w: 1.5, h: 4.0,
    fill: { color: "FF0000", transparency: 90 },
    line: { color: "FF0000", width: 0.5, dashType: "dash" }
  });
  s.addText("Fukushima\n2011–2014", {
    x: 4.3, y: 1.15, w: 1.5, h: 0.45,
    fontSize: 7, fontFace: FONT, color: "CC0000", align: "center"
  });
})();

// ── SLIDE 7: Metric Energy + Condition Number ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 2 — STAGE 1 CBS/CNT PLATES");
  addSlideTitle(s, "Metric Energy & Condition Number Over Time");

  // Two line series on separate axes not directly supported, so two charts side by side
  s.addChart(pres.charts.LINE, [{
    name: "Metric Energy",
    labels: YEARS.map(String),
    values: CBS.map(r => +r.metric_energy.toFixed(2))
  }], {
    x: 0.3, y: 1.2, w: 4.5, h: 3.8,
    chartColors: ["2196F3"],
    lineSize: 2,
    showLegend: true, legendPos: "t", legendFontSize: 7,
    catAxisLabelColor: "666666", catAxisLabelFontSize: 6,
    valAxisLabelColor: "666666", valAxisLabelFontSize: 7,
    valGridLine: { color: "E8E8E8", size: 0.5 },
    catGridLine: { style: "none" },
    showTitle: false
  });

  s.addChart(pres.charts.LINE, [{
    name: "Condition Number",
    labels: YEARS.map(String),
    values: CBS.map(r => +r.condition_number.toFixed(0))
  }], {
    x: 5.2, y: 1.2, w: 4.5, h: 3.8,
    chartColors: ["FF9800"],
    lineSize: 2,
    showLegend: true, legendPos: "t", legendFontSize: 7,
    catAxisLabelColor: "666666", catAxisLabelFontSize: 6,
    valAxisLabelColor: "666666", valAxisLabelFontSize: 7,
    valGridLine: { color: "E8E8E8", size: 0.5 },
    catGridLine: { style: "none" },
    showTitle: false
  });
})();

// ── SLIDE 8: Steering Sensitivity Table (morphographic plate) ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 2 — STAGE 1 CBS/CNT PLATES");
  s.addText("Steering Sensitivity — All Carriers × All Years (Morphographic Plate)", {
    x: 0.3, y: 0.45, w: 9.4, h: 0.35, fontSize: 14, fontFace: FONT, color: ACCENT, bold: true
  });

  const header = [headerCell("Year"), ...CARRIERS.map(c => headerCell(c))];
  const rows = CBS.map(r => {
    const yr = dataCell(String(r.year), { align: "center", bold: true });
    const cells = CARRIERS.map(c => dataCell(fmtSci(r.steering_sensitivity[c], 1)));
    return [yr, ...cells];
  });

  const colW = [0.55, ...CARRIERS.map(() => 1.05)];
  s.addTable([header, ...rows], {
    ...tableOpts(0.2, 0.85, 9.6, colW, 6),
    fontSize: 6
  });
})();

// ── SLIDE 9: Helmsman (DCDI) History Table ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 2 — STAGE 1 CBS/CNT PLATES");
  addSlideTitle(s, "Helmsman (DCDI) History — All Transitions");

  const header = [headerCell("Year"), headerCell("Helmsman"), headerCell("ω (deg)"), headerCell("Δ Delta")];
  const rows = CBS.filter(r => r.year > 2000).map(r => [
    dataCell(String(r.year), { align: "center" }),
    dataCell(r.helmsman || "-", { align: "center" }),
    dataCell(fmt(r.angular_velocity_deg, 4)),
    dataCell(fmt(r.helmsman_delta, 4))
  ]);

  s.addTable([header, ...rows], tableOpts(1.5, 1.1, 7, [1.0, 2.0, 2.0, 2.0], 8));
})();

// ── SLIDE 10: Key Pairwise Bearings Line Chart ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 2 — STAGE 1 CBS/CNT PLATES");
  addSlideTitle(s, "Key Pairwise Bearings Over Time");

  const pairs = ["Coal-Nuclear", "Gas-Nuclear", "Nuclear-Solar", "Coal-Gas"];
  const colors = ["424242", "FF9800", "FFC107", "795548"];

  const chartData = pairs.map((p, pi) => ({
    name: p,
    labels: YEARS.map(String),
    values: CBS.map(r => +(r.bearings_deg[p] || 0).toFixed(2))
  }));

  s.addChart(pres.charts.LINE, chartData, {
    x: 0.5, y: 1.1, w: 9, h: 4.2,
    chartColors: colors,
    lineSize: 2,
    showLegend: true, legendPos: "b", legendFontSize: 8,
    catAxisLabelColor: "666666", catAxisLabelFontSize: 7,
    valAxisLabelColor: "666666", valAxisLabelFontSize: 7,
    valGridLine: { color: "E8E8E8", size: 0.5 },
    catGridLine: { style: "none" },
    showTitle: false
  });
})();

// ── SLIDE 11: Diagonal Metric Tensor Table ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 2 — STAGE 1 CBS/CNT PLATES");
  s.addText("Diagonal Metric Tensor (κjj) — All Carriers × All Years", {
    x: 0.3, y: 0.45, w: 9.4, h: 0.35, fontSize: 14, fontFace: FONT, color: ACCENT, bold: true
  });

  const header = [headerCell("Year"), ...CARRIERS.map(c => headerCell(c))];
  const rows = CBS.map(r => {
    const yr = dataCell(String(r.year), { align: "center", bold: true });
    const cells = CARRIERS.map(c => dataCell(fmtSci(r.diagonal_metric[c], 1)));
    return [yr, ...cells];
  });

  const colW = [0.55, ...CARRIERS.map(() => 1.05)];
  s.addTable([header, ...rows], {
    ...tableOpts(0.2, 0.85, 9.6, colW, 6),
    fontSize: 6
  });
})();

// ── SLIDE 12: Top 10 Year-Pair Divergences ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 3 — STAGE 2 CROSS-EXAMINATION");
  addSlideTitle(s, "Top 10 Year-Pair Divergences");

  const gp = data.stage2.group_pairwise.slice(0, 10);
  const header = [headerCell("Rank"), headerCell("Year A"), headerCell("Year B"),
    headerCell("Metric Dist."), headerCell("Dominant Carrier"), headerCell("Classification")];
  const rows = gp.map((p, i) => [
    dataCell(String(i + 1), { align: "center" }),
    dataCell(p.group_A, { align: "center" }),
    dataCell(p.group_B, { align: "center" }),
    dataCell(fmt(p.metric_distance, 2)),
    dataCell(p.dominant_contrast_carrier, { align: "center" }),
    dataCell(p.classification, { align: "center", fontSize: 6 })
  ]);

  s.addTable([header, ...rows], tableOpts(0.5, 1.1, 9, [0.6, 1.0, 1.0, 1.4, 2.0, 3.0], 9));
})();

// ── SLIDE 13: Carrier Pair Opposition/Co-Movement Bar Chart ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 3 — STAGE 2 CROSS-EXAMINATION");
  addSlideTitle(s, "Carrier Pair Opposition vs Co-Movement Scores");

  const cp = data.stage2.carrier_pairwise;
  // Sort by opposition desc, then co-movement desc
  const sorted = [...cp].sort((a, b) => (b.opposition_score - a.opposition_score) || (b.co_movement_score - a.co_movement_score));

  const chartData = [
    {
      name: "Opposition",
      labels: sorted.map(p => p.carrier_pair),
      values: sorted.map(p => -p.opposition_score)  // negative for left side
    },
    {
      name: "Co-Movement",
      labels: sorted.map(p => p.carrier_pair),
      values: sorted.map(p => p.co_movement_score)
    }
  ];

  s.addChart(pres.charts.BAR, chartData, {
    x: 0.3, y: 1.1, w: 9.4, h: 4.3,
    barDir: "bar", barGrouping: "stacked",
    chartColors: ["D32F2F", "1565C0"],
    showLegend: true, legendPos: "b", legendFontSize: 8,
    catAxisLabelColor: "666666", catAxisLabelFontSize: 6,
    valAxisLabelColor: "666666", valAxisLabelFontSize: 7,
    valGridLine: { color: "E8E8E8", size: 0.5 },
    catGridLine: { style: "none" },
    showTitle: false
  });
})();

// ── SLIDE 14: Top 10 Carrier Pair Opposition Table ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 3 — STAGE 2 CROSS-EXAMINATION");
  addSlideTitle(s, "Top 10 Carrier Pairs — Full Scores");

  const cp = data.stage2.carrier_pairwise.slice(0, 10);
  const header = [headerCell("Rank"), headerCell("Pair"), headerCell("Opposition"),
    headerCell("Co-Movement"), headerCell("Metric Coupling"), headerCell("Classification")];
  const rows = cp.map((p, i) => [
    dataCell(String(i + 1), { align: "center" }),
    dataCell(p.carrier_pair, { align: "center" }),
    dataCell(fmt(p.opposition_score, 4)),
    dataCell(fmt(p.co_movement_score, 4)),
    dataCell(fmtSci(p.metric_coupling_score, 2)),
    dataCell(p.classification, { align: "center", fontSize: 6 })
  ]);

  s.addTable([header, ...rows], tableOpts(0.3, 1.1, 9.4, [0.5, 2.0, 1.3, 1.3, 2.0, 2.3], 9));
})();

// ── SLIDE 15: Section View Comparison ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 3 — STAGE 2 CROSS-EXAMINATION");
  addSlideTitle(s, "Section View Comparison (XY vs XZ vs YZ)");

  const sp = Object.values(data.stage2.section_pairwise);
  const header = [headerCell("View Pair"), headerCell("Agreement"), headerCell("Divergence"),
    headerCell("Dominant Carrier"), headerCell("Classification")];
  const rows = sp.map(p => [
    dataCell(p.view_pair, { align: "center", bold: true }),
    dataCell(fmt(p.agreement_score, 4)),
    dataCell(fmt(p.divergence_score, 4)),
    dataCell(p.dominant_carrier, { align: "center" }),
    dataCell(p.classification, { align: "center" })
  ]);

  s.addTable([header, ...rows], tableOpts(1.0, 1.3, 8, [1.5, 1.5, 1.5, 1.8, 1.7], 11));

  s.addText("All three section views show strong consistency (agreement > 0.80), confirming isotropy of the metric structure.", {
    x: 1.0, y: 3.4, w: 8, h: 0.5, fontSize: 10, fontFace: FONT, color: "777777", italic: true
  });
})();

// ── SLIDE 16: Top 10 Carrier Triads ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 4 — STAGE 3 HIGHER-DEGREE ANALYSIS");
  addSlideTitle(s, "Top 10 Carrier Triads");

  const ct = data.stage3.carrier_triads.slice(0, 10);
  const header = [headerCell("Rank"), headerCell("Triad"), headerCell("Coupling Score"),
    headerCell("Opposition Score"), headerCell("Classification")];
  const rows = ct.map((t, i) => [
    dataCell(String(i + 1), { align: "center" }),
    dataCell(t.carrier_triad, { align: "center" }),
    dataCell(fmt(t.triadic_coupling_score, 4)),
    dataCell(fmt(t.triadic_opposition_score, 4)),
    dataCell(t.classification, { align: "center", fontSize: 7 })
  ]);

  s.addTable([header, ...rows], tableOpts(0.5, 1.1, 9, [0.6, 2.8, 1.5, 1.5, 2.6], 9));
})();

// ── SLIDE 17: Subcomposition Degree Ladder ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 4 — STAGE 3 HIGHER-DEGREE ANALYSIS");
  addSlideTitle(s, "Subcomposition Degree Ladder (Degree 2)");

  const sub = Object.values(data.stage3.subcomposition).slice(0, 15);
  const header = [headerCell("Rank"), headerCell("Subset"), headerCell("Metric Energy"),
    headerCell("Boundary Pressure"), headerCell("Stability"), headerCell("Classification")];
  const rows = sub.map((e, i) => [
    dataCell(String(i + 1), { align: "center" }),
    dataCell(e.carrier_subset, { align: "center" }),
    dataCell(fmt(e.subset_metric_energy, 2)),
    dataCell(fmtSci(e.subset_boundary_pressure, 1)),
    dataCell(fmtSci(e.subset_stability_score, 4)),
    dataCell(e.classification, { align: "center", fontSize: 6 })
  ]);

  s.addTable([header, ...rows], tableOpts(0.3, 1.1, 9.4, [0.5, 2.2, 1.3, 1.8, 1.3, 2.3], 8));
})();

// ── SLIDE 18: Metric Regime Detection ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 4 — STAGE 3 HIGHER-DEGREE ANALYSIS");
  addSlideTitle(s, "Metric Regime Detection Summary");

  const regimes = data.stage3.regimes;

  // Side by side regime boxes
  regimes.forEach((r, ri) => {
    const xBase = ri === 0 ? 0.5 : 5.2;
    const boxW = 4.3;

    s.addShape(pres.shapes.RECTANGLE, {
      x: xBase, y: 1.3, w: boxW, h: 3.8,
      fill: { color: ri === 0 ? "FFF3E0" : "E8F5E9" },
      line: { color: ri === 0 ? "FF9800" : "4CAF50", width: 1.5 }
    });

    s.addText(r.regime_id + ": " + r.time_window_start.replace("_pt0","") + " – " + r.time_window_end.replace("_pt0",""), {
      x: xBase + 0.2, y: 1.4, w: boxW - 0.4, h: 0.4,
      fontSize: 14, fontFace: FONT, color: ACCENT, bold: true
    });

    const details = [
      { text: "Member Points: " + r.member_points, options: { breakLine: true, fontSize: 11, color: "444444" } },
      { text: "Within-Regime Variance: " + fmt(r.within_regime_metric_variance, 2), options: { breakLine: true, fontSize: 11, color: "444444" } },
      { text: "Between-Regime Distance: " + fmt(r.between_regime_distance, 2), options: { breakLine: true, fontSize: 11, color: "444444" } },
      { text: "Dominant Carriers: " + r.dominant_carriers.replace(/;/g, ", "), options: { breakLine: true, fontSize: 11, color: "444444" } },
      { text: "Classification: " + r.classification, options: { fontSize: 11, color: ri === 0 ? "E65100" : "2E7D32", bold: true } }
    ];

    s.addText(details, {
      x: xBase + 0.3, y: 2.0, w: boxW - 0.6, h: 2.8,
      fontFace: FONT, valign: "top"
    });
  });
})();

// ── SLIDE 19: Regime Comparison Table ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 4 — STAGE 3 HIGHER-DEGREE ANALYSIS");
  addSlideTitle(s, "Regime Comparison — R01 (2000–2013) vs R02 (2015–2025)");

  // Compute mean CLR, mean metric energy, mean Hs per regime
  const r1 = CBS.filter(r => r.year >= 2000 && r.year <= 2013);
  const r2 = CBS.filter(r => r.year >= 2015 && r.year <= 2025);

  function meanArr(arr, fn) { return arr.reduce((s, r) => s + fn(r), 0) / arr.length; }
  function helmFreq(arr) {
    const freq = {};
    arr.forEach(r => { if (r.helmsman) freq[r.helmsman] = (freq[r.helmsman] || 0) + 1; });
    return Object.entries(freq).sort((a, b) => b[1] - a[1]).map(e => e[0] + "(" + e[1] + ")").join(", ");
  }

  const header = [headerCell("Metric"), headerCell("R01 (2000–2013)"), headerCell("R02 (2015–2025)")];
  const rows = [
    [dataCell("Mean Metric Energy", { align: "left", bold: true }),
     dataCell(fmt(meanArr(r1, r => r.metric_energy), 2)),
     dataCell(fmt(meanArr(r2, r => r.metric_energy), 2))],
    [dataCell("Mean Hs", { align: "left", bold: true }),
     dataCell(fmt(meanArr(r1, r => r.hs), 4)),
     dataCell(fmt(meanArr(r2, r => r.hs), 4))],
    [dataCell("Mean Condition Number", { align: "left", bold: true }),
     dataCell(fmt(meanArr(r1, r => r.condition_number), 1)),
     dataCell(fmt(meanArr(r2, r => r.condition_number), 1))],
    [dataCell("Mean ω (deg)", { align: "left", bold: true }),
     dataCell(fmt(meanArr(r1, r => r.angular_velocity_deg), 2)),
     dataCell(fmt(meanArr(r2, r => r.angular_velocity_deg), 2))],
    [dataCell("Dominant Helmsman Freq.", { align: "left", bold: true }),
     dataCell(helmFreq(r1), { fontSize: 7 }),
     dataCell(helmFreq(r2), { fontSize: 7 })],
    [dataCell("Member Points", { align: "left", bold: true }),
     dataCell(String(r1.length)),
     dataCell(String(r2.length))],
    [dataCell("Within-Regime Variance", { align: "left", bold: true }),
     dataCell(fmt(data.stage3.regimes[0].within_regime_metric_variance, 2)),
     dataCell(fmt(data.stage3.regimes[1].within_regime_metric_variance, 2))]
  ];

  // Add mean CLR per carrier
  CARRIERS.forEach((c, ci) => {
    rows.push([
      dataCell("Mean CLR: " + c, { align: "left", fontSize: 7 }),
      dataCell(fmt(meanArr(r1, r => r.clr[ci]), 3), { fontSize: 7 }),
      dataCell(fmt(meanArr(r2, r => r.clr[ci]), 3), { fontSize: 7 })
    ]);
  });

  s.addTable([header, ...rows], tableOpts(0.8, 1.1, 8.4, [3.0, 2.7, 2.7], 9));
})();

// ── SLIDE 20: Key Findings Summary ──
(function() {
  const s = lightSlide();
  addSectionHeader(s, "SECTION 5 — CONCLUSION");
  addSlideTitle(s, "Key Findings — Deterministic Discoveries");

  const findings = [
    { text: "Nuclear dominates all divergence: Every top-20 year-pair divergence has Nuclear as the dominant contrast carrier. The Coal-Nuclear opposition score reaches 0.9990.", options: { bullet: true, breakLine: true, fontSize: 12, color: "333333" } },
    { text: "Fukushima boundary: The 2011 event creates a clear regime boundary. Angular velocity spikes to 19.8° in 2012, the highest recorded. Year 2014 appears in every top-10 divergence pair.", options: { bullet: true, breakLine: true, fontSize: 12, color: "333333" } },
    { text: "Two-regime structure: R01 (2000–2013) shows high within-regime variance (217.4) vs R02 (2015–2025) variance of only 10.4 — a 21× reduction indicating post-Fukushima compositional stabilization.", options: { bullet: true, breakLine: true, fontSize: 12, color: "333333" } },
    { text: "Triadic coupling: Coal-Gas-Nuclear triad has the highest coupling score (0.999). All triads containing Nuclear show non-zero opposition scores.", options: { bullet: true, breakLine: true, fontSize: 12, color: "333333" } },
    { text: "Nuclear-Solar subcomposition: Highest boundary pressure (2.2×10¹³) and lowest stability (0.00012) of all degree-2 subsets, indicating maximum structural tension between these carriers.", options: { bullet: true, fontSize: 12, color: "333333" } }
  ];

  s.addText(findings, {
    x: 0.7, y: 1.2, w: 8.6, h: 4.0,
    fontFace: FONT, valign: "top", paraSpaceAfter: 8
  });
})();

// ── SLIDE 21: Closing ──
(function() {
  const s = darkSlide();
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.08, fill: { color: "9C27B0" } });

  s.addText("The instrument reads.\nThe expert decides.\nThe loop stays open.", {
    x: 1.0, y: 1.5, w: 8, h: 2.0,
    fontSize: 28, fontFace: FONT, color: WHITE, align: "center", italic: true,
    lineSpacingMultiple: 1.5
  });

  s.addShape(pres.shapes.LINE, { x: 3.5, y: 3.7, w: 3, h: 0, line: { color: "9C27B0", width: 2 } });

  s.addText("Higgins Computational Instruments", {
    x: 1.0, y: 4.0, w: 8, h: 0.4,
    fontSize: 14, fontFace: FONT, color: "AAAAAA", align: "center"
  });
  s.addText("CoDaWork 2026  |  Peter Higgins", {
    x: 1.0, y: 4.5, w: 8, h: 0.3,
    fontSize: 11, fontFace: FONT, color: "777777", align: "center"
  });
})();

// ── Write ──
const outPath = path.join(__dirname, "HCI_Japan_CoDaWork2026.pptx");
pres.writeFile({ fileName: outPath }).then(() => {
  console.log("PPTX written to:", outPath);
}).catch(err => {
  console.error("Error:", err);
  process.exit(1);
});
