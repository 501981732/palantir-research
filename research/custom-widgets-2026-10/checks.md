# 验证记录与交付边界

核验日：2026-10-01 UTC。范围：官方公开文档、固定版本 npm 工件与源码、隔离客户端探针、公开模板构建和媒体证据。

本记录区分工件审计、模拟宿主检查与真实平台验收。未验证真实 Workshop / Registry、Foundry CI 或 EOS 源码；各项 PASS 只适用于表中注明的环境和范围。

## 1. 检查结果：实包、类型、构建、媒体分别记账

| 检查面 | 结果 | 证据 / 实际限制 |
| --- | --- | --- |
| API/client 实际 npm | 3.74.0 两包 digest、SRI、provenance 提交与 subject 匹配；12 个原始 source-map 源与发布 SHA 一致 | [npm checks](evidence/protocol-npm-checks.json)、[source compare](evidence/protocol-npm-source-compare.json)；未独立验证证书/透明日志签名链 |
| Client 运行探针 | 13 条断言 PASS | [client probe](evidence/protocol-client-probe.json)；实际包 + 模拟 injected API，不是真 Workshop / postMessage / origin / 权限测试 |
| API 类型正负例 | 正例通过；去除 expected-error 后 5 个非法例被拒绝 | [types probe](evidence/protocol-types-probe.json)；TypeScript 5.5.4，不证明日期格式/number范围的运行校验 |
| React adapter 来源 | 3.74.0 tarball hash 与 7 个 runtime 原始源匹配 | [react-release](evidence/react-release.json)；与当前 main 分开锁定 |
| React Components 来源 | 0.61.0 的 ObjectTable API source map 与独立发布提交逐字匹配 | [UI release](evidence/react-components-release.json)；Beta，不能与 widget 3.74.0 视作同次发布 |
| React 运行探针 | 11 组 PASS | [react-probe](evidence/react-probe-results.json)；React19/JSDOM/模拟 bridge、虚构 RID，未调用后台 |
| 自编 ObjectTable adapter | strict tsc 通过，4 个非法调用由 expected-error 确认 | [typecheck log](evidence/react-typecheck.log)、[示例](probes/react-adapter/adapter-example.tsx)；未运行 ObjectTable UI，没有双向恢复 selection 的完成声明 |
| 发布工件审计 | plugin/config 33 个原始 TS 源逐字匹配；CLI/create 33 个中间 JS 条目另外审计 | [build source-map](evidence/build-source-map-audit.json)；不把中间 JS 与原 TS 的字节差异当兼容结论 |
| 官方公开脚手架 | `create-widget@3.74.0` 的 no-OSDK 变体 lint、tsc、Vite build 通过 | [artifact checks](evidence/build-artifact-checks.json)；无 token、租户、SDK mock 或真正 host |
| 插件正负例 | 14/14 与实际源码行为一致 | [build probe](evidence/build-probe-results.json)；部分非法契约在 plugin 层通过，不表示平台允许 |
| 构建复现 | 使用锁文件在新临时目录复跑成功，10 个构建文件 hash 与首轮一致 | [artifact reproduction](evidence/build-artifact-checks.json)、[复现脚本](probes/build-reproduce.sh)；ZIP root 检查没有上传 |
| PR/案例沿革 | merged/open/draft、发布时间与固定提交记录 | [lineage PR](evidence/lineage-pr-state.json)、[React PR](evidence/react-pr-status.json)；draft 方向不作为稳定能力 |
| 媒体 | 14 张官方原图 + 1 张真实作者录像帧，15 项尺寸/bytes/SHA/出处与逐图视检 PASS | [media checks](evidence/media-checks.json)、[台账](assets.md)；仅 03:36.36 一帧，不称完整交互/发布录像 |
| 本地装配 | Markdown 文件/锚点、JSON、媒体 hash、五专题不变检查 | [assembly-checks](evidence/assembly-checks.json)、[独立审阅装配](evidence/review-assembly.json)；最终结果以机器记录为准 |
| 外部链接 | 公开 HEAD 响应与正常读取记录 | [http checks](evidence/http-checks.json)；200 不证明内容/锚点/视频可播放，拒绝或超时不绕过 |
| 可复现工具与代码片段 | 10 个 Python 语法检查、4 个参数帮助检查、36 个缓存源码对照及 2 包静态检查；React 片段 strict tsc 通过 | [范围与结果](evidence/publication-checks.json)；此项未重新执行 13/11/14 运行探针，无网络或租户请求 |

