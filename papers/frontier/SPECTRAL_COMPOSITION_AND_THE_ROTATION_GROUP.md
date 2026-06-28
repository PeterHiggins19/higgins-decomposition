# Spectral composition and the rotation group — a standalone seed

*An idea worth holding: a fixed total redistributed among discrete spectral parts **by the rotation group**,
observed through a **direction-dependent projection**, is a composition in the exact Aitchison sense — and
the group doing the redistributing is the same S³ = SU(2) = Spin(3) that anchors the Hˢ D=4 exactness. This
note is **standalone**. Acoustics is where the pattern was first seen — the *jump to pattern* — but it is
**not** the claim and **not** the same physics. Author: Peter Higgins (human authorship for all claims);
AI-assisted per HUF-STD-001. Honest-broker; every claim tiered. A seed, not a result. Nothing posted.*

---

## The idea, group-first (the standalone object)

Take a quantity that lives on the sphere of directions and carries a **conserved total**. Expand it in
spherical harmonics $Y_{\ell m}$ — the harmonic analysis of the rotation group $SO(3)$ (and its double cover
$SU(2)$ when half-integer angular momentum is involved). Three features then always travel together:

1. **A closed total.** The total "weight" is fixed; a symmetry only *redistributes* it among parts (a sum
   rule / Parseval identity). That is closure — the defining property of a composition.
2. **Parts set by the group.** The relative sizes of the parts are not free; they are fixed by
   representation theory (Clebsch–Gordan / Wigner–Eckart coefficients on the quantum side; harmonic
   directivity coefficients on the classical side).
3. **An observer projection.** What any single observer measures is a **direction-dependent projection** of
   the full object — the same total looks like a different composition from a different vantage.

