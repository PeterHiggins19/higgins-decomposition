# PNT, timing & the GNSS signal as a composition — the navigation arm

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. Seed/concept —
2026‑06‑20. The positioning/navigation/timing (PNT) extension of the constellation study. **Vision +
honest grounding.** The genuinely‑compositional PNT layers are real and well‑understood; the embedded
transmitter/receiver controller is a **horizon (T3+)**. Relativistic and signal‑structure facts quoted
here are standard references, not Hˢ results.*

---

## 0. The vision (Peter's framing)

A full‑depth navigation system in which Hˢ lives in **both the transmitter and the receiver** as a
**compositional controller** — reading every composition in the chain (the signal, the error budget, the
timing ensemble, the relativistic time/space corrections, the satellite geometry, the fleet) and holding
the whole system to its design goal: **total systems coherence, at scale and depth**. From space weather
to exact location to system performance and longevity, one deterministic, auditable coherence layer
watching everything — and feeding science back to the world that improves the very system producing it.

This document keeps that vision intact while marking honestly **what is already compositional and real**,
**what Hˢ could add**, and **what is horizon**.

## 1. Why this is not fantasy: LEO‑PNT is already real (but immature)

Using LEO constellations — Starlink included — for positioning/navigation/timing is an **active research
frontier** ("LEO‑PNT", or signals‑of‑opportunity navigation). Demonstrated advantages over traditional
MEO‑GNSS: far more satellites, favorable **dilution of precision (DOP)**, much higher received signal
power, and rich **Doppler** observables; published experiments have reached **meter‑level** positioning
from Starlink signals alone. The honest gap: **there is no commercial LEO‑PNT solution yet and no unified
framework** for it. A deterministic, fleet‑coherent, hash‑receipted compositional layer is exactly the
kind of unifying framework that gap calls for — which is why this arm belongs in the study. **[T2** the
field is real; **T3** the Hˢ role.] (Refs: ION/Inside GNSS/IEEE LEO‑PNT literature, 2021→2026.)

## 2. Where PNT is *genuinely* compositional (the honest hooks)

"The signal is a composition" is only worth saying where it is **true**. Several layers of the PNT chain
are compositional in the exact, conserved‑budget sense Hˢ was built for — parts of a whole carrying
relative information:

| layer | the composition | why it's compositional | Hˢ relevance |
|---|---|---|---|
| **GNSS error budget (UERE)** | shares of total range error: ionosphere, troposphere, ephemeris, satellite clock, multipath, receiver noise | the parts sum to a budget; what matters is the *ratios* and which term is steering the error | the loudspeaker‑energy‑budget pattern exactly — MC‑4 composition monitoring |
| **Timescale / clock ensemble** | a weighted combination of many atomic clocks → one paper timescale (e.g. a TAI‑style ensemble) | each clock contributes a *share* of the ensemble; weights are a closed composition | deterministic, coherence‑weighted ensembling + drift/anomaly detection |
| **Satellite geometry / DOP** | the active set of satellites used in a fix and their relative geometry | DOP is a purely *relative* geometric quantity; the set is a composition of viewing directions | the ILR/quaternion relative‑geometry reading; fleet‑coherence at the fix level |
| **Multi‑constellation / multi‑frequency fusion** | combining GPS+Galileo+…×L1/L2/L5 (and LEO) measurements | the fix is a weighted blend of a *set* of measurement sources | deterministic, auditable fusion weights with provenance |
| **Signal power allocation** | how transmit power is apportioned across carrier / code / data / signal components | a fixed power budget apportioned across components — a conserved‑total composition | budget‑coherence monitoring on‑board |

These are not metaphors. The **error budget** and the **clock ensemble** in particular are textbook
compositions, and they are the two places where Hˢ's "which carrier is steering the change, and is it real
or a fault" reading maps most directly. **[T2]**

## 3. Relativistic time & space — honestly

GPS is the canonical real‑world relativity application. Each satellite clock runs fast relative to the
ground by a **net ~+38 μs/day** — about **+45 μs/day** from the gravitational potential (general
relativity) minus **~7 μs/day** from orbital velocity (special relativity) — and is corrected by offsetting
the broadcast clock frequency, plus a periodic **eccentricity** term. These corrections are **exact,
analytic, and already solved**.

**Honest broker point:** Hˢ does **not** improve relativistic physics — there is nothing to improve; the
corrections are exact. What a compositional layer *can* offer is (a) a **deterministic, hash‑receipted
framework** that carries the relativistic, clock, and atmospheric corrections as an auditable *composition
of contributions* to the timing solution, and (b) **fleet‑coherence monitoring** of how those correction
terms behave across the constellation — catching, deterministically, when a clock or a correction term
drifts out of fleet coherence. The relativity stays the physicists'; the **coherent, auditable bookkeeping
of the whole correction composition** is the contribution. **[T3]**

## 4. The tight dual‑use loop — *the error you correct is the science you measure*

This is the heart of why your loop closes. In GNSS, the **two largest correctable error terms are the
ionosphere and the troposphere** — and those same two terms are **established atmospheric science
signals**:

- **Ionosphere → Total Electron Content (TEC).** Dual‑frequency GNSS measures ionospheric delay directly;
  TEC mapping and GNSS **radio occultation** (COSMIC‑class) are mature ionosphere/space‑weather sensing
  methods.
- **Troposphere → precipitable water vapor.** Ground‑based GNSS **meteorology** turns the tropospheric
  (zenith wet) delay into water‑vapor estimates used in operational weather.

