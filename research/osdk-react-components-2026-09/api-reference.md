# @osdk/react-components 0.61.0：公共导出与组件参数图鉴

核验日期：2026-10-01。锁定实际 npm tarball 和发布源码 commit `37cfd38676bf04edaef5847e929d914ea214c149`；稳定子路径不代表产品已 GA。本附录依据公开 barrel、实际 `build/types`、ESM export 和发布实现核对。类型描述可调用形状；运行时说明单独指出实际行为。未执行 React 19 全量组件测试、生产 Ontology 或 Action。

[机器可检索导出索引](./public-export-inventory.json) 记录每个符号的 runtime/type 分类、公开入口、发布声明文件和固定源码位置。组件参数表覆盖所有主/Base 家族；公开 hooks、配置类型、PDF building blocks 的完整符号名也在索引中。继承 React/Base UI 外部属性的 primitives 明确保留外部类型边界，不推测外部版本的全部参数。

## 1. 导出入口总览

实际 manifest 有 **30 个 JS 入口**（包括空根、兼容入口与 aggregate）、另有 `styles.css`；去重后 **98 个 runtime + 170 个显式 type export = 268 个(kind,name)符号**。某些 enum/const 同时可用于值与类型；本统计按照 barrel 的显式导出语法，不把类型/值空间当作同一概念。

根入口 `import {...} from "@osdk/react-components"` 没有组件导出。wildcard 只映射已有 public 文件，不能据此将内部 build 目录当作公共 API。

| 入口（省略包名前缀） | Runtime / Type 个数 | 运行时公开符号 | 状态与用途 |
|---|---:|---|---|
| [`.`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/index.ts) | 0 / 0 | — | 空入口 |
| [`./action-form`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/action-form.ts) | 2 / 26 | `ActionForm`、`BaseForm` | 稳定子路径；组件仍为 Beta 产品 |
| [`./document-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/document-viewer.ts) | 2 / 1 | `DocumentViewer`、`ViewerType` | 稳定子路径；组件仍为 Beta 产品 |
| [`./email-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/email-viewer.ts) | 2 / 4 | `BaseEmailViewer`、`EmailViewer` | 稳定子路径；组件仍为 Beta 产品 |
| [`./experimental`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental.ts) | 90 / 161 | `ActionForm`、`BaseForm`、`CbacBanner`、`CbacBannerPopover`、`CbacPicker`、`CbacPickerDialog`、`BaseCbacBanner`、`BaseCbacPicker`、`BaseCbacPickerDialog`、`computeMarkingStates`、`groupMarkingsByCategory`、`toggleMarking`、`MaxClassificationField`、`DocumentViewer`、`ViewerType`、`BaseEmailViewer`、`EmailViewer`、`BaseFilterList`、`FilterList`、`deserializeFilterStates`、`serializeFilterStates`、`FilterPopover`、`FilterInput`、`useFilterListState`、`filterHasActiveState`、`NO_VALUE`、`getFilterKey`、`getFilterLabel`、`summarizeFilterValue`、`narrowObjectSet`、`BaseImageViewer`、`ImageViewer`、`BaseMarkdownViewer`、`MarkdownViewer`、`MarkdownRenderer`、`MarkdownViewerMedia`、`ObjectTable`、`BaseTable`、`ColumnConfigDialog`、`MultiColumnSortDialog`、`LoadingCell`、`LoadingCellContent`、`useFunctionColumnsData`、`useObjectTableData`、`useColumnDefs`、`useSelectionColumn`、`useColumnPinning`、`useColumnResize`、`useColumnVisibility`、`useFocusedRow`、`useLoadedObjectsChanged`、`useRowSelection`、`useTableSorting`、`useEditableTable`、`useObjectTableSnapshot`、`useCellContextMenu`、`BasePdfViewer`、`PdfViewerAnnotationLayer`、`PdfViewerContent`、`PdfViewerOutlineSidebar`、`PdfViewerSearchBar`、`PdfViewerSidebar`、`PdfViewerToolbar`、`usePdfAnnotationPortals`、`usePdfAnnotationsByPage`、`usePdfDocument`、`usePdfFormFields`、`usePdfHighlightMode`、`usePdfOutline`、`usePdfViewer`、`usePdfViewerSearch`、`usePdfViewerSync`、`PdfViewerProvider`、`usePdfViewerContext`、`usePdfViewerInstance`、`usePdfViewerCore`、`usePdfViewerState`、`PdfViewer`、`BaseSpreadsheetViewer`、`SpreadsheetViewer`、`OsdkThemeProvider`、`useOsdkTheme`、`BaseTiffViewer`、`TiffViewer`、`TiffRenderer`、`TiffViewerMedia`、`BaseVideoViewer`、`VideoViewer`、`BaseXmlViewer`、`XmlViewer` | 兼容 aggregate；不包含 AIP Chat |
| [`./filter-list`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/filter-list.ts) | 13 / 17 | `BaseFilterList`、`FilterList`、`deserializeFilterStates`、`serializeFilterStates`、`FilterPopover`、`FilterInput`、`useFilterListState`、`filterHasActiveState`、`NO_VALUE`、`getFilterKey`、`getFilterLabel`、`summarizeFilterValue`、`narrowObjectSet` | 稳定子路径；组件仍为 Beta 产品 |
| [`./image-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/image-viewer.ts) | 2 / 2 | `BaseImageViewer`、`ImageViewer` | 稳定子路径；组件仍为 Beta 产品 |
| [`./markdown-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/markdown-viewer.ts) | 2 / 2 | `BaseMarkdownViewer`、`MarkdownViewer` | 稳定子路径；组件仍为 Beta 产品 |
| [`./object-table`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/object-table.ts) | 20 / 51 | `ObjectTable`、`BaseTable`、`ColumnConfigDialog`、`MultiColumnSortDialog`、`LoadingCell`、`LoadingCellContent`、`useFunctionColumnsData`、`useObjectTableData`、`useColumnDefs`、`useSelectionColumn`、`useColumnPinning`、`useColumnResize`、`useColumnVisibility`、`useFocusedRow`、`useLoadedObjectsChanged`、`useRowSelection`、`useTableSorting`、`useEditableTable`、`useObjectTableSnapshot`、`useCellContextMenu` | 稳定子路径；组件仍为 Beta 产品 |
| [`./pdf-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/pdf-viewer.ts) | 22 / 33 | `BasePdfViewer`、`PdfViewerAnnotationLayer`、`PdfViewerContent`、`PdfViewerOutlineSidebar`、`PdfViewerSearchBar`、`PdfViewerSidebar`、`PdfViewerToolbar`、`usePdfAnnotationPortals`、`usePdfAnnotationsByPage`、`usePdfDocument`、`usePdfFormFields`、`usePdfHighlightMode`、`usePdfOutline`、`usePdfViewer`、`usePdfViewerSearch`、`usePdfViewerSync`、`PdfViewerProvider`、`usePdfViewerContext`、`usePdfViewerInstance`、`usePdfViewerCore`、`usePdfViewerState`、`PdfViewer` | 稳定子路径；组件仍为 Beta 产品 |
| [`./primitives`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/primitives.ts) | 5 / 4 | `ActionButton`、`Dialog`、`SkeletonBar`、`Tooltip`、`TooltipArrow` | 稳定子路径；组件仍为 Beta 产品 |
| [`./spreadsheet-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/spreadsheet-viewer.ts) | 2 / 4 | `BaseSpreadsheetViewer`、`SpreadsheetViewer` | 稳定子路径；组件仍为 Beta 产品 |
| [`./tiff-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/tiff-viewer.ts) | 2 / 2 | `BaseTiffViewer`、`TiffViewer` | 稳定子路径；组件仍为 Beta 产品 |
| [`./video-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/video-viewer.ts) | 2 / 2 | `BaseVideoViewer`、`VideoViewer` | 稳定子路径；组件仍为 Beta 产品 |
| [`./xml-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/xml-viewer.ts) | 2 / 2 | `BaseXmlViewer`、`XmlViewer` | 稳定子路径；组件仍为 Beta 产品 |
| [`./experimental/action-form`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/action-form.ts) | 2 / 26 | `ActionForm`、`BaseForm` | 弃用兼容入口，优先稳定子路径 |
| [`./experimental/aip-agent-chat`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/aip-agent-chat.ts) | 3 / 5 | `AipAgentChat`、`BaseAipAgentChat`、`getUIMessageText` | experimental 专用 |
| [`./experimental/cbac-picker`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/cbac-picker.ts) | 11 / 8 | `CbacBanner`、`CbacBannerPopover`、`CbacPicker`、`CbacPickerDialog`、`BaseCbacBanner`、`BaseCbacPicker`、`BaseCbacPickerDialog`、`computeMarkingStates`、`groupMarkingsByCategory`、`toggleMarking`、`MaxClassificationField` | experimental 专用 |
| [`./experimental/document-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/document-viewer.ts) | 2 / 2 | `DocumentViewer`、`ViewerType` | 弃用兼容入口，优先稳定子路径 |
| [`./experimental/email-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/email-viewer.ts) | 2 / 4 | `BaseEmailViewer`、`EmailViewer` | 弃用兼容入口，优先稳定子路径 |
| [`./experimental/filter-list`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/filter-list.ts) | 13 / 17 | `BaseFilterList`、`FilterList`、`deserializeFilterStates`、`serializeFilterStates`、`FilterPopover`、`FilterInput`、`useFilterListState`、`filterHasActiveState`、`NO_VALUE`、`getFilterKey`、`getFilterLabel`、`summarizeFilterValue`、`narrowObjectSet` | 弃用兼容入口，优先稳定子路径 |
| [`./experimental/image-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/image-viewer.ts) | 2 / 2 | `BaseImageViewer`、`ImageViewer` | 弃用兼容入口，优先稳定子路径 |
| [`./experimental/markdown-renderer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/markdown-renderer.ts) | 4 / 3 | `BaseMarkdownViewer`、`MarkdownViewer`、`MarkdownRenderer`、`MarkdownViewerMedia` | 弃用兼容入口，优先稳定子路径 |
| [`./experimental/object-table`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/object-table.ts) | 20 / 51 | `ObjectTable`、`BaseTable`、`ColumnConfigDialog`、`MultiColumnSortDialog`、`LoadingCell`、`LoadingCellContent`、`useFunctionColumnsData`、`useObjectTableData`、`useColumnDefs`、`useSelectionColumn`、`useColumnPinning`、`useColumnResize`、`useColumnVisibility`、`useFocusedRow`、`useLoadedObjectsChanged`、`useRowSelection`、`useTableSorting`、`useEditableTable`、`useObjectTableSnapshot`、`useCellContextMenu` | 弃用兼容入口，优先稳定子路径 |
| [`./experimental/pdf-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/pdf-viewer.ts) | 22 / 33 | `BasePdfViewer`、`PdfViewerAnnotationLayer`、`PdfViewerContent`、`PdfViewerOutlineSidebar`、`PdfViewerSearchBar`、`PdfViewerSidebar`、`PdfViewerToolbar`、`usePdfAnnotationPortals`、`usePdfAnnotationsByPage`、`usePdfDocument`、`usePdfFormFields`、`usePdfHighlightMode`、`usePdfOutline`、`usePdfViewer`、`usePdfViewerSearch`、`usePdfViewerSync`、`PdfViewerProvider`、`usePdfViewerContext`、`usePdfViewerInstance`、`usePdfViewerCore`、`usePdfViewerState`、`PdfViewer` | 弃用兼容入口，优先稳定子路径 |
| [`./experimental/spreadsheet-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/spreadsheet-viewer.ts) | 2 / 4 | `BaseSpreadsheetViewer`、`SpreadsheetViewer` | 弃用兼容入口，优先稳定子路径 |
| [`./experimental/theme`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/theme.ts) | 2 / 4 | `OsdkThemeProvider`、`useOsdkTheme` | experimental 专用 |
| [`./experimental/tiff-renderer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/tiff-renderer.ts) | 4 / 3 | `BaseTiffViewer`、`TiffViewer`、`TiffRenderer`、`TiffViewerMedia` | 弃用兼容入口，优先稳定子路径 |
| [`./experimental/video-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/video-viewer.ts) | 2 / 2 | `BaseVideoViewer`、`VideoViewer` | 弃用兼容入口，优先稳定子路径 |
| [`./experimental/xml-viewer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/xml-viewer.ts) | 2 / 2 | `BaseXmlViewer`、`XmlViewer` | 弃用兼容入口，优先稳定子路径 |

## 2. 表格、筛选、表单、Chat、CBAC、主题与 primitives

本表同时包含若干配置接口；是否可以 named import 以公开符号 JSON 为准。表中 Required 是属性声明的必填性；联合类型中的受控分支另标“条件必填”。Default 优先记录源码明确值或公开 @default，写 undefined/未声明不代表某个底层库永远没有默认值。泛型名称的约束在组件说明与源码中；flatten 只是检索表，不能代替完整判别联合。

### ObjectTable / `ObjectTableProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts)；实际发布声明：`build/types/object-table/ObjectTableApi.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

