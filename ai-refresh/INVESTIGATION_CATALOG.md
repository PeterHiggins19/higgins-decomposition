# Investigation Catalog

**Status:** canonical research-methodology document, push #24 (2026-05-08).
**Machine-readable companion (JSON):** [`INVESTIGATION_CATALOG.json`](INVESTIGATION_CATALOG.json). This Markdown file is the plain-text companion.
**Registered in:** [`HS_ADMIN.json`](HS_ADMIN.json) → `investigation_catalog` (top-level block).

---

## Why this exists

The framework treats compositional data as a living record where every contribution above the EITT 5% threshold counts as a carrier; below 5% it doesn't make the cut. The same discipline applies to research investigations. Every speculative branch raised by any AI session, user contributor / researcher, or experimental pilot is data — and the disposition record is the audit trail.

This catalog is the project's research-methodology equivalent of the determinism contract: **the path of every idea is traceable**. Falsified hypotheses are kept on record (Round 2.5 Concept 4 was a falsification turned into a stronger reformulation). Deferred speculations are gated by clear pilot criteria. Open work has explicit gate criteria so future sessions know what would resolve it.

The catalog is updated every time a new investigation is raised, promoted, deferred, or falsified.

---

## Disposition taxonomy

| Disposition | Meaning | When applied |
|---|---|---|
| **CANONICAL** | Met its promotion gate. Lives in the repo. Binding doctrine, code, or schema. | After verification, pilot success, or external confirmation. |
| **DEFERRED** | Mathematically coherent or experimentally proposed, but unvalidated. Archived; awaits a pilot. | When an idea is interesting but has not been grounded. |
| **FALSIFIED** | Tested and refuted. Kept on record as audit trail. | After a clear falsification event (with reformulation if available). |
| **OPEN** | Raised, in progress, gate criteria stated, awaiting resolution. | When work is active but incomplete. |

---

## Catalog by disposition (push #24 snapshot)

### CANONICAL (9 investigations)

| ID | Title | Source | Push | Pointer |
|---|---|---|---|---|
| INV-001 | Volume IV — Quaternion View | CLAUDE | #22 | `HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md` |
| INV-003 | ChatGPT vocabulary integration (HCI family terms) | CHATGPT | #23 | `HCI-CNT/handbook/GLOSSARY.md` §H |
| INV-004 | CodaWork 2026 talking-points overlay | CHATGPT | #23 | `HCI-CNT/conference_demo/CODAWORK2026_TALKING_POINTS.md` |
| INV-005 | HCI-CNQ tier promotion | USER | #23 | `HCI-CNQ/` |
| INV-008 | DADC origin lineage | GROK | #24 | `HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md` |
| INV-009 | Helmsman family vocabulary (PROPOSED status) | GROK | #24 | `HCI-CNT/handbook/GLOSSARY.md` §I |
| INV-010 | HCI-AUDIO canonical sibling tier | USER | #24 | `HCI-AUDIO/` |
| INV-011 | HCI-ULTRASOUND canonical sibling tier | USER | #24 | `HCI-ULTRASOUND/` |
| INV-012 | RWA-001 lab identity card | USER | #24 | `RWA/RWA-001.json` |

### DEFERRED (12 investigations)

| ID | Title | Source | Gate for promotion |
|---|---|---|---|
| INV-006 | HCI-MOL — protein sliding-window analysis | CHATGPT | Working pilot on a real protein dataset |
| INV-007 | HCI-VR — Spatial Morphographic Analyzer | CHATGPT | Working pilot rendering a canonical experiment in 3D |
| INV-013 | CNQ-Q — quark sector with CKM mapping | GROK | Computational pilot on public CKM/flavour data |
| INV-014 | Pilot-wave guidance equation in CNQ language | GROK | Pilot demonstrating equivalence to standard pilot-wave simulations |
| INV-015 | Many-droplet entanglement analogs (CHSH on joint q) | GROK | Working two-droplet/two-channel simulation reproducing predicted S |
| INV-016 | Period-doubling cascade + Feigenbaum on compositional dynamics | GROK | Numerical demonstration of cascade with measurable δ at universal value |
| INV-017 | Renormalization fixed point + spectral gap on depth-tower operators | GROK | Numerical implementation extracting δ from real CNT depth-tower data |
| INV-018 | Hausdorff dimension via transfer operator on compositional attractors | GROK | Numerical extraction of d_H from real depth-tower trajectory |
| INV-019 | Quantum acoustic phonon simplex applications | GROK | Working pilot on real or simulated cQAD data |
| INV-020 | WaveMechanics-CNQ Database (full system spec) | GROK | Working prototype with at least one acoustic dataset analyzed end-to-end |
| INV-028 | **HCI Dyadic Coupling Ladder** — order-2/4/8 tensor diagnostic | CHATGPT | Working pilot showing C_ijkl detects structure order-2 κᴴˢ_ij misses |
| INV-029 | **CNQ Twin-Quaternion Factoring** — D=8 SU(2)×SU(2) decomposition (legacy name: bi-quaternion) | CHATGPT | Working pilot on EMBER D=8 country trajectory showing ρ_AB domain signal |

### FALSIFIED (1 investigations)

| ID | Title | Source | Falsification record | Reformulation |
|---|---|---|---|---|
| INV-002 | QD R2.5 Concept 4 (P2=fermion, P1=boson) | CLAUDE | Planck CMB (pure boson) terminated at P2 not P1 | LIMIT_CYCLE_P2 is universal compositional invariance signature, not particle-content distinguisher |

### OPEN (7 investigations)

