# Tiling the simplex: an exact quaternion reading of compositional dynamics and lossless high‑dimensional reconstruction

**Working draft — 2026-06-10. For HUF AI Collective review; not submission‑ready until the final novelty pass clears (see §8).**
**Author:** Peter Higgins (Independent; Rogue Wave Audio / Binaural Test Lab, Markham, Ontario, Canada). Human authorship for all claims; AI‑assisted per HUF‑STD‑001.

> **Movement I — Exactness**, the foundation of the five‑part arc (**exactness** → trust → motion → character → vigilance): before anything is interpreted, a composition is read *exactly*. Everything downstream (P3 the instrument, P4 motion, P5 character, P2 vigilance) stands on this. Suite narrative: [`../THE_HIGGINS_DECOMPOSITION_SERIES.md`](../THE_HIGGINS_DECOMPOSITION_SERIES.md).

---

## Abstract

Compositional data — vectors of parts carrying only relative information — are analysed in Aitchison geometry through log‑ratio coordinates. For a four‑part composition the three isometric‑log‑ratio (ILR) coordinates coincide in dimension with the imaginary part of the quaternions, so the composition's local dynamics can be read **exactly** as a rotation on the three‑sphere S³ = SU(2) via the quaternion sandwich product. We introduce this quaternion reading of a composition and, to carry it beyond four parts, a **tiling** construction: a high‑dimensional composition is covered by an atlas of overlapping exact four‑part charts, and its full log‑ratio trajectory is reconstructed losslessly from the charts. We prove the reconstruction reduces to a sparse graph‑Laplacian solve that is exact if and only if the charts' part co‑occurrence graph is connected, and we show that a hierarchical (e.g. phylogenetic) atlas of O(log D) diameter holds reconstruction near machine precision at high dimension. On controlled data the method reconstructs a one‑million‑part composition to ≈4×10⁻¹² in a few seconds on a laptop, using O(D) charts rather than the combinatorial alternative, and never forming a dense global basis. The pipeline is deterministic and hash‑chained throughout. We position the method carefully against established work — subcompositional coherence, log‑ratio‑graph reconstruction, group synchronization, manifold‑chart alignment, and phylogenetic balances — and isolate the two genuinely new elements: the quaternion‑exact reading of a composition, and the locally‑exact, lossless, deterministic synthesis as a single auditable instrument.

---

## 1 · Introduction

Compositional data analysis (CoDa) studies vectors whose components carry only relative information — geochemical oxide fractions, energy‑generation mixes, microbiome taxon abundances, dietary macronutrient shares. Since Aitchison [1] the standard treatment maps the simplex into real coordinates by log‑ratios (the centered log‑ratio, CLR; the isometric log‑ratio, ILR [2]) so that ordinary geometry applies in Aitchison space.

The four‑part composition is a special case with an unusually rich structure. Its three ILR coordinates have exactly the dimension of the imaginary quaternions, and the unit quaternions form the three‑sphere S³ = SU(2), the double cover of the rotation group SO(3). One can therefore read a four‑part composition's step‑to‑step change as an exact rotation, with bearing, handedness, and time‑reversal (conjugation) available in closed form. This exactness does not extend natively to higher dimension: the normed division algebras stop at dimension eight (Hurwitz [3]; octonions lose associativity, sedenions lose the division property [4]), so there is no "bigger quaternion" that reads a high‑dimensional composition as one exact rotation.

This is the gap that motivates the present work. The deterministic compositional‑navigation method on which this builds was presented at CoDaWork 2026 (Coimbra), where the scale of fields such as microbiome research — compositions of thousands to hundreds of thousands of parts — made the limitation concrete: the exact reading lives at four parts, real problems do not. **The exact four‑part quaternion reading raised at CoDaWork 2026 prompted an immediate question — how to carry that exactness to high‑dimensional compositions — and this work is the response.**

Our answer is to *tile* rather than to enlarge the algebra: cover a high‑dimensional composition with overlapping exact four‑part charts and reconstruct the whole from the parts. We show the reconstruction is lossless under a simple, checkable condition, that it scales linearly, and that it is deterministic and auditable end‑to‑end.

### Contributions
1. The **quaternion reading of a composition** (§3.1): identifying a four‑part composition's ILR coordinates with a unit quaternion on S³=SU(2) for an exact rotation reading. To our knowledge (two exhaustive prior‑art searches, §2) this specific identification is new.
2. **CNQ‑tiling** (§3.2–3.4): an atlas of overlapping exact four‑part charts whose overlaps reconstruct the full high‑dimensional log‑ratio trajectory losslessly, with an exactness condition (§3.3) and a hierarchical atlas that controls conditioning at scale (§3.4).
3. A **deterministic, hash‑chained instrument** realizing the above, validated to D=10⁶ (§4), with every claim tiered (§6) and positioned honestly against prior art (§2, §5).

