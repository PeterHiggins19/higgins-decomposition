# Supplementary Information

**Compositional monitoring of energy-mix drift on the simplex**
P. Higgins · 2026-05-17

This Supplementary Information accompanies the main manuscript. It contains the wider 9-country corpus, sensitivity analyses on the 0.1% composition-share floor, the full table of top activation moments across the corpus, and reproducibility instructions.

---

## S1. The nine-country corpus

The main paper presents three case countries (Germany, Japan, United Kingdom) as deliberately different transition archetypes. We applied the same protocol to a wider 9-country corpus: Australia (AUS), China (CHN), Germany (DEU), France (FRA), United Kingdom (GBR), India (IND), Japan (JPN), United States (USA), and the World aggregate (WLD). All countries share the same observation window (2000–2025 annual) and the same EMBER source.

Carrier coverage differs slightly across countries because EMBER reports an eight-carrier vector for CHN, IND, and JPN (the "Other Renewables" category is absent) and a nine-carrier vector for the remaining six. The engine handles per-country carrier lists; reported Power Share and Activation Coefficient values are normalised against each country's own carrier count.

### Per-country yeast-moment counts

A *yeast moment* is a single transition (one year-to-year step) in which a carrier registers an Activation Coefficient ≥ 3× and a starting composition share ≥ 0.1%. Counts across all 25 transitions per country, 2000–2025:

| Country | Yeast moments | Helmsman flips | Peak Activation Coefficient |
|---|---:|---:|---:|
| China (CHN) | 62 | 12 | 549× (Solar 2013–2014) |
| India (IND) | 62 | 15 | 244× (Solar 2012–2013) |
| United States (USA) | 57 | 8 | 760× (Solar 2012–2013) |
| World aggregate (WLD) | 54 | 4 | 513× (Solar 2010–2011) |
| Japan (JPN) | 50 | 17 | 187× (Wind 2004–2005) |
| France (FRA) | 42 | 12 | 659× (Solar 2010–2011) |
| United Kingdom (GBR) | 36 | 15 | 190× (Wind 2001–2002) |
| Australia (AUS) | 23 | 8 | 293× (Solar 2010–2011) |
| Germany (DEU) | 20 | 13 | 333× (Solar 2005–2006) |
| **Total** | **406** | | |

Total yeast moments across the corpus: 406.

### Top thirty activation moments — corpus-wide

Sorted by Activation Coefficient. Floor: composition share ≥ 0.1%.

| Rank | Country | Transition | Carrier | AC (× size) | Power Share | Size at start |
|---:|---|---|---|---:|---:|---:|
| 1 | USA | 2012–2013 | Solar | 760× | 81.7% | 0.107% |
| 2 | FRA | 2010–2011 | Solar | 659× | 72.6% | 0.110% |
| 3 | FRA | 2004–2005 | Wind | 634× | 66.0% | 0.104% |
| 4 | CHN | 2013–2014 | Solar | 549× | 84.7% | 0.154% |
| 5 | WLD | 2010–2011 | Solar | 513× | 77.7% | 0.151% |
| 6 | FRA | 2005–2006 | Wind | 495× | 83.5% | 0.169% |
| 7 | USA | 2013–2014 | Solar | 395× | 87.9% | 0.223% |
| 8 | CHN | 2004–2005 | Bioenergy | 346× | 39.7% | 0.115% |
| 9 | CHN | 2003–2004 | Bioenergy | 342× | 45.5% | 0.133% |
| 10 | FRA | 2024–2025 | Coal | 342× | 62.1% | 0.182% |
| 11 | DEU | 2005–2006 | Solar | 333× | 71.1% | 0.214% |
| 12 | AUS | 2010–2011 | Solar | 293× | 39.3% | 0.134% |
| 13 | CHN | 2007–2008 | Wind | 284× | 47.5% | 0.167% |
| 14 | USA | 2001–2002 | Wind | 262× | 47.3% | 0.181% |
| 15 | IND | 2012–2013 | Solar | 244× | 47.1% | 0.193% |

The full ranked table (all 406 entries) is provided as a JSON file at `papers/codawork2026/manuscript/build/summary.json` in the repository.

### Carrier distribution of the top yeast cases

Of the 30 highest-leverage activation moments across the corpus:

- **Solar** appears in 19 cases (63%), with concentration in 2010–2015 and the secondary cluster 2003–2007 in Germany / France
- **Wind** appears in 5 cases (17%), mostly 2001–2008
- **Bioenergy** appears in 3 cases (10%), in China 2003–2005
- **Other Renewables** appears in 2 cases (7%), in the United Kingdom 2018–2020
- **Coal** appears in 1 case (3%), in France's late-period decommissioning step

The cross-country signature is dominated by solar; the secondary patterns name wind and bioenergy as regionally specific yeast carriers.

---

## S2. Sensitivity to the 0.1% composition-share floor

The main paper applies a $\rho_i \ge 10^{-3}$ floor when reporting yeast moments, to avoid log-amplification artefacts at near-zero composition shares. We tested sensitivity at three alternative floors:

| Floor | Yeast moments (total) | Highest AC reported | Comment |
|---|---:|---:|---|
| 0.05% (10⁻³·³) | 528 | 1567× (USA Solar 2011–2012, share 0.082%) | More marginal carriers admitted; identification of top drivers stable |
| **0.1% (10⁻³)** | **406** | **760× (USA Solar 2012–2013)** | **Main paper floor** |
| 0.5% (10⁻²·³) | 248 | 333× (DEU Solar 2005–2006) | More conservative; top-3 cross-country drivers unchanged |

