# FilterList：筛选状态、聚合与对象集联动

核验日期：2026-10-01。主证据版本：实际 npm tarball `@osdk/react-components@0.61.0`，其发布 provenance 对应 upstream commit `37cfd38676bf04edaef5847e929d914ea214c149`（发布日期与 provenance 原始记录见[报告正文](README.md)）。该发布提交与 main `e53b94ecd5de7cdd7e864d0daa04363bdad4db4c` 在 `src/filter-list/`、`src/public/filter-list.ts`、`src/public/experimental/filter-list.ts`、`docs/FilterList.md`、`docs/FilterListOverview.md` 范围内无差异。以下源码引用均采用发布提交；这一限定比较不代表整个 monorepo 与 main 一致。

证据标签：**实现事实**指发布提交运行源码；**类型约束**指 TypeScript 定义；**仓库测试**指阅读上游测试但未执行；**孤立运行验证**指直接导入 npm tarball 的无依赖 utility 模块；**推断/建议**单独标记。验证包括纯函数执行与正文中的 Storybook mock 联动交互，未连接生产 Ontology 或执行 Action，生产后端尚未验证。

可重跑验证：运行 [probe 脚本](probes/filter-artifact-probes.mjs)（需指定实际 npm 解包根目录）；结果见 [记录](evidence/filter-artifact-probes.json)，包括发布模块SHA-256、Node版本、Date round-trip、两种scope分支、zero-count NO_VALUE结果。文末62处固定提交引用的文件与行范围均已核对。

## 界面与联动

![筛选与表格](assets/04-filter-table.jpg)

官方 Storybook 实拍：FilterList 与 ObjectTable 共享 mock 对象集。

![Engineering 选中后](assets/05-filter-engineering.jpg)

实际点击 Engineering 后，选中状态和右侧表格一起变化；这是 mock 演示的 UI 联动证据。

![不同筛选输入](assets/06-filter-types.jpg)

同一筛选容器组合分类、数值与日期输入；不是所有内部输入组件都拥有独立公开入口。

## 1. 定位与外部边界

- **实现事实**：FilterList 将 Ontology-aware 逻辑与 BaseFilterList 外壳分开。外层把 `objectType/objectSet`、每个筛选项排除自身的条件、链接过滤、状态与 `renderInput` 交给 BaseFilterList；Base 本身负责 panel、header、collapse、add/remove、拖拽与宿主渲染回调。[F01] [F02]
- **发布导出事实**：公开入口 `@osdk/react-components/filter-list` 导出 `FilterList`、`BaseFilterList`、`FilterPopover`、`FilterInput`、`useFilterListState`、`narrowObjectSet`、state serialization 和 key/label/value 工具；`FilterList` 公开值经过 metrics HOC 包装。旧 `experimental/filter-list` 是逐个 deprecated alias，转指 stable entry。[F03] [F04]
- **边界**：源码内部有 ListogramInput、MultiSelectInput、SingleSelectInput、RangeInput、DateRangeHistogramInput 等，但这个公开 barrel 没有导出它们，也没有导出 `usePropertyAggregation` / `useDualScopeAggregation` / `useFilterVisibility`。存在文件不代表消费者有受支持的 npm deep-import 入口。EOS 不应把任意 internal hook 视为可直接复用接口。[F03]
- **产品阶段**：`FilterListOverview.md` 明确标记 Beta，同时指向 `/filter-list`；“稳定入口路径”不等于产品 GA。[F05]

## 2. 从筛选状态到对象集：需要分开两条输出

**实现事实**：`useFilterListState` 用 metadata 的 property type/multiplicity 生成 `WhereClause`，再独立收集 active linked filters；有 `objectSet` 时运行 `narrowObjectSet` 得到 `filteredObjectSet`，没有时输出 undefined。[F06]

一个筛选变化的正式事件是 `{ snapshot: { filterClause, filteredObjectSet }, reason }`。reason 包含初始化、状态变化、remove、reset、objectSet 变化；初始化等待 metadata loading 结束后只发一次。`setFilterState` 用 ref 立即更新，避免同一 React commit 前连续写入只基于旧 render snapshot。旧的 `onFilterClauseChanged` / `onEffectiveObjectSet` 则分别在 effect 中发出，不应依赖它们提供同步的成对状态。[F07] [F08]

