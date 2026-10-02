# 附录 A：机制、评测与交付合同

> 核验：2026-10-01。本文深化[主文](../README.md)的机制细节；所有 Evals、AI FDE、Branching、Logic 和 MCP 的能力均标为关联平台合同，不表示 Evolve 自动全部使用。未进行租户执行或 EOS 源码检查。

## 1. 配置不是执行证明，执行也不是验收

公开 Evolve 配置得到的是目标、目标函数、test data、scoring、output divergence、允许变更与 iteration policy，并最终形成可审阅 prompt。Proposal 得到的是候选说明和支持证据。中间仍要确认实际执行身份、分支、用例、模型版本、工具审批、候选差异和运行结果。[Evolve](https://www.palantir.com/docs/foundry/aip-evolve/overview)、[GA 配置流程](https://www.palantir.com/docs/foundry/announcements/2026-09#introducing-aip-evolve-coordinate-ai-fde-agents-to-improve-ai-systems-in-foundry)

| 工件 | 已公开的存在性 | 建议审查字段，非公开 schema |
| --- | --- | --- |
| Evolution 配置 | target、goal、validation、constraints、prompt | 资源/版本、允许/禁止集合、预算口径、负责人 |
| Agent activity | goals、insights、artifacts、实例状态 | 输入快照、tool calls、全部失败、执行身份、审批记录 |
| Candidate | 实例模型和 prompt 变更、branch proposal | 精确差异、parent baseline、依赖版本、编译/预览结果 |
| Validation | cases/suites、outputs、比较和 metrics | run IDs、case来源、evaluator/threshold版本、重复/并发/失败 |
| Proposal | changes、outputs、evidence、confidence、limitations | 所有正式资源提案映射、绝对指标、人工结论、发布门槛 |

没有取得 Evolve candidate manifest、artifact export schema、完整历史不可变性或长期保留合同。图片的“Share”“High”“Safe to proceed”只证明对应 UI 标签，不能证明可共享底层私有 session、统计置信区间或批准完成。

## 2. AIP Evals：cases、metrics 与通过判定

**关联平台事实：** suite 的 cases 可以手工输入、从 object set 生成，或混合。Object-set 列支持对象、属性、linked objects/sets 和静态值；linked property 有 Object Storage v2 限制。Target 与 evaluator 分开，evaluator 可返回 Boolean、numeric 或多指标 struct，string 用作 debug；也可不设 evaluator，人工看 outputs。[Create suite](https://www.palantir.com/docs/foundry/aip-evals/create-suite)

内置评价器涵盖按类型精确匹配、regex、数值范围、关键词、编辑距离、ROUGE 和 LLM judge。Judge 的条件应明确可验证；actual value 不接受 object locator/RID/object set/model 这类引用类型。不能把文本 judge 对对象引用的自然语言评价当精确业务状态核验。[Create suite：evaluation functions](https://www.palantir.com/docs/foundry/aip-evals/create-suite)

通过规则可以用以下**对文档的归纳伪逻辑**表达，它不是 SDK/API：

```text
case_iteration_pass = 所有所配置 metrics 达到其 objective/threshold
case_pass = 这个 case 的所有 repetitions 都通过
```

Boolean objective 要求 true 或 false；numeric 指标设置 maximize/minimize，threshold 可选。没有阈值的指标仍有分数，不能默认解读为业务 pass。所有 metric、iteration 的口径应在比较前固定。[原始判定规则](https://www.palantir.com/docs/foundry/aip-evals/create-suite)

Evolve 的 exact/semantic/best-effort **输出偏离要求**与 Evals evaluator 的 **函数评价结果**是不同层次。主文图1/图2的指令明确不向 suite 加自动 comparison evaluator，说明此实例在过程中另做并排判断。不能直接宣称语义等价选项必用某个持久化 LLM judge，或 10 cases pass 证明全部输出精确相等。[Review 原图](https://www.palantir.com/docs/resources/foundry/aip-evolve/aip-evolve-workflow-1.png)、[历史真实帧](../assets/05-devcon-constraints-12m11s.jpg)

## 3. 执行范围、重复、证据保留与实验

| Evals 运行项 | 关联平台合同 | 对 evolution 的待核内容 |
| --- | --- | --- |
| 函数版本 | Logic 可选 last saved/published，code-authored 测 published | 是否引用同一 baseline/candidate 快照 |
| User-scoped | 默认，发起者权限，结果仅本人，24小时后删除，不写 results dataset | 私有结果如何支撑跨人审阅及长期复查 |
| Project-scoped | 当前 Beta；相关资源 import 同项目，项目访问者可看，结果无限期保留，可写 dataset | 是否启用、是否实际采用、证据 ACL 是否合适 |
| Repetitions | 每例可多次；LLM 建议至少三次 | 实际重复数、随机性、方差及失效例 |
| Concurrency | 默认十个 cases 并行，可降低缓解 rate limits | 是否与 fleet/候选并发叠加，是否造成限流 |
| Metadata | branch/version/model 自动记录，可加 key-value | 输入快照、评测版本与成本归属是否也留存 |
| Intermediate output | Logic block 可暴露 intermediate parameters，并可随 results dataset 保存 | 哪个步骤改变、哪些中间失败被最终输出掩盖 |

出处：[Run suite](https://www.palantir.com/docs/foundry/aip-evals/run-suite)、[intermediate parameters](https://www.palantir.com/docs/foundry/aip-evals/intermediate-parameters)。以上都不能写作 Evolve 统一默认值或证据保留期限。

Experiments 需先将 model/prompt 等作为 function inputs，再明确候选参数值，对所有组合做 grid search。可比较 suite runs，最多选择四个 run 查看并排 case 和 function/evaluator logs；多 target 模式不支持配置 experiments。这个机制解决显式参数空间的比较，不证明 Evolve 内部使用同一搜索算法。[Experiments](https://www.palantir.com/docs/foundry/aip-evals/experiments)、[运行限制](https://www.palantir.com/docs/foundry/aip-evals/run-suite)

## 4. 三种“测试隔离”不能混用

| 机制 | 隔离什么 | 仍须单独处理 |
| --- | --- | --- |
| Evals Ontology simulation | 每例的创建/修改/删除对象不写真实 Ontology | 外部网络、build/GPU费用、其他写工具并无全面沙箱保证 |
| Global Branching 定义 | 可 branch 资源的定义修改；Ontology entities有独立分支行为 | 普通 Foundry资源新建/删除影响main、具体资源限制、partial merge |
| Branch Action 数据 | 索引到branch的对象数据编辑不merge到main；默认抑制部分外部副作用 | 未索引类型、启用external calls后真实原端点、其他消费者 |

出处：[Evals edits](https://www.palantir.com/docs/foundry/aip-evals/ontology-edits)、[Global Branching](https://www.palantir.com/docs/foundry/global-branching/core-concepts)、[Action side effects](https://www.palantir.com/docs/foundry/action-types/branching-action-types)。

Simulation 中新建对象无法预先配置为测试用例参数，应把可识别属性传给评价函数，在模拟内搜索核验。已删除对象不能直接传给 evaluation function，应传可识别属性查询并断言不存在；这不意味着待删除的现存对象不能作为 target 输入。现存对象的 edits 可以提供给 evaluator。自定义评价函数或 intermediate outputs 能核验实际 edit，而非只看最后生成的自然语言。[Evaluate Ontology edits](https://www.palantir.com/docs/foundry/aip-evals/ontology-edits)

Branch Action 若 function-backed 且包含 external calls，默认整个失败，明确启用才调用原端点；若配置的是生产地址，测试仍可能产生生产效果。Webhook/notifications 默认不执行。这里不得写任何真实客户端点，也不能假设模拟涵盖所有副作用。[Branching Action types](https://www.palantir.com/docs/foundry/action-types/branching-action-types)

## 5. 操作审批、资源政策、恢复与发布

AI FDE server 校验当前用户权限并记录 audit，session受markings；只读、mutation、Action/publish/tag、feature/protected branch 文件/build 有不同同意规则。预批准降低重复交互，不增加权限。Evolve 产生多个子 Agent 时的审批继承与共享 session 工件规则没有单独公开，应核实际 activity 与 consent。[AI FDE security](https://www.palantir.com/docs/foundry/ai-fde/security-and-governance)、[navigation](https://www.palantir.com/docs/foundry/ai-fde/navigation)

Global Branching Owner/Space Administrator 是 branch metadata/lifecycle 管理角色，不自动成为各资源 Editor。能看 proposal 的用户在 checks/approvals 满足、未 Do not merge 时可合并，不代表他能亲自编辑每个资源。默认 policy 可被贡献者已有权限自动满足；要求独立第二人要配置 custom policy，而非依赖 proposal 的存在。[Branch security](https://www.palantir.com/docs/foundry/global-branching/branch-security)、[approval policies](https://www.palantir.com/docs/foundry/global-branching/resource-protection-and-approval-policies)

分支 lifecycle 默认 inactive 35天、之后7天删除 branch data，可在控制台配置；inactive/archived build 会失败，需先恢复后修改，可能重建/重索引并手工恢复 schedules。Merged 为终态。**这是 Global Branching 的默认生命周期，不是 Evolve evolution 或全部评测证据的保留期。**部分 merge 失败当前不能整体 revert；这比“Resume 再运行一次”更严格，应预演资源级恢复。[Core concepts/lifecycle](https://www.palantir.com/docs/foundry/global-branching/core-concepts)

Logic 分支 pre-release 的发布与 merge 条件见主文§10；Python/TSv2/OSDK 的具体分支限制也必须先查。Logic version history 可以回到以前 saved versions，但不构成 Evolve 跨数据、外部系统和所有资源的原子 rollback。[Branching Logic](https://www.palantir.com/docs/foundry/logic/branching-logic)、[integrations](https://www.palantir.com/docs/foundry/global-branching/integrations)、[Logic FAQ](https://www.palantir.com/docs/foundry/logic/faq)

## 6. MCP 与数据通道

Palantir MCP 的公共 tools 包括对象 query/aggregate、类型CRUD、branch/proposal、OSDK、代码库PR、dataset创建/build和Compute Module。它不能写 Ontology 业务数据，但不能称为“只读metadata”。类型变更经 branch/proposal 人审合并，工具目录没有 merge 或 Evolve 专用启动工具；这不等于所有工具调用逐次人审。[Tools](https://www.palantir.com/docs/foundry/palantir-mcp/available-tools)、[security](https://www.palantir.com/docs/foundry/palantir-mcp/security)

Ontology MCP 面向业务运行，应用 object types 经SQL查询，预定义 Actions作为工具写数据，另有query functions。OAuth authorization code代表用户，client credentials代表service user；有效权限取三者交集：身份权限、应用maximum restrictions、requested scopes。应用默认 restricted，也可配置 unrestricted；headless应用可在无直接人监督下读写，不能凭“MCP”附加统一人审。[Sample architecture](https://www.palantir.com/docs/foundry/ontology-mcp/sample-architecture)、[authorization](https://www.palantir.com/docs/foundry/ontology-mcp/authentication-and-authorization)、[restrictions](https://www.palantir.com/docs/foundry/developer-console/application-restrictions)、[headless](https://www.palantir.com/docs/foundry/ontology-mcp/example-mcp-workflows)

PMCP tool search 按名称、类别和关键词本地检索，不另调用模型/网络，session内启用工具、重连重置，client需处理工具目录变更。它是上下文/工具发现机制，不是 Evolve 候选优化算法。[Tool search](https://www.palantir.com/docs/foundry/palantir-mcp/tool-search)

MCP Inspector可核工具集合、input schema和结果；Ontology MCP目前不支持MCP prompts/resources。外部模型收到工具输出，适用该外部供应商合同；AIP内部受控通道不自动覆盖它。这些接口可帮助形成可调用验证契约，但不提供 Evolve 的完整可测范围或输出质量保证。[Inspector](https://www.palantir.com/docs/foundry/ontology-mcp/debugging-with-mcp-inspector)、[PMCP security](https://www.palantir.com/docs/foundry/palantir-mcp/security)、[AIP security](https://www.palantir.com/docs/foundry/aip/aip-security)

## 7. 通用优化合同示例

下面是**作者提出的合成工程合同**，不是 Evolve API、可导入配置或 EOS 当前数据。数值为示例选择，应由目标系统负责人重设。

```yaml
target:
  kind: synthetic-order-classifier
  baseline: frozen-version-1
goal:
  metric: absolute-cost-per-business-call
  direction: minimize
constraints:
  allowed: [model, prompt]
  forbidden: [business-actions, evaluator, expected-outputs, production-records]
  search_budget: owner-defined-total-compute
validation:
  exploration_cases: agent-may-add
  acceptance_cases: owner-frozen-and-versioned
  holdout: hidden-from-candidate-selection
  repetitions_per_case: 3
  critical_rules: all-pass
  latency: owner-defined-limit
approval:
  independent-reviewer: required-by-local-policy
  evidence: [all-candidates, diffs, run-ids, costs, failures, permissions]
release:
  stage: branch-integration-then-limited-rollout
  recovery: pre-tested-resource-and-side-effect-plan
```

这个合同把“能不能访问”“允许改变什么”“怎样判分”“谁批准”和“怎样真正采用/恢复”分开。建议先对最小任务检查四类反例：无改善、质量回归、越界变更、执行失败。验收分母要覆盖这些任务，不能只统计 Agent 交出了一个 proposal 的成功率。

若开放确定性替代或工具重构，建议额外锁定输入schema、授权规则、异常fallback、数据新鲜度和外部写效应；如果生成专家审阅应用，应验证专家上下文、权限、盲评/顺序、反馈版本与漏填处理。没有这些基础验证，多Agent只是扩大候选数。
