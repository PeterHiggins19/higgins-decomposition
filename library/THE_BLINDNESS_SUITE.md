# The blindness suite — what each reading cannot see, and the channel that recovers it

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-23. A unifying
concept the project arrived at by measurement, not design: **every reading of a composition is a projection,
and every projection is blind to its complement.** Each blindness names a *recoverable event class*, and each
class is recovered by adding the next channel. Ratio-blind and mass-blind were named months ago; rotation-blind
is the third member, measured on the live fleet this session — "a class beyond the class." Honest-broker
tiered; conforms to the Proof & Honesty Standard. Nothing posted; Peter is the sole gate.*

---

## The idea, in one line

> A reader that sees only **one face** of a moving composition will be **confidently silent** about events that
> live in the face it cannot see. Name the blindness, and you have named a new, recoverable class of event.

This is not a weakness to hide — it is the **map of what each layer adds.** The instrument's honesty (it says
what it cannot resolve, HISTORY_THREAD link 10) here becomes *generative*: each named blindness points directly
at the channel that removes it.

## The suite

| member | the reader that is blind | what it sees | **blind to** | the recovered event class | recovered by | status |
|---|---|---|---|---|---|---|
| **Ratio-blind** | a scalar / threshold / total-magnitude monitor | levels, totals, alarms | the **ratios** (relative change) | **deceptive / silent drift** — concentration tightens toward a failure mode while raw levels look calm | the relational (log-ratio / ILR) read | **T1**, measured — the seam all three witnesses share (W-I/W-II/W-III); the CMP/P8 result |
| **Mass-blind** | the **helmsman** (`argmax |Δclr|`) | the *fastest* log-ratio mover (often a small carrier) | the **mass** (where the bulk actually goes) | a small fast carrier flagged while the **weight** of the system shifts elsewhere | **momentum** (mass × velocity; the arrow of intent) | **T1**, measured — EMBER energy transitions; momentum and helmsman disagree every time |
| **Rotation-blind** | the **direction / rotation** read of the ILR state | the *directional* drift (which ratios turn) | the **size / magnitude** of the state vector | a **budget-magnitude move with no directional turn** — the whole mix inflates/deflates without changing its shape | the **dual-quaternion translation channel** (SE(3) 6-DOF) | **T1**, measured — Backblaze fleet, **30 rotation-blind events** in 730 days (receipt `d531e545…`) |

Read down the "blind to" column: **ratios → mass → size.** Each is an independent face of the same moving
composition. Each reader is excellent at its own face and silent on the next. The suite is the set of faces,
and the instrument is complete on a given domain only when every face that matters there is read.

## Newer members named during the rapid development burst (2026‑06, open by design)

The principle — *every reading is a projection, blind to its complement* — kept generating members as the work
moved through communications, optics, and lithography. These join the suite at the tier their evidence supports:

| member | the reader that is blind | blind to | the recovered event class | recovered by | status |
|---|---|---|---|---|---|
| **Phase‑blind** | direct / intensity detection (throws phase away) | the **phase** (and the extra quadratures/polarizations) | structure carried in amplitude **and** phase — more dimensions per symbol | **coherent detection** (amplitude + phase) — its dial is **Q** (`ρ=exp(−2π/Q)`; see [`THE_Q_CONNECTION.md`](THE_Q_CONNECTION.md)) | **T2** (reasoned); the coherence law it leans on is **T1** measured (`a5ceab9e`) |
| **Direction‑blind** | a scalar **total** count (e.g. total defect count) | the **sign / direction** of the move | a two‑sided cliff: the same total rises on *both* sides, so you cannot tell which way to correct | the composition's **signed arrow** (the directional helmsman) | **T2**, model‑grounded — the EUV stochastic valley‑of‑death (`877516b6`) |
| **Data‑blind** *(meta)* | a whole field assuming a message needs a **separate carrier** | the fact that the **data is the carrier** — control already lives in the composition | wasted carrier symbology; missed self‑describing structure | reading the **data as the carrier** (closure = reference, ilr = frame, log‑ratios = symbols) | **framing‑level**; the P‑Ω keystone (`742f1b5a`) |

