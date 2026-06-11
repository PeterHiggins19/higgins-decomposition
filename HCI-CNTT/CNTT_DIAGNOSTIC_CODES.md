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

## 7 · Claim tiers
- **Tier 1 (verified):** the code generator emits the documented codes on real runs; the automated NULL flag fires on the real Crohn null (p=0.78) and the SEP flag on a separated case; the FDIR/lifecycle codes fire correctly.
- **Tier 2 (sound):** the SS‑CCC‑LLL taxonomy and structural‑mode logic, faithful to `hs_codes.py v1.2`, adapted to the CN‑TT stages.
- **Tier 3 (to earn):** full coverage parity with the original 76 codes; per‑domain code wrappers; the `group_separation` metric/threshold calibration on real labeled contrasts.

*Lineage: `hs_codes.py v1.2` / `docs/Hs_Diagnostic_Code_Reference`. The instrument reads, and now it says — in codes — what it found, including when it found nothing, which is the finding that moves the work forward.*
