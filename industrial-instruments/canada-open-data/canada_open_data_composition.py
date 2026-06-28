#!/usr/bin/env python3
"""
Hs reads the COMPOSITION of Canada's entire open-data estate (deterministic; hash-receipted).

Real catalogue metadata from the open.canada.ca CKAN API (package_search facets), fetched 2026-06-24.
Total catalogue = 47,462 datasets. Each facet (department, format, jurisdiction, collection) is read as a
composition: shares, the arrow (dominant part), the effective dimension (perplexity = equivalent # of equal
parts), and concentration (HHI). Descriptive -- what the data structure IS -- not a political judgment.

Provenance: counts are copied verbatim from the API response (see SOURCE). Re-fetch to refresh.
Author: Peter Higgins; AI-assisted per HUF-STD-001. Internal / planning. No endorsement implied.
"""
import hashlib, json, math
import numpy as np

SOURCE = "open.canada.ca CKAN package_search facets, fetched 2026-06-24; total datasets = 47462"
TOTAL = 47462

ORG = {
 "Natural Resources (NRCan)":10247,"Statistics Canada":10203,"Health Canada":2971,"Yukon":2901,"Alberta":2897,
 "Global Affairs":2036,"British Columbia":1681,"Quebec":1531,"Environment & Climate Change":1173,"Ontario":988,
 "Fisheries & Oceans":905,"Public Health Agency":761,"Nova Scotia":748,"Parks Canada":593,"Justice":523,
 "Transportation Safety Board":429,"Saskatchewan":413,"Agriculture & Agri-Food":396,"Auditor General":361,
 "Canada Revenue Agency":353,"Comm. Security Estab.":311,"Treasury Board Sec.":303,"Correctional Service":266,
 "Employment & Social Dev.":262,"Manitoba":261,"Food Inspection Agency":259,"Public Services & Proc.":231,
 "New Brunswick":221,"Nuclear Safety Comm.":187,"National Defence":169,"Public Service Comm.":134,
 "Canadian Space Agency":133,"Canadian Heritage":132,"NW Territories":126,"Veterans Affairs":126,
 "Impact Assessment Agency":121,"Shared Services":116,"Finance":109,"Innovation/Science/Econ Dev (ISED)":98,
 "RCMP":94}
FMT = {"HTML":31954,"CSV":15724,"XML":12866,"other":10118,"PDF":8201,"ZIP":5970,"SHP":4947,"ESRI REST":2625,
 "XLSX":2203,"EDI":1881,"GEOJSON":1559,"KML":1501,"WMS":1243,"JP2":1228,"XLS":1022,"FGDB/GDB":924,"RSS":877,
 "JPG":713,"RDF":597,"TXT":573,"DOCX":477,"JSON":398,"KMZ":395,"GPKG":368,"GeoTIF":362,"SEGY":253}
JUR = {"federal":35548,"provincial":11628,"municipal":285,"user":1}
COLL = {"primary":13754,"geogratis":9799,"publication":7840,"fgp":7519,"federated":6584,"parliament_report":646,
 "parliament_committee_deputy":502,"parliament_committee":484,"transition":141,"transition_deputy":81,
 "aia":39,"code":35,"accessibility_plans":30,"api":6,"app":2}

def read_composition(name, counts):
    items = list(counts.items()); n = np.array([c for _,c in items], float)
    p = n / n.sum()
    H = -(p*np.log(p)).sum()
    eff_dim = math.exp(H)
    hhi = float((p**2).sum())
    order = np.argsort(-p)
    top = [(items[i][0], round(float(p[i])*100,1)) for i in order[:3]]
    top2 = round(float(p[order[0]]+p[order[1]])*100,1)
    clr = np.log(p) - np.log(p).mean()
    arrow = items[int(np.argmax(clr))][0]
    return {"facet":name,"parts_listed":len(items),"covered_share_%":round(float(n.sum())/TOTAL*100,1),
            "arrow_dominant":arrow,"top3_%":top,"top2_combined_%":top2,
            "effective_dimension":round(eff_dim,1),"concentration_HHI":round(hhi,3)}

def main():
    reads = [read_composition("department/jurisdiction (who holds the data)", ORG),
             read_composition("format (how the data is shaped)", FMT),
             read_composition("jurisdiction level", JUR),
             read_composition("collection type", COLL)]
    findings = [
     "Two mandates dominate: Natural Resources (NRCan) + Statistics Canada together = %.1f%% of the WHOLE catalogue from just 2 of 100+ bodies."
       % ((ORG["Natural Resources (NRCan)"]+ORG["Statistics Canada"])/TOTAL*100),
     "Open-data output does NOT track population/economy: Yukon (pop ~45k) contributes %d datasets -- ~3x Ontario (%d), far above its ~0.1%% share of national population. A mandate-and-culture signal, not a size signal."
       % (ORG["Yukon"], ORG["Ontario"]),
     "Format is metadata-heavy: HTML (landing/metadata) is the plurality (%.0f%% of format tags); the machine-readable core (CSV+XLSX+JSON+GEOJSON) is a smaller, identifiable share."
       % (FMT["HTML"]/sum(FMT.values())*100),
     "Effective dimension is far below the part count: ~%.0f equivalent departments out of 40+ listed, ~%.0f equivalent formats out of 26 -- the estate is concentrated, so a compositional read (not a headcount) is the right lens."
       % (reads[0]["effective_dimension"], reads[1]["effective_dimension"]),
    ]
    out = {"demo":"Hs reads the composition of Canada's entire open-data estate","source":SOURCE,
           "total_datasets":TOTAL,"reads":reads,"surprising_findings":findings,
           "honest_note":"Counts are real catalogue metadata; shares/arrows/effective-dimension are deterministic. Interpretation is descriptive (what the data structure IS), not a political judgment. Format shares are over resource-format tags (a dataset carries several), so they sum to >100% of datasets; HTML reflects metadata/landing pages, not data content."}
    out["content_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()
    print(json.dumps(out,indent=2))

if __name__ == "__main__":
    main()
