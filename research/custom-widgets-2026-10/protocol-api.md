# API / 宿主协议附录：公开客户端究竟能证明什么

检索与运行日期：2026-10-01。发布包锁定 `@osdk/widget.api@3.74.0`、`@osdk/widget.client@3.74.0`；发布源码锚定 `fb8ec172d540ef7819382ff036aa2a692614af75`。当前 main `e53b94ecd5de7cdd7e864d0daa04363bdad4db4c` 仅作交叉检查。本文审计公开 API、发布包和本地 mock；**没有真实 Workshop 租户接入测试，也没有闭源宿主安全审计**。

公开客户端暴露的是一个很窄的契约：宿主给参数，组件发事件及参数更新请求，再加 ready/reload/resize 生命周期通知。`widget.client` 依赖运行环境预先注入的 `window.__PALANTIR_WIDGET_API__`，没有在这个包里直接执行 `window.parent.postMessage`。因此“源码注释把值称为 postMessage wire format”与“完整传输层、origin 校验已公开”必须分开。[参数 wire 注释][parameters-wire]、[客户端注入接口与实现][client-bridge]

## 1. 版本、包与证据锁定

| 项目 | 本次实际核验 | 边界 |
|---|---|---|
| widget.api / widget.client | 稳定版均 3.74.0；分别发布于 2026-09-29 17:25:06.301Z / 17:20:31.590Z | 不把包版本等同宿主协议版本 |
| tarball | 实算 SHA-1 对上 registry `shasum`，实算 SHA-512 对上 `integrity` | 没有只信页面上的版本号 |
| 源码对应关系 | API 8 个、client 4 个发布包 browser sourcemap 的 `sourcesContent` 与发布 SHA 全文一致；也与本次 main 的相应文件一致 | source map 一致性覆盖这些源文件，不覆盖所有 Foundry 运行时代码 |
| npm provenance | 两包 registry 返回的 provenance 指向发布 SHA、`.github/workflows/release.yml`、同一 release run；SLSA subject digest 与实际 tarball 匹配 | 未做 Sigstore / DSSE / Rekor 密码学签名验证 |
| 实际运行 | Node 22.17.0 导入实际 npm 包，注入本地 bridge mock，13 条断言通过 | 不是浏览器跨源、Workshop、认证或权限测试 |
| 类型契约 | TypeScript 5.5.4 编译真实包声明；正例通过，移除预期错误标记后出现 5 个负例错误 | 类型兼容不能代替运行时格式验证 |

包文件清单、下载 URL、发布时刻、逐文件 SHA-256 见 [npm 审计](evidence/protocol-npm-audit.json)；源码全文比对见 [source comparison](evidence/protocol-npm-source-compare.json)；provenance 解码和 digest 对照见 [provenance](evidence/protocol-npm-provenance.json)。完整复现脚本见 [client probe](probes/protocol-client.mjs)、[类型 fixture](probes/protocol-types.ts)、[类型 probe runner](probes/protocol-types.mjs)。

## 2. 配置 schema 与配置面板不是同一层

开发者的 TypeScript `WidgetConfig` 描述以下字段；它不是通用 React props 描述器，也不是一份包含任意 JSON Schema 关键字的表单 schema。[WidgetConfig][config-widget]

| 字段 | 类型 / 必填 | 含义 |
|---|---|---|
| `id` | `string`，必填 | widget 标识 |
| `name` | `string`，必填 | 名称 |
| `description` | `string`，可选 | widget 说明 |
| `type` | 固定为 `"workshop"`，必填 | 本版公开 config 的宿主类型 |
| `parameters` | `Record<string, ParameterDefinition>`，必填 | 参数 ID → 参数定义 |
| `events` | event ID → `{displayName, parameterUpdateIds}`，必填 | 对宿主发出的事件及可更新参数 ID |
| `permissions` | `BrowserPermission[]`，可选 | 请求额外浏览器 / iframe 能力 |
| `refreshHostDataOnAction` | `boolean`，可选 | OSDK Action 后的宿主数据刷新配置 |