对直接字段过滤，可把 `snapshot.filterClause` 交给读取对象的查询；对 `HAS_LINK` / `LINKED_PROPERTY`，**必须读取 `snapshot.filteredObjectSet`**，因为 `buildWhereClause` 明确跳过这两种筛选。仅把 clause 喂给 ObjectTable 会丢失 link 条件。输出对象集已经包括直接条件和 link 条件，不必再把同一 clause 叠加一次。[F06] [F09]

**源码流程**：

```text
FilterState map + definitions + metadata
    ├─ buildWhereClause → direct-property / keyword / custom / static clauses
    └─ getActiveLinkedFilters → link name + positive innerWhere + excluding flag
              ↓
     narrowObjectSet(base, direct clause, linked filters)
              ↓
     snapshot.filteredObjectSet → downstream data component/query
```

### 2.1 WhereClause 映射与实际语义

| 状态/定义 | 运行实现 | 证据 |
|---|---|---|
| `CONTAINS_TEXT` | 非空 value → `$containsAnyTerm`，不是 JavaScript 本地 substring | [F10] |
| `TOGGLE` | 输出布尔值；false 仍是一个合法直接谓词 | [F10] |
| 数值范围 | `$gte`/`$lte`；双边用 `$and`；可与 `$isNull` 用 `$or` 组合；byte/short/integer 边界 clamp，long 受 JS safe-integer 范围 clamp | [F10] [F11] |
| 日期范围 / timeline | Date 转日期格式或 ISO；datetime 分支采用日期字符串，其他日期类型采用 ISO；双边 inclusive `$gte`/`$lte`；relative state 优先于缓存的 absolute Date | [F10] [F11] |
| `EXACT_MATCH` / `SELECT` | 一个值直接 equality，多个 `$in`；`NO_VALUE` sentinel → `$isNull`；literal empty string 是真实值 | [F12] |
| exclude | property clause 外包 `$not`；并非简单地移除该选项 | [F11] |
| 多个筛选项 | 所有非空 clause 以 `$and` 连接 | [F09] |
| `CUSTOM` | 调用 definition 的 `toWhereClause`，空/undefined clause 被忽略 | [F09] |
| `STATIC_VALUES` | 优先自定义 `toWhereClause`，否则使用 `key` 自动生成属性谓词 | [F09] |

**类型与运行边界**：Select 的类型允许 string/boolean/number，聚合 UI 却把非空 `$group` 值转换成 `String(rawValue)`，SingleSelect / MultiSelect 的用户选择回调写入字符串数组。迁移到 EOS 时必须保存 schema/native-value 映射，不能假定 TS 联合类型保证实际 UI payload 总是保持 number/boolean。本文未验证 Foundry 是否会在这些路径上进行服务端类型转换，因而不把它定性为 Foundry 查询故障。[F13] [F14] [F23] [F42]

### 2.2 关键词筛选不是“全对象字段任意全文搜索”

- **实现事实**：`KEYWORD_SEARCH` 将 term trim；`properties: "all"` 从 metadata 选择 `type === "string" && !multiplicity` 的字段，缺 metadata 时跳过并在开发模式 warn。显式字段数组则直接使用。[F15]
- `operator: "AND"` 在**每个字段内**用 `$containsAllTerms`，`OR` 用 `$containsAnyTerm`；不同字段的谓词始终以 `$or` 连接。因此 AND 的两个词不能靠“字段 A 有第一个词，字段 B 有第二个词”满足全部词，这不是跨字段 global conjunction。[F15]
- 输入本身通过 ContainsTextInput；operator 来自 state，未见 KeywordSearchInput 提供 AND/OR 切换控件，默认空状态用 AND。改变 operator 需种子/自定义交互。[F16]
- facet 的“Search values”是另一条本地搜索：Listogram 用 case-insensitive substring 过滤已加载 values；`renderValue` 返回 string 时搜索这个 string，返回 JSX 时回落到 raw value。它不会改变主对象集的 keyword clause。[F17] [F18]

### 2.3 链接过滤是 exists / not-exists 的源对象语义

