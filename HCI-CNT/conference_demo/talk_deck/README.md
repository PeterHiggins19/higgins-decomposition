# CodaWork 2026 — talk deck source

The 10-slide PowerPoint for the 15-minute CodaWork 2026 talk, plus
its source SVGs and the regenerable build script.

| File | Purpose |
|---|---|
| `CodaWork2026_CNT_Talk.pptx` | Editable 10-slide deck |
| `CodaWork2026_CNT_Talk.pdf`  | Same deck, exported as PDF for review |
| `slide_*.svg`                 | Source SVGs (line-art, monochrome on dark background) |
| `build_deck.js`               | PptxGenJS build script |
| `slide-NN.jpg`                | Per-slide preview thumbnails |

## Deck outline

| Slide | Topic |
|---|---|
| 1 | Title |
| 2 | What CNT adds on top of the CoDa toolkit |
| 3 | CNT pipeline overview |
| 4 | Math step 1+2 — Closure + CLR (parallel views) |
| 5 | Math step 3 — Helmert ILR (shared foundation) |
| 6 | Math step 4 — Pairwise bearing (atan2 numerical comparison) |
| 7 | Math step 5 — Metric tensor M²=I (CNT addition) |
| 8 | Math step 6+7 — Depth tower → period-2 attractor → IR class |
| 9 | CBS Cube — three orthogonal face projections |
| 10 | One-picture summary — the full hash-traceable pipeline |

## Editing

Edit any `.svg` file directly in Inkscape, Illustrator, or any vector
editor. To rebuild the deck after edits:

```bash
NODE_PATH=/usr/local/lib/node_modules_global/lib/node_modules \
  node build_deck.js
```

Output: `CodaWork2026_CNT_Talk.pptx`.

## Speaker notes

Each slide has speaker notes embedded (right-click → notes view in
PowerPoint). For the full timing plan, audience guidance, and
15-question Q&A study list, see
[`../CODAWORK2026_TALK_PLAN.md`](../CODAWORK2026_TALK_PLAN.md).

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
