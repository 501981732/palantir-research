# 实际 npm 发布包核验：widget.api / widget.client

核验日期：2026-10-01。元数据第一次抓取时间为 `2026-10-01T04:13:40.314561Z`，以 [protocol-npm-audit.json](protocol-npm-audit.json) 中的 UTC 时间为准。

**结论：两包当日的 `latest`、最高稳定语义版本和最近发布稳定版本均为 `3.74.0`。实际 tarball 的 SHA-1 与 SHA-512 均匹配官方 registry；其中内嵌的 12 个 TypeScript 源文件，与 npm provenance 声明的发布提交 `fb8ec172d540ef7819382ff036aa2a692614af75` 全文一致。** 这锁定了研究中的公开客户端实现，不能验证 Workshop 闭源宿主如何执行它。

## 1. 版本、包内容和完整性

| 包 | 稳定版本 | 官方发布时间（UTC） | tarball 大小 | 文件数 / 解包大小 | 运行时依赖 |
| --- | --- | --- | ---: | --- | --- |
| [`@osdk/widget.api`](https://registry.npmjs.org/@osdk%2fwidget.api/3.74.0) | 3.74.0 | 2026-09-29 17:25:06.301 | 25,928 bytes | 53 / 153,783 bytes | `@osdk/api: 2.75.0` |
| [`@osdk/widget.client`](https://registry.npmjs.org/@osdk%2fwidget.client/3.74.0) | 3.74.0 | 2026-09-29 17:20:31.590 | 12,978 bytes | 29 / 81,192 bytes | `@osdk/widget.api: ~3.74.0`、`tiny-invariant: ^1.3.3` |

每包都有 browser、ESM、CJS 与类型声明产物；`package.json` 的 `license` 均为 `Apache-2.0`。此次只下载、解包、读取文本和计算摘要，没有执行安装脚本或包代码。每个解包文件的相对路径、大小、SHA-256 均保存在 audit JSON 中。

| 包 | tarball SHA-256 | registry `dist.shasum`（SHA-1；已实算匹配） |
| --- | --- | --- |
| widget.api | `219b56aa5f91a6fbb1933d5042d8120ef069ec26eaa5b10ce5ee21ac75c84074` | `8fa10b761df7280785d76311b8fddfdded93136d` |
| widget.client | `2539c7c40cc027946bb8a6ccfbf23116732ef7bfc6ec48b8673db169583515b4` | `b68066b97b28e174ed94fa231be43ec1921146c0` |

完整 SHA-512 `dist.integrity`、实算值及 `integrityMatches: true` 见 audit JSON。官方 tarball：[`widget.api-3.74.0.tgz`](https://registry.npmjs.org/@osdk/widget.api/-/widget.api-3.74.0.tgz)、[`widget.client-3.74.0.tgz`](https://registry.npmjs.org/@osdk/widget.client/-/widget.client-3.74.0.tgz)。

## 2. 发布源码锚点与实现一致性

[protocol-npm-source-compare.json](protocol-npm-source-compare.json) 保存逐文件的源 URL、两侧 SHA-256 和全文比较结果。方法是读取实际 tarball 中 browser `.js.map` 的 `sourcesContent`，与官方 GitHub 固定提交的 `.ts` 文件进行比较。**没有仅按版本号推断同源。**

| 固定提交 | 角色 | source `package.json` 版本 | widget.api 源文件全文匹配 | widget.client 源文件全文匹配 |
| --- | --- | --- | ---: | ---: |
| [`fb8ec172…`](https://github.com/palantir/osdk-ts/tree/fb8ec172d540ef7819382ff036aa2a692614af75) | npm provenance 声明的 release 源码 | 3.74.0 | 8 / 8 | 4 / 4 |
| [`e53b94ec…`](https://github.com/palantir/osdk-ts/tree/e53b94ecd5de7cdd7e864d0daa04363bdad4db4c) | 本次研究选定的较新 main 源码快照 | 3.74.0 | 8 / 8 | 4 / 4 |
| [`37cfd386…`](https://github.com/palantir/osdk-ts/tree/37cfd38676bf04edaef5847e929d914ea214c149) | 既有专题使用过的旧快照 | 3.72.0 | 8 / 8 | 4 / 4 |

`widget.api` 比较的文件是 `config.ts`、`index.ts`、`manifest.ts`、`parameters.ts`、`permissions.ts`、`messages/hostMessages.ts`、`messages/widgetMessages.ts`、`utils/asyncValue.ts`；`widget.client` 是 `client.ts`、`host.ts`、`index.ts`、`tokenProvider.ts`。

这三个提交的上述实现文件一致，不代表包版本、所有仓库文件或全部依赖一致。release/main 的 source manifest 与发布 manifest 的逻辑 JSON 差异只有 `dependencies` / `devDependencies`：源码中的 `workspace:*`、`workspace:~` 被发布为实际版本或版本范围。旧 `37cfd386…` 还存在 `version: 3.72.0` 与 `3.74.0` 的差别。具体键和值见 [protocol-npm-artifact-details.json](protocol-npm-artifact-details.json)。

## 3. 实际出口与打包边界

两个包的根出口 `.` 指向的 browser JS、ESM JS、ESM types、CJS JS 和 default 文件均存在。所有 browser `.js` 与对应 ESM `.js` 全文一致。artifact details 保存了两个实际 `build/types/index.d.ts` 的根出口快照及摘要。

- `widget.api` 根出口覆盖 config、manifest、host/widget 消息判别与 visitor、`ParameterValue` / `AllowedObjectSetParameterType`、`BrowserPermission`、异步值类型等；不少名称是 TypeScript 类型，不是运行时对象。
- `widget.client` 根出口包含 `createFoundryWidgetClient`、`FoundryHostEventTarget`、`createFoundryWidgetTokenProvider`，并转导出一部分 API 契约。
- 实际 `FoundryWidgetClient` 类型含 `ready`、`reload`、`resize`、`emitEvent`、`sendMessage`、`subscribe`、`unsubscribe` 与 `hostEventTarget`。实际 browser `client.js` 读取 `window.__PALANTIR_WIDGET_API__`；这里不把实现包装成已验证的 Workshop iframe 或 `postMessage` 协议。
- 两包也声明通配子路径 `./*` → `build/*/public/*`，但实际 tarball 没有对应 `public` 文件：五个条件目标的匹配文件数均为 0。研究示例应使用包根命名导入。此项是**文件清单检查**，未在这里执行 consumer 深导入测试，也未将其扩大为整包不可用的结论。

发布包 `CHANGELOG.md` 显示 `3.74.0` 的这两个条目均为依赖推进；最新明确功能条目包括 `widget.api 3.72.0` 的 `allow-modals`、`3.71.0` 的 `mapTileLayer`。历史中也有 scenario、interface object-set、HMR reload、manifest authorizations 等演进线索。应继续回到对应提交/PR 验证具体实现，不把 changelog 文案视为宿主兼容承诺。经过有界摘取的相关条目保存在 artifact details。

## 4. npm provenance 的证据等级

已独立读取官方 [`widget.api` attestation](https://registry.npmjs.org/-/npm/v1/attestations/@osdk%2fwidget.api@3.74.0) 和 [`widget.client` attestation](https://registry.npmjs.org/-/npm/v1/attestations/@osdk%2fwidget.client@3.74.0)。解码后的 publish / SLSA statement 见 [protocol-npm-provenance.json](protocol-npm-provenance.json)：

- 两包的 statement subject SHA-512 均与实际下载 tarball 对应；四个 subject 核对均通过。
- SLSA 声明的 source `gitCommit` 均为 `fb8ec172d540ef7819382ff036aa2a692614af75`。
- 声明的 workflow 为 `.github/workflows/release.yml`、`refs/heads/main`，builder 为 GitHub hosted runner，invocation 为 [release run 36603145053 / attempt 1](https://github.com/palantir/osdk-ts/actions/runs/36603145053/attempts/1)。

**边界：此处完成的是 HTTPS registry 读取、payload 解码、subject 摘要关联与源码全文核对；没有进行 Sigstore 证书、DSSE 签名、Rekor inclusion proof 的密码学验证。** npm registry 元数据本身没有 `gitHead`，不能用该字段声称发布来源已获验证。

## 5. 复核与保存范围

以下命令在本专题目录下运行；前两个和最后一个需要对官方公开 npm / GitHub 的正常网络访问。后续复核应传入 `--version 3.74.0` 固定已研究版本，同时脚本仍会记录复核时 registry 的稳定版标签。网络抓取会重写本地 JSON 的检索时间，正式归档后如需保留首轮记录，应另存副本。

```bash
python3 evidence/protocol-npm-fetch.py --version 3.74.0
python3 evidence/protocol-npm-source-compare.py
python3 evidence/protocol-npm-artifact-inspect.py
python3 evidence/protocol-npm-provenance-fetch.py
```

本目录保留有界 JSON、接口出口快照、摘要和可复核脚本，不提交整个 npm tarball、整个仓库或凭据。下载包与原始源码使用可指定的临时目录，不把个人绝对路径写入证据；脚本可以重新取得相同固定版本内容。`protocol-npm-fetch.py` 接受 `--artifacts-dir`；比较和检查脚本接受 `--artifacts-dir` / `--sources-dir`，默认目录位于系统临时目录。三个步骤需使用相同目录参数。

最终静态核验结果见 [protocol-npm-checks.json](protocol-npm-checks.json)。本项静态工件审计不包含模拟宿主或真实 Workshop 测试；协议客户端和 React 探针的结果分别记录，均不代替真实租户验收。
