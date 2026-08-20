/**
 * INC42 Sector Tagging Audit
 * Reads "Article - Raw - Last 60 days" and rebuilds every analysis tab.
 * Does NOT touch the raw tab or "Companies List without Sectors tagging".
 * Safe to re-run: it clears and rewrites only the tabs it owns.
 */

var RAW_TAB     = 'Article - Raw - Last 60 days';
var SUMMARY_TAB = 'Breif Analysis';
var OWNED = ['Gap Buckets','Sector Fix Plan','Taxonomy Leaks','Companies Untagged',
             'Inconsistent Companies','Gaps by Dev Tag','Gaps by Tag','Trend by Month','Sector Impact'];

var INK='#1f2937', HDR='#1f2937', HDRTXT='#ffffff';
var CRIT='#fce8e6', CRITTXT='#a32e22', WARN='#fdf0d5', WARNTXT='#9c6209',
    GOOD='#e3f0e8', GOODTXT='#2e6b4a', ACC='#e2eded', ACCTXT='#0b3d41', BAND='#f6f4ef';

var MISS = {'':1,'null':1,'undefined':1,'tbd':1,'n/a':1,'na':1,'-':1,'none':1};

function clean_(v){
  if(v===null||v===undefined) return '';
  var s=String(v).trim()
        .replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>')
        .replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&nbsp;/g,' ').trim();
  return MISS[s.toLowerCase()] ? '' : s;
}
function splitPipe_(s){
  if(!s) return [];
  return s.split('|').map(function(x){return x.trim();})
          .filter(function(x){ return x && !MISS[x.toLowerCase()]; });
}
function topKey_(obj){
  var bk='', bv=-1;
  for(var k in obj) if(obj[k]>bv){bv=obj[k];bk=k;}
  return bk;
}
function pct_(a,b){ return b ? Math.round(a/b*1000)/10 : 0; }

