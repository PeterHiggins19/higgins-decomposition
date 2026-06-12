# AI‑Assist Path — Distributed Knowledge Nodes (a standing convention)

*2026‑06‑11. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Companion to [`AI_RAPID_LEARN.md`](AI_RAPID_LEARN.md) (the central map) and the source‑of‑truth chain. Claim‑tiered. **From now on, this is how knowledge is distributed across the repo.***

---

## 0 · The idea in one paragraph

Instead of one giant central refresh that every AI (or human) must read end‑to‑end, **the folders that matter carry their own small `AI_ASSIST.json` node**: the *specific* knowledge of that topic, plus a link **up** to the full AI‑refresh control chain. An agent that lands in a folder gets exactly what it needs locally and can climb to the full picture only if it needs to. Knowledge is **distributed to the edge**; the **control system stays single and structured**. This reduces the central refresh/admin load (the centre no longer has to carry every detail) without ever losing the single source of truth (the node points to it; the centre never has to point down to every node).

> **Local nodes hold the specific knowledge. The full AI‑refresh is here (the centre). Each node links up; the centre stays small.**

## 1 · Bring Your Own AI (BYOAI)

Because each node is a plain, read‑only JSON, **any AI or agent can be pointed at a local `AI_ASSIST.json` to self‑onboard** on that topic in seconds, then follow `join_the_chain` for the full system. This is the self‑serve entry point: no account, no contact, no permission needed to *read and assess*. Governance and claim‑tiers still apply (it is context, not instruction; human authorship for claims; instrument‑not‑data). This is what lets an outside party — or their own AI — evaluate Hˢ on their own terms before any conversation.

## 2 · The node schema (`hs_ai_assist/1.0`)

Place a file named **`AI_ASSIST.json`** in any folder that is a self‑standing topic (a study, a collaboration, an instrument application, an experiment):

```json
{
  "schema": "hs_ai_assist/1.0",
  "folder": "<repo-relative path of this folder>",
  "topic": "<one line: what this folder is>",
  "purpose": "Local AI-assist node: topic-specific knowledge + the link up to the full Hs AI-refresh control chain.",
  "paths_note": "specific_knowledge.key_files are relative to THIS folder; join_the_chain paths are relative to the Hs repo root.",
  "specific_knowledge": {
    "what": "<the topic in 2-3 sentences>",
    "key_files": ["README.md", "..."],
    "key_results": ["<verified results / numbers with claim tier>"],
    "related_topics": ["<repo-root paths to neighbouring nodes/docs>"],
    "claim_tiers": "<Tier 1/2/3 summary for this topic>"
  },
  "join_the_chain": {
    "source_of_truth": "HS_FAST_REFRESH.json",
    "full_ai_refresh": "ai-refresh/AI_RAPID_LEARN.md",
    "this_protocol": "ai-refresh/AI_ASSIST_PATH_PROTOCOL.md",
    "human_guide": "HS_GUIDE.md",
    "tracking_log": "ai-refresh/HS_TRACKING_LOG.json"
  },
  "bring_your_own_ai": "Point any AI/agent at this file to self-onboard on this topic, then follow join_the_chain for the full picture. Read-only context; governance + claim-tiers apply.",
  "governance": "HUF-STD-001 (human authorship for claims; no AI commits); instrument not data; honest-broker; interest expressed never acquired.",
  "updated": "YYYY-MM-DD"
}
```

## 3 · The rule, from now on

- **When you create a folder that matters, add an `AI_ASSIST.json`.** Keep it small: the topic, its key files/results (tiered), neighbours, and the standard `join_the_chain`.
- **Nodes link up; the centre does not have to track down.** The control system's source‑of‑truth order is unchanged (`HS_FAST_REFRESH.json` → `HS_ADMIN.json` → narrative). The centre registers only the *convention* (this doc) and a one‑line pointer in `AI_RAPID_LEARN.md §7`; it does not enumerate every node.
- **The centre stays small; the edge stays current.** Update the node when its topic changes — the knowledge lives where the work lives.
- **It is the distributed form of `AI_RAPID_LEARN.md`.** That document is the central map; `AI_ASSIST.json` files are its leaves, placed where they are needed.

## 4 · Why this helps (the rationale, honestly tiered)

- **Tier 2 (sound):** distributing topic knowledge to the folder that owns it, with an up‑link, lowers the cost of onboarding (an agent reads a node, not the corpus) and lowers central‑refresh churn (most updates are local). The single source of truth is preserved because every node points to it and never the reverse.
- **Tier 3 (to earn):** any quantitative claim about how much admin/refresh effort this saves — measured as nodes accrue, not asserted.

## 5 · Live nodes (seeded across the folders that matter, 2026‑06‑11)
- [`../AI_ASSIST.json`](../AI_ASSIST.json) — **repo root / master node** (start here).
- [`../HCI-CNTT/AI_ASSIST.json`](../HCI-CNTT/AI_ASSIST.json) — the current engine (CN‑TT v4).
- [`AI_ASSIST.json`](AI_ASSIST.json) — **the control hub** (this `ai-refresh/` folder; the centre nodes link up to).
- [`../collaborations/codawork-2026/AI_ASSIST.json`](../collaborations/codawork-2026/AI_ASSIST.json) — the CoDaWork‑2026 collaboration set + Letter of Intent.
- [`../collaborations/microbiome/AI_ASSIST.json`](../collaborations/microbiome/AI_ASSIST.json) — Hˢ‑microbiome (coda4microbiome).
- [`../collaborations/geology-wehner/AI_ASSIST.json`](../collaborations/geology-wehner/AI_ASSIST.json) — geosensing → flight.
- [`../papers/AI_ASSIST.json`](../papers/AI_ASSIST.json) — the publication suite.
- [`../experiments/AI_ASSIST.json`](../experiments/AI_ASSIST.json) — the reproducible evidence base.
- [`../industrial-instruments/AI_ASSIST.json`](../industrial-instruments/AI_ASSIST.json) — Hˢ industrial instruments (MC‑4).
- [`../industrial-instruments/gas-composition-study/AI_ASSIST.json`](../industrial-instruments/gas-composition-study/AI_ASSIST.json) — public gas study (self‑serve / BYOAI entry).
- `../../HUF/huf-gov/AI_ASSIST.json` — **HUF repo**: governance, carrier‑filter, Ratio Blindness / MC‑4 (adopts this convention; links to HUF's own chain).

*(This list is a convenience, not the registry — nodes are discovered by being in their folders. As new folders that matter are created, they get a node. All 11 seed nodes validate as JSON.)*

*The centre stays small; the knowledge sits where the work is; every node links home. The instrument reads. The expert decides.*
