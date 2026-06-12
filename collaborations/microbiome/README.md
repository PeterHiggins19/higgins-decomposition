# Hs‑Microbiome Research — Executive Summary

*Hs (Higgins Decomposition) / CN‑TT applied to microbiome compositional data. 2026‑06‑10. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Reference framework and data: **coda4microbiome** (Calle, Pujolassos & Susin 2023). Claim‑tiered throughout; the instrument reads, the expert decides.*

---

## 1 · What this is — and the scope line

Microbiome data is **compositional** (taxon counts carry only relative information), **high‑dimensional** (tens to tens of thousands of taxa), and **sparse** (most taxa absent in most samples) — exactly the regime Hs's tiling was built for. This folder holds Hs's results on microbiome data and the capability it brings.

**We deal with the instrument, not the data.** Hs provides a deterministic, hash‑chained compositional‑navigation engine (CN‑TT). The **datasets and their biological interpretation belong to the domain** — to coda4microbiome and the original studies (Crohn, HIV, ECAM, etc.). We do not store, own, or redistribute the data here (see `results/DATA_SOURCE.txt`); we read it where it lives and report geometry and dynamics. Biological meaning is for microbiome scientists.

## 2 · Results on microbiome data (verified, honest)

- **Lossless reconstruction on real data.** All 975 Crohn samples (48 genera) reconstructed from overlapping exact 4‑part charts to **max error 1.8×10⁻¹⁴**. The tiling works on real, sparse genus compositions.
- **Recovers a known biological trajectory.** On one ECAM infant's 34‑timepoint gut series (days 0–856), Hs's deterministic effective‑diversity read (K_eff) **rises with age — Spearman ρ = 0.71, p = 2.5×10⁻⁶**, doubling 5.7 → 11.8. Increasing gut diversity over early life is the established ECAM pattern; Hs read it from raw counts, no labels, no statistics in the science path.
- **Returns an honest null where one is warranted.** Global diversity does **not** separate Crohn's‑disease from control samples (K_eff 7.31 vs 7.23, p = 0.78). That is the correct read, and it is exactly why coda4microbiome seeks a *specific taxa balance (a signature)*, not a global scalar. Hs did not invent a result that isn't there.
- **High‑dimensional capability, deterministic and fast** (§4): lossless to **D = 10,000** at machine precision in ~7 ms/sample; proven to **D = 1,000,000** at ≈4×10⁻¹² in a few seconds, using the **phylogenetic tree as the atlas**.
- **Self‑diagnostic.** Hs can report whether an anomaly is **internal** (an instrument/sensor fault — isolated to a channel) or **external** (a real compositional change), and runs under explicit stage‑by‑stage operational control — capabilities for embedded/clinical/flight deployment.

## 3 · Use cases

- **Longitudinal microbiome monitoring** — maturation, perturbation/recovery (antibiotics, diet, treatment), regime shifts; deterministic dominant‑driver ("helmsman") and effective‑diversity trajectories with a receipt.
- **High‑D deterministic reduction** — lossless, reproducible, bit‑for‑bit dimensional handling at OTU/ASV/metagenomic scale, where statistical reductions are lossy and non‑reproducible.
- **Reproducible/auditable pipelines** — for clinical, regulatory, or pre‑publication settings: same input → same output, hash‑chained provenance (HUF‑STD‑002), claim‑tiered.
- **Field & remote sensing** — the same engine runs at the sensor edge (geosensing) and toward flight; internal/external shock diagnostics for self‑monitoring.
- **Earth/space twin studies** — because the engine is deterministic, the Earth read and a flight read are the *same measurement* (byte‑identical), so any difference is the environment, not the tool. Candidate: **gut microbiome over a long mission** with a matched Earth twin. See [`../../SPACE_READINESS_AND_CHALLENGE.md`](../../SPACE_READINESS_AND_CHALLENGE.md).
- **Complement to supervised signatures** — pair Hs's unsupervised navigation with coda4microbiome's outcome‑associated balances (§5).

## 4 · Microbiome systems capability table — D, limits, time to process

Drawn from the high‑dimensional tiling work (`results/cnq_tiling_scaling.png`, `cnq_tiling_tree_vs_path.png`) and the microbiome runs. Reconstruction is **lossless iff the chart atlas is connected**; the **hierarchical/phylogenetic tree atlas** (O(log D) diameter) holds machine precision at scale, where the simple sliding‑window atlas degrades. Per‑sample timings on a 2‑core CPU.

| Taxa (D) | microbiome scale | atlas charts (tree ≈ D/3) | reconstruction error | time / sample | atlas memory |
|---:|---|---:|---:|---:|---:|
| 48 | Crohn genera (real) | 16 | **1.8×10⁻¹⁴** (real) | 0.4 ms | ~0 |
| 60 | HIV / sCD14 genera | ~20 | ~1×10⁻¹⁴ | ~0.4 ms | ~0 |
| 256 | genus/family panel | 85 | 2.0×10⁻¹⁴ | 0.5 ms | ~0 |
| 2,048 | OTU panel | 683 | 8.1×10⁻¹⁴ | 1.4 ms | 0.1 MB |
| 10,000 | ASV scale | 3,334 | 1.6×10⁻¹³ | 7.1 ms | 0.3 MB |
| 100,000 | large ASV / strain | ~33,000 | ~1×10⁻¹² | ~0.16 s | ~5 MB |
| 1,000,000 | metagenomic gene scale | ~333,000 | **4.1×10⁻¹²** | ~2–4.5 s | 48 MB |

