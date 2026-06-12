# Fit — COPD clinical‑trial microbiome dynamics (Narayana & Chotirmall)

*CoDaWork 2026, Book of Abstracts p. 30 ("Health I", Wed). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. DRAFT — nothing sent.*

## Who & what they presented
**Jayanth Kumar Narayana¹, Sanjay H. Chotirmall²** — ¹ Lee Kong Chian School of Medicine, Nanyang Technological University, Singapore; ² Dept. of Respiratory & Critical Care Medicine, Tan Tock Seng Hospital. Presenter: `jayanth.narayana@ntu.edu.sg`.

*"The cost of ignoring compositionality: CoDA unmasks treatment effects in COPD clinical trials."* They analysed sputum metagenomes (n = 93 patients, 256 samples over 52 weeks) from a phase III RCT (NCT02305940; doxycycline vs placebo). Standard methods (diversity indices, Bray‑Curtis, PERMANOVA) found **no** treatment effect (p > 0.05). Compositional methods — **inverse perturbation (⊖)** for change residuals, **Aitchison norm** for change magnitude, ALDEx2 for differential abundance, and **moving‑window** analysis between visits — revealed significant, time‑structured effects (Streptococcus/Veillonella shifts; Rothia consistent, Burkholderia 0–3 mo, Moraxella 9–12 mo).

## Where Hˢ helps (very strong — this is Hˢ's family, done by hand)
Their workflow *is* the Hˢ navigation family applied manually with statistics. Hˢ would run the **same** read deterministically and with a receipt:

- **Per‑window helmsman.** They identified the steering taxa by inspection (Streptococcus, Veillonella, Rothia, Burkholderia, Moraxella). Hˢ's `helmsman = argmax|Δclr|` names the dominant driver of *each* between‑visit step automatically — the same answer, derived, not eyeballed.
- **Aitchison norm + perturbation step** are native Hˢ outputs already (the per‑step Aitchison step size and inverse‑perturbation residual are computed every run).
- **Regime boundaries** formalise their "three distinct temporal patterns" (short‑/consistent/long‑term) as detected change‑points rather than chosen windows.
- **`K_eff` trajectory** gives a deterministic effective‑diversity track to sit beside their diversity indices.
- **Internal‑vs‑external shock (FDIR)** can flag whether a between‑visit jump is a real compositional change or a sampling/processing artefact — directly useful when a trial signal is borderline.
- **Hash provenance** (HUF‑STD‑002): a phase III trial result that is *byte‑for‑byte reproducible* on rerun — regulatory‑grade auditability.

## What we'd offer
A deterministic navigation **cross‑check / augmentation** on their existing series: helmsman‑per‑window + regime boundaries + Aitchison‑norm track + a hash receipt, reproducing their manual taxon‑by‑window findings automatically. They keep the data and all clinical interpretation; we supply the instrument read and the receipts. A short methods note could pair their statistical DA with Hˢ's deterministic navigation as complementary lenses.

## Data scope
We do not request or store the trial data. If a collaboration formed, Hˢ would read their prepared compositions where they live and return geometry/dynamics only. All biological and clinical meaning is theirs.

## Claim tiers
- **Tier 1 (verified):** Hˢ computes helmsman, Aitchison norm/step, `K_eff`, regime boundaries, and a content hash deterministically today; demonstrated on real microbiome data (ECAM maturation ρ=0.71; Crohn null p=0.78).
- **Tier 2 (sound):** that Hˢ's automated read would reproduce their manual taxon‑by‑window findings on the same series; the regulatory‑reproducibility value.
- **Tier 3 (to earn):** any actual COPD result; that Hˢ surfaces effects beyond what they already found.

## In the common web
This work is one of the **"community‑in‑motion" trio** with the longitudinal gut‑microbiome ([`../microbiome-longitudinal-creusmarti/`](../microbiome-longitudinal-creusmarti/)) and the sand‑grain succession ([`../marine-sandgrains-mpi/`](../marine-sandgrains-mpi/)) — geometrically the same problem (a community moving under a driver), so run through one engine the three become directly cross‑verifiable. It also pairs with the supervised `coda4microbiome` signature work as the unsupervised‑vs‑supervised complement. See the unifying [`../HS_LETTER_OF_INTENT.md`](../HS_LETTER_OF_INTENT.md).

→ DRAFT outreach note: [`DRAFT_outreach_note.md`](DRAFT_outreach_note.md) · unifying letter: [`../HS_LETTER_OF_INTENT.md`](../HS_LETTER_OF_INTENT.md)
