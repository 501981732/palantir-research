# EOS：应用内助手的架构借鉴与可验证方案

> 本附录全部新增方案与验收用例均为研究建议。唯一 EOS 现状依据是仓库已公开、经授权的 [Workshop 运行机制对照](../workshop-runtime-2026-10/eos-comparison/README.md)，固定于[048108bf 提交](https://github.com/501981732/palantir-research/blob/048108bf2f01cacac40f6ef72bf96e37dca686f4/research/workshop-runtime-2026-10/eos-comparison/README.md)，基线为 2026-10-01 的静态研究；不是本轮当前代码实测。本轮未读取新的 EOS 内部代码、公司资料、后端或部署环境。

## 1. 应用助手应该成为现有运行系统的消费者

公开历史基线已经区分有效 DSL/module、UI session、运行变量、查询缓存、事件队列、Action 提交与保存发布，并记录了从事件到 Action committed、再到缓存失效与变量重算的接线。它同时明确：已找到前端装配不等于后端事务、权限、部署或完整消费者刷新已经通过验收。[公开 EOS 对照](../workshop-runtime-2026-10/eos-comparison/README.md)

因此 EOS 的助手接入可以先形成一个适配层：读取现有模块/变量/选择上下文，调用已定义的查询和业务 Action，向现有运行变量回投类型化结果，再由已有事件/刷新通道更新界面。助手不要拥有另一份未经同步的“当前筛选”“选中对象”“已提交状态”。这不是要求 EOS 使用 Palantir 的前端实现，而是借鉴它公开区分助手定义、application state、工具与宿主呈现的责任边界。[Application state](https://www.palantir.com/docs/foundry/chatbot-studio/application-state/)、[Workshop Chatbot widget](https://www.palantir.com/docs/foundry/workshop/widgets-aip-chatbot/)

| 职责 | 公开历史基线中可复用的接线 | 新方案首先需验证的契约 |
| --- | --- | --- |
| 获取上下文 | 变量策略、ObjectSet 编译/执行、所属 module/session | 当前值来自哪个实例与 generation；隐藏、失效、无权限状态如何表示 |
| 查询对象与聚合 | QueryExecutor、元数据、统一缓存 key/scope | 模型只能选择登记字段/过滤操作；服务端校验对象与属性权限 |
| 改变界面状态 | Widget outputs、变量 override、EventRegistry/Dispatcher | 类型和作用域校验；批次完成与依赖传播完成如何区分 |
| 提交业务写入 | ActionExecutor 与 committed 汇合点 | 发起/执行身份、批准对象、参数摘要、服务端幂等与未知结果查询 |
| 刷新界面 | 缓存失效、重算、revision | 哪些消费者实际看到新值；切页、并发、离线和取消后的行为 |
| 保存发布 | DSL 校验、autosave、版本、main publish | 助手修改运行值与修改应用定义是否有独立权限/审阅/回滚 |

表内现状只引用原静态基线，不能据此声称新增助手、严格 schema、服务端幂等或审批已经存在。基线 D2/D4/D5/D8 等条目本来就是待验证风险。[历史差异表](../workshop-runtime-2026-10/eos-comparison/README.md#5-palantir-对照应聚焦语义差异)

## 2. 首先定义状态合同，再设计聊天 UI

建议每次 turn 生成只读 `ContextEnvelope`，包含模块/实例/session ID、当前页面/对象选择、变量值或查询表达式、generation、环境/分支、助手与工具版本、权限上下文的引用。该命名与字段是 EOS 建议，并不是 Palantir 公开披露的 schema；敏感凭据不进入模型上下文。

将输入分成三类：模型可见文本/字段；模型不可见但可供工具使用的确定性参数；不可发送给模型的敏感内容。将输出分成回答、引用、变量更新、拟执行调用与实际执行结果。模型说“完成”不能替代 `committed` 或服务端状态回查。Palantir 的 value visibility 与确定性参数提供了可对照的机制，但隐藏变量不是权限屏障；检索/函数仍可能把它派生为模型可见结果。[Application state](https://www.palantir.com/docs/foundry/chatbot-studio/application-state/)

尤其要规定：同一 turn 的参数取初值、调用时最新值还是已经确认的快照。Palantir 的 deterministic Action/Function input 在 reasoning loop 开始时固定；同一 query 的前序工具更新不会自动改变它。EOS 若采取不同契约，需要在 UI 与工具协议里明确。不能让用户看着更新后的筛选列表，后台却提交旧集合。[Application state — deterministic tool inputs](https://www.palantir.com/docs/foundry/chatbot-studio/application-state/#deterministic-tool-inputs)

建议确认界面显示目标对象、环境、动作、实际解析参数和影响范围；批准绑定这一份调用快照。若批准后数据或选择发生变化，重新校验并告知用户，是否重审由业务规则决定。快照签名、CAS、过期策略和审阅绑定均为待实现方案，本轮没有证据证明 Chatbot Studio 提供相同的统一事务机制。

## 3. 工具登记不能只列函数名

建议 `ToolContract` 至少描述输入/输出 schema、读写语义、执行位置、目标资源、版本、授权、确认策略、幂等/重试、超时/取消、结果回查、外部副作用及审计出口。后端 Query/Action 与客户端 Command 分开登记；可隐藏 UI 不能授予权限，可显示按钮也不能证明有权限。

| 工具类别 | 建议行为 | 所需证据 |
| --- | --- | --- |
| 只读查询 | 登记允许的类型/字段/过滤/聚合；返回结构化结果和 provenance | 与人工查询同权限；空集/无权/部分字段拒绝可区分；无越界字段 |
| 变量更新 | 在正确 module/session scope 写类型化运行值 | 多实例不串值；取消后不接受过期更新；后续事件看到预期 generation |
| 业务 Action | 参数先由后端验证；需要确认时绑定实际调用 | 批准、身份、请求 ID、结果和读回一致；未知状态不自动重复写 |
| Function / Logic | 核准实现、副作用、execution mode与版本 | 没有用“函数”标签隐藏写入/外部调用；调用者与执行主体可查 |
| 客户端 Command | 配对指定应用；校验 payload 与生命周期 | 无应用/不配对/多窗口/取消时可明确失败；业务 API 仍服务端鉴权 |
| 定义修改 / 发布 | 独立于运行态业务写入的权限和审阅链 | 有差异、基线版本、依赖校验和发布回读；不把变量更新升级为配置发布 |

Palantir Action 工具可以自动执行或用户确认；Commands 默认审批可关闭，Command 工具配置能力标 Beta；Function 工具并无同页披露的统一确认保障。EOS 不宜用一个全局“助手已获批准”覆盖所有工具。[Tools](https://www.palantir.com/docs/foundry/chatbot-studio/tools/)、[Commands](https://www.palantir.com/docs/foundry/chatbot-studio/commands-as-tools/)

## 4. 知识上游需有可核验的流水线

知识库方案应同时管理原文、提取文本、chunk、embedding、Ontology 对象/链接、检索与引用映射。建议引用返回文档 ID、版本、页/片段与检索时间，用户可打开原文；回答质量与检索质量分别评测。文档更新、删除或权限撤销需验证是否使索引、缓存、已有会话和共享日志同步失效，不能仅测试新建索引的成功路径。[官方文档处理流程](https://www.palantir.com/docs/foundry/ontology/document-processing/)、[引用](https://www.palantir.com/docs/foundry/chatbot-studio/citations/)

进入模型上下文的资料是数据，不能成为替代用户的授权指令。建议在合成资料中加入“忽略权限/提交更大范围/外传记录”等诱导内容，验证工具注册、批准与后端权限仍生效。本轮未实测 Palantir 或 EOS 对这些负面用例的表现。

## 5. 会话、日志与审计分三条线

会话解决连续对话与应用状态；产品日志解决诊断；业务审计记录谁批准并实际改变了什么。建议以受控 ID 关联三者，分别设置保留期与访问策略，避免为审计复制完整敏感 prompt、原始附件或 token。

Palantir 公开日志文档明确 source/input/访问数据的 Markings 不自动传播到 logs，需要管理员选择适当敏感度；Foundry service/trace logs 也不是 audit logs，不保证 100% 投递。这意味着 EOS 要单独评审日志权限与完整性，不应假设“源数据受保护，所以聊天日志也受同样保护”。[Configure logging](https://www.palantir.com/docs/foundry/administration/configure-logging/)

建议结果状态至少区分未开始、执行中、成功、失败、部分成功、取消请求已发出、终态未知。流结束、`cancel` 返回和客户端断开都不自动证明业务副作用已经撤销；每个写工具需要自己的回查与补偿合同。公开 API 同会话禁止并发 continue，因此 EOS 可先采用 per-session 排队，再单独验证跨会话/多 Tab 的共享对象冲突。[Continue session](https://www.palantir.com/docs/foundry/api/aip-agents-v2-resources/sessions/blocking-continue-session)、[Cancel session](https://www.palantir.com/docs/foundry/api/v2/aip-agents-v2-resources/sessions/cancel-session/)

## 6. 可执行的试验矩阵

以下是建议验收，不是已执行测试，不预设任意样本量或性能目标。先在授权的合成环境建立人工基线，任务/风险与覆盖稳定后再讨论自动写入范围。

| 场景 | 输入与操作 | 应记录的证据 | 通过条件 |
| --- | --- | --- | --- |
| 当前对象解释 | 同一对象，不同用户/属性权限 | 请求、返回字段、引用、权限拒绝 | 仅返回可见字段，拒绝可区分，不泄露无权属性 |
| 筛选→列表联动 | Query 输出 ObjectSet，再更新宿主变量 | 变量类型、scope、generation、消费者结果 | 指定实例采用正确集合，其它实例不变化 |
| 同轮输入陈旧 | 工具先换集合，后发固定参数 Action | 初始/新集合、拟提交目标、批准快照 | 明确使用哪份集合；显示和实际提交一致 |
| 确认后状态变化 | 批准前后切对象/权限/版本 | 批准摘要、后端校验、拒绝/重审 | 不静默扩大目标，失效批准不能继续提交 |
| 用户拒绝 | 对所有应确认写工具拒绝 | 拟调用、拒绝事件、业务读回 | 没有实际业务写入，说明停止状态 |
| Function 隐含写入 | 受控函数含 Ontology/外部副作用 | 实现版本、execution mode、调用与读回 | 副作用与身份可查，确认策略按实际行为生效 |
| Command 配对 | 无配对、多窗口、配对销毁 | pairing、payload、实际应用实例、返回状态 | 只作用于选定实例，不能用其它窗口补执行 |
| 流式取消 | 回答/查询/写入不同阶段取消 | message ID、cancel结果、最终content、业务状态 | 回答与副作用分别报告；unknown有查询/接管路径 |
| 网络响应丢失 | 写请求已发送但回包丢失 | 后端请求 ID、状态回查、重试次数 | 不盲目重放；成功/失败/未知据状态核定 |
| 日志权限 | 含高敏感输入，低权限viewer查日志 | logging policy、Markings、日志内容 | 不能通过日志绕过原设计数据边界 |
| 知识更新撤销 | 更新/删除原文、撤销访问，再问同问题 | 文档/索引版本、缓存与引用 | 新检索按当前授权；旧会话/日志边界单列说明 |
| 发布与旧会话 | 发布助手/工具/模型新版本 | 新旧session版本、依赖版本、评测结果 | 可区分新旧行为，无静默混版假设 |
| Evals到宿主 | Function评测后跑Workshop/React路径 | 输入/输出、变量回投、确认UI、Commands | Function评分与端到端验收分别通过 |
| 多实例刷新 | 同对象两个模块/Tab与一个独立session | 缓存scope、revision、重算和显示时间 | 定义的消费者看到正确结果；不将触发刷新算已完成 |

建议首轮优先只读查询与引用、类型化变量回投、一个显式确认的可回查 Action；通过它们后再开放 Function 副作用和客户端 Commands。现有历史基线已记录幂等、离线 scope 与候选预览写入等待验证点，应一同进入测试，而不是在助手引入后才补救。[EOS 历史验证范围](../workshop-runtime-2026-10/eos-comparison/README.md#6-下一轮验证范围与完成标准)

## 7. 指标与发布判定

分别统计任务质量、检索命中/引用正确性、工具选择与参数正确性、状态回投一致性、批准覆盖、实际写入证据、拒绝与失败恢复、总人力时间、总调用成本、延迟分布。任务完成的分母应包含失败、取消、部分成功与未知状态；正确拒绝可记安全成功，但不能计作业务任务完成。流式首字延迟和业务终态耗时也应分开。

发布门槛建议以业务断言为主：所有适用的应审写入都有有效批准；实际越权或未经授权写入为零；所有已执行写入都可追踪状态；关键业务结果正确且权限负例通过。性能阈值由相同任务、权限、数据、环境和操作者的基线确定，本稿不承诺提效比例或 SLA。

固定助手配置、模型、工具/Function、检索策略、知识/索引、宿主应用与评测数据版本。模型或工具变化重跑受影响评测；知识与权限变化另测撤销路径。AIP Evals 能作为函数层质量关口，但 Commands、确认UI、宿主变量、缓存刷新和外部副作用需独立端到端验收。[Chatbots as Functions](https://www.palantir.com/docs/foundry/chatbot-studio/chatbots-as-functions/)、[Evaluate Ontology edits](https://www.palantir.com/docs/foundry/aip-evals/ontology-edits/)

故障恢复建议按“停止后续写入→查实际终态→判断幂等或补偿→授权内修复→重跑受影响验收→形成交接记录”执行。超时未知、权限撤销、部分成功、版本不一致、证据缺失或预算耗尽均需要明确停止条件；不能通过新会话、扩大权限或换通道绕过原限制。
