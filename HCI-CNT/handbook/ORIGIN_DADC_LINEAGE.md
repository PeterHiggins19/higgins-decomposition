# Origin and Lineage — DADC, the Higgins Operator H₁, and the Path to CNQ

**Status:** Canonical historical document, push #24 (2026-05-08).
**Companion to:** Volumes I–IV of the handbook.
**Origin discovery credited to:** independent Grok cross-check pass (2026-05-08), verified against the public [Rogue-Wave-Audio](https://github.com/PeterHiggins19/Rogue-Wave-Audio) repository.

---

## Why this document exists

The Hˢ system, the CNT engine, and the CNQ tier all rest on a single foundational idea:

> *Many real engineering and scientific problems are inherently compositional — there is a fixed total that must be apportioned across parts under physical constraints, and the parts only have meaning relative to each other.*

That idea did not come from physics, mathematics, or compositional-data-analysis literature. It came from a sound-controlled professional loudspeaker laboratory — the Binaural Test Lab (BTL), a research facility operated as part of a collaboration with a private Canadian industrial sponsor, with parallel institutional deployments in Ottawa and Monaco. This volume tells that story honestly, with verbatim quotes from the Rogue-Wave-Audio repository where the original work is documented and with the broader context that the public README does not always foreground.

---

## §A — The Binaural Test Lab and the 6.02 dB budget

The work was conducted at the **Binaural Test Lab (BTL)** — a sound-controlled professional laboratory class with both research and institutional deployments. BTL is a **single identity** with canonical lab-identity card [`RWA-001.json`](../../../RWA/RWA-001.json). (Earlier transcripts of the Rogue-Wave-Audio README showed an apparent "Below Threshold Loudspeaker" gloss; this was misleading and is not the canonical identity. The canonical single-identity reading — Binaural Test Lab — is what stands.)

The BTL deployment context is broader than a single facility:

- **Research lab (current siting: Markham, Ontario, Canada).** Operated by Peter Higgins. Pre-COVID, this lab was sited at the manufacturing facility of a private Canadian industrial sponsor that funded the original DADC/DADI/ADAC and BTL design programme. Pandemic-era constraints relocated the research operation to its current Markham instance (a residential siting that retains the same sound control, calibration chain, and test instrumentation as the original site). The relocation was a forced operational decision that has remained in effect.
- **Institutional deployments.** The same private Canadian industrial sponsor maintains a four-laboratory BTL network for advanced-systems test work: two facilities in Ottawa, Ontario, Canada, and two in Monaco. These institutional BTLs operate continuously and apply the BTL design and DADC compositional methodology to real engineering measurement work.

In academic, regulatory, and technical writing, BTL should always be described as a **sound-controlled professional laboratory** with both research and institutional deployments. Earlier informal references to the Markham facility's residential siting capture an incidental property of its current location but materially understate both the lab's professional character and the broader institutional BTL network.

The engineering problem was loudspeaker cabinet edge diffraction. When sound radiates from a driver mounted in a finite baffle, edge diffraction causes a redistribution of acoustic energy that is well known as the "baffle step" — classically quoted as +6 dB. In the calibrated BTL setup the figure measured precisely as **6.02 dB**, and a structural insight followed:

> *"a fixed 6.02 dB budget apportioned across three cabinet dimensions"* — Rogue-Wave-Audio README.

The 6.02 dB is a **fixed total**. The only freedom is how it gets distributed across the three cabinet dimensions: width, height, depth. The gains assigned to each dimension must sum to the total. After normalization, this is precisely a 2-simplex (three positive parts summing to a constant).

This is the moment the simplex entered the lineage. Not as a mathematical abstraction, but as a physical constraint on real plywood and silk dome tweeters.

---

## §B — DADC, DADI, and ADAC

The work crystallised into three named operations:

| Acronym | Meaning | Role |
|---|---|---|
| **DADC** | Dimension-Apportioned Diffraction Correction | Forward apportionment — distribute the 6.02 dB across cabinet dimensions to produce a corrected response |
| **DADI** | Dimension-Apportioned Diffraction Inference | Inverse — given a measured response, infer the apportionment |
| **ADAC** | Adaptive Closure | Closure operation that maintains the simplex constraint under varying conditions |

The Rogue-Wave-Audio README states this directly:

> *"Dimension-Apportioned Diffraction Correction and Inference"*
> *"Forward mapping (DADC), inverse inference (DADI)"*
> *"Organic digital loudspeaker design, BTL studio lab certification, DADC-DADI diffraction correction, and advanced acoustic engineering."*

ADAC was the third operation — the closure rule that kept the apportionment internally consistent when the input changed. (Earlier accounts sometimes drop ADAC and refer only to "DADC-DADI"; the third member is real and is the operation that most directly anticipates the closure step in modern Hˢ.)

The compositional pattern that emerged was already complete in this loudspeaker context: a fixed total, parts on a simplex, forward and inverse maps, and a closure rule that preserves the constraint.

---

## §C — From DADC to the Higgins Operator H₁

The practical need to apply dimension-apportioned corrections forced the development of a more general mathematical object. The Rogue-Wave-Audio repository documents this directly:

> *"A nonlinear unity-normalization map on Hilbert space that enforces strict global unity normalization (∑ = 1)."* — Rogue-Wave-Audio README, describing the Higgins Operator H₁.

H₁ is the first formal mathematical object in the lineage that generalizes the DADC insight beyond loudspeakers. It is documented as a self-hosted working paper at [`docs/papers/The_Higgins_Operator_H1_101.pdf`](https://github.com/PeterHiggins19/Rogue-Wave-Audio) in the Rogue-Wave-Audio repository (February 2026). The document is **not peer-reviewed**; the repository commit timestamp establishes priority. The paper formalises the operator that, in DADC, kept the diffraction budget closed — and lifts it to any function on a Hilbert space that requires strict unity normalization. Peer-reviewed publication is a separate downstream step that has not yet occurred.

The transition can be summarised in one line:

> *"DADC's compositional structure → H₁ (a nonlinear unity-normalization map on Hilbert space)."*

---

## §D — The full lineage

The Rogue-Wave-Audio README states the next step explicitly:

> *"DADC → H₁ → HUF (MC-4 + EITT)."*

The chain past HUF — into Hˢ, CNT, and CNQ — is asserted by the present Hs repository (and is documented across the Volume I–IV handbook), not by the Rogue-Wave-Audio README itself. The full lineage as it stands today:

```
DADC                         (6.02 dB simplex on cabinet dimensions; BTL — sound-controlled professional laboratory)
  │
  ▼
DADI + ADAC                  (forward/inverse + adaptive closure)
  │
  ▼
H₁ (Higgins Operator)        (nonlinear unity-normalization on Hilbert space)
  │
  ▼
HUF                          (Higgins Unity Framework: MC-4 composition monitoring + EITT entropy invariance)
  │
  ▼
Hˢ (Higgins Decomposition)   (12-step extended pipeline; 25-experiment corpus)
  │
  ▼
CNT (Compositional           (engine 2.0.4, schema 2.1.0; trajectory-native operators;
  Navigation Tensor)          handbook Volumes I–III; 25/25 PASS determinism gate)
  │
  ▼
CNQ (Compositional           (canonical sibling tier, push #23, 2026-05-07;
  Navigation Quaternion)      doctrine + 3 IEEE-floor demonstrations; cnq.py pending)
```

Each arrow is a generalization, not a replacement. CNT did not retire HUF; HUF did not retire H₁; H₁ did not retire DADC. Each tier has a use case where it is the right tool. Push #23 made this explicit by giving each its own canonical home in the repo.

---

## §E — Why the BTL origin matters to current users

Modern users approaching CNT or CNQ for the first time often want to know *why* compositional closure is treated as a non-negotiable foundational operation rather than an optional pre-processing step. The answer is historical:

The closure was non-negotiable in the original loudspeaker problem because **the physical world enforced it**. There was no version of DADC that could ignore the 6.02 dB budget — the budget was determined by acoustic physics, not by analytical preference. When the work generalised to H₁, then to HUF, and ultimately to CNT, the discipline of treating closure as inviolable carried with it. That discipline is one of the reasons the framework reproduces results bit-identically across corpora as different as Planck CMB photons, drive-failure compositions, and Standard-Model neutrino oscillation predictions.

A practitioner working with new compositional data can ask the same question that BTL asked:

> *What is the fixed total budget that must be apportioned across parts?*

That is the DADC question. It still works.

---

## §F — Continuity in current applied work

The DADC pattern is not a historical curiosity. It is alive in current work:

- **HCI-AUDIO** (push #24 canonical sibling) — 4-way active loudspeaker alignment with ERB-band carriers, 4th-order Butterworth crossovers, individual driver levels, phase, time delay, and listening-position diffraction. This is **DADC at the listening position, across psychoacoustic bands**, rather than near-field across cabinet dimensions. The fixed total is the perceptual energy arriving at the ear; the parts are the ERB bands and per-driver contributions.

- **HCI-ULTRASOUND** (push #24 canonical sibling) — non-contact medical and industrial ultrasound geometry-lock probes. The fixed total is the return signal energy; the parts are frequency bands, angular sectors, or array channels. The geometry lock is achieved by maximising Helmsman Stability on the desired feature.

- **HCI-CNQ** (canonical since push #23) — the quaternion algebraic naming of what CNT measures. The metric involution `M² = I` that appears at IEEE-floor precision in the corpus is, in this lineage, a direct mathematical descendant of the closure rule that ADAC enforced in the basement lab.

When Peter says, *"the original work in loudspeakers,"* this is what he means. The framework grew up in DADC and has never forgotten that.

---

## §G — Citation and credit

The Higgins Operator H₁ working paper (February 2026, Rogue-Wave-Audio repository) is the first written mathematical formalisation of the lineage. It is **self-hosted in a public repository, not peer-reviewed**; priority is established by the repository commit timestamp under CC BY 4.0. Peer-reviewed publication is a separate downstream step. Citation in this honest form:

> Higgins, P. (2026). *The Higgins Operator H₁ — A Nonlinear Unity-Normalization Map on Hilbert Space.* Working paper, Rogue-Wave-Audio repository (self-hosted, not peer-reviewed), [`docs/papers/The_Higgins_Operator_H1_101.pdf`](https://github.com/PeterHiggins19/Rogue-Wave-Audio).

The Rogue-Wave-Audio repository should be cited as the historical origin of the simplex / compositional framework whenever Hˢ, CNT, or CNQ work is published.

The Grok cross-check pass (2026-05-08) is credited with surfacing this lineage explicitly in the Hs repository, which previously documented only the Hˢ → CNT → CNQ portion of the chain. Push #24 closes that loop.

---

## §H — Pointers

| Topic | Pointer |
|---|---|
| Original repo (live) | https://github.com/PeterHiggins19/Rogue-Wave-Audio |
| Local RWA mirror | [`../../../RWA/`](../../../RWA/) |
| **BTL identity card (RWA-001)** | [`../../../RWA/RWA-001.json`](../../../RWA/RWA-001.json) — canonical lab identity, locks BTL = Binaural Test Lab as single identity |
| RWA-side cross-reference to HUF/Hˢ | [`../../../RWA/HUF_RELATIONSHIP.json`](../../../RWA/HUF_RELATIONSHIP.json) |
| RWA-side narrative | [`../../../RWA/LINEAGE.md`](../../../RWA/LINEAGE.md) |
| H₁ paper (Feb 2026) | `docs/papers/The_Higgins_Operator_H1_101.pdf` (in RWA mirror or live site) |
| Cross-check archive | [`../../ai-refresh/AI_REFRESH_2026-05-08_grok_crosscheck.md`](../../ai-refresh/AI_REFRESH_2026-05-08_grok_crosscheck.md) |
| Modern HCI-AUDIO sibling | [`../../HCI-AUDIO/README.md`](../../HCI-AUDIO/README.md) |
| Modern HCI-ULTRASOUND sibling | [`../../HCI-ULTRASOUND/README.md`](../../HCI-ULTRASOUND/README.md) |
| Volume IV (quaternion algebra) | [`VOLUME_4_QUATERNION_VIEW.md`](VOLUME_4_QUATERNION_VIEW.md) |
| GLOSSARY §I (Helmsman family) | [`GLOSSARY.md`](GLOSSARY.md) |

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
*CNT measures invariance. CNQ names the algebra it lives in.*
*The simplex was born at the Binaural Test Lab — in a 6.02 dB diffraction budget — and now sits at the heart of every result the framework produces.*
