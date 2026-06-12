# CoDa vs CNT vs CNQ — The Three-Tier Comparison

**Status:** experimental / candidate. See [`README.md`](README.md).
**Replaces:** the two-column compare table in `HCI-CNT/coda_community/CNT_VS_CODA_BALANCE.md` once CNQ is promoted to canonical.
**Approach:** supportive / additive throughout — CoDa is the canonical foundation, CNT inherits and extends it, CNQ inherits and extends both. No tier "competes" with the previous; each adds where the previous reached its natural ceiling.

---

## At-a-glance comparison

| Dimension | CoDa | CNT | CNQ |
|---|---|---|---|
| **What it represents** | Static compositions on the simplex | Trajectories of compositions over time | Quaternion-valued trajectories on S³ (D=4) or natural-algebra extensions (D=8 bi-quaternion, D≥9 Clifford) |
| **Foundational algebra** | Aitchison geometry on the (D−1)-simplex | CoDa + named time-series operators (θ, ω, κ, σ) | CoDa + CNT + Hamilton quaternion algebra; SU(2) cover of SO(3) for D=4 |
| **Sample space** | (D−1)-simplex | (D−1)-simplex × time | S³ (D=4); SU(2)×SU(2) (D=8); Clifford-algebra group manifold (D≥9) |
| **Primary operations** | Closure, log-ratio (CLR/ILR), variation matrix, biplot, balance dendrogram, SBP, ternary, scree | All CoDa ops + bearing (atan2), angular velocity, helmsman, 4-stage atlas, depth tower, IR classification | All CNT ops + Hamilton product, quaternion exponential/log, SLERP, sandwich product, bi-quaternion factoring, spinor-parity extraction |
| **Cross-dataset method** | Ad-hoc per pair | Stage 4 module (bespoke pairwise logic) | Single Hamilton product `R(t) = Q₁(t) · Q₂(t)⁻¹` |
| **Continuous-time interpolation** | N/A (static) | Linear in CLR space (approximation) | SLERP on S³ (geodesic, exact) |
| **Provenance / determinism** | Per-toolkit; not standardised | Hash-chained at every layer; 25-experiment determinism gate | Hash-chained; CNT determinism gate inherited; additional `cnq_content_sha256` parallel field |
| **D range (natural fit)** | Any (1 to 10000+) | 2 to ~10 | 4 (sweet spot), 8 (bi-quaternion), 2-3 (degenerate to U(1) bearing), ≥9 with Clifford extension |
| **T range (typical)** | Any (static) | 10 to ~1000 | 10 to ~100,000 |
| **Bundle size N (typical)** | Any | 1 to ~10 | 1 to ~1000 |
| **Computational complexity** (per timestep) | O(D log D) for closure + log-ratio | O(D log D) for engine + O(D²) for Stage 2 atlas | O(D log D) for engine + O(N) for Hamilton products in N-bundle |
| **AI-and-User access protocol** | None standardised | CCTT v1.0 (ai-refresh/CCTT_QUICKSTART.md) | CCTT v1.0 inherited; planned CNQ-specific extension for bundle-level operations |
| **Operational checklist** | Per-tool community conventions | OPERATIONS_PROTOCOL v1.0 (root, 12 transitions) | OPERATIONS_PROTOCOL v1.0 inherited; CNQ adds 2 transitions (bundle-level analysis, cross-domain export) |
| **Cross-domain recognisability** | Recognised in stats, geology, ecology | Recognised in CoDa community + targeted partner labs | Recognised in stats, geology, ecology, robotics, computer graphics, physics, quantum information |
| **Reviewer audit form** | Methods section + supplementary data | Hash chain + JOURNAL.md per experiment + 25-corpus gate | All CNT + parallel CNQ hash + Volume IV citation chain |
| **Maturity** | Two centuries (Aitchison 1986 codified the modern toolkit) | One year (CNT v2.0.4 / Schema 2.1.0 / 2026-05) | Round-2 validated 2026-05-07; pre-engineering |

---

## Where each tier reaches its ceiling

**CoDa ceiling.** CoDa is static-composition-oriented. It can describe what a composition *is* but not how it *evolves*. When the question becomes "what does this composition do over time?", CoDa needs to be supplemented — and CNT is what provides the supplement, in the same algebraic vocabulary CoDa uses for its static analyses.

