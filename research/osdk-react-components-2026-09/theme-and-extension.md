# 主题、公开入口、可组合边界与许可证核验

核验日期：2026-10-01。主依据是 `@osdk/react-components@0.61.0` 对应发布源码提交 `37cfd38676bf04edaef5847e929d914ea214c149`（[发布溯源已核验](README.md)）；本专题同时检查已解包的 npm JS、声明文件与 `styles.css`。`e53b94ecd5de7cdd7e864d0daa04363bdad4db4c` 仅用于 main 差异复核。主题、公开入口和 CSS 构建相关文件在两个提交间无差异；本文行为结论以发布版本为准。

## 结论

- **它不是完整 UI design system，但已经有受支持的 primitives 子路径。** npm 根入口运行时导出为空；应从 `object-table`、`filter-list` 等子路径导入。`primitives` 真实导出 `ActionButton`、`Dialog`、`SkeletonBar`、`Tooltip`、`TooltipArrow`，README 的“UI primitives 不导出”已经漂移；AGENTS 与源码/发布 JS 一致。[根源码][root-index]、[package exports][pkg-exports]、[primitives][primitives]、[README 冲突段][readme-primitives]、[AGENTS 现行指引][agents-exports]
- **稳定子路径与组件产品 GA 是两个维度。** 0.57.0 的 changelog 明确记录 stable export path promotion 和旧 experimental 路径的兼容保留；0.61.0 的 README 仍称 Beta，发布 Storybook 也给 `Components/` 统一加 Beta 标签。不能根据没有 `-beta` 后缀或 stable import path 推断整包已 GA。[promotion][promotion]、[README Beta][readme-beta]、[Storybook tag 实现][sb-tier]
- **主题是 CSS token + cascade layer，不是 CSS-in-JS Theme object。** 构建的 `styles.css` 把 token 放入 `osdk.tokens`，组件样式放入 `osdk.components`；`OsdkThemeProvider` 仍由 `experimental/theme` 导出，只负责 state/context 和 DOM 上的 `data-bp-color-scheme`。[CSS 构建][css-build]、[theme 入口][theme-export]、[Provider 实现][theme-provider]
- **Headless 不等于数据无关。** ObjectTable 公开了 14 个专门 hooks，FilterList 公开了 state hook 和组合/序列化 helpers，PDF 公开了较完整的 building blocks/hooks/context；但 `useColumnDefs` 和 `useFilterListState` 实际调用 `@osdk/react`，不能直接拿这些 hooks 接任意 REST/AntD 数据。[table public][table-public]、[filter public][filter-public]、[PDF public][pdf-public]、[useColumnDefs][column-defs]、[useFilterListState][filter-state]
- **各关键 OSDK 包的 manifest 都声明 Apache-2.0，依赖的许可并不全部相同。** UI 核心多为 MIT，Blueprint icons/PDF.js/`xlsx-republish` 是 Apache-2.0，`postal-mime@2.7.4` 声明 MIT-0。另有本地复制的 Blueprint core 6.11.3 token CSS，需要把这份代码来源纳入重分发检查。[组件 manifest][pkg-license]、[复制来源注释][blueprint-copy]、[依赖证据 JSON](evidence/components-dependency-license-metadata.json)

## 1. npm 导出边界：以已发布 JS 为准

### 1.1 包根入口与允许的子路径

`package.json` 声明 browser、ESM import/types、CJS require 条件入口，`styles.css` 是独立 export；`./*` 指向 `build/*/public/*`，不是指向整个 `src/`。因此“源码目录里存在”不代表允许公开 deep import；`src/base-components/...` 或 `src/shared/hooks/...` 并不会被这个模式自动转成公开入口。[manifest exports][pkg-exports]、[CSS/wildcard][pkg-wildcard]

实际 npm 根 ESM 模块的 `Object.keys(module)` 为 `[]`；根 `build/types/index.d.ts` 长度为 0。源码 `src/index.ts` 也只有 TODO 注释。应明确避免使用 `import { ObjectTable } from '@osdk/react-components'` 这种教程写法。[root-index][root-index]

| 类别 | 已发布入口 | 核验边界 |
| --- | --- | --- |
| 已晋升的组件 | `action-form`、`document-viewer`、`email-viewer`、`filter-list`、`image-viewer`、`markdown-viewer`、`object-table`、`pdf-viewer`、`spreadsheet-viewer`、`tiff-viewer`、`video-viewer`、`xml-viewer` | explicit package exports + public barrel；晋升记录见 0.57.0。[manifest][pkg-exports]、[promotion][promotion] |
| 通用 primitives | `primitives` | 仅 ActionButton、Dialog、SkeletonBar、Tooltip、TooltipArrow 及对应 props 类型；不是整个 base-components 目录。[primitives][primitives] |
| 仍在 experimental 的新增域 | `experimental/aip-agent-chat`、`experimental/cbac-picker`、`experimental/theme` | 无对应稳定 barrel；AGENTS 如此区分。[AGENTS][agents-exports] |
| 兼容旧路径 | `experimental/action-form`、`experimental/object-table` 等 | 已晋升组件的旧 barrel 是 `@deprecated` aliases，赋值引用稳定 symbol；不是另一份实现。[table shim][table-shim]、[form shim][form-shim] |
| 名称兼容 | `experimental/markdown-renderer`、`experimental/tiff-renderer` | 老 `MarkdownRenderer`/`TiffRenderer` alias 指向 BaseMarkdownViewer/BaseTiffViewer；老 `...ViewerMedia` 指向 OSDK wrapper。[markdown shim][markdown-shim]、[TIFF shim][tiff-shim] |
| 聚合入口 | `experimental` | 聚合部分兼容 barrel、CBAC 与 theme；**不包含 AipAgentChat**，后者须从专属子路径导入。[experimental aggregate][experimental-aggregate] |

