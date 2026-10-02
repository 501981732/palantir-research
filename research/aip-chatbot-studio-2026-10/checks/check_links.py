#!/usr/bin/env python3
"""Public HTTP check, independent of factual or tenant verification."""
from pathlib import Path
from urllib.request import Request,urlopen
import concurrent.futures,datetime,json,sys
ROOT=Path(__file__).resolve().parents[1]
registry=json.loads((ROOT/'notes/source-registry.json').read_text())
cached={}
if (ROOT/'checks/links.json').exists() and '--refresh' not in sys.argv:
    previous=json.loads((ROOT/'checks/links.json').read_text())
    cached={r['url']:{**r,'checked_at_utc':r.get('checked_at_utc',previous['checked_at_utc'])} for r in previous['links']}
def check(r):
    if r['url'] in cached:return {**cached[r['url']],'id':r['id'],'title':r['title']}
    row={'id':r['id'],'url':r['url'],'title':r['title']}
    row['checked_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with urlopen(Request(r['url'],headers={'User-Agent':'AIP-Chatbot-Research-Link-Check/1.0'}),timeout=25) as resp:
            sample=resp.read(16384);final=resp.url
            row.update(http_status=resp.status,final_url=final,content_type=resp.headers.get('Content-Type'),status='passed' if resp.status==200 and not final.rstrip('/').endswith('/404') else 'failed')
    except Exception as e:row.update(status='unavailable',error=type(e).__name__+': '+str(e))
    return row
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:rows=list(ex.map(check,registry))
result={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Public HTTP reachability only; not source accuracy, video viewing, tenant ability or CI','links':rows,'summary':{s:sum(x['status']==s for x in rows) for s in ['passed','failed','unavailable']}}
(ROOT/'checks/links.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result['summary']))
