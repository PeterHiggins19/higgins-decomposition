# The streaming tissue probe — lock fine structure, cancel motion, climb to max Q

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. How an
**existing animal-tissue ultrasound study** feeds the probe to lock onto the smallest details in a
**streaming, real-time** instrument — cancelling relative probe/patient motion so the patient can hold a
relaxed posture, emitting positional and temporal coherence control signals, and climbing the resolution
ladder to the system's own coherence limit (**max Q**). Measured on a grounded model; receipt
`f7fc1cc1cdf5203b`. **RESEARCH INSTRUMENT ONLY — not diagnostic or clinical.** Honest-broker tiered; Peter is
the sole gate; nothing posted.*

---

## How an existing ultrasound study plugs in

Public animal-tissue / phantom / in-vivo ultrasound studies already publish the raw material this probe
needs: **RF or IQ returns** — for example the **PICMUS** plane-wave dataset (IEEE IUS 2016: simulation +
CIRS multi-purpose phantom in-vitro + in-vivo carotid) and the **CUBDL** open subsets (INS, MYO, UFL, JHU,
TSH). Each return, over depth and frequency, is turned into a **per-band scattering-power composition** —
parts of one budget. That composition is the probe's input. No new acquisition is required to begin: an
existing study's RF frames *are* a stream of compositions the probe can read today (as a research re-analysis
of public data).

## Reading it: the differential locks onto structure

The probe reads each frame's composition **against a known reference** (an injected filter, or a baseline
template) in log-ratio space: `z = clr(return) − clr(reference)`. That single move does three things at once,
because `clr(g·x) = clr(x)`:

### 1 · Relative motion is cancelled — the patient can relax

When the probe moves and the patient moves, the dominant artifact is a **rigid relative motion** — a shared
change in coupling, beam-tissue alignment, and overall return level. In the composition that is a
**multiplicative common-mode**, and clr **reciprocates it away exactly.** *Measured: under a 25× relative-motion
swing, the structure read held to within 22.2 dB more stability than an absolute read.* So the instrument
reads **structure, not pose** — the patient does not have to be clamped rigidly still; they can be positioned
for comfort, and as both the probe and the patient move, the relative motion cancels and the structure read
persists. (Honest limit below.)

### 2 · Streaming climbs the resolution ladder to the system's own limit (max Q)

A stream is many frames. Averaging the differential over accumulating frames drops the decorrelation noise
~`1/√N`, so **finer and finer detail rises above the floor in real time** — the max-power ladder, climbed by
time instead of by a bigger sensor. *Measured climb (the smallest detail is `clr ≈ 0.03`):*

| frames | noise floor | features resolved |
|---|---|---|
| 1 | 0.060 | 1 (coarsest) |
| 4 | 0.030 | 2 |
| 16 | 0.015 | 3 |
| **64** | **0.008** | **4 — down to the finest 0.03 detail** |
| 256 | 0.008 | asymptote — **no further gain** |
| 1024 | 0.008 | asymptote |

The climb **stops at the coherence floor** (`0.008` here) — the irreducible out-of-plane decorrelation, the
**max-Q limit of the system itself.** Past that, more frames buy nothing: the instrument has reached *the
resolution of its own limits*, and it knows it. That is the honest ceiling the max-power doctrine demands —
the probe descends as far as the coherence supports, and not one part finer.

### 3 · Positional + temporal coherence control signals

Each frame the probe emits, as a by-product of the same read:

- a **coherence read-back** (a Q proxy) = the lock quality; the instrument flags `lock = false` when it drops
  (measured: it correctly de-asserts lock when coherence falls below 0.8);
- the **estimated rigid drift** (`log g`) — the relative-motion component, the input to an **SE(3)
  registration / mapping** channel (the SO(4)/dual-quaternion pose work) so the probe can *map* as it is
  moved;
- a **temporal-coherence** flag for frame-to-frame consistency (when to integrate, when motion is too fast).

These turn the probe into a guided, self-aware capture: it tells the operator (or the autocapture loop) when
it is locked, how the geometry is drifting, and when the stream is coherent enough to climb further.

## The honest fences (what does *not* cancel)

- **Non-rigid deformation is NOT cancelled — and must not be.** A real shear/compression that changes the
  tissue's actual structure is *signal*, and the probe **detects it** (measured: a deformation at one band
  survives the common-mode rejection and is flagged). The instrument cancels *motion*, not *change*.
- **Out-of-plane decorrelation is the floor.** It is independent across bands and does not average away
  below the coherence limit — that is the max-Q ceiling, stated plainly.
- **Tiers:** the common-mode/motion cancellation is **T1 exact**; the tissue physics here is a **grounded
  model (T2)** — real RF data (PICMUS/CUBDL) re-analysis is the next rung; any clinical/diagnostic use is
  **T3 and gated by medical validation** (IEC 62304 / ISO 13485 / clearance). This reads compositions; it
  does not make medical decisions.

## What it offers that was not available before

More of the return is now *knowable*: the same RF stream, read differentially, yields fine structure that an
absolute read loses to coupling and motion — captured in real time, with the patient relaxed, with the
geometry tracked, and with an honest, coherence-set limit on how fine it can go. The instrument shows more
because it stops throwing away the ratios — and it climbs to exactly the resolution its own coherence allows,
no further.

*Cross-refs: `streaming_tissue_probe.py`, `STREAMING_TISSUE_PROBE_RESULTS.json`, `instrument/hs_probe.py`,
`THE_FILTER_INJECTION_PROBE.md`, `../library/max_power_hs.py` (the ladder), `../library/KNOW_THE_KNOWABLE.md`
(max Q), `../library/THE_Q_CONNECTION.md`, `../triad-backbone/THE_TRIAD_BACKBONE.md`. Peter is the sole gate;
nothing posted.*

*Proof & Honesty Standard — motion cancels exactly · real change is kept · the climb stops at max Q · medical use is fenced · experts decide.*
