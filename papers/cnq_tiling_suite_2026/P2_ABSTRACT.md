# P2 — Deceptive drift (abstract only)

*The repo holds the abstract; the **full paper lives off-repo** in the CoWorker `arXiv/P2_deceptive_drift/`
folder. Once posted it will cite the arXiv paper; the paper cites the Hˢ work location below. Author: Peter
Higgins; AI-assisted per HUF-STD-001.*

**Deceptive drift: detecting concentration that hides behind quiet compositional motion.**

> In a compositional time series, concentration can increase steadily while the step-to-step composition
> barely moves — the system tightens without any loud transition. We define **deceptive drift**: an interval
> where the effective number of categories (K_eff = exp(Shannon entropy) on the closed composition) declines
> while the total-variation step distance stays below the series median. We give an operational detector,
> demonstrate it on the EMBER national electricity-generation corpus (signature reproduces in 5 of 9
> countries, 2001–2025), and position it against existing compositional monitoring. The contribution is
> narrow: fusing a *concentration trend* and a *movement-magnitude trend* into a single divergence detector.

**Work done in Hˢ:** the deceptive-drift null + EMBER run (`experiments/`, `DATA/Energy/`); the detector in the engine guard layer. **Full paper:** `arXiv/P2_deceptive_drift/` (off-repo). **arXiv:** link added once posted.
