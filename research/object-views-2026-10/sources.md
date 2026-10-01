# 来源与证据范围

检索基线：**2026-10-01**。在线文档“当前”仅指当日公开页面，没有产品构建号时不推测租户版本；没有发布日期时不补造日期。仅研究公开资料，未登录 Foundry 租户、未执行配置、发布或 Actions，未读取 EOS 内部代码。

四份原始来源表共 **93 条记录**，按 URL 归并为 **77 项**；补入 **6 个整页/固定提交源码**和 **23 个章节深链**后，本表共 **106 项**。保留原编号、原链接、出处、发布时间、检索时间、访问程度和支持范围，结构化记录见 [来源检查记录](checks/sources.json)。

归并只去除路径末尾的 `/`；保留查询参数和章节锚点。因此 YouTube 的视频参数不会丢失，章节深链也不会与整页混为一项。README 与五篇附录的直接技术外链均已登记；外部原图/动图链接属于 [媒体资产清单](notes/media-assets.md)及 [媒体资产记录](notes/media-manifest.json)，不混入技术事实来源。

官方当前文档用于支持机制和边界，有日期公告用于支持沿革，社区回复和作者教程用于提供实践线索。博客只用于交叉阅读；固定提交教学代码必须逐文件判断，不能因位于官方仓库就当作平台运行时或真实写回验收。

## 关键证据差异

- **命名与默认视图：**2026-02-19 公告使用 Core / custom；检索日文档使用 Standard / Configured。尚无正式改名日期，也未找到默认配置物化或迁移的完整协议。
- **Workshop 切换开关：**Configured 概览称 Workshop 不提供切换；专门 Object View 组件页给出模式和可选开关。保留双方来源，实际租户版本需核验。
- **保存与版本：**Object View 模块自动保存、视图发布、Explorer 保存探索/列表、Workshop 显式状态保存是不同契约。Workshop 的默认已保存状态自动加载不等于持续自动保存。
- **Carbon 与分支沿革：**2026-09 公告的选择开启与将来默认分开记录；2026-01 的审批缺口按历史处理。Carbon 可发现模块的对象类型约束是可选项。
- **作者视频：**Ontologize 视频最终只核实公开标题、频道、日期、描述和章节；保留早期直接读取失败。播放器未得到已验证内容帧，未完整观看，未交付该视频关键帧、字幕或短录屏。

