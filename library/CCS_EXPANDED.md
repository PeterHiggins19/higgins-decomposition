# Compositional Character Space at scale — 107 systems, 13 domains

*The home‑data expansion of the second‑order read (Hˢ²). Built by `ccs_batch.py` → `CCS_EXPANDED.json`. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker — and this run is itself a worked example of the discipline: a Tier‑2 claim was tested at scale and partly corrected. That correction is the result, not a footnote.*

---

## What was run

The kinematics engine was turned loose on every engine‑ready real composition in the data hold — **107 systems across 13 domains**, auto‑detected and run through one engine, each profile checkpointed:

| Domain | Systems | Source |
|---|---:|---|
| Energy (primary, OWID) | 73 | per‑country energy mix, up to 60 yrs |
| Energy (generation, EMBER) | 9 | per‑country electricity mix |
| Geochemistry | 10 | igneous oxide barycenters (Ball, Qin, Stracke, Tappe, Frielingen) |
| Economy / agriculture (FAO) | 4 | value‑added + credit compositions |
| Cosmology | 2 | Planck CMB budget, cosmic energy budget |
| Microbiome | 2 | Crohn, ECAM infant |
| Finance, nuclear, climate‑scenario, urban, chemistry, tech, language | 1 each | S&P sectors, SEMF, IIASA NGFS, Markham budget, oxide chem, Backblaze fleet, conversation drift |

All deterministic, same‑data‑same‑hash; the harness is resumable against the sandbox wall‑limit.

## Finding 1 — the four characters generalize (this strengthened)

The Character Table populates sensibly across all 13 domains. Ordered by directedness, the extremes are striking *because* the domains are unrelated:

- **Most directed (Ballistic):** the **Planck CMB** budget, the **world energy** transition, an **IIASA climate‑policy scenario**, a **municipal budget**. Three of these *should* be directed — a near‑frozen cosmological spectrum, a designed monotone policy trajectory, a planned budget — so the engine reading them as the most ballistic systems in the hold is a clean sanity check.
- **Most churning (Diffusive/Turbulent):** the **Crohn** and **ECAM** microbiomes, **human conversation drift**, and **highly‑resolved geochemistry** (the 95‑oxide mixtures). A gut community, a conversation, and a rock's trace chemistry share a *character* — many parts trading places with no committed heading — across biology, language, and geology.

That a market, a microbiome, and a conversation cluster together by how they move, with no domain knowledge fed in, is the keeper result. The taxonomy is real and it travels.

## Finding 2 — the "~3 axes" collapse does NOT survive scale (this corrected)

At the original **n = 11**, the effective rank of Compositional Character Space measured **2.80 of 5** — the impression of a tight collapse to ~3 character axes. At **n = 107** it is:

| Sample | CCS effective rank |
|---|---:|
| Full (n=107) | **4.13 of 5** |
| Domain‑balanced (1 per realm, n=13) | 4.07 of 5 |
| Energy fan‑out only (n=73) | 4.03 of 5 |

The collapse weakens to **~4 of 5** — robustly, across the full set, a balanced set, and within a single domain. The clean ~2.8 was a **small‑sample artifact** of eleven deliberately‑diverse systems; the real character space uses about four of its five measured dimensions. The one durable redundancy is that the two *directedness* measures (momentum coherence and path efficiency) move together — collapsing five raw features to roughly four independent axes: **directedness, complexity (effective rank), regime structure, and diversification trend.** That is mild structure, not a dramatic compression.

### Why this is the system working, not failing

The ~3‑axis figure was logged as **Tier‑2** with the explicit caveat *"this is what a sample of eleven shows — a real measurement, not a law; come test it at scale."* We tested it at scale; the strong version did not hold; the honest number is ~4. The claim was falsifiable, it was falsified, and the record now shows exactly when and by how much. That is adaptive anticipation — keep the anchor, let time and test correct the rest.

## What now stands (corrected claim)

- **Tier 1 (measured).** 107 real systems place on a four‑character table (Ballistic / Contested / Diffusive / Turbulent); the ordering by directedness is cross‑domain‑coherent; reproducible to the hash.
- **Tier 2 (reasoned).** The character space is *mildly* low‑dimensional — ~4 independent axes from 5 features, the one robust redundancy being directedness. The cross‑domain clustering of motion‑character is the substantive finding; the dimensional‑collapse headline is retired to "mild."
- **Not claimed.** No tight 3‑axis manifold; the four characters are a useful partition, not proven exhaustive; cross‑domain co‑clustering is shared *motion‑character*, never shared mechanism.

## Reproduce / extend

`python ccs_batch.py` (runs the engine across the hold, checkpoints `ccs_results.jsonl`) then the finalize block → `CCS_EXPANDED.json`. Add data with [`../Hs-Kinematics/hs_data_prep.py`](../Hs-Kinematics/hs_data_prep.py); the map grows by appending. The next real test is *more domains, not more energy countries* — the energy fan‑out already saturates one corner of the space; biology, language, markets, and materials are where the characters are still sparsely sampled.
