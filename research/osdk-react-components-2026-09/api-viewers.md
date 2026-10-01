# Viewer 参数图鉴：npm @osdk/react-components 0.61.0

核验日期：2026-10-01。精确 TS 类型从实际 tarball 的 `build/types/*ViewerApi.d.ts` 提取并展开 Omit 继承；固定发布源码提交 `37cfd38676bf04edaef5847e929d914ea214c149`。本页展开主/Base viewer 与七个PDF公开构件的props参数，并核验default/alias/state归属的相关实现分支；PDF hooks仅提供公开symbol、类型别名、职责及源码索引，未完整展开各hook的输入字段、返回字段或默认行为。本页不提供新增viewer端到端运行证据。

表中“可选”遵循 `?`，不是“有内容也不需传”的业务保证；未写明确 default 的属性列作 undefined。所有外层 viewer 的 `media: Media` 来自 `@osdk/api`，不是 URL string。Base 接收宿主已经获取的字节、URL、文本或解析对象。`className` 是每个表中显式列出的共享呈现属性。没有一个可通用继承 HTMLElementProps 的 shared interface；除 DocumentViewer 外，各主组件通过 Omit<Base…Props, 内容字段> 继承剩余属性。

不会因 interface 没列 children/style 就自动把它们补为组件 API。PDF 的 React ref 是组件签名附加项，单独标记，不与 BasePdfViewerProps 混淆。

## 1. PDF：PdfViewer

