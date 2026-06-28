# Control authority & governance — the distributed open/closed-loop surface

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. Seed/concept —
2026‑06‑20. How control authority is distributed across a constellation‑scale Hˢ deployment: **closed‑loop
autonomy down the chain where speed and scale demand it; open‑loop operator go/no‑go up the chain where a
human still holds the breaker.** This is not a new invention — it is the constellation reading of doctrine
the repo **already holds and has partly tested.** Tiered.*

---

## 1. The principle (Peter's refinement, in one line)

> Keep open‑loop control — just **move it up the chain** to where a single operator / mission‑control can
> still hold the whole picture. Put **closed‑loop control down the chain**, where millions of operations a
> second across millions of distributed nodes mean **no human could ever be in the loop**. Breakers at
> **every** level, each able to trip, report, find an alternate safe route, and leave a traced, documented
> evidence chain — and at the top, an operator who receives the correct picture and an evidence‑backed
> **recommendation**, not an error message, and renders a **go/no‑go**.

This resolves the controller‑vs‑observer tension I had flagged. The answer is not "human gates everything"
(impossible at scale) nor "automation decides everything" (unsafe). It is a **layered authority surface**:
autonomy where it must live, human judgment where it can live, and a breaker discipline binding the two.

## 2. This is already the repo's doctrine — "check us out" (verified)

A direct search of the Hˢ repo confirms the architecture Peter describes is **built and, in large part,
tested** — it is named, inventoried, and exercised:

| element | where it lives in the repo | status |
|---|---|---|
| **LOOP‑001 (Skydiver Principle)** — "the operator holds the last breaker; 16 breakers; Breaker 16 is held by the human and cannot be overridden by automation" | `HCI-CNT/handbook/GLOSSARY.md` | **doctrine, codified** |
| **SAFE‑001** — Breaker 16 = the final separation between the HUF‑GOV **instrument** (open loop) and the HUF‑CLS **actuator** (closed loop); "no code can enforce Breaker 16, only the operator can" | `huf-gov/README.md`, `huf-gov/BREAKER_INVENTORY.md` | **doctrine, codified** |
| **HUF‑GOV charter** — "Open‑loop operation shall take priority over closed‑loop automation **unless closure is explicitly justified, reviewable, and answerable to responsible authority.** HUF‑CLS may optimize correction. HUF‑GOV protects judgment." | `huf-gov/HUF_GOV_INTEGRATION.md` | **charter** |
| **16‑breaker inventory + test** — 16 governance circuit breakers; **12 tripped cleanly under test, 3 soft/doctrinal, 1 honest gap found** | `huf-gov/BREAKER_INVENTORY.md`, `papers/HUF_GOV_BREAKER_TEST_2026-05-12.md`, `huf-gov/tools/breaker_test_runner.py` | **TESTED (re‑runnable)** |
| **Distributed control + coherence‑weighted leader election** — every node can lead; all‑watch‑all; non‑contact; elect on **coherence** (the Hˢ‑native criterion); re‑elect on degradation; Dante/PTP/Raft/Paxos precedent | `HCI-CNTT/DISTRIBUTED_CONTROL_AND_LEADER_ELECTION.md`, `HCI-CNTT/CONTROL_POINTS_AND_REMOTE_ADAPTATION.md` | **design (T2 on T1 parts)** |
| **FDIR / Fault Management** — a **Coherence Supervisor** as fault authority; fault classes (bit‑flip, sensor drift, method drift, config/command, processor/watchdog) each with **Detection / Isolation / Recovery**; watchdog → failover → SAFE mode; `ROLLBACK` to last‑good; **escalate to operator** | `collaborations/geology-wehner/flight_spec_suite/HGS-005_Fault_Management_FDIR.md`, `CNTT_FLIGHT_CONTROL_SPEC.md` | **flight spec, Draft A / Pre‑Phase A** |
| **Mission Control** — operator at the top, one master‑control JSON, fully‑provenanced deterministic output | `HCI/MISSION_CONTROL_PLAN.md`, `HCI-CNT/mission_command/master_control.json` | **plan + control file** |
| **Double‑Verify & Staged‑Recovery (DVR‑1.0)** — lose nothing · double‑verify before+after · reversible stages with a **human gate between stages** · recovery at every stage | `ai-refresh/DOUBLE_VERIFY_AND_RECOVERY_PROTOCOL.md` | **codified protocol** |
| **Control engine code** — loop + stage controllers | `HCI-CNTT/engine/loop_control.py`, `stage_controller.py` | **code** |

So the claim "pass‑up/pass‑down administration control channels, already created and tested" is
**substantially accurate.** The primitives — breakers, the GOV/CLS open/closed fork, leader election, FDIR,
mission control, staged recovery — exist; the governance breakers are tested and re‑runnable; the operator
authority (Breaker 16 / LOOP‑001) is the named, load‑bearing top of the chain.

## 3. Where Breaker 16 goes when the system scales (the honest evolution)

SAFE‑001 today says **Breaker 16 lives inside the operator** and "holds only because Peter holds it." Peter's
new framing is the **planned evolution**, and it is faithful to the existing charter rather than a break from
it:

