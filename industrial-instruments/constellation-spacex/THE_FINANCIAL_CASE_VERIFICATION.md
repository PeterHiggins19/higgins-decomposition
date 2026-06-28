# Verification of the financial case — numbers cited, math proven, value shown, experts decide

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-22. The
honest-broker pass on `THE_FINANCIAL_CASE.md`, answering four questions in order: **were the numbers
verifiable? was the math valid? did the study have value? — then let the experts decide.** We make no
recommendation and no pitch; the **cited public data and the receipted arithmetic are the shield**. Nothing
posted; no contact; Peter is the sole gate.*

---

## Q1 — Were all the numbers verifiable? (the audit; the data is the shield)

**Honest answer: the *bases* are public and cited; the *fractions* are not — they are stated assumptions,
fenced and labelled.** Only the bases bear weight.

### Load-bearing — public, verifiable, cited (the shield)

| number | value | source |
|---|---|---|
| Feb 2022 Starlink loss | **~38 of 49** dragged to reentry by a *minor* storm; multi-$M | Baruah 2024 (*Space Weather* 2023SW003716); CIRES; SWSC 2022 |
| Per-satellite cost | V1 ~$0.2 M · ~$0.4 M avg · V2-mini ~$0.8 M | New Space Economy (2026); press |
| Starlink fleet | ~10,400 active; ~75% of active maneuverable sats | constellation `DATA_AND_SOURCES.md`; SpaceNews; Wikipedia |
| Starlink revenue 2025 | ~$11.4 B | SpaceNews |
| Orbital-DC filings | SpaceX ~1 M sats / ~100 GW·yr; Starcloud ~88 k; Blue Origin ~51.6 k | Fierce Network; Introl |

Every one of these is a third-party-checkable figure. **The derived base** (annual fleet replacement ≈
$0.6–1.7 B) is *computed from* the cited fleet size, per-sat cost, and a 5–7-yr life — shown, not asserted.

### NOT load-bearing — my assumptions (Tier 3; explicitly not public)

The improvement fractions — L1 prevention 20–50% and 1‑in‑1‑to‑3‑years; L2 0.3–0.6%; L3 $1–5 M judgement;
L6 0.1% × 20–50% attributable — are **guesses**. They are not in any source and are flagged as such in the
case and in the code. *The shield does not extend to them; they are fenced, falsifiable, and replaceable.*

## Q2 — Was the math valid? (proof, with a receipt)

**Proven, deterministically.** `fin_case_verify.py` recomputes every lever from the cited bases × the stated
assumptions and emits a SHA-256 receipt; it returns the **identical hash on rerun** (`result_hash
2d9fc354630bd5ee`, `inputs_hash cef1bad2b5b04454`). Anyone can run it and get the same numbers — the same
determinism discipline the whole project rests on, applied to its own estimate.

| lever | verified range (USD M/yr) |
|---|---|
| L1 storm-loss warning | **1.0 – 15.2** |
| L2 pre-fault replacement | **1.8 – 10.0** |
| L3 maneuver / fuel | **1.0 – 5.0** |
| L6 QoS / revenue | **2.3 – 5.7** |
| **conservative total** | **6.1 – 35.9** = **0.05 – 0.32% of Starlink revenue** |

**The proof did real work (honest-broker in action).** The arithmetic **corrected the first-pass ranges**:
L1 $3–10 M → **$1–15 M**; L2 $5–10 M → **$2–10 M**; L6 $5–11 M → **$2–6 M**; total "$10–40 M" → **$6–36 M**.
The headline survives — *low tens of millions, a fraction of a percent* — but it is now the number the math
actually supports, not a rounder one. The math disposed; we updated the case to match.

## Q3 — Did the study have value? (show it)

**Yes — and the value is exactly that it can be checked.** It converts "money is king" from a slogan into a
decision-useful object with four checkable parts:

1. **A cited public base** an expert can verify line by line (Q1).
2. **A receipted arithmetic** an expert can re-run to a matching hash (Q2).
3. **A clean fence** between fact (cited) and assumption (labelled) — so a reviewer knows precisely which
   numbers to trust and which to challenge.
4. **One decisive test** (the §6 storm backtest) that would move the flagship lever from *assumption* to
   *measurement* — turning "hours of warning before the threshold" into a receipt that anchors the whole case.

That is the deliverable: not a dollar figure to believe, but an **auditable, reproducible, falsifiable
estimate** an expert can act on *because* they can take it apart. A study whose every number is either cited
or fenced, and whose arithmetic reproduces to a hash, has value precisely in proportion to how easily it can
be checked.

## Q4 — Let the experts decide; we stay out of the way

We make **no recommendation, no pitch, no approach.** We present: the cited public data, the receipted
arithmetic, the fenced assumptions, and the one test that would settle the flagship lever — and we step back.
**The data is the shield:** the only load-bearing claims are the ones an outside expert can independently
verify, and they are marked; the assumptions are explicitly *not* load-bearing, and they are marked too. An
expert who disagrees with a fraction changes one labelled input and re-runs to a new hash; an expert who
disagrees with a base cites a better source. Either way the structure holds, because nothing is hidden behind
mortar.

## Verdict

- **Numbers:** bases **verifiable + cited**; fractions **assumptions, fenced** (T3). ✔
- **Math:** **valid, deterministic, receipted** (`2d9fc354630bd5ee`); first-pass ranges corrected to the
  computed envelope. ✔
- **Value:** **methodological + decision-useful** — checkable in four parts, with one decisive test. ✔
- **Stance:** **experts decide; the verifiable data is the shield**; no advocacy, no contact, nothing posted.

*Reproduce: `python fin_case_verify.py` (deterministic; matches `result_hash 2d9fc354630bd5ee`). Cross-refs:
`THE_FINANCIAL_CASE.md`, `THE_HUF_CONSTELLATION_SYSTEM_PROPOSAL` §6 (the decisive test). Peter is the sole
gate; nothing posted.*

Sources: [Baruah 2024 — Feb 2022 Starlink loss (*Space Weather*)](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2023SW003716), [CIRES](https://cires.colorado.edu/news/minor-geomagnetic-storm-big-impact-february-2022-starlink-satellite-loss), [SpaceNews — Starlink revenue](https://spacenews.com/starlink-soars-spacexs-satellite-internet-surprises-analysts-with-6-6-billion-revenue-projection/), [New Space Economy — manufacturing economics](https://newspaceeconomy.ca/2026/04/13/the-satellite-manufacturing-market-after-starlink-how-mass-production-changed-the-economics-of-building-spacecraft/), [Fierce Network — orbital DC filings](https://www.fierce-network.com/cloud/space-data-centers-starcloud-spacex-and-project-suncatcher-explained).
