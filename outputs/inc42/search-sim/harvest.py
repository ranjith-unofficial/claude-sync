import json,urllib.request,time,string,sys
def post(body,retry=2):
    r=urllib.request.Request("https://datalabs-api.inc42.com/header/global-search",
        data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json","Referer":"https://inc42.com/","User-Agent":"Mozilla/5.0"})
    for i in range(retry+1):
        try: return json.load(urllib.request.urlopen(r,timeout=25))
        except Exception as e:
            if i==retry: return {"_err":str(e)}
            time.sleep(3)

# regression set (known failures) + broad prefix sweep for noise
REG=["cred","ola","navi","zomato","zomto","shiprocket","shipr","iifl finance","wagh bakri",
     "waghbakri","lava mobile","tbotek","ultraviolette","ultravio","apax","birdeye","speciale",
     "ofbusiness","zepto","kiranakart","eternal","bundl","ani technologies","razorpay","razorpey",
     "flipkart","flipcart","sequoia","sequioa","peak xv","matter motor","third wave","lava",
     "brewnexa","hustle hard","emerging ledger","alphavector","swiggy","paytm","phonepe","cars24",
     "meesho","groww","dunzo","udaan","byju","unacademy","urban company","boat","mamaearth","nykaa"]
PRE=[a+b for a in "abcdefgilmnoprstuvz" for b in "aeio"]  # 76 two-char prefixes
SEEDS=REG+PRE
comp={}; people={}; inv={}; counts={}
for i,q in enumerate(SEEDS):
    d=post({"keyword":q})
    if "_err" in d: print("ERR",q,d["_err"][:60],file=sys.stderr); time.sleep(2); continue
    r=d.get("response") or {}
    counts[q]=d.get("count")
    for row in (r.get("companies") or []): comp[row.get("objectID") or row.get("slug")]=row
    for row in (r.get("person") or []): people[row.get("objectID") or row.get("slug")]=row
    for row in (r.get("investor") or []): inv[row.get("objectID") or row.get("slug")]=row
    if i%15==0: print(f"{i}/{len(SEEDS)} q={q!r} count={d.get('count')} corpus={len(comp)}",file=sys.stderr)
    time.sleep(0.7)
json.dump({"companies":list(comp.values()),"people":list(people.values()),
           "investors":list(inv.values()),"counts":counts},open("corpus.json","w"))
print(f"DONE companies={len(comp)} people={len(people)} investors={len(inv)} queries={len(counts)}")
