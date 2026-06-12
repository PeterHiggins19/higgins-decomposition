# Fit — CoDA at single‑cell scale, CoDA‑hd (Tang & Huang · CUHK)

*CoDaWork 2026, Book of Abstracts p. 52 ("Health II", Thu). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. DRAFT — nothing sent.*

## Who & what they presented
**Nelson Tang¹, Jinghan Huang¹** — ¹ Dept. of Chemical Pathology, Li Ka Shing Institute of Health Sciences, Faculty of Medicine, The Chinese University of Hong Kong. Presenter: `nelsontang@cuhk.edu.hk`.

*"First application of CoDA to the high‑dimensional (HD) biological data matrices of single‑cell RNA‑sequencing (CoDA‑hd R package)."* scRNA‑seq matrices reach **~100,000 cells × 20,000 genes**, extremely sparse ("dropout" zeros). Their pipeline: **CLR + truncated (partial) SVD** as a fast close approximation to full log‑ratio analysis (minutes–hours); a **new column/sample‑specific zero‑count addition** (the SGM scheme) for sparse data; conversion of log‑normalised matrices into CoDA log‑ratio form; better clustering and robustness to zero‑inflation. Implemented in the **CoDA‑hd R package**.

## Where Hˢ helps (strong on the high‑D axis; honest about the limits)
- **An exact, deterministic counterpart to the SVD approximation.** Their truncated SVD is a fast *approximation* to full LRA. Hˢ's tiling does **lossless** high‑dimensional reconstruction (proven to D=10⁶ at machine precision) using a hierarchy as the atlas — so where a gene/cell hierarchy (ontology, lineage tree) exists, Hˢ offers an *exact*, hash‑reproducible reduction to compare against the approximation, at comparable speed.
- **Zero‑treatment dialogue.** They developed sample‑specific count addition (SGM) for dropout zeros; Hˢ has its own structural‑vs‑rounded zero‑treatment stage. A direct methods comparison on the same sparse matrices is a clean, mutually useful exercise.
- **R synergy.** Hˢ ships an R parity port alongside Python (byte‑identical), so a CoDA‑hd ↔ Hˢ comparison can live entirely in R.
- **Determinism + receipt.** A reduction that reruns byte‑for‑byte — valuable for routine large‑scale studies that must be reproducible.

**Honest limit.** Hˢ's *navigation* read (helmsman, regime boundaries) needs an ordering; scRNA‑seq cells aren't ordered by default. It applies only if a **pseudotime/lineage trajectory** is supplied (then the helmsman names the gene steering each pseudotime step — a Tier‑3 angle). The core fit here is the **lossless high‑D reduction + zero‑treatment**, not the trajectory read.

## What we'd offer
A deterministic, lossless high‑D reduction (tree atlas) on a matrix they prepare, as an exact counterpart to CLR+partial‑SVD, plus a zero‑treatment comparison — returned as outputs + receipt, in R if preferred. Data stays with them.

## Data scope
Instrument only; no storage or redistribution of their matrices. Biological meaning stays with the authors.

## Claim tiers
- **Tier 1 (verified):** Hˢ lossless tiling to D=10⁶ at ~10⁻¹²–10⁻¹³ via tree atlas, deterministic + hashed; R/Python parity at the IEEE floor.
- **Tier 2 (sound):** Hˢ as an exact counterpart to truncated SVD where a hierarchy exists; the zero‑treatment comparison.
- **Tier 3 (to earn):** any scRNA‑seq result; the pseudotime‑trajectory helmsman read; that Hˢ's reduction improves downstream clustering.

## In the common web
Half of the **"high‑dimension / scale" pair** with the scale‑FDR foundations work ([`../scale-fdr-gloor/`](../scale-fdr-gloor/)) — together they are the foundations layer (honest CoDa at 10⁴–10⁶ parts and under unknown scale) that underwrites the microbiome and genomics applications. Hˢ's lossless tiling + scale‑free determinism is the shared substrate both can test against. See the unifying [`../HS_LETTER_OF_INTENT.md`](../HS_LETTER_OF_INTENT.md).

→ DRAFT outreach note: [`DRAFT_outreach_note.md`](DRAFT_outreach_note.md) · unifying letter: [`../HS_LETTER_OF_INTENT.md`](../HS_LETTER_OF_INTENT.md)
