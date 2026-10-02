# 应用集成附录：Workshop、Commands 与 React / OSDK 会话接入

检索日期：2026-10-01。证据范围为 Palantir 官方文档、公开 SDK 的固定提交与其公开测试。本附录没有登录 Foundry 租户，没有运行真实 Chatbot、Action、Function、OAuth 或业务数据请求，也没有重新读取 EOS 内部源码。代码示例是根据公开类型与路由构造的最小调用方案，未声称已编译或已连接租户成功。

## 1. 先按执行位置与状态归属选集成方式

应用内 AI 助手需要四条契约：宿主把业务选择与筛选送给助手；助手把结构化结果回填宿主；助手通过业务工具读取或写入后端；助手通过客户端操作改变当前应用。AIP Chatbot Studio 分别以 application state、Ontology / Function / Action 工具、Commands，以及 sessions API 对应这些契约。Workshop 是其中一个现成宿主；自建 React 应用还需实现会话 UI、流消费、状态映射和错误恢复。[Studio overview](https://www.palantir.com/docs/foundry/chatbot-studio/overview/)、[Foundry APIs](https://www.palantir.com/docs/foundry/chatbot-studio/foundry-apis/)、[Commands overview](https://www.palantir.com/docs/foundry/cross-app-interactivity/commands-overview/)

| 接入方式 | 承担什么 | 应用架构上的选择依据 |
|---|---|---|
| Workshop 的 AIP Chatbot widget | 选择已发布 Chatbot、版本、变量映射，提供聊天宿主 | 现有 Workshop 页面需要与助手交换业务状态；不必自行实现全部会话界面 |
| Chatbot 的 Commands 工具 | 在已配对的应用客户端执行已声明的操作 | 操作依赖当前地图、屏幕、选择或临时 UI 状态 |
| Platform SDK 的 Sessions / Contents API | 创建会话、逐轮发送、读完整内容、流式响应、取消、trace | 自建 React 或其他客户端需要多轮对话与自主界面 |
| 发布为 Function 后由 OSDK 执行 | 以一个函数契约执行 Chatbot；可用 sessionRid 继续会话 | 既有工作流已围绕 Function 编排，或单次任务无需自己编排完整 Session API |

上表是基于公开契约的架构归纳。Function 适配并非只支持单轮；官方明确接受可选 `sessionRid`。API 也并非直接调用裸模型：它执行已配置 Chatbot 的检索和工具链。[Chatbots as Functions](https://www.palantir.com/docs/foundry/chatbot-studio/chatbots-as-functions/)、[Blocking continue](https://www.palantir.com/docs/foundry/api/aip-agents-v2-resources/sessions/blocking-continue-session)

## 2. Workshop 接的是 Studio 产物，不应沿用 Legacy 配置说明

现代 widget 的基础配置包括 Chatbot、要纳入的已发布版本以及是否显示 reasoning。配置了 application variables 后，widget 才展示同类型 Workshop 变量映射，并按 Studio 定义的变量读写权限交互。`textbox` 对应聊天输入字段；用户打字会更新它，来自 widget 外部的变量修改则会自动发送当前值，因此 Workshop 事件可驱动发消息。[AIP Chatbot widget：Base configuration (AIP Chatbot)](https://www.palantir.com/docs/foundry/workshop/widgets-aip-chatbot/#base-configuration-aip-chatbot)

该页面同时保留 **Base configuration [Legacy]**：在 Workshop 配置中直接定义提示词和工具、引用 AIP Logic 等。它已 deprecated，页面称其即将进入 sunset 且不再加入新功能，并提供升级入口。其 Prompt / Tools 段落属于 Legacy 配置，不能拿来说明当前 Studio widget 内仍有同样的独立配置真值。[同页 Legacy 段落](https://www.palantir.com/docs/foundry/workshop/widgets-aip-chatbot/#base-configuration-legacy)

**建议：** EOS 若提供同类 widget，应把“助手配置版本”和“页面绑定配置”分别建模。页面只引用助手版本和映射，而不是把系统提示词、工具定义再复制一份到 widget DSL。页面升级与助手发布也应分别验收。这是研究建议，不是对 Palantir 内部 DSL 的推断。

## 3. application state 与 conversation state 是两种状态

### 3.1 数据桥接的时点

Studio 当前支持 string 和 ObjectSet application variables；可映射同类型 Workshop 变量。变量描述帮助模型理解用途，但“模型能否直接看变量值”与“该变量可否用于检索 / 工具输入”可分别配置。ObjectSet 可供检索或对象查询起点；动态提示词字符串需要模型可见。[Application state](https://www.palantir.com/docs/foundry/chatbot-studio/application-state/)

确定性输出可来自 Object query tool、function-backed context 或 Ontology context：Studio 记录最新输出，待 LLM 流结束再更新映射变量。Action / Function 的确定性输入取推理循环开始时的变量值；同一 query 内前序工具修改不会反映到这些已固定输入。模型决定更新的另一入口是 Update application variable tool。点击对象 citation 还可把相应对象放入配置的静态 ObjectSet。[同页更新机制](https://www.palantir.com/docs/foundry/chatbot-studio/application-state/#update-application-variables-with-chatbots)

**架构解释：** “先查得目标，再写 application variable，再执行使用该变量的 Action”在同一轮不自动构成预期依赖链。若 Action 输入配置为确定性变量，它仍取初值。应把查询到的结果作为工具输出直接用于后续工具动态参数，或分两轮确认并重新采样变量；具体采用哪种方案还应按权限、提示词、工具定义实测。application state 回填也不能被称为后端事务已提交或所有下游 widget 已完成重算。

### 3.2 状态域对照

| 状态 | 真值与边界 | 不应混称为 |
|---|---|---|
| Workshop 变量、筛选和选择 | 宿主应用业务上下文，经显式映射进入 Chatbot | 完整聊天历史或持久化业务写入 |
| Chatbot application state / API parameters | 每轮输入与可更新结构化输出 | 后端权限的替代品 |
| Chatbot session / exchanges | 与 Chatbot 版本关联的多轮会话记录 | 页面全部运行状态快照 |
| Commands 的目标应用状态 | 配对客户端可访问的当前应用状态 / 屏幕 | 任意后台工具可读取的环境 |
| Workshop 版本与 state saving | 配置发布与用户显式保存运行变量是分别的能力 | 自动保存全部 Chatbot session |

前四行依据 [Application state](https://www.palantir.com/docs/foundry/chatbot-studio/application-state/)、[API session / content](https://www.palantir.com/docs/foundry/chatbot-studio/foundry-apis/)、[Commands](https://www.palantir.com/docs/foundry/cross-app-interactivity/commands-overview/) 归纳；最后一行沿用已公开 [Workshop 数据 / 版本附录](../workshop-runtime-2026-10/data-actions-versioning.md#3-保存版本发布和用户状态应分开说明)，不代表本次重测 Workshop 或 EOS。

## 4. Commands 是客户端能力通道

Commands 让生产方应用声明可执行的客户端操作，供自身、其他 Palantir 应用、工作区组件或 Chatbot 调用。它们在用户应用中执行，能接触当前状态和屏幕；官方例子包括地图位置和地图标注。Workshop 的 Button Group、Metric Card、App Pairing 可触发 Commands，后者还可在变量更新时触发；可把 command 的输出映射到 Workshop 变量。[Commands overview](https://www.palantir.com/docs/foundry/cross-app-interactivity/commands-overview/)

Chatbot 需选取应用已声明 / 提供的 Command；它不是向任意 UI 发送自然语言点击指令。Command tool 可补说明，参数可由模型决定、固定值或 application variable 提供，也可省略可选参数。**工具配置仍是 Beta。** 默认启用执行前审批，用户审阅 payload 后批准 / 拒绝；可关闭该配置。含 Commands 工具的 Chatbot 会话 retention 自动设为闲置 24 小时到期。[Use commands as tools](https://www.palantir.com/docs/foundry/chatbot-studio/commands-as-tools/)

Studio 测试时可与另一个窗口的应用配对，也可形成多应用实例 pairing group。Assist 选择该 Chatbot 后自动与目标应用配对；Workshop 中 Chatbot widget 与 iframe 嵌入应用可自动配对。未配对或多目标时存在目标选择。Chatbot 作为 Function 在不支持 Commands 的环境执行，例如 Automate，会忽略 Commands 工具。[Commands 的配对与部署](https://www.palantir.com/docs/foundry/chatbot-studio/commands-as-tools/#embed-your-chatbot-in-aip-assist-or-workshop)

### 4.1 审批、执行位置、授权不可合并

| 通道 | 执行位置与输入 | 人工确认 | 权限边界 |
|---|---|---|---|
| application variable 回填 | 宿主映射；确定性或模型决定更新 | 该配置本身不是业务写入审批 | READ_ONLY / READ_WRITE 和 value visibility 只限制变量交互 |
| Command | 已配对的应用客户端；声明的 payload | 默认审批，可配置关闭 | 它在目标应用内执行；是否进一步调用业务 API 由具体操作决定 |
| Action tool | 后端 Action；模型或确定性输入 | Studio 的 Action confirmation 配置应单独查验 | Action 服务仍检查实际提交条件、对象 / 数据源编辑授权和副作用权限 |
| Function tool / retrieval | 配置的后端计算 / 检索 | 按工具契约讨论 | 不能借客户端变量或按钮可见性代替资源与执行权限 |

Action 的后端边界有直接公开 [Action type permissions](https://www.palantir.com/docs/foundry/action-types/permissions/)、[Submission criteria](https://www.palantir.com/docs/foundry/action-types/submission-criteria/) 支持；本表不把 Command payload 审批解释为这些服务授权的豁免，也不宣称任何具体 Command 都没有后端副作用。Studio Action 确认的产品细节由工具 / 治理附录承担。

### 4.2 自建 React 的 Commands 生产协议仍需核验

本次所读公开 Commands overview 主要说明消费者配置和 Palantir 应用配对，未提供足以复现“任意 React 应用注册 Command producer”的完整公开类型、握手 / 发现、跨 origin 校验、目标实例路由或错误协议。不能仅凭“pro-code language”就写出自定义 `registerCommand` API，也不能把 Workshop Custom Widget 参数事件协议当成 Commands 协议。OSDK 客户端可执行后端读写并不自动证明该 React 应用能参与 App Pairing。后续必须从官方可用 SDK / 租户帮助核验生产者入口。

## 5. 当前公开 API 的名字仍保留 aipAgents

产品名已从 Agent Studio 改为 Chatbot Studio，但公开 API reference、RID 和 Platform SDK 继续使用 `aipAgents`、`agentRid`、`agentVersion`、`parameterInputs` 等字段。调用时应保留原标识，正文称其为 Chatbot 会话 API，并明确这是兼容名称，不把 Agent API 泛指 AI FDE 等其他 agent。[产品更名](https://www.palantir.com/docs/foundry/chatbot-studio/overview/)、[Foundry APIs](https://www.palantir.com/docs/foundry/chatbot-studio/foundry-apis/)

SDK 核对基线：

| 公开仓库 | 固定提交 | 本次读取版本 |
|---|---|---|
| [foundry-platform-typescript](https://github.com/palantir/foundry-platform-typescript/tree/4320149c31bcbcc2d176564d9259e343d9702d2b) | `4320149c31bcbcc2d176564d9259e343d9702d2b` | [@osdk/foundry.aipagents 2.82.0](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/package.json#L2-L3) |
| [osdk-ts](https://github.com/palantir/osdk-ts/tree/dec2ee4b637a23e1b7e56fb0f50599386301c930) | `dec2ee4b637a23e1b7e56fb0f50599386301c930` | [@osdk/client 2.75.0](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/client/package.json#L2-L3) |

### 5.1 路由与操作

所有下表 Sessions API 在官方 reference 当前标为 **preview**，请求需 `preview=true`；SDK 方法标 `@beta`。表中 `{base}` 是 `/api/v2/aipAgents/agents/{agentRid}`。这两种状态标记来自不同发布面，不表示已达 GA。[Create Session](https://www.palantir.com/docs/foundry/api/aip-agents-v2-resources/sessions/create-session)、[SDK Session.ts](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/Session.ts#L32-L58)

| 能力 | REST 操作 | SDK 表面 / 返回类型 | OAuth operation scope |
|---|---|---|---|
| 创建 | POST `{base}/sessions` | `Sessions.create` → `Promise<Session>` | `api:aip-agents-write` |
| 元数据 | GET `{base}/sessions/{sessionRid}` | `Sessions.get` → `Promise<Session>` | `api:aip-agents-read` |
| 列表 | GET `{base}/sessions` | `Sessions.list` → `Promise<ListSessionsResponse>` | `api:aip-agents-read` |
| 完整响应 | POST `.../{sessionRid}/blockingContinue` | `Sessions.blockingContinue` → `Promise<SessionExchangeResult>` | `api:aip-agents-write` |
| 文本流 | POST `.../{sessionRid}/streamingContinue` | `Sessions.streamingContinue` → `Promise<Response>` | `api:aip-agents-write` |
| 取消流式轮次 | POST `.../{sessionRid}/cancel` | `Sessions.cancel` → `Promise<CancelSessionResponse>` | `api:aip-agents-write` |
| 会话交换内容 | GET `.../{sessionRid}/content` | `Contents.get` → `Promise<Content>` | `api:aip-agents-read` |
| 预检索 | PUT `.../{sessionRid}/ragContext` | `Sessions.ragContext` → `Promise<AgentSessionRagContextResponse>` | `api:aip-agents-write` |
| 删除会话 / 更新标题 | DELETE `.../{sessionRid}` / PUT `.../{sessionRid}/updateTitle` | `deleteSession` / `updateTitle` → `Promise<void>` | `api:aip-agents-write` |
| trace | GET `.../{sessionRid}/sessionTraces/{sessionTraceId}` | `SessionTraces.get` → `Promise<SessionTrace>` | `api:aip-agents-read` |

逐项路由与 scopes 来自固定 [Session.ts](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/Session.ts#L32-L317)、[Content.ts](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/Content.ts#L32-L57)、[SessionTrace.ts](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/SessionTrace.ts#L32-L61)。Sessions.list 明确仅列出调用用户由该 client 创建的会话，不包含由其他 client / Studio 创建的用户会话；因此“我的会话列表”不等于平台全部聊天记录。[list 方法注释](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/Session.ts#L100-L123)

### 5.2 精确 TypeScript 契约

下面把上下文类型简称为 `Ctx`，它实际允许新 / 旧版 SharedClient 或 SharedClientContext；除此处简称外保留实际参数顺序和返回类型。导入表面是 `@osdk/foundry.aipagents` 的 `Sessions`、`Contents`、`Agents`、`SessionTraces`，根导出指向 v2。[导出源码](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/index.ts)

```ts
Sessions.create(ctx: Ctx, agentRid: AgentRid,
  body: CreateSessionRequest, query?: { preview?: PreviewMode }): Promise<Session>
Sessions.blockingContinue(ctx: Ctx, agentRid: AgentRid, sessionRid: SessionRid,
  body: BlockingContinueSessionRequest,
  query?: { preview?: PreviewMode }): Promise<SessionExchangeResult>
Sessions.streamingContinue(ctx: Ctx, agentRid: AgentRid, sessionRid: SessionRid,
  body: StreamingContinueSessionRequest,
  query?: { preview?: PreviewMode }): Promise<Response>
Sessions.cancel(ctx: Ctx, agentRid: AgentRid, sessionRid: SessionRid,
  body: CancelSessionRequest,
  query?: { preview?: PreviewMode }): Promise<CancelSessionResponse>
Contents.get(ctx: Ctx, agentRid: AgentRid, sessionRid: SessionRid,
  query?: { preview?: PreviewMode }): Promise<Content>
```

签名直接核对 [create](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/Session.ts#L49-L58)、[blockingContinue](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/Session.ts#L176-L186)、[streamingContinue](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/Session.ts#L217-L227)、[cancel](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/Session.ts#L248-L258)、[content](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/Content.ts#L48-L57)。这段是契约展示，不能直接作为独立 TS 源文件编译。

输入值不是任意 JSON 或字符串：`userInput` 为 `{ text: string }`；string parameter 的形状是 `{ type: "string", value: string }`。ObjectSet parameter 的输入包含 `{ type: "objectSet", objectSet, ontology }`；输出为 `{ type: "objectSet", value: ObjectSetRid }`。其中 `objectSet` 是平台定义的判别联合，而非浏览器 OSDK ObjectSet builder 可直接 JSON.stringify 的保证；例如合法引用形式为 `{ type: "reference", reference: objectSetRid }`。[Parameter types](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L229-L301)、[StringParameterValue](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L431-L433)、[ObjectSet wire union](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.ontologies/src/v2/_components.ts#L4407-L4424)

官方 REST 页将 `parameterInputs` / `parameterUpdates` 标为 optional；固定 SDK 的 request / result interface 将它们定义为必填 `Record`。SDK 示例应至少传 `{}`，而不是据 REST 页省略后声称 TS 编译通过。自建适配层还应能承受 REST 响应中 map 缺省的情形。这是文档与生成类型差异，未证明服务真实返回习惯。[Blocking REST](https://www.palantir.com/docs/foundry/api/aip-agents-v2-resources/sessions/blocking-continue-session)、[SDK request](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L112-L117)、[SDK result](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L357-L363)

### 5.3 会话版本、上下文覆盖与 trace

CreateSessionRequest 可指定 `agentVersion`；省略时取**创建会话当时**最新已发布版本。Session 记录该版本，所以已创建会话不应按“每轮追最新”设计。输入变量 ID / 类型问题应结合此 session 的版本，用 `Agents.get(..., { version, preview: true })` 读取 `parameters` 校验；只对比当前 Studio 最新配置可能产生误诊。[Create Session](https://www.palantir.com/docs/foundry/api/aip-agents-v2-resources/sessions/create-session)、[Agent schema](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L28-L33)、[InvalidParameter / InvalidParameterType](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_errors.ts#L284-L321)

`contextsOverride` 指定后跳过自动检索，直接用给定 context；`ragContext` 可先取得已配置来源的相关内容供客户端预处理，然后再覆盖送入。它不是额外叠加模式，空数组与省略字段不能擅自视为相同。每轮可由客户端生成 UUIDv4 `sessionTraceId` 并在生成中轮询 trace；trace schema 包括检索 contexts 和 tool call groups，状态为 `IN_PROGRESS | COMPLETE`。[Blocking 请求](https://www.palantir.com/docs/foundry/api/aip-agents-v2-resources/sessions/blocking-continue-session)、[ragContext 源码](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/Session.ts#L260-L287)、[Trace schema](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L388-L406)

## 6. 流式响应、取消与失败恢复

blockingContinue 与 streamingContinue 都不支持同一 session 的并发 continue。客户端应等待当前响应，或取消在途的流式 exchange 后再发送下一条。SDK streamingContinue 指定 Accept `application/octet-stream`，返回浏览器 / Fetch `Response`；它不是现有 SDK 的 SSE 事件数组接口。SDK 网络层确实另有 `text/event-stream` 解析分支，但该 Chatbot 方法没有采用它。[Streaming reference](https://www.palantir.com/docs/foundry/api/aip-agents-v2-resources/sessions/streaming-continue-session)、[streaming 方法媒体类型](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/Session.ts#L188-L227)、[网络层返回方式](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/shared.net.platformapi/src/foundryPlatformFetch.ts#L176-L184)

流仅提供生成的 Markdown 文本。流结束后必须再取 `Contents.get`，才能读取完整 exchange 的 application variable updates、trace ID、token 等结构化结果。`SessionExchangeResult` 还有 `interruptedOutput`；它与 HTTP 流正常结束应分别记录。[Foundry APIs](https://www.palantir.com/docs/foundry/chatbot-studio/foundry-apis/)、[SessionExchangeResult](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L336-L363)

取消需要在 streamingContinue 请求中预先传客户端 UUID `messageId`，再调用 cancel 并传相同 ID。省略 `response` 时，该 exchange 不加入会话；提供 `response` 时，用客户端响应替换模型响应并加入会话。cancel **不会关闭原来的流**，客户端应另外停止读取 / 关闭流。reference 没有承诺已执行的 Action 或外部副作用随 cancel 回滚，所以不能把聊天停止按钮写成事务撤销。[Cancel Session](https://www.palantir.com/docs/foundry/api/v2/aip-agents-v2-resources/sessions/cancel-session/)

取消可能与 exchange 尚未启动、已结束或已取消竞态，返回 `CancelSessionFailedMessageNotInProgress`；源码建议平稳处理并重读 content。其他已公开失败包括输入变量 / 类型不匹配、上下文超限、推理轮数上限、模型限流、重试次数 / deadline 耗尽，以及 session 不存在。它们应有分别的恢复策略，不能统一为“重新发一次原消息”。[取消竞态](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_errors.ts#L112-L131)、[错误 schema](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_errors.ts)

**建议状态机：** `idle → sending → streaming / waiting → reconciling → idle`；`cancelRequested` 必须同时处理服务取消和读流关闭；`unknownOutcome` 分支先恢复会话及业务状态，再决定是否可重试。这是自建客户端建议，不是 Palantir 公布的内部状态机。

## 7. React / OSDK 的最小可核验接入

### 7.1 配置前提

官方要求用 OSDK 应用接 Chatbot 时，它所用 object / action / function types 来自单一 Ontology。Developer Console 应用需选择 application state、tool、retrieval context 所需全部 types；Platform SDK 中添加 Chatbot 项目及其他 filesystem 资源所在项目；开放 AIP Chatbots allowed operations。新增资源不会自动同步到 Developer Console，需显式更新。[Use AIP Chatbots through Foundry APIs](https://www.palantir.com/docs/foundry/chatbot-studio/foundry-apis/#deploy-an-aip-chatbot-to-a-developer-console-application)

OSDK `Client` 继承新旧 SharedClient；createClient 将两种 client-context 表面映射到同一个上下文。因此可把该 client 传入上述 Platform SDK 方法，同时继续使用生成的 Ontology 对象 / Action / Function 定义。这是源码直接支持的适配，不代表全部 SDK 版本之间无条件兼容。[Client 接口](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/client/src/Client.ts#L35-L54)、[createClient 上下文映射](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/client/src/createClient.ts#L383-L398)、[Platform SDK 取上下文](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/shared.net.platformapi/src/foundryPlatformFetch.ts#L78-L88)

仅调用 Platform APIs 时，当前 OSDK 还导出 `createPlatformClient(baseUrl, tokenProvider, options = undefined, fetchFn = fetch): PlatformClient`，不需要 Ontology RID。其源码注释明确已有 createClient 的应用无需再建一个 platform client。这个构造选择不会改变 Chatbot 服务的 scopes、Developer Console 资源配置或实际授权。[createPlatformClient](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/client/src/createPlatformClient.ts#L22-L38)

浏览器入口可用 `createPublicOauthClient` 的 options 形式，再把它当 tokenProvider 交给 createClient。默认 OAuth scopes 的源码列表不含 `api:aip-agents-read / write`，应按所用 endpoint 显式添加需要的 Chatbot scopes，并保持应用实际需要的其余 scopes。只改客户端请求 scopes 不能代替 Developer Console allowed operations 和资源权限。[OAuth options / 默认 scopes](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/oauth/src/createPublicOauthClient.ts#L55-L79)、[OAuth signature](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/oauth/src/createPublicOauthClient.ts#L123-L128)、[createClient signature](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/client/src/createClient.ts#L442-L464)

### 7.2 最小 blocking 调用序列

这段放在 React 界面背后的 service 模块即可；`auth` 与 `client` 可复用应用已有实例。占位 ID 需替换为已发布 Chatbot、真实版本和变量 ID。返回值需由应用绑定器回填已知变量；示例返回结构化结果，不把 Markdown 字符串当成业务命令执行。

```ts
import { createClient } from "@osdk/client";
import { createPublicOauthClient } from "@osdk/oauth";
import { Agents, Contents, Sessions } from "@osdk/foundry.aipagents";

const baseUrl = "https://YOUR-STACK.palantirfoundry.com";
const auth = createPublicOauthClient(
  "YOUR-PUBLIC-CLIENT-ID", baseUrl,
  `${window.location.origin}/auth/callback`,
  { scopes: ["api:aip-agents-read", "api:aip-agents-write"] },
);
const client = createClient(baseUrl, "YOUR-ONTOLOGY-RID", auth);

export async function startChatbotTask(agentRid: string, agentVersion: string) {
  const session = await Sessions.create(
    client, agentRid, { agentVersion }, { preview: true },
  );
  const configuration = await Agents.get(
    client, agentRid, { version: session.agentVersion, preview: true },
  );
  // 查看 configuration.parameters，按真实 ID、类型、access 验证映射。
  const result = await Sessions.blockingContinue(
    client, agentRid, session.rid,
    {
      userInput: { text: "汇总当前任务的关键信息" },
      parameterInputs: {},
      sessionTraceId: crypto.randomUUID(),
    },
    { preview: true },
  );
  return { session, configuration, result };
}
```

此示例只演示 Chatbot read / write endpoint 的 scopes；真实 Chatbot 若使用 Ontology 或其他资源，须依据 Developer Console 配置与官方授权指南补齐应用所需 scopes 和资源。变量输入可写成 `parameterInputs: { [真实变量ID]: { type: "string", value: 当前选择的业务上下文 } }`。上述方法和形状已对照固定 SDK；本次未安装依赖、未编译示例、未执行 auth / API，故“最小可核验”是后续可复现实验入口，不是运行通过声明。

### 7.3 streaming 需要多一步 reconcile

最小次序为：保存 sessionRID 与本轮 UUID `messageId` / `sessionTraceId` → streamingContinue → 从 Response.body 逐块读取并累计 Markdown → 正常完成后 Contents.get → 找到本轮完整 exchange 并处理 parameterUpdates / interruptedOutput → 释放发送锁。不要假定一个网络 chunk 对应一个 token、句子或完整字符；文本解码应使用流式 TextDecoder。[Streaming reference](https://www.palantir.com/docs/foundry/api/aip-agents-v2-resources/sessions/streaming-continue-session)、[Content schema](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L137-L139)

示意代码只展示原始 API 接线；沿用上一例的 `Agents` / `Contents` / `Sessions` 导入，UI 更新、重试、发送互斥和组件卸载处理留给客户端实现。完整内容应以本轮 `sessionTraceId` 匹配 `exchange.result.sessionTraceId`；`messageId` 用于取消，该固定版本的 Content / SessionExchange 没有对应 `messageId` 字段，不能用它定位 exchange。[Exchange 与 result schema](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L336-L363)

```ts
import { Contents, Sessions } from "@osdk/foundry.aipagents";

const messageId = crypto.randomUUID();
const sessionTraceId = crypto.randomUUID();
const response = await Sessions.streamingContinue(
  client, agentRid, sessionRid,
  {
    userInput: { text: userText },
    parameterInputs: {},
    messageId, sessionTraceId,
  },
  { preview: true },
);
const reader = response.body?.getReader();
if (!reader) throw new Error("Missing response body");
const decoder = new TextDecoder();
let markdown = "";
for (;;) {
  const { done, value } = await reader.read();
  if (done) break;
  markdown += decoder.decode(value, { stream: true });
}
markdown += decoder.decode();
const content = await Contents.get(
  client, agentRid, sessionRid, { preview: true },
);
const exchange = content.exchanges.find(
  item => item.result.sessionTraceId === sessionTraceId,
);
if (!exchange) throw new Error("本轮 exchange 未找到；保留待恢复状态");
const result = exchange.result;
// 分别处理 result.parameterUpdates / interruptedOutput / agentMarkdownResponse。
```

用户停止时对同一 `messageId` 调用 `Sessions.cancel`，并关闭 reader；二者应纳入同一取消流程。代码未提供已经执行的工具副作用撤销。当前 SDK 的 continue 方法签名没有标准 AbortSignal 参数，网络层也没有在这些方法参数中接收 signal，因此不要编写 `Sessions.streamingContinue(..., { signal })` 并声称官方支持。若应用另用 Fetch 或自定义网络包装，应按其实际接口核验，不能替代服务 cancel。[方法签名](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/public/Session.ts#L217-L227)、[fetch 构造](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/shared.net.platformapi/src/foundryPlatformFetch.ts#L118-L143)

### 7.4 没有公开的“暂停后批准再恢复” Session API 契约

本次对固定 aipagents v2 schema 与 Session 方法逐项读取并检索，BlockingContinueSessionRequest / StreamingContinueSessionRequest 未见 `confirmation`、`approval`、Command invocation result、`paused` 或 `resume / continuation` 字段；result 是 Markdown、parameterUpdates、token、interruptedOutput、traceID。工具 trace 不是可写回的批准协议。这只能支持“上述公开版本未给出这套协议”，不能证明 Palantir 内部 / 未来 / 其他 SDK 永远没有。[request schema](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L112-L125)、[streaming schema](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L411-L417)、[result schema](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L357-L363)

因此不能把 Workshop / Assist 中 Command 审批 UI 平移为自建 React 已获支持的 `approveToolCall` API。需要人工审批的业务流程可先设计为明确分两轮的“提议 → 用户选择 / 修改 → 已授权业务 Action”，但是否可安全使用同一 Chatbot 的工具配置需真实租户验证。工具提交权限、用户确认以及会话取消应有独立状态和审计证据。

### 7.5 公开 AipAgentChat 组件目前接 LMS，不能凭名字当作 Studio 适配器

OSDK 源码存在 `@osdk/react-components/experimental/aip-agent-chat` 的 `AipAgentChat`。当前实现以 PlatformClient 和 model API name 构造 `foundryModel`，再调用 `useChat`；它接 Foundry Language Model Service，不传 Chatbot RID、sessionRID 或 application parameters，也没有使用上述 Sessions API。[组件接线](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/react-components/src/aip-agent-chat/AipAgentChat.tsx#L17-L86)、[props](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L42-L53)

`useChat` 的源码说明其 v0 只覆盖文本聊天，不支持 tools、多步骤 agent loops 或流恢复；默认 transport 是 LmsChatTransport，可覆盖为自定义 transport。`stop` 通过 transport 的 abortSignal 管理文本流，与 Chatbot Sessions.cancel 的服务语义不是同一接口。[useChat 契约](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/react/src/aip/useChat.ts#L40-L108)、[传输调用](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/react/src/aip/chatStream.ts#L45-L65)

可复用 UI 的候选是 `BaseAipAgentChat`：它接受 messages / status / error，以及 onSendMessage / onStop / onClearError；应用可自行把 Sessions API 结果映射为 UIMessage。这是基于 props 的集成方案，不是官方已提供 / 已测试的 Studio transport。当前 AipAgentChat wrapper 测试仍为 `it.todo`；useChat 有 mock transport 的文本流、错误、停止等测试，也不能证明 Studio 工具 / 权限接线。[Base props](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L29-L84)、[wrapper tests](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/react-components/src/aip-agent-chat/__tests__/AipAgentChat.test.tsx#L19-L31)、[useChat tests](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/react/src/aip/useChat.test.tsx)

以上重新核对固定公开源码，与既有 [OSDK React Components 专题](../osdk-react-components-2026-09/README.md) 的 LMS 边界相符；不复用其模拟聊天截图作为本专题真实 Studio Chatbot 运行证据。

## 8. Chatbots as Functions：不是另一套裸模型 API

发布 Function 后，输入包括 `userInput`、可选 `sessionRid` 和全部 application variables；省略 sessionRID 创建新会话，不能用空字符串代替。输出包括 `markdownResponse`、sessionRID 及有更新的 application variables；未更新变量为空。ObjectSet 默认值是该类型 base ObjectSet，因此遗漏输入可能扩大检索范围，须显式验收。[Chatbots as Functions](https://www.palantir.com/docs/foundry/chatbot-studio/chatbots-as-functions/#function-inputs)

Function 可随 Chatbot 每次发布生成版本，也可配置保存时生成 minor Function versions；用于 AIP Evals、Automate、Code Repositories 或第三方 OSDK Function 调用。OSDK 对生成的 QueryDefinition 通过 `client(definition).executeFunction(params)` 执行，具体参数签名来自生成 SDK，不能凭本文占位 Function 名称构造兼容保证。[发布设置](https://www.palantir.com/docs/foundry/chatbot-studio/chatbots-as-functions/#publish-a-chatbot-as-a-function)、[Client query 表面](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/client/src/Client.ts#L105-L113)、[QuerySignatureFromDef](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/client/src/queries/types.ts#L32-L43)

Function 发布版、Chatbot 已发布版与 OSDK 生成版本是三个分别核查的产物。Commands 在无客户端支持环境中忽略的限制也保留；Function 方式不能替代客户端地图操作。对单轮任务它减少应用会话编排，对多轮任务则需传回 sessionRID 并处理变量更新。以上是选型解释，不宣称性能优于 Sessions API。

## 9. 公开测试证明了什么

所读 Platform SDK 的 `foundryPlatformFetch.test.ts` 测试的是 URL 组装，包括无末尾 slash、含 context path 等；本次在 aipagents 包中没有发现具体 Chatbot Session test 文件，仅有 vitest 配置。OSDK 的 createClient 测试覆盖 URL 格式化和客户端请求 metadata；query 测试用 faux Foundry 验证 executeFunction，包括简单函数以及参数类型示例。这些公开测试证明维护者对基础客户端契约有测试资产，不能当成真实 Chatbot 工具链、权限或租户端性能验收；本次也没有运行这些测试。[Platform URL 测试](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/shared.net.platformapi/src/foundryPlatformFetch.test.ts#L20-L60)、[OSDK createClient 测试](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/client/src/createClient.test.ts#L120-L156)、[OSDK query 测试](https://github.com/palantir/osdk-ts/blob/dec2ee4b637a23e1b7e56fb0f50599386301c930/packages/client/src/queries/queries.test.ts#L67-L106)

### 9.1 相关 PR 的历史语义

| 公开已合并 PR | 可追溯变化 | 本题如何使用 |
|---|---|---|
| [OSDK #320：Foundry SDK Improvements](https://github.com/palantir/osdk-ts/pull/320)，2024-05-14 | 平台 SDK 接受 OSDK client；拆分 legacy / SharedClientContext；tokenProvider 2.0 转向 Promise | 解释共享客户端是正式公开适配设计；当前契约仍以固定代码为准 |
| [OSDK #380：Introduce createPlatformClient](https://github.com/palantir/osdk-ts/pull/380)，2024-06-07 | 增加仅 Platform APIs 的客户端构造 | 没有生成 Ontology SDK 时的客户端选项；不表示绕过资源授权 |
| [OSDK #3932：streaming queries w/ SSE](https://github.com/palantir/osdk-ts/pull/3932)，2026-08-24 | 恢复 Function queries 的 SSE 流式执行 | 不应把这一变化推到 Chatbot streamingContinue；后者当前仍是 octet-stream Response |

历史 PR 与代码使协议选择可追溯，但 PR 作者所述的本地端到端验证不是本次研究执行的验证。也不能从名称含 `Agents` 的新命名空间变更反推 `foundry.aipagents` 已迁移；本题调用面按当前导出和实际路由核验。

## 10. EOS 可验证建议与尚未公开的范围

下述建议仅与已公开 [EOS 历史基线](../workshop-runtime-2026-10/eos-comparison/README.md) 对照；该稿有静态读取日期、固定 HEAD 和未运行后端 / 部署的边界，本次不把其中“当前”扩展为新的实测。

| 建议 | 可验证实验 / 验收证据 | 为什么要测 |
|---|---|---|
| 复用既有变量 / 事件接口，建立助手专用映射 | 选中对象后发消息；助手更新结果集合；引用点击更新单对象；验证不同页面实例互不串扰 | UI 业务 state 和对话 state 分域；ObjectSet 与 string wire 形状不同 |
| 记录每轮 state snapshot / version | 同轮先修改变量再调用固定输入工具；下一轮再次调用；对比输入与回填时点 | 初值固定可与用户以为的依赖链不同 |
| 单 session 发送互斥，跨标签也考虑冲突 | 在生成中重复发送；第二标签发送；cancel 尚未开始 / 已结束；reload content 恢复 | 公共 API 禁同会话并发；取消有竞态 |
| 把 UI Command 与业务写 Action 分为两类工具 | 导航 / 地图缩放无需业务事务；创建对象必须单独校验权限、确认与结果 | 当前应用客户端能力和后端提交不能共用一个“执行成功”语义 |
| 建立三份权限证据 | OAuth endpoint scope；应用 allowed operations / resource coverage；执行用户资源与 Action 授权 | 配置工具可见或变量 READ_WRITE 不代表后端可写 |
| 按明确发布产物升级 | 新 Chatbot 版本加入 tool / resource，旧 session续聊；新session按显式版本创建；Console资源补齐 | 会话版本与资源许可不会自动随最新配置统一迁移 |
| 流结束后统一 reconcile | 正常流、被中断流、客户端取消和网络断开，核对 exchange / application output / business effect | 文本流不携带全部结果；cancel不等于副作用回滚 |
| 先做已声明 Command 的可控验证 | 目标实例选择、默认审批 / 关闭审批、拒绝、iframe隐藏、页面卸载、多应用配对 | 不应在生产者协议未确认时宣称任意React已支持 |

这些是候选实验，尚未执行。现有公开证据不足以确定：自定义 React Command producer 的完整注册协议；第三方 Session API 交互式审批 / 暂停恢复协议；普遍 Chatbot 会话的统一保留时长（metadata 只给 estimatedExpiresTime，含 Commands 的 24 小时规则不应外推）；Workshop widget 卸载 / 页面切换与 Studio session 持久化的完整关系；断流时已执行工具的统一回滚 / 幂等规则；全部 enrollment 的具体功能版本和模型时延。应保留为未知或按租户实测，而不是补出内部机制。[Session metadata schema](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.aipagents/src/v2/_components.ts#L370-L376)
