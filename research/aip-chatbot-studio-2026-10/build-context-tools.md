# 构建、知识、上下文与工具机制

检索窗口：2026-10-01 23:40–23:48 UTC；Logic 写入消费路径与 API 路径补核：23:53–23:54 UTC。范围：公开官方文档；未登录 Foundry 租户、未执行 Chatbot、Action 或 Function。本文件是机制研究附录，来源与局限见 `notes/core-sources.json`。除注明“分析/建议”外，下文“文档确认”指公开文档的产品承诺，不表示本研究实测。

## 1. 结论与资源边界

AIP Chatbot Studio（旧名 AIP Agent Studio）是构建企业助手资源的工作台：构建者定义模型、指令、检索源、应用变量和可调用工具；发布后的 Chatbot 可在 Studio view、AIP Threads、Workshop 或自建应用里消费。旧名仍残留在 RID、API 路径、接口名中，因此 `aipAgents`、`agentRid` 和 `AipAgentsContextRetrieval` 不是另一套新产品。其业务范围包括上下文感知的读写工作流，不应缩为一个聊天 UI widget。[官方总览](https://www.palantir.com/docs/foundry/chatbot-studio/overview/)

Chatbot 是 Foundry 文件系统资源，有资源级访问控制。模型选择只呈现 enrollment 已启用模型的一部分；系统提示词定义助手在当前应用中的任务与业务规则，工具和变量通过 `/` 引用；温度默认 0、UI 最高 1。Save 保存进度，可附版本描述；View 可选择版本；Publish 使资源用于生产。提示框和 suggested prompts 改变入口体验，不能替代工具约束。[构建与发布](https://www.palantir.com/docs/foundry/chatbot-studio/getting-started/)

**分析：**资源不是模型本身。一个“助手版本”的行为还依赖上游 Ontology、文档数据、工具实现与模型是否仍可用；版本治理不能只备份 prompt。

## 2. 一条消息的运行路径

文档将 instructions、工具描述和变量描述编译为 raw system prompt。新用户消息触发配置好的 retrieval，结果与消息一起给模型；模型根据工具说明决定是否调用工具。上下文窗口包含系统提示词、会话历史、retrieval、application state 和 tools；溢出会报错，文档建议新建 session，未承诺自动压缩历史。[Core concepts](https://www.palantir.com/docs/foundry/chatbot-studio/core-concepts/)

| 组成 | 何时发生 | 谁决定 | 结果去向 | 容易混淆的边界 |
| --- | --- | --- | --- | --- |
| 配置 instructions/工具与变量描述 | 配置并在运行时编译 | 构建者 | 模型指令/工具定义 | 未提供的业务信息不会自动被模型理解 |
| Retrieval context | 每条新用户消息 | 配置确定执行 | 相关资料进入模型上下文 | 不是模型先决定要不要查 |
| 工具调用 | reasoning loop 中按需 | 模型选择控制流与生成参数，部分参数可绑定 | 工具结果进入模型；部分结果更新应用变量 | 不是每条消息必执行全部工具 |
| Application state | 输入、输出、引用点击 | 宿主绑定、确定性输出或模型更新 | 模型可见值、工具实参、宿主变量 | 可见性、读写能力和后端权限是不同层 |
| 回复/引用 | 模型完成生成后 | 模型内容与宿主渲染配置 | Markdown、citation UI、状态输出 | 对话文字与结构化更新分别处理 |

前两行的确定性 retrieval 机制来自 [Retrieval context](https://www.palantir.com/docs/foundry/chatbot-studio/retrieval-context/)；工具控制流来自 [Tools](https://www.palantir.com/docs/foundry/chatbot-studio/tools/)；状态更新来自 [Application state](https://www.palantir.com/docs/foundry/chatbot-studio/application-state/)。矩阵中的“容易混淆”是依据这些分层作出的解释。

## 3. 知识不是一个附件按钮：构建、索引和运行时检索

在 Ontology 路线上，知识上游可以是 PDF Media set → 提取文本 → chunk → 为每个 chunk 建立独立对象、关联原文 → 为 chunk 计算 embedding → 将 embedding 作为 Ontology vector 属性。文档的 chunk 配置包含尺寸、重叠和优先级分隔符；保留原始对象关联，是把检索命中带回 PDF 核对的基础。[Document processing](https://www.palantir.com/docs/foundry/ontology/document-processing/)

Embedding 是语义向量，Ontology 关联使最近邻搜索能返回企业对象。生成向量和向量属性属于上游工作流；消费它的入口可以是 Workshop KNN、Chatbot Ontology context 或自定义函数。官方函数教程还区分 TS v1 显式生成 query embedding 与 TS v2/Python 直接传 query text 的方法；不能把“TS v2 支持语义查询”推成“Chatbot retrieval 接口支持 TS v2”。[Semantic search](https://www.palantir.com/docs/foundry/ontology/overview-semantic-search/)、[端到端 embedding 工作流](https://www.palantir.com/docs/foundry/ontology/using-palantir-provided-models-to-create-a-semantic-search-workflow/)

Studio 提供以下三个检索上下文，可配置多个，每条新消息确定执行：

| 类型 | 资料入口与选择方式 | 工程边界 |
| --- | --- | --- |
| Ontology context | 固定 N 个对象，或在带 vector 属性的对象类型中找语义相关的 K 个；输入可为整个类型，也可为应用变量提供的过滤 object set | 可以选择传给模型的 properties；默认排除不能打印的 media reference、vector；输出可绑定 object set 与 citation 变量 |
| Document context | 选定文档的全文，或取语义相关 chunks | Relevant chunks 是 Beta，可能 enrollment 不开放；全文模式把所有文本放入窗口 |
| Function-backed context | 每次 query 执行自定义 retrieval 函数 | 适用于混合 keyword/semantic 等 Studio 原生检索不能满足的策略 |

来源：[检索类型](https://www.palantir.com/docs/foundry/chatbot-studio/retrieval-context/)。**分析：**选择全文/固定对象集适合明确且较小的工作范围；语义 top-K 降低输入规模却引入召回问题。Studio 可配置相关性检索，不等于它已提供可配置的 hybrid retrieval、reranker、质量监控与文档治理全家桶。

Function-backed context 的接口要求是 TypeScript v1 `@AipAgentsContextRetrieval()`；`messages` 是唯一必需输入，可添加 string/object set 可选参数并绑定应用变量；输出 `retrievedPrompt`，运行时粘贴到系统提示词。TS v2 repositories 不支持此 function interface。公开页面仍把直接用 AIP Logic 写 retrieval 描述为未来能力，当前建议 TS 接口 wrapper 调用 Logic。这里只记录契约，不复刻官方长示例。[Function-backed context](https://www.palantir.com/docs/foundry/chatbot-studio/retrieval-context/#function-backed-context)

**分析：**自定义 retrieval 不只是换一个查询算法；它决定输入文本、引用标识与提示片段的生成。它是可信资料和指令相遇的边界，应在工程验证中加入恶意文档、过期版本、无权限对象、空命中和重复 chunk 用例。此处是 EOS 建议，未声称 Palantir 公开文档已证明能防止 prompt injection。

## 4. Prompt 可见上下文与工具实参上下文

Studio 的 application state 旧称 parameters，公开文档明确支持 **string 和 object set**，可有多个变量，与 Workshop 同类型变量映射。变量 description 给模型解释角色；value visibility 决定值是否在 prompt 中给模型。作为 Ontology retrieval 输入的 object set 可以隐藏，因为真正选出的对象资料会被加入 prompt；动态指令 string 则必须可见。Object query 可为各对象类型绑定 initial object set，以此起点追加筛选/聚合。[Application state](https://www.palantir.com/docs/foundry/chatbot-studio/application-state/)

因此本报告用“prompt 上下文”和“工具实参上下文”作分析层区分：前者是模型需要读到的资料；后者是运行时直接传给 retrieval、Action 或 Function 的 typed input。它们不是此页面正式命名的两种产品类型。隐藏的 object set 不等于禁止工具访问；可见的 string 也不等于用户获得了某个后端权限。

有三条不同的输出路径：Object query、Ontology context、function-backed context 可把最近一次结果确定性映射到变量，**模型 streaming 结束时**更新宿主变量；Update application variable 工具让模型决定更新哪些配置变量；点击 object citation 可把该对象组成 static object set 写入引用变量。[Application state](https://www.palantir.com/docs/foundry/chatbot-studio/application-state/)

**必须单独测试的快照语义：**Action/Function deterministic input 仅支持 string/object set，且固定为 reasoning loop 开始时的变量值。同一 query 中前一个 tool 更新变量，后一个 tool 的 deterministic input 不会使用更新值。例如“先检索候选订单，再把结果绑定到 selectedOrders，接着取消 selectedOrders”不能默认按同一轮最新结果写入。建议将依赖串联封装到一个明确的 Function/Action，或在检索结果落到宿主并经用户选择后发起下一轮写请求。[Deterministic tool inputs](https://www.palantir.com/docs/foundry/chatbot-studio/application-state/#deterministic-tool-inputs)

## 5. Ontology、Action、Function、Logic 各自承担什么

| 工具 | Chatbot 可做的事 | 输入/结果边界与设计含义 |
| --- | --- | --- |
| Object query | 对指定对象类型与属性进行 filter、aggregate、inspect、link traversal | 配置限定模型能访问的类型/属性；initial object set 提供工作范围；输出可接宿主变量 |
| Action | 执行 Ontology edit，可自动执行或要求用户确认 | 人的确认与 action submission criteria/数据权限分别成立；确认不是授权替代品 |
| Function | 调用 Foundry Function，包括已发布 Logic Function | 默认自动用最新函数版本，也能指定已发布版本；确定性 state 绑定与模型生成参数可分开 |
| Update application variable | 更新允许的应用变量 | 改变应用状态，不等于写业务对象 |
| Command | 对宿主应用触发一条或多条 command | 属于宿主操作协议，详见接入研究；不能推导为 Ontology 事务 |
| Request clarification | 暂停并请求用户澄清 | 用于不充分输入；不能代替后端验证 |
| Legacy Ontology semantic search | 用 vector 属性查询 | 不带 citations、input/output variables，也不返回 resulting object set；文档推荐 Ontology context |

来源：[Chatbot tools](https://www.palantir.com/docs/foundry/chatbot-studio/tools/)。该页面称“six types”并另外列 Legacy 类型，因此上表保留六种当前工具与单独 legacy 行。

Prompted tool calling 将调用说明放进 prompt，一次只调一个工具，支持所有工具类型与可用模型。Native tool calling 利用模型原生能力，可并行调用并节省 tokens，但只支持部分 Palantir-provided 模型，以及 Action、Object query、Function、Update variable 四类。不能因为模型在供应商 API 支持 native tools，就推断在 Studio native mode 可用；Command/clarification 的工作流需按 prompted 兼容范围设计。[Tool mode](https://www.palantir.com/docs/foundry/chatbot-studio/tools/#tool-mode)

Function 是服务端隔离环境执行的业务逻辑，可读对象属性、遍历链接、编辑 Ontology。[Functions overview](https://www.palantir.com/docs/foundry/functions/overview/) Logic 把这种能力做成输入→blocks→输出的构建模型；blocks 可确定执行，也可包含 LLM 内部工具选择，后一个 block 可引用前一个输出。Logic 的核心概念与 Apply action block 文档要求：普通调用要实际写回 Ontology，须发布函数并从 Action 执行；仅含 Apply action block 不会自行取得写回上下文。因此在 Chatbot 中“Function 工具调用一个 Logic Function”和“Action 工具执行一个 Logic-backed Action”必须区分，不能仅凭前者可配置便断言写回成功。[Logic core concepts](https://www.palantir.com/docs/foundry/logic/core-concepts/)、[Logic blocks](https://www.palantir.com/docs/foundry/logic/blocks/#apply-action)

这个限制必须按消费路径表述。Automate 专页另外明确：**staged writes 关闭的 legacy Logic 可被 Logic effect 直接调用并消费其 Ontology edits；开启 staged writes 则必须包成 Action，由 action effect 调用**。这是专用 Automate 路径，不证明普通 Chatbot Function 调用也会消费并提交返回编辑。[Logic integration with Automate](https://www.palantir.com/docs/foundry/logic/aip-logic-integration-automate/)、[Logic staged writes](https://www.palantir.com/docs/foundry/logic/staged-writes/) 通用 Ontology edit Function 的编辑列表同样需消费者实际应用，函数 helper 中运行不改真实对象。[Ontology edits](https://www.palantir.com/docs/foundry/functions/edits-overview/)

也不能反向概括为“Function 工具永远只读”。公开 Function permissions 文档允许经管理员 allowlist 开放的 extended function 从内部调用 Actions，或取得额外执行所需的授权令牌。副作用要审查 Function 实现、调用权限和执行上下文，不能仅以工具名称判定；Chatbot Action 的用户确认设置也不能类推为所有 Function 内部副作用都有相同确认流程。[Extended function execution](https://www.palantir.com/docs/foundry/functions/permissions/#extended-function-execution)

Logic 默认 user-scoped execution，使用运行用户权限；project-scoped 使用包含函数的项目权限、要求依赖导入该项目且用户仍需相关 markings。后者也改变日志可见性。通用 Function 执行通常要求源 repository Viewer；function-backed Action 是例外，配置者需要读 Function，执行者按 Action 权限即可。因此无法用“能看 Chatbot”推出“能执行其全部依赖”。[Logic execution mode](https://www.palantir.com/docs/foundry/logic/execution-mode-settings/)、[Function permissions](https://www.palantir.com/docs/foundry/functions/permissions/)

## 6. 确认、权限和事务是三个层

Action 支持模型发起后人工确认，也支持自动执行；这解决交互上的意图确认。Action 后端另有 submission criteria，可联合用户/组、参数、对象状态等条件，并独立于 Action type 编辑权限。配置应把“这个用户对这批对象能否执行这个业务动作”落实为后端条件。[Chatbot Action tool](https://www.palantir.com/docs/foundry/chatbot-studio/tools/)、[Submission criteria](https://www.palantir.com/docs/foundry/action-types/submission-criteria/)

Action permissions 页面明确区分读取与写出：行/列控制过滤读取，但并不会自动限制 Action 写出的数据；保持下游保护需要 Marking/CBAC 等传播机制。调用者还须满足被编辑类型、链接、datasource 与 criteria 要求；某些只允许 Actions 的对象类型，只需 Read 也可能执行业务编辑，甚至创建自身不能读取的新对象。不要用 CRUD 直觉简单解释此模型。[Action permissions](https://www.palantir.com/docs/foundry/action-types/permissions/)

Beta staged-write Logic 可组合嵌套 Function/Action，后续读取能看到同次执行暂存的编辑。当前公开 staged-write 生产消费说明依托 Action 提供执行上下文；TS v2 文档明确嵌套 Function/Logic 的编辑加入同一批，成功后在 Action 完成前提交、异常时丢弃并由 Action 重试。未核到 Chatbot Function 工具直接调用 staged-write Logic 可独立建立写入上下文的官方契约。它不是聊天多个工具调用的全局事务，也未承诺外部系统副作用回滚。[Logic staged writes](https://www.palantir.com/docs/foundry/logic/staged-writes/)、[TS v2 staged writes](https://www.palantir.com/docs/foundry/functions/typescript-v2-staged-writes/#execution-lifecycle)

**分析：**Native 并行工具的性能能力和 staged-write 单次执行的原子性不能混合描述。“并行两个 Action 成功一个失败”的补偿、重试去重、确认之后对象状态变化、跨服务副作用等均需专项验证；公开 Chatbot 文档未提供这些保障。

## 7. 会话与版本：对话历史不是冻结全部依赖

Create Session API 是 preview，需要 `preview=true`；创建的是调用用户与 Chatbot 的会话。可显式传 `agentVersion`；省略时选择**创建时**最新 published version，Session 返回并记录版本。它提供配置版本关联，不能视为已有会话随下一次 Publish 自动升级。[Create Session](https://www.palantir.com/docs/foundry/api/aip-agents-v2-resources/sessions/create-session)

Streaming continue 增加一个 exchange 并返回 Markdown 文本流；完成后要读取 session content 才能得到完整 exchange；同一 session 不支持并发 continue，应等待或取消后再发消息。API 的 `contextsOverride` 会跳过自动 retrieval，用调用方上下文替代，因此通用的“每消息必检索”需要注明该 API override 例外。blocking 返回 `parameterUpdates`，只对配置为 `READ_WRITE` 的变量产生更新。[Streaming Continue Session](https://www.palantir.com/docs/foundry/api/aip-agents-v2-resources/sessions/streaming-continue-session)、[Blocking Continue Session](https://www.palantir.com/docs/foundry/api/aip-agents-v2-resources/sessions/blocking-continue-session)

下表路径于 2026-10-01 23:54 UTC 再次直接读取公开 API 页确认；三个 endpoint 均要求 `preview=true`，第三方 OAuth scope 为 `api:aip-agents-write`，没有执行真实调用。

| 操作 | 官方页面尾部路径（接在 `/docs/foundry/api/aip-agents-v2-resources/sessions/` 后） | HTTP 接口 |
| --- | --- | --- |
| 创建 | `create-session` | `POST /api/v2/aipAgents/agents/{agentRid}/sessions` |
| 阻塞续聊 | `blocking-continue-session` | `POST /api/v2/aipAgents/agents/{agentRid}/sessions/{sessionRid}/blockingContinue` |
| 流式续聊 | `streaming-continue-session` | `POST /api/v2/aipAgents/agents/{agentRid}/sessions/{sessionRid}/streamingContinue` |

Continue 请求里关联追踪的准确字段是 `sessionTraceId`；streaming 另可传 `messageId` 以供取消。不要把日志中常用的 `traceId` 当作请求字段名，也不要假设 Markdown 文本流等于一套结构化工具事件协议。

当 Chatbot 发布为 Function，`userInput` 必需；可选 `sessionRid` 延续会话，创建新会话须省略，不能传 empty string；application variables 成为可选输入/输出。默认 object set 输入是该类型全部对象，string 默认由 Studio 设置；输出只包含确实更新的变量。Function 返回最终 Markdown 与 session RID；可在每次 Publish 或每次 Save 时生成 Function 版本，连接 Evals、Automate 和其他 Function 消费路径。[Chatbots as Functions](https://www.palantir.com/docs/foundry/chatbot-studio/chatbots-as-functions/)

**分析：**版本相关但不同的轴至少有 Chatbot 配置、引用 Function 版本、模型部署/退役、知识数据、Ontology schema 与宿主应用版本。Chatbot 会话固定配置版本并不等于资料快照；工具若默认 latest，其实现仍可能改变。API 示例里的 estimated expiry 不能当作普遍固定 TTL；此研究未核到统一留存保证。

模型还会退役或进入 brownout，使依赖工作流失败；迁移要找到实际配置模型的上游资源，并 Save/Publish，而不是只调整 Workshop 外壳。替代模型应通过相同业务 eval 再验证。[Model deprecation](https://www.palantir.com/docs/foundry/model-catalog/model-deprecation/)

## 8. 引用和工具结果：证据展示与状态回写不同

Ontology/Document retrieval 自动提供 citation 提示，UI 展示 inline bubbles 和 Sources 下拉。Ontology 引用默认打开对象；PDF 默认打开文档页，可指定 page；URL 引用打开外链。其它 context 或工具**默认没有 citation**，构建者需提供格式指令；正确 XML 渲染并不自动证明引用支撑回答。可全局关闭 citations、覆盖点击行为，或把被点对象写入变量供其他 widget 展示。[Citations](https://www.palantir.com/docs/foundry/chatbot-studio/citations/)

日志是一个较明确的机制证据：每条用户消息为一次 execution，用 traceId 关联；`tool_call` 包含 parsed input，`tool_call_result` 的成功结果分别包含 **`llm_value`** 和 **`variable_updates`**；失败记录原因与错误。system message 在 prompted mode 将工具放进 content，native mode 单列 native_tools。final response 还可能是 client tool call，而不是最终文本。由此应分别检查“模型读到的工具结果”“宿主收到的变量更新”“业务对象已提交结果”，不能把它们合并成一个 chat response。[Session logging](https://www.palantir.com/docs/foundry/chatbot-studio/session-logging/)

## 9. EOS 可验证设计建议（分析，未读取本轮 EOS 内部代码）

| 建议 | 依据的机制 | 可验证用例/验收信号 |
| --- | --- | --- |
| 把应用选择、知识片段、工具能力和输出状态分别建模 | state visibility、retrieval、tools 与 variable output 分层 | 隐藏 object set 能缩小工具范围而不打印整个集合；不授权对象始终不可返回 |
| 将业务写入收敛为窄的 Action，绑定明确业务条件 | confirmation + submission criteria 是两道边界 | 预览正确但对象状态改变后，后端再次验证并拒绝过期操作 |
| 依赖更新结果的多步骤写入放入同一业务 Function/Action | deterministic inputs 在轮开始固定 | 同轮 query→update state→write 用旧值的用例显式失败/分轮；复合操作读后写符合预期 |
| 发布清单记录所有依赖版本与 scope | Session agentVersion 与 Function latest 是不同轴 | 固定Chatbot版本、变更Function latest，观察是否漂移；锁定后重放结果可归因 |
| 把引用检查当作质量指标 | 渲染是格式机制 | 引用对象存在、用户可读、原文支撑命题、PDF页码正确；空命中回答不伪造来源 |
| 用同一 trace 串接工具输入、模型结果、状态更新和业务提交 | Session logging 字段已分层 | 一次操作能解释是谁、用哪个版本、引用何资料、提交哪些对象、为何失败 |
| 无论宿主按钮是否确认，都验证客户端执行协议 | API只公开文本流与结构化exchange，不保证等价widget交互 | 自建React拒绝/确认/取消/重试后不误写、不双写；作用域错误准确呈现 |
| 对知识pipeline与模型迁移独立评估 | chunk/vector上游、模型退役 | 小集合/full text/top-K/hybrid在相同问题上对比召回与成本；模型替换前后的写入选择无越界 |

## 10. 仍需租户或更深公开证据核验

1. Action 人工确认在自建 React/REST 调用中的暂停、确认、恢复协议，以及 Function 化后是否支持相同交互；当前读取的 API 请求没有直接确认字段，不能说“完全没有”，也不能说“自动支持”。
2. Object query 的完整模型可调用 schema、结果数量截断、复杂聚合、link traversal 与 selected property 的具体返回形式。官方概述仅承诺能力类别。
3. Native mode 并行读写冲突时的顺序、重试与补偿；未见整个 reasoning loop 事务保证。
4. 同一 reasoning loop state 更新何时被下一次模型循环可见，除了 deterministic inputs 固定与 streaming结束宿主回写，公开文档未给完整调度契约。
5. 新 session 后默认 object set 全类型的工作范围风险；宿主是否在每次 Continue 显式送入当前选择，须实测。
6. 文档 relevant chunks Beta 的租户开通、chunk策略、embedding模型/更新周期、大小限制和实际质量；未用截图冒充本地实测。
7. Chatbot 配置变更、Function latest 更新、模型退役与已有会话的组合；Session version 不足以证明所有依赖一致冻结。
8. 会话统一 TTL/历史保留、归档与删除的产品保证；API例子中的时间不能代表规则。

## 11. 检索失败记录

从 Functions overview 导航点击 “Consistency and isolation” 返回 Internal Error；随后直接尝试 `https://www.palantir.com/docs/foundry/action-types/consistency-isolation/` 同样返回 Internal Error（工具未返回首次链接实际目标 URL，后者不能当作已核验的有效路径）。本文件的事务判断只采用可读的 Logic/TS v2 staged-write 文档，不作该页已核验声明。
