const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageNumber, PageBreak, TabStopType, TabStopPosition } = require("docx");

const border = { style: BorderStyle.SINGLE, size: 1, color: "999999" };
const borders = { top: border, bottom: border, left: border, right: border };
const hdrBorder = { style: BorderStyle.SINGLE, size: 1, color: "333333" };
const hdrBorders = { top: hdrBorder, bottom: hdrBorder, left: hdrBorder, right: hdrBorder };
const cellM = { top: 60, bottom: 60, left: 100, right: 100 };

function hdrCell(text, w) {
  return new TableCell({
    borders: hdrBorders, width: { size: w, type: WidthType.DXA },
    shading: { fill: "2B2B2B", type: ShadingType.CLEAR },
    margins: cellM,
    children: [new Paragraph({ children: [new TextRun({ text, bold: true, font: "Arial", size: 18, color: "FFFFFF" })] })]
  });
}

function cell(text, w, shade) {
  return new TableCell({
    borders, width: { size: w, type: WidthType.DXA },
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: cellM,
    children: [new Paragraph({ children: [new TextRun({ text, font: "Arial", size: 17 })] })]
  });
}

function cellBold(text, w, shade) {
  return new TableCell({
    borders, width: { size: w, type: WidthType.DXA },
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: cellM,
    children: [new Paragraph({ children: [new TextRun({ text, font: "Arial", size: 17, bold: true })] })]
  });
}

function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
    children: [new TextRun({ text, bold: true, font: "Arial", size: 32 })] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
    children: [new TextRun({ text, bold: true, font: "Arial", size: 26 })] });
}
function h3(text) {
  return new Paragraph({ spacing: { before: 200, after: 120 },
    children: [new TextRun({ text, bold: true, font: "Arial", size: 22 })] });
}
function p(text) {
  return new Paragraph({ spacing: { after: 120 },
    children: [new TextRun({ text, font: "Arial", size: 22 })] });
}
function pItalic(text) {
  return new Paragraph({ spacing: { after: 120 },
    children: [new TextRun({ text, font: "Arial", size: 22, italics: true, color: "555555" })] });
}

const TW = 13680; // landscape content width

// ─── Timeline table ───
const timelineCols = [1200, 1600, 1800, 2200, 2400, 2200, 2280];
const timelineRows = [
  ["ERA", "Date", "Method", "D", "Analysis", "Hs Computed", "Key Flaw"],
  ["1", "Mar 19", "EMBER raw download", "n/a", "Data ingestion only", "No", "No analysis"],
  ["2a", "Mar 19", "HUF 7-Axis (PCA on CLR)", "9", "Sufficiency frontier, TV shock", "No", "No per-sample output"],
  ["2b", "Mar 22", "HUF Deceptive Drift v1-v3", "9", "L2 drift + TV distance", "No", "Summary stats only, no composition trace"],
  ["3", "Mar 30", "CoDaWork Protocol", "9", "Compositions stored, Keff", "No", "Other Renewables = 1e-06 (structural zero)"],
  ["4", "Apr 13", "CoDaWork 2026 results", "9", "Closed compositions", "No", "D=9 includes phantom carrier"],
  ["5", "Apr 29", "Hs-M02 Pipeline (12-step)", "9*", "CLR, PLL, entropy, chaos", "System only", "Year column treated as carrier (bug)"],
  ["6", "Apr 30", "Hs-M02 Projections", "8", "Polar stack, manifold, helix", "Per-year", "Projection from corrected D=8"],
  ["7", "May 1", "CoDaWork Projector + Cinema", "8", "Multi-country comparison", "Per-year", "None (clean run)"],
  ["8", "May 2", "Hs_Direct (full tensor)", "8", "Hs, CLR, metric tensor, Poincare", "Per-year", "Fixed carrier set, pre-bearing"],
  ["9", "May 2", "HCI Stage 1/2/3", "8", "CBS bearings, helmsman, omega", "Per-year", "PptxGenJS dependency for output"],
  ["10", "May 3", "Stage 1 Raw Plates (matplotlib)", "8", "Same engine, Python-only output", "Per-year", "None (standalone)"],
];

function makeTimelineTable() {
  const rows = timelineRows.map((r, ri) => {
    return new TableRow({
      children: r.map((c, ci) => ri === 0 ? hdrCell(c, timelineCols[ci]) : cell(c, timelineCols[ci], ri % 2 === 0 ? "F2F2F2" : undefined))
    });
  });
  return new Table({ width: { size: TW, type: WidthType.DXA }, columnWidths: timelineCols, rows });
}