入口：`@osdk/react-components/pdf-viewer`。[发布 props 源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/PdfViewerApi.ts#L149-L261)；[官方组件文档](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/PdfViewer.md)。

PDF 页码、缩放、自适应与侧栏展开均由内部 state 管理；default* / initial* 只作为初始种子。顶层没有 currentPage、scale、onPageChange、onScaleChange 或 sidebarOpen 的受控 prop。要组装外部状态驱动工具栏，请使用后文 building blocks / hooks。

### PdfViewerProps（23 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `media` | `Media` | 必填 | 无；必须提供 | 提供 OSDK Media，主组件据此读取或解析内容。 | 数据输入；没有 media/onMediaChange 受控事件对 |
| `annotations` | `PdfAnnotation[]` | 可选 | [] | 传入要覆盖在页面上的标注集合。 | 外部覆盖层数据；与 PDF.js 原生 highlight 编辑事件分开 |
| `onAnnotationClick` | `(annotation: PdfAnnotation) => void` | 可选 | undefined | 读取用户点击的覆盖层标注。 | 事件：输出 PdfAnnotation |
| `onDownload` | `(result: PdfDownloadResult) => void` | 可选 | undefined | 获得下载成功文件名或下载失败信息。 | 事件：输出判别联合 PdfDownloadResult |
| `enableHighlight` | `boolean` | 可选 | false | 显示高亮模式入口；高亮操作由内部编辑状态处理。 | 功能开关；不是 highlightModeActive 受控值 |
| `onTextHighlight` | `(event: PdfTextHighlightEvent) => void` | 可选 | undefined | 收到新建文本高亮的页码、矩形、文字、颜色及 editorId。 | 事件；宿主自行保存 |
| `onHighlightDelete` | `(event: PdfTextHighlightEvent) => void` | 可选 | undefined | 收到原生编辑器删除的高亮信息。 | 事件；宿主自行同步持久化 |
| `defaultPage` | `number` | 可选 | 1 | 设置初始页，页码从 1 开始。 | 非受控初始值 |
| `initialPage` | `number` | 可选 | 回退 1；defaultPage 优先 | defaultPage 的弃用旧名称。 | deprecated；非受控初始值 |
| `defaultScale` | `number` | 可选 | 1.0 | 设置初始缩放倍数；启用 auto-size 时由容器宽度决定显示缩放。 | 非受控初始值 |
| `initialScale` | `number` | 可选 | 回退 1.0；defaultScale 优先 | defaultScale 的弃用旧名称。 | deprecated；非受控初始值 |
| `defaultAutoSize` | `boolean` | 可选 | false | 初始是否按容器宽度自适应；手动缩放会关闭此模式。 | 非受控初始值 |
| `initialAutoSize` | `boolean` | 可选 | 回退 false；defaultAutoSize 优先 | defaultAutoSize 的弃用旧名称。 | deprecated；非受控初始值 |
| `defaultSidebarOpen` | `boolean` | 可选 | false | 初始是否展开侧栏。 | 非受控初始值 |
| `initialSidebarOpen` | `boolean` | 可选 | 回退 false；defaultSidebarOpen 优先 | defaultSidebarOpen 的弃用旧名称。 | deprecated；非受控初始值 |
| `enableDownload` | `boolean` | 可选 | false | 显示工具栏下载按钮。 | 功能开关 |
| `downloadFileName` | `string` | 可选 | URL 推导；最终 document.pdf | 指定工具栏下载文件名。 | 呈现/下载选项；主 PdfViewer 会转成字节源，默认回退不能假定来自 Media 原名 |
| `sidebarMode` | `SidebarMode` | 可选 | "thumbnails" | 选择缩略图或目录侧栏。 | prop 变化同步到内部 state；内部亦能切换，无顶层 onSidebarModeChange 配对 |
| `outlineIcons` | `Partial<Record<number, React.ComponentType>>` | 可选 | undefined | 按目录深度提供图标组件，key=0 对应顶层。 | 呈现配置 |
| `formData` | `Record<string, PdfFormFieldValue>` | 可选 | undefined | 按字段名提供 PDF 表单填充值。 | 装载/annotation layer 填充数据；非标准 value/onChange 完全受控表单 |
| `onFormSubmit` | `(data: Record<string, PdfFormFieldValue>) => void` | 可选 | undefined | 点击表单保存入口时读取当前全部字段。 | 事件；PDF 表单保存回调，不是 Ontology Action 提交 |
| `onFormChange` | `(fieldName: string, value: PdfFormFieldValue) => void` | 可选 | undefined | 读取单个表单字段的新值。 | 事件：fieldName + PdfFormFieldValue |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |

### BasePdfViewerProps（23 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `src` | `PdfSource` | 必填 | 无；必须提供 | 指定 PDF URL、内存二进制或 Blob；类型别名见后文。 | 数据输入 |
| `annotations` | `PdfAnnotation[]` | 可选 | [] | 传入要覆盖在页面上的标注集合。 | 外部覆盖层数据；与 PDF.js 原生 highlight 编辑事件分开 |
| `onAnnotationClick` | `(annotation: PdfAnnotation) => void` | 可选 | undefined | 读取用户点击的覆盖层标注。 | 事件：输出 PdfAnnotation |
| `onDownload` | `(result: PdfDownloadResult) => void` | 可选 | undefined | 获得下载成功文件名或下载失败信息。 | 事件：输出判别联合 PdfDownloadResult |
| `enableHighlight` | `boolean` | 可选 | false | 显示高亮模式入口；高亮操作由内部编辑状态处理。 | 功能开关；不是 highlightModeActive 受控值 |
| `onTextHighlight` | `(event: PdfTextHighlightEvent) => void` | 可选 | undefined | 收到新建文本高亮的页码、矩形、文字、颜色及 editorId。 | 事件；宿主自行保存 |
| `onHighlightDelete` | `(event: PdfTextHighlightEvent) => void` | 可选 | undefined | 收到原生编辑器删除的高亮信息。 | 事件；宿主自行同步持久化 |
| `defaultPage` | `number` | 可选 | 1 | 设置初始页，页码从 1 开始。 | 非受控初始值 |
| `initialPage` | `number` | 可选 | 回退 1；defaultPage 优先 | defaultPage 的弃用旧名称。 | deprecated；非受控初始值 |
| `defaultScale` | `number` | 可选 | 1.0 | 设置初始缩放倍数；启用 auto-size 时由容器宽度决定显示缩放。 | 非受控初始值 |
| `initialScale` | `number` | 可选 | 回退 1.0；defaultScale 优先 | defaultScale 的弃用旧名称。 | deprecated；非受控初始值 |
| `defaultAutoSize` | `boolean` | 可选 | false | 初始是否按容器宽度自适应；手动缩放会关闭此模式。 | 非受控初始值 |
| `initialAutoSize` | `boolean` | 可选 | 回退 false；defaultAutoSize 优先 | defaultAutoSize 的弃用旧名称。 | deprecated；非受控初始值 |
| `defaultSidebarOpen` | `boolean` | 可选 | false | 初始是否展开侧栏。 | 非受控初始值 |
| `initialSidebarOpen` | `boolean` | 可选 | 回退 false；defaultSidebarOpen 优先 | defaultSidebarOpen 的弃用旧名称。 | deprecated；非受控初始值 |
| `enableDownload` | `boolean` | 可选 | false | 显示工具栏下载按钮。 | 功能开关 |
| `downloadFileName` | `string` | 可选 | URL 推导；最终 document.pdf | 指定工具栏下载文件名。 | 呈现/下载选项；主 PdfViewer 会转成字节源，默认回退不能假定来自 Media 原名 |
| `sidebarMode` | `SidebarMode` | 可选 | "thumbnails" | 选择缩略图或目录侧栏。 | prop 变化同步到内部 state；内部亦能切换，无顶层 onSidebarModeChange 配对 |
| `outlineIcons` | `Partial<Record<number, React.ComponentType>>` | 可选 | undefined | 按目录深度提供图标组件，key=0 对应顶层。 | 呈现配置 |
| `formData` | `Record<string, PdfFormFieldValue>` | 可选 | undefined | 按字段名提供 PDF 表单填充值。 | 装载/annotation layer 填充数据；非标准 value/onChange 完全受控表单 |
| `onFormSubmit` | `(data: Record<string, PdfFormFieldValue>) => void` | 可选 | undefined | 点击表单保存入口时读取当前全部字段。 | 事件；PDF 表单保存回调，不是 Ontology Action 提交 |
| `onFormChange` | `(fieldName: string, value: PdfFormFieldValue) => void` | 可选 | undefined | 读取单个表单字段的新值。 | 事件：fieldName + PdfFormFieldValue |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |

组件签名另附 `React.RefAttributes<PdfViewerHandle>`：

| 附加属性 | 精确 TS 类型 | Required | Default | 中文用途 / 模式 |
|---|---|---|---|---|
| `ref` | `React.RefAttributes<PdfViewerHandle>["ref"]` | 可选 | undefined | 命令式 `scrollToPage(page)` / `deleteHighlight(editorId)`；仅由 Base forwardRef 签名公开 |

[BasePdfViewer forwardRef / handle](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/BasePdfViewer.tsx#L37-L93)。主 PdfViewer 发布声明是普通函数，`PdfViewerProps` 没有 ref，也没有转交 ref 的签名，不按 handle 注释把 ref 当成主组件 prop。[主 PdfViewer 签名与转交](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/PdfViewer.tsx#L32-L103)。

默认值/别名优先级：[Base 默认开关与 default ?? initial](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/BasePdfViewer.tsx#L40-L75)；[page / scale / autoSize 种子](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfViewerCore.ts#L91-L107)；[sidebar 种子与 mode 同步](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfViewerState.ts#L84-L127)。表单填充时点见[formData ref / annotation layer 填充](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfFormFields.ts#L276-L302)；不据 onFormChange 推断它是常规 value/onChange 完全受控模型。

## 2. TIFF：TiffViewer

入口：`@osdk/react-components/tiff-viewer`。[发布 props 源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/images/tiff-viewer/TiffViewerApi.ts#L19-L38)；[官方组件文档](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/TiffViewer.md)。

Base 的 src/content 在发布声明中均可选，是旧别名兼容造成的宽松类型；两者都没有时result为undefined，组件渲染空容器，仅解码成功后才创建canvas。主 TiffViewer 不接受 src/content，只接受 Media。[无输入与渲染分支](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/images/tiff-viewer/BaseTiffViewer.tsx#L124-L154)

### TiffViewerProps（3 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `media` | `Media` | 必填 | 无；必须提供 | 提供 OSDK Media，主组件据此读取或解析内容。 | 数据输入；没有 media/onMediaChange 受控事件对 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |
| `onError` | `() => void` | 可选 | undefined | 通知图片/视频加载或 TIFF 解码失败；签名不携带 Error 对象。 | 错误事件；不代表外层 Media 读取失败都有此回调 |

### BaseTiffViewerProps（4 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `src` | `Uint8Array` | 可选 | undefined；实际需字节内容 | 直接提供 TIFF 二进制。 | 输入属性；src ?? content，src 优先 |
| `content` | `Uint8Array` | 可选 | undefined | src 的弃用旧名称。 | deprecated；兼容回退 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |
| `onError` | `() => void` | 可选 | undefined | 通知图片/视频加载或 TIFF 解码失败；签名不携带 Error 对象。 | 错误事件；不代表外层 Media 读取失败都有此回调 |

[src ?? content 与 onError 分支](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/images/tiff-viewer/BaseTiffViewer.tsx#L124-L143)。

## 3. Markdown：MarkdownViewer

入口：`@osdk/react-components/markdown-viewer`。[发布 props 源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/markdown-viewer/MarkdownViewerApi.ts#L19-L32)；[官方组件文档](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/MarkdownViewer.md)。

两者都是展示组件，没有受控编辑器 value/onChange 接口；Base 接收文本，主组件接收 Media。

### MarkdownViewerProps（2 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `media` | `Media` | 必填 | 无；必须提供 | 提供 OSDK Media，主组件据此读取或解析内容。 | 数据输入；没有 media/onMediaChange 受控事件对 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |

### BaseMarkdownViewerProps（2 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `content` | `string` | 必填 | 无；必须提供 | 直接提供 Markdown 文本。 | 数据输入；无编辑事件 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |

## 4. 统一文档：DocumentViewer

入口：`@osdk/react-components/document-viewer`。[发布 props 源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/document-viewer/DocumentViewerApi.ts#L24-L72)；[官方组件文档](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/DocumentViewer.md)。

实际公开入口只有 DocumentViewer 与 DocumentViewerProps/ViewerType，没有 BaseDocumentViewer。嵌套 props 仅有 PDF、Image、Video、TIFF 四组；Markdown/Email/Spreadsheet/XML 分支没有对应的顶层 nested props。

### DocumentViewerProps（10 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `media` | `Media` | 必填 | 无；必须提供 | 提供 OSDK Media，主组件据此读取或解析内容。 | 数据输入；没有 media/onMediaChange 受控事件对 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |
| `mimeTypeOverride` | `string` | 可选 | media reference MIME | 覆盖自动选择 viewer 时使用的 MIME 类型。 | 外部路由输入；不是网络 Content-Type 改写 |
| `pdfViewerProps` | `Partial<Omit<BasePdfViewerProps, "src" \| "className">>` | 可选 | undefined | 把允许的 PDF 选项传给 PDF 分支。 | 嵌套配置；详情对应 BasePdfViewer 表，排除 src/className |
| `imageViewerProps` | `Partial<Omit<BaseImageViewerProps, "src" \| "className">>` | 可选 | undefined | 把 alt/onError 传给图片分支。 | 嵌套配置；排除 src/className |
| `videoViewerProps` | `Partial<Omit<BaseVideoViewerProps, "src" \| "className">>` | 可选 | undefined | 把 mimeType/onError 传给视频分支。 | 嵌套配置；排除 src/className |
| `tiffViewerProps` | `Partial<Omit<BaseTiffViewerProps, "src" \| "content" \| "className">>` | 可选 | undefined | 向 TIFF 分支传 onError。 | 嵌套配置；排除 src/content/className |
| `tiffRendererProps` | `Partial<Omit<BaseTiffViewerProps, "src" \| "content" \| "className">>` | 可选 | undefined | tiffViewerProps 的弃用别名。 | deprecated；tiffViewerProps 非 nullish 时优先，二者不合并 |
| `fileName` | `string` | 可选 | undefined | 提供文件名线索，辅助识别 MIME 不明确的 TIFF。 | 路由提示；不保证设置 PDF 下载名 |
| `enableTiffToPdf` | `boolean` | 可选 | false | 请求把多页 TIFF 经 MIO 转换后作为 PDF 展示。 | 功能开关；涉及平台转换能力，不是纯本地显示参数 |

路由 default / TIFF alias 的实现依据：[DocumentViewer](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/document-viewer/DocumentViewer.tsx#L95-L160)。嵌套 PDF 配置不能携带 Base 的 ref，因为 ref 并不属于 BasePdfViewerProps。

## 5. EML 邮件：EmailViewer

入口：`@osdk/react-components/email-viewer`。[发布 props 源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/email-viewer/EmailViewerApi.ts#L19-L51)；[官方组件文档](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/EmailViewer.md)。

Base 接收解析结构；content 优先于 email。没有外部受控 HTML/text 切换或展开状态 prop。

### EmailViewerProps（2 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `media` | `Media` | 必填 | 无；必须提供 | 提供 OSDK Media，主组件据此读取或解析内容。 | 数据输入；没有 media/onMediaChange 受控事件对 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |

### BaseEmailViewerProps（3 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `content` | `ParsedEmail` | 可选 | undefined；实际需解析结果 | 直接传 ParsedEmail，不是原始 EML 字符串。 | 数据输入；content ?? email，content 优先 |
| `email` | `ParsedEmail` | 可选 | undefined | content 的弃用旧名称。 | deprecated；兼容回退 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |

[content ?? email](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/email-viewer/BaseEmailViewer.tsx#L35-L43)。

## 6. 电子表格：SpreadsheetViewer

入口：`@osdk/react-components/spreadsheet-viewer`。[发布 props 源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/spreadsheet-viewer/SpreadsheetViewerApi.ts#L19-L48)；[官方组件文档](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/SpreadsheetViewer.md)。

Base 接收解析结构；content 优先于 spreadsheet。sheet 选择内部从 index=0 开始，没有 activeSheet/onSheetChange 受控 prop，也不是电子表格编辑器。

### SpreadsheetViewerProps（2 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `media` | `Media` | 必填 | 无；必须提供 | 提供 OSDK Media，主组件据此读取或解析内容。 | 数据输入；没有 media/onMediaChange 受控事件对 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |

### BaseSpreadsheetViewerProps（3 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `content` | `ParsedSpreadsheet` | 可选 | undefined；实际需解析结果 | 提供 ParsedSpreadsheet 的 sheets/rows。 | 数据输入；content ?? spreadsheet，content 优先 |
| `spreadsheet` | `ParsedSpreadsheet` | 可选 | undefined | content 的弃用旧名称。 | deprecated；兼容回退 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |

[内部 activeSheetIndex 与 content 回退](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/spreadsheet-viewer/BaseSpreadsheetViewer.tsx#L86-L95)。

## 7. 图片：ImageViewer

入口：`@osdk/react-components/image-viewer`。[发布 props 源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/images/image-viewer/ImageViewerApi.ts#L19-L36)；[官方组件文档](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/ImageViewer.md)。

没有公开 zoom/rotation/objectFit/尺寸或图像编辑状态；外层适合 Media，Base 适合宿主已有 URL。

### ImageViewerProps（4 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `media` | `Media` | 必填 | 无；必须提供 | 提供 OSDK Media，主组件据此读取或解析内容。 | 数据输入；没有 media/onMediaChange 受控事件对 |
| `alt` | `string` | 可选 | "" | 图片替代文字，辅助无障碍访问。 | 呈现属性 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |
| `onError` | `() => void` | 可选 | undefined | 通知图片/视频加载或 TIFF 解码失败；签名不携带 Error 对象。 | 错误事件；不代表外层 Media 读取失败都有此回调 |

### BaseImageViewerProps（4 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `src` | `string` | 必填 | 无；必须提供 | 提供图片 URL、object URL 或 data URL。 | 数据输入 |
| `alt` | `string` | 可选 | "" | 图片替代文字，辅助无障碍访问。 | 呈现属性 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |
| `onError` | `() => void` | 可选 | undefined | 通知图片/视频加载或 TIFF 解码失败；签名不携带 Error 对象。 | 错误事件；不代表外层 Media 读取失败都有此回调 |

## 8. 视频：VideoViewer

入口：`@osdk/react-components/video-viewer`。[发布 props 源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/video-viewer/VideoViewerApi.ts#L19-L36)；[官方组件文档](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/VideoViewer.md)。

没有公开 currentTime、paused、onTimeUpdate、controls/autoplay 的组件 prop；Base 在实现中启用原生 video controls。用这份精确类型判断支持面，不把 DOM video 全部属性套到它上。

### VideoViewerProps（4 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `media` | `Media` | 必填 | 无；必须提供 | 提供 OSDK Media，主组件据此读取或解析内容。 | 数据输入；没有 media/onMediaChange 受控事件对 |
| `mimeType` | `string` | 可选 | 未传键时 media MIME；显式 undefined 可覆盖为 undefined | 指定传给 video source 的 MIME 类型。 | 可覆盖源类型；实现先推导 mimeType 再 spread 调用方 props |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |
| `onError` | `() => void` | 可选 | undefined | 通知图片/视频加载或 TIFF 解码失败；签名不携带 Error 对象。 | 错误事件；不代表外层 Media 读取失败都有此回调 |

### BaseVideoViewerProps（4 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `src` | `string` | 必填 | 无；必须提供 | 提供视频 URL 或 object URL。 | 数据输入；播放控制由原生 video controls 提供 |
| `mimeType` | `string` | 可选 | undefined | 指定 video source 的 MIME 类型，例如 video/mp4。 | 呈现/解码提示 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |
| `onError` | `() => void` | 可选 | undefined | 通知图片/视频加载或 TIFF 解码失败；签名不携带 Error 对象。 | 错误事件；不代表外层 Media 读取失败都有此回调 |

[主 Media MIME 回退](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/video-viewer/VideoViewer.tsx#L36-L69)；[Base 原生 controls](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/video-viewer/BaseVideoViewer.tsx#L24-L35)。

## 9. XML：XmlViewer

入口：`@osdk/react-components/xml-viewer`。[发布 props 源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/xml-viewer/XmlViewerApi.ts#L19-L30)；[官方组件文档](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/XmlViewer.md)。

Base 接收原始 XML 字符串；没有公开 XML tree、fold state 或编辑 onChange 事件。

### XmlViewerProps（2 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `media` | `Media` | 必填 | 无；必须提供 | 提供 OSDK Media，主组件据此读取或解析内容。 | 数据输入；没有 media/onMediaChange 受控事件对 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |

### BaseXmlViewerProps（2 个声明属性）

| 属性 | 精确 TS 类型 | Required | Default | 中文用途 | 事件 / 状态模式 |
|---|---|---|---|---|---|
| `content` | `string` | 必填 | 无；必须提供 | 直接提供待展示的 XML 文本。 | 数据输入；无编辑事件 |
| `className` | `string` | 可选 | undefined | 为组件根容器追加样式类。 | 呈现属性 |

## 10. 公开数据类型 / 事件 payload

这些类型与前述 props 同处发布 Api 声明，以下是类型结构的中文索引，不是验证器或 backend 保存协议。

| 公开类型 | 精确结构 / 关键字段 | 中文用途 |
|---|---|---|
| `PdfSource` | `string \| ArrayBuffer \| Uint8Array \| Blob` | Base PDF 数据源 |
| `SidebarMode` | `"thumbnails" \| "outline"` | PDF 侧栏模式 |
| `AnnotationType` | `"highlight" \| "underline" \| "comment" \| "pin" \| "custom"` | 覆盖层标注种类 |
| `PdfAnnotation` | `PdfStandardAnnotation \| PdfCustomAnnotation` | 公共联合；Standard 和 Base 具体 interface 未从公开 barrel 命名导出 |
| `PdfCustomAnnotation` | `type: "custom"; render: (props: PdfAnnotationRenderProps) => React.ReactNode`，继承 `id: string; page: number; rect: PdfRect; rects?: PdfRect[]; label?: string; color?: string` | 宿主自绘覆盖层；page 从 1 开始 |
| `PdfRect` | `x: number; y: number; width: number; height: number` | PDF points，页面左下角为原点 |
| `PdfAnnotationRenderProps` | `annotation: PdfAnnotation; scale: number; pageHeight: number; transform: number[]` | 自定义覆盖层坐标变换数据 |
| `PdfTextHighlightEvent` | `editorId: string; page: number; rects: PdfRect[]; selectedText: string; color: string` | 新建/删除高亮 callback payload |
| `PdfDownloadResult` | `{ success: true; filename: string } \| { success: false; error: Error }` | 下载结果判别联合 |
| `PdfFormFieldValue` | `string \| boolean \| string[]` | PDF 文本、布尔、列表字段值 |
| `PdfViewerHandle` | `scrollToPage: (page: number) => void; deleteHighlight: (editorId: string) => void` | Base PDF 命令式 handle；不是全部 viewer 的通用 handle |
| `OutlineItem` | `title: string; depth: number; pageNumber: number; bold: boolean; italic: boolean` | PDF 目录行 |
| `EmailAddress` | `name: string; address: string` | 邮件地址与显示名 |
| `ParsedEmail` | `subject: string \| undefined; from: EmailAddress \| undefined; to: readonly EmailAddress[]; cc: readonly EmailAddress[]; date: string \| undefined; html: string \| undefined; text: string \| undefined` | Base 邮件输入，包含字段本身均必填，部分字段值可以 undefined |
| `SheetData` | `name: string; rows: readonly (readonly string[])[]` | 一张 sheet，单元格都已转成字符串 |
| `ParsedSpreadsheet` | `sheets: readonly SheetData[]` | Base spreadsheet 输入 |
| `ViewerType` | `Pdf="pdf", Tiff="tiff", Image="image", Video="video", Markdown="markdown", Spreadsheet="spreadsheet", Email="email", Xml="xml", Unsupported="unsupported"` | 统一文档 viewer 的公开 enum |

[PDF 数据 / 事件类型](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/PdfViewerApi.ts#L20-L147)；[Email 类型](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/email-viewer/EmailViewerApi.ts#L19-L32)；[Spreadsheet 类型](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/spreadsheet-viewer/SpreadsheetViewerApi.ts#L19-L29)；[ViewerType](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/document-viewer/DocumentViewerApi.ts#L24-L34)。

## 11. PDF building blocks 与 hooks：公开接口索引

以下symbols均在 `@osdk/react-components/pdf-viewer` 的实际发布public declaration中。[固定公开barrel](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/pdf-viewer.ts#L17-L119)。本节覆盖七个公开构件和十三个公开hooks的symbol、相关类型别名及职责；构件props逐项见第13节。**hooks部分是索引，不是完整参数/返回值reference**：下表的简写不穷举输入/返回字段、required、默认值、effect时序或生命周期约束，使用时须读取链接中的固定声明与实现。内部组件/工具即使目录存在也不自动成为此入口的API。

| 公开 symbol | 公开 props / options / result alias | 中文职责及状态边界 | 固定定义路径 |
|---|---|---|---|
| `PdfViewerAnnotationLayer` | `PdfViewerAnnotationLayerProps` | 覆盖标注布局；宿主传 annotations/scale/transform/onAnnotationClick | [components/PdfViewerAnnotationLayer.tsx](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerAnnotationLayer.tsx#L28-L38) |
| `PdfViewerContent` | `PdfViewerContentProps` | 独立 PDF 内容；有 onPageChange/onScaleChange 通知，不把它误作顶层 Base 的同名参数 | [components/PdfViewerContent.tsx](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerContent.tsx#L36-L46) |
| `PdfViewerOutlineSidebar` | `PdfViewerOutlineSidebarProps` | 目录数据、当前页和模式都由宿主传值/回调 | [components/PdfViewerOutlineSidebar.tsx](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerOutlineSidebar.tsx#L27-L37) |
| `PdfViewerSearchBar` | `PdfViewerSearchBarProps` | query/匹配计数/当前索引输入 + 搜索导航回调 | [components/PdfViewerSearchBar.tsx](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerSearchBar.tsx#L22-L32) |
| `PdfViewerSidebar` | `PdfViewerSidebarProps` | 缩略图侧栏；document/页状态/模式由宿主提供 | [components/PdfViewerSidebar.tsx](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerSidebar.tsx#L32-L42) |
| `PdfViewerToolbar` | `PdfViewerToolbarProps` | 受控展示页码/scale/sidebar/highlight 并调用宿主命令 | [components/PdfViewerToolbar.tsx](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerToolbar.tsx#L39-L49) |
| `PdfViewerProvider` | `React.ComponentProps<typeof PdfViewerProvider>` | 输入 value: PdfViewerContextValue 与 children；内部 PdfViewerProviderProps 没从此 barrel 命名导出 | [PdfViewerContext.tsx](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/PdfViewerContext.tsx#L103-L113) |
| `usePdfViewerInstance` | `PdfViewerInstanceOptions → PdfViewerContextValue` | 组合式 viewer 实例，供 Provider 使用 | [PdfViewerContext.tsx](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/PdfViewerContext.tsx#L133-L143) |
| `usePdfViewerContext` | `() → PdfViewerContextValue` | 从 Provider 读取状态；Provider 外会抛错 | [PdfViewerContext.tsx](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/PdfViewerContext.tsx#L118-L128) |
| `usePdfViewerCore` | `UsePdfViewerCoreOptions → UsePdfViewerCoreResult` | 加载、页码、缩放、自适应及 PDF.js refs | [hooks/usePdfViewerCore.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfViewerCore.ts#L91-L101) |
| `usePdfViewerState` | `UsePdfViewerStateOptions → UsePdfViewerStateResult` | Core 上组合旋转、侧栏、搜索、目录与下载 | [hooks/usePdfViewerState.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfViewerState.ts#L84-L94) |
| `usePdfViewer` | `UsePdfViewerResult；参数为 refs/document/initialScale?/initialPage?` | 底层 PDF.js viewer/event bus/find controller 创建 | [hooks/usePdfViewer.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfViewer.ts#L36-L46) |
| `usePdfViewerSearch` | `UsePdfViewerSearchResult；参数为 eventBusRef/findControllerRef/document` | 内部 query/搜索导航 state 与 commands | [hooks/usePdfViewerSearch.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfViewerSearch.ts#L44-L54) |
| `usePdfFormFields` | `UsePdfFormFieldsOptions → UsePdfFormFieldsResult` | 字段填充/变化通知/读取保存数据 | [hooks/usePdfFormFields.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfFormFields.ts#L121-L131) |
| `usePdfHighlightMode` | `UsePdfHighlightModeOptions → UsePdfHighlightModeResult` | 高亮开关/事件/删除命令 | [hooks/usePdfHighlightMode.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfHighlightMode.ts#L83-L93) |
| `usePdfAnnotationPortals` | `AnnotationPortalTarget[]；参数为 refs/document` | 覆盖层每页定位目标 | [hooks/usePdfAnnotationPortals.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfAnnotationPortals.ts#L35-L45) |
| `usePdfAnnotationsByPage` | `(annotations: PdfAnnotation[]) → Record<number, PdfAnnotation[]>` | 按 page 分组覆盖层数据 | [hooks/usePdfAnnotationsByPage.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfAnnotationsByPage.ts#L24-L34) |
| `usePdfDocument` | `ReturnType<typeof usePdfDocument>；参数 src: PdfSource` | PDF 加载 document/numPages/loading/error；结果 interface 没从此 barrel 命名导出 | [hooks/usePdfDocument.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfDocument.ts#L60-L70) |
| `usePdfOutline` | `(document: PDFDocumentProxy \| undefined) → OutlineItem[]` | 目录数据提取 | [hooks/usePdfOutline.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfOutline.ts#L28-L38) |
| `usePdfViewerSync` | `ReturnType<typeof usePdfViewerSync>` | 同步 PDF.js 尺寸/页码；Options interface 没从此 barrel 命名导出 | [hooks/usePdfViewerSync.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfViewerSync.ts#L40-L50) |

`PdfViewerInstanceOptions` 精确继承：`Omit<BasePdfViewerProps, "className" | "downloadFileName"> & { highlightEnabled?: boolean }`。这意味着它含 src、上述 PDF 事件/种子/功能开关；`highlightEnabled` 是 `enableHighlight` 的弃用别名，后者设置时优先。[公开 options alias](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/PdfViewerApi.ts#L119-L137)。

这一索引不扩大导出边界：`PdfViewerProviderProps`、`UsePdfDocumentResult`、`UsePdfViewerSyncOptions`、`PdfAnnotationBase`、`PdfStandardAnnotation` 没在 `/pdf-viewer` public barrel 命名导出。消费者可用公开组件/函数的 `React.ComponentProps`、`Parameters` 或 `ReturnType` 推导，不建议直接依赖 internal path。

## 12. 对齐检查与使用限制

- 9 个 Api 源文件与对应 npm d.ts 的声明 token 对齐：忽略注释、空白、分号、声明专用 declare、leading union bar 与 trailing comma 后一致；不将 docs 文字作为运行行为证据。
- 覆盖 17 个公开主/Base props interface，共 97 个展开属性行；另附 Base PDF ref。没有为不存在的 BaseDocumentViewer 造表。
- 属性/类型/required 均来自实际 npm d.ts；默认值来自固定源码 JSDoc 与少量实现分支。PDF 尤其区分 default seed、外部覆盖层、form 回调与完全受控模型。
- Markdown、XML、Email、Spreadsheet的内容解析、安全及性能结论见[功能与限制专题](action-forms-and-viewers.md)；类型支持不等同解析成功，平台TIFF转换也不是离线能力。
- 本附录未执行生产API、Action或平台转换；hooks输入及返回结构尚未逐字段展开，不能把props覆盖范围延伸为所有PDF公开API的完整reference。

## 13. 七个 PDF 公开构件的 props 参数表

以下逐项展开第11节的七个公开组件props，不展开hooks的参数和返回结构。六个组件的props interface均在 `/pdf-viewer` barrel命名导出；`PdfViewerProvider`公开，但其 `PdfViewerProviderProps` 未在该barrel命名导出，可用 `React.ComponentProps<typeof PdfViewerProvider>` 得到参数类型。[构件导出](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/pdf-viewer.ts#L33-L57)、[Provider导出](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/pdf-viewer.ts#L88-L98)。

所有表中类型与 required 取自实际 npm 0.61.0 d.ts；未看到参数默认值时写“未声明”，不暗示调用方可以省略必传字段。七组参数没有 extends 或通用 HTML 属性继承，因此不自动增加 style、children、onClick 等字段；Provider 的 children 则有显式声明。PdfSource/PdfAnnotation/PdfFormFieldValue/OutlineItem/SidebarMode 详见第 10 节，PDFDocumentProxy 来自 pdfjs-dist，React.ReactNode/React.ComponentType 来自 React。

这些组件之间需要调用方接线。Provider 的实现仅将 value 传给 React context，六个构件仍读取各自 props；Provider 不会自动填入 currentPage、document、query 等必需参数。这里的受控状态指展示值由 props 提供、更新由宿主命令完成；Content 的 defaultPage/defaultScale 属初始化种子。以下为静态类型/源码核验，未新增浏览器交互测试。

### 13.1. PdfViewerAnnotationLayer

接口：`PdfViewerAnnotationLayerProps`；[完整 props 声明](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerAnnotationLayer.tsx#L28-L34)。

| 属性 | 精确 TS 类型 | Required | 默认 | 中文用途 | 事件与状态归属 |
| --- | --- | --- | --- | --- | --- |
| `annotations` | `PdfAnnotation[]` | 是 | 未声明 | 当前页要绘制的覆盖层集合。 | 外部数据输入；应按页切分后传入。 |
| `pageHeight` | `number` | 是 | 未声明 | 页面高度，提供给 custom annotation 渲染函数。 | 外部布局输入。 |
| `scale` | `number` | 是 | 未声明 | 页面缩放比例，提供给 custom annotation 渲染函数。 | 外部布局输入。 |
| `transform` | `number[]` | 是 | 未声明 | PDF 坐标到页面显示坐标的变换矩阵。 | 外部布局输入；TS 仅约束 number[]，不约束长度。 |
| `onAnnotationClick` | `(annotation: PdfAnnotation) => void` | 否 | 未声明 | 点击覆盖层后通知宿主，并传回该 annotation。 | 可选事件回调；不替宿主管理选中项。 |

该层直接遍历 annotations，custom 项额外收到 pageHeight/scale/transform；变换计算读取数组下标 0–5，因此调用方须提供有效矩阵，number[] 类型本身未保证六项。[变换计算](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerAnnotationLayer.tsx#L52-L59)、[custom 参数与层渲染](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerAnnotationLayer.tsx#L160-L224)。

### 13.2. PdfViewerContent

接口：`PdfViewerContentProps`；[完整 props 声明](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerContent.tsx#L36-L61)。

| 属性 | 精确 TS 类型 | Required | 默认 | 中文用途 | 事件与状态归属 |
| --- | --- | --- | --- | --- | --- |
| `src` | `PdfSource` | 是 | 未声明 | 底层 PDF 输入；可用地址或本地二进制类型。 | 资源输入；精确 PdfSource 联合见第 10 节。 |
| `annotations` | `PdfAnnotation[]` | 否 | `[]`（共享空数组） | 附加在 PDF 页面上的覆盖层集合。 | 外部覆盖层数据。 |
| `onAnnotationClick` | `(annotation: PdfAnnotation) => void` | 否 | 未声明 | 点击覆盖层时传回 annotation。 | 事件通知。 |
| `defaultPage` | `number` | 否 | `1`（JSDoc 声明） | 初始页码，从 1 开始。 | 初始化种子；没有配套 currentPage value prop。 |
| `initialPage` | `number` | 否 | 未声明 | 旧版初始页码参数，已弃用。 | 初始化种子；建议用 defaultPage。 |
| `defaultScale` | `number` | 否 | `1.0`（JSDoc 声明） | 初始缩放比例。 | 初始化种子；没有配套 scale value prop。 |
| `initialScale` | `number` | 否 | 未声明 | 旧版初始缩放参数，已弃用。 | 初始化种子；建议用 defaultScale。 |
| `onPageChange` | `(page: number) => void` | 否 | 未声明 | 内部当前页变化时通知宿主。 | 通知回调；首轮 effect 跳过通知，不构成受控页码协议。 |
| `onScaleChange` | `(scale: number) => void` | 否 | 未声明 | 内部缩放变化时通知宿主。 | 通知回调；首轮 effect 跳过通知，不构成受控缩放协议。 |
| `formData` | `Record<string, PdfFormFieldValue>` | 否 | 未声明 | 按字段名提供 PDF 表单初始数据。 | 加载/填充输入；不能仅凭此类型认定是完全受控表单。 |
| `onFormChange` | `(fieldName: string, value: PdfFormFieldValue) => void` | 否 | 未声明 | 字段变化时返回字段名和值。 | 字段事件通知，值类型见第 10 节。 |
| `className` | `string` | 否 | 未声明 | 根元素附加 CSS 类。 | 样式输入。 |

Content 自行调用 usePdfViewerCore、usePdfFormFields，未从 Provider 读取 viewer 实例。页码/缩放使用 default 参数及内部状态，两个通知回调明确跳过初始 effect。[初始化与回调实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerContent.tsx#L63-L123)。

### 13.3. PdfViewerOutlineSidebar

接口：`PdfViewerOutlineSidebarProps`；[完整 props 声明](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerOutlineSidebar.tsx#L27-L34)。

| 属性 | 精确 TS 类型 | Required | 默认 | 中文用途 | 事件与状态归属 |
| --- | --- | --- | --- | --- | --- |
| `outlineItems` | `OutlineItem[]` | 是 | 未声明 | 目录条目集合，包含层级和目标页。 | 外部目录输入；OutlineItem 结构见第 10 节。 |
| `currentPage` | `number` | 是 | 未声明 | 当前页码，用于计算活动目录项。 | 外部状态值。 |
| `onItemClick` | `(pageNumber: number) => void` | 是 | 未声明 | 点击目录项时请求跳到目标页。 | 宿主命令；接收 pageNumber。 |
| `sidebarMode` | `SidebarMode` | 是 | 未声明 | 侧栏当前模式。 | 外部状态值；联合类型见第 10 节。 |
| `onSidebarModeChange` | `(mode: SidebarMode) => void` | 是 | 未声明 | 请求切换侧栏模式。 | 与 sidebarMode 配对，由宿主提交更新。 |
| `outlineIcons` | `Partial<Record<number, React.ComponentType>>` | 否 | 未声明 | 按目录 depth 索引指定图标组件。 | 可选外部映射；React.ComponentType 来自 React。 |

活动目录项由 outlineItems/currentPage 计算；图标使用 outlineIcons?.[item.depth]，该 number key 是层级而非页码。[目录与图标实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerOutlineSidebar.tsx#L36-L81)。

### 13.4. PdfViewerSearchBar

接口：`PdfViewerSearchBarProps`；[完整 props 声明](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerSearchBar.tsx#L22-L30)。

| 属性 | 精确 TS 类型 | Required | 默认 | 中文用途 | 事件与状态归属 |
| --- | --- | --- | --- | --- | --- |
| `query` | `string` | 是 | 未声明 | 当前搜索字符串。 | 受控输入值；文本框 value 直接取 query。 |
| `totalMatches` | `number` | 是 | 未声明 | 当前匹配总数。 | 外部搜索状态。 |
| `currentMatchIndex` | `number` | 是 | 未声明 | 当前命中的零基索引；显示时加 1。 | 外部搜索状态。 |
| `onQueryChange` | `(query: string) => void` | 是 | 未声明 | 输入变更时提交新搜索字符串。 | 与 query 配对，由宿主更新 query/搜索结果。 |
| `onNext` | `() => void` | 是 | 未声明 | 请求转到下一处命中。 | 宿主命令；Enter 调用此命令。 |
| `onPrev` | `() => void` | 是 | 未声明 | 请求转到上一处命中。 | 宿主命令；Shift+Enter 调用此命令。 |
| `onClose` | `() => void` | 是 | 未声明 | 请求关闭搜索栏。 | 宿主命令；Escape 调用此命令。 |

该组件只展示并发送搜索命令，搜索执行与命中计数由调用方提供；query 为受控文本输入，currentMatchIndex 的显示偏移与键盘行为可在实现中核验。[输入、键盘与计数实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerSearchBar.tsx#L32-L83)。

### 13.5. PdfViewerSidebar

接口：`PdfViewerSidebarProps`；[完整 props 声明](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerSidebar.tsx#L32-L39)。

| 属性 | 精确 TS 类型 | Required | 默认 | 中文用途 | 事件与状态归属 |
| --- | --- | --- | --- | --- | --- |
| `document` | `PDFDocumentProxy` | 是 | 未声明 | 已加载的 PDF.js document，用于渲染缩略图。 | 外部对象输入；PDFDocumentProxy 来自 pdfjs-dist，非 Media 或 PdfSource。 |
| `numPages` | `number` | 是 | 未声明 | PDF 总页数，用于构建缩略图列表。 | 外部状态值。 |
| `currentPage` | `number` | 是 | 未声明 | 当前页码，从 1 开始；决定活动缩略图。 | 外部状态值。 |
| `onPageClick` | `(page: number) => void` | 是 | 未声明 | 点击缩略图时请求切换到该页。 | 宿主命令；回传从 1 开始的页码。 |
| `sidebarMode` | `SidebarMode` | 是 | 未声明 | 侧栏当前模式。 | 外部状态值。 |
| `onSidebarModeChange` | `(mode: SidebarMode) => void` | 是 | 未声明 | 请求更换侧栏模式。 | 与 sidebarMode 配对，由宿主更新。 |

document 是必需的外部 PDF.js 实例；此组件不接收 src，也不负责文档加载。虚拟缩略图索引转成页码时加 1，currentPage 定位时减 1。[缩略图实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerSidebar.tsx#L41-L98)。

### 13.6. PdfViewerToolbar

接口：`PdfViewerToolbarProps`；[完整 props 声明](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerToolbar.tsx#L39-L60)。

| 属性 | 精确 TS 类型 | Required | 默认 | 中文用途 | 事件与状态归属 |
| --- | --- | --- | --- | --- | --- |
| `currentPage` | `number` | 是 | 未声明 | 当前页码，从 1 开始。 | 外部页状态；文本框另有局部编辑草稿。 |
| `numPages` | `number` | 是 | 未声明 | 总页数，限定上一页、下一页及页码输入范围。 | 外部状态值。 |
| `scale` | `number` | 是 | 未声明 | 当前缩放比例，用于显示百分比。 | 外部状态值；不在工具栏内部更新 scale。 |
| `autoSize` | `boolean` | 是 | 未声明 | 当前是否自动适配尺寸。 | 外部状态值。 |
| `sidebarOpen` | `boolean` | 是 | 未声明 | 当前侧栏是否打开。 | 外部状态值。 |
| `onPageChange` | `(page: number) => void` | 是 | 未声明 | 上一页、下一页或有效输入页码后，请求切换页面。 | 与 currentPage 配对的宿主命令。 |
| `onZoomIn` | `() => void` | 是 | 未声明 | 请求放大。 | 宿主命令。 |
| `onZoomOut` | `() => void` | 是 | 未声明 | 请求缩小。 | 宿主命令。 |
| `onAutoSizeToggle` | `() => void` | 是 | 未声明 | 请求切换自动适配。 | 与 autoSize 配对的宿主命令。 |
| `onSearchOpen` | `() => void` | 是 | 未声明 | 请求打开搜索栏。 | 宿主命令。 |
| `onSidebarToggle` | `() => void` | 是 | 未声明 | 请求切换侧栏显隐。 | 与 sidebarOpen 配对的宿主命令。 |
| `onDownload` | `() => void` | 是 | 未声明 | 点击下载按钮后执行宿主提供的下载操作。 | 无参数命令；不同于主/Base viewer 返回 PdfDownloadResult 的同名事件。 |
| `enableDownload` | `boolean` | 是 | 未声明 | 是否显示下载按钮。 | 必传布尔配置；关闭按钮仍不取消 TS 对 onDownload 的必需约束。 |
| `onRotateLeft` | `() => void` | 是 | 未声明 | 请求向左旋转。 | 宿主命令；本接口没有 rotation value prop。 |
| `onRotateRight` | `() => void` | 是 | 未声明 | 请求向右旋转。 | 宿主命令；本接口没有 rotation value prop。 |
| `enableHighlight` | `boolean` | 是 | 未声明 | 是否显示高亮模式按钮。 | 必传布尔配置。 |
| `highlightModeActive` | `boolean` | 是 | 未声明 | 高亮模式是否已激活。 | 外部状态值。 |
| `onHighlightToggle` | `() => void` | 是 | 未声明 | 请求切换高亮模式。 | 与 highlightModeActive 配对的宿主命令。 |
| `enableFormSave` | `boolean` | 否 | `false` | 是否显示表单保存按钮。 | 可选配置。 |
| `onFormSave` | `() => void` | 否 | 未声明 | 点击表单保存按钮后执行宿主操作。 | 可选无参数命令；不同于主/Base onFormSubmit 接收字段数据。 |

工具栏将 currentPage 同步到局部页码输入草稿；命令仍交由宿主执行。enableFormSave=false 是解构默认值，其他必传 boolean 不能因工具栏按钮条件渲染而视为可选。[状态与页码实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerToolbar.tsx#L62-L144)；下载和表单保存只调用无参数回调：[按钮回调](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/components/PdfViewerToolbar.tsx#L287-L315)。

### 13.7. PdfViewerProvider

公开组件参数可表达为 `React.ComponentProps<typeof PdfViewerProvider>`，实际声明签名为 `({ value, children }: PdfViewerProviderProps) => React.ReactElement`。[参数与实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/PdfViewerContext.tsx#L97-L112)。

| 属性 | 精确 TS 类型 | Required | 默认 | 中文用途 | 事件与状态归属 |
| --- | --- | --- | --- | --- | --- |
| `value` | `PdfViewerContextValue` | 是 | 未声明 | 提供完整 viewer 状态、refs 与命令集合。 | 外部上下文对象；通常由公开 usePdfViewerInstance 生成，但 Provider 自己不创建 viewer。 |
| `children` | `React.ReactNode` | 是 | 未声明 | 需要共享 viewer 上下文的后代内容。 | React 子树；类型来自 React。 |

`PdfViewerContextValue`本身是公开命名类型，含document/loading/error、页码/缩放/旋转/侧栏、搜索、目录、下载、annotations、form/highlight状态与PDF.js refs；结构见[上下文value声明](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/PdfViewerContext.tsx#L40-L93)。此处只说明Provider的value prop，不逐字段展开该上下文或其组合hooks的返回结构。

覆盖范围：17 个主/Base props interface 共 97 行参数；七个 PDF 构件 props 共 58 行，名称、精确类型与可选标记逐字段对齐 npm d.ts。13 个公开 hooks 提供定位与用途索引，其输入和返回结构尚未逐字段展开。
