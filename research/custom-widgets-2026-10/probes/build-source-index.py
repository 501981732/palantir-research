#!/usr/bin/env python3
"""Generate a direct-source catalogue from the authored note, not vendor bodies."""
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urldefrag, urlsplit, unquote

topic = Path(__file__).resolve().parents[1]
sources = defaultdict(set)
for p in topic.glob("*.md"):
    if p.name in {"sources.md", "assets.md", "assets-media.md", "checks.md"}:
        continue
    t = p.read_text()
    for url in re.findall(r"https?://[^\s<>\)\]`\"|]+", t):
        base = urldefrag(url.rstrip('.,；。'))[0]
        if "/docs/resources/" not in base:
            sources[base].add(p.name)

def classify(url):
    u = urlsplit(url)
    if "palantir.com" == u.hostname or "www.palantir.com" == u.hostname:
        return "D 官方产品文档"
    if u.hostname == "github.com":
        if "/pull/" in u.path:
            return "P 作者 PR 与评审"
        return "G 公开源码与工作流"
    if u.hostname in {"registry.npmjs.org", "www.npmjs.com", "npmjs.com"}:
        return "N npm 发布物与 provenance"
    if u.hostname == "community.palantir.com":
        return "C 具名作者实践"
    if u.hostname in {"www.youtube.com", "youtube.com", "youtu.be"}:
        return "V 公开视频"
    return "O 其他一手技术资料"

def label(url):
    u = urlsplit(url)
    p = unquote(u.path)
    if "/blob/" in p:
        return p.split("/blob/", 1)[1].split("/", 1)[-1]
    if "/pull/" in p:
        return p.split("/pull/")[0].lstrip("/") + " PR #" + p.split("/pull/")[1]
    if "/docs/foundry/" in p:
        return p.split("/docs/foundry/")[1].strip("/")
    return (u.hostname or "") + p + ("?" + u.query if u.query else "")

out = ["# 来源清单与证据层级", "", "核验日期：2026-10-01。此目录列专题实际引用的直接 URL；正文与附录保留更细的固定行号。目录不是全文镜像，也不是仅凭 HTTP 200 判定功能有效。", "", "- **产品事实**以当日官方文档为准；历史公告保留日期，不能替代当前功能。", "- **实现事实**以 widget npm 3.74.0 的发布 provenance 提交 `fb8ec172d540ef7819382ff036aa2a692614af75` 为主，并逐文件比对实际 source map；CLI/config/UI 各按附录的独立版本与提交锁定，main `e53b94…` 仅作比较。", "- **版本事实**来自官方 npm registry / tarball / provenance；本轮匹配摘要与提交，未执行独立签名信任链验证。", "- **作者 PR**核对 state、draft、merged_at；未合并项不作为已发布能力。", "- **社区/视频**只支持该作者在该版本/时间点的操作观察，不泛化为全部产品保证。", "- **本地实测**见 checks.md；mock bridge、JSDOM、官方 no-OSDK 模板均与真实租户验收分开。", "- EOS 部分为建议；没有检查 EOS 源码。", "", "媒体原始资源 URL、发布时间/时间点、逐图字节与 hash 见 [assets.md](assets.md)；来源 URL 的公开 HEAD 检查见 [http-checks.json](evidence/http-checks.json)，拒绝与超时保留，不绕过。", ""]
groups = defaultdict(list)
for url in sources:
    groups[classify(url)].append(url)
for group in sorted(groups):
    out.extend([f"## {group}", "", "| ID | 来源 / 直接入口 | 支撑位置 | 访问日期 |", "| --- | --- | --- | --- |"])
    for n, url in enumerate(sorted(groups[group]), 1):
        name = label(url).replace("|", "\\|")
        article = "、".join(f"[{f}]({f})" for f in sorted(sources[url]))
        out.append(f"| {group[0]}{n:02d} | [{name}]({url}) | {article} | 2026-10-01 |")
    out.append("")
out.extend(["## 可复现来源记录", "", "| 记录 | 内容与边界 |", "| --- | --- |", "| [protocol-sources.json](evidence/protocol-sources.json) | 发布源固定行号、源文件 hash 和实际 npm 对应关系 |", "| [protocol-npm-audit.json](evidence/protocol-npm-audit.json) | API/client 发布时间、tarball hash/SRI、文件清单 |", "| [react-release.json](evidence/react-release.json)、[React 来源台账](evidence/react-sources.md) | React adapter 发布与七个 runtime source map 对应 |", "| [react-components-release.json](evidence/react-components-release.json) | UI 库 0.61.0 的独立发布与 ObjectTable API 源匹配 |", "| [build-package-versions.json](evidence/build-package-versions.json)、[source-map audit](evidence/build-source-map-audit.json) | plugin/create/CLI/config 版本与来源；中间 JS 与原 TS 不作字节等同 |", "| [lineage-pr-state.json](evidence/lineage-pr-state.json) | 已合并与 open/draft 的精确状态/时间 |", "| [lineage-documentary-sources.json](evidence/lineage-documentary-sources.json) | 当前文档与作者案例的提炼结论 |", "| [media-evidence.md](media-evidence.md) | 正常浏览器播放/字幕尝试、真实帧和未取得证据 |", ""])
(topic / "sources.md").write_text("\n".join(out))
print({"source_urls": len(sources), "groups": {g: len(v) for g, v in groups.items()}})
