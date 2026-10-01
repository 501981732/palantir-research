# React adapter research probe

研究日：2026-10-01。真实 npm packages + JSDOM / simulated injected host bridge；没有 Foundry 租户、OSDK 真数据、生产 Action、发布或外网请求。

锁定版本见 [package.json](package.json) / [package-lock.json](package-lock.json)：widget client-react/client/api 3.74.0、OSDK client/api/react 2.75.0、react-components 0.61.0、React19.1.1、JSDOM26.1.0。

react-components 0.61.0 仍为 Beta；其发布源提交与 widget wrapper 3.74.0 不同，见 [独立 API/source-map 核验](../../evidence/react-components-release.json)。

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm run probe
npm run typecheck
```

[probe.mjs](probe.mjs) 实际 import `FoundryWidget` / `useFoundryWidgetContext` / OSDK `createClient`，注入模拟 `window.__PALANTIR_WIDGET_API__`。11组检查包括 default context、initialValues聚合、scenario/mapTileLayer透传、emit与host echo、刻意不完整payload的聚合边界、resize、卸载、StrictMode重放、数组初值与ObjectSet惰性水合。没有mock `FoundryWidget` 本身，OSDK仅构造虚构ObjectSet；若有网络请求会失败。

结果见 [react-probe-results.json](../../evidence/react-probe-results.json)。不完整host消息是错误注入，不能证明真实宿主发送增量；StrictMode结果仅本地开发态。

[adapter-example.tsx](adapter-example.tsx) 为自编 ObjectTable callback→Widget event 输出适配示例，仅类型检查，没有运行ObjectTable，也没有发布manifest。MockTask为虚构定义，发布需换成含真实metadata的生成SDK export。它不恢复宿主选择集到ObjectTable受控selection。

[contract-negative.ts](contract-negative.ts) 用4个`@ts-expect-error`确认无效event、缺输出字段、错误ObjectSet wire形状和read-only地图层更新会被拒绝。

探针使用符合 RID 语法的虚构值 `ri.ontology.main.ontology.mock`，未请求、创建或验证任何真实资源。
