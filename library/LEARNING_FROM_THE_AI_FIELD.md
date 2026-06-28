# Learning from the field — the world of AI / expert systems read as a composition, and what to take from it

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. We sit at
the headwaters of one large expert-system effort; we are not the only river. This turns the instrument on our
**own field**: reads the world of AI / expert-systems development as a composition, places HUF/Hˢ in it, finds
who is **nearest** (allies to learn from) and **farthest**, and — the point — names, per axis, **who is more
battle-tested than us** so we can compose their maturity into our design. Map + receipt:
`ai_systems_composition_map.py` (`c83aa2555d857d40`). Grounded in a June-2026 landscape scan (sources at the
end). Honest-broker tiered; the scores are reasoned estimates of *schools*, not measurements of teams; allies
are named only to cite and learn from, never to imply collaboration. Peter is the sole gate; nothing posted.*

---

## The honest reading first (so the map isn't self-flattery)

The five axes the map uses — **determinism, compositionality, calibrated honesty, domain-grounding,
provenance** — are *our own design values.* So Hˢ sits near the corner **by construction.** That is not
evidence we are best, and the map says so out loud. Two things in it are real and useful anyway:

1. **Nobody else sits near all five at once.** That intersection — exact, compositional, honest, grounded,
   receipted — is our actual niche, and the map confirms it is unoccupied.
2. **On every single axis, an external school is more mature than us** — in scale, community, shared
   benchmarks, or proof-at-volume. Our scores are high by design; *their execution is hardened by years and
   crowds.* So the instruction the map gives is not "we win" — it is **compose their maturity into our design.**

## The field, nearest to farthest (who our neighbours are)

The map ranks the schools by distance from Hˢ in those five coordinates:

| rank | school | nearest to us on | what they have that we don't |
|---|---|---|---|
| 1 | **Compositional Data Analysis (CoDa)** | compositionality, grounding | our **home field and peers** — decades of method and real reviewers |
| 2 | **Neuro-symbolic AI (3rd wave)** | compositionality | a mature **symbolic-layer** framing; symbolic rules → formal *impossibility* proofs |
| 3 | **Reproducibility / provenance governance** | provenance | **shared standards** — AAAI/CVPR reproducibility checklists, compute reporting |
| 4 | **RL with Verifiable Rewards (RLVR)** | determinism | a **deterministic checker that generates unlimited data** |
| 5 | **Formal NN verification (VNN-COMP)** | determinism | an **open adversarial competition** with public benchmarks |
| 6 | **Calibrated-uncertainty / abstention** | honesty | explicit **over- and under-confidence penalties**; span-level claim checking |
| 7 | **Mainstream LLM / agentic foundation** | (the far pole) | **scale, reach, fluency, adoption** — where the users already are |

The shape is telling: our nearest neighbours are the *structured* schools (CoDa, neuro-symbolic), and the
farthest is the *generative* mainstream — the same near/far axis the world-composition map found, now pointed
at AI itself. We are far from where the users are, and that distance is the thing to bridge.

## The suggestions — compose each neighbour's strength into ours

Each suggestion takes one school's hardened practice and folds it into an existing Hˢ artifact. None replaces
what we have; each is the field's own lesson, applied.

1. **Stand up a public falsification arena (from VNN-COMP + reproducibility governance).** Our receipts make
   claims re-computable, but we have no *open arena* where outsiders try to break them. The field's discipline
   is the **competition and the checklist.** Suggestion: turn `transition_readiness.py` / `HOW_TO_VERIFY.md`
   into a published "re-run and try to break it" challenge with an AAAI/CVPR-style reproducibility checklist
   at the door. *Verifiability becomes a sport, not a footnote.* (T2 — a process change, Peter-gated.)

2. **Make the receipt a data-generating checker (from RLVR).** RLVR's insight: a deterministic checker can
   manufacture unlimited training and evaluation data. **Our receipts already are deterministic checkers.**
   Suggestion: generalize `hs_dut_stress.py` / `hs_gen2.py` so the receipt auto-generates an endless, labelled
   stress corpus (deform → read → check against the locked invariant) — self-supervised hardening with no
   human labels. (T1-feasible — we have the pieces; this composes them.)

3. **Harden the margin gate with calibration metrics (from Rewarding Doubt / REFIND).** The honesty school
   penalizes **both** over- and under-confidence and verifies each claim *span-by-span* against evidence. Our
   margin gate withholds at low confidence but is not yet *calibrated* against those metrics. Suggestion: add
   an explicit over/under-confidence penalty to the gate and a span-level "every tier-1 claim points at its
   receipt" check — measured calibration, not just a threshold. (T2 → T1 once implemented; sharpens the
   honest-broker core.)