*Relationship‑blind* (used by the three witnesses and the CMP) is the relational naming of **ratio‑blind** — the
same face, not a separate one. *Projection‑blind* is the **whole principle**, not a member: every member is a
projection blind to its complement, which is why the family keeps growing.

> Read together, the faces are now: **ratios · mass · size · phase · direction**, over a **meta** layer
> (data‑blind) that says the carrier was the data all along. The suite stays **open** — a member joins only with a
> receipt, and the next (curvature/jet of the trajectory; the second `su(2)`'s structure) is left for further
> investigation.

## Why this was predicted (the fulfilled-prediction note)

The blindness vocabulary is not new this session — it was **seeded months ago**. The compositional-momentum
work named two members explicitly: the helmsman is *"mass-blind"* and the relational read is the
*"ratio-blindness specialty"* (`experiments/compositional_momentum_2026-06/RESULTS.md`). And the extension-
predictions register set the expectation directly: *"Correct predictions validate the tool's interpretability.
**Surprises reveal new information.**"* (`Hs_EXTENSION_PREDICTIONS.json`). **Rotation-blind is exactly that
surprise made concrete** — the third face, found by running the new SO(4)/dual-quaternion channel on real data
and seeing 30 events the rotation-only read could not. The pattern predicted the member; the member arrived
with a receipt.

## Why it makes the system solid (the revelation)

Before the suite, "the relational read beats the aggregate" was a *single* claim. The suite turns it into a
**closed, checkable taxonomy**: for any compositional reading you can now ask *"which face is this, and what is
it blind to?"* — and answer with a named class and the channel that recovers it. That is what a regulated or
safety-critical adopter needs: not "trust the read," but **"here are the faces, here is the one this read cannot
see, here is the channel that sees it, and here is the receipt."** The instrument stops being a tool with one
good trick and becomes a **layered reader that knows its own coverage.**

## What is and is not claimed

- **T1 (measured):** all three members are demonstrated on real data with receipts — ratio-blind (W-I/W-II/
  W-III, CMP), mass-blind (EMBER momentum), rotation-blind (Backblaze, 30 events, `d531e545…`).
- **T2 (reasoned):** that the suite is *complete* (only three faces). It is **not** claimed closed — higher
  reads (e.g. the curvature/jet of the trajectory, or the second `su(2)`'s further structure) may name a
  fourth blindness. The suite is **open by design**; new members join only with a measured receipt.
- **Not claimed:** that any one member *replaces* another. They are **complementary faces** — the value is
  reading them together, each with its own receipt, never one in place of the rest.

*Cross-refs: `../experiments/so4_dualquaternion_2026-06/RESULTS_backblaze_so4.md` (rotation-blind, measured),
`../experiments/compositional_momentum_2026-06/RESULTS.md` (mass-blind, named), `../papers/triangulation/`
(ratio-blind, the three witnesses), `../papers/COMPOSITIONAL_MESSAGE_PRINCIPLE_PAPER_SEED.md`,
`../HISTORY_THREAD.md` (link 11), `../Hs_EXTENSION_PREDICTIONS.json`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited-or-fenced · math proven + receipted · value shown · experts decide.*

## Appendix — Q-factor review (test of concept)

*A standing test of the Q seed (`THE_Q_CONNECTION.md`): read this document through Q and report honestly where it
HOLDS and where it does NOT — the boundary is the result. Nothing published; appendix only; lose nothing, miss
nothing.*

Read the suite through Q: Q is the **dial of the phase face** (`ρ = exp(−2π/Q)`) — coherent vs intensity‑only
reading. **Holds for one face.** **Does NOT extend (the test result):** the ratios, mass, size, and direction
faces are **not** Q‑governed — Q lights exactly one axis of the suite, and that boundary is itself the honest
finding. The blindness family is broader than Q; Q is its phase member's physics.

*Q-review status: T2 where the bridge is measured (`52fee398`); the "Q is universal" generalization stays a T3
seed; the boundary noted above is the honest falsifier. Lineage: Richard H. Small & A. N. Thiele.*
