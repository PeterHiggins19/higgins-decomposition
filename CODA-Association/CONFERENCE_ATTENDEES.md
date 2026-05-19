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
| 🎞 | **[`Talk deck (PDF)`](CODAwork2026/data_outputs/CodaWork2026_FinalTalk_2026-05-17.pdf)** · [`(PPTX)`](CODAwork2026/data_outputs/CodaWork2026_FinalTalk_2026-05-17.pptx) | The 22 slides being presented. |
| 🎬 | **[`Cinema scroll (PDF)`](CODAwork2026/data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf)** | The 325-page master PDF of the engine's actual output — every plate the engine produced, master cover + 9 country sections × 6 plates each. |
| 🔭 | **[`Interactive HTML projector`](CODAwork2026/data_outputs/codawork2026_projector.html)** | The 3-D manifold projector. Runs in your browser. No install. See "How to run the projector" at the end of this page. |

---

## Slide-by-slide follow-along

### Slide 1 · Title
*Compositional monitoring of energy-mix drift on the simplex.*  Five viewpoints. One observable stack. The hidden drivers, named.

- Read along: [Manuscript cover page](CODAwork2026/Compositional_Monitoring_2026.pdf)
- Conference: CoDaWork 2026 · Coimbra · 1–5 June 2026

### Slide 2 · The Question
What carriers really drove each country's energy transition — and which were doing the structural work?

- [Manuscript — Introduction §1](CODAwork2026/Compositional_Monitoring_2026.pdf) (page 4 of the PDF)

### Slide 3 · Viewpoint 1 — the size view
What everyone sees when they look at a stacked-area chart. And what they miss.

- [Manuscript — Introduction §1, last paragraph + Fig. 1](CODAwork2026/Compositional_Monitoring_2026.pdf)
- The world stacked-area chart — coal dominant for most of the period, solar a thin yellow sliver after 2010, gas grows substantially, nuclear declines slowly, wind grows steadily but small until late. **USA 2012–2013: solar holds 0.107 % of the mix yet did 81.7 % of the structural work — Activation Coefficient 760×.** That number is what this talk is about.

### Slide 4 · The five-viewpoint protocol
Each viewpoint answers one specific question; combined, they yield a complete answer for any year-to-year transition step.

- **Fig. 1** — schematic of the five viewpoints (composition · helmsman · helmsman trajectory · Power Share · Activation Coefficient) feeding one combined observable
- [Manuscript — Introduction §3 (the five viewpoints)](CODAwork2026/Compositional_Monitoring_2026.pdf)
- [Manuscript Appendix A — Equations 1–8 (mathematical foundation)](CODAwork2026/Compositional_Monitoring_2026.pdf)

### Slide 5 · Viewpoint 2 — the helmsman
Who is at the wheel each year? The single carrier with the largest CLR displacement at each transition step. Plotted with **dotted** lines: a categorical assignment per step, not a continuous path.

- **Eq. 5** — *σ(t) = argmax_i | clr_i(t+1) − clr_i(t) |* (Appendix A of the manuscript)
- [Manuscript — Results §1 (helmsman + ILR-Helmert basis)](CODAwork2026/Compositional_Monitoring_2026.pdf)
- Helmsman flip count range across our corpus: 4 (World aggregate, stable) → 17 (Japan, post-Fukushima cascade).

### Slide 6 · Viewpoint 3 — Power Share
How much each carrier did at each transition. Squared CLR motion, decomposed across carriers; sums to 100 % at every step. No carrier hidden by the bookkeeping.

- **Eq. 6** — *π_i(t) = (Δclr_i)² / Σ_j (Δclr_j)²,  Σ_i π_i = 1*
- What's big ≠ what's moving. This is the operational distinction.

### Slide 7 · Viewpoint 4 — the Activation Coefficient (the yeast factor)
Why a small carrier mattered. Power Share divided by the carrier's composition share at the start of the step.

- **Eq. 7** — *α_i(t) = π_i(t) / ρ_i(t),  reported when ρ_i(t) ≥ 0.1 %*
- α = 1: the carrier did exactly its size's share of work. α ≫ 1: a small carrier doing structural work far beyond its size — a hidden driver, the "yeast factor". α ≪ 1: a large carrier moving less than its size predicts — structural ballast.
- **Worked example, the headline number:** USA Solar 2012 → 2013 — composition share start of 2012 = 0.107 %; Power Share of squared CLR motion = 81.7 %; Activation Coefficient = 760×.

### Slide 8 · The hidden driver — solar, 2010–2015
Across nine national electricity mixes, solar at sub-0.2 % composition share did 70–85 % of the structural directional work between 2010 and 2015. The top-10 yeast moments in the 9-country corpus.

