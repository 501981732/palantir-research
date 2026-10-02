#!/usr/bin/env python3
"""Assemble attributable source records and every used citation; no network."""
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
from datetime import datetime,timezone
import json,re
ROOT=Path(__file__).resolve().parents[1]
def canon(url):
    p=urlsplit(url);return urlunsplit((p.scheme,p.netloc,p.path.rstrip('/'),p.query,''))
def arr(x):return x if isinstance(x,list) else [x] if x else []
def category(url):
    if 'community.palantir.com' in url:return 'community_original_thread'
    if 'github.com' in url:return 'source_or_original_pr'
    if 'youtube.com' in url:return 'public_video'
    if 'linkedin.com' in url:return 'public_social_post'
    if 'palantir.com/docs' in url:return 'official_documentation_or_announcement'
    return 'public_author_blog_or_site'
records={}
for path in sorted((ROOT/'notes').glob('*sources.json')):
    data=json.loads(path.read_text());data=data.get('sources',[]) if isinstance(data,dict) else data
    for r in data:
        if not isinstance(r,dict) or not r.get('url'):continue
        url=canon(r['url']);row=records.setdefault(url,{'url':url,'title':r.get('title',r.get('name',url)),'type':r.get('source_type',r.get('type',category(url))),'retrieved_dates':[],'supports':[],'limitations':[],'original_records':[],'used_in':[],'exact_citations':[]})
        row['retrieved_dates']+=arr(r.get('retrieved_date_utc',r.get('retrieved_date',r.get('retrieved','2026-10-01'))))
        row['supports']+=arr(r.get('supports',r.get('claims')));row['limitations']+=arr(r.get('limitations'))
        row['original_records'].append({'file':'notes/'+path.name,'source_id':r.get('id')})
        for k in ['author','publication_date','author_relationship','verification','resolution_status','current_version_verified']:
            if k in r:row[k]=r[k]
media=json.loads((ROOT/'notes/media-manifest.json').read_text())['assets']
originals={canon(r['original_url']) for r in media}
for p in sorted(ROOT.rglob('*.md')):
    if p.name=='sources.md':continue
    for label,url in re.findall(r'\[([^\]]*)\]\((https?://[^)\s]+)\)',p.read_text()):
        key=canon(url)
        if key in originals and not any(key==canon(r['source_page']) for r in media):continue
        row=records.setdefault(key,{'url':key,'title':label or key,'type':category(key),'retrieved_dates':[],'supports':[],'limitations':['未单独构成能力实测；具体支持与使用边界见正文及原始来源记录'],'original_records':[],'used_in':[],'exact_citations':[]})
        row['used_in'].append(p.relative_to(ROOT).as_posix());row['exact_citations'].append(url)
        if not row['retrieved_dates']:row['retrieved_dates']=['2026-10-01']
rows=[]
for i,key in enumerate(sorted(records),1):
    row=records[key];row['id']=f'S{i:03}'
    for k in ['retrieved_dates','supports','limitations','used_in','exact_citations']:row[k]=sorted(set(str(x) for x in row[k]))
    rows.append(row)
(ROOT/'notes/source-registry.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
lines=['# 来源登记与使用边界','', '主张优先由官方文档、固定源码和原始PR支持；博客/公开视频/社区社媒用于原作者实践、历史变化和验证线索。访问日期是本轮检索时间，不能替代发布时间或证明当前租户能力。逐条作者、关系、解决状态与局限保存在JSON和公开实践附录。','', '[机器来源登记](notes/source-registry.json) · [核心来源](notes/core-sources.json) · [集成来源](notes/integration-sources.json) · [治理来源](notes/governance-sources.json) · [公开实践来源](notes/practice-sources.json) · [原始媒体来源](assets.md)','', '| ID | 来源 | 类型 | 检索 UTC | 支持/局限 |','| --- | --- | --- | --- | --- |']
for r in rows:
    support='；'.join(r['supports']) or '对应正文/附录引文与媒体出处'
    limits='；'.join(r['limitations']) or '不构成当前租户实测'
    safe=lambda s:s.replace('|','\\|').replace('\n',' ')
    lines.append(f"| {r['id']} | [{safe(r['title'])}]({r['url']}) | {r['type']} | {', '.join(r['retrieved_dates'])} | {safe(support)}。边界：{safe(limits)} |")
lines+=['','## 公开HTTP与检索限制','', '最终公开HTTP结果见 [checks/links.json](checks/links.json)；HTTP200只证明该请求可访问，不能证明文章已完整核验、视频已完整观看或租户权限有效。图片原文件HTTP状态另见 [媒体台账](notes/media-manifest.json)。失败与未核验条件保留，不改凭据、不绕登录/DRM/访问限制。','', '精确源码行号由接入附录的本地固定源码核查支撑；所有原始URL与fragment保存在source registry的exact_citations，不以去掉fragment的HTTP检查替代行号验证。']
(ROOT/'sources.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'sources':len(rows),'exact_used_citations':sum(len(r['exact_citations']) for r in rows)}))
