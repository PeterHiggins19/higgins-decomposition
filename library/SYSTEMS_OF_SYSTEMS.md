# Compositional Character Space — Hˢ applied recursively to Hˢ

*The map of how compositional systems move, discovered by reading the readings. Built by `hs_meta.py`. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker — this is a **classification discovered from the engine's own outputs**, Tier‑1 deterministic, but the *meaning* of each class is the domain expert's.*

> **Naming.** The concept is **Compositional Character Space (CCS)** — the low‑dimensional space every compositional system is placed in by how it moves. The *operation* that builds it is the **second‑order read, Hˢ²** (the reading instrument applied to its own outputs). The *artifact* is the **Character Table** below. The *finding* is **character collapse** — that the space is only ~3‑dimensional.

---

## The idea, in one line

Run the engine across many systems; take **each system's diagnostic profile — the engine's own readings — as a feature vector**; then let Hˢ read the *systems* by that profile (Hˢ²). The composition‑of‑compositions. The output is **Compositional Character Space**: a small table of **system characters** that the data structures in common reveal, and it grows by one row every time a new realm is mapped.

This is not a metaphor. The features below (effective rank, momentum coherence, path efficiency, regime count, diversification trend) are literally the kinematics engine's outputs. The classifier applies the engine's own effective‑rank machinery to the matrix of those outputs. Same data → same table → same hash.

## The profile table (real runs, this session)

Each row is one real system, read by `hs_kinematics_engine.run`. Coherence = arrow‑of‑intent alignment (navigation) / momentum coherence (physics); path efficiency = course directness; rank = effective dimensionality; trend = change in effective spread (+ diversifying, − concentrating).

| System | Realm | Eff. rank | Coherence | Path eff. | Regimes | Trend | Class |
|---|---|---:|---:|---:|---:|---:|---|
| World electricity | energy | 1.27 | 0.90 | 0.95 | 1 | +1.31 | **Ballistic** |
| China electricity | energy | 1.99 | 0.95 | 0.66 | 1 | +2.26 | **Ballistic** |
| USA electricity | energy | 1.67 | 0.71 | 0.75 | 2 | +1.47 | **Ballistic** |
| India electricity | energy | 1.73 | 0.55 | 0.65 | 2 | +0.08 | **Ballistic** |
| Germany electricity | energy | 2.66 | 0.67 | 0.53 | 1 | +2.57 | **Contested** |
| France electricity | energy | 2.14 | 0.58 | 0.56 | 2 | +0.89 | **Contested** |
| UK electricity | energy | 2.06 | 0.50 | 0.63 | 3 | +1.54 | **Contested** |
| Japan electricity | energy | 2.57 | 0.39 | 0.44 | 2 | +0.39 | **Contested** |
| S&P sectors | finance | 4.88 | 0.05 | 0.07 | 5 | +0.01 | **Turbulent** |
| Crohn microbiome | microbiome | 36.1 | 0.01 | 0.001 | 21 | −2.12 | **Turbulent** |
| Frielingen mudstone | geology | 2.05 | 0.02 | 0.03 | 12 | −0.09 | **Diffusive** |

## The discovered classes

The classifier sorts systems by **directedness** (mean of coherence and path efficiency — is the system *going somewhere*?) against **complexity** (effective rank — *how many independent things move*?). Four characters fall out:

- **Ballistic — directed and simple.** One dominant direction, high coherence, low rank. *World / China / USA / India electricity:* a global energy transition driving hard toward wind and solar along essentially one axis. These systems have an arrow of intent you can almost extrapolate (we don't — it's a vector of present motion, not a forecast).
- **Contested — mid directedness, mid rank.** Several real moves pulling at once, no single winner. *Germany / France / UK / Japan electricity:* mature grids juggling nuclear, gas, renewables, imports — direction exists but is negotiated.
- **Turbulent — churning and complex.** Low coherence, high rank, many regimes. *S&P sectors / Crohn microbiome:* dozens of factors trading places with no committed heading. A finance churn and a gut community look, **structurally, like the same kind of system** — which is exactly the cross‑domain insight the recursion was built to surface.
- **Diffusive — low direction, sedimentary mixing.** *Frielingen mudstone:* trace elements drift and swap without a coherent course — a depositional record, not a driven process.

