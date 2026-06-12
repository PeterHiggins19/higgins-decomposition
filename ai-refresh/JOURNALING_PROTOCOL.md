# Journaling Protocol — journal as you go

*2026-06-10. The discipline that keeps the histories true: any advancement or alteration to any part of the system is journaled **at the moment it happens**, not reconstructed afterward. Because this instrument operates outside traditional methods, the journal is not bookkeeping — it is the audit trail that makes the system trustworthy and lets an AI or a reviewer reconstruct exactly what changed, when, and why.*

---

## The rule

> **Every change carries its own journal entry, written in the same step as the change.**

If you advance an objective, alter a component, fix a defect, make a decision, or run a verification, you write the entry **before moving on**. No batch back‑filling. A change without a journal entry is an unfinished change.

## What counts as a change (triggers an entry)
- An objective moves status (open → in_progress → done / moot / holding).
- A component is added, altered, ported, frozen, or retired.
- A decision is made (e.g. "no native D=16", "retire the oracle after parity").
- A verification is run (a self‑test, a parity diff, a prior‑art search) — entry records the result and the claim tier.
- A defect or discrepancy is found or resolved.

## Where an entry goes (the three surfaces, in order)
1. **`HS_TRACKING_LOG.json`** — update the item's `status`, set `solved` if done, append the `support_docs` link(s), and a one‑line `note`. (Referenced by `HS_ADMIN.json _meta.tracking_log_ref`.)
2. **The nearest narrative journal** — the experiment's `RESULTS_*.md` / `EXPERIMENTS_JOURNAL.md`, or the relevant design doc's addendum. Prose, with the measured numbers and the honest caveat.
3. **The admin chain at commit time** — `CHANGELOG.md` row + `HS_FAST_REFRESH.json` `_meta` advance + `PUSHES_INDEX.md` (the §6 rhythm). This is Peter's gate; the first two surfaces are written live, this one is synced at push.

## Entry format (minimum)
`what changed · when (ISO date) · status · the measured result or decision · the support doc link · the claim tier (1/2/3)`

Example (live):
> `E-10 Backblaze parity · 2026-06-10 · done · TIER-A bit-identical on 731×4, atan2 angle agrees 5e-11° · experiments/backblaze_v4_parity_2026-06/RESULTS_backblaze_v4_vs_oracle.md · Tier 1`

## Non‑negotiables (carried from the operating discipline)
- **Claim tiers always attached** — Tier 1 (verified/computed), Tier 2 (standard math, soundly applied), Tier 3 (to earn). Never journal a Tier‑3 item as Tier 1.
- **Inspected ≠ executed** — never upgrade "looks right" into "ran and verified".
- **Honest divergence** — a discrepancy is recorded as a documented improvement or a defect to fix, never silently absorbed.
- **Dates are absolute** — convert "today/yesterday" to ISO dates in the entry.
- **Source of truth** — on any conflict, `HS_FAST_REFRESH.json` wins; the tracking log and journals defer to it.

## Why this matters more here than usual
The system reads structure in realms that are generally invisible to traditional methods (compositional dynamics on the simplex, deterministic navigation, hash‑chained provenance). A reviewer cannot fall back on familiar intuition to reconstruct what happened — the journal *is* the reconstruction. Journaling in lock‑step with change is what lets this be put into mission‑critical settings: every state of the instrument is recoverable from its own receipts.

*The instrument reads. The expert decides. The hashes carry the receipts — and the journal says when they were written.*
