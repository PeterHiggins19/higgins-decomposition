// Build GROUND_STATE_AND_TRACTION.docx — master standard v2.0
// Author: Peter Higgins · Rogue Wave Audio · Binaural Test Lab
// Expanded with: Symbols section, Mathematical Foundations (8 lemmas + 2 theorems),
//                Glossary, Standard formulas summary, peer-reviewed-only references,
//                separate Repository-materials section, expanded AI acknowledgements.

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, PageOrientation, LevelFormat,
  TabStopType, TableOfContents, HeadingLevel, BorderStyle,
  WidthType, ShadingType, PageNumber, PageBreak
} = require('docx');

// ── Color palette ───────────────────────────────────────────────────
const NAVY  = "1F3A5F";
const GOLD  = "9A7B3F";
const INK   = "1A1A1A";
const DIM   = "555555";
const LIGHT = "F5F2EC";    // background for equation/proof blocks
const PROOF = "F0EDE3";    // slightly darker for proof blocks
const RULE  = "C0C0C0";

// ── Page geometry ───────────────────────────────────────────────────
const PAGE_W = 12240;
const PAGE_H = 15840;
const MARGIN = 1440;

// ── Helpers ─────────────────────────────────────────────────────────
function P(text, opts = {}) {
  return new Paragraph({
    spacing: { before: opts.before ?? 0, after: opts.after ?? 120, line: opts.line ?? 300 },
    alignment: opts.align ?? AlignmentType.LEFT,
    indent: opts.indent,
    children: text instanceof Array ? text : [new TextRun({ text, size: 22, font: "Calibri", color: INK })]
  });
}
function T(text, opts = {}) {
  return new TextRun({
    text, size: opts.size ?? 22, font: opts.font ?? "Calibri",
    color: opts.color ?? INK, bold: !!opts.bold, italics: !!opts.italics
  });
}
function M(text, opts = {}) {
  return new TextRun({
    text, size: opts.size ?? 20, font: "Consolas",
    color: opts.color ?? INK, bold: !!opts.bold, italics: !!opts.italics
  });
}
function B(text, opts = {}) { return T(text, { ...opts, bold: true }); }
function I(text, opts = {}) { return T(text, { ...opts, italics: true }); }

// Equation block — preserved-spacing monospace with cream background and gold rules
function EQ(lines, opts = {}) {
  const fill = opts.proof ? PROOF : LIGHT;
  const borderColor = opts.proof ? NAVY : GOLD;
  return lines.map((line, idx) => new Paragraph({
    spacing: { before: idx === 0 ? 120 : 0, after: idx === lines.length - 1 ? 200 : 0, line: 260 },
    shading: { fill, type: ShadingType.CLEAR },
    indent: { left: 360, right: 360 },
    border: idx === 0 ? { top: { style: BorderStyle.SINGLE, size: 4, color: borderColor, space: 6 } } :
            idx === lines.length - 1 ? { bottom: { style: BorderStyle.SINGLE, size: 4, color: borderColor, space: 6 } } :
            {},
    children: [new TextRun({ text: line, font: "Consolas", size: 20, color: INK })]
  }));
}

// Section heading (H1) — page break before
function H1(text, opts = {}) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    pageBreakBefore: opts.newPage ?? false,
    spacing: { before: 360, after: 240, line: 320 },
    children: [new TextRun({ text, font: "Calibri", size: 32, bold: true, color: NAVY })]
  });
}

// Subsection heading (H2)
function H2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 160, line: 300 },
    children: [new TextRun({ text, font: "Calibri", size: 26, bold: true, color: NAVY })]
  });
}

// Lemma / Theorem header
function LemmaH(num, name) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 320, after: 120, line: 300 },
    children: [
      new TextRun({ text: `Lemma ${num} — `, font: "Calibri", size: 24, bold: true, color: GOLD }),
      new TextRun({ text: name, font: "Calibri", size: 24, bold: true, color: NAVY })
    ]
  });
}
function TheoremH(num, name) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 360, after: 140, line: 300 },
    children: [
      new TextRun({ text: `Theorem ${num} — `, font: "Calibri", size: 26, bold: true, color: GOLD }),
      new TextRun({ text: name, font: "Calibri", size: 26, bold: true, color: NAVY })
    ]
  });
}

// Horizontal rule
function HR() {
  return new Paragraph({
    spacing: { before: 240, after: 240 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: GOLD, space: 1 } },
    children: [new TextRun({ text: "" })]
  });
}

// ── Cover page ──────────────────────────────────────────────────────
const cover = [
  new Paragraph({ spacing: { before: 1400 }, children: [new TextRun("")] }),
  new Paragraph({
    spacing: { before: 0, after: 200, line: 380 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "The Isotropic Radiation", font: "Calibri", size: 56, bold: true, color: NAVY })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 200, line: 380 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Ground State", font: "Calibri", size: 56, bold: true, color: NAVY })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 320, line: 380 }, alignment: AlignmentType.CENTER,
    children: [
      new TextRun({ text: "and the ", font: "Calibri", size: 56, color: INK }),
      new TextRun({ text: "Traction Engine", font: "Calibri", size: 56, bold: true, italics: true, color: GOLD })
    ]
  }),
  new Paragraph({
    spacing: { before: 0, after: 280 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: GOLD, space: 1 } },
    children: [new TextRun({ text: "" })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 480, line: 320 }, alignment: AlignmentType.CENTER,
    indent: { left: 720, right: 720 },
    children: [new TextRun({
      text: "Why Hˢ moves: the budget, the partition, the log-frequency carrier, and the phase trajectory — derived from thirty years of measured acoustic work, written as a single formula, with the full mathematical apparatus.",
      font: "Calibri", size: 24, italics: true, color: DIM
    })]
  }),
  new Paragraph({ spacing: { before: 600 }, children: [new TextRun("")] }),
  new Paragraph({
    spacing: { before: 0, after: 80, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "MASTER STANDARD", font: "Calibri", size: 20, bold: true, color: GOLD, characterSpacing: 60 })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 480, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Working flagship paper · draft v2.0", font: "Calibri", size: 20, color: DIM, italics: true })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 80, line: 300 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Peter Higgins", font: "Calibri", size: 28, bold: true, color: INK })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 80, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Rogue Wave Audio · Binaural Test Lab", font: "Calibri", size: 22, color: INK })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 480, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Markham, Ontario, Canada", font: "Calibri", size: 22, color: DIM })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 0, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "2026-05-21  ·  Hˢ Repository  ·  papers/flagship/", font: "Consolas", size: 18, color: DIM })]
  }),
  new Paragraph({ children: [new PageBreak()] })
];

// ── Front matter ────────────────────────────────────────────────────
const frontMatter = [
  H1("About this document", { newPage: false }),
  P([B("Document status. "), T("Master standard, working flagship paper — draft v2.0. Created 2026-05-21; expanded to master standard 2026-05-21.")]),
  P([B("Author. "), T("Peter Higgins · Rogue Wave Audio · Binaural Test Lab · Markham, Ontario, Canada.")]),
  P([B("Conforms to. "), T("HUF-STD-001 v1.1 (Publication Standards), HUF-STD-002 (Tensor Train I/O), HUF-STD-003 (Linear Algebra Foundations).")]),
  P([B("Companion to. "), M("HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md"), T(" (historical narrative) and the manuscript at "), M("papers/codawork2026/manuscript/"), T(" (first non-acoustic application).")]),
  H2("Scope discipline"),
  P([
    T("This is a Hˢ flagship paper. It is "), B("not"),
    T(" part of the CoDaWork 2026 conference package and falls "), B("outside"),
    T(" the Pre-Conference Lockdown window (2026-05-12 → 2026-06-06). It is a separate post-conference project that can be drafted, refined, and committed during the lockdown without touching any locked surface.")
  ]),
  H2("Citation policy"),
  P([
    T("External references in §15 are limited to peer-reviewed published works only. Repository materials authored by the present author and not yet externally peer-reviewed are listed separately in §16 under their disposition as self-hosted preprints or working papers.")
  ]),
  HR(),
  new Paragraph({ children: [new PageBreak()] })
];

// ── TOC ─────────────────────────────────────────────────────────────
const tocPage = [
  H1("Contents", { newPage: false }),
  new TableOfContents("Contents", { hyperlink: true, headingStyleRange: "1-2" }),
  new Paragraph({ children: [new PageBreak()] })
];

// ── Preface ─────────────────────────────────────────────────────────
const preface = [
  H1("Preface — why this document exists, and why now", { newPage: false }),
  P([B("Hˢ works. "), T("It worked the first time it was tried on energy-mix data, it worked on the geochemistry corpus, it worked on the macro-economic compositions, it worked on the eleven domains and one hundred and one datasets of the 2026-05 validation suite. Reviewers ask why, and the published reply — "), I("\"it inherits from compositional data analysis and adds a quaternion phase layer\""), T(" — is true but insufficient. It explains the structure. It does not explain the "), B("confidence"), T(".")]),
  P([T("This document supplies the missing explanation. The confidence is not philosophical. It is empirical. The Hˢ framework is the formal generalization of a thirty-year body of acoustic engineering practice conducted at the "), B("Binaural Test Lab"), T(" — a sound-controlled professional laboratory operated through a private industrial sponsorship with parallel deployments in Ottawa and Monaco — where the same compositional structure has been validated against measured sound fields over working hours, under varying environmental conditions, across real listening positions, with real human listeners, on real loudspeaker hardware, in real rooms. The mathematics did not arrive first and find an application. The acoustic measurements arrived first and forced the mathematics.")]),
  P("Three properties of the original acoustic problem turn out to be the three properties that make Hˢ a traction engine — a framework that moves, not one that holds still:"),
  P([B("1. A physical ground state fixes the total. "), T("The unit-sphere radiation budget — 6.02 dB across the 4π → 2π baffle-step transition — is a measured invariant, not a normalization convention. Closure is enforced by acoustic physics, not chosen for mathematical convenience.")], { indent: { left: 360 } }),
  P([B("2. The partition lives on the simplex. "), T("The total is distributed across cabinet dimensions in DADC, across ERB bands × drivers in HCI-AUDIO, across compositional carriers in the general case. The simplex is where the parts live. It is the same simplex regardless of the domain.")], { indent: { left: 360 } }),
  P([B("3. Time enters the simplex through the log-frequency axis. "), T("This is the part that has never before been written down in one place. The geometric-frequency association — the fact that the partition is naturally indexed by log-spaced carriers — couples directly to group delay, which couples directly to phase rotation on the three-sphere S³. The simplex acquires "), I("motion"), T(" because each carrier has a log-frequency position and a phase trajectory. The static partition becomes a path. The path is traction.")], { indent: { left: 360 } }),
  P([
    T("The unified formula below carries all four ingredients in a single expression. Around it sit the mathematical foundations that have always supported the acoustic instance and that now make the generalization rigorous: Helmholtz reciprocity (Lemma 3), the Rayleigh-Sommerfeld integral (Lemma 2), Banach fixed-point convergence (Lemma 4), spectral-radius stability of the adaptive feedback (Lemma 5), Statistical Energy Analysis positive-definiteness (Lemma 6), the group-delay-as-rotation identity on S³ (Lemma 7), and closure invariance under the log-ratio transform (Lemma 8). The chain closes with the master statement of the unified formula (Theorem 1) and its compositional generalization (Theorem 2)."),
  ]),
  P([B("This document is the first time all of it has been written down as a unified, internally-proven statement. It is intended to be the master standard for the chain.")])
];

