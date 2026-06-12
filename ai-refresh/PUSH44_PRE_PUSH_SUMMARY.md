# PUSH #44 — pre-push summary (HOLD-TO-PUSH) — SPRING CLEANING + AI COORDINATION

**Date prepared:** 2026-05-11 (spring cleaning); **expanded 2026-05-12** with AI coordination apparatus.
**Push status:** **PREPARED locally — HOLD-TO-PUSH pending Peter authorization.**
**Push type:** doc-only + admin + cross-AI coordination (housekeeping + governance; no canonical doctrine changes; no new INV entries; no NO-CREATE files created)
**Active priority:** CoDaWork 2026 conference talk (Coimbra, Portugal, 1–5 June 2026)
**Engine / tests / schema unchanged.**

---

## Why this push exists

Original directive 2026-05-11: *"please do as much system maintenance updates and json structure refresh and full push setup with option 2 as suggested, and any other items that would make things easy... very nice time to do house cleaning for spring."*

Expansion directive 2026-05-12: *"add path 2 plus ensure the ai improvements are all onboard as these are now useable for Claude, grok and chatgpt to test and use in a coherent fashion to get this project fully tested and checked by 3 platforms before the conference would be excellent and likely solidifying for the entire structure and conference and a cross check apparatus to help Claude manage the system."*

This push leaves the repo cleaner, more traceable, and now equipped with a three-platform coordination apparatus so Claude / ChatGPT / Grok can work coherently against shared artifacts in the final three weeks before CoDaWork 2026 and beyond.

---

## What's in the expanded bundle

### 7 new files (was 3 in the original spring-cleaning bundle)