泛型 Q extends ObjectOrInterfaceDefinition；RDPs 和 FunctionColumns 分别描述派生属性和函数列。排序由 orderBy 控制，defaultOrderBy 仅初始化；selectedRows/isAllSelected 可控制选择。列显示/固定/顺序仍以组件内部状态和定义为主。tableRef 是显式 prop，不能改写成组件 ref。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTable.tsx)。

泛型：`Q extends ObjectOrInterfaceDefinition`；`RDPs extends Record<string, SimplePropertyDef> = {}`；`FunctionColumns extends Record<string, QueryDefinition<{}>> = Record<string, never>`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`objectType`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L428) | `Q` | 必填 | 无；必须提供 | 对象或接口类型定义；用于元数据和查询。 | 数据/呈现/能力配置 |
| [`objectSet`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L439) | `ObjectSet<Q>` | 可选 | undefined / 未声明 | 限定输入对象集；省略时通常查询整个类型。 | 数据/呈现/能力配置 |
| [`columnDefinitions`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L446) | `Array<ColumnDefinition<Q, RDPs, FunctionColumns>>` | 可选 | undefined / 未声明 | 配置属性、RDP、custom 或 function 列。 | 数据/呈现/能力配置 |
| [`objectSetOptions`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L448) | `ObjectSetOptions<Q>` | 可选 | undefined / 未声明 | 对基础对象集执行 union/intersect/subtract。 | 数据/呈现/能力配置 |
| [`dedupeIntervalMs`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L457) | `number` | 可选 | 60000 ms | 查询去重窗口，单位毫秒。 | 数据/呈现/能力配置 |
| [`streamUpdates`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L471) | `boolean` | 可选 | false | 订阅对象集的流更新。 | 数据/呈现/能力配置 |
| [`pageSize`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L478) | `number` | 可选 | 50 | 每次增量加载的行数。 | 数据/呈现/能力配置 |
| [`filter`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L483) | `WhereClause<Q, RDPs>` | 可选 | undefined / 未声明 | 作用于表格输入对象集的 WhereClause。 | 数据/呈现/能力配置 |
| [`enableColumnConfig`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L490) | `boolean` | 可选 | true | 启用列配置入口。 | 数据/呈现/能力配置 |
| [`enableColumnPinning`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L497) | `boolean` | 可选 | true | 显示列固定菜单。 | 数据/呈现/能力配置 |
| [`enableColumnResizing`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L504) | `boolean` | 可选 | true | 启用列宽调整入口。 | 数据/呈现/能力配置 |
| [`onColumnVisibilityChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L513) | `(newStates: Array<{ columnId: PropertyKeys<Q> \| keyof RDPs \| keyof FunctionColumns; isVisible: boolean; }>) => void` | 可选 | undefined / 未声明 | 通知列显示状态变化。 | 回调/事件；不会自动持久化 |
| [`onColumnsPinnedChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L527) | `(newStates: Array<{ columnId: PropertyKeys<Q> \| keyof RDPs \| keyof FunctionColumns; pinned: "left" \| "right" \| "none"; }>) => void` | 可选 | undefined / 未声明 | 通知列左/右固定状态变化。 | 回调/事件；不会自动持久化 |
| [`onColumnResize`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L540) | `(columnId: PropertyKeys<Q> \| keyof RDPs \| keyof FunctionColumns, newWidth: number \| null) => void` | 可选 | undefined / 未声明 | 通知某列的新宽度。 | 回调/事件；不会自动持久化 |
| [`onColumnHeaderClick`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L554) | `(columnId: PropertyKeys<Q> \| keyof RDPs \| keyof FunctionColumns) => void` | 可选 | undefined / 未声明 | 读取点击的列 ID；点击本身不自动切换排序。 | 回调/事件；不会自动持久化 |
| [`enableOrdering`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L563) | `boolean` | 可选 | true | 启用排序入口。 | 数据/呈现/能力配置 |
| [`defaultOrderBy`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L570) | `Array<{ property: PropertyKeys<Q> \| keyof RDPs; direction: "asc" \| "desc"; }>` | 可选 | undefined / 未声明 | 设置排序初始种子。 | 初始种子；具体例外见说明 |
| [`orderBy`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L580) | `Array<{ property: PropertyKeys<Q> \| keyof RDPs; direction: "asc" \| "desc"; }>` | 可选 | undefined / 未声明 | 外部提供当前排序值。 | 外部状态输入；具体所有权见本节说明 |
| [`onOrderByChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L591) | `(newOrderBy: Array<{ property: PropertyKeys<Q> \| keyof RDPs; direction: "asc" \| "desc"; }>) => void` | 可选 | undefined / 未声明 | 通知排序变化；受控宿主需回写。 | 回调/事件；不会自动持久化 |
| [`selectionMode`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L606) | `"single" \| "multiple" \| "none"` | 可选 | "none" | 选择 none/single/multiple 行选择模式。 | 数据/呈现/能力配置 |
| [`selectedRows`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L612) | `PrimaryKeyType<Q>[]` | 可选 | undefined / 未声明 | 外部提供被选主键集合。 | 外部状态输入；具体所有权见本节说明 |
| [`isAllSelected`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L618) | `boolean` | 可选 | undefined / 未声明 | 指示全结果集已选中。 | 数据/呈现/能力配置 |
| [`onRowSelectionChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L626) | `(change: RowSelectionChange<Q, RDPs>) => void` | 可选 | undefined / 未声明 | 输出已加载实例、选择对象集和全选信息。 | 回调/事件；不会自动持久化 |
| [`onLoadedObjectsChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L636) | `(change: LoadedObjectsChange<Q, RDPs>) => void` | 可选 | undefined / 未声明 | 输出当前累计加载的对象实例。 | 回调/事件；不会自动持久化 |
| [`focusedRow`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L648) | `PrimaryKeyType<Q> \| null` | 可选 | undefined / 未声明 | 外部提供视觉聚焦对象主键。 | 外部状态输入；具体所有权见本节说明 |
| [`onFocusedRowChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L658) | `(row: Osdk.Instance<Q, "$allBaseProperties", PropertyKeys<Q>, RDPs> \| null) => void` | 可选 | undefined / 未声明 | 通知视觉聚焦行变化；不是单元格键盘焦点。 | 回调/事件；不会自动持久化 |
| [`editMode`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L669) | `"always" \| "manual"` | 可选 | "manual" | 配置手动进入或始终开启编辑。 | 数据/呈现/能力配置 |
| [`showEditFooter`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L680) | `boolean` | 可选 | 有 editable 列时显示；传 false 可关闭 | 控制编辑/提交操作区的显示。 | 数据/呈现/能力配置 |
| [`onCellValueChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L688) | `(info: CellEditInfo<Osdk.Instance<Q, "$allBaseProperties", PropertyKeys<Q>, RDPs>, unknown>) => void` | 可选 | undefined / 未声明 | 输出单个本地编辑草稿；宿主决定后续同步。 | 回调/事件；不会自动持久化 |
| [`onSubmitEdits`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L702) | `(edits: CellEditInfo<Osdk.Instance<Q, "$allBaseProperties", PropertyKeys<Q>, RDPs>, unknown>[]) => Promise<boolean>` | 可选 | undefined / 未声明 | 输出草稿集合供宿主提交；组件不自动调用 Action。 | 回调/事件；不会自动持久化 |
| [`onRowClick`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L714) | `(object: Osdk.Instance<Q, "$allBaseProperties", PropertyKeys<Q>, RDPs>) => void` | 可选 | undefined / 未声明 | 读取点击的行对象。 | 回调/事件；不会自动持久化 |
| [`renderCellContextMenu`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L721) | `(row: Osdk.Instance<Q, "$allBaseProperties", PropertyKeys<Q>, RDPs>, cellValue: unknown) => React.ReactNode` | 可选 | undefined / 未声明 | 为单元格右键菜单提供内容。 | 宿主提供函数 |
| [`rowHeight`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L731) | `number` | 可选 | 40 | 固定估计行高，单位 px；供虚拟化使用。 | 数据/呈现/能力配置 |
| [`renderEmptyState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L738) | `() => React.ReactNode` | 可选 | undefined / 未声明 | 自定义没有内容时的呈现。 | 宿主提供函数 |
| [`getRowAttributes`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L744) | `(object: Osdk.Instance<Q, "$allBaseProperties", PropertyKeys<Q>, RDPs>) => Record<string, string \| undefined>` | 可选 | undefined / 未声明 | 为每一行提供 HTML 属性。 | 宿主提供函数 |
| [`tableRef`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L754) | `React.Ref<ObjectTableHandle<Q, RDPs>>` | 可选 | undefined / 未声明 | 取得 getSnapshot 等命令式表格 API。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L756) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |

### BaseTable / `BaseTableProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx)；实际发布声明：`build/types/object-table/Table.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

泛型 TData extends RowData；消费 TanStack Table<TData>，查询、排序、行选择和编辑元数据主要由宿主 Table 实例提供。它不是 AntD Table 或 react-data-grid 的 columns API。

泛型：`TData extends RowData`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`table`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L84) | `Table<TData>` | 必填 | 无；必须提供 | 宿主构造的 TanStack Table 实例。 | 数据/呈现/能力配置 |
| [`isLoading`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L92) | `boolean` | 可选 | undefined / 未声明 | 提供加载状态。 | 数据/呈现/能力配置 |
| [`fetchNextPage`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L98) | `() => Promise<void>` | 可选 | undefined / 未声明 | 滚动接近底部时加载下一批；省略以关闭。 | 数据/呈现/能力配置 |
| [`onRowClick`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L105) | `(row: TData) => void` | 可选 | undefined / 未声明 | 读取点击的行对象。 | 回调/事件；不会自动持久化 |
| [`onColumnHeaderClick`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L115) | `(columnId: string) => void` | 可选 | undefined / 未声明 | 读取点击的列 ID；点击本身不自动切换排序。 | 回调/事件；不会自动持久化 |
| [`rowHeight`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L123) | `number` | 可选 | 40 | 固定估计行高，单位 px；供虚拟化使用。 | 数据/呈现/能力配置 |
| [`renderCellContextMenu`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L128) | `(row: TData, cell: Cell<TData, unknown>) => React.ReactNode` | 可选 | undefined / 未声明 | 为单元格右键菜单提供内容。 | 宿主提供函数 |
| [`headerMenuFeatureFlags`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L138) | `HeaderMenuFeatureFlags` | 可选 | undefined / 未声明 | 控制各表头菜单项。 | 数据/呈现/能力配置 |
| [`editableConfig`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L145) | `EditableConfig<TData, unknown>` | 可选 | undefined / 未声明 | 注入编辑状态与提交操作；Base 不持有 OSDK Action。 | 数据/呈现/能力配置 |
| [`showEditFooter`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L152) | `boolean` | 可选 | true | 控制编辑/提交操作区的显示。 | 数据/呈现/能力配置 |
| [`focusedRowId`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L157) | `string \| null` | 可选 | undefined / 未声明 | 外部提供视觉聚焦行 ID。 | 外部状态输入；具体所有权见本节说明 |
| [`onFocusedRowChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L163) | `(row: TData \| null) => void` | 可选 | undefined / 未声明 | 通知视觉聚焦行变化；不是单元格键盘焦点。 | 回调/事件；不会自动持久化 |
| [`renderEmptyState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L170) | `() => React.ReactNode` | 可选 | undefined / 未声明 | 自定义没有内容时的呈现。 | 宿主提供函数 |
| [`error`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L176) | `Error` | 可选 | undefined / 未声明 | 外部提供错误；部分接口要求显式传 undefined。 | 数据/呈现/能力配置 |
| [`getRowAttributes`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L182) | `(object: TData) => Record<string, string \| undefined>` | 可选 | undefined / 未声明 | 为每一行提供 HTML 属性。 | 宿主提供函数 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L187) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |

### ObjectTable 查询配置 / `ObjectSetOptions`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts)；实际发布声明：`build/types/object-table/ObjectTableApi.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此配置作为所属主组件的输入；类型详情由固定声明定义。

泛型：`Q extends ObjectOrInterfaceDefinition`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`union`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L933) | `ObjectSet<Q>[]` | 可选 | undefined / 未声明 | 合并输入对象集。 | 数据/呈现/能力配置 |
| [`intersect`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L938) | `ObjectSet<Q>[]` | 可选 | undefined / 未声明 | 取对象集交集。 | 数据/呈现/能力配置 |
| [`subtract`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L943) | `ObjectSet<Q>[]` | 可选 | undefined / 未声明 | 从基础对象集排除指定对象集。 | 数据/呈现/能力配置 |

### ObjectTable 列配置 / `ColumnDefinition`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts)；实际发布声明：`build/types/object-table/ObjectTableApi.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此表合并列举四个列定义分支；locator/editable/cellValueType 展示为合并范围，其余显示首先声明它的分支类型。它不能还原判别联合约束。locator 包含 property / rdp / custom / function；getCellValue 只允许 derivable 分支且同时要求 cellValueType。Function 使用 locator.getValue。类型允许的 editable function 列并不保证当前运行时可编辑。getCellValue 与 cellValueType 的映射 T → PropertyValueWireToClient[T] 保留关联，不能将表格的宽类型当作可自由组合。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useColumnDefs.tsx)。