- **实现事实**：`narrowObjectSet` 对每个 link filter 创建 `osdkFilterListLinkCount_<id>` 派生属性，creator 执行 `base.pivotTo(linkName)`，可加 positive `innerWhere`，再 `.aggregate("$count")`。源对象有至少一条匹配链接时 count > 0 被保留；exclude 使用 count = 0，因此包括完全没有该链接的源对象。[F19]
- `HAS_LINK` 只有 hasLink=true 才 active；关闭 toggle 表示不施加条件，不等于“没有链接”。需要 toggle 开启且 exclude 才查询无匹配链接。[F20]
- `LINKED_PROPERTY` 先从 inner state 去掉 excluding，再生成 positive innerWhere；排除发生在**源对象的匹配 count**，并不是“把 linked object 上的谓词取反后 pivot”。这对一对多关系很关键：若一个源对象既链接 Alice 又链接 Bob，exclude Alice 会移除这个源对象。[F20] [F19]
- **运行限制**：没有 `objectSet` 时，LINKED_PROPERTY 的输入直接渲染空 fragment；HAS_LINK 仍有 toggle，但输出 `filterClause` 中无 link 条件、`filteredObjectSet` 又 undefined，因此不会产生实际 link narrowing。使用链接筛选必须传真实 ObjectSet。[F21] [F06]
- linked facet 的计数是先缩窄源对象，再 `pivotTo(linkName)` 后在**linked object set**上聚合，不能直接理解成“有这个 linked 值的源对象行数”。未对 Foundry 的 pivot distinct/aggregation backend 语义做远程实测。[F22]

## 3. 聚合与双 scope：实现比一句“aggregation-based”更具体

**实现事实**：普通分类 facet 用 `useOsdkAggregation`，请求 `$select: {$count: "unordered"}` 与 `$groupBy: {property: {$exact: {$includeNullValue: true}}}`。其结果在 UI 中转换/去重，按 count 降序（同 count 按 value）或 value 排序。`limit` 是接收到结果后的 `.slice`，不是请求的 server-side limit；内置 MultiSelect/Listogram 调用没有配置这个 limit。[F13] [F23]

每个定义都有 **excluding-self** 的 direct clause 与 linked filter 数组，基于全部 definitions/state 重建；相同结构的 per-key 值通过 `fast-deep-equal` 保留引用。某筛选自己从 Engineering 改到 Sales，其自己的候选查询不应因自身 predicate 变化而重查；其他 facet 的 scope 会变化。上游有引用稳定性的专门测试，但本文未运行这些 React hook 测试。[F24] [F49] [T01]

### 3.1 两种不同的 dual-scope 规则

1. **普通属性 facet**：`computeDualScopes` 首先用 direct clause + linked filters 得到 scoped。只有 `showFilteredOutValues` 为 true 且存在其他 active linked filter 时，才额外生成 emptySource；这个 emptySource **保留 direct where、仅删除 link filters**，不是无条件回到 raw base。因此普通属性 facet 不会为所有被其他直接字段过滤掉的值统一回补灰色行。[F25]
2. **linked-property facet**：scoped 是 narrowed source 的 pivot；开启 `showFilteredOutValues` 时，emptySource 则直接来自 raw `objectSet.pivotTo(linkName)`，因此可回补被 source direct filters 缩窄后消失的 linked 值。[F22]
3. `useDualScopeAggregation` 将 selected values 与 emptySource 中 values 合并为 activeValues；primary aggregation 缺少的 active value 被合成 count=0。loading 结合两个 scope；emptySource 聚合失败时只使用 scoped 结果，返回的 error 只取 primary error。因而“不报错”不意味着双 scope 回补一定成功。[F26] [F13]
4. 即使关闭 `showFilteredOutValues`，普通已选值也通过 selectedValues 参数尝试保留 count=0 选项。非空 chosen 值不会仅因另一个筛选使它计数归零就失去可见选择/取消入口。[F23] [T02]

### 3.2 必须标明的实现限制 / 静态疑点

