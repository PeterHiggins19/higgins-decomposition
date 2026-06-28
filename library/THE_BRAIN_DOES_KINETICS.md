# The brain does kinetics — how an animal gets the sense Hˢ reveals, from dwell and mesh

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27. The thought:
an animal brain reads the kinetics of compositional/relational systems — the same object Hˢ reads. The math
leads to **one** answer; the brain's path is *similar but different*. So how does the brain get "that sense"
Hˢ reveals from **dwell** and **mesh**? The answer is measurable, and the brain's route converges to exactly the
read Hˢ computes. Measured: `brain_kinetics_dwell_mesh.py` (`b7fd9a39b664dc1a`). Structural analogy, fenced;
Peter is the sole gate; nothing posted.*

---

## The correspondence — the brain already computes the pieces

The brain is not doing something exotic; the canonical neural computations *are* the compositional operators:

- **Divisive normalization = closure.** A neuron's response divided by the pooled activity of its neighbourhood
  (the canonical cortical computation, Carandini & Heeger 2012) is exactly **normalization to a conserved whole**
  — and, like closure/clr, it **cancels a common multiplicative gain** (luminance, contrast, overall context)
  *exactly*. Measured here: the gain residual is **4×10⁻¹⁶** — the same common-mode rejection clr performs.
- **Weber–Fechner = the log.** Perception scales with the *logarithm* of intensity. Divisive normalization
  followed by log is, structurally, the **centered-log-ratio** — the brain reads in *relative, normalized,
  log-scaled* terms, which is to say **compositionally**.
- **Mesh = the receptor population.** A large array of sensors/neurons sampling the scene (population coding).
- **Dwell = neural integration time.** Temporal signal-averaging — fixation dwell, integration windows.

## The measurement — the brain's path reaches the same answer

A neural-style reader (divisive-normalize → log → integrate over a mesh of receptors across dwell time) was run
against a true composition whose exact relational read (clr) is *the math's one answer*. As **mesh × dwell**
grows, the neural read converges to that exact answer:

| mesh | dwell | N = mesh·dwell | Aitchison error to the exact Hˢ read |
|---|---|---|---|
| 1 | 1 | 1 | 0.95 |
| 4 | 1 | 4 | 0.46 |
| 1 | 16 | 16 | 0.22 |
| 4 | 16 | 64 | 0.11 |
| 16 | 64 | 1,024 | 0.031 |
| 64 | 256 | 16,384 | **0.0075** |

The error falls at the **1/√N law** (slope −0.49) — the observability law (recoverable structure ~ (mesh−1) ×
precision, precision ~ √dwell). So the animal "gets the sense" exactly the way you guessed: **a large mesh of
normalizing receptors integrating over dwell time averages the noise away and the relational read emerges.** The
gain (context, luminance) is rejected exactly by divisive normalization; the noise is beaten down by dwell and
mesh; what remains is the relational structure — the same thing Hˢ reads.

## Same answer, different path

This is the heart of it. **The math has one answer** — the exact clr of the true composition is unique. The
brain reaches it by a *statistical, parallel, approximate, learned* route (noisy receptors, divisive pools,
integration), converging toward it as dwell and mesh grow. **Hˢ reaches the identical answer by the
deterministic route** — closure → clr — in one exact step, to the IEEE floor. Two paths up the same mountain:
the brain climbs by averaging over its mesh and its dwell; Hˢ takes the exact line. That is why the brain can
handle the systems Hˢ handles, and why Hˢ feels intuitive when it works — it is computing, exactly, the read the
brain approximates.

It also closes a loop in the project: the **tetrode** (4 channels, determinism from noise) and the **observability
law** (dwell × mesh) were the engineered versions of what the brain does with its sensory array and its
integration time. The brain is the existence proof; Hˢ is the exact instrument.

## Part of the Peterson study — the neurological leg (the connectivity reward)

This is the mechanistic half of the **Peterson convergence** (CONV-001): Peterson's general theory of meaning
describes perception *narrowing a high-dimensional world through a value-laden channel.* This model gives that
channel a **deterministic mechanism** — divisive normalization (closure) + log (Weber–Fechner) read the world
*relationally*, and dwell × mesh recover the structure from the noise. So the project now offers the Peterson
study **two receipted legs**:

- **P-ψ — the psychological use case:** a values/virtue composition read on real public data with a hash receipt
  (`8ec3ae8d5623c5d7`) — *what* the value-channel attends to, made reproducible.
- **P-ν — the neurological study (this):** a deterministic model of *how* a perceptual channel reads relationally
  and reaches the exact answer through dwell and mesh (`b7fd9a39b664dc1a`).

One frame (Peterson's perception-and-meaning), two independent receipted reads (psychology and neuroscience),
both deterministic. That is the **connectivity reward HUF set out to deliver**: a single compositional spine
binding fields that rarely share a method — and giving each a reproducible, hash-checkable model. Both legs are
**underway** (registered as P-ψ / P-ν in `papers/ABSTRACT_LEDGER.md`); any approach to Dr Peterson remains
off-repo and Peter-gated.

## Honest scope

- **T1 (measured):** divisive-normalization gain cancellation (~10⁻¹⁵), convergence of the neural read to the
  exact clr answer, and the 1/√N law reproduce (`b7fd9a39b664dc1a`).
- **T2/T3 (the analogy, fenced):** this is a **structural / computational correspondence** — divisive
  normalization (Carandini & Heeger 2012), Weber–Fechner, population coding, integration time. It is **not** a
  claim that the brain implements Hˢ, that perception is literally clr, or that real neurons compute exactly this.
  The brain's path is approximate and learned; Hˢ computes the exact answer it approaches. The "must be" is a
  hypothesis the model makes plausible, not a proof about biology.
- **Sole gate:** Peter. **Nothing posted.**

*Cross-refs: `brain_kinetics_dwell_mesh.py` (`b7fd9a39b664dc1a`); the observability law
(`industrial-instruments/.../the dwell×contact×mesh core math`); `huf-gov/doctrine/THE_TETRODE_STANDARD_for_sensitive_studies.md`
(the engineered mesh); `papers/medical-epidemiology/THE_TETRODE_TEST_determinism_from_noise.md` (determinism from
noise). Refs: Carandini & Heeger (2012), *Normalization as a canonical neural computation*, Nat. Rev. Neurosci.;
the Weber–Fechner law. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the convergence and gain-cancellation are measured and receipted · the neuroscience
named honestly and fenced as a structural analogy, not a claim about real neurons · the one-answer / two-paths
framing kept exact · the "must be" marked as hypothesis · the human keeps the gate.*
