# Geology application work × the new system — sweep, new value, and the revision plan (public)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27.*

> **Clarification (important, honest):** Matthew **has not worked on this project.** Everything in
> `collaborations/geology-wehner/` was **generated here, internally** — it is HUF/Hˢ's own application work,
> *oriented toward* compositional geoscience and prepared for a **possible future** engagement. Matthew is **not
> aware this project exists** beyond what was known around conference time. The only thing that is genuinely
> *his* is his **published work** (Wehner 2017; Dhankhar & Wehner 2023), which this is built to serve. The
> "field-directional sniffer" was a direction he raised in conference-time discussion; the build is ours.
> **When/if Matthew is shown this, it will be all new to him — and per Peter's standing rule, he is shown only
> what is fully tested and field-operational-ready. A faulty tool is a liability for a front-line field worker.**

*This is a full sweep of the internally-generated geology-application work, what the new system adds, and exactly
what to revise to reach operational-test readiness — the old material ran on a much older engine. Public science
stays here; the working relationship and any commercial terms are private and off-repo, Peter-gated. Nothing
posted; nothing sent; Matthew is the first contact, and contact has not been made.*

---

## The sweep — what exists, and on what engine

The collaboration folder (`collaborations/geology-wehner/`) holds, all **public science**:

- **The mudstone witness (W-II).** Frielingen-9 Lower-Cretaceous section (WD-XRF, PANGAEA 897615) read as a
  composition: D=6 exact, ~2.23 effective directions, 12 regime boundaries, Zr/TOC antagonism on a carbonate
  background; the coarse 3-part amalgamation *loses* the within-detrital structure (the EITT boundary). Real
  data, read and never copied, hash-receipted.
- **The geochemistry corpus.** Hs-05 on 26,266 intraplate volcanic rocks (10 oxides), intermediate-rocks decode,
  HFSP fixed-point machinery, X-ray-crystallography decomposition, and CNT domain runs (Stracke OIB/MORB, Tappe
  kimberlite, Qin clinopyroxene, Ball TAS/age).
- **The field-directional sniffer — Matthew's own idea.** A cell-phone micro-lab (Dhankhar & Wehner 2023) +
  the engine as a directional compositional "sniffer": the geologist is the rover, the phone is the map, the
  engine says which way to the target composition. **Filed as concept/feasibility.**
- **The full proposal + flight roadmap + multisensor concept.**

**The engine underneath all of it is the older CNT / CNTT.** That is the thing to update: everything above
predates the latest determinism guarantee, the tetrode standard, and — most importantly — a *measured* sniffer.

## The published work this now serves

The value is to Matthew's **already-published** research, which this complements (never replaces):

- **Wehner (2017)** — wavelet + compositional-data chemostratigraphy. The new system adds a **deterministic,
  hash-receipted navigation/driver/regime layer** that re-computes from the cited public file to the same hash —
  reproducibility a wavelet pipeline does not, by itself, provide.
- **Dhankhar & Wehner (2023)** — cell-phone-camera Raman for field identification. The new system turns that
  sensor into a **directional field instrument** — now with measured evidence (below), not just a concept.

## What the new system adds (the new value)

Four things built since, each measured and receipted, map straight onto this collaboration:

1. **The sniffer is now real.** Matthew's field-directional-sniffer concept is built, measured, and
   stress-tested (`the_sniffer.py` `520d894e0ef25a3c`; stress `d871430ef12fdcb2`): guided by the compositional
   gradient, a rover reaches the target in **14 stations vs 120 for random hunting (8.4×)**, holds through heavy
   noise and rough terrain on the tetrode alone, and — under any combined push — **a little exploration** turns a
   collapse into a 97% reach. The "which way to dig" reading is no longer a hope; it has a measured envelope and
   a named boundary (a truly flat field has no heading).