We are explicit about what is *not* new: the reconstruction theorem, the synchronization machinery, the manifold‑atlas concept, subcompositional coherence, and tree‑structured balances are all prior art, cited in §2 and used as foundations.

## 2 · Background and prior art

**Log‑ratio geometry.** CLR/ILR coordinates and the orthonormal (Helmert) contrast basis are standard [1,2]; balances and the sequential binary partition formalize tree‑structured coordinates [5]. **Subcompositional coherence** [1] — that analysis on a subcomposition is consistent with the whole — is the principle that licenses gluing overlapping subcompositions on their shared parts.

**Reconstruction from log‑ratios.** That a *connected* set of pairwise log‑ratios determines a composition up to closure, with an explicit inverse, is established by Greenacre [6,7]: a connected directed acyclic graph of J−1 log‑ratios generates all pairwise log‑ratios by linear combination. Our reconstruction step is an instance of this result; we do not claim it as new.

**Recovering a global object from relative measurements on a graph.** The least‑squares recovery of node values from edge differences, solvable iff the graph is connected, with conditioning governed by the algebraic connectivity / graph diameter, is classical spectral graph theory [8,9] and the scalar case of **group (angular) synchronization** [10,11]; the rotation analogue is **rotation averaging / SO(3) synchronization** [12,13]. The categorical home of "consistent local data glued to a global object, obstruction = cohomology" is the theory of **cellular sheaves**, whose sheaf Laplacian generalizes the graph Laplacian [14]. Our reconstruction engine is an application of these; we cite, we do not claim.

**Overlapping local charts aligned globally.** The manifold notion of an **atlas of charts with transition maps** [15] is instantiated for data by **Local Tangent Space Alignment** [16] and Brand's **"Charting a Manifold"** [17], which align overlapping local linear charts into a global embedding. Those methods use *approximate* (linear) charts and produce *lossy*, dimension‑reduced embeddings; our charts are *exact* and our reconstruction is *information‑preserving* — the distinguishing axis.

**Tree‑structured balances for high‑dimensional compositions.** Using a phylogenetic tree to define ILR balances is established as **PhILR** [18] and related tree/hierarchy methods (gneiss [19]; PhyloFactor [20]; principal balances [21]). Our hierarchical atlas uses the same tree‑structuring idea; we cite PhILR prominently and do not claim tree balances as new.

**Distinguished neighbours.** A flat, commutative Lie‑group structure on the simplex exists [22] but carries no quaternion/SU(2) content. Compositional data have been mapped to a sphere via the square‑root / Fisher–Rao transform [23], but that is a different (curved, group‑free) sphere, not the ILR↔S³=SU(2) identification with the sandwich product. Quaternions appear in shape analysis and directional statistics for *shapes and orientations*, and in colour processing for *raw RGB* — different objects.

Across two exhaustive web‑indexed searches we found no work identifying a composition's ILR coordinates with unit quaternions for a rotation reading; that specific link (§3.1) is the novel geometric element, with the standard quaternion↔SO(3) machinery [3,4] used as established tools.

## 3 · Method

### 3.1 The quaternion reading at D=4
For a four‑part composition `x`, closure and CLR give `clr(x) = log x − mean log x`; an orthonormal Helmert basis `H` (3×4) gives ILR coordinates `z = clr(x) · Hᵀ ∈ ℝ³`. Identify `z` (as a pure‑imaginary direction) and a rotation built from successive steps with unit quaternions on S³; the rotation that carries one normalized step to the next is read by the sandwich product `q v q*`, exact in SO(3). Bearing and angular velocity are read with the numerically stable form `atan2(‖a×b‖, a·b)` rather than `arccos(a·b)`, which recovers full precision near 0° and 180°. Radial magnitude is the ILR norm `‖z‖`, retained as a first‑class quantity. *(Note for referees: "D=4 special" means three ILR degrees of freedom equal the dimension SU(2) rotates exactly; ℍ is four‑dimensional as 1 real + 3 imaginary — the two "4"s coincide for distinct reasons.)*

### 3.2 The atlas
A **chart** is an ordered set of four parts; on it the §3.1 reading is exact. An **atlas** is a set of charts covering all parts. Two atlas families: a **sliding window** (consecutive 4‑part charts overlapping in 3 parts) and a **hierarchical / phylogenetic** atlas (group parts into blocks of four, promote one representative per block, recurse to a root — for microbiome data this tree is the phylogeny, so sibling taxa share low‑level charts).

