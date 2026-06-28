# Fleet Coherence Index (FCI) — technical draft

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. Seed/concept —
2026‑06‑20. **Specification draft, not an implemented result.** Pseudocode is illustrative; the
sub‑metric definitions are reasoned **[T2]** mappings of existing Hˢ machinery onto orbital data, and
every threshold/weight/output value is **[T3]** until measured on a public dataset.*

---

## 1. What the FCI is meant to measure

A single, deterministic, hash‑receipted scalar (per shell / plane / subset, and recursively for the whole
fleet) that answers: **how consistently is this group of satellites maintaining its intended relative
geometry and behaviour right now, and how concentrated is its risk?** It is designed to sit **near 1.0
under nominal conditions** and fall as the fleet deviates or as risk concentrates — a *monitoring and
early‑warning* signal that complements (never replaces) physics‑based conjunction assessment.

It is **descriptive**: it reads what the fleet is doing; it does not predict, model, or command.

## 2. Composite definition

```
FCI = w1·C_geo + w2·C_behav + w3·C_kin + w4·C_spec + w5·(1 − R_risk)
```

with weights `w1..w5 ≥ 0`, `Σ wi = 1`, tunable per shell / mission phase / solar‑activity level. Each
term is normalized to `[0,1]`.

| term | name | what it reads | Hˢ foundation | tier |
|---|---|---|---|---|
| `C_geo` | Geometric coherence | consistency of relative positions/velocities vs intended geometry | ILR + quaternion (D=4) reading on local clusters | T1 reading / T2 mapping |
| `C_behav` | Behavioural coherence | consistency of station‑keeping effort & manoeuvre patterns | Activation Coefficient + Helmsman | T2 |
| `C_kin` | Kinematic coherence | smoothness/predictability of trajectory evolution | noise‑bounded derivatives + curvature (P4) | T2 |
| `C_spec` | Spectral coherence | consistency of frequency content & response to F10.7/Kp | Lomb‑Scargle / wavelet packet features | T2 |
| `R_risk` | Risk concentration | degree to which conjunction risk clusters in subsets | EITT‑style entropy/diversity measure | T3 |

> **Honest note on weights.** The weights are *operational parameters*, not physics. They must be set with
> domain expertise and validated; an untuned FCI is a research object, not an operational signal.

## 3. Sub‑metric sketches

**Geometric coherence `C_geo` [T1 reading / T2 mapping].** For a local cluster (a four‑part group of
satellites or of along/cross/radial deviations), map deviations from the reference geometry into ILR
coordinates and read the Aitchison change as an exact quaternion rotation (axis + angle). Coherence is
high when the cluster's rotations are mutually consistent (small spread in axis/angle) and low when they
diverge.

**Behavioural coherence `C_behav` [T2].** Treat station‑keeping effort proxies (manoeuvre cadence,
attitude‑control activity, where available) compositionally; the Activation Coefficient measures how much
effort a subset spends relative to its contribution to stability, and the Helmsman measures whether
subsets are "steering" consistently. Sudden divergence across many satellites is the signal.

**Kinematic coherence `C_kin` [T2].** From the noise‑bounded kinematics layer, compare each satellite's
along/cross/radial velocity, acceleration, and jerk against the fleet (or shell) distribution; high
"chatter"/jerk or heterogeneous curvature lowers coherence.

**Spectral coherence `C_spec` [T2].** Compare per‑satellite spectral/wavelet feature vectors (see
[`ENVIRONMENTAL_SENSING.md`](ENVIRONMENTAL_SENSING.md)); a coherent fleet shows similar dominant modes
and a *coherent* response to external drivers (F10.7, Kp). Breakdown flags differential effects or
anomalies.

**Risk concentration `R_risk` [T3].** An entropy/diversity ("effective number of regimes") measure over
relative‑geometry and drift descriptors: as distinct behaviours collapse toward a few correlated modes,
effective diversity drops and `R_risk` rises. Higher `R_risk` ⇒ lower FCI.