每个参数定义提供 `type`、`displayName`；array 另有 `subType`，objectSet 另有 OSDK `allowedType`。参数定义里**没有**公开声明 `required`、`default`、`enum`、`min/max`、验证 regex、控件 renderer 或任意 React callback。`objectType` 已弃用；manifest 仍保留 `objectTypeRids` 的兼容字段。[参数定义与 manifest 定义][config-parameters]

`defineConfig()` 运行时直接返回输入对象；它的作用是保留 const generic 和事件/参数之间的类型关联。它不负责校验 JSON、camelCase、数量、日期或数据值。本地实际包 probe 验证了无类型调用可把非法 config 原样返回。[defineConfig 实现][define-config]、[probe 结果](evidence/protocol-client-probe.json)

官方文档要求最多 50 个参数和 50 个事件、参数/事件 ID 使用 camelCase，并说明 Workshop Widget setup panel 能把参数绑定到 Workshop 变量、事件绑定到 Workshop 事件。公开 Vite 校验与 manifest 转换是另外一层；其实现、哪些约束没有在插件内验证，见 [发布链路附录](build-release.md)。**没有公开 Workshop 编辑器源码，不能从 `displayName` 字段反推出实际配置面板所有控件、默认值、校验错误和 binding 行为。**[官方参数与事件文档](https://www.palantir.com/docs/foundry/custom-widgets/parameters-and-events)

类型关系由同一 config 派生：`AsyncParameterValueMap<C>` 保留参数 tag 和异步包装；`ParameterValueMap<C>` 提取内部 raw 值；`EventId<C>` 提取 events 的 key；`EventParameterValueMap<C, EventId>` 提取该事件声明可更新参数的 raw map，排除未知/只读 ID。`widget.client` 根据这些类型限制 emit 调用，实际 JS 执行时不会重新解析 config 做校验。[类型映射与事件派生][config-derived]

## 3. 参数类型完整表：文档承诺与实验性源码分列

下面的“内部值”指 `AsyncValue<V>` 内的 `V`；宿主传入的外层仍有参数 `type`，array 还有 `subType`。[类型映射][parameters-types]、[数组与 union][parameters-union]

| config `type` | 内部值 / wire 形状 | 格式与范围 | 证据性质 |
|---|---|---|---|
| `boolean` | `boolean` | true / false | 官方文档 + 发布声明 |
| `number` | `number` | 文档示例包含整数及小数；声明没有有限值或区间约束 | 官方文档 + 发布声明 |
| `string` | `string` | 文本 | 官方文档 + 发布声明 |
| `date` | `string` | 文档要求 ISO 日期 `YYYY-MM-DD`；不是 JS `Date` | 官方文档 + 发布声明 |
| `timestamp` | `string` | 文档要求含时区 ISO datetime | 官方文档 + 发布声明 |
| `scenario` | `string` | Ontology scenario RID | 官方文档 + 发布声明 |
| `objectSet` | `{objectSetRid: string}` | config 的 `allowedType` 为 OSDK object type 或 interface 定义；跨边界给集合 RID | 官方文档 + 发布声明 |
| `array` | `boolean[]` / `number[]` / `string[]` | `subType` 指定相应 primitive | 发布声明；文档描述 primitive arrays |
| `array` | `date` / `timestamp` / `scenario` 对应的 `string[]` | 发布声明包含 `ScenarioArray`；没有 objectSet array、嵌套 array 的 union | 发布声明 |
| `mapTileLayer` | `{styleJsonUrl: string}` | host 选定的只读 Mapbox / Maplibre style JSON URL；renderer 自己加载 style | **源码明确 experimental，当前公开参数文档表未列，真实租户未验证** |

`mapTileLayer` 的 config 字面量用了 `"mapTileLayer" & Record<never, never>`，源码注释说用于隐藏自动建议。事件参数 ID 的派生类型排除该类型，所以不能把地图图层当双向输出参数。[实验 config][config-map-experimental]、[只读参数排除][config-readonly]、[style wire 值][map-value]

`struct`、`objectSetFilter` 不属于本版 ParameterValue union；官方文档也明确它们尚不是第一类参数。这不妨碍 widget 内部维护复杂 React 状态，但不能把该内部状态直接宣称为 Workshop 可绑定变量契约。[公开 union][parameters-union]、[官方文档](https://www.palantir.com/docs/foundry/custom-widgets/parameters-and-events)

类型 probe 同时证明两个边界：错误 event ID / parameter ID、用字符串代替 number、用 `Date` 实例代替 date string、更新只读图层都会触发类型错误；`"not-a-date"` 和 `Infinity` 仍能分别赋给 string / number 类型。后者只说明 TypeScript 的类型宽度，**不说明宿主或服务端接受这两个值**。[类型运行记录](evidence/protocol-types-probe.json)

## 4. 异步参数是状态值，不是单一数据值

| `AsyncValue.type` | `value` | `error` | UI 适配含义 |
|---|---|---|---|
| `not-started` | 不允许 | 不允许 | 尚未开始 |
| `loading` | 不允许 | 不允许 | 初次等待 |
| `loaded` | `V \| undefined` | 不允许 | 已完成，但仍可能没有值 |
| `reloading` | `V \| undefined` | 不允许 | 允许携带当前值等待更新 |
| `failed` | `V \| undefined` | 必须，默认类型为 `Error` | 失败仍可携带当前值 |

源码给出的预期生命周期是 not-started → loading → loaded/failed → reloading。它是类型设计和注释中的预期，不是强制状态转换机；API 包没有在这些 interface 后实现转换校验。[AsyncValue 全部定义][async-value]

对 adapter 的实际意义是：不能把 `undefined` 同 loading 等同；不能在任意 reload 或失败时无条件清空数据；应明确旧值何时继续显示、何时禁用操作、何时显示错误。这里是工程建议。React convenience hook 如何合并参数状态，见 [React 适配附录](react-adapter.md)。

## 5. 当前消息契约与生命周期

`HostMessage.Version` 在发布包中为 `"1.0.0"`，与 npm 的 3.74.0 是两套版本。公开 host union 只有一个消息类型；公开 widget union 有四个。[host 消息][host-messages]、[widget 消息][widget-messages]

| 方向 | `type` | `payload` | 公开作用 / 边界 |
|---|---|---|---|
| host → widget | `host.update-parameters` | `{parameters: AsyncParameterValueMap<C>}` | 传递参数与加载状态；client 只转发 payload，不自己 fetch、merge 或重算 |
| widget → host | `widget.ready` | `{apiVersion: "1.0.0"}` | 表示可以接收第一批参数；没有公开 `host.ready-ack` |
| widget → host | `widget.emit-event` | `{eventId, parameterUpdates}` | 发出事件和由 config 导出的 raw 参数更新 map；不是 React callback 函数跨 iframe 传递 |
| widget → host | `widget.reload` | `{}` | 请求宿主 reload；JSDoc 举 full reload / HMR 为例 |
| widget → host | `widget.resize` | `{width: number, height: number}` | 文档 body 的 border-box 尺寸；不是直接设置 Workshop layout |

示意仅表示公开契约，不代表已经观察到真实租户消息顺序：

```mermaid
sequenceDiagram
    participant W as Widget UI
    participant C as Published widget.client
    participant B as Injected API bridge
    participant H as Workshop host (closed source)
    W->>C: subscribe(); ready()
    C->>B: widget.ready {apiVersion: "1.0.0"}
    B-->>H: Runtime transport (not audited)
    H-->>B: Parameter state (host behavior not audited)
    B->>C: CustomEvent detail = host.update-parameters
    C->>W: hostEventTarget CustomEvent detail = payload
    W->>C: emitEvent(eventId, parameterUpdates)
    C->>B: widget.emit-event
    Note over W,H: No public acknowledgement / request ID / revision field
```

消息定义没有 request ID、参数 revision、事务 ID、重试次数、超时值或取消消息。client 的 emit 返回 `void`，其实现调用 bridge 后结束；它不等待宿主处理结果、不生成本地 acknowledgement、不自动修改刚接收的参数。宿主是否同步应用多个参数、先更新变量还是先跑副作用、如何 deduplicate/retry，不能从这个 client 得到验证结论。[emit 类型与实现][client-methods]、[实际 mock](evidence/protocol-client-probe.json)

有一个实际产品级时序提示来自官方文档：在 `Open URL` 事件里直接更新 string URL 变量是同步的，但下游变量 transform 可能还没完成，打开链接的副作用就先执行。这支持“变量图存在异步边界”，不等于证明整个事件链都是事务或按某一种全局顺序执行。[Open a URL in Workshop](https://www.palantir.com/docs/foundry/custom-widgets/open-url-in-workshop)

## 6. `widget.client` 的真实 transport seam

客户端创建时检查 `"__PALANTIR_WIDGET_API__" in window`；缺少该属性立即抛错。它随后把该属性当以下 bridge 接口使用，没有在创建时深度验证接口形状。[注入 bridge][client-bridge]

```ts
// 仅概括公开client消费的注入接口，不是完整宿主实现。
interface InjectedBridge {
  sendMessage(message: WidgetMessage<any>): void;
  addEventListener(type: "message", listener: (event: CustomEvent<HostMessage<any>>) => unknown,
                   options?: boolean | AddEventListenerOptions): void;
  removeEventListener(type: "message", listener: (event: CustomEvent<HostMessage<any>>) => unknown,
                      options?: boolean | EventListenerOptions): void;
}
```

返回的 `FoundryWidgetClient` 提供 `ready()`、`reload()`、`resize({width,height})`、`emitEvent(eventId,{parameterUpdates})`、`sendMessage(message)`、`subscribe()`、`unsubscribe()` 和 `hostEventTarget`。创建本身不订阅，也不发 ready；手动使用时应先注册 `hostEventTarget` listener、调用 `subscribe()`，再调用 `ready()`，销毁时移除 listener 并 `unsubscribe()`。这是依据实现安排的调用建议；React provider 负责封装自己的生命周期。[完整客户端 interface][client-interface]、[发送/订阅实现][client-methods]

bridge 的 message 回调接收 `CustomEvent`，其 `detail` 是完整 `HostMessage`；`FoundryHostEventTarget` 再发一个以 `host.update-parameters` 为事件名的 `CustomEvent`，其 `detail` 则是消息 `payload`。两个层次不能混用，尤其是手写 adapter / mock 时。[client 转发][client-bridge]、[host EventTarget][host-event-target]

`isHostParametersUpdatedMessage` / `isWidget*Message` 仅比较 `event.type` 字符串；visitor 对已知 type 调 handler，否则走 `_unknown`。client 的 `_unknown` 什么也不做。这些 guard 不是不可信数据的 schema validator。实际 JS probe 可把未知 event / parameter ID 经 client 发给 bridge；这表明**这个公开 wrapper 层没有 runtime whitelist**，不是证明真实宿主接受它们，也不是一项已证实的权限漏洞。[host guard][host-guards]、[widget guards][widget-guards]、[probe](evidence/protocol-client-probe.json)

## 7. objectSet、scenario 与 OSDK 的边界

objectSet 参数的开发配置携带 OSDK object type / interface 定义，wire 值只携带 `objectSetRid`；client 自己不把它展开成对象数组，也不创建查询客户端。scenario wire 值只是 scenario RID 字符串，属于 primitive 映射。[allowed type][parameters-types]、[objectSet wire][objectset-value]

因此需要区分三个类型空间：Workshop 可绑定的参数 schema、跨宿主边界的可序列化 wire value、OSDK 的 typed/lazy ObjectSet。React 层可以负责将 wire RID 恢复成 OSDK ObjectSet，并将事件中生成的 ObjectSet 转为可传回的表示；它不能省去 ontology/client 和权限上下文。完整恢复、缓存与异步 emit 行为见 [React 适配附录](react-adapter.md)。

`createFoundryWidgetTokenProvider()` 返回签名为 `() => Promise<string>` 的 token-provider 回调；调用该回调才得到解析为 `"widgets-auth"` 的 Promise。JSDoc 说明实际请求时替换 placeholder。官方文档要求 `baseUrl = window.location.origin`，运行时使用查看者 token 和权限；它不是把一个长期真实 bearer token 发给第三方组件的公开 API，也不是在本地 standalone 页面使用该字符串就能访问 Foundry。[token provider][token-provider]、[官方 OSDK 配置](https://www.palantir.com/docs/foundry/custom-widgets/use-osdk)

OSDK 功能不能简单从通用 `@osdk/client` 能力反推。官方 widgets 文档当前明确 object set subscriptions 不受支持，Ontology APIs 还需相应 enrollment workflow 授权；本次没有测试真实请求拦截和 token replacement。[官方支持与限制](https://www.palantir.com/docs/foundry/custom-widgets/use-osdk)

## 8. iframe、权限、外网与故障恢复：已知与未知

官方文档明确 custom widget 运行在 iframe 中，默认有受限 attributes；额外能力由 widget 声明、application builder 手工授予，camera/microphone 仍需终端用户浏览器授权。本版 API 枚举包含 camera、microphone、autoplay、allow-downloads、allow-forms、allow-popups，**还含当前文档列表未列出的 `allow-modals`**；后者只按源码可见性报告，未在租户里验证可授予性。[权限枚举][permissions]、[官方 iframe attributes](https://www.palantir.com/docs/foundry/custom-widgets/iframe-attributes)

公开 client 文件没有提供 iframe 元素、完整 sandbox 默认字符串、CSP policy、跨源 `targetOrigin`、`event.origin/source` 校验、MessagePort、token 隔离或外网 proxy 的实现。不能据此声称“没有 origin 校验”或“任意外网皆可访问”；这些责任可能在注入 bridge、服务端或闭源宿主层。外链打开、浏览器能力授权、网络访问策略、API namespace allowlist 是不同边界，不能互相替代。

生命周期也须分层：client 暴露 reload 请求与 unsubscribe 清理，但没有公开 heartbeat、自动 backoff、桥断开恢复、ready timeout、崩溃重启策略。官方 troubleshooting 指出 iframe 仍可能因内存消耗或阻塞浏览器线程而使页面无响应，隔离不等于性能隔离。[reload API][widget-messages]、[官方 troubleshooting](https://www.palantir.com/docs/foundry/custom-widgets/troubleshooting)

## 9. 对 EOS 契约设计的实施建议

以下是建议，**没有检查 EOS 源码**。从 Palantir 可见契约推导的核心要求不是“接上 iframe 就完成组件平台”，而是分别管理配置、wire 协议、数据访问和 React adapter 的演进。

| EOS 工作面 | 可实施建议 | 为什么需要单独交付 |
|---|---|---|
| Registry | 同时记录 artifact digest、组件版本、schema version、adapter version、host protocol range；保存公开来源及构建证明 | npm package、wire API、manifest 和用户固定组件版本相互独立 |
| Schema / 编辑器 | 给生成器和运行时共用一份可校验 schema；编辑器用同一 schema 生成表单，限制双向参数与事件更新白名单 | TypeScript 类型和 narrow guards 无法承担不可信运行时输入验证 |
| Adapter | 明确 props 值、loading/reloading/error、输出事件、异步对象集转换、旧值策略及清理 | React callback 不能直接成为跨宿主协议；数据 RID 是引用而非已加载对象数组 |
| Runtime | 明确宿主权威状态、事件 ack/error、revision、并发覆盖策略、超时与断连恢复，并测试 origin/source/permission enforcement | 当前公开 client 没有给出这些能力的完整实现证据 |
| AI 生成链 | 在生成后运行 config/type/manifest 检查、实际 artifact probe、adapter mock、浏览器 iframe 测试，最后再真实宿主验收 | 代码能渲染不代表变量绑定、权限、事件和发布兼容完成 |
| 契约升级 | 对旧 schema、旧 artifact 和新宿主组合做 fixture；保留 deprecated 字段迁移策略和可回滚构建 | `objectType` → `allowedType` 与仍保留 `objectTypeRids` 展示了兼容迁移的实际成本 |

建议明确规定：组件新增可选参数怎样取默认值，删除/改型参数如何迁移现有绑定，事件输出改名如何兼容，read-only 输出如何拒绝，异步请求后来的结果是否可覆盖较新的用户意图。Palantir 客户端可为这些问题提供契约切面，但不是一套可直接复制的完整宿主答案。

## 10. 本次验证记录与真实租户待验项

[client probe](evidence/protocol-client-probe.json) 的 13 条断言覆盖：missing bridge、构造不自动 ready/subscribe、协议 ready 版本、原样参数转发、未知消息忽略、emit 不生成宿主确认、reload/resize、unsubscribe/re-subscribe、浅类型 guard、defineConfig identity、无类型非法 event/parameter pass-through、generic sendMessage pass-through、placeholder token。mock 仅替换 injected bridge；没有替换包实现。[类型 probe](evidence/protocol-types-probe.json) 独立验证声明的正负例；没有声称运行了整个上游 Vitest suite。

| 待验项 | 需要的证据 | 当前状态 |
|---|---|---|
| schema → 配置面板 | 真租户选类型、绑定变量、empty/default/error 控件截图和操作记录 | 未验证 |
| host 输入与事件 | 参数更新及副作用的实际时序、部分 map、并发、错误、撤销与刷新 | 未验证 |
| 传输安全 | 实际 injected bridge / iframe transport 与 origin/source 校验 | 未验证；公开 client 不含完整实现 |
| OSDK 身份 | 不同查看者、对象权限、Action 权限、API allowlist、token replacement | 未验证 |
| 故障恢复 | 首屏 bridge 缺失、ready 不回复、iframe reload/crash、host mount/unmount | wrapper 的部分行为已 mock；真实宿主未验证 |
| 新 / 旧版本组合 | 旧 binding + 新 schema、地图实验参数与额外权限、版本固定/回滚 | 未验证 |

[parameters-wire]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/parameters.ts#L83-L85
[parameters-types]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/parameters.ts#L21-L54
[parameters-union]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/parameters.ts#L77-L124
[objectset-value]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/parameters.ts#L68-L75
[map-value]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/parameters.ts#L56-L66
[config-widget]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/config.ts#L69-L86
[config-parameters]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/config.ts#L24-L67
[config-map-experimental]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/config.ts#L33-L37
[config-readonly]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/config.ts#L93-L98
[config-derived]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/config.ts#L103-L186
[define-config]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/config.ts#L191-L195
[async-value]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/utils/asyncValue.ts#L17-L58
[host-messages]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/messages/hostMessages.ts#L25-L46
[host-guards]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/messages/hostMessages.ts#L48-L81
[widget-messages]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/messages/widgetMessages.ts#L31-L97
[widget-guards]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/messages/widgetMessages.ts#L99-L147
[client-interface]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client/src/client.ts#L27-L79
[client-bridge]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client/src/client.ts#L81-L121
[client-methods]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client/src/client.ts#L123-L162
[host-event-target]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client/src/host.ts#L24-L66
[token-provider]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client/src/tokenProvider.ts#L17-L24
[permissions]: https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/permissions.ts#L20-L37
