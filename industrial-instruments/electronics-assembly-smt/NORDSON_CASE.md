# Nordson‑class case — dispense, coat, inspect as compositions (INTERNAL · PLANNING)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑23. Planning
case for applying Hˢ to Nordson‑class fluid‑dispense, conformal‑coating, and test/inspection equipment. **No
contact, partnership, or endorsement implied** — "Nordson‑class" names an equipment domain. Honest‑broker
tiered; nothing posted; Peter is the sole gate.*

---

## 1. Why dispense is the natural fit

Fluid dispense is *literally* compositional. Two compositions live at every shot:

- **Material composition** — solder paste = `{metal, flux, solvent}` shares; adhesive / underfill mixes;
  coating solids. Drift in the *ratios* (flux drying, metal settling) precedes any single‑metric failure.
- **Deposit‑quality composition** — `{volume, height, footprint, voids}` per pad: parts of one deposit's
  quality budget. A clog, a worn nozzle, a pressure drift moves these *together* in the ratios.

The deposit's **geometry** is a deformation read: `F = R·U` → orientation (registration), shape (is it
elongating/slumping), size (volume) — the rotation⊕shape⊕size split.

## 2. The early‑warning result (planning anchor)

A nozzle clog lowers volume and raises voids in concert while each channel is still in spec — the **ratio‑blind
silent drift**. Hˢ reads it in the log‑ratios first. *Measured:* clog flagged at deposit 47, single‑channel
volume alarm at deposit 67 → **20 deposits of lead time**, arrow correctly pointing to *voids* (`ca9e6c0d…`,
`dispense_drift.py`). That lead time is scrap avoided and a maintenance window earned.

## 3. Where Hˢ plugs into Nordson‑class equipment

| Nordson‑class function | the composition Hˢ reads | the value |
|---|---|---|
| jetting / valve dispense | deposit quality budget per pad | silent‑drift clog/wear early warning + auto setpoint nudge (behind Breaker 16) |
| conformal coating | coverage shares `{covered, thin, keep‑out, bridging}` over the board (a sheet) | a deformation/coverage field; uniformity read as a composition |
| fluxing | flux deposit distribution | ratio drift before defect |
| **test & inspection (AOI / X‑ray)** | defect‑class composition `{open, short, void, misalign, …}` per board/lot | the lot's *defect signature in motion* — which class is rising, before yield drops |

## 4. The honest scope

- **T1 (measured):** the dispense silent‑drift early flag and arrow (`ca9e6c0d`).
- **T2 (reasoned):** the coating‑field and inspection‑signature mappings — sound, planning‑stage, to run on
  real dispense/inspection logs.
- **T3 (to earn):** any deployment on real Nordson‑class equipment; any vendor relationship — none implied.
- Hˢ is a **complement** — a second, auditable read on data the machine already produces; it does not control
  the dispenser of record; the operator holds Breaker 16.

*Cross‑refs: `CONCEPT_AND_MATH.md`, `FUJI_SMT_CASE.md`, `PHYSICAL_IMPLEMENTATION.md`,
`../../experiments/deceptive_drift_null_2026-06/` (the silent‑drift null), `../gas-composition-study/` (fluid
compositional precedents). Peter is the sole gate; nothing posted.*