**Limits & notes.** (i) Precision is governed by atlas *conditioning*, not D: the tree atlas stays at ~10⁻¹²–10⁻¹³ to a million taxa, while a length‑D path atlas drifts to ~2×10⁻⁷ at D=10⁶ — so **use the phylogeny as the atlas**. (ii) Memory is tiny (≤48 MB at D=10⁶) because the engine never forms a dense global basis (which would be ~8 TB at D=10⁶) and never enumerates all 4‑subsets (~10²² at D=10⁶). (iii) Every run is **deterministic** — identical content hash on rerun at every D. (iv) The O(D²)/combinatorial diagnostics (pairwise stages, 2‑D PCA) auto‑gate off above D≈64; the O(D) navigation family + lossless tiling carry to any D.

## 5 · Relationship to coda4microbiome

coda4microbiome and Hs share log‑ratio / Aitchison geometry and even the same diversity measure (their `shannon_effnum` is Hs's `K_eff = exp(Shannon)`), but answer **different, complementary** questions:

| | coda4microbiome | Hs / CN‑TT |
|---|---|---|
| Mode | **Supervised** | **Unsupervised, deterministic** |
| Output | a **microbial signature** = a balance of taxa associated with an outcome (penalized regression: `coda_glmnet`, `coda_glmnet_longitudinal`, `coda_coxnet`) | **navigation**: effective diversity, dominant‑driver helmsman, regime dynamics, **lossless high‑D reconstruction**, hash receipts |
| Question | *which taxa balance predicts the phenotype?* | *how does the composition move, what steers it, and is the change real or an instrument fault?* |

The natural joint study is a **longitudinal head‑to‑head**: coda4microbiome's `coda_glmnet_longitudinal` signature vs Hs's navigation read across many ECAM children — with time‑aware change‑point detection. We cite coda4microbiome generously as the microbiome‑CoDA standard this work builds alongside.

## 6 · coda4microbiome — links and contacts (for the data and microbiome science)

The data and the microbiome‑science questions are coda4microbiome's domain. For datasets, methods, or collaboration on the microbiome side, contact the authors directly:

- **Project site:** https://malucalle.github.io/coda4microbiome/ · **Tutorials:** /tutorial · **Publications:** /publications
- **CRAN:** https://cran.r-project.org/web/packages/coda4microbiome/ · **GitHub / issues:** https://github.com/malucalle/coda4microbiome
- **Reference:** Calle M.L., Pujolassos M. & Susin A. (2023) *coda4microbiome: compositional data analysis for microbiome cross‑sectional and longitudinal studies.* **BMC Bioinformatics 24:82.** Survival extension: Pujolassos, Susin & Calle (2024) *NAR Genomics & Bioinformatics* 6(2):lqae038.

**Who to contact:**
- **Prof. Malu Calle** — lead / PI (Universitat de Vic, UVic). `malu.calle@uvic.cat` · ORCID 0000‑0001‑9334‑415X · https://mon.uvic.cat/bi-squared/malu_calle/ — *for the microbiome science and the datasets.*
- **Prof. Toni Susin** — package maintainer (UPC). `toni.susin@upc.edu` · ORCID 0000‑0002‑0874‑2784 · https://web.mat.upc.edu/toni.susin/ — *for the `coda4microbiome` package and reproducibility.*
- **Dr. Meritxell Pujolassos** — co‑author (UVic). `meritxell.pujolassos@uvic.cat` · ORCID 0000‑0003‑0313‑3506.

*(Contact details are from the public `coda4microbiome` CRAN `DESCRIPTION` and project site; listed here for onward reference, not as an endorsement or an existing collaboration.)*

## 7 · Contents of this folder

- `README.md` — this executive summary.
- `results/RESULTS_real_microbiome.md` — the real‑data run (Crohn reconstruction + diversity null; ECAM maturation).
- `results/RESULTS_microbiome_sniff.md` — the high‑D performance sniff (lossless to D=10,000; injected‑perturbation read).
- `results/real_microbiome_result.json`, `microbiome_sniff_result.json` — machine‑readable summaries (our analysis outputs, not raw data).
- `results/cnq_tiling_scaling.png`, `cnq_tiling_tree_vs_path.png` — the high‑D scaling / tree‑atlas figures.
- `results/DATA_SOURCE.txt` — where to obtain the data (not stored here).
- `code/microbiome_sniff.py`, `code/run_real_microbiome.py` — our analysis scripts.
- **Engine:** `../../HCI-CNTT/` (CN‑TT v4 + `run_cntt.py` CLI). **Method & proof:** `../geology-wehner/CNQ_TILING_METHOD_AND_PROOF.md`, `HIGHD_DETERMINISTIC_SCALING.md`. **Full spec:** `../../HCI-CNTT/CNTT_COMPLETE_SPECIFICATION.md`.

## 8 · Claim tiers
- **Tier 1 (verified):** lossless reconstruction on real Crohn (1.8e‑14) and synthetic to D=10⁴ (1.6e‑13); ECAM maturation recovery (ρ=0.71, p=2.5e‑6); the Crohn diversity null (p=0.78); determinism; the capability‑table timings/limits.
- **Tier 2 (sound):** the coda4microbiome complementarity framing; the synthetic structure faithfully modeling the microbiome regime.
- **Tier 3 (to earn):** any biological claim; the longitudinal head‑to‑head vs `coda_glmnet_longitudinal`; time‑aware change‑point detection on irregularly sampled series.

*The instrument reads. The expert decides. The hashes carry the receipts. The data belongs to the domain.*
