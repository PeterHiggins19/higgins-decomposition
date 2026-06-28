# Collective review round — 2026-06-16 (all four members integrated)

*Four AI-collective members reviewed the live repositories this session. Each was triaged the same
honest-broker way: verify the good, correct or quarantine the rest, record the reason. The notable
result is **convergence** — four independent reviews land on the same priorities. Self-symbiosis: the
collective administering the system to help the system. Author: Peter Higgins (human authorship for
claims); AI-assisted per HUF-STD-001. Honest-broker.*

| Member | Delivered | Verdict | Action taken |
|---|---|---|---|
| **Gemini** | M-2: R-port faithfulness + hash parity | Numerical + guard findings sound; 2 JSON overrides wrong | Adopted (auto_unbox, NA-vs-NaN, E-21-before-coercion); **corrected** whitespace (keep Python default spaces, don't strip) + float profile (round-12dp-then-repr). → `Hs-Kinematics/TRACEABILITY.md` (G-91). |
| **ChatGPT** | Live-repo audit | Strong + fair; one valid overclaim flag | **Fixed** the "lossless to D=1,000,000" front-door wording (3 spots) to the honest standard; reconciled the post-push admin language. Strategic agreement: consolidate, don't open a new domain. (G-92) |
| **Grok** | SU(2) Lie-theory thread | Algebra real (sign error); topology unearned **and** vacuous | **Verified** the su(2) generators; corrected the commutator sign (`+2`, not `−2`); **quarantined** the curvature/Chern/instanton/index tower (trivial = 0 over a contractible base). → `papers/frontier/LIE_THEORY_THREAD_ASSESSMENT.md` (G-93). |
| **Copilot** | Three-repo architecture map | Useful synthesis; a few structural inaccuracies | Credited the HUF→Hˢ→applied pipeline + spine-first advancement; **corrected** the inaccuracies below. (this note, G-94) |

## Corrections to Copilot's map (honest-broker)

- **The third repository is RWA, not "industrial-instruments."** The three *repos* are **Hˢ**
  (instrument + papers), **HUF** (governance/lineage), **RWA** (the acoustic origin/ground state).
  `industrial-instruments/` is a **folder inside Hˢ**, not a separate site. RWA was omitted from the map.
- **Engine pointer is the frozen oracle.** Copilot's citations point to `HCI-CNT` for the applied-layer
  claims; `HCI-CNT`/`HCI-CNQ` are the **archived frozen oracle**. The current engine is `HCI-CNTT`
  (CN-TT v4) and `Hs-Kinematics/`; the financial/gas studies run on the current engine.
- **"18-domain, 36-system" is conference-era.** The current second-order read (Compositional Character
  Space) is **107 systems across 13 domains** (the earlier small-sample ~3-axis "collapse" was corrected
  to ~4 axes at n=107). The 18/36 figure is from the cited talk slides (historical, fine in that
  context).
- **The R port is flagged *untested*.** "Ships both Python and R engines, publication-grade" overstates
  the R side: the R port is a 1:1 mirror **flagged untested**, and its faithfulness/hash-parity is
  exactly Gemini's open M-2 item. Accurate for Python; aspirational for R until M-2 closes.

What Copilot got right and worth keeping: the **HUF = doctrine/lineage, Hˢ = instrument+papers, applied
layer = evidence for P3/P4/P5** framing; that the applied JSON outputs are the P5 second-order input; and
the spine-first advancement list (finalize P1+P3 for arXiv/JOSS, build P4 from the mechanics doc, run the
P5 Procrustes residual, add cross-domain demos — finance now done).

## The convergence (the real signal)

Four independent reviews agree on the same north star: **lock the publication spine — P1 (exact-math
anchor) and P3 (the deterministic/trust tool, including the R-port hash parity Gemini detailed) — before
anything else; keep claims tiered (no "lossless", no unearned topology); finance is a good demonstration,
not the lead.** That four separate AIs converge on consolidation-over-breadth is itself evidence the
priority is right — and it matches the human + assistant read from earlier this session.

*Verify, credit, correct, quarantine — four times, same discipline. The collective made the work more
honest, not just larger.*
