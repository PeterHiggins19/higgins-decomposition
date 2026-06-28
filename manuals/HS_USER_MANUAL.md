# Hˢ User Manual — how to use it, and why this one

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. The
operating manual: what Hˢ is for, when to reach for it, how to run it, how to read the result, and how the
governance keeps it safe. Written for a user with momentum elsewhere who needs to know in five minutes whether
this is worth switching to. Honest-broker tiered; nothing posted; Peter is the sole gate.*

---

## 1. Why this one (the differentiator)

You already have tools that read your data. Reach for Hˢ when **two** things are true at once:

1. your data is a **composition** — parts of a conserved whole (a budget, a mix, shares that sum to a total); and
2. your decision must be **auditable** — re-runnable to the *same* answer by a third party (regulator, insurer,
   counterparty, reviewer), where a confident-wrong answer is unacceptable.

That intersection is thinly served. Statistical tools give you a number; **Hˢ gives you a number with a
receipt, that withholds when the evidence is thin, and that any machine reproduces to the bit.** It is the only
deterministic-*enforced*, hash-*receipted*, exact compositional instrument designed for applications-on-applications.

## 2. When to use it / when not to

| use Hˢ when… | do **not** use Hˢ when… |
|---|---|
| parts sum to a conserved total (budget, mix, shares) | the data is not compositional (the qualifier gate refuses) |
| you need reproducibility / audit / a content receipt | you only need a quick exploratory statistic |
| the signal is in the **ratios** (relative change) | the signal is purely in absolute levels |
| common-mode gain/level/distance drift corrupts you | you need to cancel in-subspace random noise (use averaging) |
| you want to read *motion* (arrow, character, drift) | you want a forecast (Hˢ reads the present, not the future) |

## 3. Quick start (the four altitudes)

```
   READ    -> open IS_Hs_RIGHT_FOR_YOU.md and this manual            (5 min: should I?)
   RUN     -> point the engine at a CSV of conserved-budget rows     (the read + receipt)
   VERIFY  -> hs_gold_fixtures.py --verify  -> reproduces d7ac6530    (trust by checking)
   EXTEND  -> son_exact_generator.py / the four-form port            (build on it)
```

Minimum input: a table whose rows are compositions (strictly positive parts summing to a budget). The engine
closes, transforms to log-ratios, guards, reads, and stamps a SHA-256 on the result.

## 4. Reading the output (what the numbers mean)

- **Arrow of intent** — which parts are gaining vs losing share, and how committed the motion is (a direction
  + a magnitude). *Where the weight is flowing now — not where it will be.*
- **Character** — Ballistic (one directed arrow) · Contested · Turbulent · Diffusive (churn). The system's
  "how it moves."
- **Effective dimension** — how many independent directions the variation really uses (often far fewer than the
  number of parts — that is the compressible, denoisable structure).
- **The blindness faces** — *ratio-blind* (what level monitors miss), *mass-blind* (what the fastest-mover view
  misses), *rotation-blind* (size moves with no directional change). Read the face you need.
- **The receipt** — the SHA-256. Two runs that agree on the receipt agree to the bit. Integrity is built in.
- **A withhold code** (e.g. `MO-DIF-WRN`, `HOLD-LOCK`) — the instrument refusing to draw a conclusion the data
  does not support. *A refusal is a result.*

## 5. Modes (operate at your scale)

| mode | who | behavior | gate |
|---|---|---|---|
| **manual** | an analyst | the instrument flags; you decide | you |
| **assisted** | an operator | reads + suggested actions, all receipted | you, per action |
| **automated** | a machine/loop | the same reads run unattended **behind breakers** (SafeLoop) | operator holds Breaker 16; full automation never |

The governance is invariant under scale: determinism is what makes delegation safe, because the machine may
*act* on a read only since the read is *checkable*.

## 6. A worked example (the shape of a session)

1. **Input:** a fleet's failure-mode budget `(Mechanical, Thermal, Age, Errors)` per day.
2. **Hˢ reads:** the arrow of intent (drift toward Mechanical/Age), the effective dimension (~1.7 — sortable),
   the silent-drift events the threshold monitors miss, the rotation-blind size events, all hash-stamped.
3. **You decide:** schedule replacement on the drifting units — or hold, if the coherence gate withheld.
   *(Real case: the Backblaze witness, receipt `058fde30…`.)*

## 7. Safety & limits (read before design-in)

- Hˢ **refuses** non-compositional input and **withholds** on incoherent or at-rest data — by design.
- Hˢ does **not** forecast, does **not** cancel in-subspace random noise, does **not** exceed information-theory
  limits, and is **not** a controller of record — it is a complementary reading layer.
- The operator is the **sole gate**; nothing acts without a human breaker; safety is dominant and absolute.

## 8. Tiers

- **T1 (measured):** every behavior above traces to a receipted experiment.
- **T2 (reasoned):** the mode model and the use/don't-use guidance.
- **T3 (rejected):** forecasting, full automation, beating Shannon, lossless-at-scale.

*Cross-refs: `HS_THEORY_OF_OPERATION.md` (the internals), `HS_USE_CASES.md` (where it earns its keep),
`../IS_Hs_RIGHT_FOR_YOU.md`, `../papers/datasheets/`. Peter is the sole gate; nothing posted.*
