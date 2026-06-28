# Compositional Character Space — for the people who read compositions

*A one‑page invitation. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker: what's measured, what's claimed, what's open — kept separate on purpose.*

---

## The move

Compositional data analysis reads **one system at a time**: a whole divided into parts, taken into log‑ratio space so the proportions behave, then characterized — biplot, balances, variation matrix. The object is always *this* composition.

Compositional Character Space turns the instrument around. Read a system in motion and it returns a **profile** — how directed its movement is, how many independent things move, which way it's trending. Treat that profile as itself a small composition of qualities and read it the same way. The log‑ratio worldview applied to its own output. We call the operation the **second‑order read (Hˢ²)**.

## What we found

Run it across many real systems from unrelated fields — national energy mixes, a stock‑market sector composition, gut microbiomes, igneous geochemistry, a climate scenario, the cosmic microwave background, conversation drift — and they do **not** scatter into as many unrelated descriptions. They organize along a few axes of character (directedness × complexity × regime structure × trend), and they sort into four recurring **characters**:

- **Ballistic** — directed and simple (World / China / USA / India electricity: one clear arrow toward wind and solar).
- **Contested** — several real moves, no single winner (Germany / France / UK / Japan electricity).
- **Turbulent** — churning, high‑dimensional, no committed heading (S&P sectors **and** the Crohn microbiome — which land in the *same* character).
- **Diffusive** — mixing without a course (the mudstone).

The headline at eleven systems looked like a tight *character collapse* (effective rank 2.80 of 5). **Tested at scale (107 systems, 13 domains) it corrected to ~4 of 5** — the collapse is real but *mild*, not tight; see [`CCS_EXPANDED.md`](CCS_EXPANDED.md). What survived and strengthened is the bridge: a market rotation and a gut community are, at the level of how they move, the **same character of system** — and across 13 domains the most directed systems (the cosmic microwave background, the world energy transition, a climate‑policy scenario) and the most churning (a microbiome, human conversation, diversified geochemistry) sort cleanly. That cross‑domain ordering is the finding you cannot see reading any one system alone.

## What we claim (and what we don't)

- **Tier 1 (measured, reproducible).** The profiles, the four characters, and their cross‑domain ordering are deterministic outputs of one engine across 107 real systems. Same data → same table → same SHA‑256. Anyone can re‑run it.
- **Tier 2 (reasoned).** The character space is *mildly* low‑dimensional — ~4 independent axes from 5 features at scale (the one robust redundancy is directedness). The substantive finding is the **cross‑domain clustering of motion‑character**, not a tight dimensional collapse.
- **Not claimed.** We do **not** claim a 3‑axis manifold (the early ~2.8 was a small‑sample impression; it corrects to ~4 at n=107), that the four characters are exhaustive, or that "finance ≈ microbiome" means shared mechanism. It means shared *motion‑character* — an analogy made rigorous at one level, nothing more.

## The invitation

This is a research program with an instrument already behind it, and it has already corrected itself once at scale — exactly as it should. **Bring your longitudinal compositions (hundreds of systems, your domain), run the second‑order read, and see where the characters sit, whether new ones appear, and where the axes truly lie.** The next real test is *more domains, not more of one* — biology, language, markets, materials are still sparsely sampled. The tooling is open and deterministic; the null is built in; the claim is falsifiable. When it breaks, it breaks cleanly — and that's a result too.

*Reproduce: `python hs_meta.py` (builds the Character Table + `SYSTEMS_PROFILES.json`); method in [`SYSTEMS_OF_SYSTEMS.md`](SYSTEMS_OF_SYSTEMS.md); feed any data with [`../Hs-Kinematics/hs_data_prep.py`](../Hs-Kinematics/hs_data_prep.py). The geometry is CoDa's; the second‑order read is the extension.*
