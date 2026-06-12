# Cross-AI Coordination — How Claude, ChatGPT, and Grok work together on Hs

**Prepared:** 2026-05-12 (push #44)
**Status:** Active governance document
**Authority:** Peter (sole authority gate for all canonical changes)

---

## Why this document exists

By May 2026 the Hs project is being inspected and prepared by three independent AI platforms — Claude (with file tools + bash sandbox + write access), ChatGPT (with GitHub connector, read access + PR drafting, no execution), and Grok (with web fetch, read-only, independent reviewer). Each has distinct capabilities and distinct failure modes. Without coordination, the platforms either duplicate work, contradict each other, or upgrade each other's inspected evidence into executed evidence and produce false confidence.

This document is the apparatus that lets the three work coherently against the same artifacts in the run-up to CoDaWork 2026 (Coimbra, Portugal, 1–5 June 2026) and beyond.

---

## Per-platform capability matrix

| Capability | Claude (this session) | ChatGPT (GitHub connector) | Grok (web fetch) | Peter | GitHub Actions CI |
|---|---|---|---|---|---|
| Read repo files | Yes | Yes (limited rate) | Yes (web only) | Yes | Yes |
| Search repo by symbol/string | Yes | Yes | Limited | Yes | Yes |
| Run code in sandbox | Yes (Linux sandbox, no GPU) | No | No | Yes (workstation) | Yes (CI runners) |
| Write files to local checkout | Yes | No | No | Yes | Yes (in CI workspace) |
| Commit and push to GitHub | No (Peter authorizes) | Draft PR only | No | Yes | Yes (via workflow) |
| Produce executed evidence | Yes (in session) | No | No | Yes | Yes (public receipts) |
| Produce inspected evidence | Yes | Yes | Yes | Yes | N/A |
| Make canonical-state claims | No (Peter authorizes) | No | No | Yes | No |
| Run pytest / pipeline scripts | Yes | No | No | Yes | Yes |

Two rules follow from this matrix:

1. **Never upgrade inspected evidence into executed evidence.** A ChatGPT or Grok claim that "the test passes" based on reading code is inspected, not executed. Only Claude-in-sandbox, Peter at workstation, or CI produces executed evidence.
2. **Peter is the only authority gate.** No AI commits to main. All canonical-state changes require Peter's explicit authorization in the conversation.

---

## Division of labor

**ChatGPT — adviser, structure, claim audit, PR drafting.** Best at: reading large structural surfaces, drafting PRs, auditing claims against doctrine, producing JSON specifications. Not at: execution, numerical verification, fresh runs.

**Claude (this session) — executor, test runner, file writer.** Best at: running the actual commands the packet specifies, writing files to the local checkout, iterating against pytest output, building the bundle, presenting HOLD-TO-PUSH state. Not at: independent review of its own work (use cross_check_archive entries for that).

**Grok — independent reviewer, devil's advocate.** Best at: arriving with no context and producing fresh signal/noise verdicts, cross-checking nomenclature, catching stale-cache assumptions. Not at: execution, structural changes.

**Peter — authority gate, narrative author, conference speaker.** Sole authority for: catalog disposition, push release, doctrine changes, NO-CREATE list adjustments. The three AIs produce drafts; Peter authorizes.

**GitHub Actions CI — public receipt mechanism.** Runs the Validate Repository workflow on every push. Produces the public log that anchors each commit SHA to a green/red verdict.

---

## Shared artifacts (the coordination surface)

These files are the common ground. Any AI session can read them; only Claude-in-sandbox can write them; only Peter can authorize them into main.

| Artifact | Owner | Read by | Written by |
|---|---|---|---|
| `ai-refresh/INVESTIGATION_CATALOG.json` | Master catalog | All three AIs + Peter | Claude (in session); Peter authorizes |
| `ai-refresh/HS_ADMIN.json` | Admin / session log | All three AIs + Peter | Claude (in session); Peter authorizes |
| `ai-refresh/HS_FAST_REFRESH.json` | Fast-state snapshot | All three AIs + Peter | Claude (in session); Peter authorizes |
| `ai-refresh/PUSHES_INDEX.md` | Chronological push index | All three AIs + Peter | Claude (in session); Peter authorizes |
| `ai-refresh/HS_REPO_STRUCTURE_TREASURE_MAP.json` | Navigation aid | All three AIs + Peter | Claude (in session); ChatGPT drafted v1 |
| `ai-refresh/CLAIM_TEST_PACKET.json` | Validation framework | All three AIs + Peter | Claude (in session); ChatGPT drafted v1 |
| `ai-refresh/CROSS_AI_COORDINATION.md` | This file | All three AIs + Peter | Claude (in session) |
| `ai-refresh/cross_check_archive/*.md` | Per-session archives | All three AIs + Peter | Claude (writes the archive entry from the transcript Peter pastes) |

---

## Handoff conventions

**ChatGPT → Claude.** ChatGPT produces a JSON spec or a PR draft. Peter pastes the relevant material into the Claude session. Claude integrates the material into the repo following the patterns in this document. The ChatGPT session is archived under `cross_check_archive/chatgpt_*_YYYY-MM-DD.md`.

**Grok → Claude.** Grok produces a review with signal/noise/hallucination verdicts. Peter pastes the transcript. Claude appends a `cross_check_archive/grok_round_N_session_YYYY-MM-DD.md` entry that preserves the transcript verbatim and adds per-section verdict annotations. Any actionable items become STAGED catalog entries.

**Claude → ChatGPT.** Claude produces a bundle (the push). Peter pushes to GitHub. ChatGPT (via connector) reads the resulting commit and either confirms or flags discrepancies against the spec it drafted.

**Claude → Grok.** Claude produces a state snapshot (HS_FAST_REFRESH.json, REPO_STATE_YYYY-MM-DD.md). Peter shares the snapshot with Grok. Grok reads and reviews.

**All three → Peter.** Each AI surfaces its findings as candidates. Peter decides what becomes canonical, what stays STAGED, and what is DEFERRED or FALSIFIED.

---

## Cross-check archive append rules

Per the existing `cross_check_archive/README.md`:

When to archive verbatim:
- Cross-check session produced a mix of valid + false findings
- AI platform exhibited a new failure mode worth cataloguing
- Substantive content needs preservation for future use even if not immediately actioned
- ChatGPT GitHub-connector sessions or Grok web-fetch sessions that produced JSON specifications or doctrine elaboration

When NOT to archive:
- Session produced clean canonical contributions → goes in a regular AI_REFRESH_*.md push narrative
- Session was pure conversation without findings

Filename pattern: `<platform>_<session_descriptor>_<YYYY-MM-DD>.md`. Examples: `grok_round_5_session_2026-05-11.md`, `chatgpt_github_connector_session_2026-05-11.md`.

Required sections in the archive entry:
1. Source and date
2. Context (what the session was about)
3. Verbatim transcript or structured summary with per-section verdicts (✅ SIGNAL / ⚠️ MIXED / ❌ HALLUCINATION / FABRICATED)
4. Catalog entries produced (if any)
5. Status: which findings were actioned, deferred, or rejected

---

## The "never upgrade inspected evidence" rule

This is the most important line in this document.

If ChatGPT reads `HCI/cnt.py` and writes "the test on line 142 will pass when EMBER data is fed", that is **inspected evidence**. It is not a passing test. It is a structural prediction.

If Claude-in-sandbox runs `pytest HCI/tests/test_cnt.py::test_ember_run` and sees `1 passed in 4.2s`, that is **executed evidence**. It is a passing test.

If GitHub Actions CI runs the same command on the same SHA and produces a green log, that is **public executed evidence**. It is the most durable form.

Any AI session — any platform — that converts inspected evidence into executed evidence in its narration is **fabricating receipts**. The cross_check_archive pattern (which preserves FABRICATED annotations alongside legitimate findings) exists specifically to make this failure mode visible. Do not let it go uncaught.

---

## The three-platform pre-conference checklist

Before CoDaWork 2026 (1–5 June 2026), the goal is that each canonical claim in the matrix (see `CLAIM_TEST_PACKET.json`) has been:

- [ ] Read and reviewed by ChatGPT (inspected evidence + PR draft if needed)
- [ ] Read and reviewed by Grok (inspected evidence + independent verdict)
- [ ] Executed by Claude-in-sandbox (executed evidence, in-session)
- [ ] Executed by GitHub Actions CI (public executed evidence, anchored to commit SHA)

When all four boxes are ticked for a given claim, that claim is **triply attested** and the speaker can present it with confidence at the lectern. The cross-check archive carries the receipts for the inspection rounds; the CI log carries the receipts for the execution rounds; this document carries the map between them.

---

## Long-view rationale

The reason for the apparatus, in one paragraph: a single AI session can be wrong in subtle ways that another AI session would catch immediately. Two-of-three platform agreement raises confidence sharply. Three-of-three agreement against the same artifact, with executed evidence anchored to a public commit, is the strongest pre-conference position a small research project can build. The cost is a modest amount of cross-referencing; the payoff is a talk that survives skeptical Q&A because the speaker can name which platform produced which receipt.

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
*First classify the environment. Then choose the route. Never upgrade inspected evidence into executed evidence.*
