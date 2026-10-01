# Object Views 的默认机制、配置与发布治理

> 检索日：2026-10-01。资料基线为当日可公开访问的 Palantir 英文官方文档及带日期的官方公告。本文没有登录 Foundry 租户；文档行为不等于租户实测。当前文档未公开其产品构建号，以下“当前”指检索日文档，“历史”指带日期公告或被官方导航归入 Legacy 的配置路径。

## 1. 研究结论

Object View 是绑定对象类型的可复用展示契约。当前官方概览把它分为 Standard 与 Configured；二者都有 Full 与 Panel 形态。Standard 保证对象类型无需额外页面配置即可查看，Configured 借助 Workshop 组织特定工作流，创建后成为默认展示，但 Standard 仍保留。[G01：Overview](https://www.palantir.com/docs/foundry/object-views/overview/)

因此，研究与架构建模至少需要分开四个维度：**展示族类**（Standard / Configured）、**尺寸与宿主形态**（Full / Panel）、**配置所有权**（自动配置 / 用户管理 / 独立复用模块）、**配置代际**（当前 Workshop 编辑器 / Legacy builder）。“default”是某一层的默认选择或初始配置，不能当作第三种稳定的展示族类；“Legacy”也不等同于自动创建的 Standard。[G01](https://www.palantir.com/docs/foundry/object-views/overview/) [G03：Configured overview](https://www.palantir.com/docs/foundry/object-views/config-overview/) [G08：Configure tabs](https://www.palantir.com/docs/foundry/object-views/config-tabs/)

Object View 外层结构与每个 Workshop 模块分别有版本；编辑过程中模块可以周期性自动保存，但未发布的 Object View 变化不会向浏览者生效。分支又将页签结构和模块内容作为不同资源处理。对于 EOS，价值主要是对象详情入口的契约、配置所有权、复用边界和发布治理，而非再增加一个页面编辑器。[G04：Manage versions](https://www.palantir.com/docs/foundry/object-views/manage-versions/) [G11：Branching](https://www.palantir.com/docs/foundry/object-views/branching-object-views/) 后半句为架构分析。

## 2. Standard、Core、Configured、Default、Legacy 的词义与张力

| 词语 | 已核实含义与时间范围 | 不应混同的概念 | 直接来源 |
|---|---|---|---|
| **Standard Object View** | 当前概览中，与对象类型配置同步的开箱即用展示；所有对象类型可用 | 已定制的 Workshop 业务页；Legacy builder | [G01](https://www.palantir.com/docs/foundry/object-views/overview/) |
| **Core Object View** | 2026-02-19 GA 公告使用的原词；公告描述自动创建、显著属性及关联展示、与 custom 并存、Full / Panel | 不能将 GA 日期写成 Object Views 整个产品首次发布日 | [G14：February 2026](https://www.palantir.com/docs/foundry/announcements/2026-02/) 的 “Core Object Views are now generally available” |
| **Configured Object View** | 当前用 Workshop 模块构建的定制展示，按对象类型复用；发布的修改适用于该类型全部对象 | 每个对象各存一份页面配置；通用对象集合探索应用 | [G03](https://www.palantir.com/docs/foundry/object-views/config-overview/) |
| **Default view** | 当前概览：未创建 Configured 时默认 Standard；创建 Configured 后其成为默认，仍可回到 Standard | “默认”为独立对象种类；创建后 Standard 消失 | [G01](https://www.palantir.com/docs/foundry/object-views/overview/) |
| **Default configured view** | 当前配置页仍写：每类型自动生成初始 full/panel，随属性增加和重命名动态更新；编辑后转用户管理，后续手动更新 | 不能据此断言 Standard 一旦定制便永久停止同步 | [G03](https://www.palantir.com/docs/foundry/object-views/config-overview/) 的 “Default configurations” |
| **Legacy Object View / builder** | 当前官方导航保留旧配置章节；旧 widget-based tab 仍支持，Legacy builder 页签不能再新增；可从管理页签对话框进入 legacy editor | Legacy builder 不是所有 Object View tab；其章节里也有 Workshop tabs 的兼容说明 | [G07：Legacy config](https://www.palantir.com/docs/foundry/object-views/config-legacy-object-views/) [G08](https://www.palantir.com/docs/foundry/object-views/config-tabs/) |

**命名沿革的证据边界。** 2026-02-19 公告使用 Core / custom，检索日文档使用 Standard / configured，功能描述高度对应。可以报告“公告词汇与当前文档词汇不同”，并在历史图注保留 Core；本次没有找到宣布正式改名的日期，不应补造一条“Core 在某日更名 Standard”的发布事件。[G14](https://www.palantir.com/docs/foundry/announcements/2026-02/) [G01](https://www.palantir.com/docs/foundry/object-views/overview/)

**当前文档内部张力。** 同一份 Configured overview 一方面说明“创建 Configured 后成为默认”，另一方面说明“每类型自动创建 default configured”。两段没有解释当前 Standard rollout 后的兼容实现、初始 configured 是否延迟物化、或采用条件。稳妥写法是：以当前概览说明用户可见的双轨机制，同时把 default configured 的同步/接管规则作为配置文档的明确陈述及待租户核验事项。不能强行画成 Standard → 编辑 → Configured 的唯一状态机，也不能推断“一个编辑动作必然复制或覆盖哪个服务端资源”。[G03](https://www.palantir.com/docs/foundry/object-views/config-overview/)

**历史上下文能解释词汇，不能替代当前验证。** 2024-04-02 官方公告明确新 Object View tabs 只能由 Workshop 构建，已有 Legacy tabs 继续支持；新类型默认详情由 Workshop 支撑，单 tab 展示属性与链接，同时允许嵌入已有 Workshop module。这个历史节点与“default configured”的初始布局相符，但不证明 2026 Standard 上线后旧资源的物化或迁移过程。[G19：April 2024](https://www.palantir.com/docs/foundry/announcements/2024-04/) 的 “New object view tabs are now built solely in Workshop”

**Workshop 切换能力也有文档差异。** Configured overview 说 Workshop 尚不可 toggle；专门的 Object View widget 页则写 builder 可选 Standard / Configured，并在 Object View Mode 提供 optional toggle。本文以专门 widget 页面记录其可配置选项，同时保留 overview 的反向陈述；实际 tenant/rollout 及用户 toggle 可用性仍待核验，不能一概写“Workshop 不支持”。[G03](https://www.palantir.com/docs/foundry/object-views/config-overview/) [G18：Workshop Object View widget](https://www.palantir.com/docs/foundry/workshop/widgets-object-view/)

### 有明确日期的发布节点

| 日期 / 文档状态 | 已核实节点 | 解释边界 | 官方来源 |
|---|---|---|---|
| 2024-04-02 | 新 tabs 统一使用 Workshop；Legacy 仅保留存量；新类型默认单 tab 由 Workshop 构建 | 是 builder 的迁移节点，不是 Object Views 首次推出 | [G19：April 2024](https://www.palantir.com/docs/foundry/announcements/2024-04/) |
| 2026-01-29 | Object Views 加入 Foundry Branching，支持结构/内容变更、跨应用预览和 rebase | 当时明确所有 OV branch 变更自动批准，审批集成尚未支持；reviewers/policies/main protection 属 roadmap | [G20：January 2026](https://www.palantir.com/docs/foundry/announcements/2026-01/) |
| 2026-02-19 | Core Object Views GA，自动展示与 custom 并存 | 历史原词保留 Core / custom；不补造正式改名日 | [G14：February 2026](https://www.palantir.com/docs/foundry/announcements/2026-02/) |
| 2026-10-01 检索日 | 当前文档为 Standard / Configured；OV branching 已有审批和项目策略继承 | 仍把 inherited main resource protection 标为 under development；不同于 1 月的“全部自动批准” | [G01](https://www.palantir.com/docs/foundry/object-views/overview/) [G11](https://www.palantir.com/docs/foundry/object-views/branching-object-views/) |

## 3. Standard 的属性、媒体和关联展示

Standard 根据 **属性 visibility 与 base type** 展示：prominent 置于上部，normal 进入普通表格，hidden 不显示。Prominent media reference 使用专门媒体查看器；time series 使用交互图表；显著 geohash、geoshape、GTSR 和表达经纬度随时间变化的 time series 可进入 Map；其他显著属性使用较大卡片。这里的自动媒体选择是标准视图文档明确的 base-type 行为，不应全部泛称“render hints”。[G02：Standard Object Views](https://www.palantir.com/docs/foundry/object-views/standard-object-views/)

Linked objects 组件按 link type 分组，支持原位属性预览、把一部分关联对象开到新 tab、在侧栏预览选中对象；Standard 的 Panel 也提供这些能力。它使默认详情本身具有沿业务关系继续探查的入口。[G02](https://www.palantir.com/docs/foundry/object-views/standard-object-views/)

Ontology 属性元数据另有 title key、base type、value / conditional formatting、type classes、render hints、visibility 等层。Title key 提供对象显示名称；visibility 默认 normal。Render hints 是应用展示和部分索引能力的提示，例子包括 long text、keywords、identifier、sortable。**其性能页多处明确讨论 Object Storage v1 / Phonograph 的额外索引与 reindex，不可直接外推成当前 OSv2 的索引实现。**[G15：Property metadata](https://www.palantir.com/docs/foundry/object-link-types/property-metadata/) [G16：Render hints](https://www.palantir.com/docs/foundry/object-link-types/metadata-render-hints/)

**EOS 架构分析：**元数据驱动的“可用默认详情”可以把首个业务对象展示的成本压低；业务定制仍需独立所有权。隐藏字段是展示描述，不能替代数据、对象及 Action 的授权验证。本次资料未证明 hidden 是安全隔离机制。

## 4. 从 Ontology Manager 到 Workshop 配置：治理边界

Ontology Manager 的对象类型 **Object views** tab 可预览详情、固定一个默认预览对象、切换 full/panel 与 light/dark；右侧 Edit 进入配置编辑器。这个“默认 display object”是编辑预览样本，不是用户默认详情族类。Object Explorer 的 More → Advanced → Edit object view 和嵌入 Panel 的 ellipsis → Edit 是同一配置体系的其他入口；Panel 的编辑菜单只向有编辑权限的用户出现。[G03](https://www.palantir.com/docs/foundry/object-views/config-overview/)

当前 Full 编辑器区分 **Object View 页签结构** 与 **每个页签的 Workshop 内容**。Header 显示 Ontology、对象类型、形态及两个版本号；对象标题栏齿轮管理 tabs。页签可新增、重排、改名、删除，删除页签会删除其包含的模块；仅一个页签时浏览态隐藏页签标题。内容按普通 Workshop 模块构建，布局与动态变量的能力由 Workshop 提供。[G05：Configure full views](https://www.palantir.com/docs/foundry/object-views/config-object-views/)

Panel 要进一步区分单对象 **Object instance** 与同一对象类型多实例的 **Object set**。初始 instance panel 是 prominent Property List；初始 set panel 有 Charts（最多五个 XY charts）和 List（每对象最多三个属性，含 title/prominent/media）两种入口。编辑器分辨率预设与手动尺寸只用于近似预览，实际尺寸取决于宿主与设备；它不是固定像素的运行保证。[G06：Configure panel views](https://www.palantir.com/docs/foundry/object-views/config-panel-views/)

**媒体的 configured 路径。** 页签继承 Workshop 的构建能力，媒体需要选用具体 widget 和输入契约。Media Preview 可显示图像、音频、视频、文档；来源包括 media URL、attachment property、media reference property，属性来源要求单对象 Object Set。外部 URL 受 enrollment 的 CSP 设置约束；PDF 内嵌附件不在 Media Preview 支持范围。PDF Viewer、Video Display、Audio and Transcription 等专用 widgets 另有对应增强能力。[G17：Media Preview](https://www.palantir.com/docs/foundry/workshop/widgets-media-preview/) 结合 [G05](https://www.palantir.com/docs/foundry/object-views/config-object-views/) 的 Workshop-backed tab；这是可组合的文档能力，不是本次已运行的示例。

## 5. Managed、Standalone 和 Legacy 配置的差异

| 路径 | 所有权与复用 | 可核实的边界 | 来源 |
|---|---|---|---|
| **OV-managed Workshop tab** | 权限随 Object View / 对象类型同步；不能跨 Object Views 重用这个 managed module | 绑定详情所有权；变成独立 module 需 legacy 配置中的手动转换 | [G08](https://www.palantir.com/docs/foundry/object-views/config-tabs/) [G03](https://www.palantir.com/docs/foundry/object-views/config-overview/) |
| **Existing / standalone Workshop tab** | 可以把已建模块嵌入多个 Object Views | 不能据 managed 默认继承规则推断独立模块也自动同权；应核对独立模块的权限和发布 | [G08](https://www.palantir.com/docs/foundry/object-views/config-tabs/)；后一项为风险分析 |
| **Legacy widget-based tab** | 按 sections 组织 widgets；配置 current object、linked objects、linked aggregates 等数据 | 仍可编辑既有 tab；不能新增此 builder 的 tab；不能在 branch 编辑；Marketplace 不支持，须先用 Workshop 重建 | [G07](https://www.palantir.com/docs/foundry/object-views/config-legacy-object-views/) [G08](https://www.palantir.com/docs/foundry/object-views/config-tabs/) [G11](https://www.palantir.com/docs/foundry/object-views/branching-object-views/) [G12](https://www.palantir.com/docs/foundry/object-views/marketplace-object-views/) |

Legacy builder 的配置还包括 widget 标题/图标/帮助、左右或全宽对齐、部分 widget 的高度范围，以及 YAML 复制复用。它的跨 section 过滤可按同一 filter-set ID 在 tabs 间消费和延续；不能把该旧机制直接称为当前 Workshop 全局变量或 state saving。[G07](https://www.palantir.com/docs/foundry/object-views/config-legacy-object-views/) [G08](https://www.palantir.com/docs/foundry/object-views/config-tabs/)

Tabs 可按对象属性等/不等于给定值、链接目标类型的可见权限、profile 控制可见；link content type 可以显示关联数量 badge。当前 Full 编辑器仍链接这些 visibility settings，但详细页位于 Legacy 导航下。应写“兼容配置文档仍保留该规则”，而非把旧 editor screenshot 的所有操作投射到新 UI。[G05](https://www.palantir.com/docs/foundry/object-views/config-object-views/) [G08](https://www.palantir.com/docs/foundry/object-views/config-tabs/)

Profile 是按角色组织展示的另一层，按 tab 分配，由 Platform Settings 中 group 的 Hubble attributes 定义。用户可以切 profile；单一 profile group membership 才能设置用户默认 profile；每 Object View 最多十个 profile。`hubble:isDiscoverable=true` 允许非成员发现该 profile，不能用 profile 的 UI 可见性替代底层资源授权。[G09：Profiles](https://www.palantir.com/docs/foundry/object-views/config-profiles/)；最后一句为安全边界分析。

Legacy Applications sidebar 可分组展示应用与 Actions，发布且有非空内容才显示；Workshop / Slate 参数可传当前对象属性、关联对象集或常量，Workshop 参数须配置为 module interface variables。链接卡开新浏览器 tab；无嵌入应用权限者仍可能看见卡片却无法打开。**这是当前保留的 Legacy sidebar 配置证据，不能宣称它是所有当前 Object Views 的统一应用导航方案。**[G10：Applications sidebar](https://www.palantir.com/docs/foundry/object-views/config-app-sidebar/)

## 6. 保存、发布与历史：两个版本层，不是用户状态保存

| 层或操作 | 官方明确行为 | 研究限制 |
|---|---|---|
| Object View version | 保存编辑生成新版本，可含页签新增/修改/删除；可预览历史与重新发布旧版本 | 未公开完整 persisted schema |
| Per-module version | 每个 Workshop module 有独立版本，编辑器同时显示 OV 与当前模块编号 | 不能把二者版本号看作同一修订号 |
| 自动发布开关 | 默认开启；Save and publish 协调 tab 与**当前**模块变化；关闭后 Save / Publish 分离 | 不推断一次发布会遍历每个未打开 tab 的任意草稿 |
| 模块 autosave | 编辑时周期性自动保存；Object View 未发布前不向用户生效 | 文档未给周期、断网恢复、并发锁/CAS、原子发布协议 |
| 历史审计界面 | 历史列表显示日期、作者、描述；当前已发布为绿勾、曾发布为灰勾、未发布无勾 | 不等于已披露完整服务端审计日志 |

上表直接依据 [G04：Object View versioning](https://www.palantir.com/docs/foundry/object-views/manage-versions/)。官方建议多人协作或大量用户使用时关闭自动发布；这是运维治理选择，不是对产品默认行为的改写。

**应用范围要准确。** 这里有直接证据证明 **Object View 编辑器内的 Workshop module** 会周期性 autosave；文档还将其类比普通 Workshop module。它未披露并发、离线或故障恢复协议。配置历史也不能与浏览者的过滤器、选中对象、当前 tab、可分享 URL 等运行状态混为一谈。[G04](https://www.palantir.com/docs/foundry/object-views/manage-versions/)

## 7. 权限、分支审批和直接主线修改是不同门禁

Object View 的普通编辑权限依对象类型的权限模型决定：legacy datasource-derived 需要 Object View Admin 加任意输入 datasource 的 Editor；Ontology roles 需要对象类型的 Ontology Editor；project-based 需要承载类型的 Compass project 的 Editor。Managed module 权限默认由对象类型管理；经 legacy 配置转换为 standalone 的模块是例外。[G03](https://www.palantir.com/docs/foundry/object-views/config-overview/)

Global Branching 对 Object Views 区分两类资源：每 Full tab / instance panel / set panel 的 **OV-managed module** 内容，与 **Full object view tabs** 结构（新增/删除/改名/profile/visibility）。可以按资源移出 branch；移出 tabs resource 会同时移出关联 tabs。分支可以面向新增 object/action types 配置，可在 Ontology Manager 预览，也可嵌入 standalone Workshop。[G11：Branching object views](https://www.palantir.com/docs/foundry/object-views/branching-object-views/)

向 main 部署须通过 publish permission、各资源 rebase、未改不支持 Legacy 字段检查；module 内容用 Workshop rebase，tabs 结构单独 rebase。结构 rebase 是 main / branch / proposed result 三列，非冲突自动接受，冲突选择 main 或 branch 的 tab 版本。Legacy tabs 不能在 branch 编辑。[G11](https://www.palantir.com/docs/foundry/object-views/branching-object-views/)

**两个容易遗漏的治理限制：**

- Datasource-derived 模型的 branch merge 比 main 编辑更严格：贡献者或批准者需对象类型 View、**所有** backing datasources 的 Editor 和 Object View Admin；main 编辑只要求任意 backing datasource 的 Editor。roles / project-based 模型则可由贡献者或 reviewer 的对象类型 edit access 满足，无须另加 Object View Admin。[G11](https://www.palantir.com/docs/foundry/object-views/branching-object-views/)
- 对象类型若 protected 且位于有 project approval policy 的项目，审批策略适用于作为 logical children 的 OV 与模块；但当前同页另写 **Inherited resource protection 仍在开发中**。在其可用之前，即使 parent object type protected，OV 及组成 tabs/panels 的 modules 仍可直接编辑 main。审批继承已经文档化，不代表阻断直接 main 编辑已完成。[G11](https://www.palantir.com/docs/foundry/object-views/branching-object-views/)

**EOS 架构分析：**对象类型是详情配置的治理锚点值得借鉴；但审批、编辑授权和禁止主线修改必须分别验证。不要仅因“子资源继承对象权限”便认为生产配置具备强制评审门禁。

## 8. Marketplace 的打包边界

Object Views 可通过 Foundry DevOps 加入 Marketplace 产品；添加 outputs → Add ontology entities，选 Object View 后再选纳入产品的 tabs。只支持 Workshop tab builder，Legacy builder 须先重建。该页面明确的是 **tabs 的打包范围**；本次未找到它单独保证 Standard 自动视图、instance/set panels、standalone 模块依赖、已有消费者定制冲突如何被打包和升级，不予推断。[G12：Marketplace Object Views](https://www.palantir.com/docs/foundry/object-views/marketplace-object-views/)

## 9. 面向 EOS 的架构取舍与验证建议（分析）

以下是通用架构分析，不基于本次读取 EOS 代码，不代表 Palantir 对 EOS 的建议。

| 架构问题 | 可借鉴机制 | 验证重点 |
|---|---|---|
| 新对象类型如何立即有入口 | 元数据驱动 Standard 保底；定制业务页单独拥有生命周期 | schema 变化后默认视图与已接管定制页分别如何更新 |
| 详情与任务应用如何组合 | Full 管综合详情，Panel 保持宿主工作流上下文；单对象与集合 panel 分开 | 宿主尺寸、对象类型、单/多选择、切换回标准视图（Workshop 文档差异待租户核验） |
| 页面是否可复用 | OV-managed 与 standalone 分开，前者自动同权，后者跨类型复用 | 复用页升级与各详情采用版本，独立页无权限时的降级行为 |
| 谁能改生产入口 | 对象类型做治理锚点；发布与保存分离；branch内容/结构分资源 | 主线是否仍可绕过审阅，父对象策略是否完整落到子资源 |
| 旧视图如何退出 | 存量兼容，停止新增；迁移后才可进入 branch/Marketplace | 旧 visibility、profile、过滤、sidebar 参数逐项等价性 |
| 富媒体如何进入对象详情 | 默认按类型识别；定制媒体组件明确输入契约 | attachment/media ref/URL、权限、CSP、PDF嵌入附件、专用播放器差异 |

## 10. 明确未验证的事项

- Core → Standard / custom → configured 的正式更名公告及精确日期。
- “每类型自动生成 default configured”与“创建 configured 后成为默认”的物化、选择及迁移规则；需要实际租户对新类型、历史类型与不同宿主核验。
- 用户 standard/configured toggle 是否跨会话或跨宿主持久化；多个 profile group 时默认选取的完整优先级。
- Workshop 的 overview 与专门 widget 页面对 toggle 的不同陈述在实际租户中的对应状态。
- 一次 OV 发布对所有 tab 草稿的精确事务边界、并发写入、模块 autosave 周期、发布后既有浏览会话刷新时机。
- Legacy → Workshop 一键转换工具或自动语义等价保证；当前资料只明确 Marketplace 要求重建。
- Object View 配置、数据、Action 执行权限的端到端实际身份；UI可见性规则不能作为实际执行授权证据。
- 父对象 protection 继承在特定租户的上线状态；本次只按公开文档仍 under development 报告。

这些限制不妨碍依据公开资料理解对象入口、默认详情、配置所有权与发布门禁；需要租户实验的部分应列为验证问题，不写成已观察结果。
