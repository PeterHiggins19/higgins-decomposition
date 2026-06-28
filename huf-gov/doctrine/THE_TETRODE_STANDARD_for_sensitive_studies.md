# The tetrode standard — four of the same topic, mandatory for sensitive studies (DOCTRINE)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-27. A standing
rule for the work going forward: **every sensitive study — cancer, blood, and all medical cases — must be done as
a tetrode of four.** Not three. The native quaternion migrated it from the triode of 3 to the tetrode of 4: four
independent studies of the same topic, so the cross-involved systems are tested and the noise self-cancels. This
is now the standard for all future sensitive studies. Peter is the sole gate; nothing posted.*

---

## The rule

> **A sensitive study is a tetrode: four independent studies of the same topic.**
> Four blood studies. Four cancer studies. Four of whatever the topic is — independent channels, independent
> cohorts/registries/assays — read as one. Three is not enough for these cases. **Must do four.**

This applies to cancer, blood panels, and all medical/clinical-adjacent work; it is recommended wherever the DUT
data is noisy and the stakes are high.

## Why four — the native quaternion, not the triode

The number is not arbitrary; it is the structure of the instrument itself.

- **The quaternion forces it.** A **four-part** composition's three ILR coordinates *are* a unit quaternion on
  $S^3 = SU(2)$ — the exact rung the whole series rests on (P1). A **triode** (3 parts) gives only two ILR
  coordinates: it cannot carry the quaternion. Four parts give the three imaginary components exactly. So for a
  read meant to be exact and redundant, **four is the native number** — the quaternion migrated the standard up
  from three to four.
- **Observability forces it.** D = 4 is the minimum mesh to *locate* a point in a 3-D volume — the four-pole
  tetrahedron (the observability core math). Three locates on a plane; four locates in the volume.
- **The division-algebra wall.** The exact compositions live at the Hurwitz dimensions 1, 2, **4**, 8; four is
  the first that carries a full non-commutative product. Below four you lose structure; the tetrode sits exactly
  on the rung.

So the tetrode is not "one more for safety" — it is the **structurally correct** redundancy: four independent
reads matched to the four-part quaternion the instrument reads exactly.

## What four buys (measured)

The tetrode result is already receipted (`papers/medical-epidemiology/THE_TETRODE_TEST_determinism_from_noise.md`,
`8515f97ecb8f23f6`), across three independent real datasets:

- **Common-mode error cancels exactly** (clr; residual ~10⁻¹⁵) — overall scale, reporting rate, illumination:
  gone, with no contribution from Hˢ ("never Hs").
- **Independent error halves at N = 4** and keeps falling as ~1/√N — the data made to pay for its own lack of
  determinism, by basic statistics and the math of scale.
- **Four independent topics tested together** = the best cross-involved-systems grouping: the same topic seen
  four ways exposes what one view would hide, exactly as the probe-and-see loop intends.

## How to run a tetrode (the procedure)

1. **Acquire four independent channels of the same topic** — four registries / cohorts / assays / instruments,
   as independent as the domain allows.
2. **Read each as a composition** (closure → clr); the per-channel common mode cancels exactly.
3. **Average across the four** (kill the independent noise) → the recovered composition + a master receipt over
   the four channel-receipts.
4. **Probe and see → course of action:** read the four together, let the differences between channels drive the
   decision (the autonomous probe loop); the operator chooses the course (Breaker 16).
5. **Record in the self-guided map** (`library/tetrode_self_guided_map.py`) so the tetrode space is acquired and
   evolved as compositional memory.

## Honest scope

- **Exact only for strictly-positive compositions** (the locked-discriminant precondition; structural zeros
  excluded, E-21). The 1/√N benefit assumes **independent** channels — correlated error common to all four is
  **not** removed by the tetrode (in-subspace noise is provably not separable). Four independent channels is the
  goal; four copies of the same biased channel buys nothing.
- **The clinical fence is unchanged:** the tetrode improves the *measurement*; sensitive medical work stays
  research / population-epidemiology, **not** clinical/diagnostic/treatment, until validated under the proper
  standards (IEC 62304 / ISO 13485) with domain experts and Peter's decision.
- **Sole gate:** Peter. **Nothing posted.**

*Cross-refs: `../../papers/medical-epidemiology/THE_TETRODE_TEST_determinism_from_noise.md` (the measured tetrode,
`8515f97ecb8f23f6`) · `A_RECEIPTED_READ_FOR_CANCER_EPIDEMIOLOGY.md` (P-μ, the first sensitive case) ·
`../../papers/ABSTRACT_LEDGER.md` (P1, the quaternion) · `../../library/tetrode_self_guided_map.py` (the
self-guided map) · `DONT_DAMAGE_WHERE_YOU_LIVE.md`. Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the number four is grounded in the quaternion/observability/Hurwitz structure, not
chosen for comfort · the benefit is measured and receipted · the independence requirement and the not-separable
boundary stated plainly · the clinical fence unchanged · the human keeps the gate.*
