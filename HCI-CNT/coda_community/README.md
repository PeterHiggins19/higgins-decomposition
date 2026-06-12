# CoDa Community — preprint papers

Three short citable papers for the compositional-data community.
Each paper is also folded into the relevant section of the consolidated
handbook (see Part references below); they are kept here as standalone
preprint artefacts for citation, sharing, and reading-without-the-handbook
contexts.

| Paper | Topic | Volume reference |
|---|---|---|
| [`CNT_VS_CODA_BALANCE.md`](CNT_VS_CODA_BALANCE.md) | Technical balance book — atan2 simplification, three-orthogonal-views comparison, M²=I licence for the depth tower, performance balance with honest costs | [Volume I §I](../handbook/VOLUME_1_THEORY_AND_MATHEMATICS.md) |
| [`CNT_ROI_AND_USE_CASES.md`](CNT_ROI_AND_USE_CASES.md) | ROI / break-even analysis with the time-budget composition rendered as a CoDa-style ternary diagram | [Volume II §G](../handbook/VOLUME_2_PRACTITIONER_AND_OPERATIONS.md) |
| [`CNT_VERIFICATION_VALUE_FOR_CODA.md`](CNT_VERIFICATION_VALUE_FOR_CODA.md) | Hash-chain provenance proposal as honest-publishing infrastructure for the CoDa community | [Volume III §B](../handbook/VOLUME_3_VERIFICATION_REFERENCE_AND_RELEASE.md) |

## Figure assets

| File | Used by |
|---|---|
| [`cnt_roi_ternary.pdf`](cnt_roi_ternary.pdf) | Figure for the ROI paper — vector |
| [`cnt_roi_ternary.png`](cnt_roi_ternary.png) | Figure for the ROI paper — raster |
| `make_roi_ternary.py` (in archived docs) | Regenerable build script for the ternary figure |

## Tone

All three papers are written in supportive / additive framing toward
classical CoDa methods: CNT is presented as additions on top of the
established CoDa toolkit, not as a replacement of incorrect work. The
classical methods (Aitchison's CLR, Egozcue's Helmert ILR, the variation
matrix, the biplot, the balance dendrogram) are explicitly presented as
canonical foundations.

## 🆕 The access layer for these papers (May 2026)

A reader who finds these papers compelling and wants to *use* CNT on their
own data does not need to install code or master the schema first. The
**CCTT v1.0** protocol gives them a 7-phase guided on-ramp — by hand or
with an AI assistant — that produces a CNT-grade analysis with hash-chained
provenance. → [`../../ai-refresh/CCTT_QUICKSTART.md`](../../ai-refresh/CCTT_QUICKSTART.md)

The **OPERATIONS_PROTOCOL v1.0** is the front-door map of the whole repo
for any reviewer who lands here from one of these papers and wants to
audit a specific result. → [`../../OPERATIONS_PROTOCOL.md`](../../OPERATIONS_PROTOCOL.md)
Section 12 is the 30-second reproducibility recipe for an external auditor.

---

*The instrument reads. The expert decides. The hashes carry the receipts.*
