# CoDaWork 2026 — follow along with the talk

**Welcome.** This page tracks the talk slide by slide. Open it on your phone or a second screen and click each link as the speaker reaches that beat. Everything you'll hear referenced is here in order, with the manuscript section, the supporting figure, the equation, or the raw data file linked exactly where it comes up. If you can't see the screen or are joining remotely, you can run the entire talk from this single page.

- **Talk:** *Compositional monitoring of energy-mix drift on the simplex*
- **Speaker:** Peter Higgins · Rogue Wave Audio · Binaural Test Lab · Markham, Ontario, Canada
- **Conference:** CoDaWork 2026 · Coimbra, Portugal · 1–5 June 2026
- **Repository:** https://github.com/PeterHiggins19/higgins-decomposition

## The presentation in three places

Pick one to keep open alongside this page; the speaker will move between them as the talk progresses.

| | File | What it is |
|---|---|---|
| 📄 | **[`Manuscript (PDF)`](CODAwork2026/Compositional_Monitoring_2026.pdf)** · [`(DOCX)`](CODAwork2026/Compositional_Monitoring_2026.docx) | The 25-page peer-reviewable paper. Cover, table of contents, six figures, three appendices, full reference list. |
| 🎞 | **[`Presentation (PDF)`](CODAwork2026/data_outputs/CodaWork2026_Presentation_2026-05-27.pdf)** · [`(PPTX)`](CODAwork2026/data_outputs/CodaWork2026_Presentation_2026-05-27.pptx) | The **21 slides** being presented — a single grayscale deck (numbered N / 21, ~14 min spoken): the talk, then the rest-of-world finale (the other six countries), then the live-projector close. Named on its subject, **deceptive drift**, defined where it first appears. The 13-slide colour predecessor + scripts are archived at [`CODAwork2026/archive/talk_decks_pre_presentation_2026-05-27/`](CODAwork2026/archive/talk_decks_pre_presentation_2026-05-27/). |
| 🎬 | **[`Full-corpus reference (PDF)`](CODAwork2026/data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf)** | The 325-page master PDF of the engine's complete output — master cover + 9 country sections × 6 plates each. For Q&A that reaches past the trajectories shown in the deck. |
| 🔭 | **[`Interactive HTML projector`](CODAwork2026/data_outputs/codawork2026_projector.html)** | The 3-D manifold projector. Runs in your browser. No install. See "How to run the projector" at the end of this page. |

---

## Slide-by-slide follow-along

The talk runs about fourteen minutes spoken across twenty-one numbered slides (N / 21): the method, the three country case-studies (Germany carried in full — the complete plate set), then the rest-of-world finale (the other six countries), then the live-projector close. About five minutes of Q&A follow.

### Slide 1 · Title — standard CoDa, and we add time
*Compositional monitoring of energy-mix drift on the simplex.*  **Which carrier did the structural work?** Not which one got bigger — which one moved the composition. Standard compositional data analysis; the one new move is reading the simplex (shares that sum to one) forward in time.

- Speaker contact, repository URL, community folder, and UN-6 handout availability are all on this slide.
- **Hˢ runs any compositional dataset the CoDa community can describe** — every view here is reproducible on your data.
- [Manuscript cover page + abstract](CODAwork2026/Compositional_Monitoring_2026.pdf)

### Slide 2 · The size view hides the work — *deceptive drift* defined
A carrier can be small in share yet do most of the structural work. **Germany Solar, 2005 → 2006** — starting share 0.21 %, structural Power Share 71.1 %, **Activation Coefficient ≈ 333×.** **Deceptive drift:** the size (share) view hides which carrier did the structural work — here a 0.21 % carrier does 71 % of it.

- [Manuscript — Introduction §1, Fig. 1](CODAwork2026/Compositional_Monitoring_2026.pdf)

### Slide 3 · Reading time on the simplex — the five named methods
**Composition** (each carrier's share) · **Helmsman** (the carrier with the largest CLR move at a step) · **Helmsman trajectory** (when the largest-motion carrier changes) · **Power Share** (each carrier's share of the squared CLR motion) · **Activation Coefficient** (Power Share ÷ starting share). All five derive from CLR + Helmert-ILR. Standard CoDa geometry; the new move is reading it over time.

- **Fig. 1** — the method diagram (each term defined in its box)
- [Manuscript Appendix A — Equations 1–8](CODAwork2026/Compositional_Monitoring_2026.pdf)

### Slide 4 · The Activation Coefficient
*α_i(t) = Power Share_i(t) ÷ starting share_i(t).*  **α ≈ 1** ordinary · **α ≫ 1** hidden driver · **α < 1** coasting. By analogy: yeast is 2 % of a loaf by mass and does 100 % of the rising — the same shape.

