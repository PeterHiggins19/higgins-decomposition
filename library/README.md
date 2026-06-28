# The Library of Understanding

*A self‑describing knowledge base that measures itself. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; Peter is the sole commit/contact gate.*

---

## What this folder is

The CoWorker workspace stopped being a pile of files and became a **library**: an engine, its safety guards, a diagnosis language, the governing doctrine, and the real‑data runs that prove them. This folder makes the library *legible to itself* and lets it **build on what it has already learned** as new realms are explored. Three parts, each a level up from the last:

1. **The catalogue — `LIBRARY_INDEX.json` / `.md`** (built by `build_index.py`). Every knowledge file classified by domain, type, and repo, with a `context_search` block so any tool — human or AI — finds the right shelf by *context* instead of by remembered path. 6,600+ files, re‑indexed on demand. *This is the library knowing **what** it contains.*

2. **The recursion — Compositional Character Space (`hs_meta.py` → `SYSTEMS_OF_SYSTEMS.md`).** Run the engine across many systems, take each system's diagnostic profile (the engine's own readings) as a feature vector, and let Hˢ read the *systems* — the **second‑order read, Hˢ²**, the composition of compositions. It builds a small **Character Table** (Ballistic / Contested / Turbulent / Diffusive) that, tested across **107 systems in 13 domains** ([`CCS_EXPANDED.md`](CCS_EXPANDED.md)), orders coherently cross‑domain — a market, a microbiome, and a conversation share a character. (The early "~3‑axis collapse" from 11 systems corrected to ~4 at scale — the falsifiable claim working.) The invitation to the field: [`CCS_FOR_COMPOSITIONAL_READERS.md`](CCS_FOR_COMPOSITIONAL_READERS.md). *This is the library knowing **how each system it has seen behaves**.*

3. **The adaptation — the realms registry inside `SYSTEMS_OF_SYSTEMS.md`.** Each realm carries a boundary signature (Tier‑3 EITT/fringe — is it resolvable or near its information edge?) and an integral signature (path efficiency / action — how it moves). New realms append rows; the same two instruments characterize anything new without retuning. *This is the library knowing **where it has been and how to take on what it hasn't**.*

## The loop, end to end

```
 any data zip ──hs_data_prep.py──▶ engine‑ready composition
        composition ──hs_kinematics_engine──▶ profile (rank, coherence, path‑eff, regimes, trend)
                profile ──hs_meta.py──▶ a row in the table of systems‑of‑systems
                        table ──build_index──▶ a shelf in the catalogue the next query reads
```

Data flows in from outside (monitored for relevance), becomes a composition, the engine reads it, the reading becomes a *character*, the character joins a table of systems, and the catalogue files it where the next exploration will find it. The boundary and integral tools watch the edges so the table can grow into realms it has not yet seen. **Use Hˢ recursively on Hˢ as needed, and a table of systems‑of‑systems assembles quickly.**

## Why it matters (the advantage, named)

A new system can be placed on the table from its profile alone. Its nearest neighbours then tell you which guards will fire, which regime structure to expect, and which diagnosis vocabulary applies — before any domain analysis. A finance churn and a gut microbiome turn out to be the *same character* of system; a national grid and the world grid differ only in how contested their direction is. That cross‑domain compression — variety collapsing to ~3 axes — is the standing advantage: the library does not just store what was learned, it **generalizes it forward**.

## Discipline

Every level is the same deterministic engine, the same guards, the same honest‑broker claim tiers (Tier‑1 measured / Tier‑2 reasoned / Tier‑3 a‑clue‑never‑a‑claim). Recursion does not manufacture new claims — it reveals structure the systems already share. The catalogue is regenerated, never hand‑curated; the table is re‑run, never hand‑edited. Raw data is read, never copied into the repo (instrument, not data). Peter is the sole gate on every outward step.

## To run it

```
python build_index.py     # re‑index the workspace → LIBRARY_INDEX.json/.md
python hs_meta.py          # re‑classify all systems → SYSTEMS_OF_SYSTEMS + SYSTEMS_PROFILES.json
```

Add a system: make an engine‑ready CSV with `../Hs-Kinematics/hs_data_prep.py`, point `hs_meta.py` at it, re‑run. The table measures the library the way the library measures the world.
