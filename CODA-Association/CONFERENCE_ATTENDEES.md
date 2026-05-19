# CoDaWork 2026 attendees — start here

**Welcome.** This page is the entry point for anyone in (or watching remotely from) the CoDaWork 2026 audience who wants to follow along, look at the data live, or explore the Hˢ framework after the talk.

- **Talk:** *Compositional monitoring of energy-mix drift on the simplex* — Peter Higgins, Rogue Wave Audio, Markham, Ontario
- **Conference:** CoDaWork 2026, 11th International Workshop on Compositional Data Analysis · Coimbra, Portugal · 1–5 June 2026
- **Repository:** https://github.com/PeterHiggins19/higgins-decomposition
- **Restore checkpoint:** [`POINT_OF_RESTORE_2026-05-19.md`](POINT_OF_RESTORE_2026-05-19.md)

---

## 🎬 The five-piece bundle (follow along)

| Piece | Direct link (GitHub web view) | What it is |
|---|---|---|
| **1. Manuscript (peer-reviewable)** | [`Compositional_Monitoring_2026.pdf`](CODAwork2026/Compositional_Monitoring_2026.pdf) | 25-page paper with cover, TOC, Nature-style structure, 6 figures, 28 external + 11 repository references. The full argument the talk condenses. |
| **2. Talk deck (the story)** | [`CodaWork2026_FinalTalk_2026-05-17.pdf`](CODAwork2026/data_outputs/CodaWork2026_FinalTalk_2026-05-17.pdf) | 22-slide narrative deck. Open and follow at your own pace. |
| **3. Cinema scroll (the engine's raw output)** | [`CodaWork2026_PremierDataOutput_2026-05-13.pdf`](CODAwork2026/data_outputs/CodaWork2026_PremierDataOutput_2026-05-13.pdf) | 325-page master PDF. Master cover + 9 country sections × 6 plates each (cover · Stage 1 Section · system course plot · helmsman · ILR-Helmert Triplet · CNQ dashboard). Hash-chained to the EMBER input CSVs. |
| **4. Interactive HTML projector (live, in your browser)** | [`codawork2026_projector.html`](CODAwork2026/data_outputs/codawork2026_projector.html) | Three projection modes (RADAR / BARY / ALIGN) + SHOCK overlay. **See "How to run the projector" below — it requires download or GitHub Pages.** |
| **5. Engine source code** | [`HCI-CNT/engine/cnt.py`](../HCI-CNT/engine/cnt.py) (v3.2.0) · [`cnt.R`](../HCI-CNT/engine/cnt.R) (v3.1.0) | Deterministic Compositional Navigation Tensor engine in Python and R. |

## 📥 If you can't see the screen / are attending remotely

You can run everything in the talk yourself, locally, in two minutes:

1. **Read the manuscript first** — [`Compositional_Monitoring_2026.pdf`](CODAwork2026/Compositional_Monitoring_2026.pdf). The cover page lays out the contribution; the abstract is on page 3; jump to Results on page 5 for the case studies.
2. **Open the talk deck PDF** — [`CodaWork2026_FinalTalk_2026-05-17.pdf`](CODAwork2026/data_outputs/CodaWork2026_FinalTalk_2026-05-17.pdf). Follow slide by slide while listening (audio/video stream depending on conference setup).
3. **Run the interactive projector** — see next section.

## 🌐 How to run the projector

The projector is a single self-contained HTML file with embedded data. No server, no install, no network call. Three options:

**Option A — GitHub Pages (no download required)** *if hosted at github.io*
Click here once GitHub Pages is enabled:
`https://peterhiggins19.github.io/higgins-decomposition/CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html`

**Option B — local download** *(works on any device with a browser)*
1. Click the projector link above.
2. On the GitHub web page, click the **"Download raw file"** button (or right-click → Save As).
3. Open the downloaded `codawork2026_projector.html` in any modern browser (Chrome / Firefox / Safari / Edge — all work).
4. The 3-D view should open immediately. No further setup.

**Option C — clone the whole repo**
```
git clone https://github.com/PeterHiggins19/higgins-decomposition.git
cd higgins-decomposition/CODA-Association/CODAwork2026/data_outputs/
open codawork2026_projector.html       # macOS
xdg-open codawork2026_projector.html   # Linux
start codawork2026_projector.html      # Windows
```

### Using the projector (90-second tour)

When it opens you'll see the 3-D Hˢ manifold for the first country in the corpus (CHN — China). The HUD has:

- **Top-left** — title + PROJECTION info panel (the math being applied to what you're seeing). Toggle off with the **PROJ** button if you want a clean view.
- **Top-right** — controls. Click a country (CHN / DEU / FRA / GBR / IND / JPN / USA / WLD) to switch dataset.
- **ORBIT** — slow auto-rotation. Click off to drag-rotate with your mouse.
- **TRAILS / LABELS / GHOST / COLOR** — display toggles.
- **PROJ** — toggle the PROJECTION info panel.
- **BARY** — switch to **BARYCENTER TRAJECTORY** mode. The plate-centres trace the composition's path through the simplex's principal 2-D subspace (engine v3.2.0 ILR-Helmert PCA).
- **ALIGN** — switch to **BARYCENTER-ALIGNED** mode. The trajectory is forced onto the central z-axis; what remains is pure compositional shape variation around each year's own centroid. This is the CoDa-standard "centred" view.
- **SHOCK** — overlay that tints plate outlines red proportional to the Aitchison-step distance from the previous year. External shocks light up.
- **FRONT / SIDE / TOP / ISO** — fixed camera angles.
- **Bottom** — TIME slider scrubs year-by-year. Drag to pause anywhere.

### Try this (Japan, 2011–2014)

1. Click **JPN** to load Japan.
2. Click **BARY**. Watch what the plate centres do in 2011 → 2012 (Fukushima shock) and especially through 2013 → 2014–2015 (multi-year reorganisation toward solar + renewables).
3. Click **ALIGN**. The bend is removed; the polygon shape variation per year is what you see now — the CoDa-correct *centred* view.
4. Click **SHOCK**. The shock years light up red.
5. Read the PROJECTION info panel for the math. It updates live with the active mode.

## 🔬 If you want to verify a result

The corpus is fully reproducible from the public EMBER CSV data:

- **Raw EMBER source** — https://ember-energy.org (Creative Commons Attribution 4.0)
- **Engine** — [`HCI-CNT/engine/cnt.py`](../HCI-CNT/engine/cnt.py) (CNT v3.2.0, schema v3.2.0). The CoDaWork 2026 corpus was produced with v3.1.0; the projector consumes a v3.2.0 forward-compatibility block (`navigation_2d`) for ILR-Helmert PCA barycenter coordinates.
- **Conference corpus JSONs** — [`CODAwork2026/data_outputs/per_country_json/cnt_v3/`](CODAwork2026/data_outputs/per_country_json/cnt_v3/) (9 countries × ~300 KB JSON each, hash-chained to EMBER inputs).
- **Supplementary Information** — [`papers/codawork2026/manuscript/SUPPLEMENTARY.md`](../papers/codawork2026/manuscript/SUPPLEMENTARY.md). Reproduction commands and SHA-256 hashes in §S4.
- **Engine standards** — [HUF-STD-001 v1.1](../huf-gov/standards/HUF_PUBLICATION_STANDARDS.json) (Publication) · [HUF-STD-002](../huf-gov/standards/HUF_TENSOR_TRAIN_IO_STANDARD.json) (Tensor Train I/O) · [HUF-STD-003](../huf-gov/standards/HUF_HS_LINEAR_ALGEBRA_FOUNDATIONS.json) (Linear Algebra Foundations).

## 🤝 If you want to challenge the result

The manuscript names four explicit defeat paths. The repository is open; the data is public; the code is Apache-2.0. From the Discussion section:

1. **Prior-art defeat** — show that an existing CoDa or environmental-monitoring framework already treats compositional structure as a primary operational monitoring category, combined with Aitchison-native change detection at the carrier level into one observable stack. Closest adjacent prior art identified: Morais, Thomas-Agnan & Simioni (2018); Arata & Onozaki (2017). Neither combines all three to our reading; a closer match is welcome.
2. **Metric defeat** — show that the protocol's verdicts reverse under a different valid simplex distance.
3. **Case defeat** — show that the 5-of-9 deceptive-drift signature is an artefact of preprocessing, carrier definition, or null-model choice.
4. **Category defeat** — show that compositional monitoring is most accurately an application note inside existing CoDa rather than a distinct monitoring category.

Open an issue on the repository or contact the author at PeterHiggins@RogueWaveAudio.com.

## 📚 Where to read next

| Read | If you want… |
|---|---|
| [`POINT_OF_RESTORE_2026-05-19.md`](POINT_OF_RESTORE_2026-05-19.md) | The milestone document — what was locked, what stays at v3.1.0, what the v3.2.0 functionality adds |
| [`CODAwork2026/README.md`](CODAwork2026/README.md) | The full folder map of conference materials |
| [`CODAwork2026/data_outputs/README.md`](CODAwork2026/data_outputs/README.md) | Run-the-presentation walkthrough + the projector v2.0 documentation |
| [`../papers/codawork2026/manuscript/SUPPLEMENTARY.md`](../papers/codawork2026/manuscript/SUPPLEMENTARY.md) | Supplementary tables (9-country corpus + sensitivity analyses + reproduction commands) |
| [`../HCI-CNT/handbook/`](../HCI-CNT/handbook/) | Hˢ handbook (Volumes I–IV: theory, engine, atlas, quaternion view) |
| [`../HCI-CNT/handbook/GLOSSARY.md`](../HCI-CNT/handbook/GLOSSARY.md) | Canonical Hˢ glossary v2.0 |
| [`../EXPERIMENTS_JOURNAL.md`](../EXPERIMENTS_JOURNAL.md) | The chronological record of every Hˢ experiment, with engine-version provenance |
| [`../README.md`](../README.md) | The top-level repository README |

## 📜 Citation

If you cite the manuscript:

> Higgins, P. (2026). *Compositional monitoring of energy-mix drift on the simplex.* Prepared for CoDaWork 2026, Coimbra, Portugal. Available at https://github.com/PeterHiggins19/higgins-decomposition

If you cite the engine:

> Higgins, P. (2026). *HCI-CNT — Compositional Navigation Tensor engine, version 3.2.0.* https://github.com/PeterHiggins19/higgins-decomposition · Apache-2.0.

Or use the BibTeX in [`../CITATION.cff`](../CITATION.cff).

## 📝 Licensing

- **Code:** Apache-2.0 (see [`../LICENSE`](../LICENSE))
- **Documentation, figures, and data outputs:** CC BY 4.0 (see [`../LICENSE-DOCS`](../LICENSE-DOCS))
- **EMBER raw data:** CC BY 4.0 (EMBER's licence) — https://ember-energy.org

Free to use, free to cite, free to remix with attribution.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*The mathematics is not new; the monitoring application may be.*

*Welcome to CoDaWork 2026. Thanks for being in the room — or watching from anywhere.*
