# USA EMBER — Diagnostic Note

**Date:** 2026-05-05
**Status:** Resolved (engine fix + data note)

## Initial finding

In the first v2.0.0 run on the EMBER 8-country battery, USA stood out as
anomalous:

| Country | T | D | curv δ | IR class | A      |
|---------|---|---|--------|----------|--------|
| CHN     |26 | 8 |   14   | CRITICALLY_DAMPED | 0.080 |
| DEU     |26 | 9 |    8   | OVERDAMPED_EXTREME | 0.918 |
| ...     |.. | . |   ..   | ... | .. |
| **USA** |**25**| 9 | **3** | **DEGENERATE** | — |

USA was T = 25 (the others were T = 26) and the curvature recursion
terminated at level 3 with no period-2 attractor detected — implausible
given USA's compositional richness.

## Two issues identified

### (1) Data — the file is one year short

The USA pipeline-ready CSV (`Current-Repo/Hs/data/Energy/EMBER_pipeline_ready/
ember_USA_United_States_generation_TWh.csv`) covers 2000–2024.

Every other country covers 2000–2025.

The newer EMBER 2025 release directory (`DATA/Energy/Embers 2025/
pipeline_ready/`) has CSVs for CHN, DEU, FRA, GBR, IND, JPN, WLD — but
**not USA**. The USA we are using comes from the older 2024 release.

Source data for USA 2025 does exist in
`DATA/Energy/Embers 2025/monthly_full_release_long_format.csv` (15,078
rows mention "United States"), but no one has yet extracted it to a
yearly pipeline-ready CSV.

**Status:** Recorded as a data omission. T = 25 vs T = 26 was not the
cause of the degeneracy — Japan worked fine at T = 26, and one year
fewer doesn't change the fundamental recursion structure. But the USA
file should be regenerated to include 2025 before the conference.

### (2) Engine — period-1 false positive at depth 2

USA's curvature trajectory was

```
L0 = 0.3224
L1 = 0.7920
L2 = 0.7959
L3 = 0.9907
```

The engine's `detect_period` checked period-1 first: `|L2 − L1| / L1 =
0.5 %` — under the 1 % gate. The depth sounder declared "limit cycle
period-1 at L2" and stopped.

But this is plainly a false positive: L3 jumps to 0.9907 — not a fixed
point at all. L1 ≈ L2 was a transient coincidence as Solar's CLR
component reached a brief plateau before the recursion continued.

The bug existed because period-1 detection only required ONE
consecutive convergence, while period-2 detection had ALWAYS required
TWO convergences (one even-parity, one odd-parity). The asymmetry was
the bug.

## Engine fix (2.0.0 → 2.0.1)

`detect_period` now requires TWO consecutive level pairs to satisfy the
precision condition for period-1 detection — mirroring the period-2
logic.

```python
# Before
for k in range(2, n):
    if abs(traj[k] - traj[k-1]) / max(abs(traj[k-1]), 1e-15) < precision:
        return (True, 1, ...)

# After
for k in range(3, n):
    rel_a = abs(traj[k]   - traj[k-1]) / max(abs(traj[k-1]), 1e-15)
    rel_b = abs(traj[k-1] - traj[k-2]) / max(abs(traj[k-2]), 1e-15)
    if rel_a < precision and rel_b < precision:
        return (True, 1, ...)
```

The principle: a period-N attractor requires N consecutive same-N-period
match conditions to be declared, not just one.

## Result after fix

USA recovers to a plausible position in the cohort:

| Country | T | D | curv δ | IR class | A      |
|---------|---|---|--------|----------|--------|
| CHN     |26 | 8 |   12   | CRITICALLY_DAMPED | 0.087 |
| DEU     |26 | 9 |    8   | OVERDAMPED_EXTREME | 0.918 |
| FRA     |26 | 9 |   14   | LIGHTLY_DAMPED | 0.265 |
| GBR     |26 | 9 |    6   | OVERDAMPED_EXTREME | 0.874 |
| IND     |26 | 8 |   11   | LIGHTLY_DAMPED | 0.262 |
| JPN     |26 | 8 |   13   | CRITICALLY_DAMPED | 0.038 |
| **USA** |25 | 9 | **16** | **LIGHTLY_DAMPED** | **0.218** |
| WLD     |26 | 9 |   14   | LIGHTLY_DAMPED | 0.290 |

USA at curv δ = 16 is the deepest in the cohort. With LIGHTLY_DAMPED
class and A = 0.22 it lands between France and World — consistent with
USA's transitional energy mix (gas-coal flip in 2016, growing renewables).

## Side effect — Ball / TAS recovery

The same false-positive bug had been silently affecting Ball / TAS
(geochem) — silica-ordered TAS bins were reported as DEGENERATE with
curv_depth = 3. After the fix:

```
geochem_ball_tas: curv δ = 12, IR = LIGHTLY_DAMPED, A = 0.094
```

Earlier journals had attributed this to "TAS bins are silica-defined
and pre-aligned, so the recursion can't develop." That claim is now
wrong — the bug was the engine, not the binning. TAS does converge to
a period-2 attractor like the other Ball schemes; the "degenerate by
design" finding in `ROBUSTNESS_JOURNAL_v2.md` was an artifact of the
1.0.0 / 2.0.0 detect_period bug, not a property of TAS.

The robustness journal (`ROBUSTNESS_JOURNAL_v2.md`) needs an erratum:
TAS curvature now converges, A = 0.094 (small but nonzero), period-2.
The general claim that period-2 attractor universality holds across
intraplate-volcanic compositions is **strengthened** by the fix.

Gold/silver D = 2 remains genuinely DEGENERATE — not a false positive,
because D = 2 has no off-diagonal metric structure for the recursion
to develop.

## Lessons

1. **Asymmetric rules are bugs in disguise.** Period-1 should always
   have required parity with period-2 logic — the historical "single
   consecutive match" was a shortcut.
2. **DEGENERATE is a hypothesis, not a verdict.** Three of the
   "DEGENERATE" results (USA, TAS, possibly USA-recurrence-tests) were
   engine artifacts. Whenever the engine reports DEGENERATE the operator
   should drill into the trajectory before believing it.
3. **The robustness journal's "degeneracy by design" reading** of TAS
   was wrong. The fix doesn't break the within-domain robustness story;
   it strengthens it (5/5 non-Higgins-extension geochem schemes now
   converge to period-2, including TAS).

## Outstanding action items

1. Regenerate USA pipeline-ready CSV from EMBER 2025 monthly long-format
   data. T = 26 then matches the other countries.
2. Add an erratum to `experiments/Hs-05_Geochemistry/region_binning/
   ROBUSTNESS_JOURNAL_v2.md` noting that the TAS DEGENERATE claim was
   the same bug.
3. Audit the Math Handbook entry on "DEGENERATE" classification — the
   IR class definition needs to distinguish "small-D / pre-aligned
   genuine degeneracy" from "engine couldn't detect convergence."

---

*The instrument reads. The expert decides. The loop stays open.*
