# CoDaWork 2026 — Reply to Prof. Egozcue
## Ready to Paste

---

**To:** codawork2026@coda-association.org
**Subject:** Re: Revised abstract — Higgins, oral presentation

---

Dear Prof. Egozcue,

Thank you for your careful reply and your clear guidance. You are right — the original abstract on energy-mix drift monitoring is the better fit for CoDaWork, and I am grateful you steered me back to it. The broader instrument paper will benefit from the additional development time, and I will pursue it through a journal submission after the conference.

I would like to propose only minor wording refinements to the original abstract, not a change of scope. The pipeline has matured since the first submission, and the language can reflect that without altering the title or the focus. In particular, I would like to:

1. Name the instrument explicitly (the Higgins Decomposition, Hˢ) rather than describe it generically — this gives the audience a handle to refer to in discussion.
2. Add one sentence on amalgamation stability: classification is preserved when carriers are merged into coarser groupings (e.g., combining wind, solar, and bioenergy into a single renewable category). This is a CoDa-native result that the audience will recognise immediately.
3. Smooth the technical wording to reflect the current state of the pipeline — same scope, cleaner language.

I have pasted the refined abstract below (282 words). If you prefer that I retain the original text exactly as submitted, I am happy to do so.

One additional note: EMBER has released their 2025 Global Electricity Review, and the energy landscape has shifted dramatically since my original submission — renewables overtook coal generation globally for the first time in 2025, Germany now generates 45% of its electricity from wind and solar, Japan is restarting its nuclear fleet, and the current geopolitical situation has created the most volatile energy-mix period in decades. I plan to update the EMBER dataset to include the latest available data (through 2025) for the presentation, so the audience will see live drift detection on a system that is actively moving. Same method, fresh data, real-time relevance.

I look forward to Coimbra.

With respect,

Peter Higgins
Independent Researcher
Rogue Wave Audio — Markham, Ontario, Canada
PeterHiggins@RogueWaveAudio.com
https://github.com/PeterHiggins19/higgins-decomposition

---

## REFINED ABSTRACT (282 words)

**Title:** Compositional monitoring of energy-mix drift on the simplex

**Author:** Peter Higgins
**Affiliation:** Independent researcher, Markham, Ontario, Canada
**Preference:** Oral presentation

**Keywords:** compositional data analysis, Aitchison geometry, simplex, energy mix, electricity generation, drift detection, amalgamation stability, log-ratio pairs, EMBER

National electricity generation is a composition: carriers — coal, gas, oil, nuclear, hydro, wind, solar, bioenergy, other renewables — are parts of a whole that sum to total output. As countries restructure their energy portfolios, the generation mix traces a trajectory on the Aitchison simplex. Detecting and characterising this drift is a compositional problem.

We apply the Higgins Decomposition (Hˢ), a deterministic twelve-step diagnostic built entirely within Aitchison geometry, to EMBER electricity data for Germany, Japan, and the United Kingdom (2000–2024). Each national mix is represented as a 9-carrier composition on the 8-simplex. The pipeline applies simplex closure, CLR transform, cumulative Aitchison variance trajectory, and log-ratio pair stability analysis without domain-specific tuning or free parameters. Every run is SHA-256 verified: same input, same output, always.

Three results are reported. First, the pipeline automatically identifies the dominant drift carriers and ranks all D(D−1)/2 log-ratio pairs by stability, distinguishing structural transitions (coal-to-renewable substitution in Germany) from compositional stasis (nuclear baseload in France). Second, classification is stable under amalgamation: merging carriers into coarser groupings — for example, combining wind, solar, and bioenergy into a single renewable category — preserves the structural diagnosis in every scheme tested. Third, entropy invariance under geometric-mean decimation holds across temporal compression ratios of 2×, 4×, and 8×, confirming that the trajectory shape is robust to sampling resolution.

The method requires no forecasting model, no fitted parameters, and no subjective thresholds. It reads drift from the geometry of the simplex. We present the instrument, the results, and three open questions for the CoDa community: can the entropy invariance be proved from Aitchison geometry, does the classification survive ILR substitution for CLR, and what does the pipeline find on community benchmark datasets?

---

*Peter Higgins — PeterHiggins@RogueWaveAudio.com*
*https://github.com/PeterHiggins19/higgins-decomposition*
