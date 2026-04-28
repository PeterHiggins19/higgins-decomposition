# The Natural Partition Principle

**Version:** 1.0
**Date:** 2026-04-28
**Author:** Peter Higgins — Rogue Wave Audio
**Claim tier:** Core principle — the reason compositional analysis works

---

## The Principle

A compositional analysis succeeds when the partition unit is natural to the system being measured. It fails — or produces noise — when the partition is synthetic.

A natural partition is one that arises from the system's own geometry or physics. A synthetic partition is one imposed by the analyst.

---

## Origin — The Loudspeaker Problem

The DADC (Dimension-Apportioned Diffraction Correction) system partitions loudspeaker radiation energy across frequency using a budget of 6.02 dB — the value of 20 log10(2). This number is not chosen for convenience. It is the acoustic consequence of a doubling: when a loudspeaker transitions from half-space radiation (2pi steradians, all energy forward) to full-space radiation (4pi steradians, energy distributed equally front and back), the intensity halves. The intensity halving IS 20 log10(2). The partition unit is not assigned by the engineer — it is read from the physics of diffraction.

The composition works because the budget and the partition are both natural. The 6.02 dB budget is the total energy redistribution across the diffraction transition. The partition is logarithmic because sound intensity follows a logarithmic scale. The simplex closure (all energy accounted for) is guaranteed by energy conservation. Nothing is synthetic. Every number comes from the physics.

This is why DADC produces correct results without calibration factors or empirical tuning. The composition aligns with the geometry that nature already uses.

---

## The Insight — From Assigned to Discovered

In DADC, the engineer recognised the natural partition (20 log10(2)) and assigned it to the composition. The success came from choosing correctly — from understanding the physics well enough to know which partition the system actually uses.

In the Higgins Decomposition (Hs), the pipeline does not assign any partition. It does not know the physics. It closes the data to the simplex, transforms to log-ratio coordinates via CLR, computes the cumulative Aitchison variance trajectory, and then asks: does this trajectory lock to a known transcendental constant?

The squeeze step against 35 constants is the instrument asking nature to reveal its own partition. When the cosmic energy budget locks to 1/(e^pi) at delta = 4.19 x 10^-5, that is not the analyst assigning a partition — that is the data declaring one.

The progression from DADC to Hs is therefore:

- **DADC:** The engineer assigns a natural partition that he recognises from domain knowledge.
- **Hs:** The instrument discovers the natural partition from the data without domain knowledge.

Both work for the same reason: the partition is natural, not synthetic. The only difference is who identifies it.

---

## The Logarithmic Thread

The connection to Compositional Data Analysis (CoDa) is direct. The CLR transform at the core of Hs takes each carrier, divides by the geometric mean of all carriers, and takes the natural logarithm. This is a log-ratio — the same family of operation as 20 log10.

Aitchison's foundational insight (1982) was that the natural geometry of compositions is logarithmic: distances, centres, and inner products on the simplex all operate through log-ratios. The geometric mean is the natural centre. Linear operations (arithmetic mean, percentage differences) distort compositional geometry.

20 log10(2) is a log-ratio. CLR is a log-ratio. The EITT result — that geometric-mean decimation preserves Shannon entropy while arithmetic-mean decimation destroys it — follows from this same structure. The geometric mean operates in log-ratio space, where natural partitions live. The arithmetic mean operates in linear space, where natural partitions are distorted.

The DADC insight, the Aitchison geometry, and the EITT invariance are three expressions of the same principle: compositional structure is logarithmic, and analysis that respects the logarithmic partition succeeds while analysis that imposes a linear partition fails.

---

## Formal Statement

**The Natural Partition Principle:** For any system whose components form a composition on the simplex, there exists a partition structure determined by the system's own geometry or physics. Analysis that aligns with this natural partition (logarithmic, ratio-based, respecting the Aitchison geometry) preserves compositional information. Analysis that imposes a synthetic partition (linear, difference-based, ignoring simplex geometry) destroys it.

**Corollary (DADC):** When the natural partition is known to the analyst, it can be assigned directly. The composition then reads the system exactly.

**Corollary (Hs):** When the natural partition is not known, the Higgins Decomposition discovers it through the variance trajectory and transcendental squeeze. The composition reads the system without requiring domain knowledge.

**Corollary (EITT):** Geometric-mean decimation preserves Shannon entropy on the simplex because it operates within the natural (logarithmic) partition structure. Arithmetic-mean decimation destroys entropy because it imposes a synthetic (linear) partition.

---

## Significance

This principle explains why the Higgins Decomposition works across 18 domains spanning 44 orders of magnitude without domain-specific tuning. It does not impose a partition — it discovers one. The twelve steps operate entirely in log-ratio space (the natural partition space of the simplex), and the transcendental squeeze reads what the data itself declares.

It also explains the origin of the project. The DADC system was successful not because of clever engineering but because the engineer happened to choose the correct natural partition for the acoustic problem. The Higgins Decomposition generalises this: instead of requiring domain expertise to identify the partition, it builds an instrument that finds it automatically.

The principle connects three previously separate observations: (1) DADC's success with 20 log10(2) as a compositional partition, (2) Aitchison's demonstration that simplex geometry is logarithmic, and (3) the EITT finding that geometric-mean operations preserve while arithmetic-mean operations destroy. All three are instances of the same underlying fact: compositions have natural partitions, and those partitions are logarithmic.

---

*Peter Higgins — Rogue Wave Audio*
*License: CC BY 4.0*
