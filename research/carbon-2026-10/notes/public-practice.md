# Carbon 公开实践：原帖、版本边界与架构含义

核验日期：2026-10-01。范围是公开网页正文与现行官方文档；未登录 Foundry 租户、未复现配置、未读取 EOS 内部实现。本附录不展开 Object Views 内部布局或 Workshop 变量机制，分别参见既有 [Object Views / Explorer / Workshop 研究](../../object-views-2026-10/) 与 [Workshop Runtime 研究](../../workshop-runtime-2026-10/)。逐条来源与检索边界见 [public-practice-sources.json](public-practice-sources.json)。

这些原帖说明 Carbon 的工程重点落在**工作流入口、对象集应用发现、状态链接与交付治理**。它们没有建立“任意 OSDK 应用作为 Carbon 原生模块”或“通用微前端框架”的公开契约。社区产品反馈、解决建议、内部 ticket 与公开正式文档分别记述，不能互相替代。

## 1. 阅读规则与身份边界

- **官方当前事实**：本次可读的 Palantir 文档说明其公开支持范围。页面没有租户构建号或产品版本号，不能自动反推功能在 2025 年已存在。
- **当时的实践与作者答复**：原帖的日期、问题和回复是可确认的发表行为；产品运行现象多为发帖者自述，未在本研究中复现。
- **作者身份**：本次读取的原帖正文未提供 evanj、helenq、Raghav 的可独立核实员工身份，故只用账号名称。jen 在 2025-11-19 的回复自称来自 Object View Team；这是页面中的自述。账号能提及内部请求并不单独证明职务或发布授权。
- **路线图**：提交内部请求、记录 feature request（FR）、作者希望迁移 registry，均不等于正式发布、GA 承诺或确定日期。

## 2. 首页如何承接动态业务内容

### 2.1 Workshop 首页替换是公开支持路径

