# CN‑TT: a deterministic, hash‑chained engine for compositional navigation

**Scaffold — 2026-06-10. For HUF AI Collective review. Tool/software paper (e.g., JOSS / SoftwareX). Gate before submission: the v4 engine reaches navigation parity with the frozen oracle (engine build phase P2).**
**Author:** Peter Higgins. Human authorship for all claims; AI‑assisted per HUF‑STD‑001.

---

## Summary (draft)

CN‑TT (HCI‑CNTT v4) is an open, deterministic engine for compositional‑navigation analysis: it reads the geometric and dynamic structure of compositional time series in Aitchison geometry, tiles high‑dimensional compositions with exact four‑part quaternion charts (P1), and emits a canonical, hash‑chained record. Its distinguishing properties are **determinism** (same input → same output, bit‑for‑bit; no statistics in the science path) and **auditability** (a SHA‑256 content hash at every pipeline link), which make analyses reproducible and verifiable — properties most high‑dimensional compositional tooling does not guarantee.

## 1 · Statement of need (incl. CoDaWork mention)
- High‑dimensional compositional analysis commonly relies on statistical/lossy reduction that is not bit‑reproducible. Need: a deterministic, auditable engine.
- **CoDaWork 2026 mention (one line):** the method this engine implements was presented at CoDaWork 2026; the high‑dimensional tiling capability (P1) is the follow‑on the conference inspired.

## 1b · Related work — how CN‑TT differs from existing CoDa software *(Grok K‑2, 2026‑06‑15)*

The compositional‑data community is well served by mature R packages, and CN‑TT does **not** claim novelty in the log‑ratio transformations themselves. The major tools each have a clear focus: **`compositions`** (van den Boogaart & Tolosana‑Delgado) is the most comprehensive general‑purpose package and the closest in scope; **`robCompositions`** emphasizes robustness to outliers and imputation under contamination; **`zCompositions`** specializes in zero and missing‑value treatment; **`easyCODA`** targets applied CoDa workflows and visualization. These tools assume the user will handle numerical stability, provenance, and the judgement of *when not to trust an output*.

CN‑TT's contribution is a **combination of guarantees** treated as first‑class, verifiable features rather than left to the user: *deterministic, cross‑platform value‑identity with a conformance hash*; an *explicit guard layer* (resolvability `HM‑NUL`/`HM‑TIE`, rank `DG‑RNK`, carrier guard `E‑21`, discovered‑floor hold‑lock) that **withholds or warns when the evidence is insufficient** rather than emitting a confident‑wrong reading; and *full traceability* (a content hash + engine version + input receipts on every output). The honest statement:

> *CN‑TT provides a deterministic, cross‑platform value‑identical compositional engine with an explicit guard layer and full traceability. This combination of guarantees is not present as a core design principle in the major existing CoDa packages (`compositions`, `robCompositions`, `zCompositions`, `easyCODA`).*

This is a differentiation of *engineering guarantees*, not a claim that the existing packages are unreliable — they simply do not prioritize the same deterministic, withholding, hash‑receipted contract. (The kinematics layer of P4 is a further additive synthesis on top of this engine.)

## 2 · Functionality
- The four‑link Tensor‑Train pipeline (HUF‑STD‑002): ingest+treat → geometry (closure/CLR/Helmert‑ILR/radial) → tile/atlas (sliding + hierarchical; lossless reconstruction) → navigate+emit (the navigation family + content hash).
- Navigation outputs: helmsman/handedness, bearing (atan2‑stable), angular velocity, K_eff, total variation, Aitchison norm/distance, concentration‑regime tagging, attractor fit, lock/degeneracy diagnostics, ILR‑PCA barycenter trajectory.
- Zero‑treatment adapter (multiplicative replacement) upstream of the engine.

## 3 · Design for reproducibility and portability
- Determinism guarantee; canonical hashing; embedded engine/schema version triple; environment metadata.
- Port‑ready kernel (numpy‑only geometry/quaternion/provenance; the sparse solver behind a single interface seam for a future compiled/flight backend).
- Frozen‑oracle parity discipline: v4 is accepted only when it reproduces the prior engine (v3.2.0/v2.0.0) and the full experiment corpus to ≤1e‑12 (Tier‑A), with the documented improvements (atan2 angle; lossless D>4; zero‑treatment) recorded as such.

## 4 · Validation
- Self‑test (BIST) reproduces the tiling proof numbers from inside the engine (quaternion exactness 2.7e‑15; lossless reconstruction ~1e‑13; D=16‑from‑D=4 1.3e‑15; tree atlas 3.8e‑13 at D=10⁵; determinism: identical content hash on rerun).
- Cross‑domain demonstrations (validation, not claims): the engine recovers known/plausible structure across the experiment corpus (energy, geochemistry, nuclear, cosmology) — evidence the instrument behaves, with no over‑claimed "discoveries."
- **A worked self‑limitation (the honest‑broker design, demonstrated):** a CHSH‑form carrier‑coupling diagnostic (`hs_carrier_coupling.py`) reads pairwise carrier coordination in the algebraic form of the Bell/CHSH statistic. Compositional data are classical, so this statistic is *bounded by 2* (the local‑hidden‑variable bound) and can never reach the quantum Tsirelson bound (≈2.828). Run deterministically on real energy mixes, the bound is **respected in every case** (e.g. the world grid's renewables read as a maximally co‑moving bloc at exactly 2.0; no case exceeds 2) — a reproducible, hash‑receipted experiment whose *result is the kill‑test passing.* This is offered not as a finding but as **evidence of the engine's character**: handed an over‑claimable idea (entanglement on classical data), the instrument computes the honest answer and refuses to manufacture a violation. The experiment is journaled as completed in the repository and reproducible from the module; the idea has prior lineage in the investigation catalog (INV‑015) and the QIT knowledge base, here implemented deterministically. *(Tier 3 — explicitly NOT quantum entanglement; see `../../Hs-Kinematics/H1_STEP5_ENTANGLED_CARRIER_CLOSURE.md`.)*

## 5 · Honest scope
- This is an engineering/reproducibility contribution, not a novel‑result paper. It deliberately excludes the speculative pattern‑matches set aside in `papers/FINDINGS_INVENTORY_2026-06-10.md`.

## 6 · Availability
- Repository, license (Apache‑2.0 for code), reproducible experiments, and self‑test receipts.

## Acknowledgments
[Shared HUF AI Collective block — see `00_SUITE_README.md`.]

## References (seed)
Aitchison 1986; Egozcue et al. 2003; HUF‑STD‑002 (Tensor Train); the P1 methods paper; standard reproducibility/software‑paper venue guidelines (JOSS).
