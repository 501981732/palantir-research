# 公开演进、作者案例与 AI 工程交付边界

核验日：2026-10-01。本附录延续 [Pilot 第 10 节](../pilot-2026-09/README.md#widget-release) 与 [React 组件的 AI 生成研究](../osdk-react-components-2026-09/ai-generation.md)，补充版本证据、旧 iframe 路径和未合并工程草案。源码基线为 osdk-ts main `e53b94ecd5de7cdd7e864d0daa04363bdad4db4c`；正式发布与草案分别锁定。没有登录 Workshop / Pilot / AI FDE 租户，没有运行生产宿主，也没有检查 EOS 源码。

**结论：Registry widget 把高码组件变为带声明契约和版本的交付单元；公开演进继续把预览状态、打包和元数据检查拆成可组合工具。** 已落地的 Pilot object-set 模拟支持，与尚在 draft 的共享预览/SuperRepo 接入必须分开。旧双向 iframe adapter 仍有正式 npm 包；它可以读写 Workshop 变量和触发事件，却与 Registry 的资源、身份和消息契约不同。AI 生成器需要交付并验证这层 adapter，React 页面渲染成功不是宿主集成完成。

## 1. 时间轴：公告、合并、发布三个日期

| 日期 | 已确认事件 | 证据强度与边界 |
|---|---|---|
| 2024-11-12 | `@osdk/workshop-iframe-custom-widget` 1.0.0 首次出现在 npm version time 中 | npm 发布记录；不等于 Workshop 功能首次上线日 |
| 2024-12-11 | VincentF 发表双向 iframe 教程：Developer Console → React → 网站托管 → Workshop | 作者案例；不是 Registry widget set 的流程 |
| 2025-01-06 | AIP Community Registry 的 `OSDK Widget in Foundry` 路径首次提交 | 路径 commit `2545a91fe6026441af71d4accfd36e8dc41ff22f`；贡献者表列 Matthew Steele |
| 2025-08-21 | 官方公告推出 custom widgets，说明未来几周向 enrollments 普遍提供 | 可确定公开公告日；不能精确推出每个租户启用日 |
| 2025-08-21 19:30:43Z | 旧 iframe adapter 1.1.1 发布；本轮 npm `latest` 仍为该版本 | `gitHead=244f70956356e869f8cc5143c815369170d056fe`；随后仓库 HEAD 有额外 commit，不能混为发布包 |
| 2026-06-01 21:50:56Z | osdk-ts [#3418](https://github.com/palantir/osdk-ts/pull/3418) 合并，增加 faux object-set references | 作者明确为 Pilot custom-widget integration 所需；测试模拟器能力 |
| 2026-06-03 14:54:10Z | `@osdk/faux` 0.23.0 发布 | changelog 将 `58922c1` 列在 0.23.0；npm 给出发布时间。未取得该版本 gitHead |
| 2026-09-28—30 | #4102/#4103/#4104/#4105/#4120 创建或更新 | 本轮全部仍 open + draft，`merged=false`、`merged_at=null` |
| 2026-09-29 | 正式 `widget.vite-plugin` / `create-widget` 3.74.0 与 CLI 0.101.0 发布 | npm/provenance 已核验；草案的 preview/extract 能力不在正式入口中 |

来源：[官方 2025-08 公告](https://www.palantir.com/docs/foundry/announcements/2025-08/)、[社区教程](https://community.palantir.com/t/how-to-create-a-custom-widget-for-workshop/2182)、[案例固定 commit](https://github.com/palantir/aip-community-registry/tree/2545a91fe6026441af71d4accfd36e8dc41ff22f/OSDK%20Widget%20in%20Foundry)、[旧包 npm 元数据](https://registry.npmjs.org/@osdk%2Fworkshop-iframe-custom-widget)、[faux changelog](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/faux/CHANGELOG.md#L305)、[faux npm 元数据](https://registry.npmjs.org/@osdk%2Ffaux)。本地复核见 [PR 状态](evidence/lineage-pr-state.json)、[npm 检查](evidence/lineage-npm-legacy.json)、[正式构建包](evidence/build-package-versions.json)。

2025 年公告已列出 dedicated developer mode；其后续计划是 Marketplace 集成、object-set 参数支持、developer mode 改进和启动性能改善，不是首次提供 dev mode。今天已有相应文档和代码，不能继续将这些全部标为未支持。公告对路径取舍的解释仍有参考价值：Registry 减少 OAuth / 子域注册负担；需要独立网站子域、页面控制和可配置 CSP 的应用继续使用网站嵌入路径。[历史公告](https://www.palantir.com/docs/foundry/announcements/2025-08/)

## 2. 普通 iframe、双向 iframe、Registry widget

| 维度 | 普通网站 iframe | 旧 Bidirectional / custom widget via iframe | Registry custom widget |
|---|---|---|---|
| 宿主选取 | 网站 URL | 网站 URL + 运行时收到的配置 | Widget Set / widget / version |
| 前端交付 | 独立网站及其托管版本 | 同左，增加 Workshop 通信库 | Widget set 的资产与 manifest 版本 |
| 变量与事件 | 不能仅因嵌入就认为有双向绑定 | `useWorkshopContext` 定义字段，读写变量、执行事件 | widget 参数和 events 的声明、绑定及消息 API |
| 典型身份链 | 由嵌入网站负责 | 官方旧库明确 iframe 自行完成所需认证；初次可能看到登录 | Pilot/Registry 文档为查看者权限的 OSDK 访问，不需独立 Developer Console app |
| 公开包 | 无统一通信包要求 | `@osdk/workshop-iframe-custom-widget` 1.1.1 | `@osdk/widget.api`、`.client`、`.client-react`、`.vite-plugin` |
| 配置来源 | URL/宿主 iframe 设置 | React app 挂载后发送 config，宿主展示字段选择器 | 发布声明契约；dev mode 用于未发布代码/契约预览 |

依据：[现行 Workshop iframe 文档](https://www.palantir.com/docs/foundry/workshop/widgets-iframe)、[旧 adapter README](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/README.md)、[Pilot widget 部署](https://www.palantir.com/docs/foundry/pilot/deploy-a-widget)、[Registry core concepts](https://www.palantir.com/docs/foundry/custom-widgets/core-concepts)。表中的架构归纳不是跨路径兼容承诺。

### 旧库的真实客户端协议

在实际 npm 1.1.1 tarball 中复核到以下符号；SRI 校验通过。协议库存来自发布源码 `244f709...`，不是从 Registry 客户端推测：

| 方向 | 可复核消息 | 客户端语义 |
|---|---|---|
| app → Workshop | `react-app-sending-config` | 挂载时发送 config 与 pathname；收到宿主请求时重新发送 |
| Workshop → app | `workshop-accepted-config` / `workshop-rejected-config` | 接受返回 iframeWidgetId/configValues；拒绝转为 failed 状态及原因 |
| Workshop → app | `workshop-requesting-config` | 客户端回传当前字段声明；源码注释解释为配置面板同步所需 |
| Workshop → app | `workshop-value-change` | 匹配 iframeWidgetId 后更新 configValues |
| app → Workshop | `react-app-setting-value` / `react-app-executing-event` | 用 locator 定位字段；值携带 async wrapper，事件独立定位 |
| app → Workshop | `react-app-set-auto-max-height` | 合法非负整数高度；功能还取决于 Workshop 的 Auto (max) 设置 |

字段结构有 `single` / 可递归 `listOf`，单字段为 `inputOutput` 或 `event`。React callback 把 loaded/reloading/loading/failed 状态先写入本地，再在已有 iframeWidgetId 时向宿主发送。监听器筛选 `event.source === window.parent`；发送使用 `window.parent.postMessage(..., "*")`。这些是旧库客户端的可观察实现，**不能据此断言宿主的 origin 校验、鉴权和完整错误处理**。[messages](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/src/internal/messages.ts)、[hook](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/src/useWorkshopContext.ts)、[config types](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/src/types/configDefinition.ts)、[callbacks](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/src/transform-config/transformConfigCallbacks.ts)、[transport](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/src/utils.ts)

这组 `react-app-*` / `workshop-*` 消息与新 Widget API 的 `widget.*` 契约分开；不应把一个库的容错或序列化行为移写到另一个库。旧库公开且未归档，也不证明 Palantir 承诺它长期保持同等维护强度。

### Object-set 的历史限制需要分路径说明

旧库 README 的早期限制段和现行 iframe 页面仍提到 concrete ObjectType 与 10,000 locators 截断，但同一 README 的 FAQ 指导 OSDK ≥ 2.0 使用 `temporaryObjectSetRid`。本轮在 **正式 1.1.1 的 d.ts 中确认该类型存在**，与 FAQ 所述临时 RID 传递路径一致。不能把所有旧 iframe object-set 传递一概标为 10,000，也不能据此承诺任意真实租户支持无限集合。应记录所选字段类型、OSDK 版本，再验证目标宿主。[旧 README FAQ](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/README.md)、[发布源码类型](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/src/internal/variableTypeWithDefaultValue.ts)、[官方 iframe 限制](https://www.palantir.com/docs/foundry/workshop/widgets-iframe#limitations)

旧包为 `SEE LICENSE IN LICENSE.md`，该 License 的授权目的限定在 Palantir Platforms；不要把公开源码直接视为 EOS 可移植实现。本报告只记录接口和研究结论，不复制该库实现。[License 原文](https://github.com/palantir/workshop-iframe-custom-widget/blob/244f70956356e869f8cc5143c815369170d056fe/LICENSE.md)

## 3. 两个作者案例，能够证明什么

**VincentF 的教程（2024-12-11，2025-01-31 补充）**展示作者如何用 Developer Console、OAuth 回调、网站托管和 `useWorkshopContext` 将 React 接入 Workshop；后续补充把 wrapper 放在 route 层、配置 CSP 和刷新配置。它是旧路径的一手实施记录，适合定位“页面已打开、配置仍 loading”等问题。作者使用第三方 typing-effect 和自定义 UI，只证明该案例的可组合性，不证明 Registry 外网能力或任意组件兼容。[作者帖子](https://community.palantir.com/t/how-to-create-a-custom-widget-for-workshop/2182)

**Matthew Steele 的 `OSDK Widget in Foundry`**是 AIP Community Registry 贡献案例，固定路径 commit 为 `2545a91f...`。README 指导安装 Marketplace bundle、配置 SDK/Developer Console、托管网站，再输入网站 URL 完成变量/事件绑定。这里的 Marketplace ZIP 交付并不等于 Registry widget set 发布；仓库名里出现 Registry，也只是 Community Registry 收藏目录。[贡献者清单](https://github.com/palantir/aip-community-registry)、[固定 README](https://github.com/palantir/aip-community-registry/blob/2545a91fe6026441af71d4accfd36e8dc41ff22f/OSDK%20Widget%20in%20Foundry/README.md)

本轮没有执行这两个需租户 SDK、OAuth 与资源安装的案例；没有把教程截图称为本报告实测。社区回复中“预计下一年简化”只能作为当时意图；产品能力应回到后来的公告/当前文档核验。

## 4. #3418：Pilot 预览驱动的已落地桥接

[#3418](https://github.com/palantir/osdk-ts/pull/3418) 的作者 `brandonwisnicki` 明确说明，为 Pilot custom-widget integration 增加临时 object-set 注册与加载支持；merge commit 为 `58922c122b7c5c7624d30c74232826c1d534e52f`。实现位于 `@osdk/faux`，用 Map 保存 RID → ObjectSet，`reference` 分支递归解析，未知 RID 产生 `ObjectSetNotFound`。与页面数组替代不同，它能让预览保留 object-set 引用和组合语义。[DataStore](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/faux/src/FauxFoundry/FauxDataStore.ts#L677)、[reference 解析](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/faux/src/FauxFoundry/getObjectsFromSet.ts#L192)

源码测试覆盖注册/覆写、未知 RID、加载引用、嵌套引用、集合交集以及 derived property 中的引用；这些是仓库已存在的测试，**本附录没有声称重新运行了它们**。[DataStore tests](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/faux/src/FauxFoundry/FauxDataStore.test.ts#L253)、[组合 tests](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/faux/src/FauxFoundry/getObjectsFromSet.test.ts#L141)

关联证据可表述为“Pilot 的 widget 集成推动公共预览基础增加能力”。不能扩大为“Pilot 已完整复用 Workshop 内部运行时”“faux 实现所有生产权限/Scenario”“生产 token 通过 mock”。新 React adapter 的 objectSet hydration/materialization 属于另一层；与 faux 组合有工程意义，但具体生产 Pilot 依赖版本和完整调用图未公开。[React hydration](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/widget.client-react/src/utils/extendParametersWithObjectSets.ts)、[事件 materialization](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/widget.client-react/src/utils/transformEmitEventPayload.ts)

## 5. Pilot、AI FDE 与 MCP：实际公开交付接口

| 入口 | 公开可确认的工件/契约 | 本轮没有取得的证据 |
|---|---|---|
| Pilot widget 项目 | 一个项目可含多个 widgets；Pilot 定义 parameters/events；preview 与 seed/production 数据选择；tag 经 CI 发布 Registry 版本 | 私有 prompt、生产模板、真实生成项目 lockfile、精确默认依赖 |
| AI FDE OSDK React mode | 官方定义其范围为 React apps 或 custom widgets；mode 按任务加载文档与工具 | 完整生产 tool schema、生成项目逐行输出、Registry 发布工具实测 |
| AI FDE prefill URL | `/workspace/ai-fde/prefill` 接收 `prompt`、可重复 `skillRid`、`autoStart` | URL 本身不是 widget 发布 API；`autoStart` 仍遵循工具审批 |
| Palantir MCP | 可获取 widget/OSDK/React components 文档，迁移现有应用与操作项目/代码仓库 | 工具表不展示私有 Pilot/AI FDE 内部同名实现或其完整参数 schema |

依据：[Pilot build](https://www.palantir.com/docs/foundry/pilot/build-a-widget)、[Pilot deploy](https://www.palantir.com/docs/foundry/pilot/deploy-a-widget)、[AI FDE modes](https://www.palantir.com/docs/foundry/ai-fde/modes-and-capabilities)、[prefill](https://www.palantir.com/docs/foundry/ai-fde/prefill-sessions)、[Palantir MCP 工具表](https://www.palantir.com/docs/foundry/palantir-mcp/available-tools)。

MCP 中与交付链直接相关的公开名称如下；说明为本报告归纳，并未实际调用 Palantir enrollment：

| 工具名 | 可确认职责 | 不应混淆 |
|---|---|---|
| `get_custom_widget_documentation` | widget 开发指导 | 文档发现不是组件生成/注册 |
| `get_osdk_react_components_documentation` | 领域 UI 库指导 | 不决定所有生成产物必须采用该库 |
| `get_ontology_sdk_context` / `get_ontology_sdk_examples` | 获取 SDK 上下文与按版本/主题筛选的范例 | 不是运行时权限授予 |
| `convert_to_osdk_react` | 将既有 OSDK 应用转向 React hooks，可选 components | 没有承诺把应用转为 Registry widget；表中 Provider2 命名也不能替代本轮 npm API |
| `generate_new_ontology_sdk_version` / `install_sdk_package` | 更新 Ontology SDK 并检查生成/安装 | 与 widget set 版本是不同工件 |
| `get_repository_context` / `create_code_repository_pull_request` / `get_build_status` | 代码上下文、变更审阅和构建观察 | 这些通用能力不等于端到端 widget 发布成功 |

在本轮可访问的完整工具表中，**未列出明确的 `generate_widget`、`convert_to_widget` 或 `publish_widget_set` 专用工具**。这只能说明公开目录的可见范围，不能推出私有内部没有这些能力。`get_custom_widget_documentation` 描述提到 Workshop 和 Slate，但当前 Registry overview 明确仅支持 Workshop；文档工具覆盖词汇更宽，不能当作 Registry 支持 Slate 的证据。[MCP 表](https://www.palantir.com/docs/foundry/palantir-mcp/available-tools)、[Registry overview](https://www.palantir.com/docs/foundry/custom-widgets/overview)

## 6. 近期作者 PR：可研究的方向，不是当前 API

以下状态来自 2026-10-01 GitHub PR 元数据。五项均为作者 `tdeitch` 的 **open + draft**，没有合并日期。GitHub 可能给未合并 PR 非空 `merge_commit_sha`，那通常是测试合并对象，不能拿它当已合并证明。精确 head/base 见 [状态证据](evidence/lineage-pr-state.json)。

| PR / 创建日 | 固定 head | 作者目标与读到的实现/测试 | 发布边界 |
|---|---|---|---|
| [#4102](https://github.com/palantir/osdk-ts/pull/4102) / 09-28 | `0fc625308467f7be81e68ae59fe7058eed6e5e4b` | `build: local` 无需已有远端 widget RID/URL；placeholder RID，发现已安装 SDK；`FOUNDRY_WIDGET_SET_VERSION` 控制本地打包版本 | 作者明确 SuperRepo 支持开发中；CLI/local preview 是其他变更，Foundry dev mode 仍需 remote config |
| [#4103](https://github.com/palantir/osdk-ts/pull/4103) / 09-28 | `3f9284d0d459d0612a53313dafc61f1c09a91584` | 脚手架拟加 `--osdkPath`、`--viteConfig`、`--buildCommand`、`--skipFoundryConfig`，支持预生成本地 SDK 项目 | 参数未作为本轮正式 create-widget API 推荐 |
| [#4104](https://github.com/palantir/osdk-ts/pull/4104) / 09-28 | `e1f16d9273eb60122571341fbd2efb6f0cde361d` | 拟增 `@osdk/widget.preview`：共享 primitive/array 参数面板、事件状态、消息展示；host 提供 resource picker、翻译、transport/auth/persistence | 官方 npm registry 对该包返回 404；作者说 initial release/消费者接入仍有前置条件 |
| [#4105](https://github.com/palantir/osdk-ts/pull/4105) / 09-28 | `7ba02facf8d3c4f0341c12e5a9837d9677e5a556` | `seedReloadPlugin` 观察 `.palantir/.ontology-sync` 完成标记，等同步完成再 reload，关闭服务器时移除 watcher | marker 的 CLI producer 另行实现；不能承诺完整同步闭环已交付 |
| [#4120](https://github.com/palantir/osdk-ts/pull/4120) / 09-30 | `0f260b6cb9d124eddeca7e1fc26500abf9499eeb` | `extractWidgetDeclarations` / `extractWidgetManifest` 拟在资产 build 前验证声明/HTML入口/SDK元数据；使用 Vite alias，执行 config modules、不运行 UI 或写产物 | 基于 #4102 分支；作者要求先合并 #4102；正式 plugin 3.74.0 只有默认入口，无这两个 subpath |

正式包 3.74.0 发布时间是 2026-09-29，provenance commit 为 `fb8ec172d540ef7819382ff036aa2a692614af75`。不能因为 PR 创建在发布时间之前就假定它进入那次发布。[正式 npm/provenance](evidence/build-package-versions.json)、[构建源码/导出检查](evidence/build-source-map-audit.json)

另一个宿主相关候选 [#4070](https://github.com/palantir/osdk-ts/pull/4070) 拟让 `createClient` 读取 iframe URL 的 `foundryBranchRid`，显式 option 优先于 query、query 优先于 build meta tag。本轮它为 open、非 draft、未合并，head `216bcc7c231ab5563dc049b7ded3448c688e0bcd`。npm 元数据存在同名 branch 的 `next-*` 标签只能证明实验分发，不证明正式 stable 已有该行为。不要为生产 Registry/OAuth 路径推定统一 branch 协议。[PR状态](evidence/lineage-pr-state.json)、[正式版本与dist-tags](evidence/build-package-versions.json)

### #4104 对状态机设计的具体启示

草案 `useWidgetPreviewState` 用 `sourceId + generation` 保护更新：切换 widget source 或 reset 参数后，旧闭包的异步完成被丢弃。事件先验证 eventId、允许更新的 parameter IDs 和值类型，再一次写入；测试断言无效混合 payload 不产生部分更新。消息历史上限 1,000，source 切换清空日志，reset 参数保留已有日志。这些是**草案源码/测试观察，未在本轮执行、未进入生产包**。[状态实现](https://github.com/palantir/osdk-ts/blob/e1f16d9273eb60122571341fbd2efb6f0cde361d/packages/widget.preview/src/useWidgetPreviewState.ts)、[草案 tests](https://github.com/palantir/osdk-ts/blob/e1f16d9273eb60122571341fbd2efb6f0cde361d/packages/widget.preview/src/__tests__/preview.test.tsx)

作者明确共享 preview 不接管 transport、authentication、persistence 和资源服务；Foundry viewer 仍保留 sandbox、permissions、object-set picker、session storage 与虚拟化日志。这恰好说明“共享参数控件与状态”不等于“开源完整 Workshop host”。草案里的资源输入可由 host 注入，也不能用 mock picker 的表现证明生产选择器行为。[草案 README](https://github.com/palantir/osdk-ts/blob/e1f16d9273eb60122571341fbd2efb6f0cde361d/packages/widget.preview/README.md)

## 7. Marketplace 支持与 SuperRepo 原生接入分开

当前文档已经允许将既有 Widget Set 或包含它的 Workshop module 加入 Marketplace 产品；要求 vite-plugin ≥ 3.1.0，安装后手工启用 Ontology APIs。还列明安装源码用于调试、Ontology API name 需要一致及函数版本限制。[Widget Set Marketplace 文档](https://www.palantir.com/docs/foundry/custom-widgets/marketplace)

这不等于 SuperRepo 已有成熟的原生 widget component：公开 core concepts 的默认 `foundry.yml` 示例列 `ONTOLOGY` / `TYPESCRIPT_FUNCTIONS` / `APP`，但仅凭示例未列出不足以证伪扩展支持。更强的当前边界是 #4102/#4120 作者明确写 SuperRepo widget integration 开发中，加上未合并状态与正式包无新入口。可写“公开工作正在补齐接入”，不能写“已验证可用的 SuperRepo widget 全链路”。[SuperRepo core concepts](https://www.palantir.com/docs/foundry/superrepo/core-concepts)、[#4102](https://github.com/palantir/osdk-ts/pull/4102)、[#4120](https://github.com/palantir/osdk-ts/pull/4120)

`@osdk/react-components` 提供领域 UI；`widget.client-react` 负责 React 与 host contract 转换；MCP 为 agent 提供开发发现/操作；Pilot/AI FDE 是生成工作入口；Registry/CI/Marketplace 是不同发布环节。它们可以组合，公开证据没有证明一个统一的页面 DSL 或一个共享的私有生成器。已有 [三类组件契约与 EOS 研究](../osdk-react-components-2026-09/origins-and-eos.md) 和 [OSDK 仓库地图](../osdk-typescript-2026-09/repository-map.md) 可作为职责基线。

## 8. 对 EOS 的实施建议与待验证清单

本节全部是建议，未检查 EOS Registry / Adapter / runtime / 造物平台的实际代码；不得改写成 EOS 已实现的功能。

| 建议 | 来源启发 | 应交付的 EOS 可审阅工件 |
|---|---|---|
| 分离声明检查与 UI 编译 | #4120 拟在 asset build 前读取契约；正式链已有 manifest | 参数/事件 schema、资源引用清单、兼容 diff、build 输出 hash；声明读取环境仍需约束 config module 执行 |
| 保持领域 UI 与宿主 adapter 分层 | 新旧两套 React bridge；preview 草案明确 host 自有职责 | 公共 props/callback，低码 binding adapter；禁止 callback 直接作为 JSON，定义跨进程序列化与错误 |
| 预览保留语义引用 | #3418 用 faux object-set references | mock RID→集合表达式、空集/未知 RID/组合场景 fixtures；标注 mock 身份，禁止暗示真实权限 |
| 用 session/generation 防止过期异步写入 | #4104 的 reset/source-change 保护 | widget切换、解绑重绑、reset、网络完成竞态测试；规定哪些日志保留、哪些本地状态重置 |
| agent 输出携带版本契约 | MCP 的按版本范例；正式包与草案差异 | manifest、adapter、SDK、UI依赖 lockfile、指导版本、公开API检查；避免生成不存在的 preview/extract import |
| 分开三个升级面 | Widget Set版本、SDK版本、宿主引用不同 | registry发布、宿主升级和领域模型迁移各有 diff 与回退计划；不假定发布新版自动修复旧宿主 |
| 把审批/发布状态作为产品状态 | AI FDE prefill仍保留审批，Pilot tag/CI/嵌入各阶段 | 生成完成、构建通过、权限已核对、契约已绑定、版本已发布分别可见，失败恢复有定位信息 |

优先验证一条纵向切片：领域集合输入 → React Filter/Table → 选中/筛选事件 → 宿主变量 → 第二个组件联动。再加入 object-set 引用失效、参数 reset 后异步返回、组件导航卸载、事件局部无效更新、SDK/契约升级。**本地协议模拟可证明 adapter 的状态与消息逻辑；真实宿主另验配置面板、权限、生命周期、故障恢复、版本升级/回滚。** 两组证据必须持续分开。

尚待取得的关键证据包括：真实租户的 host 行为记录；Registry 更新配置时完整兼容判定规则；私有 Pilot/AI FDE 模板与实际 lockfile；SuperRepo widget 接入最终合并/正式发布；scenario 与复杂 object-set 在真数据/权限下的语义。公开客户端、作者测试报告、教程 screenshots 都不能补写成这些验证结果。

## 9. 来源矩阵与本附录核验记录

| 来源组 | 本次读取 / 固定范围 | 主要支持结论 | 明确不能支持 |
|---|---|---|---|
| 官方历史公告 | 2025-08，section 日期 2025-08-21 | Registry 对旧网站嵌入的演进与当时计划 | 当前租户功能状态、精确 GA 时间 |
| 当前官方产品文档 | 2026-10-01读取；Pilot/Widget/Workshop/MCP/AI FDE/SuperRepo | 用户入口、职责、可见工具与限制 | 私有实现、实际生成/发布成功率 |
| GitHub PR metadata | 7个 PR；merged/draft/timestamps/head/base | 已合并/草案、作者意图、依赖顺序 | 单有 merge_commit 字段不能证明已合并 |
| osdk-ts 固定源码 | main `e53b94e...` 与草案 head；#3418 merge | faux桥接/测试库存；preview草案状态机 | 生产闭源 host 全行为 |
| 正式 npm | 旧1.1.1 SRI/hash/符号；faux0.23.0时间；构建包3.74.0 provenance | 实际分发API、版本与源码边界 | 安装后目标租户的可用性 |
| 作者教程与案例 | VincentF时间明确；Community Registry path commit固定 | 旧路线实际作者工作流与代码结构 | Registry通用成功率/性能/权限能力 |

精简来源事实存于 [lineage-documentary-sources.json](evidence/lineage-documentary-sources.json)，未将整篇官方文档或社区文章镜像到仓库。旧 npm tarball 在内存读取并验 SRI，仅保存元数据和符号检查；SHA-256 为 `607aa54696aa97aa39ab2d346ee26779d9eb37adf6c60076077f3c8b4798319f`。许可证原文只链接，旧库源码未转存/复用。

本附录完成：既有章节交叉阅读；PR精确状态/日期/commit核验；旧库发布包符号与SRI检查；faux版本/changelog对照；官方工具目录与产品文档边界检查；作者案例与Registry分类核对。未执行：旧案例部署、draft PR测试、Palantir租户生成/发布或EOS源码审计。跨专题图片/视频及本地协议探针的验证记录由本专题主 [checks.md](checks.md) 汇总。
