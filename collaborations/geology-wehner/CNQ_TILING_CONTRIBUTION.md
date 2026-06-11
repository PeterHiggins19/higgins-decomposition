# CNQ‑Tiling — Contribution Statement, Citations, and Terms

*Principled announcement, 2026-06-10. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Grounded in the prior‑art assessment (`CNQ_TILING_PRIOR_ART.md`) and a second confirmation search. This document states plainly what is new, what we build on (with citations), and the specifications and terms under which the method operates — so the work reads as principled science and engineering, not a press release.*

---

## 1 · The contribution, stated plainly and proudly

**CNQ‑tiling is a deterministic method that reads the dynamics of compositional data by tiling the simplex with overlapping, exact four‑part quaternion charts and reconstructing the full high‑dimensional trajectory losslessly.** Its power comes from combining, into a single auditable pipeline, principles that have until now lived in separate fields — compositional data analysis, group synchronization, manifold‑chart alignment, and phylogenetic balances — and adding one new geometric reading that we could not find anywhere in the literature: **the identification of a four‑part composition's log‑ratio coordinates with a unit quaternion on S³ = SU(2), read through the rotation sandwich `q v q*`.** The whole pipeline is deterministic and hash‑chained: same input, same output, always, with a verifiable receipt at every step.

We are deliberately precise about which parts are ours and which we inherit. The honest position is the strong one: a method standing on Aitchison, Egozcue & Pawlowsky‑Glahn, Greenacre, Singer, Fiedler, Zhang & Zha, and Silverman is *grounded*, and the genuinely new layer is sharply defined and defensible.

---

## 2 · What is new

**(N1) The quaternion‑exact reading of a composition.** Treat the three isometric‑log‑ratio (ILR) coordinates of a four‑part composition as a point on S³ = SU(2) and read its rotational/navigation structure (bearing, handedness, time‑reversal by conjugation) with the unit‑quaternion sandwich product `q v q*`. An exhaustive two‑pass search (20+ query families across arXiv, peer‑reviewed statistics/mathematics/CS, and indexed scholarly pages) found **no prior work that joins compositional/Aitchison geometry to quaternions/S³/SU(2) in this way.** The two nearest neighbours are explicitly *different* constructions and are distinguished in §4.

**(N2) The deterministic synthesis.** Locally‑*exact* quaternion charts (not linear approximations) + *provably lossless* reconstruction from overlapping charts + a deterministic, hash‑chained pipeline, presented as one engineering system with published specifications and claim tiers. This is an **application/engineering contribution** — a new *combination and instrument*, not a new theorem. Its distinguishing axis from the closest data‑method prior art (LTSA; "Charting a Manifold") is that those use approximate local charts and produce lossy, reduced embeddings, whereas CNQ‑tiling's charts are exact and its reconstruction is information‑preserving (verified to ≈4×10⁻¹² at D=10⁶; see `CNQ_TILING_METHOD_AND_PROOF.md`).

Everything else in the method is prior art, cited and credited below. We do **not** claim the reconstruction theorem, the synchronization/Laplacian machinery, the manifold‑atlas concept, subcompositional coherence, or tree‑structured balances as new.

---

## 3 · What we build on — citations by component

