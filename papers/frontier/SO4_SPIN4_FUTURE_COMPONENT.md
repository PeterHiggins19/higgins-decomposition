# so(4) / Spin(4) — the full symmetry of the four-part chart, and its real-world value

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑20. A
frontier evaluation: the D=4 reading currently uses only the **adjoint SO(3)** (the sandwich) of a larger
structure — the full **Spin(4) = SU(2)×SU(2)** symmetry of the four‑part chart. This document records the
verified structure, flags it as a critical future component, and evaluates its value for real‑world
applications. Honest‑broker tiered: the algebra is **measured (T1)**; the applications are reasoned/
exploratory (T2/T3), claimed as directions, not results.*

---

## 0. The ladder — SO(2) → SO(3) → SO(4), and the exact double cover (context)

A D-part composition has **D−1** ILR coordinates; rotations of that space are **SO(D−1)**. The hypercomplex
ladder makes three rungs special:

- **D=3 → SO(2).** Two ILR coordinates, one angle; the abelian circle group ≅ U(1) ⊂ ℂ (the complex unit
  circle). A three-part change is a single planar rotation.
- **D=4 → SO(3) — the exact rung.** Three ILR coordinates = the **imaginary part of a quaternion**; a unit
  quaternion acts by the **sandwich** `q v q*`, an exact SO(3) rotation (axis + angle), to the IEEE floor.
  Double cover **Spin(3) = SU(2) = unit quaternions S³**. This is where the *division-algebra exactness* lives
  — ℍ is a normed division algebra and conjugation is exact.
- **D=5 → SO(4).** Four ILR coordinates = a **full quaternion** (1 real + 3 imaginary ≅ ℝ⁴); a 4-D rotation is
  the **two-sided** action `x ↦ a x b` for unit quaternions a, b (the classic construction). Six parameters.

**The exact double cover, stated precisely (the often-quoted form is loose).** `SO(4) ≅ (SU(2)×SU(2))/ℤ₂`
with `ℤ₂ = {(1,1),(−1,−1)}`; equivalently **Spin(4) = SU(2)×SU(2) = Spin(3)×Spin(3)**. The popular
"`SO(3)×SO(3) ≅ SO(4)`" is imprecise: correctly, **`SO(3)×SO(3) ≅ SO(4)/ℤ₂`** — SO(4) is a *double cover* of
SO(3)×SO(3). At the Lie-algebra level it is exact and clean: **`so(4) ≅ so(3) ⊕ so(3)`** — the six
antisymmetric 4×4 matrices split into a **self-dual** and an **anti-self-dual** 3-D piece, each satisfying the
so(3) commutators; in the quaternion picture those two pieces are exactly the **left-** and
**right-multiplication** su(2)'s of §1.

**What SO(4) adds beyond SO(2) and SO(3).** SO(2) is one angle; SO(3) is one axis-and-angle (the exact rung).
SO(4)'s new structure is that a 4-D rotation **factors into a *pair* of independent 3-D rotations** (the two
chiralities / the two su(2)'s). That second, independent handle is the whole opportunity — and §3's ranking is
about which uses make it a *real, observable* degree of freedom (e.g. translation) rather than a redundant
(gauge) one. *(Standard results; see e.g. Spin(4)≅SU(2)×SU(2) and the two-sided quaternion action `x↦axb`.)*

## 1. What is there (verified — T1)

A quaternion admits **two** independent multiplication actions — left and right — and they are different:

- **Left** multiplication generators close as an su(2) with `[L_i,L_j] = +2 ε_ijk L_k`.
- **Right** multiplication generators close as an su(2) with `[R_i,R_j] = −2 ε_ijk R_k` (**opposite
  chirality**).
- **They mutually commute:** `[L_i,R_j] = 0`.

So together the six generators span **so(4) ≅ su(2) ⊕ su(2)** — the Lie algebra of **Spin(4)**, the double
cover of SO(4) (rotations in 4‑D). All of this is re‑computed directly from the Hamilton product (no
assumptions). The verified generators (quaternion order `(w,x,y,z)`):

