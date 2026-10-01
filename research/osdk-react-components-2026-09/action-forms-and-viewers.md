# ActionForm、文档媒体 viewers 与 AIP Chat 图鉴

研究时间：2026-10-01 UTC。组件证据固定于实际 npm `@osdk/react-components@0.61.0` 及其 provenance 对应发布 commit **`37cfd38676bf04edaef5847e929d914ea214c149`**。本研究未访问生产 Ontology、未执行 Foundry Action。主干 commit `e53b94ecd5de7cdd7e864d0daa04363bdad4db4c` 的 action-form/pdf/document/media/email/spreadsheet 相关目录与该发布 commit 内容一致。

以下“运行”表示实际实现，“类型”只表示声明，“测试源码”表示上游已有 mock/unit test 的覆盖意图，**本次未重跑整套 Vitest，不声称测试已通过，也不将 mock 当真实 Foundry 集成证明**。另直接以 Node 导入实际 npm tarball 的纯函数 `coerceFieldValue/getDefaultFieldDefinitions` 执行 6 条 assertion，验证整数截断、null→undefined、Date→ISO、boolean大小写拒绝、生成renderer/required、objectSet默认null；均通过，无网络或Action执行。

## 先给判断

1. **ActionForm 是轻量 OSDK Action 参数表单，不等同 Workshop/Foundry 的完整 Action 表单。** 已实现参数 metadata → UI、React Hook Form 客户端校验、受控/非受控值与提交回调；未实现后端预校验驱动的隐藏/禁用、allowed values、prefill、章节布局。官方指南直接列明这些缺口。[官方限制](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/docs/ActionForm.md#L93-L107)
2. **公开类型中有 `onValidationResponse`，运行组件没有消费它。** 属性被解构为 `_onValidationResponse`，实际只取 hook 的 `applyAction/isPending`；默认 submit 调用 `applyAction(formState)`，没有调用 `validateAction`。不能把这项类型当服务端预检、权限预检的已实现承诺。[运行实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionForm.tsx#L39-L58)、[提交实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionForm.tsx#L123-L138)、[类型](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L95-L107)
3. **viewers 的“数据层”不能概括为全部共享 `@osdk/react` 对象缓存。** 常规媒体读取直接调用 `Media.fetchContents()`，放到组件本地 state；该内部 hook 无全局 dedup、cache key 或 observable store。PDF 还保留自己的 effect。对象查询缓存能力不能自动外推到媒体字节下载。[媒体 hook](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/shared/hooks/useMediaContents.ts#L34-L92)、[PDF wrapper](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/PdfViewer.tsx#L27-L68)
4. **EOS 优先试用公开 Base 层与 PDF composable hooks；把 Foundry 数据/权限/Action adapter 放在应用边界。** 这是工程建议，依据是公开 BaseForm、Base*Viewer 与 PDF building-block/hooks 已提供；但 BaseForm 中 OBJECT_SELECT/OBJECT_SET 字段仍运行 OSDK hooks，因此 BaseForm 不是任意字段组合都能脱离 provider。[ActionForm 公开 barrel](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/action-form.ts#L17-L53)、[PDF barrel](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/pdf-viewer.ts#L17-L119)、[OSDK object fields](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/fields/ObjectSelectField.tsx#L95-L113)

## ActionForm：从 metadata 到提交

### 值、布局与生成字段

运行组件先通过 `useOsdkMetadata(actionDefinition)` 读取参数，使用 `getDefaultFieldDefinitions(metadata)` 生成字段，或完全采用传入的 `formFieldDefinitions`。传一个自定义字段不是局部覆盖，而是完整替换列表。metadata 失败通过 `onError({type:"unknown",error})` 发出；标题默认隐藏，打开后按 `formTitle → metadata.displayName → actionDefinition.apiName` 取值。[运行 data layer](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionForm.tsx#L52-L110)、[标题与 BaseForm 参数](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionForm.tsx#L153-L173)

| 参数类型 | 默认 renderer | 已实现的边界 |
| --- | --- | --- |
| string | TEXT_INPUT | label 来自 displayName 或参数 key |
| boolean | RADIO_BUTTONS | True/False，可自选 SWITCH |
| integer/double/long | NUMBER_INPUT | 数值输入，提交阶段再 coercion |
| datetime/timestamp | DATETIME_PICKER | UI 层 Date，提交 Date→ISO string；不自动套当前时间默认值 |
| attachment/mediaReference | FILE_PICKER | UI 选 File，见后文上传边界 |
| object | OBJECT_SELECT | 依据 referenced object API name 构造 minimal ObjectTypeDefinition |
| objectSet | OBJECT_SET | 只读摘要；默认 value 为 null，并非对象集选择/编辑器 |
| interface/struct、marking/geohash/geoshape/objectType/scenarioReference | UNSUPPORTED | 默认 disabled 提示，需 CUSTOM 或由应用提供受控值 |

该表是运行 switch 的实际结果，不是只从类型推测；`isRequired` 仅依据 `!param.nullable`。指南的 unsupported 表漏列 scenarioReference，但实现明确列入不支持分支。[运行字段生成](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/utils/getDefaultFieldDefinitions.ts#L28-L142)

受控类型是 discriminated union，传 `formState` 必须传 `onFormStateChange`。BaseForm 受控提交明确取父组件值而非 RHF 临时 store；用户输入经过 change callback 提醒父组件。[类型](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L30-L57)、[运行提交](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/BaseForm.tsx#L89-L110)、[测试源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/__tests__/BaseForm.test.tsx#L408-L499)

BaseForm 支持显式 `FormContentItem` field/section，section 可 collapse、1/2列、box/minimal 样式；ActionForm 自动生成的 formContent 全是平铺 field，没有读取 Action 作者的章节 metadata。[布局类型](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionFormApi.ts#L131-L155)、[自动布局实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionForm.tsx#L102-L110)

### 校验与错误 UX

底层是 `react-hook-form`，`useForm({mode:"onTouched", values/defaultValues})`；先 blur 校验，出现错误后 change 重校验。每个 FieldBridge 通过 useController 接受规则；Radio/Switch 选择立即 touched，Dropdown 的 blur 在 portal 场景单独处理。[BaseForm运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/BaseForm.tsx#L60-L80)、[FieldBridge](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/fields/FieldBridge.tsx#L46-L105)

本地规则为 required、数值 min/max、文本 minLength/maxLength、Date min/max、File maxSize，以及应用提供的 async `validate`。`onValidationError` 用于自定义错误文案；这不是 Action 后端校验结果。提交前 `trigger()`；不合法不执行 submit；尝试过提交后仍有字段错误会禁用按钮，修正后重开。Footer 显示 issue count/tooltip，pending 显示 Submitting 并禁用提交。[规则实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/utils/extractValidationRules.ts#L34-L141)、[提交 gate/状态](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/BaseForm.tsx#L89-L129)、[错误与按钮](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/BaseForm.tsx#L262-L343)

边界：UNSUPPORTED 字段虽然 visually disabled，RHF required 仍会校验，不会自动跳过必填参数；已有测试明确验证必填 unsupported 阻止提交，受控值则可提交但 UI 不显示该值。EOS 不能仅隐藏/禁用必填参数就期待 Action 正常执行。[测试源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/__tests__/BaseForm.test.tsx#L845-L915)

### React19 实际 npm 本地验证与布尔必填边界

新增有限运行证据：[独立 mock harness](probes/react19/README.md) 使用实际npm `@osdk/react-components@0.61.0`、`@osdk/api/client/react@2.75.0`、React/React DOM 19.3.0、React Hook Form 7.71.2（同发布lock）、Base UI 1.3.0，Testing Library React 16.3.3 + Vitest 5.0.3 + Happy DOM 20.14.5。4项组件行为测试全部通过，另6条npm纯函数断言通过；Vite8.3.1 client production build成功，有module directive/chunk size warning。版本与结果存于 [checks-summary.json](probes/react19/checks-summary.json)。所有组件测试全局fetch设为throwing spy并逐项assert未调用；没有provider、Ontology或Action执行。

**实测局限：required boolean RADIO 的有效业务值 False 被 required 规则视为未填。** 已选False，点击Submit会显示“This field is required”，issue数1、提交按钮disabled且onSubmit未调用；改选True后错误清除并提交。optional boolean False能够原样提交。普通必填文本与空文本的正/负向测试也符合预期。本研究另用真实浏览器独立复现并采集局部截图，不仅是Happy DOM断言。

代码链解释：默认metadata renderer将boolean做True/False选项，并将非nullable设为isRequired；规则生成直接把isRequired映射到RHF `required`，没有boolean存在性特殊处理。这是可报告的默认表单兼容边界。RHF7.71.2独立createFormControl也会把false判为required无效，所以**不能声称这是React19引发的缺陷**。EOS应在采用前对必填boolean单独制定存在性规则并回归False，但本研究未修改上游、未将建议修法验证成已实现方案。[默认boolean renderer](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/utils/getDefaultFieldDefinitions.ts#L45-L50)、[True/False选项](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/utils/getDefaultFieldDefinitions.ts#L104-L119)、[规则](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/utils/extractValidationRules.ts#L34-L41)、[RHF tag源码](https://github.com/react-hook-form/react-hook-form/blob/v7.71.2/src/logic/validateField.ts#L100-L118)。

“4项通过”表示上述包括边界复现的预期断言通过，不能写成全部校验正确或React19全组件支持已验证。覆盖仅plain-field BaseForm；对象字段、Actions权限、viewers、SSR/RSC以及生产集成仍未实测。

### Action、副作用与权限

默认 pipeline：RHF 合法 → `coerceFormState` 逐字段转换 → `useOsdkAction.applyAction` → `onSuccess(result)`。自定义 `onSubmit(state,applyAction)` 接收的也是转换后的值，并接管 Action 执行与成功回调；组件不再自动调用 onSuccess。ActionForm 的 `try` 覆盖自定义 onSubmit、默认 applyAction 和 onSuccess，其间异常会送入 `onError({type:"submission",error})`，组件不主动重抛该异常。[ActionForm运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/ActionForm.tsx#L123-L138)

**转换与 Action 异常走不同错误路径。** `coerceFormState` 位于上述 `try` 之前；转换抛错会使 handleSubmit reject，由 BaseForm 的 `useAsyncAction` 捕获并写入 submissionError，进入其提交错误提示路径。相反，默认 Action 请求失败在 ActionForm 内被捕获后，通常不会成为 BaseForm 的 submissionError，应用需要通过 onError 呈现后端失败。不能概括为“所有提交异常均进入 ActionForm onError”。[BaseForm接线](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/BaseForm.tsx#L75-L110)、[useAsyncAction捕获](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/shared/hooks/useAsyncAction.ts#L44-L60)、[BaseForm错误提示测试](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/__tests__/BaseForm.test.tsx#L644-L675)

从 React hook 实现可确认，applyAction 会调用 observableClient.applyAction，ActionValidationError 与其他异常区分记录并 rethrow；另有独立 validateAction，但 ActionForm 没有调用。**这说明预校验可由 EOS 自己组合 hook 实现，不能说明未经验证的 Action 可以绕过后端权限。** 组件源码未见权限 capability 查询、可执行性预检测、审批流、操作后 undo/rollback UI 或成功后自动关闭/清空表单。最终权限和业务校验行为需真实受限环境验证；本稿不执行。[hook实现（同发布commit）](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react/src/new/useOsdkAction.ts#L82-L189)

提交 coercion：null→undefined；integer/long 会 Math.trunc；数值字符串用 Number；boolean 只接受 boolean/"true"/"false"；Date 调用 toISOString，可解析日期字符串保持原样；object/objectSet/struct/interface 与 attachment/mediaReference 原样透传。**这是有限转换，不是完整有效性检查，也不保证失败一律返回 undefined。** 空或不可解析的数值字符串、不接受的boolean字符串等分支返回undefined；无效 Date 对象调用 toISOString 会抛 RangeError。`extractNumber` 对已是number的值直接返回，未检查 NaN/Infinity，数值字符串 "Infinity" 也不会被 Number.isNaN 拦截；这些值不会在 coercion 阶段被统一拒绝。这里是源码链路核验，不代表后端会接受这些值。[运行转换](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/utils/coerceFieldValue.ts#L27-L101)、[Date与数值分支](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/utils/coerceFieldValue.ts#L71-L99)

FilePicker 本身只输出 File/File[]，不会点击 Browse 即上传。下游 client 的 `toDataValue` 遇到 Blob+name 或 AttachmentUpload，会先调用 Attachments.upload 获得 RID，再提交 Action；MediaUpload 则走 MediaSets.uploadMedia。这意味着文件型提交流程在 Action 之前可能已有上传副作用，不能把“Action 失败”理解为所有外部资源均未产生。**待集成验证项：自动生成 mediaReference FILE_PICKER 同样输出 File，但下游 File 分支走 attachment 上传；不能仅凭 renderer 名称断言已完整支持媒体上传。** 该项是代码链路推断，本稿没有真实 Foundry 用例证明失败或成功。[FilePicker运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/fields/FilePickerField.tsx#L69-L84)、[client转换](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/client/src/util/toDataValue.ts#L79-L108)、[File guard](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/client/src/object/AttachmentUpload.ts#L19-L41)

ObjectSelect 默认 300 ms search debounce，PAGE_SIZE 50，以 `$title.$containsAllTermsInOrder` 服务端查询；可以以 objectType 或 scoped objectSet 为数据源，后续 fetchMore。ObjectSetField 用 pageSize 1拿 totalCount/metadata，显示对象集摘要，没有赋值编辑 UI。它们虽由 BaseForm renderer 调用，却仍依赖 `@osdk/react` 与 provider。[ObjectSelect运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/fields/ObjectSelectField.tsx#L30-L143)、[ObjectSet运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/fields/ObjectSetField.tsx#L40-L126)

### 测试证据的含义

ActionForm.test 中 useOsdkAction/useOsdkMetadata 被 mock：有 default metadata 字段、disabled、pending、success/error、required拦截与controlled状态测试。defaultMockActionResult 提供 validateAction mock，但本测试没有真实后端权限/validation contract 用例；应称“组件转换和回调单测覆盖”，不能称“Foundry Action 已实测”。[mock源](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/__tests__/ActionForm.test.tsx#L77-L124)、[提交/受控测试源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/action-form/__tests__/ActionForm.test.tsx#L265-L418)

## DocumentViewer 与各 renderer

### 路由是 MIME 判定，不是任意文档渲染

DocumentViewer 从 `mimeTypeOverride ?? media.getMediaReference().mimeType` 选择具体 wrapper，仅 TIFF 还根据 fileName 的 .tif/.tiff hint 回退。运行路由如下；无 MIME 参数归一化/大小写处理或通用文件扩展名识别。[路由运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/document-viewer/DocumentViewer.tsx#L38-L117)

| 路由 | 运行输入判定 | 复用/限制 |
| --- | --- | --- |
| PDF | application/pdf | PDF.js渲染；完整组件/parts/hooks最丰富 |
| TIFF | image/tiff 或文件名.tif/.tiff | UTIF客户端默认只解码首帧；可选服务端多页TIFF转PDF |
| 图片 | image/png、jpeg、gif、svg+xml、webp、bmp | browser img，无图像编辑/缩放工具栏 |
| 视频 | MIME startsWith("video/") | browser video controls，浏览器codec能力决定实际可播 |
| Markdown | text/markdown、text/x-markdown | react-markdown + remark-gfm |
| Spreadsheet | xlsx 的 OOXML精确MIME | xlsx-republish，sheet tabs+只读HTML table |
| Email | message/rfc822 | postal-mime解析headers/body，HTML iframe |
| XML | application/xml、text/xml | pre/code纯文本，保留内容，不是XML树编辑器 |
| 其他 | fallback | Unsupported file type；未实现DOCX/PPTX/CSV/plain-text/audio路由 |

具体 JSX dispatch 给 Markdown/XLSX/Email/XML 只传 media/className；DocumentViewer 的细粒度 props forwarding 主要为 PDF/Image/Video/TIFF，若要自定义其他 renderer，应直接使用对应 Base 层。[dispatch运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/document-viewer/DocumentViewer.tsx#L119-L179)、[API类型](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/document-viewer/DocumentViewerApi.ts#L36-L71)

### PDF

底层依赖是 PDF.js (`pdfjs-dist ~4.8.69`)，不是 AntD 或 Blueprint完整PDF控件。usePdfDocument 支持URL/ArrayBuffer/Uint8Array/Blob，通过 getDocument加载、配置 worker URL，unmount/source change销毁 loadingTask。PDFViewer/EventBus/PDFLinkService/PDFFindController负责文档、导航与搜索。[document运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfDocument.ts#L17-L114)、[viewer运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfViewer.ts#L17-L108)

现有UI包括页导航/缩放/fit width/旋转/搜索/缩略图或outline sidebar、外部annotations overlay、可选文字高亮与PDF表单。enableDownload、enableHighlight默认false；表单save按钮只在发现formFields且传onFormSubmit时显示。[BasePdfViewer运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/BasePdfViewer.tsx#L39-L102)、[UI assembly](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/BasePdfViewer.tsx#L142-L215)

PDF公开层可使用 Toolbar/Sidebar/Content/SearchBar/AnnotationLayer/OutlineSidebar，自组布局；公开hooks包含 usePdfDocument/viewer/search/sync/outline/formFields/highlightMode/annotationPortals/annotationsByPage 和 composition `usePdfViewerCore`、`usePdfViewerState`，另有context/provider/usePdfViewerInstance。这是已导出接口，不是能任意deep import整个src的许可或稳定性承诺。[公开barrel](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/pdf-viewer.ts#L17-L119)。[Viewer参数图鉴](api-viewers.md)展开主/Base组件及七个PDF构件的props；hooks仅覆盖公开symbol、类型别名、职责和源码索引，未完整展开各hook的输入字段、返回字段及其默认行为。

持久化边界：外部annotations来自props；文字高亮创建/删除发事件供应用保存；form fields 收集值后调用onFormSubmit，没有内建Ontology写回。下载调用`document.getData()`并生成本地blob link，而不是`saveDocument()`，不能据此宣称编辑/高亮/PDF表单值都会随下载保存。高亮删除通过 monkey-patch `annotationStorage.remove` 实现，源码自己标为fragile，应作为PDF.js升级时的回归重点。[高亮运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfHighlightMode.ts#L153-L248)、[form submit运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfFormFields.ts#L391-L443)、[download运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfViewerState.ts#L202-L231)

EOS UX风险（分析）：`usePdfViewerState` 在 window级捕获Ctrl/⌘+F，不按当前viewer焦点限定；多个viewer或页面全局搜索可能相互争用。PDF/Media wrapper用bytes输入时会先全量取内容，不能把URL模式的PDF.js能力推断成所有OSDK媒体都按range流式加载。[shortcut运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/hooks/usePdfViewerState.ts#L159-L174)、[media fetch运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/PdfViewer.tsx#L27-L54)

### TIFF、Spreadsheet、Email 和其他

TIFF默认运行 `UTIF.decode → ifds[0] → decodeImage → toRGBA8 → canvas`，输入限制25,000,000 bytes，错误显示与onError；25MB是输入压缩文件上限，不是解码后bitmap内存上限。`enableTiffToPdf`默认false，打开后先取整个TIFF并数页，多页经`@osdk/api/unstable transformAndWait` 的 `$imageToDocument/$createPdf`服务端MIO转换，失败console.warn后回退TIFF。这条路径需要client/provider、服务端转换支持与权限；本次未调用。[TIFF运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/images/tiff-viewer/BaseTiffViewer.tsx#L28-L81)、[conversion运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/document-viewer/hooks/useTiffToPdf.ts#L50-L139)

Spreadsheet解析整个ArrayBuffer，xlsx-republish.read后sheet_to_json(header:1, raw:false, defval:"")成为字符串行数组；BaseSpreadsheetViewer为当前sheet渲染所有row×maxColumns的table，标签切sheet。源码没有虚拟化、单元格编辑、公式重算、保留Excel格式/图表的功能，不能将它看成react-data-grid或在线Excel。[解析运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/spreadsheet-viewer/parseSpreadsheet.ts#L19-L43)、[表格运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/spreadsheet-viewer/BaseSpreadsheetViewer.tsx#L43-L128)

Email通过postal-mime解析ArrayBuffer，仅提取subject/from/to/cc/date/html/text；附件不放入ParsedEmail返回结果，因而本组件不是邮件附件浏览器。HTML使用srcDoc iframe、sandbox="allow-same-origin"，没有allow-scripts；纯文本回退直接显示。源码注释明确承认CSS url()/tracking像素可发外连，不能将“sandbox”解读成完整离线或隐私隔离。[解析运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/email-viewer/parseEmail.ts#L53-L68)、[HTML安全与正文运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/email-viewer/BaseEmailViewer.tsx#L45-L73)

Markdown使用react-markdown + remark-gfm（GFM表格等），当前代码没有rehype-raw插件或富文本编辑器配置。XML只是pre/code，React文本children保留字符。Image用img，Video用native video controls，二者wrapper将response.blob转objectURL并在替换/卸载时revoke；没有自带标注工具或播放器codec转码。[Markdown运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/markdown-viewer/BaseMarkdownViewer.tsx#L17-L42)、[XML运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/xml-viewer/BaseXmlViewer.tsx#L24-L39)、[Image wrapper](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/images/image-viewer/ImageViewer.tsx#L27-L64)、[Video base](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/video-viewer/BaseVideoViewer.tsx#L24-L39)

事件边界：Image/Video/TIFF的`onError`传给Base renderer，对应img/video加载或TIFF解码失败；media.fetchContents失败由wrapper显示inline错误，并未自动调用相同onError callback。EOS若需要统一记录媒体权限/网络失败，需要adapter或自有数据层，而非单挂这个renderer callback。[Image错误运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/images/image-viewer/ImageViewer.tsx#L41-L64)、[TIFF错误运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/images/tiff-viewer/TiffViewer.tsx#L38-L58)

## 界面记录

![ActionForm](assets/07-action-form.jpg)

官方 Storybook mock Action metadata 生成的表单。

![必填校验](assets/08-form-validation.jpg)

空姓名提交产生本地必填错误；本次没有执行有效 Action。

![PDF](assets/09-pdf-viewer.jpg)

PDF 工具栏和缩略图侧栏的实际 UI；样本文档来自官方 Storybook 的第三方论文 fixture，归属见 [assets.md](assets.md)。

![电子表格](assets/10-spreadsheet.jpg)

只读 sheet 展示，不是可编辑数据网格。

![邮件](assets/11-email.jpg)

公开 fixture 邮件显示 headers 与正文，没有真实邮件账户。

![AIP Chat](assets/13-aip-chat.jpg)

BaseAipAgentChat 的模拟会话；本次没有发送模型请求或运行 Agent。

## 逐 viewer 参数与状态图鉴（关键组）

下面列出组件采用决策所需的关键参数组。[Viewer参数图鉴](api-viewers.md)展开主/Base组件与七个PDF构件的props；PDF hooks仅提供公开接口索引，不是完整输入/返回值reference。`className`一般optional、默认undefined；各wrapper都要求`media: Media`并通过Omit移除Base的输入属性。

| 公开组件 | 必传/主要输入 | 默认与回调 | 状态拥有者 |
| --- | --- | --- | --- |
| DocumentViewer | media: Media | MIME取Media reference，可mimeTypeOverride；enableTiffToPdf=false，fileName为TIFF hint；分renderer *ViewerProps | 路由派生，无文件类型selection state或控制callback |
| PdfViewer / BasePdfViewer | media / src: string\|ArrayBuffer\|Uint8Array\|Blob | annotations=[]；page=1/scale=1/autoSize=false/sidebarOpen=false（default*，旧initial*已deprecated）；sidebarMode=thumbnails；enableHighlight/enableDownload=false；onAnnotationClick/onTextHighlight/onHighlightDelete/onDownload/onFormSubmit/onFormChange | 完整组件的page/scale/sidebar为内部状态+初始化props；公开hooks/parts用于更细受控组合，annotations外部传入，formData用于加载时预填 |
| TiffViewer / BaseTiffViewer | media / src?: Uint8Array | content是deprecated alias，src优先；onError?:()=>void | 本地decode state；Base类型因旧alias尚未required，二者都不传时渲染空容器，不创建canvas |
| ImageViewer / BaseImageViewer | media / src:string | alt=""；onError?:()=>void | browser img加载/显示，无选中/编辑状态 |
| VideoViewer / BaseVideoViewer | media / src:string | mimeType可选，wrapper fallback Media MIME；onError?:()=>void；native controls=true | 播放状态由browser video拥有，无公开play/pause/currentTime controlled props |
| MarkdownViewer / BaseMarkdownViewer | media / content:string | className可选，无公开render slot/events | 只读文本派生 |
| EmailViewer / BaseEmailViewer | media / content?:ParsedEmail | email为deprecated alias，content优先；无事件或渲染slots | 只读；content/email均缺时空正文 |
| SpreadsheetViewer / BaseSpreadsheetViewer | media / content?:ParsedSpreadsheet | spreadsheet为deprecated alias，content优先；无sheet change callback | activeSheetIndex内部useState(0)，类型无controlled activeSheet；越界clamp |
| XmlViewer / BaseXmlViewer | media / content:string | className可选，无events | 只读文本派生 |

参数证据：[Document API](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/document-viewer/DocumentViewerApi.ts#L36-L71)、[PDF API](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/pdf-viewer/PdfViewerApi.ts#L147-L260)、[TIFF API](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/images/tiff-viewer/TiffViewerApi.ts#L19-L38)、[Image API](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/images/image-viewer/ImageViewerApi.ts#L19-L36)、[Video API](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/video-viewer/VideoViewerApi.ts#L19-L36)、[Markdown API](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/markdown-viewer/MarkdownViewerApi.ts#L19-L32)、[Email API](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/email-viewer/EmailViewerApi.ts#L24-L51)、[Spreadsheet API](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/spreadsheet-viewer/SpreadsheetViewerApi.ts#L19-L48)、[XML API](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/xml-viewer/XmlViewerApi.ts#L19-L30)。状态结论同时参照运行链接；TIFF无输入时的空容器见[BaseTiffViewer](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/images/tiff-viewer/BaseTiffViewer.tsx#L124-L154)，不能仅凭类型推断渲染节点。

## AipAgentChat / BaseAipAgentChat（实验性）

### 定位、依赖与权限边界

`@osdk/react-components/experimental/aip-agent-chat`公开AipAgentChat/BaseAipAgentChat以及UIMessage/role、ChatStatus类型、getUIMessageText工具；message/composer/model-picker等内部子组件没有在此barrel公开。AipAgentChat名称不能据此解读为已接通Foundry Agent执行：运行链路是`PlatformClient → foundryModel → @osdk/react/experimental/aip.useChat → BaseAipAgentChat`，后端目标是Foundry Language Model Service。[公开入口](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/public/experimental/aip-agent-chat.ts#L17-L29)、[运行wrapper](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChat.tsx#L17-L86)

PlatformClient负责base URL和auth，组件没有发现模型权限、可访问model enumeration、工具/Action授权确认或能力扩张逻辑。availableModels是应用传入字符串，不是自动拉取后台授权清单；gpt-4o只是缺省API name，不构成当前环境能用它的保证。当前wrapper的model仅string，尽管aip-core foundryModel还支持ModelIdentifier对象/registeredModel RID，wrapper并未开放该对象形态。[model与picker运行](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChat.tsx#L27-L120)、[aip-core model实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/aip-core/src/model.ts#L17-L85)

useChat源码明确将v0界定为text-only，不支持tools/multi-step agent loops/stream resume；LmsChatTransport的reconnectToStream直接返回null。核心stream transport虽然有tool-call chunk转换分支，也不能因此宣称此UI带Agent执行循环。wrapper公开props没有tools、agentId、temperature/maxOutputTokens、自定义transport、chat id、regenerate/resume入口；如果EOS需要自定义传输/状态，可自己调用hook或用Base接后端，但不要把文档提到的“高级组合”当未实现Agent loops的证明。[hook界限](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react/src/aip/useChat.ts#L40-L86)、[transport resume](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/aip-core/src/lmsChatTransport.ts#L190-L196)

### 参数/模式/事件图鉴

| 组件/参数组 | required/default | 模式与回调 |
| --- | --- | --- |
| AipAgentChat client | `client:PlatformClient`必传 | 服务端LMS访问由应用配置client |
| model/defaultModel/availableModels | 均optional；初始化优先model→defaultModel→availableModels[0]→"gpt-4o" | model提供即受控；否则内部model state；有非空availableModels才显示picker；onModelChange在两模式发出，in-flight禁用picker |
| initialMessages/system | optional | seed snapshot、每请求system prompt；initialMessages不是受控messages同步入口 |
| placeholder/enableAutoScroll | "Type a message..." / true | 无受控draft prop；autoscroll用户向上滚动后暂停，回到底部附近恢复 |
| onError/onFinish | optional | hook出错/流式成功完成listener；onFinish含完成message+messages数组 |
| renderEmptyState/renderMessage/className | optional | 定制空状态/单message，或根class；无slots时完整默认UI |
| BaseAipAgentChat messages/status/error | messages:ReadonlyArray<UIMessage>、status:ChatStatus、error:Error\|undefined均必传（error属性即使undefined也必传） | 外部受控会话状态，Base只拥有composer draft等UI状态 |
| Base callbacks | onSendMessage:(text)=>Promise<void>、onStop、onClearError均必传 | send传trim后text；Stop/错误Dismiss按外部回调；Base不自行实现网络/会话持久化 |
| Base composerFooter、render slots、placeholder/autoScroll | footer/slots可选；同wrapper默认 | 用于自有model picker、后端、布局定制 |

证据：[AIP props](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/AipAgentChatApi.ts#L42-L171)、[Base props/实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/BaseAipAgentChat.tsx#L29-L141)、[initialMessages只初始化store](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react/src/aip/useChat.ts#L178-L194)、[autoscroll实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/hooks/useChatAutoScroll.ts#L19-L66)

默认消息bubble取getUIMessageText并作React文本children，非Markdown富文本/引用/source卡片/工具批准UI。composer是3行textarea，Enter发送、Shift+Enter换行，空白或in-flight禁用send，in-flight显示Stop；发送后立刻清draft，同步throw/Promise rejection被吞以等待上层chat error。自有Base backend若只reject却不更新error prop，会丢失错误展示。[message实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/components/AipAgentChatMessage.tsx#L33-L54)、[composer实现](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/components/AipAgentChatComposer.tsx#L38-L119)

Base测试源码覆盖空状态、messages、send enable/send callback、Stop、error/Dismiss、composerFooter、render slots；OSDK wrapper测试文件只有三个`it.todo`，不能声称组件LMS接线已由该单测验证。官方Storybook本身使用BaseAipAgentChat、应用内state/setTimeout模拟token流，是UI实拍而非模型对话实测。[Base测试源码](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/__tests__/BaseAipAgentChat.test.tsx#L41-L265)、[wrapper todos](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/aip-agent-chat/__tests__/AipAgentChat.test.tsx#L19-L31)、[Storybook模拟](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components-storybook/src/stories/AipAgentChat/AipAgentChat.stories.tsx#L51-L145)

## 主题、公开导出、CBAC 与许可证

主题与扩展专题见 [theme-and-extension.md](theme-and-extension.md)，包含主题/CSS层叠和变量、primitives/hooks公开边界、CBAC 8项family的参数/默认/事件/受控模式、OSDK与直接依赖许可证。

实际npm根barrel没有值导出，primitives入口却真实公开ActionButton/Dialog/SkeletonBar/Tooltip/TooltipArrow，不能沿用README关于“不导出primitives”的陈旧说明；主题仍在experimental入口。ThemeProvider通过DOM属性和CSS控制外观，不提供wrapper DOM。React19声明peer支持与全路径React19回归是不同证据；useSystemTheme直接使用React.useSyncExternalStore，不能将React17 peer字符串当该路径可运行证明。CBAC的maxClassificationConstraint只在ConstraintCallout提示，confirm回调也不自行保存权限；不能把此family当权限执行边界。OSDK 95个package manifests均声明Apache-2.0，但直接依赖含MIT/MIT-0/Apache-2.0，尚未做完整传递依赖NOTICE审计，开源不等于可以无条件复制全部素材、商标、包和服务能力。
