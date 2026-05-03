# Entropy Scale-Invariance: An Open Problem Report

**Filed:** 2026-04-29
**Context:** Response to Egozcue comments on CoDaWork 2026 abstract
**Status:** Open problem — requires investigation from inside the instrument

---

## The Concern

Prof. Egozcue correctly identifies that Shannon entropy H(x) = -Sum(x_i log x_i) is not scale invariant. For compositional data analysis, valid functionals must satisfy f(alpha * x) = f(x) for any positive constant alpha. Shannon entropy does not satisfy this.

The EITT (Entropy Invariance Through Transformation) claim in the Hs pipeline observes empirically that entropy changes very little under temporal decimation (2x, 4x, 8x compression). But "very little" is not "zero," and the question is whether this residual is noise, drift, or structure.

## The Deeper Question

The Hs pipeline operates on systems spanning approximately 44 orders of magnitude — from the cosmic energy budget (dark energy, dark matter, baryonic matter at the Planck scale) down to national electricity generation at the kilowatt-hour scale. The entropy behaviour at each scale is computed on the closed composition, meaning the closure operation normalises away the absolute magnitudes. But the question remains:

**Is the entropy residual under decimation constant across scales, or does it drift?**

If it drifts, the drift itself is a compositional signal — it tells us something about the smoothness of the trajectory on the simplex at that particular scale. A trajectory that is smooth (slowly varying compositions) will show very small entropy residuals under decimation. A trajectory with sharp transitions (sudden carrier substitution, phase changes) will show larger residuals.

This means the entropy residual is not a bug — it is a potential diagnostic. But it is scale-dependent, and that scale dependence is exactly what Egozcue warns about.

## The Self-Referential Property

Here is the critical insight: **the Hs instrument itself is the tool required to investigate this concern.**

The pipeline computes cumulative variance V(t), shape classification, and lock detection at every time step. These diagnostics characterise the smoothness and structure of the trajectory. If entropy drift exists at a given scale, the pipeline's own diagnostics should detect it as a change in V(t) trajectory shape or a shift in classification boundaries.

This creates a self-referential loop:

1. Feed the composition into Hs
2. Compute entropy at multiple decimation ratios
3. Measure the residual
4. Use the pipeline's own diagnostics to classify the residual
5. If the residual is structured, the pipeline detects it
6. If the residual is noise, the pipeline classifies it as stable

The instrument checks itself. This is not circular — it is the compositional equivalent of a telescope observing its own optical aberrations through a calibration target. The key requirement is that the calibration targets are known, which leads directly to the imaging system test suite.

## Egozcue's Alternative: Evidence Information

Egozcue and Pawlowsky-Glahn (2018) propose the evidence information I_e(x) = ||x||_a (the Aitchison norm) as a proper scale-invariant measure. This is a DfS (Dominant function under Subcomposition) — it decreases monotonically when parts are removed.

**Open question:** Can I_e(x) replace Shannon entropy in the EITT step? If the Aitchison norm is invariant under temporal decimation in the same way entropy approximately is, then EITT becomes a theorem rather than an empirical observation, because I_e is already a proper Aitchison-geometric quantity.

This substitution should be tested computationally across all existing experiments.

## Action Items

1. Compute I_e(x) = ||x||_a alongside H(x) for all existing experiments
2. Run temporal decimation tests with both measures
3. Compare residuals — does I_e show exact invariance where H shows approximate invariance?
4. If yes, replace Shannon entropy with evidence information in the EITT step
5. Run the imaging system calibration suite to establish baseline behaviour on known geometries

## Conclusion

Egozcue's comment is not a criticism — it is a research direction. The entropy concern points toward a deeper question about scale-dependent drift that the instrument itself is designed to detect. The resolution requires known-geometry calibration targets (the imaging system test suite) and a potential substitution of Shannon entropy with the Aitchison norm as the proper scale-invariant measure.

The tool must prove itself from the inside. That is what the calibration suite will do.
