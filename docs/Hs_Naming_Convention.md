# Hˢ Naming Convention

**Authority:** This document governs all file naming, internal branding, and terminology across the Higgins Decomposition repository. When naming a new file, tool, or document, follow these rules. When encountering legacy names, apply the migration table.

---

## Brand Identity

| Element | Canonical Form | Usage |
|---------|---------------|-------|
| Framework name | Higgins Decomposition | All public-facing text, titles, headers |
| Symbol | Hˢ | Mathematical and inline references |
| Symbol meaning | H-superscript-S — Higgins on the Simplex | First use in any new document |
| Parent project | Higgins Unity Framework (HUF) | Lineage references only — never as current identity |
| Supervisory layer | Hˢ-GOV | Governance and controller references |
| Author | Peter Higgins | All documents |
| Organisation | Rogue Wave Audio | Affiliation and contact |
| Tagline | The instrument reads. The expert decides. The loop stays open. | Closing lines |

---

## File Naming Rules

### Prefixes by Category

| Category | Prefix | Case | Example |
|----------|--------|------|---------|
| Pipeline code | `hs_` | lowercase | `hs_codes.py`, `hs_fingerprint.py` |
| Core engine | `higgins_` | lowercase | `higgins_decomposition_12step.py` |
| Interactive tools | `Hs_` | Title case | `Hs_Spectrum_Analyzer.html` |
| Documents (markdown) | `Hs_` | Title case | `Hs_Learning_Path.md` |
| Documents (docx) | `Higgins_` or `Hs_` | Title case | `Higgins_Decomposition_Reference_v3.0.docx` |
| Machine-readable config | `HS_` | Uppercase | `HS_MACHINE_MANIFEST.json` |
| Experiments | `Hs-NN_` | Hyphenated number | `Hs-01_Gold_Silver/` |
| CoDaWork deliverables | `CoDaWork2026_` | Event prefix | `CoDaWork2026_Speech_GiftRamp.md` |
| Cosmic tools | `cosmic_` | lowercase | `cosmic_future_projection.html` |

### General Rules

- **Underscores** separate words (not hyphens, except in experiment IDs like `Hs-01`)
- **No spaces** in any filename
- **Version numbers** use `_vN.N` suffix: `Reference_v3.0.docx`
- **Experiment results** follow `Hs-NN_results.json` pattern
- **Sub-experiment results** follow `Hs-NN{letter}_results.json`: `Hs-17A_per_drive_results.json`
- **Reports** follow `Hs-NN_report_{lang}.txt` pattern
- **Locale files** use ISO 639-1 codes: `en.json`, `zh.json`, `hi.json`, `pt.json`, `it.json`

---

## Retired Terminology — Migration Table

| Retired Term | Replacement | Context |
|-------------|-------------|---------|
| HUF (as current identity) | Hˢ / Higgins Decomposition | All active references |
| HUF (as lineage) | Higgins Unity Framework (HUF) | Lineage sections only — always qualified |
| HUF-GOV | Hˢ-GOV | Governance layer |
| HUF_Spectrum_Analyzer | Hs_Spectrum_Analyzer | Interactive tool filename |
| CIP (as current methodology) | HVLD (Higgins Vertex Lock Diagnostic) | Active diagnostic references |
| CIP Rules (in historical context) | Retain as-is | Theory/lineage documents — these are historical records |
| CIP_Systems_Primer | Hs_HVLD_Systems_Primer | Renamed reference document |
| Unity (in project name) | Decomposition | Avoid game engine SEO collision |
| PLL | HVLD | All prose, headings, and explanatory text |
| Phase-Locked Loop | Higgins Vertex Lock Diagnostic | Full name replacement |
| PLL vertex | HVLD vertex | Diagnostic terminology |
| PLL lock / PLL lock point | HVLD lock / HVLD lock point | Vertex lock references |
| PLL parabola | HVLD parabola | Quadratic fit references |
| pll_parabola (in prose) | HVLD parabola | When referenced in documentation (API key preserved in code) |

**Note on legacy API keys:** The pipeline code retains `step6_pll_shape`, `step6_pll_R2`, `step6_pll_coeffs`, and `self.pll_result` as internal dictionary keys for API compatibility. These are data identifiers, not terminology. They may appear in code listings but must always be annotated as legacy keys for HVLD when referenced in documentation.

### When to Preserve Legacy Names

Legacy terminology (HUF, CIP) is preserved in:

- **Lineage sections** — where the intellectual journey is documented
- **Theory documents** — where CIP Rules are referenced as historical methodology (e.g., "CIP Rule 5" in the Diffraction Composition Principle)
- **Experiment results JSON** — `framework` field records the name used at experiment time
- **Parent repository references** — links to Higgins-Unity-Framework repo

Legacy terminology is replaced in:

- **Active tool names** — filenames, HTML titles, page headers
- **README and navigation** — all current-facing documentation
- **Machine manifests** — config files that guide automated systems
- **Pipeline code comments** — where HUF-GOV is used as current label
- **New documents** — anything created after this convention

---

## Interactive Tool Names (Canonical)

| # | Filename | Display Name |
|---|----------|-------------|
| 1 | `Hs_CoDaWork_Demo.html` | Hˢ CoDaWork Demo |
| 2 | `cosmic_composition_interactive.html` | Cosmic Composition Slider |
| 3 | `cosmic_cone_5min_loop.html` | Cosmic Cone Loop |
| 4 | `cosmic_duality_dance.html` | Cosmic Duality Dance |
| 5 | `cosmic_future_projection.html` | Cosmic Future Projection |
| 6 | `EXP-19_Interactive_Simulator.html` | Simplex Scope |
| 7 | `EXP16_Interactive_Simulator.html` | Spring-Mass Simulator |
| 8 | `EXP-19_Fourier_Conjugate_Preservation_Theorem.html` | Conjugate Preservation Theorem |
| 9 | `Hs_Spectrum_Analyzer.html` | Hˢ Spectrum Analyzer |

---

## Document Creation — Mandatory Terminology Check

**Before creating or updating any document in the Hˢ repository, the following review is mandatory:**

1. Review `HS_ADMIN.json → canonical_names` — every entry with a `NOT` list defines banned terms.
2. Review the Retired Terminology Migration Table above — apply all substitutions.
3. Search all source content for banned terms BEFORE writing. Older source files (theory docs, experiment results, HUF-era documents) contain retired terms that must not be transcribed into new documents.
4. After document generation, grep the output for all banned terms. If any appear (except in explicitly marked legacy/lineage sections), fix before delivery.

**The full aggregated banned terms list is maintained in `HS_ADMIN.json → document_creation_checklist → banned_terms_master_list`.**

This step exists because source documents written before the naming convention was established still contain PLL, HUF-as-identity, CIP, and other retired terms. When these sources are used to build new documents, the retired terms propagate unless actively caught. The checklist is the catch.

---

## Quality Mark

Files following this convention carry the Hˢ identity. Users encountering `Hs_` or `Higgins_` prefixed files know they are part of the governed, deterministic, audited Higgins Decomposition system. The naming convention is itself a diagnostic — if a file doesn't follow it, it predates the convention or needs migration.

---

*Hˢ Naming Convention v1.0 — April 2026*
*Peter Higgins — Rogue Wave Audio*
