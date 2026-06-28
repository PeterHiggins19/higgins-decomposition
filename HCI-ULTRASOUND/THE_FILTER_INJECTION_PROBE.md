# The filter-injection probe — lock onto structure by reading the return against the injection

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. The real
test of the differential engine, made physical in its canonical home (HCI-ULTRASOUND): **inject a known
filter signal to cause a diagnostic probe, then read the return as perturbed relative to what was injected —
and the perturbation, in log-ratio space, is the structure.** Measured; receipt `50b090f83c6df461`.
Honest-broker tiered; Peter is the sole gate; nothing posted.*

---

## The idea (Peter's words, made operational)

> Use **filter injection of known properties** to cause a desired, diagnostic probe signal into a
> sub-component, and **lock onto its structure** by reading the **return as perturbed relative to the
> injected**, using Hˢ.

This is the P2 differential engine (knock-and-read against a known reference) realized as a non-contact
ultrasonic probe — and it sits directly on the existing lineage: the **geometry-lock probe** and
**inert / Paired-Measurement** doctrine of HCI-ULTRASOUND, and AN-001's law that the read *"cancels by
reciprocation; clr is the differential, reciprocal-antisymmetric."*

## The mechanism

A non-contact probe injects a **known** spectral composition `s_inj` (a flat/white filter is maximally
diagnostic — any return deviation is then pure structure). The sub-component (DUT) perturbs it through its
structural power transfer function `|H(f)|²` — a geometry resonance, plus a flaw resonance if it is damaged.
The measured return is

```
   return(f) = s_inj(f) · |H(f)|² · g   (+ noise)
```

where `g` is the **nuisance common-mode** — overall source level × couplant efficiency — the classic bane of
ultrasonic NDE, a single scalar that changes on every shot and *fools an absolute reading.*

The Hˢ read is the **reciprocation / clr differential**:

```
   z = clr(closure(return)) − clr(closure(s_inj))   =   clr(|H|²)
```

Because `clr(g·x) = clr(x)`, the scalar common-mode **cancels exactly** — what remains is the pure structure.
*The return, read against the injection in log-ratio space, is the sub-component's structure, with the
coupling/source nuisance reciprocated away.* That is the lock.

## Measured (receipt `50b090f83c6df461`)

A `D=24`-band probe, geometry resonance at band 6, flaw resonance at band 17, with the couplant/source level
`g` varied **0.2–5× (25-fold) shot to shot** — a brutal nuisance:

| test | result |
|---|---|
| **structure recovery** | RMSE to the true `clr(|H|²)` = **0.019** (the independent-noise floor); the differential reconstructs the structure cleanly |
| **geometry lock** | dominant recovered band = **6**, correct — the probe locks onto the component's resonance every time |
| **common-mode rejection** | **31.3 dB** versus an absolute (non-reciprocated) read — the coupling variation is reciprocated away |
| **flaw detection under 25× coupling swing** | Hˢ-differential separability **53.8** vs the absolute read's **1.44** — *Hˢ locks the flaw; the absolute read is swamped by coupling variation* |

The headline: an absolute spectral read cannot tell a flaw from a couplant change — both move the raw return.
The Hˢ differential reads only the *structure*, so it finds the flaw through a 25× coupling swing that blinds
the ordinary read. And it is **non-invasive**: the injection is known, the probe is read-only, it imprints
nothing (inert to the floor).

## Honest fences

- **T1 (exact):** the scalar common-mode cancellation (`clr(g·x)=clr(x)`) — source level and couplant
  efficiency are reciprocated away exactly; this is the same law as the RWA ground-state / AN-001 result.
- **T2 (model):** the ultrasonic physics here is **synthetic** — designed transfer functions and a scalar
  nuisance, not real hardware data. The numbers are model numbers; the *mechanism* is the result.
- **The one real limit:** a **frequency-shaped** nuisance (dispersive attenuation, a sloped coupling) is
  **not** a scalar common-mode and is only partly removed by clr — its shape would confound the structure
  read. That case needs the **Paired-Measurement reference channel** (inject a known reference alongside and
  difference against it), not clr alone. Stated so the win is not overclaimed.
- **T3 (to earn):** run this exact differential on **real** ultrasonic NDE data (a known couplant-variability
  dataset, a real flawed/healthy part pair) and report the measured rejection and detection.

## Why it matters

This is the differential engine passing a concrete, adversarial test: it locks onto a sub-component's
structure through the single biggest nuisance in real ultrasonic inspection, non-invasively, with the
mechanism exact and the limits named. It promotes the P2 seed from "captured connection" toward "measured on
a grounded model" — the next rung being real hardware data.

*Scope & limits (read this for the honest factorization): `THE_HONEST_SCOPE_AND_HOME_DOMAIN.md`.*

*Cross-refs: `ultrasonic_probe_hs.py`, `ULTRASONIC_PROBE_RESULTS.json`, `README.md` (HCI-ULTRASOUND),
`../papers/datasheets/AN-001_DETERMINISTIC_NOISE_REJECTION.md` (reciprocation law),
`../papers/UNWRITTEN_CONNECTIONS_SEEDS.md` (P2 the differential engine),
`../full-engine/THE_FULL_ENGINE_SPECIFICATION.md` (CH-INERT non-invasive channel). Peter is the sole gate;
nothing posted.*

*Proof & Honesty Standard — the cancellation is exact · the physics is a model · the shaped-nuisance limit is named · real-data is the T3 to earn · experts decide.*
