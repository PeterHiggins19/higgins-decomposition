# Push Index — Conference-Prep Arc + Supporting Maintenance

Single chronological index of all pushes that delivered the CoDaWork 2026 conference preparation, with commit SHAs, CI run numbers, and one-line summaries. Useful for future reviewers tracing the arc from external review intake to talk-material lock.

For deeper detail on any push, see `HS_ADMIN.json.session_log` entry of the corresponding number, or the matching `PUSH<NN>_PRE_PUSH_SUMMARY.md` file in this folder.

---

## The conference-prep arc — pushes #38 through #44

| Push | Date | Commit SHA | CI run | One-line summary |
|---|---|---|---|---|
| **#38** | 2026-05-10 | `34913f8` | #36 ("HCI Coherence") | Two named findings (INV-050 metric-invariance + INV-051 5-of-9 deceptive drift) + external review invite + AI refresh addendum |
| **#39** | 2026-05-10 | `50b7e61` | #37 ("CodaWork 2026 Conference") | Three open questions explicitly named + MC-4 three-conjunct sharpening + INV-050 framing tightened + cut list for the 10-beat plan + null-model caveat moved onto Beat 5 slide |
| **#40** | 2026-05-10 | `50b7e61` (bundled with #39) | #37 | Three ChatGPT deep-research reports archived + HCI-CNQ README refresh + CITATION.cff license fix (CC-BY-4.0 → Apache-2.0) + REPRODUCIBILITY_CHECKLIST.md at repo root + INV-052 CANONICAL (ChatGPT review pattern observation) |
| **#41** | 2026-05-10 | `f176e2c` | #38 ("Three open questions") | Grok round 4 + ChatGPT session 2 signal extraction; INV-053 CANONICAL (prior-art Area 4 partial — Morais et al. + Arata & Onozaki) + INV-054 STAGED (Hˢ Ascent Path doctrine) + ILR_BALANCE_VIEW_FOR_EMBER.md (Grok-attributed) + three concrete conference-talk improvements actioned |
| **#42** | 2026-05-10 | `7bd8e91` | #39 ("CODAWORK2026 Conference") | Talk delivery infrastructure — `papers/codawork2026/talk/` folder with 19 files: README (oratory) + STUDY_PAGE (moot method) + CHEAT_SHEET (backstage) + BACKUP_PRESENTATION (AV failure) + 10 slide files + 5 Q&A bench cards. Phone-readable, self-contained, offline-capable. INV-055 CANONICAL |
| **#43** | 2026-05-11 | `e1f95e7` | #40 ("Investigation catalog") | Grok round 5 signal extraction (first session with full repo access). Six new INV entries: INV-056 STAGED (`fit_fixed_point()` Period-1 detection) + INV-057 STAGED (Householder formalisation) + INV-058 STAGED (Power Spectrum Analyzer) + INV-059 CANONICAL (cross-model framing validation) + **INV-060 STAGED (Yeast Factor diagnostic — real tool addition)** + **INV-061 STAGED (System Terms Catalog — prevents engine bloat)** |
| **#43-sync** | 2026-05-11 | `846693a` | #41 ("AI refresh") | Post-#43 HS_FAST_REFRESH counter sync (last_push #43, totals 61 / 33 / 6 STAGED) + `REPO_STATE_2026-05-11_post-push43.md` hand-off doc |
| **#44** | 2026-05-12 | *HOLD-TO-PUSH* | *pending* | **Spring cleaning + cross-AI coordination apparatus** (path-2-plus expansion). Spring cleaning: SPEAKER_BRIEF.md + PUSHES_INDEX.md + SHA back-fill (#38–#42) + Hs_Learning_Path legacy mark + READMEs refresh. AI coordination: `HS_REPO_STRUCTURE_TREASURE_MAP.json` (limited-AI navigation aid; ChatGPT v1 + Claude integration) + `CLAIM_TEST_PACKET.json` (mirror-repo validation framework, STAGED) + `CROSS_AI_COORDINATION.md` (per-platform capability matrix + handoff conventions) + ChatGPT GitHub-connector session archived. **No catalog changes. No new INV entries. No NO-CREATE files. No engine/tests/schema changes.** |

---

## What each push delivered (deeper detail)

### Push #38 — The opening move (`34913f8`, CI #36)

Codified two empirical findings as CANONICAL catalog entries and opened external review:

- **INV-050 CANONICAL** — TV distance and Aitchison distance agree on every shock hit/miss verdict across the 9-country EMBER 2001–2025 corpus. Preempts Metric defeat.
- **INV-051 CANONICAL** — Deceptive-drift signature fires in 5 of 9 EMBER countries at annual grain (AUS, CHN, GBR, IND, JPN). Preempts Case defeat.
- **External review invite** published at `papers/codawork2026/planning/EXTERNAL_REVIEW_INVITE.md`. Five specific questions for AI assistants + human reviewers.
- **AI refresh addendum** at `ai-refresh/AI_REFRESH_2026-05-10_codawork2026_v3_1_0_findings_and_external_review.md`.

