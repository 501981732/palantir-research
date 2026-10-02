# 媒体与自绘图资产台账

记录与核验日期：2026-10-01（UTC）。本台账覆盖六张真实媒体图、三组自绘概念图的九个 DOT/SVG/PNG 文件，以及可重现渲染脚本。抓取/绘制/核验只有日期记录，**没有编造精确 UTC 时刻**。尺寸、字节数和 SHA-256 均来自仓库内实际文件；所有 PNG/JPEG 通过 Pillow 解码/完整性检查，图文件元数据重新计算并与 [diagrams/manifest.json](diagrams/manifest.json) 比对一致。

官方文档原 PNG 与实际公开视频局部帧分别记录；视频帧是正常播放后取得的播放器区域截图，包含原视频标题和频道，**不是下载的缩略图**。它们证明所示画面和历史界面，不是本研究在 Foundry 租户的运行记录。完整观看、效果复现及媒体访问边界见 [案例附录](appendices/cases.md) 和 [checks.md](checks.md)。

## 1. 官方文档与实际视频帧：来源及内容范围

| 本地文件 | 来源页 | 直接原图 URL / 视频时间定位 | 抓取日期（UTC） | 内容范围及边界 |
| --- | --- | --- | --- | --- |
| [01-review.png](assets/01-review.png) | [AIP Evolve overview](https://www.palantir.com/docs/foundry/aip-evolve/overview) | [官方原 PNG：workflow-1](https://www.palantir.com/docs/resources/foundry/aip-evolve/aip-evolve-workflow-1.png) | 2026-10-01 | Review 阶段：AIP Logic、Optimize cost、10 test cases、side-by-side、Best effort、model/prompt、最多五轮，以及发送 AI FDE 的生成指令。下方指令把并排输出判断与 suite 自动 comparison evaluator 分开。是官方实例配置，不能当产品统一默认值或租户亲测。 |
| [02-agent-graph.png](assets/02-agent-graph.png) | [AIP Evolve overview](https://www.palantir.com/docs/foundry/aip-evolve/overview) | [官方原 PNG：workflow-2](https://www.palantir.com/docs/resources/foundry/aip-evolve/aip-evolve-workflow-2.png) | 2026-10-01 | 库存分配迁移的实例活动图，三轮 Orchestrator 及分析、测试生成、分支/model swap、baseline/candidate eval、prompt、proposal/report 活动。图标题与 Review 的 cost goal 不完全同文，不能补成一致运行快照；不猜徽标 tooltip 语义或固定 Agent DAG。 |
| [03-proposal.png](assets/03-proposal.png) | [AIP Evolve overview](https://www.palantir.com/docs/foundry/aip-evolve/overview) | [官方原 PNG：workflow-3](https://www.palantir.com/docs/resources/foundry/aip-evolve/aip-evolve-workflow-3.png) | 2026-10-01 | GPT-4o→GPT-5.4 Mini、两个 substitution prompt guardrails、10 cases pass、204.6→72.4 compute-seconds/call、约65%计算成本改善，以及 Awaiting review、Review in Branching、Resume with Feedback。Safe to proceed/High 是提案标签，不是统计置信区间、审批完成或生产发布。 |
| [04-devcon-agent-graph-13m12s.jpg](assets/04-devcon-agent-graph-13m12s.jpg) | [DevCon 6：Agent Observability & Optimization](https://www.youtube.com/watch?v=GZHSCMz6Aio) | [实际局部片段：13:12](https://www.youtube.com/watch?v=GZHSCMz6Aio&t=792s) | 2026-10-01 | 正常播放至13:12附近的播放器区域，保留标题与 Palantir/Palantir Developers 联合频道。Reduce latency / `apw-create-delivery-from-rfq`（AIP Logic），五轮 Orchestrator 与 Heuristic Extraction 节点。只观察7:41–7:48、12:02–12:11、13:00–13:12附近片段；不证明完整搜索轨迹、固定 fleet 或跨会话学习。 |
| [05-devcon-constraints-12m11s.jpg](assets/05-devcon-constraints-12m11s.jpg) | [DevCon 6：Agent Observability & Optimization](https://www.youtube.com/watch?v=GZHSCMz6Aio) | [实际局部片段：12:11](https://www.youtube.com/watch?v=GZHSCMz6Aio&t=731s) | 2026-10-01 | 正常播放至12:11附近：Optimize latency、30 cases、side-by-side/Best effort、Model swapping、Prompt tweaks、Architectural changes、Tool/function-call changes、五轮及生成指令。保留标题/频道。历史约束配置，不是当前完整支持矩阵或美元/token硬预算。 |
| [06-tgh-workflow-07m17s.jpg](assets/06-tgh-workflow-07m17s.jpg) | [DevCon 6：AIP Evolve × Tampa General Hospital](https://www.youtube.com/watch?v=WLleqr4GEAw) | [实际局部片段：7:17](https://www.youtube.com/watch?v=WLleqr4GEAw&t=437s) | 2026-10-01 | 正常播放至7:17附近：AI FDE 的 UR Reviews Cost Optimization 流程图、Inpatient/Observation 两支、Write Chart Review / Claude 4.6 Sonnet、guideline loop 和 Chat outline。保留视频标题/联合频道，未见患者原始记录内容。只观察0:00–0:11、7:07–7:17附近片段，不是医院全片观看，也没有验证84%替代段。官方视频页扩展说明显示上传日期2026-07-14。 |

文档原图公开文件未标注独立拍摄/制作时刻，抓取日期不等于截图所示运行日期。视频的时间定位是内容位置，不是抓取 UTC 时刻；不为实际截图编造单独 CDN/JPEG 下载 URL。

## 2. 六张媒体图的实际文件元数据与视觉 QA

| 本地文件 | 格式 / 色彩模式 | 尺寸（px） | bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| [01-review.png](assets/01-review.png) | PNG / RGB | 1440 × 900 | 138497 | `1e52423b4c7e5c21bb1bf81ed551748bf207d6f0b31eb04ccb978c58be5ad42f` |
| [02-agent-graph.png](assets/02-agent-graph.png) | PNG / RGB | 1440 × 900 | 178243 | `27554622366859f630e5ceeb393f8e0dd49c629c1bd12fb4637b921b8bf17a80` |
| [03-proposal.png](assets/03-proposal.png) | PNG / RGB | 1440 × 900 | 126396 | `04c7ccf7826e6b67539b0b255b5ed26574e7e035aa7edac5c9999db2cce26e63` |
| [04-devcon-agent-graph-13m12s.jpg](assets/04-devcon-agent-graph-13m12s.jpg) | JPEG / RGB | 880 × 587 | 44364 | `4ee5252c463ae6bcece9e501eedb83e7efc4057107465233fb0fad43ca9e76b1` |
| [05-devcon-constraints-12m11s.jpg](assets/05-devcon-constraints-12m11s.jpg) | JPEG / RGB | 880 × 587 | 57436 | `a481abd06bb04c7d1903203a6c3bda457fe99fb2afb845106a26c50ae696e737` |
| [06-tgh-workflow-07m17s.jpg](assets/06-tgh-workflow-07m17s.jpg) | JPEG / RGB | 880 × 587 | 73734 | `053591a36d9abe8772a54d4f3a80f32014c71cab9109d871e2d993485e1631e8` |

六张均已逐图检查实际像素，未用文件名、页面摘要或缩略图代替视检。以下记录既说明可读内容，也保留小字和画面范围的限制。

| 文件 | 视觉检查结果 |
| --- | --- |
| 01-review.png | 标题、四阶段、目标/验证/约束与生成指令可读；底部是官方原图的画面终止，未补绘被截断的页面区域。所述10例、两类变更、五轮可核。 |
| 02-agent-graph.png | 三轮标题、角色节点和连线可辨；小徽标未打开 tooltip，部分节点长名称本就省略。只使用能辨认的角色/迭代结构，未扩写被省略内容或精确徽标含义。 |
| 03-proposal.png | 状态、模型名称、计算成本/单位、两处 guardrails 与 Review/Resume 入口可读；保留原图的“10 pass rate”显示，以正文 All 10 cases pass 解释，不把模糊卡片另定为100%总体准确率。 |
| 04-devcon-agent-graph-13m12s.jpg | 顶部目标、五个迭代节点及 Heuristic Extraction 可辨；下方标题/频道清楚。活动小字与省略名称受视频分辨率限制，不据图转录完整阶段指令、运行日志或隐藏工件。 |
| 05-devcon-constraints-12m11s.jpg | latency目标、30cases、评分/差异策略、四类 allowed changes 和五轮可辨；生成指令部分在文本框可见，其余不补写。标题和频道清楚，演讲者画中画保留。 |
| 06-tgh-workflow-07m17s.jpg | 两支及 guideline loop 的布局、函数/模型标签与 Chat outline 可辨；小字和折叠/截断内容不转写为完整日志。画面是结构/工具观察，没有可见病例正文；不证明演示数据的全部匿名化程度。 |

## 3. 自绘概念图：来源、边界与渲染 QA

绘制/渲染日期：2026-10-01（UTC；无精确时刻记录）。三组均为本研究依据公开资料原创归纳，**不是 Palantir 官方图、闭源服务架构、固定 Agent DAG 或实际 Foundry 运行结果**。没有上游图片直接 URL；公开资料链接是支持归纳的来源页，不是图的原图地址。保留可编辑 DOT、矢量 SVG、固定布局 PNG 与 [render.py](diagrams/render.py)。

| 概念图 | 公开支撑来源页 | 本地直接图源/渲染结果 | 内容范围与逐图视觉 QA |
| --- | --- | --- | --- |
| 01：目标、验证与人工审阅 | [Evolve overview](https://www.palantir.com/docs/foundry/aip-evolve/overview)、[AI FDE security](https://www.palantir.com/docs/foundry/ai-fde/security-and-governance)、[Global Branching](https://www.palantir.com/docs/foundry/global-branching/core-concepts) | [DOT](diagrams/01-evolve-conceptual-architecture.dot) / [SVG](diagrams/01-evolve-conceptual-architecture.svg) / [PNG](diagrams/01-evolve-conceptual-architecture.png) | 分开用户输入、优化入口、AI FDE活动、目标/验证工件、审阅和交付；审阅→发布用虚线，需另核交付链。实际PNG中文/箭头清楚，三层布局完整；跨组箭头停于分组边界，未见文字裁切、重叠或缺字。 |
| 02：基线、候选与验证闭环 | [Evolve overview](https://www.palantir.com/docs/foundry/aip-evolve/overview) | [DOT](diagrams/02-evolution-validation-flow.dot) / [SVG](diagrams/02-evolution-validation-flow.svg) / [PNG](diagrams/02-evolution-validation-flow.png) | 归纳示例迭代，10例/最多五轮/实际三轮均标为实例；搜索/停止规则未知，Resume不等于断点恢复。主流程从上至下，迭代/Resume回边为虚线，侧边约束说明完整；未见裁切、重叠或缺字。 |
| 03：两类图与状态边界 | [Evolve overview](https://www.palantir.com/docs/foundry/aip-evolve/overview)、[AI FDE security](https://www.palantir.com/docs/foundry/ai-fde/security-and-governance)、[Global Branching](https://www.palantir.com/docs/foundry/global-branching/core-concepts) | [DOT](diagrams/03-graphs-and-state-boundaries.dot) / [SVG](diagrams/03-graphs-and-state-boundaries.svg) / [PNG](diagrams/03-graphs-and-state-boundaries.png) | 区分资源依赖与agent活动，再区分定义合并、运行副作用和实际交付。概念依赖图不证明Evolve专用lineage页面；未绘固定DAG。上下分组清楚，中英文可读；未见文字裁切、重叠或缺字。 |

实际渲染使用 Graphviz 14.0.4、PingFang SC；脚本对九个图源/图文件记录字节与校验值。既有渲染记录确认所有 Graphviz 调用成功且无警告，三份PNG通过 `Image.verify()`，三份SVG通过XML解析与中文/概念声明检查；逐图像素检查见 [diagrams/qa.md](diagrams/qa.md)。本轮重新核算确认所有九个文件与现有 manifest 相符。未为台账重绘或修改图像。

## 4. 九个图文件逐文件元数据

下表日期均为2026-10-01（UTC）。DOT是UTF-8文本，尺寸不适用；SVG记录原生 `width`/`height` 的pt单位与viewBox，不误写成像素；PNG记录实际px尺寸。色彩模式仅适用于PNG。

| 文件 | 格式 / 尺寸或画布 | bytes | SHA-256 |
| --- | --- | ---: | --- |
| [01-evolve-conceptual-architecture.dot](diagrams/01-evolve-conceptual-architecture.dot) | DOT文本；尺寸不适用 | 2854 | `e7be81bd3071c68cc9ab7ec89dd91d514c7ba5c0d42124afb38eddfc89f0631b` |
| [01-evolve-conceptual-architecture.svg](diagrams/01-evolve-conceptual-architecture.svg) | SVG；2737 × 1585pt；viewBox `0 0 2737 1585` | 14148 | `c5f6d4e03d254510339be26704297c233a5757ae235d0c77a985c6e1de57a1e9` |
| [01-evolve-conceptual-architecture.png](diagrams/01-evolve-conceptual-architecture.png) | PNG / RGBA；2737 × 1585px | 439394 | `69ccaa1b3e6aed68047920eb5a5cf777fbdcc355b72d01138c326da28a6aab29` |
| [02-evolution-validation-flow.dot](diagrams/02-evolution-validation-flow.dot) | DOT文本；尺寸不适用 | 2323 | `a0fa205e6f769da9a01142e9881c6e1999dbdb4812d25e6fa719ee6b928c8dff` |
| [02-evolution-validation-flow.svg](diagrams/02-evolution-validation-flow.svg) | SVG；1900 × 2464pt；viewBox `0 0 1900 2464` | 12849 | `586b23e82ac390d6dfbd38f538559c83c4299cf5e013422c8aabc11c21cc694f` |
| [02-evolution-validation-flow.png](diagrams/02-evolution-validation-flow.png) | PNG / RGBA；1900 × 2464px | 417033 | `bc645a40ff72f32fa0381bbcd049225ba4d7fba2ec9aeab27123e400f3959b92` |
| [03-graphs-and-state-boundaries.dot](diagrams/03-graphs-and-state-boundaries.dot) | DOT文本；尺寸不适用 | 3529 | `bcdaba90318d9c10708bde0a340ad596029a416ed769f77aca75bb4785793dc2` |
| [03-graphs-and-state-boundaries.svg](diagrams/03-graphs-and-state-boundaries.svg) | SVG；2165 × 2027pt；viewBox `0 0 2165 2027` | 16029 | `7abee3c654e6e9f3c113587377553dcf60933fc379125d9bdb6d6fceeaf73d40` |
| [03-graphs-and-state-boundaries.png](diagrams/03-graphs-and-state-boundaries.png) | PNG / RGB；2165 × 2027px | 420783 | `f1c62da4db88f3f382f93a1c8a6dca4921e38deca537436ab48e558a2d3f6d21` |

## 5. 可重现渲染与核验记录

在 `diagrams/` 执行 `python3 render.py` 可从现有 DOT 重新生成 SVG/PNG及manifest；需要 Graphviz、Python、Pillow与可用中文字体。工具或字体变化可能改变排版、字节数和SHA，应重新视检并更新台账，不能期待渲染产物字节必然一致。

| 记录/工具 | 用途 | bytes | SHA-256（本次文件） |
| --- | --- | ---: | --- |
| [render.py](diagrams/render.py) | 原创渲染和清单生成脚本；文本源，尺寸不适用 | 2005 | `f837be630285df452b79ccff04e69904494077e0cd4d73a94f08f1f67a334f82` |
| [manifest.json](diagrams/manifest.json) | 九个DOT/SVG/PNG的元数据与渲染器/字体记录 | 1985 | `ed5d6068392684cc0019cdca9f151194680499b01f2c94e7ed9a86419d4a830c` |
| [qa.md](diagrams/qa.md) | 实际渲染与三图视觉QA记录 | 2795 | `ea8aad67d3cbb8320dc75403c85ada9ecb1ab86437b7870062a464857a3e9a3c` |

上游作者/频道与直接来源均保留，媒体本地保存用于可追溯的产品与机制研究。自绘图的解释边界见 [diagrams/README.md](diagrams/README.md)；没有将概念图包装成官方实现或将局部帧包装成完整观看。
