# Hˢ — Public Data Sources for Real‑Data Studies

> **Headline:** the public websites where the real data lives for every Hˢ study — so anyone can take a demonstration to real data with one deterministic instrument and **share the results for all to use**. · **Engine:** CN‑TT v4 (`HCI-CNTT/`; run `python HCI-CNTT/run_cntt.py <composition.csv> -o out.json`). · **Goal:** lower the barrier — bring your own data, read your own composition.
>
> *2026‑06‑11. Author: Peter Higgins (human authorship for claims); AI‑assisted per HUF‑STD‑001. Experiments + science only. We are the **instrument, not the data**: we read data where it lives and do not redistribute it. URLs verified 2026‑06‑11; confirm before bulk download — links and dataset versions change. Downloading any dataset is a deliberate, user‑authorised step. No rush — all adjustable, nothing pushed.*

---

## Gas & fluid composition studies (`industrial-instruments/gas-composition-study/`)

**Study 1 — closed‑loop O₂/CO₂/N₂ life‑support gas**
- **VitalDB** (open surgical/ICU vital‑signs DB; gas‑analyzer tracks FiO₂, etO₂, inspired/end‑tidal CO₂, agents; API + Python lib): https://vitaldb.net · mirror on PhysioNet: https://physionet.org/content/vitaldb/1.0.0/ · paper: https://www.nature.com/articles/s41597-022-01411-5
- **CapnoBase** (annotated capnograms — inhaled/exhaled CO₂ from anaesthesia monitors): https://capnobase.org · open files: https://open.library.ubc.ca/collections/researchdata/items/1.0395424
- *Compose:* per case form {O₂, CO₂, N₂(balance)} over time → run the engine → read helmsman / regime / lossless / hash.

**Study 2 — oil & gas produced water (CoDaWork 2026 / Engle et al.)**
- **USGS National Produced Waters Geochemical Database v3.0** (Dec 2023): DOI https://doi.org/10.5066/P9DSRCZJ · USGS data page: https://www.usgs.gov/data/us-geological-survey-national-produced-waters-geochemical-database-ver-30-december-2023 · ScienceBase: https://www.sciencebase.gov/catalog/item/64fa1e71d34ed30c2054ea11 · interactive viewer: https://www.usgs.gov/tools/us-geological-survey-national-produced-waters-geochemical-database-viewer
- *Compose:* subset Appalachian Basin (as in the talk); major‑ion composition {Na, Cl, Ca, Mg, SO₄, HCO₃, K, …} per sample, order by depth/formation → engine reads the down‑depth helmsman + transitions; the engine's zero‑treatment handles below‑detection values.

**Study 3 — blood / alveolar gas (dissolved O₂, D=4 CNQ‑native)**
- **VitalDB** (arterial blood‑gas lab tracks + gas analyzer): https://vitaldb.net
- **CapnoBase** (capnograms): https://capnobase.org · **PhysioNet** databases (capnography/respiratory): https://physionet.org/about/database/
- *Compose:* {O₂, CO₂, N₂, H₂O} partial pressures over time (D=4 → exact quaternion read).

**Study 4 — spacecraft cabin atmosphere**
- **NASA ISS Major Constituent Analyzer (MCA) on‑orbit performance** reports (N₂, O₂, H₂, CO₂, CH₄, H₂O time series in figures/tables): https://ntrs.nasa.gov/api/citations/20150013812/downloads/20150013812.pdf · https://ntrs.nasa.gov/api/citations/20120000038/downloads/20120000038.pdf
- **NASA Open Data Portal** (atmospheric CO₂, ISLSCP/Globalview): https://data.nasa.gov · ECLSS overview: https://en.wikipedia.org/wiki/ISS_ECLSS
- **Honest note:** there is **no single clean public download portal for live ISS cabin‑atmosphere time series** (MCA data is telemetered to Mission Control). The realistic public routes are the NTRS MCA performance papers (digitise their published series), NASA Open Data, and **ground analog habitats** (e.g. HI‑SEAS / closed‑habitat studies — search for the specific dataset). For a clean closed‑loop gas analog, VitalDB/CapnoBase (Study 1) are the most directly downloadable.

