# The read‑only pilot kit — turn "a pilot" into a one‑page runbook (INTERNAL · REUSABLE)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑24. The reusable,
boundary‑respecting kit that makes a real Hˢ pilot trivial to start on **any** industrial line — the concrete
"help what can be helped" for the deployment future. It builds *readiness*; it does not cross the gate (a pilot
needs a partner's data and Peter's gate). Honest‑broker; Peter is the sole gate; nothing transmitted.*

---

## Why this exists

The forward‑goal triage (`../huf-gov/doctrine/future_target.py`, `22d1652c`) found one thing that is *ours* to
make more ready: a **pilot**. We cannot run it (it needs real partner data), but we can build the **kit** so that
the moment a partner and the gate say yes, the pilot starts the same day. This is support to the fullest the
boundary allows — readiness, not action.

## The decisive test (one sentence)

> Tap one line's **existing** telemetry, read it as a composition with Hˢ, and check — against the partner's own
> recorded events — whether the **ratio drift flags earlier than the single‑channel alarm, and points the right
> way.** If yes, it converts the case from Tier 2 to Tier 1. If no, that is information too.

## The runbook (read‑only; one cell, one week)

1. **Pick one cell + one budget.** A single tool/line and one conserved budget to read (e.g. dispense
   `{volume, height, footprint, voids}`; EUV `{OK, missing, bridge}`; a fiber/FBG channel set; a cell‑health
   budget). Smallest scope that has a real failure history.
2. **Tap, read‑only.** Pull what the machine already emits — SECS/GEM, OPC‑UA, MQTT, CSV/log exports, or
   inspection/metrology/source output. **No new hardware; no actuation.**
3. **Compose → read → receipt.** closure → log‑ratio → kinematic read → coherence gate → SHA‑256 receipt. Emit the
   sentence: `ARROW · CHARACTER · EFF‑DIM · COHERENCE · RECEIPT`.
4. **Score against truth.** Line up the silent‑drift flags with the partner's **real maintenance / excursion
   records.** Measure: **lead time** (how early), **direction accuracy** (right arrow), **false‑positive rate**.
5. **Report honestly.** One page: the three metrics, the receipts, and a plain yes/no on the decisive test —
   including a clean "no" if that is what the data says.

## What the partner provides / what we provide

| partner provides | we provide |
|---|---|
| one cell's existing telemetry (read‑only) + its real event history | the engine, the runner, the conformance suite, the read, the receipts, the scoring, the report |

## Success / kill criteria (set before the run)

- **Pass:** the ratio flag leads the single‑channel alarm by a meaningful margin on the partner's own events,
  with acceptable false positives and correct direction.
- **Inconclusive:** lead present but within noise → extend the window / add parts.
- **Kill:** no lead, or false positives dominate → the read does not help this process; say so and stop. *A clean
  kill is a real result — the honest‑broker line holds.*

## The boundary (what this kit does NOT do)

- **No actuation, no control of record.** Read‑only; advisory only; the operator holds Breaker 16.
- **No data leaves the partner.** Instrument‑not‑data; we read where it lives; we keep receipts, not datasets.
- **No contact, no sending.** This kit is *ready*; using it requires a partner and **Peter's gate.**
- **No sensitive‑field deployment** without the export/steward route (`../huf-gov/doctrine/EXPORT_AND_TRANSFER_GOVERNANCE.md`).

## Honest scope

- **T1:** the engine + the receipted demos this kit reuses (EUV `877516b6`, dispense `cf9bf72f`, fiber `e791ec63`,
  coherence `a5ceab9e`).
- **T2:** the runbook and the metrics — sound, unbuilt on a real partner line.
- **T3:** the pilot's outcome — *unmeasured until run; could pass, be inconclusive, or kill.* Not advice.

*Cross‑refs: `../huf-gov/doctrine/TARGET_THE_FUTURE.md`, `electronics-assembly-smt/PHYSICAL_IMPLEMENTATION.md`,
`euv-lithography/INDUSTRY_IMPACT_AND_OFFERING.md`, `canada-program/ALL_IN_ONE_PACKAGE.md`. Peter is the sole gate;
nothing posted.*

*Proof & Honesty Standard — read‑only · scored against real events · a clean kill is a result · the human decides.*