| ID | Title | Source | Gate for promotion | Owner |
|---|---|---|---|---|
| INV-021 | `cnq.py` compiled engine | CLAUDE | Reproduces every CNT corpus content_sha256 byte-for-byte via quaternion path (~14 days) | open |
| INV-022 | Round 3 — full-corpus quaternion-view validation | CLAUDE | All 25 D=4 cases at IEEE floor; D≠4 documented (~1 day) | open |
| INV-023 | T2K/NOvA real-data neutrino verification | CLAUDE | Pilot run; result published regardless of outcome | open |
| INV-024 | First HCI-AUDIO pilot — Peter's 4-way system | USER | Single experiment record with helmsman + alignment metrics | Peter |
| INV-025 | First HCI-ULTRASOUND pilot — industrial composite inspection | USER | Single experiment record with documented S_σ time series | open |
| INV-026 | **Paper 1 — Universality result (arXiv wedge)** | CLAUDE | Full draft + arXiv submission ID + paper PDF in `Hs/papers/published/` | Peter (authorship); Claude (drafting) |
| INV-027 | **Paper 2 — DADC origin & CoDa independent discovery (CodaWork 2026)** | CLAUDE | Full draft + conference acceptance + paper PDF in `Hs/papers/published/` | Peter (authorship); Claude (drafting) |

---

## Source distribution

| Source | Count | Investigations |
|---|---:|---|
| CLAUDE | 7 | INV-001, INV-002, INV-021, INV-022, INV-023, INV-026, INV-027 |
| CHATGPT | 6 | INV-003, INV-004, INV-006, INV-007, INV-028, INV-029 |
| GROK | 10 | INV-008, INV-009, INV-013, INV-014, INV-015, INV-016, INV-017, INV-018, INV-019, INV-020 |
| USER | 6 | INV-005, INV-010, INV-011, INV-012, INV-024, INV-025 |
| PILOT | 0 | (reserved for future) |
| **Total** | **29** | |

Cross-platform pattern visible in the data: Claude builds and verifies, ChatGPT cross-checks vocabulary and framing, Grok extends speculatively. User-led investigations (Peter) carry the applied-work surfacing and the corporate/lab identity work. Each source has a different signature in the catalog.

---

## How to use this catalog

### When raising a new investigation

Add an entry to `INVESTIGATION_CATALOG.json` with the next sequential id (`INV-NNN`). Required fields:

- `id`, `title`, `raised_by`, `raised_date`, `raised_in_push`
- `disposition` (one of CANONICAL / DEFERRED / FALSIFIED / OPEN)
- `summary`
- `gate_criteria` (or `gate_for_promotion` / `falsification_record` per disposition)

Update `summary_by_disposition` and `summary_by_source` counts. Mirror the entry into the disposition table in this MD file.

### When updating a disposition

| From | To | Triggers |
|---|---|---|
| OPEN → CANONICAL | Gate criteria met. Add `promotion_date`, `canonical_location`, `gate_outcome`. |
| OPEN → DEFERRED | Pilot deferred. Add `deferred_to_location`. |
| OPEN → FALSIFIED | Test refuted. Add `falsification_date`, `falsification_record`, `reformulation` if any. |
| DEFERRED → CANONICAL | Pilot grounds the speculation. Same gate as OPEN → CANONICAL. |
| DEFERRED → FALSIFIED | Pilot run, refuted. Standard falsification record. |
| CANONICAL → RETIRED | Reserved for future use. |

### When deciding whether to add an investigation at all

Two thresholds, by analogy with EITT:

- **Above the 5% threshold (qualifies as a carrier)**: any speculative branch worth a paragraph in the AI-refresh archive deserves an investigation entry. Cataloguing is cheap and the audit trail is valuable.
- **Below threshold**: throwaway remarks, side jokes, and routine implementation choices do not need entries.

When in doubt, err toward inclusion. The catalog is meant to grow.

---

## Promotion gates — a few worked examples

**INV-001 (Volume IV) — promoted CANONICAL.** Gate was three IEEE-floor confirmations on disparate datasets. Met by QD Rounds 2 (backblaze), 2.5 (Planck CMB), 2.6 (SM neutrino) at 4.441 × 10⁻¹⁶. The bit-identical residual across two unrelated datasets was the deciding evidence — it showed the residual was hardware floating-point representation error, not algorithmic noise.

**INV-002 (Concept 4 fermion/boson conjecture) — moved to FALSIFIED.** The Planck CMB Round 2.5 test was specifically designed to falsify or confirm. Pure-photon (boson) data terminated at P2, not P1. Conjecture refuted. The reformulation — that P2 is a universal signature independent of particle statistics — is the cleaner truth and is what Volume IV §E now encodes.

**INV-013 (CNQ-Q quark sector) — DEFERRED.** Mathematically coherent. Has a documented gate: working computational pilot on public CKM data with measurable CNQ-style invariance signatures. Until that pilot exists, the doctrine stays in the Grok crosscheck archive. This is the demonstration-first discipline applied to a speculative extension.

**INV-021 (cnq.py engine) — OPEN.** Estimated 14-day implementation. Gate is straightforward: reproduce every CNT corpus content_sha256 via the quaternion-native path. When that's done, Volume IV's claim becomes engine-level rather than doctrine-level.

---

## Cross-references

- Push #22 narrative (Volume IV): [`AI_REFRESH_2026-05-07_quaternion_integration.md`](AI_REFRESH_2026-05-07_quaternion_integration.md)
- Push #23 narrative (ChatGPT crosscheck + HCI-CNQ): [`AI_REFRESH_2026-05-07_push23_chatgpt_in