# NOTATION AND TERMINOLOGY — Redirect stub

**Version:** v3.0 (redirect stub, 2026-05-19)
**Status:** SUPERSEDED. This document has been **merged into [`GLOSSARY.md`](GLOSSARY.md) v3.0**.

---

## This file is now a redirect

On 2026-05-19, by Peter's direction, the two parallel reference documents in this folder —

- `GLOSSARY.md` (the readable narrative reference, v2.0), and
- `NOTATION_AND_TERMINOLOGY.md` (the locked notation reference, v2.0, this file)

— were **combined into a single authoritative reference** at [`GLOSSARY.md`](GLOSSARY.md), now v3.0.

The merger eliminates the previous split where two parallel files could drift against each other. The merged GLOSSARY v3.0 now serves both purposes: read in sequence it is a narrative glossary, and cited by section/entry it is a locked notation reference.

---

## Go here

**For every term, symbol, formula, abbreviation, or doctrine previously documented in this file, see:**

→ [`GLOSSARY.md`](GLOSSARY.md) **v3.0** (2026-05-19)

The merged document contains approximately 220 entries across thirty sections, covering:

- §1 Foundational mathematics (PCA, SVD, eigenvalue / eigenvector, Spectral Theorem, ...)
- §2 Statistical concepts (Lyapunov exponent, Feigenbaum constant, CHSH, Tsirelson bound, ...)
- §3 CoDa foundations (closure, CLR, ILR, Aitchison geometry, Helmert basis, ...)
- §4 CNT core terms (carriers, course, helmsman, navigation chart, Activation Coefficient, ...)
- §5 CNQ / Volume IV quaternion view
- §6 HCI instrument family
- §7 Helmsman family (σ channel, sigma sequence, flips, stability, torque proxy)
- §8–§15 Vocabulary disambiguations (rank vs order, channel vs factor vs component, etc.)
- §16 HUF Standards (HUF-STD-001 v1.1, HUF-STD-002, HUF-STD-003)
- §17 Seven Linear-Algebra Foundations
- §18 Stage 0 / Foundations Plate / Dual-View
- §19 Power Share / Activation Coefficient
- §20 Canonical findings
- §21 MC-1 through MC-4 hierarchy
- §22 Other locked doctrines
- §23 Output conventions
- §24 Change control
- §25 Instrument-family and lineage names (RWA, BTL, HUF, Hs, V_Core, DADC, ...)
- §26 Standard symbols
- §27 Standard formulas
- §28 Abbreviations A–Z (including PCA, SVD, EITT, CHSH, MC, ILR, CLR, ...)
- §29 Citation policy
- §30 Maintenance log

---

## Citation form (going forward)

Old form (do not use after 2026-05-19):

> Notation: see Hs/HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md.

New form (use this):

> Notation: see Hs/HCI-CNT/handbook/GLOSSARY.md v3.0 (2026-05-19).

---

## Why the merger

The two documents had grown to ~80 % overlap by v2.0. The split was an artifact of how the project bootstrapped (a readable narrative file plus a locked terms file), but it created a maintenance hazard: a term updated in one file but not the other became a silent drift bug. Peter's 2026-05-19 directive — *"combine the glossary with the terms and make the glossary and terms complete"* — fixes this by making one file authoritative.

Old `NOTATION_AND_TERMINOLOGY.md` v2.0 content was reviewed entry-by-entry against `GLOSSARY.md` v2.0. Where the two disagreed, the more precise / more recent definition was kept. Where one file had an entry the other did not, that entry was added to the merged v3.0. Approximately fifty net new entries were added during the merge, including foundational mathematics (PCA, SVD, eigenvalue), statistical mechanics (Lyapunov, Feigenbaum), and the MC-1 / MC-2 / MC-3 hierarchy (previously only MC-4 was documented).

---

## Archive

The pre-merger v2.0 content of both files is preserved in git history. To recover the old `NOTATION_AND_TERMINOLOGY.md` v2.0, check out any commit prior to 2026-05-19. Recommended pin: the commit immediately preceding the merge, accessible via `git log -- handbook/NOTATION_AND_TERMINOLOGY.md`.

---

*Single source. No drift. One file holds the vocabulary line.*
