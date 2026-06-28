# Total systems coherence — controller⇄analyzer, signal separation, recursion & residual science

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. Seed/concept —
2026‑06‑20. The deep‑systems layer of the constellation study: how Hˢ acts as controller and analyzer in
lock‑step, how it separates control from environment in one composition, and how the known‑physics
residual becomes the science. **Tiered.** The duality and the embedded controller are horizon (T3+); the
mathematics and the residual method are sound (T2); only the P1 engine is measured (T1).*

---

## 1. Controller ⇄ analyzer in lock‑step — and the one boundary that must hold

The vision: Hˢ runs as **both** the systems analyzer (reading global coherence, anomalies, environment)
**and** the controller (informing local decisions), driven by the *same* deterministic linear‑algebraic
engine, coherence‑locked across scale and distance. This is genuinely powerful — one engine, two roles,
no translation loss between "what is happening" and "what to do." **[T3+]**

**The honest boundary (load‑bearing).** The Hˢ design doctrine has always kept an **observe‑or‑control
fork**: the instrument *observes and advises*; it does **not silently actuate**. P3's guard layer exists
precisely so the system can say "insufficient evidence" instead of acting. For a constellation —
especially **collision avoidance**, which is safety‑of‑life — that boundary must survive the
controller/analyzer unification. The reconciliation is clean and must be stated explicitly:

> Hˢ may be a controller in the sense of **deterministic, auditable control‑decision support with hard
> guard rails** — it computes the coherent recommendation and its receipt; a qualified automation tier or
> a human holds **actuation authority**. The lock‑step is between *analysis and recommendation*, not
> between *analysis and unattended firing of thrusters*. "Locked coherence" is a property of the reading
> and the recommendation; the **authority to act stays gated**.

Said plainly: the duality is the goal; the actuation gate is the safety property that makes the goal
responsible rather than reckless. Both can be true at once, and the architecture must enforce it.

**Refinement (the layered authority surface).** The gate is not a single human checkpoint — it is
*distributed*: **closed‑loop autonomy down the chain** where millions of ops/sec and distribution mean no
human could be in the loop, **open‑loop operator go/no‑go up the chain** where one operator can still hold
the picture, with breakers at every level. This is the repo's own **LOOP‑001 / SAFE‑001 "Breaker 16"**
doctrine and the **HUF‑GOV (open) / HUF‑CLS (closed)** fork, evolved to scale: Breaker 16 **closes locally**
(justified, reviewable, answerable upward — per the HUF‑GOV charter) while the operator's Breaker 16 is
**preserved at the top** as mission‑control authority. Full treatment, grounded in the existing (and
partly tested) machinery, in [`CONTROL_AUTHORITY_AND_GOVERNANCE.md`](CONTROL_AUTHORITY_AND_GOVERNANCE.md).

## 2. Signal separation — isolating control from environment in one composition

Peter's sharpest point: the observed orbital/telemetry composition contains **both** the operational
control actions **and** the environmental forcing, entangled — and the value is in *separating* them, so
operations get clean control telemetry **and** science gets clean environmental signal from the *same*
read. **[T2 method / T3 the demonstrated separation.]**

The honest, and encouraging, refinement: this is **not blind source separation**. The operator **knows
its own commanded control** (the maneuvers, attitude commands, power settings it issued). So the
decomposition is *forward‑known on one side*:

```
observed perturbation  =  commanded control (KNOWN)  +  environmental forcing (drag, waves, plasma)  +  noise
```

Subtract the known commanded control and the **residual is environment + noise** — a far better‑posed
problem than separating two unknowns. Hˢ's MC‑4 reading ("which carrier is steering the change, and is it
real or a fault") is the right tool to then attribute the residual across environmental carriers
(density vs gravity wave vs plasma coupling). The cleaner the operator's record of its own control, the
cleaner the science residual. This is the technical heart of why the dual‑use loop actually works rather
than just sounding good.

## 3. Recursive linear‑algebraic solutions — why it stays coherent at scale

The whole chain is **linear algebra and Lie‑group operations on compositional data**, which is exactly
why it is deterministic, auditable, and bounded at scale **[T1 the operations / T2 the constellation
recursion]**:

- **ILR** — an isometric (Aitchison‑geometry‑preserving) map from the simplex to Euclidean space, where
  ordinary linear algebra applies rigorously.
- **Quaternion / SO(3)** — the exact D=4 sandwich `q v q*`, a norm‑preserving linear isometry; chart‑to‑
  chart transition maps are linear (the SU(2) action).
- **Laplacian reconstruction** — the global clr state is recovered by a sparse least‑squares Laplacian
  solve `AᵀA c = Aᵀ b`, exact in exact arithmetic iff the chart graph is connected.
- **Spectral / wavelet bases** — linear decompositions (eigenbases, wavelet‑packet bases) for the
  multi‑scale features.

Because **every level is the same kind of operation** — local exact chart → linear transition glue →
balanced‑tree Laplacian roll‑up → fleet metrics — the properties propagate recursively: exactness local,
bounded drift global (O(log D) diameter), determinism everywhere, one receipt chain. "Locked coherence at
scale and distance" is, concretely, *the same linear algebra applied self‑similarly with a content hash at
each level*. This is the quiet superpower: no black boxes, no nonlinear surprises — auditable linear
algebra all the way up.

