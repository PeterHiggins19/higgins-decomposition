# Hˢ at CoDaWork 2026 — Executive Summary
## From Weakest Claims to Strongest Theorems
## What CoDa Can Refute, Support, or Extend

**Peter Higgins — Independent Researcher, Markham, Ontario, Canada**
**For: CoDaWork 2026, Coimbra, Portugal — June 2026**

---

## Strategy

This document ranks every claim in the Hˢ system from weakest to strongest.
The CoDaWork presentation inverts the usual approach: instead of leading with
the flagship result (δ = 5.87 × 10⁻⁶ in nuclear binding energy), we lead
with the points most likely to provoke productive disagreement from the CoDa
community. The goal is not defence — it is engagement. If CoDa can refute a
weak claim, the system gets stronger. If CoDa can support a strong claim, the
system gets validated by the community that owns the simplex.

---

## The Claims: Weakest to Strongest

### TIER 5 — SPECULATIVE (most attackable, most interesting)

**5.1 The Transcendental Naturalness Hypothesis**

*Claim:* Every natural compositional system exhibits statistically significant
proximity between its Aitchison variance trajectory and at least one member
of a 35-constant transcendental library.

*Weakness:* The Intermediate Value Theorem guarantees that ANY continuous
monotonic trajectory spanning a range containing a constant WILL pass near it.
Uniform random data passes the test. The hypothesis is necessary, not sufficient.

*What CoDa can attack:* Is the 1% threshold arbitrary? Is the 35-constant
library cherry-picked? Can CoDa construct a natural compositional system that
fails after exhaustive alternate decomposition?

*The hinge:* If CoDa finds a natural system that genuinely fails, either the
constant library needs expansion (Mode B calibration) or the hypothesis has a
counterexample (Mode D extraordinary interest). Either outcome advances the field.

**5.2 Euler-Family Resonance**

*Claim:* The pipeline's log → complex → polar geometry is structurally
isomorphic to the Euler identity e^(iπ) = -1, and natural systems preferentially
lock to 2π, e^π, π^e and their reciprocals.

*Weakness:* The isomorphism argument is suggestive, not proven. The CLR
transform introduces logarithms, the helix introduces angular periodicity,
but the claim that this FORCES resonance with specific constants requires a
formal proof that does not yet exist (Schanuel's conjecture, if proven, would
provide it — but Schanuel remains open).

*What CoDa can attack:* Is the observed clustering around Euler-family
constants an artefact of the pipeline's architecture, or does it reflect
genuine structure in the data? Can CoDa design a pipeline with different
geometry (e.g., ILR instead of CLR, no helix step) and test whether the
same constants appear?

*The hinge:* If the resonance disappears with a different pipeline geometry,
it's an artefact. If it persists, it's in the data. CoDa is the community
best positioned to test this.

**5.3 Conversation Drift Detection**

*Claim:* Text conversations can be decomposed into compositional carriers
and monitored for structural drift using the same pipeline that analyses
physical systems.

*Weakness:* The carrier definition (Theory/Engineering/Documentation/Discovery)
is ad hoc. Different keyword lists would produce different compositions.
The single test case (our own project milestones) is not independent validation.

*What CoDa can attack:* Is text-to-composition mapping well-defined in the
CoDa sense? Does the closure constraint (parts sum to 1) apply meaningfully
to keyword frequencies? Is this CoDa or is it something else wearing CoDa's clothes?

---

### TIER 4 — EMPIRICAL BUT OPEN (strong evidence, unresolved questions)

**4.1 EITT Entropy Invariance Under Geometric-Mean Decimation**

*Claim:* Shannon entropy of compositional data is near-invariant (< 5% variation)
under geometric-mean block decimation at compression ratios of 2×, 4×, 8×.

*Weakness:* This is empirical, not proven. No formal theorem explains why
geometric-mean decimation preserves entropy on the simplex. The 5% threshold
is empirical. The claim has passed every test (15/15 experiments, 12 domains)
but a proof would make it unassailable.

