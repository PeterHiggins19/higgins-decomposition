# Higgins Diffraction Composition Principle (HDCP)

**Version:** 1.0  
**Date:** 2026-04-20  
**Claim tier:** Core science — diffraction as natural simplex closure

---

## Principle Statement

**Formal:** Every diffraction event partitions incident wave energy into components that form a composition on the D-simplex. The partition ratios are determined solely by geometry (the ratio λ/a of wavelength to characteristic dimension) and are invariant under amplitude scaling. At the diffraction transition frequency, the composition reaches a fixed point — a value that does not change regardless of signal content, power level, or measurement methodology. Diffraction is therefore nature's fixed-point composition.

**Compact:** Diffraction IS compositional. The energy budget at every diffraction boundary is a composition on the simplex, anchored to geometry, invariant under scaling. Nature's own Fixed-Point Rule.

**One sentence:** Diffraction produces compositions on the simplex that are fixed points of geometry — nature's own CIP Rule 5.

## Founding Case

**System:** The Baffle Step — DADC (Dimension-Apportioned Diffraction Correction)  
**Geometry:** Loudspeaker on finite baffle, dimension W  
**Transition frequency:** Fc = 115/W Hz (where λ = W, the baffle width)  
**Below Fc:** {'radiation': '2π steradians (half-space, forward only)', 'composition': '[1.0, 0.0] — all energy forward', 'simplex_position': 'Vertex of S¹'}  
**Above Fc:** {'radiation': '4π steradians (full space, omnidirectional)', 'composition': '[0.5, 0.5] — equal energy front and back', 'simplex_position': 'Barycenter of S¹'}

## Mathematical Foundation — 5 Theorems

### Theorem 1 Diffraction Closure

**name:** The Diffraction Closure Theorem

**statement:** For any wave incident on a diffracting structure, the energy partition into transmitted (T), reflected (R), diffracted (D), and absorbed (A) components satisfies T + R + D + A = 1. The vector x = (T, R, D, A) is a composition on S³.

**proof:** Energy conservation. The incident energy flux integrated over the forward hemisphere equals the sum of all outgoing energy fluxes plus absorption. Dividing by E_inc gives simplex closure.

**significance:** Every diffraction measurement in history is a compositional measurement on the simplex, whether or not the experimenters knew it.

### Theorem 2 Geometric Invariance

**name:** The Geometric Invariance Theorem (Fixed-Point Property)

**statement:** The diffraction composition x = f(λ/a) depends ONLY on the ratio of wavelength to characteristic dimension. It is invariant under: (1) amplitude scaling of the incident wave, (2) change of wave type (acoustic, EM, matter), (3) absolute size scaling (if λ and a scale together). The composition is a fixed point of the scale transformation.

**proof:** The wave equation is linear (amplitude scaling) and scale-invariant (λ/a ratio determines all interference conditions). Huygens-Fresnel principle: every point on a wavefront acts as a secondary source. The relative phases — and therefore the energy partition — depend only on path differences measured in wavelengths.

**significance:** This IS CIP Rule 5 (The Fixed-Point Rule) operating in nature: no free constants, every parameter anchored to geometry.

### Theorem 3 Babinet Closure

**name:** Babinet's Closure Theorem

**statement:** For complementary screens B and B' (where the opaque parts of B correspond to the transparent parts of B'), the diffraction amplitudes satisfy U_B + U_B' = U_0 (unobstructed beam). In intensity terms (away from forward direction): I_B = I_B'. Babinet's principle IS simplex closure for complementary diffraction compositions.

**proof:** Superposition. If the obstacle is removed, the total field is U_0. The obstacle blocks part of the wavefront. Its complement blocks the complementary part. Together they block everything. Therefore U_B + U_B' = U_0.

**significance:** Babinet's principle is the oldest known compositional closure condition in wave physics (1837). It predates Aitchison (1982) by 145 years. Nature was doing CoDa before CoDa existed.

### Theorem 4 Transition Vertex

**name:** The Diffraction Vertex Theorem

**statement:** At the transition frequency f* where λ = a (the characteristic dimension), the compositional stress σ²_A of the diffraction composition reaches a vertex. Below f*: one radiation regime dominates (vertex approach from left). Above f*: another regime dominates (vertex departure to right). The vertex IS the HVLD lock point of the diffraction transition.