function buildTaggingAudit(){
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var raw = ss.getSheetByName(RAW_TAB);
  if(!raw) throw new Error('Cannot find tab: '+RAW_TAB);

  var vals = raw.getDataRange().getValues();
  var head = vals[0].map(function(h){return String(h).trim();});
  var col={}; head.forEach(function(h,i){col[h]=i;});
  ['ID','article_title','slug','published_date','development_tag','sector','companies',
   'tags','location','industries','primary_industry','secondary_industry'].forEach(function(c){
     if(col[c]===undefined) throw new Error('Raw tab missing column: '+c);
  });

  // ---------- parse ----------
  var rows=[];
  for(var i=1;i<vals.length;i++){
    var r=vals[i];
    if(!String(r[col.ID]).trim()) continue;
    var d=r[col.published_date];
    var ds = (d instanceof Date) ? Utilities.formatDate(d, ss.getSpreadsheetTimeZone(), 'yyyy-MM-dd HH:mm:ss') : String(d).trim();
    var industries = clean_(r[col.industries]);
    var path = splitPipe_(industries);
    var o={
      id:String(r[col.ID]).trim(),
      title:String(r[col.article_title]).trim(),
      slug:String(r[col.slug]).trim(),
      date:ds,
      month:ds.substring(0,7),
      dev:clean_(r[col.development_tag]),
      sector:clean_(r[col.sector]),
      companiesRaw:clean_(r[col.companies]),
      tags:clean_(r[col.tags]),
      location:clean_(r[col.location]),
      industries:industries,
      prim:clean_(r[col.primary_industry]),
      sec:clean_(r[col.secondary_industry]),
      path:path,
      indRoot: path.length?path[0]:''
    };
    o.cos = splitPipe_(o.companiesRaw);
    o.url = 'https://inc42.com/buzz/'+o.slug;
    rows.push(o);
  }
  var N=rows.length;

  // ---------- taxonomy ----------
  var sectorSet={}, SECTORS=[];
  rows.forEach(function(o){ if(o.sector && !sectorSet[o.sector]){sectorSet[o.sector]=1; SECTORS.push(o.sector);} });
  SECTORS.sort();

  var parentVotes={};
  rows.forEach(function(o){
    if(o.path.length>1 && sectorSet[o.path[0]]){
      for(var j=1;j<o.path.length;j++){
        var n=o.path[j];
        if(!parentVotes[n]) parentVotes[n]={};
        parentVotes[n][o.path[0]] = (parentVotes[n][o.path[0]]||0)+1;
      }
    }
  });
  var ORPHAN={};
  for(var n in parentVotes) ORPHAN[n]=topKey_(parentVotes[n]);
  ORPHAN['AgriTech']='Agritech';

  // company -> sector history
  var coSector={};
  rows.forEach(function(o){
    if(o.sector) o.cos.forEach(function(c){
      var k=c.toLowerCase();
      if(!coSector[k]) coSector[k]={};
      coSector[k][o.sector]=(coSector[k][o.sector]||0)+1;
    });
  });

  // ---------- resolve suggested sector ----------
  rows.forEach(function(o){
    o.sug=''; o.conf=''; o.how='';
    var srcs=[['industries root',o.indRoot],['primary_industry',o.prim]];
    for(var s=0;s<srcs.length && !o.sug;s++){
      var label=srcs[s][0], val=srcs[s][1];
      if(!val) continue;
      if(sectorSet[val]){ o.sug=val; o.conf='High'; o.how=label+' is already a valid sector'; }
      else if(ORPHAN[val]){ o.sug=ORPHAN[val]; o.conf='High'; o.how=label+" '"+val+"' rolled up to parent"; }
    }
    if(!o.sug){
      var votes={}, any=false;
      o.cos.forEach(function(c){
        var h=coSector[c.toLowerCase()];
        if(h){ any=true; for(var k in h) votes[k]=(votes[k]||0)+h[k]; }
      });
      if(any){
        var t=topKey_(votes);
        o.sug=t; o.conf=(votes[t]>1?'Medium':'Low');
        o.how='company history ('+votes[t]+' prior article'+(votes[t]>1?'s':'')+')';
      }
    }
    if(!o.sug){
      o.conf='Manual';
      o.how = o.cos.length ? 'company known but never sector-tagged'
                           : 'no company, no industry - needs editorial tagging';
    }
  });

  // ---------- helpers to count ----------
  function cnt(f){ var c=0; rows.forEach(function(o){ if(f(o)) c++; }); return c; }
  var noSector = rows.filter(function(o){return !o.sector;});
  var missSector=cnt(function(o){return !o.sector;});
  var missCo    =cnt(function(o){return !o.cos.length;});
  var missPrim  =cnt(function(o){return !o.prim;});

  // =========================================================
  // TAB: Summary  (rewrite the existing analysis tab)
  // =========================================================
  var resolvable = noSector.filter(function(o){return o.sug;}).length;
  var coKnown    = noSector.filter(function(o){return !o.sug && o.cos.length;}).length;
  var dark       = noSector.length - resolvable - coKnown;
  var fullyDark  = cnt(function(o){return !o.cos.length && !o.sector && !o.prim;});
  var bothFilled = rows.filter(function(o){return o.sector && o.prim;});
  var agree      = bothFilled.filter(function(o){return o.sector.toLowerCase()===o.prim.toLowerCase();}).length;
  var bucketF    = cnt(function(o){return !o.sector && o.prim;});
  var leakCount  = 0, leakSeen={};
  rows.forEach(function(o){ if(o.prim && !sectorSet[o.prim] && !leakSeen[o.prim]){leakSeen[o.prim]=1; leakCount++;} });

  var S=[];
  S.push(['INC42 SECTOR TAGGING AUDIT','','','']);
  S.push(['Source: '+RAW_TAB+'  ·  '+N+' articles  ·  rebuilt '+
          Utilities.formatDate(new Date(), ss.getSpreadsheetTimeZone(),'d MMM yyyy HH:mm'),'','','']);
  S.push(['','','','']);
  S.push(['HEADLINE','Count','% of '+N,'Note']);
  S.push(['Articles with no sector',missSector,pct_(missSector,N)+'%','The core gap']);
  S.push(['Articles with no company',missCo,pct_(missCo,N)+'%','108 are the literal string TBD']);
  S.push(['Fully dark articles',fullyDark,pct_(fullyDark,N)+'%','No company, no sector, no industry']);
  S.push(['Auto-fixable today',resolvable,pct_(resolvable,N)+'%','From data already in the row']);
  S.push(['Taxonomy leak values',leakCount,'','Sub-industries stored as top level']);
  S.push(['','','','']);
  S.push(['THE '+missSector+', DECOMPOSED','Count','% of gap','Fix']);
  S.push(['Resolvable from the same row',resolvable,pct_(resolvable,missSector)+'%','Script - copy or one-hop roll-up']);
  S.push(['Company known, never sector-tagged',coKnown,pct_(coKnown,missSector)+'%','Fix company master once']);
  S.push(['Genuinely dark',dark,pct_(dark,missSector)+'%','Needs a human']);
  S.push(['','','','']);
  S.push(['ROOT CAUSE','','','']);
  S.push([bucketF+' articles have primary_industry filled but sector blank.','','','']);
  S.push(['Where both are filled they agree '+pct_(agree,bothFilled.length)+'% ('+agree+' of '+bothFilled.length+').','','','']);
  S.push(['Sector is not authored independently - it is a copy of industry that silently fails to write.','','','']);
  S.push(['','','','']);
  S.push(['FIELD COMPLETENESS','Filled','Missing','Missing %']);
  [['Tag','tags'],['Sector','sector'],['Secondary industry','sec'],['Location','location'],
   ['Companies','companiesRaw'],['Industries path','industries'],['Primary industry','prim'],
   ['Development tag','dev']].forEach(function(p){
     var m=cnt(function(o){return !o[p[1]];});
     S.push([p[0],N-m,m,pct_(m,N)+'%']);
  });
  S.push(['','','','']);
  S.push(['WHAT TO DO','','','']);
  S.push(['1. Fix the write, not the rows','Sector agrees with industry '+pct_(agree,bothFilled.length)+'% and is blank on '+bucketF+' rows where industry is set. Make the derive step fire on every publish and edit.','','']);
  S.push(['2. Add Startup Ecosystem as a sector','Trackers, round-ups, fund launches and 11 investor entities have a real industry value with no sector to map to.','','']);
  S.push(['3. Run the '+resolvable+'-row backfill','See the Sector Fix Plan tab. Deterministic and reversible.','','']);
  S.push(['4. Resolve '+leakCount+' orphan taxonomy values','Map each sub-industry to its parent, merge AgriTech into Agritech, add a validation rule.','','']);
  S.push(['5. Backfill companies in the company master','See Companies Untagged. Fix once, every past and future article inherits.','','']);
  S.push(['6. Give the '+fullyDark+' dark articles a fallback','Mostly Government & Policies, Business Updates, Controversies. Decide rather than let them fall through.','','']);
  S.push(['7. Replace the blank sentinels with real nulls','NULL, null, undefined, TBD and empty string all mean the same thing today.','','']);

  var sum = ss.getSheetByName(SUMMARY_TAB) || ss.insertSheet(SUMMARY_TAB);
  sum.clear();
  sum.getRange(1,1,S.length,4).setValues(S);
  sum.getRange('A1').setFontSize(16).setFontWeight('bold').setFontColor(INK);
  sum.getRange('A2').setFontColor('#6b7683').setFontSize(9);
  [4,11,16,21,30].forEach(function(r){
    sum.getRange(r,1,1,4).setBackground(HDR).setFontColor(HDRTXT).setFontWeight('bold');
  });
  sum.getRange(17,1,3,1).setFontColor(ACCTXT).setBackground(ACC);
  sum.getRange(5,2,5,1).setFontWeight('bold');
  sum.setColumnWidth(1,340); sum.setColumnWidth(2,300);
  sum.setColumnWidth(3,90);  sum.setColumnWidth(4,260);
  sum.setFrozenRows(2);

  // =========================================================
  function writeTab(name, header, data, widths, chipCol){
    var sh = ss.getSheetByName(name);
    if(sh) sh.clear(); else sh = ss.insertSheet(name);
    sh.getRange(1,1,1,header.length).setValues([header])
      .setBackground(HDR).setFontColor(HDRTXT).setFontWeight('bold').setWrap(true);
    if(data.length) sh.getRange(2,1,data.length,header.length).setValues(data);
    sh.setFrozenRows(1);
    if(data.length) sh.getRange(1,1,data.length+1,header.length).createFilter();
    (widths||[]).forEach(function(w,i){ if(w) sh.setColumnWidth(i+1,w); });
    if(chipCol){
      for(var r=0;r<data.length;r++){
        var v=String(data[r][chipCol-1]);
        var bg=null,fg=null;
        if(/^High$/.test(v)||/Auto roll-up/.test(v)||/Backfill/.test(v)){bg=GOOD;fg=GOODTXT;}
        else if(/^Medium$/.test(v)||/^Low$/.test(v)||/duplicate/i.test(v)){bg=WARN;fg=WARNTXT;}
        else if(/^Manual$/.test(v)||/No parent/i.test(v)){bg=CRIT;fg=CRITTXT;}
        if(bg) sh.getRange(r+2,chipCol).setBackground(bg).setFontColor(fg).setFontWeight('bold');
      }
    }
    sh.getRange(1,1,1,header.length).setVerticalAlignment('middle');
    return sh;
  }

  // ---- Gap Buckets ----
  var gb=[
   ['A','Companies present, Sector MISSING', cnt(function(o){return o.cos.length&&!o.sector;}),'Fixable - company known, sector not set'],
   ['B','Companies present, Primary Industry MISSING', cnt(function(o){return o.cos.length&&!o.prim;}),'Fixable - needs industry mapping'],
   ['C','Companies MISSING and Sector MISSING', cnt(function(o){return !o.cos.length&&!o.sector;}),'Fully untagged - needs editorial tagging'],
   ['D','Companies + Sector + Primary Industry ALL missing', fullyDark,'Dark - invisible to every personalisation surface'],
   ['E','Sector present, Primary Industry missing', cnt(function(o){return o.sector&&!o.prim;}),'Sector is never set without an industry'],
   ['F','Primary Industry present, Sector MISSING', bucketF,'THE BIG ONE - sector not synced from industry'],
   ['G','Location missing while Companies present', cnt(function(o){return o.cos.length&&!o.location;}),'Company record has no HQ mapped'],
   ['H','Primary Industry is NOT a valid Sector value', cnt(function(o){return o.prim&&!sectorSet[o.prim];}),'Taxonomy leak - sub-industry as top level']
  ].map(function(x){ return [x[0],x[1],x[2],pct_(x[2],N)+'%',x[3]]; });
  writeTab('Gap Buckets',['Bucket','Definition','Articles','% of '+N,'What it means'],gb,[70,340,80,80,380]);

  // ---- Sector Fix Plan ----
  var order={High:0,Medium:1,Low:2,Manual:3};
  var fp = noSector.slice().sort(function(a,b){
    return (order[a.conf]-order[b.conf]) || (a.date<b.date?1:-1);
  }).map(function(o){
    return [o.id,o.title,o.url,o.date,o.dev||'(blank)',o.tags||'(blank)',
            o.companiesRaw||'(none)',o.sug||'(manual)',o.conf,o.how,
            o.prim||'(blank)',o.industries||'(blank)',o.location||'(blank)'];
  });
  writeTab('Sector Fix Plan',
    ['ID','Article Title','URL','Published','Development Tag','Tag','Companies',
     'SUGGESTED SECTOR','Confidence','How derived','Primary Industry','Industries Path','Location'],
    fp,[80,340,240,140,150,120,180,170,90,240,150,300,180],9);

  // ---- Taxonomy Leaks ----
  var leakCnt={};
  rows.forEach(function(o){ if(o.prim && !sectorSet[o.prim]) leakCnt[o.prim]=(leakCnt[o.prim]||0)+1; });
  var tl=Object.keys(leakCnt).map(function(k){
    return [k, leakCnt[k], ORPHAN[k]||'(unmapped)',
            ORPHAN[k] ? 'Auto roll-up' : 'No parent - add to sector list'];
  }).sort(function(a,b){return b[1]-a[1];});
  writeTab('Taxonomy Leaks',['Value stored in Primary Industry','Articles','Correct parent sector','Status'],
           tl,[300,90,220,260],4);

  // ---- Companies Untagged ----
  var coCount={}, coDisplay={}, coRows={};
  rows.forEach(function(o){ o.cos.forEach(function(c){
    var k=c.toLowerCase();
    coCount[k]=(coCount[k]||0)+1;
    if(!coDisplay[k]) coDisplay[k]=c;
    if(!coRows[k]) coRows[k]=[];
    coRows[k].push(o);
  });});
  var untagged=[], inconsistent=[];
  Object.keys(coCount).forEach(function(k){
    var list=coRows[k];
    if(!coSector[k]){
      var prims={}, sugs={};
      list.forEach(function(o){ if(o.prim) prims[o.prim]=1; if(o.sug) sugs[o.sug]=1; });
      var sg=Object.keys(sugs);
      untagged.push([coDisplay[k], coCount[k], Object.keys(prims).join(' | ')||'(none)',
                     sg.length?sg[0]:'(manual)', sg.length?'Auto roll-up':'Manual',
                     list[0].title, list[0].url]);
    } else {
      var miss=list.filter(function(o){return !o.sector;}).length;
      if(miss) inconsistent.push([coDisplay[k], coCount[k], miss,
                                  Object.keys(coSector[k]).join(' / '),
                                  'Backfill - sector already known']);
    }
  });
  untagged.sort(function(a,b){return b[1]-a[1];});
  inconsistent.sort(function(a,b){return b[2]-a[2];});
  writeTab('Companies Untagged',
    ['Company','Articles','Primary Industry seen','Suggested Sector','Status','Sample article','Sample URL'],
    untagged,[220,80,240,220,120,360,260],5);
  writeTab('Inconsistent Companies',
    ['Company','Total articles','Articles missing sector','Sector used elsewhere','Fix'],
    inconsistent,[220,110,150,280,240],5);

  // ---- grouped gap tables ----
  function groupTable(keyFn, blankLabel){
    var g={};
    rows.forEach(function(o){
      var k=keyFn(o)||blankLabel;
      if(!g[k]) g[k]={n:0,s:0,c:0,p:0};
      g[k].n++;
      if(!o.sector) g[k].s++;
      if(!o.cos.length) g[k].c++;
      if(!o.prim) g[k].p++;
    });
    return Object.keys(g).map(function(k){
      return [k,g[k].n,g[k].s,pct_(g[k].s,g[k].n)+'%',g[k].c,pct_(g[k].c,g[k].n)+'%',g[k].p];
    }).sort(function(a,b){return b[1]-a[1];});
  }
  writeTab('Gaps by Dev Tag',
    ['Development Tag','Articles','No sector','Sector missing %','No company','Company missing %','No primary industry'],
    groupTable(function(o){return o.dev;},'(no dev tag)'),[240,90,90,130,100,140,150]);
  writeTab('Gaps by Tag',
    ['Tag','Articles','No sector','Sector missing %','No company','Company missing %','No primary industry'],
    groupTable(function(o){return o.tags;},'(no tag)'),[280,90,90,130,100,140,150]);

  // ---- Trend by Month ----
  var mg={};
  rows.forEach(function(o){
    if(!mg[o.month]) mg[o.month]={n:0,s:0,c:0,p:0};
    mg[o.month].n++;
    if(!o.sector) mg[o.month].s++;
    if(!o.cos.length) mg[o.month].c++;
    if(!o.prim) mg[o.month].p++;
  });
  var tm=Object.keys(mg).sort().map(function(k){
    return [k,mg[k].n,mg[k].s,pct_(mg[k].s,mg[k].n)+'%',pct_(mg[k].c,mg[k].n)+'%',pct_(mg[k].p,mg[k].n)+'%'];
  });
  writeTab('Trend by Month',
    ['Month','Articles','No sector','Sector missing %','Company missing %','Primary industry missing %'],
    tm,[110,90,90,140,150,190]);

  // ---- Sector Impact ----
  var cur={}, aft={};
  rows.forEach(function(o){
    if(o.sector){ cur[o.sector]=(cur[o.sector]||0)+1; aft[o.sector]=(aft[o.sector]||0)+1; }
    else if(o.sug){ aft[o.sug]=(aft[o.sug]||0)+1; }
  });
  var keys={}; Object.keys(cur).forEach(function(k){keys[k]=1;}); Object.keys(aft).forEach(function(k){keys[k]=1;});
  var si=Object.keys(keys).map(function(k){
    var c=cur[k]||0, a=aft[k]||0;
    return [k,c,a,a-c, c? '+'+Math.round((a-c)/c*100)+'%' : 'new'];
  }).sort(function(a,b){return b[2]-a[2];});
  writeTab('Sector Impact',['Sector','Tagged today','After backfill','Added','Uplift'],
           si,[280,120,120,90,90]);

  // ---- ordering: analysis tabs after the summary ----
  var pos=2;
  OWNED.forEach(function(nm){
    var sh=ss.getSheetByName(nm);
    if(sh){ ss.setActiveSheet(sh); ss.moveActiveSheet(pos++); }
  });
  ss.setActiveSheet(sum);

  SpreadsheetApp.getUi().alert(
    'Tagging audit rebuilt\n\n'+
    N+' articles analysed\n'+
    missSector+' missing sector ('+pct_(missSector,N)+'%)\n'+
    resolvable+' auto-fixable\n'+
    fullyDark+' fully dark\n\n'+
    'Raw data tab and Companies List tab were not modified.');
}
