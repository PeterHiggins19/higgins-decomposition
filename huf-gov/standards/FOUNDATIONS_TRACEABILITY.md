# Foundations Traceability Audit

**Companion to:** HUF-STD-003 (`HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json` + `FOUNDATIONS.md`)
**Created:** 2026-05-14
**Author:** Peter Higgins, Rogue Wave Audio
**Purpose:** For each of the seven linear-algebra components of Hs, list every file in the repository where it lives, every plate that depends on it, and every JSON output field that records its consequence. This is the conformance-check document that supports the future CHK-FOUNDATIONS-001 consistency-checker rule.

---

## How to read this audit

Each foundation has three columns:

- **Engine code** — Python (and R port where applicable) files where the foundation is computed.
- **Plate generator** — files that visualize the foundation or its consequence.
- **Schema field** — fields in canonical CNT or CNQ JSON outputs that record the foundation's quantitative result.

A foundation can appear in multiple files. The Stage-0 plate is the dedicated visualization tier for the foundation itself (per HUF-STD-003 §7); other Stages visualize consequences.

---

## §1 — Symmetric Matrix

**Mathematical statement.** M = Mᵀ. Symmetric matrices are the canonical objects of multivariate statistics — covariance, variation, Gram matrices.

| Where | File(s) | Notes |
|---|---|---|
| Engine code | `HCI-CNT/engine/cnt.py` | Computes variation matrix implicitly via pairwise log-ratios in `coda_standard` block per timestep. CLR covariance computable from `tensor.timesteps[*].coda_standard.clr` aggregated. |
| Engine code | `HCI-CNT/engine/cnt.R` | R-port parity for the same. |
| Engine code | `HCI/codawork2026/stage1_plates/stage1_engine.py` | Stage-1 engine outputs `records[*].clr` from which variation matrix is built. |
| Plate generator | `HCI/codawork2026/stage0_foundations/foundations_plate.py` (NEW) | Direct visualization (§1 panel + numeric verification of M = Mᵀ at IEEE-floor). |
| Plate generator | `HCI/atlas/stage2_locked.py` | Uses symmetric variation matrix in CoDa-standard biplot construction (visualized indirectly as biplot axes). |
| Schema field | `tensor.timesteps[*].coda_standard.clr` | CLR vector at each timestep; variation matrix is var across timesteps of pairwise differences. |
| Schema field | `stages.stage_1.variation_summary` (if present) | Stage-1 summary may include variation matrix entries. |
| Antisymmetric sibling | `tensor.timesteps[*].bearing_tensor` (cnt.py output) | θ_ji = −θ_ij — antisymmetric (skew-symmetric) sibling of symmetric variation. |

---

## §2 — Property of Transpose

**Mathematical statement.** For orthonormal Q, Qᵀ = Q⁻¹. The key property that makes orthonormal-basis coordinate changes exact and lossless.

| Where | File(s) | Notes |
|---|---|---|
| Engine code | `HCI-CNT/engine/cnt.py` | `coda_standard.ilr` computed via `clr @ H.T` (Helmert basis transpose). |
| Engine code | `HCI-CNT/engine/cnt.R` | Same in R: `clr %*% t(H)`. |
| Plate generator | `HCI/codawork2026/stage1_plates/ilr_triplet_plate.py` line ~99 | `clr_to_ilr(clr_array, H) ⇒ clr @ H.T`. Explicit transpose use. |
| Plate generator | `HCI/codawork2026/stage0_foundations/foundations_plate.py` (NEW) | Visualizes Helmert basis H + orthonormality check H Hᵀ = I at IEEE-floor. |
| Schema field | `tensor.timesteps[*].coda_standard.ilr` | ILR coordinates (Helmert-projected CLR). |
| Verification | The Helmert basis H satisfies H Hᵀ = I_{D−1} (orthonormal rows). Verified explicitly in Stage-0 §2 panel and numeric verification table. |

---

## §3 — Matrix Decomposition

**Mathematical statement.** M = ABC... — factor a matrix into structurally-simpler pieces. Each decomposition reveals a different facet.

| Where | File(s) | Notes |
|---|---|---|
| Engine code | `HCI-CNT/engine/cnt.py` | Closure → CLR → ILR chain. Pairwise bearing tensor decomposition. Depth-tower decomposition (Order-3 output block). |
| Engine code | `HCI-CNQ/engine/cnq.py` | Twin-quaternion decomposition (D=8 case, `twin_quaternion_factoring` block). |
| Plate generator | `HCI/codawork2026/stage1_plates/stage1_plates_raw.py` | Section Plate visualizes pairwise bearing decomposition (D(D−1)/2 channels as XZ bars). |
| Plate generator | `HCI/codawork2026/stage1_plates/ilr_triplet_plate.py` | Triplet Plate visualizes ILR decomposition (three orthogonal projections). |
| Plate generator | `HCI/codawork2026/stage0_foundations/foundations_plate.py` (NEW) | §3 panel shows the decomposition chain (raw → closed → CLR → ILR) as annotated arrows. |
| Plate generator | `HCI/atlas/stage2_locked.py` | Stage-2 plates visualize CoDa-PCA decomposition. |
| Schema field | `tensor.timesteps[*].bearing_tensor` | Pairwise bearings (decomposition into D(D−1)/2 channels). |
| Schema field | `depth_tower.*` | Recursive decomposition (Order-3). |
| Schema field | `cnq.twin_quaternion_factoring` | CNQ twin-quaternion decomposition (D=8). |