- **发布 utility 孤立运行验证 + 静态链路**：`computeDualScopes(undefined, {name:"Alice"}, [], true)` 输出 scoped=undefined、emptySource=undefined；`useFilterPropertyAggregation` 后续只向 dual hook传 scoped/emptySource，不继续传 whereClause。对 MultiSelect/SingleSelect/Listogram 这条路径，objectType-only 模式下 cross-filter where 没有传入聚合 hook。Range/TextTags 的独立路径不能据此一概而论。建议消费者显式传 `client(ObjectType)` 的 base ObjectSet，而不是仅传 objectType。[F25] [F27]
- **静态疑点，未测网络**：`useDualScopeAggregation` 虽在注释里称 emptySource undefined 时等价单查询，但实现无条件先调用 `usePropertyAggregation(objectType, key, undefined)`，再调 scoped primary；`usePropertyAggregation` 没传 `enabled:false`。`useOsdkAggregation` 的 enabled 默认 true，undefined objectSet 会走全类型 observeAggregation 分支。因此可能存在“single-scope 表现，却有全类型额外 aggregation subscription/query”的成本；缓存 canonicalization 可能合并相同请求，不能从源码直接声称每次一定发两次 HTTP。[F26] [F28]
- **仓库测试的边界**：dual-scope test mock 掉 `useOsdkAggregation`，断言的是合并结果、fallback、selectedValues；`emptySource===undefined` 用例没有断言 hook 调用数量或网络请求数量，因此不能拿它证明单查询。[T03]
- **源实现边界**：普通 NumberRange / DateRange 分支只有 `objectSet + whereClause` 参数，没有接收到 linkedFilters；PropertyFilterInput 对这两个分支没转交 linkedFilters。故直方图/null count 不保证反映别的链接筛选的 scope，尽管最终 filteredObjectSet 有 link narrowing。是静态代码结论，未做真实 backend/UI 组合验证。[F29]
- **性能建议**：数值范围拿 exact grouped values 后在前端建 20 个 numeric histogram buckets；这不是让 Foundry直接返回 20 桶的 server histogram。高基数列应先用实际 Ontology 数据量验证延迟、aggregation 限额和返回规模，再决定 EOS 是否需要 dedicated facet endpoint。[F30] [F29]
- **选中缺失值的例外**：`dedupeEmptyAggregationRows` 只在合计null count > 0时插入NO_VALUE行，count=0的NO_VALUE会被丢弃；本机直接执行发布tarball这个函数，输入`[{value:"__NO_VALUE__",count:0}]`，输出`[]`。所以“已选值即使count=0仍回补”的普通string测试不能证明已选null bucket也保持同样可见性。且NO_VALUE是字符串`"__NO_VALUE__"`，EOS协议应使用独立typed null身份而不要依赖domain value不会撞这个字面量。[F50]

## 4. 状态、隐藏、reset 和受控模式

- **实现事实**：FilterList 的 filter state 是内部 `useState<Map>`，只在 mount 读取 definitions 的 `defaultFilterState`，再覆盖 `defaultFilterStates`（兼容 initialFilterStates）。reset 恢复这份 mount snapshot；后续外部 `defaultFilterStates` 变化不会重新 seed。这不是一个 `value/onChange` 全受控组件。公开 headless hook 也是这个所有权模型。[F31] [T04]
- 相同字段上两个筛选要显式独立 id；默认 PROPERTY key 是 property key，LINKED_PROPERTY key 是 link+property，keyword key来自 properties。default map、React key、reorder、per-filter query排除都依赖这个 id；重复 key会共享/覆盖状态。[F32]
- `isVisible:false` 只影响渲染；state pipeline 仍遍历完整 definitions，所以隐藏 seeded filter 可继续参与查询。“隐藏”不能等价于“清空”。内置 uncontrolled remove 则先 clearFilterState，再 hideFilter；这是另一种行为。[F01] [F09] [F33]
- visibility/order 默认内部管理，可从 `onFilterVisibilityChange` 获取可见项在前（显示顺序），隐藏项在后，并存回外部。`addFilterMode:"controlled"` 只控制 visibility，不是 filter state；它已 deprecated。[F34]
- `useFilterVisibility` 在 `filterDefinitions` 改变时重新设默认 visible order。持续每次 render创建新定义数组会使本地显隐/排序回到 prop 种子；需要 memoized definitions 或按 callback同步外部持久化的顺序/visible。源码的 effect 与上游“definitions变更同步”的测试是依据。[F33] [T05]
- panel collapse 则确实支持 controlled `collapsed` 或内部 `defaultCollapsed`；enableCollapse=false 时始终展开。collapse保持expanded DOM，以CSS隐藏，不是把组件卸载。[F02]
- **docs / implementation discrepancy**：API注释（并自动生成到docs）称省略 `filterDefinitions` 时提供所有 filterable properties；所核运行链没有 metadata自动生成 definitions，useFilterVisibility(undefined)返回空数组，FilterListContent(undefined/[])渲染 empty div。必须手工提供定义。不是根据type“optional”就推断自动发现能力。[F35] [F33] [F36]