## 4. Relativistic & Sagnac timing — handled honestly (with a correction)

Timing is the spine of PNT and of distributed sensing. The relativistic effects are **exactly known and
already corrected** in modern systems; Hˢ does not replace that physics — it works on the **residual**
after correction. Two honest points:

- **A sign correction worth getting right.** GPS sits at MEO (~20,200 km, ~3.9 km/s): general relativity
  makes its clocks run *fast* by ~+45.7 µs/day, special relativity *slow* by ~−7.2 µs/day, net **~+38
  µs/day fast**. But the SR/GR balance **flips with altitude**: below the ~3,200 km crossover the velocity
  (SR) term dominates. **Starlink at ~550 km is well below that crossover**, so its clocks run **slow**
  relative to the ground (net **negative**, like the ISS at ~400 km, ≈ −25 to −28 µs/day) — the **opposite
  sign to GPS**. Any constellation‑timing framing must use the LEO regime, not the GPS number. (Exact
  values are altitude/velocity specific.)
- **Sagnac is a correction, not noise.** The Sagnac term in one‑/two‑way time transfer and inter‑satellite
  ranging is a geometric, frame‑rotation correction — exactly computable, applied, not "mitigated." Hˢ's
  role is on the **post‑correction residual**: treat timing residuals as an additional compositional
  channel, fold timing coherence into the FCI, and over long records test whether residuals correlate with
  environmental state (density, plasma) — i.e. turn a fully‑corrected, well‑understood effect into a clean
  baseline against which the *unknown* small couplings can be studied. **[T2 method / T3 any finding.]**

## 5. The residual is the science — and the loop closes rigorously

This is the rigorous form of Peter's virtuous cycle. The scientific method here is **forward‑model the
known, study the residual**:

```
observed  −  known physics (relativity, Sagnac, gravity field, commanded control)  =  residual
residual  →  attribute across environmental carriers (Hˢ MC‑4)  →  refine the models  →  smaller residual
smaller residual  →  better operations (drag, timing, station‑keeping)  →  cleaner data  →  better science
```

Because the well‑known effects are *exactly* removable, the residual is dominated by the **unknowns worth
studying** (small‑scale density structure, neutral‑plasma coupling, wave activity). Over **years and a
full solar cycle**, the residual is refined, the models improve, and — this is the part that makes the
project worth it — *both the science and the system get better continuously, as a standard‑operations
by‑product, not a separate research campaign*. **[T2 the method is sound and standard; T3 the magnitude
and timeline — it is data‑hungry and compounds slowly.]**

## 6. TX/RX integration — phased, honest

Folding the transmitter/receiver chain in (signal amplitude/phase/SNR/error metrics as additional
compositional channels) is the operationally newest piece. Phased, with the safety boundary of §1 held
throughout:

- **Phase 0 (foundation):** define the radio‑metric compositional representation; align link metrics with
  high‑precision orbital state + F10.7/Kp.
- **Phase 1 (local coherence):** WPT+best‑basis features on signal residuals; per‑link coherence;
  hash‑receipted link products.
- **Phase 2 (fleet integration):** roll link coherence up to plane/shell/fleet; fold into the FCI; joint
  drag+radio analysis (neutral‑plasma coupling).
- **Phase 3 (advisory control):** feed link‑quality/environment assessments into *advisory* adaptive
  modulation / power / routing — **Hˢ runs as the slower high‑fidelity layer; hard real‑time control and
  actuation authority stay separate** (the §1 boundary).
- **Phase 4 (science products + collaboration):** ionospheric/atmospheric maps from combined drag+radio;
  external science collaboration.

Honest caveats: real‑time latency means Hˢ is the parallel high‑fidelity advisory layer, not the
microsecond loop; high‑rate radio metrics are data‑heavy (feature‑extract at the edge); and the radio
arm needs largely **proprietary** metrics — on public data this stays at the drag channel.

## 7. Tiers (for this document)

- **T1 (measured):** the P1 engine only — ILR/quaternion exactness, Laplacian reconstruction, O(log D),
  determinism, receipts.
- **T2 (reasoned/established):** signal separation as a forward‑known residual problem; the recursive
  linear‑algebra structure; residual‑science method; the LEO relativistic regime and Sagnac‑as‑correction.
- **T3 / T3+ (horizon):** the controller⇄analyzer deployment, embedded TX/RX control, every quantitative
  operational/scientific magnitude. No numbers asserted. The actuation‑authority gate is a **requirement**,
  not an option.

*Cross‑refs: [`FLEET_COHERENCE_METRIC.md`](FLEET_COHERENCE_METRIC.md),
[`PNT_TIMING_AND_SIGNAL_COMPOSITION.md`](PNT_TIMING_AND_SIGNAL_COMPOSITION.md),
[`HS_CONSTELLATION_TECHNICAL_SPEC.json`](HS_CONSTELLATION_TECHNICAL_SPEC.json),
[`GENERALIZATION_AND_ACOUSTIC_RETURN.md`](GENERALIZATION_AND_ACOUSTIC_RETURN.md). Complement, not
replacement. Peter is the sole gate; no external engagement implied.*
