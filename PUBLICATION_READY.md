# Hs — Higgins Decomposition

**Public-use status:** fully public. Engines, docs, experiments, corpus, and protocols all under the repository LICENSE. No "do not push" or "experimental — not for use" guards remain anywhere in the system. Anyone may clone, run, reproduce, cite, build on, or critique this repository.

**One-line summary.** A deterministic, hash-verified, multi-language compositional inference instrument: CNT measures the structural invariances of compositional dynamics on the simplex; CNQ names the algebra those invariances live in; everything is reproducible to IEEE float64 floor across platforms.

**Audience.** Researchers, practitioners, code reviewers, AI assistants, and curious readers of any technical level. If you have a CSV of compositional time-series, you can produce a CNT-grade analysis from a clean clone in two commands.

> **🛡️ Trust path for skeptical users.** Every algorithm is published in **four forms**: Python reference, R reference, language-agnostic pseudocode, and formal HUF-STD-002 specification. A skeptical user can re-implement from the pseudocode in any language and verify byte-identically against the published code via `content_sha256` on the three canonical reference inputs (Backblaze, Planck CMB, SM neutrino — all converging at IEEE float64 floor, `max_residual = 4.44 × 10⁻¹⁶`). See [`TRUST_AND_VERIFICATION.md`](TRUST_AND_VERIFICATION.md) for the 7-step verification protocol. *Trust is earned, not expected.*

---

## What's in this repository

```
higgins-decomposition/
├── HS_FAST_REFRESH.json          single-file AI loader
├── HS_FAST_REFRESH.md            companion narrative
├── PUBLICATION_READY.md          this file
├── OPERATIONS_PROTOCOL.md        Gawande-style transition checklists
├── README.md                     repo landing
│
├── HCI-CNT/                      canonical compositional engine (Tier 2)
│   ├── engine/
│   │   ├── cnt.py                Python reference (v2.0.4)
│   │   ├── cnt.R                 R port (parity-tested)
│   │   └── tests/                first-principles + determinism + corpus
│   ├── handbook/
│   │   ├── VOLUME_1_THEORY_AND_MATHEMATICS.md
│   │   ├── VOLUME_2_PRACTITIONER_AND_OPERATIONS.md
│   │   ├── VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md
│   │   ├── VOLUME_4_QUATERNION_VIEW.md
│   │   ├── GLOSSARY.md           narrative vocabulary
│   │   ├── NOTATION_AND_TERMINOLOGY.md   canonical locked vocabulary
│   │   └── ORIGIN_DADC_LINEAGE.md
│   ├── atlas/                    Stage 1/2/3/4 plate generators
│   ├── conference_demo/          CodaWork 2026 talk + extended results
│   └── experiments/              25 reproducible runs across 18 domains
│
├── HCI-CNQ/                      quaternion-native engine (Tier 3, sibling)
│   ├── engine/
│   │   ├── cnq.py                Python reference (v1.0.0)
│   │   ├── cnq.R                 R port (parity contract)
│   │   ├── geometry.py           Aitchison + Helmert + quaternion primitives
│   │   ├── cnt_adapter.py        portable bridge to cnt.py
│   │   ├── hashing.py            canonical-JSON SHA-256 contract
│   │   ├── CNQ_PSEUDOCODE.md     language-agnostic algorithm
│   │   ├── CNQ_SCHEMA.md         JSON output schema
│   │   └── tests/                43 tests — first-principles + dimension policy + determinism
│   ├── scripts/
│   │   ├── run_all_confirmations.py       one-command reproduction
│   │   └── verify_publication_results.py  strict observed-vs-expected gate
│   ├── results/
│   │   └── expected_results.json          locked expected values
│   ├── experiments/
│   │   ├── backblaze_fleet_quaternion/    drive failure D=4 confirmation
│   │   ├── planck_cmb_quaternion/         CMB photon power D=4 confirmation
│   │   └── sm_neutrino_quaternion/        SM neutrino D=3 boundary support
│   ├── STATUS_AND_MATURITY.md             4-bin maturity ladder
│   ├── CLAIM_STRENGTH_TABLE.md            locked language for claims
│   ├── CNQ_SCOPE_AND_LIMITS.md            what CNQ is and is not
│   ├── ROUND3_VALIDATION_PLAN.md          INV-022 plan
│   ├── HCI_DYADIC_COUPLING_LADDER.md      INV-028 (DEFERRED)
│   └── CNQ_BIQUATERNION_FACTORING.md      INV-029 (DEFERRED, twin-quaternion)
│
├── HCI-AUDIO/                    applied tier — 4-way psychoacoustic loudspeaker doctrine
├── HCI-ULTRASOUND/               applied tier — geometry-lock-probe doctrine
├── HCI/                          foundation vocabulary + calibration
│
├── ai-refresh/                   AI session loaders + protocols + admin
│   ├── CCTT_RUNBOOK.md           7-phase reproduction protocol
│   ├── CCTT_BUILD_INSTRUCTION_v1.0.json
│   ├── INVESTIGATION_CATALOG.json + .md   29 classified investigations
│   ├── HS_ADMIN.json
│   └── AI_REFRESH_*.md           per-push narratives
│
├── papers/                       Paper 1 (INV-026), Paper 2 (INV-027) drafts
└── RWA/                          mirror of Rogue Wave Audio repo (origin lineage)
```

