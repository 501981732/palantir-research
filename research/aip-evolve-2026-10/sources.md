# 来源台账与实际取得范围

> 全部来源访问/核验日期：**2026-10-01（UTC）**。共 **71个独立来源**：46份官方文档/公告、3份官方原始PNG、4个社区页面/JSON、5篇LinkedIn原帖、4个YouTube视频、2个X原帖、4篇二级材料及3份既有仓库研究。带时间戳的视频URL与公告锚点是定位入口，不另算独立实验或来源。

本台账对应[主文](README.md)、[机制附录](appendices/mechanisms.md)、[案例附录](appendices/cases.md)及[概念图说明](diagrams/README.md)的外部引用，并补列已核读的关联合同和三个原PNG。滚动文档的日期栏表示没有核到单独发布/修订日；它们只能代表访问时的公开正文，不能回填早期版本行为。社区/社交页面的时间按实际页面或索引显示记录，未自行换算为会议日或首发日。

## 证据层级与读取方法

| 标记 | 含义 | 本研究允许的使用范围 |
| --- | --- | --- |
| P1 | Evolve官方产品正文与发布公告 | 产品定义/当前流程或明确公告日期；不等于租户亲测。 |
| P2 | 关联平台的官方正文 | AI FDE/Evals/Logic/branch/MCP/Pilot/Workshop自身契约；组合路径须标分析，不改写为Evolve默认行为。 |
| O1 | 官方图片或原播放器中实际观察的局部画面 | 描述画面可见工件/配置；截图不证明整片已看或指标已复现。 |
| R1 | 官方原帖正文与公开短片可见Transcript | 归属清楚的演示叙述；自动转写可能误识别模型名，不视为已校订官方字幕。 |
| D1 | 开发者原帖/公开JSON | 作者在具体时间和环境中的反馈/回应；不当正式跨版本承诺或采用率。 |
| S1 | 二级解释或社交转述 | 追踪原始材料；没有独立实验时不作交叉测量。 |
| M1 | 搜索片段、页面说明或其他metadata | 日期/链接/下一步核验线索；不是完整正文、视频播放或性能证据。 |

本地公开响应清单原始记录75条请求（主清单67条、初始清单6条、补充清单2条，含重复），去重为53个URL，全部为HTTP 200。其对象是46份官方文档/公告页面、3份PNG、3个社区页面和1个公开JSON；归一记录含bytes、SHA256、最终URL、HTML title/h1（适用时），见[公开响应记录](checks/public-link-responses.json)。**HTTP 200仅证明取得对应响应，不证明已读完页面、视频成功播放、字幕完整或产品运行成功。**正文读取、逐图视检与媒体实际播放范围另列于每项。S36/S37本轮既由公开网页工具读到主体正文，也有补充HTTP 200/title/h1记录。LinkedIn/YouTube/X及二级材料的取证范围以研究笔记和正常页面实际读取为准，没有用文档下载清单替它们背书。仓库不提交HTML镜像或个人缓存路径。

## 1. Evolve直接产品文档、原始图片与发布公告

