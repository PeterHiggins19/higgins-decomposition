#!/usr/bin/env python3
"""
conference_kinetics.py -- CoDa on itself, IN MOTION. When Peter walked into CoDaWork2026 the community ran a
compositional study on the attendees and kept experimenting all week -- CoDa is already self-referential. The
one thing he is known for working on is KINETICS (the simplex in motion: velocity, momentum, the arrow -- the
P4 movement). A static attendee snapshot has no motion; this adds it: read the conference's OWN programme as a
composition that MOVES through topic-space as it unfolds, with the kinetic operators. Composition reading
itself, now with an arrow.

Method (deterministic): take the sessions in real programme order; each carries a topic; accumulate the running
topic composition session by session; read the clr trajectory kinetically -- per-step velocity, the
MOTION-HELMSMAN (the topic the conference's attention moves toward as it unfolds), and directedness.

HONEST FENCE: a METHODOLOGICAL ILLUSTRATION of compositional kinetics on a self-referential composition, from
the public programme order -- NOT a claim that conference 'dynamics' mean anything beyond the programme
sequence. It shows what kinetics ADDS to a static CoDa read. Deterministic; receipt. Author: Peter Higgins
(human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-26. Peter is the sole gate; nothing posted.
"""
import numpy as np, json, hashlib

TOPICS=["Methods/Foundations","Microbiology","Earth sciences","Health","Social sciences"]
# CoDaWork2026 sessions in real programme order (from the public schedule); each -> its topic
ORDER=["Methods/Foundations","Microbiology","Methods/Foundations","Earth sciences","Health",
       "Social sciences","Methods/Foundations","Health","Health","Methods/Foundations",
       "Methods/Foundations","Microbiology"]
EPS=0.05   # small mass on non-active topics so the running composition is strictly positive (clr-safe)

def closure(v): v=np.asarray(v,float); return v/v.sum(-1,keepdims=True)
def clr(v): v=closure(np.clip(v,1e-9,None)); g=np.exp(np.mean(np.log(v),-1,keepdims=True)); return np.log(v/g)

# accumulate the running topic composition session by session
acc=np.full(len(TOPICS),EPS); traj=[]
for s in ORDER:
    acc=acc.copy(); acc[TOPICS.index(s)]+=1.0; traj.append(closure(acc))
traj=np.array(traj); C=clr(traj)

# kinetics
vel=np.diff(C,axis=0)
net=C[-1]-C[0]                                                  # the arrow over the whole conference
motion_helm=TOPICS[int(np.argmax(net))]                         # topic attention moves TOWARD
motion_recede=TOPICS[int(np.argmin(net))]                       # topic attention moves AWAY from (relatively)
path=float(np.sum(np.linalg.norm(vel,axis=1))); netlen=float(np.linalg.norm(net))
directedness=round(netlen/path,3) if path else None
final_mix={TOPICS[i]:round(float(traj[-1][i]),3) for i in range(len(TOPICS))}
# per-step current motion-helmsman (which topic each session pushes most)
step_helm=[TOPICS[int(np.argmax(np.abs(v)))] for v in vel]

checks={
 "trajectory_has_motion": bool(path>0.5),
 "motion_helmsman_identified": bool(motion_helm in TOPICS),
 "directedness_in_range": bool(directedness is not None and 0<=directedness<=1),
}
verdict=(f"KINETICS ON A SELF-COMPOSITION: the conference opens on {ORDER[0]} and its topic-attention MOVES "
   f"toward {motion_helm} as it unfolds (directedness {directedness}); the arrow and the motion-helmsman are "
   "exactly what kinetics adds to a static CoDa read -- on a composition of itself.") if all(checks.values()) else "CHECK FAILED"

out={"_meta":{"tool":"conference_kinetics.py","source":"CoDaWork2026 public programme order",
              "what":"compositional kinetics (P4) on the conference as a composition of itself","verdict":verdict},
     "final_topic_mix":final_mix,
     "kinetics":{"motion_helmsman_toward":motion_helm,"relatively_recedes":motion_recede,
        "directedness":directedness,"path_length":round(path,3),"net_arrow_length":round(netlen,3),
        "per_session_push":step_helm},
     "reading":("the static read says WHAT the conference is made of (Methods/Foundations + Health dominant); "
        "the KINETIC read says WHICH WAY its attention moves as it runs -- the arrow. Static = the noun, "
        "kinetics = the verb. The same instrument, on the same self-composition, with motion added."),
     "fence":("Methodological ILLUSTRATION of compositional kinetics on a self-referential composition, from the "
        "public programme ORDER -- not a claim that conference dynamics mean more than the sequence. Shows what "
        "kinetics adds to a static CoDa read. Peter is the sole gate; nothing posted.")}
out["_meta"]["receipt_sha256"]=hashlib.sha256(json.dumps(
    {"final":final_mix,"kin":out["kinetics"],"checks":checks},sort_keys=True,default=str).encode()).hexdigest()[:16]
if __name__=="__main__": print(json.dumps(out,indent=2,ensure_ascii=False))