### 4.1 清晰区分三种“保留”

1. **业务状态保留**：hide不必删除 FilterState；内置remove会清掉；reset回到初始种子。[F01] [F31]
2. **选项保留**：普通selected value缺失时合成count=0，dual-scope可进一步回补source-only values。[F13] [F26]
3. **加载期间画面保留**：`useStableData` 用ref维持最近一次非loading数据，在新的isLoading阶段继续显示旧选项；MultiSelect保持chips/combobox，初次无data显示skeleton，结束后仍空才切empty-state。这是UI层持有旧值，不足以证明通用缓存具有某种SWR保证。[F37] [T06]

Listogram保留原始count/value排序，不因选中而把行跳到顶端；折叠时在前N项之后追加已选的below-fold项，View all/View less展开或回到head。其maxVisibleItems是视觉截断，不能减小网络聚合范围。[F17] [T07]

## 5. 输入节流与交互扩展

- ContainsTextInput（含keyword）默认300ms lodash debounce，本地文本即时变化、业务onChange延迟；prop更新/unmount取消pending，clear立即调用undefined且取消pending。[F38]
- 数值RangeInput的文本min/max同样300ms debounce并在unmount/prop变更取消；date picker分支直接dispatch，不能把所有filter操作都概括为统一300ms防抖。select/listogram点击经回调直接写state；顶部Search values只更新本地query。[F39] [F14] [F17] [F40]
- `renderValue`、showCount、listogram colorMap/displayMode/maxVisibleItems是built-in display调整；CUSTOM有renderInput + toWhereClause；STATIC_VALUES绕过OSDK aggregation而用固定strings与可选自定义clause。但FilterList外层仍使用OSDK metadata/context，STATIC_VALUES不等于整个FilterList完全独立于OSDK。[F41] [F16] [F06] [F51]
- **类型不等于运行承诺**：CustomFilterDefinition还声明`renderItem`，但所核FilterList/FilterInput/BaseFilterList/FilterListItem渲染链只调用`renderInput`，未读取definition.renderItem。不要把这个type字段写成已可替换整行的功能。[F41] [F16] [F40]
- **类型约束**：boolean→LISTOGRAM/SINGLE_SELECT/TOGGLE；string→LISTOGRAM/TEXT_TAGS/CONTAINS_TEXT/SINGLE_SELECT/MULTI_SELECT；datetime/timestamp→DATE_RANGE/SINGLE_DATE/MULTI_DATE/TIMELINE；常见数值→NUMBER_RANGE/SINGLE_SELECT/MULTI_SELECT；其他wire type→never。这是compile-time兼容表，runtime主要switch filterComponent，非法输入到default显示unsupported，并非通用schema validator。media、geospatial等字段需要custom策略。[F42] [F43]
- TS 的 `isExcluding` 是BaseFilterState字段，但header的supportsExcluding只对SELECT/EXACT_MATCH/CONTAINS_TEXT/TIMELINE/hasLink显示控件。不要由type字段推断所有range/keyword/custom都带exclude UI。[F44] [F40]

## 6. 拖拽与上游测试边界

**实现事实**：FilterListContent使用`@dnd-kit/core`、`@dnd-kit/sortable`，pointer activation距离8px、KeyboardSensor + sortableKeyboardCoordinates、closestCenter碰撞、verticalListSortingStrategy、x=0纵轴modifier、DragOverlay；结束用arrayMove得到keys再发onOrderChange，由外层更新visible order。附有picked/moved/dropped/cancelled的可访问性announcement。[F45]

**阅读到的仓库测试，未本机执行**：

