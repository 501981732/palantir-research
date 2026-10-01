#!/usr/bin/env python3
"""Check public citation URLs. HTTP success is not product/runtime verification."""
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
from urllib.request import urlopen,Request
import concurrent.futures, json,re,datetime
ROOT=Path(__file__).resolve().parents[1]
urls={}
for p in [ROOT/'README.md',*sorted((ROOT/'notes').glob('*.md'))]:
 for label,url in re.findall(r'\[([^\]]+)\]\((https?://[^) ]+)\)',p.read_text()):
  u=urlsplit(url); canon=urlunsplit((u.scheme,u.netloc,u.path.rstrip('/'),u.query,'')); urls.setdefault(canon,{'labels':set(),'used_in':set()});urls[canon]['labels'].add(label);urls[canon]['used_in'].add(str(p.relative_to(ROOT)))
def check(url):
 row={'url':url,'labels':sorted(urls[url]['labels']),'used_in':sorted(urls[url]['used_in'])}
 try:
  with urlopen(Request(url,headers={'User-Agent':'Carbon-research-link-check/1.0'}),timeout=35) as r:
   final=r.url;data=r.read(8192)
   row.update(http_status=r.status,final_url=final,content_type=r.headers.get('Content-Type'),status='passed' if r.status==200 and not final.rstrip('/').endswith('/404') else 'failed')
 except Exception as e:row.update(status='unavailable',error=type(e).__name__+': '+str(e))
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: rows=list(ex.map(check,sorted(urls)))
result={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Public HTTP reachability only; no tenant or product behavior tested','links':rows,'summary':{s:sum(x['status']==s for x in rows) for s in ['passed','failed','unavailable']}}
(ROOT/'checks/links.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result['summary']))
