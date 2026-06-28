# What the new engine adds — capabilities delta over the documented baseline (2026‑06)

*The additional abilities the engine now has beyond what the powerhouse "character" documents (CNTT_COMPLETE_SPECIFICATION, Higgins_Decomposition_Character_Analysis, CNTT_DIAGNOSTIC_CODES, HS_GUIDE, the attractor‑morphology paper) currently describe. Written so the spec, the code registry, and the Character Analysis can be brought current, and so a visiting expert (or the AI they bring) sees the engine as it is now, not as it was. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; every item below is Tier 1 (built + self‑tested) unless marked. Each links to its module and its kill‑test.*

---

## The one‑line summary

The documented engine was a deterministic, lossless **reader** of compositional character (helmsman, regimes, IR class, K_eff, EITT, quaternion). The new engine is the same reader **made honest about the limits of its own reading, and given a safe way to act.** It now knows when it *cannot* name a driver, when a trajectory has *collapsed in rank*, when sparsity has made the geometry an *artifact*, when motion is below its *discovered noise floor* — and it can, when asked, *close the loop* behind breakers. The character it reads now includes the character of its own confidence.

## 1. The read became honest about resolvability (new)

The documented helmsman is `argmax|Δclr|` — it always names a leader. The new engine first asks *whether a leader can honestly be named*:

- **Resolvability guard** (`engine/helmsman_guard.py`): at or near the barycentre, motion is at the numerical floor and the old argmax returned a *noise* leader that changed with the random seed. The guard now returns **None + `HM‑NUL‑WRN`** (no resolvable helmsman) and, on a true tie between carriers, **`TIE` + `HM‑TIE‑WRN`** instead of breaking it silently by column index. It reports the motion **magnitude** and the **margin** to the runner‑up, so a fragile read is visible as fragile. *(kill‑test: experiments/engine_killtest_2026-06/)*
- This is a genuine character change: the documented engine could be confidently wrong at rest; the new engine **holds its tongue when there is nothing to resolve.**

## 2. A coherent helmsman that doesn't move when an irrelevant carrier is added (new)

The documented helmsman uses CLR, which is **subcompositionally incoherent** — adding an unrelated carrier shifts the CLR centre and can change which carrier is called the driver (demonstrated: A → C on adding an irrelevant D). The new **coherent helmsman** (`engine/structural_guards.py:coherent_helmsman`) ranks carriers by pairwise log‑ratio motion, which is closure‑invariant, so the read of (A,B,C) is unchanged when D is added. The CLR helmsman is kept (it is what the oracle uses), but the engine now *also* offers the coherent read and flags that the CLR read is relative to the declared carrier set.

## 3. Rank‑deficiency / degeneracy detection (new)

The depth‑tower and stage diagnostics use `eigh`; a trajectory whose motion is confined to a subspace drives those toward near‑zero eigenvalues (an instability the documented engine did not announce). The new **SVD effective‑rank guard** (`structural_guards.effective_rank`) reports the effective number of moving dimensions (participation ratio of the singular values) and raises **`DG‑RNK‑WRN`** when motion has collapsed into a subspace — a sibling of the E‑21 carrier guard, for a different cause.

## 4. A discovered‑noise‑floor hold‑lock with hysteresis (new — and central)

This is the most consequential addition to the *character* read. The documented engine measured motion; it did not decide whether motion was *real*. The new **hold‑lock** (`structural_guards.hold_lock`) does:

- it **discovers** its trigger from two floors — the *system* noise floor (a robust estimate of the resting motion in the live data, re‑estimable online) and the *engine* numerical floor — using `noise = max(system, engine)`;
- with **hysteresis** (enter MOVING above `k_up·noise`, return to HOLD below `k_down·noise`) it **ties down near‑zero drift** and registers a structural change only when the excursion is sustained *and* the net displacement is structural;
- the held state is **announced**, never silent — the engine says "I am holding because motion is below my discovered floor," which is exactly the calibration‑cycle character of a live instrument.

This turns "regime boundary on `mean + k·std`" (documented) into a *self‑calibrating, chatter‑free structural‑change detector* that knows the difference between its own noise and a real event.

## 5. Sparsity‑regime awareness (new)

At high zero‑fraction (e.g. microbiome ~90% zeros) the CLR geometry is **dominated by the replacement δ** — the documented helmsman/CNQ read is then an artifact of imputation, not biology. The new **sparsity detector** (`engine/zero_methods.py`) raises **`GD‑SPZ‑WRN`** above a zero‑fraction threshold and adds the **Bayesian‑multiplicative** zero treatment (`GD‑ZBM‑CAL`, the CoDaWork‑favoured count‑aware, ratio‑preserving method). The engine now tells a sparse‑data user *densify before the log‑ratio*, and the zero‑robust reads (K_eff, TV, the deceptive‑drift null) are flagged as the ones that still hold.

## 6. The all‑zero / degenerate carrier guard, built and announced (was a recommendation; now Tier 1)

