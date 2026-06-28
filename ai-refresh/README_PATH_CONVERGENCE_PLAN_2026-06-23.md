# README + path convergence plan — converge the front door on the latest principles (2026-06-23)

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. A **plan**, not a bulk
rewrite: it names the latest principles now defined, and maps exactly which READMEs/paths change to converge
on them — to be **applied on the LIVE repos** (the CoWorker mirror is stale/behind on all three; never copy a
mirror file over a newer published file — see `PRE_PUSH_READINESS_2026-06-22.md` §1.5). Nothing pushed; Peter
is the sole gate.*

---

## 1. The latest principles the front door must converge on

These are the load-bearing ideas defined across the recent sessions (G-145 → G-169). The front door currently
predates most of them.

1. **The flag / the niche** — Hˢ is *the deterministic, hash-receipted, exact reader of compositions, for
   decisions that must be auditable.* Who needs it = the **intersection** of (compositional data) **and**
   (audit-critical output). Source: `papers/WHERE_HS_BELONGS.md`, `papers/HONEST_COMPETITIVE_SCOPING.md`.
2. **The system is the message / CMP (P8)** — the discriminative signal lives in the inter-part log-ratios;
   the relational read beats scalar aggregates (measured on microbiome). Source:
   `papers/COMPOSITIONAL_MESSAGE_PRINCIPLE_PAPER_SEED.md`, `library/THE_SYSTEM_IS_THE_MESSAGE.md`.
3. **Located by three (the Triangulation Trilogy)** — one law, three measured witnesses (microbiome / mudstone
   / fleet), the constellation as the reach supported by the three. Source: `papers/TRIANGULATION_TRILOGY_PLAN.md`.
4. **Determinism → transitive trust** (not transitive truth); the receipt certifies the *reading*. Source:
   `papers/DISTRIBUTED_CONTROL_TETRAHEDRAL_3N_PAPER_SEED.md` §3a, root `TRUST_AND_VERIFICATION.md`.
5. **SO(4) / dual-quaternion 6-DOF — now T1 (built + receipted)**, no longer a future-only note. Source:
   `experiments/so4_dualquaternion_2026-06/`, `papers/frontier/SO4_SPIN4_FUTURE_COMPONENT.md` §5.
6. **The Proof & Honesty Standard** — the four checks are a standing gate on every front-door claim. Source:
   `papers/PROOF_AND_HONESTY_STANDARD.md`.

## 2. The convergence map — which README/path changes, and to what

Priority: **P0** = the public first-screen; **P1** = section front doors; **P2** = supporting indexes.

| path | current role | converge-to change | prio |
|---|---|---|---|
| `README.md` (root) | three-level front door | add **one** line under the qualifier: the flag sentence (§1.1) + a pointer to `papers/WHERE_HS_BELONGS.md`; ensure the "located by three" framing is the headline of the research claim, not the SpaceX reach | **P0** |
| `IS_Hs_RIGHT_FOR_YOU.md` | self-qualify front door | lead with the **two-part qualifier** (compositional ∧ audit-critical); it currently lists domains without the intersection gate | **P0** |
| `papers/README.md` | publication index | reorder to the **published spine**: P1+P3 → witnesses (W-I/W-II/W-III) → capstone → P7/P8; mark SO(4) row **T1 built**; link the Proof & Honesty Standard once at top | **P1** |
| `papers/frontier/README` (if absent, the cluster index) | frontier map | move the SO(4) line from "future component" to **"built — see experiments/so4_dualquaternion_2026-06/"** | **P1** |
| `industrial-instruments/README.md` | applications front door | thread the flag + the niche intersection; point constellation/financial/fleet rows at their measured witness | **P1** |
| `INDUCTION_MAP.md` / `.json` | traversal map | add nodes: WHERE_HS_BELONGS, CMP/P8, the SO(4) build, Proof & Honesty Standard | **P1** |
| `papers/ABSTRACT_LEDGER.md` | intent ledger | already carries P8 + trilogy; add a one-line **SO(4) built** note under the frontier mention | **P2** |
| `HS_GUIDE.md`, `QUICKSTART.md`, `EXECUTIVE_SUMMARY.md` | orientation | light touch: ensure the one-line value prop matches the flag verbatim (consistency, not expansion) | **P2** |
| `llms.txt` | machine front door | refresh the one-paragraph description to the flag sentence | **P2** |

**Cross-repo (HUF / RWA):** the shared Level-1 README block is **unchanged** this work — the flag is an Hs-level
sharpening, not a charter change. Only propagate to HUF/RWA if the shared block's one-line value prop is edited;
otherwise leave their front doors alone (no parity change needed).

## 3. The discipline for applying this (so it stays honest + safe)

- **Apply on the live repo, file by file** — re-apply each change onto the *current published* version
  (the mirror is behind +6 on Hs); never overwrite a newer live README with a mirror copy.
- **Consolidate, don't expand** — every change above is a *pointer or a one-liner*, not a new document. The
  principles already have homes; the front door only needs to *route* to them. No new top-level files.
- **Each edited claim carries its tier** and passes the four Proof & Honesty checks; the SO(4) line says
  **T1 capability / T2 application**, not "leader."
- **One verification pass** after applying: links resolve, the flag sentence is byte-identical everywhere it
  appears, no "first/lossless/proven-universal," tiers intact.

## 4. Sequence

1. P0 (root README qualifier line + IS_Hs two-part gate) — the first screen.
2. P1 (papers/index reorder, frontier SO(4) move, industrial front door, induction map).
3. P2 (guides/quickstart/llms.txt consistency pass).
4. Verification pass → fold into the next `PRE_PUSH_READINESS` manifest. Peter gates the push.

*This plan changes routing and one-liners only; the substance lives in the linked sources. Cross-refs:
`papers/WHERE_HS_BELONGS.md`, `papers/PROOF_AND_HONESTY_STANDARD.md`, `PRE_PUSH_READINESS_2026-06-22.md`,
`COWORKER_SYSTEM_REVIEW_2026-06-22.md`. Peter is the sole gate; nothing pushed.*
