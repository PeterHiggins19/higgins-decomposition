# Is Hˢ right for your data? — start here

*A short, honest guide for anyone who has a composition to analyse. No boast — just what the instrument does, whether it fits your data, what it can do at your scale, and how to begin. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker. The data is the star; Hˢ is the lens that reveals it.*

---

> **In one line.** HUF and Hˢ are a *second viewpoint on data you already collect*: they read it from the
> compositional / relational angle — the message in the ratios — **at the speed of processing**,
> **deterministically and hash‑receipted**, and they do that *well*. No new instrument, no new collection, no
> replacement of your systems of record: a fast, reproducible re‑reading of what is already in hand, from a
> viewpoint the original collection did not take.

## Do you have a composition?

**Not sure? Run the interactive gauge → [`COMPOSITION_GAUGE.html`](COMPOSITION_GAUGE.html)** — a few questions and a few numbers walk you to a go / no-go / higher-door answer, with the reasoning shown at each step. Offline; nothing is sent anywhere.

If your data is **parts of a whole, tracked in order** — shares that sum to a total, measured over time, depth, or position — Hˢ is built for it. Examples: an energy mix over years, taxa in a gut over days, oxides down a core, market sectors over quarters, failure modes across a fleet, a budget across categories.

If your data is **not** compositional — raw signals, or absolute counts with no shared whole — then, with respect, Hˢ isn't the best tool for it, and we'd rather tell you kindly up front than waste your time: other methods are better suited to that, and we genuinely hope they serve you well. Hˢ won't force a fit (though it can still give you a standard static picture if that's all that's wanted). **An AI assistant can confirm the fit in one look at your data** before you invest any effort — sorry, compositions only.

**Or compose one level up.** If your raw data isn't a composition, a composition may still exist *above* it — the mix among **samples**, among **methods**, or among the **people and systems that study your subject**. Don't study the thing; study the *composition of those who study it*, track it in order, and Hˢ reads whether that mix has a direction. That is how a chaotic field can still yield a heading — not the device under test, but the composition of the observers of it.

## What Hˢ does, by D (the number of parts)

The instrument scales with your data, and what it offers depends on **D**:

| Your D | What Hˢ gives you |
|---|---|
| **D = 2** | one balance in motion — the single ratio read exactly (e.g. gold↔silver, pass↔fail). Modest, but exact and receipted. |
| **D = 3** | the classic ternary picture **plus its motion** — where the mix sits and where it's heading; the diagnosis speaks in a voice or two. |
| **D = 4** | the **exact** case: your composition *is* a unit quaternion (S³ = SU(2)); read and rebuilt **losslessly to machine precision**. The mathematically special rung. |
| **D = 5 – 50** | the working range — full kinematics: who's steering, the arrow of intent, how concentrated, datable regime changes, the character of the system; the diagnosis names the movers. |
| **D = 50 – 1,000** | high‑dimensional — tiled into four‑part charts and reconstructed losslessly; the diagnosis speaks in **many voices** (a microbiome of hundreds of taxa says which are gaining and shedding). |
| **up to D = 1,000,000** | proven — a tree‑atlas reconstructs a million parts to **~4.1×10⁻¹²** (floating‑point accumulation, not bit‑exact identity, but far below any practical threshold), in a few seconds. High complexity is the design point, not the limit. |

And at **any** D where the total is a real magnitude (TWh, IOPS, dollars), the **moving budget** tracks whether the whole is growing, shrinking, or steady — alongside the mix.

## How to get started — three steps

1. **Shape your data:** a table with rows = time/order points, columns = the parts (carriers).
2. **Run it:** `from hs_kinematics_engine import run; out = run(M, names)` — or hand the table to an AI assistant and ask it to run Hˢ.
3. **Read it:** the plain‑language **diagnosis** tells you what the system is doing in your own field's terms; the full output gives every reading, named twice (navigation / physics), with a receipt. **The meaning stays yours** — Hˢ says who moves and when; you say what it means.

Everything you need to reproduce or hand to a student is in **[`Hs-Kinematics/`](Hs-Kinematics/)**: the engine, the full specification, language‑agnostic pseudocode, an R port, a replication notebook, and the intake tools.

## An AI assistant can be your guide

You do not need to know compositional data analysis to use Hˢ. **An AI assistant can be trained on the Hˢ system** (start it at [`AI_WELCOME.md`](AI_WELCOME.md) → [`AI_ASSIST.json`](AI_ASSIST.json) → [`onramp/PHD_ONRAMP_PROTOCOL.md`](onramp/PHD_ONRAMP_PROTOCOL.md)) to:

- **confirm Hˢ is the right tool** for your data — and say so honestly if it isn't;
- **tell you what it can do at your D**, from the table above;
- **run it and translate** the readings into the words your field uses;
- **stay honest** — if the engine holds (nothing resolvable), is near its boundary, or hits a guard, the assistant tells you what cannot be resolved and why.

Bring your data; the assistant carries the CoDa.

## The honest line

Hˢ reveals what your carefully prepared data is already doing — **exactly, reproducibly, with a receipt, and it tells you where it cannot help.** It will not invent a signal that isn't there; it would rather hold or warn than hand back a confident wrong answer. That restraint is the point. The hard work of gathering and preparing your data is the achievement; Hˢ is the instrument that lets it be seen.

*One instrument; any composition; as far as the data can be known and not one step further; and the receipt to prove it.*
