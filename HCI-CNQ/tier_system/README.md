# CNQ tier — overview (canonical)

**Status:** live tier in the Hs system since 2026-05-07 (push #23).
**Parent:** [`HCI-CNQ/`](..) — see the [top-level README](../README.md) for the demonstration-first framing and how the family of tools (CoDa + CNT + CNQ + HCI) compose.
**Foundation:** three IEEE-floor confirmations. See [`../experiments/backblaze_fleet_quaternion/QD_ROUND_2_REPORT.md`](../experiments/backblaze_fleet_quaternion/QD_ROUND_2_REPORT.md), [`../experiments/planck_cmb_quaternion/QD_ROUND_2_5_REPORT.md`](../experiments/planck_cmb_quaternion/QD_ROUND_2_5_REPORT.md), and [`../experiments/sm_neutrino_quaternion/`](../experiments/sm_neutrino_quaternion/). Concept 1 passes at IEEE floor (4.441 × 10⁻¹⁶) on three independent datasets — drive failures, cosmic microwave background, Standard-Model neutrino oscillation — bit-identically. The quaternion identification is **not analogy** — it is what CNT has been computing all along, named in the algebra it natively belongs to.

---

## The central claim of the QD project

> **CNT measures invariance.**
> **CNQ names the algebra that invariance lives in.**

Tensor calculus exists because invariance under coordinate change is the defining property of a tensor. The same correspondence applies up the symmetry-group ladder: invariance under 3D rotation + handedness + time reversal is the defining property of a **quaternion**. Compositional dynamics on the D=4 simplex carries exactly those three invariances, simultaneously and at IEEE-floor precision. CNT measures them by detecting LIMIT_CYCLE_P2 universally across substantively-flowing compositional data; CNQ names the algebra in which all three invariances are unified — quaternions for D=4, biquaternions for D=8, Clifford Cl(D−1) for arbitrary D.

Full statement: [`../doctrine/CENTRAL_CLAIM.md`](../doctrine/CENTRAL_CLAIM.md).

---

## What CNQ is

CNQ — **C**ompositional **N**avigation **Q**uaternion — is the proposed high-performance tier of compositional analytics for the Hs system. It uses quaternion algebra natively for trajectory representation, evolution, and cross-dataset comparison. It targets dimensionally larger systems than CNT was designed for: climate modeling, multi-country economic flows, large-scale industrial composition, multi-trajectory bundles where the cross-dataset structure is the primary observable.

CNQ does not replace CNT. CNT continues as the field-use, medium-scale tier. CNQ is what comes *above* CNT for problems where:

- D ≥ 8 (multiple bi-quaternion or higher-Clifford structure becomes the natural decomposition)
- T is large (smooth interpolation between timesteps benefits from SLERP, not linear)
- Cross-dataset is primary (Hamilton products replace bespoke Stage 4 logic)
- The user community already speaks quaternion (robotics, graphics, physics, quantum information)

---

## The tiered system: CoDa → CNT → CNQ

The Hs project now has a three-tier compositional analytics stack:

| Tier | Role | Scale | Use case |
|---|---|---|---|
| **CoDa** | Grounded operational functions | Data collection + sorting | Foundational layer — Aitchison closure, CLR, ILR, balance dendrograms, all the established CoDa-community methods |
| **CNT** | Trajectory navigation tensor | Field use, small-to-medium | Most current corpus experiments (D=2-10, T=10-1000); single-trajectory and small-bundle analysis |
| **CNQ** | Quaternion-native large-scale analytics | High performance, dimensionally larger | Climate modeling, multi-country economic flows, large industrial composition; multi-trajectory bundles where structure dominates |

Full tiered-system explanation: [`CNQ_TIERED_SYSTEM.md`](CNQ_TIERED_SYSTEM.md).

---

## Documents in this folder

| File | Purpose |
|---|---|
| [`README.md`](README.md) | This file — what CNQ is, how the tiers compose |
| [`CNQ_TIERED_SYSTEM.md`](CNQ_TIERED_SYSTEM.md) | The CoDa → CNT → CNQ tier explanation in detail |
| [`CNQ_VS_CODA_VS_CNT_COMPARE.md`](CNQ_VS_CODA_VS_CNT_COMPARE.md) | Updated comparison table — three columns now, CNQ added to the existing CoDa-vs-CNT balance paper |
| [`CNQ_ROI_AND_USE_CASES.md`](CNQ_ROI_AND_USE_CASES.md) | When does CNQ make sense — break-even vs CNT, decision rules, target use cases |
| [`CNQ_ENGINE_PROPOSAL.md`](CNQ_ENGINE_PROPOSAL.md) | Proposed engine specification for CNQ — quaternion-native operations, CNT-compatibility layer, hash-chain provenance, integration plan |

---

## Status

The **CNQ tier is live and canonical** as of push #23 (2026-05-07). Doctrine, three reproducible IEEE-floor demonstrations, comparison with CoDa and CNT, and the engineering proposal all live in the public repo at `Hs/HCI-CNQ/`. The compiled `cnq.py` engine is still proposed; see [`CNQ_ENGINE_PROPOSAL.md`](CNQ_ENGINE_PROPOSAL.md) for the ~14-day implementation plan. Until that lands, the experiments under [`../experiments/`](../experiments/) are the working demonstrations and the CNT engine produces the underlying compositional data.

Roadmap:
- **Round 3 — full-corpus quaternion-view validation.** Reanalyse the 25-experiment CNT corpus as quaternion-view, reproducing every CNT content_sha256 and demonstrating at least one CNQ-only diagnostic. Promotes the tier from "live with three demonstrations" to "live with corpus-grade validation."
- **`cnq.py` engine implementation.** Quaternion-native sibling to `cnt.py`, producing a parallel `cnq_content_sha256` as a second independent verification path. ~14 days per the engineering proposal.
- **Real-data particle-physics verification.** Round 2.6 used the SM PMNS prediction; the next-tier test uses measured T2K/NOvA event data and asks whether measurement matches prediction at the invariance level.

---

## Why "the connection is real" matters

Round 2 confirmed the foundational quaternion identification at IEEE floor on real corpus data. That moves CNQ out of "interesting speculation" into "engineering specification waiting to be implemented." Every operation in CNT has a quaternion-native counterpart that will compute the same numerical result; what changes is which operations become easier to express and which adjacent communities can immediately recognize what we're doing.

For Peter, after CodaWork 2026, this is the next horizon: not a fix to CNT (CNT works), but a successor tier for problems CNT was never sized to solve. Climate models. Multi-decade economic flows. Industrial process composition with hundreds of components. Cross-system inference at scale. The quaternion view scales naturally where channel-by-channel arithmetic doesn't.

For the broader research community, CNQ is the bridge: compositional analysis becomes recognisable to physicists (SU(2) is qubit algebra), roboticists (quaternions are SLAM trajectories), and computer graphics engineers (quaternions are everywhere in animation). The CodaWork audience hears about CNT; the post-CodaWork audience hears about CNQ, and they don't need a translator.

---

*The instrument reads. The expert decides. The hashes carry the receipts. CNQ is what comes next.*
