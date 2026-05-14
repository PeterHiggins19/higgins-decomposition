# CODAwork2026 — authoritative conference folder

**Document version:** 1.2
**Document status:** authoritative folder index
**Created:** 2026-05-12 v1.0; **Revised:** 2026-05-13 v1.1 (declared as the AUTHORITY for conference materials); **Revised:** 2026-05-13 v1.2 (all documents brought into compliance with HUF Publication Standards HUF-STD-001; AI Use Declaration moved to proper scientific-community location at end of each document; deck rebuilt with corrected title slide + new AI Use Declaration slide).
**Author:** Peter Higgins, Rogue Wave Audio
**Conforms to:** HUF Publication Standards (HUF-STD-001) — `../../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json`

---

## Status declaration

**As of 2026-05-13, this folder is the single source of truth for CoDaWork 2026 speaker material.** All future edits to conference talk content happen here. Other locations in the repository (especially `../../papers/codawork2026/talk/`) remain as the lockdown-protected source snapshot from 2026-05-12, but they are no longer edited going forward.

The change of authority is recorded in [`VERSION_HISTORY.md`](VERSION_HISTORY.md).

---

## Conference

- **Event.** CoDaWork 2026 — 11th International Workshop on Compositional Data Analysis
- **Location.** Coimbra, Portugal
- **Dates.** 1–5 June 2026
- **Slot.** 15-minute talk + Q&A
- **Title.** Compositional monitoring of energy-mix drift on the simplex
- **Speaker / Author.** P. Higgins, Rogue Wave Audio
- **AI Use Declaration.** Disclosed in each document and in the deck's final slide per HUF Publication Standards (HUF-STD-001), conforming to ICMJE, COPE, Nature, Science, WAME, EU AI Act 2024, arXiv, ACM, IEEE.
- **Status.** Validated across five independent reviews (3 internal Claude rounds + ChatGPT s2 + Grok r5 + Grok r6)

---

## The complete document set in this folder

| File | Version | Purpose |
|---|---|---|
| [`README.md`](README.md) | 1.2 | This file — folder index + authority declaration + standards conformance |
| [`SPEAKER_BRIEF.md`](SPEAKER_BRIEF.md) | 1.1 | Strategic compass — why you are at the lectern, what each beat is doing |
| [`STUDY_PAGE.md`](STUDY_PAGE.md) | 1.1 | Moot methodology — five rounds to memorise the talk |
| [`CHEAT_SHEET.md`](CHEAT_SHEET.md) | 1.1 | Backstage one-pager, phone-scannable |
| [`PEDAGOGICAL_TABLES.md`](PEDAGOGICAL_TABLES.md) | 1.1 | Q&A depth backup — 4 tables (SU(2), helmsman, EITT, bread) |
| [`BACKUP_PRESENTATION.md`](BACKUP_PRESENTATION.md) | 1.1 | Equipment-fail fallback — deliver from voice alone |
| [`QA_BENCH.md`](QA_BENCH.md) | 1.1 | 12 prepared Q&A answers, short + long versions |
| [`ABSTRACT.md`](ABSTRACT.md) | 1.2 | One-page abstract for sharing (with AI Use Declaration) |
| [`CodaWork2026_Talk_2026-05-13.pptx`](CodaWork2026_Talk_2026-05-13.pptx) | 1.1 | 13-slide deck: 12 content beats + final AI Use Declaration slide |
| [`CodaWork2026_Talk_2026-05-13.pdf`](CodaWork2026_Talk_2026-05-13.pdf) | 1.1 | PDF render of the v1.1 deck |
| [`data_outputs/`](data_outputs/) | 1.0 | **Premier scientific data output — CNT v3.1.0 + CNQ v2.0.0 run on 9-country EMBER corpus. 334-page master PDF + 57-slide PPTX + 9 hash-chained JSON pairs + per-country plate PDFs.** Real engine outputs, not slides about data. |
| [`VERSION_HISTORY.md`](VERSION_HISTORY.md) | 1.2 | Audit trail of all version changes |
| [`archive/`](archive/) | — | Historical versions: May-12 v1.0 deck preserved |

**Reading order for first-time arrival:**
1. This README (2 minutes)
2. [`ABSTRACT.md`](ABSTRACT.md) (3 minutes — the talk in one page)
3. [`SPEAKER_BRIEF.md`](SPEAKER_BRIEF.md) (15 minutes — the strategic compass)
4. [`STUDY_PAGE.md`](STUDY_PAGE.md) (10 minutes — how to learn it)
5. Then drill the moot rounds; carry [`CHEAT_SHEET.md`](CHEAT_SHEET.md) backstage.

**For Q&A preparation specifically:** read [`QA_BENCH.md`](QA_BENCH.md) once, keep [`PEDAGOGICAL_TABLES.md`](PEDAGOGICAL_TABLES.md) accessible.

**For equipment-fail contingency:** [`BACKUP_PRESENTATION.md`](BACKUP_PRESENTATION.md) is the slide-free fallback talk.

---

## Versioning policy

Document versions are tracked at the header of each file ("Document version: X.Y") and in the folder-level [`VERSION_HISTORY.md`](VERSION_HISTORY.md).

- **Major (1.0 → 2.0):** substantive content change.
- **Minor (1.0 → 1.1):** clarifications, additions, repository-state updates.
- **Patch (1.0 → 1.0.1):** typo and link fixes only.

