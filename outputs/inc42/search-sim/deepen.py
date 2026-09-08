import json,urllib.request,time,sys,itertools
def post(body,retry=2):
    r=urllib.request.Request("https://datalabs-api.inc42.com/header/global-search",
        data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json","Referer":"https://inc42.com/","User-Agent":"Mozilla/5.0"})
    for i in range(retry+1):
        try: return json.load(urllib.request.urlopen(r,timeout=25))
        except Exception as e:
            if i==retry: return {"_err":str(e)}
            time.sleep(3)
# pull deeper competitor sets around every token that appears in the regression set
TARGETS=["cred","credi","credit","creda","credo","crede","ola","olaa","olan","olar","navi","navig",
 "navik","iifl","finance","financ","financi","wagh","bakri","lava","mobile","mobil","tbo","tek",
 "ultra","ultrav","viole","apax","bird","eye","birde","speci","special","ofbus","busine","zepto",
 "zomato","zomat","kirana","eternal","bundl","ani ","razor","razorp","flip","flipk","sequo","peak",
 "matter","motor","third","wave","brew","hustle","ledger","alpha","vector","swig","payt","phone",
 "cars","meesh","groww","dunzo","udaan","byjus","unacad","urban","boat","mama","nykaa","shipro","ship"]
corp=json.load(open("corpus.json"))
comp={r["objectID"]:r for r in corp["companies"]}
peo={r["objectID"]:r for r in corp["people"]}
inv={r["objectID"]:r for r in corp["investors"]}
before=len(comp)
for i,q in enumerate(TARGETS):
    d=post({"keyword":q})
    if "_err" in d: print("ERR",q,file=sys.stderr); time.sleep(2); continue
    r=d.get("response") or {}
    for row in (r.get("companies") or []): comp[row["objectID"]]=row
    for row in (r.get("person") or []): peo[row["objectID"]]=row
    for row in (r.get("investor") or []): inv[row["objectID"]]=row
    corp["counts"][q]=d.get("count")
    if i%20==0: print(f"{i}/{len(TARGETS)} {q!r} count={d.get('count')} comp={len(comp)}",file=sys.stderr)
    time.sleep(0.7)
corp["companies"]=list(comp.values()); corp["people"]=list(peo.values()); corp["investors"]=list(inv.values())
json.dump(corp,open("corpus.json","w"))
print(f"companies {before} -> {len(comp)} | people {len(peo)} | investors {len(inv)}")
