# Language as a composition — Hˢ reads a tongue by its letters

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. The idea
that arrived with the Latin colophon: a **language is a composition.** A text's letter frequencies are parts
of a budget that sum to one — a point on the simplex — so the very same instrument reads a tongue's signature.
Tested on real parallel multilingual repo text; receipt `a3204a02ffa16446`. Honest-broker tiered; Peter is the
sole gate; nothing posted.*

---

## The setup (recursion: the system that spoke Latin now reads language)

Take the same passage in several languages (the UN-6 summaries and the CoDa handout, English / Spanish /
French, plus the Latin colophon), reduce each to its **26-letter frequency composition** (de-accented to
`a–z`), and read it with closure + clr. The content is held constant across languages, so what remains is the
**language's own letter signature.**

## What it found (real, receipted)

- **Each language has a signature.** The helmsman letter is `e` in all (correct — `e` dominates Latin-script
  text); the runners-up differ meaningfully (Spanish lifts `o`, French lifts `t`).
- **The Romance languages cluster — measured.** Aitchison distance: **ES↔FR = 1.24**, smaller than **EN↔ES =
  2.06** and **EN↔FR = 2.07**. Spanish and French are nearest neighbours; English is the outlier. Hˢ recovered
  a real linguistic fact from letter frequencies alone.
- **The signature is invariant to *how much* text — above a floor.** Subsampling the *same* English text:
  distance to the full signature is **1.35 at 20%, 0.51 at 50%, 0 at full** — the language is read, not the
  amount. At **5% it breaks (34)** — too few letters, structural zeros. That breakdown is **the same
  knowable-sample floor the stress sheet found** (max-power / `D*(N)`): below the floor, manufactured; above
  it, the signature locks. Language obeys the same law as everything else here.
- **Classify a text by its tongue** (locked discriminant on letter-composition): **53%** on tiny held-out
  windows — modest, and *honestly* so: the close Romance pair ES/FR is exactly where it confuses, consistent
  with their small distance. More data would lift it.

## Honest limits

- **Latin is flagged unreliable.** The colophon sample is short and has *structural zeros* (k, w, y rare in
  Latin), which blow up the log-ratio — a real reading needs a proper Latin corpus. This is the zero-handling
  limit (cf. E-21), reported, not hidden. Its top letters (`e, t, i`) are shown as a hint only.
- **Different scripts (Cyrillic ru, CJK zh, Arabic ar) are a different alphabet composition** — out of scope
  for this a–z reader; they would each be read on their own character simplex.

## Why it is interesting (and where it fits)

Letter-frequency analysis is old (cryptanalysis, authorship attribution, language ID). What's new here is only
the framing and the discipline: a language is *literally* a composition, so the **whole instrument applies
unchanged** — the relational read, the length-invariance (= common-mode rejection of text amount), the locked
discriminant, the knowable-sample floor. The recursion is pleasing: the system that struck its colophon **in
Latin** can turn around and read Latin — and English, and Spanish — as compositions, with the same receipts.

*Cross-refs: `language_as_composition.py`, `LANGUAGE_AS_COMPOSITION_RESULTS.json`,
`AURUM_PERCUSSUM_colophon_latinum.md`, `KNOW_THE_KNOWABLE.md` (the sample floor),
`../papers/locked-discriminant/THE_LOCKED_DISCRIMINANT_PRINCIPLE.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — a real linguistic fact recovered (Romance clustering) · length-invariance shown with its floor · Latin flagged unreliable, not faked · prior art (letter-frequency ID) acknowledged · experts decide.*
