# ObjectTable：数据、交互、参数与适配边界

研究日：2026-10-01。以 npm 0.61.0 与发布提交 `37cfd38676bf04edaef5847e929d914ea214c149` 为准，版本溯源详见[报告正文](README.md)。源码、类型与上游测试分别标记，真实界面见下图。

## 一句话判断

**已确认事实：** ObjectTable 是以 OSDK 对象集为中心、用 TanStack Table 组织表格状态并用 TanStack Virtual 做行虚拟化的 UI，查询和缓存来自 `@osdk/react`。默认交互是服务端排序 + 每页 50 条的滚动加载；它不是 Ant Design Table 或 react-data-grid 的封装。[ObjectTable/useReactTable L201–237][table-runtime]、[数据 hook L162–229][table-data]、[TableBody L44–108][table-body]。

**分析：** 对已接入 Foundry/OSDK 的 EOS 对象浏览页，完整 ObjectTable 能省去 metadata、对象集、异步 function 列等集成工作；若 EOS 已有独立 API、权限和实体缓存，`BaseTable` + TanStack 实例更接近可控的适配点；若产品核心是 Excel 式键盘密集编辑，当前实现证据不足以把它视为完整数据网格替代品。选择建议属于工程判断，以下能力与限制提供依据。

## 1. 发布依赖、React 19 与可复用边界

| 证据层 | 已核验内容 | 结论边界 |
| --- | --- | --- |
| 发布源码 package.json | 包版本 0.61.0、Apache-2.0；direct dependencies 含 `@tanstack/react-table:^8.21.3`、`@tanstack/react-virtual:^3.13.13`、`@base-ui/react:>=1.0.0 <1.4.0`、dnd-kit、Blueprint icons；没有 antd/react-data-grid。 | 声明范围不是 lockfile 每个平台最终 resolve 版本。[package.json L307–336][package-deps] |
| 发布 tarball package.json | 同样的 Table/Virtual 范围与 React peer；React、React DOM、@types/react 均接受 17/18/19，OSDK api/client/react peer 都是 `^2.8.0`。发布 package 的 devDependencies 被 materialize 为 api/client/react 2.73.0；版本关系与发布溯源见[报告正文](README.md)。 | peer 接受 React 19 是作者声明兼容，React 19 浏览器回归尚未执行；源码 devDependencies 仍是 React 18.3.1。[发布源码 devDependencies L338–353][package-dev] |
| public runtime barrel | 正式子路径导出 `ObjectTable`、`BaseTable`、ColumnConfigDialog、MultiColumnSortDialog、LoadingCell/LoadingCellContent，及一组 headless hooks。ObjectTable 经 `withOsdkMetrics` 包装，BaseTable 直接导出。 | public 导出才是推荐 API；npm 内部 build 文件存在并不使深层导入成为受支持入口。[public/object-table.ts L17–161][table-public] |
| 类型 vs Base 合约 | `BaseTableProps.table` 是 `Table<TData>`，调用者须自行 `useReactTable`，数据是泛型 RowData；base 本身不抓 OSDK 对象。 | Base 可接普通业务行，但其表格状态接口依然绑定 TanStack Table，不是能直接接 AntD/react-data-grid columns 的通用皮肤。[Table.tsx L78–188][base-props] |

**EOS 建议：** React 19 可以进入验证候选，不要因 peer 范围就跳过 DOM/portal、StrictMode、虚拟滚动和编辑器回归。先固定组件及 OSDK peers 的实际 compatible versions。`0.61.0` 无 `-beta` 后缀不能单独证明产品已 GA；Beta 定位与版本溯源见[报告正文](README.md)。React 19 完整 UI 测试尚未执行。

## 2. ObjectTable 数据和渲染路径