**General‑gas baseline (null/stability control)**
- **NOAA Global Monitoring Laboratory** (atmospheric CO₂/CH₄/N₂O; data finder + ObsPack): https://gml.noaa.gov/data/data.php · https://gml.noaa.gov/ccgg/data/
- Atmospheric **O₂/N₂ ratio**: the **Scripps O₂ Program** (named source — verify the current URL before download).

---

## Other Hˢ study families (real‑data sources)

**Microbiome (`collaborations/microbiome/`)** — **coda4microbiome** (Calle, Pujolassos & Susin): project + datasets https://malucalle.github.io/coda4microbiome/ · CRAN https://cran.r-project.org/web/packages/coda4microbiome/ · GitHub https://github.com/malucalle/coda4microbiome (the Crohn / HIV / ECAM `.rda` data ship with the package).

**Space biology / the Earth‑space twin study (`SPACE_READINESS_AND_CHALLENGE.md`)** — **NASA Open Science Data Repository (OSDR) / GeneLab** (spaceflight gut‑microbiome + multi‑omics; documents elevated diversity + altered community structure in flight): https://science.nasa.gov/biological-physical/data/osdr/ · overview paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11701653/ — *this is the real data for the deterministic Earth/space twin study.*
  - **Public AWS S3 bucket (clean programmatic route):** `s3://nasa-osdr/` (`arn:aws:s3:::nasa-osdr`) — **anonymous, no credentials**: `aws s3 ls --no-sign-request s3://nasa-osdr/`. On the AWS Registry of Open Data: https://registry.opendata.aws/nasa-osdr/ · getting‑started guide: https://www.nasa.gov/reference/osdr-help-getting-started-with-aws-and-osdr-data/
  - **OSDR Public API** (programmatic metadata/files): https://genelab.nasa.gov/ · search the web GUI at https://osdr.nasa.gov for a study (e.g. a rodent/astronaut gut‑microbiome OSD‑### accession), then pull its files from the S3 path. *(NASA data is spread across systems — OSDR = biology/omics; NTRS = reports; data.nasa.gov = open‑data portal; Earthdata = Earth science; PDS = planetary. For the microbiome/twin‑study, OSDR's S3 + API is the clean route.)*

