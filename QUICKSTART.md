# Hs — Quickstart

You cloned the repo. Now what.

This is the absolute shortest path to a working result, in any language.

---

## 🛡️ Verify before you trust (skeptical-user path)

**You don't have to run the published code to verify it.** The Hˢ framework publishes every algorithm in **four forms** — Python reference, R reference, language-agnostic pseudocode, and formal HUF-STD-002 specification — so that a skeptical user can re-implement from the pseudocode in any language and verify byte-identically against the published code via `content_sha256` on the three canonical reference inputs.

| If you want to | Read |
|---|---|
| Verify *the math* before trusting anything | [`papers/flagship/GROUND_STATE_AND_TRACTION.md`](papers/flagship/GROUND_STATE_AND_TRACTION.md) v2.2 §7 — 8 lemmas + 2 theorems, each resting on standard published results (Banach 1922, Helmholtz 1860, Hamilton 1843, Aitchison 1986, …) |
| Verify *the algorithm* before trusting the code | [`HCI-CNT/engine/CNT_PSEUDOCODE.md`](HCI-CNT/engine/CNT_PSEUDOCODE.md) v3.1.0 and [`HCI-CNQ/engine/CNQ_PSEUDOCODE.md`](HCI-CNQ/engine/CNQ_PSEUDOCODE.md) — language-neutral algorithm references |
| Verify *the implementation* by independent re-implementation | [`TRUST_AND_VERIFICATION.md`](TRUST_AND_VERIFICATION.md) — the 7-step verification protocol with three canonical reference inputs and published hashes |
| Verify *the empirical claims* | Run the three pinned reference datasets (Backblaze, Planck CMB, SM neutrino) and check IEEE-floor convergence (`max_residual = 4.44 × 10⁻¹⁶`) |

The framework's discipline is **trust by independent reproduction.** *We need to prove to be trustworthy, not expect it.*

---

## 30 seconds — reproduce the three IEEE-floor confirmations

```bash
git clone https://github.com/PeterHiggins19/higgins-decomposition
cd higgins-decomposition
python HCI-CNQ/scripts/run_all_confirmations.py --repo-root .
python HCI-CNQ/scripts/verify_publication_results.py --repo-root .
```

Expected: three datasets pass at IEEE float64 floor; verifier exits 0; the published `max_residual = 4.440892098500626e-16` matches to the last digit on Backblaze and Planck.

---

## 2 minutes — install as a package, run on your own data

```bash
pip install -e .
```

Then in Python:

```python
# CNT — measure structural invariances on a compositional time-series
import numpy as np
import sys; sys.path.insert(0, "HCI-CNT/engine")
import cnt as CNT  # if you prefer src-layout: from HCI_CNT.engine import cnt as CNT

# Or just call the script:
#   python HCI-CNT/engine/cnt.py your_data.csv -o your_output.json

# CNQ — quaternion-native view of the same trajectory
import sys; sys.path.insert(0, "HCI-CNQ/engine")
import cnq as CNQ

payload = CNQ.run_cnq(
    cnt_json_path="your_output.json",
    input_csv_path="your_data.csv",
    out_path="cnq_view.json",
)
print(payload["cnq_view"]["quaternion_path"]["max_residual"])
print(payload["cnq_content_sha256"])
```

---

## 2 minutes — same, in R

```r
# install once
install.packages(c("jsonlite", "digest"))

# run
source("HCI-CNQ/engine/cnq.R")
payload <- cnq_run(
  cnt_json_path = "your_output.json",
  input_csv_path = "your_data.csv",
  out_path = "cnq_view.json"
)
cat(payload$cnq_view$quaternion_path$max_residual, "\n")
cat(payload$cnq_content_sha256, "\n")
```

For CNT in R: `Rscript HCI-CNT/engine/cnt.R input.csv output.json`.

---

## 5 minutes — let an AI assistant do it for you

Paste this prompt into Claude, ChatGPT, Grok, or any AI assistant with web access:

```
Read https://raw.githubusercontent.com/PeterHiggins19/higgins-decomposition/main/HS_FAST_REFRESH.json
Then read https://raw.githubusercontent.com/PeterHiggins19/higgins-decomposition/main/ai-refresh/CCTT_RUNBOOK.md
Then walk the 7 phases of CCTT v1.0 against my dataset: <paste CSV path or content>
Confirm at each gate. Produce the canonical CNT JSON and the CNQ JSON.
```

The CCTT runbook is designed for AI assistants to execute. The user just confirms gates.

---

## What the three confirmations look like

| Dataset | D | T | max residual | Termination | Role |
|---|---|---|---|---|---|
| Backblaze fleet (drive failures) | 4 | 731 | **4.441 × 10⁻¹⁶** | LIMIT_CYCLE_P2 | confirmed (load-bearing) |
| Planck CMB photon power | 4 | 2499 | **4.441 × 10⁻¹⁶** | LIMIT_CYCLE_P2 / OVERDAMPED_EXTREME | confirmed (load-bearing) |
| SM neutrino oscillation | 3 | 1000 | 3.331 × 10⁻¹⁶ | LIMIT_CYCLE_P2 / LIGHTLY_DAMPED | consistency support |

Bit-identical residual on Backblaze and Planck (two physically unrelated D=4 datasets) → the residual is hardware float64 representation, not algorithmic noise. The math is exact on the simplex.

---

## Where to go from here

| Goal | Read |
|---|---|
| 🛡️ **Trust path — independently verify the code without running it** | [`TRUST_AND_VERIFICATION.md`](TRUST_AND_VERIFICATION.md) |
| **Flagship paper (master standard — why the framework works)** | [`papers/flagship/GROUND_STATE_AND_TRACTION.md`](papers/flagship/GROUND_STATE_AND_TRACTION.md) v2.2 |
| Full publication-grade overview | [`PUBLICATION_READY.md`](PUBLICATION_READY.md) |
| Single-file AI loader (one fetch = full system context) | [`HS_FAST_REFRESH.json`](HS_FAST_REFRESH.json) |
| Operations protocol (12-transition Gawande checklist) | [`OPERATIONS_PROTOCOL.md`](OPERATIONS_PROTOCOL.md) |
| 7-phase reproduction runbook | [`ai-refresh/CCTT_RUNBOOK.md`](ai-refresh/CCTT_RUNBOOK.md) |
| CNT engine docs + handbook | [`HCI-CNT/`](HCI-CNT/) |
| CNQ engine docs + claim-strength + scope | [`HCI-CNQ/`](HCI-CNQ/) |
| Investigation Catalog (63 entries, 6 dispositions) | [`ai-refresh/INVESTIGATION_CATALOG.md`](ai-refresh/INVESTIGATION_CATALOG.md) |
| Locked vocabulary (~220-entry glossary v3.0) | [`HCI-CNT/handbook/GLOSSARY.md`](HCI-CNT/handbook/GLOSSARY.md) |
| Origin lineage (DADC → H₁ → HUF → Hs → CNT → CNQ) | [`HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md`](HCI-CNT/handbook/ORIGIN_DADC_LINEAGE.md) |
| **CoDaWork 2026 — attendee follow-along** | [`CODA-Association/CONFERENCE_ATTENDEES.md`](CODA-Association/CONFERENCE_ATTENDEES.md) |

---

## Licence

Code: [Apache-2.0](LICENSE). Documentation, slides, papers: [CC BY 4.0](LICENSE-DOCS). See [`NOTICE`](NOTICE) for the rationale.

---

## Help

Free to use. Help available — open a GitHub issue, find Peter at a conference, or email `peterhiggins2016@gmail.com`.

The instrument reads. The expert decides. The hashes carry the receipts.
