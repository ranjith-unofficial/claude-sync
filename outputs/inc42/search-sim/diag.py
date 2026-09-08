from engine import search,norm,score,toks,metaphone,lev
import build; index=build.index
A={}; B={"msm":True,"floor":0.30,"squash":True,"alias":True,"token":True}
for q in ["apax","sequioa"]:
    print("="*100); print("QUERY:",q)
    qt=toks(q); qn=norm(q)
    cand=[]
    for d in index:
        s,f=score(d,qn,qt,B)
        if s>0: cand.append((s,d,f))
    cand.sort(key=lambda x:-x[0])
    print(f"{'RAW rank':>8} {'raw':>7} {'type':<9} {'name':<32} winning field")
    for i,(s,d,f) in enumerate(cand[:8],1):
        win=max(f,key=f.get)
        print(f"{i:>8} {s:7.3f} {d.etype:<9} {d.name[:30]:<32} {win}={f[win]:.2f} q={d.quality:.2f}")
    # what per-index normalisation does to them
    print("  -- after PRD per-index normalisation + type weight --")
    for r in search(index,q,B)[:6]:
        print(f"     final={r['score']:.3f}  raw={r['raw']:.3f}  {r['doc'].etype:<9} {r['doc'].name}")
