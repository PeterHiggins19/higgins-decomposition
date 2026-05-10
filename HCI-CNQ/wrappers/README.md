# CNQ v2 Wrappers

This folder holds the **wrapper specification** and **example wrapper data files** for CNQ v2.

A wrapper is a JSON file that translates the engine's mathematically neutral output into a domain-specific, locale-specific user-readable view. The engine itself does not consume wrappers; an optional renderer / report-builder does. If no wrapper is used, engine output is read directly in CoDa-community standard vocabulary.

## Files

| File | Purpose |
|---|---|
| `WRAPPER_SCHEMA.md` | User-readable specification of the wrapper format (read this first if authoring a new wrapper) |
| `wrapper_schema.json` | JSON Schema for machine-validation of wrapper files |
| `wrapper_blank_template.json` | Empty starter for authoring a new domain wrapper |
| `wrapper_generic.json` | Identity / passthrough wrapper — uses CoDa standard vocabulary directly (no aliases, no calibration) |
| `wrapper_audio.json` | First full instance: multi-driver speaker system coherence analysis (en + fr) |
| `wrapper_government_budget.json` | Skeleton for Canadian government budget composition (en + fr) — Markham example |

## Authoring a new wrapper

1. Read `WRAPPER_SCHEMA.md` for conventions.
2. Copy `wrapper_blank_template.json` to `wrapper_<your_domain>.json`.
3. Fill in `wrapper_id`, `wrapper_version`, `engine_target`, `supported_locales`, `default_locale`, and `domain_metadata`.
4. For each engine carrier name your dataset uses, add an entry to `carrier_aliases`.
5. For each engine output field you want labelled, add an entry to `field_aliases`.
6. Optionally add `calibration_profiles` for fields where domain-specific value ranges and verdicts apply.
7. Validate against `wrapper_schema.json` (any JSON Schema validator works).
8. Commit alongside the engine output it interprets.

## Adding a locale to an existing wrapper

Add the new locale code to `supported_locales`, then add the locale key to every `display_name`, `description`, and label string in the file. Other locales remain unaffected.

## Engine independence

The engine does not load wrappers. Wrappers exist downstream of the engine — at report-building time, dashboard time, or report-reading time. Engine output is reproducible and verifiable independent of any wrapper.
