# Object Views 与 Workshop：对象上下文、导航和宿主边界

> 核验日期：2026-10-01。仓库资料基线：`main @ 70feed00`。本笔记仅研究公开 Palantir 文档和公告；未登录 Foundry 租户、未执行真实 Action，未读取 EOS 内部代码。没有将公开 OSDK 组件当作 Foundry 闭源 Object Views 的源码。无日期的产品文档均表示“检索日可见的当前文档”，不表示该日首次发布。来源记录见 [workshop-sources.json](workshop-sources.json)。

Object View 可以理解为**按对象类型配置、由对象上下文实例化、可进入不同宿主的共享详情入口**；configured Object View 使用 Workshop 创作，但与一个通用独立 Workshop 应用具有不同的资源身份、默认选择和权限治理。本次新增的核心证据是 Object View widget 的形态/输入规则、页签与 panel 的接口映射，以及 Carbon 的对象上下文导航；Workshop 的变量生命周期、Action 事务、Custom Widget 协议和版本机制沿用[已有运行机制专题](../../workshop-runtime-2026-10/README.md)，不重复推断闭源实现。[Object Views overview](https://www.palantir.com/docs/foundry/object-views/overview/)、[configured Object View overview](https://www.palantir.com/docs/foundry/object-views/config-overview/)

## 1. Workshop 既是创作工具，也能成为 Object View 的消费宿主

**已核实事实，当前文档，2026-10-01 检索。** configured full Object View 的每个页签都有一个 Workshop module，页签内容用 Workshop 的布局、变量和 Scenarios 创作；configured panel 也采用 Workshop 创作方式，编辑画布提供宿主应用尺寸预设、通用分辨率或手工尺寸。画布尺寸是近似预览，实际 panel 尺寸随设备和宿主变化。一个 full 页签被删除时，所含的 Workshop module 也被删除。[Configure full Object Views](https://www.palantir.com/docs/foundry/object-views/config-object-views/#edit-object-view-tabs)、[Configure panel Object Views](https://www.palantir.com/docs/foundry/object-views/config-panel-views/#edit-configured-panel-object-views)

这与“在通用 Workshop 里放入 Object View widget”是另一方向：widget 消费对象类型的已有视图，构建者可以选择 full/panel、standard/configured、header、空状态及接口映射。full 适合较大详情区域，官方举例通常放在 overlay/modal；Vertex、Map、Gaia 等应用用 panel 表达紧凑的对象选择，点击对象标题又可在可移动、可缩放的 modal 中打开 full。[Object View widget](https://www.palantir.com/docs/foundry/workshop/widgets-object-view/#configuration-options)、[Use full Object Views](https://www.palantir.com/docs/foundry/object-views/use-full-views-in-platform/#platform-applications)、[Use panel Object Views](https://www.palantir.com/docs/foundry/object-views/use-panel-views-in-platform/)

| 组合方式 | 已核实消费契约 | 重要边界 |
|---|---|---|
| Workshop Object View widget，full | 输入 ObjectSet；多对象时只显示第一个；可设 initial tab ID、换对象回 initial tab、隐藏 tabs | 隐藏 tabs 会使用户无法切换；initial tab 是 widget 配置，不能据此补造 Object View 的 tab URL 参数 |
| Workshop Object View widget，panel | `Object instance` 总显示首个；`Adaptive` 在恰好 1 个对象时显示实例，在 0 或多个时显示集合；`Object set` 总显示集合 | configured object-set panel 是同一对象类型的集合汇总；不能把集合视图写成全平台通用 Object Explorer 的替代 |
| 通用 Embedded Module widget | 选择独立子模块及 module interface 映射；消费子模块已发布版本 | 独立资源权限须分别满足；此 published-version 规则来自 Embedded Module 文档，不能无证据外推为 Object View 任意版本选择规则 |
| URL/iframe 进入 Object View | 对象链接可带对象主键或 RID；`embedded=true` 隐藏 Workspace sidebar | sidebar 隐藏是展示选项；文档没有说它撤销身份/数据权限，也没有说 URL iframe 自动建立 module interface 共享状态 |

前两行来自 [Object View widget](https://www.palantir.com/docs/foundry/workshop/widgets-object-view/#form-factor-configuration-options)，第三行来自 [Embedded module widget](https://www.palantir.com/docs/foundry/workshop/embedded-modules/#module-selection) 和 [embedding limitations](https://www.palantir.com/docs/foundry/workshop/embedding-workshop-modules-overview/#permission-of-embedded-modules)，第四行来自 [Generate Object View URLs](https://www.palantir.com/docs/foundry/object-views/generate-urls/)。这些是公开产品契约，表中“不能外推”的文字为研究边界。

## 2. 对象上下文之外还有显式 module interface

**已核实事实，当前文档。** Object View widget 先用输入 ObjectSet 确定显示对象，再可将父模块变量映射到特定对象类型的 full 页签或 panel 的 module interface。full 需要选择已经定义接口的页签；legacy Object View tabs 不支持这项接口配置。退回 legacy widget 可提高 legacy tab 的加载速度，但不支持 interface configuration。[Object View widget: advanced settings](https://www.palantir.com/docs/foundry/workshop/widgets-object-view/#form-factor-configuration-options)

module interface 是 Workshop 的输入/输出变量接口，与 Ontology 的 object interface 不是同一概念；变量有 external ID 并启用 module interface 后，才可被映射或由 URL 初始化。已映射接口由父模块的变量定义支撑，子模块的默认值、函数/变换定义和重算配置不再作为该映射变量的定义；reset 使用父模块默认值。Object View widget 文档直接将其接口配置指向这套嵌入接口文档。[Module interface](https://www.palantir.com/docs/foundry/workshop/module-interface/#embedded-module-interface)、[Embedded module interface configuration](https://www.palantir.com/docs/foundry/workshop/embedded-modules/#interface-configuration)

**分析。** 因此“正在看的对象”与“业务上下文接口”应分开：对象身份回答显示哪个实体；接口可以补充当前任务、时间范围、筛选条件、选中关联对象或布局状态。接口映射也使详情中的交互能影响共享变量，但不能把任意子模块本地变量都视为已共享，不能把共用值直接等同于跨模块统一事件总线。通用嵌入模块公开不支持父→子传递 event configuration；要让子模块控制父布局，可通过已映射的布局状态变量沟通。[Embedding: event passing](https://www.palantir.com/docs/foundry/workshop/embedding-workshop-modules-overview/#event-passing)

**文档差异待验证。** 嵌入总览一处说 child 更新不会自动回传，需显式 set variable event；专门的 Embedded Module widget 页面则说对已映射值的 widget output 或 set event 修改会反映到所有映射模块。稳妥阅读是“已映射接口值共享，普通子模块变量不自动回父”，但本次没有租户实验确认不同输出来源的确切行为。不得删掉这项差异，或宣称已验证所有 child output 都双向同步。[Embedding communication](https://www.palantir.com/docs/foundry/workshop/embedding-workshop-modules-overview/#communicating-across-embedded-modules)、[Embedded Module widget](https://www.palantir.com/docs/foundry/workshop/embedded-modules/#interface-configuration)

## 3. 导航、URL 初始化和运行中共享是三种机制

**已核实事实，当前文档。** Workshop 的应用事件包括 Open Workshop module、Open Object view 和 Open Object Explorer；在普通环境打开新浏览器 tab，在 Carbon workspace 中打开新 Carbon tab。Open Workshop module 会把调用时的接口变量当前值写入目标 URL；接口 URL 只在首次加载时初始化变量，加载后改 URL 不会动态更新值。[Events: Applications](https://www.palantir.com/docs/foundry/workshop/concepts-events/#applications)、[Module interface: Open Workshop module](https://www.palantir.com/docs/foundry/workshop/module-interface/#open-workshop-module-event)

routing 则把当前页 ID、配置了 URL update behavior 的接口变量放入 URL，支持 visible-use/always/never 等写入行为；query key 匹配 external ID 时，即使其写入选项不同，也可作为初始值。URL 不支持直接 ObjectSet filter；ObjectSet URL 限于以 RID 指定的单个对象，可用其他路由变量间接生成集合或过滤器。子模块的 routing 配置不继承，要由父模块路由变量映射到子接口。[Workshop routing](https://www.palantir.com/docs/foundry/workshop/routing/)

Object View 当前 URL 文档列出以下链接格式，路径中的 `hubble` 是公开链接格式，并非闭源架构证据：[Generate Object View URLs](https://www.palantir.com/docs/foundry/object-views/generate-urls/#generate-object-links)

```text
/workspace/hubble/external/object/v0/<object-type-id>?<primary-key-property-id>=<primary-key-property-value>
/workspace/hubble/external/search/v2/?objectId=<objectRid>
/workspace/hubble/objects/<objectRid>
```

文档明确说明第二种 RID search URL 在 Object Explorer 上下文中加载 Object View，含特殊字符的主键推荐 RID 方式。第三种不带额外包装，官方例子包括 iframe；iframe 可加 `embedded=true` 去掉 Workspace sidebar。此页没有列出“把全部详情页签、表单草稿和集合筛选序列化进 Object View URL”的完整契约，不能从这些链接推出这一能力。[Generate Object View URLs](https://www.palantir.com/docs/foundry/object-views/generate-urls/)

**分析。** 列表到详情的全页导航是一份当时状态快照；嵌入详情可持续共享接口值；可分享 routing 是部分 URL 状态。设计评估必须先选机制，再测试其初始化、更新、回退和权限行为。一个“打开对象”按钮本身不能证明以上三套机制等价。

## 4. Action、权限和刷新属于业务执行层

**已核实事实，当前文档。** 同一 Action type 可用于 Workshop 与 Object Views；表单来自 Action 定义，Workshop 变量只负责参数默认值等局部配置。Button Group 可在提交开始和提交成功后触发 Workshop 事件，进行刷新、导航或变量更新；Inline Action 也有成功事件和创建/修改对象的输出 ObjectSet。因此 configured 详情中可以组合对象展示与业务操作，业务规则及执行授权仍属于 Ontology Action。[Use Actions in Workshop](https://www.palantir.com/docs/foundry/workshop/actions-use/#chaining-an-event-with-an-action)、[Inline Action](https://www.palantir.com/docs/foundry/workshop/widgets-inline-action-form/#configuration)

Workshop 模块的打开/编辑权限与对象、Action、Function 的权限独立。managed Object View tab 模块通常由对象类型管理权限，使该类型的查看/编辑与内部模块对齐；若经 legacy 选项转成 standalone module，则不能继续假定是同一治理。legacy 页签文档也明确 managed module 不可独立复用，而已有 standalone Workshop module 可用于多个 Object Views。[Permissions in Workshop](https://www.palantir.com/docs/foundry/workshop/concepts-permissions/)、[Configured Object View permissions](https://www.palantir.com/docs/foundry/object-views/config-overview/#permissions)、[Legacy tab types](https://www.palantir.com/docs/foundry/object-views/config-tabs/)

**分析。** “可以看到详情页”不能代替“可以执行详情页里的操作”；隐藏页签或 Action 按钮也不等同提交授权。应分别检查对象可读、关联可读、Action 可提交、函数可用、宿主资源可打开。这一边界的完整说明见已有[权限与 Actions 附录](../../workshop-runtime-2026-10/data-actions-versioning.md#2-actions校验提交事务错误与刷新)，本笔记不重新复制事务语义。

刷新也不是一次统一的全 UI 完成屏障：Refresh data in module 事件重新加载模块数据；auto-refresh 通过 watch ObjectSets 对外部更新触发刷新，限 OSv2，输入控件可能随重算重置。嵌入子模块的 auto-refresh 设置不被继承；要隔离刷新，官方给出 iframe 独立环境选项。普通事件按序运行，但不等待上一步全部下游变量计算完成。[Events: data staleness / execution order](https://www.palantir.com/docs/foundry/workshop/concepts-events/)、[Auto-refresh](https://www.palantir.com/docs/foundry/workshop/auto-refresh/)、[Embedding settings limitations](https://www.palantir.com/docs/foundry/workshop/embedding-workshop-modules-overview/#no-module-settings-inheritance-of-child-modules)

## 5. 详情中的运行状态不等同视图配置版本

**已核实事实，当前文档。** state saving 保存明确启用的变量当前值和可选当前页；官方例子包括保存列表筛选、当前高亮对象，以及由原生 Text input、Date input 等组件构成的未填完表单。保存需要显式操作，启用变量不等于自动保存跨会话偏好；加载则可手动、通过链接或指定默认已保存状态。当URL没有特定已保存状态，模块再次访问会自动应用所指定的默认状态。它支持 ObjectSet 和 ObjectSet filter，而 routing 直接 URL 的支持范围更窄。状态用 external ID 关联变量，修改 ID 可能使旧状态无法重载。这没有证明任意未配置字段或Action内部事务草稿都能恢复。[State saving](https://www.palantir.com/docs/foundry/workshop/state-saving/)

子模块不继承 state saving 配置，要把需要保存的 child interface 接到父模块已启用保存的变量。state saving 还要求终端用户具备 platform access，浏览态 module header 可见。Object View widget 的 hide object-view header 是另一配置项；公开文档没有充分证据把它与 module header 的可见性直接等同。[State-saving limitations](https://www.palantir.com/docs/foundry/workshop/state-saving/#limitations)、[Object View widget options](https://www.palantir.com/docs/foundry/workshop/widgets-object-view/#core-configuration-options)

**分析。** 研究和应用评审应分别记录：对象类型/视图配置版本、backing Workshop module 的发布版本、链接初始化、用户保存状态，以及业务对象实际数据。当前资料可证明几种状态不同，不能证明已公开它们之间的完整恢复、迁移或原子发布协议。

## 6. Carbon 是有证据的工作流宿主关系

**已核实事实，当前 Carbon 文档，2026-10-01 检索。** workspace 策展应用和资源；Carbon module 是在 Carbon tab 中打开的参数化应用。导航文档的 Object Explorer 示例允许从探索列表分支打开多个 Object View tabs，保留原列表状态；Object View 的输入/输出都是单个对象，Object Explorer 接受对象集并输出当前选择集。这里说的是 Carbon 模块组合和上下文传递，没有证明 Object View、Workshop 与 Carbon 共享 React 树、闭源 runtime 或路由实现。[Carbon workspaces](https://www.palantir.com/docs/foundry/carbon/workspaces-overview/)、[Carbon modules](https://www.palantir.com/docs/foundry/carbon/modules-overview/)、[Carbon navigation](https://www.palantir.com/docs/foundry/carbon/modules-navigation/)

Workshop 的 Open in 发现需在 Carbon 的 Discoverable modules 清单登记，并在 Workshop 设置有 external ID 的 ObjectSet 接口；可选类型约束限定发现范围，没有约束的模块会在所有对象类型上可发现。Carbon 内只发现当前 workspace 清单，Carbon 外汇总用户可访问的 promoted workspaces。参数名规则是 `variable.<externalId>`，URL 则使用 `param.variable.<externalId>`；导航还存在空对象集、NaN、时序/地理/Struct 等类型限制。[Module discovery](https://www.palantir.com/docs/foundry/carbon/modules-discovery/)、[Workshop integration in Carbon](https://www.palantir.com/docs/foundry/carbon/modules-navigation/#workshop)

Carbon 的 workspace 访问不会授予其中资源访问；限制离开 workspace 的导航只是限制宿主元素，模块内部仍可能有外链。workspace 也有自己的版本历史，可以预览、修改及重发旧版本。这些机制不能补成 Object View 与 Workshop 之间的原子发布保证。[Carbon permissions](https://www.palantir.com/docs/foundry/carbon/permissions-configure/)、[Restrict workspace navigation](https://www.palantir.com/docs/foundry/carbon/restrict-workspace-nav/)、[Workspace version history](https://www.palantir.com/docs/foundry/carbon/workspaces-history/)

**带日期的沿革：2026-09-21。** 官方公告表示 Carbon 新增 Insight 探索与 modern object search，workspace owner 可通过两个独立设置 opt-in。启用 Insight 后，object types、object sets、saved explorations 的 Object Explorer-style explorations 由 Insight analyses 替代；既有 workspace 继续 opt-in，新 workspace 将来默认是计划。当前 Carbon navigation 文档仍使用 Object Explorer 示例，因此不能把 OE 写成全部 workspace 的唯一当前探索入口，也不能把新体验写成已全面默认。[September 2026 announcement](https://www.palantir.com/docs/foundry/announcements/2026-09/#explore-ontology-data-in-carbon-with-insight-analysis)

## 7. 两项资料冲突与待验证范围

1. **Workshop 中切换 standard/configured。** configured overview 仍写 Workshop 不支持 toggle，而 Object View widget 页写 mode 可选且带 toggle 选项。报告应并列记录，以 widget 页说明可配置入口，并注明没有租户验证可用范围；不能任选一句当成无条件全平台结论。[Overview](https://www.palantir.com/docs/foundry/object-views/config-overview/)、[widget mode](https://www.palantir.com/docs/foundry/workshop/widgets-object-view/#core-configuration-options)
2. **映射变量更新。** 嵌入总览与专门 widget 文档对 child 回传措辞不同，见第 2 节。后续实验需要区分 mapped interface、未映射本地变量、widget output、set event、父变量变换和 reset。

尚未从本次公开资料核实：Object View 对象上下文的内部变量 ID/数据注入实现；跨 Object View tab 的所有变量生命周期；Open Object view 事件的完整参数 schema；Object View direct URL 与全部 tab/history 状态的完整序列化规则；Insight 切换后的旧探索链接兼容性；以及各宿主中的 Action 成功到详情、父列表、关联统计全部更新的完成信号。没有租户访问也没有闭源源码，以上保持未知，不表示产品不存在这些能力。

## 8. 面向 EOS 应用架构的通用分析与验证建议

以下均为公开机制引出的架构分析，不描述 EOS 当前实现，也不构成实施计划：

- **把对象详情注册与页面创作分开。** 对象类型到 full/panel/集合视图的注册回答“从任何入口怎样找到合适详情”；Workshop 式页面组合回答“怎样构建内容”。这有助于复用同一实体入口，同时允许任务应用继续维护自己的列表和交互。
- **声明对象身份、集合上下文和业务上下文的类型。** full 的多对象取首个，panel 的 adaptive 切换，说明 cardinality 是产品行为。对象 ID、对象集、筛选描述和任务上下文应分别记录，不能用一个泛化 JSON 参数掩盖 0/1/N 与跨类型限制。
- **把权限沿消费路径验收。** 测试有详情权限但无关联/Action权限、可发现但无模块权限、standalone 与 managed tab、隐藏 UI 但 direct URL 可打开等情况；导航可见性和资源授权需要分别给出结果。
- **明确共享状态与独立导航的期望。** 测试父列表选中→详情、详情选择关联对象→父/兄弟模块、另开详情保留列表、返回/刷新后 URL 初始值、保存状态再打开与 external ID 迁移。检验共享变量是否允许 detail 回写，不仅检验首屏正确。
- **按宿主验证业务动作刷新。** 在 full overlay、compact panel、独立 tab 和 iframe 中分别提交修改；记录对象读取、关联集合、父列表与用户输入的变化，辨别 Action 已成功与画面已完成更新。若将来有获授权测试环境，再执行这些实验；本次未将建议当作亲测结果。