```text
generated ObjectDefinition / InterfaceDefinition + optional ObjectSet
  → useTableSorting → SortingState → OSDK orderBy
  → useObjectTableData
      useObjectSet(enabled when objectSet exists)
      or useOsdkObjects(enabled otherwise)
      + withProperties(RDP creators)
      + paged function-column queries
  → useColumnDefs(useOsdkMetadata)
  → useReactTable(getCoreRowModel, manualSorting=true)
  → BaseTable → TableHeader / virtual TableBody / edit footer
```

这张路径图直接映射 [ObjectTable L94–134、201–249][table-runtime]、[useObjectTableData L121–229][table-data] 与 [useColumnDefs L54–84][column-defs]。对象/接口的可选 ObjectSet 真正决定 hook 路径：两个 hook 都按 React rules 调用，但互斥 enabled；这是运行实现，不是根据 props 类型猜测。[useObjectTableData L162–192][table-data]；mocked hook 测试也验证两种 enabled 分支和接口 ObjectSet 分支。[useObjectTableData.test.tsx L353–428][table-data-test]。

| 项目 | 实现行为与具体边界 |
| --- | --- |
| 默认数据 | 没有 ObjectSet 时 `useOsdkObjects(objectType)`；存在 ObjectSet 时 `useObjectSet(objectSet)`，并叠加 filter/orderBy/pageSize、ObjectSet options、RDP creators。没有 columns 时通过 metadata 的全部 properties 生成默认列。[数据 hook][table-data]、[column defs L212–236][column-defs] |
| 接口类型 | 可传 InterfaceDefinition + ObjectSet；运行路径允许它。公开合约说明 interface objectSet 的 rows 只加载接口声明 properties，非接口 underlying props 不自动出现。[ObjectTableApi L430–439][table-api]。hook 选择有 mock 测试，完整 Foundry interface 查询尚未验证。[数据 test L403–428][table-data-test] |
| RDP | `locator.type === "rdp"` 的 creators 被提取为 `withProperties` 并随对象查询送出；不是前端 `renderCell` 临时拼出的值。[useObjectTableData L135–189][table-data] |
| Function 列 | 已加载行按 pageSize 分组；每组使用当前 object type 的 base set，再用 `$primaryKey.$in` 限定该页对象；按 page × column 调 `useOsdkFunctions`，默认 maxConcurrent=10、dedupeInterval=300000ms，优先第一页各列。locator 可提供 dependsOn，pageObjects 自动作为 dependsOnObjects，支持 mutation 后 query invalidation 的底层入口。[useFunctionColumnsData L89–147、168–211][function-hook]、[functionColumns L66–103][function-utils]、[constants L35–40][table-constants] |
| Function 类型限制 | `buildPagedObjectSets` 仅当 definition.type 为 `object` 时创建 base set；interface 返回 []，因此 function 列下游 disabled。类型允许 FunctionColumnLocator 不能证明接口 function 列实际可用。[functionColumns L84–101][function-utils] |
| 缓存 | ObjectTable 默认 dedupeInterval=60000，往 OSDK hook 传递，Function 列默认 5 分钟；Table 没有自行引入 TanStack Query。 | 
| 订阅 | `streamUpdates` 被转交 list hooks。文档类型注释注明不能和 pivotTo/withProperties 同时使用；这个限制归属于平台 subscription 能力，当前 table hook 转发测试不证明 live stream 真能工作。[ObjectTableApi L459–471][table-api]、[useObjectTableData.test L646–695][table-stream-test] |

缓存行依据 [useObjectTableData defaults L107–116、options L167–189][table-data] 与 [useFunctionColumnsData L196–207][function-hook]。是否 normalize、invalidate、订阅去重由底层专题解释；此处不会把 dedupeInterval 写成完整缓存失效策略。

## 3. 虚拟化与分页：避免把“paginated”理解成页码控件

**已确认实现：** `ObjectTable` 只配置 `getCoreRowModel()`、`manualSorting: true`，没有配置 `getPaginationRowModel()`、pageIndex 或页码 UI；`fetchMore` 被接到 BaseTable 的 `fetchNextPage`。BaseTable 在 scroll event 距底部小于 100px、未 loading、没有 in-flight request 时调用；`fetchingRef` 防快速滚动重复请求；不传 `fetchNextPage` 就关闭无限滚动。[ObjectTable L201–237、292–312][table-runtime]、[Table L252–288][table-base-runtime]。

