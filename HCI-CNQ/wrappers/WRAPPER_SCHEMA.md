# CNQ v2 Wrapper Schema Specification

**Version:** wrapper-schema/1.0
**Engine target:** CNQ v2.0.0 (`cnq/2.0.0`)
**Status:** load-bearing for the wrapper architecture (see `ai-refresh/CNT_V3_CNQ_V2_DESIGN.md` §11)
**Catalog:** INV-042 (domain wrapper convention)

---

## 1. What a wrapper is

A wrapper is a JSON file that maps CNQ engine output paths to domain-specific localised display names, units, descriptions, and calibration value-range labels. It is **data, not code**, and **does not modify the engine or its output**. The engine emits CoDa-community vocabulary; the wrapper translates that vocabulary to a chosen domain and a chosen locale at report-building time only.

**The engine does not consume wrappers.** Wrappers are read by optional renderer / report-builder tools that take engine output + wrapper + locale and produce a human-readable report. If no wrapper is provided, engine output is read directly using CoDa standard names.

## 2. Top-level required fields

```json
{
  "wrapper_id": "string",
  "wrapper_version": "string",
  "engine_target": "string",
  "supported_locales": ["en", "fr", ...],
  "default_locale": "en",
  ...
}
```

| Field | Required | Description |
|---|---|---|
| `wrapper_id` | yes | Short identifier (`audio`, `government_budget`, `geochem_basalt`, etc.) |
| `wrapper_version` | yes | Wrapper version string (e.g., `1.0`, `2.1.3`) |
| `engine_target` | yes | Engine + schema this wrapper is built for (e.g., `cnq/2.0.0`) |
| `supported_locales` | yes | Array of ISO 639-1 locale codes (e.g., `["en", "fr"]`) |
| `default_locale` | yes | Locale to use if user does not specify; must be in `supported_locales` |

## 3. Optional top-level fields

| Field | Type | Purpose |
|---|---|---|
| `domain_metadata` | object | Wrapper-level provenance: `name`, `description`, `author`, `references` |
| `t_axis_label` | localised string | Domain meaning of the trajectory dimension T (e.g., "frequency bins (Hz)", "fiscal years") |
| `carrier_aliases` | object | Map from engine carrier ID to localised display info |
| `field_aliases` | object | Map from engine output path to localised display info |
| `calibration_profiles` | object | Value-range classifications per engine field |

## 4. Localised string convention

Anywhere a string is shown to a user, it appears as a map from locale code to translated string:

```json
{
  "en": "Auditory-cortex coherence index",
  "fr": "Indice de cohérence du cortex auditif"
}
```

A wrapper must provide at least the entry for `default_locale`. Missing locales fall back to `default_locale` at render time.

## 5. `carrier_aliases`

Maps engine carrier IDs (the column names in the input CSV) to display info:

```json
"carrier_aliases": {
  "L_HF": {
    "display_name": {
      "en": "Left high-frequency driver",
      "fr": "Haut-parleur aigu gauche"
    },
    "units": "W/m^2",
    "description": {
      "en": "...",
      "fr": "..."
    }
  }
}
```

Engine carrier IDs are arbitrary strings the user chooses when building the input CSV. The wrapper assigns them human-readable names per locale. `units` and `description` are optional.

## 6. `field_aliases`

Maps engine output paths (dot-notation into the JSON output) to display info:

```json
"field_aliases": {
  "chsh_diagnostic.S_value": {
    "display_name": {
      "en": "Auditory-cortex coherence index (CHSH S)",
      "fr": "Indice de cohérence du cortex auditif (CHSH S)"
    },
    "units": "dimensionless",
    "description": {
      "en": "Single-number coherence diagnostic; range [0, 2.828]",
      "fr": "Diagnostic de cohérence à valeur unique ; plage [0; 2,828]"
    }
  }
}
```

For array fields, use `[]` to indicate "applies to every element":

```json
"bearing_trajectory.per_step[].angle_rad": {...}
"helmsman_family.sigma[]": {...}
```

## 7. `calibration_profiles`

Value-range classifications per engine field. Each range carries a localised label and a verdict tag.

```json
"calibration_profiles": {
  "chsh_diagnostic.S_value": {
    "ranges": [
      {
        "min": 0.0,
        "max": 2.0,
        "label": {
          "en": "Independent",
          "fr": "Indépendant"
        },
        "verdict": "fail"
      },
      {
        "min": 2.0,
        "max": 2.4,
        "label": {
          "en": "Borderline coupled",
          "fr": "Couplage limite"
        },
        "verdict": "borderline"
      },
      {
        "min": 2.4,
        "max": 2.828,
        "label": {
          "en": "Structurally coupled",
          "fr": "Structurellement couplé"
        },
        "verdict": "pass"
      }
    ]
  }
}
```

`verdict` values are conventionally one of `excellent`, `pass`, `borderline`, `fail`, `anomalous`, but wrapper authors may use any string; renderers may map verdicts to colours, icons, or alerts.

