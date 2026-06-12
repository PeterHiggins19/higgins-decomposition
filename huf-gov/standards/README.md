# huf-gov/standards/ — HUF Publication Standards

**Created:** 2026-05-13
**Purpose:** Authoritative JSON-database location for HUF and derivative-repository publication standards. Any task that must meet an established scientific-community standard for media generation references the JSON files in this folder.

---

## Files

| File | ID | Purpose |
|---|---|---|
| [`HUF_PUBLICATION_STANDARDS.json`](HUF_PUBLICATION_STANDARDS.json) | HUF-STD-001 | Adopts ICMJE / COPE / Nature / Science / WAME / EU AI Act / arXiv / ACM / IEEE as primary references. Establishes AI Use Declaration template, authorship attribution rules, falsifiability disclosure, provenance hash-chain, versioning, locale support, lockdown discipline, licensing. |
| [`HUF_TENSOR_TRAIN_IO_STANDARD.json`](HUF_TENSOR_TRAIN_IO_STANDARD.json) | HUF-STD-002 | Codifies the data→CNT→CNQ→vector-output chain as the named **Tensor Train v1.0**. Defines I/O contracts at each link. PDF / PNG / SVG are the standard outputs. **PPTX is explicitly excluded** — conference-only, downstream of standard outputs, not engine pipeline. Sets post-conference implementation targets for `hs_cnq_pdf_exporter.py` + Stage 3 + Stage 4 plate modules. |
| [`TENSOR_TRAIN.md`](TENSOR_TRAIN.md) | (companion) | Markdown narrative + diagram of HUF-STD-002. Read this for the visual / prose explanation; consult the JSON for the formal contract. |
| [`HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json`](HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json) | HUF-STD-003 | Names the **seven linear-algebra components** on which every Hs engine and plate generator rests: (1) Symmetric Matrix · (2) Property of Transpose · (3) Matrix Decomposition · (4) Eigenvectors / Eigenvalues · (5) Strong Property of Symmetric Matrices (Spectral Theorem) · (6) Spectral Decomposition · (7) Visualization. Establishes Stage-0 (Foundations Plate) as the dedicated visualization tier. Conformance requirements + post-conference targets included. |
| [`FOUNDATIONS.md`](FOUNDATIONS.md) | (companion) | Markdown narrative companion to HUF-STD-003 — one section per component with mapping to current Hs code. |
| [`FOUNDATIONS_TRACEABILITY.md`](FOUNDATIONS_TRACEABILITY.md) | (audit) | Per-component traceability map: every file, plate, and schema field where each foundation lives. Supports the post-conference CHK-FOUNDATIONS-001 consistency-checker rule. |

Future standards JSONs (peer-review submission conventions, poster standards, data-sharing standards, etc.) live here.

---

## How to use

**For document authors / generators (human or AI):** before publishing any HUF or derivative-repository media intended for external audiences, consult `HUF_PUBLICATION_STANDARDS.json`. The `standards_adopted` section lists the requirements; the `ai_use_declaration_template` section gives the exact format to include at the end of the document.

**For admin JSONs:** the `_meta` section of HS_ADMIN.json and HS_FAST_REFRESH.json reference HUF-STD-001 as the authoritative standard. Other admin JSONs in derivative repositories should do the same.

**For partnerships / external collaborators:** point them at this JSON file. They will recognise the established scientific-community standards being honored.

---

## Doctrine

These standards exist because the HUF + Hs work is offered to the scientific peer community under the same conventions the community uses among itself. AI assistance is disclosed transparently. Authorship is human-only. Falsifiability is published. Provenance is hash-chained. Versioning is visible.

> *Published standards from the peer community are adopted as HUF doctrine wherever they exist; HUF specializes only where the peer community has not yet ruled.*

---

*Authority is by JSON. The JSON is the source. Documents conform; conformance is recorded.*