泛型：`Q extends ObjectOrInterfaceDefinition`；`RDPs extends Record<string, SimplePropertyDef> = {}`；`FunctionColumns extends Record<string, QueryDefinition<{}>> = Record<string, never>`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`isVisible`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L156) | `boolean` | 可选 | true | 控制是否呈现此列/筛选项。 | 数据/呈现/能力配置 |
| [`pinned`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L161) | `"left" \| "right" \| "none"` | 可选 | none | 配置左固定、右固定或不固定。 | 数据/呈现/能力配置 |
| [`width`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L162) | `number` | 可选 | undefined / 未声明 | 配置宽度。 | 数据/呈现/能力配置 |
| [`minWidth`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L163) | `number` | 可选 | undefined / 未声明 | 限制最小宽度。 | 数据/呈现/能力配置 |
| [`maxWidth`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L164) | `number` | 可选 | undefined / 未声明 | 限制最大宽度。 | 数据/呈现/能力配置 |
| [`resizable`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L165) | `boolean` | 可选 | undefined / 未声明 | 控制该列能否调整宽度。 | 数据/呈现/能力配置 |
| [`orderable`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L166) | `boolean` | 可选 | undefined / 未声明 | 控制该列能否参与排序。 | 数据/呈现/能力配置 |
| [`renderCell`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L184) | `(object: Osdk.Instance<Q, "$allBaseProperties", PropertyKeys<Q>, RDPs>, locator: ColumnDefinitionLocator<Q, RDPs, FunctionColumns>, value: unknown) => React.ReactNode` | 可选 | undefined / 未声明 | 自定义只读显示；不改变数据值。 | 宿主提供函数 |
| [`columnName`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L199) | `string` | 可选 | undefined / 未声明 | 配置列名称；默认属性 displayName 或 locator ID。 | 数据/呈现/能力配置 |
| [`renderHeader`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L205) | `() => React.ReactNode` | 可选 | undefined / 未声明 | 自定义表头，优先于 columnName。 | 宿主提供函数 |
| [`editable`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L216) | `boolean \| ((object: Osdk.Instance<Q, "$allBaseProperties", PropertyKeys<Q>, RDPs>) => boolean)` | 可选 | undefined / 未声明 | 允许编辑，或逐行判定可编辑性。 | 数据/呈现/能力配置 |
| [`editFieldConfig`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L233) | `EditFieldConfig<Osdk.Instance<Q, "$allBaseProperties", PropertyKeys<Q>, RDPs>>` | 可选 | undefined / 未声明 | 配置编辑器，支持按行对象和草稿动态生成 props。 | 数据/呈现/能力配置 |
| [`validateEdit`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L243) | `(value: unknown) => Promise<string \| undefined>` | 可选 | undefined / 未声明 | 异步返回错误文字；undefined 表示通过。 | 宿主提供函数 |
| [`locator`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L64) | `PropertyColumnLocator<Q> \| RdpColumnLocator<Q,RDPs> \| CustomColumnLocator \| FunctionColumnLocator<Q,RDPs,FunctionColumns>` | 必填 | 无；必须提供 | 指定列来源。完整判别联合须同时核对类型定义。 | 数据/呈现/能力配置 |
| [`cellValueType`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L94) | `BaseWirePropertyTypes（映射关联见完整联合）` | 可选 | undefined / 未声明 | 声明 wire 数据类型；约束派生值并影响编辑器。 | 数据/呈现/能力配置 |
| [`getCellValue`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L105) | `(object: Osdk.Instance<Q, "$allBaseProperties", PropertyKeys<Q>, RDPs>, locator: ColumnDefinitionLocator<Q, RDPs, FunctionColumns>) => PropertyValueWireToClient[BaseWirePropertyTypes] \| null \| undefined` | 可选 | undefined / 未声明 | 从对象计算真正的数据值；须同时声明 cellValueType。 | 宿主提供函数 |

### 下拉编辑配置 / `DropdownEditConfig`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts)；实际发布声明：`build/types/object-table/utils/types.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此配置作为所属主组件的输入；类型详情由固定声明定义。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/components/DropdownCellField.tsx)。

泛型：`V = unknown`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`items`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L77) | `V[]` | 必填 | 无；必须提供 | 下拉可选值集合。 | 数据/呈现/能力配置 |
| [`itemToStringLabel`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L85) | `(item: V \| undefined) => string` | 可选 | String() | 将选项转为显示文字；需处理 undefined。 | 数据/呈现/能力配置 |
| [`itemToKey`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L91) | `(item: V) => string` | 可选 | undefined / 未声明 | 生成稳定选项 key；缺省用索引。 | 数据/呈现/能力配置 |
| [`isItemEqual`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L97) | `(a: V, b: V) => boolean` | 可选 | Object.is | 判断两个选项是否相等；对象值通常应配置。 | 数据/呈现/能力配置 |
| [`isSearchable`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L104) | `boolean` | 可选 | false | 是否提供选项搜索。 | 数据/呈现/能力配置 |
| [`placeholder`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L109) | `string` | 可选 | undefined / 未声明 | 配置空值占位文字。 | 数据/呈现/能力配置 |
| [`isMultiple`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L114) | `boolean` | 可选 | false | 是否允许选择多个值。 | 数据/呈现/能力配置 |

