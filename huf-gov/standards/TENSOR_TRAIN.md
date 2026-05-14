# The HUF Tensor Train v1.0

**Standard:** HUF-STD-002 (companion JSON: [`HUF_TENSOR_TRAIN_IO_STANDARD.json`](HUF_TENSOR_TRAIN_IO_STANDARD.json))
**Authority:** Foundational — applies to all HUF + Hs + derivative compositional-analysis pipelines
**Created:** 2026-05-13
**Author:** Peter Higgins, Rogue Wave Audio
**Parent doctrine:** Output Doctrine v1.0 (HCI-CNT/conference_demo/cnt_demo/05_doctrine/OUTPUT_DOCTRINE.md) + CNQ Vector PDF Spec (INV-062 STAGED)

---

## The chain in one line

> **raw CSV  →  CNT (metric tensor)  →  CNQ (metric quaternion)  →  vector diagrammatic output (PDF / PNG / SVG)**

This is the **Tensor Train v1.0**: a four-link, hash-chained pipeline that takes domain data in and emits archival vector artifacts out. The chain was implicit before 2026-05-13 — its pieces existed as separate documents. This standard names the train and makes the I/O contract explicit at every link.

---

## The four links

### Link 1 — Adapter (Order 0)

| Aspect | Specification |
|---|---|
| Purpose | Convert domain-specific raw data into a clean compositional CSV |
| Input | Domain data (EMBER electricity TWh, GDP sector values, geochem mol-fractions, etc.) |
| Output | CSV with columns `[time_index, carrier_1, …, carrier_D]` |
| Implementation | `adapters/` per-domain modules + `adapters/ADAPTERS_DISCLOSURE.md` |
| Order | 0 — pre-engine; raw composition before closure |
| Hash | `source_file_sha256` recorded in disclosure |

### Link 2 — CNT (Compositional Navigation Tensor, Orders 1–3)

| Aspect | Specification |
|---|---|
| Purpose | The metric-tensor engine — closure, CLR, ILR-Helmert, bearing tensor, angular velocity, steering metric, helmsman index, Higgins scale, depth tower, attractor fit, IR class |
| Input | Compositional CSV (link 1 output) OR in-memory composition |
| Output | **Canonical CNT JSON** — schema 3.1.0 |
| Implementation | `HCI-CNT/engine/cnt.py` (Python), `HCI-CNT/engine/cnt.R` (R parity port) |
| Entry point | `cnt.cnt_run(csv_path, out_path=...)` |
| Pseudocode | `HCI/cnt_v2/CNT_PSEUDOCODE.md` |
| Schema | `HCI/cnt_v2/CNT_JSON_SCHEMA.md` |
| Order classification | Per Output Doctrine v1.0 — Stage 1 emits Order 1, Stage 2 emits Order 2, Stage 3 emits Order 3, Stage 4+ reserved |
| Hash emitted | `metadata.content_sha256` + `metadata.engine_signature` |
| Top-level JSON blocks | `metadata`, `input`, `tensor`, `stages.{stage_1,stage_2,stage_3}`, `depth_tower`, `helmsman_family`, `attractor_fit`, `diagnostics` |

### Link 3 — CNQ (Compositional Navigation Quaternion, Order 2–3 algebraic view)

| Aspect | Specification |
|---|---|
| Purpose | The metric-quaternion engine — bearing trajectories at D=2 / D=3 / D=4 twin-factor, CHSH joint-coherence diagnostic, twin-quaternion sandwich residuals, helmsman family in SU(2) double-cover terms |
| Input | Canonical CNT JSON (link 2 output) + original CSV for cross-verification |
| Output | **Canonical CNQ JSON** — schema cnq/2.0.0 |
| Implementation | `HCI-CNQ/engine/cnq.py` (Python), `HCI-CNQ/engine/cnq.R` (R parity port) |
| Entry point | `cnq.cnq_run(input_csv=..., cnt_json_path=..., out_path=...)` |
| Pseudocode | `HCI-CNQ/engine/CNQ_PSEUDOCODE.md` |
| Schema | `HCI-CNQ/engine/CNQ_SCHEMA.md` |
| Hash emitted | `metadata.content_sha256` (CNQ) + `metadata.cnt_reference_sha256` (chain back to CNT) |
| Top-level JSON blocks | `metadata`, `input`, `cnt_reference`, `cnq_view.{bearing_trajectory_d2,d3,d4, chsh_diagnostic, twin_quaternion_factor}`, `helmsman_family`, `attractor_fit` |

