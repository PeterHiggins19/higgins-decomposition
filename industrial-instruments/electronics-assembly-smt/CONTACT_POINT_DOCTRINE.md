# The Contact‑Point Doctrine — where the dirt is, and where to spend the effort (INTERNAL · PLANNING)

*Author: Peter Higgins (human authorship — this is Peter's field doctrine, told to Fuji‑class customers over
years of line experience); AI‑assisted per HUF‑STD‑001. 2026‑06‑24. **No contact, partnership, or endorsement
with any named manufacturer is implied or sought** — equipment domains only. Honest‑broker tiered; nothing
posted; Peter is the sole gate.*

---

## The doctrine (Peter's words, kept plain)

> *Consider the machine dirty at every point of contact with the product. Every one of those points radiates the
> contaminant outward. So clean the contact points — do not waste time on the wrong places. Concentrate the
> effort near the highest points where the system makes contact. The system makes those contacts, and it tracks
> them. So: nozzles. Bingo.*

This is a **prioritization law for maintenance and for attention.** It says contamination is not uniform — it is
*sourced at the points where metal meets product*, and it spreads from there. The job is not to clean
everywhere; the job is to find the highest‑contact sources and clean *those*. Everything downstream is a shadow
of an upstream contact.

## Why it is exactly right for Hˢ (the three locks)

**1. The contact points are the source nodes of the composition.** Each place the machine touches product —
nozzle tip, squeegee edge, pick head, valve seat, feeder pocket — is a *source* in the line's compositional
graph. A fault there does not stay there; it *radiates* into every deposit and placement that touches it. That
is precisely the ratio‑drift Hˢ reads: a contaminated/clogged contact point moves the **ratios** of every
deposit it touches, together, before any one channel trips.

**2. The machine already counts its own contacts — the contamination map is free telemetry.** Every pick, every
shot, every placement, every wipe is logged. Pick counts per nozzle, shots per valve, placements per head — the
machine *knows* where it touched product and how often. **You do not have to go measure the contamination map;
it is already in the data** (the carrier again — the control is in the data). The contact registry *is* the
priority list.

**3. Weight the read by contact frequency — that is the helmsman, sharpened.** The parts of the budget that
touch product most often are the parts whose ratio‑drift matters most and shows earliest. So Hˢ should not read
every node with equal weight: it should **weight compositional attention by contact count**. The arrow then
points not just to *what* is drifting but to *the highest‑leverage place to act*. This is Pareto made
deterministic: a few contact points carry most of the contamination risk, the machine tells you which, and Hˢ
ranks them.

> **Nozzles, bingo** is the doctrine's own proof: the nozzle is the highest‑contact, highest‑radiation node, so
> it is exactly where the silent‑drift demo flagged first (`dispense_drift.py` — clog caught 20 deposits early,
> arrow → voids). The math found what 35 years on the line already knew.

## The contact‑weighted read (the rule, made quantitative)

For each contact point *i*, let *cᵢ* = contacts since last clean (from the machine log), and let *dᵢ* = the
log‑ratio drift Hˢ reads at the compositions that point sources. Rank maintenance effort by the **radiated‑risk
score**

```
    Rᵢ  =  cᵢ · dᵢ          ( contact frequency  ×  compositional drift )
```

- *cᵢ* alone is the old way — clean by schedule/usage; blind to whether a point is actually drifting.
- *dᵢ* alone is drift‑only — catches the fault but not *how far it radiates*.
- *cᵢ·dᵢ* is the doctrine: **a drifting point that touches product often is the emergency; a drifting point that
  rarely touches product can wait.** Effort goes where contamination is both *present* and *spreading*.

*Measured anchor (`contact_point_priority.py`, receipt `ae19158b`):* a small line of contact points with
real‑shaped contact counts, built with two deliberate decoys — a **busy‑but‑clean** squeegee (9000 contacts,
no real drift) and a **drifting‑but‑low‑contact** fiducial camera (big drift, touches product rarely) — plus a
genuine **nozzle clog** (6000 contacts, real drift). The result:

| plan | cleans first | points cleaned before reaching the real fault |
|---|---|---|
| uniform (clean everything) | the busy squeegee | 2 |
| counts‑only (schedule/usage) | the busy squeegee — *wasted* | 2 |
| drift‑only (chase the wobble) | the fiducial cam — *barely radiates* | 2 |
| **Rᵢ = cᵢ·dᵢ (the doctrine)** | **the nozzle — correct** | **1** |

Counts‑only is fooled by the busy clean point; drift‑only is fooled by the dramatic but low‑contact point; only
the contact‑weighted score sends the crew to the nozzle first. *The doctrine is the only rule that gets it right
on the first clean.*

## How it changes the build (one line per layer)

- **Edge node:** ingest the machine's **contact counts** alongside the process streams; compose; read drift;
  emit *Rᵢ = cᵢ·dᵢ* per contact point — a ranked clean‑list, not a flat alarm.
- **Line node:** the worst contact point across cells is the worst *Rᵢ*, hash‑verified — the conductor points
  the crew at one nozzle, not a shift of blind cleaning.
- **Operator HMI / Breaker 16:** the advisory is *"clean here first"* with the receipt; the gated nudge (if
  armed) backs off the most‑radiating point first. The human still decides; the doctrine just aims the effort.

## Honest scope

- **T1 (measured):** the silent‑drift early flag at the highest‑contact node (`dispense_drift.py`); the
  contact‑weighted ranking demo (`contact_point_priority.py`).
- **T2 (reasoned):** the contact‑registry tap and the *Rᵢ* prioritization on real line logs — sound, planning,
  to run on real pick/shot/placement counts.
- **T3 (to earn):** any deployment; any vendor relationship — none implied. Read‑only first; operator holds
  Breaker 16; Hˢ aims the effort, it does not run the machine.

*Cross‑refs: `README.md`, `CONCEPT_AND_MATH.md`, `NORDSON_CASE.md`, `FUJI_SMT_CASE.md`,
`PHYSICAL_IMPLEMENTATION.md`, `ONBOARDING_FROM_ZERO.md`, `../../library/THE_DATA_IS_THE_CARRIER.md`,
`../../library/THE_BLINDNESS_SUITE.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — numbers cited‑or‑fenced · math proven + receipted · value shown · experts decide.*
