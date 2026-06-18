# Study 3 — risk rotation (the macro altitude)

*The third financial study: the same real S&P 500 composition, amalgamated to the three Morningstar
super-sectors — **Cyclical / Sensitive / Defensive** — and read at the exact low-D end. Where Study 1
reads ten sectors in detail and Study 2 compares exchanges, this reads the **risk-on / risk-off balance**
of the whole market in one ternary. Deterministic; reproducible to `content_hash = df39da85…`;
descriptive, not advice. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001.*

Run: `python3 study3_risk_rotation.py`. Grouping (Morningstar): Cyclical = Financials, Consumer
Discretionary, Materials; Sensitive = Communication Services, Energy, Industrials, Information Technology;
Defensive = Consumer Staples, Health Care, Utilities.

## The reading

- **Balance:** Sensitive 0.525 → 0.550, Cyclical 0.258 → 0.243, Defensive 0.217 → 0.207.
- **Arrow of intent:** weight flowed **to Sensitive**, away from **both Cyclical and Defensive** — a
  quiet tilt toward the growth/sensitive complex (tech, communications, energy, industrials) at the
  expense of both the cyclical and the defensive ends.
- **Character:** coherence 0.097, path efficiency 0.077, **effective dimensionality 1.62** — about
  one-and-a-half independent directions. At the macro altitude the market is **Diffusive**: the big risk
  balance drifts and rebalances rather than marching, and it is far *simpler* than the ten-sector map.
- **Regime changes** at trading days 32, 80, 100, 194, 204, 209, 224, 246 — where the macro risk balance
  reorganised.
- **Exact:** at D=3 the composition rebuilds with zero reconstruction error.

## Why this altitude matters

The ten-sector map (Study 1) reads **Turbulent** — many sectors trading places, ~5 independent
directions. Collapse the same data to the three risk super-sectors and it reads **Diffusive** — ~1.6
directions, a gentle drift toward Sensitive. That is not a contradiction; it is **scale**: the churn
lives at the sector level, while the macro risk posture moves slowly and almost one-dimensionally. An
allocator who only watches the risk-on/risk-off dial would see calm; the instrument shows the calm is
real at that altitude *and* that the action is one level down. Same data, two honest answers, located by
reading it at two heights.

## Honest envelope

Tier 1 reading (reproducible to the hash); Tier 3 meaning (the expert's). Descriptive only — no forecast,
no probability, **not investment advice**. Public, aggregate data. The amalgamation is the standard
Morningstar super-sector grouping; a different grouping is a different (still exact) study.