Call such an object a **spectral composition**. It is a composition whose geometry *is* the rotation group.
This is precisely the structure the Hˢ D=4 chart embodies: ILR coordinates of a 4-part composition are the
imaginary part of a unit quaternion, and change acts as $q\,v\,q^{*}$ on $S^3=SU(2)$. **(Tier 2 —** sound
synthesis on established harmonic analysis; the link to Hˢ's chart is structural, not yet a measured result.)

## Two faces — same mathematics, different physics

### Face A (quantum): a magnetic field splitting a spectral line — the Zeeman effect
An external field splits a level of total angular momentum $J$ into $2J+1$ sublevels; transitions give a set
of components (the simple case: a triplet — an unshifted $\pi$ line, $\Delta m=0$, and two shifted $\sigma^\pm$
lines, $\Delta m=\pm1$; the anomalous case gives more, spaced by the Landé $g$-factor). The **relative
intensities** of the components are squared Clebsch–Gordan coefficients (the Wigner–Eckart theorem) and obey
**intensity sum rules** — the total line strength is conserved and merely redistributed. The **observation
geometry** completes the picture: viewed transverse to the field you see $\pi$ (linear, parallel to the
field) plus $\sigma$; viewed *along* the field the $\pi$ line vanishes and you see only $\sigma^\pm$ as
circular polarization. Closed total, group-set parts, observer projection — a spectral composition, exactly.
*(Stark splitting in an electric field, fine and hyperfine structure are the same kind of object.)* **(Tier 2.)**

### Face B (classical): a cabinet shaping radiated sound — directivity and diffraction
A loudspeaker radiates a **conserved total power** distributed over angle; the radiation pattern expands in
the same spherical harmonics, and the construction (baffle step, edge diffraction, dispersion, enclosure
modes) shapes which harmonic content goes where. The **listening position** is the direction-dependent
projection — the same source is a different spectrum on-axis and off-axis. **(Tier 2.)**

### The honest boundary — they are NOT the same phenomenon (a live contradiction test)
Face A is **quantum** (discrete levels; quantized, often half-integer, angular momentum). Face B is
**classical wave physics** (Helmholtz equation, boundary conditions, diffraction). They share a **group and a
closure**, not a **mechanism**. Per `../CONTRADICTION_TEST_PROTOCOL.md`: the proposition *"a magnet does to
light what a cabinet does to sound (same phenomenon)"* is **rejected** — it contradicts the established
classical/quantum mechanism distinction. What survives is the weaker, true claim: *the same SO(3)/SU(2)
harmonic-plus-closure structure organizes both.* **Acoustics is the doorway to the pattern, not an identity
with it.**

## Why the rotation group, specifically — and why SU(2) not just SO(3)
Half-integer angular momentum (electron spin; odd-electron atoms) is represented faithfully only on the
**double cover $SU(2)$**, not on $SO(3)$ alone. So the natural home of a spectral composition that includes
spin is $S^3 = SU(2)$ — the **unit quaternions**, the very chart that makes the Hˢ D=4 reading *exact* rather
than approximate. The group is not a borrowed convenience here; it is the actual symmetry of the physics.
**(Tier 2 structural; the "Hˢ reads it especially naturally" consequence is Tier 3 below.)**

## The testable bridge (Tier 3 — a hypothesis, not a result)
An atom in a **ramped magnetic field** is a real compositional *time series*: as $B$ increases, the
component-intensity composition moves on the simplex, and the motion is **generated by the rotation group**.
Predictions to falsify:
- Feed Zeeman component intensities vs. field strength into the Hˢ engine; the **arrow of intent / helmsman**
  should align with the field axis with a clean physical meaning.
- The **effective dimensionality** should track $2J+1$ (the multiplet size), and EITT should sit *within*
  analysable structure where the splitting is resolved.
- The same protocol applies to **Stark** (electric field), **hyperfine** structure, and **polarization-
  resolved acoustic directivity** as independent datasets.
A clean read would be a small, concrete demonstration that the D=4 group is the **actual symmetry of a
canonical physics problem**, not a coordinate chosen for convenience. A *null* (Hˢ adds nothing over reading
the raw Clebsch–Gordan table) is equally publishable and would bound the claim.

## Status
**SEED — standalone, not a claim.** Earned content is Tier 2 (shared group + closure, established physics);
the Hˢ-specific consequence is Tier 3 (to test). Acoustics is credited as the origin of the intuition and
explicitly distinguished from the physics. No "first"; no priority. Peter is the sole gate; nothing posted.

## Addendum — the driver, too, is the rotation group (a refinement)
*Peter's observation: magnetism is present at the **source** in both faces.* Made precise, this strengthens
the seed rather than flattening it into a false identity.

- In the **loudspeaker**, magnetism is the **transducer**: a voice-coil current in the permanent magnet's
  field feels the Lorentz force ($F = BIL$) and moves the cone. The field's job is *drive*; the radiated
  *pattern* (directivity) is a separate rotation-group story set by geometry and diffraction.
- In the **Zeeman atom**, magnetism is the **level-splitter**: the energy $-\,\boldsymbol{\mu}\!\cdot\!\mathbf{B}$
  lifts the $m$-degeneracy and *creates* the spectral composition directly.

Different roles (transduction vs symmetry-breaking; classical-macroscopic vs quantum). **But the coupling has
the same form in both — a magnetic moment in a magnetic field, $-\,\boldsymbol{\mu}\!\cdot\!\mathbf{B}$ — and a
magnetic moment *is* angular momentum** (a current loop in the coil, intrinsic/orbital $J$ in the atom, with
$\boldsymbol{\mu}\propto \mathbf{J}$). Angular momentum is the **generator of $SO(3)/SU(2)$**. So in both
faces the field couples to the *generator of the very group that organizes the composition*: it selects an
axis (breaks rotational symmetry to axial), and the response sorts by rotation-group representations. The
driver and the pattern share the group **because the coupling is to the group's generator**. **(Tier 2.)**
Per `../CONTRADICTION_TEST_PROTOCOL.md`, "same phenomenon" still fails; "**same coupling to the rotation
generator**" survives — and it ties the *source* of each face to the same $SU(2)$ that anchors the Hˢ D=4 chart.

---

*Companion: [`LIGHT_AS_COMPOSITION_RIEMANN_SILBERSTEIN.md`](LIGHT_AS_COMPOSITION_RIEMANN_SILBERSTEIN.md) — the electromagnetic case (polarization/Poincaré sphere = SU(2); Riemann–Silberstein field; the two-SU(2) Lorentz decomposition). Same sphere, light instead of an atom.*
