# Hs Linear Algebra Foundations — The Seven Components

**Standard:** HUF-STD-003 (companion JSON: [`HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json`](HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json))
**Authority:** Foundational — applies to all HUF + Hs + HCI-CNT + HCI-CNQ engines, plate generators, and schemas
**Created:** 2026-05-14
**Author:** Peter Higgins, Rogue Wave Audio
**Sibling standards:** HUF-STD-001 (Publication) · HUF-STD-002 (Tensor Train I/O)

---

## The seven components in one line

> **Symmetric Matrix → Property of Transpose → Matrix Decomposition → Eigenvectors/Eigenvalues → Strong Property of Symmetric Matrices → Spectral Decomposition → Visualization**

This is the load-bearing arc of classical linear algebra and the spine on which every Hs engine and plate generator stands. The components were employed throughout the Hs framework from the earliest versions of CNT and CNQ; HUF-STD-003 names them as a unified doctrine for the first time.

---

## Why now

The framework has matured to the point where its mathematical foundations should be visible to peer reviewers, future maintainers, and AI agents alike. Until 2026-05-14 the seven components were employed implicitly — used every time CLR was projected to ILR, every time a covariance was decomposed, every time an attractor was fit. None of them were cited by name. The Spectral Theorem in particular — the silent justification for orthonormality across the entire framework — was never invoked explicitly.

Peter directive 2026-05-14: *"these are the main components that should be employed for hs."* HUF-STD-003 makes that explicit.

---

## The seven, one by one

### 1. Symmetric Matrix

A matrix M is symmetric when M = Mᵀ, i.e. M[i,j] = M[j,i]. Symmetric matrices are the canonical objects of multivariate statistics because the natural second-order summaries — covariance, variation, Gram matrices — are inherently symmetric.

**Where it lives in Hs.** The **variation matrix** of a composition is var(log x_i / x_j), symmetric by construction. CNT computes this implicitly when forming pairwise log-ratios. The **CLR covariance** Cov(clr(X)) is symmetric and positive-semidefinite — it is the matrix CoDa-PCA decomposes in Stage 2 plates. The **Gram matrix** of the Helmert basis H · Hᵀ = I is the orthonormality certificate for ILR projection.

The bearing tensor θ_ij is the antisymmetric (skew-symmetric) sibling: θ_ji = −θ_ij. Symmetric and antisymmetric matrices are duals — both are first-class in Hs.

**Stage-0 visualization.** Variation matrix shown as a D×D heatmap with the symmetry visible to the eye.

---

### 2. Property of Transpose

Transpose has algebraic properties that make linear algebra tractable: (Aᵀ)ᵀ = A; (A+B)ᵀ = Aᵀ + Bᵀ; (AB)ᵀ = Bᵀ Aᵀ; (A⁻¹)ᵀ = (Aᵀ)⁻¹. The key special case: for orthonormal Q, Qᵀ = Q⁻¹.

**Where it lives in Hs.** The ILR-Helmert transform `ilr = clr @ Hᵀ` and its inverse `clr = ilr @ H` are both exact because H·Hᵀ = I. This is the property that makes the Triplet Plate's trajectory inspection geometrically valid — the projection from CLR space to ILR space preserves distances and angles. See `HCI/codawork2026/stage1_plates/ilr_triplet_plate.py` line ~99 for the explicit use.

The covariance propagation rule Cov(M·X) = M · Cov(X) · Mᵀ is the engine of change-of-basis statistics throughout Hs.

**Stage-0 visualization.** Helmert basis H shown as a heatmap (D−1 rows × D columns), with an orthonormality-check panel showing H·Hᵀ converging to the (D−1)×(D−1) identity matrix at machine precision.

---

### 3. Matrix Decomposition

A decomposition factors a matrix into structurally-simpler pieces. Common decompositions include LU, QR, Cholesky, SVD, and eigendecomposition. Each one reveals a different facet — triangularity, orthogonality, positive-definiteness, or directionality.

**Where it lives in Hs.** Multiple decompositions are first-class outputs:

- **closure → CLR → ILR** chain — each step is a decomposition of the composition into a more analytically-tractable form
- **Pairwise bearing tensor decomposition** — the trajectory at each timestep decomposes into D(D−1)/2 antisymmetric channels
- **Depth tower** (CNT Order-3) — nested orthogonal subspace decomposition
- **CoDa-PCA** (Stage 2) — eigendecomposition of CLR covariance

