# Palantir Research

一个以可复核的一手资料为主的 Palantir 产品与工程研究库。研究按专题存放，每个专题都应明确结论、证据边界、来源和本地保存的媒体资产。

## 已收录

| 专题 | 状态 | 核心内容 |
| --- | --- | --- |
| [SuperRepo（2026-08）](research/superrepo-2026-08/) | 已完成 | Foundry 的 Ontology-first、pro-code 全栈单体仓库能力，当前 Beta 边界与工程启示 |

## 目录约定

```text
research/
  <topic>-<yyyy-mm>/
    README.md       # 研究正文与结论
    assets/         # 研究直接引用、已获准本地保存的图片
    sources.md      # 逐条可访问来源及访问日期
    assets.md       # 图片来源、许可提示、大小、SHA-256
  _templates/       # 新专题起点
```

## 使用原则

- 结论优先引用原始公告、产品文档和源码；二手材料只用于补充线索。
- 写明“已确认”“推断”“未知”的边界；不要把 Beta 文档当作长期承诺。
- 不镜像整篇第三方文章。保存图片时保留原 URL、获取日期与校验值。
- 更新已有专题时保留历史判断，在正文中以“更新”说明发生了什么变化。

详细协作约定见 [AGENTS.md](AGENTS.md)。