**已确认实现：** TableBody 的 `useVirtualizer` count 只等于已加载 `rows.length`，以 rowHeight 估计大小，默认 40px、overscan 5。只有 virtual rows 被 render，每一行却 render `row.getVisibleCells()` 的全部可见列；没有横向列虚拟化或 per-row 动态测量回调。TableRow 的高度与 translateY 都由 virtualRow 给出；CSS 默认 cell 内容 nowrap + ellipsis。[TableBody L57–108][table-body]、[TableRow L72–94][table-row]、[constants L21–33][table-constants]、[TableCell CSS L62–68][table-cell-css]。

**分析与限制：** row virtualizer 减少 DOM 行数，没有限制已经加载的对象数组/缓存/Function 列数据数量；不能据此宣称百万行内存稳定。长文本换行、异步扩高或大量列需要 EOS 本地性能检查。传统“跳到第 N 页”、远程随机页码分页、列虚拟化都不是此 ObjectTable 发布实现已经提供的能力。BaseTable 可由调用方预先放入不同 row model，因此可建立自有分页适配，但这属于新集成工作。

**Base adapter 的静态集成风险：** `fetchNextPage` 开始时 setIsLoadingMore(true)，promise finally 只清 fetchingRef；isLoadingMore 的清理来自依赖 `[isLoading, fetchNextPage]` 的 effect。若消费方 callback 稳定且抓取期间从不改变 isLoading，第一次 promise 结束后仅更改data，可能不会触发该effect、后续滚动因此仍被 isLoadingMore guard阻止。调用方应正确驱动loading生命周期；这是一条基于代码路径的风险，**尚无浏览器复现，属于静态风险推断**。[Table L252–281][table-base-runtime]。

初始无 rows 的 loading 用 LoadingStateTable；已有 rows 时保留表体，加载下一批插入 skeleton row；error 渲染 Error Loading Data，空数据则用 renderEmptyState 或默认 No Data。[Table L335–383][table-base-tail]。实际浏览器中的闪烁与 scroll restore 行为尚未验证。

## 4. 排序和列管理

