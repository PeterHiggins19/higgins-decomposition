# The new engine on the three guests' own data — what it adds, and where it can go (2026‑06)

*The old results were produced by the old engine. Here the **new guard/resolvability layer** is run on the same kinds of **real** data, per guest, to show what it now surfaces — and the maximal developments each guest can derive from the improvements. Reproduce: `python run_guests_new_engine.py` (drives the guard logic, identical to the repo modules, on the real datasets). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; the runs are Tier 1 (computed on real data); the "extend to" directions are Tier 2 (sound, to build). Core CLR/helmsman/K_eff computed inline to engine spec; the new guards are the repo modules' logic verbatim.*

---

## Guest 2 — Geology (Wehner): Frielingen‑9 mudstone, real D=4 XRF, 219 samples down‑section

| Read | Old engine | New engine |
|---|---|---|
| Dominant driver | CLR helmsman = **Zr** (trace, over bulk Si/Al) | **coherent** helmsman = **Zr** — *confirmed, and now robust to which elements are in the panel* |
| Regime boundaries | `mean+2σ` step rule → **12** boundaries | **hold‑lock** (discovered floor 0.039) → **5 genuine** structural changes at depths **22.1, 177.8, 210.4, 229.9, 238.9 m**; 187 held vs 31 moving — chatter‑free, self‑calibrated |
| Dimensionality | — | **effective rank ≈ 2.05 of 3** — the chemistry moves in ~2 effective dimensions, not 3 (a *new* structural read) |
| Data quality | — | 0% zeros → log‑ratio read fully valid |

**What's new for the geologist:** the old `mean+kσ` rule fired 12 boundaries; the hold‑lock, calibrating its own noise floor from the section, registers **5** that are sustained and structural — the difference between marking every wiggle and marking the real lithological transitions. The **effective‑rank ≈ 2** finding is genuinely new: the four‑part chemistry's motion lives on a ~2‑D surface, hinting at two dominant geochemical controls. And the **coherent helmsman** means the "Zr drives it" conclusion no longer depends on exactly which oxides/elements were measured — essential when XRF panels differ between labs (directly adjacent to the collaborator's incomplete‑XRF imputation work).

**Extend to (Tier 2):** a field/flight **sniffer that holds steady through noise and flags only genuine transitions** (hold‑lock + SafeLoop driving adaptive sampling — slow down and sample densely where a structural change is registered); rank‑aware multi‑element reading at D≫4 via the tiling atlas; the 5 hold‑lock depths as automatic correlation tie‑points across cores.

## Guest 1 — Microbiome: real Crohn (D=48) + ECAM infant gut (D=37)

| Read | Result | New‑engine meaning |
|---|---|---|
| Crohn sparsity / rank | 0% zeros (prevalence‑filtered), **effective rank 36 of 47** | dense, full‑rank → log‑ratio read valid; the **global null holds** (K_eff ≈ 7.29, CD vs control not separable on diversity) — confirmed, the signal is taxon‑specific |
| ECAM maturation | **K_eff vs day_of_life ρ = 0.62** | the maturation clock is recovered from composition alone (old single‑child headline ≈ 0.71; this is the pooled cohort, honestly lower) |
| ECAM sparsity | **44% zeros** | the CLR step‑volatility is **inflated by zero‑flipping** — the hold‑lock floor blows up (≈60) and registers **no abrupt break**: maturation here is a *gradual drift*, correctly read by the **zero‑robust K_eff**, not the log‑ratio |

**What's new for the microbiome researcher:** the engine now **tells you which read to trust at which sparsity.** On the dense, filtered Crohn table the log‑ratio machinery is valid and the honest null stands. On the 44%‑zero ECAM table the log‑ratio step is dominated by zero churn — so the new sparsity awareness says *use the zero‑robust K_eff for the maturation trend* (ρ = 0.62), and don't read the log‑ratio "regimes" until you densify. The old engine would have reported log‑ratio regime numbers without that warning; the new one separates the trustworthy read from the artifact.

**Extend to (Tier 2):** a **maturation clock** (K_eff‑vs‑age, zero‑robust) plus an **abrupt‑dysbiosis detector** (hold‑lock on a prevalence‑filtered single subject — gradual vs sudden), with the **sparsity flag + Bayesian‑multiplicative** path gating the raw 90%‑zero tables; a **coherent driver‑taxon** robust to the filtering threshold the analyst picks. This is exactly the longitudinal‑cohort instrument (antibiotic/disease time‑series).

## Guest 3 — Frontier mathematics (frontier audience): Frielingen D=4 as an exact S³=SU(2) example source

| Read | Result |
|---|---|
| Quaternion identification | Aitchison step → unit‑quaternion sandwich `q v q*`, verified on 59 real D=4 steps: **max residual 4.71e‑16** — IEEE‑floor exactness, on a *third* independent real dataset (after Backblaze + Planck CMB) |
| Near‑identity precision | `precise_ops` (Neumaier): 200k tiny rotations summed exactly (**0.0** error) — the small‑rotation regime near the identity stays exact |
| Morphology | hold‑lock segments the S³ trajectory into **5 genuine structural episodes** (chatter‑free) |

**What's new for the mathematician:** the S³ = SU(2) identification was already exact; what the new engine adds is the thing that makes it a *clean example generator* rather than a noisy one — it **won't fabricate structure at rest** (resolvability), it **keeps the near‑identity (small‑rotation) regime exact** under long composition (compensated `precise_ops` — important precisely where the morphology is most delicate, near the identity), and it **segments the trajectory into genuine morphological episodes** instead of chasing noise. And the IEEE‑floor exactness now holds on a *third* unrelated real dataset, strengthening the empirical record.

**Extend to (Tier 3, questions *for* her):** the engine as a generator for the **PL→DIFF refinement study** — increase T (timesteps) → denser polygon on S³ → approach the smooth limit, with compensated precision so the refinement limit is *exact* rather than drifting; the **tiling atlas to D>4** as a generator of higher‑dimensional glued‑chart manifolds (the atlas‑connectivity = Fiedler/Laplacian obstruction is the place her topology intuition could say whether anything real is there); the IR/attractor morphology as a candidate **S³ sign‑octant partition** (conjecture). A side instrument that manufactures exact examples in the category she studies — now precise near the identity and honest about rest.

---

## The through‑line

Across all three, the new engine's gift is the same: **it tells the truth about its own reading.** For the geologist it separates 5 real transitions from 12 noisy ones and finds the chemistry is ~2‑D. For the microbiome researcher it says which read survives the sparsity and which is an artifact. For the mathematician it keeps the example‑generator exact where it matters and refuses to invent structure at rest. The old engine read; the new engine reads, and reports the boundary of what it can honestly resolve — which is exactly what each guest needs to trust it.

*Runs: Tier 1 (real data, reproducible). Extensions: Tier 2 (geology, microbiome — sound, to build) / Tier 3 (frontier — to earn). Nothing committed; Peter is the sole gate.*
