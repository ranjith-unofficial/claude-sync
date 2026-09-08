import re
from engine import search,norm
import build; index=build.index
A={}; C={"msm":True,"floor":0.30,"squash":True,"alias":True,"token":True,"globalnorm":True,"phon_guard":True}
D=dict(C,squash_single=True)
def rk(res,exp):
    for i,r in enumerate(res,1):
        if norm(exp) in norm(r["doc"].name): return i
    return None
print("third wave  : PRD=%s  C=%s  D(squash single-token only)=%s" % (
    rk(search(index,"third wave",A),"Third Wave Coffee"),
    rk(search(index,"third wave",C),"Third Wave Coffee"),
    rk(search(index,"third wave",D),"Third Wave Coffee")))
for q,e in [("ofbusiness","OfBusiness"),("waghbakri","wagh"),("tbotek","tbo")]:
    print(f"  {q:12}-> D rank {rk(search(index,q,D),e)}")
# ---- sensitivity: does REAL investor quality resolve 'sequioa'? ----
print("\nSENSITIVITY - investor quality (my sim uses a flat 0.55 for every investor)")
prom={"sequoia capital":0.95,"peak xv partners":0.95,"apax partners":0.85,"accel":0.9,"blume ventures":0.8}
for d in index:
    if d.etype=="investor": d.quality=prom.get(norm(d.name),0.30)
print("  after realistic investor quality:  sequioa -> rank",rk(search(index,"sequioa",D),"Sequoia Capital"))
print("  top-5:",[r["doc"].name for r in search(index,"sequioa",D)[:5]])
