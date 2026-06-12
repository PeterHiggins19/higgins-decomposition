# Hˢ Gas & Process‑Fluid Compositional Studies — Summary (EN, canonical)

*2026‑06‑11. Engine: CN‑TT v4. Open, reproducible, claim‑tiered. The English text is canonical; the other UN‑6 locales (fr, es, ru, zh, ar) are draft translations pending native‑expert review (per the HUF wrapper convention).*

Hˢ is a deterministic, open instrument that reads the **composition** of a gas or fluid as it changes over time — *which component drives each change, when the pattern shifts, and whether a change is real or a sensor fault* — losslessly and with a reproducible hash. This is the **fourth monitoring category (MC‑4)**: the one that reads ratios, which level/threshold alarms miss.

Four open, reproducible studies (each: a transparent generator, a real engine run, a figure, the science, and a named public‑data target):

1. **Closed‑loop O₂/CO₂/N₂ life support** — across most of the run every single‑channel alarm stayed green while the composition was clearly moving (the cost of "ratio blindness").
2. **Oil & gas produced water** (CoDaWork 2026, Engle et al.; public USGS Produced Waters database) — the formation transition was detected and below‑detection values handled deterministically.
3. **Blood / alveolar gas** (four parts, read **exactly** as a quaternion) — O₂ and CO₂ are named as the drivers of desaturation through a breath‑hold.
4. **Spacecraft cabin atmosphere** (ISS‑style) — the CO₂‑removal duty cycle was tracked and a **trace‑contaminant event was caught** and attributed to the right channel.

**Why public:** so anyone, in any field, can read their own gas or fluid composition with one deterministic instrument and **share the results for all to use**. The instrument reads; the expert decides; the hashes carry the receipts.
