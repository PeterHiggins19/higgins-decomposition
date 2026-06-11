"""CN-TT v4 — Stage: the uniform processing-section interface.
Every processing section is ONE of these, which makes each section simultaneously:
  - an ADAPTABILITY unit (bounded `config`, clamped to `config_bounds`) = a control point;
  - a TEST point (`self_test()` returns (ok, detail));
  - a HASHED unit (the pipeline caches by input+config+version so identical work is
    never repeated -> 'why repeat history at the cost of time and effort').
Stages are pure: run(ctx, cfg) reads ctx, returns a dict of NEW outputs to merge."""
from __future__ import annotations

class Stage:
    name = "stage"
    version = "0.0.0"
    default_config: dict = {}
    config_bounds: dict = {}     # {param: (lo, hi)} -> clamped (control-point bounds)

    def configure(self, overrides=None):
        cfg = dict(self.default_config)
        if overrides:
            cfg.update(overrides)
        for k, bnd in self.config_bounds.items():
            if k in cfg and isinstance(cfg[k], (int, float)) and not isinstance(cfg[k], bool):
                lo, hi = bnd
                cfg[k] = min(max(cfg[k], lo), hi)
        return cfg

    def run(self, ctx: dict, cfg: dict) -> dict:
        raise NotImplementedError

    def self_test(self):
        raise NotImplementedError
