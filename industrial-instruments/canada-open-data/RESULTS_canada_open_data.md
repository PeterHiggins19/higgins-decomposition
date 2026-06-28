# What Hˢ sees when it reads all of Canada's open data at once (INTERNAL · DEMO)

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. 2026‑06‑24. A small,
honest demonstration built for the Government of Canada: point the Hˢ compositional instrument at **Canada's
entire open‑data estate** and read its shape. Real catalogue metadata, deterministic, hash‑receipted. Descriptive
— *what the data structure is* — never a political judgment. Receipt `209a8559`. Internal; Peter is the sole
gate; nothing transmitted.*

---

## The data

Every dataset in Canada's official open‑data catalogue, read live from the **open.canada.ca** CKAN API
(`package_search` facets, fetched 2026‑06‑24): **47,462 datasets.** Four facets are each read as a composition —
who holds the data (department/jurisdiction), how it is shaped (format), at what level (jurisdiction), and in
what collection.

## What the instrument reads

| composition | arrow (dominant) | top three | effective dimension | concentration (HHI) |
|---|---|---|---|---|
| **department / jurisdiction** | Natural Resources (NRCan) | NRCan 22.4% · StatCan 22.3% · Health 6.5% | ~15 of 40+ | 0.12 |
| **format** | HTML | HTML 29% · CSV 14% · XML 12% | ~11 of 26 | 0.14 |
| **jurisdiction level** | federal | federal 75% · provincial 24% · municipal 0.6% | ~1.8 of 4 | 0.62 |
| **collection** | primary | primary 29% · geogratis 21% · publication 16% | ~5.7 of 15 | 0.20 |

## The surprises (and they are real)

**1. Two mandates *are* the open‑data estate.** Natural Resources Canada (10,247) and Statistics Canada (10,203)
together hold **43%** of all 47,462 datasets — from **two** of more than a hundred contributing bodies. The
"arrow of intent" of Canada's open data points squarely at *geoscience + national statistics*; everything else is
the long tail.

**2. Output does not track size.** **Yukon** — population ~45,000 — has published **2,901** datasets, about
**three times Ontario's 988**, and far above its ~0.1% share of the national population. Open‑data output is a
**mandate‑and‑culture** signal, not a population or economy signal. A headcount of provinces would never show
this; the *composition* does.

**3. The "open" estate is more metadata than data.** HTML (landing/metadata pages) is the single largest format
tag (29%); the directly machine‑readable core (CSV + XLSX + JSON + GEOJSON) is a smaller, identifiable share. The
catalogue is larger than the volume of immediately‑usable data within it.

**4. It is concentrated — so the read, not the count, is the right lens.** The effective dimension is far below
the part count: ~15 "equivalent equal departments" out of 40+, ~11 equivalent formats out of 26, ~1.8 equivalent
jurisdiction levels out of 4. A few parts carry most of the mass — exactly the situation where a compositional
instrument earns its keep over a raw inventory.

## Why this is a good demonstration *for government*

It uses **the government's own public data**, end to end, with a content receipt anyone can re‑compute — and it
shows the instrument doing something a dataset count cannot: naming *where the weight is*, *how concentrated the
estate is*, and *which signals are mandate‑driven rather than size‑driven*. The same read, pointed at a
department's internal data holdings or a process line, is the product. Here it simply reads Canada back to
itself.

## Honest fences

- **Descriptive, not political.** The shares, arrows, and effective dimensions are deterministic facts about the
  catalogue metadata. What they *mean* for policy is for the government to decide; the instrument reads, the
  expert decides.
- **Format caveat.** Format shares are over *resource‑format tags* (a dataset carries several), so they sum to
  more than 100% of datasets; HTML reflects landing/metadata pages, not data content.
- **Snapshot.** Counts are the 2026‑06‑24 fetch; the catalogue grows daily. Re‑run to refresh.
- **Top‑40 departments** cover ~96% of datasets; the residual tail is many small contributors.

*Cross‑refs: `README.md`, `canada_open_data_composition.py`, `AI_ASSIST.json`,
`../../huf-gov/doctrine/CANADA_DIVISION.md`. Source: https://open.canada.ca/data/en/dataset (CKAN API). Peter is
the sole gate; nothing posted.*

*Proof & Honesty Standard — counts real + receipted · read deterministic · descriptive not political · the expert decides.*