## Object Views 与展示配置

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S001（G01, WB01, MD01） | [Object Views 总览](https://www.palantir.com/docs/foundry/object-views/overview) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | Standard / Configured 两类及其默认选择；Full / Panel 两种形态；Configured 由 Workshop 构建。 限制：文档定义不等于租户运行验证。 |
| S002（G02, MD06） | [Standard Object Views](https://www.palantir.com/docs/foundry/object-views/standard-object-views) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 元数据 visibility / base type 驱动默认属性展示；媒体、时序、地理属性增强展示；关联对象分组、预览及详情导航。 限制：媒体种类以文档支持范围为准。 |
| S003（G03, WB02, MD02） | [Configured Object Views 配置概览](https://www.palantir.com/docs/foundry/object-views/config-overview) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 自动默认配置的 schema 同步与编辑后接管；Ontology Manager 等配置入口；对象类型、托管模块与独立模块权限。 限制：default configured 与 Standard 的物化/迁移细节未公开；此页称 Workshop 无切换开关，与 G18 / WB05 相冲突。 |
| S004（G04） | [Object View 版本管理](https://www.palantir.com/docs/foundry/object-views/manage-versions) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 视图与模块分别版本化；默认自动发布；保存/发布协调页签与当前模块；模块周期性自动保存；历史作者、日期和发布标识。 限制：未发布视图修改对浏览者不可见；未给出自动保存周期、并发协议或所有页签原子发布保证。 |
| S005（G05, WB03, MD03） | [Configured Full Object View](https://www.palantir.com/docs/foundry/object-views/config-object-views) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 每个页签对应 Workshop 模块；页签结构与模块内容分开配置；当前OV-managed路径删除页签会删除托管模块，不推断共享standalone资源删除；单页签浏览态隐藏标题。 限制：编辑器未在租户亲测；当前页仍链接遗留配置。 |
| S006（G06, WB04, MD04） | [Configured Panel Object View](https://www.palantir.com/docs/foundry/object-views/config-panel-views) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 实例面板与对象集面板分别配置；对象集 Charts / List 默认内容；同类型对象聚合；编辑尺寸预设。 限制：尺寸预设只是近似预览，运行尺寸由宿主和设备决定。 |
| S011（G11） | [Object View 分支开发](https://www.palantir.com/docs/foundry/object-views/branching-object-views) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 页签结构与模块内容分资源；变基、发布检查、合并权限；遗留页签不能在分支编辑；审批政策继承。 限制：datasource-derived的main需OV Admin+任意输入datasource Editor，merge需类型View+所有backing datasources Editor+OV Admin；继承主线资源保护仍标开发中，审批继承不代表已经阻断主线编辑。 |
| S012（G12） | [Object Views 与 Marketplace](https://www.palantir.com/docs/foundry/object-views/marketplace-object-views) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 通过 DevOps / Marketplace 按页签打包；仅支持 Workshop builder，遗留页签需重建。 限制：未说明所有面板依赖及消费者定制冲突的处理。 |
| S014（G15） | [对象属性元数据参考](https://www.palantir.com/docs/foundry/object-link-types/property-metadata) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | title key、base type、格式、render hints 与 visibility 的区别；默认 visibility 为 normal。 限制：展示隐藏不等于安全隔离。 |
| S015（G16） | [属性 Render hints](https://www.palantir.com/docs/foundry/object-link-types/metadata-render-hints) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 应用展示提示；额外索引及重新索引的历史性能说明。 限制：索引说明明确针对 OSv1 / Phonograph，不外推到 OSv2 实现。 |
| S016（G17） | [Workshop 媒体预览组件](https://www.palantir.com/docs/foundry/workshop/widgets-media-preview) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | URL、附件和 media reference 输入；外部 URL 的 CSP；单对象属性来源与专用媒体组件。 限制：内嵌 PDF 附件不支持；未执行配置组合。 |
| S017（G18, WB05） | [Workshop Object View 组件](https://www.palantir.com/docs/foundry/workshop/widgets-object-view) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | Full / Panel 与 Standard / Configured；可选切换开关；对象接口映射；面板模式；多对象 Full 取首对象；遗留组件兼容限制。 限制：切换开关与 G03 的概览陈述存在差异；实际租户版本和交互仍需核验。 |
| S044（WB06） | [平台中的 Full Object Views](https://www.palantir.com/docs/foundry/object-views/use-full-views-in-platform) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | Full 视图与宿主集成；Explorer 到详情；面板标题打开完整详情弹窗。 限制：公开文档契约，未复现租户交互。 |
| S045（WB07, MD05） | [平台中的 Panel Object Views](https://www.palantir.com/docs/foundry/object-views/use-panel-views-in-platform) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | Vertex / Maps / Gaia 选择面板；同类型对象集面板；Workshop 面板组件。 限制：宿主支持范围依页面，不推断任意嵌入容器都具有同一上下文。 |
| S046（WB08） | [生成 Object View URL](https://www.palantir.com/docs/foundry/object-views/generate-urls) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 主键和对象 RID 链接；带 Explorer 上下文的 RID 搜索 URL 与独立链接；embedded 参数隐藏侧栏。 限制：历史 hubble 路由形式不证明内部架构；隐藏侧栏不等于完整嵌入 SDK。 |

## 遗留视图兼容文档

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S007（G07） | [遗留 Object View 配置](https://www.palantir.com/docs/foundry/object-views/config-legacy-object-views) | 发布日期未标示或未核实；遗留版本边界；检索：2026-10-01；公开正文已读；未访问租户 | 遗留编辑器、组件分区、对象/关联/聚合数据、布局及 YAML 配置复用。 限制：公开页面仍可读；不能当作当前所有 Workshop 页签的配置模式。 |
| S008（G08, WB18） | [遗留视图页签兼容配置](https://www.palantir.com/docs/foundry/object-views/config-tabs) | 发布日期未标示或未核实；遗留版本边界；检索：2026-10-01；公开正文已读；未访问租户 | 托管模块不可复用、已有独立模块可复用；不可新增遗留 builder 页签；属性/关联可见性条件与旧式列布局、过滤集合。 限制：导航位于 Legacy；其中部分兼容说明涵盖 Workshop 页签，不宜逐控件等同当前编辑器。 |
| S009（G09） | [遗留视图 Profile 配置](https://www.palantir.com/docs/foundry/object-views/config-profiles) | 发布日期未标示或未核实；遗留版本边界；检索：2026-10-01；公开正文已读；未访问租户 | 组级 Hubble 属性、页签 Profile 分配与可发现性；单 Profile 成员的默认规则；每视图最多十个 Profile。 限制：属于 Legacy 文档；不证明 Profile 可以替代数据授权。 |
| S010（G10） | [遗留应用侧栏配置](https://www.palantir.com/docs/foundry/object-views/config-app-sidebar) | 发布日期未标示或未核实；遗留版本边界；检索：2026-10-01；公开正文已读；未访问租户 | 非空且发布后显示；对象上下文参数映射到模块接口；新标签页链接卡。 限制：侧栏卡可见不等于有嵌入应用权限；不宣称所有当前 Object View 统一使用此侧栏。 |

## Object Explorer

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S020（OE-01） | [Object Explorer 总览](https://www.palantir.com/docs/foundry/object-explorer/overview) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 通用 Ontology 搜索分析入口；对象集、详情、批量 Action、跨应用打开与导出；重新打开探索取得最新结果。 限制：兼容应用示例不代表任意应用都支持跨应用传递。 |
| S021（OE-02, MD07） | [Object Explorer 入门](https://www.palantir.com/docs/foundry/object-explorer/getting-started) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 搜索对象、类型、探索和模块；类型分组和预览；超过 250 个可发现类型时的搜索范围限制。 限制：未验证实际类型排序和默认顺序。 |
| S022（OE-03） | [Object Explorer 结果过滤](https://www.palantir.com/docs/foundry/object-explorer/filter-results) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 属性、关键词和逻辑组合；有无关联、关联属性及指定关联对象过滤。 限制：未执行复杂查询；UI 能力不能直接等同外部 URL JSON 能力。 |
| S023（OE-04） | [Object Explorer 图表探索](https://www.palantir.com/docs/foundry/object-explorer/explore-charts) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 主类型/关联类型聚合；移除图表不移除过滤；布局保存；个人默认优先全局；最近五个状态撤销/重做；二十条预览卡。 限制：Explorer 布局与视图/模块版本不同；撤销页面状态不等于回滚 Action 数据。 |
| S024（OE-05, MD08） | [Object Explorer 查看结果](https://www.palantir.com/docs/foundry/object-explorer/view-results) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | Title 列打开新 Explorer 标签页详情；其他列/勾选打开右侧选择预览；多选比较；内联编辑的进入/提交条件检查。 限制：默认 Full / Panel / Legacy 的具体呈现需要结合视图文档及租户版本。 |
| S025（OE-06） | [沿关联对象切换探索](https://www.palantir.com/docs/foundry/object-explorer/pivot-linked) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 先筛选机场再切到关联航班；改变探索的主对象类型。 限制：区别于原类型上的关联属性过滤。 |
| S026（OE-07） | [比较对象集](https://www.palantir.com/docs/foundry/object-explorer/compare-object-sets) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 两组动态或已保存对象集的图表比较、联合过滤、保存和分享。 限制：区别于单对象比较；示例为同类型，分享不授予关联探索或底层数据权限。 |
| S027（OE-08） | [保存探索](https://www.palantir.com/docs/foundry/object-explorer/save-explorations) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 保存搜索参数、过滤和布局；个人目录/公开位置权限；禁止个人目录保存时关闭对应入口。 限制：保存的是查询/呈现条件；分享不授予数据权限，不承诺任意嵌入应用表单和页签状态一起保存。 |
| S028（OE-09） | [保存列表](https://www.palantir.com/docs/foundry/object-explorer/save-lists) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 静态成员名单；全体结果或显式选择；个人/公开保存位置。 限制：名单需要手动更新，不是冻结对象属性值的审计快照；分享不授予数据权限。 |
| S029（OE-10） | [Object Explorer 应用 Actions](https://www.palantir.com/docs/foundry/object-explorer/apply-actions) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 选中对象或无选择时全部结果传表单；超过 1000 个选择时不可用；参数预填歧义处理；兼容目标的跨应用打开。 限制：1000 是该 Explorer 页面所述限制，不是全部 Action API 的统一上限。 |
| S030（OE-11） | [生成 Object Explorer URL](https://www.palantir.com/docs/foundry/object-explorer/generate-urls) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 关键词、类型、探索、外部对象集与结果视角路由；当前搜索 JSON 的获取；多个属性过滤和一个关联过滤限制。 限制：文档警告 JSON 示例可能过时；未运行租户 URL 或控制台命令，不推导全部运行时状态共享。 |
| S031（OE-12） | [配置 Object Explorer](https://www.palantir.com/docs/foundry/object-explorer/configure) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 成功提示中的 Object View 链接、隐藏 Action 入口；开发中的动态对象集 Action 与安全来源 RID。 限制：开发中能力可能无自动迁移地弃用；旧式组件/UI 不当作稳定通用契约。 |

## 对象模型、权限与 API

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S032（OE-13） | [平台中的 Actions](https://www.palantir.com/docs/foundry/action-types/use-actions) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 单对象引用/引用列表对应单个或批量上下文；按参数对象类型匹配；Explorer 自动发现入口。 限制：Object View 的 Actions 区域示例带历史形态，不保证所有当前视图位置和 UI 相同。 |
| S033（OE-14） | [Action 类型权限](https://www.palantir.com/docs/foundry/action-types/permissions) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 查看、编辑、执行分开；提交条件与类型/数据源可见性；Action 外部编辑的额外权限。 限制：结合对象安全及读写授权可用性解释，不能压成页面可见权限。 |
| S034（OE-15） | [Action 读写授权](https://www.palantir.com/docs/foundry/action-types/read-write-authorizations) | 发布日期未标示或未核实；Beta；检索：2026-10-01；公开正文已读；未访问租户 | 公开文档明确标 Beta，未必全部 enrollment 开启。 限制：本篇仅引用可用性边界，没有验证全部细节或某租户已开启。 |
| S035（OE-16） | [对象权限总览](https://www.palantir.com/docs/foundry/object-permissioning/overview) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | Ontology schema 资源与 objects / links 数据分两层授权。 限制：对象类型定义与实例数据不是同一授权资源。 |
| S036（OE-17） | [Ontology 项目权限](https://www.palantir.com/docs/foundry/object-permissioning/ontology-permissions) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | Ontology 资源位于 Compass project，项目决定查看、编辑、管理权限；新 Ontology 启用项目权限，既有 Ontology 需 owner 手动启用并迁移。 限制：当前不支持 Default Ontologies；未迁移情形仍需区分旧模型，不能以 Legacy 页面代替当前项目机制。 |
| S037（OE-18） | [管理对象安全](https://www.palantir.com/docs/foundry/object-permissioning/managing-object-security) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 对象/属性政策与数据源政策；单元格级授权的行/列层次。 限制：未测试受限属性聚合、关联过滤、保存分享的实际 UI 退化。 |
| S038（OE-19） | [API v2：Object Set 基础](https://www.palantir.com/docs/foundry/api/v2/ontologies-v2-resources/ontology-object-sets/ontology-object-set-basics) | 发布日期未标示或未核实；API v2；检索：2026-10-01；公开正文已读；未访问租户 | Object Set 表示 Ontology 中的对象组，并可对多个对象操作。 限制：概念定义不证明 Explorer 内部源码或持久化结构。 |
| S039（OE-20） | [API v2：加载对象集](https://www.palantir.com/docs/foundry/api/ontologies-v2-resources/ontology-object-sets/load-object-set) | 发布日期未标示或未核实；API v2；检索：2026-10-01；公开正文已读；未访问租户 | 定义输入与分页对象输出分离；API 的快照分页参数；OSv1 / OSv2 加载限制。 限制：未调用 API；不把快照分页外推为 Explorer 列表冻结属性，也不将 API 限制套 UI。 |
| S040（OE-21） | [API v2：临时对象集](https://www.palantir.com/docs/foundry/api/v2/ontologies-v2-resources/ontology-object-sets/create-temporary-object-set) | 发布日期未标示或未核实；API v2 Preview；检索：2026-10-01；公开正文已读；未访问租户 | 创建临时对象集并返回 RID；一小时过期。 限制：明确 Preview，可改变或移除；未调用此写入 API，不能替代持久探索/列表。 |
| S078（X01） | [Ontology 驱动应用总览](https://www.palantir.com/docs/foundry/ontology/applications) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | Ontology 上的多种应用入口及其关系；正文的对象中心应用定义 限制：入口关系概览，不证明 Object Views 内部源码。 |

## Workshop 组合与状态

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S047（WB09） | [Workshop 模块接口](https://www.palantir.com/docs/foundry/workshop/module-interface) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 父变量所有权；URL 调用值和首次初始化；嵌入接口；打开模块事件；Carbon 参数命名。 限制：Workshop 模块接口与 Ontology Interface 是不同概念。 |
| S048（WB10） | [Workshop 嵌入模块组件](https://www.palantir.com/docs/foundry/workshop/embedded-modules) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 加载已发布子模块；变量全映射时共享当前值；父变量定义/默认/重算与编辑调试。 限制：子变量更新传播的措辞与 WB11 有差异，需保留双方。 |
| S049（WB11） | [Workshop 模块嵌入概览](https://www.palantir.com/docs/foundry/workshop/embedding-workshop-modules-overview) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 子模块分别鉴权；设置不继承；事件配置不能传入；跨模块通信。 限制：概览与嵌入模块组件对变量更新传播表述不同，不能扩大成任意事件和设置共享。 |
| S050（WB12） | [Workshop 事件](https://www.palantir.com/docs/foundry/workshop/concepts-events) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 打开 Object View / Explorer；Carbon 标签页与浏览器标签页；刷新模块数据；执行顺序。 限制：事件顺序不保证下游数据计算完成。 |
| S051（WB13） | [Workshop 路由](https://www.palantir.com/docs/foundry/workshop/routing) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 页面/变量 URL 状态；URL 写入与初始化；单 RID 对象集；嵌入模块限制。 限制：不能直接表达对象集过滤，也不继承全部嵌入路由状态。 |
| S052（WB14） | [Workshop 状态保存](https://www.palantir.com/docs/foundry/workshop/state-saving) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 显式保存；手动、链接或默认已保存状态加载；原生 Text / Date 等未填完表单变量；稳定 external ID；选择和详情示例。 限制：默认保存状态自动应用不等于持续自动保存。子模块不继承状态保存设置；需要平台入口和模块头部。 |
| S053（WB15） | [Workshop 使用 Actions](https://www.palantir.com/docs/foundry/workshop/actions-use) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 复用 Action 类型；生成表单；变量默认参数；开始/成功事件链。 限制：Action 成功事件不自动证明跨宿主数据已经刷新。 |
| S054（WB16） | [Workshop 内联 Action 表单](https://www.palantir.com/docs/foundry/workshop/widgets-inline-action-form) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 表单/表格配置、成功事件和输出对象集。 限制：具体可执行性仍依 Action 与数据授权。 |
| S055（WB17） | [Workshop 权限](https://www.palantir.com/docs/foundry/workshop/concepts-permissions) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 模块与数据、Actions、functions 分开；读取时可见性及权限检查。 限制：模块访问权不能替代数据或 Action 执行权。 |
| S056（WB19） | [Workshop 自动刷新](https://www.palantir.com/docs/foundry/workshop/auto-refresh) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 对象集监视触发模块重载；OSv2 范围与独立 iframe 选项。 限制：重载会影响用户输入；隔离 iframe 选项不证明完整应用运行时实现。 |
| S105（X05） | [Workshop 拖放](https://www.palantir.com/docs/foundry/workshop/drag-and-drop) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | Explorer 与 Workshop 拖放工作流的官方核对入口 限制：不由候选视频推断全部租户默认启用；不声称复现拖放。 |

## Carbon 宿主

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S057（WB20） | [Carbon Workspace 总览](https://www.palantir.com/docs/foundry/carbon/workspaces-overview) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 策展应用/资源入口，承接对象工作流。 限制：宿主定位不证明 Object View 必须依赖 Carbon。 |
| S058（WB21） | [Carbon 模块总览](https://www.palantir.com/docs/foundry/carbon/modules-overview) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | Carbon 标签页中的参数化应用；输入/输出组合。 限制：只据公开组合契约，不推断内部状态桥接。 |
| S059（WB22） | [Carbon 模块导航](https://www.palantir.com/docs/foundry/carbon/modules-navigation) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | Explorer 列表到独立 Object View 标签页；详情的单对象上下文；Workshop 参数命名与变量限制。 限制：页面仍用 Explorer 例子，当前入口变化需同时看 2026-09 公告。 |
| S060（WB23, MD09） | [Carbon 模块发现配置](https://www.palantir.com/docs/foundry/carbon/modules-discovery) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 可发现模块注册；Object Set 接口 external ID；可选对象类型约束；工作区内外发现范围。 限制：类型约束可选，不能写成统一必需；不证明 Object View 依赖 Carbon。 |
| S061（WB24） | [Carbon 权限配置](https://www.palantir.com/docs/foundry/carbon/permissions-configure) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 工作区与其内部资源分别控制访问。 限制：可访问工作区不自动授予所有内容权限。 |
| S062（WB25） | [Carbon 限制工作区导航](https://www.palantir.com/docs/foundry/carbon/restrict-workspace-nav) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 宿主外部导航控制。 限制：不能消除模块内部的外部链接。 |
| S063（WB26） | [Carbon 工作区历史](https://www.palantir.com/docs/foundry/carbon/workspaces-history) | 发布日期未标示或未核实；检索：2026-10-01；公开正文已读；未访问租户 | 工作区独立版本历史。 限制：不是 Object View 或 Workshop 模块版本的替代。 |

## 有日期官方公告

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S013（G14） | [2026 年 2 月：Core Object Views 正式可用](https://www.palantir.com/docs/foundry/announcements/2026-02) | 发布/讨论：2026-02-19；检索：2026-10-01；公开正文已读；未访问租户 | 2026-02-19 公告 Core 自动默认详情正式面向各 enrollment 可用；专用属性/关联展示；Core / custom 与 Full / Panel 并存。 限制：历史原词为 Core / custom；不是 Object Views 首次发布日期，也没有给出改名 Standard 的日期。 |
| S018（G19） | [2024 年 4 月：新页签只用 Workshop 构建](https://www.palantir.com/docs/foundry/announcements/2024-04) | 发布/讨论：2024-04-02；检索：2026-10-01；公开正文已读；未访问租户 | 2024-04-02 停止新增遗留 builder 页签，已有页签继续支持；新类型默认单页签属性/关联详情由 Workshop 支撑；可嵌入已有模块。 限制：这是历史默认配置，不能证明 2026 Standard 发布后的资源迁移实现。 |
| S019（G20） | [2026 年 1 月：Object Views 支持分支开发](https://www.palantir.com/docs/foundry/announcements/2026-01) | 发布/讨论：2026-01-29；检索：2026-10-01；公开正文已读；未访问租户 | 2026-01-29 支持分支结构、内容、预览和变基；当时变更自动批准，审批/主线保护列为后续方向。 限制：历史审批限制不能替代 G11 的当前公开文档。 |
| S064（WB27） | [2026 年 9 月：Carbon 的 Insight 探索](https://www.palantir.com/docs/foundry/announcements/2026-09#explore-ontology-data-in-carbon-with-insight-analysis) | 发布/讨论：2026-09-21；检索：2026-10-01；公开正文已读；未访问租户 | 2026-09-21 公告 Insight 分析和现代对象搜索分别选择开启；启用后替代旧 Explorer 风格探索。 限制：已有工作区继续选择开启；新工作区未来默认是计划，不能写成已全面默认。 |

## 公开社区

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S041（OE-22） | [社区：可点击对象 RID](https://community.palantir.com/t/clickable-object-rid/2228) | 发布/讨论：2024-12-16；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | 2024 年用户将对象 RID 误当文件资源 RID；回复建议显式 Object View URL 与 Workshop URL Redirect 列。 限制：历史用户/作者观察，不证明 2026 Explorer 永远不支持某种链接。 |
| S066（MC01） | [社区：对象集的 Object View](https://community.palantir.com/t/object-view-for-sets-of-objects/3749) | 发布/讨论：2025-05–2025-11；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | 2025 年 5—11 月对象集入口讨论；11 月 19 日 jen 自称 Object View Team，宣布对象集面板与三种模式。 限制：身份未独立验证；现状以当前官方面板/组件文档为准，五月缺口不能写成当前限制。 |
| S067（MC02） | [社区：嵌入视图的 external ID](https://community.palantir.com/t/object-views-custom-external-id-support-for-interface-variables-of-that-object-type-when-embedding-workshop-modules/1073) | 发布/讨论：2024-08-20；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | 旧 Object View tab 的 object external ID 与普通父 Workshop 映射摩擦。 限制：2024-08-20 历史用户报告；原截图链接已读但未本地化，不证明当前所有视图限制。 |
| S068（MC03） | [社区：按钮切换 Object View 页签](https://community.palantir.com/t/navigate-to-different-object-view-tab-with-button/1111) | 发布/讨论：2024-08-22；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | 历史外层视图页签与内层 Workshop tabs 的导航差异。 限制：2024-08-22 回复，不是当前功能保证。 |
| S069（MC04） | [社区：属性改名与 Add all](https://community.palantir.com/t/add-all-object-properties-to-workshop-widget-even-after-name-change/2665) | 发布/讨论：2025-01-28；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | 2025-01-28 Workshop 显式属性列表不会自动加入后续 schema 属性的使用讨论。 限制：历史行为；不能替代当前自动默认视图机制。 |
| S070（MC05） | [社区：变量目录与应用拆分](https://community.palantir.com/t/variable-folders/3017) | 发布/讨论：2025-02-28；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | 2025-02-28 以子应用、Object Views、嵌入及 Carbon 组合的架构经验。 限制：社区建议，作者角色未独立验证，不是官方架构承诺。 |
| S071（MC06） | [社区：保存 Object View 故障](https://community.palantir.com/t/can-t-save-new-object-view-anymore/4802) | 发布/讨论：2025-08-18；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | 2025-08-18 自动保存/发布区别与当日修复回复。 限制：已解决的历史问题不能列为持续故障；此前 Palantir 任职为本人自述。 |
| S072（MC07） | [社区：关闭 Explorer 的 Actions](https://community.palantir.com/t/turn-off-actions-from-object-explorer/144) | 发布/讨论：2024-04; follow-up 2026-01；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | hubble-oe:hide-action 的历史呈现控制；2026 年 1 月追问。 限制：历史入口隐藏不等于安全规则；后续追问无新答案。 |
| S073（MC08） | [社区：列表与探索的区别](https://community.palantir.com/t/saved-list-versus-saved-exploration/2020) | 发布/讨论：2024-11；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | 2024 年 11 月动态工作队列案例。 限制：正式语义回到官方保存文档。 |
| S074（MC09） | [社区：发现权限与对象记录](https://community.palantir.com/t/records-in-search-object-discover-access-only/4875) | 发布/讨论：2025-08-27；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | 2025-08-27 用户自述获应用访问仍无对象数据权限。 限制：用户报告，未做受控租户验证。 |
| S075（MC10） | [社区：Explorer 分支切换](https://community.palantir.com/t/object-explorer-switch-branches/5034) | 发布/讨论：2025-09-15；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | 2025-09-15 旧 Explorer 未识别分支与现代化方向的讨论。 限制：历史和路线图评论不是当前状态证明。 |
| S076（MC11） | [社区：Explorer 到 Workshop 拖放](https://community.palantir.com/t/question-regarding-drag-and-drop-workflow-from-object-explorer-to-workshop/6721) | 发布/讨论：2026-06-04；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | 2026-06-04 DevCon 片段线索；放置区可能需要平台管理员开启的回复。 限制：不推断各租户默认启用；当前机制看官方拖放文档。 |
| S077（MC12） | [社区：遗留视图的属性菜单](https://community.palantir.com/t/object-view-as-configured-in-legacy-object-view/3708) | 发布/讨论：2025-04-28；检索：2026-10-01；公开讨论正文已读；作者身份未独立验证 | 2025-04-28 遗留属性搜索及省略号菜单的用户问题和截图链接。 限制：没有有效答案，不能把问题改写成已验证的功能缺失。 |

## 公开视频

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S042（OE-23, MV01） | [Ontologize：Object Explorer 入门视频](https://www.youtube.com/watch?v=YuT96FVeDuc) | 发布/讨论：2024-10-17；检索：2026-10-01；浏览器标题/频道/日期/描述/章节已读；无已验证内容帧 | 公开浏览器核实标题、作者频道、2024-10-17 上传日期、描述和章节；时长显示 15:18；教学虚构数据。 限制：作者频道；未验证其自述 Partner 身份。播放器失败、字幕不可用，无内容帧、完整观看或录屏交付。 |
| S065（MV02） | [候选视频：DevCon 4 对象驱动应用构建](https://www.youtube.com/watch?v=Cgn52Qqgxeg) | 发布日期未标示或未核实；检索：2026-10-01；仅搜索标题；直接页面被节流 | 公开搜索标题与社区拖放演示线索；帖子文字 16:08，t=972 实为 16:12。 限制：直接页面读取被节流；频道、上传日、字幕、画面未核实，无取帧或完整观看证据。 |

## 培训目录

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S043（OE-24） | [Palantir Learn：数据分析师培训目录](https://learn.palantir.com/page/training-track-data-analyst) | 发布日期未标示或未核实；检索：2026-10-01；搜索目录元数据；直接正文 Internal Error | 搜索索引显示目录收录 Ontologize 入门视频。 限制：直接读取报 Internal Error；目录收录不改变作者归属，不声称完成课程。 |

## 技术博客

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S083（X02） | [Zenn：Palantir Ontology 与 DevRev 比较](https://zenn.dev/knowledge_graph/articles/palantir-ontology-vs-devrev) | 发布/讨论：2026-07-28；初版历史记 2026-07-27；检索：2026-10-01；公开文章正文已读；身份为自述 | 跨产品比较中的共同对象语义、多种探索/操作入口问题框架 限制：作者自述为 DevRev 日本工程师，声明 AI 辅助/英译；技术事实回到官方来源，不采用规模、存储和一致性泛化。 |

## 官方公开源码

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S084（X03） | [官方 OSDK 教学源码：Home.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/examples/example-tutorial-todo-app-sdk-2.x/src/Home.tsx) | 固定提交：`fb8ec172d540ef7819382ff036aa2a692614af75`；提交日期未登记；检索：2026-10-01；固定提交源码已读；未执行 | 所选 project 传给任务列表和操作入口；示例明确使用 in-memory mock，留给学员改用 OSDK 限制：不证明 Object View 运行时或真实 Ontology 写回。 |
| S085（X04） | [官方 OSDK 教学源码：TaskListItem.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/examples/example-tutorial-todo-app-sdk-2.x/src/TaskListItem.tsx) | 固定提交：`fb8ec172d540ef7819382ff036aa2a692614af75`；提交日期未登记；检索：2026-10-01；固定提交源码已读；未执行 | 组件调用传入的删除 callback 并控制 loading 状态 限制：callback 不证明已经调用 Ontology Action；不当作真实写回验收。 |

## 未读取正文的候选

| 编号（原编号） | 来源 | 日期、版本与实际访问 | 支持范围及限制 |
|---|---|---|---|
| S106（X06） | [CSDN：Palantir Ontology 范式讨论（未用作证据）](https://blog.csdn.net/u014177256/article/details/159086063) | 发布日期未标示或未核实；检索：2026-10-01；搜索摘要；正文 Internal Error | 限制：只记候选和访问限制；未用于技术能力结论，未复制配图。 |

## 章节深链

以下深链的基页已有公开正文读取记录；未另行测试精确锚点能否定位。它们支持正文引用的相应章节，适用范围和版本边界继承基页；不能由“已登记”推断“已逐链接浏览验证”。

| 编号 | 章节链接 | 基页原编号 | 检索与访问 |
|---|---|---|---|
| S079（D01） | [Configured Object Views 配置概览：默认配置](https://www.palantir.com/docs/foundry/object-views/config-overview#default-configurations) | G03, WB02, MD02 | 2026-10-01；基页正文已读，锚点未另测 |
| S080（D02） | [Workshop Object View 组件：形态配置选项](https://www.palantir.com/docs/foundry/workshop/widgets-object-view#form-factor-configuration-options) | G18, WB05 | 2026-10-01；基页正文已读，锚点未另测 |
| S081（D03） | [Configured Object Views 配置概览：权限](https://www.palantir.com/docs/foundry/object-views/config-overview#permissions) | G03, WB02, MD02 | 2026-10-01；基页正文已读，锚点未另测 |
| S082（D04） | [Workshop 状态保存：设置默认已保存状态](https://www.palantir.com/docs/foundry/workshop/state-saving#setting-a-default-saved-state) | WB14 | 2026-10-01；基页正文已读，锚点未另测 |
| S086（D05） | [Configured Full Object View：编辑视图页签](https://www.palantir.com/docs/foundry/object-views/config-object-views#edit-object-view-tabs) | G05, WB03, MD03 | 2026-10-01；基页正文已读，锚点未另测 |
| S087（D06） | [Configured Panel Object View：编辑配置面板](https://www.palantir.com/docs/foundry/object-views/config-panel-views#edit-configured-panel-object-views) | G06, WB04, MD04 | 2026-10-01；基页正文已读，锚点未另测 |
| S088（D07） | [Workshop Object View 组件：配置选项](https://www.palantir.com/docs/foundry/workshop/widgets-object-view#configuration-options) | G18, WB05 | 2026-10-01；基页正文已读，锚点未另测 |
| S089（D08） | [平台中的 Full Object Views：平台应用](https://www.palantir.com/docs/foundry/object-views/use-full-views-in-platform#platform-applications) | WB06 | 2026-10-01；基页正文已读，锚点未另测 |
| S090（D09） | [Workshop 嵌入模块组件：模块选择](https://www.palantir.com/docs/foundry/workshop/embedded-modules#module-selection) | WB10 | 2026-10-01；基页正文已读，锚点未另测 |
| S091（D10） | [Workshop 模块嵌入概览：嵌入模块权限](https://www.palantir.com/docs/foundry/workshop/embedding-workshop-modules-overview#permission-of-embedded-modules) | WB11 | 2026-10-01；基页正文已读，锚点未另测 |
| S092（D11） | [Workshop 模块接口：嵌入模块接口](https://www.palantir.com/docs/foundry/workshop/module-interface#embedded-module-interface) | WB09 | 2026-10-01；基页正文已读，锚点未另测 |
| S093（D12） | [Workshop 嵌入模块组件：接口映射配置](https://www.palantir.com/docs/foundry/workshop/embedded-modules#interface-configuration) | WB10 | 2026-10-01；基页正文已读，锚点未另测 |
| S094（D13） | [Workshop 模块嵌入概览：事件传递](https://www.palantir.com/docs/foundry/workshop/embedding-workshop-modules-overview#event-passing) | WB11 | 2026-10-01；基页正文已读，锚点未另测 |
| S095（D14） | [Workshop 模块嵌入概览：跨嵌入模块通信](https://www.palantir.com/docs/foundry/workshop/embedding-workshop-modules-overview#communicating-across-embedded-modules) | WB11 | 2026-10-01；基页正文已读，锚点未另测 |
| S096（D15） | [Workshop 事件：应用事件](https://www.palantir.com/docs/foundry/workshop/concepts-events#applications) | WB12 | 2026-10-01；基页正文已读，锚点未另测 |
| S097（D16） | [Workshop 模块接口：打开 Workshop 模块事件](https://www.palantir.com/docs/foundry/workshop/module-interface#open-workshop-module-event) | WB09 | 2026-10-01；基页正文已读，锚点未另测 |
| S098（D17） | [生成 Object View URL：生成对象链接](https://www.palantir.com/docs/foundry/object-views/generate-urls#generate-object-links) | WB08 | 2026-10-01；基页正文已读，锚点未另测 |
| S099（D18） | [Workshop 使用 Actions：事件与 Action 串联](https://www.palantir.com/docs/foundry/workshop/actions-use#chaining-an-event-with-an-action) | WB15 | 2026-10-01；基页正文已读，锚点未另测 |
| S100（D19） | [Workshop 内联 Action 表单：配置](https://www.palantir.com/docs/foundry/workshop/widgets-inline-action-form#configuration) | WB16 | 2026-10-01；基页正文已读，锚点未另测 |
| S101（D20） | [Workshop 模块嵌入概览：子模块设置不继承](https://www.palantir.com/docs/foundry/workshop/embedding-workshop-modules-overview#no-module-settings-inheritance-of-child-modules) | WB11 | 2026-10-01；基页正文已读，锚点未另测 |
| S102（D21） | [Workshop 状态保存：限制](https://www.palantir.com/docs/foundry/workshop/state-saving#limitations) | WB14 | 2026-10-01；基页正文已读，锚点未另测 |
| S103（D22） | [Workshop Object View 组件：核心配置选项](https://www.palantir.com/docs/foundry/workshop/widgets-object-view#core-configuration-options) | G18, WB05 | 2026-10-01；基页正文已读，锚点未另测 |
| S104（D23） | [Carbon 模块导航：Workshop 导航](https://www.palantir.com/docs/foundry/carbon/modules-navigation#workshop) | WB22 | 2026-10-01；基页正文已读，锚点未另测 |

## 访问限制与未获证据

来源登记完整不代表所有来源都能读取正文。CSDN 正文返回 Internal Error，未作为技术能力、作者或日期证据；Palantir Learn 目录仅有搜索元数据；DevCon 候选视频直接页面被节流。Ontologize 视频只有公开元数据，播放器报错，最终 `readyState=0`、`videoWidth=0`，字幕导出不可用。没有绕过访问限制。

社区公开讨论正文可读，部分 profile 页面返回 403。人员职务和 Partner / 团队身份按自述标记，未独立核实；历史问题与路线图不当作检索日已交付能力。

尚未获得真实租户中默认视图选择、切换开关、跨宿主状态、Action 完成到数据刷新、分支主线保护和内部分页/上下文注入的运行证据。没有公开完整 Object Views / Explorer 前端实现的证据。官方 OSDK 教学示例已读但未执行，mock 与 callback 均不证明平台 Action 写回。

## 登记核对

- 已核对 [主文](README.md)及五篇附录，共 272 次直接技术外链引用、104个规范化去重URL（去末尾slash、保留query与fragment）；原始逐字符URL共111个；遗漏 **0**。
- 原始编号保留：G 系列 19、OE 系列 24、WB 系列 27、媒体系列 23；原始重复记录归并 16 条。
- 补充编号 X01—X06 对应六个新增整页/源码，D01—D23 对应章节深链；原来源编号未重写。
- 所有发布日期、版本标识和访问限度按既有证据登记；章节锚点未独立测试，视频未声称内容观看，源码未声称执行。
