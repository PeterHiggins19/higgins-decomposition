# From your data to an Hˢ insight — an AI-assisted onramp for domain experts (no CoDa required)

*The PhD onramp. For a researcher who is expert in their field X but has no time or appetite to learn compositional data analysis (CoDa) before knowing whether it is worth it. The deal is inverted: you do not learn CoDa, apply it, and then decide if it helped. Instead you bring X, and an AI runs Hˢ for you and tells you what your data says, why it matters, and how — in your language. Author: Peter Higgins (human authorship); AI-assisted per HUF-STD-001. Honest-broker; the engine reports low/no signal when that is the truth.*

---

## The choice this removes

The old path: invest weeks learning the simplex, log-ratios, and Aitchison geometry; re-tool your analysis; apply it to X; *then* judge whether it told you anything. High cost, deferred and uncertain payoff — so most field-capable researchers never start.

The onramp path, in one sentence you can say to an AI: **"I have X. Run it through Hˢ and tell me what my data would inform me of — what is useful, what I should care about, and why."** You stay in your domain; the AI carries the CoDa. If there is something worth your attention, you see it in one sitting. If there is not, the instrument says so — honestly — and you have lost an afternoon, not a quarter.

## We name every reading twice — your language and a physicist's

By standing rule (`HCI-CNTT/TERMINOLOGY_BRIDGE.md`), every quantity is given **both** a navigation/systems term **and** a physics term, plus a plain meaning — e.g. *the helmsman (the steerer / the fastest‑moving part)*, *the arrow of intent (momentum / mass × velocity)*, *the hold‑lock (station‑keeping / at rest)*. So you read it in whichever register you think in, and carry it to your peers in theirs — the translation is done for you.

## What Hˢ reads (and the plain question each answers)

Any data that is **parts of a whole, tracked over an ordering** (time, depth, dose, baseline, age, sample index) is compositional, whether or not you have ever called it that: gas fractions, ion concentrations, mineral oxides, taxa abundances, market-cap shares, land-cover fractions, energy mix, vote shares, budget allocations. For such data Hˢ returns a small, fixed set of readings — and each maps to a question you already ask:

| Hˢ reading (the CoDa name) | The plain question it answers |
|---|---|
| **Lossless reconstruction error** | Did the analysis distort my data? (No — exact to ~1e‑15; it is a trust certificate, not a claim.) |
| **Helmsman** (largest log‑ratio mover) | *Who is actually driving the change?* — and it is often **not** the biggest component. |
| **Regime boundaries** | *When did the system change state?* — datable, automatic, no prior labeling. |
| **K_eff / effective diversity** | *Is my system concentrating or spreading out?* — and is it doing so quietly? |
| **Activation coefficient** (a.k.a. yeast factor) | *Is a tiny component doing outsized work?* — the early-warning a threshold would miss. |
| **Deceptive drift** | *Is something shifting under cover of calm?* — concentration without the velocity you'd expect. |
| **Across cases** | *Does the same driver hold across my cohort?* — replication, the honest road to confidence. |

The single most common surprise, across every domain we have run, is the helmsman: **the component that drives the compositional change is frequently a minor one, because magnitude and ratio live in different worlds.** In Williston-Basin brines the action was in the trace sulfate and bicarbonate, not the Na-Cl bulk. In Lower-Cretaceous mudstones it was trace Zr/Rb, not the silica/alumina bulk. That is the thing a magnitude-only instrument is structurally blind to (we call it ratio blindness), and it is usually the thing worth your attention.

## If you only want the static picture — the standard CoDa apparatus, nothing more

Not everyone needs dynamics, and Hˢ does not impose them. If your data is a single snapshot or a cross-section (no time axis), or you simply want the standard compositional analysis you already trust, Hˢ gives you exactly that and stops there: the **ternary diagram** (for D=3 sub-compositions), the **CLR biplot** (Aitchison–Greenacre), the **variation matrix**, the **CLR‑PCA scree**, and the **balance dendrogram** — the standard static CoDa apparatus, computed by the atlas Stage‑2 step (`HCI-CNT/atlas/stage2_locked.py`; an R port exists). These outputs live under a `coda_standard/` key, kept separate from the Higgins extensions, so a CoDa colleague can read only the familiar quantities and ignore the rest.