So the *same compositional decomposition* that sharpens a position fix (apportioning the error budget,
isolating the ionospheric and tropospheric shares) **is** atmospheric measurement. Correcting the error
and producing the science are the **same operation** read two ways. That is the cleanest possible form of
the feedback loop you described: better positioning ⇄ better atmospheric science, each improving the other,
both falling out of one deterministic compositional read. This is the strongest *honest* statement in the
whole constellation study — and it is **established physics**, only the deterministic/fleet‑coherent
*framing* is the proposal. **[T2** the science exists; **T3** the Hˢ unification.]

## 5. Hˢ in the transmitter and the receiver (the horizon)

Your boldest move — Hˢ embedded in **both ends** as compositional controllers — is the horizon. Honestly
tiered **[T3+]**:

- **In the receiver:** a deterministic, auditable layer that reads the measurement composition (which
  satellites, which frequencies, the live error‑budget shares, the geometry) and maintains a coherent,
  receipted fix — with a guard layer that *refuses a confident position* when the composition does not
  support one (a safety property civilian and safety‑of‑life PNT both want). Complement to, not replacement
  of, the Kalman/least‑squares estimator that already does the fix.
- **In the transmitter / satellite:** an on‑board compositional controller maintaining the signal‑power
  and timing‑correction budgets in fleet coherence, emitting hash‑receipted health/coherence state.
- **Across both:** a single coherence discipline spanning emit → propagate → receive, so the *whole PNT
  chain* shares one deterministic, auditable provenance.

**What is honestly true today:** none of this is built or demonstrated; embedded real‑time deployment is a
long road; and the established estimators are very good. **What Hˢ uniquely brings to the proposal:**
determinism + hash‑receipted provenance + a coherence/guard discipline across the chain — the auditability
and total‑systems‑coherence properties, not a claim of better point accuracy. **[T3+]**

## 6. Total systems coherence as the design goal

The through‑line — from the loudspeaker ground state to the constellation — is **coherence**: a conserved
whole, apportioned across parts, held consistent at every scale. The PNT vision is that principle taken to
full depth, recursively and all hash‑receipted:

```
signal components (power/code/carrier budget)
  → receiver measurement composition (sats × frequencies × error shares)
    → the fix (relative geometry / DOP)
      → the satellite (clock + relativistic + signal budgets)
        → the fleet (Fleet Coherence Index)
          → constellation‑of‑constellations (multi‑GNSS + LEO)
            → the Earth system (ionosphere / troposphere / space weather)
```

Each arrow is a composition; each level can carry a receipt; the same engine reads all of them. That
recursive, self‑similar structure — Hˢ reading compositions of compositions — is the project's deepest
appeal and its hardest challenge, which is exactly why you like it: it has the complexity to *challenge*
the instrument while feeding value back to both the operator and science. **[T3** as a deployed system;
**T2** that the structure is genuinely recursive‑compositional.]

## 7. Honest assessment & claim tiers

- **T1 (measured):** only the underlying Hˢ engine facts (P1) — D=4 exactness, O(log D) reconstruction,
  determinism, receipts, HS‑EPS‑1.
- **T2 (reasoned / established):** the genuinely‑compositional PNT layers (error budget, clock ensemble,
  geometry/DOP, fusion, power budget); the error‑is‑the‑science loop (GNSS‑RO, TEC, GNSS‑met are mature);
  LEO‑PNT as a real, immature field.
- **T3 / T3+ (exploratory / horizon):** every claim that Hˢ *improves* PNT accuracy, longevity, or
  performance; the embedded transmitter/receiver controllers; "total systems coherence" as a deployed
  property; any quantitative figure. **No numbers are asserted.**

**What is NOT claimed:** that Hˢ improves relativistic corrections or replaces GNSS estimators/Kalman
filters; that embedded deployment exists or is near; that any positioning‑accuracy gain has been shown;
that SpaceX is engaged or approached. The value proposition is **determinism, auditability, and
fleet‑level coherence** across the PNT composition — not a claim of better point accuracy.

## 8. The first honest demonstration (public data)

Concrete, fundable, public‑only first steps that would move pieces of this from T3 toward T1:

1. **Compositional GNSS error‑budget read** — from a public reference‑station dataset (e.g. IGS),
   decompose the UERE into its component shares over time and show Hˢ's MC‑4 reading identifies *which*
   term steers an error event (ionospheric storm vs multipath vs clock), deterministically and receipted.
2. **Clock‑ensemble coherence** — on public timing/clock data, read the ensemble as a composition and
   demonstrate deterministic, coherence‑weighted drift/anomaly detection.
3. **Ionospheric TEC as the dual‑use product** — show that the ionospheric *error share* extracted in (1)
   is itself a usable space‑weather (TEC) signal — the loop closing in one dataset.

Any one of these, run reproducibly with a content receipt, is the bridge from "interesting idea and some
down‑to‑earth thinking" to a result a paper and a detailed repo can stand on — which, as you said, is what
makes it fly.

---

*Cross‑refs: [`CONCEPT_AND_VALUE.md`](CONCEPT_AND_VALUE.md), [`FLEET_COHERENCE_METRIC.md`](FLEET_COHERENCE_METRIC.md),
[`ENVIRONMENTAL_SENSING.md`](ENVIRONMENTAL_SENSING.md), [`DATA_AND_SOURCES.md`](DATA_AND_SOURCES.md),
[`PAPER_SEED.md`](PAPER_SEED.md). LEO‑PNT context: ION NAVIGATION / Inside GNSS / IEEE surveys (2021–2026).
Complement, not replacement. Peter Higgins is the sole gate; no external engagement is implied.*