2. **The tetrode standard — the field sampling protocol.** Take **four samples per station** (a tetrode): four
   points over-determine the local gradient *and* cancel the common-mode (calibration / drift / illumination)
   error exactly, while independent noise falls as ~1/√N (`8515f97ecb8f23f6`). This is precisely the field
   geologist's sampling discipline, now with the math behind it — and it is the project's standing standard for
   sensitive reads.
3. **The determinism guarantee.** Every read re-runs to the same SHA-256 (`determinism_sweep.py`). For published
   chemostratigraphy this is the strong claim: *test it, don't trust it* — a reviewer re-computes the regime/drift
   read from the public file and gets the identical hash.
4. **The latest engine.** The current Hs-Kinematics engine + its extensions (forward-cast "where the section is
   heading," common-mode rejection, the stewardship gate) replace the older CNT/CNTT the existing runs used.

## The revision plan — what to update, in order

1. **Re-run the mudstone on the latest engine.** Re-execute the Frielingen-9 read on the current Hs-Kinematics
   engine (it used the older CNT), emit fresh receipts, and confirm the W-II findings reproduce. *Named, not
   assumed.*
2. **Promote the field sniffer from concept to measured-demonstrator** (done here — see the updated
   `FIELD_DIRECTIONAL_SNIFFER.md`): cite the built, stress-tested sniffer; keep the honest fence (needs a real
   Raman/XRF feed, positioning, field calibration, zero-treatment, ground validation; the geologist decides).
3. **Adopt the tetrode sampling protocol** in the field-sniffer and mudstone methods (4 samples/station).
4. **Attach determinism receipts** to the public mudstone/geochem reads as the reproducibility guarantee.
5. **Add the forward-cast** ("where the section is heading") as an optional read, fenced as a what-if.

## Public / private split (made coherent)

- **Public (this folder):** all the science above — the measured sniffer, the tetrode protocol, the
  determinism guarantee, the re-run plan, anchored to Wehner (2017) and Dhankhar & Wehner (2023) as the
  published work it serves.
- **Private (off-repo, Peter-gated):** the working relationship, the commercial/transmission terms, and any
  contact — moved to the private folder (`HUF/dormant/geology-wehner-private/`), revised with the upgraded value.
  **The proposal's deal content does not belong on the public repo.**

## Honest scope

- **T1 (measured):** the sniffer (8.4×; stress envelope), the tetrode (common-mode ~10⁻¹⁵, 1/√N), the
  determinism guarantee, and the W-II witness all reproduce to their receipts.
- **T2 (the fit):** that these add value to Wehner (2017) / Dhankhar & Wehner (2023) is a reasoned, complementary
  positioning — Hs is a navigation/reproducibility layer over established methods, not a replacement.
- **Fences:** the field sniffer needs a real sensor feed + field calibration + ground validation; the sniffer
  gives the heading, **the geologist decides** where to dig (Breaker 16); strictly-positive compositions for the
  exact cancellation (E-21; trace/below-detection values need zero-treatment).
- **Sole gate:** Peter. **Nothing posted; nothing sent; the deal stays private.**

*Cross-refs: `FIELD_DIRECTIONAL_SNIFFER.md` (updated) · `MUDSTONE_HS_FIT.md` · `../../papers/triangulation/W2_MUDSTONE_WITNESS.md`
· `../../industrial-instruments/the-sniffer/` (the measured sniffer + stress) ·
`../../huf-gov/doctrine/THE_TETRODE_STANDARD_for_sensitive_studies.md` · `../../ai-refresh/loglog/DETERMINISM_SWEEP_RESULTS.md`
· `../../THE_PACKAGE_what_is_in_motion.md`. Published: Wehner (2017); Dhankhar & Wehner (2023). Peter is the sole
gate; nothing posted.*

*Proof & Honesty Standard — the sweep names what exists and on what engine · the new value is measured and
receipted · positioned as complement to the published work, not replacement · public science / private deal split
kept clean · the geologist decides where to dig · the human keeps the gate.*
