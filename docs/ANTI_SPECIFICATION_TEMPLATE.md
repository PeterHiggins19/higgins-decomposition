# <Subject> Anti-Specification

**Subject:** *(e.g., HCI-CNQ engine v2.0.0)*
**Subject version:** *(e.g., 2.0.0)*
**Doctrine version:** SEA-1.0
**Last audited:** *(YYYY-MM-DD)*
**Next audit due:** *(YYYY-MM-DD)*
**Auditor:** *(name or process)*
**Verity file:** `<path>/verity.json`

---

## Purpose of this document

This document is a **failure-mode enumeration with mitigation evidence**, written under the *Suspicion of Every Assumption* (SEA) doctrine documented in `docs/SUSPICION_OF_EVERY_ASSUMPTION.md`. The default presumption is that the subject artifact has failed; each entry below dispatches one specific way it could have failed.

The companion `verity.json` is the machine-readable form, validated against `docs/verity_schema.json`. Together they constitute the artifact's earned credibility.

## How to read this document

For each failure mode listed:

- **ID** is a stable identifier (e.g., `NUM_001`).
- **Category** is one of NUM (numerical), ALG (algorithmic), SCH (schema), INV (input validation), INT (integration), INTP (interpretation), REP (reproducibility), WRP (wrapper), DOC (documentation), ADV (adversarial).
- **Failure mode** is what would go wrong if this case were not handled.
- **Conditions** are the input or runtime conditions that would trigger it.
- **Mitigation** is how the engine prevents or bounds the failure.
- **Evidence** is one or more references (TEST, PROP, PROOF, EMPR, STRC, DESN) showing the mitigation works.
- **Residual risk** is one of `none`, `bounded`, `unverified`, `acknowledged_limitation`.

## Summary

*(Auto-generated or manually maintained.)*

| Metric | Value |
|---|---|
| Total failure modes catalogued | N |
| Unverified count | N |
| Acknowledged limitations | N |
| Release gate pass | true / false |

---

## NUM — Numerical failure modes

### NUM_001 — *<short title>*

- **Failure mode:** *(what would break)*
- **Conditions:** *(when it would trigger)*
- **Mitigation:** *(how it is prevented)*
- **Evidence:**
    - TEST: `tests/test_*.py::test_*` (verified YYYY-MM-DD)
- **Residual risk:** none / bounded / unverified / acknowledged_limitation
- **Notes:** *(optional)*

*(Add NUM_002, NUM_003, ... as needed.)*

---

## ALG — Algorithmic failure modes

### ALG_001 — *<short title>*

*(Same structure as above.)*

---

## SCH — Schema failure modes

### SCH_001 — *<short title>*

*(Same structure.)*

---

## INV — Input-validation failure modes

### INV_001 — *<short title>*

---

## INT — Integration failure modes

### INT_001 — *<short title>*

---

## INTP — Interpretation failure modes

### INTP_001 — *<short title>*

---

## REP — Reproducibility failure modes

### REP_001 — *<short title>*

---

## WRP — Wrapper failure modes

*(Applicable only when the subject involves wrappers; engines that emit only neutral CoDa output may have no entries here.)*

### WRP_001 — *<short title>*

---

## DOC — Documentation failure modes

### DOC_001 — *<short title>*

---

## ADV — Adversarial failure modes

### ADV_001 — *<short title>*

---

## Acknowledged limitations

For convenience, all entries with `residual_risk: acknowledged_limitation` are listed here. These are cases the engine genuinely does not handle, documented honestly so users can make informed decisions.

| ID | Category | Limitation | Recommended workaround |
|---|---|---|---|
| | | | |

---

## Audit log

| Date | Auditor | Event |
|---|---|---|
| YYYY-MM-DD | *(name)* | Initial enumeration |
| YYYY-MM-DD | *(name)* | External review by ChatGPT — added entries NUM_017, ALG_023 |
| YYYY-MM-DD | *(name)* | External review by Grok — added entry ADV_005; upgraded INV_003 evidence from STRC to TEST |

---

## Next audit due

*(date)*. Triggers: minor release of the engine; addition of a new wrapper instance; addition of a new locale; external audit cycle.

---

*This document is a living artifact. New failure modes get added; existing ones get evidence upgraded. The release gate is satisfied when `unverified_count == 0` per the verity.json summary.*