| ID | 原始来源 | 发布/显示日期 | 层级与实际取得范围 | 用途与边界 |
| --- | --- | --- | --- | --- |
| S01 | [Evolve overview](https://www.palantir.com/docs/foundry/aip-evolve/overview) | 滚动文档；未标独立发布日期 | P1；正文已读；公开响应记录HTTP 200 | 定义、目标、requirements、配置、proposal、graph、Resume与库存示例。未公布完整target/变更支持矩阵或搜索算法。 |
| S02 | [Review工作流原图](https://www.palantir.com/docs/resources/foundry/aip-evolve/aip-evolve-workflow-1.png) | 未标图片制作日 | O1；原PNG下载且逐图视检；HTTP 200 | 10cases、side-by-side、Best effort、model/prompt与五轮配置；是官方示例截图，不是本研究租户运行。 |
| S03 | [Agent graph原图](https://www.palantir.com/docs/resources/foundry/aip-evolve/aip-evolve-workflow-2.png) | 未标图片制作日 | O1；原PNG下载且逐图视检；HTTP 200 | 三轮Orchestrator与specialists的实例；不能推出固定DAG/全部目标必经步骤。 |
| S04 | [Proposal原图](https://www.palantir.com/docs/resources/foundry/aip-evolve/aip-evolve-workflow-3.png) | 未标图片制作日 | O1；原PNG下载且逐图视检；HTTP 200 | GPT-4o→GPT-5.4 Mini、204.6→72.4 compute-seconds/call、10例通过；收益仅复核算术，未复现执行。 |
| S05 | [2026年8月公告：Evolve Beta](https://www.palantir.com/docs/foundry/announcements/2026-08#introducing-aip-evolve-coordinate-ai-fde-agents-to-improve-ai-systems-in-foundry) | 2026-08-18 | P1；Evolve条目正文已读；月份页HTTP 200 | Beta状态、安装及权限前置、审查变更。不是首次公开出现或所有租户开放的证明。 |
| S06 | [2026年9月公告：Evolve GA](https://www.palantir.com/docs/foundry/announcements/2026-09#introducing-aip-evolve-coordinate-ai-fde-agents-to-improve-ai-systems-in-foundry) | 2026-09-08 | P1；Evolve条目正文已读；月份页HTTP 200 | GA流程、验证/限制、AI FDE、proposal与Global Branching；未证明自动生产发布。 |

## 2. AIP Evals：关联验证能力

| ID | 原始来源 | 发布/显示日期 | 层级与实际取得范围 | 用途与边界 |
| --- | --- | --- | --- | --- |
| S07 | [Evals overview](https://www.palantir.com/docs/foundry/aip-evals/overview) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 函数测试对象、suite/case/metric及AI FDE集成；不是页面或全部业务链路验收。 |
| S08 | [Create an evaluation suite](https://www.palantir.com/docs/foundry/aip-evals/create-suite) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | cases、目标函数、evaluator、metrics、阈值及通过判定；内置评测器不能自动推为Evolve默认选择。 |
| S09 | [Run an evaluation suite](https://www.palantir.com/docs/foundry/aip-evals/run-suite) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | last-saved/published、user/project scope、24小时/长期保留、重复/并行与metadata；逐次Evolve实际run仍需核查。 |
| S10 | [Experiments](https://www.palantir.com/docs/foundry/aip-evals/experiments) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 显式参数组合的grid search与run比较；不能据此给Evolve指定内部搜索算法。 |
| S11 | [Intermediate parameters](https://www.palantir.com/docs/foundry/aip-evals/intermediate-parameters) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 暴露/保存Logic中间输出，供评估与debug；不是所有evolution自动采集的保证。 |
| S12 | [Evaluate Ontology edits](https://www.palantir.com/docs/foundry/aip-evals/ontology-edits) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | Ontology simulation与编辑结果评估；不覆盖任意外部I/O或全部状态副作用。 |

## 3. AI FDE与AIP执行、费用及数据合同

| ID | 原始来源 | 发布/显示日期 | 层级与实际取得范围 | 用途与边界 |
| --- | --- | --- | --- | --- |
| S13 | [AI FDE overview](https://www.palantir.com/docs/foundry/ai-fde/overview) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 原生工具、初始context、预览与检查CI、branch proposal/PR；执行agent能力不等于Evolve全部目标支持。 |
| S14 | [Modes and capabilities](https://www.palantir.com/docs/foundry/ai-fde/modes-and-capabilities) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | Logic/TypeScript/Python/OSDK React等工程能力；不可由mode外推Evolve通用UI优化。 |
| S15 | [Navigation](https://www.palantir.com/docs/foundry/ai-fde/navigation) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | context、outline/tokens、工具与main/unbranched/build审批及allowlists。 |
| S16 | [Security and governance](https://www.palantir.com/docs/foundry/ai-fde/security-and-governance) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 当前用户身份/权限、mutating consent、session markings/私有性与audit；Evolve独立artifact权限尚未完整披露。 |
| S17 | [Best practices](https://www.palantir.com/docs/foundry/ai-fde/best-practices) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 连续/并行操作对资源的压力、生成代码审阅及代表数据验证；不是优化成功率承诺。 |
| S18 | [AIP compute usage](https://www.palantir.com/docs/foundry/aip/aip-compute-usage) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | tokens到compute-seconds换算、归属与用量导出；compute不是wall time，公开rates非所有客户通用价格。 |
| S19 | [AIP security and privacy](https://www.palantir.com/docs/foundry/aip/aip-security) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | AIP管理的托管模型通道保留/训练/地域合同；不自动覆盖外部MCP client的模型供应商。 |

## 4. Global Branching、Logic与Action：关联治理及发布能力

| ID | 原始来源 | 发布/显示日期 | 层级与实际取得范围 | 用途与边界 |
| --- | --- | --- | --- | --- |
| S20 | [Global Branching core concepts](https://www.palantir.com/docs/foundry/global-branching/core-concepts) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 资源新建/删除、Ontology例外、rebase/checks/merge/build选择、partial failure与生命周期。 |
| S21 | [Branch security](https://www.palantir.com/docs/foundry/global-branching/branch-security) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | branch role与resource权限、proposal可见/merge、organizations与metadata边界。 |
| S22 | [Resource protection and approval policies](https://www.palantir.com/docs/foundry/global-branching/resource-protection-and-approval-policies) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 默认自有权限满足与custom审批策略；proposal不必然代表独立双人审批。 |
| S23 | [Global Branching integrations](https://www.palantir.com/docs/foundry/global-branching/integrations) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 各资源/函数集成差异，TSv2 local OSDK、Python及OSDK限制；不声称任意程序完全隔离。 |
| S24 | [Branching Action types](https://www.palantir.com/docs/foundry/action-types/branching-action-types) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | branch对象索引/测试编辑、webhook/notification和external calls副作用；与Evals simulation分开。 |
| S25 | [Branching AIP Logic](https://www.palantir.com/docs/foundry/logic/branching-logic) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | Branched pre-release供同分支Workshop/Actions联调、deployability与merge限制；这条组合路径并非Evolve默认自动执行。 |
| S26 | [AIP Logic core concepts](https://www.palantir.com/docs/foundry/logic/core-concepts) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 函数/blocks、Workshop消费、Ontology edits须发布并经Action调用。 |
| S27 | [AIP Logic FAQ](https://www.palantir.com/docs/foundry/logic/faq) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | Workshop/function API五分钟限时与Debugger差异、saved version恢复；不是跨资源事务rollback。 |

## 5. Pilot、Workshop及平台生命周期/依赖图：应用链路边界

| ID | 原始来源 | 发布/显示日期 | 层级与实际取得范围 | 用途与边界 |
| --- | --- | --- | --- | --- |
| S28 | [Pilot overview](https://www.palantir.com/docs/foundry/pilot/overview) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 当前Beta、应用/widget生成、Ontology/seed/design能力；独立产品合同不移植给Evolve。 |
| S29 | [Pilot workspace overview](https://www.palantir.com/docs/foundry/pilot/workspace-overview) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 构建seed/Production、preview/logs、Editor/Deploy views；不证明Evolve执行隔离环境。 |
| S30 | [Deploy an application](https://www.palantir.com/docs/foundry/pilot/deploy-an-application) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 补充核验：部署、运行数据与Main Action语义；正文未用其证明Evolve自动部署。 |
| S31 | [Deploy a custom widget](https://www.palantir.com/docs/foundry/pilot/deploy-a-widget) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | Registry tag/release及既有Workshop usages不自动升级。 |
| S32 | [Use functions in Workshop](https://www.palantir.com/docs/foundry/workshop/functions-use) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | function-backed variables/actions与版本选择；解释应用如何消费优化函数。 |
| S33 | [Workshop publishing and versioning](https://www.palantir.com/docs/foundry/workshop/versions) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | save/publish、auto-publish及版本恢复；merge/proposal不是Workshop viewer发布证明。 |
| S34 | [Workshop Performance Profiler](https://www.palantir.com/docs/foundry/workshop/performance-profiler) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | widget/variable/network与module load实测表面；没有文档把它连接为Evolve自动验收器。 |
| S35 | [Widget display optimization](https://www.palantir.com/docs/foundry/workshop/widget-display-optimization) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | mount/unmount的状态、性能和资源取舍；不能由标题推成Evolve页面优化功能。 |
| S36 | [Development lifecycle](https://www.palantir.com/docs/foundry/platform-overview/development-life-cycle) | 滚动文档；未标独立发布日期 | P2；公开网页主体正文已读；补充响应HTTP 200/title/h1已核 | Beta/GA与enrollment、基础设施/合同、宣布后延迟的区别；GA不保证每个租户每项功能已启用。 |
| S37 | [Workflow Lineage overview](https://www.palantir.com/docs/foundry/workflow-lineage/overview) | 滚动文档；未标独立发布日期 | P2；公开网页主体正文已读；补充响应HTTP 200/title/h1已核 | 目标资源与调用依赖的图，与Evolve agent activity graph不同。 |

## 6. Palantir MCP与Ontology MCP：开发工具和业务执行接口

| ID | 原始来源 | 发布/显示日期 | 层级与实际取得范围 | 用途与边界 |
| --- | --- | --- | --- | --- |
| S38 | [Palantir MCP overview](https://www.palantir.com/docs/foundry/palantir-mcp/overview) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 补充核验：builder/coding-agent入口；可读业务对象，不是只读metadata。 |
| S39 | [Palantir MCP available tools](https://www.palantir.com/docs/foundry/palantir-mcp/available-tools) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 实际公开catalog、对象query/aggregate、类型/branch/proposal等；未见Evolve专用工具/通用Workshop布局编辑工具。 |
| S40 | [Palantir MCP security](https://www.palantir.com/docs/foundry/palantir-mcp/security) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | Ontology变更proposal与main人工批准、dataset限制、外部模型数据流；不扩大为每次MCP调用人审。 |
| S41 | [Palantir MCP installation](https://www.palantir.com/docs/foundry/palantir-mcp/installation) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 补充核验：管理员启用与user token权限。 |
| S42 | [Palantir MCP tool search](https://www.palantir.com/docs/foundry/palantir-mcp/tool-search) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 本地工具发现/排序和会话可用性；不是Evolve候选优化搜索算法。 |
| S43 | [Ontology MCP overview](https://www.palantir.com/docs/foundry/ontology-mcp/overview) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 对象SQL、Action、query functions与外部LLM数据流；业务数据写入不同于Ontology schema修改。 |
| S44 | [Ontology MCP sample architecture](https://www.palantir.com/docs/foundry/ontology-mcp/sample-architecture) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 业务数据、Action与functions的调用结构；自绘概念图不宣称Evolve内部采用该拓扑。 |
| S45 | [Authentication and authorization](https://www.palantir.com/docs/foundry/ontology-mcp/authentication-and-authorization) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | OAuth用户/service user、restrictions/scopes交集；不保证全部Action需实时人工批准。 |
| S46 | [Example MCP workflows](https://www.palantir.com/docs/foundry/ontology-mcp/example-mcp-workflows) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | headless agents读写业务数据；不自动获得Evolve API/会话或branch审批流程。 |
| S47 | [Debugging with MCP Inspector](https://www.palantir.com/docs/foundry/ontology-mcp/debugging-with-mcp-inspector) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | tools/schema/成功与错误结果核验；当前不支持MCP prompts/resources，不替代业务验收。 |
| S48 | [MCP tools and agent configuration](https://www.palantir.com/docs/foundry/ontology-mcp/mcp-tools-and-agent-configuration) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | 补充核验：客户端配置，Copilot Studio专门说明与authentication示例有差异；未做指定client实测。 |
| S49 | [Developer Console application restrictions](https://www.palantir.com/docs/foundry/developer-console/application-restrictions) | 滚动文档；未标独立发布日期 | P2；正文已读；公开响应记录HTTP 200 | restricted默认与unrestricted选项、资源上限；不假定所有应用已有实体白名单。 |

## 7. 开发者社区：具时间与情境的一手反馈

| ID | 原始来源 | 发布/显示日期 | 层级与实际取得范围 | 用途与边界 |
| --- | --- | --- | --- | --- |
| S50 | [AIP Evolve, where’s the tutorial?](https://community.palantir.com/t/aip-evolve-where-s-the-tutorial/6526) | 2026-04-30 09:48（页面显示） | D1；可见原帖正文已读；HTTP 200 | Kacarves教程/概念混淆；证明名称已流通，不证明首发或全面可用。 |
| S51 | [AIP Evolve Questions/Feedback](https://community.palantir.com/t/aip-evolve-questions-feedback/7148) | 2026-08-26 20:50；08-27 15:34回应，后续09-01 | D1；可见讨论正文与回应已读；HTTP 200 | tanmayb入口、heuristics、feedback与多proposal；colton迁移解释。属于当时原始回应，不是跨版本正式契约。 |
| S52 | [Questions/Feedback公开JSON](https://community.palantir.com/t/aip-evolve-questions-feedback/7148.json) | 帖子同S51；JSON访问2026-10-01 | D1；公开JSON已读；HTTP 200 | 核查作者/时间/群组标签。Palantirians且staff=false不独立证明雇佣关系，也不证明与演示者同一身份。 |
| S53 | [AIP Evolve Install Error](https://community.palantir.com/t/aip-evolve-install-error/7255) | 2026-09-21 20:52；09-22 13:20回应 | D1；可见原帖/回应正文已读；HTTP 200 | Free Dev Tier不可用与争取年底计划；66/60 Action types是具体用户情境，不能定为统一产品配额。 |

## 8. LinkedIn官方原帖、公开短片转写与社交传播

| ID | 原始来源 | 发布/显示日期 | 层级与实际取得范围 | 用途与边界 |
| --- | --- | --- | --- | --- |
| S54 | [Palantir：AIP Evolve, our new product for making agents…](https://www.linkedin.com/posts/palantir-technologies_aip-evolve-our-new-product-for-making-agents-activity-7466229875868356608-PuLS) | 5月2026线索；页面显示4mo，精确发布日期未核 | R1；官方原帖正文、作者评论、短片完整可见Transcript已读；媒体未播放 | 评论明确关联p0pjtkg1ny4；97%compute/+7pp质量、允许变更与消掉两个LLM calls的叙述。各段分母及自动转写模型名未核，不能合并收益。 |
| S55 | [Palantir：At DevCon6, see how Dr. David Zihr…](https://www.linkedin.com/posts/palantir-technologies_at-devcon6-see-how-dr-david-zihr-medical-activity-7485030356522336256-1oOV) | 页面显示2mo Edited；精确短片发布日期未核 | R1；官方正文及短片完整可见Transcript已读；未把转写当完整医院视频观看 | 具名医院流程、两处模型替换、68%compute降本与延迟取舍。临床安全、样本/版本/匿名化程度未核。 |
| S56 | [Palantir：See how Palantir FDE Colton Rusch…](https://www.linkedin.com/posts/palantir-technologies_see-how-palantir-forward-deployed-engineer-activity-7485082212904800256-rMlx) | 页面显示2mo Edited；精确短片发布日期未核 | R1；官方正文及短片完整可见Transcript已读 | 任务专用OSDK专家审阅应用、pass/fail反馈、模型/prompt迭代与一位专家90%偏好；不是90%准确率或通用UI优化。 |
| S57 | [Palantir：AIP Evolve reduced cost and compute time…](https://www.linkedin.com/posts/palantir-technologies_aip-evolve-reduced-cost-and-compute-time-activity-7503432895924064256-e7wk) | 2026年9月剪辑；精确发布日期未核 | R1；官方原帖正文及短片完整可见Transcript已读；混合剪辑缺speaker标签 | 约70%、67→88、47%/67%、另一30cases/90%、84%确定性替代分别保留上下文；宣传愿景不补成训练/发布API契约。 |
| S58 | [Tyler Robb：Palantir AIP Evolve](https://www.linkedin.com/posts/tylerjrobb_palantir-aip-evolve-activity-7503502640094461953-zyVu) | 精确发布日期未核；关联2026年9月官方短片 | S1；可见原始社交帖子已读 | 重复47%/67%并链接官方剪辑，无独立实验或客户工件；不当第二次测量。 |

## 9. YouTube原视频与局部实际观看

| ID | 原始来源 | 发布/显示日期 | 层级与实际取得范围 | 用途与边界 |
| --- | --- | --- | --- | --- |
| S59 | [Chad & Colton完整演示 p0pjtkg1ny4](https://www.youtube.com/watch?v=p0pjtkg1ny4) | 2026年5月线索；精确上传日未核 | M1；官方关联/标题说明线索；完整视频未观看 | 正常YouTube初次要求登录确认非机器人；web读取失败、LinkedIn媒体不可播放。S54转写不能升级为完整视频内容核验。 |
| S60 | [DevCon6：Product Launch, Agent Observability & Optimization](https://www.youtube.com/watch?v=GZHSCMz6Aio) | 2026年7月；本轮未重新核定精确上传日 | O1+M1；正常公开播放器局部实际播放/截图；标题、频道、时长可见 | 实际观察7:41–7:48附近、12:02–12:11附近、13:00–13:12附近；两张真实帧。没有整片观看、全文字幕或指标复现。 |
| S61 | [Code in Prod：Tampa General Hospital](https://www.youtube.com/watch?v=WLleqr4GEAw) | 2026-07-14（本轮扩展说明显示上传日） | O1+M1；正常公开播放器0:00–0:11、7:07–7:17局部实际播放；保存07:17帧 | 流程图画面、原题/频道已观察；未完整观看。68%和90%仍以S55/S56原始短片转写为数字依据，截图不是独立收益测量。 |
| S62 | [Palantir AIP Evolve：9月剪辑 yEzGboawqNw](https://www.youtube.com/watch?v=yEzGboawqNw) | 2026年9月；相对发布时间线索，精确上传日未核 | M1；页面说明/搜索元数据；YouTube版未完整观看 | 原始可见短片Transcript来自S57；未取得YouTube全文字幕或逐段speaker核验。 |

## 10. X原帖与二级追踪线索

| ID | 原始来源 | 发布/显示日期 | 层级与实际取得范围 | 用途与边界 |
| --- | --- | --- | --- | --- |
| S63 | [PalantirTech：5月Evolve演示原帖](https://x.com/PalantirTech/status/2060463832410292652) | 2026-05-29（搜索索引日期，非独立核定上传日） | M1；搜索片段/日期线索；直接原页403 | 用于追踪5月公开演示；不以搜索摘要代替完整正文、视频观看或首发日期。 |
| S64 | [PalantirTech：医院成本/调用/专家偏好原帖](https://x.com/PalantirTech/status/2079263914139758785) | 精确发布日期未核 | M1；搜索片段；直接原页403 | 70%cost、84%更少GPT calls、90%专家偏好仅登记线索；不能与68%相乘或合并为已复现结果。 |
| S65 | [Donald Zhong：AI News 2026-09-09](https://www.donaldzq.com/blog/ai-news-2026-09-09) | 2026-09-09 | S1；文章正文已读 | 转述官方库存示例；将compute cost写作average compute time，故单位/沿革回到原始来源核查，无独立实验。 |
| S66 | [Vanyar：What is Palantir, Part 7](https://vanyar.com/articles/what-is-palantir-part-7-the-ai-stack-that-starts-with-your-business) | 精确发布日期未核 | S1/M1；本轮取得搜索/可见摘录；未确认完整文章已读 | 生态解释、同一库存示例的二级材料；不作为新增实验、完整机制或独立成功证据。 |
| S67 | [Data Workers on Palantir](https://dataworkers.io/blog/data-workers-on-palantir/) | 精确发布日期未核 | S1/M1；搜索可见内容/生态介绍；未确认完整文章已读 | 把Evolve列入生态，但未取得独立执行日志/代码/评测工件，不算客户成功案例。 |
| S68 | [Black Matter：The week the model labs shipped operating layers…](https://blackmatter.vc/lab/the-week-the-model-labs-shipped-operating-layers-not-models) | 提供2026-05-29线索；文章精确发布日期未核 | S1/M1；二级周报可见线索与官方X关联；未确认完整文章已读 | 原帖追踪入口，不作产品契约、实现机制或客户效果依据。 |

### 视频定位与本地媒体的关联

S60的两个定位入口是[12:11配置与限制](https://www.youtube.com/watch?v=GZHSCMz6Aio&t=731s)和[13:12 Agent graph](https://www.youtube.com/watch?v=GZHSCMz6Aio&t=792s)，分别对应`05-devcon-constraints-12m11s.jpg`与`04-devcon-agent-graph-13m12s.jpg`。S61的[07:17医院流程图](https://www.youtube.com/watch?v=WLleqr4GEAw&t=437s)对应`06-tgh-workflow-07m17s.jpg`。这些是跳转后实际播放并确认更新的画面，不是以章节名称/缩略图冒充关键帧。原PNG及截图的尺寸、bytes、SHA256、保存/视检说明见[assets.md](assets.md)，检查范围见[checks.md](checks.md)。

正常视频/字幕读取曾遇页面读取失败、限流、DNS失败或登录确认；未成功的尝试没有升级为观看或下载成功。本研究没有取得Foundry租户运行、客户代码PR、可下载测试集/evaluator、完整候选版本、账单或生产发布日志，没有独立复现任何宣传收益，也未使用受限来源的替代凭据或绕过路径。

## 11. 既有研究：固定版本背景与去重参考

以下三项是本仓库已有研究，固定到同一base commit以保持外部背景可追溯；不是Palantir第一方材料。本轮在本地读取相关正文以划清增量范围，主文关键事实重新回到本台账中的官方原始来源，不以旧报告重复引用作为独立交叉验证。没有新增网络读取或为GitHub背景URL补造HTTP状态。

| ID | 固定版本来源 | 日期/版本 | 层级与实际取得范围 | 用途与边界 |
| --- | --- | --- | --- | --- |
| S69 | [AI FDE研究§13.2：Evolve把优化合同产品化](https://github.com/501981732/palantir-research/blob/6f2ef0eefdc5e0f2c0604eff75ed4095f582ace2/research/ai-fde-2026-10/README.md#132-evolve-把优化合同产品化) | 研究目录2026-10；固定commit `6f2ef0e` | S1；本地已有报告的Evolve及相关段落已读 | 识别既有Evolve综述与本报告机制/应用链路增量；不作新官方产品证据。 |
| S70 | [Pilot研究](https://github.com/501981732/palantir-research/blob/6f2ef0eefdc5e0f2c0604eff75ed4095f582ace2/research/pilot-2026-09/README.md) | 研究目录2026-09；固定commit `6f2ef0e` | S1；本地已有报告的产品/部署相关段落已读 | 识别专用前端构建、seed/生产及widget发布合同；本轮关键结论重新读S28–S31。 |
| S71 | [Workshop Runtime研究](https://github.com/501981732/palantir-research/blob/6f2ef0eefdc5e0f2c0604eff75ed4095f582ace2/research/workshop-runtime-2026-10/README.md) | 研究目录2026-10；固定commit `6f2ef0e` | S1；本地已有报告的运行/函数/发布相关段落已读 | 识别消费与运行时验收边界；没有扩展EOS内部对照，本轮关键结论重新读S32–S35。 |

## 引用覆盖与概念图来源

来源表覆盖主文、两附录和概念图说明中全部外部URL，包括公告锚点、社区JSON与三个已保存视频时间点。S30/S38/S41/S48及原图S03/S04是补充核验来源，不因正文未重复引用而省略。来源数量按独立页面/图片/视频计；同一视频的多个时间点、同一公告条目的锚点都不增加独立证据数量。

三张概念图为作者依据S01/S16/S20等已读合同自行绘制并实际渲染的解释图；没有取得Evolve内部固定Agent DAG、调度代码或隐藏搜索算法。图示的关联平台发布/消费路径需要各自合同核验，虚线或作者分析不代表Evolve自动执行整条链路。自绘文件和QA记录见[diagrams/README.md](diagrams/README.md)。
