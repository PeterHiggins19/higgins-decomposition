#!/usr/bin/env python3
"""
HUF-CNT — Native Units helper (v1.1 Feature B).

Converts between INPUT_UNITS and the unit in which the Higgins scale is
reported. Conversion factors come from the natural log of bases between
the unit definitions; CLR/Hs are computed in the project's unit, and
the project-card "scale_factor_to_neper" makes any conversion explicit
on every plate.

Supported INPUT_UNITS:
    "ratio"        — raw multiplicative ratios (default; no conversion)
    "neper"        — natural-log ratios (1 unit = 1 neper)
    "nat"          — same as neper (alias)
    "bit"          — log_2 ratios (1 bit = ln(2) ≈ 0.6931 neper)
    "dB_power"     — 10·log_10(P) (1 dB = 0.2303 neper)
    "dB_amplitude" — 20·log_10(A) (1 dB = 0.1151 neper)
    "%"            — percent (multiplicative; closure-friendly, no factor)
    "absolute"     — quantity in some absolute scale (closure-friendly)

Functions:
    scale_factor_to_neper(unit) -> float
    higgins_unit_for(input_unit, requested) -> str
    declare(input_unit, requested) -> dict   # for metadata.units_*
"""
from __future__ import annotations
import math

# 1 unit-of-input = factor·neper. Treat ratio/% / absolute as "no conversion"
# (they already live on the simplex once closed; CLR returns nepers).
_FACTORS_TO_NEPER: dict = {
    "ratio":        1.0,
    "neper":        1.0,
    "nat":          1.0,                  # alias
    "bit":          math.log(2.0),        # 0.6931 nep / bit
    "dB_power":     math.log(10.0)/10.0,  # 0.2303 nep / dB
    "dB_amplitude": math.log(10.0)/20.0,  # 0.1151 nep / dB
    "%":            1.0,
    "absolute":     1.0,
}


def scale_factor_to_neper(unit: str) -> float:
    """Multiplicative factor from `unit` into nepers."""
    if unit not in _FACTORS_TO_NEPER:
        raise ValueError(f"unknown INPUT_UNITS: {unit!r}.  "
                         f"Allowed: {sorted(_FACTORS_TO_NEPER)}")
    return _FACTORS_TO_NEPER[unit]


def higgins_unit_for(input_unit: str, requested: str = "auto") -> str:
    """Resolve the unit in which Hs / Aitchison norm is reported."""
    if requested != "auto":
        if requested not in {"neper", "bit", "ratio"}:
            raise ValueError(f"requested HIGGINS_SCALE_UNITS must be one of "
                             f"'auto','neper','bit','ratio'; got {requested!r}")
        return requested
    # auto:
    if input_unit in {"bit"}:
        return "bit"
    if input_unit in {"dB_power", "dB_amplitude"}:
        return "neper"   # dB inputs convert into neper natively
    return "neper"


def declare(input_unit: str, requested: str = "auto") -> dict:
    """Build the metadata.units_* block (additive schema 2.1.0 fields)."""
    hu = higgins_unit_for(input_unit, requested)
    f  = scale_factor_to_neper(input_unit)
    return {
        "input_units":                 input_unit,
        "higgins_scale_units":         hu,
        "units_scale_factor_to_neper": f,
        "feature":                     "v1.1-B native units",
        "schema_addition":             "2.1.0",
    }


def project_card_line(input_unit: str, requested: str = "auto") -> str:
    """One-line human-readable banner for plate footers."""
    d = declare(input_unit, requested)
    if input_unit in {"ratio", "neper", "nat", "%"}:
        return (f"INPUT_UNITS={input_unit}; "
                f"Hs reported in {d['higgins_scale_units']} "
                f"(no conversion needed).")
    return (f"INPUT_UNITS={input_unit}; "
            f"1 {input_unit} = {d['units_scale_factor_to_neper']:.4g} neper; "
            f"Hs reported in {d['higgins_scale_units']}.")


if __name__ == "__main__":
    import json, sys
    units = sys.argv[1] if len(sys.argv) > 1 else "ratio"
    print(json.dumps(declare(units), indent=2))
    print()
    print(project_card_line(units))
