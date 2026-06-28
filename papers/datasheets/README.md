# HS-CN1 datasheets & application notes — manufacturer-grade documentation

*The instrument documented the way an aerospace-component maker documents a part: **backwards from measured
results**, every spec citing a receipted experiment, tiered for honesty, so any reader can choose their level
of involvement and still get the best. Author: Peter Higgins (human authorship for all claims); AI-assisted
per HUF-STD-001. Nothing posted; Peter is the sole gate.*

---

## The set

| doc | what it is | status |
|---|---|---|
| [`HS-CN1_DATASHEET.md`](HS-CN1_DATASHEET.md) | the component datasheet — features, abs-max/operating boundaries, measured characteristics table, block diagram, conformance (HS-GOLD-1), tiers | **Rev A** |
| [`AN-001_DETERMINISTIC_NOISE_REJECTION.md`](AN-001_DETERMINISTIC_NOISE_REJECTION.md) | theory of operation + design equations + suggested circuit + pseudocode + application examples + honest limits for the common-mode + additive noise front-end | **Rev A** |

## Suggested application notes (named; built on demand, deterministic-only)

- **AN-002** — Fleet pre-fault monitor (the blindness suite on a constellation/drive fleet).
- **AN-003** — Telemetry source-coder / codec for a QAM space link (the error-graceful ILR layer).
- **AN-004** — Sensor-array conductor (multi-expert fusion; common-mode cancel + coherence gate).
- **AN-005** — Non-coherent unitary (rotation) constellation from the SO(n) generator.

## The documentation discipline (why these are trustworthy)

1. **Backwards-built.** Make the product (the receipted experiment), *then* document it. Every number in a
   datasheet maps to a `experiments/…` script and a SHA-256.
2. **Tiered.** T1 measured · T2 reasoned · T3 to-earn / rejected. No spec is stated above its evidence.
3. **Traceable.** HS-EPS-1 determinism contract; HS-GOLD-1 conformance (master `d7ac6530…`); a build is genuine
   only if it reproduces the golden hashes.
4. **Honest limits are first-class.** The "absolute maximum" section says where the instrument refuses or
   returns NO — because a deterministic part's value is that it can be tested and answer yes/no.
5. **Governed.** Instrument-not-data; operator is the sole gate; full automation never possible; safety dominant.

## Simplified (handout) vs industrial

The conference **handout** is the one-page front door. These datasheets are the **industrial** layer beneath
it — same facts, manufacturer depth. A reader picks the altitude: handout → datasheet → application note →
the receipted experiment → the open code. Never less than the best at any level.

*Cross-refs: `../frontier/HS_ENGINE_MORPHOLOGY_AND_CODEC.md` (the engine the parts come from),
`../../experiments/conformance_fixtures_2026-06/` (HS-GOLD-1), `../../IS_Hs_RIGHT_FOR_YOU.md` (the front door).
Proof & Honesty Standard applies throughout. Peter is the sole gate.*
