# HIGGINS DECOMPOSITION (Hˢ)

> **Available in UN-6 locales** · English (this file, canonical) · [Français](Higgins_Decomposition_Handout_CoDaCommunity.fr.md) · [Español](Higgins_Decomposition_Handout_CoDaCommunity.es.md) · [Русский](Higgins_Decomposition_Handout_CoDaCommunity.ru.md) · [中文](Higgins_Decomposition_Handout_CoDaCommunity.zh.md) · [العربية](Higgins_Decomposition_Handout_CoDaCommunity.ar.md). Non-English versions are drafts pending native expert review per `HCI-CNQ/wrappers/WRAPPER_SCHEMA.md §11.1`.

**Operationalizing compositional data analysis — a runnable standard for researchers and the AI assistants they choose**

*"Compositional monitoring of energy-mix drift on the simplex"*
**CoDaWork 2026 · Coimbra, Portugal · June 1–5**
Peter Higgins · Rogue Wave Audio / Binaural Test Lab · Markham, Ontario, Canada

---

## By the numbers

| 11 | 101 | 44 | 3 | 22 + 66 | ~220 |
|:--:|:--:|:--:|:--:|:--:|:--:|
| validated domains | reference datasets | orders of magnitude | IEEE-floor physics confirmations | slides — talk + cinema scroll | glossary v3.0 entries |

---

## What this is

Aitchison gave the field its geometry in 1986; CoDaWork has trained four decades of methodologists. **Hˢ packages current and developing CoDa methods into a runnable operational standard** — seven phases, two human gates, deterministic hash-chained output, identical results whether the keystrokes come from a researcher or from an AI assistant. The math is standard; the operational frame may be new.

---

## Why operationalize compositional analysis

- **Measurability.** Turns theoretical compositional structure into reproducible per-step diagnostics: helmsman (handedness), Power Share, Activation Coefficient, navigation bearing. Quantifiable, comparable, audit-able.
- **Consistency.** Fixed schema (CNT v3.1.0 / CNQ v2.0.0), fixed pipeline, byte-identical re-runs across machines, OS, BLAS, and years. Same input, same output, always.
- **Hypothesis testing.** The same engine that produces a finding produces the falsifiability frame (MC-4 — four named defeat paths) that would overturn it. No publication-without-falsification.

---

## Numerical and operational advantages over ad-hoc CoDa pipelines

- **Helmert-ILR orthonormal coordinates** — no choice-of-balance arbitrariness; deterministic basis across teams.
- **atan2 for helmsman and navigation angles** — wrap-safe across ±π; no precision loss or sign jumps at the cycle boundary.
- **Hash-chained provenance** — SHA-256 from raw CSV through CNT JSON, plates, projector, and manuscript figure. A reviewer in 2030 can prove nothing changed.
- **IEEE-floor cross-platform determinism** — verified on Backblaze drive telemetry, Planck CMB polarization, Standard-Model neutrino oscillations.
- **Coherent Range Doctrine (CRD-1.0)** — multi-carrier comparisons computed on the intersection of all members' ranges; asymmetric-drift artifacts eliminated.
- **Schema-versioned outputs** — every JSON declares its schema; the conference corpus is locked at `3.1.0` / `cnq/2.0.0` and remains readable independently of engine version drift.

---

## The three-layer operational standard

| Layer | Role | What it does |
|---|---|---|
| **CNT v3.1.0** | measure | Closure → CLR → Helmert-ILR → per-step compositional metrics, helmsman, Power Share, Activation Coefficient, navigation, diagnostics, hashes. Current source v3.2.0 adds `navigation_2d` for ILR-Helmert PCA barycenter trajectory. |
| **CNQ v2.0.0** | name the algebra | Quaternion-view dashboards and higher-order structure diagnostics (CHSH joint coherence, twin-quaternion factoring at D=8 with Tsirelson-bound respect). Algebraic companion to CNT. |
| **CCTT v1.0** | operationalize | The runnable standard. Seven phases (diagnose → adapter *gate* → engine → outputs → render → self-verify *gate* → present + journal). Two human gates; everything else deterministic. **The repo trains both researcher and AI assistant — same protocol, identical hash-verifiable output.** |

---

## CCTT 7-phase protocol

`[1] Diagnose` → `[2] Adapter (gate)` → `[3] Engine` → `[4] Outputs` → `[5] Render` → `[6] Self-verify (gate)` → `[7] Present + journal`

---

## Five viewpoints in the talk

- **Composition** — share each carrier has.
- **Helmsman** — largest CLR displacement at a step.
- **Helmsman trajectory** — when steering changes.
- **Power Share** — how much squared CLR motion each carrier did.
- **Activation Coefficient** — Power Share ÷ starting share = "yeast factor."

---

## Operational evidence — what the standard surfaces

A carrier can be small in share but large in structural work. **USA Solar 2012 → 2013:** 0.107% starting share, 81.7% of structural Power Share, **Activation Coefficient ≈ 760×**.

The cross-country deceptive-drift signature fires in **5 of 9 countries** (AUS, CHN, GBR, IND, JPN) and does *not* fire in DEU (annual), FRA, USA, or WLD. The protocol discriminates; it does not over-fire. **A regression on raw shares would not have surfaced either finding.**

---

## Standard onboarding — choose your entry point

1. **Conference attendee:** `CODA-Association/CONFERENCE_ATTENDEES.md` — slide-by-slide follow-along.
2. **Explore visually (zero install):** `CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html`.
3. **Run your own composition:** `QUICKSTART.md` + `ai-refresh/CCTT_QUICKSTART.md` — 7-phase runbook, manual or AI-assisted.
4. **Verify a published number:** manuscript + Supplementary Information + per-country JSON + hash chain.
5. **Vocabulary lookup:** `HCI-CNT/handbook/GLOSSARY.md` v3.0 (~220 entries: PCA, SVD, CLR/ILR, Helmert, CHSH, Tsirelson, Activation Coefficient, MC-1..MC-4).

---

## Contact and adoption

| Field | Details |
|---|---|
| **Talk** | *"Compositional monitoring of energy-mix drift on the simplex,"* CoDaWork 2026, Coimbra, June 1–5. Find Peter during sessions and Q&A — happy to walk the projector live. |
| **Contact** | Peter Higgins — **PeterHiggins@RogueWaveAudio.com** · Rogue Wave Audio / Binaural Test Lab, Markham, Ontario, Canada |
| **Repository** | `github.com/PeterHiggins19/higgins-decomposition` · community: `CODA-Association/` · conference: `CODA-Association/CODAwork2026/` |
| **How to cite** | Higgins, P. (2026). *Compositional monitoring of energy-mix drift on the simplex.* CoDaWork 2026, Coimbra. Repo: github.com/PeterHiggins19/higgins-decomposition (commit in `HS_FAST_REFRESH.json`). |
| **How to adopt** | Fork the repo, run the 7-phase CCTT on your composition, file a `JOURNAL.md`. AI assistant follows the same gates. See `ai-refresh/COMMUNITY_TEST_PACKET.json` for the structured adoption test. |
| **License** | Apache-2.0 (code) · CC BY 4.0 (docs and figures). Fully open source — fork, audit, extend, attribute. |

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line. The AI follows the same protocol.*
