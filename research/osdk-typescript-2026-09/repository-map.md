# osdk-ts 全仓地图、测试与发布边界

研究日：2026-10-01。仓库地图固定 main `e53b94ecd5de7cdd7e864d0daa04363bdad4db4c`；关键运行链在 [架构正文](README.md) 分别固定实际 npm 发布源。地图不是所有包行为的详审。

## 1. 范围与计数

本次读取 `packages/*/package.json` 共 **95** 个目录，44 个 `private:true`、51 个未设 private；全部 manifest 声明 Apache-2.0。这是包目录计数，**不是已发布 npm 包数，也不是整个 workspace 数**。workspace 还含 examples/examples-extra/tests/benchmarks/docs。[workspace globs](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/pnpm-workspace.yaml#L1-L8)、[机器清单](package-inventory.json)

## 2. 包地图与深度边界

| 家族 | 代表包 | 责任 | 本次深度 |
|---|---|---|---|
| 本体类型 | api | 对象/接口/Action/Query、集合/谓词/实例/media 类型 | 运行与类型边界深入 |
| SDK 编译 | generator、generator-converters*、generator-utils、foundry-sdk-generator | metadata 规范化、类型与包生成 | 主要生成链深入；周边工具清单 |
| 运行时 | client、client.unstable、shared.client.impl、shared.net* | dispatch、ObjectSet、Action、Query、transport/errors | 关键链深入 |
| 认证 | oauth | public/confidential/authless，token-provider seam | 发布源与行为深入 |
| 响应数据 | client/observable、react、react-devtools | cache/optimistic/subscriptions 与 React bridge | cache/hooks 深入；devtools 范围清单 |
| UI | react-components、react-components-storybook、cbac-components | wrapper/Base/parts/CSS、stories，CBAC 迁移 | 独立[组件篇](../osdk-react-components-2026-09/) |
| 应用脚手架 | create-app* | 应用模板与 bootstrap | 模板 manifest/入口清单，不验证全部新建应用 |
| 嵌入宿主 | create-widget*、widget.api、widget.client*、widget.vite-plugin | host/child 参数事件、widget 构建 | public manifest 和模板边界，非完整宿主行为审计 |
| Ontology-as-code / 本地 | maker*、faux、aliases、vite-plugin-oac、vite-plugin-branch | authoring、仿真与开发反馈循环 | 地图/声明；不自动等同 Foundry 完整服务 |
| AI / Functions | aip-core、language-models、agents、functions | 邻近 runtime；AIP 接 React/UI | 主要依赖与导出，不做全部 Agent 运行审计 |
| 测试/seed | unit-testing、integration-testing、seed-helpers/compiler、shared.test*、e2e.* | fixtures、mock/seeds、integration | 关键测试源码阅读，未整仓执行 |
| 仓库基础设施 | monorepo.*、tool.release、doc generators | 构建/type/export/docs/release | 固定版本与发布渠道审读 |

主要公开入口：[api](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/api/src/index.ts)、[client](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/client/src/index.ts)、[generator](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/generator/src/index.ts)、[react](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/react/src/index.ts)、[oauth](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/oauth/src/index.ts)。其他家族的类别来自 manifest/目录，不把“已盘点”写成每种行为已验证。

“全仓研究”的有效交付是系统地图 + 决策关键路径的深入追踪，不能用 95 个包同样长的介绍替代 architecture。EOS 的适配决策主要由 codegen/type/runtime/cache/React 和宿主边界决定，其他邻近包保留后续深入入口。

## 3. 版本族与 release 渠道

Changesets fixed groups 把 api/client/react/codegen/create-app 核心族耦合；CLI 和 widget 分别有自己的固定族。components 与 OAuth 不在上述核心固定族中。package publishConfig public 与 Changesets 默认 restricted 要一起读，默认值不说明所有包私有。[changeset config](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/.changeset/config.json#L1-L54)、[组件 publishConfig](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/react-components/package.json#L355-L357)

release workflow 监听 main/release/*/next，正式 release job 对 main/release/* 运行 ciPublish；snapshot job 计算 snapshot 并以 `next-${branch}` 发布。根 standalone snapshot script 则使用 `next`。**channel 要同时看 workflow、branch、版本、dist-tag**，不能给所有 next/beta 一致产品含义。[release.yml](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/.github/workflows/release.yml#L1-L88)、[ciPublish](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/tool.release/src/ciPublish.ts#L25-L64)、[root scripts](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/package.json#L6-L30)

main 的 api/client/react/generator 2.75.0、components 0.61.0 是 manifest 观察；本文另通过 registry/provenance 实证 npm。GitHub release collection 又是第三个面，不用 “GitHub newest release” 代替 npm latest。部分 e2e.generated fixtures 为真实 beta semver，也不意味着全 core runtime 都 Beta。

## 4. 测试体系是什么，证明到哪里

| 层 | 阅读的代表验证 | 本次能说什么 |
|---|---|---|
| generator | 生成文件、manifest、foreign refs、metadata export、版本冲突 | 设计契约与 snapshot；未生成真实用户 SDK |
| API 类型 | quickinfo / intellisense / test-d | IDE/type 契约，不等于运行行为 |
| client | list key、canonicalizer、invalidation、Action optimism、websocket | 关键算法意图；未重跑全套 |
| React | Provider 稳定、Hook 订阅、action pending/error | mock 状态桥接覆盖；非实际 Foundry 权限 |
| UI | table/filter/form/viewer/base 单元和 stories | 有预期断言；实际执行的有限 probes/截图在组件篇单列 |
| e2e / integration | generated SDK 与 platform 环境 fixtures | 盘点边界；没有登录执行 |

client/generator Vitest 配置使用 fork pools；React 使用 happy-dom；components 使用 happy-dom/polyfills/UTC locale/thread pool。这不是 React17/18/19 × 真实浏览器的矩阵。[client config](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/client/vitest.config.mts#L19-L26)、[generator config](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/generator/vitest.config.mts#L19-L26)、[React config](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/react/vitest.config.mts#L19-L25)、[components config](https://github.com/palantir/osdk-ts/blob/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c/packages/react-components/vitest.config.mts#L19-L31)

## 5. 与 AI 工具及 UI 专题的边界

AGENTS、生成 docs、Storybook manifest/MCP 开发配置，使类型和例子可供 AI 读取；这与 runtime cache/codegen 是互补责任。Pilot/AI FDE 的指导/实际反馈证据、SuperRepo 的组合及默认依赖未知，见[组件篇 AI 专章](../osdk-react-components-2026-09/ai-generation.md)。不在底层篇重新列组件 props，也不把 private Storybook 工具当 npm runtime API。
