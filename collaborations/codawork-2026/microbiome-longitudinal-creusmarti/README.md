# Fit — Longitudinal microbiome under time‑varying treatment (Creus‑Martí et al.)

*CoDaWork 2026, Book of Abstracts p. 14 ("Microbiology II", Fri). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. DRAFT — nothing sent.*

## Who & what they presented
**Irene Creus‑Martí¹, Marc Comas‑Cufí², Javier Palarea‑Albaladejo²** — ¹ Dept. of Statistics & OR, Universitat de València; ² Dept. of Computer Science, Applied Mathematics & Statistics, University of Girona. Presenter: `irene.creus@uv.es`.

*"Modelling longitudinal microbiome data subject to time‑varying treatment regime through low‑dimensional projection."* They summarise dominant temporal variation with **PCA** and identify its key drivers, then use **mixed‑effects modelling** to test time‑varying covariates. Illustrated on a longitudinal gut‑microbiome dataset (German cockroach *Blattella germanica*) under intermittent Kanamycin vs untreated control, the method differentiates treatment regimes over time and identifies the **leading taxa** involved.

## Where Hˢ helps (strong — a deterministic navigation companion)
Their goals — capture dominant temporal variation, find its key drivers, separate treatment regimes — map directly onto Hˢ's navigation read, computed deterministically without a statistical model in the path:

- **Leading taxa, per step.** They extract key drivers from PCA loadings; Hˢ's **helmsman** names the dominant driver of *each* time step (`argmax|Δclr|`), giving a driver *trajectory*, not a global loading.
- **`K_eff` effective‑diversity track** quantifies diversity erosion/recovery under the antibiotic pulses — a deterministic companion to their projection.
- **Regime boundaries** mark where the dynamics shift (e.g. onset/recovery around each Kanamycin pulse) as detected change‑points.
- **Attractor fit** quantifies return‑to‑baseline (recovery) vs drift after perturbation.
- **Lossless high‑D + hash receipts** mean the read scales to OTU/ASV resolution and is byte‑for‑byte reproducible.

Their statistical projection and Hˢ's deterministic geometry are complementary lenses on the same series; agreement between them is itself a validation.

## What we'd offer
A deterministic helmsman/`K_eff`/regime read on the cockroach‑Kanamycin series (or any longitudinal set they prepare), returned as geometry + receipt for comparison with their PCA + mixed‑effects drivers. Optionally a short note pairing the two approaches.

## Data scope
Instrument only. We read prepared compositions where they live; we do not store or redistribute the data. Biological meaning stays with the authors.

## Claim tiers
- **Tier 1 (verified):** Hˢ computes helmsman, `K_eff`, regime boundaries, attractor fit deterministically; ECAM infant‑gut maturation recovered (ρ=0.71, p=2.5e‑6) on real coda4microbiome data.
- **Tier 2 (sound):** that the helmsman trajectory corroborates/augments their PCA‑driver identification; perturbation‑recovery reads on antibiotic pulses.
- **Tier 3 (to earn):** any specific result on their dataset.

## In the common web
One of the **"community‑in‑motion" trio** with the COPD lung microbiome ([`../microbiome-copd-narayana/`](../microbiome-copd-narayana/)) and the sand‑grain succession ([`../marine-sandgrains-mpi/`](../marine-sandgrains-mpi/)) — same geometry, one engine, mutually verifiable. The natural complement is the supervised `coda4microbiome` work: does Hˢ's unsupervised helmsman land on the same taxa as their outcome‑associated balance? See the unifying [`../HS_LETTER_OF_INTENT.md`](../HS_LETTER_OF_INTENT.md).

→ DRAFT outreach note: [`DRAFT_outreach_note.md`](DRAFT_outreach_note.md) · unifying letter: [`../HS_LETTER_OF_INTENT.md`](../HS_LETTER_OF_INTENT.md)
