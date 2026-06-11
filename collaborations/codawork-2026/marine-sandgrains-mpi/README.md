# Fit — Bacterial succession on single sand grains (Silva‑Solar, Amann & Knittel · MPI Bremen)

*CoDaWork 2026, Book of Abstracts p. 48 ("Microbiology I", Tue). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. DRAFT — nothing sent. This talk also seeds the space twin‑study → [`../../../SPACE_READINESS_AND_CHALLENGE.md`](../../SPACE_READINESS_AND_CHALLENGE.md).*

## Who & what they presented
**Sebastián Silva‑Solar¹, Rudolf Amann¹, Katrin Knittel¹** — ¹ Max Planck Institute for Marine Microbiology, Bremen. Presenter: `ssilva@mpi-bremen.de`.

*"Ecological succession of bacterial communities on single sand grains."* Diverse marine communities from subtidal sediments colonised **sterile sand grains** in a controlled microcosm; succession tracked by 16S rRNA amplicon sequencing. Genus‑level succession ran **Vibrionaceae (early) → Rhodobacteraceae / Alteromonadaceae (mid) → Flavobacteriaceae / Saprospiraceae (final)**. Key finding: communities on **individual grains converge over time** while the liquid fraction does not; ~10,000 ASVs per bottle per timepoint; strong selection and recognisable taxonomic patterns during colonisation of free surfaces.

## Where Hˢ helps (strong — a deterministic succession + convergence read)
Their result is a *trajectory with structure* — exactly Hˢ's regime:

- **Succession as a helmsman handoff.** Their three named stages are, in Hˢ terms, a sequence of **helmsman** changes — the genus whose log‑ratio change dominates each step. Hˢ would render the Vibrionaceae→Rhodobacteraceae/Alteromonadaceae→Flavobacteriaceae/Saprospiraceae succession as a deterministic driver trajectory with **regime boundaries** at the stage transitions.
- **A quantitative convergence metric.** Their central finding — grains converge, liquid does not — is, geometrically, a **shrinking Aitchison step / attractor fit** over time. Hˢ can turn "converge" into a number per grain and per time, and contrast it against the non‑converging liquid fraction.
- **Lossless high‑D.** ~10,000 ASVs is within Hˢ's lossless tiling range (proven to D=10⁶ at machine precision using a phylogeny as the atlas), all hash‑reproducible.
- **Determinism + receipt.** A succession read that reruns byte‑for‑byte — useful for a microcosm result others will want to reproduce.

## What we'd offer
A deterministic **succession + convergence** read on a series they prepare: helmsman trajectory, regime boundaries at stage transitions, a per‑grain convergence (attractor) metric, and the grain‑vs‑liquid contrast — returned as geometry + receipt. They keep the data and the ecology.

## The space connection (separate, Tier‑3)
Free‑surface microbial colonisation is a natural microgravity experiment; this talk is the inspiration for the Earth/space deterministic twin‑study idea in `SPACE_READINESS_AND_CHALLENGE.md`. That is a speculative, unsolicited Tier‑3 direction and is **kept out of the outreach note** — the note offers only the immediate, concrete help above.

## Data scope
Instrument only; we do not request, store, or redistribute their sequences. Ecological meaning stays with the authors.

## Claim tiers
- **Tier 1 (verified):** Hˢ computes helmsman, regime boundaries, attractor fit, lossless high‑D, and a hash deterministically (lossless on real 48‑genus Crohn data to 1.8e‑14; synthetic to D=10⁴ at 1.6e‑13).
- **Tier 2 (sound):** rendering their named succession as a helmsman trajectory; the Aitchison‑step convergence metric formalising "communities converge."
- **Tier 3 (to earn):** any result on their data; the space twin‑study extension.

## In the common web
One of the **"community‑in‑motion" trio** with the COPD lung microbiome ([`../microbiome-copd-narayana/`](../microbiome-copd-narayana/)) and the longitudinal gut microbiome ([`../microbiome-longitudinal-creusmarti/`](../microbiome-longitudinal-creusmarti/)) — a clinical trial, a treated gut, and a colonising grain are the *same* Hˢ read, so one engine makes them cross‑verifiable. This folder is also the **bridge to the space horizon** (free‑surface colonisation → microgravity twin study). See the unifying [`../HS_LETTER_OF_INTENT.md`](../HS_LETTER_OF_INTENT.md).

→ DRAFT outreach note: [`DRAFT_outreach_note.md`](DRAFT_outreach_note.md) · unifying letter: [`../HS_LETTER_OF_INTENT.md`](../HS_LETTER_OF_INTENT.md)
