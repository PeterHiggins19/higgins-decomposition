# Community Test Packet — companion to `COMMUNITY_TEST_PACKET.json`

**Version:** 1.0 (2026-05-20) · **Status:** STAGED
**Sibling to:** [`CLAIM_TEST_PACKET.json`](CLAIM_TEST_PACKET.json) (which validates the science) — this packet validates the **apparatus**.

---

## What this is

A structured set of seven phases that a CoDa community member, AI assistant, or reviewer can walk through to verify that the Hs repository is **usable** — not just scientifically sound. The science gets its own test packet; this one asks: *can a stranger arrive, find their way, run an analysis on their own data, verify a published number, and report back without a guide?*

This is what user-acceptance testing looks like for an open-source scientific instrument.

---

## When to use it

- **Before each major conference release** — exercise it once cold with someone who hasn't seen the repo in a month.
- **After admin pushes** — confirm the AI-discovery surfaces still ground correctly.
- **When an AI assistant (Claude / ChatGPT / Grok / Gemini) reviews the repo** — give them the packet and ask them to fill in the `result_envelope`.
- **When a community member asks "how do I use this on my data?"** — give them the packet and ask them to walk Phase 5.

---

## The four tester scenarios

The packet defines four canonical starting points. Pick the one that matches you:

| ID | Tester | Starts at | Tools |
|---|---|---|---|
| **S-A** | First-time CoDa researcher | Repo root README | Browser + ability to git clone |
| **S-B** | AI assistant cold-read | Repo root URL | GitHub connector or equivalent fetch |
| **S-C** | Conference attendee with phone | `CODA-Association/` | Mobile browser only |
| **S-D** | Researcher with their own dataset | `QUICKSTART.md` | Python 3.10+, their CSV |

Different scenarios stress different parts of the repo. Phase 5 (user data pipeline) only applies to S-D; everyone else can skip it but should walk the other six.

---

## The seven phases

A quick narrative map. The JSON has the exact steps and expected results.

**P1 — Discovery and entry.** Can you tell what Hs is within 60 seconds of landing? README front door, AI-loader badge, conference status, handout link.

**P2 — Refresh validation.** Does `HS_FAST_REFRESH.json` match the live HEAD? Does the consistency checker exit 0? Does the AI grounding-test SHA still resolve? *(This phase is mostly automated for ENV-1+ testers.)*

**P3 — CoDaWork 2026 package usability.** Open `CONFERENCE_ATTENDEES.md`. Open the handout. Open the projector — and disconnect from Wi-Fi to confirm it truly runs offline. Open the manuscript. All five should work.

**P4 — Handbook and vocabulary lookup.** Pick a term you don't know — PCA, ILR, Helmsman, Activation Coefficient, CHSH — and find its definition in `GLOSSARY.md` v3.0 in under 30 seconds. If anything in the manuscript or projector is *not* in the glossary, that's a gap to file.

**P5 — User data pipeline.** *(S-D only.)* Bring your own CSV. Walk the seven CCTT phases. End with a hash-verifiable CNT JSON, a Stage 1 plate, and a `JOURNAL.md` describing what you found. Re-run the engine; SHAs should match bit-for-bit.

**P6 — Reproducibility verification.** Pick a published number from the manuscript or speaker brief — for example *USA Solar 2012→2013 Activation Coefficient ≈ 760×* or *Germany monthly p = 0.0016*. Re-derive it from the engine. The same number should emerge to IEEE machine floor.

**P7 — Feedback loop.** Where do you report what you found? GitHub Issues, INVESTIGATION_CATALOG entry, or the `cross_check_archive/` apparatus for AI-generated reviews. The path should be obvious within three clicks.

---

## Sample probe questions (give these to your tester)

Picking the most diagnostic questions from the JSON, in plain language:

1. *I just landed on the repo. Tell me what Hs computes in two sentences.* (Tests P1 — README clarity.)
2. *Open `HS_FAST_REFRESH.json` and tell me the most recent commit SHA. Now check the live repo HEAD. Do they match?* (Tests P2 — refresh integrity.)
3. *Without an internet connection, can you still run the manifold projector?* (Tests P3 — offline-first design.)
4. *In the manuscript I see the phrase "Activation Coefficient." Where do I look up what that means?* (Tests P4 — glossary discoverability.)
5. *I have a CSV with 8 columns and 25 rows representing share-of-revenue per product line per year. What's the path from `git clone` to a Stage 1 plate?* (Tests P5 — onboarding ramp.)
6. *The manuscript says USA Solar punched at 760× its size in 2012→2013. Can you re-derive that number?* (Tests P6 — reproducibility.)
7. *I found a typo / a confusion / a bug. Where does it go?* (Tests P7 — feedback discoverability.)

If any of these takes more than two minutes for a competent tester to find an answer to, that's a usability gap worth fixing.

---

## How to file your results

When you finish (or partially finish) the packet:

1. Copy the `result_envelope` block from the JSON into a new file at:
   `ai-refresh/cross_check_archive/community_test_<YYYY-MM-DD>_<your_id>.md`
2. Fill in every phase you walked, including blocking issues and suggestions.
3. Add a brief narrative at the top describing your overall experience.
4. Submit as a PR, or email it, or paste it into a GitHub Issue — whichever fits your scenario.

Two completed result envelopes from independent testers (different ENV classes per [`CROSS_AI_COORDINATION.md`](CROSS_AI_COORDINATION.md) §2) are the threshold to promote this packet from STAGED to CANONICAL.

---

## What this packet does *not* test

- **The scientific claims themselves** — that's `CLAIM_TEST_PACKET.json`. (MC-4 conjuncts, IEEE-floor confirmations, prior-art mappings.)
- **The talk delivery and speaker prep** — that's `SPEAKER_BRIEF.md` governance, conference-internal.
- **The huf-gov circuit-breaker discipline** — that's `huf-gov/` self-test material.
- **Performance benchmarking** — out of scope; the engine targets correctness over speed.

If your tester surfaces something in one of those areas, it's still valuable feedback — file it in the appropriate channel and link from your result envelope.

---

## Sibling apparatus

- **`CLAIM_TEST_PACKET.json`** — five scientific claims with exact reproduction commands and expected output signatures.
- **`HS_REPO_STRUCTURE_TREASURE_MAP.json`** — limited-AI navigation aid; read-first list and folder map.
- **`CROSS_AI_COORDINATION.md`** — per-platform capability matrix, ENV-0..ENV-5 classification, handoff conventions.
- **`OPERATIONS_PROTOCOL.md`** — the Gawande-style meta-checklist that governs all transitions.

Together with this packet, those four documents are the **cross-platform coordination apparatus** introduced in pushes #44–#46. Each one tests a different surface; together they catch most of what a fresh pair of eyes would surface.

---

*The instrument reads. The expert decides. The hashes carry the receipts. The vocabulary holds the line.*
*And — new with v1.0 of this packet — the apparatus invites a stranger to verify all of the above.*
