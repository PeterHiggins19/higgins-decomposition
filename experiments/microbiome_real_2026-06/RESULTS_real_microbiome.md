# CN‑TT v4 on real coda4microbiome data — Crohn + ECAM

*Experiment journal, 2026-06-10. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. The real‑data microbiome run, on the datasets Peter downloaded. Interpretation deferred to domain experts; here CN‑TT reads are checked against **established** microbiome biology as honest validation, not as novel findings.*

**Data:** coda4microbiome v0.2.4 (Calle, Pujolassos & Susin 2023, *BMC Bioinformatics* 24:82), read from the local `.rda` files via `pyreadr`. Code: `run_real_microbiome.py`; export: `export` step → `crohn.csv`, `ecam_child.csv`; result: `real_microbiome_result.json`.
**Method note — what coda4microbiome does vs what CN‑TT does:** coda4microbiome performs **supervised variable selection** (penalized regression on log‑ratios → a *microbial signature* = a balance of taxa associated with an outcome: `coda_glmnet`, `coda_glmnet_longitudinal`, `coda_coxnet`). CN‑TT performs **unsupervised, deterministic navigation** (diversity dynamics, dominant‑driver helmsman, lossless reconstruction, hash receipts). They share log‑ratio/Aitchison geometry — coda4microbiome even computes `shannon_effnum`, which is exactly CN‑TT's `K_eff = exp(Shannon)`. The two are **complementary**: coda4microbiome answers "which taxa balance predicts the phenotype"; CN‑TT answers "how does the composition move and what steers it, deterministically."

---

## (A) Crohn — cross‑sectional (975 samples × 48 genera)

- **Lossless reconstruction at real D=48, all 975 samples:** max error **1.8×10⁻¹⁴**. The tile/tree atlas reconstructs real sparse genus compositions to machine precision. ✅
- **Deterministic diversity read — honest null:** effective diversity `K_eff` is **CD mean 7.31 (n=662) vs control mean 7.23 (n=313)**, Mann–Whitney **p = 0.78** — **no separation** (and the tiny difference runs opposite to the naïve "reduced diversity in CD" expectation). This is reported straight: **global diversity does not discriminate CD from control in this genus‑level data.**
- **Why that's the right result, not a failure:** global α‑diversity is a weak/inconsistent CD marker at genus level; this is precisely the motivation for coda4microbiome's approach — find a *specific balance of taxa* (a signature), not a global scalar. CN‑TT's strength here is the exact, deterministic reconstruction + a faithful null; discriminating CD would call for the supervised‑signature tool (coda4microbiome) or a CN‑TT helmsman/balance analysis targeted at the contrast, which this run did not do.

## (B) ECAM — one infant's longitudinal trajectory (real infant gut)

ECAM = Early Childhood Antibiotics and the Microbiome (the longitudinal infant‑gut study; 42 children in the filtered set). Analyzed child `studyid=20`: **34 timepoints, days 0–856, Cesarean delivery**, ordered by day of life.

- **CN‑TT recovers infant‑gut maturation — clean hit:** `K_eff` (effective diversity) **rises with age, Spearman ρ = 0.71 (p = 2.5×10⁻⁶)**, roughly doubling from **5.7 (early) → 11.8 (late)**. Increasing gut diversity over the first ~2 years is the **established** ECAM/infant‑gut pattern (Bokulich et al.) — the deterministic instrument read it directly from raw counts, with no labels and no statistics in the science path. ✅
- **Regime tripwire — honest miss:** **0** regime boundaries flagged. The maturation is gradual and the sampling is irregular (days 0,1,2,…,856 unevenly spaced), so the `mean + 2·std` step‑distance tripwire — designed for evenly‑spaced series — did not fire. This is a **time‑aware‑thresholding** gap (the same open null‑model question, Q3), not a read failure. The child was antibiotic‑exposed at many timepoints; resolving whether those produce detectable shifts needs the time‑aware change‑point work.
- Regime mix over the trajectory: 16 loosening (diversifying) vs 5 tightening, 10 deceptive — consistent with a net‑diversifying maturation.
- **Determinism:** identical navigation hash on rerun. ✅

## What this run establishes (claim tiers)

- **Tier 1 (verified):** lossless reconstruction of real Crohn genus data at D=48 (1.8e‑14); CN‑TT's deterministic K_eff recovers the established ECAM maturation trend (ρ=0.71, p=2.5e‑6); the Crohn diversity null (p=0.78) is a correct, reproducible read; determinism.
- **Tier 2 (sound):** the complementarity framing vs coda4microbiome (supervised signature vs unsupervised navigation; both log‑ratio; shared `shannon_effnum`/`K_eff`).
- **Tier 3 (to earn):** any biological claim; time‑aware regime detection on irregularly‑sampled longitudinal data; a real head‑to‑head where coda4microbiome's signature and a CN‑TT targeted balance/helmsman analysis are compared on the same labeled contrast.

## Honest bottom line
CN‑TT ingests and reconstructs real microbiome data losslessly, and its deterministic read **recovers a known biological trajectory (infant‑gut maturation) on real longitudinal data** while returning an **honest null where one is warranted (global diversity ≠ CD signature)**. That combination — recovering the real signal where it exists and not inventing one where it doesn't — is the right outcome for a first real run. The natural next study is the **longitudinal head‑to‑head**: coda4microbiome's `coda_glmnet_longitudinal` signature vs CN‑TT's navigation read across many ECAM children, with time‑aware change‑point detection — the conference Tier‑1 "longitudinal microbiome" follow‑up.

## Reproduce
```
cd experiments/microbiome_real_2026-06/
pip install pyreadr
python run_real_microbiome.py      # reads the local coda4microbiome .rda files directly
# or, via the engine CLI on the exported CSV:
python ../../HCI-CNTT/run_cntt.py crohn.csv -o crohn_cntt.json
```

*The instrument reads. The expert decides. The hashes carry the receipts.*
