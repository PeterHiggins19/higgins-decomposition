# Hˢ data‑prep — any data zip → engine‑ready composition (streaming)

> Turn a zip, a folder of zips, a folder of CSVs, a CSV, or an xlsx into a composition the engine can consume — by **streaming** (never fully extracting big zips). Generalises the Backblaze `huf_preparser.py` trick (stream zipped CSVs, keep only the tiny composition) so it works for any compositional data. Module: `hs_data_prep.py`. Author: Peter Higgins; AI‑assisted per HUF‑STD‑001. Honest‑broker.

---

## Why it exists

The engine wants a clean composition matrix (rows = order, cols = parts). Real data arrives as multi‑GB zips of CSVs (trade, drive health, sensor logs). This tool sits in front of the engine: it **streams the zip row by row, accumulates only the aggregated composition** (kilobytes of memory regardless of file size), and writes an **engine‑ready CSV + a provenance manifest** (source path, output sha256, the exact config). So the limit is wall‑time, not memory — a 4.5 GB zip is processed on a normal machine without ever unzipping it.

## Two shapes

- **WIDE** — each row is one order‑point; the carriers are already columns (EMBER, sector weights).
  ```
  python hs_data_prep.py SOURCE --mode wide --order Year [--exclude World] [--top-k 15] -o out.csv --run
  ```
- **LONG** — rows are records; aggregate a value by `(order, carrier)`, optionally filtered.
  ```
  python hs_data_prep.py SOURCE --mode long --order YEAR --carrier IMPORTER --value VALUE \
                         --filter CODE:^2204 --top-k 20 -o out.csv --run
  ```
  (`--filter col:^prefix` = startswith; `col:value` = exact. Repeat `--filter` to AND them.)

## The headline use — the BACI wine‑trade composition (the new big data)

The CEPII BACI zips are ~4.5 GB each; wine is **HS 2204**. To build *Portugal's wine export‑destination composition over time* — "where is the wine going" in motion — stream the wine slice straight out of the zip and into the engine:

```
python hs_data_prep.py "DATA/Industrial Compositions/CN-TT 15June2026/trade_i_baci_a_22.csv.zip" \
   --mode long --order t --carrier j --value v --filter k:^2204 --filter i:620 \
   --top-k 25 -o pt_wine_destinations.csv --run
```
*(BACI columns: `t` year · `i` exporter · `j` importer · `k` HS6 · `v` value · `q` quantity. `i:620` is Portugal's BACI code; drop it for the whole‑world wine‑trade composition. Run on a machine that can stream the file — the sandbox's 45 s wall‑limit stops only there, not the method.)*

Then `hs_kinematics_engine.run` / `hs_diagnosis.diagnose` read the trade flows in motion: which destinations are gaining vs shedding share, when the trade pattern shifted, how concentrated it is — the wine‑trade study the OIV production run sets up.

## Verified (this session)

- **WIDE** on a real EMBER country CSV → engine‑ready `[26×8]`, correct read ("Nuclear is steering, shedding").
- **LONG + filter + streaming from a `.zip`** on a synthetic trade file → filtered HS `^2204`, aggregated year × importer → `[11×5]` engine‑ready composition + provenance manifest, then diagnosed.

## Output

`out.csv` (order column + carrier columns of summed values — the engine closes to a composition) and `out.csv.manifest.json` (source, config, shape, carriers, output sha256). Drop `out.csv` into `run(M, names)` or pass `--run` to diagnose immediately. *Streaming in, composition out, provenance attached.*
