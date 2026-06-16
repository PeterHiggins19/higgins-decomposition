# Deceptive-drift null model — results and recommendation (2026-06-12)

*Closes the Q3 / S1-7 gate ("a defensible null choice required before final submission") and gives P2 a real footing. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker; claim tiers below. Reproduce: `python deceptive_drift_null.py` → `content_sha256: 0022de045169c2c23c88b6941c7f98421f84790f65170ac4808c332e2ce6c9f5`.*

---

## The question

"Deceptive drift" = the mix **concentrating** (effective number of fuels `K_eff` falling) while step-to-step motion (total-variation distance `TV`) stays **quiet** — the size/velocity view looks calm while the structure shifts underneath. You cannot label a country "deceptive" without a **null** that separates a real concentration-while-quiet coupling from chance. That null was the open gate.

## What we found about the null itself (a methods result)

Two nulls were built and tested:

- **Naïve composition time-shuffle (BIASED — do not use).** Permute the year order of the compositions and recompute. It fails its own self-test and returns p ≈ 1 for every country, because **the true trajectory is the smoothest ordering** (consecutive years are similar ⇒ low TV everywhere). Any TV-based statistic is confounded by that smoothness. Kept in the code as a documented trap.
- **Label-permutation null (RECOMMENDED — smoothness-invariant).** Hold the TV values fixed; permute *which* steps are labelled "concentration" (`K_eff` falling). Statistic = mean TV-rank of the concentration steps (low rank ⇒ concentration is quiet ⇒ deceptive). This tests exactly the deceptive hypothesis without the smoothness bias. **Self-test passes:** planted-deceptive p = 0.0001 (PRESENT), loud-concentration p = 1.0000 (absent), random p = 0.68 (absent).

## Result — EMBER nine countries, annual grain, whole record (2000–2025)

| Country | #conc | #div | mean TV-rank | p | class | prior deck |
|---|---|---|---|---|---|---|
| **AUS** | 6 | 19 | 5.00 | **0.0011** | **PRESENT** | present |
| CHN | 6 | 19 | 9.33 | 0.085 | absent (borderline) | present |
| WLD | 6 | 19 | 9.33 | 0.089 | absent (borderline) | absent |
| GBR | 9 | 16 | 11.67 | 0.264 | absent | present |
| USA | 6 | 18 | 13.00 | 0.595 | absent | absent |
| FRA | 10 | 15 | 15.00 | 0.871 | absent | absent |
| IND | 12 | 13 | 15.17 | 0.926 | absent | present |
| JPN | 10 | 15 | 15.70 | 0.934 | absent | present |
| DEU | 6 | 19 | 18.17 | 0.978 | absent | absent |

**At annual grain, deceptive drift is significant (p < 0.05) only for Australia.** The deck's "5 of 9" (AUS, CHN, GBR, IND, JPN) **does not survive the null at annual grain** — only AUS does; CHN and WLD are borderline; the rest are clearly not deceptive (DEU/JPN/IND concentrate *loudly*, if at all).

## Reading it honestly

This **confirms and sharpens** the existing `DECEPTIVE_DRIFT_REPORT.md` caveat. Over 2000–2025 these mixes are **diversifying** (`K_eff` rises in every country — solar/wind added breadth), so "quiet concentration" is the exception, not the rule. The packet's headline deceptive signal (Germany, **p = 0.0016**) is a **monthly, deseasonalised, pre-shock** result; annual data smooths the monthly quietness away. So:

- The `K_eff` concentration side is grain-robust; the **TV-quietness qualifier is grain-dependent** — that is the real, falsifiable finding.
- The prior annual-grain "5 of 9 present" was **not null-supported**; AUS is the one annual case that genuinely is.

## Recommendation for P2 / S1-7

1. **Adopt the label-permutation null** as the canonical deceptive-drift null (smoothness-invariant, self-tested, deterministic, hash-receipted). *(Ratified direction from Peter, 2026-06-12: time-shuffle family — corrected here to the label-permutation form that removes the smoothness confound.)*
2. **Run it at monthly grain.** The pipeline `monthly_deceptive_drift.py` is now **built and self-tested** (deseasonalisation removes the month-of-year cycle; 6-month sliding window; the same label-permutation null; planted-deceptive p = 0.0008 detected, pure-seasonality p = 0.31 correctly *not* flagged). It only needs **monthly long-format EMBER data** (not in the repo — annual is all that ships) wired into `load_monthly_ember()`. That is where the packet's p = 0.0016 lives and where the honest reproduction belongs.
3. **Frame P2 around the grain-dependence**: concentration is detectable at both grains; the *deceptive* (quiet) qualifier needs monthly resolution; AUS is the annual-grain exemplar. This is a stronger, more defensible paper than an annual "5 of 9" that a null dissolves.

## Claim tiers

- The null, its self-test, and the reproducible EMBER run — **Tier 1** (implemented, verified, hash-receipted).
- The annual-grain finding ("1 of 9; prior 5-of-9 not null-robust annually") — **Tier 1** (computed).
- The monthly-grain expectation and the P2 framing — **Tier 2** (sound, to be run).

*The instrument flags; the expert decides. The null says: at annual grain, the deception is mostly diversification wearing a costume — only Australia is genuinely concentrating in the quiet.*