4. **Position the determinism as the symbolic layer (from neuro-symbolic AI).** The third wave's pattern is
   neural fluency + symbolic rigor. **Hˢ's clr/ilr lock is exactly a symbolic invariant** a neural front-end
   can call for an exact, provable read. Suggestion: frame the locked-discriminant principle as a drop-in
   *symbolic-verification layer* for neuro-symbolic stacks — our determinism is their missing rigorous core.
   (T2 — positioning, ties to `locked-discriminant/`.)

5. **Be the trustworthy tool a generative agent calls (from the mainstream far pole).** We are farthest from
   where users live; the contact-length lesson applied to AI is to **bridge, not shout.** Suggestion: ship Hˢ
   as a verifiable *skill/tool* a fluent agent invokes when it needs an exact compositional read with a
   receipt — the determinism layer *under* the conversation. The far pole has the users; we have the thing
   their fluency can't give them (a re-computable answer). (T2 — strategic, the highest-leverage bridge.)

6. **Community-first with the peers, still (from CoDa).** The nearest school is the one we must not reinvent.
   The Q-node offer already does this; the lesson is to keep **citing and contributing before claiming** —
   reviewers, not megaphones. (Ongoing; `coda-q-node/`, `CODA-Association/`.)

## The one composite move

Read together, the six suggestions are a single idea, and it is our own: **we do not compete with any of these
schools — we compose.** Hˢ is the exact-compositional-provenance *core*; each neighbouring school is strong on
one axis and can plug into that core or have its practice folded in. The field is telling us the same thing we
tell the world: the value is in the relation between the parts, not in any one part winning. Our niche is to be
the part that makes the others' outputs **exact, honest, and re-computable** — and to learn their hard-won
execution while we do.

## Honest scope

- **T1 (measured/deterministic):** the *math* of the map — distances, per-axis leaders, ranking — is
  deterministic and receipted (`c83aa2555d857d40`, reproduces). The landscape facts are sourced below.
- **T2 (reasoned estimate / doctrine):** the per-school axis scores are estimates from a literature scan, not
  a survey; the six suggestions are design intent, not commitments. The reflexive bias (our axes → our corner)
  is named, not hidden.
- **T3 (to be earned):** that composing these lessons measurably improves Hˢ — testable only by doing them.
- **Falsifier:** rubric-survey each school's literature, refit the scores, and see if the near/far order and
  the per-axis leaders hold. **Allies named to cite and learn from, never to imply collaboration. Nothing
  posted; Peter is the sole gate.**

## Sources (June-2026 landscape scan)

- Neuro-symbolic / compositional AI: [A Survey on Compositional Learning of AI Models (arXiv 2406.08787)](https://arxiv.org/pdf/2406.08787); [Neuro-Symbolic AI: the Third Wave's Hybrid Core](https://gregrobison.medium.com/neuro-symbolic-ai-a-foundational-analysis-of-the-third-waves-hybrid-core-cc95bc69d6fa); [Compositional AI Beyond LLMs (ACM ASPLOS 2026)](https://dl.acm.org/doi/10.1145/3760250.3762235).
- Formal verification / verifiable rewards: [VNN-COMP 2025 Summary and Results (arXiv 2512.19007)](https://arxiv.org/pdf/2512.19007); [Formal methods for safety-critical ML — systematic review (Frontiers, 2026)](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2026.1749956/full); [awesome-RLVR (verifiable rewards)](https://github.com/opendilab/awesome-RLVR).
- Calibrated honesty / abstention: [Do LLMs Know When to NOT Answer? (arXiv 2407.16221)](https://arxiv.org/pdf/2407.16221); [Toward Trustworthy AI Development: Verifiable Claims (arXiv 2004.07213)](https://arxiv.org/pdf/2004.07213).
- Reproducibility / provenance: [What is Reproducibility in AI/ML Research? (AI Magazine, 2025)](https://onlinelibrary.wiley.com/doi/full/10.1002/aaai.70004); [Reproducibility: The New Frontier in AI Governance (arXiv 2510.11595)](https://arxiv.org/pdf/2510.11595).

*Cross-refs: `ai_systems_composition_map.py` (the map), `THE_WORLD_COMPOSITION_AND_STAGED_ONRAMP.md`
(the same near/far lens on application fields), `../papers/transition/transition_readiness.py` (the arena
seed), `../experiments/hs_dut_stress_2026-06/` (the checker seed), `locked-discriminant/` (the symbolic
layer), `../papers/coda-q-node/HS_AS_A_Q_NODE_FOR_CODA.md` (the peers). Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the map is deterministic and receipted · the reflexive bias is named, not hidden ·
every suggestion folds a sourced external practice into a real Hˢ artifact · we compose, we do not claim to
win · allies cited, not co-opted · the human keeps the gate.*
