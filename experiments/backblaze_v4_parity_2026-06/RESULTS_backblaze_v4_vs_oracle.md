# Backblaze parity — CN‑TT v4 vs the frozen oracle (CNT v3.2.0)

*Experiment journal, 2026-06-10. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. The first head‑to‑head of the new modular v4 engine against the old system on a full real dataset.*

**Code/artifacts:** `bb_parity.py`, `bb_parity_result.json`, `bb_oracle_v3.json` (oracle run). **Input:** `HCI-CNT/experiments/codawork2026/backblaze_fleet/backblaze_fleet_input.csv` (731 daily fleet‑mean compositions × D=4 carriers [Mechanical, Thermal, Age, Errors], built by `HCI-CNT/adapters/backblaze_adapter.py` from the 22 GB BackBlaze SMART corpus).

---

## What was compared

The "old system" here is the **frozen oracle CNT v3.2.0** (`cnt.py`) — the engine v4 replaces. Both engines were run on the **identical** full Backblaze longitudinal composition, and v4's output was diffed field‑by‑field against the oracle's, over all 731 timesteps. (The historical Hs‑17 results in `experiments/Hs-17_Backblaze/` are from an even older 12‑step pipeline and are kept for lineage; the rigorous baseline is the canonical oracle on identical input.)

v4 was run **through the modular `Pipeline`** (adapt → treat → calibrate → geometry → atlas → navigate), proving the new section architecture processes a real dataset end‑to‑end (0.30 s; atlas lossless at 8.9e‑16; chain hash `9d903bfb…`).

## Result — TIER‑A PARITY (bit‑identical)

Max `|v4 − oracle|` over 731 steps:

| Field | max abs diff |
|---|---|
| composition, CLR, shannon_entropy, aitchison_norm, k_eff, higgins_scale, κ_HS trace, s_j_sensitivity, bearing θ, aitchison_step, tv_step | **0.00e+00** |
| ilr_norm | 1.33e‑15 (machine ε) |

Categorical fields — mismatches over 731 steps:

| Field | mismatches |
|---|---|
| ring_class | **0** |
| concentration_regime (incl. deceptive) | **0** |
| helmsman_local (argmax\|Δclr\|) | **0** |

The one intended difference:

| Field | v4 vs oracle |
|---|---|
| angular_velocity | v4 **atan2** vs oracle **arccos**: max 5.12e‑11°, mean 2.07e‑12° — agree to oracle precision; v4 is strictly more accurate near 0°/180° by construction (the documented improvement). |

**Verdict: v4 reproduces the oracle bit‑for‑bit on the entire real dataset**, across the full core navigation family and key diagnostics, with the only divergence being the numerically superior angle. Oracle `cnt_content_sha256` `47196cb6…`.

## Why the exact match is expected (and what it proves)

The matched quantities are functions of the composition and its CLR, which are **basis‑independent** — so an exact match is the correct outcome and confirms v4's geometry, treatment, and navigation math are faithful ports. `ilr_norm` matching to 1.33e‑15 further confirms v4's Helmert basis agrees with the oracle's to machine precision. This is the first real‑data certification that the new engine = the old engine where it should, and is the kind of evidence the parity harness (engine build P3) will produce automatically across the whole corpus.

## Honest scope (claim tiers)

- **Tier 1 (verified here):** bit‑identical parity on the **core per‑step navigation family + key diagnostics** listed above, over the full 731‑step Backblaze series; the atan2 angle agreeing to 5e‑11°.
- **Tier 2 (sound):** the basis‑independence reasoning; the modular pipeline running real data end‑to‑end.
- **Tier 1 (now also verified — FULL-OUTPUT parity, 2026-06-10):** the remaining oracle blocks were ported into v4 and diffed against the same oracle run (`bb_parity_full.py`): **helmsman rolling-window family** (flips 220=220; sigma, sign, stability, torque, rolling, chaos), **attractor fit** (fitted/period/dominant_pair{1,0}/amplitude/damping/contraction), **depth tower** (energy + curvature levels, termination EXHAUSTED, ir_class MODERATELY_DAMPED, involution), **stage 1/2/3** (clr ranges, variation matrix, pairwise correlations, triadic area, subcomposition ladder, regime boundaries n=28), **EITT bench**, and **navigation_2d PCA** (variance_explained, bary_xy) — **all bit-identical, max diff 0.0e+00** (the Helmert bases were confirmed identical to the oracle's, so coordinate-frame quantities match exactly). **v4 now reproduces the entire oracle output on real data; the only engine-wide difference is the atan2 angle improvement (5e-11°). The navigation-parity layer (P2) is complete.**

## Addendum — the engine is now a full-output CLI (2026-06-10)
`HCI-CNTT/run_cntt.py <csv> -o out.json` ingests any composition CSV (label column + D carriers) and emits the complete payload — at low D the full oracle-parity output (geometry, atlas, navigation, helmsman_family, attractor_fit, depth_tower, stages 1/2/3, navigation_2d, EITT, content hash); at high D it auto-gates the O(D²)/combinatorial blocks and emits the O(D) family + lossless tiling. Verified on Backblaze (731×4, full output, helmsman.flips=220, 0.06 s) and a synthetic D=200 (high-D mode, 0.03 s). **This is the ingestion path for the real coda4microbiome data: drop the CSV in the data folder and run.**

## Reproduce
```
cd experiments/backblaze_v4_parity_2026-06/
# oracle baseline (frozen engine):
python ../../HCI-CNT/engine/cnt.py \
  ../../HCI-CNT/experiments/codawork2026/backblaze_fleet/backblaze_fleet_input.csv -o bb_oracle_v3.json
python bb_parity.py            # runs v4 + diffs every field
```

*The instrument reads. The expert decides. The hashes carry the receipts.*
