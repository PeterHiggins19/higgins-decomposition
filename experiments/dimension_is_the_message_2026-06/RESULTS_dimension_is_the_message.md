# Dimension is the message — proved on real data, and placed against the literature

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. The
falsifiable core of "the system is the message," tested directly: as the number of parts D grows, does the
relational signal grow and the communication capacity grow, while the scalar diversity read stays blind? Yes,
measured on real microbiome data. Receipt `bf24c615…`. Honest-broker tiered; nothing posted; Peter is the sole
gate.*

---

## The measurement (real coda4microbiome Crohn data, N=975, D up to 48)

| parts D | relational AUC (the message) | scalar Shannon AUC (Margalef/Wilson read) | symbol capacity (bits) |
|---:|---:|---:|---:|
| 5 | 0.639 | 0.527 | 7.0 |
| 9 | 0.657 | 0.519 | 13.8 |
| 17 | 0.729 | 0.533 | 28.9 |
| 25 | 0.804 | 0.515 | 42.7 |
| 33 | 0.828 | 0.506 | 56.7 |
| **48** | **0.830** | **0.505** | **78.9** |

Three things, one dataset, one engine:

1. **The relational message grows with D.** Reading the *ratios* (ILR coordinates), the discriminative signal
   about Crohn's disease rises monotonically from AUC 0.64 at 5 parts to **0.83 at 48 parts.** More parts =
   more message. (CMP Law 2, Dimensional Articulation.)
2. **The scalar diversity read is blind.** The Shannon diversity index — the classic "community as a message"
   read (Margalef; E.O. Wilson) — stays at **chance (~0.5)** at every D. The scalar saw none of it; the signal
   was always in the *structure*, never the summary.
3. **The communication capacity grows with D.** Read as an N-dimensional signal constellation, the composition's
   Gaussian-channel capacity over its ILR eigen-directions grows from **7 bits at 5 parts to ~79 bits at 48
   parts** — more dimensions carry more distinguishable symbols. *The more parts, the more symbology.*

## Where this stands against the literature (web-checked 2026-06-23)

- **"The community is a message; species are symbols."** This is **established and old** — Margalef and
  E.O. Wilson applied Shannon's entropy to ecosystems decades ago, treating each species as a symbol and the
  community as "a message rich in information." *But that lineage reads the message as a SCALAR (the diversity
  index)* — exactly the ratio-blind functional this experiment shows stays at chance. Hˢ inherits the idea and
  advances it from the scalar to the **full relational, dimensional read.**
- **"The microbiome communicates."** Also **established**, but it means *chemical* signaling — quorum sensing,
  autoinducers (AI-2), molecular-communication channels. That is bacteria signaling *each other*; this work is
  about reading the *composition itself* as the message — a different, complementary claim.
- **"Higher-dimensional signal constellations carry more symbols."** **Established** in communications —
  N-dimensional modulation, manifold/symplectic coding. Hˢ connects the *compositional* dimension to this:
  a D-part composition is a D−1-dimensional constellation, and its capacity grows with D, as measured.
- **"Read the composition's relational geometry as a channel whose capacity grows in D."** This specific
  synthesis **does not yet appear in the literature — it crawls.** It is Hˢ's distinctive contribution, and it
  is now measured, not asserted.

## The one-line claim, earned

> The community **is** a message — but the message lives in the *ratios* and grows with the *number of parts*,
> not in the scalar diversity. Read relationally, a 48-part composition delivers a 0.83-AUC diagnostic and ~79
> bits of channel capacity where the classic scalar read delivers chance and ~one number. *Group size and data
> structure is the message; more dimensions, more symbology.*

## Tiers

- **T1 (measured):** the AUC-vs-D and capacity-vs-D curves on real Crohn data; the scalar-read null; receipt
  `bf24c615…`.
- **T2 (reasoned):** the synthesis "compositional relational geometry as a channel whose capacity grows in D"
  — sound, demonstrated here, novel vs the literature.
- **T3 (open):** that the capacity translates to a usable communications scheme on hardware — named, to earn
  (cf. the SO(n) codec and QAM sandbox).

*Reproduce: `python3 dim_message.py`. Cross-refs: `../compositional_message_2026-06/` (Law 1 + the HIV
replicate), `../../papers/COMMUNICATIONS_GEOMETRY_LITERATURE_SCAN.md`, `../../papers/NINE_STUDY_TRUST_LEDGER.md`,
`../conformance_fixtures_2026-06/hs_codec_demo.py` (the symbol channels). Peter is the sole gate.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*

Sources (literature placement): [Shannon entropy in ecology — species as symbols](https://ai-talks.org/2025/07/13/understanding-species-balance-info-theory-ecology/) ·
[Diversity index (Wikipedia)](https://en.wikipedia.org/wiki/Diversity_index) ·
[Quorum sensing — Bassler](https://explorebiology.org/summary/cell-biology/quorum-sensing:-how-bacteria-communicate) ·
[Information- and communication-centric microbial communities (bioRxiv)](https://www.biorxiv.org/content/10.1101/2023.08.23.554558v1.full) ·
[Understanding sequencing data as compositions (Bioinformatics)](https://academic.oup.com/bioinformatics/article/34/16/2870/4956011)
