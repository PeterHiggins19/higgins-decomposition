# The microbiome support case — leg two of the medical-quality tetrode (why, for HUF and Hˢ)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27. The fastest of
the three medical support cases, because the real data was already in hand. A deterministic, receipted relational
read of the gut microbiome in Crohn's disease — the second independent leg toward the medical-quality tetrode.
Measured: `microbiome_support_case.py` (`8e38f840b49f040a`). Research / methods only — not clinical. The data and
its biology belong to the domain; Hˢ is the instrument. Peter is the sole gate; nothing posted.*

---

## The reading

On the real coda4microbiome Crohn dataset (Calle, Pujolassos & Susin 2023 — 975 samples, 48 genera, 662 CD vs
313 control), with a deterministic held-out split:

| view | what it measures | held-out AUC (CD vs control) |
|---|---|---|
| **Diversity** (Shannon) | a totals/aggregate summary of the gut | **0.53 — near-null** |
| **Relational** (clr nearest-centroid) | the inter-genus log-ratios | **0.71** |
| *Relational, CV-validated (CMP)* | logistic regression on ILR | *0.832* |

The aggregate "how diverse is the gut" carries almost no signal about disease state; the **relational** structure
— which genera stand in what ratio to which — separates clearly. *The message is in the ratios.* And the input
data hash is **`0b1daa0f9edee6b8`**, matching the message-principle record exactly: same data, same hash, a clean
determinism confirmation before a single statistic is read.

## Why this matters — for HUF and Hˢ

**For HUF:** this is the second leg of a **medical-quality tetrode** — four independent medical domains (cancer
epidemiology · *microbiome* · blood · respiratory), each a receipted compositional read. HUF's standard for a
sensitive claim is not one study but **four independent confirmations**; the microbiome leg is now in place. It
also demonstrates HUF's promise in a notoriously hard area: microbiome data is high-dimensional, sparse,
zero-laden, and confounded — exactly where a totals view fails and a *relational, deterministic* view earns its
keep.

**For Hˢ:** it is a clean instance of the instrument's core thesis — closure → clr → relational read — on a
system where the relational signal is real and the aggregate signal is null. It is reproducible to the hash, on
public data the domain can re-pull and re-check. *That is the value: not a louder claim, but a re-checkable one.*

**The shield.** In a field as difficult and contested as the microbiome — where studies famously fail to
replicate — our defence is not rhetoric. **Our shield is our confidence in our receipt of determinism:** the
same data gives the same hash and the same read on any machine, so the result cannot quietly drift, and a
skeptic re-runs rather than argues. In a hard area, that is the strongest thing an instrument can offer.

## Where this is heading (the tetrahedral build)

The plan (`papers/THE_NEXT_COMPONENTS_two_tetrodes.md`): complete the medical tetrode with **blood** and
**respiratory** legs, so four independent domains stand together. Then — once all the experiments on public data
are compiled — read the four as a **tetrahedron** and let *that* test reveal the dynamics and direction: which
domains cohere, where the method is strongest, how the medical group connects. The tetrahedron is not just four
studies; it is the geometry that locates the law across them, and the frame for connecting to all medical studies
as supporting groups. One leg at a time; this is leg two.

## Honest scope

- **T1 (measured):** the diversity-null / relational-separation contrast, the held-out AUCs, and the input-hash
  match reproduce (`8e38f840b49f040a`); the CV-validated 0.832 is from the prior CMP analysis.
- **T2:** that this is a "medical-quality" leg is the tetrode-standard framing; the nearest-centroid AUC is a
  conservative, fully-deterministic confirmation of the direction (the CV logistic read is stronger).
- **Fences:** **research / methods only — not clinical, not diagnostic.** The data and biology belong to the
  domain (coda4microbiome / original studies); Hˢ provides the instrument. +0.5 pseudocount zero-treatment
  (E-21). **Sole gate:** Peter. **Nothing posted.**

*Cross-refs: `microbiome_support_case.py` (`8e38f840b49f040a`); `../../experiments/compositional_message_2026-06/`
(the CMP analysis, CV 0.832); `THE_NEXT_COMPONENTS_two_tetrodes.md` (the build plan);
`../../huf-gov/doctrine/THE_TETRODE_STANDARD_for_sensitive_studies.md`; `../ABSTRACT_LEDGER.md` (P-μ). Data:
coda4microbiome (Calle, Pujolassos & Susin 2023). Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — real public data, read and never owned · diversity-null vs relational-signal measured
and receipted · the input hash matches the prior record (determinism the shield) · conservative deterministic
discriminant, the stronger CV number cited not claimed as ours · research-not-clinical fence kept · the human
keeps the gate.*
