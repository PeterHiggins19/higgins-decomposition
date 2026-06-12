# Restructure Journal — 2026‑06‑11 (Fable session)

*A single record of the mirror restructure done this session: house‑cleaning, the workplace front door, the huf‑gov trim + doctrine modernization, NASA‑style governance, and the enhanced distributed AI‑assist nodes. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001 (Claude Fable 5). Navigation/cohesion + governance‑doctrine layer — **not** an advancement of the science; engine code, schemas (HUF‑STD‑001/002/003), the INV catalog, and the frozen oracle are **untouched**. On any conflict, `Hs/HS_FAST_REFRESH.json` wins. Peter is the sole commit/contact gate; nothing sent.*

---

## 0 · Your GitHub‑Desktop question (recorded for the paste workflow)

**GitHub Desktop locates a repo by exactly one thing: the `.git/` directory at the path it registered.** So the only ways to trigger "where is the Hs repo?" are to **delete `.git/`** or to **delete/rename the repo's root folder itself**.

- The mirror's `Current-Repo/Hs` has **no `.git`** (only `.github/` + `.gitignore`); the live Hs git repo is in your separate GitHub‑Desktop "originals" folder. The mirror can never trigger the error.
- **Safe clear‑and‑paste method (in the watched/originals folder):** clear the folder's *contents* but **keep `.git/`**, then paste the new files in. Never "delete the folder and recreate it" — that destroys `.git`.
- **Always preserve:** `.git/` (critical — it *is* the repo), `.github/` (CI, e.g. the "Validate Repository" workflow), `.gitignore`, `.gitattributes`, `LICENSE`/`NOTICE`. Everything else can be overwritten; git reads it as changes.

---

## 1 · House‑cleaning (executed, reversible)

Moved **280 items** (276 old EITT/HUF‑era root docs + the historical folders `Chatgpt/`, `Quaternion Decomposition/`, `regimes/`, `code/`) from the mirror root into `_archive_2026-06-11/` (manifest: `_archive_2026-06-11/ARCHIVE_MANIFEST_2026-06-11.json`). Mirror root went **312 → 36** loose files. Kept current/reference/navigation at root; **wine P1, Personal‑Contacts, and Studies untouched**. Driven by the document‑level `DOCUMENT_LEDGER_2026-06-11.json` + `RELEVANCE_MAP_2026-06-11.md`. Bulk buckets (`EITT/`, `DATA/`, `node_modules/`, `_archive_2026-06-07/`, `remote_data_in/`) not touched.

## 2 · The workplace front door (new)

`Hs-Workplace/` — a self‑contained, offline **UN‑6 interactive walk‑in** (`index.html`) for the two guests **Matthew (geology)** and **microbiome (bio)**; the wine carrier (P1) is held for in‑person delivery and is **not** featured or archived. Two furnished rooms with real diagnostic "receipts" (Frielingen‑9: helmsman Zr, 19 regime steps, lossless 3.3e‑16; microbiome: Crohn 975 samples lossless 1.8e‑14, ECAM infant K_eff 5.7→11.8 ρ=0.71, honest Crohn‑vs‑control null p=0.78, scales to D=10⁶), an instrument toy computing **real** K_eff + helmsman on an illustrative path, and the "the instrument reads, the expert decides" close. Machine companion: `Hs-Workplace/WORKPLACE_INDEX.json`. Formula: impress the mind, busy the body (the CoDaWork register).

## 3 · huf‑gov trim + shift‑the‑good (`Current-Repo/HUF/huf-gov/`)

The old/new mix is resolved with no loss:
- **Archived** the March‑2026 set (governance/ science/ evidence/ tools/, **53 files** incl. LOOP‑001, SAFE‑001, KILL‑001, MONITOR‑001, GOV‑003, HAGF‑001, TRANS‑001, ontological‑foundation) into `HUF/huf-gov/_legacy_2026-03/` — preserved **verbatim**, reversible.
- **June canon kept at top:** `HUF_GOVERNANCE_CHARTER.md`, `CARRIER_FILTER_DOCTRINE.md`, `RATIO_BLINDNESS_DOCTRINE.md`, `AI_ASSIST.json`.
- **Modernized the good doctrines** into a new current set `HUF/huf-gov/doctrine/`:
  - `HUF_GOV_OPERATING_DOCTRINE_2026-06.md` (v2.0) — carries **Open‑Loop/Skydiver, Safe‑Operations, Kill‑Test, Composition‑Monitoring (MC‑4)** forward, CN‑TT v4‑aligned, claim‑tiered, NASA cross‑walked. Supersedes the March originals (which it points to).
  - `DOCTRINE_INDEX.json` — machine index of the four doctrines + their CN‑TT bindings + NASA mappings.

