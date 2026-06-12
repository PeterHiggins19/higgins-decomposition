# The Tiered Compositional Analytics System — CoDa → CNT → CNQ

**Status:** experimental / candidate. See [`README.md`](README.md).
**Foundation:** [`../experiments/backblaze_fleet_quaternion/QD_ROUND_2_REPORT.md`](../experiments/backblaze_fleet_quaternion/QD_ROUND_2_REPORT.md) — quaternion identification confirmed at IEEE floor on real corpus data.

---

## The three tiers in one paragraph

The Hs project's compositional analytics now spans three tiers, each grounded in the previous and serving a different scale of problem. **CoDa** is the foundation — Aitchison closure, log-ratios, ILR, balance dendrograms; the operational layer where data is collected, validated, and made compositional. **CNT** is the middle — the trajectory-navigation tensor on top of CoDa, adding bearings, angular velocity, period-2 attractors, and IR classification; it serves field projects, single-trajectory and small-bundle analyses, the kind of work that fits in one practitioner's working memory. **CNQ** is the top — quaternion-native operations for systems too large to keep in one head: climate models with thousands of components, multi-decade economic flows, industrial composition with hundreds of variables, multi-trajectory bundles where the cross-dataset structure is the primary observable. Each tier includes the previous; each adds capability without replacing what came before.

---

## Tier 1 — CoDa (foundation)

**Role.** Grounded operational functions at the data-collection and sorting phase. The mathematical apparatus that makes a "composition" a well-defined object — closure to constant sum, log-ratio transforms, isometric basis projections, geometric means, balance dendrograms, sequential binary partitions.

**Provenance.** Aitchison (1986), Egozcue (2003), Pawlowsky-Glahn (2015). Two centuries of statistical work on the simplex, matured into a stable toolkit.

**What it does well.**
- Establishes the simplex as the natural sample space for compositional data.
- Provides the geometry (Aitchison metric) that respects scale-invariance and subcompositional coherence.
- Gives the practitioner the standard plates: variation matrix, biplot, balance dendrogram, ternary diagram, scree plot.
- Cleans, validates, and structures raw data into a form that can be further analyzed.

**What it doesn't do natively.**
- Time-series dynamics (CoDa is static-distribution-oriented).
- Cross-dataset trajectory comparison (handled ad-hoc, not as a first-class operation).
- Hash-chained provenance for individual analytical results (not a feature of the toolkit itself).

**Scale.** Any. CoDa works on D=2 commodities and D=10000 microbiome samples equally well, as long as the analyst's question is "what is the structure of this composition" rather than "how is this trajectory evolving."

**When to use it alone.** Static analyses. Cross-sectional comparisons. Initial data understanding. Anything where the question is *what* the composition is, not *what it is doing*.

---

## Tier 2 — CNT (field use, medium scale)

**Role.** The Compositional Navigation Tensor. CoDa's geometric apparatus extended with trajectory-native operators: bearings (atan2 over CLR pairs), angular velocity, helmsman (signed cumulative rotation), period-2 attractor detection, depth tower, 8-class IR classification, four-stage atlas, hash-chained provenance.

**Provenance.** Higgins (2026), built on CoDa foundations. Engine 2.0.4 / Schema 2.1.0 / Output Doctrine v1.0.1. 25-experiment determinism gate. Three-volume handbook. CCTT v1.0 user-and-AI access protocol. OPERATIONS_PROTOCOL v1.0 meta-checklist.

**What it adds over CoDa.**
- First-class trajectory dynamics: bearing, ω, κ, σ as named channels.
- Stage 1 (per-timestep ortho), Stage 2 (Order-2 atlas), Stage 3 (depth/IR), Stage 4 (cross-dataset).
- Hash-chained provenance: every JSON, every PDF, every input CSV is SHA-256 indexed.
- Determinism gate: 25 experiments pinned, every release must reproduce all 25 hashes.
- Mission Command orchestrator.
- CCTT v1.0 access protocol — any user, by hand or with AI, can produce CNT-grade output from raw data.
- OPERATIONS_PROTOCOL v1.0 meta-checklist — every operational transition has a binary checklist.