在发布 `package.json`/`src/public` 中未发现 `alpha` export tier。Storybook brand theme extractor 的 `generateMarkdown()` 确实写 `version: alpha`，但它是生成 `DESIGN.md` 的 frontmatter，不能用来给整个组件库判 Alpha。[brand export][brand-alpha]

### 1.2 README 与真实 API 的差异

README L241 的“UI primitives 不导出”和 L245 建议简单控件用别家库，应解读为早期产品定位；不能用它否定实际 `primitives` API。当前 CLAUDE/AGENTS 开发说明已经要求公开 primitives barrel 列出可复用 symbol，未列入的 primitives 保持 internal。发布 npm ESM `public/primitives.js` 与 `public/primitives.d.ts` 分别有 runtime value exports 和 props type exports，两个面相互吻合。[README][readme-primitives]、[public primitives][primitives]、[开发说明][claude-primitives]

`ActionButton` 是 Base UI Button 的 memo/forwardRef 包装，提供 `variant='secondary'`（`primary|secondary`）和 `appearance='default'`（`default|minimal`），其余原生 button 属性透传；`Dialog` 是受控 Base UI Dialog 包装，必需 `isOpen`、`onOpenChange`、`title`、`children`，可选 footer/className/disablePointerDismissal。这些是已有基础控件，不是自动执行 Ontology Action 的 `ActionForm`。[ActionButton][action-button]、[Dialog][dialog]

### 1.3 可组合层的精确范围

| 表面 | Runtime 可复用项 | 重要限制 |
| --- | --- | --- |
| ObjectTable | BaseTable、ColumnConfigDialog、MultiColumnSortDialog、LoadingCell/LoadingCellContent；14 hooks：useFunctionColumnsData、useObjectTableData、useColumnDefs、useSelectionColumn、useColumnPinning、useColumnResize、useColumnVisibility、useFocusedRow、useLoadedObjectsChanged、useRowSelection、useTableSorting、useEditableTable、useObjectTableSnapshot、useCellContextMenu | 数据/metadata hooks 接 OSDK，状态 hooks 的 props/返回值仍常绑定 OSDK type 和 TanStack shape。[table public][table-public] |
| FilterList | BaseFilterList、FilterPopover、FilterInput、useFilterListState；serialize/deserializeFilterStates、filterHasActiveState、NO_VALUE、getFilterKey/getFilterLabel、summarizeFilterValue、narrowObjectSet | state hook 与 helper 中有 ObjectSet/metadata 语义；不是一套与 Ontology 无关的 generic query-builder。[filter public][filter-public]、[state imports][filter-state] |
| ActionForm | ActionForm、BaseForm；大量 form field/parameter/renderer 定义是 `export type` | 0.61.0 public barrel 没有公开 field component values，也没有 `useBaseForm`/`useActionForm` hook；类型名存在不代表可 import 一个对应 UI component。[form public][form-public] |
| PDF | BasePdfViewer、AnnotationLayer/Content/OutlineSidebar/SearchBar/Sidebar/Toolbar；PdfViewerProvider、usePdfViewerContext/usePdfViewerInstance；primitive/composition hooks | 公共组合 hooks 的签名是既定 PDF state/document/annotation 形状，需要按 Context/实例机制组合。[PDF public][pdf-public] |
| 其他文档 viewer | 多数各自公开 OSDK wrapper、Base counterpart 与 props；DocumentViewer 公开 DocumentViewer、ViewerType | 不要由统一 DocumentViewer 推断它导出一个 OSDK 无关的 BaseDocumentViewer；该 public barrel 没有这个 value。[document public][document-public] |

某些目录内 hook（如通用 useMediaContents/useAsyncAction）未出现在 public barrel，也没有对应 export target；不要凭源码文件清单称为支持 API。[table public][table-public]、[package exports][pkg-exports]

`BaseTable` 并非 AntD Table 的 `dataSource` 替代品：它必需一个通过 `useReactTable` 构建的 TanStack `Table<TData>` 实例。它没有网络获取，允许可选 `fetchNextPage` 连接自有数据源，但 rendering contract 已经绑定 TanStack Table。[BaseTable signature][base-table]

公开 OSDK wrapper 通常在 barrel 用 `withOsdkMetrics` 包装，它在 render 时调用 `useRegisterUserAgent`；Base counterpart 不经该包装。因此“拿 OSDK wrapper 当纯 UI”会顺便引入 provider/OSDK 依赖；这与直接用 Base 层不同。[table wrapper][table-public]、[metrics implementation][metrics]

## 2. Theme Provider、CSS layers 与变量

![Workshop Dark](assets/12-workshop-dark.jpg)

在官方 Storybook 切换 Workshop Dark 后的真实界面。主题名称和视觉对齐有直接证据，不能据此推断 Workshop 源码同源。

### 2.1 Provider 的 runtime contract

