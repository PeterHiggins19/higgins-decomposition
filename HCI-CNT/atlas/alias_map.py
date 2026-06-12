#!/usr/bin/env python3
"""
HUF-CNT — carrier alias map (v1.1 feature E).

Loads per-experiment carrier_aliases from master_control.json (or any
JSON file) and provides a small lookup that the atlas display layer
can use to substitute friendly names. Original carrier codes are
unchanged in the JSON; this is purely a display layer.

Usage:
  from alias_map import load_aliases, alias

  aliases = load_aliases("mission_command/master_control.json", "ember_jpn")
  display_name = alias("Coal", aliases)   # "Coal" if no alias defined

The master_control.json schema for aliases:

    {
      "experiments": {
        "ember_jpn": {
          "is_temporal": true,
          "ordering_method": "by-time",
          "carrier_aliases": {
            "Coal":         "Coal-fired",
            "Other Fossil": "Other fossil fuels",
            "Wind":         "Wind generation"
          }
        }
      }
    }
"""
from __future__ import annotations
import json
from pathlib import Path


def load_aliases(master_control_path, dataset_id: str) -> dict:
    """Return carrier_aliases dict for dataset_id; {} if none defined."""
    p = Path(master_control_path)
    if not p.exists():
        return {}
    try:
        cat = json.loads(p.read_text())
    except json.JSONDecodeError:
        return {}
    return (cat.get("experiments", {})
              .get(dataset_id, {})
              .get("carrier_aliases", {}))


def alias(carrier: str, aliases: dict) -> str:
    """Look up the alias for a carrier; return the original name if none."""
    return aliases.get(carrier, carrier)


def alias_list(carriers: list, aliases: dict) -> list:
    """Apply alias() to every carrier in a list."""
    return [alias(c, aliases) for c in carriers]


def alias_label(label: str, aliases: dict) -> str:
    """For event labels like 'Coal–Gas: spread = 8.39°', substitute aliases
    in the carrier-pair prefix only. Carrier names separated by en-dash
    or ascii hyphen."""
    if not aliases:
        return label
    for sep in ("–", "-"):
        if sep in label:
            head, *rest = label.split(":", 1)
            parts = [p.strip() for p in head.split(sep)]
            if all(p in aliases for p in parts):
                head = sep.join(aliases.get(p, p) for p in parts)
                return head + (":" + rest[0] if rest else "")
    return label