- **Eq. 7** — Activation Coefficient formula, Appendix A
- Worked example: Germany Solar 2005 → 2006 = 333×.
- [Supplementary Information §S2 — full activation-moment table](../papers/codawork2026/manuscript/SUPPLEMENTARY.md)

### Slide 5 · Three archetypes — one instrument, three regimes
**Germany** — deliberate transition, continuous arc on the simplex. **Japan** — external shock from Fukushima 2011, loop and reorganise. **United Kingdom** — regime change, coal exit, jump and return. One protocol reads all three. Each country runs as a pair next.

- [Manuscript — Results §2–4](CODAwork2026/Compositional_Monitoring_2026.pdf)

### Slide 6 · Germany — share and structural work *(case study 1, beat 1)*
The Energiewende through the share-and-structural-work lens. **Solar 2005–2006** at 0.21 % share, doing 71.1 % of the work — **α ≈ 333×**. The structural beginning of the transition is named *three years* before the size view calls it visible — the deceptive-drift signature.

- **Fig. 2** — Germany size-view (hatched stacked area) + Power-Share decomposition
- [Manuscript — Results §2 Germany](CODAwork2026/Compositional_Monitoring_2026.pdf)
- 📂 Raw output: [`cnt_DEU.json`](CODAwork2026/data_outputs/per_country_json/cnt_v3/cnt_DEU.json)
- 📂 Germany plates: [`DEU_stage0.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_stage0.pdf), [`DEU_stage1.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_stage1.pdf), [`DEU_stage23.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_stage23.pdf), [`DEU_cnq.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_cnq.pdf)

### Slide 7 · Germany — the trajectory *(case study 1, beat 2)*
The Helmsman trajectory at full size — **trajectory directness 0.41** (end-to-end distance ÷ path length), a continuous arc toward the renewable vertex. Smooth, monotone reorientation — no loops, no flips. Deliberate transition as a single sustained trajectory.

- **Fig. 6 (Germany panel)** — per-country navigation chart at full legibility
- Germany, the worked exemplar, gets two more plates next — the complete geometric set — then the contrasting regimes.

### Slide 8 · Germany — orthogonal projections (the complete set)
Germany is the worked exemplar, so Germany alone is shown with the **complete plate set**. This is the Stage-1 **Section view**: the CLR plan (XY), the carrier-pair bearings (XZ), and per-carrier CLR (YZ) for a representative year, plus the metadata box (Hˢ, kappa, the Helmsman, the directness ratio).