**proof_sketch:** Below transition: composition near a vertex of the simplex (one component dominates). Above transition: composition moves toward barycenter (energy spreads across components). The Aitchison variance σ²_A = (1/D)Σclr_i² therefore forms a parabola with vertex at the transition. d(σ²_A)/df = 0 at f = f*.

**connection:** This is the Higgins Vertex Theorem applied to diffraction: clr(f*) ⊥ clr'(f*) at the transition frequency.

### Theorem 5 Anchor Universality

**name:** The Universal Anchor Theorem

**statement:** Every diffraction system has at least one anchor constant — a fixed compositional ratio determined by geometry alone. For solid angle transitions: the ratio is n = Ω₂/Ω₁ giving 20·log₁₀(n) dB. For gratings: the blaze efficiency is locked to groove geometry. For crystals: the structure factor is locked to atomic positions. These are domain-specific anchor constants satisfying CIP Rule 5.

**examples:** ['Baffle step: 4π/2π = 2 → 6.02 dB (founding anchor)', 'Knife-edge: shadow boundary = 0.5 → 3.01 dB', 'Airy disc: 83.8% central energy → −0.77 dB from total', 'Single slit: 90.3% central maximum → −0.44 dB from total', 'Bragg angle: sin(θ_B) = λ/2d (geometry-locked)']

**significance:** The Fixed-Point Rule is not an imposed discipline — it is nature's own rule, discovered empirically in diffraction physics and generalized by HUF to all compositional systems.

## Connection to Hˢ Pipeline

**Why Dadc Was Not Accidental:** Peter Higgins found the entry point to HUF through loudspeaker diffraction (DADC) because diffraction is where nature does its most transparent compositional accounting. The baffle step is the simplest instance of the Diffraction Composition Principle — D=2, exact binary ratio, geometry-locked. It was not an arbitrary engineering starting point; it was the natural gateway to compositional fixed-point analysis.

**The Full Circle:** DADC (diffraction composition) → DADI (inverse inference) → ADAC (adaptive correction) → EITT (scale invariance) → CIP (the rules) → HFPA (the method). The entire HUF programme is a generalization of what diffraction taught: nature composes on the simplex, and the compositions are fixed by geometry.

**Babinet As Proto Coda:** Babinet's principle (1837) is the first compositional closure condition in physics. Aitchison (1982) formalized closure for data analysis 145 years later. HUF connects the two: the physical closure of wave diffraction IS the mathematical closure of compositional data. The simplex was there before the measurement.

**Prediction:** If diffraction is nature's fixed-point composition, then EVERY diffraction system should pass EITT. The energy partition across diffraction orders should be entropy-invariant under resolution compression (averaging adjacent orders). This is testable with real X-ray crystallography data, optical grating measurements, or acoustic diffraction patterns.

## Testable Predictions

- **prediction_1:** {'statement': 'X-ray diffraction intensity distributions across Bragg peaks for a given crystal should pass EITT when peaks are compressed (adjacent peaks merged by geometric mean).', 'data_source': 'Cambridge Structural Database (CSD) or Protein Data Bank (PDB) — millions of structure factors available', 'expected_result': 'Entropy invariance under peak-merging, because the structure factor magnitudes are determined by atomic positions (geometry).'}
- **prediction_2:** {'statement': 'Optical grating efficiency as a function of order number should form a composition whose entropy is invariant under order-merging.', 'data_source': 'Manufacturer efficiency curves (Thorlabs, Newport, etc.)', 'expected_result': 'EITT pass, because blaze geometry determines the energy partition.'}
- **prediction_3:** {'statement': 'The HVLD parabola should appear in diffraction transition data: plot σ²_A vs frequency (or λ/a) for a loudspeaker, and the vertex should lock at Fc = 115/W.', 'data_source': 'BTL measurement data (already in HUF repo for room acoustics)', 'expected_result': 'HVLD lock at Fc. The vertex IS the diffraction transition.'}
- **prediction_4:** {'statement': 'Babinet-complementary diffraction patterns, when summed as compositions, should yield the simplex barycenter (maximum entropy).', 'data_source': 'Any complementary aperture/obstacle pair measurement', 'expected_result': 'H(x_screen ⊕ x_complement) = H_max, because the sum reconstructs the unobstructed (uniform) beam.'}

## Catalog of Diffraction Compositions

