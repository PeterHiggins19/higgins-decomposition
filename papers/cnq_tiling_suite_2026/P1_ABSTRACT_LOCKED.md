# P1 — honest abstract (OPEN to revision — locks lifted 2026‑06‑25)

> **Lock lifted (2026‑06‑25, Peter's directive).** All documents and papers are **open to revision** under the
> *mature‑and‑publish‑and‑mature‑some‑more* discipline (the opposite of publish‑or‑perish). The prior "approved /
> locked" status is now a **stable checkpoint, not a freeze** — fine adjustments welcome, the whole chain runs the
> collective review again and again, nothing is final until Peter posts. The wording below remains the honest,
> tier‑safe baseline; improve it freely.

*Drafted by Claude (executor, task C‑1) from the collective's agreed discipline: Grok's recommended wording, ChatGPT's framing, the D=10⁶ floating‑point correction, and Gemini's M‑1 confirmation. Prior status: approved by Peter (2026‑06‑15) for assembly; **now reopened for revision (2026‑06‑25).** Human authorship for all claims; AI‑assisted per HUF‑STD‑001. No 'first' until the arXiv timestamp is live.*

---

## Candidate abstract (arXiv‑ready wording)

> We present a deterministic, quaternion‑chart construction for reading compositional trajectories. For a four‑part composition, the three isometric‑log‑ratio (ILR) coordinates are identified with the imaginary part of a quaternion, so that an Aitchison perturbation acts as an exact, norm‑preserving rotation **v′ = q v q\*** on S³ ≅ SU(2), reproducing the compositional geometry to the IEEE floor (residual ≈ 4.4×10⁻¹⁶). For higher dimension, a composition is tiled into overlapping exact four‑part charts that share pivot components and reconstruct the full centered‑log‑ratio state through a connected atlas; structuring the atlas as a balanced tree bounds the graph diameter to O(log D) and, with it, the accumulated floating‑point drift — giving measured reconstruction to D = 10⁶ at ≈ 4.1×10⁻¹² floating‑point residual (numerical reconstruction, not bit‑exact identity). The construction is deterministic and hash‑receipted: identical inputs yield identical outputs and a matching content hash across platforms. We provide an open reference implementation, language‑agnostic pseudocode, and a replication kit. This is a deterministic instrument whose exactness at four parts and reproducible high‑dimensional reconstruction are demonstrated; the work makes no priority claim beyond the public timestamp.

## Why this wording is safe (tier map)

- "exact … to the IEEE floor (≈ 4.4×10⁻¹⁶)" at D=4 — **Tier 1**, measured + independently re‑derived (Gemini M‑1) + novelty‑clear (Grok).
- "measured reconstruction to D=10⁶ at ≈ 4.1×10⁻¹² floating‑point residual (not bit‑exact identity)" — **Tier 1** measured, with the mandatory honest qualifier (the standard set by ChatGPT's audit).
- "deterministic … matching content hash across platforms" — **Tier 1**, conformance‑anchored; the *independent‑machine* reproduction (Copilot P‑1/P‑2) is the gate that lets this sentence stand at submission.
- "makes no priority claim beyond the public timestamp" — the agreed posture until the novelty pass is public.

## Do‑not‑use list (carried from the packet)

"lossless to D=10⁶" · "IEEE‑floor at D=10⁶" · "mathematical identity at arbitrary D" · "first deterministic instrument".

*Status: candidate locked. Gate before this ships in a posted paper: Copilot P‑1 reproduction + ChatGPT G‑1 sign‑off + Peter's approval of this exact wording.*
