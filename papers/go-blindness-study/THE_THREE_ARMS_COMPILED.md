# Three arms compiled — and what the third axis reveals

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. With the third
condition — **both players reading relationally (both-Hˢ)** — we now hold the full 2×2 of who-can-read-the-
relational-view, and three conditions is the minimum for a comparison to carry weight. The third axis shows
something a single pair test cannot: **the Hˢ benefit is an interaction with the opponent's view — it is the
shared relational view that has value, not an edge over a peer.** Measured: `go_three_arms_compiled.py`
(`f34141004be19ef8`), N = 2,400 games per condition, matched trajectories. Synthetic parable, not Go tactics;
Peter is the sole gate; nothing posted.*

---

## The three conditions (same games, same noise, only the reading changes)

| condition | player 1 | player 2 | late-registration rate | foresight | what happens |
|---|---|---|---|---|---|
| **Both-absolute** (the base) | absolute | absolute | **98.2% / 98.2%** | −21 moves | an absolute-only reader registers the proportional turn late on both sides |
| **One-Hˢ** (the asymmetric arm) | **Hˢ** | absolute | **0.0% / 98.2%** | **+13.6** / −21 | the relational reader has foresight — the asymmetric benefit |
| **Both-Hˢ** (the new arm) | **Hˢ** | **Hˢ** | **0.0% / 0.0%** | **+13.6 / +13.6** | both see the turn early — a fully-informed, fair contest |

Across the three conditions, per-player late-registration moves **98% → (0% / 98%) → 0%**. A χ² across conditions
is decisive: **χ² = 9,270, p ≈ 0**.

## The third-axis reveal

A pair test alone — *one-Hˢ vs the absolute-only base* — shows Hˢ helps. But two points cannot separate *what*
helps from *when* it helps. The **third** condition does:

- **Both-absolute:** the proportional turn is registered late by both readers. The game is settled while both
  watch an even board — the deceptive-drift situation, with no one holding the relational view.
- **One-Hˢ:** the benefit appears — and notice *where it lives*. It is not in Hˢ alone; it is in the **difference**
  between a reader who holds the relational view and one who does not.
- **Both-Hˢ:** give both readers the relational view and the asymmetry **resolves**. Both see the turn ~13 moves
  early; the game is settled on the **real position**, fully informed on both sides.

So the honest structure is an **interaction, not a main effect**: the asymmetric advantage in the middle arm is
the product of Hˢ *and* the absence of the relational view on the other side. Supply the view to both and what
remains is a fair, fully-informed contest. **The value is the shared view.** Stating that plainly makes the
study more trustworthy, and it points straight at the right way to offer the tool.

## The offer — a powerful tool joining a bench of powerful tools

The relational, compositional reading is not new and not ours alone. **It already exists, in scattered and
disconnected forms, across many fields** — geology, microbiome science, economics, signal processing, planetary
remote sensing. The idea has been loose in the world for a long time; relational and contextual reasoning has
been gaining ground across the sciences for decades. What is missing is not the idea but a **home** for it: a
coherent, documented, reproducible place where the pieces are gathered, named, and shown to work together.

That is the offer, in positive terms:

> **Here is a capable tool, taking its place on a bench already full of capable tools. The people responsible for
> choosing which tools to reach for deserve to know it exists and what it does — because the parts already exist,
> just scattered. Use what exists to create better value. If we do not gather and demonstrate it, someone else
> will; better to give it a good home and tell the world clearly.**

The three-arm result is exactly why this framing is the right one. The tool's value is **not** an advantage over
a peer who also reads the ratios — give both sides the view and the advantage dissolves into a fair contest. Its
value is that **the relational view can be shared**: when a market, a clinic, a grid, or an autonomous probe
reads relationally, the proportional turn is seen in time, by everyone who holds the view. That is a world worth
building toward — informed parity, more capable decisions, and a tool that earns its place on the bench by being
useful and well-documented, alongside the others rather than against them.

## Honest scope

- **T1 (measured):** the per-condition late-registration rates (98.2% / asymmetric / 0%), the +13.6-move foresight
  when Hˢ reads, the −21-move (non-predictive) absolute foresight, and χ² = 9,270 (p ≈ 0) across conditions are
  measured over 2,400 games per condition and reproduce (`f34141004be19ef8`).
- **T2 (the inference):** that this is an *interaction* (benefit = Hˢ × the other side lacking the view) and that
  both-Hˢ is a fully-informed fair contest is the standard factorial reading of the three conditions.
- **The fence:** synthetic parable; **Hˢ is not a Go engine**; the statistics describe the **model** across
  randomized conditions, not real Go and not a universal law. **Nothing posted; Peter is the sole gate.**

## The compiled series (where each piece sits)

| file | role | receipt |
|---|---|---|
| `go_blindness_study.py` | the one-Hˢ main study (N = 2,400, ANOVA) | `30ecbc0d25363162` |
| `go_blindness_control.py` | the absolute-only base (supply removes the foresight) | `4a529ad402f33da0` |
| `go_three_arms_compiled.py` | **all three conditions; the interaction reveal** | `f34141004be19ef8` |
| `MAKE_THE_BLIND_SEE_paper_seed.md` | the P1 companion paper seed | — |

*Cross-refs as above; `../cnq_tiling_suite_2026/P1_ABSTRACT_LOCKED.md` (P1, the foundation). Peter is the sole
gate; nothing posted.*

*Proof & Honesty Standard — three conditions, the minimum for a real comparison · the benefit stated as an
interaction (Hˢ × a shared view), with the value placed on sharing the view rather than on any edge · both-Hˢ
measured as a fully-informed fair contest · framed positively as a tool joining a bench of tools · fenced as a
synthetic parable, not a Go engine · the human posts and keeps the gate.*
