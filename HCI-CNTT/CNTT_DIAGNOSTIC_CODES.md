# CN‑TT v4 — Diagnostic & Error Code System

*2026-06-10. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Revives the original pipeline's code system — `hs_codes.py v1.2` (76 diagnostic codes · 10 structural modes · 5 severity levels · 13 stages; `docs/Hs_Diagnostic_Code_Reference`) — for the tile‑native CN‑TT engine. Implemented in `engine/codes.py`; demonstrated by `engine/self_test/codes_demo.py` (all cases shown). Why this exists: in the early engines a machine‑readable code system for diagnostics and error tracking made advancement much faster — every run reports *what it found and what to do about it*, automatically. The key new capability is the **automated NULL flag**.*

---

## 1 · Format and levels

**`SS‑CCC‑LLL`** — Stage · Condition · Level (e.g. `DX‑NUL‑DIS`).

| Level | Meaning |
|---|---|
| **INF** | Information — normal operation; the step ran and what it measured |
| **WRN** | Warning — a quality threshold missed; interpret with caution |
| **ERR** | Error — input rejected or operation failed; pipeline cannot produce a valid result |
| **DIS** | **Discovery — a noteworthy finding** (the scientific output: regime shifts, separations, **and nulls**) |
| **CAL** | Calibration — the instrument's own precision/limits, not the data's properties |

## 2 · Stages (CN‑TT tile‑native)

`GD` Guard (input validation) · `L1` Ingest/Treat/Calibrate · `L2` Geometry · `L3` Tile/Atlas · `L4` Navigate · `DX` Diagnostics/Result · `SK` Shock (FDIR) · `LC` Lifecycle · `RP` Report.

## 3 · The code table (implemented)

| Code | Level | Fires when |
|---|---|---|
| `GD‑ALL‑INF` | INF | input guards passed; pipeline ran |
| `L2‑CLR‑INF` | INF | closure → CLR → Helmert‑ILR computed |
| `L3‑LSL‑INF` | INF | atlas connected + **lossless** reconstruction (with the error) |
| `L3‑DSJ‑ERR` | ERR | atlas **disjoint** → reconstruction rank‑deficient (overlap missing) |
| `L3‑HID‑CAL` | CAL | **high‑D mode** — O(D²)/combinatorial diagnostics gated off (instrument limit, not data) |
| `L4‑RGB‑DIS` | DIS | regime boundary(ies) detected (with locations) |
| `L4‑DEC‑WRN` | WRN | deceptive‑drift step(s): concentration tightening while motion stays quiet |
| `L4‑HVO‑WRN` | WRN | volatile helmsman (low stability) — dominant driver changing often |
| `DX‑ATR‑DIS` | DIS | period‑2 limit cycle fitted |
| `DX‑IRC‑INF` | INF | IR class (damping regime) |
| **`DX‑SEP‑DIS`** | DIS | **group separation detected** on the chosen metric (p < threshold) |
| **`DX‑NUL‑DIS`** | DIS | **NULL: no separation** (p ≥ threshold) — the global read is insufficient; a targeted signature is indicated |
| `SK‑EXT‑INF` | INF | EXTERNAL shock — real change; channels coherent (with magnitude) |
| `SK‑INT‑ERR` | ERR | INTERNAL fault — **isolated to a channel** |
| `SK‑UND‑CAL` | CAL | shock class undetermined — no redundancy (needs ≥2 channels) |
| `RP‑DET‑INF` / `RP‑VER‑INF` / `RP‑SHA‑INF` | INF | deterministic rerun · engine version · content hash |

## 4 · Structural modes (second‑order reads of the code pattern)