| props/输出 | 合约及运行实现 |
| --- | --- |
| `theme?: 'light'\|'dark'\|'system'` | 传入即受控；`theme = controlledTheme ?? internalTheme`，descendant `setTheme` 不改变 internal state，只通知回调。[provider][theme-provider] |
| `defaultTheme` | 默认 `system`；仅给 uncontrolled `useState` 初值，之后改该 prop 不是同步 state 的机制。[provider][theme-provider] |
| `onThemeChanged(next)` | 每次调用 `setTheme(next)` 都调用回调；不因 OS preference 改变或父 props 改变自动通知，源码 callback 只在 setTheme 内。[provider callback][theme-provider] |
| `target?: HTMLElement\|null` | `target ?? document.documentElement`；`null` 不是禁止写属性的 signal。Effect 保存上一个属性值，unmount/依赖变化 cleanup 后恢复/删除。[DOM effect][theme-dom] |
| `children` | 必需 ReactNode；仅返回 Context.Provider，没有新增 div/布局/portal container。[provider return][theme-provider] |
| `useOsdkTheme()` | 返回 `{theme,resolvedTheme,setTheme}`；不在 Provider 下会直接 throw。[hook][theme-hook] |
| 系统监听 | `useSyncExternalStore` + `matchMedia('(prefers-color-scheme: dark)')` 的 change listener；无 window/matchMedia 和 server snapshot 取 light。[system hook][theme-system] |

Theme Provider 自身只依赖 React，不读取 OsdkProvider/client；文档把它放在 OsdkProvider 内是完整 OSDK app 的组合例子，不是这个 Provider 的 runtime dependency。它没有 storage/persistence、跨 tab 同步、AntD ThemeConfig 注入或自动读 Zustand/Jotai；若 EOS 已有主题 store，调用者可把 store 值给 `theme`，把 `onThemeChanged` 写回 store。这是一个很薄的 adapter seam。[源码完整实现][theme-provider]；后半为**集成建议**。

上游测试源码覆盖默认 system、light override、OS 改变、uncontrolled setTheme、controlled 忽略本地变更并通知、受控父 rerender、unmount 恢复/清除、custom target、hook 越界 throw。本次没有执行上游测试，不能把“有测试”写成“本环境已通过”。[Provider tests][theme-tests]、[throw test][theme-throw-test]

**React 19 支持边界：** 发布 peers 声明 React/ReactDOM/@types/react `^17 || ^18 || ^19`，而开发依赖和发布锁文件实际用 React 18.3.1。声明 React19 可装不等于本文证明每个组件在 React19 已全面回归；有限 React19 mock 验证只覆盖普通 BaseForm 路径，见 [验证范围](checks.md)。[peers/devdeps][pkg-deps]、[lock][component-lock]

