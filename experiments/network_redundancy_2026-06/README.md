# Network cross‑verification — any node checks any node (2026‑06‑11)

*The triple‑channel reader, generalized from one box to a network. Any Hˢ processor can verify any other connected compositional system — regardless of what each natively processes — because every read is deterministic and hash‑receipted. Verified (Tier 1). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. See [`../../CROSS_BRAIN.md`](../../CROSS_BRAIN.md) §3.*

Run: `python experiments/network_redundancy_2026-06/network_redundancy.py`

## The idea

The instrument that reads compositions can read the composition of **its own readers**. The primitive is determinism: the same composition produces the same `cntt_content_sha256` on any node. So:

1. **Determinism = the cross‑verify primitive.** A node confirms a peer's read by recomputing it and comparing the receipt — no trust, just reproduction.
2. **Any node checks any other.** A gas mask reading {O₂,CO₂,N₂,agent} and a geo probe reading {SiO₂,Al₂O₃,…} emit hash‑receipted reads in the same form; a node with spare capacity recomputes a peer's input and confirms its receipt. *The geo probe on the wall is a backup channel for the gas mask in the infirmary.*
3. **N‑node FDIR.** A majority vote across nodes gives `RC‑CON‑INF` (consensus) · `RC‑ISO‑WRN` (isolate the minority node) · `RC‑HLT‑ERR` (no majority → halt‑and‑report safe state).

## Verified

| test | result |
|---|---|
| node B reproduces node A's receipt | identical hash (`efdd0437…` == `efdd0437…`) ✓ |
| heterogeneous nodes (gas mask + geo probe) | distinct valid receipts; geo‑probe **verifies** gas‑mask by recompute ✓ |
| 5 nodes, one faulty | `RC‑ISO‑WRN` → **isolates the faulty node** ✓ |
| 5 nodes, all clean | `RC‑CON‑INF` consensus ✓ |

## Lineage — this is the 3^n index, built

The theory came first. Peter's **3^n Systems Confidence Index** (HUF, April 5 2026 — `../HUF/science/methodology/CONFIDENCE_INDEX.md`, resolver in `../../CROSS_BRAIN.md`) named the geometry exactly: *"three perspectives define a plane; the odd one out is identified; three is the minimum to **locate** an error, not just detect it."* That is this vote. `n=1` (3 independent checks) is the single‑box triple‑channel; `n=4`/`n=5` (replication across sites, then time) is this network. *Detect with two, isolate with three, scale to N* is the operational face of `C_n = 1 − (1−p)^(3^n)`.

## Scope (honest)

- **Tier 1:** the cross‑verification primitive (determinism + identical receipts + the N‑node vote) is implemented and verified on the real engine.
- **Tier 3:** a *deployed* mesh of Hˢ‑instrumented devices lending each other redundancy across domains. Grounded in the primitive, but to earn.

*All possible because it is all just the way the system handles compositions — including itself.*
