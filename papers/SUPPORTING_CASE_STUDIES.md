# Supporting case studies — the documented work behind the papers (PAPERS · maintained index)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑25. The single
maintained register that **cites all of our work inside our work**: every real‑data Hˢ study, demonstration, and
documented study of interest that *supports* the P‑series without itself being a paper. Each entry names its
content receipt and its repository home, so any reader can route to the proof in one hop. New studies are added
here as they are run. Honest‑broker tiered; descriptive; nothing posted; Peter is the sole gate.*

---

## Why this register exists

The papers carry the *higher intelligence*; the repository carries the *vast effort of evidence*
([`PAPER_AND_REPO_DIVISION.md`](PAPER_AND_REPO_DIVISION.md)). This page is the bridge for the **studies that are
not (yet) papers** — receipted, real‑data work that backs the claims and shows the instrument's reach. The
practice is deliberate: **advertise by citing all our work in our work** — so a first‑time reader sees the breadth,
and every claim points to a runnable receipt.

## A · Industrial‑instrument studies (real data, receipted)

| study | what it reads | receipt | home |
|---|---|---|---|
| Gas / process‑fluid (×4: life‑support, produced‑water, blood‑gas, cabin) | conserved gas budgets; ratio‑blind silent drift | lossless 1e‑15 class | `industrial-instruments/gas-composition-study/` |
| Financial (S&P ten‑sector) | the composition that allocates money; arrow + regimes | `5b2a32d6` | `industrial-instruments/financial/` |
| Backblaze fleet (4th anchor) + SO(4) | pre‑fault drift; **rotation‑blind** 6‑DOF (30 events) | `d531e545` | `experiments/so4_dualquaternion_2026-06/` |
| Constellation (SpaceX) | fleet coherence; storm/anomaly read (concept) | — (T2/T3) | `industrial-instruments/constellation-spacex/` |
| Electronics‑assembly SMT (Nordson/Fuji) | dispense silent‑drift; contact‑point doctrine | `cf9bf72f`, `ae19158b` | `industrial-instruments/electronics-assembly-smt/` |
| Fiber × Hˢ + coherence | common‑mode in glass (310 dB); coherence law | `e791ec63`, `a5ceab9e` | `…/electronics-assembly-smt/` |
| EUV lithography | stochastic valley‑of‑death; directional dose arrow | `877516b6` | `industrial-instruments/euv-lithography/` |
| Canada open‑data estate | composition of all 47,462 open.canada.ca datasets | `209a8559` | `industrial-instruments/canada-open-data/` |
| **World monetary composition — GDP layer** | **world economic weight over time; laminar/turbulent flow; country→bloc recursion** | **`d03048c3`** | `industrial-instruments/world-monetary-composition/` |
| **World monetary composition — money layer (IMF COFER)** | **reserve‑currency composition; USD 72→58%; reserves _diversify_ while GDP _concentrates_** | **`e339945f`** | `…/world-monetary-composition/RESULTS_cofer_money_layer.md` |
| Energy (EMBER) + wine trade | Canada/Portugal + all‑countries energy mix; wine‑trade composition | (per‑run receipts) | `industrial-instruments/…` / showcase |

## B · Witness / triangulation studies (the 9‑study trust)

| study | claim it witnesses | home |
|---|---|---|
| W‑I Microbiome (Crohn/HIV) | **dimension is the message** (AUC 0.64→0.83) `bf24c615` | `papers/triangulation/W1_*`, `experiments/dimension_is_the_message_2026-06/` |
| W‑II Mudstone (geology, Wehner) | relational read on real geochemistry | `papers/triangulation/W2_*`, `collaborations/geology-wehner/` |
| W‑III Fleet (Backblaze) | rotation‑blind / pre‑fault drift | `papers/triangulation/W3_*` |

## C · Engine / frontier demonstrations (the method, receipted)