// ─── Data comparison table ───
const dataCols = [2000, 2000, 1600, 1600, 1600, 1600, 1640, 1640];
const dataRows = [
  ["Method", "Year", "Hs", "Ring", "omega (deg)", "d_A", "kappa", "Helmsman"],
  ["HUF 7-Axis", "2000", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a"],
  ["HUF 7-Axis", "2012", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a"],
  ["Drift v3", "2000", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a"],
  ["Drift v3", "2012", "n/a", "n/a", "n/a", "TV=0.136", "n/a", "n/a"],
  ["Hs-M02 (D=9*)", "2000", "system", "n/a", "n/a", "n/a", "n/a", "n/a"],
  ["Hs_Direct", "2000", "0.234683", "Hs-2", "0.0", "0.0", "2901.09", "---"],
  ["Hs_Direct", "2012", "0.312291", "Hs-3", "27.46", "2.201", "92.07", "Nuclear"],
  ["HCI CBS", "2000", "0.234683", "Hs-2", "0.0", "0.0", "2901.09", "---"],
  ["HCI CBS", "2012", "0.312291", "Hs-3", "27.46", "2.201", "92.07", "Nuclear"],
  ["Stage 1 Plates", "2000", "0.234683", "Hs-2", "0.0", "0.0", "2901.09", "---"],
  ["Stage 1 Plates", "2012", "0.312291", "Hs-3", "27.46", "2.201", "92.07", "Nuclear"],
];

function makeDataTable() {
  const rows = dataRows.map((r, ri) => {
    return new TableRow({
      children: r.map((c, ci) => ri === 0 ? hdrCell(c, dataCols[ci]) : cell(c, dataCols[ci], ri % 2 === 0 ? "F2F2F2" : undefined))
    });
  });
  return new Table({ width: { size: TW, type: WidthType.DXA }, columnWidths: dataCols, rows });
}

// ─── Validity assessment table ───
const valCols = [1800, 1200, 2400, 4200, 4080];
const valRows = [
  ["Method", "Validity", "What It Measured", "Flaws", "Addressed by Stage 1?"],
  ["HUF 7-Axis", "LOW", "Global PCA eigenstructure across countries. Japan = one row in a matrix.", "No per-sample output. D=9 with phantom carrier. No Hs, no composition trace, no per-year data accessible.", "Yes. Stage 1 produces per-year section plates with all tensor channels visible. D=8 (phantom carrier removed)."],
  ["HUF Drift v1-v3", "LOW", "L2 and TV distance between consecutive years. Detected 2012 shock correctly.", "Summary statistics only. No CLR coordinates. No bearings. No metric tensor. No Hs. Cannot identify which carrier caused the shock.", "Yes. Stage 1 identifies Nuclear as helmsman with delta=-2.04, omega=27.46 deg. The cause is visible, not just the effect."],
  ["CoDaWork Protocol", "MEDIUM", "Correctly closed compositions for 7 countries. Stored raw data.", "D=9 includes Other Renewables = 1e-06 (structural zero). No analysis beyond storage. Compositions correct but carrier set wrong.", "Yes. D=8 with Other Renewables excluded. Same underlying data, correct carrier set."],
  ["Hs-M02 Pipeline", "MEDIUM", "Full 12-step Hs pipeline. CLR, PLL shape, entropy, chaos detection.", "Year column accidentally included as carrier (D=9 with Year bug). System-level statistics, not per-year Hs. Projections ran on corrected D=8 but pipeline diagnostics contaminated.", "Partially. Stage 1 uses correct D=8 from the start. Per-year Hs is now the primary output, not a system summary."],
  ["Hs_Direct", "HIGH", "Full Higgins Coordinate tensor: Hs, CLR, metric tensor diagonal, Poincare disc, circularity. Per-year output.", "No bearings. No angular velocity between years. No helmsman. No steering sensitivity per carrier. Tensor output limited to diagonal.", "Yes. Stage 1 adds all D(D-1)/2=28 pairwise bearings, omega, helmsman, full steering sensitivity. The tensor is now fully displayed."],
  ["HCI CBS", "HIGH", "Full CBS oscilloscope: Hs, CLR, bearings, omega, helmsman, steering sensitivity, metric tensor, lock detection.", "Output format required PptxGenJS (Node.js). Not standalone Python. AI-formatted slides, not raw data display.", "Yes. Stage 1 Plates (matplotlib) is pure Python, produces raw PDF output. No Node.js, no AI formatting. Field-deployable."],
  ["Stage 1 Plates", "HIGHEST", "All CBS tensor channels in raw matplotlib display. 3 orthogonal faces per year. All carriers, all pairs.", "Current version. No known data flaws. Output is raw and uninterpreted as specified.", "This IS the current method."],
];

function makeValTable() {
  const rows = valRows.map((r, ri) => {
    return new TableRow({
      children: r.map((c, ci) => {
        if (ri === 0) return hdrCell(c, valCols[ci]);
        if (ci === 1) {
          const color = c === "HIGHEST" ? "1B5E20" : c === "HIGH" ? "2E7D32" : c === "MEDIUM" ? "E65100" : "B71C1C";
          return new TableCell({
            borders, width: { size: valCols[ci], type: WidthType.DXA },
            margins: cellM,
            children: [new Paragraph({ children: [new TextRun({ text: c, font: "Arial", size: 17, bold: true, color })] })]
          });
        }
        return cell(c, valCols[ci], ri % 2 === 0 ? "F2F2F2" : undefined);
      })
    });
  });
  return new Table({ width: { size: TW, type: WidthType.DXA }, columnWidths: valCols, rows });
}

// ─── CLR comparison table ───
const clrCols = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1680];
const carriers = ["Bio", "Coal", "Gas", "Hydro", "Nuclear", "OFos", "Solar", "Wind"];
const clr2000 = ["-0.462", "2.232", "2.313", "1.195", "2.524", "1.967", "-4.320", "-5.449"];
const clr2012 = ["-0.792", "1.924", "2.188", "0.457", "-0.999", "1.448", "-1.891", "-2.335"];

function makeCLRTable() {
  const rows = [
    new TableRow({ children: [hdrCell("Year", clrCols[0]), ...carriers.map((c, i) => hdrCell(c, clrCols[i+1]))] }),
    new TableRow({ children: [cellBold("2000", clrCols[0]), ...clr2000.map((v, i) => cell(v, clrCols[i+1]))] }),
    new TableRow({ children: [cellBold("2012", clrCols[0], "F2F2F2"), ...clr2012.map((v, i) => cell(v, clrCols[i+1], "F2F2F2"))] }),
  ];
  return new Table({ width: { size: TW, type: WidthType.DXA }, columnWidths: clrCols, rows });
}

// ─── Build document ───
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840, orientation: "landscape" },
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
      }
    },
    headers: {
      default: new Header({ children: [
        new Paragraph({
          children: [
            new TextRun({ text: "EMBER Japan Energy Analysis — Project Evolution & Data Validity Assessment", font: "Arial", size: 16, color: "888888" }),
            new TextRun({ text: "\tHCI Stage 1 Plates", font: "Arial", size: 16, color: "888888" }),
          ],
          tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        })
      ] })
    },
    footers: {
      default: new Footer({ children: [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", font: "Arial", size: 16, color: "888888" }),
            new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 16, color: "888888" }),
          ]
        })
      ] })
    },
    children: [
      // ── TITLE ──
      new Paragraph({ spacing: { after: 80 }, children: [
        new TextRun({ text: "EMBER Japan Energy Analysis", font: "Arial", size: 44, bold: true })
      ] }),
      new Paragraph({ spacing: { after: 200 }, children: [
        new TextRun({ text: "Project Evolution and Data Validity Assessment", font: "Arial", size: 32, color: "555555" })
      ] }),
      p("Dataset: Japan electricity generation (TWh), 2000-2025, EMBER Global Electricity Review"),
      p("Carriers: 8 (Bioenergy, Coal, Gas, Hydro, Nuclear, Other Fossil, Solar, Wind)"),
      p("Assessment date: 3 May 2026"),
      pItalic("This document traces the complete analytical history of Japan EMBER energy data through every method applied across the HUF and Hs projects. It compares numerical outputs, identifies where and why data changed, and assesses the validity of each method."),

      new Paragraph({ children: [new PageBreak()] }),

      // ── 1. DEVELOPMENT TIMELINE ──
      h1("1. Development Timeline"),
      p("The table below shows every analytical method applied to EMBER Japan data in chronological order. The project evolved from global summary statistics (ERA 1-2) through compositional storage (ERA 3-4) to full per-year tensor analysis (ERA 6-10)."),
      new Paragraph({ spacing: { after: 120 } }),
      makeTimelineTable(),
      new Paragraph({ spacing: { after: 120 } }),
      pItalic("* ERA 5 (Hs-M02) accidentally included the Year column as a 9th carrier. This was identified and corrected in ERA 6 onwards."),

      new Paragraph({ children: [new PageBreak()] }),

      // ── 2. WHAT CHANGED AND WHY ──
      h1("2. What Changed and Why"),

      h2("2.1 Carrier Set: D=9 to D=8"),
      p("The original EMBER data contains 9 generation categories. For Japan, the \"Other Renewables\" category contains effectively zero generation across all 26 years (replaced by 1e-06 floor). This creates a structural zero — a carrier that never carries information. Including it inflates the dimensionality without adding signal. The transition to D=8 (excluding Other Renewables) occurred between ERA 4 and ERA 6. All analyses from Hs_Direct onwards use D=8."),
      p("Impact: Hs values are affected by D because H_max = ln(D). With D=9, H_max = ln(9) = 2.197. With D=8, H_max = ln(8) = 2.079. The same entropy H gives a different Hs. However, since the phantom carrier contributes near-zero entropy, the practical difference is small but the mathematical cleanliness is significant."),

      h2("2.2 The Year-as-Carrier Bug (ERA 5)"),
      p("In the Hs-M02 pipeline run, the CSV reader treated the Year column as a carrier, making D=9 with Year as a \"component.\" This produced CLR values where the Year dimension dominated (CLR mean = 6.725 for Year vs -1 to +2 for actual carriers). The 12-step pipeline diagnostics (sigma2, PLL shape, chaos detection) were all computed on this contaminated 9-dimensional space. The projections (polar stack, manifold, helix) were subsequently re-run with corrected D=8 data, but the pipeline diagnostic numbers in the results JSON remain from the buggy run."),
      p("Impact: Pipeline diagnostics for Hs-M02 are unreliable. The projection outputs are correct because they were regenerated. All analyses from ERA 8 onwards start from scratch with verified D=8."),

      h2("2.3 From Summary Statistics to Per-Year Output"),
      p("ERA 2 (HUF) produced only system-level statistics: TV distance = 0.136 for 2012, L2 drift = 0.152 for 2012. These correctly detected the Fukushima shock but could not identify which carrier caused it or how the composition restructured. ERA 8 (Hs_Direct) was the first method to produce per-year Hs, CLR, and metric tensor values. ERA 9 (HCI CBS) added bearings, angular velocity, helmsman identification, and lock detection. ERA 10 (Stage 1 Plates) displays all of this as raw matplotlib output."),

      h2("2.4 From AI-Formatted to Field-Deployable"),
      p("ERA 9 produced PPTX via PptxGenJS (requires Node.js). ERA 10 produces PDF via matplotlib (requires only Python). This is not a data change but an output independence change. The same JSON drives both. The Stage 1 Plates program can run on any laptop with Python and matplotlib — no internet, no AI, no Node.js."),

      new Paragraph({ children: [new PageBreak()] }),

      // ── 3. NUMERICAL COMPARISON ──
      h1("3. Numerical Comparison — Japan Year 2000 and 2012"),
      p("The table below compares actual numerical outputs across methods for two reference years: 2000 (baseline) and 2012 (Fukushima transition, the largest structural event in the dataset)."),
      new Paragraph({ spacing: { after: 120 } }),
      makeDataTable(),
      new Paragraph({ spacing: { after: 200 } }),
      p("Key finding: All methods that compute Hs on D=8 produce identical values (0.234683 for 2000, 0.312291 for 2012). The underlying composition data has never changed — only the analysis depth and carrier set have evolved. The CNT engine is deterministic: same input, same output, no parameters."),

      h2("3.1 CLR Coordinates (Identical Across ERA 8-10)"),
      p("The CLR transform h = clr(x) is computed identically across Hs_Direct, HCI CBS, and Stage 1 Plates:"),
      new Paragraph({ spacing: { after: 120 } }),
      makeCLRTable(),
      new Paragraph({ spacing: { after: 120 } }),
      p("The 2012 values show Nuclear CLR dropping from +2.524 to -0.999 (a shift of 3.52 in log-ratio space), which is the quantitative Fukushima signal. Solar and Wind CLR values rise (becoming less negative), reflecting their increased share post-shutdown."),

      new Paragraph({ children: [new PageBreak()] }),

      // ── 4. VALIDITY ASSESSMENT ──
      h1("4. Data Validity Assessment by Method"),
      p("Each method is rated for validity based on: correctness of carrier set, completeness of tensor output, reproducibility without AI, and whether per-year data is accessible."),
      new Paragraph({ spacing: { after: 120 } }),
      makeValTable(),

      new Paragraph({ children: [new PageBreak()] }),

      // ── 5. DOES THE NEW OUTPUT MAKE SENSE? ──
      h1("5. Does the New Output Make More Sense?"),

      h2("5.1 What Early Methods Could See"),
      p("ERA 2 (HUF Drift) detected that 2012 was anomalous: TV distance = 0.136, well above the p90 threshold of 0.074. But it could not say why. It measured the size of the shock without identifying the source. This is equivalent to an oscilloscope showing a voltage spike without labeling which channel produced it."),

      h2("5.2 What Stage 1 Plates Show"),
      p("The Stage 1 section plate for t=12 (Year 2012) shows all three faces simultaneously. The YZ bar shows Nuclear CLR dropping from +2.52 to -1.00. The XZ bar shows all 28 bearing pairs restructuring — the Bioenergy-Hydro bearing jumps to +150 degrees while Coal-Nuclear drops to -27 degrees. The plate info field reports omega = 27.46 degrees (total angular velocity in 8-dimensional CLR space) and helmsman = Nuclear with delta = -2.04."),
      p("This is not a different answer from ERA 2 — it is the same answer with full resolution. ERA 2 said \"something big happened in 2012.\" Stage 1 says \"Nuclear CLR displaced by -3.52 units in log-ratio space, rotating the full compositional vector by 27.46 degrees, with Gas absorbing the largest replacement share (CLR from 2.31 to 2.19 while composition fraction rose from 0.235 to 0.393).\""),

      h2("5.3 What Stage 1 Adds That No Previous Method Had"),
      p("Bearings: 28 pairwise angular measurements per year. These show structural relationships between carrier pairs — Coal-Gas lock (bearing spread = 8.4 degrees across all years) was invisible to every previous method. Angular velocity: the total heading change between consecutive years, measured in degrees. This is a single scalar that captures the magnitude of compositional restructuring regardless of which carriers moved. Helmsman: the carrier responsible for the largest CLR displacement at each timestep. This is the cause, not just the effect. Steering sensitivity: the metric tensor diagonal shows that Wind (sensitivity = 9997.0) has 2900x the steering authority of Nuclear (sensitivity = 3.45) in 2000. Any movement in Wind, however small, produces enormous compositional rotation."),

      h2("5.4 Consistency Verdict"),
      p("The data is consistent across all methods. No method produced contradictory results. Each subsequent method revealed more structure in the same underlying data. The Hs values, CLR coordinates, and composition fractions are identical wherever they overlap. The project evolution is one of increasing resolution on a fixed dataset, not changing answers."),

      new Paragraph({ children: [new PageBreak()] }),

      // ── 6. CONCLUSION ──
      h1("6. Conclusion"),
      p("The EMBER Japan energy analysis has evolved through 10 distinct eras over 45 days (19 March to 3 May 2026). The underlying data has never changed. What changed is the depth of analysis applied to it:"),
      new Paragraph({ spacing: { after: 80 } }),
      p("ERA 1-4: Data ingestion and storage. No per-year Hs. D=9 with phantom carrier."),
      p("ERA 5: Pipeline run with Year-as-carrier bug. System-level diagnostics contaminated."),
      p("ERA 6-7: Corrected D=8. First per-year projections. Manifold and polar stack output."),
      p("ERA 8: Full Higgins Coordinate tensor per year. Hs, CLR, metric, Poincare disc."),
      p("ERA 9: Full CBS oscilloscope. Bearings, helmsman, angular velocity, lock detection."),
      p("ERA 10: Standalone Python output. Same data, field-deployable format."),
      new Paragraph({ spacing: { after: 120 } }),
      p("The Stage 1 Plates method (ERA 10) addresses every flaw identified in earlier methods: correct carrier set (D=8), full tensor output (28 bearings + omega + helmsman + kappa), per-year section plates (not system summaries), and standalone Python generation (no AI, no Node.js). The data validity is the highest of any method because it displays the complete raw tensor output without interpretation, letting the expert examine every channel at every timestep."),
      new Paragraph({ spacing: { after: 200 } }),
      pItalic("The instrument reads. The expert decides. The loop stays open."),
    ]
  }]
});

const outPath = process.argv[2] || "EMBER_Analysis_Evolution.docx";
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outPath, buf);
  console.log("Written: " + outPath);
});
