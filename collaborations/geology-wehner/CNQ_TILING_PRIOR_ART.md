# CNQ-Tiling — Prior-Art Assessment

*Prior-art search, 2026-06-10. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Method: five parallel literature searches, each decomposing the CNQ-tiling concept into one mathematical component, hunting the established named principle behind it, with adversarial verification of citations against primary/DOI sources. Companion to `CNQ_TILING_METHOD_AND_PROOF.md` and `HIGHD_DETERMINISTIC_SCALING.md`.*

---

## The question

"CNQ tiling" is an internal name — a literal search returns nothing. The honest question is whether the **underlying mathematics** is supported as a named principle and method elsewhere, by whom, and therefore what is established prior art versus what (if anything) is novel.

## Headline verdict

**No single named principle "is" CNQ-tiling — it is a *synthesis* of several established, named principles, plus one component for which no prior art was found.** Four of the five mathematical pillars are well-established and correctly attributable to existing peer-reviewed work; treating them as prior art (and citing them) is the honest and credibility-strengthening move. The genuinely unoccupied piece is the **quaternion reading of a 4-part composition** (ILR→S³=SU(2) exact rotation), which — on this search — appears novel, with the caveat that this is a negative result and should be confirmed with a Google Scholar / arXiv pass before any printed novelty claim.

This is good news, not bad: a method built from Aitchison, Egozcue/Pawlowsky-Glahn, Greenacre, Singer, Fiedler, Zhang–Zha, and Silverman is *grounded*, not crankish. The defensible position is "a deterministic synthesis of established compositional, synchronization, and manifold-atlas principles, with a novel quaternion exactness layer at D=4" — far stronger before a skeptical reviewer than an unsupported "new principle" claim.

---

## Component-by-component findings