| File | Purpose |
|---|---|
| `papers/codawork2026/talk/SPEAKER_BRIEF.md` | **Strategic compass for the speaker.** 8 parts: motivation as orator, strategic objective per beat, per-country narrative (DEU/JPN/GBR/AUS/CHN/IND/FRA/USA/WLD), narrative arc (3 acts), speaker's compass per beat, 6-sentence fallback, Q&A posture, long-view rationale. |
| `ai-refresh/PUSHES_INDEX.md` | **Full traceability of the conference-prep arc (pushes #38–#44).** Chronological index with commit SHAs, CI run numbers, one-line summaries, catalog state at each push, cross-check archive verdicts, hand-off doc references, post-conference research roadmap. |
| `ai-refresh/PUSH44_PRE_PUSH_SUMMARY.md` | This file. |
| `ai-refresh/HS_REPO_STRUCTURE_TREASURE_MAP.json` (NEW IN EXPANSION) | **Limited-AI navigation aid.** Read-first list, doctrine files, folder map with key files per top-level folder, INV catalog quick index, NO-CREATE protected list, binding doctrine lines. Any AI session can read this and know where every important file lives within five minutes. ChatGPT drafted v1 during 2026-05-11 GitHub-connector session; Claude verified paths and integrated. |
| `ai-refresh/CLAIM_TEST_PACKET.json` (NEW IN EXPANSION, STAGED) | **Mirror-repo claim validation framework.** Five claims (MC-4.C1 Aitchison-native, MC-4.C2 5-of-9 drift, MC-4.C3 carrier attribution, YEAST.C1 4-phase classifier, DOCTRINE.C1 engine-independence) with exact commands, expected output signatures, stop rules, ENV-0..ENV-5 classification, receipt format, promotion rule. STAGED until exercised end-to-end from two independent environments. |
| `ai-refresh/CROSS_AI_COORDINATION.md` (NEW IN EXPANSION) | **Cross-check apparatus.** Per-platform capability matrix (Claude / ChatGPT / Grok / Peter / CI), division of labor, shared artifacts list, handoff conventions, cross_check_archive append rules, the "never upgrade inspected evidence" rule, three-platform pre-conference checklist. |
| `ai-refresh/cross_check_archive/chatgpt_github_connector_session_2026-05-11.md` (NEW IN EXPANSION) | **Archive of the ChatGPT GitHub-connector session** that produced the treasure map + claim test packet drafts and the ENV-0..ENV-5 environment classification doctrine. Section-by-section verdicts; Peter's "ascend not descend" narrative correction preserved permanently. |

### 7 modified files (unchanged from original spring-cleaning bundle)

| File | Change |
|---|---|
| `papers/codawork2026/talk/README.md` | Added SPEAKER_BRIEF as the strategic-compass first layer in the "five layers" intro + recommended reading order |
| `papers/codawork2026/talk/STUDY_PAGE.md` | Added "read SPEAKER_BRIEF first" note before the moot rounds |
| `papers/codawork2026/talk/CHEAT_SHEET.md` | Added SPEAKER_BRIEF link at the top of the backstage scanner |
| `papers/codawork2026/README.md` | Added "START HERE" section pointing at `talk/` + `planning/`; moved earlier manuscript drafts to "Earlier manuscript drafts (pre-MC-4)" historical section |
| `README.md` (root) | Added "What's New — May 2026 (CoDaWork 2026 Conference-Prep Arc)" section linking talk folder + SPEAKER_BRIEF + REPO_STATE + PUSHES_INDEX |
| `docs/Hs_Learning_Path.md` | Added **LEGACY — APRIL 2026** header note linking to INV-054 Ascent Path STAGED. Phase 2 prep that does NOT violate Phase 5 (just a label; no new files). Content unchanged. |
| `ai-refresh/HS_ADMIN.json` | SHA back-fill for pushes #38–#42 + push #44 session_log entry with expanded scope (4 changes listed) |

---

## Why the AI coordination apparatus belongs in push #44

The original directive was housekeeping. The expansion directive was: *"a cross check apparatus to help Claude manage the system."* These are the same goal at different scales — clean the repo and make it sustainable to maintain across three AI platforms. Doing them in one push keeps push boundaries clean (one push, one coherent goal: prepare the repo for the final pre-conference stretch).

Critically, **no canonical claims change** in this push. The treasure map and coordination doc are doc-only. The claim test packet is explicitly STAGED — it specifies what a mirror-repo run would do, but no mirror run has happened yet, so no canonical promotion follows. Phase 5 conference-window discipline is fully intact.

---

## SHA back-fill detail (unchanged from original bundle)

```
Push #38 | SHA: 34913f8 | CI run #36 "HCI Coherence"
Push #39 | SHA: 50b7e61 | CI run #37 "CodaWork 2026 Conference" (bundled with #40)
Push #40 | SHA: 50b7e61 | CI run #37 (bundled with #39)
Push #41 | SHA: f176e2c | CI run #38 "Three open questions"
Push #42 | SHA: 7bd8e91 | CI run #39 "CODAWORK2026 Conference"
Push #43 | SHA: e1f95e7 | CI run #40 "Investigation catalog"
Push #43 post-sync | SHA: 846693a | CI run #41 "AI refresh"
```

---

## What's explicitly NOT in this push (per Phase 5 discipline)

The Ascent Path NO-CREATE list remains intact. None of these are created in push #44:

- `docs/HS_ASCENT_PATH.md`
- `CLAIMS_REGISTER.md`
- `GLOSSARY_CANON.md`
- `PROMOTION_LOG.md`
- `PROMOTION_PACKET_TEMPLATE.md`
- `STAGED_ASCENT_MAP.md`

Marking `Hs_Learning_Path.md` as "Legacy April 2026" is Phase 2 prep that doesn't create new files. **No engine code or test changes. No catalog changes. No new INV entries. No NO-CREATE files created.**

The ChatGPT-drafted claim test packet is STAGED, not CANONICAL — it is a specification, not a passing run. It is promoted only after a complete batch of receipts from two independent environments is committed to `cross_check_archive/`.

---

## Hold-to-push protocol (when you authorize release)

8-step release sequence (extended for the expanded bundle):

1. Update `HS_FAST_REFRESH.json._meta.last_push` from `#43` → `#44`
2. Catalog counts unchanged (61 / 33 / 6) — no INV changes in this push
3. Source counts unchanged (USER 25, GROK 18, CHATGPT 10, CLAUDE 8)
4. Remove `push_44_prepared_held` from `HS_FAST_REFRESH.json._meta`
5. Remove `push_44_status` HOLD line from `HS_ADMIN.json._meta`
6. Set `push_44_completed = 2026-05-12` (or actual commit date)
7. Flip session_log push #44 `push_status` from HOLD to `PUSHED <SHA> 2026-05-12` after commit
8. After CI green: verify CROSS_AI_COORDINATION.md is reachable from root README; verify TREASURE_MAP paths still match live filesystem; if any drift, plan a refresh in next push

---

## Pre-flight checks (all green expected after admin commit)

| Check | Expected |
|---|---|
| 4/4 admin JSONs parse | OK |
| INV catalog math | 61 / 61 / 61 / 61 (unchanged from #43) |
| Push #44 session_log entry present with 4 changes | OK (HOLD status, ready for release) |
| 6 NO-CREATE files still uncreated | INTACT |
| SPEAKER_BRIEF.md present + 4-link cross-reference | OK |
| PUSHES_INDEX.md present + 7 pushes documented | OK |
| HS_REPO_STRUCTURE_TREASURE_MAP.json present + parses | OK (new) |
| CLAIM_TEST_PACKET.json present + parses + STAGED flag set | OK (new) |
| CROSS_AI_COORDINATION.md present + references treasure map + claim test packet | OK (new) |
| cross_check_archive entry for ChatGPT session present | OK (new) |
| Hs_Learning_Path.md carries LEGACY header | OK |
| Root README carries "What's New" section | OK |
| All 6 SHA back-fills present in session_log | OK |

---

## Recommended commit message

```
push #44 — Spring cleaning + cross-AI coordination apparatus

Path-2-plus expansion of the spring-cleaning bundle. Pure maintenance +
governance push. No catalog changes. No new INV entries. No engine /
test / schema changes. No new NO-CREATE files (Phase 5 discipline
intact).

Major additions:
  papers/codawork2026/talk/SPEAKER_BRIEF.md — strategic compass for
    the speaker.
  ai-refresh/PUSHES_INDEX.md — full chronological traceability of the
    conference-prep arc.
  ai-refresh/HS_REPO_STRUCTURE_TREASURE_MAP.json — limited-AI
    navigation aid (ChatGPT v1, Claude integrated, paths verified).
  ai-refresh/CLAIM_TEST_PACKET.json — mirror-repo claim validation
    framework (STAGED until exercised from two independent
    environments).
  ai-refresh/CROSS_AI_COORDINATION.md — cross-check apparatus:
    per-platform capability matrix, division of labor, handoff
    conventions, the "never upgrade inspected evidence" rule.
  ai-refresh/cross_check_archive/chatgpt_github_connector_session
    _2026-05-11.md — archive of the ChatGPT session that produced
    the JSON drafts and the ENV-0..ENV-5 doctrine.

Maintenance:
  HS_ADMIN.json — SHA back-fill for pushes #38–#42 + push #44
    session_log entry with expanded scope.
  docs/Hs_Learning_Path.md — LEGACY April 2026 header (link to
    INV-054 STAGED).
  Talk folder cross-references + papers/codawork2026/README +
    Root README — refreshed.

Catalog state unchanged: 61 / 33 CANONICAL / 6 STAGED / 12 DEFERRED
                         / 8 OPEN / 1 FALSIFIED / 1 CLOSED.
Sources unchanged: USER 25 / GROK 18 / CHATGPT 10 / CLAUDE 8.

No engine / test / schema changes.
```

---

## What this push delivers

**To the speaker:** SPEAKER_BRIEF + the apparatus that makes the talk's underlying claims testable across three platforms before Coimbra. By 2026-06-01 each canonical claim can be triply attested (Claude executed + CI public receipt + ChatGPT and Grok independent inspections).

**To the repo:** Cleaner front door (root README + papers/codawork2026/README + Hs_Learning_Path legacy mark), full traceability (PUSHES_INDEX + SHA back-fill), and a deterministic AI-navigation layer (TREASURE_MAP + CROSS_AI_COORDINATION) that any future AI session can use without archaeology time.

**To future reviewers:** The cross_check_archive now contains a full record of how ChatGPT, Grok, and Claude each contributed. The claim test packet specifies exactly what an independent reproduction would do. The receipts pattern is documented.

---

## Three weeks to Coimbra

- 20 days from today (2026-05-12)
- Conference talk material complete and validated across 5 reviews
- Cross-AI coordination apparatus now active for the final stretch
- Post-conference research roadmap (6 STAGED entries) ready to promote after 2026-06-06
- Phase 5 discipline intact throughout

**The work is sound. The framing is validated. The talk is ready. The repo is now cleaner than it has ever been, and the three platforms have an explicit way to work together.**

---

*Prepared 2026-05-11; expanded 2026-05-12 in push #44 (spring cleaning + cross-AI coordination). HOLD-TO-PUSH pending Peter authorization.*