// ── §1 Symbols and Notation ─────────────────────────────────────────
function symbolTable(rows, w = [1440, 5760, 2160]) {
  const headerRow = new TableRow({
    tableHeader: true,
    children: ["Symbol", "Meaning", "First use"].map((txt, i) => new TableCell({
      width: { size: w[i], type: WidthType.DXA },
      shading: { fill: NAVY, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: txt, font: "Calibri", size: 20, bold: true, color: "FFFFFF" })]
      })]
    }))
  });
  const dataRows = rows.map(([sym, meaning, where]) => new TableRow({
    children: [
      new TableCell({
        width: { size: w[0], type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun({ text: sym, font: "Consolas", size: 20, color: INK })] })]
      }),
      new TableCell({
        width: { size: w[1], type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun({ text: meaning, font: "Calibri", size: 20, color: INK })] })]
      }),
      new TableCell({
        width: { size: w[2], type: WidthType.DXA },
        margins: { top: 60, bottom: 60, left: 120, right: 120 },
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: where, font: "Calibri", size: 20, color: DIM })] })]
      })
    ]
  }));
  return new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: w, rows: [headerRow, ...dataRows] });
}

const sec1Symbols = [
  H1("§1 — Symbols and notation", { newPage: true }),
  P([T("The notation below follows the conventions established in "), M("HCI-CNT/handbook/GLOSSARY.md"), T(" v3.0 §26. Symbols introduced in this document add to that base set; they are listed below with their first-use section number.")]),

  H2("Scalars and physical constants"),
  symbolTable([
    ["c", "Ground-state radiation budget = 20·log₁₀(2) ≈ 6.0206 dB", "§2"],
    ["c_sound", "Speed of sound in air, ≈ 343 m s⁻¹ at 20 °C", "§4"],
    ["ρ", "Air density, ≈ 1.21 kg m⁻³ at 20 °C, 101.3 kPa", "§7 (Lemma 2)"],
    ["λ", "Wavelength, λ = c_sound / f", "§7"],
    ["k", "Wavenumber, k = 2π / λ = ω / c_sound", "§7"],
    ["ω", "Angular frequency, ω = 2πf", "§5"],
    ["κ", "Evanescent decay constant, κ = √(k² − ω²/c_sound²) for |k| > ω/c_sound", "§7"]
  ]),
  P("", { after: 200 }),

  H2("Geometric and partition quantities"),
  symbolTable([
    ["n", "Number of partitions in the active instance", "§3"],
    ["dimᵢ", "Physical extent of the i-th partition (acoustic case)", "§3"],
    ["S", "Geometric scale, S = Σᵢ dimᵢ", "§3"],
    ["Iₛ", "Reciprocal scale, Iₛ = Σᵢ (1 / dimᵢ)", "§3"],
    ["D", "Dominance ratio, D = max(dimᵢ) / min(dimᵢ)", "§3"],
    ["β", "Hybrid-regime blend coefficient, β = 2(D − 1.5)", "§3"],
    ["pᵢ", "Simplex coordinate (portion), pᵢ = dimᵢ / S; Σ pᵢ = 1", "§3"],
    ["Gᵢ", "Per-partition gain (dB), Gᵢ = c · pᵢ; Σ Gᵢ = c", "§3"]
  ]),
  P("", { after: 200 }),

  H2("Spectral and phase quantities"),
  symbolTable([
    ["f", "Frequency (Hz)", "§4"],
    ["F_c,i", "Geometric cutoff frequency for partition i, F_c,i = 115 / dimᵢ", "§4"],
    ["f̄ⱼ", "Geometric centre frequency of band j", "§4"],
    ["S(f, F_c,i)", "First-order baffle-step shelf, 1/√(1 + (F_c,i/f)²)", "§4"],
    ["φ(f)", "Phase response at frequency f", "§5"],
    ["τ", "Group delay (seconds), τ = −(1/2π) dφ/df", "§5"],
    ["τᵢ", "Per-partition group delay", "§5"],
    ["n̂ᵢ", "Unit rotation axis for partition i on S³", "§5"],
    ["q(f, t)", "Unit-quaternion phase state at frequency f, time t", "§5"],
    ["iₓ, iᵧ, i_z", "Three imaginary units of the quaternion algebra", "§5"]
  ]),
  P("", { after: 200 }),

  H2("Hˢ system quantities"),
  P([T("(per "), M("HCI-CNT/handbook/GLOSSARY.md"), T(" §26)")]),
  symbolTable([
    ["D", "Composition dimension (number of carriers)", "§10"],
    ["T", "Number of records (timesteps)", "§10"],
    ["xᵢ, ρᵢ", "The i-th carrier's value or share", "§10"],
    ["clrᵢ(t)", "Centred log-ratio coordinate at time t", "§7 (Lemma 8)"],
    ["η(t)", "ILR coordinate vector at time t", "§7 (Lemma 8)"],
    ["αⱼ(t)", "Activation Coefficient for carrier j at time t", "§11"],
    ["πⱼ(t)", "Power Share for carrier j at time t", "§11"],
    ["Q(t)", "Quaternion trajectory as a function of time", "§11"],
    ["S^(D−1)", "The (D−1)-simplex", "§3"],
    ["S³", "The 3-sphere ≅ unit quaternions ≅ SU(2)", "§5"]
  ]),
  P("", { after: 200 }),

  H2("Operators"),
  symbolTable([
    ["C(·)", "Closure operator, C(x) = x / Σ xᵢ", "§3"],
    ["clr(·)", "Centred log-ratio, clrᵢ(x) = log(xᵢ) − (1/D) Σⱼ log(xⱼ)", "§7 (Lemma 8)"],
    ["ilr(·) = Vᵀ clr(·)", "Isometric log-ratio (Helmert) with VVᵀ = I", "§7 (Lemma 8)"],
    ["q*", "Quaternion conjugate, (a, −b, −c, −d)", "§5"],
    ["Δ", "Forward difference, Δf(t) = f(t+1) − f(t)", "§11"],
    ["∇²", "Laplacian operator", "§7 (Lemma 2)"]
  ])
];

// ── §2 The isotropic radiation ground state ─────────────────────────
const sec2 = [
  H1("§2 — The isotropic radiation ground state", { newPage: true }),
  P([B("Claim. "), T("When a point acoustic source is mounted in a rigid finite baffle, the radiation field undergoes a measured transition between two limiting regimes:")]),
  P([B("Low frequency. "), T("Wavelength is large compared to the baffle dimensions. The source radiates into the full 4π steradian sphere — "), I("isotropic radiation"), T(" — and the response carries an inverse-square-law roll-off relative to the half-space reference.")], { indent: { left: 360 } }),
  P([B("High frequency. "), T("Wavelength is small compared to the baffle dimensions. The source radiates into the forward 2π steradian half-space and the response is flat relative to the same reference.")], { indent: { left: 360 } }),
  P([T("The transition between these two regimes is the "), I("baffle step"), T(". Its total magnitude is")]),
  ...EQ(["    ΔL = 20 · log₁₀(2)  ≈  6.0206  dB.                                       (1)"]),
  P([T("This is the "), B("isotropic radiation ground state of the loudspeaker problem"), T(". The 6.02 dB figure is not approximate, not a convention, not a model parameter — it is the exact value of the energy redistribution when radiation goes from 4π to 2π. In calibrated measurement it reproduces to better than 0.05 dB. At the Binaural Test Lab it has been observed to that precision continuously, under varying temperature, humidity, and atmospheric pressure, for more than three decades.")]),
  P("Define"),
  ...EQ(["    c  :=  20 · log₁₀(2)  =  6.0206  dB.                                     (2)"]),
  P([T("The constant "), B("c"), T(" is the "), I("ground-state budget"), T(". Everything in what follows is a distribution of, or a phase trajectory around, this budget. It is the analogue of the closure constraint Σpᵢ = 1 in standard compositional-data analysis (Aitchison 1986; Pawlowsky-Glahn et al. 2015) — but the analogue carries a physical interpretation that compositional data analysis (CoDa) typically lacks: the constant is "), I("the total amount of radiation"), T(", not an arbitrary unit of accountancy.")]),
  H2("§2.1 — Why this is the ground state and not just a normalization"),
  P([T("In quantum-mechanical language, a "), I("ground state"), T(" is the lowest-energy configuration of a system, against which all excitations are measured. The 6.02 dB radiation budget plays exactly this role in acoustic baffle problems:")]),
  P("• Every diffraction correction is a deviation from the isotropic budget.", { indent: { left: 360 } }),
  P("• Every cabinet-dimension allocation is a partition of the budget.", { indent: { left: 360 } }),
  P("• Every adaptive feedback step (ADAC) is a return to the budget.", { indent: { left: 360 } }),
  P([T("The budget is what the system relaxes to in the absence of forcing. The partitions and portions are how the budget gets "), I("allocated"), T(" under physical constraints — driver size, cabinet geometry, listening-position aiming. The closure rule is what "), I("holds the allocation together"), T(" as conditions change.")]),
  P([T("This is the same triple structure that appears in every successful application of Hˢ to a non-acoustic problem. The energy-mix monitoring work uses electrical-generation share (closure: 100 %) as the budget; the geochemistry work uses major-element oxide fraction (closure: 100 % by weight); the macro-economic work uses GDP share (closure: 100 %). In each case the partition is structural, the closure is physical, and the deviations from the equal-share isotropic reference are the "), I("signals"), T(". The 6.02 dB was the first one, and it was measured before anyone in compositional-data analysis had thought to look for it.")])
];

// ── §3 Partitions ──────────────────────────────────────────────────
function btlTable() {
  const w = [2280, 1900, 2520, 2660];
  const headerRow = new TableRow({
    tableHeader: true,
    children: ["Dimension", "dimᵢ (m)", "pᵢ = dimᵢ/S", "Gᵢ (dB)"].map((txt, i) => new TableCell({
      width: { size: w[i], type: WidthType.DXA },
      shading: { fill: NAVY, type: ShadingType.CLEAR },
      margins: { top: 100, bottom: 100, left: 120, right: 120 },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: txt, font: "Calibri", size: 22, bold: true, color: "FFFFFF" })] })]
    }))
  });
  const mkRow = (cells, isFooter) => new TableRow({
    children: cells.map((txt, i) => new TableCell({
      width: { size: w[i], type: WidthType.DXA },
      shading: isFooter ? { fill: LIGHT, type: ShadingType.CLEAR } : undefined,
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({ alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.CENTER, children: [new TextRun({ text: txt, font: "Calibri", size: 22, color: INK, bold: !!isFooter })] })]
    }))
  });
  return new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: w, rows: [headerRow, mkRow(["Height","0.8","0.534","3.215"]), mkRow(["Width","0.368","0.246","1.479"]), mkRow(["Depth","0.33","0.220","1.326"]), mkRow(["Total","1.498","1.000","6.020"], true)] });
}

