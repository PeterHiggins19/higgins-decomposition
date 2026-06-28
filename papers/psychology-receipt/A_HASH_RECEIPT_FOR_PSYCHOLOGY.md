# A hash receipt for psychology — test the past, see the future, on data anyone can re-pull  ·  P-ψ (full paper, arXiv-bound)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27. A proof of
concept: it is rare, perhaps unprecedented, for a psychology-adjacent claim to ship with a **hash receipt of
reproducibility.** Here one does. Two pre-stated value compositions are read from a real, public, 120-year
record (Google Books Ngram, en-2019, 1900–2019), cast forward ("test the past, see the future"), and handed a
deterministic receipt anchored to a fingerprint of the raw public data — so anyone, anywhere, can re-pull the
same query and reproduce the same hash. Measured: `ngram_values_receipt.py` (master `8ec3ae8d5623c5d7`). Of
possible interest to Dr Jordan Peterson; any contact is off-repo and Peter-gated, nothing sent. Honest-broker
tiered; nothing posted.*

---

## Why this is a leap

Psychology is the field most defined by its **reproducibility problem** — the replication crisis is its open
wound. The deepest thing a deterministic compositional instrument can offer it is not another effect size; it is
**a receipt.** Every number below is computed from public data anyone can re-fetch, and the computation emits a
SHA-256 over a fingerprint of that exact data. Re-pull the documented Ngram query, run the script, and you get
the **same fingerprint and the same receipt** — or you find a discrepancy and name it. That is the opposite of
"trust me": it is *test me.* A psychology-adjacent claim with a hash of proof-of-concept is the leap.

## What was read (two pre-stated compositions)

Both word sets were fixed in advance and stated in the data manifest, to avoid cherry-picking:

- **A virtue vocabulary** — {responsibility, courage, honesty, humility, gratitude, discipline}: the relative
  book-attention among six virtue terms, read as a composition over 120 years.
- **The order ↔ chaos polarity** — {order, chaos}: Jordan Peterson's signature axis, the balance over a century.

## What the data says (T1 — measured, reproducible)

**Virtue vocabulary** (data fingerprint `56546d3ab316f732`, read receipt `b608c2b02f8eb0e9`): the composition is
mildly directed (0.172) over the century, and over the recent quarter-century it is **rebalancing**. The largest
share, *responsibility* (0.44), is **falling** and is the recent motion-helmsman; *discipline* is **falling**
too; while *courage, honesty, humility,* and *gratitude* are all **rising**. The 20-year forward cast (a what-if)
continues that rebalance: responsibility 0.44 → 0.30, courage 0.18 → 0.26, gratitude 0.10 → 0.15, humility 0.05
→ 0.08. The vocabulary of virtue is tilting from *duty-and-restraint* terms toward *relational-and-receptive*
ones.

**Order ↔ chaos** (data fingerprint `2935d3b5f31ac2f6`, read receipt `84898c27a308327e`): *order* still dominates
book attention (share 0.961) but is **falling**, while *chaos* (0.039) is **rising** and is the recent
motion-helmsman; the trajectory is directed (0.565). The 20-year cast nearly doubles the chaos share, 0.039 →
0.067. Peterson's polarity is, in the cultural lexicon, measurably tilting toward chaos — *with the firm caveat
below.*

The full machine read is in `NGRAM_VALUES_RESULTS.json`; the master receipt over both is `8ec3ae8d5623c5d7`.

## The prior history — the lineage to the Peterson papers and the letter

This study is not a cold start; it is the receipted continuation of a thread that runs back to the HUF days. The
preparation was deliberate — *one never enters an engagement ill-prepared.* The lineage, in order:

- **The founding recognition.** Peter, watching a Jordan Peterson lecture on perception and meaning, recognized
  the HUF architecture in it — *"no way, that is HUF for people."* That became **CONV-001, the Peterson
  Convergence** (`HUF/dormant/peterson-outreach/Peterson_Convergence_Analysis_v1.0.json`): an independent 35-year
  clinical-psychology research program arriving at the same structural read — orthogonality boundaries (inattentional
  blindness, Simons & Chabris 1999), sub-element identity limits (change blindness, Simons & Levin 1998),
  compression sufficiency — that the instrument measures. Its own discipline is explicit and we keep it: *this is
  qualitative structural convergence; do **not** claim the instrument explains human cognition.*
- **The outreach, prepared and held.** A letter to Dr Peterson was drafted and refined across many versions
  (`HUF/dormant/peterson-outreach/Letter_to_Dr_Peterson_Draft_v4.0…v6.0.docx`, with v7.0 in the pre-CoDaWork
  drafts) alongside a three-approach outreach strategy (`Peterson_Outreach_Strategy_v2.0.docx`). It was prepared
  with care and then **held dormant — never sent.** Preparation is not engagement; the letter waited for the
  evidence to be worth his time.