| 能力 | 运行证据 | 注意 |
| --- | --- | --- |
| 受控/非受控排序 | `orderBy !== undefined` 定义 controlled，`defaultOrderBy` 只 seed internal state；onSortingChange 只在非受控更新 internal，但两种模式都发 onOrderByChanged。array 顺序转换到 TanStack SortingState；数据 hook reduce 成 OSDK orderBy。[useTableSorting L72–115、118–139][table-sort] | 受控 props 的 callback 在 TS 是 optional；如果传 orderBy 又不回写，UI 动作不会持久改变排序。JSDoc 称 required 不是运行 guard。[ObjectTableApi L575–596][table-api] |
| 服务端排序 | `manualSorting:true`，没有 getSortedRowModel；function columns `enableSorting:false`；RDP id 可进 orderBy，与 withProperties 一起请求。[ObjectTable L224][table-runtime]、[useColumnDefs L168–174][column-defs] | 自定义 getCellValue 不自动变成服务器 sort expression；custom locator 应显式 `orderable:false`，避免把虚拟列 id 发给服务器。当前 story 的 custom columns 也这么设置。[Editing story L140–160][editing-story] |
| 表头排序路径 | menu 的升/降序会 setSorting 单列数组；多列排序通过 MultiColumnSortDialog 后 setSorting，显示各 sort 的优先级序号。普通 header 点击只有 onColumnHeaderClick listener，不绑定 toggle sorting。[TableHeaderWithPopover L146–175、217–257、279–307][table-header-menu]、[TableHeader L104–110][table-header] | 与“一点击表头循环升降序”的常见表格预期不同。EOS 可监听 header click 实现自己行为，但要避免与 menu 相冲突。 |
| 列显示/顺序 | initial 由 definitions 的 meta.isVisible、array order 生成，allColumns 改变会 effect 重置两种 state；ColumnConfigDialog Apply 调 setColumnOrder 再 setColumnVisibility。[useColumnVisibility L73–125][column-visibility]、[TableHeader L112–123][table-header] | 非完整受控 columns state；不能只把回调写进 Zustand/Jotai 就认为组件会读取它。defs 引用/metadata 变化可能覆盖用户手动调整，应用应 memoize definitions并验证偏好恢复。 |
| 列 pin | initial definitions 可左/右；selection column 固定加入 left；definitions 改变会重新 seed；callback 只枚举新 state 里 left/right，并排除 selection。内置 menu “Pin column” 只 pin-left；right 可从 definition 设置。[useColumnPinning L68–101、123–164][column-pinning]、[TableHeaderWithPopover L128–144][table-header-menu] | callback 类型列出 none，但 `convertColumnPinningStateToArray` 没为被 unpin 的列发显式 none，消费方要比较整套状态，不能假设每次都是逐列事件。 |
| 列 resize | internal ColumnSizingState，onChange 实时 resize、ltr；changed width 回调、被 reset 的 key 发 null；header drag用 TanStack resize handler，double click reset。[ObjectTable L222–227][table-runtime]、[useColumnResize L29–59][column-resize]、[TableHeader L175–182][table-header] | 不是 externally controlled widths prop；定义 width/min/max 被转换为 size/minSize/maxSize。 |
| pin DOM | 左/右偏移取 TanStack getStart/getAfter、width取getSize；cell CSS position:sticky。[getColumnPinningStyles L24–35][pin-styles]、[TableCell CSS L38–55][table-cell-css] | 未验证大量 pin columns、RTL 或 AntD Drawer 的特殊布局。本发布 columnResizeDirection 明确 ltr。 |

**源码注释与实现小差异：** ObjectTableApi 对列 visibility 的 JSDoc 说 callback 会返回 display order；运行 callback 仅 Object.entries(newState)，独立 onColumnOrderChange 不发 callback。因此不应把 onColumnVisibilityChanged 当可靠的完整列排序持久化 API。[ObjectTableApi L506–518][table-api]、[useColumnVisibility L90–125][column-visibility]。需要列偏好全受控时优先 BaseTable 中自建 state。

## 5. 行选择、全选与焦点

selectionMode 默认 none；single 与 multiple 都有行 checkbox，multiple 另有 header checkbox。selectedRows 是 primary key 数组，存在时 controlled；isAllSelected 在 controlled 模式可覆盖 selectedRows 数组让已加载行全选。[ObjectTable L74–76、156–170][table-runtime]、[useSelectionColumn L65–94][selection-column]、[useRowSelection L89–125][row-selection]。

**重要的三种数据：**

1. `selectedRows` prop：primary key 数组，用于 controlled UI。
2. `onRowSelectionChanged.selectedRows`：只能从当前 loaded `data` 筛出实际 object instances，既不是所有匹配对象，也不是全部永续跨查询选择。[useRowSelection L131–143][row-selection]。
3. callback 的 `objectSet`：ObjectTable 外层根据 resultingObjectSet 派生；普通 partial selection 是 `$primaryKey.$in`；显式 selectAll 且 loaded selectedRows 非空，则直接返回**完整 resultingObjectSet**，不会先把整个对象集拉进内存。[ObjectTable L136–147][table-runtime]、[deriveSelectionObjectSet L37–54][selection-objectset]。

**已确认实现：** uncontrolled header select-all 保留 internalIsAllSelected，当 fetchMore 带来新行会自动勾选，并 re-fire callback；controlled 模式不会自动调用 callback，只按新 data 计算勾选状态。[useRowSelection L82–112、228–244][row-selection]。在 partial/indeterminate 时点 header 是清空，不是补为全部选中；一次 toggle row 会退出 select-all。Shift click 按已加载 data index 做区间，合并既有 selection。[useRowSelection L147–225、280–303][row-selection]。

