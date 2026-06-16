# Prior‑art assessment — "Compositional Systems Kinematics"

*Is the term new? Honest answer: the **label** appears unused for this idea (with one name‑collision to avoid), but the **concept** — velocity/acceleration on the simplex — has deep roots in three established fields. This maps them, says what is genuinely distinctive in the Hˢ construction, and recommends a defensible name and citation set. Recognition, not invention — the framework's discipline. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; sources are web‑searched 2026‑06‑14, Tier‑2 (literature scan, not an exhaustive patent/Scholar search — that final pass is Tier 3).*

---

## Verdict in one paragraph

As a **named term** for "the kinematics of observed compositional‑data trajectories on the Aitchison simplex," **Compositional Systems Kinematics** appears **new** — but it **collides in name** with an existing, *different* use of "compositional kinematics" in category theory (composing kinematic *subsystems*), so the label is not collision‑free. As a **concept**, velocity/acceleration of a composition on the simplex is **well established** — explicitly in **replicator dynamics** and **information geometry**, and implicitly in CoDa's **perturbation operator**. So the honest position is: *a new synthesis and a new descriptive instrument, standing on prior art that must be cited — not a new discovery of "motion on the simplex."*

## 1 · The exact label

- **"Compositional kinematics" exists, but means something else.** arXiv **2602.20125, "A compositional framework for classical kinematic systems"** uses *compositional* in the **category‑theory** sense — composing open kinematic subsystems as morphisms — not the CoDa/simplex sense. A true homonym. → A name collision risk for "Compositional … Kinematics."
- **"compositional momentum," "compositional velocity," "simplex kinematics"** return no established defined concept (the hits are relativistic *velocity‑composition laws* — frame addition — which is unrelated).
- So **the label for our meaning is effectively unused**, but not collision‑free.

## 2 · The concept — three real prior‑art homes

**(a) Replicator dynamics — evolutionary game theory.** The strongest prior art for "velocity of a composition." The replicator equation `ẋ_i = x_i((Ax)_i − xᵀAx)` is literally described as *"the original velocity vector field"* and `ẋ_i` as *"the evolution velocity of the probability"*; evolutionary **trajectories on the simplex** are standard (Taylor & Jonker 1978; Hofbauer & Sigmund). **How ours differs:** replicator dynamics is a *prescribed model* (you supply a payoff matrix and integrate a velocity field); ours is a *descriptive read of observed data* (no model, no payoff), it uses the **Aitchison log‑ratio** velocity (not Euclidean share‑velocity `ẋ_i`), and it adds a mass‑weighted momentum and a full higher‑order tower.

**(b) Information geometry — Amari and successors.** The deepest prior art. The literature *"considers curves mapping time to probability distributions and looks for proper definitions of **velocity and acceleration**"*; m‑/e‑geodesics on the probability simplex; and explicitly: *"geodesic motion on statistical manifolds … recovers the equations of motion governing **Hamiltonian mechanics**, … **replicator dynamics**, and natural gradient descent."* So velocity, acceleration, geodesics, and a **mechanics connection on the simplex already exist**. **How ours differs:** information geometry uses the **Fisher‑Rao** metric; we use the **Aitchison** metric (a different, log‑ratio geometry — though both are simplex geometries). Their work is largely theoretical/optimization (natural gradient); ours is a **deterministic descriptive instrument** for real compositional trajectories, with mass = share and a noise‑bounded jet.

**(c) Compositional data analysis itself.** CoDa has the simplex, Aitchison geometry, and the **perturbation operator** — and the literature notes *"differences between subsequent rows … using the perturbation operator … measures change in the simplex geometry,"* and *"exponential decay describes straight lines in the simplex."* So the **velocity is implicit** in CoDa (perturbation between successive compositions). Compositional **time‑series** models exist (VARIMA, Dirichlet‑ARMA, Bayesian compositional forecasting). **How ours differs:** CoDa frames this as *perturbation + PCA/VAR*, **not** as kinematics — it does **not** use velocity/acceleration/momentum/force vocabulary or a mechanics instrument (confirmed: CoDa sources "do not contain … kinematics … velocity, acceleration, trajectory concepts"). Our contribution is precisely to **read CoDa's perturbation as kinematics** and build the descriptive mechanics on it.

