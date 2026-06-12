# Hs (Higgins Decomposition) — Fast Refresh

> **⚠️ HISTORICAL SNAPSHOT — push #27 (2026-05-08).** This Markdown mirror has not been regenerated since push #27 and reports outdated engine versions and investigation counts. For live current state (CNT v3.1.0, CNQ v2.0.0, 63+ investigations as of push #47), load [`HS_FAST_REFRESH.json`](HS_FAST_REFRESH.json) — it is the single live source of truth under Hs Change Control v1.0 rule HCC-R001. This file is preserved as a legacy snapshot for traceability per HCC-R004 (archive preservation). The figures below are historical and may not match current canon.

**Single-file context loader for any AI session or fresh reader.**
**Companion machine-readable form:** [`HS_FAST_REFRESH.json`](HS_FAST_REFRESH.json) — **this JSON is the authoritative live state.**
**Version:** 1.0 (2026-05-08, push #27) — **snapshot only, see legacy header above.**

---

## Identity

- **Framework:** Higgins Decomposition (Hs)
- **Author:** Peter Higgins (Rogue Wave Audio / Binaural Test Lab, Markham, Ontario, Canada)
- **Repo:** [github.com/PeterHiggins19/higgins-decomposition](https://github.com/PeterHiggins19/higgins-decomposition)
- **Public-use status:** **fully public** (push #26+#27, 2026-05-08). Engines, docs, experiments, and corpus all under the repo licence.
- **Doctrine:** *The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
- **Central claim:** *CNT measures invariance. CNQ names the algebra it lives in.*

---

## What you can do today

| If you want to … | Read this | Then run this |
|---|---|---|
| Use CNT (compositional analysis on a CSV) | [`HCI-CNT/handbook/`](HCI-CNT/handbook/) Volumes 1–4 | `python HCI-CNT/engine/cnt.py input.csv -o output.json` |
| Use CNQ (quaternion-native view of a CNT JSON) | [`HCI-CNQ/CNQ_SCOPE_AND_LIMITS.md`](HCI-CNQ/CNQ_SCOPE_AND_LIMITS.md) | `python HCI-CNQ/engine/cnq.py --cnt-json X.json --out Y.json` |
| Use CNT in R | [`HCI-CNT/engine/README.md`](HCI-CNT/engine/) | `Rscript HCI-CNT/engine/cnt.R input.csv output.json` |
| Use CNQ in R | [`HCI-CNQ/engine/CNQ_PSEUDOCODE.md`](HCI-CNQ/engine/CNQ_PSEUDOCODE.md) | `Rscript HCI-CNQ/engine/cnq.R --cnt-json X.json --out Y.json` |
| Reproduce the three IEEE-floor confirmations | [`HCI-CNQ/results/expected_results.json`](HCI-CNQ/results/expected_results.json) | `python HCI-CNQ/scripts/run_all_confirmations.py --repo-root .` |
| Verify against locked expected values | (same) | `python HCI-CNQ/scripts/verify_publication_results.py --repo-root .` |
| Run the AI-led 7-phase reproduction protocol | [`ai-refresh/CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md) | follow phases 1–7 |
| Review the audit-trail of every speculative branch | [`ai-refresh/INVESTIGATION_CATALOG.md`](ai-refresh/INVESTIGATION_CATALOG.md) | (29 entries: 9 CANONICAL, 12 DEFERRED, 1 FALSIFIED, 7 OPEN) |

---

## Engines (all four shipped, all public)

| Engine | Path | Version | Schema | Lang | Tests |
|---|---|---|---|---|---|
| CNT Python | [`HCI-CNT/engine/cnt.py`](HCI-CNT/engine/cnt.py) | 2.0.4 | 2.1.0 | Python 3.9+ | `HCI-CNT/engine/tests/` (4 modules) |
| CNT R | [`HCI-CNT/engine/cnt.R`](HCI-CNT/engine/cnt.R) | 2.0.4 | 2.1.0 | R 4.0+ | parity-tested against cnt.py |
| CNQ Python | [`HCI-CNQ/engine/cnq.py`](HCI-CNQ/engine/cnq.py) | 1.0.0 | cnq/1.0.0 | Python 3.9+ | `HCI-CNQ/engine/tests/` (43 tests) |
| CNQ R | [`HCI-CNQ/engine/cnq.R`](HCI-CNQ/engine/cnq.R) | 1.0.0 | cnq/1.0.0 | R 4.0+ | parity contract with cnq.py |
| **Pseudocode** | [`HCI-CNQ/engine/CNQ_PSEUDOCODE.md`](HCI-CNQ/engine/CNQ_PSEUDOCODE.md) | — | — | language-agnostic | conformance test in §9 |

All engines are deterministic. Two runs on the same input produce identical content hashes. Cross-platform reproducibility is the test: any reviewer can clone, run, and match the published `cnq_content_sha256`.

---

## The three IEEE-floor confirmations

| Dataset | D | T | max residual | Termination | Role |
|---|---|---|---|---|---|
| Backblaze fleet (drive failures) | 4 | 731 | **4.441 × 10⁻¹⁶** | LIMIT_CYCLE_P2 | confirmed (load-bearing) |
| Planck CMB photon power | 4 | 2499 | **4.441 × 10⁻¹⁶** | LIMIT_CYCLE_P2 / OVERDAMPED_EXTREME | confirmed (load-bearing) |
| SM neutrino oscillation | 3 | 1000 | 3.331 × 10⁻¹⁶ | LIMIT_CYCLE_P2 / LIGHTLY_DAMPED | consistency support |

**Bit-identical residual on Backblaze and Planck** (two physically unrelated D=4 datasets) → the residual is hardware float64 representation, not algorithmic noise. The mathematics is exact on the simplex.

---

## Vocabulary that holds the line

These are locked per [`HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md`](HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md). Other docs cite that file.

- **Order, not rank** — for index count on a tensor. Reserve "rank" for matrix rank or CP-decomposition rank.
- **κᴴˢ_ij** is the **order-2** Aitchison pullback metric (full tensor); **s_j = 1/x_j** is the **order-1** carrier sensitivity vector. Distinct objects.
- **Twin-quaternion factoring**, not "bi-quaternion factoring", for the SU(2) × SU(2) decomposition of D=8 trajectories. Strict bi-quaternion (ℍ ⊗ ℂ) is a different object.
- **Tier** (CoDa/CNT/CNQ) ≠ **Stage** (atlas plate 1/2/3/4) ≠ **Order** (tensor index count) ≠ **Level** (HLR magnitude) ≠ **Regime** (HUF multi-scale).
- **BTL = Binaural Test Lab** — single canonical identity. Sound-controlled professional laboratory in Markham + four-laboratory institutional deployment (2 Ottawa, 2 Monaco) operated by a private Canadian industrial sponsor.

---

## Dimension policy (CNQ)

| D | Label | Claim strength |
|---|---|---|
| 4 | `native_quaternion` | confirmed (load-bearing) |
| 3 | `boundary_or_degenerate_support` | consistency channel only |
| 2 | `degenerate_below_quaternion` | bearing only; quaternion view does not apply |
| 8 | `bi_quaternion_factoring_candidate` | experimental (INV-029); formal name = twin-quaternion |
| ≥5 (not 8) | `reduced_or_projected` | projection diagnostic only |

---

## Cross-platform reproduction challenge — open

**To any AI platform or third-party reviewer:** clone the repo, run

```
python HCI-CNQ/scripts/run_all_confirmations.py --repo-root .
```

and compare your `cnq_content_sha256` against the reference observations in [`HCI-CNQ/results/expected_results.json`](HCI-CNQ/results/expected_results.json). Bit-identical hashes across platforms = a fourth independent confirmation channel beyond the three load-bearing datasets. Hash drift is a finding, not a failure — file a GitHub issue.

---

## Drift errors caught (cross-AI session log)

These are mistakes that have actually happened in AI sessions. Look for them during refresh:

| Drift | Catch date | Push |
|---|---|---|
| "rank-N" used for tensor index count | 2026-05-08 | #27 |
| κᴴˢ conflated with s_j = 1/x_j | 2026-05-07 | #23 |
| "Bi-quaternion" used for SU(2)×SU(2) factoring (strict bi-quaternion is ℍ⊗ℂ) | 2026-05-08 | #27 |
| BTL framed as dual-gloss "Below Threshold Loudspeaker" / "Binaural Test Lab" | 2026-05-08 | #24 |
| BTL described as "basement lab" (unprofessional) | 2026-05-08 | #24 |
| H₁ paper miscited as "published" (self-hosted only) | 2026-05-08 | #24 |
| D=3 neutrino claimed as native quaternion proof (it's consistency support) | 2026-05-08 | #26 |
| "EXPERIMENTAL — NOT FOR REPO USE" / "do_not_push" guards used as live state | 2026-05-08 | #27 |

---

## Investigation catalog (research methodology layer)

29 classified investigations: 9 CANONICAL, 12 DEFERRED, 1 FALSIFIED, 7 OPEN.

By source: Claude 7, ChatGPT 6, Grok 10, User 6.

The catalog is the audit trail. Every speculative branch from any AI cross-check has a disposition + gate criteria. Falsifications are kept on record (see INV-002: P2-as-fermion conjecture, falsified 2026-05-07, reformulated to universal compositional invariance signature).

Authoritative file: [`ai-refresh/INVESTIGATION_CATALOG.json`](ai-refresh/INVESTIGATION_CATALOG.json) + [`.md`](ai-refresh/INVESTIGATION_CATALOG.md) companion.

---

## Paper pipeline

1. **Paper 1** (INV-026) — *A Universal Compositional Invariance Signature*. Draft 3 in [`papers/in_progress/`](papers/in_progress/). Target: arXiv physics.data-an. Release tag `v3.0.0-paper1` after Round 3 (INV-022) lands.
2. **Paper 2** (INV-027) — *DADC Origin and Independent Discovery of Compositional Data Analysis*. Outline drafted. Target: CoDaWork 2026.

Both papers are tied to the canonical engines and the locked claim-strength language.

---

## Origin

The compositional mathematics in Hs originated in Peter's loudspeaker work at the Binaural Test Lab — specifically DADC (Dimension-Apportioned Diffraction Correction). The lineage is documented at [`HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md). The arc:

```
DADC (loudspeakers, BTL) → H₁ (Higgins Operator on Hilbert space) → HUF
                                                                      ↓
                                                                      Hs → CNT → CNQ
```

The companion repository [Higgins-Unity-Framework (HUF)](https://github.com/PeterHiggins19/Higgins-Unity-Framework) covers the governance / theory / EITT side.

---

## Contact

Peter Higgins — `peterhiggins2016@gmail.com` (personal) / `PeterHiggins@RogueWaveAudio.com` (business)
Rogue Wave Audio, Markham, Ontario, Canada

---

*The simplex is the simplex regardless of what lives on it.*