| 测试族 | 能支持的边界 | 不能据此证明 |
|---|---|---|
| WhereClause mapping | $in/$not/range/null、keyword字段OR、custom、linked active records的纯转换 | backend结果、索引/语言分词性能 [T08] |
| narrowObjectSet | 用mock ObjectSet/builder验证pivot/withProperties/count/where链，以及exclude count=0 | Foundry真实RDP执行、权限/aggregation限制 [T09] |
| filter state | seed/reset、同步连续变更、effective set、metadata后init、objectSet变化事件、引用稳定 |浏览器真实缓存/网络 [T01] [T04] [T10] |
| selected / dual / stable values | React mock aggregation的zero-count补项、失败fallback、加载时chips/combobox保留 | 全集completion、HTTP数量、真实query race [T02] [T03] [T06] |
| drag | handle与aria、实际pointer事件后visibility顺序回调；测试人工stub getBoundingClientRect以模拟jsdom行位置 | 真实浏览器拖拽、键盘/屏幕阅读器全面QA [T11] |

这套测试说明维护者明确关心“faceted filtering不丢选择”“重查询不闪空”和排序/状态同步；它们不是Foundry端到端认证集成的证据。

## 7. 本机孤立运行验证：状态序列化Date承诺不成立

直接从npm0.61.0 tarball读取并执行：`build/esm/filter-list/utils/filterStateSerialization.js`。此模块没有React/网络依赖；执行环境Node v22.17.0。用DATE_RANGE minValue=Date('2026-09-01T00:00:00.000Z')序列化后再反序列化，输出如下：

```json
{"version":"0.61.0","node":"v22.17.0","serialized":"[[\"startDate\",{\"type\":\"DATE_RANGE\",\"minValue\":\"2026-09-01T00:00:00.000Z\"}]]","restoredType":"string","restoredIsDate":false}
```

**已验证限制**：docs称helpers preserving Date；实现的JSON replacer只检测`value instanceof Date`，实际Date在JSON流程中变为普通ISO字符串，未加`__date__:`前缀，reviver也就不会还原Date。[F46] [F47] 这是发布tarball的utility结果；未验证浏览器package resolution、React重载、Foundry日期过滤结果。EOS持久化不能照搬文档保证，应显式按schema reviver/自定义 tagged serialization，并为Date、relative state、null、custom state设计迁移/校验。

同时直接导入tarball的`computeDualScopes`做两组无网络utility验证：no objectSet时scoped与emptySource均undefined；有fake base.where且direct-only条件时调用where({name:"Alice"})，返回scoped，emptySource仍undefined。这仅证明纯function分支，与第3.2节静态链路一致，未执行useOsdkAggregation hook。

## 8. EOS采用建议（明确为建议）

| 路线 | 适合条件 | 要做的工作与边界 |
|---|---|---|
| 直接FilterList | 数据确实来自Foundry/OSDK、现有metadata与ObjectSet足够、接受Beta API | 固定整组OSDK版本；显式base ObjectSet；下游使用filteredObjectSet；验证link/range cross-facet、high-cardinality、native value、Date持久化 |
| BaseFilterList + EOS adapter | EOS是自有后端，想保留panel/排序/显隐/输入布局组织 | 公开Base没有OSDK网络hook；宿主供controlled filterStates、renderInput、key/label/count/reset/order回调；AntD输入可在renderInput中实现；EOS query AST / facet results /网络缓存由adapter负责 |
| 自主实现faceted panel | 需要完整受控Zustand/Jotai状态、EOS权限/存储协议、复杂对象关系或高基数facet | 复用“excluding-self”“selected zero-count”“稳定旧数据”“不会跳行”“exists count语义”的设计；自建schema/native值/后端facet协议，避免依赖未导出的internal hook |

依据：BaseFilterListProps接受Map与宿主renderInput/回调，Base运行文件不导入OSDK hooks。[F02] [F48] 但它仍使用此包的FilterState联合（可用customState承载业务对象）与FilterDefinitionControls；不是一个完全没有类型约束的任意form engine。Zustand/Jotai可管理选中值、显隐和持久化，TanStack Query可管理EOS facet endpoint请求；它们解决的是宿主状态/网络查询，而FilterList所实现的是定义→关系语义→查询scope→UI选项的组合协议，不能只替换一个cache库就完成迁移。

