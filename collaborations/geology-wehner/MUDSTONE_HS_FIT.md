# Can Hs assist mudstone analysis? — a fit assessment (public)

**Short answer: yes — and it is arguably the strongest near-term entry point** — because mudstone chemostratigraphy is, in Hs's own terms, a compositional time-series on the simplex, which is exactly what the CNT engine reads. This is the honest case: the fit, the method mapping, the pitfalls, and a minimum credible demo. Research-grade and calibration-gated; Hs *assists* the geologist, it does not replace established methods or decide interpretations.

## Why the fit is natural
Mudstone chemostratigraphy measures **elemental / oxide composition** (XRF: major + trace) at closely spaced intervals **down a section** — depth is the ordering axis (a proxy for time via the age model). That is:
- **compositional** (parts of a whole, closed) — so log-ratio / Aitchison geometry applies, and
- **ordered** (a sequence) — so the *motion* between samples is meaningful.

CNT is built precisely for "ordered compositions": it reads the step-to-step trajectory down the section. The published **wavelet + compositional-data** chemostratigraphy approach (Wehner 2017) already lives in this space; CNT adds a deterministic *navigation / driver / regime* layer that pairs with it rather than competing.

## What CNT would add, reading a section down-depth
| CNT output | Chemostratigraphic meaning |
|---|---|
| **Aitchison step** ‖Δclr‖ (size of compositional change between samples) | sharp steps flag **surfaces** — sequence boundaries, flooding surfaces, condensed sections, ash beds, hiatuses |
| **Helmsman** (which element/oxide drives the change at each step) | *what is steering the section here* — e.g. detrital Al/Ti/Si ↔ carbonate Ca, or a redox-sensitive Mo/V/U/Re excursion |
| **Helmsman flips / directness** | one dominant driver = a directed depositional trend; steering bouncing = reorganization / mixed regime — a reading that maps onto systems-tract behaviour |
| **Regime tripwires** (entropy/drift thresholds) | objective, reproducible candidate **boundaries** where the depositional regime changes |
| **Deceptive drift** (Activation Coefficient: a *small-share* element doing *large* structural work) | a **trace** element punching above its abundance — a subtle redox / volcanic-ash / provenance marker the bulk view misses. The genuinely novel detector for this domain. |
| **Determinism + hash chain** | a byte-reproducible chemostratigraphic analysis — provenance for the published section |

Pairing: **CNT for the regime/driver structure; wavelet analysis for the periodicity (Milankovitch).** Complementary axes of the same signal.

## The honest pitfalls (these decide whether it works on real mudstone)
1. **Zeros / below-detection trace elements.** Mudstone trace data is full of detection-limit values. Hs's default crude floor (1e-15) would poison the geometry — **proper upstream Bayesian-multiplicative zero treatment is mandatory** before CNT ingest. Critically, this bites *exactly* in the trace elements where the deceptive-drift detector fires, so **any trace-driven flag must be sensitivity-tested against the replacement constant** — that is where false positives hide.
2. **Closure / subcompositional coherence.** Be explicit about what the composition is closed to (whole-rock major-oxide suite vs a trace sub-suite vs element ratios). Mixing frames silently breaks comparability; choose a coherent basis (a balance/SBP basis tied to mineralogy/provenance is ideal).
3. **Calibration is mandatory (the firmest requirement).** CNT applied to chemostratigraphy is a **candidate** application — exploratory, not validated. It must be anchored against established results and known sections: do its regime tripwires land on the published picked surfaces? does the helmsman name the expected driver? Characterise error/sensitivity before any interpretive claim.
4. **Warn, don't decide.** CNT flags candidate surfaces, drivers, and regimes; the geologist interprets. It is an instrument, not an oracle.

## Minimum credible demo (the publishable test)
Take a **published mudstone section** (e.g. an Eagle Ford XRF chemostratigraphic profile), treat the published interpretation as ground truth, then:
1. Proper zero treatment + a coherent compositional basis.
2. Run CNT down-section → bearing / Aitchison-step, helmsman, helmsman flips/directness, regime tripwires, deceptive-drift on the trace suite.
3. Overlay against the published picked surfaces and the published wavelet cyclicity: **does CNT independently recover the surfaces, and does deceptive drift surface any real trace-element signal the bulk view missed?**
4. Report the sensitivity of every flag to the zero-replacement constant and the basis choice.

Result if it holds: *"A deterministic compositional-navigation layer for mudstone chemostratigraphy"* — a methods contribution that complements wavelet + CoDa, with reproducible provenance, with domain expertise steering the standard.

## One-line verdict
Mudstone chemostratigraphy is a compositional time-series; CNT reads compositional time-series deterministically; the honest work is the zero-treatment, the calibration against known sections, and letting the deceptive-drift trace signal prove itself.

*Research-grade · calibration-gated · the instrument reads, the expert decides.*
