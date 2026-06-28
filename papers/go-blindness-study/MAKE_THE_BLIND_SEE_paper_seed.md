# Make the blind see — a game that makes ratio-blindness evident (P1 companion paper seed)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. A paper
**seed**, staged for arXiv as the **engaging companion to P1**: where P1 (CNQ-tiling) proves the *exact* math —
a four-part composition is a quaternion, read exactly, ratio-blindness lifted — this paper makes the **cost** of
ratio-blindness **evident and felt**, through a game played thousands of times with statistics. People like
games; the two released together read as a series. Evidence: `go_blindness_study.py` (`30ecbc0d25363162`),
N = 2400. Honest-broker tiered; a synthetic parable, not Go tactics; **Peter is the sole gate; nothing posted.**

---

## Abstract (seed)

We give a controlled, Go-framed contest in which two decision-makers watch the same board: one reads the
**relational** position (the compositional / log-ratio view), the other reads only **absolute** levels (stone
counts). Both place stones at the same rate, so the absolute scoreboard stays even; meanwhile one side converts
territory in **proportion** — a shift that lives entirely in the ratios. Across **2,400 randomized games** in
three drift regimes, the absolute-only ("blind") player is **blindsided in 97.9% of games** (95% CI
97.3–98.5%) — it sees an even board (mean margin **1.6**, far below any alarm) at the very move the game is
already decided — while the relational ("Hˢ") player sees the decisive turn **13.6 moves early on average**
(95% CI 13.4–13.8). A one-way ANOVA of foresight across drift regimes is decisive (**F = 4915, p < 10⁻³**):
faster proportional drift decides the game sooner, shrinking foresight (18.7 → 7.3 moves) while *raising* the
blindsided rate to 100%. The cost of ratio-blindness is not anecdote; it is large, robust, and statistically
certain **within the model.**

## The game (and why it makes the point evident)

A composition is hard to feel; a lost game is not. The board state is `{black-control, white-control,
contested}` — a composition. The win-condition lives in the **proportion** of decided territory, while the
**stone count** (the thing a level-only player watches) is held even by construction. So the board *looks* even
to the blind player from start to finish — and then the game is simply over. That is the **deceptive drift**
(*every alarm green while the mixture turned*, the gas-tank result) made **competitive and visceral.** The
reader does not need the simplex to feel it: *you can be dead even on the scoreboard and have already lost.*

## The evidence (statistics, not a story)

`go_blindness_study.py` (`30ecbc0d25363162`), N = 2400 across slow/med/fast drift:

| measure | result (95% CI) |
|---|---|
| **Blindsided rate** | **97.9%** (97.3–98.5) |
| **Hˢ foresight** | **13.6 moves** (13.4–13.8) |
| Absolute margin at the decided move | 1.6 (1.5–1.6) — even, vs an alarm at 6 |
| **ANOVA of foresight by drift regime** | **F = 4915, p < 10⁻³** |
| per regime (blindsided / foresight) | slow 94.6% / 18.7 · med 99.0% / 14.8 · **fast 100% / 7.3** |

The honest, interpretable finding the ANOVA carries: *the faster the proportional turn, the less warning the
absolute reader gets and the more certainly it is blindsided* — the blindness is worst exactly when the stakes
move fastest.

## Why publish it with P1

P1 is the **exact, beautiful** result — the foundation, the splash. It is also abstract. This game is the
**door**: it shows, with statistics anyone can re-run, *why the exactness matters* — because reading the ratios
is the difference between seeing the turn and being blindsided. Released as a pair, the series gains an
on-ramp: the curious reader plays the game (or reads its numbers), feels the cost, and then wants the math that
fixes it — which is P1. The companion **makes the blind see**, and the foundation paper shows them how.

## Honest scope

- **T1 (measured):** the 97.9% blindsided rate, the 13.6-move foresight, the even-board-at-decision (1.6), and
  the ANOVA (F = 4915, p < 10⁻³) are measured over 2,400 randomized games and reproduce (`30ecbc0d25363162`).
- **T2 (the framing):** that this demonstrates the cost of ratio-blindness in proportional competition is a
  reasoned reading; the mapping to real contests (markets, attrition, governance, the autonomous probe) is
  argued, not measured here.
- **The firm fence:** **Hˢ is not a Go engine and this is not Go tactics** — real Go engines are not
  ratio-blind. The statistics describe the **model's** behaviour across randomized conditions, **not** real Go
  and **not** a universal law. The claim is narrow and honest: *an absolute-only reader of a proportional
  contest is blindsided by a shift a relational reader catches — robustly, in this controlled study.*
- **Sole gate:** this is a **seed staged** for arXiv as P1's companion; **Peter posts. Nothing is posted.**

*Cross-refs: `go_blindness_study.py`, `../../simulations/games/HS_VS_BLIND_THE_CONSEQUENCE.md` (the single-game
parable), `../cnq_tiling_suite_2026/P1_ABSTRACT_LOCKED.md` (P1, the foundation), `../THE_SIMPLIFIED_RELEASE_PLAN.md`
(the series/on-ramp), `../../library/THE_BLINDNESS_SUITE.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the cost is measured over 2,400 games with CIs and an ANOVA · the game makes the
abstract result felt · fenced as a synthetic parable, not Go tactics, not a Go engine · positioned as P1's
companion, staged not posted · the human posts and keeps the gate.*
