# The Diagnostic-Constructive Duality — the math that finds the flaw is the math that proves the conjecture (PAPER SEED)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. An idea
that has quietly run the whole project, now named: in a **deterministic, invariance-based** compositional
framework, the computation that **locates a flaw** is the **same** computation that **certifies the proof** —
falsifier and certificate are one function, read by its value. Demonstrated; receipt `b9b62de04d6d69e1`.
Honest-broker tiered; Peter is the sole gate; nothing posted.*

---

## The name and the one line

> **The Diagnostic-Constructive Duality — "the math used to find the flaw is the math to prove the
> conjecture."** A single invariance functional, applied to a construct, returns the **falsifier** when its
> value is low (a flaw located) and the **certificate** when its value is one (a proof). Because the framework
> is deterministic, the flaw is *located*, and its location is exactly the constructive datum that proves the
> fix.

## The statement

Let `G` be the nuisance group the system rejects (multiplicative common-mode, baseline offset), and let
`I(c)` = the invariance of a construct `c` under `G`. Then `I` is simultaneously:

- a **diagnostic** — `I(c) < 1` *locates* a flaw: a coordinate where `c` is not invariant (degenerate,
  drifting, non-reproducible); and
- a **constructive certificate** — `I(c) = 1` *proves* the corresponding claim: `c` factors through the
  maximal invariant (it is locked, reproducible, correct).

The flaw and the proof are **the boundary of one invariance structure**: where the invariant *isn't* is the
flaw; where it *is* is the proof. One computation, two readings.

## Demonstrated (receipt `b9b62de04d6d69e1`)

The **same** functional `nuisance_invariance(rule)` run on two constructs at D=2 (and the geology at D=4):

| construct | the SAME functional reads | role it plays |
|---|---|---|
| `argmax\|clr\|` at D=2 (degenerate: `clr=[a,−a]`) | **0.52** | **falsifier** — flaw located |
| ilr-balance discriminant | **1.00** | **certificate** — proof certified |

One function. Low on the broken construct, exactly one on the correct one. The math that *found* the D=2
discriminant flaw is the math that *proved* the ilr-balance fix.

## The evidence ledger — it has always worked this way (past + present)

This is not a new trick; it is the pattern under the whole corpus. Each row: the same math located a flaw and
proved the corresponding claim.

| instance | the flaw the math located | the proof the same math gave | receipt |
|---|---|---|---|
| **Locked-Discriminant Principle** | the non-invariant discriminants (rate 0.61/0.83) | "invariance is the lock" (the failures *were* the necessity proof) | `9055c4a9` |
| **Gen-2 evolution** | the D=2 `clr` degeneracy | the ilr-balance fix (non-degenerate, locked) | `f56abdb6` |
| **this demonstration** | `argmax\|clr\|` not invariant | the ilr-balance certified invariant | `b9b62de0` |
| **the blindness suite** | each blindness = what a projection cannot see | names the recoverable class + the channel that recovers it | `d531e545` |
| **the triad backbone** | the coherence vote *locates* the outlier route | the same coherence vote *certifies* agreement | `f8ee9f6f` |
| **the DUT stress sheet** | where the system fails (the low-D envelope) | *is* the proof of where it holds (D≥8, all the deterministic core) | `e395fa38` |
| **C2 common-mode** | where rejection fails (additive noise floor) | where it is exact (multiplicative common-mode) | `09fff092` |
| **E-21 guard** | the all-zero carrier → `log(0)` failure | the same condition *defines* the guard that fixes it | engine |

In every case the diagnostic and the construction are one analysis. Build on all of them: the duality is the
through-line.

## Why it holds (the two ingredients)

- **Invariance.** The framework is built on what is invariant under `G`. A flaw is a *non-invariance*; a proof
  is an *invariant*. The same invariance test reads both — it cannot help but be both.
- **Determinism.** Because every read is exact and receipted, a flaw is *located*, not merely detected
  statistically. A located flaw is **constructive**: knowing *where* invariance breaks tells you exactly which
  coordinate to move to (clr → ilr), which channel recovers a blindness, which route is the outlier. The
  location *is* the fix.

## Honest scope (classical roots + the contribution)

- **Classical and cited:** *falsifiability* (Popper) is the diagnostic half; the *constructive vs.
  non-constructive proof* distinction (Brouwer, Bishop) is the constructive half; the *invariance principle /
  maximal invariants* (Eaton) is the machinery. None of these is new here.
- **The contribution (T2, a framing/conjecture):** that in a **deterministic invariance framework these two
  halves coincide as a single computation** — the falsifier and the certificate are the same functional read
  by its value, and determinism makes the falsifier constructive. We claim this as an organising **conjecture
  about the method**, supported by the evidence ledger, not a new theorem of logic.
- **Falsifier of the duality itself:** exhibit, in this framework, a flaw that the system's own invariance
  analysis *cannot* locate, or a located non-invariance that gives *no* constructive route to a fix. The
  conjecture forbids both.

*Cross-refs: `diagnostic_constructive_duality.py`, `DUALITY_RESULTS.json`,
`../locked-discriminant/THE_LOCKED_DISCRIMINANT_PRINCIPLE.md`, `../../experiments/hs_dut_stress_2026-06/THE_EVOLUTION_GEN2.md`,
`../../library/THE_BLINDNESS_SUITE.md`, `../../triad-backbone/THE_TRIAD_BACKBONE.md`,
`../connection-confirmation/CONFIRMATION_LEDGER.md` (C2). Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the duality is demonstrated (one functional, two roles) · the evidence ledger is receipted · the classical roots are cited · it is claimed as a conjecture about the method, with its own falsifier · experts decide.*
