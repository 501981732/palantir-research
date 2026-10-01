# React 适配来源台账

取得日均为 2026-10-01。下表均为一手来源，不是 vendor 文档镜像。固定代码引用保持 Git SHA，官方文档页面未提供可核实的最后修改日期。未储存来自这些来源的图像或长视频。

| ID | 来源 / 直接 URL | 版本 / 日期锁定 | 本次用途及边界 |
|---|---|---|---|
| R00 | [@osdk/widget.client-react npm](https://registry.npmjs.org/@osdk%2Fwidget.client-react) | 3.74.0；发布 2026-09-29 | npm 官方 registry；time、version、dist、peers。 |
| R00T | [@osdk/widget.client-react npm](https://registry.npmjs.org/@osdk/widget.client-react/-/widget.client-react-3.74.0.tgz) | 3.74.0；发布 2026-09-29 | 真实 npm wrapper tarball，SHA-256 和 sourcesContent 已核对。 |
| R00P | [@osdk/widget.client-react npm](https://registry.npmjs.org/-/npm/v1/attestations/@osdk%2fwidget.client-react@3.74.0) | 3.74.0；发布 2026-09-29 | publisher provenance 解码，固定 wrapper 发布 SHA；未独立验 Sigstore 证书链。 |
| R01 | [client.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/client.tsx) | 固定 fb8ec17；wrapper发布组合3.74.0 | 公开 wrapper 全文件，与真实 3.74.0 source map 逐字匹配。 |
| R01A | [client.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/client.tsx#L40-L141) | 固定 fb8ec17；wrapper发布组合3.74.0 | props、初始参数、create client、emit callback。 |
| R01B | [client.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/client.tsx#L143-L232) | 固定 fb8ec17；wrapper发布组合3.74.0 | 入站 merge 与便利聚合状态。 |
| R01C | [client.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/client.tsx#L99-L141) | 固定 fb8ec17；wrapper发布组合3.74.0 | 同步/异步 emit、per-event call ID、void 返回。 |
| R01D | [client.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/client.tsx#L143-L290) | 固定 fb8ec17；wrapper发布组合3.74.0 | effect、ready、resize、HMR、cleanup 和 Provider 边界。 |
| R02 | [context.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/context.ts) | 固定 fb8ec17；wrapper发布组合3.74.0 | 公开 context 全文件，与真实 3.74.0 source map 逐字匹配。 |
| R02A | [context.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/context.ts#L75-L127) | 固定 fb8ec17；wrapper发布组合3.74.0 | context 字段及泛型 map。 |
| R02B | [context.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/context.ts#L146-L160) | 固定 fb8ec17；wrapper发布组合3.74.0 | withTypes 只作类型绑定。 |
| R02C | [context.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/context.ts#L129-L150) | 固定 fb8ec17；wrapper发布组合3.74.0 | 默认 context 与无 Provider 的行为。 |
| R02D | [context.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/context.ts#L34-L73) | 固定 fb8ec17；wrapper发布组合3.74.0 | React ObjectSet 输出类型及 emit 返回 void。 |
| R03 | [index.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/index.ts#L17-L19) | 固定 fb8ec17；wrapper发布组合3.74.0 | 根入口实际 exports。 |
| R04 | [asyncValue.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/utils/asyncValue.ts#L17-L58) | 固定 fb8ec17；wrapper发布组合3.74.0 | 五种 AsyncValue 状态；undefined 与旧值。 |
| R05 | [config.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/config.ts#L93-L146) | 固定 fb8ec17；wrapper发布组合3.74.0 | 参数/event 的类型 map。 |
| R05A | [config.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/config.ts#L33-L72) | 固定 fb8ec17；wrapper发布组合3.74.0 | allowedType、deprecated objectType 与兼容 manifest。 |
| R06 | [initializeParameters.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/utils/initializeParameters.ts#L24-L34) | 固定 fb8ec17；wrapper发布组合3.74.0 | not-started 初始化形状。 |
| R07 | [extendParametersWithObjectSets.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/utils/extendParametersWithObjectSets.ts#L33-L102) | 固定 fb8ec17；wrapper发布组合3.74.0 | ObjectSet RID 水合、缓存及输入检查分支。 |
| R08 | [transformEmitEventPayload.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/utils/transformEmitEventPayload.ts#L52-L136) | 固定 fb8ec17；wrapper发布组合3.74.0 | ObjectSet 输出序列化；同步 passThrough 与 async helper。 |
| R09 | [client.test.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/client.test.tsx#L88-L322) | 固定 fb8ec17；wrapper发布组合3.74.0 | 4 个作者竞态 tests；已审计未运行。 |
| R10 | [parameters.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/parameters.ts#L21-L110) | 固定 fb8ec17；wrapper发布组合3.74.0 | scenario/mapTileLayer/wire 参数值。 |
| R11 | [withScenario.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/client/src/scenarios/withScenario.ts#L23-L49) | 固定 fb8ec17；wrapper发布组合3.74.0 | OSDK withScenario 的实验状态；非 widget 的自动水合。 |
| R12 | [widgetMessages.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/messages/widgetMessages.ts) | 固定 fb8ec17；wrapper发布组合3.74.0 | typed widget 消息；context 没有任意导航服务。 |
| R12A | [hostMessages.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.api/src/messages/hostMessages.ts) | 固定 fb8ec17；wrapper发布组合3.74.0 | host 消息版本、typed update-parameters。 |
| R13 | [index.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/react/src/index.ts#L17-L28) | 固定 fb8ec17；wrapper发布组合3.74.0 | OSDK React root OsdkProvider 导出。 |
| R14 | [ObjectTableApi.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L885-L927) | 固定 37cfd38；react-components0.61.0，2026-09-28 发布 | 0.61.0 ObjectTable RowSelectionChange；actual source map ↔ 固定发布源码逐字匹配。 |
| R14A | [ObjectTableApi.ts](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/src/object-table/ObjectTableApi.ts#L593-L626) | 固定 37cfd38；react-components0.61.0，2026-09-28 发布 | 0.61.0 受控 selection props。 |
| R15 | [ErrorBoundary.tsx](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/ErrorBoundary.tsx#L23-L89) | 固定 fb8ec17；wrapper发布组合3.74.0 | children ErrorBoundary 行为与限制。 |
| R16 | [client.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client/src/client.ts#L28-L151) | 固定 fb8ec17；wrapper发布组合3.74.0 | 公开 client ready/api 版本，不是 widget set 版本。 |
| R17 | [extendParametersWithObjectSets.test.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/utils/extendParametersWithObjectSets.test.ts) | 固定 fb8ec17；wrapper发布组合3.74.0 | 7 个作者水合 tests；已审计未运行。 |
| R18 | [transformEmitEventPayload.test.ts](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/widget.client-react/src/utils/transformEmitEventPayload.test.ts) | 固定 fb8ec17；wrapper发布组合3.74.0 | 5 个作者序列化 tests；已审计未运行。 |
| R19 | [README.md](https://github.com/palantir/osdk-ts/blob/37cfd38676bf04edaef5847e929d914ea214c149/packages/react-components/README.md#L1-L3) | 固定 37cfd38；react-components0.61.0，2026-09-28 发布 | react-components 的 Beta 状态。 |
| D01 | [dark-theme](https://www.palantir.com/docs/foundry/custom-widgets/dark-theme) | 2026-10-01 读取；页面更新时间未知 | 官方 CSS/JS 配色检测指导；未实测租户 theme。 |
| D02 | [auto-sizing](https://www.palantir.com/docs/foundry/custom-widgets/auto-sizing) | 2026-10-01 读取；页面更新时间未知 | 官方 auto vs absolute/flex 尺寸指导；最低 client-react3.3.0。 |
| D03 | [open-url-in-workshop](https://www.palantir.com/docs/foundry/custom-widgets/open-url-in-workshop) | 2026-10-01 读取；页面更新时间未知 | 官方 Workshop Open URL 副作用指导与 async transform 限制。 |
| D04 | [iframe-attributes](https://www.palantir.com/docs/foundry/custom-widgets/iframe-attributes) | 2026-10-01 读取；页面更新时间未知 | iframe capability 指导；与宿主 Open URL 区分。 |

## 作者 PR 与 review 讨论

| PR | 一手链接 | 截至研究日状态 | 用途 |
|---|---|---|---|
| #2033 | [Add object set support to widgets config](https://github.com/palantir/osdk-ts/pull/2033) | merged 2025-10-07T11:19:10Z | ObjectSet envelope 设计来源 |
| #2294 | [Improved object set writes](https://github.com/palantir/osdk-ts/pull/2294) | merged 2025-12-19T11:35:02Z | 输出自动序列化、per-event call ID、同步兼容；旧 body 拼法不作现行 API |
| #2214 | [[widgets] Error boundary](https://github.com/palantir/osdk-ts/pull/2214) | merged 2025-11-27T19:47:53Z | 初始化渲染错误与宿主 spinner 动机 |
| #2216 | [[widgets] expand ErrorBoundary to catch all errors](https://github.com/palantir/osdk-ts/pull/2216) | merged 2025-11-29T00:46:45Z | 扩大 fallback，而非捕获所有异步错误 |
| #2218 | [Backport widget fixes](https://github.com/palantir/osdk-ts/pull/2218) | merged 2025-12-01T11:04:13Z | release/2.5.x backport |
| #3023 | [Support reloading widget on vite HMR full reload](https://github.com/palantir/osdk-ts/pull/3023) | merged 2026-05-18T12:09:16Z | Vite full reload 父子生命周期协作 |
| #2545 | [[custom widgets] lazy load @osdk/client](https://github.com/palantir/osdk-ts/pull/2545) | open / unmerged；2026-10-01 查询 | lazy load 提案，仍未合并，不能作已发布能力 |
| #2538 | [[custom widgets] HMR for widget config files](https://github.com/palantir/osdk-ts/pull/2538) | merged 2026-02-17T11:04:23Z | config HMR 与宿主 dev reload 的边界 |
| #2474 | [[custom widgets] support interfaces in object set parameters](https://github.com/palantir/osdk-ts/pull/2474) | merged 2026-02-06T16:32:53Z | allowedType/interface breaking source change；minor changeset 和 backend manifest 迁移 |

- [#2294 同步/异步兼容 review](https://github.com/palantir/osdk-ts/pull/2294#discussion_r2631152449)：同步参数连续事件不宜被 ObjectSet 的丢弃语义覆盖。
- [#2294 emitEventAsync 提议](https://github.com/palantir/osdk-ts/pull/2294#discussion_r2627269147)：作者讨论未来可能 API，未纳入此次3.74.0公共context。

## 其余版本和文档入口

- [react-components0.61.0 npm metadata](https://registry.npmjs.org/@osdk%2Freact-components/0.61.0)、[完整 registry](https://registry.npmjs.org/@osdk%2Freact-components)：实际版本、integrity、2026-09-28T14:10:56.505Z 发布记录。
- [react-components0.61.0 provenance](https://registry.npmjs.org/-/npm/v1/attestations/@osdk%2freact-components@0.61.0)、[publisher release invocation](https://github.com/palantir/osdk-ts/actions/runs/36432616035/attempts/1)：固定37cfd38发布源，非独立证书验证。
- [widget.client-react3.74.0 release invocation](https://github.com/palantir/osdk-ts/actions/runs/36603145053/attempts/1)：provenance里的发布执行身份来源，未重跑发布。
- [参数与事件官方文档](https://www.palantir.com/docs/foundry/custom-widgets/parameters-and-events)：文档中的历史 OsdkProvider2 import 与实际2.75.0 root provider 区分。
- [useDarkTheme 官方模板](https://github.com/palantir/osdk-ts/blob/fb8ec172d540ef7819382ff036aa2a692614af75/packages/create-widget.template.react.v2/templates/src/useDarkTheme.ts)：matchMedia/change/cleanup 的可执行官方示范；未在真宿主运行。

## 可复核本地产物

- [react-release.json](react-release.json)：wrapper发布、hash、source-map 7文件匹配。
- [react-components-release.json](react-components-release.json)：UI库独立发布和ObjectTable API匹配。
- [react-pr-status.json](react-pr-status.json)：9个PR的状态/日期/merge SHA。
- [react-probe-results.json](react-probe-results.json)：实际公开客户端 + 模拟宿主，11组PASS。
- [react-typecheck.log](react-typecheck.log)：自编输出adapter与4个类型负例，tsc退出0。
- [探针复跑说明](../probes/react-adapter/README.md)：npm依赖锁、边界、首次mock RID失败及修正。