E‑21 (`engine/zero_methods.py` + `run_cntt` wiring) is now an **announced multi‑method zero registry**: a structural‑zero or constant carrier is dropped to a sub‑composition with a `GD‑ZRC‑CAL` / `GD‑CNC‑CAL` code instead of producing a silent `nan` that crashed the `eigh`. The documented engine had this only as a flagged recommendation; it is now built, self‑tested, and hash‑neutral on clean data. *(Commit remains at Peter's gate.)*

## 7. Precision protection of the two zeros (new infrastructure)

`engine/precise_ops.py` adds Neumaier/Kahan compensated summation for the closure and CLR‑centre reductions and an **error‑feedback accumulator** (the balanced‑twin carry) for any long‑running stateful integrator — so a value near zero stays exact and a long automation run does not accumulate a DC bias. (Honest finding: at the engine's operating D the compensated CLR is bit‑identical to numpy, so this is *not* an oracle re‑baseline — the carry matters in the stateful/control path, not the per‑step CLR.)

## 8. A safe way to close the loop (new mode — the biggest functional addition)

The documented engine is a **read‑only** navigation instrument. The new **`engine/loop_control.py:SafeLoop`** lets it, *when explicitly asked*, become a bounded controller — the first time the engine can *act*, not just read:

- states **OBSERVE → ACTIVE → TRIPPED**; closed‑loop authority is permitted only inside a **time‑boxed automation window**;
- breakers checked before any action — **`LC‑TRIP‑NAN/RATE/WIND/SAT/DOG`** — plus a manual **`LC‑ESTOP`**, latched until a human `reset()`;
- bounded authority + rate limit + dead‑band + TPDF dither (no limit cycle) + anti‑windup error‑feedback integrator + bumpless soft‑start;
- deterministic. All seven safety paths self‑test PASS.

This is a category change in what the engine *is*: an instrument that may, behind mandatory breakers, regulate a plant — built so a non‑expert hand cannot be hurt by it (see DESIGN_PHILOSOPHY and PRECISION_AND_CONTROL).

## 9. A certifiable metrological character (new framing)

The engine's determinism now has a standards‑grade reading: **gauge R&R ≈ machine epsilon** (the analysis adds no measurement variation), exact GUM‑compatible uncertainty propagation, a determinism certificate (re‑run → identical hash), and a **6σ/9σ decision gate** that withholds below threshold. The documented engine claimed determinism; the new framing makes it *conformance‑testable* — the IEEE‑754‑of‑the‑simplex character (see DETERMINISM_GAUGE_RR_AND_CONFIDENCE and stewardship/iso‑standards/PATH_TO_A_STANDARD).

## 10. The static fallback is now a documented door (new presentation)

The engine could always produce the standard static CoDa apparatus (ternary, CLR biplot, variation matrix, scree, balance dendrogram via `HCI-CNT/atlas/stage2_locked.py`), but it was undocumented as a path. It is now an explicit branch (onramp `static_only_path`): a static‑only user gets standard CoDa and is left alone — *the dynamic layer is offered, never imposed.*

---

## The delta, as a table

| Ability | Documented engine | New engine | Module / code |
|---|---|---|---|
| Helmsman at rest | always names a leader (could be noise) | **holds** — None + `HM‑NUL‑WRN` | helmsman_guard |
| Helmsman ties | broken by index, silently | **`TIE` + `HM‑TIE‑WRN`** + margin | helmsman_guard |
| Subcompositional coherence | CLR helmsman can flip on adding a carrier | **coherent pairwise‑log‑ratio helmsman** | structural_guards |
| Rank collapse | unannounced eigh instability | **`DG‑RNK‑WRN`** effective‑rank | structural_guards |
| Real vs noise motion | `mean+k·std` boundary | **discovered‑floor hold‑lock + hysteresis** | structural_guards |
| High sparsity | silent δ‑artifact | **`GD‑SPZ‑WRN`** + Bayesian‑multiplicative | zero_methods |
| Zero/constant carrier | silent `nan` → crash | **announced drop** `GD‑ZRC/CNC‑CAL` | zero_methods + run_cntt |
| Near‑zero precision | naive reductions | **compensated + error‑feedback** | precise_ops |
| Acting on a plant | read‑only | **SafeLoop with breakers + e‑stop** | loop_control |
| Metrological claim | "deterministic" | **gauge‑R&R≈0 + conformance + 6σ/9σ gate** | DETERMINISM_GAUGE_RR |
| Static‑only user | capability undocumented | **documented static fallback** | onramp / atlas Stage‑2 |

## What stays exactly as documented

The lossless tiling core (to D=10⁶), the quaternion/CNQ algebra, K_eff/Aitchison/TV, the IR classification and depth tower, EITT invariance, the diagnostic‑code taxonomy, and the frozen oracle parity — all unchanged. **Every new ability is additive and observe‑only by default; the oracle is untouched.** The new engine reads everything the old one read, and now also reads, and reports, the boundary of what it can honestly resolve.
