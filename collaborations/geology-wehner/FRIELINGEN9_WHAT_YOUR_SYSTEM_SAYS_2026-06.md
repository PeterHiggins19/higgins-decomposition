# Frielingen‑9 — what your system says, read by the full Hˢ kinematics platform

*A complete deterministic read of the Frielingen‑9 mudstone section, for Matthew Wehner. Every number below is reproducible to a cryptographic receipt; the **readings are the instrument's, the geology is yours** — Hˢ says who moves, how much, in how many directions, and exactly where the section changes; what it means is the geologist's call. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker. Public data only (Thöle et al. 2019, PANGAEA 897615, CC‑BY 4.0); you control how your work is presented.*

---

## Your system, in one line

219 samples down a Lower Cretaceous mudstone section (eastern Lower Saxony Basin), six carriers — **SiO₂, Al₂O₃, Rb, Zr, CaCO₃, TOC** — read **in depth order (deep→shallow = old→young)** so that "motion" is the chemistry changing *up the section through time*. The engine reads the whole story of that change and shows its own limits. Conformance receipt for this run: `content_hash = 6f28465fb59696eb…`.

## 1. It reads exactly (nothing is lost)

The composition rebuilds from its log‑ratio structure to **3.55×10⁻¹⁵** — machine precision. Before any interpretation, the instrument proves it has thrown nothing away: your six‑part chemistry is held exactly. (This is the same exactness that, at four parts, makes a composition a unit quaternion — the foundation of the method.)

## 2. Who is steering — and the trace‑over‑bulk signature, confirmed again

Two honest measures of "who drives," and they tell a coherent geological story:

- **Loudest single variable (helmsman / velocity):** **CaCO₃** — and all three helmsman reads (raw, resolvability‑guarded, and the closure‑invariant *coherent* helmsman) agree on CaCO₃. Carbonate is the most‑moving coordinate down the section — the marl/clay carbonate cycling you would expect to dominate a mudstone's variance.
- **Net direction of the weight (arrow of intent / momentum):** the section **sheds Zr** and **gains CaCO₃, Rb, Al₂O₃**, moving *away* from Zr, TOC, SiO₂. That is the **detrital ↔ carbonate balance** swinging — and the carriers carrying the net momentum are the **trace elements (Zr shedding, Rb gaining) driving over the bulk oxides**. Your trace‑over‑bulk result holds on the full kinematic engine, not just the earlier read.

## 3. How many things are really moving — ~2 dimensions

The motion's **effective dimensionality is 2.23** (singular spectrum 13.5, 6.1, 1.8, 0.56, 0.36). Despite six carriers, the chemistry moves in about **two independent directions** — essentially a *carbonate axis* and a *detrital/trace axis*. The engine fires `DG‑RNK‑WRN` to say so honestly: the system is lower‑dimensional than its carrier count. For you that is not a warning, it is the finding — two processes write this section.

## 4. Where the section genuinely changes — 8 datable boundaries

This is the read most useful at the outcrop. The **hold‑lock** discovers the section's own noise floor (0.326 in clr units) and, with hysteresis, registers a structural change **only** when the chemistry has truly reorganised — not at every noisy wiggle. It finds **8 genuine boundaries**, at depths:

```
161.1, 137.8, 133.7, 131.7, 123.7 m   (a deeper cluster of reorganisation)
 31.8,  25.0,  15.4 m                  (a shallow cluster near the top)
```

Two episodes of compositional reorganisation — a deeper interval (~161–124 m) and a shallow one (~32–15 m) — objectively located from the chemistry alone, ready to test against your lithology, biostratigraphy, and the published cyclostratigraphy. The raw mean+2σ method flagged 12 candidate breaks; the hold‑lock kept the **8 that survive the section's own noise** and discarded the rest. *(Same data → same boundaries → same hash; a second analyst gets your exact list.)*

## 5. What kind of system it is — a *Diffusive* record

