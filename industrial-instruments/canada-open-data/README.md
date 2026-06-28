# Canada open‑data composition — an Hˢ demo for the Government of Canada (INTERNAL · DEMO)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑24. A small,
self‑contained demonstration: point the Hˢ compositional instrument at **all of Canada's open data** and read its
shape — using the government's **own public catalogue**, deterministically, with a content receipt. Part of the
**Canada Division** (`../../huf-gov/doctrine/CANADA_DIVISION.md`). Internal; **no endorsement implied or sought**;
Peter is the sole gate; nothing transmitted.*

---

## The idea

A government's open‑data catalogue is itself a **composition** — datasets distributed across departments,
formats, jurisdictions, and collections. Nobody reads it that way; they count it. Hˢ reads the *shape*: which
mandate carries the weight (the arrow), how concentrated the estate is (effective dimension), and which signals
are mandate‑driven rather than size‑driven. It is the smallest possible proof, on data Canada already publishes,
that the instrument sees something a headcount cannot.

## The result in one line

Reading all **47,462** datasets (open.canada.ca, 2026‑06‑24): **two mandates — Natural Resources + Statistics
Canada — are 43% of the entire estate**; **Yukon out‑publishes Ontario 3‑to‑1**; the catalogue is **more metadata
than machine‑readable data**; and its **effective dimension (~15 departments, ~11 formats) is far below the part
count** — so the composition, not the count, is the right lens. *(Receipt `209a8559`; full read in
[`RESULTS_canada_open_data.md`](RESULTS_canada_open_data.md).)*

## What's here

| file | what it holds |
|---|---|
| [`RESULTS_canada_open_data.md`](RESULTS_canada_open_data.md) | the read, the surprises, the honest fences |
| `canada_open_data_composition.py` | the runner (real CKAN facet counts → the Hˢ compositional read; needs numpy) |
| `AI_ASSIST.json` | the standard onramp node |

## How to verify it

The counts are copied verbatim from the public CKAN API; re‑fetch to refresh:
`https://open.canada.ca/data/api/3/action/package_search?rows=0&facet.field=["organization","res_format","jurisdiction","collection"]`.
Then `python canada_open_data_composition.py` reproduces every number to the receipt.

## Honest scope

- **Descriptive, not political.** Deterministic facts about the catalogue metadata; meaning is the government's to
  decide. The instrument reads; the expert decides.
- **T1:** the engine + the receipted read (`209a8559`). **T2:** the framing as a government demonstration.
  **T3:** any value/uptake. **No endorsement, no contact** — Peter is the sole gate.

*Cross‑refs: `../../huf-gov/doctrine/CANADA_DIVISION.md`, `../euv-lithography/`, `../README.md`. Source:
https://open.canada.ca/data/en/dataset. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — counts real + receipted · read deterministic · descriptive not political · the expert decides.*
