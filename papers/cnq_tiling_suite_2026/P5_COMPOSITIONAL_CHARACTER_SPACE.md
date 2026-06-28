# P5 — Compositional Character Space: a cross-domain taxonomy of compositional dynamics via the second-order read

*Draft. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker — claims tiered; the central dimensionality result is presented together with its own at-scale correction. Pairs with P4 (Compositional Kinematics), on which it depends.*

> **Movement IV — Character**, in the five‑part arc (exactness → trust → motion → **character** → vigilance). Builds on P1's exact reading, P3's trustworthy instrument, and P4's motion; the survey here turns the instrument on its own outputs. Suite narrative: [`../THE_HIGGINS_DECOMPOSITION_SERIES.md`](../THE_HIGGINS_DECOMPOSITION_SERIES.md).

---

## Abstract

Compositional data analysis characterizes one system at a time: a whole partitioned into parts, mapped into log-ratio (Aitchison) geometry, and described. We introduce the **second-order read (Hˢ²)**: apply a deterministic compositional-dynamics engine across many systems, take **each system's diagnostic profile — a vector of quantities invariant under the natural symmetry group (part relabeling × Aitchison isometry) — as itself a point**, and analyze the resulting space of systems. We call this **Compositional Character Space (CCS)**. Across **107 real longitudinal compositions spanning 13 domains** (national energy mixes, igneous geochemistry, gut microbiomes, financial-sector rotation, agricultural economies, a cosmic-energy budget including the Planck CMB, a climate-policy scenario, a municipal budget, a storage fleet, and human conversation drift), systems sort into four recurring **characters** — *Ballistic, Contested, Diffusive, Turbulent* — whose ordering by directedness is coherent across unrelated fields: the most directed systems are the cosmic microwave background, the world energy transition, and a designed climate-policy trajectory; the most churning are gut microbiomes, human conversation, and finely-resolved geochemistry. We find that **momentum coherence is the principal organizing axis** of CCS (53% of variance) and that a system's required embedding dimension is governed by its coherence (coherent systems are low-dimensional; incoherent systems require more dimensions). We interpret "character" as an **isomorphism class** of compositional dynamics, anchored by the exact D=4 ILR ↔ unit-quaternion (S³ = SU(2)) isomorphism, and argue that **coherence is isomorphizability**. The work is deterministic and reproducible to a content hash; we report, as part of the result, that an apparent tight dimensional collapse at a small sample (n=11) corrects to a milder one at scale (n=107) — a falsifiable claim behaving as designed.

## 1. Introduction

The log-ratio program (Aitchison; Egozcue & Pawlowsky-Glahn) gives compositions a coherent geometry, within which a single dataset can be described — biplots, balances, variation matrices. P4 (Compositional Kinematics) extends this to *motion*: position, velocity, momentum, curvature, and action of a compositional trajectory in Aitchison space, as a deterministic descriptive instrument.

This paper takes one further step. If the engine returns, for any system, a set of scalar **invariants** of its dynamics — invariants because they are unchanged by relabeling the parts and by Aitchison isometries — then those invariants are coordinates in a space whose points are *whole systems*. Reading that space is the second-order read. The question it answers is not "what is this composition doing?" but "**what kind of compositional system is this, among all of them?**"

## 2. Method — the second-order read (Hˢ²)

For each system we run the kinematics engine (P4) on its closed compositional time series and extract a profile of five invariants: **effective rank** (participation ratio of the CLR-trajectory SVD — intrinsic dimensionality of the motion), **momentum coherence** (alignment of the per-step arrow of intent), **path efficiency** (net displacement over path length in CLR space), **regime count** (hold-locked structural transitions above the discovered noise floor), and **diversification trend** (change in effective spread / compositional entropy). Each is invariant under permutation of parts and under Aitchison isometry by construction (§ engine: coherent helmsman, closure-invariant reads).

The systems × invariants matrix is standardized; its **effective rank** measures the dimensionality of Character Space, and its principal axes name what organizes it. Systems are assigned a **character** by directedness (mean of coherence and path efficiency) against complexity (effective rank). Everything is deterministic: same data → same table → same SHA-256.

## 3. Results

### 3.1 The four characters generalize across domains

107 systems in 13 domains populate four characters. Ordered by directedness, the extremes are cross-domain-coherent and independently sensible:

- **Most directed (Ballistic):** the Planck CMB energy budget, the world energy transition, an IIASA climate-policy scenario, a municipal budget. Three of these are *expected* to be directed (a near-frozen spectrum, a designed monotone trajectory, a planned budget) — the engine agreeing, with no domain input, is a sanity check.
- **Most churning (Diffusive/Turbulent):** the Crohn and ECAM gut microbiomes, human conversation drift, and high-resolution igneous geochemistry. A market, a microbiome, and a conversation share a *character* — many parts trading places with no committed heading — across biology, language, finance, and geology.

That cross-domain co-clustering of motion-character, recovered without any domain knowledge, is the substantive finding.

### 3.2 Coherence organizes the embedding

Principal-component analysis of the 107×5 invariant matrix:

