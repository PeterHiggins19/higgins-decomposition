# Data & sources — what a prototype needs, and the precision wall

*Author: Peter Higgins (human authorship for all claims); AI‑assisted per HUF‑STD‑001. Seed/concept —
2026‑06‑20. Public sources only for any prototype; the proprietary/precision boundary is stated honestly
so no one is misled about what public data can and cannot show.*

---

## 1. Public data (sufficient for a first prototype)

| data | source(s) | cadence / form | use |
|---|---|---|---|
| Starlink orbital elements (TLE) | CelesTrak, Space‑Track.org (free account) | per‑object TLEs, updated ~daily | fleet geometry, drag proxy, spectral input |
| Two‑line element history | Space‑Track historical TLE archive | time series per object | kinematics / spectral / wavelet analysis |
| Solar radio flux **F10.7** | NOAA SWPC; NRCan (Penticton) | daily (observed + adjusted) | solar‑cycle/27‑day context, detrending |
| Geomagnetic **Kp** | GFZ Potsdam; NOAA SWPC | 3‑hourly | storm context, adaptive thresholds |
| Geomagnetic indices (Dst, Ap, F10.7 history) | NASA OMNIWeb | various | extended space‑weather context |
| Conjunction / decay context | public SSA notes, CelesTrak SOCRATES‑style products | event‑level | validation context (qualitative) |

All of these are public and free (Space‑Track requires a free account). A Phase‑1 prototype runs entirely
on this set — **no proprietary data, no engagement.**

## 2. The precision wall (be honest about it)

**Public TLEs are low‑precision.** They are mean elements with along‑track position errors typically on
the order of ~1 km (growing with propagation age), and they are smoothed/fitted rather than precise
ephemerides. Consequences:

- **Fleet coherence / anomaly detection [feasible on TLEs, T3].** Relative‑geometry coherence, gross
  drift, storm‑scale density response, and coarse spectral structure are plausibly visible even at TLE
  precision — enough to *test the FCI's behaviour* and the storm‑response hypothesis.
- **Fine science products [NOT feasible on TLEs].** Gravity‑wave detection, thermospheric **wind**
  mapping, and quantitative density retrieval need **high‑precision ephemerides** (operator‑grade GPS‑based
  orbit determination, metre/sub‑metre class) and knowledge of each satellite's **ballistic coefficient**
  (mass, attitude‑dependent cross‑section). These are largely **proprietary**.
- **Ionospheric scintillation [NOT feasible on public orbital data].** Needs high‑rate **radio
  link‑quality metrics** — proprietary.

**Rule for this study:** state which channel each result comes from, and never present a TLE‑precision
result as if it were a high‑precision science product. The precision floor *per product* is itself one of
the open questions the prototype must answer (see CONCEPT §14).

## 3. Derived‑data hygiene (matches repo doctrine)

Any derived compositions / drag proxies / feature tables are kept **off‑repo** (under `DATA/_derived/` in
the workspace), exactly as the GLDS‑1 and other real‑data studies do. The repo carries the method, the
honest notes, and (once a prototype runs) the receipted *output*, not bulk derived data.

## 4. Reproducibility contract (when a prototype exists)

Every prototype run must ship: the public input manifest (with source URLs + retrieval dates + the
exact TLE epochs used), the fixed method parameters (bands, wavelet, cost function, weights), the engine
build, and the **content receipt** over the output. Same inputs ⇒ same numbers ⇒ same receipt — the only
basis on which any result here may leave Tier 3.

## 5. Ethics / scope note

Only public, aggregate orbital and space‑weather data is used. No user‑terminal data, no proprietary
telemetry, no operator‑internal feeds are accessed or implied. Nothing in this study constitutes contact
with, or a request to, SpaceX or any party. Peter Higgins is the sole gate for any external step.