### Push #39 — Claim sharpening (`50b7e61`, CI #37)

Actioned six self-review recommendations:

1. MC-4 sharpened to three-conjunct form: *"natively in Aitchison geometry + formal change detection + carrier-level attribution — combined into one observable stack."*
2. INV-050 framing tightened from "family of valid simplex distances" to "demonstrated pair-invariance for TV + Aitchison across the 9-country corpus"; broader-family invariance demoted to Q2.
3. Three open questions explicitly named at `papers/codawork2026/planning/THREE_OPEN_QUESTIONS.md` (Q1 abstract, Q2 INV-050, Q3 INV-051).
4. Cut list written into master plan §5.1.1.
5. Null-model caveat moved onto Beat 5 slide (out of speaker notes).
6. Prior-art search targets enumerated at `papers/codawork2026/planning/PRIOR_ART_SEARCH_TARGETS.md`.

### Push #40 — ChatGPT review intake (bundled in `50b7e61`)

Three ChatGPT deep-research reports archived verbatim at `ai-refresh/cross_check_archive/` with section-by-section signal/noise verdicts:

- Most useful findings actioned: HCI-CNQ README refresh (removed "compiled engine still proposed" stale language), CITATION.cff license fix (CC-BY-4.0 → Apache-2.0; version 1.0.0 → 3.1.0), new REPRODUCIBILITY_CHECKLIST.md at repo root (five-step verification path).
- **INV-052 CANONICAL** captures the methodological observation: ChatGPT defaults to repo-audit when given a GitHub URL, bypassing the brief inside the repo. Remedy is explicit deep-audit suppression in the re-prompt template.
- Hallucinated function names and fake JSON diffs explicitly disowned with `[FABRICATED]` annotations in the INDEX.

### Push #41 — Grok r4 + ChatGPT s2 signal extraction (`f176e2c`, CI #38)

Two narrowed-re-prompt external reviews on the same packet:

- **Grok round 4:** Cleanly engaged the brief on first answer, then drifted across follow-ups, then collapsed into hallucination when asked to "run cnq.py." Two real signal extracted: INV-053 prior-art Area 4 partial execution (Morais, Thomas-Agnan & Simioni 2017/2018 + Arata & Onozaki 2017) and a Grok-attributed SBP + 7×8 orthonormal contrast matrix for D=9 EMBER energy mix at `papers/codawork2026/planning/ILR_BALANCE_VIEW_FOR_EMBER.md`.
- **ChatGPT session 2:** Cleanest external review received; engaged the brief cleanly on first answer. Three concrete talk improvements adopted as default: Cuts 1+2 applied by default (not held in reserve); Q&A bench reordered Q3-first; Beat 9 prior-art sharpened to operational form (*"A defeater must combine all three conjuncts"*).
- **INV-054 STAGED:** Ascent Path doctrine filed verbatim at `ai-refresh/HS_ASCENT_PATH_HANDOFF_2026-05-10.json` per Peter's literal request. Phase 5 staging discipline prevents ripple before conference.
- **INV-052 narrative refined** with the Grok drift-to-hallucination observation.

### Push #42 — Talk delivery infrastructure (`7bd8e91`, CI #39)

Built `papers/codawork2026/talk/` as the phone-readable repo-as-presentation layer:

- **19 new files:** README (oratory), STUDY_PAGE (5-round moot method), CHEAT_SHEET (one phone screen), BACKUP_PRESENTATION (AV-failure protocol), 10 slide files, 5 Q&A bench cards.
- **Phone-readable design:** short paragraphs, no wide tables, self-contained, offline-capable.
- **INV-055 CANONICAL:** the talk-delivery infrastructure itself (branch-layer per Ascent Path tree taxonomy; does not touch trunk or root canon).

### Push #43 — Grok r5 signal extraction (`e1f95e7`, CI #40)

First external-review session with full GitHub repo access. ~10,000 words across 15+ subsections. Substantial valid signal mixed with some hallucination. Six new catalog entries:

