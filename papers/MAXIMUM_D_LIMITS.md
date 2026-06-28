# Maximum D in Hˢ — the limits, physical/deterministic and not

*The honest scope of "how high can D go." The short version: **Hˢ has no intrinsic mathematical ceiling on
D** — the tiling is scale-free by design (O(log D) chart-graph diameter). Every real limit is **external**,
and the limits fall into two classes that must not be confused: **(A) physical/deterministic** — fixed by the
algebra, the IEEE-754 format, and the hardware word size, **identical on every conformant machine and
knowable exactly in advance**; and **(B) non-deterministic / data-dependent** — set by what the data *is*,
varying dataset to dataset, and reported by the instrument (EITT) rather than computed ahead of time. Author:
Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. Honest-broker; numerical
anchors **measured** (`experiments/max_D_limits_probe.py`), every claim tiered.*

---

## The one sentence
The **algebra** fixes one hard number — **D = 4 for exactness** — and otherwise imposes **nothing**; the
**machine** fixes three deterministic ceilings (precision, index width, memory); and the **data** fixes the
soft ceiling that usually binds first and that only the instrument can tell you (**EITT**).

## Class A — physical & deterministic (hard; same on every conformant machine; knowable in advance)

These are guarantees. Given the algebra, IEEE-754 double precision, and a 64-bit word, you can state each of
these *before running anything*, and a conformant machine cannot disagree (this is the determinism the
HS-EPS-1 conformance receipt anchors).

| Limit | Ceiling | Mechanism | Tier |
|---|---|---|---|
| **Exactness rung** | **D = 4** | only the four-part chart is bit-floor exact (S³=SU(2)=Spin(3)); there is **no native exact high-D rotor** — associativity dies at the octonions (D=8), the division/norm property at the sedenions (D=16), so tiling is *forced*, not chosen | 1 (structural) |
| **Float64 global precision** | **D ≈ 4.5×10¹⁵** | the geometric-mean log-sum loses ~1 ULP-of-the-whole when D·ε ≈ 1 (ε = 2.22×10⁻¹⁶). *Per-element* CLR stays at the floor far below this (closure error ~√D·ε ≈ 9×10⁻¹⁶ even at D=10⁷) | 1 (measured) |
| **Reconstruction conditioning** | **no practical ceiling** | the balanced-tree atlas keeps diameter ~2log₃D, so conditioning grows only as (log D)²; diameter²·ε ≈ 10⁻¹² even at D=10¹⁸ | 1 (measured) |
| **Index width (int64)** | **D < 2⁶³ ≈ 9.2×10¹⁸** | a single contiguous array is addressed by a 64-bit integer; beyond this you need hierarchical/bignum addressing | 1 (exact) |
| **Memory (single machine)** | **~10⁹–10¹⁰** | storage is O(D): 8 bytes/part → 8 MB at 10⁶, **8 GB at 10⁹, 8 TB at 10¹²**; beyond one machine, the streaming/distributed path extends it | 1 (arithmetic) |
| **Underflow floor** | part > ~2.2×10⁻³⁰⁸ | a part smaller than the smallest normal double underflows; for ~equal parts (each ~1/D) this only bites at D ~ 10³⁰⁸ — never binding | 1 |

**Reading the table:** for *exactness*, the wall is D=4 and nothing moves it. For *raw size*, the binding
deterministic wall is **memory (~10⁹ on one machine)** then **index width (~9.2×10¹⁸)**; float64 precision
(~4.5×10¹⁵) sits between them, so the format is not what stops you first. The tiling math itself adds **no**
ceiling — that is the whole point of the O(log D) construction.

## Class B — non-deterministic & data-dependent (soft; varies by dataset; the instrument tells you)

These cannot be computed in advance because they depend on what the data *is*. They vary dataset to dataset
and even region to region within one dataset, and Hˢ's job is to **report** them, not to pretend they aren't
there.

- **The statistical / support ceiling (usually binds first).** A D-part composition is only *meaningful* up
  to the data's intrinsic rank/support. If the signal lives in a few hundred carriers, the engine's effective
  dimensionality **K_eff sits far below D** no matter how large D is. Pushing D past the support adds parts
  that carry no information. *(Tier 2 — design/empirical; depends on the data.)*
- **The EITT boundary (the in-built honest signal).** Where the entropy-invariance breaks, the structure has
  stopped being analysable — and that point is **set by the data, not the machine**. EITT returns "boundary"
  exactly there, so the instrument *holds* rather than fabricating structure that the numerical headroom would
  otherwise let it report. This is the "no surprises" property: the deterministic limits are guarantees you
  compute ahead of time; the EITT limit is the one the instrument refuses to lie about.
  *(See `EITT_PAPER_SEED.md`, `CONTRADICTION_TEST_PROTOCOL.md`.)*
- **Sparsity / zero-domination.** As D grows against a fixed sample size N, the composition sparsifies; below
  a data-dependent point the read is dominated by zero-treatment (E-21), not by structure. Where this bites
  depends entirely on N and the data's concentration. *(Tier 2.)*

## The synthesis — which binds first
1. If you need an **exact** reading: **D = 4** (Class A, hard).
2. If you need a **meaningful** reading: the **data ceiling** (Class B) almost always binds first, and
   **EITT names it for your specific dataset**.
3. If you only need **raw scale**: **memory (~10⁹ on one machine)** binds first, then **index width
   (~9.2×10¹⁸)**; precision and conditioning have room to spare; the distributed/streaming path moves the
   memory wall.

The deterministic ceilings are **promises** (computable, machine-independent, receipt-anchored). The
data-dependent ceiling is a **measurement the instrument makes for you** (EITT) — and conflating the two is
itself a claim the contradiction test would reject: *"the math limits D"* is false; **the machine and the
data limit D, and the instrument tells you which.**

## Reproduce
`python experiments/max_D_limits_probe.py` regenerates the Class-A numerical anchors (ε, the CLR round-trip
and closure errors vs D, the D·ε≈1 floor, the tree-diameter conditioning). The exactness rung and the
Cayley–Dickson break are in `frontier/THE_LADDER_AND_THE_BREAK.md`; the data ceiling and EITT are in
`EITT_PAPER_SEED.md` and `TRIANGULATION_PROTOCOL.md` (View C).

*Status: honest-scope reference for P1/P3. Class A measured (Tier 1); Class B design/empirical (Tier 2) and,
for EITT, instrument-reported. No "lossless"/"identity"; no "first". Peter is the sole gate.*