建议EOS保留自有AntD/theme与typed query DSL，先以BaseFilterList做有限adapter验证，再依据设计一致性与高基数性能决定是否自主实现；源码中未导出的built-in inputs不应作为稳定adapter依赖。两层scope特别值得借鉴，但应把direct与linked zero-count行为定义得比当前实现更统一，并为native number/boolean、missing value和Date round-trip补契约测试。

## 固定提交证据目录

[F01]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterList.tsx#L64-L242
[F02]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterList.tsx#L17-L169
[F03]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/filter-list.ts#L17-L67
[F04]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/filter-list.ts#L20-L134
[F05]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/FilterListOverview.md#L1-L6
[F06]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/useFilterListState.ts#L82-L152
[F07]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/useFilterListState.ts#L156-L239
[F08]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/useFilterListState.ts#L264-L304
[F09]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/filterStateToWhereClause.ts#L268-L424
[F10]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/filterStateToWhereClause.ts#L53-L224
[F11]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/filterStateToWhereClause.ts#L230-L261
[F12]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/filterStateToWhereClause.ts#L525-L560
[F13]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/usePropertyAggregation.ts#L54-L160
[F14]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/inputs/SingleSelectFilterInput.tsx#L62-L88
[F15]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/filterStateToWhereClause.ts#L311-L374
[F16]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L77-L245
[F17]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/inputs/ListogramInput.tsx#L71-L150
[F18]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/inputs/comboboxFilter.ts#L19-L31
[F19]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/narrowObjectSet.ts#L28-L88
[F20]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/filterStateToWhereClause.ts#L431-L523
[F21]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L77-L105
[F22]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/inputs/LinkedPropertyInput.tsx#L91-L145
[F23]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/inputs/MultiSelectFilterInput.tsx#L67-L122
[F24]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/useFilterListState.ts#L306-L332
[F25]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/narrowObjectSet.ts#L90-L107
[F26]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/useDualScopeAggregation.ts#L33-L102
[F27]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/useFilterPropertyAggregation.ts#L37-L66
[F28]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react/src/new/useOsdkAggregation.ts#L175-L248
[F29]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/inputs/PropertyFilterInput.tsx#L90-L115
[F30]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/inputs/createHistogramBuckets.ts#L17-L103
[F31]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/useFilterListState.ts#L179-L262
[F32]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/getFilterKey.ts#L22-L50
[F33]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/useFilterVisibility.ts#L33-L114
[F34]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L183-L256
[F35]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L117-L137
[F36]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterListContent.tsx#L204-L212
[F37]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/inputs/useStableData.ts#L19-L28
[F38]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/inputs/ContainsTextInput.tsx#L44-L90
[F39]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/inputs/RangeInput.tsx#L190-L250
[F40]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterListItem.tsx#L69-L208
[F41]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/CustomRendererTypes.ts#L64-L102
[F42]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L76-L147
[F43]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/inputs/PropertyFilterInput.tsx#L66-L226
[F44]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/filterValues.ts#L60-L84
[F45]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterListContent.tsx#L17-L273
[F46]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/filterStateSerialization.ts#L17-L51
[F47]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/FilterListOverview.md#L161-L165
[F48]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L24-L99
[F49]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/useStableMapEntries.ts#L17-L34
[F50]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/filterValues.ts#L86-L138
[F51]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L26-L122
[T01]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/__tests__/useFilterListState.test.tsx#L1186-L1319
[T02]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/inputs/__tests__/filteredOutValues.test.tsx#L71-L149
[T03]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/__tests__/useDualScopeAggregation.test.ts#L26-L134
[T04]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/__tests__/useFilterListState.test.tsx#L985-L1014
[T05]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/__tests__/useFilterVisibility.test.ts#L296-L310
[T06]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/inputs/__tests__/stableData.test.tsx#L33-L196
[T07]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/inputs/__tests__/ListogramInput.test.tsx#L33-L235
[T08]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/__tests__/filterStateToWhereClause.test.ts#L61-L279
[T09]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/utils/__tests__/narrowObjectSet.test.ts#L31-L229
[T10]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/__tests__/useFilterListState.test.tsx#L534-L893
[T11]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/__tests__/FilterList.test.tsx#L165-L308