**EOS 建议：** 批量业务 Action 用 full `objectSet` 还是用当前 loaded instances，应是明确产品语义；例如“选择全部搜索结果”不等于“选择眼前这一页”。筛选/排序/数据替换后，调用方应定义 selection reset 或重映射；当前 implementation 没有统一自动 query-change reset。不要将这个 UI 标记当服务端 authorization，只在业务执行处验证权限与 Action 可适用性。

**焦点边界：** focusedRow 表示视觉上的 last-interacted row，click capture 设置 row id；edit mode 时 onRowClick 暂停；outer pointerdown 清掉焦点，portalTracker避免 dropdown portal 被误判为外部。它不是 WAI-ARIA grid 的单元格 keyboard focus model。[TableRow L49–59、72–94][table-row]、[Table L236–250、300–323][table-base-runtime]、[ObjectTableApi L638–660][table-api]。

**测试证据：** upstream hook tests mock 数据验证 Shift range、partial header清空、select-all 后 data增长、controlled 模式；deriveSelectionObjectSet test 明确断言 select-all 返回原对象集、partial/deselect调用 where。[row-selection test L565–707][row-selection-test]、[deriveSelectionObjectSet test L45–88][selection-objectset-test]。有一个 test title 说 “no stale anchor”，但 L552–560 的实际 assertion 仍期待之前 anchor 形成 [1..3] 范围；**只按 assertion读结论**，不能照测试标题宣布 anchor被清除。[row-selection test L523–563][row-selection-anchor-test]。

## 6. 单元格交互与编辑

| 能力 | 发布运行实现 | 限制/验证层 |
| --- | --- | --- |
| 读值/renderer | getCellValue 若存在则成为 accessorFn；否则 accessorKey取locator.id。renderCell只在当前不editable时使用，编辑器接管后不使用自定义display renderer。[useColumnDefs L133–205][column-defs] | 类型约束要求 getCellValue 与 cellValueType配对；需要区分 value transformation 与仅改变 display。类型test与runtime rendering test各有覆盖。[useColumnDefs test L433–475、567–620、651–836][column-defs-test] |
| editor 类型 | 内置 text/number input，数据类型为 datetime/timestamp 或显式 DATE_PICKER 用 DatePicker，显式 DROPDOWN 用 DropdownCellField；dropdown props可依当前 row 和 row pending edits。[EditableCell L263–330][editable-cell] | `date` 没在 auto DATE_TYPES 列表；不用文档“日期编辑”泛称所有 wire date类型自动正确。编辑器只是有限集合，无任意 renderEditor public slot证据。 |
| 输入 commit | text/number blur 才 commit；Enter触发blur，Escape回到currentValue后blur；数值空串转null、Number转换失败保留string；Dropdown/DatePicker change即commit。[EditableCell L85–101、186–261][editable-cell] | 没有 spreadsheet cell navigation、range selection、复制粘贴、多单元格fill/undo的运行实现。相关键盘处理集中在editor与selection handlers；“clipboard export”的文档表述不能证明存在内置剪贴板grid功能。 |
| local draft | useEditableTable record存 CellEditInfo，包括rowId/columnId/oldValue/newValue/originalRowData；回到原值删除draft；null和undefined当相同空值，空字符串另算。[useEditableTable L68–117][editable-hook] | 不是直接编辑Observable cache的对象属性，不自动调用Ontology Action。onCellValueChanged可以监听commit；业务将draft map成Action params是消费方职责。 |
| async validation | commit先储存newValue并触发callback，再runValidation；新的输入/commit取消旧validation结果race；错误显示Tooltip；底栏validationErrors已有值时禁submit。[EditableCell L146–210][editable-cell]、[TableEditContainer L43–63、112–119][edit-footer] | AbortController使过期结果不应用，不向 validateEdit传signal，因此不能保证取消用户validator里的网络/副作用。实现没有pending-validation state送到底栏；静态推断：新validation尚未resolve时，如果旧error为空，submit可能仍可用。需EOS运行验证/业务submit二次校验。 |
| submit | 只有onSubmitEdits存在才显示submit；promise true才clear草稿并退出manual edit；false则保留，finally解除submitting。[useEditableTable L124–153][editable-hook]、[TableEditContainer L50–70、112–119][edit-footer] | 没有内置Ontology Action metadata、权限提示或跨行事务保证；promise throw路径没有本组件catch成可见错误，调用方应处理和反馈。 |
| editable 声明≠运行可编辑 | API union包含 EditableFunctionColumnDefinition，但DefaultCellRenderer遇function AsyncCellData直接render AsyncValueCell；CBAC/MANDATORY也先走专用display renderer。[ObjectTableApi L257–269][table-api]、[DefaultCellRenderer L64–78][default-cell] | 必须以renderer分支为准，不写“任意function值可就地持久化编辑”。在function列标editable甚至可能出现编辑footer，但值仍server-computed read-only。 |
| selection keyboard | 行checkbox wrapper的Enter调onToggleRow，并读取shiftKey；注释明确Shift+Space待处理，因两次toggle。[SelectionCells L50–83][selection-cells] | Checkbox/BaseUI仍有其自身键盘行为，但不能推导完整cell keyboard grid。 |
| context menu | TableCell右键时render consumer内容；selection cell不展示；CellContextMenu 用createPortal到document.body，自定义内容自己负责语义。[TableCell L54–97][table-cell]、[CellContextMenu L38–67][cell-context] | 表头menu使用BaseUI/Menu与局部portal container；cell context menu路径不同，EOS modal/drawer/z-index要实测。不是内置copy/edit/delete菜单。 |