```
RIGHT (q → q·e),  [R_i,R_j] = −2 ε_ijk R_k :
  Rx=[[0,-1,0,0],[1,0,0,0],[0,0,0,1],[0,0,-1,0]]
  Ry=[[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]]
  Rz=[[0,0,0,-1],[0,0,1,0],[0,-1,0,0],[1,0,0,0]]
LEFT  (q → e·q),  [L_i,L_j] = +2 ε_ijk L_k :
  Lx=[[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]
  Ly=[[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]]
  Lz=[[0,0,0,-1],[0,0,-1,0],[0,1,0,0],[1,0,0,0]]
```
*(These are the corrected forms — a collective contribution had mislabeled both sets as the left family and
wrongly claimed the six span so(4) by themselves; the genuine so(4) needs the distinct, commuting left AND
right families above. This file is the verified reference for the replication kit's `app:su2` content.)*

## 2. Why it is a critical future component

The P1 reading uses **only the adjoint SO(3)** — the sandwich `q v q*` = (left by q)∘(right by q*) — which
rotates the imaginary part and fixes the real part. That is one 3‑parameter rotation. But the four‑part
chart actually carries a **6‑parameter Spin(4)** symmetry (two independent SU(2)'s). **P1 spends 3 of the 6
available degrees of freedom.** The other half — the second, independent su(2) — is sitting unused. A
structure that "leaves half its symmetry on the table" is exactly where the next capability tends to live.

## 3. Real‑world value — an honest evaluation

What the second su(2) / full Spin(4) could buy, each tagged by tier:

| direction | the idea | real‑world value | tier |
|---|---|---|---|
| **Dual‑quaternion 6‑DOF kinematics** | Spin(4)'s two SU(2)'s are the natural home of **dual quaternions**, the standard tool for rigid‑body pose (rotation **+** translation = SE(3)) in robotics, graphics, aerospace, and **satellite attitude+position** | a *single exact compositional object* that reads orientation **and** displacement together — directly relevant to the constellation pose/control and the SMT‑line kinematics | **T2** (the math is exact; the Hˢ use is a sound mapping, undemonstrated) |
| **Two‑channel D=4 reading** | use the two independent su(2)'s to read **two conjugate aspects at once** — e.g. a composition *and* its rate, or amplitude *and* phase — instead of one rotation | a richer single‑chart read (state + motion in one exact object), reducing the need to pair separate reads | **T3** (hypothesis; needs a worked construction) |
| **Two‑helicity / electromagnetism** | the complexification so(3,1)\_ℂ ≅ su(2) ⊕ su(2) is the algebra behind the **Riemann–Silberstein** two‑helicity description of light (the EMF/light‑as‑composition frontier seed) | a principled bridge from the D=4 chart to electromagnetic field structure — the acoustics/optics frontier | **T3** (frontier seed; see `LIGHT_AS_COMPOSITION_RIEMANN_SILBERSTEIN.md`) |
| **Richer atlas glue** | tiling transition maps could use the **full Spin(4)** rather than only SO(3), adding degrees of freedom in how charts are glued | potentially better‑conditioned high‑D reconstruction or new invariants on the atlas | **T3** (exploratory; must be tested against the current O(log D) result) |
| **Isoclinic/screw structure** | left vs right isoclinic rotations in 4‑D are the screw‑motion decomposition | a clean language for coupled rotate‑and‑advance motions (robotics, orbital transfers) | **T2/T3** |

**Strongest near‑term value:** the **dual‑quaternion 6‑DOF** direction — because it is (a) exact math, (b) a
mature, widely‑used real‑world tool (robotics/aerospace already trust dual quaternions for pose), and (c)
directly aligned with the constellation control + the SMT‑line kinematics already in the project. It is the
one to prototype first.

## 4. What is NOT claimed

Spin(4) does **not** change P1's results or claims — P1 correctly uses the adjoint SO(3) and is exact. No
performance, accuracy, or capability gain from the second su(2) has been demonstrated; §3 is a tiered map
of *where value would come from*, not a result. The exact division‑algebra reason D=4 is special (and why
high‑D needs tiling, not a native rotor) is unchanged — Spin(4) is the **full local symmetry of that same
exact rung**, not a new rung.

## 5. The next step — ✅ BUILT AND PASSED (2026-06-23): dual-quaternion SE(3) 6-DOF

The minimal **dual‑quaternion demonstration** named here is now **built, tested, and receipted**
(`experiments/so4_dualquaternion_2026-06/`): a rigid‑body pose (rotation **+** translation) of a four‑part
compositional configuration encoded as one unit dual quaternion `η = q_r + ε q_d`, with exact read‑back of
**both** orientation and displacement to the IEEE floor, exact rigid‑motion composition, the screw (Chasles)
decomposition, and a determinism receipt. **All eight checks pass:**

- `so(4) = so(3)_L ⊕ so(3)_R` commutators recomputed from the Hamilton product — **exact 0**;
- two‑sided `x ↦ q_L x q_R^*` a genuine SO(4) element — orthogonality **8.9e‑16**, det **1.6e‑15**;
- Spin(4) double cover `(q_L,q_R) ≡ (−q_L,−q_R)` — **exact 0**;
- pose round‑trip and rigid‑motion composition vs the homogeneous 4×4 — **~1.1–1.4e‑14**;
- **four‑form conformance** (dual‑quaternion sandwich · extract‑then‑`Rp+t` · homogeneous 4×4) on a real
  4‑part composition's ILR point — agree to **1.4e‑14**;
- determinism — full re‑run byte‑identical. **Receipt `b0fd32a2a1eac074d68024861bb9229a6998b436252a8fea94e6b9652979c813`.**

The four‑form cross‑check **caught a real bug** on the first run (the wrong point‑transform conjugate; the
correct one is the combined `η⋆ = q_r^* − ε q_d^*`) — the receipt corrected the claim before it shipped.

**Tier move.** The **capability** (the second `su(2)` carrying translation as an exact, deterministic,
receipted object) is now **T1 — built and measured**, no longer "named but not built." What remains **T2** is
the *application* to a real constellation pose/control or SMT‑line trajectory (a sound mapping, not yet run on
field data). Full write‑up: `experiments/so4_dualquaternion_2026-06/RESULTS_so4_dual_quaternion.md`.

## 6. Evaluation of the multi-agent SO(4) framework (Grok, 2026-06-22) — honest broker

Grok proposed a full SO(4) multi-agent framework: hold a **global** frame (left $\mathfrak{su}(2)$) and a
**local/sensor** frame (right $\mathfrak{su}(2)$) independently, with a 50-agent synthetic experiment
**labelled "demonstrated."** Verified:

- **Correct (credit):** the $\mathfrak{so}(4)=\mathfrak{su}(2)\oplus\mathfrak{su}(2)$ decomposition, the
  commuting factors, the bi-invariant curvature `K = ¼‖[X,Y]‖²` (positive within each $\mathfrak{su}(2)$,
  **zero in mixed planes**), geodesics = one-parameter subgroups, and the **Kepler / hydrogen-atom hidden
  $SO(4)$ symmetry** (angular momentum + Runge–Lenz closing into $\mathfrak{so}(4)$, explaining the
  $n^2$ degeneracy) — all standard and right; the hydrogen precedent is a genuine asset for the paper.
- **Generators (still mislabeled):** the JSON's `G` / `L` are again $\pm$ the *same* (left) chirality, not a
  genuine left/right pair; the §1 verified generators are the correct ones.
- **The "demonstration" does NOT demonstrate the claim — run verbatim** (50 agents, 0.08 rad noise):
  left-only / right-only / both all give composed error **≈ 2.07–2.30 rad** (random ≈ 2.0; $\pi$ is the
  max) — **none converge**; "both lowest" is within noise, not a result. Even an **anchored single-product**
  estimate fails (composed ≈ 2.28) → the optimizer itself (the `2[x,y,z]/(w+ε)` gradient + symmetric
  retraction) is broken, independent of $SO(4)$.
- **The real issue — identifiability:** the relative measurements constrain only the **product**
  $q_i = q_g\cdot q_l$. The split into global·local has a **gauge freedom** ($q_g\!\cdot\!h,\ h^{-1}\!\cdot\!q_l$),
  so the two $\mathfrak{su}(2)$ "handles" are a **gauge redundancy here, not two estimable quantities.** The
  headline use case (recover separate global + local *rotation* frames from relative measurements) is
  **not well-posed** without extra gauge-breaking information.
- **Where the value actually is:** the second $\mathfrak{su}(2)$ is useful when it encodes a *physically
  observable* DOF, not a gauge one — i.e. the **dual-quaternion 6-DOF** case (§3), where the second factor
  carries **translation** (independently observable). **Redirect the framework from "global/local rotation
  frames" (ill-posed) to "rotation + translation" (well-posed).**

**Verdict:** strong, mostly-correct mathematical core (keep the so(4) algebra, curvature, and the hydrogen
precedent for the paper); but the headline multi-agent use case is **not demonstrated and not identifiable
as posed** — the JSON's `claim_discipline.demonstrated` must be corrected to *"proposed; synthetic test does
not converge; use case ill-posed without anchoring."* The **dual-quaternion 6-DOF** direction (§3) remains
the valid, fundable first prototype.

*Tiers: T1 = the so(4)=su(2)⊕su(2) structure + the verified generators (re‑computed). T2 = the
dual‑quaternion / isoclinic mappings (exact math, sound but undemonstrated for Hˢ). T3 = two‑channel
reading, two‑helicity EM, richer atlas glue (hypotheses). Cross‑refs: `../P7_FOUNDATIONS_SEED.md`,
`LIGHT_AS_COMPOSITION_RIEMANN_SILBERSTEIN.md`, `LIE_THEORY_THREAD_ASSESSMENT.md`,
`../../arXiv/P1_cnq_tiling/collective_review/GROK_REVIEW_VERIFICATION.md`. Peter is the sole gate; nothing
pushed.*