| # | CNQ-tiling component | Closest established named principle | Originator(s) / key citation | Match |
|---|---|---|---|---|
| 1 | CLR/ILR with Helmert orthonormal basis | Isometric log-ratio coordinates; balances/SBP | Aitchison 1982/1986; Egozcue, Pawlowsky-Glahn, Mateu-Figueras, Barceló-Vidal 2003 (*Math. Geol.* 35:279) | **Exact** |
| 2 | Gluing overlapping subcompositions on shared parts | **Subcompositional coherence** | Aitchison 1982/1986 (eponymous principle) | **Exact** (justifies the gluing; doesn't itself reconstruct) |
| 3 | Reconstruct the full composition from a connected set of pairwise log-ratios (overlap necessary) | A connected DAG/spanning tree of log-ratios carries all compositional information; explicit inverse exists | **Greenacre 2019** (*Math. Geosci.* 51:649), **Greenacre 2020** (*ACAGS* 5:100017), Greenacre 2021 (*Annu. Rev. Stat.*) | **Exact** — this is a known theorem, **not novel** |
| 4 | Recover global from overlapping local / relative measurements on a graph via the graph Laplacian; exact iff connected; conditioning ∝ diameter | **ℝ/translation group synchronization** (scalar case of group synchronization); Laplacian "potentials from edge differences"; algebraic connectivity (Fiedler value) | Singer 2011 (*ACHA* 30:20); Bandeira–Singer–Spielman 2013; **Fiedler 1973**; Chung 1997 (*Spectral Graph Theory*) | **Exact** — foundational, **not novel** |
| 4b | Rotation/quaternion version of the same reconstruction | **Rotation averaging / SO(3) synchronization** | Govindu 2004 (CVPR); Hartley, Trumpf, Dai, Li 2013 (*IJCV* 103:267) | **Strong** (curved/non-abelian sibling) |
| 4c | Categorical "local-to-global gluing, obstruction = cohomology" home | **Cellular sheaves / sheaf Laplacian** (reduces to graph Laplacian in our case) | Robinson 2014 (*Topological Signal Processing*); Hansen & Ghrist 2019 (*JACT* 3:315) | **Strong** (proper general framework) |
| 5 | Overlapping local exact charts aligned into a global structure | **Atlas of charts + transition maps**; data instantiations **LTSA** and **"Charting a Manifold"** | Lee 2012 (*Intro to Smooth Manifolds*); **Zhang & Zha 2004** (LTSA, *SIAM J. Sci. Comput.* 26:313); **Brand 2002** (NIPS, "Charting a Manifold") | **Strong** — but those are *linear/approximate, lossy*; ours is *exact/lossless* (the real difference) |
| 6 | Phylogenetic/hierarchical tree atlas for high-D microbiome | **PhILR — phylogenetic ILR**; tree-defined balances | **Silverman, Washburne, Mukherjee, David 2017** (*eLife* 6:e21887); Egozcue & Pawlowsky-Glahn 2005; gneiss (Morton 2017); PhyloFactor (Washburne 2017); principal balances (Martín-Fernández 2018) | **Exact** — firmly established, **do not claim as new** |
| 3↔quaternion | A 4-part composition's ILR coords ↔ unit quaternions / S³ / SU(2), read with the sandwich `q v q*` | *No prior art found.* (Quaternion↔SO(3) math is textbook — Gallier, Hopf 1931, Hurwitz 1898, Baez 2002 — but its application to **compositions** was not found) | nearest: sqrt/Fisher–Rao "spherical CoDa" (Scealy & Welsh 2011) — a **different** sphere, no quaternions | **Novel (negative result)** |

---

## The three-part verdict

**(a) Is "CNQ-tiling" supported as a named principle under any name?**
No — there is no single named principle that is the whole method. It is a synthesis. The names that come closest, by piece: *subcompositional coherence* (the gluing), *log-ratio-graph reconstruction / Greenacre's connected-DAG result* (the reconstruction), *ℝ-group synchronization + graph-Laplacian connectivity* (the engine), *manifold atlas / LTSA / "charting a manifold"* (the chart-alignment scaffolding), and *PhILR* (the phylogenetic tree atlas).

**(b) Established prior art vs. possibly novel.**
- **Established (cede freely, cite as prior art):** the reconstruction theorem (connected log-ratio graph → composition recoverable up to closure, with explicit inverse — Greenacre); the graph-Laplacian/synchronization machinery and the connected-iff-recoverable + diameter-conditioning facts (Singer, Fiedler, Chung); the overlapping-local-charts-aligned-globally scaffolding (LTSA, Brand, Lee); and the tree-structured balances for high-D microbiome (PhILR, gneiss, PhyloFactor).
- **Apparently novel (with caveats):** (i) the **D=4 quaternion exactness reading of compositions** — ILR→S³=SU(2)→`q v q*` on a composition — no prior art found; (ii) the **specific operational synthesis**: *locally-exact* quaternion charts + *provably lossless* overlap reconstruction + deterministic/hash-chained pipeline as one auditable engine. Note (ii) is an *engineering/application* contribution, not a new theorem; and the LTSA/Brand contrast (their charts are approximate and their output lossy, ours exact and lossless) is the honest axis on which the chart layer differs.

**(c) Citation guidance.**
- **Cite, do not claim as new:** Aitchison 1986 (subcompositional coherence, CLR); Egozcue et al. 2003 + Egozcue & Pawlowsky-Glahn 2005 (ILR, balances/SBP); **Greenacre 2019/2020** (reconstruct composition from a connected log-ratio graph — this is your reconstruction theorem, attribute it); Singer 2011 + Fiedler 1973 + Chung 1997 (synchronization + Laplacian connectivity/conditioning — your reconstruction *engine*); Hartley 2013 / Govindu 2004 (rotation averaging — pre-empts "this is just rotation averaging"); Zhang & Zha 2004 + Brand 2002 + Lee 2012 (the chart-atlas scaffolding); **Silverman et al. 2017 (PhILR)** + gneiss + PhyloFactor (the phylogenetic tree atlas — *cite prominently*, it is essentially the same tree-balance idea). Optionally Robinson 2014 / Hansen–Ghrist 2019 (sheaf framework) as the rigorous categorical home.
- **Position novelty narrowly and honestly:** the quaternion-exact D=4 reading of compositions, and the deterministic locally-exact + lossless synthesis — *as an application/engineering advance built on the above*, not as a new mathematical principle.
- **Do NOT claim as new:** reconstruction-from-connected-graph; tree-structured balances; the graph-Laplacian/synchronization result; the manifold-atlas concept; subcompositional coherence.

---

## Honest caveats on this assessment

- The quaternion-composition **novelty is a negative search result** ("not found"), which is weaker than a positive finding. The search agent flagged that WebSearch under-indexes recent/niche and non-English preprints and recommended a confirmatory **Google Scholar + arXiv** pass on terms like `"compositional" "quaternion"`, `"ilr" "SU(2)"`, `"Aitchison" "S^3"` before asserting novelty in any paper. **Do not print "novel" without that pass.**
- A precision point a referee will probe: "D=4 is special" rests on *3 ILR degrees of freedom = the 3-D space SU(2) rotates exactly*; quaternions ℍ are 4-**dimensional** (1 real + 3 imaginary). The two "4"s coincide numerically for different reasons — state it precisely (the quaternion search agent flagged this).
- The standard "compositions on a sphere" literature (Scealy & Welsh 2011; the √-transform / Fisher–Rao orthant) is a **different** construction (curved orthant, no group/quaternion structure). Distinguish it explicitly so reviewers don't conflate the two.
- SBP/balances are by construction **non-overlapping**; CNQ-tiling's *overlapping* charts are deliberately outside standard SBP — a genuine, citable point of difference (and exactly where the synchronization/sheaf framing, not the CoDa-balance framing, applies).

## Claim tiers for this document

- **Tier 1 (verified):** every cited result and attribution above (DOIs/primary sources checked by the search agents).
- **Tier 2 (sound judgment):** the match-closeness ratings and the cite/don't-claim guidance.
- **Tier 3 (to confirm):** the *novelty* of the quaternion-composition link (negative result — needs the Scholar/arXiv pass); whether the locally-exact+lossless synthesis survives as novel once compared line-by-line against LTSA/Brand and Greenacre in full.

*The instrument reads. The expert decides. The hashes carry the receipts. — Sources verified against publisher/DOI/arXiv primary pages during the search.*
