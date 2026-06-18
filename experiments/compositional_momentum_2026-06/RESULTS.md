# Compositional momentum — the arrow of intent (2026‑06)

*Peter's concept: each carrier has a **mass** (its share), a **velocity** (its log‑ratio change, Δclr), and therefore a **momentum** (mass × velocity). The system's net momentum vector is the **arrow of intent** — where the *weight* of the composition is flowing and how committed the motion is. A **descriptive vector of present motion, not a prediction.** Module: `HCI-CNTT/engine/compositional_momentum.py` (self‑test PASS). Reproduce: `python run_momentum_demo.py`. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; Tier 1 on the runs.*

---

## The definition

- **mass** mⱼ = the carrier's share (its weight in the whole), taken at the midpoint of each step.
- **velocity** vⱼ = Δclrⱼ — the Aitchison (log‑ratio) velocity per step.
- **momentum** pⱼ = mⱼ · vⱼ — per carrier.
- **arrow of intent** = the net system momentum vector **P = Σ pⱼ** over the window: its **direction** (which carriers are net receivers vs donors of momentum) and its **magnitude** (how much).
- **coherence** = ‖Σ p(t)‖ / Σ‖p(t)‖ ∈ [0,1] — is the motion a *directed arrow* (≈1) or *churn* (≈0)?
- **kinetic energy** ½ Σ mⱼvⱼ² — the energy of the compositional motion.

A near‑conservation falls out: in a closed composition Σⱼ mⱼvⱼ ≈ 0 (momentum is conserved), so the vector shows **mass redistribution** — what each carrier *receives* must come *from* others. The arrow is "from → to."

## Why it is new — momentum ≠ helmsman

The **helmsman** (= argmax|Δclr|) is **mass‑blind**: it catches the *fastest log‑ratio mover*, often a small carrier (the ratio‑blindness specialty). **Momentum** re‑weights by mass: it catches **where the bulk is shifting**. They answer different questions — *who steers fastest* vs *where the weight goes* — and on real data they **disagree**, which is the point. Use both.

## Real‑data demonstration — EMBER national energy transitions (yearly, D=8/9)

| System | Arrow: mass flowing **to** | **from** | magnitude | coherence | mass‑blind helmsman |
|---|---|---|---|---|---|
| **Germany** | Wind · Solar · Bioenergy | Coal · Nuclear · Other Renewables | 3.08 | **0.53** (directed) | Other Renewables |
| **UK** | Wind · Bioenergy · Solar | Coal · Gas · Nuclear | 2.11 | 0.44 | Other Renewables |
| **Japan** | Solar · Wind · Bioenergy | Nuclear · Gas · Coal | 0.70 | **0.15** (barely directed) | Nuclear |
| **India** | Solar · Wind | Coal · Gas · Hydro | 0.69 | 0.55 | Solar |
| **World** | Solar · Wind | Coal · Nuclear · Hydro | 0.61 | **0.90** (strongly directed) | Solar |

What it reads, honestly:
- **The arrows match the known transitions** — Germany's Energiewende (mass to Wind/Solar, from Coal/Nuclear), Japan's post‑Fukushima nuclear loss, the global coal→renewables shift.
- **Momentum and helmsman disagree every time** — e.g. Germany's *momentum* points to Wind/Solar (where the weight goes) while the *helmsman* points to "Other Renewables" (the small fastest mover). Both true; complementary.
- **Coherence is doing real work.** The **World** arrow is strongly directed (0.90 — the aggregate averages out national noise), while **Japan**'s is barely directed (0.15 — a contested, churny transition). A low coherence honestly says *there is motion but no clear net intent*. The recent‑window UK arrow (last 8 yr) drops to 0.18 — the easy coal‑exit gains are spent; the present arrow is less committed than the full‑series.

## The honesty (why it's "not a prediction")

Momentum is the **present** vector of motion. By Newton's first law it *continues absent a force* — but the instrument does **not** claim no force will act; a policy, shock, or constraint can redirect it tomorrow. So it reports *where the mass is moving now and how committed*, never *where it will be*. And it carries the same refusal as the resolvability guard: a directed arrow is reported **only when coherent** — below `coh_floor` it returns **`MO‑DIF‑WRN`** (diffuse / churn, no net intent); at rest it returns **`MO‑NUL‑WRN`**. The instrument will not draw an arrow the data doesn't support.

## Where it extends to (Tier 2)

A per‑step momentum trajectory (the arrow over time, with the hold‑lock marking when the arrow *turns*); a momentum‑vs‑helmsman pair‑read in the navigation payload; the kinetic‑energy series as a "how energetic is the transition right now" gauge; and — for the SafeLoop — momentum as the *observed* state a controller would damp toward a setpoint (still behind breakers, still not a forecast).

*Tier 1 (real data, reproducible, self‑tested). The arrow of intent is a read of the present, gated by coherence — a vector, honestly drawn, never a prophecy.*
