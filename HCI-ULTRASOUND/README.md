# HCI-ULTRASOUND — Higgins Compositional Instrument for Non-Contact Ultrasound

**Status:** canonical sibling tier, doctrine-only (push #24, 2026-05-08).
**Sibling of:** [`HCI-CNT/`](../HCI-CNT/), [`HCI-CNQ/`](../HCI-CNQ/), [`HCI-AUDIO/`](../HCI-AUDIO/), and the [`HCI/`](../HCI/) instrument family.
**Origin:** identified by Peter as *"one of the major application goals derivative from the original work"* (the original DADC work in Rogue-Wave-Audio). See [`../HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](../HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md).
**Engine status:** no compiled engine yet. Doctrine and design specifications only.

---

## What this folder is

This is the canonical home for **non-contact ultrasound work** in the Hˢ system: object detection, autofocus, image stabilisation, and **geometry lock probes** for medical and industrial use.

The headline use case is the **geometry lock probe** — a probe (or fixed array) that uses CNT/CNQ-driven feedback to actively lock onto a specific geometric feature in 3D space (an edge, a curvature, a tissue interface, a defect, etc.) and maintain that lock under relative motion, drift, or noise.

---

## How this relates to DADC (the historical origin)

The original DADC question was:

> *Which cabinet dimension is currently carrying most of the fixed 6.02 dB diffraction budget?*

The HCI-ULTRASOUND question for a geometry-lock probe is the same question, generalised to **active sensing**:

> *Which frequency, angular sector, or array channel of the return signal is currently providing the strongest, most stable lock onto the target geometry?*

The fixed total is no longer a near-field 6.02 dB; it is the total return-signal energy (and phase information) arriving back at the probe. The parts are no longer cabinet dimensions; they are frequency bands, angular sectors, or array channels. The closure rule remains. The new ingredient — not present in DADC — is that the **system actively steers** to keep the helmsman locked on the desired geometric feature.

---

## What "geometry lock" means

A geometry-lock probe in CNQ terms:

1. **Transmit** ultrasound pulses (multi-frequency or from multiple array elements).
2. **Receive** returns and form a **joint quaternion field** combining amplitude (intensity per channel/frequency) and phase (time-of-flight) information.
3. **Continuously extract** the Joint Helmsman from `log(q_joint)`.
4. **Use Helmsman Stability** (proposed extension, see [`../HCI-CNT/handbook/GLOSSARY.md`](../HCI-CNT/handbook/GLOSSARY.md) §I) as the primary control signal.
5. **Adjust** focus / beam steering / mechanical probe orientation to maintain lock on the target geometric feature.

When the helmsman is stable on the desired feature, the probe is "locked." When stability drops or the helmsman flips off the target, the probe acts to recover the lock.

---

## Folder map

```
HCI-ULTRASOUND/
├── README.md                       (this file)
├── HCI-ULTRASOUND_ADMIN.json       tier admin and provenance
│
├── doctrine/                       what HCI-ULTRASOUND measures and why
│   ├── GEOMETRY_LOCK_PROBE.md      doctrine of the lock probe (carriers, joint field, control loop)
│   ├── OBJECT_DETECTION.md         using helmsman flips to detect target presence and identity
│   ├── AUTOFOCUS_AND_STABILIZATION.md  using helmsman stability as autofocus / image-stabilisation metric
│   └── MEDICAL_VS_INDUSTRIAL.md    domain-specific concerns (safety, contact-free coupling, regulatory)
│
└── spec/                           specifications for future engines / pipelines
    └── ULTRASOUND_ADAPTER_SPEC.md  adapter for ultrasound return-signal data
```

---

## What's here today (push #24)

This is a **doctrine-only** scaffold. The folder exists so that ultrasound work has a canonical home when pilot data arrives. Specifically:

- Geometry lock probe doctrine ([`doctrine/GEOMETRY_LOCK_PROBE.md`](doctrine/GEOMETRY_LOCK_PROBE.md)) defines carriers, the joint quaternion field, the control loop, and the success criteria.
- Object detection, autofocus, and image stabilisation each get their own doctrine document, all rooted in the same Helmsman/Joint-quaternion machinery.
- Domain split (medical vs industrial) is handled in a single doctrine note covering safety, coupling, and regulatory differences.
- One adapter spec lays out how raw ultrasound return data flows into the canonical compositional form.

---

## What's *not* here yet

- Compiled `UltrasoundAdapter`.
- Real ultrasound datasets (medical or industrial).
- Hardware-in-the-loop control implementation.
- Validation against any specific commercial probe or imaging system.
- IRB / regulatory documentation for medical pilots.

These are the next pilots. Until one lands, the doctrine here is testable in the same sense Volume IV was testable before HCI-CNQ promotion: the framework's predictions are stated, and the measurements that would falsify or confirm them are specified.

---

## Why this is its own tier (and not just an application of HCI-CNQ)

HCI-CNQ is general (any quaternion-lifted compositional system). HCI-ULTRASOUND has its own tier because:

- Active sensing (closing a control loop on Helmsman Stability) is a different operational mode than passive analysis.
- Medical and industrial domains have specific safety, regulatory, and hardware concerns that deserve a dedicated doctrine layer.
- Future ultrasound-specific tooling (probe drivers, beamforming integrations, real-time visualisation, lock-quality dashboards) belongs here.
- It is one of Peter's stated major application goals, and giving it a canonical home signals seriousness about the application path.

---

## Pointers

- Origin lineage: [`../HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](../HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md)
- CNT engine (back-end for compositional data flow): [`../HCI-CNT/`](../HCI-CNT/)
- CNQ tier (joint quaternion machinery): [`../HCI-CNQ/`](../HCI-CNQ/)
- Helmsman family vocabulary: [`../HCI-CNT/handbook/GLOSSARY.md`](../HCI-CNT/handbook/GLOSSARY.md) §I
- Sister applied tier: [`../HCI-AUDIO/`](../HCI-AUDIO/)

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
*From a 6.02 dB diffraction budget on cabinet dimensions to active geometry lock at the probe — the same closure principle, applied at the right scale.*
