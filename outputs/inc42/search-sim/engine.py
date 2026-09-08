"""Simulator of the Global Search PRD's scoring logic.
Implements: name.exact^10 > name.prefix^5 (edge-ngram 2..15) > name.fuzzy^2 (AUTO)
> name.phonetic^1 > description^0.5, multi_match/best_fields, function_score multiply
by _quality_score, per-index normalisation, cross-type weights. ES BM25 approximated:
within a field, matched query terms sum (coordination); across fields, max (best_fields).
"""
import json,re,math,unicodedata

# ---------- analysis ----------
def norm(s):
    s=unicodedata.normalize("NFKD",(s or "")).encode("ascii","ignore").decode()
    return re.sub(r"[^a-z0-9 ]+"," ",s.lower()).strip()
def toks(s): return [t for t in norm(s).split() if t]
def squash(s): return re.sub(r"[^a-z0-9]+","",(s or "").lower())      # R3: name_squash
def ngrams(t,lo=2,hi=15): return {t[:i] for i in range(lo,min(len(t),hi)+1)}

def metaphone(w):
    """Compact double-metaphone-style key: enough to model 'flipcart'->'flipkart'."""
    w=re.sub(r"[^a-z]","",w.lower())
    if not w: return ""
    w=re.sub(r"^(kn|gn|pn|ae|wr)","",w); w=re.sub(r"^x","s",w)
    r=[]
    i=0
    while i<len(w):
        c=w[i]; nx=w[i+1] if i+1<len(w) else ""
        if r and c==r[-1] and c!="c": i+=1; continue
        if c in "aeiou": r.append("A" if not r else ""); i+=1; continue
        if c=="c":
            if nx=="h": r.append("X"); i+=2; continue
            if nx in "iey": r.append("S"); i+=1; continue
            r.append("K"); i+=1; continue
        if c=="g":
            if nx=="h": r.append("K"); i+=2; continue
            if nx in "iey": r.append("J"); i+=1; continue
            r.append("K"); i+=1; continue
        if c=="p": r.append("F" if nx=="h" else "P"); i+=2 if nx=="h" else 1; continue
        if c=="q": r.append("K"); i+=1; continue
        if c=="s": r.append("X" if nx=="h" else "S"); i+=2 if nx=="h" else 1; continue
        if c=="t":
            if nx=="h": r.append("0"); i+=2; continue
            r.append("T"); i+=1; continue
        if c in "dv": r.append("T" if c=="d" else "F"); i+=1; continue
        if c=="z": r.append("S"); i+=1; continue
        if c=="k": r.append("K"); i+=1; continue
        if c=="x": r.append("KS"); i+=1; continue
        if c in "bfhjlmnrwy": r.append(c.upper()); i+=1; continue
        i+=1
    return "".join(r)

def lev(a,b,cap=3):
    if abs(len(a)-len(b))>cap: return cap+1
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]+[0]*len(b)
        for j,cb in enumerate(b,1):
            cur[j]=min(prev[j]+1,cur[j-1]+1,prev[j-1]+(ca!=cb))
        if min(cur)>cap: return cap+1
        prev=cur
    return prev[-1]
def auto_fuzz(t): return 0 if len(t)<=2 else (1 if len(t)<=5 else 2)   # ES AUTO

# ---------- index ----------
class Doc:
    __slots__=("id","name","etype","desc","quality","ntoks","ngr","phon","sq","meta")
    def __init__(s,id,name,etype,desc,quality,meta=None):
        s.id=id; s.name=name; s.etype=etype; s.desc=desc or ""; s.quality=quality
        s.meta=meta or {}
        s.ntoks=toks(name); s.sq=squash(name)
        s.ngr={}; 
        for t in s.ntoks: s.ngr[t]=ngrams(t)
        s.phon=[metaphone(t) for t in s.ntoks]

TYPE_W={"company":1.0,"investor":0.9,"person":0.8,"industry":0.6,"report":0.5}
SIZES={"company":5,"investor":3,"person":3,"industry":2,"report":2}   # PRD _msearch sizes

# ---------- scoring ----------
def fieldnorm(doc):
    # BM25 length normalisation: a 1-token name beats a 4-token name at equal term match
    return 1.0/math.sqrt(max(1,len(doc.ntoks)))