**CNT ceiling.** CNT works on the channel-by-channel decomposition of trajectories. This is excellent for D ≤ 10 and small bundles. For larger D or larger bundles, channel-by-channel arithmetic becomes the bottleneck — both computationally (everything scales by D times the number of pairs) and cognitively (the practitioner can't hold all the channels in working memory simultaneously). When the question becomes "what does this 100-trajectory bundle of D=20 composition look like cross-sectionally?", CNT needs a higher-algebra view — and CNQ provides it.

**CNQ ceiling.** CNQ uses unit quaternions for D=4 and natural Clifford generalisations for higher D. The Clifford algebra Cl(D-1) for very large D becomes computationally expensive (O(2^(D-1)) basis elements). For D ≥ 30 or so, Clifford-native operations become impractical, and CNQ would need either (a) approximation via dominant-mode reduction (project to the most variable D=4 or D=8 subspace) or (b) decomposition into multiple coupled Clifford components. This ceiling is well beyond any current corpus dataset and is a problem for CNQ v2.0+, not v1.0.

---

## Where each tier is the right choice

| Use case | Best tier | Why |
|---|---|---|
| Single static composition (one snapshot) | CoDa | Time isn't in the question; CNT/CNQ add overhead with no benefit. |
| One time-series, D=2-10, T<1000 | CNT | The CNT operating range. Channel-by-channel is fine; Stage 1+2 atlas tells the story. |
| Small bundle (≤ 10 trajectories), D=4 | CNT or CNQ | CNT works; CNQ would give SLERP and parity diagnostics for free. |
| Small bundle, D=8 | CNT for routine; CNQ for structure | CNT handles it; CNQ exposes the bi-quaternion factoring that may be the key insight. |
| Large bundle (≥ 100 trajectories) | CNQ | CNT's Stage 4 wasn't designed for this scale; CNQ's Hamilton-product approach is O(N²) in single algebraic operations. |
| Climate model output, D=20-100, T=10000+ | CNQ | CNT would work but with significant engineering. CNQ's Clifford-algebra extension is the natural fit. |
| Microbiome cohort, D=1000+, T=10-100, N=100+ | CNQ with dominant-mode reduction | CNT cannot handle D=1000 efficiently. CNQ's reduction to dominant-D=4 or D=8 subspace, with the residual carried as a CoDa-CNT-compatible JSON, is the path. |
| Cross-domain communication (with roboticists, physicists, graphics engineers) | CNQ | Quaternion vocabulary is immediately recognised; CNT's bearing/ω/κ/σ channels are not. |

---

## What survives vs what changes when going up the tiers

**What survives.**

- The Aitchison metric is preserved through all three tiers. CoDa defines it; CNT inherits it; CNQ operates on it via the SU(2) representation.
- Hash-chained provenance is preserved and extended. CNT adds the 25-experiment determinism gate; CNQ adds a parallel `cnq_content_sha256` that lets reviewers double-audit.
- The supportive / additive tone is preserved. CNQ does not claim to surpass CoDa or CNT in their respective domains; it claims to extend reach into domains the previous tiers were not designed for.
- The CCTT user/AI access protocol is preserved. CNQ inherits CCTT and extends it for bundle-level operations.
- The OPERATIONS_PROTOCOL meta-checklist is preserved. CNQ adds two new transitions (bundle-level analysis, cross-domain export) without removing any existing transition.

**What changes.**

- The natural unit of analysis changes. CoDa: one composition. CNT: one trajectory. CNQ: one bundle (which can be one trajectory if N=1).
- The natural cross-comparison operation changes. CoDa: log-ratio differences. CNT: Stage 4 bespoke pairwise logic. CNQ: Hamilton product `R = Q₁ · Q₂⁻¹`.
- The natural interpolation method changes. CoDa: N/A. CNT: linear in CLR space. CNQ: SLERP on S³ (geodesic).
- The natural cross-domain audience changes. CoDa: stats/geology/ecology. CNT: CoDa community + targeted partners. CNQ: above plus robotics/graphics/physics/quantum information.

---

## Three-tier compatibility

A CNQ analysis can always be reduced to a CNT view (per-trajectory channel decomposition) and a CoDa view (just the cleaned input compositions). The three tiers compose as a stack: every higher tier produces all the lower-tier outputs as side-products at no additional cost, plus the higher-tier-only outputs.

A reviewer auditing a CNQ result can verify at any level:
- CoDa-level: the input compositions are valid, closure holds, log-ratios are well-defined.
- CNT-level: the per-trajectory CNT JSONs reproduce the canonical content_sha256 (using the existing 25-experiment determinism gate as the meta-test).
- CNQ-level: the bundle-level Hamilton products and SLERP interpolations reproduce the canonical `cnq_content_sha256`.

Three independent levels of audit. A drift detected at any level is a real signal.

---

## When to NOT use the higher tier

- **Don't use CNT for static analyses.** A single composition snapshot is a CoDa problem; CNT adds time-series overhead with no benefit.
- **Don't use CNQ for D ≤ 3.** D=2 and D=3 don't have natural quaternion structure (D=4 is the smallest D where SO(D-1)=SO(3) is exactly the group quaternions cover). Use CNT.
- **Don't use CNQ for small bundles when CNT's Stage 4 already does what you need.** If the EMBER 8-country spectrum already answers your question via Stage 4, there's no reason to wait for CNQ to do the same thing in fewer lines of algebra.
- **Don't use CNQ if the audience is the CoDa community.** They speak Aitchison; CNT and CoDa are the right vocabulary. Save CNQ for when the audience is in adjacent fields.

---

## What surpassing means concretely

In the supportive/additive tone the project adopted:

- CNQ does not surpass CoDa; CoDa is the foundation CNQ stands on.
- CNQ does not surpass CNT; CNT is the trajectory layer CNQ refines.
- CNQ surpasses **CNT-without-CNQ** for the high-D, large-T, multi-bundle, cross-domain regime that CNT was not designed for. That regime is real and growing — climate science, multi-system economic modeling, large industrial process composition, gene-expression panels — and CNQ is the natural extension to reach it.

---

*The instrument reads. The expert decides. The hashes carry the receipts. Three tiers, one stack, each tier including and surpassing the previous within its proper domain.*
