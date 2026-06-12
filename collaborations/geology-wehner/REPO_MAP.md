# Repo Map — where everything relevant lives across the PeterHiggins19 structure

A single index to every relevant part of the work, **no matter which repo it lives in.** Three public repos plus the local working mirror; browse online (GitHub) or locally. Copies of the smaller documents are already in `copies/`; the large datasets are linked (see `large-linked/`).

## The three repositories
| Repo | GitHub | Role for this case |
|---|---|---|
| **higgins-decomposition (Hs)** | `github.com/PeterHiggins19/higgins-decomposition` | the instrument (CNT/CNQ) + the geochemistry validation |
| **Higgins-Unity-Framework (HUF)** | `github.com/PeterHiggins19/Higgins-Unity-Framework` | EITT + the EXP geochem / crystallography / fixed-point experiments |
| **Rogue-Wave-Audio (RWA)** | `github.com/PeterHiggins19/Rogue-Wave-Audio` | origin of the diffraction-composition principle (DADC) that became the compositional method |

## Entry points (read first)
- **Hs:** `HS_FAST_REFRESH.json` (source of truth) · `README.md` · `AI_AGENTS.md` · the working notes `Hs_CNT_CNQ_Operating_Limits_Working_Notes.md` — **§5/§8 (zero treatment) and §9 (forensic soil) are directly relevant to mudstone trace-element zeros.**
- **HUF:** `ai-refresh/HUF_FAST_REFRESH.json` · `ai-refresh/MASTER_LINEAGE.json`.

## The engine (deterministic; published Python + R + pseudocode)
- `Hs/HCI-CNT/engine/cnt.py` (+ `cnt.R`) — CNT.
- `Hs/HCI-CNQ/engine/cnq.py` (+ `cnq.R`) — CNQ.

## Geology / geochemistry material, by repo
**Hs (higgins-decomposition):**
- `experiments/Hs-05_Geochemistry/` — Ball intraplate-volcanics validation (26,266 rocks, 10 oxides) + `region_binning/` + `pipeline_output/`.
- `experiments/Hs-CNT_2026-05/domain/geochem_*` — CNT runs: Ball region / TAS / age, Stracke OIB & MORB, Tappe kimberlite, Qin clinopyroxene; `…/extended/chemixhub_oxide`.
- `data/Geochemistry/` — composition CSVs (`ball_oxides_composition.csv`).
- `data/pipeline_output/DATA-GEOCHEM_*` — manifold paper / projections / polar stack (large — see `large-linked/`).
- `docs/theory/Higgins_Diffraction_Composition_Principle.{md,json}`.
- `papers/validation/EXP15_Xray_Crystallography_Journal.docx`.

**HUF (Higgins-Unity-Framework):**
- `codawork2026/experiments/EXP-14_Fixed_Point_Selection/` — HFSP catalog, **intermediate-rocks decode** (mafic↔felsic), fixed-point/phase machinery.
- `codawork2026/experiments/EXP-15_Xray_Crystallography/` — crystallography decomposition (`.py/.png/.json`).
- `science/core/HFSP_MASTER_CATALOG.json` · `HIGGINS_DIFFRACTION_COMPOSITION_PRINCIPLE.json`.
- `codawork2026/journals/HIGGINS_Geochemistry_EITT.pdf`.
- `codawork2026/extended/CoDaWork2026_Handout_Geochemistry_Bridge.docx`.
- `science/chemistry/CHEM_EITT_RESEARCH_PLAN.md`.

**RWA (Rogue-Wave-Audio):**
- The diffraction-composition origin (DADC/DADI): `docs/papers/…`, `LINEAGE.md`, `RWA-001.json`. *Lineage: the 6.02 dB diffraction simplex → HUF's MC-4 → CNT.*

**Working artifacts (coworker mirror, not in a repo):**
- `HIGGINS_geochem_master_panel.png`, `HIGGINS_geochem_clr_trajectory.png`, `hfsp_anchor_refinement.{md,json,png}`, `hfsp_chain_test.{json,png}`, `intermediate_rocks_decode.{json,png}` — copied into `copies/coworker-root/`.

## Large datasets (local mirror only — linked, not copied)
- `DATA/Geochemistry/` (**18 GB**): Ball, Stracke, Tappe, Woerner, Kemnitz-Lausitz, Hawaii-volcanism, chemixhub — the raw source data.
- `Hs/data/pipeline_output/DATA-GEOCHEM_manifold_paper.pdf` (**~100 MB**), `DATA-GEOCHEM_polar_stack.json` (~21 MB).

*If any path has moved, `HS_FAST_REFRESH.json` (Hs) and `MASTER_LINEAGE.json` (HUF) are the durable anchors.*


---

## Addendum — 2026-06-09 (post-publication advancement)

*Non-destructive note (Cowork working tree; not yet git-committed). The content above is unchanged and remains valid as published.*

New under `collaborations/geology-wehner/`: `00_EXECUTIVE_OVERVIEW.md` (front door + §9 receipts link layer), `demo_frielingen9/` (reproducible Frielingen-9 mudstone demo + 16:9 dashboard + field-by-field guide + HS_PRIMER), and the concept docs `CNQ_TILING_CONCEPT.html` / `FACETED_READ_CONCEPT.html` / `HS_FRONTEND_POSITION.html`. Off-repo: `Pipeline-Projects/P2_Matthew-Wehner-Geology-Collab/proposal_USGS_NASA_2026-06-09/`.

Since publication the system advanced: Hs/CNT/CNQ was applied to **mudstone chemostratigraphy** as a cited, reproducible demo on real PANGAEA data (`collaborations/geology-wehner/`), and a new concept — **CNQ tiling / "faceted read"** (overlapping exact D=4 charts glued on shared parts reconstruct the full higher-dimensional compositional move **losslessly**: alignment 9e-16, reconstruction 4e-14, overlap proven necessary) — was tested. **Engine, schemas, and canonical numbers are UNCHANGED**; this is a documentation / application / concept advance. Gluing maths CONFIRMED; scientific value on real high-D data TO TEST. Full current picture: `collaborations/geology-wehner/00_EXECUTIVE_OVERVIEW.md`.