- **INV-056 STAGED** — `fit_fixed_point()` Period-1 detection symmetric to `fit_attractor()`. Engineering gap identified; full design provided. Post-conference.
- **INV-057 STAGED** — Householder formalisation of the metric-dual involution (`M² ≈ I`). Paper-worthy mathematical bridge. Post-conference.
- **INV-058 STAGED** — Systemic Power Spectrum Analyzer (per-window per-component decomposition into Steering / Hidden / Coupling / Concentration). Depends on per-carrier Depth Tower decomposition methodology not yet implemented.
- **INV-059 CANONICAL** — Cross-model framing validation: ChatGPT session 2 + Grok round 5 independently arrive at the same humble-invitation methods-challenge framing from cold-reads of the MC-4 packet. **Talk posture externally validated across three internal + two external reviews.**
- **INV-060 STAGED** — **Yeast Factor diagnostic.** Real tool addition (4-phase classifier: dormant / activating / dominant / saturated / declining). Peter named the cross-domain pattern (loudspeaker, bread, energy, microbiome, finance); Claude designed the formalization.
- **INV-061 STAGED** — **System Terms Catalog.** Peter's architectural observation: prevent engine revisions for domain-specific cases by formalizing domain-term-to-engine-operation mappings as front-and-center user-facing wrappers.

### Post-#43 sync (`846693a`, CI #41)

Cleared push #43 HOLD-TO-PUSH flags + bumped HS_FAST_REFRESH counters (61 / 33 / 6) + wrote `REPO_STATE_2026-05-11_post-push43.md` as the conference-prep arc summary and AI-session hand-off document.

### Push #44 — Spring cleaning + cross-AI coordination apparatus (HOLD-TO-PUSH as of 2026-05-12)

Path-2-plus expansion of the spring-cleaning maintenance push. Two coherent goals in one push: leave the repo cleaner than it was, and equip the three AI platforms (Claude / ChatGPT / Grok) with a deterministic coordination apparatus for the final pre-conference stretch.

Spring-cleaning layer:
- `papers/codawork2026/talk/SPEAKER_BRIEF.md` — strategic compass for the speaker (8 parts).
- `ai-refresh/PUSHES_INDEX.md` — this file (full chronological traceability).
- `ai-refresh/HS_ADMIN.json` SHA back-fill for pushes #38–#42.
- `docs/Hs_Learning_Path.md` marked **LEGACY April 2026** (link to INV-054 STAGED).
- Talk folder cross-references + papers/codawork2026/README + Root README refreshed with What's New section.

AI-coordination layer (path-2-plus expansion, 2026-05-12):
- `ai-refresh/HS_REPO_STRUCTURE_TREASURE_MAP.json` — limited-AI navigation aid. Read-first list, doctrine files, folder map, INV catalog quick index, NO-CREATE protected list, binding doctrine lines. ChatGPT drafted v1 during 2026-05-11 GitHub-connector session; Claude verified all paths against live filesystem and integrated.
- `ai-refresh/CLAIM_TEST_PACKET.json` — mirror-repo claim validation framework, STAGED. Five claims (MC-4.C1 Aitchison-native, MC-4.C2 5-of-9 drift, MC-4.C3 carrier attribution, YEAST.C1 4-phase classifier, DOCTRINE.C1 engine-independence) with exact commands, expected output signatures, stop rules, ENV-0..ENV-5 classification, receipt format, promotion rule. STAGED until exercised end-to-end from two independent environments.
- `ai-refresh/CROSS_AI_COORDINATION.md` — cross-check apparatus. Per-platform capability matrix, division of labor, shared artifacts list, handoff conventions, cross_check_archive append rules, the "never upgrade inspected evidence" rule, three-platform pre-conference checklist.
- `ai-refresh/cross_check_archive/chatgpt_github_connector_session_2026-05-11.md` — archive of the ChatGPT session that produced the two JSON drafts and the ENV-0..ENV-5 doctrine. Peter's "ascend not descend" narrative correction preserved permanently.

Catalog state unchanged: **61 / 33 CANONICAL / 6 STAGED / 12 DEFERRED / 8 OPEN / 1 FALSIFIED / 1 CLOSED.** Phase 5 conference-window discipline intact: no NO-CREATE files created.

---

## Catalog state across the arc

| Push | Total | CANONICAL | STAGED | DEFERRED | OPEN | Other |
|---|---|---|---|---|---|---|
| Before #38 | 48 | 26 | — | 12 | 8 | 2 |
| After #38 | 51 | 29 | — | 12 | 8 | 2 |
| After #39 | 51 | 29 | — | 12 | 8 | 2 |
| After #40 | 52 | 30 | — | 12 | 8 | 2 |
| After #41 | 54 | 30 | 1 | 12 | 8 | 2 |
| After #42 | 55 | 31 | 1 | 12 | 8 | 2 |
| After #43 | 61 | 33 | 6 | 12 | 8 | 2 |
| After #44 (HOLD) | 61 | 33 | 6 | 12 | 8 | 2 |

The STAGED disposition was introduced in push #41 (INV-054 Ascent Path doctrine) to capture "canonical content with deferred ripple" per Phase 5 conference-window discipline. Five more STAGED entries were added in push #43 (INV-056, 057, 058, 060, 061).

---

## Cross-check archive (all preserved verbatim with verdicts)

