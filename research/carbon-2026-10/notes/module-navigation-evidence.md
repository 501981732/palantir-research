# Carbon 模块、发现与导航：公开契约证据

> 核验日：2026-10-01。范围为公开 Palantir 产品文档、带日期公告与公开源码线索；未登录 Foundry 租户，未执行导航实验，未读取 EOS 内部源码。内部布局、变量重算、Custom Widget 协议详见既有专题，本篇仅研究它们作为工作台模块的连接边界。

**结论：Carbon 的可核实增量是策展工作台、参数化资源和跨模块导航。** 官方把 module 定义为在 Carbon tab 内打开的参数化 Foundry 应用；`dynamic` 指业务构建者可创建的 Workshop、Slate、Quiver 等资源。公开材料没有建立一个任意 JavaScript / OSDK 应用原生注册为 Carbon module 的契约。`custom` 首页 section、`dynamic` module 和 Workshop Custom Widget 是三种不同概念。[Modules overview](https://www.palantir.com/docs/foundry/carbon/modules-overview/)、[Navigation integration](https://www.palantir.com/docs/foundry/carbon/modules-navigation/#integration-with-the-navigation-framework-for-carbon-modules)、[YAML reference](https://www.palantir.com/docs/foundry/carbon/code-reference/)、[Custom widgets](https://www.palantir.com/docs/foundry/custom-widgets/overview/)

## 1. 先分清模块清单、发现清单与创建快捷方式

下表是当前文档实际出现的三个清单。它们服务不同入口，不能拼成一个已验证的通用插件 type enum。

| 清单 | 当前官方列出的内容 | 直接来源与正文定位 |
|---|---|---|
| 可用 Carbon modules | Object Views 中的对象/对象集/对象类型、Workshop modules、Quiver dashboards、Vertex graphs、Slate applications、Object Explorer searches、只读 Notepad documents | [Modules overview](https://www.palantir.com/docs/foundry/carbon/modules-overview/)，正文 `Available Carbon modules` |
| 可显式加入 Open in 的发现对象 | Workshop、Quiver dashboard、Slate、Vertex | [Module discovery](https://www.palantir.com/docs/foundry/carbon/modules-discovery/)，正文开头及四个类型小节 |
| Anchored / New-tab 快捷方式 | Object views、object sets/explorations、object type explorations、Workshop、Quiver templates、Slate、Search；New-tab 与 Anchored 可选相同资源类型 | [Menu bar configuration](https://www.palantir.com/docs/foundry/carbon/configuration-menu-bar/)，`Anchored modules`、`New-tab modules` |

**已确认的区分。** built-in Object View / Object Explorer / Search 是 Carbon 导航的内置模块类别，输入输出由产品预定义；dynamic module 对应可创作资源并需显式配置发现。这不否认底层 Object View 有独立配置与版本。Navigation 文档的动态模块示例还出现 Map，但模块 overview 清单没有 Map；不能据此承诺 Map 已被全部租户、所有入口与 Marketplace 完整支持。[Navigation integration](https://www.palantir.com/docs/foundry/carbon/modules-navigation/#integration-with-the-navigation-framework-for-carbon-modules)、[既有Object View配置研究](../../object-views-2026-10/README.md)

**分析。** EOS 的模块目录可借鉴“系统内置处理器”和“业务资源实例”的分离；这不要求复刻 Foundry 的枚举名称。能配置导航入口、能接受对象参数、能保留状态、能安装复用，应分别声明能力。

## 2. Open in 的范围与资源授权

| 场景 | 已确认行为 | 证据定位 |
|---|---|---|
| Carbon workspace 内 | Open in 只使用当前 workspace 配置的 discoverable modules | [Discovery behavior](https://www.palantir.com/docs/foundry/carbon/modules-discovery/#module-discovery-behavior-in-carbon-and-outside-carbon) |
| Carbon 外部 | 汇总用户可访问的 promoted workspaces；Navigation 细化为主组织与 guest 组织的 promoted workspace 清单求并集，再过滤与当前输出约束匹配的模块 | [Navigation discovery behavior](https://www.palantir.com/docs/foundry/carbon/modules-navigation/#module-discovery-behavior-in-carbon-and-outside-carbon) |
| 不直接使用 Carbon 的独立应用 | 可创建用户可访问且已 promoted 的 workspace，专门配置外部 Open in；官方建议同时保证模块资源可访问，例如与 workspace 放同一 Project | [Standalone discovery setup](https://www.palantir.com/docs/foundry/carbon/modules-navigation/#setting-up-navigation-when-carbon-is-not-accessed-directly-by-users) |
| 未 promoted workspace | 用户持 view 权限可通过直接链接访问；它不是外部 Open in 汇总范围的等价替代物 | [Workspace overview](https://www.palantir.com/docs/foundry/carbon/workspaces-overview/#promoted-workspaces)、[Viewer permissions](https://www.palantir.com/docs/foundry/carbon/permissions-configure/#configure-workspace-viewer-permissions) |
| 有 workspace 权限 | 不自动获得模块、对象、应用及其他资源权限 | [Viewer permissions](https://www.palantir.com/docs/foundry/carbon/permissions-configure/#configure-workspace-viewer-permissions) |

Workshop 的 Open in 配置有两端：Carbon General → Discoverable modules 登记模块资源；Workshop 输入 ObjectSet 设置 external ID 和类型约束。没有类型约束时可在所有对象类型上发现。Quiver 发现受 dashboard 的基准对象类型约束；Slate discovery 页面说包含 variable 的 application 可在所有类型探索中出现，Navigation 的 Slate 输入细则又要求可解释为单一 object/object set 参数，故配置时应同时检查两页规则。[Workshop discovery](https://www.palantir.com/docs/foundry/carbon/modules-discovery/#workshop-modules)、[Quiver discovery](https://www.palantir.com/docs/foundry/carbon/modules-discovery/#quiver-dashboards)、[Slate discovery](https://www.palantir.com/docs/foundry/carbon/modules-discovery/#slate-applications)、[Slate input](https://www.palantir.com/docs/foundry/carbon/modules-navigation/#slate-input-via-module-discovery)

**EOS 架构分析。** 角色工作台的“可发现入口”可以形成有边界的任务菜单；授权仍必须由资源与业务操作层独立判断。为排障保留三类原因：未进入当前工作台目录、输入不满足约束、用户无资源/业务权限。公开文档并未披露发现过滤与鉴权的内部调用次序，不应画出凭空的安全服务时序。

## 3. 输入输出和来源状态：可确认到哪一层

| 模块 | 已确认输入 / 输出 | 公开边界 |
|---|---|---|
| Object View | 输入任意类型的单个对象；输出当前展示对象 | 内置对象菜单导航不能在 workspace 发现配置中禁用；视图内布局不在此重写 |
| Object Explorer | 输入 versioned / unversioned object set；类型、保存 Exploration、List 等可成为探索起点；专门 Output 小节写当前选中 object set | 总述另写 current results，选择集/全部结果对应哪个具体菜单命令须租户验证 |
| Search | 首页查询是输入；用户操作类型、Exploration、List、Comparison 等资源决定后续探索入口 | Search 不是可任意改写输入输出的业务模块 |
| Workshop | ObjectSet interface 作为可发现输入；应用 Event 使用调用时选定变量值发起导航 | 可直接配具体目标；并不要求用一个“全局当前对象”承载所有业务上下文 |
| Slate | 输入可解释为单个 object 或 object set；输出来自具体用户链接动作 | state 另有 Carbon 与 Slate iframe 的保存 view identifier 协作，不是任意 JS 默认拥有的协议 |
| Quiver | Carbon 集成对象为 dashboard；输入对象/对象集受对象类型约束 | 卡片对象可进一步进入 Object View；不能将所有 Quiver analysis 都视为同一种 Carbon module |

本表的接口边界来自 [Navigation integration](https://www.palantir.com/docs/foundry/carbon/modules-navigation/#integration-with-the-navigation-framework-for-carbon-modules)；Object Views 的内部配置与 Workshop 的变量生命周期分别引用 [既有对象入口研究](../../object-views-2026-10/README.md) 和 [既有运行机制研究](../../workshop-runtime-2026-10/README.md)。

**导航的已确认保证。** 来源模块动作在 Carbon 中打开新的接收 tab，保留来源模块状态，使列表可分支打开多份详情，甚至以不同输入多次出现相同目标模块。Carbon 外对应动作打开新的浏览器 tab。[Navigation introduction](https://www.palantir.com/docs/foundry/carbon/modules-navigation/#introduction-to-navigation-in-carbon)、[Workshop Applications events](https://www.palantir.com/docs/foundry/workshop/concepts-events/#applications)

**不能由此推出的保证。** 没有证据证明所有模块共享 React 树、统一缓存、双向实时变量，或任意输入输出会建立持续订阅。原界面状态被保留也不等于所有草稿和 Action 事务状态会跨浏览器刷新/重登录恢复；公开资料没有给出统一 tab history 序列化、LRU 驱逐、恢复失败、冲突解决或多端同步契约。

## 4. Workshop 参数导航与 URL routing 的重要差别

| 通道 | 已确认契约 | 来源 |
|---|---|---|
| Carbon tab 参数 | Carbon 参数名为 `variable.<原external ID>`；Carbon URL query key 为 `param.variable.<原external ID>`；Workshop 原 external ID 无需加前缀或修改 | [Workshop integration](https://www.palantir.com/docs/foundry/carbon/modules-navigation/#workshop-module-interface) |
| Carbon 的 Workshop → Workshop tab 导航 | 支持 Object set filter variables | [Module interface: Carbon navigation](https://www.palantir.com/docs/foundry/workshop/module-interface/#carbon-navigation) |
| Carbon navigation 限制 | 空 ObjectSet、NaN、time series set、geoshape/geopoint、struct、scenario 变量列为不支持 | [Workshop limitations](https://www.palantir.com/docs/foundry/carbon/modules-navigation/#limitations) |
| 普通 Workshop URL 初始化 | 首次加载读取 interface 参数；加载后仅改变 URL 不动态更新变量；Open Workshop module Event 取调用时值构造目标 URL | [Open module event / URL](https://www.palantir.com/docs/foundry/workshop/module-interface/#open-workshop-module-event) |
| 普通 Workshop routing | URL 不直接承载 ObjectSet filter；ObjectSet URL 只支持以 RID 指定的单对象，可用其他 routing 变量间接构造值 | [Routing limitations](https://www.palantir.com/docs/foundry/workshop/routing/#limitations) |

例如 Workshop 原 external ID 为 `alert` 时，Carbon 参数名是 `variable.alert`，Carbon URL query key 是 `param.variable.alert`，Workshop 中仍保留 `alert`。前缀属于 Carbon 的参数映射，不属于 Workshop 的原 external ID。

因此，本次不将 URL routing 的 ObjectSet filter 限制泛化为 Carbon 参数导航限制。保存状态又是第三种契约，参见 [Workshop Runtime 的状态章节](../../workshop-runtime-2026-10/README.md#6-配置版本运行状态和可分享链接)。具体接口值与来源状态之间的关系应由用例验证，不能单凭同名 variable 认定持久共享。

## 5. YAML 是资源配置证据，不是任意代码注册证据

官方 reference 展示 `discoverableModules` 的资源 RID 清单；Menu bar 用 `configuration.moduleShortcuts.primary` / `secondary`，各项用 `moduleRid` 和 `parameterValues`。内置 RID 例子分别是 `ri.carbon..core-module.object-view`、`...exploration`、`...search`；Workshop 是 `ri.workshop.main.module...`。首页 `contents.type: custom` 表示自定义 section，其 items 可为 module、objectType、object、compassResource 或 foundryApplication；最后一种例子指定 Foundry application 名称和相对 URL。没有展示 JavaScript bundle、OSDK app manifest 或 native module SDK 注册方式。[YAML reference](https://www.palantir.com/docs/foundry/carbon/code-reference/)，`Setting discoverable modules`、`Anchor modules`、`Multi-tab modules`、`Custom section` 诸小节。

**事实与分析的分界。** Custom widgets 当前官方宿主范围是 Workshop；Workshop 本身是支持的 Carbon module。因此“用 Workshop 承载 Custom Widget，再作为 Carbon module”是由公开支持关系组成的路径；它不是直接把 Widget Set 或独立 OSDK 应用登记为 Carbon native module。widget 参数、事件、OSDK认证和发布机制沿用 [Custom Widgets 专题](../../custom-widgets-2026-10/README.md)，本篇不重写。[Custom widgets overview](https://www.palantir.com/docs/foundry/custom-widgets/overview/)、[Modules overview](https://www.palantir.com/docs/foundry/carbon/modules-overview/)

公开源码交叉核对也只支持较窄结论：`palantir/osdk-ts` 固定 commit `e53b94ecd5de7cdd7e864d0daa04363bdad4db4c` 的 `WidgetConfig.type` 为字面类型 `"workshop"`，这是该公开 Widget API 的宿主配置证据。独立 OSDK 托管文档确实讨论父网站获取子网站 `remoteEntry.js` 的 micro-frontend CORS，但那是托管网站组合案例，没有描述 Carbon module registration。[WidgetConfig源码](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/widget.api/src/config.ts#L76)、[Hosting application: CORS](https://www.palantir.com/docs/foundry/developer-console/deploy-custom-application-on-foundry#cross-origin-resource-sharing-cors)

**未知。** 本次没有得到可复核的公开 Carbon native SDK / 任意 OSDK module registration schema。搜索未找到不能证明产品绝无私有扩展或租户特性；报告只应写“公开证据不足以承诺”，不能写“Carbon 禁止所有自定义应用”。链接可用、iframe 可嵌、对象传参、宿主认证、资源权限、状态恢复及升级治理也不是同一接入层。

## 6. 版本与范围差异会影响架构判断

2026-09-21 公告明确：按 workspace 分别 opt-in Insight exploration 和现代 search。Insight 开启后替换 object types、object sets、saved explorations 的 Object Explorer-style exploration；现有 tab 需重开或刷新。既有 workspace 保持 opt-in，新 workspace 默认化在公告中还是后续方向。因此上面的 Object Explorer 流程用于解释当前仍公开的接口与旧入口，不能当成所有 workspace 的唯一最新 UI。[September announcement](https://www.palantir.com/docs/foundry/announcements/2026-09/#explore-ontology-data-in-carbon-with-insight-analysis)

两处要保留的资料差异：菜单配置使用 Quiver templates，模块 overview 使用 dashboards，Workshop Events 又列 Open Quiver analysis；应按具体入口分别标识，不能合并成“全部 Quiver 资源都原生支持”。Marketplace 也有更窄交付范围：当前 Carbon product 文档排除非 Workshop/object type/Link to Foundry Application 的 module types，另排除 walkthroughs、search groups 与 Select objects item。支持运行不等于可跨环境打包复用。[Menu configuration](https://www.palantir.com/docs/foundry/carbon/configuration-menu-bar/)、[Modules](https://www.palantir.com/docs/foundry/carbon/modules-overview/)、[Workshop Events](https://www.palantir.com/docs/foundry/workshop/concepts-events/#applications)、[Marketplace supported features](https://www.palantir.com/docs/foundry/carbon/marketplace-carbon-workspace/#supported-features)

## 7. EOS 应用架构验证建议（分析，未读取内部实现）

1. **先定义业务工作台契约。** 一个工作台目录管理入口与策展范围；模块资源管理实现和版本；数据/Action权限单独管理。复用同一模块时，允许多个业务工作台有不同的发现清单与初始参数。
2. **用“对象身份 + 集合查询 + 业务参数”作为显式导航输入。** 不把全局选中对象变成所有模块必读共享状态。首先验证对象详情、筛选集合和业务任务 ID 的组合，明确参数复制、引用或实时同步的选择。
3. **状态保留要按层验收。** 逐项检查新 tab 打开后返回原列表、同模块不同对象多实例、刷新、关闭再开、无权限目标、删除资源、external ID 迁移、旧链接与升级后的恢复结果。集合为空、集合类型不匹配、filter传参应有明确结果。
4. **能力注册要面向真实宿主。** 普通 URL link、iframe 嵌入、Custom Widget adapter 与完整原生模块列为独立级别。只有验证参数、导航、权限、认证、状态及版本后，再承诺更高接入等级。
5. **同一功能按运行与交付各验一次。** 验证单工作台可用后，还需验证复制/安装时模块、对象类型、权限映射与链接迁移；不要从运行演示推断跨环境部署完整性。

以上是参考 Carbon 公共产品契约形成的 EOS 取舍，均不是 Palantir 内部实现或 EOS 已批准设计。

## 8. 逐条来源与检索状态

以下均于 2026-10-01 通过公开网页读取成功。无日期文档表示核验日可见内容，不表示同日发布或全部租户统一 build。

| ID | 直接来源 | 本次核验的正文位置 |
|---|---|---|
| MN01 | [Carbon Modules overview](https://www.palantir.com/docs/foundry/carbon/modules-overview/) | 定义与 Available Carbon modules |
| MN02 | [Carbon Module discovery](https://www.palantir.com/docs/foundry/carbon/modules-discovery/) | 四类 discoverable resource；Carbon 内/外范围 |
| MN03 | [Carbon Module navigation](https://www.palantir.com/docs/foundry/carbon/modules-navigation/) | introduction、discovery union、built-in/dynamic、六类 integration、Workshop限制、Slate状态 |
| MN04 | [YAML reference](https://www.palantir.com/docs/foundry/carbon/code-reference/) | discoverableModules、moduleShortcuts、parameterValues、首页custom item示例 |
| MN05 | [Menu bar configuration](https://www.palantir.com/docs/foundry/carbon/configuration-menu-bar/) | Anchored / New-tab modules的类型清单 |
| MN06 | [Workshop Module interface](https://www.palantir.com/docs/foundry/workshop/module-interface/) | 首次加载URL初始化；Carbon支持object set filter |
| MN07 | [Workshop Events](https://www.palantir.com/docs/foundry/workshop/concepts-events/) | Applications：Carbon tab vs浏览器tab |
| MN08 | [Workshop Routing](https://www.palantir.com/docs/foundry/workshop/routing/) | URL变量类型限制、embedded routing不继承 |
| MN09 | [Carbon workspace overview](https://www.palantir.com/docs/foundry/carbon/workspaces-overview/) | Promoted workspaces、guest组织、直接链接 |
| MN10 | [Carbon Permissions](https://www.palantir.com/docs/foundry/carbon/permissions-configure/) | Workspace与底层资源权限分离 |
| MN11 | [Custom widgets overview](https://www.palantir.com/docs/foundry/custom-widgets/overview/) | 当前仅支持Workshop宿主 |
| MN12 | [September 2026 announcement](https://www.palantir.com/docs/foundry/announcements/2026-09/#explore-ontology-data-in-carbon-with-insight-analysis) | 2026-09-21；Insight/search独立设置、opt-in范围 |
| MN13 | [Marketplace Carbon workspace](https://www.palantir.com/docs/foundry/carbon/marketplace-carbon-workspace/) | Supported features的排除列表 |
| MN14 | [Restrict workspace navigation](https://www.palantir.com/docs/foundry/carbon/restrict-workspace-nav/) | 宿主UI限制与module内部链接/Application access分开 |
| MN15 | [WidgetConfig公开源码](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/widget.api/src/config.ts#L76) | 固定commit；`WidgetConfig.type`声明Workshop；不代表Carbon闭源实现 |
| MN16 | [Hosting OSDK application](https://www.palantir.com/docs/foundry/developer-console/deploy-custom-application-on-foundry) | CORS小节micro-frontend/remoteEntry示例；未定义Carbon原生注册 |

媒体由主报告统一获取、视检与登记。本笔记没有新增图片或视频，也没有以未观看视频作为画面证据。
