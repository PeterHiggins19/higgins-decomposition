# Adaptive Anticipation — the hash is the anchor, time and test do the rest

*Operating doctrine. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; Peter is the sole commit/contact gate.*

---

## The principle, in Peter's words

> "Keep the hash. The errors get fixed by time and test. Track and verify after push, correct and justify — is all we can do. Adaptive anticipation."

## What it means

The system does **not** advance by pretending it is error‑free before it ships. It advances by holding one thing fixed — the **determinism hash**, the conformance receipt that says *this engine, on this input, returns exactly this output, bit‑for‑bit, on any platform* — and letting everything else be corrected through use. The hash is the invariant you can always return to; bugs, edge cases, and mis‑reads are found by **time and test**, not by a claim of perfection made in advance.

This is the honest‑broker stance turned on the codebase's own evolution. We do not say "there are no errors." We say "here is the fixed reference, here is the cycle that finds and justifies every deviation from it." Anticipate that errors exist; build the loop that catches them. That is *adaptive* anticipation — the opposite of brittle over‑promising.

## The cycle

```
   anchor ──▶ push ──▶ track ──▶ verify ──▶ correct ──▶ justify ──▶ (re‑anchor)
   (hash)            (what       (against    (fix the    (log why,
                     changed)     the hash)   deviation)  re‑hash)
```

1. **Anchor.** The determinism certificate (SHA‑256 of the engine output on the reference corpus) is the fixed point. Cross‑platform value‑identity already demonstrated (Windows ≡ Linux). It does not move unless the engine *intends* to move, and when it does the change is announced and re‑certified.
2. **Push.** Ship the change (Peter's gate — no AI commits or pushes, ever).
3. **Track.** Record what changed and what it touched (the tracking log, the journals, the manifests).
4. **Verify after push.** Re‑run the conformance hash + the self‑tests + the real‑data runs. A matching hash means *nothing silently drifted*; a deviation is a signal, located precisely because the anchor is exact.
5. **Correct.** Fix the deviation — in code, in a guard, or in the claim's tier.
6. **Justify.** Log *why* it deviated and *why* the correction is right. The justification is part of the record, not an afterthought. Then re‑anchor (re‑hash) if the engine's intended behavior changed.

## Why the hash must be kept

Without a fixed anchor, "we fixed some bugs" is unfalsifiable and every change risks silent regression. **With** the hash, correction becomes *measurable*: you know exactly when behavior changed, by how much, and whether it was intended. The determinism certificate is what makes "track and verify after push" mean something instead of being a hope. It is the same discipline as a calibration cycle on a measuring instrument — the reference is held; the instrument is re‑checked against it; drift is found, corrected, and documented.

## Relation to the rest of the doctrine

- The hash and its metrology live in [`DETERMINISM_GAUGE_RR_AND_CONFIDENCE.md`](DETERMINISM_GAUGE_RR_AND_CONFIDENCE.md) (gauge R&R ≈ 0, the 6σ/9σ gate).
- The guards that *fail loud* rather than guess ([`engine/`](engine/): E‑21, hold‑lock, resolvability, SafeLoop breakers) are the run‑time face of the same idea — the system would rather hold or trip than emit a confident‑wrong answer that the verify step would later have to unwind.
- The claim tiers (Tier‑1 measured / Tier‑2 reasoned / Tier‑3 a‑clue‑never‑a‑claim) are how a *justification* is graded.
- The self‑measuring library ([`../library/`](../library/)) is verified the same way: regenerate the index, re‑run the recursive classifier, compare — the table is a measurement, so it is re‑checked, not trusted.

## When a torn read happens (the mount artifact ≠ a repo problem)

A "torn" read — the sandbox/bash mount serving a truncated or stale copy of a file that was *just* written (FM‑1) — looks like corruption but is not. The file on the authoritative side (Windows) is whole. **Do not report it as an error.** The resolution is the same anchor logic:

- **The hash + verify‑on‑push confirms the repo, not the torn read.** A truncated bash view is a *view*, not the state. The conformance hash and the post‑push verify are what say whether the repo is actually good. Trust the anchor over the artifact.
- **Refresh and wait before reporting.** Give the mount a moment to settle, re‑read (Windows‑authoritative Read is the tiebreaker), and only then report. A torn read that clears on refresh was never a defect — reporting it as one is a false positive the verify step would have dismissed anyway.
- This is itself adaptive anticipation: *anticipate* the artifact, *verify* against the anchor, *wait* rather than mistaking a transient view for a fault.

## The standing instruction

Keep the hash. Ship behind Peter's gate. After every push: re‑verify against the anchor, correct what deviated, and log the justification. That is all we can do, and — done every cycle — it is enough. Adaptive anticipation: the errors get fixed by time and test, and the record shows exactly how.