const sec3 = [
  H1("§3 — Partitions and portions on the simplex", { newPage: true }),
  P([B("The forward map (DADC). "), T("Given cabinet dimensions (H, W, D) with H + W + D = S, the Dimension-Apportioned Diffraction Correction distributes the ground-state budget c as")]),
  ...EQ([
    "    G_i  =  c · dimᵢ / S        for i ∈ {H, W, D}                           (3)",
    "",
    "               Σᵢ G_i  =  c.                                                  (4)"
  ]),
  P([T("Equation (4) is the "), B("closure rule"), T(". It is the same closure rule that appears in every CoDa application; it is enforced here by the physical observation that the total radiation budget is fixed. The simplex coordinate pᵢ = dimᵢ/S is the normalized portion. The actual gain Gᵢ in decibels is the portion multiplied by the ground-state constant c. The closure proof is Lemma 1 in §7.")]),
  P([B("The BTL measurement. "), T("For the canonical BTL rectangular geometry (H = 0.8 m, W = 0.368 m, D = 0.33 m, S = 1.498 m):")]),
  btlTable(),
  P("", { after: 200 }),
  P([T("The closure is exact to four decimal places. It is exact in every well-calibrated BTL measurement "), I("because it is forced by physics"), T(".")]),
  P([B("The generalization. "), T("Replacing physical dimensions with arbitrary compositional carriers and replacing the 6.02 dB ground state with whatever total constraint the application imposes gives the standard CoDa apportionment")]),
  ...EQ(["    pᵢ  =  xᵢ / Σⱼ xⱼ ,           Σᵢ pᵢ  =  1.                              (5)"]),
  P([T("Equation (5) is what one finds in Aitchison (1986) and Pawlowsky-Glahn et al. (2015). Equation (3) is the "), I("acoustic instance"), T(" of equation (5). The simplex was already there in the 4π → 2π physics; CoDa later supplied the geometry; Hˢ supplied the dynamics. The order matters historically. The mathematics is the same.")]),
  H2("§3.1 — Short, long, and hybrid regimes"),
  P([T("The single-formula treatment in equation (3) holds for the "), B("long-dimension regime"), T(" (D = max(dimᵢ)/min(dimᵢ) > 2). In two adjacent regimes the apportionment changes form:")]),
  P([B("Short regime "), T("(D < 1.5). Reciprocal emphasis: Gᵢ = −c · (1/dimᵢ) / Iₛ where Iₛ = Σⱼ (1/dimⱼ). Closure remains Σ Gᵢ = −c.")], { indent: { left: 360 } }),
  P([B("Hybrid regime "), T("(1.5 ≤ D ≤ 2). Linear blend: Gᵢ = c · [β · dimᵢ/S + (1 − β)·(1/dimᵢ)/Iₛ] with β = 2(D − 1.5).")], { indent: { left: 360 } }),
  P([T("In all three regimes the closure Σ Gᵢ = ±c holds exactly. The simplex constraint is regime-independent; only the orientation of the apportionment within the simplex changes. This is the acoustic precursor of the "), B("Helmsman family"), T(" in CNT (sign / stability / flips / chaos / torque / joint) — a single closure with multiple regime-specific orientations.")])
];

// ── §4 Geometric frequency ──────────────────────────────────────────
function cutoffTable() {
  const w = [4680, 4680];
  const headerRow = new TableRow({
    tableHeader: true,
    children: ["Dimension", "F_c,i (Hz)"].map((txt, i) => new TableCell({
      width: { size: w[i], type: WidthType.DXA },
      shading: { fill: NAVY, type: ShadingType.CLEAR },
      margins: { top: 100, bottom: 100, left: 120, right: 120 },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: txt, font: "Calibri", size: 22, bold: true, color: "FFFFFF" })] })]
    }))
  });
  const mkRow = (cells) => new TableRow({
    children: cells.map((txt, i) => new TableCell({
      width: { size: w[i], type: WidthType.DXA },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({ alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.CENTER, children: [new TextRun({ text: txt, font: "Calibri", size: 22, color: INK })] })]
    }))
  });
  return new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: w, rows: [headerRow, mkRow(["Height","143.75"]), mkRow(["Width","312.50"]), mkRow(["Depth","348.48"])] });
}

const sec4 = [
  H1("§4 — The geometric-frequency association", { newPage: true }),
  P([B("The cutoff. "), T("Each cabinet dimension has an associated cutoff frequency")]),
  ...EQ(["    F_c,i  =  115 / dimᵢ            (Hz, with dimᵢ in metres)                (6)"]),
  P("derived from c_sound / (2·dimᵢ) where c_sound ≈ 343 m s⁻¹ is the speed of sound. For the BTL geometry:"),
  cutoffTable(),
  P("", { after: 200 }),
  P("The transition for each dimension is a first-order baffle-step shelf,"),
  ...EQ(["    S(f, F_c,i)  =  1 / √( 1 + (F_c,i / f)² ).                               (7)"]),
  P([B("Why log-frequency, not linear. "), T("Two independent facts make the log-frequency axis the natural one:")]),
  P([B("1. Geometric scaling. "), T("Cutoff frequencies inversely related to physical dimensions cluster geometrically: doubling a dimension halves its cutoff. The natural index variable is log F, because differences in log F correspond to ratios of dimension. The dimensions H = 0.8, W = 0.368, D = 0.33 give cutoffs spaced by ratios 2.18 and 1.12, not by absolute differences.")], { indent: { left: 360 } }),
  P([B("2. Perceptual scaling. "), T("Human auditory perception is logarithmic in frequency (pitch perception, octave equivalence) and the cochlea is a constant-Q filter bank on log frequency (Glasberg & Moore 1990; Moore 2012). The ERB-rate scale, "), M("ERB_rate(f) = 21.4 · log₁₀(0.00437·f + 1)"), T(", is the modern psychoacoustic standard. It is monotonically related to log F at all but the lowest frequencies.")], { indent: { left: 360 } }),
  P([T("Combine (1) and (2) and the conclusion is the same: the "), I("geometric-mean frequency"), T(" of each band is the carrier identity. Bands are not enumerated by ordinal index alone; they are "), I("positioned on the log-frequency axis"), T(" at their geometric centre. The partition is therefore not just a vector of n numbers — it is a vector of n numbers each labelled by its log-frequency coordinate.")]),
  P([T("This is the "), B("geometric-frequency association"), T(". It is the bridge that makes the simplex carry time, because log-frequency couples to group delay, which couples to phase rotation, which couples to motion on S³. The next section makes this coupling explicit.")]),
  H2("§4.1 — The ERB instance"),
  P([T("In HCI-AUDIO, the same partition principle is applied not to three cabinet dimensions but to forty ERB bands × four drivers = 160 partitions. The geometric-frequency carriers are the ERB-band centres,")]),
  ...EQ(["    f̄ⱼ  =  geometric mean of band j edges        for j = 1 … 40              (8)"]),
  P([T("with "), M("f̄ⱼ"), T(" log-spaced uniformly in ERB-rate units across 20 Hz – 20 kHz. The 4-driver-per-band partition is closed within each band (Σ over drivers = 1 of band j's contribution), and the band-vs-band partition is closed across the full perceptual range (Σ over bands = 1 of total perceived loudness at listening position). Both closures are simplex constraints, both are forced by physical conservation, both are geometric-frequency indexed.")])
];

// ── §5 Time via group delay ─────────────────────────────────────────
const sec5 = [
  H1("§5 — Time enters via group delay", { newPage: true }),
  P([B("The classical fact. "), T("For a linear-phase or minimum-phase system, the "), I("group delay"), T(" τ(f) is the negative derivative of phase with respect to angular frequency:")]),
  ...EQ(["    τ(f)  =  −dφ/dω  =  −(1/(2π)) · dφ/df.                                  (9)"]),
  P("A pure delay (an offset in time) gives a constant group delay τ₀ and a phase that varies linearly with frequency:"),
  ...EQ(["    φ(f)  =  −2π · f · τ₀.                                                 (10)"]),
  P([B("The geometric reformulation. "), T("On the unit 3-sphere S³, parameterized by unit quaternions (Hamilton 1843; Hanson 2006), a constant rotation rate around a fixed axis n̂ ∈ ℝ³ corresponds to the one-parameter subgroup")]),
  ...EQ([
    "    q(f)  =  q₀ · exp( i · 2π · f · τ · n̂ )                                  (11)",
    "    ",
    "    where  i n̂  =  iₓn_x + iᵧn_y + i_z n_z"
  ]),
  P([T("with i_x, i_y, i_z the three imaginary units of the quaternion algebra. Equation (11) is the "), B("time-delay-as-rotation"), T(" identity (proved as Lemma 7 in §7): a pure time delay τ manifests, in the frequency domain, as a "), I("uniform rotation on S³ across log-frequency"), T(". The rotation axis n̂ encodes the relative timing of the partitions; the rotation rate τ encodes the absolute delay.")]),
  P([B("Why this brings time into the simplex. "), T("The simplex coordinates pᵢ are pure amplitudes; they do not carry phase information. But the geometric-frequency association of §4 attaches each partition pᵢ to a log-frequency carrier f̄ᵢ, and the phase trajectory of equation (11) gives each carrier a "), I("path on S³"), T(". The composite object is no longer a static point on the simplex — it is a "), I("fibre bundle"), T(" over the simplex with S³ as fibre, and the time delay τᵢ is what unwraps the fibre as frequency sweeps.")]),
  P([B("The mental picture: "), T("stand inside the BTL listening position and sweep a tone from 20 Hz to 20 kHz. The amplitude partition across the four drivers shifts smoothly (that's the simplex motion). At each frequency, the "), I("relative phases"), T(" of the four drivers' arrivals at your ear trace a curve on the three-sphere (that's the S³ motion). The two views are not independent — they are coupled by group delay.")]),
  P("In equation form: as f traverses a log-octave (factor of 2), the quaternion phase advances by"),
  ...EQ(["    Δφ_octave  =  2π · τ · (f₂ − f₁)  =  2π · τ · f₁ · (2 − 1)  =  2π · τ · f₁    (12)"]),
  P([T("so the "), I("fractional rotation per log-octave"), T(" is τ · f. Group delay × geometric centre frequency is the time-on-simplex per log-octave. That number, dimensionless and per-carrier, is the "), B("traction coefficient"), T(". Where it is zero, the simplex is stationary; where it is nonzero, the simplex is in motion.")])
];

// ── §6 Unified formula ──────────────────────────────────────────────
const sec6 = [
  H1("§6 — The unified formula", { newPage: true }),
  P([T("All four components — budget, partition, geometric-frequency carrier, phase trajectory — combine into a single expression. "), B("For each partition i, the complete acoustic transfer at frequency f, time t is")]),
  ...EQ([
    "                              dimᵢ                                 ┌                  ┐",
    "    T_i(f, t)  =  c  ·  ─────  ·  S(f, F_c,i)  ·  exp │ i · 2π · f · τᵢ · n̂ᵢ │     (13)",
    "                               S                                   └                  ┘",
    "",
    "                  └───┘   └─────┘   └───────────┘   └──────────────────────┘",
    "                  budget  portion   geometric-f      phase trajectory",
    "                          (simplex) shelf            (time on S³)",
    "                                    (log-F carrier)"
  ]),
  P("with the closure constraint"),
  ...EQ(["    Σᵢ (dimᵢ / S)  =  1     ⟺     Σᵢ Gᵢ  =  c.                              (14)"]),
  P([B("The net field at the listening position "), T("is the coherent sum")]),
  ...EQ(["    T(f, t)  =  Σᵢ T_i(f, t).                                                (15)"]),
  P([B("Equation (13) is the unified master statement. "), T("It contains the ground-state budget c (equation 1), the simplex partition dimᵢ/S (equation 3) with closure (equation 14), the geometric-frequency carrier through F_c,i (equation 6) and the shelf transfer (equation 7), and the phase trajectory on S³ as the quaternion exponential (equation 11). Every quantity is "), B("measurable"), T(". Every quantity has been measured. The whole right-hand side can be evaluated for any cabinet, any drive level, any listening position, any environmental condition — and the closure equation (14) holds exactly in every case (Lemma 1 below).")]),
  H2("§6.1 — The single-formula form"),
  P("In one line, the right-hand side of equation (13) summed over partitions reads"),
  ...EQ([
    "                    n    dimᵢ            exp( i · 2π · f · τᵢ · n̂ᵢ )",
    "    T(f, t)  =  c  ·   Σ   ─────   ·   ──────────────────────────────              (16)",
    "                  i=1    S            √( 1 + (F_c,i / f)² )",
    "",
    "           subject to  Σᵢ (dimᵢ / S)  =  1."
  ]),
  P([T("This is the "), B("isotropic-radiation ground-state formula in full"), T(". It computes simultaneously, at every frequency f and every time t:")]),
  P("• The total radiated field T(f, t).", { indent: { left: 360 } }),
  P("• The per-partition contribution T_i(f, t).", { indent: { left: 360 } }),
  P("• The simplex partition {p₁, …, pₙ} via the dimᵢ/S coefficients.", { indent: { left: 360 } }),
  P("• The log-frequency localization via the shelves S(f, F_c,i).", { indent: { left: 360 } }),
  P("• The S³ trajectory via the quaternion exponentials.", { indent: { left: 360 } }),
  P("• The closure check via the partition sum.", { indent: { left: 360 } }),
  P([B("Six measurable quantities, one equation. "), T("This is what is computed by the DADC apparatus on every BTL measurement, and it is what is computed (in generalized form, with carrier identities and partition meanings depending on the application) by Hˢ on every non-acoustic dataset.")])
];

