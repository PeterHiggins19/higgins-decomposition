# Provenance — the 7-bit core (V∞Core) and the road to the composition

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. A
rediscovered ancestor, found in the archive on request: the **V∞Core** project (Jan–Feb 2026) — a **7-bit,
unity-normalized regime engine with a 1-bit XOR "how-to-use" header** — and how it prefigures the composition
idea and the deterministic vector-render lineage. Sourced to the original files; interpretation tiered.
Honest-broker; Peter is the sole gate; nothing posted.*

---

## What was found (the original artifact, quoted)

`RWA/concepts/v-infinity-core/V_Infinity_Core_V3.0_Hilbert.txt` — *"V∞Core V3.0: Hilbert Oneness Operator
(7-bit Core)"*:

- **7-bit data.** *"7-bit regime container: metadata {weight: 0–127 …}"*; `encode_7bit(val) = clamp(round(val*127),0,127)`; *"ROOT regime weight=127 // 7-bit scale."*
- **The 1-bit XOR header.** `decode_7bit(input_7bit) // strip 8th metadata bit (XOR "how-to-use")`, and
  `decode_7bit(b) = b & 0x7F  // strip metadata`. The eighth bit was a **metadata / how-to-use** flag,
  XOR'd onto the 7-bit payload.
- **Unity-normalization = closure.** *"regimes: map … ROOT sums to 1.0"*; `normalize_unity(x)` forces
  `Σ = 1.0` by softmax/renorm. (`HUF_VCore_Stack_Brief_v1.0.md`: *"Unity is enforced at every level via
  softmax or renormalization … w_i = ωᵢ/127 … Σwᵢ = 1.0."*)
- **Dates / status.** V2.0–V4.1, Jan–Feb 2026; *"the working implementation of HUF's invariant";*
  *"normalize_unity = μ in H₁."*

So your memory is exact: **7-bit data + a 1-bit XOR header, on a unity-summed regime container.**

## Why it is an ancestor of the composition idea

Three lines run straight from V∞Core into the present framework:

1. **Unity-sum regimes → closure → the simplex.** The V∞Core ROOT-sums-to-1.0 with `w_i = ω_i/127` *is*
   closure — parts of a budget summing to a constant — written before the CoDa vocabulary was attached. The
   brief states it plainly: `normalize_unity = μ in H₁`, the Higgins Operator, which is the abstract form of
   the closure map that Hˢ now reads as a composition. **The 7-bit core was doing compositional data analysis
   under another name.** (T1 — documented identity in the source.)
2. **The 8th XOR "how-to-use" bit → "the data is the carrier."** The metadata bit said *how to use the
   payload, carried in the payload itself.* That is the seed of the keystone the project later named
   explicitly — **the data carries its own frame / control; no separate carrier** (the P-Ω "data is the
   carrier" result, and the P3 verify/lock framing). The 8th bit is the earliest form of "the message
   describes its own reading." (T2 — a reasonable reading of the artifact, not a claim the old code proved
   the keystone.)
3. **Determinism → the same discipline, then graphics now.** V∞Core's typed, verifiable RMUs and unity
   contract are the same determinism-first instinct that became the hash-receipt engine.

## The vector-image thread you remembered

It is real, and it is two strands — "or some such" is apt:

- **Deterministic tensor → vector render.** `…/atlas/DETERMINISTIC_PDF_PROPOSAL.md` (*"Direct Tensor → PDF
  Rendering"*): replace matplotlib with a pure-stdlib renderer that emits pages **directly from the CNT JSON
  tensor**, because *"matplotlib version drift changes byte output even at identical vector content"* — the
  goal being a **deterministic hash on the vector graphic itself.** This is the lineage that became the
  `arc_of_discovery.svg`, the CNQ tiling plates, and the hash-stamped atlas: a **vector image generated from
  the composition, reproducible to the byte.**
- **A 7-bit visual language.** `papers/codawork2026/HIGGINS_DIAGRAMS.md`: a diagram system on **7-bit ASCII
  only (0x20–0x7E)**, *"no font dependency,"* *"every symbol has exactly one meaning,"* *"composable —
  diagrams nest and chain."* A font-free, composable, 7-bit visual encoding — the same 7-bit, one-meaning,
  composable instinct as V∞Core, applied to graphics.

So the path you remember is: **a 7-bit unity-normalized compositional encoding, carrying its own how-to-use
header, that renders deterministically to vector graphics.** The "vector image system" is the
deterministic-render + 7-bit-glyph side of that one idea.

## Is there value in the 7-bit idea? (measured)

Tested on the three real public compositions (gas / blood / produced-water), `7-bit quantization` two ways —
on the **linear shares** (as the original V∞Core did) vs in **log-ratio (clr) space**:

| dataset | share dynamic-range | 7-bit LINEAR (clr error) | 7-bit in CLR space (clr error) |
|---|---|---|---|
| GAS (D=3) | 188× | 0.38 — poor | **0.020 — near-lossless** |
| BLOOD (D=4) | 15× | 0.047 | **0.011** |
| WATER (D=7) | 31,893× | **7.13 — catastrophic** | **0.041 — near-lossless** |

And the 7-bit *integer* encode is **bit-identical across runs** (vs float, which can drift across platforms).

So the value is real but **conditional**, in three honest parts:

1. **Quantize in clr/log-ratio space, NOT linear shares.** Linear 7-bit crushes the trace parts — and in
   compositions the trace parts often *carry the signal* (the measured "SO₄/HCO₃ drive the read, not Na-Cl").
   The original V∞Core's linear 0–127 is the wrong coordinate; **7-bit on the clr is near-lossless even at a
   30,000× dynamic range.** This is a genuine correction to the old idea.
2. **The value is deployment + determinism, not new analytical power.** A 7-bit integer + 1 flag bit packs a
   self-describing part into one byte: compact, byte-aligned, integer-only, and **bit-exact reproducible**
   (better than float for the hash/receipt discipline) — ideal for edge sensors, embedded probes, and
   transmission (the Hs Duplex / P3 verify-lock). The 8th "how-to-use" bit is a cheap *data-is-the-carrier*
   frame tag.
3. **It is right-sized to the knowable.** 7 bits ≈ 0.8% per part — often near the real per-part precision the
   coherence floor (max Q) supports anyway, so quantizing there matches resolution to what the data carries,
   rather than spending float64 on noise.

**Verdict:** worth keeping — as an *encoding/deployment* discipline applied **in log-ratio coordinates**, for
edge/transmission/determinism. Not a new capability; a right-sized, deterministic codec for compositions.

## Honest scope

- **Faithfully sourced (T1):** the 7-bit core, the XOR 8th-bit header, the unity-normalization, and the
  deterministic-render proposal are all quoted from the original files.
- **Interpretation (T2):** the lines drawn from the 8th bit to "data is the carrier," and from the 7-bit
  render to the present SVG lineage, are *readings* of the provenance — strong and consistent, but the old
  code did not *prove* the later keystones; it **prefigured** them.
- **What it earns:** a documented ancestor. The composition idea, the data-is-the-carrier keystone, and the
  deterministic-vector-render discipline were all already breathing in a 7-bit regime engine in early 2026 —
  which is exactly the kind of tacit history the repositories exist to hold.

*Cross-refs: `../../RWA/concepts/v-infinity-core/V_Infinity_Core_V3.0_Hilbert.txt`,
`../../HUF/science/quantum/HUF_VCore_Stack_Brief_v1.0.md`, `../papers/codawork2026/HIGGINS_DIAGRAMS.md`,
`THE_DATA_IS_THE_CARRIER.md`, `../ARC_OF_DISCOVERY.md`, `../HISTORY_THREAD.md`. Peter is the sole gate;
nothing posted.*

*Proof & Honesty Standard — the artifact is quoted, not paraphrased · prefigured vs proved is marked · the lineage is sourced · experts decide.*
