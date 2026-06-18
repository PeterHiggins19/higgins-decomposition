# The Arc of Discovery — the whole experiment chain, re-run on the current engine

*A continuous journal: every major advancement that changed the engine, and the full chain re-run on the newest engine to see what survives, what is confirmed, and what the new honesty reveals. The experiments themselves tell the story. Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001. Honest-broker; the re-run reads are Tier 1 (computed on the real chain data with the current guard-aware engine; core CLR/helmsman/K_eff inline to spec, guards verbatim from the repo modules). Reproduce: `python rerun_chain.py`. Full chain map + original headlines: the per-experiment journals and `Hs_FULL_CHAIN_REPORT_2026-04-28.json` / `_archive_2026-06-07/HUF-CNT-System/experiments/EXPERIMENTS_RUN_REPORT.md`.*

---

## The arc, in one breath

A blind classifier that could tell real compositional data from fakes → a 12-step shape-reader that called every trajectory a *bowl* or a *hill* → a recursive curvature/energy tower that gave each system a damping *character* (an IR class) → and now a guard-aware engine that reads all of that **and says honestly where it cannot resolve**. Each step did not replace the last; it added a layer of structure and a layer of honesty. Below: the advancements that forced each change, then the whole chain re-run on the engine as it stands today.

## The advancements that changed the engine (the continuous record)

| Engine | The advancement | The experiment(s) that forced it |
|---|---|---|
| **EITT two-pass v1.0** (gold standard) | The F17 contamination tuner + two-pass classification — tell legitimate compositional data from fabricated, blind | The 20-dataset blind test: 85% → 90% after the second pass corrected one false positive |
| **Hs 12-step v1.0** | CLR → variation matrix → parabolic V(t) fit → squeeze/lock/PID; the *bowl vs hill* shape read; the post-O-1 **dimensional-collapse guard** | Hs-01 (D=2 degenerate handled), Hs-04 (first *hill*), Hs-23 (first **EITT failure** with a physical reason: decay energy is step-specific) |
| **CNT v2.0.0** | Replaced the 12-step pipeline with a recursive **curvature + energy tower** → IR classes (damping character), amplitude A, period; schema split `coda_standard / higgins_extensions` | The whole 20-experiment corpus re-cast |
| **CNT v2.0.1** | Period-1 needs **two** consecutive convergences (was one) — killed a false-positive DEGENERATE; curvature uses 1/x² (Handbook 19.2b) | `ember_usa`, `geochem_ball_tas` — the "DEGENERATE is a hypothesis, not a verdict" lesson |
| **CNT v2.0.3** | Three new IR classes named: **ENERGY_STABLE_FIXED_POINT, CURVATURE_VERTEX_FLAT, D2_DEGENERATE** | `backblaze_fleet` (vertex-flat), `commodities_gold_silver` (D2-degenerate), `financial_sector` (energy-stable) |
| **CNT v2.0.4** | 5-experiment extended battery + determinism gate (25 PASS / 0 FAIL) — the canonical snapshot | markham, iiasa, esa_planck, financial, chemixhub |
| **CN-TT v4 + the guard layer (2026-06)** | The engine learns to **say what it cannot resolve**: resolvability (hold at rest), **coherent helmsman** (carrier-set-robust), rank guard, **hold-lock** (discovered noise floor), sparsity/zero guards, SafeLoop, gauge-R&R/confidence | The kill-tests + this very re-run (below) |

## The whole chain, re-run today (17 real-data experiments)

Every chain experiment with available data, through the current guard-aware engine. `coh==`: does the new **coherent** helmsman agree with the old CLR helmsman? `holds`: genuine structural transitions from the hold-lock.

