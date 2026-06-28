# Export & Transfer Governance — rules for every field where Hˢ meets industry (DOCTRINE · INTERNAL)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑24. A reusable
governance doctrine that defines, for **any** industrial application of Hˢ, what is published openly and what is
transferred up to a governance steward — built because the EUV case showed the question will recur. Honest‑broker
tiered; **not legal advice** (competent export‑control authority/counsel governs specifics); Peter is the sole
gate; nothing posted.*

---

## 1. First principle — publish the principle, steward the applied

Every Hˢ application separates into two layers:

- **The principle** — the abstract compositional method (closure → log‑ratio → kinematic read → coherence gate →
  receipt) and its mathematics. *Basic science. Always publishable.* It advances the whole field and invites the
  verification that earns trust.
- **The applied how‑to** — a specific, tuned recipe to deploy on real tools in a sensitive field. *May be
  controlled or strategically weighty.* Its release is **not ours to decide alone**.

The rule: **publish the principle; gate the applied how‑to by sensitivity; defer sensitive release upward** to
the governance system we are a sub‑composition of (a national jurisdiction — Canada — and through it an allied
order). The instrument's own doctrine — *the part reports up; control flows down only when authorized; the
operator holds the breaker* — applies to **us**.

## 2. The classification method (deterministic, receipted)

Read each application as a **composition over four export/transfer‑sensitivity axes**:

| axis | meaning |
|---|---|
| **open_science** | share that is publishable principle (basic science) |
| **applied_knowhow** | share that is transferable applied how‑to |
| **controlled_adj** | proximity to export‑controlled / dual‑use technology |
| **strategic_weight** | impingement on global economics / national security |

Define the **transfer‑sensitivity index** `tsi = closed‑share(controlled_adj + strategic_weight)`. The axis
scores are honest **judgment inputs (Tier 3)**; the compositional read and ranking are **deterministic and
hash‑receipted** (`export_sensitivity_read.py`, `EXPORT_SENSITIVITY_LEDGER.json`, receipt `14b2f557`).

## 3. The three dispositions

| disposition | rule | action |
|---|---|---|
| **OPEN** | `tsi < 0.42` | publish (principle *and* applied), low transfer sensitivity |
| **REVIEW** | `0.42 ≤ tsi < 0.55` | publish the principle; route the **applied how‑to** to a steward; case‑by‑case |
| **STEWARD** | `tsi ≥ 0.55` | publish the principle; **withhold the applied how‑to** and **offer it to national governance**; the government decides distribution and any export control |

Thresholds are deliberately conservative. A high `tsi` does **not** assert that something *is* legally
controlled — it asserts that **we are not the right party to decide its release alone**, and we route it up.

## 4. The doctrine applied to the whole portfolio (already done + projected)

From the receipted read (`14b2f557`). **STEWARD** (offer applied how‑to to governance): **fusion/nuclear
diagnostics, aerospace‑defense sensor‑skin, EUV lithography, space‑launch GNC, constellation/space‑SSA**.
**REVIEW**: quantum‑photonics manufacturing, critical‑infrastructure control, advanced packaging/chiplet,
fiber‑photonics, telecom/6G, autonomous robotics, energy‑grid, microbiome/bio. **OPEN**: SMT dispense/placement,
financial‑markets, produced‑water, Backblaze fleet, gas/life‑support, blood‑gas/clinical, geoscience.

| application | done? | tsi | dominant axis | disposition |
|---|---|---|---|---|
| fusion‑nuclear‑diag | future | 0.59 | controlled_adj | **STEWARD** |
| aerospace‑defense‑skin | future | 0.58 | strategic_weight | **STEWARD** |
| **euv‑lithography** | ✅ | 0.58 | controlled_adj | **STEWARD** |
| space‑launch‑GNC | future | 0.57 | controlled_adj | **STEWARD** |
| constellation‑space‑SSA | ✅ | 0.55 | strategic_weight | **STEWARD** |
| quantum‑photonics‑mfg | future | 0.55 | controlled_adj | REVIEW |
| critical‑infra‑control | future | 0.54 | strategic_weight | REVIEW |
| advanced‑packaging‑chiplet | future | 0.50 | applied_knowhow | REVIEW |
| fiber‑photonics | ✅ | 0.48 | applied_knowhow | REVIEW |
| telecom‑6g‑comms | future | 0.48 | applied_knowhow | REVIEW |
| autonomous‑robotics | future | 0.46 | applied_knowhow | REVIEW |
| energy‑grid | ✅ | 0.46 | open_science | REVIEW |
| microbiome‑bio | ✅ | 0.46 | open_science | REVIEW |
| smt‑dispense‑placement | ✅ | 0.42 | applied_knowhow | OPEN |
| financial‑markets | ✅ | 0.39 | open_science | OPEN |
| produced‑water‑oilgas | ✅ | 0.32 | open_science | OPEN |
| backblaze‑fleet | ✅ | 0.30 | open_science | OPEN |
| gas‑life‑support | ✅ | 0.22 | open_science | OPEN |
| blood‑gas‑clinical | ✅ | 0.22 | open_science | OPEN |
| geoscience | ✅ | 0.22 | open_science | OPEN |