## 3 · What appears genuinely distinctive in the Hˢ construction

Not "motion on the simplex" (that exists), but the specific assembly:
1. A **descriptive deterministic instrument** over *observed* compositional trajectories — not a prescribed dynamical model (replicator) and not an optimizer (natural gradient).
2. In the **Aitchison (log‑ratio)** metric specifically — distinct from Fisher‑Rao (info geometry) and Euclidean shares (replicator).
3. **Mass = share → momentum/force** as the "arrow of intent," and the demonstrated **momentum ≠ helmsman** (mass‑weighted vs mass‑blind). I find no prior art for this specific mass‑weighted descriptive read.
4. The **complete kinematic+dynamic tower as one read** — jet (velocity→acceleration→…), Frenet curvature, momentum/force/energy/action, spectral modes — with an explicit **noise‑bounded maximum order N\*** as an honesty ceiling.
5. The **honesty layer** (coherence gate on the arrow; resolvability on the jet) — descriptive, never predictive.

## 4 · Recommendation

- **Position as recognition + synthesis, not invention.** "We read the compositional perturbation as kinematics and build a deterministic descriptive mechanics on the Aitchison manifold — connecting CoDa to the velocity/acceleration language already used in replicator dynamics and information geometry." Cite all three.
- **Reconsider the exact label** to dodge the category‑theory collision and to be precise about the metric. Defensible options, most distinctive first: **"Aitchison Kinematics"** / **"Compositional Trajectory Mechanics"** / **"Simplex Trajectory Kinematics."** If "Compositional Systems Kinematics" is kept, define it explicitly and note the category‑theory homonym in a footnote.
- **Required citations:** Aitchison (1986); Egozcue & Pawlowsky‑Glahn (Aitchison geometry, perturbation); Taylor & Jonker 1978 / Hofbauer & Sigmund (replicator dynamics velocity field); Amari (information geometry, velocity/acceleration on the simplex). The novelty claim is the **descriptive instrument + mass‑weighted momentum + noise‑bounded tower in Aitchison geometry**, not the existence of compositional velocity.
- **Claim tier:** the *instrument and its computed values* — Tier 1; *the kinematics framing on the Aitchison manifold* — Tier 2 (sound, with the prior art above); *absolute terminological novelty* — **Tier 3, and partly refuted** (the concept is not new; the label is new but collides). A final Scholar/patent pass is the remaining Tier‑3 step before any public novelty claim.

## Sources (web‑searched 2026‑06‑14)

- arXiv 2602.20125 — *A compositional framework for classical kinematic systems* (the category‑theory homonym): https://arxiv.org/abs/2602.20125
- *Information Geometry of the Probability Simplex: A Short Course* (arXiv 1911.01876): https://arxiv.org/pdf/1911.01876
- *Transport information geometry: Riemannian calculus on the probability simplex*: https://link.springer.com/article/10.1007/s41884-021-00059-1
- *The Replicator Dynamic* (lecture notes, Imperial): https://www.ma.imperial.ac.uk/~svanstri/GamesAndDynamics/The%20Replicator%20Dynamic%20(Draft).pdf
- Pawlowsky‑Glahn & Egozcue, *Lecture Notes on Compositional Data Analysis*: http://www.sediment.uni-goettingen.de/staff/tolosana/extra/CoDa.pdf
- *Modelling Compositional Data — the Sample Space Approach* (perturbation, straight lines in the simplex): https://link.springer.com/chapter/10.1007/978-3-319-78999-6_4
