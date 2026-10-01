# Palantir Research

一个以可复核的一手资料为主的 Palantir 产品与工程研究库。研究按专题存放，每个专题都应明确结论、证据边界、来源和本地保存的媒体资产。

## 已收录

| 专题 | 状态 | 核心内容 |
| --- | --- | --- |
| [SuperRepo（2026-08）](research/superrepo-2026-08/) | 已完成 | Foundry 的 Ontology-first、pro-code 全栈单体仓库能力，当前 Beta 边界与工程启示 |
| [Pilot（2026-09）](research/pilot-2026-09/) | 研究报告，待用户评审 | AI 生成 Ontology、设计与 React/OSDK；独立应用及 Workshop widget 交付，数据/权限边界与 EOS 验证计划 |
| [OSDK React Components（2026-09）](research/osdk-react-components-2026-09/) | 研究报告，待用户评审 | 实际 npm 组件/API 图鉴、真实界面、Workshop 来源边界、AI 生成与 EOS 复用路线 |
| [OSDK TypeScript（2026-09）](research/osdk-typescript-2026-09/) | 研究报告，待用户评审 | Ontology codegen、typed client、observable 缓存、React 订阅、发布与许可证边界 |
| [AI FDE（2026-10）](research/ai-fde-2026-10/) | 深入研究，待用户评审 | Foundry 工程 Agent 的 Modes、上下文、工具与验证闭环；分支/审批/数据副作用边界、公开实践与 EOS 分期验证 |
| [Custom Widgets / Widget Registry（2026-10）](research/custom-widgets-2026-10/) | 详尽研究报告 | 宿主协议、ObjectSet/React adapter、实际发布包与构建链、版本兼容、真实界面/视频证据及 EOS 实施建议 |
| [Workshop Runtime（2026-10）](research/workshop-runtime-2026-10/) | 深入研究，待用户评审 | React/Pilot→OSDK→Widget Set/Registry→宿主变量与事件→Ontology读写→页面与版本；EOS当前实现、语义差异与验证范围 |
| [Object Views / Object Explorer / Workshop（2026-10）](research/object-views-2026-10/) | 深入研究，待用户评审 | 对象中心入口、Standard/Configured/Legacy沿革、Full/Panel与对象上下文、探索到操作、配置版本与发布治理，以及EOS架构取舍 |
| [Carbon（2026-10）](research/carbon-2026-10/) | 深入研究，待用户评审 | 角色工作台、首页与tab实例、模块发现/对象导航、权限与发布边界、Insight入口演进及EOS验证建议 |

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
