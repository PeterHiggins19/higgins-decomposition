# ChatGPT deep-research reports — 2026-05-10 — INDEX + INV-052 reference

**Archive date:** 2026-05-10 (push #40)
**Catalog entry:** INV-052 (CANONICAL — methodological observation)
**Three reports archived in this folder:**

| File | Source | What it audited | Triggered by |
|---|---|---|---|
| `chatgpt_deep_research_report4_2026-05-10.md` | ChatGPT (Peter's session) | HCI-CNQ engine + repo packaging + license + R/Python parity | "review the repo" (no brief reference) |
| `chatgpt_deep_research_report5_2026-05-10.md` | ChatGPT (Peter's session) | Repo as a whole (README, HCI-CNQ, governance, dependencies) | "review the repo" |
| `chatgpt_deep_research_report6_2026-05-10.md` | ChatGPT (Peter's session) | HCI-CNQ engine again + conference readiness + hallucinated cnq.py/cnq.R diffs | "review the repo" |

All three were generated after push #38 (the EXTERNAL_REVIEW_INVITE.md was live) and after the push #38 AI-refresh addendum named the two findings + the open questions + the four defeat paths.

---

## The methodological observation (INV-052)

**None of the three reports engaged the brief at EXTERNAL_REVIEW_INVITE.md.** Three for three, ChatGPT defaulted to repository-wide deep audit when given a GitHub URL, rather than reading the planning folder and answering the five questions the invite asks.

What the invite specifically asks for (and what got engaged):

| The invite asks for | Report 4 | Report 5 | Report 6 |
|---|---|---|---|
| The two named findings (INV-050, INV-051) | not engaged | not engaged | not engaged |
| Methodological framing / claim-strength (MC-4) | not engaged | not engaged | not engaged |
| 10-beat slide structure for 15 min | not engaged | not engaged | not engaged |
| Three open questions for the community | not engaged | not engaged | not engaged |
| Prior-art / Category defeat paths | not engaged | not engaged | not engaged |

This is the methodological signal: **open-ended prompts that name only the repo URL trigger ChatGPT's repo-audit instinct, not the brief inside the repo.** A successful re-prompt would name the specific files to read, the specific questions to answer, and explicitly negate the deep-audit default ("do not audit the repository; do not look at HCI-CNQ").

---

## What WAS useful (signal we kept)

Three engineering findings, validated against the on-disk code in push #40:

1. **HCI-CNQ/README.md had stale "compiled engine still proposed" language** at lines 28, 66, and 118 — pre-push #32 wording that survived the v2.0.0 promotion. Refreshed in push #40.
2. **README.md and CITATION.cff carried stale "18 domains" and "v1.0.0 / CC-BY-4.0 software" metadata** — pre-push #34. Reconciled to "11 domains / 101 datasets" and `Apache-2.0` / `3.1.0` in push #40.
3. **No centralised reproducibility checklist for cold reviewers.** New `REPRODUCIBILITY_CHECKLIST.md` at repo root in push #40 — five-step verification path.

Additionally, three engineering findings from report 4 are queued (not blockers for the conference, slated for the post-conference cleanup INV):

- `pyproject.toml packages = []` while script entry points are declared → `pip install -e .` does not wire the scripts. Known-incomplete state in the file's own comments.
- `cnq.R` dimension dispatch is incomplete (D=3 and projected D≥5 advertised by classifier but not implemented in `cnq_run`). EngPromo-2 follow-on covers this when cnt.R goes to v3.1.0.
- `cnq.py` and `cnq.R` disagree on `radial_trajectory.std` (population vs sample). Parity bug, real, queued for post-conference cleanup.

---

## What was noise (we did not action)

**Hallucinations** in report 6 — these are important to flag because they would be load-bearing if blindly applied:

- Function name `QuaternionCalc(q1, q2)` in cnq.py — **does not exist.** The actual quaternion product is `quaternion_multiply` in `hci_shared/geometry.py`.
- Function name `cnqEngine <- function(x)` in cnq.R — **does not exist.** The actual entry point is `cnq_run()`.
- A made-up "seven-operator CNQ pipeline" (closure, quaternion embedding, variance trajectory, transcendental squeeze, classification, entropy test, mode synthesis). This is actually the *Hˢ master pipeline* (R∘M∘E∘C∘T∘V∘S) — not what CNQ specifically computes. CNQ's actual pipeline is Helmert/ILR projection → bearing trajectory → quaternion sandwich rotations → helmsman → attractor fit, per `CNQ_PSEUDOCODE.md`.
- Fake JSON diff patches against the made-up function names — if these had been applied to a real codebase they would have failed; if applied to a different codebase they would have introduced bugs.

**Numbers that don't match** anything in our docs (report 5):

- "53 decision units" — not in our docs
- "78 codes" — not in our docs
- "15/15 NATURAL classification preserved", "12/12 Fourier conjugation preserved", "58/58 subcompositional merges preserved" — not in our current docs (may be legacy v1.0 numbers from very old material)
- "9 HTML/Jupyter demo files" — invented count
- Timeline ending 2026-05-08 — misses pushes #32 through #39

**Stale metadata** (report 5 / 6):

- "License is CC BY 4.0 for software" — partially correct; the legacy CITATION.cff did say CC-BY-4.0 (fixed in push #40); the actual code LICENSE is Apache-2.0 and has been since push #28a (2026-05-08). ChatGPT's render of GitHub didn't pick up the split.
- "No requirements.txt / setup.py / Dockerfile" — wrong; `pyproject.toml` + `requirements.txt` shipped in push #28a. ChatGPT's deep-audit pass missed them.
- "Only 28 commits / 1 GitHub star" — date-of-snapshot only; the repo has progressed well past these numbers since report 5 was generated.

---

## Lesson for the next external review pass

The re-prompt that should work (tested-in-theory; not yet tested-in-practice):

> *I need a review for a 15-minute CoDaWork 2026 conference talk. **Do not audit the repository.** **Do not look at HCI-CNQ.** **Do not suggest code changes.** Only read these three files at these exact URLs:*
> *1. https://raw.githubusercontent.com/PeterHiggins19/higgins-decomposition/main/papers/codawork2026/planning/EXTERNAL_REVIEW_INVITE.md*
> *2. https://raw.githubusercontent.com/PeterHiggins19/higgins-decomposition/main/papers/codawork2026/planning/NAMED_FINDINGS_FOR_CODA_DISCUSSION.md*
> *3. https://raw.githubusercontent.com/PeterHiggins19/higgins-decomposition/main/papers/codawork2026/planning/CONFERENCE_2026_06_PLAN.md*
>
> *Then answer the five questions in EXTERNAL_REVIEW_INVITE.md. If you cannot fetch a file, say so and stop. If any answer would require commentary on code or repo structure, omit it.*

The bold negative framing is the load-bearing part. Without it, the repo-audit default reasserts.

---

## Cross-references

- INV-052: this catalog entry (CANONICAL, push #40)
- Earlier ChatGPT crosscheck: `chatgpt_corpus_review_2026-03-22.md` (the L2 → TV metric correction; archived as a success case — that review IS what gave us Appendix A of the HUF MC-4 packet)
- Grok crosschecks: rounds 2 and 3 archived as `grok_round_2_session_2026-05-08.md` and `grok_round_3_session_2026-05-08.md`
- Earlier methodological observations: INV-031 (AI platform fitness matrix), INV-032 (Grok round 2 findings split)

---

*Archived 2026-05-10 (push #40). The reports themselves are preserved verbatim in this folder for full traceability. The signal extracted from them landed in push #40 admin + REPRODUCIBILITY_CHECKLIST.md + HCI-CNQ README refresh + CITATION.cff fix. The noise was discarded explicitly so future sessions know what to ignore.*
