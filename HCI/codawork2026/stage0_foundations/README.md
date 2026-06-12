# Stage-0 Foundations Plate Generator

**Created:** 2026-05-14
**Author:** Peter Higgins, Rogue Wave Audio
**Conforms to:** HUF-STD-001 (Publication) + HUF-STD-002 (Tensor Train I/O) + HUF-STD-003 (Hs Linear Algebra Foundations)

---

## What this module is

The Stage-0 plate is the **foundations tier** of the Hs Output Doctrine — read once per dataset to visualize the seven linear-algebra components on which the framework rests:

1. Symmetric matrix — variation matrix heatmap (D × D)
2. Property of transpose — Helmert basis + orthonormality verification H Hᵀ = I
3. Matrix decomposition — raw → CLR → ILR chain
4. Eigenvectors / eigenvalues — eigenvalue scree + cumulative variance
5. Strong property of symmetric matrices (Spectral Theorem) — residual ‖Σ − Q Λ Qᵀ‖ at IEEE floor
6. Spectral decomposition — orthonormal eigenbasis Q heatmap + rank-k variance breakdown
7. Visualization — the plate itself

Stages 1–4 read derived per-timestep quantities; Stage 0 reads what doesn't change — the foundations of the geometry.

---

## Where Stage 0 fits in the Output Doctrine

| Stage | Order | Cadence | What it shows |
|---|---|---|---|
| **0 (NEW)** | Order 0+ (foundational) | once per dataset | Seven linear-algebra components — bedrock |
| 1 | Order 1 | once per timestep + summary | Pairwise bearings (Section) + ILR projection (Triplet) |
| 2 | Order 2 | once per dataset | Helmsman, course, variation analysis, CoDa-PCA biplot |
| 3 | Order 3 | once per dataset | Depth tower, IR class, attractor fit, κ^HS |
| 4 | Order 4+ | varies | EITT, cross-dataset comparison, schema validation |

---

## Files

| File | Purpose |
|---|---|
| `foundations_plate.py` | Generator. Reads `stage1_output.json` from `stage1_engine.py`, emits 2-page PDF (foundations grid + numeric verification). |
| `README.md` | This file. |

---

## Usage

```bash
# From repo root, generate a stage1 JSON first, then run the foundations plate
cd HCI/codawork2026/stage1_plates
python3 stage1_engine.py ../../../data/Energy/EMBER_pipeline_ready/ember_DEU_Germany_generation_TWh.csv stage1_DEU.json

# Then the foundations plate
cd ../stage0_foundations
python3 foundations_plate.py ../stage1_plates/stage1_DEU.json DEU_stage0.pdf
```

For all 9 EMBER countries, the per-country PDFs live in `CODA-Association/CODAwork2026/data_outputs/per_country_pdfs/{ISO}_stage0.pdf`, and the master Foundations PDF is `data_outputs/CodaWork2026_FoundationsPlates_2026-05-14.pdf` (19 pages: cover + 9 × 2-page country sections).

---

## Output specification

**Page 1 — Foundations grid (2 rows × 3 columns):**

```
┌──────────────────┬──────────────────┬──────────────────┐
│ §1 Variation     │ §2 Helmert       │ §3 Decomposition │
│ matrix heatmap   │ basis +          │ chain (raw→CLR   │
│ (D×D symmetric)  │ orthonormality   │ →ILR)            │
├──────────────────┼──────────────────┼──────────────────┤
│ §4 Eigenvalue    │ §6 Orthonormal   │ §5 Spectral      │
│ scree + cum-var  │ eigenbasis Q     │ Theorem residual │
│ curve            │ heatmap          │ + rank-k panel   │
└──────────────────┴──────────────────┴──────────────────┘
```

**Page 2 — Numeric verification table:** 16 numeric proofs at machine precision. Every foundation gets a `max|...|` quantity reported alongside its IEEE-floor judgment. Example readings for Germany:

- max|M − Mᵀ| = 0.00e+00 for variation matrix (symmetric by construction)
- max|H Hᵀ − I| = 2.22e-16 (IEEE-floor)
- max|Σ − Q Λ Qᵀ| = 1.14e-13 (Spectral Theorem holds at IEEE-floor)
- Rank-1 = 60.5%, Rank-2 = 90.4%, Rank-3 = 99.9% — Germany's mix lives essentially in a 2-D ILR plane

---

## Doctrine status

Stage 0 is a **doctrinal addition** under HUF-STD-002 link 4 (Vector Diagrammatic Output) and HUF-STD-003 §7 (Visualization). It does **not** change engine code or schemas. It is a new plate-generator module added under the existing lockdown discipline (same risk-profile as `stage1_plates/ilr_triplet_plate.py` added 2026-05-13).

---

## AI Use Declaration

Per HUF-STD-001.

**AI tools used:** Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI) — the HUF AI Collective.

**Tasks performed by AI:** Drafting `foundations_plate.py`; identifying which JSON keys to read; designing the six-panel grid layout and numeric verification table.

**Author responsibility:** P. Higgins, Rogue Wave Audio. The mathematics is textbook linear algebra (Cayley, Sylvester, Schur, von Neumann); the choice to surface it as a dedicated Stage-0 plate is the author's editorial decision per Peter directive 2026-05-14.

**Dates of use:** 2026-05-14.

**Standards reference:** HUF-STD-001 + HUF-STD-002 + HUF-STD-003.

---

*The foundations carry the bedrock.*
*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