**测试边界：** useEditableTable test验证submit收到两条edits，未证明服务器写入；EditableCell test用fake timers证明过时validation不显示、成功会clear错误、Boolean dropdown能提交false/true；Storybook Editing story的handler展示lastEdit/UI，仍不是生产Ontology Action。[useEditableTable test L236–280][editable-hook-test]、[EditableCell test L46–125、153–309][editable-cell-test]、[Editing story L174–210][editing-story]。

## 7. Snapshot/下载边界

公开tableRef exposes getSnapshot；snapshot读取当前可见leaf columns，排除selection与custom locator；按 resolved ObjectSet.asyncIter 拉取匹配全量对象，默认rowLimit=10000，已知totalCount时提前拒绝、未知时超过limit中途拒绝。format-agnostic rows/columns由调用者转换CSV/XLSX/JSON，不提供默认下载按钮。[useObjectTableSnapshot L119–178、209–236][table-snapshot]、[default rowLimit L32–37][snapshot-utils]。

function columns export按页受限并发调用函数（默认10），失败在该页的cells保留 Error而不是drop整个snapshot。[objectTableSnapshot L90–120、134–178][snapshot-utils]。值得区分：snapshot “全量抓取”是另一次本地内存收集，与表体DOM行虚拟化无关。

**已确认数据语义：** property/RDP snapshot buildSnapshotRow直接读 `object[columnId]`，不调用column.getCellValue transformation、display renderer或pending cellEdits。[buildSnapshotRow L45–79][snapshot-utils]。因此下载值可能与经过 getCellValue/格式化后的显示不同；custom列即使getCellValue能展示也被排除。业务要求“所见即所得导出”时需自行实现转换。

## 8. BaseTable / headless hooks 对 EOS 的适配判断

