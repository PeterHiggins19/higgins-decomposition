# Hˢ industrial manual suite — how to use it, why, and what's inside

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. The
manufacturer-grade manual set for the Hˢ compositional-navigation instrument: operating manual, theory of
operation (the internals as a documented state machine, flow-charted), use cases, and design concept. Built
backwards from receipted results, tiered for honesty, prepared for industrial use. Nothing posted; Peter is
the sole gate.*

---

## What Hˢ is (the one line that moves a busy user)

> **Hˢ is the only deterministic-*enforced*, hash-*receipted*, exact compositional instrument built for
> applications-on-applications.** If your data is parts of a conserved whole (a budget, a mix, a set of
> shares) and your decision must be *auditable* — re-run to the same answer on any machine — Hˢ is the tool
> whose entire design is that guarantee.

Most tools that read compositions are statistical and non-reproducible at the bit level. Hˢ inverts that: the
read is exact at the rung, deterministic by contract (same input → same output → same SHA-256), guarded so it
withholds rather than guesses, and governed so a human always holds the gate. **That is the differentiator —
not a feature, the foundation.**

## The suite

| manual | what it answers | status |
|---|---|---|
| [`HS_USER_MANUAL.md`](HS_USER_MANUAL.md) | *How do I use it, and why this one?* — quick start, modes, a worked example, the gate, governance | **Rev A** |
| [`HS_THEORY_OF_OPERATION.md`](HS_THEORY_OF_OPERATION.md) | *What happens inside, stage by stage?* — the engine as a documented **state machine**, flow-charted, with diagnostic codes and breakers | **Rev A** |
| [`HS_USE_CASES.md`](HS_USE_CASES.md) | *Where does it earn its keep?* — applications-on-applications, each tied to a receipt | **Rev A** |
| [`HS_DESIGN_CONCEPT.md`](HS_DESIGN_CONCEPT.md) | *Why is it built this way?* — the design concept and the application concept, lineage to the ground state | **Rev A** |
| [`../papers/datasheets/HS-CN1_DATASHEET.md`](../papers/datasheets/HS-CN1_DATASHEET.md) | the component spec sheet (characteristics, abs-max, conformance) | Rev A |
| [`../papers/datasheets/AN-001_DETERMINISTIC_NOISE_REJECTION.md`](../papers/datasheets/AN-001_DETERMINISTIC_NOISE_REJECTION.md) | application note: noise rejection front-end | Rev A |
| *planned:* AN-002 fleet · AN-003 telemetry codec · AN-004 sensor conductor · AN-005 unitary constellation | applications, built on demand | named |

## How to read this suite (pick your altitude)

```
   one line (above)  ─►  USER MANUAL  ─►  USE CASES  ─►  THEORY OF OPERATION  ─►  DATASHEET + AN  ─►  the code + receipts
   "should I?"            "how?"           "where?"        "what's inside?"         "the spec"          "prove it yourself"
```

A manager stops at the user manual; an integrator goes to the theory of operation and datasheet; a skeptic
runs the conformance check and reproduces the hash. **Never less than the best at any altitude.**

## The documentation discipline (why these are trustworthy)

1. **Backwards-built** — the product (a receipted experiment) exists first; the manual documents it. Every
   number cites a `experiments/…` script and a SHA-256.
2. **Tiered** — T1 measured · T2 reasoned · T3 to-earn/rejected. No claim above its evidence.
3. **Traceable** — HS-EPS-1 determinism contract; HS-GOLD-1 conformance (master `d7ac6530…`).
4. **Honest limits first-class** — every manual states where the instrument refuses or returns NO.
5. **Governed** — instrument-not-data; the operator is the sole gate; full automation is never possible.

## The helmsman swing (why this set exists now)

The instrument is essentially complete and measured; the open work that most changes its value before any push
is **not more capability — it is making the capability usable.** So the directing effort (the helmsman) swings
here: from *building* to *documenting for industrial use*. These manuals are the vehicle that turns a proven
instrument into one a user with momentum elsewhere can adopt, audit, and trust.

*Cross-refs: `../IS_Hs_RIGHT_FOR_YOU.md` (the front door), `../papers/PAPER_REFINEMENT_AND_RELEASE_PLAN_2026-06.md`
(the release arc), `../INDUCTION_MAP.md` (traversal), `../experiments/` (the receipts). Proof & Honesty Standard
throughout. Peter is the sole gate; nothing posted.*