---

## §4 — Eigenvectors and Eigenvalues

**Mathematical statement.** M v = λ v, v ≠ 0. Eigenvectors are the privileged directions of M; eigenvalues are how strongly M acts along them.

| Where | File(s) | Notes |
|---|---|---|
| Engine code | `HCI-CNQ/engine/cnq.py` | `attractor_fit` computes eigenvalues of local linearization (amplitude A + contraction λ). |
| Engine code | `HCI-CNT/engine/cnt.py` | κ^HS sensitivity vector is an eigenvector-style direction emitted in `tensor.timesteps[*].higgins_extensions.kappa_hs_vector` (or equivalent). |
| Plate generator | `HCI/codawork2026/stage0_foundations/foundations_plate.py` (NEW) | §4 panel: eigenvalue scree of CLR covariance + cumulative variance curve. |
| Plate generator | `HCI/atlas/stage2_locked.py` | CoDa-PCA biplot uses eigendecomposition of CLR covariance to find principal axes (visualizes the top 2 eigenvectors). |
| Plate generator | `HCI/codawork2026/stage1_plates/stage23_plates.py` | CNQ dashboard shows `attractor_fit.amplitude_A` and `.contraction_lambda` in diagnostics box. |
| Schema field | `attractor_fit.amplitude_A` | CNQ output — top eigenvalue magnitude. |
| Schema field | `attractor_fit.contraction_lambda` | CNQ output — exponential contraction rate. |
| Schema field | `tensor.timesteps[*].higgins_extensions.kappa_hs_vector` | CNT output — κ^HS sensitivity direction (eigenvector-style). |

---

## §5 — Strong Property of Symmetric Matrices (Spectral Theorem)

**Mathematical statement.** Real symmetric Σ has real eigenvalues and orthonormal eigenbasis Q: Σ = Q Λ Qᵀ. The strongest result in elementary linear algebra; the silent justification for orthonormality everywhere.

| Where | File(s) | Notes |
|---|---|---|
| Silent justification | ALL of the above — the Spectral Theorem justifies why ILR is orthonormal, why CoDa-PCA produces real principal components, why attractor_fit produces real eigenvalues. |
| Explicit verification | `HCI/codawork2026/stage0_foundations/foundations_plate.py` (NEW) | Page 1 §5 panel + page 2 verification table compute ‖Σ − Q Λ Qᵀ‖ on actual data, displaying IEEE-floor residual (~1e-13 typical). |
| Documentation | `huf-gov/standards/FOUNDATIONS.md` | First explicit citation of the theorem as Hs's silent justification. |
| Documentation | `huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json` §5 | Standards-level citation. |
| Schema field | (none — the theorem is implicit; foundation tag added post-conference per HUF-STD-003 conformance_requirements.for_schema_authors) | |

---

## §6 — Spectral Decomposition

**Mathematical statement.** Σ = Q Λ Qᵀ explicitly. Truncating Λ at rank-k gives the optimal rank-k approximation (Eckart–Young).

| Where | File(s) | Notes |
|---|---|---|
| Engine code | `HCI-CNQ/engine/cnq.py` | `attractor_fit` performs spectral analysis of local linearization. |
| Plate generator | `HCI/atlas/stage2_locked.py` | CoDa-PCA biplot — partial spectral decomposition (first 2 axes visualized). |
| Plate generator | `HCI/codawork2026/stage0_foundations/foundations_plate.py` (NEW) | Full spectral decomposition: §6 panel shows orthonormal eigenbasis Q heatmap + rank-k cumulative variance (k=1, 2, 3, D). |
| Schema field | `depth_tower.*` (cnt.py output) | Recursive decomposition fields — includes top-eigenvalue-style summaries. |
| Schema field | `attractor_fit.amplitude_A`, `.contraction_lambda`, `.period` | CNQ output — spectral analysis of attractor. |

---

## §7 — Visualization

**Statement.** Every foundation above admits a visual representation. Stage-0 is the dedicated visualization tier.