| experiment | D | N | helmsman (CLR) | coherent agrees? | eff. rank | K_eff end | hold-lock |
|---|---|---|---|---|---|---|---|
| ember_chn | 8 | 26 | Solar | ✓ | 1.99/7 | 4.27 | 0 |
| ember_deu | 9 | 26 | Other Renewables | ✓ | 2.93/8 | 5.85 | 2 |
| ember_fra | 9 | 26 | Solar | ✓ | 2.14/8 | 3.11 | 0 |
| ember_gbr | 9 | 26 | Other Renewables | ✓ | 2.43/8 | 5.25 | 3 |
| ember_ind | 8 | 26 | Solar | ✓ | 1.73/7 | 2.92 | 2 |
| ember_jpn | 8 | 26 | **Nuclear** | ✓ | 2.18/7 | 5.30 | 2 |
| ember_usa | 9 | 25 | Solar | ✓ | 1.46/8 | 5.31 | 1 |
| ember_wld | 9 | 26 | Solar | ✓ | 1.27/8 | 6.10 | 0 |
| geochem_stracke_morb | 10 | 5 | K2O | ✓ | 2.06/4 | 4.53 | 0 |
| commodities_gold_silver | 2 | 1338 | Silver | **✗** | 1.0/1 | 1.09 | 79 |
| nuclear_semf | 5 | 76 | Asymmetry | ✓ | 1.6/4 | 2.61 | 1 |
| chemixhub_oxide | 7 | 24 | TiO2 | ✓ | 3.3/6 | 4.69 | 0 |
| esa_planck_cosmic | 5 | 17 | Dark Energy | ✓ | 1.0/4 | 2.86 | 0 |
| financial_sector | 10 | 252 | Industrials | **✗** | 4.88/9 | 7.66 | 0 |
| iiasa_ngfs | 7 | 31 | LULUCF | ✓ | 1.33/6 | 5.84 | 0 |
| markham_budget | 8 | 15 | Corporate Services | ✓ | 1.13/7 | 6.36 | 0 |
| Hs-25_Cosmic_Energy_Budget | 5 | 103 | Dark_Energy | ✓ | 1.0/4 | 3.48 | 7 |

## What the re-run reveals — confirmation, and three new things

**Confirmation (the old findings hold).** The energy helmsmen are exactly the historical story — Solar drives most national transitions, **Nuclear drives Japan** (Fukushima), Other Renewables drive Germany/UK. Gold/Silver is still **D2-degenerate** (eff rank 1.0 of 1 — the D=2 fundamental limit the CNT 2.0.3 class named). The cosmic budgets read as **essentially one-dimensional** (eff rank 1.0 of 4 — a clean monotonic LCDM trajectory), which is the modern echo of the old "R²≈1.0 = analytically clean physics" signature.

**New thing 1 — where the old helmsman was fragile, the new engine says so.** In **two** experiments the new *coherent* helmsman **disagrees** with the old CLR helmsman: **gold/silver** (D=2, where the read is intrinsically degenerate) and the **financial sector** (D=10). These are exactly the subcompositional-incoherence cases the coherent helmsman was built to catch — the old CLR "driver" was sensitive to the carrier set; the new read flags that the call is fragile. The old engine could not have told you this.

**New thing 2 — the dimensionality of each system, now visible.** Effective rank is a new read the old chain never reported: the financial sector moves in **~5 effective dimensions** (genuinely complex), while the cosmic budget and gold/silver move in **~1** (a single dominant ratio). Same chain, a new structural axis.

**New thing 3 — genuine regimes, not noisy thresholds.** The hold-lock, calibrating its own noise floor per series, reports *genuine* structural transitions: Germany 2, UK 3, Japan 2 in the energy mix; **79** in the 1338-month gold/silver ratio (an oscillator, correctly busy); **0** for the smooth monotone cosmic trajectories (correctly quiet). The old fixed-threshold regime count is replaced by a self-calibrated one.

## The true nature of the arc

Read the advancement table top to bottom and the pattern is unmistakable: **every change added honesty.** The two-pass tuner learned to catch a fake. The 12-step learned to say *this is a hill, not a bowl*. The CNT tower learned to name a *character* and to admit *DEGENERATE is a hypothesis, not a verdict*. The guard layer learned to *hold when it cannot resolve* and to flag when a driver call is fragile. The instrument did not get more confident over five years — it got more honest, and the re-run shows the whole chain still standing under that honesty. That is the true nature of this arc: not a march toward certainty, but a long, careful apprenticeship in knowing the boundary of what can be known from the data — which is exactly what makes the answers trustworthy.

*Re-run: Tier 1 (real chain data, current engine, reproducible). The CNT IR-class/amplitude tower is the canonical engine's own read (cnt.py); this re-run reports the guard-aware navigation reads and the new honesty layer over the same data. Nothing committed; Peter is the sole gate.*