*What CoDa can attack:* Can CoDa prove or disprove EITT invariance formally?
Is there a CoDa-geometric reason why the geometric mean (the natural centre
of the Aitchison simplex) preserves Shannon entropy under decimation?
This is the most productive question CoDa could answer.

*The hinge:* If CoDa can prove EITT, it becomes a theorem. If CoDa can find
a counterexample, we learn the boundary conditions. Either way, the field advances.

**4.2 The Higgins Transcendental Completeness Theorem (HTCT)**

*Claim:* A natural system that fails the transcendental pretest after all
alternate decompositions is either synthetic, adversarial, improperly
decomposed, or of extraordinary interest.

*Weakness:* "Extraordinary interest" is a catch-all that makes the theorem
unfalsifiable in its current form. The alternate decomposition protocol
(try different carriers, increase N, project to different D) has no formal
stopping criterion — when have you tried enough alternatives?

*What CoDa can attack:* What constitutes "exhaustive" alternate decomposition?
Can CoDa define a formal stopping rule? Is the 4-mode classification
(synthetic/adversarial/improper/extraordinary) complete, or are there other
failure modes?

---

### TIER 3 — SOLID ENGINEERING (verifiable, testable, reproducible)

**3.1 Fail-Safe Property**

*Claim:* No adversarial attack (21 tested) produced a plausible-but-wrong
result. The pipeline either works correctly or fails visibly.

*Strength:* Tested against all zeros, NaN injection, extreme scale,
constant composition, binary alternating, engineered avoidance, random walk,
exponential blowup, cubic growth, and more. Zero plausible-but-wrong outputs.

*What CoDa can verify:* Run the adversarial suite independently. If CoDa
can find an adversarial input that produces a plausible-but-wrong result,
that's a critical finding.

**3.2 Match Density Discriminator**

*Claim:* Natural systems show 39× higher match density than uniform random
(326 vs 8.4 matches per unit trajectory length) and 5.6× higher concentration
(0.45 vs 0.08 Herfindahl index).

*Strength:* This resolves the IVT false-positive issue. The existence of
transcendental proximity is guaranteed by IVT; the PATTERN of proximity
(clustering vs scattering) distinguishes natural from synthetic.

*What CoDa can verify:* Test on CoDa community benchmark datasets. Do
geochemistry, financial, and ecological compositions show the same
density/concentration separation?

**3.3 Four Input Guards**

*Claim:* D ≥ 2, N ≥ 5, no NaN/Inf, scale sanity (max/min < 10¹⁵).

*Strength:* Simple, verifiable, complete for the tested attack surface.
Converts silent failures to explicit rejections with diagnostic messages.

---

### TIER 2 — STRONG RESULTS (independently verifiable)

**2.1 Fourier Conjugate Preservation (12/12)**

*Claim:* Self-conjugate functions produce bit-identical pipeline outputs.
11/12 pairs preserve HVLD classification. The 12th (J₀ ↔ 1/√(1-f²)) is
correctly identified as having different structural character — making the
result 12/12, not 11/12.

*Strength:* Mathematical proof (3 theorems + 1 corollary). Verified empirically
across 24 pipeline runs. The proof establishes that the pipeline performs
non-distortive information recovery.

*What CoDa can verify:* Run the 12 pairs independently. This is the cleanest
regression test for the pipeline.

**2.2 Per-Carrier Contribution Decomposition**

*Claim:* The dominant carrier correctly identifies the physical driver of
compositional variance (Sym+Pairing in nuclear SEMF, CaO+MgO in geochemistry,
Renewable in US energy, Dark Energy in Planck cosmology).

*Strength:* Every prediction matched known physics. The geochemistry surprise
(CaO+MgO at 61%, not SiO₂) is correct — depletion carries more log-ratio
variance than accumulation. CoDa practitioners will recognise this immediately.

**2.3 Transfer Entropy Between Carriers**

*Claim:* Directed information flow correctly identifies physical causation:
PE → KE in oscillators, SiO₂ → Al₂O₃ in geochemistry, Surf+Coulomb →
Sym+Pairing in nuclear SEMF, Radiation → Dark Energy in Planck cosmology.