2025-04-09，haavard 希望把动态 Workshop 区块与 Carbon 的模块、对象、URL 菜单放在同一首页。evanj 推荐从 Workshop 的 Resource List widget 开始复现首页资源入口，并把缺项作为独立 feature request 提出。这是“用 Workshop 构造完整首页”的建议，不能推为 Carbon 默认三栏内可任意拼入 Workshop 局部区块。[原帖：Carbon landing page in Workshop](https://community.palantir.com/t/carbon-landing-page-in-workshop/3457)

**当前官方交叉**：Carbon Home configuration 同时说明默认首页的 featured items 与 module-backed home page。后者通过 `Replace Home with Compass Resource` 选择 module 和 parameters，也能恢复最后配置的默认首页。Resource List 当前覆盖资源、对象类型、对象集，并列出 Recent、Favorite、Folders、Tags 等动态资源列表；资源的跳转方式仍取决于类型与是否能在 Carbon 中打开。[Home configuration](https://www.palantir.com/docs/foundry/carbon/configuration-home/#module-backed-home-pages)、[Resource List](https://www.palantir.com/docs/foundry/workshop/widgets-resource-list/)

**分析**：EOS 可以把工作台首页做成可治理业务模块，同时保留宿主的统一导航与上下文。应明确“默认首页组件配置”和“替换整个首页模块”是两种扩展层级，不宜从此例推出宿主提供任意前端组件插件点。

### 2.2 自定义首页与完整 Foundry sidebar 存在取舍

2025-05-06 的发帖者自述已用 OSDK 构造 Workshop widget 作为组织首页；改用 Carbon 后，标准 Foundry sidebar 消失。2025-05-14，evanj 的答复把 Carbon 描述为聚焦工作流的界面，sidebar 被有意隐藏；建议之一是用顶层 Workshop 的 iframe 嵌入 Carbon，但提示 Carbon URL 更新会丢失，影响 deep link。另一建议是导航到独立浏览器 tab，同时提及会失去 Carbon 的跨 tab shared caching。[原帖：Carbon Homepage Sidebar](https://community.palantir.com/t/carbon-homepage-sidebar/3791)

**证据边界**：上述 iframe、缓存与 URL 代价是作者在 2025 年的答复，未由本研究测得性能或重现浏览器行为。发帖者的 OSDK widget 自述体现的是 OSDK → Workshop → Carbon 的多层组合，不能证明 OSDK 应用获得 Carbon 的原生 module 输入输出契约。

**当前官方交叉**：官方 example workspaces 仍把 Carbon 定位为面向 operational users 的精简 Foundry 界面。`Navigation out of Carbon` 的禁用选项只约束 Carbon 界面元素；module 内的 Dataset Preview、Data Lineage 等出口可能仍存在，需要 Control Panel 的 application access 配置配合。[Example workspaces](https://www.palantir.com/docs/foundry/carbon/example-workspaces/)、[Restrict navigation out of a workspace](https://www.palantir.com/docs/foundry/carbon/restrict-workspace-nav/)

**分析**：EOS 应先区分操作员工作台与构建者平台工作区。精简导航是角色体验策略；可见菜单、workspace access 和底层应用权限是不同控制面。保留完整平台菜单、保留 deep link 和 iframe 组合之间的取舍应成为真实场景验收，不能只靠首页静态截图判断。

## 3. 保存状态链接会绕过首页：入口治理不等于必经页面

2025-10-01—02，mikewogden 希望首页列出用户的 saved/shared module states，使用户不再直接使用浏览器书签、漏掉首页公告。evanj 答复说，在 Carbon 内复制 saved-state URL 应携带 workspace；同时说当时不能强制某个 saved state 在指定 workspace 打开。其聚合建议是 Workshop 首页、集中保存目录与 Resource List，并提醒 saved state 是遵循普通 folder permissions 的 Compass resource；公共目录可能让其他用户看到其中的状态。用户 home folder 又遇到 Resource List 的 folder selection 当时为静态配置的问题。[原帖：Saved Module States in Carbon](https://community.palantir.com/t/saved-module-states-in-carbon/5155)

该回复还提出在业务模块中显示公告，或用横幅提醒首页更新。回复中的动态 Resource List 配置 ticket 是反馈记录，不能作为该功能已发布的证据。

**当前官方交叉**：Workshop state saving 文档说明它保存显式选择的变量状态和可选页面，且不是自动跨 session 持久化用户偏好；本次不重写其变量细节。当前 Resource List 已有动态 Recent/Favorite 等模式，但文档未证明支持动态解析每个用户 home folder，或专门汇总用户全部 saved states 的入口。因此应保留狭义未知，不能写成“Resource List 当前只能静态显示”。[State saving](https://www.palantir.com/docs/foundry/workshop/state-saving/)、[Resource List](https://www.palantir.com/docs/foundry/workshop/widgets-resource-list/)

**分析**：EOS 的首页应作为发现与工作起点，同时接受 deep link 作为正常入口。重要公告、任务提醒和版本迁移提示可考虑在相关业务模块内呈现，并定义已读状态；不能指望用户每次经由首页。收藏/保存状态的聚合需同时验证个性化查询和资源权限，不能用公开目录作为天然替代。

## 4. 对象集应用发现：Carbon 清单与 Object Set Panels 的演进

2025-05-01 的问题是希望 Object Explorer 将选中或过滤的对象集传给自定义 Object View。5 月回复建议接受对象集接口的 Workshop module，再通过 Carbon Discoverable modules 进入 `Open in`。evanj 也评论 Carbon 外的发现会汇总用户可访问的 promoted workspaces，并希望未来把 registry 移往更中央的位置。此处“中央 registry”是作者设计意见，不能说迁移已经发生。[原帖：Object View for sets of objects](https://community.palantir.com/t/object-view-for-sets-of-objects/3749)

**当前官方事实**：Module discovery 文档确认：Carbon 内只展示当前 workspace 的 discoverable 清单；Carbon 外取用户可访问 promoted workspaces 的并集。Workshop 的发现还需要对象集 module-interface external ID 和可选类型约束；未约束类型时在所有对象类型上出现。Discovery 支持 Workshop、Quiver、Slate、Vertex 各自的配置规则，不能扩大为任意应用注册 API。[Configure module discovery](https://www.palantir.com/docs/foundry/carbon/modules-discovery/)

**版本更新**：同帖在 2025-11-19 由 jen 补充 Object Set Panels；当前官方 panel 文档确认 object instance / object set 两种 panel。所以 5 月的缺口不能写成 2026-10 的当前限制。Object Set Panel 的对象类型视图配置与 Carbon 按工作台策展 `Open in` 是两种有联系的入口，不应合并成一个机制。内部布局与行为细节留在既有专题。[原帖后续](https://community.palantir.com/t/object-view-for-sets-of-objects/3749/11)、[Configured panel Object View](https://www.palantir.com/docs/foundry/object-views/config-panel-views/)、[既有 Object Views 研究](../../object-views-2026-10/)

**分析**：EOS 可以借鉴“对象集接口 + 业务域策展 + 按用户工作区发现”，并将其与对象类型默认视图分开。测试时至少覆盖：相同对象集从不同 workspace 进入 `Open in`、workspace 外的 promoted 并集、多个组的角色交叉，以及目标应用有权限却未被当前策展清单发现。最后一种是发现差异，不能据此断言权限失败。

## 5. 应用链接选项不是任意原生 module 接入

2025-07-03，Flackermann 报告 Carbon 配置中的链接类型清单未包含其希望添加的 Object Explorer 等应用。2026-03-12，evanj 解释这些选项可视为预设 shortcut；不在清单中的 Foundry 应用可以填完整 URL。答复同时说已提出把 `Link to a URL outside of Foundry` 改名为 `Link to custom URL` 的内部请求。[原帖：Add all Foundry Applications as link possibilities in Carbon Workspace](https://community.palantir.com/t/add-all-foundry-applications-as-link-possibilities-in-carbon-workspace/4374)

**版本边界**：帖中的新名称是建议截图和内部请求；本研究未找到正式发布公告证明重命名完成。完整 URL 是可导航地址，不自动具备 Carbon 原生模块的参数、输出、源 tab 状态保留和 `Open in` discovery 能力。

**当前官方交叉**：Carbon modules 文档把 module 定义为在 Carbon tab 中打开的参数化 Foundry application，并列出受支持类型。Menu bar 配置分别说明固定的 Anchored modules 与从 `+` 菜单启动的 New-tab modules。文章应依据这些公开类型与导航契约描述集成，不根据链接设置推断“所有 Foundry/OSDK 应用均可原生挂载”。[Modules](https://www.palantir.com/docs/foundry/carbon/modules-overview/)、[Menu bar configuration](https://www.palantir.com/docs/foundry/carbon/configuration-menu-bar/)

## 6. 模块迁移与书签稳定：兼容壳有文档，自动重定向仍需核验

2024-05-31，sharan 的问题涉及 Marketplace 部署重构后 Workshop resource RID 变化，用户旧书签将指向旧应用。Raghav 的建议以前提为用户旧书签指向原 module 的 `/view/latest/`，而不是固定版本链接；此时可更新并发布原 module，使其仅嵌入新 module。evanj 当时提醒每层嵌套会先加载外层再加载内层、带来额外延迟，并称当时没有 module 弃用后自动 redirect 的能力。2025-04-10，该账号补贴官方 in-place replacement 文档链接。[原帖：Automatically redirecting users to updated Workshop module](https://community.palantir.com/t/automatically-redirecting-users-to-updated-workshop-module/298)

**当前官方事实**：Embedding overview 的 `In-place replacement of a Workshop module` 明确支持：以 embedded module 作为原 module 的唯一 widget，使实现更换而用户仍使用原资源。这是可复核的资源稳定与实现替换方法。原资源入口需加载已更新并发布的父 module；指向父 module 固定旧版本的书签不会仅因新 module 发布就自动迁移，嵌入目标的版本选择也需另行确认。它不是 RID 层自动跳转，也不能忽略父/子 module 的 routing、state saving 等设置不继承的限制；细节参见已有 Workshop Runtime 专题。[In-place replacement](https://www.palantir.com/docs/foundry/workshop/embedding-workshop-modules-overview/#in-place-replacement-of-a-workshop-module)、[既有版本与交付研究](../../workshop-runtime-2026-10/data-actions-versioning.md)

**未知**：2024 年“没有自动 redirect”的回复不能直接证明 2026 年依旧没有；本次未找到正式公开文档确认当前 RID redirect 服务。EOS 建议是验证稳定应用 ID、旧 deep link/保存状态的兼容策略与退役提示，而不是照搬无限嵌套代理模块。

## 7. Workspace 依赖可追踪性：反馈不能当当前支持矩阵

2026-01-08，mikem 希望 Data Lineage 的 Linked Items 体现 Workshop 等资源所在的 Carbon workspace，便于知道操作员实际看到哪些产物。2026-01-09，helenq 回复将跟踪在 Workflow Lineage graph 显示 Carbon 信息的 FR。这里提问者说 Data Lineage，答复说 Workflow Lineage；不能合并成同一个产品入口。[原帖：Data Linage - Present Carbon Workspaces as Linkable Item](https://community.palantir.com/t/data-linage-present-carbon-workspaces-as-linkable-item/5795)

**当前交叉与未知**：Workflow Lineage 当前官方 overview 列有 Ontology 资源、应用、custom widgets、模型等，并明确其与 Data Lineage 的互补定位，但正文未明确说明 Carbon workspace 在图中的节点、关联项或支持矩阵。原帖仅证明 FR 被记录；本研究不能由此断言已经发布，也不能用文档未列出证明绝对不支持。[Workflow Lineage overview](https://www.palantir.com/docs/foundry/workflow-lineage/overview/)

**分析**：EOS 如把 workspace 当交付单位，应建立 workspace → 注册 module → 版本 → 底层资源依赖的可查清单。功能“可链接”与资源“被哪个工作台曝光”是不同问题。验证应包括重复复用 module、跨工作台版本差异和资源退役时的影响分析；不能假定一个 lineage 图已覆盖整个应用外壳。

## 8. 技术博客与公开源码检索

### 8.1 工作区作为受控发布渠道：作者文章与访谈交叉

Dorian Smiley 的 [The CodeStrap Operating Model for Palantir Foundry](https://medium.com/codestrap/the-codestrap-operating-model-for-palantir-foundry-c2e230b7f64a) 页面明确标注 **2025-07-30**。SDLC 段建议结合 feature branches、release groups 与 Carbon workspaces，把工作区作为受控发布渠道，围绕观测与回退组织发布。这是 CodeStrap 作者的交付建议；文章没有提供 Carbon canary 路由 API、实现代码或已验证的性能数据。

Connor Deeks 的 [原始 LinkedIn 帖与自带访谈转录](https://www.linkedin.com/posts/connordeeks_end-to-end-branching-from-the-data-lake-to-activity-7401648835934285824-SEpH) 补充了具体操作叙述：不同 working groups 用不同 Carbon workspaces，打开 Workshop feature branch，逐步向团队放开，合并后把链接更新回主线。转录称它们为实验性版本；页面仅显示相对时间 `10mo`，精确发布日期未核定。**本研究只读取文字转录，未观看视频，不能把此条当作画面或关键帧证据，也不能据转录独立确定每句话的说话者。**

**官方前提与边界**：当前 Workshop branching 文档确认 Workshop 与 Global Branching 的集成，但不支持该机制的非 Workshop 元素（例如 Quiver dashboards）不能在分支上修改。这支持作者方案的一部分前提，没有证明 workspace 整体原子分支、内置流量比例控制或原生 canary 发布引擎。[Branching Workshop modules](https://www.palantir.com/docs/foundry/workshop/branching-integration/)

**分析**：对 EOS 更有价值的启示是把工作台与人群、应用版本和观测联系起来，而非模仿一个未公开的 Carbon 发布 API。应验证相同业务域中的试用组隔离、deep link 指向、保存状态兼容、升级后的默认入口和回退链；不要用工作台首页版本代替底层应用版本治理。

### 8.2 已找到的公开配置与窄范围源码

官方 [Claim Portal YAML configuration example](https://www.palantir.com/docs/foundry/carbon/code-example/) 是可复核的工作区配置实例，包含 `discoverableModules`、Workshop module RIDs、内置 search/exploration modules、`parameterValues` 和首页配置。它能支撑声明式策展与 module 参数的研究，是配置示例，不能当作 Carbon shell 的前端运行时源码。

公开 Palantir TypeScript SDK 的 [ResourceType，固定 commit](https://github.com/palantir/foundry-platform-typescript/blob/4320149c31bcbcc2d176564d9259e343d9702d2b/packages/foundry.filesystem/src/v2/_components.ts#L665) 包含 `CARBON_WORKSPACE`；OSDK 仓库 `client.unstable` 的 [生成 URL target 类型，固定 commit](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/client.unstable/src/generated/ontology-metadata/api/__components.ts#L2687) 包含 `CarbonWorkspaceUrlTarget`。这些类型分别证明资源类别和生成 URL target 存在；它们没有提供通用 microfrontend mount/unmount、任意 OSDK module 注册或 Carbon shell 源码的契约。

### 8.3 有界检索结果与未确认事项

2026-10-01 的检索覆盖 Palantir 官方文档、作者原文、公开访谈转录，以及 Palantir 组织和全站 GitHub code/repository 查询。`Carbon org:palantir` 返回 9 处，相关项为 SDK 枚举/生成类型，其余为无关内容；`"Carbon Workspaces" org:palantir` 返回 0 处且结果未截断。扩大到 `"carbon workspaces" -repo:JeremyMeissner/palantir-docs` 的查询返回 16 处，主要是文档镜像、参考资料与架构评论。检索中的碳排放同名材料全部排除，CodeStrap 文章链接的 `doriansmiley/foundry-developer-foundations` 本次读取为 404，也未作为 Carbon 实现证据。查询与边界完整列于来源 JSON。

**结论范围**：公开材料可以支持 Carbon 的工作区配置与特定交付实践；本次有界检索未发现高质量、可核验的 Carbon 应用壳源码实例。不能把“未找到”改写为“Carbon 没有开源实现”，也不能用 OSDK 枚举中的 Carbon 名称推导任意前端可原生接入。

## 9. 建议进入 EOS 验证清单的六个用例

以下均是基于公开材料的架构分析，不代表 EOS 当前实现：

| 验证用例 | 需要观察的结果 | 由哪个实践问题驱动 |
| --- | --- | --- |
| 从首页与 saved-state deep link 分别进入同一业务 module | 入口保留 workspace；关键公告能在相关业务上下文到达用户；保存状态遵循资源权限 | Saved Module States |
| 操作员工作台与构建者工作区切换 | 精简导航不误充权限边界；外部应用出口遵从真正的 access 配置 | Sidebar / Restrict navigation |
| 同一对象集在 workspace 内与外执行 Open in | 当前策展清单与外部 promoted 并集的差异可解释；目标资源仍单独鉴权 | Object View for sets / Discovery |
| 普通 URL、参数化 module 与原生 discovery 项分别注册 | 能力声明覆盖实际接口；普通链接不会被误标为宿主协议集成 | Link possibilities |
| 原 module 替换实现但保留旧资源入口 | 旧书签、routing、保存状态、发布版本与额外加载延迟可测 | Redirect / In-place replacement |
| module 被多个角色工作台复用、再升级或退役 | 曝光范围、版本差异、影响清单和回退对象可追踪 | Lineage FR |

这些验证也应包含 current workspace 权限、promoted 可见性与底层 resource permissions 的不同组合。官方明确 workspace access 不等于其中所有 module、object 或 resource 的访问权。[Carbon permissions](https://www.palantir.com/docs/foundry/carbon/permissions-configure/)
