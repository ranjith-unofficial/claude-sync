import json,re,csv,math
from engine import Doc,norm

corp=json.load(open("corpus.json"))
# real quality signals from the 443-row DataLabs pull
emp={}; fund={}
try:
    for r in csv.DictReader(open("/Users/cepl/ClaudeDocs/inc42/brief-data/datalabs_company_pages_443.csv")):
        if r.get("employees"): 
            try: emp[r["slug"]]=int(float(r["employees"]))
            except: pass
        if r.get("total_funding_str"):
            try: fund[r["slug"]]=float(r["total_funding_str"])
            except: pass
except Exception as e: print("csv:",e)

MULT={"K":1e3,"M":1e6,"B":1e9}
def parse_fund(desc):
    m=re.search(r"\$([\d.]+)\s*([KMB])",desc or "")
    return float(m.group(1))*MULT[m.group(2)] if m else None

def bucket_fund(v):
    if v is None: return None
    if v<1e6: return 0.3
    if v<1e7: return 0.5
    if v<1e8: return 0.7
    if v<1e9: return 0.9
    return 1.0
def bucket_emp(n):
    if n is None: return None
    return 0.2 if n<=10 else 0.4 if n<=50 else 0.6 if n<=200 else 0.8 if n<=1000 else 1.0

def quality_company(row):
    d=row.get("description") or ""; slug=row.get("slug")
    f=parse_fund(d) or fund.get(slug)
    e=emp.get(slug)
    bf=bucket_fund(f); be=bucket_emp(e)
    status=0.3 if re.search(r"shut ?down|acquired|defunct",d,re.I) else 1.0
    completeness=0.9 if f else 0.5
    recency=0.6                      # not exposed by this endpoint -> neutral
    trending=0.0                     # PRD: 'rest = 0'
    parts=[(bf if bf is not None else 0.4,0.25),(be if be is not None else 0.4,0.15),
           (status,0.20),(recency,0.15),(completeness,0.10),(trending,0.15)]
    return max(0.1,min(1.0,sum(v*w for v,w in parts)))

index=[]; 
for r in corp["companies"]:
    index.append(Doc(r["objectID"],r["name"],"company",r.get("description"),quality_company(r),
                     {"slug":r.get("slug")}))
for r in corp["people"]:
    d=r.get("description") or ""
    sen=1.0 if re.search(r"founder|ceo|cxo|chief|cto|coo|cfo",d,re.I) else 0.7 if re.search(r"vp|vice president|director",d,re.I) else 0.5
    index.append(Doc(r["objectID"],r["name"],"person",d,max(0.1,0.30*sen+0.30*0.5+0.20*1.0+0.0),{"slug":r.get("slug")}))
for r in corp["investors"]:
    index.append(Doc(r["objectID"],r["name"],"investor",r.get("description"),0.55,{"slug":r.get("slug")}))
# industries (PRD's new index) - small synthetic set from real sectors
SECT=["Fintech","Ecommerce","Edtech","Health Tech","Enterprise Tech","Consumer Services",
      "Logistics","Clean Tech","Media & Entertainment","Travel Tech","Deeptech","Agritech"]
for s in SECT: index.append(Doc("IND-"+s,s,"industry","Industry sector page",0.85))
json.dump({"n":len(index)},open("_built.json","w"))
print("indexed:",len(index),"| companies",sum(1 for d in index if d.etype=="company"),
      "people",sum(1 for d in index if d.etype=="person"),
      "investors",sum(1 for d in index if d.etype=="investor"),
      "industries",len(SECT))
q=[d for d in index if d.name.upper()=="CRED"]
print("CRED in index:",[(d.id,d.name,round(d.quality,3)) for d in q])
print("docs whose name contains 'cred':",sum(1 for d in index if 'cred' in norm(d.name)))