Portfolio mean shares: open_science 0.29 · applied_knowhow 0.26 · controlled_adj 0.20 · strategic_weight 0.24 —
i.e. **most of the portfolio is openly publishable**, with a small, identifiable high‑sensitivity tail that goes
to a steward. Effective dimension over the sensitivity spread ≈ 1.4: the field is mostly *one* axis of
variation — open‑science vs strategic‑weight — which is exactly the publish‑vs‑steward line.

> **Resolved cases:** EUV and the constellation work are STEWARD → both routed to the Government of Canada offering
> (`../../industrial-instruments/euv-lithography/OFFER_TO_CANADA_AND_PUBLIC_SCIENCE.md`). The OPEN cases continue
> on the existing public P‑series path. REVIEW cases are flagged for case‑by‑case handling at Peter's gate.

## 5. Standing rules (apply to every field)

1. **Publish the principle** — always; it is the part's gift to the whole.
2. **Gate the applied how‑to by `tsi`** — OPEN / REVIEW / STEWARD per §3.
3. **Defer sensitive release upward** — STEWARD applied how‑to is *offered to* national governance, never
   distributed on our authority.
4. **No company contact by us** — the only sensitive‑case recipient is the appropriate government; companies and
   allies are served through that steward.
5. **Peter is the sole gate** — for any publication, transfer, or offer. Nothing posted or sent without it.
6. **Honest scope of "how‑to"** — we hand methods, application plans, roadmaps, and conformance — *never* claimed
   controlled hardware we do not possess.
7. **Not legal advice** — competent export‑control authority/counsel decides what is actually controlled; this
   doctrine sets *our* conservative default.

## 6. The diffusion question — how long before it becomes apparent

Peter's question: once the principle is released and "even better minds get on it," how long before the value of
what is *already published* becomes apparent? Honest, **Tier‑3** projection (a reasoned range, not a measurement):

- **The principle is already partly public** (the P‑series, the public‑physics framings). Recognition of a new
  cross‑domain method typically follows a **diffusion S‑curve**: a quiet period while the idea is read and
  reproduced, then acceleration once independent groups confirm it in their own domains.
- **Rough horizon (reasoned, not promised):** *months* for first independent reproductions of the receipted,
  public demonstrations; **~1–3 years** for the cross‑domain pattern ("composition is the message / the data is
  the carrier") to be picked up by stronger groups and pushed past where we took it; **longer tail** for the
  high‑sensitivity applied fields, whose pace is set by *governance* (steward uptake), not by science.
- **What accelerates it:** open, reproducible receipts (anyone can re‑run); a clean principle; the honest tiering
  that lets others trust and build. **What slows it:** the very sensitivity that sends the applied tail to a
  steward — there, slower *is the design*.
- **The asymmetry that favors a head start:** the moment the principle is public, the *open* tier compounds in
  the world while the *applied* high‑sensitivity tier is held by whichever steward moved first. A steward who
  reads the package early (Canada) holds a lead on the applied front precisely while the science spreads
  everywhere — "a head start, if they even read it."

These are **judgments, explicitly tiered T3** — offered to think with, not as forecasts. The durable, honest
claim is structural: *open science diffuses on its own timescale; sensitive applied know‑how moves only as fast
as governance allows; a prepared steward converts that gap into a lead.*

## 7. Honest scope

- **T1:** the engine + the deterministic compositional read/ranking (`14b2f557`).
- **T2:** the four‑axis model, the thresholds, the dispositions — reasoned governance design.
- **T3:** every axis score (judgment), every diffusion horizon, every uptake — none asserted as fact; revisable
  at Peter's gate.

*Cross‑refs: `export_sensitivity_read.py`, `EXPORT_SENSITIVITY_LEDGER.json`,
`../../industrial-instruments/euv-lithography/POLITICAL_COMPOSITION_AND_EXPORT.md`,
`../../industrial-instruments/euv-lithography/OFFER_TO_CANADA_AND_PUBLIC_SCIENCE.md`,
`../COMPONENT_REQUEST_ESCALATION_DOCTRINE.md` (escalate‑upward / Breaker 16), `CARRIER_FILTER_DOCTRINE.md` (HUF).
Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited‑or‑fenced · classification deterministic · sensitive release deferred upward · the human decides.*