### Link 4 — Vector Diagrammatic Output Tensor

| Aspect | Specification |
|---|---|
| Purpose | Render the canonical CNT and CNQ JSON outputs as deterministic vector graphics — the output IS itself a tensor (one plate per timestep × N timesteps + summary plates) |
| Input formats | Canonical CNT JSON + canonical CNQ JSON |
| **Standard output formats** | **PDF (primary, PDF/A-3 archival), PNG (raster fallback), SVG (vector editable)** |
| **Out of standard** | **PPTX — conference-only, downstream of standard outputs, not produced by the engine pipeline** |
| Currently implemented (Stage 1) | `stage1_plates_raw.py` — Higgins Tensor Data Field Layout v1.0; XY scatter + XZ bearing bar + YZ CLR bar + info + legend; one plate per timestep + course plot |
| Currently implemented (Stage 1 locked reference) | `atlas/stage1_v4.py` — ILR-Helmert orthogonal triplet, 27-point calibration fixture |
| Currently implemented (Stage 2) | `stage23_plates.py` (informal) + `atlas/stage2_locked.py` (19 reference plates) |
| Currently implemented (Stage 3) | Partial — depth tower / IR class / attractor are text-output from CNT; no dedicated visual plate module yet |
| Currently implemented (Stage 4) | Not yet |
| Specified but not implemented | `tools/pipeline/hs_cnq_pdf_exporter.py` per INV-062 STAGED spec |
| Hash chain | Every output artifact embeds `Hs_Content_SHA256` (CNT) + `Hs_CNQ_Content_SHA256` (CNQ when rendered) + `Hs_Generated_At` + `Hs_Engine_Version` + `Hs_Provenance_JSON` (minified). Source CNT/CNQ JSONs attached as PDF/A-3 file attachments for full reproducibility. |
| Validation | veraPDF `--flavour pdfa-3b` — archival PDF must validate or be rejected |

---

## What is excluded — the PPTX boundary

**PPTX is NOT part of the standard tensor-train package.** It is a conference-delivery format only. Reasons codified in HUF-STD-002:

1. PPTX is a binary multimedia container with no standard hash-embedding mechanism.
2. PPTX permits arbitrary post-creation reordering that breaks any embedded hash chain.
3. PPTX rendering is not deterministic — different versions of PowerPoint render the same file differently.
4. PPTX has no archival ISO format equivalent to PDF/A-3.

PPTX is built **downstream of** the standard PDF / PNG / SVG outputs by curating selected pages and adding narrative slides. The CoDaWork 2026 conference deck at `CODA-Association/CODAwork2026/CodaWork2026_Talk_2026-05-13.pptx` is exactly this kind of downstream curation. Conference-delivery tooling (build_deck.js + pptxgenjs, python-pptx scripts) consumes the standard outputs; it does not extend the train.

---

## What was already there vs what HUF-STD-002 adds

| Already there (before 2026-05-13) | What HUF-STD-002 adds |
|---|---|
| Output Doctrine v1.0 — Order/Stage classification (locked May 5 2026) | The name "Tensor Train v1.0" |
| INV-062 STAGED — CNQ Vector PDF Spec | The explicit I/O contract per link |
| CNT_JSON_SCHEMA, CNQ_SCHEMA | The PDF/PNG/SVG-in / PPTX-out boundary |
| stage1_plates_raw.py, stage23_plates.py, atlas/stage1_v4.py, atlas/stage2_locked.py | The post-conference implementation target order |
| Hash-chained engines emitting content_sha256 | A single authoritative reference for the chain |

The pieces existed; the train was implicit. HUF-STD-002 makes it explicit, names it, contracts it.