**Stage-0 visualization.** A composition-decomposition tree: raw composition → closed → CLR → ILR, with each arrow labeled by the operation and visualized as a small panel.

---

### 4. Eigenvectors and Eigenvalues

For a square matrix M, an eigenvector v is a non-zero direction that M scales rather than rotates: M·v = λ·v. Eigenvectors are the privileged directions of M; eigenvalues λ are how strongly M acts along them.

**Where it lives in Hs.** The **attractor fit** in `cnq.py` computes the eigenvalues of the local linearization to detect exponential contraction — surfaced in the CNQ dashboard's diagnostics box as `amplitude_A` and `contraction_λ`. The **κ^HS sensitivity vector** in `cnt.py` is an eigenvector-style direction naming which carrier is most responsible for trajectory change. The **CoDa-PCA biplot** uses eigendecomposition of Cov(clr(X)) to find principal axes.

**Stage-0 visualization.** Eigenvalue scree plot — eigenvalues of the CLR covariance in descending order, with a cumulative-variance-explained overlay. The visual signature of dimension-reduction potential.

---

### 5. Strong Property of Symmetric Matrices (Spectral Theorem)

Every real symmetric matrix has real eigenvalues and an orthonormal basis of eigenvectors. This is the **Spectral Theorem** and is the strongest single result in elementary linear algebra. It guarantees that symmetric matrices can *always* be diagonalized by an orthogonal change of basis — and that the eigenvalues come out real, not complex.

**Where it lives in Hs.** Everywhere — silently. ILR coordinates form an orthonormal basis because the Helmert (or any SBP) construction relies on the Spectral Theorem. CoDa-PCA produces real principal components because Cov(clr(X)) is symmetric. The attractor fit's eigenvalues are real because the local Jacobian, when symmetrizable, falls under the theorem.

Until HUF-STD-003 this load-bearing theorem was never cited in any Hs document. The work used it constantly but did not name it. The Stage-0 verification panel surfaces the dependency: it computes Σ = Q·Λ·Qᵀ on the CLR covariance and displays ‖Σ − Q·Λ·Qᵀ‖ as a numeric norm at the IEEE floor — visual proof that the theorem holds at machine precision on the actual data.

**Stage-0 visualization.** Verification panel — numeric reconstruction-residual of the Spectral Theorem, displayed at machine precision (typical ~1e-15).

---

### 6. Spectral Decomposition

The explicit factorization Σ = Q·Λ·Qᵀ for symmetric Σ, where Q is the orthonormal eigenbasis and Λ is the diagonal of eigenvalues sorted in descending order. Truncating Λ at rank-k gives the optimal rank-k approximation (Eckart–Young).

**Where it lives in Hs.** Stage 2 CoDa-PCA biplot performs this decomposition partially (showing the first 2 axes). CNQ's `attractor_fit` performs spectral analysis of the local linearization. But no existing plate shows the *full* spectral decomposition Q·Λ·Qᵀ side-by-side. Stage-0 closes that gap.

**Stage-0 visualization.** Two-panel display: (a) eigenvalue spectrum bar chart with cumulative-explained-variance curve; (b) orthonormal eigenbasis Q as a (D−1)×(D−1) heatmap, each column an eigenvector, with carrier labels on the rows. Together they show *the* spectral decomposition for the dataset.

---

### 7. Visualization

Linear algebra without visualization is opaque. Every component above admits a visual representation: symmetric matrix as heatmap, transpose as axis swap, decomposition as factorized panels, eigenvectors as arrows, eigenvalues as a scree plot, spectral decomposition as a reconstruction-quality curve. The **Stage-0 Foundations Plate** is the plate suite that makes the foundations legible.

**Where it lives in Hs.** Section Plate, Triplet Plate, CNQ dashboard, and helmsman/spike-detector plates all visualize *consequences* of the foundations. None of them visualize the foundations themselves. Stage-0 Foundations Plate (`HCI/codawork2026/stage0_foundations/foundations_plate.py`) is the new dedicated tier.

**Stage-0 visualization.** Stage-0 IS this component. See the per-country Foundations Plate PDFs in `CODA-Association/CODAwork2026/data_outputs/per_country_pdfs/{ISO}_stage0.pdf`.

---

