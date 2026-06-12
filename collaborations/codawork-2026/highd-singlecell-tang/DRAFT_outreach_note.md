> **DRAFT — NOT SENT.** For Peter's review and gate. Verify the recipient's current email and the fairness of the framing before any contact. Per RWA‑001.

**To:** Dr. Nelson Tang — `nelsontang@cuhk.edu.hk` (cc Jinghan Huang)
**From:** Peter Higgins — `PeterHiggins@RogueWaveAudio.com`
**Subject:** Your CoDaWork 2026 CoDA‑hd talk — an exact, deterministic counterpart to the SVD step

Dear Dr. Tang,

Your CoDaWork 2026 talk on bringing CoDA to single‑cell RNA‑seq — the CoDA‑hd package, the CLR + partial‑SVD pipeline, and especially the sample‑specific SGM treatment of dropout zeros — was a genuinely useful contribution to the high‑dimensional problem.

I develop Hˢ (Higgins Decomposition), a deterministic compositional instrument whose tiling does **lossless** high‑dimensional reconstruction — proven to a million parts at machine precision — by using a hierarchy (a phylogeny, ontology, or lineage tree) as its atlas, in seconds and with a content hash on every run. Where your truncated SVD is a fast, close *approximation* to full log‑ratio analysis, Hˢ offers an *exact*, byte‑reproducible reduction wherever such a hierarchy is available — so the two could be compared directly on the same matrices, at comparable cost. I would also be interested to compare your SGM zero scheme against Hˢ's own zero‑treatment stage on the same sparse data; that seems like a clean, mutually informative exercise. Hˢ ships an R port that is byte‑identical to its Python, so the whole comparison could stay in R alongside CoDA‑hd.

I should be candid about the boundary: Hˢ's trajectory read (its "helmsman", the gene steering each step) needs an ordering, so on scRNA‑seq it would only apply along a pseudotime or lineage you already have. The part I think is immediately useful is the **exact high‑D reduction and the zero‑treatment comparison**, not the trajectory read.

I am offering an instrument, not a reanalysis — I would never need to hold your data. If a comparison were useful, I would run it on a matrix you prepare and return the outputs and a receipt for you to judge. And mostly I would value your feedback: scrutiny from someone working at true single‑cell scale is the best test this kind of method can get.

With appreciation for the talk,

Peter Higgins
Rogue Wave Audio / Binaural Test Lab
Markham, Ontario, Canada
`PeterHiggins@RogueWaveAudio.com`

*Hˢ is deterministic and hash‑chained; it reads compositional geometry, and the domain expert decides what it means. Developed with AI assistance under the HUF publication standard; all claims are mine.*