| 路径 | 适用情境 | 接入工作 | 当前证据给出的限制 |
| --- | --- | --- | --- |
| 完整 ObjectTable | EOS页面真实使用generated OSDK type与ObjectSet，需要metadata列、RDP、Function列、Action后缓存同步 | 接provider/client/generated SDK，传definitions/filter/objectSet；编辑提交映射到业务Action；fixed版本/CSS setup | 数据层依OSDK、server ordering，不是任意REST data prop；React19尚需产品内回归 |
| OSDK hooks → EOS现有 AntD/react-data-grid | EOS有成熟table UI，只缺Ontology fetch/cache与function列数据 | 将useObjectTableData结果映射rows、把EOSsort/filter转换为OSDK，调用fetchMore；用useFunctionColumnsData异步状态映射自有cell | hooks/columns仍有OSDK类型耦合；不建议把useColumnDefs输出TanStack ColumnDef直接塞AntD。导出hooks在public barrel已确认。[table-public] |
| EOS API/cache → BaseTable | 想复用Palantir列菜单/虚拟行UI，数据来源独立 | 自建TanStack useReactTable、controlled state、columns/cell、loading/fetchNextPage、editableConfig；BaseTable只消费实例 | 自有Zustand/Jotai可以管sort/selection/drafts；服务端entity query/cache应由EOS已有cache owner管，不要对相同entities双写OSDK cache与自有store |
| 自主实现 EOS对象浏览器 | 多源实体、复杂权限、saved views、强键盘编辑、批量事务是中心需求 | 复用“对象集查询语义 → table state”的设计思路，选适配EOS的UI/cache | 需要自己实现facet count、跨页all-selection、permission/action validation等语义；不应仅因源码Apache-2.0就复制依赖/图标/assets且忽视各自licenses |

上表是**建议**，不是对 AntD/react-data-grid 或 Zustand/Jotai 自身能力的未经查证比较。主要依据是本包明确的outer/base/public-hook seams：[BaseTable props][base-props]、[public exports][table-public]。BaseTable的官方示例使用普通Person[]和本地 `getSortedRowModel`，这说明消费方可以建立前端sort的base adapter；而完整ObjectTable明确服务端sort，两者要分开。[BaseTable story L20–79、81–130][base-story]。

**本地化边界：** 历史0.41 CHANGELOG称加入labels prop，但当前0.61发布ObjectTableApi/BaseTableProps里未找到labels、菜单/footer仍硬编码英文。不能把历史发布说明当作当前合约。EOS中文流程需逐项检查当前public props，或使用自己的UI adapter；这段不推断当年commit为何未保留。[历史CHANGELOG L320–325][labels-changelog]、[当前菜单 L263–321][table-header-menu]、[当前footer L98–119][edit-footer]。同一CHANGELOG的0.38明确建议hook消费方安装匹配此包的TanStack Table版本以避免type incompatibility。[CHANGELOG L339–344][hooks-changelog]。

## 9. 实际界面

![ObjectTable 默认表格](assets/01-object-table.jpg)

官方 Storybook 实拍，mock 对象数据。表格展示对象属性与已加载行；滚动虚拟化并不改变查询分页语义。

![列菜单](assets/02-column-menu.jpg)

点击姓名列菜单后，实际看到排序、pin、配置入口。

![列配置](assets/03-column-config.jpg)

列配置对话框显示可用属性、显示/隐藏与次序选项。来源、尺寸、摘要见 [assets.md](assets.md)。

## 10. 有限验证记录

- 固定源码范围 diff：`git diff 37cfd38676bf04edaef5847e929d914ea214c149 e53b94ecd5de7cdd7e864d0daa04363bdad4db4c -- packages/react-components/src/object-table packages/react-components/src/public/object-table.ts packages/react-components/docs/ObjectTable.md packages/react-components-storybook/src/stories/ObjectTable`，exit 0、无输出（2026-10-01）。
- 直接核对下载tarball ESM：ObjectTable manualSorting、TableBody useVirtualizer、Table scroll阈值、function column enableSorting=false、edit footer validation disabled均存在；public barrel与源码一致。
- 孤立published artifact helper probes：[table probe](probes/table-artifact-probes.mjs)，exit 0，输出 `probes:passed`。验证 partial selection `$primaryKey.$in`、select-all返回原ObjectSet、deselect空集、无underlying set时undefined；验证默认constants与snapshot10000；验证function snapshot失败保留Error、传maxConcurrent=1实际peak=1。纯helper synthetic callback，**无network、React render、真实Foundry、Ontology Action**；从internal build路径import只是研究探针，不作为生产建议。
- 未执行完整上游vitest/Storybook test suite；上述上游test证据来自其assertions。selection anchor测试的title与assertion存在差异，具体见行选择一节。