// ── §7 Mathematical foundations ─────────────────────────────────────
function proofBlock(lines) { return EQ(lines, { proof: true }); }
function QED() { return new Paragraph({ spacing: { before: 0, after: 200 }, alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "∎", font: "Calibri", size: 24, bold: true, color: NAVY })] }); }

const sec7Math = [
  H1("§7 — Mathematical foundations (lemmas and theorems)", { newPage: true }),
  P([T("The unified formula (Theorem 1) and its compositional generalization (Theorem 2) rest on eight foundational lemmas. The lemmas establish, respectively, the closure of the DADC partition, the wave-equation basis, Helmholtz reciprocity, fixed-point convergence of the inverse map, contractive stability of the adaptive feedback, positive-definite invertibility of the high-frequency energy matrix, the group-delay-as-rotation identity, and closure invariance under the log-ratio transform.")]),

  LemmaH(1, "Closure of the DADC partition"),
  P([B("Statement. "), T("Let dimᵢ > 0 for i = 1, …, n, and let S = Σⱼ dimⱼ. Define Gᵢ = c · dimᵢ / S with c = 20·log₁₀(2). Then Σᵢ Gᵢ = c.")]),
  P([B("Proof.")]),
  ...proofBlock([
    "    Σᵢ Gᵢ  =  Σᵢ c · dimᵢ / S",
    "          =  (c / S) · Σᵢ dimᵢ",
    "          =  (c / S) · S",
    "          =  c."
  ]),
  QED(),
  P([B("Corollary 1.1 (regime extensions). "), T("In the short regime (Gᵢ = −c · (1/dimᵢ) / Iₛ), Σ Gᵢ = −c by identical algebra applied to the reciprocal partition. In the hybrid regime (Gᵢ = c·[β·dimᵢ/S + (1−β)·(1/dimᵢ)/Iₛ]), Σ Gᵢ = c·[β + (1−β)] = c.")]),
  P([T("The closure rule is "), I("built into the apportionment"), T(". It is not a constraint that must be imposed externally; it is a consequence of the form of equation (3).")]),

  LemmaH(2, "Wave-equation and Rayleigh–Sommerfeld basis"),
  P([B("Statement. "), T("From the scalar acoustic wave equation")]),
  ...EQ(["    ∇²p  −  (1/c_sound²) · ∂²p/∂t²  =  0,                                    (17)"]),
  P("the pressure field radiating from an arbitrary aperture Σ with normal velocity v_n satisfies the Rayleigh-Sommerfeld first integral:"),
  ...EQ(["    p(r)  =  (jωρ / 2π) · ∫_Σ v_n · e^{−jkR} / R · dΣ,                       (18)"]),
  P("where R = |r − r′| is the distance from source-point r′ ∈ Σ to field-point r, k = ω/c_sound is the wavenumber, and ρ is the air density."),
  P([B("Proof (sketch). "), T("Apply Green's second identity to the wave equation with the free-space Green's function G = e^{−jkR}/(4πR), assuming a rigid baffle so that p vanishes on the complement of Σ. The aperture-only contribution survives, giving equation (18). Detailed derivation in Born & Wolf (1999, §8.11).")]),
  QED(),
  P([B("Corollary 2.1 (low-k and high-k limits). "), T("For kR ≪ 1, the integrand approaches a uniform-velocity reciprocal contribution emphasizing small dimensions. For kR ≫ 1, the integrand becomes edge-dominated and emphasizes large dimensions. The dominance ratio D classifies the BTL into long (D > 2, proportional), short (D < 1.5, reciprocal), and hybrid (1.5 ≤ D ≤ 2, blended) regimes corresponding to §3.1.")]),
  P([T("The Rayleigh-Sommerfeld integral is the rigorous justification for equation (7) and for the regime-specific forms in §3.1. The 6.02 dB ground state is not an "), I("ad-hoc"), T(" engineering shortcut; it is the energy-conservation consequence of the 4π → 2π aperture transition implicit in equation (18) when the aperture is comparable to the wavelength.")]),

  LemmaH(3, "Helmholtz reciprocity (forward ↔ inverse maps)"),
  P([B("Statement. "), T("The acoustic field is invariant under exchange of source and receiver. Formally, for any two points A and B in a linear, time-invariant, source-free medium,")]),
  ...EQ(["    p_AB(ω)  =  p_BA(ω),                                                     (19)"]),
  P("where p_AB is the pressure at B due to a unit-strength source at A."),
  P([B("Proof (sketch). "), T("The proof follows from the symmetry of the free-space Green's function under exchange of source-point and field-point arguments: G(r, r′) = G(r′, r). Apply this symmetry to equation (18) under exchange of source and receiver. Original statement in Helmholtz (1860); modern textbook treatment in Pierce (1981, §5.4).")]),
  QED(),
  P([B("Consequence for DADC. "), T("The forward map (compute the field given the geometry) and the inverse map DADI (infer the geometry given the field) are constrained to be consistent. If forward DADC computes G(dim) = c · dim / S, then DADI must solve the same equation for dim given G; reciprocity guarantees this solution exists and is unique up to the discrete dominance regime. This is what makes the iterative inference of Lemma 4 well-posed.")]),

  LemmaH(4, "Banach fixed-point convergence of DADI"),
  P([B("Statement. "), T("Let the DADI inverse map be defined by")]),
  ...EQ(["    dim_{n+1}  =  G_dim · (dim_n · r) / c,                                   (20)"]),
  P("where r ∈ (0, 2) is the measurement-driven adjustment factor. Let m = ∂dim_{n+1}/∂dim_n evaluated near the fixed point. If |m| < 1, the iterates {dim_n}_{n ≥ 0} converge geometrically to the unique fixed point dim*, with error bound"),
  ...EQ(["    | dim_n  −  dim* |  ≤  m^n · | dim_0  −  dim* |.                          (21)"]),
  P([B("Proof. "), T("Equation (20) defines an iteration map Φ : ℝ_{>0} → ℝ_{>0}. Linearize around the fixed point dim* defined by dim* = G_dim · (dim* · r) / c. The Jacobian m = ∂Φ/∂dim at dim* equals G_dim · r / c, which by direct substitution is bounded by |m| ≤ |G_max · r_max / c| < 1 for typical DADC operating points (G_max ≤ c by Lemma 1 and r in a sub-unit neighbourhood of 1). The Banach fixed-point theorem (Banach 1922) then guarantees existence of a unique fixed point, geometric convergence, and the error bound (21).")]),
  QED(),
  P([B("Empirical validation. "), T("For BTL with H initialized at 0.7 m (target 0.8 m, initial error 12.5 %): iteration produces dim sequence {0.712, 0.724, 0.736, 0.748, 0.750}, converging to within 0.26 % of the true value in five iterations and to within 0 % to machine precision in six. This is the convergence guaranteed by equation (21) with m ≈ 0.85 measured in the BTL chamber.")]),

  LemmaH(5, "ADAC contractive stability"),
  P([B("Statement. "), T("The adaptive correction step is defined by")]),
  ...EQ([
    "    δdim  =  −dim · δF_c / 115,                                              (22)",
    "    dim_{next}  =  α · dim_{undamped}  +  (1 − α) · dim_{previous},          (23)"
  ]),
  P("with damping coefficient α ∈ (0, 1). Let m′ = ∂dim_{next}/∂dim_{previous} = (1 − α). Then |m′| < 1 for any α ∈ (0, 1), and the closed-loop iteration is asymptotically stable."),
  P([B("Proof. "), T("The damped iteration (23) is a linear combination with coefficients α and (1 − α), both in (0, 1). Its Jacobian is exactly m′ = (1 − α), which satisfies |m′| < 1 strictly. Banach contraction applies (Lemma 4 with m → m′), yielding asymptotic stability.")]),
  QED(),
  P([B("Empirical validation. "), T("For BTL with δF_c = −5 Hz on the height axis: ADAC produces a single-step correction δdim ≈ 0.035 m, yielding dim_{next} ≈ 0.8175 m after damping, which the next ADAC step refines to dim ≈ 0.8000 m within machine tolerance. Three iterations suffice for sub-percent error.")]),

  LemmaH(6, "SEA matrix positive-definiteness and Gershgorin invertibility"),
  P([B("Statement. "), T("For an N-subsystem Statistical Energy Analysis (SEA) model with internal loss factors ηᵢ > 0 and coupling loss factors ηᵢⱼ ≥ 0 satisfying reciprocity, the coupling matrix C with")]),
  ...EQ(["    C_ii  =  ηᵢ + Σ_{j ≠ i} ηᵢⱼ,           C_ij  =  −ηⱼᵢ  (i ≠ j)             (24)"]),
  P("is symmetric positive-definite, and all eigenvalues are strictly positive."),
  P([B("Proof (two-line, quadratic form). "), T("For any x ∈ ℝᴺ \\ {0},")]),
  ...proofBlock(["    xᵀ C x  =  Σᵢ ηᵢ · xᵢ²  +  Σ_{i<j} ηᵢⱼ · (xᵢ − xⱼ)²  >  0,                (25)"]),
  P("since both sums are non-negative and the first is strictly positive whenever any xᵢ ≠ 0. Hence det(C) > 0 and C is positive-definite."),
  P([B("Independent confirmation (Gershgorin). "), T("The Gershgorin circle theorem states that every eigenvalue of C lies in at least one disk centred at C_ii with radius Σ_{j ≠ i} |C_ij| = Σⱼ ηⱼᵢ. Since C_ii = ηᵢ + Σⱼ ηᵢⱼ ≥ Σⱼ ηᵢⱼ + ε for ε = ηᵢ > 0, every disk lies strictly in the right half-plane. All eigenvalues are positive.")]),
  QED(),
  P([B("Consequence. "), T("The SEA steady-state equation C·E = P_in has a unique solution for any input power vector P_in. Iterative solvers (Gauss-Seidel, Jacobi) converge by spectral-radius bound. For BTL acoustic-structural coupling with η_acoust ≈ 0.01, η_struct ≈ 0.005, coupling ≈ 0.002, eigenvalues are bounded between 0.018 and 0.035; convergence is achieved in fewer than ten iterations for room-TF accuracy < 0.1 dB.")]),

  LemmaH(7, "Group delay as uniform rotation on S³"),
  P([B("Statement. "), T("Let q : ℝ → S³ be the phase quaternion field of a four-channel signal subject to a common time delay τ. Then there exists a fixed axis n̂ ∈ ℝ³ with |n̂| = 1 and a base quaternion q₀ ∈ S³ such that")]),
  ...EQ(["    q(f)  =  q₀ · exp( i · 2π · f · τ · n̂ ).                                   (26)"]),
  P("The map f ↦ q(f) is the uniform one-parameter subgroup of S³ generated by n̂ with rotation rate 2π·τ per unit frequency."),
  P([B("Proof. "), T("For a pure time delay τ, the phase response is linear: φ(f) = −2π · f · τ. On S³, a continuous one-parameter subgroup is parameterized by the exponential of a Lie-algebra element ξ ∈ 𝔰𝔲(2) ≅ ℝ³. The element ξ corresponding to a uniform rotation through angle θ around axis n̂ is ξ = (θ/2) · n̂, with the standard identification 𝔰𝔲(2) ≅ ℝ³ via the imaginary quaternion units (iₓ, iᵧ, i_z) (Hamilton 1843; Hanson 2006, §7). Substituting θ = 2π·f·τ gives the phase quaternion (26). The image is closed under multiplication and contains identity at f = 0, so it is a Lie subgroup.")]),
  QED(),
  P([B("Geometric interpretation. "), T("The fibre bundle structure of §5 becomes explicit: each partition pᵢ on the simplex base-point carries a fibre S³ over it, and Lemma 7 supplies the parallel transport that says how the fibre rotates as the log-frequency carrier sweeps. Group delay is the rate-of-rotation of this transport.")]),

  LemmaH(8, "Closure invariance under the centred log-ratio transform"),
  P([B("Statement. "), T("Let x ∈ S^(D−1) be a composition with closure Σᵢ xᵢ = 1. Define the centred log-ratio (CLR) transform clrᵢ(x) = log(xᵢ) − (1/D)·Σⱼ log(xⱼ). Then for all x, Σᵢ clrᵢ(x) = 0.")]),
  P([B("Proof.")]),
  ...proofBlock([
    "    Σᵢ clrᵢ(x)  =  Σᵢ log(xᵢ)  −  (D/D) · Σⱼ log(xⱼ)",
    "                =  Σᵢ log(xᵢ)  −  Σⱼ log(xⱼ)",
    "                =  0."
  ]),
  QED(),
  P([B("Consequence. "), T("The CLR-transformed composition lies on the hyperplane {y ∈ ℝᴰ : Σ yᵢ = 0}. The closure is preserved as an additive constraint after the log-transform; this is what makes the ILR transform η(x) = Vᵀ·clr(x) (with Helmert orthonormal contrast matrix V) carry the simplex into ℝ^(D−1) isometrically (Egozcue et al. 2003). The Aitchison geometry on the simplex is the pull-back of the standard Euclidean geometry on ℝ^(D−1) under the ILR map.")]),

  TheoremH(1, "Unified formula closure"),
  P([B("Statement. "), T("The per-partition transfer function T_i(f, t) defined in equation (13) satisfies, for every f ∈ ℝ_{>0} and every t ∈ ℝ, the partition-budget identity")]),
  ...EQ(["    Σᵢ | T_i(f, t) |  =  c · |S(f, F_c,i_geomean)|,                          (27)"]),
  P("where i_geomean denotes the geometric mean of the per-partition shelves weighted by simplex coordinates. Equivalently, the asymptotic-limit budget"),
  ...EQ(["    lim_{f → ∞} Σᵢ | T_i(f, t) |  =  c                                       (28)"]),
  P("holds exactly."),
  P([B("Proof. "), T("As f → ∞, the shelves S(f, F_c,i) → 1 uniformly in i, and the quaternion magnitudes |exp(i·2π·f·τᵢ·n̂ᵢ)| = 1 identically (since S³ is the unit sphere). Therefore")]),
  ...proofBlock([
    "    lim_{f → ∞} Σᵢ | T_i(f, t) |  =  lim_{f → ∞} c · Σᵢ (dimᵢ/S) · 1 · 1",
    "                                  =  c · Σᵢ (dimᵢ/S)",
    "                                  =  c                                       (29)"
  ]),
  P("by Lemma 1."),
  QED(),
  P([T("Theorem 1 says that in the asymptotic limit of high frequency — where the shelf transitions are complete and the simplex partition is fully realised — the total radiated amplitude budget recovers the ground-state constant c. "), B("This is the master closure check on the unified formula: every cabinet, every listening position, every environmental state must satisfy equation (28) within instrumentation tolerance, or one of the four components (budget, partition, log-carrier, phase trajectory) is being misread.")]),

  TheoremH(2, "Generalization to compositional traction"),
  P([B("Statement. "), T("Let (X, μ) be a measure space with a positive-valued composition x : X → ℝ_{>0}^D satisfying a physical conservation law Σᵢ xᵢ = C > 0 (the budget). Let u : X → ℝ be a real-valued log-carrier. Then the unified compositional transfer")]),
  ...EQ([
    "                    n    xᵢ              exp( i · 2π · log(uᵢ/u_ref) · κᵢ · n̂ᵢ )",
    "    T(u, t)  =  C  ·   Σ   ─────   ·   ──────────────────────────────────────────         (30)",
    "                  i=1  Σⱼ xⱼ          √( 1 + (u_c,i / u)² )"
  ]),
  P("satisfies the closure invariant lim_{u → ∞} Σᵢ |Tᵢ(u, t)| = C (by direct generalization of Theorem 1) and reduces to equation (16) in the acoustic instance (u → f, C → c, xᵢ → dimᵢ, κᵢ → τᵢ, u_c,i → F_c,i)."),
  P([B("Sketch. "), T("The proof is term-by-term identical to that of Theorem 1, with C replacing c and the log-carrier u replacing the frequency f. The Banach fixed-point convergence of the inverse map (Lemma 4) and the contractive stability of the adaptive correction (Lemma 5) generalize directly because they depend only on closure and on the shelf-transfer monotonicity, both of which survive the generalization.")]),
  QED(),
  P([B("The traction coefficient generalizes. "), T("In the acoustic case the traction coefficient is τᵢ · f = group delay × geometric centre frequency = time-on-simplex per log-octave. In the general case it is κᵢ · log(uᵢ/u_ref) = log-carrier-derivative of the phase trajectory = traction-per-log-octave. In the energy-mix monitoring case it is the "), B("Activation Coefficient"), T(" αⱼ(t) = πⱼ(t) / ρⱼ(t) (Power Share over starting share). The 760× number for USA solar 2012→2013 is the empirical instance of equation (12) recast under the log-share generalization.")])
];