| Component of CNQ‑tiling | Established principle we use | Cite |
|---|---|---|
| Log‑ratio geometry; CLR/ILR; Helmert orthonormal basis | Aitchison geometry; isometric log‑ratio coordinates; balances / sequential binary partition | Aitchison 1986; Egozcue, Pawlowsky‑Glahn, Mateu‑Figueras & Barceló‑Vidal 2003 (*Math. Geol.* 35:279); Egozcue & Pawlowsky‑Glahn 2005 (*Math. Geol.* 37:795) |
| Gluing overlapping subcompositions on shared parts | **Subcompositional coherence** (eponymous principle) | Aitchison 1982, 1986 |
| Reconstruct the full composition from a connected set of pairwise log‑ratios; explicit inverse | A connected DAG / spanning tree of log‑ratios carries all compositional information | **Greenacre 2019** (*Math. Geosci.* 51:649); **Greenacre 2020** (*Appl. Comput. Geosci.* 5:100017); Greenacre 2021 (*Annu. Rev. Stat.* 8:271) |
| Recover a global object from relative measurements on a graph; exact iff connected; conditioning ∝ diameter | **Group / angular synchronization** (scalar ℝ case); graph‑Laplacian "potentials from edge differences"; algebraic connectivity | Singer 2011 (*ACHA* 30:20); Bandeira, Singer & Spielman 2013; **Fiedler 1973** (*Czech. Math. J.* 23:298); Chung 1997, *Spectral Graph Theory* |
| Rotation/quaternion version of that reconstruction | **Rotation averaging / SO(3) synchronization** | Hartley, Trumpf, Dai & Li 2013 (*IJCV* 103:267); Govindu 2004 (CVPR) |
| Overlapping local charts aligned into a global structure | Manifold **atlas of charts + transition maps**; data instantiations | Lee 2012, *Introduction to Smooth Manifolds*; **Zhang & Zha 2004** (LTSA, *SIAM J. Sci. Comput.* 26:313); **Brand 2002** ("Charting a Manifold," NIPS 15) |
| Local‑to‑global gluing; obstruction = cohomology; sheaf Laplacian ⊃ graph Laplacian | **Cellular sheaves / sheaf Laplacian** (categorical home) | Robinson 2014, *Topological Signal Processing*; Hansen & Ghrist 2019 (*J. Appl. Comput. Topol.* 3:315) |
| Hierarchical / phylogenetic tree atlas for high‑D microbiome | **PhILR — phylogenetic ILR**; tree‑defined balances | **Silverman, Washburne, Mukherjee & David 2017** (*eLife* 6:e21887); Morton et al. 2017 (gneiss, *mSystems* 2:e00162‑16); Washburne et al. 2017 (PhyloFactor, *PeerJ* 5:e2969); Martín‑Fernández et al. 2018 (principal balances, *Math. Geosci.* 50:273) |
| Quaternion ↔ S³ = SU(2) ↔ SO(3); sandwich product; Hopf fibration; D=4 is the largest exact‑rotation algebra | Standard algebra/topology (for N1's machinery) | Gallier 2011, *Geometric Methods and Applications*; Hopf 1931 (*Math. Ann.* 104:637); Hurwitz 1898; Baez 2002 (*Bull. AMS* 39:145) |

---

## 4 · Distinguished from the nearest neighbours (so reviewers don't conflate)

- **Birtea & Gavra 2022** ("Parametric Lie group structures on the probabilistic simplex…," arXiv:2206.03774; *J. Geom. Phys.*) puts a **flat, commutative** (perturbation) Lie‑group structure on the simplex — verified to contain **no** quaternion, SU(2), S³, or rotation content. CNQ‑tiling's N1 uses the **curved, non‑abelian SU(2)** rotation reading. Different group, different geometry.
- **Scealy & Welsh 2011** (*JRSS‑B* 73:351) and the α‑transformation family (Tsagris et al. 2011) map compositions to a sphere via the **square‑root / Fisher–Rao** transform — a *different sphere* (curved positive orthant, no group structure, no quaternion multiplication). CNQ‑tiling uses the **flat ILR coordinates identified with S³ = SU(2)** and reads `q v q*`. Different map, different metric, no group action in theirs.
- **Kendall shape space / directional statistics (Mardia–Jupp)** use quaternions/S³ for **shapes and orientations**, not compositions. **Quaternionic colour processing** uses **raw RGB**, not log‑ratios. Different objects.

One precision note we state up front to any referee: "D=4 is special" means *three ILR degrees of freedom equal the dimension SU(2) rotates exactly*; the quaternions ℍ are four‑**dimensional** (1 real + 3 imaginary). The two "4"s coincide numerically for distinct reasons.

---

## 5 · The deterministic approach — specifications and terms

CNQ‑tiling is not an ad‑hoc procedure; it runs under published specifications and explicit operating terms.

**Specifications.**
- **HUF‑STD‑002 (Tensor Train):** the four hash‑linked links `Ingest&Treat → Geometry → Tile/Atlas → Navigate&Emit`. "Hs measures, HUF carries."
- **CN‑TT v4 engine design spec** (`ai-refresh/CNTT_V4_ENGINE_DESIGN.md`): the reference implementation, with parity acceptance criteria against the frozen v3.2.0/v2.0.0 oracle.
- **Method & proof** (`CNQ_TILING_METHOD_AND_PROOF.md`) and the runnable, journaled experiment (`experiments/cnq_tiling_highd_2026-06/`).

**Terms & conditions (the honest‑broker operating terms).**
1. **Determinism guarantee:** same input → same output, bit‑for‑bit; no statistics, no sampling in the science path; a canonical SHA‑256 receipt at every link.
2. **Claim tiers, always attached:** Tier 1 (verified/computed), Tier 2 (standard math, soundly applied), Tier 3 (to be earned by validation). No quantity is presented above its tier.
3. **Reconstruction validity condition:** lossless **iff** the chart atlas's co‑occurrence graph is connected; disjoint atlases are rejected, not silently approximated.
4. **Interpretation boundary:** the instrument reads; the domain expert decides. CNQ‑tiling produces geometry and provenance, not domain conclusions.
5. **Provenance & governance:** AI‑assisted per HUF‑STD‑001 (human authorship for all claims; no AI commits); HUF‑Gov carrier‑filter for need‑to‑know data; Apache‑2.0 (code) / docs‑licensed.

---

## 6 · Honest boundaries (what we do not claim, and the one open check)

- We do **not** claim, as new: the connected‑log‑ratio‑graph reconstruction theorem (Greenacre), group/angular synchronization or the Laplacian connectivity/conditioning facts (Singer; Fiedler; Chung), rotation averaging (Hartley; Govindu), the manifold‑atlas concept (Lee; LTSA; Brand), subcompositional coherence (Aitchison), or tree‑structured balances (PhILR; gneiss; PhyloFactor). These are prior art and are cited as such.
- **N1's novelty rests on an exhaustive but negative search result.** It is safe to announce now (to collaborators, internally, and in the repository). Before **formal journal submission**, run one more confirmation pass against Google Scholar, NASA ADS, Semantic Scholar, and a patent database (USPTO/WIPO) — the channels the web search could not reach directly — and add a non‑English CoDa‑community check. Until then, N1 is stated as "novel to the best of an exhaustive web‑indexed search," not as an absolute.
- **N2's novelty** is as a synthesis/instrument; its strength is demonstrated determinism and losslessness, not a claim of new underlying mathematics.

---

## 7 · Claim tiers for this statement

- **Tier 1 (verified):** all citations and attributions (DOIs/primary sources checked); the determinism and losslessness results referenced here (measured in the companion experiment).
- **Tier 2 (sound judgment):** the novelty framing of N1/N2 and the distinctions in §4.
- **Tier 3 (to confirm before formal publication):** the absolute novelty of N1 (pending the Scholar/ADS/patent/non‑English pass).

*The instrument reads. The expert decides. The hashes carry the receipts.*
