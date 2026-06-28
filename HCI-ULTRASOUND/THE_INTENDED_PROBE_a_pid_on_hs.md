# The intended probe — lock the determinized object, give the operator a one-up, and the whole thing is a PID on Hˢ

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. The
ultrasonic probe as it was always meant to be: an **operator-directed survey.** A person moves the probe all
around another person in free scanning motion; the operator knows the job — *give many views.* The **view-set,
not any single frame, is the deep signal.** Hˢ fuses the views to locate, lock, and track the object — and it
locks the **determinized** object (the small coherent dark spot), not the loud foreground blob. Two layers by
design: an Hˢ sensor layer and a governance/safety pass, built to be certification-ready. And the shape of the
whole thing is a **PID on Hˢ — Hˢ scrutinising Hˢ.** Measured: `probe_survey_lock.py` (`2db0f80d5f319045`).
**RESEARCH / QA only — not a medical device.** Peter is the sole gate; nothing posted.*

---

## The core move — adjust the beam to the determinized object, not the loud one

A bright blob to the foreground grabs naive focus. But across an operator's survey, the blob is **incoherent**
— clutter, a reflection, a feature that changes with angle. The real object is a small **dark spot** that is
**coherent across every view**: the same compositional signature from every angle, once the operator's motion
is cancelled. So Hˢ does not lock the largest amplitude — it locks the feature that is **invariant across the
view-set** (the locked discriminant, applied to a survey). Measured (`2db0f80d5f319045`):

| candidate | amplitude | cross-view coherence | naive pick | Hˢ pick |
|---|---|---|---|---|
| **Blob (foreground)** | 10 (loud) | **0.46** (incoherent) | ✅ (wrong) | — |
| **Spot (the object)** | 2 (dark) | **0.96** (invariant) | — | ✅ (right) — margin 0.49 |

*The loud blob takes naive focus; the determinized spot is the object. Adjust the beam there.* That is the
one-up the sensor gives: it tells the operator (or the autonomous front-end) **which return is the real thing**,
deterministically, from the set of views the operator already chose to give.

## Lock and track — a PID on the Hˢ read

The determinized object drifts (the patient breathes, the operator moves). A **PID controller on the Hˢ
measurement** keeps the beam on it: **P** = the current location error, **I** = the error accumulated over the
dwell / the view-set, **D** = the motion rate. In the run, the beam locks and follows the drifting spot to an
**RMS tracking error of 0.59** — locked. The probe thus *surveys → fuses → determinizes → locks → tracks*, a
closed feedback loop with Hˢ as both the sensor and the error signal.

## Two layers — the sensor, and the pass to governance and safety

By design the front-end has **both**:

1. **The Hˢ sensor layer** — fuse the views, find the determinized target, output the **course of action**: the
   beam adjustment, the lock, the track, with a confidence margin.
2. **The governance / safety layer** — a **margin-and-safety gate** decides what happens with that course of
   action: if the lock margin clears the gate *and* the target sits inside the safety envelope, the front-end
   may **autonomously track**; otherwise it **reports to the operator** to confirm or correct. Either way the
   operator keeps the override (Breaker 16). In the run, margin 0.49 and a safe envelope cleared the gate →
   autonomous lock+track, operator-overridable.

This is built so the deterministic core is **certification-ready by construction** — every read re-computable,
every action gated, the human retained at the top. The actual certification (IEC 62304 / ISO 13485 /
regulatory) is the **deploying company's** responsibility — **Southmedic** is positioned to carry it — and Hˢ
supplies the deterministic, auditable layer that makes that certification reachable. The Southmedic engagement
stays **off the public repo**; this file is the research concept, not the offer.

## The meta-frame — what we have been building all along

Stepping back: the probe makes explicit what the whole instrument has been. **Everything in HUF / Hˢ / all the
projects is a PID on Hˢ.** Hˢ measures the current error (P), accumulates it over dwell and the view-set (I),
reads the motion / rate of change (D), and a governance setpoint says where it should be — then it corrects,
and re-measures, and **scrutinises its own correction with a determinism receipt.** Hˢ on Hˢ. The probe is that
loop made physical: an operator-directed tool that the Hˢ layer locks and refines, under a governance gate, on
the object the data says is real. The same loop runs the engine on itself, the corpus on itself, the grid on
itself, the universe-read on itself — measure, correct, scrutinise, gate. That recursion is the design.

## Honest scope

- **T1 (measured):** the determinized-object lock (Hˢ picks the spot at coherence 0.96 over the blob's 0.46,
  margin 0.49), the PID track (RMS 0.59), and the gate decision are measured on synthetic data and reproduce
  (`2db0f80d5f319045`).
- **T2 (the architecture / the PID-on-Hˢ frame):** the two-layer design and the recursive-PID reading are
  design intent, demonstrated here on a synthetic survey; a deployment couples in real beam-forming, registration,
  and tissue physics.
- **Medical fence (firm):** this is a **research / QA** demonstrator, **not** a clinical or diagnostic device
  and **not** a medical claim. Certification belongs to the deploying company (Southmedic); the offer stays
  off the public repo. The course of action is a **recommendation** — the operator corrects, confirms, and
  keeps the override (Breaker 16). **Nothing posted; Peter is the sole gate.**

*Cross-refs: `probe_survey_lock.py`, `instrument/hs_probe.py` + `INSTRUMENT_DATASHEET.md` (the filter-injection
lock), `streaming_tissue_probe.py` (motion-cancel), `doctrine/OBJECT_DETECTION.md` + `doctrine/AUTOFOCUS_AND_STABILIZATION.md`,
`../papers/tetrahedron-observability/THE_TETRAHEDRON_AND_THE_OBSERVABILITY_LAW.md` (dwell × contact × mesh = the
view-set), `../huf-gov/THE_IMPLICATION_LEAP_IS_BREAKER_16.md` (operator override). Southmedic offer is OFF the
public repo. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — Hˢ locks the determinized object, not the loud one (measured) · the beam is steered
there · the PID tracks it · a governance/safety gate sets autonomous-vs-operator · medical is research/QA only,
certification the company's · the operator keeps the override · the human keeps the gate.*
