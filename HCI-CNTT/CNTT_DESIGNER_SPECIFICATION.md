# CN‑TT v4 — Designer Specification (replicate it, and know when to use it)

*The complete picture for someone who wants to **reimplement** CN‑TT and **wield** it well — the code, the context, and the judgment of how/where/when/why. This is the distilled engine (core reads + lossless tiling + the 2026‑06 guard layer); the full frozen‑oracle binary adds the depth‑tower/IR‑class recursion, the CNQ quaternion bench, and EITT (`CNTT_COMPLETE_SPECIFICATION.md`). Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Honest‑broker; claim tiers at the end.*

---

## 1 · What CN‑TT is, in one paragraph

CN‑TT reads the **dynamics of compositional data** — data where only the *relative* sizes of the parts carry information (energy mixes, ion concentrations, mineral oxides, microbiome taxa, market shares, budget allocations — anything that is "a few components of a whole, tracked in some order"). It works in **Aitchison (log‑ratio) geometry**, reconstructs the full high‑dimensional structure **losslessly** from overlapping exact 4‑part charts, reads each step's structure, and emits a result with a **deterministic content hash** — same input, same output, same receipt, on any machine. It is an *instrument*, not a statistical model: it reads structure; the domain expert decides what it means. As of 2026‑06 it also **says what it cannot resolve** — it holds at rest, flags a fragile driver, calibrates its own noise floor, and (separately) can act only behind breakers.

## 2 · The "4 W" — how, where, when, why to use it

**WHO it's for.** A domain expert (or an AI assisting one) who has compositional data and wants a deterministic, auditable read of *who is driving change, when the system changed state, and how concentrated it is* — without building a statistical model or learning the full CoDa apparatus first.

**WHERE it fits.** As the **analysis stage** of a measurement chain: sensors/assays/surveys produce the composition; CN‑TT reads it. It contributes ≈ zero measurement variation (gauge R&R ≈ machine epsilon) and propagates the input's uncertainty; it does **not** replace the sensor or the domain model. It is an *extension of standard CoDa into dynamics* — for a single snapshot it falls back to the standard static apparatus (ternary/biplot/variation matrix) and imposes no dynamics.

**WHEN to reach for it (good fits):**
- the data is genuinely compositional (parts of a conserved whole), tracked over time / depth / dose / sample order;
- you suspect the *driver is not the biggest component* (ratio blindness) — CN‑TT's specialty;
- you need a **reproducible, hash‑receipted** read (audits, flight/medical/industrial, cross‑lab);
- you need to know *when* a system genuinely changed state, separated from noise.

