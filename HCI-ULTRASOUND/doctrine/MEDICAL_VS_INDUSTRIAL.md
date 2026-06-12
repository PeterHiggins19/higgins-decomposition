# Medical vs Industrial Use of HCI-ULTRASOUND

**Status:** doctrine, push #24 (2026-05-08).
**Companion:** [GEOMETRY_LOCK_PROBE.md](GEOMETRY_LOCK_PROBE.md), [OBJECT_DETECTION.md](OBJECT_DETECTION.md), [AUTOFOCUS_AND_STABILIZATION.md](AUTOFOCUS_AND_STABILIZATION.md).

---

## Why this split matters

The same CNQ machinery (Joint Helmsman, Helmsman Stability, M² = I) applies to both medical and industrial ultrasound. The differences are not in the framework — they are in **safety, regulatory, coupling, and acceptance criteria**. This document captures those differences in one place so doctrine documents elsewhere don't have to repeat them.

---

## Medical use cases

| Use case | Why CNQ helps |
|---|---|
| **Air-coupled wound assessment** | Non-contact (no gel), useful for burns or post-surgical wounds where contact is contraindicated. Helmsman locks onto wound-edge geometry. |
| **Neonatal monitoring** | Non-contact, low acoustic dose; helmsman lock allows imaging on a moving infant without firm contact. |
| **Vascular imaging stabilisation** | Vessels move with cardiac and respiratory cycles; helmsman lock follows the vessel automatically. |
| **Fetal monitoring** | Helmsman lock onto specific fetal anatomy (e.g., heart, head) reduces operator-dependence. |
| **Musculoskeletal robotic guidance** | Robot-held probe locks geometry on tendon/bone interface; surgeon sees stable image. |

### Medical-specific concerns

- **Acoustic dose limits**: ultrasound power is regulated (e.g., FDA MI/TI limits). Lock loops must respect dose budgets.
- **Coupling**: air-coupled ultrasound has dramatically different acoustic impedance than gel-coupled. The framework is agnostic, but the adapter must know which domain it's in.
- **Regulatory pathway**: medical devices require IRB / FDA / equivalent submission. Doctrine + determinism contract + hash chain support this; specific submission documents are pilot-time work.
- **Privacy**: patient-identifiable data must be handled per HIPAA / equivalent. The framework's content_sha256 mechanism allows verification without storing raw measurements.

---

## Industrial use cases

| Use case | Why CNQ helps |
|---|---|
| **Composite inspection** | Layered structures have characteristic helmsman signatures; defects flip the helmsman. |
| **Pipeline inspection through air gaps** | Non-contact, robust to standoff variation; lock follows pipe geometry. |
| **Hot-material non-contact inspection** | Air-coupled probe at safe distance; lock on hot edges/joints. |
| **Robotic probe on curved surfaces** | Probe maintains lock on specific weld or feature without precise positioning. |
| **Additive-manufacturing quality control** | Layer-by-layer scanning with lock on print bed geometry. |

### Industrial-specific concerns

- **Throughput**: industrial inspection often has time-per-part budgets. Lock loop latency matters.
- **Surface variation**: industrial parts have wider geometric variation than anatomy; the signature library (see [OBJECT_DETECTION.md](OBJECT_DETECTION.md)) needs broader coverage.
- **Environment**: dust, vibration, electromagnetic interference. Hash-chain provenance supports traceability for QA/QC.
- **Standards**: ASTM, ISO, NADCAP, etc. Doctrine + bit-identical reproduction support standards compliance.

---

## What's the same across both domains

- The CNT engine (`HCI-CNT/engine/cnt.py`) is unchanged and identical for both.
- The CNQ joint-quaternion machinery is identical for both.
- The Helmsman family extensions ([`../../HCI-CNT/handbook/GLOSSARY.md`](../../HCI-CNT/handbook/GLOSSARY.md) §I) apply to both.
- The lock criteria (S_σ thresholds, M² = I, joint rotation angle) are common.
- The determinism contract is preserved in both domains.

---

## What's different (summary)

| Concern | Medical | Industrial |
|---|---|---|
| Power limits | Strict (regulatory) | Looser (engineering) |
| Coupling | Often air-coupled or low-gel | Often air-coupled at standoff |
| Latency tolerance | Variable | Often tight (throughput) |
| Regulatory burden | High (IRB, FDA, etc.) | Domain-specific (ISO, ASTM, NADCAP) |
| Data handling | HIPAA / privacy | Confidentiality / IP |
| Pilot timeline | Slower (IRB) | Faster (engineering) |
| First-pilot recommendation | Wound or vascular monitoring (lower-risk pathway) | Composite inspection (rich features, public datasets exist) |

---

## Recommended pilot order

When pilots begin (after push #24), the practical order is:

1. **Industrial first** — composite inspection on a public dataset. Validates the full pipeline (adapter → CNT → joint quaternion → helmsman → lock) without regulatory overhead.
2. **Medical second** — wound assessment or vascular monitoring with appropriate IRB. Builds on the validated industrial pipeline; only the adapter and signature library are domain-specific.

This is a recommendation, not a mandate. Peter may have access to a medical pilot path that flips the order.

---

*Same closure principle. Same helmsman. Different gates around the pilot.*