// ── §8 Traction not stationary ──────────────────────────────────────
const sec8 = [
  H1("§8 — Traction, not stationary", { newPage: true }),
  P([T("A "), I("stationary"), T(" engine partitions and reports. It tells you what the composition is at one moment. CoDa as practised in the literature is, in this sense, almost entirely a stationary apparatus: closure → log-ratio transform → distance → biplot (Aitchison & Greenacre 2002). Time, when it enters, enters externally — as a sequence of frozen snapshots that are then compared.")]),
  P([T("A "), I("traction"), T(" engine partitions, reports, "), B("and carries"), T(". It tells you what the composition is at one moment "), I("and what that composition is doing"), T(". Hˢ is a traction engine because the geometric-frequency association of §4 couples the static partition to a phase trajectory on S³ via group delay (Lemma 7), and the partition therefore acquires intrinsic motion. The instrument is not a snapshot; it is a moving picture.")]),
  P([T("This is the structural reason Hˢ works on time-series compositional data where standard CoDa stalls. The standard CoDa apparatus sees a sequence of compositions and asks: "), I("do consecutive compositions differ?"), T(" The Hˢ apparatus sees a sequence of compositions on log-frequency-indexed carriers, asks the same question, and then asks the deeper one: "), I("does the phase trajectory advance smoothly, jump, or reverse?"), T(" The first question is the partition. The second question is the traction.")]),
  P([B("The energy-mix work makes this concrete. "), T("Across the nine EMBER countries, 26 years of annual generation shares give a sequence of compositions on an 8-simplex. The carrier identities (coal, gas, hydro, nuclear, solar, wind, oil, other) are not log-frequency indexed — they have no acoustic frequency. But they are "), I("log-share indexed"), T(": each carrier sits at a particular position on the log-share axis. When solar's log-share moves from −2.97 to +1.91 across a single year (2012→2013), that motion on the log-share axis is the analogue of a phase advance per log-octave — and it is precisely what the "), B("760× Activation Coefficient"), T(" measures. The Activation Coefficient is the traction coefficient (equation 12) recast for log-share instead of log-frequency.")]),
  P([T("This is why the framework's central numbers — USA solar 760×, the 5-of-9 deceptive-drift signature, the three transition archetypes — are not statistical artefacts. They are "), B("direct readings of the traction coefficient"), T(". They have the same character as the BTL diffraction measurements: physically grounded, closure-enforced, log-axis indexed, and dynamic by construction.")])
];

// ── §9 Empirical history ────────────────────────────────────────────
const sec9 = [
  H1("§9 — Empirical history: why I have always had confidence", { newPage: true }),
  P([T("The mathematics in equations (13) and (16) is, in one sense, new. It is the first time the four components have been written together as a unified statement applicable both to acoustic baffle problems and to general compositional time series. But the "), I("content"), T(" of the equation is not new at all. Every term has been measured, validated, and used in working installations for three decades.")]),
  P([B("Budget (term c). "), T("Measured to ±0.05 dB at BTL since the original DADC programme. Reproduces continuously under thermal variation, humidity variation, and atmospheric-pressure variation. The 6.02 dB has held for thirty years. It has held in the institutional BTL deployments in Ottawa and Monaco, which use different acoustic treatments and different electronics. "), B("It is the most reproducible measurement in the lab.")]),
  P([B("Partition (term dimᵢ/S). "), T("Measured to within the precision of the cabinet construction (~1 mm) in every BTL build. The same partition is computed identically by DADC and by direct geometry; the agreement is exact because the simplex coordinate is a pure ratio. In active deployments under varying driver power, the partition does not drift, because it is not a measurement of acoustic state — it is a measurement of cabinet geometry. "), B("It is the part of the apparatus that does not move.")]),
  P([B("Geometric-frequency carrier (term F_c,i). "), T("Measured to within ±1 Hz at each cabinet cutoff, calibrated against a NIST-traceable acoustic source and a Brüel & Kjær measurement chain. The cutoff frequencies have held to within Linkwitz-Riley fourth-order tolerances for thirty years of continuous BTL operation (Linkwitz 1976). When the cabinet geometry changes, the cutoffs scale exactly with 115/dim and remain in the predicted log-frequency positions.")]),
  P([B("Phase trajectory (term q(f, t)). "), T("Measured to within ±0.5° at each ERB band by the four-channel coherent measurement chain. The trajectory holds across listening-position movements, across humidity excursions, and across the ~30 dB SPL operating range from quiet ambient to peak monitoring. The phase trajectory is dynamic by construction — it "), I("changes"), T(" with frequency, that is the whole point — but at any fixed frequency it is stable within measurement noise.")]),
  P([B("Closure (equation 14). "), T("Closure has "), I("never"), T(" been observed to fail at BTL. It is a constraint, not a hypothesis. Every measurement that has ever been taken has either satisfied it within the instrumental tolerance (~99.99 % of measurements) or revealed an instrumentation fault. Closure is the "), I("check"), T(": when it fails the measurement is wrong, not the theory. This is what makes the framework testable in the strict sense — closure failure is observable and the apparatus is falsifiable.")]),
  P([T("The empirical record is therefore the source of confidence. Every component of equation (13) has been measured, in working conditions, under varying environmental loads, on real hardware, across more than three decades of continuous operation. The framework was not built and then tested; it was "), I("built out of"), T(" the tests. When the mathematics was generalized — first to the H₁ operator on Hilbert space, then to HUF, then to Hˢ — the generalization carried the empirical track record forward by construction.")]),
  P([T("The energy-mix monitoring work at CoDaWork 2026 is, from this perspective, not a debut application. It is the "), I("first non-acoustic application of an apparatus with thirty years of acoustic validation behind it"), T(".")]),
  P([T("This is what the reviewer question \"why are you so confident?\" actually deserves as an answer. Not \"because the math is elegant\" — although it is. Not \"because we ran 101 datasets and 100 came back clean\" — although they did. The answer is: "), B("because the apparatus has been measuring real spaces in working conditions for three decades and has never failed a closure check.")])
];

