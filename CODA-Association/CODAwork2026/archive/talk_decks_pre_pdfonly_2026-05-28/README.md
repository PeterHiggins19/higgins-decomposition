# archive/talk_decks_pre_pdfonly_2026-05-28/

The 21-slide grayscale Presentation as it stood **just before** the 2026-05-28 switch to **PDF-only delivery** + the layout-expansion rebuild.

## What's here

- **`CodaWork2026_Presentation_2026-05-27.pptx`** — the prior PPTX (3.3 MB, 21 slides, Letter landscape 11 × 8.5). Built with `outputs/combined_build/build_grayscale_deck_v10.py`. Generated 2026-05-27. The last version where the PPTX shipped as a public artifact.
- **`CodaWork2026_Presentation_2026-05-27.pdf`** — the prior PDF (2.9 MB), rendered from that PPTX via LibreOffice. Same 21-slide content as the 2026-05-28 active PDF, but with the older v10 layout (figures under-using canvas width; some sub-7-pt fonts at distance).

## What changed in the 2026-05-28 rebuild

Two coordinated changes, both per Peter (2026-05-28):

1. **PDF-only delivery.** "*the PowerPoint can be archived and no more PowerPoint, only pdf — the complications with PowerPoint software make pdf just that much easier and faster to work with.*" The PPTX continues to exist as a build scaffold inside the v11 builder, but it is **not shipped**; it is generated, converted to PDF, then discarded at the workspace boundary.
2. **Layout expanded to fully use the Letter-landscape canvas.** "*regenerate to utilize the expanded width real estate and make the slide even better to see at a distance now with 25 % more width space — pdf landscape matches the full frame of the display much better.*" Margins tightened 0.5 → 0.4 in (content width 10.00 → 10.20 in); figure widths bumped — share-and-work figures 9.60 → 10.20 (+6 %), method diagram 9.80 → 10.20 (+4 %), world-plate / Germany-plate trajectories 8.50 → 9.50 (+12 %), nav-chart trajectories 7.00 → 7.30 (+4 %), cross-country bar set 5.70 → 6.00 (+5 % — content-bounded by the multi-panel figure's intrinsic aspect). Fonts scaled up ~20 % throughout for distance reading; the formula on slide 4 and the Activation-Coefficient Consolas line on slide 2 were re-fit to one line each. Captions on slides 7 and 10 were tightened so they fit the new layout cleanly without 2-line wrap.

## Active replacement

[`../../data_outputs/CodaWork2026_Presentation_2026-05-28.pdf`](../../data_outputs/CodaWork2026_Presentation_2026-05-28.pdf) — same 21-slide arc, PDF-only, layout expanded.

## Builder lineage

Live: `outputs/combined_build/build_grayscale_deck_v11b.py` (workspace scratchpad, not in the repo — the PDF is the deliverable). The v10 builder remains in the same scratchpad for archival reference. No build scripts are shipped in the repo for the deck.