- **Down the chain:** at the millions‑of‑ops/sec leaf level, no operator can be in the loop, so **closure is
  the justified case** — exactly the charter's "*unless closure is explicitly justified, reviewable, and
  answerable to responsible authority.*" Local Hˢ controllers run **closed‑loop (HUF‑CLS)** under prepared
  rules, full breakers, FDIR, and a traced evidence chain. Breaker 16 **closes locally**.
- **Up the chain:** Breaker 16 does **not disappear** — it **re‑appears at the top** as the
  **mission‑control / single‑operator go/no‑go** (open‑loop, HUF‑GOV). The human still holds the last
  breaker; it has simply moved to the only place a human can hold it at scale.
- **Between them:** the **pass‑up/pass‑down admin channels** carry health, coherence, breaker‑trip reports,
  and escalations up; authority, rule‑updates, and go/no‑go down. Each level is **answerable to the level
  above** — which is precisely what the charter requires for justified closure.

So "Breaker 16 is closed" (Peter's phrase) is true **locally and necessarily**, while the operator's Breaker
16 is **preserved globally** at mission control. The doctrine is not violated by closing the loop at the
bottom; it is **honored by keeping it open at the top.**

## 4. The smart controller — prepared rules, fallbacks, emergency composition‑balancing

The closed‑loop leaf controller Peter describes is a **smart controller with the rules well prepared** and a
**series of fallbacks and safety considerations**. Its Hˢ‑native shape:

1. **Deterministic, governed action.** Every control decision is a deterministic, hash‑receipted function of
   the composition state + the governance ruleset — reproducible and auditable after the fact.
2. **Breakers at every level.** A trip → (a) **reports** up‑channel with the evidence, (b) **isolates** the
   fault (FDIR), (c) **finds an alternate safe route** (re‑route / re‑elect leader / failover / `ROLLBACK`),
   (d) **traces and documents** the whole event.
3. **Emergency = balance the composition, then recommend.** In a crisis the controller does what Hˢ is for —
   **balance the composition** (read what is actually steering, what is real vs a fault) and **determine
   courses of action** under determinism + governance — and, at the operator boundary, present a **go/no‑go
   with an evidence chain and real‑data recommendation, not just an error message.** This is the single most
   important UX/safety property: the operator receives *the correct picture and proper advice*, and decides.
4. **Graceful degradation.** If evidence is insufficient, the guard layer **holds / drops to SAFE mode**
   rather than acting on a confident falsehood — the P3 guard discipline, now distributed.

## 5. The hard part — and it IS the real work

Peter is right that this is the real work: a **distributed manual/automatic gated control surface** where
*every element is Hˢ, every composition is under Hˢ control with full safeties at every level, all
integrated.* The genuine difficulties (named honestly, none solved here):

- **Authority boundaries.** Drawing the exact line at each level between autonomous action and required
  escalation — and proving it stable — is delicate control‑systems + governance engineering.
- **Stability under closure.** Closed loops at the bottom must be provably stable and must not interact
  pathologically with neighbours (the "thrashing" risk) — needs control‑theoretic analysis, not just
  determinism.
- **Latency budget.** Go/no‑go up + authority down must fit the decision‑speed envelope at every tier.
- **Safety case.** A real deployment needs a formal safety case (FDIR coverage, breaker independence,
  failure‑mode analysis) of the kind HGS‑005 begins but a flight program completes.
- **Verification.** Every breaker, at every level, needs the kind of mechanical test the 15 governance
  breakers already get — extended to the constellation control surface.

## 6. Tiers (honest)

- **Tier 1 / tested:** the 16 governance breakers (15 tested, re‑runnable), DVR‑1.0 staged recovery,
  engine loop/stage controllers, determinism + receipts.
- **Tier 2 / designed on tested parts:** coherence‑weighted distributed leader election; the FDIR /
  Coherence‑Supervisor flight spec (Draft A, Pre‑Phase A); Mission Control plan; the GOV/CLS open/closed
  fork.
- **Tier 3 / 3+ (horizon):** the **constellation‑scale integrated control surface** — millions of
  distributed closed‑loop Hˢ controllers with Breaker 16 closed locally, escalating up tiered admin
  channels to an operator go/no‑go — is the **documented eventual goal**, **not built or deployed**. No
  performance, latency, or safety figure is claimed; the safety case is unwritten.

*The operator holds the last breaker — it just moves to the top. Everything below runs closed, governed,
breakered, traced, and answerable upward. Complement, not replacement. Peter is the sole gate; no external
engagement implied. Cross‑refs: [`TOTAL_SYSTEMS_COHERENCE.md`](TOTAL_SYSTEMS_COHERENCE.md),
`../../huf-gov/BREAKER_INVENTORY.md`, `../../HCI-CNTT/DISTRIBUTED_CONTROL_AND_LEADER_ELECTION.md`,
`../../collaborations/geology-wehner/flight_spec_suite/HGS-005_Fault_Management_FDIR.md`.*
