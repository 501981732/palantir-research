#!/usr/bin/env python3
"""Validate research integrity; does not test tenant/product behavior."""
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,unquote
from datetime import datetime,timezone
import hashlib,json,re,subprocess,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
BASE='6f2ef0eefdc5e0f2c0604eff75ed4095f582ace2'
checks=[]
def add(name,ok,**detail):checks.append({'check':name,'status':'passed' if ok else 'failed',**detail})
def rel(p):return p.relative_to(REPO).as_posix()
def canonical(u):
 s=urlsplit(u);return urlunsplit((s.scheme,s.netloc,s.path.rstrip('/'),s.query,''))
def slug(s):
 s=re.sub(r'[`*_]','',s).lower();s=re.sub(r'[^\w\-\s]','',s);return s.replace(' ','-')
required=['README.md','sources.md','assets.md','checks.md','notes/module-navigation-evidence.md','notes/public-practice.md','notes/public-practice-sources.json','notes/media-insight-evidence.md','notes/media-manifest.json','notes/media-checks.json','notes/source-registry.json','diagrams/manifest.json','checks/links.json']
for f in required:add('required deliverable', (ROOT/f).is_file(),file=f)
registry=json.loads((ROOT/'notes/source-registry.json').read_text());source_urls={canonical(r['url']) for r in registry}
media=json.loads((ROOT/'notes/media-manifest.json').read_text())['assets'];diagrams=json.loads((ROOT/'diagrams/manifest.json').read_text())
asset_urls={canonical(r['original_url']) for r in media}
for p in sorted(ROOT.rglob('*')):
 if not p.is_file() or p.suffix not in {'.md','.json','.py','.dot','.svg'}:continue
 text=p.read_text();bad=[]
 for pattern in [r'/(?:Users|home)/[A-Za-z0-9._-]+/',r'https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+)',r'\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}',r'\bBearer\s+[A-Za-z0-9._~-]{20,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']:
  if re.search(pattern,text):bad.append(pattern)
 add('privacy and secret patterns',not bad,file=rel(p),findings=bad)
 if p.suffix!='.md':continue
 add('balanced Markdown code fences',sum(1 for l in text.splitlines() if l.startswith('```'))%2==0,file=rel(p))
 missing=[];outside=[];not_registered=[];badanchors=[]
 for label,url in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',text):
  if url.startswith(('https://','http://')):
   if canonical(url) not in source_urls|asset_urls:not_registered.append(url)
   continue
  if url.startswith('#'):continue
  path,_,anchor=url.partition('#');target=(p.parent/unquote(path)).resolve()
  try:target.relative_to(REPO)
  except ValueError:outside.append(path);continue
  if not target.exists():missing.append(path);continue
  if anchor and target.suffix=='.md':
   heads={slug(l.lstrip('#').strip()) for l in target.read_text().splitlines() if l.startswith('#')}
   if unquote(anchor) not in heads:badanchors.append(url)
 add('local links exist',not missing and not outside,file=rel(p),missing=missing,outside_repository=outside)
 add('local heading anchors',not badanchors,file=rel(p),invalid=badanchors)
 add('public sources registered',not not_registered,file=rel(p),unregistered=sorted(set(not_registered)))
for r in media+diagrams:
 p=ROOT/r.get('path',r.get('file'));b=p.read_bytes();add('asset bytes and SHA256',len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],file=rel(p))
 if p.suffix=='.png':
  with Image.open(p) as im:
   im.load();expected=(r['width'],r['height']) if 'width'in r else tuple(r['dimensions']);add('PNG decodes and dimensions',im.size==expected,file=rel(p),dimensions=list(im.size))
for stem in ['01-workspace-model','02-context-navigation','03-release-boundaries']:
 add('rendered diagram with editable source',all((ROOT/'diagrams'/f'{stem}.{ext}').is_file() for ext in ['dot','svg','png']),diagram=stem)
for r in media:add('individual image inspection recorded',r.get('visual_inspection',{}).get('status')=='passed',asset=r['id'])
add('exact media files inventoried',{p.relative_to(ROOT).as_posix() for p in (ROOT/'assets').glob('*')}=={r['path'] for r in media})
for name in ['README.md','research/README.md']:
 old=subprocess.check_output(['git','show',BASE+':'+name],cwd=REPO,text=True);now=(REPO/name).read_text();oldtopics=set(re.findall(r'\]\(([^)]+2026-\d{2}/)\)',old));add('all previous topic index links retained',oldtopics.issubset(set(re.findall(r'\]\(([^)]+2026-\d{2}/)\)',now))),file=name,baseline_topics=sorted(oldtopics))
result={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'scope':'Deliverable integrity only; no tenant/product/runtime tests','baseline_commit':BASE,'checks':checks,'summary':{'checks':len(checks),'passed':sum(c['status']=='passed' for c in checks),'failed':sum(c['status']=='failed' for c in checks)}}
(ROOT/'checks/results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result['summary']));print(json.dumps([c for c in checks if c['status']=='failed'],ensure_ascii=False));sys.exit(bool(result['summary']['failed']))
