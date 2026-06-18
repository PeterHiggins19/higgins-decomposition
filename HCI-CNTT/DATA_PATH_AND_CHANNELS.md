# The data path, and the channel/carrier distinction — the engine as its own transmission controller

*CN-TT v4 design doctrine. Home: Hˢ (the instrument). Author: Peter Higgins (human authorship for claims); AI-assisted per HUF-STD-001; honest-broker; claim tiers marked. Resolver for cross-repo links: `../CROSS_BRAIN.md`. Answers a standing question — "carrier or channel?" — and records the design principle behind it: a dead engine serves nobody, so the engine exists to move data to a trustworthy output.*

> **Ratified by Peter, 2026-06-12.** Keep both terms (carrier = payload part; channel = transport path); the shortest-complete-path data-path principle stands as policy. (Companion ratification: the no-LFS raw `.gitattributes` policy, `DOCUMENT_DISTRIBUTION.md` / `G-9`.)

---

## 1 · The data-path principle — shortest complete path

The goal is a **straight path from data to output in the fewest steps — and no step missed.** Two failure modes, equally forbidden:

- **Bloat:** adding a step the path does not need. Every extra step is latency, surface area, and a place to drift.
- **Skipping:** bypassing a *required* step to look fast. A read that skips a maintained stage is not faster; it is *wrong sooner*.

The rule that resolves both: **if a maintained step exists in the CN-TT channel system, use it; if no step is required, do not invent one.** The maintained pipeline is the canonical path —

> closure → CLR → tiling → diagnostics → hash

— and the shortest *complete* path through it is the only correct one. A run is right when it touches every stage it needs, in order, and nothing else, and emits a hash receipt at the end. *(Tier 2 — design principle, soundly applied; the determinism contract that backs it is Tier 1.)*

*A dead engine serves nobody.* The point of the instrument is not elegance for its own sake; it is to deliver a trustworthy output, every time, by the most direct route that misses nothing.

## 2 · Carrier vs channel — keep both; they are different axes

The two words name **orthogonal things**, and the recent shift toward a transmission-control system is exactly why they must stay distinct rather than merge.

| Term | What it is | Axis | Lineage |
|---|---|---|---|
| **Carrier** | a *part of the composition* — O₂, SiO₂, a fuel type. The carriers collectively hold the structural information (the departure from the barycentre). | the **payload** axis — *what* carries the information | signal-processing carrier (the acoustic origin) |
| **Channel** | an *independent read / transmit / verify path* — a triple-channel reader (tiling · Clifford · matrix), a node in the network. | the **transport** axis — *how* the payload is moved and cross-checked | communications channel |

The one-line memory: **the carrier rides the channel.** A single read of a composition has D *carriers* on 1 *channel*; the triple-channel reads the same D carriers on 3 channels; the network is many channels carrying many compositions, each a payload of carriers. Conflating the two would collapse the payload into the transport and lose the very thing that makes the system a transmission controller.

**Recommendation (the answer to "carrier or channel?"):** **keep both, unchanged.** Carrier = the compositional part; channel = the independent path. Do *not* rename `carrier` in the engine — it is correct, pervasive, and load-bearing. A rename would be a large, risky change for no gain, and it would erase a distinction the system now depends on. *(If a future decision ever wants different surface words, that is a separate gated change; the concepts above stand regardless of the labels.)*

## 3 · The invention — a compositional analyzer that is its own transmission controller

Here is what is actually new, stated plainly. The **same object** — a composition — does two jobs at once:

- **As data:** its carriers are read, and the structure (shape, drift, helmsman) is the analysis.
- **As transport:** because every read is deterministic and hash-receipted, the composition becomes the *medium* of a self-verifying transmission system — any channel can recompute any other channel's read and confirm the receipt. The geo probe is a backup channel for the gas mask because both are just compositions to the instrument.

So the framework is not only a compositional **analysis** system; it is also its own **transmission controller** — the carriers are the payload, the channels are the transport-and-check, and determinism + the content hash are the protocol. The analyzer and the controller are the same engine, because reading a composition and verifying a transmission are, here, the identical operation.

*(Tier 1: the cross-verify primitive — determinism + identical hashes across channels — is implemented and verified. Tier 3: a deployed mesh of Hˢ-instrumented devices lending each other redundancy across domains — real, grounded, to earn.)*

## 4 · One sentence

Move data to a trustworthy output by the shortest path that misses no maintained step; the parts you read are **carriers** (the payload) and the independent paths you read and verify them on are **channels** (the transport), and because the instrument reads compositions deterministically it is, in the same act, its own transmission controller — which is the whole point, because a dead engine serves nobody.

**Cross-references:** `CNTT_COMPLETE_SPECIFICATION.md` (the maintained pipeline) · `MODULAR_ARCHITECTURE.md` (stage = control point + test point + cache) · `engine/geometry.py` (`carrier_health`) · `../CROSS_BRAIN.md` §3 (the network the channels enable) · `../experiments/network_redundancy_2026-06/` and `../experiments/clifford_tiling_redundancy_2026-06/` (channels, verified).
