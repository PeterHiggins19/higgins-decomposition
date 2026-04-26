#!/usr/bin/env python3
"""
Hˢ DIAGNOSTIC REPORTER
========================
Reads diagnostic codes from the Hˢ pipeline and produces
readable reports in multiple languages.

Languages: English (en), 中文 (zh), हिन्दी (hi), Português (pt), Italiano (it)

Architecture:
  - Pipeline emits codes via hs_codes.py (fixed, lightweight)
  - This reporter reads codes and formats for readers (independent, evolvable)
  - Translations loaded from locales/*.json (one file per language)
  - Adding a language = adding one JSON file, zero code changes

Author: Peter Higgins / Claude
Version: 2.0
For: CoDaWork 2026 + global distribution
"""

import json, os

LOCALES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locales")

SUPPORTED_LANGUAGES = {
    "en": "English",
    "zh": "中文 (Mandarin Chinese)",
    "hi": "हिन्दी (Hindi)",
    "pt": "Português (Portuguese)",
    "it": "Italiano (Italian)",
}

def _load_locale(lang):
    """Load a locale JSON file. Falls back to English if not found."""
    path = os.path.join(LOCALES_DIR, f"{lang}.json")
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    en_path = os.path.join(LOCALES_DIR, "en.json")
    if os.path.exists(en_path):
        with open(en_path, encoding='utf-8') as f:
            return json.load(f)
    return {}


def report(codes, lang="en"):
    """Generate a readable report from diagnostic codes.

    Parameters
    ----------
    codes : list of dict (from hs_codes.generate_codes)
    lang : str, one of 'en', 'zh', 'hi', 'pt', 'it'

    Returns
    -------
    str : formatted report in the requested language
    """
    locale = _load_locale(lang)

    def t(key):
        return locale.get(key, key)

    lines = []
    lines.append(t("_title"))
    lines.append("=" * 60)

    errors = [c for c in codes if c['code'].endswith('-ERR')]
    warnings = [c for c in codes if c['code'].endswith('-WRN')]
    discoveries = [c for c in codes if c['code'].endswith('-DIS')]
    calibrations = [c for c in codes if c['code'].endswith('-CAL')]
    infos = [c for c in codes if c['code'].endswith('-INF')]

    lines.append(f"\n{t('_total')}: {len(codes)}")
    lines.append(f"  {t('_errors')}:       {len(errors)}")
    lines.append(f"  {t('_warnings')}:     {len(warnings)}")
    lines.append(f"  {t('_discoveries')}: {len(discoveries)}")
    lines.append(f"  {t('_calibrations')}: {len(calibrations)}")
    lines.append(f"  {t('_information')}:  {len(infos)}")

    if errors:
        lines.append(f"\n── {t('_section_errors')} ──")
        for c in errors:
            msg = t(c['code'])
            lines.append(f"  [{c['code']}] {msg}")

    if warnings:
        lines.append(f"\n── {t('_section_warnings')} ──")
        for c in warnings:
            msg = t(c['code'])
            lines.append(f"  [{c['code']}] {msg}")

    if discoveries:
        lines.append(f"\n── {t('_section_discoveries')} ──")
        for c in discoveries:
            msg = t(c['code'])
            val = ""
            if c.get('value'):
                if isinstance(c['value'], dict):
                    parts = []
                    for k, v in c['value'].items():
                        if isinstance(v, float):
                            parts.append(f"{k}={v:.6f}")
                        else:
                            parts.append(f"{k}={v}")
                    val = f" ({', '.join(parts[:3])})"
                elif isinstance(c['value'], (int, float)):
                    val = f" ({c['value']})"
            lines.append(f"  [{c['code']}] {msg}{val}")

    if calibrations:
        lines.append(f"\n── {t('_section_calibrations')} ──")
        for c in calibrations:
            msg = t(c['code'])
            lines.append(f"  [{c['code']}] {msg}")

    lines.append(f"\n{t('_run_complete')}")
    lines.append(t("_deterministic"))

    return "\n".join(lines)


def report_all_languages(codes):
    """Generate reports in all supported languages.

    Returns dict of {lang_code: report_string}
    """
    return {lang: report(codes, lang) for lang in SUPPORTED_LANGUAGES}


if __name__ == "__main__":
    print("Hˢ Reporter v2.0")
    print(f"Locale directory: {LOCALES_DIR}")
    print(f"Supported languages:")
    for code, name in SUPPORTED_LANGUAGES.items():
        path = os.path.join(LOCALES_DIR, f"{code}.json")
        status = "✓" if os.path.exists(path) else "✗ MISSING"
        print(f"  {code}: {name} [{status}]")
