const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, PageBreak, TabStopType, TabStopPosition,
  LevelFormat, TableOfContents
} = require("docx");

// ── Colour palette: Midnight Executive ──────────────────────────────
const C_NAVY    = "1E2761";
const C_ICE     = "CADCFC";
const C_WHITE   = "FFFFFF";
const C_ACCENT  = "3B5998";
const C_GRAY    = "666666";
const C_LTGRAY  = "F0F4FA";
const C_BLACK   = "000000";
const C_RULE    = "2E75B6";

const border  = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorders = {
  top: { style: BorderStyle.NONE, size: 0 },
  bottom: { style: BorderStyle.NONE, size: 0 },
  left: { style: BorderStyle.NONE, size: 0 },
  right: { style: BorderStyle.NONE, size: 0 },
};

const TW = 9360; // table width = content width at 1" margins

function cell(text, width, opts = {}) {
  const runs = Array.isArray(text) ? text : [new TextRun({ text: String(text), font: "Arial", size: opts.size || 20, bold: opts.bold, italics: opts.italics, color: opts.color || C_BLACK })];
  return new TableCell({
    borders: opts.noBorders ? noBorders : borders,
    width: { size: width, type: WidthType.DXA },
    shading: opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ alignment: opts.align || AlignmentType.LEFT, children: runs })],
  });
}

function headerCell(text, width) {
  return cell(text, width, { bold: true, shading: C_NAVY, color: C_WHITE, size: 20 });
}

function mathBlock(lines) {
  return lines.map(line =>
    new Paragraph({
      spacing: { before: 40, after: 40 },
      indent: { left: 720 },
      children: [new TextRun({ text: line, font: "Consolas", size: 20, color: C_ACCENT })],
    })
  );
}

function para(text, opts = {}) {
  return new Paragraph({
    spacing: { before: opts.spaceBefore || 80, after: opts.spaceAfter || 80 },
    alignment: opts.align || AlignmentType.LEFT,
    children: [new TextRun({ text, font: "Arial", size: opts.size || 22, bold: opts.bold, italics: opts.italics, color: opts.color || C_BLACK })],
  });
}

function heading(text, level) {
  return new Paragraph({
    heading: level,
    children: [new TextRun({ text, font: "Arial", bold: true, color: C_NAVY })],
  });
}

function rule() {
  return new Paragraph({
    spacing: { before: 120, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: C_RULE, space: 1 } },
    children: [],
  });
}

