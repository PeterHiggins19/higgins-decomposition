# Built on, and for, the compositional-data community

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. The
foundations this work stands on are the compositional-data community's, and the community **welcomed** this
work in person. This note does three things in return: **credit** the allies accurately, **give back** what
is ours to give, and **incorporate and test** their ideas in our frame so the work is directly useful to
them. Honest-broker tiered; Peter is the sole gate; nothing posted.*

---

## The allies, and what we build on (cited)

Nothing here would exist without the people who built compositional data analysis. We name them the only
honest way — by their published work:

- **J. Aitchison (1986),** *The Statistical Analysis of Compositional Data* — the simplex, closure, the
  log-ratio transforms, subcompositional coherence. The ground our `clr` read stands on.
- **J. J. Egozcue, V. Pawlowsky-Glahn, G. Mateu-Figueras & C. Barceló-Vidal (2003),** "Isometric Logratio
  Transformations for Compositional Data Analysis," *Mathematical Geology* 35(3):279–300 — the **ilr** and
  the principle of **working on coordinates** (balances).
- **V. Pawlowsky-Glahn, J. J. Egozcue & R. Tolosana-Delgado (2015),** *Modeling and Analysis of Compositional
  Data* — the modern synthesis.
- **J. A. Martín-Fernández and colleagues** — principled treatment of zeros and missing values, which our
  zero handling follows.

The CoDaWork community welcomed this work in person. This note is the reciprocation.

## We incorporated their idea and tested it (receipt `74e8e6e544108759`)

We took the community's signature coordinates — the **isometric log-ratio (ilr) / balances** (Egozcue et al.
2003) — and tested, on real Frielingen-9 geology, two things our work claims, *in their frame*:

| test | result |
|---|---|
| **ilr is an isometry of our reads** — Aitchison distance = Euclidean distance in ilr | **confirmed to 3.3×10⁻¹⁶** |
| **the Locked-Discriminant Principle holds in ilr (balances)** — the centred-balance discriminant is invariant under the nuisance group | **confirmed, invariance rate 1.0** |

So our reads and our reproducibility result are **coordinate-free and native to the community's preferred
coordinates** — a user already working on balances loses nothing and gains the determinism guarantee with no
change of frame. *(Code: `../papers/locked-discriminant/ilr_incorporation.py`.)*

## What we give back (make it useful to them)

The contribution we can honestly offer the community is not new compositional theory — it is **engineering
discipline and open instruments built on their mathematics:**

1. **Determinism + receipts.** A reproducibility discipline expressed directly on their balances: same input →
   same output → same content hash, on any machine. A way to make a compositional analysis *auditable*.
2. **The Locked-Discriminant Principle** (`lock = nuisance-group invariance`) — a clean, testable criterion
   for when a compositional decision rule is reproducible. Stated in their coordinates; theirs to use.
3. **Open instruments** — the engine, the filter-injection probe, the compositional memory and conveyor, the
   triad cross-verify — all operating on `clr`/`ilr`, all receipted, all open.
4. **Honest tiers** — every claim marked measured / reasoned / vision, so nothing borrows certainty it has
   not earned.

## The spirit (and the honest fence)

We **stand on their shoulders and say so.** We claim **no priority** over the compositional-data
foundations and **no new theorem** here — the ilr is theirs, the simplex geometry is theirs, the invariance
principle is classical statistics. What we add is the determinism, the instrumentation, the receipts, and the
framing — offered back, open, on their coordinates, for the community that built the field and welcomed the
work. Names appear only as citations of published work; no collaboration is implied beyond what is real and
consented; the welcome was a kindness, and this is the thanks.

*Cross-refs: `../papers/locked-discriminant/THE_LOCKED_DISCRIMINANT_PRINCIPLE.md`,
`../papers/locked-discriminant/ilr_incorporation.py`, `../papers/SUPPORTING_CASE_STUDIES.md` (the cited
study register), `../README.md` (References & Acknowledgments). Peter is the sole gate; nothing posted.*

*Sources: [Egozcue et al. 2003, Mathematical Geology (Springer)](https://link.springer.com/article/10.1023/A:1023818214614).*

*Proof & Honesty Standard — the allies are cited accurately · their idea is incorporated and tested (receipted) · what we give back is named · no priority or new theorem claimed · experts decide.*
