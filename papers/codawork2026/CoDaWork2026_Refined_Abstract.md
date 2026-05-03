# CoDaWork 2026 — Refined Abstract (Original Scope)
## Minor Improvements Only — Amalgamation + Smoothed Wording

**Title:** Compositional monitoring of energy-mix drift on the simplex

**Author:** Peter Higgins

**Affiliation:** Independent researcher, Markham, Ontario, Canada

**Preference:** Oral presentation

**Keywords:** compositional data analysis, Aitchison geometry, simplex, energy mix, electricity generation, drift detection, amalgamation stability, log-ratio pairs, EMBER

**Abstract:**

National electricity generation is a composition: carriers — coal, gas, oil, nuclear, hydro, wind, solar, bioenergy, other renewables — are parts of a whole that sum to total output. As countries restructure their energy portfolios, the generation mix traces a trajectory on the Aitchison simplex. Detecting and characterising this drift is a compositional problem.

We apply the Higgins Decomposition (Hˢ), a deterministic twelve-step diagnostic built entirely within Aitchison geometry, to EMBER electricity data for Germany, Japan, and the United Kingdom (2000–2024). Each national mix is represented as a 9-carrier composition on the 8-simplex. The pipeline applies simplex closure, CLR transform, cumulative Aitchison variance trajectory, and log-ratio pair stability analysis without domain-specific tuning or free parameters. Every run is SHA-256 verified: same input, same output, always.

Three results are reported. First, the pipeline automatically identifies the dominant drift carriers and ranks all D(D−1)/2 log-ratio pairs by stability, distinguishing structural transitions (coal-to-renewable substitution in Germany) from compositional stasis (nuclear baseload in France). Second, classification is stable under amalgamation: merging carriers into coarser groupings — for example, combining wind, solar, and bioenergy into a single renewable category — preserves the structural diagnosis in every scheme tested. Third, entropy invariance under geometric-mean decimation holds across temporal compression ratios of 2×, 4×, and 8×, confirming that the trajectory shape is robust to sampling resolution.

The method requires no forecasting model, no fitted parameters, and no subjective thresholds. It reads drift from the geometry of the simplex. We present the instrument, the results, and three open questions for the CoDa community: can the entropy invariance be proved from Aitchison geometry, does the classification survive ILR substitution for CLR, and what does the pipeline find on community benchmark datasets?

---

*Peter Higgins — PeterHiggins@RogueWaveAudio.com*
*https://github.com/PeterHiggins19/higgins-decomposition*

---

**Word count:** 269
**Changes from original submission:**
1. Wording smoothed to reflect matured pipeline ("Higgins Decomposition (Hˢ)" named explicitly, "twelve-step diagnostic" rather than generic description)
2. One sentence added on amalgamation stability (classification preserved under carrier merging)
3. Three open questions added at close — consistent with the full framework but scoped to energy data
4. Year range updated to 2000–2024 (matching current EMBER release)
5. Title, scope, and data sources unchanged