| Where | File(s) | Notes |
|---|---|---|
| Stage 0 (NEW) | `HCI/codawork2026/stage0_foundations/foundations_plate.py` | Direct visualization of §1–§6. |
| Stage 1 | `HCI/codawork2026/stage1_plates/stage1_plates_raw.py` | Section Plate — visualizes pairwise bearings (§1 antisymmetric sibling, §3 decomposition) and CLR (§3). |
| Stage 1 | `HCI/codawork2026/stage1_plates/ilr_triplet_plate.py` | Triplet Plate — visualizes ILR orthonormal projection (§2, §5 silent). |
| Stage 2 | `HCI/codawork2026/stage1_plates/stage23_plates.py` + `HCI/atlas/stage2_locked.py` | Helmsman, course, CoDa-PCA biplot (§4 eigenvalues, §6 partial spectral decomposition). |
| Stage 3 | `HCI/atlas/stage2_locked.py` (depth tower) | Depth-tower recursive decomposition (§3) + attractor fit (§4 eigenvalues). |
| Stage 4 | (post-conference) `atlas/stage4.py` planned | EITT + cross-dataset comparison + schema validation visual surface. |
| Conference output | `CODA-Association/CODAwork2026/data_outputs/CodaWork2026_FoundationsPlates_2026-05-14.pdf` | 19-page master Foundations PDF covering all 9 EMBER countries. |

---

## Per-country verification summary (Stage-0 numeric outputs)

For each EMBER country, the Stage-0 plate's page-2 verification table reports machine-precision residuals on all seven foundations. Headline rank-k breakdown:

| Country | D | N | Rank-1 % | Rank-2 % | Rank-3 % |
|---|---|---|---|---|---|
| AUS | 9 | 26 | (read from `data_outputs/per_country_pdfs/AUS_stage0.pdf` page 2) |
| CHN | 8 | 26 | |
| DEU | 9 | 26 | 60.48 | 90.42 | 99.92 |
| FRA | 9 | 26 | |
| GBR | 9 | 26 | |
| IND | 8 | 26 | |
| JPN | 8 | 26 | |
| USA | 9 | 25 | |
| WLD | 9 | 26 | |

Germany's 60.48% / 90.42% / 99.92% breakdown says the German electricity-mix evolution lives essentially in a **2-D plane within 8-D ILR space** — the dominant Coal-to-Renewable axis plus a secondary Nuclear-shaped axis is enough to capture > 90% of the variance. This is consistent with the talk's headline narrative.

---

## Post-conference follow-up — CHK-FOUNDATIONS-001 rule

The repository's consistency checker (`scripts/check_ai_refresh_consistency.py`) will gain a new rule after the conference lockdown clears (2026-06-06):

- **CHK-FOUNDATIONS-001** — for every module under `HCI-CNT/engine/`, `HCI-CNQ/engine/`, `HCI/codawork2026/`, `HCI/atlas/`, audit that its docstring declares which of the seven HUF-STD-003 foundations it employs. Compare declared foundations against actual computational content. Report any module that computes a foundation but does not declare it.

The rule is **deferred** to post-conference because:
1. Adding a checker rule requires testing it against the live tree.
2. Engine and plate docstrings need to be updated to declare foundations — a docs-only sweep, but better done deliberately under HCC (Hs Change Control) than under conference rush.
3. The lockdown forbids speculative checker-rule additions during the pre-conference window.

The CHK-FOUNDATIONS-001 specification is recorded in HUF-STD-003 `conformance_requirements.verification` and in `post_conference_targets.order_1`.

---

## Files added 2026-05-14 for HUF-STD-003

| File | Type | Lockdown-class |
|---|---|---|
| `huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json` | Standards JSON | S2 doc-only |
| `huf-gov/standards/FOUNDATIONS.md` | Narrative companion | S2 doc-only |
| `huf-gov/standards/FOUNDATIONS_TRACEABILITY.md` | This audit | S2 doc-only |
| `HCI/codawork2026/stage0_foundations/foundations_plate.py` | Plate generator | S2 new-module (same risk-class as ilr_triplet_plate.py added 2026-05-13) |
| `HCI/codawork2026/stage0_foundations/README.md` | Folder README | S2 doc-only |
| `CODA-Association/CODAwork2026/data_outputs/per_country_pdfs/{ISO}_stage0.pdf` × 9 | Generated output | S2 doc-only |
| `CODA-Association/CODAwork2026/data_outputs/CodaWork2026_FoundationsPlates_2026-05-14.pdf` | Master Foundations PDF | S2 doc-only |

All files are additive. No existing engine, schema, INV catalog disposition, NO-CREATE file, or `papers/codawork2026/talk/` content is modified. Lockdown compatibility preserved.

---

## AI Use Declaration

Per HUF-STD-001.

**AI tools used:** Claude (Anthropic), with the broader HUF AI Collective (ChatGPT, Copilot, Gemini, Grok) for cross-check.

**Tasks performed by AI:** Producing this traceability audit by reading repository files and mapping each component to its location.

**Author responsibility:** P. Higgins, Rogue Wave Audio. The mapping reflects the current state of the repository; the seven foundations are textbook linear algebra.

**Dates of use:** 2026-05-14.

**Standards reference:** HUF-STD-001 + HUF-STD-003.

---

*The foundations carry the bedrock.*
*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
