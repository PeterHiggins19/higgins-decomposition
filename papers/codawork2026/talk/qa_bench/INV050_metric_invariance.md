# Q&A bench card — INV-050 metric-invariance

**When to use:** if asked about TV vs Aitchison, metric robustness, or whether the verdict survives metric choice.

---

## The 30-second answer

> *"We compute both TV distance and Aitchison distance per timestep. They differ in magnitude — TV is bounded zero-to-one, Aitchison is unbounded. They agree on every shock hit-or-miss verdict across the 9-country EMBER 2001–2025 corpus. INV-050 in our catalog. The qualitative verdict is robust to substitution within this pair. Whether the invariance extends to weighted log-ratio distances, Mahalanobis on CLR covariance, or Egozcue–Pawlowsky-Glahn evidence information distance is open — that's Q2 in our three open questions."*

## If pressed further

**"How did you operationalise 'shock verdict'?"**
> *"Threshold on whether step-Δ is above the series median. The alternative threshold rules — z-scoring, Mahalanobis-style thresholding, quantile-relative — are worth testing. We have not done that."*

**"Why only two metrics?"**
> *"Catching the L2 → TV mislabelling in March 2026 gave us side-by-side computation, which revealed the pair-invariance. Extending to a broader family is exactly the question we're asking the room."*

**"Could the corpus be biased?"**
> *"Nine EMBER countries are a small corpus. The 73-country OWID expansion and the 101-dataset reference suite are available for anyone wanting independent verification."*

## What to NOT claim

- Do not say *"metric-invariant on the simplex"* — overclaim. The earlier framing was too broad. The push #39 sharpening narrows to **pair-invariance demonstrated for TV + Aitchison.**
- Do not say *"the family of valid simplex distances"* unless explicitly invoking Q2 as open.

## Receipts

- INV-050 in `ai-refresh/INVESTIGATION_CATALOG.json`
- Per-country verdicts inspectable in `papers/codawork2026/conference_2026_06/per_country/ember_*/cnt_v3.json`
- Sharpened framing in `papers/codawork2026/planning/NAMED_FINDINGS_FOR_CODA_DISCUSSION.md`
