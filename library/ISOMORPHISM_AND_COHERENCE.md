# Seeking isomorphism — and why the embedding needs coherence

*Peter's reframe (2026‑06‑15): "the engine should be seeking isomorphism, my guess on the embed need for coherence." Tested against the 107‑system Compositional Character Space. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker, tiered.*

---

## The reframe

"Same character" should mean **isomorphic**, not merely near. Two compositional systems share a character when a **structure‑preserving map** carries one system's dynamics onto the other's — a relabeling of parts composed with an Aitchison rotation (an element of the natural symmetry group: permutations × ILR isometries). Proximity of summary numbers is a proxy; the existence of the map is the truth.

This is the generalization of a result the engine already holds exactly. The **D=4 ILR ↔ unit‑quaternion S³ = SU(2) isomorphism** (Aitchison rotation = the quaternion sandwich q v q*, residual at the IEEE floor ~4.4e‑16 on Backblaze, Planck CMB, and Frielingen) is *the* exact isomorphism. "Character" promotes that one exact case to an approximate equivalence across systems. Seeking isomorphism is therefore not a new philosophy — it is the engine's deepest validated behavior, made the explicit goal of comparison.

**The profile is already isomorphism‑invariant.** Effective rank, momentum coherence, path efficiency, regime count, and entropy‑trend are each invariant under part‑relabeling and Aitchison isometry by construction (that was the point of the coherent helmsman and the closure‑invariant reads). So the CCS profile is a fingerprint of *what survives the symmetry group* — the engine was implicitly seeking isomorphism all along. The proposal is to make it active: construct the map and report the residual, the way the quaternion case does.

## The guess, tested — coherence organizes the embedding

Run on the 107‑system character matrix (`ccs_results.jsonl`):

- **Coherence is the principal axis.** PC1 carries **53% of total variance**, loaded coherence −0.51, path‑efficiency −0.46, effective rank +0.45 — i.e. the directedness/coherence axis. The embedding of Character Space is organized *around coherence* before anything else. (PC2 complexity 19%, PC3 trend 17%; three axes hold 89%.)
- **The embed‑need is governed by coherence, with the expected sign.** Per‑system embedding dimension (effective rank) anti‑correlates with coherence: **corr = −0.35** (path‑efficiency −0.37). Coherent systems collapse to few dimensions; incoherent systems need more. The dimensional cost is incurred exactly where coherence is absent.

**Reading:** *coherence is isomorphizability.* The coherent part of a system is the part that admits a clean structure‑preserving map (low residual — the quaternion floor is the limiting case). The incoherent part is the residual that resists the map, and that residual is what forces extra embedding dimensions. The "embed need for coherence" is literal: the embedding needs dimensions in proportion to the *failure* of coherence; the coherent core maps cleanly and costs almost nothing.

| Claim | Tier | Status |
|---|---|---|
| The CCS invariants are isomorphism‑invariant (permutation × isometry) | 1 | by construction |
| Coherence is PC1 (53%) and governs per‑system embed dimension (r≈−0.36) | 1 | measured, 107 systems |
| D=4 ILR↔S³ isomorphism, IEEE‑floor exact | 1 | reproduced on 3 datasets |
| "Character = isomorphism class"; coherence = isomorphizability | 2 | reasoned from the above |
| Embed‑need = dimension of the coherent (isomorphizable) subspace | 3 | conjecture — the next test |

## The source — it was the loudspeaker's design law

This result is not new physics; it is the **origin physics, recognized at the instrument level**. The framework began at Rogue Wave Audio with a ground state: an array of drivers controlled in time (phase/delay) and space (position) so their radiation sums to a *uniform, coherent composition* at the listening position — coherence engineered as the condition for reaching the isotropic ground state (the simplex barycentre). Two facts of that design reappear, measured, in Compositional Character Space: **coherence is the organizing axis** (it was the engineered quantity), and the **exact isomorphism is D=4** (the four drivers per cabinet → unit quaternion S³ = SU(2); stereo and quadraphonic are the D=8 and D=16 rungs). "Coherence is isomorphizability" is therefore the loudspeaker's design law generalized: the coherent field is exactly the one the exact four‑driver quaternion description fits; lose coherence and you get the residual that resists the map and costs dimensions. Origin document: `RWA/THE_GROUND_STATE.md` (§ *The drivers*). *(Tier 1 for the acoustic system + D=4 exactness; Tier 2 for the lineage to the abstract result.)*

## The concrete upgrade (next, at Peter's gate)

Promote the comparison step from *proximity* to *isomorphism‑seeking*:

1. For each system, isolate the **coherent subspace** of its CLR motion (the top modes the coherent helmsman keeps, above the discovered noise floor).
2. To compare A and B, search the symmetry group for the best **structure‑preserving map** — orthogonal Procrustes alignment of the coherent subspaces, composed with the optimal part‑permutation — and report the **alignment residual**.
3. **Residual → floor ⇒ isomorphic ⇒ same character** (the quaternion 4.4e‑16 is the exact‑isomorphism limit of this same residual). A nonzero residual is the incoherent remainder — and its rank is the extra embed‑need.

This makes character identity falsifiable per‑pair (a residual, not a cluster boundary), continuous with the exact quaternion result, and it operationalizes the guess: **the embedding dimension a class needs is the dimension of the coherent subspace its members share.** Cross‑dimensional systems (D differs) are compared at the level of the reduced coherent dynamics, not the raw composition — the isomorphism is of the *motion*, which is where "a market and a microbiome share a character" has to live.

*The engine already seeks isomorphism in everything it reports; coherence is the measure of how much of a system will submit to one. Making the search explicit turns the Character Table from a map of neighbourhoods into a map of equivalence classes — with a residual receipt on every claim.*
