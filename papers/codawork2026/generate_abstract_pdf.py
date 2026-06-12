#!/usr/bin/env python3
"""Generate A4 PDF of CoDaWork 2026 abstract submission."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable
)

OUTPUT = "CoDaWork2026_Abstract_Higgins.pdf"

# A4 page with generous margins
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    topMargin=25*mm,
    bottomMargin=20*mm,
    leftMargin=25*mm,
    rightMargin=25*mm,
    title="CoDaWork 2026 Abstract — Higgins Decomposition",
    author="Peter Higgins",
    subject="Abstract submission for CoDaWork 2026, Coimbra",
)

# --- Styles ---
DARK = HexColor("#1a1a1a")
MID = HexColor("#444444")
ACCENT = HexColor("#2E5090")

title_style = ParagraphStyle(
    "Title",
    fontName="Times-Bold",
    fontSize=14,
    leading=18,
    alignment=TA_CENTER,
    textColor=DARK,
    spaceAfter=6,
)

author_style = ParagraphStyle(
    "Author",
    fontName="Times-Roman",
    fontSize=11,
    leading=14,
    alignment=TA_CENTER,
    textColor=DARK,
    spaceAfter=2,
)

affiliation_style = ParagraphStyle(
    "Affiliation",
    fontName="Times-Italic",
    fontSize=10,
    leading=13,
    alignment=TA_CENTER,
    textColor=MID,
    spaceAfter=2,
)

contact_style = ParagraphStyle(
    "Contact",
    fontName="Times-Roman",
    fontSize=9,
    leading=12,
    alignment=TA_CENTER,
    textColor=ACCENT,
    spaceAfter=4,
)

keyword_label_style = ParagraphStyle(
    "KeywordLabel",
    fontName="Times-Bold",
    fontSize=9.5,
    leading=12,
    alignment=TA_LEFT,
    textColor=DARK,
    spaceAfter=8,
)

body_style = ParagraphStyle(
    "Body",
    fontName="Times-Roman",
    fontSize=10.5,
    leading=14,
    alignment=TA_JUSTIFY,
    textColor=DARK,
    spaceAfter=8,
    firstLineIndent=0,
)

body_indent_style = ParagraphStyle(
    "BodyIndent",
    parent=body_style,
    firstLineIndent=12,
)

footer_style = ParagraphStyle(
    "Footer",
    fontName="Times-Roman",
    fontSize=8.5,
    leading=11,
    alignment=TA_CENTER,
    textColor=MID,
    spaceBefore=6,
)

# --- Content ---
story = []

# Conference header
story.append(Paragraph(
    "CoDaWork 2026 — 11<super>th</super> International Workshop on Compositional Data Analysis",
    ParagraphStyle("ConfHeader", fontName="Times-Italic", fontSize=9, leading=11,
                   alignment=TA_CENTER, textColor=MID, spaceAfter=12)
))

# Title
story.append(Paragraph(
    "The Higgins Decomposition: a deterministic compositional<br/>"
    "diagnostic on the Aitchison simplex",
    title_style
))

story.append(Spacer(1, 4))

# Author
story.append(Paragraph("Peter Higgins", author_style))
story.append(Paragraph("Independent researcher, Markham, Ontario, Canada", affiliation_style))
story.append(Paragraph(
    "PeterHiggins@RogueWaveAudio.com &nbsp;&nbsp;|&nbsp;&nbsp; "
    "github.com/PeterHiggins19/higgins-decomposition",
    contact_style
))

story.append(Spacer(1, 4))

# Rule
story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#CCCCCC"),
                         spaceAfter=8, spaceBefore=2))

# Keywords
story.append(Paragraph(
    "<b>Keywords:</b> compositional data analysis, Aitchison geometry, simplex, "
    "amalgamation stability, entropy invariance, log-ratio pairs, deterministic "
    "diagnostics, cross-domain composition",
    keyword_label_style
))

# Abstract body — paragraph 1
story.append(Paragraph(
    "This contribution presents a deterministic diagnostic instrument for compositional "
    "data operating entirely within Aitchison geometry on the simplex. The instrument "
    "decomposes into seven sequential operators — simplex closure, variance trajectory, "
    "CLR transform, classification, entropy test, mode synthesis, and report — each "
    "inheriting a determinism axiom: same input, same output, always. Four operators are "
    "standard CoDa operations; two contain open questions for the community.",
    body_style
))

# Paragraph 2
story.append(Paragraph(
    "The instrument has been applied to 25 systems across 18 domains spanning 44 orders "
    "of physical magnitude, including nuclear binding energy, cosmological composition "
    "(Planck 2018), particle physics branching ratios, geochemistry, energy-portfolio "
    "drift, and municipal budgets — all using the same twelve steps with no "
    "domain-specific tuning.",
    body_indent_style
))

# Paragraph 3 — result 1
story.append(Paragraph(
    "Three results are reported. First, classification stability under amalgamation: "
    "across 58 schemes applied to five datasets, classification is preserved in every "
    "case. In cosmological data, two ratio locks corresponding to known conservation "
    "laws survive all amalgamation levels, quantifying what subcompositional merging "
    "hides and what it preserves.",
    body_indent_style
))

# Paragraph 4 — result 2
story.append(Paragraph(
    "Second, entropy invariance under geometric-mean decimation: Shannon entropy on the "
    "simplex varies less than 5% when observations are replaced by pairwise geometric-mean "
    "blocks at compression ratios of 2, 4, and 8 across all natural systems tested. The "
    "geometric mean is the Aitchison centre; this invariance may follow from simplex "
    "geometry, but no proof is offered.",
    body_indent_style
))

# Paragraph 5 — result 3
story.append(Paragraph(
    "Third, a seven-dimensional compositional fingerprint enables cross-domain comparison. "
    "Systems sharing a fingerprint share compositional geometry — a structural homology "
    "detectable without domain knowledge.",
    body_indent_style
))

# Paragraph 6 — open questions
story.append(Paragraph(
    "The instrument is fully reproducible with SHA-256 hash verification. All code and data "
    "are publicly available. Three open questions for CoDaWork: (1) Can the entropy invariance "
    "be proved from Aitchison geometry? (2) Does classification survive ILR substitution for "
    "CLR? (3) Independent validation on CoDa community datasets.",
    body_indent_style
))

# Footer rule
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#CCCCCC"),
                         spaceAfter=4, spaceBefore=2))

# Footer
story.append(Paragraph(
    "Submitted to CoDaWork 2026 — Coimbra, Portugal — June 1–5, 2026<br/>"
    "Preference: oral presentation &nbsp;&nbsp;|&nbsp;&nbsp; Word count: 279",
    footer_style
))

# Build
doc.build(story)
print(f"Generated: {OUTPUT}")