## 4 · NASA‑style governance (new)

`HUF/huf-gov/NASA_STYLE_GOVERNANCE.md` + `.json` — maps **what Hs already does** to NASA principles, honestly tiered:
- lifecycle + Key Decision Points → HGS‑000…008 + CCTT 2 gates + CI gate (T2);
- Technical Authority → Peter (programmatic) / frozen oracle (engineering) / honest‑broker (mission assurance) (T2);
- IV&V → frozen‑oracle parity + self‑test + AI‑collective + cross‑platform challenge (T1/T2);
- FDIR → internal/external shock classifier + E‑21 carrier guard (T1);
- Configuration Management → hash chain + frozen oracle + push chain (T1);
- fail‑safe → Safe‑Ops hold‑and‑report + `DX‑NUL‑DIS` (T1/T2);
- human authority → Open‑Loop doctrine (T2);
- V&V limits → Kill‑Test (T1/T2);
- observability → MC‑4 (T2);
- flight readiness / Earth‑space twin → `SPACE_READINESS_AND_CHALLENGE.md` (**T3, aspiration**).
Honest line included: *Hs is not NASA‑certified; this adopts NASA‑style methods as a discipline.*

## 5 · Distributed AI‑assist onboarding nodes (enhanced)

New schema **`hs_ai_assist/1.1`** adds a shared `byo_ai_onboarding` block — *learn compositional analysis with Hs as a deterministic **extension to standard CoDa**, using standard CoDa tools (CLR/ILR/Aitchison) in machine applications, determinism binding by doctrine and practice.* **18 new nodes** added across the major domain folders (CODA‑Association, HCI‑CNQ/CNT/AUDIO/ULTRASOUND, huf‑gov, huf‑gov/standards, collaborations, docs, applications, scripts, tools, constants, Higgins_Coordinate_System, Hs_Direct, hci_shared, plus `Hs-Workplace/` and `HUF/huf-gov/doctrine/`). With the 12 existing 1.0 nodes, **30 nodes** now cover the repo for bring‑your‑own‑AI fast onboarding. All validated as valid JSON.

## 6 · Admin

Machine record for the §6 admin chain: `ai-refresh/ADMIN_DELTA_2026-06-11_restructure.json` (a delta — the giant `HS_ADMIN.json`/`HS_FAST_REFRESH.json` are **not** edited from the mount, which serves truncated copies; fold the delta in on your machine at your gate). Earlier this session: the **E‑21 carrier guard** patch (`ai-refresh/E21_PATCH_READY_2026-06-11.md`) remains drafted, verified, and **uncommitted** awaiting your gate.

---

## 7 · Public‑good folder of pursuit imported (new)

New top‑level `Hs/stewardship/` — the **stewardship track, deliberately separate from the commercial `industrial-instruments/` line.** Imports the *basics* of two purposes from Peter's own source docs: **ISO** (positioning MC‑4 / Composition Monitoring as the missing 4th monitoring category — MC‑1/2/3 are standardised under ISO/TC 69; composition has no ISO home; a **proposal**, not a standard) and **Ramsar** (Convention on Wetlands, 172 Parties, ~2,500 sites; a two‑tier offer — governance + field‑work — across five wetland CoDa series; the honest complexity gap named). Files: `README.md`, `COMMITMENT_OF_PURPOSE.md` (the charter — *offered, not sold; the expert decides; interest expressed, never acquired*), `iso-standards/README.md`, `ramsar-wetlands/README.md`, `AI_ASSIST.json` (1.1). Distilled (not copied) from `papers/in_progress/WETLAND_COMPOSITIONAL_ANALYSIS_RAMSAR.md`, `HUF/archive/post-coimbra-planning/RAMSAR_COMPLEXITY_GAP.md`, `HUF/science/wetlands/HUF_Human_AI_Accord_Ramsar_v1.0.json`, and `HUF/science/coda-monitoring/MC4_ISO_Positioning_Document.docx`. The Human‑AI Accord's more philosophical framing is cited as a source, not amplified; the charter keeps the grounded core. All Tier‑3 engagement; nothing initiated or sent.

## Lockdown compliance

S2 doc/governance only. Engine code (`cnt.py`/`cnq.py`/CN‑TT v4), schemas (HUF‑STD‑001/002/003), the INV catalog, and the frozen oracle are **untouched**. All moves are reversible (nothing deleted). All outreach remains DRAFT/unsent. AI‑assisted per HUF‑STD‑001; human authorship; Peter sole commit authority.

*The instrument reads. The expert decides. The hashes carry the receipts. The loop stays open.*