---

## Post-conference implementation targets

When the PRE_CONFERENCE_LOCKDOWN clears on 2026-06-06, four targets close the remaining gaps in link 4:

| Order | Target | Closes | Effort |
|---|---|---|---|
| 1 | `tools/pipeline/hs_cnq_pdf_exporter.py` implementation (INV-062 → CANONICAL) | The hash-coded fraud-prevention PDF exporter; the final mandatory step of CCTT Phase 7 | 2–3 days |
| 2 | PNG / SVG export siblings for `stage1_plates_raw.py` + `stage23_plates.py` | Raster + editable-vector outputs alongside PDF | 0.5 days |
| 3 | `atlas/stage3.py` — depth tower / IR / attractor visual plates | Stage 3 visual surface (currently text-only) | 1–2 days |
| 4 | `atlas/stage4.py` — EITT bench + cross-dataset comparison + schema-validator surface | Stage 4 visual surface | 2–3 days |

All four targets implement existing doctrine — they extend link 4 only and do not touch engine code in `cnt.py` or `cnq.py`.

---

## Reading the train as a tensor of tensors

The standard is named "Tensor Train" because each link operates on tensors and emits tensors:

- **Adapter** emits an N × D compositional matrix
- **CNT** emits a 4-channel time-tensor (bearing tensor θ_ij, angular velocity ω, steering metric κ, helmsman σ) over N timesteps with D(D-1)/2 pairwise channels
- **CNQ** emits a quaternion-view tensor q(t) ∈ S³ over N timesteps + scalar CHSH(t) + twin-quaternion residuals at IEEE floor
- **Vector output** emits a tensor of plates: N × (XY plate, XZ plate, YZ plate) for Stage 1, plus stage-2/3/4 summary plates per dataset, plus per-dataset CNQ dashboards

The output package itself is a tensor. The full per-country PDF in `CODA-Association/CODAwork2026/data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf` is the rendered tensor for the 9-country EMBER corpus: 9 countries × (1 cover + 27 Stage-1 plates + 7 Stage-2/3 pages + 2 CNQ plates) = 333 country-tensor pages plus master cover and TOC.

---

## How to use this standard

**For engine code maintainers.** Read this document and the Output Doctrine v1.0 together. Engine output (CNT / CNQ JSON) must conform to the I/O contract. Schema changes route through Hs Change Control v1.0 with a DCP.

**For plate-generator authors.** Read this document + INV-062 (the PDF spec) + the existing Stage 1 / Stage 2 plate generators. New plate generators conform to the link-4 format menu (PDF / PNG / SVG). PPTX is not a target.

**For downstream tools / partners.** The CNT JSON and CNQ JSON are the canonical interchange formats. Anyone with the JSON can reproduce the plates. Anyone with the plates can verify against the embedded hashes.

**For conference / publication authors.** PDF is the artifact you cite. Hashes in the PDF metadata are the authority. PPTX is what you project on stage; it is not what gets cited.

---

## AI Use Declaration

Per HUF Publication Standards (HUF-STD-001).

**AI tools used:** Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI) — the HUF AI Collective.

**Tasks performed by AI:** drafting this standard document; consolidating the existing Output Doctrine v1.0 + INV-062 spec + CNT/CNQ schemas into one named train; cross-checking I/O contracts against engine reality.

**Author responsibility:** The author retains full responsibility for the standard. The four links described all exist in code (with the noted exception of `hs_cnq_pdf_exporter.py` which is specified but not implemented). The author has reviewed and verified each I/O contract. AI tools are not authors.

**AI use governance:** HUF AI Collective cross-check protocol per HUF Governance Charter Articles II–IV and SAFE-001.

**Dates of use:** March 2026 – May 2026.

**Standards reference:** HUF-STD-001 (publication standards) + HUF-STD-002 (this standard).

---

*Each link of the train hash-chains forward.*
*The data enters once. The output carries every hash from the entry.*
*PDF is the archival format. PNG and SVG are rendering siblings. PPTX is conference delivery, not engine output.*
*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
