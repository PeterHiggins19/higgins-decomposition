# Fit — Scale uncertainty & FDR in sequencing (Dos Santos, Murariu, Silverman & Gloor)

*CoDaWork 2026, Book of Abstracts p. 16 ("Microbiology II", Fri). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. DRAFT — nothing sent. This is the most "peer/foundations" of the set — framed honestly as complementary, not as "we solve your problem."*

## Who & what they presented
**Scott J. Dos Santos¹, Andreea C. Murariu¹, Justin D. Silverman², Gregory B. Gloor¹** — ¹ University of Western Ontario, Canada; ² Penn State. Presenter: `ggloor@uwo.ca`.

*"Accounting for scale controls for false discovery rate in the analysis of high throughput sequencing data."* Standard normalisations make hidden assumptions about the **scale** (absolute abundance/size) of the sampled system; ignoring this inflates FDR in differential‑abundance/expression analysis. They include **scale uncertainty** in the scale model by modifying the CoDa normalisations used by ALDEx2/ALDEx3, show across 10 RNA‑seq datasets that this is essential, and demonstrate a predictable relationship between scale uncertainty and incremental FDR.

## Where Hˢ helps (complementary / foundations — honest framing)
This is a foundations contribution where Hˢ is largely a **peer**, but two genuine points of contact exist:

- **Scale‑free by construction.** Hˢ reads only log‑ratios on the simplex, so it is scale‑invariant by design. It does not *estimate* scale (so it does not replace their scale‑uncertainty model) — but it is a clean, deterministic reference for "what the analysis looks like when only relative information is used," a useful counterpoint in their scale discussion.
- **Reproducible infrastructure.** Hˢ's determinism + content hash (HUF‑STD‑002) make it a natural home for a *reproducible* scale‑aware DA pipeline: a result that reruns byte‑for‑byte, with the configuration (including any scale assumptions) echoed and hashed in the output.

The honest offer is a **methods dialogue**, not a tool that fixes their problem: how does explicit scale uncertainty interact with a strictly scale‑free deterministic reading, and where do the two views agree or diverge on the same 10 datasets? There is also a natural collegial angle — Gloor's group (Western Ontario) is a leading CoDa+microbiome lab, and Peter is in Ontario.

## What we'd offer
A scale‑free deterministic read on the same public datasets as a comparison point, and Hˢ's hash‑chained provenance as reproducibility infrastructure for scale‑aware pipelines. Primarily: a conversation between their scale‑uncertainty framing and Hˢ's determinism.

## Data scope
They work with public RNA‑seq datasets; Hˢ would read those where they live and return geometry only. No storage or redistribution; interpretation stays with the authors.

## Claim tiers
- **Tier 1 (verified):** Hˢ is scale‑invariant (log‑ratio), deterministic, and hash‑chained.
- **Tier 2 (sound):** Hˢ as a reproducibility layer; the value of a scale‑free deterministic comparison point.
- **Tier 3 (to earn):** any joint result; that Hˢ adds anything to their FDR control specifically (it likely does not directly — this is a dialogue, not a fix).

## In the common web
Half of the **"high‑dimension / scale" pair** with the single‑cell CoDA‑hd work ([`../highd-singlecell-tang/`](../highd-singlecell-tang/)) — the foundations layer beneath every microbiome and genomics application here. Scale honesty and deterministic reproducibility are complementary: a scale‑free, hash‑chained reading is a clean reference against which scale‑aware methods can be checked. See the unifying [`../HS_LETTER_OF_INTENT.md`](../HS_LETTER_OF_INTENT.md).

→ DRAFT outreach note: [`DRAFT_outreach_note.md`](DRAFT_outreach_note.md) · unifying letter: [`../HS_LETTER_OF_INTENT.md`](../HS_LETTER_OF_INTENT.md)