Filenames are stable. Version number lives in the document, not in the filename (except for the PowerPoint and PDF, which carry a date stamp for archival clarity).

Whenever a file is edited, the document version is bumped, the change is logged in `VERSION_HISTORY.md`, and the prior version (if substantively different) is preserved in an `archive/` subfolder.

---

## The talk in 10 beats

| Beat | Time | Anchor phrase |
|---|---|---|
| 1 | 1 min | *Energy generation is a composition.* |
| 2 | 1 min | *No monitoring framework combines all three conjuncts.* |
| 3 | 2 min | *Perturbation, Aitchison distance, TV distance, K-eff.* |
| 4 | 2 min | *Japan, Fukushima, 2011–2012, the spike.* |
| 5 | 3 min | *Germany, the trajectory, the deceptive drift, p = 0.0016 — with the null caveat.* |
| 6 | 1 min | *The UK coal exit registers as a regime change.* |
| 7 | 1 min | *5 of 9 countries reproduce the deceptive-drift signature.* |
| 8 | 1 min | *Three open questions for the room.* |
| 9 | 2 min | *A defeater must combine all three conjuncts.* |
| 10 | 1 min | *Two repositories, one self-discipline note, thank you.* |
| **Total** | **15 min** | |

---

## The central claim (memorise word-for-word)

**MC-4 three-conjunct claim:** *natively in Aitchison geometry, with formal change detection, at the carrier level — combined into one observable stack.*

This conjunction is the falsifiable claim of the talk. Four defeat paths are catalogued in Beat 9 (two preempted by INV-050 and INV-051; two open — prior-art and category). A defeater must combine all three conjuncts.

---

## Key results that load-bear the talk

| Result | Status | What it says |
|---|---|---|
| INV-050 | CANONICAL | TV distance / Aitchison distance pair-invariance verified across 101 datasets |
| INV-051 | CANONICAL | 5 of 9 EMBER countries reproduce the deceptive-drift signature (AUS, CHN, GBR, IND, JPN fire; DEU at annual grain, FRA, USA, WLD do not) |
| INV-059 | CANONICAL | Humble-invitation framing externally validated across five independent reviews |
| Germany p = 0.0016 | empirical claim, monthly grain | The packet's headline — read on slide with the null-model caveat |
| INV-029 | CANONICAL | Twin-quaternion factoring at D=8 verified at IEEE machine floor on EMBER China (3.33e-16) |
| INV-035 | CANONICAL | CHSH joint-coherence diagnostic at 0.88 within Tsirelson bound |

---

## Q&A backstops (not on slides, available on demand)

- **EITT — Entropy-Invariant Time Transformer** — Shannon entropy conserved under geometric-mean temporal compression for compositional carriers; 0.18% / 341:1. The temporal-invariance sibling of MC-4's spatial-invariance. Full canonical explanation at [`../../papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md`](../../papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md).
- **KILL-001** — Published falsifiability artifact (HUF, 2026-03-23). 19 named failure modes in 5 categories. Worst failure mode KILL-3.3 (artificial carrier) cannot be mechanically detected — only the domain expert can.
- **HUF Governance Charter** — 9 articles, April 2026. Parent doctrine for Hs Change Control v1.0.
- **Bread the Hs way** — verbal memorable pedagogy. The framework as a recipe. → [`../../papers/BREAD_THE_HS_WAY_2026-05-12.md`](../../papers/BREAD_THE_HS_WAY_2026-05-12.md).

---

## Reproducing the result

For anyone with the raw EMBER CSV and Python or R:

```bash
git clone https://github.com/PeterHiggins19/higgins-decomposition
cd higgins-decomposition
python3 verify_publication_results.py
```

Expected: 25 reference experiments pass the determinism gate. content_sha256 and engine_signature appear on every page of every output. Anyone with the raw CSV can verify any plate in approximately 2 minutes. See [`../../REPRODUCIBILITY_CHECKLIST.md`](../../REPRODUCIBILITY_CHECKLIST.md) for the full recipe.

---

## Relationship to other folders in the repo

| Folder | Role | Status |
|---|---|---|
| `Hs/CODA-Association/CODAwork2026/` (this folder) | **AUTHORITY for conference materials going forward** | Editable; versioned |
| `Hs/papers/codawork2026/talk/` | Historical source snapshot (May 12) | Lockdown-protected through 2026-06-06; not edited |
| `Hs/papers/codawork2026/planning/` | Planning material that fed the May 12 talk | Lockdown-protected; not edited |
| `Hs/HCI-CNT/conference_demo/talk_deck/` | Legacy April-built deck (CNT engine architecture, not energy-mix monitoring) | Preserved with regeneration note for archival |
| `Hs/CODA-Association/` (parent folder) | CoDa-community general entry point | Maps to all CoDa-relevant material |

---

## Lockdown compatibility

Active 2026-05-12 → 2026-06-06.

- Engine code: untouched
- Schema: untouched
- Investigation Catalog disposition counts: untouched
- Six NO-CREATE files: untouched
- `papers/codawork2026/talk/` lockdown content: untouched
- Consistency checker: 23 passes / 0 warnings / 0 errors (verified post-changes)

This folder is S2 doc-only — additive linked-document creation, no current-state claim changes, no engine touches.

---

## The doctrine line

> *The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*

The vocabulary is the CoDa community's. The work is offered for inspection. The talk is an ascent waypoint, not the summit.

---

*The repo holds. The speaker walks to the lectern. The CoDa community has one clean door.*
