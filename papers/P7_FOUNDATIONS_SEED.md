# P7 (seed) — Foundations: the deeper mathematics the instrument revealed

*The closing paper of the series — Movement VI, the Coda. It is written **last**, assembled from results
that have already landed in P1, P3, P4, P5 (and the frontier triage), each carried in with its receipt.
This file is the **living seed**: it accumulates as the papers develop, so that when the spine is published
the synthesis is already assembled and verified. Author: Peter Higgins (human authorship for all claims);
AI-assisted per HUF-STD-001. Honest-broker; every finding below carries its tier and its source. Nothing
here is posted; Peter is the sole gate.*

---

## Thesis

A practical instrument — built to read conserved mixtures and pushed until it was *exact* — turned out to
sit on a specific, nameable piece of mathematics. The same push revealed, with equal sharpness, what the
mathematics **forbids**. This paper reports both: the positive structure that the exactness exposed, and
the negative space that the exactness rules out. The discipline is the contribution as much as the algebra:
when a construction is exact and deterministic, falsification becomes *internal and cheap* (a claim that
contradicts the exactness is dead on arrival), and the negative results are as load-bearing as the positive
ones. The deeper math is not a decoration on the instrument; it is what the instrument's exactness *is*.

**The premise (the program in one line).** Push determinism as far as it can be *proven* to go, and let that maximal exact core **define, by its complement, the tightest boundary that can be drawn around what remains non-deterministic.** Exactness is not the claim that everything is deterministic; it is the sharpest available knife for cutting out what is not. Each place the exact read stops is a *measured* point on that boundary — the floating-point drift at scale (F-5), the finite-sample capacity $D^{*}(N)$ of the compositional message (CMP), a carrier with no admissible log-ratio (the E-21 guard), a residual a guard refuses to resolve. The union of those points is the current frontier; *'as tight as determinism can draw it'* is the asymptote the program walks toward, **not** a theorem it claims to have reached. **Conditional on EITT** (Shannon entropy conserved under geometric-mean temporal compression), the frontier closes in *time* as well as in composition: **MC-4** bounds the deterministic envelope across space/parts, **EITT** across time, and the non-deterministic world is what lies outside both — no larger than those two invariances force it to be. *Tier: the premise is T2 (a program/framing); it inherits exactly EITT's certainty and no more — EITT is T1-measured on its cases but carries explicit kill conditions (proportional data; sufficient carrier dimensionality; conservation, not prediction; external forcing invisible). The boundary is only as tight as EITT is true.*

## What "deeper" means here (the discipline of this paper)

Only results that are **earned** enter: Tier 1 (measured/reproduced) or Tier 2 (sound synthesis on
established prior art). Suggestive analogy does not. The paper's spine is the **contradiction-test register**
(`CONTRADICTION_TEST_PROTOCOL.md`): each "deeper" claim is stated together with the claim it excludes, so the
reader can see exactly where the structure stops. This is why the negative results below are stated as
strongly as the positive ones — they are theorems of the same construction.

## The findings (each matures when its home paper lands)

### F-1 · The exact rung — a composition *is* a rotation, at four parts
At $D=4$ the three ILR coordinates are the imaginary part of a quaternion, and an Aitchison perturbation is
the sandwich $q\,v\,q^{*}$ — an exact element of $SO(3)$ on $S^3 \cong SU(2) = \mathrm{Spin}(3)$, reproduced
to the IEEE floor (residual one ULP; 5-way cross-platform receipt `06ccdb25…`). **Tier 1.**
*Home: P1 + HS-EPS-1. Matures: now (P1 carries it).*

### F-2 · Two chiralities, one rotation — the hidden $SU(2)\times SU(2)$
Left- and right-quaternion multiplication give **two commuting copies** of $\mathfrak{su}(2)$, closing with
**opposite** structure constants ($+2$ left/adjoint, $-2$ right) — the $\mathrm{Spin}(4)=SU(2)\times SU(2)$
seen at $D=8$. The sign that looked like an error is a *chirality*. **Tier 1** (verified numerically).
P1 spends only 3 of these 6 degrees of freedom (the adjoint $SO(3)$); the second, independent $\mathfrak{su}(2)$
is unused, and its **future value is evaluated** in [`frontier/SO4_SPIN4_FUTURE_COMPONENT.md`](frontier/SO4_SPIN4_FUTURE_COMPONENT.md)
— strongest near‑term direction: **dual‑quaternion 6‑DOF kinematics** (exact rotation + translation in one
object; robotics / aerospace / satellite pose) [T2], plus two‑channel reads and the two‑helicity EM bridge
[T3]. The **verified, corrected** explicit left/right generators (a collective contribution had mislabeled
them) live in that file, for the replication kit.
*Home: P1 appendix + frontier assessment + SO4 evaluation. Matures: now (structure) / next (dual‑quaternion demo).*

### F-3 · Why four, and only four — the ladder and its break
The Cayley–Dickson ladder explains why the exact rung is $D=4$ and cannot be pushed natively: associativity
dies at the octonions ($D=8$), and the division/norm-multiplicative property dies at the sedenions ($D=16$,
explicit zero divisor). There is **no native high-dimensional division-algebra rotor** — so reaching high
dimension by **tiling four-part charts is forced, not a design choice**. **Tier 1.**
*Home: frontier (`THE_LADDER_AND_THE_BREAK`, `WHICH_GROUP_REAL_SYSTEMS_JOIN`). Matures: as a P7 section.*

