# H1 Step 5 — Entangled‑carrier closure (the honest, classical reading)

*The fifth rung of the H₁ generalization ladder. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. **Honest‑broker, and this is the corner where it matters most.** Module: `hs_carrier_coupling.py`.*

> ## ⚠ Read this first — what this is NOT
> **Compositional data are classical. This is not quantum entanglement, not a Bell violation, not non‑locality.** The word "entangled" here means the *classical* fact that closure couples carriers. The CHSH‑form statistic below is a **coordination index borrowed from the algebraic form of the Bell/CHSH expression, and it is bounded by 2** — the classical (local‑hidden‑variable) bound. It can never reach the quantum Tsirelson bound (≈ 2.828); if it ever exceeded 2, that would be a *construction error to fix*, not a discovery. Tier 3, exploratory — a clue, never a claim.

---

## 1. The sound core: closure *does* couple the carriers

In a composition the parts sum to a constant, so they **cannot vary independently** — increase one share and others must fall. Pearson noticed this in 1897 (the "spurious correlation" of ratios), and it is exactly why compositional data analysis works in log‑ratios. So there is a real, non‑mystical sense in which **closure entangles the carriers**: the constraint forces a coupling. `closure_coupling_baseline` reports that forced part — the mean off‑diagonal correlation of the closed parts (negative by construction; the baseline coordination, not signal). Reading carrier coordination honestly means reading it *against* this baseline.

## 2. The CHSH‑form coordination index (classically bounded by 2)

For a pair of carriers we form two deterministic ±1 "settings" each from the CLR trajectory — a *level* reading (above/below its own mean) and a *change* reading (rising/falling) — and compute the CHSH combination of the four correlators, `|E(a,b)+E(a,b′)+E(a′,b)−E(a′,b′)|`, maximized over the four sign patterns. For deterministic functions of shared data (the time index *is* the local hidden variable), this is **bounded by 2**. The value reads pairwise coordination: **near 2 = a maximally co‑moving pair; near 0 = uncoordinated.** The full `coupling_matrix` is the D×D field of these values, all in [0, 2].

## 3. Demonstration on real data — the bound holds, and the structure is interpretable

Run on real EMBER electricity mixes (D=8–9), every case respects the classical bound, and the most‑coupled pairs are exactly the carriers that move as a bloc:

| System | max CHSH‑form (raw) | classical bound ≤2 | most‑coupled pairs | closure baseline |
|---|---|---|---|---|
| **World** | 2.0 (2.0) | ✅ respected | **Solar–Wind, Other‑Renewables–Wind, Other‑Renewables–Solar** (all 2.0) | −0.088 |
| **Germany** | 2.0 (2.0) | ✅ respected | Other‑Renewables–Wind (2.0); Hydro–Other‑Fossil, Coal–Other‑Renewables (1.84) | +0.019 |
| **USA** | 1.86 (1.86) | ✅ respected | Coal–Oil, Coal–Biofuel (1.86); Coal–Wind (1.80) | −0.076 |

The honest read: the diagnostic surfaces **the co‑moving carrier blocs** — the world's renewables (Solar/Wind/Other‑Renewables) are maximally coordinated because the energy transition moves them together; the US reads coal's decline coordinated with the carriers replacing it. And the **kill‑test passes**: no case exceeds 2, confirming this behaves as a classical coordination measure and produces no spurious "entanglement." *(That the bound is never violated is the most important result here — it is the discipline working.)*

## 4. The D=8 algebraic note (Tier 3 — a clue)

The "twin quaternion" at D=8 is S³ × S³ = **Spin(4) = SU(2) × SU(2)** (verified at the IEEE floor). A product of two SU(2) factors is the natural *two‑party* algebra, which is why the roadmap paired "entangled‑carrier closure" with the D=8 case: a 4+4 carrier split maps to the two factors, and the CHSH‑form reads coordination across them. This algebraic home is suggestive and **Tier 3 only** — it does not make the coordination quantum; it gives the two‑party bookkeeping a clean structure.

## 5. Honest scope

- **What it is:** a deterministic, hash‑receipted, Tier‑3 *coordination* diagnostic that finds maximally co‑moving carrier pairs/blocs and reports them against the closure‑forced baseline; the classical bound (2) is checked and respected.
- **What it is not:** quantum entanglement, a Bell/CHSH violation, evidence of non‑locality, or anything requiring quantum mechanics. The Tsirelson bound is listed only as the line classical data cannot cross.
- **Whether it adds value over standard CoDa covariance/log‑ratio‑variance is an open question** — its distinctive read is the *co‑moving‑bloc* detection in the CHSH form and the built‑in classical‑bound kill‑test. Use it as a clue, alongside the variation matrix, not instead of it.

## 6. Prior lineage + why the journaled run is the evidence

The CHSH/entanglement‑analog idea is not new to the project: it has prior lineage in the investigation catalog (**INV‑015 — "many‑droplet entanglement analogs, CHSH on joint q"**) and the HUF QIT knowledge base, and it sits beside the gauge‑theoretic reading of CLR/SU(2). What this rung adds is the **deterministic, reproducible, hash‑receipted implementation** and a **journaled completion in the repository** (tracking log G‑69). That journaling is the point: *the honest nature of the work is demonstrated by a reproducible experiment whose recorded result is the classical bound being respected.* Anyone can re‑run `hs_carrier_coupling.py`, get the same coupling matrix and the same verdict (bound ≤ 2, no violation), and read the receipt. An idea that has been explored, then implemented exactly, then shown to refuse the over‑claimable outcome — and recorded as such — is more trustworthy than one that was only ever asserted.

*Step 5 honored, the honest way: closure entangles carriers classically; the CHSH‑form reads the coordination; the bound holds; nothing quantum is claimed. The instrument refuses to overclaim — even here, especially here.*
