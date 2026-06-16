# Sparsity scope boundary — 90%-zero microbiome (2026-06-12)

*What survives high sparsity and what does not — the boundary the engine must respect. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker; claim tiers below. Reproduce: `python sparsity_demo.py`.*

---

## The question

Microbiome OTU/ASV tables are ~90% zeros. Does the instrument's reading survive that?

## The demonstration (D=200 taxa, T=40 samples, 92% zeros)

**Two paths, two fates.**

**The CLR log-ratio geometry does NOT survive — it becomes an artifact of the replacement δ.** As the fixed-δ replacement shrinks, the dominant "movers" the engine reads flip from the real abundant taxa to imputed rare-taxa noise, and the CLR radius inflates:

| δ (×min positive) | top-5 movers (taxa idx) | mean \|CLR\| radius |
|---|---|---|
| 0.65 | **6, 5, 2, 4, 1** — the real core taxa | 13.3 |
| 0.10 | 6, **107, 37**, 5, **72** — noise creeping in | 18.1 |
| 0.01 | **107, 37, 72, 75, 21** — all imputed noise; core gone | 25.6 |

The E-21 structural-zero drop removed only the all-zero taxa (37 of 200), leaving **still 90.2% zeros** — because a taxon present in even one sample is not *structurally* zero. So the engine-default fixed-δ replacement is the wrong method at this sparsity: **δ is a tuning knob that drives the answer.** This is the canonical CoDa sparsity trap.

**The zero-robust reads DO survive — δ-independent.** `K_eff` (computed on raw shares, 0·log0 = 0) read the real concentration cleanly, **8.71 → 5.30**, regardless of δ; the deceptive-drift label-permutation null ran without complaint (p = 0.85). These instruments take no logarithm, so zeros need no imputation.

## What the engine now does about it

`HCI-CNTT/engine/zero_methods.py` gained a **sparsity-regime detector**: above `sparsity_warn_at` (default 50%) it emits **`GD-SPZ-WRN`** and announces that the log-ratio geometry is replacement-dominated, recommending the data be densified **before** the log-ratio step. It also gained a **`policy='bayes'` Bayesian-multiplicative replacement** (`GD-ZBM-CAL`) — the count-aware, ratio-preserving treatment the CoDa community favours for sparse/sequencing data (Palarea-Albaladejo & Martín-Fernández): zeros receive Dirichlet-posterior mass; non-zero ratios are preserved exactly (subcompositional coherence; verified 1.2969 → 1.2969 in the self-test).

## Recommendation — the sparse-data path

At high sparsity, densify **before** the CLR/ILR step:
1. **Prevalence filter** — keep taxa present in ≥ X% of samples (standard microbiome practice).
2. **Agglomerate to phylogenetic balances** — SBP / the tree atlas the engine already carries.
3. **Bayesian-multiplicative replacement** (`policy='bayes'`) — count-aware, ratio-preserving; the CoDaWork-preferred treatment.

Then the full log-ratio instrument (helmsman, CNQ, tiling) is sound. The zero-robust reads (K_eff, TV, diversity, the deceptive-drift null) are valid on the raw sparse table as-is.

## Consistency with the framework's microbiome wins

This **sharpens, does not contradict**, the existing runs: the Crohn (975×48) and ECAM results used *prevalence-filtered / agglomerated* taxa (D=48, not a raw 90%-zero table), and the headline there was the **K_eff** maturation read (ρ = 0.71) — exactly the zero-robust path. The scope boundary is now explicit: **K_eff/diversity/null instruments — sound on raw sparse data; the log-ratio geometry instrument — densify first.**

## Claim tiers

- The demonstration (δ-dependence vs K_eff stability) and the registry detector + Bayesian-multiplicative method — **Tier 1** (computed, self-tested, reproducible).
- The recommended densification paths — **Tier 2** (standard CoDa, soundly applicable).

*The instrument flags; the expert decides. At 90% zeros it now flags: the geometry is reading your imputation, not your biology — densify first.*