| File | Source | Push | Verdict |
|---|---|---|---|
| `chatgpt_deep_research_report4_2026-05-10.md` | ChatGPT pre-#40 | #40 | Mixed — some real engineering findings; out-of-scope for brief |
| `chatgpt_deep_research_report5_2026-05-10.md` | ChatGPT pre-#40 | #40 | Mixed — comprehensive but stale-data hallucinations |
| `chatgpt_deep_research_report6_2026-05-10.md` | ChatGPT pre-#40 | #40 | Fabrication-heavy — invented function names + fake JSON diffs |
| `chatgpt_deep_research_2026-05-10_INDEX.md` | Claude analysis | #40 | INDEX — signal vs noise breakdown + retry template + INV-052 source |
| `grok_round_4_session_2026-05-10.md` | Grok r4 | #41 | First-answer signal + drift on follow-ups + hallucination on "run cnq.py" — INV-052 refinement source |
| `chatgpt_review_2026-05-10_session2_three_parts.md` | ChatGPT s2 | #41 | Cleanest external review — three concrete talk improvements adopted |
| `grok_round_5_session_2026-05-11.md` | Grok r5 | #43 | Longest session (full repo access) — INV-056 through INV-061 sources |
| `chatgpt_github_connector_session_2026-05-11.md` | ChatGPT GH-connector | #44 (HOLD) | First session with GitHub-connector access — produced TREASURE_MAP + CLAIM_TEST_PACKET drafts + ENV-0..ENV-5 environment classification doctrine. Substantial structural signal; integrated as doc-only + STAGED. |

The narrowed re-prompt template from the INDEX has now been validated across two independent external models reading the MC-4 packet cold. Both converged on the same humble-invitation framing. INV-059 captures this.

---

## Hand-off docs at each release point

| Doc | Purpose |
|---|---|
| `PUSH38_PRE_PUSH_SUMMARY.md` | Push #38 bundle summary |
| `PUSH39_PRE_PUSH_SUMMARY.md` | Push #39 claim-sharpening pass summary |
| `PUSH40_PRE_PUSH_SUMMARY.md` | Push #40 ChatGPT-intake summary |
| `PUSH41_PRE_PUSH_SUMMARY.md` | Push #41 prep (Grok r4 only initially, then expanded with ChatGPT s2) |
| `PUSH41_READY_FOR_COMMIT.md` | Push #41 release card (post-HOLD) |
| `PUSH42_READY_FOR_COMMIT.md` | Push #42 release card (talk infrastructure) |
| `PUSH43_PRE_PUSH_SUMMARY.md` | Push #43 prep (Grok r5 signal extraction) |
| `REPO_STATE_2026-05-11_post-push43.md` | Post-#43 hand-off card with full arc summary + next-cycle queue |
| `PUSH44_PRE_PUSH_SUMMARY.md` | Push #44 prep summary (spring cleaning + cross-AI coordination apparatus; HOLD-TO-PUSH as of 2026-05-12) |

---

## Engine / test / schema state — unchanged across the entire arc

All seven pushes were doc-only or admin-only. **No engine, test, or schema changes.** Engine versions locked at:

- `cnt.py` v3.1.0 (push #37, pre-arc)
- `cnq.py` v2.0.0 (push #32)
- `cnt.R` v3.0.0 (push #32; v3.1.0 parity queued as EngPromo-2)
- `cnq.R` v2.0.0 (push #32)
- 43-test suite green throughout

The Ascent Path Phase 5 conference-window discipline has been maintained: six NO-CREATE files (`docs/HS_ASCENT_PATH.md`, `CLAIMS_REGISTER.md`, `GLOSSARY_CANON.md`, `PROMOTION_LOG.md`, `PROMOTION_PACKET_TEMPLATE.md`, `STAGED_ASCENT_MAP.md`) remain uncreated and will not be created before 2026-06-06.

---

## What comes after the conference (post-2026-06-05)

Six STAGED entries form the post-conference research roadmap in dependency order:

1. **INV-061** System Terms Catalog — front-door + per-domain wrappers + auto-detect + pipeline gate
2. **INV-054** Hˢ Ascent Path doctrine — Phase 2 onward (HS_ASCENT_PATH.md + 5 supporting files)
3. **INV-058** Power Spectrum Analyzer — requires per-carrier Depth Tower decomposition methodology first
4. **INV-060** Yeast Factor diagnostic — depends on INV-058
5. **INV-056** `fit_fixed_point()` — engineering completeness
6. **INV-057** Householder formalisation — paper-worthy theoretical work

Highest cross-domain value: INV-060 (Yeast Factor) + INV-061 (Terms Catalog). Together they make the framework cross-domain usable (loudspeaker → bread → energy → microbiome → finance) without engine revisions.

---

*Index authored 2026-05-11 in push #44 (spring cleaning + SHA back-fill); expanded 2026-05-12 with the cross-AI coordination layer of the same push. Updated when new pushes land that materially change the arc.*