def field_scores(doc,q,qt,opts):
    nname=norm(doc.name)
    f={}
    # name.exact ^10  (keyword field: whole-string equality)
    f["exact"]=10.0 if nname==q else 0.0
    # R3 name_squash ^9 (refinement only)
    if opts.get("squash") and doc.sq and squash(q) and (len(qt)==1 or not opts.get("squash_single")):
        if doc.sq==squash(q): f["squash"]=9.0
        elif doc.sq.startswith(squash(q)) and len(squash(q))>=4: f["squash"]=6.0
    # R5: name.token ^7 - query token equals a complete name token (refinement only)
    if opts.get("token"):
        th=sum(1 for t in qt if t in doc.ntoks)
        if th: f["token"]=7.0*(th/len(qt))
    # name.prefix ^5 (edge-ngram, index-side)
    hit=0
    for t in qt:
        if any(t in doc.ngr[n] for n in doc.ngr): hit+=1
    f["prefix"]=5.0*(hit/len(qt)) if hit else 0.0
    # name.fuzzy ^2 (AUTO)
    fh=0; dsum=0
    for t in qt:
        best=99
        for n in doc.ntoks:
            d=lev(t,n,auto_fuzz(t))
            if d<=auto_fuzz(t): best=min(best,d)
        if best<99: fh+=1; dsum+=best
    f["fuzzy"]=2.0*(fh/len(qt))*(1-0.25*(dsum/max(fh,1))) if fh else 0.0
    prefix_hits_ref=[hit]; fuzzy_hits_ref=[fh]
    # name.phonetic ^1
    if opts.get("phon_guard"):
        ph=sum(1 for t in qt if len(t)>=5 and metaphone(t) and metaphone(t) in doc.phon)
        f["phonetic"]=1.0*(ph/len(qt)) if (ph and (prefix_hits_ref[0] or fuzzy_hits_ref[0])) else 0.0
    else:
        ph=sum(1 for t in qt if metaphone(t) and metaphone(t) in doc.phon)
        f["phonetic"]=1.0*(ph/len(qt)) if ph else 0.0
    # description ^0.5
    dt=set(toks(doc.desc))
    dh=sum(1 for t in qt if t in dt)
    f["desc"]=0.5*(dh/len(qt)) if dh else 0.0
    return f,hit,fh

def score(doc,q,qt,opts):
    f,prefix_hits,fuzzy_hits=field_scores(doc,q,qt,opts)
    matched=max(prefix_hits,fuzzy_hits, 1 if f["exact"] else 0)
    # R1: minimum_should_match — require ALL query tokens on multi-token queries
    sq_ok=bool(opts.get("squash") and doc.sq and squash(q) and (doc.sq==squash(q) or squash(q) in doc.sq))
    if opts.get("msm") and len(qt)>1 and matched<len(qt) and not f["exact"] and not sq_ok:
        return 0.0,f
    base=max(f.values()) if f else 0.0                 # best_fields = max across fields
    if base<=0: return 0.0,f
    return base*fieldnorm(doc)*doc.quality,f

def search(index,query,opts=None,per_type=None):
    opts=opts or {}; per_type=per_type or SIZES
    q=norm(query); qt=toks(query)
    if not qt: return []
    by={}
    for d in index:
        s,f=score(d,q,qt,opts)
        if s>0: by.setdefault(d.etype,[]).append((s,d,f))
    out=[]
    GLOBAL_MAX=10.0
    for et,rows in by.items():
        rows.sort(key=lambda r:-r[0])
        mx=rows[0][0]
        keep=rows[:per_type.get(et,5)]                  # PRD per-index size cap
        for s,d,f in keep:
            denom=GLOBAL_MAX if opts.get("globalnorm") else mx
            out.append({"score":(s/denom)*TYPE_W.get(et,1.0),"raw":s,"doc":d,"fields":f})
    out.sort(key=lambda r:-r["score"])
    # R2: relevance floor — drop rows far below the leader
    if opts.get("floor") and out:
        top=out[0]["score"]; out=[r for r in out if r["score"]>=opts["floor"]*top]
    return out[:10]
