#!/usr/bin/env python3
"""Research deliverable integrity, not tenant behavior or CI."""
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,unquote
from datetime import datetime,timezone
import hashlib,json,re,subprocess,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
BASE='e64916da0d781652d5a337ce77f05a579ff49ef8'
checks=[]
def add(name,ok,**details):
    checks.append({'check':name,'status':'passed' if ok else 'failed',**details})
def canonical(url):
    s=urlsplit(url);return urlunsplit((s.scheme,s.netloc,s.path.rstrip('/'),s.query,''))
def slug(s):
    s=re.sub(r'[`*_]','',s).lower();s=re.sub(r'[^\w\-\s]','',s);return s.replace(' ','-')
required=['README.md','build-context-tools.md','application-integration.md','governance-and-lifecycle.md','public-practice.md','eos-architecture.md','media-evidence.md','sources.md','assets.md','checks.md','notes/source-registry.json','notes/media-manifest.json','diagrams/manifest.json','checks/links.json']
for f in required:add('required deliverable',(ROOT/f).is_file(),file=f)
registry=json.loads((ROOT/'notes/source-registry.json').read_text())
registered={canonical(r['url']) for r in registry}
media=json.loads((ROOT/'notes/media-manifest.json').read_text())['assets']
diagrams=json.loads((ROOT/'diagrams/manifest.json').read_text())
asset_urls={canonical(r['original_url']) for r in media}
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p.suffix not in {'.md','.json','.dot','.svg'}:continue
    s=p.read_text();findings=[]
    for pattern in [r'/(?:Users|home)/[A-Za-z0-9._-]+/',r'https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+)',r'\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}',r'\bBearer\s+[A-Za-z0-9._~-]{20,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']:
        if re.search(pattern,s):findings.append(pattern)
    add('privacy and credential patterns',not findings,file=str(p.relative_to(ROOT)),findings=findings)
    if p.suffix!='.md':continue
    add('balanced code fences',sum(l.startswith('```') for l in s.splitlines())%2==0,file=p.relative_to(ROOT).as_posix())
    missing=[];outside=[];anchors=[];unregistered=[]
    for label,url in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',s):
        if url.startswith(('http://','https://')):
            if canonical(url) not in registered|asset_urls:unregistered.append(url)
            continue
        path,_,anchor=url.partition('#')
        target=p if not path else (p.parent/unquote(path)).resolve()
        try:target.relative_to(REPO)
        except ValueError:outside.append(url);continue
        if not target.exists():missing.append(url);continue
        if anchor and target.suffix=='.md':
            heads={slug(l.lstrip('#').strip()) for l in target.read_text().splitlines() if l.startswith('#')}
            if unquote(anchor) not in heads:anchors.append(url)
    add('local links exist',not missing and not outside,file=p.relative_to(ROOT).as_posix(),missing=missing,outside=outside)
    add('local heading anchors',not anchors,file=p.relative_to(ROOT).as_posix(),invalid=anchors)
    add('sources registered',not unregistered,file=p.relative_to(ROOT).as_posix(),unregistered=sorted(set(unregistered)))
for r in media+diagrams:
    p=ROOT/r['path'];b=p.read_bytes()
    add('asset hash and bytes',len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],file=r['path'])
    if p.suffix.lower() in {'.png','.jpg','.jpeg','.gif'}:
        with Image.open(p) as im:im.load();dims=[im.width,im.height]
        add('media decodes and dimensions',dims==[r['width'],r['height']],file=r['path'],dimensions=dims)
    inspected=r.get('visual_inspection')
    add('visual inspection recorded',bool(inspected),file=r['path'])
add('exact media file inventory',{p.relative_to(ROOT).as_posix() for p in (ROOT/'assets').iterdir() if p.is_file()}=={r['path'] for r in media})
allmd='\n'.join(p.read_text() for p in ROOT.rglob('*.md'))
for r in media:add('every media used',Path(r['path']).name in allmd,file=r['path'])
for src in sorted((ROOT/'diagrams').glob('*.dot')):add('editable rendered diagram',all(src.with_suffix('.'+e).is_file() for e in ['png','svg']),source=src.name)
for name in ['README.md','research/README.md']:
    old=subprocess.check_output(['git','show',BASE+':'+name],cwd=REPO,text=True);new=(REPO/name).read_text()
    add('original index content retained',all(line in new.splitlines() for line in old.splitlines()),file=name)
changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=REPO,text=True).splitlines()
unexpected=[p for p in changed if p not in ['README.md','research/README.md'] and not p.startswith('research/aip-chatbot-studio-2026-10/')]
add('old topics unchanged',not unexpected,unexpected=unexpected)
result={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'baseline_main':BASE,'scope':'Deliverable integrity only; no tenant, EOS runtime or CI execution','checks':checks,'summary':{'checks':len(checks),'passed':sum(c['status']=='passed' for c in checks),'failed':sum(c['status']=='failed' for c in checks)}}
(ROOT/'checks/results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result['summary']));print(json.dumps([c for c in checks if c['status']=='failed'],ensure_ascii=False));sys.exit(bool(result['summary']['failed']))
