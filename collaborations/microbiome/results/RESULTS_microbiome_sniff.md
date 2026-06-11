# Microbiome sniff — CN‑TT v4 high‑D performance + first dynamics read

*Experiment journal, 2026-06-10. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. The first time CN‑TT is pointed at microbiome‑scale compositional data — a "sniff," not a study. Interpretation deferred to domain experts (instrument reads, expert decides).*

**Code/artifacts:** `microbiome_sniff.py`, `microbiome_sniff_result.json`.
**Reference framework:** coda4microbiome — Calle, Pujolassos & Susin (2023), *BMC Bioinformatics* 24:82; survival extension Pujolassos et al. (2024), *NAR Genomics & Bioinformatics* 6(2):lqae038. coda4microbiome is the CoDA microbiome standard (cross‑sectional / longitudinal / survival; microbial signatures as balances).
**Honest data note:** coda4microbiome's `Crohn`/`HIV` datasets ship as R `.rda` binaries; the sandbox's web‑fetch restrictions cannot pull binary data, so this sniff uses **synthetic, microbiome‑realistic** compositions (sparse, many taxa, log‑normal abundances, a phylogenetic tree as the atlas). The real Crohn/HIV run is the trivial next step on a machine with R or `pyreadr`. Performance metrics (reconstruction error, time, memory) depend on D and sparsity, not on biological identity, so they transfer; the dynamics read (B) is illustrative on injected structure.

---

## (A) High‑dimensional lossless reconstruction + performance — the headline

The tile‑native tree atlas reconstructs each microbiome‑scale composition's full log‑ratio structure losslessly, in milliseconds, at tiny footprint:

| taxa (D) | samples | charts (≈D/3) | reconstruction error | time / sample | atlas memory |
|---:|---:|---:|---:|---:|---:|
| 48 (Crohn‑scale) | 20 | 16 | 9.3e‑15 | 0.4 ms | ~0 MB |
| 256 | 20 | 85 | 2.0e‑14 | 0.5 ms | ~0 MB |
| 2,048 | 20 | 683 | 8.1e‑14 | 1.4 ms | 0.1 MB |
| **10,000** | 20 | 3,334 | **1.6e‑13** | **7.1 ms** | 0.3 MB |

Lossless to machine precision across two orders of magnitude in D, sub‑10 ms per sample at ten thousand taxa, deterministic. This is the high‑D capability the tiling arc was built for, now demonstrated on microbiome‑structured sparse data. (Earlier work proved the path to D=10⁶ at ≈4e‑12; this confirms it on realistic sparse compositions with heavy zero‑treatment.)

## (B) Longitudinal navigation — does the instrument read the dynamics?

A synthetic subject series (D=128 taxa, T=60 timepoints) with an **antibiotic‑like perturbation injected at t=30** (6 taxa bloom, others suppressed, then exponential recovery). The CN‑TT navigation family, run on the series:

- **Diversity collapse detected:** K_eff fell from a baseline mean of **59.4** to a post‑perturbation minimum of **45.6** — the instrument saw the loss of effective diversity.
- **Helmsman correctly identified bloom taxa:** at the onset, the helmsman (`argmax|Δclr|`) pointed at taxa **53 and 98 — both members of the injected bloom set** {8, 48, 53, 80, 98, 123}. The instrument fingered real drivers from geometry alone, with no labels.
- **Regime boundary near the onset:** boundaries flagged at t = {2, 4, **32**}; the onset at t=30 surfaced at t=32.
- Deceptive‑drift steps: 15; tightening: 12.

**Honest read:** the instrument clearly responded to the injected dynamics — diversity collapse, correct steering taxa, and a regime boundary two steps after onset. But the boundary timing was **+2, not exact**, and two **early‑series false‑positive boundaries** appeared. That is a **threshold‑tuning** matter (the regime tripwire `mean + k·std`), deliberately **not** tuned‑to‑fit here (tuning to make the onset land exactly would be p‑hacking the demo). The takeaway: the navigation is genuinely responsive to microbiome perturbation/recovery; precise change‑point timing needs the null‑model/threshold work (open question Q3, the P2 paper) and real data.

## (C) Determinism
The navigation output's `stable_hash` is identical on rerun (`a1b31204…`) — same input → same read, bit‑for‑bit.

## What this sniff establishes (claim tiers)
- **Tier 1 (verified):** lossless tree‑atlas reconstruction at D up to 10,000 on sparse microbiome‑structured data (≤1.6e‑13), in ms/sample; determinism; the navigation family runs end‑to‑end at microbiome D and is responsive to injected diversity collapse with a correct helmsman.
- **Tier 2 (sound):** the synthetic structure faithfully models the microbiome compositional regime (sparsity + heavy zero‑treatment + phylogenetic tree atlas); performance transfers to real data.
- **Tier 3 (to earn):** any biological reading; change‑point precision (needs threshold/null‑model work); and the real coda4microbiome Crohn/HIV/longitudinal run.

## Next step (real data)
Run the identical pipeline on coda4microbiome's `Crohn` (≈48 taxa) and a longitudinal dataset, comparing the CN‑TT navigation read against coda4microbiome's balance‑based microbial signatures — a real, citable, head‑to‑head feasibility study (the conference Tier‑1 "longitudinal microbiome" follow‑up). On a machine with R/`pyreadr`, exporting the `.rda` to CSV is a one‑liner; the pipeline runs unchanged.

## Reproduce
```
cd experiments/microbiome_sniff_2026-06/
python microbiome_sniff.py
```

*The instrument reads. The expert decides. The hashes carry the receipts.*
