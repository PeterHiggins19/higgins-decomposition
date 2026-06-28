# Gen-2 — evolving the system from its own stress test

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. The usual
Hˢ standard: **build on the past, make the future.** The stress sheet (G-248, master receipt `e395fa38`) is
the **stepping stone** — it found the system's two low-dimension weaknesses. Gen-2 takes those exact findings,
applies a principled improvement to each, and **re-tests on the same failing cases**, keeping a refinement
only where the data shows it earns its place. Receipt `f56abdb6ffa1f577`. Honest-broker; Peter is the sole
gate; nothing posted.*

---

## Orientation — what the past test said (the stepping stone)

The Gen-1 stress sheet passed the deterministic core at every dimension under 10⁶× deformation, but flagged
**two real low-D failures**: the discriminant collapsed at D=2, and associative memory recall failed at low
D / near-duplicate data. Those are the two seams Gen-2 works on. Nothing is re-derived from scratch; the prior
result orients the work.

## Refinement 1 — the discriminant (KEPT)

**Diagnosis.** At D=2 the per-component rule `argmax|clr|` is *degenerate*: with two parts `clr = [a, −a]`, so
`|clr| = [|a|, |a|]` — a guaranteed tie that flips under any noise. The failure was structural, not bad luck.

**The improvement (and it cites our allies).** Discriminate on the **ilr / balances** (Egozcue,
Pawlowsky-Glahn, Mateu-Figueras & Barceló-Vidal 2003) — the D−1 orthonormal coordinates — which are
**non-degenerate at every dimension**, plus a **margin gate** that **withholds** the decision when the top-two
contrasts are too close (the coherence-gate discipline) rather than flipping. This is exactly the
Locked-Discriminant Principle, which we already proved holds in ilr (`74e8e6e5`).

**Re-tested:**

| D | Gen-1 invariance | Gen-2 invariance (on confident) | Gen-2 confident fraction |
|---|---|---|---|
| **2** | **0.58 (fail)** | **1.00** | 0.97 |
| 3 | 1.00 | 1.00 | 0.85 |
| 4 (geology) | 1.00 | 1.00 | 0.43 |
| 8 | 1.00 | 1.00 | 0.83 |

The D=2 failure is **fixed**: the balance discriminant is locked at every D, and where it cannot decide
confidently it **says so** (an honest withhold) instead of flipping. **Kept.**

## Refinement 2 — the memory (one idea rejected, the honest one kept)

**Tried:** a **whitened (Mahalanobis)** distance, to separate near-duplicate compositions by their
discriminative directions. **Result:** it did **not** help — geology recall `0.26 → 0.24`. The data said no.

**Why, and the honest fix.** The geology bank's **minimum pairwise clr separation is 0.003** — the entries
genuinely *are* nearly the same composition (one mudstone formation). **No metric can recall apart things that
are the same**, and pretending otherwise would be dishonest. So Gen-2 replaces the failed metric with a
**diversity gate**: when the bank's minimum separation is below threshold, the memory **flags recall as
unreliable** rather than returning a confident wrong answer. On a diverse bank, recall stays ~1.0 and the gate
passes. **Mahalanobis rejected; detection kept.**

## The evolution, stated plainly

Gen-2 is **strictly better at the discriminant** (the D=2 hole closed, with honest withholds) and **honestly
bounded at the memory** (near-duplicate recall correctly flagged, not faked). That is the standard: a
refinement is kept only where it measurably helps; where it does not, the system is taught to **recognise its
limit**, which is itself an improvement. The future was built on the past test, and the past test is cited as
the rudimentary baseline it was.

## Verify + further refinements

- Verify: `python3 hs_gen2.py` → receipt `f56abdb6ffa1f577`; `python3 hs_dut_stress.py` → `e395fa38` (the
  Gen-1 baseline it builds on).
- **Next refinements (open):** tune the margin-gate threshold per application; collapse near-duplicate bank
  entries on write (dedup) so the diversity gate becomes a storage optimisation; carry the ilr/balance
  discriminant into the conveyor's routing; re-run the full D=2..1000 sheet with the Gen-2 discriminant wired
  in for a Gen-2 master receipt.

## Honest tiers

- **T1 (measured):** both re-tests on real + seeded data, receipted; the D=2 fix and the diversity gate.
- **T2 (a design choice):** the margin threshold (0.05) and the diversity threshold (0.15) — application-set.
- **Not claimed:** that near-duplicate recall is "solved" — it is correctly *detected*, not recovered.

*Cross-refs: `hs_gen2.py`, `HS_GEN2_RESULTS.json`, `THE_DUT_STRESS_REPORT.md` (the stepping stone),
`../../papers/locked-discriminant/ilr_incorporation.py` (the ally tool), `../../CODA-Association/BUILT_ON_AND_FOR_THE_CODA_COMMUNITY.md`.
Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — built on the past test (cited) · the kept refinement is measured · the rejected one is reported, not buried · the limit is detected, not faked · anyone can verify.*
