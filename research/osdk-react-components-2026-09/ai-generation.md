# 从组件库到 AI 生成应用：Pilot / AI FDE / SuperRepo 的真实关系

研究日：2026-10-01。组件消费能力按 npm 0.61.0；本文另引用固定 main `e53b94ecd5de7cdd7e864d0daa04363bdad4db4c` 的开发工具/模板证据，逐项标明。没有取得私有 system prompt、生产模板或真实生成项目 lockfile，没有在 enrollment 执行生成。EOS 部分是建议，未检查 EOS 项目。

**结论：组件库正在被有意识地建设为 AI 编写 OSDK 应用的可发现、可学习、可复用基础。** Pilot / AI FDE 有明确指导目的，Pilot 有实际使用反馈，MCP 有官方文档和可选迁移工具。公开资料没有证明所有产物必须使用它，更没有证明所有低码/高码被编译成单一页面 DSL。对 EOS 值得共享的是领域契约、数据行为、组件、版本匹配的指导与验证。

## 1. 证据强度与未知项

| 证据 | 状态/内容 | 可以推出 | 不能推出 |
|---|---|---|---|
| [#2628 精确评论](https://github.com/palantir/osdk-ts/pull/2628#issuecomment-3985012402)、[docs 评审](https://github.com/palantir/osdk-ts/pull/2628#discussion_r2896645315) | 已合并 2026-03-09；指导面向 Pilot AI FDE，详细 docs 避免重复 | 文档设计有直接产品意图 | Pilot/AI FDE 为同进程，或每次调用读取此文件 |
| [#2915](https://github.com/palantir/osdk-ts/pull/2915) | 已合并 2026-04-02；Pilot 测试中 agent 写错 CSS 顺序促成修正 | 存在实际组件集成反馈 | 全部模板默认使用、视觉问题已自动解决 |
| [#3289](https://github.com/palantir/osdk-ts/pull/3289) | 已合并 2026-05-19；示例/安装指导修正涉及 Pilot npm/pnpm 与 harness 竞态 | 依赖管理、agent 行为是产品化工作 | 文档等同强制执行规则或 agent 不再出错 |
| [#2953](https://github.com/palantir/osdk-ts/pull/2953) | 已合并 2026-04-09；相对 docs 链接与 npm files | 版本匹配/离线文档随库分发 | 任意 agent 自动发现遵从 |
| [发布 manifest files](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/package.json#L358-L369)、[消费端 AGENTS](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/AGENTS.md#L1-L35) | 本次实际 tarball 有 AGENTS/docs；版本/入口/安装错误说明 | 有可读取的消费契约 | 所有使用行为已可自动验证 |
| [Palantir MCP 工具表](https://www.palantir.com/docs/foundry/palantir-mcp/available-tools) | 组件文档工具 + convert_to_osdk_react 可选 components | 官方 AI 开发生态可发现它 | 内部产品必定共用同名实现；Provider2 是当前 npm API 名 |
| [Storybook main](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/react-components-storybook/.storybook/main.ts#L21-L42)、[#2575](https://github.com/palantir/osdk-ts/pull/2575) | main/private 开发工具配置 addon-mcp、components manifest；另有 docs/a11y/vitest | 有机器可发现元数据基础 | 安装公开 npm 即取得 MCP 服务，或公网/Pilot已连通该 endpoint |
| [props 文档生成规范](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/react-components/README.md#L333-L360) | TS/JSDoc 生成 props，CI check-gen-props | 新鲜度有机械校验 | 参数运行语义和示例全部正确 |
| [Pilot frontend guide](https://www.palantir.com/docs/foundry/pilot/build-an-application#frontend-generation) | 读设计、Ontology 和 OSDK 文档，产出 React/hooks | 有应用级设计生成流程 | 文档中 components 一词必指这个 npm 包 |
| [AI FDE modes](https://www.palantir.com/docs/foundry/ai-fde/modes-and-capabilities) | OSDK React 模式涉及应用/widgets，模式加载相关指导 | 产品进入 pro-code UI 范围 | 此模式全部任务必用本库 |
| [SuperRepo core concepts](https://www.palantir.com/docs/foundry/superrepo/core-concepts)、[tutorial](https://www.palantir.com/docs/foundry/superrepo/tutorial-develop-with-a-superrepo) | OaC/functions/app、生成 SDK、本地闭环，教程使用 React hooks | 提供手写/AI 代码共同工具链 | 默认预装 react-components 或它本身是生成器 |
| [Pilot widget guide](https://www.palantir.com/docs/foundry/pilot/build-a-widget)、[host 契约](https://www.palantir.com/docs/foundry/custom-widgets/core-concepts) | widget parameters/events、sandbox/宿主约束 | low/pro-code 互操作边界明确 | Workshop 内建 widget 就是本包实现 |
| [#3418](https://github.com/palantir/osdk-ts/pull/3418) | 已合并 2026-06-01；faux object-set references 为 Pilot widget integration | Pilot 仿真推动底层公共能力 | 单此 PR 证明 widget 依赖组件库 |
| [app 模板](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/create-app.template.react.beta/templates/package.json.osdk.hbs#L16-L24)、[widget 模板](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/create-widget.template.react.v2/templates/package.json.osdk.hbs#L13-L23) | 检查到 React/widget 等依赖，没有组件包字面依赖 | 不能称公开脚手架一律预装 | 这些即全部私有生产模板，或搜索不到即从未使用 |
| [#3726](https://github.com/palantir/osdk-ts/pull/3726) | open/未合并；组件库模板/skill 探索 | 弱前瞻方向 | 已发布产品或正式承诺 |

消费端 AGENTS/docs 与贡献端 [.claude add-new-component](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/.claude/skills/add-new-component/SKILL.md#L9-L17) / [contribute](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/.claude/skills/contribute/SKILL.md#L68-L108) 也要分开：前者教 agent 消费库，后者教维护者建设库；贡献流程不能冒称 Pilot 的完整生产 prompt。

## 2. 按职责看产品关系

| 层 / 产品 | 共享价值 | 关系口径 |
|---|---|---|
| Ontology / OSDK | 业务语义、类型与访问协议 | 共同实体/关系/Action 基础 |
| @osdk/react | 对象查询、缓存、动作与订阅行为 | 可以与自有 UI 独立使用，见[架构篇](../osdk-typescript-2026-09/) |
| react-components | 公共业务交互、默认主题与 composition | 直接减少生成复杂 UI 的自由发挥面 |
| Pilot | 从需求/模型到设计与前端，支持应用/widget | 有直接指导目的与实际使用反馈，采用比例未知 |
| AI FDE | 更广的开发操作 agent，包含 OSDK React 模式 | 有指导关联，全部运行时依赖未知 |
| SuperRepo | OaC/functions/generated SDK/app 的开发与交付单元 | 类型工具链可组合，默认组件依赖未确认 |
| Workshop | 低代码 host 与现成工作流，接 custom widgets | npm UI 可以在 adapter 内使用，宿主协议独立 |

从这些职责可解释“统一高码”的可能机制：让手写与 AI 生成代码调用同一语义和行为，而不是另造 ObjectSet、Action 和缓存。组件维护者修复一次分页、加载或使用范例，下游可以复用。**这是架构推论，公开资料没有给出节省工时、tokens 或缺陷率的定量基准。**

## 3. 标准化的四层

1. **语义：** identity、属性/关系/Action 类型、权限和错误契约，来自 Ontology/OSDK 或 EOS 自有领域层。
2. **行为：** loading/empty/error、分页/排序/facet、validation/pending、Action 后刷新，组件与数据层各负责一部分。
3. **体验：** 可访问性、键盘、tokens、密度、props/slots；业务布局保留定制空间。
4. **生产过程：** 固定依赖、可编译示例、types/contracts、交互预览、权限负例、审查/发布回滚。

任何单包都不是完整标准化平台。Pilot 自己有 design 阶段，组件也有 tokens/Base/hooks；因此合理目标是语义和行为一致、视觉有边界地统一，布局和业务组合自由。现有 AntD/react-data-grid 不必为了这个目标都重写。

## 4. EOS 五层共享资产与两个宿主

| 共享层 | 要沉淀的资产 | 高码 / AI 消费 | 低码消费 |
|---|---|---|---|
| 领域契约 | 身份、类型、集合运算、Action 参数/结果、权限错误 | typed client/hooks | metadata 绑定与属性面板 |
| 数据行为 | 分页/聚合/订阅、取消/并发、验证/失效 | 独立 hooks/service | 数据源与执行器 adapter |
| 交互组件 | Table/Filter/ActionForm/Detail/Viewer；Base 与 wrapper | 默认高层，特殊场景组合 Base | 注册组件，宿主映射 props/events |
| 生成指导 | 版本一起发布的清单、选择规则、正反例、配方 | 检索后生成普通 React | 有限制的配置生成 |
| 验证与治理 | types/contracts、交互/a11y、权限、遥测、审查/回滚 | CI/staging/发布门禁 | 设计时与发布门禁 |

宿主 adapter 只解决路由、尺寸、主题、变量/事件、生命周期与权限接口；领域组件解决业务交互。不要让公共组件依赖一个编辑器私有状态机，也不要把 React callback 直接当 JSON。完整来源/架构分层图见 [origins-and-eos.md](origins-and-eos.md)。

## 5. 四阶段采用与 A/B/C 基线

**阶段一，先建立代表性低风险纵向场景。** 同一模型、输入和约束比较：A 通用 primitives + 自由生成取数；B typed hooks + 自定义 UI；C typed hooks + 领域组件 + 版本匹配指导。覆盖查询→筛选→详情→写入动作，而不是只做静态列表。不要预设 C 必胜，找哪些场景更少修复、哪些应走 Base。

**阶段二，小而强的公共组件与使用包。** 优先高频交互，把 setup、版本、props、limits、范例一并交付；文档类型生成与 CI 新鲜度检查。prompt 负责选择和边界，机械规则进入 linter/types/tests。不要只教模型记规则。

**阶段三，接第二宿主。** 同一场景在独立 React 与 Workshop 类嵌入 runtime 运行；验证参数/事件、主题、权限、状态同步。如果 adapter 被业务逻辑淹没，回到领域契约重划边界。

**阶段四，形成模板与治理。** 只把验证过的组合进入黄金模板与生成目录。升级跑回归，允许有理由的 hooks/Base/custom UI 出口，生产异常回馈共享库与范例。无需仅为“像 Pilot”先重造全生成平台或统一页面 DSL。

## 6. 指标与停止条件

| 维度 | 可测项目 |
|---|---|
| 生成正确性 | 首次 typecheck/build，错误 import/props/依赖，人工修复分钟 |
| 业务闭环 | 过滤/排序/分页、Action validation/pending、防重复、成功失败后同步 |
| 权限 | 越权负例、无权限 vs 空数据、服务器执行，禁止硬编码生产数据 |
| 体验 | focus/keyboard/a11y、长内容、移动端、loading/error、主题密度 |
| 查询/性能 | 请求数、N+1、缓存重复/过期、数据量增长与重渲染 |
| 演进 | schema/Action 改动定位，升级回归、退出 wrapper 成本 |
| 组合 | 第三方设计系统、两宿主、Base/custom code 出口 |
| 成本 | 同模型同任务集的交付时间/tokens/重试/人工时间 |

类型/构建/关键交互失败、越权、错误 Action 或数据不一致是硬门禁，生成更快不能抵消。投资阈值由 EOS 的基线决定，不编造百分比。多数场景都要 fork 或大量绕过时，停止扩张 API，先改善契约与可组合性；agent 频繁误用时先查文档版本、范例可执行性和发现机制。

## 7. 实际风险与调查边界

共享库集中维护责任，不会消除责任；Beta/peer 耦合需锁兼容组合和升级测试。Ontology-aware wrapper 有数据契约绑定，Base 不自动迁走 Action/权限/治理。mock/seed 预览与生产规模、网络、权限和并发是不同验证阶段。没有获得私有依赖图或 prompt，只描述已读公开证据；未发现不是未使用的反证。