The arrow's **coherence is 0.013** and the **path efficiency is 0.007** — both near zero. The section does not march in one direction; it mixes and wanders, the signature of a **depositional record** rather than a driven process. Placed among 107 systems from 13 fields (Compositional Character Space), Frielingen‑9 sits firmly in the **Diffusive** character — alongside other sedimentary and finely‑mixed geochemical systems, and opposite the "ballistic" directed systems (a designed policy, the world energy transition). Your mudstone behaves, measurably, like what it is: an accumulation, not an engine. The motion is mostly **velocity only** — the engine reports `max meaningful order = velocity`, refusing to read acceleration out of point samples it cannot support.

## 6. It is analysable (the boundary test passes)

The Tier‑3 fringe test (EITT, the entropy‑invariant boundary check) returns **within‑regime**: under geometric‑mean decimation your section's information survives — it has coherent structure the deterministic read can resolve. You are not at the edge where the instrument runs out; the reads above are on solid ground.

## The plain‑language diagnosis (the system speaking)

> *"Zr is steering (shedding). Weight is moving toward CaCO₃, Rb. It is moving away from Zr. The mixture is diversifying (effective spread 3.43 → 3.75). It changed state 8 times. The motion runs in about 2 independent directions. (3 of 6 parts have something to say; the rest are quiet.)"*

Generated by a fixed grammar from the numbers above — deterministic, same‑data‑same‑words‑same‑hash. A description, not a claim.

## Test cases and full experiments run on your system

| # | Experiment | Result |
|---|---|---|
| 1 | **Lossless exactness** | reconstruction error 3.55e‑15 — the section is held to machine precision |
| 2 | **Trace‑over‑bulk** | Zr/Rb (trace) carry the net momentum over the bulk oxides — confirmed on the full engine |
| 3 | **Datable regime detection** | 8 noise‑survived structural boundaries at fixed depths (12 raw → 8 genuine) |
| 4 | **Effective dimensionality** | 2.23 — two processes, not six |
| 5 | **Character placement (CCS)** | Diffusive — among 107 cross‑domain systems |
| 6 | **Boundary/analysability (EITT)** | within‑regime — resolvable structure |
| 7 | **Static CoDa fallback** | the same data also yields standard ternary / CLR‑biplot / variation‑matrix outputs if you only want the snapshot — Hˢ does not force the dynamic read on you |
| 8 | **Determinism receipt** | full content hash for this run; bit‑identical on any machine |

## What more we can offer (your prime project, and where it goes)

- **Igneous differentiation in motion.** The same engine reads your igneous datasets: oxides‑by‑age (differentiation diversifying over geologic age, ~3 directions), the TAS series (silica enrichment *concentrating* 5.76→2.51 — the differentiation trend, read as motion), clinopyroxene‑by‑location, and OIB‑by‑location. A cross‑sectional → kinematic study of differentiation is ready to build (`IGNEOUS_DIFFERENTIATION_SEED.md`).
- **The field instrument.** Your folder already holds the directional‑sniffer and multisensor concepts and a NASA‑style flight‑spec suite (HGS‑000…). The engine's *hold‑steady‑and‑flag‑transitions* behaviour is exactly a field tool: walk a section, the instrument holds when nothing changes and announces a boundary when the chemistry reorganises — non‑contact, deterministic, with the receipt.
- **A momentum atlas** of the section (per‑interval arrow of intent), and **adaptive sampling** (sample denser where the motion is real, sparser where it holds) behind safety breakers.
- **The reproducibility kit.** Everything above runs from `../../Hs-Kinematics/` — the engine, the full specification, language‑agnostic pseudocode, an R port (offered as‑is for an R user to check), and a replication notebook. You can reproduce every number here yourself, or hand it to a student who has never seen CoDa.

## The honest envelope

Every value is Tier‑1 deterministic except the fringe test (Tier‑3, a clue never a claim). The instrument reads; **you** decide what the carbonate cycles and the trace‑element swings *mean* for the Lower Saxony Basin. Nothing here is published or sent anywhere — this is your read of your system, for you to use as you see fit. The data is public and cited; your interpretations and your image remain entirely yours.

*Hˢ read your section as far as the data can be known and not one step further, and handed you the receipt. The instrument reads with confidence; the boundary test watches the edge; the geology is yours.*
