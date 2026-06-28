# The honest scope — and why diffraction and dispersion are home

*Author: Peter Higgins (human authorship for all claims); AI-assisted per HUF-STD-001. 2026-06-25. A
scientific scoping of the filter-injection probe: stated as conditions, not claims — exactly where the
deterministic read is exact, where it is partial, and why the domain it began in (diffraction and
dispersion) is the one where its boundary all but disappears. Honest-broker tiered; nothing posted; Peter is
the sole gate.*

---

## The read, written as a condition (the deterministic core)

Model a measured return over bands `f` as

```
   r(f) = ref(f) · g · s(f) · m(f)  +  n(f)
```

| term | what it is | what the clr differential does to it |
|---|---|---|
| `ref(f)` | the **known reference / injected filter of known properties** | differenced out **by construction** |
| `g` | a **scalar** multiplicative common-mode (coupling, source level, dilution, bulk gain) | **cancels exactly** — `clr(g·x)=clr(x)` |
| `s(f)` | the **unknown structure** we want | **recovered** (this is the read) |
| `m(f)` | a **multiplicative shaping** (per-band gain, geometry, dispersion) | **only its geometric-mean removed**; the *shape* survives unless known |
| `n(f)` | **additive** noise / offset / interferer | **not removed** — sets the floor |

This is the whole truth in one line: **the read is exact for the part of the perturbation that is
multiplicative and either scalar (`g`) or known (foldable into `ref`); it is partial for an unknown
multiplicative shape (`m`), and it fails for the additive part (`n`).** Everything the instrument claims
follows from this factorization, and nothing beyond it.

## Where it is genuinely useful (the exact slice)

When the dominant nuisance is a **scalar multiplicative common-mode** and the signal lives in **proportions**,
the instrument is excellent and the cancellation is exact — verified to the numerical floor on three real
public datasets (`instrument/HITS_AND_MISSES.md`). That slice is large and real: couplant variability, sensor
gain drift, source droop, dilution, bulk coupling — across gas blends, spectral band power, ion panels, fleet
telemetry.

## Where the real world bites (stated, not hidden)

- **Variable geometry / non-rigid motion** → an *unknown* per-band shaping `m(f)`. clr removes only its mean;
  the rest leaks into the read. **Partial.** (Out-of-plane decorrelation is the irreducible floor — max Q.)
- **Variable mass** → if the bulk is nuisance, closure rejects it for free; if the bulk **is** the signal,
  closure discards it — the **mass-blind** case — and the momentum/size channel must be brought back.
- **Additive noise** → `n(f)` is not the differential's job; precondition the raw signal first.
- **A real structural change** → this is `s(f)` moving, i.e. **signal, correctly kept** (the instrument
  cancels *motion*, never *change*).

A generic part with arbitrary mass and geometry sits in the partial regime. Overstating the exact result
there would be the dishonest move; the factorization above is the honest bound.

## Why diffraction and dispersion are home — and it is not nostalgia

In the domain the framework began in, the two failure axes above turn **lawful**, and a lawful perturbation
is one the deterministic read can be **told to expect** rather than be fooled by:

- **Diffraction is natively compositional.** A conserved radiation budget apportioned across dimensions *is*
  a composition on the simplex — the framework was **forced** by that structure (DADC), not grafted onto it.
  There, "variable geometry" is not an unknown `m(f)` corrupting the read; it **is** `s(f)`, the read itself.
  The thing the method struggles with on a generic part is the literal signal in a diffraction pattern.
- **Dispersion is a knowable filter you fold into `ref`.** Frequency-shaped propagation — the very `m(f)`
  that bounds the method in a generic case — has a **known law** `D(f)`. Set `ref'(f) = ref(f)·D(f)` and the
  shaping joins the part that cancels by construction; the residual is read exactly. **The named limit
  becomes a handled case precisely when the shaping is lawful and known** — which, in dispersion, it is.

That is the deterministic discipline doing the work: **model the known physics into the reference; read what
remains exactly; and never claim past `ref`.** The home domain is not the easy case — it is the case where
the world's variability is on the instrument's terms, because there the variability is *lawful*, and lawful
shaping is foldable.

## Tiers (true to determinism)

- **T1 (exact):** the scalar-`g` cancellation, and any shaping folded into a **known** `ref` — proven,
  receipted, reproducible.
- **T2 (model):** the realizations here (ultrasonic, tissue) use grounded synthetic physics; numbers are
  model numbers.
- **T3 (to earn):** real RF/field data with a measured dispersion law folded into `ref`; the
  Paired-Measurement reference channel for shapings not known a priori.

The boundary is part of the result. The instrument is exact exactly as far as its reference models the
physics, and it says so.

*Cross-refs: `THE_FILTER_INJECTION_PROBE.md`, `THE_STREAMING_TISSUE_PROBE.md`, `instrument/INSTRUMENT_DATASHEET.md`,
`instrument/HITS_AND_MISSES.md`, `../ARC_OF_DISCOVERY.md` (diffraction → the simplex),
`../library/KNOW_THE_KNOWABLE.md` (max Q). Peter is the sole gate; nothing posted.*

*Proof & Honesty Standard — the scope is a factorization, not a boast · exact where stated, partial where stated · the home domain folds its own variability · experts decide.*
