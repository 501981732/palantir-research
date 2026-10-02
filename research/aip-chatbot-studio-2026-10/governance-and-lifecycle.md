# AIP Chatbot Studio 治理、评估、发布与产品边界

> 治理、生命周期与产品边界附录。检索日期：2026-10-01（UTC）。本轮直接阅读公开文档、API 文档和具名社区讨论，没有登录 Foundry 租户，没有执行 Chatbot、Action、Function、Evals、发布或 Marketplace 安装。没有读取新的 EOS 内部代码或公司资料。技术事实来自下列直接链接；EOS 项目建议均为待验证设计。完整来源元数据见 [governance-sources.json](notes/governance-sources.json)。

## 1. 治理结论：配置助手也要配置执行合同

AIP Chatbot 是带企业上下文和工具的交互助手；Chatbot Studio 是它的构建与发布入口，助手既可在 Foundry 应用内使用，也可经 OSDK 和平台 API 对接自建应用。旧名称 Agent Studio / AIP Agents 仍残留于 API 路径、RID 和日志字段中；不能把名称里的 Agent 等同于 AI FDE 或 Evolve 的工程工作流。官方概览支持应用中的读写工作流，并声明复用平台安全模型。[Chatbot Studio 概览](https://www.palantir.com/docs/foundry/chatbot-studio/overview)

对架构负责人最重要的不是“聊天框有没有确认按钮”，而是把六份合同同时讲清楚：谁能访问助手和资源；哪些数据可发给所选模型；工具在哪里、以什么身份执行；哪些操作要用户确认且如何满足业务写规则；执行和结果怎样观察、保留与保护；哪个版本和依赖被交付给哪个消费者。这是本文分析。当前文档并没有给 Chatbot Studio 公开一个覆盖全部工具、宿主、Function 消费与保留模式的统一审批或分支合同，因此不能从其他产品补齐这一合同。

| 治理层 | 已确认的产品行为 | 对 EOS 的设计含义（分析） |
| --- | --- | --- |
| 助手资源 ACL | Chatbot 是有细粒度访问控制的 Foundry 文件系统资源 | 助手配置本身应具备资源 ID、归属、读/编辑权限；应用可见性不足以授权全部依赖 |
| 模型可用性与数据通道 | 模型取决于 enrollment 开启与用户访问；模型 Markings 策略检查请求 token 的 mandatory Markings | 选择模型时同时展示数据发送政策；不能只按记录标签判断能否发送 |
| 工具与执行范围 | 后端 Action / Function 与运行在用户应用里的 Command 是不同路径 | 注册工具时声明执行位置、权限来源、写入与外部副作用，不以“Function”标签假定只读 |
| 确认与提交 | Action 工具可自动或确认后执行；Command 配置默认要求审批，可关；Action 仍需 submission criteria、对象访问及相应写入授权规则 | UI 确认只决定用户是否接受所提议操作，后端仍独立检查权限和业务约束 |
| 观察与记录 | Chatbot 可导出结构化执行事件；日志访问与原业务数据权限分开治理 | 日志要有专门的敏感度、查看权限与保留策略，不当低敏统计表 |
| 版本与分发 | Save、View 指定版本、Publish；Function 版本与 Marketplace 产品另有交付机制 | 发布记录至少包含 Chatbot 版本、工具版本、知识依赖和消费应用声明 |

上述各层事实分别依据 [Getting started](https://www.palantir.com/docs/foundry/chatbot-studio/getting-started)、[Tools](https://www.palantir.com/docs/foundry/chatbot-studio/tools)、[Commands](https://www.palantir.com/docs/foundry/chatbot-studio/commands-as-tools)、[Session logging](https://www.palantir.com/docs/foundry/chatbot-studio/session-logging)、[模型 Markings 政策](https://www.palantir.com/docs/foundry/aip/control-llm-data-access-with-markings)。

## 2. 身份、资源访问与模型数据边界

### 2.1 访问助手不是访问它的全部依赖

Chatbot 是文件系统资源，保存位置决定其权限边界。在通过 Assist 部署自定义知识助手的教程中，官方明确要求使用者对 Chatbot 保存位置有读取权，同时能访问背后的 custom content source；使用者还应有所选模型的访问权限。教程还提醒“注册内容源”只让内容可被发现，并不会自动改变 Assist 或其他 Chatbot 的行为，仍需构建并部署使用它的 Chatbot。[Chatbot 创建](https://www.palantir.com/docs/foundry/chatbot-studio/getting-started#create-an-aip-chatbot)、[Deploy AIP Chatbots to AIP Assist](https://www.palantir.com/docs/foundry/assist/agents-in-aip-assist)

自建应用还多一层客户端约束：Developer Console 要选择单一 Ontology 中 Chatbot 使用的所有对象、Action 与 Function 类型；这些应覆盖 state、tools、retrieval context。Platform SDK 需添加 Chatbot 所属 Project，以及其他媒体资源所属 Project，开启所需 AIP Chatbot API 操作。新添依赖后客户端声明不会自动更新。[Use AIP Chatbots through Foundry APIs](https://www.palantir.com/docs/foundry/chatbot-studio/foundry-apis)

据此可以归纳“助手 ACL × 依赖资源 ACL × 模型数据通道 × 客户端允许的资源和操作 × 工具具体执行模式”的约束面；这是架构归纳，不是 Palantir 公布的统一授权公式。对 EOS，应避免仅把助手绑定到页面角色，然后让一个高权限服务身份执行全部工具。

### 2.2 身份需要按入口和工具核验

API 的 Create Session 明确创建调用者与 Chatbot 之间的会话；OAuth 需要 `api:aip-agents-write`。普通 Foundry API 的授权遵循客户端 scope 与用户或 service user 原有权限的交集：Authorization Code grant 代表用户，Client Credentials grant 代表 service user。两条路径都存在，不应把某个 React 示例的身份选择当成 Chatbot 全部执行的默认。[Create Session](https://www.palantir.com/docs/foundry/api/v2/aip-agents-v2-resources/sessions/create-session)、[API Authentication](https://www.palantir.com/docs/foundry/api/v2/general/overview/authentication)

Function 工具又可以调用 AIP Logic。Logic 当前默认 user-scoped，以运行者权限执行；project-scoped 则使用 Logic 所在 Project 的权限，所有依赖需导入同 Project，用户仍需依赖资源的 Markings。两种模式的日志可见性也不同。这是 **Logic 的明确合同**，不能直接重写为 Chatbot 的统一执行模式。[Logic execution mode settings](https://www.palantir.com/docs/foundry/logic/execution-mode-settings)

普通已发布 Function 执行通常要求用户对来源 repository 有 Viewer；Function-backed Action 是例外，配置者须读 Function，提交者随后按 Action 权限执行，不必有相同 Function 读权。函数加载对象时按执行用户可读对象过滤，但行列读控制不自动保护 Function 输出，下游仍要 Markings / CBAC。平台还对 extended Functions 的发布 repository、运行 Function 与 Marketplace 安装 Project 设管理员 allowlist；其中可包含函数内部调用 Actions 等扩展能力。这些规则再次要求按具体调用路径核验，不能把“能调用外层 Function”推导成任意内层工具已授权。[Function permissions](https://www.palantir.com/docs/foundry/functions/permissions)

Commands 的合同更具体：它们直接在用户的应用中运行，读当前应用状态与屏幕，并代表用户触发应用操作。即使模型选择了命令，实际效果仍依赖目标应用已声明并产生该命令、配对关系和客户端环境。[Commands as tools](https://www.palantir.com/docs/foundry/chatbot-studio/commands-as-tools)

**未证实：** 本轮 Chatbot 专页没有公开证明“所有 Chatbot、所有保留模式、所有 Function/Action 工具都始终以同一最终用户身份执行”的完整合同。AI FDE 的安全专页确有 entirely under your identity 的表述，但这是 AI FDE 的产品合同，本文不移植到 Chatbot。[AI FDE security and governance](https://www.palantir.com/docs/foundry/ai-fde/security-and-governance)

### 2.3 Markings 模型政策按 token 检查，不是只看这次文字

管理员可以为模型设 Allow any data 或 mandatory Markings allowlist。allowlist 要求请求 token 可用的每个 mandatory Marking 都在允许集合内；没有 mandatory Markings 的 token 可通过。若模型允许 A、B，当前会话 token 带 A、C，即使本次消息和取回的数据不带 C，请求也被拒绝。用户可选 scoped session 缩小当前 token 上的 Markings；这不赋予新的数据权限。registered model 的专属政策完全替换 enrollment 政策，可以更严也可以更宽，未配置才继承默认。[Control LLM data access with Markings](https://www.palantir.com/docs/foundry/aip/control-llm-data-access-with-markings)

EOS 建议把“可读业务数据”和“允许发给特定模型”设计成独立策略，并对调用者 token 与模型有效策略留可解释记录。需要验证模型切换、会话 scope 改变和 service identity 这三种变化，而不能仅用脱敏一条消息的测试判定整个通道合规。

Palantir 的 AIP 安全页声明：经 AIP 提供的第三方托管模型不保留 prompts/completions，不用客户内容训练，技术与合同保证在接入模型前取得。这不是 Foundry 自身会话和日志“零存储”的声明，也不能自动覆盖用户另行注册、自行连接的任意外部模型服务；对应的实际合同和部署需分别核验。[AIP security and privacy](https://www.palantir.com/docs/foundry/aip/aip-security)

## 3. 确认、写入与副作用：至少四道独立检查

### 3.1 工具确认是产品配置，不能说所有写入默认审批

Chatbot 的 Action 工具可以自动执行，或在用户确认后执行。Function 工具可调用任意 Foundry Function（包括已发布 AIP Logic），默认使用 latest，也可固定已发布版本；工具概览没有为所有 Function 调用声明统一人工确认规则。Command 的配置当前仍为 **Beta**，默认要求用户审阅 payload 后 Reject/Approve，可由构建者关闭审批。因此“有工具确认”“默认批准”“用户按过一次按钮”必须具体到工具类型和配置版本。[Chatbot Tools](https://www.palantir.com/docs/foundry/chatbot-studio/tools)、[Command approval](https://www.palantir.com/docs/foundry/chatbot-studio/commands-as-tools#asks-for-user-approval-before-execution)

EOS 建议为工具注册一份机器可检查的 effect 声明：只读 / UI 状态更改 / 业务写入 / 外部副作用；确认 UI 显示目标对象、参数、受影响范围和执行身份。对业务写入保留服务器重新验证，避免把自然语言“确认”或客户端更新变量当作写授权。

### 3.2 服务器提交条件、对象访问及相应写入授权规则仍生效

Action 提交需访问被编辑的对象/关联类型及 datasources，并通过 submission criteria；开放动作以外写入的类型还需相应 writeback dataset edit permission 或 Restricted View edit policy。配置了 Action log 时，提交者还需日志对象类型权限，否则提交失败。行列读控制过滤 Action 能读取的数据，**不会自动延伸到 Action 的写入**；下游保护要结合 Markings/CBAC 与读写 authorizations。这些是 Action 平台规则，Chatbot 的确认不会替代它们。[Action type permissions](https://www.palantir.com/docs/foundry/action-types/permissions)

Submission criteria 可组合用户、参数、对象/关系与执行上下文，全部满足才可提交，与“能否编辑 Action type”独立。当前不支持 attachment / object set 参数作为 criteria。对 group、Marking、organization membership 用 NOT 是官方明确的误配：scoped token 可能没有所检属性，反而让 NOT 条件通过。EOS 应优先用正向授权和确定性业务验证，覆盖未知属性、受限 token 与重复操作。[Submission criteria](https://www.palantir.com/docs/foundry/action-types/submission-criteria)

### 3.3 接入 Logic 并不形成整个 Chatbot 会话的事务

Logic staged writes 当前仍标 **Beta**，尚用“将很快对新函数默认开启”的表述，不能写成已经默认全面开启。启用后，嵌套函数/Action 的 Ontology edits 暂存于临时存储，同一次 Logic execution 内后续读取可见，执行完成再应用。它是 Logic 的执行语义，不是“用户整段 Chatbot 对话先暂存、最后一次确认原子提交”的保证。[AIP Logic staged writes](https://www.palantir.com/docs/foundry/logic/staged-writes)

同样，不可把 AI FDE 的 Ask/Allow 工具策略、Global Branching 默认分支，或 Evolve 的 proposal review 移植成 Chatbot 内置治理。在 Chatbot 中调用一个执行真正业务 Action 的工具，是运行时业务写入；用 AI FDE 修改 Action 定义/函数，是工程变更。两条链可能连接，却必须分别说明分支、对象数据、外部系统和发布目标。

**未知与验证要求：** 多工具并行情况下哪些写入可并行、重复 tool retry 是否产生重复副作用、浏览器取消与 server cancellation 是否停止已经提交的操作、跨多个 Action 是否有原子性、本次未得到 Chatbot 级保证。EOS 的建议是显式串行化冲突写入、使用业务幂等键和状态前置条件，再通过故障注入验证；不能凭模型文本承诺成功。

## 4. 会话、日志、反馈与保留时间

### 4.1 会话保留、日志保留、供应商零保留要分开

官方确认：**含 Commands 的 Chatbot** 会自动采用 24 小时 inactivity 后过期的 retention window。普通 Chatbot 的通用默认保留时间，本轮所读当前专页没有明确承诺；API 有 `estimatedExpiresTime` 元数据，也不足以推出所有会话固定 24 小时。Delete Session 使会话不能再访问且不再列出，文档没有把这描述为同步删除所有遥测与已导出数据集。[Commands retention](https://www.palantir.com/docs/foundry/chatbot-studio/commands-as-tools)、[Get Session](https://www.palantir.com/docs/foundry/api/v2/aip-agents-v2-resources/sessions/get-session)、[Delete Session](https://www.palantir.com/docs/foundry/api/v2/aip-agents-v2-resources/sessions/delete-session)


官方 2025-05-06 公告提供了更精确的历史配置依据：indefinite retention 在 Studio 为 opt-in，针对特定助手与版本，保存后未来版本沿用，旧未启用版本不追溯；restricted view-backed 类型当时不支持。Threads model mode默认长期保留，Chatbot mode则遵从助手设置。公告页面现有注释另标2026-04-27当周更名。上述为带日期的发布依据，不能据此替代当前普通新助手默认值或租户保留验收。[2025-05官方公告](https://www.palantir.com/docs/foundry/announcements/2025-05/)

历史线索另存边界：2025-07-10 CodeStrap 的社区讨论中，jason 将 indefinite retention 与 scoped execution 相关联，指出 stateful compute module Functions 当时受限；讨论最终因 retention UI 设置纠正而由提问者确认 resolved。它帮助提出“保留模式会影响工具适用性”的核验问题，不能证明 2026-10 默认模式或永久支持矩阵。[社区 4448](https://community.palantir.com/t/aip-agent-studio-does-not-support-compute-module-functions-as-tools/4448)

| 被保留内容 | 文档明确的时间 / 条件 | 不应如何类推 |
| --- | --- | --- |
| 带 Commands 的 Chatbot 会话 | 24 小时 inactivity 后过期 | 不等于所有 Chatbot 默认 24 小时 |
| 普通 Chatbot 会话 | 当前资料未给通用默认；API 返回 estimated expiry | 不从 API 示例日期或历史社区默认推出 SLA |
| 平台内服务/trace logs | 有权限者查他人日志的说明为 30 天；本人最近 24 小时仍需 view-execution-history operation，免除 enablement（CBAC 除外） | 24 小时是本人访问窗口，不是所有 logs 的存储寿命 |
| Logic user-scoped execution logs | 仅本人可见，保存 24 小时 | 不代表 Chatbot 本体或导出数据集同样保存 24 小时 |
| Evals user-scoped 结果 | 仅发起人、24 小时删除，不写 results dataset | 不代表 project-scoped 结果同样短期 |
| Evals project-scoped 结果 | 该模式为 Beta，结果 indefinite，项目成员可见，可写 dataset | 必须额外配置结果保留与敏感度 |
| AIP 第三方托管模型 prompts/completions | Palantir 声明模型供应商零保留 | 不等于 Palantir 业务会话、运行日志和客户导出数据集零保留 |

表中来源：[Configure logging](https://www.palantir.com/docs/foundry/administration/configure-logging#in-platform-log-access-for-ontology-and-aip-workflows)、[Logic execution modes](https://www.palantir.com/docs/foundry/logic/execution-mode-settings)、[Evals run configuration](https://www.palantir.com/docs/foundry/aip-evals/run-suite#execution-mode)、[AIP privacy](https://www.palantir.com/docs/foundry/aip/aip-security)。

### 4.2 结构化日志可跨工具追踪，也会保存高敏信息

Chatbot 每个用户消息计一次 execution；`traceId` 关联一次执行，`session_rid` 关联整段会话，`uid` 标识发起用户，`owning_rid` 指向最初发起执行的资源，适合把嵌套 Chatbot/Function/模型调用串起来。事件覆盖 session metadata、用户请求与取回上下文/variables、编译 system prompt 与工具定义、assistant 内容、工具输入和成功/失败结果、final response、execution error。工具结果含耗时与变量更新；事件 schema 和类型会变。[Session logging](https://www.palantir.com/docs/foundry/chatbot-studio/session-logging)

因此日志既是调试证据，也是业务数据的第二个落点。它可能包含检索片段、对象属性、用户标识和提示词；EOS 不应把日志导出当成“只记录耗时和状态”。建议区分可运营的脱敏统计流、受限调试正文和真正需要长期保存的审计证据，并记录日志 schema 版本、tool call ID、权限拒绝与客户端确认事件。后半段是 EOS 设计建议，不是已证实 Palantir 同时提供这三套流。

### 4.3 平台内查看与 streaming dataset 导出分别授权

Chatbot 导出复用 Foundry configure logging；**log exporting 当前为 Beta，可能未在目标 enrollment 开启**，由 Organization Administrator 配置目的地，从配置创建时连续写入。输出 dataset 宜设 security Markings；组织 Markings、source executor Project 与 Action project-based permissions 另有约束。导出 user IDs 默认 redacted，可配置解除；不要把 schema 存在 uid 字段当成导出默认可识别本人。[Session log prerequisites](https://www.palantir.com/docs/foundry/chatbot-studio/session-logging#prerequisites)、[Configure logging](https://www.palantir.com/docs/foundry/administration/configure-logging#export-foundry-logs)

平台内 telemetry logs 与导出 dataset 的权限独立。查看他人 traces / service logs 通常需要源执行资源 Edit（或授予等价 telemetry operation 的自定义角色）、项目或资源的 log access、以及所有日志 Markings。**日志不从 source executor 资源、输入或执行时访问的数据自动派生 Markings**；管理员显式设置的 Markings 才在日志查看时生效，必须覆盖工作流可触及的最高敏感度。无 Markings 的启用日志会对满足角色与 log access 的人开放。[Log permissions](https://www.palantir.com/docs/foundry/aip-observability/log-permissioning)

本人过去 24 小时日志的例外仍要求 `foundry-telemetry-service:view-execution-history` operation，只豁免 log access enablement；CBAC 环境不享该豁免。不要写成任何使用者自然能看自己的所有 trace。当前权限页把 AIP agent 明确纳入 source executor；配置与同名资源权限必须一起核验。[本人日志权限](https://www.palantir.com/docs/foundry/aip-observability/log-permissioning#required-roles)

这意味着“某用户不能在业务页读某对象，所以也看不到含该对象的日志”不是可接受的默认假设。EOS 验证应让两个不同授权用户分别尝试页面、Chatbot 输出、trace log 和导出 dataset；授权结果需要逐面记录。

还要区分记录的完备性：Foundry logs **不是 audit logs，也不保证 100% 投递**。Action log 是另一层业务决策对象，只记录成功提交，不记录失败；经 API / SDK 提交 Action 也生成它，绕过 Action 的直接 datasource 或 legacy writeback 不覆盖，完整对象编辑历史另有机制。需要证明业务写入时，应关联 session trace、成功 Action log、失败 metrics、对象 edit history 与平台 audit attribution，不以助手“已完成”的文字作唯一证据。[日志投递保证](https://www.palantir.com/docs/foundry/administration/configure-logging#log-guarantees)、[Action log](https://www.palantir.com/docs/foundry/action-types/action-log)

### 4.4 反馈与使用指标不能直接当效果验收

Chatbot Studio 的 Monitoring 和 Usage tabs 展示使用与用户反馈；点赞/点踩是反馈来源之一。运行时 View reasoning 可在 edit/view/Workshop/Threads 查看文档提供的过程视图。它们帮助定位问题，但用户偏好、工具成功、业务正确性、成本和目标动作完成率是不同指标。不要把“满意度提升”自动等同于安全正确写入；也不要把 View reasoning 命名为已证明访问模型私有完整思维过程的接口。[Monitoring](https://www.palantir.com/docs/foundry/chatbot-studio/getting-started#track-aip-chatbot-feedback-and-usage)、[View reasoning](https://www.palantir.com/docs/foundry/chatbot-studio/tools#view-reasoning)

## 5. Chatbots as Functions 与 Evals：可复用入口及测试边界

### 5.1 Function 化改变消费方式，但保留会话契约

把 Chatbot 发布成 Function 后，可在 Evals、Automate、Code Repositories 等 Function 消费点调用。发布设置可选每次 Publish 生成函数版本，或每次 Save 发 minor Function version。输入 `userInput` 必需；`sessionRid` 省略才创建新会话，不能传空字符串；传 RID 则继续已有会话。所有 application variables 成为可选输入，ObjectSet 默认是该对象类型的 base set；输出包括 `markdownResponse`、`sessionRid` 和被更新的变量，未更新变量输出为空。[Chatbots as Functions](https://www.palantir.com/docs/foundry/chatbot-studio/chatbots-as-functions)

这是一条接入后端自动化与测试的桥梁，不是完整浏览器宿主的替身。在不支持 Commands 的环境（官方举 Automate 为例）执行 Chatbot Function，Commands 会被忽略。EOS 应把“不支持的工具”作为明确能力协商结果处理，并记录宿主依赖；不能将 headless 执行的文字结果当成地图已经移动或页面已完成操作的证据。[Commands in Function environments](https://www.palantir.com/docs/foundry/chatbot-studio/commands-as-tools#test-an-aip-chatbots-ability-to-use-commands-as-tools)

### 5.2 Evals 的测试对象、结果权限与隔离是不同设置

AIP Evals 明确支持 Logic、Chatbot Function 和 code-authored Function，围绕 test cases、target function、evaluation function 与 metrics 评估非确定性输出、比较版本与模型、观察多次运行的方差。测试用例可人工定义，也可由对象集生成，并可给同一 suite 配多个目标函数。[Evals overview](https://www.palantir.com/docs/foundry/aip-evals/overview)、[Create suite](https://www.palantir.com/docs/foundry/aip-evals/create-suite)

Chatbot 需先发布为 Function，再从 Evaluation tab 创建 suite，并放在同一个 Project。官方建议测试 `sessionRid=null` 开新会话，避免意外接续历史；ObjectSet 输入应为 `null` 或实际值，不能为空。对 EOS，单轮测试和多轮测试应分开：单轮明示新 session，多轮显式串接上一轮 RID，并固定 state 初值和评判真值；并行度不自动构成同一对话。[Chatbot Evals setup](https://www.palantir.com/docs/foundry/chatbot-studio/chatbots-as-functions#evaluate-chatbots-with-aip-evals)

suite run 默认 user-scoped，使用发起用户权限，结果本人可见、24 小时删除、不写 dataset；project-scoped **Beta** 要求函数和 evaluator 用到的资源均导入同 Project，结果项目可见并 indefinite，可写 result dataset。文档建议 LLM-backed functions 每个用例至少跑三次，此数字是官方建议而非本文已执行次数。结果 dataset 要和 suite 同 Project，并且只有 project-scoped 才写入；可含输出、evaluator 结果、元数据、错误，当前不支持将 metric objective 的 passed/failed 状态写出。[Run suite](https://www.palantir.com/docs/foundry/aip-evals/run-suite)、[Result dataset](https://www.palantir.com/docs/foundry/aip-evals/results-dataset)

### 5.3 Evals 不可替代宿主端到端验收

Ontology edits 专页明确说明 **每个测试用例的 Logic function** 在 Ontology simulation 中执行，真实 Ontology 不变；自定义 evaluator 可检查模拟创建、修改、删除。其语境是 Logic 和受支持的 Ontology edits。本文没有找到能据此承诺 Chatbot 的每个 Action、Command、外部 API Function、通知或 webhook 都由 Evals 自动模拟的证据。[Evaluate Ontology edits](https://www.palantir.com/docs/foundry/aip-evals/ontology-edits)

EOS 因而需要四类验收：确定性权限/业务规则测试；Function 级对话与检索质量评估；宿主变量、Commands、确认/拒绝和取消的端到端测试；指定业务环境的可观测写入与副作用验证。必须在测试前列清楚允许真实触发的 effect，用受限资源和业务幂等条件控制验证。这是测试设计建议，不是本轮已完成验证。

## 6. Save、Publish、依赖版本与 Marketplace

### 6.1 至少存在三个版本面

Chatbot Studio 可以 Save 并给保存版本写描述，View 时选择版本；Publish 才让配置用于生产。Create Session API 可指定 `agentVersion`，省略则绑定**会话创建时**的最新 published 版本。因此发布 v2 不等于已证实已有 v1 session 自动迁移；应读取该 session 的版本元数据核验。与之并行，Function 工具默认 latest，可固定 published Function version，Function 化发布设置还会生成自己的版本。[Save/View/Publish](https://www.palantir.com/docs/foundry/chatbot-studio/getting-started#save-view-and-publish-an-aip-chatbot)、[Create Session version](https://www.palantir.com/docs/foundry/api/v2/aip-agents-v2-resources/sessions/create-session)、[Function tool version](https://www.palantir.com/docs/foundry/chatbot-studio/tools)

对 EOS，发布时应把“助手定义版本”和“被调用工具实现版本”同时固定或明确跟随规则，附上模型选择、检索配置、知识资源、state schema、host 能力与客户端允许资源。现有 session 的上下文与旧输出仍可能影响新请求；一个文件版本号不足以表达运行全貌。这是可复现性建议。当前材料没有证明知识内容全量快照、统一依赖 lockfile、不可变所有模型行为或 Chatbot 原子回滚保证。

Assist 的专用教程描述首版 1.0 与后续修改需重新 Publish；近期 Commands 教程则以 Usage 中 Assist toggle 配合 Publish 部署最新 published 版本。版本概念是可信事实，教程里的旧图标或 selector 位置不应硬写成所有 enrollment 的最新 UI。[Deploy Chatbots to Assist](https://www.palantir.com/docs/foundry/assist/agents-in-aip-assist)、[Commands Assist publishing](https://www.palantir.com/docs/foundry/chatbot-studio/commands-as-tools#publish-your-chatbot-to-aip-assist)

### 6.2 Marketplace 打包真实依赖，不只是提示词

Chatbot 可通过 Foundry DevOps 加入 Marketplace product，直接选 Chatbot 文件，或打包含 Chatbot widget 的 Workshop module 自动纳入 Chatbot。当前专页称功能可打包，明确例外是 **Assist agents**。带 document context 的 Chatbot 自动包含所属 media set，打包的是**整个 media set**，包含没有被该 Chatbot 使用的条目；若只想分发必要文档，应先建专用 media set 并改 Chatbot 配置。[Distribute Chatbots using Marketplace](https://www.palantir.com/docs/foundry/chatbot-studio/marketplace)

EOS 可借鉴以产品包管理可部署依赖图，但应把“资源进入产品包”“安装成功”“目标用户能读”“模型能接收”“工具可执行”设为不同验收项。特别是共享媒体集合混装其他内容时，最小检索范围不会自动等于最小分发范围。本文不把 Marketplace 的打包支持理解为会话历史、遥测数据或所有外部系统凭据随包迁移；当前专页未证明这些行为。

## 7. 与其他助手 / Agent 产品的边界

| 产品 / 入口 | 当前主要工作对象 | 与 Chatbot Studio 的关系 | 应避免的错误判断 |
| --- | --- | --- | --- |
| Chatbot Studio | 应用建设者配置的企业助手：模型、prompt、retrieval、state、tools 与 session | 本题构建与发布主线；不同宿主消费同一助手 | 不能缩成 Workshop widget；也不能从旧 Agent 名称推导全能工程 Agent |
| AIP Analyst | 自然语言驱动临时数据分析，自主搜索 Ontology、对象集变换、汇总和图表，可保存 analysis | 提供成品分析界面，也能嵌 Workshop/iframe | 当前能调用 Function 和 Action；不能称它纯只读或不执行工具 |
| 默认 AIP Assist | 平台导航、用法帮助、文档问答与应用上下文 | 平台支持入口；可承载 Studio 构建的 custom Chatbots | 默认 Assist“不访问你的数据”不能类推至已配置 Ontology/tools 的 custom Chatbot |
| AI FDE | 操作 Foundry 工程资源，修改管道、代码、Ontology、函数和应用 | 可帮助建设或维护 AI 系统；与业务 Chatbot 的运行生命周期不同 | FDE 的 session identity / Ask-Allow / 分支治理不是 Chatbot 全部工具的默认合同 |
| Pilot | 从自然语言生成 Ontology、design spec、React/OSDK code、seed data，并部署应用/widget；当前 Beta | 可能生成 Chatbot 的宿主应用，或为应用构建工程基础 | Pilot 构建时 seed data 隔离不保证嵌入式 Chatbot 运行时永不读真数据 |
| AIP Evolve | 目标、验证与约束驱动的 AI 系统优化，协调 AI FDE，交付 proposal 与 agent activity | 可用于更大 AI 系统的模型/提示词优化；仍需目标资源访问和验证 | 不等于 Chatbot 内置自我学习；不能假定每个 Chatbot 默认会持续自动优化或分支 |

表中事实依据：[Chatbot](https://www.palantir.com/docs/foundry/chatbot-studio/overview)、[Analyst overview](https://www.palantir.com/docs/foundry/aip-analyst/overview)、[Analyst capabilities](https://www.palantir.com/docs/foundry/aip-analyst/capabilities)、[Assist](https://www.palantir.com/docs/foundry/assist/overview)、[Assist custom Chatbots](https://www.palantir.com/docs/foundry/assist/agents-in-aip-assist)、[AI FDE](https://www.palantir.com/docs/foundry/ai-fde/overview)、[Pilot](https://www.palantir.com/docs/foundry/pilot/overview)、[Evolve](https://www.palantir.com/docs/foundry/aip-evolve/overview)。

Analyst 的当前 capabilities 值得单独强调：除 Ontology 查询、SQL、visualization 和 Skills，还有 Function lookup/Execute function，以及 Action lookup/Execute action；后者可创建/修改对象，通常要用户审批，除非配置自动提交。这使“是否能写”“是否有工具”不足以划产品线。更可用的划分是主要任务、建设者可配置面、可复用资源、执行环境与具体部署合同。[Analyst Functions/Actions](https://www.palantir.com/docs/foundry/aip-analyst/capabilities#functions)

Assist 也并非只能被动问答：它可以建议导航或 in-application action，并在缺信息时引导创建 Community 帖子；这个建议仍不等同于 Chatbot 的任意业务 Action 工具。custom Chatbot 的 Assist 入口可以有 Ontology context 与 Functions，甚至借 Commands 操作配对应用。应在研究和 EOS 产品命名中区分“平台支持 assistant”“应用运营 assistant”“工程 builder”“优化 orchestrator”，同时允许它们复用模型网关、资源寻址、工具描述和日志基础设施。最后一句为架构分析。[Suggested actions in Assist](https://www.palantir.com/docs/foundry/assist/aip-assist-suggested-actions)、[Deploy custom Chatbots](https://www.palantir.com/docs/foundry/assist/agents-in-aip-assist)

## 8. 可验证的 EOS 建议：先建立证据合同，再扩大自动化

这里只引用既有公开 EOS 对照章节作为历史基线，不判断当前内部实现。既有研究曾讨论 [Workshop / EOS 对照](../workshop-runtime-2026-10/eos-comparison/README.md)、[Custom Widgets / EOS 历史对照](../custom-widgets-2026-10/eos-implementation.md)；本轮未重读或获取内部源码，下面属于下一轮实验方案。

| 实验 | 设置与操作 | 可验证验收证据 |
| --- | --- | --- |
| 身份交集 | 两个数据权限不同用户、user OAuth 和受限 service OAuth 分别执行相同检索/工具 | 返回对象集合、调用者/服务身份、拒绝原因、source resource RID；不得由高权限缓存混给低权限用户 |
| 模型通道政策 | 模型允许 A/B；token 分别无 mandatory、A、A/C，消息均用低敏内容 | token A/C 被模型政策拒绝；scoped session 后通过需要有独立记录，不能把失败归因检索为空 |
| 四层写入 | Action 自动/需确认两配置；业务 criteria 允许/拒绝；对象权限允许/拒绝；payload 正确/错误 | Confirm / Reject 和后端提交结果各自可定位；拒绝时无写入，重复调用业务幂等 |
| Prompt injection | 在受控检索文档放入要求忽略权限、改工具目标的诱导文本 | 后端权限/criteria 不被自然语言更改；记录模型是否越界选择工具、服务器是否正确拒绝；不宣称默认全面防护 |
| Function 版本 | Chatbot v1 使用固定工具版本；另一个使用 latest；更新工具与发布 v2 | session metadata 与工具实现版本可复原；解释固定/跟随差异；新依赖触发客户端资源声明变更 |
| 多轮与并发 | 同 session 顺序发两轮；两用户、两client各建session；重复continue/cancel故障注入 | 不串话；同 session 不并发 continue；取消与已提交 effect 分开报告；不能仅用最终文字验收 |
| Headless 能力 | 同 bot 在宿主、Chatbot Function、Evals、Automate 路径执行 Commands 工作流 | 不支持环境明确标明未执行；API return、UI真实状态和工具结果互相核对 |
| 日志权限 | 高敏检索、tool输入与prompt写入日志；两用户分别读原业务资源、trace、export dataset | 四面访问结果独立；日志 Markings 覆盖最高敏感度；导出与platform viewer角色均验证 |
| 评估质量 | 固定事实真值、权限负例、检索噪声、错误tool参数、无结果、多轮状态；多次运行 | evaluator准则和错误样本可审阅；文字质量、真实工具结果、变量变化与成本分项比较 |
| Marketplace 最小分发 | 共享 media set 含使用/未使用文档；另建专用集合比较产物 | 包资源清单与内容差异；安装后依赖ACL、模型和tool权限核对；不把selected docs等于package docs |

建议 EOS 首版先选“明确任务 + 有限对象集 + 只读/预览工具 + 真实拒绝反馈”的应用助手，再按可验证工具合同开放业务 Action。扩展时优先建立可寻址资源、类型化输入/输出、宿主能力协商、后端授权、trace 和发布依赖记录。这一顺序由上面的产品机制推导，不是“已在 EOS 实测有效”。

表中“同 session 不并发 continue”有明确 API 契约：Blocking Continue Session 不支持同一 session 的并发请求，必须等上一响应后继续；本轮所读 session 创建、继续和删除端点均标 **Preview**。这是 API 状态与客户端要求，不等于整个 Chatbot Studio 主功能都为 Preview。[Blocking Continue Session](https://www.palantir.com/docs/foundry/api/v2/aip-agents-v2-resources/sessions/blocking-continue-session)

## 9. 尚未核实，不能补成事实

- 普通 Chatbot 当前通用默认 session retention；indefinite 模式的完整权限 scope、资源同 Project 的硬约束与当前 stateful Function 支持矩阵。
- 所有 Chatbot 工具是否统一最终用户身份；在 Function / Automate / service OAuth 下的逐层执行身份与日志归属。
- 自建 API 宿主如何完整接续所有客户端 tool approvals、Command payload 与取消流程；需按实际SDK版本与API契约核验。
- 多 Action/Function tool 的跨调用原子性、外部系统副作用的回滚、重试/幂等默认机制。
- Chatbot 普通运行、Evals、Logic simulation 是否完整隔离所有外部工具/通知/webhook；本轮只确认 Logic Ontology edit simulation 的较窄合同。
- Chatbot Publish 的多人审批、工程 branch 默认、统一依赖快照、回滚与迁移保证；不能移用 AI FDE/Pilot/Evolve 的分支表述。
- 安装 Marketplace product 是否迁移所有聊天历史、日志或外部凭据；当前 Chatbot 打包专页未给该保证。
- 模型供应商零保留之外，客户 Foundry 会话、导出 dataset 和审计日志的完整组织保留政策；必须按目标 enrollment 和合同核验。

这些未知项不推翻已经确认的配置、调用和发布能力，而是限定研究可以据公开资料承诺到哪里。
