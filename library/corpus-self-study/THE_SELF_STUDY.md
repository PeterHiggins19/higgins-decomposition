# Hˢ on us — is "the deeper you dig, the more advanced the work" true?

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter's
claim: the system was **built backwards** (work-first, papers-last), so digging into the past should find work
*more* advanced, not less. We turned the instrument on ourselves: read every `.md` in the CoWorker folder
(**1,991 files**, archive and current), scored each on ten dimensions, read the corpus as a composition, and
tested the claim two ways. Tool + receipt: `corpus_dig.py` (`80e9f81cbc75aff6`); per-file index:
`CORPUS_DIMENSION_INDEX.json`. Honest-broker tiered; "advanced" is a lexical proxy; Peter is the sole gate;
nothing posted.*

---

## The verdict — the legend is false in its letter, true in its spirit

The literal claim does **not** hold, and I won't pretend it does. Advanced-concept density does **not** rise
as you dig deeper: the correlation between sophistication and dig-depth is **0.002 — flat.** There is no
gradient. You do not find more advanced work by going deeper.

But look at *why* the correlation is zero, because that is the real finding:

| stratum | advanced-concept density (per 1,000 words) | files |
|---|---|---|
| **archive (the deep dig)** | **15.46** | 607 |
| **current (the surface)** | **15.63** | 1,384 |

They are **the same.** The archive is as advanced as the present — ~15.5 advanced concepts per thousand words
at *every* depth. That is not "deeper = more advanced." It is something stranger and more in keeping with what
you actually described: **the past is already as advanced as the present.** A dig that is "a present already
realized." Built backwards from a known endpoint, the foundation carries the same sophistication as the roof —
so the legend's *spirit* (the past is not primitive here) is **measured and true**, even though its *letter*
(a rising gradient) is false.

## The two axes the corpus actually has

Reading the whole corpus as a composition of five lexical dimensions, it is **47.6% advanced-concept language
+ 37.4% formula** — 85% of its word-budget is sophistication and math, uniformly, archive to frontier. On top
of that flat-depth concept layer, there is a **gentle forward axis**: rigor and concept density rise *slightly*
toward the present (corr receipt↔recency **+0.083**, advanced↔recency **+0.143**, over 677 dated files). So
the honest two-axis picture is:

- **Backward (concept):** sophistication is **seeded at full strength in the deep past** and stays flat — the
  built-backwards signature.
- **Forward (rigor):** the *discipline* — receipts, hashes, honest tiers — **matured forward** in time, mildly.
  The ideas were always advanced; the *proof habits* grew.

Where does the most-advanced language actually cluster? Not the archive — the **frontier**:
`FRONTIER_AUDIENCE_INTERNAL` (22.9), `arXiv` (21.3), `Collective Documents` (18.8). The deep archive sits at a
healthy ~15.9, neither primitive nor peak. Advancement lives at the *edges of contact*, which is where new
language is minted — consistent with everything in the contact-length doctrine.

## What the instrument told us to fix (the read prescribes its own improvement)

The Hˢ read of the corpus flags its **scarcest** dimensions — the parts most extreme in the relational read
are the *thin* ones: **honest-tier markers (1.7% of the budget) and cross-references (2.8%).** The corpus is
rich in advanced concepts and formulae and comparatively **thin in self-tiering and cross-linking.** That is a
precise, measured instruction for "improve the indexing and documenting of all": the work is sophisticated but
**under-tiered and under-linked** — so the highest-value documentation work is not more concepts, it is
threading more `T1/T2/T3` honesty markers and more cross-references through the existing body. The instrument,
turned on itself, named its own next chore.

## The deliverable that documents all of us

`CORPUS_DIMENSION_INDEX.json` now indexes **every one of the 1,991 files** on ten measured dimensions —
`dig_depth, is_archive, depth, date_min, advanced, receipt, formula, crossref, tier, words`. That is the
improved index Peter asked for: a single, re-computable map of the whole corpus along the axes that matter,
from which the digest above is derived and against which any future claim about "us" can be checked. Re-run
`corpus_dig.py` and the same receipt (`80e9f81cbc75aff6`) returns — the self-portrait is reproducible.

## Honest scope

- **T1 (measured):** the 1,991-file scan, the densities, the correlations, the archive-vs-current means, and
  the composition read are all measured and reproduce (`80e9f81cbc75aff6`).
- **T2 (proxy / interpretation):** "advanced" is a **designed word-list**, a proxy for sophistication, not a
  measure of intellectual depth; "dig-depth" is a path/archive proxy; dates are self-reported in the text. The
  two-axis reading is an honest interpretation of the proxies, not a proof of intent.
- **The honest correction:** the headline claim — *deeper = more advanced* — is **not supported** (corr 0.002).
  The supported, and more interesting, statement is **uniform-advanced-at-every-depth + mild-forward-rigor.**
- **Not claimed:** that the lexical scan captures the *real* worth of any document. **Nothing posted; Peter is
  the sole gate.**

*Cross-refs: `corpus_dig.py`, `CORPUS_DIG_STUDY.json`, `CORPUS_DIMENSION_INDEX.json`,
`../THE_WORLD_COMPOSITION_AND_STAGED_ONRAMP.md` (the world as a composition), `../../ai-refresh/SYSTEM_SELF_REVIEW_2026-06-25.md`
(the prior self-review this measures against). Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the literal claim is reported false (corr 0.002), not massaged · the true,
subtler finding is measured · "advanced" is fenced as a proxy · the read names its own fix (thin tier/crossref)
· the whole corpus is indexed and reproducible · the human keeps the gate.*