**Sand‑grain succession (the CoDaWork inspiration)** — Silva‑Solar, Amann & Knittel (MPI Marine Microbiology) 16S amplicon data: search **NCBI SRA** (https://www.ncbi.nlm.nih.gov/sra) / **ENA** (https://www.ebi.ac.uk/ena) for the study's accession (to confirm with the authors).

**Geosensing / mudstone (`collaborations/geology-wehner/`)** — the Frielingen‑9 chemostratigraphy demo: **PANGAEA** dataset 897615 (https://doi.org/10.1594/PANGAEA.897615). Orbital mineral remote sensing: **USGS EarthExplorer** (https://earthexplorer.usgs.gov) / NASA EMIT.

**Drive‑health / engine parity (`experiments/backblaze_v4_parity_2026-06/`)** — **Backblaze Hard Drive Data** (quarterly, public): https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data

---

## Per‑case link directory (many links each)

*Verified 2026‑06‑11 via web search. Multiple links per case — official portal, mirrors, DOIs, APIs, and related public datasets. Confirm before bulk download; instrument‑not‑data (we read where it lives).*

### Gas — closed‑loop O₂/CO₂/N₂ **and** blood/alveolar gas (Studies 1 & 3)
- **VitalDB** — official: https://vitaldb.net · API/docs: https://vitaldb.net/docs · Python lib: https://github.com/vitaldb/vitaldb-python · paper: https://www.nature.com/articles/s41597-022-01411-5 · PhysioNet mirror: https://physionet.org/content/vitaldb/1.0.0/
- **University of Queensland Vital Signs Dataset** (anaesthesia: capnograph + end‑tidal O₂/CO₂/N₂O/agents, SpO₂, ABP, ventilator): https://outbox.eait.uq.edu.au/uqdliu3/uqvitalsignsdataset/index.html · **per‑case download (recommended — the all‑cases ZIP is ~1.1 GB and flaky):** https://outbox.eait.uq.edu.au/uqdliu3/uqvitalsignsdataset/browse.html · record: https://researchdata.edu.au/university-queensland-vital-signs-dataset/14011 · paper: https://pubmed.ncbi.nlm.nih.gov/22190558/ · *(per‑case trenddata.csv holds the 1‑s gas‑analyzer numerics; ✅ ran in `industrial-instruments/gas-composition-study/blood-gas/results_real_uq/`)*
- **CapnoBase** (annotated capnograms): https://capnobase.org · open files: https://open.library.ubc.ca/collections/researchdata/items/1.0395424 · (event benchmark) https://open.library.ubc.ca/collections/researchdata/items/1.0395422
- **PhysioNet** index of databases: https://physionet.org/about/database/ · **MIMIC‑IV Waveform**: https://physionet.org/content/mimic4wdb/ · **MIMIC‑III Waveform**: https://archive.physionet.org/physiobank/database/mimic3wdb/ · **eICU‑CRD**: https://physionet.org/content/eicu-crd/

### Oil & gas produced water (Study 2)
- **USGS NPWGD v3.0** (Dec 2023): DOI https://doi.org/10.5066/P9DSRCZJ · USGS data page: https://www.usgs.gov/data/us-geological-survey-national-produced-waters-geochemical-database-ver-30-december-2023 · USGS Science Data Catalog: https://data.usgs.gov/datacatalog/data/USGS:64fa1e71d34ed30c2054ea11 · viewer: https://www.usgs.gov/tools/us-geological-survey-national-produced-waters-geochemical-database-viewer
- **USGS NPWGD v2.3** (the file you have): ScienceBase https://www.sciencebase.gov/catalog/item/59d25d63e4b05fe04cc235f9 · data.gov https://catalog.data.gov/dataset/u-s-geological-survey-national-produced-waters-geochemical-database-v2-3 · data.doi.gov https://data.doi.gov/dataset/u-s-geological-survey-national-produced-waters-geochemical-database-v2-3 · USGS SDC https://data.usgs.gov/datacatalog/data/USGS:59d25d63e4b05fe04cc235f9
- USGS update note (23 new datasets — Marcellus/Permian/Bakken/Williston): https://www.usgs.gov/news/technical-announcement/usgs-updates-database-oil-and-gas-and-other-energy-wastewaters-23-new · basin source study (Marcellus Li): https://doi.org/10.1016/j.chemgeo.2016.01.009

### Spacecraft cabin atmosphere (Study 4)
- NASA NTRS — ISS **Major Constituent Analyzer** on‑orbit performance: https://ntrs.nasa.gov/api/citations/20150013812/downloads/20150013812.pdf · https://ntrs.nasa.gov/api/citations/20120000038/downloads/20120000038.pdf · CO₂ control issues: https://ntrs.nasa.gov/api/citations/20100021976/downloads/20100021976.pdf
- **NASA Open Data Portal**: https://data.nasa.gov · ISS ECLSS overview: https://en.wikipedia.org/wiki/ISS_ECLSS
- **HI‑SEAS** Mars analog (FTIR/CO₂ habitat air): https://www.hi-seas.org · https://en.wikipedia.org/wiki/HI-SEAS · Mars analogs list: https://en.wikipedia.org/wiki/List_of_Mars_analogs
- *(Honest: no single clean public download portal for live ISS cabin time series — MCA data is telemetered to Mission Control. Use the NTRS series, NASA Open Data, or analog habitats.)*

### Microbiome (coda4microbiome + public accessions)
- **coda4microbiome**: https://malucalle.github.io/coda4microbiome/ · CRAN https://cran.r-project.org/web/packages/coda4microbiome/ · GitHub https://github.com/malucalle/coda4microbiome
- **curatedMetagenomicData** (25 studies / 5,716 samples incl. IBD/Crohn, HIV): Bioconductor https://bioconductor.org/packages/release/data/experiment/html/curatedMetagenomicData.html · site https://waldronlab.io/curatedMetagenomicData/ · GitHub https://github.com/waldronlab/curatedMetagenomicData
- **ECAM** infant gut: bile‑acids paper https://www.nature.com/articles/s41467-020-17183-8 · raw via **Qiita** https://qiita.ucsd.edu and **ENA** https://www.ebi.ac.uk/ena (search the study accession)
- General microbiome repositories: **NCBI SRA** https://www.ncbi.nlm.nih.gov/sra · **EBI MGnify** https://www.ebi.ac.uk/metagenomics · **Earth Microbiome Project** https://earthmicrobiome.org

### Space gut‑microbiome twin study (OSDR / GeneLab)
- **OSDR portal**: https://osdr.nasa.gov · https://science.nasa.gov/biological-physical/data/osdr/ · **GeneLab**: https://genelab.nasa.gov
- **Public AWS S3**: `s3://nasa-osdr/` (`arn:aws:s3:::nasa-osdr`) — `aws s3 ls --no-sign-request s3://nasa-osdr/` · registry: https://registry.opendata.aws/nasa-osdr/ · guide: https://www.nasa.gov/reference/osdr-help-getting-started-with-aws-and-osdr-data/
- Specific studies: **OSD‑745** (the one you have) · **OSD‑249** (murine gut multiomics, 29/56‑day spaceflight) · **Rodent Research‑6** microbiome benchmark (6 datasets) · spaceflight gut paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11362537/

### Sand‑grain succession (the CoDaWork inspiration, MPI Bremen)
- CoDaWork 2026 talk: Silva‑Solar, Amann & Knittel — Book of Abstracts p.48.
- Foundational paper, same lab: **Probandt, Eickhorst, Ellrott, Amann & Knittel (2018), "Microbial life on a sand grain: from bulk sediment to single grains," ISME J** — https://www.nature.com/articles/ismej2017197 · open: https://pmc.ncbi.nlm.nih.gov/articles/PMC5776476/ (16S of 17 single grains; SRA accession in the paper's data‑availability).
- Sequence repositories: **NCBI SRA** https://www.ncbi.nlm.nih.gov/sra · **ENA** https://www.ebi.ac.uk/ena · MPI Marine Microbiology: https://www.mpi-bremen.de/en/Home.html

### Geology mudstone (Frielingen‑9)
- **PANGAEA**: https://doi.org/10.1594/PANGAEA.897615 (the `.tab` you supplied). Orbital mineral remote sensing follow‑ons: **USGS EarthExplorer** https://earthexplorer.usgs.gov · **NASA EMIT** https://earth.jpl.nasa.gov/emit/

### Drive‑health / engine parity
- **Backblaze Hard Drive Data** (quarterly): https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data

### General‑gas atmospheric baseline
- **NOAA GML** data finder: https://gml.noaa.gov/data/data.php · CCGG: https://gml.noaa.gov/ccgg/data/ · CO₂ trends: https://gml.noaa.gov/ccgg/trends/data.html
- **Scripps O₂ Program** (atmospheric O₂/N₂ + CO₂): https://scrippso2.ucsd.edu/ · plots https://scrippso2.ucsd.edu/plots · data https://scrippso2.ucsd.edu/osub2sub-data · CDIAC modern records https://cdiac.ess-dive.lbl.gov/trends/oxygen/modern_records.html · **Scripps CO₂**: https://scrippsco2.ucsd.edu/

## How to run any of these
1. Download the public data (authorised, per dataset terms).
2. Form a composition CSV: **first column = an ordering label** (time, depth, sample id), **remaining columns = the parts**.
3. `python HCI-CNTT/run_cntt.py your_composition.csv -o out.json`
4. Read `atlas.lossless`, `navigation.helmsman` / `regime_boundaries`, `K_eff`, and the `cntt_content_sha256` receipt.

*The instrument reads. The expert decides. The data belongs to the domain. Bring your own data — and share what you find.*
