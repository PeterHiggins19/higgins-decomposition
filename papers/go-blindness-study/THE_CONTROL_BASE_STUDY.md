# The control base study — run it with no Hˢ

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. The control
arm Peter asked for: play the same 2,400 games with **no Hˢ** — the player reading only **absolute** levels — to
prove the main study's foresight is the **Hˢ effect**, not an artifact of the setup. Measured:
`go_blindness_control.py` (`4a529ad402f33da0`). The result is the cleanest kind: with no Hˢ, there is no sight.
Synthetic parable, not Go tactics; Peter is the sole gate; nothing posted.*

---

## The comparison (same games, two readers)

| arm | blindsided rate (95% CI) | foresight (mean, 95% CI) | games that ever alerted *before* the decision |
|---|---|---|---|
| **Hˢ (relational read)** | **0.0%** | **+13.6 moves** (13.4–13.8), all 2400 | 2400 / 2400 |
| **Control — no Hˢ (absolute only)** | **98.2%** (97.7–98.8) | **−21.0 moves** (−22.6 to −19.5) | **39 / 2400 (1.6%)** |

Two-sample comparison: **Welch t = 42.7, p ≈ 10⁻¹⁴⁹, Cohen's d = 2.97** (an enormous effect). The Hˢ arm's
large *positive* foresight has **no counterpart** in the control.

## What the baseline shows

With **no Hˢ**, the absolute-only player is functionally blind:

- it is **blindsided 98.2%** of the time — essentially always;
- its few alerts are **noise, not signal**: only **1.6%** of games produce any warning *before* the decision,
  and its average alert timing is **−21 moves** — it "sees" the threat, when it sees it at all, *long after the
  game is already lost*;
- there is **no predictive sight** to attribute to anything but luck.

The contrast is the whole point of a control: the Hˢ arm sees the decisive turn **every game, ~13 moves early,
and is never blindsided**; the no-Hˢ arm is blindsided almost always and never sees it coming. The difference
(d ≈ 3) is **attributable to the relational read alone** — same games, same noise, same thresholds, the *only*
change is whether the player reads the ratios. The foresight **is** the Hˢ effect.

## Why this strengthens the companion paper

A reviewer's first question of the main study — *"is the foresight real, or baked into the setup?"* — is
answered by this control: **strip out Hˢ and the foresight vanishes (goes negative).** The effect survives the
most basic falsifier, with a huge effect size and a p-value past any threshold. The two studies together — the
Hˢ arm and this no-Hˢ baseline — make the claim defensible: *the relational read, and nothing else, turns a
98%-blindsided player into a never-blindsided one.*

## Honest scope

- **T1 (measured):** the control's 98.2% blindsided rate, −21-move (non-predictive) foresight, 1.6% pre-decision
  alert rate, and the Hˢ-vs-control comparison (t = 42.7, p ≈ 10⁻¹⁴⁹, d = 2.97) are measured over 2,400 games
  and reproduce (`4a529ad402f33da0`).
- **T2 (the inference):** that the control isolates the Hˢ effect is the standard controlled-comparison reading.
- **The fence:** synthetic parable; **Hˢ is not a Go engine**; the statistics describe the **model** across
  randomized conditions, not real Go. **Nothing posted; Peter is the sole gate.**

*Cross-refs: `go_blindness_control.py`, `go_blindness_study.py` (the Hˢ arm), `MAKE_THE_BLIND_SEE_paper_seed.md`
(the companion paper). Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the control strips Hˢ and the foresight vanishes (measured) · same games, the only
change is reading the ratios · huge effect size, p past any threshold · fenced as a synthetic parable · the
human posts and keeps the gate.*