## 11. 配套筛选器

完整筛选和链接聚合语义见 [FilterList 专题](filter-list.md)。

[package-deps]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/package.json#L307-L336
[package-dev]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/package.json#L338-L353
[labels-changelog]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/CHANGELOG.md#L320-L325
[hooks-changelog]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/CHANGELOG.md#L339-L344
[table-runtime]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTable.tsx#L94-L312
[table-data]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useObjectTableData.ts#L107-L229
[table-body]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/TableBody.tsx#L44-L108
[table-public]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/object-table.ts#L17-L161
[base-props]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L78-L188
[column-defs]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useColumnDefs.tsx#L54-L252
[table-api]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L38-L789
[function-hook]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useFunctionColumnsData.ts#L73-L317
[function-utils]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/functionColumns.ts#L66-L103
[table-constants]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/constants.ts#L17-L42
[table-base-runtime]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L200-L334
[table-base-tail]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L335-L387
[table-row]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/TableRow.tsx#L49-L94
[table-cell-css]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/TableCell.module.css#L17-L68
[table-sort]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useTableSorting.ts#L72-L139
[table-header-menu]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/TableHeaderWithPopover.tsx#L103-L323
[table-header]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/TableHeader.tsx#L70-L200
[column-visibility]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useColumnVisibility.ts#L73-L156
[column-pinning]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useColumnPinning.ts#L68-L164
[column-resize]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useColumnResize.ts#L29-L59
[pin-styles]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/getColumnPinningStyles.ts#L24-L35
[selection-column]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useSelectionColumn.tsx#L65-L94
[row-selection]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useRowSelection.ts#L69-L392
[selection-objectset]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/deriveSelectionObjectSet.ts#L37-L54
[selection-cells]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/SelectionCells.tsx#L28-L83
[editable-cell]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/EditableCell.tsx#L85-L330
[editable-hook]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useEditableTable.ts#L68-L153
[edit-footer]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/TableEditContainer.tsx#L31-L123
[default-cell]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/DefaultCellRenderer.tsx#L56-L134
[table-cell]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/TableCell.tsx#L38-L99
[cell-context]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/CellContextMenu.tsx#L32-L67
[table-snapshot]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useObjectTableSnapshot.ts#L119-L236
[snapshot-utils]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/objectTableSnapshot.ts#L32-L219
[table-data-test]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/__tests__/useObjectTableData.test.tsx#L353-L470
[table-stream-test]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/__tests__/useObjectTableData.test.tsx#L646-L695
[row-selection-test]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/__tests__/useRowSelection.test.tsx#L565-L707
[row-selection-anchor-test]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/__tests__/useRowSelection.test.tsx#L523-L563
[selection-objectset-test]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/__tests__/deriveSelectionObjectSet.test.ts#L45-L88
[column-defs-test]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/__tests__/useColumnDefs.test.tsx#L433-L836
[editable-hook-test]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/__tests__/useEditableTable.test.ts#L236-L280
[editable-cell-test]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/__tests__/EditableCell.test.tsx#L46-L309
[table-story]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/src/stories/ObjectTable/ObjectTable.stories.tsx#L38-L83
[base-story]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/src/stories/ObjectTable/BaseTable.stories.tsx#L20-L304
[editing-story]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/src/stories/ObjectTable/Features/Editing.stories.tsx#L49-L210
[sorting-story]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/src/stories/ObjectTable/Features/Sorting.stories.tsx
[selection-story]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/src/stories/ObjectTable/Features/Selection.stories.tsx
[columns-story]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/src/stories/ObjectTable/Features/Columns.stories.tsx
