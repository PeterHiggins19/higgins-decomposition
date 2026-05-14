# CODA-Association — entry point for the compositional-data community

**Document version:** 1.2
**Document status:** authoritative folder index
**Created:** 2026-05-12 v1.0; **Revised:** 2026-05-13 v1.1 (declared CODAwork2026 subfolder as conference authority); **Revised:** 2026-05-13 v1.2 (brought into compliance with HUF Publication Standards HUF-STD-001 — AI assistance disclosure moved to proper scientific-community location).
**Author:** Peter Higgins, Rogue Wave Audio
**Conforms to:** HUF Publication Standards (HUF-STD-001) — [`../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json`](../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json)

**Purpose.** This is the curated landing area for anyone arriving from the CoDa (Compositional Data Analysis) community — practitioners, theorists, conference attendees, future readers, journal reviewers. The folder is intentionally small. It serves two roles: (1) for the conference, **[`CODAwork2026/`](CODAwork2026/) is the AUTHORITY** — the editable, versioned source of truth for all conference materials going forward; (2) for the broader CoDa-community-relevant content, this README maps to canonical sources elsewhere in the repository.

If you are looking for the conference talk, go to **[`CODAwork2026/`](CODAwork2026/)**.

If you are looking for anything else compositional, the map below tells you where it lives.

---

## What this repository contains for the CoDa community

The Hs (Higgins Decomposition) repository operates inside Aitchison geometry. The two compositional engines are:

- **CNT v3.1.0** — Compositional Navigation Tensor. Aitchison-native compositional dynamics on the simplex. Source: [`HCI-CNT/`](../HCI-CNT/).
- **CNQ v2.0.0** — Compositional Navigation Quaternion. Twin-quaternion factoring of compositional carriers at D=8. Source: [`HCI-CNQ/`](../HCI-CNQ/).

Both are deterministic, hash-chained, cross-language (Python + R) implementations. Output is byte-identical across runs; hashes are embedded in every artifact.

---

## Map — where to find what

### The conference talk (CoDaWork 2026)

| Item | Location | What it is |
|---|---|---|
| Fresh slide deck (May 12 state) | [`CODAwork2026/CodaWork2026_Talk_2026-05-12.pptx`](CODAwork2026/CodaWork2026_Talk_2026-05-12.pptx) | The talk-as-delivered: 12 slides matching the 10-beat narrative |
| Fresh slide deck (PDF render) | [`CODAwork2026/CodaWork2026_Talk_2026-05-12.pdf`](CODAwork2026/CodaWork2026_Talk_2026-05-12.pdf) | PDF version for screen-share / archival |
| One-page abstract | [`CODAwork2026/ABSTRACT.md`](CODAwork2026/ABSTRACT.md) | What the talk is about, in one page |
| Folder orientation | [`CODAwork2026/README.md`](CODAwork2026/README.md) | What's in the conference subfolder and what's not |
| Canonical speaker materials | [`../papers/codawork2026/talk/`](../papers/codawork2026/talk/) | SPEAKER_BRIEF, README oratory, STUDY_PAGE, CHEAT_SHEET, PEDAGOGICAL_TABLES, BACKUP_PRESENTATION (currently lockdown-locked through 2026-06-06) |

The two locations are intentionally separated. The CODA-Association folder is **community-facing**: clean, current, audit-trail-light, the front door. The `papers/codawork2026/talk/` folder is **speaker-facing**: tactical preparation material under lockdown discipline. New visitors land here; the speaker lands there.

### Scientific results — the CoDa-community-relevant contributions