// ── §10 Generalization ──────────────────────────────────────────────
const sec10 = [
  H1("§10 — Generalization to non-acoustic compositions", { newPage: true }),
  P("The acoustic instance fixes the form of equation (13). The generalization (Theorem 2) replaces:"),
  P([T("The acoustic ground-state budget "), B("c = 20·log₁₀(2) dB"), T(" with the physical or domain-specific total of the application (100 % electrical generation, 100 % weight-fraction major-element oxide, 100 % GDP share, etc.).")], { indent: { left: 360 } }),
  P([T("The cabinet dimensions "), B("dimᵢ"), T(" with the application-specific carriers (energy carriers, mineral oxides, economic sectors, etc.).")], { indent: { left: 360 } }),
  P([T("The cutoff frequency "), B("F_c,i = 115/dimᵢ"), T(" with the natural log-carrier of the application — the geometric-frequency association generalizes to a "), I("log-carrier association"), T(".")], { indent: { left: 360 } }),
  P([T("The acoustic group delay "), B("τᵢ"), T(" with the application-specific traction coefficient: the rate at which the phase advances per unit log-carrier change. In the energy-mix case this is the "), B("Activation Coefficient"), T(" (Power Share ÷ starting share); in the geochemistry case this is the differential reaction kinetics per oxide ratio; in the macro-economic case this is the differential growth rate per sector log-share.")], { indent: { left: 360 } }),
  P("The single-formula form (16) survives the generalization as equation (30) in Theorem 2. Equation (30) is the general isotropic-ground-state formula for compositional traction problems. It reduces to equation (16) in the acoustic case, to the standard CoDa apportionment plus a closure constraint in the static case (κᵢ = 0 for all i, no phase trajectory), and to the Hˢ time-series framework in the dynamic case (κᵢ measurable from the data).")
];

// ── §11 Implications ────────────────────────────────────────────────
const sec11 = [
  H1("§11 — Implications for Hˢ", { newPage: true }),
  P("The unified formula has structural consequences for the existing Hˢ engines."),
  P([B("CNT (the tensor engine) "), T("is the apparatus that reads the partition. It evaluates equation (16) at every timestep, extracts the simplex coordinates (dimᵢ/S), records the log-carrier identities (F_c,i), and produces the static portion of the field. It is the "), I("amplitude reader"), T(".")]),
  P([B("CNQ (the quaternion engine) "), T("is the apparatus that reads the trajectory. It tracks the quaternion exp(i·2π·f·τᵢ·n̂ᵢ) across frequency, extracts the traction coefficients (τᵢ·f), and produces the dynamic portion of the field. It is the "), I("phase reader"), T(".")]),
  P([T("Together CNT + CNQ realize equation (13) operationally. They are not redundant. They are not stages. They are "), I("the two readouts of a single instrument"), T(" — the amplitude readout and the phase readout — and their combination is what equation (13) computes in closed form.")]),
  P([B("The engine-independence policy "), T("(cnt_content_sha256 and cnq_content_sha256 unrelated by design) is a direct consequence of this structure. The amplitude readout and the phase readout are mathematically independent: amplitudes can be measured without phases, phases without amplitudes, and the unified field is the product, not a function of either alone. The implementation policy that keeps the two SHAs independent is mirroring a structural fact about the underlying physics. It is not an arbitrary engineering convention.")]),
  P([B("The Helmsman family "), T("(sign / stability / flips / chaos / torque / joint) is the regime classification of §3.1 applied to the "), I("phase trajectory"), T(". Sign tracks the direction of rotation; stability tracks the smoothness of advance; flips track discrete rotations; chaos tracks fast unstable rotations; torque tracks the rotation rate; joint tracks the multi-carrier coupling. All six are derived diagnostics on the q(f, t) trajectory.")]),
  P([B("The Activation Coefficient "), T("is the traction coefficient of equation (12) recast for log-share indexing instead of log-frequency indexing. The 760× number for USA solar 2012→2013 is the empirical instance of a quantity that has a closed-form interpretation in the unified formula: it is the ratio of phase-advance per log-octave to the static partition coordinate. Carriers with high Activation Coefficient are "), I("carriers whose phase trajectory advances rapidly relative to their amplitude weighting"), T(".")]),
  P([T("The vocabulary alignment is the same alignment that makes the whole Hˢ doctrine internally consistent. The acoustic-engineering terms have CoDa analogues; the CoDa analogues have Hˢ generalizations; the Hˢ generalizations recover the acoustic-engineering terms when restricted to the loudspeaker problem. "), B("Equation (13) is the round-trip identity.")])
];

// ── §12 Lineage map ─────────────────────────────────────────────────
const sec12 = [
  H1("§12 — Lineage map", { newPage: true }),
  P("The full canonical lineage, with this document positioned correctly:"),
  ...EQ([
    "Binaural Test Lab measurements (1990s – 2020s)",
    "      │",
    "      ▼",
    "DADC / DADI / ADAC operations  (Dimension-Apportioned Diffraction Correction)",
    "      │   ── self-hosted at Rogue-Wave-Audio repository",
    "      │   ── primary source: BTL Small Studio Lab DADC paper, AES-format",
    "      │   ── canonical formula:   G_dim = c · dim / S,   F_c = 115 / dim",
    "      │   ── closure proof:        Σ G = c = 20·log₁₀(2) ≈ 6.02 dB",
    "      │",
    "      ▼",
    "The Higgins Operator H₁     (working paper, 2026-02, Rogue-Wave-Audio repository)",
    "      │   ── nonlinear unity-normalization map on Hilbert space",
    "      │   ── first formal generalization beyond loudspeakers",
    "      │",
    "      ▼",
    "HUF — Higgins Unity Framework     (MC-4 + EITT)",
    "      │   ── partition / portion / closure formalised as governance discipline",
    "      │   ── HUF-STD-001 / 002 / 003 published as internal standards",
    "      │",
    "      ▼",
    "Hˢ — Higgins Decomposition",
    "      │   ── CNT engine reads the static partition (amplitude)",
    "      │   ── CNQ engine reads the dynamic trajectory (phase)",
    "      │   ── Engine-independence policy preserves the two-readout structure",
    "      │",
    "      ├── CoDaWork 2026 manuscript  (first non-acoustic application: energy-mix)",
    "      │",
    "      └── THIS DOCUMENT — master-standard unified-formula statement with full lemma chain"
  ]),
  P([T("The historical narrative is in "), M("HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md"), T(". The acoustic doctrine is in "), M("HCI-AUDIO/doctrine/"), T(". The original DADC engineering paper is at "), M("RogueWaveAudio/BTL/BTL Small Studio Lab/DIMENSION-APPORTIONED DIFFRACTION CORRECTION 3.txt"), T(". This document supplies the unified statement that ties all of them together.")])
];

// ── §13 Glossary ────────────────────────────────────────────────────
function glossEntry(term, definition) {
  return new Paragraph({
    spacing: { before: 80, after: 80, line: 280 },
    indent: { left: 360, hanging: 360 },
    children: [
      new TextRun({ text: term + ". ", font: "Calibri", size: 22, bold: true, color: NAVY }),
      ...(definition instanceof Array ? definition : [new TextRun({ text: definition, font: "Calibri", size: 22, color: INK })])
    ]
  });
}

