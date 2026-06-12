# CN‑TT v4 — Chain Completeness Map (input → output, and beyond)

*Synthesis, 2026-06-10. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Answers: across all proposals, all past experiments, and all agenda plans, what else must be implemented to make CN‑TT a complete working input→output chain that does every desired task — and stays open to the not‑yet‑imagined? Ties together `CNTT_V4_ENGINE_DESIGN.md`, `ENGINE_INTEROP_REGISTRY.md`, `HCI-CNTT/CONTROL_POINTS_AND_REMOTE_ADAPTATION.md`, and the flight spec suite.*

---

## 0 · How to read this

Two jobs complete the chain, and it's honest to keep them separate:

- **(A) Port‑forward** — the *oracle* (`cnt.py`/`cnq.py` + its tree) is already a fuller chain than the v4 kernel. v4 must bring those pieces into the tile‑native architecture. These get the chain to oracle‑equivalence.
- **(B) New layers** — capabilities the desired tasks (real‑time geosensing, flight, monitoring, cross‑platform remote) and the unimagined ones need, that the oracle never had.

Legend: ✅ built · 📝 specced, not built · ⬆️ port from oracle · 🆕 new gap (not in any plan yet).

> **Build progress 2026-06-10 (`HCI-CNTT/MODULAR_ARCHITECTURE.md`):** the engine was made **modular** — every processing section is now a uniform `Stage` (adaptability unit + test point + hash‑cacheable). **Built & self‑test‑green:** the Stage/Pipeline framework, the **cross‑platform determinism contract** (item §2.3 — done), hash‑keyed caching ("don't repeat history"), delta‑isolation, and the six sections adapt/treat/**calibrate**/geometry/atlas/**navigate (core family)**. So §1's calibration stage, the adapter contract (basic), the determinism contract, and the start of the L4 navigation‑parity layer are now built. Still pending as listed below.

---

## 1 · The chain, stage by stage

```
RAW → [L0 Adapt] → [L1 Ingest+Treat+Calibrate] → [L2 Geometry] → [L3 Tile/Atlas] → [L4 Navigate+Emit] → OUT → [Consumers]
        ⬆️/🆕            ✅/⬆️/🆕                     ✅            ✅                ✅(D4)/📝(parity)        ⬆️/🆕
```

| Stage | Status | What's there | What's missing (the suggestion) |
|---|---|---|---|
| **L0 Adapt** (domain raw → canonical composition) | ⬆️🆕 | oracle has many bespoke adapters (ember, backblaze, geochem, planck…) | **Unified adapter contract** — one deterministic interface `domain raw → (carriers, labels, matrix)` so new domains attach without touching the core. The Canada StatCan/CER loader and the 4 feasibility domains are the first adapters to write against it. |
| **L1 Ingest + Treat + Calibrate** | ✅⬆️🆕 | zero‑treatment built ✅; oracle has `standard_calibration` | **Calibration stage as a first‑class chain step** — recurring across experiments ("calibration mandatory": forensic soil, mudstone vs Matthew's sections, multi‑sensor). Map raw instrument readings → calibrated composition; gate outputs on calibration state. *(High — it appears in nearly every applied case and isn't yet a formal stage.)* |
| **L2 Geometry** | ✅ | closure/CLR/Helmert‑ILR/radial (kernel) | complete |
| **L3 Tile/Atlas** | ✅ | sliding + hierarchical + lossless reconstruction (kernel, proven) | complete |
| **L4 Navigate + Emit** | ✅(D4)/📝 | D=4 quaternion + radial built | **Navigation‑parity layer (P2)** — port the full family (helmsman, K_eff, regime, activation guard, attractor, lock/degeneracy, EITT, nav‑2D). The single biggest port. |
| **OUT (schema)** | ⬆️ | oracle has `CNT_V3_SCHEMA.md` | **`CNTT_V4_SCHEMA.md`** — pin the canonical output contract (incl. the `config` block from the control‑points work). |
| **Consumers** | ⬆️🆕 | oracle has the 16:9 projector + field guide; ground‑receiver flow specced | **Consumer/visualization layer** for v4 (connect the dashboard/projector pattern) + the **ground‑receiver resolver** (read hash → registry → interpret). |

---

## 2 · New layers the desired + unimagined tasks need (the heart of the question)

These are genuinely **not yet in any plan** and are what turn "a chain that runs a CSV" into "the instrument the agenda describes":

1. **🆕 Streaming / online mode.** Today the chain is batch (whole series). The real‑time front‑end thesis, the geosensing rover, and deceptive‑drift *monitoring* need an incremental mode: ingest one timestep, update state, emit, without recomputing the past. *High — it's the difference between an analysis script and a live instrument.*
2. **🆕 Input‑uncertainty propagation.** The chain is deterministic but assumes *exact* inputs; real instruments have measurement error. A deterministic propagation of input bounds → output bounds (error bars on helmsman/bearing/K_eff) completes it for actual hardware. *High, and absent from every plan.* (Distinct from EITT, which tests invariance, not input error.)
3. **🆕 Cross‑platform numerical‑determinism contract.** For the remote‑hash story to hold, the hash must be **identical on the rover and on the ground** — which requires fixed evaluation order and IEEE‑754 discipline so float results are bit‑identical across platforms. This is the Stage‑1 "cross‑platform reproduction" item, reframed as an engine contract. *High — the entire hash‑routing/registry value rests on it.*
4. **🆕 Smart‑downlink / reconstructable‑reduction emit mode.** For bandwidth‑limited remote, emit a prioritized, reconstructable, bounded subset (the reduction is already reversible — make it a deliberate output mode). *Medium (flight).*
5. **🆕 Change‑point / monitoring emit diagnostics.** Fold the deceptive‑drift detector (and its null model, open Q3) into L4 as a standing monitoring output — the P2 paper's method as a chain capability, not a one‑off script.
6. **🆕 Extension contracts — the answer to "not yet imagined."** Formalize the five edges so new capability attaches *without touching the locked core*: **adapter** (new domain in), **wrapper** (new domain interpretation out — the oracle's "interpretation lives in wrappers" principle), **version** (new engine via the interop registry), **control point** (bounded adaptation), **consumer** (new output sink). A chain that is *locked in the middle and contracted at the edges* is the structural definition of future‑proof. This is the single most important item for the unimagined.

---

## 3 · Cross‑cutting trust/ops (mostly specced; must be built to "complete")

- **📝 Parity harness (P3)** — certifies v4 = oracle *and* generates the interop transforms. Critical; everything downstream (registry, retiring the oracle) depends on it.
- **📝 Interop registry + resolver** — built from the harness; lets all engines read all engines (`ENGINE_INTEROP_REGISTRY.md`).
- **📝 Control‑point config layer + Coherence Supervisor/FDIR** — the bounded adaptation surface + the engine‑monitoring‑engine (`CONTROL_POINTS…md`, `CNTT_FLIGHT_CONTROL_SPEC.md`).
- **⬆️ Anti‑specification (failure‑mode enumeration) for v4** — the oracle has one; v4 needs `ANTI_SPECIFICATION.md`: what the chain does with degenerate, adversarial, or out‑of‑envelope input. *Directly serves "dealing with the unexpected."*
- **⬆️🆕 v4 test corpus + CI gate** — port the self‑test (done ✅) into a continuous regression corpus + CI so every change re‑certifies. (GitHub Actions already exists at the repo level.)
- **⬆️ Pipeline + verify tooling** — the oracle's `run_pipeline.py` / `verify_package.py` equivalents for v4.

---

## 4 · What is NOT needed (settle it, save the effort)

- **Native D=8/D=16 quaternion engine** — settled no (Hurwitz). Clifford/Spin(n) recorded as the only real "native" option, not built.
- **The `compute_stage3` ladder fix** — **moot for v4**: the tile‑native atlas replaces the materialized‑combinations path entirely. (Only mattered for the oracle.)
- **The differential‑geometry tower** (curvature/holonomy/Chern‑Simons/Berry/instanton) — stays out of the canonical chain until one invariant is earned on real data.
- **The transcendental‑constant findings** — out of the chain and the papers (per `FINDINGS_INVENTORY_2026-06-10.md`).

---

## 5 · Critical path (recommended order)

1. **P2 — navigation‑parity layer** (L4) → the chain *does what the oracle did*.
2. **P3 — parity harness** → certifies parity + emits the interop transforms (unlocks registry, oracle retirement, delta‑testing).
3. **Calibration stage + unified adapter contract** (L0/L1) → the chain *ingests real domains correctly* (Canada loader + the 4 feasibility domains are the first clients).
4. **Output schema + anti‑specification + CI corpus** → the chain is *contracted and self‑guarding*.
5. **Cross‑platform determinism contract + streaming mode** → the chain is *real‑time and remote‑trustworthy* (front‑end/geosensing/flight).
6. **Interop registry + control‑point config + Supervisor** → the chain is *adaptable, updatable, and delta‑testable*.
7. **Input‑uncertainty propagation + smart‑downlink + consumer layer** → the chain is *instrument‑grade end to end*.
8. **Formalize the extension contracts** → the chain is *open to the not‑yet‑imagined*.

Items 1–4 make it a complete, honest, oracle‑equivalent chain. Items 5–8 make it the instrument the agenda actually describes.

## 6 · Claim tiers
- **Tier 1 (verified):** the kernel stages (L2/L3, D=4) are built and proven; the oracle's fuller components exist and are the port source.
- **Tier 2 (sound engineering):** the gap analysis, the critical path, the extension‑contract framing.
- **Tier 3 (to build):** every 📝/⬆️/🆕 item above; the input‑uncertainty and cross‑platform‑determinism layers are the two highest‑value items absent from all prior plans.

*Locked in the middle, contracted at the edges. The instrument reads. The expert decides. The hashes carry the receipts.*