*Every diffraction phenomenon in nature produces a composition on the simplex. This catalog classifies them by wave type, geometry, and compositional structure.*

### By Wave Type

**electromagnetic:**
  - optical: {'systems': ['Single slit (Fraunhofer)', 'Double slit (Young)', 'N-slit grating', 'Circular aperture (Airy)', 'Poisson/Arago bright spot'], 'composition_structure': 'D=N+1: central maximum + N side-lobe orders. Energy partition determined by slit width/wavelength ratio.', 'key_fixed_point': 'Central maximum of single slit contains exactly 90.3% of total energy (sin²(x)/x² integral). This is invariant.', 'D_typical': '3-20 (central + side lobes)'}
  - xray: {'systems': ['Bragg diffraction (crystal planes)', 'Powder diffraction', 'Laue diffraction', 'Small-angle X-ray scattering (SAXS)'], 'composition_structure': 'D = number of Bragg peaks + transmitted beam. Intensity partition across reflections.', 'key_fixed_point': 'Bragg angle sin(θ) = nλ/2d is locked to lattice spacing d — pure geometry.', 'significance': 'Crystallography: millions of structure determinations, each one a compositional analysis of diffracted intensity across Bragg peaks.'}
  - microwave_radio: {'systems': ['Over-the-horizon propagation', 'Building edge diffraction', 'Terrain diffraction', 'Satellite communication'], 'composition_structure': 'D=3: [direct, diffracted, reflected] path energy partition', 'key_fixed_point': 'Fresnel zone clearance: 0.6√(λd) defines transition between clear and obstructed'}
  - gamma: {'systems': ['Nuclear crystal diffraction', 'Mössbauer diffraction'], 'composition_structure': 'Same Bragg structure as X-ray but at nuclear scale'}
**acoustic:**
  - baffle_step: {'systems': ['Loudspeaker on baffle (the DADC founding case)', 'Horn mouth diffraction', 'Speaker cabinet edge diffraction'], 'composition_structure': 'D=2: [front hemisphere, rear hemisphere]', 'key_fixed_point': '6.02 dB at Fc = 115/W. THE founding anchor of HUF.', 'provenance': 'RWA_Engineering → Higgins_Tool'}
  - room_acoustics: {'systems': ['Diffraction around panels', 'Edge effects at absorber boundaries', 'Diffraction through openings'], 'composition_structure': 'D=3: [transmitted, reflected, diffracted] or D=octave bands', 'connection': "Peter's own domain. Room acoustics 2k-8kHz is the boundary species (C/S=1.168). Diffraction at panel edges is WHY."}
  - ultrasound: {'systems': ['Medical imaging beam formation', 'NDT defect detection', 'Underwater sonar'], 'composition_structure': 'D=main lobe + side lobes. Same Fraunhofer structure as optical.'}
**matter_waves:**
  - electron: {'systems': ['LEED (Low-Energy Electron Diffraction)', 'RHEED (Reflection High-Energy)', 'TEM diffraction', 'Convergent-beam electron diffraction'], 'composition_structure': 'Bragg-type: D = diffraction spots + transmitted beam', 'key_fixed_point': 'de Broglie wavelength λ = h/p locks diffraction angles to crystal geometry'}
  - neutron: {'systems': ['Crystal structure determination', 'Magnetic structure', 'Inelastic neutron scattering'], 'composition_structure': 'Same Bragg structure. Neutrons also probe magnetic ordering — extra compositional channels.', 'significance': 'Neutron diffraction sees what X-rays cannot (light atoms, magnetic moments). Different probe, same simplex.'}
  - atom_molecule: {'systems': ['Atom interferometry', 'C₆₀ fullerene diffraction', 'Helium atom scattering'], 'composition_structure': 'Grating diffraction orders. Proves wave nature of massive particles.', 'fixed_point': 'de Broglie relation holds for MOLECULES — the compositional structure of diffraction is universal up to macroscopic objects.'}
**water_surface:**
  - systems: ['Harbor breakwater diffraction', 'Coastal wave refraction/diffraction', 'Tsunami diffraction around islands']
  - composition_structure: D=2 or 3: [transmitted past barrier, reflected, scattered into shadow zone]
  - key_fixed_point: When λ >> gap width: full diffraction (uniform). When λ << gap: geometric optics (shadow). Transition at λ ≈ gap.