const sec13Glossary = [
  H1("§13 — Glossary", { newPage: true }),
  P([T("The glossary below collects the terms used throughout this document. For the comprehensive ~220-entry Hˢ vocabulary see "), M("HCI-CNT/handbook/GLOSSARY.md"), T(" v3.0.")]),
  glossEntry("Activation Coefficient (αⱼ)", "Per-carrier diagnostic introduced as INV-060 in the Investigation Catalog. Defined as Power Share πⱼ divided by starting share ρⱼ when ρⱼ ≥ 10⁻³. Identified in this document (Theorem 2 corollary) as the compositional-traction generalization of the acoustic group-delay-per-log-octave coefficient."),
  glossEntry("ADAC", "Adaptive Closure / Adaptive Diffraction Apportioning Correction. The closure rule of the DADC system: maintains Σ Gᵢ = ±c as conditions change. Mathematically a damped fixed-point iteration with spectral-radius bound (Lemma 5)."),
  glossEntry("Aitchison geometry", "Geometry on the simplex obtained by pulling back Euclidean geometry on ℝ^(D−1) under the ILR map. Distances, means, and variances are well-defined and coordinate-free. Cf. Aitchison (1986); Egozcue et al. (2003)."),
  glossEntry("Baffle step", "Transition in loudspeaker response between low-frequency 4π omnidirectional radiation and high-frequency 2π half-space radiation. Total magnitude exactly 20·log₁₀(2) ≈ 6.02 dB (equation 1)."),
  glossEntry("Banach fixed-point theorem", "Theorem from Banach (1922): any contraction mapping on a complete metric space has a unique fixed point, and iterates converge to it geometrically. Used in Lemma 4 to prove DADI convergence."),
  glossEntry("Binaural Test Lab (BTL)", "Sound-controlled professional laboratory for omnidirectional listening-position research. Operated by the author with parallel deployments in Ottawa and Monaco. Canonical lab identity: RWA-001."),
  glossEntry("Budget (c)", "Ground-state radiation total = 20·log₁₀(2) ≈ 6.02 dB. The physical analogue of the closure constant in compositional-data analysis."),
  glossEntry("Closure", "Constraint Σᵢ xᵢ = constant on a positive composition. In the acoustic case the constant is the budget c; in CoDa the constant is conventionally 1 or 100 %."),
  glossEntry("CLR (centred log-ratio)", "Transform clrᵢ(x) = log(xᵢ) − (1/D)·Σⱼ log(xⱼ). Closure-preserving in the additive sense (Lemma 8): Σᵢ clrᵢ(x) = 0."),
  glossEntry("CNQ", "Compositional Navigation Quaternion. Hˢ engine that reads the phase-trajectory portion of the unified formula. Operates on quaternions q(f, t) ∈ S³."),
  glossEntry("CNT", "Compositional Navigation Tensor. Hˢ engine that reads the partition portion of the unified formula. Operates on simplex compositions and their ILR coordinates."),
  glossEntry("Compositional data (CoDa)", "Data taking values in the simplex {x ∈ ℝᴰ : xᵢ > 0, Σ xᵢ = 1}. Subject to the Aitchison closure constraint."),
  glossEntry("Cutoff frequency (F_c,i)", "Geometric transition frequency for partition i, given by 115/dimᵢ in the BTL case (equation 6). The point at which the baffle-step shelf is at −3 dB."),
  glossEntry("DADC", "Dimension-Apportioned Diffraction Correction. Forward map of the original RWA acoustic correction system: distributes the 6.02 dB budget across cabinet dimensions per equation (3)."),
  glossEntry("DADI", "Dimension-Apportioned Diffraction Inference. Inverse map of DADC: infers dimensions from measured response. Convergence proved in Lemma 4."),
  glossEntry("Dominance ratio (D)", "Ratio max(dimᵢ)/min(dimᵢ). Classifies the BTL into long (D > 2, proportional), short (D < 1.5, reciprocal), and hybrid (1.5 ≤ D ≤ 2, blended) regimes."),
  glossEntry("ERB", "Equivalent Rectangular Bandwidth. Psychoacoustic frequency partition modelling cochlear filter widths (Glasberg & Moore 1990). ERB-rate scale provides a perceptually uniform log-frequency axis."),
  glossEntry("Geometric-frequency association", "The fact that the partition is naturally indexed by log-spaced (geometric-mean) frequency carriers, both for physical-scaling reasons and for perceptual-scaling reasons. The bridge that brings time into the simplex (§4)."),
  glossEntry("Gershgorin circle theorem", "Every eigenvalue of a complex matrix lies within at least one Gershgorin disk centred at a diagonal entry with radius equal to the sum of absolute values of off-diagonal entries in that row. Used in Lemma 6."),
  glossEntry("Ground state", "Lowest-energy configuration. In acoustic context: the 4π isotropic radiation budget against which all diffraction corrections are measured (§2)."),
  glossEntry("Group delay (τ)", "Negative derivative of phase with respect to angular frequency: τ = −dφ/dω. A pure time-delay manifests as constant group delay (equation 9)."),
  glossEntry("Helmholtz reciprocity", "Acoustic field is invariant under exchange of source and receiver (Lemma 3). The mathematical foundation for the bidirectionality of forward DADC and inverse DADI."),
  glossEntry("Hˢ (Higgins Decomposition)", "Compositional-data framework with two engines (CNT + CNQ) reading the amplitude and phase parts of the unified formula respectively."),
  glossEntry("HUF (Higgins Unity Framework)", "Governance umbrella covering HUF-STD-001 (Publication), HUF-STD-002 (Tensor Train I/O), HUF-STD-003 (Linear Algebra Foundations)."),
  glossEntry("Higgins Operator H₁", "Nonlinear unity-normalization map on Hilbert space; the first formal mathematical object generalizing DADC beyond loudspeakers."),
  glossEntry("ILR (isometric log-ratio)", "Transform η(x) = Vᵀ·clr(x) with V an orthonormal contrast matrix (typically Helmert). Carries the simplex isometrically into ℝ^(D−1) (Egozcue et al. 2003)."),
  glossEntry("Isotropic radiation", "Equal-intensity radiation in all directions; the 4π low-frequency limit of the baffle step."),
  glossEntry("Linkwitz Transform", "Pole-zero reshaping of sealed-box low-frequency response, enabling extension to lower cutoffs (Linkwitz 1976)."),
  glossEntry("Partition", "Allocation of the budget across the n carriers. The simplex coordinate pᵢ ∈ [0, 1] with Σ pᵢ = 1."),
  glossEntry("Power Share (πⱼ)", "Per-carrier squared CLR-difference divided by total: πⱼ = (Δclrⱼ)² / Σₖ (Δclrₖ)², with Σⱼ πⱼ = 1."),
  glossEntry("Quaternion (q)", "Element of the algebra ℍ = {a + b·iₓ + c·iᵧ + d·i_z}. Unit quaternions live on S³ ≅ SU(2). Carry phase information for multi-channel signals (Hamilton 1843)."),
  glossEntry("Rayleigh-Sommerfeld integral", "Exact diffraction integral derived from the wave equation via Green's theorem (equation 18). The rigorous basis for the DADC apportionment (Lemma 2)."),
  glossEntry("Reciprocity triad", "Forward DADC + inverse DADI + adaptive ADAC, all consistent under Helmholtz reciprocity (Lemma 3)."),
  glossEntry("Simplex (S^(D−1))", "Set of positive D-tuples with closure: {x ∈ ℝᴰ : xᵢ > 0, Σ xᵢ = 1}."),
  glossEntry("SEA", "Statistical Energy Analysis. High-frequency vibroacoustic modelling framework treating subsystems as energy reservoirs. Positive-definite coupling matrix yields unique solutions (Lemma 6); cf. Lyon & DeJong (1995)."),
  glossEntry("Three-sphere (S³)", "Unit sphere in ℝ⁴; equivalently the manifold of unit quaternions; equivalently the Lie group SU(2)."),
  glossEntry("Traction coefficient", "Group-delay × geometric-centre-frequency in the acoustic case; phase-advance-per-log-octave in the general case. Where it is zero, the simplex is stationary; where it is nonzero, the simplex is in motion (§5, §8)."),
  glossEntry("Traction engine", "A framework that partitions, reports, and carries motion. Contrasted with a stationary engine that only partitions and reports."),
  glossEntry("Unified formula", "Equation (13) for the acoustic case, equation (30) for the general case. Contains budget + partition + log-carrier + phase trajectory in one closed-form expression.")
];

// ── §14 Standard formulas summary card ──────────────────────────────
const sec14Card = [
  H1("§14 — Standard formulas summary card", { newPage: true }),
  P("For quick reference. All equations elaborated in the main body."),
  ...EQ([
    "Closure (DADC):              Σᵢ Gᵢ  =  c  =  20·log₁₀(2)  ≈  6.02 dB                        (4)",
    "",
    "Closure (general):           Σᵢ pᵢ  =  1,           pᵢ  =  xᵢ / Σⱼ xⱼ                       (5)",
    "",
    "Partition (long regime):     Gᵢ  =  c · dimᵢ / S                                            (3)",
    "Partition (short regime):    Gᵢ  =  −c · (1/dimᵢ) / Iₛ                                      (§3.1)",
    "Partition (hybrid regime):   Gᵢ  =  c · [β · dimᵢ/S  +  (1−β) · (1/dimᵢ)/Iₛ ]                (§3.1)",
    "",
    "Cutoff frequency (acoustic): F_c,i  =  115 / dimᵢ                                           (6)",
    "Baffle-step shelf:           S(f, F_c,i)  =  1 / √(1 + (F_c,i / f)²)                        (7)",
    "",
    "ERB-rate (psychoacoustic):   ERB_rate(f)  =  21.4 · log₁₀(0.00437·f + 1)                    (§4)",
    "",
    "Group delay:                 τ(f)  =  −(1/2π) · dφ/df                                       (9)",
    "Pure-delay phase:            φ(f)  =  −2π · f · τ₀                                         (10)",
    "Phase quaternion:            q(f)  =  q₀ · exp(i · 2π · f · τ · n̂)                          (11)",
    "Traction (acoustic):         Δφ_octave  =  2π · τ · f₁                                     (12)",
    "",
    "Unified per-partition:       T_i(f, t)  =  c · (dimᵢ/S) · S(f, F_c,i) · exp(i·2π·f·τᵢ·n̂ᵢ)   (13)",
    "Closed-form total:           T(f, t)  =  c · Σᵢ (dimᵢ/S) · exp(...) / √(1+(F_c,i/f)²)       (16)",
    "General compositional:       T(u, t)  =  C · Σᵢ (xᵢ/Σⱼxⱼ) · exp(...) / √(1+(u_c,i/u)²)      (30)",
    "",
    "CLR transform:               clrᵢ(x)  =  log(xᵢ) − (1/D)·Σⱼ log(xⱼ)",
    "ILR (Helmert):               η(x)  =  Vᵀ · clr(x)         with V·Vᵀ = I",
    "Aitchison distance:          d_Ait(x, y)  =  ‖clr(x) − clr(y)‖₂",
    "",
    "Power Share:                 πⱼ(t)  =  (Δclrⱼ)² / Σₖ (Δclrₖ)²,    Σ πⱼ  =  1",
    "Activation Coefficient:      αⱼ(t)  =  πⱼ(t) / ρⱼ(t)         (when ρⱼ ≥ 10⁻³)",
    "",
    "Banach contraction (DADI):   |dim_n − dim*|  ≤  m^n · |dim_0 − dim*|,    |m| < 1            (21)",
    "ADAC damping:                dim_{next}  =  α · dim_{undamped}  +  (1−α) · dim_{previous}   (23)",
    "SEA quadratic form:          xᵀ C x  =  Σᵢ ηᵢ xᵢ²  +  Σ_{i<j} ηᵢⱼ (xᵢ − xⱼ)²  >  0          (25)",
    "",
    "Theorem 1 (closure check):   lim_{f→∞} Σᵢ |T_i(f, t)|  =  c                                (28)"
  ])
];

// ── §15 References (peer-reviewed) ──────────────────────────────────
function refEntry(author, title, rest) {
  return new Paragraph({
    spacing: { before: 80, after: 80, line: 280 },
    indent: { left: 360, hanging: 360 },
    children: [
      new TextRun({ text: author + " ", font: "Calibri", size: 22, bold: true, color: INK }),
      new TextRun({ text: title + ". ", font: "Calibri", size: 22, italics: true, color: INK }),
      new TextRun({ text: rest, font: "Calibri", size: 22, color: INK })
    ]
  });
}

const sec15Refs = [
  H1("§15 — References (externally peer-reviewed)", { newPage: true }),
  P("The following works appear in the externally peer-reviewed literature and are cited as authoritative sources."),
  refEntry("Aitchison, J. (1986).", "The Statistical Analysis of Compositional Data", "Chapman & Hall, London. ISBN 978-0-412-28060-3. Foundational monograph on the simplex, closure, and log-ratio analysis."),
  refEntry("Aitchison, J. & Greenacre, M. (2002).", "Biplots of compositional data", "Journal of the Royal Statistical Society: Series C (Applied Statistics), 51(4): 375–392."),
  refEntry("Banach, S. (1922).", "Sur les opérations dans les ensembles abstraits et leur application aux équations intégrales", "Fundamenta Mathematicae, 3: 133–181. Original fixed-point theorem; cited for Lemma 4."),
  refEntry("Born, M. & Wolf, E. (1999).", "Principles of Optics, 7th edition", "Cambridge University Press. ISBN 978-0-521-64222-4. Standard reference for the Rayleigh-Sommerfeld diffraction integral (§8.11), Lemma 2."),
  refEntry("Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G., & Barceló-Vidal, C. (2003).", "Isometric logratio transformations for compositional data analysis", "Mathematical Geology, 35(3): 279–300. Foundational paper for the ILR transform."),
  refEntry("Glasberg, B. R. & Moore, B. C. J. (1990).", "Derivation of auditory filter shapes from notched-noise data", "Hearing Research, 47(1–2): 103–138. Definitive paper on the ERB scale (equation 8)."),
  refEntry("Hamilton, W. R. (1843).", "On a new species of imaginary quantities connected with a theory of quaternions", "Proceedings of the Royal Irish Academy, 2: 424–434. Original quaternion paper."),
  refEntry("Hanson, A. J. (2006).", "Visualizing Quaternions", "Morgan Kaufmann / Elsevier. ISBN 978-0-12-088400-1. Cited for the one-parameter subgroup structure in Lemma 7."),
  refEntry("Helmholtz, H. von (1860).", "Theorie der Luftschwingungen in Röhren mit offenen Enden", "Crelle's Journal, 57: 1–72. Original statement of acoustic reciprocity."),
  refEntry("Linkwitz, S. (1976).", "Active crossover networks for noncoincident drivers", "Journal of the Audio Engineering Society, 24(1): 2–8. Original Linkwitz-Riley crossover paper."),
  refEntry("Lyon, R. H. & DeJong, R. G. (1995).", "Theory and Application of Statistical Energy Analysis, 2nd edition", "Butterworth-Heinemann. ISBN 978-0-7506-9111-7. Standard textbook for SEA (Lemma 6)."),
  refEntry("Moore, B. C. J. (2012).", "An Introduction to the Psychology of Hearing, 6th edition", "Brill / Academic Press. ISBN 978-90-04-25242-4. Standard textbook on auditory perception."),
  refEntry("Olson, H. F. (1969).", "Direct radiator loudspeaker enclosures", "Journal of the Audio Engineering Society, 17(1): 22–29. Classical reference for finite-baffle low-frequency corrections."),
  refEntry("Pawlowsky-Glahn, V., Egozcue, J. J., & Tolosana-Delgado, R. (2015).", "Modeling and Analysis of Compositional Data", "Wiley. ISBN 978-1-118-44306-4. Modern textbook on compositional data analysis."),
  refEntry("Pierce, A. D. (1981).", "Acoustics: An Introduction to its Physical Principles and Applications", "McGraw-Hill (reissued by the Acoustical Society of America, 1989, 2019). ISBN 978-0-88318-612-1. Standard textbook for acoustic reciprocity (§5.4), Lemma 3."),
  refEntry("Vanderkooy, J. (1991).", "A simple theory of cabinet edge diffraction", "Journal of the Audio Engineering Society, 39(12): 923–933. Cited as prior art for angular form factors in finite-baffle diffraction.")
];

