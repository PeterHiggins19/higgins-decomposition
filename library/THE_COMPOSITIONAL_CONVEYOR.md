# The compositional conveyor — self-packaging, self-routing data, top to bottom

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. The
compositional memory turned into a **live conveyor**: each data unit packages itself into **8-bit form**,
**tags itself**, and **routes itself** through the command chain — fast, buffered, and **native to the
existing pipeline without disruption**. Measured top-down on two real projects already underway. Receipt
`99e6d93555005cc6` (`compositional_conveyor.py`). Honest-broker tiered; Peter is the sole gate; nothing
posted.*

---

## The idea (top level down to the nuts and bolts)

A single layer that rides **inside** the data flow of any compositional project, from the framework at the
top to the nuts-and-bolts sensor at the bottom, doing four things per unit, by itself:

1. **Package itself — 8-bit.** Each composition unit is encoded to one byte per part: the **7-bit clr
   payload** (right-sized, near-lossless, G-239) plus an **8th XOR/parity bit** — the integrity / "how-to-use"
   flag — stripped on decode (`b & 0x7F`), exactly the V∞Core 8th-bit idea.
2. **Tag itself.** The unit's **SHA-256 content hash is its address** — it names itself by what it is
   (content-addressable), so no external registry assigns identity.
3. **Route itself — deterministic command chain.** Two routes fall out for free: a **hash route** (`tag %
   lanes`, for dedup / load-balance) and a **structural route** — the **differential helmsman**
   (`argmax|clr − running baseline|`) — by which the unit **self-sorts to the lane of its dominant regime
   deviation.** Same stream → same routes, on any node.
4. **Move as a conveyor, non-disruptively.** The units flow through a FIFO ring buffer as a stream; the layer
   is **pass-through** — decoding reproduces the original clr to the 7-bit floor, so the source read is
   **preserved, not altered.** It rides alongside the existing pipeline; it does not replace it.

## Measured top-down on two real projects (receipt `99e6d93555005cc6`)

| project (real, already underway) | units | D | bytes/unit | roundtrip clr error | non-disruptive | deterministic | self-sort across lanes (by regime) |
|---|---|---|---|---|---|---|---|
| **GEO — Frielingen-9 mudstone** (Wehner collab; WD-XRF SiO₂/Al₂O₃/Rb/Zr, PANGAEA 897615) | 219 | 4 | 4 | 0.047 (= 7-bit floor) | **yes** | **yes** | 0:10 · 1:51 · 2:39 · 3:119 |
| **ARRAY — Backblaze fleet** (remote sensor array; Mechanical/Thermal/Age failure modes) | 108 | 3 | 3 | 0.047 | **yes** | **yes** | 0:87 · 1:12 · 2:9 |

The same conveyor, unchanged, ran on both — the small terrestrial geo gather first, then the remote sensor
array. In each, every unit packed itself into D bytes, tagged itself by content hash, and **self-sorted
across the lanes by its own compositional regime** (the geology data spread across all four components'
regimes; the fleet across its three failure modes), **deterministically** and **without disturbing the
source read** (roundtrip stays within the 7-bit floor). That is the "native moving as conveyors through the
system as-is" behavior, on real project data.

## Why it is non-disruptive (the key property)

The conveyor never owns the data — it **observes and re-expresses** it. The original composition read is
recoverable to the 7-bit floor at any point, so an existing project keeps running exactly as before; the
conveyor adds a compact, tagged, routable **shadow stream** that can be buffered, addressed, and routed
without touching the source. Adopt it incrementally, lane by lane, with nothing to break.

## Honest tiers

- **T1 (exact, measured):** the 8-bit pack/unpack, the content-hash self-tag, and the deterministic routing —
  reproducible, run on two real datasets.
- **T2 (modeled):** the streaming buffer/throughput and the differential-routing running baseline — the
  mechanism is real; "fast" here means O(D) per unit, not a benchmarked production rate.
- **T3 (vision — to earn):** native integration across **all** live projects top-to-bottom simultaneously,
  inside real running pipelines, at production throughput, with the command chain wired to real consumers.
  That full top-down deployment is the architecture this demonstrates, not yet a fielded system.
- **Honest overlap:** this is kin to message queues, content-addressable storage, and self-describing packet
  formats. The novelty is the **compositional, regime-aware, scale-invariant** routing and the **deterministic
  8-bit self-tagging** — not a claim to replace those.

*Cross-refs: `compositional_conveyor.py`, `CONVEYOR_RESULTS.json`, `compositional_memory.py` (the recall side),
`PROVENANCE_THE_7BIT_CORE.md` (the 8th-bit lineage), `../papers/UNWRITTEN_CONNECTIONS_SEEDS.md` (P4),
`THE_FEEDBACK_CHAIN_IS_THE_GOAL.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — packs/tags/routes itself, measured on real data · non-disruptive verified · deterministic · the full top-down deployment is fenced as vision · experts decide.*