---

## Get started in two commands

After cloning the repository:

```bash
# 1. Reproduce all three IEEE-floor confirmations
python HCI-CNQ/scripts/run_all_confirmations.py --repo-root .

# 2. Verify your run against the locked expected values
python HCI-CNQ/scripts/verify_publication_results.py --repo-root .
```

Expected output (verifier exits 0):

```
[backblaze_fleet_quaternion] PASS
[planck_cmb_quaternion]      PASS
[sm_neutrino_quaternion]     PASS
ALL EXPERIMENTS VERIFIED — publication-ready
```

The Planck CMB run reproduces `max_residual = 4.440892098500626e-16` to the last digit on Linux x86_64 / Python 3.10 / numpy. The same value is reproduced on Backblaze. Bit-identical residual on two physically unrelated D=4 datasets is the load-bearing evidence.

---

## Use the engines directly

### Python — CNT on your own CSV

```bash
python HCI-CNT/engine/cnt.py your_data.csv -o your_output.json
```

### Python — CNQ on a CNT JSON

```bash
python HCI-CNQ/engine/cnq.py --cnt-json your_output.json --out cnq_view.json
```

### R — same operations

```bash
Rscript HCI-CNT/engine/cnt.R your_data.csv your_output.json
Rscript HCI-CNQ/engine/cnq.R --cnt-json your_output.json --out cnq_view.json
```

### AI assistant — full reproduction protocol

```
Read ai-refresh/CCTT_RUNBOOK.md, then walk the seven phases.
Phase 2 (confirmation gate) and Phase 6 (four-check gate) require
explicit human approval; all other phases run automatically.
```

---

## What the system computes

CNT decomposes a compositional time-series (any number of carriers D, any length T) into four channels:

| Channel | Symbol | Meaning |
|---|---|---|
| Bearing | θ | atan2-stable angular direction in ILR space |
| Angular velocity | ω | per-step rotation rate |
| Steering metric tensor | κᴴˢ | order-2 Aitchison pullback metric — full off-diagonal Fisher information |
| Helmsman | σ | signed handedness of the rotation channel |

CNQ takes the same trajectory and computes the quaternion-native view: per-step rotation quaternion, sandwich-product reconstruction, residual, gate pass/fail, captured-energy fraction, and a hash-chained `cnq_content_sha256` linked to the parent CNT run.

For D=4 trajectories specifically, the quaternion sandwich product reproduces the Aitchison rotation **exactly** to floating-point precision — across physically unrelated datasets. This is the load-bearing result of Paper 1.

---

## Key results

**Three IEEE-floor confirmations.** Backblaze fleet (drive failures, D=4, T=731), Planck 2018 CMB photon power (cosmology, D=4, T=2499), SM 3-flavour numu oscillation (particle physics, D=3, T=1000). Max residual `4.441e-16` on the two D=4 cases (bit-identical to the last digit). Metric-involution residual at machine epsilon on all three.

**The signature.** LIMIT_CYCLE_P2 — period-2 termination of the CNT depth-tower return map — appears at IEEE floor on all three datasets. Together with the structural invariances (SO(D-1), SU(2), M²=I), this is the *Universal Compositional Invariance Signature* described in Paper 1.

**Cross-platform reproduction.** The CNQ engine is deterministic by design. Two runs on the same input produce identical `cnq_content_sha256`. Different platforms running cnq.py against the same CNT JSON should produce bit-identical hashes. Hash drift is a finding to file as a GitHub issue, not a failure.

---

## What CNT and CNQ do NOT claim

- **Not** a universal physical law that applies to arbitrary systems. The signature is universal *for compositional dynamics that meet the structural preconditions* — flow-directional, positive carriers, three structural invariances at the floor.
- **Not** a finished general theory at every dimension. D=4 is load-bearing. D=3 is consistency support. D=8 is a deferred algebraic extension (twin-quaternion factoring, INV-029). D≥5 (not 8) is a projection diagnostic.
- **Not** a replacement for standard CoDa methods. Hs adds verification and metrology-grade reproducibility on top of Aitchison geometry; it does not supersede the CoDa toolkit.
- **Not** finished — Round 3 corpus validation (INV-022) is the next milestone, and the catalog has 7 OPEN + 12 DEFERRED investigations awaiting their gates.

