# Field directional compositional sniffer — Hs on a cell-phone micro-lab (public)

**Concept (raised by a field geologist in discussion).** Pair an onsite composition sensor — e.g. a **cell-phone-camera Raman spectrometer** (Dhankhar & Wehner 2023) — with the Hs / CNT engine to turn a phone into a field **micro-laboratory + directional compositional "sniffer."** The geologist is the rover; the phone is the instrument and the map.

## The idea
- **Onsite & deterministic.** Measure a sample's composition in the field; CNT reduces it to its lossless compositional record. *Sample-and-toss:* keep the deterministic Hs record, not bulky raw storage.
- **Directional analysis (the bloodhound).** As the geologist moves and samples, CNT reads the compositional trajectory **across space** — here the ordering axis is position, not depth or time. The **bearing** and **helmsman** point toward the direction and driver of compositional change, so one can **follow a vein / gradient of any target composition.** The system can suggest **left / right / forward / back / up / down** to chase a target, or simply **geo-map** samples with directional pattern/composition analysis.
- **Rover analog.** A cheap, human-in-the-loop version of a Mars-rover's onboard compositional targeting: the phone carries the micro-lab + a Google-Maps overlay; Hs carries the analysis and the "which way" reading.

## Why Hs fits
- Composition is CNT's **native object**; the tensor train gives lossless compositional storage **and** directional (bearing/helmsman) readings in one pass.
- **Deterministic + hash-chained** → reproducible field provenance per sample and location.
- It is an **analysis/navigation layer over existing field hardware** (cell-phone Raman / portable XRF) — Hs is not the sensor.

## Roles, easiest first
1. **Geo-mapping with directional pattern/composition analysis** — map what's present and how it changes across space (the strong, low-risk first role).
2. **Directional sampling guidance** — follow-the-vein toward a target composition.
3. **Onboard sample-and-toss** — store the Hs record, discard bulk raw data.

## Audiences
USGS; NASA / planetary science (the rover analog); mineral exploration; environmental / contamination mapping.

## Honest framing
Concept / feasibility, research-grade — not a deployed device. It needs: a real onsite composition feed (Raman / XRF), positioning, **field calibration**, proper **zero-treatment** for trace / below-detection values, and validation against known ground. Hs assists targeting; **the geologist decides** where to dig. Claim tier: candidate application of CNT to field remote-sensing.

## References
- Dhankhar, D. & Wehner, M. (2023). *Feasibility of cell-phone camera Raman spectrometer for geological samples identification in field or mobile situations.* EGUsphere (preprint). https://egusphere.copernicus.org/preprints/2023/egusphere-2023-2146/
- The Hs geochemistry corpus — see `REPO_MAP.md`.