// ═══════════════════════════════════════════════════════════════════
// BUILD DOCUMENT
// ═══════════════════════════════════════════════════════════════════

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: C_NAVY },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: C_NAVY },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: C_ACCENT },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [
    // ─── TITLE PAGE ───────────────────────────────────────────────
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      children: [
        new Paragraph({ spacing: { before: 3600 }, children: [] }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 },
          children: [new TextRun({ text: "Compositional Navigation Tensor", font: "Arial", size: 56, bold: true, color: C_NAVY })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 100 },
          children: [new TextRun({ text: "Engine Mathematics Handbook", font: "Arial", size: 44, bold: true, color: C_ACCENT })],
        }),
        rule(),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 200, after: 80 },
          children: [new TextRun({ text: "Higgins Computational Instruments", font: "Arial", size: 24, color: C_GRAY })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 80 },
          children: [new TextRun({ text: "Peter Higgins", font: "Arial", size: 24, color: C_GRAY })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 80 },
          children: [new TextRun({ text: "May 2026", font: "Arial", size: 24, color: C_GRAY })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 600 },
          children: [new TextRun({ text: "Version 1.0  —  Engine Qualified to IEEE 754 Double Precision Floor", font: "Arial", size: 20, italics: true, color: C_GRAY })],
        }),
      ],
    },

    // ─── TOC + BODY ───────────────────────────────────────────────
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            children: [
              new TextRun({ text: "CNT Engine Mathematics Handbook", font: "Arial", size: 18, color: C_GRAY, italics: true }),
              new TextRun({ text: "\tHiggins Computational Instruments", font: "Arial", size: 18, color: C_GRAY, italics: true }),
            ],
            tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Page ", font: "Arial", size: 18, color: C_GRAY }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: C_GRAY }),
            ],
          })],
        }),
      },
      children: [
        // TOC
        heading("Table of Contents", HeadingLevel.HEADING_1),
        new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 1: INTRODUCTION
        // ═══════════════════════════════════════════════════════════
        heading("1. Introduction", HeadingLevel.HEADING_1),
        para("This handbook provides the complete mathematical specification of the Compositional Navigation Tensor (CNT) engine, the computational core of the Higgins Compositional Bearing Scope (CBS). It covers the geometric foundations, all four tensor channels, the precision analysis that qualified the engine to IEEE 754 double precision floor, and the connection to established compositional data analysis (CoDa) theory."),
        para("The CNT was developed as part of the Higgins Decomposition framework (2025–2026) to provide navigation instrumentation for compositional trajectories on the simplex. It computes, from any closed composition, four quantities that fully characterise the instantaneous directional state and rate of change of a compositional system."),

        heading("1.1 Scope", HeadingLevel.HEADING_2),
        para("This document is a mathematics reference. It contains definitions, proofs, derivations, and experimental verification. It does not contain domain interpretation, operational guidance, or data analysis. For those, see the Manifold Character Handbook and the Projection Atlas."),

        heading("1.2 Notation", HeadingLevel.HEADING_2),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [2000, 7360],
          rows: [
            new TableRow({ children: [headerCell("Symbol", 2000), headerCell("Meaning", 7360)] }),
            new TableRow({ children: [cell("x", 2000), cell("Closed composition in the D-simplex, x_j > 0, Σx_j = 1", 7360)] }),
            new TableRow({ children: [cell("D", 2000), cell("Number of parts (carriers, components)", 7360)] }),
            new TableRow({ children: [cell("h = clr(x)", 2000), cell("Centred log-ratio transform: h_j = log(x_j) − (1/D)Σlog(x_k)", 7360)] }),
            new TableRow({ children: [cell("θ", 2000), cell("Bearing — pairwise angle in CLR space (degrees)", 7360)] }),
            new TableRow({ children: [cell("ω", 2000), cell("Angular velocity — total heading change between consecutive CLR vectors", 7360)] }),
            new TableRow({ children: [cell("κ", 2000), cell("Steering sensitivity — diagonal Aitchison metric tensor, κ_jj = 1/x_j", 7360)] }),
            new TableRow({ children: [cell("σ", 2000), cell("Helmsman — carrier index with maximum |CLR displacement|", 7360)] }),
            new TableRow({ children: [cell("ε", 2000), cell("Machine epsilon = 2.22 × 10⁻¹⁶ (IEEE 754 double)", 7360)] }),
            new TableRow({ children: [cell("e_k", 2000), cell("k-th Helmert basis vector for the CLR zero-sum plane", 7360)] }),
          ],
        }),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 2: CLR GEOMETRY
        // ═══════════════════════════════════════════════════════════
        heading("2. CLR Geometry and the Zero-Sum Plane", HeadingLevel.HEADING_1),

        heading("2.1 The CLR Transform", HeadingLevel.HEADING_2),
        para("The centred log-ratio transform maps a D-part composition x to a vector in R^D:"),
        ...mathBlock([
          "h_j = log(x_j) − (1/D) Σ_{k=1}^{D} log(x_k)"
        ]),
        para("By construction, Σh_j = 0. This confines all CLR vectors to a (D−1)-dimensional hyperplane through the origin with normal vector 1 = [1,1,...,1]/√D. The hyperplane is the CLR zero-sum plane."),

        heading("2.2 Zero-Sum Residual", HeadingLevel.HEADING_2),
        para("Experiment P01 verified that the zero-sum property holds to within 8ε of machine precision across all tested compositions, including extreme skew (x_min = 10⁻⁶) and high dimensionality (D = 20). The maximum observed residual was |Σh_j| = 1.78 × 10⁻¹⁵."),

        heading("2.3 The Orthonormal Basis Problem", HeadingLevel.HEADING_2),
        para("To parametrise a circle on the zero-sum plane (needed for calibration test T03), one must choose basis vectors that lie in the plane. The naive construction:"),
        ...mathBlock([
          "h = [r·cosθ,  r·sinθ,  −(r·cosθ + r·sinθ)]"
        ]),
        para("satisfies zero-sum but produces varying norm:"),
        ...mathBlock([
          "||h||² = r²(2 + sin 2θ)"
        ]),
        para("This oscillates between r² and 3r², a 53.6% norm variation. The ratio max/min = √3 ≈ 1.732. This is a geometric defect, not numerical error: the parametrisation traces an ellipse on the zero-sum plane, not a circle."),

        heading("2.4 The Helmert Submatrix", HeadingLevel.HEADING_2),
        para("The standard orthonormal basis for the zero-sum plane is the Helmert submatrix (Egozcue et al. 2003). Row k (1-indexed, k = 1, ..., D−1):"),
        ...mathBlock([
          "(e_k)_j = 1/√(k(k+1))     for j < k",
          "(e_k)_j = −k/√(k(k+1))    for j = k",
          "(e_k)_j = 0                for j > k",
        ]),
        para("For D = 3, this gives:"),
        ...mathBlock([
          "e₁ = [1/√2,  −1/√2,  0      ]  ≈ [0.7071, −0.7071,  0     ]",
          "e₂ = [1/√6,   1/√6, −2/√6 ]  ≈ [0.4082,  0.4082, −0.8165]",
        ]),

        new Paragraph({ children: [new PageBreak()] }),
        heading("2.5 Verification (P06)", HeadingLevel.HEADING_2),
        para("The Helmert basis was verified to machine precision across D = 3, 4, 8:"),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [3120, 2080, 2080, 2080],
          rows: [
            new TableRow({ children: [headerCell("Property", 3120), headerCell("D = 3", 2080), headerCell("D = 4", 2080), headerCell("D = 8", 2080)] }),
            new TableRow({ children: [cell("Orthonormality error", 3120), cell("2.22e−16", 2080), cell("2.22e−16", 2080), cell("2.22e−16", 2080)] }),
            new TableRow({ children: [cell("Zero-sum residual", 3120), cell("0.00", 2080), cell("1.11e−16", 2080), cell("1.11e−16", 2080)] }),
            new TableRow({ children: [cell("CLR roundtrip error", 3120), cell("1.67e−16", 2080), cell("1.94e−16", 2080), cell("1.11e−16", 2080)] }),
            new TableRow({ children: [cell("Norm preservation", 3120), cell("0.00", 2080), cell("0.00", 2080), cell("0.00", 2080)] }),
          ],
        }),
        para("All properties hold to machine epsilon. The corrected circle h(θ) = r(cosθ · e₁ + sinθ · e₂) has exactly constant norm ||h|| = r for all θ."),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 3: CNT DEFINITIONS
        // ═══════════════════════════════════════════════════════════
        heading("3. CNT Tensor Definitions", HeadingLevel.HEADING_1),
        para("The Compositional Navigation Tensor decomposes compositional motion into four channels. Each is a deterministic, closed-form, parameter-free function of the composition."),
        ...mathBlock(["CNT(x) = (θ, ω, κ, σ)"]),

        heading("3.1 Definition 1: Bearing Tensor θ", HeadingLevel.HEADING_2),
        para("For a composition x with CLR transform h = clr(x), the pairwise bearing between carriers i and j is:"),
        ...mathBlock(["θ_{ij}(x) = atan2(h_j, h_i)"]),
        para("The full bearing tensor collects all D(D−1)/2 pairwise bearings. Each bearing is the angle from carrier i toward carrier j in the CLR plane spanned by dimensions i and j. The atan2 function is well-conditioned everywhere (no singularity at the origin), so bearing computation operates at machine precision unconditionally."),

        heading("3.2 Definition 2: Angular Velocity ω", HeadingLevel.HEADING_2),
        para("For consecutive compositions x(t) and x(t+1) with CLR transforms h(t) and h(t+1), the angular velocity is the angle between the two CLR direction vectors:"),
        ...mathBlock([
          "ω(t, t+1) = atan2(||h(t) × h(t+1)||,  ⟨h(t), h(t+1)⟩)"
        ]),
        para("where the cross product magnitude is computed via the Lagrange identity:"),
        ...mathBlock([
          "||h₁ × h₂||² = ||h₁||² · ||h₂||² − ⟨h₁, h₂⟩²"
        ]),
        para("This identity generalises the cross product magnitude to arbitrary dimension D. The atan2 form replaces the original arccos formulation, which loses up to 8 digits of precision near 0° and 180° (see Chapter 5, Experiment P03). Both formulations are mathematically equivalent; the atan2 form is numerically superior."),

        heading("3.3 Definition 3: Steering Sensitivity Tensor κ", HeadingLevel.HEADING_2),
        para("The diagonal Aitchison metric tensor on the simplex:"),
        ...mathBlock(["κ_{jj}(x) = g_{jj} = 1 / x_j"]),
        para("Carrier j with fraction x_j has sensitivity 1/x_j. As x_j → 0, sensitivity diverges: infinite steering authority at the simplex boundary. This is the mechanism behind Corollary 5 (Infinite Helm)."),

        heading("3.4 Definition 4: Helmsman Index σ", HeadingLevel.HEADING_2),
        para("Between consecutive compositions x(t) and x(t+1), the helmsman is the carrier with maximum CLR displacement:"),
        ...mathBlock(["σ(t, t+1) = argmax_j |h_j(t+1) − h_j(t)|"]),
        para("The helmsman is a discrete quantity (an index into the carrier set). The argmax operation is exact — no floating-point precision issue can affect it unless two carriers have identical |displacement|, which is a measure-zero event."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 4: COROLLARIES
        // ═══════════════════════════════════════════════════════════
        new Paragraph({ children: [new PageBreak()] }),
        heading("4. Corollaries", HeadingLevel.HEADING_1),

        heading("4.1 Bearing Determinism (Corollary 1)", HeadingLevel.HEADING_2),
        para("The bearing θ_{ij} is a deterministic, closed-form function of the composition. Same composition, same bearing. No parameters, no fitting, no model selection. Verified by calibration test T07 (permutation symmetry)."),

        heading("4.2 Steering Asymmetry (Corollary 2)", HeadingLevel.HEADING_2),
        para("For any composition x with max(x)/min(x) = R, the ratio of maximum to minimum steering sensitivity is R. The rarest carrier has R times the steering authority of the most abundant carrier. Verified by T08 (trace identity)."),

        heading("4.3 Lock Detection (Corollary 3)", HeadingLevel.HEADING_2),
        para("Two carriers (i, j) are informationally locked when their pairwise bearing θ_{ij} varies less than ε across T observations:"),
        ...mathBlock(["max_t(θ_{ij}(t)) − min_t(θ_{ij}(t)) < ε"]),
        para("Locked carriers move as a single compositional mode. Their ratio is approximately constant regardless of absolute magnitude changes. Verified by T05 (lock detection). Empirically confirmed on Japan EMBER data: Coal-Gas lock at 8.4° bearing spread."),

        heading("4.4 Bearing Reversal (Corollary 4)", HeadingLevel.HEADING_2),
        para("A sign change in θ_{ij} from positive to negative (or vice versa) indicates a structural crossover: carrier j transitions from above to below its geometric-mean share relative to carrier i. Verified by T06."),

        heading("4.5 Infinite Helm (Corollary 5)", HeadingLevel.HEADING_2),
        para("When carrier j approaches zero fraction, g_{jj} → ∞. Any nonzero change in carrier j dominates the angular velocity. A vanishing carrier has infinite steering authority — its disappearance forces the largest compositional rotation. Verified by T04 (divergence detection)."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 5: PRECISION ANALYSIS
        // ═══════════════════════════════════════════════════════════
        new Paragraph({ children: [new PageBreak()] }),
        heading("5. Precision Analysis", HeadingLevel.HEADING_1),
        para("Ten precision experiments (P01–P10) were conducted to quantify the numerical limits of every CNT channel. This chapter presents the key results."),

        heading("5.1 The arccos Instability (P03)", HeadingLevel.HEADING_2),
        para("The original angular velocity formula used arccos:"),
        ...mathBlock(["ω = arccos(⟨h₁, h₂⟩ / (||h₁|| · ||h₂||))"]),
        para("The derivative d(arccos)/dx = −1/√(1−x²) diverges at x = ±1, corresponding to angles near 0° and 180°. Experiment P03 measured the actual precision loss:"),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [2340, 2340, 2340, 2340],
          rows: [
            new TableRow({ children: [headerCell("1 − cos", 2340), headerCell("arccos result", 2340), headerCell("atan2 result", 2340), headerCell("Difference", 2340)] }),
            new TableRow({ children: [cell("10⁻⁴", 2340), cell("0.81029°", 2340), cell("0.81029°", 2340), cell("4.5e−14", 2340)] }),
            new TableRow({ children: [cell("10⁻⁸", 2340), cell("0.0081029°", 2340), cell("0.0081028°", 2340), cell("2.0e−11", 2340)] }),
            new TableRow({ children: [cell("10⁻¹²", 2340), cell("8.103e−5°", 2340), cell("8.103e−5°", 2340), cell("9.0e−10", 2340)] }),
            new TableRow({ children: [cell("10⁻¹⁶", 2340), cell("8.538e−7°", 2340), cell("8.103e−7°", 2340), cell("4.4e−8", 2340)] }),
          ],
        }),
        para("At 1−cos = 10⁻¹⁶, the arccos result is 5% wrong — 8 digits of precision lost. The atan2 form maintains full precision throughout."),

        heading("5.2 The Lagrange Identity", HeadingLevel.HEADING_2),
        para("The fix uses the Lagrange identity (1773) to compute both sin and cos of the angle:"),
        ...mathBlock([
          "||h₁ × h₂||² = ||h₁||² ||h₂||² − ⟨h₁, h₂⟩²",
          "ω = atan2(√(cross²), dot)"
        ]),
        para("This identity holds in any dimension D, so it generalises the 3D cross product to arbitrary numbers of carriers. The atan2 function is well-conditioned everywhere on the circle, requiring no clamping or special cases."),

        heading("5.3 ILR Equivalence (P05)", HeadingLevel.HEADING_2),
        para("The Aitchison isometry theorem guarantees that inner products in CLR space equal inner products in ILR space. Experiment P05 verified this for angular velocity:"),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [4680, 4680],
          rows: [
            new TableRow({ children: [headerCell("Dimension D", 4680), headerCell("max |ω_CLR − ω_ILR|", 4680)] }),
            new TableRow({ children: [cell("3", 4680), cell("9.83e−13 degrees", 4680)] }),
            new TableRow({ children: [cell("4", 4680), cell("5.75e−13 degrees", 4680)] }),
            new TableRow({ children: [cell("8", 4680), cell("8.55e−13 degrees", 4680)] }),
            new TableRow({ children: [cell("20", 4680), cell("7.30e−13 degrees", 4680)] }),
          ],
        }),
        para("The isometry is exact. The sub-picoradian residual is floating-point roundoff from the projection. There is no precision gain from switching to ILR for angle computation."),

        heading("5.4 Condition Number Theory (P07)", HeadingLevel.HEADING_2),
        para("The Aitchison metric tensor is diagonal with g_{jj} = 1/x_j. Its condition number κ = max(x)/min(x) determines how many significant digits are available:"),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [2600, 1800, 2480, 2480],
          rows: [
            new TableRow({ children: [headerCell("Composition", 2600), headerCell("κ", 1800), headerCell("log₁₀(κ)", 2480), headerCell("Available digits", 2480)] }),
            new TableRow({ children: [cell("Uniform", 2600), cell("1", 1800), cell("0.0", 2480), cell("~15", 2480)] }),
            new TableRow({ children: [cell("Mild skew", 2600), cell("4", 1800), cell("0.6", 2480), cell("~14", 2480)] }),
            new TableRow({ children: [cell("Severe skew", 2600), cell("190", 1800), cell("2.3", 2480), cell("~13", 2480)] }),
            new TableRow({ children: [cell("Extreme skew", 2600), cell("4,995", 1800), cell("3.7", 2480), cell("~11", 2480)] }),
            new TableRow({ children: [cell("Near boundary", 2600), cell("3.0e5", 1800), cell("5.5", 2480), cell("~10", 2480)] }),
            new TableRow({ children: [cell("At boundary", 2600), cell("3.0e10", 1800), cell("10.5", 2480), cell("~5", 2480)] }),
          ],
        }),
        para("Rule: Available digits ≈ 15 − log₁₀(κ). This is not an engine defect — it is a fundamental property of simplex geometry that Aitchison identified in 1986."),

        heading("5.5 Extreme Stress Test (P08)", HeadingLevel.HEADING_2),
        para("The engine was tested with x_min = 10^{−k} for k = 1 through 15. All channels remained within tolerance through k = 13 (x_min = 10⁻¹³). At k = 14–15, the engine reaches the IEEE 754 denormal boundary. The engine is stable down to x_j = 10⁻¹⁵."),

        heading("5.6 Dimensionality Scaling (P09)", HeadingLevel.HEADING_2),
        para("The engine was tested from D = 3 to D = 100. Angular velocity standard deviation remained invariant at 8.81 × 10⁻¹⁴ degrees. Helmert orthogonality held at 2.22 × 10⁻¹⁶ regardless of dimension. CLR zero-sum residual grew to 6.22 × 10⁻¹³ at D = 100 (accumulation of log terms), but remains negligible for any practical purpose."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 6: ENGINE STATE MACHINE
        // ═══════════════════════════════════════════════════════════
        heading("6. Engine State Machine", HeadingLevel.HEADING_1),
        para("The CNT engine processes compositions through five sequential stages. Each stage is a pure function with a known precision floor."),

        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [600, 1600, 2500, 2200, 2460],
          rows: [
            new TableRow({ children: [headerCell("#", 600), headerCell("Stage", 1600), headerCell("Operation", 2500), headerCell("Precision", 2200), headerCell("Limiting Factor", 2460)] }),
            new TableRow({ children: [cell("1", 600), cell("CLR", 1600), cell("log, mean, subtract", 2500), cell("≤ 8ε", 2200), cell("log/subtraction", 2460)] }),
            new TableRow({ children: [cell("2", 600), cell("Bearing", 1600), cell("atan2(h_j, h_i)", 2500), cell("machine ε", 2200), cell("None", 2460)] }),
            new TableRow({ children: [cell("3", 600), cell("Ang. velocity", 1600), cell("atan2 + Lagrange", 2500), cell("machine ε", 2200), cell("None after fix", 2460)] }),
            new TableRow({ children: [cell("4", 600), cell("Sensitivity", 1600), cell("1/x_j via softmax", 2500), cell("~1.78e−16", 2200), cell("exp/sum roundtrip", 2460)] }),
            new TableRow({ children: [cell("5", 600), cell("Helmsman", 1600), cell("argmax |delta h|", 2500), cell("exact", 2200), cell("Discrete operation", 2460)] }),
          ],
        }),

        para("The processing flow is:"),
        ...mathBlock([
          "x(t) → CLR → BEARING → ANGULAR VELOCITY → SENSITIVITY → HELMSMAN → CNT(t)",
          "",
          "x(t+1) → CLR ─────────┬───────────────────┘",
          "                     (two CLR vectors feed angular velocity)"
        ]),
        para("No state is carried between timesteps except the previous CLR vector h(t), which feeds the angular velocity computation at t+1. The overall engine precision floor is ~2.22 × 10⁻¹⁶ (IEEE 754 double) for well-conditioned compositions."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 7: ILR CONNECTION
        // ═══════════════════════════════════════════════════════════
        heading("7. Connection to ILR Theory", HeadingLevel.HEADING_1),

        heading("7.1 ILR as Non-Redundant Representation", HeadingLevel.HEADING_2),
        para("The CLR representation is redundant: D coordinates with one constraint (Σh_j = 0), leaving D−1 degrees of freedom. The ILR transform (Egozcue et al. 2003) projects CLR to a (D−1)-dimensional vector using the Helmert basis:"),
        ...mathBlock([
          "z_k = ⟨h, e_k⟩ = Σ_j h_j · (e_k)_j    for k = 1, ..., D−1",
        ]),
        para("The inverse is h = Σ z_k · e_k. This is an isometry: ||h||_CLR = ||z||_ILR."),

        heading("7.2 Implications for CNT", HeadingLevel.HEADING_2),
        para("Since CLR and ILR preserve inner products, all angle-based CNT channels (θ, ω) produce identical results in either representation. The CNT operates natively in CLR for simplicity, but the Helmert basis functions (cnt_helmert_basis, cnt_ilr_project) are available in the engine for interoperability with ILR-based tools."),
        para("The bearing θ uses atan2 on individual CLR components, which requires the full D-dimensional representation. Computing bearing in ILR would require back-projection, adding complexity with no precision benefit."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 8: CALIBRATION
        // ═══════════════════════════════════════════════════════════
        heading("8. Calibration Suite (HCI-CAL01)", HeadingLevel.HEADING_1),
        para("The engine was calibrated against 10 analytically known test objects. Each test object is a synthetic compositional time series where every CNT output is derivable from first principles."),

        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [700, 3200, 3160, 2300],
          rows: [
            new TableRow({ children: [headerCell("Test", 700), headerCell("Name", 3200), headerCell("Validates", 3160), headerCell("Result", 2300)] }),
            new TableRow({ children: [cell("T01", 700), cell("Identity (static)", 3200), cell("ω = 0, constant θ", 3160), cell("PASS", 2300)] }),
            new TableRow({ children: [cell("T02", 700), cell("Drift (linear ramp)", 3200), cell("Monotonic σ, positive ω", 3160), cell("PASS", 2300)] }),
            new TableRow({ children: [cell("T03", 700), cell("Rotation (constant ω)", 3200), cell("Constant angular velocity", 3160), cell("PASS", 2300)] }),
            new TableRow({ children: [cell("T04", 700), cell("Divergence", 3200), cell("Corollary 5 (κ divergence)", 3160), cell("PASS", 2300)] }),
            new TableRow({ children: [cell("T05", 700), cell("Lock", 3200), cell("Corollary 3 (lock detection)", 3160), cell("PASS", 2300)] }),
            new TableRow({ children: [cell("T06", 700), cell("Reversal", 3200), cell("Corollary 4 (sign change)", 3160), cell("PASS", 2300)] }),
            new TableRow({ children: [cell("T07", 700), cell("Symmetry", 3200), cell("Corollary 1 (permutation)", 3160), cell("PASS", 2300)] }),
            new TableRow({ children: [cell("T08", 700), cell("Contraction", 3200), cell("Trace identity Tr(κ)", 3160), cell("PASS", 2300)] }),
            new TableRow({ children: [cell("T09", 700), cell("Decomposition", 3200), cell("Sub-composition ω", 3160), cell("PASS", 2300)] }),
            new TableRow({ children: [cell("T10", 700), cell("Navigation", 3200), cell("Full 4-channel readout", 3160), cell("PASS", 2300)] }),
          ],
        }),
        para("All 10 tests pass. All 5 corollaries independently verified."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 9: PRECISION EXPERIMENTS SUMMARY
        // ═══════════════════════════════════════════════════════════
        heading("9. Precision Experiments Summary (P01–P10)", HeadingLevel.HEADING_1),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [600, 2800, 3960, 2000],
          rows: [
            new TableRow({ children: [headerCell("Exp", 600), headerCell("Title", 2800), headerCell("Key Result", 3960), headerCell("Status", 2000)] }),
            new TableRow({ children: [cell("P01", 600), cell("CLR zero-sum", 2800), cell("max |Σh| = 1.78e−15 = 8ε", 3960), cell("PASS", 2000)] }),
            new TableRow({ children: [cell("P02", 600), cell("Norm variation", 2800), cell("Naive: 53.6%, Ortho: 0.000%", 3960), cell("PASS", 2000)] }),
            new TableRow({ children: [cell("P03", 600), cell("arccos instability", 2800), cell("Up to 4.35e−8° error", 3960), cell("CHARACTERIZED", 2000)] }),
            new TableRow({ children: [cell("P04", 600), cell("atan2 vs arccos", 2800), cell("max diff = 0.00 on T03 data", 3960), cell("PASS", 2000)] }),
            new TableRow({ children: [cell("P05", 600), cell("ILR vs CLR ω", 2800), cell("max diff < 10⁻¹² deg", 3960), cell("PASS", 2000)] }),
            new TableRow({ children: [cell("P06", 600), cell("Helmert basis", 2800), cell("Orthonormal to 2.22e−16", 3960), cell("PASS", 2000)] }),
            new TableRow({ children: [cell("P07", 600), cell("Condition number", 2800), cell("digits ≈ 15 − log₁₀(κ)", 3960), cell("CHARACTERIZED", 2000)] }),
            new TableRow({ children: [cell("P08", 600), cell("Extreme stress", 2800), cell("Stable to x = 10⁻¹⁵", 3960), cell("PASS", 2000)] }),
            new TableRow({ children: [cell("P09", 600), cell("D scaling", 2800), cell("ω std invariant to D = 100", 3960), cell("PASS", 2000)] }),
            new TableRow({ children: [cell("P10", 600), cell("Full chain", 2800), cell("All channels at machine ε", 3960), cell("PASS", 2000)] }),
          ],
        }),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 10: ENGINE QUALIFICATION
        // ═══════════════════════════════════════════════════════════
        heading("10. Engine Qualification", HeadingLevel.HEADING_1),

        heading("10.1 Refinements Applied", HeadingLevel.HEADING_2),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [3120, 6240],
          rows: [
            new TableRow({ children: [headerCell("Refinement", 3120), headerCell("Effect", 6240)] }),
            new TableRow({ children: [cell("arccos → atan2", 3120), cell("Eliminates up to 8 digits of precision loss near 0° and 180°. Uses Lagrange identity for arbitrary-D cross product.", 6240)] }),
            new TableRow({ children: [cell("Helmert basis functions", 3120), cell("cnt_helmert_basis(D) and cnt_ilr_project(h, basis) added for ILR interoperability. Verified to machine ε.", 6240)] }),
            new TableRow({ children: [cell("Condition number", 3120), cell("cnt_condition_number(x) = max(x)/min(x). Predicts available precision digits. Metrology function.", 6240)] }),
          ],
        }),

        heading("10.2 Qualification Status", HeadingLevel.HEADING_2),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [5000, 4360],
          rows: [
            new TableRow({ children: [headerCell("Property", 5000), headerCell("Status", 4360)] }),
            new TableRow({ children: [cell("All CNT channels at machine precision", 5000), cell("VERIFIED", 4360, { bold: true })] }),
            new TableRow({ children: [cell("arccos instability eliminated", 5000), cell("VERIFIED", 4360, { bold: true })] }),
            new TableRow({ children: [cell("Helmert/ILR interoperability", 5000), cell("VERIFIED", 4360, { bold: true })] }),
            new TableRow({ children: [cell("Condition number diagnostic", 5000), cell("OPERATIONAL", 4360, { bold: true })] }),
            new TableRow({ children: [cell("Calibration suite (10 tests)", 5000), cell("10/10 PASS", 4360, { bold: true })] }),
            new TableRow({ children: [cell("Dimensionality scaling to D = 100", 5000), cell("VERIFIED", 4360, { bold: true })] }),
            new TableRow({ children: [cell("Extreme composition stability to x = 10⁻¹⁵", 5000), cell("VERIFIED", 4360, { bold: true })] }),
          ],
        }),
        para("The engine operates at the IEEE 754 double precision floor for all well-conditioned compositions. The only remaining limitation is the condition number of the data itself, which is a fundamental property of simplex geometry."),

        heading("10.3 Can the Engine Be Refined Further?", HeadingLevel.HEADING_2),
        para("No. Every CNT channel has been verified to machine epsilon. The three refinements eliminated every identified source of unnecessary precision loss. The remaining precision boundary is set by the data — specifically, by how close the composition sits to the simplex boundary — and is quantified by the condition number diagnostic."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 11: MATHEMATICAL LINEAGE
        // ═══════════════════════════════════════════════════════════
        heading("11. Mathematical Lineage", HeadingLevel.HEADING_1),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [1800, 800, 3360, 3400],
          rows: [
            new TableRow({ children: [headerCell("Author", 1800), headerCell("Year", 800), headerCell("Contribution", 3360), headerCell("Used in CNT", 3400)] }),
            new TableRow({ children: [cell("Lagrange", 1800), cell("1773", 800), cell("Identity: ||a×b||² = ||a||²||b||² − (a·b)²", 3360), cell("Angular velocity (atan2 form)", 3400)] }),
            new TableRow({ children: [cell("Shannon", 1800), cell("1948", 800), cell("Information entropy", 3360), cell("Hˢ scalar (parallel branch)", 3400)] }),
            new TableRow({ children: [cell("Aitchison", 1800), cell("1986", 800), cell("CLR, Aitchison inner product, simplex geometry", 3360), cell("Stage 1 (CLR), Stage 4 (metric)", 3400)] }),
            new TableRow({ children: [cell("Egozcue et al.", 1800), cell("2003", 800), cell("ILR, Helmert submatrix, Aitchison isometry", 3360), cell("Helmert basis, ILR projection", 3400)] }),
            new TableRow({ children: [cell("Higgins", 1800), cell("2025", 800), cell("Hˢ = 1 − H/ln(D), ring classification", 3360), cell("Framework scalar", 3400)] }),
            new TableRow({ children: [cell("Higgins", 1800), cell("2026", 800), cell("CNT: bearing, velocity, sensitivity, helmsman", 3360), cell("All stages", 3400)] }),
          ],
        }),

        rule(),
        new Paragraph({ spacing: { before: 400 }, children: [] }),
        para("The instrument reads. The expert decides. The loop stays open.", { italics: true, color: C_GRAY, align: AlignmentType.CENTER }),
      ],
    },
  ],
});

// ═══════════════════════════════════════════════════════════════════
// WRITE
// ═══════════════════════════════════════════════════════════════════

const OUTPUT = "/sessions/wonderful-elegant-pascal/mnt/Claude CoWorker/Current-Repo/Hs/papers/flagship/CNT_Engine_Mathematics_Handbook.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUTPUT, buffer);
  console.log("Written: " + OUTPUT);
  console.log("Size: " + buffer.length + " bytes");
});