## The headline finding — character collapse: the space is ~3‑dimensional

Apply Hˢ's effective‑rank read to the standardized profile matrix itself: **the effective rank of Compositional Character Space is 2.80 of 5.** Eleven systems spanning energy, finance, microbiology and geology are told apart by only **~3 axes of character** — directedness, complexity, and diversification trend. The variety of the world's compositional systems, seen through the engine, collapses to a low‑dimensional space. That compression — **character collapse** — *is* the advantage Peter anticipated ("to some advantage yet determined"): a new system can be placed in CCS from its profile alone, and its nearest neighbours predict which guards, which regime structure, and which diagnosis vocabulary will apply.

*Honest scope: ~3 axes is what **this** sample of eleven shows — a real, reproducible measurement, but a Tier‑2 finding, not a proven law.*

> **⚠ Corrected at scale (2026‑06‑15).** The engine was then run across the whole data hold — **107 systems, 13 domains** — and the strong collapse did **not** survive: CCS effective rank is **4.13 of 5** at n=107 (4.07 balanced, 4.03 energy‑only). The clean ~2.80 was a small‑sample artifact of eleven diverse systems. What **strengthened** at scale is the four‑character taxonomy and its cross‑domain ordering (the CMB, world energy, and a climate scenario are the most directed; a microbiome, a conversation, and diversified geochemistry the most churning). The retained claim: the character space is *mildly* low‑dimensional (~4 axes, the one robust redundancy being directedness), and the **cross‑domain clustering of motion‑character is the substantive finding**. Full result: [`CCS_EXPANDED.md`](CCS_EXPANDED.md). This correction is the falsifiable claim working as designed.

## The realms registry — what's mapped, and how it grows

Each realm carries a **boundary signature** (the Tier‑3 EITT/fringe verdict — is the system inside the resolvable interior or near its information boundary?) and an **integral signature** (path efficiency / action — how economically it moves). New realms append rows; the boundary tools flag when a realm sits at the edge of what the data can resolve, and the integral computations summarize its motion. This is the adaptive part: as exploration reaches a new realm, the same two instruments (boundary test + path integral) characterize it without retuning.

| Realm | Mapped | Character | Boundary signature | Next frontier |
|---|---|---|---|---|
| Energy | ✓ deep | Ballistic ↔ Contested | interior, resolvable | per‑country momentum atlas |
| Finance | ✓ | Turbulent | interior | monthly null model (P2) |
| Microbiome | ✓ | Turbulent | high‑D, near boundary | single‑subject clock |
| Geology | ✓ | Diffusive | interior | igneous differentiation |
| Wine / trade | ✓ production; trade pending | (Contested expected) | TBD on BACI extract | bilateral HS‑2204 in motion |
| Physics / maths | ✓ exact cases | degenerate (rank→1) | floor (IEEE) | kinematics paper |
| Audio / acoustic | origin | — | — | the founding instrument |

## How to extend it

Run `python hs_meta.py` after any new real‑data run; it reads the profiles, re‑classifies, recomputes the system‑space rank, and rewrites `SYSTEMS_PROFILES.json`. Add a realm by pointing it at the new engine‑ready CSV (use `hs_data_prep.py` to make one from any data zip). The table is meant to be re‑run, not hand‑edited — it is a measurement of the library, the way the library measures the world.

*Recursion with discipline: every level is the same deterministic engine, the same guards, the same honest‑broker tiers. Hˢ reading Hˢ does not invent a new claim — it reveals the structure the systems already share.*
