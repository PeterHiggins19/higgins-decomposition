# Hs — a short primer (method only)

*One page on what the instrument is and does. It contains **no geological claims.** The displays and numbers are yours to read; the meaning is yours to determine, led by the data.*

## What Hs is
**Hs (the Higgins Decomposition)** is a deterministic instrument for **compositional series** — any ordered set of parts-of-a-whole (percentages, ppm, fractions) indexed by something: depth down a core, time, or position along a traverse. It does not model a process; it *reads* the sequence and reports how the composition moves.

Two engines:

- **CNT — Compositional Navigation Tensor.** Reads the ordered compositions on the simplex (closure → centred-log-ratio → orthonormal **ILR** isometry) and reports, **per step**:
  - **Aitchison step** — how big the compositional change is (a proper distance, scale-invariant, subcompositionally coherent);
  - **helmsman** — which part steers that step (largest log-ratio move);
  - **power share / Activation Coefficient** — a "small-part-doing-large-work" detector (*deceptive drift*: a trace component driving structural change out of proportion to its abundance);
  - **K_eff** — the effective number of parts actively in play;
  - **regime tripwire** — where the step series jumps past a robust threshold (candidate boundaries).
- **CNQ — Compositional Navigation Quaternion.** Names the rotational algebra of the path. **Exact (native) at D = 4** — three ILR balances map to a quaternion, giving a **radial magnitude + bearing rotation** per step with no projection loss. (Above D = 4 it is experimental or a declared lossy projection — the claim tier travels with the number.)

**Deterministic and hash-chainable:** same input → same output, every time; runs can be stamped for provenance.

## What Hs does (uses)
It turns an ordered composition into a **navigation record** — *how far* the composition moved, *in which direction*, *which component steered*, *where the regime changed*, and *whether a minor component is doing outsized work*. Typical uses: chemostratigraphy down a core, compositional time-series, spatial/traverse compositional change, and screening for change-points and trace-driven shifts. It **complements** established compositional-data and time-series methods; it does not replace them.

## What Hs is **not** — and the discipline
- It is an **instrument, not an interpreter.** It reports compositional *structure*; it does **not** assign geological (or any domain) meaning.
- Outputs are **research-grade and calibration-gated**. Correlations, thresholds, and "events" are readings to be tested against independent evidence and a domain expert's judgement.
- Claim tiers (**confirmed / experimental / not-implemented**) travel with every output and are never inflated.

## For the geologist
The displays show you **where the composition moves, how much, which element steers, and where regimes change.** What those movements *mean* — surfaces, systems tracts, provenance, sorting, redox, diagenesis, dilution, events — is **for you to determine, led by the data and the displays.** Nothing in this folder is a geological claim; it is an instrument reading awaiting your interpretation.

## Pointers
- Engine: `cnt.py` / `cnq.py` in the Hs repo (this folder is `collaborations/geology-wehner/`).
- Worked demo on real mudstone: `demo_frielingen9/` — fully cited and reproducible (`REPRODUCE.md`).
- Fit assessment for mudstone chemostratigraphy: `MUDSTONE_HS_FIT.md`.

*The instrument reads. The expert decides. The hashes carry the receipts.*