### F-4 · Exactness *is* flatness — the global structure is exactly connectivity, no richer
The high-D atlas reconstructs the clr state exactly **iff** the chart graph is connected (graph-Laplacian /
angular-synchronization recovery); the conditioning is set by the graph **diameter** ($O(\log D)$ for a
balanced tree). Read as a connection, exact path-independent transport **is** a **flat** connection — zero
curvature. The deeper statement: *the global geometry is exactly as rich as connectivity demands and no
richer.* **Tier 1/2.**
*Home: P1 §3.3–3.4. Matures: now.*

### F-5 · The negative space, as theorems (what the math forbids)
Stated as strongly as the positive structure, by contradiction (the register):
- **No nontrivial topology.** Over a contractible region of the simplex every principal $SU(2)$-bundle is
  trivial; $c_2=0$, instanton number $0$. Exact reconstruction $\Rightarrow$ flat $\Rightarrow$ no
  curvature, holonomy, monopoles, or "topological protection" (test **C-1**). The bundle *language* is a
  valid description of consistent gluing; the bundle *topology* is provably vacuous here.
- **No "lossless" at scale.** Measured reconstruction drift is non-zero and grows with $D$
  ($\sim4.1\times10^{-12}$ at $D=10^6$); "lossless/identity at high D" is excluded (test **C-2**).
- **No manufactured significance / no entanglement.** A deterministic instrument (Gauge R&R $\approx 0$)
  adds no spread (**C-4**); classical compositional carriers obey CHSH $\le 2$ (**C-7**).
**Tier 1.** *Home: frontier triage + P3. Matures: as the P7 "boundary" section.*

### F-6 · The instrument turned on itself — character and native recursion
Applying the reading to its own outputs yields a low-rank **Compositional Character Space** (a handful of
recurring characters across unrelated domains; rank $\approx 4$ at $n{=}107$), and the construction is
**natively recursive**: Hˢ reads Hˢ, and the read converges. The deeper math of self-application: the
instrument is a member of the class it measures. **Tier 2.**
*Home: P5 + `library/THE_ARCHITECTURE_AS_COMPOSITION`. Matures: with P5.*

### F-7 · The epistemics the exactness forced — method as a result
Because the core is exact and deterministic, three practices became available that are not usually available
to a statistical method: a **machine-epsilon conformance receipt** (one fixed-vector test, identical across
platforms), a **content-hash determinism** contract, and an **internal contradiction test** (falsification
at zero external cost). The claim: *exactness changes the epistemics* — it makes a method that can be tested
by what cannot both be true. **Tier 1/2.**
*Home: P3 + `CONTRADICTION_TEST_PROTOCOL` + HS-EPS-1. Matures: with P3.*

### F-8 · The determinism boundary — exactness as the tightest cut around the non-deterministic
The positive structure (F-1–F-4) and the negative space (F-5) are two faces of one premise: a maximally exact, deterministic instrument **defines the boundary of the non-deterministic as its own complement**, and draws it as tightly as the proven exactness allows. The boundary is *assembled from measured stop-points* (scale drift; the CMP capacity $D^{*}(N)$; inadmissible carriers; unresolved-residual guards), never asserted. With **EITT** the cut extends across time: **MC-4** (spatial/parts invariance) $\oplus$ **EITT** (temporal invariance) form a two-axis deterministic envelope. **Tier 2** (framing/program), **conditional on EITT** (T1-measured on its cases, with stated kill conditions). *Home: the P7 boundary framing + the MC-4 / EITT lineage. Matures: as the thesis of the boundary section.*

## How this paper builds as the series develops

1. The seed (this file) holds each finding with its **tier, receipt, and home paper**.
2. As P1, P3, P4, P5 land, each finding's "matures" line flips to *published*, and its statement is pulled
   from the now-public paper with a citation rather than re-derived — the **paper/repo division of labour**
   (`PAPER_AND_REPO_DIVISION.md`): the deeper synthesis is P7's, the proofs/data live in the prior papers
   and the repo.
3. P7 is **assembled last** and only from findings that have cleared their home paper's gate — so the Coda
   makes no claim its predecessors have not already banked.

## Honest envelope (carried)

- Earned only: Tier 1/2; no Tier-3 speculation in the spine. No "lossless", no "first" until timestamps are
  live. The quarantined towers (topological super-structure; transcendental numerology) appear **only** in
  F-5, as the boundary — what the math forbids — never as positive claims.
- Framing/venue (to decide later): foundations of compositional geometry / applied algebra — a framing that
  invites the structure **and** its boundary, not one that invites the topology the construction rules out.
- The negative results are first-class: a paper that states precisely where its structure ends is stronger
  than one that implies it never ends.

## Status

**SEED — not written, assembled last.** Supporting papers: P1 (compiling), P3 (drafted), P4/P5 (drafted),
P2 (vigilance), P6 (financial demonstration). P7 follows them. Registered in the abstract ledger as the
series Coda. Peter is the sole gate; nothing here is posted.