`min` is inclusive, `max` is exclusive (except the final range, where `max` may be `null` to mean unbounded).

## 8. `domain_metadata`

Free-form provenance:

```json
"domain_metadata": {
  "name": {
    "en": "Multi-driver speaker system coherence analysis",
    "fr": "Analyse de cohérence des systèmes d'enceintes multi-haut-parleurs"
  },
  "description": {
    "en": "Translates CNQ engine output to audio engineering quantities...",
    "fr": "Traduit la sortie du moteur CNQ en grandeurs d'ingénierie audio..."
  },
  "author": "Rogue Wave Audio",
  "references": [
    "HCI-AUDIO/CNQ_AUDIO_WRAPPER.md"
  ]
}
```

## 9. `t_axis_label`

Localised label describing what the engine's T (trajectory) dimension represents in this domain:

```json
"t_axis_label": {
  "en": "Frequency bins (Hz, log-spaced)",
  "fr": "Bandes de fréquence (Hz, espacement logarithmique)"
}
```

## 10. Versioning

A wrapper declares its `engine_target` (e.g., `cnq/2.0.0`). When the engine schema bumps, existing wrappers continue to work for fields whose paths did not change; new fields require wrapper updates. Wrapper version (`wrapper_version`) increments independently of engine version.

## 11. Conventions for new wrappers

- Wrapper IDs are lowercase snake_case (`audio`, `government_budget`, `geochem_basalt`, `nuclear_decay_chain`).
- Wrapper file names follow `wrapper_<wrapper_id>.json`.
- Locale codes are ISO 639-1 two-letter codes.
- Field paths use dot-notation into the engine output JSON.
- Array iteration is denoted with `[]` (e.g., `bearing_trajectory.per_step[].angle_rad`).
- Carrier IDs are domain-defined strings used in the input CSV header row.

### 11.1 Standard locale set (UN-6)

For shipped reference wrappers (`wrapper_audio.json`, `wrapper_government_budget.json`), the framework ships **support for the six UN official languages** plus any additional locales the wrapper author needs:

| Locale | Code | Purpose | Authoring discipline |
|---|---|---|---|
| English | `en` | Default; primary CoDa-community language | Peter-authored, project-canonical |
| French | `fr` | Bureau International des Poids et Mesures (BIPM) co-official; Measurement Canada bilingual requirement; Government of Canada compliance | Peter-authored at International-French/BIPM register; reviewed by qualified bilingual expert before metrology deployment |
| Spanish | `es` | International standards reach (Latin America, Iberian peninsula) | Initial draft; **expert metrology review pending before formal deployment** |
| Russian | `ru` | UN official; major scientific publication language | Initial draft; expert review pending |
| Chinese (Mandarin) | `zh` | UN official; major economic/scientific reach (PRC, Singapore, Taiwan) | Initial draft; expert review pending |
| Arabic | `ar` | UN official; Middle East / North Africa metrology | Initial draft; expert review pending |

The 6-locale set is the **lowest bar for international compliance**. A Canadian metrology deployment requires en + fr at minimum; an international standards body deployment (BIPM, ISO) typically requires en + fr + at least one of {es, ru, zh}; a UN agency deployment may require all 6.

Locale codes can be extended freely. A wrapper for a domain that needs additional locales (e.g., German `de` for European industrial metrology, Japanese `ja` for Asian audio standards, Portuguese `pt` for Brazilian markets) simply adds those entries to `supported_locales` and provides translations in the strings.

### 11.2 Translation quality marking

A wrapper may declare per-locale translation status via a top-level `locale_quality` block:

```json
"locale_quality": {
  "en": "canonical",
  "fr": "canonical",
  "es": "draft_pending_review",
  "ru": "draft_pending_review",
  "zh": "draft_pending_review",
  "ar": "draft_pending_review"
}
```

Renderers may surface this metadata to users (e.g., a banner: "This report is rendered in Spanish from a draft translation pending expert metrology review"). The convention `canonical | reviewed | draft_pending_review | machine_translated` is recommended; wrappers may use other strings provided they are documented in the wrapper's `domain_metadata.references`.

### 11.3 Why this matters for Canadian metrology

Measurement Canada (the federal regulator) requires bilingual English/French for all measurement reports of regulated devices. The Bureau International des Poids et Mesures (BIPM) — the international standards authority that defines the SI units Measurement Canada enforces — uses both English and French as official publication languages. By shipping `en` + `fr` as canonical-quality wrapper translations from day one, the framework can be used directly in Canadian metrology contexts without translation review delay. The other UN-6 locales position the framework for international standards-body deployment when those audiences emerge.

## 12. What wrappers do NOT contain

- Engine code or algorithm changes.
- Hashes or signatures of engine output.
- Anything that affects the determinism contract.
- Anything that needs to be parsed by the engine itself.

Wrappers live downstream of the engine in every sense.

## 13. Validation

A wrapper file must validate against `wrapper_schema.json` (a JSON Schema document in this folder). Any JSON Schema validator works. Renderer tools should validate before consuming.