This is the honest face of the stance: **Hˢ is an extension of standard CoDa into dynamic systems analysis — the dynamic layer is offered, never forced.** A geochemist with one cross-sectional dataset gets a clean ternary/biplot and is left entirely alone; the trajectory, helmsman, and regime readings below are there only for those whose data moves in time and who want them.

## The intake — five minutes, in your words

An AI running this protocol asks only what it needs to map X onto the readings above. You answer in domain terms; you never need a CoDa word:

1. **What are the parts?** List the components that sum to a whole (e.g., the 7 ions, the 9 fuels, the OTUs). Don't pre-filter for "importance" — the point is to find the non-obvious driver.
2. **What is the ordering?** Time, depth, age, dose, baseline-to-followup, or just sample index. (Even a cross-section works — Hˢ then reads structure across the section.)
3. **What would surprise you, or cost you, if you missed it?** A regime change, a hidden driver, an early warning, a quiet concentration. This tells the AI which reading to lead with.
4. **What is your data's noise floor?** Roughly — measurement precision, detection limits, how many zeros. (Hˢ discovers its own floor too, but your estimate sharpens the honest/withhold line.)
5. **What would make this worth your time?** One concrete thing you'd act on. The AI checks whether Hˢ can speak to it before running.

If the data is not really compositional, or is too sparse/short to resolve, the honest answer at step 5 is "this won't tell you what you need" — given *before* you invest, not after.

## The output — what you get back, and the shape of it

For your X, the AI returns the four-element certificate every Hˢ run produces, translated into your domain:

1. **What went in** — the parts, the ordering, the source, the size. (Reproducible.)
2. **Trust certificate** — the reconstruction error (~1e‑15) — proof the reading didn't distort your data.
3. **Who is driving** — the helmsman lineage: which component(s) carry the compositional change, when each leads, and the explicit note when it is a *minor* component (the ratio-blindness catch).
4. **When it changed** — the regime boundaries, dated against your ordering, with the activation-coefficient and deceptive-drift flags where they fire.

Then the part that earns your time: **"here is what this means in your field, and what you might do about it"** — phrased as a hypothesis for you, the domain expert, to accept or reject. Hˢ is the instrument; you remain the scientist. It flags; you decide.

## Why this is worth a PhD candidate's afternoon

- **Fast value, low cost.** You see whether your data has a hidden driver, a datable regime shift, or an early-warning signal without re-tooling your research around CoDa.
- **A boost into the community.** If it surfaces something real, your next paper carries the basic CoDa methods *intact and correctly applied* — which is exactly what the field wants more of, and it puts your name in the room early.
- **It makes ratio blindness visible.** Most researchers eventually arrive at the realization that single-channel/magnitude monitoring misses the ratio story — but few have the time, interest, or platform to publish it. Each onramp run is a small, concrete demonstration of it on real domain data, which is how an industry-wide blind spot becomes an aware topic.
- **It is honest.** When the answer is "no signal" or "your global composition doesn't separate — the signal is sparse, use your domain's targeted method," it says so (see the Crohn and spaceflight runs). That honesty is what makes the *positive* readings trustworthy.

## The honest envelope (so the value is real)

- Hˢ analyzes the data you give it; it does not replace your sensors or your domain model. It removes the *computation* uncertainty (it is deterministic and lossless) and propagates yours — it does not remove sampling/measurement uncertainty. (See `HCI-CNTT/DETERMINISM_GAUGE_RR_AND_CONFIDENCE.md`.)
- Confidence is bounded by your data, not manufactured by the engine. Actionable claims clear a stated gate; otherwise the instrument withholds. High confidence comes from **replication across your cases**, not from one run.
- At extreme sparsity (e.g., 90%-zero tables) the log-ratio reading is densification-dependent; Hˢ flags the regime and the zero-robust reads (diversity, regime null) still hold. (See `experiments/sparsity_microbiome_2026-06/`.)
- Nothing here is acquisition or endorsement; interest expressed is never acquired. Peter is the sole contact/commit gate.

## How to start

Bring your X to any AI with this repo's context and say the one sentence. The AI follows `Hs/onramp/AI_ASSIST.json` (the machine-readable intake), maps your data to the readings, and — where helpful — points you at the closest worked example in `Hs/onramp/WORKED_EXAMPLES.md` (gas, water chemistry, core geology, microbiome, transcriptome, energy, social science). You read one document in your own field's shape and decide if Hˢ just told you something you should care about.