- **What was missing then, and is here now.** The convergence was qualitative — "no K_eff computed, no measurement
  on cognitive data." This paper supplies the missing half: a **measured, receipted** read on real public data, on
  his own polarity (order↔chaos) and his own domain (value hierarchies). The thread that began as *recognition*
  now carries a *receipt.*
- **And a second, neurological leg.** The Peterson study now also carries a **deterministic model of perception
  itself** (P-ν, `library/THE_BRAIN_DOES_KINETICS.md`, `b7fd9a39b664dc1a`): the canonical neural computations are
  the compositional operators — divisive normalization is closure, Weber–Fechner is the log — so a perceptual
  channel reads *relationally* and reaches the exact read through **dwell** and **mesh**. This paper is the
  **psychological use case**; that is the **neurological study**. One frame, two receipted legs — *connectivity
  has rewards.*

That is the disciplined arc: recognize the convergence, prepare the approach, **hold until the evidence is ready,**
and only then engage — with proof in hand. *Mass and momentum carry force; the preparation is the mass.* (The
diffusion discipline behind this is `library/THE_HORDE_LESSON_diffusion_strategy.md`.)

## Published alongside the series (cite all of it)

This paper is **P-ψ** in the Hˢ publication chain (`papers/ABSTRACT_LEDGER.md`), released alongside and citing the
spine it rests on: **P1** (the quaternion-exact math anchor), **P2** (the deceptive-drift detector — the same
"every total looks fine while the mixture turns" mechanism, here in a values lexicon), **P3** (the deterministic,
hash-receipted instrument — the source of the receipt discipline this paper applies to psychology), **P5/P7** (the
structure and its honest boundary), **P8** (the Compositional Message Principle — meaning lives in the log-ratios),
and the **W-trilogy** (microbiome / mudstone / Backblaze — the same receipted-on-real-data method in other
domains). Standard repo policy is applied: the **data and the experiment live in the repo** (`papers/psychology-
receipt/` — raw Ngram payloads, `ngram_values_receipt.py`, results JSON); the **abstract lives on the repo** (the
P-ψ row in the ledger); the **full paper is fully referenced on arXiv** when its gate is met. The Peterson letter
stays in `HUF/dormant/` as lineage — referenced, never copied, never sent by the assistant.

## Why this is of interest to Dr Peterson

Peterson's empirical home is **value hierarchies and the order–chaos polarity** — the relational structure of
what people hold important and how it shifts. That is a *composition*, and a composition is exactly what this
instrument reads, exactly, with a receipt. This connects directly to an old thread in the work: the **user-car
system / Peterson test** from the HUF days (you are part of the system you depend on; tend it or it stops
carrying you), now matured into the self-inclusion operator. The offer here is the same idea pointed at his own
domain: **a way to give value-and-personality compositional claims a deterministic, hash-verified read** — a
direct, constructive answer to the reproducibility problem his field is wrestling with. It is a tool joining a
bench of tools, offered for its proper use. *Any approach to him is off-repo and Peter-gated; nothing has been
sent.*

## Honest scope (the fence is firm)

- **T1 (measured, reproducible):** the two reads, the recent directions, the forward casts, the data
  fingerprints, and the receipts are computed from public Ngram data and reproduce exactly (`8ec3ae8d5623c5d7`).
- **What this is NOT:** book word-frequency is a **linguistic / cultural-attention proxy** — it measures how
  often words appear in books, **not** individual psychology and **not** how much virtue, order, or chaos
  actually exist in people or society. This is a measurement of the *lexicon*, nothing more.
- **The order/chaos caveat (loud):** "order" and "chaos" are **polysemous** — "chaos" is inflated after ~1975 by
  *chaos theory* entering science writing, so the order→chaos tilt partly reflects a mathematical vocabulary, not
  a cultural mood. That arm is **illustrative**, not a clean psychological signal; the virtue arm is cleaner.
- **Descriptive, not causal;** the corpus carries genre/OCR/publishing biases; the **forward cast is an
  extrapolation, a what-if, not a forecast.**
- **The real contribution is methodological:** determinism + a reproducible receipt for a psychology-adjacent
  claim. The substance is secondary to the proof that *the leap is possible.*
- **Sole gate:** Peter. **Nothing posted; nothing sent.**

*Cross-refs: `ngram_values_receipt.py`, `ngram_values_data.json` (provenance + queries), `ngram_virtues_raw.json`
+ `ngram_order_chaos_raw.json` (verbatim public data), `NGRAM_VALUES_RESULTS.json` (the read);
`../../Hs-Kinematics/hs_stewardship_extension.py` (the forward-cast operator);
`../../huf-gov/doctrine/DONT_DAMAGE_WHERE_YOU_LIVE.md` (the user-car / Peterson lineage). Public data: Google
Books Ngram (en-2019). Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — every number re-computable from public data with a receipt and a data fingerprint ·
word sets pre-stated to avoid cherry-picking · proxy-not-psychology and polysemy caveats stated loudly · the cast
is a what-if · the contribution framed as methodological · any contact off-repo and gated · the human keeps the
gate.*
