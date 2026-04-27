# CoDaWork 2026 — Letter and Revised Abstract
## For Juan José Egozcue, Chair of Scientific Committee

---

## Part 1: The Letter

Dear Professor Egozcue,

Thank you again for the invitation to present at CoDaWork 2026 in Coimbra. I am grateful for the oral presentation slot.

Since submitting the original abstract in March, the project has developed considerably. The energy-mix drift monitoring protocol described in that submission remains valid work, but it now represents only one application within a broader compositional diagnostic framework that has matured over the past several weeks.

The original abstract proposed a perturbation-based drift detector for energy portfolios. The work has since grown into a general-purpose compositional analysis instrument built entirely on Aitchison geometry — using simplex closure, CLR transform, Aitchison variance, geometric-mean operations, log-ratio pairs, and amalgamation as its foundational operations. The instrument has been validated across 25 experiments spanning 18 domains, from nuclear binding energy to cosmological composition to municipal budgets, all using the same twelve deterministic steps.

I would like to submit a revised abstract that better reflects the current state of the work and, I believe, offers more to the CoDaWork community. The original energy-mix application would appear as one validated example within the broader framework rather than as the sole contribution.

The revised abstract is below. If the scientific committee prefers that I stay with the original submission, I am happy to do so — the energy-mix work is complete and ready to present. But if there is flexibility, I believe the revised contribution has more to offer to the discussions in Coimbra, particularly around amalgamation, entropy properties of the geometric mean, and cross-domain compositional comparison.

I look forward to seeing you in June.

With respect,

Peter Higgins
Independent Researcher
Markham, Ontario, Canada
PeterHiggins@RogueWaveAudio.com

---

## Part 2: Revised Abstract

**Title:** The Higgins Decomposition: a deterministic compositional diagnostic on the Aitchison simplex

**Author:** Peter Higgins

**Affiliation:** Independent researcher, Markham, Ontario, Canada

**Keywords:** compositional data analysis, Aitchison geometry, simplex, amalgamation stability, entropy invariance, log-ratio pairs, deterministic diagnostics, cross-domain composition

**Abstract:**

This contribution presents a deterministic diagnostic instrument for compositional data that operates entirely within Aitchison geometry on the simplex. The instrument decomposes into seven sequential operators — simplex closure, variance trajectory, CLR transform, classification, entropy test, mode synthesis, and report — each inheriting a determinism axiom: same input, same output, always. Four of the seven operators are standard CoDa operations; two contain open questions for the community.

The instrument has been applied to 25 systems across 18 domains and 44 orders of physical magnitude, including nuclear binding energy, cosmological composition (Planck 2018), particle physics branching ratios (HEPData), geochemistry, energy-portfolio drift, and municipal budget allocation. All systems are analysed using the same twelve steps with no domain-specific tuning.

Three empirical results are reported. First, classification stability under amalgamation: across 58 amalgamation schemes applied to five datasets, the compositional classification is preserved in every case (100%). Amalgamation is used not for data reduction but as a structural diagnostic — testing which features survive regrouping and which vanish inside merged carriers. In the Planck 2018 cosmological data, two ratio locks (CDM/Baryon and Photon/Neutrino, both CV = 0) survive all amalgamation levels, corresponding to known conservation laws. These become invisible when their carriers are merged, providing a concrete quantification of what subcompositional incoherence hides and what it preserves.

Second, entropy invariance under geometric-mean decimation (EITT): Shannon entropy computed on the simplex is empirically invariant (variation < 5%) when observations are replaced by their pairwise geometric-mean blocks at compression ratios of 2, 4, and 8. This holds across all natural systems tested and fails only under extreme carrier hierarchy (five or more orders of magnitude between largest and smallest carrier). The geometric mean is the Aitchison centre; this invariance may be a consequence of simplex geometry, but no formal proof is offered. The conjecture is presented as an open question.

Third, the instrument produces a seven-dimensional compositional fingerprint (shape, fit quality, classification, constant family, entropy stability, turbulence level, drift direction) that enables cross-domain geometric comparison. Systems from unrelated domains that share a fingerprint share compositional geometry — a structural homology detectable without domain knowledge.

The instrument is deterministic and reproducible: every run produces a SHA-256 hash that is bit-identical on repeated execution. All code, data, and documentation are publicly available. Three open questions are posed directly to the CoDaWork community: (1) Can the EITT entropy invariance be proved from Aitchison geometry? (2) Does the variance-trajectory classification survive the substitution of ILR for CLR? (3) Independent validation on datasets held by CoDa practitioners.

Peter Higgins
PeterHiggins@RogueWaveAudio.com
https://github.com/PeterHiggins19/higgins-decomposition