## Where Stage-0 fits in the Output Doctrine tower

The Hs Output Doctrine v1.0 already defined Stage 1 → 2 → 3 → 4 plates. HUF-STD-003 adds Stage 0 underneath:

| Stage | Order | What it visualizes |
|---|---|---|
| **0** (NEW) | Order 0+ (foundational) | The seven linear-algebra foundations themselves — variation matrix, Helmert basis, eigenvalue spectrum, spectral decomposition |
| 1 | Order 1 (first-principles) | Pairwise bearings (Section Plate) + orthonormal ILR projection (Triplet Plate) |
| 2 | Order 2 (inter-timestep) | Helmsman, course plot, CoDa-PCA biplot, variation analysis |
| 3 | Order 3 (recursive) | Depth tower, IR class, attractor fit, κ^HS |
| 4 | Order 4+ (inferential) | EITT, cross-dataset comparison, schema validation |

Stage 0 is read **once per dataset** (the foundations don't change frame-to-frame; they characterize the data's geometry). Stage 1 is read **once per timestep**. Together they form the complete per-dataset reading.

---

## How to use this standard

**For engine authors.** Read HUF-STD-003 alongside HUF-STD-002 and the Output Doctrine v1.0. Any new computational module declares which foundations it employs in its docstring. The CHK-FOUNDATIONS-001 consistency-checker rule will audit this declaration against the actual computational content (post-conference target).

**For plate-generator authors.** Stage-0 is reserved for foundations visualization. Stages 1–4 visualize derived quantities. All Stage-N plates produce PDF / PNG / SVG per HUF-STD-002 link 4.

**For schema authors.** JSON output blocks recording eigenstructures, symmetric matrices, or orthonormal bases shall carry foundation-reference tags (`HUF-STD-003-§1` through `§6`). This is a post-conference target.

**For conference / publication authors.** Cite HUF-STD-003 when describing the mathematical foundations of Hs. The seven components are textbook linear algebra — naming them makes the framework's bedrock visible to peer reviewers without claiming novelty for what is already canonical mathematics.

---

## What was already there vs what HUF-STD-003 adds

| Already there (before 2026-05-14) | What HUF-STD-003 adds |
|---|---|
| ILR-Helmert orthonormal basis used in all Stage 1 plates | The naming of the Spectral Theorem as the silent justification |
| Variation matrix computed inside cnt.py | The naming of foundation 1 as "Symmetric Matrix" and a dedicated visualization |
| Attractor fit using eigenstructure inside cnq.py | The naming of foundations 4 + 6 and their schema-tag conformance |
| Output Doctrine Stages 1–4 visualizations | Stage 0 — the foundations-explicit tier |
| Hash-chained CNT + CNQ JSON outputs | Foundation tags on schema fields (post-conference) |

The framework already rested on these foundations. HUF-STD-003 makes that rest visible.

---

## AI Use Declaration

Per HUF Publication Standards (HUF-STD-001).

**AI tools used:** Claude (Anthropic), ChatGPT (OpenAI), Copilot (Microsoft), Gemini (Google), Grok (xAI) — the HUF AI Collective.

**Tasks performed by AI:** Drafting HUF-STD-003 JSON and this narrative companion; mapping each of the seven foundations to where it lives in current Hs code; drafting the Stage-0 plate generator (`foundations_plate.py`); drafting the traceability audit.

**Author responsibility:** Peter Higgins, Rogue Wave Audio retains full responsibility. The seven foundations are classical linear algebra known since the 19th–20th centuries (Cayley, Sylvester, Schur, von Neumann). Their identification as the load-bearing components of Hs is the author's editorial choice. AI tools are NOT listed as authors.

**AI use governance:** HUF AI Collective cross-check protocol per HUF Governance Charter Articles II–IV and SAFE-001.

**Dates of use:** 2026-05-14 (HUF-STD-003 drafting session).

**Standards reference:** HUF-STD-001 + HUF-STD-002 + HUF-STD-003 (this standard).

---

*Foundations are first-class.*
*Symmetric matrices have orthonormal eigenbases.*
*Transposes invert orthonormal matrices.*
*Decompositions reveal structure.*
*Eigenvectors name the privileged directions.*
*The Spectral Theorem is the silent justification.*
*Spectral decomposition is the visible factorization.*
*Visualization makes all six legible.*
*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line. The foundations carry the bedrock.*
