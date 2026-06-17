# For a visiting expert — and the AI they bring

*The fastest honest path for an invited guest to "see the work done," and for any AI assistant they bring to get oriented and help them. Three tracks, because the three kinds of guest read differently — a longitudinal‑microbiome researcher, a geoscientist, and a frontier mathematician. Role‑based by design (named outreach is kept off‑repo per carrier‑filter governance; the non‑contact / ghost‑tool doctrine governs all of it — `papers/in_progress/AUDIENCES_AT_THE_FRONTIER.md` §4). Author: Peter Higgins (human authorship); AI‑assisted per HUF‑STD‑001. Read‑only; honest‑broker; nothing here asks for anything — it shows the work.*

---

## If you bring an AI assistant — point it here first

Any AI a guest brings can self‑orient in four reads and then help its human:

1. **`AI_WELCOME.md`** (repo root) — the spirit of the place, the lineage, the house rules.
2. **`AI_ASSIST.json`** (repo root) — the machine‑readable map to every topic node.
3. **`HCI-CNTT/ENGINE_CAPABILITIES_DELTA_2026-06.md`** — what the engine can do *now* (so the AI describes the current instrument, not last month's).
4. **`onramp/PHD_ONRAMP_PROTOCOL.md`** — how to turn the guest's own data into an Hˢ reading without making them learn CoDa first; the `static_only_path` if they just want a ternary/biplot.

Then the AI can run the guest's data, or walk them through the track below. Governance applies: read‑only context, claim tiers, instrument‑not‑data, Peter is the sole gate.

## Track 1 — the microbiome / longitudinal‑omics researcher

For a guest working with abundance tables over time (gut/lung microbiome, antibiotic or disease cohorts), the hook is **two real runs that show both faces — the honest null and the real signal**:

- **The worked runs:** Crohn (D=48 OTUs, 975 samples) → lossless, and an **honest global null** (K_eff 7.31 vs 7.23, p=0.78) auto‑flagged as `DX‑NUL‑DIS` — *the signal is taxon‑specific, not global, and the engine says so*; ECAM infant gut → **maturation recovered from composition alone** (K_eff vs age, ρ=0.71, p=2.5e‑6). Read: `collaborations/microbiome/results/RESULTS_real_microbiome.md`.
- **It scales:** lossless tree‑atlas reconstruction to **D=10,000 at ~7 ms/sample** — your metagenomic table runs (`RESULTS_microbiome_sniff.md`).
- **The honest sparsity boundary:** at ~90% zeros the CLR geometry is replacement‑dominated — the engine raises **`GD‑SPZ‑WRN`** and tells you to densify (prevalence filter / agglomerate / Bayesian‑multiplicative) before the log‑ratio, while the zero‑robust reads (K_eff, the deceptive‑drift null) still hold (`experiments/sparsity_microbiome_2026-06/`). The K_eff = Shannon‑effnum equivalence ties it to `coda4microbiome`.
- **Why a microbiome PhD cares:** it tells you *where the signal is not* as readily as where it is, runs at metagenomic scale, and is honest about sparsity — complementing differential‑abundance methods, not competing with them.

## Track 2 — the geoscience collaborator

For a working geologist, the hook is a **real, reproducible run on published data**:

- **The worked demo:** 219 Lower‑Cretaceous mudstone samples (PANGAEA), lossless, **trace elements Zr/Rb driving over the bulk oxides**, 19 datable regime tripwires, a blind CaCO₃ calibration hit. Open the offline dashboard, point at a depth, read the helmsman — no CoDa vocabulary required. Read: `collaborations/geology-wehner/demo_frielingen9/RESULTS_Frielingen9_CNT_CNQ.md` + `REPRODUCE.md` + `frielingen9_projector.html`; honesty assessment: `MUDSTONE_HS_FIT.md`.
- **The standard‑CoDa comfort:** if dynamics aren't the question, Stage‑2 gives the **ternary / CLR biplot / variation matrix** and stops there (`onramp/PHD_ONRAMP_PROTOCOL.md` → "If you only want the static picture"). The static‑only researcher is served and left alone.
- **What's new to see:** sparsity awareness, the self‑calibrating hold‑lock, and the announced degenerate‑carrier guard — so a real XRF dataset with zeros and quiet stretches is read honestly. (Routes to incomplete‑XRF imputation work the collaborator already does.)

## Track 3 — the frontier‑mathematics visitor

For a guest who thinks in low‑dimensional topology and gauge theory, the offer is narrow, exact, and **honestly scoped — a side instrument, not a primary tool** (`AUDIENCES_AT_THE_FRONTIER.md` §2):

- **The exact structure (Tier 1):** a four‑part composition's three ILR coordinates identify with a unit quaternion on **S³ = SU(2)**; an Aitchison rotation *is* the sandwich product `q v q*`, confirmed to the **IEEE floor (4.441e‑16 = 2× machine epsilon)** bit‑identically on two unrelated D=4 datasets (Backblaze, Planck CMB). Read: `papers/in_progress/PAPER_1_UNIVERSAL_INVARIANCE_DRAFT.md`, `_archive_2026-06-11/Quaternion Decomposition/QD_CENTRAL_CLAIM.md`.
- **What it offers her:** an **inert, deterministic generator of examples** in the category she studies — a machine that turns real compositional data into exact, reproducible, hash‑certified objects in the S³/SU(2) and PL→DIFF setting, surfacing adjacencies one wouldn't construct by hand. The four hooks (gauge‑theoretic structure; explicit PL→DIFF refinement; native dimension‑4; inert data‑driven generation) are in `AUDIENCES_AT_THE_FRONTIER.md` §2.1, with companion notes `GAUGE_THEORY_AND_Hs.md`, `MANIFOLD_CATEGORY_OF_Hs_PROJECTION.md`.
- **What it honestly will NOT do (§2.2):** no Alexander/Khovanov/Heegaard‑Floer, no Kirby calculus, no slice obstructions, no theorems about specific manifolds. The 4‑manifold toolbox proper is outside it. The gauge/topology connections are **Tier‑3 conjecture — questions *for* her judgment, not claims *to* her.**
- **Posture:** offer, do not ask; one light artifact load; no follow‑up; her refutation strengthens the work. A ghost tool advertises itself by being available, not conspicuous.

## What every guest should leave with

That this is **an extension of standard CoDa into dynamics** (geometry is CoDa's; the motion is the extension — `CODA-Association/HS_AS_AN_EXTENSION_OF_CODA.md`), built as a **deterministic, gauge‑R&R‑clean instrument** that now also **says honestly when it cannot resolve** — and that the door is open, read‑only, with the work on the table to examine. *The instrument reads. The expert decides. Nothing is asked; the work is shown.*
