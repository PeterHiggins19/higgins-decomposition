# Hˢ Terminology Migration Log

**Date:** April 29, 2026
**Author:** Peter Higgins / Claude
**Purpose:** Permanent audit trail documenting the removal of all banned terminology from the Hˢ repository.

---

## Background

The Higgins Decomposition repository inherited terminology from its predecessor, the Higgins Unity Framework (HUF). Several terms used in the HUF era were either misleading (hijacking established meanings from other fields) or no longer accurate. The most persistent offender was **PLL** — originally borrowed from "Phase-Locked Loop" electronics terminology, which was never accurate: the pipeline contains no phase detector, no loop filter, no VCO, and no feedback loop. The term was formally retired in favour of **HVLD** (Higgins Vertex Lock Diagnostic) but kept reappearing in documents built from older source material.

This migration log records the final, comprehensive cleanup.

---

## Banned Terms and Their Replacements

| Banned Term | Replacement | Reason for Ban |
|---|---|---|
| PLL | HVLD | Hijacks "Phase-Locked Loop" from electronics. No PLL exists in the pipeline. |
| Phase-Locked Loop | Higgins Vertex Lock Diagnostic | Technically false — no feedback loop exists. |
| Pipeline Lock List | (never used) | Alternative PLL expansion, also incorrect. |
| PLL vertex | HVLD vertex | Carries the banned PLL prefix. |
| PLL lock / PLL lock point | HVLD lock / HVLD lock point | Carries the banned PLL prefix. |
| PLL parabola | HVLD parabola | Carries the banned PLL prefix. |
| HD | Hˢ | Ambiguous — conflicts with "High Definition", "Hard Drive", etc. |
| Higgins Decomp / H-decomp | Higgins Decomposition / Hˢ | Informal abbreviations that lack clarity. |
| EITT conjecture | EITT Analytic Bound | O-1 is resolved (April 28, 2026). It is no longer a conjecture. |
| EITT hypothesis | EITT Analytic Bound | Same — it is a proven theorem, not a hypothesis. |
| open problem O-1 | (resolved) | O-1 was closed by the Gemini analytic proof. |
| boundary threshold | Compositional Horizon | Vague — could mean anything in any field. |
| simplex edge | Compositional Horizon | Imprecise — the horizon is a specific min(x_i) threshold, not a geometric edge. |
| dimension reduction / PCA | Dimensional Collapse Cycle | PCA is a completely different technique. The collapse is a phase transition, not a projection. |
| data cleaning / outlier removal | Compositional Pruning | Pruning preserves structure. Cleaning implies noise removal. Fundamentally different. |

---

## Legacy API Keys (Preserved)

The following internal Python dictionary keys are retained for API compatibility. They are data identifiers, not terminology. All documentation annotates them as legacy HVLD keys.

| Key | Used In | Note |
|---|---|---|
| `step6_pll_shape` | Pipeline result dict, all experiment JSONs | HVLD shape classification |
| `step6_pll_R2` | Pipeline result dict, all experiment JSONs | HVLD R² fit quality |
| `step6_pll_coeffs` | Pipeline result dict | HVLD quadratic coefficients |
| `self.pll_result` | HigginsDecomposition class attribute | HVLD fit result storage |
| `def pll_parabola()` | HigginsDecomposition method | HVLD parabola fitting (annotated with "Legacy name retained") |

---

## Files Modified (April 28-29, 2026)

### Governance and Admin

| File | Change |
|---|---|
| `ai-refresh/HS_ADMIN.json` | Expanded HVLD ban list (3→10 entries). Added `legacy_api_keys_preserved`, `legacy_note`, `document_creation_checklist`, and `banned_terms_master_list`. |
| `ai-refresh/HS_MACHINE_MANIFEST.json` | `PLL_shapes` → `HVLD_shapes` |
| `ai-refresh/PREPARE_FOR_REPO.json` | `PLL_shapes` → `HVLD_shapes` |
| `docs/Hs_Naming_Convention.md` | Added 6 PLL→HVLD migration rows, legacy API key note, and mandatory Document Creation Terminology Check section. |

### Documentation (Markdown)

| File | Change |
|---|---|
| `EXECUTIVE_SUMMARY.md` | "PLL shapes" → "HVLD shapes" (line 1444). "simplex edge" → "compositional horizon" (lines 430, 1352). |
| `docs/theory/Natures_Confirmation_Series.md` | 4× PLL → HVLD (table entries and tier references). |
| `docs/theory/Higgins_Diffraction_Composition_Principle.md` | 3× PLL → HVLD (theorem statement and predictions). |
| `papers/codawork2026/CoDaWork2026_Future_Path.md` | "EITT conjecture" → "EITT analytic bound". |
| `papers/codawork2026/CoDaWork2026_Collaboration_Path.md` | "EITT conjecture" → "EITT analytic bound". |

### Documentation (JSON)

| File | Change |
|---|---|
| `docs/theory/NATURES_CONFIRMATION_SERIES.json` | All `pll_result` → `hvld_result`. All PLL → HVLD in text (~16 occurrences). |
| `docs/theory/HIGGINS_DIFFRACTION_COMPOSITION_PRINCIPLE.json` | 3× PLL → HVLD. |
| `experiments/Hs_FULL_CHAIN_REPORT_2026-04-28.json` | 25× `PLL_shape` → `HVLD_shape`. `PLL_shapes` → `HVLD_shapes`. Summary text PLL → HVLD. |

### Pipeline Code

| File | Change |
|---|---|
| `tools/pipeline/higgins_decomposition_12step.py` | Comment "PLL" → "HVLD" (line 1079). "Simplex edge" → "Compositional horizon" in constant dict (line 167). |

### HTML and Notebooks

No changes needed — already clean.

### Archived Files

None. All files were fixable in place.

---

## Industry Conflict Check

| Hˢ Term | Known Industry Meaning | Conflict Risk |
|---|---|---|
| HVLD | High Voltage Leak Detection (pharma packaging) | Low — completely different domain. No realistic confusion. |
| EITT | No prominent conflicting acronym found | Minimal |
| HTP | High Test Peroxide (rocketry), Hydroxytryptophan (biochem) | Low — context disambiguates. Full name "Higgins Transcendental Pretest" is used on first reference. |
| CLR | Centered Log-Ratio (CoDa standard) | None — this IS the CoDa term. Correct usage. |
| CoDa | Compositional Data Analysis | None — standard field terminology. |

---

## Enforcement

The `document_creation_checklist` in `HS_ADMIN.json` makes the ban list review mandatory before creating or updating any document. The `Hs_Naming_Convention.md` migration table is the definitive mapping. Any AI system generating content for this repository must review both before writing.

The `archive/` folder exists for files that cannot be cleanly migrated. As of this date, no files required archival — all were successfully migrated in place.

---

*This log is the permanent record. The banned terms are dead. HVLD stands.*

*Peter Higgins — Rogue Wave Audio*
*April 29, 2026*
