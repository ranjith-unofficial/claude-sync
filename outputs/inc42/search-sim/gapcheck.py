import json,urllib.request,time
def post(k):
    r=urllib.request.Request("https://datalabs-api.inc42.com/header/global-search",
        data=json.dumps({"keyword":k}).encode(),
        headers={"Content-Type":"application/json","Referer":"https://inc42.com/","User-Agent":"Mozilla/5.0"})
    try: return json.load(urllib.request.urlopen(r,timeout=25))
    except Exception as e: return {"_err":str(e)}
CHECKS=[("wagh bakri","wagh bakri"),("wagh","wagh bakri"),("bakri","bakri"),
        ("lava","lava"),("lava mobile","lava"),("tbo tek","tbo tek"),("tbotek","tbo tek"),
        ("tbo","tbo"),("birdeye","birdeye"),("bird eye","bird"),("iifl finance","iifl finance"),
        ("iifl","iifl finance"),("eternal limited","eternal"),("ani technologies","ani technologies"),
        ("matter motor","matter"),("third wave","third wave"),("cred","cred"),("ola","ola"),("navi","navi")]
for q,expect in CHECKS:
    d=post(q); time.sleep(0.7)
    if "_err" in d: print(f"{q:18} ERR"); continue
    r=d.get("response") or {}
    co=[x["name"] for x in (r.get("companies") or [])]
    hit=[n for n in co if expect.lower() in n.lower()]
    print(f"{q:18} count={str(d.get('count')):>6}  rows={len(co):>2}  match={hit[:2]}  top3={co[:3]}")
