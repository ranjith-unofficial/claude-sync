import json,sys
from engine import search,norm
import build   # builds `index`
index=build.index

ALIAS={"eternal limited":"Zomato","eternal":"Zomato","kiranakart":"Zepto",
       "bundl technologies":"Swiggy","ani technologies":"Ola"}

def run(q,cfg):
    query=q
    if cfg.get("alias") and norm(q) in ALIAS: query=ALIAS[norm(q)]
    res=search(index,query,cfg)
    if cfg.get("msm") and not res:                     # R1 fallback: AND -> OR
        c=dict(cfg); c["msm"]=False; res=search(index,query,c)
    return res

def rank_of(res,expect):
    for i,r in enumerate(res,1):
        if norm(r["doc"].name)==norm(expect): return i
    for i,r in enumerate(res,1):
        if norm(expect) in norm(r["doc"].name): return i
    return None

# (query, expected entity)  -- only entities VERIFIED present in the live index
CASES=[("cred","CRED"),("ola","Ola"),("navi","Navi"),("zomato","Zomato"),
 ("zomto","Zomato"),("shipr","Shiprocket"),("razorpey","Razorpay"),("flipcart","Flipkart"),
 ("sequioa","Sequoia Capital"),("ultravio","Ultraviolette Automotive"),("apax","Apax Partners"),
 ("speciale","Speciale Invest"),("ofbusiness","OfBusiness"),("iifl finance","IIFL Finance"),
 ("matter motor","Matter"),("third wave","Third Wave Coffee"),("zepto","Zepto"),
 ("of business","OfBusiness"),("iifl","IIFL Finance"),("shiprocket","Shiprocket"),
 ("eternal limited","Zomato"),("kiranakart","Zepto")]

A={}                                        # PRD exactly as written
B={"msm":True,"floor":0.30,"squash":True,"alias":True,"token":True}
C=dict(B,globalnorm=True,phon_guard=True,squash_single=True)   # final: + squash as single-token fallback

print(f"{'query':<17}{'expected':<26}{'PRD rank':>9}{'  PRD top-3':<44}{'C rank':>7}  C top-3")
print("-"*140)
rows=[]
for q,exp in CASES:
    ra=run(q,A); rb=run(q,C)
    pa=rank_of(ra,exp); pb=rank_of(rb,exp)
    t3a=", ".join(r["doc"].name for r in ra[:3]) or "(none)"
    t3b=", ".join(r["doc"].name for r in rb[:3]) or "(none)"
    rows.append((q,exp,pa,pb))
    print(f"{q:<17}{exp:<26}{str(pa or 'MISS'):>9}  {t3a[:42]:<44}{str(pb or 'MISS'):>7}  {t3b[:42]}")
ok=lambda rs,i:sum(1 for r in rs if r[i] is not None)
top1=lambda rs,i:sum(1 for r in rs if r[i]==1)
print("-"*140)
print(f"PRD as written : found {ok(rows,2)}/{len(rows)}   rank-1 {top1(rows,2)}/{len(rows)}")
print(f"PRD + fixes    : found {ok(rows,3)}/{len(rows)}   rank-1 {top1(rows,3)}/{len(rows)}")
json.dump([[r[0],r[1],r[2],r[3]] for r in rows],open("results.json","w"))