| Axis | Variance | Dominant loadings |
|---|---:|---|
| PC1 | 53% | coherence −0.51, path-efficiency −0.46, effective-rank +0.45 (the directedness axis) |
| PC2 | 19% | regimes +0.55, effective-rank +0.54 (complexity) |
| PC3 | 17% | trend +0.80 |

Coherence is the principal axis of Character Space. Moreover, a system's **embedding dimension (effective rank) is governed by its coherence**: corr(effective-rank, coherence) = −0.35, corr(effective-rank, path-efficiency) = −0.37. Coherent systems collapse to few dimensions; incoherent systems require more. The embedding needs dimensions in proportion to the *failure* of coherence.

### 3.3 The dimensionality claim, and its at-scale correction

At a small, deliberately diverse sample (n=11), CCS effective rank measured 2.80 of 5 — an apparent tight collapse to ~3 character axes. **At scale (n=107) it is 4.13 of 5** (4.07 domain-balanced; 4.03 within energy alone — robust, not a sampling artifact of one domain). The clean ~3 was a small-sample impression; the durable redundancy is that the two directedness measures (coherence, path-efficiency; r=+0.73) move together, leaving roughly four independent axes. We retain only the milder claim: **Character Space is weakly low-dimensional, organized primarily by coherence.** This correction was logged in advance of the scale test as the explicit risk of a Tier-2 claim; we present it as evidence the method is falsifiable and self-correcting, not as an embarrassment to be hidden.

## 4. Interpretation — character as isomorphism class; coherence as isomorphizability

We interpret two systems sharing a character as their reduced dynamics being **isomorphic**: a structure-preserving map (a part-permutation composed with an Aitchison isometry) carries one system's coherent motion onto the other's. This generalizes a result the engine holds exactly — the **D=4 ILR ↔ unit-quaternion isomorphism** (Aitchison rotation = `q v q*`, residual at the IEEE floor ≈ 4.4×10⁻¹⁶ on three independent datasets) — promoting it from one exact case to an approximate cross-system equivalence. Because the CCS invariants are themselves symmetry-group invariants, the engine is implicitly classifying by isomorphism already.

The coherence result then reads cleanly: **coherence is isomorphizability.** The coherent part of a system is the part that admits a low-residual structure-preserving map (the quaternion floor being the limiting case); the incoherent part is the residual that resists the map, and that residual is precisely what costs embedding dimensions. This unifies §3.2 with the isomorphism picture and motivates the engine upgrade in §6.

**Provenance.** Both facts — coherence as the organizing axis, and the exactness at D=4 — trace to the instrument's acoustic origin. The method began as a loudspeaker ground state: an array of drivers controlled in time and space so their radiation sums to a uniform, *coherent* composition at the listening position, with four drivers per cabinet (D=4, the unit‑quaternion reading) and stereo/quadraphonic giving the D=8/D=16 rungs. Coherence was the engineered quantity and the four‑driver geometry was the exact case; Compositional Character Space recovers both by measurement on unrelated systems. The "coherence is isomorphizability" reading is the loudspeaker's design law generalized (origin: `RWA/THE_GROUND_STATE.md`).

## 5. Claims and limits (tiered)

- **Tier 1 (measured, reproducible):** the 107-system Character Table; the four characters and their cross-domain ordering; coherence as PC1 (53%) and its negative correlation with embedding dimension; the exact D=4 quaternion isomorphism.
- **Tier 2 (reasoned):** Character Space is weakly low-dimensional, organized by coherence; "character" is usefully read as an isomorphism class; coherence ≈ isomorphizability.
- **Not claimed:** a tight 3-axis manifold (the early figure corrected at scale); exhaustiveness of the four characters; that cross-domain co-clustering implies shared *mechanism* (it is shared *motion-character* only).

## 6. Reproducibility and next test

Reproduce with `library/ccs_batch.py` (checkpointed; runs the engine across the data hold) → `CCS_EXPANDED.json`; the n=11 demonstration is `library/hs_meta.py`; any new data is made engine-ready by `Hs-Kinematics/hs_data_prep.py`. The decisive next experiment, stated so it can refute the §4 conjecture: for pairs of systems, align their coherent subspaces by orthogonal Procrustes plus optimal part-permutation and report the **alignment residual**; if same-character pairs are more nearly isomorphic (lower residual) than cross-character pairs, and the residual's rank tracks the incoherence, the isomorphism reading and the coherence-governs-embedding result are confirmed together. The next sampling priority is **more domains, not more energy countries** — the energy corner is already saturated.

## References (to complete in the novelty pass)

Aitchison (1986), *The Statistical Analysis of Compositional Data*. Egozcue & Pawlowsky-Glahn (ILR, isometric log-ratio). Pawlowsky-Glahn, Egozcue & Tolosana-Delgado (2015), *Modeling and Analysis of Compositional Data*. Amari (information geometry). Replicator dynamics (evolutionary game theory) for the kinematics lineage. Prior-art context per `papers/PRIOR_ART_compositional_kinematics_2026-06-14.md`. The CNQ-tiling quaternion isomorphism per P1.

*One instrument, turned on itself: the geometry is CoDa's; the second-order read, and the character map it reveals, are the extension.*
