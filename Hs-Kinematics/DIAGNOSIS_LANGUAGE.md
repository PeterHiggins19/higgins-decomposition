# The diagnosis language — letting a composition say what it is doing

> A deterministic language of diagnosis. The same readings the engine computes are composed, by a fixed grammar, into plain human sentences — and **the language expands automatically with complexity**: a 2‑part system has a word or two; a microbiome of hundreds of taxa has many voices. The number of voices isn't chosen — it's the count of parts actually *doing* something. So the system tells you what it's doing in exactly as many words as it has structure to fill.

*Module: `hs_diagnosis.py` (numpy only; deterministic; hash‑stable). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; Tier 1 (the narrative is a deterministic function of the deterministic readings) — interpretation of the words is the domain expert's, never the engine's.*

---

## How it works

Every clause is rule‑generated from the engine state: the **steerer** (helmsman), the **arrow of intent** (which parts are *gaining* vs *shedding* mass‑weighted momentum), the **spread trend** (diversifying / concentrating, from K_eff), the **state changes** (waypoints), and the **independent directions** (effective rank). The narrator names every part whose net momentum clears a threshold — so a simple system names one or two, a complex one names many. Same input → same words → same hash: it is a *deterministic utterance*, not LLM text (an LLM may polish the phrasing, but the canonical sentence carries the engine's trust).

If the system is **at rest**, it says one honest sentence and stops. The words are a *description*; what they *mean* (a stress response, a dysbiosis, a policy shift) is the expert's read — the engine never claims it.

## The language scaling with complexity (real + synthetic)

| System | Voices | What it said (deterministic) |
|---|---|---|
| **Gold/Silver** (D=2) | **2** | "Gold is steering (shedding). Weight is moving toward Silver. The mixture is diversifying (1.84 → 1.99)." |
| **Energy mix** (D=8) | **4** | "Coal is steering. Weight is moving toward Coal, Gas, Nuclear, Other. Concentrating (6.27 → 4.03). Changed state 4 times. Runs in about 3 independent directions." |
| **Crohn microbiome** (real, D=48) | **14** | "**g__Prevotella is steering (gaining). Weight is moving toward Prevotella, Enterobacteriaceae, Veillonella, Streptococcus, Bifidobacterium…; away from Bacteroides, Haemophilus, Aggregatibacter…**. Concentrating (7.14 → 5.01). (14 of 48 parts have something to say.)" |

**The striking part:** on the *real* Crohn data the community narrated a **Prevotella ↑ / Bacteroides ↓** shift — a genuine, recognized microbiome axis. The engine only stated who gains and who sheds; the clinical meaning fell out for the reader to claim. That is the whole point: *the composition speaks; the scientist interprets; the words are deterministic and carry a receipt.*

## Why this matters

- **One read, every audience.** A non‑specialist reads the sentence; a specialist reads the named parts and supplies the meaning in their field's terms (paired with the navigation/physics vocabulary, `../HCI-CNTT/TERMINOLOGY_BRIDGE.md`).
- **Complexity becomes legible.** A 200‑taxon table is unreadable as numbers; as a narrative — "these are gaining, those are shedding, in this many directions, changing state here" — it becomes a sentence a human can hold.
- **Deterministic and honest.** Same data, same words, same hash; at rest it says so; the meaning stays the expert's. The instrument gave the composition a voice without giving it an opinion.

*A million bacteria can't say "turn off the hot lights" — but the engine can say, deterministically, "the community is moving away from these taxa and toward those, concentrating, in thirty directions at once," and the biologist hears the stressor. That is the language of diagnosis: real, deterministic, and as many words as the system has to say.*
