#!/usr/bin/env python3
"""
go_hs_vs_blind.py -- give one Go player the Hs (relational) read and leave the other BLIND (absolute levels
only). The consequence is the blindness-suite result in a contest: a proportional position can be DECIDED while
the absolute stone-counts still look EVEN -- 'every alarm green while the mixture turned' (the gas-tank deceptive
drift), now on a board.

Setup (a Go-framed COMPOSITIONAL contest, not Go tactics): both sides place stones at the SAME rate, so the
absolute stone-count margin stays ~0 (the board looks even). But White quietly converts CONTESTED territory into
White CONTROL -- a proportional shift in the {black-control, white-control, contested} composition. Two
decision-makers watch the same board:
  BLIND player: reads the ABSOLUTE stone margin |black - white|. ~0 -> sees no threat, ever.
  Hs player  : reads the RELATIONAL control composition (clr); White's share of the DECIDED board rises
               decisively -> flags the turn EARLY and responds in time.
The game is DECIDED at move D (White's relational control crosses the winning line). Flag at/below D -> respond
in time; flag after D (or never) -> BLINDSIDED -> lose.

HONEST FENCE: Hs is NOT a Go engine and this is NOT Go tactics -- a parable that ratio-blindness loses in
COMPETITION exactly as in monitoring (an absolute reader is blindsided by a proportional shift a relational
reader catches). Deterministic; receipt. Author: Peter Higgins (human authorship for all claims); AI-assisted
per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
T=60
b_stones=4.0; w_stones=4.0                    # stones: both place at the same rate -> margin stays ~0 (the blind metric)
b_ctrl=4.0; w_ctrl=4.0; contested=73.0        # control: White converts contested (the relational metric that turns)
abs_margin=[]; w_share=[]; rel_alert=None; blind_alert=None; decided=None
WIN=0.62; HS_GATE=0.55; BLIND_GATE=6.0
for m in range(T):
    b_stones+=1.0; w_stones+=1.0                                   # EVEN placement -> even board
    conv=0.4+0.05*m                                                # White's proportional conversion, increasing
    w_ctrl+=conv; b_ctrl+=0.30; contested=max(contested-conv-0.30,1.0)
    am=abs(b_stones-w_stones); ws=w_ctrl/(b_ctrl+w_ctrl)
    abs_margin.append(round(am,2)); w_share.append(round(ws,3))
    if rel_alert is None and ws>HS_GATE: rel_alert=m
    if blind_alert is None and am>BLIND_GATE: blind_alert=m
    if decided is None and ws>WIN: decided=m

hs_in_time=bool(rel_alert is not None and decided is not None and rel_alert<=decided)
blind_in_time=bool(blind_alert is not None and decided is not None and blind_alert<=decided)
margin_at_decided=round(float(abs_margin[decided]),2) if decided is not None else None
checks={
 "game_is_decided_proportionally": bool(decided is not None),
 "Hs_flags_in_time": hs_in_time,
 "blind_is_blindsided": bool(not blind_in_time),
 "board_looked_even_in_stones": bool(decided is not None and abs_margin[decided] < BLIND_GATE),
}
verdict=(f"CONSEQUENCE: the game is DECIDED at move {decided} (White's relational control crosses {WIN}); the Hs "
   f"player saw the turn at move {rel_alert} and acted in time, while the BLIND player -- reading only stone "
   f"counts -- saw an EVEN board (absolute margin {margin_at_decided}) and was BLINDSIDED (alert {blind_alert}). "
   "Ratio-blindness loses the proportional game it never saw turning.") if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"go_hs_vs_blind.py","what":"Go: an Hs (relational) player vs a blind (absolute-only) player","verdict":verdict},
     "decided_move":decided,"Hs_alert_move":rel_alert,"blind_alert_move":blind_alert,
     "Hs_responded_in_time":hs_in_time,"blind_responded_in_time":blind_in_time,
     "at_the_decided_move":{"absolute_stone_margin":margin_at_decided,"blind_threshold":BLIND_GATE,
        "white_relational_control_share":w_share[decided] if decided is not None else None,
        "reading":"the board looked EVEN in stones while the relational position had already turned -- deceptive drift, in a contest"},
     "checks":checks,
     "fence":("Hs is NOT a Go engine and this is NOT Go tactics -- a parable that ratio-blindness loses in "
        "COMPETITION exactly as in monitoring. Transparent synthetic contest. Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps({k:v for k,v in out.items() if k!="_meta"},sort_keys=True,default=str).encode()).hexdigest()[:16]
if __name__=="__main__": print(json.dumps(out,indent=2))
