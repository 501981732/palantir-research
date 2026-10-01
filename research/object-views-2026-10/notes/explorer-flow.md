# Object Explorer：从对象集探索到对象详情和操作

检索日期：2026-10-01。本文依据公开官方文档的当日可访问内容；官方页面普遍未给出发布日期或对应租户 build，因此“当前文档”不等于已在某个 Foundry 租户亲测。作者视频、社区讨论按历史材料单列。本文没有访问 EOS 内部代码。

## 结论

Object Explorer 为 Ontology 提供通用搜索和对象集分析入口：先找到对象类型或对象，再过滤、聚合、沿关联切换类型，从结果进入单个对象的 Object View，或把当前集合用于 Action、其他兼容应用和导出。Object View 负责对象详情入口；Explorer 的 Exploration、List 和 Layout 分别保存查询工作、静态成员和分析呈现。这几个资源应分开理解。[Object Explorer overview](https://www.palantir.com/docs/foundry/object-explorer/overview/)、[Save explorations](https://www.palantir.com/docs/foundry/object-explorer/save-explorations/)、[Save lists](https://www.palantir.com/docs/foundry/object-explorer/save-lists/)、[Explore with charts](https://www.palantir.com/docs/foundry/object-explorer/explore-charts/)

**分析：** 对 EOS 的价值是把“通用发现对象”“面向一个对象的业务详情”“面向一项任务的应用”组合为连续入口，同时保留各自的状态与授权边界。公共资料不支持把所有入口归为一个页面 DSL，也不支持宣称 Open In 会携带完整 Workshop 运行时状态。

## 1. 对象、对象集、探索、列表和布局分别是什么

| 概念 | 已核实含义 | 保存或变化语义 | 证据 |
| --- | --- | --- | --- |
| Object | Ontology 中具有实际主键和属性值的数据实例；schema 资源与实例数据分层授权 | 本文不把 Object View 页面配置当成对象数据 | [Object permissioning](https://www.palantir.com/docs/foundry/object-permissioning/overview/) |
| Object Set | Ontology 中的一组对象，可对多个对象做操作；API 可依据集合定义加载对象 | 集合定义与分页返回的对象数组是两件事；不能把网页当前已渲染的行数当成集合规模 | [Object Set basics](https://www.palantir.com/docs/foundry/api/v2/ontologies-v2-resources/ontology-object-sets/ontology-object-set-basics/)、[Load Object Set](https://www.palantir.com/docs/foundry/api/ontologies-v2-resources/ontology-object-sets/load-object-set/) |
| Saved Exploration | 可重新打开的搜索参数、filters 和配置布局 | 返回同一组条件下的最新结果；不是冻结对象属性或成员的快照 | [Save explorations](https://www.palantir.com/docs/foundry/object-explorer/save-explorations/)、[Overview](https://www.palantir.com/docs/foundry/object-explorer/overview/) |
| Saved List | 从探索结果保存的静态对象名单，可保存全部结果或手动勾选的子集 | 成员不会自动随查询条件改变，除非手动更新；官方这里未承诺冻结属性值、删除对象保留方式或审计快照 | [Save lists](https://www.palantir.com/docs/foundry/object-explorer/save-lists/) |
| Explorer Layout | 某个 object type 的可分享分析视图，包含 charts、表格列配置和 sorting | 可设 Explore/Results 初始 perspective；个人默认优先全体用户默认 | [Explore with charts](https://www.palantir.com/docs/foundry/object-explorer/explore-charts/) |
| Comparison View | 两个过滤对象集的对比视图，来源可为动态过滤或已保存 Exploration | 可像 Exploration 保存和分享；不是单个对象详情页的并排比较 | [Compare object sets](https://www.palantir.com/docs/foundry/object-explorer/compare-object-sets/) |
| Temporary Object Set | API 由定义创建并返回 RID 的临时集合 | 当前 API 为 Preview，一小时过期；不能替代持久 Exploration/List | [Create Temporary Object Set](https://www.palantir.com/docs/foundry/api/v2/ontologies-v2-resources/ontology-object-sets/create-temporary-object-set/) |

**分析：** EOS 讨论“保存视图”时应先明确保存的是条件、对象 ID 名单、显示布局，还是业务数据版本。上述 Palantir 文档只证明了前三类和临时引用机制；它没有在 Explorer 文档中给出所有资源的内部存储结构、通用版本 API或永续链接合同。

## 2. 跨应用流程的可核实步骤

| 步骤 | 当前公开文档中的行为 | 对象上下文如何变化 |
| --- | --- | --- |
| 找到入口 | 首页可全局搜索、按 object type group 导航、预览 object type 的说明/属性/关联类型，再 Start Exploration；全局搜索覆盖对象、类型、Saved Explorations 和 objects-backed modules | 从跨类型发现收敛到指定 object type。可发现类型超过 250 时，首页 keyword search 限于前 250 个类型，文档建议使用类型/分组搜索。[Getting started](https://www.palantir.com/docs/foundry/object-explorer/getting-started/) |
| 收敛集合 | 搜索栏支持当前类型属性、关键词和关联过滤；关联可按有无 link、关联对象属性或关联到指定对象过滤 | 主类型保持不变，筛选条件缩小其对象集。[Filter results](https://www.palantir.com/docs/foundry/object-explorer/filter-results/) |
| 聚合并下钻 | Explore perspective 的图表针对主类型或 linked type 属性做聚合/过滤；移除图表并不会移除其筛选条件 | 图表呈现和集合筛选分开；某些图表只展示指标，例如 Single Statistic 不支持过滤。[Explore with charts](https://www.palantir.com/docs/foundry/object-explorer/explore-charts/) |
| Pivot | 从过滤后的 Airports，选择 Linked Objects 下的 Departing Flights，探索的主类型切换为 Flights，集合只包含这些机场关联的出发航班 | 是沿 Ontology link 的集合变换，不是打开某个单体对象详情。[Pivot to explore linked objects](https://www.palantir.com/docs/foundry/object-explorer/pivot-linked/) |
| 查看结果 | Results 用表格展示探索对象并滚动加载；点击 Title 列在新的 Object Explorer tab 打开该对象的 Object View | 当前集合变为一个对象详情上下文。[View results](https://www.palantir.com/docs/foundry/object-explorer/view-results/) |
| 预览详情 | 点击其他列或 checkbox，在 Results tab 右侧打开 Selection Preview；多选时可预览前 20 个对象中的任意对象；另有 Compare objects 并排详情入口 | 集合页保留，选择集合和预览对象并存；此比较不同于两个对象集聚合比较。[View results](https://www.palantir.com/docs/foundry/object-explorer/view-results/) |
| 直接从 Explore 进入详情 | Explore 右侧预览最多显示 20 条结果；点击 card 打开 Object View tab | 从聚合结果进入单个对象，无须先切换 Results。[Explore with charts](https://www.palantir.com/docs/foundry/object-explorer/explore-charts/) |
| 对集合操作 | 顶部按 Actions / Open In / Export 分组，分别用于 writeback、其他兼容平台应用和平台外导出；overview 举例兼容应用包括 Quiver | 当前 object set 或选中对象成为操作上下文；文档未承诺每个 Foundry 应用都接受它。[Apply Actions](https://www.palantir.com/docs/foundry/object-explorer/apply-actions/)、[Overview](https://www.palantir.com/docs/foundry/object-explorer/overview/) |

当前 Explorer 文档还描述 Results inline edit：配置了 inline edit action 的属性，在满足 submission criteria 后显示可编辑入口；提交时仍须再次通过 criteria。它不是任意属性直接写库的通用承诺。[View results — Inline edits](https://www.palantir.com/docs/foundry/object-explorer/view-results/)

**分析：** “关联过滤”与“Pivot”对于应用架构很关键：前者回答“哪些订单的客户满足条件”，后者回答“这些订单关联哪些客户”。EOS 如果只保留一个普通表格过滤器，会丢失主类型切换和关联对象上下文的区分。

## 3. Explorer 如何决定 Action 入口及参数

当前公开 Action 文档区分单对象 `object reference` 参数与批量 `object reference list` 参数。集合上下文只展示与对象类型匹配的 bulk actions；Object Explorer 会按当前上下文自动列出适用 Action。[Use actions in the platform](https://www.palantir.com/docs/foundry/action-types/use-actions/)

Explorer Exploration 中选 Action 会打开参数表单，把选中的对象直接带入；没有手动选择时传入当前全部对象。超过 1,000 个选中对象时 Action 不可用。如果无法确定应预填哪个参数，Explorer 留给用户填写。这是 Explorer UI 文档里的限制，不应延伸为 Ontology Action API 或后台批处理的统一上限。[Apply Actions](https://www.palantir.com/docs/foundry/object-explorer/apply-actions/)

Action 文档还列出三处自动发现入口：Exploration 的 Actions dropdown、对象详情的 Object Actions dropdown、详情中的 Linked objects section；单体详情可列适用的单体与 bulk Action。该页的 Object View 配图和 Actions section 配置包含历史形态，不能据此保证所有当前 configured/full/panel Object Views 都显示同一菜单、位置和参数配置界面。[Use actions in the platform](https://www.palantir.com/docs/foundry/action-types/use-actions/)

公开 Explorer 配置文档描述两个 metadata 入口：给 create Action 的主键参数或 modify Action 的对象引用列表参数加入 `actions` / `view_object_with_type:<OBJECT_TYPE_ID>` type class，可让成功 toast 指向被创建/修改对象的详情；`hubble-oe:hide-action` type class 可隐藏 Explorer 自动显示的 Action。这些涉及 Ontology 编辑权限，文档中的 Ontology Editor 名称和截图也需结合当前 Ontology Manager 界面核实。[Configure Object Explorer](https://www.palantir.com/docs/foundry/object-explorer/configure/)

**分析：** Action 自动发现可以把对象类型元数据变成应用入口，但“隐藏按钮”应仅被视为发现策略。安全判断仍在 Action 执行权限、对象/属性可见性和 submission criteria，不应依赖入口是否隐藏。成功后的详情链接则把“修改成功”与“定位刚产生的业务对象”连接起来，值得作为对象中心工作流的体验机制评估。

## 4. 查询、布局和操作状态应如何区分

Explorer Layout 允许保存图表、列和排序，并设置初始 Explore 或 Results perspective；个人默认可覆盖全局默认。它管理的是一个对象类型的分析呈现，不是 Object View 的 Workshop module、Object View version 或默认详情选择。[Explore with charts](https://www.palantir.com/docs/foundry/object-explorer/explore-charts/)

Explorer 文档记载其 undo/redo 暂存最近 5 个探索状态，可恢复 filter、图表布局、perspective 和 pivot。这是探索状态回退，不是撤销 Ontology Action 的业务数据写入。Explorer Saved Exploration 保留过滤和布局；Saved List 保留静态成员。官方这些页面没有说明 Action 提交中表单状态、某个对象详情的页签或任意嵌入应用的内部变量会随 Exploration 一并保存。[Explore with charts](https://www.palantir.com/docs/foundry/object-explorer/explore-charts/)、[Save explorations](https://www.palantir.com/docs/foundry/object-explorer/save-explorations/)、[Save lists](https://www.palantir.com/docs/foundry/object-explorer/save-lists/)

Comparison View 可由已保存探索、该类型全体对象或新定义的过滤集合构成；图表并排显示两组结果，可共同添加过滤，也保留 Results、Action 和导出功能；保存比较和分享比较是独立操作。分享不会给予 linked explorations 或 underlying objects 的权限。[Compare object sets](https://www.palantir.com/docs/foundry/object-explorer/compare-object-sets/)

**分析：** 这些边界适合用于评估 EOS 的恢复与分享行为：从详情返回集合页，需要恢复的是用户筛选、选择和布局，还是重新求值的对象结果；“撤销”需要明确只退 UI 状态还是回滚业务写入。两者不能共用未经说明的同一个按钮语义。

## 5. 跨应用链接合同与当前公开限制

官方 Generate Object Explorer URLs 文档给出以下入口。示例使用文档占位符，未在租户执行验证。[Generate Object Explorer URLs](https://www.palantir.com/docs/foundry/object-explorer/generate-urls/)

| 意图 | 文档格式或参数 | 边界 |
| --- | --- | --- |
| keyword-only 搜索 | `<BASEURL>/hubble/external/keyword/v0/<ENCODED_TEXT>` | 对空格/特殊字符编码 |
| 指定 object type 探索 | `/workspace/hubble/exploration?objectTypeId=<OBJECT_TYPE_ID>` | 不等于单个对象详情 |
| 直接进入表格 Results | 在探索链接加 `perspectiveId=results` | 改变初始呈现 perspective |
| Saved Exploration / Object Set | `/workspace/hubble/exploration/saved/<VERSIONED_OBJECT_SET_RID>` | 文档示例 RID 为 `ri.object-set.main.versioned-object-set…`；RID 存在不自动授予权限 |
| 其他应用创建的 Object Set | `/workspace/hubble/external/objectSet/v0/<OBJECT_SET_RID>` | 未承诺携带源应用的布局、Widget 状态或全部变量 |
| 复杂筛选搜索 | `<BASEURL>/hubble/external/search/v2/<ENCODED_FILTERS>` | 文档提醒示例 JSON 可能已过时；建议用实际 Explorer 的 `hubble_get_current_search()` 取得当前结构；可有多项 PROPERTY filter，但仅 1 项 LINK filter |
| 单个对象详情 | 本页转向独立的 Generate Object View URLs 文档 | 必须与集合 route 分开理解 |

**分析：** 这些公开 URL 说明“可从应用 A 带对象集合意图进入应用 B”，而不是证实双方共享同一个应用状态容器。EOS 可用“对象引用 / 集合表达式或引用 / 目标入口 / 可选呈现意图”评估入口一致性，但上述 URL 路径不是 EOS 的实现建议，也不是 Palantir 长期不会变化的 API 保证。复杂 filter 结构已有官方自述的过时风险。

临时集合 API 的一小时过期尤其影响外部链接：保存临时 RID、保存持久探索、保存对象名单不是等价手段。API 的 `LoadObjectSet` 本身另有分页、snapshot 和 storage-version 差异，不能从 Explorer UI 的 1,000 个 Action 对象上限推断 API 加载极限，也不能从 API snapshot 参数推断 Explorer List 会冻结属性值。[Create Temporary Object Set](https://www.palantir.com/docs/foundry/api/v2/ontologies-v2-resources/ontology-object-sets/create-temporary-object-set/)、[Load Object Set](https://www.palantir.com/docs/foundry/api/ontologies-v2-resources/ontology-object-sets/load-object-set/)

## 6. 共享、数据和 Action 的权限边界

Saved Exploration 与 Saved List 均可 Private 或 Public：Private 默认存入用户 home 的 Explorations folder，只对本人可见；Public 指定保存位置，权限来自该位置。Enrollment 若禁止在 home 保存，Private 选项也会禁用。分享这两种资源均不授予 underlying objects 的访问权。[Save explorations](https://www.palantir.com/docs/foundry/object-explorer/save-explorations/)、[Save lists](https://www.palantir.com/docs/foundry/object-explorer/save-lists/)

Ontology 的 object/link/action types 作为 schema 资源，与实际对象和关系数据分成两层授权。在 project-based 模型下，schema资源权限由 Compass project 管理：新Ontology启用此能力，既有Ontology需owner手动启用并迁移，当前不支持Default Ontologies；未迁移场景仍需区分Ontology roles与datasource-derived等旧模型。数据可由 object/property policies 或 data source policies 控制到 row/column 组合的 cell 层级。仅能看到某个类型或一个已分享探索，不能推出能看到其所有对象或属性。[Object permissioning](https://www.palantir.com/docs/foundry/object-permissioning/overview/)、[Ontology permissions](https://www.palantir.com/docs/foundry/object-permissioning/ontology-permissions/)、[Manage object security](https://www.palantir.com/docs/foundry/object-permissioning/managing-object-security/)

Action 是否可见、可编辑和可提交是不同判断。公开 permissions 文档要求执行者能查看涉及的类型/关联/数据源并通过 submission criteria；若允许 Action 之外的编辑，还涉及 writeback dataset 权限或 Restricted View edit policy。Read/write authorizations 另被标为 Beta 且未必对所有 enrollment 开启，不能在未核对租户机制时一概写成“所有 Action 只看某一个角色”。[Action permissions](https://www.palantir.com/docs/foundry/action-types/permissions/)、[Read and write authorizations](https://www.palantir.com/docs/foundry/action-types/read-write-authorizations/)

**分析：** EOS 的通用详情或通用探索入口应同时检查“入口资源权限”“对象/属性数据权限”“Action 可执行性”。共享链接需要保留对接收者权限独立求值的语义，而非把创建者过滤后的可见数据默认为接收者也可见。

## 7. Dynamic Object Set Action 是专门机制，不能泛化

Configure Object Explorer 文档展示一种专门配置：保存当前探索的过滤表达，创建动态集合并把其 RID 写入对象的 String 属性；新数据满足或不满足条件时，集合成员会变化。文档同时明确该功能仍在开发，可在没有自动迁移的情况下弃用，并建议使用前联系 Palantir。示例通过 object-set-rid 和 security-rid type classes 绑定类型及权限来源；保存的集合不会作为可搜索 Project 资源暴露，folder RID 在此用于确定其权限。[Configure Object Explorer — Actions on a Dynamic Object Set](https://www.palantir.com/docs/foundry/object-explorer/configure/)

**分析：** 这个模式说明“业务对象可以引用条件集合”，但它不能作为所有 Workshop Action、全部 Object Set 类型或外部 OSDK App 都具备相同持久化与分享能力的证据。文档随后出现 Linked Objects Exploration widget 和旧式 Object View 配置示例，不能跳过当前 Object View 机制核对直接照搬。

## 8. 历史演示与社区交叉核对

| 资料 | 本次实际读取程度 | 能支持什么 | 不能支持什么 |
| --- | --- | --- | --- |
| [Ontologize — Intro to Object Explorer](https://www.youtube.com/watch?v=YuT96FVeDuc) | 初次直接正文读取失败，后续公开浏览器描述核实2024-10-17发布、频道与章节；播放器失败、字幕不可用，未观看内容、未取帧，详见[媒体附录](media-evidence.md) | 历史教程的标题、作者、日期及开始探索、过滤、定制、结果、comparison等章节元数据 | 没有验证所有演示行为或当前版本一致性；不是 Palantir 官方频道视频 |
| [Palantir Learn — Data Analyst track](https://learn.palantir.com/page/training-track-data-analyst) | 搜索索引显示收录 “Ontologize: Intro to Object Explorer”；直接读取返回 Internal Error | 官方培训目录收录该作者教程的线索 | 目录收录不把作者观点变成平台保证，也不证明完成观看 |
| [Clickable object RID](https://community.palantir.com/t/clickable-object-rid/2228) | 读取完整公开讨论；2024-12-16 提问、2024-12-17 回复 | 当时用户试图把 Object RID 当 Resource/File RID 渲染为直接详情链接，joshOntologize 建议明确构造详情 URL，并在 Workshop 用 URL Redirect column；说明对象 RID、对象集合 RID、应用资源 RID 的导航用途容易混淆 | 是特定时间的用户报告及作者答复；不能当“2026 Explorer 永远不支持此链接”的保证 |

以上社区材料只用于识别误解和验证问题，核心能力以官方文档为依据。公开源码未在本附录找到可证明 Object Explorer 内部路由、查询状态或菜单发现实现的第一方代码；不据公开 UI 文档推断前端内部实现。

## 9. 面向 EOS 的架构判断与验证问题（分析）

1. **统一对象入口语义。** 评估同一业务对象从全局搜索、列表、关联对象、Action 成功回执和外部链接进入详情时，是否得到相同对象身份、符合权限的属性与当前默认业务视图。目标是入口的一致性，不是复制 Explorer UI。
2. **区分集合操作与单体详情。** 评估 Action 接收的是显式勾选名单、当前完整查询结果，还是动态集合表达式；空选择、超量选择、多参数歧义必须有清楚行为。这能避免“只渲染 20 行却误操作全部结果”的语义风险。
3. **分别定义四种保存。** 查询条件、静态成员、分析布局、业务数据快照应分别回答：什么会随数据变化、谁可访问、能否恢复、会不会过期。Palantir 当前公开材料不能替 EOS 回答业务数据快照的需求。
4. **关联导航需要可解释上下文。** 在对象 A 过滤关联 B 和沿 link Pivot 到 B 两个路径中，评估最终主类型、集合计数和返回路径是否清楚；不要让 UI 只显示相同的一个过滤标签而隐藏语义变化。
5. **跨应用携带最小上下文。** 评估对象标识、集合标识/条件、目标 view/perspective 与必要 return context；目标宿主必须重新鉴权，不能假设源应用可见状态等于目标应用可见状态。
6. **治理入口默认值。** Explorer personal/global layout 与 Object View type-level default、Workshop module release version 是不同层级。验证某个全局默认变化是否会覆盖个人默认、历史 exploration，及受限用户无权使用目标详情时的退化行为。

待有授权租户时最值得验证的公共资料空白：当前 Results Selection Preview 具体采用哪类 Panel Object View；Full/Panel/Legacy 默认选择与已保存 Explorer 状态的联动；离开并返回 Explorer 是否保留 selection 和 scroll；Action 成功后的集合再求值/详情刷新；受限属性参与聚合、关联过滤与保存/分享后的行为；temporary RID 到期后 deep link 的提示；跨应用 Open In 对目标权限和状态的处理。本文没有把这些问题写成已验证结果。