### 3.3 Lossless reconstruction and the connectivity condition
Each chart measures the three independent log‑ratios among its parts. Stacking all chart log‑ratios `log(xᵢ/xⱼ) = clrᵢ − clrⱼ` gives a linear system `A c = b` on the CLR vector `c`; the normal matrix `AᵀA` is the **graph Laplacian** of the parts' co‑occurrence graph. The CLR is recovered (up to the fixed sum‑zero constraint) **if and only if that graph is connected**; a disconnected atlas leaves inter‑component offsets unidentified. This is the Greenacre connected‑graph result [6,7] / the scalar synchronization result [10] in compositional form. **Overlap is therefore necessary, not decorative.**

### 3.4 Conditioning and the hierarchical atlas
The reconstruction's numerical conditioning is set by the co‑occurrence graph's diameter (via the Laplacian's algebraic connectivity [8,9]). A sliding‑window atlas is a path of length ~D, so accumulated rounding grows with D. A balanced hierarchical atlas has diameter **O(log D)**, keeping reconstruction near machine precision at any dimension while still using O(D) charts.

### 3.5 Determinism and provenance
Every step is deterministic (same input → same output, bit‑for‑bit), with no statistics or sampling in the science path, organized as a four‑link hash‑chained pipeline (ingest+treat → geometry → tile/atlas → navigate+emit) carrying a canonical content hash. Below‑detection zeros are handled by an upstream multiplicative‑replacement adapter rather than a hard floor.

## 4 · Results (measured; reproducible)

All numbers from `experiments/cnq_tiling_highd_2026-06/` (fixed seeds; rerun to identical values) and reproduced from inside the reference engine's self‑test.

- **Quaternion exactness (D=4).** Sandwich product vs. the Rodrigues rotation: max error **2.7×10⁻¹⁵** over 2×10⁴ random rotations. Angle near 0°: the atan2 form is exact (0 relative error) where `arccos` reaches 100% relative error.
- **Lossless reconstruction (connected atlas).** Max reconstruction error **2.1×10⁻¹³** across D = 16, 64, 256 (single connected component every time).
- **Overlap necessity.** A disjoint atlas fails: error **1.16** (order one), the graph splitting into D/4 components.
- **Native D=16 unnecessary.** A random sixteen‑part move is reconstructed from four‑part charts to **2.2×10⁻¹⁵** — a four‑part tiler reproduces the high‑dimensional move exactly.
- **Scaling.** Charts grow as O(D); reconstruction runs in **0.16 s at D=10⁵** and **1.9 s / <50 MB at D=10⁶**, versus a brute‑force C(D,4) chart count (~10²² at D=10⁶) and an 8‑TB dense global‑ILR basis that the method never forms.
- **Hierarchical atlas at scale.** Tree atlas diameter grows 3→10 over D = 64→10⁶ (path atlas: 21→333,333); reconstruction stays **≈1×10⁻¹³ – 4×10⁻¹²** (path atlas degrades to 2×10⁻⁷). Using ~D/3 charts.

## 5 · Discussion

The method's strength is that it makes the exact four‑part reading usable at arbitrary dimension *without* abandoning determinism or losslessness — the two properties most high‑dimensional compositional pipelines trade away for statistics or lossy reduction. The honest delineation from prior art: the reconstruction primitive and the tree‑balance idea are established (§2); the new elements are the quaternion reading of a composition (§3.1) and the locally‑exact, lossless, deterministic synthesis as one instrument. The contrast with LTSA / "Charting a Manifold" [16,17] is precise — their charts are approximate and their output lossy; ours are exact and information‑preserving.

**Limitations.** (i) The quaternion reading's novelty rests on a thorough but negative literature search (§8). (ii) Reconstruction is lossless only for a connected atlas; degenerate (vanishing) parts require the zero‑treatment adapter and can locally reduce effective dimension. (iii) Conditioning, while controlled by a hierarchical atlas, is not bit‑exact at extreme D (≈10⁻¹² at D=10⁶), set by floating‑point accumulation over ~log D tree levels; double‑double arithmetic would close it if ever needed. (iv) The scientific value of the per‑chart quaternion *ensemble* on real high‑dimensional data — beyond exact reconstruction — remains to be demonstrated on a real phylogeny/dataset.

## 6 · Claim tiers
- **Tier 1 (verified):** all §4 results; the connectivity condition; the atan2 advantage.
- **Tier 2 (standard, soundly applied):** the Greenacre / synchronization reconstruction result; Hurwitz/Cayley‑Dickson; the diameter→conditioning argument.
- **Tier 3 (to earn):** the absolute novelty of §3.1 (pending §8); the per‑chart ensemble's added scientific value on real high‑D data with a real phylogeny.

## 7 · Reproducibility
Code, data, figures, and a journaled experiment are in `experiments/cnq_tiling_highd_2026-06/`; the reference engine and its self‑test are in `HCI-CNTT/`. Deterministic under fixed seeds.

## 8 · Pre‑submission gate
Before submission, run a final novelty confirmation against Google Scholar, NASA ADS, Semantic Scholar, and a patent database (USPTO/WIPO), plus a non‑English CoDa‑community check — the channels the web search could not reach directly. Until then §3.1's novelty is stated as "novel to the best of an exhaustive web‑indexed search."

## Acknowledgments
This work was developed with assistance from the HUF AI Collective under HUF‑STD‑001 (AI Use Declaration): Claude (Anthropic) as executor/test‑runner/file‑writer, ChatGPT (OpenAI) for structure and claim‑audit, Grok (xAI) as independent reviewer and prior‑art devil's‑advocate, Gemini (Google) for cross‑checking, and Copilot (Microsoft) where available. All scientific claims are human‑authored; no AI system is an author. The cardinal rule throughout was never to upgrade inspected evidence into executed evidence. The author thanks the collective for accelerating the initial concept development, and the CoDaWork 2026 community whose discussion of high‑dimensional compositional problems inspired this line of work.

## References (to be completed/verified at submission)
[1] Aitchison, J. (1986) *The Statistical Analysis of Compositional Data.* Chapman & Hall.
[2] Egozcue, J.J., Pawlowsky‑Glahn, V., Mateu‑Figueras, G., Barceló‑Vidal, C. (2003) Isometric logratio transformations. *Math. Geol.* 35:279–300.
[3] Hurwitz, A. (1898) Über die Composition der quadratischen Formen. *Nachr. Ges. Wiss. Göttingen.*
[4] Baez, J.C. (2002) The Octonions. *Bull. Amer. Math. Soc.* 39:145–205.
[5] Egozcue, J.J., Pawlowsky‑Glahn, V. (2005) Groups of parts and their balances. *Math. Geol.* 37:795–828.
[6] Greenacre, M. (2019) Variable selection in CoDa using pairwise logratios. *Math. Geosci.* 51:649–682.
[7] Greenacre, M. (2020) Amalgamations are valid in CoDa… inverse transformation. *Appl. Comput. Geosci.* 5:100017.
[8] Fiedler, M. (1973) Algebraic connectivity of graphs. *Czech. Math. J.* 23:298–305.
[9] Chung, F.R.K. (1997) *Spectral Graph Theory.* AMS.
[10] Singer, A. (2011) Angular synchronization by eigenvectors and SDP. *Appl. Comput. Harmon. Anal.* 30:20–36.
[11] Bandeira, A.S., Singer, A., Spielman, D.A. (2013) A Cheeger inequality for the graph connection Laplacian. *SIAM J. Matrix Anal. Appl.* 34:1611–1630.
[12] Hartley, R., Trumpf, J., Dai, Y., Li, H. (2013) Rotation averaging. *Int. J. Comput. Vis.* 103:267–305.
[13] Govindu, V.M. (2004) Lie‑algebraic averaging for globally consistent motion estimation. *CVPR.*
[14] Hansen, J., Ghrist, R. (2019) Toward a spectral theory of cellular sheaves. *J. Appl. Comput. Topol.* 3:315–358.
[15] Lee, J.M. (2012) *Introduction to Smooth Manifolds*, 2nd ed. Springer.
[16] Zhang, Z., Zha, H. (2004) Principal manifolds and nonlinear dimension reduction via local tangent space alignment. *SIAM J. Sci. Comput.* 26:313–338.
[17] Brand, M. (2002) Charting a manifold. *NIPS 15.*
[18] Silverman, J.D., Washburne, A.D., Mukherjee, S., David, L.A. (2017) A phylogenetic transform enhances analysis of compositional microbiota data. *eLife* 6:e21887.
[19] Morton, J.T. et al. (2017) Balance trees reveal microbial niche differentiation. *mSystems* 2:e00162‑16.
[20] Washburne, A.D. et al. (2017) Phylogenetic factorization of compositional data. *PeerJ* 5:e2969.
[21] Martín‑Fernández, J.A. et al. (2018) Advances in principal balances for compositional data. *Math. Geosci.* 50:273–298.
[22] Birtea, P., Gavra, I. (2022) Parametric Lie group structures on the probabilistic simplex. arXiv:2206.03774; *J. Geom. Phys.*
[23] Scealy, J.L., Welsh, A.H. (2011) Regression for compositional data using distributions on the hypersphere. *JRSS‑B* 73:351–375.

*The instrument reads. The expert decides. The hashes carry the receipts.*