Fired by `requires`/`forbids` logic over the emitted codes (the original's mechanism):

- `SM‑CLN‑INF` — clean lossless deterministic run (well‑behaved).
- `SM‑MCA‑WRN` — **missing/untracked carrier**: atlas disjoint → information leaking to an untracked part; add the carrier and re‑run. *(The original's "missing carrier" mode.)*
- **`SM‑NUL‑DIS`** — **NULL RESULT**: the expected separation is absent → ADVANCE via a targeted balance/signature, not a global scalar. *This is a finding, not a failure.*
- `SM‑RGS‑DIS` — regime shift(s) present → segment the trajectory at the boundaries and investigate.
- `SM‑IFT‑ERR` — **internal fault**: a channel diverges → isolate the component and roll back to last‑known‑good.

## 5 · The NULL as the key to advancement (the issue, detailed, and the automation)

**The issue.** When CN‑TT compared Crohn's‑disease vs control samples on effective diversity, it found **no separation** (K_eff 7.31 vs 7.23, p = 0.78). A weaker pipeline would either hide this (report only what separates) or treat it as a failure. It is neither — it is a **discovery**: the global, unsupervised read does **not** carry the contrast, which is precisely the signal that the discriminating structure lives in a **specific balance of taxa**, not a scalar. Nulls bound the problem: they tell you *where not to look*, which is what turns a search into a result. Hidden nulls are how fields waste years; flagged nulls are how they advance.

**Why automate it.** A human noticing a null is slow, inconsistent, and unrecorded. The advancement comes from making it a **coded, machine‑readable, auditable output** that fires every time, the same way, with a recommended next action — exactly what the original code system did for diagnostics, and what sped that work up.

**How it is automated.** `codes.group_separation(comps, labels, metric)` runs the comparison (Mann–Whitney on the metric) and `codes.generate_codes(payload, comparison=…)` emits:
- separation present → **`DX‑SEP‑DIS`** (a discovery to pursue);
- **separation absent → `DX‑NUL‑DIS` + structural mode `SM‑NUL‑DIS`** — the null is now a first‑class, coded, hash‑stamped output with the explicit next step ("advance via a targeted signature"). No human attention required to surface it.

**Demonstrated (real data):** on the actual Crohn comparison the engine auto‑emitted `DX‑NUL‑DIS (p=0.78)` + `SM‑NUL‑DIS`; on a clearly‑separated synthetic case it emitted `DX‑SEP‑DIS (p=1.4e‑14)`. The same generator emits the operational codes (lossless, regime shifts, IR class, determinism) on the Backblaze run, and `SK‑INT‑ERR`/`SM‑IFT‑ERR` on an internal fault.

## 6 · How to use

```python
from engine import codes, run_cntt
payload = run_cntt.run("data.csv")
report  = codes.generate_codes(payload)                       # operational codes + modes
# group comparison -> automated NULL/SEP flag:
cmp = codes.group_separation(closed_comps, group_labels, metric="k_eff")
report = codes.generate_codes(payload, comparison=cmp)
# FDIR shock -> SK codes:
report = codes.generate_codes(payload, shock=shock_verdict)
```
Codes are designed to ride in the emitted payload (`payload["diagnostics"]["codes"]`) and downlink as a compact, deterministic status line a central controller can read.

## 7 · Guard & control‑layer codes (additive, 2026‑06)

The guard modules built this round (`engine/zero_methods.py`, `engine/helmsman_guard.py`, `engine/structural_guards.py`, `engine/loop_control.py`) emit the codes below. They extend the registry so the engine announces the **boundary of what it can honestly resolve**, and the codes a closed loop raises. Full rationale: `ENGINE_CAPABILITIES_DELTA_2026-06.md`. *(Stage‑prefix harmonization — `HM`/`DG` are navigate‑/geometry‑family guard prefixes — is a Tier‑3 tidy; codes are registered here as the modules actually emit them.)*

| Code | Level | Fires when | Module |
|---|---|---|---|
| `GD‑ZRC‑CAL` | CAL | structural‑zero carrier dropped to sub‑composition (was silent `nan`) | zero_methods (E‑21) |
| `GD‑CNC‑CAL` | CAL | constant/degenerate carrier dropped | zero_methods (E‑21) |
| `GD‑ZRP‑CAL` | CAL | detection‑limit zeros: multiplicative replacement applied | zero_methods |
| `GD‑ZBM‑CAL` | CAL | **Bayesian‑multiplicative** zero replacement (count‑aware, ratio‑preserving) | zero_methods |
| `GD‑ZUN‑WRN` | WRN | unresolved zeros — **not imputed** (honest default; flagged) | zero_methods |
| `GD‑SPZ‑WRN` | WRN | **sparsity regime**: zero‑fraction past threshold → CLR geometry is δ‑dominated; densify before the log‑ratio | zero_methods |
| `HM‑NUL‑WRN` | WRN | **no resolvable helmsman** — motion below the floor (at/near barycentre); leader would be noise | helmsman_guard |
| `HM‑TIE‑WRN` | WRN | **helmsman tie** — leader not separated from runner‑up (margin ≤ tol); not broken by index | helmsman_guard |
| `DG‑RNK‑WRN` | WRN | **rank‑deficient trajectory** — motion confined to a subspace (eigh‑instability sibling of E‑21) | structural_guards |
| `MO‑DIF‑WRN` | WRN | **diffuse momentum** — motion present but no coherent *arrow of intent* (the system is churning; `coherence < floor`) | compositional_momentum |
| `MO‑NUL‑WRN` | WRN | **no resolvable momentum** — the composition is at rest (no mass flow to report) | compositional_momentum |
| `FR‑BND‑INF` | INF | **boundary of analysable structure** — entropy not invariant under geometric‑mean decimation (EITT‑as‑boundary; *Tier‑3 fringe, exploratory clue, never a claim*) | fringe_boundary |
| `L4‑HLD‑INF` | INF | **hold‑lock engaged** — motion below the *discovered* noise floor `max(system,engine)`; structural change withheld until sustained (announced, never silent) | structural_guards `hold_lock` *(code emitted when wired to the run path — Peter's gate)* |
| `LC‑WIN‑END` | INF | closed‑loop **automation window exhausted** → graceful revert to OBSERVE | loop_control |
| `LC‑TRIP‑NAN` | ERR | breaker: non‑finite measurement | loop_control |
| `LC‑TRIP‑RATE` | ERR | breaker: fast excursion / instability | loop_control |
| `LC‑TRIP‑WIND` | ERR | breaker: integral windup / runaway drift | loop_control |
| `LC‑TRIP‑SAT` | ERR | breaker: authority saturated too long (fighting the plant) | loop_control |
| `LC‑TRIP‑DOG` | ERR | breaker: watchdog/deadman timeout | loop_control |
| `LC‑ESTOP` | ERR | **manual emergency stop** — latched safe until human `reset()` | loop_control |

These follow the same spirit as the NULL flag: every guard that fires says *what it found and what to do about it*, automatically. The `HM`/`DG`/`GD‑SPZ` family is the engine learning to say **"I cannot honestly resolve this"**; the `LC` family is the engine acting only behind breakers.

## 8 · Claim tiers
- **Tier 1 (verified):** the code generator emits the documented codes on real runs; the automated NULL flag fires on the real Crohn null (p=0.78) and the SEP flag on a separated case; the FDIR/lifecycle codes fire correctly. The guard/control codes in §7 are each emitted + self‑tested by their modules (kill‑tests in `experiments/engine_killtest_2026-06/`); `L4‑HLD‑INF` emission awaits run‑path wiring (Peter's gate).
- **Tier 2 (sound):** the SS‑CCC‑LLL taxonomy and structural‑mode logic, faithful to `hs_codes.py v1.2`, adapted to the CN‑TT stages.
- **Tier 3 (to earn):** full coverage parity with the original 76 codes; per‑domain code wrappers; the `group_separation` metric/threshold calibration on real labeled contrasts.

*Lineage: `hs_codes.py v1.2` / `docs/Hs_Diagnostic_Code_Reference`. The instrument reads, and now it says — in codes — what it found, including when it found nothing, which is the finding that moves the work forward.*