See [`HCI-CNQ/CLAIM_STRENGTH_TABLE.md`](HCI-CNQ/CLAIM_STRENGTH_TABLE.md) for the locked claim-strength taxonomy.

---

## Reproducibility contract

Every CNT JSON carries a `diagnostics.content_sha256` computed over the canonical-JSON serialisation of the output (after stripping clock-dependent fields). Every CNQ JSON carries:

1. `provenance.parent_cnt_content_sha256` — the parent CNT hash (provenance chain)
2. `cnq_content_sha256` — its own canonical hash
3. `provenance.source_file_sha256` — the input CSV's bytes hash

Three hashes per CNQ run. Anyone can verify the full chain end-to-end. The determinism contract is what makes cross-platform reproduction meaningful.

---

## Citation

Until the paper has an arXiv ID, cite the repository:

```
Higgins, P. (2026). Higgins Decomposition (Hs): a deterministic compositional
inference instrument with quaternion-native verification layer.
github.com/PeterHiggins19/higgins-decomposition,
release tag v3.0.0-paper1 (planned).
```

After Paper 1 is on arXiv, cite the paper as the primary reference and the repository as the reproduction artefact.

---

## Lineage

The compositional mathematics here originated in loudspeaker work at the Binaural Test Lab — specifically DADC (Dimension-Apportioned Diffraction Correction), where a fixed 6.02 dB diffraction budget had to be apportioned across cabinet dimensions. The arc:

```
DADC (loudspeakers, BTL)
    → H₁ (Higgins Operator on Hilbert space, 2026-02)
    → HUF (Higgins Unity Framework — governance, EITT, theory)
    → Hs (this repo — deterministic inference instrument)
        → CNT (canonical engine)
        → CNQ (quaternion-native verification layer)
```

Full narrative: [`HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md). The companion HUF repository is at [github.com/PeterHiggins19/Higgins-Unity-Framework](https://github.com/PeterHiggins19/Higgins-Unity-Framework).

---

## Cross-platform reproduction challenge — open invitation

If you are an AI platform, a third-party reviewer, or a curious researcher: **clone this repo, run cnq.py (or cnq.R) against the shipped CNT JSONs, and produce your own `cnq_content_sha256`**. Bit-identical hashes across platforms = a fourth independent confirmation channel beyond the three load-bearing datasets.

Reference observations (Linux x86_64 / Python 3.10) are recorded in [`HCI-CNQ/results/expected_results.json`](HCI-CNQ/results/expected_results.json). Hash drift is welcomed as a finding — file a GitHub issue with platform details.

---

## Help, free, on request

Free to use, help available. If you have a compositional dataset and want to know whether CNT or CNQ fits, open a GitHub issue, find Peter at a conference, or use the contact below. The framework is open. The methodology is reproducible. The receipts are in the hashes.

---

## Contact

- Peter Higgins — `peterhiggins2016@gmail.com` (personal) / `PeterHiggins@RogueWaveAudio.com` (business)
- Rogue Wave Audio / Binaural Test Lab — Markham, Ontario, Canada
- Companion governance repo: [github.com/PeterHiggins19/Higgins-Unity-Framework](https://github.com/PeterHiggins19/Higgins-Unity-Framework)

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*

*The simplex is the simplex regardless of what lives on it.*


---

## Addendum — 2026-06-09 (post-publication advancement)

*Non-destructive note (Cowork working tree; not yet git-committed). The content above is unchanged and remains valid as published.*

A second worked application (geology) and a staged, off-repo outreach package now exist; pitch language stays at 'interest expressed', and all claim tiers are preserved.

Since publication the system advanced: Hs/CNT/CNQ was applied to **mudstone chemostratigraphy** as a cited, reproducible demo on real PANGAEA data (`collaborations/geology-wehner/`), and a new concept — **CNQ tiling / "faceted read"** (overlapping exact D=4 charts glued on shared parts reconstruct the full higher-dimensional compositional move **losslessly**: alignment 9e-16, reconstruction 4e-14, overlap proven necessary) — was tested. **Engine, schemas, and canonical numbers are UNCHANGED**; this is a documentation / application / concept advance. Gluing maths CONFIRMED; scientific value on real high-D data TO TEST. Full current picture: `collaborations/geology-wehner/00_EXECUTIVE_OVERVIEW.md`.