**静态发现：React17 范围存在疑点。** `useSystemTheme` 从 `react` 直接 import `useSyncExternalStore`，React 官方把它列为 React18 新增 hook；没有看到 shim。因此至少 theme entry 在普通 React17 环境不能仅凭 peer 范围断言可用。本文未执行 React17 fixture，标为源码与官方 API 的兼容性推断。[system import][theme-system]、[React18 新 hooks](https://react.dev/blog/2022/03/29/react-v18#usesyncexternalstore)

### 2.2 样式结构和主题来源

`src/tokens.css` 串联 base.css、dark.css 和各 component token 文件。base.css 导入 **本地** `blueprint-design-tokens.css`；该文件注释明确是复制自 `@blueprintjs/core@6.11.3`，用于移除 `@blueprintjs/core` runtime dependency。当前依赖表只有 `@blueprintjs/icons`，没有 `@blueprintjs/core`。因此 CSSVariables.md 的“通过 @import 从 Blueprint Core 导入”图示已与实际实现不同。[token entry][token-entry]、[base import][base-tokens]、[copy note][blueprint-copy]、[dependencies][pkg-deps]、[旧图][css-doc-old]

Token 层次是 Blueprint `--bp-*` → OSDK semantic `--osdk-*` → component `--osdk-table-*`/`--osdk-filter-*`/`--osdk-form-*` 等。table token 可以控制 header 高度、border、row backgrounds、cell padding、loading skeleton、column config dialog 和编辑 footer；filter token 可控制 container、header、filtered-out muted rows 等。它是 CSS 样式的细粒度入口，不会替换组件 DOM 和行为。[base mappings][base-tokens]、[table token][table-tokens]、[filter token][filter-tokens]

构建脚本把 CSS Modules 转成 hashed class mapping proxy，收集 token CSS 和 component CSS，输出单独 `build/browser/styles.css`，内部声明 `@layer osdk.tokens, osdk.components`。发布 npm 将 CSS 标为 sideEffects；应用仍必须显式引入样式，不能期待单纯 JS import 包含完整 token 和 component styles。[build script][css-build]、[style export / side effects][pkg-wildcard]、[files/sideEffects][pkg-files]

dark.css 通过 `[data-bp-color-scheme='dark']` 和 `.bp6-dark` selector 激活 OSDK overrides；`--osdk-dark-*` 是源码注释标明私有 helpers。建议 EOS consumer override 公共 semantic/component tokens，不直接依赖 helpers。[dark selectors/private note][dark-tokens]

README 推荐把 styles.css 再放进外层 `osdk.styles`，品牌层置后；Tailwind4 import 放单独早层。它同时要求 app root `isolation:isolate` 配合 Base UI portals。[CSS setup][readme-css]

```css
/* 推荐的 EOS token 桥接示意；不是已运行 demo。 */
@layer host.reset, osdk.styles, eos.brand;
@import '@osdk/react-components/styles.css' layer(osdk.styles);
@layer eos.brand {
  :root {
    --osdk-typography-family-default: var(--eos-font-family);
    --osdk-intent-primary-rest: var(--eos-color-primary);
    --osdk-table-header-height: 44px;
  }
}
```

**CSS 集成推断：** README 的“later layer always wins”只适用于同 origin、同 importance 的普通 layered 声明。CSS 规范规定 unlayered 普通声明排在显式层之后；`!important` 的层优先序反转。若 EOS/AntD 宿主把全局 reset 或通用 button rules 留在 unlayered，可能覆盖 OSDK layered rules。应按实际 bundler 的 import 和浏览器 computed styles 验证，不能仅从 layer 名称断言隔离成功。[W3C cascade sorting](https://www.w3.org/TR/css-cascade-5/#cascade-sort)、[layer ordering](https://www.w3.org/TR/css-cascade-5/#layer-order)

### 2.3 theme 的 scope 与限制

默认写 `<html>` 能让 React tree 外的 portal 继承 dark/light。换成局部 target 时，theme docs 明确提醒 portal 可能仍跟 document theme；Dialog 确实把 portal container 取自内部 `PortalContainerContext`，这个 Context/Provider 自身没有 public export。不能把局部 theme target 误认为自动迁移 portal。[docs scope][theme-scope]、[Dialog portal][dialog]、[internal context][portal-context]

**需复测的文档陷阱（静态推断）：** docs 用 `target={scopeRef.current}` 的简单示例在第一次 render 传 null，Provider 的 `?? document.documentElement` 会回落全局；React ref 赋值本身不会 rerender，不能假设 ref 设置后 target 必然更新。更稳妥的 adapter 先用 callback ref/state 得到 DOM node，再挂载局部 Provider；仍须检验 portal 的实际主题。本文未写上游 bug 或给它标已实测。[文档例子][theme-scope]、[provider fallback][theme-dom]、[React useRef caveat](https://react.dev/reference/react/useRef#caveats)

## 3. CBAC family 图鉴

![CBAC Picker](assets/14-cbac-picker.jpg)

官方 BaseCbacPicker fixture；画面中的安全标记字符串是公开测试数据，不是实际受限数据或权限结果。

### 3.1 定位、依赖与公开 family

CBAC family 是 **分类标记的选择和展示 UI**：按 category 展示 markings，反映 selected/implied/disallowed/required 状态，取得分类 banner 文本与颜色；它不自行把 marking 写回任何对象/文件，也不是 EOS 独立的权限决策引擎。OSDK-aware wrappers 用 `@osdk/react/platform-apis` 获取 categories、markings、banner/restrictions；后者实际调用 `@osdk/foundry.admin` 的 list/get，banner 和 restrictions 带 `preview:true`。这些 APIs 的权限来自 provider/client 的用户身份，本文未访问真实 admin API。[state data flow][cbac-state]、[admin restrictions hook][cbac-restrictions]、[admin banner hook][cbac-banner-hook]

`@osdk/foundry.admin`/`@osdk/foundry.core` 在 `@osdk/react` 是 optional peers；用了此 platform-apis 域仍须确保匹配包存在。Base counterparts 不 import OSDK query hooks，允许 EOS 提供自己的 category/state/banner 数据；但**rules/restrictions/保存权限必须由自有 backend 提供**。[react peers][react-pkg]、[base picker imports][cbac-base-picker]、[CBAC public][cbac-public]

| Runtime export（均来自 `experimental/cbac-picker`） | 定位/关键输入 | 状态、默认、events 与限制 |
| --- | --- | --- |
| `CbacPicker` | Inline OSDK-aware selector；必需 `onChange(ids)`；可选 initialMarkingIds、maxClassificationConstraint、readOnly、className | 初始 ids 默认 []；readOnly 未传时为 false-ish。toggle 写内部 selection 并发 onChange；清除 banner 写 [] 并发 onChange。没有 `value`/`selectedIds` controlled prop。[Picker props/runtime][cbac-picker] |
| `CbacPickerDialog` | Modal OSDK selector；必需 isOpen、onOpenChange、onConfirm(ids)；可选 initialMarkingIds、maxClassificationConstraint | open 受控；selection 为内部 state，初始 ids 默认 []。有初始值 title 为 Edit classification，否则 Add classification；confirm 不自行关闭，不保存；cancel reset selection 并通知 close。[Dialog runtime][cbac-dialog] |
| `CbacBanner` | OSDK ids → resolved banner；必需 markingIds；可选 onClick/onDismiss/className/isLoading | isLoading 默认 false，与 banner query loading 作 OR。给 onClick 变可点击，给 onDismiss 显示清除按钮；onDismiss 不自行写后端或调用 onChange。[Banner][cbac-banner] |
| `CbacBannerPopover` | banner + applied-marking 详情 + Edit dialog；必需 markingIds 与 onChange；可选 maxClassificationConstraint/className | markings 是父控制输入；内部只拥有 dialog open。confirm 调用 onChange(newIds) 并关闭 dialog，调用方仍需更新 markingIds/持久化；支持 query error/retry 展示。[Popover][cbac-popover] |
| `BaseCbacPicker` | 无 OSDK fetch；必需 categories、markingStates Map、onMarkingToggle(id) | selection 数据是 caller 控制。可选 banner/onDismissBanner/showInfoBanner/requiredMarkingGroups/isValid/readOnly/isLoading/error/validationCallouts/className；showInfoBanner 仅 `===true` 显示，initial loading 仅在 categories 为空时展示；没有生成 restrictions 的能力。[BasePicker][cbac-base-picker] |
| `BaseCbacPickerDialog` | BasePicker + Dialog layout；继承 BasePicker 输入并必需 isOpen、onOpenChange、onConfirm()、onCancel() | title 默认 Select classification；showInfoBanner 未传时在此 wrapper 默认 true；disablePointerDismissal=true；submitDisabledReason 存在即 disable confirm 并配 tooltip。Base caller 自行给 disable 原因，isValid 本身并不自动 disable footer。[BaseDialog][cbac-base-dialog]、[footer][cbac-footer] |
| `BaseCbacBanner` | 必需 classificationString、textColor、backgroundColors；可选 callbacks/className/isLoading | isLoading 默认 false；颜色作为 inline CSS custom props 注入；onDismiss stopPropagation 后只调用回调；无数据 fetching/验证。[BaseBanner][cbac-base-banner] |
| `MaxClassificationField` | 静态最大分类提示；必需 classificationString、textColor、backgroundColors；可选 helperText/className | 输出固定 label + BaseCbacBanner + helper text，没有 field value/setter、选择器、比较器或 onChange，因此名称里的 Field 不等于可编辑输入。[Max field][cbac-max-field] |

`BaseCbacBannerPopover` 源码虽然存在，**不在 public barrel 导出**。同样 `useCbacSelection`、`useCbacPickerState` 是内部 hooks；真正公开的 headless values 仅 `toggleMarking`、`computeMarkingStates`、`groupMarkingsByCategory` 三个纯 selection utilities。`CbacPickerProps`/`CbacPickerDialogProps`/Base props 在内层源码声明，但 barrel 没有同名 `export type`；可推断 `React.ComponentProps<typeof CbacPicker>`，不能让报告正文把“源码 interface”当成 named public type import。[public barrel][cbac-public]

### 3.2 selection 和 UI 行为

`initialMarkingIds` 并非严格的一次性 default：内部 hook 比较新旧 **数组引用**，引用变化即 reset selectedIds；因此传每次新建的字面量数组会重置正在编辑的 selection。这是由 runtime 直接看到的行为，上游 `useCbacSelection` 测试也覆盖 ids prop 改变会 reset；EOS adapter 应稳定数组引用或显式控制初始化时机。[selection state][cbac-selection]、[reset test][cbac-selection-test]

DISJUNCTIVE category 的选择为单选替换，CONJUNCTIVE 为叠加/取消；`toggleMarking` 不识别的 id 返回原 selection。`computeMarkingStates` 中 selected 优先于 implied/disallowed，未出现在这些集合的 id 用 UI fallback NONE。这个纯工具不持有 server restrictions 或 authorization context。[selection utilities][cbac-selection-utils]

当前 category grid 采用4列×3行，超过12 markings 时显示11个加一个 overflow入口；category heading 使用 `useId`/aria group，描述和禁止选择提示用 Base UI tooltip。用户的“implied”项会显示括号样式；这些布局是内部实现，不是可调 rows/columns 的 public props。[CategoryMarkingGroup][cbac-category]、[MarkingButton][cbac-marking-button]

readOnly 的实际合约较窄：Picker 的 toggle handler 会 return；但 banner clear handler 没有 readOnly guard，仍可 clear 并通知。因此不要用 readOnly 表示“整个 selection 不可发生任何变更”，主文可准确写“禁止 marking toggle”。[Picker handlers][cbac-picker]

### 3.3 权限、限制与失败行为：关键结论

1. **`maxClassificationConstraint` 目前是提示信息。** Picker/Dialog 仅把该 prop 变成 `ConstraintCallout`，后者取最大 mark 的 banner colors 并渲染 MaxClassificationField；没有比较 current selection 与 max，也没有把 max 参数送到 restrictions hook，更不参与 confirm gate。源码与测试都显示提供 prop 即渲染 callout，不是只在超过限制时触发。报告正文不要把 JSDoc 的“capping”写成已执行的强制规则。[Picker][cbac-picker]、[Dialog][cbac-dialog]、[ConstraintCallout][cbac-constraint]、[callout test][cbac-picker-test]
2. **Dialog gate 是 UI 提示，不是权限保证。** `getSubmitDisabledReason` 首先在 isValid=true 时直接返回 undefined，再按 required/disallowed/user satisfaction 给原因；state hook 在 restrictions 未返回时 `isValid ?? true` 和 `userSatisfiesMarkings ?? true`。loading/error 没传入 confirm-disable 函数，所以不能宣称它在 pending/失败时自动 fail-closed。保存动作必须在 backend 再校验。[state defaults][cbac-state]、[gate][cbac-validation]、[Dialog wiring][cbac-dialog]
3. **confirm/callback 不执行提交。** `CbacPickerDialog` 的 handleConfirm 只调用 caller onConfirm(selectedIds)，父控制 close；inline Picker 的 onChange 和 BannerPopover 的 onChange 也只是 callback。组件没有自动调用 Ontology Action 或更新 marking assignment。[Dialog confirm][cbac-dialog]、[Picker toggle][cbac-picker]、[Popover confirm][cbac-popover]
4. **query-driven 配色/限制与视觉 state 会暂时不同步。** state hook 在新 banner 未到时保留上一个 bannerRef；isLoading 合并4组 query 状态、error 聚合多个错误，但包装层没有公开 retry prop。由源码可理解为尽量稳定展示，不应把旧 banner 当成新 selection 已被 server 接受的证据。[state hook][cbac-state]

尚未用实际身份校验分类限制、list分页完整性或server最终授权；这些不由 Storybook mock截图证明。上游测试源码覆盖 toggle/readonly toggle/clear/callout、initial ids reset、disjunctive/conjunctive、footer disable 与原因优先级；本次未运行这些 tests。[Picker tests][cbac-picker-test]、[selection tests][cbac-selection-test]、[footer tests][cbac-footer-test]

**EOS 建议：** Foundry 原生应用可优先用 wrappers，让 server 返回 markings/restrictions；EOS 自有 policy backend 可用 BasePicker/BaseBanner 复用视觉结构，adapter 明确提供 category、selected/implied/disallowed、required groups 与确认原因，再把持久化及权限审计放在 EOS 服务端。不能只复制 toggleMarking 就声称复现 Foundry CBAC。

## 4. 许可证和依赖差异

### 4.1 OSDK 分包

在组件发布 commit 的 `packages/*/package.json` 中逐包扫描到 95 个 manifests，全部 license 字段声明 `Apache-2.0`；44 个同时标 private。完整名称、source version、private flag 与每个 license 字段的源码行链接存于 [manifest 许可清单](evidence/osdk-package-license-inventory.json)。这个结果只覆盖该 commit 的 manifests，不把 docs/screenshot/商标或整个 Foundry 服务条款都纳入同一许可。关键可公开引用的分包如下。

| 包 | 该组件发布源码中的版本 | license 声明 | 依赖职责差异 |
| --- | --- | --- | --- |
| `@osdk/react-components` | 0.61.0 | Apache-2.0 | Base UI/icons、DnD、TanStack Table/Virtual、RHF、PDF/邮件/TIFF/XLSX/Markdown rendering；api/client/react 是 peers。[manifest][pkg-deps] |
| `@osdk/react` | 2.73.0 | Apache-2.0 | 轻量 React binding + aip-core + fast-deep-equal；api/client/React peers，foundry.admin/core optional peers。[manifest][react-pkg] |
| `@osdk/client` | 2.73.0 | Apache-2.0 | api/client.unstable、Foundry APIs、shared net、RxJS、trie、WebSocket 等；不是 TanStack Query 或 Zustand 的 runtime。[manifest][client-pkg] |
| `@osdk/api` | 2.73.0 | Apache-2.0 | Type/contract 核心，另有 fetch-retry/tiny-invariant/type-fest/GeoJSON type 依赖。[manifest][api-pkg] |
| `@osdk/oauth` | 1.14.0 | Apache-2.0 | oauth4webapi、tiny-invariant、typescript-event-target；auth 包独立版本线。[manifest][oauth-pkg] |
| `@osdk/generator` | 2.73.0 | Apache-2.0 | code generation 侧 api/ontology/converters、Prettier 等；应区别浏览器 bundle。[manifest][generator-pkg] |
| `@osdk/foundry-sdk-generator` | 2.73.0 | Apache-2.0 | generator/client 与 Rollup/ts-morph/TypeScript/CLI options 组合。[manifest][foundry-generator-pkg] |
| `@osdk/aip-core` | 0.12.0 | Apache-2.0 | language-models + client/provider peers，是额外 AI 域。[manifest][aip-pkg] |
| `@osdk/cbac-components` | 0.11.0 | Apache-2.0 | Base UI/icons，react/react-components peers；不要把这个独立包与 react-components/experimental/cbac-picker 当同名完全等价面。[manifest][cbac-pkg] |
| `@osdk/react-components-storybook` | 0.60.0，private | Apache-2.0 | faux/MSW 辅助环境；不是应安装的产品 npm API。[manifest][storybook-pkg] |

上述 2.73.0 是 **组件发布源码快照中版本**，研究日 api/client/react 的 npm latest 为 2.75.0，详见[发布版本矩阵](README.md)。发布 `react-components` tarball 把 workspace aip-core 改写成 `0.12.0`，把 dev api/client/react 改写成 `2.73.0`；这也说明 monorepo `workspace:*` 不是 consumer 看到的依赖表达式。[npm manifest](https://registry.npmjs.org/@osdk/react-components/0.61.0)、[upstream manifest][pkg-deps]

### 4.2 UI 直接依赖声明的许可

以下版本从 **该 commit 的 pnpm-lock.yaml** 取出，再只读 npm registry 获取指定版本 `license` 字段；它们不是每个 EOS consumer 在今天解析 ranges 后必然得到的版本。完整 20 项证据与原始 registry URL 已存 [components-dependency-license-metadata.json](evidence/components-dependency-license-metadata.json)。没有下载/执行它们的代码，没有完成传递依赖 NOTICE/SBOM 审计。[锁文件][component-lock]

| 依赖及已查版本 | registry license 字段 | 第一方声明 |
| --- | --- | --- |
| Base UI React 1.0.0 | MIT | [npm registry](https://registry.npmjs.org/@base-ui%2Freact/1.0.0) |
| Blueprint icons 6.8.0 | Apache-2.0 | [npm registry](https://registry.npmjs.org/@blueprintjs%2Ficons/6.8.0) |
| dnd-kit core 6.3.1/sortable 10.0.0/utilities 3.2.2 | MIT | [core](https://registry.npmjs.org/@dnd-kit%2Fcore/6.3.1)、[sortable](https://registry.npmjs.org/@dnd-kit%2Fsortable/10.0.0)、[utilities](https://registry.npmjs.org/@dnd-kit%2Futilities/3.2.2) |
| TanStack react-table 8.21.3/react-virtual 3.13.17 | MIT | [table](https://registry.npmjs.org/@tanstack%2Freact-table/8.21.3)、[virtual](https://registry.npmjs.org/@tanstack%2Freact-virtual/3.13.17) |
| PDF.js dist 4.8.69 | Apache-2.0 | [npm registry](https://registry.npmjs.org/pdfjs-dist/4.8.69) |
| postal-mime 2.7.4 | MIT-0 | [npm registry](https://registry.npmjs.org/postal-mime/2.7.4) |
| react-hook-form 7.71.2 / react-day-picker 8.10.1 | MIT | [RHF](https://registry.npmjs.org/react-hook-form/7.71.2)、[day-picker](https://registry.npmjs.org/react-day-picker/8.10.1) |
| react-markdown 9.1.0 / remark-gfm 4.0.1 | MIT | [markdown](https://registry.npmjs.org/react-markdown/9.1.0)、[gfm](https://registry.npmjs.org/remark-gfm/4.0.1) |
| UTIF 3.1.0 | MIT | [npm registry](https://registry.npmjs.org/utif/3.1.0) |
| xlsx-republish 0.20.3 | Apache-2.0 | [npm registry](https://registry.npmjs.org/xlsx-republish/0.20.3)；这是 republisher 包，不应在报告里悄悄改名成官方 `xlsx@0.20.3` |

Blueprint core 本地复制的 CSS 在源注释写明来源和版本；相应 Blueprint 6.11.3 tag 的 LICENSE 为 Apache-2.0。token 文件本身不再作为 package dependency 出现在 npm manifest，源代码拷贝仍应纳入归属/许可检查。[copy provenance][blueprint-copy]、[Blueprint source license](https://github.com/palantir/blueprint/blob/%40blueprintjs%2Fcore%406.11.3/LICENSE)

### 4.3 对 EOS 复用的许可建议

**官方条款事实：** Apache-2.0 §§2–4 允许按条件使用、改编、分发；分发时需随附许可文本、对修改文件加明显修改通知、保留适用归属声明，并在上游带 NOTICE 时保留相关 NOTICE。§6 不授予一般商标/产品名使用许可。授权是针对 Work，不是授予访问 Foundry 服务或客户 Ontology 的权限。[Apache 官方条款](https://www.apache.org/licenses/LICENSE-2.0)

**建议：** EOS 若仅 npm 引入并写 adapter，可锁版本与 license inventory；若复制 `BaseTable`/tokens/hooks，应记录上游 commit、版权/许可与修改清单，另查实际分发依赖及 NOTICE。品牌 token 和交互思想可借鉴，但 Palantir logo、原 Storybook 截图、客户数据、服务访问不能用“源码 Apache-2.0”统一覆盖。后半为工程/内容治理建议，不冒充法律结论。

## 5. 已做核验与未完成事项

已做：read-only checkout HEAD 核验；源码和已发布 JS/类型/CSS 边界比对；相关主题/public/tokens/main-vs-release diff；npm 根入口实际 import 证明空 exports；上游测试用例阅读；指定 lockfile 版本 direct dependency registry 许可声明查询；未运行 Foundry、生产 Ontology、外部 Action。

未做：React17 fixture、全组件 React19/SSR/浏览器兼容矩阵、局部 target 文档例子的运行复现、完整 transitive dependencies license/NOTICE audit、host AntD unlayered CSS 回归。上述均应按“未验证”或“源码推断”写进报告正文。

本地已发布产物证据（供主 `checks.md` 选择记录）：

| 文件 | 字节 | SHA-256 |
| --- | ---: | --- |
| `package.json` | 15344 | `1ba2a31120207a8c7390d7bae215e8e5516750f9c89f0d3137d1b9fa259d8e6d` |
| `build/esm/index.js` | 754 | `64954913092d92964d4fac79a66ea4ea8854d6711628ee214bfefa3ff9aa041f` |
| `build/types/index.d.ts` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `build/esm/public/primitives.js` | 965 | `abce2206bb2fa9673466944b040c632b00efc04fdc92eb3cc32220f73e385273` |
| `build/esm/public/experimental/theme.js` | 796 | `c55af4fe1abace1b25477ebda93e8b576af2ee4f805f4eaf522d5b48b95b2280` |
| `build/browser/styles.css` | 380284 | `8bfb7a92616c48d278564bc10cfd1eae70b96227103d88409f42c7f30e5124e1` |

[root-index]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/index.ts#L17-L18
[pkg-exports]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/package.json#L9-L278
[pkg-wildcard]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/package.json#L280-L289
[pkg-license]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/package.json#L2-L7
[pkg-deps]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/package.json#L307-L353
[pkg-files]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/package.json#L358-L376
[primitives]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/primitives.ts#L17-L30
[readme-primitives]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/README.md#L237-L250
[agents-exports]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/AGENTS.md#L39-L58
[claude-primitives]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/CLAUDE.md#L44-L49
[promotion]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/CHANGELOG.md#L34-L78
[readme-beta]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/README.md#L1-L7
[sb-tier]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/.storybook/main.ts#L45-L64
[brand-alpha]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/.storybook/addons/brand-theme-extractor/export.ts#L102-L129
[experimental-aggregate]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental.ts#L17-L30
[table-shim]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/object-table.ts#L20-L33
[form-shim]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/action-form.ts#L17-L32
[markdown-shim]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/markdown-renderer.ts#L17-L42
[tiff-shim]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/tiff-renderer.ts#L17-L39
[table-public]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/object-table.ts#L17-L161
[filter-public]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/filter-list.ts#L17-L67
[form-public]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/action-form.ts#L17-L53
[pdf-public]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/pdf-viewer.ts#L17-L119
[document-public]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/document-viewer.ts#L17-L25
[column-defs]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/hooks/useColumnDefs.tsx#L17-L44
[filter-state]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/filter-list/hooks/useFilterListState.ts#L17-L49
[base-table]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/Table.tsx#L78-L98
[metrics]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/util/withOsdkMetrics.ts#L17-L36
[action-button]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/action-button/ActionButton.tsx#L17-L50
[dialog]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/base-components/dialog/Dialog.tsx#L17-L73
[theme-export]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/theme.ts#L17-L26
[theme-provider]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/theme/OsdkThemeProvider.tsx#L27-L127
[theme-dom]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/theme/OsdkThemeProvider.tsx#L90-L105
[theme-hook]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/theme/useOsdkTheme.ts#L36-L42
[theme-system]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/theme/useSystemTheme.ts#L17-L56
[theme-tests]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/theme/__tests__/OsdkThemeProvider.test.tsx#L114-L280
[theme-throw-test]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/theme/__tests__/OsdkThemeProvider.test.tsx#L284-L299
[theme-scope]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/OsdkThemeProvider.md#L202-L221
[portal-context]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/shared/PortalContainerContext.tsx#L21-L42
[readme-css]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/README.md#L71-L120
[css-build]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/scripts/build-css.mjs#L90-L147
[token-entry]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/tokens.css#L1-L35
[base-tokens]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/tokens/base-tokens/base.css#L1-L86
[blueprint-copy]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/tokens/base-tokens/blueprint-design-tokens.css#L1-L6
[dark-tokens]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/tokens/base-tokens/dark.css#L1-L106
[table-tokens]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/tokens/component-tokens/table.css#L1-L89
[filter-tokens]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/tokens/component-tokens/filter-list.css#L1-L70
[css-doc-old]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/CSSVariables.md#L63-L77
[component-lock]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/pnpm-lock.yaml#L5113-L5257
[react-pkg]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react/package.json#L1-L117
[client-pkg]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/client/package.json#L1-L116
[api-pkg]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/api/package.json#L1-L70
[oauth-pkg]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/oauth/package.json#L1-L46
[generator-pkg]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/generator/package.json#L1-L55
[foundry-generator-pkg]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/foundry-sdk-generator/package.json#L1-L63
[aip-pkg]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/aip-core/package.json#L1-L64
[cbac-pkg]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/cbac-components/package.json#L1-L62
[storybook-pkg]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/package.json#L1-L35
[cbac-public]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/cbac-picker.ts#L17-L52
[cbac-picker]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPicker.tsx#L26-L124
[cbac-dialog]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacPickerDialog.tsx#L25-L115
[cbac-banner]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBanner.tsx#L17-L54
[cbac-popover]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/CbacBannerPopover.tsx#L32-L125
[cbac-base-picker]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPicker.tsx#L17-L116
[cbac-base-dialog]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacPickerDialog.tsx#L24-L72
[cbac-base-banner]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/BaseCbacBanner.tsx#L27-L117
[cbac-max-field]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/MaxClassificationField.tsx#L24-L52
[cbac-constraint]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/ConstraintCallout.tsx#L17-L46
[cbac-selection]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/useCbacSelection.ts#L34-L80
[cbac-selection-utils]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/utils/selectionLogic.ts#L24-L123
[cbac-category]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/CategoryMarkingGroup.tsx#L28-L134
[cbac-marking-button]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/MarkingButton.tsx#L47-L117
[cbac-footer]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/CbacPickerDialogFooter.tsx#L30-L73
[cbac-validation]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/utils/validationMessages.ts#L19-L47
[cbac-state]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/useCbacPickerState.ts#L63-L181
[cbac-restrictions]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react/src/new/platform-apis/admin/useCbacMarkingRestrictions.ts#L61-L109
[cbac-banner-hook]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react/src/new/platform-apis/admin/useCbacBanner.ts#L60-L103
[cbac-picker-test]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/__tests__/CbacPicker.test.tsx#L83-L132
[cbac-selection-test]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/__tests__/useCbacSelection.test.ts#L77-L125
[cbac-footer-test]: https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/cbac-picker/base/__tests__/CbacPickerDialogFooter.test.tsx#L22-L47
