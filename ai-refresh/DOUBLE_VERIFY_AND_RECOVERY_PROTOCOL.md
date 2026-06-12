# Double‑Verify & Staged‑Recovery Protocol — DVR‑1.0

*Codified 2026‑06‑11. The named, documented form of the operating discipline this project has run on since the beginning: **lose nothing · check everything · verify before and after · move slowly in reversible stages · recover from any mistake.** This consolidates discipline that was previously scattered across `AI_AGENTS.md §2.1`, `PUSH_PROTOCOL.md §2.5/§6`, `OPERATIONS_PROTOCOL.md`, and `CHANGE_CONTROL_README.md`, and adds the failure modes now understood from live experience. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001.*

> **Lineage — credit where due.** The check‑everything, lose‑nothing system was built over many sessions by the **HUF AI Collective caretakers — ChatGPT, Grok, and Claude — under Peter's direction.** They did the job well: the reason this framework can be restructured, archived, re‑pasted, and pushed without losing anything is that those caretakers made *not losing* the default. DVR‑1.0 names what they built and extends it with the lessons that are now understood, so the next caretaker inherits the discipline explicitly rather than by osmosis.

---

## 1 · The four pillars

1. **Lose nothing.** Nothing is ever deleted in place — superseded material is **moved to a dated, reversible archive** (`_archive_YYYY-MM-DD/`, `_legacy_*`), with a manifest. A mistake can always be undone by moving a file back. *Archive, never delete.*
2. **Double‑verify — before *and* after.** Every change has a **pre‑condition check** (does the ground truth match what I think, before I act?) and a **post‑condition check** (did the action land exactly as intended, after?). One check is a guess; two checks are control. This is the heart of the system.
3. **Slow, in reversible stages.** Work advances in small stages, each independently verifiable and independently reversible, with a **human gate** between substantive stages (Peter is the sole commit/contact gate). No large irreversible leaps.
4. **Recovery at every stage.** Because nothing is deleted and every stage is double‑checked, **any mistake — AI or human — is caught at the next gate and rolled back.** Recovery is the design, not the exception.

---

## 2 · The double‑verify gate (apply to every change)

| | Pre‑condition (before) | Action | Post‑condition (after) |
|---|---|---|---|
| **File edit** | Read the authoritative current content first | Edit / Write | Read the result back (authoritative) and confirm it landed; never trust a single bash read of a just‑edited file |
| **Archive move** | Confirm the move list + that nothing current is in it | Move (never delete) | Count source + destination; write a manifest; confirm reversibility |
| **Engine change** | Capture the baseline hash/result | Patch | Re‑run self‑test + confirm clean‑data hash unchanged (hash‑neutral where intended) |
| **Push** | Pre‑push verification (`PUSH_PROTOCOL §2`): consistency checker, NO‑CREATE absent, frozen oracle untouched, JSON parse, self‑test | Commit + push | Post‑push closure check (`§6`): live SHA == recorded SHA; CI green; admin chain rolled |
| **Repo structure change** | List what the verification config (CI, checkers) references | Restructure | Update the verification config to track the *current* files; re‑verify |

*The rule in one line:* **read the truth before you write it; read it back after; and have a way back.**

---

## 3 · Known failure modes — now understood, with recovery

These are real failures observed in live operation. Each is now named so it is caught, not rediscovered.

### 3.1 Buffered / stale‑mount reads (the "buffered‑read AI")
The sandbox file mount can serve a **stale, truncated, or NUL‑padded copy** of a file that was just written through the authoritative Read/Write tools — so a bash `cat`/`json.load`/`python` of a just‑edited file can falsely report it broken (`Unterminated string`, `binary file matches`, a stale byte‑count, or even the *old* code's line numbers in a traceback).
- **Authority order:** the **Read/Write/Edit tools are authoritative** (Windows‑side); **bash reads can lag**. On any disagreement, the tool wins.
- **Recovery:** verify a just‑edited file via the authoritative Read tool, not bash. To *run* just‑edited code, reconstruct it into a pure‑local `/tmp` copy from authoritative content and run there. Big admin JSONs (`HS_FAST_REFRESH.json`, `HS_ADMIN.json`) truncate around a fixed offset — validate them Windows‑side, never blind‑edit them from the sandbox. *(Prior art: `AI_AGENTS.md §2.1`, `PUSH_PROTOCOL §2.5`.)*

### 3.2 Stale pipelines / verification coupled to moved files
When structure changes (e.g., archiving the old `tools/pipeline`), any **verification config hard‑wired to the old paths fails** — the CI `validate.yml` checked for (and ran) files that had been correctly archived, so it went red on a healthy repo.
- **Recovery:** treat the verification config as part of the structure. When you move/rename, **update the checker's file list in the same change** (pre‑condition pillar #2: "list what the config references"). A red CI here is the system working — it caught the drift loudly.

### 3.3 Unseen‑commit fabrication
Narrating a commit you have not seen (to "complete" an admin entry) silently corrupts the audit trail.
- **Recovery:** **never fabricate.** Use placeholders, flag the blocker, and reconcile at the human gate. *(This is the honest‑broker rule applied to bookkeeping.)*

### 3.4 Mis‑numbering / drift in the admin chain
Push numbers and CI runs can desync (e.g., `last_updated` ahead of `last_push`), and an empty‑and‑repaste cycle can skip chain entries.
- **Recovery:** the post‑push closure check (`§6`) reconciles the chain at the gate; draft control rows number‑agnostically until the number is confirmed.

### 3.5 Ordinary AI / human mistakes
Anyone — AI or person — can make a wrong call.
- **Recovery:** the before/after double‑check catches it at the next gate, and reversibility (pillar #1) undoes it. *No single actor is trusted to be right once; the system is trusted to catch it twice.*

---

## 4 · Why it works (the design claim, Tier 2)

The framework's scientific core is **determinism + hash receipts**: same input → same output → same `cntt_content_sha256`. DVR‑1.0 applies the *same epistemology to the operations layer* — every state has a checkable receipt, before and after, and a reversible path back. That is why the system can absorb a buffered read, a stale pipeline, a mis‑numbered push, or a plain mistake **without losing anything**: each is a caught, recoverable event rather than a silent loss. The discipline is the product as much as the engine is.

---

## 5 · Where this is registered (so it stays known)

- **Machine‑readable:** `ai-refresh/VERIFICATION_PROTOCOL.json` (first‑class admin JSON).
- **AI control hub:** registered in `ai-refresh/AI_ASSIST.json` (`key_files` + `join_the_chain.operating_discipline`) — so every bring‑your‑own‑AI that climbs the chain reads it.
- **Operations front door:** `ai-refresh/OPERATIONS_INDEX_2026-06-11.md` §Govern.
- **To fold in at the gate (Windows‑side):** a pointer in `HS_FAST_REFRESH.json` `_meta` + an `HS_ADMIN.json` note (the big JSONs are edited Windows‑side per §3.1; `HS_MACHINE_MANIFEST.json` is a legacy snapshot and is *not* used as the registration home).
- **Prior art it consolidates:** `AI_AGENTS.md §2.1`, `PUSH_PROTOCOL.md §2.5` + `§6`, `OPERATIONS_PROTOCOL.md`, `CHANGE_CONTROL_README.md`, and `HS_MACHINE_MANIFEST.json fault_tolerance_dual_folder_method`.

*Lose nothing. Check everything. Verify before and after. Move slowly, in stages. Recover from anything. — built by the caretakers; named here so it is never lost either.*
