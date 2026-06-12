# Archive — talk decks superseded by the 10-slide compressed final

**Archived:** 2026-05-20 · **Original successor (when this folder was created):** the 10-slide compressed deck.

> **📌 Update 2026-05-24** — the 10-slide deck has itself since been archived. The current active conference deck is the **13-slide expanded final talk** at [`../../data_outputs/CodaWork2026_FinalTalk_13Slide_2026-05-24.pptx`](../../data_outputs/CodaWork2026_FinalTalk_13Slide_2026-05-24.pptx); the 10-slide predecessor lives in the sibling archive folder [`../talk_decks_pre_13slide_2026-05-24/`](../talk_decks_pre_13slide_2026-05-24/). The rest of this README documents what it documented at the time of archival; the "Active talk deck" references below refer to the 10-slide deck (the active deck *then*), now itself archived. For the full chain see [`../README.md`](../README.md).

These files are the **refinement trail** that led to the 10-slide compressed final talk. They are preserved for lineage and reproducibility, **not** for use at CoDaWork 2026. The active talk deck and its speaking script live one level up at [`../../data_outputs/`](../../data_outputs/) and [`../../SPEAKING_SCRIPT_10slide.md`](../../SPEAKING_SCRIPT_10slide.md).

## What's in here

| File | Date | Slides | Role at time of writing |
|---|---|---|---|
| `CodaWork2026_FinalTalk_2026-05-17.pptx` / `.pdf` | 2026-05-17 | 22 | The original full narrative final-talk deck. Story arc with full per-country navigation slides, MC-4 falsifiability, and the "Inspect the instrument" closer. Superseded when the talk was compressed for the 15-minute conference slot. |
| `CodaWork2026_FinalTalk_12Slide_2026-05-20.pptx` / `.pdf` | 2026-05-20 | 12 | Intermediate compression — produced from the ChatGPT-prepared `CompressionPlan.json`. Kept the MC-4 falsifiability slide and the closer. Superseded same day by the 10-slide final after Peter's directive to "drop slide 11 and 12 entirely, place full contact details on slide 1". |
| `CodaWork2026_FinalTalk_12Slide_CompressionPlan.json` | 2026-05-20 | — | The 22→12 compression plan (ChatGPT-prepared, Claude-executed). Records the slide-by-slide rationale for the first compression pass. |
| `build_final_talk.py` | 2026-05-17 | — | python-pptx builder for the 22-slide narrative deck. |
| `build_final_talk_v2.py` | 2026-05-17 | — | Iteration of the 22-slide builder (image-overlap fixes on Germany/Japan/UK case slides). |
| `build_final_talk_12slide.py` | 2026-05-20 | — | python-pptx builder for the 12-slide intermediate compression. |
| `SPEAKING_SCRIPT.md` | 2026-05-19 | — | Beat-by-beat speaking script for the **22-slide** deck. Slide numbers and beat references in this file apply to the 22-slide narrative; using it against the 10-slide deck will mislead. The current speaking script is [`../../SPEAKING_SCRIPT_10slide.md`](../../SPEAKING_SCRIPT_10slide.md). |

## Why these are archived, not deleted

Lineage. The 22-slide deck was the full pedagogical narrative; the 12-slide deck was the first compression pass; the 10-slide deck is the final stage with MC-4 + the closer absorbed into the manuscript and footer. Reviewers tracing the talk's evolution should find each stage intact.

Reproducibility. Each builder script in this folder regenerates its own deck deterministically from the corpus in `../../data_outputs/per_country_json/`. The story arc and figure references hold across the three stages; only the slide count and beat weighting differ.

## What replaced these

- **Active talk deck:** [`../../data_outputs/CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx`](../../data_outputs/CodaWork2026_FinalTalk_10Slide_2026-05-20.pptx) — 10 slides, ~8 min spoken, slides 6/7/8 (Germany/Japan/UK) weighted at 75 sec each. Full contact details on slide 1; MC-4 falsifiability and "Inspect the instrument" closer absorbed into the manuscript and slide-10 footer.
- **Active builder:** [`../../data_outputs/build_final_talk_10slide.py`](../../data_outputs/build_final_talk_10slide.py).
- **Active speaking script:** [`../../SPEAKING_SCRIPT_10slide.md`](../../SPEAKING_SCRIPT_10slide.md).

## The manuscript still carries the full apparatus

Both MC-4 falsifiability (3 conjuncts + 4 defeat paths) and the "Inspect the instrument" closing posture live in [`../../Compositional_Monitoring_2026.pdf`](../../Compositional_Monitoring_2026.pdf). The 10-slide talk performs the argument; the manuscript supplies the evidence depth that the older 22-slide deck had to do verbally.

---

*The instrument reads.   The expert decides.   The hashes carry the receipts.   The vocabulary holds the line.*
*Old versions held here so the new ones can be trusted as current.*