**WHEN NOT to (honest limits):**
- the data is not compositional (absolute magnitudes matter independently) → use a magnitude method (that's MC‑1, not MC‑4);
- the table is **> ~50% zeros** → the log‑ratio geometry is replacement‑dominated; CN‑TT flags `GD‑SPZ‑WRN` and you should densify first (prevalence filter / agglomerate / Bayesian‑multiplicative), while the zero‑robust reads (K_eff, hold‑lock) still hold;
- you have 1–2 records, or motion below the noise floor → CN‑TT holds (`HM‑NUL‑WRN`) rather than invent a driver;
- you need a *causal* explanation → CN‑TT reads structure; causation is the expert's.

**WHY it works (the one idea).** A four‑part composition has exactly three log‑ratio degrees of freedom — the dimension of a quaternion rotation — so a 4‑part move is read **exactly** as a rotation, and higher‑D is **tiled** from overlapping exact 4‑part charts and stitched losslessly. No statistics, no lossy reduction; structure recovered exactly and deterministically.

## 3 · Architecture & data flow

```
RAW M[T×D] ─▶ carrier guard (E-21) ─▶ zero treatment ─▶ closure → CLR → ILR
           ─▶ lossless 4-part tiling (reconstruct full CLR; report error)
           ─▶ navigation family (K_eff · helmsman · regimes · deceptive drift)
           ─▶ guard layer (resolvability · coherent helmsman · effective rank · hold-lock · sparsity)
           ─▶ deterministic content hash ─▶ payload (+ conditional guard codes)
```
The full algorithm, stage by stage, is in **`CNTT_PSEUDOCODE.md`**. Reference implementations: **`tools/CNTT_single_cell.py`** (verified) and **`tools/cntt_single_cell.R`** (1:1 port).

## 4 · The components (what each does, and why it's there)

| Component | What it computes | Why it exists |
|---|---|---|
| **Carrier guard (E‑21)** | drops structurally‑zero carriers, flags constants, replaces sporadic zeros | a carrier never positive is undefined under log‑ratio → would crash the geometry with a silent `nan` |
| **Closure → CLR → ILR** | onto the simplex; centered & isometric log‑ratios | the natural geometry of relative data; Euclidean stats on raw shares are systematically wrong |
| **Lossless 4‑part tiling** | full CLR reconstructed from overlapping charts; error reported | exactness at scale without a bigger algebra; the *signature* CN‑TT capability |
| **Navigation family** | K_eff, helmsman, regime boundaries, deceptive drift | the actual reads a user acts on — who drives, when it changed, is it concentrating quietly |
| **Resolvability guard** | `HM‑NUL`/`HM‑TIE` + margin | refuse to name a driver at rest or break a tie by index — honesty about the read |
| **Coherent helmsman** | pairwise‑log‑ratio driver | a driver call robust to which carriers are in the panel (CLR's is not) |
| **Effective rank** | participation ratio of CLR singular values; `DG‑RNK` | the true dimensionality of the motion; degeneracy warning |
| **Hold‑lock** | discovered‑noise‑floor + hysteresis structural detector | separate genuine state changes from noise, self‑calibrated, chatter‑free |
| **Sparsity detector** | `GD‑SPZ` + the densify recommendation | tell the user when the log‑ratio read is an imputation artifact |
| **Content hash** | rounded‑float canonical SHA‑256 | the receipt — reproducibility *is* the proof |

Full diagnostic‑code registry: `CNTT_DIAGNOSTIC_CODES.md`. The safe closed‑loop controller and the precision layer: `PRECISION_AND_CONTROL.md`, `engine/loop_control.py`.

## 5 · Determinism contract (the property a replication must preserve)

1. No randomness in the science path; any sampling uses a fixed declared seed.
2. Round floats to a declared precision (12 dp) before hashing → receipts match **across platforms** (a value‑level guarantee, demonstrated: the Python cell produced an identical SHA‑256 on Windows and Linux).
3. Guard blocks attach **conditionally** (only when a code fires) → on clean data the payload and hash are identical with or without the guard layer. This is what lets the layer be added without re‑basing a frozen reference.
4. Byte‑identical cross‑*language* hashing additionally needs a shared canonical serialization — a Tier‑3 item; the ports each hash within their own language while reproducing all numeric reads.

## 6 · Conformance — how to know your reimplementation is correct

Run your port on the shared demo (D=8 synthetic energy mix, `seed=0`, in every reference file) and check:

- **lossless reconstruction error** ≈ machine floor (≤ 1e‑12; the references hit ~7e‑15);
- **helmsman = Solar**, and the **coherent helmsman** agrees;
- **K_eff** falls from ~6.1 to ~4.3 over the series;
- **effective rank** ≈ 3.1 of 7, and **`DG‑RNK‑WRN`** fires (motion is lower‑dimensional than D);
- the **hold‑lock** returns a small set of structural events; **regime boundaries** are reported.

If the numeric reads match, the port is faithful. (The content hash will match another run *in the same language*; cross‑language hash identity is the Tier‑3 serialization item.) For frozen‑oracle parity (the hashed run path), use `verify_hash_parity.py` against `run_cntt.py`.

## 7 · The replication kit (all in this repo)

| Artifact | Path |
|---|---|
| Language‑agnostic pseudocode | `HCI-CNTT/CNTT_PSEUDOCODE.md` |
| Python single cell (verified) | `tools/CNTT_single_cell.py` · `.ipynb` |
| Annotated replication notebook | `tools/CNTT_replication_notebook.ipynb` |
| R port (1:1 mirror) | `tools/cntt_single_cell.R` |
| This specification | `HCI-CNTT/CNTT_DESIGNER_SPECIFICATION.md` |
| Full engine spec (oracle + backlog) | `HCI-CNTT/CNTT_COMPLETE_SPECIFICATION.md` |
| Diagnostic‑code registry | `HCI-CNTT/CNTT_DIAGNOSTIC_CODES.md` |
| Capability delta (what's new) | `HCI-CNTT/ENGINE_CAPABILITIES_DELTA_2026-06.md` |
| Trust / metrology / confidence | `HCI-CNTT/DETERMINISM_GAUGE_RR_AND_CONFIDENCE.md` |

## 8 · Claim tiers

- The distilled engine (geometry, lossless tiling, navigation, the guard layer) and its determinism — **Tier 1** (implemented, self‑tested, cross‑platform hash demonstrated).
- The reconstruction theorem (lossless ⇔ connected overlap graph; Greenacre / graph‑Laplacian basis) and the quaternion 4‑part identification — **Tier 2** (standard math, soundly applied).
- Full frozen‑oracle parity of any reimplementation; byte‑identical cross‑language hashing; the depth‑tower/CNQ/EITT layers not in the distilled cell — **Tier 3** (to earn / see the full spec).

*Locked in the middle, contracted at the edges, hashed at every step. The instrument reads; the expert decides; the hash carries the receipt. Now it also tells you, honestly, where it cannot.*