- [Manuscript — Results §5 (cross-country signature) + Fig. 5 caption](CODAwork2026/Compositional_Monitoring_2026.pdf)
- [Supplementary Information §S2 — full 406-yeast-moment table](../papers/codawork2026/manuscript/SUPPLEMENTARY.md)

### Slide 9 · Germany — the continuous arc to the renewable vertex
Twenty-five years of deliberate composition change. The Energiewende, read at year-grain compositional resolution. Solar 2005–2006 at 0.21 % share, doing 71.1 % of the work — AC ≈ 333×. The structural beginning is named.

- **Fig. 2** — four-panel Germany plate (size view · helmsman · Power Share · top yeast)
- [Manuscript — Results §2 Germany](CODAwork2026/Compositional_Monitoring_2026.pdf)
- 📂 Raw per-country output: [`cnt_DEU.json`](CODAwork2026/data_outputs/per_country_json/cnt_v3/cnt_DEU.json) (CNT v3.1.0 engine output)
- 📂 Full Germany plate set: [`per_country_pdfs/DEU_stage0.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_stage0.pdf), [`DEU_stage1.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_stage1.pdf), [`DEU_stage23.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_stage23.pdf), [`DEU_cnq.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_cnq.pdf)

### Slide 10 · Japan — Fukushima 2011 and the multi-year reorganisation
An external shock that registers in every viewpoint. Helmsman flips 17 times — the loudest in the corpus. Aitchison distance 2011 → 2012 ≈ 3× neighbouring years. The post-shock cascade tells the deeper story.

- **Fig. 3** — Japan four-panel plate (gold-shaded 2011–2013 window)
- [Manuscript — Results §3 Japan](CODAwork2026/Compositional_Monitoring_2026.pdf)
- 📂 Raw output: [`cnt_JPN.json`](CODAwork2026/data_outputs/per_country_json/cnt_v3/cnt_JPN.json)
- 📂 Japan plates: [`JPN_stage0.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_stage0.pdf), [`JPN_stage1.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_stage1.pdf), [`JPN_stage23.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_stage23.pdf), [`JPN_cnq.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_cnq.pdf)

### Slide 11 · United Kingdom — the coal exit as a regime change
Policy-driven transition. Coal goes from > 30 % to < 2 %. Specific small carriers — wind, solar, Other Renewables — absorbed the displaced share, each doing structural work for two-to-three years at a time.

- **Fig. 4** — UK four-panel plate (gold-shaded 2018–2021 window)
- [Manuscript — Results §4 United Kingdom](CODAwork2026/Compositional_Monitoring_2026.pdf)
- 📂 Raw output: [`cnt_GBR.json`](CODAwork2026/data_outputs/per_country_json/cnt_v3/cnt_GBR.json)
- 📂 UK plates: [`GBR_stage0.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_stage0.pdf), [`GBR_stage1.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_stage1.pdf), [`GBR_stage23.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_stage23.pdf), [`GBR_cnq.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_cnq.pdf)

### Slide 12 · Germany — the navigation chart
PCA 2-D projection of the CLR trajectory. Continuous-arc archetype — course directness 0.41.

- **Fig. 6** (Germany panel) — the navigation chart in the manuscript
- This is Plate 16 of `DEU_stage23.pdf` (the System Course Plot)
- 📂 [`per_country_pdfs/DEU_stage23.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_stage23.pdf) — open and jump to page 16

### Slide 13 · Japan — the navigation chart
PCA 2-D projection of the CLR trajectory. Heavy-looping archetype — course directness 0.09. The post-Fukushima multi-year reorganisation registers as path curvature.

- **Fig. 6** (Japan panel)
- 📂 [`per_country_pdfs/JPN_stage23.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_stage23.pdf) — page 16

### Slide 14 · United Kingdom — the navigation chart
PCA 2-D projection of the CLR trajectory. Jump-and-return archetype — course directness 0.36. The coal-exit regime change.