### 日期编辑配置 / `DatePickerEditConfig`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts)；实际发布声明：`build/types/object-table/utils/types.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此配置作为所属主组件的输入；类型详情由固定声明定义。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/components/DatePickerCellField.tsx)。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`min`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L127) | `Date` | 可选 | undefined / 未声明 | 最早允许日期。 | 数据/呈现/能力配置 |
| [`max`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L132) | `Date` | 可选 | undefined / 未声明 | 最晚允许日期。 | 数据/呈现/能力配置 |
| [`showTime`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L137) | `boolean` | 可选 | 表格中默认 dataType==="timestamp"；可覆盖 | 是否同时选择时间。 | 数据/呈现/能力配置 |
| [`closeOnSelection`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L143) | `boolean` | 可选 | !showTime | 选择日期后是否收起弹层。 | 数据/呈现/能力配置 |
| [`placeholder`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L148) | `string` | 可选 | undefined / 未声明 | 配置空值占位文字。 | 数据/呈现/能力配置 |
| [`formatDate`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L154) | `(date: Date) => string` | 可选 | undefined / 未声明 | 将 Date 格式化为输入显示文字。 | 数据/呈现/能力配置 |
| [`parseDate`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/utils/types.ts#L160) | `(text: string) => Date \| undefined` | 可选 | undefined / 未声明 | 解析输入为 Date；须匹配 formatDate。 | 数据/呈现/能力配置 |

### ColumnConfigDialog / `ColumnConfigDialogProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ColumnConfigDialog.tsx)；实际发布声明：`build/types/object-table/ColumnConfigDialog.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此配置作为所属主组件的输入；类型详情由固定声明定义。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`isOpen`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ColumnConfigDialog.tsx#L41) | `boolean` | 必填 | 无；必须提供 | 外部控制对话框是否打开。 | 外部状态输入；具体所有权见本节说明 |
| [`onClose`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ColumnConfigDialog.tsx#L42) | `() => void` | 必填 | 无；必须提供 | 请求宿主关闭对话框。 | 回调/事件；不会自动持久化 |
| [`columnOptions`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ColumnConfigDialog.tsx#L43) | `ColumnConfigOptions` | 必填 | 无；必须提供 | 可配置列的候选集合。 | 数据/呈现/能力配置 |
| [`currentVisibility`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ColumnConfigDialog.tsx#L44) | `VisibilityState` | 可选 | undefined / 未声明 | 当前列可见性快照。 | 数据/呈现/能力配置 |
| [`currentColumnOrder`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ColumnConfigDialog.tsx#L45) | `ColumnOrderState` | 可选 | undefined / 未声明 | 当前列顺序快照。 | 数据/呈现/能力配置 |
| [`onApply`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ColumnConfigDialog.tsx#L46) | `(columns: ColumnConfig[]) => void` | 必填 | 无；必须提供 | 读取应用后的配置；宿主回写。 | 回调/事件；不会自动持久化 |
| [`isValidConfig`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ColumnConfigDialog.tsx#L47) | `(columns: ColumnConfig[]) => boolean` | 可选 | undefined / 未声明 | 宿主判断列配置是否合法。 | 数据/呈现/能力配置 |

### MultiColumnSortDialog / `MultiColumnSortDialogProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/MultiColumnSortDialog.tsx)；实际发布声明：`build/types/object-table/MultiColumnSortDialog.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此配置作为所属主组件的输入；类型详情由固定声明定义。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`isOpen`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/MultiColumnSortDialog.tsx#L38) | `boolean` | 必填 | 无；必须提供 | 外部控制对话框是否打开。 | 外部状态输入；具体所有权见本节说明 |
| [`onClose`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/MultiColumnSortDialog.tsx#L39) | `() => void` | 必填 | 无；必须提供 | 请求宿主关闭对话框。 | 回调/事件；不会自动持久化 |
| [`onApply`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/MultiColumnSortDialog.tsx#L40) | `(sortColumns: SortingState) => void` | 必填 | 无；必须提供 | 读取应用后的配置；宿主回写。 | 回调/事件；不会自动持久化 |
| [`currentSorting`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/MultiColumnSortDialog.tsx#L41) | `SortingState` | 必填 | 无；必须提供 | 当前 TanStack SortingState 快照。 | 数据/呈现/能力配置 |
| [`columnOptions`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/MultiColumnSortDialog.tsx#L42) | `ColumnOption[]` | 必填 | 无；必须提供 | 可配置列的候选集合。 | 数据/呈现/能力配置 |

### FilterList / `FilterListProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts)；实际发布声明：`build/types/filter-list/FilterListApi.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

Q extends ObjectTypeDefinition。筛选值由内部状态持有，defaultFilterStates 为初始/Reset 快照；没有整体受控值 prop。定义上的 filterState/旧名存在但已弃用，请核对迁移。addFilterMode 仅控制可见性且已弃用。HAS_LINK/LINKED_PROPERTY 必须提供 objectSet，并通过 onEffectiveObjectSet 接收结果；onFilterClauseChanged 不包含这些关联筛选。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterList.tsx)。

泛型：`Q extends ObjectTypeDefinition`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`objectType`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L107) | `Q` | 必填 | 无；必须提供 | 对象类型定义；用于元数据和查询。 | 数据/呈现/能力配置 |
| [`objectSet`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L115) | `ObjectSet<Q>` | 可选 | undefined / 未声明 | 限定输入对象集；省略时通常查询整个类型。 | 数据/呈现/能力配置 |
| [`filterDefinitions`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L121) | `Array<FilterDefinitionUnion<Q>>` | 可选 | undefined / 未声明 | 显式筛选项配置；当前实现省略后是空列表。 | 数据/呈现/能力配置 |
| [`defaultFilterStates`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L132) | `Map<string, FilterState>` | 可选 | 各 definition 初始值；无外部 Map | 筛选值初始快照；也是 Reset 的恢复目标。 | 初始种子；具体例外见说明 |
| [`initialFilterStates`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L137) | `Map<string, FilterState>` | 可选 | undefined / 未声明 | defaultFilterStates 的弃用旧名。 | 弃用；初始种子 |
| [`onFilterListChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L145) | `(event: FilterChangeEvent<Q>) => void` | 可选 | undefined / 未声明 | 输出组合筛选事件与结果快照。 | 回调/事件；不会自动持久化 |
| [`onFilterClauseChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L158) | `(newClause: WhereClause<Q>) => void` | 可选 | undefined / 未声明 | 输出直接属性筛选 WhereClause；不含关联筛选。 | 回调/事件；不会自动持久化 |
| [`onFilterStateChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L168) | `(definition: FilterDefinitionUnion<Q>, newState: FilterState) => void` | 可选 | undefined / 未声明 | 输出某筛选项新状态；Base/FilterInput 由宿主回写。 | 回调/事件；不会自动持久化 |
| [`onEffectiveObjectSet`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L181) | `(objectSet: ObjectSet<Q>) => void` | 可选 | undefined / 未声明 | 输出包含关联筛选的最终对象集；需要 objectSet。 | 回调/事件；不会自动持久化 |
| [`addFilterMode`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L198) | `"controlled" \| "uncontrolled"` | 可选 | "uncontrolled" | 控制新增/移除筛选项可见性的模式；不控制筛选值。 | 弃用配置 |
| [`renderAddFilterButton`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L205) | `() => React.ReactNode` | 可选 | undefined / 未声明 | 自定义新增筛选的触发按钮。 | 宿主提供函数 |
| [`onFilterAdded`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L214) | `(filterKey: string, newDefinitions: Array<FilterDefinitionUnion<Q>>) => void` | 可选 | undefined / 未声明 | 通知新增可见筛选项。 | 回调/事件；不会自动持久化 |
| [`onFilterRemoved`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L227) | `(filterKey: string) => void` | 可选 | undefined / 未声明 | 通知移除筛选项；wrapper 同时清理状态。 | 回调/事件；不会自动持久化 |
| [`enableSorting`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L238) | `boolean` | 可选 | false | 启用筛选项拖拽排序。 | 数据/呈现/能力配置 |
| [`onFilterVisibilityChange`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L251) | `(newStates: Array<{ filterKey: string; isVisible: boolean; }>) => void` | 可选 | undefined / 未声明 | 输出可见性及当前排列顺序。 | 回调/事件；不会自动持久化 |
| [`enableCollapse`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L264) | `boolean` | 可选 | true | 是否允许收起面板；false 时忽略折叠值。 | 数据/呈现/能力配置 |
| [`collapsed`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L274) | `boolean` | 可选 | undefined / 未声明 | 外部控制折叠状态。 | 外部状态输入；具体所有权见本节说明 |
| [`defaultCollapsed`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L285) | `boolean` | 可选 | false | 非受控折叠状态初始种子。 | 初始种子；具体例外见说明 |
| [`onCollapsedChange`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L292) | `(collapsed: boolean) => void` | 可选 | undefined / 未声明 | 通知折叠变化；受控宿主需回写。 | 回调/事件；不会自动持久化 |
| [`showResetButton`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L297) | `boolean` | 可选 | false | 显示 Reset 按钮。 | 数据/呈现/能力配置 |
| [`onReset`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L302) | `() => void` | 可选 | undefined / 未声明 | 读取 Reset 点击。 | 回调/事件；不会自动持久化 |
| [`title`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L307) | `ReactNode` | 可选 | undefined / 未声明 | 配置标题。 | 数据/呈现/能力配置 |
| [`titleIcon`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L312) | `React.ReactNode` | 可选 | undefined / 未声明 | 配置标题图标。 | 数据/呈现/能力配置 |
| [`showActiveFilterCount`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L317) | `boolean` | 可选 | false | 显示有效筛选项数量。 | 数据/呈现/能力配置 |
| [`showFilteredOutValues`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L324) | `boolean` | 可选 | false | 保留其他筛选排除的值并显示 count=0。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListApi.ts#L329) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |

### BaseFilterList / `BaseFilterListProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts)；实际发布声明：`build/types/filter-list/base/BaseFilterListApi.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

泛型 D extends FilterDefinitionControls。filterStates + onFilterStateChanged 是完全外部状态输入/回写协议，输入控件由 renderInput 提供。折叠可以通过 collapsed/onCollapsedChange 控制；enableCollapse=false 时忽略。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterList.tsx)。

泛型：`D extends FilterDefinitionControls`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`filterDefinitions`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L34) | `Array<D>` | 可选 | undefined / 未声明 | 显式筛选项配置；当前实现省略后是空列表。 | 数据/呈现/能力配置 |
| [`filterStates`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L35) | `Map<string, FilterState>` | 必填 | 无；必须提供 | 外部持有筛选状态 Map。 | 外部状态输入；具体所有权见本节说明 |
| [`onFilterStateChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L36) | `(filterKey: string, state: FilterState) => void` | 必填 | 无；必须提供 | 输出某筛选项新状态；Base/FilterInput 由宿主回写。 | 回调/事件；不会自动持久化 |
| [`renderInput`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L37) | `RenderFilterInput<D>` | 必填 | 无；必须提供 | 自定义筛选输入渲染。 | 宿主提供函数 |
| [`getFilterKey`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L38) | `(definition: D) => string` | 必填 | 无；必须提供 | 生成筛选项稳定 key。 | 宿主提供函数 |
| [`getFilterLabel`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L39) | `(definition: D) => string` | 必填 | 无；必须提供 | 生成筛选项显示名称。 | 宿主提供函数 |
| [`getEmptyDisplayState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L45) | `(definition: D) => FilterState \| undefined` | 可选 | undefined / 未声明 | 只用于无状态项的呈现回退，不写入状态 Map。 | 宿主提供函数 |
| [`activeFilterCount`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L46) | `number` | 必填 | 无；必须提供 | 宿主计算的有效筛选项数量。 | 数据/呈现/能力配置 |
| [`onReset`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L47) | `() => void` | 可选 | undefined / 未声明 | 读取 Reset 点击。 | 回调/事件；不会自动持久化 |
| [`onFilterAdded`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L48) | `() => void` | 可选 | undefined / 未声明 | 通知新增可见筛选项。 | 回调/事件；不会自动持久化 |
| [`onFilterRemoved`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L49) | `(filterKey: string) => void` | 可选 | undefined / 未声明 | 通知移除筛选项；wrapper 同时清理状态。 | 回调/事件；不会自动持久化 |
| [`onOrderChange`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L50) | `(orderedKeys: string[]) => void` | 可选 | undefined / 未声明 | 输出筛选项排列 key 顺序。 | 回调/事件；不会自动持久化 |
| [`enableCollapse`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L58) | `boolean` | 可选 | true | 是否允许收起面板；false 时忽略折叠值。 | 数据/呈现/能力配置 |
| [`collapsed`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L68) | `boolean` | 可选 | undefined / 未声明 | 外部控制折叠状态。 | 外部状态输入；具体所有权见本节说明 |
| [`defaultCollapsed`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L79) | `boolean` | 可选 | false | 非受控折叠状态初始种子。 | 初始种子；具体例外见说明 |
| [`onCollapsedChange`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L86) | `(collapsed: boolean) => void` | 可选 | undefined / 未声明 | 通知折叠变化；受控宿主需回写。 | 回调/事件；不会自动持久化 |
| [`title`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L87) | `React.ReactNode` | 可选 | undefined / 未声明 | 配置标题。 | 数据/呈现/能力配置 |
| [`titleIcon`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L88) | `React.ReactNode` | 可选 | undefined / 未声明 | 配置标题图标。 | 数据/呈现/能力配置 |
| [`showResetButton`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L89) | `boolean` | 可选 | false | 显示 Reset 按钮。 | 数据/呈现/能力配置 |
| [`showActiveFilterCount`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L90) | `boolean` | 可选 | false | 显示有效筛选项数量。 | 数据/呈现/能力配置 |
| [`canReset`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L95) | `boolean` | 可选 | undefined / 未声明 | 宿主判定 Reset 是否可用。 | 数据/呈现/能力配置 |
| [`enableSorting`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L96) | `boolean` | 可选 | 关闭（undefined） | 启用筛选项拖拽排序。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L97) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |
| [`renderAddFilterButton`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/BaseFilterListApi.ts#L98) | `() => React.ReactNode` | 可选 | undefined / 未声明 | 自定义新增筛选的触发按钮。 | 宿主提供函数 |

### FilterInput / `FilterInputProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx)；实际发布声明：`build/types/filter-list/FilterInput.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

Q extends ObjectTypeDefinition。消费单项外部 FilterState，宿主传排除自身后的 WhereClause / linkedFilters；此组件不代替整个列表状态管理。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx)。

泛型：`Q extends ObjectTypeDefinition`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`objectType`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L42) | `Q` | 必填 | 无；必须提供 | 对象类型定义；用于元数据和查询。 | 数据/呈现/能力配置 |
| [`objectSet`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L43) | `ObjectSet<Q>` | 可选 | undefined / 未声明 | 限定输入对象集；省略时通常查询整个类型。 | 数据/呈现/能力配置 |
| [`definition`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L44) | `FilterDefinitionUnion<Q>` | 必填 | 无；必须提供 | 筛选项定义。 | 数据/呈现/能力配置 |
| [`filterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L45) | `FilterState \| undefined` | 必填 | 无；必须提供 | 该筛选项当前状态；允许显式 undefined。 | 数据/呈现/能力配置 |
| [`onFilterStateChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L46) | `(state: FilterState) => void` | 必填 | 无；必须提供 | 输出某筛选项新状态；Base/FilterInput 由宿主回写。 | 回调/事件；不会自动持久化 |
| [`whereClause`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L48) | `WhereClause<Q>` | 必填 | 无；必须提供 | 当前筛选项排除自身后得到的直接筛选条件。 | 数据/呈现/能力配置 |
| [`linkedFilters`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L50) | `ReadonlyArray<LinkedFilter<Q>>` | 可选 | undefined / 未声明 | 排除自身后的关联筛选记录。 | 数据/呈现/能力配置 |
| [`showFilteredOutValues`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L51) | `boolean` | 可选 | undefined / 未声明 | 保留其他筛选排除的值并显示 count=0。 | 数据/呈现/能力配置 |
| [`searchQuery`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L52) | `string` | 可选 | undefined / 未声明 | 筛选候选值的搜索文本。 | 数据/呈现/能力配置 |
| [`excludeRowOpen`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L53) | `boolean` | 可选 | undefined / 未声明 | 控制排除值区域的显示。 | 数据/呈现/能力配置 |
| [`layout`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterInput.tsx#L61) | `MultiSelectInputLayout` | 可选 | "dropdown" | MULTI_SELECT 的 dropdown/inline 布局。 | 数据/呈现/能力配置 |

### FilterPopover / `FilterPopoverProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterPopover.tsx)；实际发布声明：`build/types/filter-list/base/FilterPopover.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此配置作为所属主组件的输入；类型详情由固定声明定义。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterPopover.tsx)。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`label`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterPopover.tsx#L26) | `string` | 必填 | 无；必须提供 | 配置展示名称。 | 数据/呈现/能力配置 |
| [`summary`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterPopover.tsx#L28) | `string` | 必填 | 无；必须提供 | 当前值摘要；空时使用 placeholder。 | 数据/呈现/能力配置 |
| [`isActive`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterPopover.tsx#L29) | `boolean` | 必填 | 无；必须提供 | 标示当前筛选已激活。 | 数据/呈现/能力配置 |
| [`onRemove`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterPopover.tsx#L30) | `() => void` | 可选 | undefined / 未声明 | 读取移除点击。 | 回调/事件；不会自动持久化 |
| [`children`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterPopover.tsx#L32) | `React.ReactNode` | 必填 | 无；必须提供 | 嵌套内容。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterPopover.tsx#L33) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |
| [`placeholder`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterPopover.tsx#L34) | `string` | 可选 | "Any" | 配置空值占位文字。 | 数据/呈现/能力配置 |
| [`labelPlacement`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/base/FilterPopover.tsx#L40) | `"inline" \| "top"` | 可选 | "inline" | 标签与触发器同排或标签位于上方。 | 数据/呈现/能力配置 |

### 属性筛选定义 / `PropertyFilterDefinition`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts)；实际发布声明：`build/types/filter-list/FilterListItemApi.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

泛型 Q,K 把属性 key 和可用 filterComponent 联系起来。FilterDefinitionControls.searchField/id/isVisible 是所有定义共享字段。defaultFilterState 为初始种子；filterState 为弃用旧字段。

泛型：`Q extends ObjectTypeDefinition`；`K extends PropertyKeys<Q> = PropertyKeys<Q>`；`C extends ValidComponentsForPropertyType<PropertyTypeFromKey<Q, K>> = ValidComponentsForPropertyType<PropertyTypeFromKey<Q, K>>`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`searchField`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L51) | `boolean` | 可选 | true | 显示候选值搜索入口。 | 数据/呈现/能力配置 |
| [`id`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L63) | `string` | 可选 | 由属性/关联定义推导 | 稳定筛选 ID；重复属性配置时应显式提供。 | 数据/呈现/能力配置 |
| [`isVisible`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L70) | `boolean` | 可选 | true | 控制是否呈现此列/筛选项。 | 数据/呈现/能力配置 |
| [`type`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L328) | `"PROPERTY"` | 必填 | 无；必须提供 | 筛选定义的判别标记。 | 数据/呈现/能力配置 |
| [`key`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L333) | `K` | 必填 | 无；必须提供 | 属性 key 或自定义筛选 key。 | 数据/呈现/能力配置 |
| [`label`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L338) | `string` | 可选 | undefined / 未声明 | 配置展示名称。 | 数据/呈现/能力配置 |
| [`filterComponent`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L344) | `C` | 必填 | 无；必须提供 | 配置输入控件类别；类型与属性数据类型关联。 | 数据/呈现/能力配置 |
| [`defaultFilterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L351) | `FilterStateByComponentType[C]` | 可选 | undefined，初始无值 | 该项初始值种子。 | 初始种子；具体例外见说明 |
| [`filterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L356) | `FilterStateByComponentType[C]` | 可选 | undefined / 未声明 | 该筛选项当前状态；允许显式 undefined。 | 弃用配置 |
| [`colorMap`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L362) | `Record<string, string>` | 可选 | undefined / 未声明 | 按候选值配置颜色。 | 数据/呈现/能力配置 |
| [`listogramConfig`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L368) | `{ displayMode?: "full" \| "count" \| "minimal"; maxVisibleItems?: number; }` | 可选 | undefined / 未声明 | 配置条形计数呈现。 | 数据/呈现/能力配置 |
| [`renderValue`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L384) | `(value: string) => ReactNode` | 可选 | undefined / 未声明 | 自定义候选值的呈现。 | 宿主提供函数 |
| [`showCount`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L391) | `boolean` | 可选 | LISTOGRAM/MULTI_SELECT=true；SINGLE_SELECT=false | 控制候选值计数显示。 | 数据/呈现/能力配置 |
| [`clickToFilter`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L405) | `boolean` | 可选 | false | 是否点击条形直接筛选。 | 数据/呈现/能力配置 |

### 关键字筛选定义 / `KeywordSearchFilterDefinition`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/KeywordSearchTypes.ts)；实际发布声明：`build/types/filter-list/types/KeywordSearchTypes.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此配置作为所属主组件的输入；类型详情由固定声明定义。

泛型：`Q extends ObjectTypeDefinition`；`K extends StringPropertyKeys<Q> = StringPropertyKeys<Q>`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`searchField`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L51) | `boolean` | 可选 | true | 显示候选值搜索入口。 | 数据/呈现/能力配置 |
| [`id`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L63) | `string` | 可选 | 由属性/关联定义推导 | 稳定筛选 ID；重复属性配置时应显式提供。 | 数据/呈现/能力配置 |
| [`isVisible`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L70) | `boolean` | 可选 | true | 控制是否呈现此列/筛选项。 | 数据/呈现/能力配置 |
| [`type`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/KeywordSearchTypes.ts#L51) | `"KEYWORD_SEARCH"` | 必填 | 无；必须提供 | 筛选定义的判别标记。 | 数据/呈现/能力配置 |
| [`properties`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/KeywordSearchTypes.ts#L57) | `"all" \| K[]` | 必填 | 无；必须提供 | 关键字搜索字段集合，或 all 字符串属性。 | 数据/呈现/能力配置 |
| [`label`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/KeywordSearchTypes.ts#L58) | `string` | 可选 | undefined / 未声明 | 配置展示名称。 | 数据/呈现/能力配置 |
| [`defaultFilterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/KeywordSearchTypes.ts#L64) | `KeywordSearchFilterState` | 可选 | undefined，初始无值 | 该项初始值种子。 | 初始种子；具体例外见说明 |
| [`filterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/KeywordSearchTypes.ts#L69) | `KeywordSearchFilterState` | 可选 | undefined / 未声明 | 该筛选项当前状态；允许显式 undefined。 | 弃用配置 |

### 关联存在性筛选定义 / `HasLinkFilterDefinition`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts)；实际发布声明：`build/types/filter-list/types/LinkedFilterTypes.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此配置作为所属主组件的输入；类型详情由固定声明定义。

泛型：`Q extends ObjectTypeDefinition`；`L extends LinkNames<Q> = LinkNames<Q>`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`searchField`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L51) | `boolean` | 可选 | true | 显示候选值搜索入口。 | 数据/呈现/能力配置 |
| [`id`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L63) | `string` | 可选 | 由属性/关联定义推导 | 稳定筛选 ID；重复属性配置时应显式提供。 | 数据/呈现/能力配置 |
| [`isVisible`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L70) | `boolean` | 可选 | true | 控制是否呈现此列/筛选项。 | 数据/呈现/能力配置 |
| [`type`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L88) | `"HAS_LINK"` | 必填 | 无；必须提供 | 筛选定义的判别标记。 | 数据/呈现/能力配置 |
| [`linkName`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L89) | `L` | 必填 | 无；必须提供 | 来源对象的 link 名称。 | 数据/呈现/能力配置 |
| [`label`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L90) | `string` | 可选 | undefined / 未声明 | 配置展示名称。 | 数据/呈现/能力配置 |
| [`defaultFilterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L97) | `HasLinkFilterState` | 可选 | undefined，初始无值 | 该项初始值种子。 | 初始种子；具体例外见说明 |
| [`filterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L102) | `HasLinkFilterState` | 可选 | undefined / 未声明 | 该筛选项当前状态；允许显式 undefined。 | 弃用配置 |

### 关联属性筛选定义 / `LinkedPropertyFilterDefinition`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts)；实际发布声明：`build/types/filter-list/types/LinkedFilterTypes.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

filterComponent/defaultFilterState 为当前名称；linkedFilterComponent/defaultLinkedFilterState/linkedFilterState 为兼容旧名。关联目标的属性类型和反向 link 配置仍需遵循联合类型。

泛型：`Q extends ObjectTypeDefinition`；`L extends LinkNames<Q>`；`LinkedQ extends ObjectTypeDefinition = LinkedType<Q, L>`；`LinkedK extends PropertyKeys<LinkedQ> = PropertyKeys<LinkedQ>`；`LinkedC extends ValidComponentsForPropertyType<PropertyTypeFromKey<LinkedQ, LinkedK>> = ValidComponentsForPropertyType<PropertyTypeFromKey<LinkedQ, LinkedK>>`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`searchField`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L51) | `boolean` | 可选 | true | 显示候选值搜索入口。 | 数据/呈现/能力配置 |
| [`id`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L63) | `string` | 可选 | 由属性/关联定义推导 | 稳定筛选 ID；重复属性配置时应显式提供。 | 数据/呈现/能力配置 |
| [`isVisible`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L70) | `boolean` | 可选 | true | 控制是否呈现此列/筛选项。 | 数据/呈现/能力配置 |
| [`type`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L117) | `"LINKED_PROPERTY"` | 必填 | 无；必须提供 | 筛选定义的判别标记。 | 数据/呈现/能力配置 |
| [`linkName`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L118) | `L` | 必填 | 无；必须提供 | 来源对象的 link 名称。 | 数据/呈现/能力配置 |
| [`reverseLinkName`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L122) | `LinkNames<LinkedQ>` | 可选 | undefined / 未声明 | 目标对象指回来源对象的 link 名称。 | 弃用配置 |
| [`linkedPropertyKey`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L123) | `LinkedK` | 必填 | 无；必须提供 | 要筛选的目标对象属性。 | 数据/呈现/能力配置 |
| [`filterComponent`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L135) | `LinkedC` | 可选 | undefined / 未声明 | 配置输入控件类别；类型与属性数据类型关联。 | 数据/呈现/能力配置 |
| [`linkedFilterComponent`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L140) | `LinkedC` | 可选 | undefined / 未声明 | 旧的关联输入控件字段。 | 弃用配置 |
| [`defaultFilterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L148) | `FilterStateByComponentType[LinkedC]` | 可选 | undefined，初始无值 | 该项初始值种子。 | 初始种子；具体例外见说明 |
| [`defaultLinkedFilterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L153) | `FilterStateByComponentType[LinkedC]` | 可选 | undefined / 未声明 | 旧的关联初始状态字段。 | 弃用；初始种子 |
| [`linkedFilterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L158) | `FilterStateByComponentType[LinkedC]` | 可选 | undefined / 未声明 | 旧的关联状态字段。 | 弃用配置 |
| [`filterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L163) | `LinkedPropertyFilterState<FilterStateByComponentType[LinkedC]>` | 可选 | undefined / 未声明 | 该筛选项当前状态；允许显式 undefined。 | 弃用配置 |
| [`label`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L165) | `string` | 可选 | undefined / 未声明 | 配置展示名称。 | 数据/呈现/能力配置 |
| [`showCount`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L172) | `boolean` | 可选 | LISTOGRAM/MULTI_SELECT=true；SINGLE_SELECT=false | 控制候选值计数显示。 | 数据/呈现/能力配置 |
| [`renderValue`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/LinkedFilterTypes.ts#L181) | `(value: string) => ReactNode` | 可选 | undefined / 未声明 | 自定义候选值的呈现。 | 宿主提供函数 |

### 自定义筛选定义 / `CustomFilterDefinition`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/CustomRendererTypes.ts)；实际发布声明：`build/types/filter-list/types/CustomRendererTypes.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

CUSTOM 定义：renderInput 是实际采用的输入扩展点；renderItem 虽有类型，当前渲染路径未使用。toWhereClause 负责自定义值到对象查询条件的转换。

泛型：`Q extends ObjectTypeDefinition`；`State extends BaseFilterState = CustomFilterState`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`searchField`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L51) | `boolean` | 可选 | true | 显示候选值搜索入口。 | 数据/呈现/能力配置 |
| [`id`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L63) | `string` | 可选 | 由属性/关联定义推导 | 稳定筛选 ID；重复属性配置时应显式提供。 | 数据/呈现/能力配置 |
| [`isVisible`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L70) | `boolean` | 可选 | true | 控制是否呈现此列/筛选项。 | 数据/呈现/能力配置 |
| [`type`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/CustomRendererTypes.ts#L68) | `"CUSTOM"` | 必填 | 无；必须提供 | 筛选定义的判别标记。 | 数据/呈现/能力配置 |
| [`key`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/CustomRendererTypes.ts#L72) | `string` | 必填 | 无；必须提供 | 属性 key 或自定义筛选 key。 | 数据/呈现/能力配置 |
| [`label`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/CustomRendererTypes.ts#L73) | `string` | 可选 | undefined / 未声明 | 配置展示名称。 | 数据/呈现/能力配置 |
| [`filterComponent`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/CustomRendererTypes.ts#L74) | `"CUSTOM"` | 必填 | 无；必须提供 | 配置输入控件类别；类型与属性数据类型关联。 | 数据/呈现/能力配置 |
| [`defaultFilterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/CustomRendererTypes.ts#L81) | `State` | 可选 | undefined，初始无值 | 该项初始值种子。 | 初始种子；具体例外见说明 |
| [`filterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/CustomRendererTypes.ts#L86) | `State` | 可选 | undefined / 未声明 | 该筛选项当前状态；允许显式 undefined。 | 弃用配置 |
| [`renderInput`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/CustomRendererTypes.ts#L91) | `(props: CustomFilterInputRendererProps<Q, State>) => ReactNode` | 可选 | undefined / 未声明 | 自定义筛选输入渲染。 | 宿主提供函数 |
| [`renderItem`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/CustomRendererTypes.ts#L96) | `(props: CustomFilterItemRendererProps<Q, State>) => ReactNode` | 可选 | undefined / 未声明 | 类型存在，当前渲染路径未使用；采用 renderInput。 | 宿主提供函数 |
| [`toWhereClause`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/CustomRendererTypes.ts#L101) | `(state: State) => WhereClause<Q> \| undefined` | 必填 | 无；必须提供 | 将输入状态转为 WhereClause。 | 宿主提供函数 |

### 静态选项筛选定义 / `StaticValuesFilterDefinition`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts)；实际发布声明：`build/types/filter-list/types/StaticValuesTypes.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此配置作为所属主组件的输入；类型详情由固定声明定义。

泛型：`Q extends ObjectTypeDefinition`；`C extends StaticValuesComponentType = StaticValuesComponentType`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`searchField`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L51) | `boolean` | 可选 | true | 显示候选值搜索入口。 | 数据/呈现/能力配置 |
| [`id`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L63) | `string` | 可选 | 由属性/关联定义推导 | 稳定筛选 ID；重复属性配置时应显式提供。 | 数据/呈现/能力配置 |
| [`isVisible`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/FilterListItemApi.ts#L70) | `boolean` | 可选 | true | 控制是否呈现此列/筛选项。 | 数据/呈现/能力配置 |
| [`type`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L45) | `"STATIC_VALUES"` | 必填 | 无；必须提供 | 筛选定义的判别标记。 | 数据/呈现/能力配置 |
| [`key`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L52) | `string` | 必填 | 无；必须提供 | 属性 key 或自定义筛选 key。 | 数据/呈现/能力配置 |
| [`label`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L57) | `string` | 可选 | undefined / 未声明 | 配置展示名称。 | 数据/呈现/能力配置 |
| [`filterComponent`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L62) | `C` | 必填 | 无；必须提供 | 配置输入控件类别；类型与属性数据类型关联。 | 数据/呈现/能力配置 |
| [`defaultFilterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L69) | `FilterStateByComponentType[C]` | 可选 | undefined，初始无值 | 该项初始值种子。 | 初始种子；具体例外见说明 |
| [`filterState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L74) | `FilterStateByComponentType[C]` | 可选 | undefined / 未声明 | 该筛选项当前状态；允许显式 undefined。 | 弃用配置 |
| [`values`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L80) | `string[]` | 必填 | 无；必须提供 | 宿主提供的静态候选选项。 | 数据/呈现/能力配置 |
| [`renderValue`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L89) | `(value: string) => ReactNode` | 可选 | undefined / 未声明 | 自定义候选值的呈现。 | 宿主提供函数 |
| [`showCount`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L96) | `boolean` | 可选 | LISTOGRAM/MULTI_SELECT=true；SINGLE_SELECT=false | 控制候选值计数显示。 | 数据/呈现/能力配置 |
| [`colorMap`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L102) | `Record<string, string>` | 可选 | undefined / 未声明 | 按候选值配置颜色。 | 数据/呈现/能力配置 |
| [`listogramConfig`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L108) | `{ displayMode?: "full" \| "count" \| "minimal"; maxVisibleItems?: number; }` | 可选 | undefined / 未声明 | 配置条形计数呈现。 | 数据/呈现/能力配置 |
| [`toWhereClause`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/types/StaticValuesTypes.ts#L122) | `(state: FilterState) => WhereClause<Q> \| undefined` | 可选 | undefined / 未声明 | 将输入状态转为 WhereClause。 | 宿主提供函数 |

### ActionForm / `ActionFormProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts)；实际发布声明：`build/types/action-form/ActionFormApi.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

Q extends ActionDefinition<unknown>。这是 ControlledActionFormProps | UncontrolledActionFormProps：传 formState 时必须同时传 onFormStateChange；省略时组件持有状态。onSubmit 回调会接管默认提交，回调内按需调用 applyAction。Action 权限/服务端校验仍由平台执行。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionForm.tsx)。

泛型：`Q extends ActionDefinition<unknown>`。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`formTitle`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L190) | `string` | 可选 | undefined / 未声明 | 配置表单标题。 | 数据/呈现/能力配置 |
| [`isSubmitDisabled`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L196) | `boolean` | 可选 | false | 宿主额外禁用提交。 | 数据/呈现/能力配置 |
| [`actionDefinition`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L66) | `Q` | 必填 | 无；必须提供 | 已生成的 ActionDefinition。 | 数据/呈现/能力配置 |
| [`showFormTitle`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L73) | `boolean` | 可选 | false | 是否展示标题；false 时 formTitle 不显示。 | 数据/呈现/能力配置 |
| [`formFieldDefinitions`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L78) | `ReadonlyArray<FormFieldDefinition<Q>>` | 可选 | undefined / 未声明 | 字段覆写配置；省略时依据 Action 元数据生成。 | 数据/呈现/能力配置 |
| [`onSubmit`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L88) | `(formState: FormState<Q>, applyAction: (formState: FormState<Q>) => Promise<ActionEditResponse \| undefined>) => Promise<unknown> \| void` | 可选 | undefined / 未声明 | 接管提交；ActionForm 回调获得 applyAction 供显式调用。 | 回调/事件；不会自动持久化 |
| [`onValidationResponse`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L100) | `(results: ActionValidationResponse) => void` | 可选 | undefined / 未声明 | 仅类型声明，当前 ActionForm 实现未消费此回调。 | 声明回调；当前无运行调用 |
| [`onSuccess`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L107) | `(results: ActionEditResponse \| undefined) => void` | 可选 | undefined / 未声明 | 读取 Action 提交成功结果。 | 回调/事件；不会自动持久化 |
| [`onError`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L114) | `(error: FormError) => void` | 可选 | undefined / 未声明 | 接收 metadata 错误及 try 范围内提交错误；coercion 抛错由 BaseForm 的异步错误状态处理。 | 回调/事件；不会自动持久化 |
| [`formState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L42) | `FormState<Q>` | 条件必填 | 受控分支必须提供；非受控省略 | 外部提供当前表单状态。 | 受控分支的必填值；省略进入非受控 |
| [`onFormStateChange`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L48) | `(updater: (prevState: FormState<Q>) => FormState<Q>) => void` | 条件必填 | 受控分支必须提供；非受控省略 | ActionForm 通过 updater 通知外部状态更新。 | 受控分支必填；非受控分支可选 |

### BaseForm / `BaseFormProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts)；实际发布声明：`build/types/action-form/ActionFormApi.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

受控分支必须同时提供 formState 与 onFieldValueChange；非受控分支由内部 react-hook-form 持有字段值。onSubmit 是必要业务函数；Base 不生成 OSDK Action 请求。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/BaseForm.tsx)。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`formTitle`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L190) | `string` | 可选 | undefined / 未声明 | 配置表单标题。 | 数据/呈现/能力配置 |
| [`formContent`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L192) | `ReadonlyArray<FormContentItem>` | 必填 | 无；必须提供 | 字段或分区的渲染定义集合。 | 数据/呈现/能力配置 |
| [`onSubmit`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L194) | `(formState: Record<string, unknown>) => Promise<void> \| void` | 必填 | 无；必须提供 | 提交当前 formState 给必填业务回调；BaseForm 不提供 applyAction。 | 回调/事件；不会自动持久化 |
| [`isSubmitDisabled`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L196) | `boolean` | 可选 | false | 宿主额外禁用提交。 | 数据/呈现/能力配置 |
| [`isPending`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L198) | `boolean` | 可选 | false | 标示当前提交尚未结束。 | 数据/呈现/能力配置 |
| [`isLoading`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L200) | `boolean` | 可选 | false | 提供加载状态。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L202) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |
| [`submitButtonText`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L204) | `string` | 可选 | "Submit" | 提交按钮文字。 | 数据/呈现/能力配置 |
| [`submitButtonVariant`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L206) | `"primary" \| "secondary"` | 可选 | "primary" | 提交按钮样式。 | 数据/呈现/能力配置 |
| [`formState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L174) | `Record<string, unknown>` | 条件必填 | 受控分支必须提供；非受控省略 | 外部提供当前表单状态。 | 受控分支的必填值；省略进入非受控 |
| [`onFieldValueChange`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L180) | `(fieldKey: string, value: unknown) => void` | 条件必填 | 受控分支必须提供；非受控省略 | BaseForm 通知单字段变化，受控宿主回写。 | 受控分支必填；非受控分支可选 |

### 表单分区配置 / `FormSectionDefinition`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts)；实际发布声明：`build/types/action-form/ActionFormApi.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此配置作为所属主组件的输入；类型详情由固定声明定义。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/FormSection.tsx)。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`title`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L144) | `string` | 必填 | 无；必须提供 | 配置标题。 | 数据/呈现/能力配置 |
| [`description`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L145) | `string` | 可选 | undefined / 未声明 | 分区说明。 | 数据/呈现/能力配置 |
| [`fields`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L146) | `ReadonlyArray<RendererFieldDefinition>` | 必填 | 无；必须提供 | 分区中的字段定义。 | 数据/呈现/能力配置 |
| [`collapsedByDefault`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L148) | `boolean` | 可选 | false | 分区初始折叠状态。 | 初始种子；具体例外见说明 |
| [`showTitleBar`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L150) | `boolean` | 可选 | true | 显示分区标题栏。 | 数据/呈现/能力配置 |
| [`columnCount`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L152) | `1 \| 2` | 可选 | 1 | 单列或双列字段布局。 | 数据/呈现/能力配置 |
| [`style`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L154) | `"box" \| "minimal"` | 可选 | "box" | 分区 box 边框或 minimal 呈现。 | 数据/呈现/能力配置 |

### AipAgentChat / `AipAgentChatProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts)；实际发布声明：`build/types/aip-agent-chat/AipAgentChatApi.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

仅 experimental/aip-agent-chat 子入口。model + onModelChange 为受控模型选择，defaultModel 是非受控种子；initialMessages 是聊天初始化输入。公开 barrel 未导出内部 Composer/Message 子组件。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChat.tsx)。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`client`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L48) | `PlatformClient` | 必填 | 无；必须提供 | 用于聊天的已配置 PlatformClient。 | 数据/呈现/能力配置 |
| [`model`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L63) | `string` | 可选 | undefined / 未声明 | 外部提供所选模型。 | 外部状态输入；具体所有权见本节说明 |
| [`defaultModel`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L75) | `string` | 可选 | availableModels[0]，否则 "gpt-4o" | 非受控模型初始值。 | 初始种子；具体例外见说明 |
| [`availableModels`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L83) | `ReadonlyArray<string>` | 可选 | undefined / 未声明 | 模型选择列表；省略时不显示 picker。 | 数据/呈现/能力配置 |
| [`onModelChange`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L101) | `(model: string) => void` | 可选 | undefined / 未声明 | 读取模型 picker 变化。 | 回调/事件；不会自动持久化 |
| [`system`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L106) | `string` | 可选 | undefined / 未声明 | 模型 system 指令。 | 数据/呈现/能力配置 |
| [`initialMessages`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L112) | `ReadonlyArray<UIMessage>` | 可选 | undefined / 未声明 | 聊天消息初始种子。 | 初始种子；具体例外见说明 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L117) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |
| [`placeholder`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L124) | `string` | 可选 | "Type a message..." | 配置空值占位文字。 | 数据/呈现/能力配置 |
| [`enableAutoScroll`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L132) | `boolean` | 可选 | true | 自动滚动到新消息。 | 数据/呈现/能力配置 |
| [`onError`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L141) | `(error: Error) => void` | 可选 | undefined / 未声明 | 接收聊天或 transport 的 Error（转交 useChat 的 onError）。 | 回调/事件；不会自动持久化 |
| [`onFinish`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L150) | `(event: { message: UIMessage; messages: ReadonlyArray<UIMessage>; }) => void` | 可选 | undefined / 未声明 | 读取本次完成消息和完整消息数组。 | 回调/事件；不会自动持久化 |
| [`renderEmptyState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L161) | `() => React.ReactNode` | 可选 | undefined / 未声明 | 自定义没有内容时的呈现。 | 宿主提供函数 |
| [`renderMessage`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L171) | `(message: UIMessage) => React.ReactNode` | 可选 | undefined / 未声明 | 自定义单条消息呈现。 | 宿主提供函数 |

### BaseAipAgentChat / `BaseAipAgentChatProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx)；实际发布声明：`build/types/aip-agent-chat/BaseAipAgentChat.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

messages/status/error 与发送/停止/清错均由宿主提供。error 属性本身必填，但其值可为 undefined。没有内置 client 请求。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx)。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`messages`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L33) | `ReadonlyArray<UIMessage>` | 必填 | 无；必须提供 | 宿主持有的完整消息集合。 | 外部状态输入；具体所有权见本节说明 |
| [`status`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L38) | `ChatStatus` | 必填 | 无；必须提供 | 宿主提供聊天运行状态。 | 数据/呈现/能力配置 |
| [`error`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L43) | `Error \| undefined` | 必填 | 无；必须提供 | 外部提供错误；部分接口要求显式传 undefined。 | 数据/呈现/能力配置 |
| [`onSendMessage`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L51) | `(text: string) => Promise<void>` | 必填 | 无；必须提供 | 宿主执行发送；Base 不建立请求。 | 回调/事件；不会自动持久化 |
| [`onStop`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L56) | `() => void` | 必填 | 无；必须提供 | 宿主停止正在运行的生成。 | 回调/事件；不会自动持久化 |
| [`onClearError`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L61) | `() => void` | 必填 | 无；必须提供 | 宿主清除错误。 | 回调/事件；不会自动持久化 |
| [`composerFooter`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L68) | `React.ReactNode` | 可选 | undefined / 未声明 | 在输入区底部插入内容。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L70) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |
| [`placeholder`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L75) | `string` | 可选 | "Type a message..." | 配置空值占位文字。 | 数据/呈现/能力配置 |
| [`enableAutoScroll`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L80) | `boolean` | 可选 | true | 自动滚动到新消息。 | 数据/呈现/能力配置 |
| [`renderEmptyState`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L82) | `() => React.ReactNode` | 可选 | undefined / 未声明 | 自定义没有内容时的呈现。 | 宿主提供函数 |
| [`renderMessage`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L83) | `(message: UIMessage) => React.ReactNode` | 可选 | undefined / 未声明 | 自定义单条消息呈现。 | 宿主提供函数 |

### CbacPicker / `CbacPickerProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPicker.tsx)；实际发布声明：`build/types/cbac-picker/CbacPicker.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此 Props 接口在内部组件声明中可见，但公共 barrel 没有 named type export。initialMarkingIds 初始化本地状态，数组 identity 变化也会重设选择；onChange 不写入对象安全标记。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/useCbacSelection.ts)。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`initialMarkingIds`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPicker.tsx#L32) | `string[]` | 可选 | [] | CBAC 本地选择初值；数组 identity 变化重设选择。 | 初始化＋数组 identity 变化重设 |
| [`onChange`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPicker.tsx#L39) | `(markingIds: string[]) => void` | 必填 | 无；必须提供 | 读取标记选择变化。 | 回调/事件；不会自动持久化 |
| [`maxClassificationConstraint`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPicker.tsx#L45) | `MaxClassificationConstraint` | 可选 | undefined / 未声明 | 最高分类提示约束；当前实现不阻止选择。 | 数据/呈现/能力配置 |
| [`readOnly`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPicker.tsx#L52) | `boolean` | 可选 | false | 禁用用户选择操作。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPicker.tsx#L57) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |

### CbacPickerDialog / `CbacPickerDialogProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPickerDialog.tsx)；实际发布声明：`build/types/cbac-picker/CbacPickerDialog.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

isOpen/onOpenChange 控制打开状态；initialMarkingIds 初始化并在数组 identity 变化时重设选择；cancel 调用 reset。单独 isOpen 变化没有重置 effect。onConfirm 返回 ID；保存、权限变更由宿主执行。Props 类型未从公共 barrel 导出。 [运行时状态/默认值实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/useCbacSelection.ts)。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`isOpen`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPickerDialog.tsx#L26) | `boolean` | 必填 | 无；必须提供 | 外部控制对话框是否打开。 | 外部状态输入；具体所有权见本节说明 |
| [`onOpenChange`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPickerDialog.tsx#L27) | `(open: boolean) => void` | 必填 | 无；必须提供 | 通知打开/关闭变化，宿主回写。 | 回调/事件；不会自动持久化 |
| [`onConfirm`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPickerDialog.tsx#L28) | `(markingIds: string[]) => void` | 必填 | 无；必须提供 | 读取确认；宿主自行保存，组件不写权限。 | 回调/事件；不会自动持久化 |
| [`initialMarkingIds`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPickerDialog.tsx#L29) | `string[]` | 可选 | undefined / 未声明 | CBAC 本地选择初值；数组 identity 变化重设选择。 | 初始化＋数组 identity 变化重设 |
| [`maxClassificationConstraint`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPickerDialog.tsx#L30) | `MaxClassificationConstraint` | 可选 | undefined / 未声明 | 最高分类提示约束；当前实现不阻止选择。 | 数据/呈现/能力配置 |

### CbacBanner / `CbacBannerProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBanner.tsx)；实际发布声明：`build/types/cbac-picker/CbacBanner.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

Props 类型未从公共 barrel 导出。markingIds 驱动加载/呈现，onClick/onDismiss 为宿主事件。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`markingIds`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBanner.tsx#L24) | `string[]` | 必填 | 无；必须提供 | 需要展示/编辑的标记 ID 集合。 | 数据/呈现/能力配置 |
| [`onClick`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBanner.tsx#L25) | `() => void` | 可选 | undefined / 未声明 | 读取点击。 | 回调/事件；不会自动持久化 |
| [`onDismiss`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBanner.tsx#L26) | `() => void` | 可选 | undefined / 未声明 | 读取关闭/移除提示点击。 | 回调/事件；不会自动持久化 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBanner.tsx#L27) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |
| [`isLoading`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBanner.tsx#L28) | `boolean` | 可选 | undefined / 未声明 | 提供加载状态。 | 数据/呈现/能力配置 |

### CbacBannerPopover / `CbacBannerPopoverProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBannerPopover.tsx)；实际发布声明：`build/types/cbac-picker/CbacBannerPopover.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

Props 类型未从公共 barrel 导出。markingIds 输入到内层选择，onChange 输出选择变化；不是自动权限更新。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`markingIds`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBannerPopover.tsx#L33) | `string[]` | 必填 | 无；必须提供 | 需要展示/编辑的标记 ID 集合。 | 数据/呈现/能力配置 |
| [`onChange`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBannerPopover.tsx#L34) | `(markingIds: string[]) => void` | 必填 | 无；必须提供 | 读取标记选择变化。 | 回调/事件；不会自动持久化 |
| [`maxClassificationConstraint`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBannerPopover.tsx#L35) | `MaxClassificationConstraint` | 可选 | undefined / 未声明 | 最高分类提示约束；当前实现不阻止选择。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBannerPopover.tsx#L36) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |

### BaseCbacPicker / `BaseCbacPickerProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx)；实际发布声明：`build/types/cbac-picker/base/BaseCbacPicker.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

categories/markingStates 和验证信息完全由宿主计算。isValid===false 与 requiredMarkingGroups 一起控制提示；maxClassificationConstraint 在 wrapper 侧只提示，不能把这些 props 视作授权校验。Props 类型未从公共 barrel 导出。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`categories`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L35) | `CategoryMarkingGroupType[]` | 必填 | 无；必须提供 | 已分组的候选标记。 | 数据/呈现/能力配置 |
| [`markingStates`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L36) | `Map<string, MarkingSelectionState>` | 必填 | 无；必须提供 | 外部提供每个标记的勾选/可选状态。 | 外部状态输入；具体所有权见本节说明 |
| [`banner`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L37) | `CbacBannerData` | 可选 | undefined / 未声明 | 外部提供分类 banner 数据。 | 数据/呈现/能力配置 |
| [`onMarkingToggle`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L38) | `(markingId: string) => void` | 必填 | 无；必须提供 | 请求宿主切换某标记状态。 | 回调/事件；不会自动持久化 |
| [`onDismissBanner`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L39) | `() => void` | 可选 | undefined / 未声明 | 读取信息 banner 的关闭点击。 | 回调/事件；不会自动持久化 |
| [`showInfoBanner`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L40) | `boolean` | 可选 | undefined / 未声明 | 显示信息 banner。 | 数据/呈现/能力配置 |
| [`requiredMarkingGroups`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L41) | `ReadonlyArray<RequiredMarkingGroup>` | 可选 | undefined / 未声明 | 需要至少选择一个标记的分组。 | 数据/呈现/能力配置 |
| [`isValid`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L42) | `boolean` | 可选 | undefined / 未声明 | 宿主计算当前选择是否有效。 | 数据/呈现/能力配置 |
| [`readOnly`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L43) | `boolean` | 可选 | undefined / 未声明 | 禁用用户选择操作。 | 数据/呈现/能力配置 |
| [`isLoading`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L44) | `boolean` | 可选 | undefined / 未声明 | 提供加载状态。 | 数据/呈现/能力配置 |
| [`error`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L45) | `Error` | 可选 | undefined / 未声明 | 外部提供错误；部分接口要求显式传 undefined。 | 数据/呈现/能力配置 |
| [`validationCallouts`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L46) | `React.ReactNode` | 可选 | undefined / 未声明 | 宿主插入校验提示内容。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L47) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |

### BaseCbacPickerDialog / `BaseCbacPickerDialogProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPickerDialog.tsx)；实际发布声明：`build/types/cbac-picker/base/BaseCbacPickerDialog.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

继承全部 BaseCbacPickerProps；额外要求 onConfirm/onCancel。Props 类型未从公共 barrel 导出。对话框关闭与确认均需宿主处理。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`categories`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L35) | `CategoryMarkingGroupType[]` | 必填 | 无；必须提供 | 已分组的候选标记。 | 数据/呈现/能力配置 |
| [`markingStates`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L36) | `Map<string, MarkingSelectionState>` | 必填 | 无；必须提供 | 外部提供每个标记的勾选/可选状态。 | 外部状态输入；具体所有权见本节说明 |
| [`banner`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L37) | `CbacBannerData` | 可选 | undefined / 未声明 | 外部提供分类 banner 数据。 | 数据/呈现/能力配置 |
| [`onMarkingToggle`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L38) | `(markingId: string) => void` | 必填 | 无；必须提供 | 请求宿主切换某标记状态。 | 回调/事件；不会自动持久化 |
| [`onDismissBanner`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L39) | `() => void` | 可选 | undefined / 未声明 | 读取信息 banner 的关闭点击。 | 回调/事件；不会自动持久化 |
| [`showInfoBanner`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L40) | `boolean` | 可选 | true（?? 回退） | 显示信息 banner。 | 数据/呈现/能力配置 |
| [`requiredMarkingGroups`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L41) | `ReadonlyArray<RequiredMarkingGroup>` | 可选 | undefined / 未声明 | 需要至少选择一个标记的分组。 | 数据/呈现/能力配置 |
| [`isValid`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L42) | `boolean` | 可选 | undefined / 未声明 | 宿主计算当前选择是否有效。 | 数据/呈现/能力配置 |
| [`readOnly`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L43) | `boolean` | 可选 | undefined / 未声明 | 禁用用户选择操作。 | 数据/呈现/能力配置 |
| [`isLoading`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L44) | `boolean` | 可选 | undefined / 未声明 | 提供加载状态。 | 数据/呈现/能力配置 |
| [`error`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L45) | `Error` | 可选 | undefined / 未声明 | 外部提供错误；部分接口要求显式传 undefined。 | 数据/呈现/能力配置 |
| [`validationCallouts`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L46) | `React.ReactNode` | 可选 | undefined / 未声明 | 宿主插入校验提示内容。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L47) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |
| [`isOpen`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPickerDialog.tsx#L25) | `boolean` | 必填 | 无；必须提供 | 外部控制对话框是否打开。 | 外部状态输入；具体所有权见本节说明 |
| [`onOpenChange`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPickerDialog.tsx#L26) | `(open: boolean) => void` | 必填 | 无；必须提供 | 通知打开/关闭变化，宿主回写。 | 回调/事件；不会自动持久化 |
| [`onConfirm`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPickerDialog.tsx#L27) | `() => void` | 必填 | 无；必须提供 | 读取确认；宿主自行保存，组件不写权限。 | 回调/事件；不会自动持久化 |
| [`onCancel`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPickerDialog.tsx#L28) | `() => void` | 必填 | 无；必须提供 | 读取取消点击。 | 回调/事件；不会自动持久化 |
| [`title`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPickerDialog.tsx#L29) | `string` | 可选 | "Select classification" | 配置标题。 | 数据/呈现/能力配置 |
| [`submitDisabledReason`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPickerDialog.tsx#L30) | `string` | 可选 | undefined / 未声明 | 提供禁用确认的原因提示。 | 数据/呈现/能力配置 |

### BaseCbacBanner / `BaseCbacBannerProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacBanner.tsx)；实际发布声明：`build/types/cbac-picker/base/BaseCbacBanner.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

纯展示分类字符串、颜色与可选点击。Props 类型未从公共 barrel 导出。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`classificationString`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacBanner.tsx#L28) | `string` | 必填 | 无；必须提供 | 已计算的分类显示文字。 | 数据/呈现/能力配置 |
| [`textColor`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacBanner.tsx#L29) | `string` | 必填 | 无；必须提供 | 已计算的分类文字颜色。 | 数据/呈现/能力配置 |
| [`backgroundColors`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacBanner.tsx#L30) | `string[]` | 必填 | 无；必须提供 | 已计算的分类背景颜色集合。 | 数据/呈现/能力配置 |
| [`onClick`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacBanner.tsx#L31) | `() => void` | 可选 | undefined / 未声明 | 读取点击。 | 回调/事件；不会自动持久化 |
| [`onDismiss`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacBanner.tsx#L32) | `() => void` | 可选 | undefined / 未声明 | 读取关闭/移除提示点击。 | 回调/事件；不会自动持久化 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacBanner.tsx#L33) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |
| [`isLoading`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacBanner.tsx#L34) | `boolean` | 可选 | undefined / 未声明 | 提供加载状态。 | 数据/呈现/能力配置 |

### MaxClassificationField / `MaxClassificationFieldProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/MaxClassificationField.tsx)；实际发布声明：`build/types/cbac-picker/base/MaxClassificationField.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

此配置作为所属主组件的输入；类型详情由固定声明定义。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`classificationString`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/MaxClassificationField.tsx#L25) | `string` | 必填 | 无；必须提供 | 已计算的分类显示文字。 | 数据/呈现/能力配置 |
| [`textColor`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/MaxClassificationField.tsx#L26) | `string` | 必填 | 无；必须提供 | 已计算的分类文字颜色。 | 数据/呈现/能力配置 |
| [`backgroundColors`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/MaxClassificationField.tsx#L27) | `string[]` | 必填 | 无；必须提供 | 已计算的分类背景颜色集合。 | 数据/呈现/能力配置 |
| [`helperText`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/MaxClassificationField.tsx#L28) | `string` | 可选 | undefined / 未声明 | 追加分类说明。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/MaxClassificationField.tsx#L29) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |

### OsdkThemeProvider / `OsdkThemeProviderProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/theme/OsdkThemeProvider.tsx)；实际发布声明：`build/types/theme/OsdkThemeProvider.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

theme + onThemeChanged 为受控主题模式；defaultTheme 为非受控种子，system 通过 matchMedia 解析。target 影响 DOM 主题属性和 portal 呈现，不自动改写所有业务 CSS。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`theme`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/theme/OsdkThemeProvider.tsx#L37) | `OsdkThemeMode` | 可选 | undefined / 未声明 | 外部控制 light/dark/system。 | 外部状态输入；具体所有权见本节说明 |
| [`defaultTheme`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/theme/OsdkThemeProvider.tsx#L44) | `OsdkThemeMode` | 可选 | "system" | 非受控主题初始种子。 | 初始种子；具体例外见说明 |
| [`onThemeChanged`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/theme/OsdkThemeProvider.tsx#L47) | `(theme: OsdkThemeMode) => void` | 可选 | undefined / 未声明 | 读取主题模式变化。 | 回调/事件；不会自动持久化 |
| [`target`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/theme/OsdkThemeProvider.tsx#L56) | `HTMLElement \| null` | 可选 | document.documentElement | 承载 data-bp-color-scheme 的 DOM 元素。 | 数据/呈现/能力配置 |
| [`children`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/theme/OsdkThemeProvider.tsx#L58) | `React.ReactNode` | 必填 | 无；必须提供 | 嵌套内容。 | 数据/呈现/能力配置 |

### ActionButton / `ButtonProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/action-button/ActionButton.tsx)；实际发布声明：`build/types/base-components/action-button/ActionButton.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>；以下只列包装器新增字段，React 原生 button 属性（disabled/type/onClick/aria-* 等）整体透传。组件通过 forwardRef<HTMLButtonElement> 公开 ref。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`variant`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/action-button/ActionButton.tsx#L24) | `"primary" \| "secondary"` | 可选 | "secondary" | primary/secondary 按钮样式。 | 数据/呈现/能力配置 |
| [`appearance`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/action-button/ActionButton.tsx#L25) | `"default" \| "minimal"` | 可选 | "default" | default/minimal 按钮呈现。 | 数据/呈现/能力配置 |

### Dialog / `DialogProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/dialog/Dialog.tsx)；实际发布声明：`build/types/base-components/dialog/Dialog.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

isOpen/onOpenChange 是受控接口；不能把 Base UI Root 的全部 props 当作本包装器支持。只有这里列出的字段被读取与转交。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`isOpen`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/dialog/Dialog.tsx#L27) | `boolean` | 必填 | 无；必须提供 | 外部控制对话框是否打开。 | 外部状态输入；具体所有权见本节说明 |
| [`onOpenChange`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/dialog/Dialog.tsx#L28) | `(open: boolean) => void` | 必填 | 无；必须提供 | 通知打开/关闭变化，宿主回写。 | 回调/事件；不会自动持久化 |
| [`title`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/dialog/Dialog.tsx#L29) | `React.ReactNode` | 必填 | 无；必须提供 | 配置标题。 | 数据/呈现/能力配置 |
| [`children`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/dialog/Dialog.tsx#L30) | `React.ReactNode` | 必填 | 无；必须提供 | 嵌套内容。 | 数据/呈现/能力配置 |
| [`footer`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/dialog/Dialog.tsx#L31) | `React.ReactNode` | 可选 | undefined / 未声明 | 对话框页脚内容。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/dialog/Dialog.tsx#L32) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |
| [`disablePointerDismissal`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/dialog/Dialog.tsx#L33) | `boolean` | 可选 | undefined / 未声明 | 将点击外部关闭限制转交 Base UI。 | 数据/呈现/能力配置 |

### SkeletonBar / `SkeletonBarProps`

[固定源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/skeleton/SkeletonBar.tsx)；实际发布声明：`build/types/base-components/skeleton/SkeletonBar.d.ts`。本地核对展开字段的名称与类型均已对齐发布 d.ts（忽略空白、可省标点与 union 前导竖线）。

宽/高/最大宽可 string 或 number；未给值时由 CSS 决定。没有公开通用 HTML 属性继承。

| 属性 | TS 类型（继承展开） | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| [`width`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/skeleton/SkeletonBar.tsx#L23) | `string \| number` | 可选 | undefined / 未声明 | 配置宽度。 | 数据/呈现/能力配置 |
| [`height`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/skeleton/SkeletonBar.tsx#L24) | `string \| number` | 可选 | undefined / 未声明 | 配置占位条高度。 | 数据/呈现/能力配置 |
| [`maxWidth`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/skeleton/SkeletonBar.tsx#L25) | `string \| number` | 可选 | undefined / 未声明 | 限制最大宽度。 | 数据/呈现/能力配置 |
| [`className`](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/skeleton/SkeletonBar.tsx#L26) | `string` | 可选 | undefined / 未声明 | 追加组件样式类。 | 数据/呈现/能力配置 |

### Tooltip / TooltipArrow（compound primitive）

入口 `@osdk/react-components/primitives`。`TooltipProps extends Omit<TooltipRootProps,"className">`，继承实际安装的 `@base-ui/react/tooltip` 类型；本包依赖范围 `>=1.0.0 <1.4.0`，不将某个外部版本全部参数固定成 0.61.0 自有 API。[完整包装器源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/tooltip/Tooltip.tsx#L17-L162)。

| 公开访问 | TS 接口 / 签名 | Required / 状态 | 本包装器默认与用途 |
|---|---|---|---|
| `Tooltip.Root` | `TooltipProps` | 继承 `TooltipRootProps`，支持其 open/defaultOpen/onOpenChange 协议 | 向 Base UI Root 透传；本包装器不新增 className |
| `Tooltip.Provider` | `Omit<TooltipProviderProps,"className"> & {className?:string}` | 继承外部 provider 参数 | 统一 tooltip 调度；className 是类型额外字段，实际 provider 参数需看实现 |
| `Tooltip.Trigger` | `Omit<TooltipTriggerProps,"className"> & {className?:string}` | 继承外部触发参数 | `delay` 默认 200ms；用户可覆盖 |
| `Tooltip.Positioner` | `Omit<TooltipPositionerProps,"className"> & {className?:string}` | 继承外部定位参数 | `sideOffset` 默认 4px |
| `Tooltip.Popup` | `Omit<TooltipPopupProps,"className"> & {className?:string}` | 继承外部弹出内容参数 | 加入本组件样式 |
| `Tooltip.Portal` | `typeof BaseUITooltip.Portal` | 原始 Base UI Portal 类型 | 直接引用；不同于本包某些其他组件的 portal context 包装 |
| `Tooltip.Arrow` / `TooltipArrow` | `() => ReactElement` | 无组件自有 props | 渲染固定 SVG 箭头 |

公开表格占位构件 `LoadingCell({width}:{width:number})` 的 width 必填；`LoadingCellContent()` 不接收自有 props。[对应源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/LoadingCell.tsx#L25-L39)。

公共 primitives 只导出 ActionButton、Dialog、SkeletonBar、Tooltip、TooltipArrow 及对应 4 个 props 类型。其余 source/base-components 输入控件没有自动变成公共 API。

## 3. Viewer 全参数图鉴

Viewer 的 17 个主/Base接口、97 行参数与 PDF 7 个构件58行参数统一放在 [api-viewers.md](api-viewers.md)，避免在两个文件重复。包含 exact types、必填、默认、事件、受控状态、ref 与 hooks 索引；与本文合计531行参数。

## 4. 全部公开 type symbols 索引

以下按公开 canonical 家族列出类型；兼容入口的重复/别名和所有 symbol → entrypoint 反向关系保留在 JSON。CBAC 多个 Props 接口只出现在组件签名中，不能假定可以 named import。

| 公共入口 | 显式 type exports |
|---|---|
| `@osdk/react-components/action-form` | `ActionFormProps`、`BaseFormProps`、`FormContentItem`、`FormError`、`FormSectionDefinition`、`FormState`、`ActionParameters`、`BaseFormFieldProps`、`CustomFieldProps`、`DropdownFieldProps`、`FieldComponent`、`FieldValueType`、`FilePickerProps`、`FormFieldDefinition`、`FormFieldPropsByType`、`NumberInputFieldProps`、`ObjectSelectFieldProps`、`ObjectSetFieldProps`、`Option`、`PortalContainer`、`RadioButtonsFieldProps`、`RendererFieldDefinition`、`TextAreaFieldProps`、`TextInputFieldProps`、`UnsupportedFieldProps`、`ValidationError` |
| `@osdk/react-components/document-viewer` | `DocumentViewerProps` |
| `@osdk/react-components/email-viewer` | `BaseEmailViewerProps`、`EmailAddress`、`EmailViewerProps`、`ParsedEmail` |
| `@osdk/react-components/filter-list` | `BaseFilterListProps`、`RenderFilterInput`、`FilterChangeEvent`、`FilterChangeReason`、`FilterChangeSnapshot`、`FilterDefinitionUnion`、`FilterListProps`、`FilterComponentType`、`FilterDefinitionControls`、`FilterState`、`PropertyFilterDefinition`、`RelativeDateBound`、`RelativeDateState`、`FilterPopoverProps`、`FilterInputProps`、`UseFilterListStateResult`、`LinkedFilter` |
| `@osdk/react-components/image-viewer` | `BaseImageViewerProps`、`ImageViewerProps` |
| `@osdk/react-components/markdown-viewer` | `BaseMarkdownViewerProps`、`MarkdownViewerProps` |
| `@osdk/react-components/object-table` | `ColumnDefinition`、`ColumnDefinitionLocator`、`CustomColumnLocator`、`EditFieldConfig`、`FunctionColumnLocator`、`LoadedObjectsChange`、`ObjectTableDataColumn`、`ObjectTableDataRow`、`ObjectTableHandle`、`ObjectTableProps`、`ObjectTableSnapshot`、`ObjectTableSnapshotOptions`、`PropertyColumnLocator`、`RdpColumnLocator`、`CellEditInfo`、`BaseTableProps`、`ColumnConfigDialogProps`、`ColumnConfigOptions`、`MultiColumnSortDialogProps`、`SortColumnItem`、`FunctionColumnData`、`UseFunctionColumnsDataProps`、`UseObjectTableDataProps`、`UseObjectTableDataResult`、`UseColumnDefsResult`、`UseSelectionColumnProps`、`UseColumnPinningProps`、`UseColumnPinningResult`、`UseColumnResizeProps`、`UseColumnResizeResult`、`UseColumnVisibilityProps`、`UseColumnVisibilityResult`、`UseFocusedRowProps`、`UseFocusedRowResult`、`UseLoadedObjectsChangedProps`、`UseRowSelectionChange`、`UseRowSelectionProps`、`UseRowSelectionResult`、`UseTableSortingProps`、`UseTableSortingResult`、`UseEditableTableProps`、`UseObjectTableSnapshotProps`、`UseCellContextMenuProps`、`UseCellContextMenuResult`、`PopoverPosition`、`ObjectSetOptions`、`RowSelectionChange`、`AsyncCellData`、`EditableConfig`、`EditModeState`、`OrderBy` |
| `@osdk/react-components/pdf-viewer` | `AnnotationType`、`BasePdfViewerProps`、`PdfAnnotation`、`PdfAnnotationRenderProps`、`PdfCustomAnnotation`、`PdfDownloadResult`、`PdfFormFieldValue`、`PdfRect`、`PdfSource`、`PdfTextHighlightEvent`、`SidebarMode`、`PdfViewerAnnotationLayerProps`、`PdfViewerContentProps`、`PdfViewerOutlineSidebarProps`、`PdfViewerSearchBarProps`、`PdfViewerSidebarProps`、`PdfViewerToolbarProps`、`AnnotationPortalTarget`、`UsePdfFormFieldsOptions`、`UsePdfFormFieldsResult`、`UsePdfHighlightModeOptions`、`UsePdfHighlightModeResult`、`UsePdfViewerResult`、`UsePdfViewerSearchResult`、`OutlineItem`、`PdfViewerHandle`、`PdfViewerInstanceOptions`、`PdfViewerContextValue`、`UsePdfViewerCoreOptions`、`UsePdfViewerCoreResult`、`UsePdfViewerStateOptions`、`UsePdfViewerStateResult`、`PdfViewerProps` |
| `@osdk/react-components/primitives` | `ButtonProps`、`DialogProps`、`SkeletonBarProps`、`TooltipProps` |
| `@osdk/react-components/spreadsheet-viewer` | `BaseSpreadsheetViewerProps`、`ParsedSpreadsheet`、`SheetData`、`SpreadsheetViewerProps` |
| `@osdk/react-components/tiff-viewer` | `BaseTiffViewerProps`、`TiffViewerProps` |
| `@osdk/react-components/video-viewer` | `BaseVideoViewerProps`、`VideoViewerProps` |
| `@osdk/react-components/xml-viewer` | `BaseXmlViewerProps`、`XmlViewerProps` |
| `@osdk/react-components/experimental/aip-agent-chat` | `AipAgentChatProps`、`BaseAipAgentChatProps`、`UIMessage`、`UIMessageRole`、`ChatStatus` |
| `@osdk/react-components/experimental/cbac-picker` | `CategoryMarkingGroup`、`CbacBannerData`、`MarkingSelectionState`、`MaxClassificationConstraint`、`PickerMarking`、`PickerMarkingCategory`、`RequiredMarkingGroup`、`MaxClassificationFieldProps` |
| `@osdk/react-components/experimental/theme` | `OsdkThemeProviderProps`、`OsdkThemeContextValue`、`OsdkThemeMode`、`ResolvedOsdkTheme` |

## 5. 核验与适用边界

30 个声明入口的 symbols 与发布源码 barrel 对齐，ESM runtime exports 与声明中的 runtime symbols 对齐；没有靠类型检查推断服务端行为。35 个非 viewer 参数/配置接口的展开字段名和类型文本也与实际 npm d.ts 对齐（忽略格式差异）；Viewer 参数的独立核验结果见上文。Props 表里 callback 不表示持久化、校验能力不表示权限授予、initial/default 不表示完全受控。

参考来源均为固定发布源码、npm 0.61.0 的 declaration/runtime 文件和该提交官方 docs。中文用途为研究者概括；实现边界以源码分支为准。此附录不替代 React/Base UI 外部继承 API、泛型关联的完整联合类型或实际平台授权测试。