**What it doesn't do natively.**
- D ≥ 8 datasets are handled element-by-element rather than via natural higher-algebra structures (bi-quaternion factoring for D=8 would be more efficient).
- Cross-dataset comparison (Stage 4) is bespoke per-pair logic rather than single-operation algebra.
- Continuous-time interpolation between timesteps is linear in CLR space, not geodesic on the underlying manifold.
- Spinor parity (whether a trajectory lifts to the spinor or vector branch of SU(2)) is computed implicitly via LIMIT_CYCLE_P1 vs LIMIT_CYCLE_P2 termination codes, not exposed as a first-class diagnostic.

**Scale.** D = 2 to ~10. T = 10 to ~1000. Single trajectories or small bundles (8-country EMBER is the upper end of routine current use). Most current corpus experiments fit comfortably in this tier.

**When to use it.** Field projects, single domain analyses, the kind of work where the practitioner can reason about every channel by hand. The current 25-experiment corpus is exactly the CNT operating range.

---

## Tier 3 — CNQ (high performance, dimensionally larger)

**Role.** The Compositional Navigation Quaternion. CNT's operations rebuilt natively in quaternion algebra, with Hamilton products replacing channel-by-channel cross-dataset arithmetic, SLERP replacing linear interpolation, bi-quaternion / Clifford-algebra factoring exposing structure that channel-by-channel operations hide. Same scientific result; different algebra; new operations become possible.

**Provenance.** Hamilton (1843) for the underlying algebra. Aitchison (1986) and Higgins (2026) for the compositional and trajectory foundations CNQ inherits. Round 2 validation 2026-05-07 confirmed the foundational identification at IEEE floor (4.4e-16 max diff on backblaze_fleet, T=731). The connection is real.

**What it adds over CNT.**

- **Single-operation cross-dataset comparison.** Stage 4 collapses from bespoke pairwise logic to one Hamilton product `R(t) = Q₁(t) · Q₂(t)⁻¹`. The relative quaternion R(t) decomposes into relative angle + relative axis at every timestep — exactly what CNT's Stage 4 computes by hand, in one line.

- **Geodesic continuous-time interpolation.** Between-timestep interpolation becomes SLERP (spherical linear interpolation) on S³, the geodesic of the underlying manifold. Currently CNT approximates this with linear interpolation in CLR space; CNQ does it exactly.

- **Bi-quaternion factoring for D=8.** EMBER country datasets are D=8 (or D=9 with the World aggregate). D=8 admits a natural decomposition SO(8) ⊃ SU(2) × SU(2), which means each EMBER trajectory potentially factors into **two coupled quaternion paths** — one for the fossil sub-mix, one for the renewables sub-mix. This factoring is invisible to channel-by-channel arithmetic; CNQ exposes it.

- **First-class spinor-parity diagnostic.** CNQ exposes per-trajectory parity (vector branch / spinor branch) as a top-level field, not implicit in the termination code. Future researchers can ask *"is this trajectory in the spinor sector?"* directly.

- **Higher-order Clifford generalisation.** For D > 8, the natural algebra is the Clifford algebra Cl(D-1). Quaternions are the special case Cl(2); octonions are (with caveats) Cl(3). CNQ's algebra layer can extend to Clifford-algebra-native operations for very large D, providing a coordinated mathematical machinery where CNT would need bespoke logic per D.

- **Cross-domain recognisability.** Quaternion algebra is the daily working language of robotics (SLAM, orientation tracking), computer graphics (animation, rotation interpolation), physics (rigid-body dynamics, quantum information), and several other fields. Compositional analysis expressed in quaternion terms becomes immediately recognisable and adoptable in those communities, in a way Aitchison-and-Helmert language is not.

**What it doesn't change.**

- Every CNT result remains valid. CNQ reproduces every CNT content_sha256 (Round 3 will confirm at corpus scale). The 25-experiment determinism gate stands.
- The CCTT and OPERATIONS_PROTOCOL access layers continue to work — CNQ adds a Stage 5 (or Volume IV view) without removing any existing stage or volume.
- The dual-folder fault-tolerance protocol applies identically.
- Hash-chained provenance is preserved; CNQ adds a parallel `cnq_content_sha256` field, not a replacement.

**Scale.**
- D = 4 to D = 10000 cleanly (D=4 is the natural sweet spot; bi-quaternion factoring for D=8; Clifford-algebra extension for arbitrary D).
- T = 10 to T = 100,000 with linear scaling (Hamilton products are O(1) per pair; geodesic interpolation is O(T) per trajectory).
- Bundles of N trajectories: cross-dataset operations are O(N²) Hamilton products, but each is a single algebraic operation.

**When to use it.**