| Result | Status | Where to read it |
|---|---|---|
| INV-050 — TV / Aitchison metric-invariance pair | CANONICAL | [`../ai-refresh/INVESTIGATION_CATALOG.json`](../ai-refresh/INVESTIGATION_CATALOG.json) (search INV-050) |
| INV-051 — 5-of-9 deceptive-drift signature | CANONICAL | Same catalog, INV-051 entry |
| INV-059 — Humble-invitation framing externally validated | CANONICAL | Same catalog, INV-059 entry |
| INV-029 — Twin-quaternion factoring at D=8 | CANONICAL | Same catalog, INV-029 entry. Engine: [`HCI-CNQ/hci_shared/factoring.py`](../HCI-CNQ/hci_shared/factoring.py) |
| INV-035 — CHSH joint-coherence diagnostic | CANONICAL | Same catalog, INV-035 entry |
| MC-4 — Monitoring Category 4 (parent framing) | HUF-side published framework | [Higgins-Unity-Framework](https://github.com/PeterHiggins19/Higgins-Unity-Framework) — `huf-gov/science/MONITOR-001.json` |
| EITT — Entropy-Invariant Time Transformer | HUF-side published result; 0.18% / 341:1 | [`../papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md`](../papers/EITT_CANONICAL_EXPLANATION_2026-05-12.md) |
| KILL-001 — 19 named failure modes | HUF-side falsifiability artifact | [Higgins-Unity-Framework](https://github.com/PeterHiggins19/Higgins-Unity-Framework) — `huf-gov/governance/KILL-001-kill-test.json` |

### Pedagogy

| Document | Purpose | Where |
|---|---|---|
| Bread the Hs Way | Verbal memorizable narrative — the framework as a recipe for bread | [`../papers/BREAD_THE_HS_WAY_2026-05-12.md`](../papers/BREAD_THE_HS_WAY_2026-05-12.md) |
| Pedagogical tables (Aitchison ↔ SU(2), Helmsman 6-step) | Step-by-step pipeline mapping for Q&A depth | [`../papers/codawork2026/talk/PEDAGOGICAL_TABLES.md`](../papers/codawork2026/talk/PEDAGOGICAL_TABLES.md) |
| Q&A bench cards | Prepared answers for ten anticipated questions | [`../papers/codawork2026/talk/qa_bench/`](../papers/codawork2026/talk/qa_bench/) |

### Governance and falsifiability

| Document | Purpose | Where |
|---|---|---|
| HUF Governance Charter | The parent doctrine (9 articles, April 2026) | [Higgins-Unity-Framework](https://github.com/PeterHiggins19/Higgins-Unity-Framework) — `huf-gov/HUF_GOVERNANCE_CHARTER.md` |
| Hs Change Control v1.0 | Working specialization of the parent doctrine | [`../ai-refresh/CHANGE_CONTROL_README.md`](../ai-refresh/CHANGE_CONTROL_README.md) |
| Breaker inventory | The 16-breaker map with status per breaker | [`../huf-gov/BREAKER_INVENTORY.md`](../huf-gov/BREAKER_INVENTORY.md) |
| Breaker test report | 2026-05-12 falsifiability exercise of the breakers themselves | [`../papers/HUF_GOV_BREAKER_TEST_2026-05-12.md`](../papers/HUF_GOV_BREAKER_TEST_2026-05-12.md) |
| Reproducibility checklist | What it takes to reproduce any plate | [`../REPRODUCIBILITY_CHECKLIST.md`](../REPRODUCIBILITY_CHECKLIST.md) |

### Partnership and outreach

| Document | Purpose | Where |
|---|---|---|
| Post-Coimbra partnership targets matrix | 14 leader systems, what HUF metabolizes from each, bidirectional exchange | [`../papers/POST_CODA_PARTNERSHIP_TARGETS.md`](../papers/POST_CODA_PARTNERSHIP_TARGETS.md) |
| HUF-Gov integration map | Article-by-Article traceability HUF Charter ↔ Hs Change Control v1.0 | [`../huf-gov/HUF_GOV_INTEGRATION.md`](../huf-gov/HUF_GOV_INTEGRATION.md) |

### Engine code (reproducible from these)

| Engine | Language | Schema | Where |
|---|---|---|---|
| CNT v3.1.0 (Python) | Python | schema 3.1.0 | [`../HCI-CNT/cnt.py`](../HCI-CNT/cnt.py) |
| CNT v3.1.0 (R) | R | schema 3.1.0 | [`../HCI-CNT/cnt.R`](../HCI-CNT/cnt.R) |
| CNQ v2.0.0 (Python) | Python | schema cnq/2.0.0 | [`../HCI-CNQ/cnq.py`](../HCI-CNQ/cnq.py) |
| CNQ v2.0.0 (R) | R | schema cnq/2.0.0 | [`../HCI-CNQ/cnq.R`](../HCI-CNQ/cnq.R) |
| Shared library | Python | — | [`../HCI-CNQ/hci_shared/`](../HCI-CNQ/hci_shared/) |
| Expected results (verification) | JSON | — | [`../expected_results.json`](../expected_results.json) |
| Verification script | Python | — | [`../verify_publication_results.py`](../verify_publication_results.py) |

---

## The doctrine line

The same line carries through every document, every slide, and every push:

> *The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*

CoDa community context: **the vocabulary is yours.** Aitchison, Egozcue, Pawlowsky-Glahn, Tolosana-Delgado, Filzmoser, Morais, Arata. The Hs work uses your geometry, your operators, your tradition. The contributions we add — TV distance and K-eff as small supporting metrics, the three-conjunct MC-4 framing, twin-quaternion factoring at D=8, EITT as the temporal-invariance sibling, the hash-chained reproducibility apparatus — sit alongside your work, not above it.

---

## Why this folder exists

Previous folder iterations (`papers/codawork2026/`, `HCI-CNT/conference_demo/talk_deck/`, planning materials in various places) accumulated as the system developed. Visitors landing fresh could not tell which was current. This folder solves that:

- **`CODA-Association/`** is the front door for the CoDa community in general.
- **`CODA-Association/CODAwork2026/`** is the conference-specific subfolder.
- Both folders **reference canonical sources rather than copy them**, so when canonical sources drift these pages do not go stale.

The lockdown discipline (active 2026-05-12 → 2026-06-06) means the speaker-facing material in `../papers/codawork2026/talk/` is locked and authoritative until the conference ends. This folder is additive — new visitor-facing entry points pointing at locked authoritative sources.

---

## File status

- **Created:** 2026-05-12 at Peter's directive *"put only the most current and structured documents for the conference into … help future CoDa users landing and using the repo."*
- **Severity:** S2 (linked doc addition, no current-state claim changes, no engine touches).
- **Lockdown compatibility:** fully compliant — additive S2, no modifications to engine, schema, INV catalog dispositions, NO-CREATE files, or the locked talk material in `papers/codawork2026/talk/`.
- **Travel plan:** stays in working repo; commits with other docs at the first post-conference push window opening 2026-06-06.

---

*The repo holds. The speaker walks to the lectern. The CoDa community has a clean door.*
