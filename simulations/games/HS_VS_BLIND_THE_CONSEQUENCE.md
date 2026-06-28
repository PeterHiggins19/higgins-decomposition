# Hˢ player vs blind player — the consequence

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter: in
Go, give one player Hˢ and leave the other blind — consequences. Measured: `go_hs_vs_blind.py`
(`436f1de15b8676a4`). The blindness suite, made competitive: a proportional game can be **decided while the
board still looks even in stones.** Hˢ is **not** a Go engine — this is a parable of the cost of ratio-blindness
in a contest. Peter is the sole gate; nothing posted.*

---

## The consequence, in one run

Both players place stones at the same rate, so the **absolute stone margin stays 0.0** — the board looks
perfectly even the whole game. But White quietly converts contested territory into control — a **proportional**
shift. Result:

| who | what they read | when they saw the turn |
|---|---|---|
| **Hˢ player** | the relational control composition (clr) | **move 5** — acted in time |
| **Blind player** | absolute stone counts only | **never** — the margin stayed 0.0 |
| *the game* | — | **decided at move 12** (White's control share crossed 0.62) |

At the moment the game was already lost (move 12), the blind player's scoreboard read **dead even (margin
0.0)** while White's relational control was **0.624.** The blind player was **blindsided** — not narrowly beaten,
but beaten *without ever seeing it coming.* The Hˢ player had a **seven-move foresight** of the decisive turn.

## Why this is the worst kind of loss

A loss you can see coming, you can fight. The blind player's loss is the other kind: **the scoreboard says even
until the end, then the game is simply over.** That is the gas-tank deceptive drift — *every alarm green while
the mixture turned* — now in a contest, and it is exactly the failure mode behind a lost probe, a missed market
turn, a governance system that reports "stable" until it isn't. **Ratio-blindness does not lose loudly; it
loses silently, then totally.**

## What it generalizes to

The Go board is a stand-in. In **any** contest where the win-condition lives in the **proportions** —
territory, influence, market share, resource control, attrition, coalition share — a competitor reading only
**absolute levels** can be *even or ahead on the scoreboard while already losing the real game*, and will be
blindsided at the decision point. The relational reader's advantage is **earlier sight of the decisive turn**,
and that advantage **compounds** (the blind don't know they are behind, so they don't adapt). This is the same
result as the adoption-advantage (the blind are disadvantaged where data is compositional), the deceptive-drift
monitor, and the reason the autonomous probe needs a relational *skin* — a blind probe walks into the loss the
board was telling it about.

## Honest scope

- **T1 (measured):** decided at move 12, Hˢ saw it at move 5, blind never alerted, absolute margin 0.0 at the
  decided move; reproduces (`436f1de15b8676a4`).
- **T2 (the parable):** the mapping to real competition is a reasoned reading; the contest is a **transparent
  synthetic** model of a proportional game.
- **The fence — firm:** Hˢ is **not** a Go engine and this is **not** Go tactics. Real Go engines are not
  ratio-blind; the claim is narrow and honest — *a decision-maker who reads only absolute levels of a
  proportional contest is blindsided by a shift a relational reader catches.* **Nothing posted; Peter is the
  sole gate.**

*Cross-refs: `go_hs_vs_blind.py`, `THE_GAMES_LIFE_AND_GO.md` (Hˢ reads the game), `../../library/THE_BLINDNESS_SUITE.md`
(ratio-blindness), `../../industrial-instruments/gas-composition-study/` (the deceptive-drift original),
`../../industrial-instruments/sensor-skin/THE_AUTONOMOUS_PROBE_SENSOR_SKIN.md` (why a probe needs the relational
skin). Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the blindsiding is measured (even board, decided game) · the foresight gap is real ·
generalized to proportional contests with care · fenced as a parable, not Go tactics, not a Go engine · the
human keeps the gate.*