| demonstration | result | receipt | home |
|---|---|---|---|
| SO(n) exact generator | exact rotor to n=1024; the math's boundary | `8107b173` | `experiments/son_generator_2026-06/` |
| HS‑GOLD‑1 conformance + codec | known‑hash fixtures; exact encode/decode | `d7ac6530`, `041de7c9` | `experiments/conformance_fixtures_2026-06/` |
| Compression benchmark | ~3.5–10× (honest — no Shannon‑beating) | `305cc0db` | `experiments/compression_benchmark_2026-06/` |
| QAM space‑link sandbox | ILR ~700× representation robustness | `f502c15d` | `experiments/qam_spaceradio_2026-06/` |
| Ground‑state common‑mode | 313 dB numerical rejection | `d8c21c70` | `experiments/ground_state_noise_cancel_2026-06/` |
| Hs Duplex | bidirectional compositional comms, round‑trip exact | `4241d38a` | `experiments/hs_duplex_2026-06/` |
| Skin of sensors / deformation / workcell | more sensors→more sensitivity; deformation field; closed loop | `de859b2f`, `6e9426ac`, `c17e9ceb` | `experiments/…` |
| Math Hˢ makes simpler | Euler→quaternion exactness, gimbal lock | `552cea61` | `library/math_simpler_demo.py` |

*(This is a living index — not every run is listed; the full chronological record is
[`../ai-refresh/HS_TRACKING_LOG.json`](../ai-refresh/HS_TRACKING_LOG.json) and
[`../EXPERIMENTS_JOURNAL.md`](../EXPERIMENTS_JOURNAL.md).)*

---

## The community this connects to — Compositional Data Analysis (CoDa)

The single most valuable thing a newcomer may not realize: **Hˢ is not alone.** Its mathematics — closure, the
centered‑ and isometric‑log‑ratio transforms, the Aitchison metric on the simplex — is the shared language of an
established, rigorous, and welcoming international research community: **Compositional Data Analysis (CoDa)**. It is
quietly one of the most coherent communities in applied mathematics — *little known outside its field, almost a
secret society to those who haven't met it* — and connecting to it is a large part of the value here: it means the
instrument stands on decades of peer‑reviewed geometry, not a private invention.

**The scholars the instrument stands on (publicly known credentials; full citations in the README):**

- **John Aitchison (1926–2016)** — the founder; *The Statistical Analysis of Compositional Data* (1982/1986) — the
  work that defined the field.
- **Vera Pawlowsky‑Glahn** — Emeritus Professor, **University of Girona**; co‑architect of the modern Aitchison
  geometry (the geometric approach to the simplex, 2001).
- **Juan José Egozcue** — Department of Applied Mathematics, **Universitat Politècnica de Catalunya (UPC),
  Barcelona**; co‑developer of the **isometric log‑ratio (ILR)** transform (2003) — the exact map this instrument's
  D=4 quaternion rung builds on. *(Chaired the committee that accepted this work at CoDaWork 2026.)*
- **Raimon Tolosana‑Delgado** — co‑author of *Modeling and Analysis of Compositional Data* (2015); compositional
  geostatistics.
- **Peter Filzmoser & Karel Hron** — *Applied Compositional Data Analysis* (2018); robust CoDa (TU Wien; Palacký
  University Olomouc).
- **Michael Greenacre** — *Compositional Data Analysis in Practice* (2018); correspondence analysis.
- **Gregory B. Gloor** — "Microbiome datasets are compositional: and this is not optional" (2017) — the result that
  made CoDa essential to genomics.
- **Antonella Buccianti** (geochemistry), **Javier Palarea‑Albaladejo** (`zCompositions`; zeros & censoring), and
  the **CoDaWork** conference series (biennial, since 2003, Girona) — the community's home.

**Why this matters to a user:** adopting Hˢ is *joining a field, not betting on a lone tool.* The geometry is
peer‑reviewed and taught; the vocabulary is shared; the community is active and generous (two of its founders gave
this work written discussion). The instrument's contribution — *determinism, hash‑receipts, the kinematic
extension, the blindness suite* — sits **on top of** that foundation and points back to it at every step. The full,
maintained acknowledgments and references live in [`../README.md`](../README.md) §References & Acknowledgments;
this showcase exists to make sure no reader misses the door into that community.

> *The instrument reads. The expert decides. These are the experts — and they are a community you can join.*

## Honest scope

- **T1:** every receipted study above (real data, reproducible).
- **T2:** the framing as a coherent supporting body of work.
- **T3:** any value/uptake. Credentials stated are publicly known; the authoritative citations are in the README.
  Not advice; nothing posted; Peter is the sole gate.

*Cross‑refs: `THE_HIGGINS_DECOMPOSITION_SERIES.md`, `PAPER_AND_REPO_DIVISION.md`, `../README.md` (References &
Acknowledgments), `../ai-refresh/HS_TRACKING_LOG.json`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — all our work cited in our work · the community showcased with real credentials · every claim points to a receipt · the human decides.*
