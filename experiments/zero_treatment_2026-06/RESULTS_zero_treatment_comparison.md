# Zero-treatment module — build + all-EMBER baseline-vs-treated comparison

**2026-06-09 · Cowork working tree (not committed). Confirms performance of the new upstream zero-treatment against the engine's 1e-15 floor.**

## What & why
The canonical CNT engine floors any zero to 1e-15. A floored zero produces an absurd CLR (≈ −33) and badly inflates the Aitchison norm. The new **upstream** module `HCI-CNT/adapters/zero_treatment.py` (Tensor Train Link 1 / Adapter; **engine unchanged**) replaces that floor, distinguishing two zero types:

- **Structural** (carrier zero in *every* year → genuinely absent) → **drop** the carrier (run at true dimensionality).
- **Rounded** (zero in *some* years, real but below reporting precision) → **multiplicative replacement** (Martín-Fernández et al. 2003): fill with δⱼ = 0.65 × DLⱼ, DLⱼ = smallest positive value in column j; non-zero ratios preserved; closure restored by the engine.

Deterministic; no randomness; no engine change.

## Comparison — all 10 EMBER pipeline-ready countries (canonical CNT v3.2.0)
RAW (engine 1e-15 floor) vs ZERO-TREATED. `maxN` = max Aitchison norm over the series (the floor-artifact indicator).

| ISO | D_in | D_out | rounded repl. | maxN raw | maxN treated | structural dropped |
|---|---|---|---|---|---|---|
| AUS | 9 | 9 | 0 | 14.5 | 14.5 | — |
| CAN | 9 | 8 | 0 | **36.2** | **8.8** | Other Renewables |
| CHN | 8 | 8 | 0 | 9.1 | 9.1 | — |
| DEU | 9 | 9 | 12 | **48.2** | **9.6** | — |
| FRA | 9 | 9 | 0 | 9.7 | 9.7 | — |
| GBR | 9 | 9 | 29 | **47.0** | **10.9** | — |
| IND | 8 | 8 | 0 | 8.7 | 8.7 | — |
| JPN | 8 | 8 | 1 | **36.4** | **8.4** | — |
| USA | 9 | 9 | 2 | **37.6** | **7.8** | — |
| WLD | 9 | 9 | 0 | 8.2 | 8.2 | — |

## Findings (the delta, confirmed)

**1 · Safe on clean data (no-op where there are no zeros).** The five zero-free countries — AUS, CHN, FRA, IND, WLD — are **bit-identical** baseline vs treated (helmsman counts, regime counts, and max norm all unchanged). The treatment does not perturb data that doesn't need it. *Confirmed.*

**2 · The norm artifact is removed wherever zeros exist.** Every zero-affected country (CAN, DEU, GBR, JPN, USA) had its max Aitchison norm inflated to **36–48** by the 1e-15 floor; treatment brings it to a normal **~8–11**. The floor artifact in the radial/position metric is eliminated.

**3 · The step-based navigation was already robust to *rounded*-zero flooring — the past results stand.** For DEU, GBR, JPN, USA the **helmsman counts, regime counts, and deceptive-drift counts are unchanged** between raw and treated. Because the 1e-15 floor is a constant, it largely cancels in the step differences (Δclr), so it corrupted the *norm* but not the *navigation*. **This means the prior conference findings (helmsman trajectories, the 5-of-9 deceptive-drift result) are robust to zero-treatment.**

**4 · The *structural*-zero case did shift the navigation — and the drop corrects it.** Canada's absent "Other Renewables" carrier, floored to 1e-15, had spuriously taken one step's helmsman (baseline Wind 7 / no Nuclear → treated Wind 6 / Nuclear 1) and inflated the norm 4×. Dropping the absent carrier (D 9→8) corrects both. Structural zeros, unlike rounded ones, *do* distort the navigation under the floor — which is exactly why they must be dropped, not floored.

## Conclusion
The zero-treatment is **safe** (identity on zero-free series) and **corrective** (removes the floor artifact; fixes the structural-zero navigation distortion). The headline takeaway for the corpus: **past EMBER navigation results are confirmed robust**; the only material correction is the radial-norm metric and the structural-zero (Canada-type) case. Recommend running zero-treatment as the standard upstream adapter for any series containing zeros — and especially before the high-dimensional province runs, where structural and rounded zeros will be common.

## Honest caveats
- `frac = 0.65` (the "65 % of detection limit" convention) is a choice; results for rounded zeros are insensitive to it here (navigation unchanged).
- This is the **multiplicative-replacement** form, appropriate for continuous below-precision data; the strict count-data Bayesian-multiplicative (Dirichlet posterior) is a generalization not needed for TWh values.
- Structural-drop changes D by design (intended; the absent carrier is not part of the sub-system).

## Files
`HCI-CNT/adapters/zero_treatment.py` (module) · `zero_treatment_comparison.json` (full per-country detail) · treated CSVs in `outputs/zt_treated/`.

*The instrument reads. The expert decides.*