- **Fig. 6** (UK panel)
- 📂 [`per_country_pdfs/GBR_stage23.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_stage23.pdf) — page 16

### Slide 15 · Cross-country signature — 5 of 9 countries reproduce the deceptive-drift pattern
Australia, China, United Kingdom, India, Japan fire the signature. Germany, France, USA, and the World aggregate do not. The pattern is read at year-grain across all nine national electricity mixes.

- **Fig. 5** — the cross-country signature plate
- [Manuscript — Results §5 (cross-country signature)](CODAwork2026/Compositional_Monitoring_2026.pdf)
- 📂 9-country corpus, all JSONs: [`per_country_json/cnt_v3/`](CODAwork2026/data_outputs/per_country_json/cnt_v3/) — AUS, CHN, DEU, FRA, GBR, IND, JPN, USA, WLD

### Slide 16 · Synthesis — WHAT path + WHY
The five viewpoints stack into one observable. Each gives a partial glimpse; together they answer WHAT carriers are big, WHO is at the wheel, WHEN the wheel changes, HOW MUCH each carrier did, and WHY a small carrier mattered.

- [Manuscript — Discussion §1 (synthesis)](CODAwork2026/Compositional_Monitoring_2026.pdf)

### Slide 17 · The falsifiable claim — MC-4 in three conjuncts and four defeat paths
**Aitchison-native + formal change detection + carrier-level attribution → one observable stack.** Four explicit ways a CoDa specialist could defeat the claim: prior-art defeat · metric defeat · case defeat · category defeat.

- [Manuscript — Discussion §2 (MC-4 and the four defeat paths)](CODAwork2026/Compositional_Monitoring_2026.pdf)
- [MC-4 packet (original methods-challenge framing, March 2026)](CODAwork2026/Codaworks2026%20proposal%20for%20conference/HUF_MC4_CoDaWork_Packet_v3.pdf)

### Slide 18 · Bridge — every plate the engine produced
What follows is not slides about data. It is the data, run through the engine, scrolled through as a movie. Nine countries · twenty-six years · six plates per country.

- 🎬 **[Cinema scroll PDF — 325 pages](CODAwork2026/data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf)** — open this and scroll. Every quantity is hash-chained to the input CSV.
- [Or as PPTX (66 slides, auto-advance at ~1 sec/slide)](CODAwork2026/data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pptx)

### Slide 19 · Q & A — with the manifold projector running
Live HTML projector. Interactive 3-D view of the energy-mix manifold. Runs offline; no network required.

- 🔭 **[`codawork2026_projector.html`](CODAwork2026/data_outputs/codawork2026_projector.html)** — open in any browser
- **How to use:** click a country (CHN / DEU / FRA / GBR / IND / JPN / USA / WLD), then try **BARY** (barycenter trajectory), **ALIGN** (CoDa-standard centred view), **SHOCK** (Aitchison-step highlight). See "How to run the projector" at the end of this page.

### Slide 20 · Repositories — reproduce every plate in five minutes
Two public repositories. Hashes carry the receipts. The mathematics is not new; the monitoring application may be.

- [`higgins-decomposition` (Hˢ)](https://github.com/PeterHiggins19/higgins-decomposition) — CNT v3.x and CNQ v2.x engines, Investigation Catalog, HUF-STD-001/002/003, this manuscript
- [`Higgins-Unity-Framework` (HUF)](https://github.com/PeterHiggins19/Higgins-Unity-Framework) — MC-4 framing, EITT canonical, governance charter

### Slide 21 · AI Use Declaration
Per HUF Publication Standards (HUF-STD-001 v1.1) — conforming to ICMJE / COPE / Nature/Springer / Science/AAAS / WAME / EU AI Act (2024) / arXiv / ACM / IEEE.

- [`HUF-STD-001 v1.1` (Publication Standards)](../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json)
- [Manuscript — Acknowledgements section](CODAwork2026/Compositional_Monitoring_2026.pdf)

### Slide 22 · Standard Stamp — engine declaration · find us · contact
- **Repository:** https://github.com/PeterHiggins19/higgins-decomposition
- **Author / Lab:** Peter Higgins · Rogue Wave Audio / Binaural Test Lab · Markham, Ontario, Canada
- **Contact:** PeterHiggins@RogueWaveAudio.com
- **License:** code Apache-2.0 · documentation CC BY 4.0
- Help is available — free, no gatekeeping.

---

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
  - **SHOCK** — combine with any mode: tints plate outlines red proportional to Aitchison-step magnitude.
  - **FRONT / SIDE / TOP / ISO** — fixed camera angles.
- **Bottom** — TIME slider scrubs year-by-year. Drag to pause anywhere.

### Try this on Japan (matches the Slide 12–14 reading)

1. Click **JPN**.
2. Click **BARY**. Watch what happens at 2011 → 2012 (Fukushima) and especially through 2013 → 2014–2015 (the multi-year reorganisation toward solar + renewables).
3. Click **ALIGN**. The bend is removed; the polygon shape variation per year is what remains — the CoDa-correct centred view.
4. Click **SHOCK**. The shock years light up in red.
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

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*The mathematics is not new; the monitoring application may be.*

*Welcome to CoDaWork 2026. Thanks for being in the room — or watching from anywhere.*
