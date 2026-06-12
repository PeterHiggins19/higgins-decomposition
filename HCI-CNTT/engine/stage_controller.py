"""CN-TT v4 — StageController: per-stage operational state + lifecycle commands.
States: IDLE, READY, RUNNING, BUSY, HALTED, ERROR. Commands: halt/start, stage-by-stage.
CN-TT drives this now; an external controller (Matthew / NASA / USGS) can drive the
same interface later. The controller holds operational state; stages stay pure compute."""
from __future__ import annotations

class StageController:
    STATES = ("IDLE", "READY", "RUNNING", "BUSY", "HALTED", "ERROR")

    def __init__(self, stage_names, owner="CN-TT"):
        self.owner = owner                       # who is controlling (CN-TT / external)
        self._state = {n: "READY" for n in stage_names}
        self._halt = set()

    # --- commands (idempotent) ---
    def halt(self, name):  self._halt.add(name);  self._state[name] = "HALTED"
    def start(self, name):
        self._halt.discard(name)
        if self._state.get(name) == "HALTED": self._state[name] = "READY"
    def halt_all(self):  [self.halt(n) for n in self._state]
    def start_all(self): [self.start(n) for n in self._state]

    # --- queries / state ---
    def is_halted(self, name): return name in self._halt
    def set_state(self, name, s): self._state[name] = s
    def state(self, name): return self._state.get(name)
    def snapshot(self): return dict(self._state)
