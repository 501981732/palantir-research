# AIP Evolve 自绘概念图

绘制与资料核验日期：2026-10-01。三图均为作者依据公开资料自行归纳和绘制，**不是 Palantir 官方图片、内部实现架构或本研究的 Foundry 运行记录**。未复制、改绘官方截图。

| 图 | PNG | SVG | 可编辑源文件 |
| --- | --- | --- | --- |
| 1：目标、验证与人工审阅 | [PNG](01-evolve-conceptual-architecture.png) | [SVG](01-evolve-conceptual-architecture.svg) | [Graphviz DOT](01-evolve-conceptual-architecture.dot) |
| 2：基线、候选与验证闭环 | [PNG](02-evolution-validation-flow.png) | [SVG](02-evolution-validation-flow.svg) | [Graphviz DOT](02-evolution-validation-flow.dot) |
| 3：两种图、两类状态边界 | [PNG](03-graphs-and-state-boundaries.png) | [SVG](03-graphs-and-state-boundaries.svg) | [Graphviz DOT](03-graphs-and-state-boundaries.dot) |

图 1 将用户输入、Evolve 协调、AI FDE 活动、目标及验证工件、提案审阅和交付步骤分开。图中虚线连接人工审阅与发布，表示资源发布流程需要另行核验；它不表示 Evolve 承诺直接完成所有资源的部署。

图 2 只归纳官方示例展示的验证闭环。10 个用例、最多 5 轮和实际 3 轮属于该示例；候选选择、调度与停止策略未知。Resume 对继续 evolution 的支持，不等同于已验证的断点恢复、幂等执行或自动重试保证。

图 3 上半部分区分“被优化系统的资源依赖”和“进行优化的 agent 活动”。Workflow lineage 部分是概念依赖图，不能解释为 Evolve 拥有已公开的同名专用页面；Agent graph 部分只列示活动和可观察工件，未规定固定 agent DAG。下半部分结合 AI FDE 和 Global Branching 文档，分别提示定义合并、运行副作用与实际发布的验证责任。

证据来源（均访问于 2026-10-01）：

- [AIP Evolve overview](https://www.palantir.com/docs/foundry/aip-evolve/overview)：目标、goal、validation、limits；AI FDE fleet；示例迭代、模型与 prompt 变更；Proposal、Review in Branching 与 Resume。
- [AI FDE security and governance](https://www.palantir.com/docs/foundry/ai-fde/security-and-governance)：用户身份与权限、按工具及分支区分的操作审批、发布与 Action 的审批类别。这些是 AI FDE 支撑能力的边界。
- [Global Branching core concepts](https://www.palantir.com/docs/foundry/global-branching/core-concepts)：资源检查、审批、合并与构建选项，资源创建/删除及部分合并失败的限制。这些是分支层能力的边界。

重新渲染：在本目录执行 `python3 render.py`。需要 Graphviz `dot`、Python 和 Pillow；本轮使用 Graphviz 14.0.4 与 PingFang SC 中文字体。更换渲染器或字体可能改变布局与校验值。正文推荐嵌入 PNG，以固定本次中文排版；SVG 保留矢量缩放与文字结构。

文件元数据与 SHA-256 见 [manifest.json](manifest.json)，逐图视觉检查见 [qa.md](qa.md)。