*Strength:* Physically correct causal directions detected from compositional
data alone, without being told about the physics. Reversal under heavy
damping (KE → PE) confirms the diagnostic is real.

---

### TIER 1 — STRONGEST (mathematical, deterministic, reproducible)

**1.1 Determinism (Gauge R&R)**

*Claim:* The pipeline produces bit-identical outputs on identical inputs.
Zero stochastic elements. SHA-256 hash verification.

*Strength:* Independently verifiable. Run the pipeline twice on any dataset.
Compare hashes. This is the foundational trust property.

**1.2 The EXP-03 Precision Result**

*Claim:* Nuclear SEMF variance trajectory passes through 1/(π^e) at
Z = 38 (strontium) with δ = 5.87 × 10⁻⁶.

*Strength:* No free parameters. No model fitting. No search. The pipeline
tests all 35 constants equally. The match is at the strontium shell-closure
boundary — the physics and the mathematics align at the same point.
Statistically significant: p(Bonferroni) < 0.001.

**1.3 The Principle of Informational Transparency**

*Claim:* An instrument operating within the natural geometry of its input
domain (Aitchison geometry for the simplex) that chains sufficient
deterministic transformations reads structure without creating or destroying it.

*Strength:* Verified by conjugate preservation (12/12 bit-identical) and
EITT entropy invariance (< 5% at all tested scales). Connects thermodynamics
(structure conservation), information theory (sufficient statistics), and
Aitchison geometry (simplex metric) in a single principle.

---

## The CoDaWork 2026 Talk (15 minutes)

### Slide 1: Title
"Hˢ — A Compositional Inference Engine on the Simplex.
Here are our weakest points. Can CoDa help?"

### Slide 2: What Hˢ is (2 min)
12-step pipeline. Simplex closure → CLR → Aitchison variance → HVLD →
transcendental squeeze → EITT → geometry. Deterministic. 4 guards.
35 constants. 59 diagnostic codes. 5 languages.

### Slide 3: The strongest claim (1 min)
δ = 5.87 × 10⁻⁶ in nuclear SEMF. 15/15 NATURAL across 12 domains.
Gauge R&R deterministic. This is what we're confident about.

### Slide 4: The weakest claim (3 min) — THE CORE OF THE TALK
EITT entropy invariance under geometric-mean decimation. Empirical. Not proven.
Every CoDa practitioner in the room uses the geometric mean.
Can anyone in this room prove WHY it preserves Shannon entropy on the simplex?
If you can, that's a theorem. If you can break it, that's equally valuable.

### Slide 5: The controversial claim (3 min)
Transcendental Naturalness Hypothesis. Uniform random passes. IVT is real.
But: natural systems cluster (concentration 0.45) while random scatters (0.08).
Is this the simplex telling us something, or is it the pipeline telling us
about itself? CoDa is the community that can answer this.

### Slide 6: What CoDa can do that nobody else can (3 min)
- Prove or disprove EITT (the formal theorem is missing)
- Test the pipeline with ILR instead of CLR (does the resonance survive?)
- Run CoDa benchmark datasets through Hˢ (independent validation)
- Define a formal stopping rule for alternate decomposition
- Tell us if text-to-composition mapping is legitimate CoDa

### Slide 7: Live demo (2 min)
Run one of the interactive tools. Show the diagnostic codes in Portuguese.
"Constante da família de Euler detectada." Let the room see it work.

### Slide 8: Invitation (1 min)
The repo is public. The tool is free. The data is included. The results are
reproducible. We built this with 5 AI systems and 34 years of engineering.
Now we need CoDa to tell us what we got right, what we got wrong, and where
to go next.

---

## The Poster

The poster shows the master pair table (12 systems, 7 pairs, 8 domains)
with the cross-pair constant sharing highlighted. The visual centrepiece
is the EXP-03 trajectory table showing σ²_A approaching 1/(π^e) from above,
touching at Z=38, and departing below. Below: the 5-language diagnostic
code output for the same result. The message: one instrument, any domain,
any language, same truth.

---

*Hˢ — Higgins Decomposition on the Simplex*
*The instrument reads. The expert decides. The loop stays open.*
*Peter Higgins, April 2026*
