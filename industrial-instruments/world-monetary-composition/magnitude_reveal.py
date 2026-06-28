import hashlib, json

RES_TOTAL_2024=12.36e12; RES_TOTAL_2001=2.05e12
COFER_2024={"USD":58,"EUR":20,"JPY":6,"GBP":5,"CNY":2,"Nontraditional":9}
GDP_2023={"United States":27.292,"China":18.270,"Japan":4.213,"Germany":4.562,"India":3.638,
          "United Kingdom":3.421,"France":3.056,"Italy":2.317,"Brazil":2.191,"Canada":2.173}
GDP_2009={"United States":14.478,"China":5.190,"Japan":5.289,"Germany":3.479,"India":1.342,
          "United Kingdom":2.429,"France":2.700,"Italy":2.209,"Brazil":1.667,"Canada":1.375}

res_2024_usd={k:round(v/100*RES_TOTAL_2024/1e12,2) for k,v in COFER_2024.items()}
usd_2001=round(0.72*RES_TOTAL_2001/1e12,1); usd_2024=round(0.58*RES_TOTAL_2024/1e12,1)
ten_2023=round(sum(GDP_2023.values()),1); ten_2009=round(sum(GDP_2009.values()),1)
gdp_add={k:round(GDP_2023[k]-GDP_2009[k],2) for k in GDP_2023}

out={
 "title":"The magnitude reveal -- shares x real totals = real dollars (all figures real & cited)",
 "RESERVES_money_layer":{
   "total_2024_$T":round(RES_TOTAL_2024/1e12,2),
   "by_currency_2024_$T":res_2024_usd,
   "USD_share_pct_2001_to_2024":[72,58],
   "USD_dollars_held_$T_2001_to_2024":[usd_2001,usd_2024],
   "the_honest_twist":"The dollar SHARE fell 72 to 58 percent, but the DOLLARS THEMSELVES grew about "+str(usd_2001)+"T to "+str(usd_2024)+"T -- roughly 5x -- because total reserves grew from ~$2T to ~$12.4T. A falling share is NOT a falling dollar holding; that is the magnitude the share alone hides."
 },
 "GDP_economy_layer":{
   "ten_economies_total_$T_2009_to_2023":[ten_2009,ten_2023],
   "world_total_2023_$T_approx":105.4,
   "ten_as_pct_of_world_2023":round(ten_2023/105.4*100),
   "absolute_added_2009_to_2023_$T":gdp_add,
   "reading":"China added ~$"+str(gdp_add["China"])+"T and the US ~$"+str(gdp_add["United States"])+"T of GDP 2009-2023 -- both grew in DOLLARS; China's SHARE rose because it grew faster, not because the US shrank."
 },
 "the_point":"For REAL measured data these magnitudes are public facts, not estimates -- completing them is MORE honest, not less. Fencing belongs only on the UNMEASURED value-of-Hs figures (the trillions, the $M/yr), which stay Tier 3.",
 "honest_note":"Reserve totals: IMF COFER ($12.36T 2024Q4 cited; ~$2T end-2001 widely-cited approximate). GDP: World Bank current US$ (mixes growth+price+FX). World total 2023 ~$105T (World Bank, approximate). Descriptive, not advice."
}
out["content_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()
print(json.dumps(out,indent=2))
