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
| 🎞 | **[`Talk deck (PDF)`](CODAwork2026/data_outputs/CodaWork2026_FinalTalk_13Slide_2026-05-24.pdf)** · [`(PPTX)`](CODAwork2026/data_outputs/CodaWork2026_FinalTalk_13Slide_2026-05-24.pptx) | The **13 slides** being presented (expanded final version, ~8 min 50 sec spoken). Each country case-study runs as a paired sequence — share-and-work view, then dedicated navigation chart at legible size. The 10-slide compressed predecessor is archived at [`CODAwork2026/archive/talk_decks_pre_13slide_2026-05-24/`](CODAwork2026/archive/talk_decks_pre_13slide_2026-05-24/); the earlier 22-slide narrative and 12-slide intermediate at [`CODAwork2026/archive/talk_decks_pre_10slide_2026-05-20/`](CODAwork2026/archive/talk_decks_pre_10slide_2026-05-20/). |
| 🎬 | **[`Cinema scroll (PDF)`](CODAwork2026/data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf)** | The 325-page master PDF of the engine's actual output — every plate the engine produced, master cover + 9 country sections × 6 plates each. |
| 🔭 | **[`Interactive HTML projector`](CODAwork2026/data_outputs/codawork2026_projector.html)** | The 3-D manifold projector. Runs in your browser. No install. See "How to run the projector" at the end of this page. |

---

## Slide-by-slide follow-along

The talk runs about nine minutes spoken across thirteen slides, with the three country case-studies each split into a paired sequence (share-and-work view, then navigation chart at legible size). The cinema scroll and projector then run during Q&A.

### Slide 1 · Title + question + contact
*Compositional monitoring of energy-mix drift on the simplex.*  **Which carrier did the structural work?** Not which one got bigger — which one moved the composition.

- Speaker contact, repository URL, community folder, and UN-6 handout availability are all on this slide.
- [Manuscript cover page + abstract](CODAwork2026/Compositional_Monitoring_2026.pdf)

### Slide 2 · The size view hides the work
A carrier can be small in share and large in structural work. **USA Solar, 2012 → 2013** — starting share 0.107 %, structural Power Share 81.7 %, **Activation Coefficient ≈ 760×.** Solar acted at 760× its size. No size view shows that.

- [Manuscript — Introduction §1, Fig. 1](CODAwork2026/Compositional_Monitoring_2026.pdf)
- That number is the reason for this talk.

### Slide 3 · Five viewpoints, one observable stack
**Composition** (size) · **Helmsman** (largest CLR move at a step) · **Helmsman trajectory** (when steering changes) · **Power Share** (how much squared CLR motion each carrier did) · **Activation Coefficient** (Power Share ÷ starting share — the yeast factor). All five derive from CLR + Helmert-ILR. Standard CoDa geometry, new framing as a stack.

- **Fig. 1** — the five-viewpoint schematic
- [Manuscript Appendix A — Equations 1–8](CODAwork2026/Compositional_Monitoring_2026.pdf)

### Slide 4 · The Activation Coefficient — the yeast factor
*α_i(t) = Power Share_i(t) ÷ starting share_i(t).*  **α ≈ 1** ordinary · **α ≫ 1** hidden driver · **α < 1** coasting. Yeast is 2 % of a loaf by mass and does 100 % of the rising — same mathematical shape.

- **Eq. 7** — Activation Coefficient formula, Appendix A
- Worked example carried through: USA Solar 2012 → 2013 = 760×.
- [Supplementary Information §S2 — full 406-yeast-moment table](../papers/codawork2026/manuscript/SUPPLEMENTARY.md)

### Slide 5 · Three archetypes — one instrument, three regimes
**Germany** — deliberate transition, continuous arc on the simplex. **Japan** — external shock from Fukushima 2011, loop and reorganise. **United Kingdom** — regime change, coal exit, jump and return. One protocol reads all three. Each country runs as a paired sequence next.

- [Manuscript — Results §2–4](CODAwork2026/Compositional_Monitoring_2026.pdf)

### Slide 6 · Germany — share-and-work view *(case study 1, beat 1)*
The Energiewende through the share-and-work lens. **Solar 2005–2006** at 0.21 % share, doing 71.1 % of the work — **AC ≈ 333×**. The structural beginning of the transition is named *three years* before the size view calls it visible. Tiny share, dominant work — the yeast-factor signature.

