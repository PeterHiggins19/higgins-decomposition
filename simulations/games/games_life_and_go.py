#!/usr/bin/env python3
"""
games_life_and_go.py -- Hs as a MEASURE of two games. Hs does not play them; it READS the game's state as a
composition and reports its structure and motion.

GAME OF LIFE (a system under deterministic law): the board's texture = the composition over live-neighbour
counts {0..8}. As Life evolves, a random soup SETTLES into a stationary 'ash' composition (still-lifes +
oscillators) -- iterated lawful evolution converges to a FIXED POINT, measured by the TIME-AVERAGED composition
stabilising (robust to oscillators, which keep step-to-step velocity high while the long-run average is
constant). The recursion fixed point, made literal on a cellular automaton.

GAME OF GO (a competitive/decision system): the board is a 3-part composition {black, white, empty} that moves
move-by-move. Hs reads the helmsman (which colour reshapes the board), the directedness of the game (a march to
a result vs a balanced fight), and the leader -- the relational position, not the play.

HONEST FENCE: Hs READS the game-state composition; NOT a Life engine (the rules are the law) and NOT a Go
player/evaluator (an engine like AlphaGo plays; Hs measures the state's dynamics). The Go game here is a
transparent synthetic trajectory. Deterministic; receipt. Author: Peter Higgins (human authorship for all
claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib
def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,1e-9,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)
def aitch(a,b): return float(np.linalg.norm(clr(a)-clr(b)))
def eff_dim(v): v=closure(v); H=-np.sum(v*np.log(v+1e-300)); return float(np.exp(H))

# ===== GAME OF LIFE =====
def life_step(g):
    nb=sum(np.roll(np.roll(g,i,0),j,1) for i in(-1,0,1) for j in(-1,0,1) if not(i==0 and j==0))
    return ((g==1)&((nb==2)|(nb==3)))|((g==0)&(nb==3))
def ncomp(g):
    nb=sum(np.roll(np.roll(g,i,0),j,1) for i in(-1,0,1) for j in(-1,0,1) if not(i==0 and j==0))
    return closure(np.array([np.sum(nb==k) for k in range(9)],float)+0.5)
rng=np.random.default_rng(20260626); G=(rng.random((32,32))<0.30).astype(int)
comps=[]; pop=[]
for t in range(180):
    comps.append(ncomp(G)); pop.append(int(G.sum())); G=life_step(G).astype(int)
comps=np.array(comps)
def wavg(a,b): return closure(comps[a:b].mean(0))
early=aitch(wavg(0,20),wavg(20,40)); late=aitch(wavg(140,160),wavg(160,180))
helm_life=int(np.argmax(np.sum(np.abs(np.diff(clr(comps),axis=0)),axis=0)))
life={"steps":180,"pop_start":pop[0],"pop_end":pop[-1],"early_avg_drift":round(early,4),"late_avg_drift":round(late,4),
      "settled_to_stationary_composition":bool(late<0.3*early),"ash_eff_neighbour_classes":round(eff_dim(wavg(160,180)),2),
      "motion_helmsman_neighbour_count":helm_life,
      "reading":"lawful evolution converges to a stationary 'ash' composition (time-average stabilises) -- the recursion fixed point on a real CA"}

# ===== GAME OF GO (synthetic, transparent) =====
P=81; moves=60; black=2.0; white=2.0; empty=P-4.0; go_comps=[]; names=["black","white","empty"]
for m in range(moves):
    take_b=1.0+0.03*m; take_w=1.0
    black+=take_b; white+=take_w; empty=max(empty-take_b-take_w,1.0)
    go_comps.append(closure([black,white,empty]))
GC=clr(np.array(go_comps))
path=float(np.sum(np.linalg.norm(np.diff(GC,axis=0),axis=1))); net=float(np.linalg.norm(GC[-1]-GC[0]))
mover=names[int(np.argmax(np.sum(np.abs(np.diff(GC,axis=0)),axis=0)))]; final=go_comps[-1]
go={"moves":moves,"final_composition":{names[i]:round(float(final[i]),3) for i in range(3)},
    "directedness":round(net/path,3) if path else None,"motion_helmsman":mover,"leader":names[int(np.argmax(final[:2]))],
    "reading":"the board as {black,white,empty} in motion: helmsman = the colour reshaping it, directedness = a march to a result vs a balanced fight; Hs measures the position, it does not play"}

checks={
 "life_settles_to_fixed_point": bool(life["settled_to_stationary_composition"]),
 "life_read_is_compositional": bool(life["ash_eff_neighbour_classes"]>1),
 "go_has_helmsman_and_direction": bool(go["motion_helmsman"] in names and go["directedness"] is not None),
}
verdict=(f"Hs MEASURES THE GAMES: Life's lawful evolution SETTLES to a stationary ash composition (avg drift "
   f"{life['early_avg_drift']}->{life['late_avg_drift']}, a fixed point); Go reads as {{black,white,empty}} in "
   f"motion -- helmsman '{go['motion_helmsman']}', directedness {go['directedness']}, leader {go['leader']}. One "
   "is a system under law converging; the other a contest in motion -- both as compositions.") if all(checks.values()) else "CHECK FAILED"
out={"_meta":{"tool":"games_life_and_go.py","what":"Hs as a measure of the Game of Life and the Game of Go","verdict":verdict},
     "game_of_life":life,"game_of_go":go,"checks":checks,
     "fence":("Hs READS the game-state composition; NOT a Life engine (rules are the law) and NOT a Go player/"
        "evaluator (an engine plays; Hs measures the dynamics). The Go trajectory is transparent synthetic. "
        "Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps({"life":life,"go":go,"c":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]
if __name__=="__main__": print(json.dumps(out,indent=2))