- Climate models. The CMIP archive contains compositional time series (atmospheric mixing ratios, ocean tracer compositions, vegetation cover fractions) at D in the tens to hundreds, T in the thousands of months.
- Multi-decade economic flows. National accounts, sector composition over decades, cross-country comparison; D in the dozens, T in the hundreds, N in the dozens.
- Industrial process composition. Refinery streams, fermentation broths, chemical process monitoring; D in the tens to hundreds, T in the thousands of samples.
- Multi-trajectory bundles where structure is primary. Microbiome cohorts (D ~ thousands, T ~ dozens, N ~ hundreds). Gene-expression panels (D ~ tens of thousands, requires Clifford-algebra extension).
- Anywhere CNT's channel-by-channel operations begin to obscure rather than reveal structure.

---

## How the tiers compose in practice

A typical large-scale analysis under the full three-tier system:

1. **CoDa** receives raw data. Closure, imputation, log-ratio transforms, validation. Output: a clean compositional time series.

2. **CNT** processes per-trajectory dynamics. Bearings, angular velocity, depth tower, IR class. Output: a CNT JSON per trajectory, hash-chained.

3. **CNQ** processes the bundle. Reads the CNT JSONs, lifts each trajectory to a quaternion path, computes pairwise Hamilton products for cross-dataset structure, applies SLERP for continuous-time interpolation, exposes spinor-parity diagnostics, factors high-D trajectories into bi-quaternion or Clifford components. Output: a CNQ JSON bundling the cross-dataset structure, plus per-trajectory CNQ supplements that extend the per-trajectory CNT JSONs.

The downward compatibility runs the other way: a CNQ-only analysis can always be reduced to its CNT view (per-trajectory channels) and to its CoDa view (just the cleaned input compositions). The hashes propagate at every layer; an auditor can verify the full chain or any single tier independently.

---

## Diagrammatically

```
┌─────────────────────────────────────────────────────────────────┐
│ CNQ — Quaternion-native large-scale analytics                   │
│   • Hamilton products for cross-dataset                         │
│   • SLERP geodesic interpolation                                │
│   • Bi-quaternion / Clifford factoring                          │
│   • Spinor-parity diagnostic                                    │
│   • Cross-domain recognisability                                │
├─────────────────────────────────────────────────────────────────┤
│ CNT — Trajectory navigation tensor                              │
│   • Bearings, ω, κ, σ channels                                  │
│   • 4-stage atlas (Stage 1, 2, 3, 4)                            │
│   • 8-class IR taxonomy                                         │
│   • Hash-chained provenance, 25-experiment determinism gate     │
│   • CCTT user/AI access protocol                                │
├─────────────────────────────────────────────────────────────────┤
│ CoDa — Compositional data analysis foundation                   │
│   • Aitchison closure, CLR, ILR                                 │
│   • Helmert / orthonormal basis                                 │
│   • Variation matrix, biplot, balance dendrogram, ternary       │
│   • Two centuries of mathematical machinery                     │
└─────────────────────────────────────────────────────────────────┘
        ▲                        ▲                       ▲
        │                        │                       │
   Climate models,       25-corpus experiments,    Cleaning, sorting,
   long economic flows,  field projects,           data validation,
   high-D bundles        single trajectories       any composition
```

---

## What this changes for the CodaWork audience

Nothing immediate. CodaWork 2026 is about CNT, and CNT works at the scale CodaWork's audience operates at. CNQ is the *next* horizon — what becomes possible after CodaWork, when the project starts engaging with adjacent communities (robotics, climate science, computer graphics, quantum information) where quaternion algebra is the daily working language.

The CodaWork talk closes with CNT and the 25-experiment corpus as the proof. The post-CodaWork conversation can open with CNQ as the proposed bridge: "we've validated the quaternion identification at machine precision; here's the proposed engineering plan; would your community find this useful?" That's the conversation that turns CNT from a single-author research line into a collaborative research direction.

---

## What this changes for current users

Nothing forced. CNT stays canon. Existing scripts, existing JSONs, existing hashes all continue to work. CNQ is opt-in for users who need its scale; CNT remains the default for everyone else.

A CNT user who wants to try CNQ can start by loading their CNT JSON into a quaternion view (when CNQ ships) and see what the additional diagnostics show. If they find the spinor-parity flag or the SLERP interpolation useful, they can adopt incrementally.

---

*The instrument reads. The expert decides. The hashes carry the receipts. CoDa cleans. CNT navigates. CNQ scales.*
