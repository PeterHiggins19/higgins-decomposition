# Interference‑free naming + the two‑layer architecture (a recommendation)

*Two requests answered: (1) an interference‑free name for the matured system, verified by search; (2) bringing the old tools (the frozen oracle + EITT) back as the **boundary/fringe engine** behind the deterministic instrument. This is a **recommendation** — the name is Peter's to choose; nothing is renamed here. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; interference scan is Tier‑2 (web search 2026‑06‑14), the fringe layer is Tier‑3 by construction.*

---

## 1 · The interference landscape (why descriptive names are a trap)

Compositional/simplex terminology is a **crowded, contested field** — searched and confirmed:

- **"Compositional navigation"** (our CN‑TT core term) is **heavily taken** in robotics/NLP — instruction‑following navigation, ComposableNav, "composing motion primitives." Public collision.
- **"Compositional kinematics"** is taken in **category theory** (composing kinematic *subsystems*) — the homonym from the prior‑art note.
- **"Compositional state" on the Aitchison simplex** is being actively worked by **someone else** — a 2026 paper, *"Toward Operationalizing Rasmussen: Drift Observability on the Simplex for Evolving Systems,"* doing "compositional state in Aitchison geometry, stabilized under churn." This is both a **name collision and a near‑competitor on the MC‑4/drift turf** — worth watching.
- **"Barycentric instrument"** collides with quantum instruments; **"compositional velocity/momentum"** with relativistic velocity‑composition.

**Conclusion:** every *descriptive* compositional name is occupied or contested. The only inherently interference‑free class is **eponymous**.

## 2 · Recommendation — consolidate under the eponymous name

- **System / instrument name (public):** **Hˢ — Higgins Decomposition.** Eponymous ⇒ collision‑free by construction; already established; honest; carries the lineage. This is the interference‑free choice the search points to.
- **`CN‑TT` (Compositional Navigation Tensor Train):** keep as the **internal engine‑architecture codename**, not the public name — because "compositional navigation" collides publicly. Internally it's fine; publicly, lead with Hˢ.
- **New layers:** prefix with the eponymous name to dodge the homonyms — **"Hˢ kinematics" / "Hˢ mechanics"** (not "compositional kinematics"); the dual vocabulary (`TERMINOLOGY_BRIDGE.md`) still carries the navigation + physics terms underneath.
- **The background research layer:** name it distinctly — proposal: **"the Hˢ Fringe Engine"** (or "Boundary Engine") — see §3.
- **One‑line identity:** *Hˢ (Higgins Decomposition) — the deterministic instrument that reads the most a composition can be known to say, with honest confidence, and explores the rest at the boundary.*

*(If you prefer a non‑eponymous public name, the cleanest unoccupied descriptive candidate from the scan is "Simplex Navigator," but it is weaker and less defensible than the eponymous Hˢ. The name is your call; the search says eponymous is safest.)*

## 3 · The two‑layer architecture — instrument + fringe engine

The matured system is honestly two things, and naming them apart keeps the trust clean:

**Foreground — the deterministic instrument (Hˢ core, Tier 1).** Reads the *most that can be determined with confidence*: lossless reconstruction, the navigation family, the full mechanics tower to its noise‑bounded maximum, the guard layer — and **holds at its limit** (resolvability, hold‑lock, the derivative ceiling). Trustworthy, reproducible, claim‑grade.

**Background — the Fringe / Boundary Engine (Tier 3, exploratory).** Where the instrument holds or withholds, this layer looks at the **edge** for *patterns that might reveal other patterns* — using the **old tools that got us here, which still hold something:**

- **EITT, in a new role: a boundary test** (`engine/fringe_boundary.py`, built + self‑tested). Shannon entropy is ~invariant under geometric‑mean (CoDa‑correct) decimation when the composition has coherent structure, and **drifts when the region is structureless** — so a large drift flags a **boundary of analysable structure**. *Demonstrated:* a real Germany energy series stays within‑regime (drift 0.69%), a white/structureless composition is flagged **BOUNDARY** (drift 4.5%, code `FR‑BND‑INF`). The edge where the deterministic read runs out is now itself detectable.
- **The frozen oracle, as a fringe character read.** The old engine's **attractor / IR‑class** (CRITICALLY_DAMPED … OVERDAMPED) and **transcendental‑basin proximity** (the quarantined transcendental‑constant cluster) can offer an *exploratory* fingerprint at the boundary — "does this edge sit near a known basin? what is its damping character?" Call `HCI-CNT/engine/cnt.py` for these; they are **fringe clues, never claims.**

**The honest wall between the layers:** the Fringe Engine is **Tier 3, observe‑only, quarantined** — it surfaces "here is a boundary; here is a possible pattern worth a human look," and it is never promoted to a claim without the full honest‑broker gate. This is exactly where the transcendental/conjugate exploration belongs: visible, useful for direction, and clearly fenced off from the deterministic instrument's trustworthy output. *The instrument says what it knows; the fringe engine whispers what might be at the edge — and the two are never confused.*

## 4 · What this buys

- A **public name that cannot be challenged for interference** (eponymous), with the descriptive collisions retired to internal codenames.
- A **clean two‑tier identity:** a Tier‑1 instrument you can stake a claim on, and a Tier‑3 explorer that honours "these tools still hold something" without letting fringe patterns contaminate the trustworthy core.
- A **boundary detector** (EITT's new role) that makes the *edge of analysability* itself a measured quantity — the natural complement to the instrument's "I hold here."

*Recommendation only. Pick the name; the architecture is additive and already seeded. The instrument reads with confidence; the fringe engine explores the boundary; the eponymous name keeps both clear of everyone else's.*
