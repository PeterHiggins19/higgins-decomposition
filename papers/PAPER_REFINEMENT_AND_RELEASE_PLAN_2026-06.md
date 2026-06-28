# Paper refinement, revised tests, and the staged-release plan — under the new engine

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. One plan
covering three things Peter asked for: (1) what the **new engine** changes for each paper + its **revised test
status**; (2) the **staged release** that walks readers from the foundation up to the application reveals (the
existing work gets a head start; applications follow with demonstration); (3) the **get-involved kit** — every
paper tied to its tools, data, tests, and receipts at full depth. P1 is tested the most (done; see its
RESULTS). Honest-broker tiered; nothing posted; Peter is the sole gate.*

---

## 1. Per-paper refinement + revised test status

| paper | new-engine delta | revised test | status / receipt |
|---|---|---|---|
| **P1** Tiling the Simplex | none material (uses adjoint SO(3)); re-receipted under HS-GOLD-1; **add: name the direct solver** for the 10⁶ residual | **full re-validation** (T1–T5) | ✅ `99ec0581` — `experiments/p1_revalidation_2026-06/` |
| **P2** Deceptive-drift detector | unchanged; the blindness-suite frames it (ratio-blind) | re-run null on EMBER | needs a defensible null (open) |
| **P3** Deterministic instrument (tool) | **gains** the generator↔reader codec + HS-GOLD-1 as the conformance exhibit | conformance = HS-GOLD-1 `--verify` | ✅ master `d7ac6530` |
| **P4** Compositional kinematics | unchanged; the dual-quaternion 6-DOF is a *forward pointer* (SE(3) reading) | re-run kinematic tower self-test | green (prior) |
| **P5** Character Space (Hˢ²) | the self-read (`SELF_NAVIGATION_READ`) is a new worked instance | re-run CCS battery | ✅ prior CCS |
| **P6** Compositional finance | unchanged | re-run S&P + time-permutation null | green (prior) |
| **P7** Foundations (coda) | **gains** the SO(n)/Hurwitz boundary (`HOW_FAR_THE_MATH_GOES`, `THE_LADDER_AND_THE_BREAK`) as the negative-result spine | assembled last | seed |
| **P8** CMP (the message) | unchanged; W-I/W-II/W-III are its witnesses | re-run Crohn + HIV | ✅ `acf65ce…` |
| **W-I/II/III** witnesses | **gain** rotation-blind (W-III) from the SO(4) Backblaze run | re-receipt each | ✅ measured |
| **Capstone** constellation | **gains** the 6-DOF + blindness suite + the QAM/codec/denoise application stack | storm-backtest (the decisive test) | T2/T3, named |

**New engine-era artifacts now available to cite (all T1, receipted):** SO(n) generator (`8107b173`),
HS-GOLD-1 (`d7ac6530`), common-mode 313 dB (`d8c21c70`), deterministic denoise (`cb0c3f52`), compression
(`305cc0db`), QAM sandbox (`f502c15d`), self-read (`120bb621`).

## 2. The staged release — training up to the reveals

The point of sequencing is a **smooth transition of advancement**: each release teaches what the next needs,
so by the time the application reveals land, the audience already holds the foundation. Existing foundation
work goes first (head start); applications follow with demonstration-by-example.

```
  WAVE 1 — FOUNDATION (the math everyone cites)        head start; teaches the exact rung + tiling
     P1 (tiling, tested most) ─► P3 (the deterministic instrument + HS-GOLD-1 conformance)
                                   │
  WAVE 2 — THE READING (what the instrument says)      teaches motion + character + the message
     P4 (kinematics) ─► P5 (character space / Hˢ²) ─► P8 (the compositional message + W-I/II/III)
                                   │
  WAVE 3 — THE BOUNDARY (what it cannot do)             teaches honesty: where it stops
     P2 (deceptive-drift null) ─► P7 (foundations: Hurwitz/SO(n) limits, negative results first-class)
                                   │
  WAVE 4 — THE APPLICATIONS (the reveals)              demonstration by example: the payoff
     P6 (finance) ─► the Capstone (constellation) ─► the application notes (AN-001…005:
     noise rejection · fleet · telemetry codec · sensor-array conductor · unitary constellation)
```

Each wave only releases when its gate is met (review + Peter's decision); the order means no reader meets a
claim before the foundation that justifies it. The **reveals (Wave 4)** are deliberately last so the existing
work has time to land and be reproduced first.

## 3. The get-involved kit — every paper, reproducible to full depth

Anyone can pick their altitude: read → run → verify → extend. The chain for each paper:

```
   PAPER (claim) ─► EXPERIMENT (script) ─► DATA (public, cited) ─► RECEIPT (SHA-256) ─► CONFORMANCE (HS-GOLD-1)
```

| level of involvement | what you touch | entry point |
|---|---|---|
| **Read** | the handout / datasheet | `IS_Hs_RIGHT_FOR_YOU.md`, `papers/datasheets/` |
| **Run** | one script, one public dataset | the `experiments/*/` folder named in each paper |
| **Verify** | reproduce the headline hash | `experiments/conformance_fixtures_2026-06/hs_gold_fixtures.py --verify` |
| **Extend** | the open determinism contract + the generator | `son_exact_generator.py`, the four-form port |
| **Full depth** | the whole tools/apps/data/test chain | this plan + the `experiments/` index + `library/` |

**Kit contents already on hand:** the engine + guards; the SO(n) generator (data factory); HS-GOLD-1 (the
known-hash standard); the codec + denoise + common-mode demos; the QAM simulator; the interactive front doors
(`COMPOSITION_GAUGE.html`, the financial projector); the replication notebook + R port + pseudocode; the public
datasets (energy/fleet/microbiome/geochem) read-but-never-claimed. Every number traces to a script and a hash.

## 4. Tiers & governance

- **T1:** the P1 re-validation and all engine-era receipts above.
- **T2:** the release sequencing and the kit architecture (reasoned; adjust as reviews land).
- **T3:** application reveals (Wave 4) — claimed only with their decisive receipts (storm-backtest, etc.).
- Off-repo arXiv full papers stay off the public repo (abstracts only); Peter is the sole gate; nothing posted.

*Cross-refs: `ABSTRACT_LEDGER.md`, `PUBLICATION_STAGING_AND_REVIEW_PLAN.md`, `COLLECTIVE_REVIEW_PACKAGE_2026-06-22.md`,
`frontier/HS_ENGINE_MORPHOLOGY_AND_CODEC.md`, `datasheets/README.md`, `../experiments/p1_revalidation_2026-06/`.
Proof & Honesty Standard throughout. Peter is the sole gate.*