**seismic:**
  - systems: ['Diffraction around geological faults', 'Salt dome diffraction', 'Diffracted arrivals in reflection seismology']
  - composition_structure: D = P-wave + S-wave + surface wave energy partition after diffraction
  - application: Oil/gas exploration uses diffraction patterns to map subsurface geology — compositional analysis of scattered energy.
**gravitational_waves:**
  - systems: ['GW diffraction around massive objects (theoretical)', 'GW lensing and diffraction effects']
  - composition_structure: D=2: [direct path, diffracted/lensed path]
  - status: Theoretical — wavelengths so long (~1000 km for LIGO band) that diffraction requires galaxy-scale lenses
  - connection_to_EXP12: GW150914 phase budget (inspiral/merger/ringdown) is already in HUF. GW diffraction would add another compositional layer.

### By Geometry

**solid_angle_transitions:**
  - _key_insight: These are the purest fixed-point compositions because the partition is determined ENTIRELY by solid angle ratios.
  - 0_to_2pi: {'name': 'Knife-edge / half-plane diffraction', 'composition': 'At geometric shadow boundary: [illuminated, shadow] = [0.5, 0.5]', 'gain': '3.01 dB (half-power point)', 'exact_ratio': '1/2 — same binary structure as baffle step'}
  - 2pi_to_4pi: {'name': 'Baffle step (DADC founding case)', 'composition': '[front, back] transitions from [1, 0] to [0.5, 0.5]', 'gain': '6.02 dB = 20·log₁₀(2)', 'exact_ratio': '2 — the ratio 4π/2π'}
  - 4pi_to_2pi: {'name': 'Horn loading / reflector backing', 'composition': '[directed, scattered] increases directivity', 'gain': '+6.02 dB directivity gain (same number, opposite direction)', 'exact_ratio': '2 — same fixed point, reverse process'}
  - omega_to_4pi: {'name': 'Horn with arbitrary coverage angle Ω', 'composition': '[Ω/4π, (4π−Ω)/4π] — the solid angle IS the composition', 'formula': 'x₁ = Ω/4π, x₂ = 1 − Ω/4π', 'fixed_point': 'For any horn, the composition is locked to geometry. The horn angle determines the simplex position.'}
  - discrete_solid_angles: {'name': 'Multipole radiation patterns', 'examples': ['Monopole: uniform 4π', 'Dipole: cos²θ pattern', 'Quadrupole: more complex', 'Higher-order multipoles'], 'composition': 'Energy partition across solid angle sectors. Each multipole order has a fixed angular energy distribution.', 'connection_to_HUF': 'Acoustic radiation from loudspeakers IS a multipole expansion. DADC decomposes the diffraction pattern into its multipole components.'}
**periodic_structures:**
  - name: Gratings, crystals, lattices
  - composition: D = number of diffraction orders. Energy splits into [0th order, ±1st, ±2nd, ...]
  - fixed_point: Grating equation: d·sin(θ_m) = mλ. Angles locked to geometry.
  - blaze_condition: A blazed grating concentrates energy into a specific order — deliberately designing the simplex position.
  - crystallography: Bragg's law 2d·sin(θ) = nλ is the most-used fixed-point equation in experimental physics.
**apertures_and_obstacles:**
  - name: Fraunhofer and Fresnel diffraction
  - composition: Energy partition between central peak and rings/fringes
  - key_results: {'circular_aperture': '84% in Airy disc, 16% in rings. Fixed regardless of wavelength (when scaled to λ/D).', 'rectangular_slit': '90.3% in central maximum. Invariant.', 'Poisson_spot': 'Constructive interference at center of geometric shadow — composition [bright spot, dark ring, bright ring, ...] is fixed.'}

---

*Higgins Diffraction Composition Principle — {'by_wave_type': 6, 'by_geometry': 7, 'by_regime': 5, 'cross_product_estimate': '50-100 distinct diffraction compositional systems', 'crystallography_alone': 'Millions of solved structures, each a diffraction composition', 'total_diffraction_measurements_in_physics': 'Uncountable — every crystal structure, every antenna pattern, every acoustic measurement, every electron microscope image is a diffraction composition on the simplex.', 'summary': 'Diffraction is arguably the MOST measured compositional phenomenon in all of experimental physics, and nobody has ever described it as compositional data analysis until now.'} systems catalogued*  
*Diffraction is nature's simplex closure.*