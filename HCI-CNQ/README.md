> ⚠️ **ARCHIVED — frozen validation oracle · past reference only.** This is no longer the active Hˢ engine. The **current engine is CN‑TT v4** → [`../HCI-CNTT/`](../HCI-CNTT/) — the latest engine information always lives there (start at [`../HCI-CNTT/CNTT_COMPLETE_SPECIFICATION.md`](../HCI-CNTT/CNTT_COMPLETE_SPECIFICATION.md) and [`../HS_GUIDE.md`](../HS_GUIDE.md)). CN‑TT v4 carries the exact D=4 quaternion reading forward and tiles it to any dimension; it reproduces this engine's output bit‑for‑bit on real data. Retained as the frozen oracle for lineage + validation. **Do not build new work on this engine.** The content below is the historical CNQ v2.0.0 record.

---

# HCI-CNQ — Compositional Navigation Quaternion

> **🎉 CNQ engine fully public — Python + R + pseudocode + 43-test suite (push #27, 2026-05-08).** [`engine/cnq.py`](engine/cnq.py) Python reference. [`engine/cnq.R`](engine/cnq.R) R port (parity contract). [`engine/CNQ_PSEUDOCODE.md`](engine/CNQ_PSEUDOCODE.md) language-agnostic algorithm. [`engine/CNQ_SCHEMA.md`](engine/CNQ_SCHEMA.md) formal output schema. [`engine/ANTI_SPECIFICATION.md`](engine/ANTI_SPECIFICATION.md) failure-mode catalogue. [`engine/tests/`](engine/tests/) 43 tests covering geometry, dimension policy, determinism. All deterministic, all hash-chained to parent CNT. Cross-platform reproduction challenge open.

> **🛡️ For skeptical users — [`../TRUST_AND_VERIFICATION.md`](../TRUST_AND_VERIFICATION.md).** The engine ships in four forms (Python + R + language-agnostic pseudocode + HUF-STD-002 specification) precisely so a skeptical user can re-implement in any language and verify byte-identically against the published code via `cnq_content_sha256`. The engine-independence policy means CNQ verification is independent of CNT verification — each engine carries its own hash and its own conformance test.

**Status (four-field model, push #26):**

| Field | Value |
|---|---|
| `current_repo_status` | **canonical_public_tier** |
| `engine_status` | **cnq.py shipped (push #26)** — full Hamilton-product engine; cross-platform reproduction challenge open |
| `validation_status` | **three IEEE-floor confirmations** (Backblaze D=4, Planck CMB D=4, SM neutrino D=3 boundary support); Round 3 full-corpus validation pending (INV-022) |
| `archive_status` | historical candidate state preserved for audit in [`ARCHIVE_README.json`](ARCHIVE_README.json) and [`HCI-CNQ_ADMIN.json -> status._legacy_single_field_status_for_audit`](HCI-CNQ_ADMIN.json) |

**Sibling of:** [`HCI-CNT/`](../HCI-CNT/) (the established trajectory-navigation tier) and the [`HCI/`](../HCI/) instrument family.
**Foundation:** three IEEE-floor confirmations across drive failures, Planck CMB photons, and Standard-Model neutrino oscillation. See [`experiments/`](experiments/).
**Maturity:** see [`STATUS_AND_MATURITY.md`](STATUS_AND_MATURITY.md), [`CLAIM_STRENGTH_TABLE.md`](CLAIM_STRENGTH_TABLE.md), [`CNQ_SCOPE_AND_LIMITS.md`](CNQ_SCOPE_AND_LIMITS.md), [`ROUND3_VALIDATION_PLAN.md`](ROUND3_VALIDATION_PLAN.md).

---

## What this folder is

This is the canonical home for the **CNQ tier** of the Hs compositional analytics stack. It contains the doctrine that established the tier, the documents that describe how it composes with the rest of the system, and the three reproducible experiments that demonstrate it works.

Two things to be clear about:

1. **The tier is live.** CoDa → CNT → CNQ is now the documented three-level stack. The doctrine, the comparisons with CoDa and CNT, the use-case decision rules, and the engineering proposal for a quaternion-native engine all live in this folder, in public, where they can be inspected, copied, and built on.

2. **The compiled `cnq.py` engine is canonical at v2.0.0.** Shipped in push #32 (2026-05-09) as a ground-up rebuild; lives at [`engine/cnq.py`](engine/cnq.py) with R parity at [`engine/cnq.R`](engine/cnq.R) and the 43-test suite at [`engine/tests/`](engine/tests/). The original proposal in [`tier_system/CNQ_ENGINE_PROPOSAL.md`](tier_system/CNQ_ENGINE_PROPOSAL.md) is preserved for historical reference. Under push #32's engine-independence doctrine, CNQ has its own deterministic hash chain (`cnq_content_sha256`) — not chained to the parent CNT JSON. The three experiments in this folder remain the canonical IEEE-floor demonstrations.

---

## How we work — demonstration first

The tools in this repo are built and tested in public. For every tool in the family — CoDa methods (in the standard CoDa toolkit), CNT (in [`HCI-CNT/`](../HCI-CNT/)), CNQ (here), and the HCI instrument family (in [`HCI/`](../HCI/) and across the repo) — the pattern is the same:

- **We show what the tool is.** Defined in the doctrine, named in the canonical [`HCI-CNT/handbook/GLOSSARY.md`](../HCI-CNT/handbook/GLOSSARY.md).
- **We show what it does, by demonstration.** Real datasets, real outputs, hash-traceable from raw input to plate. The three experiments in this folder are the CNQ-tier demonstrations; the 25-experiment corpus in `HCI-CNT/experiments/` is the CNT-tier demonstration.
- **We document when to use it.** [`tier_system/CNQ_ROI_AND_USE_CASES.md`](tier_system/CNQ_ROI_AND_USE_CASES.md) covers when CNQ is the right tier vs CNT vs straight CoDa.
- **We document how to use it.** Each experiment folder has its script, its inputs, its outputs, and its report. Anyone can re-run.
- **We offer to help build it to specification, free.** If you have a compositional dataset and want to know whether CNQ (or CNT, or HCI) is the right tier for it — open an issue on the repo or follow the build-to-spec contact in the project README. We will help you size the problem, pick the tier, and build the analysis.

The repo cannot talk about a phantom method. This folder exists because the CNQ tier is published on the same terms as the rest of the Hs system: in the open, with the code, with the receipts, with the help available.

---

## Folder map

```
HCI-CNQ/
├── README.md                       (this file)
├── HCI-CNQ_ADMIN.json              project state and provenance
├── ARCHIVE_README.json             original QD-project state record (preserved as audit)
│
├── doctrine/                       what the tier is and why
│   ├── CENTRAL_CLAIM.md            "CNT measures invariance. CNQ names the algebra it lives in."
│   ├── DEEPER_CONNECTIONS.md       ten correspondences with claim-strength labels
│   ├── CONCEPTS_FOR_TEST.md        operational test catalogue
│   ├── CORPUS_COMPARISON_PLAN.md   surpass-and-include methodology vs the CNT corpus
│   └── BENEFITS_POST_CODA.md       integration benefits for the CoDa community
│
├── tier_system/                    how CoDa + CNT + CNQ compose
│   ├── README.md                   the CNQ tier overview (originally Hs-CNQ/README.md)
│   ├── CNQ_TIERED_SYSTEM.md        three-tier explanation
│   ├── CNQ_VS_CODA_VS_CNT_COMPARE.md   updated comparison table
│   ├── CNQ_ROI_AND_USE_CASES.md    when CNQ makes sense, decision rules
│   └── CNQ_ENGINE_PROPOSAL.md      historical engineering plan (executed in push #32, 2026-05-09; v2.0.0 shipped)
│
└── experiments/                    the three working demonstrations
    ├── backblaze_fleet_quaternion/   Round 2 — drive failures (D=4, T=731)
    │   ├── QD_round_2.py             script
    │   ├── QD_round_2_results.json   per-pair quaternion sandwich-product results
    │   └── QD_ROUND_2_REPORT.md      verdict and reasoning
    │
    ├── planck_cmb_quaternion/        Round 2.5 — Planck CMB best-fit theory (D=4, T=2499)
    │   ├── QD_round_2_5_planck.py    script
    │   ├── QD_round_2_5_results.json results
    │   ├── QD_ROUND_2_5_REPORT.md    verdict (boson sector falsification + reformulation)
    │   ├── planck_cmb_boson_input.csv
    │   ├── planck_cmb_boson_cnt.json
    │   └── planck_theory_raw.txt
    │
    └── sm_neutrino_quaternion/       Round 2.6 — SM 3-flavour νμ oscillation (D=3, T=1000)
        ├── QD_round_2_6_neutrino.py  script
        ├── QD_round_2_6_results.json results
        ├── sm_numu_oscillation_input.csv
        └── sm_numu_oscillation_cnt.json
```

---

## The three demonstrations (what you can re-run today)

| Round | Dataset | D | T | Test | Result |
|---|---|---:|---:|---|---|
| 2 | `backblaze_fleet` (drive-failure compositions) | 4 | 731 | Sandwich product reproduces Aitchison rotation | max diff **4.441 × 10⁻¹⁶** (IEEE floor) |
| 2.5 | Planck 2018 CMB best-fit theory spectrum | 4 | 2499 | Sandwich + M²=I | bit-identical residual + M²=I 7.63 × 10⁻¹⁷ |
| 2.6 | Standard-Model 3-flavour νμ oscillation | 3 | 1000 | LIMIT_CYCLE_P2 + M²=I | LIMIT_CYCLE_P2 confirmed + M²=I 7.40 × 10⁻¹⁷ |

The 4.441 × 10⁻¹⁶ figure is exactly 2 × IEEE 754 machine epsilon — the hardware floor. Bit-identical residual across two completely different datasets shows the quaternion identification is **mathematically exact**, not approximate. Three datasets span ~30 orders of magnitude in physical scale: subatomic neutrinos → drive failures → cosmic photons. All three agree at the same hardware-precision floor.

To re-run any of them:

```
cd HCI-CNQ/experiments/backblaze_fleet_quaternion
python QD_round_2.py     # produces QD_round_2_results.json
```

(Each script is self-contained and reads from its own folder. The Planck and neutrino scripts use the matching input CSVs in their respective experiment folders.)

---

## Where this fits in the Hs system

| Tier | Engine | Doctrine | Demonstrations | Status |
|---|---|---|---|---|
| **CoDa** | community-standard tools (Aitchison closure, CLR, ILR, balance, ternary, biplot) | classical CoDa references | the literature | foundational layer the rest sits on |
| **CNT** | [`HCI-CNT/engine/cnt.py`](../HCI-CNT/engine/cnt.py) (3.1.0, schema 3.1.0; push #37) | [`HCI-CNT/handbook/`](../HCI-CNT/handbook/) (Volumes I–IV) | 101-dataset reference suite (push #34) + 9-country EMBER corpus | live; deterministic; field-use across small-to-medium D |
| **CNQ** | [`HCI-CNQ/engine/cnq.py`](engine/cnq.py) (2.0.0, schema cnq/2.0.0; push #32) + [`engine/cnq.R`](engine/cnq.R) parity port | this folder, plus [`HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md`](../HCI-CNT/handbook/VOLUME_4_QUATERNION_VIEW.md) | three IEEE-floor confirmations (this folder) + 43-test suite | live; deterministic; engine independent of CNT (separate hash chain by design) |
| **HCI** family | [`HCI/`](../HCI/) (CBS, Stage 1 plate generator, more) | [`HCI/HCI_FOUNDATION.md`](../HCI/HCI_FOUNDATION.md) | calibration suite + EMBER plates | live; deterministic; specialised instruments |

The four tiers are siblings, not replacements. Picking the right tier for a problem is part of what we offer to help with — see [`tier_system/CNQ_ROI_AND_USE_CASES.md`](tier_system/CNQ_ROI_AND_USE_CASES.md).

---

## How to engage

- **Re-run a demonstration.** Each `experiments/*/` folder is self-contained.
- **Read the doctrine.** `doctrine/CENTRAL_CLAIM.md` first; then `doctrine/DEEPER_CONNECTIONS.md` if you want the ten correspondences; then any of the tier_system docs.
- **Compare against your data.** Open an issue on the public repo describing the dataset; we can talk about whether CNQ, CNT, or straight CoDa is the right tier.
- **Ask for build-to-spec help.** Free. If your data is novel and the tooling needs an extension or an adapter, we will help you build it. The catch is just that it lands in the public repo on the same terms as everything else: open code, hash-chained outputs, doctrine published.
- **Sit in on the engine build.** When `cnq.py` lands, the build will be in public. Watch the commit stream, raise issues, propose tests.

---

## What this isn't

**Not a closed product.** Every script, every JSON, every doctrine document in this folder is licensed on the same terms as the rest of the repo. Use it. Cite it. Improve it.

**Not a CNT replacement.** CNT remains the canonical engine for the 25-experiment corpus and for everything in field use today. CNQ is for the cases CNT was not designed for — high D, large T, multi-trajectory bundles, problems where the cross-dataset structure is the primary observable.

**Not a finished theory.** Three IEEE-floor confirmations is strong evidence and is enough to make the tier public. It is not enough to claim the architecture is right at every dimension. Help us test it.

---

## Provenance — how this folder got here

The CNQ tier was developed in an experimental folder at the Cowork workspace root (`Quaternion Decomposition/`) between 2026-05-06 and 2026-05-07. It was kept outside the canonical repo while the foundational claim was being tested. After the third IEEE-floor confirmation landed, and after independent cross-check from a second AI platform (ChatGPT) confirmed the architectural framing, the entire body of work was promoted to canonical status on 2026-05-07.

The promotion is documented in:

- [`../ai-refresh/AI_REFRESH_2026-05-07_quaternion_integration.md`](../ai-refresh/AI_REFRESH_2026-05-07_quaternion_integration.md) — push #22 narrative (Volume IV integration into the handbook).
- [`../ai-refresh/AI_REFRESH_2026-05-07_chatgpt_crosscheck.md`](../ai-refresh/AI_REFRESH_2026-05-07_chatgpt_crosscheck.md) — the cross-check turn that confirmed the framing.
- [`