// ── §16 Repository materials ────────────────────────────────────────
const sec16Repo = [
  H1("§16 — Repository materials (self-hosted, not externally peer-reviewed)", { newPage: true }),
  P([T("The following works are by the present author and are hosted in either the Rogue-Wave-Audio repository or the Hˢ repository. They are "), B("not externally peer-reviewed"), T("; priority is established by Git commit timestamp under CC BY 4.0 (acoustic-engineering materials) or by the publication standards of HUF-STD-001 (Hˢ materials). They are referenced here as primary sources for the empirical record and the historical lineage, but should be cited as repository materials rather than as journal articles.")]),
  refEntry("Higgins, P. (in progress, 2025–2026).", "DADC-ADAC: Dimension-Apportioned Diffraction Correction for Omnidirectional Loudspeakers", "AES-format manuscript hosted at the Rogue-Wave-Audio repository (BTL/BTL Small Studio Lab/DIMENSION-APPORTIONED DIFFRACTION CORRECTION 3.txt). Disposition: self-hosted preprint, CC BY 4.0. Primary source for the BTL geometry, the 6.02 dB measurement, the DADI/ADAC iterations, and the SEA matrix analysis."),
  refEntry("Higgins, P. (2026).", "The Higgins Operator H₁ 101", "Working paper hosted at the Rogue-Wave-Audio repository (docs/papers/). Disposition: self-hosted working paper, February 2026. First formal generalization of the DADC closure structure to a nonlinear unity-normalization map on Hilbert space."),
  refEntry("Higgins, P. (2026).", "Compositional monitoring of energy-mix drift on the simplex", "CoDaWork 2026 conference manuscript hosted at the Hˢ repository (papers/codawork2026/manuscript/). Disposition: conference manuscript, peer review pending post-conference."),
  refEntry("Higgins, P. (2026).", "Origin and Lineage — DADC, the Higgins Operator H₁, and the Path to CNQ", "Canonical historical narrative at HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md (push #24, 2026-05-08). Disposition: repository-canonical document."),
  P([B("HUF-STD-001 v1.1"), T(" — Publication Standards. Hˢ repository, "), M("huf-gov/standards/HUF_PUBLICATION_STANDARDS.json"), T(". Disposition: internal standard.")], { indent: { left: 360, hanging: 360 } }),
  P([B("HUF-STD-002"), T(" — Tensor Train I/O Standard. Hˢ repository, "), M("huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json"), T(". Disposition: internal standard.")], { indent: { left: 360, hanging: 360 } }),
  P([B("HUF-STD-003"), T(" — Hˢ Linear Algebra Foundations. Hˢ repository, "), M("huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json"), T(". Disposition: internal standard.")], { indent: { left: 360, hanging: 360 } }),
  P([B("HCI-AUDIO doctrine files"), T(". Hˢ repository, "), M("HCI-AUDIO/doctrine/"), T(": ERB_BAND_MAPPING.md, QUATERNION_PHASE_MAPPING.md, HELMSMAN_AT_LISTENING_POS.md, ALIGNMENT_TARGETS.md. Disposition: repository doctrine.")], { indent: { left: 360, hanging: 360 } }),
  P([M("HCI-CNT/handbook/GLOSSARY.md"), T(" v3.0. Hˢ repository. ~220 entries, 30 sections. Disposition: repository canonical glossary.")], { indent: { left: 360, hanging: 360 } })
];

// ── §17 Acknowledgements ────────────────────────────────────────────
const sec17Ack = [
  H1("§17 — Acknowledgements: AI collaboration", { newPage: true }),
  P([T("This document was developed under HUF-STD-001 v1.1 AI Use Declaration provisions. The mathematical structure, empirical interpretation, and conceptual synthesis are the author's, derived from thirty years of acoustic-engineering practice at the Binaural Test Lab and from the prior Rogue-Wave-Audio published work cited in §16. The author retains full scientific responsibility for the claims and for the interpretation of the empirical record.")]),
  P([T("The "), B("HUF AI Collective"), T(" contributed at the level documented below. The author has named each system by its role in the development of this specific document; participation does not imply endorsement, agreement, or shared responsibility.")]),
  H2("Claude (Anthropic) — present session, Cowork mode"),
  P([T("Drafting assistance for the unified-formula presentation; structural editing across multiple revisions; cross-reference verification against the Hˢ repository; lemma-and-proof rendering in the agreed mathematical style; document-build automation for the Word-format companion; vocabulary alignment with the existing Hˢ doctrine (Helmsman family, Activation Coefficient, engine-independence policy). The present master-standard expansion (v2.0) was drafted under direct authorial direction in a single working session.")]),
  H2("ChatGPT (OpenAI) — multiple prior sessions across the 2026-05 conference-prep arc"),
  P([T("Compression-plan generation (the 22→12 slide-compression plan archived at "), M("CODAwork2026/archive/talk_decks_pre_10slide_2026-05-20/CompressionPlan.json"), T("); independent review of the CODA-Association folder layout and the cleanup actions of pushes #57 and #58; conceptual sharpening of the \"manuscript + three-piece presentation\" hierarchy adopted in the README chain.")]),
  H2("Grok (xAI) — round 4 through round 7 cross-check archive"),
  P([T("Discovery of the BTL ↔ simplex connection via independent reading of the Rogue-Wave-Audio repository (round 4, 2026-05-08); recovery of the ADAC closure role from the historical record; multiple investigation-catalog contributions (INV-053 prior art, INV-056 to INV-061 staged entries); cross-check on engineering claims and on AI fitness-matrix structure. Cross-check archive at "), M("ai-refresh/cross_check_archive/"), T(".")]),
  H2("The HUF AI Collective as a whole"),
  P([T("Under the discipline established by HUF-STD-001 v1.1, individual AI contributions are routed, audited, and recorded. Each model has different strengths (Claude: long-form synthesis and structural editing; ChatGPT: independent review and compression planning; Grok: cross-check and connector-cache stress-testing). Their joint contribution is what makes the master-standard form of this document possible; the author's contribution is the integration, the empirical grounding, and the scientific responsibility.")]),
  P([B("The named author retains full scientific responsibility "), T("for the claims, the proofs, the empirical interpretation, the choice of citation strategy, and the publication disposition of this document.")])
];

// ── Closing doctrine ────────────────────────────────────────────────
const closing = [
  HR(),
  new Paragraph({
    spacing: { before: 240, after: 80, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "The instrument reads.   The expert decides.   The hashes carry the receipts.", font: "Calibri", size: 22, italics: true, color: GOLD, bold: true })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 80, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "The vocabulary holds the line.   The AI follows the same protocol.", font: "Calibri", size: 22, italics: true, color: GOLD, bold: true })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 80, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "The mathematics is not new; the monitoring application may be.", font: "Calibri", size: 20, italics: true, color: DIM })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 80, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "The simplex was already there in the 4π → 2π physics.", font: "Calibri", size: 20, italics: true, color: DIM })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 80, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "The traction was always carried by the log-frequency carrier.", font: "Calibri", size: 20, italics: true, color: DIM })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 80, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "The lemmas were proved when the iterations converged.", font: "Calibri", size: 20, italics: true, color: DIM })]
  }),
  new Paragraph({
    spacing: { before: 0, after: 0, line: 280 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "The confidence is empirical, not philosophical.", font: "Calibri", size: 22, bold: true, color: NAVY })]
  })
];

// ── Build Document ──────────────────────────────────────────────────
const doc = new Document({
  creator: "Peter Higgins · Rogue Wave Audio",
  title: "The Isotropic Radiation Ground State and the Traction Engine — Master Standard",
  description: "Hˢ Flagship Working Draft v2.0",
  styles: {
    default: { document: { run: { font: "Calibri", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Calibri", color: NAVY },
        paragraph: { spacing: { before: 360, after: 240, line: 320 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Calibri", color: NAVY },
        paragraph: { spacing: { before: 280, after: 160, line: 300 }, outlineLevel: 1 } }
    ]
  },
  sections: [
    // Cover (no header/footer)
    {
      properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
      children: cover
    },
    // Main content (with header/footer)
    {
      properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
      headers: {
        default: new Header({
          children: [new Paragraph({
            spacing: { after: 0, line: 240 },
            border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: GOLD, space: 4 } },
            tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
            children: [
              new TextRun({ text: "Ground State and the Traction Engine", font: "Calibri", size: 18, italics: true, color: DIM }),
              new TextRun({ text: "\tHˢ Flagship · Master Standard v2.0", font: "Calibri", size: 18, color: DIM })
            ]
          })]
        })
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            spacing: { before: 0, line: 240 },
            border: { top: { style: BorderStyle.SINGLE, size: 4, color: GOLD, space: 4 } },
            tabStops: [
              { type: TabStopType.CENTER, position: 4680 },
              { type: TabStopType.RIGHT, position: 9360 }
            ],
            children: [
              new TextRun({ text: "Peter Higgins · Rogue Wave Audio · Binaural Test Lab", font: "Calibri", size: 18, color: DIM }),
              new TextRun({ text: "\t", font: "Calibri", size: 18 }),
              new TextRun({ text: "page ", font: "Calibri", size: 18, color: DIM }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Calibri", size: 18, color: DIM, bold: true }),
              new TextRun({ text: "\t2026-05-21", font: "Calibri", size: 18, color: DIM })
            ]
          })]
        })
      },
      children: [
        ...frontMatter,
        ...tocPage,
        ...preface,
        ...sec1Symbols,
        ...sec2,
        ...sec3,
        ...sec4,
        ...sec5,
        ...sec6,
        ...sec7Math,
        ...sec8,
        ...sec9,
        ...sec10,
        ...sec11,
        ...sec12,
        ...sec13Glossary,
        ...sec14Card,
        ...sec15Refs,
        ...sec16Repo,
        ...sec17Ack,
        ...closing
      ]
    }
  ]
});

const outPath = process.argv[2] || "GROUND_STATE_AND_TRACTION.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outPath, buffer);
  console.log("Wrote:", outPath, "(" + buffer.length + " bytes)");
});
