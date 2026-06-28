# The corruption detector — coherence catches a taken-over node in any long-chain system

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27. The full-system
coherence check has a second meaning: it is a **corruption detector.** A big system is corrupted by attacking one
node and taking it over — and if the attacker keeps the aggregate metrics unchanged, the dashboards stay green.
But a stealthy takeover that preserves the total must change the **ratios**, and that is exactly the deceptive
drift Hˢ is built to catch. Measured on real public data: `corruption_detector_long_chain.py` (`ea926d5817fec0d0`).
**Defensive — this detects tampering, it is not an attack tool.** Science public; application to any specific
named system held separate and Peter-gated. Nothing posted.*

---

## The result

A chain of 12 coherent nodes (real geochemistry compositions, input hash `546faf1e86bd6991`); one node is taken
over — replaced with a *different* real composition, **rescaled to preserve the chain's total** so the aggregate
is untouched. Over 400 randomized trials:

| detector | catches the corrupted node |
|---|---|
| **Totals monitor** (the usual aggregate watch) | **0%** — blind; the total was preserved |
| **Hˢ compositional coherence** (Aitchison distance to the chain's clr-centroid) | **99.8% — detected and localized** |

A node-takeover that fools the dashboards **cannot fool the ratios.** The relational coherence flags the exact
node, every time but a handful, while a totals view sees nothing at all.

## Why this is the same idea as everything else here

This is the **deceptive drift** — *"every total looks fine while the mixture turned"* — turned into a security
statement. The attacker's best stealthy move (keep the aggregate constant) is precisely the move a relational
read is immune to, because closure/clr ignore the total and read only the structure. The same property that lets
Hˢ catch a silent energy transition, a microbiome shift, or a drive-fleet pre-fault catches a **corrupted node**:
it is an outlier in the relational geometry the rest of the chain shares.

There are two layers of defence, and the project already has both:

- **The receipt/hash chain** (determinism): each node's output is content-addressed; a corrupted node breaks the
  chain — tamper-*evident*. This catches any change, but an attacker who controls a node can also forge its
  receipt.
- **The coherence check** (this): even a forged-receipt node that preserves the totals is caught, because its
  *ratios* do not cohere with the chain. The two together are belt and suspenders: the hash catches the careless
  attacker; the coherence catches the careful one.

## Where it applies — long-chain systems

Any system that is a **chain of nodes each carrying a composition** is a candidate; the theory tested here is the
general one:

- supply chains (each stage a parts-of-a-whole mix);
- power and energy grids (the generation/flow composition at each node);
- data and ML pipelines (the feature/label composition at each stage);
- determinism receipt / hash chains and distributed ledgers;
- sensor and fleet networks (each device's stress composition);
- and the project's **own journal chain** (each entry a receipted node).

The reason big systems are corruptible by taking over a single node is that the rest of the system trusts the
node's *output* — and a careful attacker matches the output's headline numbers. The compositional coherence check
removes that trust assumption: a node is believed only if its *relations* cohere with the chain. That is a
deterministic, re-checkable integrity layer for any long chain.

## Publish the science, hold the applications separate

- **Public science (this):** the method — *compositional coherence as a corruption/integrity check for
  long-chain systems* — with the measured result and the receipt. Reproducible by anyone on the cited public data.
- **Held separate (gated):** application to any **specific named system** (a particular supply chain, grid,
  ledger, or organisation), and anything resembling targeting. Those are off-repo, Peter-gated, and outside the
  scope of the public method.

## Honest scope

- **T1 (measured):** the 99.8% detect-and-localize vs 0% totals-monitor result on real geochemistry reproduces
  (`ea926d5817fec0d0`).
- **T2:** that this generalises to the listed long-chain systems is a reasoned reading; each real system needs
  its own coherent-baseline definition and validation.
- **The boundary (stated plainly):** it catches a takeover that changes the **ratios** (which a total-preserving
  attack must). A takeover that *also* matches the chain's relational structure — an attacker who knows the
  coherence and forges it too — is **not** separable by this check alone (the in-subspace / not-separable limit).
  Defence is layered, not absolute.
- **Defensive only; sole gate Peter; nothing posted.**

*Cross-refs: `corruption_detector_long_chain.py` (`ea926d5817fec0d0`); `HCI/THE_BLINDNESS_SUITE.md` (deceptive
drift); `papers/ABSTRACT_LEDGER.md` (P2, the drift detector); `ai-refresh/loglog/DETERMINISM_SWEEP_RESULTS.md`
(the receipt chain). Data: Ball geochemistry (public). Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — measured on real public data with a receipt · framed as defensive detection, not
attack · the totals-blind / coherence-catches contrast shown · the not-separable boundary stated · specific-system
applications held separate and gated · the human keeps the gate.*