- 📂 Germany Stage-1 plates: [`DEU_stage1.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_stage1.pdf)

### Slide 9 · Germany — ILR-Helmert triplet (the complete set)
The orthonormal companion: three orthogonal scatter projections of Germany's 2000–2025 trajectory onto the first three Helmert ILR axes (ilr1×ilr2 · ilr1×ilr3 · ilr2×ilr3) — the same continuous arc, in the basis with no preferred carrier. That is the complete geometric set for one country; the other regimes follow.

- 📂 Dual-view (Section + Triplet): [`dual_view/`](CODAwork2026/data_outputs/dual_view/)

### Slide 10 · Japan — share and structural work *(case study 2, beat 1)*
The Fukushima 2011 shock appears in every reading at once. **17 Helmsman flips** — the loudest count in the corpus. **Aitchison distance (distance on the simplex) 2011 → 2012 ≈ 3× the baseline step.** The years *after* tell the deeper story: a decade-long reorganisation across solar, gas, wind, renewables.

- **Fig. 3** — Japan size-view + Power-Share decomposition
- [Manuscript — Results §3 Japan](CODAwork2026/Compositional_Monitoring_2026.pdf)
- 📂 Raw output: [`cnt_JPN.json`](CODAwork2026/data_outputs/per_country_json/cnt_v3/cnt_JPN.json)
- 📂 Japan plates: [`JPN_stage0.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_stage0.pdf), [`JPN_stage1.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_stage1.pdf), [`JPN_stage23.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_stage23.pdf), [`JPN_cnq.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_cnq.pdf)

### Slide 11 · Japan — the trajectory *(case study 2, beat 2)*
The Helmsman trajectory at full size — **trajectory directness 0.09**, the loop-and-reorganise pattern. The trajectory revisits and reroutes. Compared to Germany's smooth arc, Japan's trajectory shows a system *searching* for a new composition rather than walking a planned one.

- **Fig. 6 (Japan panel)** — per-country navigation chart at full legibility
- 🔭 **Projector matches this slide:** click **JPN**, then **BARY**, then **SHOCK**, then **ALIGN** for the CoDa-centred view.

### Slide 12 · United Kingdom — share and structural work *(case study 3, beat 1)*
Coal exit as regime change. Between 2012 and 2020, coal goes from > 30 % to < 2 %. A true regime change, not a drift. The Power-Share view tells you *how the displaced structural work was absorbed* — wind, solar, biomass, other renewables each took portions. No single replacement carrier.

- **Fig. 4** — UK size-view + Power-Share decomposition
- [Manuscript — Results §4 United Kingdom](CODAwork2026/Compositional_Monitoring_2026.pdf)
- 📂 Raw output: [`cnt_GBR.json`](CODAwork2026/data_outputs/per_country_json/cnt_v3/cnt_GBR.json)
- 📂 UK plates: [`GBR_stage0.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_stage0.pdf), [`GBR_stage1.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_stage1.pdf), [`GBR_stage23.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_stage23.pdf), [`GBR_cnq.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_cnq.pdf)

### Slide 13 · United Kingdom — the trajectory *(case study 3, beat 2)*
The Helmsman trajectory at full size — **trajectory directness 0.36**, the jump-and-return pattern. The trajectory leaves the coal vertex sharply, then settles toward a new mix. Distinct from Germany's continuous arc, distinct from Japan's looping search. Three transitions, three patterns, one geometry.

- **Fig. 6 (UK panel)** — per-country navigation chart at full legibility

### Slide 14 · Across the corpus — deceptive drift in 5 of 9
Same instrument, nine EMBER countries. Deceptive drift is **present in 5 of 9** — **AUS, CHN, GBR, IND, JPN** — and **absent in four** — DEU (annual grain), FRA, USA, the World aggregate. Discrimination — flagging some systems and not others — is itself evidence the detector reads real structure.

- **Fig. 5** — nine-country signature plate (top activation moments + counts + Activation Coefficients + Helmsman flips)
- [Manuscript — Results §5 (cross-country signature)](CODAwork2026/Compositional_Monitoring_2026.pdf)
- 📂 All nine countries: [`per_country_json/cnt_v3/`](CODAwork2026/data_outputs/per_country_json/cnt_v3/)

### Slides 15–20 · The rest of the world — the other six
The breadth sweep: one full-trajectory diagram per country, the six not walked through in the case studies. **Deceptive drift present** — **Slide 15 Australia · Slide 16 China · Slide 17 India.** **Deceptive drift absent** — **Slide 18 France · Slide 19 United States · Slide 20 World aggregate** (large-N smoothing hides the deceptive drift in its constituents). One breath each; this is the direct visual backing for slide 12.

- 📂 All six: [`per_country_json/cnt_v3/`](CODAwork2026/data_outputs/per_country_json/cnt_v3/) — `cnt_AUS`, `cnt_CHN`, `cnt_IND`, `cnt_FRA`, `cnt_USA`, `cnt_WLD`
- 📂 Full plate sets for every country: [`per_country_pdfs/`](CODAwork2026/data_outputs/per_country_pdfs/) and the full-corpus reference PDF

### Slide 21 · What the stack answers — the live instrument closes
**WHAT** carriers are big · **WHO** is in largest motion (Helmsman) · **WHEN** the largest-motion carrier changes · **HOW MUCH** structural work each carrier did (Power Share) · **WHY** a small carrier mattered (Activation Coefficient). One observable, five questions, one reproducible object. *The stack does not replace interpretation. It gives interpretation a reproducible object.* Then the live projector takes over for Q&A.

- [Manuscript — Discussion + Conclusions](CODAwork2026/Compositional_Monitoring_2026.pdf)
- **AI Use Declaration (HUF-STD-001 v1.1)** — research design, mathematical content, code, and scientific responsibility remain with the named author. AI assistants used for drafting, sweeps, and reviews. Author retains full responsibility.
- 🔭 Open the projector; for any question past the trajectories, the full-corpus reference holds all 27 plates per country.

---

## Things not in the deck but available

The talk deliberately omits the MC-4 falsifiability slide and the "inspect the instrument" closer to keep within time. Both still live in the repo:

- **MC-4 falsifiable claim** (three conjuncts + four defeat paths) — full text in the manuscript Discussion and in [`papers/codawork2026/MC4_PACKET.md`](../papers/codawork2026/planning/HUF_MC4_CoDaWork_Packet_v3.pdf).
- **Speaker brief** with optional verbal closing-line (the locomotive metaphor) — [`papers/codawork2026/talk/SPEAKER_BRIEF.md`](../papers/codawork2026/talk/SPEAKER_BRIEF.md).
- **Cinema scroll** — 66-slide / 325-page reel of every plate the engine produced. Runs during Q&A as evidence reserve.
- **Interactive projector** — RADAR / BARY / ALIGN / SHOCK modes. Q&A backdrop. See "How to run the projector" below.
- **Repository, manuscript, glossary, contact, reproduction commands** — all on slide 1 and on the printed handout.

## How to run the projector

The HTML projector is a single self-contained file with embedded data. No server, no install, no network call. Three options:

**Option A — local download (works on any device with a browser).**
1. Click the [`codawork2026_projector.html`](CODAwork2026/data_outputs/codawork2026_projector.html) link above.
2. On the GitHub page, click **"Download raw file"** (top-right of the file view).
3. Open the downloaded file in any modern browser (Chrome / Firefox / Safari / Edge).

**Option B — GitHub Pages (no download, click-through).**
If Pages is enabled, the projector is live at `https://peterhiggins19.github.io/higgins-decomposition/CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html`.

**Option C — clone the repo.**
```
git clone https://github.com/PeterHiggins19/higgins-decomposition.git
cd higgins-decomposition/CODA-Association/CODAwork2026/data_outputs/
open codawork2026_projector.html
```

### Using the projector (90-second tour)

The HUD is laid out as follows:

- **Top-left** — title and a PROJECTION info panel showing the math being applied to what you're seeing. Toggle off with **PROJ** if you want a clean view.
- **Top-right** — controls:
  - **Country buttons** (CHN / DEU / FRA / GBR / IND / JPN / USA / WLD) — pick a dataset.
  - **ORBIT / TRAILS / LABELS / GHOST / COLOR** — display toggles.
  - **BARY** — barycenter trajectory mode: the spine bends through space, tracing the composition's path on the simplex's principal 2-D subspace.
  - **ALIGN** — barycenter-aligned mode: the trajectory is forced onto the central z-axis; pure shape variation around each year's own centroid (the CoDa-standard centred view).
  - **SHOCK** — combine with any mode: on a shock year (Aitchison-step distance above threshold) the year label flips to the chromatic opposite of the plate's base colour — a dedicated channel that flags shock years without disturbing the trajectory's own colours.
  - **FRONT / SIDE / TOP / ISO** — fixed camera angles.
- **Bottom** — TIME slider scrubs year-by-year. Drag to pause anywhere.

### Try this on Japan (matches Slides 10–11 — the Japan pair)

1. Click **JPN**.
2. Click **BARY**. Watch what happens at 2011 → 2012 (Fukushima) and especially through 2013 → 2014–2015 (the multi-year reorganisation toward solar + renewables).
3. Click **ALIGN**. The bend is removed; the polygon shape variation per year is what remains — the CoDa-correct centred view.
4. Click **SHOCK**. The shock years' labels flip to the chromatic-opposite colour.
5. Read the PROJECTION info panel for the math. It updates live with the active mode.

---

## To dig deeper

| To … | Read … |
|---|---|
| Verify a specific number | [Manuscript Methods](CODAwork2026/Compositional_Monitoring_2026.pdf) + [Supplementary Information §S4 (reproduction commands, SHA-256 hashes)](../papers/codawork2026/manuscript/SUPPLEMENTARY.md) |
| See the engine that produced the numbers | [`HCI-CNT/engine/cnt.py`](../HCI-CNT/engine/cnt.py) (Python) · [`cnt.R`](../HCI-CNT/engine/cnt.R) (R) |
| Read the canonical Hˢ glossary and notation | [`HCI-CNT/handbook/GLOSSARY.md`](../HCI-CNT/handbook/GLOSSARY.md) · [`NOTATION_AND_TERMINOLOGY.md`](../HCI-CNT/handbook/NOTATION_AND_TERMINOLOGY.md) |
| See Hˢ across all 101 reference datasets | [`experiments/2026-05-10_full-corpus-validation/`](../experiments/2026-05-10_full-corpus-validation/) |
| Get oriented in the repository | [`README.md`](../README.md) · [`QUICKSTART.md`](../QUICKSTART.md) · [`PUBLICATION_READY.md`](../PUBLICATION_READY.md) |
| Challenge or extend the claim | Open an issue at https://github.com/PeterHiggins19/higgins-decomposition/issues, or contact PeterHiggins@RogueWaveAudio.com |

## Citation

> Higgins, P. (2026). *Compositional monitoring of energy-mix drift on the simplex.* Prepared for CoDaWork 2026, Coimbra, Portugal. https://github.com/PeterHiggins19/higgins-decomposition

> Higgins, P. (2026). *HCI-CNT — Compositional Navigation Tensor engine.* https://github.com/PeterHiggins19/higgins-decomposition · Apache-2.0.

Full citation metadata: [`CITATION.cff`](../CITATION.cff).

## Licensing

- **Code:** Apache-2.0 ([`LICENSE`](../LICENSE))
- **Documentation, figures, data outputs:** CC BY 4.0 ([`LICENSE-DOCS`](../LICENSE-DOCS))
- **EMBER raw data:** CC BY 4.0 — https://ember-energy.org

Free to use, free to cite, free to remix with attribution.

---

*The instrument reads.   The expert d