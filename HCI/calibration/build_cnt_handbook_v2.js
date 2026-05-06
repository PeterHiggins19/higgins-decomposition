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
          children: [new TextRun({ text: "Complete Mathematics Handbook", font: "Arial", size: 44, bold: true, color: C_ACCENT })],
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
          spacing: { before: 400 },
          children: [new TextRun({ text: "Version 2.0", font: "Arial", size: 28, bold: true, color: C_ACCENT })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 100 },
          children: [new TextRun({ text: "Engine Mathematics + Dynamical Systems + Control Theory + Information Theory", font: "Arial", size: 18, italics: true, color: C_GRAY })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 100 },
          children: [new TextRun({ text: "Engine Qualified to IEEE 754 Double Precision Floor", font: "Arial", size: 18, italics: true, color: C_GRAY })],
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
              new TextRun({ text: "CNT Complete Mathematics Handbook v2.0", font: "Arial", size: 18, color: C_GRAY, italics: true }),
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
        // PART I: FOUNDATIONS
        // ═══════════════════════════════════════════════════════════

        // CHAPTER 1: INTRODUCTION
        heading("1. Introduction", HeadingLevel.HEADING_1),
        para("This handbook provides the complete mathematical specification of the Compositional Navigation Tensor (CNT), the computational core of the Higgins Compositional Bearing Scope (CBS). Version 2.0 extends the original engine mathematics (v1.0) with the full Aitchison metric tensor, the HLR unit family, the System Course Plot, the three-stage analysis pipeline, and three new theoretical connections: dynamical systems theory, control theory, and information theory. Together these establish the CNT as a complete analytical framework for compositional time series."),
        para("The CNT was developed as part of the Higgins Decomposition framework (2025-2026) to provide navigation instrumentation for compositional trajectories on the simplex. It computes, from any closed composition, four quantities that fully characterise the instantaneous directional state and rate of change of a compositional system. Version 2.0 demonstrates that these four channels provide the foundation for importing the entire machinery of dynamical systems analysis, state-space control theory, and information-theoretic diagnostics into the compositional domain."),

        heading("1.1 Scope", HeadingLevel.HEADING_2),
        para("Part I (Chapters 1-7) covers the engine mathematics: CLR geometry, tensor definitions, corollaries, the full Aitchison metric tensor, precision analysis, and engine qualification. Part II (Chapters 8-10) covers the analysis pipeline: Stage 1 section plates, Stage 2 metric cross-examination, Stage 3 higher-degree structural analysis. Part III (Chapters 11-13) establishes three new theoretical connections. Part IV (Chapters 14-16) covers the HLR unit family, the System Course Plot, and the CBS display instrument."),

        heading("1.2 Notation", HeadingLevel.HEADING_2),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [2200, 7160],
          rows: [
            new TableRow({ children: [headerCell("Symbol", 2200), headerCell("Meaning", 7160)] }),
            new TableRow({ children: [cell("x", 2200), cell("Closed composition in the D-simplex, x_j > 0, sum(x_j) = 1", 7160)] }),
            new TableRow({ children: [cell("D", 2200), cell("Number of parts (carriers, components)", 7160)] }),
            new TableRow({ children: [cell("h = clr(x)", 2200), cell("Centred log-ratio transform: h_j = ln(x_j) - (1/D) sum ln(x_k)", 7160)] }),
            new TableRow({ children: [cell("theta", 2200), cell("Bearing tensor: pairwise angle in CLR space (degrees)", 7160)] }),
            new TableRow({ children: [cell("omega", 2200), cell("Angular velocity: total heading change between consecutive CLR vectors", 7160)] }),
            new TableRow({ children: [cell("kappa_HS", 2200), cell("Higgins Steering Metric Tensor: full Aitchison pullback metric on simplex", 7160)] }),
            new TableRow({ children: [cell("sigma", 2200), cell("Helmsman (DCDI): carrier index with maximum |CLR displacement|", 7160)] }),
            new TableRow({ children: [cell("epsilon", 2200), cell("Machine epsilon = 2.22 x 10^-16 (IEEE 754 double)", 7160)] }),
            new TableRow({ children: [cell("e_k", 2200), cell("k-th Helmert basis vector for the CLR zero-sum plane", 7160)] }),
            new TableRow({ children: [cell("HLR", 2200), cell("Higgins Log-Ratio Level: dimensionless natural-log ratio unit", 7160)] }),
            new TableRow({ children: [cell("d_A", 2200), cell("Aitchison distance: Euclidean distance in CLR space", 7160)] }),
            new TableRow({ children: [cell("P", 2200), cell("Centring matrix: I - (1/D) 1 1^T", 7160)] }),
          ],
        }),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 2: CLR GEOMETRY
        // ═══════════════════════════════════════════════════════════
        heading("2. CLR Geometry and the Zero-Sum Plane", HeadingLevel.HEADING_1),

        heading("2.1 The CLR Transform", HeadingLevel.HEADING_2),
        para("The centred log-ratio transform maps a D-part composition x to a vector in R^D:"),
        ...mathBlock(["h_j = ln(x_j) - (1/D) sum_{k=1}^{D} ln(x_k)"]),
        para("By construction, sum(h_j) = 0. This confines all CLR vectors to a (D-1)-dimensional hyperplane through the origin with normal vector 1 = [1,1,...,1]/sqrt(D). The hyperplane is the CLR zero-sum plane. The CLR value h_j measures the log-displacement of carrier j from the geometric mean of all carriers, expressed in HLR (Higgins Log-Ratio Level) units."),

        heading("2.2 Geometric Interpretation", HeadingLevel.HEADING_2),
        para("The simplex S^D (the space where proportions live) is a (D-1)-dimensional surface embedded in D-space. CLR unfolds this curved surface into a flat coordinate system. The constraint changes from 'proportions sum to 1' to 'coordinates sum to 0'. Positive h_j means carrier j is above its geometric-mean share. Negative h_j means below. Large negative h_j means carrier j is approaching absence. The barycenter (geometric mean composition) maps to the origin h = (0, 0, ..., 0)."),

        heading("2.3 Zero-Sum Verification", HeadingLevel.HEADING_2),
        para("Experiment P01 verified that the zero-sum property holds to within 8 epsilon of machine precision across all tested compositions, including extreme skew (x_min = 10^-6) and high dimensionality (D = 20). The maximum observed residual was |sum(h_j)| = 1.78 x 10^-15."),

        heading("2.4 The Helmert Submatrix", HeadingLevel.HEADING_2),
        para("The standard orthonormal basis for the zero-sum plane is the Helmert submatrix (Egozcue et al. 2003). Row k (1-indexed, k = 1, ..., D-1):"),
        ...mathBlock([
          "(e_k)_j = 1/sqrt(k(k+1))     for j < k",
          "(e_k)_j = -k/sqrt(k(k+1))    for j = k",
          "(e_k)_j = 0                   for j > k",
        ]),
        para("This basis was verified to machine precision across D = 3, 4, 8, 20, 100. Orthonormality error: 2.22 x 10^-16. Zero-sum residual: < 1.11 x 10^-16. CLR roundtrip error: < 1.94 x 10^-16."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 3: CNT DEFINITIONS
        // ═══════════════════════════════════════════════════════════
        heading("3. CNT Tensor Definitions", HeadingLevel.HEADING_1),
        para("The Compositional Navigation Tensor decomposes compositional motion into four channels. Each is a deterministic, closed-form, parameter-free function of the composition."),
        ...mathBlock(["CNT(x) = (theta, omega, kappa_HS, sigma)"]),

        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [1600, 1400, 1200, 2000, 1800, 1360],
          rows: [
            new TableRow({ children: [headerCell("Channel", 1600), headerCell("Symbol", 1400), headerCell("Rank", 1200), headerCell("Shape", 2000), headerCell("Unit", 1800), headerCell("Bounds", 1360)] }),
            new TableRow({ children: [cell("Bearing", 1600), cell("theta_ij", 1400), cell("2 (antisym)", 1200), cell("D(D-1)/2", 2000), cell("degrees", 1800), cell("[-180, +180]", 1360)] }),
            new TableRow({ children: [cell("Angular vel.", 1600), cell("omega", 1400), cell("0 (scalar)", 1200), cell("1", 2000), cell("deg/step", 1800), cell("[0, 180]", 1360)] }),
            new TableRow({ children: [cell("Steering", 1600), cell("kappa_HS", 1400), cell("2 (sym)", 1200), cell("D x D", 2000), cell("HLR^-2", 1800), cell("[0, inf)", 1360)] }),
            new TableRow({ children: [cell("Helmsman", 1600), cell("sigma", 1400), cell("0 (categ.)", 1200), cell("1", 2000), cell("index", 1800), cell("{1..D}", 1360)] }),
          ],
        }),

        heading("3.1 Definition 1: Bearing Tensor", HeadingLevel.HEADING_2),
        para("For a composition x with CLR transform h = clr(x), the pairwise bearing between carriers i and j is:"),
        ...mathBlock(["theta_{ij}(x) = atan2(h_j, h_i)"]),
        para("The full bearing tensor collects all D(D-1)/2 pairwise bearings. Each bearing is the angle from carrier i toward carrier j in the CLR plane spanned by dimensions i and j. The atan2 function is well-conditioned everywhere, so bearing computation operates at machine precision unconditionally."),

        heading("3.2 Definition 2: Angular Velocity", HeadingLevel.HEADING_2),
        para("For consecutive compositions x(t) and x(t+1) with CLR transforms h(t) and h(t+1), the angular velocity is the angle between the two CLR direction vectors:"),
        ...mathBlock([
          "omega(t, t+1) = atan2( ||h(t) x h(t+1)||,  <h(t), h(t+1)> )",
          "",
          "where  ||h1 x h2||^2 = ||h1||^2 ||h2||^2 - <h1,h2>^2   (Lagrange identity, 1773)"
        ]),
        para("The Lagrange identity generalises the cross product magnitude to arbitrary dimension D. The atan2 form replaces the original arccos formulation, which loses up to 8 digits of precision near 0 and 180 degrees (see Chapter 6, Experiment P03)."),

        heading("3.3 Definition 3: Higgins Steering Metric Tensor", HeadingLevel.HEADING_2),
        para("The full Aitchison pullback metric tensor on the simplex:"),
        ...mathBlock([
          "kappa_HS_ij(x) = (delta_ij - 1/D) / (x_i x_j)",
          "",
          "In matrix form:  kappa_HS(x) = diag(1/x) P diag(1/x)",
          "where  P = I - (1/D) 1 1^T  (the centring matrix)"
        ]),
        para("The diagonal elements kappa_HS_jj(x) = (1 - 1/D) / x_j^2 govern single-carrier sensitivity. The off-diagonal elements kappa_HS_ij(x) = -1 / (D x_i x_j) govern inter-carrier metric coupling. The negative sign encodes the anti-correlation forced by the closure constraint: when one carrier increases, others must decrease."),
        para("The repo's existing quantity 1/x_j is the diagonal steering sensitivity, which is a readout from the metric tensor rather than the tensor itself. The full tensor captures the complete local geometry of the simplex at any composition."),

        heading("3.4 Metric Tensor Properties", HeadingLevel.HEADING_3),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [3000, 6360],
          rows: [
            new TableRow({ children: [headerCell("Property", 3000), headerCell("Statement", 6360)] }),
            new TableRow({ children: [cell("Symmetry", 3000), cell("kappa_HS_ij = kappa_HS_ji (covariant metric)", 6360)] }),
            new TableRow({ children: [cell("Rank", 3000), cell("D-1 in ambient coordinates (zero-sum constraint removes one dimension)", 6360)] }),
            new TableRow({ children: [cell("Positive semi-definite", 3000), cell("v^T kappa_HS v >= 0 for all v in the tangent space", 6360)] }),
            new TableRow({ children: [cell("Trace", 3000), cell("Tr(kappa_HS) = (1 - 1/D) sum(1/x_j^2)", 6360)] }),
            new TableRow({ children: [cell("Determinant", 3000), cell("det(kappa_HS) = 0 in D-space (rank deficient); det > 0 restricted to (D-1)-subspace", 6360)] }),
            new TableRow({ children: [cell("Condition number", 3000), cell("kappa = max(x)/min(x): determines available precision digits", 6360)] }),
          ],
        }),

        heading("3.5 Definition 4: Helmsman Index (DCDI)", HeadingLevel.HEADING_2),
        para("Between consecutive compositions x(t) and x(t+1), the helmsman is the carrier with maximum CLR displacement:"),
        ...mathBlock(["sigma(t, t+1) = argmax_j |h_j(t+1) - h_j(t)|"]),
        para("Formal name: Dominant Carrier Displacement Index (DCDI). HCI instrument alias: Helmsman Index. The argmax operation is exact. The helmsman is connected to the metric tensor: a carrier with large kappa_jj (rare carrier, high sensitivity) needs only a tiny proportional change to produce a large CLR displacement, making it the likely helmsman."),

        heading("3.6 Dimensionality Expansion", HeadingLevel.HEADING_2),
        para("For D = 8 (Japan EMBER energy), the CNT produces 66 independent measurements from 16 input numbers (8 proportions at 2 time points): 28 bearings + 1 angular velocity + 36 independent metric tensor entries + 1 helmsman index. The tensor reveals structure that is implicit in the raw proportions but invisible in the original representation."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 4: COROLLARIES
        // ═══════════════════════════════════════════════════════════
        heading("4. Corollaries", HeadingLevel.HEADING_1),

        heading("4.1 C1: Bearing Determinism", HeadingLevel.HEADING_2),
        para("The bearing theta_ij is a deterministic, closed-form function of the composition. Same composition, same bearing. No parameters, no fitting, no model selection."),

        heading("4.2 C2: Steering Asymmetry", HeadingLevel.HEADING_2),
        para("For any composition x with max(x)/min(x) = R, the ratio of maximum to minimum diagonal steering sensitivity is R^2. The rarest carrier has R^2 times the steering authority of the most abundant carrier. For Japan EMBER: R approximately 30 (Coal 30% vs Nuclear post-Fukushima 1%), so steering asymmetry approximately 900."),

        heading("4.3 C3: Lock Detection", HeadingLevel.HEADING_2),
        para("Two carriers (i, j) are informationally locked when their pairwise bearing theta_ij varies less than epsilon across T observations: max_t(theta_ij(t)) - min_t(theta_ij(t)) < epsilon. Locked carriers move as a single compositional mode. Their ratio is approximately constant regardless of absolute magnitude changes."),

        heading("4.4 C4: Bearing Reversal", HeadingLevel.HEADING_2),
        para("A sign change in theta_ij from positive to negative (or vice versa) indicates a structural crossover: carrier j transitions from above to below its geometric-mean share relative to carrier i."),

        heading("4.5 C5: Infinite Helm", HeadingLevel.HEADING_2),
        para("When carrier j approaches zero fraction, kappa_HS_jj approaches infinity. Any nonzero change in carrier j dominates the angular velocity. A vanishing carrier has infinite steering authority: its disappearance forces the largest compositional rotation. This is the mechanism behind Japan 2011-2014, where Nuclear shutdown dominated the helmsman readings."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 5: AITCHISON DISTANCE AND METRIC OPERATIONS
        // ═══════════════════════════════════════════════════════════
        heading("5. Aitchison Distance and Metric Operations", HeadingLevel.HEADING_1),

        heading("5.1 Aitchison Distance", HeadingLevel.HEADING_2),
        para("The distance between two compositions x1 and x2 in the Aitchison geometry is the Euclidean distance between their CLR transforms:"),
        ...mathBlock([
          "d_A(x1, x2) = sqrt( sum_j (h1_j - h2_j)^2 )",
          "",
          "Equivalently:  d_A(x1, x2) = sqrt( (1/D) sum_{i<j} (ln(x1_i/x1_j) - ln(x2_i/x2_j))^2 )"
        ]),
        para("This distance is scale-invariant, permutation-symmetric, and subcompositionally coherent (Aitchison 1986). It is the natural distance on the simplex that respects the log-ratio geometry."),

        heading("5.2 Metric Energy", HeadingLevel.HEADING_2),
        para("The metric energy of a composition measures its displacement from the barycenter:"),
        ...mathBlock(["E(x) = ||h||^2 = sum_j h_j^2 = d_A(x, g(x))^2"]),
        para("High metric energy indicates a composition far from the geometric mean. In time series, the sum of metric energies over all steps gives the total displacement energy of the system trajectory."),

        heading("5.3 Metric Inner Product", HeadingLevel.HEADING_2),
        para("The Aitchison inner product between two tangent vectors u, v at composition x is:"),
        ...mathBlock(["<u, v>_A = u^T kappa_HS(x) v"]),
        para("This defines the local geometry: distances, angles, and volumes on the simplex. The metric norm is ||u||_A = sqrt(<u, u>_A). The Aitchison angle between two directions is arccos(<u, v>_A / (||u||_A ||v||_A))."),

        heading("5.4 Geodesics", HeadingLevel.HEADING_2),
        para("In the CLR representation, geodesics on the simplex are straight lines. The shortest path between two compositions x1 and x2 is the line h1 + t(h2 - h1) for t in [0, 1], mapped back to the simplex by applying the inverse CLR (exponentiate and close). This is the compositional analogue of great circles on a sphere."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 6: PRECISION ANALYSIS
        // ═══════════════════════════════════════════════════════════
        heading("6. Precision Analysis", HeadingLevel.HEADING_1),
        para("Ten precision experiments (P01-P10) qualified every CNT channel to the IEEE 754 double precision floor."),

        heading("6.1 The arccos Instability (P03)", HeadingLevel.HEADING_2),
        para("The original angular velocity formula used arccos, whose derivative d(arccos)/dx = -1/sqrt(1-x^2) diverges at x = +/-1, corresponding to angles near 0 and 180 degrees. At 1-cos = 10^-16, the arccos result is 5% wrong: 8 digits of precision lost. The atan2 form, using the Lagrange identity, maintains full precision everywhere."),

        heading("6.2 Condition Number Theory (P07)", HeadingLevel.HEADING_2),
        para("The metric tensor condition number kappa = max(x)/min(x) determines available significant digits: approximately 15 - log10(kappa). For well-conditioned compositions (kappa < 100), all 15 digits are available. For extreme compositions (kappa > 10^10), only 5 digits remain reliable. This is not an engine defect but a fundamental property of simplex geometry."),

        heading("6.3 Precision Summary", HeadingLevel.HEADING_2),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [600, 2400, 4000, 2360],
          rows: [
            new TableRow({ children: [headerCell("Exp", 600), headerCell("Title", 2400), headerCell("Key Result", 4000), headerCell("Status", 2360)] }),
            new TableRow({ children: [cell("P01", 600), cell("CLR zero-sum", 2400), cell("max |sum(h)| = 1.78e-15 = 8 epsilon", 4000), cell("PASS", 2360)] }),
            new TableRow({ children: [cell("P02", 600), cell("Norm variation", 2400), cell("Naive: 53.6%, Helmert: 0.000%", 4000), cell("PASS", 2360)] }),
            new TableRow({ children: [cell("P03", 600), cell("arccos instability", 2400), cell("Up to 4.35e-8 deg error at boundary", 4000), cell("CHARACTERISED", 2360)] }),
            new TableRow({ children: [cell("P04", 600), cell("atan2 vs arccos", 2400), cell("max diff = 0.00 on T03 data", 4000), cell("PASS", 2360)] }),
            new TableRow({ children: [cell("P05", 600), cell("ILR vs CLR omega", 2400), cell("max diff < 10^-12 deg", 4000), cell("PASS", 2360)] }),
            new TableRow({ children: [cell("P06", 600), cell("Helmert basis", 2400), cell("Orthonormal to 2.22e-16", 4000), cell("PASS", 2360)] }),
            new TableRow({ children: [cell("P07", 600), cell("Condition number", 2400), cell("digits approx 15 - log10(kappa)", 4000), cell("CHARACTERISED", 2360)] }),
            new TableRow({ children: [cell("P08", 600), cell("Extreme stress", 2400), cell("Stable to x = 10^-15", 4000), cell("PASS", 2360)] }),
            new TableRow({ children: [cell("P09", 600), cell("D scaling", 2400), cell("omega std invariant to D = 100", 4000), cell("PASS", 2360)] }),
            new TableRow({ children: [cell("P10", 600), cell("Full chain", 2400), cell("All channels at machine epsilon", 4000), cell("PASS", 2360)] }),
          ],
        }),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 7: ENGINE STATE MACHINE AND QUALIFICATION
        // ═══════════════════════════════════════════════════════════
        heading("7. Engine State Machine and Qualification", HeadingLevel.HEADING_1),
        para("The CNT engine processes compositions through five sequential stages. Each stage is a pure function with a known precision floor."),

        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [600, 1600, 2800, 2000, 2360],
          rows: [
            new TableRow({ children: [headerCell("#", 600), headerCell("Stage", 1600), headerCell("Operation", 2800), headerCell("Precision", 2000), headerCell("Limit", 2360)] }),
            new TableRow({ children: [cell("1", 600), cell("CLR", 1600), cell("log, mean, subtract", 2800), cell("<= 8 epsilon", 2000), cell("log/subtraction", 2360)] }),
            new TableRow({ children: [cell("2", 600), cell("Bearing", 1600), cell("atan2(h_j, h_i)", 2800), cell("machine epsilon", 2000), cell("None", 2360)] }),
            new TableRow({ children: [cell("3", 600), cell("Ang. velocity", 1600), cell("atan2 + Lagrange", 2800), cell("machine epsilon", 2000), cell("None after fix", 2360)] }),
            new TableRow({ children: [cell("4", 600), cell("Metric tensor", 1600), cell("(delta_ij - 1/D)/(x_i x_j)", 2800), cell("~1.78e-16", 2000), cell("exp/sum roundtrip", 2360)] }),
            new TableRow({ children: [cell("5", 600), cell("Helmsman", 1600), cell("argmax |delta h|", 2800), cell("exact", 2000), cell("Discrete operation", 2360)] }),
          ],
        }),
        para("No state is carried between timesteps except the previous CLR vector h(t), which feeds the angular velocity computation at t+1. The engine is qualified to IEEE 754 double precision floor for all well-conditioned compositions. All 10 calibration tests (T01-T10) pass. All 5 corollaries independently verified."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // PART II: ANALYSIS PIPELINE
        // ═══════════════════════════════════════════════════════════

        heading("8. Stage 1: Section Engine", HeadingLevel.HEADING_1),
        para("Stage 1 processes a compositional time series through the CNT and produces per-timestep section plates displaying three orthogonal projections of the CLR state."),

        heading("8.1 Processing Chain", HeadingLevel.HEADING_2),
        ...mathBlock([
          "Y_j(t) --> x_j = Y_j / sum(Y) --> h_j = CLR(x) --> CNT channels --> section triad"
        ]),
        para("For each timestep t, the engine computes: all D(D-1)/2 bearings (theta), the angular velocity (omega, requires t-1), the full metric tensor (kappa_HS), the helmsman index (sigma, requires t-1), the Aitchison distance from the previous timestep (d_A), and the Higgins Scale value (Hs)."),

        heading("8.2 Section Triad (CBS Cube Faces)", HeadingLevel.HEADING_2),
        para("Each timestep produces three orthogonal views arranged as faces of a cube:"),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [1200, 2600, 2800, 2760],
          rows: [
            new TableRow({ children: [headerCell("Face", 1200), headerCell("Axes", 2600), headerCell("Content", 2800), headerCell("Fixed Scale", 2760)] }),
            new TableRow({ children: [cell("XY (plan)", 1200), cell("h_i vs h_j", 2600), cell("Carrier scatter in CLR space", 2800), cell("[CLR_min, CLR_max]", 2760)] }),
            new TableRow({ children: [cell("XZ (bearing)", 1200), cell("pair index vs theta", 2600), cell("Bar chart of all bearings", 2800), cell("[-180, +180] degrees", 2760)] }),
            new TableRow({ children: [cell("YZ (profile)", 1200), cell("carrier vs h_j", 2600), cell("CLR value bar chart", 2800), cell("[CLR_min, CLR_max]", 2760)] }),
          ],
        }),
        para("All three faces use fixed-scale graticules that never change between plates. This is what makes the CBS an instrument rather than a chart: the graticule is fixed, only the data moves. Scrolling the cine-deck (time sequence of plates) reveals genuine compositional motion against the static backdrop."),

        heading("8.3 Metric Ledger", HeadingLevel.HEADING_2),
        para("The metric ledger is the numerical authority: a table of all CNT channel values for every timestep. It contains year, theta (bearing in chosen carrier pair), omega, d_A, Hs, ring code, helmsman identity, helmsman displacement, and steering sensitivity range. The ledger is the measurement; the section plates are the visualisation."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 9: STAGE 2
        // ═══════════════════════════════════════════════════════════
        heading("9. Stage 2: Metric Cross-Examination Engine", HeadingLevel.HEADING_1),
        para("Stage 2 performs pairwise and group-level comparisons on Stage 1 outputs using the shared Higgins coordinate frame. It does not create new geometry; it examines the geometry produced by Stage 1."),

        heading("9.1 Group Barycenter Analysis", HeadingLevel.HEADING_2),
        para("Stage 1 observations are grouped (by year, by regime, by external category). For each group, the CLR barycenter (arithmetic mean of CLR vectors) is computed. The barycenter represents the group's central compositional tendency in Aitchison geometry. Per-group diagnostics: metric energy, boundary pressure, helmsman frequency distribution, dominant carrier."),

        heading("9.2 Pairwise Group Cross-Examination", HeadingLevel.HEADING_2),
        para("All pairs of group barycenters are compared under the Aitchison metric:"),
        ...mathBlock([
          "d_A(G_a, G_b) = ||bary_a - bary_b||_CLR",
          "angle(G_a, G_b) = atan2(||bary_a x bary_b||, <bary_a, bary_b>)",
          "dominant_carrier = argmax_k |bary_a_k - bary_b_k|"
        ]),
        para("Results are ranked by metric distance (largest divergence first) and classified as STRONG_DIVERGENCE (d_A > 1.0 HLR), MODERATE_DIVERGENCE (d_A > 0.3), or WEAK_DIVERGENCE."),

        heading("9.3 Carrier Pair Cross-Examination", HeadingLevel.HEADING_2),
        para("For each pair of carriers (i, j), Stage 2 computes: CLR increment correlation (Pearson r of delta_h_i vs delta_h_j across all timesteps), co-movement score (positive correlation), opposition score (negative correlation), and average metric coupling (mean |kappa_HS_ij| across all timesteps). Results ranked by opposition score. Japan EMBER result: Nuclear opposes all other carriers with r = -0.82 to -0.97."),

        heading("9.4 Distance Matrix", HeadingLevel.HEADING_2),
        para("The full N x N Aitchison distance matrix D_ij = d_A(h(t_i), h(t_j)) is computed between all pairs of timesteps. The maximum entry identifies the pair of most divergent observations. For Japan: D_max = 39.18 HLR between 2000 and 2014, dominated by Nuclear carrier."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 10: STAGE 3
        // ═══════════════════════════════════════════════════════════
        heading("10. Stage 3: Higher-Degree Structural Analysis", HeadingLevel.HEADING_1),
        para("Stage 3 extends the analysis beyond pairwise comparisons into triadic structure, subcompositional analysis, and regime detection."),

        heading("10.1 Triadic Day Analysis", HeadingLevel.HEADING_2),
        para("For each combination of three timesteps (t_a, t_b, t_c), Stage 3 computes the metric triangle formed by their CLR barycenters. Side lengths are Aitchison distances. Area is computed via Heron's formula in CLR space:"),
        ...mathBlock([
          "s = (d_AB + d_BC + d_CA) / 2",
          "Area = sqrt( s (s - d_AB) (s - d_BC) (s - d_CA) )"
        ]),
        para("Large triangular area indicates maximum system divergence across three time points. Triadic imbalance (longest/shortest side) measures whether the divergence is directional (high imbalance) or isotropic (low imbalance). Japan: largest triad area 126.17 HLR^2, spanning 2000-2014-2025."),

        heading("10.2 Carrier Triad Analysis", HeadingLevel.HEADING_2),
        para("For each combination of three carriers (i, j, k), Stage 3 computes triadic coupling: the average absolute CLR increment correlation across all three pairs. High coupling indicates three carriers moving as a structural unit. The nuclear-coal-gas triad in Japan shows maximum coupling (r = 0.93-0.99) because the Fukushima event displaced all three simultaneously in opposite directions."),

        heading("10.3 Subcomposition Degree Ladder", HeadingLevel.HEADING_2),
        para("For each subset of k carriers (k = 2, 3, ..., D), Stage 3 extracts the subcomposition, re-closes it, computes CLR, and measures the subcompositional metric energy and boundary pressure. This reveals which carrier subsets are internally stable (low energy variance) and which are volatile (high energy variance). The degree ladder: D0 = point state, D1 = temporal increment, D2 = pairwise (Stage 2), D3 = triadic, Dk = k-face structure, DD = full simplex."),

        heading("10.4 Metric Regime Detection", HeadingLevel.HEADING_2),
        para("Stage 3 partitions the time series into regimes with internally similar metric structure. Consecutive timesteps with similar metric energy are grouped. Within-regime variance and between-regime distance are computed. Japan EMBER reveals two primary regimes: pre-Fukushima (2000-2010, stable low energy) and post-Fukushima (2011-2025, high energy with partial relaxation)."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // PART III: THEORETICAL CONNECTIONS
        // ═══════════════════════════════════════════════════════════

        heading("11. Connection to Dynamical Systems Theory", HeadingLevel.HEADING_1),
        para("The CNT trajectory h(t) is a path through a metric vector space (the CLR zero-sum hyperplane with the Aitchison inner product). This is precisely the mathematical structure required for dynamical systems analysis. The bridge is not analogy; it is direct mathematical import. Every theorem in dynamical systems theory that requires a metric vector space applies to CLR trajectories without modification."),

        heading("11.1 Phase Space Representation", HeadingLevel.HEADING_2),
        para("The CLR zero-sum hyperplane is the phase space. It is a (D-1)-dimensional real vector space with the Euclidean metric (which equals the Aitchison metric in CLR coordinates). Each composition maps to a unique point in this space. A time series of compositions traces a trajectory (the System Course Plot). The compositional constraint (parts sum to 1) becomes the linear constraint (CLR coordinates sum to 0), which defines the phase space as a hyperplane rather than all of R^D."),

        heading("11.2 Lyapunov Exponents", HeadingLevel.HEADING_2),
        para("The maximal Lyapunov exponent measures the average rate of divergence of nearby trajectories in CLR space. Given a reference trajectory h(t) and a perturbed trajectory h*(t) = h(t) + delta(t), the maximal Lyapunov exponent is:"),
        ...mathBlock([
          "lambda_max = lim_{T->inf} (1/T) sum_{t=0}^{T-1} ln( ||delta(t+1)|| / ||delta(t)|| )"
        ]),
        para("For compositional time series, this quantifies structural stability. lambda_max < 0 indicates stable convergence to an attractor. lambda_max = 0 indicates marginal stability (limit cycle or quasiperiodic). lambda_max > 0 indicates sensitivity to initial conditions (chaos). In practice, the finite-time Lyapunov exponent is computed from the observed CLR trajectory using the tangent map derived from the transition operator A(t)."),

        heading("11.3 Attractors and Fixed Points", HeadingLevel.HEADING_2),
        para("A compositional attractor is a set in CLR space toward which the trajectory converges. The CLR barycenter (origin) is a natural candidate fixed point: it represents the maximum-entropy composition where all carriers are equal. If the system tends toward the origin, entropy is increasing and the composition is equilibrating."),
        para("A fixed-point attractor at a non-zero CLR position indicates a stable structural equilibrium with specific carrier dominance. A limit cycle indicates periodic compositional oscillation (e.g., seasonal energy production cycles). A strange attractor would indicate deterministic chaos in the compositional evolution."),
        para("Detection method: compute the CLR barycenter of the last N observations and compare with the barycenter of the first N. If the two are converging, an attractor exists. The Aitchison distance between successive barycenters quantifies the rate of approach."),

        heading("11.4 Bifurcation Analysis", HeadingLevel.HEADING_2),
        para("A compositional bifurcation occurs when a small change in an external parameter causes a qualitative change in the trajectory structure. The CNT channels provide natural bifurcation detectors:"),
        ...mathBlock([
          "omega(t) spikes sharply    -->   trajectory direction changes suddenly",
          "sigma(t) switches carrier  -->   a new carrier takes the helm",
          "kappa_jj(t) diverges       -->   a carrier approaches zero (boundary crisis)",
          "theta_ij(t) reverses sign  -->   structural ordering inverts"
        ]),
        para("Japan 2011: the Fukushima event is a bifurcation. Nuclear carrier approaches zero, kappa_Nuclear diverges, omega spikes to 66 degrees, sigma switches to Nuclear, and multiple bearing reversals occur. The system transitions from one structural regime to another."),

        heading("11.5 Phase Portrait and Velocity Field", HeadingLevel.HEADING_2),
        para("The compositional velocity field maps each CLR position to the average velocity of trajectories passing through that region. For a compositional time series with multiple realizations (e.g., countries), the velocity at position h is:"),
        ...mathBlock([
          "v(h) = E[ h(t+1) - h(t) | h(t) near h ]"
        ]),
        para("The resulting field shows where compositions naturally flow in CLR space. Convergence of flow lines identifies attractors. Divergence identifies repellers. Saddle points identify unstable equilibria. The phase portrait is the compositional analogue of wind maps: it shows the currents in the compositional ocean."),

        heading("11.6 Recurrence Quantification Analysis", HeadingLevel.HEADING_2),
        para("The recurrence matrix R_ij = Theta(epsilon - d_A(h(t_i), h(t_j))) (where Theta is the Heaviside function) identifies timestep pairs where the system revisits a previous CLR state within tolerance epsilon. Recurrence rate measures the fraction of revisited states. Determinism measures the fraction of recurrent points forming diagonal lines (indicating predictable dynamics). Laminarity measures vertical/horizontal line structures (indicating trapping). All of these operate directly in Aitchison geometry using the Aitchison distance d_A."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 12: CONTROL THEORY
        // ═══════════════════════════════════════════════════════════
        heading("12. Connection to Control Theory", HeadingLevel.HEADING_1),
        para("The CLR state vector h(t) fits directly into the standard state-space framework of control theory. The compositional constraint (sum = 0) is a linear constraint, making the state space a linear subspace of R^D. All standard results from linear systems theory, controllability, observability, and optimal control apply."),

        heading("12.1 State-Space Model", HeadingLevel.HEADING_2),
        para("The compositional system in CLR coordinates follows a discrete-time state equation:"),
        ...mathBlock([
          "h(t+1) = A(t) h(t) + B(t) u(t) + w(t)",
          "",
          "where:",
          "  h(t)  = CLR state vector (D-dimensional, sum = 0)",
          "  A(t)  = state transition matrix (D x D)",
          "  B(t)  = input matrix (D x m, m = number of external inputs)",
          "  u(t)  = external forcing vector (policy, intervention, events)",
          "  w(t)  = process noise (model uncertainty)"
        ]),
        para("The transition matrix A(t) encodes how the current compositional state determines the next state. For a stationary system, A is constant and can be estimated from the CLR trajectory by linear regression: A = (sum h(t+1) h(t)^T) (sum h(t) h(t)^T)^-1. The eigenvalues of A determine stability: all |lambda_i| < 1 means the system is asymptotically stable. The eigenvectors identify the principal modes of compositional evolution."),

        heading("12.2 Observation Equation", HeadingLevel.HEADING_2),
        para("The observation model relates measured outputs to the CLR state:"),
        ...mathBlock([
          "y(t) = C h(t) + v(t)",
          "",
          "where:",
          "  y(t)  = observed measurement vector",
          "  C     = observation matrix (maps CLR state to measurements)",
          "  v(t)  = measurement noise"
        ]),
        para("If all carriers are directly observed, C = I (identity). If only a subset of carriers are measured, C is a selection matrix and the system becomes a partial-observation problem amenable to Kalman filtering."),

        heading("12.3 Controllability", HeadingLevel.HEADING_2),
        para("The controllability matrix determines which compositions can be reached from a given initial state via external forcing:"),
        ...mathBlock([
          "C_ctrl = [B, AB, A^2 B, ..., A^{D-2} B]",
          "",
          "rank(C_ctrl) = D-1  -->  fully controllable",
          "rank(C_ctrl) < D-1  -->  some compositional modes cannot be steered"
        ]),
        para("For energy systems: if the controllability matrix has rank < D-1, there exist compositional directions that no combination of policy interventions can reach. This identifies structural constraints on energy transition that are geometric, not political. The maximum rank is D-1 (not D) because the CLR sum-to-zero constraint removes one dimension."),

        heading("12.4 Observability", HeadingLevel.HEADING_2),
        para("The observability matrix determines whether the full compositional state can be reconstructed from partial measurements:"),
        ...mathBlock([
          "O_obs = [C; CA; CA^2; ...; CA^{D-2}]",
          "",
          "rank(O_obs) = D-1  -->  fully observable",
          "rank(O_obs) < D-1  -->  some compositional modes are invisible"
        ]),
        para("Unobservable modes are compositional changes that produce no measurable output. If a country reports only three energy categories (fossil, nuclear, renewable), the full 8-carrier state is unobservable and must be estimated."),

        heading("12.5 Kalman Filter for Compositional State Estimation", HeadingLevel.HEADING_2),
        para("When measurements are noisy or incomplete, the Kalman filter provides optimal (minimum-variance) estimates of the true CLR state:"),
        ...mathBlock([
          "Predict:  h_hat(t|t-1) = A h_hat(t-1|t-1)",
          "          P(t|t-1)     = A P(t-1|t-1) A^T + Q",
          "",
          "Update:   K(t)         = P(t|t-1) C^T (C P(t|t-1) C^T + R)^{-1}",
          "          h_hat(t|t)   = h_hat(t|t-1) + K(t) (y(t) - C h_hat(t|t-1))",
          "          P(t|t)       = (I - K(t) C) P(t|t-1)"
        ]),
        para("The Kalman gain K(t) optimally balances the model prediction against the measurement. Q is the process noise covariance (model uncertainty in CLR space). R is the measurement noise covariance. The filter operates entirely in CLR coordinates, respecting the Aitchison geometry."),

        heading("12.6 Transfer Function and Frequency Response", HeadingLevel.HEADING_2),
        para("The Z-transform of the state equation yields the transfer function G(z) = C(zI - A)^{-1} B, relating input forcing u to output response y in the frequency domain. Poles of G(z) (eigenvalues of A) determine natural frequencies of compositional oscillation. Zeros determine frequencies at which forcing is ineffective. The Bode magnitude plot |G(e^{j omega})| shows which forcing frequencies produce the largest compositional response."),

        heading("12.7 Stability Margins", HeadingLevel.HEADING_2),
        para("For controlled compositional systems, stability margins quantify robustness:"),
        ...mathBlock([
          "Gain margin    = maximum multiplicative increase in forcing before instability",
          "Phase margin   = maximum phase shift before instability",
          "Delay margin   = maximum time delay in feedback before instability"
        ]),
        para("These diagnostics directly address the question: how much perturbation can the compositional system absorb before leaving a desired operating region?"),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 13: INFORMATION THEORY
        // ═══════════════════════════════════════════════════════════
        heading("13. Connection to Information Theory", HeadingLevel.HEADING_1),
        para("The composition x lives on the simplex, which is also the space of probability distributions over D outcomes. This duality connects the CNT directly to information theory. Every composition is simultaneously a physical composition and a probability distribution, making information-theoretic measures natural diagnostics."),

        heading("13.1 Shannon Entropy on the Simplex", HeadingLevel.HEADING_2),
        para("The Shannon entropy of composition x, treated as a probability distribution:"),
        ...mathBlock([
          "H(x) = -sum_j x_j ln(x_j)",
          "",
          "Range: 0 <= H <= ln(D)",
          "H = 0       when one carrier has all the share (x_j = 1 for some j)",
          "H = ln(D)   when all carriers are equal (x_j = 1/D for all j)"
        ]),
        para("The Higgins Scale Hs = 1 - H/ln(D) normalises this to [0, 1] and inverts it: Hs = 0 at maximum entropy (uniform), Hs = 1 at minimum entropy (degenerate). The entropy is a scalar summary of the full CLR state: it measures how far the composition is from the maximum-entropy barycenter."),

        heading("13.2 Fisher Information on the Simplex", HeadingLevel.HEADING_2),
        para("The Fisher information metric on the multinomial family is:"),
        ...mathBlock([
          "g^F_ij(x) = delta_ij / x_j"
        ]),
        para("The Aitchison metric kappa_HS is the Fisher metric with the centring matrix P applied. Specifically, kappa_HS = diag(1/x) P diag(1/x) where P removes the sum constraint. The Fisher information measures the curvature of the log-likelihood surface: high Fisher information at carrier j means small changes in x_j produce large changes in the likelihood. This is precisely the steering sensitivity: the metric tensor IS the Fisher information on the simplex."),

        heading("13.3 Kullback-Leibler Divergence", HeadingLevel.HEADING_2),
        para("The KL divergence from composition x1 to x2, treating both as distributions:"),
        ...mathBlock([
          "D_KL(x1 || x2) = sum_j x1_j ln(x1_j / x2_j)"
        ]),
        para("This is asymmetric (not a metric). Its symmetrised form (Jeffreys divergence) is sum_j (x1_j - x2_j) ln(x1_j/x2_j). The Aitchison distance d_A is related but distinct: d_A uses log-ratios of both compositions relative to their respective geometric means, while KL uses log-ratios of one composition relative to the other. For small perturbations, D_KL approximately (1/2) delta^T G^F delta, where G^F is the Fisher metric: the KL divergence is locally the squared Fisher distance."),

        heading("13.4 Mutual Information Between Carriers", HeadingLevel.HEADING_2),
        para("For a time series of compositions, the mutual information between carriers i and j measures the statistical dependence of their CLR trajectories:"),
        ...mathBlock([
          "I(h_i; h_j) = H(h_i) + H(h_j) - H(h_i, h_j)"
        ]),
        para("High mutual information indicates carriers that carry redundant information about the system state. Low mutual information indicates carriers that provide independent structural information. The lock detection corollary (C3) identifies the extreme case: locked carriers have maximum mutual information (their CLR trajectories are linearly dependent). The carrier pair cross-examination in Stage 2 measures this through CLR increment correlation, which is a proxy for mutual information."),

        heading("13.5 Entropy Rate of the Compositional Process", HeadingLevel.HEADING_2),
        para("The entropy rate of the CLR process h(t) measures the average information generated per timestep:"),
        ...mathBlock([
          "h_rate = lim_{T->inf} H(h(T) | h(T-1), ..., h(1)) / T"
        ]),
        para("A low entropy rate means the trajectory is predictable (the system follows a deterministic path through CLR space). A high entropy rate means the trajectory is unpredictable (the system explores CLR space randomly). The angular velocity omega is a geometric proxy for entropy rate: high omega means large heading changes, which correlate with high unpredictability."),

        heading("13.6 Information Geometry: The Simplex as a Statistical Manifold", HeadingLevel.HEADING_2),
        para("The simplex, equipped with the Fisher metric, is a Riemannian manifold called the multinomial statistical manifold. The CNT channels have direct information-geometric interpretations:"),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [2200, 3800, 3360],
          rows: [
            new TableRow({ children: [headerCell("CNT Channel", 2200), headerCell("Information-Geometric Meaning", 3800), headerCell("Fisher Metric Role", 3360)] }),
            new TableRow({ children: [cell("theta (bearing)", 2200), cell("Direction in the statistical manifold", 3800), cell("Geodesic direction on Fisher sphere", 3360)] }),
            new TableRow({ children: [cell("omega (velocity)", 2200), cell("Rate of information change", 3800), cell("Geodesic speed on Fisher sphere", 3360)] }),
            new TableRow({ children: [cell("kappa_HS (metric)", 2200), cell("Local curvature of log-likelihood", 3800), cell("Fisher information matrix (centred)", 3360)] }),
            new TableRow({ children: [cell("sigma (helmsman)", 2200), cell("Maximum information contributor", 3800), cell("Direction of max Fisher curvature", 3360)] }),
          ],
        }),
        para("The simplex with Fisher metric has constant negative sectional curvature -1/4 (for the standard parametrisation). This makes it a hyperbolic space, connecting the CNT to hyperbolic geometry and the Poincare disc model. Geodesics on this manifold correspond to exponential family paths between distributions."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // PART IV: INSTRUMENTS AND STANDARDS
        // ═══════════════════════════════════════════════════════════

        heading("14. The HLR Unit Family", HeadingLevel.HEADING_1),
        para("All log-ratio measurement systems are related by constant multiplicative k-factors. The HLR (Higgins Log-Ratio Level) is the natural unit of the CLR coordinate: one HLR = one natural-log ratio unit of displacement from the geometric mean barycenter."),

        heading("14.1 The Unit Family", HeadingLevel.HEADING_2),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [2400, 2400, 2280, 2280],
          rows: [
            new TableRow({ children: [headerCell("System", 2400), headerCell("Formula", 2400), headerCell("k (to HLR)", 2280), headerCell("k (from HLR)", 2280)] }),
            new TableRow({ children: [cell("HLR (Np)", 2400), cell("ln(ratio)", 2400), cell("1.000000", 2280), cell("1.000000", 2280)] }),
            new TableRow({ children: [cell("dB amplitude", 2400), cell("20 log10(ratio)", 2400), cell("0.115129", 2280), cell("8.685890", 2280)] }),
            new TableRow({ children: [cell("dB power", 2400), cell("10 log10(ratio)", 2400), cell("0.230259", 2280), cell("4.342945", 2280)] }),
            new TableRow({ children: [cell("log2 fold change", 2400), cell("log2(ratio)", 2400), cell("0.693147", 2280), cell("1.442695", 2280)] }),
            new TableRow({ children: [cell("Cents (music)", 2400), cell("1200 log2(ratio)", 2400), cell("0.000578", 2280), cell("1731.234", 2280)] }),
            new TableRow({ children: [cell("Magnitudes (astro)", 2400), cell("-2.5 log10(ratio)", 2400), cell("-0.921034", 2280), cell("-1.085736", 2280)] }),
            new TableRow({ children: [cell("pH", 2400), cell("-log10([H+])", 2400), cell("-2.302585", 2280), cell("-0.434294", 2280)] }),
            new TableRow({ children: [cell("f-stops (photo)", 2400), cell("log2(ratio)", 2400), cell("0.693147", 2280), cell("1.442695", 2280)] }),
          ],
        }),

        heading("14.2 Universal Conversion", HeadingLevel.HEADING_2),
        ...mathBlock([
          "HLR_value = native_value x k_to_HLR",
          "native_value = HLR_value x k_from_HLR"
        ]),
        para("Any cyclic chain of conversions returns the starting value exactly: k_A/k_B x k_B/k_C x ... x k_N/k_A = 1 (algebraic cancellation). No rounding, no approximation, no model."),

        heading("14.3 Two Categories of CNT-Applicable Systems", HeadingLevel.HEADING_2),
        para("Category 1 (Log-ratio native): 46 systems across RF/telecom, audio, genomics, spectroscopy, astronomy, nuclear physics, pH chemistry, and others. These already measure in logarithmic units. CNT applies via a single k-factor, no closure step needed. Category 2 (Compositional but linear): 30+ systems including geochemistry, food science, election data, market share, energy mix, demographics. These measure in percentages or counts and require the full CLR transform (closure, log, centre). Both categories end up on the same CNT plate. The math is identical; only the entry path differs."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 15: SYSTEM COURSE PLOT
        // ═══════════════════════════════════════════════════════════
        heading("15. The System Course Plot", HeadingLevel.HEADING_1),
        para("The System Course Plot is the literal geometric path of a compositional system through Aitchison space over time. It plots the CLR trajectory as a navigational track with real metric distances measured in HLR."),

        heading("15.1 Construction", HeadingLevel.HEADING_2),
        para("Given a time series of compositions x(1), x(2), ..., x(T):"),
        ...mathBlock([
          "1. Compute h(t) = CLR(x(t)) for all t",
          "2. Project h(t) from D-dimensional CLR space to 2D via PCA",
          "   (find top-2 eigenvectors of Cov(h) across all t)",
          "3. Plot projected h(t) as connected path with year markers",
          "4. Mark start (S) and end (F) with distinct symbols"
        ]),
        para("The first two principal components typically capture 80-95% of total CLR variance, so the 2D projection preserves the dominant trajectory structure. The projection uses PCA on the CLR covariance matrix, which is the Aitchison covariance in CLR coordinates."),

        heading("15.2 What the Course Plot Reveals", HeadingLevel.HEADING_2),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [3000, 6360],
          rows: [
            new TableRow({ children: [headerCell("Feature", 3000), headerCell("Interpretation", 6360)] }),
            new TableRow({ children: [cell("Tight cluster of points", 3000), cell("Stable compositional regime (low omega)", 6360)] }),
            new TableRow({ children: [cell("Long straight excursion", 3000), cell("Rapid unidirectional structural change", 6360)] }),
            new TableRow({ children: [cell("Sharp turn in path", 3000), cell("Bifurcation event (high omega spike)", 6360)] }),
            new TableRow({ children: [cell("Loop back toward start", 3000), cell("Partial return to previous structure (recurrence)", 6360)] }),
            new TableRow({ children: [cell("Divergent arms", 3000), cell("Two or more carriers displaced massively", 6360)] }),
            new TableRow({ children: [cell("Path not returning", 3000), cell("System on a new attractor (regime change permanent)", 6360)] }),
          ],
        }),

        heading("15.3 Prior Art and Novelty", HeadingLevel.HEADING_2),
        para("CoDa has biplots (Gabriel, covariance) that show compositional variation as static scatter. There are ternary diagrams for 3-part compositions. There are CLR time series where individual components are plotted against time separately. In ecology, ordination trajectory plots use PCA or NMDS space. None of these plot the temporal path as a connected navigational track in native Aitchison geometry with the full CNT channel readout. The System Course Plot takes CLR coordinates as literal positions and draws the temporal trajectory as a ship's course. The navigational metaphor is the correct interpretation: a composition moving through time IS tracing a course through a metric space."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 16: CBS DISPLAY INSTRUMENT
        // ═══════════════════════════════════════════════════════════
        heading("16. The Compositional Bearing Scope (CBS)", HeadingLevel.HEADING_1),
        para("The CBS is an oscilloscope-class display instrument that renders CNT outputs as calibrated traces on fixed-scale axes. It projects the full D-dimensional CLR state onto three orthogonal cube faces, swept along the Higgins axis (time) as a cine-deck of section plates."),

        heading("16.1 Cube Structure", HeadingLevel.HEADING_2),
        para("The CBS IS a cube. Each section plate shows three faces simultaneously: XY (plan view: carrier scatter in CLR space), XZ (bearing view: bar chart of D(D-1)/2 pairwise bearings), and YZ (profile view: bar chart of D CLR values). All faces use fixed-scale graticules that never change between plates."),

        heading("16.2 Time Projection (Higgins Axis)", HeadingLevel.HEADING_2),
        para("The cube exists at one time point. To see evolution, project the cube along the time axis. Each face generates a continuous surface when swept. The XY face traces a trajectory surface (the System Course Plot in 2D). The XZ face traces a bearing evolution surface. The YZ face traces a profile evolution surface. The section plate is a cross-section of this volume at one time instant."),

        heading("16.3 Display Standard", HeadingLevel.HEADING_2),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [3000, 6360],
          rows: [
            new TableRow({ children: [headerCell("Property", 3000), headerCell("Standard", 6360)] }),
            new TableRow({ children: [cell("Colour", 3000), cell("None. 8-bit monochrome. 32-level grayscale only", 6360)] }),
            new TableRow({ children: [cell("Symbology", 3000), cell("ASCII: . (data), * (helm), + (origin), x (lock), ^ (reversal)", 6360)] }),
            new TableRow({ children: [cell("Vertical axes", 3000), cell("Full range. Hs [0,1], theta [-180,+180], CLR [fixed min/max]", 6360)] }),
            new TableRow({ children: [cell("Text size", 3000), cell("Higgins Display Standard: 18pt min body, 28pt titles", 6360)] }),
            new TableRow({ children: [cell("Graphics", 3000), cell("Line only. No gradients, shadows, 3D effects, colour fills", 6360)] }),
            new TableRow({ children: [cell("Unit", 3000), cell("HLR (Higgins Log-Ratio Level). Info panel shows DUT native k-factor", 6360)] }),
          ],
        }),

        heading("16.4 Info Panel", HeadingLevel.HEADING_2),
        para("Each section plate includes an info panel showing: system name, carrier count (D), observation count (T), scale provenance chain (Y -> x = Y/T -> h = CLR -> section), DUT native unit with k-factor conversion, year/timestep identifier, Hs value and ring code, helmsman identity, and CLR dynamic range."),
        new Paragraph({ children: [new PageBreak()] }),

        // ═══════════════════════════════════════════════════════════
        // CHAPTER 17: MATHEMATICAL LINEAGE
        // ═══════════════════════════════════════════════════════════
        heading("17. Mathematical Lineage", HeadingLevel.HEADING_1),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [1800, 800, 3400, 3360],
          rows: [
            new TableRow({ children: [headerCell("Author", 1800), headerCell("Year", 800), headerCell("Contribution", 3400), headerCell("Used in CNT", 3360)] }),
            new TableRow({ children: [cell("Lagrange", 1800), cell("1773", 800), cell("Identity: ||axb||^2 = ||a||^2 ||b||^2 - (a.b)^2", 3400), cell("Angular velocity (atan2 form)", 3360)] }),
            new TableRow({ children: [cell("Lyapunov", 1800), cell("1892", 800), cell("Stability theory, characteristic exponents", 3400), cell("Ch.11: trajectory stability diagnostics", 3360)] }),
            new TableRow({ children: [cell("Shannon", 1800), cell("1948", 800), cell("Information entropy", 3400), cell("Ch.13: entropy, Hs scalar", 3360)] }),
            new TableRow({ children: [cell("Kalman", 1800), cell("1960", 800), cell("Optimal state estimation, controllability", 3400), cell("Ch.12: Kalman filter, state-space", 3360)] }),
            new TableRow({ children: [cell("Fisher", 1800), cell("1922", 800), cell("Fisher information, sufficient statistics", 3400), cell("Ch.13: metric = Fisher info", 3360)] }),
            new TableRow({ children: [cell("Aitchison", 1800), cell("1986", 800), cell("CLR, Aitchison geometry, simplex distance", 3400), cell("Foundations: CLR, metric, distance", 3360)] }),
            new TableRow({ children: [cell("Egozcue et al.", 1800), cell("2003", 800), cell("ILR, Helmert submatrix, Aitchison isometry", 3400), cell("Helmert basis, ILR projection", 3360)] }),
            new TableRow({ children: [cell("Higgins", 1800), cell("2025", 800), cell("Hs = 1 - H/ln(D), ring classification", 3400), cell("Framework scalar", 3360)] }),
            new TableRow({ children: [cell("Higgins", 1800), cell("2026", 800), cell("CNT 4-channel tensor, CBS, HCI pipeline", 3400), cell("All chapters", 3360)] }),
          ],
        }),

        heading("17.1 Mathematical Properties (All Channels)", HeadingLevel.HEADING_2),
        new Table({
          width: { size: TW, type: WidthType.DXA },
          columnWidths: [2800, 6560],
          rows: [
            new TableRow({ children: [headerCell("Property", 2800), headerCell("Statement", 6560)] }),
            new TableRow({ children: [cell("Deterministic", 2800), cell("Same input, same output, always. No randomness.", 6560)] }),
            new TableRow({ children: [cell("Closed-form", 2800), cell("No iteration, no convergence criterion, no optimisation.", 6560)] }),
            new TableRow({ children: [cell("Parameter-free", 2800), cell("No tuning, no fitting, no model selection.", 6560)] }),
            new TableRow({ children: [cell("Scale-invariant", 2800), cell("Multiply all carriers by a constant, tensor unchanged.", 6560)] }),
            new TableRow({ children: [cell("Domain-agnostic", 2800), cell("Energy, chemistry, ecology, finance, nuclear, cosmic, audio, RF.", 6560)] }),
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
  console.log("Version: 2.0 — Complete Mathematics Handbook");
  console.log("Chapters: 17 (was 11 in v1.0)");
  console.log("New: Full metric tensor, HLR family, System Course Plot, Stage 1/2/3, Dynamical Systems, Control Theory, Information Theory");
});