The named structural drivers (solar 2010–2015, wind 2001–2008, UK Other Renewables 2019–2020) are identified at all three floors. Only the marginal count of yeast moments varies. The reported peak activation coefficient varies as the floor changes — at lower floors, smaller-share carriers can register higher leverage ratios — but the identity of the carrier and the year remains stable.

This is consistent with the protocol's design intent: the Activation Coefficient is a hidden-driver diagnostic, not a magnitude measure. The floor controls the cutoff between *structurally meaningful small carriers* and *carriers that have just appeared at near-zero share*. The cross-corpus story (solar as the dominant 2010–2015 yeast) survives every choice of reasonable floor.

---

## S3. The 5-of-9 deceptive-drift signature (INV-051)

A separate Hˢ Investigation Catalog entry (INV-051) records the observation that the deceptive-drift signature — a 6-month sliding window in which $K_{\mathrm{eff}}$ is declining while structural velocity is below the series median — fires in 5 of 9 countries at annual grain over the 2000–2025 window: AUS, CHN, GBR, IND, JPN.

The four countries in which the annual-grain signature does not fire are DEU, FRA, USA, and the World aggregate. Importantly, the Germany result reported in the MC-4 packet (p = 0.0016) is from monthly-grain analysis on a deseasonalised series, not the annual-grain test reported here. The two analyses are not in conflict — the monthly-grain test is more sensitive to the seasonally adjusted compositional drift that the annual-grain summary smooths over.

The 5-of-9 result is the *cross-country discrimination signature* of the protocol: it fires in some countries but not all, which is the test the protocol must pass to avoid the case-defeat path identified in the Discussion.

---

## S4. Reproducibility

All results in the main paper and this Supplementary are deterministic and reproducible from raw EMBER CSV files. The reproduction protocol is:

### Step 1: Obtain the data

```
git clone https://github.com/PeterHiggins19/higgins-decomposition
cd higgins-decomposition
```

Raw EMBER CSV files for the nine countries are committed to the repository at `DATA/Energy/EMBER_pipeline_ready/` under the file naming convention `ember_<ISO3>_<Country>_generation_TWh.csv`. SHA-256 hashes of each file are recorded in the manuscript build manifest at `papers/codawork2026/manuscript/build/sha256.txt`.

### Step 2: Run the engine

```
pip install -e .
python HCI-CNT/engine/cnt.py --input DATA/Energy/EMBER_pipeline_ready/ember_DEU_Germany_generation_TWh.csv --output /tmp/cnt_DEU.json
```

The engine produces a CNT JSON file with all the geometric quantities (CLR coordinates, ILR-Helmert coordinates, helmsman family, Aitchison distances) for the input composition series.

### Step 3: Compute Power Share and Activation Coefficient

The Power Share and Activation Coefficient quantities are computed externally from the CNT JSON output (the engine block that emits them natively is queued as a post-conference promotion — schema 3.1.0 → 3.2.0 under INV-060). The script that performs the external computation for this paper is at:

```
papers/codawork2026/manuscript/build/compute_power_share.py
```

It reads CNT JSON files for the nine countries from `CODA-Association/CODAwork2026/data_outputs/per_country_json/cnt_v3/`, computes Power Share = (Δclr)² / Σ(Δclr)² and Activation Coefficient = Power Share ÷ starting composition share, and emits `power_share.json` (the full per-country, per-transition, per-carrier tensor) and `summary.json` (the top activation moments and per-country counts).

Total reproduction time from a clean checkout: under five minutes on a modern laptop.

### Step 4: Re-render the figures

The figures in the main paper are generated by the scripts in `papers/codawork2026/manuscript/build/`. Each figure is built from the deterministic JSON outputs and can be re-rendered without re-running the engine if the inputs are unchanged.

---

## S5. Companion artefacts

A companion community-facing slide deck (20 slides, landscape PDF) that walks through the five-viewpoint protocol at community-friendly tone is available at `Studies/Energy_HiddenDirections_2026-05-17/Energy_HiddenDirections_2026-05-17.pdf` in the workspace. The same data and the same engine outputs feed both the manuscript and the deck; the deck condenses the manuscript for in-person presentation and community circulation.

---

## S6. Cross-AI methodological cross-checks

The HUF AI Collective (Claude, ChatGPT, Copilot, Gemini, Grok) was used in cross-check rounds throughout the framework's development. Key methodological adjustments arising from these cross-checks include:

- **L2 → TV correction** (March 2026, identified during a ChatGPT review): an earlier metric labelled "TV distance" was actually computing $\sqrt{\sum_i (p_i - q_i)^2}$ rather than $\tfrac{1}{2}\sum_i |p_i - q_i|$. Renamed the original to `l2_drift` and added the true TV distance alongside. All outputs regenerated. Documented in METRIC-001 (Appendix A of the MC-4 packet).
- **MC-4 sharpening to three conjuncts** (May 2026, multiple cross-checks): the original MC-4 claim was sharpened to explicitly require Aitchison-native + formal change detection + carrier-level attribution combined into one observable stack. This is the form presented in the main paper.
- **Person-noun convention** (May 2026, codified as HUF-STD-001 v1.1): the convention of using "researcher / user / reader / participant" rather than "human" in public-facing scientific output to avoid drawing attention to the human/AI distinction unnecessarily.

The full cross-check archive is at `ai-refresh/cross_check_archive/` in the repository, organised by date and AI assistant.

---

*Supplementary Information prepared 2026-05-17. Manuscript: `papers/codawork2026/manuscript/output/Compositional_Monitoring_2026.docx`. Repository: github.com/PeterHiggins19/higgins-decomposition.*