## 4. Determinism & receipt (the non‑negotiable property)

Every FCI evaluation is computed by a fixed procedure over fixed inputs and emits a **SHA‑256 content
receipt** over the canonical payload (the index, its five components, and the hashes of the input
orbital‑state set and reference geometry). Identical inputs ⇒ identical FCI ⇒ identical receipt, on any
conformant platform. This is the same determinism discipline as the P1 engine — it is what makes the FCI
*auditable* rather than merely indicative.

## 5. Pseudocode (illustrative)

```python
def compute_fleet_coherence(orbital_states, reference_geometry, external_drivers, weights):
    """
    orbital_states     : {sat_id: {epoch, pos, vel, elements, (effort proxies)}}
    reference_geometry : intended relative-geometry model for the shell/plane
    external_drivers   : {f107: ..., kp: ...} aligned in time
    weights            : (w1..w5), sum == 1
    Deterministic; returns FCI, components, and a content receipt.
    """
    comp   = build_fleet_composition(orbital_states, reference_geometry)   # relative, closed

    C_geo   = geometric_coherence(comp)                 # ILR + quaternion (D=4) on clusters
    C_behav = behavioural_coherence(orbital_states)     # Activation + Helmsman
    C_kin   = kinematic_coherence(orbital_states)       # noise-bounded derivatives + curvature
    C_spec  = spectral_coherence(orbital_states, external_drivers)  # wavelet/Lomb-Scargle features
    R_risk  = risk_concentration(orbital_states)        # EITT-style effective-diversity

    FCI = (weights[0]*C_geo + weights[1]*C_behav + weights[2]*C_kin
           + weights[3]*C_spec + weights[4]*(1.0 - R_risk))

    receipt = content_hash({
        "fci": FCI, "C_geo": C_geo, "C_behav": C_behav, "C_kin": C_kin,
        "C_spec": C_spec, "R_risk": R_risk,
        "states_hash": hash_states(orbital_states),
        "refgeom_hash": hash_obj(reference_geometry),
        "weights": list(weights),
    })  # full-precision canonical payload, sort_keys, UTF-8

    return {
        "fleet_coherence_index": FCI,
        "components": {"geometric": C_geo, "behavioural": C_behav,
                       "kinematic": C_kin, "spectral": C_spec,
                       "risk_concentration": R_risk},
        "content_receipt": receipt,
    }
```

Recursion: `compute_fleet_coherence` runs at cluster level, then plane, then shell, then full
constellation, reusing the balanced‑tree atlas so the global roll‑up keeps O(log D) diameter and a
single, reproducible receipt chain.

## 6. Honest limitations (read before any use)

- **No validation yet [T3].** The FCI has not been computed on real orbital data. Its dynamic range,
  sensitivity, false‑positive behaviour, and lead time vs conjunction probability are **unknown**.
- **Reference geometry is hard.** `C_geo` and `R_risk` need a well‑defined intended geometry per shell;
  defining it is an operational task requiring domain expertise.
- **Weighting is a research problem.** Until tuned and validated, the composite is a prototype object.
- **Effort proxies may be unavailable publicly.** `C_behav` likely needs operator data; on public data it
  may be partial or omitted (the FCI degrades gracefully to the available sub‑metrics).
- **Complement, not replacement.** The FCI is a monitoring/early‑warning scalar; conjunction decisions
  remain with physics‑based assessment.

## 7. The single experiment that would validate it

On a public dataset (a Starlink shell's TLEs/ephemerides + public F10.7 + Kp), compute the FCI (with the
sub‑metrics achievable from public data) across a window spanning a **known geomagnetic storm**, and test
whether the index (a) drops coherently as the storm drives the fleet, and (b) shows differential/risk
structure that *precedes* or *adds information to* per‑pair conjunction metrics. A positive, reproducible
result is the first thing in this study that could be promoted from **T3 → T1**.
