# Hˢ is an extension of standard CoDa into dynamic systems analysis

*The canonical positioning. Every Hˢ/HUF/RWA work should align to the stance stated here. Written after an internal audit of how the corpus presents itself relative to standard compositional data analysis. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; recognition, not invention.*

---

## The stance, in one sentence

**Hˢ is an extension of standard CoDa into dynamic systems analysis, built entirely on the simplex geometry the CoDa community established — offered as an extension of that geometry, never as a replacement for, improvement on, or competitor to it.**

## What is CoDa's, and what the extension adds

The line is clean and we keep it clean:

- **CoDa's (the foundation — not ours):** the simplex and its Aitchison geometry; closure; the CLR/ILR transforms; the geometric mean and Aitchison distance; balances and the SBP; the variation matrix and the compositional biplot; the four decades of method and statistical theory (Aitchison 1982/1986; Egozcue & Pawlowsky‑Glahn; Hron; Martín‑Fernández; Filzmoser; Gloor; and the wider CoDaWork community).
- **The extension (what Hˢ adds, on top of that foundation):** a *temporal/longitudinal monitoring layer* — the trajectory read, the helmsman (which log‑ratio is driving), regime‑boundary detection, the EITT entropy invariance under geometric‑mean decimation, and a deterministic, hash‑chained, reproducible instrument so a compositional read is auditable. The mathematics is standard CoDa‑compatible geometry; the new contribution is the *dynamic monitoring application and the reproducible instrument*, not new simplex mathematics.

We do not say "CoDa has not developed X," "CoDa cannot do Y," or "CoDa missed Z." CoDa's scope was the geometry; the extension is into time. Both statements are true and neither diminishes the other.

## The static user is fully served — and left alone

The dynamic layer is **offered, never imposed.** A colleague whose data is a single snapshot or a cross‑section (no time axis), or who simply wants the standard analysis they already trust, gets exactly the standard CoDa apparatus and nothing more:

- **ternary diagram** (D=3 sub‑compositions), **CLR biplot** (Aitchison–Greenacre), **variation matrix**, **CLR‑PCA scree**, **balance dendrogram** — computed by the atlas Stage‑2 step (`HCI-CNT/atlas/stage2_locked.py`; an R port exists), and stored under a `coda_standard/` key kept separate from the Higgins extensions, so a CoDa reviewer can read only the familiar quantities.

The static‑geology / cross‑sectional researcher — including the many at CoDaWork for whom dynamics are not (yet) the question — is met where they are, given a clean standard output, and left entirely alone. The trajectory/helmsman/regime machinery exists only for data that moves in time and for users who want it. (See `onramp/PHD_ONRAMP_PROTOCOL.md` → "If you only want the static picture.")

## Posture toward the CoDa community

Respectful, collegial, invitational, and correct in attribution — by design and by record. The work is presented to the community as an invitation to refute and strengthen, not a claim to defend: *if CoDa can refute a weak claim, the instrument gets stronger.* Attribution to Aitchison, Egozcue, Pawlowsky‑Glahn, Hron, Martín‑Fernández, Gloor and the wider community is maintained in the README reference blocks and the handout. The geometry is CoDa's; the monitoring layer is the extension; the opportunity is to join them.

## Alignment note (for maintainers)

An audit (2026‑06‑14) found this stance already the consistent primary message across the handout, README, executive summary, and HUF README, with the static outputs genuinely implemented in Stage‑2. Two items were corrected to keep it airtight: one live sentence in `HUF/science/core/WHAT_HUF_IS.md` that had implied a CoDa gap (reworded to "extends … built on the geometry the CoDa community established"), and the static‑user pathway (now documented in the onramp). One archived draft (`HUF/archive/pre-codawork2026-drafts/THE_UNION.md`) still carries "CoDa has no X" table language; it is archive‑only — if ever promoted or cited, reword to "CoDa's scope did not include X; X is the extension's contribution." New works should align to the one‑sentence stance above.

*The geometry is CoDa's. The motion is the extension. The static user is served and left alone. Recognition, not invention.*
