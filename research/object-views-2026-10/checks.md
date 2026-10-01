# 核验范围与可复查结果

核验日：2026-10-01 UTC。资料基线为当日公开文档及带日期公告，仓库基线为 `main@70feed00b61f7572190b94741bfba9958a573486`。本篇仅增加对象中心入口主题，根索引保留已有专题，并补齐研究索引原来漏列的已合并 Workshop Runtime。

## 事实与版本

- 当前 Standard/Configured、Full/Panel、单对象/集合规则，分别与对应官方页面交叉核对；2024、2026-01、2026-02、2026-09的公告与当前能力分开标注。
- 不用“default”概括多个默认选择；Standard 与自动生成 default configured 的文档张力明确保留。
- Workshop toggle、嵌入模块变量更新范围的资料差异并列记录，未补出未公开的租户行为。
- 保存、发布、模块 autosave、审批继承与资源保护逐项区分；预览不是发布的必经步骤。
- State saving 区分显式保存与默认已保存状态自动加载；原生组件未填完表单是支持用例，任意字段和Action事务草稿未据此推出。
- Project-based Ontology权限保留新建、启用、迁移与Default Ontologies限制；可发现、资源访问、数据访问、Action提交各自论证。
- Carbon 2026-09-21更新按既有workspace opt-in与未来默认计划表述，未把历史Object Explorer入口写成唯一当前入口。

## 媒体与公开源码

13个媒体文件包括11个官方原图或GIF与2个解码静帧；原始URL、来源页、UTC、字节、尺寸、hash与派生方式见 [assets](assets.md)、[media manifest](notes/media-manifest.json)。[媒体检查记录](notes/media-checks.json)保存解码和checksum结果。动图帧时间指原始GIF的帧起始时间，未增补UI。

3张概念图有Mermaid源、实际渲染SVG/PNG及[逐文件manifest](diagrams/manifest.json)，使用Mermaid CLI 11.12.0和中文字体；所有渲染图已实际查看，无裁切、遮挡或乱码。它们是依据公开产品契约自绘的关系图，不是Palantir服务拓扑、租户截图或内部实现。

官方公开OSDK教程两个文件固定到完整提交SHA后阅读；示例声明在内存mock数据上运行。本篇没有执行该应用，也不把组件交互当成真实Foundry Action写回或Object Views内部源码证据。

## 可复查的结构与链接检查

在仓库根目录运行：

```sh
python3 research/object-views-2026-10/checks/validate.py
```

[结构检查结果](checks/results.json)记录本地链接、Markdown围栏、所有资产的字节/hash/尺寸、三组图文件、安全文本扫描、来源登记覆盖和既有专题索引保留；脚本以退出码表示结果。它验证交付物完整性，不代替产品事实审阅。

[公开链接健康记录](checks/links.json)与[检查脚本](checks/check_links.py)记录普通HTTP请求的可达性。HTTP成功不意味着租户功能可用、播放器内容成功观看、评论者身份得到官方认证或所有源都同日更新。正文读取证据以[sources](sources.md)逐项范围为准；被拒绝、超时或页面读取失败保留，不绕过访问限制。

## 没有做的验证与剩余问题

未登录Foundry租户、提交Action、编辑/发布真实视图、执行临时对象集API、读取EOS内部源码或执行官方示例。YouTube读取了公开描述、日期与章节，播放器失败且字幕不可用；没有声称完整观看，也未从广告画面取内容帧。

尚不能从公开资料确定Standard/default configured的物化与迁移条件、managed module对象变量的内部注入协议、多个tab草稿是否原子发布、活动会话更新策略、所有widget设置的租户rollout范围，以及当前文档差异对应的准确版本。EOS章节把这些问题转成架构评估和验证建议，没有转为实施排期。
