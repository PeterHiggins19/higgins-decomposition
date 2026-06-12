# Abstract-to-CNT-v3 mapping — bringing the past forward

**Companion to:** `CONFERENCE_2026_06_PLAN.md` (master plan)
**Created:** 2026-05-10 (push #36 + uploaded original-abstract verification)
**Status:** active reference — every talk slide must trace back to a row in §3 of this document

---

## 1. The two source documents (both are the original)

The "original submission" was actually a **two-piece package**: an abstract for the book of abstracts (CoDa-canonical vocabulary) plus an 11-page methods packet (operational vocabulary). Both are the same submission; the abstract is the published face, the packet is the methodological depth. Both must be honored.

### 1.1 The published abstract (book of abstracts page 25)

Verified verbatim from the upload `Compositional monitoring of energy-mix drift on the simplex.txt` against `External_Published_Papers/book-of-abstracts-codawork-2026-draft.pdf` page 25. Identical word for word.

| Field | Value |
|---|---|
| Title | **Compositional monitoring of energy-mix drift on the simplex** |
| Author | Peter Higgins, Independent researcher, Markham, Ontario, Canada |
| Keywords | compositional time series, perturbation, drift detection, energy mix |
| Countries | **Germany, Japan, United Kingdom** |
| Period | **2000–2025** |
| Carriers | 9 fuel types → composition on the 8-simplex |
| Headline operators | **perturbation** (compositional ratio between consecutive observations); **Aitchison distance** (period-to-period magnitude); **concentration measure related to effective diversity** |
| Three named transitions | Japan post-Fukushima 2011–2012 perturbation spike; Germany continuous trajectory toward renewable vertex; UK coal exit as abrupt regime change in the Aitchison distance matrix |
| Open question | Relationship between concentration measure and Aitchison norm |
| Falsifiability | "Four specific ways it could be defeated" (the four defeat paths from the packet) |
| Repository named in submission | **github.com/PeterHiggins19/Higgins-Unity-Framework** (HUF — not the current Hs repo) |

### 1.2 The HUF MC-4 Packet v3 (11-page attachment)

| Section | Content |
|---|---|
| Part I — CoDa Primer | States the MC-4 claim in CoDa terms; HUF as a monitoring **application** of standard CoDa, not new mathematics |
| Part II — MC-4 Methods Challenge | The narrowest version of the claim + the 4 defeat paths (prior-art / metric / case / category) |
| Part III — EMBER Case Note | The lead public demonstration (Germany pre-2022 gas crisis) + 5 countries (DE, JP, GB, **FR**, **AU**) + 9 fuel types + 2000–2025 + monthly deseasonalised |
| Appendix A — Metric Correction | The L2 → TV distance correction (caught March 22, 2026 in ChatGPT corpus review) — both metrics now computed side-by-side |

**Key vocabulary the packet defines** (and which the talk should use):

- **MC-4** — the formal name of the central claim ("no prior monitoring framework tracks compositional market share at the carrier level with formal change detection")
- **Deceptive drift** — internal redistribution or compositional concentration emerging within an apparently stable whole; the headline pattern the framework detects
- **TV distance** — Total Variation, ½ Σ|ρᵢ(t) − ρᵢ(t−1)|, the half-L1 norm; bounded [0, 1]
- **K_eff** — effective number of categories, exp(H(t)) where H is Shannon entropy on the closed composition; equal distribution → K_eff = D, single-carrier dominance → K_eff → 1
- **Carrier proportions** ρᵢ(t) = xᵢ(t) / Σⱼ xⱼ(t)
- **Derived observables** — d(TV)/dt and per-carrier attribution
- **Stable total, shifting mix** — the operational signature of deceptive drift

**Key empirical claim** (from the packet):

- Germany, monthly deseasonalised EMBER, pre-2022 gas crisis, **p = 0.0016** under the deceptive-drift detection protocol (6-month sliding window, K_eff YoY change < −0.05, structural velocity below series median, within 12 months of a known structural shock)
- **Caveat the packet itself flags:** the null distribution is the empirical frequency under the series' own distributional baseline, not a Dirichlet / permutation / bootstrap formal null. A CoDa reviewer should press on this.

---

## 2. The framework lineage — where the original lives now

The submission was sent from the HUF repository. The framework has since matured into Hs / CNT v3 / CNQ v2 in this repository. The lineage is well-documented in `EXPERIMENTS_JOURNAL.md` and `HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`:

```
DADC (BTL/Rogue Wave Audio)
   ↓
H₁ (Higgins Operator, nonlinear unity-normalisation on Hilbert space)
   ↓
HUF (Higgins Unity Framework — MC-4 + EITT + the original CoDaWork submission)   ← THE ABSTRACT IS HERE
   ↓
Hˢ (Higgins Decomposition, this repo: deterministic 12-step → CNT canonical engine)
   ↓
CNT v3.0.0 (push #32, 2026-05-09, ground-up rebuild)   ← THE TALK IS HERE
   ↓
CNQ v2.0.0 (quaternion view; depth/Q&A material only)
```

**Implications for the talk:**

- The audience that read the abstract sees a HUF link in the submission letter. We should not pretend the framework is named otherwise.
- The matured engine (CNT v3) does everything HUF did **plus** strictly more, with documented determinism + hash chains + four binding doctrines.
- The talk can present the lineage transparently: "the submitted MC-4 packet was built on the HUF prototype; the production engine that runs the analysis today is CNT v3.0.0 in the Hs repository, which preserves every HUF operator and adds determinism."
- The repository pointer in slides should give both: HUF (where the submission was sent from) and Hs (where the production work lives now).

---

## 3. Operator-by-operator mapping — abstract / packet → CNT v3 output

Every quantity the **abstract** or **packet** names has a counterpart in CNT v3.0.0's JSON output. This table is the binding reference for talk material: every figure / number / claim must trace back to one row.

| Abstract / packet term | What it is | CNT v3 output field | Notes |
|---|---|---|---|
| ρᵢ(t) — carrier proportions | Closed composition at time t | `tensor.timesteps[t].coda_standard.composition` | Output of the closure operator (S in Hˢ = R∘M∘E∘C∘T∘V∘S) |
| Perturbation ρ(t) ⊖ ρ(t−1) | Compositional ratio between consecutive observations | Computable from `composition[t] / composition[t-1]` then re-normalised | Not currently a top-level field; can add to runner output |
| Aitchison distance period-to-period | Magnitude of compositional movement | `tensor.timesteps[t].coda_standard.aitchison_distance_step` | **Direct match** — the abstract's headline metric |
| Aitchison norm of the composition | Distance from the simplex barycenter | `tensor.timesteps[t].coda_standard.aitchison_norm` | The metric the open question is about |
| TV distance (packet) | ½ Σ|ρᵢ(t) − ρᵢ(t−1)| | **Not currently in CNT v3 output** — add as a derived field for the talk; agrees with Aitchison distance on shock hit/miss verdicts per the metric-correction note |
| K_eff (packet) — effective number of categories | exp(Shannon entropy) on closed composition | Computable as `exp(coda_standard.shannon_entropy)` per timestep | Currently only Shannon entropy is exposed; adding K_eff = exp(H) is one line |
| Shannon entropy / "concentration measure related to effective diversity" | Diversity readout per timestep | `tensor.timesteps[t].coda_standard.shannon_entropy` | The concentration measure the abstract names |
| d(TV)/dt — acceleration (packet) | Rate-of-change of TV | Computable from step-Δ Aitchison distance differences | Useful for inflection-point detection |
| Per-carrier attribution (packet) | Which carrier drove the change | `helmsman_family.flips` + `helmsman_family.dominant_axis_per_step` | The helmsman family was added at push #24 specifically for carrier attribution |
| "Stable total, shifting mix" diagnostic | Total stays calm while composition rotates | Total = `input.row_sums[t]`; composition = `tensor.timesteps[t].coda_standard.composition`; flag when `var(row_sums)` is small AND `aitchison_distance_step` is large | Compose at runner level; not a single field |
| Japan post-Fukushima 2011–2012 spike | Large perturbation in JPN compositional time series | Read JPN's `coda_standard.aitchison_distance_step` at indices for years 2011 and 2012 | **Verification task 5.3.C in master plan** |
| Germany continuous trajectory toward renewable vertex | Smooth drift toward renewable corner of simplex | DEU IR class `OVERDAMPED_EXTREME` (snap-to-attractor) + helmsman flips=13; trajectory is monotone | Already in `papers/codawork2026/conference_2026_06/per_country/ember_deu/` |
| UK coal exit as abrupt regime change | Step-change in step-Δ Aitchison distance pattern | GBR IR class `OVERDAMPED_EXTREME` + helmsman flips=15; step-Δ shows the regime change | Already in `papers/codawork2026/conference_2026_06/per_country/ember_gbr/` |
| MC-4 claim — "no prior monitoring framework tracks compositional market share at the carrier level" | Falsifiable central claim | Whole framework; documented in `EXPERIMENTS_JOURNAL.md` + `HCI-CNT/handbook/VOLUME_*` | The slide deck should state MC-4 explicitly |

### 3.1 What needs adding to the runner output

For full alignment with the packet's vocabulary, three quantities should be added to the conference runner's per-country JSON (does not require engine changes — wraps existing CNT v3 output):

1. **TV distance** — ½ Σ|ρᵢ(t) − ρᵢ(t−1)| per timestep. Independent calculation alongside `aitchison_distance_step`. ~10 lines in `run_ember_corpus.py`.
2. **K_eff** — exp(`shannon_entropy`) per timestep. One-line derivation.
3. **Deceptive-drift detection result** — apply the packet's protocol (6-month sliding window where K_eff YoY change < −0.05 AND structural velocity < series median) to the Germany series. Should reproduce the p = 0.0016 result OR explicitly document that the v3 engine + monthly EMBER 2025 data give a different number. Either way is honest.

---

## 4. The four defeat paths (the falsifiability conditions)

The published abstract says: *"This claim is presented as falsifiable: the contribution identifies four specific ways it could be defeated."* Those four ways are documented in **Part II of the HUF MC-4 packet, page 5–6**:

| # | Defeat path | What it would show | Talk treatment |
|---|---|---|---|
| 1 | **Prior-art defeat** | Existing CoDa work already frames compositional structure as a primary operational monitoring category; MC-4 would not be novel | Acknowledge Aitchison (1982/1986), Egozcue, Pawlowsky-Glahn lineage; ask the room for prior-art pointers |
| 2 | **Metric defeat** | The current observable stack adds no information beyond ordinary CoDa summary; or chosen metrics are poorly posed | Show TV distance + Aitchison distance side-by-side per the Appendix A correction; both agree on shock verdicts; demonstrate metric robustness |
| 3 | **Case defeat** | The EMBER result is an artefact of carrier definition, preprocessing, or null-model setup | Document carrier definitions, preprocessing (deseasonalisation), null-model caveat in plain view; invite reviewer pressure |
| 4 | **Category defeat** | Composition monitoring is at most a useful application note inside existing CoDa, not a distinct monitoring category | Accept this as a possible outcome; note that even category defeat would leave the energy case methodologically sound |

The talk should name MC-4 explicitly, list the four defeat paths on a slide, and invite the room to defeat the claim. This is the "this is the right room to kill it" framing from the packet's bottom line.

---

## 5. Country scope — abstract / packet / current corpus / Peter's expansion

| Source | Countries | Count |
|---|---|---|
| Published abstract (book of abstracts page 25) | Germany, Japan, United Kingdom | **3** |
| HUF MC-4 packet (the methods attachment) | Germany, Japan, UK, France, Australia | **5** |
| Current `papers/codawork2026/conference_2026_06/` | USA, CHN, DEU, FRA, GBR, IND, JPN, WLD | **8** |
| Full OWID Phase 2 expansion | 73 country trajectories (1965–2024 typical) | **73** |
| **Peter's directive (2026-05-10):** acceptable to expand to all countries | All EMBER + all OWID | **up to ~80 country-level compositions** |

**Updated recommendation:** the talk can comfortably stage every country we have. The abstract's three (DEU/JPN/GBR) are **the headline narrative** — those are what the audience read about and the three named transitions live there. Beyond the headline, every additional country becomes scaling evidence. The natural structure is now:

- **Headline (in the slides):** DEU, JPN, GBR — the three named transitions; one slide per country
- **Methods extension (still in slides, briefer):** FRA, AUS, USA, CHN, IND, WLD — the rest of the EMBER 8 + Australia. Shows the protocol generalises across the G7 + emerging economies and at the world-aggregate level.
- **Scaling demonstration (one summary slide):** the 73-country OWID primary-energy expansion. IR-class distribution across 73 countries on one chart shows the protocol is not cherry-picked.
- **Q&A depth bench:** any country can be pulled up individually from the per-domain folders.

The abstract is still binding for the **headline narrative**; the packet's 5 countries become explicit when discussing the methods reach; the broader corpus becomes the scaling evidence. All three layers are now in scope.

**Australia (AUS) status:** still needs to be added to `data/Energy/EMBER_pipeline_ready/` and to the runner. **Task 5.3.K in the master plan stays HIGH priority** — without AUS the packet's 5-country set is incomplete. The OWID expansion already covers Australia (one of the 73 OWID countries).

---

## 6. Updated translation table — what the audience hears vs what we deliver

The audience reads the abstract. They expect what the abstract names. The packet expanded the vocabulary that the talk should use. CNT v3 is the engine that produces the numbers.

| What the audience expects (from abstract) | What we say on stage (with packet vocabulary) | What the engine actually computed (CNT v3) |
|---|---|---|
| "compositional drift detection" | "MC-4 — compositional change detection at the carrier level with formal perturbation-based drift measurement" | CNT v3 Stage 1 `coda_standard.aitchison_distance_step` + helmsman family carrier attribution |
| "perturbation" | "perturbation ρ(t) ⊖ ρ(t−1) in Aitchison terms; magnitude is Aitchison distance; the packet's TV distance gives the same hit/miss verdicts and is bounded [0,1] for visual presentation" | Aitchison distance (CNT v3 native) + TV distance (added at runner level) |
| "concentration measure" | "K_eff = exp(Shannon entropy on the closed composition); related to but distinct from the Aitchison norm — that relationship is the open question for the community" | `coda_standard.shannon_entropy` (and `exp(shannon_entropy)` for K_eff) |
| "Japan post-Fukushima spike" | Cite the year 2011–2012 entries in the JPN per-country STAGE_1_REPORT step-Δ column; show the full T=26 trajectory with the spike highlighted | Already in `per_country/ember_jpn/STAGE_1_REPORT.md` (verify spike visibility — task 5.3.C) |
| "Germany continuous trajectory" | Show DEU's IR classification + helmsman flips count + composition triangle animation toward renewable vertex | Already in `per_country/ember_deu/` |
| "UK abrupt regime change" | Show GBR's step-Δ Aitchison distance pattern with the coal-exit regime change highlighted | Already in `per_country/ember_gbr/` |
| "stable total, shifting mix" | Side-by-side: total generation TWh stable; carrier-share composition rotating | Compose total from `input.row_sums` + composition from `coda_standard.composition` |
| "deceptive drift" | The packet's signature concept; Germany pre-2022 result with the null-model caveat front-and-centre | New runner-level computation; verify p ≈ 0.0016 reproduces or document the difference honestly |
| "the four falsifiability conditions" | Slide listing the 4 defeat paths from the packet (prior-art / metric / case / category) | Methods slide; not a numerical result |
| "all data, code, documentation publicly available" | Point at both repos: the HUF submission origin (Higgins-Unity-Framework) and the production engine home (higgins-decomposition / Hs) | Both are public; CNT v3 has hash chains + 43-test suite |

---

## 7. Concrete additions to the planning bundle

Following from this mapping, the master plan §5.3 deliverable list adds:

| New item | What it is | Effort | Priority |
|---|---|---|---|
| **5.3.K** Add Australia (AUS) EMBER pipeline-ready CSV to `data/Energy/EMBER_pipeline_ready/` and to the conference runner | Bring the corpus to packet-aligned 5 countries | 0.5 day | **HIGH** |
| **5.3.L** Extend `run_ember_corpus.py` to compute TV distance and K_eff alongside Aitchison distance and Shannon entropy; emit both | Honor the packet's operator stack | 0.5 day | **HIGH** |
| **5.3.M** Verify the Germany pre-2022 deceptive-drift detection on CNT v3 + monthly EMBER 2025 data; reproduce p = 0.0016 OR document the difference | Honor the packet's headline empirical claim | 1 day | **HIGH** |
| **5.3.N** Slide for the four defeat paths (prior-art / metric / case / category) named explicitly | Honor MC-4 falsifiability | 0.5 day | **HIGH** |
| **5.3.O** Slide for the deceptive-drift definition + the 6-month sliding window protocol | The packet's signature concept | 0.5 day | **HIGH** |
| **5.3.P** Repository pointer slide that names BOTH HUF (submission origin) and Hs (production engine), with the lineage one-liner | Audience expects HUF link from the submission; we present the matured framework honestly | 0.25 day | **MEDIUM** |
| **5.3.Q** Methodological self-discipline slide — the L2 → TV correction (Appendix A of the packet) | Shows the framework caught its own metric error during ChatGPT review March 2026; this is a feature, not an embarrassment | 0.5 day | **MEDIUM** |

---

## 8. Reading order for any AI session resuming this work

1. `papers/codawork2026/planning/CONFERENCE_2026_06_PLAN.md` (the master plan)
2. **This document** (`ABSTRACT_TO_CNT_V3_MAP.md`) — the operator translation
3. `External_Published_Papers/book-of-abstracts-codawork-2026-draft.pdf` page 25
4. The HUF MC-4 packet v3 (PDF in the uploads or at `Current-Repo/HUF/archive/pre-codawork2026-drafts/HUF_MC4_CoDaWork_Packet_v3.pdf`)
5. `papers/codawork2026/CoDaWork2026_Reply_to_Egozcue_Final.txt` (correspondence record)
6. `papers/codawork2026/conference_2026_06/per_country/ember_deu/STAGE_1_REPORT.md` (the headline result on CNT v3)

Do not pivot away from the energy-mix drift focus. The agenda is set. The MC-4 framing, the four defeat paths, the deceptive-drift concept, and the Germany p = 0.0016 result are the **packet's contribution** to the abstract — they go in the talk's depth and Q&A bench.

---

*This document is the bridge between what was submitted (HUF MC-4 packet + CoDa-canonical abstract) and what we now deliver (CNT v3 + 8-country EMBER corpus + full reference suite). Refresh whenever a deliverable in master plan §5.3 lands.*