本轮没有运行上游整个 monorepo Vitest suite。作者 tests 已读，用于说明特定代码语义；本地独立 probes 用于复核实际发布包的窄接口。自编 example 与真实官方 template 分开标记，防止误称租户应用成功。

最终装配扫描 16 个 Markdown、37 个 JSON、393 个本地链接及 7 个锚点；15 项媒体 hash/bytes 全部一致。公开 HEAD 清单包含 176 个唯一 URL，其中 173 项响应 200；3 个 YouTube 入口未取得 HEAD 响应，浏览器取帧结果另行记录。计数与具体项目以机器记录为准。

## 2. 技术复核范围

技术复核核对公开文档、固定发布源码及已保存的 probe 结果，检查注入 API 与闭源 transport 的分界、mock 与真实 Workshop 的分界、版本与权限层次、未合并方向以及 EOS 建议的来源边界。Vite plugin 仅实施局部校验，permissions 原样进入 manifest；React Components 0.61.0 为独立发布的 Beta 依赖。

这项复核没有重新执行 13 条客户端断言、11 组 React 检查或 14 条插件探针，不应称为其独立复算通过。实际探针结果仍以表中原运行记录为准；复核方法及未验证范围见 [review-findings](evidence/review-findings.md)。

## 3. 媒体和网络未完成项

正常 Chrome 一次成功取得 Ontologize 正片 **03:36.36** 帧（readyState 4）；内容是 Code Workspace welcome、dev server 与预览加载状态，不能证明完整 UI/事件交互。后续重要章节和第二条 objectSet 教学视频在正常跳转/刷新后未可靠加载，错误/广告/stale 片头均不当证据。两条视频标准字幕导出不可用，未补造字幕。

**未取得真实短录屏或可用字幕**。连续正片未达到可靠采集状态；metadata-only 读取与编码可用性检查的命令、版本和结果见 [媒体检查记录](evidence/media-attempts.json)。这些获取结果不构成 Palantir 产品能力或故障的证据。

官方 npm 网页未取得有效响应的项目使用公开 registry 元数据核验版本。公开来源的状态记录与技术结论分开；文档正文未作为整页镜像提交。

## 4. 本地复跑入口

```sh
# 装配检查；不联网，不执行包安装或生产操作。
python3 research/custom-widgets-2026-10/probes/check-review-pack.py
python3 research/custom-widgets-2026-10/probes/check-assembly.py 9a3bf0898d1505cc34fb5823d22042025b7b7a1f
```

协议 probe 的隔离依赖准备见 [protocol-client.mjs](probes/protocol-client.mjs) 开头；React 锁文件与命令见 [React probe README](probes/react-adapter/README.md)；官方 no-OSDK 模板、锁文件和完整构建命令见 [build-reproduce.sh](probes/build-reproduce.sh)。公开源码、npm 下载与 HTTP 检查需要正常网络；已有检查结果可先离线审阅。

本地 script 使用临时目录/研究虚构 RID，不接入 Foundry。不把脚本里的 placeholder token/RID 当有效资源，重跑也不需要租户凭据。

## 5. 真实宿主与 EOS 仍需的验收

- 真实 Workshop：schema 到配置面板、输入完整性、事件/echo 时序、ObjectSet/scenario、Action 刷新、身份/权限/API allowlist。
- 真浏览器 runtime：实际 transport/origin、CSP、media/download、storage 限制、remount/keep-mounted、首屏/崩溃/资产失败恢复。
- 真发布：Foundry CI、Registry 上传与固定引用、显式升级/绑定迁移、恢复旧版本；没有把本地 ZIP 当成功发布。
- EOS：实际 Registry 定义、Adapter 语义、Compiler/DSL/创建保存链、生命周期与发布可追溯性；本轮没读取其源码。

这些是后续证据缺口，不阻止审阅本轮已完成的公开事实与建议；它们也不能用本地 PASS 代替。