- **Fig. 2** — four-panel Germany plate (shares, helmsman trajectory, Power Share, Activation Coefficient)
- [Manuscript — Results §2 Germany](CODAwork2026/Compositional_Monitoring_2026.pdf)
- 📂 Raw output: [`cnt_DEU.json`](CODAwork2026/data_outputs/per_country_json/cnt_v3/cnt_DEU.json)
- 📂 Germany plates: [`DEU_stage0.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_stage0.pdf), [`DEU_stage1.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_stage1.pdf), [`DEU_stage23.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_stage23.pdf), [`DEU_cnq.pdf`](CODAwork2026/data_outputs/per_country_pdfs/DEU_cnq.pdf)

### Slide 7 · Germany — course on the simplex *(case study 1, beat 2)*
The Helmsman trajectory at full size — **course directness 0.41**, a continuous arc toward the renewable vertex. Smooth, monotone reorientation. No loops, no flips. The geometry of policy intent — deliberate transition reads as a single sustained course, year after year, in one direction.

- **Fig. 6 (Germany panel)** — per-country navigation chart at full legibility
- The next country pair will show what an unplanned reorganisation looks like by contrast.

### Slide 8 · Japan — share-and-work view *(case study 2, beat 1)*
The Fukushima 2011 shock appears in every viewpoint at once. **Helmsman flips 17 times** — the loudest count in the corpus. **Aitchison distance 2011 → 2012 ≈ 3× neighbouring-year baseline.** The years *after* tell the deeper story: a decade-long reorganisation across solar, gas, wind, renewables — wind 2004→2005 α 188, nuclear 2015→2016 α 187, solar 2005→2006 α 176, the list goes on.

- **Fig. 3** — Japan four-panel plate (gold-shaded 2011–2013 window)
- [Manuscript — Results §3 Japan](CODAwork2026/Compositional_Monitoring_2026.pdf)
- 📂 Raw output: [`cnt_JPN.json`](CODAwork2026/data_outputs/per_country_json/cnt_v3/cnt_JPN.json)
- 📂 Japan plates: [`JPN_stage0.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_stage0.pdf), [`JPN_stage1.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_stage1.pdf), [`JPN_stage23.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_stage23.pdf), [`JPN_cnq.pdf`](CODAwork2026/data_outputs/per_country_pdfs/JPN_cnq.pdf)

### Slide 9 · Japan — course on the simplex *(case study 2, beat 2)*
The Helmsman trajectory at full size — **course directness 0.09**, the loop-and-reorganise archetype. Trajectory revisits and reroutes. Compared directly to Germany's smooth arc, Japan's course shows a system *searching* for a new composition rather than walking a planned one — a basin being explored, not a direction being followed.

- **Fig. 6 (Japan panel)** — per-country navigation chart at full legibility
- 🔭 **Projector matches this slide:** click **JPN**, then **BARY**, then **SHOCK**, then **ALIGN** for the CoDa-centred view.

### Slide 10 · United Kingdom — share-and-work view *(case study 3, beat 1)*
Coal exit as regime change. Between 2012 and 2020, coal goes from > 30 % to < 2 %. A true regime change, not a drift. The Power Share view tells you *how the displaced structural work was absorbed* — wind, solar, biomass, other renewables each took portions. Multiple yeast moments across the exit period; no single replacement carrier.

- **Fig. 4** — UK four-panel plate
- [Manuscript — Results §4 United Kingdom](CODAwork2026/Compositional_Monitoring_2026.pdf)
- 📂 Raw output: [`cnt_GBR.json`](CODAwork2026/data_outputs/per_country_json/cnt_v3/cnt_GBR.json)
- 📂 UK plates: [`GBR_stage0.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_stage0.pdf), [`GBR_stage1.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_stage1.pdf), [`GBR_stage23.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_stage23.pdf), [`GBR_cnq.pdf`](CODAwork2026/data_outputs/per_country_pdfs/GBR_cnq.pdf)

### Slide 11 · United Kingdom — course on the simplex *(case study 3, beat 2)*
The Helmsman trajectory at full size — **course directness 0.36**, the jump-and-return archetype. The course leaves the coal vertex sharply, then settles toward a new mix. Distinct from Germany's continuous arc, distinct from Japan's looping search. Regime change as one decisive displacement followed by re-stabilisation. Three transitions, three archetypes, one geometry.

- **Fig. 6 (UK panel)** — per-country navigation chart at full legibility

### Slide 12 · Cross-country signature — 5 of 9 reproduce the pattern
Same instrument, nine EMBER countries. The deceptive-drift signature fires in **5 of 9** — **AUS, CHN, GBR, IND, JPN**. It does *not* fire in DEU at annual grain, FRA, USA, or the World aggregate. A useful detector should not fire everywhere; discrimination is itself evidence the protocol is reading real structure.

- **Fig. 5** — nine-country cross-country signature plate (top-10 activation moments + yeast-moment counts + Activation Coefficients + helmsman flips)
- [Manuscript — Results §5 (cross-country signature)](CODAwork2026/Compositional_Monitoring_2026.pdf)
- 📂 All nine countries: [`per_country_json/cnt_v3/`](CODAwork2026/data_outputs/per_country_json/cnt_v3/)

### Slide 13 · What the stack answers — closing synthesis
**WHAT** carriers are big · **WHO** is at the wheel · **WHEN** the steering changes · **HOW MUCH** work each carrier did · **WHY** a small carrier mattered. One observable, five questions, one reproducible object. *The stack does not replace interpretation. It gives interpretation a reproducible object.*

- [Manuscript — Discussion + Conclusions](CODAwork2026/Compositional_Monitoring_2026.pdf)
- **AI Use Declaration (HUF-STD-001 v1.1)** — research design, mathematical content, code, and scientific responsibility remain with the named author. AI assistants used for drafting, sweeps, and reviews. Author retains full responsibility.
- Then the cinema scroll runs as Q&A backdrop. Pause it anywhere.

---

## Things not in the deck but available

The 13-slide deck deliberately omits the MC-4 falsifiability slide and the "inspect the instrument" closer to keep the talk under nine minutes. Both still live in the repo:

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
  - **SHOCK** — combine with any mode: tints plate outlines red proportional to Aitchison-step magnitude.
  - **FRONT / SIDE / TOP / ISO** — fixed camera angles.
- **Bottom** — TIME slider scrubs year-by-year. Drag to pause anywhere.

### Try this on Japan (matches Slides 8–9 — the Japan pair)

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

*The instrument reads.   The expert d